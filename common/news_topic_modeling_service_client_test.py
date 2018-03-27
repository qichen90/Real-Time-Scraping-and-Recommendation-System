import news_topic_modeling_service_client as client

def test_basic():
    title = "Pentagon might propose ground troops for Syria"
    topic = client.classifyForNews(title)
    assert topic == 'US'
    print("test_basic passed")

if __name__ == "__main__":
    test_basic()