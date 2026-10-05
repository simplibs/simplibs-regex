# ======================================================================
# Base Class
# ======================================================================
from .base_class.Regex import Regex

# ======================================================================
# Compiler
# ======================================================================
from .compiler.RegexPattern import RegexPattern

# ======================================================================
# Elements & Enums
# ======================================================================
from .elements.Anchor import Anchor
from .elements.enums.AnchorKind import AnchorKind
from .elements.AnyCharacter import AnyCharacter
from .elements.CharacterClass import CharacterClass
from .elements.CharacterRange import CharacterRange
from .elements.CharacterType import CharacterType
from .elements.enums.CharacterTypeKind import CharacterTypeKind
from .elements.CharacterCode import CharacterCode
from .elements.enums.CharacterCodeKind import CharacterCodeKind
from .elements.GroupReference import GroupReference
from .elements.Literal import Literal
from .elements.RawPattern import RawPattern

# ======================================================================
# Containers & Enums
# ======================================================================
from .containers.Alternation import Alternation
from .containers.Conditional import Conditional
from .containers.Group import Group
from .containers.Lookaround import Lookaround
from .containers.enums.LookaroundDirection import LookaroundDirection
from .containers.Repeat import Repeat
from .containers.enums.RepeatMode import RepeatMode
from .containers.Sequence import Sequence

# ======================================================================
# Flags
# ======================================================================
from .flags.Flag import Flag

# ======================================================================
# Presets (Anchors)
# ======================================================================
from .presets.anchors.END import END
from .presets.anchors.END_STRING import END_STRING
from .presets.anchors.NON_WORD_BOUNDARY import NON_WORD_BOUNDARY
from .presets.anchors.START import START
from .presets.anchors.START_STRING import START_STRING
from .presets.anchors.WORD_BOUNDARY import WORD_BOUNDARY

# ======================================================================
# Presets (Any character)
# ======================================================================
from .presets.any_character.ANY import ANY

# ======================================================================
# Presets (Character Types)
# ======================================================================
from .presets.character_types.DIGIT import DIGIT
from .presets.character_types.NON_DIGIT import NON_DIGIT
from .presets.character_types.NON_WHITESPACE import NON_WHITESPACE
from .presets.character_types.NON_WORD_CHARACTER import NON_WORD_CHARACTER
from .presets.character_types.WHITESPACE import WHITESPACE
from .presets.character_types.WORD_CHARACTER import WORD_CHARACTER

# ======================================================================
# Presets (Character Classes)
# ======================================================================
from .presets.character_classes.ALPHANUMERIC import ALPHANUMERIC
from .presets.character_classes.HEX_DIGIT import HEX_DIGIT
from .presets.character_classes.LETTER import LETTER
from .presets.character_classes.LOWERCASE_LETTER import LOWERCASE_LETTER
from .presets.character_classes.UPPERCASE_LETTER import UPPERCASE_LETTER

# ======================================================================
# Presets (Groups)
# ======================================================================
from .presets.groups.ATOMIC_GROUP import ATOMIC_GROUP
from .presets.groups.CASE_INSENSITIVE import CASE_INSENSITIVE
from .presets.groups.NAMED_GROUP import NAMED_GROUP
from .presets.groups.NON_CAPTURING import NON_CAPTURING
from .presets.groups.VERBOSE_GROUP import VERBOSE_GROUP
from .presets.groups.WITH_FLAGS import WITH_FLAGS

# ======================================================================
# Presets (Lookaround)
# ======================================================================
from .presets.lookaround.LOOKAHEAD import LOOKAHEAD
from .presets.lookaround.LOOKBEHIND import LOOKBEHIND
from .presets.lookaround.NEGATIVE_LOOKAHEAD import NEGATIVE_LOOKAHEAD
from .presets.lookaround.NEGATIVE_LOOKBEHIND import NEGATIVE_LOOKBEHIND

# ======================================================================
# Presets (Literals)
# ======================================================================
from .presets.literals.BACKSLASH import BACKSLASH
from .presets.literals.BELL import BELL
from .presets.literals.CARRIAGE_RETURN import CARRIAGE_RETURN
from .presets.literals.FORM_FEED import FORM_FEED
from .presets.literals.NEWLINE import NEWLINE
from .presets.literals.TAB import TAB
from .presets.literals.VERTICAL_TAB import VERTICAL_TAB

