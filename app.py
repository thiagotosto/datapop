# coding: utf-8


from flask import Flask, render_template, request, session, redirect, url_for, session
import ast
import datetime
from pymongo import MongoClient
import os
import requests as rq



app = Flask(__name__)

app.secret_key = 'likujnyhtbgrvf67543'



@app.route('/get_tweets_sample')
def getTweetsSample():
    mg_client = MongoClient('localhost', 27017)
    tweets = mg_cliente.datapop.tweets

    return {obj['_id']: obj for obj in tweets.aggregate([{'$sample': {'size': 10}}])}

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
    #tweets = rq.get('localhost:5000/get_tweets_sample').json()

    #return tweets
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)
