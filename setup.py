"""Set up."""
import gzip
import logging
import os
import sys
from argparse import ArgumentParser
from subprocess import check_output

from setuptools import setup
from shtab import complete

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "src")
sys.path.insert(0, src)

from translate_shell.__main__ import get_parser  # noqa: E402

logger = logging.getLogger(__name__)
parser = get_parser()
prog = parser.prog
shells = {
    "bash": prog,
    "zsh": "_" + prog,
    "tcsh": prog + ".csh",
}
dist = os.path.join(here, "dist")
os.makedirs(dist, exist_ok=True)
gzip_name = os.path.join(dist, prog + ".1.gz")


def generate_completions(
    parser: ArgumentParser, shells: dict[str, str], dist: str
) -> None:
    """Generate completions.

    :param parser:
    :type parser: ArgumentParser
    :param shells:
    :type shells: dict[str, str]
    :param dist:
    :type dist: str
    :rtype: None
    """
    for shell, name in shells.items():
        content = complete(parser, shell)
        with open(os.path.join(dist, name), "w") as f:
            f.write(content)


def generate_man(gzip_name: str) -> None:
    """Generate man.

    :param gzip_name:
    :type gzip_name: str
    :rtype: None
    """
    try:
        with gzip.open(gzip_name, "wb") as f:
            output = check_output(  # nosec B603 B607
                ["help2man", "scripts/trans"]
            )
            f.write(output)
    except FileNotFoundError:
        logger.warning("Please install help2man firstly!")


if __name__ == "__main__":
    generate_completions(parser, shells, dist)
    generate_man(gzip_name)
    setup()
