#   python-o11c - generic utilities library
#   Copyright © 2017  Ben Longbons
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import abc
import importlib
import numpy as np
import unittest

mod = importlib.import_module(__name__.replace('.containers.tests.test_', '.containers.'))
for name in '''
    SortedSet RangeSet AutoSet
    SortedMap RangeMap DeltaMap AutoMap
'''.split():
    globals()[name] = getattr(mod, name)
del name
from o11c.enums import ErrorBool


class _TestSetBase(unittest.TestCase, metaclass=abc.ABCMeta):
    cls = None
    need_int_key = False

    def test_iter(self):
        s = self.cls()
        assert not s and len(s) == 0
        assert list(s) == []
        s = self.cls(set())
        assert not s and len(s) == 0
        assert list(s) == []
        s = self.cls({2, 1})
        assert s and len(s) == 2
        assert list(s) == [1, 2]
        if not self.need_int_key:
            s = self.cls({'foo', 'bar'})
            assert s and len(s) == 2
            assert list(s) == ['bar', 'foo']
        s = self.cls([])
        assert not s and len(s) == 0
        assert list(s) == []
        s = self.cls([2, 1])
        assert s and len(s) == 2
        assert list(s) == [1, 2]
        if not self.need_int_key:
            s = self.cls(['foo', 'bar'])
            assert s and len(s) == 2
            assert list(s) == ['bar', 'foo']

    def test_lookup(self):
        s = self.cls()
        assert [x for x in s if x in s] == []
        s = self.cls({2, 1})
        assert [x for x in s if x in s] == [1, 2]
        if not self.need_int_key:
            s = self.cls({'foo', 'bar'})
            assert [x for x in s if x in s] == ['bar', 'foo']

    def test_repr(self):
        s = self.cls()
        repr(s)
        s = self.cls({2, 1})
        repr(s)
        if not self.need_int_key:
            s = self.cls({'foo', 'bar'})
            repr(s)

    def test_raw(self):
        s = self.cls()
        r = s._to_raw()
        t = self.cls._from_raw(*r)
        u = self.convert_raw('>u4', *r)
        v = self.cls._from_raw(*u)
        assert s == t == v
        s = self.cls({2, 1})
        r = s._to_raw()
        t = self.cls._from_raw(*r)
        u = self.convert_raw('>u4', *r)
        v = self.cls._from_raw(*u)
        assert s == t == v
        if not self.need_int_key:
            s = self.cls({'foo', 'bar'})
            r = s._to_raw()
            t = self.cls._from_raw(*r)
            u = self.convert_raw('O', *r)
            v = self.cls._from_raw(*u)

    def cls_from_pairs(self, pairs):
        rv = self.cls()
        append_range = self.append_range
        for low_key, high_key in pairs:
            append_range(rv, low_key, high_key)
        rv._freeze()
        return rv

    @staticmethod
    @abc.abstractmethod
    def append_range(self, low_key, high_key):
        pass # pragma: no cover

    def test_harder(self):
        # important key patterns:
        # (x = prior, X = being added)
        #  0123456
        #   x X
        #   x XX
        #   xx X
        #   xx XX
        #   xX
        #   xXX
        #   xxX
        #   xxXX
        s = self.cls_from_pairs([(1, 1), (3, 3)])
        assert [k for k in range(7) if k in s] == [1, 3]
        s = self.cls_from_pairs([(1, 1), (3, 4)])
        assert [k for k in range(7) if k in s] == [1, 3, 4]
        s = self.cls_from_pairs([(1, 2), (4, 4)])
        assert [k for k in range(7) if k in s] == [1, 2, 4]
        s = self.cls_from_pairs([(1, 2), (4, 5)])
        assert [k for k in range(7) if k in s] == [1, 2, 4, 5]
        s = self.cls_from_pairs([(1, 1), (2, 2)])
        assert [k for k in range(7) if k in s] == [1, 2]
        s = self.cls_from_pairs([(1, 1), (2, 3)])
        assert [k for k in range(7) if k in s] == [1, 2, 3]
        s = self.cls_from_pairs([(1, 2), (3, 3)])
        assert [k for k in range(7) if k in s] == [1, 2, 3]
        s = self.cls_from_pairs([(1, 2), (3, 4)])
        assert [k for k in range(7) if k in s] == [1, 2, 3, 4]
        # All together now
        s = self.cls_from_pairs([
            (1001, 1001), (1003, 1003),
            (1011, 1011), (1013, 1014),
            (1021, 1022), (1024, 1024),
            (1031, 1032), (1034, 1035),
            (1041, 1041), (1042, 1042),
            (1051, 1051), (1052, 1053),
            (1061, 1062), (1063, 1063),
            (1071, 1072), (1073, 1074),
        ])
        assert [k for k in range(1000, 1100) if k in s] == [
            1001, 1003,
            1011, 1013, 1014,
            1021, 1022, 1024,
            1031, 1032, 1034, 1035,
            1041, 1042,
            1051, 1052, 1053,
            1061, 1062, 1063,
            1071, 1072, 1073, 1074,
        ]


