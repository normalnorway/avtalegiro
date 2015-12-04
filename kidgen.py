"""Generate AvtaleGiro KID number for member

>>> from apps.member.models import Member
>>> random.sample ([obj.member_no() for obj in Member.objects.only('pk')], 10)

KID number: yyiiiiivvc

y = year (2)            [Must be fixed?]
i = member-no (5)       [Nets-Avtale: Kundenummer]
v = custom (2)          [Nets-Avtale: Betalingstype]
c = controll digit (1)

Send tests to testgruppen@bbs.no
"""

customer_no_list = [15548, 15590, 14339, 9118, 14250, 15424, 14289, 15374, 15638, 15506]

from mod10 import mod10

def generate_kid (customer_no, payment_type=1, fixed=15):
    assert fixed == 15    # can't change without notifying Nets?
    assert 0 <= payment_type < 100
    if not isinstance (customer_no, basestring):
        customer_no = '%05d' % customer_no
    assert len(customer_no) == 5
    kidstr = '%02d%5s%02d' % (fixed, customer_no, payment_type)
    return kidstr + str(mod10(kidstr))


for num in customer_no_list:
    print generate_kid (num)
