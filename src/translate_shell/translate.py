"""translate
============

Define some utilities.
"""
import asyncio
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


async def _translate_once(
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
    translate_once(translator, translations, option)


async def translate_many(
    translators: list[Translator],
    translations: Translations,
    options: dict[str, dict[str, Any]],
) -> None:
    """Translate many.

    :param translators:
    :type translators: list[Translator]
    :param translations:
    :type translations: Translations
    :param options:
    :type options: dict[str, dict[str, Any]]
    :rtype: None
    """
    tasks = []
    for translator in translators:
        tasks += [
            asyncio.create_task(
                _translate_once(
                    translator, translations, options.get(translator.name, {})
                )
            )
        ]
    for task in tasks:
        await task


def translate(
    text: str,
    target_lang: str = "auto",
    source_lang: str = "auto",
    translators: list[Callable[[], Translator]] | list[str] | None = None,
    options: dict[str, dict[str, Any]] | None = None,
    use: str = "coroutine",
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
    :param use:
    :type use: str
    :rtype: Translations
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
        if translator is None:
            continue
        true_translators += [translator]

    if len(true_translators) == 1:
        translator = true_translators[0]
        translate_once(
            translator, translations, options.get(translator.name, {})
        )
    elif use == "threading":
        threads = []
        for translator in true_translators:
            thread = Thread(
                target=translate_once,
                args=(
                    translator,
                    translations,
                    options.get(translator.name, {}),
                ),
            )
            threads += [thread]
        list(map(lambda x: x.start(), threads))
        list(map(lambda x: x.join(), threads))
    elif use == "coroutine":
        asyncio.run(translate_many(true_translators, translations, options))
    else:
        for translator in true_translators:
            translate_once(
                translator, translations, options.get(translator.name, {})
            )
    return translations
