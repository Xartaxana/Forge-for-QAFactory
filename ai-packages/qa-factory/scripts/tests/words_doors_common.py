#!/usr/bin/env python3
"""Every door that carries a person's words names the FILE form (legacy-2406 wave 3, node W3-D-A).

W3-W1 made a person's words travel by file (`--words-file`, one reader: `person_words.read`),
because cmd.exe stops a command line at its first line break and an inline answer is recorded
cut (M30). About 45 refusals, hints and docs still told the orchestrator to pass the words inline
(`waiver.py ... --decision "<their words>"`): a door contradicting the rule the roles read (FR-37),
a second mechanism for one job (FR-17). This is the class fix: ONE renderer
(`person_words.door`), ONE detector (here), and a door-opening test per refusal a program prints.

  (a) the detector greps for the PROBLEM (an inline words part after a recording command), over
      the string constants of `scripts/*.py` and over the text of skills / references / design /
      handoffs / agents. Sites that belong to other open nodes are in PENDING: a hit there is
      printed, not failed; a pending file found clean says "clean now: remove <path>".
  (b) FR-2: every refusal a program prints is produced from the REAL code, the command is taken
      out of the printed backtick span (never retyped), only named placeholders are filled, the
      REAL CLI is run, and the refusing code then no longer refuses.
  (c) a story in flight: overrides recorded under the keywords the OLD texts advised still pass
      the new texts.
  (d) Windows only: one door through the real launcher (hooks/run-py.cmd).
"""
# Shared helpers of test_words_doors.py, split by tools/test_split.py (TD-11c).
import io
import json
import os
import re
import shlex
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness import PLUGIN_ROOT, SCRIPTS, check, check_eq, check_in, run_script, temp_project, use_project
sys.path.insert(0, str(SCRIPTS))
import test_obligation_join as OJ  # noqa: E402


WIN = os.name == "nt"


LAUNCHER = PLUGIN_ROOT / "hooks" / "run-py.cmd"


FLAG = "--words-file"


WORDS = "Go on.\n\nKeep it local - \"do not publish\" to Jira.\n"


# --- (a) the detector --------------------------------------------------------------------------

# The recording commands, then up to 300 characters of the same command (no backtick or bare pipe,
# so one command in one markdown span or table cell; an ESCAPED pipe `\|` is a character of the
# command - a table cell cannot hold a bare one, and `--gate A\|B` hid the door behind it), then a
# words option whose value is typed on the line: a quote, a backslash-quote (yaml / json) or a
# `<placeholder>`.
INLINE_DOOR = re.compile(
    r'''(waiver\.py|gate-decision|--operation release|archive_task\.py|project_decisions\.py'''
    r'''|accept-gap|review --record|onboarding_notes\.py|story_step\.py decide)(?:\\\||[^`|]){0,300}?\s(--decision|--words|--text|--note)\s+\\?["'<]''')


DRIVER_KEY = "scripts/story_run.py"  # the one key of the whole driver set (the entry file and its driver_*.py parts)


PENDING = {
    # The remedy of a tracker route that is not proven: upstream's text, kept by decision (spec
    # t-428: the readiness texts name no script of ours, so ours' `door(..., for_person=True)` is
    # not carried).
    "scripts/readiness.py": ('waiver.py --stage S1 --block "tracker route" --decision "',),
    # The driver's own texts, upstream's, shown to a person or put to the conductor: the note about a
    # stand-gap line it could not read; the mode-switch question (`{self.scripts / 'waiver.py'}` is read
    # as `waiver.py`: `_placeholder`, the blind spot of the first version); the two stand questions.
    DRIVER_KEY: ('waiver.py --task <T> --stage <stage> --block "<block>" --decision "',
                             'waiver.py" --task {} --stage {} --block "mode switch" --decision "',
                             ),      # C1-6b took off the two stand questions: their free-words prompts hand the words by `--words-file`
    "skills/qa-story/phases/s5.md": ('waiver.py --task <TICKET> --stage S5 --block "stand not confirmed" --decision "',),
    # Two doors that were converted to the file form and are back to upstream's inline text, because an
    # upstream test pins that text: the S9 report-check door (test_story_closed.py) and the mode-switch
    # door of `run_mode_refusal` (test_package_generation.py). The matched text is as the scan renders it
    # (`{}` for a formatted value; `run_mode_refusal` spells the script through `RP.script_command`, so its
    # placeholder renders as the bare `waiver.py`, with no closing quote after the name).
    "scripts/stage_done.py": ('waiver.py --task {} --stage S9 --block "{}" --decision "',),
    "scripts/story_step.py": ('waiver.py --task {} --stage {} --block "{}" --decision "',),
}


