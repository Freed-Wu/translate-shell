#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.
"""
import re as _re

_RE_CHINESE = _re.compile("[\u4e00-\u9fff]", _re.UNICODE)
_RE_JAPANESE = _re.compile("[\u3041-\u30FE]", _re.UNICODE)
LangDetectException = Exception


def detect(text: str) -> str:
    """detect.

    :param text:
    :type text: str
    :rtype: str
    """
    if _RE_JAPANESE.match(text):
        return "ja"
    if _RE_CHINESE.match(text):
        return "zh-cn"
    return "en"


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
