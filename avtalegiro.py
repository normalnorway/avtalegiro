import datetime
import itertools
from collections import namedtuple
from recorddef import *

ENCODING = 'iso-8859-1'     # welcome to the pre-unicode era

# rename _OrderTrans? (only used internally)
OrderTransaction = namedtuple ('OrderTransaction',
        ('due', 'amount', 'kid', 'name', 'ref', 'spec'))


_CancelTrans = namedtuple ('_CancelTrans', ('due', 'amount', 'kid'))


def render_record (rec_def, fp, data):
    for field in rec_def[1:]:
        fp.write (field.render (data))

def render_record_dbg (rec_def, fp, data):
    #from pprint import pprint
    #pprint (data)
    #return
    # @todo write record name
    for field in rec_def[1:]:
        print field.name
        print field.render (data)
#render_record = render_record_dbg


# rename: clean_string
def _to_string (s, maxlen):
    if s is None: return ''
    assert isinstance (s, basestring)
    if isinstance (s, unicode):
        s = s.encode (ENCODING)
    assert len(s) <= maxlen
    return s


from textwrap import TextWrapper
def line_iterator (text, max_width=80): # _line_iterator
    """Split text in lines of max_width length and iterate over them"""
    wrapper = TextWrapper (width=max_width)
    for line in text.splitlines():
        if len(line) <= max_width:
            yield line
        else:
            for l in wrapper.wrap (line):
                yield l


SpecRecord = namedtuple ('SpecRecord', ('line', 'column', 'text'))
def _specification_record_iterator (text):  # _generator?
    """Prepeare textual data for Avtalegiro's 2.2.4 Specification record.
    Every specification line is divided in two parts of 40 characters each.
    To position the specifications correctly, the payee must state which
    column and which line each specification record belongs to.
    Note: Empty specification records must not be transferred.
    Yields namedtuple of (line-number, column-number, text)
    """
    line_it = itertools.count(1)
    for line in line_iterator (text, max_width=80):
        lineno = line_it.next()
        if line.strip() == '':
            continue
        if len(line) <= 40:
            yield SpecRecord (lineno, 1, line)
        else:
            if line[0:40].strip() != '':
                yield SpecRecord (lineno, 1, line[0:40])
            yield SpecRecord (lineno, 2, line[40:])



class Transmission (object):
    def __init__ (self, data_sender, transmission_number):
        self.data_sender = data_sender
        self.transmission_number = transmission_number
        self.orders = []

    def add (self, obj):    # obj is PaymentClaim or CancellationRequest
        self.orders.append (obj)

    # add helper for add_order & add_cancellation?

    def render (self, fp):
        render_record (REC_START_RECORD_TRANSMISSION, fp, {
            'DATA SENDER': self.data_sender,
            'TRANSMISSION NUMBER': self.transmission_number,
        })

        rec_cnt = 0
        amount = 0
        first_date = datetime.date.max
        for order in self.orders:
            order.render (fp)   # xxx must pass trans_no_base
            rec_cnt += order.num_records
            amount += sum(t.amount for t in order.transactions)
            due = min(t.due for t in order.transactions)
            if due < first_date: first_date = due
        # update: don't need separate list, can use polymorphism
        # update: might be better with separate list if due date and amount
        #         from cancellations should be skipped
#        for item in self.cancelations:
#            item.render (fp)

        render_record (REC_END_RECORD_TRANSMISSION, fp, {
            #'NUMBER OF TRANSACTIONS': len(self.orders) + len(self.cancelations),
            'NUMBER OF TRANSACTIONS': len(self.orders),
            'NUMBER OF RECORDS': rec_cnt + 2,  # include start & end record
            'TOTAL AMOUNT': amount,
            'FIRST DATE': first_date,
        })



# Note: All PaymentClaim must be to the same customer! To make claims
# to multiple customers, you must put multiple PaymentClaim inside
# the same transaction.
class PaymentClaim (object):
    """Payment Claim Order"""
    def __init__ (self, order_account, order_number):
        assert len(str(order_account)) == 11
        assert all(c.isdigit() for c in str(order_account))
        assert int(order_number)
        assert order_number < 1e7
        self.order_account = order_account
        self.order_number = order_number
        self.transactions = []
        self.transno = 1
        self.num_records = 0

    def add (self, due, amount, kid, abbreviated_name=None,
             external_reference=None, specification=None):
        """Add one order line (amount posting 1&2 + specification record)"""
        # Add transaction (payment claim + specification)

        # Convert and validate: due
        if not isinstance (due, datetime.date):
            due = datetime.datetime.strptime (due, '%d%m%y').date()
        assert due > datetime.date.today()     # allow today?

        # Convert and validate: amount
        amount = long(amount)
        assert amount < 1e17

        # Validate: kid
        assert isinstance (kid, basestring)
        assert len(kid) <= 25
        assert all(ch.isdigit() for ch in kid)

        abbreviated_name = _to_string (abbreviated_name, 10)
        external_reference = _to_string (external_reference, 25)
        specification = _to_string (specification, 42*80)

