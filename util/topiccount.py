#!/usr/bin/python3
# coding=utf-8

from pymongo import MongoClient
import sys
import datetime

client = MongoClient('mongodb://localhost:27017')
db = client.local

beginDate = datetime.date(2018, 1, 1)

for i in (2018, 2019, 2020):
  for j in range(1, 13):
    if (j == 12):
      beginDate = datetime.date(i, j, 1)
      endDate = datetime.date(i + 1, 1, 1);
    else:
      beginDate = datetime.date(i, j, 1)
      endDate = datetime.date(i, j + 1, 1);

    bdaystr = "{0:%Y/%m/%d}".format(beginDate)
    edaystr = "{0:%Y/%m/%d}".format(endDate)
    beginTime = bdaystr + " 00:00:00"
    endTime   = edaystr + " 00:00:00"
    print("{},".format(bdaystr), end="")
    for k in range(150): 
      count = db.test20200113.find({"postdate" : { "$gte": beginTime, "$lt": endTime}, "maxtopic150": k}).count()
      print("{},".format(count), end="")
    print("") # newline
client.close()
