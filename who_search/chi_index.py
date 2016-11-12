# coding=utf-8


from  whoosh.fields import Schema, TEXT,ID
from  whoosh import index
from  whoosh.filedb.filestore import FileStorage

import os
import re
import json

import chi_analyzer

def zhprint(obj):
    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())

analyzer = chi_analyzer.ChinesesAnalyzer()

schema = Schema(title=TEXT(stored=True),content=TEXT(stored=True,analyzer=analyzer),url = ID(stored=True))
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

ix = index.create_in("indexdir", schema)

stopwords = open('E:\\search_engine\\chinese_stopword.txt').read()
with open("E:\\who_search\\second.json",'r') as f:
    d1 = json.load(f)

writer = ix.writer()

for d in d1:
    # print d['data']
    # print d['title']
    # print d['url']
    writer.add_document(title=d['title'],content =d['data'],url= d['url'] )
writer.add_document(title=u"学习",content=u"今天看了一部电影",)

writer.commit()

searcher = ix.searcher()
results = searcher.find("content",u"一遍下来还不太明白")
print results[0].highlights("content")
