import os
from collections import defaultdict

from src.corpus import Corpus
from src.ngram_model import START_TOKEN
from src.ngram_model import END_TOKEN
from src.ngram_model import ngram_model
from src.ngram_model import sentence_prob
from src.smoothing import kneser_ney
from src.math_utils import weighted_choice
from src.datasets import the_donald

DEBUG = os.environ.get('DEBUG', False)

OVERLAP = 2
LENGTH_BOOST = 0.06

MIN_PROB = 10 ** -15

def generate_brown():
    print('loading corpus')
    corpus = the_donald()

    bridge = defaultdict(list)
    start_ngrams = []
    for ngram, w in corpus.all_ngrams().items():
        if len(ngram) < 3:
            continue
        
        bridge[ngram[:OVERLAP]].append((ngram, w))

        if ngram[0] == START_TOKEN:
            start_ngrams.append((ngram, w))
        
    #import ipdb; ipdb.set_trace()

    print('started generation')
    while True:
        try:
            new_sentence = _generate_sentence(start_ngrams, bridge)
            new_sentence_prob = sentence_prob(' '.join(new_sentence), ngram_model(3, kneser_ney), corpus) * len(new_sentence)**LENGTH_BOOST
            if DEBUG: print('sentence_prob', new_sentence_prob)
            
            while MIN_PROB > new_sentence_prob:
                new_sentence = _generate_sentence(start_ngrams, bridge) 
                new_sentence_prob = sentence_prob(' '.join(new_sentence), ngram_model(3, kneser_ney), corpus) * len(new_sentence)**LENGTH_BOOST
                if DEBUG: print('retry: sentence_prob', new_sentence_prob)                

        
            print(' '.join(new_sentence))
            input()
        except AssertionError:
            continue

def _generate_sentence(start_ngrams, bridge):
    current_ngram = weighted_choice(start_ngrams)

    #import ipdb; ipdb.set_trace()
    
    sentence = list(current_ngram[:OVERLAP-1])  # let's get this party started
    
    while current_ngram[-1] != END_TOKEN:
        #print(current_ngram)

        #import ipdb; ipdb.set_trace()

        key_for_next_ngram = current_ngram[len(current_ngram) - OVERLAP:]
        current_ngram = weighted_choice(bridge[key_for_next_ngram])

        sentence.append(current_ngram[0])

    sentence.extend(current_ngram[1:])

    return sentence[1:-1]
    


if __name__ == '__main__':
    generate_brown()
