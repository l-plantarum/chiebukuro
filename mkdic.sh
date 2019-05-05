#python3 mkdic.py dic/univ.txt univ
#python3 mkdic.py dic/undergraduate.txt
#python3 mkdic.py dic/department.txt
#python3 mkdic.py dic/subject.txt
#python3 mkdic.py dic/term.txt
cat dic/univ.csv dic/undergraduate.csv dic/department.csv dic/subject.csv dic/term.csv maru.csv > dic/univterm.csv 
/usr/lib/mecab/mecab-dict-index -d/usr/local/src/mecab-ipadic-neologd/build/mecab-ipadic-2.7.0-20070801-neologd-20190425/ -u dic/univterm.dic -f utf8 -t utf8 dic/univterm.csv
