#!/usr/bin/env python3
"""
Basic Punycode usage examples.

This script demonstrates the basic Punycode encoding and decoding functions.
"""

from punycode import encode, decode


def main():
    print("=" * 60)
    print("Basic Punycode Usage Examples")
    print("=" * 60)

    # Example 1: Round-trip encoding/decoding
    print("\n1. Round-trip encoding:")
    original = "Hello World"
    encoded = encode(original)
    decoded = decode(encoded)
    print(f"   Original: {original}")
    print(f"   Encoded:  {encoded}")
    print(f"   Decoded:  {decoded}")
    print(f"   Match: {original == decoded}")

    # Example 2: Chinese (Simplified)
    print("\n2. Chinese (Simplified) - RFC 3492 Example:")
    chinese = "他们为什么不说中文"
    encoded = encode(chinese)
    decoded = decode(encoded)
    print(f"   Original: {chinese}")
    print(f"   Encoded:  {encoded}")
    print(f"   Decoded:  {decoded}")

    # Example 3: Japanese
    print("\n3. Japanese - RFC 3492 Example:")
    japanese = "3年B組金八先生"
    encoded = encode(japanese)
    decoded = decode(encoded)
    print(f"   Original: {japanese}")
    print(f"   Encoded:  {encoded}")
    print(f"   Decoded:  {decoded}")

    # Example 4: Arabic
    print("\n4. Arabic - RFC 3492 Example:")
    arabic = "لماذا لا يتكلمون بالعربية؟"
    encoded = encode(arabic)
    decoded = decode(encoded)
    print(f"   Original: {arabic}")
    print(f"   Encoded:  {encoded}")
    print(f"   Decoded:  {decoded}")

    # Example 5: ASCII-only string (no encoding needed)
    print("\n5. ASCII-only string:")
    ascii_str = "example"
    encoded = encode(ascii_str)
    decoded = decode(encoded)
    print(f"   Original: {ascii_str}")
    print(f"   Encoded:  {encoded}")
    print(f"   Decoded:  {decoded}")

    # Example 6: Mixed ASCII and Unicode
    print("\n6. Mixed ASCII and Unicode:")
    mixed = "こんにちはWorld"
    encoded = encode(mixed)
    decoded = decode(encoded)
    print(f"   Original: {mixed}")
    print(f"   Encoded:  {encoded}")
    print(f"   Decoded:  {decoded}")

    # Example 7: Empty string
    print("\n7. Empty string:")
    empty = ""
    encoded = encode(empty)
    decoded = decode(encoded)
    print(f"   Original: '{empty}'")
    print(f"   Encoded:  '{encoded}'")
    print(f"   Decoded:  '{decoded}'")

    # Example 8: Case preservation in decoded output
    print("\n8. Case preservation (ASCII portion):")
    mixed_case = "AbC-xyz123"
    encoded = encode(mixed_case)
    decoded = decode(encoded)
    print(f"   Original: {mixed_case}")
    print(f"   Encoded:  {encoded}")
    print(f"   Decoded:  {decoded}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()