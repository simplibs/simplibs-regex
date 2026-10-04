import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import raise_group_reference_numeric_out_of_range_error


def test_raise_group_reference_numeric_out_of_range_error_contract(subtests) -> None:
    invalid_value = 150
    low, high = 1, 99

    assert_exception_function(
        subtests,
        raise_group_reference_numeric_out_of_range_error,
        invalid_params=(invalid_value, low, high),
        exception_type=ValidationError,
        error_name="GROUP_REFERENCE_NUMERIC_OUT_OF_RANGE",
        label="id_or_name",
        value=invalid_value,
        problem=(
            f"Numeric group reference {invalid_value} is out of range.",
            f"Python's regex engine supports numbered backreferences only from {low} to {high} (values >= 100 are treated as octal escapes).",
        ),
        expected=f"An integer between {low} and {high}, or a named group string.",
        how_to_fix=(
            f"Provide a group number between {low} and {high}, or use a named group reference.",
            "Example: GroupReference(5) or GroupReference('group_name')",
        ),
        exception=ValueError,
        verbose=False,
    )