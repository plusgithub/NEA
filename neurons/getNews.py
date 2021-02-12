from newsapi import NewsApiClient

def getNews():
    newsapi = NewsApiClient(api_key='67625a054f3f44969d4f20b14a56afe7')
    news = newsapi.get_top_headlines(sources='bbc-news',
                                            language='en')
    return news