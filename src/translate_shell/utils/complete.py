"""Complete
===========
"""
import os

from ..__main__ import LANGS
from ..translators import TRANSLATORS


def complete(text: str, state: int) -> str:
    """Complete.

    :param text:
    :type text: str
    :param state:
    :type state: int
    :rtype: str
    """
    langs = list(LANGS.keys())
    volcab = ["=", "<", "!", ":"] + langs
    sl = text.split(":")[0]
    if text.startswith("="):
        length = len("=")
        left, _, right = text[length:].rpartition(",")
        if right in TRANSLATORS:
            volcab = [text + ","]
        else:
            translators = left.split(",")
            volcab = map(
                lambda x: "=" + left + ("," if left else "") + x,
                filter(lambda x: x not in translators, TRANSLATORS),
            )
    elif text.startswith("<"):
        length = len("<")
        dirname = os.path.dirname(text[length:])
        if dirname:
            files = os.listdir(dirname)
        else:
            files = os.listdir()
        files = map(lambda x: os.path.join(dirname, x), files)
        volcab = map(
            lambda x: "<" + x + ("/" if os.path.isdir(x) else ""),
            files,
        )
    elif text.startswith("!"):
        length = len("!")
        dirname = os.path.dirname(text[length:])
        if os.path.isdir(dirname):
            bins = filter(
                lambda x: os.access(x, os.X_OK),
                map(lambda x: os.path.join(dirname, x), os.listdir(dirname)),
            )
        else:
            bins = []
            for path in os.getenv("PATH", ".").split(os.path.pathsep):
                if os.path.isdir(path):
                    files = os.listdir(path)
                    for file in files:
                        if os.path.isfile(os.path.join(path, file)):
                            bins += [file]
        volcab = map(lambda x: "!" + x, bins)
    elif sl in langs + [""] and len(text.split(":")) == 2:
        volcab = map(lambda x: sl + ":" + x, langs)
    results = [x for x in volcab if x.startswith(text)]
    return results[state]
