"""Fake pystardict
==================
"""
try:
    from pystardict import *  # type: ignore
except ImportError:
    from .__main__ import *
