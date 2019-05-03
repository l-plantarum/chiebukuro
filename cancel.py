#!/usr/bin/python3
# キャンセルされた質問にマークをつける

import urllib.request
from pymongo import MongoClient
import datetime
import time

# 古すぎてキャンセル期間を過ぎているか
def isOld(postdatetime):
	# 日付と時間で区切る
	daytime = postdatetime.split()
	# 日付を区切る
	postdate = daytime[0].split('/')
	# 日付をdatetime.dateに変換
	postday = datetime.date(int(postdate[0]), int(postdate[1]), int(postdate[2]))
	
	# 今日より8日前
	today = datetime.date.today()
	eighth = datetime.timedelta(days = 8)
	threshold = today - eighth
	if threshold > postday:
		return True 
	else:
		return False


client = MongoClient("mongodb://localhost:27017")
db = client.local
allqa = db.qa.find()

canceled = []

print("search all entries")

for q in allqa:
	# キャンセル済みの質問は調べない
	if "cancel" not in q == True and q["cancel"] == True:
		print("canceled entry:")
		print(q["body"])
		continue
	url = q["url"]
	# 取り消せるのは最初の一週間なので8日経ったら調べない
	postdate = q["postdate"]
	if isOld(postdate):
		continue
	try:
		resp = urllib.request.urlopen(url)
		time.sleep(1)
	except urllib.error.HTTPError as e:
		# キャンセル済みならリストに追加する
		if e.code == 404:
			print(url)
			canceled.append(url)

print("update database")
for c in canceled:
	db.qa.update({'url': c}, {'$set':{'cancel': True}})
