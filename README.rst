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

An ``F`` expression extends placeholders with function composition, but at a slight performance cost.
They can be created explicitly from a function, or implicitly through operators as with placeholders.

.. code-block:: python

   >>> F(len) + 1
   lambda obj: len(obj) + 1

   >>> (___ * 2) + 1
   lambda obj: obj * 2 + 1

``__`` and ``___`` are placeholder and F singletons which can be imported from the module,
but each can of course be instantiated and bound to any desired name.

See tests for more example usage.

Installation
==================
Standard installation from pypi or local download. ::

   $ pip install placeholder
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
   * ``composer`` object depecated in favor of optimized ``F`` expression
