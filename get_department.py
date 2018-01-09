#!/usr/bin/python3
# wikipediaの学科リスト

import urllib.request
from bs4 import BeautifulSoup
import sys
import re

url = "https://ja.wikipedia.org/wiki/%E5%AD%A6%E7%A7%91%E3%81%AE%E4%B8%80%E8%A6%A7"

resp = urllib.request.urlopen(url)
src = resp.read()
soup = BeautifulSoup(src, 'lxml')

top = soup.find("div", class_="mw-parser-output")
flag = False

for t in top:
	if (t.name == None):
		continue
	if (t.name == "h3"):
		flag = True
		continue
	if (flag == False):
		continue
	if (t.name == "h2" and t.text == "関連項目[編集]"):
		break
	li = t.find_all("li")
	for l in li:
		print(l.text)
