"""The stub role of the dry world (P1-b spec section 4.1, node N0): the executable the REAL driver runs in place of `claude -p`.

    STORY_RUN_CLAUDE=<this file>      the driver runs `python dry_stub.py <the arguments of claude -p>` (a `.py` path, as the tests' stubs)
    python -B dry_stub.py --selftest  the table of cases of the stub and of `dry_world.load_types()` (the only local run)

A role call: the stub reads the handover form the controller wrote (`work/handoffs/<dispatch>.yaml`), fills it with the P1-a filler
(`form_filler.fill_form`, the contract named in the form's own `contract:` line, the verdict from the row's control or the
vocabulary's first word), writes every output of the stage whose writer is THIS role with `fill_artifact`, and runs the command the
role would run for an output code builds from it. Everything the filler cannot fill is a `live_only` row of the stub's journal with
its reason - never a hand-written text (E13). The stub decides nothing: verdict, result text and the moves of a conductor come from
the row's control (`dry-stub-control.json`) or the closed list the prompt itself offers.

The journal `state/dry-stub.jsonl` (written only here) starts with one line holding the value of STORY_RUN_CLASS the stub saw: the
walker checks it before the first step (E18) - a dry run is never counted as a live one.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import harness  # noqa: E402
import story_run_common as T  # noqa: E402

COMMANDS = {"context_bundle.py": ["--manifest", "{task_root}/work/context-manifest.json", "--output", "{task_root}/work/context-bundle.json",
                                      "--root", "{task_root}"]}
# The commands a role runs that BUILD a file code owns but that is no output of the stage (the scout's source collection: skills/qa-story/phases/s1.md
# "Source collection", the one writer of work/source-inventory.json is ticket_adapter.py). Only a step that decides nothing is here: recording the task is
# a read by the tracker's own client; the judging of a mentioned ticket (`assess`) is the role's and stays with no step (E13).
ROLE_STEPS = {"qa-scout": [("work/source-inventory.json", "ticket_adapter.py",
                            ["collect", "{task}", "--relation", "task", "--output", "{task_root}/work/source-inventory.json", "--summary"])]}
MOVE_LINE =re.compile(r"^- `(\w+)`(?: — token `([^`]+)`)?;")
FORM_CONTRACT = re.compile(r"^contract:\s*(\S+)", re.M)
FORM_STAGE = re.compile(r"^stage:\s*(\S+)", re.M)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_moves(prompt: str) -> list:
    """`[(move, token)]` of the section `## Moves open here` of a conductor's prompt (`no_move.moves_section`): the moves a person may be
    offered. The section is read as the prompt prints it; no section is no move (the caller says so, it never guesses one)."""
    moves, inside = [], False
    for line in prompt.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## Moves open here"
        elif inside:
            found = MOVE_LINE.match(line)
            if found and found.group(2):
                moves.append((found.group(1), found.group(2)))
    return moves


STUB_ONLY = ("variant", "execute")        # keys of a row's `conductor` control the stub itself reads; they are never part of the verdict it prints


def move_option(move: str, token: str) -> dict:
    """One option of an `ask_person` answer for an open move, every line from the move's own row of conductor-actions.json (`says`, and the price lines
    `factory` / `person` / `delivery` resolved by `no_move.price_row`, the one resolution): no text of the stub's own. A row that does not resolve is a
    `KitError` naming the move."""
    import hooklib
    import no_move as NM
    row = NM.move_rows().get(move)
    if not row or not str(row.get("says") or "").strip():
        raise KitError(f"references/conductor-actions.json: no move `{move}` with a `says`; the prompt offered it")
    try:
        priced = NM.price_row(NM.data(), (hooklib.load_ref_json(NM.VERDICTS_FILE) or {}).get("words") or {}, row, f"moves.{move}")
    except NM.DataUnreadable as exc:
        raise KitError(f"references/conductor-actions.json: the price row of `{move}` does not resolve ({exc})") from None
    return {"token": token, "move": move, "says": str(row["says"]).strip(), "factory": priced["factory"], "person": priced["person"],
            "story": {"delivery": str(row.get("delivery") or "")}}


def conductor_verdict(prompt: str, control: dict) -> dict:
    """The conductor stub, deterministic. A row's `conductor` control that names an `action` other than `ask_person`, or carries its own `options`, is the
    verdict as written (minus the keys the stub reads itself, `STUB_ONLY`). Otherwise `ask_person` offering EVERY open move of the prompt's own list, or
    only those the row's `variant` names (a token, or a list of tokens; one the prompt does not offer is `stop` naming it, never an invented option),
    each option priced from the move's row; `why_person`, `checked`, `question`, `did` come from the row, else from the defaults of RN1-9. No open move
    in the prompt is `stop` naming that the prompt offered none."""
    row = control.get("conductor") or {}
    if row.get("options") or row.get("action") not in (None, "ask_person"):
        return {k: v for k, v in row.items() if k not in STUB_ONLY}
    if row.get("execute") and not row.get("action"):
        return {"action": "continue", "did": f"stub: ran the move {row['execute'].get('move')}", "question": ""}
    moves = parse_moves(prompt)
    if not moves:
        return {"action": "stop", "did": "stub: the prompt lists no open move to offer", "question": ""}
    wanted = row.get("variant")
    if wanted is not None:
        wanted = [wanted] if isinstance(wanted, str) else list(wanted)
        absent = [w for w in wanted if w not in [token for _m, token in moves]]
        if absent:
            return {"action": "stop", "did": f"stub: the row's variant {absent} is not offered by the prompt (open: {[t for _m, t in moves]})", "question": ""}
        moves = [(m, t) for m, t in moves if t in wanted]
    return {"action": "ask_person", "did": row.get("did") or "stub: offered every open move",
            "question": row.get("question") or "Which of these should happen?",
            "why_person": row.get("why_person", DEFAULT_WHY), "checked": row.get("checked", DEFAULT_CHECKED),
            "options": [move_option(move, token) for move, token in moves]}


def conductor_execute(execute, project, task_dir, task: str, run=None) -> dict:
    """The journal's account of the move a conductor row says to run (E3). `execute`: `{"move": <id>, "run": [[script, args...], ...]}` - exactly the
    commands of the move (each script must be the one the move's own `run` text in conductor-actions.json starts with; `{task_root}` and `{task}` in an
    argument are filled) - or `{"move": <id>, "executor": "conductor_judgment"}` for a move no command fills without judgment: nothing runs and the
    row says so, so the case is judged by the later checks only, never counted as run (AR-29). A move or a script the data does not hold is `refused`."""
    import no_move as NM
    run = run or run_script
    if not isinstance(execute, dict) or not execute.get("move"):
        return {"refused": "`execute` names no move"}
    move = str(execute["move"])
    row = NM.move_rows().get(move)
    if row is None:
        return {"move": move, "refused": f"no move `{move}` in references/conductor-actions.json"}
    if execute.get("executor") == "conductor_judgment":
        return {"move": move, "executor": "conductor_judgment", "ran": []}
    head = str(row.get("run") or "").split()[:1]
    ran = []
    for command in execute.get("run") or []:
        if not isinstance(command, list) or not command or [command[0]] != head:
            return {"move": move, "ran": ran, "refused": f"the command {command!r} is not the move's own (its `run` starts with {head})"}
        code, text = run(project, command[0], [str(a).replace("{task_root}", str(task_dir)).replace("{task}", task) for a in command[1:]])
        ran.append({"command": command, "exit": code, "text": cut(text)})
    return {"move": move, "executor": "stub", "ran": ran}


def source_key(item: dict) -> str:
    """The tracker key of an inventory source: the tail of its canonical ref (the rule of `source_inventory._key`)."""
    return str(item.get("canonical_ref") or item.get("source_id") or "").rsplit("/browse/", 1)[-1]


def read_sources(inventory: Path):
    """`(sources, "")` of the inventory read through the package's one reader (`source_inventory.load_inventory`, AR-13), or `([], why)`."""
    import source_inventory as SI
    try:
        return [s for s in SI.load_inventory(inventory).get("sources") or [] if isinstance(s, dict)], ""
    except (OSError, ValueError):
        return [], "work/source-inventory.json is missing or unreadable after the collect step"


def awaiting(sources: list) -> tuple:
    """`(unjudged, uncollected)`: the required sources whose relevance is still `pending` (a mention the scout must `peek` and `assess`), and the
    kept ones (`relevant`) whose full collection has not replaced the pending status yet (`source_inventory.record_relevance_assessment`)."""
    unjudged = [s for s in sources if s.get("required") and s.get("relevance") == "pending"]
    uncollected = [s for s in sources if s.get("required") and s.get("relevance") == "relevant" and s.get("status") == "pending"]
    return unjudged, uncollected


def pending_judgments(inventory: Path, skip=()) -> str:
    """"" when the inventory holds no source awaiting the scout (`awaiting`), else the live_only reason, naming each source: an unjudged mention is
    the role's judgment - a key the type's `stub.source_relevance` does not name gets no value from the stub (E13, AR-29) and the exit gate's own refusal
    stands; a kept source left uncollected has no read step that closed it. `skip` holds the keys a command already reported with its own text."""
    sources, why = read_sources(inventory)
    if why:
        return why
    unjudged, uncollected = awaiting(sources)
    parts = []
    refs = [s.get("canonical_ref") or s.get("source_id") for s in unjudged if source_key(s) not in skip]
    if refs:
        parts.append(f"{len(refs)} mentioned source(s) await the scout's judgment ({', '.join(map(str, refs[:5]))}): `ticket_adapter.py peek` then `assess "
                     "--relevance` is role judgment and the type holds no closed answer for it")
    kept = [s.get("canonical_ref") or s.get("source_id") for s in uncollected if source_key(s) not in skip]
    if kept:
        parts.append(f"{len(kept)} kept source(s) left pending after `assess` with no read step that closes them ({', '.join(map(str, kept[:5]))})")
    return "; ".join(parts)


