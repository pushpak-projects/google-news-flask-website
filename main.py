import json
import operator
from flask import Flask, jsonify, abort, request
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
import string
import traceback
import sys
app = Flask(__name__)
API_KEY = '4b2ffccd663f4297bca8e9f634ed37e8'
#API_KEY = '1ce83886d60e4afb977787bfacfb225d'
#API_KEY = '65e5909de0514729a489b5123f8c2675'
newsapi = NewsApiClient(api_key=API_KEY)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def homepage():
    return app.send_static_file("p2u1s1h1a1k1hw6.html")

@app.route('/v1.0/top-headlines/cnn', methods=['GET'])
def get_topheadlines_cnn():
    try:
        top_headlines = newsapi.get_top_headlines(sources='cnn')
    except NewsAPIException as err:
        print(err.get_message())
        dic = {}
        dic['message'] = str(err.get_message())
        print("in exceptionnnn")
        return jsonify(dic)
    headlines = list(top_headlines['articles'])
    print(len(headlines))
    
    null_values = ["null", "None", ""]
    articles = []

    for data in headlines:
        if str(data['source']['id']) in null_values or str(data['source']['name']) in null_values:
            continue
        if str(data['author']) in null_values or str(data['url']) in null_values or str(data['description']) in null_values or str(data['title']) in null_values or str(data['urlToImage']) in null_values or str(data['publishedAt']) in null_values:
            continue
        articles.append(data)
        if len(articles) == 4:
            break

    print(len(articles))
    return jsonify(articles)


@app.route('/v1.0/top-headlines/fox', methods=['GET'])
def get_topheadlines_fox():
    try:
        top_headlines = newsapi.get_top_headlines(sources='fox-news')
    except NewsAPIException as err:
        print(err.get_message())
        dic = {}
        dic['message'] = str(err.get_message())
        print("in exceptionnnn")
        return jsonify(dic)

    headlines = list(top_headlines['articles'])
    print(len(headlines))

    null_values = ["null", "None", ""]
    articles = []

    for data in headlines:
        if str(data['source']['id']) in null_values or str(data['source']['name']) in null_values:
            continue
        if str(data['author']) in null_values or str(data['url']) in null_values or str(data['description']) in null_values or str(data['title']) in null_values or str(data['urlToImage']) in null_values or str(data['publishedAt']) in null_values:
            continue
        articles.append(data)
        if len(articles) == 4:
            break

    print(len(articles))
    return jsonify(articles)


@app.route('/v1.0/top-headlines/slide', methods=['GET'])
def get_topheadlines_slide():
    try:
        top_headlines = newsapi.get_top_headlines(language="en")
    except NewsAPIException as err:
        print(err.get_message())
        dic = {}
        dic['message'] = str(err.get_message())
        print("in exceptionnnn")
        return jsonify(dic)

    headlines = list(top_headlines['articles'])

    null_values = ["null", "None", ""]
    articles = []

    for data in headlines:
        if str(data['source']['id']) in null_values or str(data['source']['name']) in null_values:
            continue
        if str(data['author']) in null_values or str(data['url']) in null_values or str(data['description']) in null_values or str(data['title']) in null_values or str(data['urlToImage']) in null_values or str(data['publishedAt']) in null_values:
            continue
        articles.append(data)
        if len(articles) == 5:
            break

    print(len(articles))
    return jsonify(articles)


