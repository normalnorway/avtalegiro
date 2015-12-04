import operator
from itertools import imap, cycle

__all__ = ['mod10']

#digit_sum = lambda n: sum (map(int,str(n)))

def digit_sum (n):
    return n if n<10 else digit_sum (sum(map(int, str(n))))

def mod10 (number):
    """Luhn algorithm aka modulus 10 aka mod10."""
    # 1. Double every second digit from the right (and take digit sum if > 9)
    # 2. Compute sum of digits
    # 3. Multiply by nine
    # 4. Last digit is the check digit
    #assert isinstance (number, (int, long))    # drop to accept strings
    digits = reversed ([int(n) for n in str(number)])
    lst = map (digit_sum, imap (operator.mul, digits, cycle((2,1))))  # 1
    return sum (lst)*9 % 10     # 2,3,4


if __name__ == '__main__':
    print 'Running tests ...',
    assert digit_sum (18) == 9
    assert digit_sum (16) == 7
    assert digit_sum (7992739871) == 8
    assert digit_sum (111111111123) == 6
    assert digit_sum (11111111111111111111) == 2
    assert mod10 (7992739871) == 3
    assert mod10 (402400719617664) == 7
    assert mod10 (453991220275900) == 5
    assert mod10 (455638083309692) == 4
    assert mod10 (546762652538468) == 8
    assert mod10 (525377587033719) == 3
    assert mod10 (523524140354689) == 4
    print 'passed'
