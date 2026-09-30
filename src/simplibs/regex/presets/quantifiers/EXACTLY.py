# Outers
from ...base_class import Regex
from ...containers.Repeat import Repeat


def EXACTLY(inner: Regex, count: int) -> Repeat:
    """Build a regex expression matching an exact count of occurrences.

    Init Params:
        inner (Regex): The inner regex expression to repeat.
        count (int): The exact number of times the inner expression must repeat.

    Pattern:
        An exact number of repetitions (`...{count}`).

    Example:
        pattern = EXACTLY(DIGIT, 3)
        # Matches: "123", "999"
        # Does not match: "12", "1234"
    """
    return Repeat(inner, min=count, max=count)