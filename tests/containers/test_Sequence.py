"""
Tests for the Sequence container.
"""
import pytest
from simplibs.regex.base_class.Regex import Regex
from simplibs.regex.containers.Sequence import Sequence


class DummyNode(Regex):
    def __init__(self, pattern: str, fixed_len: int | None = None):
        self._pattern = pattern
        self._fixed_len = fixed_len

    def to_pattern(self) -> str:
        return self._pattern

    def fixed_length(self) -> int | None:
        return self._fixed_len


def test_sequence_requires_nodes():
    """Verify that empty sequence raises an error."""
    with pytest.raises(ValueError):
        Sequence()


def test_sequence_invalid_node_type():
    """Verify that non-Regex nodes raise a TypeError."""
    with pytest.raises(TypeError):
        Sequence(DummyNode("a"), "not-a-regex")  # type: ignore


def test_sequence_flattening():
    """Verify that nested Sequences are flattened."""
    seq1 = Sequence(DummyNode("a"), DummyNode("b"))
    seq2 = Sequence(seq1, DummyNode("c"))
    assert tuple(n.to_pattern() for n in seq2.nodes) == ("a", "b", "c")
    assert seq2.to_pattern() == "abc"


def test_sequence_fixed_length():
    """Verify fixed length calculation for Sequence sums."""
    seq_fixed = Sequence(DummyNode("a", fixed_len=2), DummyNode("b", fixed_len=3))
    assert seq_fixed.fixed_length() == 5

    seq_mixed = Sequence(DummyNode("a", fixed_len=2), DummyNode("b", fixed_len=None))
    assert seq_mixed.fixed_length() is None