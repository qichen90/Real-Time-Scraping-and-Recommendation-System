import cnn_news_scraper

URL = "https://www.cnn.com/2018/03/11/us/new-york-city-helicopter-accident/index.html"
EXPECTED_CONTENT = "Two people were killed when a helicopter went down Sunday evening in New York's East River, authorities said"
def test_basic():
    news = cnn_news_scraper.extract_news(URL)
    print(news)
    assert EXPECTED_CONTENT in news

    print("CNN scraper works!")

if __name__ == '__main__':
    test_basic()