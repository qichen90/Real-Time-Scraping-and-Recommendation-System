import requests
from json import loads

NEWS_API_ENDPOINT = 'https://newsapi.org/v1/'
NEWS_API_ARTICLES = 'articles'
NEWS_API_APIKEY = 'cf9e2c4d79974aca9b9d668069dfeecb'
DEFAULT_SOURCES = [
    'cnn'
]
SORT_BY_TOP = 'top'

def _buildUrl(endPoint=NEWS_API_ENDPOINT, apiName=NEWS_API_ARTICLES):
    """ build URL for News API """
    return  endPoint + apiName 

def getNewsList(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    """ Get the list of news from News API """
    articles = []
    for source in sources:
        # get news through News API
        payload = {
            'source': source,
            'apiKey': NEWS_API_APIKEY,
            'sortBy': SORT_BY_TOP
        }
        response = requests.get(_buildUrl(), params=payload)
        res_json = loads(response.content.decode('utf-8'))

        if(res_json is not None and
            res_json['status'] == 'ok' and 
            res_json['source'] is not None):
            # add source to each news for future usage
            for news in res_json['articles']:
                news['source'] = res_json['source']
            
            articles.extend(res_json['articles'])
    return articles
        