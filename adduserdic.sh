cat ../dic/univ.dic ../dic/subject.txt.dic ../dic/term.txt.dic ../dic/slang.txt.dic ../dic/department.dic ../dic/undergraduate.dic > chiebukuro.csv
/usr/local/libexec/mecab/mecab-dict-index -d/home/katsumi/mecab-ipadic-2.7.0-20070801 -u chiebukuro.dic -f utf-8 -t utf-8 chiebukuro.csv
