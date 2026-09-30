# Outers
from ...base_class import Regex
from ...containers.Repeat import Repeat, RepeatMode


def AT_LEAST(inner: Regex, count: int, *, mode: RepeatMode = RepeatMode.GREEDY) -> Repeat:
    """Build a regex expression matching a minimum number of occurrences.

    Init Params:
        inner (Regex): The inner regex expression to repeat.
        count (int): The minimum required number of repetitions.
        mode (RepeatMode): The backtracking behavior (greedy, lazy, or possessive).

    Pattern:
        A minimum number of repetitions with no upper bound (`...{count,}`).

    Example:
        pattern = AT_LEAST(DIGIT, 2)
        # Matches: "12", "12345"
        # Does not match: "1"
    """
    return Repeat(inner, min=count, max=None, mode=mode)