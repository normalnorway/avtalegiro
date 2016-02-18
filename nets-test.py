# Send tests to payment-test-no@nets.eu
import sys
from avtalegiro import Transmission
from avtalegiro import PaymentClaim, CancellationRequest

import argparse
parser = argparse.ArgumentParser()
parser.add_argument ('--sender', required=True)
parser.add_argument ('--account', required=True)
parser.add_argument ('--trans-no', required=True)   # TRANSMISSION NUMBER
args = parser.parse_args()

# Note: Must be unique per year + one day.
#def make_order_number_generator (value=0):
#    while True:
#        yield value
#        value += 1
#        if value >= 1e8:
#            raise RuntimeError ('order number to large. max 7 digits.')

#next_order_number = make_order_number_generator (1).next
from ordernumber import next_order_number

from datetime import date, timedelta
#from kidgen import generate_kid     # kidgen.member(), kidgen.donor()
import kidgen

trans = Transmission (data_sender=args.sender, transmission_number=args.trans_no)

o1 = PaymentClaim (args.account, next_order_number())
#o1.add (date.today()+timedelta(days=14), 250*100, kidgen.donor (123,1))
o1.add (date.today()+timedelta(days=14), 250*100, kidgen.donor (123),
        abbreviated_name = 'Abbr. name',
        external_reference = 'External reference',
        specification = 'This is the specification line')

# @todo test multiple claims per order
# But note: Et oppdrag kan kun inneholde transaksjoner for 1 oppdragstype
# som gjelder 1 avtale.
#o1.add (date.today()+timedelta(days=20), 100*100, kidgen.member (123,0))

o2 = PaymentClaim (args.account, next_order_number())
o2.add (date.today()+timedelta(days=30), 500*100, kidgen.donor (321))

# Q: Must use same order number as the payment-claim we are canceling?
#c1 = CancellationRequest (args.account, next_order_number())
#c1.add (date.today()+timedelta(days=14), 250*100, kidgen.donor (123))
c1 = CancellationRequest (args.account, o1.order_number)
rec = o1.transactions[0]
c1.add (rec.due, rec.amount, rec.kid)

trans.add (o1)
trans.add (o2)
trans.add (c1)
trans.render (sys.stdout)

# @todo store transmission on permantent storage


# Q: If one order (PaymentClaim) have multiple claims. Is it possible
#    to cancel just one of them?


#o1 = PaymentClaim (order_account = args.account,
#                   order_number  = next_order_number())
#o1.add (due = date.today()+timedelta(days=14), amount = 250*100, kid=generate_kid (123))
