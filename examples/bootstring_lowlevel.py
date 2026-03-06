#!/usr/bin/env python3
"""
Low-level Bootstring API examples.

This script demonstrates the low-level Bootstring algorithm functions
that are used internally by Punycode encoding and decoding.
"""

from punycode import Bootstring


def main():
    print("=" * 60)
    print("Low-level Bootstring API Examples")
    print("=" * 60)

    # Example 1: Checking if code points are basic (ASCII)
    print("\n1. Checking basic (ASCII) code points:")
    test_chars = ['a', 'Z', '0', '9', 'あ', '中']
    for char in test_chars:
        cp = ord(char)
        is_basic = Bootstring.is_basic(cp)
        status = "BASIC" if is_basic else "NON-BASIC"
        print(f"   '{char}' (U+{cp:04X}): {status}")

    # Example 2: Digit value mapping (ASCII char -> digit value)
    print("\n2. Digit value mapping (ASCII char -> digit value):")
    test_chars = ['a', 'z', 'A', 'Z', '0', '9']
    for char in test_chars:
        cp = ord(char)
        digit = Bootstring.digit_value(cp)
        print(f"   '{char}' (U+{cp:04X}): digit value = {digit}")

    # Example 3: Code point for digit (digit value -> ASCII char)
    print("\n3. Code point for digit (digit value -> ASCII char):")
    test_digits = [0, 1, 25, 26, 35]
    for d in test_digits:
        try:
            cp = Bootstring.code_point_for_digit(d)
            char = chr(cp)
            print(f"   Digit {d:2d}: U+{cp:04X} ('{char}')")
        except ValueError as e:
            print(f"   Digit {d:2d}: Error: {e}")

    # Example 4: Adapt function - first time
    print("\n4. Adapt function (first time):")
    print("   RFC 3492 example from section 7.1:")
    delta = 19853
    numpoints = 1
    firsttime = True
    bias = Bootstring.adapt(delta, numpoints, firsttime)
    print(f"   adapt(delta={delta}, numpoints={numpoints}, firsttime={firsttime})")
    print(f"   => bias = {bias}")

    # Example 5: Adapt function - subsequent calls
    print("\n5. Adapt function (subsequent calls):")
    test_cases = [
        (100, 5, False),
        (1000, 10, False),
        (10000, 100, False),
    ]
    for delta, numpoints, firsttime in test_cases:
        bias = Bootstring.adapt(delta, numpoints, firsttime)
        print(f"   adapt(delta={delta:5d}, numpoints={numpoints:3d}, firsttime={firsttime})")
        print(f"   => bias = {bias}")

    # Example 6: Bootstring parameter values
    print("\n6. Bootstring parameter values (Punycode):")
    print(f"   BASE         = {Bootstring.BASE}")
    print(f"   TMIN         = {Bootstring.TMIN}")
    print(f"   TMAX         = {Bootstring.TMAX}")
    print(f"   SKEW         = {Bootstring.SKEW}")
    print(f"   DAMP         = {Bootstring.DAMP}")
    print(f"   INITIAL_BIAS = {Bootstring.INITIAL_BIAS}")
    print(f"   INITIAL_N    = {Bootstring.INITIAL_N} (0x{Bootstring.INITIAL_N:X})")
    print(f"   DELIMITER    = '{Bootstring.DELIMITER}' (U+{ord(Bootstring.DELIMITER):04X})")

    # Example 7: Invalid digit value
    print("\n7. Invalid digit value:")
    try:
        digit = Bootstring.digit_value(ord('@'))
        print(f"   Digit value: {digit}")
    except Exception as e:
        print(f"   ✓ Digit value for '@': None (not a valid digit)")

    # Example 8: Invalid code point for digit
    print("\n8. Invalid code point for digit:")
    try:
        cp = Bootstring.code_point_for_digit(100)
        print(f"   Code point: {cp}")
    except ValueError as e:
        print(f"   ✓ Caught ValueError: {e}")

    # Example 9: Adapt over multiple iterations
    print("\n9. Adapt progression during encoding:")
    print("   Simulating bias changes during encoding...")
    bias = Bootstring.INITIAL_BIAS
    deltas = [19853, 100, 50, 2000, 500]
    numpoints = 1
    print(f"   Initial bias: {bias}")
    for i, delta in enumerate(deltas):
        is_first = (i == 0)
        bias = Bootstring.adapt(delta, numpoints, is_first)
        numpoints += 1
        print(f"   Step {i+1}: delta={delta:5d}, numpoints={numpoints}, firsttime={is_first}")
        print(f"          new bias = {bias}")

    # Example 10: Understanding the digit range
    print("\n10. Understanding the digit range (0-35):")
    print("    Punycode uses base-36 encoding:")
    print("    Digits 0-25  -> characters 'a' through 'z'")
    print("    Digits 26-35 -> characters '0' through '9'")
    print("\n    Full mapping:")
    for d in range(36):
        cp = Bootstring.code_point_for_digit(d)
        if d == 26:
            print()
        print(f"    {d:2d} -> '{chr(cp)}'", end="    ")
        if (d + 1) % 6 == 0:
            print()

    # Example 11: Case insensitivity in digit_value
    print("\n11. Case insensitivity in digit_value:")
    for char in ['a', 'z', 'A', 'Z']:
        upper_cp = ord(char.upper())
        lower_cp = ord(char.lower())
        upper_digit = Bootstring.digit_value(upper_cp)
        lower_digit = Bootstring.digit_value(lower_cp)
        print(f"   '{char.upper()}' (U+{upper_cp:04X}): {upper_digit}")
        print(f"   '{char.lower()}' (U+{lower_cp:04X}): {lower_digit}")
        print(f"   Match: {upper_digit == lower_digit}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()