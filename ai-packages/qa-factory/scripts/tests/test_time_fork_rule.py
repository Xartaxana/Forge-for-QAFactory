"""test_time_fork_rule.py - TQ1-24 (t-1701 D5-B): a time fork names its tolerance and its "cannot tell" outcome.

Keys are fixed in the spec BEFORE the run (doc-witness property i):
K1 `from the requirements` and `cannot tell` stand in both case charters (whitespace folded);
K2 `cannot tell` and `t_after + tolerance` stand in the test-code patterns;
K3 `cannot-tell` stands in the code-review rubric.
NEG: a key absent from a copy of the text is reported (property iii).

Runnable on its own: `python -B scripts/tests/test_time_fork_rule.py`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import PLUGIN_ROOT, check, finish  # noqa: E402

DESIGNER = "agents/qa-case-designer.md"
CRITIC = "agents/qa-case-critic.md"
PATTERNS = "references/test-code-patterns.md"
RUBRIC = "references/code-review-rubric.md"

KEYS = [
    ("K1", DESIGNER, "from the requirements"),
    ("K1", DESIGNER, "cannot tell"),
    ("K1", CRITIC, "from the requirements"),
    ("K1", CRITIC, "cannot tell"),
    ("K2", PATTERNS, "cannot tell"),
    ("K2", PATTERNS, "t_after + tolerance"),
    ("K3", RUBRIC, "cannot-tell"),
    ("F2", DESIGNER, "manual-evidence"),   # t-1755 F2: the case critic keeps the review its designer twin keeps
    ("F2", CRITIC, "manual-evidence"),
]


def folded(rel: str) -> str:
    return " ".join((PLUGIN_ROOT / rel).read_text(encoding="utf-8").split())


def absent(text: str, key: str) -> bool:
    return key not in text


def main() -> None:
    for item, rel, key in KEYS:
        check(f"{item}: {key!r} stands in {rel}", not absent(folded(rel), key))
    stripped = folded(CRITIC).replace("cannot tell", "")
    check("NEG: the critic text without `cannot tell` is reported absent by the same helper", absent(stripped, "cannot tell"))
    finish("time fork rule (key presence + negative control)")


if __name__ == "__main__":
    main()
