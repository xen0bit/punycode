"""
Punycode (RFC 3492) implementation for Internationalized Domain Names.

This module provides encoding and decoding of Unicode domain name labels
to ASCII-compatible encoding (ACE) as specified in RFC 3492.
"""

from .core import encode, decode, PunycodeError, InvalidInput, Overflow
from .bootstring import Bootstring
from .idna import (
    to_ascii,
    to_unicode,
    to_ascii_domain,
    to_unicode_domain,
    IDNAError,
    InvalidLabel,
    LabelTooLong,
    DomainTooLong,
)

__version__ = "0.1.0"
__all__ = [
    # Punycode core functions
    "encode",
    "decode",
    "Bootstring",
    # Punycode exceptions
    "PunycodeError",
    "InvalidInput",
    "Overflow",
    # IDNA functions
    "to_ascii",
    "to_unicode",
    "to_ascii_domain",
    "to_unicode_domain",
    # IDNA exceptions
    "IDNAError",
    "InvalidLabel",
    "LabelTooLong",
    "DomainTooLong",
]