# The same problem written as prose, with the option named and no value shown (`--words`,
# `... --gate A --words with their words`): the shape the evals and a conductor table use. The
# lookahead keeps `--words-file` out; the same command stretch rule applies.
BARE_DOOR = re.compile(
    r'''(waiver\.py|gate-decision|--operation release|archive_task\.py|project_decisions\.py'''
    r'''|accept-gap|review --record|onboarding_notes\.py|story_step\.py decide)(?:\\\||[^`|]){0,300}?\s(--decision|--words|--text|--note)(?![-\w])''')


def normalised(text: str) -> str:
    return " ".join(text.split())


def hits_in(text: str) -> list:
    """The inline doors in one text, whitespace-normalised: each as the matched excerpt. A value
    typed on the line first; then a bare option name that no such hit already covers."""
    flat = normalised(text)
    quoted = list(INLINE_DOOR.finditer(flat))
    found = [match.group(0) for match in quoted]
    for match in BARE_DOOR.finditer(flat):
        if not any(hit.start() <= match.start() < hit.end() for hit in quoted):
            found.append(match.group(0))
    return found


# --- (b) FR-2: the printed door opens ------------------------------------------------------------

SPAN = re.compile(r"`([^`]*)`")


def project_env(root: Path) -> dict:
    return dict(os.environ, CLAUDE_PROJECT_DIR=str(root), PYTHONDONTWRITEBYTECODE="1")


def door_of(text: str) -> str:
    """The waiver command in the LAST backtick span of a printed text that holds one."""
    spans = [s for s in SPAN.findall(text) if "waiver.py" in s]
    return spans[-1] if spans else ""


def open_door(root: Path, text: str, ticket: str, stage: str, head: str = ""):
    """Run the command printed in `text` through the real waiver.py: the span is taken as printed,
    only the named placeholders are filled, the words go to a UTF-8 file under state/words/."""
    span = door_of(text)
    check_in("the printed door is the file form", FLAG, span)
    if FLAG not in span:
        return None, [], ""
    tail = span[span.index(FLAG):]
    check("and ends with a file placeholder",
          tail in (f"{FLAG} <file>", f"{FLAG} <file with your words>"), tail)
    argv = []
    for token in shlex.split(span[:span.index(FLAG)]):
        for placeholder, value in (("<TICKET>", ticket), ("<T>", ticket), ("<id>", ticket),
                                   ("<S>", stage), ("<part of the line>", head),
                                   ("<the finding's tag, or its whole id>", head)):
            token = token.replace(placeholder, value)
        argv.append(token)
    left = [t for t in argv if "<" in t and ">" in t]
    check_eq("no placeholder is left unnamed", left, [])
    check_eq("the command is waiver.py", argv[0], "waiver.py")
    words = root / "qa-factory" / "artifacts" / ticket / "state" / "words" / "door.txt"
    words.parent.mkdir(parents=True, exist_ok=True)
    words.write_bytes(WORDS.encode("utf-8"))  # bytes: write_text would turn \n into \r\n on Windows
    done = run_script(argv[0], *argv[1:], FLAG, str(words), cwd=root, env=project_env(root))
    return done, argv, str(words)


def overrides_of(root: Path, ticket: str) -> list:
    path = root / "qa-factory" / "artifacts" / ticket / "pipeline.json"
    return json.loads(path.read_text(encoding="utf-8")).get("stage_overrides") or []


def recorded(label: str, done, root: Path, ticket: str, stage: str, block: str) -> None:
    check(f"{label}: the real waiver.py records the printed door (exit 0)",
          done is not None and done.returncode == 0,
          "" if done is None else f"{done.returncode} {done.stdout} {done.stderr}")
    mine = [o for o in overrides_of(root, ticket) if o.get("match") == block and o.get("stage") == stage]
    check_eq(f"{label}: one override of exactly that block, with the person's words from the file",
             [o.get("decision") for o in mine], [WORDS.strip()])


