from typing import Any

import pytest
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.elements.Anchor import Anchor, AnchorKind
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.flags.Flag import Flag
from simplibs.regex.presets.anchors import (
    START,
    END,
    START_STRING,
    END_STRING,
    WORD_BOUNDARY,
    NON_WORD_BOUNDARY,
)
from simplibs.regex.testing import assert_pattern


@pytest.mark.parametrize(
    ("preset", "kind", "expected", "matches"),
    [
        (START, AnchorKind.START, "^", [""]),
        (END, AnchorKind.END, "$", [""]),
        (START_STRING, AnchorKind.START_STRING, "\\A", [""]),
        (END_STRING, AnchorKind.END_STRING, "\\Z", [""]),
        (WORD_BOUNDARY, AnchorKind.WORD_BOUNDARY, "\\b", []),
        (NON_WORD_BOUNDARY, AnchorKind.NON_WORD_BOUNDARY, "\\B", []),
    ],
    ids=["START", "END", "START_STRING", "END_STRING", "WORD_BOUNDARY", "NON_WORD_BOUNDARY"],
)
def test_anchor_preset(
    subtests: Any, preset: Anchor, kind: AnchorKind, expected: str, matches: list[str]
) -> None:
    """Test that each preset is the right Anchor and renders the right pattern."""
    assert isinstance(preset, Anchor)
    assert preset.kind is kind
    # A zero-width anchor never fully matches non-empty text.
    assert_pattern(subtests, preset, expected, matches=matches, non_matches=["a"])


def test_anchor_presets_compose(subtests: Any) -> None:
    """Test whole-string anchoring around a literal."""
    assert_pattern(
        subtests, START_STRING + Literal("ab") + END_STRING, "\\Aab\\Z",
        matches=["ab"],
        non_matches=["abc", "xab", "ab\n", ""],
    )


def test_end_matches_before_a_trailing_newline_but_end_string_does_not() -> None:
    """`$` tolerates one final newline; `\\Z` is the strict end of the text."""
    assert RegexPattern(Literal("a") + END).search("a\n") is not None
    assert RegexPattern(Literal("a") + END_STRING).search("a\n") is None


def test_start_and_end_follow_the_multiline_flag() -> None:
    """MULTILINE moves `^` to every line start; `\\A` stays at the start of the text."""
    multiline = frozenset({Flag.MULTILINE})
    assert RegexPattern(START + Literal("b")).search("a\nb") is None
    assert RegexPattern(START + Literal("b"), flags=multiline).search("a\nb") is not None
    assert RegexPattern(START_STRING + Literal("b"), flags=multiline).search("a\nb") is None
