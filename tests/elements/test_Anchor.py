import sys
from typing import Any

import pytest
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.elements.Anchor import Anchor, AnchorKind
from simplibs.regex.elements.CharacterClass import CharacterClass
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.flags.Flag import Flag
from simplibs.regex.testing import assert_pattern

_PORTABLE_KINDS = [kind for kind in AnchorKind if kind.name != "END_STRING_PY314"]


# Anchors are zero-width: `fullmatch` cannot say anything useful about them
# with non-empty text, so the pattern string is checked with assert_pattern
# and the behaviour is checked through RegexPattern.search below.
@pytest.mark.parametrize(
    ("kind", "expected"),
    [
        (AnchorKind.START, "^"),
        (AnchorKind.END, "$"),
        (AnchorKind.START_STRING, "\\A"),
        (AnchorKind.END_STRING, "\\Z"),
        (AnchorKind.WORD_BOUNDARY, "\\b"),
        (AnchorKind.NON_WORD_BOUNDARY, "\\B"),
    ],
)
def test_anchor_pattern(subtests: Any, kind: AnchorKind, expected: str) -> None:
    """Test the pattern string of every portable Anchor kind."""
    assert_pattern(subtests, Anchor(kind), expected)


@pytest.mark.parametrize("kind", _PORTABLE_KINDS)
def test_anchor_fixed_length_is_zero(kind: AnchorKind) -> None:
    """Test that every anchor is zero-width."""
    assert Anchor(kind).fixed_length() == 0


def test_anchor_stores_kind() -> None:
    """Test that the kind is kept on the instance."""
    assert Anchor(AnchorKind.START).kind is AnchorKind.START


def test_anchor_invalid_kind() -> None:
    """Test that anything other than an AnchorKind is rejected."""
    with pytest.raises(TypeError):
        Anchor("^")  # type: ignore[arg-type]


def test_anchor_not_usable_in_char_class() -> None:
    """Test that an anchor can never be an item of a CharacterClass."""
    assert Anchor._usable_in_char_class is False
    with pytest.raises(TypeError):
        CharacterClass(Anchor(AnchorKind.START))


def test_start_is_line_start_only_with_multiline() -> None:
    """Test that `^` follows MULTILINE while `\\A` never does."""
    start = Anchor(AnchorKind.START) + Literal("b")
    start_string = Anchor(AnchorKind.START_STRING) + Literal("b")
    multiline = frozenset({Flag.MULTILINE})

    assert RegexPattern(start).search("a\nb") is None
    assert RegexPattern(start, flags=multiline).search("a\nb") is not None
    assert RegexPattern(start_string, flags=multiline).search("a\nb") is None


def test_end_differs_from_end_string_before_trailing_newline() -> None:
    """Test that `$` accepts a trailing newline and `\\Z` does not."""
    dollar = RegexPattern(Literal("a") + Anchor(AnchorKind.END))
    end_string = RegexPattern(Literal("a") + Anchor(AnchorKind.END_STRING))

    assert dollar.search("a\n") is not None
    assert end_string.search("a\n") is None
    assert end_string.search("a") is not None


def test_word_boundaries() -> None:
    """Test `\\b` and `\\B` against words inside longer text."""
    boundary = Anchor(AnchorKind.WORD_BOUNDARY)
    non_boundary = Anchor(AnchorKind.NON_WORD_BOUNDARY)

    whole_word = RegexPattern(boundary + Literal("cat") + boundary)
    assert whole_word.search("a cat!") is not None
    assert whole_word.search("concat") is None

    inside_word = RegexPattern(non_boundary + Literal("cat"))
    assert inside_word.search("concat") is not None
    assert inside_word.search(" cat") is None


@pytest.mark.skipif(sys.version_info < (3, 14), reason="`\\z` needs Python 3.14+")
def test_anchor_end_string_py314(subtests: Any) -> None:
    """Test that `\\z` renders on Python 3.14+."""
    assert_pattern(subtests, Anchor(AnchorKind.END_STRING_PY314), "\\z")


@pytest.mark.skipif(sys.version_info >= (3, 14), reason="`\\z` is valid on 3.14+")
def test_anchor_end_string_py314_rejected_on_older_python() -> None:
    """Test that `\\z` fails at construction, not later in re.compile."""
    with pytest.raises(ValueError):
        Anchor(AnchorKind.END_STRING_PY314)