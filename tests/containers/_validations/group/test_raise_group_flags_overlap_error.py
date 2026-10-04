import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_group_flags_overlap_error,
)
from simplibs.regex.flags.Flag import Flag


def test_raise_group_flags_overlap_error_contract(subtests) -> None:
    """Verify that raise_group_flags_overlap_error raises ValidationError wrapping ValueError."""
    overlapping_flags = frozenset({Flag.IGNORECASE})
    formatted_flags = "IGNORECASE"

    assert_exception_function(
        subtests,
        raise_group_flags_overlap_error,
        invalid_params=(overlapping_flags,),
        exception_type=ValidationError,
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
        verbose=False,
    )