"""Fake rich.traceback
======================
"""
try:
    from rich.traceback import *  # type: ignore
except ImportError:
    from .__main__ import *
