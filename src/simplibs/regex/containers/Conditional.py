# Outers
from ..base_class import Regex, _Precedence
# Inners
from ._validations import (
    raise_conditional_invalid_numeric_id_error,
    raise_conditional_invalid_name_error,
    raise_conditional_invalid_id_type_error,
    raise_conditional_yes_not_regex_error,
    raise_conditional_no_not_regex_error,
)


class Conditional(Regex):
    """Match `yes` if the referenced group participated in the match so
    far, otherwise match `no` (or nothing, if `no` is omitted).

    Pattern:
        (?(id_or_name)yes)         no is None
        (?(id_or_name)yes|no)      no is given

    Example:
        Conditional(1, Literal("a"), Literal("b"))   # -> "(?(1)a|b)"
        Conditional("quoted", Literal('"'))          # -> "(?(quoted)\\")"
    """

    __slots__ = ("id_or_name", "yes", "no")

    # Self-delimiting via its own (?(...)...) syntax — stays at the base
    # class ATOM default, same reasoning as Group/Lookaround/CharacterClass.

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(self, id_or_name: int | str, yes: Regex, no: Regex | None = None) -> None:

        # 1. Parameter validation — id_or_name (explicit condition check + dedicated raise)
        if isinstance(id_or_name, int):
            if id_or_name < 1:
                raise_conditional_invalid_numeric_id_error(id_or_name)
        elif isinstance(id_or_name, str):
            if not id_or_name.isidentifier():
                raise_conditional_invalid_name_error(id_or_name)
        else:
            raise_conditional_invalid_id_type_error(id_or_name)

        # 2. Parameter validation — yes/no
        if not isinstance(yes, Regex):
            raise_conditional_yes_not_regex_error(yes)
        if no is not None and not isinstance(no, Regex):
            raise_conditional_no_not_regex_error(no)

        # 3. Parameter assignment
        self.id_or_name = id_or_name
        self.yes = yes
        self.no = no

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Own parentheses already delimit both branches — render each
        #    at the loosest precedence, same reasoning as Group/Lookaround.
        yes_pattern = self.yes.render(_Precedence.ALTERNATION)
        prefix = f"(?({self.id_or_name})"

        if self.no is None:
            return f"{prefix}{yes_pattern})"

        no_pattern = self.no.render(_Precedence.ALTERNATION)
        return f"{prefix}{yes_pattern}|{no_pattern})"

    # ----------------------------------------------------------------------
    # Fixed-length introspection (Point 3)
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Without a `no` branch, the whole construct is effectively
        #    optional (matches `yes` or nothing) — variable by nature.
        if self.no is None:
            return None

        # 2. With both branches present, the length is fixed only if
        #    both branches individually have the SAME fixed length —
        #    identical reasoning to Alternation.fixed_length.
        yes_length = self.yes.fixed_length()
        no_length = self.no.fixed_length()

        if yes_length is not None and yes_length == no_length:
            return yes_length

        return None


_DESIGN_NOTES = """
# Conditional — Group-Existence Branching

## Why it stays a single, standalone mechanism
Unlike `Repeat`/`Group`/`Lookaround`, `Conditional` has only one real
Python `re` syntax shape (with or without a `no` branch) — there is no
family of variant syntaxes to collapse here, so it does not need an
internal mode enum the way those three do. `no: Regex | None = None`
already captures the one genuine variation point.

## `fixed_length` mirrors Alternation, with one extra case
A `Conditional` with no `no` branch is, in effect, an optional match —
the same "may or may not consume characters" shape as `Repeat(min=0,
max=1)`, hence the unconditional `None`. With both branches present, the
logic is identical to `Alternation.fixed_length`: fixed only if both
sides agree exactly. Reusing that same "equal-or-None" shape here rather
than inventing a different rule keeps the two conceptually-similar
"pick one of two/more paths" mechanisms consistent with each other.
"""