def run_script(project: Path, script: str, args: list) -> tuple:
    """`(exit code, stderr or stdout)` of the ONE runner of a package script in the project, as the role runs it: `harness.run_script` (no bytecode, a
    timeout). A script that outlives the timeout is exit -9 with that text, a failed command like any other (never a traceback)."""
    try:
        done = harness.run_script(script, *args, cwd=project)
    except subprocess.TimeoutExpired:
        return -9, f"{script} did not finish within its timeout"
    return done.returncode, (done.stderr or done.stdout)


def cut(text: str, limit: int = 400) -> str:
    """The head of a command's text on one line (a `live_only` carries it; the stub journal keeps the whole row)."""
    return " ".join(text.split())[:limit]


# ------------------------------------------------------------------------------------------------ the story kit and the runner table (node N2)
STORIES = HERE / "fixtures" / "stories"
ABSENT_JSON = {"$absent": True}        # in a row's `overrides`: the field is left out (`form_filler.ABSENT`, which JSON cannot carry)
DEFAULT_WHY, DEFAULT_CHECKED = "access", "the refusal"       # RN1-9: a question names a class and what was read; a row that wants another says so
CHANNELS = ("auto", "manual")


class Unfillable(Exception):
    """An output or form the filler cannot fill: WHICH form or output, WHICH field and why. Never a text value, never a default: a role call that meets
    it writes nothing for that output and the journal row says `live_only` with these words (E13)."""

    def __init__(self, form: str, field: str, why: str):
        super().__init__(f"{form}: cannot fill {field or 'the whole output'}: {why}")
        self.form, self.field, self.why = form, field, why


class KitError(ValueError):
    """A story file (`story.json`, `kit.json`, a runner row) that cannot be used: the message names the file and what was expected (FR-1, FR-59)."""


def read_json(path) -> dict:
    """The JSON object at `path`, or a `KitError` naming the file: absent, empty, not JSON, or not an object. An unreadable file is a red line, never a skip."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise KitError(f"{path}: cannot be read ({type(exc).__name__}); expected a JSON object") from None
    if not text.strip():
        raise KitError(f"{path}: the file is empty; expected a JSON object")
    try:
        found = json.loads(text)
    except ValueError as exc:
        raise KitError(f"{path}: not valid JSON ({exc}); expected a JSON object") from None
    if not isinstance(found, dict):
        raise KitError(f"{path}: holds {type(found).__name__}; expected a JSON object")
    return found


def load_kit(story_id: str, base=None) -> dict:
    """The kit of a story (`kit.json`: the task key, the requirement ids, the cases with their channel, the ids other forms issue, the runner row it
    walks) checked against its `story.json` (same task key). The ONE reader of the kit: the filler's context is built from it and from nothing else."""
    folder = Path(base or STORIES) / story_id
    story, kit = read_json(folder / "story.json"), read_json(folder / "kit.json")
    problems = []
    if not isinstance(kit.get("key"), str) or not kit["key"].strip():
        problems.append("`key` is not a non-empty text")
    if story.get("task") != kit.get("key"):
        problems.append(f"`key` {kit.get('key')!r} is not the `task` {story.get('task')!r} of story.json")
    reqs = kit.get("requirements")
    if not isinstance(reqs, list) or not reqs or not all(isinstance(r, str) and r.strip() for r in reqs):
        problems.append("`requirements` is not a non-empty list of ids")
    cases = kit.get("cases")
    if not isinstance(cases, list) or not cases or not all(isinstance(c, dict) and isinstance(c.get("id"), str) and c["id"].strip()
                                                           and c.get("channel") in CHANNELS for c in cases):
        problems.append(f"`cases` is not a non-empty list of {{id, channel in {list(CHANNELS)}}}")
    elif len({c["id"] for c in cases}) != len(cases):
        problems.append("`cases` names one id twice")
    if not isinstance(kit.get("minted"), dict):
        problems.append("`minted` is not an object (prefix -> the ids the world issues)")
    if not isinstance(kit.get("runner"), str) or not kit["runner"].strip():
        problems.append("`runner` is not the id of a row under runners/")
    if problems:
        raise KitError(f"{folder / 'kit.json'}: " + "; ".join(problems))
    return kit


def kit_context(kit: dict, dispatch: str = "", impl_diff: str = "", cases=None):
    """The `FillContext` of the kit for ONE call: its ids (`cases` narrows them, a test file is one per case), the call's dispatch id."""
    import form_filler as FF
    ids = [c["id"] for c in kit["cases"]] if cases is None else list(cases)
    return FF.FillContext(task_key=kit["key"], dispatch_id=dispatch, requirements=list(kit["requirements"]), cases=ids,
                          minted={k: list(v) for k, v in kit["minted"].items()}, impl_diff=impl_diff)


def runner_rows(story_id: str = "dry-1", base=None) -> list:
    """The table of runners (F5): one row per folder `runners/<row>/runner.json` (`id` = the folder, `lang`, `profile` with its `profile_id` and `commands`).
    An empty or absent `runners/` is a refusal naming the folder; so is a row folder with no `runner.json`."""
    folder = Path(base or STORIES) / story_id / "runners"
    dirs = sorted(d for d in folder.iterdir() if d.is_dir()) if folder.is_dir() else []
    if not dirs:
        raise KitError(f"{folder}: no runner row; expected runners/<row>/runner.json (the table of runners, F5)")
    rows = []
    for d in dirs:
        row = read_json(d / "runner.json")
        profile = row.get("profile")
        if row.get("id") != d.name or not isinstance(row.get("lang"), str) or not row["lang"].strip() \
                or not isinstance(profile, dict) or profile.get("profile_id") != row.get("profile_id") or not row.get("profile_id"):
            raise KitError(f"{d / 'runner.json'}: expected `id` = {d.name!r}, a `lang`, and a `profile` whose `profile_id` is the row's `profile_id`")
        rows.append(dict(row, dir=str(d)))
    return rows


def runner_row(row_id: str, story_id: str = "dry-1", base=None) -> dict:
    rows = runner_rows(story_id, base)
    found = [r for r in rows if r["id"] == row_id]
    if not found:
        raise KitError(f"{Path(base or STORIES) / story_id / 'runners'}: no runner row {row_id!r}; expected one of {[r['id'] for r in rows]}")
    return found[0]


def config_path(project) -> Path:
    return Path(project) / "qa-factory" / "config.json"


def install_runner(project, row: dict) -> None:
    """Put a runner row into a world: the tiny project of the row (`<row>/project/`) beside the config, the row's profile into `config.profiles` (replacing
    the one of the same id). The commands the automator stub runs are the ones the WORLD holds afterwards, read through `profile_contract`."""
    src = Path(row["dir"]) / "project"
    if src.is_dir():
        shutil.copytree(src, project, dirs_exist_ok=True)
    cfg = read_json(config_path(project))
    cfg["profiles"] = [p for p in cfg.get("profiles") or [] if not (isinstance(p, dict) and p.get("profile_id") == row["profile_id"])] + [row["profile"]]
    config_path(project).write_text(json.dumps(cfg, indent=2), encoding="utf-8")


def world_profile(project, profile_id: str):
    """The profile row of the world's config with this id (the config's own `profiles`, read the way `config_contract._profile_slot` reads it), or None."""
    rows = read_json(config_path(project)).get("profiles")
    return next((p for p in rows if isinstance(p, dict) and str(p.get("profile_id")) == str(profile_id)), None) if isinstance(rows, list) else None


def live_row(exc: Unfillable) -> dict:
    """The `live_only` row of the journal for an `Unfillable`: the output or form, the field when there is one, the reason."""
    return {"output": exc.form, **({"field": exc.field} if exc.field else {}), "why": exc.why[:240]}


def decode_overrides(raw) -> dict:
    """`{path: value | ABSENT}` of a row's overrides (`{path: value}`, a value `{"$absent": true}` meaning the field is left out)."""
    import form_filler as FF
    return {path: (FF.ABSENT if value == ABSENT_JSON else value) for path, value in (raw or {}).items()}


def overrides_for(mine: dict, key: str, n: int) -> dict:
    """The overrides of the row for form or output `key` on the `n`-th call of this dispatch (1-based): none from the call named by `repair_on_round` on
    (the repair round fills clean). The row decides both; the stub holds no judgment of what to seed or when to repair."""
    repair = mine.get("repair_on_round")
    if isinstance(repair, int) and not isinstance(repair, bool) and n >= repair:
        return {}
    return decode_overrides((mine.get("overrides") or {}).get(key))


def fill_output(output: str, ctx, overrides=None):
    """The `FilledArtifact` of a role output, or `Unfillable` (the output, the field, why): an output code writes, one the filler has no kind for
    (`not_covered`), one the tables cannot place, and a field no rule fills are all the same refusal - no text is ever put in their place (E13)."""
    import form_filler as FF
    try:
        made = FF.fill_artifact(output, ctx, overrides=overrides)
    except (FF.Unclassified, ValueError) as exc:
        raise Unfillable(output, "", str(exc)) from None
    if isinstance(made, FF.ByCode):
        raise Unfillable(output, "", f"written by code ({made.writer}), not by the role")
    if isinstance(made, FF.NotCovered):
        raise Unfillable(output, "", f"no filler kind: {made.why}")
    if made.unfillable:
        first = made.unfillable[0]
        raise Unfillable(output, first.path, first.why + (f" (and {len(made.unfillable) - 1} more)" if len(made.unfillable) > 1 else ""))
    return made


