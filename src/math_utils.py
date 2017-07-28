import random


def approx(value, expected, delta=0.0001):
    return abs(value - expected) < delta


def log2(decimal_obj):
    from decimal import Decimal
    return decimal_obj.ln() / Decimal(2).ln()
    


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    target = random.uniform(0, total)
    upto = 0

    for c, w in choices:
        if upto + w >= target:
            return c
        upto += w

    assert False, "Should have found something by now"
