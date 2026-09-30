from simplibs.regex.elements.Literal import Literal
from simplibs.regex.presets.lookaround import (
    LOOKAHEAD,
    NEGATIVE_LOOKAHEAD,
    LOOKBEHIND,
    NEGATIVE_LOOKBEHIND,
)

def test_lookaround_presets():
    """Verify that lookaround presets produce the correct patterns."""
    # Lookbehind requires a fixed-length inner node
    inner_fixed = Literal("abc")

    assert LOOKAHEAD(inner_fixed).to_pattern() == "(?=abc)"
    assert NEGATIVE_LOOKAHEAD(inner_fixed).to_pattern() == "(?!abc)"
    assert LOOKBEHIND(inner_fixed).to_pattern() == "(?<=abc)"
    assert NEGATIVE_LOOKBEHIND(inner_fixed).to_pattern() == "(?<!abc)"