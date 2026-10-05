import re

import pytest
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.elements.RawPattern import RawPattern
from simplibs.regex.presets.character_types import DIGIT
from simplibs.regex.presets.lookaround import LOOKBEHIND
from simplibs.regex.presets.quantifiers import ONE_OR_MORE
from simplibs.regex.testing import assert_pattern

USD_AMOUNT = LOOKBEHIND(Literal("USD")) + ONE_OR_MORE(DIGIT)


def test_passes_when_everything_holds(subtests):
    assert_pattern(subtests, DIGIT, "\\d", matches=["5"], non_matches=["a", "55"])


def test_fast_mode_needs_no_subtests_fixture():
    assert_pattern(None, DIGIT, "\\d", matches=["5"], non_matches=["a"], verbose=False)


def test_wrong_pattern_string_raises():
    with pytest.raises(AssertionError, match="Expected pattern string"):
        assert_pattern(None, DIGIT, "\\w", verbose=False)


def test_text_that_should_match_but_does_not_raises():
    with pytest.raises(AssertionError, match="to match value"):
        assert_pattern(None, DIGIT, "\\d", matches=["a"], verbose=False)


def test_text_that_should_not_match_but_does_raises():
    with pytest.raises(AssertionError, match="NOT to match value"):
        assert_pattern(None, DIGIT, "\\d", non_matches=["5"], verbose=False)


def test_failure_message_keeps_a_real_control_character_on_one_line():
    """`RawPattern` is verbatim, so its pattern really contains a newline; the message must show it with repr."""
    with pytest.raises(AssertionError) as error:
        assert_pattern(None, RawPattern("a\nb"), "x", verbose=False)
    assert repr("a\nb") in str(error.value)
    assert "\n" not in str(error.value)


def test_failure_message_shows_a_literal_control_character_as_a_readable_escape():
    """`Literal("\n")` renders the two characters backslash, n — never a raw newline."""
    with pytest.raises(AssertionError) as error:
        assert_pattern(None, Literal("\n"), "x", verbose=False)
    assert repr("\\n") in str(error.value)
    assert "\n" not in str(error.value)


def test_finds_checks_a_search_in_context(subtests):
    assert_pattern(
        subtests, USD_AMOUNT, "(?<=USD)\\d+",
        finds={"USD42": "42", "total USD7 paid": "7", "EUR42": None},
    )


def test_finds_catches_a_different_result():
    with pytest.raises(AssertionError, match="to find"):
        assert_pattern(None, USD_AMOUNT, "(?<=USD)\\d+", finds={"USD42": "4"}, verbose=False)


def test_finds_catches_a_search_that_should_find_nothing():
    with pytest.raises(AssertionError, match="to find"):
        assert_pattern(None, USD_AMOUNT, "(?<=USD)\\d+", finds={"USD42": None}, verbose=False)


def test_fullmatch_alone_cannot_check_a_lookbehind():
    """The reason `finds` exists."""
    with pytest.raises(AssertionError):
        assert_pattern(None, USD_AMOUNT, "(?<=USD)\\d+", matches=["42"], verbose=False)


@pytest.mark.parametrize("bad", [["USD42"], "USD42", ("USD42", "42")])
def test_finds_must_be_a_mapping(bad):
    with pytest.raises(TypeError, match="finds"):
        assert_pattern(None, USD_AMOUNT, "(?<=USD)\\d+", finds=bad, verbose=False)


@pytest.mark.parametrize("argument", ["matches", "non_matches"])
def test_a_bare_string_is_rejected(argument):
    with pytest.raises(TypeError, match=argument):
        assert_pattern(None, DIGIT, "\\d", verbose=False, **{argument: "abc"})


def test_pattern_obj_must_be_a_regex():
    with pytest.raises(TypeError, match="Regex instance"):
        assert_pattern(None, "\\d", "\\d", verbose=False)
