# coding=utf-8

import MeCab
import sys
from pymongo import MongoClient

tagger = MeCab.Tagger('-F\s%f[6] -U\s%m -E\\n')
client = MongoClient('mongodb://localhost:27017')
db = client.local

post = db.qa.find().limit(10)
for it in post:
	result = tagger.parse(it['body'])
	print(result[1:])
