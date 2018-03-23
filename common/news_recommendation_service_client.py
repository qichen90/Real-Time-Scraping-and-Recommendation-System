import jsonrpclib

URL = "http://localhost:6060"

client = jsonrpclib.ServerProxy(url=URL)

def classifyForNews(text): 
    topic = client.classifyForNews(text)
    print("Topic: %s" % topic)
    return topic