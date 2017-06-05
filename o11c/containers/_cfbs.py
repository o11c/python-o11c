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


# Orders:
# (If not one-less-than-a-power-of-2, the last row will collapse as needed)
#
#                        07
#            03                      11
#      01          05          09          13
#   00    02    04    06    08    10    12    14
# 15: 07 03 11 01 05 09 13 00 02 04 06 08 10 12 14
#
#                        07
#            03                      11
#      01          05          09          13
#   00    02    04    06    08    10    12    __
# 14: 07 03 11 01 05 09 13 00 02 04 06 08 10 12
#
#                        07
#            03                      11
#      01          05          09          12
#   00    02    04    06    08    10    __    __
# 13: 07 03 11 01 05 09 12 00 02 04 06 08 10
#
#                        07
#            03                      10
#      01          05          09          11
#   00    02    04    06    08    __    __    __
# 12: 07 03 10 01 05 09 11 00 02 04 06 08
#
#                        07
#            03                      09
#      01          05          08          10
#   00    02    04    06    __    __    __    __
# 11: 07 03 09 01 05 08 10 00 02 04 06
#
#                        06
#            03                      08
#      01          05          07          09
#   00    02    04    __    __    __    __    __
# 10: 06 03 08 01 05 07 09 00 02 04
#
#                        05
#            03                      07
#      01          04          06          08
#   00    02    __    __    __    __    __    __
# 09: 05 03 07 01 04 06 08 00 02
#
#                        04
#            02                      06
#      01          03          05          07
#   00    __    __    __    __    __    __    __
# 08: 04 02 06 01 03 05 07 00
#
#                        03
#            01                      05
#      00          02          04          06
# 07: 03 01 05 00 02 04 06
#
#                        03
#            01                      05
#      00          02          04          __
# 06: 03 01 05 00 02 04
#
#                        03
#            01                      04
#      00          02          __          __
# 05: 03 01 04 00 02
#
#                        02
#            01                      03
#      00          __          __          __
# 04: 02 01 03 00
#
#                        01
#            00                      02
# 03: 01 00 02
#
#                        01
#            00                      __
# 02: 01 00
#
#                        00
# 01: 00
#
# 00:


def parent(n):
    assert n is not None
    return (n - 1) // 2


def left_child(n):
    assert n is not None
    return n * 2 + 1


def right_child(n):
    assert n is not None
    return n * 2 + 2


def is_root(n):
    assert n is not None
    return n == 0


def is_left_child(n):
    assert n is not None
    return n % 2 == 1


def is_right_child(n):
    assert n is not None
    return n != 0 and n % 2 == 0


def has_left_child(n, sz):
    assert n is not None
    return left_child(n) < sz


def has_right_child(n, sz):
    assert n is not None
    return right_child(n) < sz


def leftmost_child(n, sz):
    assert n is not None
    while has_left_child(n, sz):
        n = left_child(n)
    return n


def rightmost_child(n, sz):
    assert n is not None
    while has_right_child(n, sz):
        n = right_child(n)
    return n


def predecessor(n, sz):
    assert n is not None
    if has_left_child(n, sz):
        n = left_child(n)
        return rightmost_child(n, sz)
    while True:
        if is_right_child(n):
            return parent(n)
        if is_root(n):
            return None
        n = parent(n)


def successor(n, sz):
    assert n is not None
    if has_right_child(n, sz):
        n = right_child(n)
        return leftmost_child(n, sz)
    while True:
        if is_left_child(n):
            return parent(n)
        if is_root(n):
            return None
        n = parent(n)


def first(sz):
    if sz == 0:
        return None
    n = 0
    return leftmost_child(n, sz)


def last(sz):
    if sz == 0:
        return None
    n = 0
    return rightmost_child(n, sz)


def iter_forward(sz):
    n = first(sz)
    while n is not None:
        yield n
        n = successor(n, sz)


def iter_backward(sz):
    n = last(sz)
    while n is not None:
        yield n
        n = predecessor(n, sz)


def make_order(arr, *, into=None):
    if into is None:
        sz = len(arr)
        into = [None] * sz
    else:
        # Don't require random-access `arr` in this case.
        sz = len(into)
    # Do the source array in order since it can be prefetched,
    # whereas the destination array can use cache-line masking regardless.
    for idx, elem in zip(iter_forward(sz), arr):
        into[idx] = elem
    return into


def iter_order_forward(arr):
    for i in iter_forward(len(arr)):
        yield arr[i]


def iter_order_backward(arr):
    for i in iter_backward(len(arr)):
        yield arr[i]


def freeze(arr):
    ''' Return a CFBS-ordered copy of arr.

        We're *allowed* to munge arr in place, but I haven't figured out how.
    '''
    arr = make_order(arr)
    return arr


def _do_search(arr, item):
    len_arr = len(arr)
    if not len_arr:
        return None
    rv = 0
    while True:
        if item < arr[rv]:
            tmp = left_child(rv)
            if tmp < len_arr:
                rv = tmp
                continue
            return predecessor(rv, len_arr)
        elif arr[rv] < item:
            tmp = right_child(rv)
            if tmp < len_arr:
                rv = tmp
                continue
            return rv
        else:
            return rv


def search(arr, item):
    ''' Return the index where the item might be.
    '''
    rv = _do_search(arr, item)
    if rv is None:
        rv = -1
    assert rv == -1 or arr[rv] <= item, rv
    # Note: successor(-1, i) == first(i), except when i == 0
    assert len(arr) == 0 or successor(rv, len(arr)) is None or item < arr[successor(rv, len(arr))], rv
    return rv
