"""Fake platformdirs
====================
"""
try:
    from platformdirs import *  # type: ignore
except ImportError:
    from .__main__ import *
