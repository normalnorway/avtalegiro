import operator
from itertools import imap, cycle

__all__ = ['mod10']

#digit_sum = lambda n: sum (map(int,str(n)))

def digit_sum (n):
    return n if n<10 else digit_sum (sum(map(int, str(n))))

# mod10 algorithm:
# 1. Double every second digit from the right (and take digit sum if > 9)
# 2. Compute sum of digits
# 3. Multiply by nine
# 4. Last digit is the check digit

def mod10 (number):
    """Luhn algorithm aka modulus 10 aka mod10."""
    #assert isinstance (number, (int, long))    # drop to accept strings
    #digits = reversed ([int(n) for n in str(number)])
    digits = map (int, reversed (str(number)))
    lst = map (digit_sum, imap(operator.mul, digits, cycle((2,1))))  # 1
    return sum (lst)*9 % 10     # 2,3,4
