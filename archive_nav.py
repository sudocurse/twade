#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, sys
import tweet as tweet_utils
from flask import Flask,redirect

app = Flask(__name__)

FILENAME = "PUT YOUR TWEETS.JS FULL FILE PATH HERE" # get rid of this

HEADER = '<html><head><meta charset="UTF-8"><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous"></head><body>'
FOOTER = '</body></html>'
TWEETS_LISTING_TEMPLATE = """<div class="container">{}</div>"""
TWEET_TEMPLATE = """<h4>{tweet.full_text}</h4>
<a href="https://twitter.com/sudocurse/status/{tweet.id}">☁ go</a> |  Tweeted from {tweet.source} at {tweet.created_at}
"""

def render_page(body):
    return HEADER + body + FOOTER


def render_tweet(tweet):
    return TWEET_TEMPLATE.format(tweet=tweet)

def render_tweets(tweets):
    output = ""
    for tweet in tweets:
      output = output + render_tweet(tweet)
    return TWEETS_LISTING_TEMPLATE.format(output)


@app.route('/')
def main_dashboard():
    app.logger.debug("Invoked root")
    return render_page("""<section class='container'>So like this is supposed to have a nice way to idk load up your
                        tweets / remember if you've loaded them before, right? Maybe just take you there or show you a
                        preview?</section>
                        <section class='container'>Welll so i'm definitely rusty on my frontend. And haven't really
                        gotten to that part yet. So for now:
                        <ul><li> you have to unzip the archive yourself and put the full file path up above on FILENAME
                            <li>you can go to <a href="/tweets">/tweets</a> to see the full list</li>
                            <li>you can go to /search/KEYWORD to search your tweet text for KEYWORD</li></ul>
                            <form action="/search/">Search: <input value="keywords"/><submit /></form></section>
                            """)

@app.route('/tweets')
def page_render_all():
    app.logger.debug("Invoked list")
    return render_page(render_tweets(sorted_archive))

@app.route('/search', methods=['POST'])
def handle_search():
    pass

@app.route('/search/<kw>')
def render_search(kw=None):
    app.logger.debug("Invoked search")
    if not kw:
        return "yikes you gotta have search terms"
    results = search(sorted_archive, kw)
    body = render_tweets(results)
    return render_page(body)

def search(tweets, kw):
    results = []
    for tweet in tweets:
        if kw.upper() in tweet.full_text.upper():
            results.append(tweet)
    return results


def setup():

    # filename = sys.argv[2]
    filename = FILENAME
    tweets = json.load(open(filename))    
    my_archive = tweet_utils.parse_tweets(tweets)
    return my_archive

sorted_archive = list(reversed(setup()))
app.logger.debug("uhhhh are there tweets? {}".format(sorted_archive))
# print(page_render_all(sorted_archive))
