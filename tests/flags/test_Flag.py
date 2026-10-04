import re
import pytest
from simplibs.regex.flags.Flag import Flag


@pytest.mark.parametrize(
    ("member", "letter", "re_flag"),
    [
        (Flag.ASCII, "a", re.ASCII),
        (Flag.IGNORECASE, "i", re.IGNORECASE),
        (Flag.LOCALE, "L", re.LOCALE),
        (Flag.MULTILINE, "m", re.MULTILINE),
        (Flag.DOTALL, "s", re.DOTALL),
        (Flag.UNICODE, "u", re.UNICODE),
        (Flag.VERBOSE, "x", re.VERBOSE),
    ],
)
def test_flag_letter_and_re_flag(member, letter, re_flag):
    """Each member maps to its inline letter and its `re` module flag."""
    assert member.value == letter
    assert member.re_flag == re_flag


def test_flag_has_exactly_the_seven_supported_members():
    """`re.DEBUG` and `re.NOFLAG` are deliberately not members."""
    assert {f.name for f in Flag} == {
        "ASCII", "IGNORECASE", "LOCALE", "MULTILINE", "DOTALL", "UNICODE", "VERBOSE",
    }


def test_flag_letters_are_unique():
    """Two members sharing a letter would render the wrong inline group."""
    letters = [f.value for f in Flag]
    assert len(letters) == len(set(letters))


def test_every_member_has_a_distinct_re_flag():
    """The lookup table covers every member, and no two members share a bit."""
    re_flags = [f.re_flag for f in Flag]
    assert all(isinstance(rf, re.RegexFlag) for rf in re_flags)
    assert len(re_flags) == len(set(re_flags))


def test_re_flags_combine_with_or():
    """RegexPattern ORs the flags together — the result must equal the plain `re` one."""
    combined = Flag.IGNORECASE.re_flag | Flag.MULTILINE.re_flag
    assert combined == re.IGNORECASE | re.MULTILINE


def test_member_lookup_by_letter():
    assert Flag("i") is Flag.IGNORECASE


@pytest.mark.parametrize("flag", [f for f in Flag if f is not Flag.LOCALE])
def test_inline_letter_is_accepted_by_re(flag):
    """Every letter except `L` is valid in a scoped inline group on a str pattern."""
    re.compile(f"(?{flag.value}:x)")


def test_locale_letter_is_rejected_by_re_for_str_patterns():
    """Why Group and RegexPattern reject Flag.LOCALE up front."""
    with pytest.raises(re.error):
        re.compile("(?L:x)")
