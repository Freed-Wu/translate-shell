"""Graphics User Interface
==========================
"""
from argparse import Namespace

from .. import __name__ as NAME
from ..__main__ import ICON_FILE
from ..external.pynotifier import Notification

APP_NAME = NAME.replace("_", "-")


class GUIPrint:
    """GUIPrint."""

    def __init__(self, args: Namespace) -> None:
        """__init__.

        :param args:
        :type args: Namespace
        :rtype: None
        """
        self.duration = args.duration

    def __call__(self, text: str, end: str = "") -> None:
        """__call__.

        :param text:
        :type text: str
        :param end:
        :type end: str
        :rtype: None
        """
        if text:
            Notification(
                "Translate Result",
                text,
                self.duration,
                "low",
                ICON_FILE,
                APP_NAME,
            ).send()
