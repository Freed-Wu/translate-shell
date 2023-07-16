"""Bing Translator
==================

Refer https://github.com/voldikss/vim-translator
https://www.microsoft.com/en-us/translator/help/bing/
"""
import re
from typing import Any
from urllib.parse import quote_plus

from .. import TRANSLATION
from . import OnlineTranslator


class BingTranslator(OnlineTranslator):
    """BingTranslator."""

    def __init__(self) -> None:
        """Init.

        :rtype: None
        """
        super().__init__("bing")
        self._url = "http://bing.com/dict/SerpHoverTrans"
        self._cnurl = "http://cn.bing.com/dict/SerpHoverTrans"
        self.pat_attr = re.compile(
            r'<span class="ht_attr" lang=".*?">\[(.*?)\] </span>'
        )
        self.pat_trs = re.compile(
            r'<span class="ht_pos">(.*?)</span>'
            r'<span class="ht_trs">(.*?)</span>'
        )

    def __call__(
        self, text: str, tl: str, sl: str, option: dict[str, Any]
    ) -> TRANSLATION | None:
        """Call.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :param option:
        :type option: dict[str, Any]
        :rtype: TRANSLATION | None
        """
        res = self.create_translation(text, tl, sl)
        tl, sl = self.convert_langs(tl, sl)
        url = self._cnurl if "zh" in tl else self._url
        url = url + "?q=" + quote_plus(text)
        headers = {
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;"
                "q=0.9,*/*;q=0.8"
            ),
            "Accept-Language": "en-US,en;q=0.5",
            "Cookie": "_EDGE_S=mkt=" + tl,
        }
        resp = self.http_get(url, None, headers)
        if not resp:
            return None
        res["phonetic"] = self.get_phonetic(resp)
        res["explains"] = self.get_explains(resp)
        return res

    def get_phonetic(self, html: str) -> str:
        """Get phonetic.

        :param html:
        :type html: str
        :rtype: str
        """
        if not html:
            return ""
        m = self.pat_attr.findall(html)
        if not m:
            return ""
        return self.html_unescape(m[0].strip())

    def get_explains(self, html: str) -> dict[str, str]:
        """Get explains.

        :param html:
        :type html: str
        :rtype: dict[str, str]
        """
        expls = {}
        if not html:
            return expls
        m = self.pat_trs.findall(html)
        for pos, explain in m:
            expls[pos] = explain
        return expls
