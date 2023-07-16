"""Youdaozhiyun Translator
==========================

Refer https://github.com/felixonmars/ydcv

https://ai.youdao.com/DOCSIRMA/html/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E7%BF%BB%E8%AF%91/API%E6%96%87%E6%A1%A3/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1/%E6%96%87%E6%9C%AC%E7%BF%BB%E8%AF%91%E6%9C%8D%E5%8A%A1-API%E6%96%87%E6%A1%A3.html
"""
import json
import logging
import random
from typing import Any

from ...__main__ import ASSETS_PATH
from ...external.keyring import get_keyring
from ...external.keyring.errors import NoKeyringError
from .. import TRANSLATION
from . import OnlineTranslator

logger = logging.getLogger(__name__)
ERROR = json.loads(
    (ASSETS_PATH / "json" / "youdaozhiyun-error.json").read_text(
        encoding="utf-8"
    )
)


class YoudaozhiyunTranslator(OnlineTranslator):
    """YoudaozhiyunTranslator."""

    def __init__(self) -> None:
        """Init.

        :rtype: None
        """
        super().__init__("youdaozhiyun")
        self.url = "https://openapi.youdao.com/api"
        self.app_id = self.app_sec = ""

    def init(self, option: dict[str, Any]) -> None:
        """Init.

        :param option:
        :type option: dict[str, Any]
        :rtype: None
        """
        if self.app_id and self.app_sec:
            return
        self.app_id, self.app_sec = option.get(
            "get_youdaozhiyun_app_info",
            self.__class__.get_youdaozhiyun_app_info,
        )()

    def sign(self, text: str, salt: str) -> str:
        """Sign.

        :param text:
        :type text: str
        :param salt:
        :type salt: str
        :rtype: str
        """
        s = self.app_id + text + salt + self.app_sec
        return self.md5sum(s)

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
        self.init(option)
        salt = str(random.randint(1, 65536))  # nosec B311
        sign = self.sign(text, salt)
        if tl == "zh-cn":
            to = "zh-CHS"
        elif tl == "zh-tw":
            to = "zh-CHT"
        else:
            to = tl
        data = {
            "appKey": self.app_id,
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
                logger.error("Wrong json format!")
                return None
        else:
            return None
        if obj["errorCode"] != 0:
            logger.warning(ERROR.get(obj["errorCode"], "Unknown error!"))
            return None

        basic = obj.get("basic")
        res["paraphrase"] = obj.get("translation", "")
        res["detail"] = obj.get("web", "")
        if basic:
            # ignore us/uk-phonetic
            res["phonetic"] = basic.get("phonetic", "")
            res["explains"] = basic.get("explains", [])
        return res

    @staticmethod
    def get_youdaozhiyun_app_info(
        service_name: str = "youdaozhiyun",
        user_name4appid: str = "appid",
        user_name4appsec: str = "appsec",
    ) -> tuple[str, str]:
        """Get youdaozhiyun app info.

        :param service_name:
        :type service_name: str
        :param user_name4appid:
        :type user_name4appid: str
        :param user_name4appsec:
        :type user_name4appsec: str
        :rtype: tuple[str, str]
        """
        keyring = get_keyring()
        try:
            YDAPPID = keyring.get_password(service_name, user_name4appid)
            YDAPPSEC = keyring.get_password(service_name, user_name4appsec)
        except NoKeyringError:
            logger.error("no installed backend!")
            return "", ""
        if not YDAPPID:
            logger.error(
                service_name + "/" + user_name4appid + "has no password!"
            )
            return "", ""
        if not YDAPPSEC:
            logger.error(
                service_name + "/" + user_name4appsec + "has no password!"
            )
            return "", ""
        return YDAPPID, YDAPPSEC
