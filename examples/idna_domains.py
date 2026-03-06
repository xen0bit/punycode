#!/usr/bin/env python3
"""
IDNA domain name conversion examples.

This script demonstrates the IDNA functions for converting domain names
between Unicode and ASCII (Punycode with ACE prefix).
"""

from punycode import (
    to_ascii,
    to_unicode,
    to_ascii_domain,
    to_unicode_domain,
    InvalidLabel,
    LabelTooLong,
    DomainTooLong,
)


def main():
    print("=" * 60)
    print("IDNA Domain Name Conversion Examples")
    print("=" * 60)

    # Example 1: Label encoding/decoding
    print("\n1. Label encoding and decoding:")
    label = "例え"
    ascii_label = to_ascii(label)
    back_to_unicode = to_unicode(ascii_label)
    print(f"   Original label: {label}")
    print(f"   ASCII (ACE):     {ascii_label}")
    print(f"   Decoded back:    {back_to_unicode}")
    print(f"   Match:           {label == back_to_unicode}")

    # Example 2: Full domain encoding
    print("\n2. Full domain encoding:")
    domain = "例え.jp"
    ascii_domain = to_ascii_domain(domain)
    back_to_unicode_domain = to_unicode_domain(ascii_domain)
    print(f"   Original domain: {domain}")
    print(f"   ASCII domain:    {ascii_domain}")
    print(f"   Decoded domain:  {back_to_unicode_domain}")

    # Example 3: International TLD
    print("\n3. International Top-Level Domain:")
    domain = "例子.测试"
    ascii_domain = to_ascii_domain(domain)
    back_to_unicode_domain = to_unicode_domain(ascii_domain)
    print(f"   Original domain: {domain}")
    print(f"   ASCII domain:    {ascii_domain}")
    print(f"   Decoded domain:  {back_to_unicode_domain}")

    # Example 4: Mixed ASCII and Unicode labels
    print("\n4. Mixed ASCII and Unicode labels:")
    domain = "www.测试.com"
    ascii_domain = to_ascii_domain(domain)
    back_to_unicode_domain = to_unicode_domain(ascii_domain)
    print(f"   Original domain: {domain}")
    print(f"   ASCII domain:    {ascii_domain}")
    print(f"   Decoded domain:  {back_to_unicode_domain}")

    # Example 5: ASCII-only domain (no change)
    print("\n5. ASCII-only domain (no encoding needed):")
    domain = "example.com"
    ascii_domain = to_ascii_domain(domain)
    back_to_unicode_domain = to_unicode_domain(ascii_domain)
    print(f"   Original domain: {domain}")
    print(f"   ASCII domain:    {ascii_domain}")
    print(f"   Decoded domain:  {back_to_unicode_domain}")
    print(f"   No change: {domain == ascii_domain}")

    # Example 6: Case insensitivity in ACE prefix
    print("\n6. Case insensitivity in ACE prefix:")
    ascii_label = "XN--R8JZ45G"
    decoded1 = to_unicode(ascii_label)
    decoded2 = to_unicode(ascii_label.lower())
    print(f"   Uppercase input: {ascii_label} -> {decoded1}")
    print(f"   Lowercase input: {ascii_label.lower()} -> {decoded2}")
    print(f"   Match: {decoded1 == decoded2}")

    # Example 7: Trailing dot handling
    print("\n7. Domain with trailing dot:")
    domain = "例え.jp."
    ascii_domain = to_ascii_domain(domain)
    back_to_unicode_domain = to_unicode_domain(ascii_domain)
    print(f"   Original domain: {domain}")
    print(f"   ASCII domain:    {ascii_domain}")
    print(f"   Decoded domain:  {back_to_unicode_domain}")

    # Example 8: Error handling - empty label
    print("\n8. Error handling - empty label:")
    try:
        label = ""
        ascii_label = to_ascii(label)
        print(f"   Error: Should have raised InvalidLabel")
    except InvalidLabel as e:
        print(f"   ✓ Caught InvalidLabel: {e}")

    # Example 9: Error handling - label too long
    print("\n9. Error handling - label too long:")
    try:
        # Create a label that will exceed 63 characters after encoding
        label = "测试" * 20  # This will be > 63 chars when encoded
        ascii_label = to_ascii(label)
        print(f"   Encoded: {len(ascii_label)} chars (should fail)")
    except LabelTooLong as e:
        print(f"   ✓ Caught LabelTooLong: {e}")

    # Example 10: Error handling - domain too long
    print("\n10. Error handling - domain too long:")
    try:
        # Create a domain that will exceed 253 characters
        long_domain = ".".join(["label" * 10] * 10)
        ascii_domain = to_ascii_domain(long_domain)
        print(f"   Encoded: {len(ascii_domain)} chars (should fail)")
    except DomainTooLong as e:
        print(f"   ✓ Caught DomainTooLong: {e}")

    # Example 11: Round-trip for multiple domains
    print("\n11. Round-trip test for multiple domains:")
    test_domains = [
        "例え.jp",
        "例子.测试",
        "www.测试.com",
        "münchen.de",
        "naïve.example.org",
    ]
    for domain in test_domains:
        ascii_domain = to_ascii_domain(domain)
        decoded_domain = to_unicode_domain(ascii_domain)
        match = "✓" if domain == decoded_domain else "✗"
        print(f"   {match} {domain} -> {ascii_domain} -> {decoded_domain}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()