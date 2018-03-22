import pyjsonrpc

URL = "http://localhost:6060"

client = pyjsonrpc.HttpClient(url=URL)

def classifyForNews(text): 
    topic = client.classifyForNews(text)
    print("Topic: %s" % topic)
    return topic