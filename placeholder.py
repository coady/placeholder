import itertools
import operator
import warnings
from functools import partial

__version__ = '0.7.1'


def rpartial(func, other):
    return lambda self: func(self, other)


def pipe(funcs, value):
    for func in funcs:
        value = func(value)
    return value


def methods(func):
    name = func.__name__.rstrip('_')

    def left(self, other):
        return type(self)(self, getattr(other, '__r{}__'.format(name), rpartial(func, other)))

    def right(self, other):
        return type(self)(self, getattr(other, '__{}__'.format(name), partial(func, other)))
    return left, right


def binary(func):
    return lambda self, arg: type(self)(self, func(arg))


def unary(func):
    return lambda self: type(self)(self, func)


class F(partial):
    """Singleton for creating composite functions."""
    __slots__ = ()

    def __new__(cls, *funcs):
        funcs = tuple(itertools.chain.from_iterable(
            func if isinstance(func, cls) else [func] for func in funcs))
        return partial.__new__(cls, *(funcs if len(funcs) == 1 else (pipe, funcs)))

    def __iter__(self):
        return iter(self.args[0] if self.args else [self.func])

    __getattr__ = binary(operator.attrgetter)
    __getitem__ = binary(operator.itemgetter)

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


class placeholder(F):
    def __new__(cls, *funcs):
        warnings.warn("Use `F.func` if necessary", DeprecationWarning)
        return F.__new__(cls, *funcs).func


_ = F()
__ = F.__new__(placeholder)
