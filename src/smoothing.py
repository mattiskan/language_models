""" This is where all the cool stuff happends.
See http://joneschen.org/spigdog/papers/h015a-techreport.pdf for guidance.
"""
import os

DEBUG = os.environ.get('DEBUG', False)

def no_smoothing(ngram, corpus):
    if DEBUG:
        print(ngram, corpus.count(ngram))
        print(ngram[:-1] + ('*',), corpus.count(ngram[:-1]))
        print('|V|', corpus.total(1))
        print('p:',  corpus.count(ngram) / float(corpus.count(ngram[:-1])))
        print()
    
    return corpus.count(ngram) / float(corpus.count(ngram[:-1]))

def additive_smoothing(ngram, corpus, delta=1):
    numerator = delta + corpus.count(ngram)
    denominator = delta*corpus.total(1) + corpus.count(ngram[:-1])

    if DEBUG:
        print(ngram, corpus.count(ngram))
        print(ngram[:-1] + ('*',), corpus.count(ngram[:-1]))
        print('|V|', corpus.total(1))
        
        print('num', numerator)
        print('den', denominator)
        print('p:',  numerator / float(denominator))
        print()

    return numerator / float(denominator)
