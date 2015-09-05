import operator
import itertools
from functools import partial

__version__ = '0.5'


class placeholder(object):
    "Create partially bound function."
    __slots__ = ()
    __getattribute__ = operator.attrgetter
    __getitem__ = operator.itemgetter
    __call__ = operator.methodcaller

    def __iter__(self):
        raise TypeError("'placeholder' object is not iterable")
    def __contains__(self, item):
        raise TypeError("argument of type 'placeholder' is not iterable")

    def __neg__(self):
        return operator.neg
    def __pos__(self):
        return operator.pos
    def __invert__(self):
        return operator.invert

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
    def __floordiv__(self, other):
        return getattr(other, '__rfloordiv__', lambda left: left // other)
    def __rfloordiv__(self, other):
        return getattr(other, '__floordiv__', partial(operator.floordiv, other))
    def __truediv__(self, other):
        return getattr(other, '__rtruediv__', lambda left: left / other)
    def __rtruediv__(self, other):
        return getattr(other, '__truediv__', partial(operator.truediv, other))
    __div__, __rdiv__ = __truediv__, __rtruediv__

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


class F(object):
    "Create composite function."
    __slots__ = ()
    def __new__(cls, func):
        method = staticmethod(func if cls is F else lambda arg: func(cls.__call__(arg)))
        return object.__new__(type('F', (F,), {'__slots__': (), '__call__': method}))

    def __neg__(self):
        return type(self)(-__)
    def __pos__(self):
        return type(self)(+__)
    def __invert__(self):
        return type(self)(~__)

    def __getattribute__(self, name):
        return type(self)(getattr(__, name))
    def __getitem__(self, keys):
        return type(self)(__[keys])

    def __add__(self, other):
        return type(self)(__ + other)
    def __radd__(self, other):
        return type(self)(other + __)
    def __sub__(self, other):
        return type(self)(__ - other)
    def __rsub__(self, other):
        return type(self)(other - __)

    def __mul__(self, other):
        return type(self)(__ * other)
    def __rmul__(self, other):
        return type(self)(other * __)
    def __floordiv__(self, other):
        return type(self)(__ // other)
    def __rfloordiv__(self, other):
        return type(self)(other // __)
    def __truediv__(self, other):
        return type(self)(__ / other)
    def __rtruediv__(self, other):
        return type(self)(other / __)
    __div__, __rdiv__ = __truediv__, __rtruediv__

    def __mod__(self, other):
        return type(self)(__ % other)
    def __rmod__(self, other):
        return type(self)(other % __)
    def __divmod__(self, other):
        return type(self)(divmod(__, other))
    def __rdivmod__(self, other):
        return type(self)(divmod(other, __))
    def __pow__(self, other):
        return type(self)(__ ** other)
    def __rpow__(self, other):
        return type(self)(other ** __)

    def __lshift__(self, other):
        return type(self)(__ << other)
    def __rlshift__(self, other):
        return type(self)(other << __)
    def __rshift__(self, other):
        return type(self)(__ >> other)
    def __rrshift__(self, other):
        return type(self)(other >> __)

    def __and__(self, other):
        return type(self)(__ & other)
    def __rand__(self, other):
        return type(self)(other & __)
    def __xor__(self, other):
        return type(self)(__ ^ other)
    def __rxor__(self, other):
        return type(self)(other ^ __)
    def __or__(self, other):
        return type(self)(__ | other)
    def __ror__(self, other):
        return type(self)(other | __)

    def __lt__(self, other):
        return type(self)(__ < other)
    def __le__(self, other):
        return type(self)(__ <= other)
    def __eq__(self, other):
        return type(self)(__ == other)
    def __ne__(self, other):
        return type(self)(__ != other)
    def __gt__(self, other):
        return type(self)(__ > other)
    def __ge__(self, other):
        return type(self)(__ >= other)

___ = object.__new__(F)
composer = F  # deprecated
