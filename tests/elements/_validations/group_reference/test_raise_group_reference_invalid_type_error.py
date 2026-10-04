import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import raise_group_reference_invalid_type_error


def test_raise_group_reference_invalid_type_error_contract(subtests) -> None:
    invalid_value = True
    assert_exception_function(
        subtests,
        raise_group_reference_invalid_type_error,
        invalid_params=(invalid_value,),
        exception_type=ValidationError,
        error_name="GROUP_REFERENCE_INVALID_TYPE",
        label="id_or_name",
        value=invalid_value,
        problem=(
            f"Invalid group reference type: received {invalid_value!r} (type bool).",
            "Booleans and non-integer/non-string types are not permitted as group references.",
        ),
        expected="An integer group number (1-99) or a valid identifier string for a named group.",
        how_to_fix=(
            "Provide an integer or a string instead of a boolean or other type.",
            "Example: GroupReference(1) or GroupReference('year')",
        ),
        exception=TypeError,
        verbose=False,
    )