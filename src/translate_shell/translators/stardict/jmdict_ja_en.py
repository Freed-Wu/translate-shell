"""jmdict_ja_en"""
from ...external.langdetect.__main__ import _RE_JAPANESE
from .. import Translation


def parse_tokens(tokens: list[str], res: Translation) -> Translation:
    """Parse tokens.

    :param tokens:
    :type tokens: list[str]
    :param res:
    :type res: Translation
    :rtype: Translation
    """
    last_key = ""
    explains = {}
    for token in tokens:
        if len(token) == len(_RE_JAPANESE.findall(token)):
            if last_key == "" or last_key in explains:
                last_key = token
            else:
                last_key += "; " + token
        else:
            if last_key in explains:
                explains[last_key] += "; " + token
            else:
                if last_key == "":
                    last_key = res.text
                explains[last_key] = token
    res.explains = explains
    return res
