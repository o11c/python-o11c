#   python-o11c - generic utilities library
#   Copyright © 2017-2018  Ben Longbons
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


import functools

from ..enums import Direction


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


def child(n, dir):
    assert n is not None
    return n * 2 + (1 + dir.value)
left_child = functools.partial(child, dir=Direction.LEFT)
right_child = functools.partial(child, dir=Direction.RIGHT)


def is_root(n):
    assert n is not None
    return n == 0


def is_child(n, dir):
    assert n is not None
    return n != 0 and n % 2 == (1 - dir.value)
is_left_child = functools.partial(is_child, dir=Direction.LEFT)
is_right_child = functools.partial(is_child, dir=Direction.RIGHT)


def has_child(n, sz, dir):
    assert n is not None
    return child(n, dir=dir) < sz
has_left_child = functools.partial(has_child, dir=Direction.LEFT)
has_right_child = functools.partial(has_child, dir=Direction.RIGHT)


def most_child(n, sz, dir):
    assert n is not None
    while has_child(n, sz, dir=dir):
        n = child(n, dir=dir)
    return n
leftmost_child = functools.partial(most_child, dir=Direction.LEFT)
rightmost_child = functools.partial(most_child, dir=Direction.RIGHT)


def adcessor(n, sz, dir):
    assert n is not None
    if has_child(n, sz, dir=dir):
        n = child(n, dir=dir)
        return most_child(n, sz, dir=dir.flipped())
    while True:
        if is_child(n, dir=dir.flipped()):
            return parent(n)
        if is_root(n):
            return None
        n = parent(n)
predecessor = functools.partial(adcessor, dir=Direction.LEFT)
successor = functools.partial(adcessor, dir=Direction.RIGHT)


def edge(sz, dir):
    if sz == 0:
        return None
    n = 0
    return most_child(n, sz, dir=dir)
first = functools.partial(edge, dir=Direction.LEFT)
last = functools.partial(edge, dir=Direction.RIGHT)


def iter_toward(sz, dir):
    n = edge(sz, dir=dir.flipped())
    while n is not None:
        yield n
        n = adcessor(n, sz, dir=dir)
iter_backward = functools.partial(iter_toward, dir=Direction.LEFT)
iter_forward = functools.partial(iter_toward, dir=Direction.RIGHT)


'''
Given an array in which we'd normally do a binary search:

    sorted_letters = 'abcdefghijklmno'
    ordered_letters = make_order(sorted_letters)
    assert cfbs_ordered_letters == list('hdlbfjnacegikmo')
    assert list(iter_order_forward(cfbs_ordered_letters)) == list(sorted_letters)

    The li'th element of sorted_letters is the pi'th element of ordered_letters.
'''

def to_physical_index_complete(li, sz):
    # adjust both starting position and stride until we get there
    # half_sz is the value if the first star
    # li/2 is how many stars to go over
    # each iteration, we forget about earlier values
    #
    # Note that the bit shifted-off from both `li` and `sz` is *always* a 1,
    # except for the final `li>>1` after the loop.
    #
    # li =    0  1  2  3  4  5   6  7   8  9  10 11  12 13  14
    # sz=15: [7, 3, 8, 1, 9, 4, 10, 0, 11, 5, 12, 2, 13, 6, 14]
    #         *     *     *      *      *      *      *      *
    #
    # li =       0     1     2      3      4      5      6
    # sz=7:  [   3,    1,    4,     0,     5,     2,     6    ]
    #            *           *             *             *
    #
    # li =             0            1             2
    # sz=3:  [         1,           0,            2,          ]
    #                  *                          *
    #
    # li =                          0
    # sz=1:  [                      0,                        ]
    #                               *
    assert ((sz + 1) & sz) == 0, 'sz+1 must be a power-of-2'
    assert 0 <= li < sz

    while li & 1:
        li >>= 1
        sz >>= 1
    return (sz>>1) + (li>>1)

