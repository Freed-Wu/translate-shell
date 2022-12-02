#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.
"""
import logging as _logging
from typing import NoReturn

_logger = _logging.getLogger(__name__)


def dump(*args, **kwargs) -> NoReturn:
    """dump.

    :param args:
    :param kwargs:
    :rtype: NoReturn
    """
    _logger.error("Please install pyyaml firstly!")
    exit(1)


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
