#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.
"""
import logging as _logging

_logger = _logging.getLogger(__name__)


class _Keyring:
    """_Keyring."""

    def get_password(self, *args: str) -> str:
        """get_password.

        :param args:
        :type args: str
        :rtype: str
        """
        _logger.error("Please install keyring firstly!")
        return ""


def get_keyring() -> _Keyring:
    """get_keyring.

    :rtype: _Keyring
    """
    return _Keyring()


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
