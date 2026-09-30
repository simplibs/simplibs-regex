"""
Tests for raise_conditional_invalid_id_type_error.
"""
import pytest
from simplibs.regex.containers._validations import (
    raise_conditional_invalid_id_type_error,
)
from simplibs.exception.exceptions import ParamError
from simplibs.exception.testing import assert_exception_function


@pytest.mark.parametrize("invalid_type", [1.5, None, object()])
def test_raise_conditional_invalid_id_type_error(subtests, invalid_type):
    """Verify that unsupported types for id_or_name raise a ParamError."""
    assert_exception_function(
        subtests,
        raise_conditional_invalid_id_type_error,
        invalid_params=(invalid_type,),
        exception_type=ParamError,
        value=type(invalid_type).__name__,
        label="Conditional id_or_name",
        expected="An int or str instance.",
        problem="requires an int or str for `id_or_name`",
        how_to_fix="Pass an integer group index or a string group name",
        exception=TypeError,
        verbose=False
    )