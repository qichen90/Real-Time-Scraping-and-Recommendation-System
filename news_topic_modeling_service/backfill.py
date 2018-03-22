import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client
import news_topic_modeling_service_client as predictModel

if __name__ == "__main__":
    db = mongodb_client.get_db()
    # cursor like iterator
    cursor = db['news'].find({})
    count = 0
    for news in cursor:
        count += 1
        if 'class' not in news:
            print('Populating classes...')
            topic = predictModel.classifyForNews(news['title'])
            if topic is not None:
                news['class'] = topic
                db['news'].replace_one({'digest': news['digest']}, news, upsert=True)
        