def fill_handover(contract: str, ctx, verdict=None, overrides=None):
    """The `Filled` form of a contract, or `Unfillable` naming the contract and the first field no rule fills."""
    import form_filler as FF
    filled = FF.fill_form(contract, ctx, verdict=verdict, overrides=overrides)
    if filled.unfillable:
        first = filled.unfillable[0]
        raise Unfillable(contract, first.path, first.why + (f" (and {len(filled.unfillable) - 1} more)" if len(filled.unfillable) > 1 else ""))
    return filled


def rel(project, path) -> str:
    return str(Path(path).relative_to(project)).replace("\\", "/")


def run_command(words: list, cwd, timeout: int = 120) -> tuple:
    """`(exit code, text)` of ONE command of the profile as it stands (argv words, the project as cwd): a missing program is exit 127 and a command that
    outlives the timeout is -9, each with its text - a failed command like any other, never a traceback."""
    try:
        done = subprocess.run(words, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    except FileNotFoundError:
        return 127, f"{words[0]}: program not found"
    except subprocess.TimeoutExpired:
        return -9, f"{words[0]} did not finish within {timeout} s"
    return done.returncode, (done.stdout + done.stderr)


def automator_branch(project, task_dir, kit: dict, runner: dict, dispatch: str, run=run_script) -> dict:
    """What the automator role does at S5, as the journal row's keys. The test file of each automated case is the `test_file:<lang>` of the runner row's
    language, written by the filler; the command that runs the tests is the one the WORLD's profile holds (`profile_contract.profile_commands`, axis 30) -
    nothing in this function reads the call's text; a profile with no command is `no_command` in the row and nothing is run. The manifest fragment of
    each case is the filler's `manifest_row`, merged by `manifest_put.py` (the one writer of the manifest)."""
    import form_filler as FF
    import profile_contract as PC
    out = {"wrote": [], "live_only": [], "ran": []}
    cases = [c["id"] for c in kit["cases"] if c["channel"] == "auto"]
    written = []
    for case in cases:
        try:
            made = fill_output(f"test_file:{runner['lang']}", kit_context(kit, dispatch, cases=[case]))
            out["wrote"] += [rel(project, p) for p in FF.write_outputs(task_dir, project, made)]
            written.append(case)
        except Unfillable as exc:
            out["live_only"].append(dict(live_row(exc), case=case))
    profile = world_profile(project, runner["profile_id"])
    commands, problem = PC.profile_commands(profile)
    name = runner.get("command") or "one_test"
    spec = commands.get(name)
    words, word_problem = PC.command_argv(spec)
    if problem or word_problem or not words:
        out["no_command"] = f"no command `{name}` in the profile {runner['profile_id']!r}: " + (problem or word_problem or "the profile holds none")
        out["live_only"].append({"output": "the run of the tests", "why": out["no_command"]})
    elif written:
        code, text = run_command(words, Path(project) / str(spec.get("cwd") or "."))
        out["ran"].append({"argv": words, "exit": code, "text": cut(text)})
    for case in written:
        try:
            frag = task_dir / "state" / "dry-stub-fragments" / f"{dispatch}-{case}.json"
            frag.parent.mkdir(parents=True, exist_ok=True)
            frag.write_text(fill_output("manifest_row", kit_context(kit, dispatch, cases=[case])).files["work/automation-manifest.json"], encoding="utf-8")
            code, text = run(project, "manifest_put.py", ["--task", kit["key"], "--fragment", str(frag)])
            if code == 0:
                out["wrote"].append("work/automation-manifest.json")
            else:
                out["live_only"].append({"output": "work/automation-manifest.json", "case": case, "why": f"manifest_put.py exit {code}: {cut(text)}"})
        except Unfillable as exc:
            out["live_only"].append(dict(live_row(exc), case=case))
    return out


def judge_sources(inventory: Path, declared: dict, runner) -> tuple:
    """`(ran, judged, live_only)` of the scout's source work after `collect`: for each required source with `relevance: pending` whose key IS in
    `declared` (the type row's `stub.source_relevance`, data the stub only READS - AR-29) run `ticket_adapter.py peek <KEY>` then `assess` with exactly
    the declared value and the `assessment_ref` peek wrote; a key not named is left alone (`live_only` by the caller, no command); each kept source
    (`relevant`, still pending) gets the complete collector `collect <KEY> --relation referenced`, a read that decides nothing. A command that fails
    is a `live_only` with its text cut at 400 and is never retried with another value (E-R4). `runner(script, args) -> (exit, text)`."""
    ran, judged, live_only, tried = [], [], [], set()
    out = str(inventory)
    for _round in range(8):         # a collected ticket names further tickets, each needing peek+assess then its collection: a bounded few rounds, then what is left is reported
        sources, why = read_sources(inventory)
        if why:
            live_only.append({"output": "work/source-inventory.json", "why": why})
            break
        unjudged, uncollected = awaiting(sources)
        moved = False
        for item in unjudged:
            key = source_key(item)
            decl = declared.get(key)
            if not decl or ("judge", key) in tried:
                continue
            tried.add(("judge", key))
            moved = True
            code, text = runner("ticket_adapter.py", ["peek", key, "--output", out])
            ran.append(f"peek {key} exit {code}")
            after = next((s for s in read_sources(inventory)[0] if s.get("source_id") == item.get("source_id")), {})
            if after.get("relevance") != "pending" or not after.get("assessment_ref"):
                live_only.append({"output": "work/source-inventory.json", "key": key,
                                  "why": f"peek {key} left nothing to cite for `assess` (exit {code}): {cut(text)}"})
                continue
            code, text = runner("ticket_adapter.py", ["assess", "--output", out, "--source-id", item["source_id"], "--relevance", decl["relevance"],
                                                      "--reason", decl["reason"], "--assessment-ref", after["assessment_ref"]])
            ran.append(f"assess {key} {decl['relevance']} exit {code}")
            if code == 0:
                judged.append(key)
            else:
                live_only.append({"output": "work/source-inventory.json", "key": key,
                                  "why": f"assess {key} refused (exit {code}): {cut(text)}"})
        for item in uncollected:
            key = source_key(item)
            if key not in judged or ("collect", key) in tried:
                continue            # kept before this call (not by a declared value): the stub does not collect what it did not judge
            tried.add(("collect", key))
            moved = True
            code, text = runner("ticket_adapter.py", ["collect", key, "--relation", "referenced", "--output", out, "--summary"])
            ran.append(f"collect {key} referenced exit {code}")
            if code != 0:
                live_only.append({"output": "work/source-inventory.json", "key": key,
                                  "why": f"collect {key} refused (exit {code}): {cut(text)}"})
        if not moved:
            break
    return ran, judged, live_only


def role_plan(role: str, stage: str, ff) -> list:
    """`[(output, kind)]` of the stage's outputs this role writes: `fill` (a role output with a template), `live_only:<why>` (the
    filler has no kind for it, E13), `command:<script>` (code builds it from the role's file; the role runs the command)."""
    plan = []
    for stage_id, out in ff.stage_outputs():
        if stage_id != stage:
            continue
        try:
            writer = ff.writer_of(out)
            kind = ff.classify(out)
        except ff.Unclassified as exc:
            plan.append((out, f"live_only:{exc.why}"))
            continue
        if writer == f"{role}{ff.ROLE_WRITER}":
            plan.append((out, "fill" if kind == "role" else f"live_only:{ff.rules()['not_covered'].get(out, 'no filler kind')}"))
        elif writer in COMMANDS and role == "qa-scout":
            plan.append((out, f"command:{writer}"))
    return plan


def run_class_problem(rows: list) -> str:
    """"" when the first row of the stub journal says the run class reached the stub as `dry`; else the red line (E18)."""
    first = rows[0] if rows else {}
    if first.get("run_class") != "dry":
        return f"run class not propagated: the stub saw STORY_RUN_CLASS={first.get('run_class')!r}, expected 'dry'"
    return ""


def journal(task_dir: Path, row: dict) -> None:
    path = task_dir / "state" / "dry-stub.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        path.write_text(json.dumps({"first": True, "ts": now(), "run_class": os.environ.get("STORY_RUN_CLASS", "")}) + "\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")


def calls_before(task_dir: Path, key: str) -> int:
    path = task_dir / "state" / "dry-stub.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.is_file() else []
    return len([r for r in rows if (r.get("dispatch") or r.get("conductor")) == key])


def fill_role(role: str, prompt: str, control: dict, project: Path, task_dir: Path, dispatch: str = "", n: int = 1) -> tuple:
    """`(dispatch, result text, journal row)` of one role call; see the module text. `dispatch` names the call when the prompt does not (a repair resume);
    `n` is the call's number within its dispatch (the row's `repair_on_round` reads it)."""
    import form_filler as FF
    found = re.search(r"Dispatch: (\S+)\.", prompt)
    dispatch = found.group(1) if found else dispatch
    row = {"role": role, "wrote": [], "live_only": []}
    form = task_dir / "work" / "handoffs" / f"{dispatch}.yaml"
    text = form.read_text(encoding="utf-8") if form.is_file() else ""
    contract, stage = FORM_CONTRACT.search(text), FORM_STAGE.search(text)
    stage = stage.group(1) if stage else ""
    row["stage"] = stage
    mine = (control.get("stub") or {}).get(role) or {}
    task = control.get("task", "")
    import dry_world as W
    diff = W.mr_diff(W.type_row(control.get("type"))) if control.get("type") else ""
    kit = load_kit(control["story"]) if control.get("story") else None
    ctx = kit_context(kit, dispatch, diff) if kit else FF.FillContext(task_key=task, dispatch_id=dispatch, impl_diff=diff)
    if not contract:
        row["live_only"].append({"output": f"work/handoffs/{dispatch}.yaml", "why": "no form with a `contract:` line at that path"})
    else:
        try:
            filled = fill_handover(contract.group(1), ctx, mine.get("verdict"), overrides_for(mine, contract.group(1), n))
            form.write_bytes(filled.text.encode("utf-8"))
            row["wrote"].append(f"work/handoffs/{dispatch}.yaml")
        except Unfillable as exc:
            row["live_only"].append(dict(live_row(exc), output=f"form {contract.group(1)}"))
    if kit and role == "qa-automator" and stage == "S5":
        done = automator_branch(project, task_dir, kit, runner_row(kit["runner"]), dispatch)
        row["wrote"] += done["wrote"]
        row["live_only"] += done["live_only"]
        row["ran"] = done["ran"]
        if "no_command" in done:
            row["no_command"] = done["no_command"]
    for out, script, args in ROLE_STEPS.get(role, []) if stage == "S1" else []:
        code, text = run_script(project, script, [a.format(task=task, task_root=str(task_dir)) for a in args])
        (row["wrote"] if code == 0 else row["live_only"]).append(out if code == 0 else {"output": out, "why": f"{script} exit {code}: {cut(text)}"})
    if stage == "S1" and role in ROLE_STEPS:
        inventory = task_dir / "work" / "source-inventory.json"
        ran, judged, failed = judge_sources(inventory, (control.get("stub") or {}).get("source_relevance") or {},
                                            lambda script, args: run_script(project, script, args))
        row["ran"], row["judged"] = ran, judged
        row["live_only"].extend(failed)
        gap = pending_judgments(inventory, skip={f["key"] for f in failed if f.get("key")})
        if gap:
            row["live_only"].append({"output": "work/source-inventory.json", "why": gap})
    for out, kind in role_plan(role, stage, FF):
        if kind == "fill":
            try:
                FF.write_outputs(task_dir, project, fill_output(out, ctx, overrides_for(mine, out, n)))
                row["wrote"].append(out)
                for where, why in (FF._row_of(out).get("synthetic") or {}).items():       # a value the row declares synthetic is named, not passed as a fact
                    row.setdefault("synthetic", []).append({"output": out, "field": where, "why": why[:120]})
            except (Unfillable, FF.NotFillable, ValueError) as exc:
                row["live_only"].append(live_row(exc) if isinstance(exc, Unfillable) else {"output": out, "why": str(exc)[:240]})
        elif kind.startswith("command:"):
            argv = [a.format(task_root=str(task_dir)) for a in COMMANDS[kind[8:]]]
            code, text = run_script(project, kind[8:], argv)
            (row["wrote"] if code == 0 else row["live_only"]).append(out if code == 0 else {"output": out, "why": f"{kind[8:]} exit {code}: {cut(text)}"})
        else:
            row["live_only"].append(live_row(Unfillable(out, "", kind[len("live_only:"):])))        # no filler kind: the same refusal, no text in its place
    default = f"{role} {stage} {task} - the stub filled the handover form of {dispatch}; nothing else to say"
    return dispatch, mine.get("result_text") or default, row


def claude_main(argv: list) -> int:
    """The stub `claude -p`: one JSON line on stdout, the shape the driver's `run_claude` reads."""
    def opt(name):
        return argv[argv.index(name) + 1] if name in argv else ""
    prompt = sys.stdin.buffer.read().decode("utf-8")
    control_path = os.environ.get("DRY_STUB_CONTROL", "")
    control = json.loads(Path(control_path).read_text(encoding="utf-8")) if control_path and Path(control_path).is_file() else {}
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".").resolve()
    task_dir = project / "qa-factory" / "artifacts" / control.get("task", "")
    agent, resume = opt("--agent"), opt("--resume")
    role = agent.split(":")[-1]
    if resume or agent:
        found = re.search(r"Dispatch: (\S+)\.", prompt)
        derived = re.fullmatch(r"stub-(.+)-\d+", resume)      # a resume names the session the stub answered before: `stub-<dispatch>-<n>`
        key = found.group(1) if found else (derived.group(1) if derived else (resume or role))
        n = calls_before(task_dir, key) + 1
        repair = (control.get("stub") or {}).get(role, {}).get("repair_on_round")
        if resume and not (isinstance(repair, int) and not isinstance(repair, bool) and n >= repair):
            # a repair resume before the row's repair round: the stub has no judgment to repair with, so it answers as before and writes nothing
            result, row, session = (control.get("stub") or {}).get(role, {}).get("result_text") or "", {"role": role, "resume": True, "wrote": [], "live_only": []}, resume
            dispatch_id = key
        else:         # a call, or the repair resume the row's `repair_on_round` names: the forms are filled again, now without the row's overrides
            dispatch_id, result, row = fill_role(role, prompt, control, project, task_dir, dispatch=key, n=n)
            session = resume if resume else f"stub-{dispatch_id}-{n}"
            row = dict(row, resume=True) if resume else row
        journal(task_dir, dict(row, ts=now(), dispatch=dispatch_id, n=n, prompt_sha=hashlib.sha256(
            prompt.replace(dispatch_id, "<dispatch>").encode("utf-8")).hexdigest(), run_class=os.environ.get("STORY_RUN_CLASS", "")))
    else:
        n = calls_before(task_dir, "conductor") + 1
        execute = (control.get("conductor") or {}).get("execute")
        done = conductor_execute(execute, project, task_dir, control.get("task", "")) if execute else None
        verdict = conductor_verdict(prompt, control)
        if done and done.get("refused"):
            verdict = {"action": "stop", "did": f"stub: {done['refused']}", "question": ""}
        result, session = "I looked.\n" + json.dumps(verdict), f"stub-conductor-{n}"
        journal(task_dir, dict({"ts": now(), "conductor": "conductor", "n": n, "role": "", "wrote": [], "live_only": [], "action": verdict.get("action"),
                                "prompt_sha": hashlib.sha256(prompt.encode("utf-8")).hexdigest(), "run_class": os.environ.get("STORY_RUN_CLASS", "")},
                               **({"executed": done} if done else {})))
    ns: dict = {}
    exec(T.RECEIPT, ns)
    ns["write_receipt"](session, None)
    print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "session_id": session, "num_turns": 3,
                      "total_cost_usd": 0.0, "duration_ms": 1, "result": result}))
    sys.stdout.flush()
    return 0


