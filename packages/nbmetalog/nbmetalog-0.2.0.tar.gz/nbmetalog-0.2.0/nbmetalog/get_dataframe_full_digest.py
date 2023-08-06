import hashlib
import pandas as pd

from . import _except_return_none

@_except_return_none
def get_dataframe_full_digest(df):
    # adapted from https://stackoverflow.com/a/47800021
    return hashlib.sha256(
        pd.util.hash_pandas_object(df, index=True).values
    ).hexdigest()
