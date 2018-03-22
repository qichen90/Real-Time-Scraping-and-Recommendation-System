import sys
import os
from newspaper import Article

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient

SCRAPE_TASK_QUEUE_URL = 'amqp://zyxttdzy:CgfaZUfBCryGa5xfxdmJEfXSpVQZ-CN8@llama.rmq.cloudamqp.com/zyxttdzy'
SCRAPE_TASK_QUEUE_NAME = 'SCRAPE_News'
DEDUPE_TASK_QUEUE_URL = 'amqp://gnzuwdxl:fyO1ipOpAmQDH4HNlrZ0UXFllDoSfelG@skunk.rmq.cloudamqp.com/gnzuwdxl'
DEDUPE_TASK_QUEUE_NAME = 'Dedupe_News'

SLEEP_IN_SECONDS = 10

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
