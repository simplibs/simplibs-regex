"""
Tests for the Alternation container.
"""
import pytest
from simplibs.regex.base_class.Regex import Regex, Precedence
from simplibs.regex.containers.Alternation import Alternation


class DummyNode(Regex):
    def __init__(self, pattern: str, precedence: Precedence = Precedence.ATOM, fixed_len: int | None = None):
        self._pattern = pattern
        self._precedence = precedence
        self._fixed_len = fixed_len

    def to_pattern(self) -> str:
        return self._pattern

    def fixed_length(self) -> int | None:
        return self._fixed_len


def test_alternation_requires_nodes():
    """Verify that empty alternation raises an error."""
    with pytest.raises(ValueError):
        Alternation()


def test_alternation_invalid_node_type():
    """Verify that non-Regex nodes raise a TypeError."""
    with pytest.raises(TypeError):
        Alternation(DummyNode("a"), "not-a-regex")  # type: ignore


def test_alternation_flattening():
    """Verify that nested Alternations are flattened."""
    alt1 = Alternation(DummyNode("a"), DummyNode("b"))
    alt2 = Alternation(alt1, DummyNode("c"))
    assert tuple(n.to_pattern() for n in alt2.nodes) == ("a", "b", "c")
    assert alt2.to_pattern() == "a|b|c"


def test_alternation_fixed_length():
    """Verify fixed length calculation for Alternation."""
    # All branches have the same fixed length
    alt_fixed = Alternation(DummyNode("cat", fixed_len=3), DummyNode("dog", fixed_len=3))
    assert alt_fixed.fixed_length() == 3

    # Branches have different lengths
    alt_diff = Alternation(DummyNode("a", fixed_len=1), DummyNode("abc", fixed_len=3))
    assert alt_diff.fixed_length() is None

    # Branches have unknown lengths (None)
    alt_none = Alternation(DummyNode("a", fixed_len=None), DummyNode("b", fixed_len=None))
    assert alt_none.fixed_length() is None