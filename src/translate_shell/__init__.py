"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""
try:
    from ._version import __version__, __version_tuple__  # type: ignore
except ImportError:
    __version__ = "rolling"
    __version_tuple__ = (0, 0, 0, __version__, "")

from .external.platformdirs import AppDirs

__all__ = [
    "__version__",
    "__version_tuple__",
    "APPDIRS",
    "CONFIG_PATH",
    "CONFIG_FILE",
    "HISTORY_PATH",
    "HISTORY_FILE",
    "STARDICT_PATHS",
    "STARDICT_DIRS",
]

APPDIRS = AppDirs(__name__.split(".")[0].replace("_", "-"))
CONFIG_PATH = APPDIRS.user_config_path / "config.py"
CONFIG_FILE = str(CONFIG_PATH)
HISTORY_PATH = APPDIRS.user_data_path / "history.txt"
HISTORY_FILE = str(HISTORY_PATH)
stardict_appdirs = AppDirs("stardict/dic")
STARDICT_PATHS = [
    stardict_appdirs.user_data_path,
    stardict_appdirs.site_data_path,
]
STARDICT_DIRS = [
    stardict_appdirs.user_data_dir,
    stardict_appdirs.site_data_dir,
]
