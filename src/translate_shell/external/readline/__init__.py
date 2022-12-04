"""Fake readline
================
"""
try:
    from readline import *  # type: ignore
except ImportError:
    from .__main__ import *
