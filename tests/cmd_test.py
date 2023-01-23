"""Test cmd."""
from contextlib import suppress

from translate_shell.__main__ import get_parser
from translate_shell._metainfo import (  # type: ignore
    DESCRIPTION,
    EPILOG,
    VERSION,
)

from . import ASSETS_PATH

parser = get_parser()
USAGE = (ASSETS_PATH / "txt" / "usage.txt").read_text()
OPTIONS = (ASSETS_PATH / "txt" / "options.txt").read_text()
HELP = "\n".join([USAGE, DESCRIPTION, "", OPTIONS, EPILOG])


class Test:
    """Test."""

    @staticmethod
    def test_help(capsys) -> None:
        """Test help.

        :param capsys:
        """
        with suppress(SystemExit):
            parser.parse_args(["--help"])
        captured = capsys.readouterr()
        assert captured.out.strip() == HELP

    @staticmethod
    def test_version(capsys) -> None:
        """Test version.

        :param capsys:
        """
        with suppress(SystemExit):
            parser.parse_args(["--version"])
        captured = capsys.readouterr()
        assert captured.out.strip() == VERSION.strip()