# ------------------------------------------------------------------------------------------------ the selftest
def selftest() -> int:
    from harness import check, check_eq, finish
    import dry_world as W
    import form_filler as FF
    tmp = Path(tempfile.mkdtemp(prefix="qa-dry-selftest-"))

    def table(name, content, folders=(), expect=None):
        folder = tmp / name
        folder.mkdir()
        for f in folders:
            (folder / f).mkdir()
            (folder / f / "routes.json").write_text("{}", encoding="utf-8")
        (folder / "dry-types.json").write_text(content, encoding="utf-8")
        try:
            W.load_types(folder / "dry-types.json")
            return "ok"
        except W.TypesError as exc:
            return str(exc)

    def one(tid, **extra):
        return dict({"id": tid, "input": f"in-{tid}", "task": "T-1", "tracker": {"kind": "jira", "routes": "routes.json"}}, **extra)

    good = json.dumps({"default": "a", "types": [one("a")], "gaps": []})
    # A1-E4: every broken table is red naming the file and the id; the good one passes (control)
    cases = {
        "a good table loads (control)": (good, ("in-a",), "ok"),
        "an empty file": ("", (), "dry-types.json: the file is empty"),
        "a type without its folder": (good, (), "type 'a' names the folder 'in-a'"),
        "two types with one id": (json.dumps({"default": "a", "types": [one("a"), one("a")], "gaps": []}), ("in-a",), "share the id 'a'"),
        "default not among the types": (json.dumps({"default": "zz", "types": [one("a")], "gaps": []}), ("in-a",), "`default` is 'zz'"),
        "not JSON": ("{nope", (), "not valid JSON"),
        "no types": (json.dumps({"default": "a", "types": []}), (), "`types` is missing or empty"),
        "an unknown tracker kind": (json.dumps({"default": "a", "types": [one("a", tracker={"kind": "x"})], "gaps": []}), ("in-a",), "tracker kind 'x'"),
    }
    for n, (name, (content, folders, needle)) in enumerate(cases.items()):
        got = table(f"t{n}", content, folders)
        check(f"load_types: {name}", got == "ok" if needle == "ok" else needle in got, f"got {got!r}")
    types, gaps = W.load_types()
    check_eq("load_types: the real table holds the one type and both gaps", ([t["id"] for t in types], [g["id"] for g in gaps]),
             (["codemie-14857"], ["mybooks-local-1", "no-autotests"]))
    # A1-E8 / A1-E9: a known route answers its file, an absent one 404, a repeat answers the same and is counted
    server = W.tracker_server(W.type_row())
    try:
        import urllib.error
        import urllib.request
        def get(path):
            try:
                with urllib.request.urlopen(server.base_url + path, timeout=10) as r:
                    return r.status, r.read()
            except urllib.error.HTTPError as exc:
                return exc.code, b""
        known, again = get("/rest/api/2/issue/TP1-14857?fields=*all"), get("/rest/api/2/issue/TP1-14857?fields=*all")
        missing = get("/rest/api/2/issue/TP1-14857/remotelink")
        check_eq("tracker: the ticket route answers 200 with the issue key", (known[0], json.loads(known[1])["key"]), (200, "TP1-14857"))
        check_eq("tracker: a repeated request gets the same bytes", again, known)
        check_eq("tracker: a route the world does not hold answers 404", missing[0], 404)
        check_eq("tracker: the request count is printed per path", server.counts["/rest/api/2/issue/TP1-14857?fields=*all"], 2)
        check("tracker: the summary names the path without a route", "remotelink" in server.summary())
    finally:
        server.stop()
    # E13: an output the filler has no kind for is live_only and nothing is written; a form the filler can fill is written whole
    plan = dict(role_plan("qa-scout", "S1", FF))
    check_eq("round 2: impl-diff.txt and context-manifest.json are filled, the bundle is built by its command",
             (plan.get("work/impl-diff.txt"), plan.get("work/context-manifest.json"), plan.get("work/context-bundle.json")),
             ("fill", "fill", "command:context_bundle.py"))
    row_type = W.type_row()
    diff = W.mr_diff(row_type)
    check("round 2: the type's merge request diff is the raw file, byte for byte", diff.startswith("diff --git ") and diff.encode("utf-8") ==
          (W.STORIES / row_type["input"] / "tracker" / "mr-4566.diff").read_bytes(), diff[:40])
    check_eq("round 2: the diff lands in work/impl-diff.txt as the world holds it", FF.fill_artifact("work/impl-diff.txt", FF.FillContext(impl_diff=diff)).files["work/impl-diff.txt"], diff)
    check_eq("E13: a world with no diff leaves impl-diff.txt unfillable, nothing is written",
             [u.hint for u in FF.fill_artifact("work/impl-diff.txt", FF.FillContext()).unfillable], ["<the diff text>"])
    inv = tmp / "inv.json"
    for name, body, expect in (("a pending required mention", {"sources": [{"required": True, "relevance": "pending", "canonical_ref": "https://x/browse/A-1"}]}, "await the scout's judgment (https://x/browse/A-1)"),
                               ("only the task, read", {"sources": [{"required": True, "relevance": "relevant"}]}, ""),
                               ("no source", {"sources": []}, "")):
        inv.write_text(json.dumps(body), encoding="utf-8")
        check(f"round 2: inventory with {name}", expect in pending_judgments(inv) and bool(pending_judgments(inv)) == bool(expect), pending_judgments(inv))
    check("round 2: an inventory that is not there is named, never read as no pending source", "missing or unreadable" in pending_judgments(tmp / "nope.json"))
    # round 3: the declared judgment is data the stub reads (AR-29, E-R1..E-R5)
    mention = {"source_id": "SRC-a", "canonical_ref": "https://x/browse/A-1", "required": True, "relevance": "pending", "status": "pending"}
    declared = {"A-1": {"relevance": "relevant", "reason": "explicit required source", "from": "x"}}

    class FakeRole:
        """A runner standing in for `ticket_adapter.py`: it records every call and changes the inventory as the real commands would."""
        def __init__(self, path, assess_exit=0, peek_ref="sources/SRC-a/assessment/ticket.json"):
            self.path, self.calls, self.assess_exit, self.peek_ref = path, [], assess_exit, peek_ref

        def __call__(self, script, args):
            self.calls.append([script, *args])
            body = json.loads(self.path.read_text(encoding="utf-8"))
            item = body["sources"][0]
            if args[0] == "peek":
                item["assessment_ref"] = self.peek_ref
            elif args[0] == "assess" and self.assess_exit == 0:
                item.update(relevance=args[args.index("--relevance") + 1], relevance_reason=args[args.index("--reason") + 1])
            elif args[0] == "collect":
                item["status"] = "read"
            self.path.write_text(json.dumps(body), encoding="utf-8")
            return (self.assess_exit, "assess refused: the person left it out") if args[0] == "assess" and self.assess_exit else (0, "")

    def fresh(name, **kw):
        path = tmp / f"{name}.json"
        path.write_text(json.dumps({"sources": [dict(mention)]}), encoding="utf-8")
        return path, FakeRole(path, **kw)

    path, role = fresh("named")
    ran, judged, gap = judge_sources(path, declared, role)
    check_eq("round 3: a named key runs peek then assess then the collector, argv exactly the data values",
             role.calls, [["ticket_adapter.py", "peek", "A-1", "--output", str(path)],
                          ["ticket_adapter.py", "assess", "--output", str(path), "--source-id", "SRC-a", "--relevance", "relevant", "--reason",
                           "explicit required source", "--assessment-ref", "sources/SRC-a/assessment/ticket.json"],
                          ["ticket_adapter.py", "collect", "A-1", "--relation", "referenced", "--output", str(path), "--summary"]])
    check_eq("round 3: a judged and collected source leaves no gap", (judged, gap, pending_judgments(path)), (["A-1"], [], ""))
    path, role = fresh("unnamed")
    ran, judged, gap = judge_sources(path, {}, role)
    check_eq("E-R1 / AR-29: a pending source the data does not name gets no command (no peek, no assess) and is a live_only naming it",
             (role.calls, ran, judged, "https://x/browse/A-1" in pending_judgments(path)), ([], [], [], True))
    path, role = fresh("refused", assess_exit=1)
    ran, judged, gap = judge_sources(path, declared, role)
    check("E-R4: an assess refused is a live_only with the refusal verbatim, no second attempt with another value",
          "assess A-1 refused (exit 1): assess refused: the person left it out" in gap[0]["why"] and [c[1] for c in role.calls] == ["peek", "assess"] and not judged, f"{gap} {role.calls}")
    path, role = fresh("noref", peek_ref=None)
    ran, judged, gap = judge_sources(path, declared, role)
    check("E-R5: a peek that left no assessment to cite is a live_only and no assess runs", "left nothing to cite" in gap[0]["why"] and [c[1] for c in role.calls] == ["peek"], f"{gap} {role.calls}")
    path = tmp / "kept.json"
    path.write_text(json.dumps({"sources": [dict(mention, relevance="relevant")]}), encoding="utf-8")
    check("round 3: a kept source left pending after `assess relevant` with no read step is named by pending_judgments",
          "left pending after `assess`" in pending_judgments(path) and "https://x/browse/A-1" in pending_judgments(path), pending_judgments(path))
    check_eq("round 3: judge_sources does not collect a kept source it did not judge", judge_sources(path, {}, FakeRole(path))[0], [])
    cut_gap = judge_sources(fresh("cut")[0], declared, lambda s, a: (1, "x" * 900))[2]
    check("E-R10: the command text a live_only carries is cut at 400 characters and keeps its head", "x" * 400 in cut_gap[0]["why"] and "x" * 401 not in cut_gap[0]["why"], cut_gap[0]["why"][:80])
    real_run = judge_sources(fresh("real")[0], declared, lambda s, a: run_script(tmp, s, a))[2]
    check("F4: a failing command through the one runner is a live_only with its text head kept, no retry",
          len(real_run) == 1 and real_run[0]["why"].startswith("peek A-1 left nothing to cite for `assess` (exit 3): A-1: this project's tracker is read by its recorded route")
          and len(real_run[0]["why"].split("): ", 1)[1]) <= 400, f"{real_run}")
    check_eq("F4: the cut helper keeps the head, one line, at the limit", (cut("a\n b  c"), len(cut("x" * 900)), len(cut("x" * 900, 10))), ("a b c", 400, 10))
    check_eq("E-R2 / note/unasked-key-note: a declared key the road never asked for is a NOTE",
             W.unused_judgments({"A-1": {}, "B-2": {}}, [{"judged": ["A-1"]}, {}]),
             ["NOTE: unused judgment B-2 (the road never asked for a source with that key)"])
    check_eq("F7 / note/refused-key-no-note: a key whose command was refused has its live_only, no unused note",
             W.unused_judgments({"A-1": {}, "B-2": {}}, [{"judged": [], "live_only": [{"output": "o", "key": "A-1", "why": "assess A-1 refused"}]}]),
             ["NOTE: unused judgment B-2 (the road never asked for a source with that key)"])
    check_eq("F7 / spike-line/stages-run: the stages named are the ones that ran",
             (W.stage_ended({"S0": "done", "S1": "running"}), W.stage_ended({"S0": "done", "S1": "done", "S2": "done", "S3": "done"}), W.stage_ended({})),
             ("S1", "S3", "S0"))
    check_eq("item 2: the row's own value wins over the type's, key by key; the type's other keys stay",
             W.merge_stub({"source_relevance": {"A-1": {"relevance": "relevant"}, "B-2": {"relevance": "unknown"}}, "qa-scout": {"verdict": "x"}},
                          {"source_relevance": {"A-1": {"relevance": "not_relevant"}}}),
             {"source_relevance": {"A-1": {"relevance": "not_relevant"}, "B-2": {"relevance": "unknown"}}, "qa-scout": {"verdict": "x"}})
    check_eq("item 2: the main pass reads the type's stub alone", W.merge_stub({"source_relevance": {"A-1": {}}}, None), {"source_relevance": {"A-1": {}}})
    # E-R3 / A1-E4: a declared judgment that cannot be trusted is red before the world is built
    good_j = {"relevance": "relevant", "reason": "r", "from": "f"}
    for n, (name, stub, needle) in enumerate((
            ("a row without `stub` (the round-2 table) loads (control)", None, "ok"),
            ("a good judgment loads (control)", {"source_relevance": {"A-1": good_j}}, "ok"),
            ("`stub` not a mapping", ["x"], "`stub` is not a mapping"),
            ("a value outside the closed list", {"source_relevance": {"A-1": dict(good_j, relevance="maybe")}}, "relevance 'maybe'"),
            ("an empty reason", {"source_relevance": {"A-1": dict(good_j, reason="  ")}}, "has no `reason`"),
            ("a key twice, case-folded", {"source_relevance": {"A-1": good_j, "a-1": good_j}}, "repeats a key"),
            ("stub/no-from: a judgment with no `from`", {"source_relevance": {"A-1": {"relevance": "relevant", "reason": "r"}}}, "has no `from`"),
            ("stub/blank-from: a judgment with a blank `from`", {"source_relevance": {"A-1": dict(good_j, **{"from": " "})}}, "has no `from`"),
            ("`source_relevance` not a mapping", {"source_relevance": []}, "is not a mapping"))):
        got = table(f"s{n}", json.dumps({"default": "a", "types": [one("a", **({} if stub is None else {"stub": stub}))], "gaps": []}), ("in-a",))
        check(f"load_types (E-R3): {name}", got == "ok" if needle == "ok" else needle in got and "'a'" in got, f"got {got!r}")
    # F2: the probe rows' own `stub` is checked when the rows are loaded, before any world is built: the file, the row id and the key are named
    def rows_of(name, stub, absent=False):
        file = tmp / f"{name.replace('/', '-')}.json"
        file.write_text(json.dumps({"rows": [{"id": "r1", "start": "S0", **({} if absent else {"stub": stub})}]}), encoding="utf-8")
        try:
            return W.load_rows(file)
        except W.TypesError as exc:
            return str(exc)
    for name, stub, absent, needle in (
            ("stub/row-no-reason", {"source_relevance": {"A-1": {"relevance": "relevant", "from": "f"}}}, False, "row 'r1' `stub.source_relevance['A-1']` has no `reason`"),
            ("stub/row-not-mapping", ["x"], False, "row 'r1' `stub` is not a mapping"),
            ("stub/row-bad-relevance", {"source_relevance": {"A-1": dict(good_j, relevance="maybe")}}, False, "relevance 'maybe'")):
        got = rows_of(name, stub, absent)
        check(f"load_rows (F2): {name}", isinstance(got, str) and needle in got and got.startswith(name.replace("/", "-") + ".json: "), f"got {got!r}")
    got = rows_of("stub/row-absent", None, absent=True)
    check_eq("load_rows (F2): stub/row-absent loads, the row has no `stub`", [r.get("stub") for r in got] if isinstance(got, list) else got, [None])
    check_eq("load_rows (F2): the committed probe rows load (control)", [r["id"] for r in W.load_rows()], ["s1.review/go on", "questions/answers", "halt/words"])
    real = W.type_row()
    check_eq("item 1: the real type declares the recorded verdict of TP1-15791", (real["stub"]["source_relevance"]["TP1-15791"]["relevance"],
             real["stub"]["source_relevance"]["TP1-15791"]["from"].split(":")[0]), ("relevant", "investigation-14857/TP1-14857/work/source-inventory.json"))
    # AR-28: a gate verdict only when S3 is done; E-R8: a byte change in a snapshot is red
    all_done = {"S0": "done", "S1": "done", "S2": "done", "S3": "done"}
    reached = {"id": "r1", "outcome": "asked s1_review (as expected); answered; next turn exit 0", "seconds": 5}
    short = {"id": "r2", "outcome": "live_only: expected a halt question, the road meets s1_review first", "seconds": 1}
    line = W.gate_line(all_done, {}, 10, 5, 8, [reached, reached])
    check("F1 / gate/all-reached: S3 done, every row reached its question, no red: the numbers verdict", line.startswith("gate: continue ("), line)
    line = W.gate_line(all_done, {}, 10, 1, 1, [reached, short])
    check("F1 / gate/row-short-of-its-question: S3 done, one row short: undecided naming the row, never `continue`",
          line.startswith("gate: undecided -- row r2 did not reach its question: live_only: expected a halt question") and "continue" not in line, line)
    line = W.gate_line(all_done, {}, 10, 5, 8, [reached], ["red: snapshot changed by a row: r1"])
    check("F1 / gate/snapshot-red: S3 done, rows reached, a snapshot red: undecided naming the red", line.startswith("gate: undecided -- red: snapshot changed by a row: r1;"), line)
    line = W.gate_line(all_done, {}, 10, 0, 0, [])
    check("F1 / gate/no-rows: S3 done and no probe row: undecided, `no probe row`", line.startswith("gate: undecided -- no probe row: "), line)
    early = W.gate_line(dict(all_done, S2="running", S3="absent"), {"S2": "running - live_only: " + "y" * 300}, 10, 5, 8)
    check("AR-28 / E-R7: S3 not done prints `undecided` with the stage, the cut outcome and the measured part",
          early.startswith("gate: undecided -- the road ended at S2: running - live_only: y") and "measured: S0..S2 10.0 s, row median 5.0 s" in early
          and "y" * 20 in early and "y" * 300 not in early and len(early.split(": ", 2)[2].split("; measured")[0]) <= 160, early)
    check("AR-28: an undecided line never reads `continue`", "continue" not in early, early)
    snap_dir = tmp / "snapdir"
    snap_dir.mkdir()
    (snap_dir / "a.txt").write_bytes(b"one")
    before = W.tree_hash(snap_dir)
    check_eq("E-R8: an untouched tree is not red", W.snapshot_red("row1", before, snap_dir), "")
    (snap_dir / "a.txt").write_bytes(b"onE")
    check_eq("E-R8: a byte change between the two hashes is red naming the row", W.snapshot_red("row1", before, snap_dir), "red: snapshot changed by a row: row1")
    check_eq("round 2: the answers of the road are the words of the first row naming the kind", W.closed_answers([{"answers": {"a": "x"}}, {"answers": {"a": "y", "b": "z"}}]), {"a": "x", "b": "z"})
    # the conductor stub offers every open move the prompt lists, and stops when it lists none
    prompt = "x\n## Moves open here\n\nintro\n- `retry` — token `again`; option carries no \"args\"\n- `story_fact` — yours to run, never an option\n- `stop_here` — token `stop`; option carries no \"args\"\n\n## Other\n- `no` — token `no`;"
    check_eq("conductor: the open moves of the prompt, in order", parse_moves(prompt), [("retry", "again"), ("stop_here", "stop")])
    import no_move as NM
    real_prompt = NM.moves_section(NM.data(), ["approve_gate", "release_and_restart"], {})        # the prompt the driver prints, from the data
    verdict = conductor_verdict(real_prompt, {})
    check_eq("conductor: ask_person with every open move as an option", (verdict["action"], [o["move"] for o in verdict["options"]]),
             ("ask_person", ["approve_gate", "release_and_restart"]))
    check_eq("conductor: no section, no move: stop", conductor_verdict("no section", {})["action"], "stop")
    # E18: the class the stub saw
    check("E18: dry as the first line passes", run_class_problem([{"first": True, "run_class": "dry"}]) == "")
    check("E18: a missing class is red", "run class not propagated" in run_class_problem([{"first": True, "run_class": ""}]))
    check("E18: an empty journal is red", "run class not propagated" in run_class_problem([]))
    # E16: a snapshot not made by this run, and one that is not there
    world = W.World({"id": "t", "task": "T-1"}, tmp / "proj", {}, None, tmp / "snaps")
    (tmp / "proj").mkdir()
    snap = W.snapshot(world, "S0")
    check("E16: a snapshot of this run is copied", W.from_snapshot(world, "S0").root.is_dir())
    marker = snap / ".dry-snapshot.json"
    marker.write_text(json.dumps({"label": "other", "from": str(tmp / "proj")}), encoding="utf-8")
    try:
        W.from_snapshot(world, "S0")
        got = "no refusal"
    except W.SnapshotError as exc:
        got = str(exc)
    check("E16: a snapshot of another run is refused", "snapshot not from this run" in got, got)
    try:
        W.from_snapshot(world, "S9")
        got = "no refusal"
    except W.SnapshotError as exc:
        got = str(exc)
    check("E16: a snapshot the main pass never made is named missing", "not found" in got, got)
    check_eq("gate: the numbers of the spec", (W.gate_verdict(100, 10, 15), W.gate_verdict(200, 10, 15), W.gate_verdict(100, 30, 40), W.gate_verdict(301, 5, 5), W.gate_verdict(10, 5, 61)),
             ("continue", "narrow", "narrow", "stop", "stop"))
    selftest_n2(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    finish("dry_stub --selftest")
    return 0


def selftest_n2(tmp: Path) -> None:
    """The rows of node N2: the story kit and the runner table, the role branch (S2 through the filler, `Unfillable`, overrides and the repair round),
    the automator (the world's profile commands, the manifest fragment), the conductor (every open move, the row's variant, the move's command,
    `conductor_judgment`), the journal and the receipt, and `dry_driver.py`. The calls go through the stub as a PROCESS, the way the driver runs it."""
    import harness as H
    import dry_driver
    import form_filler as FF
    import no_move as NM
    import scenario_walk as SW
    from harness import check, check_eq
    kit = load_kit("dry-1")
    story = SW.load_story("dry-1")
    check_eq("N2 item 6: scenario_walk.load_story reads dry-1: id, task, synthetic, the nine stages", (story.id, story.task, [e["stage"] for e in story.walk]),
             ("dry-1", "DRY-1", [f"S{n}" for n in range(1, 10)]))
    check_eq("N2 item 6: the kit holds two requirements, one automated case and one manual case, and names the first runner row",
             ([c["id"] for c in kit["cases"] if c["channel"] == "auto"], [c["id"] for c in kit["cases"] if c["channel"] == "manual"], kit["requirements"],
              [r["id"] for r in runner_rows()], kit["runner"]), (["TC-1"], ["TC-2"], ["R-1", "R-2"], ["python-pytest"], "python-pytest"))
    # an unreadable story file is a red line naming the file; an empty runners folder is a refusal naming it
    def broken(name, files):
        folder = tmp / name
        for rel_path, text in files.items():
            (folder / rel_path).parent.mkdir(parents=True, exist_ok=True)
            (folder / rel_path).write_text(text, encoding="utf-8")
        return folder
    good_story, good_kit = (STORIES / "dry-1" / "story.json").read_text(encoding="utf-8"), (STORIES / "dry-1" / "kit.json").read_text(encoding="utf-8")
    for name, files, needle in (("n2-story-bad", {"s/story.json": "{nope", "s/kit.json": good_kit}, "story.json: not valid JSON"),
                                ("n2-story-empty", {"s/story.json": "", "s/kit.json": good_kit}, "story.json: the file is empty"),
                                ("n2-kit-missing", {"s/story.json": good_story}, "kit.json: cannot be read"),
                                ("n2-kit-list", {"s/story.json": good_story, "s/kit.json": "[]"}, "kit.json: holds list"),
                                ("n2-kit-other-task", {"s/story.json": good_story, "s/kit.json": good_kit.replace('"DRY-1"', '"DRY-2"')}, "is not the `task`"),
                                ("n2-kit-no-case", {"s/story.json": good_story, "s/kit.json": good_kit.replace('"auto"', '"both"')}, "`cases` is not")):
        try:
            load_kit("s", broken(name, files))
            got = "no refusal"
        except KitError as exc:
            got = str(exc)
        check(f"N2 edge: {name} is red naming the file", needle in got and ("kit.json" in got or "story.json" in got), got)
    for name, make in (("absent", lambda f: None), ("empty", lambda f: (f / "runners").mkdir(parents=True))):
        folder = tmp / f"n2-runners-{name}"
        make(folder / "s")
        try:
            runner_rows("s", folder)
            got = "no refusal"
        except KitError as exc:
            got = str(exc)
        check(f"N2 edge: a runners folder that is {name} is a refusal naming it", "no runner row" in got and "runners" in got, got)

    def world(tag, commands=True):
        project = H.temp_project(f"qa-dry-n2-{tag}-")
        install_runner(project, runner_row(kit["runner"]))
        if not commands:                      # a COPY of the profile without `commands`: the world's own config row, the packaged row stays as it is
            cfg = read_json(config_path(project))
            for profile in cfg["profiles"]:
                profile.pop("commands", None)
            config_path(project).write_text(json.dumps(cfg), encoding="utf-8")
        task_dir = project / "qa-factory" / "artifacts" / "DRY-1"
        (task_dir / "work").mkdir(parents=True)
        return project, task_dir

    def call(project, control, prompt, *argv, run_class="dry"):
        control_file = project / "dry-stub-control.json"
        control_file.write_text(json.dumps(control), encoding="utf-8")
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project), DRY_STUB_CONTROL=str(control_file), PYTHONDONTWRITEBYTECODE="1")
        env.pop("STORY_RUN_CLASS", None)
        if run_class is not None:
            env["STORY_RUN_CLASS"] = run_class
        done = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), *argv], input=prompt.encode("utf-8"), capture_output=True, env=env,
                              cwd=str(project), timeout=300)
        out = done.stdout.decode("utf-8", "replace").strip().splitlines()
        return done.returncode, (json.loads(out[-1]) if out else {}), done.stderr.decode("utf-8", "replace")

    def form(project, task_dir, stage, role, dispatch):
        done = H.run_script("handoff_init.py", "--task", "DRY-1", "--stage", stage, "--role", role, "--dispatch", dispatch, "--task-root", str(task_dir), cwd=project)
        return done.returncode, (done.stderr or done.stdout)[-300:]

    def rows(task_dir):
        path = task_dir / "state" / "dry-stub.jsonl"
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.is_file() else []

    role_arg = ("-p", "--agent", "qa-factory:qa-requirements-tester")
    control = {"task": "DRY-1", "story": "dry-1"}
    # N2 (1), (3), (4), (5): the S2 role writes the register and the form through the filler; the same input gives the same bytes; the session id carries the dispatch
    # and a counter per dispatch; the journal opens with the run class and every row carries it
    saved = []
    for tag in ("a", "b"):
        project, task_dir = world(tag)
        code, text = form(project, task_dir, "S2", "qa-requirements-tester", "D2")
        check(f"N2 (1): handoff_init made the S2 form (world {tag})", code == 0, text)
        prompt = f"Artifacts dir: {task_dir}\nDispatch: D2.\n"
        template = (task_dir / "work" / "handoffs" / "D2.yaml").read_bytes()
        rc, answer, err = call(project, control, prompt, *role_arg)
        check_eq(f"N2 (1): the S2 call answers a result with the session `stub-D2-1` (world {tag})", (rc, answer.get("type"), answer.get("session_id")), (0, "result", "stub-D2-1"))
        register = task_dir / "work" / "requirements-register.md"
        handover = (task_dir / "work" / "handoffs" / "D2.yaml")
        got = rows(task_dir)
        left = FF.HINT.findall(handover.read_text(encoding="utf-8")) if handover.is_file() else ["no form"]
        template_hints = FF.HINT.findall(template.decode("utf-8"))
        check_eq(f"N2 (1): the register and the form are written by the filler (the form has fewer hints than the template; the rest are code's fields), no live_only (world {tag})",
                 (register.is_file(), handover.is_file(), got[1]["live_only"], len(left) < len(template_hints)), (True, True, [], True))
        saved.append((register.read_bytes(), handover.read_bytes()))
        if tag == "a":
            rc, second, err = call(project, control, prompt, *role_arg)
            rc3, other, err = call(project, control, f"Artifacts dir: {task_dir}\nDispatch: D3.\n", *role_arg)
            check_eq("N2 (4): the counter is per dispatch: D2 again is 2, D3 starts at 1", (second.get("session_id"), other.get("session_id")), ("stub-D2-2", "stub-D3-1"))
            check_eq("N2 (5): the first line of the journal is the run class the stub saw, and every row carries it",
                     (got[0].get("run_class"), all(r.get("run_class") == "dry" for r in rows(task_dir))), ("dry", True))
            check_eq("N2 (5): the journal sits at state/dry-stub.jsonl of the task", (task_dir / "state" / "dry-stub.jsonl").is_file(), True)
            rc, _a, _e = call(project, control, f"Artifacts dir: {task_dir}\nDispatch: D4.\n", *role_arg, run_class=None)
            check_eq("N2 (5) / E18: with no class in the environment the row says so (the walker turns it red)", rows(task_dir)[-1].get("run_class"), "")
    check_eq("N2 (3): the same input gives the same bytes: register and form of two worlds are identical", saved[0], saved[1])
    # N2 (1): an output with no filler kind is an `Unfillable` naming the form and the field, never a text; the row it leaves is live_only
    ctx = kit_context(kit, "D9")
    for output, form_needle, field_needle in (("work/s5-plan.json", "work/s5-plan.json", ""), ("test_file:typescript", "test_file:typescript", "marker")):
        try:
            fill_output(output, ctx)
            got = ("no refusal", "")
        except Unfillable as exc:
            got = (exc.form, exc.field)
        check(f"N2 (1): {output} raises Unfillable with the form {form_needle!r} and the field {field_needle!r}", got == (form_needle, field_needle), f"{got}")
    try:
        fill_handover("references/no-such-contract.md", ctx)
        got = "no refusal"
    except Unfillable as exc:
        got = exc.form
    except Exception as exc:               # noqa: BLE001 - the filler itself names a contract it cannot read in its own words
        got = f"{type(exc).__name__}"
    check("N2 (1): a contract the filler cannot place is not a text either (an Unfillable or the filler's own refusal)", got != "no refusal", got)
    # overrides and the repair round come from the row
    check_eq("N2 row: overrides apply before the repair round and not from it", (overrides_for({"overrides": {"f": {"a.b": 1}}, "repair_on_round": 2}, "f", 1),
             overrides_for({"overrides": {"f": {"a.b": 1}}, "repair_on_round": 2}, "f", 2), overrides_for({"overrides": {"f": {"a.b": ABSENT_JSON}}}, "f", 5)),
             ({"a.b": 1}, {}, {"a.b": FF.ABSENT}))
    contract = FORM_CONTRACT.search(template.decode("utf-8")).group(1)
    base_form = fill_handover(contract, kit_context(kit, "D2"))
    key = next(f.path for f in base_form.fills if f.rule not in ("verdict", "override") and isinstance(f.value, str))        # a field the rules filled with a text
    seeded = fill_handover(contract, kit_context(kit, "D2"), overrides=overrides_for({"overrides": {contract: {key: "seeded-by-the-row"}}, "repair_on_round": 2}, contract, 1))
    repaired = fill_handover(contract, kit_context(kit, "D2"), overrides=overrides_for({"overrides": {contract: {key: "seeded-by-the-row"}}, "repair_on_round": 2}, contract, 2))
    check_eq("N2 row: an override of the row reaches the filled form on round 1 and is gone on the repair round (bytes equal to the clean fill)",
             ("seeded-by-the-row" in seeded.text, seeded.text != base_form.text, repaired.text == base_form.text), (True, True, True))
    # N2 (2), (6): the automator, the world's profile
    for tag, commands in (("auto", True), ("nocmd", False)):
        project, task_dir = world(tag, commands)
        code, text = form(project, task_dir, "S5", "qa-automator", "A5")
        check(f"N2 (6): handoff_init made the S5 form (world {tag})", code == 0, text)
        decoy = "Run `python -m pytest decoy-from-the-brief` to prove the case.\n"
        rc, answer, err = call(project, control, f"Artifacts dir: {task_dir}\nDispatch: A5.\n{decoy}", "-p", "--agent", "qa-factory:qa-automator")
        row = rows(task_dir)[1]
        check_eq(f"N2 (2): the automator call answers `stub-A5-1` (world {tag})", (rc, answer.get("session_id")), (0, "stub-A5-1"))
        if commands:
            check_eq("N2 (2): the test file of the automated case is written by the filler and the command is the profile's own (exit 0, not the brief's)",
                     ([r["argv"] for r in row.get("ran", [])], [r["exit"] for r in row.get("ran", [])], (project / "qa-factory" / "tests" / "TC-1_test.py").is_file(),
                      "decoy" in json.dumps(row)), ([["python", "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "qa-factory/tests"]], [0], True, False))
            check("N2 (2): the manifest fragment of the case was merged by manifest_put.py (exit 0)", "work/automation-manifest.json" in row["wrote"], json.dumps(row)[:600])
        else:
            check("N2 (6): a profile without `commands` is `no command` in the journal, nothing is run, and the brief's command is not looked for",
                  "no command" in row.get("no_command", "") and row.get("ran") == [] and "decoy" not in json.dumps(row.get("ran")), json.dumps(row)[:600])
    # N2 (2)-(3): the conductor
    spec = NM.data()
    offerable = [mid for mid, mrow in NM.move_rows(spec).items() if NM.move_columns(mrow, strict=False)[1] and NM.move_columns(mrow, strict=False)[0] is None
                 and str(mrow.get("token") or "") not in ("", "—")][:3]
    prompt = NM.moves_section(spec, offerable, {}) + "\n\nSomething refused.\n"
    project, task_dir = world("cond")
    rc, answer, err = call(project, control, prompt)
    verdict = json.loads(answer["result"].split("\n", 1)[1]) if answer else {}
    words = (NM.hooklib.load_ref_json(NM.VERDICTS_FILE) or {}).get("words") or {}
    options, rule_text = NM.validate_options(verdict, offerable, spec, lambda s: s.strip().lower(), words)
    check_eq("N2 (2): the conductor answers `ask_person` offering every open move, session `stub-conductor-1`",
             (answer.get("session_id"), verdict.get("action"), [o["move"] for o in verdict.get("options", [])]), ("stub-conductor-1", "ask_person", offerable))
    check("N2 item 3: the answer passes no_move.validate_options", options is not None and len(options) == len(offerable), rule_text)
    first = NM.move_rows(spec)[offerable[0]]
    check_eq("N2 item 3: every line of an option is the move's own row, no text of the stub's", (verdict["options"][0]["says"], verdict["options"][0]["token"]),
             (first["says"].strip(), first["token"]))
    tokens = [o["token"] for o in verdict["options"]]
    rc, answer, err = call(project, dict(control, conductor={"variant": tokens[-1], "why_person": "decision", "checked": "the gate card"}), prompt)
    verdict = json.loads(answer["result"].split("\n", 1)[1])
    check_eq("N2 item 3: the row's variant narrows the offer and its why_person / checked are the row's; the counter runs on",
             (answer["session_id"], [o["token"] for o in verdict["options"]], verdict["why_person"], verdict["checked"]), ("stub-conductor-2", [tokens[-1]], "decision", "the gate card"))
    rc, answer, err = call(project, dict(control, conductor={"variant": "no-such-token"}), prompt)
    verdict = json.loads(answer["result"].split("\n", 1)[1])
    check("N2 edge: a variant the prompt does not offer is a `stop` naming it, never an invented option", verdict["action"] == "stop" and "no-such-token" in verdict["did"], str(verdict))
    # E3: the move's own command, and the move no command fills without judgment
    moves = NM.move_rows(spec)
    ran = conductor_execute({"move": "rework_stage", "run": [["case_versions.py", "--all"]]}, project, task_dir, "DRY-1", run=lambda *a: (0, "never"))
    check("E3: a command that is not the move's own is refused naming it and nothing runs", "is not the move's own" in ran.get("refused", "") and ran["ran"] == [], str(ran))
    seen = []
    ran = conductor_execute({"move": "rework_stage", "run": [["controller.py", "--task-root", "{task_root}", "--operation", "stage-scope"]]}, project, task_dir, "DRY-1",
                            run=lambda p, s, a: (seen.append((s, a)) or (0, "ok")))
    check_eq("E3: the move's own script runs with the row's arguments, `{task_root}` filled", seen, [("controller.py", ["--task-root", str(task_dir), "--operation", "stage-scope"])])
    ran = conductor_execute({"move": "rework_stage", "executor": "conductor_judgment"}, project, task_dir, "DRY-1", run=lambda *a: (_ for _ in ()).throw(AssertionError("ran")))
    check_eq("E3: a move that needs judgment is `executor: conductor_judgment`, nothing runs, never counted as run", (ran["executor"], ran["ran"]), ("conductor_judgment", []))
    check("E3: a move the data does not hold is refused", "no move `nope`" in conductor_execute({"move": "nope"}, project, task_dir, "DRY-1").get("refused", ""))
    rc, answer, err = call(project, dict(control, conductor={"execute": {"move": "rework_stage", "executor": "conductor_judgment"}}), prompt)
    check_eq("E3: through the process: the journal row of the conductor carries `executed`, the answer is `continue`", (json.loads(answer["result"].split("\n", 1)[1])["action"],
             rows(task_dir)[-1]["executed"]["executor"]), ("continue", "conductor_judgment"))
    # E4: the counter is read from the journal, one file, so two dispatches never share an index (the stub never waits for anyone)
    counted = rows_dir(tmp, "n2-count", [("D2", 2), ("D3", 1)])
    check_eq("E4: the counters are per key in the journal (D2: 2 calls, D3: 1), never a shared index", (calls_before(counted, "D2"), calls_before(counted, "D3")), (2, 1))
    # dry_driver.py: a spy that passes, and no attribute of the driver's class assigned (a grep over the owned files, with its positive control)
    seen = []
    spy = dry_driver.passing_spy(lambda key, options, *a, **k: (seen.append(key) or [{"token": None}]), tmp / "n2-priced" / "dry-priced.jsonl")
    answered = spy("s1.gap", [{"answer": "go on"}, {"answer": "stop"}], {}, {})
    check_eq("N2 item 5: the spy returns what the real function returned and records {key, answers}",
             (answered, [json.loads(l) for l in (tmp / "n2-priced" / "dry-priced.jsonl").read_text(encoding="utf-8").splitlines()]),
             ([{"token": None}], [{"key": "s1.gap", "answers": ["go on", "stop"]}]))
    try:
        dry_driver.passing_spy(lambda *a, **k: (_ for _ in ()).throw(ValueError("unreadable prices")), tmp / "n2-priced" / "never.jsonl")("k", [])
        got = "no error"
    except ValueError:
        got = "raised"
    check_eq("N2 item 5: a refusal of the real function passes through and nothing is recorded", (got, (tmp / "n2-priced" / "never.jsonl").exists()), ("raised", False))
    check_eq("N2 item 5: the sink is the task's state folder of the call's own --project and --task",
             dry_driver.sink_path(["--project", "P", "--task", "T", "--x"]), Path("P") / "qa-factory" / "artifacts" / "T" / "state" / "dry-priced.jsonl")
    check("N2 edge: no --project or --task is None, the wrapper refuses naming them", dry_driver.sink_path(["--task", "T"]) is None)
    pattern = re.compile(r"\bDri" + r"ver\.\w+\s*=[^=]")
    owned = [Path(__file__).resolve(), Path(__file__).resolve().with_name("dry_driver.py")]
    check("N2 item 5: positive control of the grep: the pattern finds an assignment to an attribute of the driver's class", pattern.search("Dri" + "ver.run = spy") is not None)
    check("N2 item 5: positive control of the grep: it finds the assignment the wrapper does make (the one module attribute)",
          re.search(r"\bno_move\.priced_options\s*=[^=]", owned[1].read_text(encoding="utf-8")) is not None)
    check("N2 item 5: no owned file assigns an attribute of the driver's class", not [str(p) for p in owned if pattern.search(p.read_text(encoding="utf-8"))])


def rows_dir(tmp: Path, name: str, calls: list) -> Path:
    """A task folder whose stub journal holds one row per call of `calls` (`[(key, how many)]`)."""
    folder = tmp / name
    (folder / "state").mkdir(parents=True, exist_ok=True)
    (folder / "state" / "dry-stub.jsonl").write_text("\n".join([json.dumps({"first": True, "run_class": "dry"})] + [json.dumps({"dispatch": k, "n": i + 1})
                                                      for k, count in calls for i in range(count)]) + "\n", encoding="utf-8")
    return folder


def main(argv: list) -> int:
    if "--selftest" in argv:
        return selftest()
    if "--spike" in argv:
        import dry_world
        return dry_world.main(argv)
    return claude_main(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
