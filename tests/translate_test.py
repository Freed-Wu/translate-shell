"""Test translators."""
import json

from translate_shell.translate import translate

from . import ASSETS_PATH


class Test:
    """Test."""

    @staticmethod
    def test_google() -> None:
        """Test google"""
        rst = dict(translate("The Mythical Man-Month", "zh_CN").to_dict())
        expected = json.loads(
            (ASSETS_PATH / "json" / "google.json").read_text()
        )
        assert rst == expected
