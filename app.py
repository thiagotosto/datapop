# coding: utf-8


from flask import Flask, render_template, request, session, redirect, url_for, session
import ast
import datetime
from pymongo import MongoClient
import os
import requests as rq
import json
import ast



app = Flask(__name__)

app.secret_key = 'likujnyhtbgrvf67543'


@app.route('/login/' methods=['POST'])
def login():
    

@app.route('/get_tweets_sample')
def getTweetsSample():
    mg_client = MongoClient('localhost', 27017)
    tweets = mg_client.datapop.tweets_to_classify

    return json.dumps({str(obj['_id']): {i:obj[i] for i in obj if i != '_id'} for obj in tweets.aggregate([{'$sample': {'size': 3}}])})

@app.route('/classify_tweet/', methods=['POST'])
def classifyTweet():
    #recolhendo dados do formulario
    tweet_ids = request.form.to_dict()

    #instanciando banco
    mg_client = MongoClient('localhost', 27017)
    tweets = mg_client.datapop.tweets_to_classify
    tweets_classified = mg_client.datapop.tweets_classified

    #trocando tweet de lugar
    for tweet_id in tweet_ids.keys():
        tweet = tweets.find_one({'id_str': tweet_id})

        if tweets.delete_one({"_id": tweet['_id']}):
            #setando nota
            tweet['rate'] = tweet_ids[tweet_id]

            #setando sentimento
            tweet['sentiment'] = 'positive' if int(tweet['rate']) > 3 else 'negative' if int(tweet['rate']) < 3 else 'neutral'

            tweets_classified.insert_one(tweet)

    return redirect(url_for('index'))

@app.route('/')
def index():
    tweets_str = rq.get('http://localhost:5000/get_tweets_sample').text
    tweets =  json.loads(tweets_str)

    return render_template('index.html', tweets=tweets)

if __name__ == '__main__':
    app.run(debug=True)
