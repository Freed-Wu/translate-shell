#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.
"""
from pathlib import Path


class AppDirs:
    """AppDirs."""

    def __init__(self, appname: str) -> None:
        """Init.

        :param appname:
        :type appname: str
        :rtype: None
        """
        self.site_data_path = (
            self.user_config_path
        ) = self.user_data_path = Path().home() / ("." + appname)
        self.site_data_dir = str(self.site_data_path)
        self.user_config_dir = str(self.user_config_path)
        self.user_data_dir = str(self.user_data_path)


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
