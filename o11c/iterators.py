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


class MinIter:
    def __init__(self, *iterables):
        self._iterators = []
        self._values = []
        for iterable in iterables:
            iterator = iter(iterable)
            try:
                value = next(iterator)
            except StopIteration:
                continue
            self._iterators.append(iterator)
            self._values.append(value)

    def __iter__(self):
        return self

    def __next__(self):
        if not self._values:
            raise StopIteration
        idx = min(range(len(self._values)), key=lambda i: self._values[i])
        rv = self._values[idx]
        try:
            self._values[idx] = next(self._iterators[idx])
        except StopIteration:
            del self._iterators[idx]
            del self._values[idx]
        return rv
