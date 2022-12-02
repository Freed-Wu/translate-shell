"""Get prompt
=============
"""
import os
from contextlib import suppress
from datetime import datetime
from pathlib import Path

from ..external.colorama import Back, Fore, Style, init

init()


def get_prompt_p10k(tl: str, sl: str, translators: str) -> str:
    """get_prompt_p10k.

    :param tl:
    :type tl: str
    :param sl:
    :type sl: str
    :param translators:
    :type translators: str
    :rtype: str
    """
    cwd = os.getcwd()
    if os.access(cwd, 7):
        logo = "  "
    else:
        logo = "  "
    with suppress(ValueError):
        cwd = str(Path(cwd).relative_to(Path.home()))
        if cwd == ".":
            cwd = "~"
        else:
            cwd = "~/" + cwd
    head, mid, tail = cwd.rpartition("/")
    prompt = (
        Fore.BLACK
        + Back.YELLOW
        + " 韛"
        + sl
        + ":"
        + tl
        + " "
        + Fore.YELLOW
        + Back.BLACK
        + ""
        + Fore.GREEN
        + "  "
        + translators
        + " "
        + Fore.BLACK
        + Back.BLUE
        + ""
        + Fore.WHITE
        + logo
        + head
        + mid
        + Style.BRIGHT
        + tail
        + " "
        + Style.RESET_ALL
        + Fore.BLUE
        + Back.WHITE
        + ""
        + Fore.BLACK
        + " "
        + datetime.now().strftime("%T")
        + " "
        + Fore.WHITE
        + Back.RESET
        + ""
        + Style.RESET_ALL
        + "\n"
        + "❯ "
    )
    return prompt


def process_clipboard(text: str, prompt: str) -> str:
    """process_clipboard.

    :param text:
    :type text: str
    :param prompt:
    :type prompt: str
    :rtype: str
    """
    if text:
        return "\n" + prompt + text
    else:
        return prompt


def get_prompt(text: str, tl: str, sl: str, translators: str) -> str:
    """Get prompt.

    ``text`` is clipboard content, which means you append it to result.

    :param text:
    :type text: str
    :param tl:
    :type tl: str
    :param sl:
    :type sl: str
    :param translators:
    :type translators: str
    :rtype: str
    """
    prompt = get_prompt_p10k(tl, sl, translators)
    return process_clipboard(text, prompt)