# ======================================================================
# Presets (Quantifiers)
# ======================================================================
from .presets.quantifiers.AT_LEAST import AT_LEAST
from .presets.quantifiers.BETWEEN import BETWEEN
from .presets.quantifiers.EXACTLY import EXACTLY
from .presets.quantifiers.ONE_OR_MORE import ONE_OR_MORE
from .presets.quantifiers.OPTIONAL import OPTIONAL
from .presets.quantifiers.ZERO_OR_MORE import ZERO_OR_MORE


__all__ = [
    # Base Class
    "Regex",
    # Compiler
    "RegexPattern",
    # Elements & Enums
    "Anchor",
    "AnchorKind",
    "AnyCharacter",
    "CharacterClass",
    "CharacterRange",
    "CharacterType",
    "CharacterTypeKind",
    "CharacterCode",
    "CharacterCodeKind",
    "GroupReference",
    "Literal",
    "RawPattern",
    # Containers & Enums
    "Alternation",
    "Conditional",
    "Group",
    "Lookaround",
    "LookaroundDirection",
    "Repeat",
    "RepeatMode",
    "Sequence",
    # Flags
    "Flag",
    # Presets - Anchors
    "END",
    "END_STRING",
    "NON_WORD_BOUNDARY",
    "START",
    "START_STRING",
    "WORD_BOUNDARY",
    # Any character
    "ANY",
    # Presets - Character Types
    "DIGIT",
    "NON_DIGIT",
    "NON_WHITESPACE",
    "NON_WORD_CHARACTER",
    "WHITESPACE",
    "WORD_CHARACTER",
    # Presets - Character Classes
    "ALPHANUMERIC",
    "HEX_DIGIT",
    "LETTER",
    "LOWERCASE_LETTER",
    "UPPERCASE_LETTER",
    # Presets - Groups
    "ATOMIC_GROUP",
    "CASE_INSENSITIVE",
    "NAMED_GROUP",
    "NON_CAPTURING",
    "VERBOSE_GROUP",
    "WITH_FLAGS",
    # Presets - Lookaround
    "LOOKAHEAD",
    "LOOKBEHIND",
    "NEGATIVE_LOOKAHEAD",
    "NEGATIVE_LOOKBEHIND",
    # Presets - Literals
    "BACKSLASH",
    "BELL",
    "CARRIAGE_RETURN",
    "FORM_FEED",
    "NEWLINE",
    "TAB",
    "VERTICAL_TAB",
    # Presets - Quantifiers
    "AT_LEAST",
    "BETWEEN",
    "EXACTLY",
    "ONE_OR_MORE",
    "OPTIONAL",
    "ZERO_OR_MORE",
]


_DESIGN_NOTES = """
# Simplibs Regex Library — Main Package Root

## Purpose
The `simplibs-regex` root package provides a clean, expressive,
and type-safe Domain Specific Language (DSL) for constructing,
composing, and compiling regular expressions in Python.
It decouples primitive AST nodes from structural containers
and ergonomic presets, ensuring robust IDE support
and fail-fast validation.

## Core Architecture & Root Packages Registry

| Sub-Package / Module | Type             | Description                                                                         |
| :------------------- | :--------------- | :---------------------------------------------------------------------------------- |
| `base_class`         | Foundation       | Provides the root abstract AST node class (`Regex`) and precedence management.      |
| `compiler`           | Compilation      | Handles expression compilation, pattern generation, and execution (`RegexPattern`). |
| `elements`           | Atomic AST Nodes | Foundational building blocks like literals, anchors, character classes, and codes.  |
| `containers`         | Higher-Order AST | Structural combinators like sequences, alternations, groups, and quantifiers.       |
| `flags`              | Configuration    | Regular expression compilation flags (`Flag`).                                      |
| `presets`             | DSL Shortcuts    | Ready-to-use syntactic helpers and atomic aliases for clean expression building.    |
"""