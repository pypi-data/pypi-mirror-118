#!/usr/bin/env python

'''
`dub` tests for `nbmetalog` package.
'''

import pytest

from nbmetalog import nbmetalog as nbm

def test_print_metadata():
    nbm.print_metadata()
