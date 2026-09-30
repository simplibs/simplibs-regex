# Outers
from ...base_class import Regex
from ...containers.Lookaround import Lookaround, LookaroundDirection


def LOOKBEHIND(inner: Regex) -> Lookaround:
    """Build a regex expression matching a positive lookbehind assertion.

    Init Params:
        inner (Regex): The inner regex expression that must precede the current position (must have a fixed length).

    Pattern:
        A zero-width positive lookbehind assertion (`(?<=...)`).

    Example:
        pattern = Sequence(LOOKBEHIND(Literal("foo")), Literal("bar"))
        # Matches: "bar" only if it is preceded by "foo"
    """
    return Lookaround(inner, direction=LookaroundDirection.BEHIND)