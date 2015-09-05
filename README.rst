About Placeholder
==================
Operator overloading for fast anonymous functions.

A ``placeholder`` object uses operator overloading to create partially bound functions on-the-fly.
When used in a binary expression, it will return a callable object with the other argument bound.
It's useful for replacing lambda in functional programming, and resembles Scala's placeholders.

.. code-block:: python

   >>> __[key]
   operator.itemgetter(key)

   >>> __.name
   operator.attrgetter('name')

   >>> 1 + __
   (1).__add__

   >>> __ - 1
   (1).__rsub__

   >>> -__
   operator.neg

A ``composer`` object extends placeholders with function composition, but at a performance cost.
In addition to operator overloading, functions can be supplied explicitly with postfix notation.

.. code-block:: python

   >>> (___ * 2) + 1
   lambda obj: obj * 2 + 1

   >>> composer(len, math.sqrt)
   lambda obj: math.sqrt(len(obj))

   >>> composer(len) + 1
   lambda obj: len(obj) + 1

``__`` and ``___`` are placeholder and composer singletons which can be imported from the module,
but each can of course be instantiated and bound to any desired name.

See tests for more example usage.

Installation
==================
Standard installation from pypi or local download. ::

   $ pip install multimethod
   $ python setup.py install

Dependencies
==================
Python 2.7 or 3.2+.

Tests
==================
100% branch coverage. ::

   $ py.test

Changes
==================
0.5

   * Unary operators
   * ``__call__`` implements ``methodcaller``
   * ``__getitem__`` supports only single argument
   * Improved error handling