class _TestMapBase(unittest.TestCase, metaclass=abc.ABCMeta):
    cls = None
    need_int_key = False
    need_int_value = False

    def test_iter(self):
        m = self.cls()
        assert not m and len(m) == 0
        assert list(m) == []
        m = self.cls({})
        assert not m and len(m) == 0
        assert list(m) == []
        if not self.need_int_value:
            m = self.cls({3: 'x', 1: 'y', 2: 'x'})
            assert m and len(m) == 3
            assert list(m) == [1, 2, 3]
        m = self.cls({3: -1, 1: -2, 2: -1})
        assert m and len(m) == 3
        assert list(m) == [1, 2, 3]
        if not self.need_int_key:
            m = self.cls({'foo': 1, 'bar': 2, 'baz': 1})
            assert m and len(m) == 3
            assert list(m) == ['bar', 'baz', 'foo']
        m = self.cls([])
        assert not m and len(m) == 0
        assert list(m) == []
        if not self.need_int_value:
            m = self.cls([(3, 'x'), (1, 'y'), (2, 'x')])
            assert m and len(m) == 3
            assert list(m) == [1, 2, 3]
        m = self.cls([(3, -1), (1, -2), (2, -1)])
        assert m and len(m) == 3
        assert list(m) == [1, 2, 3]
        if not self.need_int_key:
            m = self.cls([('foo', 1), ('bar', 2), ('baz', 1)])
            assert m and len(m) == 3
            assert list(m) == ['bar', 'baz', 'foo']

    def test_lookup(self):
        m = self.cls()
        assert list(m.items()) == []
        if not self.need_int_value:
            m = self.cls({3: 'x', 1: 'y', 2: 'x'})
            assert list(m.items()) == [(1, 'y'), (2, 'x'), (3, 'x')]
        m = self.cls({3: -1, 1: -2, 2: -1})
        assert list(m.items()) == [(1, -2), (2, -1), (3, -1)]
        if not self.need_int_key:
            m = self.cls({'foo': 1, 'bar': 2, 'baz': 1})
            assert list(m.items()) == [('bar', 2), ('baz', 1), ('foo', 1)]

    def test_repr(self):
        m = self.cls()
        repr(m)
        if not self.need_int_value:
            m = self.cls({3: 'x', 1: 'y', 2: 'x'})
            repr(m)
        m = self.cls({3: -1, 1: -2, 2: -1})
        repr(m)
        if not self.need_int_key:
            m = self.cls({'foo': 1, 'bar': 2, 'baz': 1})
            repr(m)

    def test_raw(self):
        m = self.cls()
        r = m._to_raw()
        t = self.cls._from_raw(*r)
        u = self.convert_raw('>u4', '>u4', *r)
        v = self.cls._from_raw(*u)
        assert m == t == v
        if not self.need_int_value:
            m = self.cls({3: 'x', 1: 'y', 2: 'x'})
            r = m._to_raw()
            t = self.cls._from_raw(*r)
            u = self.convert_raw('>u4', 'O', *r)
            v = self.cls._from_raw(*u)
            assert m == t == v
        m = self.cls({3: -1, 1: -2, 2: -1})
        r = m._to_raw()
        t = self.cls._from_raw(*r)
        u = self.convert_raw('>u4', 'O', *r)
        v = self.cls._from_raw(*u)
        assert m == t == v
        if not self.need_int_key:
            m = self.cls({'foo': 1, 'bar': 2, 'baz': 1})
            r = m._to_raw()
            t = self.cls._from_raw(*r)
            u = self.convert_raw('O', '>u4', *r)
            v = self.cls._from_raw(*u)
            assert m == t == v

    def cls_from_quads(self, quads):
        rv = self.cls()
        append_quad = self.append_quad
        for low_key, high_key, value, is_delta in quads:
            append_quad(rv, low_key, high_key, value, is_delta)
        rv._freeze()
        return rv

    @staticmethod
    @abc.abstractmethod
    def append_quad(self, low_key, high_key, value, is_delta):
        pass # pragma: no cover

    def test_harder(self):
        # important key patterns:
        # (x = prior, X = being added)
        #  0123456
        #   x X
        #   x XX
        #   xx X
        #   xx XX
        #   xX
        #   xXX
        #   xxX
        #   xxXX
        # important value patterns:
        #   11
        #   12
        #   13
        #   1 1
        #   1 2
        #   1 3
        #   1 4
        #   1  1
        #   1  2
        #   1  3
        #   1  4
        #   1  5
        F = False
        T = True
        E = ErrorBool

        m = self.cls_from_quads([(1, 1, 101, E), (3, 3, 101, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 101), (3, 101)]
        m = self.cls_from_quads([(1, 1, 101, E), (3, 3, 102, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 101), (3, 102)]
        m = self.cls_from_quads([(1, 1, 101, E), (3, 3, 103, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 101), (3, 103)]
        m = self.cls_from_quads([(1, 1, 101, E), (3, 3, 104, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 101), (3, 104)]

        m = self.cls_from_quads([(1, 1, 201, E), (3, 4, 201, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 201), (3, 201), (4, 201)]
        m = self.cls_from_quads([(1, 1, 201, E), (3, 4, 201, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 201), (3, 201), (4, 202)]
        m = self.cls_from_quads([(1, 1, 201, E), (3, 4, 202, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 201), (3, 202), (4, 202)]
        m = self.cls_from_quads([(1, 1, 201, E), (3, 4, 202, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 201), (3, 202), (4, 203)]
        m = self.cls_from_quads([(1, 1, 201, E), (3, 4, 203, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 201), (3, 203), (4, 203)]
        m = self.cls_from_quads([(1, 1, 201, E), (3, 4, 203, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 201), (3, 203), (4, 204)]
        m = self.cls_from_quads([(1, 1, 201, E), (3, 4, 204, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 201), (3, 204), (4, 204)]
        m = self.cls_from_quads([(1, 1, 201, E), (3, 4, 204, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 201), (3, 204), (4, 205)]

        m = self.cls_from_quads([(1, 2, 301, F), (4, 4, 301, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 301), (2, 301), (4, 301)]
        m = self.cls_from_quads([(1, 2, 301, T), (4, 4, 301, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 301), (2, 302), (4, 301)]
        m = self.cls_from_quads([(1, 2, 301, F), (4, 4, 302, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 301), (2, 301), (4, 302)]
        m = self.cls_from_quads([(1, 2, 301, T), (4, 4, 302, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 301), (2, 302), (4, 302)]
        m = self.cls_from_quads([(1, 2, 301, F), (4, 4, 303, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 301), (2, 301), (4, 303)]
        m = self.cls_from_quads([(1, 2, 301, T), (4, 4, 303, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 301), (2, 302), (4, 303)]
        m = self.cls_from_quads([(1, 2, 301, F), (4, 4, 304, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 301), (2, 301), (4, 304)]
        m = self.cls_from_quads([(1, 2, 301, T), (4, 4, 304, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 301), (2, 302), (4, 304)]
        m = self.cls_from_quads([(1, 2, 301, F), (4, 4, 305, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 301), (2, 301), (4, 305)]
        m = self.cls_from_quads([(1, 2, 301, T), (4, 4, 305, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 301), (2, 302), (4, 305)]

        m = self.cls_from_quads([(1, 2, 401, F), (4, 5, 401, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 401), (4, 401), (5, 401)]
        m = self.cls_from_quads([(1, 2, 401, F), (4, 5, 401, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 401), (4, 401), (5, 402)]
        m = self.cls_from_quads([(1, 2, 401, T), (4, 5, 401, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 402), (4, 401), (5, 401)]
        m = self.cls_from_quads([(1, 2, 401, T), (4, 5, 401, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 402), (4, 401), (5, 402)]
        m = self.cls_from_quads([(1, 2, 401, F), (4, 5, 402, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 401), (4, 402), (5, 402)]
        m = self.cls_from_quads([(1, 2, 401, F), (4, 5, 402, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 401), (4, 402), (5, 403)]
        m = self.cls_from_quads([(1, 2, 401, T), (4, 5, 402, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 402), (4, 402), (5, 402)]
        m = self.cls_from_quads([(1, 2, 401, T), (4, 5, 402, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 402), (4, 402), (5, 403)]
        m = self.cls_from_quads([(1, 2, 401, F), (4, 5, 403, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 401), (4, 403), (5, 403)]
        m = self.cls_from_quads([(1, 2, 401, F), (4, 5, 403, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 401), (4, 403), (5, 404)]
        m = self.cls_from_quads([(1, 2, 401, T), (4, 5, 403, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 402), (4, 403), (5, 403)]
        m = self.cls_from_quads([(1, 2, 401, T), (4, 5, 403, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 402), (4, 403), (5, 404)]
        m = self.cls_from_quads([(1, 2, 401, F), (4, 5, 404, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 401), (4, 404), (5, 404)]
        m = self.cls_from_quads([(1, 2, 401, F), (4, 5, 404, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 401), (4, 404), (5, 405)]
        m = self.cls_from_quads([(1, 2, 401, T), (4, 5, 404, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 402), (4, 404), (5, 404)]
        m = self.cls_from_quads([(1, 2, 401, T), (4, 5, 404, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 402), (4, 404), (5, 405)]
        m = self.cls_from_quads([(1, 2, 401, F), (4, 5, 405, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 401), (4, 405), (5, 405)]
        m = self.cls_from_quads([(1, 2, 401, F), (4, 5, 405, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 401), (4, 405), (5, 406)]
        m = self.cls_from_quads([(1, 2, 401, T), (4, 5, 405, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 402), (4, 405), (5, 405)]
        m = self.cls_from_quads([(1, 2, 401, T), (4, 5, 405, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 401), (2, 402), (4, 405), (5, 406)]

        m = self.cls_from_quads([(1, 1, 501, E), (2, 2, 501, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 501), (2, 501)]
        m = self.cls_from_quads([(1, 1, 501, E), (2, 2, 502, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 501), (2, 502)]
        m = self.cls_from_quads([(1, 1, 501, E), (2, 2, 503, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 501), (2, 503)]

        m = self.cls_from_quads([(1, 1, 601, E), (2, 3, 601, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 601), (2, 601), (3, 601)]
        m = self.cls_from_quads([(1, 1, 601, E), (2, 3, 601, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 601), (2, 601), (3, 602)]
        m = self.cls_from_quads([(1, 1, 601, E), (2, 3, 602, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 601), (2, 602), (3, 602)]
        m = self.cls_from_quads([(1, 1, 601, E), (2, 3, 602, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 601), (2, 602), (3, 603)]
        m = self.cls_from_quads([(1, 1, 601, E), (2, 3, 603, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 601), (2, 603), (3, 603)]
        m = self.cls_from_quads([(1, 1, 601, E), (2, 3, 603, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 601), (2, 603), (3, 604)]

        m = self.cls_from_quads([(1, 2, 701, F), (3, 3, 701, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 701), (2, 701), (3, 701)]
        m = self.cls_from_quads([(1, 2, 701, T), (3, 3, 701, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 701), (2, 702), (3, 701)]
        m = self.cls_from_quads([(1, 2, 701, F), (3, 3, 702, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 701), (2, 701), (3, 702)]
        m = self.cls_from_quads([(1, 2, 701, T), (3, 3, 702, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 701), (2, 702), (3, 702)]
        m = self.cls_from_quads([(1, 2, 701, F), (3, 3, 703, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 701), (2, 701), (3, 703)]
        m = self.cls_from_quads([(1, 2, 701, T), (3, 3, 703, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 701), (2, 702), (3, 703)]
        m = self.cls_from_quads([(1, 2, 701, F), (3, 3, 704, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 701), (2, 701), (3, 704)]
        m = self.cls_from_quads([(1, 2, 701, T), (3, 3, 704, E)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 701), (2, 702), (3, 704)]

        m = self.cls_from_quads([(1, 2, 801, F), (3, 4, 801, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 801), (3, 801), (4, 801)]
        m = self.cls_from_quads([(1, 2, 801, F), (3, 4, 801, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 801), (3, 801), (4, 802)]
        m = self.cls_from_quads([(1, 2, 801, T), (3, 4, 801, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 802), (3, 801), (4, 801)]
        m = self.cls_from_quads([(1, 2, 801, T), (3, 4, 801, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 802), (3, 801), (4, 802)]
        m = self.cls_from_quads([(1, 2, 801, F), (3, 4, 802, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 801), (3, 802), (4, 802)]
        m = self.cls_from_quads([(1, 2, 801, F), (3, 4, 802, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 801), (3, 802), (4, 803)]
        m = self.cls_from_quads([(1, 2, 801, T), (3, 4, 802, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 802), (3, 802), (4, 802)]
        m = self.cls_from_quads([(1, 2, 801, T), (3, 4, 802, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 802), (3, 802), (4, 803)]
        m = self.cls_from_quads([(1, 2, 801, F), (3, 4, 803, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 801), (3, 803), (4, 803)]
        m = self.cls_from_quads([(1, 2, 801, F), (3, 4, 803, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 801), (3, 803), (4, 804)]
        m = self.cls_from_quads([(1, 2, 801, T), (3, 4, 803, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 802), (3, 803), (4, 803)]
        m = self.cls_from_quads([(1, 2, 801, T), (3, 4, 803, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 802), (3, 803), (4, 804)]
        m = self.cls_from_quads([(1, 2, 801, F), (3, 4, 804, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 801), (3, 804), (4, 804)]
        m = self.cls_from_quads([(1, 2, 801, F), (3, 4, 804, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 801), (3, 804), (4, 805)]
        m = self.cls_from_quads([(1, 2, 801, T), (3, 4, 804, F)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 802), (3, 804), (4, 804)]
        m = self.cls_from_quads([(1, 2, 801, T), (3, 4, 804, T)])
        assert [(k, m[k]) for k in range(7) if k in m] == [(1, 801), (2, 802), (3, 804), (4, 805)]

        # All together now
        m = self.cls_from_quads([
            (1001, 1001, 101, E), (1003, 1003, 101, E),
            (1011, 1011, 101, E), (1013, 1013, 102, E),
            (1021, 1021, 101, E), (1023, 1023, 103, E),
            (1031, 1031, 101, E), (1033, 1033, 104, E),

            (1101, 1101, 201, E), (1103, 1104, 201, F),
            (1111, 1111, 201, E), (1113, 1114, 201, T),
            (1121, 1121, 201, E), (1123, 1124, 202, F),
            (1131, 1131, 201, E), (1133, 1134, 202, T),
            (1141, 1141, 201, E), (1143, 1144, 203, F),
            (1151, 1151, 201, E), (1153, 1154, 203, T),
            (1161, 1161, 201, E), (1163, 1164, 204, F),
            (1171, 1171, 201, E), (1173, 1174, 204, T),

            (1201, 1202, 301, F), (1204, 1204, 301, E),
            (1211, 1212, 301, T), (1214, 1214, 301, E),
            (1221, 1222, 301, F), (1224, 1224, 302, E),
            (1231, 1232, 301, T), (1234, 1234, 302, E),
            (1241, 1242, 301, F), (1244, 1244, 303, E),
            (1251, 1252, 301, T), (1254, 1254, 303, E),
            (1261, 1262, 301, F), (1264, 1264, 304, E),
            (1271, 1272, 301, T), (1274, 1274, 304, E),
            (1281, 1282, 301, F), (1284, 1284, 305, E),
            (1291, 1292, 301, T), (1294, 1294, 305, E),

            (1301, 1302, 401, F), (1304, 1305, 401, F),
            (1311, 1312, 401, F), (1314, 1315, 401, T),
            (1321, 1322, 401, T), (1324, 1325, 401, F),
            (1331, 1332, 401, T), (1334, 1335, 401, T),
            (1341, 1342, 401, F), (1344, 1345, 402, F),
            (1351, 1352, 401, F), (1354, 1355, 402, T),
            (1361, 1362, 401, T), (1364, 1365, 402, F),
            (1371, 1372, 401, T), (1374, 1375, 402, T),
            (1381, 1382, 401, F), (1384, 1385, 403, F),
            (1391, 1392, 401, F), (1394, 1395, 403, T),
            (1401, 1402, 401, T), (1404, 1405, 403, F),
            (1411, 1412, 401, T), (1414, 1415, 403, T),
            (1421, 1422, 401, F), (1424, 1425, 404, F),
            (1431, 1432, 401, F), (1434, 1435, 404, T),
            (1441, 1442, 401, T), (1444, 1445, 404, F),
            (1451, 1452, 401, T), (1454, 1455, 404, T),
            (1461, 1462, 401, F), (1464, 1465, 405, F),
            (1471, 1472, 401, F), (1474, 1475, 405, T),
            (1481, 1482, 401, T), (1484, 1485, 405, F),
            (1491, 1492, 401, T), (1494, 1495, 405, T),

            (1501, 1501, 501, E), (1502, 1502, 501, E),
            (1511, 1511, 501, E), (1512, 1512, 502, E),
            (1521, 1521, 501, E), (1522, 1522, 503, E),

            (1601, 1601, 601, E), (1602, 1603, 601, F),
            (1611, 1611, 601, E), (1612, 1613, 601, T),
            (1621, 1621, 601, E), (1622, 1623, 602, F),
            (1631, 1631, 601, E), (1632, 1633, 602, T),
            (1641, 1641, 601, E), (1642, 1643, 603, F),
            (1651, 1651, 601, E), (1652, 1653, 603, T),

            (1701, 1702, 701, F), (1703, 1703, 701, E),
            (1711, 1712, 701, T), (1713, 1713, 701, E),
            (1721, 1722, 701, F), (1723, 1723, 702, E),
            (1731, 1732, 701, T), (1733, 1733, 702, E),
            (1741, 1742, 701, F), (1743, 1743, 703, E),
            (1751, 1752, 701, T), (1753, 1753, 703, E),
            (1761, 1762, 701, F), (1763, 1763, 704, E),
            (1771, 1772, 701, T), (1773, 1773, 704, E),

            (1801, 1802, 801, F), (1803, 1804, 801, F),
            (1811, 1812, 801, F), (1813, 1814, 801, T),
            (1821, 1822, 801, T), (1823, 1824, 801, F),
            (1831, 1832, 801, T), (1833, 1834, 801, T),
            (1841, 1842, 801, F), (1843, 1844, 802, F),
            (1851, 1852, 801, F), (1853, 1854, 802, T),
            (1861, 1862, 801, T), (1863, 1864, 802, F),
            (1871, 1872, 801, T), (1873, 1874, 802, T),
            (1881, 1882, 801, F), (1883, 1884, 803, F),
            (1891, 1892, 801, F), (1893, 1894, 803, T),
            (1901, 1902, 801, T), (1903, 1904, 803, F),
            (1911, 1912, 801, T), (1913, 1914, 803, T),
            (1921, 1922, 801, F), (1923, 1924, 804, F),
            (1931, 1932, 801, F), (1933, 1934, 804, T),
            (1941, 1942, 801, T), (1943, 1944, 804, F),
            (1951, 1952, 801, T), (1953, 1954, 804, T),
        ])
        assert [(k, m[k]) for k in range(1000, 2000) if k in m] == [
            (1001, 101), (1003, 101),
            (1011, 101), (1013, 102),
            (1021, 101), (1023, 103),
            (1031, 101), (1033, 104),

            (1101, 201), (1103, 201), (1104, 201),
            (1111, 201), (1113, 201), (1114, 202),
            (1121, 201), (1123, 202), (1124, 202),
            (1131, 201), (1133, 202), (1134, 203),
            (1141, 201), (1143, 203), (1144, 203),
            (1151, 201), (1153, 203), (1154, 204),
            (1161, 201), (1163, 204), (1164, 204),
            (1171, 201), (1173, 204), (1174, 205),

            (1201, 301), (1202, 301), (1204, 301),
            (1211, 301), (1212, 302), (1214, 301),
            (1221, 301), (1222, 301), (1224, 302),
            (1231, 301), (1232, 302), (1234, 302),
            (1241, 301), (1242, 301), (1244, 303),
            (1251, 301), (1252, 302), (1254, 303),
            (1261, 301), (1262, 301), (1264, 304),
            (1271, 301), (1272, 302), (1274, 304),
            (1281, 301), (1282, 301), (1284, 305),
            (1291, 301), (1292, 302), (1294, 305),

            (1301, 401), (1302, 401), (1304, 401), (1305, 401),
            (1311, 401), (1312, 401), (1314, 401), (1315, 402),
            (1321, 401), (1322, 402), (1324, 401), (1325, 401),
            (1331, 401), (1332, 402), (1334, 401), (1335, 402),
            (1341, 401), (1342, 401), (1344, 402), (1345, 402),
            (1351, 401), (1352, 401), (1354, 402), (1355, 403),
            (1361, 401), (1362, 402), (1364, 402), (1365, 402),
            (1371, 401), (1372, 402), (1374, 402), (1375, 403),
            (1381, 401), (1382, 401), (1384, 403), (1385, 403),
            (1391, 401), (1392, 401), (1394, 403), (1395, 404),
            (1401, 401), (1402, 402), (1404, 403), (1405, 403),
            (1411, 401), (1412, 402), (1414, 403), (1415, 404),
            (1421, 401), (1422, 401), (1424, 404), (1425, 404),
            (1431, 401), (1432, 401), (1434, 404), (1435, 405),
            (1441, 401), (1442, 402), (1444, 404), (1445, 404),
            (1451, 401), (1452, 402), (1454, 404), (1455, 405),
            (1461, 401), (1462, 401), (1464, 405), (1465, 405),
            (1471, 401), (1472, 401), (1474, 405), (1475, 406),
            (1481, 401), (1482, 402), (1484, 405), (1485, 405),
            (1491, 401), (1492, 402), (1494, 405), (1495, 406),

            (1501, 501), (1502, 501),
            (1511, 501), (1512, 502),
            (1521, 501), (1522, 503),

            (1601, 601), (1602, 601), (1603, 601),
            (1611, 601), (1612, 601), (1613, 602),
            (1621, 601), (1622, 602), (1623, 602),
            (1631, 601), (1632, 602), (1633, 603),
            (1641, 601), (1642, 603), (1643, 603),
            (1651, 601), (1652, 603), (1653, 604),

            (1701, 701), (1702, 701), (1703, 701),
            (1711, 701), (1712, 702), (1713, 701),
            (1721, 701), (1722, 701), (1723, 702),
            (1731, 701), (1732, 702), (1733, 702),
            (1741, 701), (1742, 701), (1743, 703),
            (1751, 701), (1752, 702), (1753, 703),
            (1761, 701), (1762, 701), (1763, 704),
            (1771, 701), (1772, 702), (1773, 704),

            (1801, 801), (1802, 801), (1803, 801), (1804, 801),
            (1811, 801), (1812, 801), (1813, 801), (1814, 802),
            (1821, 801), (1822, 802), (1823, 801), (1824, 801),
            (1831, 801), (1832, 802), (1833, 801), (1834, 802),
            (1841, 801), (1842, 801), (1843, 802), (1844, 802),
            (1851, 801), (1852, 801), (1853, 802), (1854, 803),
            (1861, 801), (1862, 802), (1863, 802), (1864, 802),
            (1871, 801), (1872, 802), (1873, 802), (1874, 803),
            (1881, 801), (1882, 801), (1883, 803), (1884, 803),
            (1891, 801), (1892, 801), (1893, 803), (1894, 804),
            (1901, 801), (1902, 802), (1903, 803), (1904, 803),
            (1911, 801), (1912, 802), (1913, 803), (1914, 804),
            (1921, 801), (1922, 801), (1923, 804), (1924, 804),
            (1931, 801), (1932, 801), (1933, 804), (1934, 805),
            (1941, 801), (1942, 802), (1943, 804), (1944, 804),
            (1951, 801), (1952, 802), (1953, 804), (1954, 805),
        ]


class TestSortedSet(_TestSetBase):
    cls = SortedSet

    @staticmethod
    def convert_raw(key_dtype, len, keys):
        keys = np.array(keys, dtype=key_dtype)
        return len, keys

    @staticmethod
    def append_range(self, low_key, high_key):
        for key in range(low_key, high_key + 1):
            self._append(key)


class TestRangeSet(_TestSetBase):
    cls = RangeSet
    need_int_key = True

    @staticmethod
    def convert_raw(key_dtype, len, low_keys, high_keys):
        low_keys = np.array(low_keys, dtype=key_dtype)
        high_keys = np.array(high_keys, dtype=key_dtype)
        return len, low_keys, high_keys

    append_range = staticmethod(cls._append_range)


class TestAutoSet(_TestSetBase):
    cls = AutoSet

    @staticmethod
    def convert_raw(key_dtype, simple_raw, compressed_raw):
        simple_raw = TestSortedSet.convert_raw(key_dtype, *simple_raw)
        compressed_raw = TestRangeSet.convert_raw(key_dtype, *compressed_raw)
        return simple_raw, compressed_raw

    append_range = staticmethod(cls._append_range)


class TestSortedMap(_TestMapBase):
    cls = SortedMap

    @staticmethod
    def convert_raw(key_dtype, value_dtype, len, keys, values):
        keys = np.array(keys, dtype=key_dtype)
        values = np.array(values, dtype=value_dtype)
        return len, keys, values

    @staticmethod
    def append_quad(self, low_key, high_key, value, is_delta):
        if low_key == high_key or not is_delta:
            for key in range(low_key, high_key + 1):
                self._append(key, value)
            return
        assert is_delta
        for i, key in enumerate(range(low_key, high_key + 1)):
            self._append(key, value + i)


class TestRangeMap(_TestMapBase):
    cls = RangeMap
    need_int_key = True

    @staticmethod
    def convert_raw(key_dtype, value_dtype, len, low_keys, high_keys, values):
        low_keys = np.array(low_keys, dtype=key_dtype)
        high_keys = np.array(high_keys, dtype=key_dtype)
        values = np.array(values, dtype=value_dtype)
        return len, low_keys, high_keys, values

    @staticmethod
    def append_quad(self, low_key, high_key, value, is_delta):
        if low_key == high_key or not is_delta:
            self._append_range(low_key, high_key, value)
            return
        assert is_delta
        for i, key in enumerate(range(low_key, high_key + 1)):
            self._append_range(key, key, value + i)


class TestDeltaMap(_TestMapBase):
    cls = DeltaMap
    need_int_key = True
    need_int_value = True

    @staticmethod
    def convert_raw(key_dtype, value_dtype, len, low_keys, high_keys, values):
        low_keys = np.array(low_keys, dtype=key_dtype)
        high_keys = np.array(high_keys, dtype=key_dtype)
        values = np.array(values, dtype=value_dtype)
        return len, low_keys, high_keys, values

    @staticmethod
    def append_quad(self, low_key, high_key, value, is_delta):
        if low_key == high_key or is_delta:
            self._append_range(low_key, high_key, value)
            return
        assert not is_delta
        for key in range(low_key, high_key + 1):
            self._append_range(key, key, value)


class TestAutoMap(_TestMapBase):
    cls = AutoMap

    @staticmethod
    def convert_raw(key_dtype, value_dtype, simple_raw, compressed_raw, sequential_raw):
        simple_raw = TestSortedMap.convert_raw(key_dtype, value_dtype, *simple_raw)
        compressed_raw = TestRangeMap.convert_raw(key_dtype, value_dtype, *compressed_raw)
        sequential_raw = TestDeltaMap.convert_raw(key_dtype, value_dtype, *sequential_raw)
        return simple_raw, compressed_raw, sequential_raw

    append_quad = staticmethod(cls._append_range)


del _TestSetBase
del _TestMapBase
