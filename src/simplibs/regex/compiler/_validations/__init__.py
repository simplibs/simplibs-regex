from .raise_invalid_pattern_error import raise_invalid_pattern_error
from .raise_regex_pattern_invalid_flags_error import raise_regex_pattern_invalid_flags_error
from .raise_regex_pattern_invalid_node_error import raise_regex_pattern_invalid_node_error

_DESIGN_NOTES = """
# Pattern Validations Sub-Package

## Purpose
Provides structured exception emission helpers for RegexPattern validation.

## Internal Components Registry

| Component                                   | Type     | Description                                                                     |
| :------------------------------------------ | :------- | :------------------------------------------------------------------------------ |
| `raise_invalid_pattern_error`               | Function | Emits structured validation error when regex compilation fails (`re.error`).    |
| `raise_regex_pattern_invalid_flags_error`   | Function | Emits structured `ParamError` when RegexPattern receives invalid flags.        |
| `raise_regex_pattern_invalid_node_error`    | Function | Emits structured `ParamError` when RegexPattern receives an invalid node type.  |
"""