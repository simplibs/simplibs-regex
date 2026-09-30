# Outers
from ...base_class import Regex
from ...containers.Lookaround import Lookaround, LookaroundDirection


def LOOKAHEAD(inner: Regex) -> Lookaround:
    """Build a regex expression matching a positive lookahead assertion.

    Init Params:
        inner (Regex): The inner regex expression that must follow the current position.

    Pattern:
        A zero-width positive lookahead assertion (`(?=...)`).

    Example:
        pattern = Sequence(Literal("foo"), LOOKAHEAD(Literal("bar")))
        # Matches: "foo" only if it is followed by "bar"
    """
    return Lookaround(inner, direction=LookaroundDirection.AHEAD)