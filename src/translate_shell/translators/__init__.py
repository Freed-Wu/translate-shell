"""Provide ``TRANSLATORS`` for shell completion."""
from __future__ import annotations

import logging
from argparse import Namespace
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from .llm._llama_cpp import LlamaTranslator
    from .llm._openai import OpenaiTranslator
    from .online.bing import BingTranslator
    from .online.google import GoogleTranslator
    from .online.haici import HaiciTranslator
    from .online.youdaozhiyun import YoudaozhiyunTranslator
    from .speaker import Speaker
    from .stardict import StardictTranslator

logger = logging.getLogger(__name__)


class Translation(Namespace):
    """Translation."""

    def __init__(
        self,
        translator: str,
        sl: str,
        tl: str,
        text: str,
        phonetic: str,
        paraphrase: str,
        explains: dict[str, str],
        details: dict[str, dict[str, str]],
        alternatives: list[str],
    ) -> None:
        """Init.

        :param translator:
        :type translator: str
        :param sl:
        :type sl: str
        :param tl:
        :type tl: str
        :param text:
        :type text: str
        :param phonetic:
        :type phonetic: str
        :param paraphrase:
        :type paraphrase: str
        :param explains:
        :type explains: dict[str, str]
        :param details:
        :type details: dict[str, dict[str, str]]
        :param alternatives:
        :type alternatives: list[str]
        :rtype: None
        """
        super().__init__(
            translator=translator,
            sl=sl,
            tl=tl,
            text=text,
            phonetic=phonetic,
            paraphrase=paraphrase,
            explains=explains,
            details=details,
            alternatives=alternatives,
        )


class Translator:
    """Basic translator. All other translators must be its subclass."""

    def __init__(self, name: str) -> None:
        """Init.

        :param name:
        :type name: str
        :rtype: None
        """
        self.name = name

    def create_translation(self, text: str, tl: str, sl: str) -> Translation:
        """Create translation.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :rtype: Translation
        """
        return Translation(
            translator=self.name,
            sl=sl,
            tl=tl,
            text=text,
            phonetic="",
            paraphrase="",
            explains={},
            details={},
            alternatives=[],
        )

    @staticmethod
    def convert_langs(*langs: str) -> list[str]:
        """Convert langs to URL friendly form.

        :param langs:
        :type langs: str
        :rtype: list[str]
        """
        return [lang.lower().replace("_", "-") for lang in langs]

    def __call__(
        self, text: str, tl: str, sl: str, option: dict[str, Any]
    ) -> dict[str, str] | None:
        """Call.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :param option:
        :type option: dict[str, Any]
        :rtype: dict[str, str] | None
        """
        logger.warning(
            self.name + " translator hasn't been implemented."
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


def get_stardict() -> "StardictTranslator":
    """Get stardict.

    :rtype: StardictTranslator
    """
    from .stardict import StardictTranslator

    return StardictTranslator()


def get_speaker() -> "Speaker":
    """Get speaker.

    :rtype: Speaker
    """
    from .speaker import Speaker

    return Speaker()


def get_google() -> "GoogleTranslator":
    """Get google.

    :rtype: GoogleTranslator
    """
    from .online.google import GoogleTranslator

    return GoogleTranslator()


def get_youdaozhiyun() -> "YoudaozhiyunTranslator":
    """Get youdaozhiyun.

    :rtype: YoudaozhiyunTranslator
    """
    from .online.youdaozhiyun import YoudaozhiyunTranslator

    return YoudaozhiyunTranslator()


def get_bing() -> "BingTranslator":
    """Get bing.

    :rtype: BingTranslator
    """
    from .online.bing import BingTranslator

    return BingTranslator()


def get_haici() -> "HaiciTranslator":
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


def get_openai() -> "OpenaiTranslator":
    """Get openai.

    :rtype: "OpenaiTranslator"
    """
    from .llm._openai import OpenaiTranslator

    return OpenaiTranslator()


def get_llama() -> "LlamaTranslator":
    """Get llama.

    :rtype: "LlamaTranslator"
    """
    from .llm._llama_cpp import LlamaTranslator

    return LlamaTranslator()


TRANSLATORS = {
    "stardict": get_stardict,
    "google": get_google,
    "speaker": get_speaker,
    "yandex": get_yandex,
    "youdao": get_youdao,
    "youdaozhiyun": get_youdaozhiyun,
    "bing": get_bing,
    "haici": get_haici,
    "openai": get_openai,
    "llama": get_llama,
}
