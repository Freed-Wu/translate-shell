"""Fake shtab
=============
"""
try:
    from shtab import *  # type: ignore
except ImportError:
    from .__main__ import *
