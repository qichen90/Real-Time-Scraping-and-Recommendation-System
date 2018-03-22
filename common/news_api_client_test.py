import news_api_client

def test_basic():
    news = news_api_client.getNewsList()
    print(news)
    assert len(news) > 0

    news = news_api_client.getNewsList(sources=['cnn'], sortBy='top')
    assert len(news) > 0

    print('getNewsList works well')

if __name__ == '__main__':
    test_basic()