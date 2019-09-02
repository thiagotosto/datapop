# coding: utf-8


from flask import Flask, render_template, request, session, redirect, url_for, session
import ast
import datetime
from pymongo import MongoClient
import os
import requests as rq
import json
import ast
import redis
from utils import Utils

app = Flask(__name__)

app.secret_key = 'likujnyhtbgrvf67543'


def checkToken():
    r = redis.Redis(host='localhost', port='6379', db=0)

    #print('Session Keys: {}'.format(session.keys()))

    if 'user' not in session.keys() or 'token' not in session.keys():
        #print('False 1')
        return False

    r_user = r.get(session['user'])

    if not r_user:
        return False
    if str(session['token']) != str(r_user.decode('utf-8')):
        #print('{} : {}'.format(session['token'], r.get(session['user']).decode('utf-8')))
        #print('False 2')
        return False

    return True

@app.route('/')
def index():
    #checando se usuario eta logado
    if not checkToken():
        return render_template('login.html')

    tweets_str = rq.get('http://localhost:5000/get_tweets_sample').text
    tweets =  json.loads(tweets_str)

    return render_template('index.html', tweets=tweets, session=session)


@app.route('/login/', methods=['POST'])
def login():
    #instanciando bancos
    r = redis.Redis(host='localhost', port='6379', db=0)
    mg_client = MongoClient('localhost', 27017)
    users = mg_client.datapop.users

    #recolhendo dados do formulario
    credentials = request.form.to_dict()

    #buscando usuario
    user = users.find_one({'user': credentials['user']})

    #checando se usuario existe e se senha corresponde
    if user:
        if user['password'] == credentials['password']:
            #gerando token
            token = Utils.generateKey(15)

            #guardando token do usuario
            r.set(credentials['user'], token, ex=7200)
            session['user'] = credentials['user']
            session['token'] = token
            session['name'] = user['name']

    return redirect(url_for('index'))

@app.route('/get_tweets_sample')
def getTweetsSample():
    mg_client = MongoClient('localhost', 27017)
    tweets = mg_client.datapop.tweets_to_classify

    return json.dumps({str(obj['_id']): {i:obj[i] for i in obj if i != '_id'} for obj in tweets.aggregate([{'$sample': {'size': 3}}])})

@app.route('/classify_tweet/', methods=['POST'])
def classifyTweet():
    #checando se usuario eta logado
    if not checkToken():
        return render_template('login.html')

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
            #setando dono da classificação
            tweet['classified_by'] = session['name']

            #setando nota
            tweet['rate'] = tweet_ids[tweet_id]

            #setando sentimento
            tweet['sentiment'] = 'positive' if int(tweet['rate']) > 3 else 'negative' if int(tweet['rate']) < 3 else 'neutral'

            tweets_classified.insert_one(tweet)

    return redirect(url_for('index'))

@app.route('/logout/')
def logout():
    session.clear()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
