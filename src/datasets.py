import json
from os import listdir
from src.corpus import Corpus
from nltk.corpus import brown
from nltk.tokenize import word_tokenize


def brown_dataset(n=3):
    stop_words = {"''", '``', ';', ':', "'"}

    def sentences():
        for sent in brown.sents():
            yield [word for word in sent if word not in stop_words]

    return Corpus.from_dataset(n, sentences())


def donald_tweets(n=3):
    return Corpus.from_dataset(n, (line['text'].split() for line in parse_file('the_donald_tweets.json')))


def donald_speech(n=3):

    def results():
        for fname in listdir('crawler_raw_responses/time.com/'):
            with open('crawler_responses/time.com/' + fname, 'r') as rfile:
                yield from json.load(rfile)


    def tokenize_and_filter(sent):
        return [word for word in word_tokenize(sent) if word not in {'.', ';', ':'}]

    return Corpus.from_dataset(n, (tokenize_and_filter(sent) for sent in results()))


def parse_file(filename):
    with open(filename, 'r') as rfile:
        yield from (json.loads(line.strip()) for line in rfile)



