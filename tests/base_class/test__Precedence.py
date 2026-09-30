"""
Tests for the _Precedence enum.
"""
from simplibs.regex.base_class._Precedence import _Precedence


def test_precedence_ordering():
    """Verify that precedence levels follow the correct numerical order (loosest to tightest)."""
    assert _Precedence.ALTERNATION < _Precedence.SEQUENCE
    assert _Precedence.SEQUENCE < _Precedence.REPEAT
    assert _Precedence.REPEAT < _Precedence.ATOM

    assert _Precedence.ALTERNATION.value == 0
    assert _Precedence.SEQUENCE.value == 1
    assert _Precedence.REPEAT.value == 2
    assert _Precedence.ATOM.value == 3