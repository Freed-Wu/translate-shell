"""translate
============

Define some utilities.
"""

import asyncio
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from inspect import iscoroutine
from typing import Any

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


async def translate_once(
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
    res = translator(  # type: ignore
        translations.text,
        translations.to_lang,
        translations.from_lang,
        option,
    )
    if iscoroutine(res):
        res: Translation = await res
    if res:
        translations.results.append(res)
        translations.status = 1


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
                translate_once(
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

    asyncio.run(translate_many(true_translators, translations, options))
    return translations
