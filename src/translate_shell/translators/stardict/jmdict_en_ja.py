"""jmdict_en_ja"""
from ...external.langdetect.__main__ import _RE_JAPANESE
from .. import TRANSLATION


def parse_tokens(tokens: list[str], res: TRANSLATION) -> TRANSLATION:
    """parse_tokens.

    :param tokens:
    :type tokens: list[str]
    :param res:
    :type res: TRANSLATION
    :rtype: TRANSLATION
    """
    last_key = ""
    explains = {}
    for token in tokens:
        if len(token) != len(_RE_JAPANESE.findall(token)):
            if last_key == "" or last_key in explains.keys():
                last_key = token
            else:
                last_key += "; " + token
        else:
            if last_key in explains.keys():
                explains[last_key] += "; " + token
            else:
                explains[last_key] = token
    res["explains"] = explains
    return res
