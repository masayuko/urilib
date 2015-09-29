import ipaddress
import numbers
import re

from collections import Iterable, Mapping

from .chars import SUB_DELIMS
from .encoding import uriencode, uriencode_plus, idnencode
from .split import uriunsplit

# RFC 3986 3.1: scheme = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )
_SCHEME_RE = re.compile(r"\A[A-Za-z][A-Za-z0-9+.-]*\Z")

# RFC 3986 3.2: authority = [ userinfo "@" ] host [ ":" port ]
_AUTHORITY_RE_STRING = re.compile(r"\A(?:(.*)@)?(.*?)(?::([0-9]*))?\Z")

def _scheme(scheme):
    if not scheme:
        return None
    if _SCHEME_RE.match(scheme):
        return scheme.lower()
    else:
        raise ValueError('Invalid scheme component')


def _authority(userinfo, host, port, encoding):
    authority = []

    if userinfo is not None:
        authority.append(uriencode(userinfo, ':', encoding))
        authority.append('@')

    if host is not None and host != '':
        if isinstance(host, ipaddress.IPv6Address):
            if isinstance('', bytes):
                iphost = host.compressed.encode('ascii')
            else:
                iphost = host.compressed
            authority.append('[' + iphost + ']')
        elif isinstance(host, ipaddress.IPv4Address):
            if isinstance('', bytes):
                iphost = host.compressed.encode('ascii')
            else:
                iphost = host.compressed
            authority.append(iphost)
        else:
            authority.append(_host(host))

    if isinstance(port, numbers.Number):
        authority.append(_port(str(port)))
    elif isinstance(port, type('')):
        authority.append(_port(port))

    return ''.join(authority) if authority else None


def _ip_literal(address):
    if address.startswith('v'):
        raise ValueError('Address mechanism not supported')
    else:
        if isinstance(address , bytes):
            address = address.decode('utf-8')
            iphost = ipaddress.IPv6Address(address).compressed.encode('ascii')
        else:
            iphost = ipaddress.IPv6Address(address).compressed
        return '[' + iphost + ']'


def _host(host):
    # RFC 3986 3.2.3: Although host is case-insensitive, producers and
    # normalizers should use lowercase for registered names and
    # hexadecimal addresses for the sake of uniformity, while only
    # using uppercase letters for percent-encodings.
    if host.startswith('[') and host.endswith(']'):
        return _ip_literal(host[1:-1])
    # check for IPv6 addresses as returned by SplitResult.gethost()
    try:
        return _ip_literal(host)
    except ValueError:
        return idnencode(host)


def _port(port):
    # RFC 3986 3.2.3: URI producers and normalizers should omit the
    # port component and its ":" delimiter if port is empty or if its
    # value would be the same as that of the scheme's default.
    if port.lstrip('0123456789'):
        raise ValueError('Invalid port subcomponent')
    elif port:
        return ':' + port
    else:
        return ''


def _querylist(items, encoding='utf-8', safe=''):
    if len(items) == 0:
        return None
    terms = []
    append = terms.append
    for key, value in items:
        name = uriencode_plus(key, safe, encoding)
        if value is None:
            append(name)
        else:
            if isinstance(value, numbers.Number):
                value = str(value)
            elif not isinstance(value, type('')):
                value.encode(encoding)
            append(name + '=' + uriencode_plus(value, safe, encoding))
    return '&'.join(terms)


def _querydict(mapping, encoding='utf-8', safe=''):
    items = []
    for key, value in mapping.items():
        if isinstance(value, type('')):
            items.append((key, value))
        elif isinstance(value, Iterable):
            items.extend([(key, v) for v in value])
        else:
            items.append((key, value))
    return _querylist(items, encoding, safe)


def uricompose(scheme=None, authority=None, path='', query=None,
               fragment=None, userinfo=None, host=None, port=None,
               encoding='utf-8'):
    """Compose a URI string from its individual components."""

    # RFC 3986 3.1: Scheme names consist of a sequence of characters
    # beginning with a letter and followed by any combination of
    # letters, digits, plus ("+"), period ("."), or hyphen ("-").
    # Although schemes are case-insensitive, the canonical form is
    # lowercase and documents that specify schemes must do so with
    # lowercase letters.  An implementation should accept uppercase
    # letters as equivalent to lowercase in scheme names (e.g., allow
    # "HTTP" as well as "http") for the sake of robustness but should
    # only produce lowercase scheme names for consistency.
    scheme = _scheme(scheme)

    # authority must be string type or three-item iterable
    if authority is None:
        authority = (None, None, None)
    #elif isinstance(authority, bytes):
    #    authority = _AUTHORITY_RE_BYTES.match(authority).groups()
    elif isinstance(authority, type('')):
        authority = _AUTHORITY_RE_STRING.match(authority).groups()
    elif not isinstance(authority, Iterable):
        raise TypeError('Invalid authority type')
    elif len(authority) != 3:
        raise ValueError('Invalid authority length')
    authority = _authority(
        userinfo if userinfo is not None else authority[0],
        host if host is not None else authority[1],
        port if port is not None else authority[2],
        encoding
    )

    # RFC 3986 3.3: If a URI contains an authority component, then the
    # path component must either be empty or begin with a slash ("/")
    # character.  If a URI does not contain an authority component,
    # then the path cannot begin with two slash characters ("//").
    path = uriencode(path, '/:@+,', encoding)
    if authority is not None and path and not path.startswith('/'):
        raise ValueError('Invalid path with authority component')
    if authority is None and path.startswith('//'):
        raise ValueError('Invalid path without authority component')

    # RFC 3986 4.2: A path segment that contains a colon character
    # (e.g., "this:that") cannot be used as the first segment of a
    # relative-path reference, as it would be mistaken for a scheme
    # name.
    if scheme is None and authority is None and not path.startswith('/'):
        if ':' in path.partition('/')[0]:
            path = '/' + path

    # RFC 3986 3.4: The characters slash ("/") and question mark ("?")
    # may represent data within the query component.  Beware that some
    # older, erroneous implementations may not handle such data
    # correctly when it is used as the base URI for relative
    # references (Section 5.1), apparently because they fail to
    # distinguish query data from path data when looking for
    # hierarchical separators.  However, as query components are often
    # used to carry identifying information in the form of "key=value"
    # pairs and one frequently used value is a reference to another
    # URI, it is sometimes better for usability to avoid percent-
    # encoding those characters.
    if isinstance(query, type('')) and query:
        query = uriencode_plus(query, '=&;@,', encoding)
    elif isinstance(query, Mapping):
        query = _querydict(query, encoding)
    elif isinstance(query, Iterable):
        query = _querylist(query, encoding)
    elif query is not None:
        raise TypeError('Invalid query type')

    # RFC 3986 3.5: The characters slash ("/") and question mark ("?")
    # are allowed to represent data within the fragment identifier.
    # Beware that some older, erroneous implementations may not handle
    # this data correctly when it is used as the base URI for relative
    # references.
    if fragment is not None:
        fragment = uriencode_plus(fragment, '@,', encoding)

    return uriunsplit((scheme, authority, path, query, fragment))
