r"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_.
"""
import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime

import yaml

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
    action = yaml.safe_load(
        open(os.path.join(os.path.dirname(__file__), "action.yml"))
    )
    parser = ArgumentParser(
        description=action["description"],
        epilog=EPILOG,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", version=VERSION, action="version")
    shtab.add_argument_to(parser)
    for input, info in action["inputs"].items():
        default = os.getenv(
            "INPUT_" + input.upper().replace("-", "_"),
            info.get("default", ""),
        )
        if input == "option":
            default = default.split()
            action = "append"
        else:
            action = "store"
        parser.add_argument(
            "--" + input,
            # https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#example-specifying-inputs
            default=default,
            help=info["description"] + ". default: %(default)s",
            action=action,
        )
    parser.add_argument(
        "workspace",
        default=os.getenv("GITHUB_WORKSPACE", "."),
        help="the directory which contains *.po. default: %(default)s",
    )
    return parser


def main() -> None:
    r"""Parse arguments and provide shell completions."""
    parser = get_parser()
    args = parser.parse_args()

    from .main import run

    run(args)


if __name__ == "__main__":
    main()