#        trans = OrderTransaction (due, amount, kid,
#                    _to_string (abbreviated_name, 10),
#                    _to_string (external_reference, 25),
#                    _to_string (specification, 42*80))

        self.transactions.append (OrderTransaction (
            due, amount, kid, abbreviated_name,
            external_reference, specification))

    def render (self, fp):
        """
        Renders one complete payment claim order:
        Start record payment claim order    {1}
          ----------------------------------------------+
          Amount posting 1                  {1}         |
          Amount posting 2                  {1}         |-- [1-N]
          Specification record              [0-84]      |
          ----------------------------------------------+
        End record payment claim order      {1}
        """
        render_record (REC_START_PAYMENT_CLAIM, fp, {
            'ORDER NUMBER': self.order_number,
            'ORDER ACCOUNT': self.order_account,
        })

        for data in self.transactions:
            self._render_transaction (fp, data)
            self.transno += 1

        render_record (REC_END_PAYMENT_CLAIM, fp, {
            'NUMBER OF TRANSACTIONS': len(self.transactions),
            'NUMBER OF RECORDS': self.num_records,
            'TOTAL AMOUNT': sum(t.amount for t in self.transactions),
            'FIRST DUE DATE': min(t.due for t in self.transactions),
            'LAST DUE DATE': max(t.due for t in self.transactions),
        })
        self.num_records += 2


    def _render_transaction (self, fp, trans):
        render_record (REC_AMOUNT_POSTING_1, fp, {
            'TRANSACTION TYPE': '21',   # hardcoded (AvtalGiro info)
            'TRANSACTION NUMBER': self.transno,
            'DUE DATE': trans.due,
            'AMOUNT': trans.amount,
            'KID': trans.kid,
        })
        render_record (REC_AMOUNT_POSTING_2, fp, {
            'TRANSACTION TYPE': '21',   # hardcoded (AvtalGiro info)
            'TRANSACTION NUMBER': self.transno,
            'ABBREVIATED NAME': trans.name,
            'EXTERNAL REFERENCE': trans.ref,
            'KID': trans.kid,
        })
        self.num_records += 2
        if not trans.spec: return  # @todo not needed

        for item in _specification_record_iterator (trans.spec):
            self.num_records += 1
            render_record (REC_SPECIFICATION_RECORD, fp, {
                'TRANSACTION NUMBER': self.transno,
                'PLACEMENT/LINE': item.line,
                'POSITION/COLUMN': item.column,
                'MESSAGE SPECIFICATION': item.text,
            })



# @todo share code with PaymentClaim
class CancellationRequest (object):
    def __init__ (self, account, number):
        self.account = account
        self.number = number
        self.transactions = []

    def add (self, due, amount, kid):
        if not isinstance (due, datetime.date):
            due = datetime.datetime.strptime (due, '%d%m%y').date()
        assert due >= datetime.date.today()

        amount = long(amount)
        assert amount < 1e17

        assert isinstance (kid, basestring)
        assert len(kid) <= 25
        assert all(ch.isdigit() for ch in kid)

        self.transactions.append (_CancelTrans (due, amount, kid))


    def render (self, fp):
        render_record (REC_START_RECORD_CANCELLATION_REQUEST, fp, {
            'ORDER ACCOUNT': self.account,
            'ORDER NUMBER':  self.number,
        })

        for trans in self.transactions:
            render_record (REC_CANCELLATION_POSTING_1, fp, {
                'TRANSACTION TYPE': '21',
                'TRANSACTION NUMBER': 666,  # @todo get from Transmission
                'DUE DATE': trans.due,
                'AMOUNT': trans.amount,
                'KID': trans.kid,
            })

        render_record (REC_END_RECORD_CANCELLATION_REQUEST, fp, {
            'NUMBER OF TRANSACTIONS': len (self.transactions),
            'NUMBER OF RECORDS':      len (self.transactions) + 2,  # start + end + one record per transaction
            'TOTAL AMOUNT':   sum (t.amount for t in self.transactions),
            'FIRST DUE DATE': min (t.due for t in self.transactions),
            'LAST DUE DATE':  max (t.due for t in self.transactions),
        })

        # Pass back to Transmission
        self.num_records = 2 + len (self.transactions)


        # Transaction numbers within an order featuring cancellations
        # should be unique and in ascending sequence. In the case of
        # a cancellation request, amount posting 1, 2, if relevant, and
        # the specification records have the same transaction number.

        # There is no requirement for the transaction number to be the
        # same as for the original transaction.
