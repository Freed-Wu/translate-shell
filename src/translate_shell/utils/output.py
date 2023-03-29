"""Process Output
=================
"""
import json
from contextlib import suppress

from ..__main__ import ASSETS_PATH
from ..external.colorama import Fore, Style
from ..translate import Translation
from .misc import p10k_sections

NUMBER = json.loads(
    (ASSETS_PATH / "json" / "number.json").read_text(encoding="utf-8")
)


def process_output_firstline(rst: dict) -> str:
    """Process output firstline.

    :param rst:
    :type rst: dict
    :rtype: str
    """
    # Config
    insert_translator = " {translator}"
    insert_paraphrase = " {paraphrase}"
    insert_phonetic = " {phonetic}"

    sep = ""
    insert_text = " {text} "
    sections = [
        (
            "GREEN",
            "BLACK",
            insert_translator.format(translator=rst["translator"]),
        ),
        (
            "WHITE",
            "BLUE",
            insert_paraphrase.format(paraphrase=rst["paraphrase"]),
        ),
        ("BLACK", "WHITE", insert_phonetic.format(phonetic=rst["phonetic"])),
    ]

    prompt = p10k_sections(sections, insert_text, sep)
    return prompt


def process_output_explain(explain: list[str]) -> str:
    """Process output explain.

    :param explain:
    :type explain: list[str]
    :rtype: str
    """
    # Config
    insert_name = " {name}"

    sep = ""
    insert_text = " {text} "
    sections = [
        ("WHITE", "BLUE", insert_name.format(name=explain[0])),
    ]
    prompt = p10k_sections(sections, insert_text, sep)  # type: ignore
    prompt += " " + explain[1]
    return prompt


def process_output_pos(pos: str) -> str:
    """Process output pos.

    :param pos:
    :type pos: str
    :rtype: str
    """
    # Config
    insert_pos = " {pos}"

    sep = ""
    insert_text = " {text} "
    sections = [
        ("WHITE", "BLUE", insert_pos.format(pos=pos)),
    ]
    prompt = p10k_sections(sections, insert_text, sep)  # type: ignore
    return prompt


def process_output_p10k(translation: Translation) -> str:
    """Process output p10k.

    :param translation:
    :type translation: Translation
    :rtype: str
    """
    outputs = []
    for rst in translation.results:
        outputs += [process_output_firstline(rst)]
        for i, explain in enumerate(rst["explains"].items(), 1):
            outputs += [process_output_explain(explain)]
        for pos, details in rst["details"].items():
            outputs += [process_output_pos(pos)]
            for i, examples in enumerate(details.items(), 1):
                outputs += [
                    Fore.GREEN
                    + Style.BRIGHT
                    + " "
                    + NUMBER.get(str(i), str(i))
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
    with suppress(ImportError):
        from repl_python_wakatime import wakatime_hook

        wakatime_hook(
            plugin="translate-shell-wakatime", category="translating"
        )
    return rst
