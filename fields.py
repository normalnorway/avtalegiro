# Note: Need both numeric and alpha numeric fillers. So filler=true is
# implemented internally as always='' (i.e., by adjusting and padding
# the empty string).

import datetime

class FieldBase (object):
    def __init__ (self, pos, always=None, key=None, filler=False, name=None):
        #assert sum (map(bool,(always,key,filler))) == 1  # mutually exclusive
        #assert any ((always, key))
        #assert not all ((always, key))
        if key is True:     # => use name as key
            key = name
            #key = name.replace(' ', '_').lower()
        self.pos = pos
        self.always = always
        self.key = key
        self.filler = filler
        self.name = name

    @property
    def length (self):
        return self.pos[1] - self.pos[0] + 1
        #return = 1 + -operator.sub (*self.pos)

    # Q: can handle filler by setting always=''?
    def get_value (self, data):
        if self.filler:
            return ''
        if self.always is not None:
            return self.always
        return data[self.key]
        #return data.get (self.key)

    def render (self, data=None):
        raise NotImplementedError()


class FieldAlpha (FieldBase):
    def render (self, data=None):   # Q: why defaults to None?
        value = str (self.get_value (data))
        return value.ljust (self.length)


class FieldNumeric (FieldBase):
    def render (self, data):
        value = self.get_value (data)
        if not self.filler:
            #assert isinstance (value, (int, long)) # use duck-typing instead?
            if isinstance (value, datetime.date):
                value = value.strftime('%d%m%y')
            elif isinstance (value, basestring):
                # update: was only used for kid
                assert all(c.isdigit() for c in value)
            else:
                assert isinstance (value, (int, long))
        return str(value).rjust (self.length, '0')


# KID is defined to be a Numeric field, but with spaces as padding.
class FieldKid (FieldBase):
    def render (self, data):
        value = self.get_value (data)
        assert all(c.isdigit() for c in str(value))
        return value.rjust (self.length)
