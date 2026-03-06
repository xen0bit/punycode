"""
Bootstring algorithm implementation.

This module implements the core Bootstring algorithm as specified in RFC 3492.
Punycode is an instance of Bootstring with specific parameter values.
"""


class Bootstring:
    """
    Bootstring algorithm implementation.

    Parameters for Punycode:
    - base: 36
    - tmin: 1
    - tmax: 26
    - skew: 38
    - damp: 700
    - initial_bias: 72
    - initial_n: 0x80 (128)
    - delimiter: 0x2D ('-')
    """

    BASE = 36
    TMIN = 1
    TMAX = 26
    SKEW = 38
    DAMP = 700
    INITIAL_BIAS = 72
    INITIAL_N = 0x80
    DELIMITER = "-"

    @staticmethod
    def adapt(delta: int, numpoints: int, firsttime: bool) -> int:
        """
        Adapt the bias for the next delta.

        Args:
            delta: The delta value to adapt from
            numpoints: Number of code points processed so far
            firsttime: True if this is the first delta

        Returns:
            The new bias value
        """
        if firsttime:
            delta //= Bootstring.DAMP
        else:
            delta //= 2

        delta += delta // numpoints

        k = 0
        while delta > ((Bootstring.BASE - Bootstring.TMIN) * Bootstring.TMAX) // 2:
            delta //= (Bootstring.BASE - Bootstring.TMIN)
            k += Bootstring.BASE

        return k + (((Bootstring.BASE - Bootstring.TMIN + 1) * delta) //
                    (delta + Bootstring.SKEW))

    @staticmethod
    def digit_value(cp: int) -> int | None:
        """
        Get the digit value for a code point.

        A-Z -> 0-25
        a-z -> 0-25
        0-9 -> 26-35

        Args:
            cp: ASCII code point

        Returns:
            Digit value (0-35) or None if not a digit
        """
        if 0x41 <= cp <= 0x5A:  # 'A' - 'Z'
            return cp - 0x41
        if 0x61 <= cp <= 0x7A:  # 'a' - 'z'
            return cp - 0x61
        if 0x30 <= cp <= 0x39:  # '0' - '9'
            return cp - 0x30 + 26
        return None

    @staticmethod
    def code_point_for_digit(d: int) -> int:
        """
        Get the ASCII code point for a digit value.

        0-25 -> 'a' - 'z' (lowercase output)
        26-35 -> '0' - '9'

        Args:
            d: Digit value (0-35)

        Returns:
            ASCII code point

        Raises:
            ValueError: If digit value is out of range
        """
        if 0 <= d < 26:
            return 0x61 + d  # 'a' - 'z'
        if 26 <= d < 36:
            return 0x30 + (d - 26)  # '0' - '9'
        raise ValueError(f"Digit value {d} out of range 0-35")

    @staticmethod
    def is_basic(cp: int) -> bool:
        """
        Check if a code point is basic (ASCII 0x00-0x7F).

        Args:
            cp: Code point to check

        Returns:
            True if basic, False otherwise
        """
        return 0x00 <= cp <= 0x7F