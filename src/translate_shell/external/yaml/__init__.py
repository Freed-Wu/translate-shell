"""Fake yaml
============
"""
try:
    from yaml import *  # type: ignore
except ImportError:
    from .__main__ import *
