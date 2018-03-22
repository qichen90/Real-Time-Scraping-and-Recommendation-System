import news_cnn_model
import numpy as np 
import os
import pandas as pd 
import tensorflow as tf 
import pickle 
import shutil
from sklearn import metrics

learn = tf.contrib.learn 

REMOVE_PREVIOUS_MODEL = True

MODEL_OUTPUT_DIR = '../model'
DATA_SET_FILE = '../data/labeled_news.csv'
VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_processor_save_file'
MAX_DOCUMENT_LENGTH = 100
N_CLASSES = 8

# training steps
STEPS = 200

def main(unused_argv):
    if REMOVE_PREVIOUS_MODEL:
        print("Removing previous model...")
        shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)
    
    df = pd.read_csv(DATA_SET_FILE, header=None)
    train_df = df[0: 400]
    test_df = df.drop(train_df.index)

    # x - title
    x_train = train_df[1] 
    x_test = test_df[1]
    # y - classes
    y_train = train_df[0]
    y_test = test_df[0]

    vocab = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    # print(x_train)
    x_train = np.array(list(vocab.fit_transform(x_train)))
    x_test = np.array(list(vocab.transform(x_test)))

    n_words = len(vocab.vocabulary_)
    print("Total words: %d" % n_words)
    # save the vocabulary
    with open(VARS_FILE, 'wb') as f:
        pickle.dump(n_words, f)
    vocab.save(VOCAB_PROCESSOR_SAVE_FILE)

    # Build model
    model = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR)

    # train model
    model.fit(x_train, y_train, steps=STEPS)

    # evaluate model
    y_predict = [
        p['class'] for p in model.predict(x_test, as_iterable=True)
    ]
    model_score = metrics.accuracy_score(y_test, y_predict)
    print("Accuracy of the model: {0:f}".format(model_score))

if __name__ == '__main__':
    tf.app.run(main=main)
