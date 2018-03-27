import sys
import os
import datetime
from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient
import mongodb_client 
import news_topic_modeling_service_client as predictClient

with open('../config.json') as json_data_file:
    config = json.load(json_data_file)

DEDUPE_TASK_QUEUE_URL = config['cloudAMQP']['deduperTaskQueue']['url']
DEDUPE_TASK_QUEUE_NAME = config['cloudAMQP']['deduperTaskQueue']['name']

SLEEP_IN_SECONDS = config['cloudAMQP']['deduperTaskQueue']['sleep']
dedupe_task_mq_client = CloudAMQPClient(DEDUPE_TASK_QUEUE_URL, DEDUPE_TASK_QUEUE_NAME)

NEWS_TABLE_NAME = 'news'
NEWS_SIMILARITY_THREDHOLD = 0.8

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print("News data is invalid")
        return 
    
    task = msg
    text = task['text']
    if text is None:
        return 
    
    # get latest news
    published_at = parser.parse(task['publishedAt'])
    published_at_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_end = published_at_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    same_date_news_list = list(db[NEWS_TABLE_NAME].find({'published_At': {'$gte': published_at_begin, '$lt': published_at_end}}))

    # check duplicates
    if same_date_news_list is not None and len(same_date_news_list) > 0:
        documents = [news['text'] for news in same_date_news_list]
        document.insert(0, text)

        # calculate similarity
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T 

        rows, _ = pairwise_sim.shape
        for row in range(1, rows):
            if pairwise_sim[row, 0] > NEWS_SIMILARITY_THREDHOLD:
                print("Duplicate News found")
                return 
    task['publishedAt'] = parser.parse(task['publishedAt'])
    # assign class for news
    title = task['title']
    if title is not None:
        topic = predictClient.classifyForNews(title)
        task['class'] = topic
        
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)
    print("write into MongoDB table %s" % NEWS_TABLE_NAME)
        
def deduperOn():
    while True:
        if dedupe_task_mq_client is not None:
            msg = dedupe_task_mq_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as ex:
                    print(ex)
                    pass
            dedupe_task_mq_client.sleep(SLEEP_IN_SECONDS)

if __name__ == '__main__':
    deduperOn()
