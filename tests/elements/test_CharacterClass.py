import warnings
from typing import Any

import pytest
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.elements.Anchor import Anchor, AnchorKind
from simplibs.regex.elements.AnyCharacter import AnyCharacter
from simplibs.regex.elements.CharacterClass import CharacterClass
from simplibs.regex.elements.CharacterRange import CharacterRange
from simplibs.regex.elements.CharacterType import CharacterType, CharacterTypeKind
from simplibs.regex.elements.CharacterCode import CharacterCode, CharacterCodeKind
from simplibs.regex.elements.GroupReference import GroupReference
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.elements.RawPattern import RawPattern
from simplibs.regex.testing import assert_pattern


def test_character_class_literals(subtests: Any) -> None:
    """Test a class built from single-character literals."""
    node = CharacterClass(Literal("a"), Literal("b"), Literal("c"))
    assert_pattern(
        subtests, node, "[abc]",
        matches=["a", "b", "c"],
        non_matches=["d", "", "ab"],
    )


def test_character_class_negated(subtests: Any) -> None:
    """Test that negate=True produces `[^...]`."""
    node = CharacterClass(CharacterRange("a", "z"), negate=True)
    assert_pattern(
        subtests, node, "[^a-z]",
        matches=["A", "0", " "],
        non_matches=["a", "z", "ab", ""],
    )


def test_character_class_character_types(subtests: Any) -> None:
    """Test that character types keep their meaning inside a class."""
    node = CharacterClass(
        CharacterType(CharacterTypeKind.DIGIT),
        CharacterType(CharacterTypeKind.WHITESPACE),
    )
    assert_pattern(
        subtests, node, "[\\d\\s]",
        matches=["5", " ", "\t"],
        non_matches=["a", "55"],
    )


def test_character_class_mixed_items(subtests: Any) -> None:
    """Test a class mixing a character code, a range and a literal."""
    node = CharacterClass(
        CharacterCode(CharacterCodeKind.HEX, 0x41),
        CharacterRange("a", "c"),
    )
    assert_pattern(
        subtests, node, "[\\x41a-c]",
        matches=["A", "a", "b", "c"],
        non_matches=["B", "d"],
    )


def test_character_class_escapes_special_characters(subtests: Any) -> None:
    """Test that `] ^ - \\` are escaped inside a class."""
    node = CharacterClass(Literal("]"), Literal("^"), Literal("-"), Literal("\\"))
    assert_pattern(
        subtests, node, "[\\]\\^\\-\\\\]",
        matches=["]", "^", "-", "\\"],
        non_matches=["a", ""],
    )


@pytest.mark.parametrize("negate", [False, True])
def test_character_class_fixed_length(negate: bool) -> None:
    """Test that a class always matches exactly one character."""
    assert CharacterClass(Literal("a"), negate=negate).fixed_length() == 1


def test_character_class_keeps_items_and_negate() -> None:
    """Test that items are stored as a tuple together with negate."""
    a, b = Literal("a"), Literal("b")
    node = CharacterClass(a, b, negate=True)
    assert node.items == (a, b)
    assert node.negate is True


@pytest.mark.parametrize(
    "bad_item",
    [
        pytest.param(Anchor(AnchorKind.START), id="anchor"),
        pytest.param(AnyCharacter(), id="any-character"),
        pytest.param(GroupReference(1), id="group-reference"),
        pytest.param(RawPattern("a"), id="raw-pattern"),
        pytest.param(CharacterClass(Literal("a")), id="nested-class"),
        pytest.param("a", id="plain-str"),
        pytest.param(None, id="none"),
    ],
)
def test_character_class_rejects_unusable_items(bad_item: object) -> None:
    """Test that items not opted into class usage are rejected."""
    with pytest.raises(TypeError):
        CharacterClass(bad_item)  # type: ignore[arg-type]


def test_character_class_rejects_multi_character_literal() -> None:
    """Test that `[ab]` can never silently mean the substring "ab"."""
    with pytest.raises(ValueError):
        CharacterClass(Literal("ab"))


def test_character_class_rejects_empty() -> None:
    """Test that at least one item is required."""
    with pytest.raises(ValueError):
        CharacterClass()


@pytest.mark.parametrize(
    "items",
    [
        pytest.param((Literal("["), Literal("a")), id="leading-bracket"),
        pytest.param((Literal("a"), Literal("&"), Literal("&"), Literal("b")), id="double-ampersand"),
        pytest.param((Literal("a"), Literal("-"), Literal("-"), Literal("b")), id="double-dash"),
    ],
)
def test_character_class_compiles_without_future_warnings(items: tuple) -> None:
    """Test that no `FutureWarning` ("possible nested set / intersection / difference") is raised."""
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        RegexPattern(CharacterClass(*items))