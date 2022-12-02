"""Stardict Translator
======================

TODO: more stardicts.
TODO: Create different subclasses for different dict to get phonetic, explains
better
"""
import logging

from pystardict import Dictionary

from ... import STARDICT_PATHS
from .. import TRANSLATION, Translator

logger = logging.getLogger(__name__)


def parse_tokens(tokens: list[str], res: TRANSLATION) -> TRANSLATION:
    """parse_tokens.

    :param rst:
    :type rst: str
    :param res:
    :type res: TRANSLATION
    :rtype: TRANSLATION
    """
    res["paraphrase"] = "; ".join(tokens)
    return res


class StardictTranslator(Translator):
    """StardictTranslator."""

    def __init__(self):
        """__init__."""
        super().__init__("stardict")

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
        tokens, dictionary = self.get_tokens(text, tl, sl)
        if tokens == []:
            return
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
            from . import parse_tokens
        res = parse_tokens(tokens, res)
        return res

    def get_tokens(self, text: str, tl: str, sl: str) -> tuple[list[str], str]:
        """get_tokens.

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

        dictionary = STARDICT.get(sl, STARDICT.get("en", {})).get(tl, "")
        if not dictionary:
            logger.warning(sl + " to " + tl + " dictionary is not found!")
            return [], ""
        target_dir = None
        for dir in STARDICT_PATHS:
            exist = False
            for ext in ["dict.dz", "dict"]:
                if not (dir / ".".join([dictionary, ext])).exists():
                    exist = True
                    break
            if exist:
                target_dir = dir
                break
        if target_dir:
            tokens = (
                Dictionary(str(target_dir / dictionary)).get(text).split("\n")
            )
            return tokens, dictionary
        logger.warning(
            dictionary
            + " is not found in "
            + ", ".join(map(str, STARDICT_PATHS))
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
