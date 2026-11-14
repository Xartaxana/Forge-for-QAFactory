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


# --- the run scoreboard (P1-v N6): one table per behaviour, the case id names the row ------------------------------
# The same tables run two ways: `python -m pytest experiments/measurers/test_measurers.py` (one parameterised test per table, the
# parameter id is the case) and `python -B experiments/measurers/test_measurers.py` (the self-running list above, `check` per case).
try:
    import pytest
except ImportError:                                  # the self-running form needs no pytest
    pytest = None


def _parametrize(cases):
    if pytest is None:
        return lambda function: function
    return pytest.mark.parametrize("case", cases, ids=[c[0] for c in cases])


def _sb():
    import scoreboard
    return scoreboard


def sb_cli(*argv):
    """(code, stdout, stderr) of `scoreboard.main(argv)`."""
    import io
    import contextlib
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = _sb().main([str(a) for a in argv])
        except SystemExit as stop:
            code = stop.code
    return code, out.getvalue(), err.getvalue()


def sb_run(tmp: Path, name="run", start="2026-11-01T10:00:00+00:00", run_class="live", role_s=300, questions=0,
           cumulative=False, process=True) -> Path:
    """A story folder (qa-factory/artifacts/QA-9) with the carriers run_counters reads: one process window of 20 minutes, one first-pass
    role call of `role_s` seconds and one resumed call of 100 s that names a check; `questions` rows of driver-questions.jsonl."""
    from datetime import datetime, timedelta
    t0 = datetime.fromisoformat(start)
    at = lambda minutes: (t0 + timedelta(minutes=minutes)).isoformat()  # noqa: E731
    task = tmp / name / "qa-factory" / "artifacts" / "QA-9"
    (task / "state").mkdir(parents=True)
    sid = "stub-S1-qa-scout-1-1" if run_class != "live" else "sess-1"
    rows = []
    if process:
        rows.append({"kind": "process", "event": "end", "since": at(0), "ts": at(20), "package": "p1", "config_sha": None,
                     "answer_file": False, "run_class": run_class, "process_code": 0, "question_kind": None})
    rows.append({"kind": "role", "role": "qa-scout", "stage": "S1", "dispatch": "S1-qa-scout-1", "session_id": sid, "ts": at(5),
                 "wall_ms": role_s * 1000, "duration_ms": role_s * 1000 - 5000, "resumed": False, "is_error": False,
                 **({"total_cost_usd": 0.424} if cumulative else {})})
    rows.append({"kind": "role", "role": "qa-scout", "stage": "S1", "dispatch": "S1-qa-scout-1", "session_id": sid, "ts": at(8),
                 "wall_ms": 100000, "duration_ms": 95000, "resumed": True, "resume_kind": "refusal_resume",
                 "checks": ["s5_precheck:manifest"], "checks_n": {"s5_precheck:manifest": 2}, "is_error": False,
                 **({"total_cost_usd": 0.455} if cumulative else {})})
    (task / "state" / "driver-runs.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    if questions:
        (task / "state" / "driver-questions.jsonl").write_text(
            "\n".join(json.dumps({"ts": at(3), "kind": "k", "stage": "S1", "source": "driver", "why_person": "x"}) for _ in range(questions)) + "\n",
            encoding="utf-8")
    return task


def sb_assemble(task: Path, out: Path, *extra, arm="factory", version="9.9.9"):
    return sb_cli("assemble", "--task-root", task, "--stand", "mybooks", "--story", "add-to-cart", "--arm", arm, "--version", version,
                  "--out-root", out, *extra)


def sb_files(out: Path) -> list:
    return sorted((out / "mybooks" / "add-to-cart").glob("*.yaml")) if (out / "mybooks" / "add-to-cart").is_dir() else []


def sb_yaml(path):
    import yaml
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def sb_truth(path: Path, ids=(1, 2, 3)) -> Path:
    import yaml
    path.write_text(yaml.safe_dump({"schema": "truth/1", "versions": [{"id": "v1", "cards": [{"id": i, "class": "bug"} for i in ids]},
                                                                       {"id": "v2", "cards": [{"id": i, "class": "bug"} for i in ids]}]}), encoding="utf-8")
    return path


def sb_judgment(path: Path, rows) -> Path:
    import yaml
    if isinstance(rows, bytes):
        path.write_bytes(rows)
    elif isinstance(rows, str):
        path.write_text(rows, encoding="utf-8")
    else:
        path.write_text(yaml.safe_dump({"schema": "judgment/1", "evaluated_against_version": "v1",
                                        "key": {"X": {"arm": "free"}, "Y": {"arm": "factory"}}, "card_rows": rows}, allow_unicode=True), encoding="utf-8")
    return path


def sb_good_rows(ids=(1, 2, 3)) -> list:
    return [{"card": i, "arm": arm, "verdict": "found" if (arm == "Y" and i == 1) else "missed", "unsure": arm == "Y" and i == 3}
            for arm in ("X", "Y") for i in ids]


def sb_rows_file(tmp: Path) -> Path:
    """A copy of rows.json that declares a verdict vocabulary and the categories of QA1 (the shipped file declares none)."""
    doc = json.loads((HERE.parent / "scoreboards" / "rows.json").read_text(encoding="utf-8"))
    doc["verdicts"] = {"found": "found", "missed": "missed"}
    doc["rows"]["QA1"]["quality"]["categories"] = ["found"]
    path = tmp / "rows-vocabulary.json"
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


def _dup(rows):
    return rows + [dict(rows[-1])]


SB_JUDGMENT_CASES = [
    # (case id, how the judgment rows are changed -> rows | text | bytes, the refusal's words or None when the file is accepted)
    ("AT: exactly the truth's card count", lambda r: r, None),
    ("BEYOND: one extra card", lambda r: r + [{"card": 4, "arm": "Y", "verdict": "found"}], "card 4 is not in truth version v1"),
    ("a card listed twice", _dup, "listed twice"),
    ("a card of the truth with no row", lambda r: [x for x in r if not (x["card"] == 2 and x["arm"] == "Y")], "card 2 of truth version v1 has no verdict row"),
    ("a verdict word outside the vocabulary", lambda r: [dict(r[0], arm="Y", verdict="maybe")] + r[1:], "verdict word 'maybe'"),
    ("a list where the card id is a scalar", lambda r: r + [{"card": [1, 2], "arm": "Y", "verdict": "found"}], "`card` must be a scalar"),
    ("a mapping where the verdict is a text", lambda r: [dict(x, verdict={"a": 1}) if x["arm"] == "Y" and x["card"] == 1 else x for x in r], "`verdict` must be a non-empty text"),
    ("an empty file", lambda r: "", "is empty"),
    ("non-UTF-8 bytes", lambda r: b"card_rows: \xff\xfe\n", "is not UTF-8 text"),
    ("10,000 rows", lambda r: [{"card": n, "arm": "Y", "verdict": "found"} for n in range(10000)], "and 9"),
    ("a truth version the truth file lacks", lambda r: r, "has no version v9"),
]


def sb_judgment_case(tmp: Path, case) -> None:
    name, mutate, want = case
    task, out, truth = sb_run(tmp), tmp / "out", sb_truth(tmp / "truth.yaml")
    rows = mutate(sb_good_rows())
    judgment = sb_judgment(tmp / "judgment.yaml", rows)
    extra = ["--truth", truth, "--judgment", judgment, "--rows", sb_rows_file(tmp)]
    if name.startswith("a truth version"):
        extra += ["--truth-version", "v9"]
    code, printed, err = sb_assemble(task, out, *extra)
    if want is None:
        assert code == 0, err
        doc = sb_yaml(sb_files(out)[0])
        assert doc["run"]["truth_version"] == "v1"
        assert (doc["rows"]["QA1"]["state"], doc["rows"]["QA1"]["value"]) == ("measured", 1), doc["rows"]["QA1"]
        assert "1 unsure card(s)" in doc["rows"]["QA2"]["why"] or doc["rows"]["QA2"]["state"] == "unknown"
    else:
        assert code == 2 and want in err, (code, err[:400])
        assert "RED" in err and str(judgment) in err or "truth" in err
        assert sb_files(out) == [], "a refused judgment wrote a file"
        assert len(err) < 4000, "the refusal is not bounded"


SB_MONEY_CASES = [
    ("agreement: the value of task_price", {"status": "agrees", "price_low_usd": 0.455, "price_high_usd": 0.455}, "live", True, "measured", 0.455),
    ("a journal whose session totals rise is NOT summed (0.424 then 0.455 stays task_price's 0.455)",
     {"status": "agrees", "price_low_usd": 0.455, "price_high_usd": 0.455}, "live", True, "measured", 0.455),
    ("differs: the state range, the value {low, high, note}", {"status": "differs", "finding": "A and B differ", "price_low_usd": 2.0, "price_high_usd": 3.5},
     "live", False, "range", {"low": 2.0, "high": 3.5, "note": "A and B differ"}),
    ("incomplete: the state at_least, the value {at_least, note}", {"status": "incomplete", "finding": "a session has no record", "price_low_usd": 1.0,
                                                                     "price_high_usd": 1.0}, "live", False, "at_least",
     {"at_least": 1.0, "note": "a session has no record"}),
    ("not_cross_checked: the state one_source, the value {value, note: one source}",
     {"status": "not_cross_checked", "price_low_usd": 0.4, "price_high_usd": 0.4}, "live", False, "one_source", {"value": 0.4, "note": "one source"}),
    ("a status task_price does not define: unknown naming it, never measured", {"status": "mystery", "price_low_usd": 0.4, "price_high_usd": 0.4},
     "live", False, "unknown", None),
    ("agrees but the ends differ: a range, not a scalar", {"status": "agrees", "price_low_usd": 1.0, "price_high_usd": 2.0}, "live", False, "range",
     {"low": 1.0, "high": 2.0, "note": "task_price status agrees but the low and high ends differ"}),
    ("no price at all", {"status": "incomplete", "finding": "No session of this task has a record."}, "live", False, "unknown", None),
    ("task_price raises", RuntimeError("boom"), "live", False, "unknown", None),
    ("a dry run has no money", {"status": "agrees", "price_low_usd": 9.0, "price_high_usd": 9.0}, "dry", False, "n/a", None),
]


def sb_money_case(tmp: Path, case) -> None:
    import contextlib
    name, answer, run_class, cumulative, state, value = case
    scoreboard = _sb()

    def fake(root, task):
        if isinstance(answer, Exception):
            raise answer
        return answer
    saved, scoreboard.TP.task_price = scoreboard.TP.task_price, fake
    try:
        code, _printed, err = sb_assemble(sb_run(tmp, run_class=run_class, cumulative=cumulative), tmp / "out")
    finally:
        scoreboard.TP.task_price = saved
    assert code == 0, err
    row = sb_yaml(sb_files(tmp / "out")[0])["rows"]["X1"]
    assert (row["state"], row["value"]) == (state, value), row
    assert row["unit"] == "usd"
    if name.startswith("a status task_price does not define"):
        assert "mystery" in row["why"], row


def _m(value):
    return {"state": "measured", "value": value}


_U = {"state": "unknown", "value": None, "why": "not recorded"}


def _bar(value, truth="v1", row="T1"):
    return {"run": {"truth_version": truth}, "rows": {row: _m(value), "QA1": _m(value)}}


SB_NORM_CASES = [
    # (case id, norm, rows, run class, bar, truth version, verdict)
    ("N-questions AT the norm (40)", "N-questions", {"Q1": _m(40)}, "live", None, None, "green"),
    ("N-questions BEYOND the norm (41)", "N-questions", {"Q1": _m(41)}, "live", None, None, "red"),
    ("an unknown row is never green", "N-questions", {"Q1": _U}, "live", None, None, "unknown"),
    ("N-gate within the norm, no unknown check", "N-gate", {"G1": _m(16), "G1u": _m(0)}, "live", None, None, "green"),
    ("N-gate within the norm but the unknown check is above it: unknown (AR-28)", "N-gate", {"G1": _m(3), "G1u": _m(17)}, "live", None, None, "unknown"),
    ("N-gate beyond the norm is red whatever the unknown count", "N-gate", {"G1": _m(17), "G1u": _m(17)}, "live", None, None, "red"),
    ("N-wall with no bar is unknown (7.5)", "N-wall", {"T1x": _m(357)}, "live", None, None, "unknown"),
    ("N-wall ratio AT the norm (357 / 10 = 35.7)", "N-wall", {"T1x": _m(357)}, "live", _bar(10), None, "green"),
    ("N-wall ratio BEYOND the norm (358 / 10 = 35.8)", "N-wall", {"T1x": _m(358)}, "live", _bar(10), None, "red"),
    ("N-wall with a bar of 0 is unknown, never a ratio", "N-wall", {"T1x": _m(358)}, "live", _bar(0), None, "unknown"),
    ("N-brief: the norm value is not set, so unknown even when measured", "N-brief", {"B1": _m(0)}, "live", None, None, "unknown"),
    ("a dry run judges no norm (K7)", "N-questions", {"Q1": _m(1)}, "dry", None, None, "unknown"),
    ("an unknown run class judges no norm (K7)", "N-questions", {"Q1": _m(1)}, "unknown", None, None, "unknown"),
    ("quality worse than the bar of the same truth version: red", "N-quality-QA1", {"QA1": _m(1)}, "live", _bar(2), "v1", "red"),
    ("quality equal to the bar: green", "N-quality-QA1", {"QA1": _m(2)}, "live", _bar(2), "v1", "green"),
    ("quality against a bar of another truth version: unknown", "N-quality-QA1", {"QA1": _m(9)}, "live", _bar(2, "v2"), "v1", "unknown"),
    ("quality against no bar: unknown", "N-quality-QA1", {"QA1": _m(9)}, "live", None, "v1", "unknown"),
    ("a quality row with no declared direction is not decided", "N-quality-QA3", {"QA3": _m(1)}, "live", _bar(2, row="QA3"), "v1", "unknown"),
]


def sb_norm_case(tmp: Path, case) -> None:
    _name, norm, rows, run_class, bar, truth, want = case
    scoreboard = _sb()
    judged = scoreboard.judge_norms(scoreboard.load_norms(), rows, run_class, bar, truth, scoreboard.load_rows())
    assert judged[norm]["verdict"] == want, judged[norm]


def _norms():
    """The shipped norms.json (norms/2) as the K2/K5 view `load_norms` returns: {norms: {id: ...}, raises: [...], rows, bar_changes}."""
    return _sb().load_norms(HERE.parent / "scoreboards" / "norms.json")


def _edit(doc, fn):
    fn(doc)
    return doc


RAISE = {"norm": "N-questions", "from": 40, "to": 50, "raised_by": "Lead", "reason": "the story grew", "word": "owner, 14.11.2026"}


def _set_value(nid, value):
    return lambda d: d["norms"][nid].update(value=value)


SB_RATCHET_CASES = [
    # (case id, edit of the new file, edit of the old file or None (then no --against), words of the problem or None when green)
    ("the shipped file is green", lambda d: None, None, None),
    ("a looser value with no raise row", _set_value("N-questions", 50), None, "looser than its baseline"),
    ("a tighter value is green", _set_value("N-questions", 30), None, None),
    ("a raise with raised_by, reason and the owner's word is green",
     lambda d: (d["raises"].append(dict(RAISE)), d["norms"]["N-questions"].update(value=50)), None, None),
    ("a raise without the owner's word", lambda d: (d["raises"].append({k: v for k, v in RAISE.items() if k != "word"}), d["norms"]["N-questions"].update(value=50)),
     None, "needs `norm`, `raised_by`, `reason`"),
    ("a raise without raised_by", lambda d: (d["raises"].append({k: v for k, v in RAISE.items() if k != "raised_by"}), d["norms"]["N-questions"].update(value=50)),
     None, "needs `norm`, `raised_by`, `reason`"),
    ("a raise with an empty reason", lambda d: (d["raises"].append(dict(RAISE, reason=" ")), d["norms"]["N-questions"].update(value=50)), None, "needs `norm`"),
    ("a 'raise' to a stricter value", lambda d: (d["raises"].append(dict(RAISE, to=30)), d["norms"]["N-questions"].update(value=30)), None, "is not looser"),
    ("a raise that starts from a wrong baseline", lambda d: (d["raises"].append(dict(RAISE, **{"from": 35})), d["norms"]["N-questions"].update(value=50)),
     None, "the baseline is 40"),
    ("a norm the raise row does not name stays refused", lambda d: (d["raises"].append(dict(RAISE)), d["norms"]["N-gate"].update(value=20)), None, "norm N-gate"),
    ("against: `initial` rewritten", _set_value("N-questions", 40), lambda o: o["norms"]["N-questions"].update(initial=30, value=30), "`initial` changed"),
    ("against: a norm dropped", lambda d: d["norms"].pop("N-gate"), lambda o: None, "was dropped"),
    ("against: looser than before with no new raise row", lambda d: (d["norms"]["N-questions"].update(value=35)),
     lambda o: o["norms"]["N-questions"].update(value=30), "no new raise row"),
    ("against: looser than before WITH a new raise row is green",
     lambda d: (d["raises"].append(dict(RAISE, **{"from": 40, "to": 45})), d["norms"]["N-questions"].update(value=45)),
     lambda o: o["norms"]["N-questions"].update(value=30), None),
    ("against: an earlier raise row removed", lambda d: None, lambda o: o["raises"].append(dict(RAISE)), "may only be appended"),
    ("against: an unset norm may be set once", lambda d: d["norms"]["N-brief"].update(value=12, initial=12), lambda o: None, None),
]


def sb_ratchet_case(tmp: Path, case) -> None:
    _name, edit, old_edit, want = case
    scoreboard = _sb()
    new, old = _norms(), _norms()
    edit(new)
    if old_edit is not None:
        old_edit(old)
    problems = scoreboard.check_norms(new, old if old_edit is not None else None)
    if want is None:
        assert problems == [], problems
    else:
        assert any(want in p for p in problems), problems


def _doc(run_class="live", arm="factory", truth="v1", **rows):
    return {"run": {"run_class": run_class, "arm": arm, "truth_version": truth},
            "rows": {k: (v if isinstance(v, dict) else _m(v)) for k, v in rows.items()}}


def _rg(low, high):
    return {"state": "range", "value": {"low": low, "high": high, "note": "n"}}


SB_COMPARE_CASES = [
    # (case id, now doc, previous doc or None, row, expected entry fields or the not_comparable words)
    ("a first run: previous none, no worse flag at all", _doc(Q1=5), None, "Q1", "first"),
    ("a lower-is-better row that rose is worse", _doc(Q1=5), _doc(Q1=3), "Q1", {"was": 3, "now": 5, "worse": True}),
    ("the same value is not worse", _doc(Q1=3), _doc(Q1=3), "Q1", {"worse": False}),
    ("a row that fell is not worse", _doc(Q1=2), _doc(Q1=3), "Q1", {"worse": False}),
    ("a higher-is-better row that fell is worse", _doc(QA1=1), _doc(QA1=2), "QA1", {"worse": True}),
    ("unknown now, measured before: undecided, never a pass", _doc(Q1=_U), _doc(Q1=3), "Q1", {"worse": None, "now": "unknown"}),
    ("measured now, unknown before: undecided", _doc(Q1=3), _doc(Q1=_U), "Q1", {"worse": None, "was": "unknown"}),
    ("a row with no declared direction is never worse", _doc(Q2=9), _doc(Q2=1), "Q2", {"worse": None}),
    ("a dry file against a live file: not comparable (K7)", _doc(run_class="dry", Q1=9), _doc(Q1=1), None, "run_class live vs dry"),
    ("a live file against a dry file: not comparable (K7)", _doc(Q1=9), _doc(run_class="dry", Q1=1), None, "run_class dry vs live"),
    ("a mixed run is not comparable", _doc(run_class="mixed", Q1=9), _doc(Q1=1), None, "run_class live vs mixed"),
    ("an unknown run class is not comparable", _doc(run_class="unknown", Q1=9), _doc(Q1=1), None, "run_class live vs unknown"),
    ("another arm is not comparable", _doc(arm="free", Q1=9), _doc(Q1=1), None, "arm factory vs free"),
    ("a quality row across truth versions: not comparable (7.8)", _doc(truth="v2", QA1=2), _doc(truth="v1", QA1=1), "QA1", "truth v1 vs v2"),
    ("a time row across truth versions is still compared", _doc(truth="v2", Q1=5), _doc(truth="v1", Q1=3), "Q1", {"worse": True}),
    ("money ranges that do not overlap: worse", _doc(X1=_rg(5.0, 6.0)), _doc(X1=_rg(2.0, 3.0)), "X1", {"worse": True, "outcome": "worse"}),
    ("money ranges that overlap: undecided", _doc(X1=_rg(2.5, 6.0)), _doc(X1=_rg(2.0, 3.0)), "X1", {"worse": None, "outcome": "not decided: range"}),
    # B2: the three pairs of the critic's control run; `compare` and `compare --release` read them with ONE judge (lower is better)
    ("B2 pair: was 10, now 10..12: not decided, not 'not worse'", _doc(Q1=_rg(10, 12)), _doc(Q1=10), "Q1", {"worse": None, "outcome": "not decided: range"}),
    ("B2 pair: was 8..12, now 8..14: not decided", _doc(Q1=_rg(8, 14)), _doc(Q1=_rg(8, 12)), "Q1", {"worse": None, "outcome": "not decided: range"}),
    ("B2 pair: was 10, now 7..10: not worse (the whole range is at or below)", _doc(Q1=_rg(7, 10)), _doc(Q1=10), "Q1", {"worse": False, "outcome": "not_worse"}),
    ("one_source now above the previous scalar: worse, compared as a value", _doc(X1={"state": "one_source", "value": {"value": 5.0, "note": "one source"}}),
     _doc(X1=3.0), "X1", {"worse": True, "outcome": "worse"}),
    ("at_least now above the previous high end: worse", _doc(X1={"state": "at_least", "value": {"at_least": 5.0, "note": "n"}}), _doc(X1=3.0), "X1",
     {"worse": True, "outcome": "worse"}),
    ("at_least now below the previous value: not decided, never 'not worse'", _doc(X1={"state": "at_least", "value": {"at_least": 2.0, "note": "n"}}),
     _doc(X1=3.0), "X1", {"worse": None, "outcome": "not decided: lower bound"}),
    ("an at_least PREVIOUS value is not a price to compare with: unknown", _doc(X1=3.0), _doc(X1={"state": "at_least", "value": {"at_least": 2.0}}), "X1",
     {"worse": None, "outcome": "unknown"}),
]


def sb_compare_case(tmp: Path, case) -> None:
    _name, now, previous, row, want = case
    scoreboard = _sb()
    comp = scoreboard.build_compare(now, previous, "was.yaml" if previous else None, None, scoreboard.load_rows())
    if want == "first":
        assert comp["previous"] == "none" and "rows" not in comp and "not_comparable" not in comp, comp
    elif row is None:
        assert comp.get("not_comparable") == want and "rows" not in comp, comp
    elif isinstance(want, str):
        assert comp["rows"][row] == {"not_comparable": want}, comp["rows"][row]
    else:
        assert all(comp["rows"][row].get(k) == v for k, v in want.items()), comp["rows"][row]
        if want.get("worse") is None:
            assert "why" in comp["rows"][row]


def sb_put(folder: Path, stamp: str, arm: str, run_class: str) -> Path:
    import yaml
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{stamp}-1.0.0-{arm}.yaml"
    path.write_text(yaml.safe_dump({"schema": "scoreboard/1", "run": {"arm": arm, "run_class": run_class}, "rows": {}}), encoding="utf-8")
    return path


SB_PREVIOUS_CASES = [
    # (case id, files already in the folder as (stamp, arm, class), the file being compared, the expected previous or None)
    ("the newest EARLIER live file of the same arm", [("20261101-1000", "factory", "live"), ("20261102-1000", "factory", "live")], ("20261103-1000", "factory"),
     "20261102-1000-1.0.0-factory.yaml"),
    ("a later file is not previous", [("20261105-1000", "factory", "live")], ("20261103-1000", "factory"), None),
    ("another arm is not previous (7.7)", [("20261101-1000", "free", "live")], ("20261103-1000", "factory"), None),
    ("a dry file is not previous of a live one", [("20261101-1000", "factory", "dry"), ("20261031-1000", "factory", "live")], ("20261103-1000", "factory"),
     "20261031-1000-1.0.0-factory.yaml"),
    ("only a dry file earlier: none", [("20261101-1000", "factory", "dry")], ("20261103-1000", "factory"), None),
    ("no earlier file at all", [], ("20261103-1000", "factory"), None),
]


def sb_previous_case(tmp: Path, case) -> None:
    _name, files, current, want = case
    folder = tmp / "folder"
    folder.mkdir()
    for stamp, arm, run_class in files:
        sb_put(folder, stamp, arm, run_class)
    found, _doc_, notes = _sb().previous_of(folder / f"{current[0]}-1.0.0-{current[1]}.yaml")
    assert (found.name if found else None) == want and notes == [], (found, notes)


def sb_assemble_case(tmp: Path, case) -> None:
    """The edges of 7.2-7.7 and the refusals, each through the command line."""
    name = case[0]
    scoreboard = _sb()
    out = tmp / "out"
    if name == "an empty run folder is refused naming the folder":
        empty = tmp / "empty-run"
        empty.mkdir()
        code, _p, err = sb_assemble(empty, out)
        assert code == 2 and str(empty) in err and "is empty" in err and sb_files(out) == [], err
    elif name == "a run folder that does not exist is refused naming it":
        code, _p, err = sb_assemble(tmp / "nowhere", out)
        assert code == 2 and str(tmp / "nowhere") in err and sb_files(out) == [], err
    elif name == "an absent rows file is a red line naming it":
        code, _p, err = sb_assemble(sb_run(tmp), out, "--rows", tmp / "no-rows.json")
        assert code == 2 and "RED" in err and str(tmp / "no-rows.json") in err and sb_files(out) == [], err
    elif name == "a norms file that is not JSON is a red line naming it":
        (tmp / "norms.json").write_text("{not json", encoding="utf-8")
        code, _p, err = sb_assemble(sb_run(tmp), out, "--norms", tmp / "norms.json")
        assert code == 2 and str(tmp / "norms.json") in err and sb_files(out) == [], err
    elif name == "a norms file of non-UTF-8 bytes is a red line naming it":
        (tmp / "norms.json").write_bytes(b"\xff\xfe{}")
        code, _p, err = sb_assemble(sb_run(tmp), out, "--norms", tmp / "norms.json")
        assert code == 2 and "not UTF-8" in err and str(tmp / "norms.json") in err, err
    elif name == "compare reads no scoreboard from an unreadable norms file":
        code, _p, _e = sb_assemble(sb_run(tmp), out)
        (tmp / "norms.json").write_text("[]", encoding="utf-8")
        code, printed, err = sb_cli("compare", sb_files(out)[0], "--norms", tmp / "norms.json")
        assert code == 2 and printed == "" and str(tmp / "norms.json") in err, (printed, err)
    elif name == "a stand name with a path separator is refused":
        code, _p, err = sb_cli("assemble", "--task-root", sb_run(tmp), "--stand", "../x", "--story", "s", "--arm", "factory", "--version", "1", "--out-root", out)
        assert code == 2 and "not a plain name" in err and not (tmp / "x").exists(), err
    elif name == "the same input gives the same bytes":
        task = sb_run(tmp)
        assert sb_assemble(task, out)[0] == 0
        first = sb_files(out)[0].read_bytes()
        assert sb_assemble(task, out)[0] == 0
        assert sb_files(out)[0].read_bytes() == first
    elif name == "an old record: a counter it cannot know stays unknown in the row and the norm (7.6)":
        code, _p, err = sb_assemble(sb_run(tmp, process=False), out)
        doc = sb_yaml(sb_files(out)[0])
        assert code == 0 and doc["rows"]["Q1"]["state"] == "unknown" and doc["rows"]["Q1"]["value"] is None, doc["rows"]["Q1"]
        assert doc["rows"]["T6"]["value"] is None and doc["norms"]["N-questions"]["verdict"] == "unknown", doc["norms"]["N-questions"]
        assert doc["run"]["run_class"] == "unknown" and all(n["verdict"] == "unknown" for n in doc["norms"].values())
    elif name == "a counter key the run cannot give reads unknown in rows G1us and U1u, never 0":
        task = sb_run(tmp)
        runs = task / "state" / "driver-runs.jsonl"
        stripped = [{k: v for k, v in json.loads(line).items() if k not in ("checks", "checks_n", "resume_kind")} for line in runs.read_text(encoding="utf-8").splitlines()]
        runs.write_text("\n".join(json.dumps(r) for r in stripped) + "\n", encoding="utf-8")
        code, _p, err = sb_assemble(task, out)
        doc = sb_yaml(sb_files(out)[0])
        assert code == 0, err
        assert doc["rows"]["G1us"]["state"] == "unknown" and doc["rows"]["G1us"]["value"] is None, doc["rows"]["G1us"]
        assert doc["rows"]["U1u"]["state"] == "measured" and doc["rows"]["U1u"]["value"] == 0, doc["rows"]["U1u"]
    elif name == "a dry run: stub-role rows are n/a and no norm is judged (7.9)":
        doc = (sb_assemble(sb_run(tmp, run_class="dry"), out), sb_yaml(sb_files(out)[0]))[1]
        assert doc["run"]["run_class"] == "dry" and doc["rows"]["T9"]["state"] == "n/a" and doc["rows"]["R1r"]["state"] == "n/a"
        assert all(n["verdict"] == "unknown" and "K7" in n["why"] for n in doc["norms"].values())
    elif name == "a dry file next to a live file: compare says not comparable, no worse flag, no finding":
        assert sb_assemble(sb_run(tmp, "live", questions=1), out)[0] == 0
        assert sb_assemble(sb_run(tmp, "dry", start="2026-11-03T10:00:00+00:00", run_class="dry", questions=9), out)[0] == 0
        dry = [f for f in sb_files(out) if f.name.startswith("20261103")][0]
        code, printed, err = sb_cli("compare", dry, "--findings", "--findings-root", tmp / "piles")
        assert code == 0 and "not comparable: run_class live vs dry" in printed and "worse" not in printed.replace("not comparable", ""), printed
        assert not (tmp / "piles").exists(), "a finding was drafted for a non-comparable pair"
    elif name == "the owner's word passes a red norm and is recorded (P13)":
        code, printed, err = sb_assemble(sb_run(tmp, questions=41), out, "--pass", "N-questions", "owner", "14.11.2026")
        doc = sb_yaml(sb_files(out)[0])
        assert doc["norms"]["N-questions"]["verdict"] == "red" and doc["passes"] == [{"norm": "N-questions", "word": "owner", "date": "14.11.2026"}], doc
        code, printed, err = sb_cli("compare", sb_files(out)[0])
        assert "passed by the owner's word: owner, 14.11.2026" in printed and "release: warning -- red" not in printed, printed
    elif name == "a pass for a norm that does not exist is refused":
        code, _p, err = sb_assemble(sb_run(tmp), out, "--pass", "N-nope", "owner", "14.11.2026")
        assert code == 2 and "N-nope" in err and sb_files(out) == [], err
    elif name == "no run dir is touched: the run folder is read only":
        task = sb_run(tmp)
        before = sorted((str(p.relative_to(task)), p.read_bytes()) for p in task.rglob("*") if p.is_file())
        sb_assemble(task, out)
        assert before == sorted((str(p.relative_to(task)), p.read_bytes()) for p in task.rglob("*") if p.is_file())
    else:
        raise AssertionError("no such case: " + name)
    del scoreboard


SB_ASSEMBLE_CASES = [(n,) for n in (
    "an empty run folder is refused naming the folder", "a run folder that does not exist is refused naming it",
    "an absent rows file is a red line naming it", "a norms file that is not JSON is a red line naming it",
    "a norms file of non-UTF-8 bytes is a red line naming it", "compare reads no scoreboard from an unreadable norms file",
    "a stand name with a path separator is refused", "the same input gives the same bytes",
    "an old record: a counter it cannot know stays unknown in the row and the norm (7.6)",
    "a counter key the run cannot give reads unknown in rows G1us and U1u, never 0",
    "a dry run: stub-role rows are n/a and no norm is judged (7.9)",
    "a dry file next to a live file: compare says not comparable, no worse flag, no finding",
    "the owner's word passes a red norm and is recorded (P13)", "a pass for a norm that does not exist is refused",
    "no run dir is touched: the run folder is read only")]


def sb_cli_case(tmp: Path, case) -> None:
    name = case[0]
    out = tmp / "out"
    if name == "--help names assemble, compare and norms":
        code, printed, _e = sb_cli("--help")
        assert code == 0 and all(word in printed for word in ("assemble", "compare", "norms", "--findings", "--check")), printed
    elif name == "norms --check is green on the shipped file":
        code, printed, _e = sb_cli("norms", "--check")
        assert code == 0 and printed.strip().endswith("norms: green"), printed
    elif name == "norms --check exits 1 and names the norm when it loosened":
        doc = _norms()
        doc["norms"]["N-wall"]["value"] = 99
        (tmp / "n.json").write_text(json.dumps(_sb().legacy_to_v2(doc)), encoding="utf-8")
        code, printed, _e = sb_cli("norms", "--check", "--norms", tmp / "n.json")
        assert code == 1 and "N-wall" in printed and printed.strip().endswith("norms: red"), printed
    elif name == "compare names the previous file, the bar and 'can tighten' for a green norm":
        assert sb_assemble(sb_run(tmp, "a", questions=3), out)[0] == 0
        assert sb_assemble(sb_run(tmp, "b", start="2026-11-02T10:00:00+00:00", questions=2), out)[0] == 0
        newest = sb_files(out)[-1]
        code, printed, _e = sb_cli("compare", newest)
        assert code == 0 and "previous: 20261101-1000-9.9.9-factory.yaml" in printed and "bar: none" in printed, printed
        assert "Q1: was 3.0, now 2.0 questions -- not worse" in printed.replace("was 3,", "was 3.0,").replace("now 2 ", "now 2.0 ") or "Q1: was 3, now 2" in printed, printed
        assert "can tighten: N-questions 40 -> 2" in printed, printed
    elif name == "compare --findings writes ONE finding per worsened row, in the pile, quoting the row":
        assert sb_assemble(sb_run(tmp, "a", questions=1), out)[0] == 0
        assert sb_assemble(sb_run(tmp, "b", start="2026-11-02T10:00:00+00:00", questions=5), out)[0] == 0
        newest = sb_files(out)[-1]
        code, printed, _e = sb_cli("compare", newest, "--findings", "--findings-root", tmp / "piles")
        found = sorted((tmp / "piles").rglob("*.md"))
        assert code == 0 and [f.name for f in found] == ["20261102-scoreboard-q1-factory.md"] and found[0].parent == tmp / "piles" / "live-runs" / "findings", found
        text = found[0].read_text(encoding="utf-8")
        assert "Q1" in text and "было 1" in text and "стало 5" in text and "sha256" in text and "Решение владельца нужно: нет" in text, text
        assert "card row, pile live-runs" in printed
        again = [f.read_bytes() for f in found]
        sb_cli("compare", newest, "--findings", "--findings-root", tmp / "piles")
        assert [f.read_bytes() for f in sorted((tmp / "piles").rglob("*.md"))] == again, "the finding is not deterministic"
    elif name == "compare --findings on a first run writes nothing":
        assert sb_assemble(sb_run(tmp, "a", questions=1), out)[0] == 0
        code, printed, _e = sb_cli("compare", sb_files(out)[0], "--findings", "--findings-root", tmp / "piles")
        assert code == 0 and "previous: none" in printed and not (tmp / "piles").exists(), printed
    elif name == "the scoreboard file carries no absolute path of this machine (AR-4)":
        assert sb_assemble(sb_run(tmp), out)[0] == 0
        text = sb_files(out)[0].read_text(encoding="utf-8")
        assert str(tmp) not in text and re.search(r"[A-Za-z]:\\", text) is None, text[:400]
    else:
        raise AssertionError("no such case: " + name)


SB_CLI_CASES = [(n,) for n in (
    "--help names assemble, compare and norms", "norms --check is green on the shipped file",
    "norms --check exits 1 and names the norm when it loosened",
    "compare names the previous file, the bar and 'can tighten' for a green norm",
    "compare --findings writes ONE finding per worsened row, in the pile, quoting the row",
    "compare --findings on a first run writes nothing",
    "the scoreboard file carries no absolute path of this machine (AR-4)")]

# --- P1-v N7: the free arm's bar price (spec 3 item 2) and the release check (K3, F7, OQ2) ---------------------------------------------
# Catalogue control (references/model-rates.json, per 1M tokens): claude-sonnet-5-5 input 2, output 10, cache_read 0.1, cache_write_5m 2.5.
# Session A, one request, hand-priced: 1,000,000 in x 2 + 100,000 out x 10 + 2,000,000 read x 0.1 + 400,000 write x 2.5 = 4,200,000 / 1e6 = 4.2 usd.
# Session B, one request: 500,000 in x 2 + 50,000 out x 10 = 1,500,000 / 1e6 = 1.5 usd. A resume is A + B = 5.7 usd. The host's figure is 6.1234.
BAR_MODEL = "claude-sonnet-5-5"
BAR_A, BAR_B, BAR_SUM, BAR_HOST = 4.2, 1.5, 5.7, 6.1234


def _sbb():
    import scoreboard_bar
    return scoreboard_bar


def bar_transcript(path: Path, requests, model=BAR_MODEL) -> Path:
    """A `free-N` session transcript: one assistant line per request (message id, model, usage); `requests` = [(id, usage dict)]."""
    path.write_text("\n".join(json.dumps({"type": "assistant", "uuid": f"u-{mid}", "timestamp": "2026-11-01T10:00:00Z",
                                          "message": {"id": mid, "model": model, "usage": usage, "content": []}}) for mid, usage in requests) + "\n",
                    encoding="utf-8")
    return path


BAR_USAGE_A = {"input_tokens": 1000000, "output_tokens": 100000, "cache_read_input_tokens": 2000000,
               "cache_creation": {"ephemeral_5m_input_tokens": 400000, "ephemeral_1h_input_tokens": 0}}
BAR_USAGE_B = {"input_tokens": 500000, "output_tokens": 50000}


def bar_result(path: Path, total=BAR_HOST) -> Path:
    """A free-N.log: a line of text, then the host's result object with its own total_cost_usd."""
    path.write_text("starting the free agent\n" + json.dumps({"type": "result", "num_turns": 7, "total_cost_usd": total}) + "\n", encoding="utf-8")
    return path


def sb_bar_case(tmp: Path, case) -> None:
    name, bar = case[0], _sbb()
    a = bar_transcript(tmp / "a.jsonl", [("m1", BAR_USAGE_A)])
    b = bar_transcript(tmp / "b.jsonl", [("m2", BAR_USAGE_B)])
    log = bar_result(tmp / "free-1.log")
    if name == "one session: the re-priced value equals the hand re-pricing of the same row by the catalogue, 4.2 usd":
        got = bar.bar_price([a], None)
        assert (got["state"], got["value"]) == ("measured", BAR_A), got
    elif name == "two sessions (a resume): the sum of the re-priced sessions, 5.7 usd":
        got = bar.bar_price([a, b], None)
        assert (got["state"], got["value"]) == ("measured", BAR_SUM), got
    elif name == "a transcript that cannot be read (not UTF-8): unknown, not 0 and not the host's total_cost_usd":
        (tmp / "bad.jsonl").write_bytes(b"\xff\xfe\x00 not a transcript\n")
        got = bar.bar_price([tmp / "bad.jsonl"], None, [log])
        assert got["state"] == "unknown" and got["value"] is None and "not recomputed" in got["why"], got
        assert got["value"] != BAR_HOST and got["host_total_usd"] == BAR_HOST, got
    elif name == "the host's total_cost_usd 6.1234 is printed next to the value 4.2 and is not part of it":
        got = bar.bar_price([a], None, [log])
        line = bar.price_line(got)
        assert got["value"] == BAR_A and got["host_total_usd"] == BAR_HOST, got
        assert f"bar price: {BAR_A} usd" in line and f"host total_cost_usd: {BAR_HOST}" in line and "not part of the value" in line, line
    elif name == "a missing transcript: unknown, never a bar of zeros":
        got = bar.bar_price([tmp / "gone.jsonl"], None)
        assert got["state"] == "unknown" and got["value"] is None and "gone.jsonl" in got["why"] and str(tmp) not in got["why"], got
    elif name == "an empty transcript list: unknown":
        for empty in ([], (), None):
            got = bar.bar_price(empty, None, [log])
            assert got["state"] == "unknown" and got["value"] is None and got["host_total_usd"] == BAR_HOST, got
    elif name == "one of two sessions missing: unknown, not the other session's sum":
        got = bar.bar_price([a, tmp / "gone.jsonl"], None)
        assert got["state"] == "unknown" and got["value"] is None, got
    elif name == "a model the catalogue does not know: unknown, the unpriced request is counted":
        got = bar.bar_price([bar_transcript(tmp / "x.jsonl", [("m1", BAR_USAGE_A)], model="claude-unheard-9")], None)
        assert got["state"] == "unknown" and got["value"] is None and got["unpriced"] == 1, got
    elif name == "a transcript with no usage block: unknown":
        (tmp / "n.jsonl").write_text(json.dumps({"type": "user", "message": {"content": "hi"}}) + "\nnot json at all\n", encoding="utf-8")
        got = bar.bar_price([tmp / "n.jsonl"], None)
        assert got["state"] == "unknown" and got["value"] is None, got
    elif name == "the same message id twice in one transcript is one request":
        got = bar.bar_price([bar_transcript(tmp / "d.jsonl", [("m1", BAR_USAGE_A), ("m1", BAR_USAGE_A)])], None)
        assert got["value"] == BAR_A, got
    elif name == "cfg rate_overrides price the model before the catalogue (B1-E6): every rate 1 gives 3.5 usd":
        rates = {k: 1 for k in ("input", "output", "cache_read", "cache_write_5m", "cache_write_1h")}
        got = bar.bar_price([a], {"rate_overrides": [{"model_id": BAR_MODEL, "rates": rates}]})
        assert got["value"] == 3.5, got
    elif name == "a result file with no total_cost_usd: the host figure is not given, the value is untouched":
        (tmp / "free-2.log").write_text("died\n", encoding="utf-8")
        got = bar.bar_price([a], None, [tmp / "free-2.log"])
        assert got["value"] == BAR_A and got["host_total_usd"] is None and "host total_cost_usd: not given" in bar.price_line(got), got
    elif name == "the line of an unknown value names the reason and still prints the host figure":
        line = bar.price_line(bar.bar_price([tmp / "gone.jsonl"], None, [log]))
        assert line.startswith("bar price: unknown: ") and f"host total_cost_usd: {BAR_HOST}" in line and "bar price: 0" not in line, line
    elif name == "price command line: two transcripts and a result file print the sum and the host figure":
        code = bar.main(["price", "--transcript", str(a), "--transcript", str(b), "--result", str(log)])
        assert code == 0
    elif name == "F5: a long-context request (terra, 300,000 input) is valued by the package's value_usage, 1.218 usd, not the short rate 0.612":
        # hand: 300,000 x 4 / 1e6 + 1,000 x 18 / 1e6 = 1.2 + 0.018 (long band, threshold 272,000); the short rates give 0.6 + 0.012 = 0.612
        long_t = bar_transcript(tmp / "long.jsonl", [("m1", {"input_tokens": 300000, "output_tokens": 1000})], model="gpt-5.6-terra")
        got = bar.bar_price([long_t], None)
        assert (got["state"], got["value"]) == ("measured", 1.218), got
    elif name == "F5: a request just under the long-context threshold is valued at the short rates":
        short_t = bar_transcript(tmp / "short.jsonl", [("m1", {"input_tokens": 272000, "output_tokens": 1000})], model="gpt-5.6-terra")
        assert bar.bar_price([short_t], None)["value"] == 0.556, bar.bar_price([short_t], None)       # 272,000 x 2 / 1e6 + 1,000 x 12 / 1e6
    elif name == "F5: a request dated before the catalogue window of its model is unpriced, not valued at a later entry":
        old = tmp / "old.jsonl"
        old.write_text(json.dumps({"type": "assistant", "timestamp": "2026-01-01T10:00:00Z", "message": {
            "id": "m1", "model": "gpt-5.6-terra", "usage": {"input_tokens": 1000}, "content": []}}) + "\n", encoding="utf-8")
        got = bar.bar_price([old], None)
        assert got["state"] == "unknown" and got["value"] is None and got["unpriced"] == 1, got
    elif name == "F7: the line prints the gap host - re-priced when both are known, and no gap when one is unknown":
        line = bar.price_line(bar.bar_price([a], None, [log]))
        assert f"gap: {round(BAR_HOST - BAR_A, 4)} (host - re-priced)" in line, line
        assert "gap:" not in bar.price_line(bar.bar_price([a], None)), "a gap was printed with no host figure"
        assert "gap:" not in bar.price_line(bar.bar_price([tmp / "gone.jsonl"], None, [log]))
    else:
        raise AssertionError("no such case: " + name)


SB_BAR_CASES = [(n,) for n in (
    "one session: the re-priced value equals the hand re-pricing of the same row by the catalogue, 4.2 usd",
    "two sessions (a resume): the sum of the re-priced sessions, 5.7 usd",
    "a transcript that cannot be read (not UTF-8): unknown, not 0 and not the host's total_cost_usd",
    "the host's total_cost_usd 6.1234 is printed next to the value 4.2 and is not part of it",
    "a missing transcript: unknown, never a bar of zeros", "an empty transcript list: unknown",
    "one of two sessions missing: unknown, not the other session's sum",
    "a model the catalogue does not know: unknown, the unpriced request is counted", "a transcript with no usage block: unknown",
    "the same message id twice in one transcript is one request",
    "cfg rate_overrides price the model before the catalogue (B1-E6): every rate 1 gives 3.5 usd",
    "a result file with no total_cost_usd: the host figure is not given, the value is untouched",
    "the line of an unknown value names the reason and still prints the host figure",
    "price command line: two transcripts and a result file print the sum and the host figure",
    "F5: a long-context request (terra, 300,000 input) is valued by the package's value_usage, 1.218 usd, not the short rate 0.612",
    "F5: a request just under the long-context threshold is valued at the short rates",
    "F5: a request dated before the catalogue window of its model is unpriced, not valued at a later entry",
    "F7: the line prints the gap host - re-priced when both are known, and no gap when one is unknown")]

# --- P1-v N9: the writer of the free arm's bar file (`scoreboard_bar.py bar`; spec 20261114-p1v-n8-carriers-draft.md 7(a)) -----------------
# Hand figures: transcript 1 = events 10:00:00 and 10:05:00 (T1 300 s), one request of BAR_USAGE_B (1.5 usd), two tool calls (Read, Bash),
# the Bash one refused (is_error) with its result 300 s after the call (T10 300 s). Transcript 2 = 10:10:00 .. 10:20:00, BAR_USAGE_A (4.2 usd).
# Two transcripts: T1 = 10:00 .. 10:20 = 1200 s, X1 = 1.5 + 4.2 = 5.7 usd, T10 = 300 + 600 s.
def bf_transcript(path: Path, start="10:00:00", end="10:05:00", usage=BAR_USAGE_B, mid="m1", model=BAR_MODEL, stamps=True) -> Path:
    ts = (lambda t: {"timestamp": f"2026-11-01T{t}Z"}) if stamps else (lambda t: {})
    rows = [{"type": "assistant", "uuid": f"u-{mid}", **ts(start), "message": {"id": mid, "model": model, "usage": usage, "content": [
                {"type": "tool_use", "id": f"{mid}-r", "name": "Read", "input": {"file_path": "x.txt"}},
                {"type": "tool_use", "id": f"{mid}-b", "name": "Bash", "input": {"command": "ls"}}]}},
            {"type": "user", "uuid": f"r-{mid}", **ts(end), "message": {"content": [
                {"type": "tool_result", "tool_use_id": f"{mid}-r", "content": "ok"},
                {"type": "tool_result", "tool_use_id": f"{mid}-b", "content": "denied", "is_error": True}]}}]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


def bf_cli(*argv):
    """(code, stdout, stderr) of `scoreboard_bar.main(argv)`."""
    import io
    import contextlib
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = _sbb().main([str(a) for a in argv])
        except SystemExit as stop:
            code = stop.code
    return code, out.getvalue(), err.getvalue()


def bf_bar(tmp: Path, *extra, model=BAR_MODEL, stand="mybooks", story="add-to-cart"):
    """The command line `bar` into tmp/out; returns (code, stdout, stderr)."""
    return bf_cli("bar", "--stand", stand, "--story", story, "--model", model, "--out-root", tmp / "out", *extra)


def bf_file(tmp: Path, model=BAR_MODEL) -> Path:
    return tmp / "out" / "mybooks" / "add-to-cart" / f"bar-{model}.yaml"


def bf_written(tmp: Path) -> list:
    return sorted(str(p) for p in (tmp / "out").rglob("*") if p.is_file()) if (tmp / "out").exists() else []


def bf_judgment_pair(tmp: Path, free_found=(2,)) -> tuple:
    """(truth, judgment): arm X is the free arm (key), it found the cards in `free_found`; the verdict vocabulary is declared by `sb_rows_file`."""
    rows = [{"card": i, "arm": arm, "verdict": "found" if (arm == "X" and i in free_found) else "missed", "unsure": False}
            for arm in ("X", "Y") for i in (1, 2, 3)]
    return sb_truth(tmp / "truth.yaml"), sb_judgment(tmp / "judgment.yaml", rows)


SB_BAR_FILE_CASES = [(n,) for n in (
    "one session: X1 1.5 re-priced, T1 300 s, T10 300 s, turns 7, tool calls by name, the host figure beside and not in X1, no machine path",
    "two transcripts are summed: X1 5.7, T1 from the first event of the earliest to the last of the latest 1200 s, T10 900 s",
    "a transcript that is absent: X1 and T1 and T10 unknown with the reason, the file is still written, the model is not verified",
    "an empty transcript: X1 and T1 unknown, the file is still written",
    "a transcript that cannot be read (not UTF-8): unknown, never 0, the file is still written",
    "one of two transcripts absent: unknown, not the other transcript's figures",
    "no transcript given at all: unknown rows, the file says the model was not verified",
    "a result with no total_cost_usd: the host figure is unknown, X1 and turns are untouched",
    "a result with no num_turns, or a result file that is absent: turns unknown, X1 untouched",
    "no readable timestamp: T1 unknown, never 0, X1 still measured",
    "the model id is not a message.model of the transcript: refused naming both, nothing written",
    "--model with a slash, a backslash, .. or empty: refused as not a plain name, nothing written",
    "--stand or --story with a slash, .. or empty: refused, nothing written",
    "--truth without --judgment, or the reverse: refused naming the missing one, nothing written",
    "a judgment that K1 refuses: its text passed through, nothing written",
    "a judgment of the free arm: truth_version and the QA rows come through read_judgment and quality_rows",
    "no judgment: the QA rows are unknown and truth_version is null",
    "every row the free arm has no part for is n/a with the reason, never 0",
    "an existing bar file is replaced by the same write, the line says replaced, no second file",
    "the written file is read back by assemble --bar and compare --release (_bars) without refusal")]


def sb_bar_file_case(tmp: Path, case) -> None:
    name = case[0]
    a = bf_transcript(tmp / "a.jsonl")
    b = bf_transcript(tmp / "b.jsonl", "10:10:00", "10:20:00", BAR_USAGE_A, "m2")
    log = bar_result(tmp / "free-1.log")
    rows_doc = _sb().load_rows()

    def written(*extra, **kw):
        code, printed, err = bf_bar(tmp, *extra, **kw)
        assert code == 0, (code, printed, err)
        return sb_yaml(bf_file(tmp, kw.get("model", BAR_MODEL)))

    def refused(words, *extra, **kw):
        code, printed, err = bf_bar(tmp, *extra, **kw)
        assert code == 2 and "RED:" in err and words in err, (code, printed, err[:300])
        assert bf_written(tmp) == [], ("a refusal wrote", bf_written(tmp))

    if name.startswith("one session"):
        doc = written("--transcript", a, "--result", log)
        assert doc["schema"] == "scoreboard/1" and doc["run"]["arm"] == "free" and doc["run"]["run_class"] == "live", doc["run"]
        assert doc["run"]["models"] == [BAR_MODEL] and doc["run"]["model_verified"] is True, doc["run"]
        r = doc["rows"]
        assert (r["X1"]["state"], r["X1"]["value"]) == ("measured", BAR_B), r["X1"]
        assert (r["T1"]["state"], r["T1"]["value"]) == ("measured", 300.0), r["T1"]
        assert (r["T10"]["state"], r["T10"]["value"]) == ("measured", 300.0), r["T10"]
        free = doc["free"]
        assert free["turns"]["value"] == 7 and free["tool_calls"]["by_name"] == {"Bash": 1, "Read": 1}, free
        assert free["refused_calls"]["n"] == 1 and free["host_total_usd"] == BAR_HOST, free
        assert r["X1"]["value"] != BAR_HOST
        assert str(tmp) not in bf_file(tmp).read_text(encoding="utf-8"), "a machine path was written (AR-4)"
    elif name.startswith("two transcripts"):
        doc = written("--transcript", a, "--transcript", b)
        r = doc["rows"]
        assert (r["X1"]["state"], r["X1"]["value"]) == ("measured", BAR_SUM), r["X1"]
        assert r["T1"]["value"] == 1200.0 and r["T10"]["value"] == 900.0, (r["T1"], r["T10"])
        assert doc["free"]["tool_calls"]["by_name"] == {"Bash": 2, "Read": 2}, doc["free"]
    elif name.startswith("a transcript that is absent"):
        doc = written("--transcript", tmp / "gone.jsonl")
        r = doc["rows"]
        for rid in ("X1", "T1", "T10"):
            assert r[rid]["state"] == "unknown" and r[rid]["value"] is None and "absent" in r[rid]["why"], (rid, r[rid])
        assert doc["run"]["model_verified"] is False and "not verified" in r["X1"]["why"], doc["run"]
        assert doc["free"]["tool_calls"]["state"] == "unknown" and doc["free"]["refused_calls"]["n"] is None
    elif name.startswith("an empty transcript"):
        (tmp / "empty.jsonl").write_text("", encoding="utf-8")
        r = written("--transcript", tmp / "empty.jsonl")["rows"]
        assert r["X1"]["state"] == "unknown" and r["T1"]["state"] == "unknown" and r["T1"]["value"] is None, r
    elif name.startswith("a transcript that cannot be read"):
        (tmp / "bad.jsonl").write_bytes(b"\xff\xfe\x00 not a transcript\n")
        r = written("--transcript", tmp / "bad.jsonl", "--result", log)["rows"]
        assert r["X1"]["state"] == "unknown" and r["X1"]["value"] is None and r["T10"]["value"] is None, r
    elif name.startswith("one of two transcripts absent"):
        doc = written("--transcript", a, "--transcript", tmp / "gone.jsonl")
        r = doc["rows"]
        assert r["X1"]["state"] == "unknown" and r["T1"]["state"] == "unknown" and r["T10"]["state"] == "unknown", r
        assert doc["free"]["tool_calls"]["by_name"] is None, doc["free"]
    elif name.startswith("no transcript given"):
        doc = written()
        assert doc["run"]["model_verified"] is False and "not verified" in doc["run"]["model_note"], doc["run"]
        assert doc["rows"]["X1"]["state"] == "unknown" and "not verified" in doc["rows"]["X1"]["why"], doc["rows"]["X1"]
    elif name.startswith("a result with no total_cost_usd"):
        (tmp / "free-2.log").write_text(json.dumps({"type": "result", "num_turns": 4}) + "\n", encoding="utf-8")
        doc = written("--transcript", a, "--result", tmp / "free-2.log")
        assert doc["free"]["host_total_usd"] == "unknown" and doc["free"]["turns"]["value"] == 4, doc["free"]
        assert doc["rows"]["X1"]["value"] == BAR_B, doc["rows"]["X1"]
    elif name.startswith("a result with no num_turns"):
        (tmp / "free-2.log").write_text(json.dumps({"type": "result", "total_cost_usd": 2.0}) + "\n", encoding="utf-8")
        for result in (tmp / "free-2.log", tmp / "no-such.log"):
            doc = written("--transcript", a, "--result", result)
            assert doc["free"]["turns"]["state"] == "unknown" and doc["free"]["turns"]["value"] is None, doc["free"]
            assert doc["rows"]["X1"]["value"] == BAR_B, doc["rows"]["X1"]
    elif name.startswith("no readable timestamp"):
        bf_transcript(tmp / "nots.jsonl", stamps=False)
        r = written("--transcript", tmp / "nots.jsonl")["rows"]
        assert r["T1"]["state"] == "unknown" and r["T1"]["value"] is None and "timestamp" in r["T1"]["why"], r["T1"]
        assert r["X1"]["state"] == "measured", r["X1"]
    elif name.startswith("the model id is not"):
        refused("claude-opus-5", "--transcript", a, model="claude-opus-5")
        code, _o, err = bf_bar(tmp, "--transcript", a, model="claude-opus-5")
        assert "claude-opus-5" in err and BAR_MODEL in err, err
    elif name.startswith("--model with"):
        for bad in ("a/b", "a\\b", "..", "a..b", ""):
            refused("not a plain name", "--transcript", a, model=bad)
    elif name.startswith("--stand or --story"):
        for bad in ("a/b", "..", ""):
            refused("not a plain name", "--transcript", a, stand=bad)
            refused("not a plain name", "--transcript", a, story=bad)
    elif name.startswith("--truth without"):
        truth, judgment = bf_judgment_pair(tmp)
        refused("--judgment is missing", "--transcript", a, "--truth", truth)
        refused("--truth is missing", "--transcript", a, "--judgment", judgment)
    elif name.startswith("a judgment that K1 refuses"):
        truth, _j = bf_judgment_pair(tmp)
        judgment = sb_judgment(tmp / "bad-judgment.yaml", sb_good_rows()[:-1] + [{"card": 9, "arm": "X", "verdict": "found"}])
        refused("card 9 is not in truth version v1", "--transcript", a, "--truth", truth, "--judgment", judgment)
    elif name.startswith("a judgment of the free arm"):
        truth, judgment = bf_judgment_pair(tmp)
        path, text, _notes = _sbb().bar_doc("mybooks", "add-to-cart", BAR_MODEL, [a], [], None, truth, judgment, None, sb_rows_file(tmp), tmp / "out")
        doc = _sb().yaml.safe_load(text)
        assert doc["run"]["truth_version"] == "v1", doc["run"]
        sb = _sb()
        want = sb.quality_rows(sb.load_rows(sb_rows_file(tmp)), sb.read_judgment(judgment, truth, "free", {"found": "found", "missed": "missed"}), "")
        assert doc["rows"]["QA1"]["state"] == "measured" and doc["rows"]["QA1"]["value"] == want["QA1"]["value"] == 1, (doc["rows"]["QA1"], want)
        assert path == bf_file(tmp), path
    elif name.startswith("no judgment"):
        doc = written("--transcript", a)
        assert doc["run"]["truth_version"] is None and doc["rows"]["QA1"]["state"] == "unknown" and doc["rows"]["QA1"]["value"] is None, doc["rows"]["QA1"]
    elif name.startswith("every row the free arm"):
        doc = written("--transcript", a)
        assert list(doc["rows"]) == list(rows_doc["rows"]), "a row of rows.json is missing from the bar file"
        own = {"X1", "T1", "T10"} | {rid for rid, s in rows_doc["rows"].items() if "quality" in s}
        for rid, row in doc["rows"].items():
            if rid not in own:
                assert row == {"name": rows_doc["rows"][rid]["name"], "value": None, "unit": rows_doc["rows"][rid]["unit"], "source": "none",
                               "state": "n/a", "why": "no such part in a free agent"}, (rid, row)
    elif name.startswith("an existing bar file"):
        code, first, _e = bf_bar(tmp, "--transcript", a)
        assert code == 0 and first.startswith("wrote "), first
        before = bf_file(tmp).read_text(encoding="utf-8")
        code, second, _e = bf_bar(tmp, "--transcript", a, "--transcript", b)
        assert code == 0 and second.startswith("replaced "), second
        assert bf_file(tmp).read_text(encoding="utf-8") != before and len(bf_written(tmp)) == 1, bf_written(tmp)
    elif name.startswith("the written file is read back"):
        written("--transcript", a, "--result", log)
        task = sb_run(tmp)
        code, printed, err = sb_cli("assemble", "--task-root", task, "--stand", "mybooks", "--story", "add-to-cart", "--arm", "factory",
                                    "--version", "9.9.9", "--bar", bf_file(tmp), "--out-root", tmp / "out2")
        assert code == 0 and "RED" not in err, (code, printed, err)
        notes = []
        found = _sbb()._bars(tmp / "out", "mybooks", "add-to-cart", notes)
        assert [(label, model) for label, model, _doc in found] == [(f"mybooks/add-to-cart/bar-{BAR_MODEL}.yaml", BAR_MODEL)] and notes == [], (found, notes)
        lines = _sbb().release_lines("9.9.9", _sb().load_norms(), tmp / "out")
        assert not any("note" in line for line in lines), lines
    else:
        raise AssertionError("no such case: " + name)


RC_VERSION, RC_PAIR = "1.1.0", "claude-sonnet-5-5/add-to-cart"
RC_OK = "release: ok -- Q1 " + RC_PAIR + " not worse"
RC_NEED = f"release: owner's word needed -- Q1 {RC_PAIR} was 1 (1.0.0) now 3 (1.1.0)"
RC_BAR = "mybooks/add-to-cart/bar-claude-opus-5.yaml"
RC_OQ2 = f"release: owner's word needed -- Q1 ratcheted, new bar {RC_BAR} is better than the factory"


def rc_norms(tmp: Path, rows=None, bar_changes=None, raw=None, schema="norms/2") -> Path:
    doc = {"schema": schema, "rows": rows if rows is not None else {}}
    if bar_changes is not None:
        doc["bar_changes"] = bar_changes
    path = tmp / "norms.json"
    path.write_text(raw if raw is not None else json.dumps(doc), encoding="utf-8")
    return path


def rc_pass(row="Q1", version=RC_VERSION, pair=RC_PAIR, word="owner, 14.11.2026"):
    return {row: {"worsened_passes": [{"version": version, "pair": pair, "word": word, "quote": "ship it"}]}}


def rc_run(tmp: Path, lines, norms, version=RC_VERSION):
    code, printed = _sbb().release_check(lines, version, norms)
    return code, "\n".join(printed)


def sb_release_case(tmp: Path, case) -> None:
    name, bar = case[0], _sbb()
    absent = tmp / "none.json"
    if name == "all lines ok: exit 0":
        code, text = rc_run(tmp, [RC_OK, RC_OK.replace("Q1", "Q2")], absent)
        assert code == 0 and text.endswith("release-check: ok"), text
    elif name == "one owner's-word-needed line with no worsened_passes: exit 1 with the list":
        code, text = rc_run(tmp, [RC_OK, RC_NEED], rc_norms(tmp, rows={"Q1": {}}))
        assert code == 1 and f"[Q1 {RC_PAIR} was 1" in text and "needed for 1 line(s)" in text, text
    elif name == "worsened_passes of the same row, version and pair: exit 0":
        code, text = rc_run(tmp, [RC_NEED], rc_norms(tmp, rows=rc_pass()))
        assert code == 0 and "owner's word recorded" in text and "owner, 14.11.2026" in text, text
    elif name == "worsened_passes of ANOTHER pair: exit 1":
        code, text = rc_run(tmp, [RC_NEED], rc_norms(tmp, rows=rc_pass(pair="claude-opus-5/add-to-cart")))
        assert code == 1, text
    elif name == "worsened_passes of the same pair for ANOTHER version: exit 1":
        code, text = rc_run(tmp, [RC_NEED], rc_norms(tmp, rows=rc_pass(version="1.0.9")))
        assert code == 1, text
    elif name == "worsened_passes with an empty word: exit 1":
        code, text = rc_run(tmp, [RC_NEED], rc_norms(tmp, rows=rc_pass(word="  ")))
        assert code == 1, text
    elif name == "worsened_passes of ANOTHER row, same version and pair: exit 1":
        code, text = rc_run(tmp, [RC_NEED], rc_norms(tmp, rows=rc_pass(row="Q2")))
        assert code == 1, text
    elif name == "two needed lines, only one has its pass: exit 1 naming the other":
        other = RC_NEED.replace("Q1", "Q2")
        code, text = rc_run(tmp, [RC_NEED, other], rc_norms(tmp, rows=rc_pass()))
        assert code == 1 and "[Q2 " in text and "[Q1 " not in text.split("release-check:")[1], text
    elif name == "a warning line alone: exit 0 and the warning is printed":
        warn = "release: warning -- Q3 red: 9 against norm 5"
        code, text = rc_run(tmp, [warn, RC_OK], absent)
        assert code == 0 and warn in text, text
    elif name == "'no previous release' alone: exit 0 (no ratcheted row exists)":
        code, text = rc_run(tmp, ["release: no previous release -- ratchet not judged"], absent)
        assert code == 0, text
    elif name == "no lines at all: a named error, never a pass":
        for empty in ([], ["", "  "]):
            try:
                bar.release_check(empty, RC_VERSION, absent)
            except _sb().Refusal as exc:
                assert "no `release:` line" in str(exc), exc
            else:
                raise AssertionError("an empty input passed")
    elif name == "a needed line whose shape cannot be matched stays open: exit 1":
        code, text = rc_run(tmp, ["release: owner's word needed -- something unexpected"], rc_norms(tmp, rows=rc_pass()))
        assert code == 1, text
    elif name == "OQ2: a new bar strictly better than the factory (lower is better) gives the line":
        assert bar.bar_better_line("Q1", RC_BAR, "lower", 10.0, 7.0) == RC_OQ2
        assert bar.bar_better_line("Q1", RC_BAR, "higher", 3, 4) == RC_OQ2
        assert bar.bar_better_line("X1", RC_BAR, "lower", {"low": 5.0, "high": 6.0}, 4.0) == RC_OQ2.replace("Q1", "X1")
    elif name == "OQ2: a new bar equal to or worse than the factory gives no line; an overlapping range is not decided and gives the line":
        assert bar.bar_better_line("Q1", RC_BAR, "lower", 10.0, 10.0) is None
        assert bar.bar_better_line("Q1", RC_BAR, "lower", 10.0, 12.0) is None
        assert bar.bar_better_line("X1", RC_BAR, "lower", {"low": 5.0, "high": 6.0}, {"low": 7.0, "high": 8.0}) is None
        assert bar.bar_better_line("X1", RC_BAR, "lower", {"low": 5.0, "high": 6.0}, {"low": 5.5, "high": 7.0}, "range") == RC_OQ2.replace("Q1", "X1")
        assert bar.bar_better_line("X1", RC_BAR, "lower", {"value": 6.0, "note": "one source"}, 3.0, "one_source") == RC_OQ2.replace("Q1", "X1")
    elif name == "OQ2: a value that is not a number, or no direction, is a named refusal, never 'not better'":
        for args in (("lower", None, 3), ("lower", 3, "x"), (None, 3, 4), ("lower", True, 4)):
            try:
                bar.bar_better_line("Q1", RC_BAR, *args)
            except _sb().Refusal as exc:
                assert "Q1" in str(exc), exc
            else:
                raise AssertionError(f"{args} passed")
    elif name == "OQ2: the line alone and no answer in norms.json: exit 1":
        code, text = rc_run(tmp, [RC_OQ2], rc_norms(tmp, bar_changes=[]))
        assert code == 1 and "ratcheted, new bar" in text, text
    elif name == "OQ2: bar_changes decision keep for that bar: exit 0":
        code, text = rc_run(tmp, [RC_OQ2], rc_norms(tmp, bar_changes=[{"bar": RC_BAR, "word": "owner, 14.11.2026", "decision": "keep"}]))
        assert code == 0 and "owner's word recorded" in text, text
    elif name == "OQ2: bar_changes decision lift for that bar: exit 0":
        code, text = rc_run(tmp, [RC_OQ2], rc_norms(tmp, bar_changes=[{"bar": RC_BAR, "word": "owner, 14.11.2026", "decision": "lift"}]))
        assert code == 0, text
    elif name == "OQ2: bar_changes decision 'maybe' is ignored and named: exit 1":
        code, text = rc_run(tmp, [RC_OQ2], rc_norms(tmp, bar_changes=[{"bar": RC_BAR, "word": "owner", "decision": "maybe"}]))
        assert code == 1 and "bar_changes entry 0 ignored" in text, text
    elif name == "OQ2: bar_changes without a word is ignored and named: exit 1":
        code, text = rc_run(tmp, [RC_OQ2], rc_norms(tmp, bar_changes=[{"bar": RC_BAR, "word": "", "decision": "keep"}]))
        assert code == 1 and "bar_changes entry 0 ignored" in text, text
    elif name == "OQ2: bar_changes for ANOTHER bar file: exit 1":
        code, text = rc_run(tmp, [RC_OQ2], rc_norms(tmp, bar_changes=[{"bar": "mybooks/add-to-cart/bar-other.yaml", "word": "owner", "decision": "keep"}]))
        assert code == 1, text
    elif name == "norms.json absent: the keys are read as empty, exit 1 on a needed line":
        code, text = rc_run(tmp, [RC_NEED, RC_OQ2], absent)
        assert code == 1, text
    elif name == "norms.json of the older shape (no bar_changes, no rows): read as empty, exit 1":
        code, text = rc_run(tmp, [RC_OQ2], rc_norms(tmp))
        assert code == 1, text
    elif name == "norms.json that is not JSON: a named error, never exit 0":
        for raw in ("{not json", "[]", ""):
            try:
                bar.release_check([RC_OK], RC_VERSION, rc_norms(tmp, raw=raw))
            except _sb().Refusal as exc:
                assert "norms file" in str(exc), exc
            else:
                raise AssertionError(f"{raw!r} passed")
    elif name == "norms.json whose bar_changes is not a list: a named error":
        try:
            bar.release_check([RC_OK], RC_VERSION, rc_norms(tmp, raw=json.dumps({"schema": "norms/2", "rows": {}, "bar_changes": {}})))
        except _sb().Refusal as exc:
            assert "bar_changes" in str(exc), exc
        else:
            raise AssertionError("a bad bar_changes passed")
    elif name == "limit: 20 open lines are all named":
        code, text = rc_run(tmp, [RC_NEED.replace("Q1", f"Q{i}") for i in range(20)], absent)
        assert code == 1 and "more" not in text.split("release-check:")[-1] and "[Q19 " in text.split("release-check:")[-1], text
    elif name == "limit: 21 open lines name 20 and count one more":
        code, text = rc_run(tmp, [RC_NEED.replace("Q1", f"Q{i}") for i in range(21)], absent)
        tail = text.split("release-check:")[-1]
        assert code == 1 and "21 line(s)" in tail and "... and 1 more" in tail and "[Q20 " not in tail, text
    elif name == "10,000 ok lines: exit 0":
        code, text = rc_run(tmp, [RC_OK] * 10000 + ["release: warning -- é" * 3], absent)
        assert code == 0, text[-200:]
    elif name == "command line: exit codes 0, 1 and 2 through scoreboard.py release-check":
        ok, need = tmp / "ok.txt", tmp / "need.txt"
        ok.write_text(RC_OK + "\n", encoding="utf-8")
        need.write_text(RC_OK + "\n" + RC_NEED + "\n", encoding="utf-8")
        norms = rc_norms(tmp, rows=rc_pass())
        assert sb_cli("release-check", "--version", RC_VERSION, "--lines", ok, "--norms", absent)[0] == 0
        code, printed, _e = sb_cli("release-check", "--version", "1.0.9", "--lines", need, "--norms", norms)
        assert code == 1 and "owner's word needed for 1 line(s)" in printed, printed
        assert sb_cli("release-check", "--version", RC_VERSION, "--lines", need, "--norms", norms)[0] == 0
        code, _o, err = sb_cli("release-check", "--version", RC_VERSION, "--lines", tmp / "no-such.txt", "--norms", norms)
        assert code == 2 and "RED:" in err, err
    else:
        raise AssertionError("no such case: " + name)


def _sb_names(*names):
    return [(n,) for n in names]


SB_RELEASE_CASES = _sb_names(
    "all lines ok: exit 0", "one owner's-word-needed line with no worsened_passes: exit 1 with the list",
    "worsened_passes of the same row, version and pair: exit 0", "worsened_passes of ANOTHER pair: exit 1",
    "worsened_passes of the same pair for ANOTHER version: exit 1", "worsened_passes with an empty word: exit 1",
    "worsened_passes of ANOTHER row, same version and pair: exit 1", "two needed lines, only one has its pass: exit 1 naming the other",
    "a warning line alone: exit 0 and the warning is printed", "'no previous release' alone: exit 0 (no ratcheted row exists)",
    "no lines at all: a named error, never a pass", "a needed line whose shape cannot be matched stays open: exit 1",
    "norms.json absent: the keys are read as empty, exit 1 on a needed line",
    "norms.json of the older shape (no bar_changes, no rows): read as empty, exit 1", "norms.json that is not JSON: a named error, never exit 0",
    "norms.json whose bar_changes is not a list: a named error", "limit: 20 open lines are all named",
    "limit: 21 open lines name 20 and count one more", "10,000 ok lines: exit 0",
    "command line: exit codes 0, 1 and 2 through scoreboard.py release-check")

SB_OQ2_CASES = _sb_names(
    "OQ2: a new bar strictly better than the factory (lower is better) gives the line",
    "OQ2: a new bar equal to or worse than the factory gives no line; an overlapping range is not decided and gives the line",
    "OQ2: a value that is not a number, or no direction, is a named refusal, never 'not better'",
    "OQ2: the line alone and no answer in norms.json: exit 1", "OQ2: bar_changes decision keep for that bar: exit 0",
    "OQ2: bar_changes decision lift for that bar: exit 0", "OQ2: bar_changes decision 'maybe' is ignored and named: exit 1",
    "OQ2: bar_changes without a word is ignored and named: exit 1", "OQ2: bar_changes for ANOTHER bar file: exit 1")


# --- P1-v N6b: norms/2, the ratchet check (K5), `compare --release` (B2) and the direct road of release-check ----------------------------
REL_VER, REL_FM, REL_STAND, REL_STORY = "1.1.0", "factory-model-a", "mybooks", "add-to-cart"
REL_BAR1 = f"{REL_STAND}/{REL_STORY}/bar-claude-sonnet-5-5.yaml"
REL_BAR2 = f"{REL_STAND}/{REL_STORY}/bar-claude-opus-5.yaml"
REL_OQ2 = f"release: owner's word needed -- Q1 ratcheted, new bar {REL_BAR2} is better than the factory"
REL_PAIR2 = f"claude-opus-5/{REL_STORY}"


def rel_el(value=10, factory_model=REL_FM, since="1.0.0", pair=RC_PAIR, bar=REL_BAR1):
    return {"pair": pair, "factory_model": factory_model, "since": since, "value": value, "bar": bar}


def rel_board(tmp: Path, row=None, version=REL_VER, models=(REL_FM,), run_class="live", norms=None, passes=None, rows=None, stamp="20261110-1000"):
    import yaml
    folder = tmp / "sb" / REL_STAND / REL_STORY
    folder.mkdir(parents=True, exist_ok=True)
    doc = {"schema": "scoreboard/1", "run": {"run_class": run_class, "arm": "factory", "models": list(models)},
           "rows": rows if rows is not None else ({"Q1": row} if row is not None else {}), "norms": norms or {}, "passes": passes or []}
    (folder / f"{stamp}-{version}-factory.yaml").write_text(yaml.safe_dump(doc), encoding="utf-8")


def rel_bar(tmp: Path, model: str, value, state="measured"):
    import yaml
    folder = tmp / "sb" / REL_STAND / REL_STORY
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"bar-{model}.yaml").write_text(yaml.safe_dump({"schema": "scoreboard/1", "run": {"arm": "free"},
                                                              "rows": {"Q1": {"state": state, "value": value}}}), encoding="utf-8")


