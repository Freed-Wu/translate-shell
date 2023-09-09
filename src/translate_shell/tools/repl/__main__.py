r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime

from ... import __name__ as NAME
from ... import __version__

try:
    import shtab
except ImportError:
    from ...external import shtab

NAME = NAME.replace("_", "-")
VERSION = rf"""{NAME} {__version__}
Copyright (C) {datetime.now().year}
Written by Wu Zhenyu
"""
EPILOG = """
Report bugs to <wuzhenyu@ustc.edu>.
"""


def get_parser() -> ArgumentParser:
    r"""Get a parser for unit test."""
    parser = ArgumentParser(
        epilog=EPILOG, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", version=VERSION, action="version")
    shtab.add_argument_to(parser)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--no-wakatime",
        action="store_false",
        dest="wakatime",
        help="disable wakatime",
    )
    group.add_argument(
        "--wakatime", action="store_true", help="enable wakatime (default)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--no-codestats",
        action="store_false",
        dest="codestats",
        help="disable codestats",
    )
    group.add_argument(
        "--codestats", action="store_true", help="enable codestats (default)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--no-jedi",
        action="store_false",
        dest="jedi",
        help="disable jedi",
    )
    group.add_argument(
        "--jedi", action="store_true", help="enable jedi (default)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--no-rich",
        action="store_false",
        dest="rich",
        help="disable rich",
    )
    group.add_argument(
        "--rich", action="store_true", help="enable rich (default)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--no-ps1",
        action="store_false",
        dest="ps1",
        help="disable ps1",
    )
    group.add_argument(
        "--ps1", action="store_true", help="enable ps1 (default)"
    )
    return parser


def main() -> None:
    r"""Parse arguments and provide shell completions."""
    parser = get_parser()
    args = parser.parse_args()

    from .main import interact

    interact(**args.__dict__)


if __name__ == "__main__":
    main()
