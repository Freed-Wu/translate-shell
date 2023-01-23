"""Test translators."""
import json
import sys

import pytest

from translate_shell.translate import translate

from . import ASSETS_PATH


class Test:
    """Test."""

    @pytest.mark.skipif(
        sys.platform == "win32", reason="'charmap' codec can't decode byte"
    )
    def test_google(self) -> None:
        """Test google"""
        rst = vars(translate("The Mythical Man-Month", "zh_TW"))
        expected = json.loads(
            (ASSETS_PATH / "json" / "google.json").read_text()
        )
        assert rst == expected
