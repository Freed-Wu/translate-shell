"""Provide ``__version__`` for
`importlib.metadata.version() <https://docs.python.org/3/library/importlib.metadata.html#distribution-versions>`_.
"""
from ._version import version as __version__
from ._version import version_tuple
from .external.platformdirs import AppDirs

__all__ = [
    "__version__",
    "version_tuple",
    "APPDIRS",
    "HISTORY_PATH",
    "HISTORY_FILE",
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
