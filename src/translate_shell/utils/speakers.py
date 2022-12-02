"""Speakers
===========
"""
import logging
from shlex import split
from shutil import which

logger = logging.getLogger(__name__)


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
