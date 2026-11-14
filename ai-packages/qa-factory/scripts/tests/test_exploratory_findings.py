"""test_exploratory_findings.py - the register writer and reader (P2 M1 step 1).

Run from the package root: python -B scripts/tests/test_exploratory_findings.py

Keys: K-M1-1 (every refusal, with an in-test negative control), K-M1-2, K-M1-2b, K-M1-3, K-M1-4, K-M1-4b, K-M1-4c.
Mutation -> killing key (named, not run; the batch canon decides): drop the required `why_not_a_bug` -> K-M1-1; id from the
count of VALID lines -> K-M1-4; skip the torn-tail newline -> K-M1-4b; allow `add` on a chained target -> K-M1-2b; check
excluded keys at the top level only -> K-M1-4c.
"""
import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from harness import PLUGIN_ROOT, check, check_eq, cleanup, finish, run_script, temp_project  # noqa: E402

import exploratory_findings as EF  # noqa: E402
import role_cli  # noqa: E402

PIPELINES = {
    "gate-a-open": {"gates": {"A": {}, "B": {}}, "stages": {"S8": {"status": "pending"}}},
    "between": {"gates": {"A": {"status": "approved"}, "B": {}}, "stages": {"S8": {"status": "pending"}}},
    "gate-b": {"gates": {"A": {"status": "approved"}, "B": {"status": "approved"}}, "stages": {}},
    "s8-done": {"gates": {"A": {"status": "approved"}, "B": {}}, "stages": {"S8": {"status": "done"}}},
}


def story(root: Path, pipeline="between") -> Path:
    task = root / "qa-factory" / "artifacts" / "TP1-TEST"
    (task / "work" / "evidence").mkdir(parents=True)
    for name in ("one", "two", "three"):
        (task / "work" / "evidence" / f"{name}.txt").write_text(f"the page said {name}\n", encoding="utf-8")
    set_pipeline(task, pipeline)
    return task


def set_pipeline(task: Path, pipeline) -> None:
    (task / "pipeline.json").write_text(json.dumps(PIPELINES[pipeline]) if isinstance(pipeline, str) else pipeline,
                                        encoding="utf-8")


