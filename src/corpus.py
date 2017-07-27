from collections import defaultdict
from nltk.util import ngrams as to_ngrams

from src.ngram_model import tokenize


class Corpus(object):

    def __init__(self, n):
        self.n = n
        self._counts = [defaultdict(int) for _ in range(n)]
        self._hist = [defaultdict(int) for _ in range(n)]
    
    def add_sentence(self, sentence):
        tokenized_sentence = tokenize(sentence)

        for n, count_dict in enumerate(self._counts, 1):
            for ngram in to_ngrams(tokenized_sentence, n):
                count_dict[ngram] += 1

    def count(self, ngram):
        if len(ngram) > self.n: raise ValueError
        return self._counts[len(ngram) - 1][ngram]

    def total(self, n):
        return len(self._counts[n-1].values()) - 2 # don't include <BOS> & <EOS>

    def hist_count(self, ngram, add=1):
        history = ngram[:-1]
        return sum(count for candidate,count in self._counts[len(ngram)-1].items() if candidate[:-1] == history)
