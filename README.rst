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

   _.age < 18     # lambda obj: obj.age < 18
   _[key] ** 2    # lambda obj: obj[key] ** 2

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

However, there is slight overhead (in CPython) in making an object callable.
Placeholders with single operators can access the ``func`` attribute directly for optimal performance.

.. code-block:: python

   _.age.func         # operator.attrgetter('age')
   _[key].func        # operator.itemgetter(key)

Performance should generally be comparable to inlined expressions, and faster than lambda.
Below are some example benchmarks.

.. code-block:: python

   min(data, key=operator.itemgetter(-1))    # 22.7 ms
   min(data, key=_[-1])                      # 25.9 ms
   min(data, key=lambda x: x[-1])            # 27.2 ms

Installation
==================
::

   $ pip install placeholder

Dependencies
==================
* Python ~=2.7, >=3.4

Tests
==================
100% branch coverage. ::

   $ pytest [--cov]

Changes
==================
0.7

* Deprecated ``__`` (double underscore)

0.6

* Optimized composite functions
* Renamed to ``_`` (single underscore) for consistency

0.5

* Unary operators
* ``__call__`` implements ``methodcaller``
* ``__getitem__`` supports only single argument
* Improved error handling
* ``composer`` object deprecated in favor of optimized ``F`` expression