def captured(call):
    """(returned value, stdout, stderr) of an in-process call."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        value = call()
    return value, out.getvalue(), err.getvalue()


def story_with(root: Path, ticket: str, stages: dict) -> Path:
    task = root / "qa-factory" / "artifacts" / ticket
    task.mkdir(parents=True, exist_ok=True)
    (task / "pipeline.json").write_text(json.dumps({"ticket": ticket, "stages": stages}), encoding="utf-8")
    return task


def critic_story(root: Path) -> None:
    task = story_with(root, "QA-1", {"S4": {"status": "running"}})
    folder = task / "work" / "test-cases" / "workflows"
    folder.mkdir(parents=True)
    (folder / "critic-findings.md").write_text("# Critic findings\n\nVerdict: reject.\n", encoding="utf-8")


def plan_story(root: Path) -> None:
    task = story_with(root, "QA-1", {"S3": {"status": "running"}})
    (task / "work").mkdir()
    (task / "work" / "test-plan.json").write_text(json.dumps({"rows": [{"id": "TS-1"}]}), encoding="utf-8")


def s5_story(root: Path) -> None:
    task = root / "qa-factory" / "artifacts" / OJ.TICKET
    (task / "work" / "test-cases").mkdir(parents=True)
    (task / "work" / "test-plan.json").write_text(json.dumps({"rows": OJ.PLAN_ROWS}), encoding="utf-8")
    for case, row in (("TC-005", "TS-1"), ("TC-006", "TS-2")):
        (task / "work" / "test-cases" / f"{case}.md").write_text(OJ.CASE_MD.format(case=case, row=row),
                                                               encoding="utf-8")
    (task / "work" / "automation-manifest.json").write_text(json.dumps({
        "tests": [{"case": "TC-005", "file": "tests/t.py", "instance_id": "test_five",
                   "covers": ["TC-005"], "status": "green"}],
        "obligation_bindings": [{"obligation_id": "OB-1", "instance_ids": ["test_five"]}]}), encoding="utf-8")
    (task / "pipeline.json").write_text(json.dumps(
        {"ticket": OJ.TICKET, "stages": {"S5": {"status": "running"}}}), encoding="utf-8")


# --- (b) FR-2 for the controller's own refusals (legacy-2406 wave 3, node W3-D-B) -----------------
# The controller printed `waiver.py ... --decision "<their words>"` in nine places, the stage guard's
# own hint in a tenth, a release door in two more (`next` and the spawn guard), and a gate-decision
# door in a thirteenth. Every one is produced here from the REAL code, the command is taken from the
# printed text, the REAL CLI is run with a words file, and the refusing code then no longer refuses.

TICKET = "QA-1"


def ctrl_project(prefix: str):
    """(project root, task root): a controller story lives where waiver.py looks for it."""
    root = temp_project(prefix)
    use_project(root)
    task = root / "qa-factory" / "artifacts" / TICKET
    task.mkdir(parents=True)
    return root, task


def refused_text(call) -> str:
    """The message of a refusal the controller raises, or '' when the call went through."""
    from event_store import StateConflict
    try:
        call()
    except (StateConflict, ValueError) as exc:
        return str(exc)
    return ""


def critic_review(c, task, name, scope):
    """The code critic's re-review the way a real one ends: it leaves its findings file. A story that came through S5 has its manifest
    on disk, and with one the controller demands the findings receipt at the critic's accept (C4-1 fixtures)."""
    import test_controller_state as BASE
    import test_s5_process as S5
    S5.dispatch(c, task, name, role="qa-code-critic", scope=scope, accept=False)
    c.apply("accept", {"id": name, "status": "accepted", "stage_complete": False, "unresolved": True,
                       "reason": "the window's repair round is still open",
                       "evidence_refs": [S5.evidence(task, name + ".txt"), BASE.evidence_ref(task, name + "-findings.md", "# findings")],
                       "idempotency_key": name + "-ok"})


def story_pipeline(task: Path) -> None:
    """waiver.py records only into a story that has a pipeline.json; the controller does not write
    one itself in these fixtures. Written AFTER the refusal, with every stage done, so it adds no
    refusal of the stage guard's own."""
    path = task / "pipeline.json"
    if not path.is_file():
        path.write_text(json.dumps({"ticket": TICKET, "stages": {f"S{n}": {"status": "done"} for n in range(10)}}),
                        encoding="utf-8")
