from typing import NoReturn
from simplibs.exception import ValidationError


def raise_literal_not_single_char_error(text: str) -> NoReturn:
    """Raise a structured ValidationError when a multi-character literal is rendered inside a character class."""
    raise ValidationError(
        error_name="LITERAL_NOT_SINGLE_CHAR",
        label="text",
        value=text,
        problem=(
            f"Literal text '{text}' has length {len(text)}, but character classes require single-character fragments.",
            "Multi-character literals cannot be rendered directly inside character class brackets (`[...]`).",
        ),
        expected="A single-character literal (e.g., Literal('a')).",
        how_to_fix=(
            "Ensure the literal contains only one character when used inside a CharacterClass.",
            "Example: CharacterClass(Literal('a'))",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_literal_not_single_char_error — Multi-Character Literal Fragment Guard

## Purpose
Guards against attempting to render a multi-character literal as a character class fragment where only single characters are legal.
"""