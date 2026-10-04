from ...base_class import Regex
from ...containers.Group import Group
from ...flags.Flag import Flag

def WITH_FLAGS(inner: Regex, *flags: Flag) -> Group:
    """Build a regex expression matching `inner` with scoped inline flags.

    Init Params:
        inner (Regex): The inner regex expression the flags apply to.
        *flags (Flag): The flags to switch on inside the group.

    Pattern:
        A non-capturing group with flags scoped to `inner` only (`(?flags:...)`).
        Generic fallback for any flag combination without its own named preset.

    Example:
        pattern = WITH_FLAGS(ONE_OR_MORE(DIGIT), Flag.MULTILINE, Flag.DOTALL)
        # Matches: digits, with MULTILINE and DOTALL active inside the group only
    """
    return Group(inner, capturing=False, flags=frozenset(flags))
