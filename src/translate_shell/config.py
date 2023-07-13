"""config
=========

Define a class for user customization.
"""
from argparse import Namespace
from typing import Any, Literal

from .translate import Translation


class Configuration(Namespace):
    """Configuration."""

    __all__ = [
        "process_input",
        "process_output",
        "get_clipper",
        "get_prompt",
        "notify",
        "complete",
    ]

    def __init__(self) -> None:
        """Init.

        :rtype: None
        """
        super().__init__()
        self.source_lang: str = "auto"
        self.target_lang: str = "auto"
        self.translators: str = "google"
        self.format: Literal["text", "json", "yaml"] = "text"
        self.sleep_seconds: float = 0.1
        self.clipboard: bool = True
        self.options: dict[str, dict[str, Any]] = {}

    @staticmethod
    def process_input(
        text: str,
        target_lang: str,
        source_lang: str,
        translators: str,
        is_repl: bool = False,
    ) -> tuple[str, str, str, str]:
        """Process input.

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
        from .utils.input import process_input

        return process_input(
            text, target_lang, source_lang, translators, is_repl
        )

    @staticmethod
    def process_output(translation: Translation) -> str:
        """Process output.

        :param translation:
        :type translation: Translation
        :rtype: str
        """
        from .utils.output import process_output

        return process_output(translation)

    @staticmethod
    def get_clipper() -> list[str]:
        """Get clipper.

        :rtype: list[str]
        """
        from .utils.clippers import get_clipper

        return get_clipper()

    @staticmethod
    def get_prompt(text: str, tl: str, sl: str, translators: str) -> str:
        """Get prompt.

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
        from .utils.prompt import get_prompt

        return get_prompt(text, tl, sl, translators)

    @staticmethod
    def get_youdaozhiyun_app_info(*unused_args: Any) -> tuple[str, str]:
        """Get youdaozhiyun APP info.

        :param unused_args:
        :type unused_args: Any
        :rtype: tuple[str, str]
        """
        return "", ""

    @staticmethod
    def notify(rst: str) -> None:
        """Notify.

        :param rst:
        :type rst: str
        :rtype: None
        """
        from .utils.notify import notify

        notify(rst)

    @staticmethod
    def complete(text: str, state: int) -> str:
        """Complete.

        :param text:
        :type text: str
        :param state:
        :type state: int
        :rtype: str
        """
        from .utils.complete import complete

        return complete(text, state)
