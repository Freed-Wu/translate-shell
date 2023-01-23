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
        self.timeout = 15

    def __call__(self, text: str, tl: str, sl: str) -> TRANSLATION | None:
        """Call.

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
            return None

        res = self.create_translation(text, tl, sl)
        res["phonetic"] = self.get_phonetic(resp)
        res["explains"] = self.get_explains(resp)
        res["details"] = self.get_details(resp)
        return res

    @staticmethod
    def get_phonetic(html: str) -> str:
        """Get phonetic.

        :param html:
        :type html: str
        :rtype: str
        """
        m = re.findall(r"<span class='p'> \[(.*?)\]</span>", html)
        return m[0] if m else ""

    @staticmethod
    def get_explains(html: str) -> dict[str, str]:
        """Get explains.

        :param html:
        :type html: str
        :rtype: dict[str, str]
        """
        m = re.findall(r'<div id="e">(.*?)</div>', html)
        explains = {}
        for item in m:
            for e in item.split("<br>"):
                k, dot, v = e.partition(".")
                explains[k + dot] = v
        return explains

    @staticmethod
    def get_details(html: str) -> dict[str, dict[str, str]]:
        """Get details.

        :param html:
        :type html: str
        :rtype: dict[str, dict[str, str]]
        """
        details = {}
        m = re.findall(r'<div id="s">(.*?)</div>', html)
        rst = {}
        for item in m:
            sentences = item.split("<br>")
            for s1, s2 in list(zip(sentences[::2], sentences[1::2])):
                _, _, v = s1.partition(". ")
                rst[v] = s2
        details["例句与用法"] = rst

        m = re.findall(r'<div id="t">(.*?)</div>', html)
        rst = {}
        for item in m:
            sentences = item.split("</i>")
            for s in sentences:
                k, _, v = s.partition(": ")
                k = k.strip()
                if k:
                    rst[k] = v.replace("<i>", "").strip()
        details["词形变化"] = rst
        return details
