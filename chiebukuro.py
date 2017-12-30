# coding=utf-8

import time
import urllib.request
from bs4 import BeautifulSoup
import sys
from pymongo import MongoClient
import re
import datetime
import json



def insertQuestion(url, main, mainlink):
	# 検索クエリを発行
	resp = urllib.request.urlopen(url)
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
	qbody = question.find("p", class_="yjDirectSLinkTarget").text
	
	now = datetime.datetime.now()
	
	# 質問の一行目の前にタブがいっぱい入るので除去
	body = re.sub(r'^\s+', '', qbody)
	
	client = MongoClient('mongodb://localhost:27017')
	db = client.local
	
	# 既に登録済みか?
	
	res = db.qa.find({"url":url})
	if res.count() != 0:
		return	
	
	# mongoへの書き込み
	data = {
		'author': author.text,
		'url' : url,
		'getdate': now.strftime("%Y/%m/%d %H:%M:%S"),
		'postdate': day + ' ' + time,
		'main': main,
		'mainlink': mainlink, 
		'body': body
	}
	
	db.qa.insert_one(data)
	client.close()

# 知恵袋・大学入試カテゴリのトップページ
url = 'https://chiebukuro.yahoo.co.jp/dir/list.php?did=2079405665&flg=3&type=list&sort=2' 

resp = urllib.request.urlopen(url)
src = resp.read()
soup = BeautifulSoup(src, 'lxml')

qalst = soup.find("ul", id="qalst")
qas = qalst.find_all("dl")

while True:
	for qa in qas:
		dt = qa.find("dt")
		dd = qa.find("dd", class_="maincat")
		it = dt.find("a");
		print('text:'+it.text)
		print('href:'+it.get('href'))
		if dd != None:
			mainq = dd.find("a")
			insertQuestion(it.get('href'), mainq.text, mainq.get('href'))
		else:
			insertQuestion(it.get('href'), '', '')
		time.sleep(1)
		
	anchor = soup.find("strong", id="yschnxtb")
	break
	if anchor == None:
		break
	url = anchor.a.get("href")
	resp = urllib.request.urlopen(anchor.a.get("href"))

