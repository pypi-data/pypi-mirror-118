import sys

from . import _except_return_none

@_except_return_none
def get_interpreter():
    return sys.version.replace('\n', ' ').strip()
