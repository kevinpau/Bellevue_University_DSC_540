#%%[markdown]
# # Week 9: Exercise 9.2
# File: DSC540_Paulovici_Exercise_9_2.py (.ipynb)<br> 
# Name: Kevin Paulovici<br>
# Date: 2/9/2020<br>
# Course: DSC 540 Data Preparation (2203-1)<br>
# Assignment: Exercise 9.2

#%%[markdown]
# In this exercise, you will create a twitter account (if you don’t already have one, or don’t wish to use your personal account) and practice pulling data from Twitter’s publicly available API. You can delete the twitter account as soon as you have completed the exercise. Include your code and output for each step.

#%%[markdown]
# ## Part 1
# Create a Twitter API Key and Access Token (Data Wrangling with Python, pg. 365-366)

#%%
""" Retrieve Authentication keys from separate file 

To protect authentication keys, using a seprate file (keys.py) to 
store them, then calling the GET_KEYS function to use them
"""
# import keys

# API_KEY, API_SECRET, TOKEN_KEY, TOKEN_SECRET = keys.GET_KEYS()

# print("API_KEY len - {}\nAPI_SECRET len - {}\nTOKEN_KEY length - {}\nTOKEN_SECRET length - {}".format(
#     len(API_KEY), len(API_SECRET), len(TOKEN_KEY), len(TOKEN_SECRET)))

""" The above function should work but for some reason my import does not update
in the envirnment I'm working this. So, as alternative, just reading a file and setting the keys
format: API_KEY API_SECRET TOKEN_KEY TOKEN SECRET
"""
keys = []
with open('keys.txt') as fileIn:
    for line in fileIn:
        line = line.strip()
        line = line.split()

        for item in line:
            keys.append(item)

API_KEY = keys[0]
API_SECRET = keys[1]
TOKEN_KEY = keys[2]
TOKEN_SECRET = keys[3]

#%%
# input keys directly if no external file is used

# API_KEY = ""
# API_SECRET = ""
# TOKEN_KEY = ""
# TOKEN_SECRET = ""

#%%[markdown]
# ## Part 2
# Do a single data pull from Twitter’s REST API (Data Wrangling with Python, pg. 366 – 368).

#%%
import oauth2
import json

# creat the OAuth connection
def oauth_req(url, key, secret, http_method="GET", post_body=b"",
                http_headers=None):
    
    consumer = oauth2.Consumer(key=API_KEY, secret=API_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client= oauth2.Client(consumer, token)
    resp, content = client.request(url, method=http_method,
                    body=post_body, headers=http_headers)
    
    return content

url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23childlabor'
data = oauth_req(url, TOKEN_KEY, TOKEN_SECRET)

# save data to parse later
data = json.loads(data)
print(type(data))

with open('tweet_data.json', 'w') as data_file:
    json.dump(data, data_file)

#%%[markdown]
# ## Part 3
# Execute multiple queries at a time from Twitter’s REST API (Data Wrangling with Python, pg. 368 – 371).

#%%
import tweepy
import json
import dataset

def store_tweet(item):
    db = dataset.connect('sqlite:///data_wranfling.db')
    # table = db['tweets']
    table = db.create_table('tweets', primary_id=False)
    item_json = item._json.copy()

    for k, v in item_json.items():
        if isinstance(v, dict):
            item_json[k] = str(v)
    
    table.insert(item_json)

# set the OAuth and access token
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)

api = tweepy.API(auth)

query = '#childlabor'
cursor = tweepy.Cursor(api.search, q=query, lanf="en")

# iterate through pages and save the data
for page in cursor.pages():
    for item in page:
        store_tweet(item)


#%%
import os

files = os.listdir()

if 'data_wranfling.db' in files:
    print(True) 

#%%[markdown]
# ## Part 4
# Do a data pull from Twitter’s Streaming API (Data Wrangling with Python, pg. 372 – 374).

# %%
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

class Listener(StreamListener):
    def on_data(Self,data):
        print(data)
        return True

auth = OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)

stream = Stream(auth, Listener())
stream.filter(track=['child labor'])

# %%
