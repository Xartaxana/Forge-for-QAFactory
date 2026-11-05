"""t-219, the texts half: the role texts say what the blocked-window code now demands (FR-38, FR-34, P20).

A stand block is the one road on which a RED test can leave the window as "not a failure": the window code
cannot tell the stand from the product (E4), so the guards are text - the automator's `detail` naming the
control it did, the critic reading `last_run.reason` against the change. A text nobody can check is a wish,
so this is the key-presence witness of those sentences.

THE KEYS were fixed BEFORE the texts were written, and the first eight groups below are quoted VERBATIM from
the DoD of the dispatch (not chosen after the fact). A few items carry no quoted phrase in the DoD (the
refusal the automator will meet, the one pointer in the charter, the three handoff fields, the row shape);
their keys were fixed in this file before the texts too and are marked `# builder-chosen` - the acceptor
may replace them. Whitespace runs (a line break of a soft-wrapped paragraph) count as one space on both sides.

The NEGATIVE CONTROLS at the end run the same reader over a scratch copy with one key deliberately absent
and require it to fail naming that key: a witness that cannot fail is indistinguishable from a broken one.
"""
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, check, check_eq, cleanup, finish, temp_dir  # noqa: E402

AUTOMATOR = "agents/qa-automator.md"
CRITIC = "agents/qa-code-critic.md"
RUBRIC = "references/code-review-rubric.md"
HANDOFF = "handoffs/s5-automator-to-critic.yaml"
CONTRACT = "references/artifact-contract-automation.md"
SLICE = "references/slices/qa-automator/artifact-contract-automation.md"
FILES = (AUTOMATOR, CRITIC, RUBRIC, HANDOFF, CONTRACT, SLICE)

# (file, key, what it protects) - verbatim from the DoD
KEYS = (
    (AUTOMATOR, "instance_ids: every blocked instance", "(1) a blocked row names EVERY blocked instance"),
    (AUTOMATOR, "a red that ran needs detail", "(2) a red that ran carries `detail`, the control it did"),
    (AUTOMATOR, "a product answer is never a stand block: a wrong status code, a wrong body, a failed assertion "
                "is red, not blocked", "(2) P20/FR-34: the product's answer is red"),
    (AUTOMATOR, "rung 5", "(3) the P19 ladder: blocked by this stand = written, a person runs it elsewhere"),
    (RUBRIC, "ran red: read the reason against the change", "(5) the critic reads `last_run.reason` against the change"),
    (RUBRIC, "unverified is not a pass", "(6) `unverified` never covers a test that ran red"),
    (CONTRACT, "a window where every instance is blocked by the stand closes with the verdict blocked — it is a "
               "recorded null outcome, not a missing one", "(9) FR-23: the null outcome is recorded"),
    (CONTRACT, "the person sees `ran red: <reason>` beside every blocked row that ran", "(9) gate B shows the red"),
    # builder-chosen: the shape the DoD names without quoting it
    # 12b (t-121) cut the sentence «The window refuses a row that "says nothing about what stopped it" while its
    # test "ran and failed"» from item 5b: the refusal says it in its own words when it is met (acceptance.py,
    # REFUSED_NO_DETAIL), and the duty - a red that ran carries a `detail` naming the control - lives in the slice the
    # automator is injected with (and in 5b's "a red that ran needs detail", key 2 above). So the pin reads the slice.
    (SLICE, "`detail` — required when the instance ran and failed", "(4) the duty the refusal enforces, in the slice the automator is injected with"),
    (SLICE, "the control that shows the stand, not the product, blocked it", "(4) ... and what that `detail` names"),
    (RUBRIC, "last_run.reason", "(5) the field the critic reads"),
    (RUBRIC, "A blocked row that ran red", "(7) the rubric rule the charter points at (its heading)"),
    (CONTRACT, "one row per case", "(9) the `blocked_by_env` row shape: one per case"),
    (CONTRACT, "`instance_ids[]` (every instance the stand blocked)", "(9) ... with the list of instances"),
    (CONTRACT, "`detail` — required when the instance ran and failed", "(9) ... and the detail of a red that ran"),
)
HANDOFF_FIELDS = ("instance_ids", "detail", "remedy")  # (8), builder-chosen: one line each saying what the critic checks


def squash(text: str) -> str:
    return " ".join(text.split())


def read(root: Path, rel: str) -> str:
    try:
        return (root / rel).read_text(encoding="utf-8")
    except OSError:
        return ""


def refusal_item(text: str) -> str:
    """The automator's item 5b: from `5b.` to the next numbered item."""
    found = re.search(r"^5b\..*?(?=^6\.)", text, re.S | re.M)
    return found.group(0) if found else ""