def rel_norms(tmp: Path, ratchets=(), better="lower", raises=(), bar_changes=(), passes=(), name="norms.json", row_extra=None) -> Path:
    row = {"norm": 40, "unit": "questions", "better": better, "ratchets": list(ratchets), "raises": list(raises), "worsened_passes": list(passes)}
    row.update(row_extra or {})
    path = tmp / name
    path.write_text(json.dumps({"schema": "norms/2", "rows": {"Q1": row}, "bar_changes": list(bar_changes)}), encoding="utf-8")
    return path


def rel_lines(tmp: Path, norms: Path, version=REL_VER):
    return _sbb().release_lines(version, _sb().load_norms(norms), tmp / "sb")


def _need(text, factory_model=REL_FM):
    return f"release: owner's word needed -- Q1 {RC_PAIR} {text} [factory model {factory_model}]"


REL_NOLIVE = f"release: warning -- no live factory scoreboard of {REL_VER}: nothing judged"


def _m(value):
    return {"state": "measured", "value": value}


RNG = lambda low, high: {"low": low, "high": high}      # noqa: E731
SB_REL_JUDGE_CASES = [
    # (case id, the scoreboard row of the release, the ratchet's value, better, the ONE line expected)
    ("worse: a measured value above the ratchet (lower is better)", _m(12), 10, "lower", _need("was 10 (1.0.0) now 12 (1.1.0)")),
    ("not worse: equal to the ratchet", _m(10), 10, "lower", RC_OK),
    ("not worse: better than the ratchet", _m(8), 10, "lower", RC_OK),
    ("higher is better: below the ratchet is worse", _m(8), 10, "higher", _need("was 10 (1.0.0) now 8 (1.1.0)")),
    ("higher is better: above the ratchet is not worse", _m(11), 10, "higher", RC_OK),
    ("range now overlapping the ratchet: not decided: range", _m(RNG(9, 11)), 10, "lower", _need("not decided: range (9..11)")),
    ("range now with low_now > high_prev: worse", _m(RNG(11, 13)), 10, "lower", _need("was 10 (1.0.0) now 11..13 (1.1.0)")),
    ("range now with high_now <= low_prev: not worse", _m(RNG(7, 10)), 10, "lower", RC_OK),
    ("previous range, now above its high end: worse", _m(13), RNG(8, 12), "lower", _need("was 8..12 (1.0.0) now 13 (1.1.0)")),
    ("previous range, now at its low end: not worse", _m(8), RNG(8, 12), "lower", RC_OK),
    ("previous range, now inside it: not decided: range", _m(10), RNG(8, 12), "lower", _need("not decided: range (10)")),
    ("ranges that overlap at the edge: not decided: range", _m(RNG(12, 14)), RNG(8, 12), "lower", _need("not decided: range (12..14)")),
    ("range against range, now wholly above: worse", _m(RNG(13, 15)), RNG(8, 12), "lower", _need("was 8..12 (1.0.0) now 13..15 (1.1.0)")),
    ("range against range, now wholly below: not worse", _m(RNG(5, 8)), RNG(8, 12), "lower", RC_OK),
    ("one_source above the ratchet: worse, compared as a value", {"state": "one_source", "value": 12}, 10, "lower", _need("was 10 (1.0.0) now 12 (1.1.0)")),
    ("at_least above the ratchet: worse", {"state": "at_least", "value": 11}, 10, "lower", _need("was 10 (1.0.0) now at least 11 (1.1.0)")),
    # the shapes `assemble` writes (amendment B1): {at_least, note}, {low, high, note}, {value, note}
    ("X1 at_least {at_least, note} above the ratchet: worse", {"state": "at_least", "value": {"at_least": 11, "note": "n"}}, 10, "lower",
     _need("was 10 (1.0.0) now at least 11 (1.1.0)")),
    ("X1 at_least {at_least, note} below the ratchet: not decided: lower bound", {"state": "at_least", "value": {"at_least": 9, "note": "n"}}, 10, "lower",
     _need("not decided: lower bound (9)")),
    ("X1 range {low, high, note} overlapping the ratchet: not decided: range", {"state": "range", "value": {"low": 9, "high": 11, "note": "n"}}, 10, "lower",
     _need("not decided: range (9..11)")),
    ("X1 range {low, high, note} wholly above the ratchet: worse", {"state": "range", "value": {"low": 11, "high": 13, "note": "n"}}, 10, "lower",
     _need("was 10 (1.0.0) now 11..13 (1.1.0)")),
    ("X1 one_source {value, note} below the ratchet: not worse, compared as a value", {"state": "one_source", "value": {"value": 8, "note": "one source"}}, 10,
     "lower", RC_OK),
    ("X1 one_source {value, note} above the ratchet: worse", {"state": "one_source", "value": {"value": 12, "note": "one source"}}, 10, "lower",
     _need("was 10 (1.0.0) now 12 (1.1.0)")),
    ("at_least below the ratchet: not decided: lower bound", {"state": "at_least", "value": 9}, 10, "lower", _need("not decided: lower bound (9)")),
    ("at_least when higher is better: never decided", {"state": "at_least", "value": 20}, 10, "higher", _need("not decided: lower bound (20)")),
    ("state unknown: unknown: <why>", {"state": "unknown", "value": None, "why": "no price"}, 10, "lower", _need("unknown: no price")),
    ("state n/a: unknown with the reason", {"state": "n/a", "value": None, "why": "stub roles"}, 10, "lower", _need("unknown: stub roles")),
    ("the scoreboard has no such row: unknown", None, 10, "lower", _need("unknown: the scoreboard has no row Q1")),
    ("a value that is not a number: unknown", _m("x"), 10, "lower", _need("unknown: the value of Q1 is not a number")),
]


