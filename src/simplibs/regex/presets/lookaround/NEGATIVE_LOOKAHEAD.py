# Outers
from ...base_class import Regex
from ...containers.Lookaround import Lookaround, LookaroundDirection


def NEGATIVE_LOOKAHEAD(inner: Regex) -> Lookaround:
    """Build a regex expression matching a negative lookahead assertion.

    Init Params:
        inner (Regex): The inner regex expression that must NOT follow the current position.

    Pattern:
        A zero-width negative lookahead assertion (`(?!...)`).

    Example:
        pattern = Sequence(Literal("foo"), NEGATIVE_LOOKAHEAD(Literal("bar")))
        # Matches: "foo" only if it is NOT followed by "bar"
    """
    return Lookaround(inner, direction=LookaroundDirection.AHEAD, negate=True)