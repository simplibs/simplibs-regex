import pytest
from simplibs.exception import ValidationError
from simplibs.regex.compiler.RegexPattern import RegexPattern
from simplibs.regex.containers.Group import Group
from simplibs.regex.elements.Literal import Literal
from simplibs.regex.flags.Flag import Flag
from simplibs.regex.presets.any_character import ANY
from simplibs.regex.presets.anchors import START
from simplibs.regex.presets.character_types import DIGIT
from simplibs.regex.presets.groups import NAMED_GROUP
from simplibs.regex.presets.quantifiers import ONE_OR_MORE


def _duplicate_group_names():
    """A tree no single node can reject: only `re.compile` sees both names."""
    return Group(DIGIT, name="a") + Group(DIGIT, name="a")


def test_regex_pattern_execution():
    """Core operations delegate correctly to the compiled pattern."""
    pattern = RegexPattern(Literal("test"))

    assert pattern.pattern_string == "test"

    assert pattern.search("this is a test string") is not None
    assert pattern.search("no match here") is None

    assert pattern.match("test string") is not None
    assert pattern.match("string test") is None

    assert pattern.fullmatch("test") is not None
    assert pattern.fullmatch("test string") is None

    assert RegexPattern(Literal("a")).findall("banana") == ["a", "a", "a"]
    assert pattern.sub("passed", "this is a test") == "this is a passed"
    assert RegexPattern(Literal("-")).split("a-b-c") == ["a", "b", "c"]


def test_pos_and_endpos_are_passed_through():
    a = RegexPattern(Literal("a"))
    assert a.search("baa", 1).span() == (1, 2)
    assert a.search("baa", 0, 1) is None
    assert a.match("baa", 1) is not None
    assert RegexPattern(Literal("ab")).fullmatch("abc", 0, 2) is not None


def test_sub_subn_and_split_respect_counts():
    a = RegexPattern(Literal("a"))
    assert a.subn("x", "banana") == ("bxnxnx", 3)
    assert a.subn("x", "banana", 1) == ("bxnana", 1)
    assert a.sub("x", "banana", 2) == "bxnxna"
    assert RegexPattern(Literal("-")).split("a-b-c", 1) == ["a", "b-c"]


def test_findall_returns_group_contents_and_finditer_yields_matches():
    numbers = RegexPattern(NAMED_GROUP(ONE_OR_MORE(DIGIT), "n"))
    assert numbers.findall("a1 b22") == ["1", "22"]
    assert [m.group("n") for m in numbers.finditer("a1 b22")] == ["1", "22"]


# ----------------------------------------------------------------------
# Flags
# ----------------------------------------------------------------------
def test_regex_pattern_with_flags():
    pattern = RegexPattern(Literal("TEST"), flags=frozenset({Flag.IGNORECASE}))
    assert pattern.search("hello test world") is not None
    assert RegexPattern(Literal("TEST")).search("hello test world") is None


def test_top_level_flags_are_not_rendered_into_the_pattern_string():
    pattern = RegexPattern(Literal("a"), flags=frozenset({Flag.IGNORECASE}))
    assert pattern.pattern_string == "a"


def test_multiline_and_dotall_flags_change_matching():
    anchored = START + Literal("b")
    assert RegexPattern(anchored).search("a\nb") is None
    assert RegexPattern(anchored, flags=frozenset({Flag.MULTILINE})).search("a\nb") is not None

    dotted = Literal("a") + ANY + Literal("b")
    assert RegexPattern(dotted).search("a\nb") is None
    assert RegexPattern(dotted, flags=frozenset({Flag.DOTALL})).search("a\nb") is not None


@pytest.mark.parametrize("flags", [{Flag.IGNORECASE}, frozenset({Flag.IGNORECASE})])
def test_flags_accept_set_and_frozenset(flags):
    """Needs the shared `set | frozenset` flag type (itinerary part 1)."""
    assert RegexPattern(Literal("a"), flags=flags).search("A") is not None


def test_locale_flag_is_rejected():
    with pytest.raises(ValidationError):
        RegexPattern(Literal("a"), flags=frozenset({Flag.LOCALE}))


def test_ascii_together_with_unicode_is_rejected():
    """`re.compile` raises a bare ValueError for this; it must come out structured."""
    with pytest.raises(ValidationError):
        RegexPattern(Literal("a"), flags=frozenset({Flag.ASCII, Flag.UNICODE}))


# ----------------------------------------------------------------------
# Eager vs lazy compilation
# ----------------------------------------------------------------------
def test_eager_compiles_at_construction():
    assert RegexPattern(Literal("a"))._compiled is not None


def test_lazy_compiles_on_first_use_and_caches():
    pattern = RegexPattern(Literal("a"), lazy=True)
    assert pattern._compiled is None

    assert pattern.search("a") is not None
    assert pattern._compiled is not None
    assert pattern.compiled is pattern.compiled


def test_invalid_tree_fails_at_construction_when_eager():
    with pytest.raises(ValidationError):
        RegexPattern(_duplicate_group_names())


def test_invalid_tree_fails_on_first_use_when_lazy():
    pattern = RegexPattern(_duplicate_group_names(), lazy=True)   # no error yet
    with pytest.raises(ValidationError):
        pattern.search("12")
    with pytest.raises(ValidationError):                          # not cached as "compiled"
        pattern.search("12")


# ----------------------------------------------------------------------
# Input validation and repr
# ----------------------------------------------------------------------
def test_node_must_be_a_regex():
    with pytest.raises(ValidationError):
        RegexPattern("abc")


def test_repr_shows_description_only_when_given():
    assert "description" not in repr(RegexPattern(Literal("a")))
    assert "description='year'" in repr(RegexPattern(Literal("a"), description="year"))
