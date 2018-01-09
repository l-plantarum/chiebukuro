#!/usr/bin/python3
# coding=utf-8

import time
import urllib.request
from bs4 import BeautifulSoup
import sys
from pymongo import MongoClient
import re
import datetime
import json
import syslog


# 指定した記事を開き，取り消し済みならNoneを返す
def urlopen(url):
	try:
		resp = urllib.request.urlopen(url)
	except urllib.HTTPError as e:
		if e.code == 404: # これは取り消し済
			return None
		else: # どの道中身は返せない
			return None
	else:
		return resp

# 指定したURLのページを情報を取得しMongoDBに追加する
def insertQuestion(url, main, mainlink):
	# 登録済URLなら以下の処理は実施しない
	client = MongoClient('mongodb://localhost:27017')
	db = client.local
	res = db.qa.find({"url":url})
	if res.count() != 0:
		return	
	# 取り消し済みなら何もしない
	if "cancel" not in res == True:
		return
	
	# 検索クエリを発行
	resp = urlopen(url)
	# 最初から取り消ししてあれば何もしない
	if resp == None: 
		return
	src = resp.read()
	soup = BeautifulSoup(src, 'lxml')
	
	# 質問
	usrQ = soup.find("div", class_="usrQstn")
	# 質問者情報
	usrInfo = usrQ.find("div", class_="usrInfo")
	author = usrInfo.find("p", class_="usrNm")
	posttime = usrInfo.find("p", class_="upDt")
	# <p>日付<span>時間</span></p>から時間を取得後，時間を除去
	time = posttime.span.string
	posttime.span.extract()
	day = posttime.text

	# 投稿
	question = usrQ.find("div", class_="ptsQes")
	qbody = question.find_all("p", class_="yjDirectSLinkTarget")

	# 質問の前後にタブがいっぱい入るので除去
	# 一行しかない質問なら配列の長さは1
	# 複数行あれば配列の長さは2
	car = re.sub('^s+$', '', re.sub(r'^\s+', '', qbody[0].text))
	if (len(qbody) == 2):
		cdr = re.sub(r'\s+$', '', re.sub(r'^\s+', '', qbody[1].text))

	# 補足
	qsup = question.find("p", class_="queTxtsup")
	if (qsup != None):
		sup = qsup.text
	else:
		sup = ''
	
	# お礼
	thxpt = question.find("cc", class_="cin")
	if (thxpt != None):
		point = thxpt.text.replace('枚', '')
	else:
		point = 0

	# 現在時刻
	now = datetime.datetime.now()
	
	# MongoDBに接続
	client = MongoClient('mongodb://localhost:27017')
	db = client.local
	
	# mongoへの書き込み
	data = {
		'author': author.text,
		'url' : url,
		'getdate': now.strftime("%Y/%m/%d %H:%M:%S"),
		'postdate': day + ' ' + time,
		'main': main,
		'mainlink': mainlink, 
		'body': car + cdr,
		'point': point,
		'sup': sup
	}
	
	db.qa.insert_one(data)
	client.close()


# syslogに質問件数を書き込む
def outputCount(msg):
	client = MongoClient('mongodb://localhost:27017')
	db = client.local
	count = db.qa.count()
	syslog.openlog("chiebukuro")
	syslog.syslog(msg + ":" + str(count))
	client.close()

# 知恵袋・大学入試カテゴリのトップページ
url = 'https://chiebukuro.yahoo.co.jp/dir/list.php?did=2079405665&flg=3&type=list&sort=2' 

# トップページの情報を取得
resp = urllib.request.urlopen(url)

# バッチモード
if len(sys.argv) == 2 and sys.argv[1] == "--batch":
	batchMode = True
else:
	batchMode = False


if batchMode == True:
	outputCount("begin")

while True:
	src = resp.read()
	soup = BeautifulSoup(src, 'lxml')

	qalst = soup.find("ul", id="qalst")
	qas = qalst.find_all("dl")
	for qa in qas:
		dt = qa.find("dt")
		dd = qa.find("dd", class_="maincat")
		it = dt.find("a");
		if batchMode == False:
			print('text:'+it.text)
			print('href:'+it.get('href'))
		if dd != None:
			mainq = dd.find("a")
			insertQuestion(it.get('href'), mainq.text, mainq.get('href'))
		else:
			insertQuestion(it.get('href'), '', '')
		time.sleep(1)
		
	anchor = soup.find("strong", id="yschnxtb")
	if anchor == None:
		break
	url = anchor.a.get("href")
	time.sleep(10)
	if batchMode == False:
		print('anchor:'+anchor.a.get("href"))
	else:
		syslog.syslog(anchor.a.get("href"))
	resp = urllib.request.urlopen(anchor.a.get("href"))

if batchMode == True:
	outputCount("begin")
