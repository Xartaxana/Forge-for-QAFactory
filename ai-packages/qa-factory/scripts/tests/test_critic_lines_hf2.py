"""test_critic_lines_hf2.py - the code critic's lines of HF2-13/14/15 (TQ1-13, TQ1-14, TQ1-12), key presence.

The seven key phrases are the ones the spec t-084 quoted BEFORE the run; each must stand VERBATIM
(raw bytes, no whitespace folding) in the file the spec names. A key already said by an older line
is extended there, never said twice, so presence in the named file is the whole check. The
generated slices that carry the new patterns section to the automator and the critic are checked
for the D14a key as well, and a NEGATIVE control proves the helper can fail: a key that is in no
file is reported absent by the same helper.

Runnable on its own: `python -B scripts/tests/test_critic_lines_hf2.py`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness import PLUGIN_ROOT, check, finish  # noqa: E402

KEYS = [
    ("D13a", "agents/qa-code-critic.md", "a second helper beside an existing one"),
    ("D13b", "references/code-review-rubric.md", "the same fixture created twice"),
    ("D14a", "references/test-code-patterns.md", "assert the count before unpacking"),
    ("D14b", "references/code-review-rubric.md", "the red line names the Then"),
    ("D14c", "agents/qa-code-critic.md", "the test's level matches the S3 plan"),
    ("D15a", "references/code-review-rubric.md", "a refusal test discriminates the cause"),
    ("D15b", "references/code-review-rubric.md", "a masked value compared with a masked value"),
]
SLICES_WITH_D14A = [
    "references/slices/qa-automator/test-code-patterns.md",
    "references/slices/qa-code-critic/test-code-patterns.md",
]


def key_present(rel: str, key: str) -> bool:
    """True when `key` stands verbatim in the package file `rel`; prints one line saying which."""
    text = (PLUGIN_ROOT / rel).read_text(encoding="utf-8")
    found = key in text
    print(f"  key {'present' if found else 'ABSENT '} in {rel}: {key!r}")
    return found


for item, rel, key in KEYS:
    check(f"{item}: {key!r} stands in {rel}", key_present(rel, key))

for rel in SLICES_WITH_D14A:
    check(f"D0: the D14a key reached the generated slice {rel}",
          key_present(rel, "assert the count before unpacking"))

# NEGATIVE control (doc-witness property iii): the same helper must report a key that is in no file as absent.
check("negative control: 'zzz-not-in-any-file' is reported ABSENT by the same helper",
      not key_present("references/code-review-rubric.md", "zzz-not-in-any-file"))

finish("critic lines HF2-13/14/15 (key presence + negative control)")
