#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.

Because Windows don't have
`readline <https://docs.python.org/3/library/readline.html>`_.
"""


def read_history_file(unused_path: str) -> None:
    """Read history file.

    :param unused_path:
    :type unused_path: str
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
