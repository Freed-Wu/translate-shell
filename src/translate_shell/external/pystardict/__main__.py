#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.
"""
import logging as _logging

_logger = _logging.getLogger(__name__)


class Dictionary:
    """Dictionary."""

    def __init__(self, path: str) -> None:
        """__init__.

        :param path:
        :type path: str
        :rtype: None
        """
        _logger.error("Please install pyyaml firstly!")

    def get(self, text: str) -> str:
        """get.

        :param text:
        :type text: str
        :rtype: str
        """
        return ""


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
