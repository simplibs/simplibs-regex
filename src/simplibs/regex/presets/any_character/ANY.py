# Outers
from ...elements.AnyCharacter import AnyCharacter


ANY = AnyCharacter()
"""Regex expression matching any single character.

Init Params:
    (no parameters)

Pattern:
    Matches any character except a newline (`.`); with the DOTALL flag
    it matches a newline too.

Example:
    ANY
    # Matches: "a", "5", " ", "!"
    # Does not match: "\\n" (without DOTALL)
"""