#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.
"""
import logging as _logging

_logger = _logging.getLogger(__name__)


class Dictionary:
    """Dictionary."""

    def __init__(self, unused_path: str) -> None:
        """Init.

        :param unused_path:
        :type unused_path: str
        :rtype: None
        """
        _logger.error("Please install pystardict firstly!")

    @staticmethod
    def get(unused_text: str) -> str:
        """Get.

        :param unused_text:
        :type unused_text: str
        :rtype: str
        """
        return ""


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