@app.route('/v1.0/top-headlines/wordcount', methods=['GET'])
def get_topheadlines_wordcount():
    try:
        top_headlines = newsapi.get_top_headlines(language="en")
    except NewsAPIException as err:
        print(err.get_message())
        dic = {}
        dic['message'] = str(err.get_message())
        print("in exceptionnnn")
        return jsonify(dic)

    headlines = list(top_headlines['articles'])
    null_values = ["null", "None", ""]
    articles = []
    wordCountDict = dict()
    for data in headlines:
        if str(data['source']['id']) in null_values or str(data['source']['name']) in null_values:
            continue
        if str(data['author']) in null_values or str(data['url']) in null_values or str(data['description']) in null_values or str(data['title']) in null_values or str(data['urlToImage']) in null_values or str(data['publishedAt']) in null_values:
            continue
        sent = str(data['title'])
        words = sent.split()
        for word in words:
            if word in wordCountDict:
                wordCountDict[word] += 1
            else:
                wordCountDict[word] = 1

    sortedDict = dict(sorted(wordCountDict.items(),
                             key=operator.itemgetter(1), reverse=True))
    
    stopWordList = [stopword.rstrip('\n')
                    for stopword in open("stopwords_en.txt")]
    finalList = []
    for key in sortedDict:
        if key.casefold() in stopWordList:
            continue
        if key in string.punctuation:
            continue
        if len(finalList) == 30:
            break
        wordCloudDict = {}
        print(key, " ", sortedDict[key])
        wordCloudDict['word'] = key.translate(
            {ord(specialChar): '' for specialChar in "\"\'!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        wordCloudDict['size'] = str(sortedDict[key])
        finalList.append(wordCloudDict)
    print(finalList)
    return jsonify(finalList)


@app.route('/v1.0/sources', methods=['GET'])
def get_news_sources():
    category = request.args.get('category')
    print(category)
    news_sources = []
    if category == 'all':
        try:
            news_sources = newsapi.get_sources(language="en")
        except NewsAPIException as err:
            print(err.get_message())
            dic = {}
            dic['message'] = str(err.get_message())
            print("in exceptionnnn")
            return jsonify(dic)
    else:
        try:
            news_sources = news_sources = newsapi.get_sources(
                category=category, language="en")
        except NewsAPIException as err:
            print(err.get_message())
            dic = {}
            dic['message'] = str(err.get_message())
            print("in exceptionnnn")
            return jsonify(dic)

    null_values = ["null", "None", ""]
    srcList = list(news_sources['sources'])

    finalList = []
    for src in srcList:
        srcDict = dict()
        print(str(src['id']))
        if str(src['id']) in null_values or str(src['name']) in null_values:
            continue
        srcDict['id'] = src['id']
        srcDict['name'] = src['name']
        finalList.append(srcDict)
    return jsonify(finalList)


@app.route('/v1.0/cards', methods=['GET'])
def get_every_news():
    keyword = request.args.get('q')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    lang = request.args.get('lang')
    news_sources = []
    category = request.args.get('category')
    # take the list of sources from category
    if category == 'all':
        print('hello')
        try:
            news_sources = newsapi.get_sources(language="en")
        except NewsAPIException as err:
            print(err.get_message())
            dic = {}
            dic['message'] = str(err.get_message())
            return jsonify(dic)
    else:
        print('hi')
        try:
            news_sources = newsapi.get_sources(
                category=category, language="en")
        except NewsAPIException as err:
            print(err.get_message())
            dic = {}
            dic['message'] = str(err.get_message())
            return jsonify(dic)

    null_values = ["null", "None", ""]
    srcList = list(news_sources['sources'])
    print(srcList)
    sources = ""
    for src in srcList:
        if str(src['id']) in null_values or str(src['name']) in null_values:
            continue
        sources += src['id']+","
    sources = sources[:-1]
    print(sources)
    exceptionDict = dict()
    try:
        news_sources = newsapi.get_everything(
            q=keyword, sources=sources, from_param=from_date, to=to_date, language='en', sort_by='publishedAt', page_size=30)
    except NewsAPIException as err:
        print(err.get_message())
        print(type(err.get_message()))
        dic = {}
        dic['message'] = str(err.get_message())
        print("in exceptionnnn")
        return jsonify(dic)
    articles = []
    print(news_sources['articles'])
    for data in news_sources['articles']:
        if str(data['source']['id']) in null_values or str(data['source']['name']) in null_values:
            continue
        if str(data['author']) in null_values or str(data['url']) in null_values or str(data['description']) in null_values or str(data['title']) in null_values or str(data['urlToImage']) in null_values or str(data['publishedAt']) in null_values:
            continue
        articles.append(data)
        if len(articles) == 15:
            break

    print(len(articles))
    return jsonify(articles)
