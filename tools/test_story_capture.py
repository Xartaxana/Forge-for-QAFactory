"""tools/story_capture.py on a synthetic six-event root: refusal by rule id, a clean capture, not-synthetic, target exists, expected."""
import json
import re
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import story_capture as sc  # noqa: E402

PACKAGE = Path(__file__).resolve().parent.parent / "ai-packages" / "qa-factory"
CYR = "".join(map(chr, (0x43f, 0x440, 0x438, 0x432, 0x435, 0x442)))    # a Russian word, written by code point
NAME = "Dev1"


def make_root(base, task="LOCAL-1", words=None, actions=("approve", "approve")):
    sys.path.insert(0, str(PACKAGE / "scripts"))
    from event_store import content_hash
    root = base / task
    (root / "state" / "words").mkdir(parents=True)
    (root / "work").mkdir()
    rows = [("stage_transition", {"stage": "S0", "status": "done", "digest": "ok " + CYR}),
            ("dispatch", {"id": "S1-scout-1", "stage": "S1"}),
            ("accept", {"id": "S1-scout-1", "status": "accepted", "evidence_refs": [{"path": "work/context.json"}]}),
            ("decision", {"gate": "A", "action": actions[0], "status": "approved", "authorization_source": r"D:/" r"AI/Factory/testproject1-dev-010\x"}),   # the stand root (sc.STAND), split so no line names a machine path
            ("checkpoint", {"stage": "S1", "status": "blocked", "reason": "waiting"}),
            ("decision", {"gate": "B", "action": actions[1], "status": "approved", "authorization_source": CYR})]
    previous, lines = "", []
    for n, (kind, payload) in enumerate(rows, 1):
        e = {"task_id": task, "sequence": n, "previous_hash": previous, "type": kind, "payload": payload}
        previous = e["event_hash"] = content_hash(e)
        lines.append(json.dumps(e, ensure_ascii=False))
    (root / "state" / "events.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (root / "state" / "words" / "gate-a-decision.txt").write_text(words or "go on\n", encoding="utf-8")
    (root / "work" / "delivery-summary.json").write_text('{"delivery_verdict": "no"}', encoding="utf-8")
    return root


def run(root, base, story_id="s1", *extra):
    pkg = base / "pkg"
    (pkg / "scripts").mkdir(parents=True, exist_ok=True)
    shutil.copy(PACKAGE / "scripts" / "event_store.py", pkg / "scripts" / "event_store.py")
    (pkg / "scripts" / "tests").mkdir(exist_ok=True)    # what `expected` imports by path: the walker, its harness, the form parser
    for name in ("tests/scenario_walk.py", "tests/harness.py", "handoff.py"):
        shutil.copy(PACKAGE / "scripts" / name, pkg / "scripts" / name)
    return sc.main(["capture", "--source", str(root), "--id", story_id, "--package", str(pkg), *extra]), pkg


def story_text(pkg, story_id):
    root = pkg.joinpath(*sc.STORIES, story_id)
    return {p.relative_to(root).as_posix(): p.read_text(encoding="utf-8") for p in root.rglob("*") if p.is_file()}


def test_class1_scratch_is_named_after_the_task_and_removed(tmp_path, monkeypatch):
    root = make_root(tmp_path / "src", task="CART-1")
    (root / "work" / "test-plan.json").write_text("{}", encoding="utf-8")
    names = []

    class FakeController:
        def __init__(self, target):
            names.append(Path(target).name)

        def gate_inputs(self):
            return {"plan_content_hash": "h1"}

    monkeypatch.setitem(sys.modules, "controller", type(sys)("controller"))
    sys.modules["controller"].Controller = FakeController
    code, pkg = run(root, tmp_path, "c1")
    assert code == 0 and names == ["CART-1"]
    gate_a = [json.loads(x) for x in (pkg.joinpath(*sc.STORIES, "c1") / "state" / "events.jsonl").read_text().splitlines()]
    assert [e for e in gate_a if e["type"] == "decision"][0]["payload"]["plan_content_hash"] == "h1"
    assert not list(pkg.joinpath(*sc.STORIES).glob("*.partial")) and not list(Path(tempfile_dir()).glob("story-capture-*"))
    # a refused capture leaves nothing in the target
    bad = make_root(tmp_path / "bad", task="CART-2", words="dev1\n")
    assert run(bad, tmp_path, "c2")[0] == 1
    assert not pkg.joinpath(*sc.STORIES, "c2").exists() and not list(Path(tempfile_dir()).glob("story-capture-*"))


def tempfile_dir():
    import tempfile
    return tempfile.gettempdir()


def test_class2_3_foreign_paths_and_scan_on_result(tmp_path):
    root = make_root(tmp_path / "src")
    (root / "work" / "p.json").write_text(json.dumps(
        {"a": "C:\\Work\\Other\\proj\\x.py", "b": "c:/work/other/proj/y.py", "c": "D:\\Else\\z\\q\\w",
         "d": "C:\\Users\\dev1\\AppData\\python.exe", "e": "/home/bob/proj/f", "f": "/c/" + "AI/Factory/t/g"}), encoding="utf-8")
    (root / "work" / "t.md").write_text("see C:\\\\Work\\\\Other\\\\proj\\\\k and C:\\Users\\dev1\\r\n", encoding="utf-8")
    code, pkg = run(root, tmp_path, "f1")
    assert code == 0    # the person name sat only in a home path that the replacement removed: not a hit
    files = story_text(pkg, "f1")
    data = json.loads(files["work/p.json"])    # still valid JSON
    assert data["a"] == "<path-1>\\x.py" and data["b"] == "<path-1>/y.py" and data["c"] == "<path-2>\\w"
    assert data["d"] == "<home>\\AppData\\python.exe" and data["e"] == "<home>/proj/f" and data["f"].startswith("<path-3>")
    assert "<path-1>" in files["work/t.md"] and "<home>" in files["work/t.md"]
    assert "3 of them" in files["README.txt"]
    assert "Other" not in "".join(files.values()) and "bob" not in "".join(files.values())


def test_class4_rewrites_counted_and_residue_refused(tmp_path, capsys):
    root = make_root(tmp_path / "src")
    (root / "work" / "h.yaml").write_text(
        "# cost on ACME-13797 and XPANBFLFA-140, again ACME-13797 (LOCAL-1 stays), L126-128 is a range\n"
        "url: https://example.org/browse/CART-1 and %s runs\n" % ("Code" "Mie"), encoding="utf-8")   # the product word, assembled
    (root / "work" / "r.json").write_text('{"x": "ACME-13797 \\"q\\""}', encoding="utf-8")
    code, pkg = run(root, tmp_path, "w1")
    assert code == 0
    files = story_text(pkg, "w1")
    assert files["work/h.yaml"] == ("# cost on REF-1 and REF-2, again REF-1 (LOCAL-1 stays), L126-128 is a range\n"
                                    "url: https://example.invalid/1/browse/CART-1 and product runs\n")
    assert json.loads(files["work/r.json"]) == {"x": 'REF-1 "q"'}    # the same key, the same REF, across files
    readme = files["README.txt"]
    assert "changed: ticket-key x 4 (2 distinct)" in readme and "changed: example-url x 1" in readme and "changed: product-word x 1" in readme
    # residue of a scan rule after the rewrites is still a refusal with file:line and the rule id
    (root / "work" / "h.yaml").write_text("clone from githost now\n", encoding="utf-8")
    assert run(root, tmp_path, "w2")[0] == 1
    assert "work/h.yaml:1: rule githost" in capsys.readouterr().err
    # the task's own internal key is still not synthetic
    assert run(make_root(tmp_path / "tp3", "EP" "MXX-5"), tmp_path, "w3")[0] == 1


def test_recorded_hash_follows_a_rewritten_file(tmp_path):
    import hashlib
    root = make_root(tmp_path / "src")
    snap = '{"t": "see https://example.org/browse/X"}'
    (root / "work" / "snap.json").write_text(snap, encoding="utf-8")
    old = hashlib.sha256(snap.encode()).hexdigest()
    (root / "work" / "inv.json").write_text(json.dumps({"content_hash": old}), encoding="utf-8")
    code, pkg = run(root, tmp_path, "h1")
    assert code == 0
    files = story_text(pkg, "h1")
    assert json.loads(files["work/inv.json"])["content_hash"] == hashlib.sha256(files["work/snap.json"].encode()).hexdigest() != old
    assert "1 replacements" in files["README.txt"]


def test_bare_example_host_and_package_prefix(tmp_path):
    import hashlib
    root = make_root(tmp_path / "src")
    snap = "on example.com and git.example.com, again EXAMPLE.com; class com.example.jira.tm.X; https://a.example.com/p"
    (root / "work" / "n.txt").write_text(snap, encoding="utf-8")
    (root / "work" / "inv.json").write_text(json.dumps({"content_hash": hashlib.sha256(snap.encode()).hexdigest()}), encoding="utf-8")
    code, pkg = run(root, tmp_path, "e1")
    assert code == 0
    files = story_text(pkg, "e1")
    assert files["work/n.txt"] == ("on host-1.example.invalid and host-2.example.invalid, again host-1.example.invalid; "
                                   "class com.example.jira.tm.X; https://example.invalid/1")
    assert json.loads(files["work/inv.json"])["content_hash"] == hashlib.sha256(files["work/n.txt"].encode()).hexdigest()
    assert "changed: example-host x 3 (2 distinct)" in files["README.txt"] and "changed: example-package x 1" in files["README.txt"]


def test_binary_still_refused(tmp_path, capsys):
    root = make_root(tmp_path / "src")
    (root / "work" / "b.bin").write_bytes(b"\xff\xfe\x00\x01")
    assert run(root, tmp_path, "b1")[0] == 1 and "rule binary" in capsys.readouterr().err
    assert run(root, tmp_path, "b2", "--drop", "*.bin")[0] == 0


def test_capture_table(tmp_path, capsys):
    bad = make_root(tmp_path / "bad", words="go on, %s\n" % NAME)
    assert run(bad, tmp_path)[0] == 1
    err = capsys.readouterr().err
    assert "state/words/gate-a-decision.txt:1: rule person" in err and "--drop" in err
    code, pkg = run(bad, tmp_path, "s1", "--drop", "state/words/*")    # the door: drop the file
    assert code == 0 and "state/words/gate-a-decision.txt" in (pkg.joinpath(*sc.STORIES, "s1") / "README.txt").read_text()
    ok = make_root(tmp_path / "ok")
    (ok / "work" / "handoffs").mkdir()
    (ok / "work" / "handoffs" / "S1-scout-1.yaml").write_text(FORM, encoding="utf-8")
    assert run(ok, tmp_path, "s2", "--cut-after-seq", "6")[0] == 0
    story = pkg.joinpath(*sc.STORIES, "s2")
    text = "".join(p.read_text(encoding="utf-8") for p in story.rglob("*") if p.is_file())
    assert not re.search("[\u0400-\u04ff]", text) and "C:\\AI" not in text and "<stand>" in text and "privet" in text
    from event_store import content_hash
    previous = ""
    for line in (story / "state" / "events.jsonl").read_text().splitlines():
        e = json.loads(line)
        assert e["previous_hash"] == previous
        previous = e.pop("event_hash")
        assert content_hash(e) == previous
    assert json.loads((story / "story.json").read_text())["synthetic"] is True
    assert run(make_root(tmp_path / "ok2"), tmp_path, "s2")[0] == 1 and "exists" in capsys.readouterr().err
    assert run(make_root(tmp_path / "tp3", "EP" "MXX-1"), tmp_path, "s3")[0] == 1
    assert "not synthetic: internal ticket key" in capsys.readouterr().err
    assert sc.main(["expected", "--id", "s2", "--package", str(pkg)]) == 0
    stages = json.loads((story / "expected.json").read_text())["stages"]
    # item 2: handed = what the FORM names as required (not the accept's evidence_refs `work/other.json`; the optional input is out)
    assert stages["S1"]["outcome"] == "accepted" and stages["S1"]["handed"] == ["work/context.json", "work/<area>/t.md"]
    assert stages["gateA"]["decision"] == "approve" and "gate-a-decision.txt" in stages["gateA"]["words"]
    assert stages["S8"]["delivery"] == "no" and stages["S1"]["refused"][0]["status"] == "blocked"
    not_walked = {n["stage"] for n in json.loads((story / "story.json").read_text())["not_walked"]}
    assert "S4" in not_walked and "S1" not in not_walked


FORM = ("inputs:\n  - path: work/context.json\n    what: the bundle\n    required: true\n"
        "  - path: work/<area>/t.md\n    what: a template\n    required: true\n"
        "  - path: work/optional.json\n    what: not required\n    required: false\n")


def test_expected_vocabulary_and_form_inputs(tmp_path):
    """Items 1 and 2: the decision is written in the walker's token, the event's action kept apart, the question kind in the
    walker's form, `handed` from the form; a form with no required inputs gives []; an unknown action is refused by name."""
    root = make_root(tmp_path / "v", actions=("approve_plan_and_cases", "approve_delivery"))
    (root / "state" / "driver-questions.jsonl").write_text(
        json.dumps({"kind": "gate_A"}) + "\n" + json.dumps({"kind": "gate_b"}) + "\n" + json.dumps({"kind": "other"}) + "\n", encoding="utf-8")
    (root / "work" / "handoffs").mkdir()
    (root / "work" / "handoffs" / "S1-scout-1.yaml").write_text(FORM, encoding="utf-8")
    code, pkg = run(root, tmp_path, "v1")
    assert code == 0 and sc.main(["expected", "--id", "v1", "--package", str(pkg)]) == 0
    stages = json.loads((pkg.joinpath(*sc.STORIES, "v1") / "expected.json").read_text())["stages"]
    walker = sc.load_walker(pkg)
    assert (stages["gateA"]["decision"], stages["gateA"]["recorded_action"]) == ("approve", "approve_plan_and_cases")
    assert (stages["gateB"]["decision"], stages["gateB"]["recorded_action"]) == ("approve", "approve_delivery")
    assert stages["gateA"]["question_kind"] == "gate_a" == walker.QUESTION_KINDS["gate_a"] and stages["gateB"]["question_kind"] == "gate_b"
    assert stages["S1"]["handed"] == ["work/context.json", "work/<area>/t.md"]
    assert "options" not in stages["gateA"] and "options" not in stages["gateB"]    # item 3: the carrier recorded no options: no key
    assert walker.decision_of("approve_delivery", "approved") == "approve" and walker.decision_of("approve", "rejected") == "refused"
    # a form with no required inputs: handed is an empty list (the walker passes it with a NOTE)
    (root / "work" / "handoffs" / "S1-scout-1.yaml").write_text("inputs:\n  - path: work/x.json\n    required: false\n", encoding="utf-8")
    assert run(root, tmp_path, "v2")[0] == 0 and sc.main(["expected", "--id", "v2", "--package", str(pkg)]) == 0
    assert json.loads((pkg.joinpath(*sc.STORIES, "v2") / "expected.json").read_text())["stages"]["S1"]["handed"] == []
    # an action the walker's mapping does not know: refused naming the action and the event seq; no expected.json is written
    odd = make_root(tmp_path / "o", actions=("reopen_everything", "approve"))
    assert run(odd, tmp_path, "v3")[0] == 0
    try:
        sc.expected("v3", pkg)
        refused = ""
    except sc.Refusal as exc:
        refused = str(exc)
    assert "reopen_everything" in refused and "seq 4" in refused and "GATE_ACTIONS" in refused
    assert not (pkg.joinpath(*sc.STORIES, "v3") / "expected.json").exists()


def test_expected_writes_options_when_the_carrier_records_them(tmp_path):
    """Item 3: a question row that carries `options` gives the gate an `options` list (sorted); a row of the kind alone gives no key."""
    root = make_root(tmp_path / "o", actions=("approve_plan_and_cases", "approve_delivery"))
    (root / "state" / "driver-questions.jsonl").write_text(
        json.dumps({"kind": "gate_A", "options": ["b", "a"]}) + "\n" + json.dumps({"kind": "gate_B"}) + "\n", encoding="utf-8")
    code, pkg = run(root, tmp_path, "o1")
    assert code == 0 and sc.main(["expected", "--id", "o1", "--package", str(pkg)]) == 0
    stages = json.loads((pkg.joinpath(*sc.STORIES, "o1") / "expected.json").read_text())["stages"]
    assert stages["gateA"]["options"] == ["a", "b"] and "options" not in stages["gateB"] and stages["gateB"]["question_kind"] == "gate_b"


def test_not_walked_is_one_row_per_stage_facet_reason(tmp_path):
    """Item 3: five dropped files of one dispatch are ONE row with a count of 5 and three sample paths."""
    root = make_root(tmp_path / "n")
    for n in range(5):
        (root / "work" / "briefs").mkdir(exist_ok=True)
        (root / "work" / "briefs" / ("S1-scout-1-%d.md" % n)).write_text("b%d\n" % n, encoding="utf-8")
    code, pkg = run(root, tmp_path, "n1", "--drop", "work/briefs/*")
    assert code == 0 and sc.main(["expected", "--id", "n1", "--package", str(pkg)]) == 0
    rows = [r for r in json.loads((pkg.joinpath(*sc.STORIES, "n1") / "story.json").read_text())["not_walked"] if r["stage"] == "S1"]
    assert len(rows) == 1 and rows[0]["facet"] == "digest" and rows[0]["count"] == 5 and len(rows[0]["samples"]) == 3


def test_rerun_keeps_amendments_and_lead_not_walked_rows(tmp_path):
    """TD-15.4 item 3: a re-run keeps `amendments` of expected.json and the `by: lead` rows of not_walked; the rest is rewritten."""
    root = make_root(tmp_path / "k")
    code, pkg = run(root, tmp_path, "k1")
    assert code == 0 and sc.main(["expected", "--id", "k1", "--package", str(pkg)]) == 0
    folder = pkg.joinpath(*sc.STORIES, "k1")
    row = {"stage": "S2", "field": "outcome", "recorded": "accepted", "expected": "refused", "why": "w", "ref": "r", "accepted_by": "Lead"}
    exp = json.loads((folder / "expected.json").read_text())
    exp["amendments"], exp["stages"]["S1"]["outcome"] = [row], "hand-edited"
    (folder / "expected.json").write_text(json.dumps(exp), encoding="utf-8")
    story = json.loads((folder / "story.json").read_text())
    lead = {"stage": "S9", "facet": "accepted", "why": "by hand", "by": "lead"}
    story["not_walked"] = story["not_walked"] + [lead, {"stage": "S8", "facet": "accepted", "why": "by hand, no key"}]
    (folder / "story.json").write_text(json.dumps(story), encoding="utf-8")
    assert sc.main(["expected", "--id", "k1", "--package", str(pkg)]) == 0
    after = json.loads((folder / "expected.json").read_text())
    rows = json.loads((folder / "story.json").read_text())["not_walked"]
    assert after["amendments"] == [row] and after["stages"]["S1"]["outcome"] == "accepted"
    assert lead in rows and not any(r.get("why") == "by hand, no key" for r in rows)
    assert len([r for r in rows if r.get("why") == "by hand"]) == 1


def test_ticket_key_keeps_the_runs_own_ids_and_rewrites_real_keys(tmp_path):
    """Item 8: BN-10, BN-11 and RUN-2026 are the run's own ids, not tracker keys; a real key still becomes REF-n."""
    root = make_root(tmp_path / "t")
    (root / "work" / "r.md").write_text("BN-10 and BN-11 in RUN-2026, but ACME-13797 and ABCD-123\n", encoding="utf-8")
    code, pkg = run(root, tmp_path, "t1")
    assert code == 0
    assert story_text(pkg, "t1")["work/r.md"] == "BN-10 and BN-11 in RUN-2026, but REF-1 and REF-2\n"


def test_story_version_is_the_runs_not_the_packages(tmp_path):
    """W5: story.json carries `pipeline.json` `run_mode.plugin_version` of the run, else unknown (never the current package's)."""
    root = make_root(tmp_path / "v")
    code, pkg = run(root, tmp_path, "w0")
    assert code == 0 and json.loads(story_text(pkg, "w0")["story.json"])["package_version"] == "unknown"
    (root / "pipeline.json").write_text('{"run_mode": {"plugin_version": "0.10.5"}}', encoding="utf-8")
    assert run(root, tmp_path, "w1")[0] == 0
    assert json.loads(story_text(pkg, "w1")["story.json"])["package_version"] == "0.10.5"
    # item 2: the version comes from the SOURCE, so a dropped pipeline.json no longer gives "unknown"
    assert run(root, tmp_path, "w2", "--drop", "pipeline.json")[0] == 0
    texts = story_text(pkg, "w2")
    assert "pipeline.json" not in texts and json.loads(texts["story.json"])["package_version"] == "0.10.5"


def full_package(base):
    """A package folder with the real top-level scripts (branch_accounting and what it imports) and nothing else."""
    pkg = base / "fullpkg"
    if not pkg.exists():
        (pkg / "scripts").mkdir(parents=True)
        for path in (PACKAGE / "scripts").glob("*.py"):
            shutil.copy(path, pkg / "scripts" / path.name)
        shutil.copytree(PACKAGE / "references", pkg / "references")    # the data files the modules read at import
    return pkg


SNAPSHOT = {"key": "LOCAL-1", "title": "t", "acceptance_criteria": ["Check XPANBFLFA-141 page"],
            "description": "See https://example.org/projects/Q/issues/XPANBFLFA-141?filter=a for context.\nA plain line stays.",
            "comments": [{"text": "Mentions XPANBFLFA-141 here. And a second sentence."}, {"text": "No key in this comment."}]}


def accounting(pkg):
    return sc.load_accounting(pkg)


def snapshot_ids(ba, snap):
    return [(u[1], ba.unit_id(u[1]), u[2]) for u in ba.snapshot_units(snap, title_counts=True)["units"]]


def test_text_derived_ids_follow_the_rewrites(tmp_path):
    """TD-15 fix round 3 item 1: a unit id homed in the register stays homed after the scrub rewrote its line; an id whose text the
    scrub did not change is untouched; an id-like token no captured text produces is untouched; the recorded hash of the re-keyed
    register follows its new bytes (the id remap runs BEFORE the hash follow)."""
    import hashlib
    pkg = full_package(tmp_path)
    ba = accounting(pkg)
    root = make_root(tmp_path / "src")
    (root / "work" / "ticket-snapshot.json").write_text(json.dumps(SNAPSHOT), encoding="utf-8")
    old = snapshot_ids(ba, SNAPSHOT)
    register = "## Source obligations\n| unit | home |\n|---|---|\n" + "".join("| %s | R-1 |\n" % i for _t, i, _g in old)
    register += "| %s | R-2 |\n| U-0123456789ab | R-3 |\n" % ", ".join(sorted({g for _t, _i, g in old if g}))
    (root / "work" / "requirements-register.md").write_text(register, encoding="utf-8")
    (root / "work" / "inv.json").write_text(json.dumps({"register_sha256": hashlib.sha256(register.encode()).hexdigest()}), encoding="utf-8")
    info = {}
    sc.capture(root, "ids1", package=pkg, report=info)
    story = pkg.joinpath(*sc.STORIES, "ids1")
    scrubbed = json.loads((story / "work" / "ticket-snapshot.json").read_text(encoding="utf-8"))
    new = snapshot_ids(ba, scrubbed)
    text = (story / "work" / "requirements-register.md").read_text(encoding="utf-8")
    assert [t for t, _i, _g in new] != [t for t, _i, _g in old] and len(new) == len(old)
    assert all(i in text for _t, i, _g in new) and all(g in text for _t, _i, g in new if g)    # every unit and group is still homed
    changed = [(o, n) for o, n in zip(old, new) if o[1] != n[1]]
    assert changed and not any(o[1] in text for o, _n in changed)    # the old ids are gone
    same = [(o, n) for o, n in zip(old, new) if o[1] == n[1]]
    assert same and all(o[1] in text for o, _n in same)    # a line the scrub did not change keeps its id
    assert "U-0123456789ab" in text    # an id-like token no captured text produces
    inv = json.loads((story / "work" / "inv.json").read_text(encoding="utf-8"))
    assert inv["register_sha256"] == hashlib.sha256((story / "work" / "requirements-register.md").read_bytes()).hexdigest()
    assert info["ids"]["U"][1] == len(changed) and info["ids"]["G"][1] >= 1
    readme = (story / "README.txt").read_text(encoding="utf-8")
    assert "U- %d ids" % info["ids"]["U"][1] in readme and "G- %d ids" % info["ids"]["G"][1] in readme


def test_two_old_ids_on_one_new_id_are_refused_by_line(tmp_path):
    """Edge: two lines that became equal after the rewrite: a refusal naming both lines, nothing captured."""
    pkg = full_package(tmp_path)
    root = make_root(tmp_path / "src")
    snap = dict(SNAPSHOT, description="privet\n" + CYR, comments=[], acceptance_criteria=[])
    (root / "work" / "ticket-snapshot.json").write_text(json.dumps(snap), encoding="utf-8")
    try:
        sc.capture(root, "ids2", package=pkg)
        refused = ""
    except sc.Refusal as exc:
        refused = str(exc)
    assert "description unit 1" in refused and "description unit 2" in refused and "became one" in refused
    assert not pkg.joinpath(*sc.STORIES, "ids2").exists()


def test_a_story_with_no_text_derived_change_is_untouched(tmp_path):
    """Edge: no snapshot (or one the scrub did not change): no remap, the files are what the scrub alone gives, README says 0 ids."""
    root = make_root(tmp_path / "src")
    code, pkg = run(root, tmp_path, "ids3")    # a package with no branch_accounting at all: never asked for
    assert code == 0
    assert "U- 0 ids 0 replacements, G- 0 ids 0 replacements" in story_text(pkg, "ids3")["README.txt"]
    clean = dict(SNAPSHOT, description="plain", comments=[], acceptance_criteria=[])
    (root / "work" / "ticket-snapshot.json").write_text(json.dumps(clean), encoding="utf-8")
    assert run(root, tmp_path, "ids4")[0] == 0    # a snapshot the scrub does not change needs no package function either


def test_example_url_keeps_the_browse_key_and_the_key_follows_ticket_key(tmp_path):
    """Item 6 (C-2): `https://example.org/browse/XPAN-141?x` keeps `/browse/<KEY>`; the key becomes the SAME REF-n as the bare key
    elsewhere; one host is one number; a URL with no /browse/ is still replaced whole."""
    root = make_root(tmp_path / "src")
    (root / "work" / "u.txt").write_text(
        "key XPANBFLFA-141 and https://example.org/browse/XPANBFLFA-141?filter=a and https://example.org/browse/OTHERQ-12 "
        "and https://git.example.com/x/y and https://example.org/projects/Q\n", encoding="utf-8")
    code, pkg = run(root, tmp_path, "u1")
    assert code == 0
    assert story_text(pkg, "u1")["work/u.txt"] == (
        "key REF-1 and https://example.invalid/1/browse/REF-1 and https://example.invalid/1/browse/REF-2 "
        "and https://example.invalid/2 and https://example.invalid/3\n")


def test_hash_follow_is_a_fixpoint(tmp_path):
    """Item 9: raw.json changes by a rewrite; ticket.json embeds raw's hash (changes again); the inventory records ticket.json's
    ORIGINAL hash and must end up with the hash of the final ticket.json."""
    import hashlib
    root = make_root(tmp_path / "f")
    raw = '{"t": "see TP1-13797"}'
    sha = lambda text: hashlib.sha256(text.encode()).hexdigest()    # noqa: E731
    ticket = json.dumps({"raw_sha256": sha(raw), "k": "TP1-13797"})
    (root / "work" / "raw.json").write_text(raw, encoding="utf-8")
    (root / "work" / "ticket.json").write_text(ticket, encoding="utf-8")
    (root / "work" / "inv.json").write_text(json.dumps({"ticket_sha256": sha(ticket)}), encoding="utf-8")
    code, pkg = run(root, tmp_path, "f1")
    assert code == 0
    files = story_text(pkg, "f1")
    assert json.loads(files["work/ticket.json"])["raw_sha256"] == sha(files["work/raw.json"])
    assert json.loads(files["work/inv.json"])["ticket_sha256"] == sha(files["work/ticket.json"])


def test_cap_counts_run_files_only_and_is_exact(tmp_path, monkeypatch, capsys):
    """Item 5: the cap is on the captured run files; README.txt / story.json / expected.json are not counted. At the cap: accepted;
    one byte over: refused, naming the largest files."""
    root = make_root(tmp_path / "c")
    (root / "work" / "big.txt").write_text("x" * 5000, encoding="utf-8")
    for n in range(40):    # a long dropped list makes README.txt and story.json big: they must not count
        (root / "work" / ("dropped-%02d.png.txt" % n)).write_text("d", encoding="utf-8")
    info = {}
    pkg = tmp_path / "pkg"
    (pkg / "scripts").mkdir(parents=True)
    shutil.copy(PACKAGE / "scripts" / "event_store.py", pkg / "scripts" / "event_store.py")
    sc.capture(root, "k1", package=pkg, drop=["*.png.txt"], report=info)
    run_bytes = info["size"]
    own = sum((pkg.joinpath(*sc.STORIES, "k1") / n).stat().st_size for n in sc.OWN_FILES if (pkg.joinpath(*sc.STORIES, "k1") / n).is_file())
    assert own > 1000
    monkeypatch.setattr(sc, "LIMIT_BYTES", run_bytes)
    sc.capture(root, "k2", package=pkg, drop=["*.png.txt"])    # exactly at the cap: accepted
    monkeypatch.setattr(sc, "LIMIT_BYTES", run_bytes - 1)
    try:
        sc.capture(root, "k3", package=pkg, drop=["*.png.txt"])
        refused = ""
    except sc.Refusal as exc:
        refused = str(exc)
    assert "over the %d limit" % (run_bytes - 1) in refused and "work/big.txt" in refused
    assert not pkg.joinpath(*sc.STORIES, "k3").exists()


# -- the classes built from the SOURCE (TD-15 scrub fix round; every value below is invented) ---------------------------------------------
PERSON, LOGIN, HOMEUSER, PROJECT = "Zed Quarkson", "zquark_login", "hhomeuser", "ZZPROJ"


def person_root(base, **extra):
    root = make_root(base)
    (root / "work" / "sources").mkdir()
    ticket = {"key": "LOCAL-1", "reporter": PERSON, "assignee": None, "creator": {
        "displayName": PERSON, "emailAddress": "Zed_Quarkson@corp.example", "name": LOGIN, "key": LOGIN, "accountId": "acc12345"},
        "project": {"key": PROJECT, "name": "ZZPN"}, "kind": {"reporter": "junit-xml"}, "owner": {"reporter": ""}}
    (root / "work" / "sources" / "ticket.json").write_text(json.dumps(ticket, indent=1), encoding="utf-8")
    (root / "work" / "notes.md").write_text(
        "ping zed_quarkson@corp.example and %s about %s-12 and %s alone, %s lower; %s on C:\\Users\\%s\\x and bare %s, cc kestrel.vane@corp.example\n"
        % (LOGIN, PROJECT, PROJECT, PROJECT.lower(), PERSON.upper(), HOMEUSER, HOMEUSER), encoding="utf-8")
    (root / "work" / "form.yaml").write_text("reporter: %s\nassignee: \nauthor: '%s'\n" % (PERSON, LOGIN), encoding="utf-8")
    return root


def all_text(pkg, story_id):
    return "\n".join(story_text(pkg, story_id).values())


def test_person_mail_login_and_project_classes_are_rewritten_to_marks(tmp_path):
    code, pkg = run(person_root(tmp_path / "p"), tmp_path, "p1")
    assert code == 0
    files, text = story_text(pkg, "p1"), all_text(pkg, "p1").lower()
    for value in (PERSON, LOGIN, HOMEUSER, PROJECT, "quarkson", "acc12345", "kestrel"):    # nothing of any class is left, in any case
        assert value.lower() not in text
    ticket = json.loads(files["work/sources/ticket.json"])
    assert ticket["reporter"] == "person-1" and ticket["creator"]["displayName"] == "person-1"    # one person, one mark, across fields
    assert ticket["creator"]["emailAddress"] == "person-1@example.invalid"    # a mail address; its local part spelt with a dot or underscore
    assert ticket["creator"]["name"] == ticket["creator"]["key"] == "person-2"    # the login is a second spelling: its own mark
    assert ticket["creator"]["accountId"] == "person-5"    # numbered by first appearance in the source (the second mail was person-3, the home user person-4)
    assert ticket["assignee"] is None and ticket["owner"]["reporter"] == "" and ticket["kind"]["reporter"] == "junit-xml"    # empty / not a person
    assert ticket["project"] == {"key": "REF", "name": "REF"}
    notes = files["work/notes.md"]    # the same marks in another file: stable
    assert notes == ("ping person-1@example.invalid and person-2 about REF-1 and REF alone, REF lower; person-1 on <home>\\x and bare person-4, cc person-3@example.invalid\n")
    assert files["work/form.yaml"] == "reporter: person-1\nassignee: \nauthor: 'person-2'\n"
    readme = files["README.txt"]
    assert "changed: person x" in readme and "changed: mail x 3 (2 distinct)" in readme and "changed: project-key x" in readme


def test_a_value_the_rewrite_misses_refuses_the_capture_by_class_and_line(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sc.Registry, "rewrite", lambda self, value, cleaner: value)    # a rewrite that misses everything
    assert run(person_root(tmp_path / "p"), tmp_path, "r1")[0] == 1
    err = capsys.readouterr().err
    for rule in ("residue-person", "residue-mail", "residue-login", "residue-project"):
        assert re.search(r"work/[a-z/]+\.(?:json|md|yaml):\d+: rule %s: " % rule, err), rule
    assert "work/sources/ticket.json:" in err and "work/notes.md:" in err
    low = err.lower()
    assert not any(v.lower() in low for v in (PERSON, LOGIN, HOMEUSER, PROJECT, "quarkson"))    # the refusal never prints a value
    assert not tmp_path.joinpath("pkg", *sc.STORIES, "r1").exists()


def test_a_dropped_file_name_carrying_a_value_reaches_the_readme_only_as_a_refusal(tmp_path, monkeypatch, capsys):
    root = make_root(tmp_path / "p")
    (root / "work" / "n.md").write_text("see %s-12\n" % PROJECT, encoding="utf-8")    # the ticket key makes the project a collected value
    (root / "work" / ("page-%s.html" % PROJECT.lower())).write_text("x", encoding="utf-8")
    code, pkg = run(root, tmp_path, "d1", "--drop", "work/page-*")
    assert code == 0 and "page-zzproj" not in story_text(pkg, "d1")["README.txt"].lower()    # the dropped name is listed scrubbed
    assert "dropped: work/page-REF.html" in story_text(pkg, "d1")["README.txt"]
    monkeypatch.setattr(sc.Registry, "rewrite", lambda self, value, cleaner: value)
    assert run(root, tmp_path, "d2", "--drop", "work/page-*")[0] == 1
    assert "README.txt:" in capsys.readouterr().err


def test_two_files_that_become_one_name_are_refused(tmp_path, capsys):
    root = person_root(tmp_path / "p")
    (root / "work" / ("a-%s.txt" % PROJECT)).write_text("1", encoding="utf-8")
    (root / "work" / "a-REF.txt").write_text("2", encoding="utf-8")
    assert run(root, tmp_path, "n1")[0] == 1 and "became one name" in capsys.readouterr().err


def test_residue_command_counts_per_class_and_never_prints_a_value(tmp_path, capsys):
    root = person_root(tmp_path / "p")
    code, pkg = run(root, tmp_path, "c1")
    assert code == 0
    capsys.readouterr()
    assert sc.main(["residue", "--source", str(root), "--id", "c1", "--package", str(pkg)]) == 0
    out = capsys.readouterr().out
    assert "residue-person: 0 hits" in out and "residue-mail: 0 hits" in out and "residue-login: 0 hits" in out and "residue-project: 0 hits" in out
    planted = pkg.joinpath(*sc.STORIES, "c1", "work", "notes.md")
    planted.write_text(planted.read_text(encoding="utf-8") + "left: %s\n" % PERSON.lower(), encoding="utf-8")
    assert sc.main(["residue", "--source", str(root), "--id", "c1", "--package", str(pkg), "--lines"]) == 1
    out = capsys.readouterr().out
    assert "work/notes.md:2 residue-person" in out and PERSON.lower() not in out.lower() and "residue-person: 1 hits" in out


# -- the repository handle and the agent project folder (TD-15 scrub2; every value below is invented) ----------------------------------------
FOX, BETA, MAPPED = "alphafox", "betafox", "zlogin9"
SEED = "github.com/%s github.com/%s C:\\Users\\%s\\x" % (FOX, BETA, MAPPED)    # the order the numbers are given in: 1, 2, then the login


def sha(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cleaner_for(tmp_path, *seen):
    registry = sc.Registry(sc.load_derived(), rows=sc.load_residue_rows())
    for text in seen or (SEED,):
        registry.read_text(text)
    return sc.Cleaner(tmp_path, sc.load_rewrites(), registry=registry), registry


URL_TABLE = [    # (text in, text out): scheme / no scheme / .git / www / case / the repository name stays / the host stays
    ("https://github.com/alphafox/repo-one", "https://github.com/person-1/repo-one"),
    ("see github.com/alphafox", "see github.com/person-1"),
    ("github.com/alphafox.git", "github.com/person-1.git"),
    ("https://github.com/betafox/lib.git", "https://github.com/person-2/lib.git"),
    ("http://www.gitlab.com/alphafox/z", "http://www.gitlab.com/person-1/z"),
    ("gitlab.com/BetaFox/Z", "gitlab.com/person-2/Z"),
    ("(github.com/alphafox)", "(github.com/person-1)"),
    ("github.com/alphafox/alphafox", "github.com/person-1/alphafox"),    # the repository name after the handle is kept
    ("https://github.com/", "https://github.com/"),    # no handle: untouched
    ("github.com/ and gitlab.com", "github.com/ and gitlab.com"),
    ("https://api.github.com/", "https://api.github.com/"),    # the api host with no handle behind it: untouched
    ("https://api.github.com/repos/alphafox/r", "https://api.github.com/repos/person-1/r"),    # api.<host>/repos/<handle>
    ("https://api.github.com/users/BetaFox", "https://api.github.com/users/person-2"),    # api.<host>/users/<handle>
    ("git@github.com:alphafox/r.git", "git@github.com:person-1/r.git"),    # the scp form
    ("ssh://git@gitlab.com/betafox/r.git", "ssh://git@gitlab.com/person-2/r.git"),
    ("https://raw.githubusercontent.com/alphafox/r/main/x.md", "https://raw.githubusercontent.com/person-1/r/main/x.md"),
    ("https://alphafox.github.io/site/", "https://person-1.github.io/site/"),    # a pages host: the handle is the label before it
    ("https://github.com/users/betafox/x", "https://github.com/users/person-2/x"),    # <host>/users/<handle>: the handle is the segment after `users`
    ("https://github.com/orgs/alphafox", "https://github.com/orgs/person-1"),
    ("https%3A%2F%2Fgithub.com%2Falphafox%2Frepo", "https%3A%2F%2Fgithub.com%2Fperson-1%2Frepo"),    # percent-encoded slash
    ("https:\\/\\/github.com\\/alphafox\\/repo", "https:\\/\\/github.com\\/person-1\\/repo"),    # JSON-escaped slash, as text
    ("github.com/person-7/r", "github.com/person-7/r"),    # already a mark
    ("https://person-7.github.io/s", "https://person-7.github.io/s"),
    ("", ""),
]


@pytest.mark.parametrize("text,expected", URL_TABLE)
def test_repository_handle_becomes_the_persons_mark_and_is_a_fixpoint(tmp_path, text, expected):
    cleaner, _ = cleaner_for(tmp_path)
    once = cleaner.text(text)
    assert once == expected
    assert cleaner.text(once) == once


def test_handle_in_json_and_jsonl_and_the_same_handle_twice_is_one_number(tmp_path):
    cleaner, _ = cleaner_for(tmp_path)
    doc = '{"u": "https://github.com/alphafox/r", "v": ["github.com/alphafox", "github.com/betafox/x"]}'
    out = json.loads(cleaner.json_text(doc))
    assert out == {"u": "https://github.com/person-1/r", "v": ["github.com/person-1", "github.com/person-2/x"]}
    rows = '{"a": "github.com/alphafox/r"}\n{"b": "gitlab.com/alphafox.git"}\n'
    assert cleaner.json_text(rows) == '{"a": "github.com/person-1/r"}\n{"b": "gitlab.com/person-1.git"}\n'
    assert cleaner.json_text(cleaner.json_text(rows)) == cleaner.json_text(rows)    # a fixpoint


def test_a_handle_that_is_also_a_mapped_login_keeps_the_logins_number(tmp_path):
    cleaner, registry = cleaner_for(tmp_path)
    login_mark = cleaner.text("bare %s here" % MAPPED).split()[1]
    assert login_mark.startswith("person-")
    assert cleaner.text("https://github.com/%s/r" % MAPPED) == "https://github.com/%s/r" % login_mark
    assert registry.people[sc.norm(MAPPED)]["n"] == int(login_mark.split("-")[1])


AGENT_TABLE = [
    ("<home>\\.claude\\projects\\D--ws-demo-stand\\abc", "<home>\\.claude\\projects\\C--work-stand\\abc"),
    ("<home>\\\\.claude\\\\projects\\\\D--ws-demo-stand\\\\abc", "<home>\\\\.claude\\\\projects\\\\C--work-stand\\\\abc"),
    ("~/.claude/projects/D--ws-demo-stand/abc", "~/.claude/projects/C--work-stand/abc"),
    ("~/.claude/projects/C--work-stand/abc", "~/.claude/projects/C--work-stand/abc"),    # the constant itself: untouched
    ("a folder named D--ws-demo-stand alone", "a folder named D--ws-demo-stand alone"),    # not under .claude/projects
    ("~/.claude/projects/-home-alice-demo-stand/abc", "~/.claude/projects/C--work-stand/abc"),    # the POSIX encoding
    ("~/.claude/projects/-Users-alice-demo-stand/abc", "~/.claude/projects/C--work-stand/abc"),
    ("~/.Claude/Projects/-home-alice-demo/abc", "~/.Claude/Projects/C--work-stand/abc"),    # `.claude` in any case
    ("~/.CLAUDE/projects/D--ws-demo-stand/abc", "~/.CLAUDE/projects/C--work-stand/abc"),
    ("x.claude\\/projects\\/D--ws-demo-stand\\/abc", "x.claude\\/projects\\/C--work-stand\\/abc"),    # JSON-escaped slash, as text
    ("x.claude\\/projects\\/-home-alice-demo\\/abc", "x.claude\\/projects\\/C--work-stand\\/abc"),
    ("", ""),
]


@pytest.mark.parametrize("text,expected", AGENT_TABLE)
def test_agent_project_folder_is_a_neutral_constant_in_any_slash_form(tmp_path, text, expected):
    cleaner, _ = cleaner_for(tmp_path)
    once = cleaner.text(text)
    assert once == expected
    assert cleaner.text(once) == once


def test_the_residue_scan_reports_each_new_class_and_nothing_on_clean_text(tmp_path):
    _, registry = cleaner_for(tmp_path)
    planted = "ok line\nsee https://github.com/leftfox/r\n<home>\\.claude\\projects\\D--ws-demo-stand\\abc\n"
    assert registry.residue("a.md", planted) == [("a.md", 2, "residue-handle"), ("a.md", 3, "residue-agent-project-folder")]
    clean = "see https://github.com/person-3/r\n<home>\\.claude\\projects\\C--work-stand\\abc\nhttps://github.com/\n"
    assert registry.residue("a.md", clean) == []
    assert registry.residue("github.com/leftfox/x.md", "") == [("github.com/leftfox/x.md", 0, "residue-handle")]


RESIDUE_TABLE = [    # (planted leftover, the clean text the rewrite makes of it, class): one row per form
    ("https://github.com/leftfox/r", "https://github.com/person-3/r", "handle"),
    ("see github.com/leftfox.git now", "see github.com/person-3.git now", "handle"),
    ("git@github.com:leftfox/r.git", "git@github.com:person-3/r.git", "handle"),    # scp
    ("https://api.github.com/repos/leftfox/r", "https://api.github.com/repos/person-3/r", "handle"),
    ("https://api.github.com/users/leftfox", "https://api.github.com/users/person-3", "handle"),
    ("https://raw.githubusercontent.com/leftfox/r/main/x", "https://raw.githubusercontent.com/person-3/r/main/x", "handle"),
    ("https://leftfox.github.io/s", "https://person-3.github.io/s", "handle"),
    ("https://www.leftfox.github.io/s", "https://www.person-3.github.io/s", "handle"),    # a host with one more label: the rewrite misses it, the detector does not
    ("https://github.com/users/leftfox/x", "https://github.com/users/person-3/x", "handle"),
    ("https://gitlab.com/orgs/leftfox", "https://gitlab.com/orgs/person-3", "handle"),
    ("https%3A%2F%2Fgithub.com%2Fleftfox%2Frepo", "https%3A%2F%2Fgithub.com%2Fperson-3%2Frepo", "handle"),    # percent-encoded slash
    ("https:\\/\\/github.com\\/leftfox\\/repo", "https:\\/\\/github.com\\/person-3\\/repo", "handle"),    # JSON-escaped slash
    ("x\\.claude\\projects\\D--ws-demo-stand\\q", "x\\.claude\\projects\\C--work-stand\\q", "agent-project-folder"),
    ("~/.claude/projects/-home-alice-demo-stand/q", "~/.claude/projects/C--work-stand/q", "agent-project-folder"),    # POSIX encoding
    ("~/.Claude/Projects/-home-alice-demo/q", "~/.Claude/Projects/C--work-stand/q", "agent-project-folder"),    # case
    ("x.claude\\/projects\\/-home-alice-demo\\/q", "x.claude\\/projects\\/C--work-stand\\/q", "agent-project-folder"),    # JSON-escaped slash
    ("~/.claude/projects/some-other-name/q", "~/.claude/projects/C--work-stand/q", "agent-project-folder"),    # a name the rewrite row does not know: only the detector sees it
]
CLEAN_TEXT = ["see https://github.com/person-3/r.", "https://github.com/", "gitlab.com and github.com, nothing else", "github.com: a colon, a space",
              "https://api.github.com/repos/", "person-3.github.io is a mark","~/.claude/projects/C--work-stand/abc",
              "a folder .claude with no projects", "http://example.invalid/leftfox/r", ""]


@pytest.mark.parametrize("planted,clean,cls", RESIDUE_TABLE)
def test_residue_scan_reports_each_form_once_and_is_silent_on_the_rewritten_text(tmp_path, planted, clean, cls):
    cleaner, registry = cleaner_for(tmp_path)
    assert registry.residue("a.md", "ok line\n%s\nnext\n" % planted) == [("a.md", 2, "residue-" + cls)]    # one hit (rewrite and detector are not added up), line 2
    assert registry.residue("a.md", "ok line\n%s\nnext\n" % clean) == []    # what the rewrite makes of it is clean: the detector has no false alarm on it


@pytest.mark.parametrize("planted,clean,cls", RESIDUE_TABLE)
def test_the_residue_detectors_find_a_form_without_the_rewrite_patterns(tmp_path, planted, clean, cls):    # independent: not a fixpoint of the rewrite
    _, registry = cleaner_for(tmp_path)
    registry.handle, registry.rows = re.compile("(?!x)x"), []
    assert registry.residue("a.md", "ok\n%s\n" % planted) == [("a.md", 2, "residue-" + cls)]


@pytest.mark.parametrize("text", CLEAN_TEXT)
def test_the_residue_scan_is_silent_on_clean_text(tmp_path, text):
    _, registry = cleaner_for(tmp_path)
    assert registry.residue("a.md", text + "\n") == []


def test_residue_command_and_capture_refuse_a_leftover_handle_by_class_and_line(tmp_path, monkeypatch, capsys):
    root = person_root(tmp_path / "p")
    (root / "work" / "refs.md").write_text("one\nhttps://github.com/leftfox/r\n", encoding="utf-8")
    monkeypatch.setattr(sc.Registry, "rewrite_handles", lambda self, value, cleaner: value)    # a rewrite that misses the class
    assert run(root, tmp_path, "h1")[0] == 1
    err = capsys.readouterr().err
    assert "work/refs.md:2: rule residue-handle" in err and "leftfox" not in err
    monkeypatch.undo()
    code, pkg = run(root, tmp_path, "h2")
    assert code == 0 and "leftfox" not in all_text(pkg, "h2") and "github.com/person-" in all_text(pkg, "h2")
    capsys.readouterr()
    assert sc.main(["residue", "--source", str(root), "--id", "h2", "--package", str(pkg)]) == 0
    assert "residue-handle: 0 hits" in capsys.readouterr().out
    planted = pkg.joinpath(*sc.STORIES, "h2", "work", "refs.md")
    planted.write_text(planted.read_text(encoding="utf-8") + "x\\.claude\\projects\\D--ws-demo-stand\\q\nhttp://gitlab.com/rightfox/z\n", encoding="utf-8")
    assert sc.main(["residue", "--source", str(root), "--id", "h2", "--package", str(pkg), "--lines"]) == 1
    out = capsys.readouterr().out
    assert "residue-handle: 1 hits" in out and "residue-agent-project-folder: 1 hits" in out
    assert "work/refs.md:4 residue-handle" in out and "rightfox" not in out and "demo-stand" not in out


def test_rescrub_rewrites_in_place_leaves_other_files_equal_and_is_a_fixpoint(tmp_path, capsys):
    root = person_root(tmp_path / "p")
    code, pkg = run(root, tmp_path, "r1")
    assert code == 0
    story = pkg.joinpath(*sc.STORIES, "r1")
    (story / "work" / "late.md").write_text("see https://github.com/leftfox/r and github.com/leftfox\nx\\.claude\\projects\\D--ws-demo-stand\\q\n", encoding="utf-8")
    (story / "work" / "late.json").write_text('{"u": "gitlab.com/leftfox/r.git"}\n', encoding="utf-8")
    (story / "work" / "empty.txt").write_text("", encoding="utf-8")
    (story / "work" / "plain.md").write_text("nothing to see here\n", encoding="utf-8")
    (story / "work" / "blob.bin").write_bytes(b"\xff\xfe\x00github.com/leftfox\x80")
    stay = {n: sha(story / "work" / n) for n in ("empty.txt", "plain.md", "blob.bin")}
    untouched = {n: sha(story / n) for n in ("story.json", "work/delivery-summary.json")}
    assert sc.main(["rescrub", "--id", "r1", "--package", str(pkg)]) == 0
    assert "handle x 3" in capsys.readouterr().out
    late = (story / "work" / "late.md").read_text(encoding="utf-8")
    first = re.fullmatch(r"see https://github.com/(person-\d+)/r and github.com/(person-\d+)", late.splitlines()[0])
    assert first and first.group(1) == first.group(2)    # one handle, one number
    assert "leftfox" not in late and "C--work-stand" in late and json.loads((story / "work" / "late.json").read_text(encoding="utf-8"))["u"].startswith("gitlab.com/person-")
    assert {n: sha(story / "work" / n) for n in stay} == stay    # empty, no match, binary: byte-equal
    assert {n: sha(story / n) for n in untouched} == untouched    # the hand-made / unrelated files: byte-equal
    everything = {p.relative_to(story).as_posix(): sha(p) for p in story.rglob("*") if p.is_file()}
    assert sc.main(["rescrub", "--id", "r1", "--package", str(pkg)]) == 0
    assert "files written: 0" in capsys.readouterr().out
    assert {p.relative_to(story).as_posix(): sha(p) for p in story.rglob("*") if p.is_file()} == everything    # a fixpoint by sha256


def test_rescrub_keeps_the_cap_and_a_refusal_changes_nothing(tmp_path, monkeypatch, capsys):
    code, pkg = run(person_root(tmp_path / "p"), tmp_path, "r2")
    assert code == 0
    story = pkg.joinpath(*sc.STORIES, "r2")
    (story / "work" / "late.md").write_text("github.com/leftfox/r\n", encoding="utf-8")
    before = {p.relative_to(story).as_posix(): sha(p) for p in story.rglob("*") if p.is_file()}
    monkeypatch.setattr(sc, "LIMIT_BYTES", 10)
    assert sc.main(["rescrub", "--id", "r2", "--package", str(pkg)]) == 1
    assert "over the 10 limit" in capsys.readouterr().err
    assert {p.relative_to(story).as_posix(): sha(p) for p in story.rglob("*") if p.is_file()} == before
