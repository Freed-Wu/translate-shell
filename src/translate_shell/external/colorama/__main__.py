#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.
"""


def init() -> None:
    """init.

    :rtype: None
    """
    pass


class _Colorama:
    """_Colorama."""

    def __getattribute__(self, _: str) -> str:
        """__getattribute__.

        :param _:
        :type _: str
        :rtype: str
        """
        return ""


Fore = Back = Style = _Colorama()


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
