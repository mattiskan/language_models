import os
import math

from nltk.util import ngrams as to_ngrams

DEBUG = os.environ.get('DEBUG', False)

START_TOKEN = '<BOS>'
END_TOKEN = '<EOS>'


def sentence_prob(sentence, model, corpus):
    sentence = tokenize(sentence)
    return model(sentence, corpus)


def ngram_model(n, smoothing):
    def probability_function(sentence, corpus):
        prob = 1.0

        for ngram in to_ngrams(sentence, n):
            prob *= smoothing(ngram, corpus)

            if not prob:
                break

        return prob
    return probability_function

  
def tokenize(sentence):
    if (START_TOKEN in sentence) or (END_TOKEN in sentence):
        raise ValueError(f'Sentence already tokenized: {sentence}')

    return [START_TOKEN] + sentence + [END_TOKEN]
