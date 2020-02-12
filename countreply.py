import time
import urllib.request
from bs4 import BeautifulSoup
import sys
from pymongo import MongoClient
import re
import datetime
import json
import syslog

# import pdb
# pdb.set_trace()


def urlopen(url):
    try:
        resp = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        if e.code == 404: # canceled
            return None
        else: # どの道中身は返せない
            return None
    else:
        return resp

# 回答数を取得する
client = MongoClient('mongodb://localhost:27017')
db = client.local

for qa in db.qa.find({"$and":[{"cancel": {"$exists": False}}, {"ansnum": {"$exists": False}}, {"postdate": {"$lte": '2020/01/31'}} ]}):
    resp = urlopen(qa['url'])
    # キャンセル済
    if (resp == None):
        print("Canceled")
        qa['cancel'] = True
    else:
            # 回答数をカウント
        src = resp.read()
        soup = BeautifulSoup(src, 'lxml')
        inf = soup.find("dd", itemprop="answerCount")
        qa['ansnum'] = inf.text
        print(qa['ansnum'])
    print(qa['url'])
    db.qa.update_one({'_id': qa['_id']}, {'$set': qa}, upsert=True)