def cli(*argv):
    """main() in-process: (code, stdout, stderr). SystemExit (argparse) is the exit code, as in a real run."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = EF.main([str(item) for item in argv])
        except SystemExit as stop:
            code = stop.code
    return code, out.getvalue(), err.getvalue()


def guarded(command, function):
    """A direct `append` call under the same guard the CLI uses: (code, stderr); code 0 and the id when it is accepted."""
    err = io.StringIO()
    result = []
    with contextlib.redirect_stderr(err):
        code = role_cli.run_guarded(command, lambda: result.append(function()) or 0)
    return code, err.getvalue(), (result[0] if result else None)


def add_args(task, **over):
    args = {"kind": "observation", "title": "page says one", "statement": "the page said one",
            "why-not-a-bug": "nothing in the requirements says what it should say", "evidence": "work/evidence/one.txt",
            "by": "S7-qa-failure-analyst-1"}
    args.update(over)
    out = ["add", "--task-root", task]
    for key, value in args.items():
        if value is not None:
            out += [f"--{key}", value]
    return out


def good_line(**over):
    line = {"op": "add", "kind": "observation", "title": "page says one", "statement": "the page said one",
            "why_not_a_bug": "nothing says what it should say", "evidence_refs": [{"path": "work/evidence/one.txt"}]}
    line.update(over)
    return {key: value for key, value in line.items() if value is not None}


def file_bytes(task: Path):
    path = EF.register_path(task)
    return path.read_bytes() if path.exists() else None


def refused(name, task, code, err, *needles, command="exploratory_findings.py add", before=None):
    first = err.splitlines()[0] if err else ""
    check(f"{name}: exit 2, first line `{command}: <problem>`", code == 2 and first.startswith(command + ": "), err[:300])
    for needle in needles:
        check(f"{name}: names {needle!r}", needle in err, err[:400])
    check(f"{name}: the file bytes are unchanged", file_bytes(task) == before)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def key_m1_1(root):
    task = story(root)
    # the refusals a CLI call can make, argument by argument
    code, out, err = cli(*add_args(task, **{"why-not-a-bug": ""}))
    refused("K-M1-1 empty why-not-a-bug (CLI)", task, code, err, "--why-not-a-bug is required: say why this is not a product bug")
    code, out, err = cli(*add_args(task, **{"why-not-a-bug": None}))
    refused("K-M1-1 absent why-not-a-bug (CLI)", task, code, err, "--why-not-a-bug is required")
    code, out, err = cli(*add_args(task, kind="unresolved_question"))
    refused("K-M1-1 unresolved_question without question", task, code, err, "an `unresolved_question` needs --question and --owner-role")
    code, out, err = cli(*add_args(task, kind="unresolved_question", question="what should it say?"))
    refused("K-M1-1 unresolved_question without owner-role", task, code, err, "--owner-role")
    code, out, err = cli(*add_args(task, kind="coverage_gap"))
    refused("K-M1-1 coverage_gap without prerequisite", task, code, err, "a `coverage_gap` needs --missing-prerequisite")
    code, out, err = cli(*add_args(task, evidence=None))
    refused("K-M1-1 no evidence", task, code, err, "--evidence is required: at least one file under the story folder")
    code, out, err = cli(*add_args(task, evidence="work/evidence/absent.txt"))
    refused("K-M1-1 evidence that is not a file", task, code, err, "is not a file under the task root")
    code, out, err = cli(*add_args(task, evidence="../outside.txt"))
    refused("K-M1-1 evidence that escapes the root", task, code, err, "escapes the task root")
    code, out, err = cli(*add_args(task, evidence=str(task / "work" / "evidence" / "one.txt")))
    refused("K-M1-1 absolute evidence path: evidence_ref_issue's own words", task, code, err, "is absolute; the task-relative spelling is work/evidence/one.txt")
    code, out, err = cli(*add_args(task, kind="bug"))
    refused("K-M1-1 closed list: kind", task, code, err, "`kind` is `bug`; expected one of observation, unresolved_question, coverage_gap")
    code, out, err = cli(*add_args(task, **{"oracle-status": "confirmed"}))
    refused("K-M1-1 oracle_status confirmed", task, code, err, "a confirmed oracle is a case check: it goes through the case and S7, not this register")
    code, out, err = cli(*add_args(task, **{"oracle-status": "maybe"}))
    refused("K-M1-1 closed list: oracle_status", task, code, err, "`oracle_status` is `maybe`; expected one of none, documented_text_only, owner_question")
    code, out, err = cli(*add_args(task, **{"verification-status": "reproduced"}))
    refused("K-M1-1 a status that needs captures, with no probe", task, code, err, "`verification_status` is `reproduced`", "investigation_probe.py record")
    code, out, err = cli(*add_args(task, **{"verification-status": "investigated"}))
    refused("K-M1-1 closed list: verification_status", task, code, err, "`verification_status` is `investigated`; expected one of")
    code, out, err = cli(*add_args(task, by=None))
    refused("K-M1-1 --by absent (F-6)", task, code, err, "--by names who records")
    code, out, err = cli(*add_args(task, by="  "))
    refused("K-M1-1 --by blank (F-6)", task, code, err, "--by names who records")
    code, out, err = cli(*add_args(task, by="code:investigation.project"))
    refused("K-M1-1 --by starting `code:` (F-6)", task, code, err, "--by names who records")
    for key in EF.EXCLUDED:
        code, out, err = cli(*add_args(task, **{key.replace("_", "-"): "x"}))
        refused(f"K-M1-1 excluded key {key} (CLI)", task, code, err, f"`{key}` is not a field of the findings register",
                "a product bug goes through S7 triage and gate B")
    code, out, err = cli(*add_args(task, title="", statement="x"))
    refused("K-M1-1 empty title", task, code, err, "--title is required")
    code, out, err = cli(*add_args(task, statement=" "))
    refused("K-M1-1 empty statement", task, code, err, "--statement is required")
    # the refusals only an in-process caller can reach, under the same guard
    command = "exploratory_findings.py add"
    for key, value in (("blocker", 1), ("_status", "active")):
        code, err, _ = guarded(command, lambda key=key, value=value: EF.append(task, good_line(**{key: value}), by="S7-1"))
        refused(f"K-M1-1 unknown key {key}", task, code, err, f"`{key}` is not a field of the findings register; its fields are")
    for key in EF.CODE_SET:
        code, err, _ = guarded(command, lambda key=key: EF.append(task, good_line(**{key: "x"}), by="S7-1"))
        refused(f"K-M1-1 code-set field {key}", task, code, err, f"`{key}` is set by code; leave it out")
    code, err, _ = guarded(command, lambda: EF.append(task, good_line(op="close"), by="S7-1"))
    refused("K-M1-1 closed list: op", task, code, err, "`op` is `close`; expected one of add, correct, withdraw")
    code, err, _ = guarded(command, lambda: EF.append(task, good_line(refs="R-1"), by="S7-1"))
    refused("K-M1-1 refs that is not a list", task, code, err, "`refs`")
    code, err, _ = guarded(command, lambda: EF.append(task, good_line(probe={"method": "ui", "runs": 2, "reproduced": 3,
                                                                              "safe_to_break": True}), by="S7-1"))
    refused("K-M1-1 safe_to_break set", task, code, err, "safe_to_break")
    code, err, _ = guarded(command, lambda: EF.append(task, good_line(why_not_a_bug=""), by="S7-1"))
    check("K-M1-1 the real module refuses the same line", code == 2 and "--why-not-a-bug is required" in err, err[:200])
    # a good call is accepted by the same CLI (the refusals above are not a broken harness)
    code, out, err = cli(*add_args(task))
    check_eq("K-M1-1 control: the clean call is accepted", (code, json.loads(out)["id"] if out else None), (0, "EX-1"))
    check_eq("K-M1-1 the accepted CLI call prints exactly one JSON object", len(out.strip().splitlines()), 1)
    line = json.loads(file_bytes(task).decode("utf-8").splitlines()[0])
    check_eq("K-M1-1 code-set fields on the written line", (line["evidence_kind"], line["recorded_by"], line["window"], line["probe"],
                                                           line["verification_status"], line["oracle_status"]),
             ("exploratory_probe", "S7-qa-failure-analyst-1", "s5-s8", None, "unverified", "none"))
    check("K-M1-1 the written ref carries the measured sha256",
          line["evidence_refs"] == [{"path": "work/evidence/one.txt", "sha256": sha((task / "work" / "evidence" / "one.txt").read_bytes())}])
    code, out, err = cli(*add_args(task, title="open question", kind="unresolved_question", question="what should it say?",
                                   **{"owner-role": "the product owner"}))
    row = json.loads(file_bytes(task).decode("utf-8").splitlines()[1])
    check_eq("K-M1-1 oracle default per kind: unresolved_question", (code, row["oracle_status"]), (0, "owner_question"))
    code, out, err = cli("add", "--task-root", task, "--no-such-flag", "1")
    check("K-M1-1 an argparse refusal has the one shape", code == 2 and err.splitlines()[1].startswith("exploratory_findings.py add: "), err[:300])


def key_m1_2(root):
    task = story(root)
    path = EF.register_path(task)
    check_eq("K-M1-2 no file: the empty register", EF.read(task), {"lines": [], "unreadable": [], "active": {}})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")
    check_eq("K-M1-2 a 0-byte file: the empty register", EF.read(task), {"lines": [], "unreadable": [], "active": {}})
    path.unlink()
    steps = [
        add_args(task, title="a", **{"target": "case-TC-1"}),
        add_args(task, title="b", **{"target": "case-TC-2"}),
        add_args(task, title="c", **{"target": "case-TC-3"}),
        ["correct", "--task-root", task, "--id", "EX-1", "--reason", "seen again", "--by", "S7-1", "--kind", "observation",
         "--title", "a2", "--statement", "the page said one twice", "--why-not-a-bug", "still no requirement",
         "--evidence", "work/evidence/two.txt"],
        ["withdraw", "--task-root", task, "--id", "EX-2", "--reason", "it was the test data", "--by", "S7-1"],
    ]
    for count, argv in enumerate(steps, 1):
        before = [line for line in (file_bytes(task) or b"").split(b"\n") if line]
        code, out, err = cli(*argv)
        after = [line for line in file_bytes(task).split(b"\n") if line]
        check_eq(f"K-M1-2 step {count}: accepted with id EX-{count}", (code, json.loads(out)["id"] if code == 0 else err[:200]), (0, f"EX-{count}"))
        check_eq(f"K-M1-2 step {count}: lines 1..{len(before)} are byte-identical (sha256)", [sha(line) for line in after[:len(before)]],
                 [sha(line) for line in before])
    state = EF.read(task)
    check_eq("K-M1-2 one active line per live target, none for the withdrawn one",
             {key: line["id"] for key, line in state["active"].items()}, {"case-TC-1": "EX-4", "case-TC-3": "EX-3"})
    by_id = {line["id"]: line for line in state["lines"]}
    check_eq("K-M1-2 the marks: add -> superseded by the correct, add -> withdrawn by the withdraw",
             (by_id["EX-1"]["_status"], by_id["EX-1"]["_next"], by_id["EX-1"]["_why"], by_id["EX-2"]["_status"], by_id["EX-2"]["_next"],
              by_id["EX-2"]["_why"], by_id["EX-5"]["_status"]),
             ("superseded", "EX-4", "seen again", "withdrawn", "EX-5", "it was the test data", "withdraw"))
    check("K-M1-2 the marks are never written", all("_status" not in json.loads(raw) for raw in file_bytes(task).decode("utf-8").splitlines()))
    check_eq("K-M1-2 a withdraw line carries the chain fields and nothing else (F-2)",
             sorted(json.loads(file_bytes(task).decode("utf-8").splitlines()[4])),
             sorted(["id", "op", "withdraws", "origin", "recorded_by", "recorded_at", "window"]))
    code, out, err = cli("list", "--task-root", task)
    listed = json.loads(out)
    check_eq("K-M1-2 list: one JSON object, active / superseded / unreadable",
             (code, [line["id"] for line in listed["active"]], [line["id"] for line in listed["superseded"]], listed["unreadable"]),
             (0, ["EX-3", "EX-4"], ["EX-1", "EX-2", "EX-5"], []))
    # a withdraw of a correct is allowed: add -> correct -> withdraw leaves no active line
    code, out, err = cli("withdraw", "--task-root", task, "--id", "EX-4", "--reason", "retracted", "--by", "S7-1")
    check_eq("K-M1-2 withdraw of a correct line is accepted", (code, json.loads(out)["id"]), (0, "EX-6"))
    check_eq("K-M1-2 ... and the target has no active line", sorted(EF.read(task)["active"]), ["case-TC-3"])
    code, out, err = cli("check", "--task-root", task)
    check_eq("K-M1-2 check on a sound register", (code, json.loads(out)), (0, {"ok": True, "lines": 6}))
    # a free finding (no --target) is its own chain, keyed by its id
    code, out, err = cli(*add_args(task, title="free"))
    code2, out2, err2 = cli("withdraw", "--task-root", task, "--id", "EX-7", "--reason", "gone", "--by", "S7-1")
    check_eq("K-M1-2 a free finding can be withdrawn; no origin on its line", (code, code2, "origin" in json.loads(out2 and file_bytes(task).decode("utf-8").splitlines()[7])),
             (0, 0, False))


def key_m1_2b(root):
    task = story(root)
    command = "exploratory_findings.py"
    code, out, err = cli(*add_args(task, **{"target": "case-TC-6"}))
    check_eq("K-M1-2b a code line for a target", (code, json.loads(out)["id"]), (0, "EX-1"))
    before = file_bytes(task)
    code, out, err = cli(*add_args(task, title="again", **{"target": "case-TC-6"}))
    refused("K-M1-2b add on a chained target", task, code, err, "target case-TC-6 already has line EX-1; use `correct` or `withdraw` of it",
            "exploratory_findings.py list --task-root", before=before)
    code, out, err = cli("correct", "--task-root", task, "--id", "EX-1", "--reason", "better words", "--by", "S7-1", "--kind", "observation",
                         "--title", "t2", "--statement", "s2", "--why-not-a-bug", "w2", "--evidence", "work/evidence/two.txt")
    check_eq("K-M1-2b a correct of the active line is accepted", (code, json.loads(out)["id"]), (0, "EX-2"))
    check_eq("K-M1-2b ... and the target still has ONE active line", {key: line["id"] for key, line in EF.read(task)["active"].items()},
             {"case-TC-6": "EX-2"})
    before = file_bytes(task)
    for name, argv, needle in (
        ("correct of a superseded line", ["correct", "--task-root", task, "--id", "EX-1", "--reason", "r", "--by", "S7-1", "--kind", "observation",
                                          "--title", "t", "--statement", "s", "--why-not-a-bug", "w", "--evidence", "work/evidence/one.txt"],
         "EX-1 is not an active line (unknown, superseded or withdrawn)"),
        ("withdraw of an unknown id", ["withdraw", "--task-root", task, "--id", "EX-9", "--reason", "r", "--by", "S7-1"], "EX-9 is not an active line"),
        ("withdraw of an empty id", ["withdraw", "--task-root", task, "--id", "", "--reason", "r", "--by", "S7-1"], "is not an active line"),
        ("withdraw without a reason", ["withdraw", "--task-root", task, "--id", "EX-2", "--by", "S7-1"], "--reason is required"),
    ):
        code, out, err = cli(*argv)
        refused(f"K-M1-2b {name}", task, code, err, needle, command=command + " " + argv[0], before=before)
    code, err, _ = guarded(command + " correct", lambda: EF.append(task, dict(good_line(op="correct", corrects={"id": "EX-2", "reason": "r"}),
                          origin={"dispatch": "S7-1", "target": "case-TC-7"}), by="S7-1"))
    refused("K-M1-2b a correction that changes the target", task, code, err, "EX-2 belongs to target case-TC-6; a correction keeps its target",
            command=command + " correct", before=before)
    code, out, err = cli("withdraw", "--task-root", task, "--id", "EX-2", "--reason", "gone", "--by", "S7-1")
    check_eq("K-M1-2b withdraw of the corrected line", (code, json.loads(out)["id"]), (0, "EX-3"))
    before = file_bytes(task)
    code, out, err = cli(*add_args(task, title="after withdraw", **{"target": "case-TC-6"}))
    refused("K-M1-2b add on a withdrawn target is refused too (the chain exists)", task, code, err, "target case-TC-6 already has line EX-3", before=before)
    code, out, err = cli("withdraw", "--task-root", task, "--id", "EX-3", "--reason", "twice", "--by", "S7-1")
    refused("K-M1-2b withdraw of a withdraw line", task, code, err, "EX-3 is not an active line", command=command + " withdraw", before=before)


def key_m1_3(root):
    expected = {"gate-a-open": "pre-gate-a", "between": "s5-s8", "gate-b": "post-s8", "s8-done": "post-s8"}
    for name, window in expected.items():
        task = story(root / name, name)
        code, out, err = cli(*add_args(task))
        line = json.loads(file_bytes(task).decode("utf-8").splitlines()[0]) if code == 0 else {}
        check_eq(f"K-M1-3 pipeline `{name}` -> window {window}", (code, line.get("window")), (0, window))
    task = story(root / "unreadable")
    for label, content in (("not JSON", "{broken"), ("a list", "[]")):
        (task / "pipeline.json").write_text(content, encoding="utf-8")
        code, out, err = cli(*add_args(task))
        refused(f"K-M1-3 pipeline.json that is {label} (F-3)", task, code, err,
                "the window of this finding cannot be read from pipeline.json; restore the file, then record")
    (task / "pipeline.json").unlink()
    code, out, err = cli(*add_args(task))
    refused("K-M1-3 no pipeline.json (F-3: never a guessed window)", task, code, err, "cannot be read from pipeline.json")


def key_m1_4(root):
    task = story(root)
    for flag in ("--runs", "--reproduced"):
        code, out, err = cli(*add_args(task), flag, "3")
        refused(f"K-M1-4 typed {flag}", task, code, err, "counts come from captures: `investigation_probe.py record`")
    code, out, err = cli(*add_args(task))
    check_eq("K-M1-4 first add", (code, json.loads(out)["id"]), (0, "EX-1"))
    path = EF.register_path(task)
    with open(path, "ab") as handle:
        handle.write(b"this line is damaged\n")
    state = EF.read(task)
    check_eq("K-M1-4 read: the damaged line 2 is in unreadable, not dropped", (len(state["lines"]), [n for n, _ in state["unreadable"]]), (1, [2]))
    code, out, err = cli(*add_args(task, title="third"))
    check_eq("K-M1-4 damaged line 2 -> the next id is EX-3", (code, json.loads(out)["id"]), (0, "EX-3"))
    code, out, err = cli("check", "--task-root", task)
    check("K-M1-4 check exits 2 naming line 2", code == 2 and "line 2:" in err and not json.loads(out)["ok"], err[:200])
    code, out, err = cli("list", "--task-root", task)
    check_eq("K-M1-4 list shows the damaged line", [item[0] for item in json.loads(out)["unreadable"]], [2])
    # a line whose id is not its physical line is damaged, and so is a wrong op
    path.write_bytes(b'{"id": "EX-9", "op": "add"}\n{"id": "EX-2", "op": "nope"}\n[1]\n\n')
    state = EF.read(task)
    check_eq("K-M1-4 id != physical line, unknown op, not an object, blank line: all four damaged, none readable",
             ([n for n, _ in state["unreadable"]], state["lines"], state["active"]), ([1, 2, 3, 4], [], {}))
    code, out, err = cli(*add_args(task))
    check_eq("K-M1-4 only damaged lines: the next id is EX-5 (the physical line)", (code, json.loads(out)["id"]), (0, "EX-5"))
    # a ref whose bytes changed: check names it, nothing is rewritten
    task2 = story(root / "edit")
    cli(*add_args(task2))
    kept = file_bytes(task2)
    (task2 / "work" / "evidence" / "one.txt").write_text("somebody edited this\n", encoding="utf-8")
    code, out, err = cli("check", "--task-root", task2)
    check("K-M1-4 an edited ref: check exits 2 in evidence_ref_issue's words", code == 2 and "EX-1:" in err and "stale sha256" in err, err[:300])
    check("K-M1-4 ... and the line is not rewritten", file_bytes(task2) == kept)
    code, out, err = cli("check", "--task-root", root / "no-such-folder")
    refused("K-M1-4 a task root that is not a folder", task2, code, err, "is not a folder", command="exploratory_findings.py check", before=kept)


def key_m1_4b(root):
    task = story(root)
    code, out, err = cli(*add_args(task))
    path = EF.register_path(task)
    with open(path, "ab") as handle:
        handle.write(b'{"id": "EX-2", "op": "add"')                     # a torn tail: no newline
    check("K-M1-4b the file does not end with a newline before the add", not file_bytes(task).endswith(b"\n"))
    code, out, err = cli(*add_args(task, title="after the tear"))
    data = file_bytes(task)
    check_eq("K-M1-4b the add is accepted as the next physical line", (code, json.loads(out)["id"]), (0, "EX-3"))
    check("K-M1-4b the file ends with a newline", data.endswith(b"\n"))
    state = EF.read(task)
    check_eq("K-M1-4b read: the fragment is ONE damaged line, plus the new line", ([n for n, _ in state["unreadable"]], [line["id"] for line in state["lines"]]),
             ([2], ["EX-1", "EX-3"]))
    check("K-M1-4b the new line is its own line (not merged into the fragment)", data.split(b"\n")[2].startswith(b'{"id": "EX-3"'))
    # a refused call on a torn tail repairs nothing
    task2 = story(root / "torn")
    cli(*add_args(task2))
    with open(EF.register_path(task2), "ab") as handle:
        handle.write(b"fragment")
    before = file_bytes(task2)
    code, out, err = cli(*add_args(task2, **{"why-not-a-bug": ""}))
    refused("K-M1-4b a refused call leaves a torn tail as it was", task2, code, err, "--why-not-a-bug is required", before=before)


def key_m1_4c(root):
    task = story(root)
    command = "exploratory_findings.py add"
    probe = {"method": "ui", "runs": 2, "reproduced": 1, "environment": "stand", "safe_to_break": None}
    code, err, ident = guarded(command, lambda: EF.append(task, good_line(probe=probe, verification_status="reproduced", origin={"dispatch": "S7-1", "target": "t1"}),
                                                          by="S7-1"))
    check_eq("K-M1-4c control: a clean probe line (the in-process M3 path) is accepted", (code, ident), (0, "EX-1"))
    before = file_bytes(task)
    for where, key, line in (
        ("probe.severity", "severity", good_line(probe=dict(probe, severity="high"), verification_status="reproduced")),
        ("evidence_refs[0].impact", "impact", good_line(evidence_refs=[{"path": "work/evidence/one.txt", "impact": "x"}])),
        ("origin.priority", "priority", good_line(origin={"dispatch": "S7-1", "target": "t2", "priority": 1})),
        ("a list inside a list", "bug", good_line(refs=[["R-1", {"bug": True}]])),
        ("withdraws.confirmation", "confirmation", {"op": "withdraw", "withdraws": {"id": "EX-1", "reason": "r", "confirmation": "yes"}}),
    ):
        code, err, _ = guarded(command, lambda line=line: EF.append(task, line, by="S7-1"))
        refused(f"K-M1-4c excluded key nested in {where}", task, code, err, f"`{key}` is not a field of the findings register",
                before=before)
    code, err, _ = guarded(command, lambda: EF.append(task, good_line(probe=dict(probe, runs=True)), by="S7-1"))
    refused("K-M1-4c a bool where a count belongs", task, code, err, "`probe.runs`", before=before)


def key_m1_smoke(root):
    task = story(root)
    done = run_script("exploratory_findings.py", *add_args(task))
    check_eq("smoke: the script run as a process prints one JSON object and exits 0", (done.returncode, json.loads(done.stdout)["id"]), (0, "EX-1"))
    done = run_script("exploratory_findings.py", "add", "--task-root", task)
    first = done.stderr.splitlines()[0] if done.stderr else ""
    check("smoke: a refusal as a process: exit 2, `exploratory_findings.py add: <problem>`, the shared door line",
          done.returncode == 2 and first.startswith("exploratory_findings.py add: ") and "if you cannot" in done.stderr, done.stderr[:300])
    done = run_script("exploratory_findings.py", "frob")
    check("smoke: an unknown subcommand is the script-level refusal", done.returncode == 2 and done.stderr.startswith("usage:")
          and "exploratory_findings.py: " in done.stderr, done.stderr[:300])


def key_fix1(root):
    """The fix round of t-109: B1 (exact flags, the story first), m1 (one command_of), m2 (one chain derivation), m5 (the
    shared appender)."""
    task = story(root)
    code, out, err = cli("list", "--task", task)
    check("B1 the abbreviation `--task` is refused (it was read as `--task-root`): exit 2, nothing on stdout, nothing written",
          code == 2 and out == "" and file_bytes(task) is None, f"{code} {err[:200]}")
    code, out, err = cli("list", "--task-root", root / "no-such-story")
    check("B1 a phantom story folder is the story driver's refusal, not a listing", code == 2 and out == "" and "names no story" in err,
          err[:300])
    check_eq("m1 command_of: the first subcommand word wins, else the script", (
        EF.command_of("x.py", ("a", "b"), ["--k", "b", "a"]), EF.command_of("x.py", ("a", "b"), ["--k", "v"])),
        ("x.py b", "x.py"))
    first = EF.append(task, good_line(origin={"dispatch": "D", "target": "t-1"}), by="D")
    second = EF.append(task, good_line(statement="the page said two", origin={"dispatch": "D", "target": "t-1"},
                                       corrects={"id": first, "reason": "read again"}, op="correct"), by="D")
    state = EF.read(task)
    check_eq("m2 chains_of(read lines): the lines of a target in file order, the one derivation",
             ({t: [line["id"] for line in chain] for t, chain in EF.chains_of(state["lines"]).items()}, EF.target_of(state["lines"][-1])),
             ({"t-1": [first, second]}, "t-1"))
    check_eq("m2 chains_of: a line with no target is in no chain", EF.chains_of([{"id": "EX-1"}, {"id": "EX-2", "origin": 5}]), {})
    # m5: the register is appended through hooklib.append_jsonl_line - a torn tail gets its newline, nothing is truncated
    path = EF.register_path(task)
    kept = path.read_bytes()
    path.write_bytes(kept.rstrip(b"\n"))
    third = EF.append(task, good_line(statement="the page said three", origin={"dispatch": "D", "target": "t-2"}), by="D")
    after = path.read_bytes()
    check("m5 a torn tail is repaired by one newline and the earlier bytes are untouched",
          after.startswith(kept.rstrip(b"\n") + b"\n") and after.count(b"\n") == kept.count(b"\n") + 1 and third == "EX-3",
          f"{third} {after[-120:]!r}")


def reads_of(name_pattern: str, skip: tuple) -> list:
    """The package scripts (not tests) whose text matches `name_pattern`, minus `skip` - the one scan K-M3 uses."""
    import re
    pattern = re.compile(name_pattern)
    return sorted(path.name for path in (PLUGIN_ROOT / "scripts").glob("*.py")
                  if path.name not in skip and pattern.search(path.read_text(encoding="utf-8")))


def key_m3(root):
    """K-M3 (AR-22): the fields the register records and nobody downstream reads are DECLARED terminal; every other field is read.
    KILLS: a terminal field that gains a reader without leaving the list, a declared field that is not a register field."""
    check_eq("K-M3 the three terminal fields", EF.TERMINAL_FIELDS, ("evidence_kind", "probe.environment", "probe.safe_to_break"))
    for name in EF.TERMINAL_FIELDS:
        head, _, leaf = name.partition(".")
        check(f"K-M3 {name} is a field of the register" + (" (a key of `probe`)" if leaf else ""),
              head in EF.FIELDS and (not leaf or leaf in EF.PROBE_FIELDS), name)
    producers = ("exploratory_findings.py", "investigation_probe.py")        # name the keys to WRITE them
    check_eq("K-M3 nothing downstream reads `evidence_kind`", reads_of(r"evidence_kind|EVIDENCE_KIND", producers), [])
    # `env_probe.py` and `manual_capture.py` (`fill-new-account`, `_stand_may_change`) read a STAND's `safe_to_break` (a config key of
    # the same name, environments[] row), not the register's probe field; `story_run.py` reads the stand's flag from the config through
    # `MC._stand_may_change`, `walk_pool.py` only names it in a docstring (the stand's flag is not consulted there)
    check_eq("K-M3 nothing downstream reads probe.safe_to_break from a register line", reads_of(r"safe_to_break", producers),
             ["driver_stage_s6.py", "env_probe.py", "manual_capture.py", "walk_pool.py"])
    check_eq("K-M3 nothing downstream reads probe.environment from a register line",
             reads_of(r"probe\w*\.get\(\s*[\"']environment[\"']|probe\w*\[\s*[\"']environment[\"']\s*\]", producers), [])
    # positive control, the same shape of scan: `owner_role` of a register line IS read by the report
    check("K-M3 POSITIVE CONTROL: the same scan finds `owner_role` in report_facts.py", "report_facts.py" in reads_of(r"owner_role", producers))


def key_m1_h(root):
    """K-M1-h (F2, AR-24/FR-58): `person_confirmed` is the person's word at gate B and nothing else. `confirmed` stays refused.
    KILLS (M-l): the `by` check dropped - a role confirming an oracle; `add` accepting the word."""
    task = story(root)
    target = {"dispatch": "S7-1", "target": "t"}
    code, err, _ = guarded("exploratory_findings.py add", lambda: EF.append(task, good_line(oracle_status="confirmed", origin=target), by="S7-1"))
    check("K-M1-h `confirmed` is still refused, with today's words", code == 2 and "a confirmed oracle is a case check" in err, err[:200])
    question = {"kind": "unresolved_question", "question": "Is it meant?", "owner_role": "the person", "oracle_status": "owner_question"}
    first = EF.append(task, good_line(origin=target, **question), by="S7-1")
    before = file_bytes(task)

    def fix(**over):
        line = good_line(op="correct", origin=target, corrects={"id": first, "reason": "confirmed as intended by the person at gate B"},
                         **dict(question, oracle_status="person_confirmed"))
        line.update(over)
        return line
    for name, line, by in (("by a role id", fix(), "S7-qa-failure-analyst-1"), ("on an add", good_line(oracle_status="person_confirmed"), "person"),
                           ("by a plain name", fix(), "x"), ("by a name that only starts like the person", fix(), "personal-1")):
        code, err, _ = guarded("exploratory_findings.py correct", lambda: EF.append(task, line, by=by))
        check(f"K-M1-h person_confirmed {name} is refused and nothing is written",
              code == 2 and "recorded only on a person's word" in err.replace("\n", " ") and file_bytes(task) == before, err[:300])
    check_eq("K-M1-h the role-facing list of oracles does not offer it", ("person_confirmed" in EF.ROLE_ORACLES, "person_confirmed" in EF.ORACLES), (False, True))
    code, err, _ = guarded("exploratory_findings.py correct", lambda: EF.append(task, fix(), by="person"))
    check("K-M1-h a person's correction is accepted", code == 0, err[:300])
    state = EF.read(task)
    line = next(iter(state["active"].values()))
    check_eq("K-M1-h and read() shows ONE active line for the target, person_confirmed", (len(state["active"]), line["oracle_status"]), (1, "person_confirmed"))
    code, err, _ = guarded("exploratory_findings.py correct", lambda: EF.append(task, fix(corrects={"id": line["id"], "reason": "again"}), by="person:Dev1"))
    check("K-M1-h `person:<name>` is a person too", code == 0, err[:300])


def critic_findings(task: Path) -> str:
    """The S4 case critic's findings file, a file under the story folder (the evidence a register-gap line cites)."""
    folder = task / "work" / "test-cases" / "TP1-TEST"
    folder.mkdir(parents=True)
    (folder / "critic-findings.md").write_text("R-2: the register states no boundary; the designer cannot close it\n", encoding="utf-8")
    return "work/test-cases/TP1-TEST/critic-findings.md"


