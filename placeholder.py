import operator
from functools import partial

__version__ = '0.5'


def rmethod(name, op=None):
    op = getattr(operator, name, op)
    return lambda self, other: getattr(other, '__{}__'.format(name), partial(op, other))


def umethod(name):
    return lambda self: getattr(operator, name)


class placeholder(object):
    """Singleton for creating partially bound functions."""
    __slots__ = ()
    __getattribute__ = operator.attrgetter
    __getitem__ = operator.itemgetter
    __call__ = operator.methodcaller

    def __iter__(self):
        raise TypeError("'placeholder' object is not iterable")
    def __contains__(self, item):
        raise TypeError("argument of type 'placeholder' is not iterable")

    __neg__ = umethod('neg')
    __pos__ = umethod('pos')
    __invert__ = umethod('invert')

    def __add__(self, other):
        return getattr(other, '__radd__', lambda left: left + other)
    __radd__ = rmethod('add')
    def __sub__(self, other):
        return getattr(other, '__rsub__', lambda left: left - other)
    __rsub__ = rmethod('sub')

    def __mul__(self, other):
        return getattr(other, '__rmul__', lambda left: left * other)
    __rmul__ = rmethod('mul')
    def __floordiv__(self, other):
        return getattr(other, '__rfloordiv__', lambda left: left // other)
    __rfloordiv__ = rmethod('floordiv')
    def __truediv__(self, other):
        return getattr(other, '__rtruediv__', lambda left: left / other)
    __rtruediv__ = rmethod('truediv')
    __div__, __rdiv__ = __truediv__, __rtruediv__

    def __mod__(self, other):
        return getattr(other, '__rmod__', lambda left: left % other)
    __rmod__ = rmethod('mod')
    def __divmod__(self, other):
        return getattr(other, '__rdivmod__', lambda left: divmod(left, other))
    __rdivmod__ = rmethod('divmod', divmod)
    def __pow__(self, other):
        return getattr(other, '__rpow__', lambda left: left ** other)
    __rpow__ = rmethod('pow')

    def __lshift__(self, other):
        return getattr(other, '__rlshift__', lambda left: left << other)
    __rlshift__ = rmethod('lshift')
    def __rshift__(self, other):
        return getattr(other, '__rrshift__', lambda left: left >> other)
    __rrshift__ = rmethod('rshift')

    def __and__(self, other):
        return getattr(other, '__rand__', lambda left: left & other)
    __rand__ = rmethod('and', operator.and_)
    def __xor__(self, other):
        return getattr(other, '__rxor__', lambda left: left ^ other)
    __rxor__ = rmethod('xor')
    def __or__(self, other):
        return getattr(other, '__ror__', lambda left: left | other)
    __ror__ = rmethod('or', operator.or_)

    __lt__ = rmethod('gt')
    __le__ = rmethod('ge')
    __eq__ = rmethod('eq')
    __ne__ = rmethod('ne')
    __gt__ = rmethod('lt')
    __ge__ = rmethod('le')


__ = placeholder()


class F(object):
    """Singleton for creating composite functions."""
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
