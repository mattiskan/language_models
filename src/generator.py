import os
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

OVERLAP = 2

TARGET_LENGTH = 12
LENGTH_BOOST = 1.0

MIN_PROB = 10 ** -13

def generate_brown():
    print('loading corpus')
    corpus = src.datasets.donald_speech(n=3)

    bridge = defaultdict(list)
    start_ngrams = []
    for ngram, w in corpus.all_ngrams().items():

        if len(ngram) < OVERLAP + 1:
            continue
        
        bridge[ngram[:OVERLAP]].append((ngram, w))

        if ngram[0] == START_TOKEN:
            start_ngrams.append((ngram, w))
       
        
    print('started generation')
    while True:
        try:
            new_sentence = _generate_sentence(start_ngrams, bridge)
            new_sentence_prob = _weighted_prob(new_sentence, corpus)
            if DEBUG: print('sentence_prob', new_sentence_prob)
            
            while MIN_PROB > new_sentence_prob:
                new_sentence = _generate_sentence(start_ngrams, bridge) 
                new_sentence_prob = _weighted_prob(new_sentence, corpus)
                if DEBUG: print('retry: sentence_prob', new_sentence_prob)                

        
            print(_sanitize(new_sentence))
            input()
        except AssertionError:
            continue

def _generate_sentence(start_ngrams, bridge):
    current_ngram = weighted_choice(start_ngrams)

    #import ipdb; ipdb.set_trace()
    
    sentence = [current_ngram[0]]  # let's get this party started
    
    while current_ngram[-1] != END_TOKEN:
        if DEBUG: print(current_ngram)

        #import ipdb; ipdb.set_trace()

        key_for_next_ngram = current_ngram[len(current_ngram) - OVERLAP:]
        current_ngram = weighted_choice(bridge[key_for_next_ngram])

        sentence.append(current_ngram[0])

    sentence.extend(current_ngram[1:])

    return sentence[1:-1]

def _weighted_prob(new_sentence, corpus):
    original_prob = sentence_prob(new_sentence, ngram_model(3, kneser_ney), corpus)
    target_diff = (len(new_sentence) - TARGET_LENGTH)
    adjusted_diff = target_diff
    
    result = original_prob * (2**adjusted_diff)
    if DEBUG: print(locals())
    return result

    
def _sanitize(sentence):
    sentence_str = ' '.join(sentence)

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
    generate_brown()
