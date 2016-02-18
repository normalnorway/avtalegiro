r"""
ORDER NUMBER: Numerical, 7 positions.

Unique numbering must be used for orders per payee's recipient agreement,
12 months + one day ahead.

An atomic incrementing counter is used, modulu 1e8. A check is done to
assert that order number is not reused in the last 12 months + 1 day.
@todo implement that check!
"""

# @todo new name. does more than generate order numbers

# Only store one row with one column
#SQL_TABLE1 = 'CREATE TABLE order_number (next BIGINT)'
# one row per order_number? use auto increment primary key?

import sqlite3

conn = sqlite3.connect ('transmissions.db')
cursor = conn.cursor()

def _init_db():
    cursor.execute ('create table keyval (key TEXT, val BIGINT)')
    cursor.execute ('insert into keyval values (?,?)', ('order_number', 1))


def next_order_number():
    """Note: Will wrap around after 10 million numbers are generated"""
    oldlevel = conn.isolation_level
    try:
        conn.isolation_level = 'EXCLUSIVE'
        params = ('order_number',)
        cursor.execute ('select val from keyval where key=?', params)
        number = cursor.fetchone()[0]
        cursor.execute ('update keyval set val=val+1 where key=?', params)
        conn.commit()
    except sqlite3.OperationalError as ex:
        conn.rollback()    # needed? done by default?
        if ex.message != 'no such table: keyval': raise ex
        _init_db()
        return next_order_number()
    finally:
        conn.isolation_level = oldlevel
    return number % int(1e8)
