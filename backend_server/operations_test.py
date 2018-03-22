"""Test get_one_news function"""
import operations

def test_get_one_news_basic():
    """Test get_one_news function"""
    news = operations.get_one_news()
    assert news is not None
    print('operations basically work!') # pylint: disable=superfluous-parens

def test_get_news_summaries_for_user_basic():
    """Test get_news_summaries_for_user basic."""
    news = operations.get_news_summaries_for_user('test', 1)
    assert len(news) > 0
    print("get_news_summaries_for_user basic test passed!")

def test_get_news_summaries_for_user_pagination_basic():
    news1 = operations.get_news_summaries_for_user('test1', 1)
    news2 = operations.get_news_summaries_for_user('test1', 2)
    digest1 = set([news['digest'] for news in news1])
    digest2 = set([news['digest'] for news in news2])

    assert len(digest1.intersection(digest2)) == 0
    print("get_news_summaries_for_user pagination test passed!")

def test_log_news_click_for_user_basic():
    operations.log_news_click_for_user('test', '6rawLZRh3cZMJ51/Vi/7dA==\n')
    print("log_news_click_for_user pagination test passed!")

if __name__ == '__main__':
    test_get_one_news_basic()
    test_get_news_summaries_for_user_basic()
    test_get_news_summaries_for_user_pagination_basic()
    test_log_news_click_for_user_basic()
