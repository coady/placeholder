from __future__ import division

import unittest, sys
from distutils import util

# patch for testing in-place
sys.path.append('build/lib.%s-%s' % (util.get_platform(), sys.version[:3]))

from placeholder import partial, placeholder, __

class TestCase(unittest.TestCase):

    def testObject(self):
        assert type(__) is placeholder
        self.assertRaises(TypeError, partial)
        self.assertRaises(TypeError, partial, 1)
        self.assertRaises(TypeError, partial, 1, 2, 3)
        c = partial(1, 2)
        assert type(c) is partial and hasattr(c, '__call__')
        self.assertRaises(TypeError, __)
        self.assertRaises(TypeError, __, x=0)
        self.assertRaises(TypeError, __, 0)
        self.assertRaises(TypeError, __, 0, 1)

    def testBasic(self):
        assert (__.__class__)(None) == type(None)
        self.assertRaises(AttributeError, __.name, None)
        assert (__[0])({0: None}) == (__[0])([None]) == None
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

    def testBinary(self):
        assert (__ << 2)(1) == (1 << __)(2) == 4
        assert (__ >> 2)(7) == (7 >> __)(2) == 1
        assert (__ & 3)(5) == (5 & __)(3) == 1
        assert (__ | 3)(5) == (5 | __)(3) == 7
        assert (__ ^ 3)(5) == (5 ^ __)(3) == 6

if __name__ == '__main__':
    unittest.main()
