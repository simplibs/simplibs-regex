from typing import Any, NoReturn
from simplibs.exception import ParamError


def raise_repeat_invalid_mode_error(mode: Any) -> NoReturn:
    """Raise a structured ParamError when Repeat() receives an invalid mode type."""
    raise ParamError(
        error_name="REPEAT_INVALID_MODE",
        label="Repeat mode",
        value=type(mode).__name__,
        problem=(
            f"Repeat() requires a RepeatMode for `mode`, got {mode!r} of type '{type(mode).__name__}'.",
            "The mode parameter must be a valid member of the RepeatMode enumeration.",
        ),
        expected="A RepeatMode instance (e.g. RepeatMode.GREEDY, RepeatMode.LAZY, or RepeatMode.POSSESSIVE).",
        how_to_fix=(
            "Pass an explicit RepeatMode enum value.",
        ),
        exception=TypeError,
    )