"""Provide ``TRANSLATORS`` for shell completion."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .online.bing import BingTranslator
    from .online.google import GoogleTranslator
    from .online.haici import HaiciTranslator
    from .online.youdaozhiyun import YoudaozhiyunTranslator
    from .speaker import Speaker
    from .stardict import StardictTranslator

logger = logging.getLogger(__name__)
TRANSLATION = dict[
    str,
    str | list[str] | dict[str, str] | dict[str, dict[str, str]],
]


class Translator:
    """Basic translator. All other translators must be its subclass."""

    def __init__(self, name: str) -> None:
        """Init.

        :param name:
        :type name: str
        :rtype: None
        """
        self._name = name

    def create_translation(self, text: str, tl: str, sl: str) -> TRANSLATION:
        """Create translation.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :rtype: TRANSLATION
        """
        res = {
            "translator": self._name,
            "sl": sl,
            "tl": tl,
            "text": text,
            "phonetic": "",
            "paraphrase": "",
            "explains": {},
            "details": {},
            "alternatives": {},
        }
        return res

    def __call__(self, text: str, tl: str, sl: str) -> dict[str, str] | None:
        """Call.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :rtype: dict[str, str] | None
        """
        logger.warning(
            self._name + " translator hasn't been implemented."
            " Maybe you input a typo?"
        )


def get_dummy(name: str) -> Callable[[], Translator]:
    """Get dummy.

    :param name:
    :type name: str
    :rtype: Callable[[], Translator]
    """

    def _get_dummy() -> Translator:
        """Define a temporary function.

        :rtype: Translator
        """
        return Translator(name)

    return _get_dummy


def get_stardict() -> StardictTranslator:
    """Get stardict.

    :rtype: StardictTranslator
    """
    from .stardict import StardictTranslator

    return StardictTranslator()


def get_speaker() -> Speaker:
    """Get speaker.

    :rtype: Speaker
    """
    from .speaker import Speaker

    return Speaker()


def get_google() -> GoogleTranslator:
    """Get google.

    :rtype: GoogleTranslator
    """
    from .online.google import GoogleTranslator

    return GoogleTranslator()


def get_youdaozhiyun() -> YoudaozhiyunTranslator:
    """Get youdaozhiyun.

    :rtype: YoudaozhiyunTranslator
    """
    from .online.youdaozhiyun import YoudaozhiyunTranslator

    return YoudaozhiyunTranslator()


def get_bing() -> BingTranslator:
    """Get bing.

    :rtype: BingTranslator
    """
    from .online.bing import BingTranslator

    return BingTranslator()


def get_haici() -> HaiciTranslator:
    """Get haici.

    :rtype: HaiciTranslator
    """
    from .online.haici import HaiciTranslator

    return HaiciTranslator()


def get_youdao() -> Callable[[], Translator] | None:
    """Get youdao.

    :rtype: Callable[[], Translator] | None
    """
    logger.warning(
        "youdao translator hasn't been implemented."
        " Maybe you want to send a PR?"
    )
    return


def get_yandex() -> Callable[[], Translator] | None:
    """Get yandex.

    :rtype: Callable[[], Translator] | None
    """
    logger.warning(
        "yandex translator hasn't been implemented."
        " Maybe you want to send a PR?"
    )
    return


TRANSLATORS = {
    "stardict": get_stardict,
    "google": get_google,
    "speaker": get_speaker,
    "yandex": get_yandex,
    "youdao": get_youdao,
    "youdaozhiyun": get_youdaozhiyun,
    "bing": get_bing,
    "haici": get_haici,
}
