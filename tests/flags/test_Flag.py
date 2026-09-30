from simplibs.regex.flags.Flag import Flag
import re

def test_flag_values_and_re_mapping():
    """Verify that Flag members map to their correct regex string values and re module flags."""
    assert Flag.ASCII.value == "a"
    assert Flag.ASCII.re_flag == re.ASCII

    assert Flag.IGNORECASE.value == "i"
    assert Flag.IGNORECASE.re_flag == re.IGNORECASE

    assert Flag.LOCALE.value == "L"
    assert Flag.LOCALE.re_flag == re.LOCALE

    assert Flag.MULTILINE.value == "m"
    assert Flag.MULTILINE.re_flag == re.MULTILINE

    assert Flag.DOTALL.value == "s"
    assert Flag.DOTALL.re_flag == re.DOTALL

    assert Flag.UNICODE.value == "u"
    assert Flag.UNICODE.re_flag == re.UNICODE

    assert Flag.VERBOSE.value == "x"
    assert Flag.VERBOSE.re_flag == re.VERBOSE