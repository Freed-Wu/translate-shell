"""Fake errors
==============
"""
try:
    from errors import *  # type: ignore
except ImportError:
    from .__main__ import *
