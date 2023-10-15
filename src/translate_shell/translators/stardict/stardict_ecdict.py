r"""Stardict Ecdict
===================
"""
from .. import Translation


def parse_tokens(tokens: list[str], res: Translation) -> Translation:
    """Parse tokens.

    :param tokens:
    :type tokens: list[str]
    :param res:
    :type res: Translation
    :rtype: Translation
    """
    res.phonetic = tokens[0].split()[0].lstrip("*[").rstrip("]")
    explains = {}
    for token in tokens[1:-1]:
        k, _, v = token.partition(" ")
        if v:
            explains[k] = v
    res.explains = explains
    k, _, v = tokens[-1].lstrip("(").rstrip(")").partition(" ")
    source = {"来源": {k: v}}
    res.details = source
    return res
