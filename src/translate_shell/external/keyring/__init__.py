"""Fake keyring
===============
"""
try:
    from keyring import *  # type: ignore
except ImportError:
    from .__main__ import *
