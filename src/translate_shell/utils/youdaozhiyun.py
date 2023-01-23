"""Get Youdaozhiyun APP Info."""
import logging

from ..external.keyring import get_keyring
from ..external.keyring.errors import NoKeyringError

logger = logging.getLogger(__name__)


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
        logger.error(service_name + "/" + user_name4appid + "has no password!")
        return "", ""
    if not YDAPPSEC:
        logger.error(
            service_name + "/" + user_name4appsec + "has no password!"
        )
        return "", ""
    return YDAPPID, YDAPPSEC
