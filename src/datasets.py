import json
import html
from os import listdir
from src.corpus import Corpus
import nltk
from nltk.corpus import brown
from nltk.tokenize import word_tokenize


def brown_dataset(n=3):
    stop_words = {"''", '``', ';', ':', "'"}

    def sentences():
        for sent in brown.sents():
            yield nltk.pos_tag(word for word in sent if word not in stop_words)

    return Corpus.from_dataset(n, sentences())


def donald_tweets(n=3):

    def gen():
        for line in parse_file('the_donald_tweets.json'):
            yield [ (word, '') for word in word_tokenize(line['text']) ]

    return Corpus.from_dataset(n, gen())

    
def donald_speech(n=3):

    def raw_data():
        for fname in listdir('crawler_raw_responses/time.com/'):
            with open('crawler_responses/time.com/' + fname, 'r') as rfile:
                yield from json.load(rfile)

    def tokenize_and_filter(sent):
        return [word for word in word_tokenize(html.unescape(sent)) if word not in {';', ':', '``', '&', '#', "''"}]

    return Corpus.from_dataset(n, (nltk.pos_tag(tokenize_and_filter(sent)) for sent in raw_data()))


def parse_file(filename):
    with open(filename, 'r') as rfile:
        yield from (json.loads(line.strip()) for line in rfile)