def sb_rel_judge_case(tmp: Path, case) -> None:
    _name, row, prev, better, want = case
    rel_board(tmp, rows={"Q1": row} if row is not None else {})
    assert rel_lines(tmp, rel_norms(tmp, [rel_el(prev)], better)) == [want]


def _cli_release(tmp, *extra, norms=None, version=REL_VER):
    return sb_cli("compare", "--release", version, "--norms", norms or rel_norms(tmp, [rel_el()]), "--root", tmp / "sb", *extra)


def _check_release(tmp, norms, *extra, version=REL_VER):
    return sb_cli("release-check", "--release", version, "--norms", norms, "--root", tmp / "sb", *extra)


def sb_rel_case(tmp: Path, case) -> None:
    name = case[0]
    if name == "no scoreboard for the pair: no value in this release":
        assert rel_lines(tmp, rel_norms(tmp, [rel_el()])) == [REL_NOLIVE, _need("no value in this release (no scoreboard for the pair)")]
    elif name == "a scoreboard of ANOTHER version only: no value in this release":
        rel_board(tmp, _m(1), version="1.0.9")
        assert rel_lines(tmp, rel_norms(tmp, [rel_el()])) == [REL_NOLIVE, _need("no value in this release (no scoreboard for the pair)")]
    elif name == "factory model differs: no comparable measurement":
        rel_board(tmp, _m(1), models=("factory-model-b",))
        assert rel_lines(tmp, rel_norms(tmp, [rel_el()])) == [_need("no comparable measurement (factory model factory-model-a vs factory-model-b)")]
    elif name == "a dry run: no comparable measurement":
        rel_board(tmp, _m(1), run_class="dry")
        assert rel_lines(tmp, rel_norms(tmp, [rel_el()])) == [REL_NOLIVE, _need("no comparable measurement (run class dry vs live)")]
    elif name == "two ratchet elements print exactly two element lines":
        rel_board(tmp, _m(1))
        lines = rel_lines(tmp, rel_norms(tmp, [rel_el(), rel_el(pair=REL_PAIR2, bar=REL_BAR2)]))
        assert lines == [RC_OK, f"release: ok -- Q1 {REL_PAIR2} not worse"], lines
    elif name == "no ratchet and no earlier release: 'no previous release', nothing else":
        assert rel_lines(tmp, rel_norms(tmp)) == ["release: no previous release -- ratchet not judged", REL_NOLIVE]
    elif name == "empty ratchets and a previous release: only warnings, release-check exit 0":
        rel_board(tmp, _m(9), norms={"N-q": {"norm": {"kind": "limit", "row": "Q1", "op": "<=", "value": 5}, "verdict": "red"}})
        rel_board(tmp, _m(3), version="1.0.9", stamp="20261001-1000")
        norms = rel_norms(tmp)
        assert rel_lines(tmp, norms) == ["release: warning -- Q1 red: 9 against norm 5"]
        code, printed, _e = _check_release(tmp, norms)
        assert code == 0 and "release: warning -- Q1 red: 9 against norm 5" in printed and printed.strip().endswith("release-check: ok"), printed
    elif name == "a previous release and nothing to say: no line, release-check exit 0":
        rel_board(tmp, _m(3), version="1.0.9", stamp="20261001-1000")
        rel_board(tmp, _m(3))
        assert rel_lines(tmp, rel_norms(tmp)) == []
        assert _check_release(tmp, rel_norms(tmp))[0] == 0
    elif name == "a red row that is ratcheted gets its element line, not a warning":
        rel_board(tmp, _m(9), norms={"N-q": {"norm": {"kind": "limit", "row": "Q1", "op": "<=", "value": 5}, "verdict": "red"}})
        assert rel_lines(tmp, rel_norms(tmp, [rel_el(10)])) == [RC_OK]
    elif name == "a red norm the owner passed gives no warning":
        rel_board(tmp, _m(9), norms={"N-q": {"norm": {"kind": "limit", "row": "Q1", "op": "<=", "value": 5}, "verdict": "red"}},
                  passes=[{"norm": "N-q", "word": "owner", "date": "14.11.2026"}])
        assert rel_lines(tmp, rel_norms(tmp)) == ["release: no previous release -- ratchet not judged"]
    elif name == "a measured row better than its bar: can ratchet, with the bar file and its value":
        rel_board(tmp, _m(4))
        rel_bar(tmp, "claude-sonnet-5-5", 10)
        assert rel_lines(tmp, rel_norms(tmp)) == ["release: no previous release -- ratchet not judged",
                                                  f"can ratchet: Q1 {RC_PAIR} 4 better than bar {REL_BAR1} (10)"]
    elif name == "a row equal to or worse than its bar is not proposed":
        for value in (10, 12):
            rel_board(tmp, _m(value))
            rel_bar(tmp, "claude-sonnet-5-5", 10)
            assert not [x for x in rel_lines(tmp, rel_norms(tmp)) if x.startswith("can ratchet")], value
    elif name == "a row in the state one_source, range, at_least or unknown is never proposed":
        rel_bar(tmp, "claude-sonnet-5-5", 10)
        for row in ({"state": "one_source", "value": 4}, _m(RNG(3, 4)), {"state": "at_least", "value": 4}, {"state": "unknown", "value": None}):
            rel_board(tmp, row)
            assert not [x for x in rel_lines(tmp, rel_norms(tmp)) if x.startswith("can ratchet")], row
    elif name == "a row already ratcheted for that pair is not proposed again":
        rel_board(tmp, _m(4))
        rel_bar(tmp, "claude-sonnet-5-5", 10)
        assert not [x for x in rel_lines(tmp, rel_norms(tmp, [rel_el(10)])) if x.startswith("can ratchet")]
    elif name == "a bar whose row is not measured is never beaten":
        rel_board(tmp, _m(4))
        rel_bar(tmp, "claude-sonnet-5-5", None, state="unknown")
        assert not [x for x in rel_lines(tmp, rel_norms(tmp)) if x.startswith("can ratchet")]
    elif name == "OQ2: a new bar better than the factory on a ratcheted row prints the line; release-check exit 1, with bar_changes exit 0":
        rel_board(tmp, _m(6))
        rel_bar(tmp, "claude-opus-5", 3)
        norms = rel_norms(tmp, [rel_el(10)])
        assert rel_lines(tmp, norms) == [RC_OK, REL_OQ2]
        assert _check_release(tmp, norms)[0] == 1
        answered = rel_norms(tmp, [rel_el(10)], bar_changes=[{"bar": REL_BAR2, "word": "owner, 14.11.2026", "decision": "keep"}], name="n2.json")
        assert _check_release(tmp, answered)[0] == 0
    elif name == "OQ2: a new bar worse than the factory gives no line":
        rel_board(tmp, _m(6))
        rel_bar(tmp, "claude-opus-5", 8)
        assert REL_OQ2 not in rel_lines(tmp, rel_norms(tmp, [rel_el(10)]))
    elif name == "compare --release exits 0 even when a line needs the owner's word":
        rel_board(tmp, _m(12))
        code, printed, _e = _cli_release(tmp)
        assert code == 0 and printed.strip() == _need("was 10 (1.0.0) now 12 (1.1.0)"), printed
    elif name == "release-check --release: a worse row without worsened_passes exit 1, with the same row, version and pair exit 0":
        rel_board(tmp, _m(12))
        code, printed, _e = _check_release(tmp, rel_norms(tmp, [rel_el()]))
        assert code == 1 and "owner's word needed for 1 line(s)" in printed, printed
        word = {"version": REL_VER, "pair": RC_PAIR, "word": "owner, 14.11.2026", "quote": "ship it"}
        assert _check_release(tmp, rel_norms(tmp, [rel_el()], passes=[word], name="p.json"))[0] == 0
    elif name == "release-check --release: a worsened_passes entry of another pair or another version does not cover the line":
        rel_board(tmp, _m(12))
        for change in ({"pair": REL_PAIR2}, {"version": "1.0.9"}, {"word": " "}):
            word = dict({"version": REL_VER, "pair": RC_PAIR, "word": "owner, 14.11.2026", "quote": "x"}, **change)
            assert _check_release(tmp, rel_norms(tmp, [rel_el()], passes=[word], name="p.json"))[0] == 1, change
    elif name == "release-check --release: all ratchets not worse: exit 0":
        rel_board(tmp, _m(9))
        code, printed, _e = _check_release(tmp, rel_norms(tmp, [rel_el()]))
        assert code == 0 and printed.strip().endswith("release-check: ok"), printed
    elif name == "norms.json absent: compare --release and release-check --release exit 2 naming the path":
        absent = tmp / "none.json"
        for code, _o, err in (sb_cli("compare", "--release", REL_VER, "--norms", absent, "--root", tmp / "sb"), _check_release(tmp, absent)):
            assert code == 2 and str(absent) in err, err
    elif name == "norms.json that is not JSON: exit 2 naming the path":
        bad = tmp / "bad.json"
        bad.write_text("{not json", encoding="utf-8")
        for code, _o, err in (_cli_release(tmp, norms=bad), _check_release(tmp, bad)):
            assert code == 2 and str(bad) in err, err
    elif name == "norms.json whose rows is a list: exit 2 naming the path":
        bad = tmp / "list.json"
        bad.write_text(json.dumps({"schema": "norms/2", "rows": []}), encoding="utf-8")
        for code, _o, err in (_cli_release(tmp, norms=bad), _check_release(tmp, bad)):
            assert code == 2 and str(bad) in err and "rows" in err, err
    elif name == "a version that is empty or has path separators: exit 2, nothing read":
        for version in ("", "../x", "a/b", "a\\b", ".."):
            for code, printed, err in (_cli_release(tmp, version=version), _check_release(tmp, rel_norms(tmp), version=version)):
                assert code == 2 and "version" in err and printed == "", (version, err)
    elif name == "release-check takes exactly one input: both or neither is exit 2":
        norms = rel_norms(tmp)
        assert sb_cli("release-check", "--release", REL_VER, "--lines", tmp / "x.txt", "--norms", norms)[0] == 2
        assert sb_cli("release-check", "--norms", norms)[0] == 2
        assert sb_cli("release-check", "--lines", tmp / "x.txt", "--norms", norms)[0] == 2
    elif name == "compare takes a scoreboard or --release, not both and not neither":
        assert sb_cli("compare", "--norms", rel_norms(tmp))[0] == 2
        assert sb_cli("compare", str(tmp / "x.yaml"), "--release", REL_VER, "--norms", rel_norms(tmp))[0] == 2
    else:
        sb_rel_fix_case(tmp, name)


