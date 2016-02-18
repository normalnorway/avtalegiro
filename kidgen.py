"""Generate KID from member number

KID layout: yyiiiiivvc

y = year (2)            [Must be fixed?]
i = member-no (5)       [Nets-Avtale: Kundenummer]
v = custom (2)          [Nets-Avtale: Betalingstype]
c = controll digit (1)

i: 00000 - 08999    donor no
   09000 - 99999    member no

v: 00 = medlemskontingent
   01 = donasjon
"""

MEMBER = 0
DONOR = 1

from mod10 import mod10

# @todo assert range of memberno & donorno)

def kid_member (memberno):
    return generate_kid (memberno, payment_type = MEMBER)

def kid_donor (donorno):
    return generate_kid (donorno, payment_type = DONOR)

# @todo make payment_type required? rename paytype?
def generate_kid (memberno, payment_type=DONOR, fixed=15):
    assert fixed == 15    # can't change without notifying Nets?
    assert 0 <= payment_type < 100
    if not isinstance (memberno, basestring):
        memberno = '%05d' % memberno
    assert len(memberno) == 5
    kidstr = '%02d%5s%02d' % (fixed, memberno, payment_type)
    return kidstr + str(mod10(kidstr))
