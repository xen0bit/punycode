"""
Punycode (RFC 3492) implementation entry point.

This module provides a command-line interface for encoding and decoding
Punycode strings and IDNA (Internationalized Domain Names in Applications).
"""

import sys
import argparse
from punycode import (
    encode,
    decode,
    to_ascii,
    to_unicode,
    to_ascii_domain,
    to_unicode_domain,
)


def main():
    """Main entry point for the punycode package."""
    parser = argparse.ArgumentParser(
        description="Punycode encoder/decoder (RFC 3492) and IDNA support"
    )
    parser.add_argument(
        "action",
        choices=["encode", "decode", "to-ascii", "to-unicode", "to-ascii-domain", "to-unicode-domain"],
        help="Action to perform"
    )
    parser.add_argument("input", help="Input string")
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="punycode 0.1.0"
    )

    args = parser.parse_args()

    try:
        if args.action == "encode":
            # Basic Punycode encoding
            result = encode(args.input)
            print(result)
        elif args.action == "decode":
            # Basic Punycode decoding
            result = decode(args.input)
            print(result)
        elif args.action == "to-ascii":
            # IDNA label to ASCII (with ACE prefix)
            result = to_ascii(args.input)
            print(result)
        elif args.action == "to-unicode":
            # IDNA label from ASCII (removes ACE prefix)
            result = to_unicode(args.input)
            print(result)
        elif args.action == "to-ascii-domain":
            # IDNA domain to ASCII
            result = to_ascii_domain(args.input)
            print(result)
        elif args.action == "to-unicode-domain":
            # IDNA domain from ASCII
            result = to_unicode_domain(args.input)
            print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()