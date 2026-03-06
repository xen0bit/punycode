#!/usr/bin/env python3
"""
Error handling examples.

This script demonstrates the various error types and how to handle them
when using the Punycode library.
"""

from punycode import (
    encode,
    decode,
    PunycodeError,
    InvalidInput,
    Overflow,
)
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


def show_exception(label: str, exception_type: type[Exception], fn, *args):
    """Helper function to show exception handling."""
    print(f"   {label}")
    try:
        result = fn(*args)
        print(f"      ✗ No exception raised! Result: {result}")
    except exception_type as e:
        print(f"      ✓ Caught {exception_type.__name__}: {e}")
    except Exception as e:
        print(f"      ✗ Caught unexpected exception: {type(e).__name__}: {e}")


def main():
    print("=" * 60)
    print("Error Handling Examples")
    print("=" * 60)

    # Section 1: Punycore core exceptions
    print("\n1. Punycore core exceptions:")

    print("\n   a) InvalidInput - invalid characters in Punycode data:")
    show_exception(
        "Decode invalid Punycode (contains @)",
        InvalidInput,
        decode,
        "abc@def"
    )

    print("\n   b) InvalidInput - unexpected end of input:")
    show_exception(
        "Decode incomplete Punycode",
        InvalidInput,
        decode,
        "abc-"
    )

    print("\n   c) InvalidInput - non-basic code point before delimiter:")
    show_exception(
        "Decode with non-ASCII before delimiter",
        InvalidInput,
        decode,
        "あ-bc"
    )

    print("\n   d) Overflow - integer overflow during encoding:")
    show_exception(
        "Encode very long string (potential overflow)",
        Overflow,
        encode,
        "测试" * 1000
    )

    # Section 2: IDNA exceptions
    print("\n\n2. IDNA exceptions:")

    print("\n   a) InvalidLabel - empty label:")
    show_exception(
        "Encode empty label",
        InvalidLabel,
        to_ascii,
        ""
    )

    print("\n   b) InvalidLabel - empty domain:")
    show_exception(
        "Encode empty domain",
        InvalidLabel,
        to_ascii_domain,
        ""
    )

    print("\n   c) InvalidLabel - empty domain decode:")
    show_exception(
        "Decode empty domain",
        InvalidLabel,
        to_unicode_domain,
        ""
    )

    print("\n   d) LabelTooLong - label exceeds 63 chars:")
    # Create a Unicode string that will be > 63 chars when encoded
    # Note: LabelTooLong is a subclass of InvalidLabel
    print("      Encoding very long label (should raise LabelTooLong):")
    try:
        result = to_ascii("测试" * 20)
        print(f"         ✗ No exception raised! Result: {result}")
    except LabelTooLong as e:
        print(f"         ✓ Caught LabelTooLong: {e}")
    except Exception as e:
        print(f"         ✗ Caught unexpected exception: {type(e).__name__}: {e}")

    print("\n   e) DomainTooLong - domain exceeds 253 chars:")
    # Create a domain that will be > 253 chars when encoded
    long_label = "测试" * 10  # Each label will be ~30 chars encoded
    long_domain = ".".join([long_label] * 10)
    show_exception(
        "Encode very long domain",
        DomainTooLong,
        to_ascii_domain,
        long_domain
    )

    print("\n   f) InvalidLabel - malformed ACE label:")
    show_exception(
        "Decode malformed ACE label (empty after prefix)",
        InvalidLabel,
        to_unicode,
        "xn--"
    )

    # Section 3: Exception hierarchy
    print("\n\n3. Exception hierarchy:")

    print("\n   a) IDNAError is the base for IDNA exceptions:")
    show_exception(
        "Catch IDNAError for InvalidLabel",
        IDNAError,
        to_ascii,
        ""
    )

    print("\n   b) PunycodeError is the base for Punycore exceptions:")
    show_exception(
        "Catch PunycodeError for InvalidInput",
        PunycodeError,
        decode,
        "abc@def"
    )

    # Section 4: Practical error handling patterns
    print("\n\n4. Practical error handling patterns:")

    print("\n   a) Encoding with user-friendly error messages:")
    def label_to_ascii(label: str) -> str:
        """Convert label to ASCII with friendly error messages."""
        try:
            return to_ascii(label)
        except LabelTooLong:
            raise ValueError(f"Label exceeds 63 character limit") from None
        except InvalidLabel as e:
            if "Empty label" in str(e):
                raise ValueError("Domain label cannot be empty") from None
            else:
                raise

    for test in ["test", "例え", "", "测试" * 20]:
        print(f"      Encoding '{test[:20]}{'...' if len(test) > 20 else ''}':", end=" ")
        try:
            result = label_to_ascii(test)
            print(f"Success -> {result}")
        except ValueError as e:
            print(f"Error -> {e}")

    print("\n   b) Decoding with specific error handling:")
    def safe_decode(punycode: str) -> str:
        """Decode Punycode with comprehensive error handling."""
        try:
            return decode(punycode)
        except InvalidInput as e:
            if "invalid character" in str(e).lower():
                raise ValueError(f"Invalid Punycode format: contains invalid characters") from None
            elif "unexpected end" in str(e).lower():
                raise ValueError(f"Invalid Punycode format: incomplete or truncated") from None
            else:
                raise
        except Overflow:
            raise ValueError("Invalid Punycode format: numeric overflow") from None

    for test in ["ihqwcrb4cv8a8dqg056pqjye", "abc@def", "abc-", ""]:
        print(f"      Decoding '{test[:30]}{'...' if len(test) > 30 else ''}':", end=" ")
        try:
            result = safe_decode(test)
            print(f"Success -> {result}")
        except ValueError as e:
            print(f"Error -> {e}")

    print("\n   c) Domain conversion with validation:")
    def convert_domain(domain: str, to_ascii: bool = True) -> str:
        """Convert domain with comprehensive validation and error handling."""
        try:
            if to_ascii:
                return to_ascii_domain(domain)
            else:
                return to_unicode_domain(domain)
        except InvalidLabel as e:
            if "Empty domain" in str(e):
                raise ValueError("Domain cannot be empty") from None
            else:
                raise
        except DomainTooLong:
            raise ValueError("Domain exceeds 253 character limit") from None

    for test in ["example.com", "例え.jp", "", "label" * 100]:
        print(f"      Converting '{test[:30]}{'...' if len(test) > 30 else ''}':", end=" ")
        try:
            result = convert_domain(test, to_ascii=True)
            print(f"Success -> {result}")
        except ValueError as e:
            print(f"Error -> {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()