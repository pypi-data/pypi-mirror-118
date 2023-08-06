from datetime import datetime, timezone

from . import _except_return_none

@_except_return_none
def get_timestamp():
    return datetime.now().replace(
        tzinfo=timezone.utc,
    ).replace(
        microsecond=0,
    ).isoformat().replace('+', 'Z')
