"""
Core Punycode encoding and decoding functions.
"""

from .bootstring import Bootstring


class PunycodeError(Exception):
    """Base exception for Punycode errors."""
    pass


class InvalidInput(PunycodeError):
    """Raised when input contains invalid characters."""
    pass


class Overflow(PunycodeError):
    """Raised when integer overflow would occur."""
    pass


# CHAOS AGENT SUGGESTION: Performance
# Consider enhancing with: Optimize main encoding loop using list comprehensions and precomputed bias values
# Rationale: Could improve encoding performance for large strings by reducing loop overhead

def encode(input_str: str) -> str:
    """
    Encode a Unicode string to Punycode (RFC 3492).

    Args:
        input_str: Unicode string to encode

    Returns:
        Punycode-encoded ASCII string (lowercase)

    Raises:
        Overflow: If encoding would cause integer overflow
    """
    if not input_str:
        return ""

    # Convert input to code points
    input_cp = [ord(c) for c in input_str]

    # Separate basic and non-basic code points
    output = []
    non_basic = []
    for cp in input_cp:
        if Bootstring.is_basic(cp):
            output.append(cp)
        else:
            non_basic.append(cp)

    # Initialize encoding state
    n = Bootstring.INITIAL_N
    delta = 0
    bias = Bootstring.INITIAL_BIAS
    h = len(output)
    b = h

    # Copy basic code points to output (already done)
    # Add delimiter if there were any basic code points
    if b > 0:
        output.append(ord(Bootstring.DELIMITER))

    # Main encoding loop - encode non-basic code points
    while h < len(input_cp):
        # Find minimum non-basic code point >= n
        m = min(cp for cp in non_basic if cp >= n)

        # Increase delta
        delta += (m - n) * (h + 1)
        if delta > 0x7FFFFFFF:
            raise Overflow("Integer overflow")

        n = m

        # Encode all occurrences of code point n
        for c in input_cp:
            if c < n:
                delta += 1
                if delta > 0x7FFFFFFF:
                    raise Overflow("Integer overflow")

            if c == n:
                # Encode delta as generalized variable-length integer
                q = delta
                k = Bootstring.BASE
                while True:
                    if k <= bias:
                        t = Bootstring.TMIN
                    elif k >= bias + Bootstring.TMAX:
                        t = Bootstring.TMAX
                    else:
                        t = k - bias

                    if q < t:
                        break

                    digit = t + ((q - t) % (Bootstring.BASE - t))
                    output.append(Bootstring.code_point_for_digit(digit))
                    q = (q - t) // (Bootstring.BASE - t)
                    k += Bootstring.BASE

                output.append(Bootstring.code_point_for_digit(q))

                # Adapt bias
                bias = Bootstring.adapt(delta, h + 1, h == b)

                # Reset delta and increment h
                delta = 0
                h += 1

        # Increment delta and n
        delta += 1
        if delta > 0x7FFFFFFF:
            raise Overflow("Integer overflow")
        n += 1

    # Convert code points to string (output is already lowercase per RFC 3492)
    return "".join(chr(cp) for cp in output)


# CHAOS AGENT SUGGESTION: Performance
# Consider enhancing with: Optimize main encoding loop using list comprehensions and precomputed bias values
# Rationale: Could improve encoding performance for large strings by reducing loop overhead

def decode(input_str: str) -> str:
    """
    Decode a Punycode string to Unicode (RFC 3492).

    Args:
        input_str: Punycode-encoded ASCII string

    Returns:
        Decoded Unicode string

    Raises:
        InvalidInput: If input contains invalid characters
        Overflow: If decoding would cause integer overflow
    """
    if not input_str:
        return ""

    # Convert input to code points
    input_cp = [ord(c) for c in input_str]

    # Initialize decoding state
    n = Bootstring.INITIAL_N
    i = 0
    bias = Bootstring.INITIAL_BIAS
    output = []

    # Find the last delimiter
    delimiter_index = len(input_cp) - 1
    while delimiter_index >= 0 and input_cp[delimiter_index] != ord(Bootstring.DELIMITER):
        delimiter_index -= 1

    # Process literal portion (all code points before the last delimiter)
    if delimiter_index >= 0:
        # Copy all basic code points before the last delimiter
        for cp in input_cp[:delimiter_index]:
            if not Bootstring.is_basic(cp):
                raise InvalidInput(f"Non-basic code point in literal portion: U+{cp:04X}")
            output.append(cp)
        # The encoded portion starts after the last delimiter
        input_cp = input_cp[delimiter_index + 1:]
    else:
        # No delimiter, so no literal portion
        input_cp = input_cp[:]  # All characters are encoded

    # Decode deltas
    while input_cp:
        oldi = i
        w = 1
        k = Bootstring.BASE

        while True:
            if not input_cp:
                raise InvalidInput("Unexpected end of input")

            cp = input_cp.pop(0)
            digit = Bootstring.digit_value(cp)
            if digit is None:
                raise InvalidInput(f"Invalid digit: {chr(cp)} (U+{cp:04X})")

            i += digit * w
            if i > 0x7FFFFFFF:
                raise Overflow("Integer overflow")

            if k <= bias:
                t = Bootstring.TMIN
            elif k >= bias + Bootstring.TMAX:
                t = Bootstring.TMAX
            else:
                t = k - bias

            if digit < t:
                break

            w *= (Bootstring.BASE - t)
            if w > 0x7FFFFFFF:
                raise Overflow("Integer overflow")

            k += Bootstring.BASE

        bias = Bootstring.adapt(i - oldi, len(output) + 1, oldi == 0)
        n += i // (len(output) + 1)
        if n > 0x10FFFF:
            raise Overflow("Code point exceeds maximum Unicode value")
        i = i % (len(output) + 1)

        output.insert(i, n)
        i += 1

    # Convert code points to string
    return "".join(chr(cp) for cp in output)