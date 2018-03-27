
# -*- coding: utf-8 -*-
'''
Time decay model:
If selected:
p = (1-α)p + α
If not:
p = (1-α)p
Where p is the selection probability, and α is the degree of weight decrease.
The result of this is that the nth most recent selection will have a weight of
(1-α)^n. Using a coefficient value of 0.05 as an example, the 10th most recent
selection would only have half the weight of the most recent. Increasing epsilon
would bias towards more recent results more.
'''

import os
import sys
import news_classes

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client
from cloudAMQP_client import CloudAMQPClient

with open('../config.json') as json_data_file:
    config = json.load(json_data_file)

CLICK_LOGGER_QUEUE_URL = config['cloudAMQP']['clickLoggerQueue']['url']
CLICK_LOGGER_QUEUE_NAME = config['cloudAMQP']['clickLoggerQueue']['name']
click_logger_client = CloudAMQPClient(CLICK_LOGGER_QUEUE_URL, CLICK_LOGGER_QUEUE_NAME)
SLEEP_TIME_IN_SECONDS = config['cloudAMQP']['clickLoggerQueue']['sleep']

TABLE_NAME_FOR_NEWS = config['mongoDB']['mainDB']['newsTable']
TABLE_NAME_FOR_PREFERENCE_MODEL = config['mongoDB']['mainDB']['preferenceModelTable']

N_CLASSES = 8
INITIAL_P = 1.0 / N_CLASSES
ALPHA = 0.1 

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        return 
    
    if('userId' not in msg
        or 'newsId' not in msg
        or 'timestamp' not in msg):
        return 
    
    user_id = msg['userId']
    news_id = msg['newsId']

    db = mongodb_client.get_db()
    model = db[TABLE_NAME_FOR_PREFERENCE_MODEL].find_one({'userId': user_id})

    # if model not exists, create one
    if model is None:
        print("Create new model for user: %s" % user_id)
        news_model = {'userId': user_id}
        preference = {}
        for i in news_classes.classes:
            preference[i] = float(INITIAL_P)
        news_model['preference'] = preference
        model = news_model
    
    print("Recalculating preference model for user %s" % user_id)
    # recalculate model
    news = db[TABLE_NAME_FOR_NEWS].find_one({'digest': news_id})
    if(news is None
        or 'class' not in news
        or news['class'] not in news_classes.classes):
        print("Skipping update preferecne model...")
        return 

    click_class = news['class']
    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)
    for i, p in model['preference'].items():
        if not i == click_class:
            # old_p = model['preference'][i]
            model['preference'][i] = float((1 - ALPHA) * p)
    
    # update the model in DB
    print("Updating preference model for user %s in DB" % user_id)
    db[TABLE_NAME_FOR_PREFERENCE_MODEL].replace_one({'userId': user_id}, model, upsert=True)


def processorRun():
    while True:
        if click_logger_client is not None:
            msg = click_logger_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as ex:
                    print(ex)
                    pass
        
        click_logger_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == "__main__":
    processorRun()
