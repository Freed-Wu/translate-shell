#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.
"""
import logging as _logging
import sys
from typing import Any, NoReturn

_logger = _logging.getLogger(__name__)


def dump(*args: Any, **kwargs: Any) -> NoReturn:
    """Dump.

    :param args:
    :type args: Any
    :param kwargs:
    :type kwargs: Any
    :rtype: NoReturn
    """
    _logger.error("Please install pyyaml firstly!")
    sys.exit(1)


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
