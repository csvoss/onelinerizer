import math

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    n = int(n)
    factors = range(2, int(math.ceil(math.sqrt(n))+1))
    i = 0
    while i < len(factors):
        factor = factors[i]
        if n % factor == 0:
            return False
        i = i + 1
    return True

def smallest_prime_larger_than(x):
    while True:
        x = x + 1
        if is_prime(x):
            return x

print is_prime(1)
print is_prime(2)
print is_prime(3)
print is_prime(4)
print is_prime(5)
print is_prime(45)
print is_prime(91)
print is_prime(89)

print smallest_prime_larger_than(1)
print smallest_prime_larger_than(91)
print smallest_prime_larger_than(1000)
