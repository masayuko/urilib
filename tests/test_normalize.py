# -*- coding: utf-8 -*-
import unittest

from uritools import urinormalize


class NormalizeTest(unittest.TestCase):

    def check(self, good, **kwargs):
        result = urinormalize(**kwargs)
        self.assertEqual(good, result, msg='%r != %r (kwargs=%r)' % (
            result, good, kwargs)
        )


    def test_scheme(self):
        cases = [
            ('http://www.thedraymin.co.uk:/main/?p=308', 'http://www.thedraymin.co.uk/main/?p=308'), # empty port
            ('http://www.foo.com:80/foo', 'http://www.foo.com/foo'),
            ('http://www.foo.com:8000/foo', 'http://www.foo.com:8000/foo'),
            ('http://www.foo.com./foo/bar.html', 'http://www.foo.com/foo/bar.html'),
            ('http://www.foo.com.:81/foo', 'http://www.foo.com:81/foo'),
            ('http://www.foo.com/%7ebar', 'http://www.foo.com/~bar'),
            ('http://www.foo.com/%7Ebar', 'http://www.foo.com/~bar'),
            ('ftp://user:pass@ftp.foo.net/foo/bar', 'ftp://user:pass@ftp.foo.net/foo/bar'),
            ('http://USER:pass@www.Example.COM/foo/bar', 'http://USER:pass@www.example.com/foo/bar'),
            ('http://www.example.com./', 'http://www.example.com/'),
            ('http://test.example/?a=%26&b=1', 'http://test.example/?a=%26&b=1'), # should not un-encode the & that is part of a parameter value
            (u'http://test.example/?a=%e3%82%82%26', u'http://test.example/?a=%E3%82%82%26'), # should return a unicode character
            # note: this breaks the internet for parameters that are positional (stupid nextel) and/or don't have an = sign
            # 'http://test.example/?a=1&b=2&a=3': 'http://test.example/?a=1&a=3&b=2', # should be in sorted/grouped order

            # 'http://s.xn--q-bga.de/':       'http://s.q\xc3\xa9.de/'.decode('utf-8'), # should be in idna format
            ('http://test.example/?', 'http://test.example/'), # no trailing ?
            ('http://test.example?', 'http://test.example/'), # with trailing /
            ('http://a.COM/path/?b&a', 'http://a.com/path/?b&a'),
            # test utf8 and unicode
            (u'http://XBLAのXbox.com', u'http://xn--xblaxbox-jf4g.com/'),
            #(u'http://XBLAのXbox.com'.encode('utf-8'), b'http://xn--xblaxbox-jf4g.com/'),
            ('http://XBLAのXbox.com', 'http://xn--xblaxbox-jf4g.com/'),
            # test idna + utf-8 domain
            # u'http://xn--q-bga.XBLA\u306eXbox.com'.encode('utf-8'): b'http://q\xc3\xa9.xbla\xe3\x81\xaexbox.com'.decode('utf-8'),
            ('http://ja.wikipedia.org/wiki/%E3%82%AD%E3%83%A3%E3%82%BF%E3%83%94%E3%83%A9%E3%83%BC%E3%82%B8%E3%83%A3%E3%83%91%E3%83%B3', 'http://ja.wikipedia.org/wiki/%E3%82%AD%E3%83%A3%E3%82%BF%E3%83%94%E3%83%A9%E3%83%BC%E3%82%B8%E3%83%A3%E3%83%91%E3%83%B3'),
            ('http://test.example/キ', 'http://test.example/%E3%82%AD'),

            # check that %23 (#) is not escaped where it shouldn't be
            ('http://test.example/?p=%23val#test-%23-val%25', 'http://test.example/?p=%23val#test-%23-val%25'),
            # check that  %25 is not unescaped to %. %20 is to '+'
            ('http://test.example/%25/?p=%20val%20%25', 'http://test.example/%25/?p=+val+%25'),
            ("http://test.domain/I%C3%B1t%C3%ABrn%C3%A2ti%C3%B4n%EF%BF%BDliz%C3%A6ti%C3%B8n", "http://test.domain/I%C3%B1t%C3%ABrn%C3%A2ti%C3%B4n%EF%BF%BDliz%C3%A6ti%C3%B8n"),
            # check that spaces in paths are not eunscaped
            ('http://test.example/abcde%20def', 'http://test.example/abcde%20def'),
            ("http://test.example/path/with a%20space+/", "http://test.example/path/with%20a%20space+/"),
            ("http://[2001:db8:1f70::999:de8:7648:6e8]/test", "http://[2001:db8:1f70:0:999:de8:7648:6e8]/test"), #ipv6 address
            # not supported
            #("http://[::ffff:192.168.1.1]/test", "http://[::ffff:192.168.1.1]/test"), # ipv4 address in ipv6 notation
            #("http://[::ffff:192.168.1.1]:80/test", "http://[::ffff:192.168.1.1]/test"), # ipv4 address in ipv6 notation
            #("htTps://[::fFff:192.168.1.1]:443/test", "https://[::ffff:192.168.1.1]/test"), # ipv4 address in ipv6 notation

            ('http://localhost/', 'http://localhost/'),
            ('http://localhost:8080/', 'http://localhost:8080/'),
            ('homefeedapps://pinterest/', 'homefeedapps://pinterest/'), # can handle Android deep link
            ('mailto:me@pinterest.com', 'mailto:me@pinterest.com'), # can handle mailto:
            ("itms://itunes.apple.com/us/app/touch-pets-cats/id379475816?mt=8#23161525,,1293732683083,260430,tw", "itms://itunes.apple.com/us/app/touch-pets-cats/id379475816?mt=8#23161525,,1293732683083,260430,tw"), #can handle itms://
            ("http://example.com/../foo", "http://example.com/foo"),
            ("http://example.com//foo/../../bar", "http://example.com/bar"),
            ("http://example.com/../foo/../bar/../baz", "http://example.com/baz")
        ]
        for uri, good in cases:
            self.check(good, uri=uri)