def _rel_two_rows_norms(tmp: Path) -> Path:
    """Two ratcheted rows (Q1, Q2) whose ratchets name the same bar file."""
    rows = {rid: {"norm": 40, "unit": "questions", "better": "lower", "ratchets": [rel_el(10)], "raises": [], "worsened_passes": []} for rid in ("Q1", "Q2")}
    path = tmp / "two.json"
    path.write_text(json.dumps({"schema": "norms/2", "rows": rows, "bar_changes": []}), encoding="utf-8")
    return path


def sb_rel_fix_case(tmp: Path, name: str) -> None:
    """The fix round t-714: F2, F3, F4, F6, and W16 of the topic critic's worlds (each a row of SB_REL_CASES)."""
    import yaml
    other = "release: warning -- Q1 unknown: row Q1: not recorded"
    unknown_norm = {"N-q": {"norm": {"kind": "limit", "row": "Q1", "op": "<=", "value": 5}, "verdict": "unknown", "why": "row Q1: not recorded"}}
    if name == "W9: an older live board of the ratchet's factory model is judged, a newer board of another model does not hide it":
        rel_board(tmp, _m(9), models=("factory-model-a",), stamp="20261105-1000")
        rel_board(tmp, _m(99), models=("factory-model-b",), stamp="20261110-1000")
        assert rel_lines(tmp, rel_norms(tmp, [rel_el()])) == [RC_OK]
    elif name == "W9b: no live board holds the factory model: the line still names the model mismatch":
        rel_board(tmp, _m(9), models=("factory-model-b",), stamp="20261105-1000")
        rel_board(tmp, _m(9), models=("factory-model-c",), stamp="20261110-1000")
        assert rel_lines(tmp, rel_norms(tmp, [rel_el()])) == [_need("no comparable measurement (factory model factory-model-a vs factory-model-c)")]
    elif name == "W10: a newer dry board does not hide an older live one":
        rel_board(tmp, _m(9), stamp="20261105-1000")
        rel_board(tmp, _m(99), run_class="dry", stamp="20261110-1000")
        assert rel_lines(tmp, rel_norms(tmp, [rel_el()])) == [RC_OK]
    elif name == "W11: an unratcheted row whose norm verdict is unknown gets a warning; release-check exit 0":
        rel_board(tmp, _m(3), norms=unknown_norm)
        rel_board(tmp, _m(3), version="1.0.9", stamp="20261001-1000")
        norms = rel_norms(tmp)
        assert rel_lines(tmp, norms) == [other]
        code, printed, _e = _check_release(tmp, norms)
        assert code == 0 and other in printed and printed.strip().endswith("release-check: ok"), printed
    elif name == "W11b: a ratcheted row with an unknown norm verdict gets no warning (its element line speaks)":
        rel_board(tmp, _m(3), norms=unknown_norm)
        assert rel_lines(tmp, rel_norms(tmp, [rel_el()])) == [RC_OK]
    elif name == "W12: no live factory scoreboard of the version, an older release exists: a warning, release-check exit 0":
        rel_board(tmp, _m(3), version="1.0.9", stamp="20261001-1000")
        norms = rel_norms(tmp)
        assert rel_lines(tmp, norms) == [REL_NOLIVE]
        code, printed, _e = _check_release(tmp, norms)
        assert code == 0 and REL_NOLIVE in printed, printed
    elif name == "W13: the factory value one_source or a range, a better new bar: the OQ2 line, release-check exit 1":
        rel_bar(tmp, "claude-opus-5", 3)
        for row in ({"state": "one_source", "value": {"value": 6, "note": "one source"}}, {"state": "range", "value": {"low": 2, "high": 8, "note": "n"}}):
            rel_board(tmp, row)
            norms = rel_norms(tmp, [rel_el(10)])
            assert REL_OQ2 in rel_lines(tmp, norms), row
            assert _check_release(tmp, norms)[0] == 1, row
    elif name == "W13b: a measured factory value that is no worse than the new bar gives no OQ2 line":
        rel_bar(tmp, "claude-opus-5", 6)
        rel_board(tmp, _m(6))
        assert REL_OQ2 not in rel_lines(tmp, rel_norms(tmp, [rel_el(10)]))
    elif name == "OQ2 is keyed by (row, bar): a second ratcheted row beaten by the same bar gets its own line":
        rel_board(tmp, rows={"Q1": _m(6), "Q2": _m(6)})
        folder = tmp / "sb" / REL_STAND / REL_STORY
        (folder / "bar-claude-opus-5.yaml").write_text(yaml.safe_dump({"schema": "scoreboard/1", "run": {"arm": "free"}, "rows": {
            "Q1": _m(3), "Q2": _m(3)}}), encoding="utf-8")
        lines = [x for x in rel_lines(tmp, _rel_two_rows_norms(tmp)) if "new bar" in x]
        assert lines == [REL_OQ2, REL_OQ2.replace("Q1", "Q2")], lines
    elif name == "W16: one worsened_passes entry clears the element of ITS factory model only":
        rel_board(tmp, _m(12), models=("factory-model-a", "factory-model-b"))
        els = [rel_el(10, factory_model="factory-model-a"), rel_el(10, factory_model="factory-model-b")]
        word = {"version": REL_VER, "pair": RC_PAIR, "word": "owner, 14.11.2026", "quote": "x", "factory_model": "factory-model-a"}
        code, printed, _e = _check_release(tmp, rel_norms(tmp, els, passes=[word]))
        tail = printed.split("release-check:")[-1]
        assert code == 1 and printed.count("owner's word recorded") == 1 and "factory-model-b" in tail and "factory-model-a" not in tail, printed
        both = [word, dict(word, factory_model="factory-model-b")]
        assert _check_release(tmp, rel_norms(tmp, els, passes=both, name="b.json"))[0] == 0
    elif name == "W16b: a worsened_passes entry with no factory_model (an old entry) is read as before: it clears both":
        rel_board(tmp, _m(12), models=("factory-model-a", "factory-model-b"))
        els = [rel_el(10, factory_model="factory-model-a"), rel_el(10, factory_model="factory-model-b")]
        word = {"version": REL_VER, "pair": RC_PAIR, "word": "owner, 14.11.2026", "quote": "x"}
        code, printed, _e = _check_release(tmp, rel_norms(tmp, els, passes=[word]))
        assert code == 0 and printed.count("owner's word recorded") == 2, printed
    elif name == "release: a scoreboard built by `assemble` with one_source X1 is never proposed by `can ratchet:`; the same with agrees is":
        _release_assembled_case(tmp)
    else:
        raise AssertionError("no such case: " + name)


