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
    Decode a Punycode-encoded string to Unicode (RFC 3492).

    Args:
        input_str: Punycode-encoded ASCII string

    Returns:
        Decoded Unicode string

    Raises:
        InvalidInput: If input contains invalid characters
        Overflow: If integer overflow would occur
    """
    if not input_str:
        return ""

    # Keep the original case for literal portion, but use uppercase for digit lookup
    # Find the last delimiter
    last_delimiter_pos = input_str.rfind(Bootstring.DELIMITER)

    # Initialize output with basic code points (everything before last delimiter)
    # Preserve original case in the literal portion
    output = []
    if last_delimiter_pos != -1:
        for i in range(last_delimiter_pos):
            c = input_str[i]
            cp = ord(c)
            # Validate that all characters before delimiter are basic code points
            if not Bootstring.is_basic(cp):
                raise InvalidInput("Non-basic code point before delimiter")
            output.append(cp)

    # Initialize decoding state
    n = Bootstring.INITIAL_N
    i = 0
    bias = Bootstring.INITIAL_BIAS

    # Process the remainder of the input (after the last delimiter, or all if no delimiter)
    input_pos = last_delimiter_pos + 1
    while input_pos < len(input_str):
        # Decode one delta
        old_i = i
        w = 1
        for k in range(Bootstring.BASE, Bootstring.BASE + 1000, Bootstring.BASE):
            # Consume a code point
            if input_pos >= len(input_str):
                raise InvalidInput("Unexpected end of input")

            c = input_str[input_pos]
            input_pos += 1

            # Get digit value (case-insensitive - use uppercase)
            cp = ord(c.upper())
            digit = Bootstring.digit_value(cp)
            if digit is None:
                raise InvalidInput(f"Invalid character in encoded data: {c}")

            # Accumulate into i, checking for overflow
            if i > (0x7FFFFFFF - digit * w) // 1:
                raise Overflow("Integer overflow")
            i += digit * w

            # Calculate threshold
            if k <= bias:
                t = Bootstring.TMIN
            elif k >= bias + Bootstring.TMAX:
                t = Bootstring.TMAX
            else:
                t = k - bias

            if digit < t:
                break

            # Update weight, checking for overflow
            if w > 0x7FFFFFFF // (Bootstring.BASE - t):
                raise Overflow("Integer overflow")
            w *= (Bootstring.BASE - t)

        # Adapt bias
        bias = Bootstring.adapt(i - old_i, len(output) + 1, old_i == 0)

        # Calculate the new code point
        if n > 0x7FFFFFFF - i // (len(output) + 1):
            raise Overflow("Integer overflow")
        n = n + i // (len(output) + 1)

        i = i % (len(output) + 1)

        # Insert the new code point
        output.insert(i, n)
        i += 1

    # Convert code points to string
    return "".join(chr(cp) for cp in output)


# CHAOS AGENT SUGGESTION: Performance
# Consider enhancing with: Optimize main encoding loop using list comprehensions and precomputed bias values
# Rationale: Could improve encoding performance for large strings by reducing loop overhead