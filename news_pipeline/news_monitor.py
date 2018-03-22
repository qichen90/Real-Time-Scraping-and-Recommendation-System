import os
import sys
import redis
import hashlib
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import news_api_client
from cloudAMQP_client import CloudAMQPClient

SLEEP_IN_SECONDS = 10
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
CLOUD_AMQP_NAME = 'amqp://zyxttdzy:CgfaZUfBCryGa5xfxdmJEfXSpVQZ-CN8@llama.rmq.cloudamqp.com/zyxttdzy'
QUEUE_NAME = 'SCRAPE_News'

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
message_queue = CloudAMQPClient(CLOUD_AMQP_NAME, QUEUE_NAME)

def monitorOn(newsAPI_client=news_api_client):
    while True:
        news_list = newsAPI_client.getNewsList(sources=NEWS_SOURCES)
        num_of_news = 0

        for news in news_list:
            # create digest for Redis checking duplicates
            news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()
            if redis_client.get(news_digest) is None:
                num_of_news += 1
                news['digest'] = news_digest

                if news['publishedAt'] is None:
                    news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                # write in Redis
                redis_client.set(news_digest, "True")
                redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)
                # push to MQ
                message_queue.sendMessage(news)
        
        print("The number of news fetched: %d" % num_of_news)
        message_queue.sleep(SLEEP_IN_SECONDS)

if __name__ == '__main__':
    monitorOn()
