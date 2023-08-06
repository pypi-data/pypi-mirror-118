from functools import lru_cache
import uuid

from . import _except_return_none

@lru_cache()
@_except_return_none
def get_session_uuid():
    return str(uuid.uuid4())
