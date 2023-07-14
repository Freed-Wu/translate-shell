"""List Setting
===============
"""
from ..__main__ import SETTING


def get_setting(name: SETTING | None) -> str:
    """get_setting.

    :param name:
    :type name: SETTING | None
    :rtype: str
    """
    if name == "config_file":
        from .. import CONFIG_FILE as result
    elif name == "history_file":
        from .. import HISTORY_FILE as result
    elif name == "dictionary_dirs":
        from .. import STARDICT_DIRS

        result = "\n".join(map(str, STARDICT_DIRS))
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
        from ..translators.speaker import Speaker

        result = " ".join(Speaker.get_speaker("")).strip()
    elif name == "dictionary_priorities":
        from ..translators.stardict import STARDICT

        result = "\n".join(
            [
                "\t".join([sl, tl] + [",".join(dictionaries)])
                for sl, v in STARDICT.items()
                for tl, dictionaries in v.items()
            ]
        )
    elif name is None:
        from ..__main__ import SETTING

        result = "\n\n".join("## " + setting + "\n\n" + get_setting(setting) for setting in SETTING.__args__)  # type: ignore
    else:
        result = ""
    return str(result)


def print_setting(name: SETTING) -> int:
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
