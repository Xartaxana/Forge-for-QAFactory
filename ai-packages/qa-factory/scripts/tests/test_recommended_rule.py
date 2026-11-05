#!/usr/bin/env python3
"""GW1-44: an option is called recommended only after its executor is named (t-538 section 3).

CART-1: the conductor's free text called an option recommended (a config key the factory never reads) and went
past the option validator. Code cannot gate free text, so the rule lives in the text the conductor is given. The one
label code prints itself is the no-change question's `(Recommended)` on `current code` (`story_run.py`, SS1-13), and only
where its reader is named: `launch.implementation_source`, read by `s0_rest`, `role_lines` and qa-scout.md steps 4 and 6.

HONEST NOTE (FR-33): this file proves the rule IS there - the sentence in references/human-questions.md and the
pointer in references/conductor.md. Whether the conductor obeys it is proven only by reading the questions of a
live run.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, check_in, finish  # noqa: E402

REFS = PLUGIN_ROOT / "references"
KEY = "An option is called recommended only after"          # the presence key of the spec, VERBATIM
POINTER = "Recommend an option only after naming who carries it out"
CAP = 12000                                                 # references/*.md, selftest --limits

hq = (REFS / "human-questions.md").read_text(encoding="utf-8")
cond = (REFS / "conductor.md").read_text(encoding="utf-8")
stages = (REFS / "stages.json").read_text(encoding="utf-8")

check_in("human-questions.md carries the rule", KEY, hq)
check_in("the rule names the reader", "the function or field of the factory that reads what the option changes", hq)
check_in("no reader: not recommended, said unchecked", "the option is not recommended, and if it stays, the text says it is unchecked", hq)
check_in("config key: reader first, no reader no option", "no reader, no option, and the text says why", hq)
check_in("conductor.md points at the rule", POINTER, cond)
check("the rule follows item 6 (price and consequences)", 0 < hq.index("6. **Price and consequences") < hq.index(KEY))
# negative control: the same search over a file that must not carry the rule is empty
check("negative control: stages.json has no such key", KEY not in stages and POINTER not in stages)
check("positive control of the same search shape: stages.json is readable and not empty", len(stages) > 100)
for name, text in (("human-questions.md", hq), ("conductor.md", cond)):
    size = len((REFS / name).read_bytes())
    check(f"{name} stays within the {CAP} byte ceiling ({size})", size <= CAP)

finish("test_recommended_rule")
