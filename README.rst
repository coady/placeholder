.. image:: https://img.shields.io/pypi/v/placeholder.svg
   :target: https://pypi.python.org/pypi/placeholder/
.. image:: https://img.shields.io/pypi/pyversions/placeholder.svg
.. image:: https://img.shields.io/pypi/status/placeholder.svg
.. image:: https://img.shields.io/travis/coady/placeholder.svg
   :target: https://travis-ci.org/coady/placeholder
.. image:: https://img.shields.io/codecov/c/github/coady/placeholder.svg
   :target: https://codecov.io/github/coady/placeholder

A ``placeholder`` uses operator overloading to create partially bound functions on-the-fly.
When used in a binary expression, it will return a callable object with the other argument bound.
It's useful for replacing ``lambda`` in functional programming, and resembles Scala's placeholders.

Usage
==================
.. code-block:: python

   from placeholder import _     # single underscore

   _.age < 18     # lambda person: person.age < 18
   _[key] ** 2    # lambda data: data[key] ** 2

``_`` is a singleton of an ``F`` class, and ``F`` expressions can also be used with functions.

.. code-block:: python

   from placeholder import F

   -F(len)        # lambda obj: -len(obj)

All applicable double underscore methods are supported.
See tests for more example usage.

Performance
==================
Every effort is made to optimize the placeholder instance.
It's 20-40x faster than similar libraries on PyPI.

However, there is overhead (in CPython) in making an object callable.
Therefore a lower-level ``placeholder`` ``__`` is also exposed;
it returns builtins which can't be composed any further.

.. code-block:: python

   from placeholder import __    # double underscore

   __.age         # operator.attrgetter('age')
   __[key]        # operator.itemgetter(key)
   __ + 1         # (1).__radd__

``__`` should generally be faster than even inlined code.
Whereas ``_`` will likely be slightly slower than inlined code, but faster than a ``lambda``.
Below are some example benchmarks comparing ``map`` to an inlined generator expression.

.. code-block:: python

   any(map(__ > 0, data))           # 3.92 ms
   any(x > 0 for x in data)         # 5.6 ms
   any(map(_ > 0, data))            # 6.81 ms
   any(map(lambda x: x > 0, data))  # 9.17 ms

Installation
==================
::

   $ pip install placeholder

Dependencies
==================
Python 2.7 or 3.3+.

Tests
==================
100% branch coverage. ::

   $ pytest [--cov]

Changes
==================
0.6

* Optimized composite functions
* Renamed to ``_`` (single underscore) for consistency

0.5

* Unary operators
* ``__call__`` implements ``methodcaller``
* ``__getitem__`` supports only single argument
* Improved error handling
* ``composer`` object deprecated in favor of optimized ``F`` expression
