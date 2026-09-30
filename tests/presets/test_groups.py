from simplibs.regex.elements.Literal import Literal
from simplibs.regex.presets.groups import (
    NAMED_GROUP,
    NON_CAPTURING,
    ATOMIC_GROUP,
)

def test_group_presets():
    """Verify that group helper presets produce the correct patterns."""
    inner = Literal("abc")

    assert NAMED_GROUP(inner, "id").to_pattern() == "(?P<id>abc)"
    assert NON_CAPTURING(inner).to_pattern() == "(?:abc)"
    assert ATOMIC_GROUP(inner).to_pattern() == "(?>abc)"