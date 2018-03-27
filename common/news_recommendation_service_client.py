import jsonrpclib
import json

with open('../config.json') as json_data_file:
    config = json.load(json_data_file)

HOST_NAME = config['services']['recommendationService']['host']
HOST_PORT = config['services']['recommendationService']['port']
URL = 'http://' + HOST_NAME + ":" + str(HOST_PORT)
client = jsonrpclib.ServerProxy(URL)

def getPreferenceForUser(userId):
    preference = client.getPreferenceForUser(userId)
    print("Preference list: %s" % str(preference))
    return preference
