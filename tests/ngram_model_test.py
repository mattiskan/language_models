import mock
import pytest

from decimal import Decimal
from src.ngram_model import tokenize
from src.ngram_model import ngram_model
from src.ngram_model import START_TOKEN
from src.ngram_model import END_TOKEN
from src.math_utils import approx

def test_tokenize():
    assert tokenize('') == [START_TOKEN, END_TOKEN]
    assert tokenize('foo') == [START_TOKEN, 'foo', END_TOKEN]
    assert tokenize('my name is luca') == [START_TOKEN, 'my', 'name', 'is', 'luca', END_TOKEN]

    with pytest.raises(ValueError):
        tokenize(START_TOKEN + ' foo')

    with pytest.raises(ValueError):
        tokenize(END_TOKEN + ' foo')


def test_create_ngram_model():
    mock_smoothing = mock.Mock(return_value=Decimal(0.3))
    MockCorpus = mock.Mock()
    prob_fn = ngram_model(2, mock_smoothing)

    prob = prob_fn(['a', 'b', 'c'], MockCorpus)

    assert  approx(prob, 0.3**2, 0.00001)
    assert mock_smoothing.call_args_list == [mock.call(('a', 'b'), MockCorpus), mock.call(('b', 'c'), MockCorpus)]
