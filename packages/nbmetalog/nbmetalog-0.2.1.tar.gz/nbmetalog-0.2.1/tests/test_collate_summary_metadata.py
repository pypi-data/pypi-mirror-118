#!/usr/bin/env python

'''
`dub` tests for `nbmetalog` package.
'''

from keyname import keyname as kn
import pytest

from nbmetalog import nbmetalog as nbm

def test_collate_summary_metadata():
    nbm.collate_summary_metadata()

def test_collate_outattr_metadata():
    for k, v in nbm.collate_outattr_metadata().items():
        first, *rest = k
        assert first == '_'
        if v is not None:
            assert kn.demote(v) == v
