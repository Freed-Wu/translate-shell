r"""Notify
==========
"""

import re
from contextlib import suppress

from .. import APPNAME
from ..__main__ import ASSETS_PATH

Notify = None
termux = None

with suppress(ImportError):
    from notifypy import Notify

with suppress(ImportError):
    import termux

PAT = re.compile(r"\x1b\[[0-9;]+?m")
ICON_FILE = str(ASSETS_PATH / "images" / "translate-shell.png")


def notify(rst: str) -> None:
    """Notify. use termux-api or notify-py.

    `<https://github.com/ms7m/notify-py/issues/72>_`

    :param rst:
    :type rst: str
    :rtype: None
    """
    text = PAT.sub("", rst)
    if termux:
        termux.UI.toast(text, position="top")
        termux.Notification.notify(
            "Translation", text, ("c",), {"group": APPNAME, "icon": ICON_FILE}
        )
    if Notify:
        Notify("Translation", text, APPNAME, "low", ICON_FILE).send()
