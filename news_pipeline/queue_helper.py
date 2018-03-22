""" clear Message Queue helper """
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient

SCRAPE_TASK_QUEUE_URL = 'amqp://zyxttdzy:CgfaZUfBCryGa5xfxdmJEfXSpVQZ-CN8@llama.rmq.cloudamqp.com/zyxttdzy'
SCRAPE_TASK_QUEUE_NAME = 'SCRAPE_News'
DEDUPE_TASK_QUEUE_URL = 'amqp://gnzuwdxl:fyO1ipOpAmQDH4HNlrZ0UXFllDoSfelG@skunk.rmq.cloudamqp.com/gnzuwdxl'
DEDUPE_TASK_QUEUE_NAME = 'Dedupe_News'

def clearQueue(queue_url, queue_name):
    mq_client = CloudAMQPClient(queue_url, queue_name)
    num_of_message = 0
    while True:
        if mq_client is not None:
            msg = mq_client.getMessage()
            if msg is None:
                print("Messages cleared: %d" % num_of_message)
                return 
            num_of_message += 1

if __name__ == '__main__':
    clearQueue(SCRAPE_TASK_QUEUE_URL, SCRAPE_TASK_QUEUE_NAME)
    clearQueue(DEDUPE_TASK_QUEUE_URL, DEDUPE_TASK_QUEUE_NAME)
