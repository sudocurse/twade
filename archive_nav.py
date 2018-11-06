#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, sys
from flask import Flask

app = Flask(__name__)
"""
 The archive file you get from twitter is javascript EXPRESSIONS... not objects.
 aka you can't read them as json until you remove the thing at the beginning:

10066 $  head ./tweet.js         # this is the file that has all the tweets
window.YTD.tweet.part0 = [ {
  "retweeted" : false,
  "source" : "<a href=\"https://twitterrific.com/ios\" rel=\"nofollow\">Twitterrific for iOS</a>",
  "entities" : {
    "hashtags" : [ ],
    "symbols" : [ ],
    "user_mentions" : [ ],
    "urls" : [ ]
  },
  "display_text_range" : [ "0", "73" ],

----

So we have to get rid of the "window.YTD.tweet.part0 =".

I did all that out of band but i guess here it would be like


with open(fname) as tweet_js:
    raw = tweet_js.readlines()
    raw[0] = raw[0][25:]
    tweets = json.loads("\n".join(raw))

---

Anyways

>>> tweets[0].keys()
dict_keys(['retweeted', 'source', 'entities', 'display_text_range', 'favorite_count', 'id_str', 'truncated', 'retweet_count', 'id', 'created_at', 'favorited', 'full_text', 'lang'])

>>> for tweet in tweets:
...   for key in tweet.keys():
...     if key in key_count.keys():
...       key_count[key] = key_count[key] + 1
...     else:
...       key_count[key] = 1

{'retweeted': 3501, 'source': 3501, 'entities': 3501, 'display_text_range': 3501, 'favorite_count': 3501, 'id_str': 3501, 'truncated': 3501, 'retweet_count': 3501, 'id': 3501, 'created_at': 3501, 'favorited': 3501, 'full_text': 3501, 'lang': 3501, 'possibly_sensitive': 960, 'extended_entities': 536, 'in_reply_to_status_id_str': 653, 'in_reply_to_user_id': 752, 'in_reply_to_status_id': 653, 'in_reply_to_screen_name': 711, 'in_reply_to_user_id_str': 752, 'coordinates': 4, 'geo': 4}


It seems as though nearly everything has all of the attributes up until lang.
possible_sensitive -- geo are all variable.

"""

HEADER = '<html><head><meta charset="UTF-8"></head><body>'
FOOTER = '</body></html>'
TEMPLATE = """<h4>{tweet.full_text}</h4>
<a href="https://twitter.com/sudocurse/status/{tweet.id}">☁ go</a> |  Tweeted from {tweet.source} at {tweet.created_at}
"""

class Tweet(object):

    def __init__(self, source, entities, display_text_range, favorite_count, id_str, retweet_count, id, created_at, full_text, lang, possibly_sensitive=None, extended_entities=None, in_reply_to_status_id_str=None, in_reply_to_user_id=None, in_reply_to_status_id=None, in_reply_to_screen_name=None, in_reply_to_user_id_str=None, coordinates=None, geo=None):
        # i had to do so much of this kind of shit ', '.join(list(map(lambda x: return "{0} = tweet['{0}']".format(x), tweets[0].keys() ) ))

        self.source = source
        self.entities = entities
        self.display_text_range = display_text_range
        self.favorite_count = favorite_count
        self.id_str = id_str
        self.retweet_count = retweet_count
        self.id = id
        self.created_at = created_at
        self.full_text = full_text
        self.lang = lang
        self.possibly_sensitive = possibly_sensitive
        self.extended_entities = extended_entities
        self.in_reply_to_status_id_str = in_reply_to_status_id_str
        self.in_reply_to_user_id = in_reply_to_user_id
        self.in_reply_to_status_id = in_reply_to_status_id
        self.in_reply_to_screen_name = in_reply_to_screen_name
        self.in_reply_to_user_id_str = in_reply_to_user_id_str
        self.coordinates = coordinates
        self.geo = geo

    
def parse_tweets(tweets):
    """
    >>> all
    ['retweeted', 'source', 'entities', 'display_text_range', 'favorite_count', 'id_str', 'truncated', 'retweet_count', 'id', 'created_at', 'favorited', 'full_text', 'lang', 'possibly_sensitive', 'extended_entities', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_status_id', 'in_reply_to_screen_name', 'in_reply_to_user_id_str', 'coordinates', 'geo']

    >>> for k in all:
    ...   if k in tweet.keys() and not tweet[k]: # aka if this is false
    ...     tmp.append(k)
    ...   if k in tweet.keys() and tweet[k] and k in tmp:
    ...     del(tmp[tmp.index(k)])


    so there's a tweet limit that varies (display_text_range)
    ['retweeted', 'truncated', 'favorited'] are always false
    """
    parsed = []
    for tweet in tweets:

        # initialize with known ones
        tw = Tweet(source = tweet['source'], entities = tweet['entities'], display_text_range = tweet['display_text_range'], favorite_count = tweet['favorite_count'], id_str = tweet['id_str'], retweet_count = tweet['retweet_count'], id = tweet['id'], created_at = tweet['created_at'], full_text = tweet['full_text'], lang = tweet['lang'])

        # check for others possibly_sensitive, extended_entities, in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_status_id, in_reply_to_screen_name, in_reply_to_user_id_str, coordinates, geo'

        other_keys = ['possibly_sensitive', 'extended_entities', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_status_id', 'in_reply_to_screen_name', 'in_reply_to_user_id_str', 'coordinates', 'geo']

        cur_keys = tweet.keys() # i need to drive my cur where are my cur keys

        for key in other_keys:
            if key in cur_keys:
                setattr(tw, key, tweet[key])

        parsed.append(tw)
    return parsed

def render_tweet(tweet):
    return TEMPLATE.format(tweet=tweet)

def render_tweets(tweets):
    output = ""
    for tweet in tweets:
      output = output + render_tweet(tweet)
    return output

@app.route('/')
def page_render_all():
    return HEADER + render_tweets(sorted_archive) + FOOTER # lmao wtf is this, php?

@app.route('/search/<kw>')
def render_search(kw=None):
    if not kw:
        return "yikes you gotta have search terms"
    results = search(sorted_archive, kw)
    body = render_tweets(results)
    return HEADER + body + FOOTER

def search(tweets, kw):
    results = []
    for tweet in tweets:
        if kw.upper() in tweet.full_text.upper():
            results.append(tweet)
    return results

# filename = sys.argv[2]
def setup():
    tweets = json.load(open(filename))    
    my_archive = parse_tweets(tweets)
    return my_archive

sorted_archive = list(reversed(setup()))
# print(page_render_all(sorted_archive))
