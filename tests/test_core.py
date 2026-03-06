"""
Test suite for punycode encode/decode functions (RFC 3492 examples).
"""

import pytest
from punycode import encode, decode
from punycode.core import PunycodeError, InvalidInput, Overflow


class TestEncodeDecode:
    """Test encoding and decoding with RFC 3492 examples."""

    # Example A: Arabic (Egyptian)
    # u+0644 u+064A u+0647 u+0645 u+0627 u+0628 u+062A u+0643 u+0644
    # u+0645 u+0648 u+0634 u+0639 u+0631 u+0628 u+064A u+061F
    def test_encode_arabic(self):
        """Test encoding Arabic example."""
        # "لماذا لا يتكلمون بالعربية؟" (without punctuation)
        input_str = "لماذا لا يتكلمون بالعربية؟"
        output = encode(input_str)
        # Just verify it produces valid ASCII output
        assert output.isascii()
        assert len(output) > 0

    # Example B: Chinese (simplified)
    # u+4ED6 u+4EEC u+4E3A u+4EC0 u+4E48 u+4E0D u+8BF4 u+4E2D u+6587
    def test_encode_chinese_simplified(self):
        """Test encoding Chinese simplified example."""
        input_str = "他们为什么不说中文"
        expected = "ihqwcrb4cv8a8dqg056pqjye"
        result = encode(input_str)
        assert result == expected

    def test_decode_chinese_simplified(self):
        """Test decoding Chinese simplified example."""
        input_str = "ihqwcrb4cv8a8dqg056pqjye"
        expected = "他们为什么不说中文"
        result = decode(input_str)
        assert result == expected

    # Example C: Chinese (traditional)
    # u+4ED6 u+5011 u+7232 u+4EC0 u+9EBD u+4E0D u+8AAA u+4E2D u+6587
    def test_encode_chinese_traditional(self):
        """Test encoding Chinese traditional example."""
        # Use exact code points from RFC 3492
        input_str = "".join([chr(0x4ED6), chr(0x5011), chr(0x7232), chr(0x4EC0),
                            chr(0x9EBD), chr(0x4E0D), chr(0x8AAA), chr(0x4E2D),
                            chr(0x6587)])
        expected = "ihqwctvzc91f659drss3x8bo0yb"
        result = encode(input_str)
        assert result == expected

    def test_decode_chinese_traditional(self):
        """Test decoding Chinese traditional example."""
        input_str = "ihqwctvzc91f659drss3x8bo0yb"
        expected = "".join([chr(0x4ED6), chr(0x5011), chr(0x7232), chr(0x4EC0),
                           chr(0x9EBD), chr(0x4E0D), chr(0x8AAA), chr(0x4E2D),
                           chr(0x6587)])
        result = decode(input_str)
        assert result == expected

    # Example D: Czech
    # Pro<ccaron>prost<ecaron>nemluv<iacute><ccaron>esky
    def test_encode_czech(self):
        """Test encoding Czech example."""
        input_str = "Pročprostěnemluvíčesky"
        expected = "Proprostnemluvesky-uyb24dma41a"
        result = encode(input_str)
        assert result == expected

    def test_decode_czech(self):
        """Test decoding Czech example."""
        input_str = "Proprostnemluvesky-uyb24dma41a"
        expected = "Pročprostěnemluvíčesky"
        result = decode(input_str)
        assert result == expected

    # Example E: Hebrew
    def test_encode_hebrew(self):
        """Test encoding Hebrew example."""
        input_str = "למה הםלא מדברים עברית?"
        output = encode(input_str)
        assert output.isascii()

    # Example I: Russian (Cyrillic)
    # U+043F u+043E u+0447 u+0435 u+043C u+0443 u+0436 u+0435 u+043E
    # u+043D u+0438 u+043D u+0435 u+0433 u+043E u+0432 u+043E u+0440
    # u+044F u+0442 u+043F u+043E u+0440 u+0443 u+0441 u+0441 u+043A
    # u+0438
    def test_encode_russian(self):
        """Test encoding Russian example."""
        # Use exact code points from RFC 3492
        input_str = "".join([chr(0x043F), chr(0x043E), chr(0x0447), chr(0x0435),
                            chr(0x043C), chr(0x0443), chr(0x0436), chr(0x0435),
                            chr(0x043E), chr(0x043D), chr(0x0438), chr(0x043D),
                            chr(0x0435), chr(0x0433), chr(0x043E), chr(0x0432),
                            chr(0x043E), chr(0x0440), chr(0x044F), chr(0x0442),
                            chr(0x043F), chr(0x043E), chr(0x0440), chr(0x0443),
                            chr(0x0441), chr(0x0441), chr(0x043A), chr(0x0438)])
        expected = "b1abfaaepdrnnbgefbadotcwatmq2g4l"  # encoder uses lowercase
        result = encode(input_str)
        assert result == expected

    def test_decode_russian(self):
        """Test decoding Russian example."""
        # Test case-insensitive decoding with RFC example (mixed case in RFC)
        input_str = "b1abfaaepdrnnbgefbaDotcwatmq2g4l"
        expected = "".join([chr(0x043F), chr(0x043E), chr(0x0447), chr(0x0435),
                           chr(0x043C), chr(0x0443), chr(0x0436), chr(0x0435),
                           chr(0x043E), chr(0x043D), chr(0x0438), chr(0x043D),
                           chr(0x0435), chr(0x0433), chr(0x043E), chr(0x0432),
                           chr(0x043E), chr(0x0440), chr(0x044F), chr(0x0442),
                           chr(0x043F), chr(0x043E), chr(0x0440), chr(0x0443),
                           chr(0x0441), chr(0x0441), chr(0x043A), chr(0x0438)])
        result = decode(input_str)
        assert result == expected

    # Example J: Spanish: Porqu<eacute>nopuedensimplementehablarenEspa<ntilde>ol
    # U+0050 u+006F u+0072 u+0071 u+0075 u+00E9 u+006E u+006F u+0070
    # u+0075 u+0065 u+0064 u+0065 u+006E u+0073 u+0069 u+006D u+0070
    # u+006C u+0065 u+006D u+0065 u+006E u+0074 u+0065 u+0068 u+0061
    # u+0062 u+006C u+0061 u+0072 u+0065 u+006E U+0045 u+0073 u+0070
    # u+0061 u+00F1 u+006F u+006C
    def test_encode_spanish(self):
        """Test encoding Spanish example."""
        # Use exact code points from RFC 3492
        input_str = "".join([chr(0x0050), chr(0x006F), chr(0x0072), chr(0x0071),
                            chr(0x0075), chr(0x00E9), chr(0x006E), chr(0x006F),
                            chr(0x0070), chr(0x0075), chr(0x0065), chr(0x0064),
                            chr(0x0065), chr(0x006E), chr(0x0073), chr(0x0069),
                            chr(0x006D), chr(0x0070), chr(0x006C), chr(0x0065),
                            chr(0x006D), chr(0x0065), chr(0x006E), chr(0x0074),
                            chr(0x0065), chr(0x0068), chr(0x0061), chr(0x0062),
                            chr(0x006C), chr(0x0061), chr(0x0072), chr(0x0065),
                            chr(0x006E), chr(0x0045), chr(0x0073), chr(0x0070),
                            chr(0x0061), chr(0x00F1), chr(0x006F), chr(0x006C)])
        expected = "PorqunopuedensimplementehablarenEspaol-fmd56a"
        result = encode(input_str)
        assert result == expected

    def test_decode_spanish(self):
        """Test decoding Spanish example."""
        input_str = "PorqunopuedensimplementehablarenEspaol-fmd56a"
        expected = "".join([chr(0x0050), chr(0x006F), chr(0x0072), chr(0x0071),
                           chr(0x0075), chr(0x00E9), chr(0x006E), chr(0x006F),
                           chr(0x0070), chr(0x0075), chr(0x0065), chr(0x0064),
                           chr(0x0065), chr(0x006E), chr(0x0073), chr(0x0069),
                           chr(0x006D), chr(0x0070), chr(0x006C), chr(0x0065),
                           chr(0x006D), chr(0x0065), chr(0x006E), chr(0x0074),
                           chr(0x0065), chr(0x0068), chr(0x0061), chr(0x0062),
                           chr(0x006C), chr(0x0061), chr(0x0072), chr(0x0065),
                           chr(0x006E), chr(0x0045), chr(0x0073), chr(0x0070),
                           chr(0x0061), chr(0x00F1), chr(0x006F), chr(0x006C)])
        result = decode(input_str)
        assert result == expected

    # Example L: Japanese
    # 3<nen>B<gumi><kinpachi><sensei>
    # u+0033 u+5E74 U+0042 u+7D44 u+91D1 u+516B u+5148 u+751F
    def test_encode_japanese(self):
        """Test encoding Japanese example."""
        input_str = "3年B組金八先生"
        expected = "3B-ww4c5e180e575a65lsy2b"
        result = encode(input_str)
        assert result == expected

    def test_decode_japanese(self):
        """Test decoding Japanese example."""
        input_str = "3B-ww4c5e180e575a65lsy2b"
        expected = "3年B組金八先生"
        result = decode(input_str)
        assert result == expected

    # Example N: Japanese
    def test_encode_japanese_mixed(self):
        """Test encoding Japanese mixed example."""
        input_str = "Hello-Another-Way-それぞれの場所"
        expected = "Hello-Another-Way--fc4qua05auwb3674vfr0b"
        result = encode(input_str)
        assert result == expected

    def test_decode_japanese_mixed(self):
        """Test decoding Japanese mixed example."""
        input_str = "Hello-Another-Way--fc4qua05auwb3674vfr0b"
        expected = "Hello-Another-Way-それぞれの場所"
        result = decode(input_str)
        assert result == expected


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_string(self):
        """Test encoding and decoding empty strings."""
        assert encode("") == ""
        assert decode("") == ""

    def test_ascii_only(self):
        """Test encoding and decoding ASCII-only strings."""
        input_str = "Hello-World"
        # ASCII strings are mostly unchanged, delimiter may be added
        result = encode(input_str)
        assert result.isascii()
        # Round-trip
        assert decode(result) == input_str

    def test_single_non_basic(self):
        """Test encoding single non-basic code point."""
        input_str = "é"  # U+00E9
        result = encode(input_str)
        assert result.isascii()
        decoded = decode(result)
        assert decoded == input_str

    def test_round_trip(self):
        """Test round-trip encoding and decoding."""
        test_strings = [
            "他们为什么不说中文",
            "日本語",
            "한국어",
            "Привет",
            "مرحبا",
            "Γεια σας"
        ]
        for s in test_strings:
            encoded = encode(s)
            decoded = decode(encoded)
            assert decoded == s, f"Round-trip failed for: {s}"

    def test_invalid_input_decode(self):
        """Test decoding invalid input."""
        with pytest.raises(InvalidInput):
            decode("ihqwcrb4cv8a8dqg056@qjye")  # @ is not a valid digit

    def test_case_insensitive(self):
        """Test that decoding is case-insensitive."""
        encoded_lower = "ihqwcrb4cv8a8dqg056pqjye"
        encoded_upper = "IHQWCRB4CV8A8DQG056PQJYE"
        encoded_mixed = "IhQwCrB4cV8A8dQg056pQjYe"
        assert decode(encoded_lower) == "他们为什么不说中文"
        assert decode(encoded_upper) == "他们为什么不说中文"
        assert decode(encoded_mixed) == "他们为什么不说中文"