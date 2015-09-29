from .split import urisplit


def urijoin(base, ref, strict=False):
    """Convert a URI reference relative to a base URI to its target URI
    string.

    """
    return urisplit(base).transform(ref, strict).geturi()
