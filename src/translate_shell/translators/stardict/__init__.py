"""Stardict Translator
======================

TODO: more stardicts.
TODO: Create different subclasses for different dict to get phonetic, explains
better
"""
import logging
import os

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

    def __call__(self, text: str, tl: str, sl: str) -> TRANSLATION | None:
        """Call.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :rtype: TRANSLATION | None
        """
        tokens, dictionary = self.get_tokens(text, tl, sl)
        if tokens == []:
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
        else:
            parse_tokens = parse_tokens_fallback
        res = parse_tokens(tokens, res)
        return res

    @staticmethod
    def get_tokens(text: str, tl: str, sl: str) -> tuple[list[str], str]:
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

        dictionary = STARDICT.get(sl, STARDICT["en"]).get(tl, "")
        if not dictionary:
            logger.warning(sl + " to " + tl + " dictionary is not found!")
            return [], ""
        for directory in STARDICT_DIRS:
            for ext in ["dict.dz", "dict"]:
                for path in [directory, directory / dictionary]:
                    if not (
                        path / (dictionary + os.path.extsep + ext)
                    ).exists():
                        continue
                    tokens = (
                        Dictionary(path / dictionary).get(text, "").split("\n")
                    )
                    return tokens, dictionary
        logger.warning(
            dictionary
            + " is not found in "
            + ", ".join(map(str, STARDICT_DIRS))
        )
        return [], dictionary


STARDICT = {
    "en": {
        "zh-cn": "langdao-ec-gb",
        "ja": "jmdict-en-ja",
        "ru": "quick_english-russian",
    },
    "zh-cn": {"en": "langdao-ce-gb"},
    "ja": {"en": "jmdict-ja-en"},
    "ru": {"en": "quick_russian-english"},
}
