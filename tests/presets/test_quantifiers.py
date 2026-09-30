from simplibs.regex.elements.Literal import Literal
from simplibs.regex.containers.Repeat import RepeatMode
from simplibs.regex.presets.quantifiers import (
    OPTIONAL,
    ZERO_OR_MORE,
    ONE_OR_MORE,
    EXACTLY,
    AT_LEAST,
    BETWEEN,
)

def test_quantifier_presets():
    """Verify that quantifier presets produce the correct patterns."""
    inner = Literal("a")

    assert OPTIONAL(inner).to_pattern() == "a?"
    assert ZERO_OR_MORE(inner).to_pattern() == "a*"
    assert ONE_OR_MORE(inner).to_pattern() == "a+"
    assert EXACTLY(inner, 3).to_pattern() == "a{3}"
    assert AT_LEAST(inner, 2).to_pattern() == "a{2,}"
    assert BETWEEN(inner, 2, 4).to_pattern() == "a{2,4}"

    # Test with non-greedy mode
    assert ZERO_OR_MORE(inner, mode=RepeatMode.LAZY).to_pattern() == "a*?"