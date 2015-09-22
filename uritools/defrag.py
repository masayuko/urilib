import collections

from .encoding import uridecode


class DefragResult(collections.namedtuple('DefragResult', 'uri fragment')):
    """Class to hold :func:`uridefrag` results."""

    __slots__ = ()  # prevent creation of instance dictionary

    def geturi(self):
        """Return the recombined version of the original URI as a string."""
        fragment = self.fragment
        if fragment is None:
            return self.uri
        else:
            return self.uri + '#' + fragment

    def getfragment(self, default=None, encoding='utf-8', errors='replace'):
        """Return the decoded fragment identifier, or `default` if the
        original URI did not contain a fragment component.

        """
        fragment = self.fragment
        if fragment is not None:
            return uridecode(fragment, encoding, errors)
        else:
            return default


def uridefrag(uristring):
    """Remove an existing fragment component from a URI string."""
    parts = uristring.partition('#')
    return DefragResult(parts[0], parts[2] if parts[1] else None)
