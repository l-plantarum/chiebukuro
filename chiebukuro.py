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
	except urllib.error.HTTPError as e:
		if e.code == 404: # これは取り消し済
			return None
		else: # どの道中身は返せない
			return None
	else:
		return resp

# 指定したURLのページを情報を取得しMongoDBに追加する
# True: DBの内容を変更した
# False: DBの内容はそのまま
def insertQuestion(url, main, mainlink):
	# 登録済URLなら以下の処理は実施しない
	client = MongoClient('mongodb://localhost:27017')
	db = client.local
	res = db.qa.find({"url":url})
	if res.count() != 0:
		return False	
	# 取り消し済みなら何もしない
	if "cancel" not in res == True:
		return False
	
	# 検索クエリを発行
	resp = urlopen(url)
	# 最初から取り消ししてあれば何もしない
	if resp == None: 
		return False
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
	arr = day.split('/')
	if (len(arr[1]) == 1):
		arr[1] = '0' + arr[1]
	if (len(arr[2]) == 1):
		arr[2] = '0' + arr[2]
	day = '/'.join(arr)

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
	return True


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

# オプション
batchMode = False
allMode = False
for i in range(1, len(sys.argv)):
	# バッチモード
	if sys.argv[i] == "--batch":
		batchMode = True
	if sys.argv[i] == "--all":
		allMode = True

if batchMode == True:
	outputCount("begin")

breakFlag = False
series = 0
# 最後までクロールしたらbreakする
while True:
	src = resp.read()
	soup = BeautifulSoup(src, 'lxml')

	qalst = soup.find("ul", id="qalst")
	qas = qalst.find_all("dl")

	# 一画面分
	for qa in qas:
		dt = qa.find("dt")
		dd = qa.find("dd", class_="maincat")
		it = dt.find("a");
		# クロール中の記事のタイトルとURLの表示
		if batchMode == False:
			print('text:'+it.text)
			print('href:'+it.get('href'))
		if dd != None:
			# 複数カテゴリへの投稿
			mainq = dd.find("a")
			dbFlag = insertQuestion(it.get('href'), mainq.text, mainq.get('href'))
		else:
			# 当該カテゴリのみへの投稿
			dbFlag = insertQuestion(it.get('href'), '', '')
		if dbFlag == False:
			series = series + 1
		else:
			series = 0
			time.sleep(1)
		if allMode == False and series == 10:
			breakFlag = True
			break
		
	if breakFlag == True:
		break
	# 次へのリンクを探す
	anchor = soup.find("strong", id="yschnxtb")
	# なければ終了(最後までクロールした)
	if anchor == None:
		break
	url = anchor.a.get("href")
	time.sleep(10)
	# 次のクロールする質問リスト
	if batchMode == False:
		print('anchor:'+anchor.a.get("href"))
	else:
		syslog.syslog(anchor.a.get("href"))
	resp = urllib.request.urlopen(anchor.a.get("href"))

if batchMode == True:
	outputCount("begin")
