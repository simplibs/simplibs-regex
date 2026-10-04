"""
Tests for the Repeat container.
"""
import pytest
from simplibs.regex.base_class.Regex import Regex, Precedence
from simplibs.regex.containers.Repeat import Repeat, RepeatMode
from simplibs.regex.containers.Group import Group
from simplibs.regex.containers.Lookaround import Lookaround, LookaroundDirection
from simplibs.regex.elements.Anchor import Anchor, AnchorKind
from simplibs.regex.presets.character_types.DIGIT import DIGIT

class DummyNode(Regex):
    def __init__(self, pattern: str, precedence: Precedence = Precedence.ATOM, fixed_len: int | None = None, wrap_repeat: bool = False):
        self._pattern = pattern
        self._precedence = precedence
        self._fixed_len = fixed_len
        self._wrap_repeat = wrap_repeat

    def to_pattern(self) -> str:
        return self._pattern

    def fixed_length(self) -> int | None:
        return self._fixed_len

    def needs_wrap_for_repeat(self) -> bool:
        return self._wrap_repeat


def test_repeat_validation():
    """Verify parameter validation for Repeat."""
    inner = DummyNode("a")

    # Invalid inner
    with pytest.raises(TypeError):
        Repeat("not-regex", min=1)  # type: ignore

    # Negative min
    with pytest.raises(ValueError):
        Repeat(inner, min=-1)

    # Max less than min
    with pytest.raises(ValueError):
        Repeat(inner, min=3, max=2)

    # Invalid mode
    with pytest.raises(TypeError):
        Repeat(inner, min=0, mode="greedy")  # type: ignore


def test_repeat_quantifier_patterns():
    """Verify shorthand quantifiers and modes output."""
    inner = DummyNode("a")

    # Shorthands + Modes
    assert Repeat(inner, min=0, max=None, mode=RepeatMode.GREEDY).to_pattern() == "a*"
    assert Repeat(inner, min=1, max=None, mode=RepeatMode.LAZY).to_pattern() == "a+?"
    assert Repeat(inner, min=0, max=1, mode=RepeatMode.POSSESSIVE).to_pattern() == "a?+"
    assert Repeat(inner, min=5, max=5, mode=RepeatMode.GREEDY).to_pattern() == "a{5}"
    assert Repeat(inner, min=3, max=None, mode=RepeatMode.GREEDY).to_pattern() == "a{3,}"
    assert Repeat(inner, min=2, max=4, mode=RepeatMode.GREEDY).to_pattern() == "a{2,4}"


def test_repeat_wrapping_for_multi_char():
    """Verify that multi-character atomic nodes get wrapped with (?:...) before repeating."""
    inner = DummyNode("ab", wrap_repeat=True)
    assert Repeat(inner, min=3, max=3).to_pattern() == "(?:ab){3}"


def test_repeat_fixed_length():
    """Verify fixed length introspection for Repeat."""
    inner_fixed = DummyNode("a", fixed_len=3)
    inner_var = DummyNode("a", fixed_len=None)

    # min=0, max=0 is always 0 length regardless of inner
    assert Repeat(inner_var, min=0, max=0).fixed_length() == 0

    # min != max returns None
    assert Repeat(inner_fixed, min=1, max=2).fixed_length() is None

    # min == max with fixed inner length
    assert Repeat(inner_fixed, min=4, max=4).fixed_length() == 12

    # min == max with variable inner length returns None
    assert Repeat(inner_var, min=3, max=3).fixed_length() is None


@pytest.mark.parametrize("kind", [AnchorKind.START, AnchorKind.WORD_BOUNDARY, AnchorKind.END_STRING])
def test_repeat_rejects_a_bare_anchor(kind):
   with pytest.raises(ValueError):
       Repeat(Anchor(kind), min=0)


def test_repeat_accepts_a_wrapped_anchor_and_a_lookaround():
   assert Repeat(Group(Anchor(AnchorKind.START), capturing=False)).to_pattern() == "(?:^)*"
   assert Repeat(Lookaround(DIGIT, direction=LookaroundDirection.AHEAD)).to_pattern() == "(?=\\d)*"