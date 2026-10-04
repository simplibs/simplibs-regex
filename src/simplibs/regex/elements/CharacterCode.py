import unicodedata
# Outers
from ..base_class import Regex
# Inners
from .enums import CharacterCodeKind
from ._validations import (
    raise_character_code_invalid_kind_error,
    raise_character_code_invalid_named_value_error,
    raise_character_code_unknown_name_error,
    raise_character_code_invalid_type_error,
    raise_character_code_out_of_range_error,
)


class CharacterCode(Regex):
    """A single character specified by numeric code or Unicode name.

    Unifies all 5 Python `re` character-code escape syntaxes into one
    parameterized mechanism.

    Pattern:
        \\xFF, \\uFFFF, \\U0010FFFF, \\N{NAME}, \\ooo  (depending on `kind`)

    Example:
        CharacterCode(CharacterCodeKind.HEX, 0x41)              # -> "\\x41"  (matches "A")
        CharacterCode(CharacterCodeKind.NAMED, "BULLET")         # -> "\\N{BULLET}"
        CharacterCode(CharacterCodeKind.OCTAL, 0o101)            # -> "\\101"  (matches "A")
    """

    __slots__ = ("kind", "value")

    # Every one of these five escapes means the same thing
    # inside a CharacterClass as outside it (same rationale as
    # CharacterType), so always usable there.
    _usable_in_char_class = True

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        kind: CharacterCodeKind,
        value: int | str
    ) -> None:

        # 1. Parameter validation — kind type
        if not isinstance(kind, CharacterCodeKind):
            raise_character_code_invalid_kind_error(kind)

        # 2. Parameter validation — NAMED needs a non-empty string
        if kind is CharacterCodeKind.NAMED:
            if not isinstance(value, str) or not value:
                raise_character_code_invalid_named_value_error(value)

            # 2.1 The name must denote exactly one character — looked up the
            #     same way `re` resolves `\\N{...}`, so an unknown name fails here
            #     instead of at compile time. A named sequence of several
            #     characters is rejected by `re` too.
            try:
                character = unicodedata.lookup(value)
            except KeyError:
                character = ""
            if len(character) != 1:
                raise_character_code_unknown_name_error(value)

        # 3. Parameter validation — numeric kinds
        else:

            # 3.1 Parameter validation — must be an int (bool is a subclass of int, so it is excluded explicitly)
            if isinstance(value, bool) or not isinstance(value, int):
                raise_character_code_invalid_type_error(kind, value)

            # 3.2 Parameter validation — range check per numeric kind
            low, high = _VALUE_RANGES[kind]
            if not (low <= value <= high):
                raise_character_code_out_of_range_error(kind, value, low, high)

        # 4. Parameter assignment
        self.kind = kind
        self.value = value

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        if self.kind is CharacterCodeKind.HEX:
            return f"\\x{self.value:02x}"
        if self.kind is CharacterCodeKind.UNICODE_SHORT:
            return f"\\u{self.value:04x}"
        if self.kind is CharacterCodeKind.UNICODE_LONG:
            return f"\\U{self.value:08x}"
        if self.kind is CharacterCodeKind.NAMED:
            return f"\\N{{{self.value}}}"
        # OCTAL
        return f"\\{self.value:03o}"

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Every CharacterCode variant denotes exactly one character.
        return 1


# Populated after the class body so the Enum members already exist.
_VALUE_RANGES: dict[CharacterCodeKind, tuple[int, int]] = {
    CharacterCodeKind.HEX: (0x00, 0xFF),
    CharacterCodeKind.UNICODE_SHORT: (0x0000, 0xFFFF),
    CharacterCodeKind.UNICODE_LONG: (0x000000, 0x10FFFF),
    CharacterCodeKind.OCTAL: (0o0, 0o377),
}


_DESIGN_NOTES = """
# CharacterCode — Unified Character-Code Escape Mechanism

## The 5-to-1 collapse, with per-kind range validation
Same "one class, one enum" shape as `Anchor`/`CharacterType`, but each
kind additionally carries its own numeric range — a `CharacterCode(HEX, 300)`
is caught at construction time (300 > 0xFF) rather than producing
`\\x12c`, which is not valid `\\xFF`-style syntax at all and would only
fail later, confusingly, at `re.compile()`.

## Why NAMED is validated separately from the numeric kinds
`\\N{name}` takes a Unicode character name (a string), not a numeric
code — trying to route it through the same `_VALUE_RANGES` int-range
check as the other four would be a type error waiting to happen. The
`if kind is CharacterCodeKind.NAMED` branch keeps that one genuinely
different validation shape isolated, rather than forcing an awkward
"a range that doesn't apply" special case into the shared table.

The name is looked up with `unicodedata.lookup`, the same function `re`
uses for `\\N{...}`, so an unknown name is rejected at construction
instead of at compile time. Lookup is case-insensitive and accepts
aliases (`LINE FEED`). Named sequences (more than one character) are
rejected too, exactly as `re` rejects them.

## Why OCTAL stops at 0o377
Python's `re` accepts an octal escape only up to `\\377` (character code
255); `\\400` and above fail with "octal escape value outside of range".
The range is verified against `re.compile` itself, so a value such as
`0o400` is rejected at construction time with a clear message.

## Why octal renders zero-padded to exactly 3 digits
`\\1` alone is ambiguous with a backreference — Python's `re` resolves
this by octal escapes needing to be distinguishable, and a
consistently zero-padded `\\ooo` (e.g. `\\001` rather than `\\1`) avoids
that ambiguity entirely at the syntax level, never relying on
context-dependent disambiguation rules a reader would have to know.

## Why `bool` is rejected
`True` and `False` are `int` instances in Python, so a plain type check
would accept `CharacterCode(HEX, True)` and silently render `\\x01`. They are
refused explicitly as an invalid type.
"""