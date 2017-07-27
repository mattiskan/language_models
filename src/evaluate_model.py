import random
import math

from decimal import Decimal
from decimal import getcontext
from collections import defaultdict

from src.smoothing import additive_smoothing
from src.smoothing import good_turing
from src.ngram_model import sentence_prob
from src.ngram_model import ngram_model
from src.corpus import Corpus
from src.math_utils import log2


def perplexity(model, corpus, testing_data):
    return 2 ** cross_entropy(model, corpus, testing_data)

def cross_entropy(model, corpus, testing_data):

    log_prob_product = Decimal(0.0)
    word_count = 0
    for sentence in testing_data:
        prob = sentence_prob(sentence, model, corpus)

        # log(a * b) <==> log(a) + log(b)
        log_prob_product += log2(prob)
        word_count += len(sentence.split()) - 1

    return -log_prob_product / word_count


def _parse_data(filename):
    with open(filename, 'r') as rfile:
        yield from rfile


def _split_data(data, frac=0.5):
    random.shuffle(data)

    cutoff = int(len(data) * frac)
    return data[:cutoff], data[cutoff:]


if __name__ == '__main__':

    getcontext().prec = 100

    from nltk.corpus import brown
    brown_dataset = [' '.join(sent) for sent in brown.sents()]

    results = defaultdict(list)
    for _ in range(3):
        training_data, testing_data = _split_data(brown_dataset)
        corpus = Corpus.from_dataset(3, training_data)
        
        for smoothing_method in [additive_smoothing, good_turing]:
            results[smoothing_method.__name__].append(
                perplexity(ngram_model(3, smoothing_method), corpus, testing_data)
            )

    for smoothing_name, _results in results.items():
        print(smoothing_name, sum(_results) / len(_results))
