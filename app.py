from flask import Flask, render_template, request
from newsapi import NewsApiClient
import requests

app = Flask(__name__)

BASE_URL = 'https://www.reddit.com/'
OAUTH_URL = 'https://oauth.reddit.com'

with open('psd.txt', 'r') as f:
    psd = f.read()


def get_token():
    data = {'grant_type': 'password', 'username': "zubairwazir", 'password': psd}

    app_id = "6RUip_QjhLeHUISet5PTxw"
    secret_key = "VbpWr1EvfJFZWC74K5etl6D7L-mMcg"
    auth = requests.auth.HTTPBasicAuth(app_id, secret_key)

    app_name = 'FlaskNewsApp'

    r = requests.post(BASE_URL + 'api/v1/access_token',
                      data=data,
                      headers={'user-agent': app_name},
                      auth=auth
                      )
    d = r.json()
    if "access_token" not in d:
        return {}
    token = 'bearer ' + d['access_token']
    return {'Authorization': token, 'User-Agent': app_name}


HEADERS = get_token()


@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return internal_server_error(e)


@app.route('/reddit_news')
def reddit_news():
    if HEADERS:
        response = requests.get(OAUTH_URL + '/r/headlines/new/', headers=HEADERS)

        headline = []
        link = []
        source = []
        img = []

        for i in response.json()['data']['children']:
            headline.append(i['data']['title']),
            link.append(i['data']['url']),
            source.append(i['data']['domain'])
            img.append(i['data']['url'])

        news_list = zip(headline, link, source, img)

        return render_template('index.html', context=news_list)

    return unauthorized_error(Exception)


@app.route('/search_reddit', methods=['POST'])
def search_reddit():
    if HEADERS:
        q = request.form['keyword']
        response = requests.get(OAUTH_URL + '/r/' + q + '/new', headers=HEADERS)

        headline = []
        link = []
        source = []
        img = []

        for i in response.json()['data']['children']:
            headline.append(i['data']['title']),
            link.append(i['data']['url']),
            source.append(i['data']['domain']),
            img.append(i['data']['url'])

        news_list = zip(headline, link, source, img)

        return render_template('index.html', context=news_list)

    return unauthorized_error(Exception)


@app.route('/newsapi_news')
def newsapi_news():
    try:
        newsapi = NewsApiClient(api_key="2c9ae45aceea424cb9e11eab17ee00a7")
    except Exception as e:
        return unauthorized_error(e)

    try:
        topheadlines = newsapi.get_top_headlines(
            # q=keyword   #optional you can search by any keyword
            # sources='bbc-news,the-verge',#optional and you can change
            # category='business', #optional and you can change also
            language='en',  # optional and you can change also
            country='in')

        news = topheadlines['articles']

        headline = []
        link = []
        source = []
        img = []

        for i in range(len(news)):
            news_list = news[i]

        headline.append(news_list['title'])
        link.append(news_list['url'])
        source.append(news_list['source']['name'])
        img.append(news_list['urlToImage'])

        news_list = zip(headline, link, source, img)
        return render_template('index.html', context=news_list)
    except Exception as e:
        misunderstood_error(e)


@app.route('/search_newsapi', methods=['POST'])
def search_newsapi():
    keyword = request.form['keyword']  # getting input from user

    try:
        newsapi = NewsApiClient(api_key="2c9ae45aceea424cb9e11eab17ee00a7")
    except Exception as e:
        return unauthorized_error(e)

    try:
        news = newsapi.get_top_headlines(q=keyword,
                                         # sources='bbc-news,the-verge',#optional and you can change
                                         # category='business', #optional and you can change also
                                         language='en',  # optional and you can change also
                                         country='in')
        news = news['articles']

        headline = []
        link = []
        source = []
        img = []

        for i in range(len(news)):
            news_list = news[i]

        headline.append(news_list['title'])
        link.append(news_list['url'])
        source.append(news_list['source']['name'])
        img.append(news_list['urlToImage'])

        news_list = zip(headline, link, source, img)
        return render_template('index.html', context=news_list)
    except Exception as e:
        return misunderstood_error(e)


@app.errorhandler(404)
def page_not_found_error(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(400)
def misunderstood_error(e):
    return render_template('400.html'), 400


@app.errorhandler(401)
def unauthorized_error(e):
    return render_template('401.html'), 401


if __name__ == '__main__':
    app.run(debug=True)
