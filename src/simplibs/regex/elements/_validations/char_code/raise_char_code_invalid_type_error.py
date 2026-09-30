from enum import Enum
from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_char_code_invalid_type_error(kind: Enum, value: Any) -> NoReturn:
    """Raise a structured ParamError when a numeric CharCode receives a non-int value."""
    raise ParamError(
        error_name="CHAR_CODE_INVALID_TYPE",
        label=f"CharCode {kind.name} value",
        value=type(value).__name__,
        problem=(
            f"CharCode({kind.name}, ...) requires an int value, got {value!r} of type '{type(value).__name__}'.",
            "Numeric character codes must be specified using integer values.",
        ),
        expected="An integer value.",
        how_to_fix=(
            "Pass an integer representing the character code.",
        ),
        exception=TypeError,
    )