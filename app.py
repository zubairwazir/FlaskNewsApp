from flask import Flask, render_template, request
from newsapi import NewsApiClient
import requests

app = Flask(__name__)


base_url = 'https://www.reddit.com/'

with open('psd.txt', 'r') as f:
    psd = f.read()

data = {'grant_type': 'password', 'username': "zubairwazir", 'password': psd}

app_id = "6RUip_QjhLeHUISet5PTxw"
secret_key = "VbpWr1EvfJFZWC74K5etl6D7L-mMcg"
auth = requests.auth.HTTPBasicAuth(app_id, secret_key)

app_name = 'FlaskNewsApp'

r = requests.post(base_url + 'api/v1/access_token',
                  data=data,
                  headers={'user-agent': app_name},
                  auth=auth
                  )
d = r.json()
token = 'bearer ' + d['access_token']
headers = {'Authorization': token, 'User-Agent': app_name}
api_url = 'https://oauth.reddit.com'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reddit_news')
def reddit_news():
    response = requests.get(api_url + '/r/headlines/new/', headers=headers)

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

    return render_template('index.html', context = news_list)

@app.route('/search_reddit', methods=['POST'])
def search_reddit():

    q = request.form['keyword']
    response = requests.get(api_url + '/r/' + q +'/new', headers=headers)

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

    return render_template('index.html', context = news_list)
