[![image](https://img.shields.io/pypi/v/placeholder.svg)](https://pypi.org/project/placeholder/)
[![image](https://img.shields.io/pypi/pyversions/placeholder.svg)](https://python3statement.org)
![image](https://img.shields.io/pypi/status/placeholder.svg)
[![image](https://img.shields.io/travis/coady/placeholder.svg)](https://travis-ci.org/coady/placeholder)
[![image](https://img.shields.io/codecov/c/github/coady/placeholder.svg)](https://codecov.io/github/coady/placeholder)
[![image](https://readthedocs.org/projects/placeholder/badge)](https://placeholder.readthedocs.io)
[![image](https://requires.io/github/coady/placeholder/requirements.svg)](https://requires.io/github/coady/placeholder/requirements/)
[![image](https://api.codeclimate.com/v1/badges/3d859b1e30ffac79f10e/maintainability)](https://codeclimate.com/github/coady/placeholder/maintainability)

A `placeholder` uses operator overloading to create partially bound functions on-the-fly.
When used in a binary expression, it will return a callable object with the other argument bound.
It's useful for replacing `lambda` in functional programming, and resembles Scala's placeholders.

# Usage
```python
from placeholder import _     # single underscore

_.age < 18     # lambda obj: obj.age < 18
_[key] ** 2    # lambda obj: obj[key] ** 2
```

Note interactive shells use `_` as the previous output, so assign to a different name as needed.

`_` is a singleton of an `F` class, and `F` expressions can also be used with functions.

```python
from placeholder import F

-F(len)        # lambda obj: -len(obj)
```

All applicable double underscore methods are supported.

# Performance
Every effort is made to optimize the placeholder instance.
It's 20-40x faster than similar libraries on PyPI.

However, there is slight overhead (in CPython) in making an object callable.
Placeholders with single operators can access the `func` attribute directly for optimal performance.

```python
_.age.func         # operator.attrgetter('age')
_[key].func        # operator.itemgetter(key)
```

Performance should generally be comparable to inlined expressions,
and faster than lambda. Below are some example benchmarks.

```python
min(data, key=operator.itemgetter(-1))    # 22.7 ms
min(data, key=_[-1])                      # 25.9 ms
min(data, key=lambda x: x[-1])            # 27.2 ms
```

# Installation

    $ pip install placeholder

# Tests
100% branch coverage.

    $ pytest [--cov]

# Changes
1.0
* Removed `__` (double underscore)
* Variable arguments of first function
* Method callers and multi-valued getters

0.7
* Deprecated `__` (double underscore)

0.6
* Optimized composite functions
* Renamed to `_` (single underscore) for consistency

0.5
* Unary operators
* `__call__` implements `methodcaller`
* `__getitem__` supports only single argument
* Improved error handling
* `composer` object deprecated in favor of optimized `F` expression
