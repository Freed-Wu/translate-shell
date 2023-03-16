#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
See `man <../resources/man.html>`_.
"""
import json
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from typing import Literal, NoReturn

from translate_shell import __version__  # type: ignore
from translate_shell._metainfo import (  # type: ignore
    DESCRIPTION,
    EPILOG,
    VERSION,
)
from translate_shell.config import Configuration
from translate_shell.external import shtab
from translate_shell.translators import TRANSLATORS

# for vim
__file__ = vars().get("__file__", sys.argv[0])
ASSETS_PATH = Path(__file__).absolute().parent / "assets"
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
TYPE = Literal["json", "yaml", "text"]
FORMATS = list(TYPE.__args__)  # type: ignore
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
config = Configuration()


def get_parser() -> ArgumentParser:
    """Get a parser for unit test.
    Provide shell completions.

    :rtype: ArgumentParser
    """
    parser = ArgumentParser(
        "trans",
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--no-notification",
        action="store_false",
        dest="notification",
        help="disable notification",
    )
    group.add_argument(
        "--notification",
        action="store_true",
        help="enable notification (default)",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=config.sleep_seconds,
        help="avoid checkout clipboard too frequently. default: %(default)s",
    )
    parser.add_argument(
        "--config",
        help="use a python file as config",
    ).complete = PY_FILE  # type: ignore
    parser.add_argument(
        "--format",
        choices=FORMATS,
        default=config.format,
        help="output format for jq(1), yq(1). default: %(default)s",
    )
    parser.add_argument(
        "--translators",
        default=config.translators,
        help="translate engines joined with ','. default: %(default)s",
    ).complete = TRANSLATOR_COMPLETE  # type: ignore
    parser.add_argument(
        "--target-lang",
        default=config.target_lang,
        help="target languages. default: %(default)s",
    ).complete = LANG_COMPLETE  # type: ignore
    parser.add_argument(
        "--source-lang",
        default=config.source_lang,
        help="source languages. default: %(default)s",
    ).complete = LANG_COMPLETE  # type: ignore
    parser.add_argument(
        "text",
        nargs="*",
        help="text needed to be translated, empty means entering REPL",
    ).complete = HISTORY_COMPLETE  # type: ignore
    return parser


def main() -> None | NoReturn:
    """``python -m translate_shell`` call this function.
    Parse arguments is before init configuration to provide ``--config``.

    :rtype: None | NoReturn
    """
    parser = get_parser()
    args = parser.parse_args()

    if args.print_setting != "":
        from translate_shell.utils.setting import print_setting

        sys.exit(print_setting(args.print_setting))

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
