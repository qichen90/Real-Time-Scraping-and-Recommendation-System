import requests
import json
from json import loads

with open('../config.json') as json_data_file:
    config = json.load(json_data_file)

NEWS_API_ENDPOINT = config['newsAPI']['endpoint']
NEWS_API_ARTICLES = 'articles'
NEWS_API_APIKEY = config['newsAPI']['apikey']
DEFAULT_SOURCES = config['newsAPI']['defaultSource']
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
        