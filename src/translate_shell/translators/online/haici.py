"""Haici Translator
===================

Refer https://github.com/voldikss/vim-translator
http://dict.cn
"""
import re
from urllib.parse import quote_plus

from .. import TRANSLATION
from . import OnlineTranslator


class HaiciTranslator(OnlineTranslator):
    """HaiciTranslator."""

    def __init__(self) -> None:
        """__init__.

        :rtype: None
        """
        super().__init__("haici")

    def __call__(self, text: str, tl: str, sl: str) -> TRANSLATION | None:
        """__call__.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :rtype: TRANSLATION | None
        """
        url = "http://dict.cn/mini.php"
        req = {}
        req["q"] = quote_plus(text)
        resp = self.http_get(url, req)
        if not resp:
            return

        res = self.create_translation(text, tl, sl)
        res["phonetic"] = self.get_phonetic(resp)
        res["explains"] = self.get_explains(resp)
        return res

    def get_phonetic(self, html: str) -> str:
        """get_phonetic.

        :param html:
        :type html: str
        :rtype: str
        """
        m = re.findall(r"<span class='p'> \[(.*?)\]</span>", html)
        return m[0] if m else ""

    def get_explains(self, html: str) -> dict[str, str]:
        """get_explains.

        :param html:
        :type html: str
        :rtype: dict[str, str]
        """
        m = re.findall(r'<div id="e">(.*?)</div>', html)
        explains = {}
        for item in m:
            for e in item.split("<br>"):
                k, dot, v = e.rpartition(".")
                explains[k + dot] = v
        return explains
