#!/usr/bin/env python3
"""The measurers of this experiment, against a run whose arithmetic is known.

A measurer is code and gets a test like any other code (factory rule FR-28). These nine scripts
had none, and two of them published wrong numbers in run 5 before anybody noticed:

  * the retro roll-up counted the operator's own session as the story's money — $1,911 against
    the $128 actually charged (FR-24), because it took every session that MENTIONED the ticket;
  * `report_run.py --left-cache` defaulted to the cached measurement of the baseline and applied it
    to whatever `--left` named, so every comparison printed the baseline on the left: "the left run
    $109.00 vs $128.53", where the left run had cost $62.08 (FR-27);
  * and the family table of `conductor_families.py` was first computed by grouping distinct
    FIRST LINES instead of sessions, which under-counted threefold (7/5/2 instead of 18/18/5).

Each of those is a case here, and each fails without its fix. The rest is the arithmetic every
published number of the delivery rests on: the total, the conductor's share, the first dispatch
of a (stage, role) against its repeats, and the price of a resumed turn against a fresh one.

    python -B experiments/measurers/test_measurers.py

The fixture is a whole run in a temp directory — a driver journal, a conductor journal, a
controller state and two transcripts — small enough that every expected number is visible here
in the test rather than copied from an output.
"""
import json
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TICKET = "QA-1"
RUN = "fixture"
MODEL = "claude-sonnet-4-20250514"
RESULTS = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    RESULTS.append((bool(ok), name))
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail and not ok else ""))
    return bool(ok)


def check_eq(name: str, got, expected) -> bool:
    return check(name, got == expected, f"expected {expected!r}, got {got!r}")


# --- the fixture ------------------------------------------------------------------------------
# Four role sessions and one conductor session. The numbers are chosen so that every figure the
# delivery publishes divides cleanly:
#   total 3.75 | conductor 0.25 (7%) | first dispatch of (S1, qa-scout) 1.50, its repeat 2.00
#   fresh 3.00 over 20 turns = 0.1500/turn | resumed 0.50 over 5 turns = 0.1000/turn
DRIVER_RUNS = [
    {"kind": "role", "role": "qa-scout", "stage": "S1", "dispatch": "S1-qa-scout-1",
     "session_id": "sess-a", "total_cost_usd": 1.00, "num_turns": 10, "resumed": False},
    {"kind": "role", "role": "qa-scout", "stage": "S1", "dispatch": "S1-qa-scout-1",
     "session_id": "sess-b", "total_cost_usd": 0.50, "num_turns": 5, "resumed": True},
    {"kind": "role", "role": "qa-scout", "stage": "S1", "dispatch": "S1-qa-scout-2",
     "session_id": "sess-c", "total_cost_usd": 2.00, "num_turns": 10, "resumed": False},
    {"kind": "conductor", "stage": "S1", "session_id": "sess-d", "total_cost_usd": 0.25,
     "num_turns": 5},
]
# Three sessions raised for ONE refusal, word for word, and one for another. A table grouped by
# distinct text would report the first family as 1.
REPEATED = ("story_step finish S1-qa-scout-1 (exit 2): story_step: refused - "
            "the qa-code-critic window is not receipted for this dispatch")
CONDUCTOR = [
    {"refusal": REPEATED, "action": "ask_person", "did": "", "total_cost_usd": 0.10, "num_turns": 4},
    {"refusal": REPEATED, "action": "ask_person", "did": "", "total_cost_usd": 0.10, "num_turns": 4},
    {"refusal": REPEATED, "action": "continue", "did": "ran waiver.py", "total_cost_usd": 0.10,
     "num_turns": 4},
    {"refusal": "story_step start (exit 2): story_step: refused - sequential task already has an "
                "active dispatch S1-qa-scout-2",
     "action": "continue", "did": "No command run", "total_cost_usd": 0.05, "num_turns": 2},
]


def transcript(session: str, role_line: str, requests: list) -> str:
    """A session transcript the way `compare.scan` reads one: the first user turn names the role,
    every assistant turn with a `usage` block is one priced request."""
    lines = [json.dumps({"type": "user", "timestamp": "2026-09-27T00:00:00Z",
                         "message": {"content": role_line}})]
    for index, usage in enumerate(requests):
        lines.append(json.dumps({"type": "assistant", "timestamp": "2026-09-27T00:01:00Z",
                                 "uuid": f"{session}-{index}",
                                 "message": {"id": f"msg-{session}-{index}", "model": MODEL,
                                             "usage": usage, "content": []}}))
    return "\n".join(lines) + "\n"


def build(root: Path) -> Path:
    task = root / "copies" / RUN / "test-harness" / "qa-factory" / "artifacts" / TICKET
    (task / "state").mkdir(parents=True)
    (task / "state" / "driver-runs.jsonl").write_text(
        "\n".join(json.dumps(row) for row in DRIVER_RUNS) + "\n", encoding="utf-8")
    (task / "state" / "conductor.jsonl").write_text(
        "\n".join(json.dumps(row) for row in CONDUCTOR) + "\n", encoding="utf-8")
    (task / "state" / "controller.json").write_text(json.dumps({"dispatches": {
        "S1-qa-scout-1": {"status": "accepted"}, "S1-qa-scout-2": {"status": "accepted"}}}),
        encoding="utf-8")
    (task / "pipeline.json").write_text(json.dumps({"ticket": TICKET, "stages": {
        "S1": {"status": "done", "started": "2026-09-27T00:00:00+00:00",
               "finished": "2026-09-27T01:00:00+00:00"}}}), encoding="utf-8")

    # 1M input tokens at $3/M = $3.00 for the session the journal owns, and a session it does
    # not own, twice as expensive, that must not reach the story's money (FR-24).
    tdir = root / "transcripts"
    tdir.mkdir()
    (tdir / "sess-a.jsonl").write_text(
        transcript("sess-a", f"qa-scout on {TICKET}", [{"input_tokens": 1_000_000}]), encoding="utf-8")
    (tdir / "operator.jsonl").write_text(
        transcript("operator", f"my own session about {TICKET}", [{"input_tokens": 2_000_000}]),
        encoding="utf-8")
    return task


# --- the measurers that had no test: stage_compare, code_friction, context_shape, check_all_contracts,
# paths.py and the catalogue they price from ---------------------------------------------------------
# Hand values below are computed from the catalogue's own rates (per million tokens):
#   claude-sonnet-5-5  input 2, output 10, cache_read 0.1, cache_write_5m 2.5, cache_write_1h 4   (page rate; cache_read 0.1, not the 0.2 of the old table)
#   claude-opus-5-5    input 4, output 20, cache_read 0.2, cache_write_5m 5,   cache_write_1h 8
SYNTH_PREFIX = "synth-" + "copy-"                  # built from parts: this file must not trip its own guard
SYNTH_FOLDER = "synth-" + "folder-" + "base-off"


def guard_literals(table: dict) -> list:
    """The strings no measurer may spell by hand: the folder and prefix values of a runs table. They are data of
    the table now (QA_RUNS_TABLE), so the list is the synthetic table of this test plus, when one is set, the
    real table of the experiment."""
    values = [SYNTH_FOLDER, SYNTH_PREFIX]
    values += [v for v in (table.get("baselines") or {}).values()]
    values += [v for v in (table.get("story_runs") or {}).values()]
    if table.get("copy_prefix"):
        values.append(table["copy_prefix"])
    return sorted(set(v for v in values if v))


