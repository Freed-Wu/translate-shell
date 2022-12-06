"""Fake rich.logging
====================
"""
try:
    from rich.logging import *  # type: ignore
except ImportError:
    from .__main__ import *
