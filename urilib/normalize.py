import collections
from .compose import uricompose
from .split import urisplit, querylist
from unicodedata import normalize as unicodenormalize

_default_port = {
    'http': 80,
    'itms': 80,
    'ws': 80,
    'https': 443,
    'wss': 443,
    'gopher': 70,
    'news': 119,
    'snews': 563,
    'nntp': 119,
    'snntp': 563,
    'ftp': 21,
    'telnet': 23,
    'prospero': 191,
}

def _unicodenormalize(ustr, method='NFC'):
    if isinstance(ustr, bytes):
        return unicodenormalize(method, ustr.decode('utf-8')).encode('utf-8')
    else:
        return unicodenormalize(method, ustr)

def urinormalize(uri):
    """Normalize URIs"""
    if isinstance(uri, bytes):
        DOT = b'.'
        SLASH = b'/'
    else:
        DOT = '.'
        SLASH = '/'
    result = urisplit(uri)
    scheme = result.getscheme()
    userinfo = result.getuserinfo()
    if userinfo:
        userinfo = _unicodenormalize(userinfo)
    host = result.gethost()
    if isinstance(host, collections.Iterable) and host[-1] == DOT:
        host = host[:-1]
    port = result.getport()
    if scheme and port and port == _default_port.get(scheme, None):
        port = None
    path = result.getpath()
    if path:
        path = _unicodenormalize(path)
    else:
        path = SLASH
    query = result.query
    if query:
        qsl = querylist(_unicodenormalize(query))
    else:
        qsl = None
    fragment = result.getfragment()
    if fragment:
        fragment = _unicodenormalize(fragment)
    return uricompose(scheme=scheme, path=path, query=qsl, fragment=fragment,
                      userinfo=userinfo, host=host, port=port)