def gap_line(evidence):
    return {"op": "add", "kind": "coverage_gap", "title": "R-2 has no boundary", "statement": "the register of R-2 names no boundary value",
            "why_not_a_bug": "the requirement is silent; nothing in the product contradicts it", "refs": ["R-2"],
            "missing_prerequisite": "the owner's word on the boundary of R-2", "evidence_refs": evidence}


def key_a3(root):
    """A3 (F3): the S4 case critic records a register remainder it found in the one findings register, and the test report's
    exploratory block reads it. X1 `s4-register-gap-line-accepted`, X2 `s4-register-gap-no-evidence-refused`."""
    import report_facts
    command = "exploratory_findings.py add"
    task = story(root / "x1", "gate-a-open")
    evidence = critic_findings(task)
    check_eq("X1 no register yet: the report reads none", report_facts._exploratory(task, {}), None)
    code, err, ident = guarded(command, lambda: EF.append(task, gap_line([{"path": evidence}]), by="S4-qa-case-critic-1"))
    check_eq("X1 s4-register-gap-line-accepted: an id", (code, ident), (0, "EX-1"))
    written = json.loads(file_bytes(task).decode("utf-8").splitlines()[0])
    check_eq("X1 the window comes from code: gate A unanswered -> pre-gate-a; recorded_by is the critic",
             (written["window"], written["recorded_by"], written["kind"]), ("pre-gate-a", "S4-qa-case-critic-1", "coverage_gap"))
    unknown: dict = {}
    got = report_facts._exploratory(task, unknown)
    check_eq("X1 the report's reader counts ONE gap and no finding", (got["formal"]["gaps"], got["formal"]["findings"], unknown), (1, 0, {}))
    task2 = story(root / "x2", "gate-a-open")
    critic_findings(task2)
    for label, refs in (("absent", None), ("empty", [])):
        line = gap_line(refs)
        if refs is None:
            del line["evidence_refs"]
        code, err, _ = guarded(command, lambda line=line: EF.append(task2, line, by="S4-qa-case-critic-1"))
        refused(f"X2 s4-register-gap-no-evidence-refused ({label})", task2, code, err, "--evidence")
    try:
        EF.append(task2, gap_line([]), by="S4-qa-case-critic-1")
        raised = ""
    except ValueError as exc:
        raised = str(exc)
    check("X2 the writer raises ValueError naming --evidence", "--evidence" in raised, raised)


