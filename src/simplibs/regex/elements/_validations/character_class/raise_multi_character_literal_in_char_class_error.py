from typing import NoReturn
from simplibs.exception import ValidationError


def raise_multi_character_literal_in_char_class_error(
    text: str
) -> NoReturn:
    """Raise a structured ValidationError when a multi-character Literal is passed to CharacterClass."""
    raise ValidationError(
        error_name="MULTI_CHAR_LITERAL_IN_CHAR_CLASS",
        label="items",
        value=text,
        problem=(
            f"Literal text '{text}' has length {len(text)}, but character classes only accept single-character literals.",
            "A character class matches a single character from a set; multi-character strings cannot be direct members.",
        ),
        expected="A single-character Literal (e.g., Literal('a')).",
        how_to_fix=(
            "Pass single-character Literals or split the string into individual characters.",
            "Example: CharacterClass(Literal('a'), Literal('b'))",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_multi_character_literal_in_char_class_error — Multi-Character Literal Guard

## Purpose
Guards CharacterClass against multi-character Literal items, which would break the single-character matching semantics of brackets.
"""