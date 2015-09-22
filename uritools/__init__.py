"""RFC 3986 compliant, Unicode-aware, scheme-agnostic replacement for
urlparse.

This module defines RFC 3986 compliant replacements for the most
commonly used functions of the Python 2.7 Standard Library
:mod:`urlparse` module.

"""

from .chars import GEN_DELIMS, RESERVED, SUB_DELIMS, UNRESERVED
from .compose import uricompose
from .defrag import DefragResult, uridefrag
from .encoding import (idndecode, idnencode, uriencode, uriencode_plus,
                       uridecode, uridecode_plus, uridecode_safe,
                       uridecode_safe_plus)
from .join import urijoin
from .normalize import urinormalize
from .split import SplitResult, querylist, urisplit, uriunsplit

__all__ = (
    'GEN_DELIMS',
    'RESERVED',
    'SUB_DELIMS',
    'UNRESERVED',
    'DefragResult',
    'SplitResult',
    'uricompose',
    'idndecode',
    'idnencode',
    'querylist',
    'uriencode',
    'uriencode_plus',
    'uridecode',
    'uridecode_safe',
    'uridecode_safe_plus',
    'uridefrag',
    'urijoin',
    'urinormalize',
    'urisplit',
    'uriunsplit'
)

__version__ = '1.0.1'
