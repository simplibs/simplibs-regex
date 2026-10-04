import pytest
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.flags.Flag import Flag
from simplibs.regex.presets.any_character import ANY
from simplibs.regex.presets.character_types import DIGIT
from simplibs.regex.presets.groups import (
    ATOMIC_GROUP, NAMED_GROUP, NON_CAPTURING, WITH_FLAGS, CASE_INSENSITIVE, VERBOSE_GROUP,
)
from simplibs.regex.presets.quantifiers import ONE_OR_MORE
from simplibs.regex.testing import assert_pattern


CASES = [
    (ATOMIC_GROUP(DIGIT), '(?>\\d)', ['5'], ['a', '55'], frozenset()),
    (NAMED_GROUP(DIGIT, "code"), '(?P<code>\\d)', ['5'], ['a'], frozenset()),
    (NON_CAPTURING(Literal("ab")), '(?:ab)', ['ab'], ['a', 'abab'], frozenset()),
    (WITH_FLAGS(DIGIT, Flag.MULTILINE, Flag.DOTALL), '(?ms:\\d)', ['5'], ['a'], frozenset()),
    (WITH_FLAGS(ANY, Flag.DOTALL), '(?s:.)', ['\n', 'a'], ['ab'], frozenset()),
    (CASE_INSENSITIVE(Literal("ab")), '(?i:ab)', ['ab', 'AB', 'aB'], ['a', 'abc'], frozenset()),
    (VERBOSE_GROUP(Literal("a b")), '(?x:a\\ b)', ['a b'], ['ab', 'a  b'], frozenset()),
    (Literal("a") + CASE_INSENSITIVE(Literal("b")), 'a(?i:b)', ['ab', 'aB'], ['AB', 'a'], frozenset()),
]


@pytest.mark.parametrize(("node", "expected", "matches", "non_matches", "flags"), CASES)
def test_groups_presets(subtests, node, expected, matches, non_matches, flags) -> None:
    """Each preset renders the documented pattern and matches / rejects the documented texts."""
    assert_pattern(
        subtests, node, expected,
        matches=matches, non_matches=non_matches, flags=flags,
    )


def test_named_group_captures_under_its_name():
    assert RegexPattern(Literal("a") + NAMED_GROUP(DIGIT, "code")).search("a5").group("code") == "5"


def test_non_capturing_group_adds_no_capture():
    assert RegexPattern(NON_CAPTURING(Literal("ab"))).compiled.groups == 0


def test_atomic_group_does_not_backtrack():
    """`(?>a+)a` can never match "aaa": the group keeps every "a"."""
    atomic = ATOMIC_GROUP(ONE_OR_MORE(Literal("a"))) + Literal("a")
    plain = ONE_OR_MORE(Literal("a")) + Literal("a")
    assert RegexPattern(atomic).fullmatch("aaa") is None
    assert RegexPattern(plain).fullmatch("aaa") is not None


def test_flags_apply_only_inside_the_group():
    """`(?i:b)` is case-insensitive, the literal `a` before it stays case-sensitive."""
    pattern = RegexPattern(Literal("a") + CASE_INSENSITIVE(Literal("b")))
    assert pattern.fullmatch("aB") is not None
    assert pattern.fullmatch("AB") is None


def test_flag_groups_are_non_capturing():
    for node in (WITH_FLAGS(DIGIT, Flag.DOTALL), CASE_INSENSITIVE(DIGIT), VERBOSE_GROUP(DIGIT)):
        assert RegexPattern(node).compiled.groups == 0


def test_with_flags_orders_letters_alphabetically():
    """Flags are a set: the rendered letters do not depend on the call order."""
    assert WITH_FLAGS(DIGIT, Flag.DOTALL, Flag.MULTILINE).to_pattern() == WITH_FLAGS(DIGIT, Flag.MULTILINE, Flag.DOTALL).to_pattern()


def test_factories_configure_the_group() -> None:
    """Each factory sets exactly the Group options it is named after."""
    assert NAMED_GROUP(DIGIT, "code").name == "code"
    assert ATOMIC_GROUP(DIGIT).atomic is True
    assert NON_CAPTURING(DIGIT).capturing is False
    assert CASE_INSENSITIVE(DIGIT).flags == frozenset({Flag.IGNORECASE})
    assert VERBOSE_GROUP(DIGIT).flags == frozenset({Flag.VERBOSE})
    assert WITH_FLAGS(DIGIT, Flag.DOTALL, Flag.MULTILINE).flags == frozenset({Flag.DOTALL, Flag.MULTILINE})
