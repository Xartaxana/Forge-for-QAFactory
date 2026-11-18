"""tools/ascii_line.py: the one ASCII line helper. One table, one behaviour per row (FG7-56)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ascii_line  # noqa: E402

REPLACE = {}
REAPER = {"control": " ", "strip": False, "none": ""}
ESCAPE = {"errors": "backslashreplace", "control": None, "strip": False}
ROWS = [  # (value, max_len, profile, expected)
    ("a\nINJECTED", 80, REPLACE, "aINJECTED"),
    ("\x00 a", 80, REPLACE, " a"),  # strip runs before control removal
    ("café \U0001F600 \ud800", 80, REPLACE, "caf? ? ?"),
    ("   ", 80, REPLACE, ""),
    (None, 80, REPLACE, "None"),
    (ValueError("é\nboom"), 80, REPLACE, "?boom"),
    ("a" * 80, 80, REPLACE, "a" * 80),
    ("a" * 81, 80, REPLACE, "a" * 80),
    ("abc", 0, REPLACE, ""),
    (None, 20, REAPER, ""),
    (" a\t\x7fbé ", 20, REAPER, " a  b? "),
    ("caféд\U0001F600\n", None, ESCAPE, "caf\\xe9\\u0434\\U0001f600\n"),
    ("x" * 1_000_000, 80, REPLACE, "x" * 80),
    ("x" * 1_000_000, None, REPLACE, "x" * 1_000_000),
    ("abc", 5, {"errors": "ignore"}, ValueError),
    ("abc", -1, REPLACE, ValueError),
]


@pytest.mark.parametrize("value,max_len,profile,expected", ROWS)
def test_clip(value, max_len, profile, expected):
    if expected is ValueError:  # a mistyped handler and a negative cap are refused on an ASCII input
        with pytest.raises(ValueError):
            ascii_line.clip(value, max_len, **profile)
    else:
        assert ascii_line.clip(value, max_len, **profile) == expected
