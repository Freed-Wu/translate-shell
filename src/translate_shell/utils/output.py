"""Process Output
=================
"""
import json
from contextlib import suppress

from ..__main__ import ASSETS_PATH
from ..external.colorama import Fore, Style
from ..translate import Translations
from ..translators import Translation
from .section import p10k_sections

NUMBER = json.loads(
    (ASSETS_PATH / "json" / "number.json").read_text(encoding="utf-8")
)


def process_output_firstline(rst: Translation) -> str:
    """Process output firstline.

    :param rst:
    :type rst: Translation
    :rtype: str
    """
    # Config
    insert_translator = " {translator}"
    insert_paraphrase = " {paraphrase}"
    insert_phonetic = " {phonetic}"

    sections = [
        (
            "GREEN",
            "BLACK",
            insert_translator.format(translator=rst.translator),
        ),
        (
            "WHITE",
            "BLUE",
            insert_paraphrase.format(paraphrase=rst.paraphrase),
        ),
        ("BLACK", "WHITE", insert_phonetic.format(phonetic=rst.phonetic)),
    ]

    prompt = p10k_sections(sections)
    return prompt


def process_output_explain(explain: tuple[str, str]) -> str:
    """Process output explain.

    :param explain:
    :type explain: tuple[str, str]
    :rtype: str
    """
    # Config
    insert_name = " {name}"

    sections = [
        ("WHITE", "BLUE", insert_name.format(name=explain[0])),
    ]
    prompt = p10k_sections(sections)  # type: ignore
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

    sections = [
        ("WHITE", "BLUE", insert_pos.format(pos=pos)),
    ]
    prompt = p10k_sections(sections)  # type: ignore
    return prompt


def process_output_p10k(translations: Translations) -> str:
    """Process output p10k.

    :param translations:
    :type translations: Translations
    :rtype: str
    """
    outputs = []
    for rst in translations.results:
        outputs += [process_output_firstline(rst)]
        for i, explain in enumerate(rst.explains.items(), 1):
            outputs += [process_output_explain(explain)]
        for pos, details in rst.details.items():
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


def process_output(translations: Translations) -> str:
    """Process output.

    :param translations:
    :type translations: Translations
    :rtype: str
    """
    rst = process_output_p10k(translations)
    with suppress(ImportError):
        from repl_python_wakatime.hooks.wakatime import wakatime_hook

        wakatime_hook(
            plugin="translate-shell-wakatime", category="translating"
        )
    return rst
