"""Get prompt
=============
"""
from .misc import p10k_sections, section_path, section_time


def prompt_p10k(tl: str, sl: str, translators: str) -> str:
    """Prompt p10k.

    :param tl:
    :type tl: str
    :param sl:
    :type sl: str
    :param translators:
    :type translators: str
    :rtype: str
    """
    # Config
    insert_lang = "󰗊 {sl}:{tl}"
    insert_translators = " {translators}"
    insert_time = " {time}"
    time_format = "%H:%M:%S"

    sep = ""
    insert_text = " {text} "
    sections = [
        ("BLACK", "YELLOW", insert_lang.format(sl=sl, tl=tl)),
        (
            "GREEN",
            "BLACK",
            insert_translators.format(translators=translators),
        ),
        ("WHITE", "BLUE", section_path),
        (
            "BLACK",
            "WHITE",
            lambda: insert_time.format(time=section_time(time_format)),
        ),
    ]
    prompt = p10k_sections(sections, insert_text, sep)
    prompt += "\n❯ "
    return prompt


def process_clipboard(text: str, prompt: str) -> str:
    """Process clipboard.

    :param text:
    :type text: str
    :param prompt:
    :type prompt: str
    :rtype: str
    """
    if text:
        return "\n" + prompt + text
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
    prompt = prompt_p10k(tl, sl, translators)
    return process_clipboard(text, prompt)
