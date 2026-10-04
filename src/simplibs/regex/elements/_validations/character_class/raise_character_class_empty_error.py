from typing import NoReturn
from simplibs.exception import ValidationError


def raise_character_class_empty_error() -> NoReturn:
    """Raise a structured ValidationError when a CharacterClass has no items."""
    raise ValidationError(
        error_name="CHAR_CLASS_EMPTY",
        label="items",
        value="()",
        problem=(
            "A character class (`[...]`) cannot be empty.",
            "Python's regex engine requires at least one character or item inside a character class.",
        ),
        expected="At least one valid regex item (e.g., Literal, CharacterType, CharacterRange).",
        how_to_fix=(
            "Provide one or more items to include in the character class.",
            "Example: CharacterClass(Literal('a'), Literal('b'))",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_character_class_empty_error — Empty Character Class Guard

## Purpose
Guards CharacterClass against being constructed with zero items.
"""