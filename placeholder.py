"""
A placeholder object uses operator overloading to create partially bound
functions on-the-fly.  When used in a binary expression, it will return a
callable object with the other argument bound.  It's useful for replacing
lambda when doing functional programming.  For example:

    __[key]     ==   operator.itemgetter(key)
    __.name     ==   operator.attrgetter('name')
    (1 + __)    ==   (1).__add__ or partial(operator.add, 1)
    (__ - 1)    ==   (1).__rsub__ or lambda obj: obj - 1

where '__' is a placeholder instance (it can have any name of course).

See tests for more example usage.
"""

import operator
from functools import partial

class placeholder(object):
    __slots__ = ()

    def __getattribute__(self, name):
        return operator.attrgetter(name)
    def __getitem__(self, keys):
        if not isinstance(keys, tuple):
            keys = keys,
        return operator.itemgetter(*keys)

    def __add__(self, other):
        return getattr(other, '__radd__', lambda left: left + other)
    def __radd__(self, other):
        return getattr(other, '__add__', partial(operator.add, other))
    def __sub__(self, other):
        return getattr(other, '__rsub__', lambda left: left - other)
    def __rsub__(self, other):
        return getattr(other, '__sub__', partial(operator.sub, other))
    def __mul__(self, other):
        return getattr(other, '__rmul__', lambda left: left * other)
    def __rmul__(self, other):
        return getattr(other, '__mul__', partial(operator.mul, other))
    def __div__(self, other):
        return getattr(other, '__rdiv__', lambda left: left / other)
    def __rdiv__(self, other):
        return getattr(other, '__div__', partial(operator.div, other))
    def __floordiv__(self, other):
        return getattr(other, '__rfloordiv__', lambda left: left // other)
    def __rfloordiv__(self, other):
        return getattr(other, '__floordiv__', partial(operator.floordiv, other))
    def __truediv__(self, other):
        return getattr(other, '__rtruediv__', lambda left: left / other)
    def __rtruediv__(self, other):
        return getattr(other, '__truediv__', partial(operator.truediv, other))
    def __mod__(self, other):
        return getattr(other, '__rmod__', lambda left: left % other)
    def __rmod__(self, other):
        return getattr(other, '__mod__', partial(operator.mod, other))
    def __divmod__(self, other):
        return getattr(other, '__rdivmod__', lambda left: divmod(left, other))
    def __rdivmod__(self, other):
        return getattr(other, '__divmod__', partial(divmod, other))
    def __pow__(self, other):
        return getattr(other, '__rpow__', lambda left: left ** other)
    def __rpow__(self, other):
        return getattr(other, '__pow__', partial(operator.pow, other))

    def __lshift__(self, other):
        return getattr(other, '__rlshift__', lambda left: left << other)
    def __rlshift__(self, other):
        return getattr(other, '__lshift__', partial(operator.lshift, other))
    def __rshift__(self, other):
        return getattr(other, '__rrshift__', lambda left: left >> other)
    def __rrshift__(self, other):
        return getattr(other, '__rshift__', partial(operator.rshift, other))
    def __and__(self, other):
        return getattr(other, '__rand__', lambda left: left & other)
    def __rand__(self, other):
        return getattr(other, '__and__', partial(operator.and_, other))
    def __xor__(self, other):
        return getattr(other, '__rxor__', lambda left: left ^ other)
    def __rxor__(self, other):
        return getattr(other, '__xor__', partial(operator.xor, other))
    def __or__(self, other):
        return getattr(other, '__ror__', lambda left: left | other)
    def __ror__(self, other):
        return getattr(other, '__or__', partial(operator.or_, other))

    def __lt__(self, other):
        return getattr(other, '__gt__', partial(operator.gt, other))
    def __le__(self, other):
        return getattr(other, '__ge__', partial(operator.ge, other))
    def __eq__(self, other):
        return getattr(other, '__eq__', partial(operator.eq, other))
    def __ne__(self, other):
        return getattr(other, '__ne__', partial(operator.ne, other))
    def __gt__(self, other):
        return getattr(other, '__lt__', partial(operator.lt, other))
    def __ge__(self, other):
        return getattr(other, '__le__', partial(operator.le, other))

__ = placeholder()