def _release_assembled_case(tmp: Path) -> None:
    """B1 end to end: `assemble` writes the X1 state; `compare --release` reads that very file (positive control: `agrees` is proposed)."""
    import yaml
    scoreboard = _sb()
    folder = tmp / "sb" / REL_STAND / REL_STORY
    folder.mkdir(parents=True)
    (folder / "bar-claude-sonnet-5-5.yaml").write_text(yaml.safe_dump({"schema": "scoreboard/1", "run": {"arm": "free"}, "rows": {"X1": _m(5.0)}}), encoding="utf-8")
    norms = tmp / "x1.json"
    norms.write_text(json.dumps({"schema": "norms/2", "rows": {"X1": {"norm": None, "unit": "usd", "better": "lower", "ratchets": [], "raises": [],
                                                                       "worsened_passes": []}}}), encoding="utf-8")
    saved = scoreboard.TP.task_price
    try:
        for status, proposed in (("agrees", True), ("not_cross_checked", False), ("differs", False), ("incomplete", False)):
            scoreboard.TP.task_price = lambda root, task, status=status: {"status": status, "price_low_usd": 2.0, "price_high_usd": 2.0}
            task = sb_run(tmp / f"r-{status}", run_class="live")
            for old in folder.glob("*-factory.yaml"):
                old.unlink()
            code, _p, err = sb_cli("assemble", "--task-root", task, "--stand", REL_STAND, "--story", REL_STORY, "--arm", "factory", "--version", REL_VER,
                                   "--model", REL_FM, "--out-root", tmp / "sb")
            assert code == 0, err
            lines = _sbb().release_lines(REL_VER, scoreboard.load_norms(norms), tmp / "sb")
            got = [x for x in lines if x.startswith("can ratchet: X1")]
            assert bool(got) == proposed, (status, lines)
    finally:
        scoreboard.TP.task_price = saved


