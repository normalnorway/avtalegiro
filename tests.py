# Stolen from Wikipedia. This is the canonical version.
def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def calculate_luhn(partial_card_number):
    check_digit = luhn_checksum(int(partial_card_number) * 10)
    return check_digit if check_digit == 0 else 10 - check_digit


from mod10 import mod10
import operator
import random

def random_number (max_digits=20):
    """Returns random number between 1 and max_digits. All digit lengths
    have equal probability."""
    digits = str (random.randrange(10**max_digits, 10**(max_digits+1)))
    return long (digits[:random.randint(1,max_digits)])

NUM_TESTS = 100

lst = [random_number() for nil in xrange(NUM_TESTS)]

assert all (map (operator.eq, map(calculate_luhn, lst), map(mod10, lst)))

#for nil in xrange (NUM_TESTS):
#    num = random_number()
#    assert calculate_luhn (num) == mod10 (num)
