from typing import AbstractSet, NoReturn
from simplibs.exception import ValidationError
from simplibs.regex.flags.Flag import Flag


def raise_flags_off_restricted_error(
    not_turnable_off: AbstractSet[Flag]
) -> NoReturn:
    """Raise a structured ValidationError when flags_off contains flags that Python's re cannot turn off."""
    formatted_flags = ", ".join(sorted(f.name for f in not_turnable_off))

    raise ValidationError(
        error_name="FLAGS_OFF_RESTRICTED",
        label="flags_off",
        value=formatted_flags,
        problem=(
            f"The following flags cannot be turned off in Python's regex: {formatted_flags}.",
            "Python's `re` module only permits turning off IGNORECASE, MULTILINE, DOTALL, and VERBOSE.",
        ),
        expected="Only turnable-off flags in `flags_off` (ASCII, LOCALE, and UNICODE cannot be turned off).",
        how_to_fix=(
            "Remove ASCII, LOCALE, or UNICODE from the `flags_off` set.",
            "Example: Group(inner, flags={Flag.ASCII}, flags_off={Flag.IGNORECASE})",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_flags_off_restricted_error — Restricted Flags-Off Guard

## Purpose
Guards Group against attempting to turn off flags (like ASCII, UNICODE, LOCALE) that Python's engine doesn't allow to be scoped-off.
"""