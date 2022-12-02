"""Google Translator
====================

Refer https://github.com/voldikss/vim-translator
https://support.google.com/translate
"""
import json
from typing import Any
from urllib.parse import quote_plus

from .. import TRANSLATION
from . import OnlineTranslator


class GoogleTranslator(OnlineTranslator):
    """GoogleTranslator."""

    def __init__(self) -> None:
        """__init__.

        :rtype: None
        """
        super().__init__("google")
        self._host = "translate.googleapis.com"
        self._cnhost = "translate.google.com.hk"

    def get_url(self, sl: str, tl: str, qry: str) -> str:
        """get_url.

        :param sl:
        :type sl: str
        :param tl:
        :type tl: str
        :param qry:
        :type qry: str
        :rtype: str
        """
        http_host = self._cnhost if "zh" in tl else self._host
        qry = quote_plus(qry)
        url = (
            "https://{}/translate_a/single?client=gtx&sl={}&tl={}&dt=at&dt=bd&"
            "dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&q={}".format(
                http_host, sl, tl, qry
            )
        )
        return url

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
        url = self.get_url(sl, tl, text)
        resp = self.http_get(url)
        if not resp:
            return
        obj = json.loads(resp)

        res = self.create_translation(text, tl, sl)
        res["paraphrase"] = self.get_paraphrase(obj)
        res["explains"] = self.get_explains(obj)
        res["phonetic"] = self.get_phonetic(obj)
        res["details"] = self.get_details(obj)
        res["alternative"] = self.get_alternative(obj)
        return res

    def get_phonetic(self, obj: list[Any]) -> str:
        """get_phonetic.

        :param obj:
        :type obj: list[Any]
        :rtype: str
        """
        for x in obj[0]:
            if len(x) == 4:
                return x[3]
        return ""

    def get_paraphrase(self, obj: list[Any]) -> str:
        """get_paraphrase.

        :param obj:
        :type obj: list[Any]
        :rtype: str
        """
        paraphrase = ""
        for x in obj[0]:
            if x[0]:
                paraphrase += x[0]
        return paraphrase

    def get_explains(self, obj: list[Any]) -> dict[str, str]:
        """get_explains.

        :param obj:
        :type obj: list[Any]
        :rtype: dict[str, str]
        """
        expls = {}
        if obj[1]:
            for x in obj[1]:
                expls[x[0][0]] = ""
                for i in x[2]:
                    expls[x[0][0]] += i[0] + "; "
        return expls

    def get_details(self, resp: list[Any]) -> dict[str, dict[str, str]]:
        """get_detail.

        :param resp:
        :type resp: list[Any]
        :rtype: dict[str, dict[str, str]]
        """
        result = {}
        if len(resp) < 13 or resp[12] is None:
            return result
        for x in resp[12]:
            result[x[0]] = {}
            for y in x[1]:
                if len(y) > 2 and isinstance(y[2], str):
                    example = y[2]
                else:
                    example = ""
                result[x[0]][y[0]] = example
        return result

    def get_alternative(self, resp: list[Any]) -> list[str]:
        """get_alternative.

        :param resp:
        :type resp: list[Any]
        :rtype: list[str]
        """
        if len(resp) < 6 or resp[5] is None:
            return []
        definition = self.get_paraphrase(resp)
        result = []
        for x in resp[5]:
            for i in x[2]:
                if i[0] != definition:
                    result.append(i[0])
        return result
