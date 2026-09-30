from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_char_class_item_not_allowed_error(item: Any) -> NoReturn:
    """Raise a structured ParamError when an item is not allowed inside a CharacterClass."""
    raise ParamError(
        error_name="CHAR_CLASS_ITEM_NOT_ALLOWED",
        label="CharacterClass item",
        value=type(item).__name__,
        problem=(
            f"CharacterClass() received an item {item!r} of type '{type(item).__name__}' which is not allowed.",
            "Only specific nodes opted into character-class usage (_usable_in_char_class=True) are permitted.",
        ),
        expected="A valid character class item (Literal, CharacterType, CharacterRange, or CharCode).",
        how_to_fix=(
            "Ensure all items passed to CharacterClass support character class contexts.",
        ),
        exception=TypeError,
    )