def handoff_block(text: str) -> list:
    """The lines of the `unresolved:` section of the handoff form."""
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith("unresolved:")), None)
    if start is None:
        return []
    out = []
    for ln in lines[start + 1:]:
        if ln and not ln.startswith((" ", "#")):
            break
        out.append(ln)
    return out


def failures(root: Path) -> list:
    """What is missing under `root`, one line per gap; empty = every key is there."""
    texts = {rel: squash(read(root, rel)) for rel in FILES}
    found = []
    for rel, key, why in KEYS:
        if squash(key) not in texts[rel]:
            found.append(f"{rel}: missing `{key}` - {why}")
    # (4) the paraphrase of the refusal names no script (the person-facing rule's spirit, kept for the role too)
    item = refusal_item(read(root, AUTOMATOR))
    if not item:
        found.append(f"{AUTOMATOR}: item 5b not found")
    elif re.search(r"\w\.py\b", item):
        found.append(f"{AUTOMATOR}: item 5b names a script - the refusal is paraphrased without script names")
    # (7) ONE pointer in the charter; the rule itself lives in the rubric only (a rule in both pays twice)
    charter = squash(read(root, CRITIC))
    pointers = charter.count("A blocked row that ran red")
    if pointers != 1:
        found.append(f"{CRITIC}: the pointer to the rubric rule is there {pointers} times, expected exactly 1")
    for key in ("ran red: read the reason against the change", "unverified is not a pass"):
        if key in charter:
            found.append(f"{CRITIC}: carries `{key}` - the rule lives in the rubric, the charter only points at it")
    # (8) the three fields on the blocked rows, each with a line saying what the critic checks
    block = handoff_block(read(root, HANDOFF))
    for field in HANDOFF_FIELDS:
        lines = [ln for ln in block if re.match(rf"\s+{field}:", ln)]
        if not lines:
            found.append(f"{HANDOFF}: the `unresolved` row has no `{field}` field")
        elif not any("the critic checks" in ln for ln in lines):
            found.append(f"{HANDOFF}: `{field}` does not say what the critic checks")
    return found


def scratch_copy(without: tuple = ()) -> Path:
    """A scratch copy of the five files; `without` = (file, text) pairs removed from it."""
    root = temp_dir("qa-blocked-texts-")
    for rel in FILES:
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PLUGIN_ROOT / rel, target)
    for rel, text in without:
        path = root / rel
        body = path.read_text(encoding="utf-8")
        assert squash(text) in squash(body), f"the control cannot remove what is not there: {text}"
        path.write_text(re.sub(r"\s+".join(map(re.escape, text.split())), "", body, count=1), encoding="utf-8")
    return root


def main() -> None:
    got = failures(PLUGIN_ROOT)
    check_eq("the package texts carry every key", got, [])
    for gap in got:
        print("  - " + gap)

    # --- negative controls: one key deliberately absent -> the reader fails, naming it
    for rel, key, why in (KEYS[0], KEYS[2], KEYS[4], KEYS[7]):
        root = scratch_copy(((rel, key),))
        try:
            # what the package itself already lacks is not the control's business: only the NEW lines count
            lost = [line for line in failures(root) if line not in got]
            check(f"control: without `{key[:48]}` the witness fails", bool(lost), "no failure reported")
            check("control: and names it", any(key in line for line in lost), "; ".join(lost)[:200])
            check("control: and only it", len(lost) == 1, "; ".join(lost)[:300])
        finally:
            cleanup(root)
    root = scratch_copy()
    try:
        path = root / HANDOFF
        text = path.read_text(encoding="utf-8")
        path.write_text(re.sub(r"(?m)^(\s+)remedy:", r"\1remedy_gone:", text), encoding="utf-8")
        lost = failures(root)
        check("control: a handoff row without `remedy` fails, naming the field",
              any("no `remedy` field" in line for line in lost), "; ".join(lost)[:200])
        shutil.copyfile(PLUGIN_ROOT / HANDOFF, path)
        path = root / CRITIC
        path.write_text(path.read_text(encoding="utf-8") + "\nunverified is not a pass\n", encoding="utf-8")
        lost = failures(root)
        check("control: the rule restated in the charter fails (a rule in both pays twice)",
              any("the rule lives in the rubric" in line for line in lost), "; ".join(lost)[:200])
        shutil.copyfile(PLUGIN_ROOT / CRITIC, path)
        path = root / AUTOMATOR
        path.write_text(path.read_text(encoding="utf-8").replace("5b.", "5b. (see manifest_put.py)", 1), encoding="utf-8")
        lost = failures(root)
        check("control: a script name in the refusal paraphrase fails",
              any("names a script" in line for line in lost), "; ".join(lost)[:200])
    finally:
        cleanup(root)
    finish("test_blocked_by_env_texts")


if __name__ == "__main__":
    main()
