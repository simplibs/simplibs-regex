from enum import Enum


class CharCodeKind(Enum):
    """Which character-code escape syntax a CharCode represents."""

    HEX = "hex"                # \xFF        — value: int 0-255
    UNICODE_SHORT = "u_short"  # \uFFFF      — value: int 0-0xFFFF
    UNICODE_LONG = "u_long"    # \U0010FFFF  — value: int 0-0x10FFFF
    NAMED = "named"            # \N{NAME}    — value: str (Unicode name)
    OCTAL = "octal"            # \ooo        — value: int 0-0o777


_DESIGN_NOTES = """
# CharCodeKind — Character-Code Escape Syntax Kind

## Purpose
Defines the specific character-code escape syntax variant represented by 
a `CharCode` element (such as hexadecimal, short/long unicode, named unicode, 
or octal codes).

## Members
- `HEX`: Represents a two-digit hexadecimal character code (`\\xFF`).
- `UNICODE_SHORT`: Represents a four-digit Unicode character code (`\\uFFFF`).
- `UNICODE_LONG`: Represents an eight-digit Unicode character code (`\\U0010FFFF`).
- `NAMED`: Represents a Unicode character by its formal name (`\\N{NAME}`).
- `OCTAL`: Represents an octal character code (`\\ooo`).
"""