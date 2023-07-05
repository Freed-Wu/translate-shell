r"""Misc
========
"""
import os
import platform
import sys
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import Callable

from ..external.colorama import Back, Fore, Style, init

init()


def section_os() -> str:
    """Section os.

    :rtype: str
    """
    os_name = sys.platform
    if os_name.startswith("linux"):
        try:
            # python 3.10 support platform.freedesktop_os_release()
            os_name = platform.freedesktop_os_release().get("ID", "")
        except AttributeError:
            pass
        except OSError:
            if os.getenv("PREFIX") == "/data/data/com.termux/files/usr":
                os_name = "android"

    icons = {
        "emscripten": "ﰍ",
        "linux": "",
        "linux2": "",
        "linux3": "",
        "hurd": "",
        "darwin": "",
        "dos": "",
        "win16": "",
        "win32": "",
        "cygwin": "",
        "java": "",
        "android": "",
        "arch": "",
        "gentoo": "",
        "ubuntu": "",
        "cent": "",
        "debian": "",
        "nixos": "",
    }
    return icons.get(os_name, "?")


def section_path() -> str:
    """Section path.

    :rtype: str
    """
    cwd = os.getcwd()
    if os.access(cwd, 7):
        logo = " "
    else:
        logo = " "
    with suppress(ValueError):
        cwd = str(Path(cwd).relative_to(Path.home()))
        if cwd == ".":
            cwd = "~"
        else:
            cwd = "~/" + cwd
    head, mid, tail = cwd.rpartition("/")
    path = logo + head + mid + Style.BRIGHT + tail
    return path


def section_time(time_format: str = "%H:%M:%S") -> str:
    """Section time.

    :param time_format:
    :type time_format: str
    :rtype: str
    """
    return datetime.now().strftime(time_format)


def p10k_sections(
    sections: list[tuple[str, str, str | Callable[[], str]]],
    insert_text: str = " {text} ",
    sep: str = "",
) -> str:
    """p10k sections.

    :param sections:
    :type sections: list[tuple[str, str, str | Callable[[], str]]]
    :param insert_text:
    :type insert_text: str
    :param sep:
    :type sep: str
    :rtype: str
    """
    prompt = ""
    last_bg = ""
    for section in sections:
        fg, bg, action = section
        if isinstance(action, str):
            text = action
        elif isinstance(action, Callable):
            text = action()
        else:
            raise NotImplementedError(f"{type(action)} is not supported!")
        text = insert_text.format(text=text)
        if last_bg:
            prompt += getattr(Fore, last_bg) + getattr(Back, bg) + sep
        prompt += getattr(Fore, fg) + getattr(Back, bg) + text
        last_bg = bg
    prompt += getattr(Fore, last_bg) + Back.RESET + sep + Style.RESET_ALL
    return prompt
