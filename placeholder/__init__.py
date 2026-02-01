import functools
import math
import operator
from collections.abc import Callable, Iterable
from functools import partial
from typing import Self

try:
    from .partials import rpartial  # type: ignore
except ImportError:

    def rpartial(func, right):  # pragma: no cover
        return lambda left, f=func, r=right: f(left, r)


def composed(f: Callable, g: Callable, *args):
    """Compose and call functions."""
    return f(g(*args))


def methods(func: Callable):
    def left(self, other):
        if isinstance(other, F):
            return type(self)(func)
        if not hasattr(functools, "Placeholder"):  # <3.14
            f = rpartial(func, other)
            return type(self)(f) if self is _ else type(self)(composed, f, self)
        f = type(self)(func, functools.Placeholder, other)
        return f if self is _ else type(self)(composed, f, self)

    def right(self, other):
        f = type(self)(func, other)
        return f if self is _ else type(self)(composed, f, self)

    return left, right


def unary(func: Callable):
    return lambda self: type(self)(func) if self is _ else type(self)(composed, func, self)


class F(partial):
    """Partial function with operator support."""

    def __iter__(self):
        yield super().__getattribute__("func")
        yield from super().__getattribute__("args")

    def __getattribute__(self, name: str) -> Self:
        if name.startswith("__") and name.endswith("__"):
            return super().__getattribute__(name)
        return unary(operator.attrgetter(name))(self)

    def __getitem__(self, key) -> Self:
        return unary(operator.itemgetter(key))(self)

    def __round__(self, ndigits: int | None = None) -> Self:
        if ndigits is None:
            return unary(round)(self)
        f = type(self)(round, ndigits=ndigits)
        return f if self is _ else type(self)(composed, f, self)

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

    __eq__ = methods(operator.eq)[1]
    __ne__ = methods(operator.ne)[1]
    __lt__ = methods(operator.gt)[1]
    __gt__ = methods(operator.lt)[1]
    __le__ = methods(operator.ge)[1]
    __ge__ = methods(operator.le)[1]


class M:
    """Singleton for creating method callers and multi-valued getters."""

    def __getattr__(cls, name: str) -> F:
        """Return a `methodcaller` constructor."""
        return F(operator.methodcaller, name)

    def __call__(self, *names: str) -> F:
        """Return a tupled `attrgetter`."""
        return F(operator.attrgetter(*names))

    def __getitem__(self, keys: Iterable) -> F:
        """Return a tupled `itemgetter`."""
        return F(operator.itemgetter(*keys))


_ = F(composed)
m = M()
