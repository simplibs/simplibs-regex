import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_param_not_identifier_error,
)


@pytest.mark.parametrize(
    "param_name, invalid_value",
    [
        ("name", "123group"),
        ("name", "my-group"),
        ("id_or_name", "invalid name with spaces"),
        ("id_or_name", "group.name"),
    ],
)
def test_raise_param_not_identifier_error_contract(
    subtests,
    param_name,
    invalid_value,
) -> None:
    """Verify that raise_param_not_identifier_error raises ParamError
    wrapping ValueError when a parameter value is not a valid identifier."""

    assert_exception_function(
        subtests,
        raise_param_not_identifier_error,
        invalid_params=(param_name, invalid_value),
        exception_type=ParamError,
        error_name="PARAM_NOT_IDENTIFIER_ERROR",
        label=param_name,
        expected="a valid Python identifier string",
        value=invalid_value,
        problem=(
            f"Parameter '{param_name}' received value {invalid_value!r}, which is not a valid identifier.",
            "Identifiers must consist of alphanumeric characters and underscores, and cannot start with a digit.",
        ),
        how_to_fix=(
            f"Provide a valid Python identifier string for parameter '{param_name}'.",
            "Example: use alphanumeric characters and underscores (e.g., 'my_group', 'target1').",
        ),
        exception=ValueError,
        verbose=False,
    )