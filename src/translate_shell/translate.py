"""translate
============

Define some utilities.
"""
import logging
from argparse import Namespace
from copy import deepcopy
from threading import Thread
from typing import Any, Callable

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


def translate_once(
    translator: Translator, translation: Translation, option: dict[str, Any]
) -> None:
    """Translate once.

    :param translator:
    :type translator: Translator
    :param translation:
    :type translation: Translation
    :param option:
    :type option: dict[str, Any]
    :rtype: None
    """
    res = translator(
        translation.text,
        translation.to_lang,
        translation.from_lang,
        option,
    )
    if res:
        translation.results.append(deepcopy(res))
        translation.status = 1


def translate(
    text: str,
    target_lang: str = "auto",
    source_lang: str = "auto",
    translators: list[Callable[[], Translator]] | list[str] | None = None,
    options: dict[str, dict[str, Any]] | None = None,
) -> Translation:
    """Translate.

    :param text:
    :type text: str
    :param target_lang:
    :type target_lang: str
    :param source_lang:
    :type source_lang: str
    :param translators:
    :type translators: list[Callable[[], Translator]] | list[str] | None
    :param options:
    :type options: dict[str, dict[str, Any]] | None
    :rtype: Translation
    """
    if translators is None:
        translators = ["google"]
    if options is None:
        options = {}
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
        translate_once(
            translator, translation, options.get(translator.name, {})
        )
    else:
        threads = []
        for translator in true_translators:
            if translator is None:
                continue

            task = Thread(
                target=translate_once,
                args=(
                    translator,
                    translation,
                    options.get(translator.name, {}),
                ),
            )
            threads.append(task)

        list(map(lambda x: x.start(), threads))
        list(map(lambda x: x.join(), threads))

    return translation
