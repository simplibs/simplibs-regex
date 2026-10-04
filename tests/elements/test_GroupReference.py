import pytest
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.containers.Group import Group
from simplibs.regex.containers.Sequence import Sequence
from simplibs.regex.elements.CharacterClass import CharacterClass
from simplibs.regex.elements.GroupReference import GroupReference
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.presets.groups import NAMED_GROUP


def test_group_reference() -> None:
    """Verify GroupReference patterns and fixed length (None)."""
    assert GroupReference(1).to_pattern() == "\\1"
    assert GroupReference("year").to_pattern() == "(?P=year)"
    assert GroupReference(1).fixed_length() is None


@pytest.mark.parametrize("number", [1, 99])
def test_group_reference_valid_numbers(number: int) -> None:
    """Test the inclusive bounds of the numeric range."""
    assert GroupReference(number).to_pattern() == f"\\{number}"


@pytest.mark.parametrize("number", [0, -1, 100])
def test_group_reference_number_out_of_range(number: int) -> None:
    """Test that numbers outside 1-99 are rejected (100+ would be an octal escape)."""
    with pytest.raises(ValueError):
        GroupReference(number)


@pytest.mark.parametrize("bad", [True, False, 1.5, None, b"a"])
def test_group_reference_invalid_type(bad: object) -> None:
    """Test that bool and other non-int/str values are rejected."""
    with pytest.raises(TypeError):
        GroupReference(bad)  # type: ignore[arg-type]


@pytest.mark.parametrize("bad", ["", "1abc", "a-b", "a b"])
def test_group_reference_invalid_name(bad: str) -> None:
    """Test that names which are not valid identifiers are rejected."""
    with pytest.raises(ValueError):
        GroupReference(bad)


def test_group_reference_not_usable_in_char_class() -> None:
    """Test that `\\1` can never silently become an octal escape in a class."""
    assert GroupReference._usable_in_char_class is False
    with pytest.raises(TypeError):
        CharacterClass(GroupReference(1))


def test_group_reference_wrapped_when_embedded() -> None:
    """Test that a numeric reference cannot merge with a following digit."""
    assert Sequence(GroupReference(1), Literal("0")).to_pattern() == "(?:\\1)0"
    assert Sequence(GroupReference("x"), Literal("0")).to_pattern() == "(?P=x)0"


def test_group_reference_numeric_end_to_end() -> None:
    """Test that the wrapped form really means 'group 1, then the digit 0'."""
    pattern = RegexPattern(Group(Literal("a")) + GroupReference(1) + Literal("0"))
    assert pattern.fullmatch("aa0") is not None


def test_group_reference_named_end_to_end() -> None:
    """Test a named group followed by its reference."""
    pattern = RegexPattern(NAMED_GROUP(Literal("a"), "x") + GroupReference("x"))
    assert pattern.fullmatch("aa") is not None
    assert pattern.fullmatch("ab") is None