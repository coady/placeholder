import sys
import pytest
from placeholder import placeholder, F, __, _


def test_object():
    assert type(_) is F and type(__) is placeholder
    assert placeholder()
    with pytest.raises(TypeError):
        placeholder(None)


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
    assert __('split', '.')('x.y') == ['x', 'y']


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


def test_comparisons():
    for x, y in [(1, 2), (1.0, 2.0)]:
        assert (_ < y)(x) and (_ > x)(y)
        assert (_ <= y)(x) and (_ >= x)(y)
        assert (_ == x)(x) and (_ != x)(y)


def test_composition():
    f = F(len) + 1
    assert f('') == 1
    assert (f * 2)('') == 2


def test_errors():
    for obj in (__ + None, __ - None, __ * None, __ // None, __ / None, __ % None, divmod(__, None),
                __ ** None, __ << None, __ >> None, __ & None, __ ^ None, __ | None):
        with pytest.raises(TypeError):
            obj(0)
    with pytest.raises(TypeError):
        list(__)
    with pytest.raises(TypeError):
        None in __


def test_unary():
    assert (-_)(1) == -1
    assert (+_)(-1) == -1
    assert (~_)(0) == -1


@pytest.mark.skipif(sys.version_info < (3, 5), reason="requires Python 3.5+")
def test_matmul():
    for func in map(eval, ('_ @ None', 'None @ _')):
        assert isinstance(func, F)
        with pytest.raises(TypeError):
            func(0)
