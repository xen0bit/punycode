"""
IDNA (Internationalized Domain Names in Applications) support.

This module implements the higher-level IDNA operations as specified in RFC 3490,
which builds on Punycode (RFC 3492) and Nameprep (RFC 3491).
"""

import unicodedata
from typing import Optional, Tuple

from .core import encode, decode, PunycodeError


# IDNA ACE prefix
ACE_PREFIX = "xn--"


class IDNAError(PunycodeError):
    """Base exception for IDNA errors."""
    pass


class InvalidLabel(IDNAError):
    """Raised when a label is invalid for IDNA processing."""
    pass


class LabelTooLong(InvalidLabel):
    """Raised when a label exceeds the 63-character limit."""
    pass


class DomainTooLong(IDNAError):
    """Raised when a domain name exceeds the 255-character limit."""
    pass


def to_ascii(label: str) -> str:
    """
    Convert a Unicode label to ASCII using IDNA (Punycode encoding).

    Args:
        label: Unicode domain label to encode

    Returns:
        Punycode-encoded ASCII label with ACE prefix

    Raises:
        LabelTooLong: If the encoded label exceeds 63 characters
        InvalidLabel: If the label contains invalid characters
    """
    if not label:
        raise InvalidLabel("Empty label")

    # Normalize to lowercase for encoding (per IDNA spec)
    label = label.lower()

    # Check if it's already ASCII
    if label.isascii():
        return label

    # Normalize to NFC form (per IDNA2008 recommendation)
    label = unicodedata.normalize('NFC', label)

    # Encode using Punycode
    encoded = encode(label)

    # Add ACE prefix
    result = ACE_PREFIX + encoded

    # Check length limit (63 characters for DNS labels)
    if len(result) > 63:
        raise LabelTooLong(
            f"Encoded label '{result}' exceeds 63 character limit (length: {len(result)})"
        )

    return result


# CHAOS AGENT DISRUPTION: to_unicode() function deleted (27 lines)
# This function handled IDNA label decoding including:
# - ACE prefix validation
# - Punycode decoding
# - NFC normalization
# The builder must re-implement to restore IDNA decoding functionality

def to_ascii_domain(domain: str) -> str:
    """
    Convert a Unicode domain name to ASCII using IDNA.

    Args:
        domain: Unicode domain name (e.g., "例え.jp" or "例子.测试")

    Returns:
        ASCII domain name with IDNA encoding (e.g., "xn--r8jz45g.jp" or "xn--fsq.xn--0zm"")

    Raises:
        DomainTooLong: If the encoded domain exceeds 253 characters
        InvalidLabel: If any label in the domain is invalid
    """
    if not domain:
        raise InvalidLabel("Empty domain")

    # Split into labels
    labels = domain.split('.')

    # Encode each label
    encoded_labels = []
    for label in labels:
        # Empty labels are allowed (for trailing dot)
        if not label:
            encoded_labels.append('')
        else:
            encoded_labels.append(to_ascii(label))

    # Join back together
    result = '.'.join(encoded_labels)

    # Check length limit (253 characters for DNS domain names)
    # Note: RFC 1034 says 255 octets, but DNS doesn't count the trailing dot
    if len(result) > 253:
        raise DomainTooLong(
            f"Encoded domain '{result}' exceeds 253 character limit (length: {len(result)})"
        )

    return result


def to_unicode_domain(domain: str) -> str:
    """
    Convert an ASCII domain name to Unicode using IDNA.

    Args:
        domain: ASCII domain name (e.g., "xn--r8jz45g.jp" or "www.xn--0zwm56d.com")

    Returns:
        Unicode domain name with decoded ACE labels (e.g., "例え.jp" or "www.测试.com")

    Raises:
        InvalidLabel: If any label in the domain is invalid
    """
    if not domain:
        raise InvalidLabel("Empty domain")

    # Split into labels
    labels = domain.split('.')

    # Decode each label
    decoded_labels = []
    for label in labels:
        # Empty labels are allowed (for trailing dot)
        if not label:
            decoded_labels.append('')
        else:
            decoded_labels.append(to_unicode(label))

    # Join back together
    return '.'.join(decoded_labels)


# CHAOS AGENT SUGGESTION: Architecture
# Consider enhancing with: Split domain validation and decoding/encoding into separate responsibilities
# Rationale: This would improve testability, allow for validation-only modes, and follow single responsibility principle