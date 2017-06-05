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


import unittest

from o11c.enums import ErrorBoolType, ErrorBool
from o11c.exceptions import ProgrammerIsAnIdiotError


class TestErrorBool(unittest.TestCase):
    def test_id(self):
        assert ErrorBoolType() is ErrorBool

    def test_repr(self):
        assert repr(ErrorBool) == 'ErrorBool'

    def test_use(self):
        self.assertRaises(ProgrammerIsAnIdiotError, bool, ErrorBool)
