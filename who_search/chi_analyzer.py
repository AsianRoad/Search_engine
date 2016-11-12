# coding=utf-8

import jieba
from whoosh.analysis import Token,Tokenizer

class ChinessTokenizer(Tokenizer):
    def __call__(self, value,positions=False,chars=False,
                 keeporiginal=False,removestops=True,
                 start_pos=0,start_char=0,mode='',**kwargs):
        # assert isinstance(value,text_type)
        t = Token(positions,chars,removestops=removestops,mode=mode,**kwargs)
        seglist = jieba.cut_for_search(value)
        for w in seglist:
            t.original = t.text = w
            t.boost = 1.0
            if positions:
                t.pos =start_pos+value.find(w)
            if chars:
                t.startchar = start_char+value.find(w)
                t.endchar = start_char+value.find(w)+len(w)
            yield t

def ChinesesAnalyzer():
    return ChinessTokenizer()
