""" This is where all the cool stuff happends.
See http://joneschen.org/spigdog/papers/h015a-techreport.pdf for guidance.
"""
import os
from decimal import Decimal
from collections import defaultdict
from functools import lru_cache

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

    return numerator / float(denominator)

def good_turing(ngram, corpus):
    r = corpus.count(ngram)
    n_r = corpus.num_with_same_count_as(ngram) or 0.00001 # fallback chosen randomly ¯\_(ツ)_/¯

    r_star = (r + 1) * (n_r+1) / float(n_r)
        
    return r_star / float(corpus.nr_count_distr())

def kneser_ney(ngram, corpus):

    assert isinstance(ngram, tuple)
    
    n1, n2, n3, n4 = [corpus.count_with_len(n) for n in (1,2,3,4)]
    
    Y = n1 / (n1 + 2*n2)

    D = defaultdict(lambda: D[3], {
        0: 0.0,
        1: 1 - 2 * Y * (n2 / n1),
        2: 2 - 3 * Y * (n3 / n2),
        3: 3 - 4 * Y * (n4 / n3),
    })

    #import ipdb; ipdb.set_trace()
    
    if len(ngram) == 1:
        if DEBUG:
            print(ngram, corpus.specific_prefix_count(ngram[0]) / corpus.unique_ngrams(n=2))

        return corpus.specific_prefix_count(ngram[0]) / float(corpus.unique_ngrams(n=2))


    term1 = (corpus.count(ngram) - D[corpus.count(ngram)]) / (corpus.prefix_count(ngram) or 1)


    term2 = kneser_ney(ngram[1:], corpus) * (
        D[1] * corpus.postfixes_occuring_exactly(ngram[:-1], 1)
        + D[2] * corpus.postfixes_occuring_exactly(ngram[:-1], 2)
        + D[3] * corpus.postfixes_occuring_at_least(ngram[:-1], 3)
    ) / (corpus.prefix_count(ngram) or 1.0)

    if corpus.prefix_count(ngram) == 0:
        assert not corpus.postfixes_occuring_exactly(ngram[:-1], 1)
        assert not corpus.postfixes_occuring_exactly(ngram[:-1], 2)
        assert not corpus.postfixes_occuring_at_least(ngram[:-1], 3)

    if DEBUG:
        print(ngram, term1 + term2)

    #import ipdb; ipdb.set_trace()
    return term1 + term2
