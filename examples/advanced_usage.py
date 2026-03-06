#!/usr/bin/env python3
"""
Advanced usage examples.

This script demonstrates advanced use cases such as batch processing,
Unicode normalization, and integration scenarios.
"""

import unicodedata
from punycode import (
    encode, decode,
    to_ascii, to_unicode,
    to_ascii_domain, to_unicode_domain,
)


def main():
    print("=" * 60)
    print("Advanced Usage Examples")
    print("=" * 60)

    # Example 1: Batch processing multiple domains
    print("\n1. Batch processing multiple domains:")
    domains = [
        "example.com",
        "例え.jp",
        "例子.测试",
        "www.测试.com",
        "münchen.de",
        "bücher.de",
        "naïve.example.org",
    ]

    print("   Encoded:")
    for domain in domains:
        ascii_domain = to_ascii_domain(domain)
        decoded_back = to_unicode_domain(ascii_domain)
        match = "✓" if domain == decoded_back else "✗"
        print(f"      {match} {domain:25s} -> {ascii_domain}")

    # Example 2: Unicode normalization
    print("\n2. Unicode normalization (IDNA uses NFC automatically):")
    text = "例え"

    # Different normalization forms
    nfc = unicodedata.normalize('NFC', text)
    nfd = unicodedata.normalize('NFD', text)
    nfd_with_diacritic = unicodedata.normalize('NFD', 'é')

    print(f"   Original:      {text} (U+{ord('例'):04X} U+{ord('え'):04X})")
    print(f"   NFC form:      {nfc}")
    print(f"   NFD form:      {nfd}")
    print(f"   NFD 'é':       {nfd_with_diacritic}")
    print()

    # Encode both forms - IDNA normalizes to NFC automatically
    ascii_nfc = to_ascii(nfc)
    ascii_nfd = to_ascii(nfd)

    print(f"   Encoded NFC:   {ascii_nfc}")
    print(f"   Encoded NFD:   {ascii_nfd}")
    print(f"   Match:         {ascii_nfc == ascii_nfd} (should be True)")

    # Example 3: Case handling in IDNA
    print("\n3. Case handling in IDNA:")
    test_cases = [
        ("Example.COM", "example.com"),
        ("EXAMPLE.com", "example.com"),
        ("例え.JP", "例え.jp"),
        ("mÜNCHEN.de", "münchen.de"),
    ]

    print("   Encoding (lowercased automatically):")
    for input_domain, expected in test_cases:
        encoded = to_ascii_domain(input_domain)
        decoded = to_unicode_domain(encoded)
        normalized = expected.lower()
        print(f"      '{input_domain}' -> {encoded} -> {decoded}")
        print(f"         Normalized: {normalized} (Expected: {expected.lower()})")
        print(f"         Match: {decoded == normalized}")

    # Example 4: Subdomain handling
    print("\n4. Subdomain handling:")
    test_domains = [
        "a.b.c.d.example.com",
        "www.例え.jp",
        "mail.例子.测试",
        "ftp.测试.co.jp",
    ]

    for domain in test_domains:
        encoded = to_ascii_domain(domain)
        decoded = to_unicode_domain(encoded)
        labels = domain.split('.')
        encoded_labels = encoded.split('.')
        print(f"      Original: {domain}")
        print(f"         # labels: {len(labels)}")
        print(f"      Encoded: {encoded}")
        print(f"      Decoded: {decoded}")
        print(f"         Match: {domain == decoded}")
        print()

    # Example 5: Punycode without ACE prefix
    print("\n5. Pure Punycode (without xn-- prefix):")
    texts = [
        "例え",
        "テスト",
        "测试",
        "例之",
    ]

    for text in texts:
        punycode = encode(text)
        decoded = decode(punycode)
        encoded_with_prefix = to_ascii(text)

        print(f"      Text:     {text}")
        print(f"      Punycode: {punycode}")
        print(f"      IDNA:     {encoded_with_prefix}")
        print(f"      Decoded:  {decoded}")
        print(f"      Match:    {text == decoded}")
        print()

    # Example 6: Comparing different scripts
    print("\n6. Encoding efficiency across different scripts:")
    scripts = [
        ("Arabic", "لماذا لا يتكلمون بالعربية؟"),
        ("Chinese (Simplified)", "他们为什么不说中文"),
        ("Chinese (Traditional)", "他們為什麼不說中文"),
        ("Czech", "Pročprostěnemluvíčesky"),
        ("Russian", "почемуони говорятпорусски"),
        ("Spanish", "PorquénopuedensimplementehablarenEspañol"),
        ("Japanese", "3年B組金八先生"),
        ("Hebrew", "למההםלאמדבריםעברית"),
    ]

    print("   Length comparison:")
    print(f"   {'Script':20s} {'Orig Chars':<10} {'Encoded Chars':<10} {'Ratio':<10}")
    print("      " + "-" * 50)

    for script_name, text in scripts:
        encoded = encode(text)
        orig_len = len(text.encode('utf-8'))  # UTF-8 bytes
        puny_len = len(encoded)
        ratio = puny_len / orig_len if orig_len > 0 else 0

        print(f"      {script_name:18s} {orig_len:5d}        {puny_len:5d}        {ratio:.2f}")

    # Example 7: Internationalized Email Addresses (fictional)
    print("\n7. Internationalized Email Addresses (local part only):")
    # Note: This demonstrates encoding the local part, not full email (which requires SMTPUTF8)
    local_parts = [
        "例え",  # Japanese
        "测试",  # Chinese
        "münchen",  # German
    ]

    for local in local_parts:
        encoded = encode(local)
        # Fictional email address - domain would need its own IDNA encoding
        ascii_email = f"{encoded}@example.com"
        print(f"      Local part:  {local}")
        print(f"      Encoded:     {encoded}")
        print(f"      ASCII email: {ascii_email}")
        print()

    # Example 8: Finding ASCII vs Unicode labels
    print("\n8. Identifying ASCII vs Unicode labels in a domain:")
    test_domain = "www.例え.jp"
    labels = test_domain.split('.')

    print(f"   Domain: {test_domain}")
    for i, label in enumerate(labels):
        is_ascii = label.isascii()
        print(f"      Label {i+1}: '{label}' -> {'ASCII' if is_ascii else 'Unicode'}")

        if not is_ascii:
            encoded = to_ascii(label)
            print(f"         Encoded: {encoded}")

    # Example 9: Round-trip fidelity test
    print("\n9. Round-trip fidelity test (stress test):")
    import random
    import string
    import sys

    # Generate random ASCII + Unicode strings
    random_strings = []

    # ASCII-only
    random_strings.append(''.join(random.choices(
        string.ascii_letters + string.digits + '-',
        k=random.randint(5, 30)
    )))

    # Mixed ASCII and various Unicode
    for _ in range(5):
        length = random.randint(5, 20)
        parts = []
        for _ in range(length):
            # Mix of ASCII and random code points
            choice = random.random()
            if choice < 0.3:
                # ASCII
                parts.append(random.choice(string.ascii_letters))
            elif choice < 0.6:
                # CJK characters
                parts.append(chr(random.randint(0x4E00, 0x9FFF)))
            elif choice < 0.8:
                # Arabic
                parts.append(chr(random.randint(0x0600, 0x06FF)))
            else:
                # Other
                parts.append(chr(random.randint(0x0080, 0xFFFF)))

        random_strings.append(''.join(parts))

    print("   Testing round-trip encoding/decoding:")
    all_passed = True
    for i, text in enumerate(random_strings):
        try:
            encoded = encode(text)
            decoded = decode(encoded)
            passed = text == decoded
            all_passed = all_passed and passed
            status = "✓" if passed else "✗"
            print(f"      Test {i+1}: {status} {text[:15]}{'...' if len(text) > 15 else ''} -> {len(encoded)} chars")
        except Exception as e:
            print(f"      Test {i+1}: ✗ Error: {e}")
            all_passed = False

    print(f"\n   Overall: {'✓ All tests passed!' if all_passed else '✗ Some tests failed'}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()