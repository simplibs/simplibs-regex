_NAMED_CONTROLS = {
    "\t": "\\t",
    "\n": "\\n",
    "\r": "\\r",
    "\f": "\\f",
    "\v": "\\v",
    "\a": "\\a",
}


def escape_control_character(char: str) -> str | None:
    """Return the readable `re` escape of a control character, or None.

    The six common controls become their short names (`\\t \\n \\r \\f \\v \\a`);
    every other control character (`U+0000`-`U+001F`, `U+007F`) becomes `\\xhh`.
    Any other character is not handled here: the function returns None and the
    caller escapes it in its own, context-specific way.
    """
    named = _NAMED_CONTROLS.get(char)
    if named is not None:
        return named

    code = ord(char)
    if code < 0x20 or code == 0x7F:
        return f"\\x{code:02x}"

    return None


_DESIGN_NOTES = """
# escape_control_character — Readable Control-Character Escapes

## Purpose
One shared rule for how control characters are written into a pattern, used
by `Literal` (outside a class) and `escape_char_class_char` (inside one).

## Why not leave it to `re.escape`
`re.escape("\\n")` is a backslash followed by an ACTUAL newline: valid, but
invisible. Pattern strings, error messages and test expectations then break
across lines and cannot be read or compared by eye. `\\n` means exactly the
same to `re`, so only the text of the pattern changes, never its behaviour.

## Why one function for both contexts
`\\t \\n \\r \\f \\v \\a` and `\\xhh` mean the same inside and outside `[...]`
(unlike `\\1`), so the rule is defined once. `\\b` is deliberately NOT used for
backspace: outside a class it is a word boundary, so U+0008 is written
`\\x08`.

## Why a space is not handled here
A space is not a control character. `re.escape` writes it `\\ `, which also
keeps it safe under the `VERBOSE` flag, so `Literal` leaves it to `re.escape`.
"""
