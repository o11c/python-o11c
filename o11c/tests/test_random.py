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

from o11c.random import ordered_sample


class TestOrderedSample(unittest.TestCase):
    def test_edge(self):
        x = list(reversed(string.ascii_lowercase))
        assert ordered_sample(x, 0) == []
        assert ordered_sample(x, 26) == x

    def test_random(self):
        x = list(string.ascii_lowercase)
        random.shuffle(x)
        for _ in range(100):
            k = random.randint(0, len(x))
            s = ordered_sample(x, k)
            indices = [x.index(v) for v in s]
            assert all([indices[i-1] < indices[i] for i in range(1, k)])
