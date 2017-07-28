

def approx(value, expected, delta=0.0001):
    return abs(value - expected) < delta


def log2(decimal_obj):
    from decimal import Decimal
    return decimal_obj.ln() / Decimal(2).ln()
    
