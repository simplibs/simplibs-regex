from typing import NoReturn
from simplibs.exception import ParamError


def raise_multi_char_literal_in_char_class_error(text: str) -> NoReturn:
    """Raise a structured ParamError when a multi-character Literal is passed to CharacterClass."""
    raise ParamError(
        error_name="MULTI_CHAR_LITERAL_IN_CHAR_CLASS",
        label="CharacterClass literal",
        value=text,
        problem=(
            f"CharacterClass() received a multi-character Literal({text!r}) with length {len(text)}.",
            "Character classes can only contain single-character literals.",
        ),
        expected="A single-character Literal (len == 1).",
        how_to_fix=(
            "Split multi-character strings into individual literals or use character ranges.",
        ),
        exception=ValueError,
    )