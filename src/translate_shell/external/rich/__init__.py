"""Fake rich
============
"""
try:
    from rich import *  # type: ignore
except ImportError:
    from .__main__ import *
