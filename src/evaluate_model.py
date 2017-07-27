import random
import math

from decimal import Decimal

from src.ngram_model import sentence_prob
from src.corpus import Corpus
from src.math_utils import log2


def perplexity(dataset, model):
    return 2 ** cross_entropy(dataset, model)

def cross_entropy(dataset, model):
    training_data, testing_data = _split_data(dataset)

    training_corpus = Corpus.from_dataset(3, training_data)

    log_prob_product = Decimal(0.0)
    word_count = 0
    for sentence in testing_data:
        prob = sentence_prob(sentence, model, training_corpus)

        # log(a * b) <==> log(a) + log(b)
        log_prob_product += log2(prob)
        word_count += len(sentence.split()) - 1

    return -log_prob_product / word_count


def _parse_data(filename):
    with open(filename, 'r') as rfile:
        yield from rfile


def _split_data(data_gen, frac=0.5):
    data = list(data_gen)

    random.shuffle(data)

    cutoff = int(len(data) * frac)
    return data[:cutoff], data[cutoff:]


if __name__ == '__main__':
    from src.ngram_model import ngram_model
    from src.smoothing import additive_smoothing

    from decimal import getcontext
    getcontext().prec = 100

    from nltk.corpus import brown
    brown_dataset = [' '.join(sent) for sent in brown.sents()]
    
    results = []
    for _ in range(3):
        results.append(perplexity(brown_dataset, ngram_model(2, additive_smoothing)))

    print(sum(results) / len(results))
