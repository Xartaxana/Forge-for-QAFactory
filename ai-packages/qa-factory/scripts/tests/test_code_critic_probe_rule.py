#!/usr/bin/env python3
"""RN1-8 K6 / K11: the code critic's charter carries the door for a probe whose failure is AT the mutated line but whose wording the detector row
did not know (`incomplete`, `cause: data_row`): it reads the probe-run log and, when the inverted assertion form is there, writes
`critic_verdict: unverified` plus `sensitivity_proof_missing_reason` quoting the log line (the contract has no `killed`; the guard refuses it).
Two checks: the rule's keys are present (with a negative control: a key removed -> red), and EVERY `critic_verdict:` value the charter names is
a word of `contract.CRITIC_VERDICTS` (with a negative control: `killed` -> red), so the door the charter opens is one the guard lets through."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import contract as C  # noqa: E402
from harness import SCRIPTS, check, check_eq, finish  # noqa: E402

CHARTER = SCRIPTS.parent / "agents" / "qa-code-critic.md"
KEYS = ("`incomplete` whose failure is AT the mutated line", "`cause: data_row`", "read the probe-run log",
        "`expect(received).not.toBe`", "`critic_verdict: unverified`", "`sensitivity_proof_missing_reason` quoting that log line")


def missing(text: str) -> list:
    """The keys of the rule that the text does not carry, in order."""
    return [key for key in KEYS if key not in text]


def unknown_verdicts(text: str) -> list:
    """The `critic_verdict: <word>` values the text names that the contract does not know."""
    return sorted({w for w in re.findall(r"critic_verdict:\s*`?([a-z_]+)", text) if w not in C.CRITIC_VERDICTS})


def main() -> None:
    text = CHARTER.read_text(encoding="utf-8")
    check_eq("K6: the charter carries every key of the data_row door", missing(text), [])
    for key in KEYS:
        check_eq(f"K6 negative control: without {key!r} the check is red", missing(text.replace(key, "")), [key])
    start = text.index(KEYS[0])
    check("K6: the rule stands in step 3 of the window procedure (before step 4, the sandbox probe)",
          text.index("3. `probe_by_code.py`") < start < text.index("4. `red_sandbox.py --probe`"))
    check("K6: the rule is at most 4 lines", text[start:text.index("4. `red_sandbox.py --probe`")].count("\n") <= 4)
    check("K6: the old step-3 sentence no longer says every `incomplete` is tooling (the data_row case is named)",
          "(except the `cause: data_row` case below)" in text)
    check_eq("K11: every critic_verdict value the charter names is in contract.CRITIC_VERDICTS", unknown_verdicts(text), [])
    check("K11 control premise: the charter names at least one critic_verdict", "critic_verdict:" in text)
    check_eq("K11 negative control: `critic_verdict: killed` is caught", unknown_verdicts(text + "\n`critic_verdict: killed`"), ["killed"])
    finish("test_code_critic_probe_rule")


if __name__ == "__main__":
    main()
