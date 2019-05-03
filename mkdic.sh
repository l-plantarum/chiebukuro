python3 mkdic.py dic/univ.txt univ
python3 mkdic.py dic/undergraduate.txt
python3 mkdic.py dic/department.txt
python3 mkdic.py dic/subject.txt
python3 mkdic.py dic/slang.txt
cat dic/univ.csv dic/undergraduate.csv dic/department.csv dic/subject.csv slang.csv > dic/univterm.csv 
/usr/local/libexec/mecab/mecab-dict-index -d/usr/local/lib/mecab/dic/ipadic -u dic/univterm.dic -f utf8 -t utf8 dic/univterm.csv
