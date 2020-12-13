#!/usr/bin/python3
# coding=utf-8

from pymongo import MongoClient
import sys
import datetime

tablename = "test20200304"

client = MongoClient('mongodb://localhost:27017')
db = client.local

print(",", end='')
r = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 500, 1000, 2000, 100000]
for k in r:
	print("{},".format(k), end='')
print()

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
    for k in range(len(r) - 1):
      count = db[tablename].find({"postdate" : { "$gte": beginTime, "$lt": endTime}, "nwords": {"$gte": r[k], "$lt": r[k + 1]}}).count()
      print("{},".format(count), end="")
    print("") # newline
client.close()
