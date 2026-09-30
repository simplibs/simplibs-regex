# Outers
from ...base_class import Regex
from ...containers.Lookaround import Lookaround, LookaroundDirection


def NEGATIVE_LOOKBEHIND(inner: Regex) -> Lookaround:
    """Build a regex expression matching a negative lookbehind assertion.

    Init Params:
        inner (Regex): The inner regex expression that must NOT precede the current position (must have a fixed length).

    Pattern:
        A zero-width negative lookbehind assertion (`(?<!...)`).

    Example:
        pattern = Sequence(NEGATIVE_LOOKBEHIND(Literal("foo")), Literal("bar"))
        # Matches: "bar" only if it is NOT preceded by "foo"
    """
    return Lookaround(inner, direction=LookaroundDirection.BEHIND, negate=True)