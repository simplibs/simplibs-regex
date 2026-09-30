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
from .elements.CharacterClass import CharacterClass
from .elements.CharacterRange import CharacterRange
from .elements.CharacterType import CharacterType
from .elements.enums.CharacterTypeKind import CharacterTypeKind
from .elements.CharCode import CharCode
from .elements.enums.CharCodeKind import CharCodeKind
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
# Presets (Character Types)
# ======================================================================
from .presets.character_types.DIGIT import DIGIT
from .presets.character_types.NON_DIGIT import NON_DIGIT
from .presets.character_types.NON_WHITESPACE import NON_WHITESPACE
from .presets.character_types.NON_WORD import NON_WORD
from .presets.character_types.WHITESPACE import WHITESPACE
from .presets.character_types.WORD import WORD

# ======================================================================
# Presets (Groups)
# ======================================================================
from .presets.groups.ATOMIC_GROUP import ATOMIC_GROUP
from .presets.groups.NAMED_GROUP import NAMED_GROUP
from .presets.groups.NON_CAPTURING import NON_CAPTURING

# ======================================================================
# Presets (Lookaround)
# ======================================================================
from .presets.lookaround.LOOKAHEAD import LOOKAHEAD
from .presets.lookaround.LOOKBEHIND import LOOKBEHIND
from .presets.lookaround.NEGATIVE_LOOKAHEAD import NEGATIVE_LOOKAHEAD
from .presets.lookaround.NEGATIVE_LOOKBEHIND import NEGATIVE_LOOKBEHIND

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
    "CharacterClass",
    "CharacterRange",
    "CharacterType",
    "CharacterTypeKind",
    "CharCode",
    "CharCodeKind",
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
    # Presets - Character Types
    "DIGIT",
    "NON_DIGIT",
    "NON_WHITESPACE",
    "NON_WORD",
    "WHITESPACE",
    "WORD",
    # Presets - Groups
    "ATOMIC_GROUP",
    "NAMED_GROUP",
    "NON_CAPTURING",
    # Presets - Lookaround
    "LOOKAHEAD",
    "LOOKBEHIND",
    "NEGATIVE_LOOKAHEAD",
    "NEGATIVE_LOOKBEHIND",
    # Presets - Quantifiers",
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
| `presets`            | DSL Shortcuts    | Ready-to-use syntactic helpers and atomic aliases for clean expression building.    |
"""