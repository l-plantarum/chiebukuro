# 文科省のサイトから大学名のリストを取得する

import urllib.request
from bs4 import BeautifulSoup
import sys
import re

national_url = "http://www.mext.go.jp/b_menu/link/daigaku1.htm"
public_url = "http://www.mext.go.jp/b_menu/link/daigaku2.htm"
private_url = "http://www.mext.go.jp/b_menu/link/daigaku4.htm"

# 国立大学
resp = urllib.request.urlopen(national_url)
src = resp.read()
soup = BeautifulSoup(src, 'lxml')

univs = soup.find_all("td", class_="table-back")
for u in univs:
	uname = u.find("a")
	if uname != None and uname.text != "":
		print(uname.text)

# 公立大学

resp = urllib.request.urlopen(public_url)
src = resp.read()
soup = BeautifulSoup(src, 'lxml')

top = soup.find("div", class_="wysiwyg")

univs = top.find_all("li")
for u in univs:
	uname = u.find("a")
	if uname != None and uname.text != "":
		print(re.sub(r'（.*$', '', uname.text))

# 私立大学
resp = urllib.request.urlopen(private_url)
src = resp.read()
soup = BeautifulSoup(src, 'lxml')

univs = soup.find_all("td", class_="table-back")
for u in univs:
	uname = u.find("a")
	if uname != None and uname.text != "":
		print(uname.text)
