#!/usr/bin/env python
"""This module can be called by
`python -m <https://docs.python.org/3/library/__main__.html>`_
to check if it imports any variable don't owned by any true module.

Call ``--print-completion`` will warn when shtab is not installed.

https://github.com/iterative/shtab/blob/95b0e3092cd4dcf1ac2871d44cebda01a89992df/shtab/__init__.py#L786-L789
"""
from argparse import Action, ArgumentParser
from typing import Any, NoReturn

FILE = None
DIRECTORY = DIR = None


class _PrintCompletionAction(Action):
    """Print completion action."""

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Any,
        values: list[Any],
        option_string: str | None = None,
    ) -> NoReturn:
        """__call__

        :param parser:
        :type parser: ArgumentParser
        :param namespace:
        :type namespace: Any
        :param values:
        :type values: list[Any]
        :param option_string:
        :type option_string: str | None
        :rtype: NoReturn
        """
        print("Please install shtab firstly!")
        parser.exit(0)


def add_argument_to(
    parser: ArgumentParser, *args: list[Any], **kwargs: dict[str, Any]
) -> ArgumentParser:
    """Add completion argument to parser.

    :param parser:
    :type parser: ArgumentParser
    :param args:
    :type args: list[Any]
    :param kwargs:
    :type kwargs: dict[str, Any]
    :rtype: ArgumentParser
    """
    Action.complete = None  # type: ignore
    parser.add_argument(
        "--print-completion",
        choices=["bash", "zsh", "tcsh"],
        action=_PrintCompletionAction,
        help="print shell completion script",
    )
    return parser


if __name__ == "__main__":
    from ..__main__ import main_once as _main

    _main(__file__, vars())
