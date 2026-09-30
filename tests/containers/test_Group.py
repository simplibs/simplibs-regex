"""
Tests for the Group container.
"""
import pytest
from simplibs.regex.base_class.Regex import Regex
from simplibs.regex.containers.Group import Group
from simplibs.regex.flags.Flag import Flag


class DummyNode(Regex):
    def __init__(self, pattern: str, fixed_len: int | None = None):
        self._pattern = pattern
        self._fixed_len = fixed_len

    def to_pattern(self) -> str:
        return self._pattern

    def fixed_length(self) -> int | None:
        return self._fixed_len


def test_group_validation():
    """Verify parameter validations and conflict handling in Group."""
    inner = DummyNode("a")

    # Invalid inner
    with pytest.raises(TypeError):
        Group("not-regex")  # type: ignore

    # Invalid group name
    with pytest.raises(ValueError):
        Group(inner, name="123invalid")

    # Conflicts: atomic and name
    with pytest.raises(ValueError):
        Group(inner, atomic=True, name="test")

    # Conflicts: atomic and flags
    with pytest.raises(ValueError):
        Group(inner, atomic=True, flags={Flag.IGNORECASE})

    # Conflicts: name and flags
    with pytest.raises(ValueError):
        Group(inner, name="test", flags={Flag.IGNORECASE})

    # Conflicts: name requires capturing
    with pytest.raises(ValueError):
        Group(inner, name="test", capturing=False)

    # Conflicts: flags require non-capturing
    with pytest.raises(ValueError):
        Group(inner, flags={Flag.IGNORECASE}, capturing=True)

    # Conflicts: flags_off without flags
    with pytest.raises(ValueError):
        Group(inner, flags_off={Flag.IGNORECASE}, capturing=False)


def test_group_patterns():
    """Verify pattern creation for different Group variants."""
    inner = DummyNode("abc")

    assert Group(inner).to_pattern() == "(abc)"
    assert Group(inner, capturing=False).to_pattern() == "(?:abc)"
    assert Group(inner, name="my_group").to_pattern() == "(?P<my_group>abc)"
    assert Group(inner, atomic=True).to_pattern() == "(?>abc)"
    assert Group(inner, flags={Flag.IGNORECASE, Flag.DOTALL}, capturing=False).to_pattern() == "(?is:abc)"
    assert Group(inner, flags={Flag.IGNORECASE}, flags_off={Flag.MULTILINE}, capturing=False).to_pattern() == "(?i-m:abc)"

def test_group_fixed_length():
    """Verify Group delegates fixed length correctly to inner node."""
    inner = DummyNode("abc", fixed_len=3)
    group = Group(inner)
    assert group.fixed_length() == 3