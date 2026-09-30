from typing import NoReturn
from simplibs.exception import ParamError


def raise_repeat_min_negative_error(min_val: int) -> NoReturn:
    """Raise a structured ParamError when Repeat() receives a negative min value."""
    raise ParamError(
        error_name="REPEAT_MIN_NEGATIVE",
        label="Repeat min",
        value=min_val,
        problem=(
            f"Repeat() requires min >= 0, got min={min_val}.",
            "Quantifier minimum repetition count cannot be negative.",
        ),
        expected="An integer greater than or equal to 0.",
        how_to_fix=(
            "Provide a non-negative integer for the `min` parameter.",
        ),
        exception=ValueError,
    )