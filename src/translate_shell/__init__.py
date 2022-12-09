"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""
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
appdirs = AppDirs(APPNAME)
CONFIG_FILE = appdirs.user_config_path / "config.py"
HISTORY_FILE = appdirs.user_data_path / "history.txt"
stardict_appdirs = AppDirs("stardict/dic")
STARDICT_DIRS = [
    stardict_appdirs.user_data_path,
    stardict_appdirs.site_data_path,
]
