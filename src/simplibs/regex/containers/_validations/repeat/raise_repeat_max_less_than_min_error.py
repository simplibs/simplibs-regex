from typing import NoReturn
from simplibs.exception import ParamError


def raise_repeat_max_less_than_min_error(min_val: int, max_val: int) -> NoReturn:
    """Raise a structured ParamError when Repeat() max is less than min."""
    raise ParamError(
        error_name="REPEAT_MAX_LESS_THAN_MIN",
        label="Repeat bounds",
        value=f"min={min_val}, max={max_val}",
        problem=(
            f"Repeat() requires max >= min, got min={min_val}, max={max_val}.",
            "Quantifier maximum boundary cannot be smaller than its minimum boundary.",
        ),
        expected="max >= min.",
        how_to_fix=(
            "Ensure `max` is greater than or equal to `min`, or leave `max=None` for unbounded repetition.",
        ),
        exception=ValueError,
    )