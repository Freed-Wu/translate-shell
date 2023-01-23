"""Process Input
================
"""
import logging
import os
import re
from pathlib import Path
from shlex import split
from subprocess import run

from ..__main__ import LANGS
from ..translators import TRANSLATORS

logger = logging.getLogger(__name__)
PATS = [
    re.compile(r"([a-z])([A-Z][a-z])"),
    re.compile(r"([a-zA-Z])_([a-zA-Z])"),
]
WHITESPACES_PAT = re.compile(r"\s+")
LANG_CODES = list(LANGS.keys()) + [""]


def process_text_redundant(text: str) -> str:
    """process_text_redundant.

    :param text:
    :type text: str
    :rtype: str
    """
    text = WHITESPACES_PAT.sub(" ", text)
    return text


def process_text_camelcase(text: str) -> str:
    """process_text_camelcase.

    :param text:
    :type text: str
    :rtype: str
    """
    text = PATS[0].sub(r"\1 \2", text)
    text = PATS[1].sub(r"\1 \2", text)
    return text


def process_text_multilines(text: str) -> str:
    """process_text_multilines.

    :param text:
    :type text: str
    :rtype: str
    """
    text = text.replace("-\n", "").replace("\n", "")
    return text


def process_lang_code(
    text: str, target_lang: str, source_lang: str, char: str = ":"
) -> tuple[str, str, str]:
    """process_lang_code.

    :param text:
    :type text: str
    :param target_lang:
    :type target_lang: str
    :param source_lang:
    :type source_lang: str
    :param char:
    :type char: str
    :rtype: tuple[str, str, str]
    """
    lang_codes = text.split(char)
    if (
        len(lang_codes) != 2
        or lang_codes[0] not in LANG_CODES
        or lang_codes[1] not in LANG_CODES
    ):
        return text, target_lang, source_lang
    if lang_codes[0]:
        source_lang = lang_codes[0]
    if lang_codes[1]:
        target_lang = lang_codes[1]
    if lang_codes[0] == lang_codes[1] == "":
        source_lang, target_lang = target_lang, source_lang
    logger.info("Now translate from " + source_lang + " to " + target_lang)
    return "", target_lang, source_lang


def process_translators_code(
    text: str, translators: str, char: str = "="
) -> tuple[str, str]:
    """process_translators_code.

    :param text:
    :type text: str
    :param translators:
    :type translators: str
    :param char:
    :type char: str
    :rtype: tuple[str, str]
    """
    if not text.startswith(char):
        return text, translators
    code = text.lstrip(char)
    if code == "":
        logger.info("current translators are " + translators)
        return "", translators
    if any(translator not in TRANSLATORS for translator in code.split(",")):
        logger.error(
            "Incorrect translators. Currently support "
            + " ".join(TRANSLATORS.keys())
        )
        return "", translators
    translators = code
    logger.info("Now use " + translators + " to translate")
    return "", translators


def process_shell(text: str, char: str = "!") -> str:
    """process_shell.

    :param text:
    :type text: str
    :param char:
    :type char: str
    :rtype: str
    """
    if not text.startswith(char):
        return text
    code = text.lstrip(char)
    tokens = split(code)
    if tokens == []:
        tokens = os.getenv("SHELL", "sh")
    try:
        run(tokens, check=True)
    except Exception as e:  # skipcq: PYL-W0703
        logger.error(e)
    return ""


def process_file(text: str, char: str = "<") -> str:
    """process_file.

    :param text:
    :type text: str
    :param char:
    :type char: str
    :rtype: str
    """
    if not text.startswith(char):
        return text
    code = text.lstrip(char)
    try:
        text = Path(code).read_text()
    except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
        logger.error(e)
        text = ""
    return text


def process_input(
    text: str,
    target_lang: str,
    source_lang: str,
    translators: str,
    is_repl: bool = False,
) -> tuple[str, str, str, str]:
    """process_input.

    :param text:
    :type text: str
    :param target_lang:
    :type target_lang: str
    :param source_lang:
    :type source_lang: str
    :param translators:
    :type translators: str
    :param is_repl:
    :type is_repl: bool
    :rtype: tuple[str, str, str, str]
    """
    if is_repl:
        text, target_lang, source_lang = process_lang_code(
            text, target_lang, source_lang
        )
        text, translators = process_translators_code(text, translators)
        text = process_shell(text)
        text = process_file(text)
    text = text.replace("\t", " ")
    text = text.strip()
    text = process_text_redundant(text)
    text = process_text_multilines(text)
    text = process_text_camelcase(text)
    text = text.lower()

    return text, target_lang, source_lang, translators
