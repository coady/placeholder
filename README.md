[![image](https://img.shields.io/pypi/v/placeholder.svg)](https://pypi.org/project/placeholder/)
![image](https://img.shields.io/pypi/pyversions/placeholder.svg)
[![image](https://pepy.tech/badge/placeholder)](https://pepy.tech/project/placeholder)
![image](https://img.shields.io/pypi/status/placeholder.svg)
[![build](https://github.com/coady/placeholder/actions/workflows/build.yml/badge.svg)](https://github.com/coady/placeholder/actions/workflows/build.yml)
[![image](https://codecov.io/gh/coady/placeholder/branch/main/graph/badge.svg)](https://codecov.io/gh/coady/placeholder/)
[![CodeQL](https://github.com/coady/placeholder/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/coady/placeholder/actions/workflows/github-code-scanning/codeql)
[![CodSpeed Badge](https://img.shields.io/endpoint?url=https://codspeed.io/badge.json)](https://codspeed.io/coady/placeholder)
[![image](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)

A `placeholder` uses operator overloading to create partially bound functions on-the-fly. When used in a binary expression, it will return a callable object with the other argument bound. It's useful for replacing `lambda` in functional programming, and resembles Scala's placeholders.

## Usage
```python
from placeholder import _     # single underscore

_.age < 18     # lambda obj: obj.age < 18
_[key] ** 2    # lambda obj: obj[key] ** 2
```

Note `_` has special meaning in other contexts, such as the previous output in interactive shells. Assign to a different name as needed.

`_` is a singleton of an `F` class, and `F` expressions can also be used with functions.

```python
from placeholder import F

-F(len)        # lambda obj: -len(obj)
```

All applicable double underscore methods are supported. Some methods coerce types: `len`, `bool`, `in`.

## Performance
The placeholder instance leverages `functools.partial` and `Placeholder` for optimization. It is significantly faster than similar libraries on PyPI.

Placeholders are provisionally iterable, allowing access to the underlying function and bound args.

```python
(func,) = _.age  # operator.attrgetter('age')
```

Performance should generally be comparable to inlined expressions, and faster than lambda.

## Installation
```console
pip install placeholder
```

## Tests
100% branch coverage.

```console
pytest [--cov]
```
