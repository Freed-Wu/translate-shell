"""Fake langdetect
==================
"""
try:
    from langdetect import *  # type: ignore
except ImportError:
    from .__main__ import *
