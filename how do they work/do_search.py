# coding=utf-8

import query_texts
import re

def zhprint(obj):
    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())

q = query_texts.Query(['E:\\search_engine\\corpus\\chi1.txt','E:\\search_engine\\corpus\\chi2.txt'])

zhprint(q.invertedIndex)

search_words = raw_input('请输入搜索内容: ').decode('utf-8')
# print search_words
results =  q.free_text_query(search_words)
print results
if results[0]:
    for r in results:
        print r.keys()[0]

else:
    print '没有找到'