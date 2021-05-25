#!/usr/bin/env python3
# https://api.twitter.com/1.1/statuses/user_timeline.json\?screen_name\=irth7\&count\=1 -H Authorization:\ Bearer\ $BEARER_TOKEN 

import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json

BEARER_TOKEN=os.getenv("BEARER_TOKEN")
import time

_cache={}
def cache(seconds=60):
    def decorator(f):
        _cache[f]={}
        _cache[f]['v'] = None
        _cache[f]['t'] = None
        def wrapped(*args, **kwargs):
            n = time.time()
            if _cache[f]['t'] is None or n - _cache[f]['t'] > seconds:
                _cache[f]['t'] = n
                _cache[f]['v'] = f(*args, **kwargs)
            return _cache[f]['v']
        return wrapped
    return decorator

@cache(seconds=60)
def get_latest_tweet(user="irth7"):
    print("Requesting")
    resp = requests.get(f"https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={user}&count=1", headers={'Authorization': f"Bearer {BEARER_TOKEN}"})
    data = json.loads(resp.text)
    return data[0]["text"], data[0]["id"]

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    opis, tid = get_latest_tweet()
    return render_template('index.html', opis=opis, url=f"https://twitter.com/irth7/status/{tid}")
