from fields import FieldAlpha, FieldNumeric, FieldKid
from copy import deepcopy


# 2.1 Start record transmission
REC_START_RECORD_TRANSMISSION = (
    None,
    FieldAlpha   (( 1, 2), always='NY',     name='FORMAT CODE'),
    FieldNumeric (( 3, 4), always=0,        name='SERVICE CODE'),
    FieldNumeric (( 5, 6), always=0,        name='TRANSMISSION TYPE'),
    FieldNumeric (( 7, 8), always=10,       name='RECORD TYPE'),
    FieldNumeric (( 9,16), key=True,        name='DATA SENDER'),
    FieldNumeric ((17,23), key=True,        name='TRANSMISSION NUMBER'),
    FieldNumeric ((24,31), always=8080,     name='DATA RECIPIENT'),
    FieldNumeric ((32,80), filler=True,     name='FILLER'),
)


# 2.2.1 Start record payment claim order
REC_START_PAYMENT_CLAIM = (
    None,
    FieldAlpha   (( 1, 2), always='NY',     name='FORMAT CODE'),
    FieldNumeric (( 3, 4), always=21,       name='SERVICE CODE'),
    FieldNumeric (( 5, 6), always=0,        name='ORDER TYPE'),
    FieldNumeric (( 7, 8), always=20,       name='RECORD TYPE'),
    FieldNumeric (( 9,17), filler=True,     name='FILLER'),
    FieldNumeric ((18,24), key=True,        name='ORDER NUMBER'),
    FieldNumeric ((25,35), key=True,        name='ORDER ACCOUNT'),
    FieldNumeric ((36,80), filler=True,     name='FILLER'),
)


# 2.2.2 Amount posting 1
REC_AMOUNT_POSTING_1 = (
    None,
    FieldAlpha   (( 1, 2), always='NY',     name='FORMAT CODE'),
    FieldNumeric (( 3, 4), always=21,       name='SERVICE CODE'),
    FieldNumeric (( 5, 6), key=True,        name='TRANSACTION TYPE'),
    FieldNumeric (( 7, 8), always=30,       name='RECORD TYPE'),
    FieldNumeric (( 9,15), key=True,        name='TRANSACTION NUMBER'),
    FieldNumeric ((16,21), key=True,        name='DUE DATE'),
    FieldNumeric ((22,32), filler=True,     name='FILLER'),
    FieldNumeric ((33,49), key=True,        name='AMOUNT'),
    # The KID should be right-justified, without special characters and any
    # vacant positions should be left blank. Letters cannot be used.
    #FieldNumeric ((50,74), key=True,        name='KID'),
    FieldKid     ((50,74), key=True,        name='KID'),
    FieldNumeric ((75,80), filler=True,     name='FILLER'),
)


# 2.2.3 Amount posting 2
REC_AMOUNT_POSTING_2 = (
    None,
    FieldAlpha   (( 1, 2), always='NY',     name='FORMAT CODE'),
    FieldNumeric (( 3, 4), always=21,       name='SERVICE CODE'),
    FieldNumeric (( 5, 6), key=True,        name='TRANSACTION TYPE'),
    FieldNumeric (( 7, 8), always=30,       name='RECORD TYPE'),
    FieldNumeric (( 9,15), key=True,        name='TRANSACTION NUMBER'),
    FieldAlpha   ((16,25), key=True,        name='ABBREVIATED NAME'),
    FieldAlpha   ((26,50), filler=True,     name='FILLER'),
    FieldAlpha   ((51,75), key=True,        name='EXTERNAL REFERENCE'),
    FieldNumeric ((76,80), filler=True,     name='FILLER'),
)


# 2.2.4 Specification record
REC_SPECIFICATION_RECORD = (
    None,
    FieldAlpha   (( 1, 2), always='NY',     name='FORMAT CODE'),
    FieldNumeric (( 3, 4), always=21,       name='SERVICE CODE'),
    FieldNumeric (( 5, 6), always=21,       name='TRANSACTION TYPE'),
    FieldNumeric (( 7, 8), always=49,       name='RECORD TYPE'),
    FieldNumeric (( 9,15), key=True,        name='TRANSACTION NUMBER'),
    FieldNumeric ((16,16), always=4,        name='PAYMENT NOTIFICATION'),

    FieldNumeric ((17,19), key=True,        name='PLACEMENT/LINE'),
    FieldNumeric ((20,20), key=True,        name='POSITION/COLUMN'),
    FieldAlpha   ((21,60), key=True,        name='MESSAGE SPECIFICATION'),
    FieldNumeric ((61,80), filler=True,     name='FILLER'),
)


# 2.2.5 End record payment claim order
REC_END_PAYMENT_CLAIM = (
    None,
    FieldAlpha   (( 1, 2), always='NY',     name='FORMAT CODE'),
    FieldNumeric (( 3, 4), always=21,       name='SERVICE CODE'),
    FieldNumeric (( 5, 6), always=0,        name='ORDER TYPE'),
    FieldNumeric (( 7, 8), always=88,       name='RECORD TYPE'),
    FieldNumeric (( 9,16), key=True,        name='NUMBER OF TRANSACTIONS'),
    FieldNumeric ((17,24), key=True,        name='NUMBER OF RECORDS'),
    FieldNumeric ((25,41), key=True,        name='TOTAL AMOUNT'),
    FieldNumeric ((42,47), key=True,        name='FIRST DUE DATE'),
    FieldNumeric ((48,53), key=True,        name='LAST DUE DATE'),
    FieldNumeric ((54,80), filler=True,     name='FILLER'),
)


# 2.3.1 Start record cancellation request order
REC_START_RECORD_CANCELLATION_REQUEST = deepcopy (REC_START_PAYMENT_CLAIM)
REC_START_RECORD_CANCELLATION_REQUEST[3].always = 36


# 2.3.3 Cancellation posting 1
REC_CANCELLATION_POSTING_1 = deepcopy (REC_AMOUNT_POSTING_1)
REC_CANCELLATION_POSTING_1[3].always = 93


# 2.3.4 Cancellation posting 2
# Note: This is never used
REC_CANCELLATION_POSTING_2 = deepcopy (REC_AMOUNT_POSTING_2)
REC_CANCELLATION_POSTING_2[3].always = 93


# 2.3.5 End record cancellation request order
REC_END_RECORD_CANCELLATION_REQUEST = deepcopy (REC_END_PAYMENT_CLAIM)
REC_END_RECORD_CANCELLATION_REQUEST[3].always = 36


# 2.4 End record transmission
REC_END_RECORD_TRANSMISSION = (
    None,
    FieldAlpha   (( 1, 2), always='NY', name='FORMAT CODE'),
    FieldNumeric (( 3, 4), always=0,    name='SERVICE CODE'),
    FieldNumeric (( 5, 6), always=0,    name='TRANSMISSION TYPE'),
    FieldNumeric (( 7, 8), always=89,   name='RECORD TYPE'),
    FieldNumeric (( 9,16), key=True,    name='NUMBER OF TRANSACTIONS'),
    FieldNumeric ((17,24), key=True,    name='NUMBER OF RECORDS'),
    FieldNumeric ((25,41), key=True,    name='TOTAL AMOUNT'),
    FieldNumeric ((42,47), key=True,    name='FIRST DATE'),
    FieldNumeric ((48,80), filler=True, name='FILLER'),
)


#__all__ = [key for key in globals() if key.startswith('REC_')]
