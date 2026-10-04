import pytest
from simplibs.regex.base_class import Regex
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.containers.Repeat import Repeat
from simplibs.regex.elements.AnyCharacter import AnyCharacter
from simplibs.regex.elements.CharacterClass import CharacterClass
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.flags.Flag import Flag


def test_any_character_is_regex() -> None:
    """Test that AnyCharacter is a Regex node."""
    assert isinstance(AnyCharacter(), Regex)


def test_any_character_pattern() -> None:
    """Test that the pattern is always a single dot."""
    assert AnyCharacter().to_pattern() == "."


def test_any_character_fixed_length() -> None:
    """Test that AnyCharacter always has a fixed length of one."""
    assert AnyCharacter().fixed_length() == 1


def test_any_character_not_usable_in_char_class() -> None:
    """Test that `[.]` (a literal dot) can never be built by accident."""
    assert AnyCharacter._usable_in_char_class is False
    with pytest.raises(TypeError):
        CharacterClass(AnyCharacter())


def test_any_character_composition() -> None:
    """Test rendering inside a Sequence and under a Repeat."""
    assert (Literal("a") + AnyCharacter() + Literal("c")).to_pattern() == "a.c"
    assert Repeat(AnyCharacter(), min=0, max=None).to_pattern() == ".*"


def test_any_character_matching() -> None:
    """Test that it matches one character, but not a newline by default."""
    pattern = RegexPattern(AnyCharacter())

    assert pattern.fullmatch("a") is not None
    assert pattern.fullmatch("5") is not None
    assert pattern.fullmatch(" ") is not None
    assert pattern.fullmatch("\n") is None
    assert pattern.fullmatch("ab") is None
    assert pattern.fullmatch("") is None


def test_any_character_dotall() -> None:
    """Test that the DOTALL flag makes it match a newline too."""
    pattern = RegexPattern(AnyCharacter(), flags=frozenset({Flag.DOTALL}))

    assert pattern.fullmatch("\n") is not None