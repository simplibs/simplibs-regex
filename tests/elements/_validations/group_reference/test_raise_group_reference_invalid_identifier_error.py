import pytest
from simplibs.exception import ValidationError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.elements._validations import raise_group_reference_invalid_identifier_error


def test_raise_group_reference_invalid_identifier_error_contract(subtests) -> None:
    invalid_value = "123-invalid"
    assert_exception_function(
        subtests,
        raise_group_reference_invalid_identifier_error,
        invalid_params=(invalid_value,),
        exception_type=ValidationError,
        error_name="GROUP_REFERENCE_INVALID_IDENTIFIER",
        label="id_or_name",
        value=invalid_value,
        problem=(
            f"Named group reference '{invalid_value}' is not a valid identifier.",
            "Group names must be valid Python identifiers (alphanumeric characters and underscores, not starting with a digit).",
        ),
        expected="A valid identifier string representing a named group.",
        how_to_fix=(
            "Provide a valid identifier string for the group name.",
            "Example: GroupReference('user_id')",
        ),
        exception=ValueError,
        verbose=False,
    )