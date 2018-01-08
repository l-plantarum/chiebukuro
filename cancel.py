# キャンセルされた質問にマークをつける

import urllib.request
from pymongo import MongoClient

# url = "https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q11184364016"

client = MongoClient("mongodb://localhost:27017")
db = client.local
allqa = db.qa.find()

for q in allqa:
	# キャンセル済みの質問は調べない
	if "cancel" not in q == True and q["cancel"] == True:
		print("canceled")
		print(q)
		continue
	url = q["url"]
	try:
		resp = urllib.request.urlopen(url)
	except urllib.error.HTTPError as e:
		# キャンセル済みならマークをつける
		if e.code == 404:
			db.qa.update({'url': url}, {'$set':{'cancel': True}})
			print(q)
