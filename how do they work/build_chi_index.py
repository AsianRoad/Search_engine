# coding=utf-8
import codecs
import re
import jieba
import math


def zhprint(obj):
    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())

class BuildIndex:

    def __init__(self,files):
        self.tf = {}
        self.df = {}
        self.idf = {}
        self.filenames = files
        self.file_to_terms = self.process_files()
        self.regdex = self.regIndex()
        self.totalIndex = self.execute()
        self.vectors = self.vectorize()
        self.mags = self.magnitude(self.filenames)
        self.populateScores()

    def process_files(self):
        file_to_terms = {}
        for file in self.filenames:
            file_to_terms[file] = open(file, 'r').read()
            stopwords = open('E:\\search_engine\\chinese_stopword.txt').read()
            file_to_terms[file] = " ".join(jieba.cut_for_search(file_to_terms[file]))
            file_to_terms[file] = file_to_terms[file].split()
            file_to_terms[file] = [w for w in file_to_terms[file] if w.encode('utf-8') not in stopwords]
        return file_to_terms

    def index_one_file(self,termlist):
        file_index = {}
        for index , word in enumerate(termlist):
            if word in file_index.keys():
                file_index[word].append(index)
            else:
                file_index[word] = [index]
        return file_index


    def make_indices(self,termlists):
        total = {}
        for filename in termlists.keys():
            total[filename] = self.index_one_file(termlists[filename])
        return total

    def full_index(self):
        total_index = {}
        indie_indices = self.regdex
        for filename in indie_indices.keys():
            self.tf[filename] = {}
            for word in indie_indices[filename].keys():
                self.tf[filename][word] = len(indie_indices[filename][word])
                if word in self.df.keys():
                    self.df[word] += 1
                else:
                    self.df[word] = 1
                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        total_index[word][filename].append(indie_indices[filename][word][:])
                    else:
                        total_index[word][filename] = indie_indices[filename][word]
                else:
                    total_index[word] = {filename:indie_indices[filename][word]}
        return  total_index


    def regIndex(self):
        return self.make_indices(self.file_to_terms)

    def execute(self):
        return self.full_index()

    def getUniques(self):
        return self.totalIndex.keys()

    def vectorize(self):
        vectors = {}
        for filename in self.filenames:
            vectors[filename] = [len(self.regdex[filename][word]) for word in self.regdex[filename].keys()]
        return vectors

    def term_frequency(self,term,document):
        return self.tf[document][term]/self.mags[document] if term in self.tf[document].keys() else 0

    def idf_func(self,N,N_t):
        if N_t != 0:
            return math.log(N/N_t)
        else:
            return 0

    def document_frequency(self, term):
        if term in self.totalIndex.keys():
            return len(self.totalIndex[term].keys())
        else:
            return 0

    def generateScore(self,term,document):
        return self.tf[document][term] * self.idf[term]

    def populateScores(self):
        for filename in self.filenames:
            for term in self.getUniques():
                self.tf[filename][term] = self.term_frequency(term, filename)
                if term in self.df.keys():
                    self.idf[term] = self.idf_func(self.collection_size(), self.df[term])
                else:
                    self.idf[term] = 0
        return self.df, self.tf, self.idf

    def magnitude(self, documents):
        mags = {}
        for document in documents:
            mags[document] = pow(sum(map(lambda x:x**2, self.vectors[document])),.5)
        return mags

    def collection_size(self):
        return len(self.filenames)


# i = BuildIndex(['E:\\search_engine\\corpus\\chi1.txt','E:\\search_engine\\corpus\\chi2.txt'])
# zhprint (  i.totalIndex )
# zhprint( i.df )
# zhprint( i.tf )
# zhprint( i.idf )

