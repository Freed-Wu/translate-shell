#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
See `man <../resources/man.html>`_.
"""
import json
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime
from pathlib import Path
from typing import NoReturn

from translate_shell import __version__
from translate_shell.external import shtab
from translate_shell.translators import TRANSLATORS

__file__ = vars().get("__file__", sys.argv[0])
ASSETS_PATH = Path(__file__).absolute().parent / "assets"
COPYRIGHT = "2022-" + str(datetime.now().year)
AUTHOR = "Wu Zhenyu"
VERSION = f"""trans {__version__}
Copyright (C) {COPYRIGHT}
Written by {AUTHOR}.
"""
EPILOG = (ASSETS_PATH / "txt" / "epilog.txt").read_text()
PREAMBLE = {
    "bash": (ASSETS_PATH / "bash" / "preamble.sh").read_text(),
    "zsh": (ASSETS_PATH / "zsh" / "preamble.zsh").read_text(),
}
PY_FILE = {
    "bash": "_shtab_greeter_compgen_PYFiles",
    "zsh": "_files -g '(*.py|*.PY)'",
    "tcsh": "f:*.py",
}
HISTORY_COMPLETE = {"zsh": "history_complete"}
TRANSLATOR_COMPLETE = {"zsh": f"""({" ".join(TRANSLATORS.keys())})"""}
LANGS = json.loads((ASSETS_PATH / "json" / "lang.json").read_text())
LANG_COMPLETE = {
    "zsh": "(("
    + " ".join(
        map(
            lambda d: d[0]
            + r"\:"
            + d[1].replace(" ", r"\ ").replace("(", r"\(").replace(")", r"\)"),
            LANGS.items(),
        )
    )
    + "))"
}
FORMATS = ["json", "yaml", "text"]
SETTINGS = [
    "config_file",
    "history_file",
    "dictionary_dirs",
    "translators",
    "languages",
    "formats",
    "clipper",
    "speaker",
]


def get_parser() -> ArgumentParser:
    """Get a parser for unit test.

    :rtype: ArgumentParser
    """
    parser = ArgumentParser(
        "trans", epilog=EPILOG, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument("-V", "--version", version=VERSION, action="version")
    shtab.add_argument_to(parser, preamble=PREAMBLE)  # type: ignore
    parser.add_argument(
        "--print-setting",
        choices=SETTINGS,
        default="",
        nargs="?",
        help="print some setting",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="increase logger level",
    )
    parser.add_argument(
        "-q", "--quiet", action="count", default=0, help="reduce logger level"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--no-clipboard",
        action="store_false",
        dest="clipboard",
        help="disable clipboard",
    )
    group.add_argument(
        "--clipboard", action="store_true", help="enable clipboard (default)"
    )
    parser.add_argument(
        "--config",
        help="use a python file as config",
    ).complete = PY_FILE  # type: ignore
    parser.add_argument(
        "--format",
        choices=FORMATS,
        default="text",
        help="output format for jq(1), yq(1). default: %(default)s",
    )
    parser.add_argument(
        "--translators",
        default="google",
        help="translate engines joined with ','. default: %(default)s",
    ).complete = TRANSLATOR_COMPLETE  # type: ignore
    parser.add_argument(
        "--target-lang",
        default="auto",
        help="target languages. default: %(default)s",
    ).complete = LANG_COMPLETE  # type: ignore
    parser.add_argument(
        "--source-lang",
        default="auto",
        help="source languages. default: %(default)s",
    ).complete = LANG_COMPLETE  # type: ignore
    parser.add_argument(
        "text", nargs="*"
    ).complete = HISTORY_COMPLETE  # type: ignore
    return parser


def main() -> None | NoReturn:
    """``python -m translate_shell`` call this function.
    Parse arguments and provide shell completions.

    :rtype: None
    """
    parser = get_parser()
    args = parser.parse_args()
    if args.print_setting != "":
        from translate_shell.utils.setting import print_setting

        exit(print_setting(args.print_setting))

    try:
        import vim  # type: ignore
    except ImportError:
        if not sys.stdin.isatty():
            args.text = [sys.stdin.read()] + args.text
    if args.text:
        from translate_shell.ui.cli import run
    else:
        from translate_shell.ui.repl import run
    run(args)


if __name__ == "__main__":
    main()
