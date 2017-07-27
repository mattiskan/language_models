import pytest

from src.corpus import Corpus
from src.ngram_model import START_TOKEN
from src.ngram_model import END_TOKEN
   

def test_count():
    corpus = Corpus(2)
    corpus.add_sentence('a b c')

    assert corpus.count(('a', 'b')) == 1
    assert corpus.count((START_TOKEN, 'a')) == 1
    assert corpus.count(('c', END_TOKEN)) == 1

def test_count_unsupported_ngram():
    corpus = Corpus(3)
    unsupported_ngram = ('a',)*4
    
    with pytest.raises(ValueError):
        corpus.count(unsupported_ngram)