GAP_PLACEHOLDER = ('  - title: "<the gap in one line>"\n    statement: "<the register line and what no requirement holds>"\n'
                   '    refs:\n      - <R-n or TC-n the gap stands against, or omit>\n    missing_prerequisite: "<what would close it>"\n')


def gap_row(title="R-2 has no boundary", statement="the register of R-2 names no boundary value", refs=("R-2",),
            missing="the owner's word on the boundary of R-2", extra=""):
    """One block-YAML row of a critic's `register_gaps` (what its values file produces); a `None` field is left out."""
    lines = [f'{key}: "{value}"' for key, value in (("title", title), ("statement", statement)) if value is not None]
    if refs:
        lines += ["refs:"] + [f"  - {ref}" for ref in refs]
    if missing is not None:
        lines.append(f'missing_prerequisite: "{missing}"')
    return "".join(("  - " if k == 0 else "    ") + line + "\n" for k, line in enumerate(lines)) + extra


def gap_form(task: Path, dispatch: str, section: str, verdict="ok") -> str:
    """Write `work/handoffs/<dispatch>.yaml` with the verdict and a `register_gaps` section (the text after the key); return its path."""
    path = task / "work" / "handoffs" / f"{dispatch}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"header:\n  verdict: {verdict}\nregister_gaps:{section}", encoding="utf-8")
    return f"work/handoffs/{dispatch}.yaml"


