urilib
========================================================================

This module is a fork of the uritools_.

This module defines replacements for the most commonly used functions of
the Python 2.7 Standard Library urlparse_ and Python 3 `urllib.parse`_ modules.

.. code-block:: pycon

    >>> from urilib import urisplit, uriunsplit, urijoin, uridefrag
    >>> parts = urisplit('foo://user@example.com:8042/over/there?name=ferret#nose')
    >>> parts
    SplitResult(scheme='foo', authority='user@example.com:8042',
                path='/over/there', query='name=ferret', fragment='nose')
    >>> parts.scheme
    'foo'
    >>> parts.authority
    'user@example.com:8042'
    >>> parts.userinfo
    'user'
    >>> parts.host
    'example.com'
    >>> parts.port
    '8042'
    >>> uriunsplit(parts[:3] + ('name=swallow&type=African', 'beak'))
    'foo://user@example.com:8042/over/there?name=swallow&type=African#beak'
    >>> urijoin('http://www.cwi.nl/~guido/Python.html', 'FAQ.html')
    'http://www.cwi.nl/~guido/FAQ.html'
    >>> uridefrag('http://pythonhosted.org/uritools/index.html#constants')
    DefragResult(uri='http://pythonhosted.org/uritools/index.html',
                 fragment='constants')


License
------------------------------------------------------------------------

Copyright (c) 2014, 2015 Thomas Kemmer.
Copyright (c) 2015 IGARASHI Masanao.

Licensed under the `MIT License`_.


.. _uritools: https://github.com/tkem/uritools
.. _urlparse: http://docs.python.org/2/library/urlparse.html
.. _urllib.parse: http://docs.python.org/3/library/urllib.parse.html
.. _Lib/urllib/parse.py: https://hg.python.org/cpython/file/3.4/Lib/urllib/parse.py

.. _MIT License: http://raw.github.com/masayuko/urilib/master/LICENSE
