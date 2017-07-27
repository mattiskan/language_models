""" This is where all the cool stuff happends.
See http://joneschen.org/spigdog/papers/h015a-techreport.pdf for guidance.
"""
import os
from decimal import Decimal

DEBUG = os.environ.get('DEBUG', False)

def no_smoothing(ngram, corpus):
    return additive_smoothing(ngram, corpus, delta=0)

def additive_smoothing(ngram, corpus, delta=1):
    numerator = delta + corpus.count(ngram)
    denominator = delta*corpus.unique_word_count() + corpus.prefix_count(ngram)

    if DEBUG:
        print(ngram, corpus.count(ngram))
        print(ngram[:-1] + ('*',), corpus.prefix_count(ngram))
        print('|V|', corpus.unique_word_count())
        
        print('num', numerator)
        print('den', denominator)
        print('p:',  numerator / float(denominator))
        print()

    return Decimal(numerator) / Decimal(denominator)

def good_turing(ngram, corpus):
    r = corpus.count(ngram)
    n_r = corpus.num_with_same_count_as(ngram) or 0.00001 # fallback chosen randomly ¯\_(ツ)_/¯

    r_star = Decimal(r + 1) * (Decimal(n_r+1) / Decimal(n_r))
        
    return r_star / Decimal(corpus.nr_count_distr())


def modified_kneser_ney(ngram, corpus):
    pass
