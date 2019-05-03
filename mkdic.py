# coding=utf-8

import MeCab
import sys

if len(sys.argv) == 1:
	print("mkdir.py <file> [univ]\n")
	sys.exit(1)
if len(sys.argv) == 3 and sys.argv[2] == 'univ':
	dictype = '固有名詞'
	nauntype = '組織'
else:
	dictype = '名詞'
	nauntype = '一般'

tagger = MeCab.Tagger('-Oyomi')
out = sys.argv[1].replace(".txt", ".csv")

fo = open(out, 'w')
fi = open(sys.argv[1], 'r')
line = fi.readline()
while line:
	naun = line.replace('\n', '')
	yomi = tagger.parse(naun).replace('\n', '')
	fo.write('{naun},*,*,2000,名詞,{dictype},{nauntype},*,*,*,{naun},{yomi},{yomi}\n'.format(naun=naun, dictype=dictype, nauntype=nauntype, yomi=yomi))
	line = fi.readline()
		
fi.close();
fo.close()



