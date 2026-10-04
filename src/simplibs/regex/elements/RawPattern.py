# Outers
from ..base_class import Regex, Precedence
# Inners
from ._validations import (
    raise_raw_pattern_empty_error,
    raise_param_invalid_type_error
)


class RawPattern(Regex):
    """Escape hatch for raw regex syntax the DSL does not (yet) express as
    its own node — the text is trusted to already be valid `re` syntax
    and is inserted UNCHANGED, with no escaping.

    Unlike `Literal` (which escapes its text — "the string you gave me,
    matched literally"), `RawPattern` makes the opposite promise: "the
    regex syntax you gave me, unchanged." The two are not
    interchangeable, and the difference is exactly why this is its own
    node rather than something `Literal` or `RegexPattern` would infer
    from a plain `str`.

    Example:
        RawPattern(r"a{2,4}")            # -> "a{2,4}", inserted as-is
        RawPattern("(?:x|y)+")           # -> "(?:x|y)+", verbatim
    """

    __slots__ = ("text",)

    # Always wrapped in (?:...) when embedded in any composed context —
    # the safest possible default, since this node's actual internal
    # structure (does it contain a top-level "|"? a quantifier?) is
    # unknown and unknowable without parsing it, which is exactly the
    # work this DSL exists to avoid doing.
    _precedence = Precedence.ALTERNATION

    # Never usable inside a CharacterClass — the escaping rules inside
    # [...] differ from the rest of a pattern, and an opaque
    # raw string cannot be verified to follow them.
    _usable_in_char_class = False

    # ----------------------------------------------------------------------
    # Constructor initialization
    # ----------------------------------------------------------------------
    def __init__(
        self,
        text: str
    ) -> None:

        # 1. Parameter validation — type
        if not isinstance(text, str):
            raise_param_invalid_type_error(
                "text", "a str", text, 'RawPattern("a{2,4}")'
            )

        # 2. Parameter validation — raw pattern text cannot be empty
        if text == "":
            raise_raw_pattern_empty_error()

        # 3. Parameter assignment
        self.text = text

    # ----------------------------------------------------------------------
    # Pattern production
    # ----------------------------------------------------------------------
    def to_pattern(self) -> str:

        # 1. Inserted verbatim — this is the entire point of the node.
        return self.text

    # ----------------------------------------------------------------------
    # Fixed-length introspection
    # ----------------------------------------------------------------------
    def fixed_length(self) -> int | None:

        # 1. Never guessed. The text's actual match width cannot be
        #    known without parsing it — always reporting None means a
        #    RawPattern inside Lookaround(direction=BEHIND) is always
        #    rejected, which is the correct, safe outcome: this library
        #    would rather refuse a lookbehind it cannot verify than
        #    silently accept one that might not actually have a fixed
        #    width at runtime.
        return None


_DESIGN_NOTES = """
# RawPattern — Explicit Raw-Syntax Escape Hatch

## Why this exists at all, given the DSL's whole point is avoiding raw regex
No DSL can express every corner of `re` syntax on day one, and forcing a
caller to wait for a new `Regex` node before they can use a legitimate
piece of syntax would make the library a blocker rather than a tool.
`RawPattern` is the pressure valve — but a NAMED one, so reaching for it
is always a visible, searchable decision in the code, not something
that happens by accident.

## Why every capability defaults to the safest possible answer
`RawPattern` cannot know what its own text actually contains — it might
be `a{2,4}` (one token), `cat|dog` (a top-level alternation), or
`(?:x)(?:y)` (already self-delimiting). Rather than trying to guess,
every method answers as conservatively as possible:
* `_precedence = ALTERNATION` — always wrapped in `(?:...)` when
  embedded, since it might genuinely need it (an unwrapped `cat|dog`
  inside a Sequence) and over-wrapping is harmless.
* `fixed_length() -> None` — never claims a width it cannot verify, so
  it can never be the cause of a `Lookaround` silently compiling
  something Python's `re` would have rejected.
* `_usable_in_char_class = False` — never offered as a CharacterClass
  item, since the escaping rules inside [...] cannot be confirmed for
  opaque text.

This is the same design stance `CharacterRange.to_pattern` takes when it
refuses to render standalone — when a node genuinely cannot know
something safely, it says so structurally, rather than quietly guessing
and letting a wrong guess surface as a confusing bug three layers away.

## Why this lives in `elements/`, not as a `RegexPattern` constructor path
Keeping it as its own node (rather than accepting a bare `str` in
`RegexPattern.__init__`) preserves a real, load-bearing distinction:
`Literal("b.c")` and `RawPattern("b.c")` render to visibly different
output (`b\\.c` vs `b.c`) precisely because they mean different things —
"this literal text" vs. "this regex syntax, trust me." Collapsing that
distinction into one implicit `str` overload would force every reader
to know, from context alone, which meaning was intended at any given
call site.
"""