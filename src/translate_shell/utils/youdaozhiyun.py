"""Get Youdaozhiyun APP Info."""
import logging

from ..external.keyring import get_keyring

logger = logging.getLogger(__name__)


def get_youdaozhiyun_app_info(
    ydappid_path: str = "youdaozhiyun/appid",
    ydappsec_path: str = "youdaozhiyun/appsec",
) -> tuple[str, str]:
    """get_youdaozhiyun_app_info.

    :param ydappid_path:
    :type ydappid_path: str
    :param ydappsec_path:
    :type ydappsec_path: str
    :rtype: tuple[str, str]
    """
    YDAPPID = YDAPPSEC = ""
    keyring = get_keyring()
    if _YDAPPID := keyring.get_password(*ydappid_path.split("/")):
        YDAPPID = _YDAPPID
    if _YDAPPSEC := keyring.get_password(*ydappsec_path.split("/")):
        YDAPPSEC = _YDAPPSEC
    return YDAPPID, YDAPPSEC
