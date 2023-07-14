r"""Openai
==========
"""
import openai

from . import LLMTranslator


class OpenaiTranslator(LLMTranslator):
    """Openaitranslator."""

    def __init__(self) -> None:
        """Init.

        :rtype: None
        """
        super().__init__("openai")
        self.create_chat_completion = openai.ChatCompletion.create  # type: ignore
