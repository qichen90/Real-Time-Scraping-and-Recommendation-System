import os
import requests
import random
from lxml import html

USER_AGENT_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENT_LIST = []

with open(USER_AGENT_FILE, 'rb') as ua_file:
    for ua in ua_file.readlines():
        if ua:
            USER_AGENT_LIST.append(ua.strip()[1:-1])
random.shuffle(USER_AGENT_LIST)

CNN_XPATH_NEWS_CONTENT = """//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 'zn-body__paragraph')]//text()"""

def _generate_headers():
    ua = random.choice(USER_AGENT_LIST)
    headers = {
        "Connection": "close",
        "User-Agent": ua
    }
    return headers

def extract_news(news_url):
    # mock human actions browsing websites
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=_generate_headers())
    news = {}
    try:
        tree = html.fromstring(response.content)
        news = tree.xpath(CNN_XPATH_NEWS_CONTENT)
        news = ''.join(news)
    except Exception:
        return {}
    
    return news

