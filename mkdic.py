# coding=utf-8

import MeCab
import sys

if len(sys.argv) == 1:
	print("mkdir.py <file> [univ]\n")
	sys.exit(1)
if len(sys.argv) == 3 and sys.argv[2] == 'univ':
	dictype = '固有名詞'
else:
	dictype = '名詞'

tagger = MeCab.Tagger('-Oyomi')
out = sys.argv[1] + ".dic"

fo = open(out, 'w')
fi = open(sys.argv[1], 'r')
line = fi.readline()
while line:
	naun = line.replace('\n', '')
	yomi = tagger.parse(naun).replace('\n', '')
	fo.write('{naun},*,*,*,名詞,{dictype},組織,*,*,*,{naun},{yomi},{yomi}\n'.format(naun=naun, dictype=dictype,yomi=yomi))
	line = fi.readline()
		
fi.close();
fo.close()



