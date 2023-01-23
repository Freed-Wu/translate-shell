"""Fake rich
============
"""
try:
    # skipcq: PYL-W0622
    from rich import *  # type: ignore
except ImportError:
    from .__main__ import *
