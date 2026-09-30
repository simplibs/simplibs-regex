# Outers
from ..base_class import Regex
# Inners
from .enums import CharCodeKind
from ._validations import (
    raise_char_code_invalid_kind_error,
    raise_char_code_invalid_named_value_error,
    raise_char_code_invalid_type_error,
    raise_char_code_out_of_range_error,
)


class CharCode(Regex):
    """A single character specified by numeric code or Unicode name.

    Unifies all 5 Python `re` character-code escape syntaxes into one
    parameterized mechanism.

    Pattern:
        \\xFF, \\uFFFF, \\U0010FFFF, \\N{NAME}, \\ooo  (depending on `kind`)

    Example:
        CharCode(CharCodeKind.HEX, 0x41)              # -> "\\x41"  (matches "A")
        CharCode(CharCodeKind.NAMED, "BULLET")         # -> "\\N{BULLET}"
    """

    __slots__ = ("kind", "value")

    # Point 4 — every one of these five escapes means the same thing
    # inside a CharacterClass as outside it (same rationale as
    # CharacterType), so always usable there[cite: 28].
    _usable_in_char_class = True

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(self, kind: CharCodeKind, value: int | str) -> None:

        # 1. Parameter validation — kind
        if not isinstance(kind, CharCodeKind):
            raise_char_code_invalid_kind_error(kind)

        # 2. Parameter validation — value, per kind[cite: 28]
        if kind is CharCodeKind.NAMED:
            if not isinstance(value, str) or not value:
                raise_char_code_invalid_named_value_error(value)
        else:
            if not isinstance(value, int):
                raise_char_code_invalid_type_error(kind, value)
            low, high = _VALUE_RANGES[kind]
            if not (low <= value <= high):
                raise_char_code_out_of_range_error(kind, value, low, high)

        # 3. Parameter assignment
        self.kind = kind
        self.value = value

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        if self.kind is CharCodeKind.HEX:
            return f"\\x{self.value:02x}"
        if self.kind is CharCodeKind.UNICODE_SHORT:
            return f"\\u{self.value:04x}"
        if self.kind is CharCodeKind.UNICODE_LONG:
            return f"\\U{self.value:08x}"
        if self.kind is CharCodeKind.NAMED:
            return f"\\N{{{self.value}}}"
        # OCTAL
        return f"\\{self.value:03o}"

    # ----------------------------------------------------------------------
    # Fixed-length introspection (Point 3)
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Every CharCode variant denotes exactly one character[cite: 28].
        return 1


# Populated after the class body so the Enum members already exist.
_VALUE_RANGES: dict[CharCodeKind, tuple[int, int]] = {
    CharCodeKind.HEX: (0x00, 0xFF),
    CharCodeKind.UNICODE_SHORT: (0x0000, 0xFFFF),
    CharCodeKind.UNICODE_LONG: (0x000000, 0x10FFFF),
    CharCodeKind.OCTAL: (0o0, 0o777),
}


_DESIGN_NOTES = """
# CharCode — Unified Character-Code Escape Mechanism

## The 5-to-1 collapse, with per-kind range validation
Same "one class, one enum" shape as `Anchor`/`CharacterType`, but each
kind additionally carries its own numeric range — a `CharCode(HEX, 300)`
is caught at construction time (300 > 0xFF) rather than producing
`\\x12c`, which is not valid `\\xFF`-style syntax at all and would only
fail later, confusingly, at `re.compile()`.

## Why NAMED is validated separately from the numeric kinds
`\\N{name}` takes a Unicode character name (a string), not a numeric
code — trying to route it through the same `_VALUE_RANGES` int-range
check as the other four would be a type error waiting to happen. The
`if kind is CharCodeKind.NAMED` branch keeps that one genuinely
different validation shape isolated, rather than forcing an awkward
"a range that doesn't apply" special case into the shared table.

## Why octal renders zero-padded to exactly 3 digits
`\\1` alone is ambiguous with a backreference — Python's `re` resolves
this by octal escapes needing to be distinguishable, and a
consistently zero-padded `\\ooo` (e.g. `\\001` rather than `\\1`) avoids
that ambiguity entirely at the syntax level, never relying on
context-dependent disambiguation rules a reader would have to know.
"""
