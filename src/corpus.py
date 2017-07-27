from collections import defaultdict
from nltk.util import ngrams as to_ngrams

from src.ngram_model import tokenize


class Corpus(object):

    def __init__(self, n):
        self.n = n
        self._counts = defaultdict(int)
        self._totals = defaultdict(int)
        self._reverse = defaultdict(int)

    @classmethod
    def from_dataset(cls, n, dataset):
        instance = cls(n)
        for sentence in dataset:
            instance.add_sentence(sentence)

        instance.post_process()
        return instance
    
    def add_sentence(self, sentence):
        tokenized_sentence = tokenize(sentence)

        for n in range(1, self.n + 1):
            for ngram in to_ngrams(tokenized_sentence, n):

                if ngram not in self._counts:
                    self._totals[len(ngram)] += 1

                self._counts[ngram] += 1

    def post_process(self):
        for value in self._counts.values():
            self._reverse[value] += 1
    
    def count(self, ngram):
        if len(ngram) > self.n: raise ValueError
        return self._counts[ngram]

    def num_with_same_count_as(self, ngram):
        return self._reverse[self._counts[ngram]]

    def unique_ngrams(self, n):
        return self._totals[n]

    def unique_word_count(self):
        return self.unique_ngrams(n=1) - 2 # don't include <BOS> & <EOS>

    def prefix_count(self, ngram, add=1):
        return self._counts[ngram[:-1]]


    def nr_count_distr(self):
        if not hasattr(self, '_nr_count_distr'):
            self._nr_count_distr = sum(n_r * r for r,n_r in self._reverse.items())

        return self._nr_count_distr
