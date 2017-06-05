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


import random
import string
import unittest

from o11c.iterators import MinIter
from o11c.random import ordered_sample


class TestMinIter(unittest.TestCase):
    def test_hardcoded(self):
        lr10 = list(range(10))
        assert list(MinIter([0, 1, 2, 3, 4], [5, 6, 7, 8, 9])) == lr10
        assert list(MinIter([5, 6, 7, 8, 9], [0, 1, 2, 3, 4])) == lr10
        assert list(MinIter([0, 2, 4, 6, 8], [1, 3, 5, 7, 9])) == lr10
        assert list(MinIter([1, 3, 5, 7, 9], [0, 2, 4, 6, 8])) == lr10
        assert list(MinIter([0], [0])) == [0, 0]

    def test_random(self):
        for _ in range(100):
            num_samples = random.randint(0, 4)
            expected = []
            samples = []
            for _ in range(num_samples):
                sample_size = random.randint(0, 26)
                s = ordered_sample(string.ascii_lowercase, sample_size)
                expected.extend(s)
                samples.append(s)
            expected.sort()
            assert list(MinIter(*samples)) == expected
