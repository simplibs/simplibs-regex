from .raise_raw_pattern_empty_error import raise_raw_pattern_empty_error


_DESIGN_NOTES = """
# RawPattern Validations Sub-Package

## Purpose
Provides structured exception emission helpers for RawPattern element validation.

## Internal Components Registry

| Component                      | Type     | Description                                                                     |
| :----------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_raw_pattern_empty_error`| Function | Emits structured `ValidationError` when raw pattern text is empty.              |
"""