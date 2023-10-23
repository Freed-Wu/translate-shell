r"""Openai
==========
"""
from dataclasses import dataclass

import openai

from . import LLMTranslator


@dataclass
class OpenaiTranslator(LLMTranslator):
    """Openaitranslator."""

    name: str = "openai"

    def __post_init__(self) -> None:
        """Post init.

        :rtype: None
        """
        self.create_chat_completion = openai.ChatCompletion.create  # type: ignore
