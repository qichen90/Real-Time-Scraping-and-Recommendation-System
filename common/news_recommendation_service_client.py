import jsonrpclib

URL = 'http://localhost:5050'
client = jsonrpclib.ServerProxy(URL)

def getPreferenceForUser(userId):
    preference = client.call("getPreferenceForUser", userId)
    print("Preference list: %s" % str(preference))
    return preference
