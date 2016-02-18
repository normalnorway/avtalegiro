import unittest
import operator
import random
from mod10 import mod10, digit_sum
from avtalegiro import Transmission
from avtalegiro import PaymentClaim, CancellationRequest


class AvtaleGiroTestCase (unittest.TestCase):
    def test_test1 (self):
        trans = Transmission (data_sender='11223344',
                              transmission_number='1234567')
        order = PaymentClaim (order_account = 15035149098,
                              order_number = 7654321)

        # Note: All orders/transactions inside a PaymentClaim must
        # be to the same customer!
        order.add (due='200516', amount=250*100, kid='00010001')
        order.add (due='270616', amount=300*100, kid='00010002',
                   abbreviated_name = 'Abbr. name',
                   external_reference = 'External reference',
                   specification = 'Hello\nLine two\n\nLast line')
        order.add (due='140316', amount=500*100, kid='00010003')

        cancellation = CancellationRequest (account=15035149098, number=7654321)
        cancellation.add ('200516', 250*100, '00010001')
        cancellation.add ('140316', 500*100, '00010003')

        trans.add (order)
        trans.add (cancellation)

        from io import BytesIO
        buf = BytesIO()
        trans.render (buf)
        #with open('fixture/test1','wb') as fp: fp.write (buf.getvalue())

        self.assertEqual (buf.getvalue(), open('fixture/test1').read())
        # @todo use debug renderer. then the diff is much nicer
        # @todo test multiple orders per transmission



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
