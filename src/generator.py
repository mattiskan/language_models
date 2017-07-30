import os
import math
from collections import defaultdict

import src.datasets
from src.corpus import Corpus
from src.ngram_model import START_TOKEN
from src.ngram_model import END_TOKEN
from src.ngram_model import ngram_model
from src.ngram_model import sentence_prob
from src.smoothing import kneser_ney
from src.math_utils import weighted_choice


DEBUG = os.environ.get('DEBUG', False)

OVERLAP = 3

TARGET_LENGTH = 12
LENGTH_BOOST = 10

MIN_PROB = 10**-30

class StartOver(Exception):
    pass


def generate_from(corpus):
    bridge = defaultdict(list)
    start_ngrams = []

    for ngram, w in corpus.all_ngrams().items():

        if len(ngram) <= OVERLAP:
            continue

        bridge[ngram[:OVERLAP]].append((ngram, w))

        if ngram[0] == START_TOKEN:
            start_ngrams.append((ngram, w))

    assert start_ngrams

    print('started generation')
    while True:
        try:
            new_sentence = _generate_sentence(start_ngrams, bridge)
            #import ipdb; ipdb.set_trace()
            new_sentence_prob = _weighted_prob(new_sentence, corpus)
            if DEBUG: print('sentence_prob', new_sentence_prob)
            
            while MIN_PROB > new_sentence_prob:
                new_sentence = _generate_sentence(start_ngrams, bridge) 
                new_sentence_prob = _weighted_prob(new_sentence, corpus)
                if DEBUG: print('retry: sentence_prob', new_sentence_prob, _sanitize(new_sentence))
        
            yield _sanitize(new_sentence)
        except StartOver:
            continue

def _generate_sentence(start_ngrams, bridge):
    current_ngram = weighted_choice(start_ngrams)

    #import ipdb; ipdb.set_trace()
    sentence = [current_ngram[0]]  # let's get this party started

    only_choice = 0
    
    while current_ngram[-1] != END_TOKEN:
        if DEBUG: print(current_ngram)

        key_for_next_ngram = current_ngram[len(current_ngram) - OVERLAP:]

        choices = bridge[key_for_next_ngram]

        if len(choices) == 1:
            only_choice += 1

        current_ngram = weighted_choice(choices)
        sentence.append(current_ngram[0])

    
    print('only_choice', float(only_choice) / len(sentence))
    if float(only_choice) / len(sentence) > 0.8:
        raise StartOver
    
            
    sentence.extend(current_ngram[1:])

    #import ipdb; ipdb.set_trace()

    return sentence

def _weighted_prob(new_sentence, corpus):
    original_prob = ngram_model(4, kneser_ney)(new_sentence, corpus)
    return original_prob

    length_diff = len(new_sentence) - 3

    #print(new_sentence)
    #print('len', len(new_sentence))
    #print('prob', original_prob)
    #print('diff', length_diff)
    #
    #wb = original_prob * (10**length_diff)
    #print('weighted', wb)
    #input()
    return original_prob * (3**length_diff)

    
def _sanitize(sentence):
    #import ipdb; ipdb.set_trace()
    sentence_str = ' '.join(word for word, pos in sentence[1:-1])

    for appo in ("'", '’'):
        sentence_str = sentence_str.replace(f" n{appo}t", f"n{appo}t")
        sentence_str = sentence_str.replace(f" {appo}ve", f"{appo}ve")
        sentence_str = sentence_str.replace(f" {appo}s", f"{appo}s")
        sentence_str = sentence_str.replace(f" {appo}d", f"{appo}d")
        sentence_str = sentence_str.replace(f" {appo}re", f"{appo}re")
        sentence_str = sentence_str.replace(f" {appo}m", f"{appo}m")
        sentence_str = sentence_str.replace(f" {appo}ll", f"{appo}ll")
        sentence_str = sentence_str.replace(f" {appo}ll", f"{appo}ll")

        sentence_str = sentence_str.replace(f" {appo} ", f"{appo}")

    sentence_str = sentence_str.replace(" ,", ",")
    sentence_str = sentence_str.replace(" .", ".")
    sentence_str = sentence_str.replace(" ?", "?")
    return sentence_str
    

if __name__ == '__main__':
    print('loading corpus')

    corpus = src.datasets.donald_speech(n=4)

    #from collections import defaultdict
    #probs = defaultdict(list)
    #
    #for (sent, prob), i in zip(generate_from(corpus), range(10**6)):
    #    if not (i % 1000):
    #        print(i)
    #    probs[len(sent)].append(prob)
    #
    #with open('averages.csv', 'w') as wfile:
    #    for key,values in sorted(probs.items()):
    #        tot = len(values)
    #        print(key, sum(values) / tot, sep=',', file=wfile)
    #
    #
    #exit()
    for sentence in generate_from(corpus):
        print(sentence)
        input()
