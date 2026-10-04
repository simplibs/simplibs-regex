from typing import NoReturn
from simplibs.exception import ValidationError


def raise_group_atomic_and_flags_conflict_error() -> NoReturn:
    """Raise a structured ValidationError when atomic=True is combined with scoped flags."""
    raise ValidationError(
        error_name="GROUP_ATOMIC_AND_FLAGS_CONFLICT",
        label="Group modifiers",
        value="atomic=True, flags",
        problem=(
            "`atomic=True` cannot be combined with `flags`/`flags_off`.",
            "Python's `re` syntax does not support scoped flags inside an atomic group opening.",
        ),
        expected="Only one structural modifier (atomic or flags) per group.",
        how_to_fix=(
            "Separate scoped flags and atomic grouping into nested groups.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_group_atomic_and_flags_conflict_error — Atomic and Flags Conflict Guard

## Purpose
Guards Group against combining atomic grouping with scoped flags, which Python regex syntax forbids.
"""