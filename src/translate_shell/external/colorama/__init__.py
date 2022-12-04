"""Fake colorama
================
"""
try:
    from colorama import *  # type: ignore
except ImportError:
    from .__main__ import *
