__all__ = [ 'get_context_name', 'set_context_name', 'hackide_root', 'script_name', 'script_version' ]

import sys

script_name = len(sys.argv)>1 and sys.argv[1] or sys.argv[0]
script_version = "0.1beta!"

_context_name = None


def set_context_name(pn):
    global _context_name
    _context_name = pn
    return pn

def get_context_name():
    return _context_name

hackide_root = '/'.join(sys.path[0].split('/')[:-1])

