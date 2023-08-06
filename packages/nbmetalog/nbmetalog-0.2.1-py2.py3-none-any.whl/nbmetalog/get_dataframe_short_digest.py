from . import _except_return_none
from . import get_dataframe_full_digest

@_except_return_none
def get_dataframe_short_digest(df):
    return get_dataframe_full_digest(df)[:16]
