import json
from pymongo import MongoClient

with open('../config.json') as json_data_file:
    config = json.load(json_data_file)

MONGO_DB_HOST = config['mongoDB']['mainDB']['host']
MONGO_DB_PORT = config['mongoDB']['mainDB']['port']
DB_NAME = config['mongoDB']['mainDB']['DBname']

client = MongoClient("%s:%s" % (MONGO_DB_HOST, MONGO_DB_PORT))
def get_db(db=DB_NAME):
    db = client[db]
    return db
