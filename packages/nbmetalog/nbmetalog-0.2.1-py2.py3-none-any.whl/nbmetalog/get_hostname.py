from functools import lru_cache
import socket

from . import _except_return_none

@lru_cache()
@_except_return_none
def get_hostname():
    return socket.gethostname()
