from typing import Any, NoReturn
from simplibs.exception import ValidationError


def raise_character_class_item_not_allowed_error(
    item: Any
) -> NoReturn:
    """Raise a structured ValidationError when an item is not allowed inside a CharacterClass."""
    received_type = type(item).__name__

    raise ValidationError(
        error_name="CHAR_CLASS_ITEM_NOT_ALLOWED",
        label="items",
        value=item,
        problem=(
            f"Item of type '{received_type}' with value {item!r} is not allowed inside a character class.",
            "Only specific regex elements opted into character class usage (`_usable_in_char_class = True`) are permitted.",
        ),
        expected="A valid character class item (Literal, CharacterType, CharacterRange, or CharacterCode).",
        how_to_fix=(
            "Ensure all items passed to CharacterClass are supported inside character classes.",
            "Example: CharacterClass(DIGIT, Literal('a'))",
        ),
        exception=TypeError,
    )


_DESIGN_NOTES = """
# raise_character_class_item_not_allowed_error — Item Not Allowed in Character Class Guard

## Purpose
Guards CharacterClass against receiving unsupported items that cannot be rendered inside character class brackets.
"""