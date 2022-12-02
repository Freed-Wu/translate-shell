"""List Setting
===============
"""


def get_setting(name: str | None) -> str:
    """get_setting.

    :param name:
    :type name: str | None
    :rtype: str
    """
    if name == "config_file":
        from .. import CONFIG_FILE as result
    elif name == "history_file":
        from .. import HISTORY_FILE as result
    elif name == "dictionary_dirs":
        from .. import STARDICT_DIRS

        result = "\n".join(STARDICT_DIRS)
    elif name == "translators":
        from ..translators import TRANSLATORS

        result = "\n".join(TRANSLATORS)
    elif name == "languages":
        from ..__main__ import LANGS

        result = "\n".join(map(lambda x: x[0] + ": " + x[1], LANGS.items()))
    elif name == "formats":
        from ..__main__ import FORMATS

        result = "\n".join(FORMATS)
    elif name == "clipper":
        from .clippers import get_clipper

        result = " ".join(get_clipper())
    elif name == "speaker":
        from .speakers import get_speaker

        result = " ".join(get_speaker("")).strip()
    elif name is None:
        from ..__main__ import SETTINGS

        result = "\n".join(SETTINGS)
    else:
        result = ""
    return result


def print_setting(name: str) -> int:
    """print_setting.

    :param name:
    :type name: str
    :rtype: int
    """
    setting = get_setting(name)
    if setting:
        print(setting)
        return 0
    return 1
