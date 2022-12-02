"""Fake __init__
================
"""
try:
    from __init__ import *  # type: ignore
except ImportError:
    from .__main__ import *