def literal_hits(directory: Path, literals: list | None = None) -> dict:
    """{file name: [literals]} for every experiment script that spells a run folder or a copy prefix by hand.
    No script, paths.py included, may name one: the runs table is the one place a run name becomes a folder.
    Without a table this looks only for the two synthetic literals, so it is a weak guard in the CI form; the real
    protection is the export scanner (docs/migration/scrub_scan.py)."""
    import paths
    literals = guard_literals(paths.TABLE) if literals is None else literals
    hits = {}
    for path in sorted(directory.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        found = [lit for lit in literals if lit in text]
        if found:
            hits[path.name] = found
    return hits


def sample_dir(what: str):
    """The sample run's folder (`sample_task` of the runs table), or None after ONE named SKIP line: the three
    sample-run checks share this condition and this text."""
    import paths
    sample = paths.table_path("sample_task")
    if sample is not None and sample.is_dir():
        return sample
    print(f"SKIP {what} on the sample run (no sample_task in the runs table, or its folder is not in this tree)")
    return None


def tx(mid, model, usage, tool=None, result=None) -> list:
    """The lines of one assistant turn (and the result of its tool call) the way a transcript has them."""
    content = [{"type": "tool_use", "id": "tu-" + mid, "name": tool[0], "input": {"command": tool[1]}}] if tool else []
    lines = [json.dumps({"type": "assistant", "message": {"id": mid, "model": model, "usage": usage,
                                                          "content": content}})]
    if result is not None:
        lines.append(json.dumps({"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "tu-" + mid, "content": result}]}}))
    return lines


def run_main(module, argv) -> tuple:
    """(exit code, printed text) of `module.main()` with the given command line."""
    import io
    import contextlib
    buffer, old = io.StringIO(), sys.argv
    sys.argv = [module.__name__ + ".py", *argv]
    try:
        with contextlib.redirect_stdout(buffer):
            code = module.main()
    finally:
        sys.argv = old
    return code, buffer.getvalue()


def more(root: Path, base: Path) -> None:
    import io
    import contextlib
    import os
    import subprocess
    import compare
    import paths

    # --- paths.py: the one place the package and the runs are found ---------------------------
    check("the package is found from paths.py's own location, not from a typed path",
          paths.PACKAGE.is_dir() and paths.RATES.is_file() and paths.SCRIPTS.is_dir()
          and paths.HANDOFFS.is_dir(), f"{paths.PACKAGE}")
    check_eq("the transcript folder key is every non-alphanumeric turned into a dash, as Claude Code does",
             paths.transcript_key("D:\\runs\\copy-run3\\test-harness"),
             "D--runs-copy-run3-test-harness")
    check("and transcript_dir is that key under ~/.claude/projects",
          paths.transcript_dir(r"C:\x\y") == Path.home() / ".claude" / "projects" / "C--x-y")
    env = dict(os.environ, QA_RUNS_BASE=str(root / "elsewhere"))
    env.pop("QA_RUNS_TABLE", None)       # the developer's environment must not decide the outcome (edge 9)
    shown = subprocess.run([sys.executable, "-B", "-c", "import paths; print(paths.BASE)"], cwd=HERE,
                           env=env, capture_output=True, text=True).stdout.strip()
    check_eq("QA_RUNS_BASE moves the runs folder", shown, str(root / "elsewhere"))

    # --- the guard: no script keeps a run folder or a copy prefix --------------------------------
    check_eq("no experiment script spells a run folder or a copy prefix of the runs table",
             literal_hits(HERE), {})
    control = root / "guard-control"
    control.mkdir()
    (control / "compare.py").write_text(
        (HERE / "compare.py").read_text(encoding="utf-8")
        + f'\nOLD = r"D:/runs/{SYNTH_FOLDER}/ai-packages"\n', encoding="utf-8")
    (control / "paths.py").write_text((HERE / "paths.py").read_text(encoding="utf-8"), encoding="utf-8")
    check_eq("negative control: the same guard fails on a copy of a script with a table literal put back",
             literal_hits(control), {"compare.py": [SYNTH_FOLDER]})

    # --- the catalogue: the two models the comparison run is on ------------------------------
    rate = compare.rates()
    check("the catalogue prices claude-sonnet-5-5 and claude-opus-5-5", "claude-sonnet-5-5" in rate
          and "claude-opus-5-5" in rate)
    usage = {"input_tokens": 1_000_000, "output_tokens": 100_000, "cache_read_input_tokens": 2_000_000,
             "cache_creation": {"ephemeral_5m_input_tokens": 1_000_000,
                                "ephemeral_1h_input_tokens": 500_000}}
    # opus-5-5: 4 + 2 + 0.4 + 5 + 4 = 15.4 ; sonnet-5-5 (cache_read 0.1): 2 + 1 + 2M*0.1 = 0.2 + 2.5 + 2 = 7.7
    check_eq("price() of a fixed usage on claude-opus-5-5 is the hand value",
             round(compare.price(rate, "claude-opus-5-5", usage), 6), 15.4)
    check_eq("and on claude-sonnet-5-5", round(compare.price(rate, "claude-sonnet-5-5", usage), 6), 7.7)
    check_eq("an entry without the rate of a token kind the request used is unpriced, not a KeyError",
             compare.price({"m": {"input": 2}}, "m", {"input_tokens": 1, "output_tokens": 1}), None)
    check_eq("and the same entry prices a request that used only the kinds it has",
             round(compare.price({"m": {"input": 2}}, "m", {"input_tokens": 1_000_000}), 6), 2.0)
    check_eq("a model with no cache-write rate is unpriced for a request that wrote cache",
             compare.price(rate, "gpt-5.5", {"input_tokens": 10, "cache_creation_input_tokens": 5}), None)
    check_eq("a turn with no usage costs 0 whatever its model", compare.price_turn(
        rate, "<synthetic>", {"input_tokens": 0, "output_tokens": 0}), 0.0)
    check_eq("a synthetic turn WITH usage is unpriced", compare.price_turn(
        rate, "<synthetic>", {"input_tokens": 5}), None)
    check_eq("a turn with no model and usage is unpriced", compare.price_turn(
        rate, None, {"input_tokens": 5}), None)

    # --- stage_compare ------------------------------------------------------------------------
    import stage_compare
    stage_compare.BASE, stage_compare.RUNS, stage_compare.TASK = base, {RUN: RUN}, TICKET
    work = base / RUN / "test-harness/qa-factory/artifacts" / TICKET / "work"
    work.mkdir(parents=True, exist_ok=True)
    register = work / "requirements-register.md"
    register.write_text("| id | text |\n|---|---|\n| R-1 | a |\n| R-2 | b |\n| R-3 | c |\nR-9 in prose\n",
                        encoding="utf-8")
    check_eq("count_rows counts the table rows that match, not every mention",
             stage_compare.count_rows(register, r"^\|\s*R-\d+"), 3)
    check_eq("and a file that is not there is None, not zero",
             stage_compare.count_rows(None, r"^\|\s*R-\d+"), None)
    check_eq("counter: a column becomes its distribution, biggest first",
             stage_compare.counter(["passed", "failed", "passed"]), "passed=2,failed=1")
    check_eq("counter: ties break by name, and an empty column is empty",
             (stage_compare.counter(["b", "a"]), stage_compare.counter([])), ("a=1,b=1", ""))
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        stage_compare.s2()
    printed = buffer.getvalue()
    check("stage S2 prints the register row count of the run it was pointed at",
          f"{'register_rows(R-n)':24} | {'3':22}" in printed and "## S2" in printed, printed[:300])
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        stage_compare.s6()
    check("a stage whose artifact is absent says none, it does not crash",
          f"{'run_report':24} | {'none':22}" in buffer.getvalue(), buffer.getvalue()[:300])

    # --- code_friction: money by the turn's own model -----------------------------------------
    import code_friction
    crash = "Traceback (most recent call last):\n  File x\nValueError: boom"
    for name, text, want in (
            ("a traceback", crash, "crash"),
            ("a traceback inside a typed broken_run result", crash + ' "execution_status": "broken_run"', "stand"),
            ("a guard refusal", "pre-tool guard refused this write", "guard"),
            ("argparse's usage dump", "usage: foo.py [-h] [--x X]", "usage"),
            ("a validator refusal", "story is not ready: two rows lack a verdict", "validator"),
            ("a working result", "wrote 3 rows", None),
            ("a numbered file listing that mentions refusing", "1\tthe validator refuses rows", None),
            ("nothing at all", "", None), ("None", None, None)):
        check_eq(f"classify: {name}", code_friction.classify(text), want)

    session = root / "friction.jsonl"
    lines = []
    lines += tx("m1", "claude-sonnet-5-5", {"input_tokens": 1_000_000, "output_tokens": 100_000,
                                            "cache_read_input_tokens": 2_000_000},
                ("Bash", "python a.py"), crash)                                     # 2 + 1 + 2M*0.1 = 0.2 -> 3.20
    lines += tx("m2", "claude-opus-5-5", {"input_tokens": 500_000, "output_tokens": 50_000,
                                          "cache_creation": {"ephemeral_5m_input_tokens": 1_000_000,
                                                             "ephemeral_1h_input_tokens": 100_000}},
                ("Bash", "python b.py"), "ok")                                      # 2 + 1 + 5 + 0.8 = 8.80
    lines += tx("m3", "no-such-model", {"input_tokens": 1_000_000},
                ("Bash", "python foo.py"), "usage: foo.py [-h]")                    # unknown: unpriced
    lines += tx("m4", "<synthetic>", {"input_tokens": 0, "output_tokens": 0})       # no usage: 0
    lines += tx("m1", "claude-sonnet-5-5", {"input_tokens": 9_999_999})             # a repeat of m1: not a new turn
    session.write_text("\n".join(lines) + "\n", encoding="utf-8")
    got = code_friction.friction(session)
    check_eq("friction: four unique turns, the repeat of a message id is not a fifth", got["turns"], 4)
    check_eq("friction: money is each turn's own catalogue value (sonnet-5-5 3.20 + opus-5-5 8.80)",
             round(got["cost"], 6), 12.0)
    check_eq("friction: the unknown-model turn is counted unpriced, not priced at a fallback", got["unpriced"], 1)
    check_eq("friction: the crash and the usage dump are the two friction turns",
             (got["fric_turns"], dict(got["tally"])), (2, {"crash": 1, "usage": 1}))
    check_eq("friction: an unpriced friction turn adds no dollars", round(got["fric_cost"], 6), 3.2)
    empty = root / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    zero = code_friction.friction(empty)
    check_eq("friction: an empty transcript is zero totals, not a crash",
             (zero["turns"], zero["cost"], zero["fric_turns"], zero["unpriced"]), (0, 0, 0, 0))

    code_friction.BASE, code_friction.RUNS, code_friction.TASK = base, {RUN: RUN}, TICKET
    code_friction.project_dir = lambda run: root / "transcripts"
    code, printed = run_main(code_friction, [RUN])
    check("code_friction over the fixture run prices sess-a at its catalogue value and prints the unpriced line",
          code == 0 and "3.00" in printed and "unpriced turns: 0" in printed, printed[:600])
    nowhere = root / "no-journal"
    code_friction.BASE = nowhere
    code, printed = run_main(code_friction, [RUN])
    check("code_friction on a run without driver-runs.jsonl names the missing file and does not crash",
          code == 0 and "no driver journal for" in printed and "driver-runs.jsonl" in printed, printed[:400])

    # --- context_shape ------------------------------------------------------------------------
    import context_shape
    shape = root / "shape.jsonl"
    body = "x" * 400
    lines = tx("c1", "claude-sonnet-5-5", {"input_tokens": 1000, "output_tokens": 200,
                                           "cache_read_input_tokens": 50_000,
                                           "cache_creation": {"ephemeral_5m_input_tokens": 3000,
                                                              "ephemeral_1h_input_tokens": 0}},
               ("Bash", "python - <<'EOF'\nprint(1)\nEOF"), body)
    lines += tx("c2", "no-such-model", {"input_tokens": 10})
    lines += tx("c3", "<synthetic>", {"input_tokens": 0})
    shape.write_text("\n".join(lines) + "\n", encoding="utf-8")
    turns, results, calls = context_shape.read_session(shape)
    check_eq("read_session: one entry per unique turn, with its own token counts",
             [(t["i"], t["o"], t["read"], t["w5"], t["w1"]) for t in turns],
             [(1000, 200, 50_000, 3000, 0), (10, 0, 0, 0, 0), (0, 0, 0, 0, 0)])
    check_eq("read_session: the result's size in tokens and the inline-script mark",
             (results["tu-c1"], calls["tu-c1"]["inline"]), (100, True))
    # (1000*2 + 200*10 + 50000*0.1 + 3000*2.5) / 1e6 = (2000 + 2000 + 5000 + 7500) / 1e6 = 0.0165
    check_eq("cost: a claude-sonnet-5-5 turn is its catalogue value", round(context_shape.cost(turns[0]), 6), 0.0165)
    check_eq("cost: an unknown model is None (unpriced), and a no-usage turn is 0",
             (context_shape.cost(turns[1]), context_shape.cost(turns[2])), (None, 0.0))
    context_shape.BASE, context_shape.RUNS, context_shape.TASK = nowhere, {RUN: RUN}, TICKET
    code, printed = run_main(context_shape, [RUN])
    check("context_shape on a run without driver-runs.jsonl names the missing file and does not crash",
          code == 0 and "no driver journal for" in printed and "driver-runs.jsonl" in printed, printed[:400])

    # --- check_all_contracts ------------------------------------------------------------------
    import check_all_contracts
    sample = sample_dir("check_all_contracts")      # data of the experiment's runs table; None without one

    def snapshot(folder):
        return sorted((str(p.relative_to(folder)), p.stat().st_size, p.stat().st_mtime_ns)
                      for p in folder.rglob("*") if p.is_file())
    if sample is not None:
        before = snapshot(sample)
        code, printed = run_main(check_all_contracts, ["--task-dir", str(sample)])
        check("check_all_contracts on the sample run exits 0 and prints the have/MISS/CATCH totals",
              code == 0 and re.search(r"=== TOTAL  have=\d+  MISS=\d+  CATCH=\d+", printed) is not None
              and "Traceback" not in printed, printed[-300:])
        check("a contract whose input the sample lacks says which file is absent",
              "MISS  work/ledger.json\n         file absent: work/ledger.json" in printed, printed[-1500:])
        check_eq("the sample run is read in place and left as it was", snapshot(sample), before)
    hollow = root / "hollow-task"
    hollow.mkdir()
    code, printed = run_main(check_all_contracts, ["--task-dir", str(hollow)])
    check("check_all_contracts on an empty folder exits 0, no traceback, every contract with inputs MISSes",
          code == 0 and "Traceback" not in printed and "file absent: pipeline.json" in printed
          and "file absent: work/retro-numbers.json" in printed
          and int(re.search(r"MISS=(\d+)", printed).group(1)) > 0, printed[-400:])
    code, printed = run_main(check_all_contracts, ["--task-dir", str(root / "no-such-folder")])
    check("a task folder that does not exist is refused by name, with the form to pass",
          code == 2 and "task folder not found" in printed and "--task-dir" in printed, printed)
    # QA_RUNS_BASE given (env, above): the import then does not consult tools/dev.config.yaml, whose absence
    # is one WARN line on stderr (t-584); without it this check would fail on every clone without the file
    quiet = subprocess.run([sys.executable, "-B", "-c", "import check_all_contracts"], cwd=HERE, env=env,
                           capture_output=True, text=True)
    check("imports read nothing beyond the config when QA_RUNS_BASE is set: importing check_all_contracts prints "
          "nothing", quiet.returncode == 0 and quiet.stdout == "" and quiet.stderr == "", quiet.stderr[-300:])
    # second arm: no QA_RUNS_BASE, so the import consults the config - through the QA_DEV_CONFIG door to a
    # temp file that names all four keys (a valid one: no refusal, no missing-key WARN)
    door = root / "dev-config-door.yaml"
    door.write_text("developer: measurer\nstand_copy_root: %s\nrelease_repo_root: %s\ngithub_token_env: GITHUB_TOKEN\n"
                    % (root / "from-config", root / "skills"), encoding="utf-8")
    env_config = {k: v for k, v in os.environ.items() if k not in ("QA_RUNS_BASE", "QA_DEV_CONFIG", "QA_RUNS_TABLE")}
    env_config["QA_DEV_CONFIG"] = str(door)
    configured = subprocess.run([sys.executable, "-B", "-c", "import check_all_contracts"], cwd=HERE,
                                env=env_config, capture_output=True, text=True)
    check("imports read nothing beyond the config when QA_RUNS_BASE is unset: with QA_DEV_CONFIG on a valid "
          "file, importing check_all_contracts prints nothing on either stream",
          configured.returncode == 0 and configured.stdout == "" and configured.stderr == "",
          configured.stderr[-300:])


# --- the yardstick's own fidelity (t-020): unpriced is counted, the plan is read, a case is a case ----
# Hand values (per million tokens, from the catalogue): claude-sonnet-5-5 input 2; gpt-5.6-terra
# input 2, output 12, cache_read 0.2 and NO cache-write key, so a Terra request that wrote cache
# cannot be priced.
STAMP = "2026-09-27T00:01:00Z"


def pair_transcript(path: Path, extra=()) -> Path:
    """One transcript: a Terra turn that wrote cache (unpriceable) + a sonnet-5-5 turn of 1M input
    tokens (2.00), plus whatever turns `extra` adds as (id, model, usage)."""
    turns = [("t1", "gpt-5.6-terra", {"input_tokens": 10, "cache_creation_input_tokens": 5}),
             ("t2", "claude-sonnet-5-5", {"input_tokens": 1_000_000}), *extra]
    lines = [json.dumps({"type": "user", "timestamp": STAMP, "message": {"content": "qa-scout on QA-1"}})]
    for mid, model, usage in turns:
        lines.append(json.dumps({"type": "assistant", "timestamp": STAMP, "uuid": mid, "message": {
            "id": mid, "model": model, "usage": usage, "content": []}}))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def scan_pair(module, path: Path, extra=()) -> tuple:
    """(cost_usd, unpriced_requests) that `module.scan` reads out of the pair transcript."""
    row = module.scan(pair_transcript(path, extra), module.rates())
    return row["cost_usd"], row["unpriced_requests"]


def fidelity(root: Path) -> None:
    import importlib.util
    import compare
    import paths
    import report_to_gate
    import report_run
    import check_all_contracts
    import stage_compare

    # --- F1: an unpriced request is counted and left out of the dollars, never a $0 fact ---------
    path = root / "pair.jsonl"
    check_eq("scan: a Terra turn that wrote cache is unpriced, the sonnet-5-5 turn is 2.00",
             scan_pair(compare, path), (2.0, 1))
    check_eq("scan: a <synthetic> turn WITH usage is treated like any model, unknown -> unpriced",
             scan_pair(compare, path, [("t3", "<synthetic>", {"input_tokens": 5})]), (2.0, 2))
    check_eq("scan: a <synthetic> turn with zero usage costs 0, is not counted, is not a request",
             (compare.scan(pair_transcript(path, [("t3", "<synthetic>", {"input_tokens": 0})]),
                           compare.rates())["requests"], scan_pair(compare, path)), (2, (2.0, 1)))
    only = pair_transcript(root / "all-unpriced.jsonl")
    only.write_text("\n".join(line for line in only.read_text(encoding="utf-8").splitlines()
                              if "sonnet" not in line) + "\n", encoding="utf-8")
    row = compare.scan(only, compare.rates())
    check_eq("scan: every turn unpriced -> cost 0.0 AND the count says how many", (row["cost_usd"], row["unpriced_requests"]), (0.0, 1))
    cut = datetime(2030, 1, 1, tzinfo=timezone.utc)
    check_eq("scan_until: the same pair -> (role, requests, cost 2.0, unpriced 1)",
             (lambda r: (r[0], r[1], round(r[2], 2), r[3]))(
                 report_to_gate.scan_until(pair_transcript(path), compare.rates(), cut)),
             ("qa-scout", 2, 2.0, 1))
    check_eq("scan_until: a <synthetic> turn with usage is unpriced there too",
             report_to_gate.scan_until(pair_transcript(path, [("t3", "<synthetic>", {"input_tokens": 5})]),
                                       compare.rates(), cut)[3], 2)
    check_eq("the printed line", compare.unpriced_line(3), "unpriced requests: 3 (excluded from $)")
    check_eq("report_run: a cached measurement that predates the count says unknown, not 0",
             report_run.unpriced_total({"x": {"requests": 1, "cost_usd": 1.0}}).startswith("unpriced requests: unknown"), True)
    check_eq("report_run: a measured column prints its count",
             report_run.unpriced_total({"a": {"unpriced_requests": 1}, "b": {"unpriced_requests": 2}}),
             "unpriced requests: 3 (excluded from $)")

    # negative control: the same check fails on a copy of compare.py with `or 0` put back
    src = (HERE / "compare.py").read_text(encoding="utf-8")
    old = "        if one is None:\n            unpriced += 1\n        else:\n            cost += one\n"
    check("negative-control setup: the fix is where the copy expects it", old in src)
    (root / "compare_zero.py").write_text(src.replace(old, "        cost += one or 0\n"), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("compare_zero", root / "compare_zero.py")
    zero = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(zero)
    zero_row = zero.scan(pair_transcript(root / "pair-zero.jsonl"), zero.rates())
    check("negative control: with `or 0` restored the unpriced turn vanishes ($ right, count gone)",
          (zero_row["cost_usd"], zero_row.get("unpriced_requests")) != (2.0, 1), str(zero_row))

    # --- F2: the plan is read in the shape the package writes it; a tool failure is SHAPE, not MISS ---
    sample = sample_dir("check_all_contracts")
    if sample is not None:
        code, printed = run_main(check_all_contracts, ["--task-dir", str(sample)])
        check("check_all_contracts on the sample: exit 0, no SHAPE row, SHAPE counted in its own total",
              code == 0 and not re.search(r"^  SHAPE", printed, re.M)
              and re.search(r"=== TOTAL  have=\d+  MISS=\d+  CATCH=\d+  SHAPE=0", printed) is not None, printed[-300:])
        check("and it reads the plan: s3, s4-case-critic, s4-runner and gate-a have no 'input shape' row",
              "input shape" not in printed, printed[-300:])
        check("and its first printed line says which rows are analysis, not measurement (FR-41)",
              printed.splitlines()[0].startswith("NOTE: rows whose verdict is a constant or a narrative"), printed[:200])
    check_eq("plan_rows: {'rows': [...]} and a bare legacy list are the same rows",
             (check_all_contracts.plan_rows({"rows": [1, 2]}), check_all_contracts.plan_rows([1, 2])), ([1, 2], [1, 2]))
    hollow = root / "shape-task"
    (hollow / "work").mkdir(parents=True)
    (hollow / "pipeline.json").write_text(json.dumps({"gates": {"A": {}}}), encoding="utf-8")
    rows = check_all_contracts.check(hollow)
    check("pipeline.json without gate_waivers / stage_overrides: gate-a reads it, no SHAPE row",
          any(r[0] == "gate-a-to-automator" and r[1] == "have" for r in rows)
          and not any(r[1] == "SHAPE" for r in rows), str(rows[-3:]))
    (hollow / "pipeline.json").write_text(json.dumps({"gates": []}), encoding="utf-8")
    rows = check_all_contracts.check(hollow)
    check("a real shape failure gets the SHAPE word and is not a MISS",
          [r[1] for r in rows if r[0] == "gate-a-to-automator"] == ["SHAPE"], str(rows[-3:]))

    # --- F6: a case is a file whose front matter id is its own stem, whatever the id form --------
    tree = root / "case-tree"
    for rel, text in {
            "a/TC-001.md": "---\nid: TC-001\ntitle: x\n---\nbody\n",
            "a/PROJ-1_TC_001.md": "---\nid: PROJ-1_TC_001\n---\nbody\n",
            "a/quoted.md": "---\nid: \"quoted\"\n---\n",
            "a/critic-findings.md": "---\nid: critic-findings\n---\n",
            "a/critic-findings-2.md": "---\nid: critic-findings-2\n---\n",
            "cases/X/cv_a.md": "---\nid: cv_a\n---\n",
            "a/case-versions/cv_b.md": "---\nid: cv_b\n---\n",
            "a/TC-002.md": "---\nid: TC-999\n---\n",
            "a/no-front.md": "id: no-front\n",
            "a/unclosed.md": "---\ntitle: x\n",
            "a/notes.txt": "---\nid: notes\n---\n"}.items():
        (tree / rel).parent.mkdir(parents=True, exist_ok=True)
        (tree / rel).write_text(text, encoding="utf-8")
    check_eq("case_files: TC-001 and the project's own id form count; findings, versions, an id that is not the stem, "
             "no front matter, and a non-md file do not",
             sorted(p.name for p in compare.case_files(tree)),
             ["PROJ-1_TC_001.md", "TC-001.md", "quoted.md"])
    (root / "empty-tree").mkdir()
    check_eq("case_files: an empty tree, an absent one and None are 0",
             (compare.case_files(root / "empty-tree"), compare.case_files(root / "nope"),
              compare.case_files(None)), ([], [], []))
    sample = sample_dir("case_files")
    if sample is not None:
        check_eq("case_files on the sample run's tree counts its three cases, not its versions",
                 len(compare.case_files(sample / "work" / "test-cases")), 3)
    stage_compare.RUNS, stage_compare.BASE, stage_compare.TASK = {"c": "c"}, root / "case-base", "T"
    target = root / "case-base" / "c" / "test-harness/qa-factory/artifacts/T/work/test-cases"
    target.mkdir(parents=True)
    (target / "PROJ-1_TC_001.md").write_text("---\nid: PROJ-1_TC_001\n---\n", encoding="utf-8")
    import io
    import contextlib
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        stage_compare.s4()
    check("stage_compare s4 counts the project-form case (it counted 0 with rglob TC-*)",
          f"{'case_files':24} | {'1':22}" in buffer.getvalue(), buffer.getvalue())


def run_main_text(module, argv) -> tuple:
    """`run_main` for a script whose main() reconfigures sys.stdout (report_run, report_to_gate): a
    StringIO has no `reconfigure`, so the capture is a text wrapper over bytes."""
    import io
    import contextlib
    raw = io.BytesIO()
    buffer, old = io.TextIOWrapper(raw, encoding="utf-8", write_through=True), sys.argv
    sys.argv = [module.__name__ + ".py", *argv]
    try:
        with contextlib.redirect_stdout(buffer):
            code = module.main()
    finally:
        sys.argv = old
    buffer.flush()
    return code, raw.getvalue().decode("utf-8")


def unpriced_sum(root: Path) -> None:
    """The unpriced count SUMMED over transcripts, through every measurer that reports it (critic
    t-025: six mutations of these sums survived a suite that only counted a single transcript).

    Two top-level transcripts, one with a subagent, each turn a Terra request that wrote cache (no
    price): session p1 has 1 unpriced + 1 in its subagent, session p2 has 2. So the run's total is 4,
    the orchestrator's share 3, the subagent's 1 - and no total equals one transcript's own count."""
    import compare
    import report_run
    import report_to_gate

    unpriced = ("gpt-5.6-terra", {"input_tokens": 10, "cache_creation_input_tokens": 5})
    tdir = root / "pair-transcripts"
    (tdir / "sess-p1" / "subagents").mkdir(parents=True)
    pair_transcript(tdir / "sess-p1.jsonl")                                       # 1 unpriced
    pair_transcript(tdir / "sess-p1" / "subagents" / "sub-1.jsonl")               # 1 unpriced
    pair_transcript(tdir / "sess-p2.jsonl", [("t3", *unpriced)])                  # 2 unpriced
    # "pair" has no driver journal (transcript sessions are all `orchestrator`); "pairj" has one
    # that names both sessions `qa-scout`, so its money takes report_run.money's journal branch.
    base = root / "pair-base"
    for run in ("pair", "pairj"):
        task = base / run / "test-harness" / "qa-factory" / "artifacts" / TICKET
        task.mkdir(parents=True)
        (task / "pipeline.json").write_text(json.dumps({"ticket": TICKET, "stages": {
            "S1": {"status": "done", "started": "2026-09-27T00:00:00+00:00",
                   "finished": "2026-09-27T01:00:00+00:00"}}}), encoding="utf-8")
    journal = base / "pairj" / "test-harness" / "qa-factory" / "artifacts" / TICKET / "state"
    journal.mkdir()
    (journal / "driver-runs.jsonl").write_text("\n".join(json.dumps(row) for row in (
        {"kind": "role", "role": "qa-scout", "session_id": "sess-p1", "total_cost_usd": 1.0,
         "num_turns": 1, "resumed": False},
        {"kind": "role", "role": "qa-scout", "session_id": "sess-p2", "total_cost_usd": 1.0,
         "num_turns": 1, "resumed": False})) + "\n", encoding="utf-8")

    saved = (compare.transcript_dir, report_run.BASE, report_run.COPIES)
    compare.transcript_dir = lambda project: tdir
    report_run.BASE, report_run.COPIES = base, {"pair": "pair", "pairj": "pairj"}
    try:
        report = compare.cost_report(base / "pair" / "test-harness", TICKET)
        check_eq("cost_report: the run's unpriced total is the sum over both sessions and the subagent",
                 report["unpriced_requests"], 4)
        check_eq("cost_report: each session carries its own count (p1 has 2, p2 has 2)",
                 sorted(s["unpriced_requests"] for s in report["sessions"]), [2, 2])
        check_eq("cost_report: by_role accumulates across sessions (orchestrator 1+2, qa-scout 1)",
                 {role: v["unpriced_requests"] for role, v in report["by_role"].items()},
                 {"orchestrator": 3, "qa-scout": 1})
        check_eq("report_run.money without a journal: the same per-role sums",
                 {role: v["unpriced_requests"] for role, v in report_run.money("pair", TICKET).items()},
                 {"orchestrator": 3, "qa-scout": 1})
        check_eq("report_run.money with a journal: both sessions and the subagent land on qa-scout",
                 {role: v["unpriced_requests"] for role, v in report_run.money("pairj", TICKET).items()},
                 {"qa-scout": 4})
        check_eq("report_to_gate.by_agent without a journal: the same per-role sums",
                 {role: v["unpriced_requests"] for role, v in report_to_gate.by_agent("pair", TICKET).items()},
                 {"orchestrator": 3, "qa-scout": 1})
        check_eq("report_to_gate.by_agent with a journal: qa-scout carries all four",
                 {role: v["unpriced_requests"] for role, v in report_to_gate.by_agent("pairj", TICKET).items()},
                 {"qa-scout": 4})

        line = "unpriced requests: 4 (excluded from $)"
        code, printed = run_main(compare, ["--project", str(base / "pair" / "test-harness"), "--ticket", TICKET])
        check("compare.main prints the run's unpriced line under TOTAL",
              code == 0 and re.search(r"^TOTAL \$[\d.]+\n" + re.escape(line) + r"$", printed, re.M) is not None,
              printed[:500])
        code, printed = run_main_text(report_to_gate, ["--left", "pair", "--right", "pairj", "--ticket", TICKET])
        check("report_to_gate.main prints one unpriced line per column, 4 and 4",
              code == 0 and f"pair: {line}" in printed and f"pairj: {line}" in printed, printed[-400:])
        code, printed = run_main_text(report_run, ["--left", "pair", "--right", "pairj", "--ticket", TICKET])
        check("report_run.main prints one unpriced line per column, 4 and 4",
              code == 0 and f"pair: {line}" in printed and f"pairj: {line}" in printed, printed[-600:])

        # the cached column: its note claims the transcripts are gone only when the folder is absent,
        # and a cache that predates the count says how to fill it
        cache = root / "old-cache.json"
        cache.write_text(json.dumps({"cost": {"by_role": {"orchestrator": {
            "requests": 9, "cost_usd": 1.0, "dispatches": 1}}}}), encoding="utf-8")
        argv = ["--left", "pair", "--right", "pairj", "--ticket", TICKET, "--left-cache", str(cache)]
        code, printed = run_main_text(report_run, argv)
        check("report_run.main: a cached column whose transcripts exist does not say they are gone",
              code == 0 and "read from the cached measurement old-cache.json, not from transcripts" in printed
              and "transcripts are gone" not in printed, printed[:300])
        check("and a cache that predates the count says how to fill it",
              "pair: unpriced requests: unknown (this cached measurement predates the count; "
              "rerun compare.py --json to fill it)" in printed, printed[-500:])
        compare.transcript_dir = lambda project: root / "no-such-transcripts"
        code, printed = run_main_text(report_run, argv)
        check("with the transcript folder absent the note says so",
              code == 0 and "old-cache.json (its transcripts are gone), not from transcripts" in printed,
              printed[:300])
    finally:
        compare.transcript_dir, report_run.BASE, report_run.COPIES = saved


def stamped(role_line: str, stamps: list) -> str:
    """A transcript whose first user turn and every request carry the given ISO stamps:
    `stamps` = [(iso stamp, usage)]; the user turn is stamped like the first request."""
    lines = [json.dumps({"type": "user", "timestamp": stamps[0][0], "message": {"content": role_line}})]
    for index, (stamp, usage) in enumerate(stamps):
        lines.append(json.dumps({"type": "assistant", "timestamp": stamp, "uuid": f"u{index}",
                                 "message": {"id": f"m{index}-{stamp}", "model": MODEL, "usage": usage,
                                             "content": []}}))
    return "\n".join(lines) + "\n"


def stage_role_table_tests(root: Path) -> None:
    """t-082: the stage-by-role table. Two synthetic runs, every expected number visible here.

    srt-drv (a driver run, 1M input tokens = $3.00 at the fixture model's rate): sess-a is the scout
    of S1 (two journal rows, 10 + 5 min), sess-b the conductor of S1, sess-c the automator of S2 with
    one subagent, sess-x a session whose first row names no stage; `operator` is a transcript the
    journal does not own. Its pipeline.json: S1 00:00 -> 00:46, S2 opened at 01:00 and never
    finished (the missing-`finished` fallback).
    srt-orc (an orchestrator run, no journal): pipeline.json opens S1 at 00:00 (finished 00:50) and
    S2 at 01:00 (never finished), the
    event log dispatched qa-scout in S1 and qa-automator in S2; the orchestrator made 2 requests in
    S1 and 1 in S2 ($9.00), and four subagents ($3.00 each): a scout inside S1 (placed), an
    automator inside S2 (placed), a scout inside S2 (S2 never dispatched a scout: unplaceable) and a
    scout before any window (unplaceable)."""
    import contextlib
    import io
    import compare
    import report_run
    import stage_role_table as srt

    # --- the helpers -------------------------------------------------------------------------
    parts = srt.apportion(100, {"a": 1, "b": 1, "c": 1})
    check_eq("apportion: 100 cents over three equal weights are whole cents that add back to 100",
             (sum(parts.values()), sorted(parts.values())), (100, [33, 33, 34]))
    check_eq("apportion: nothing to go by (all weights zero) puts the whole amount on the first key, "
             "never drops it", srt.apportion(7, {"a": 0, "b": 0}), {"a": 7, "b": 0})
    check_eq("apportion: 2 : 1 is 600 : 300 of 900", srt.apportion(900, {"s1": 6.0, "s2": 3.0}),
             {"s1": 600, "s2": 300})
    at = lambda minute: datetime(2026, 9, 27, 0, minute, tzinfo=timezone.utc)  # noqa: E731
    check_eq("union_seconds: overlap counts once, a gap not at all",
             srt.union_seconds([(at(0), at(10)), (at(5), at(15)), (at(20), at(30))]), 25 * 60.0)
    check_eq("hmm rounds to the nearest minute", (srt.hmm(3600 * 2 + 29), srt.hmm(3600 * 2 + 31)),
             ("2:00", "2:01"))

    # --- the fixture -------------------------------------------------------------------------
    base = root / "srt-base"
    txs = {"srt-drv": root / "srt-tx-drv", "srt-orc": root / "srt-tx-orc"}
    for run, tdir in txs.items():
        (base / run / "test-harness" / "qa-factory" / "artifacts" / TICKET / "state").mkdir(parents=True)
        tdir.mkdir()
    state = base / "srt-drv" / "test-harness" / "qa-factory" / "artifacts" / TICKET / "state"
    row = lambda sid, stage, minute, seconds, **kw: {  # noqa: E731
        "kind": kw.get("kind", "role"), "role": kw.get("role", "qa-scout"), "stage": stage,
        "session_id": sid, "ts": f"2026-09-27T{minute // 60:02d}:{minute % 60:02d}:00+00:00",
        "duration_ms": seconds * 1000, "resumed": False}
    (state / "driver-runs.jsonl").write_text("\n".join(json.dumps(r) for r in (
        row("sess-a", "S1", 10, 600), row("sess-a", "S1", 40, 300),
        row("sess-b", "S1", 45, 60, kind="conductor", role=""),
        row("sess-c", "S2", 120, 1800, role="qa-automator"),
        {"kind": "delivery", "ts": "2026-09-27T02:05:00+00:00"},
        row("sess-x", "", 130, 120, role="qa-critic"))) + "\n", encoding="utf-8")
    drv = txs["srt-drv"]
    for sid, requests in (("sess-a", 1_000_000), ("sess-b", 500_000), ("sess-c", 500_000),
                          ("sess-x", 100_000), ("operator", 2_000_000)):
        (drv / f"{sid}.jsonl").write_text(transcript(sid, f"qa-scout on {TICKET}",
                                                     [{"input_tokens": requests}]), encoding="utf-8")
    (drv / "sess-c" / "subagents").mkdir(parents=True)
    (drv / "sess-c" / "subagents" / "agent-1.jsonl").write_text(
        transcript("sess-c-sub", f"qa-critic on {TICKET}", [{"input_tokens": 500_000}]), encoding="utf-8")

    orc_task = base / "srt-orc" / "test-harness" / "qa-factory" / "artifacts" / TICKET
    (orc_task / "pipeline.json").write_text(json.dumps({"stages": {
        "S1": {"started": "2026-09-27T00:00:00+00:00", "finished": "2026-09-27T00:50:00+00:00"},
        "S2": {"started": "2026-09-27T01:00:00+00:00"}}}), encoding="utf-8")
    (state.parent / "pipeline.json").write_text(json.dumps({"stages": {
        "S1": {"started": "2026-09-27T00:00:00+00:00", "finished": "2026-09-27T00:46:00+00:00"},
        "S2": {"started": "2026-09-27T01:00:00+00:00"}}}), encoding="utf-8")
    (orc_task / "state" / "events.jsonl").write_text("\n".join(json.dumps(e) for e in (
        {"type": "dispatch", "payload": {"id": "S1-qa-scout-1", "stage": "S1", "role": "qa-scout"}},
        {"type": "dispatch", "payload": {"id": "S2-qa-automator-1", "stage": "S2", "role": "qa-automator"}},
        {"type": "returned", "payload": {"dispatch_id": "S1-qa-scout-1"}})) + "\n", encoding="utf-8")
    orc, million = txs["srt-orc"], {"input_tokens": 1_000_000}
    day = "2026-09-27T"
    (orc / "orch-main.jsonl").write_text(stamped(f"orchestrate {TICKET}", [
        (day + "00:10:00Z", million), (day + "00:20:00Z", million), (day + "01:30:00Z", million)]),
        encoding="utf-8")
    (orc / "orch-main" / "subagents").mkdir(parents=True)
    for name, role, first, last in (("a", "qa-scout", "00:05", "00:15"), ("b", "qa-automator", "01:10", "01:25"),
                                    ("c", "qa-scout", "01:20", "01:30"), ("d", "qa-scout", "-1", "-1")):
        early = first == "-1"
        first, last = (("2026-09-26T23:00:00Z", "2026-09-26T23:10:00Z") if early
                       else (day + first + ":00Z", day + last + ":00Z"))
        text = stamped(f"{role} on {TICKET}", [(first, million)])
        text = text.replace(f'"timestamp": "{first}", "uuid": "u0"', f'"timestamp": "{last}", "uuid": "u0"')
        (orc / "orch-main" / "subagents" / f"agent-{name}.jsonl").write_text(text, encoding="utf-8")

    saved = (compare.transcript_dir, report_run.BASE, report_run.COPIES)
    compare.transcript_dir = lambda project: txs[Path(project).parent.name]
    report_run.BASE, report_run.COPIES = base, {run: run for run in txs}
    try:
        def quiet(function, *args):
            with contextlib.redirect_stdout(io.StringIO()):
                return function(*args)

        def shown(run):
            return {key: (cell["cents"], cell["tokens"], srt.union_seconds(cell["intervals"]) + cell["loose"])
                    for key, cell in run["cells"].items()}

        # --- the driver run: 3 sessions on 2 stages, one without a stage --------------------
        drv_run = quiet(srt.collect, "srt-drv", TICKET)
        check_eq("driver run: each session is placed once, by its first journal row; resumed rows "
                 "add their time, a conductor is a role of its own, a stageless session is under the dash",
                 shown(drv_run),
                 {("S1", "qa-scout"): (300, 1_000_000, 900.0), ("S1", "conductor"): (150, 500_000, 60.0),
                  ("S2", "qa-automator"): (300, 1_000_000, 1800.0),
                  (srt.NO_STAGE, "qa-critic"): (30, 100_000, 120.0)})
        check_eq("driver run: the subagent's money and tokens are in its session's row (sess-c 1.50 + 1.50)",
                 drv_run["cells"][("S2", "qa-automator")]["cents"], 300)
        check_eq("driver run: 4 sessions, 1 unplaceable counted, the operator's transcript not counted",
                 (drv_run["notes"]["sessions"], drv_run["notes"]["unplaced"], drv_run["notes"]["not_owned"]),
                 (4, 1, 1))
        drv_reported = quiet(srt.report_run_cents, "srt-drv", TICKET)
        check_eq("the table total equals the total report_run.py prints, to the cent ($7.80)",
                 (drv_run["cents"], drv_reported), (780, 780))
        check_eq("and the printed line says gap $0.00",
                 srt.total_line("srt-drv", drv_run["cents"], drv_reported),
                 "srt-drv: total by this table vs total by report_run.py: $7.80 vs $7.80, gap $0.00")

        # --- negative control: a dropped session shows as a gap ------------------------------
        dropped = dict(drv_run["cells"])
        dropped.pop(("S2", "qa-automator"))
        check_eq("negative control: with one session dropped the line reports the $3.00 gap",
                 srt.total_line("srt-drv", sum(c["cents"] for c in dropped.values()), drv_reported),
                 "srt-drv: total by this table vs total by report_run.py: $4.80 vs $7.80, gap -$3.00")

        # --- the orchestrator run: windows, the role check, the split of the orchestrator ------
        orc_run = quiet(srt.collect, "srt-orc", TICKET)
        check_eq("orchestrator run: the orchestrator is cut by stage window ($6.00 in S1, $3.00 in S2), "
                 "a subagent goes to the window of its first stamp when that stage dispatched its role, "
                 "else to the dash (two scouts)",
                 shown(orc_run),
                 {("S1", "orchestrator"): (600, 2_000_000, 600.0), ("S2", "orchestrator"): (300, 1_000_000, 0.0),
                  ("S1", "qa-scout"): (300, 1_000_000, 600.0), ("S2", "qa-automator"): (300, 1_000_000, 900.0),
                  (srt.NO_STAGE, "qa-scout"): (600, 2_000_000, 600.0 * 2)})
        check_eq("orchestrator run: 5 transcripts = 1 session, 2 unplaceable counted",
                 (orc_run["notes"]["sessions"], orc_run["notes"]["unplaced"]), (1, 2))
        orc_reported = quiet(srt.report_run_cents, "srt-orc", TICKET)
        check_eq("orchestrator run: the table total equals report_run's ($21.00), nothing dropped",
                 (orc_run["cents"], orc_reported), (2100, 2100))

        # --- the printed table -----------------------------------------------------------------
        code, printed = run_main_text(srt, ["--left", "srt-drv", "--right", "srt-orc", "--ticket", TICKET])
        lines = printed.splitlines()
        check("main: the header is the owner's layout",
              "| Стадии | Роли | srt-drv время | srt-drv токены | srt-drv цена | srt-orc время "
              "| srt-orc токены | srt-orc цена |" in lines, printed[:400])
        check("main: a stage header row carries the stage span only, pipeline started->finished "
              "(left 0:46, right 0:50), the other cells empty",
              "| S1 |  | 0:46 |  |  | 0:50 |  |  |" in lines, printed[:900])
        check("main: a role row has tokens and price in both runs and an EMPTY time cell",
              "|  | qa-scout |  | 1.0M | $3.00 |  | 1.0M | $3.00 |" in lines, printed[:900])
        check("main: a role only one run dispatched has the dash on the other side",
              "|  | orchestrator |  | — | — |  | 2.0M | $6.00 |" in lines
              and "|  | conductor |  | 500k | $1.50 |  | — | — |" in lines, printed[:900])
        check("main: no stage subtotal rows any more", "итого по стадии" not in printed, printed[:900])
        check("main: the missing `finished` (S2 in both runs, and the dash stage) falls back to the union of "
              "the stage's session intervals, marked with a star (0:30 / 0:15 / 0:02 / 0:20)",
              "| S2 |  | 0:30\\* |  |  | 0:15\\* |  |  |" in lines
              and "| — |  | 0:02\\* |  |  | 0:20\\* |  |  |" in lines, printed[:1400])
        check("main: one footnote line explains the star", printed.count(srt.FOOTNOTE) == 1, printed[-900:])
        check("main: the grand total row: time = sum of the stage spans (0:46 + 0:30* + 0:02* = 1:18; "
              "0:50 + 0:15* + 0:20* = 1:25), tokens and price = sums",
              "| **Итого** |  | **1:18** | **2.6M** | **$7.80** | **1:25** | **7.0M** | **$21.00** |" in lines,
              printed[:2000])
        stage_rows = [line.split("|")[1].strip() for line in lines
                      if re.match(r"\| (S\d+|—) \|  \|", line)]
        check_eq("main: stages in order S1, S2, then the dash last", stage_rows, ["S1", "S2", srt.NO_STAGE])
        code, printed = run_main_text(srt, ["--left", "srt-drv", "--right", "srt-orc", "--ticket", TICKET,
                                            "--role-time"])
        lines = printed.splitlines()
        check("main --role-time: the role's own time is back (0:15 / 0:10), the stage header unchanged",
              "|  | qa-scout | 0:15 | 1.0M | $3.00 | 0:10 | 1.0M | $3.00 |" in lines
              and "| S1 |  | 0:46 |  |  | 0:50 |  |  |" in lines
              and "|  | orchestrator | — | — | — | 0:10 | 2.0M | $6.00 |" in lines, printed[:900])

        # --- the stage span: report_run's own, and the fallback -----------------------------------
        check_eq("stage_spans: started->finished in seconds, and the same span report_run prints as a clock",
                 (drv_run["spans"], report_run.clock(drv_run["spans"]["S1"]),
                  report_run.stage_times("srt-drv", TICKET)["S1"]["span"]),
                 ({"S1": 2760.0}, "0:46:00", "0:46:00"))
        check_eq("stage_span: a stage with `finished` is its pipeline span, not estimated",
                 srt.stage_span(drv_run, "S1"), (2760.0, False))
        check_eq("stage_span: no `finished` -> the union of the session intervals, flagged estimated",
                 srt.stage_span(drv_run, "S2"), (1800.0, True))
        check_eq("stage_span: nothing at all for the stage -> unknown, not a zero",
                 srt.stage_span(drv_run, "S9"), (None, False))
        (orc_task / "pipeline.json").write_text(json.dumps({"stages": {
            "S1": {"started": "2026-09-27T01:00:00+00:00", "finished": "2026-09-27T00:00:00+00:00"}}}),
            encoding="utf-8")
        check_eq("stage_spans: a `finished` before `started` is not a span",
                 srt.stage_spans("srt-orc", TICKET), {})
        check("main: one total line per run, both agreeing",
              "srt-drv: total by this table vs total by report_run.py: $7.80 vs $7.80, gap $0.00" in lines
              and "srt-orc: total by this table vs total by report_run.py: $21.00 vs $21.00, gap $0.00" in lines,
              printed[-500:])
        code, printed = run_main_text(srt, ["--left", "a/b", "--right", "srt-orc", "--ticket", TICKET])
        check("main: a run name that is a path is refused by name (B-267 shape check), exit 2",
              code == 2 and "run name 'a/b' is not a copy name" in printed, printed)
        check_eq("main: a run no table lists resolves by the copy rule, like the other measurers (not refused)",
                 report_run.copy_folder("nope", report_run.COPIES), report_run.paths.COPY_PREFIX + "nope")
        try:        # the transcript stub of this group knows only its own runs: reaching it means the name was accepted
            code, printed = run_main_text(srt, ["--left", "nope", "--right", "srt-orc", "--ticket", TICKET])
            passed = f"{code} {printed[:200]}"
        except KeyError as exc:
            passed = "" if exc.args == (report_run.copy_folder("nope", report_run.COPIES),) else repr(exc)
        check("main: an unlisted run name is a folder by the rule, not refused as unknown", passed == "", passed)
    finally:
        compare.transcript_dir, report_run.BASE, report_run.COPIES = saved


# --- t-267 / B4: the ticket-file measurer and the S0 table of one story (keys K2 and K16) --------------
# A fixture shaped like a real story's ticket, every number visible here. UTF-8 BYTES, not characters: the
# description "d" + "e acute" is 3 bytes, a comment "e acute" is 2.
#   LLM snapshot : title "T1" 2 + description 3 + AC "a1\nb2" 5 + comments "ccc" 3 + "e acute" 2 = 15 own-words bytes
#   REST file    : title 2 + description 3 + AC "" 0 + comments 5 = 10 own-words bytes; 7 custom-field keys,
#                  5 of them empty (None, "", [], {}, "  "), one object and one 0 are values
E_ACUTE = chr(0xE9)
LLM_SNAPSHOT = {"key": "T-1", "title": "T1", "description": "d" + E_ACUTE, "acceptance_criteria": ["a1", "b2"],
                "comments": [{"text": "ccc"}, {"text": E_ACUTE}], "parent": "T-0", "subtasks": [],
                "links": {"merge_request": None, "branch": None}, "status": "Open"}
REST_FILE = {"key": "T-1", "id": "1", "title": "T1", "type": "Story", "status": "Open",
             "description": "d" + E_ACUTE, "acceptance_criteria": "",
             "custom_fields": {"customfield_1": None, "customfield_2": "", "customfield_3": [],
                               "customfield_4": {}, "customfield_5": "  ", "customfield_6": {"value": "x"},
                               "customfield_7": 0},
             "parent": "T-0", "links": [],
             "comments": [{"id": "9", "author": "", "created": "c", "text": "ccc", "updated": "u"},
                          {"id": "10", "author": "", "created": "c", "text": E_ACUTE, "updated": "u"}]}
# What the original `s0()` of stage_compare printed for two runs, `a` with this snapshot and `b` without
# one, captured BEFORE the story table was added (the baseline rows must stay byte-identical):
S0_BASELINE_FIXTURE = (
    "## S0 — ticket snapshot\n"
    "                         | a                      | b                     \n"
    "acceptance_criteria      | 2                      | —                     \n"
    "comments                 | 1                      | —                     \n"
    "parent                   | P-1                    | —                     \n"
    "subtasks                 | 0                      | —                     \n"
    "description_len          | 5                      | —                     \n"
    "merge_request            | True                   | —                     \n"
    "issue_links              | 1                      | —                     \n"
    "remote_links             | 2                      | —                     \n"
    "attachments              | 1                      | —                     \n"
    "status                   | Open                   | —                     \n"
    "snapshot                 | —                      | none                  \n")
# sha256 of the real s0 table of the six baseline copies as printed before the change (read-only data)
S0_REAL_SHA = "c310f3d250b1dfdb24c19924840066b1dbf13a23c39573b29ecf1678c3ae9b05"


def put_json(path: Path, data) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def jira_light_tests(root: Path) -> None:
    import contextlib
    import hashlib
    import importlib.util
    import io
    import subprocess
    import jira_light_check as jlc

    # --- the measurer: bytes, own words, custom fields --------------------------------------------
    base = root / "jl-base"
    story = base / "jl" / "test-harness" / "qa-factory" / "artifacts" / "T-1"
    snap_path = put_json(story / "work" / "ticket-snapshot.json", LLM_SNAPSHOT)
    rest_path = put_json(story / "work" / "sources" / "SRC-a" / "rev1" / "ticket.json", REST_FILE)
    # decoys: a peek of the same key under assessment/ and the ticket.json of another story
    put_json(story / "work" / "sources" / "SRC-b" / "assessment" / "ticket.json", dict(REST_FILE, title="DECOY"))
    put_json(story / "work" / "sources" / "SRC-c" / "rev9" / "ticket.json", dict(REST_FILE, key="T-9"))
    m = jlc.measure(snap_path)
    size = snap_path.stat().st_size
    check_eq("measure: the file size is os.path.getsize", m["bytes"], size)
    check_eq("measure: own words = title 2 + description 3 (UTF-8 bytes, not chars) + AC joined by \\n 5 + "
             "comment texts 3 + 2 = 15", m["own_words_bytes"], 15)
    check_eq("measure: share = own words / file bytes, one decimal", m["share_pct"], round(100 * 15 / size, 1))
    check_eq("measure: counts of the snapshot (2 AC, 2 comments, parent T-0)",
             (m["acceptance_criteria"], m["comments"], m["parent"]), (2, 2, "T-0"))
    check_eq("measure: a snapshot with no custom_fields block holds 0 of them, and its bytes are 0 too",
             (m["custom_field_keys"], m["custom_field_empty_keys"], m["custom_field_bytes"]), (0, 0, 0))
    check_eq("measure: attachments the file does not carry are absent (None), not 0", m["attachments"], None)
    r = jlc.measure(rest_path)
    check_eq("measure REST: own words 10 (the AC string is empty: nothing to join)", r["own_words_bytes"], 10)
    check_eq("measure REST: 0 AC", r["acceptance_criteria"], 0)
    check_eq("measure REST: custom fields are counted over the custom_fields object, not over the file's keys "
             "(7 keys, 5 empty: None, '', [], {}, blank)",
             (r["custom_field_keys"], r["custom_field_empty_keys"]), (7, 5))
    check_eq("measure REST: the share is its own file's (10 / size)", r["share_pct"],
             round(100 * 10 / rest_path.stat().st_size, 1))
    tiny = put_json(root / "tiny.json", {"custom_fields": {"customfield_1": None, "customfield_2": "",
                                                           "customfield_3": E_ACUTE}})
    # json.dumps(indent=2, sort_keys=True, ensure_ascii=False): "{\n" 2 + 25 + 23 + 24 + "}" 1 = 75 bytes
    check_eq("measure: custom_field_bytes is the pretty JSON of the block in UTF-8 bytes (hand value 75)",
             (jlc.measure(tiny)["custom_field_keys"], jlc.measure(tiny)["custom_field_empty_keys"],
              jlc.measure(tiny)["custom_field_bytes"]), (3, 2, 75))
    check_eq("measure: a zero-valued custom field is a value, not an empty one",
             jlc.measure(put_json(root / "zero.json", {"custom_fields": {"a": 0, "b": False}}))
             ["custom_field_empty_keys"], 0)
    hollow = put_json(root / "hollow.json", {"title": None, "description": None, "acceptance_criteria": None,
                                             "comments": [None, {"text": None}], "parent": None})
    h = jlc.measure(hollow)
    check_eq("measure: None title/description/AC/comment text count as nothing, no crash",
             (h["own_words_bytes"], h["acceptance_criteria"], h["comments"], h["parent"]), (0, 0, 2, None))
    check_eq("measure: a string AC counts its non-empty lines",
             jlc.measure(put_json(root / "acstr.json", {"acceptance_criteria": "x\n\n y\n"}))["acceptance_criteria"], 2)
    check_eq("measure: attachment_names stands in when there is no attachments list",
             jlc.measure(put_json(root / "att.json", {"attachment_names": ["a", "b", "c"]}))["attachments"], 3)
    check_eq("find_rest: the story's own ticket.json only - not the assessment peek, not another key's file",
             jlc.find_rest(story, "T-1"), [rest_path])
    check_eq("find_rest: no sources folder -> nothing", jlc.find_rest(root / "no-story", "T-1"), [])

    # --- absent / unreadable: said, never 0 -------------------------------------------------------
    gone = jlc.measure(root / "nope.json")
    check_eq("measure: a file that is not there is absent and every number is None",
             (gone["state"], gone["bytes"], gone["own_words_bytes"], gone["share_pct"], gone["custom_field_keys"],
              gone["comments"], gone["acceptance_criteria"]), ("absent", None, None, None, None, None, None))
    broken = root / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    check_eq("measure: a file that is not JSON is unreadable, named, not a crash", jlc.measure(broken)["state"],
             "unreadable")

    # --- the command line -------------------------------------------------------------------------
    code, printed = run_main(jlc, [str(story)])
    check("CLI: exit 0 and each row carries snapshot | rest | the counting command",
          code == 0 and re.search(r"^own_words_bytes\s+\|\s+15\s+\|\s+10\s+\|\s+sum len", printed, re.M) is not None
          and re.search(r"^custom_field_keys\s+\|\s+0\s+\|\s+7\s+\|", printed, re.M) is not None
          and re.search(r"^acceptance_criteria\s+\|\s+2\s+\|\s+0\s+\|", printed, re.M) is not None, printed)
    check("CLI: the carrier paths of both files are printed",
          f"[snapshot] {snap_path}" in printed and f"[rest]     {rest_path}" in printed, printed[:500])
    check("CLI: the decoys are not measured (no DECOY, one REST file)", "DECOY" not in printed
          and "REST files carry this key" not in printed, printed[:500])
    code, printed = run_main(jlc, [str(story), "--rest", str(root / "nope.json")])
    check("CLI: --rest to a file that is not there -> every REST cell reads absent (never 0)",
          code == 0 and all(re.search(rf"^{row}\s+\|\s+\S+\s+\|\s+absent\s+\|", printed, re.M) is not None
                            for row in ("bytes", "own_words_bytes", "share_%", "custom_field_keys",
                                        "custom_field_empty_keys", "custom_field_bytes", "comments",
                                        "attachments", "parent", "acceptance_criteria")), printed)
    code, printed = run_main(jlc, [str(story), "--snapshot", str(snap_path), "--rest", str(rest_path), "--json"])
    shown = json.loads(printed)
    check_eq("CLI --json: the same numbers", (shown["snapshot"]["own_words_bytes"], shown["rest"]["own_words_bytes"],
                                              shown["rest"]["custom_field_keys"], shown["story"]), (15, 10, 7, "T-1"))
    code, printed = run_main(jlc, [str(root / "no-such-story")])
    check("CLI: a story folder that does not exist is refused by name, exit 2",
          code == 2 and "story folder not found" in printed, printed)
    quiet = subprocess.run([sys.executable, "-B", "-c", "import jira_light_check"], cwd=HERE,
                           capture_output=True, text=True)
    check("importing jira_light_check prints nothing", quiet.returncode == 0 and quiet.stdout == "", quiet.stderr[-300:])
    check("the measurer is standalone: it does not import the package module it will measure",
          "ticket_light" not in " ".join(line for line in (HERE / "jira_light_check.py").read_text(
              encoding="utf-8").splitlines() if line.startswith(("import ", "from "))))

    # --- stage_compare s0 --story: K16 and K2 -----------------------------------------------------
    import stage_compare as sc
    saved = sc.BASE
    sc.BASE = base
    try:
        def s0_story(*args, **kwargs):
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = sc.s0_story(*args, **kwargs)
            return code, buffer.getvalue()

        code, printed = s0_story("T-1", ref_run="jl")
        check("s0 --story, driver = the REST file: exit 1 and the STOP names acceptance_criteria LLM 2, driver 0",
              code == 1 and "STOP K16 acceptance_criteria: LLM 2, driver 0" in printed, printed)
        check("s0 --story: the table has the baseline columns for the LLM and for the driver",
              all(re.search(rf"^{row:24} \|", printed, re.M) for row in (
                  "acceptance_criteria", "comments", "parent", "subtasks", "description_len", "merge_request",
                  "issue_links", "remote_links", "attachments", "status")), printed)
        check("s0 --story: K2 stops too while the driver file IS the unfiltered REST file (share below the "
              "LLM's, bytes not below the REST's)",
              "STOP K2a own-words share %" in printed and "STOP K2b bytes" in printed, printed)
        check("s0 --story: comments, parent and description_len are not stops there (1:1, equal, more)",
              "STOP K16 comments" not in printed and "STOP K16 parent" not in printed
              and "STOP K16 description_len" not in printed, printed)
        # the driver run: a light snapshot that keeps everything the LLM's had, in fewer bytes than REST
        light = dict(LLM_SNAPSHOT, comments=LLM_SNAPSHOT["comments"] + [{"text": "extra words"}])
        put_json(base / "jl2" / "test-harness" / "qa-factory" / "artifacts" / "T-1" / "work" / "ticket-snapshot.json",
                 light)
        code, printed = s0_story("T-1", driver_run="jl2", ref_run="jl")
        check("s0 --story --driver-run: a snapshot that shows at least the LLM's -> exit 0, no STOP line",
              code == 0 and "STOP" not in printed and "verdict: ok" in printed, printed)
        # one column fewer at a time: each is named, nothing else is
        for column, change, expect in (
                ("comments", {"comments": [{"text": "ccc"}]}, "STOP K16 comments: LLM 2, driver 1"),
                ("acceptance_criteria", {"acceptance_criteria": ["a1"]}, "STOP K16 acceptance_criteria: LLM 2, driver 1"),
                ("parent", {"parent": "T-5"}, "STOP K16 parent"),
                ("description_len", {"description": "d"}, "STOP K16 description_len: LLM 2, driver 1")):
            put_json(base / "jl3" / "test-harness" / "qa-factory" / "artifacts" / "T-1" / "work" / "ticket-snapshot.json",
                     dict(light, **change))
            code, printed = s0_story("T-1", driver_run="jl3", ref_run="jl")
            check(f"s0 --story: fewer {column} than the LLM -> STOP on that column, exit 1",
                  code == 1 and expect in printed
                  and sum(1 for line in printed.splitlines() if line.startswith("STOP K16")) == 1, printed)
        code, printed = s0_story("T-1", driver_run="nope", ref_run="jl")
        check("s0 --story: a driver file that is not there is NOT MEASURED, exit 2 - not a pass, not a 0",
              code == 2 and "NOT MEASURED" in printed and "driver file: absent" in printed, printed)
        code, printed = s0_story("T-2", ref_run="jl")
        check("s0 --story: a reference that is not there is NOT MEASURED too",
              code == 2 and "LLM snapshot: absent" in printed, printed)
        code, printed = s0_story("T-1", ref_run="jl", as_json=True)
        shown = json.loads(printed)
        check_eq("s0 --story --json: the same verdict, the STOP lines and the driver's path",
                 (code, shown["verdict"], len(shown["stops"]), shown["driver"]["path"] == str(rest_path)),
                 (1, "STOP", 3, True))
        code, printed = run_main(types_module(sc, "story_main"), ["s1", "--story", "T-1"])
        check("s0 --story: another stage with --story is refused, exit 2", code == 2 and "s0 table only" in printed, printed)
        # k16() on its own: the edges of the comparison
        ref = {"acceptance_criteria": 2, "comments": 1, "parent": "P", "description_len": 5, "attachments": jlc.ABSENT,
               "subtasks": 0}
        drv = dict(ref)
        check("k16: equal on every column is ok, an absent attachments column on both sides is not a stop",
              all(ok for *_, ok, _ in sc.k16(ref, drv)))
        check("k16: the driver has no subtasks key and the LLM had 0 -> not a stop; the LLM had 1 -> a stop",
              dict((c, ok) for c, _, _, ok, _ in sc.k16(ref, dict(drv, subtasks=jlc.ABSENT)))["subtasks"] is True
              and dict((c, ok) for c, _, _, ok, _ in sc.k16(dict(ref, subtasks=1), dict(drv, subtasks=jlc.ABSENT)))["subtasks"] is False)
        check("k16: more than the LLM is ok; the LLM's parent None puts no condition on the driver's",
              all(ok for *_, ok, _ in sc.k16(dict(ref, parent=None), dict(drv, comments=9, parent="X"))))
    finally:
        sc.BASE = saved

    # --- the baseline rows stay byte-identical ---------------------------------------------------------
    fixture = root / "s0-baseline"
    snap_base = fixture / "a" / "test-harness/qa-factory/artifacts/T/work"
    put_json(snap_base / "ticket-snapshot.json", {
        "acceptance_criteria": ["x", "y"], "comments": [{}], "parent": "P-1", "subtasks": [], "description": "hello",
        "links": {"merge_request": "u", "issue_links": [1], "remote_links": [1, 2]}, "attachments": [1],
        "status": "Open"})
    (fixture / "b").mkdir()
    pristine = importlib.util.spec_from_file_location("stage_compare_pristine", HERE / "stage_compare.py")
    module = importlib.util.module_from_spec(pristine)
    pristine.loader.exec_module(module)
    module.BASE, module.RUNS, module.TASK = fixture, {"a": "a", "b": "b"}, "T"
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        module.s0()
    check_eq("the baselines S0 table prints exactly what it printed before the story table was added",
             buffer.getvalue(), S0_BASELINE_FIXTURE)
    real = importlib.util.module_from_spec(pristine)
    pristine.loader.exec_module(real)
    folders = [real.BASE / name for name in real.RUNS.values()]
    if folders and all(f.is_dir() for f in folders):          # no table: no baselines: nothing to hash
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            real.s0()
        check_eq("and the real six-run baseline table has the sha256 it had before",
                 hashlib.sha256(buffer.getvalue().encode("utf-8")).hexdigest(), S0_REAL_SHA)
    else:
        print("SKIP the real baseline table (no runs table named by QA_RUNS_TABLE, or the run copies are not on this machine)")

    # --- the real story-run files: read-only; skipped where the copy is not there -----------------------
    story_ticket = real.paths.TABLE.get("story_ticket")
    story_run = next(iter(real.STORY_RUNS), None)       # the reference run is a key of the table, never a literal
    story_copy = real.story_dir(story_run, story_ticket) if story_ticket and story_run else None
    if not (story_ticket and story_run):
        print("SKIP real story-run checks (no story_ticket or story_runs key in the runs table)")
    elif (story_copy / "work" / "ticket-snapshot.json").is_file() and jlc.find_rest(story_copy):
        s, rest = jlc.measure(story_copy / "work" / "ticket-snapshot.json"), jlc.measure(jlc.find_rest(story_copy)[-1])
        check_eq("story run (real): the agent snapshot is 2,071 B, 72.2 % own words, 15 AC",
                 (s["bytes"], s["share_pct"], s["acceptance_criteria"]), (2071, 72.2, 15))
        check_eq("story run (real): the REST ticket.json is 11,107 B, 20.4 % own words, 0 AC",
                 (rest["bytes"], rest["share_pct"], rest["acceptance_criteria"]), (11107, 20.4, 0))
        check_eq("story run (real): 164 custom-field keys, 132 empty, 7,799 B",
                 (rest["custom_field_keys"], rest["custom_field_empty_keys"], rest["custom_field_bytes"]),
                 (164, 132, 7799))
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = real.s0_story(story_ticket, ref_run=story_run)
        check("story run (real): today `s0 --story <story_ticket>` stops - AC 0 against 15 - exit 1",
              code == 1 and "STOP K16 acceptance_criteria: LLM 15, driver 0" in buffer.getvalue(), buffer.getvalue())
    else:
        print("SKIP the real story-run files (the copy is not on this machine)")


def b267_tests(root: Path) -> None:
    """t-329 B-267: a run nobody listed (man1) is read as the copy `<copy_prefix><name>` under the runs base by the
    three tools that kept their own dicts (`report_run`, `spend_by_dispatch`, `stage_compare`); the dicts stay for the
    named baselines; a name is a folder suffix, never a path; `prepare_copy` prints the Start-Process start line.
    Every case fails on the code before the change: it raised KeyError (report_run, stage_compare) or argparse's
    `invalid choice` (spend_by_dispatch)."""
    import io
    import contextlib
    import prepare_copy
    import report_run
    import spend_by_dispatch
    import stage_compare as sc

    import paths
    base = root / "b267-base"
    ticket = "B-267"
    pre = SYNTH_PREFIX                      # the copy prefix of a synthetic runs table
    task = base / (pre + "man1") / "test-harness" / "qa-factory" / "artifacts" / ticket
    (task / "state").mkdir(parents=True)
    (task / "work").mkdir()
    (task / "work" / "requirements-register.md").write_text("| id |\n|---|\n| R-1 |\n| R-2 |\n", encoding="utf-8")
    (task / "state" / "driver-runs.jsonl").write_text(json.dumps(
        {"kind": "role", "role": "qa-scout", "stage": "S1", "dispatch": "S1-qa-scout-1", "session_id": "s",
         "total_cost_usd": 1.25, "num_turns": 5, "resumed": False}) + "\n", encoding="utf-8")
    (task / "state" / "controller.json").write_text(json.dumps(
        {"dispatches": {"S1-qa-scout-1": {"status": "accepted"}}}), encoding="utf-8")
    saved = (report_run.BASE, report_run.COPIES, spend_by_dispatch.BASE, spend_by_dispatch.RUNS,
             sc.BASE, sc.RUNS, sc.TASK, list(sc.EXTRA), sys.argv, paths.COPY_PREFIX, dict(sc.STORY_RUNS))
    report_run.BASE = spend_by_dispatch.BASE = sc.BASE = base
    paths.COPY_PREFIX = pre
    try:
        # --- the one rule
        check_eq("copy_folder: a baseline keeps the folder its dict names",
                 report_run.copy_folder("base-off", {"base-off": "odd-folder"}), "odd-folder")
        check_eq("copy_folder: a name no dict holds is <copy_prefix><name>", report_run.copy_folder("man1", {}), pre + "man1")
        for bad in ("", ".", "..", "../x", "a/b", "a\\b", "-x", "x.", "x y"):
            try:
                report_run.copy_folder(bad, {})
                refused = ""
            except ValueError as exc:
                refused = str(exc)
            check(f"copy_folder: {bad!r} is not a copy name - refused, naming the form to give",
                  "is not a copy name" in refused and pre + "<name>" in refused, refused)
        # --- report_run
        report_run.COPIES = {"base-off": pre + "base-off"}
        check_eq("report_run.project: an unknown name resolves to the BASE path (it was a KeyError)",
                 report_run.project("man1"), base / (pre + "man1") / "test-harness")
        check_eq("report_run.project: a baseline still resolves through its dict",
                 report_run.project("base-off"), base / (pre + "base-off") / "test-harness")
        check_eq("report_run: the stage clock of the unknown run reads ITS pipeline.json",
                 report_run.task_root("man1", ticket), task)
        # --- spend_by_dispatch
        spend_by_dispatch.RUNS = {"r3": pre + "r3"}
        buffer = io.StringIO()
        sys.argv = ["spend_by_dispatch.py", "--run", "man1", "--ticket", ticket]
        with contextlib.redirect_stdout(buffer):
            code = spend_by_dispatch.main()
        check("spend_by_dispatch --run man1: an unknown name reads the copy's journal ($1.25), exit 0",
              code == 0 and "$1.25" in buffer.getvalue() and "man1" in buffer.getvalue(), buffer.getvalue()[:300])
        for argv, what in ((["--run", "nobody", "--ticket", ticket], "a copy that is not there"),
                           (["--run", "../x", "--ticket", ticket], "a name that is a path")):
            err = io.StringIO()
            sys.argv = ["spend_by_dispatch.py", *argv]
            with contextlib.redirect_stderr(err):
                code = spend_by_dispatch.main()
            check(f"spend_by_dispatch: {what} is refused by name, exit 2, no traceback",
                  code == 2 and ("no driver journal for run 'nobody'" in err.getvalue()
                                 or "is not a copy name" in err.getvalue()), err.getvalue()[:300])
        # --- stage_compare
        sc.RUNS, sc.TASK = {"base-off": pre + "base-off"}, ticket
        check_eq("stage_compare.art: an unknown name resolves to the BASE path (it was a KeyError)",
                 sc.art("man1", "work/requirements-register.md"), task / "work" / "requirements-register.md")
        check_eq("stage_compare.art: a baseline that has no folder is None, as before", sc.art("base-off", "x"), None)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = sc.main(["s2", "--run", "man1"])
        printed = buffer.getvalue()
        check("stage_compare s2 --run man1: the unknown run is a column beside the baseline, with ITS register rows",
              code == 0 and "base-off" in printed and "man1" in printed
              and f"{'register_rows(R-n)':24} | {'None':22} | {'2':22}" in printed, printed[:400])
        check_eq("stage_compare.runs: the baselines first, then the runs --run added, nothing twice",
                 (sc.runs(), (sc.EXTRA.append("base-off"), sc.runs())[1]), (["base-off", "man1"], ["base-off", "man1"]))
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code, code_stage = sc.main(["s2", "--run", "../x"]), sc.main(["s77"])
        check("stage_compare: a path as a run name and an unknown stage are refused by name, exit 2 (it was a KeyError)",
              (code, code_stage) == (2, 2) and "is not a copy name" in err.getvalue() and "unknown stage 's77'" in err.getvalue(),
              err.getvalue()[:300])
        # the story table's run: the bare suffix, the old folder spelling, and a folder that exists under its own name
        (base / "plainfolder").mkdir()
        check_eq("story_dir: the suffix man1 is <copy_prefix>man1 under BASE", sc.story_dir("man1", ticket),
                 base / (pre + "man1") / "test-harness" / "qa-factory" / "artifacts" / ticket)
        check_eq("story_dir: the full folder spelling is the same folder", sc.story_dir(pre + "man1", ticket),
                 sc.story_dir("man1", ticket))
        check_eq("story_dir: a folder that exists under BASE keeps its own name (no name that worked changes)",
                 sc.story_dir("plainfolder", ticket).parts[-5], "plainfolder")
        sc.STORY_RUNS = {"sr": pre + "sr"}
        check_eq("story_dir: a key of STORY_RUNS is still its folder", sc.story_dir("sr", ticket).parts[-5], pre + "sr")
    finally:
        (report_run.BASE, report_run.COPIES, spend_by_dispatch.BASE, spend_by_dispatch.RUNS,
         sc.BASE, sc.RUNS, sc.TASK, extra, sys.argv, paths.COPY_PREFIX, sc.STORY_RUNS) = saved
        sc.EXTRA[:] = extra

    # --- prepare_copy: the start line is the Start-Process form of docs/RUNBOOK.md 9.3, never `cd <project>`
    lines = prepare_copy.start_lines(r"C:\p\copy-man1\test-harness", "C:/pkg/qa-factory", "PROJ-1", "man1",
                                     runs=r"C:\r\runs")
    text = "\n".join(lines)
    check("start line: Start-Process with -WorkingDirectory on the copy's test-harness, and the pid is printed",
          'Start-Process -FilePath python -WorkingDirectory "C:\\p\\copy-man1\\test-harness"' in text
          and "-PassThru" in text, text)
    check("start line: the driver, the task, the package, and the logs the notebook names",
          '"C:/pkg/qa-factory/scripts/story_run.py","--task","PROJ-1"' in text and '"--plugin-dir","C:/pkg/qa-factory"' in text
          and '-RedirectStandardOutput "C:\\r\\runs\\man1-1.log"' in text and '-RedirectStandardError "C:\\r\\runs\\man1-1.err"' in text, text)
    check("start line: unbuffered (FR-43) and no `cd` into the project anywhere", '$env:PYTHONUNBUFFERED = "1"' in text
          and "cd " not in text and "Set-Location" not in text, text)
    check("start line: the interactive session is Start-Process too", 'Start-Process -FilePath claude -WorkingDirectory' in text, text)
    default_logs = "\n".join(prepare_copy.start_lines(r"C:\p\copy-man1\test-harness", "C:/pkg/qa-factory", "PROJ-1", "man1"))
    check("start line: with no runs folder named the logs go under BASE, never into the measurers' folder (edge 3)",
          str(HERE) not in default_logs
          and str(paths.table_path("runs_dir") or paths.BASE / "runs") in default_logs, default_logs)


FULL_TABLE = {
    "_comment": "a synthetic runs table: every known key", "task": "QA-7", "copy_prefix": SYNTH_PREFIX,
    "baselines": {"b1": "f1", "b2": "f2"}, "story_runs": {"s1": "g1"}, "default_left": "b1",
    "default_right": "b2", "story_ticket": "QA-8", "caches": {"b1": "runs/c.json"}, "runs_dir": "runs", "sample_task": "../sample", "live_repo": "live",
    "toolchain": {"import": "pkg", "tests": "suite/tests"}, "installed_plugins": ["plug@market", "plug@other"]}
DERIVED = ("import json, paths\n"
           "print(json.dumps({'b': paths.BASELINES, 's': paths.STORY_RUNS, 'p': paths.COPY_PREFIX, 't': paths.TASK,\n"
           " 'l': paths.DEFAULT_LEFT, 'r': paths.DEFAULT_RIGHT, 'st': paths.TABLE.get('story_ticket'), 'live': str(paths.LIVE_REPO), 'cache': str(paths.table_path('caches', 'b1')),\n"
           " 'other': str(paths.table_path('caches', 'zz')), 'runs': str(paths.table_path('runs_dir')),\n"
           " 'sample': str(paths.table_path('sample_task')), 'chain': paths.TABLE['toolchain'],\n"
           " 'plugins': paths.TABLE['installed_plugins']}))\n")


class RunsTableProbe:
    """What the runs-table groups share: a work folder, a writer of table files and a subprocess probe that strips the
    developer's own QA_RUNS_TABLE (edge 9) and points QA_RUNS_BASE at a folder that is not there."""

    def __init__(self, root: Path):
        self.work = root / "runs-table"
        self.work.mkdir()
        self.elsewhere = self.work / "elsewhere"

    def probe(self, code, value=None, cwd=HERE):
        import os
        import subprocess
        env = {k: v for k, v in os.environ.items() if k not in ("QA_RUNS_TABLE", "QA_RUNS_BASE")}
        env["QA_RUNS_BASE"] = str(self.elsewhere)
        if value is not None:
            env["QA_RUNS_TABLE"] = value
        return subprocess.run([sys.executable, "-B", "-c", code], cwd=str(cwd), env=env, capture_output=True,
                              text=True, encoding="utf-8")

    def table_file(self, name, content):
        path = self.work / name
        path.write_bytes(content if isinstance(content, bytes) else json.dumps(content).encode("utf-8"))
        return path


def runs_table_tests(root: Path) -> None:
    """The runs table (QA_RUNS_TABLE, paths.py): run names, ticket, copy prefix and caches are DATA of an experiment,
    not literals of the measurers. Subprocesses strip the developer's own QA_RUNS_TABLE (edge 9); the loader refuses
    a table that was asked for and cannot be used (I1), and importing any measurer without one prints nothing (I2).
    One group per concern, each under ~60 lines."""
    rt = RunsTableProbe(root)
    rt_without_table(rt)
    rt_full_table(rt)
    rt_refusals(rt)
    rt_require_args()
    rt_empty_prefix(root)
    rt_prepare_copy_and_run_headless(root)
    rt_run_headless_child(root)
    rt_key_prefix_strip(root)


def rt_without_table(rt: RunsTableProbe) -> None:
    """No table: empty, silent (I2); an empty variable is the same as none; the arguments have no default."""
    importing = "import paths, report_run, stage_compare, code_friction, context_shape, spend_by_dispatch, prepare_copy"
    quiet = rt.probe(importing)
    check("no QA_RUNS_TABLE: importing the measurers prints nothing on either stream",
          quiet.returncode == 0 and quiet.stdout == "" and quiet.stderr == "", quiet.stderr[-300:])
    for label, value in (("unset", None), ("empty", "")):
        shown = rt.probe("import paths; print(paths.TABLE, paths.COPY_PREFIX == '', paths.TASK, paths.LIVE_REPO, "
                         "paths.BASELINES)", value)
        check_eq(f"{label} QA_RUNS_TABLE: the table is empty, no prefix, no ticket, no live repo",
                 shown.stdout.strip(), "{} True None None {}")
    shown = rt.probe("import paths; print(paths.DEFAULT_LEFT, paths.DEFAULT_RIGHT)")
    check_eq("no table: default_left and default_right are None (the arguments are required)",
             shown.stdout.strip(), "None None")
    for argv0 in ("report_run", "report_to_gate", "stage_role_table"):
        done = rt.probe(f"import sys, {argv0}; sys.argv = ['{argv0}.py', '--left', 'x', '--ticket', 'T-1']; {argv0}.main()")
        check(f"{argv0} without a table and without --right: exit 2 naming --right, no traceback",
              done.returncode == 2 and "--right is required" in done.stderr and "Traceback" not in done.stderr,
              done.stderr[-300:])
    for argv0 in ("conductor_families", "spend_by_dispatch"):
        done = rt.probe(f"import sys, {argv0}; sys.argv = ['{argv0}.py', '--ticket', 'T-1']; sys.exit({argv0}.main())")
        check(f"{argv0} without a table and without --run: exit 2 naming --run, no traceback (no run literal)",
              done.returncode == 2 and "--run is required" in done.stderr and "Traceback" not in done.stderr,
              done.stderr[-300:])
    done = rt.probe("import sys, runpy; sys.argv = ['read_misses.py']; runpy.run_path('read_misses.py', run_name='__main__')")
    check("read_misses without a table and without a run: exit 2 saying the run is required, no traceback",
          done.returncode == 2 and "run is required" in done.stderr and "Traceback" not in done.stderr, done.stderr[-300:])
    done = rt.probe("import sys, stage_compare as sc; sys.exit(sc.story_main(['s0', '--story', 'T-1']))")
    check("stage_compare s0 --story without a table and without --ref-run: exit 2 naming --ref-run, no traceback",
          done.returncode == 2 and "--ref-run is required" in done.stderr and "Traceback" not in done.stderr,
          done.stderr[-300:])


def rt_full_table(rt: RunsTableProbe) -> None:
    """A full table: every known key is accepted (the boundary), every derived value is the table's, the defaults of
    the tools come from it, and a relative QA_RUNS_TABLE is resolved against the repository."""
    import os
    import paths
    check_eq("the boundary table carries EVERY key paths.TABLE_KEYS knows (a new key cannot be left untested)",
             set(FULL_TABLE), set(paths.TABLE_KEYS))
    path = rt.table_file("full.json", b"\xef\xbb\xbf" + json.dumps(FULL_TABLE).encode("utf-8"))
    done = rt.probe(DERIVED, str(path))
    got = json.loads(done.stdout) if done.returncode == 0 and done.stdout.strip() else {"error": done.stderr[-400:]}
    check_eq("a table with BOM and every known key: baselines, story runs, prefix, ticket, default left and right",
             (got.get("b"), got.get("s"), got.get("p"), got.get("t"), got.get("l"), got.get("r")),
             (FULL_TABLE["baselines"], FULL_TABLE["story_runs"], SYNTH_PREFIX, "QA-7", "b1", "b2"))
    check_eq("and story_ticket is the table's", got.get("st"), "QA-8")
    check_eq("and the live repo is a folder under BASE, the cache, runs folder and sample resolve from the table's folder",
             (got.get("live"), got.get("cache"), got.get("runs"), got.get("sample"), got.get("other")),
             (str(rt.elsewhere / "live"), os.path.normpath(rt.work / "runs/c.json"), os.path.normpath(rt.work / "runs"),
              os.path.normpath(rt.work / "../sample"), "None"))
    check_eq("and the toolchain proof and EVERY plugin id to disable are the table's",
             (got.get("chain"), got.get("plugins")),
             ({"import": "pkg", "tests": "suite/tests"}, ["plug@market", "plug@other"]))
    done = rt.probe("import sys, conductor_families as c; sys.argv = ['c.py', '--ticket', 'T-1']; sys.exit(c.main())", str(path))
    check("conductor_families with the table and no --run: the run is default_right (b2), read as its folder",
          done.returncode == 1 and "no conductor journal for b2" in done.stdout, done.stdout[-200:] + done.stderr[-200:])
    done = rt.probe("import sys, stage_compare as sc; sys.exit(sc.story_main(['s0', '--story', 'T-1']))", str(path))
    check("stage_compare s0 --story with the table and no --ref-run: the reference is the first story_runs key (s1)",
          done.returncode == 2 and "NOT MEASURED" in done.stdout and "--ref-run is required" not in done.stderr,
          done.stdout[-200:] + done.stderr[-200:])
    try:
        relative = os.path.relpath(path, paths.REPO)
    except ValueError:
        relative = None
    if relative:
        done = rt.probe("import sys; sys.path.insert(0, %r)\n" % str(HERE) + DERIVED, relative, cwd=rt.work)
        check("a relative QA_RUNS_TABLE is resolved against the repository, whatever the cwd",
              done.returncode == 0 and json.loads(done.stdout)["t"] == "QA-7", done.stderr[-300:])
    else:
        print("SKIP relative QA_RUNS_TABLE (the temp folder is on another drive than the repository)")


def rt_refusals(rt: RunsTableProbe) -> None:
    """A table that was asked for and cannot be used is a refusal naming the key, never a partial table (I1); each
    limit is tested AT it (accepted) and BEYOND it (refused)."""
    work = rt.work
    bad_tables = {
        "a folder, not a file": (str(work), "not a file"),
        "a file that is not there": (str(work / "missing.json"), "not a file"),
        "a JSON array": (rt.table_file("array.json", [1, 2]), "JSON object"),
        "not JSON": (rt.table_file("broken.json", b"{not json"), "JSON"),
        "one unknown key beyond the known ones": (rt.table_file("typo.json", dict(FULL_TABLE, baseline={})), "'baseline'"),
        "the old single installed_plugin key": (rt.table_file("old.json", {"installed_plugin": "a@b"}), "'installed_plugin'"),
        "a baseline folder with a separator": (rt.table_file("slash.json", {"baselines": {"a": "a/b"}}), "baselines"),
        "a story-run folder that starts with a dash": (rt.table_file("dash.json", {"story_runs": {"a": "-x"}}), "story_runs"),
        "a baseline folder that ends with a dot": (rt.table_file("dot.json", {"baselines": {"a": "x."}}), "baselines"),
        "a task that is not a string": (rt.table_file("task.json", {"task": 7}), "'task'"),
        "a story_ticket that is not a string": (rt.table_file("st.json", {"story_ticket": 7}), "'story_ticket'"),
        "a default_right that is not a string": (rt.table_file("right.json", {"default_right": 7}), "'default_right'"),
        "a live repo that is a path": (rt.table_file("live.json", {"live_repo": "a/b"}), "live_repo"),
        "a toolchain key that is not known": (rt.table_file("chain.json", {"toolchain": {"imports": "x"}}), "toolchain"),
        "installed_plugins that is a string": (rt.table_file("plug-str.json", {"installed_plugins": "a@b"}), "installed_plugins"),
        "installed_plugins with a non-string id": (rt.table_file("plug-int.json", {"installed_plugins": ["a@b", 7]}), "installed_plugins")}
    for n, prefix in enumerate(("C:", "a/", "a\\", "..", "x:y", "a b", 7)):
        bad_tables[f"a copy_prefix {prefix!r}"] = (rt.table_file(f"prefix{n}.json", {"copy_prefix": prefix}), "copy_prefix")
    for n, name in enumerate(("os; x", "-m", "", "a.", "1pkg", "a..b", "pkg sub")):
        bad_tables[f"a toolchain.import {name!r}"] = (rt.table_file(f"import{n}.json", {"toolchain": {"import": name}}),
                                                       "toolchain.import")
    for label, (value, want) in bad_tables.items():
        done = rt.probe("import paths", str(value))
        check(f"QA_RUNS_TABLE = {label}: refused, exit non-zero, RunsTableError naming {want!r}",
              done.returncode != 0 and "RunsTableError" in done.stderr and want in done.stderr, done.stderr[-300:])
    good = {"copy_prefix 'copy-' (at the boundary)": {"copy_prefix": "copy-"},
            "copy_prefix '' (the empty prefix)": {"copy_prefix": ""},
            "copy_prefix 'A_b.9-' (every allowed character)": {"copy_prefix": "A_b.9-"},
            "toolchain.import 'pkg'": {"toolchain": {"import": "pkg"}},
            "toolchain.import 'pkg.sub' (dotted)": {"toolchain": {"import": "pkg.sub"}},
            "installed_plugins [] (nothing disabled)": {"installed_plugins": []}}
    for n, (label, table) in enumerate(good.items()):
        done = rt.probe("import paths; print('loaded')", str(rt.table_file(f"good{n}.json", table)))
        check(f"QA_RUNS_TABLE with {label}: accepted", done.returncode == 0 and "loaded" in done.stdout, done.stderr[-300:])


def rt_require_args() -> None:
    """paths.require_args, the one refusal of an argument that has no default without a runs table."""
    import argparse
    import contextlib
    import io
    import paths
    ap = argparse.ArgumentParser(prog="t.py")
    err = io.StringIO()
    code = None
    with contextlib.redirect_stderr(err):
        try:
            paths.require_args(ap, ("--ok", "x"), ("--gone", None), ("--also", ""))
        except SystemExit as exc:
            code = exc.code
    check("paths.require_args: the first empty argument ends the run with exit 2 naming it and the variable",
          code == 2 and "--gone is required" in err.getvalue() and "QA_RUNS_TABLE" in err.getvalue()
          and "--also" not in err.getvalue(), err.getvalue()[-300:])
    check("and when every value is there it returns without a word", paths.require_args(ap, ("--a", "1"), ("--b", "2")) is None)


def rt_empty_prefix(root: Path) -> None:
    """The one rule that turns a run name into a folder, with an empty prefix (edge 5), and the stage_compare refusals
    with an empty table. Every module attribute it patches is restored in a `finally`."""
    import contextlib
    import io
    import paths
    import report_run
    import stage_compare as sc
    import conductor_families
    saved = (paths.COPY_PREFIX, sc.TASK, dict(sc.RUNS), list(sc.EXTRA), sc.BASE,
             conductor_families.BASE, conductor_families.RUNS)
    paths.COPY_PREFIX = ""
    try:
        check_eq("copy_folder with no prefix: a name no table holds is the folder of the same name",
                 paths.copy_folder("man1", {}), "man1")
        check_eq("copy_folder: a baseline keeps its folder, with or without a prefix",
                 paths.copy_folder("b1", {"b1": "f1"}), "f1")
        try:
            paths.copy_folder("../x", {})
            refused = ""
        except ValueError as exc:
            refused = str(exc)
        check("copy_folder with no prefix: a path is still refused by name", "is not a copy name" in refused, refused)
        check("report_run.copy_folder is the same function (one rule)", report_run.copy_folder is paths.copy_folder)
        check_eq("story_dir with no prefix: startswith('') does not turn every name into a folder",
                 sc.story_dir("nobody", "T-1").parts[-5], "nobody")

        # --- stage_compare: no ticket and no runs are refusals with the form to pass, exit 2 -------
        sc.RUNS, sc.TASK, sc.BASE = {}, None, root / "rt-base"
        for argv, want in ((["s2"], "no ticket"), (["s2", "--ticket", "T-9"], "no runs"),
                           (["s2", "--run", "man1"], "no ticket")):
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                code = sc.main(argv)
            sc.TASK = None
            check(f"stage_compare.main({argv}) with an empty table: exit 2 and {want!r}, no traceback",
                  code == 2 and want in err.getvalue(), err.getvalue()[:300])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = sc.main(["s2", "--run", "man1", "--ticket", "T-9"])
        check("stage_compare.main with --ticket and --run and an empty table: runs, the ticket is the flag's",
              code == 0 and sc.TASK == "T-9" and "man1" in out.getvalue(), out.getvalue()[:300])

        # --- a baseline name given to the other tools is not an argparse 'invalid choice' -----------
        conductor_families.BASE, conductor_families.RUNS = root / "rt-base", {}
        code, printed = run_main(conductor_families, ["--run", "man1", "--ticket", "T-9"])
        check("conductor_families --run man1 with an empty table reads the folder man1 (no 'invalid choice')",
              code == 1 and "no conductor journal for man1" in printed, printed[:300])
    finally:
        (paths.COPY_PREFIX, sc.TASK, sc.RUNS, sc.BASE, conductor_families.BASE, conductor_families.RUNS) = (
            saved[0], saved[1], saved[2], saved[4], saved[5], saved[6])
        sc.EXTRA[:] = saved[3]


def rt_prepare_copy_and_run_headless(root: Path) -> None:
    """prepare_copy and run_headless without what the table would name."""
    import contextlib
    import io
    import paths
    import prepare_copy
    import run_headless
    saved = (paths.TABLE, paths.BASE, prepare_copy.LIVE_REPO, run_headless.ROOT, sys.argv)
    paths.TABLE, paths.BASE, prepare_copy.LIVE_REPO, run_headless.ROOT = {}, root / "rt-base", None, root / "rt-base"
    try:
        err = io.StringIO()
        sys.argv = ["prepare_copy.py", "--name", "man1"]
        with contextlib.redirect_stderr(err):
            code = prepare_copy.main()
        check("prepare_copy.main with no live_repo in the table: exit 2 and 'live_repo', no copy made",
              code == 2 and "live_repo" in err.getvalue(), err.getvalue()[:300])
        try:
            prepare_copy.prepare_toolchain(root, run=lambda *a, **k: None)
            raised = ""
        except prepare_copy.ToolchainNotReady as exc:
            raised = str(exc)
        check("prepare_copy.prepare_toolchain with no proof named anywhere: refused, nothing started",
              "no toolchain proof" in raised, raised)
        err = io.StringIO()
        sys.argv = ["run_headless.py", "--name", "nobody", "--message", "hi", "--out", str(root / "rt-out.json")]
        with contextlib.redirect_stderr(err):
            code = run_headless.main()
        check("run_headless --name nobody: exit 2 and 'no copy at', before claude is started",
              code == 2 and "no copy at" in err.getvalue() and not (root / "rt-out.json").exists(), err.getvalue()[:300])
    finally:
        paths.TABLE, paths.BASE, prepare_copy.LIVE_REPO, run_headless.ROOT, sys.argv = saved


def rt_run_headless_child(root: Path) -> None:
    """run_headless gives its child the desktop road: E16 a parent env with a run mode, a stale plugin root, a host
    session marker and an ordinary key; E17 a plugin path with spaces is one argv element and no env value."""
    import contextlib
    import io
    import os
    import paths
    import run_headless
    base = {"QA_FACTORY_RUN_MODE": "driver", "CLAUDE_PLUGIN_ROOT": "/other/copy", "CLAUDE_CODE_CHILD_SESSION": "1",
            "X": "1"}
    before = dict(base)
    got = run_headless.child_env(base)
    rows = [("E16 env: no run mode, no stale root, no host session marker",
             not {"QA_FACTORY_RUN_MODE", "CLAUDE_PLUGIN_ROOT", "CLAUDE_CODE_CHILD_SESSION"} & set(got)),
            ("E16 env: other keys kept, ceiling is '0'",
             got.get("X") == "1" and got.get("CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS") == "0"),
            ("E16 env: the base dict is not mutated", base == before)]
    spaced = "C:/my plugins/qa-factory"
    seen = {}

    def fake_run(cmd, **kw):
        seen["cmd"], seen["env"] = cmd, kw.get("env") or {}
        return type("R", (), {"stdout": "", "stderr": "", "returncode": 0})()

    saved = (paths.TABLE, paths.BASE, run_headless.ROOT, run_headless.PLUGIN, run_headless.subprocess.run, sys.argv,
             os.environ.get("CLAUDE_PLUGIN_ROOT"))
    paths.TABLE, paths.BASE, run_headless.ROOT, run_headless.PLUGIN = {}, root / "rt-base", root / "rt-base", spaced
    (root / "rt-base" / paths.copy_folder("sp1", {}) / "test-harness").mkdir(parents=True, exist_ok=True)
    run_headless.subprocess.run = fake_run
    os.environ["CLAUDE_PLUGIN_ROOT"] = "/stale"
    sys.argv = ["run_headless.py", "--name", "sp1", "--message", "hi", "--out", str(root / "rt-sp.json")]
    try:
        with contextlib.redirect_stdout(io.TextIOWrapper(io.BytesIO())):   # main() reconfigures stdout
            run_headless.main()
    finally:
        (paths.TABLE, paths.BASE, run_headless.ROOT, run_headless.PLUGIN, run_headless.subprocess.run, sys.argv,
         stale) = saved
        if stale is None:
            os.environ.pop("CLAUDE_PLUGIN_ROOT", None)
        else:
            os.environ["CLAUDE_PLUGIN_ROOT"] = stale
    cmd = seen.get("cmd") or []
    at = cmd.index("--plugin-dir") if "--plugin-dir" in cmd else -1
    rows += [("E17 argv: the spaced path is the one element after --plugin-dir, verbatim",
              at >= 0 and cmd[at + 1] == spaced and cmd.count(spaced) == 1),
             ("E17 env: the child env carries no plugin root and no run mode",
              "CLAUDE_PLUGIN_ROOT" not in seen.get("env", {"CLAUDE_PLUGIN_ROOT": 1})
              and "QA_FACTORY_RUN_MODE" not in seen.get("env", {"QA_FACTORY_RUN_MODE": 1}))]
    for label, ok in rows:
        check(f"run_headless child: {label}", ok, str(seen)[:300])


def rt_key_prefix_strip(root: Path) -> None:
    """stage_compare s1 shows a source by its ticket number: the key prefix of the TASK is stripped from the ref
    (`QA-7` -> `7`); a ref of another project keeps its whole name; a task with no dash strips nothing."""
    import contextlib
    import io
    import stage_compare as sc
    saved = (sc.BASE, dict(sc.RUNS), sc.TASK, list(sc.EXTRA))
    base = root / "kp-base"
    inventory = {"sources": [{"canonical_ref": "browse/QA-7", "relevance": "relevant"},
                             {"canonical_ref": "browse/OTHER-9", "relevance": "relevant"},
                             {"canonical_ref": "browse/QA-5", "relevance": "not_relevant"}]}
    sc.BASE, sc.RUNS = base, {"kp": "kp"}
    sc.EXTRA[:] = []
    try:
        for task, relevant, excluded in (("QA-7", "7,OTHER-9", "5"), ("NOKEY", "OTHER-9,QA-7", "QA-5")):
            put_json(base / "kp" / "test-harness" / "qa-factory" / "artifacts" / task / "work" / "source-inventory.json",
                     inventory)
            sc.TASK = task
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                sc.s1()
            lines = {ln.split("|")[0].strip(): [c.strip() for c in ln.split("|")[1:]] for ln in out.getvalue().splitlines()}
            check_eq(f"stage_compare s1 with the task {task!r}: relevant and excluded sources print as {relevant!r} / {excluded!r}",
                     (lines.get("relevant"), lines.get("excluded")), ([relevant], [excluded]))
    finally:
        sc.BASE, sc.RUNS, sc.TASK = saved[0], saved[1], saved[2]
        sc.EXTRA[:] = saved[3]


def verdict_word_tests() -> None:
    """K-N8.25 (t-305 N8, FR-28): the three readers of the ledger's delivery verdict print the WORD - `after_checks` is
    not read as `no` (the truthiness of a three-valued field), and the string "no" is never read as ready."""
    import check_all_contracts
    import compare
    import stage_compare
    third = {"delivery_verdict": "after_checks", "delivery_ready": False, "reason_records": [], "blocked_by": []}
    for ledger, want in ((third, "after_checks"), ({"delivery_verdict": "yes", "delivery_ready": True}, "yes"),
                         ({"delivery_ready": False}, "no"), ({"delivery_ready": True}, "yes"),
                         ({"delivery_ready": "no"}, "unknown"), (None, None)):
        check_eq(f"verdict word: compare.verdict_word({ledger}) is {want}", compare.verdict_word(ledger), want)

    class Run:
        J = staticmethod(lambda rel: third)
    notes = []
    check_all_contracts.s8_scribe_to_gate_b(Run, lambda c, kind, field, text: notes.append((field, text)))
    check_eq("check_all_contracts prints the word for delivery.ready", dict(notes)["delivery.ready"], "after_checks")
    # stage_compare reads it through the same function (no private reading of the bool is left in the three files)
    for module in (compare, stage_compare, check_all_contracts):
        source = Path(module.__file__).read_text(encoding="utf-8")
        check(f"{module.__name__} does not read the verdict as a truth value",
              not re.search(r'(\.get\("delivery_ready"\)|(ledger|led)\["delivery_ready"\])', source), module.__name__)
    check("stage_compare asks compare.verdict_word", "compare.verdict_word(" in
          Path(stage_compare.__file__).read_text(encoding="utf-8"))


def types_module(module, name):
    """A stand-in module whose main() is `module.<name>` with the shared argv - for run_main."""
    import types
    stand = types.ModuleType(name)
    stand.main = lambda: getattr(module, name)(sys.argv[1:])
    return stand


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="qa-measurers-"))
    try:
        build(root)
        base = root / "copies"

        # --- spend_by_dispatch: the arithmetic under every figure of the delivery -------------
        import spend_by_dispatch
        spend_by_dispatch.BASE, spend_by_dispatch.RUNS = base, {RUN: RUN}
        rows = [json.loads(line) for line
                in (base / RUN / "test-harness/qa-factory/artifacts" / TICKET /
                    "state/driver-runs.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        total = sum(r["total_cost_usd"] for r in rows)
        check_eq("spend_by_dispatch reads every session of the journal", len(rows), 4)
        check_eq("and its total is their sum", round(total, 2), 3.75)
        conductor = sum(r["total_cost_usd"] for r in rows if r.get("kind") == "conductor")
        check_eq("the conductor's share is its own sessions, not a proportion", round(conductor, 2), 0.25)
        first = sum(r["total_cost_usd"] for r in rows if r.get("dispatch") == "S1-qa-scout-1")
        repeat = sum(r["total_cost_usd"] for r in rows if r.get("dispatch") == "S1-qa-scout-2")
        check_eq("the first dispatch of a (stage, role) carries its resumptions", round(first, 2), 1.50)
        check_eq("and every later dispatch of the same pair is counted apart", round(repeat, 2), 2.00)
        for label, want, cost, turns in (("resumed", True, 0.50, 5), ("fresh", False, 3.00, 20)):
            sessions = [r for r in rows if r.get("kind") == "role" and bool(r.get("resumed")) is want]
            check_eq(f"{label} sessions cost ${cost:.2f} over {turns} turns",
                     (round(sum(r["total_cost_usd"] for r in sessions), 2),
                      sum(r["num_turns"] for r in sessions)), (cost, turns))
        check_eq("so a resumed turn is dearer than a fresh one, by the run's own numbers",
                 (round(0.50 / 5, 4) > round(3.00 / 20, 4)), False)

        # The script itself runs over the fixture and prints the same totals.
        import io
        import contextlib
        buffer = io.StringIO()
        sys.argv = ["spend_by_dispatch.py", "--run", RUN, "--ticket", TICKET]
        with contextlib.redirect_stdout(buffer):
            spend_by_dispatch.main()
        printed = buffer.getvalue()
        check("spend_by_dispatch prints the total it read", "$3.75" in printed, printed[:300])
        check("and names the conductor's share", "conductor **$0.25**" in printed, printed[:600])

        # --- conductor_families: a family is a group of SESSIONS ------------------------------
        import conductor_families
        conductor_families.BASE, conductor_families.RUNS = base, {RUN: RUN}
        families = {}
        for row in CONDUCTOR:
            key = conductor_families.family(row["refusal"])
            entry = families.setdefault(key, [0, 0.0])
            entry[0] += 1
            entry[1] += row["total_cost_usd"]
        window = [value for key, value in families.items() if "receipt" in key]
        check_eq("three sessions raised for one refusal are three sessions, not one",
                 [item[0] for item in window], [3])
        check_eq("and their money is the sum of all three",
                 [round(item[1], 2) for item in window], [0.30])
        check_eq("a different refusal is a different family", len(families), 2)
        buffer = io.StringIO()
        sys.argv = ["conductor_families.py", "--run", RUN, "--ticket", TICKET]
        with contextlib.redirect_stdout(buffer):
            conductor_families.main()
        printed = buffer.getvalue()
        check("the script's own table counts sessions, not distinct texts",
              "| 3 | $0.30 |" in printed, printed[:900])
        check("and says how many the driver's table would have answered by code",
              "**1 of 4**" in printed, printed[:900])

        name, action = conductor_families.known_match(CONDUCTOR[3]["refusal"])
        check_eq("the driver's own table would have answered the second one by code",
                 (name, action), ("active_dispatch", "continue"))
        check_eq("and would not have answered the first", conductor_families.known_match(REPEATED)[0], None)

        # --- report_run: whose money, and whose cache -----------------------------------------
        import compare
        import report_run
        report_run.BASE, report_run.COPIES = base, {RUN: RUN, "other": RUN}
        compare.transcript_dir = lambda project: root / "transcripts"
        money = report_run.money(RUN, TICKET)
        check_eq("the story's money is the sessions its own journal names (FR-24)",
                 {agent: round(value["cost_usd"], 2) for agent, value in money.items()},
                 {"qa-scout": 3.00})
        check("the operator's own session in the same folder is not the story's money",
              all(round(value["cost_usd"], 2) != 6.00 for value in money.values()), str(money))

        cache = root / "cache.json"
        cache.write_text(json.dumps({"cost": {"by_role": {"orchestrator": {
            "requests": 9, "cost_usd": 109.00, "dispatches": 1}}}}), encoding="utf-8")
        check_eq("a cache is read for the run it belongs to",
                 round(report_run.money(RUN, TICKET, cache)["orchestrator"]["cost_usd"], 2), 109.00)
        check_eq("and the same call without it measures the run itself (FR-27)",
                 {agent: round(value["cost_usd"], 2) for agent, value in report_run.money(RUN, TICKET).items()},
                 {"qa-scout": 3.00})
        # --- compare: the pricing every money number in this folder is built on ------------
        rate = compare.rates()
        priced = compare.price(rate, MODEL, {"input_tokens": 1_000_000, "output_tokens": 100_000,
                                             "cache_read_input_tokens": 2_000_000})
        # $3 + $1.50 + $0.60 at the published Sonnet rates, straight from model-rates.json.
        check_eq("a request is priced from the rate table, token kind by token kind",
                 round(priced, 2), 5.10)
        check_eq("a model the table does not know is priced as unknown, never as free",
                 compare.price(rate, "no-such-model", {"input_tokens": 1_000_000}), None)

        # --- report_to_gate: the same money, cut at the start of S5 --------------------------
        import report_to_gate
        cut = report_to_gate.cut_at(RUN, TICKET)
        check("a run that never reached S5 is cut at now, not at zero", cut.year >= 2026, str(cut))
        role, requests, cost, unpriced = report_to_gate.scan_until(
            root / "transcripts" / "sess-a.jsonl", rate, cut)
        check_eq("and up to that cut it reads the same session the same way",
                 (role, requests, round(cost, 2), unpriced), ("qa-scout", 1, 3.00, 0))
        past = report_to_gate.scan_until(root / "transcripts" / "sess-a.jsonl", rate,
                                         datetime(2026, 1, 1, tzinfo=timezone.utc))
        check_eq("a cut before the run counts nothing of it", (past[1], round(past[2], 2)), (0, 0.00))

        # a synthetic runs table that gives ONE run a cache (FR-27, edge 4)
        import paths
        saved_table = (paths.TABLE, paths.TABLE_FILE)
        paths.TABLE, paths.TABLE_FILE = {"caches": {"base-off": "runs/compare-off.json"}}, root / "tables" / "t.json"
        try:
            chosen = report_run.cache_for("other-run", "")
            check_eq("no run but the one the table names has a default cache, so nothing is substituted", chosen, None)
            check_eq("the run the table names keeps its own, from the folder of the table",
                     report_run.cache_for("base-off", ""), root / "tables" / "runs" / "compare-off.json")
            named = report_run.cache_for("other-run", "cache.json")
            check_eq("a cache named on the command line is used for whatever run named it, relative to the cwd",
                     named, Path("cache.json"))
        finally:
            paths.TABLE, paths.TABLE_FILE = saved_table

        more(root, base)
        fidelity(root)
        unpriced_sum(root)
        stage_role_table_tests(root)
        jira_light_tests(root)
        b267_tests(root)
        runs_table_tests(root)
        verdict_word_tests()
    finally:
        shutil.rmtree(root, ignore_errors=True)

    bad = sum(1 for ok, _ in RESULTS if not ok)
    print(f"\n=== test_measurers: {len(RESULTS) - bad}/{len(RESULTS)} ok ===")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
