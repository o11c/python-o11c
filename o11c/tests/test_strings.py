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

from o11c.strings import u2b, b2u


class TestStrings(unittest.TestCase):
    def test_u2b(self):
        assert u2b(u'') == b''
        assert u2b(u'Hello, World!') == b'Hello, World!'

        assert u2b(u'\u0000') == b'\x00'
        assert u2b(u'\u007f') == b'\x7f'
        assert u2b(u'\u0080') == b'\xc2\x80'
        assert u2b(u'\u07ff') == b'\xdf\xbf'
        assert u2b(u'\u0800') == b'\xe0\xa0\x80'
        assert u2b(u'\uffff') == b'\xef\xbf\xbf'
        assert u2b(u'\U00010000') == b'\xf0\x90\x80\x80'
        assert u2b(u'\U0010ffff') == b'\xf4\x8f\xbf\xbf'

        with self.assertRaises(UnicodeEncodeError):
            u2b(u'\ud800')
        with self.assertRaises(UnicodeEncodeError):
            u2b(u'\udbff')

        with self.assertRaises(UnicodeEncodeError):
            u2b(u'\udc00')
        with self.assertRaises(UnicodeEncodeError):
            u2b(u'\udc7f')
        assert u2b(u'\udc80') == b'\x80'
        assert u2b(u'\udcff') == b'\xff'

        with self.assertRaises(UnicodeEncodeError):
            u2b(u'\udd00')
        with self.assertRaises(UnicodeEncodeError):
            u2b(u'\udfff')

    def test_b2u(self):
        assert b2u(b'') == u''
        assert b2u(b'Hello, World!') == u'Hello, World!'

        assert b2u(b'\x00') == u'\u0000'
        assert b2u(b'\x7f') == u'\u007f'
        assert b2u(b'\xc2\x80') == u'\u0080'
        assert b2u(b'\xdf\xbf') == u'\u07ff'
        assert b2u(b'\xe0\xa0\x80') == u'\u0800'
        assert b2u(b'\xef\xbf\xbf') == u'\uffff'
        assert b2u(b'\xf0\x90\x80\x80') == u'\U00010000'
        assert b2u(b'\xf4\x8f\xbf\xbf') == u'\U0010ffff'

        assert b2u(b'\x80') == u'\udc80'
        assert b2u(b'\xff') == u'\udcff'
