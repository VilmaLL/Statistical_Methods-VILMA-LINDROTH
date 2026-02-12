

def congruent(a: int, b: int, p: int) -> bool:
    if a % p == b:
        return True

def divisor(a: int, b: int) -> bool:
    if b % a == 0:
        return True
    
def prime(a) -> bool:
    if a < 2:
        return False
    for i in range(2, int(a**0.5) + 1):
        if a % i == 0:
            return False
    return True