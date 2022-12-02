"""Speaker
==========

Play the pronunciation.
"""
from subprocess import check_output

from ..ui import get_speaker
from . import Translator


class Speaker(Translator):
    """Speaker."""

    def __init__(self) -> None:
        """__init__.

        :rtype: None
        """
        super().__init__("speaker")

    def __call__(self, text: str, tl: str, sl: str) -> None:
        """__call__.

        :param text:
        :type text: str
        :param tl:
        :type tl: str
        :param sl:
        :type sl: str
        :rtype: None
        """
        tokens = get_speaker(text)
        if tokens:
            check_output(tokens)
