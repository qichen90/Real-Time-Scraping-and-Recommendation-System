"""Backend Service """
from __future__ import print_function
import json
from bson.json_util import dumps
import operations
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer # pylint: disable=import-error

with open('../config.json') as json_data_file:
    config = json.load(json_data_file)

SERVER_HOST_NAME = config['services']['backendService']['host']
SERVER_PORT = config['services']['backendService']['port']

def add(num1, num2):
    """Test for the servcie: Add two number. """
    print("add is called with %d and %d" % (num1, num2))
    return num1 + num2

def get_one_news():
    """Get one news from MONGODB """
    return json.loads(dumps(operations.get_one_news()))

def get_news_summaries_for_user(user_id, page_num):
    print('get_news_summaries_for_user is called by user: %s for page: %s' % (user_id, page_num))
    return operations.get_news_summaries_for_user(user_id, page_num)

def log_news_click_for_user(user_id, news_id):
    print('log_news_click_for_user is called by user: %s clicking on %s' % (user_id, news_id))
    operations.log_news_click_for_user(user_id, news_id)

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST_NAME, SERVER_PORT))

RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(get_one_news, 'getOneNews')
RPC_SERVER.register_function(get_news_summaries_for_user, 'getNewsSummariesForUser')
RPC_SERVER.register_function(og_news_click_for_user, 'logNewsClickForUser')

print("Starting RPC server on %s:%d" % (SERVER_HOST_NAME, SERVER_PORT))
RPC_SERVER.serve_forever()
