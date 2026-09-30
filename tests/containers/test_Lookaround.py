"""
Tests for the Lookaround container.
"""
import pytest
from simplibs.regex.base_class.Regex import Regex
from simplibs.regex.containers.Lookaround import Lookaround, LookaroundDirection


class DummyNode(Regex):
    def __init__(self, pattern: str, fixed_len: int | None = None):
        self._pattern = pattern
        self._fixed_len = fixed_len

    def to_pattern(self) -> str:
        return self._pattern

    def fixed_length(self) -> int | None:
        return self._fixed_len


def test_lookaround_validation():
    """Verify validation of parameters and variable-length lookbehinds."""
    inner_var = DummyNode("a", fixed_len=None)
    inner_fixed = DummyNode("a", fixed_len=1)

    # Invalid inner type
    with pytest.raises(TypeError):
        Lookaround("not-regex", direction=LookaroundDirection.AHEAD)  # type: ignore

    # Invalid direction type
    with pytest.raises(TypeError):
        Lookaround(inner_fixed, direction="ahead")  # type: ignore

    # Point 3 enforcement: variable-length lookbehind must raise ValueError
    with pytest.raises(ValueError):
        Lookaround(inner_var, direction=LookaroundDirection.BEHIND)

    # Fixed-length lookbehind should pass
    look_behind = Lookaround(inner_fixed, direction=LookaroundDirection.BEHIND)
    assert look_behind.fixed_length() == 0


def test_lookaround_patterns():
    """Verify pattern production for all 4 lookaround variants."""
    inner = DummyNode("abc", fixed_len=3)

    assert Lookaround(inner, direction=LookaroundDirection.AHEAD, negate=False).to_pattern() == "(?=abc)"
    assert Lookaround(inner, direction=LookaroundDirection.AHEAD, negate=True).to_pattern() == "(?!abc)"
    assert Lookaround(inner, direction=LookaroundDirection.BEHIND, negate=False).to_pattern() == "(?<=abc)"
    assert Lookaround(inner, direction=LookaroundDirection.BEHIND, negate=True).to_pattern() == "(?<!abc)"

def test_lookaround_fixed_length():
    """Verify that any Lookaround always reports a fixed length of 0 (zero-width assertion)."""
    inner = DummyNode("abc", fixed_len=3)
    look = Lookaround(inner, direction=LookaroundDirection.AHEAD)
    assert look.fixed_length() == 0