def to_physical_index(li, sz):
    assert 0 <= li < sz

    bits = sz.bit_length()
    sz_completed = (1 << bits) - 1
    missing = sz_completed - sz
    assert 0 <= missing < sz <= sz_completed

    # `list(iter_forward(sz))` returns something like:
    #     [7, 3, 8, 1, 9, 4, 10, 0, 11, 5, 12, 2, 13, 6, 14]
    # with any out-of-bounds values simply skipped, like so:
    # sz\  0  1  2  3  4  5   6  7   8  9  10 11  12 13  14
    #  8: [7, 3,    1,    4,     0,     5,     2,     6,     ]  missing=7, adjust 2->3, 3->5, 4->7, 5->9, 6->11, 7->13
    #  9: [7, 3, 8, 1,    4,     0,     5,     2,     6,     ]  missing=6, adjust       4->5, 5->7, 6->9, 7->11, 8->13
    # 10: [7, 3, 8, 1, 9, 4,     0,     5,     2,     6,     ]  missing=5, adjust             6->7, 7->9, 8->11, 9->13
    # 11: [7, 3, 8, 1, 9, 4, 10, 0,     5,     2,     6,     ]  missing=4, adjust                   8->9, 9->11, 10->13
    # 12: [7, 3, 8, 1, 9, 4, 10, 0, 11, 5,     2,     6,     ]  missing=3, adjust                        10->11, 11->13
    # 13: [7, 3, 8, 1, 9, 4, 10, 0, 11, 5, 12, 2,     6,     ]  missing=2, adjust                                12->13
    # 14: [7, 3, 8, 1, 9, 4, 10, 0, 11, 5, 12, 2, 13, 6,     ]  missing=1, no real adjust (14->undef)
    # 15: [7, 3, 8, 1, 9, 4, 10, 0, 11, 5, 12, 2, 13, 6, 14, ]  missing=0, never adjust (perfect)
    # Given an `sz` value, we know both how many and *which* values are skipped.
    adjustment_base = sz - missing
    adjustment_diff = li - adjustment_base
    if adjustment_diff >= 0:
        li += adjustment_diff
    return to_physical_index_complete(li, sz_completed)

def to_logical_index_complete(pi, sz):
    '''
    Inverse function of:

        while li & 1:
            li >>= 1
            sz >>= 1
        return (sz>>1) + (li>>1)

    This is invertible because (sz>>1)+1 shares no bits with (li>>1), and we
    always know what bit was shifted off.
    '''
    assert ((sz + 1) & sz) == 0, 'sz+1 must be a power-of-2'
    assert 0 <= pi < sz

    sz_goal_plus_1 = sz + 1

    # with (true) sz == 15:
    # if 7 <= pi <= 14, then bits=4
    bits = (pi+1).bit_length()
    # if bits == 4, then sz>>1 == 7
    sz_plus_1 = (1 << (bits-1))         # (sz>>1)+1 in the return statement
    li = pi+1 - sz_plus_1               # li>>1 in the return statement

    sz_plus_1 <<= 1                     # sz+1 in the return statement
    li <<= 1                            # li in the return statement
    li_plus_1 = li + 1; del li

    while sz_plus_1 != sz_goal_plus_1:
        # i.e. sz = (sz << 1) | 1
        sz_plus_1 <<= 1
        li_plus_1 <<= 1

    return li_plus_1 - 1

def to_logical_index(pi, sz):
    assert 0 <= pi < sz

    bits = sz.bit_length()
    sz_completed = (1 << bits) - 1
    missing = sz_completed - sz
    assert 0 <= missing < sz <= sz_completed

    li = to_logical_index_complete(pi, sz_completed)
    adjustment_base = sz - missing
    adjustment_diff_2 = li - adjustment_base
    if adjustment_diff_2 >= 0:
        assert (adjustment_diff_2 & 1) == 0
        li -= adjustment_diff_2>>1
    return li


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
