import itertools
import operator
from functools import partial

__version__ = '0.6'


def rmethod(name, op=None):
    op = getattr(operator, name, op)
    return lambda self, other: getattr(other, '__{}__'.format(name), partial(op, other))


def umethod(name):
    return lambda self: getattr(operator, name)


class placeholder(object):
    """Singleton for creating partially bound functions."""
    __slots__ = ()
    __getattr__ = operator.attrgetter
    __getitem__ = operator.itemgetter
    __call__ = operator.methodcaller

    def __iter__(self):
        raise TypeError("'placeholder' object is not iterable")

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
    def __matmul__(self, other):
        return getattr(other, '__rmatmul__', lambda left: operator.matmul(left, other))
    __rmatmul__ = rmethod('matmul')

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


def pipe(funcs, value):
    for func in funcs:
        value = func(value)
    return value


def method(func):
    return lambda self, other: F(self, func(__, other))


def rmethod(func):
    return lambda self, other: F(self, func(other, __))


def umethod(func):
    return lambda self: F(self, func(__))


class F(partial):
    """Singleton for creating composite functions."""
    __slots__ = ()

    def __new__(cls, *funcs):
        funcs = tuple(itertools.chain.from_iterable(
            func if isinstance(func, cls) else [func] for func in funcs))
        return partial.__new__(cls, *(funcs if len(funcs) == 1 else (pipe, funcs)))

    def __iter__(self):
        return itertools.chain({self.func} - {pipe}, *self.args)

    __neg__ = umethod(operator.neg)
    __pos__ = umethod(operator.pos)
    __invert__ = umethod(operator.invert)

    __getattr__ = method(getattr)
    __getitem__ = method(operator.getitem)

    __add__ = method(operator.add)
    __radd__ = rmethod(operator.add)
    __sub__ = method(operator.sub)
    __rsub__ = rmethod(operator.sub)

    __mul__ = method(operator.mul)
    __rmul__ = rmethod(operator.mul)
    __floordiv__ = method(operator.floordiv)
    __rfloordiv__ = rmethod(operator.floordiv)
    __div__ = __truediv__ = method(operator.truediv)
    __rdiv__ = __rtruediv__ = rmethod(operator.truediv)

    __mod__ = method(operator.mod)
    __rmod__ = rmethod(operator.mod)
    __divmod__ = method(divmod)
    __rdivmod__ = rmethod(divmod)
    __pow__ = method(operator.pow)
    __rpow__ = rmethod(operator.pow)
    if hasattr(operator, 'matmul'):
        __matmul__ = method(operator.matmul)
        __rmatmul__ = rmethod(operator.matmul)

    __lshift__ = method(operator.lshift)
    __rlshift__ = rmethod(operator.lshift)
    __rshift__ = method(operator.rshift)
    __rrshift__ = rmethod(operator.rshift)

    __and__ = method(operator.and_)
    __rand__ = rmethod(operator.and_)
    __xor__ = method(operator.xor)
    __rxor__ = rmethod(operator.xor)
    __or__ = method(operator.or_)
    __ror__ = rmethod(operator.or_)

    __lt__ = method(operator.lt)
    __le__ = method(operator.le)
    __eq__ = method(operator.eq)
    __ne__ = method(operator.ne)
    __gt__ = method(operator.gt)
    __ge__ = method(operator.ge)


_ = F(pipe)
___ = _  # deprecated