SB_REL_FIX_NAMES = (
    "W9: an older live board of the ratchet's factory model is judged, a newer board of another model does not hide it",
    "W9b: no live board holds the factory model: the line still names the model mismatch",
    "W10: a newer dry board does not hide an older live one",
    "W11: an unratcheted row whose norm verdict is unknown gets a warning; release-check exit 0",
    "W11b: a ratcheted row with an unknown norm verdict gets no warning (its element line speaks)",
    "W12: no live factory scoreboard of the version, an older release exists: a warning, release-check exit 0",
    "W13: the factory value one_source or a range, a better new bar: the OQ2 line, release-check exit 1",
    "W13b: a measured factory value that is no worse than the new bar gives no OQ2 line",
    "OQ2 is keyed by (row, bar): a second ratcheted row beaten by the same bar gets its own line",
    "W16: one worsened_passes entry clears the element of ITS factory model only",
    "W16b: a worsened_passes entry with no factory_model (an old entry) is read as before: it clears both",
    "release: a scoreboard built by `assemble` with one_source X1 is never proposed by `can ratchet:`; the same with agrees is")

SB_REL_CASES = _sb_names(*SB_REL_FIX_NAMES,
    "no scoreboard for the pair: no value in this release", "a scoreboard of ANOTHER version only: no value in this release",
    "factory model differs: no comparable measurement", "a dry run: no comparable measurement",
    "two ratchet elements print exactly two element lines", "no ratchet and no earlier release: 'no previous release', nothing else",
    "empty ratchets and a previous release: only warnings, release-check exit 0", "a previous release and nothing to say: no line, release-check exit 0",
    "a red row that is ratcheted gets its element line, not a warning", "a red norm the owner passed gives no warning",
    "a measured row better than its bar: can ratchet, with the bar file and its value", "a row equal to or worse than its bar is not proposed",
    "a row in the state one_source, range, at_least or unknown is never proposed", "a row already ratcheted for that pair is not proposed again",
    "a bar whose row is not measured is never beaten",
    "OQ2: a new bar better than the factory on a ratcheted row prints the line; release-check exit 1, with bar_changes exit 0",
    "OQ2: a new bar worse than the factory gives no line", "compare --release exits 0 even when a line needs the owner's word",
    "release-check --release: a worse row without worsened_passes exit 1, with the same row, version and pair exit 0",
    "release-check --release: a worsened_passes entry of another pair or another version does not cover the line",
    "release-check --release: all ratchets not worse: exit 0",
    "norms.json absent: compare --release and release-check --release exit 2 naming the path", "norms.json that is not JSON: exit 2 naming the path",
    "norms.json whose rows is a list: exit 2 naming the path", "a version that is empty or has path separators: exit 2, nothing read",
    "release-check takes exactly one input: both or neither is exit 2", "compare takes a scoreboard or --release, not both and not neither")

