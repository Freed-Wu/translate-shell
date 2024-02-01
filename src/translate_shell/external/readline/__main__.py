#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.

Because Windows don't have
`readline <https://docs.python.org/3/library/readline.html>`_.
"""

from collections.abc import Callable


def read_history_file(unused_path: str) -> None:
    """Read history file.

    :param unused_path:
    :type unused_path: str
    :rtype: None
    """


def write_history_file(unused_path: str) -> None:
    """Write history file.

    :param unused_path:
    :type unused_path: str
    :rtype: None
    """


def set_completer_delims(delims: str) -> None:
    """Set completer delims.

    :param delims:
    :type delims: str
    :rtype: None
    """


def set_completer(completer: Callable[[str, int], str]) -> None:
    """Set completer.

    :param completer:
    :type completer: Callable[[str, int], str]
    :rtype: None
    """


def add_history(unused_path: str) -> None:
    """Add history.

    :param unused_path:
    :type unused_path: str
    :rtype: None
    """


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
