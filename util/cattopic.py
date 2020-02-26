#!/usr/bin/python3
# coding=utf-8

from pymongo import MongoClient
import sys

testdb = "test20200113"
qadb = "qa20200113"

client = MongoClient('mongodb://localhost:27017')
db = client.local

# cattopic.py {150|20} id th

topic = int(sys.argv[2])
prob = sys.argv[3]
posts = db[testdb].find({"maxtopic150":"34","maxprob150":{"$gte":"0.5"}})

if sys.argv[1] == "150":
	posts = db[testdb].find({"maxtopic150": topic, "maxprob150": {"$gte": prob}}, {"_id"})
elif sys.argv[1] == "20":
	posts = db[testdb].find({"maxtopic20": topic, "maxprob20": {"$gte": prob}}, {"_id"})
else:
	print("cattopic.py {150|20} <topicid> <probablity>")
	sys.exit(0)

for p in posts:
	id = p	
	post = db[qadb].find(id, {"body", "postdate"})
	for q in post:
		print("{}:{}".format(q['postdate'], q['body']))

client.close()

