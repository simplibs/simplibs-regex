from .raise_invalid_pattern_error import raise_invalid_pattern_error
from .raise_invalid_locale_error import raise_invalid_locale_error
from .raise_param_invalid_type_error import raise_param_invalid_type_error


_DESIGN_NOTES = """
# Pattern Validations Sub-Package

## Purpose
Provides structured exception emission helpers for RegexPattern validation.

## Internal Components Registry

| Component                                   | Type     | Description                                                                     |
| :------------------------------------------ | :------- | :------------------------------------------------------------------------------ |
| `raise_invalid_pattern_error`               | Function | Emits structured validation error when regex compilation fails (`re.error`).    |
| `raise_invalid_locale_error`                | Function | Emits structured `ParamError` when Flag.LOCALE is used with string compilation. |
| `raise_param_invalid_type_error`            | Function | Emits structured `ParamError` when a constructor argument has the wrong type.   |
"""