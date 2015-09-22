# -*- coding: utf-8 -*-
import unittest

from uritools import (RESERVED, UNRESERVED, uriencode, uriencode_plus,
                      uridecode, uridecode_plus, uridecode_safe,
                      uridecode_safe_plus)


class EncodingTest(unittest.TestCase):

    def check(self, decoded, encoded, safe='', encoding='utf-8'):
        self.assertEqual(uriencode(decoded, safe, encoding), encoded)
        self.assertEqual(uridecode(encoded, encoding), decoded)

    def test_encoding(self):
        cases = [
            ('', ''),
            (' ', '%20'),
            ('%', '%25'),
            ('~', '~'),
            (UNRESERVED, UNRESERVED),
        ]
        for decoded, encoded in cases:
            self.check(decoded, encoded)

    def test_safe_encoding(self):
        cases = [
            ('', '', ''),
            (' ', ' ', ' '),
            ('%', '%', '%'),
            (RESERVED, RESERVED, RESERVED)
        ]
        for decoded, encoded, safe in cases:
            self.check(decoded, encoded, safe)

    def test_utf8_encoding(self):
        cases = [
            (u'ölkürbis', u'%C3%B6lk%C3%BCrbis'),
            (u'ölkürbis'.encode('utf-8'), b'%C3%B6lk%C3%BCrbis')
        ]
        for decoded, encoded in cases:
            self.check(decoded, encoded, encoding='utf-8')

    def test_latin1_encoding(self):
        cases = [
            (u'ölkürbis', u'%F6lk%FCrbis'),
            (u'ölkürbis'.encode('latin-1'), b'%F6lk%FCrbis'),
        ]
        for decoded, encoded in cases:
            self.check(decoded, encoded, encoding='latin-1')

    def test_decode_bytes(self):
        cases = [
            (u'%F6lk%FCrbis', u'ölkürbis'),
            (b'%F6lk%FCrbis', u'ölkürbis'.encode('iso-8859-1'))
        ]
        for input, output in cases:
            self.assertEqual(uridecode(input, encoding='iso-8859-1'), output)

    def test_uriencode(self):
        cases = [
            ('%', '%25'),
            ('あい', '%E3%81%82%E3%81%84'),
            ('あ い', '%E3%81%82%20%E3%81%84'),
        ]
        for input, output in cases:
            self.assertEqual(uriencode(input), output)

    def test_uriencode(self):
        cases = [
            ('%', '%25'),
            ('あい', '%E3%81%82%E3%81%84'),
            ('あ い', '%E3%81%82%20%E3%81%84'),
        ]
        for input, output in cases:
            self.assertEqual(uriencode(input), output)

    def test_uridecode(self):
        cases = [
            ('%', '%'),
            (b'%', b'%'),
            ('%ZZ', '%ZZ'),
            (b'%ZZ', b'%ZZ'),
            ('%Z', '%Z'),
            (b'%Z', b'%Z'),
            ('%Z%E3%81%82', '%Zあ'),
            ('%Z%E3%81%82a', '%Zあa')
        ]
        for input, output in cases:
            self.assertEqual(uridecode(input), output)

    def test_uridecode_safe(self):
        cases = [
            ('%', '%'),
            (b'%', b'%'),
            ('%ZZ', '%ZZ'),
            (b'%ZZ', b'%ZZ'),
            ('%Z', '%Z'),
            (b'%Z', b'%Z'),
            ('%Z%E3%81%82', '%Zあ'),
            ('%Z%E3%81%82a', '%Zあa'),
            ('%Z%19%E3%81%82', '%Z%19あ')
        ]
        for input, output in cases:
            self.assertEqual(uridecode_safe(input), output)

    def test_encode_bytes(self):
        cases = [
            (b'\xf6lk\xfcrbis', b'%F6lk%FCrbis')
        ]
        for input, output in cases:
            self.assertEqual(uriencode(input), output)
