r"""Notify
==========
"""
import re
from contextlib import suppress
from shlex import split
from shutil import which
from subprocess import run

from .. import APPNAME
from ..__main__ import ASSETS_PATH

with suppress(ImportError):
    from pynotifier import Notification, NotificationClient
    from pynotifier.backends import platform

    client = NotificationClient()
    client.register_backend(platform.Backend())

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
    # https://github.com/YuriyLisovskiy/pynotifier/pull/29
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
        with suppress(NameError):
            client.notify_all(
                Notification(
                    title="Translation",
                    message=text,
                    duration=10,
                    urgency="low",
                    icon_path=ICON_FILE,
                    app_name=APPNAME,
                )
            )
