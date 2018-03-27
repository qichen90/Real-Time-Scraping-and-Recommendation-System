import news_classes
import os
import sys
import numpy as np 
import pandas as pd 
import pickle 
import time
import json
import tensorflow as tf
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from tensorflow.contrib.learn.python.learn.estimators import model_fn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trainer'))
import news_cnn_model

learn = tf.contrib.learn

with open('../config.json') as json_data_file:
    config = json.load(json_data_file)

SERVER_HOST_NAME = config['services']['modelingService']['host']
SERVER_PORT = config['services']['modelingService']['port']

MODEL_DIR = '../model'
MDOEL_UPDATE_LAG_IN_SECONDS = 10

N_CLASSES = 8

VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_processor_save_file'

n_words = 0
MAX_DOCUMENT_LENGTH = 500
vocab_processor = None
classifier = None

def restoreVocab():
    """ Restore vocabulary processor. """
    with open(VARS_FILE, 'rb') as f:
        global n_words
        n_words = pickle.load(f)
    
    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(VOCAB_PROCESSOR_SAVE_FILE)

def loadModel():
    global classifier
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_DIR)

    df = pd.read_csv('../data/labeled_news.csv', header=None)
    # We have to call evaluate or predict at least once to make the restored Estimator work.
    train_df = df[0:400]
    x_train = train_df[1]
    x_train = np.array(list(vocab_processor.transform(x_train)))
    y_train = train_df[0]
    classifier.evaluate(x_train, y_train)

    print("Model updated!")

restoreVocab()
loadModel()

class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print("Model update detected. Loading new model.")
        time.sleep(MDOEL_UPDATE_LAG_IN_SECONDS)
        restoreVocab()
        loadModel()

# setup watchdog for model update
observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()

def classify_for_news(text):
    text_series = pd.Series([text])
    predict_based_x = np.array(list(vocab_processor.transform(text_series)))
    print(predict_based_x)

    y_predictd = [
        p['class'] for p in classifier.predict(predict_based_x, as_iterable=True)
    ]
    print(y_predictd[0])
    topic = news_classes.class_map[str(y_predictd[0])]
    return topic

RPCSEVER = SimpleJSONRPCServer((SERVER_HOST_NAME, SERVER_PORT))
RPCSEVER.register_function(classify_for_news, 'classifyForNews')

print("Starting RPC server on %s:%d" % (SERVER_HOST_NAME, SERVER_PORT))
RPCSEVER.serve_forever()