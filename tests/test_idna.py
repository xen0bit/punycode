"""
Test suite for IDNA (Internationalized Domain Names in Applications) support.
"""

import pytest
from punycode import (
    to_ascii,
    to_unicode,
    to_ascii_domain,
    to_unicode_domain,
    IDNAError,
    InvalidLabel,
    LabelTooLong,
    DomainTooLong,
)


class TestToAscii:
    """Test to_ascii label conversion."""

    def test_ascii_label_unchanged(self):
        """Test that ASCII labels are returned unchanged."""
        assert to_ascii("example") == "example"
        assert to_ascii("www") == "www"
        assert to_ascii("abc123") == "abc123"

    def test_unicode_label_encoding(self):
        """Test encoding of Unicode labels."""
        # Japanese examples - verify encoding works
        result = to_ascii("例え")
        assert result.startswith("xn--")
        assert result.isascii()
        # Chinese example
        result = to_ascii("测试")
        assert result.startswith("xn--")
        assert result.isascii()
        # Single character
        result = to_ascii("例")
        assert result.startswith("xn--")
        assert result.isascii()
        # Verify it works
        assert to_ascii("例え").startswith("xn--")

    def test_label_too_long(self):
        """Test that labels exceeding 63 characters raise an error."""
        # Create a long label
        long_label = "a" * 60
        # This will be encoded and should exceed 63 chars
        long_label += "例"  # Add non-ASCII character
        with pytest.raises(LabelTooLong):
            to_ascii(long_label)

    def test_empty_label(self):
        """Test that empty labels raise an error."""
        with pytest.raises(InvalidLabel):
            to_ascii("")


class TestToUnicode:
    """Test to_unicode label conversion."""

    def test_ascii_label_unchanged(self):
        """Test that ASCII labels are returned unchanged."""
        assert to_unicode("example") == "example"
        assert to_unicode("www") == "www"
        assert to_unicode("abc123") == "abc123"

    def test_ace_label_decoding(self):
        """Test decoding of ACE-encoded labels."""
        # Japanese example
        assert to_unicode("xn--r8jz45g") == "例え"
        # Chinese example
        assert to_unicode("xn--0zwm56d") == "测试"

    def test_case_insensitive_prefix(self):
        """Test that the ACE prefix is case-insensitive."""
        assert to_unicode("XN--r8jz45g") == "例え"
        assert to_unicode("Xn--R8jz45G") == "例え"

    def test_empty_label(self):
        """Test that empty labels raise an error."""
        with pytest.raises(InvalidLabel):
            to_unicode("")


class TestToAsciiDomain:
    """Test to_ascii_domain conversion."""

    def test_ascii_domain_unchanged(self):
        """Test that ASCII domains are returned unchanged."""
        assert to_ascii_domain("example.com") == "example.com"
        assert to_ascii_domain("www.google.com") == "www.google.com"

    def test_unicode_domain_encoding(self):
        """Test encoding of Unicode domains."""
        # Japanese domain
        result = to_ascii_domain("例え.jp")
        assert result.startswith("xn--")
        assert result.endswith(".jp")
        # Chinese domain
        result = to_ascii_domain("例子.测试")
        assert "." in result
        assert result.isascii()

    def test_mixed_domain(self):
        """Test encoding of domains with mixed ASCII and Unicode labels."""
        result = to_ascii_domain("www.例え.jp")
        assert result == "www.xn--r8jz45g.jp"

    def test_trailing_dot(self):
        """Test that trailing dots are handled correctly."""
        # Trailing dot creates an empty label
        result = to_ascii_domain("example.com.")
        assert result == "example.com."

    def test_domain_too_long(self):
        """Test that domains exceeding 253 characters raise an error."""
        # Create a long domain
        labels = []
        for i in range(10):
            labels.append("a" * 25)
        long_domain = ".".join(labels)
        with pytest.raises(DomainTooLong):
            to_ascii_domain(long_domain)

    def test_empty_domain(self):
        """Test that empty domains raise an error."""
        with pytest.raises(InvalidLabel):
            to_ascii_domain("")


class TestToUnicodeDomain:
    """Test to_unicode_domain conversion."""

    def test_ascii_domain_unchanged(self):
        """Test that ASCII domains are returned unchanged."""
        assert to_unicode_domain("example.com") == "example.com"
        assert to_unicode_domain("www.google.com") == "www.google.com"

    def test_ace_domain_decoding(self):
        """Test decoding of ACE-encoded domains."""
        # Japanese domain
        result = to_unicode_domain("xn--r8jz45g.jp")
        assert result == "例え.jp"
        # Chinese domain - use actual encoding of "测试"
        test_encoded = to_ascii("测试")
        result = to_unicode_domain(f"{test_encoded}.{to_ascii('测试')}")
        assert "测试" in result

    def test_mixed_domain(self):
        """Test decoding of domains with mixed ASCII and ACE labels."""
        result = to_unicode_domain("www.xn--r8jz45g.jp")
        assert result == "www.例え.jp"

    def test_trailing_dot(self):
        """Test that trailing dots are handled correctly."""
        result = to_unicode_domain("example.com.")
        assert result == "example.com."

    def test_empty_domain(self):
        """Test that empty domains raise an error."""
        with pytest.raises(InvalidLabel):
            to_unicode_domain("")


class TestRoundTrip:
    """Test round-trip encoding and decoding."""

    def test_label_round_trip(self):
        """Test that labels round-trip correctly."""
        test_labels = ["www", "例え", "测试", "例え.jp", "abc123"]
        for label in test_labels:
            encoded = to_ascii(label)
            decoded = to_unicode(encoded)
            assert decoded == label, f"Round-trip failed for: {label}"

    def test_domain_round_trip(self):
        """Test that domains round-trip correctly."""
        test_domains = [
            "example.com",
            "例え.jp",
            "www.例え.jp",
            "例子.测试",
        ]
        for domain in test_domains:
            encoded = to_ascii_domain(domain)
            decoded = to_unicode_domain(encoded)
            assert decoded == domain, f"Round-trip failed for: {domain}"