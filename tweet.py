import json

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

    def __repr__(self):
        if self.full_text:
            return "<Tweet:id={}:{}>".format(self.id, str(self.full_text))
        else:
            return str(object.__repr__(self))

    def __str__(self):
        if self.full_text:
            return str(self.full_text)
        else:
            return object.__str__(self)

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

FIELDS

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

-----
false fields?? 
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


def parse_tweet(tweet):
    """
    Parses fields from a Tweet JSON object and returns a Tweet object 
    TODO: handle lists
	"""

    # so first initialize with known ones
    tw = Tweet(source = tweet['source'], entities = tweet['entities'], display_text_range = tweet['display_text_range'], 
    		   favorite_count = tweet['favorite_count'], id_str = tweet['id_str'], retweet_count = tweet['retweet_count'],
    		   id = tweet['id'], created_at = tweet['created_at'], full_text = tweet['full_text'], lang = tweet['lang'])

    """ check for others.
    """
    other_keys = ['possibly_sensitive', 'extended_entities', 'in_reply_to_status_id_str', 
    			  'in_reply_to_user_id', 'in_reply_to_status_id', 'in_reply_to_screen_name', 
    			  'in_reply_to_user_id_str', 'coordinates', 'geo']

    cur_keys = tweet.keys() # i need to drive my cur where are my cur keys
    for key in other_keys:
        if key in cur_keys:
            setattr(tw, key, tweet[key])
    return tw

def parse_tweets(tweets):
    """takes a Tweet json list and returns a list of Tweet object"""
     
    parsed = []
    for tweet in tweets:
        tw = parse_tweet(tweet)
        parsed.append(tw)
    return parsed

def rank_popularity(tweets):
    return sorted(tweets, key=lambda tweet: int(tweet.favorite_count)+int(tweet.retweet_count), reverse=True)
