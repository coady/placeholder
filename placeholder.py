import itertools
import math
import operator
from functools import partial, update_wrapper

__version__ = '1.1'


def rpartial(func, other):
    return lambda self: func(self, other)


def pipe(funcs, *args, **kwargs):
    value = funcs[0](*args, **kwargs)
    for func in funcs[1:]:
        value = func(value)
    return value


def methods(func):
    name = func.__name__.rstrip('_')

    def left(self, other):
        if isinstance(other, F):
            return type(self)(self, func)
        return type(self)(self, getattr(other, '__r{}__'.format(name), rpartial(func, other)))

    def right(self, other):
        return type(self)(self, getattr(other, '__{}__'.format(name), partial(func, other)))

    return update_wrapper(left, func), update_wrapper(right, func)


def unary(func):
    return update_wrapper(lambda self: type(self)(self, func), func)


class F(partial):
    """Singleton for creating composite functions."""

    def __new__(cls, *funcs):
        funcs = (func if isinstance(func, cls) else [func] for func in funcs)
        funcs = tuple(itertools.chain(*funcs))
        return partial.__new__(cls, *(funcs if len(funcs) == 1 else (pipe, funcs)))

    def __iter__(self):
        return iter(self.args[0] if self.args else [self.func])

    def __getattr__(self, attr):
        return type(self)(self, operator.attrgetter(attr))

    def __getitem__(self, item):
        return type(self)(self, operator.itemgetter(item))

    def __round__(self, ndigits=None):
        return type(self)(self, round if ndigits is None else partial(round, ndigits=ndigits))

    __neg__ = unary(operator.neg)
    __pos__ = unary(operator.pos)
    __invert__ = unary(operator.invert)

    __abs__ = unary(abs)
    __reversed__ = unary(reversed)

    __trunc__ = unary(math.trunc)
    __floor__ = unary(math.floor)
    __ceil__ = unary(math.ceil)

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


class M(object):
    """Singleton for creating method callers and multi-valued getters."""

    def __getattr__(cls, name):
        """Return a `methodcaller` constructor."""
        return F(partial(operator.methodcaller, name), F)

    def __call__(self, *names):
        """Return a tupled `attrgetter`."""
        return F(operator.attrgetter(*names))

    def __getitem__(self, keys):
        """Return a tupled `itemgetter`."""
        return F(operator.itemgetter(*keys))


_ = F()
m = M()
