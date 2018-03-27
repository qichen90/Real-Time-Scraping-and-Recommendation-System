import sys
import os
from newspaper import Article

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient

with open('../config.json') as json_data_file:
    config = json.load(json_data_file)

SCRAPE_TASK_QUEUE_URL = config['cloudAMQP']['scraperTaskQueue']['url']
SCRAPE_TASK_QUEUE_NAME = config['cloudAMQP']['scraperTaskQueue']['name']
DEDUPE_TASK_QUEUE_URL = config['cloudAMQP']['deduperTaskQueue']['url']
DEDUPE_TASK_QUEUE_NAME = config['cloudAMQP']['deduperTaskQueue']['name']

SLEEP_IN_SECONDS = config['cloudAMQP']['scraperTaskQueue']['sleep']

scrape_task_mq_client = CloudAMQPClient(SCRAPE_TASK_QUEUE_URL, SCRAPE_TASK_QUEUE_NAME)
dedupe_task_mq_client = CloudAMQPClient(DEDUPE_TASK_QUEUE_URL, DEDUPE_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print('message is invalid')
        return 

    task = msg

    article = Article(task['url'])
    article.download()
    article.parse()
    task['text'] = article.text
    dedupe_task_mq_client.sendMessage(task)

while True:
    if scrape_task_mq_client is not None:
        msg = scrape_task_mq_client.getMessage()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as ex:
                print(ex)
                pass
        scrape_task_mq_client.sleep(SLEEP_IN_SECONDS)
