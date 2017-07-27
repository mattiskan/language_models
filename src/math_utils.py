from decimal import Decimal

def approx(value, expected, delta=0.0001):
    return (value - Decimal(expected)).copy_abs() < delta


def log2(decimal_obj):
    return decimal_obj.ln() / Decimal(2).ln()
    
