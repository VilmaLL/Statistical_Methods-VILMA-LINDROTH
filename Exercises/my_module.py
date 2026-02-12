import my_modulo_module as m

def test_congruence():
    a = m.congruent(5, 2, 3)
    b = not m.congruent(1, 4, 2)
    return a and b

def test_divisor():
    a = m.divisor(2, 12)
    b = not m.divisor(5, 7)
    return a and b

def test_prime():
    a = m.prime(37)
    b = not m.prime(8)
    return a and b

if __name__ == "__main__":
    print(f"Congruence a, b: {test_congruence()} \nDivisor a, b: {test_divisor()} \nPrime a, b: {test_prime()}")