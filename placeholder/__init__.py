import functools
import math
import operator
from collections.abc import Callable, Iterable
from typing import Self

try:
    from .partials import rpartial  # type: ignore
except ImportError:

    def rpartial(func, right):  # pragma: no cover
        return lambda left, f=func, r=right: f(left, r)


def composed(f: Callable, g: Callable, *args):
    """Compose and call functions."""
    return f(g(*args))


def compose(func: Callable, self):
    """Compose function with `F` instance."""
    if self is _:
        return func if isinstance(func, F) else F(func)
    return F(composed, func, self)


def methods(func: Callable):
    def left(self, other):
        if isinstance(other, F):
            return F(func)
        if not hasattr(functools, "Placeholder"):  # <3.14
            return compose(rpartial(func, other), self)
        return compose(F(func, functools.Placeholder, other), self)

    def right(self, other):
        return compose(F(func, other), self)

    return left, right


def unary(func: Callable):
    return lambda self: compose(func, self)


class F(functools.partial):
    """Partial function with operator support."""

    def __iter__(self):
        yield super().__getattribute__("func")
        yield from super().__getattribute__("args")

    def __getattribute__(self, name: str) -> Self:
        if name.startswith("__") and name.endswith("__"):
            return super().__getattribute__(name)
        return compose(operator.attrgetter(name), self)

    def __getitem__(self, key) -> Self:
        return compose(operator.itemgetter(key), self)

    def __round__(self, ndigits: int | None = None) -> Self:
        return compose(round if ndigits is None else F(round, ndigits=ndigits), self)

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