class GapStub:
    """The driver's own methods bound to a minimal object: `task_root`, the stages table, the dispatch the finish names and stubs for the
    two moves the call site must come before (the acceptance record and the verdict seam); no driver process, no subprocess."""
    def __init__(self, task: Path, dispatch: str):
        import driver_stage_plan as DSP
        self.task_root, self.task, self.last_dispatch, self.calls = task, "TP1-TEST", dispatch, []
        for name in ("register_gaps_write", "s4_critic_completion", "stage_acceptor", "stage_verdict_known", "case_verdict"):
            setattr(self, name, getattr(DSP.DriverStagePlan, name).__get__(self))
        self.stages = lambda: {"S4": {"acceptance_by": "qa-case-critic"}}
        self.stage_acceptance_write = lambda stage, dispatch: self.calls.append(("acceptance", dispatch))
        self.stage_review_exhausted = lambda *a, **k: self.calls.append(("seam", k.get("unreadable"))) or "seam"


def gap_write(task, dispatch):
    """`register_gaps_write` for `dispatch`: (printed text, refusal text or "", the Refusal)."""
    out, text, refusal = io.StringIO(), "", None
    with contextlib.redirect_stdout(out):
        try:
            GapStub(task, dispatch).register_gaps_write("S4", dispatch)
        except Exception as exc:  # noqa: BLE001 - the table names the refusal class below
            text, refusal = str(exc), exc
    return out.getvalue(), text, refusal


