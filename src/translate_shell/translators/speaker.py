"""Speaker
==========

Play the pronunciation.
"""
import logging
from shlex import split
from shutil import which
from subprocess import check_output
from typing import Any

from . import Translator

logger = logging.getLogger(__name__)


class Speaker(Translator):
    """Speaker."""

    def __init__(self) -> None:
        """Init.

        :rtype: None
        """
        super().__init__("speaker")

    def __call__(
        self, text: str, tl: str, sl: str, option: dict[str, Any]
    ) -> None:
        """Call.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :rtype: None
        """
        tokens = option.get("get_speaker", self.__class__.get_speaker)(text)
        if tokens:
            check_output(tokens)

    @staticmethod
    def get_speaker(query: str) -> list[str]:
        """Get default speaker.

        https://github.com/felixonmars/ydcv/blob/2db05d41e1fc927cd0c49aad101ed6a21ad92c2b/src/ydcv.py#L199-L235

        :param query:
        :type query: str
        :rtype: list[str]
        """
        cmds = [
            "termux-tts-speak " + query,
            "espeak " + query,
            "festival --tts " + query,
            "say " + query,
        ]

        for cmd in cmds:
            tokens = split(cmd)
            if which(tokens[0]):
                return tokens
        logger.warning("Please install any speaker firstly!")
        return []
