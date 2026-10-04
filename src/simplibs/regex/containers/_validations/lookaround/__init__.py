from .raise_variable_length_lookbehind_error import raise_variable_length_lookbehind_error

_DESIGN_NOTES = """
# Lookaround Validations Sub-Package

## Purpose
Provides structured exception emission helpers for Lookaround container validation.

## Internal Components Registry

| Component                                       | Type     | Description                                                                     |
| :---------------------------------------------- | :------- | :------------------------------------------------------------------------------ |
| `raise_variable_length_lookbehind_error`        | Function | Emits structured `ParamError` when lookbehind has variable length.              |
"""