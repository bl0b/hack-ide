__all__ = [ 'get_context_name', 'set_context_name' ]

_context_name = None


def set_context_name(pn):
    global _context_name
    _context_name = pn
    return pn

def get_context_name():
    return _context_name
