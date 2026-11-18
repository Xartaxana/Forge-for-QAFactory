"""contract.one_line: the one fold-and-cut one-liner (FG7-1)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import contract as C  # noqa: E402

ROWS = [
    ("none", None, None, ""),
    ("empty", "", 5, ""),
    ("falsy non-str", 0, None, ""),
    ("non-str truthy", 12345, None, "12345"),
    ("tabs and newlines", "  a\tb\n\n c \r\n", None, "a b c"),
    ("no limit, long", "x" * 500, None, "x" * 500),
    ("exactly at the limit", "abcde", 5, "abcde"),
    ("one beyond the limit", "abcdef", 5, "abcd…"),
    ("fold before measuring", "a  b  c", 5, "a b c"),
]


class OneLine(unittest.TestCase):
    def test_rows(self):
        for name, text, limit, want in ROWS:
            with self.subTest(name):
                self.assertEqual(C.one_line(text, limit), want)


if __name__ == "__main__":
    unittest.main()
