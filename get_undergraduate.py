# wikipediaの学部リスト

import urllib.request
from bs4 import BeautifulSoup
import sys
import re

url = "https://ja.wikipedia.org/wiki/%E5%AD%A6%E9%83%A8%E3%81%AE%E4%B8%80%E8%A6%A7"

resp = urllib.request.urlopen(url)
src = resp.read()
soup = BeautifulSoup(src, 'lxml')

top = soup.find("div", class_="mw-parser-output")
h2cnt = 0
for t in top:
	if t == None:
		continue
	if t.name == "h2": # 学部の一覧，関連項目
		if h2cnt != 0:
			break
		h2cnt = h2cnt + 1
	if t.name != "ul":
		continue
	li = t.find_all("li")
	for it in li:
		print(it.find("a").text)

