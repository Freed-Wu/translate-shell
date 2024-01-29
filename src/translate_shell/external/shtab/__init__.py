"""Fake shtab
=============
"""

try:
    from shtab import *  # type: ignore  # noqa: F403
except ImportError:
    from .__main__ import *  # noqa: F403
