
import time
import urllib.request
from bs4 import BeautifulSoup
import sys
from pymongo import MongoClient
import re
import datetime
import json
import syslog


def urlopen(url):
    try:
        resp = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        if e.code == 404: # これは取り消し済
            return None
        else: # どの道中身は返せない
            return None
    else:
        return resp

# 回答数を取得する
client = MongoClient('mongodb://localhost:27017')
db = client.local

for qa in db.qa.find({"$and":[{"cancel": {"$exists": False}}, {"ansnum": {"$exists": False}}, {"postdate": {"$lt": '2019/08/01'}} ]}):
    resp = urlopen(qa['url'])
    # キャンセル済
    if (resp == None):
        print("hoge")
        qa['cancel'] = True
    else:
            # 回答数をカウント
        src = resp.read()
        soup = BeautifulSoup(src, 'lxml')
        inf = soup.find("dd", itemprop="answerCount")
        qa['ansnum'] = inf.text
    db.qa.update_one({'url': qa['url']}, {'$set': qa}, upsert=True)
    print(qa['url'])
