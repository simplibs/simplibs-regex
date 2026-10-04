from typing import AbstractSet, NoReturn
from simplibs.exception import ValidationError
from simplibs.regex.flags.Flag import Flag


def raise_group_flags_overlap_error(
    overlapping: AbstractSet[Flag]
) -> NoReturn:
    """Raise a structured ValidationError when flags overlap between flags and flags_off."""
    formatted_flags = ", ".join(sorted(f.name for f in overlapping))

    raise ValidationError(
        error_name="GROUP_FLAGS_OVERLAP",
        label="flags and flags_off",
        value=formatted_flags,
        problem=(
            f"The following flags appear in both `flags` and `flags_off`: {formatted_flags}.",
            "A flag cannot be simultaneously turned on and off in the same group scope.",
        ),
        expected="Disjoint sets for `flags` and `flags_off`.",
        how_to_fix=(
            f"Remove the conflicting flags ({formatted_flags}) from either `flags` or `flags_off`.",
            "Example: Group(inner, flags={Flag.IGNORECASE}, flags_off={Flag.MULTILINE})",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_group_flags_overlap_error — Flags Overlap Guard

## Purpose
Guards Group against specifying the same flag in both `flags` (ON) and `flags_off` (OFF).
"""