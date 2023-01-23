#!/usr/bin/env python
"""Fake logging."""
from logging import Handler
from typing import Any


class RichHandler(Handler):  # skipcq: PY-A6006
    """RichHandler."""

    def __init__(self, **kwargs: Any) -> None:
        """Init.

        :param kwargs:
        :type kwargs: Any
        :rtype: None
        """
        super().__init__()

    def emit(self, record: str) -> str:
        """Emit.

        :param record:
        :type record: str
        :rtype: str
        """
        return record


if __name__ == "__main__":
    from ...__main__ import main_once as _main

    _main(__file__, vars())
