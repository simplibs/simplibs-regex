"""
Tests for the Conditional container.
"""
import pytest
from simplibs.regex.base_class.Regex import Regex
from simplibs.regex.containers.Conditional import Conditional


class DummyNode(Regex):
    def __init__(self, pattern: str, fixed_len: int | None = None):
        self._pattern = pattern
        self._fixed_len = fixed_len

    def to_pattern(self) -> str:
        return self._pattern

    def fixed_length(self) -> int | None:
        return self._fixed_len


def test_conditional_validation_id():
    """Verify validation of id_or_name parameter."""
    yes = DummyNode("a")
    # Invalid numeric ID (< 1)
    with pytest.raises(ValueError):
        Conditional(0, yes)
    # Invalid string identifier
    with pytest.raises(ValueError):
        Conditional("invalid-name!", yes)
    # Invalid type
    with pytest.raises(TypeError):
        Conditional(3.14, yes)  # type: ignore


def test_conditional_validation_branches():
    """Verify validation of yes and no branches."""
    with pytest.raises(TypeError):
        Conditional(1, "not-regex")  # type: ignore
    with pytest.raises(TypeError):
        Conditional(1, DummyNode("a"), no="not-regex")  # type: ignore


def test_conditional_patterns():
    """Verify pattern generation for Conditional with and without 'no' branch."""
    yes = DummyNode("a")
    no = DummyNode("b")

    cond_without_no = Conditional(1, yes)
    assert cond_without_no.to_pattern() == "(?(1)a)"

    cond_with_no = Conditional("group_name", yes, no)
    assert cond_with_no.to_pattern() == "(?(group_name)a|b)"


def test_conditional_fixed_length():
    """Verify fixed length calculation for Conditional."""
    yes_fixed = DummyNode("a", fixed_len=2)
    yes_diff = DummyNode("abc", fixed_len=3)
    no_fixed = DummyNode("b", fixed_len=2)

    # Without 'no' branch, length is always None (optional)
    assert Conditional(1, yes_fixed).fixed_length() is None

    # With both branches having identical fixed length
    assert Conditional(1, yes_fixed, no_fixed).fixed_length() == 2

    # With both branches having different fixed lengths
    assert Conditional(1, yes_fixed, yes_diff).fixed_length() is None