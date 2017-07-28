import json
from src.corpus import Corpus
from nltk.corpus import brown



def brown_dataset(n=3):
    stop_words = {"''", '``', ';', ':', "'"}

    def sentences():
        for sent in brown.sents():
            yield ' '.join(word for word in sent if word not in stop_words)

    return Corpus.from_dataset(n, sentences())


def the_donald(n=3):
    return Corpus.from_dataset(n, (line['text'].split() for line in parse_file('the_donald_tweets.json')))



def parse_file(filename):
    with open(filename, 'r') as rfile:
        yield from (json.loads(line.strip()) for line in rfile)



