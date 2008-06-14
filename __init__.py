"""
A placeholder object uses operator overloading to create partially bound
functions on-the-fly.  When used in a binary expression, it will return a
callable object with the other argument bound.  It's useful for replacing
lambda when doing functional programming.  For example:

    __[key]     ==   operator.itemgetter(key)
    __.name     ==   operator.attrgetter('name')
    (1 + __)    ==   lambda obj: 1 + obj
    (__ - 1)    ==   lambda obj: obj - 1

where '__' is a placeholder instance (it can have any name of course).

The ctypes module is used to access the Python C API directly,
so it is also much faster than using a python function.

See tests for more example usage.
"""

import ctypes
import partial
cdll = ctypes.CDLL(partial.__file__)

def factory(name, **kwargs):
    "Return partial object from the python api or the partial dll itself."
    lib = ctypes.pythonapi if name.startswith('Py') else cdll
    pointer = ctypes.cast(getattr(lib, name), ctypes.c_void_p)
    return partial.partial(name, pointer.value, **kwargs)

class placeholder(object):
    __slots__ = ()
    def __getattribute__(self, other):
        return factory('PyObject_GetAttr', right=other)
    def __getitem__(self, other):
        return factory('PyObject_GetItem', right=other)

    def __add__(self, other):
        return factory('PyNumber_Add', right=other)
    def __radd__(self, other):
        return factory('PyNumber_Add', left=other)
    def __sub__(self, other):
        return factory('PyNumber_Subtract', right=other)
    def __rsub__(self, other):
        return factory('PyNumber_Subtract', left=other)
    def __mul__(self, other):
        return factory('PyNumber_Multiply', right=other)
    def __rmul__(self, other):
        return factory('PyNumber_Multiply', left=other)
    def __div__(self, other):
        return factory('PyNumber_Divide', right=other)
    def __rdiv__(self, other):
        return factory('PyNumber_Divide', left=other)
    def __floordiv__(self, other):
        return factory('PyNumber_FloorDivide', right=other)
    def __rfloordiv__(self, other):
        return factory('PyNumber_FloorDivide', left=other)
    def __truediv__(self, other):
        return factory('PyNumber_TrueDivide', right=other)
    def __rtruediv__(self, other):
        return factory('PyNumber_TrueDivide', left=other)
    def __mod__(self, other):
        return factory('PyNumber_Remainder', right=other)
    def __rmod__(self, other):
        return factory('PyNumber_Remainder', left=other)
    def __divmod__(self, other):
        return factory('PyNumber_Divmod', right=other)
    def __rdivmod__(self, other):
        return factory('PyNumber_Divmod', left=other)
    def __pow__(self, other):
        return factory('Number_Power', right=other)
    def __rpow__(self, other):
        return factory('Number_Power', left=other)

    def __lshift__(self, other):
        return factory('PyNumber_Lshift', right=other)
    def __rlshift__(self, other):
        return factory('PyNumber_Lshift', left=other)
    def __rshift__(self, other):
        return factory('PyNumber_Rshift', right=other)
    def __rrshift__(self, other):
        return factory('PyNumber_Rshift', left=other)
    def __and__(self, other):
        return factory('PyNumber_And', right=other)
    def __rand__(self, other):
        return factory('PyNumber_And', left=other)
    def __xor__(self, other):
        return factory('PyNumber_Xor', right=other)
    def __rxor__(self, other):
        return factory('PyNumber_Xor', left=other)
    def __or__(self, other):
        return factory('PyNumber_Or', right=other)
    def __ror__(self, other):
        return factory('PyNumber_Or', left=other)

    def __lt__(self, other):
        return factory('Object_LT', right=other)
    def __le__(self, other):
        return factory('Object_LE', right=other)
    def __eq__(self, other):
        return factory('Object_EQ', right=other)
    def __ne__(self, other):
        return factory('Object_NE', right=other)
    def __gt__(self, other):
        return factory('Object_GT', right=other)
    def __ge__(self, other):
        return factory('Object_GE', right=other)

__ = placeholder()
