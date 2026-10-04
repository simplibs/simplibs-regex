import pytest

from simplibs.exception import ParamError
from simplibs.exception.testing import assert_exception_function
from simplibs.regex.containers._validations import (
    raise_conditional_invalid_id_type_error,
)


@pytest.mark.parametrize(
    "invalid_id",
    [
        True,
        False,
        3.14,
        None,
        ["group1"],
    ],
)
def test_raise_conditional_invalid_id_type_error_contract(
    subtests,
    invalid_id,
) -> None:
    """Verify that raise_conditional_invalid_id_type_error raises ParamError
    wrapping TypeError when a conditional group reference has an invalid type."""

    received_type = type(invalid_id).__name__

    assert_exception_function(
        subtests,
        raise_conditional_invalid_id_type_error,
        invalid_params=(invalid_id,),
        exception_type=ParamError,
        error_name="CONDITIONAL_INVALID_ID_TYPE_ERROR",
        label="id_or_name",
        expected="an integer (>= 1) or a string identifier",
        value=invalid_id,
        problem=(
            f"Conditional group reference received an invalid type '{received_type}' with value {invalid_id!r}.",
            "Booleans and other non-int/non-str types are not valid group references.",
        ),
        how_to_fix=(
            "Provide either a positive integer group number or a string group identifier.",
            "Example: Conditional(1, Literal('yes'), Literal('no')) or Conditional('group_name', Literal('yes'))",
        ),
        exception=TypeError,
        verbose=False,
    )