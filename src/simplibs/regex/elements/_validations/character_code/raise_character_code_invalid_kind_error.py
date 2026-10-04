from typing import Any, NoReturn
from simplibs.exception import ValidationError


def raise_character_code_invalid_kind_error(kind: Any) -> NoReturn:
    """Raise a structured ValidationError when CharacterCodeKind is invalid."""
    raise ValidationError(
        error_name="CHAR_CODE_INVALID_KIND",
        label="kind",
        value=kind,
        problem=(
            f"Invalid character code kind: {kind!r}.",
            "The kind parameter must be a valid member of the `CharacterCodeKind` enum.",
        ),
        expected="A valid `CharacterCodeKind` instance (e.g., CharacterCodeKind.HEX).",
        how_to_fix=(
            "Provide a valid `CharacterCodeKind` enum member.",
            "Example: CharacterCode(CharacterCodeKind.HEX, 0x41)",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_character_code_invalid_kind_error — Invalid CharacterCode Kind Guard

## Purpose
Guards CharacterCode against invalid kind arguments that do not belong to the `CharacterCodeKind` enum.
"""