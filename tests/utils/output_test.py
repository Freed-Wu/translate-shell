"""Test output."""
from translate_shell.utils.output import number_to_sign


class Test:
    """Test."""

    def test_number_to_sign(self):
        """test_number_to_sign."""
        sign = number_to_sign(42)
        assert sign == "④②"
