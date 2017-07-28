from src.evaluate_model import _split_data


def test_split_data_even_length():
    test_data = list(range(30))

    x, y = _split_data(test_data, frac=0.5)

    assert len(x) == len(y) == 15
    assert not set(x).intersection(y)

def test_split_data_odd_length():
    test_data = list(range(31))

    x, y = _split_data(test_data, frac=0.5)

    assert len(x),len(y) == (15, 16)
    assert not set(x).intersection(y)
