import jsonrpclib
import json

with open('../config.json') as json_data_file:
    config = json.load(json_data_file)

HOST_NAME = config['services']['modelingService']['host']
HOST_PORT = config['services']['modelingService']['port']
URL = 'http://' +   HOST_NAME + ":" + str(HOST_PORT)

client = jsonrpclib.ServerProxy(URL)

def classifyForNews(text): 
    topic = client.classifyForNews(text)
    print("Topic: %s" % topic)
    return topic