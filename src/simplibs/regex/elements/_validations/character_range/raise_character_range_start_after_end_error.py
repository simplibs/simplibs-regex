from typing import NoReturn
from simplibs.exception import ParamError


def raise_character_range_start_after_end_error(start: str, end: str) -> NoReturn:
    """Raise a structured ParamError when CharacterRange start comes after end."""
    raise ParamError(
        error_name="CHARACTER_RANGE_START_AFTER_END",
        label="CharacterRange bounds",
        value=f"start={start!r}, end={end!r}",
        problem=(
            f"CharacterRange({start!r}, {end!r}) is invalid — `start` must not come after `end`.",
            "Range boundaries must be in ascending ASCII/Unicode order.",
        ),
        expected="start <= end in character order.",
        how_to_fix=(
            "Ensure `start` comes before or equals `end`.",
        ),
        exception=ValueError,
    )