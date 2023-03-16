r"""Notify
==========
"""
import re
from shlex import split
from shutil import which
from subprocess import run

from .. import APPNAME
from ..__main__ import ASSETS_PATH
from ..external.pynotifier import Notification

PAT = re.compile(r"\x1b\[[0-9;]+?m")
ICON_FILE = str(ASSETS_PATH / "images" / "translate-shell.png")


def notify(rst: str) -> None:
    """Notify.

    `<https://github.com/YuriyLisovskiy/pynotifier/issues/21>_`

    :param rst:
    :type rst: str
    :rtype: None
    """
    text = PAT.sub("", rst)
    if which("termux-toast"):
        run(split("termux-toast -g top") + [text], check=True)
    if which("termux-notification"):
        run(
            split(
                f"termux-notification -t Translation --group {APPNAME} "
                f"--icon {ICON_FILE} -c"
            )
            + [text],
            check=True,
        )
    else:
        Notification("Translation", text, 10, "low", ICON_FILE, APPNAME).send()
