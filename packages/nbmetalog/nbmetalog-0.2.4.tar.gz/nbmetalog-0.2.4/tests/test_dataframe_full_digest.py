#!/usr/bin/env python

'''
`dub` tests for `nbmetalog` package.
'''

import numpy as np
import pandas as pd
import pytest

from nbmetalog import nbmetalog as nbm

def test_dataframe_full_digest():
    df = pd.DataFrame({
         "A": 1.0,
         "B": pd.Timestamp("20130102"),
         "C": pd.Series(1, index=list(range(4)), dtype="float32"),
         "D": np.array([3] * 4, dtype="int32"),
         "E": pd.Categorical(["test", "train", "test", "train"]),
         "F": "foo",
    })
    assert \
        nbm.get_dataframe_full_digest(df) \
        == '8ebde3e7d75fee3e8a590c103b35d4c2c6646977c95fc824297874eb427c374e'
