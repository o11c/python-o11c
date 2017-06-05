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


import bisect


def iter_forward(sz):
    return range(sz)


def freeze(arr):
    ''' Does nothing here (input is already sorted).
    '''
    return arr


def search(arr, item):
    ''' Return the index where the item might be.
    '''
    rv = bisect.bisect_right(arr, item) - 1
    assert rv == -1 or arr[rv] <= item
    assert rv+1 == len(arr) or item < arr[rv+1]
    return rv
