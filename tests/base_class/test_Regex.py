"""
Tests for the abstract base class Regex.
"""
import pytest
from abc import ABC
from simplibs.regex.base_class.Regex import Regex
from simplibs.regex.base_class.enums.Precedence import Precedence


class DummyRegex(Regex):
    """Concrete subclass of Regex for testing base class functionality."""
    def __init__(self, pattern: str, precedence: Precedence = Precedence.ATOM, fixed_len: int | None = None, wrap_repeat: bool = False, usable_char_class: bool = False):
        self._pattern = pattern
        self._precedence = precedence
        self._fixed_len = fixed_len
        self._wrap_repeat = wrap_repeat
        self._usable_in_char_class = usable_char_class

    def to_pattern(self) -> str:
        return self._pattern

    def fixed_length(self) -> int | None:
        return self._fixed_len

    def needs_wrap_for_repeat(self) -> bool:
        return self._wrap_repeat


def test_regex_is_abstract():
    """Verify that Regex cannot be instantiated directly."""
    with pytest.raises(TypeError):
        Regex()  # type: ignore


def test_default_attributes():
    """Verify default class attributes on Regex subclasses."""
    node = DummyRegex("test")
    assert node._precedence == Precedence.ATOM
    assert node._usable_in_char_class is False
    assert node.fixed_length() is None
    assert node.needs_wrap_for_repeat() is False


def test_render_no_wrap():
    """Verify render does not wrap when child precedence is greater than or equal to parent precedence."""
    node = DummyRegex("abc", precedence=Precedence.ATOM)
    # Parent has SEQUENCE precedence (1), child has ATOM (3) -> 3 < 1 is False -> no wrap
    assert node.render(Precedence.SEQUENCE) == "abc"


def test_render_with_wrap():
    """Verify render wraps in (?:...) when child precedence is strictly lower than parent precedence."""
    node = DummyRegex("a|b", precedence=Precedence.ALTERNATION)
    # Parent has SEQUENCE precedence (1), child has ALTERNATION (0) -> 0 < 1 is True -> wrap
    assert node.render(Precedence.SEQUENCE) == "(?:a|b)"


def test_to_char_class_fragment_default():
    """Verify default to_char_class_fragment delegates to to_pattern."""
    node = DummyRegex("abc")
    assert node.to_char_class_fragment() == "abc"


def test_compile():
    """Verify compile returns a compiled re.Pattern object."""
    node = DummyRegex(r"\d+")
    compiled = node.compile()
    assert compiled.pattern == r"\d+"
    assert compiled.match("123") is not None


def test_operators_addition():
    """Verify __add__ and __radd__ create a Sequence."""
    node1 = DummyRegex("a")
    node2 = DummyRegex("b")

    seq1 = node1 + node2
    from simplibs.regex.containers.Sequence import Sequence
    assert isinstance(seq1, Sequence)

    # Test __radd__ directly with another Regex object
    seq2 = node1.__radd__(node2)
    assert isinstance(seq2, Sequence)
    assert seq2.to_pattern() == "ba"


def test_operators_alternation():
    """Verify __or__ and __ror__ create an Alternation."""
    node1 = DummyRegex("a")
    node2 = DummyRegex("b")

    alt1 = node1 | node2
    from simplibs.regex.containers.Alternation import Alternation
    assert isinstance(alt1, Alternation)

    alt2 = DummyRegex("a") | node2
    assert isinstance(alt2, Alternation)