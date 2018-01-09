#!/usr/bin/python3
# coding=utf-8

from pymongo import MongoClient
import sys
import datetime

client = MongoClient('mongodb://localhost:27017')
db = client.local

# 2017/12/30からデータ収集を開始した
beginDate = datetime.date(2017, 12, 30)
today = datetime.date.today()
workday = today
oneday = datetime.timedelta(days = 1)

while (workday >= beginDate):
	# YYYY/MM/DD
	theday = "{0:%Y/%m/%d}".format(workday).replace("/0","/")
	# 投稿月・投稿日の形式注意(○2018/1/2 ×2018/01/02)
	beginTime = theday + " 00:00:00"
	endTime   = theday + " 23:59:59"
	count = db.qa.find({"postdate" : { "$gte": beginTime, "$lte": endTime}}).count()
	print(theday + "," + str(count))
	# 前の日
	workday = workday - oneday
client.close()
