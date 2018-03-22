"""Operations functions"""
import json
import os
import sys
import redis
import pickle
from bson.json_util import dumps
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client # pylint: disable=import-error, wrong-import-position
from cloudAMQP_client import CloudAMQPClient
import news_recommendation_service_client

NEWS_TABLE_NAME = 'news'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_LIMIT = 200
NEWS_LIST_SIZE = 10
USER_NEWS_TIME_OUT = 3600 * 24

CLICK_LOGGER_QUEUE_URL = 'amqp://wznspxdt:cXB3A3r1PSBv9AeDIV2gbY0rvfaqQ2hf@skunk.rmq.cloudamqp.com/wznspxdt'
CLICK_LOGGER_QUEUE_NAME = 'Click_Logger'
click_logger_client = CloudAMQPClient(CLICK_LOGGER_QUEUE_URL, CLICK_LOGGER_QUEUE_NAME)

def get_one_news():
    """Get one news from MONGODB. """
    db = mongodb_client.get_db()
    news = db[NEWS_TABLE_NAME].find_one()
    return news

def get_news_summaries_for_user(user_id, page_num):
    """Get news list from MongoDB. """
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    db = mongodb_client.get_db()

    news_index_begin = (int(page_num) - 1)* NEWS_LIST_SIZE
    news_index_end = news_index_begin + NEWS_LIST_SIZE
    sliced_news = []

    # userid in Redis, get digest from Redis
    if redis_client.get(user_id) is not None:
        sliced_news_digests = pickle.loads(redis_client.get(user_id))[news_index_begin: news_index_end]
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest': {'$in': sliced_news_digests}}))
    # userid not in Redis, get 200 news from Mongo first
    else:
        all_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        all_news_digests = [news['digest'] for news in all_news]

        redis_client.set(user_id, pickle.dumps(all_news_digests))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT)

        sliced_news = all_news[news_index_begin: news_index_end]
    
    # get preference for user
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None
    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    # prepare news
    for news in sliced_news:
        del news['text']
        # set time chip for front-end
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
        #     now = datetime.now()
        #     news_hour = news['publishedAt'].time().hour
        #     if now.hour - news_hour <= 3:
        #         news['time'] = '%s hours ago' % (now.hour - news_hour)
        else:
            news['time'] = news['publishedAt'].date().strftime("%m/%d/%y")
        
        if news['class'] == topPreference:
            news['reason'] = 'Recommend'
        
    return json.loads(dumps(sliced_news))

def log_news_click_for_user(user_id, news_id):
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    click_logger_client.sendMessage(message)