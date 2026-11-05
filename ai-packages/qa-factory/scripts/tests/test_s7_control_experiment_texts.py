"""test_s7_control_experiment_texts.py - the role, phase, critic and eval texts of HF2-18 part B (S7 control experiment).

Why. On TP1-12586 the S7 rules sent both red UI tests to `APP_BUG` by default: rule 1 ("ambiguous cases
default to `APP_BUG`"), rule 2b ("the default whenever both readings are tenable") and the phase text ("a red with
`contradicts_requirement` is an `APP_BUG` by construction ... never `TEST_BUG`"). The owner's word (25.10.2026): ask
whether the same action WITHOUT the change gives the same value, before any bug. Part A (code) gave the word
`ASSERT_STRICTER` and the `control` block; this file holds the texts that tell the roles to use them.

This is the doc-dispatch witness (CLAUDE.md rule 11): the keys are the phrases of the spec
docs/tasks/specs/t-1247-hf2-18-s7-control-experiment.md section 5 (B-K1 .. B-K13) plus the Lead amendments N2, N3,
N4, N5 and the edges E14, E18, E21 and N8 (a), fixed BEFORE the texts were written; the script is committed and
carries its own NEGATIVE controls (a copy with the old sentence put back, a copy with a key taken out, a copy of the
critic with a second question, evals without eval 21, a PRESENT key that is in no file - all through `problems_of`).
The fresh round t-1343 (after the critic's verdict t-1342: B1, F1 .. F10) added the keys B1, F1a-c, F2a-b2, F4a-d, F5,
F6, F7, F10a-c and Scribe, the old-F* ABSENT rows, the one-summary COUNT and the fourth test of eval 21.

Whitespace is folded (the texts wrap near column 100); the words, the punctuation and the backticks are verbatim.

Eval 21 is a scenario for the live run (no fixture, no stand). The only runner this repository has for it is the JSON
parse below (`npm run eval:check` lives in the release repository, not here); what separates old text from new is
the key list, and the live proof of the batch carries the rest.

Runnable on its own: `python -B scripts/tests/test_s7_control_experiment_texts.py`.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, check_eq, finish  # noqa: E402

ANALYST = "agents/qa-failure-analyst.md"
S7 = "skills/qa-story/phases/s7.md"
CRITIC = "agents/qa-code-critic.md"
RUBRIC = "references/code-review-rubric.md"
STATE_EXITS = "design/state-exits.md"
S6_HANDOFF = "handoffs/s6-runner-to-analyst.yaml"
EVALS = "skills/qa-story/evals/evals.json"
SCRIBE = "agents/qa-doc-scribe.md"
FILES = (ANALYST, S7, CRITIC, RUBRIC, STATE_EXITS, S6_HANDOFF, SCRIBE)

RUBRIC_HEADING = "## An assert stricter than the requirement"
CRITIC_ITEM = "1f. **Is the assert stricter than the requirement?**"
RUBRIC_CAP = 12000        # selftest.py --limits: a size pin is a cap (builder rule 7), never "no larger than before"

# (id, file, key) - PRESENT, the spec's B-K keys verbatim.
PRESENT = (
    ("B-K1", ANALYST, "**Control experiment before an `APP_BUG` on an extra or different value.**"),
    ("B-K2a", ANALYST, "ASSERT_STRICTER"),
    ("B-K2b", S7, "ASSERT_STRICTER"),
    ("B-K2c", S7, "`ASSERT_STRICTER` → no repair, no draft, no rework"),
    ("B-K3", ANALYST, "the same action without the change under test"),
    ("B-K4", ANALYST, "no return to gate A and no rewrite of the case"),
    ("B-K5", ANALYST, "test data weaker than the case's Given is a `TEST_BUG` of the data"),
    ("B-K6", ANALYST, "`APP_BUG` when both readings are tenable, and only after the control experiment"),
    ("B-K7", ANALYST, "a control experiment the stand cannot run is named in `control` (`result: impossible`, `why`), "
                      "never read as a pass"),
    ("B-K8", S7, "A red on an extra or different value gets the control experiment first"),
    ("B-K9a", ANALYST, "`CASE_DEFECT` · `ASSERT_STRICTER`"),
    ("B-K9b", S7, "`CASE_DEFECT` · `ASSERT_STRICTER`"),
    ("B-K10a", CRITIC, CRITIC_ITEM),
    ("B-K10b", RUBRIC, RUBRIC_HEADING),
    ("B-K13", STATE_EXITS, "or `ASSERT_STRICTER` after its control experiment"),
    # Lead amendments and edges (decided before the texts, same discipline).
    ("N2", S6_HANDOFF, "A red on an extra or different value gets the control experiment first"),
    ("N3a", ANALYST, "`CASE_DEFECT` only after the control experiment (2d) showed no effect without the change"),
    ("N3b", ANALYST, "never `CASE_DEFECT`"),
    ("N3c", S7, "never `CASE_DEFECT`"),
    ("N3d", S7, "never skips the control experiment"),
    ("N8a", ANALYST, "only when EVERY difference is outside the requirement"),
    ("E14", ANALYST, "running the action again with the same change is a reproduction, not a control experiment"),
    ("E21a", ANALYST, "under `evidence/`"),
    ("E21b", S7, "under `evidence/`"),
    ("F2b", ANALYST, "`given_gap`"),
    ("Role", ANALYST, "`ASSERT_STRICTER` gets no repair and no draft"),
    ("Rule1", ANALYST, "default to `APP_BUG` after the control experiment (2d)"),
    ("Witness", ANALYST, "the control experiment's evidence file and the requirement quoted"),
    # Fresh round t-1343, after the critic's verdict t-1342 (B1, F1 .. F10).
    ("B1", ANALYST, "A judge's leaning or decided verdict on such a red, `case_defect` included, never replaces "
                    "this experiment."),
    ("F1a", ANALYST, "when it shows the effect, (a) holds and the weakness goes to `given_gap`"),
    ("F1b", ANALYST, "when it does not, the red is the data's: `TEST_BUG`"),
    ("F1d", ANALYST, "(c) no effect without the change, on data that answers the Given: the change causes it, rules 2 "
                     "and 2b as before; on weaker data the data check above decides first."),
    ("F1c", S7,"(both, weak data and the effect: `ASSERT_STRICTER` with `given_gap`)"),
    ("F2a", S7, "otherwise `APP_BUG`, or `CASE_DEFECT` by rule 2b when no effect shows without the change"),
    ("F2b2", S7, "with the requirement silent on what the assert asks"),
    ("F4a", RUBRIC, "only in `critic-findings.md`, never in the form's `findings[]`"),
    ("F4b", CRITIC, "only in `critic-findings.md`, never in the form's `findings[]`"),
    ("F4c", RUBRIC, "S7 runs its control experiment on such a red anyway (rule 2d); the note is for the reader "
                    "of the review."),
    ("F4d", CRITIC, "S7 runs its control experiment on such a red anyway (rule 2d), the note is for the reader "
                    "of the review."),
    ("F5", ANALYST, "the Left with you line shows the Thens the S5 row handed over red, the case's `R-n` and your "
                    "`control.observed`: write `observed` so a person understands it alone, and when the red is "
                    "one Then of several, say which in `observed`"),
    ("F6", ANALYST, "`without` names the change under test that was left out, never the assert or the test's "
                    "data; a run with the assert changed or removed is no experiment, it adjusts the "
                    "expectation (Role)"),
    ("F7", ANALYST, "never read as a pass (the stand, or no route you can drive: no API call and no test for "
                    "the action)"),
    ("F10a", ANALYST, "under the task's `evidence/` folder"),
    ("F10b", ANALYST, "`qa-factory/artifacts/<TICKET>/evidence/control-<label>.json`"),
    ("F10c", ANALYST, "file the contradiction by rule 2d"),
    ("Scribe", SCRIBE, "an expectation nobody confirmed, an assert stricter than its requirement"),
)

# (id, file, key) - ABSENT, the old sentences.
ABSENT = (
    ("old-2b", ANALYST, "the default whenever both"),
    ("old-s7a", S7, "is an `APP_BUG` by"),
    ("old-s7b", S7, "It is never `TEST_BUG`"),
    ("old-s6", S6_HANDOFF, "APP_BUG by construction"),
    # Fresh round t-1343: the sentences the critic's verdict t-1342 took out.
    ("old-F1", ANALYST, "Data also weaker than the Given: still"),
    ("old-F1d", ANALYST, "(c) no effect without the change: the change causes it"),
    ("old-F2a", S7,"the rest stays `APP_BUG`"),
    ("old-F2b", S7, "anything else is an `APP_BUG`"),
    ("old-F4a", RUBRIC, "so S7 can put the red"),
    ("old-F4b", CRITIC, "is a note with no `cause`, for S7"),
    ("old-F5", ANALYST, "the row names the failing Then"),
    ("old-F10", ANALYST, "file the contradiction as `APP_BUG`"),
)

# (id, file, key, how many times) - COUNT: one question, one place (E18); one summary, one place (F2).
COUNT = (
    ("B-K11a", CRITIC, "stricter than the requirement", 1),
    ("B-K11b", RUBRIC, RUBRIC_HEADING, 1),
    ("F2-one-summary", S7, "with the requirement silent on what the assert asks", 1),
)

EVAL_ASSERTIONS = ("control-before-app-bug", "stricter-assert-left-with-you", "no-gate-a-return",
                   "seed-weaker-is-test-bug", "both-readings-after-control", "control-impossible-named",
                   "no-case-defect-after-control", "weak-seed-and-stricter-given-gap")


def fold(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def read_texts() -> dict:
    return {name: (PLUGIN_ROOT / name).read_text(encoding="utf-8") for name in FILES}


def read_evals() -> str:
    return (PLUGIN_ROOT / EVALS).read_text(encoding="utf-8")


def eval_problems(evals_text: str) -> list:
    """Every way eval 21 is wrong in `evals_text`; [] when it is right."""
    try:
        evals = {item["id"]: item for item in json.loads(evals_text)["evals"]}
    except Exception as exc:
        return [f"evals.json does not parse: {exc}"]
    item = evals.get(21)
    if item is None:
        return ["evals.json has no eval 21"]
    problems = []
    for field in ("prompt", "expected_output"):
        if not str(item.get(field) or "").strip():
            problems.append(f"eval 21 has no {field}")
    if item.get("files") != []:
        problems.append("eval 21 'files' is not [] (the form of evals 16-20: no fixture, no stand)")
    named = {}
    for a in item.get("assertions") or []:
        if not (str(a.get("name") or "").strip() and str(a.get("description") or "").strip()):
            problems.append(f"eval 21 has an assertion without a name or a description: {a!r}")
        named[a.get("name")] = a
    for want in EVAL_ASSERTIONS:
        if want not in named:
            problems.append(f"eval 21 has no assertion named {want!r}")
    prompt = str(item.get("prompt") or "")
    for word in ("contradicts_requirement", "alias", "resource_id", "assistant_ids", "username"):
        if word not in prompt:
            problems.append(f"eval 21 prompt lacks {word!r}")
    expected = str(item.get("expected_output") or "")
    for word in ("ASSERT_STRICTER", "TEST_BUG", "APP_BUG", "impossible", "Left with you", "Test four", "given_gap"):
        if word not in expected:
            problems.append(f"eval 21 expected_output lacks {word!r}")
    return problems


def problems_of(texts: dict, evals_text: str, extra_present: tuple = ()) -> list:
    """Every key that is wrong in `texts` ({file: text}) and `evals_text`; [] when the texts are right.

    `extra_present` is more PRESENT rows, (id, file, key): the negative control of a key that is in no file."""
    problems = []
    folded = {name: fold(text) for name, text in texts.items()}
    for item, name, key in PRESENT + tuple(extra_present):
        if fold(key) not in folded[name]:
            problems.append(f"{item}: {name} lacks {key!r}")
    for item, name, key in ABSENT:
        if fold(key) in folded[name]:
            problems.append(f"{item}: {name} still carries {key!r}")
    for item, name, key, want in COUNT:
        got = folded[name].count(fold(key))
        if got != want:
            problems.append(f"{item}: {name} carries {key!r} {got} times, want {want}")
    size = len(texts[RUBRIC].replace("\r\n", "\n").encode("utf-8"))
    if size > RUBRIC_CAP:
        problems.append(f"{RUBRIC} is {size} bytes, over the cap of {RUBRIC_CAP}")
    # E18, positional: the new rubric section stands right after "An expected value with no source" and
    # before the smells table; the critic's 1f stands after 1e and before step 2.
    rubric = texts[RUBRIC]
    order = [rubric.find(h) for h in ("## An expected value with no source", RUBRIC_HEADING, "## STLC's smells")]
    if -1 in order or order != sorted(order):
        problems.append(f"{RUBRIC}: the new section is not between 'An expected value with no source' and "
                        "'STLC's smells'")
    critic = texts[CRITIC]
    order = [critic.find(h) for h in ("\n1e. ", "\n" + CRITIC_ITEM, "\n2. Reuse")]
    if -1 in order or order != sorted(order):
        problems.append(f"{CRITIC}: item 1f is not between 1e and step 2")
    return problems + eval_problems(evals_text)


def the_keys_hold_in_the_shipped_texts() -> None:
    texts, evals_text = read_texts(), read_evals()
    found = problems_of(texts, evals_text)
    for line in found:
        print("  PROBLEM:", line)
    check_eq(f"every key holds in the shipped texts ({len(PRESENT)} PRESENT, {len(ABSENT)} ABSENT, {len(COUNT)} "
             f"COUNT, the rubric cap, the positions, eval 21)", found, [])


def the_checker_reports_what_it_should() -> None:
    """The negative controls: a checker that cannot fail is indistinguishable from a broken one."""
    texts, evals_text = read_texts(), read_evals()

    old2b = dict(texts, **{ANALYST: texts[ANALYST] + "\nWhen the register backs the case it is `APP_BUG`, the default whenever both\n"})
    check("analyst with 'the default whenever both' put back: reported",
          any("the default whenever both" in p for p in problems_of(old2b, evals_text)))
    print("negative control: analyst with the old 2b sentence re-inserted -> reported")

    no_k8 = dict(texts, **{S7: texts[S7].replace("A red on an extra or different value gets the control experiment first", "")})
    check("s7.md without B-K8: reported",
          any(p.startswith("B-K8") for p in problems_of(no_k8, evals_text)))
    print("negative control: s7.md with B-K8 removed -> reported")

    old_s7 = dict(texts, **{S7: texts[S7] + "\nis an `APP_BUG` by construction. It is never `TEST_BUG`\n"})
    found = problems_of(old_s7, evals_text)
    check("s7.md with the old 'by construction' sentence: both old keys reported",
          any(p.startswith("old-s7a") for p in found) and any(p.startswith("old-s7b") for p in found))
    print("negative control: s7.md with the old sentence re-inserted -> reported")

    old_yaml = dict(texts, **{S6_HANDOFF: texts[S6_HANDOFF] + "\n  - \"is an APP_BUG by construction\"\n"})
    check("the S6 handoff with 'APP_BUG by construction' put back: reported",
          any(p.startswith("old-s6") for p in problems_of(old_yaml, evals_text)))
    print("negative control: s6-runner-to-analyst.yaml with the old line re-inserted -> reported")

    two_items = dict(texts, **{CRITIC: texts[CRITIC] + "\n1g. Is the Then stricter than the requirement?\n"})
    check("critic with a second 'stricter than the requirement': COUNT reports",
          any(p.startswith("B-K11a") for p in problems_of(two_items, evals_text)))
    print("negative control: critic with a second question -> COUNT reported")

    two_sections = dict(texts, **{RUBRIC: texts[RUBRIC] + "\n" + RUBRIC_HEADING + "\n"})
    check("rubric with the section heading twice: COUNT reports",
          any(p.startswith("B-K11b") for p in problems_of(two_sections, evals_text)))
    print("negative control: rubric with a second section -> COUNT reported")

    moved = dict(texts, **{RUBRIC: texts[RUBRIC].replace(RUBRIC_HEADING, "## Moved") + "\n" + RUBRIC_HEADING + "\n"})
    check("rubric with the section moved to the end: the position is reported",
          any("is not between" in p for p in problems_of(moved, evals_text)))
    print("negative control: rubric section moved -> position reported")

    fat = dict(texts, **{RUBRIC: texts[RUBRIC] + "x" * RUBRIC_CAP})
    check("a rubric over the cap: reported", any("over the cap" in p for p in problems_of(fat, evals_text)))
    print("negative control: rubric over the cap -> reported")

    check("evals.json that does not parse: reported", any("does not parse" in p for p in problems_of(texts, "{not json")))
    try:
        stripped = json.dumps({"evals": [e for e in json.loads(evals_text)["evals"] if e["id"] != 21]})
    except Exception:
        stripped = json.dumps({"evals": []})
    check("evals.json without eval 21: reported", any("no eval 21" in p for p in problems_of(texts, stripped)))
    print("negative control: evals.json without eval 21 -> reported")

    try:
        data = json.loads(evals_text)
        for e in data["evals"]:
            if e["id"] == 21:
                e["assertions"] = [a for a in e["assertions"] if a["name"] != "control-impossible-named"]
        lacking = json.dumps(data)
    except Exception:
        lacking = json.dumps({"evals": [{"id": 21, "prompt": "p", "expected_output": "e", "files": [], "assertions": []}]})
    check("eval 21 without one named assertion: reported",
          any("control-impossible-named" in p for p in problems_of(texts, lacking)))
    print("negative control: eval 21 without control-impossible-named -> reported")

    no_b1 = dict(texts, **{ANALYST: fold(texts[ANALYST]).replace("never replaces this experiment.", "")})
    check("analyst without the judge sentence (B1): reported", any(p.startswith("B1:") for p in problems_of(no_b1, evals_text)))
    print("negative control: analyst without the judge sentence -> reported")

    two_summaries = dict(texts, **{S7: texts[S7] + "\nwith the requirement silent on what the assert asks\n"})
    check("s7.md with the summary written twice: COUNT reports",
          any(p.startswith("F2-one-summary") for p in problems_of(two_summaries, evals_text)))
    print("negative control: s7.md with a second copy of the summary -> COUNT reported")

    old_note = dict(texts, **{RUBRIC: texts[RUBRIC] + "\nOne note, without a `cause`, so S7 can put the red\n"})
    check("rubric with the old note text put back: reported", any(p.startswith("old-F4a") for p in problems_of(old_note, evals_text)))
    print("negative control: rubric with the old note text -> reported")

    no_scribe = dict(texts, **{SCRIBE: texts[SCRIBE].replace("an assert stricter than its requirement", "")})
    check("scribe without the new kind: reported", any(p.startswith("Scribe:") for p in problems_of(no_scribe, evals_text)))
    print("negative control: scribe without the new kind -> reported")

    data = json.loads(evals_text)
    for e in data["evals"]:
        if e["id"] == 21:
            e["assertions"] = [a for a in e["assertions"] if a["name"] != "weak-seed-and-stricter-given-gap"]
    check("eval 21 without the test-four assertion: reported",
          any("weak-seed-and-stricter-given-gap" in p for p in problems_of(texts, json.dumps(data))))
    print("negative control: eval 21 without weak-seed-and-stricter-given-gap -> reported")

    # A key that is in no file: the same problems_of reports it as a missing PRESENT key.
    zzz = ("zzz", ANALYST, "zzz-not-in-any-file")
    check("a PRESENT key that is in no file: reported by problems_of",
          any(p.startswith("zzz:") for p in problems_of(texts, evals_text, extra_present=(zzz,))))
    print("negative control: 'zzz-not-in-any-file' as a PRESENT key -> reported")


if __name__ == "__main__":
    the_keys_hold_in_the_shipped_texts()
    the_checker_reports_what_it_should()
    finish("S7 control experiment texts (HF2-18 B)")
