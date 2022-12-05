"""Process Output
=================
"""
import json

from ..__main__ import ASSETS_PATH
from ..translate import Translation

NUMBER = json.loads((ASSETS_PATH / "json" / "number.json").read_text())


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


def process_output_p10k(translation: Translation, plain: bool = False) -> str:
    """process_output_p10k.

    :param translation:
    :type translation: Translation
    :param plain:
    :type plain: bool
    :rtype: str
    """
    if plain:
        from ..external.colorama.__main__ import Back, Fore, Style, init
    else:
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
            + "  "
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
    return process_output_p10k(translation)


def process_output_plain(translation: Translation) -> str:
    """Process output plain.

    :param translation:
    :type translation: Translation
    :rtype: str
    """
    return process_output_p10k(translation, True)
