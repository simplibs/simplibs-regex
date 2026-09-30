from enum import Enum
from typing import NoReturn
from simplibs.exception import ParamError


def raise_char_code_out_of_range_error(kind: Enum, value: int, low: int, high: int) -> NoReturn:
    """Raise a structured ParamError when a numeric CharCode value is out of valid range."""
    raise ParamError(
        error_name="CHAR_CODE_OUT_OF_RANGE",
        label=f"CharCode {kind.name} range",
        value=str(value),
        problem=(
            f"CharCode({kind.name}, {value}) is invalid — expected {low} <= value <= {high}.",
            "The given character code exceeds the allowed range for this kind.",
        ),
        expected=f"A value between {low} and {high}.",
        how_to_fix=(
            f"Provide a numeric value within the range [{low}, {high}].",
        ),
        exception=ValueError,
    )