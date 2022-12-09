"""Test output."""
import sys

import pytest

from translate_shell.utils.output import number_to_sign


class Test:
    """Test."""

    @pytest.mark.skipif(
        sys.platform == "win32", reason="'charmap' codec can't decode byte"
    )
    def test_number_to_sign(self):
        """Test number to sign."""
        sign = number_to_sign(42)
        assert sign == "④②"