def register_lines(task: Path) -> list:
    return [json.loads(raw) for raw in (file_bytes(task) or b"").decode("utf-8").splitlines()]


def key_f7rc(root):
    """F7-RC: the S4 case critic's `register_gaps` rows are recorded by the driver (G1-G14, J1, A1, A4). One world per row id."""
    import report_facts
    import driver_stage_plan as DSP
    from driver_core import Refusal
    D = "S4-qa-case-critic-1"
    n = [0]

    def world(pipeline="gate-a-open"):
        n[0] += 1
        return story(root / f"w{n[0]}", pipeline)

    # G1 rows recorded (R1): kind, recorded_by, evidence is the form, why_not_a_bug is the constant, window pre-gate-a
    task = world()
    form = gap_form(task, D, "\n" + gap_row() + gap_row("Second gap", "a second sentence", ("R-3", "TC-1"), "an answer"))
    printed, text, _ = gap_write(task, D)
    lines = register_lines(task)
    check_eq("G1 two rows recorded, in form order", [(l["title"], l["kind"], l["refs"]) for l in lines],
             [("R-2 has no boundary", "coverage_gap", ["R-2"]), ("Second gap", "coverage_gap", ["R-3", "TC-1"])])
    check_eq("G1 recorded_by is the dispatch, the evidence is the form, the window comes from code, the why is the constant",
             {(l["recorded_by"], l["evidence_refs"][0]["path"], l["window"], l["why_not_a_bug"]) for l in lines},
             {(D, form, "pre-gate-a", DSP.REGISTER_GAP_WHY)})
    check("G1 the print names each row and its id", "register_gaps[0] recorded in the findings register as EX-1" in printed
          and "register_gaps[1] recorded in the findings register as EX-2" in printed, printed)
    check("G1 the why text holds no stage code and no role name", "S4" not in DSP.REGISTER_GAP_WHY and "qa-" not in DSP.REGISTER_GAP_WHY)
    # G2 absent / [] / null / a placeholder-only section -> nothing written, nothing printed (R3)
    for label, section in (("empty list", " []\n"), ("null", "\n"), ("placeholder row only", "\n" + GAP_PLACEHOLDER)):
        task = world()
        gap_form(task, D, section)
        printed, text, _ = gap_write(task, D)
        check_eq(f"G2 {label}: no file, no print, no refusal", (file_bytes(task), printed, text), (None, "", ""))
    task = world()
    path = task / "work" / "handoffs" / f"{D}.yaml"
    path.parent.mkdir(parents=True)
    path.write_text("header:\n  verdict: ok\n", encoding="utf-8")
    check_eq("G2 section absent (an older form): nothing", (gap_write(task, D)[0], file_bytes(task)), ("", None))
    # G3 the placeholder row is skipped, a real row after it keeps the form's own index (R4)
    task = world()
    gap_form(task, D, "\n" + GAP_PLACEHOLDER + gap_row())
    printed, _, _ = gap_write(task, D)
    check("G3 placeholder skipped, the real row recorded as register_gaps[1]", "register_gaps[1] recorded" in printed
          and len(register_lines(task)) == 1 and register_lines(task)[0]["title"] == "R-2 has no boundary", printed)
    # G4 a string / a mapping -> Refusal, register bytes unchanged (R5)
    for label, section in (("a word", " none\n"), ("a mapping", "\n  title: x\n"), ("a number", " 5\n")):
        task = world()
        gap_form(task, D, section)
        _, text, refusal = gap_write(task, D)
        check(f"G4 {label}: a Refusal naming the section and the expected list, nothing written",
              isinstance(refusal, Refusal) and "register_gaps: is " in text and "Expected a list of rows" in text and file_bytes(task) is None, text)
    # G5 two rows with shape problems -> ONE refusal naming both, nothing written (R6); the refusal carries the dispatch and the
    # conductor's door (A3); a key outside the template row is ignored with a print line, never refused (A9)
    task = world()
    gap_form(task, D, '\n  - title: 5\n    statement: "x"\n    missing_prerequisite: "y"\n  - title: "t"\n    statement: "s"\n    refs: oops\n'
                      '    missing_prerequisite: "m"\n')
    _, text, refusal = gap_write(task, D)
    check("G5 ONE refusal names both rows' problems", text.count("register_gaps[0].title: is int") == 1 and "register_gaps[1].refs: is str" in text, text)
    check("G5 the refusal carries the dispatch and a door the conductor can use", getattr(refusal, "dispatch", "") == D
          and f"handoff_check.py --file work/handoffs/{D}.yaml --set register_gaps[<i>].<field>=<value>" in text and "questions[]" in text
          and "retry the finish" in text, text)
    check("G5 nothing written, and the refusal is not routed by phrase (known False)", file_bytes(task) is None
          and getattr(refusal, "known", True) is False)
    task = world()
    gap_form(task, D, "\n" + gap_row(extra="    note: extra\n"))
    printed, text, _ = gap_write(task, D)
    check("G5 a key outside the row is ignored with a print line, the row recorded", text == "" and len(register_lines(task)) == 1
          and "carries `note`, not a field of the row; ignored" in printed, printed + text)
    # G6 a placeholder field is absent -> the writer's own refusal names the flag and the row index (R7, R8)
    task = world()
    gap_form(task, D, '\n  - title: "t"\n    statement: "s"\n    missing_prerequisite: "<what would close it>"\n')
    _, text, refusal = gap_write(task, D)
    check("G6 the writer's refusal names --missing-prerequisite, the row index, the form and the door", "register_gaps[0]" in text
          and "--missing-prerequisite" in text and f"work/handoffs/{D}.yaml" in text and "delete the row" in text
          and file_bytes(task) is None and getattr(refusal, "dispatch", "") == D, text)
    # G7 row 0 ok, row 1 refused -> row 0 written, the refusal names row 1; after the fix the retry writes ONLY row 1 (R8, D.4)
    task = world()
    gap_form(task, D, "\n" + gap_row() + gap_row("Bad", "a sentence", ("R-4",), None))
    _, text, _ = gap_write(task, D)
    check("G7 row 0 stays written, the refusal names row 1", len(register_lines(task)) == 1 and "register_gaps[1]" in text, text)
    gap_form(task, D, "\n" + gap_row() + gap_row("Bad", "a sentence", ("R-4",), "now fixed"))
    printed, text, _ = gap_write(task, D)
    check("G7 the retry skips row 0 as recorded already and writes only row 1", text == "" and len(register_lines(task)) == 2
          and "register_gaps[0] of" in printed and "is recorded already as EX-1" in printed and "register_gaps[1] recorded" in printed, printed + text)
    # G8 the same form twice (a repeated finish, the recovery road) -> one line per row
    task = world()
    gap_form(task, D, "\n" + gap_row())
    gap_write(task, D)
    first = file_bytes(task)
    printed, _, _ = gap_write(task, D)
    check("G8 the second call writes nothing: the register bytes are equal, the row skipped", file_bytes(task) == first
          and "recorded already as EX-1" in printed)
    # G9 a repair round's new form: one equal row, one new -> only the new row is recorded (R11)
    gap_form(task, "S4-qa-case-critic-2", "\n" + gap_row() + gap_row("Third", "a third sentence", ("R-5",), "an answer"))
    gap_write(task, "S4-qa-case-critic-2")
    check_eq("G9 only the new row was added, by the later dispatch", [(l["title"], l["recorded_by"]) for l in register_lines(task)],
             [("R-2 has no boundary", D), ("Third", "S4-qa-case-critic-2")])
    # G10 a reworded row is a second line (R12): duplicate allowed, loss never
    gap_form(task, "S4-qa-case-critic-3", "\n" + gap_row(statement="the register of R-2 names no boundary value at all"))
    gap_write(task, "S4-qa-case-critic-3")
    check_eq("G10 the reworded row is a second line", len(register_lines(task)), 3)
    # G11 the register path is a directory -> the read gives the empty register, the append raises -> a refusal naming the register (R10, A5)
    task = world()
    (task / "work" / "exploratory-findings.jsonl").mkdir()
    gap_form(task, D, "\n" + gap_row())
    _, text, refusal = gap_write(task, D)
    check("G11 a Refusal that names work/exploratory-findings.jsonl and the form, with the dispatch", isinstance(refusal, Refusal)
          and "work/exploratory-findings.jsonl" in text and f"work/handoffs/{D}.yaml" in text and getattr(refusal, "dispatch", "") == D, text)
    # G12 after gate A answered -> the window is s5-s8 (R14)
    task = world("between")
    gap_form(task, D, "\n" + gap_row())
    gap_write(task, D)
    check_eq("G12 window s5-s8", register_lines(task)[0]["window"], "s5-s8")
    # G13 the unknown verdict word and one gap row: the line is written, THEN the seam stub is called (positional invariant, R2)
    task = world()
    gap_form(task, D, "\n" + gap_row(), verdict="wibble")
    stub = GapStub(task, D)
    with contextlib.redirect_stdout(io.StringIO()):
        answer = stub.s4_critic_completion(["TC-1"], 1, 3, dispatch_id=D)("digest")
    check_eq("G13 the gap line is written, the seam stub called once (unreadable), the acceptance record not written",
             (len(register_lines(task)), answer, stub.calls), (1, "seam", [("seam", True)]))
    # G14 a refused gap row: a Refusal, and neither the acceptance record nor the seam was reached
    task = world()
    gap_form(task, D, "\n" + gap_row(None, "s", (), "m"))
    stub = GapStub(task, D)
    try:
        stub.s4_critic_completion(["TC-1"], 1, 3, dispatch_id=D)("digest")
        refused_at_call = False
    except Refusal:
        refused_at_call = True
    check_eq("G14 a refused row stops the finish before the record and the seam", (refused_at_call, stub.calls, file_bytes(task)), (True, [], None))
    # G15 a finish with no dispatch id records nothing and goes on to the seam as before (R13)
    task = world()
    stub = GapStub(task, "")
    with contextlib.redirect_stdout(io.StringIO()):
        answer = stub.s4_critic_completion(["TC-1"], 1, 3, dispatch_id="")("digest")
    check_eq("G15 no dispatch id: the seam, no register", (answer, stub.calls, file_bytes(task)), ("seam", [("seam", True)], None))
    # J1 form -> register -> the report's reader counts one gap and its text holds the statement and `missing:`
    task = world()
    gap_form(task, D, "\n" + gap_row())
    gap_write(task, D)
    unknown: dict = {}
    got = report_facts._exploratory(task, unknown)
    text = report_facts._r_exploratory({"exploratory": got, "unknown": unknown, "gate_b": {}})
    check_eq("J1 the report's reader counts ONE gap and no finding", (got["formal"]["gaps"], got["formal"]["findings"], unknown), (1, 0, {}))
    check("J1 the report text holds the statement and `missing:` with the critic's words",
          "the register of R-2 names no boundary value" in text and "missing: the owner's word on the boundary of R-2" in text, text)
    # A1 the role's copy holds `register_gaps: []`; the exit check of a form with one filled row and no refs raises no problem of this
    # section, while the untouched sample row of the raw template does (the control that the check would have refused it)
    import handoff
    import handoff_check
    import handoff_init
    name = "s4-case-critic-to-designer"
    raw = handoff_init.fill_head((handoff.CONTRACTS / f"{name}.yaml").read_text(encoding="utf-8"), task="QA-1", dispatch=D,
                                 role="qa-case-critic", stage="S4", scope="R-1")
    emptied = handoff_init.empty_optional_lists(raw, name)
    check_eq("A1 the role's copy holds register_gaps: []", handoff.parse(emptied).data.get("register_gaps"), [])
    art = handoff_check.Artifacts(root)
    mine = lambda text: [p.path for p in handoff_check.check(handoff.parse(text), name, art)[2] if p.path.startswith("register_gaps")]
    check("A1 control: the untouched sample row of the raw template is refused as not filled", mine(raw) != [], str(mine(raw)))
    check_eq("A1 the emptied copy raises no problem of its own", mine(emptied), [])
    out, applied, problems, _notes = handoff_check.apply_values(handoff.parse(emptied), name, [
        ("register_gaps[0].title", "R-2 has no boundary", 0, ""), ("register_gaps[0].statement", "no boundary", 0, ""),
        ("register_gaps[0].missing_prerequisite", "the owner's word", 0, "")])
    check_eq("A1 a values file opens row 0 of the emptied section", (applied, [p.path for p in problems]), (3, []))
    check_eq("A1 a filled row with no refs gives no register_gaps problem at the exit check", mine(out.text()), [])
    # A4 a second `handoff_check --fix` over the unchanged form leaves equal bytes
    task = world()
    fixed = task / "work" / "handoffs" / f"{D}.yaml"
    fixed.parent.mkdir(parents=True)
    fixed.write_text(out.text(), encoding="utf-8")
    argv = ("handoff_check.py", "--file", str(fixed), "--task", "TP1-TEST", "--task-root", str(task), "--fix")
    run_script(*argv, cwd=root)
    after_first = fixed.read_bytes()
    run_script(*argv, cwd=root)
    check("A4 the second --fix leaves the form's bytes equal to the first", fixed.read_bytes() == after_first)


def main():
    for key in (key_m1_1, key_m1_2, key_m1_2b, key_m1_3, key_m1_4, key_m1_4b, key_m1_4c, key_m1_smoke, key_fix1, key_m3, key_m1_h, key_a3, key_f7rc):
        root = temp_project()
        try:
            key(root)
        finally:
            cleanup(root)
    finish("test_exploratory_findings")


if __name__ == "__main__":
    main()
