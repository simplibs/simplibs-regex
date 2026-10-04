"""
Tests for the Precedence enum.
"""
from simplibs.regex.base_class.enums.Precedence import Precedence


def test_precedence_ordering():
    """Verify that precedence levels follow the correct numerical order (loosest to tightest)."""
    assert Precedence.ALTERNATION < Precedence.SEQUENCE
    assert Precedence.SEQUENCE < Precedence.REPEAT
    assert Precedence.REPEAT < Precedence.ATOM

    assert Precedence.ALTERNATION.value == 0
    assert Precedence.SEQUENCE.value == 1
    assert Precedence.REPEAT.value == 2
    assert Precedence.ATOM.value == 3