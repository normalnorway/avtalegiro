import unittest
import operator
import random
from mod10 import mod10, digit_sum


# Stolen from Wikipedia.
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



class MyTestCase (unittest.TestCase):
    NUM_TESTS = 100

    @classmethod
    def rand (klass, max_digits=20):
        """Returns random number between 1 and max_digits. All digit lengths
        have equal probability."""
        digits = str (random.randrange(10**max_digits, 10**(max_digits+1)))
        return long (digits[:random.randint(1,max_digits)])

    def test_mod10 (self):
        lst = [self.rand() for nil in xrange(self.NUM_TESTS)]
        self.assertListEqual (map(calculate_luhn, lst), map(mod10, lst))

    def test_digit_sum (self):
        self.assertEqual (digit_sum (18), 9)
        self.assertEqual (digit_sum (16), 7)
        self.assertEqual (digit_sum (7992739871), 8)
        self.assertEqual (digit_sum (111111111123), 6)
        self.assertEqual (digit_sum (11111111111111111111), 2)


if __name__ == '__main__':
    unittest.main()
