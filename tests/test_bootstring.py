"""
Test suite for punycode Bootstring implementation.
"""

import pytest
from punycode.bootstring import Bootstring


class TestBootstring:
    """Test Bootstring static methods."""

    def test_is_basic(self):
        """Test code point basic check."""
        # ASCII range
        assert Bootstring.is_basic(0x00) is True
        assert Bootstring.is_basic(0x7F) is True
        assert Bootstring.is_basic(ord('a')) is True
        assert Bootstring.is_basic(ord('Z')) is True
        assert Bootstring.is_basic(ord('0')) is True

        # Non-ASCII
        assert Bootstring.is_basic(0x80) is False
        assert Bootstring.is_basic(0x100) is False
        assert Bootstring.is_basic(0x4E00) is False  # 中文

    def test_digit_value_uppercase(self):
        """Test digit value mapping for uppercase letters."""
        assert Bootstring.digit_value(ord('A')) == 0
        assert Bootstring.digit_value(ord('Z')) == 25

    def test_digit_value_lowercase(self):
        """Test digit value mapping for lowercase letters."""
        assert Bootstring.digit_value(ord('a')) == 0
        assert Bootstring.digit_value(ord('z')) == 25

    def test_digit_value_digits(self):
        """Test digit value mapping for digits."""
        assert Bootstring.digit_value(ord('0')) == 26
        assert Bootstring.digit_value(ord('9')) == 35

    def test_digit_value_invalid(self):
        """Test digit value for invalid characters."""
        assert Bootstring.digit_value(ord('-')) is None
        assert Bootstring.digit_value(ord(' ')) is None
        assert Bootstring.digit_value(0x80) is None

    def test_code_point_for_digit_lowercase(self):
        """Test code point for digit (lowercase output)."""
        assert Bootstring.code_point_for_digit(0) == ord('a')
        assert Bootstring.code_point_for_digit(25) == ord('z')

    def test_code_point_for_digit_digits(self):
        """Test code point for digit (digit output)."""
        assert Bootstring.code_point_for_digit(26) == ord('0')
        assert Bootstring.code_point_for_digit(35) == ord('9')

    def test_code_point_for_digit_invalid(self):
        """Test code point for invalid digit values."""
        with pytest.raises(ValueError):
            Bootstring.code_point_for_digit(-1)
        with pytest.raises(ValueError):
            Bootstring.code_point_for_digit(36)

    def test_adapt_firsttime(self):
        """Test bias adaptation for first delta."""
        # From RFC 3492 decoding trace example B
        bias = Bootstring.adapt(delta=19853, numpoints=1, firsttime=True)
        assert bias == 21

    def test_adapt_subsequent(self):
        """Test bias adaptation for subsequent deltas."""
        # From RFC 3492 decoding trace example B
        bias = Bootstring.adapt(delta=64, numpoints=2, firsttime=False)
        assert bias == 20

    def test_adapt_late_deltas(self):
        """Test bias adaptation for later deltas."""
        # From RFC 3492 decoding trace example B
        bias = Bootstring.adapt(delta=46301, numpoints=8, firsttime=False)
        assert bias == 84
        bias = Bootstring.adapt(delta=88531, numpoints=9, firsttime=False)
        assert bias == 90