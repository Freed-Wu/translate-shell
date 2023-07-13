"""Test translators."""
import json

from translate_shell.translate import translate

from . import ASSETS_PATH


class Test:
    """Test."""

    @staticmethod
    def test_google() -> None:
        """Test google"""
        rst = vars(translate("The Mythical Man-Month", "zh_CN"))
        expected = json.loads(
            (ASSETS_PATH / "json" / "google.json").read_text()
        )
        assert rst == expected
