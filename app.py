from flask import Flask, render_template, request
from newsapi import NewsApiClient

app = Flask(__name__)

@app.route('/news')
def index():
    newsapi = NewsApiClient(api_key="660bf94fd55d4391bd7166337fb35ae6")
    topheadlines = newsapi.get_top_headlines(sources="al-jazeera-english")


    news = topheadlines['articles']

    headline = []
    link = []
    source = []
    img = []


    for i in range(len(news)):
       news_list = news[i]
       
       headline.append(news_list['title'])
       link.append(news_list['url'])
       source.append(news_list['source'])
       img.append(news_list['urlToImage'])


    news_list = zip(headline, link, source, img)


    return render_template('index.html', context = news_list)



@app.route('/news/bbc')
def bbc_news():
    newsapi = NewsApiClient(api_key="660bf94fd55d4391bd7166337fb35ae6")
    topheadlines = newsapi.get_top_headlines(sources="bbc-news")

    news = topheadlines['articles']

    headline = []
    link = []
    source = []
    img = []


    for i in range(len(news)):
       news_list = news[i]
       
       headline.append(news_list['title'])
       link.append(news_list['url'])
       source.append(news_list['source'])
       img.append(news_list['urlToImage'])



    news_list = zip(headline, link, source)

    return render_template('bbc.html', context = news_list)

@app.route('/')
def home():
    return render_template('search.html',news='')
    
@app.route('/bbc/search',methods=['POST']) 
def search_news():
    keyword = request.form['keyword']  #getting input from user

    newsapi = NewsApiClient(api_key="660bf94fd55d4391bd7166337fb35ae6")
    # topheadlines = newsapi.get_top_headlines(sources="bbc-news")

    news = newsapi.get_top_headlines(q=keyword,
                                     #sources='bbc-news,the-verge',#optional and you can change
                                     #category='business', #optional and you can change also
                                     language='en', #optional and you can change also
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
       source.append(news_list['source'])
       img.append(news_list['urlToImage'])


    news_list = zip(headline, link, source, img)


    return render_template('index.html', context = news_list)




    #print(news['articles'])
    # return render_template('search.html',news=news['articles'])
# @app.route('/r/news')
# def r_news():




if __name__ == "__main__":
    app.run(debug=True)