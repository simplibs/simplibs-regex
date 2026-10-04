from .assert_pattern import assert_pattern


__all__ = ["assert_pattern"]


_DESIGN_NOTES = """
# Regex Testing Sub-Package

## Purpose
Test helpers for code built on `simplibs-regex`: its own presets and
libraries such as `simplibs-patterns`.

## Components Registry

| Component        | Type     | Description                                                              |
| :--------------- | :------- | :----------------------------------------------------------------------- |
| `assert_pattern` | Function | Verifies a pattern's rendered string and its matching / non-matching texts. |

## Why it is not exported from `simplibs.regex`
A test helper is not part of the DSL itself. It is imported explicitly
(`from simplibs.regex.testing import assert_pattern`), so ordinary use of
the library never loads it.
"""