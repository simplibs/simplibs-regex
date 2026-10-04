# Outers
from ..base_class import Regex, Precedence
# Inners
from ._validations import (
    raise_param_not_identifier_error,
    raise_conditional_invalid_numeric_id_error,
    raise_conditional_invalid_id_type_error,
    raise_param_invalid_type_error
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
    def __init__(
        self,
        id_or_name: int | str,
        yes: Regex,
        no: Regex | None = None
    ) -> None:

        # 1. Parameter validation — id_or_name type (bool is a subclass of int, so it is excluded explicitly)
        if isinstance(id_or_name, bool) or not isinstance(id_or_name, (int, str)):
            raise_conditional_invalid_id_type_error(id_or_name)

        # 2. Parameter validation — numeric ID range check (must be at least 1)
        if isinstance(id_or_name, int) and id_or_name < 1:
            raise_conditional_invalid_numeric_id_error(id_or_name)

        # 3. Parameter validation — string ID/name check (must be a valid Python identifier)
        if isinstance(id_or_name, str) and not id_or_name.isidentifier():
            raise_param_not_identifier_error("id_or_name", id_or_name)

        # 4. Parameter validation — branches
        if not isinstance(yes, Regex):
            raise_param_invalid_type_error("yes", yes)
        if no is not None and not isinstance(no, Regex):
            raise_param_invalid_type_error("no", no)

        # 5. Parameter assignment
        self.id_or_name = id_or_name
        self.yes = yes
        self.no = no

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. The `|` between the branches is Conditional's OWN syntax (and
        #    `re` allows at most two branches), so an Alternation branch
        #    must be wrapped: render each branch at SEQUENCE precedence.
        yes_pattern = self.yes.render(Precedence.SEQUENCE)
        prefix = f"(?({self.id_or_name})"

        if self.no is None:
            return f"{prefix}{yes_pattern})"

        no_pattern = self.no.render(Precedence.SEQUENCE)
        return f"{prefix}{yes_pattern}|{no_pattern})"

    # ----------------------------------------------------------------------
    # Fixed-length introspection
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

## Why branches render at SEQUENCE, not ALTERNATION
Unlike Group/Lookaround, the pipe inside `(?(1)yes|no)` is part of
Conditional's own syntax, and `re` accepts exactly two branches. An
unwrapped Alternation branch would add a third (`(?(1)a|b|c)` ->
"conditional backref with more than two branches") or silently shift
the yes/no split. SEQUENCE wraps it: `(?(1)(?:a|b))`.

## `fixed_length` mirrors Alternation, with one extra case
A `Conditional` with no `no` branch is, in effect, an optional match —
the same "may or may not consume characters" shape as `Repeat(min=0,
max=1)`, hence the unconditional `None`. With both branches present, the
logic is identical to `Alternation.fixed_length`: fixed only if both
sides agree exactly. Reusing that same "equal-or-None" shape here rather
than inventing a different rule keeps the two conceptually-similar
"pick one of two/more paths" mechanisms consistent with each other.
"""
