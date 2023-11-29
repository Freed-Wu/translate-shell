"""translate
============

Define some utilities.
"""
import logging
from dataclasses import dataclass, field
from threading import Thread
from typing import Any, Callable

from .translators import TRANSLATORS, Translation, Translator

logger = logging.getLogger(__name__)


@dataclass
class Translations:
    """Translation."""

    text: str = ""
    to_lang: str = ""
    from_lang: str = ""
    status: int = 0
    results: list[Translation] = field(default_factory=list)


def translate_once(
    translator: Translator, translations: Translations, option: dict[str, Any]
) -> None:
    """Translate once.

    :param translator:
    :type translator: Translator
    :param translations:
    :type translations: Translations
    :param option:
    :type option: dict[str, Any]
    :rtype: None
    """
    res = translator(
        translations.text,
        translations.to_lang,
        translations.from_lang,
        option,
    )
    if res:
        translations.results.append(res)
        translations.status = 1


def translate(
    text: str,
    target_lang: str = "auto",
    source_lang: str = "auto",
    translators: list[Callable[[], Translator]] | list[str] | None = None,
    options: dict[str, dict[str, Any]] | None = None,
) -> Translations:
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
    translations = Translations(text, target_lang, source_lang)

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
            translator, translations, options.get(translator.name, {})
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
                    translations,
                    options.get(translator.name, {}),
                ),
            )
            threads.append(task)

        list(map(lambda x: x.start(), threads))
        list(map(lambda x: x.join(), threads))

    return translations
