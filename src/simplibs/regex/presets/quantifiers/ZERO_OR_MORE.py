# Outers
from ...base_class import Regex
from ...containers.Repeat import Repeat, RepeatMode


def ZERO_OR_MORE(inner: Regex, *, mode: RepeatMode = RepeatMode.GREEDY) -> Repeat:
    """Build a regex expression matching zero or more occurrences of the inner pattern.

    Init Params:
        inner (Regex): The inner regex expression to repeat.
        mode (RepeatMode): The backtracking behavior (greedy, lazy, or possessive).

    Pattern:
        Zero or more occurrences of the inner node (`...*`).

    Example:
        pattern = ZERO_OR_MORE(DIGIT)
        # Matches: "", "5", "12345"
    """
    return Repeat(inner, min=0, max=None, mode=mode)