# K5 for a ratchet element: (case id, old ratchets, new ratchets, new raises, better, words of the problem or None when green)
WORD = {"ratchet": f"{RC_PAIR}@{REL_FM}", "raised_by": "Lead", "reason": "the story grew", "word": "owner, 14.11.2026"}
SB_RATCHET_ELEMENT_CASES = [
    ("a ratchet element unchanged is green", [rel_el(10)], [rel_el(10)], [], "lower", None),
    ("a ratchet element removed with no raise: refused", [rel_el(10)], [], [], "lower", "was removed"),
    ("a ratchet element removed with a raise carrying the word: green", [rel_el(10)], [], [WORD], "lower", None),
    ("a ratchet value worsened (lower is better): refused", [rel_el(10)], [rel_el(11)], [], "lower", "worsened from 10 to 11"),
    ("a ratchet value worsened with a raise carrying the word: green", [rel_el(10)], [rel_el(11)], [WORD], "lower", None),
    ("a ratchet value worsened with a raise whose word is empty: refused", [rel_el(10)], [rel_el(11)], [dict(WORD, word=" ")], "lower", "worsened"),
    ("a ratchet value improved is green", [rel_el(10)], [rel_el(8)], [], "lower", None),
    ("higher is better: a lower ratchet value is refused", [rel_el(10)], [rel_el(9)], [], "higher", "worsened from 10 to 9"),
    ("higher is better: a higher ratchet value is green", [rel_el(10)], [rel_el(11)], [], "higher", None),
    ("a range ratchet whose high end grew: refused", [rel_el(RNG(5, 8))], [rel_el(RNG(5, 9))], [], "lower", "worsened"),
    ("a ratchet element added is green", [], [rel_el(10)], [], "lower", None),
    ("only the other element removed: refused naming the pair", [rel_el(10), rel_el(7, pair=REL_PAIR2, bar=REL_BAR2)], [rel_el(10)], [], "lower", REL_PAIR2),
]


KIND = {"id": "N-q", "kind": "limit", "op": "<=", "norm": 40, "initial": 40}      # a row WITH a norm (every row of the shipped file has one)
NORM_RAISE = {"raised_by": "Lead", "reason": "the norm moved", "word": "owner, 14.11.2026", "from": 40, "to": 41}
PASS = {"version": REL_VER, "pair": RC_PAIR, "word": "owner, 14.11.2026", "quote": "x"}
# B3 / Q-b: (case id, extra keys of the old row, of the new row, old ratchets, new ratchets, old raises, new raises, old passes, new passes, `--against`, words or None)
SB_RAISE_SCOPE_CASES = [
    ("K5 on a row WITH a kind: a worsened ratchet and a ratchet raise {ratchet, raised_by, reason, word} is green", KIND, KIND, [rel_el(10)], [rel_el(11)], [], [WORD],
     [], [], True, None),
    ("K6 on a row with a kind: the same raise carrying from=to=40 is green (from and to are not read for a ratchet raise)", KIND, KIND, [rel_el(10)], [rel_el(11)],
     [], [dict(WORD, **{"from": 40, "to": 40})], [], [], True, None),
    ("K7 on a row with a kind: a NORM raise 40 -> 41 legalises no ratchet change", KIND, KIND, [rel_el(10)], [rel_el(11)], [], [NORM_RAISE], [], [], True, "worsened"),
    ("a ratchet raise legalises no norm change: the norm loosened to 45 with no norm raise", KIND, dict(KIND, norm=45), [rel_el(10)], [rel_el(11)], [], [WORD],
     [], [], True, "looser"),
    ("a ratchet raise for ANOTHER factory model does not clear this element", KIND, KIND, [rel_el(10)], [rel_el(11)], [],
     [dict(WORD, ratchet=f"{RC_PAIR}@factory-model-b")], [], [], True, "worsened"),
    ("a ratchet raise missing its reason is refused on a row with a kind", KIND, KIND, [rel_el(10)], [rel_el(11)], [], [{k: v for k, v in WORD.items() if k != "reason"}],
     [], [], True, "raises[0]"),
    ("a raise {word} alone on a row with no kind is refused (K8b)", {}, {}, [], [], [], [{"word": "x"}], [], [], True, "raises[0]"),
    ("a ratchet raise whose `ratchet` is not <pair>@<model>: refused", KIND, KIND, [], [], [], [dict(WORD, ratchet="nonsense")], [], [], True, "`ratchet` is"),
    ("an earlier ratchet raise kept: green", KIND, KIND, [rel_el(10)], [rel_el(10)], [WORD], [WORD], [], [], True, None),
    ("an earlier ratchet raise removed: refused", KIND, KIND, [rel_el(10)], [rel_el(10)], [WORD], [], [], [], True, "may only be appended"),
    ("a NEW worsened_passes entry without factory_model: refused", KIND, KIND, [], [], [], [], [], [PASS], True, "needs the `factory_model`"),
    ("a NEW worsened_passes entry with factory_model: green", KIND, KIND, [], [], [], [], [], [dict(PASS, factory_model=REL_FM)], True, None),
    ("a worsened_passes entry already in the base file without factory_model: read as before, green", KIND, KIND, [], [], [], [], [PASS], [PASS], True, None),
    ("no --against: an entry without factory_model is refused (every entry is new)", KIND, KIND, [], [], [], [], [], [PASS], False, "needs the `factory_model`"),
    ("a worsened_passes factory_model that is blank: refused", KIND, KIND, [], [], [], [], [], [dict(PASS, factory_model=" ")], True, "needs the `factory_model`"),
]


def sb_raise_scope_case(tmp: Path, case) -> None:
    _name, old_extra, new_extra, old_r, new_r, old_raises, new_raises, old_passes, new_passes, against, want = case
    scoreboard = _sb()
    old_file = rel_norms(tmp, old_r, "lower", raises=old_raises, passes=old_passes, name="old.json", row_extra=old_extra)
    new_file = rel_norms(tmp, new_r, "lower", raises=new_raises, passes=new_passes, name="new.json", row_extra=new_extra)
    problems = scoreboard.check_norms(scoreboard.load_norms(new_file), scoreboard.load_old_norms(old_file) if against else None)
    if want is None:
        assert problems == [], problems
    else:
        assert any(want in p for p in problems), problems
        argv = ["norms", "--check", "--norms", new_file] + (["--against", old_file] if against else [])
        code, printed, _e = sb_cli(*argv)
        assert code == 1 and printed.strip().endswith("norms: red"), printed


def sb_ratchet_element_case(tmp: Path, case) -> None:
    _name, old, new, raises, better, want = case
    old_file = rel_norms(tmp, old, better, name="old.json")
    new_file = rel_norms(tmp, new, better, raises=raises, name="new.json")
    scoreboard = _sb()
    problems = scoreboard.check_norms(scoreboard.load_norms(new_file), scoreboard.load_old_norms(old_file))
    if want is None:
        assert problems == [], problems
    else:
        assert any(want in p for p in problems), problems
        code, printed, _e = sb_cli("norms", "--check", "--norms", new_file, "--against", old_file)
        assert code == 1 and printed.strip().endswith("norms: red"), printed


def _v1_of(view: dict) -> dict:
    return {"schema": "norms/1", "norms": view["norms"], "raises": view["raises"]}


