from .NAMED_GROUP import NAMED_GROUP
from .NON_CAPTURING import NON_CAPTURING
from .ATOMIC_GROUP import ATOMIC_GROUP
from .WITH_FLAGS import WITH_FLAGS
from .CASE_INSENSITIVE import CASE_INSENSITIVE
from .VERBOSE_GROUP import VERBOSE_GROUP


_DESIGN_NOTES = """
# Groups Presets Sub-Package

## Purpose
Provides structural group helpers (`NAMED_GROUP`, `NON_CAPTURING`, `ATOMIC_GROUP`) built on top of the underlying `Group` container.

## Components Registry

| Component       | Type   | Description                                           |
| :-------------- | :----- | :---------------------------------------------------- |
| `NAMED_GROUP`   | Preset | Builds a named capturing group (`(?P<name>...)`).     |
| `NON_CAPTURING` | Preset | Builds a non-capturing group (`(?:...)`).             |
| `ATOMIC_GROUP`  | Preset | Builds an atomic non-backtracking group (`(?>...)`).  |
"""