"""translate
============

Define some utilities.
"""
import logging
from argparse import Namespace
from copy import deepcopy
from threading import Thread
from typing import Callable

from .translators import TRANSLATORS, Translator

logger = logging.getLogger(__name__)


class Translation(Namespace):
    """Translation."""

    def __init__(self, text: str, target_lang: str, source_lang: str) -> None:
        """Init.

        :param text:
        :type text: str
        :param target_lang:
        :type target_lang: str
        :param source_lang:
        :type source_lang: str
        :rtype: None
        """
        super().__init__()
        self.status = 0
        self.results = []
        self.text = text
        self.to_lang = target_lang
        self.from_lang = source_lang
        self.results = []
        self.status = 0


def translate_once(translator: Translator, translation: Translation) -> None:
    """Translate once without multi threads.

    :param translator: individual for each thread
    :type translator: Translator
    :param translation: same for each thread
    :type translation: Translation
    :rtype: None
    """
    res = translator(
        translation.text,
        translation.to_lang,
        translation.from_lang,
    )
    if res:
        translation.results.append(deepcopy(res))
        translation.status = 1


def translate(
    text: str,
    target_lang: str = "auto",
    source_lang: str = "auto",
    translators: list[Callable[[], Translator]] | list[str] | None = None,
) -> Translation:
    """Translate.

    :param text:
    :type text: str
    :param target_lang:
    :type target_lang: str
    :param source_lang:
    :type source_lang: str
    :param translators:
    :type translators: list[Callable[[], Translator] | str] | None
    :rtype: Translation
    """
    if translators is None:
        translators = ["google"]
    translation = Translation(text, target_lang, source_lang)

    true_translators = []
    for translator in translators:
        if isinstance(translator, str):
            translator = TRANSLATORS.get(translator)
        if isinstance(translator, Callable):
            translator = translator()
        true_translators += [translator]
    if len(translators) == 1:
        translator = true_translators[0]
        translate_once(translator, translation)
    else:
        threads = []
        for translator in true_translators:
            if translator is None:
                continue

            task = Thread(
                target=translate_once, args=(translator, translation)
            )
            threads.append(task)

        list(map(lambda x: x.start(), threads))
        list(map(lambda x: x.join(), threads))

    return translation
