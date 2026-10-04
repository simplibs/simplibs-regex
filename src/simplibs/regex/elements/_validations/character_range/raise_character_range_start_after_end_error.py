from typing import NoReturn
from simplibs.exception import ValidationError


def raise_character_range_start_after_end_error(
    start: str,
    end: str,
) -> None:
    """Raise a structured ValidationError when start character comes after end character."""
    raise ValidationError(
        error_name="CHARACTER_RANGE_START_AFTER_END",
        label="start/end",
        value=f"{start}-{end}",
        problem=(
            f"Character range start ('{start}', ord={ord(start)}) cannot come after end ('{end}', ord={ord(end)}).",
            "The starting character of a range must have a lower or equal ASCII/Unicode code point than the ending character.",
        ),
        expected="A valid ascending range (start <= end).",
        how_to_fix=(
            "Swap the start and end characters so they form an ascending range.",
            f"Example: CharacterRange('{end}', '{start}')",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_character_range_start_after_end_error — Range Start After End Guard

## Purpose
Guards CharacterRange against inverted ranges where the start character has a higher code point than the end character.
"""