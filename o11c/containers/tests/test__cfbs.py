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


import numpy as np
from string import ascii_lowercase
import unittest

from o11c.containers import _cfbs as cfbs


class TestCfbs(unittest.TestCase):
    def test_hardcoded(self):
        assert cfbs.make_order(range(0)) == []
        assert list(cfbs.iter_forward(0)) == []
        #                       0
        assert cfbs.make_order(range(1)) == [0]
        assert list(cfbs.iter_forward(1)) == [0]
        #                       1
        #           0
        assert cfbs.make_order(range(2)) == [1, 0]
        assert list(cfbs.iter_forward(2)) == [1, 0]
        #                       1
        #           0                       2
        assert cfbs.make_order(range(3)) == [1, 0, 2]
        assert list(cfbs.iter_forward(3)) == [1, 0, 2]
        #                       2
        #           1                       3
        #     0
        assert cfbs.make_order(range(4)) == [2, 1, 3, 0]
        assert list(cfbs.iter_forward(4)) == [3, 1, 0, 2]
        #                       3
        #           1                       4
        #     0           2
        assert cfbs.make_order(range(5)) == [3, 1, 4, 0, 2]
        assert list(cfbs.iter_forward(5)) == [3, 1, 4, 0, 2]
        #                       3
        #           1                       5
        #     0           2           4
        assert cfbs.make_order(range(6)) == [3, 1, 5, 0, 2, 4]
        assert list(cfbs.iter_forward(6)) == [3, 1, 4, 0, 5, 2]
        #                       3
        #           1                       5
        #     0           2           4           6
        assert cfbs.make_order(range(7)) == [3, 1, 5, 0, 2, 4, 6]
        assert list(cfbs.iter_forward(7)) == [3, 1, 4, 0, 5, 2, 6]
        #                       4
        #           2                       6
        #     1           3           5           7
        #  0
        assert cfbs.make_order(range(8)) == [4, 2, 6, 1, 3, 5, 7, 0]
        assert list(cfbs.iter_forward(8)) == [7, 3, 1, 4, 0, 5, 2, 6]
        #                       5
        #           3                       7
        #     1           4           6           8
        #  0     2
        assert cfbs.make_order(range(9)) == [5, 3, 7, 1, 4, 6, 8, 0, 2]
        assert list(cfbs.iter_forward(9)) == [7, 3, 8, 1, 4, 0, 5, 2, 6]
        #                       6
        #           3                       8
        #     1           5           7           9
        #  0     2     4
        assert cfbs.make_order(range(10)) == [6, 3, 8, 1, 5, 7, 9, 0, 2, 4]
        assert list(cfbs.iter_forward(10)) == [7, 3, 8, 1, 9, 4, 0, 5, 2, 6]
        #                       7
        #           3                       9
        #     1           5           8          10
        #  0     2     4     6
        assert cfbs.make_order(range(11)) == [7, 3, 9, 1, 5, 8, 10, 0, 2, 4, 6]
        assert list(cfbs.iter_forward(11)) == [7, 3, 8, 1, 9, 4, 10, 0, 5, 2, 6]
        #                       7
        #           3                      10
        #     1           5           9          11
        #  0     2     4     6     8
        assert cfbs.make_order(range(12)) == [7, 3, 10, 1, 5, 9, 11, 0, 2, 4, 6, 8]
        assert list(cfbs.iter_forward(12)) == [7, 3, 8, 1, 9, 4, 10, 0, 11, 5, 2, 6]
        #                       7
        #           3                      11
        #     1           5           9          12
        #  0     2     4     6     8    10
        assert cfbs.make_order(range(13)) == [7, 3, 11, 1, 5, 9, 12, 0, 2, 4, 6, 8, 10]
        assert list(cfbs.iter_forward(13)) == [7, 3, 8, 1, 9, 4, 10, 0, 11, 5, 12, 2, 6]
        #                       7
        #           3                      11
        #     1           5           9          13
        #  0     2     4     6     8    10    12
        assert cfbs.make_order(range(14)) == [7, 3, 11, 1, 5, 9, 13, 0, 2, 4, 6, 8, 10, 12]
        assert list(cfbs.iter_forward(14)) == [7, 3, 8, 1, 9, 4, 10, 0, 11, 5, 12, 2, 13, 6]
        #                       7
        #           3                      11
        #     1           5           9          13
        #  0     2     4     6     8    10    12    14
        assert cfbs.make_order(range(15)) == [7, 3, 11, 1, 5, 9, 13, 0, 2, 4, 6, 8, 10, 12, 14]
        assert list(cfbs.iter_forward(15)) == [7, 3, 8, 1, 9, 4, 10, 0, 11, 5, 12, 2, 13, 6, 14]

        assert cfbs.make_order(ascii_lowercase[:0]) == list()
        assert cfbs.make_order(ascii_lowercase[:1]) == list('a')
        assert cfbs.make_order(ascii_lowercase[:2]) == list('ba')
        assert cfbs.make_order(ascii_lowercase[:3]) == list('bac')
        assert cfbs.make_order(ascii_lowercase[:4]) == list('cbda')
        assert cfbs.make_order(ascii_lowercase[:5]) == list('dbeac')
        assert cfbs.make_order(ascii_lowercase[:6]) == list('dbface')
        assert cfbs.make_order(ascii_lowercase[:7]) == list('dbfaceg')
        assert cfbs.make_order(ascii_lowercase[:8]) == list('ecgbdfha')
        assert cfbs.make_order(ascii_lowercase[:9]) == list('fdhbegiac')
        assert cfbs.make_order(ascii_lowercase[:10]) == list('gdibfhjace')
        assert cfbs.make_order(ascii_lowercase[:11]) == list('hdjbfikaceg')
        assert cfbs.make_order(ascii_lowercase[:12]) == list('hdkbfjlacegi')
        assert cfbs.make_order(ascii_lowercase[:13]) == list('hdlbfjmacegik')
        assert cfbs.make_order(ascii_lowercase[:14]) == list('hdlbfjnacegikm')
        assert cfbs.make_order(ascii_lowercase[:15]) == list('hdlbfjnacegikmo')

    def test_iter(self):
        for sz in range(100):
            orig = ['E%d' % i for i in range(sz)]
            order = cfbs.make_order(orig)
            assert list(orig) == list(cfbs.iter_order_forward(order))
            assert list(reversed(orig)) == list(cfbs.iter_order_backward(order))

    def test_tree(self):
        for sz in range(100):
            order = cfbs.make_order(range(sz))
            for i in range(len(order)):
                if cfbs.has_left_child(i, sz):
                    assert order[cfbs.left_child(i)] < order[i]
                if cfbs.has_right_child(i, sz):
                    assert order[i] < order[cfbs.right_child(i)]

    def test_numpy(self):
        for sz in range(100):
            order_in_python_list = cfbs.make_order(range(sz))
            order_in_numpy_array = cfbs.make_order(iter(range(sz)), into=np.ndarray(sz, dtype=np.int32))
            assert isinstance(order_in_numpy_array, np.ndarray)
            assert all(order_in_python_list == order_in_numpy_array)
