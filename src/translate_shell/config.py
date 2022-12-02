"""config
=========

Define a class for user customization.
"""
from argparse import Namespace

from .__main__ import get_parser
from .translate import Translation


class Configuration(Namespace):
    """Configuration."""

    __all__ = [
        "process_input",
        "process_output",
        "get_clipper",
        "get_speaker",
        "get_prompt",
        "get_youdaozhiyun_app_info",
    ]

    def __init__(self) -> None:
        """__init__.

        :rtype: None
        """
        # Don't use ``setattr`` to provide information to LSP.
        super().__init__()
        actions = get_parser()._option_string_actions
        self.source_lang: str = actions["--source-lang"].default
        self.target_lang: str = actions["--target-lang"].default
        self.translators: str = actions["--translators"].default
        self.format: str = actions["--format"].default

    def process_input(
        self,
        text: str,
        target_lang: str,
        source_lang: str,
        translators: str,
        is_repl: bool = False,
    ) -> tuple[str, str, str, str]:
        """process_input.

        :param self:
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

    def process_output(self, translation: Translation) -> str:
        """Process output.

        :param translation:
        :type translation: Translation
        :rtype: str
        """
        from .utils.output import process_output

        return process_output(translation)

    def get_clipper(self) -> list[str]:
        """Get clipper.

        :rtype: list[str]
        """
        from .utils.clippers import get_clipper

        return get_clipper()

    def get_speaker(self, query: str) -> list[str]:
        """Get speaker.

        :param query:
        :type query: str
        :rtype: list[str]
        """
        from .utils.speakers import get_speaker

        return get_speaker(query)

    def get_prompt(self, text: str, tl: str, sl: str, translators: str) -> str:
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

    def get_youdaozhiyun_app_info(self) -> tuple[str, str]:
        """Get youdaozhiyun app info.

        :rtype: tuple[str, str]
        """
        from .utils.youdaozhiyun import get_youdaozhiyun_app_info

        return get_youdaozhiyun_app_info()
