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


from .exceptions import ProgrammerIsAnIdiotError


class ErrorBoolType:
    def __new__(cls):
        return ErrorBool

    def __repr__(self):
        return 'ErrorBool'

    def __bool__(self):
        raise ProgrammerIsAnIdiotError('I should not be used as a bool!')


ErrorBool = object.__new__(ErrorBoolType)
