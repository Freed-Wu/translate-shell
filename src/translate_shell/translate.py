"""translate
============

Define some utilities.
"""
import logging
from argparse import Namespace
from collections import OrderedDict
from copy import deepcopy
from threading import Thread
from typing import Any, Callable

from .translators import TRANSLATORS, Translator

logger = logging.getLogger(__name__)


class Translations(Namespace):
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
        super().__init__(
            status=0,
            results=[],
            text=text,
            to_lang=target_lang,
            from_lang=source_lang,
        )

    @staticmethod
    def any2any(v: Any) -> Any:
        """Convert any to any.

        :param v:
        :type v: Any
        :rtype: Any
        """
        if isinstance(v, Namespace):
            return Translations.namespace2dict(v)
        if isinstance(v, list):
            return Translations.list2list(v)
        if isinstance(v, dict):
            return Translations.dict2dict(v)
        return v

    @staticmethod
    def list2list(d: list) -> list:
        """Convert list to list.

        :param d:
        :type d: list
        :rtype: list
        """
        for k, v in enumerate(d):
            d[k] = Translations.any2any(v)
        return d

    @staticmethod
    def dict2dict(d: dict) -> dict:
        """Convert dict to dict.

        :param d:
        :type d: dict
        :rtype: dict
        """
        for k, v in d.items():
            d[k] = Translations.any2any(v)
        return d

    @staticmethod
    def namespace2dict(namespace: Namespace) -> OrderedDict:
        """Convert Namespace to OrderedDict.

        :param namespace:
        :type namespace: Namespace
        :rtype: OrderedDict
        """
        d = OrderedDict(vars(namespace))
        for k, v in d.items():
            d[k] = Translations.any2any(v)
        return d

    def to_dict(self) -> OrderedDict:
        """Convert self to dict.

        :rtype: OrderedDict
        """
        return self.namespace2dict(self)


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
        translations.results.append(deepcopy(res))
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
