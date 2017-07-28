import pytest
from decimal import Decimal
from src.corpus import Corpus
from src.ngram_model import ngram_model
from src.ngram_model import START_TOKEN
from src.ngram_model import sentence_prob
from src.math_utils import approx
from src.smoothing import additive_smoothing
from src.smoothing import no_smoothing


@pytest.fixture
def example_corpus():
    corpus = Corpus(2)
    corpus.add_sentence('John read Moby Dick')
    corpus.add_sentence('Mary read a different book')
    corpus.add_sentence('She read a book by Cher')

    return corpus


def test_example_counts(example_corpus):
    assert example_corpus.unique_word_count() == 11

    assert example_corpus.count(('John', )) == 1
    assert example_corpus.count(('<BOS>', 'John')) == 1

    assert example_corpus.prefix_count(('<BOS>', 'WHATEVER')) == 3


def test_integration_no_smoothing(example_corpus):
    
    model = ngram_model(2, no_smoothing)

    estimated_probability = sentence_prob('John read a book', model, example_corpus)
    assert approx(estimated_probability, 0.06, delta=0.01)
    assert sentence_prob('Cher read a book', model, example_corpus) == 0


def test_blah(example_corpus):
    
    model = ngram_model(2, no_smoothing)

    estimate = model([START_TOKEN, 'John'], example_corpus)
    assert approx(estimate, 1/3.0)

    
def test_integration_additive_smoothing(example_corpus):
    
    model = ngram_model(2, additive_smoothing)

    estimate = sentence_prob('John read a book', model, example_corpus)
    
    assert approx(estimate, 0.0001, delta=0.00003)
    assert sentence_prob('Cher read a book', model, example_corpus) > 0
