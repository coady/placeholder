from __future__ import division

import unittest
from placeholder import placeholder, __

class TestCase(unittest.TestCase):

    def testObject(self):
        assert type(__) is placeholder
        assert placeholder()
        self.assertRaises(TypeError, placeholder, None)

    def testGetters(self):
        assert (__.__class__)(None) is type(None)
        self.assertRaises(AttributeError, __.name, None)
        assert (__[0])({0: None}) is (__[0])([None]) is None
        self.assertRaises(KeyError, __[0], {})
        self.assertRaises(IndexError, __[0], [])
        assert sorted(enumerate('cba'), key=__[1]) == [(2, 'a'), (1, 'b'), (0, 'c')]
        assert (__[0, 1])([True, False]) == (True, False)

    def testMath(self):
        assert (__ + 1)(2) == (1 + __)(2) == 3
        self.assertRaises(TypeError, __ + None, 0)
        assert (__ - 1)(2) == (3 - __)(2) == 1
        self.assertRaises(TypeError, __ + 1, 2, x=None)
        assert [x+1 for x in range(3)] == map(__ + 1, range(3))
        assert (__ * 2)(3) == (2 * __)(3) == 6
        assert (__ / 2)(3) == (3 / __)(2) == 1.5
        assert (__ // 2)(3) == (3 // __)(2) == 1
        assert (__ % 2)(3) == (3 % __)(2) == 1
        assert divmod(__, 2)(3) == divmod(3, __)(2) == (1, 1)
        assert (__ ** 3)(2) == (2 ** __)(3) == 8
        
        assert (__ + [1])([0]) == ([0] + __)([1]) == [0, 1]
        assert (__ * [0])(2) == ([0] * __)(2) == [0, 0]

    def testBinary(self):
        assert (__ << 2)(1) == (1 << __)(2) == 4
        assert (__ >> 2)(7) == (7 >> __)(2) == 1
        assert (__ & 3)(5) == (5 & __)(3) == 1
        assert (__ | 3)(5) == (5 | __)(3) == 7
        assert (__ ^ 3)(5) == (5 ^ __)(3) == 6

    def testComparisons(self):
        for x, y in [(1, 2), (1.0, 2.0)]:
            assert (__ < y)(x) and (__ > x)(y)
            assert (__ <= y)(x) and (__ >= x)(y)
            assert (__ == x)(x) and (__ != x)(y)

if __name__ == '__main__':
    unittest.main()
