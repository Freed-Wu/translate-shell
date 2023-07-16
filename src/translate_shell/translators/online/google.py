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
        """Get url.

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
        url = f"https://{http_host}/translate_a/single?client=gtx&sl={sl}\
&tl={tl}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&q={qry}"
        return url

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
        url = self.get_url(sl, tl, text)
        resp = self.http_get(url)
        if not resp:
            return None
        obj = json.loads(resp)

        res["paraphrase"] = self.get_paraphrase(obj)
        res["explains"] = self.get_explains(obj)
        res["phonetic"] = self.get_phonetic(obj)
        res["details"] = self.get_details(obj)
        res["alternatives"] = self.get_alternatives(obj)
        return res

    @staticmethod
    def get_phonetic(obj: list[Any]) -> str:
        """Get phonetic.

        :param obj:
        :type obj: list[Any]
        :rtype: str
        """
        for x in obj[0]:
            if len(x) == 4:
                return x[3]
        return ""

    @staticmethod
    def get_paraphrase(obj: list[Any]) -> str:
        """Get paraphrase.

        :param obj:
        :type obj: list[Any]
        :rtype: str
        """
        paraphrase = ""
        for x in obj[0]:
            if x[0]:
                paraphrase += x[0]
        return paraphrase

    @staticmethod
    def get_explains(obj: list[Any]) -> dict[str, str]:
        """Get explains.

        :param obj:
        :type obj: list[Any]
        :rtype: dict[str, str]
        """
        expls = {}
        if obj[1]:
            for x in obj[1]:
                expls[x[0]] = ""
                for i in x[2]:
                    expls[x[0]] += i[0] + "; "
        return expls

    @staticmethod
    def get_details(resp: list[Any]) -> dict[str, dict[str, str]]:
        """Get details.

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

    def get_alternatives(self, resp: list[Any]) -> list[str]:
        """Get alternatives.

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
