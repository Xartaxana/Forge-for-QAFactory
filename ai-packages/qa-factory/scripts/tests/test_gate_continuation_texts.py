"""After a gate decision is recorded the factory goes on in the same window (HF1-8, GW1-12).

The skill text used to end the window unconditionally: "After the decision is recorded, stop with one
line: `<TICKET> is at S<n>; continue with /qa-factory:qa-story <TICKET>`" (SKILL.md since 0.7.11) and the
twin in s8.md ("Then end your window ... One step left: the retro"). On TP1-12586 the orchestrator
stopped after an approved gate A with the window budget untouched and asked the person to restart a factory
that could have gone on. The window is changed by `window_budget` alone, and the one planned stop is the
project's `pipeline.stop_after`.

This is the doc-dispatch witness (CLAUDE.md rule 11): the keys are quoted VERBATIM from the spec
(docs/tasks/specs/t-050-hf1-8-gw1-12.md, section 3.7) and were fixed before the run, the script is
committed, and it carries its own NEGATIVE control - the same checker run over a copy of SKILL.md with the
removed sentence put back, and over a copy of s8.md with one required key taken out, must report each.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, check_eq, finish  # noqa: E402

SKILL_DIR = PLUGIN_ROOT / "skills" / "qa-story"
SKILL_CAP = 19000          # selftest.py --limits: a size pin is a cap (builder rule 7), never "no larger than before"

# (file, key) pairs. ABSENT keys are the removed unconditional stop; PRESENT keys are its replacement.
ABSENT = (
    ("SKILL.md", "stop with one line"),
    ("SKILL.md", "is at S<n>;"),
    ("phases/s8.md", "Then end your window"),
    ("phases/s8.md", "One step left: the retro."),
    ("SKILL.md", "fresh window"),
    ("phases/s4.md", "fresh window"),
    ("phases/s8.md", "fresh window"),
)
PRESENT = (
    ("SKILL.md", "Read the gate-decision answer whole: follow `next_action` in this window;"),
    ("SKILL.md", "only its `window` line changes it."),
    ("SKILL.md", "A window that only recovered or recorded"),
    ("phases/s4.md", "the gate-decision answer's `next_action` is then `stop`"),
    ("phases/s4.md", "start S5 in this window unless the answer's `window` line asks for a change"),
    ("phases/s4.md", "never pipe it through `cut`, `head` or `tail`"),
    ("phases/s8.md", "go on to S9 in this window"),
    ("phases/s8.md", "never pipe it through `cut`, `head` or `tail`"),
)


def read_texts() -> dict:
    return {name: (SKILL_DIR / name).read_text(encoding="utf-8")
            for name in ("SKILL.md", "phases/s4.md", "phases/s8.md")}


def problems_of(texts: dict, evals_text: str) -> list:
    """Every key that is wrong in `texts` ({file: text}) and `evals_text`; [] when the texts are right."""
    problems = []
    for name, key in ABSENT:
        if key in texts[name]:
            problems.append(f"{name} still carries {key!r}")
    for name, key in PRESENT:
        if key not in texts[name]:
            problems.append(f"{name} lacks {key!r}")
    size = len(texts["SKILL.md"].replace("\r\n", "\n").encode("utf-8"))
    if size > SKILL_CAP:
        problems.append(f"SKILL.md is {size} bytes, over the cap of {SKILL_CAP}")
    try:
        evals = {item["id"]: item for item in json.loads(evals_text)["evals"]}
    except Exception as exc:
        return problems + [f"evals.json does not parse: {exc}"]
    for number in (18, 19, 20):
        if number not in evals:
            problems.append(f"evals.json has no eval {number}")
    names = [a.get("name") for a in (evals.get(14) or {}).get("assertions", [])]
    if "s5-in-same-window" not in names:
        problems.append("eval 14 has no assertion named 's5-in-same-window'")
    return problems


def the_unconditional_stop_is_gone_and_its_replacement_is_there() -> None:
    texts = read_texts()
    evals_text = (SKILL_DIR / "evals" / "evals.json").read_text(encoding="utf-8")
    check_eq("every key of the spec holds in the shipped texts", problems_of(texts, evals_text), [])
    check("SKILL.md is at most the cap (measured, not assumed)",
          len(texts["SKILL.md"].replace("\r\n", "\n").encode("utf-8")) <= SKILL_CAP)
    names = {a["name"] for item in json.loads(evals_text)["evals"] if item["id"] in (18, 19, 20)
             for a in item["assertions"]}
    for want in ("continues-after-gate-a", "answer-read-whole", "window-change-only-by-code", "stop-after-holds",
                 "no-window-line-with-stop", "delivery-before-window-change", "third-outcome-is-not-a-stop"):
        check(f"evals 18-20 carry the assertion {want!r}", want in names)


def the_checker_reports_what_it_should() -> None:
    """The negative control: a checker that cannot fail is indistinguishable from a broken one."""
    texts = read_texts()
    evals_text = (SKILL_DIR / "evals" / "evals.json").read_text(encoding="utf-8")

    reinserted = dict(texts, **{"SKILL.md": texts["SKILL.md"].replace(
        "Read the gate-decision answer whole: follow `next_action` in this window;",
        "After the decision is recorded, stop with one line: `<TICKET> is at S<n>;")})
    found = problems_of(reinserted, evals_text)
    check("SKILL.md with the old stop re-inserted: the stop is reported", any("stop with one line" in p for p in found), str(found))
    check("and the missing replacement is reported", any("Read the gate-decision answer whole" in p for p in found), str(found))
    print("negative control: SKILL.md with `stop with one line` re-inserted -> reported")

    without_key = dict(texts, **{"phases/s8.md": texts["phases/s8.md"].replace("go on to S9 in this window", "")})
    found = problems_of(without_key, evals_text)
    check("s8.md without its present-key: reported", any("go on to S9 in this window" in p for p in found), str(found))
    print("negative control: s8.md with `go on to S9 in this window` removed -> reported")

    cut_hint = dict(texts, **{"phases/s4.md": texts["phases/s4.md"].replace("never pipe it through `cut`, `head` or `tail`", "")})
    check("s4.md without the whole-answer rule: reported",
          any("never pipe it through" in p for p in problems_of(cut_hint, evals_text)))
    print("negative control: s4.md with the whole-answer rule removed -> reported")

    fat = dict(texts, **{"SKILL.md": texts["SKILL.md"] + "x" * SKILL_CAP})
    check("a SKILL.md over the cap: reported", any("over the cap" in p for p in problems_of(fat, evals_text)))
    print("negative control: SKILL.md over the cap -> reported")

    check("evals.json that does not parse: reported", any("does not parse" in p for p in problems_of(texts, "{not json")))
    stripped = json.dumps({"evals": [e for e in json.loads(evals_text)["evals"] if e["id"] != 19]})
    check("evals.json without eval 19: reported", any("no eval 19" in p for p in problems_of(texts, stripped)))
    print("negative control: evals.json without eval 19 -> reported")

    # Positive control of the absence keys: the old sentence DID stand in SKILL.md before this change.
    check("the key 'stop with one line' is a real phrase of the old text (it is in the re-inserted copy)",
          "stop with one line" in reinserted["SKILL.md"])


if __name__ == "__main__":
    the_unconditional_stop_is_gone_and_its_replacement_is_there()
    the_checker_reports_what_it_should()
    finish("gate continuation texts")
