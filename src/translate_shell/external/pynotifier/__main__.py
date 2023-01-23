#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.
"""
import logging as _logging
from typing import Any

_logger = _logging.getLogger(__name__)


class Notification:
    """Notification."""

    def __init__(self, *args: Any) -> None:
        """Init.

        :param args:
        :type args: Any
        :rtype: None
        """

    @staticmethod
    def send() -> None:
        """Send.

        :rtype: None
        """
        _logger.error("Please install pynotifier firstly!")


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
