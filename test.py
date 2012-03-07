from __future__ import division

import unittest
from placeholder import placeholder, composer, __, ___

class TestCase(unittest.TestCase):

    def testObject(self):
        assert type(___) is composer and type(__) is placeholder
        assert placeholder()
        self.assertRaises(TypeError, placeholder, None)

    def testGetters(self):
        assert (___.__class__)(None) is type(None)
        self.assertRaises(AttributeError, ___.name, None)
        assert (___[0])({0: None}) is (___[0])([None]) is None
        self.assertRaises(KeyError, ___[0], {})
        self.assertRaises(IndexError, ___[0], [])
        assert sorted(enumerate('cba'), key=___[1]) == [(2, 'a'), (1, 'b'), (0, 'c')]
        assert (___[0, 1])([True, False]) == (True, False)

    def testMath(self):
        assert (___ + 1)(2) == (1 + ___)(2) == 3
        self.assertRaises(TypeError, ___ + None, 0)
        assert (___ - 1)(2) == (3 - ___)(2) == 1
        self.assertRaises(TypeError, ___ + 1, 2, x=None)
        assert [x+1 for x in range(3)] == list(map(___ + 1, range(3)))
        assert (___ * 2)(3) == (2 * ___)(3) == 6
        assert (___ / 2)(3) == (3 / ___)(2) == 1.5
        assert (___ // 2)(3) == (3 // ___)(2) == 1
        assert (___ % 2)(3) == (3 % ___)(2) == 1
        assert divmod(___, 2)(3) == divmod(3, ___)(2) == (1, 1)
        assert (___ ** 3)(2) == (2 ** ___)(3) == 8
        
        assert (___ + [1])([0]) == ([0] + ___)([1]) == [0, 1]
        assert (___ * [0])(2) == ([0] * ___)(2) == [0, 0]

    def testBinary(self):
        assert (___ << 2)(1) == (1 << ___)(2) == 4
        assert (___ >> 2)(7) == (7 >> ___)(2) == 1
        assert (___ & 3)(5) == (5 & ___)(3) == 1
        assert (___ | 3)(5) == (5 | ___)(3) == 7
        assert (___ ^ 3)(5) == (5 ^ ___)(3) == 6

    def testComparisons(self):
        for x, y in [(1, 2), (1.0, 2.0)]:
            assert (___ < y)(x) and (___ > x)(y)
            assert (___ <= y)(x) and (___ >= x)(y)
            assert (___ == x)(x) and (___ != x)(y)

    def testComposition(self):
        assert ___(Ellipsis) is Ellipsis
        assert (composer(len) + 1)('') == 1
        assert composer(len, bool)('') is False

if __name__ == '__main__':
    unittest.main()
