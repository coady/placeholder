import itertools
import operator
from functools import partial

__version__ = '0.6'


def rpartial(func, other):
    return lambda self: func(self, other)


def methods(func):
    name = func.__name__.rstrip('_')
    return (lambda self, other: getattr(other, '__r{}__'.format(name), rpartial(func, other)),
            lambda self, other: getattr(other, '__{}__'.format(name), partial(func, other)))


def unary(func):
    return lambda self: func


class placeholder(object):
    """Singleton for creating partially bound functions."""
    __slots__ = ()
    __getattr__ = operator.attrgetter
    __getitem__ = operator.itemgetter
    __call__ = operator.methodcaller

    def __iter__(self):
        raise TypeError("'placeholder' object is not iterable")

    __neg__ = unary(operator.neg)
    __pos__ = unary(operator.pos)
    __invert__ = unary(operator.invert)

    __add__, __radd__ = methods(operator.add)
    __sub__, __rsub__ = methods(operator.sub)
    __mul__, __rmul__ = methods(operator.mul)
    __floordiv__, __rfloordiv__ = methods(operator.floordiv)
    __div__, __rdiv__ = __truediv__, __rtruediv__ = methods(operator.truediv)

    __mod__, __rmod__ = methods(operator.mod)
    __divmod__, __rdivmod__ = methods(divmod)
    __pow__, __rpow__ = methods(operator.pow)
    if hasattr(operator, 'matmul'):
        __matmul__, __rmatmul__ = methods(operator.matmul)

    __lshift__, __rlshift__ = methods(operator.lshift)
    __rshift__, __rrshift__ = methods(operator.rshift)

    __and__, __rand__ = methods(operator.and_)
    __xor__, __rxor__ = methods(operator.xor)
    __or__, __ror__ = methods(operator.or_)

    __lt__ = methods(operator.gt)[1]
    __le__ = methods(operator.ge)[1]
    __eq__ = methods(operator.eq)[1]
    __ne__ = methods(operator.ne)[1]
    __gt__ = methods(operator.lt)[1]
    __ge__ = methods(operator.le)[1]


__ = placeholder()


def pipe(funcs, value):
    for func in funcs:
        value = func(value)
    return value


def methods(func):
    return (lambda self, other: F(self, func(__, other)),
            lambda self, other: F(self, func(other, __)))


def unary(func):
    return lambda self: F(self, func)


class F(partial):
    """Singleton for creating composite functions."""
    __slots__ = ()
    __getattr__ = methods(getattr)[0]
    __getitem__ = methods(operator.getitem)[0]

    def __new__(cls, *funcs):
        funcs = tuple(itertools.chain.from_iterable(
            func if isinstance(func, cls) else [func] for func in funcs))
        return partial.__new__(cls, *(funcs if len(funcs) == 1 else (pipe, funcs)))

    def __iter__(self):
        return iter(self.args[0] if self.args else [self.func])

    __neg__ = unary(-__)
    __pos__ = unary(+__)
    __invert__ = unary(~__)

    __add__, __radd__ = methods(operator.add)
    __sub__, __rsub__ = methods(operator.sub)
    __mul__, __rmul__ = methods(operator.mul)
    __floordiv__, __rfloordiv__ = methods(operator.floordiv)
    __div__, __rdiv__ = __truediv__, __rtruediv__ = methods(operator.truediv)

    __mod__, __rmod__ = methods(operator.mod)
    __divmod__, __rdivmod__ = methods(divmod)
    __pow__, __rpow__ = methods(operator.pow)
    if hasattr(operator, 'matmul'):
        __matmul__, __rmatmul__ = methods(operator.matmul)

    __lshift__, __rlshift__ = methods(operator.lshift)
    __rshift__, __rrshift__ = methods(operator.rshift)

    __and__, __rand__ = methods(operator.and_)
    __xor__, __rxor__ = methods(operator.xor)
    __or__, __ror__ = methods(operator.or_)

    __lt__ = methods(operator.gt)[1]
    __le__ = methods(operator.ge)[1]
    __eq__ = methods(operator.eq)[1]
    __ne__ = methods(operator.ne)[1]
    __gt__ = methods(operator.lt)[1]
    __ge__ = methods(operator.le)[1]


_ = F()
