import pytest
from placeholder import placeholder, F, __, ___


def test_object():
    assert type(___) is F and type(__) is placeholder
    assert placeholder()
    with pytest.raises(TypeError):
        placeholder(None)


def test_getters():
    assert (___.__class__)(None) is None.__class__
    with pytest.raises(AttributeError):
        ___.name(None)
    assert (___[0])({0: None}) is (___[0])([None]) is None
    with pytest.raises(KeyError):
        ___[0]({})
    with pytest.raises(IndexError):
        ___[0]([])
    assert sorted(enumerate('cba'), key=___[1]) == [(2, 'a'), (1, 'b'), (0, 'c')]
    assert __('split', '.')('x.y') == ['x', 'y']


def test_math():
    assert (___ + 1)(2) == (1 + ___)(2) == 3
    assert (___ - 1)(2) == (3 - ___)(2) == 1
    with pytest.raises(TypeError):
        (___ + 1)(2, x=None)
    assert [x + 1 for x in range(3)] == list(map(___ + 1, range(3)))
    assert (___ * 2)(3) == (2 * ___)(3) == 6
    assert (___ / 2)(3) == (3 / ___)(2) == 1.5
    assert (___ // 2)(3) == (3 // ___)(2) == 1
    assert (___ % 2)(3) == (3 % ___)(2) == 1
    assert divmod(___, 2)(3) == divmod(3, ___)(2) == (1, 1)
    assert (___ ** 3)(2) == (2 ** ___)(3) == 8
    assert (___ + [1])([0]) == ([0] + ___)([1]) == [0, 1]
    assert (___ * [0])(2) == ([0] * ___)(2) == [0, 0]


def test_binary():
    assert (___ << 2)(1) == (1 << ___)(2) == 4
    assert (___ >> 2)(7) == (7 >> ___)(2) == 1
    assert (___ & 3)(5) == (5 & ___)(3) == 1
    assert (___ | 3)(5) == (5 | ___)(3) == 7
    assert (___ ^ 3)(5) == (5 ^ ___)(3) == 6


def test_comparisons():
    for x, y in [(1, 2), (1.0, 2.0)]:
        assert (___ < y)(x) and (___ > x)(y)
        assert (___ <= y)(x) and (___ >= x)(y)
        assert (___ == x)(x) and (___ != x)(y)


def test_composition():
    F(len).__call__ is len
    assert (F(len) + 1)('') == 1


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
    assert (-___)(1) == -1
    assert (+___)(-1) == -1
    assert (~___)(0) == -1
