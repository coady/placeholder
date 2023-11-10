[![image](https://img.shields.io/pypi/v/placeholder.svg)](https://pypi.org/project/placeholder/)
![image](https://img.shields.io/pypi/pyversions/placeholder.svg)
[![image](https://pepy.tech/badge/placeholder)](https://pepy.tech/project/placeholder)
![image](https://img.shields.io/pypi/status/placeholder.svg)
[![image](https://github.com/coady/placeholder/workflows/build/badge.svg)](https://github.com/coady/placeholder/actions)
[![image](https://codecov.io/gh/coady/placeholder/branch/main/graph/badge.svg)](https://codecov.io/gh/coady/placeholder/)
 [![image](https://github.com/coady/placeholder/workflows/codeql/badge.svg)](https://github.com/coady/placeholder/security/code-scanning)
[![image](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![image](https://mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

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

Placeholders are also iterable, allowing direct access to the underlying functions.

```python
(func,) = _.age  # operator.attrgetter('age')
```

Performance should generally be comparable to inlined expressions, and faster than lambda. Below are some example benchmarks.

```python
min(data, key=operator.itemgetter(-1))    # 1x
min(data, key=_[-1])                      # 1.3x
min(data, key=lambda x: x[-1])            # 1.6x
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