def sb_norms2_case(tmp: Path, case) -> None:
    name, scoreboard = case[0], _sb()
    view = _norms()
    if name == "a norms/1 file is refused by load_norms with what is wrong, what is expected and how to convert":
        old = tmp / "old.json"
        old.write_text(json.dumps(_v1_of(view)), encoding="utf-8")
        try:
            scoreboard.load_norms(old)
        except scoreboard.Refusal as exc:
            assert all(word in str(exc) for word in ("norms/1", "norms/2", "--convert", str(old))), exc
        else:
            raise AssertionError("a norms/1 file was read")
        assert sb_cli("norms", "--check", "--norms", old)[0] == 2
    elif name == "round trip: norms/1 -> norms/2 -> the same K2/K5 view, every norm key kept":
        v2 = scoreboard.legacy_to_v2(_v1_of(view))
        path = tmp / "v2.json"
        path.write_text(json.dumps(v2), encoding="utf-8")
        again = scoreboard.load_norms(path)
        assert again["norms"] == view["norms"] and again["raises"] == view["raises"], (again["norms"], view["norms"])
        assert set(v2["rows"]) == {n["row"] for n in view["norms"].values()} and all(r["id"] in view["norms"] for r in v2["rows"].values())
        for rid, row in v2["rows"].items():
            assert {"norm", "unit", "better", "ratchets", "raises", "worsened_passes", "id", "kind"} <= set(row) or row["kind"] == "not_worse_than_bar", rid
    elif name == "round trip: the K5 verdicts of today's rows are unchanged through a norms/1 file read as --against":
        old = _v1_of(view)
        old["norms"]["N-questions"]["value"] = 30
        old["norms"]["N-questions"]["initial"] = 30
        (tmp / "old.json").write_text(json.dumps(old), encoding="utf-8")
        code, printed, _e = sb_cli("norms", "--check", "--norms", HERE.parent / "scoreboards" / "norms.json", "--against", tmp / "old.json")
        assert code == 1 and "`initial` changed" in printed, printed
        old["norms"]["N-questions"]["initial"] = 40
        old["norms"]["N-questions"]["value"] = 40
        (tmp / "old.json").write_text(json.dumps(old), encoding="utf-8")
        code, printed, _e = sb_cli("norms", "--check", "--norms", HERE.parent / "scoreboards" / "norms.json", "--against", tmp / "old.json")
        assert code == 0 and printed.strip().endswith("norms: green"), printed
    elif name == "norms --convert prints a norms/2 file that load_norms reads":
        old = tmp / "old.json"
        old.write_text(json.dumps(_v1_of(view)), encoding="utf-8")
        code, printed, _e = sb_cli("norms", "--convert", old)
        (tmp / "new.json").write_text(printed, encoding="utf-8")
        assert code == 0 and scoreboard.load_norms(tmp / "new.json")["norms"] == view["norms"]
    elif name == "two norms pointing at ONE row are refused naming both ids, never merged":
        v1 = {"norms": {"N-a": {"kind": "limit", "row": "Q1", "op": "<=", "value": 1}, "N-b": {"kind": "limit", "row": "Q1", "op": "<=", "value": 2}}, "raises": []}
        try:
            scoreboard.legacy_to_v2(v1)
        except scoreboard.Refusal as exc:
            assert "N-a" in str(exc) and "N-b" in str(exc) and "Q1" in str(exc), exc
        else:
            raise AssertionError("two norms of one row were merged")
    elif name == "a raise naming an unknown norm is refused at conversion":
        try:
            scoreboard.legacy_to_v2({"norms": {}, "raises": [dict(RAISE)]})
        except scoreboard.Refusal as exc:
            assert "unknown norm N-questions" in str(exc), exc
        else:
            raise AssertionError("an orphan raise was dropped")
    elif name == "a norm id carried by two rows is refused":
        row = {"id": "N-a", "kind": "limit", "op": "<=", "norm": 1, "better": "lower"}
        (tmp / "d.json").write_text(json.dumps({"schema": "norms/2", "rows": {"Q1": row, "Q3": dict(row)}}), encoding="utf-8")
        try:
            scoreboard.load_norms(tmp / "d.json")
        except scoreboard.Refusal as exc:
            assert "N-a" in str(exc) and "Q1" in str(exc) and "Q3" in str(exc), exc
        else:
            raise AssertionError("a duplicate id was read")
    elif name == "`op` and `better` that disagree are refused":
        row = {"id": "N-a", "kind": "limit", "op": "<=", "norm": 1, "better": "higher"}
        (tmp / "d.json").write_text(json.dumps({"schema": "norms/2", "rows": {"Q1": row}}), encoding="utf-8")
        try:
            scoreboard.load_norms(tmp / "d.json")
        except scoreboard.Refusal as exc:
            assert "disagree" in str(exc), exc
        else:
            raise AssertionError("op and better disagreed silently")
    elif name == "a norm whose row is absent from rows.json keeps the refusal of K2 (unknown row: not green)":
        view["norms"]["N-ghost"] = {"kind": "limit", "row": "ZZ9", "op": "<=", "value": 1, "unit": "x"}
        judged = scoreboard.judge_norms(view, {"Q1": {"state": "measured", "value": 1}}, "live", None, None, scoreboard.load_rows())
        assert judged["N-ghost"]["verdict"] == "unknown", judged["N-ghost"]
    elif name == "a norms/2 file of another schema is refused naming the schema":
        (tmp / "d.json").write_text(json.dumps({"schema": "norms/3", "rows": {}}), encoding="utf-8")
        try:
            scoreboard.load_norms(tmp / "d.json")
        except scoreboard.Refusal as exc:
            assert "norms/3" in str(exc) and "norms/2" in str(exc), exc
        else:
            raise AssertionError("an unknown schema was read")
    elif name == "the shipped norms.json is norms/2 with empty ratchets and worsened_passes and every norm key of norms/1":
        doc = json.loads((HERE.parent / "scoreboards" / "norms.json").read_text(encoding="utf-8"))
        assert doc["schema"] == "norms/2" and doc["bar_changes"] == []
        for row in doc["rows"].values():
            assert row["ratchets"] == [] and row["worsened_passes"] == [] and row["raises"] == [], row
            assert {"id", "kind", "norm", "unit", "better", "carrier", "ratcheted_since"} <= set(row) and ("initial" in row or row["kind"] == "not_worse_than_bar"), row
        assert {r["id"] for r in doc["rows"].values()} == {"N-rework", "N-gate", "N-questions", "N-wall", "N-brief"} | {f"N-quality-QA{i}" for i in range(1, 7)}
        assert doc["rows"]["G1"]["unknown_row"] == "G1u" and doc["rows"]["T1x"]["bar_row"] == "T1"
    else:
        raise AssertionError("no such case: " + name)


SB_NORMS2_CASES = _sb_names(
    "a norms/1 file is refused by load_norms with what is wrong, what is expected and how to convert",
    "round trip: norms/1 -> norms/2 -> the same K2/K5 view, every norm key kept",
    "round trip: the K5 verdicts of today's rows are unchanged through a norms/1 file read as --against",
    "norms --convert prints a norms/2 file that load_norms reads",
    "two norms pointing at ONE row are refused naming both ids, never merged", "a raise naming an unknown norm is refused at conversion",
    "a norm id carried by two rows is refused", "`op` and `better` that disagree are refused",
    "a norm whose row is absent from rows.json keeps the refusal of K2 (unknown row: not green)",
    "a norms/2 file of another schema is refused naming the schema",
    "the shipped norms.json is norms/2 with empty ratchets and worsened_passes and every norm key of norms/1")

# a ratchet element that is itself malformed is refused at load (outside input: a norms file)
BAD_RATCHETS = [
    ("a pair with a space", rel_el(pair="claude sonnet/add-to-cart"), "pair"), ("a pair with no story", rel_el(pair="claude-sonnet-5-5"), "pair"),
    ("a bar with `..` in it", rel_el(bar="mybooks/../bar-x.yaml"), "bar"), ("a bar of another story than the pair", rel_el(bar="mybooks/other/bar-x.yaml"), "bar"),
    ("a bar that is an absolute path", rel_el(bar="/etc/bar-x.yaml"), "bar"), ("a value that is not a number", rel_el(value="ten"), "value"),
    ("an empty factory model", rel_el(factory_model=" "), "factory_model"), ("a missing since", {k: v for k, v in rel_el().items() if k != "since"}, "since"),
    ("an element that is not an object", "x", "ratchets[0]"),
]
SB_BAD_RATCHET_CASES = [(f"a ratchet element with {n} is refused naming the key", e, k) for n, e, k in BAD_RATCHETS] + [
    ("a ratchet on a row with no direction is refused", rel_el(), "better")]


def sb_bad_ratchet_case(tmp: Path, case) -> None:
    name, element, key = case
    scoreboard = _sb()
    path = rel_norms(tmp, [element], better=None if "no direction" in name else "lower")
    try:
        scoreboard.load_norms(path)
    except scoreboard.Refusal as exc:
        assert key in str(exc) and str(path) in str(exc), exc
    else:
        raise AssertionError("a malformed ratchet was read")


BOM = b"\xef\xbb\xbf"
# B4, outside input: a saved `compare --release` output (Windows PowerShell 5.1 `Out-File -Encoding utf8` writes the BOM). (case id, file bytes, exit code, words in the output)
SB_LINES_CASES = [
    ("a needed line with no pass: exit 1 (the control the BOM rows are read against)", (RC_OK + "\n" + RC_NEED + "\n").encode(), 1, "owner's word needed for 1 line(s)"),
    ("a UTF-8 BOM before the same needed line: still exit 1, never ok", BOM + (RC_OK + "\n" + RC_NEED + "\n").encode(), 1, "owner's word needed for 1 line(s)"),
    ("a UTF-8 BOM before ok lines: exit 0", BOM + (RC_OK + "\n").encode(), 0, "release-check: ok"),
    ("a leading-space needed line: exit 1", ("  " + RC_NEED + "\n").encode(), 1, "owner's word needed for 1 line(s)"),
    ("blank lines and a can ratchet line between release lines: exit 0", (RC_OK + "\n\n   \ncan ratchet: Q1 a/b 4 better than bar x (10)\n").encode(), 0, "release-check: ok"),
    ("a text file that is no release output: exit 2 naming line 1 and the line", b"hello world\nnot a release line\n", 2, "line 1"),
    ("a wrong line after good ones: exit 2 naming line 3", (RC_OK + "\n\nsomething else\n").encode(), 2, "line 3"),
    ("the prefix in upper case: exit 2", ("Release: owner's word needed -- Q1 a/b was 1 (1.0.0) now 3 (1.1.0)\n").encode(), 2, "line 1"),
    ("no space after the prefix: exit 2", b"release:ok -- Q1 a/b not worse\n", 2, "line 1"),
    ("an empty file: exit 2, never ok", b"", 2, "no lines"),
    ("a BOM and nothing else: exit 2", BOM, 2, "no lines"),
    ("blank lines only: exit 2", b"\n  \n\n", 2, "no lines"),
    ("UTF-16 text: exit 2", (RC_OK + "\n").encode("utf-16"), 2, "RED"),
    ("10,000 lines with a wrong one at the end: exit 2 naming line 10001", ((RC_OK + "\n") * 10000 + "oops\n").encode(), 2, "line 10001"),
]


def sb_lines_case(tmp: Path, case) -> None:
    _name, data, want_code, words = case
    lines_file = tmp / "lines.txt"
    lines_file.write_bytes(data)
    code, printed, err = sb_cli("release-check", "--version", RC_VERSION, "--lines", lines_file, "--norms", tmp / "none.json")
    assert code == want_code and words in printed + err, (code, printed[-300:], err[:300])
    assert len(err) < 1000, "the refusal is not bounded"


SB_GROUPS =(("judgment shape (K1, 7.4, 7.10)", SB_JUDGMENT_CASES, sb_judgment_case), ("money row (X1)", SB_MONEY_CASES, sb_money_case),
             ("norm verdict (K2, 7.5)", SB_NORM_CASES, sb_norm_case), ("norms only tighten (K5)", SB_RATCHET_CASES, sb_ratchet_case),
             ("comparison (K7, 7.5, 7.7-7.9)", SB_COMPARE_CASES, sb_compare_case), ("previous file (K7, 7.7)", SB_PREVIOUS_CASES, sb_previous_case),
             ("assemble edges", SB_ASSEMBLE_CASES, sb_assemble_case), ("command line and findings (K4)", SB_CLI_CASES, sb_cli_case),
             ("bar price (N7, B1-E5/E6)", SB_BAR_CASES, sb_bar_case), ("release-check (K3, F7)", SB_RELEASE_CASES, sb_release_case),
             ("release-check OQ2 (ratcheted row, new bar)", SB_OQ2_CASES, sb_release_case),
             ("compare --release, one element one line (B1 table, range against range)", SB_REL_JUDGE_CASES, sb_rel_judge_case),
             ("compare --release, edges B2-E1..E9 and the direct road", SB_REL_CASES, sb_rel_case),
             ("norms only tighten: ratchet elements (K5)", SB_RATCHET_ELEMENT_CASES, sb_ratchet_element_case),
             ("norms/2 shape and conversion", SB_NORMS2_CASES, sb_norms2_case),
             ("a malformed ratchet element", SB_BAD_RATCHET_CASES, sb_bad_ratchet_case),
             ("a ratchet raise is scoped to its element; a pass to its factory model (B3, Q-b)", SB_RAISE_SCOPE_CASES, sb_raise_scope_case),
             ("release-check --lines is outside input (B4)", SB_LINES_CASES, sb_lines_case),
             ("the free arm's bar file writer (N9)", SB_BAR_FILE_CASES, sb_bar_file_case))


@_parametrize(SB_JUDGMENT_CASES)
def test_scoreboard_judgment_shape(tmp_path, case):
    sb_judgment_case(tmp_path, case)


@_parametrize(SB_MONEY_CASES)
def test_scoreboard_money_row(tmp_path, case):
    sb_money_case(tmp_path, case)


@_parametrize(SB_NORM_CASES)
def test_scoreboard_norm_verdict(tmp_path, case):
    sb_norm_case(tmp_path, case)


@_parametrize(SB_RATCHET_CASES)
def test_scoreboard_norms_only_tighten(tmp_path, case):
    sb_ratchet_case(tmp_path, case)


@_parametrize(SB_COMPARE_CASES)
def test_scoreboard_comparison(tmp_path, case):
    sb_compare_case(tmp_path, case)


@_parametrize(SB_PREVIOUS_CASES)
def test_scoreboard_previous_file(tmp_path, case):
    sb_previous_case(tmp_path, case)


@_parametrize(SB_ASSEMBLE_CASES)
def test_scoreboard_assemble_edges(tmp_path, case):
    sb_assemble_case(tmp_path, case)


@_parametrize(SB_CLI_CASES)
def test_scoreboard_command_line(tmp_path, case):
    sb_cli_case(tmp_path, case)


@_parametrize(SB_BAR_CASES)
def test_scoreboard_bar_price(tmp_path, case):
    sb_bar_case(tmp_path, case)


@_parametrize(SB_RELEASE_CASES)
def test_scoreboard_release_check(tmp_path, case):
    sb_release_case(tmp_path, case)


@_parametrize(SB_OQ2_CASES)
def test_scoreboard_release_check_oq2(tmp_path, case):
    sb_release_case(tmp_path, case)


@_parametrize(SB_REL_JUDGE_CASES)
def test_scoreboard_release_judge(tmp_path, case):
    sb_rel_judge_case(tmp_path, case)


@_parametrize(SB_REL_CASES)
def test_scoreboard_release_edges(tmp_path, case):
    sb_rel_case(tmp_path, case)


@_parametrize(SB_RATCHET_ELEMENT_CASES)
def test_scoreboard_ratchet_elements(tmp_path, case):
    sb_ratchet_element_case(tmp_path, case)


@_parametrize(SB_NORMS2_CASES)
def test_scoreboard_norms2(tmp_path, case):
    sb_norms2_case(tmp_path, case)


@_parametrize(SB_BAD_RATCHET_CASES)
def test_scoreboard_bad_ratchet(tmp_path, case):
    sb_bad_ratchet_case(tmp_path, case)


@_parametrize(SB_RAISE_SCOPE_CASES)
def test_scoreboard_raise_scope(tmp_path, case):
    sb_raise_scope_case(tmp_path, case)


@_parametrize(SB_LINES_CASES)
def test_scoreboard_release_lines_file(tmp_path, case):
    sb_lines_case(tmp_path, case)


@_parametrize(SB_BAR_FILE_CASES)
def test_scoreboard_bar_file(tmp_path, case):
    sb_bar_file_case(tmp_path, case)


def scoreboard_tests(root: Path) -> None:
    """The self-running form of the scoreboard tables: every case in its own folder, one `check` line each."""
    for number, (group, cases, runner) in enumerate(SB_GROUPS):
        for index, case in enumerate(cases):
            folder = root / f"sb-{number}-{index}"
            folder.mkdir(parents=True)
            try:
                runner(folder, case)
                check(f"scoreboard, {group}: {case[0]}", True)
            except Exception as exc:  # noqa: BLE001 - a failing case is a FAIL line, not a crash
                check(f"scoreboard, {group}: {case[0]}", False, f"{type(exc).__name__}: {str(exc)[:300]}")


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
        scoreboard_tests(root)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    bad = sum(1 for ok, _ in RESULTS if not ok)
    print(f"\n=== test_measurers: {len(RESULTS) - bad}/{len(RESULTS)} ok ===")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
