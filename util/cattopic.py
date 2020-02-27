#!/usr/bin/python3
# coding=utf-8

from pymongo import MongoClient
import sys
import getopt

testdb = "test20200113"
qadb = "qa20200113"
begindate = "2018/01/01"
enddate = "2019/12/31"
ntopic = "150"
topicid = -1
prob = "0.6"

opts, args = getopt.getopt(sys.argv[1:], "n:f:t:i:p:h",  longopts=[])

for opt, arg in opts:
	if opt == "-h":
		print("[usage] cattopic.py [-n {150|20}] [-f <from>] [-t <to>] -i <topicid> -p <probability>\n")
		sys.exit(0)
	if opt == "-n":
		if arg != "150" and arg != "20":
			print("-n 150 or -n 20")
			sys.exit(1)
		ntopic = arg
	if opt == "-f":
		begindate = arg
	if opt == "-t":
		enddate = arg
	if opt == "-i":
		topicid = int(arg)
	if opt == "-p":
		prob = arg

if topicid == -1:
	print("topicid must be specified\n")
	sys.exit(1)

client = MongoClient('mongodb://localhost:27017')
db = client.local

if ntopic == "150":
	posts = db[testdb].find({"maxtopic150": topicid, "maxprob150": {"$gte": prob}, "postdate": {"$gte": begindate, "$lte": enddate}}, {"_id"})
if ntopic == "20":
	posts = db[testdb].find({"maxtopic20": topicid, "maxprob20": {"$gte": prob}, "postdate": {"$gte": begindate, "$lte": enddate}}, {"_id"})

for p in posts:
	id = p	
	post = db[qadb].find(id, {"body", "postdate"})
	for q in post:
		print("{}:{}".format(q['postdate'], q['body']))

client.close()

