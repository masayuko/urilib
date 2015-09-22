# -*- coding: utf-8 -*-
import unittest

from uritools import urisplit


class SplitTest(unittest.TestCase):

    def check(self, uri, parts):
        result = urisplit(uri)
        self.assertEqual(result, parts, 'Error parsing %r' % uri)
        self.assertEqual(result.geturi(), uri, 'Error recomposing %r' % uri)

    def test_rfc3986(self):
        """urisplit test cases from [RFC3986] 3. Syntax Components"""
        cases = [
            ('foo://example.com:8042/over/there?name=ferret#nose',
             ('foo', 'example.com:8042', '/over/there', 'name=ferret',
              'nose')),
            ('urn:example:animal:ferret:nose',
             ('urn', None, 'example:animal:ferret:nose', None, None)),
        ]
        for uri, parts in cases:
            self.check(uri, parts)

    def test_idn(self):
        """international domain name"""
        cases = [
            ('https://xn--gckc5l.xn--fsq.jp/%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA/%E3%83%91%E3%82%B9?%E5%A4%89%E6%95%B0=%E5%80%A4#%E3%83%95%E3%83%A9%E3%82%B0%E3%83%A1%E3%83%B3%E3%83%88',
             ('https', 'xn--gckc5l.xn--fsq.jp', '/%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA/%E3%83%91%E3%82%B9', '%E5%A4%89%E6%95%B0=%E5%80%A4',
              '%E3%83%95%E3%83%A9%E3%82%B0%E3%83%A1%E3%83%B3%E3%83%88')),
        ]
        for uri, parts in cases:
            result = urisplit(uri)
            self.assertEqual(result, parts, 'Error parsing %r' % uri)
            self.assertEqual(result.geturi(), uri, 'Error recomposing %r' % uri)
            self.assertEqual(result.getscheme(), 'https')
            self.assertEqual(result.gethost(), 'ウェブ.例.jp')
            self.assertEqual(result.host, 'xn--gckc5l.xn--fsq.jp')
            self.assertEqual(result.getpath(), '/ディレクトリ/パス')
            self.assertEqual(result.path, '/%E3%83%87%E3%82%A3%E3%83%AC%E3%82%AF%E3%83%88%E3%83%AA/%E3%83%91%E3%82%B9')
            self.assertEqual(result.getquery(), '変数=値')
            self.assertEqual(result.query, '%E5%A4%89%E6%95%B0=%E5%80%A4')
            self.assertEqual(result.getquerydict(), {'変数': ['値']})
            self.assertEqual(result.getquerylist(), [('変数', '値')])
            self.assertEqual(result.getfragment(), 'フラグメント')
            self.assertEqual(result.fragment, '%E3%83%95%E3%83%A9%E3%82%B0%E3%83%A1%E3%83%B3%E3%83%88')

    def test_abnormal(self):
        cases = [
            ('', (None, None, '', None, None)),
            (':', (None, None, ':', None, None)),
            (':/', (None, None, ':/', None, None)),
            ('://', (None, None, '://', None, None)),
            ('://?', (None, None, '://', '', None)),
            ('://#', (None, None, '://', None, '')),
            ('://?#', (None, None, '://', '', '')),
            ('//', (None, '', '', None, None)),
            ('///', (None, '', '/', None, None)),
            ('//?', (None, '', '', '', None)),
            ('//#', (None, '', '', None, '')),
            ('//?#', (None, '', '', '', '')),
            ('?', (None, None, '', '', None)),
            ('??', (None, None, '', '?', None)),
            ('?#', (None, None, '', '', '')),
            ('#', (None, None, '', None, '')),
            ('##', (None, None, '', None, '#')),
        ]
        for uri, parts in cases:
            self.check(uri, parts)

    def test_members(self):
        uri = 'foo://user@example.com:8042/over/there?name=ferret#nose'
        result = urisplit(uri)
        self.assertEqual(result.scheme, 'foo')
        self.assertEqual(result.authority, 'user@example.com:8042')
        self.assertEqual(result.path, '/over/there')
        self.assertEqual(result.query, 'name=ferret')
        self.assertEqual(result.fragment, 'nose')
        self.assertEqual(result.userinfo, 'user')
        self.assertEqual(result.host, 'example.com')
        self.assertEqual(result.port, '8042')
        self.assertEqual(result.geturi(), uri)
        self.assertEqual(result.getscheme(), 'foo')
        self.assertEqual(result.getuserinfo(), 'user')
        self.assertEqual(result.gethost(), 'example.com')
        self.assertEqual(result.getport(), 8042)
        self.assertEqual(result.getpath(), '/over/there')
        self.assertEqual(result.getquery(), 'name=ferret')
        self.assertEqual(dict(result.getquerydict()), {'name': ['ferret']})
        self.assertEqual(list(result.getquerylist()), [('name', 'ferret')])
        self.assertEqual(result.getfragment(), 'nose')

        uri = 'urn:example:animal:ferret:nose'
        result = urisplit(uri)
        self.assertEqual(result.scheme, 'urn')
        self.assertEqual(result.authority, None)
        self.assertEqual(result.path, 'example:animal:ferret:nose')
        self.assertEqual(result.query, None)
        self.assertEqual(result.fragment, None)
        self.assertEqual(result.userinfo, None)
        self.assertEqual(result.host, None)
        self.assertEqual(result.port, None)
        self.assertEqual(result.geturi(), uri)
        self.assertEqual(result.getscheme(), 'urn')
        self.assertEqual(result.getuserinfo(), None)
        self.assertEqual(result.gethost(), None)
        self.assertEqual(result.getport(), None)
        self.assertEqual(result.getpath(), 'example:animal:ferret:nose')
        self.assertEqual(result.getquery(), None)
        self.assertEqual(dict(result.getquerydict()), {})
        self.assertEqual(list(result.getquerylist()), [])
        self.assertEqual(result.getfragment(), None)

        uri = 'file:///'
        result = urisplit(uri)
        self.assertEqual(result.scheme, 'file')
        self.assertEqual(result.authority, '')
        self.assertEqual(result.path, '/')
        self.assertEqual(result.query, None)
        self.assertEqual(result.fragment, None)
        self.assertEqual(result.userinfo, None)
        self.assertEqual(result.host, '')
        self.assertEqual(result.port, None)
        self.assertEqual(result.geturi(), uri)
        self.assertEqual(result.getscheme(), 'file')
        self.assertEqual(result.getuserinfo(), None)
        self.assertEqual(result.gethost(), '')
        self.assertEqual(result.getport(), None)
        self.assertEqual(result.getpath(), '/')
        self.assertEqual(result.getquery(), None)
        self.assertEqual(dict(result.getquerydict()), {})
        self.assertEqual(list(result.getquerylist()), [])
        self.assertEqual(result.getfragment(), None)

    def test_getscheme(self):
        self.assertEqual(urisplit('foo').getscheme(default='bar'), 'bar')
        self.assertEqual(urisplit('FOO_BAR:/').getscheme(), 'foo_bar')

    def test_gethost(self):
        from ipaddress import IPv4Address, IPv6Address
        cases = [
            ('http://Test.python.org:5432/foo/', 'test.python.org'),
            ('http://12.34.56.78:5432/foo/', IPv4Address(u'12.34.56.78')),
            ('http://[::1]:5432/foo/', IPv6Address(u'::1')),
        ]
        for uri, host in cases:
            self.assertEqual(urisplit(uri).gethost(), host)
        for uri in ['http://[::1/', 'http://::1]/']:
            with self.assertRaises(ValueError, msg='%r' % uri):
                urisplit(uri).gethost()

    def test_getport(self):
        for uri in ['foo://bar', 'foo://bar:', 'foo://bar/', 'foo://bar:/']:
            result = urisplit(uri)
            if result.authority.endswith(':'):
                self.assertEqual(result.port, '')
            else:
                self.assertEqual(result.port, None)
            self.assertEqual(result.gethost(), 'bar')
            self.assertEqual(result.getport(8000), 8000)

    def test_getpath(self):
        cases = [
            ('', '', '/'),
            ('.', './', '/'),
            ('./', './', '/'),
            ('./.', './', '/'),
            ('./..', '../', '/'),
            ('./foo', 'foo', '/foo'),
            ('./foo/', 'foo/', '/foo/'),
            ('./foo/.', 'foo/', '/foo/'),
            ('./foo/..', './', '/'),
            ('..', '../', '/'),
            ('../', '../', '/'),
            ('../.', '../', '/'),
            ('../..', '../../', '/'),
            ('../foo', '../foo', '/foo'),
            ('../foo/', '../foo/', '/foo/'),
            ('../foo/.', '../foo/', '/foo/'),
            ('../foo/..', '../', '/'),
            ('../../foo', '../../foo', '/foo'),
            ('../../foo/', '../../foo/', '/foo/'),
            ('../../foo/.', '../../foo/', '/foo/'),
            ('../../foo/..', '../../', '/'),
            ('../../foo/../bar', '../../bar', '/bar'),
            ('../../foo/../bar/', '../../bar/', '/bar/'),
            ('../../foo/../bar/.', '../../bar/', '/bar/'),
            ('../../foo/../bar/..', '../../', '/'),
            ('../../foo/../..', '../../../', '/')
        ]
        for uri, relpath, abspath in cases:
            parts = urisplit(uri)
            self.assertEqual(relpath, parts.getpath())
            parts = urisplit('/' + uri)
            self.assertEqual(abspath, parts.getpath())

    def test_getquery(self):
        cases = [
            ("?", [], {}),
            ("?&", [], {}),
            ("?&&", [], {}),
            ("?=",
             [('', '')],
             {'': ['']}),
            ("?=a",
             [('', 'a')],
             {'': ['a']}),
            ("?a",
             [('a', None)],
             {'a': [None]}),
            ("?a=",
             [('a', '')],
             {'a': ['']}),
            ("?&a=b",
             [('a', 'b')],
             {'a': ['b']}),
            ("?a=a+b&b=b+c",
             [('a', 'a b'), ('b', 'b c')],
             {'a': ['a b'], 'b': ['b c']}),
            ("?a=a%20b&b=b%20c",
             [('a', 'a b'), ('b', 'b c')],
             {'a': ['a b'], 'b': ['b c']}),
            ("?a=a%20+b&b=b%20+c",
             [('a', 'a  b'), ('b', 'b  c')],
             {'a': ['a  b'], 'b': ['b  c']}),
            ("?a=a%2B+b&b=b%2B+c",
             [('a', 'a+ b'), ('b', 'b+ c')],
             {'a': ['a+ b'], 'b': ['b+ c']}),
            ("?a=1&a=2",
             [('a', '1'), ('a', '2')],
             {'a': ['1', '2']}),
        ]
        for query, querylist, querydict in cases:
            self.assertEqual(urisplit(query).getquerylist(), querylist,
                             'Error parsing query dict for %r' % query)
            self.assertEqual(urisplit(query).getquerydict(), querydict,
                             'Error parsing query list for %r' % query)

    def test_ip_literal(self):
        cases = [
            ('http://Test.python.org:5432/foo/', 'test.python.org', 5432),
            ('http://12.34.56.78:5432/foo/', '12.34.56.78', 5432),
            ('http://[::1]:5432/foo/', '::1', 5432),
            ('http://[dead:beef::1]:5432/foo/', 'dead:beef::1', 5432),
            ('http://[dead:beef::]:5432/foo/', 'dead:beef::', 5432),
            ('http://[dead:beef:cafe:5417:affe:8FA3:deaf:feed]:5432/foo/',
             'dead:beef:cafe:5417:affe:8fa3:deaf:feed', 5432),
            ('http://[::12.34.56.78]:5432/foo/', '::c22:384e', 5432),
            ('http://[::ffff:12.34.56.78]:5432/foo/', '::ffff:c22:384e', 5432),
            ('http://Test.python.org/foo/', 'test.python.org', None),
            ('http://12.34.56.78/foo/', '12.34.56.78', None),
            ('http://[::1]/foo/', '::1', None),
            ('http://[dead:beef::1]/foo/', 'dead:beef::1', None),
            ('http://[dead:beef::]/foo/', 'dead:beef::', None),
            ('http://[dead:beef:cafe:5417:affe:8FA3:deaf:feed]/foo/',
             'dead:beef:cafe:5417:affe:8fa3:deaf:feed', None),
            ('http://[::12.34.56.78]/foo/', '::c22:384e', None),
            ('http://[::ffff:12.34.56.78]/foo/', '::ffff:c22:384e', None),
            ('http://Test.python.org:/foo/', 'test.python.org', None),
            ('http://12.34.56.78:/foo/', '12.34.56.78', None),
            ('http://[::1]:/foo/', '::1', None),
            ('http://[dead:beef::1]:/foo/', 'dead:beef::1', None),
            ('http://[dead:beef::]:/foo/', 'dead:beef::', None),
            ('http://[dead:beef:cafe:5417:affe:8FA3:deaf:feed]:/foo/',
             'dead:beef:cafe:5417:affe:8fa3:deaf:feed', None),
            ('http://[::12.34.56.78]:/foo/', '::c22:384e', None),
            ('http://[::ffff:12.34.56.78]:/foo/', '::ffff:c22:384e', None),
            ]
        for uri, host, port in cases:
            parts = urisplit(uri)
            self.assertEqual(host, str(parts.gethost()))
            self.assertEqual(port, parts.getport())

    def test_invalid_ip_literal(self):
        uris = [
            'http://::12.34.56.78]/',
            'http://[::1/foo/',
            'ftp://[::1/foo/bad]/bad',
            'http://[::1/foo/bad]/bad',
            'http://[foo]/',
            'http://[v7.future]'
        ]
        for uri in uris:
            with self.assertRaises(ValueError, msg='%r' % uri):
                urisplit(uri).gethost()
