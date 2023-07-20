"""Stardict Translator
======================

TODO: more stardicts.
TODO: Create different subclasses for different dict to get phonetic, explains
better
"""
import logging
import os
from contextlib import suppress
from glob import glob
from typing import Any

from ... import STARDICT_DIRS
from ...external.pystardict import Dictionary
from .. import TRANSLATION, Translator

logger = logging.getLogger(__name__)


def parse_tokens_fallback(tokens: list[str], res: TRANSLATION) -> TRANSLATION:
    """Parse tokens for fallback.

    :param tokens:
    :type tokens: list[str]
    :param res:
    :type res: TRANSLATION
    :rtype: TRANSLATION
    """
    res["paraphrase"] = "; ".join(tokens)
    return res


class StardictTranslator(Translator):
    """StardictTranslator."""

    def __init__(self) -> None:
        """Init.

        :rtype: None
        """
        super().__init__("stardict")
        self.stardict = {}

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
        self.stardict = option.get("stardict", STARDICT)
        tokens, dictionary = self.get_tokens(text, tl, sl)
        if tokens == []:
            logger.warning(
                "No appropriate dictionary is found in "
                + ", ".join(map(str, STARDICT_DIRS))
            )
            return None
        res = self.create_translation(text, tl, sl)
        if dictionary == "langdao-ec-gb":
            from .langdao_ec_gb import parse_tokens
        elif dictionary == "langdao-ce-gb":
            from .langdao_ce_gb import parse_tokens
        elif dictionary == "jmdict-en-ja":
            from .jmdict_en_ja import parse_tokens
        elif dictionary == "jmdict-ja-en":
            from .jmdict_ja_en import parse_tokens
        elif dictionary == "stardict-ecdict":
            from .stardict_ecdict import parse_tokens
        else:
            parse_tokens = parse_tokens_fallback
        res = parse_tokens(tokens, res)
        return res

    def get_tokens(self, text: str, tl: str, sl: str) -> tuple[list[str], str]:
        """Get tokens.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :rtype: tuple[list[str], str]
        """
        if sl == "auto":
            from ...external.langdetect import LangDetectException, detect

            try:
                sl = detect(text)
            except LangDetectException:
                sl = "en"
            # convert zh-cn to zh_CN
            lang, _, country = sl.partition("-")
            sl = lang + "_" + country.upper() if country else ""

        dictionaries = self.stardict.get(sl, self.stardict["en"]).get(tl, [])
        for directory in STARDICT_DIRS:
            for dictionary in dictionaries:
                expr = os.path.join(
                    directory,
                    os.path.join(
                        "**", dictionary + "*" + os.path.extsep + "dict*"
                    ),
                )
                paths = glob(expr, recursive=True)
                for path in paths:
                    prefix = path.rpartition(".dict")[0]
                    with suppress(AttributeError):
                        tokens = Dictionary(prefix).get(text).split("\n")
                        return tokens, dictionary
        return [], ""


STARDICT = {
    "en": {
        "zh_CN": ["langdao-ec-gb", "stardict-ecdict"],
        "ja": ["jmdict-en-ja"],
        "ru": ["quick_english-russian"],
    },
    "zh_CN": {"en": ["langdao-ce-gb"]},
    "ja": {"en": ["jmdict-ja-en"]},
    "ru": {"en": ["quick_russian-english"]},
}
