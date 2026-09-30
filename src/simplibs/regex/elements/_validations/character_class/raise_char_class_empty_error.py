from typing import NoReturn
from simplibs.exception import ParamError


def raise_char_class_empty_error() -> NoReturn:
    """Raise a structured ParamError when CharacterClass() receives no items."""
    raise ParamError(
        error_name="CHAR_CLASS_EMPTY",
        label="CharacterClass items",
        value="none",
        problem=(
            "CharacterClass() requires at least one item — got none.",
            "A character class cannot be empty.",
        ),
        expected="At least one valid regex item for the character class.",
        how_to_fix=(
            "Provide one or more items (like Literals, CharacterRanges, or CharacterTypes).",
        ),
        exception=ValueError,
    )