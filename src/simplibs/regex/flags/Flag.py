from enum import Enum
import re as _re


class Flag(Enum):
    """Inline regex flags — the letters usable inside `(?letters:...)` or
    `(?letters)`, and the corresponding `re` module flags for top-level
    `RegexPattern.compile(flags=...)`.

    Deliberately NOT a tree node (does not inherit from `Regex`): a flag
    has no `to_pattern`/`fixed_length` of its own — it only ever appears
    as a parameter to `Group` (scoped) or `RegexPattern.compile`
    (global), never as a standalone composable fragment.
    """

    ASCII = "a"
    IGNORECASE = "i"
    LOCALE = "L"
    MULTILINE = "m"
    DOTALL = "s"
    UNICODE = "u"
    VERBOSE = "x"

    @property
    def re_flag(self) -> _re.RegexFlag:
        """The corresponding `re` module flag, for top-level compilation."""
        return _RE_FLAG_TABLE[self]


_RE_FLAG_TABLE: dict[Flag, _re.RegexFlag] = {
    Flag.ASCII: _re.ASCII,
    Flag.IGNORECASE: _re.IGNORECASE,
    Flag.LOCALE: _re.LOCALE,
    Flag.MULTILINE: _re.MULTILINE,
    Flag.DOTALL: _re.DOTALL,
    Flag.UNICODE: _re.UNICODE,
    Flag.VERBOSE: _re.VERBOSE,
}


_DESIGN_NOTES = """
# Flag — Inline / Compile-Time Regex Flags

## Why this is an Enum living outside the Regex hierarchy
`re.DEBUG` and `re.NOFLAG` from the raw catalog are deliberately excluded
— `DEBUG` has no inline form at all (konverzace 4), and `NOFLAG` is just
the value `0`, not a flag a caller would ever compose with others.
Everything else maps 1:1 between its inline letter and its `re` module
constant, which is exactly what `re_flag` exposes — one table, used both
by `Group`'s inline rendering (the `.value` letter) and by
`RegexPattern.compile`'s top-level `flags=` (the `.re_flag` OR-ed
together), so the two call sites never risk disagreeing about what a
given `Flag` member means.
"""
