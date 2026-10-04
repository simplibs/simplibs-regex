from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_character_code_unknown_name_error(
    value: Any
) -> NoReturn:
    """Raise a ParamError when a NAMED character code is not an official
    Unicode name of exactly one character.

    Args:
        value: The invalid name received.

    Raises:
        ParamError: Always.
    """
    raise ParamError(
        error_name="CHARACTER_CODE_UNKNOWN_NAME_ERROR",
        label="value",
        expected="an official Unicode character name that denotes exactly one character",
        value=value,
        problem=(
            f"Unicode has no single character named {value!r}.",
            "Names are looked up exactly like \\N{...} in Python's re (case-insensitive, aliases such as 'LINE FEED' are accepted).",
        ),
        how_to_fix=(
            "Check the spelling of the name.",
            "Example: CharacterCode(CharacterCodeKind.NAMED, 'BULLET') or 'LATIN SMALL LETTER A'",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_character_code_unknown_name_error — Unknown Unicode Name Guard

## Purpose
Guards CharacterCode(NAMED) against names that `re` would reject later
("undefined character name"), including names of multi-character named
sequences, so the mistake is reported at the line that built the node.
"""
