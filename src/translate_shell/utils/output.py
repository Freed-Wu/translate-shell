"""Process Output
=================
"""
import json
import re
from shlex import split
from shutil import which
from subprocess import run

from .. import __name__ as NAME
from ..__main__ import ASSETS_PATH
from ..external.pynotifier import Notification
from ..translate import Translation
from ..ui import is_sub_thread

PAT = re.compile(r"\x1b\[[0-9;]+?m")
APP_NAME = NAME.replace("_", "-")
NUMBER = json.loads((ASSETS_PATH / "json" / "number.json").read_text())
ICON_FILE = str(ASSETS_PATH / "images" / "icon.png")


def number_to_sign(number: int) -> str:
    """number_to_sign.

    :param number:
    :type number: int
    :rtype: str
    """
    sign = ""
    while number > 0:
        last_digit = number % 10
        sign = NUMBER.get(str(last_digit), "") + sign
        number = number // 10
    return sign


def process_output_p10k(translation: Translation) -> str:
    """process_output_p10k.

    :param translation:
    :type translation: Translation
    :rtype: str
    """
    from ..external.colorama import Back, Fore, Style, init

    init()
    outputs = []
    for rst in translation.results:
        outputs += [
            Fore.GREEN
            + Back.BLACK
            + "  "
            + rst["translator"]
            + " "
            + Fore.BLACK
            + Back.BLUE
            + ""
            + Fore.WHITE
            + "  "
            + Style.BRIGHT
            + rst["paraphrase"]
            + " "
            + Style.RESET_ALL
            + Fore.BLUE
            + Back.WHITE
            + ""
            + Fore.BLACK
            + "  "
            + rst["phonetic"]
            + " "
            + Fore.WHITE
            + Back.RESET
            + ""
            + Style.RESET_ALL
        ]
        for i, explain in enumerate(rst["explains"].items(), 1):
            outputs += [
                Fore.WHITE
                + Back.BLUE
                + "  "
                + explain[0]
                + " "
                + Fore.BLUE
                + Back.RESET
                + ""
                + Style.RESET_ALL
                + " "
                + explain[1]
            ]
        for pos, details in rst["details"].items():
            outputs += [
                Fore.WHITE
                + Back.BLUE
                + "  "
                + pos
                + " "
                + Fore.BLUE
                + Back.RESET
                + ""
                + Style.RESET_ALL
            ]
            for i, examples in enumerate(details.items(), 1):
                outputs += [
                    Fore.GREEN
                    + Style.BRIGHT
                    + " "
                    + number_to_sign(i)
                    + " "
                    + Style.RESET_ALL
                    + " "
                    + examples[0]
                    .replace("<em>", Fore.RED)
                    .replace("</em>", Fore.RESET)
                ]
                if examples[1] != "":
                    outputs += [examples[1]]
    output = "\n".join(outputs)
    return output


def process_output(translation: Translation) -> str:
    """Process output.

    :param translation:
    :type translation: Translation
    :rtype: str
    """
    rst = process_output_p10k(translation)
    if rst and is_sub_thread():
        # https://github.com/YuriyLisovskiy/pynotifier/issues/21
        text = PAT.sub("", rst)
        if which("termux-toast"):
            run(split("termux-toast -g top") + [text])
        if which("termux-notification"):
            run(
                split(
                    "termux-notification -t 'Translation' --icon "
                    + ICON_FILE
                    + " -c"
                )
                + [text]
            )
        Notification(
            "Translation",
            text,
            10,
            "low",
            ICON_FILE,
            APP_NAME,
        ).send()
    return rst
