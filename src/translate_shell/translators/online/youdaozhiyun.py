"""Youdaozhiyun Translator
==========================

Refer https://github.com/felixonmars/ydcv

https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html
"""
import json
import logging
import random

from ...__main__ import ASSETS_PATH
from ...ui import get_youdaozhiyun_app_info  # type: ignore
from .. import TRANSLATION
from . import OnlineTranslator

try:
    YDAPPID, YDAPPSEC = get_youdaozhiyun_app_info()
except Exception:
    YDAPPID = YDAPPSEC = ""

logger = logging.getLogger(__name__)

ERROR = json.loads(
    (ASSETS_PATH / "json" / "youdaozhiyun_error.json").read_text()
)


class YoudaozhiyunTranslator(OnlineTranslator):
    """YoudaozhiyunTranslator."""

    def __init__(self) -> None:
        """__init__.

        :rtype: None
        """
        super().__init__("youdaozhiyun")
        self.url = "https://openapi.youdao.com/api"

    def sign(self, text: str, salt: str) -> str:
        """sign.

        :param text:
        :type text: str
        :param salt:
        :type salt: str
        :rtype: str
        """
        s = YDAPPID + text + salt + YDAPPSEC
        return self.md5sum(s)

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
        salt = str(random.randint(1, 65536))  # nosec B311
        sign = self.sign(text, salt)
        if tl == "zh-cn":
            to = "zh-CHS"
        elif tl == "zh-tw":
            to = "zh-CHT"
        else:
            to = tl
        data = {
            "appKey": YDAPPID,
            "q": text,
            "from": sl,
            "to": to,
            "salt": salt,
            "sign": sign,
        }
        resp = self.http_get(self.url, data, None)

        if isinstance(resp, str):
            try:
                obj = json.loads(resp)
            except json.decoder.JSONDecodeError:
                return
        else:
            return
        if obj["errorCode"] != 0:
            logger.warning(ERROR.get(obj["errorCode"], "Unknown error!"))
            return

        res = self.create_translation(text, tl, sl)
        basic = obj.get("basic")
        res["paraphrase"] = obj.get("translation", "")
        res["detail"] = obj.get("web", "")
        if basic:
            # ignore us/uk-phonetic
            res["phonetic"] = basic.get("phonetic", "")
            res["explains"] = basic.get("explains", [])
        return res
