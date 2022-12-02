"""Test cmd."""
from contextlib import suppress

from translate_shell.__main__ import EPILOG, VERSION, get_parser

from . import ASSETS_PATH

parser = get_parser()


class Test:
    """Test."""

    def test_help(self, capsys):
        """Test help.

        :param capsys:
        """
        with suppress(SystemExit):
            parser.parse_args(["--help"])
        captured = capsys.readouterr()
        expected = (ASSETS_PATH / "txt" / "help.txt").read_text()
        assert captured.out == expected + EPILOG

    def test_version(self, capsys):
        """Test version.

        :param capsys:
        """
        with suppress(SystemExit):
            parser.parse_args(["--version"])
        captured = capsys.readouterr()
        assert captured.out == VERSION
