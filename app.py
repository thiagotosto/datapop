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



@app.route('/get_tweets_sample')
def getTweetsSample():
    mg_client = MongoClient('localhost', 27017)
    tweets = mg_client.datapop.tweets_to_classify

    return json.dumps({str(obj['_id']): {i:obj[i] for i in obj if i != '_id'} for obj in tweets.aggregate([{'$sample': {'size': 3}}])})

@app.route('/classify_tweet/<id>')
def classifyTweet(id):
    mg_client = MongoClient('localhost', 27017)
    tweet = mg_client.find({'_id': id})
    tweets = mg_client.datapop.tweets
    tweets_classified = mg_cliente.datapop.tweets_classified

    if tweets.delete_one({"_id": tweet['_id']}):
        tweets_classified.insert_one(tweet)

@app.route('/')
def index():
    tweets_str = rq.get('http://localhost:5000/get_tweets_sample').text
    tweets =  json.loads(tweets_str)
    
    return render_template('index.html', tweets=tweets)
    #return "Hello"

if __name__ == '__main__':
    app.run(debug=True)
