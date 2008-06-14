from __future__ import division

import unittest, sys
from distutils import util

# patch for testing in-place
sys.path.append('build/lib.%s-%s' % (util.get_platform(), sys.version[:3]))
from placeholder import partial, placeholder, __

class TestCase(unittest.TestCase):

    def testObject(self):
        assert type(__) is placeholder
        self.assertRaises(TypeError, partial.partial, '', 0)
        self.assertRaises(TypeError, partial.partial, '', None, None)
        self.assertRaises(TypeError, partial.partial, None, 0, None)
        self.assertRaises(TypeError, partial.partial, '', 0, None, None)
        func = partial.partial('', 0, None)
        assert type(func) is partial.partial and hasattr(func, '__call__')
        self.assertRaises(TypeError, func)
        self.assertRaises(TypeError, func, None, None)
        self.assertRaises(TypeError, func, arg=None)

    def testAttributes(self):
        func = __ + 1
        assert func.name == 'PyNumber_Add'
        assert not hasattr(func, 'left')
        assert func.right == 1
        assert str(func) == 'PyNumber_Add(, 1)'
        for name in ('name', 'left', 'right'):
            self.assertRaises(TypeError, setattr, func, name, None)

    def testGetters(self):
        assert (__.__class__)(None) is type(None)
        self.assertRaises(AttributeError, __.name, None)
        assert (__[0])({0: None}) is (__[0])([None]) is None
        self.assertRaises(KeyError, __[0], {})
        self.assertRaises(IndexError, __[0], [])
        assert sorted(enumerate('cba'), key=__[1]) == [(2, 'a'), (1, 'b'), (0, 'c')]

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

    def testBinary(self):
        assert (__ << 2)(1) == (1 << __)(2) == 4
        assert (__ >> 2)(7) == (7 >> __)(2) == 1
        assert (__ & 3)(5) == (5 & __)(3) == 1
        assert (__ | 3)(5) == (5 | __)(3) == 7
        assert (__ ^ 3)(5) == (5 ^ __)(3) == 6

    def testComparisons(self):
        assert (__ < 2)(1) and (__ > 1)(2)
        assert (__ <= 2)(1) and (__ >= 1)(2)
        assert (__ == 1)(1) and (__ != 1)(2)

if __name__ == '__main__':
    unittest.main()
