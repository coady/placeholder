import itertools
import math
import operator
from functools import partial
from typing import Callable, Iterable, Iterator, Sequence
from . import partials  # type: ignore

__version__ = '1.4'


def update_wrapper(wrapper: Callable, func: Callable):
    wrapper.__doc__ = func.__doc__
    wrapper.__name__ = func.__name__
    wrapper.__annotations__['return'] = 'F'
    return wrapper


def pipe(funcs: Sequence[Callable], *args, **kwargs):
    value = funcs[0](*args, **kwargs)
    for func in funcs[1:]:
        value = func(value)
    return value


def methods(func: Callable):
    def left(self, other):
        if isinstance(other, F):
            return type(self)(self, func)
        return type(self)(self, partials.partial(func, other).left)

    def right(self, other):
        return type(self)(self, partials.partial(func, other).right)

    return update_wrapper(left, func), update_wrapper(right, func)


def unary(func: Callable):
    return update_wrapper(lambda self: type(self)(self, func), func)


class F(partial):
    """Singleton for creating composite functions.

    Args:
        *funcs (Callable): ordered callables
    """

    def __new__(cls, *funcs):
        funcs = (func if isinstance(func, cls) else [func] for func in funcs)
        funcs = tuple(itertools.chain(*funcs))
        return partial.__new__(cls, *(funcs if len(funcs) == 1 else (pipe, funcs)))

    def __iter__(self) -> Iterator[Callable]:
        """Return composed functions in order."""
        args = super().__getattribute__('args')
        return iter(args[0] if args else [super().__getattribute__('func')])

    def __getattribute__(self, attr: str) -> 'F':
        """Return `attrgetter`."""
        if attr.startswith('__') and attr.endswith('__'):
            return super().__getattribute__(attr)
        return type(self)(self, operator.attrgetter(attr))

    def __getitem__(self, item) -> 'F':
        """Return `itemgetter`."""
        return type(self)(self, operator.itemgetter(item))

    def __round__(self, ndigits: int = None) -> 'F':
        """Return `round(...)`."""
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
    __truediv__, __rtruediv__ = methods(operator.truediv)

    __mod__, __rmod__ = methods(operator.mod)
    __divmod__, __rdivmod__ = methods(divmod)
    __pow__, __rpow__ = methods(operator.pow)
    __matmul__, __rmatmul__ = methods(operator.matmul)

    __lshift__, __rlshift__ = methods(operator.lshift)
    __rshift__, __rrshift__ = methods(operator.rshift)

    __and__, __rand__ = methods(operator.and_)
    __xor__, __rxor__ = methods(operator.xor)
    __or__, __ror__ = methods(operator.or_)

    __eq__ = methods(operator.eq)[0]
    __ne__ = methods(operator.ne)[0]
    __lt__, __gt__ = methods(operator.lt)
    __le__, __ge__ = methods(operator.le)


class M:
    """Singleton for creating method callers and multi-valued getters."""

    def __getattr__(cls, name: str) -> F:
        """Return a `methodcaller` constructor."""
        return F(partial(operator.methodcaller, name), F)

    def __call__(self, *names: str) -> F:
        """Return a tupled `attrgetter`."""
        return F(operator.attrgetter(*names))

    def __getitem__(self, keys: Iterable) -> F:
        """Return a tupled `itemgetter`."""
        return F(operator.itemgetter(*keys))


_ = F()
m = M()
