from typing import NoReturn
from simplibs.exception import ParamError


def raise_literal_not_single_char_error(text: str) -> NoReturn:
    """Raise a structured ParamError when a multi-character Literal is used as a char class fragment."""
    raise ParamError(
        error_name="LITERAL_NOT_SINGLE_CHAR",
        label="Literal char class fragment",
        value=text,
        problem=(
            f"Literal({text!r}) is not a single character — it cannot be used as a CharacterClass item.",
            "Character classes require single-character fragments.",
        ),
        expected="A single-character Literal (len == 1).",
        how_to_fix=(
            "Ensure only single-character literals are used inside character classes.",
        ),
        exception=ValueError,
    )