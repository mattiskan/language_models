import json
import html
import os
import pickle
from src.corpus import Corpus
import nltk
from nltk.corpus import brown
from nltk.tokenize import word_tokenize


def cached(dataset_function):

    def decorator(n=3):
        cache_path = f'corpus_cache/{dataset_function.__name__}_{n}.pickle'
        try:
            with open(cache_path, 'rb') as rfile:
                return pickle.load(rfile)
        except IOError:
            print('Missed cache: Generating corpus...')

        corpus = dataset_function(n)
        with open(cache_path, 'wb') as wfile:
            pickle.dump(corpus, wfile)

        return corpus

    return decorator
    

@cached
def brown_dataset(n=3):
    stop_words = {"''", '``', ';', ':', "'"}

    def sentences():
        for sent in brown.sents():
            yield nltk.pos_tag(word for word in sent if word not in stop_words)

    return Corpus.from_dataset(n, sentences())

@cached
def donald_tweets(n=3):

    def gen():
        for line in parse_file('data/the_donald_tweets.json'):
            yield [ (word, '') for word in word_tokenize(line['text']) ]

    return Corpus.from_dataset(n, gen())

@cached
def donald_speech(n=3):

    def raw_data():
        for fname in os.listdir('data/crawler_responses/time.com/'):
            with open('data/crawler_responses/time.com/' + fname, 'r') as rfile:
                yield from json.load(rfile)

    def tokenize_and_filter(sent):
        return [word for word in word_tokenize(html.unescape(sent)) if word not in {';', ':', '``', '&', '#', "''"}]

    return Corpus.from_dataset(n, (nltk.pos_tag(tokenize_and_filter(sent)) for sent in raw_data()))


def parse_file(filename):
    with open(filename, 'r') as rfile:
        yield from (json.loads(line.strip()) for line in rfile)



