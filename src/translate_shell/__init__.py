"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""

from pathlib import Path

try:
    from ._version import __version__, __version_tuple__  # type: ignore
except ImportError:  # For vim
    __version__ = "rolling"
    __version_tuple__ = (0, 0, 0, __version__, "")

from .external.platformdirs import AppDirs

__all__ = [
    "__version__",
    "__version_tuple__",
    "APPNAME",
    "CONFIG_FILE",
    "HISTORY_FILE",
    "STARDICT_DIRS",
]

APPNAME = __name__.replace("_", "-")
appdirs = AppDirs(APPNAME, multipath=True)
CONFIG_FILE = appdirs.user_config_path / "config.py"
HISTORY_FILE = appdirs.user_data_path / "history.txt"
stardict_appdirs = AppDirs("stardict/dic")
# https://github.com/platformdirs/platformdirs/issues/259
# don't use site_data_path
STARDICT_DIRS = [
    stardict_appdirs.user_data_path,
] + [Path(path) for path in stardict_appdirs.site_data_dir.split(":")]
