# Punycode (RFC 3492) Implementation

A Python implementation of Punycode encoding/decoding for Internationalized Domain Names (IDNA), as specified in RFC 3492.

## Features

- Full RFC 3492 compliance
- Bootstring algorithm implementation
- Encoding and decoding of Unicode domain labels
- IDNA support (RFC 3490) with Unicode NFC normalization
- Comprehensive error handling with overflow detection
- Type-safe Python 3.12+ implementation
- 54 test cases covering RFC 3492 examples and edge cases

## Installation

```bash
uv sync
```

Or with pip:

```bash
pip install -e .
```

## Usage

### Command Line

```bash
# Basic Punycode encode/decode
python main.py encode "他们为什么不说中文"
# Output: ihqwcrb4cv8a8dqg056pqjye

python main.py decode "ihqwcrb4cv8a8dqg056pqjye"
# Output: 他们为什么不说中文

# IDNA label encoding (adds xn-- prefix)
python main.py to-ascii "例え"
# Output: xn--r8jz45g

# IDNA label decoding (removes xn-- prefix)
python main.py to-unicode "xn--r8jz45g"
# Output: 例え

# IDNA domain encoding
python main.py to-ascii-domain "例え.jp"
# Output: xn--r8jz45g.jp

# IDNA domain decoding
python main.py to-unicode-domain "xn--r8jz45g.jp"
# Output: 例え.jp
```

### Python API

#### Basic Punycode Functions

```python
from punycode import encode, decode

# Encode a Unicode string to Punycode
encoded = encode("他们为什么不说中文")
print(encoded)  # ihqwcrb4cv8a8dqg056pqjye

# Decode a Punycode string to Unicode
decoded = decode("ihqwcrb4cv8a8dqg056pqjye")
print(decoded)  # 他们为什么不说中文
```

#### IDNA Functions (Domain Name Support)

```python
from punycode import to_ascii, to_unicode, to_ascii_domain, to_unicode_domain

# Convert a Unicode domain label to ASCII (with ACE prefix)
ascii_label = to_ascii("例え")
print(ascii_label)  # xn--r8jz45g

# Convert an ASCII domain label to Unicode (removes ACE prefix)
unicode_label = to_unicode("xn--r8jz45g")
print(unicode_label)  # 例え

# Convert a Unicode domain name to ASCII
ascii_domain = to_ascii_domain("例え.jp")
print(ascii_domain)  # xn--r8jz45g.jp

# Convert an ASCII domain name to Unicode
unicode_domain = to_unicode_domain("xn--r8jz45g.jp")
print(unicode_domain)  # 例え.jp
```

#### Direct Bootstring API

```python
from punycode import Bootstring

# Adapt the bias for the next delta
bias = Bootstring.adapt(delta=19853, numpoints=1, firsttime=True)
print(bias)  # 21

# Get the digit value for an ASCII character
digit = Bootstring.digit_value(ord('A'))  # Returns: 0
digit = Bootstring.digit_value(ord('z'))  # Returns: 25
digit = Bootstring.digit_value(ord('9'))  # Returns: 35

# Get the ASCII code point for a digit value
cp = Bootstring.code_point_for_digit(0)  # Returns: 97 ('a')
cp = Bootstring.code_point_for_digit(35)  # Returns: 57 ('9')

# Check if a code point is basic (ASCII)
is_basic = Bootstring.is_basic(ord('a'))  # Returns: True
is_basic = Bootstring.is_basic(0x4E00)    # Returns: False (中文字符)
```

## Error Handling

The library provides specific exceptions for different error conditions:

```python
from punycode import (
    encode, decode,
    InvalidInput,      # Invalid characters in input
    Overflow,          # Integer overflow during encoding/decoding
    IDNAError,         # Base IDNA error
    InvalidLabel,      # Invalid domain label
    LabelTooLong,      # Label exceeds 63 character limit
    DomainTooLong,     # Domain exceeds 253 character limit
)

try:
    encoded = encode("some string")
except InvalidInput as e:
    print(f"Invalid input: {e}")
except Overflow as e:
    print(f"Overflow: {e}")

try:
    ascii_label = to_ascii("a" * 100)  # Too long
except LabelTooLong as e:
    print(f"Label too long: {e}")
```

## Unicode Normalization

IDNA functions automatically normalize strings to NFC form (Normalization Form C) as recommended by IDNA2008:

```python
import unicodedata
from punycode import to_ascii

# NFD form (decomposed)
nfd_str = unicodedata.normalize('NFD', '例え')
# NFC form (composed, used automatically)
nfc_str = unicodedata.normalize('NFC', '例え')

# Both produce the same encoding
assert to_ascii(nfd_str) == to_ascii(nfc_str)
```

## Examples

Comprehensive example scripts are available in the `examples/` directory:

```bash
# Basic Punycode encoding/decoding
python examples/basic_usage.py

# IDNA domain name conversion
python examples/idna_domains.py

# Low-level Bootstring API
python examples/bootstring_lowlevel.py

# Error handling patterns
python examples/error_handling.py

# Advanced usage scenarios
python examples/advanced_usage.py
```

## Testing

Run the full test suite:

```bash
pytest
```

Run tests with verbosity:

```bash
pytest -v
```

Run specific test modules:

```bash
# Test Bootstring algorithm
pytest tests/test_bootstring.py

# Test core Punycode encode/decode
pytest tests/test_core.py

# Test IDNA support
pytest tests/test_idna.py
```

## RFC 3492 Examples

This implementation passes the official RFC 3492 test cases:

- **Arabic**: `لماذا لا يتكلمون بالعربية؟`
- **Chinese (Simplified)**: `他们为什么不说中文` → `ihqwcrb4cv8a8dqg056pqjye`
- **Chinese (Traditional)**: `他們為什麼不說中文` → `ihqwctvzc91f659drss3x8bo0yb`
- **Czech**: `Pročprostěnemluvíčesky` → `Proprostnemluvesky-uyb24dma41a`
- **Russian**: `почемуони говорятпорусски` → `b1abfaaepdrnnbgefbadotcwatmq2g4l`
- **Spanish**: `PorquénopuedensimplementehablarenEspañol` → `PorqunopuedensimplementehablarenEspaol-fmd56a`
- **Japanese**: `3年B組金八先生` → `3B-ww4c5e180e575a65lsy2b`

See RFC 3492, Section 7 for more examples.

## Specification

This implementation follows:

- [RFC 3492: Punycode: A Bootstring encoding of Unicode for Internationalized Domain Names in Applications (IDNA)](https://www.rfc-editor.org/rfc/rfc3492)
- [RFC 3490: Internationalizing Domain Names in Applications (IDNA)](https://www.rfc-editor.org/rfc/rfc3490)

## License

See LICENSE file for details.