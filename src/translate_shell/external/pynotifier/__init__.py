"""Fake pynotifier
==================
"""
try:
    from pynotifier import *  # type: ignore
except ImportError:
    from .__main__ import *
