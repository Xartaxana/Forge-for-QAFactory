"""test_volume: one table over (numstat text, message text, merge flag) -> (warned, (test, product))."""
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_volume as tv  # noqa: E402

T = "tools/test_x.py"
P = "tools/x.py"


def ns(*rows):
    return "\n".join("%s\t0\t%s" % r for r in rows) + "\n"


CASES = [
    # id, numstat, message, merge, warned, numbers
    ("equal", ns((10, T), (10, P)), "m", False, False, (10, 10)),
    ("test_gt_product", ns((11, T), (10, P)), "m", False, True, (11, 10)),
    ("door_present", ns((11, T), (10, P)), "m\n\nTests-Over: big fixture", False, False, (11, 10)),
    ("door_indented", ns((11, T), (10, P)), "m\n   tests-over: why", False, False, (11, 10)),
    ("door_empty", ns((11, T), (10, P)), "m\ntests-over:   \n", False, True, (11, 10)),
    ("door_commented", ns((11, T), (10, P)), "m\n# tests-over: why\n", False, True, (11, 10)),
    ("empty_then_real_door", ns((11, T), (10, P)), "tests-over:\ntests-over: why", False, False, (11, 10)),
    ("merge", ns((50, T), (1, P)), "Merge x", True, False, (50, 1)),
    ("binary", "-\t-\ttools/fixtures/a.bin\n3\t0\t" + P + "\n", "m", False, False, (0, 3)),
    ("rename_added_only", "2\t9\ttools/{old_x.py => test_new.py}\n1\t0\t" + P + "\n", "m", False, True, (2, 1)),
    ("rename_arrow", "5\t0\ttools/a.py => tools/test_a.py\n", "m", False, True, (5, 0)),
    ("excluded_only", ns((99, "docs/a.md"), (99, "plans/b.md"), (9, "README.md"), (9, "logs/j.jsonl")),
     "m", False, False, (0, 0)),
    ("both_zero", "", "m", False, False, (0, 0)),
    ("product_zero", ns((4, T)), "m", False, True, (4, 0)),
    ("fixture_50000", ns((50000, "ai-packages/q/tests/fixtures/big.json"), (10, P)), "m", False, True, (50000, 10)),
    ("excluded_dirs", ns((5, ".claude/x.py"), (5, ".githooks/h"), (5, "kb/p.md"), (5, "a/changelog.d/f.md"),
                         (5, "experiments/foo/test_a.py")), "m", False, False, (0, 0)),
    ("measurers_product", ns((5, "experiments/measurers/m.py")), "m", False, False, (0, 5)),
    ("unknown_dir_excluded", ns((9, "scripts/s.py")), "m", False, False, (0, 0)),
    ("garbage_rows", "junk\nx\ty\n", "m", False, False, (0, 0)),
]


@pytest.mark.parametrize(
    "numstat,message,merge,warned,numbers", [c[1:] for c in CASES], ids=[c[0] for c in CASES]
)
def test_decide(numstat, message, merge, warned, numbers):
    w, nums, text = tv.decide(numstat, message, merge)
    assert (w, nums) == (warned, numbers)
    assert bool(text) == warned
    if warned:
        assert "+%d test lines vs +%d product lines" % numbers in text
        assert "tests-over:" in text


def test_empty_door_text_says_reason_empty():
    _w, _n, text = tv.decide(ns((11, T), (10, P)), "tests-over:", False)
    assert "reason is empty" in text


def test_git_failure_never_blocks(tmp_path):
    # not a repo: git diff fails -> "not measured", exit 0 (E-A3-6)
    r = subprocess.run(
        [sys.executable, "-B", tv.__file__, str(tmp_path / "absent-msg")],
        cwd=str(tmp_path), capture_output=True, text=True,
        env={**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path.parent)},
    )
    assert r.returncode == 0
    assert "test_volume: not measured" in r.stderr
