import re
from string import hexdigits

from .chars import UNRESERVED

if isinstance(chr(0), bytes):
    _fromint = chr
else:
    _fromint = lambda i: bytes([i])


# RFC 3986 2.1: For consistency, URI producers and normalizers should
# use uppercase hexadecimal digits for all percent-encodings.
def _pctenc(byte):
    return ('%%%02X' % byte).encode('ascii')

_unreserved = frozenset(memoryview(UNRESERVED.encode('ascii')).tolist())

_encoded = {
    b'': [_fromint(i) if i in _unreserved else _pctenc(i) for i in range(256)]
}


def uriencode(uristring, safe='', encoding='utf-8', errors='strict'):
    """Encode a URI string or string component."""
    if isinstance(uristring, bytes):
        values = memoryview(uristring).tolist()
    else:
        values = memoryview(uristring.encode(encoding, errors)).tolist()
    if not isinstance(safe, bytes):
        safe = safe.encode('ascii')
    try:
        encode = _encoded[safe].__getitem__
    except KeyError:
        enclist = _encoded[b''][:]
        for i in memoryview(safe).tolist():
            enclist[i] = _fromint(i)
        _encoded[safe] = enclist
        encode = enclist.__getitem__
    if isinstance(uristring, bytes):
        return b''.join(map(encode, values))
    else:
        return b''.join(map(encode, values)).decode(encoding)


def uriencode_plus(uristring, safe='', encoding='utf-8', errors='strict'):
    """Encode a URI string or string component. Replace space with plus."""
    if isinstance(safe, bytes):
        safe = safe + b' '
    else:
        safe = safe + ' '
    encode = uriencode(uristring, safe, encoding, errors)
    if isinstance(uristring, bytes):
        return re.sub(b' ', b'+', encode)
    else:
        return re.sub(' ', '+', encode)


def uridecode(uristring, encoding='utf-8', errors='strict'):
    """Decode a URI string or string component."""
    if isinstance(uristring, bytes):
        parts = uristring.split(b'%')
    else:
        parts = uristring.encode('utf-8', errors).split(b'%')
    bary = bytearray(parts[0])
    for s in parts[1:]:
        if len(s) < 2:
            bary.append(b'%'[0])
            bary.extend(s)
        else:
            try:
                raw = int(s[:2], 16)
                if raw < 256:
                    raw_chr = chr(raw)
                    bary.append(raw)
                    bary.extend(s[2:])
                else:
                    bary.append(b'%'[0])
                    bary.extend(s)
            except:
                bary.append(b'%'[0])
                bary.extend(s)
    if isinstance(uristring, bytes):
        #return bytes(bary)
        return bary.decode(encoding, errors).encode(encoding)
    else:
        return bary.decode(encoding, errors)


def uridecode_safe(uristring, encoding='utf-8', errors='replace'):
    """Decode a URI string or string component. Prefer to be safe."""
    if isinstance(uristring, bytes):
        parts = uristring.split(b'%')
    else:
        parts = uristring.encode('utf-8', errors).split(b'%')
    bary = bytearray(parts[0])
    for s in parts[1:]:
        if len(s) < 2:
            bary.append(b'%'[0])
            bary.extend(s)
        else:
            try:
                raw = int(s[:2], 16)
                if raw < 32:
                    bary.append(b'%'[0])
                    bary.extend(s[:2].upper())
                    bary.extend(s[2:])
                elif raw < 256:
                    raw_chr = chr(raw)
                    bary.append(raw)
                    bary.extend(s[2:])
                else:
                    bary.append(b'%'[0])
                    bary.extend(s)
            except:
                bary.append(b'%'[0])
                bary.extend(s)
    if isinstance(uristring, bytes):
        return bary.decode(encoding, errors).encode(encoding)
    else:
        return bary.decode(encoding, errors)


def uridecode_plus(uristring, encoding='utf-8', errors='strict'):
    """Decode a URI string or string component. Replace plus with space."""
    if isinstance(uristring, bytes):
        uristring = re.sub(b'\+', b' ', uristring)
    else:
        uristring = re.sub('\+', ' ', uristring)
    return uridecode(uristring, encoding, errors)


def uridecode_safe_plus(uristring, encoding='utf-8', errors='replace'):
    """
    Decode a URI string or string component. Replace plus with space.
    Prefer to safe.
    """
    if isinstance(uristring, bytes):
        uristring = re.sub(b'\+', b' ', uristring)
    else:
        uristring = re.sub('\+', ' ', uristring)
    return uridecode_plus(uristring, encoding, errors)


def idnencode(domain, encoding='utf-8', errors='strict'):
    """Encode International domain string."""
    if not isinstance(domain, bytes):
        return domain.encode('idna', errors).decode(encoding)
    else:
        return domain.decode(encoding, errors).encode('idna', errors)


def idndecode(domain, encoding='utf-8', errors='strict'):
    """Decode International domain string."""
    if not isinstance(domain, bytes):
        return domain.encode('idna').decode('idna', errors)
    else:
        return domain.decode(encoding, errors).encode('idna').decode('idna', errors).encode(encoding, errors)
