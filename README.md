[![image](https://img.shields.io/pypi/v/placeholder.svg)](https://pypi.org/project/placeholder/)
![image](https://img.shields.io/pypi/pyversions/placeholder.svg)
[![image](https://pepy.tech/badge/placeholder)](https://pepy.tech/project/placeholder)
![image](https://img.shields.io/pypi/status/placeholder.svg)
[![image](https://github.com/coady/placeholder/workflows/build/badge.svg)](https://github.com/coady/placeholder/actions)
[![image](https://codecov.io/gh/coady/placeholder/branch/main/graph/badge.svg)](https://codecov.io/gh/coady/placeholder/)
 [![image](https://github.com/coady/placeholder/workflows/codeql/badge.svg)](https://github.com/coady/placeholder/security/code-scanning)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)
[![image](http://mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

A `placeholder` uses operator overloading to create partially bound functions on-the-fly. When used in a binary expression, it will return a callable object with the other argument bound. It's useful for replacing `lambda` in functional programming, and resembles Scala's placeholders.

## Usage
```python
from placeholder import _     # single underscore

_.age < 18     # lambda obj: obj.age < 18
_[key] ** 2    # lambda obj: obj[key] ** 2
```

Note `_` has special meaning in other contexts, such as the previous output in interactive shells. Assign to a different name as needed. Kotlin uses `it`, but in Python `it` is a common short name for an iterator.

`_` is a singleton of an `F` class, and `F` expressions can also be used with functions.

```python
from placeholder import F

-F(len)        # lambda obj: -len(obj)
```

All applicable double underscore methods are supported.

## Performance
Every effort is made to optimize the placeholder instance. It's 20-40x faster than similar libraries on PyPI.

However, there is slight overhead (in CPython) in making an object callable. Placeholders with single operators can access the `func` attribute directly for optimal performance.

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

## Installation
```console
% pip install placeholder
```

## Tests
100% branch coverage.

```console
% pytest [--cov]
```

## Changes
1.2.1

* setup fix

1.2

* Python >=3.6 required
* Optimized `partial` implementation

1.1

* Additional unary functions

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
