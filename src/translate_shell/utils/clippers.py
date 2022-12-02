"""Clippers
===========
"""
import logging
import os
from shlex import split
from shutil import which

logger = logging.getLogger(__name__)


def get_clipper() -> list[str]:
    """Get default clipper.

    don't use try/catch to call these program, fork will cost more time than
    judge existence of these program by `which()`

    https://github.com/neovim/neovim/blob/ef1d291f29961ae10cc122e92fb2419cbbd29f3b/runtime/autoload/provider/clipboard.vim#L87-L151

    :rtype: list[str]
    """
    cmds = []
    if os.getenv("WAYLAND_DISPLAY"):
        cmds += ["wl-paste --no-newline"]
    if os.getenv("DISPLAY"):
        cmds += ["xsel -o", "xclip -o"]
    cmds += [
        "pbpaste",
        "lemonade paste",
        "doitclient wclip -r",
        "win32yank -o --lf",
        "getclip",
        "clip",
        "termux-clipboard-get",
        "tmux save-buffer -",
    ]

    for cmd in cmds:
        tokens = split(cmd)
        if which(tokens[0]):
            return tokens
    logger.warning("Please install any clipper firstly!")
    return []
