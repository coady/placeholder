import math
import pytest
from parametrized import parametrized
from placeholder import F, _, m


def test_object():
    assert type(_) is F
    assert F({}.get) > 1
    assert (_ == 1)(1.0) is (1 == _)(1.0) is True


def test_getters():
    assert (_.append)(list) is list.append
    with pytest.raises(AttributeError):
        _.name(None)
    assert (_[0])({0: None}) is (_[0])([None]) is None
    with pytest.raises(KeyError):
        _[0]({})
    with pytest.raises(IndexError):
        _[0]([])
    assert sorted(enumerate('cba'), key=_[1]) == [(2, 'a'), (1, 'b'), (0, 'c')]
    assert m.split('-')('a-b') == ['a', 'b']
    assert m('real', 'imag')(1) == (1, 0)
    assert m[0, -1]('abc') == ('a', 'c')


def test_math():
    assert (_ + 1)(2) == (1 + _)(2) == 3
    assert (_ - 1)(2) == (3 - _)(2) == 1
    with pytest.raises(TypeError):
        (_ + 1)(2, x=None)
    assert [x + 1 for x in range(3)] == list(map(_ + 1, range(3)))
    assert (_ * 2)(3) == (2 * _)(3) == 6
    assert (_ / 2)(3) == (3 / _)(2) == 1.5
    assert (_ // 2)(3) == (3 // _)(2) == 1
    assert (_ % 2)(3) == (3 % _)(2) == 1
    assert divmod(_, 2)(3) == divmod(3, _)(2) == (1, 1)
    assert (_ ** 3)(2) == (2 ** _)(3) == 8
    assert (_ + [1])([0]) == ([0] + _)([1]) == [0, 1]
    assert (_ * [0])(2) == ([0] * _)(2) == [0, 0]


def test_binary():
    assert (_ << 2)(1) == (1 << _)(2) == 4
    assert (_ >> 2)(7) == (7 >> _)(2) == 1
    assert (_ & 3)(5) == (5 & _)(3) == 1
    assert (_ | 3)(5) == (5 | _)(3) == 7
    assert (_ ^ 3)(5) == (5 ^ _)(3) == 6


@parametrized.zip
def test_comparisons(x=(1, 1.0), y=(2, 2.0)):
    assert (_ < y)(x) and (_ > x)(y)
    assert (_ <= y)(x) and (_ >= x)(y)
    assert (_ == x)(x) and (_ != x)(y)


def test_composition():
    f = F(len) + 1
    assert f('') == 1
    assert (f * 2)('') == 2
    mean = (_ + _) / 2.0
    assert mean(0, 1) == 0.5


@parametrized
def test_errors(op='+ - * // / % ** << >> & ^ | @'.split()):
    for expr in ('_ {} None', 'None {} _'):
        func = eval(expr.format(op))
        with pytest.raises(TypeError):
            func(0)


def test_unary():
    assert (-_)(1) == -1
    assert (+_)(-1) == -1
    assert (~_)(0) == -1

    assert abs(_)(-1) == 1
    assert list(reversed(_)('abc')) == ['c', 'b', 'a']
    assert math.trunc(_)(-1.1) == -1

    assert round(_)(0.1) == 0
    assert round(_, 1)(0.11) == 0.1
    assert math.floor(_)(-1.1) == -2
    assert math.ceil(_)(-1.1) == -1
