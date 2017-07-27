import pytest
from src.corpus import Corpus
from src.ngram_model import ngram_model
from src.ngram_model import START_TOKEN
from src.ngram_model import sentence_prob
from src.math_utils import approx
from src.smoothing import add_one_smoothing
from src.smoothing import no_smoothing


@pytest.fixture
def example_corpus():
    corpus = Corpus(2)
    corpus.add_sentence('John read Moby Dick')
    corpus.add_sentence('Mary read a different book')
    corpus.add_sentence('She read a book by Cher')

    return corpus


def test_integration_no_smoothing(example_corpus):
    
    model = ngram_model(2, no_smoothing)

    estimated_probability = sentence_prob('John read a book', model, example_corpus)
    assert approx(estimated_probability, 0.06, delta=0.01)
    assert sentence_prob('Cher read a book', model, example_corpus) == 0


def test_blah(example_corpus):
    
    model = ngram_model(2, no_smoothing)

    estimate = model([START_TOKEN, 'John'], example_corpus)
    assert approx(estimate, 1/3.0)

    
def test_integration_add_one_smoothing(example_corpus):

    model = ngram_model(2, add_one_smoothing)

    estimate = sentence_prob('John read a book', model, example_corpus)
    
    assert  0.059 < estimate < 0.061
    assert sentence_prob('Cher read a book', model, example_corpus) > 0
