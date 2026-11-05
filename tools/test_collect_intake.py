"""Tests of tools/collect_intake.py (CL1-6; t-1075 with §L and §L-2; the plan critic's battery t-1079 §5). Expected values come from the
requirements named beside each pin (the spec's invariants I1-I10 and edges), never from running the code (FR-58). The archives are
built here: a hand-made one carries the hostile shapes, a real `collect_pack.pack` one pins the schema the intake reads.
"""
import datetime
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import types
import zipfile
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import collect_intake as ci  # noqa: E402
import piles  # noqa: E402
import piles_testkit as kit  # noqa: E402

NAME = "qa-collect-abababab-20261019T120000Z.zip"
IID, PID = "ab" * 16, "0123456789ab"
NOW = datetime.datetime(2026, 10, 20, 12, 30)
OK_PKG = {"package_modified": "no", "package_modified_why": "match", "package_modified_detail": {"running_version": "0.9.1", "install": "cache"}}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def M(data, set_="A", rel=None, flags=(), attr=0):
    return {"data": data.encode("utf-8") if isinstance(data, str) else data, "set": set_, "rel": rel, "flags": list(flags), "attr": attr}


def build(d, members, doc=None, name=NAME, rows=None, extra_parts=()):
    """A hand-made archive in directory d. members: {arc: M(...)}; rows default to one honest row per member."""
    rows = rows if rows is not None else [{"arc": a, "src_rel": m["rel"] or a, "set": m["set"], "mode": "copy", "bytes": len(m["data"]), "sha256": sha(m["data"]),
                                            "src_sha256": None, "flags": m["flags"], "redactions": {}} for a, m in members.items()]
    manifest = {"schema": "qa-collect/1", "project_id": PID, "install_id": IID, "collected_at": "2026-10-19T12:00:00Z", **OK_PKG, "files": rows,
                "skipped": [], "gaps": [], "stories": [], "answers": {"problems": {"state": "blank", "arc": None}, "suggestions": {"state": "blank", "arc": None}},
                "parts": list(extra_parts), "part_count": len(extra_parts) + 1, **(doc or {})}
    path = Path(d) / name
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest.json", json.dumps(manifest))
        for arc, m in members.items():
            info = zipfile.ZipInfo(arc)
            info.external_attr = m["attr"] << 16
            zf.writestr(info, m["data"])
    return path


def fb_json(*rows):
    return json.dumps({"findings": [{"id": i, "essence": e, "scope": "local-calibration", "witness/details": w, "created": "2026-10-19", "status": "open", "decision": "—"}
                                    for i, e, w in rows]})


D2 = "records/project-decisions.json"


def fb_archive(d, rows, **kw):
    return build(d, {D2: M(fb_json(*rows), "D", D2)}, **kw)


@pytest.fixture(autouse=True)
def fixed_time(monkeypatch):
    monkeypatch.setattr(ci, "now", lambda: NOW)
    ci.limits()
    monkeypatch.setattr(ci, "LIMITS", dict(ci.LIMITS))          # a test that moves a ceiling moves its own copy


@pytest.fixture
def work(tmp_path):
    arch, inbox = tmp_path / "arch", tmp_path / "inbox"
    arch.mkdir()
    return arch, inbox


@pytest.fixture
def tree(session_tree, tmp_path):
    """This module's repo: a full copy (with .git, `piles.py check` wants it) of the mini repo of piles_testkit."""
    dst = tmp_path / "repo"
    shutil.copytree(session_tree, dst)
    return dst


def scratch_tree(tree):
    """The mini repo of piles_testkit + the pieces the intake needs: a registry with three package features, three package files, forge batch 2
    untaken, a `proposals` and a `cost-dashboard` pile with an untaken batch 1, and `report-delivery` with NO untaken batch."""
    if (tree / "ai-packages/qa-factory/scripts/forge_thing.py").exists():
        return tree
    kit.put(tree, "plans/features.json", json.dumps({"schema_version": 1, "features": [
        {"id": "F19", "name": "forge", "root": "package", "globs": ["scripts/forge_thing.py"], "stages": [], "words": []},
        {"id": "F08", "name": "report", "root": "package", "globs": ["scripts/traceability.py"], "stages": [], "words": []},
        {"id": "F22", "name": "collect", "root": "package", "globs": ["scripts/collect_x.py"], "stages": [], "words": []}]}))
    for f in ("forge_thing", "traceability", "collect_x"):
        kit.put(tree, "ai-packages/qa-factory/scripts/%s.py" % f, "x = 1\n")
    kit.batch2(tree)
    for slug, feats in (("proposals", "F22"), ("cost-dashboard", "F14")):
        kit.put(tree, "plans/piles/%s/README.md" % slug, kit.card_text(slug, slug, [["1", "x", "—", "S", "ожидает", "—", "—", "—"]], feats))
        kit.put(tree, "plans/piles/%s/batch-1-x.md" % slug, kit.batch_text(slug, 1, "ожидает", [kit.node("PR1-1", "`tools/z.py`", "ожидает")], who="—", branch="—", proof=kit.PROOF_DONE))
    return tree


def run(tree, inbox, *archives, apply=False, place=(), capsys=None, extra=()):
    argv = [str(a) for a in archives] + ["--repo", str(tree)] + (["--inbox", str(inbox)] if inbox else []) + (["--apply"] if apply else [])
    for p in place:
        argv += ["--place", p]
    code = ci.main(argv + list(extra))
    out = capsys.readouterr()
    return code, out.out, out.err


def files_under(root):
    return sorted(str(p.relative_to(root)) for p in Path(root).rglob("*") if p.is_file()) if Path(root).exists() else []


# ---------------------------------------------------------------- A. verify: the untrusted-input battery (t-1079 section 5)

@pytest.mark.parametrize("bad", ["../x", "a/../b", "/abs/x", "C:x", "//srv/share/x", "a//b", "a/./b", "./a"])
def test_zip_slip_and_absolute_names_refuse_the_archive(work, bad):
    """zip-slip: no member name with `..`, absolute, drive-letter, UNC, empty or `.` segment is accepted (I1)."""
    arch, _ = work
    path = build(arch, {bad: M("x")})
    with pytest.raises(ci.Refusal) as exc:
        ci.open_archive(path)
    assert "refused" in str(exc.value) and "expected" in str(exc.value)


def test_name_checks_that_a_zip_cannot_carry_are_pinned_on_the_function():
    """NUL and a control character are refused on the raw name (a zip writer truncates NUL, so the function is pinned directly)."""
    assert ci.name_problem("a\x00b") and ci.name_problem("a\x1b[2Jb") and ci.name_problem("..\\x") and ci.name_problem("\\\\srv\\share\\x")
    assert ci.name_problem("A/config.json") is None and ci.name_problem("a" * 300 + "/" + "/".join("d" * 3 for _ in range(30))) is None   # long and deep are legal (m-1)


def test_a_symlink_member_is_refused(work):
    arch, _ = work
    path = build(arch, {"A/link": M("target", attr=stat.S_IFLNK | 0o777)})
    with pytest.raises(ci.Refusal, match="not a regular file"):
        ci.open_archive(path)


def test_a_member_larger_than_declared_is_refused_at_and_beyond(work):
    """AT the declared bytes the member passes; one byte more streams past the cap and refuses (the header size is never believed)."""
    arch, _ = work
    ok = build(arch, {"A/x": M("12345")}, name=NAME)
    assert ci.open_archive(ok).members["A/x"].size == 5
    rows = [{"arc": "A/x", "src_rel": "x", "set": "A", "bytes": 5, "sha256": sha(b"123456"), "flags": []}]
    bad = build(arch, {"A/x": M("123456")}, rows=rows, name=NAME.replace("abababab", "cdcdcdcd"))
    with pytest.raises(ci.Refusal, match="larger than the manifest declares"):
        ci.open_archive(bad)


def test_the_file_ceiling_is_independent_of_the_manifest(work, monkeypatch):
    """M-2: a manifest that promises 10**12 bytes does not raise the cap; `file_max_bytes` AT passes, +1 refuses."""
    arch, _ = work
    monkeypatch.setitem(ci.limits(), "file_max_bytes", 50)
    assert ci.open_archive(build(arch, {"A/x": M("x" * 50)}, name=NAME)).members
    rows = [{"arc": "A/x", "src_rel": "x", "set": "A", "bytes": 10 ** 12, "sha256": sha(b"x" * 51), "flags": []}]
    with pytest.raises(ci.Refusal, match="larger than"):
        ci.open_archive(build(arch, {"A/x": M("x" * 51)}, rows=rows, name=NAME.replace("abababab", "cdcdcdcd")))


def test_the_archive_ceiling_counts_all_members(work, monkeypatch):
    arch, _ = work
    monkeypatch.setitem(ci.limits(), "archive_max_bytes", 10)
    ci.open_archive(build(arch, {"A/x": M("12345"), "A/y": M("12345")}, name=NAME))
    with pytest.raises(ci.Refusal, match="larger than"):
        ci.open_archive(build(arch, {"A/x": M("12345"), "A/y": M("123456")}, name=NAME.replace("abababab", "cdcdcdcd")))


def test_the_part_ceiling_is_at_and_beyond(work, monkeypatch):
    arch, _ = work
    path = build(arch, {"A/x": M(os.urandom(4000))})                       # the manifest (about 1 KB) must itself fit under the ceiling
    monkeypatch.setitem(ci.limits(), "part_max_bytes", path.stat().st_size)
    assert ci.open_archive(path).members
    monkeypatch.setitem(ci.limits(), "part_max_bytes", path.stat().st_size - 1)
    with pytest.raises(ci.Refusal, match="part ceiling"):
        ci.open_archive(path)


def test_a_member_missing_from_the_manifest_and_a_wrong_sha_refuse(work):
    arch, _ = work
    rows = [{"arc": "A/x", "src_rel": "x", "set": "A", "bytes": 1, "sha256": sha(b"x"), "flags": []}]
    with pytest.raises(ci.Refusal, match="not listed"):
        ci.open_archive(build(arch, {"A/x": M("x"), "A/y": M("y")}, rows=rows))
    rows[0]["sha256"] = sha(b"other")
    with pytest.raises(ci.Refusal, match="does not match"):
        ci.open_archive(build(arch, {"A/x": M("x")}, rows=rows, name=NAME.replace("abababab", "cdcdcdcd")))


@pytest.mark.parametrize("over", [{"install_id": "../" * 8}, {"project_id": "a/b"}, {"collected_at": "x/../../.."}, {"collected_at": "2026-13-45T00:00:00Z"},
                                  {"install_id": "AB" * 16}])
def test_hostile_identity_fields_are_refused_by_form_before_any_path_is_built(work, over):
    arch, inbox = work
    with pytest.raises(ci.Refusal, match="malformed|not a date"):
        ci.open_archive(build(arch, {"A/x": M("x")}, doc=over))
    assert files_under(inbox) == []


@pytest.mark.parametrize("schema,door", [("qa-collect/0", "collect again with the current plugin"), ("qa-collect/2", "update tools/"), ("zzz", "update tools/")])
def test_older_newer_and_unknown_schemas_refuse_by_name_with_their_door(work, schema, door):
    arch, _ = work
    with pytest.raises(ci.Refusal) as exc:
        ci.open_archive(build(arch, {"A/x": M("x")}, doc={"schema": schema}))
    assert door in str(exc.value) and "schema" in str(exc.value)


def test_not_zip_empty_truncated_deep_and_bom_inputs(work):
    arch, _ = work
    junk = arch / NAME
    for payload in (b"", b"not a zip at all", build(arch, {"A/x": M("x")}, name="t.zip").read_bytes()[:40]):
        junk.write_bytes(payload)
        with pytest.raises(ci.Refusal, match="not a (valid )?collect archive"):
            ci.open_archive(junk)
    deep = arch / "deep.zip"
    with zipfile.ZipFile(deep, "w") as zf:
        zf.writestr("manifest.json", "[" * 10000 + "]" * 10000)
    with pytest.raises(ci.Refusal, match="not JSON"):
        ci.open_archive(deep)
    bom = build(arch, {"A/x": M("x")}, name=NAME.replace("abababab", "efefefef"))
    raw = zipfile.ZipFile(bom).read("manifest.json")
    with zipfile.ZipFile(bom, "w") as zf:
        zf.writestr("manifest.json", b"\xef\xbb\xbf" + raw)
        zf.writestr("A/x", "x")
    assert ci.open_archive(bom).project_id == PID


def test_a_missing_main_part_refuses_a_missing_transcripts_part_is_the_persons_choice(work):
    """Q4 (t-1067): a deleted transcripts file is 'not sent', a vanished main part is a refusal naming it."""
    arch, _ = work
    base = NAME[:-4]
    t_row = {"arc": "transcripts/T/s.jsonl", "src_rel": "transcripts/T/s.jsonl", "set": "H", "bytes": 1, "sha256": sha(b"t"), "flags": ["transcript"]}
    parts = [{"name": base + "-transcripts.zip", "sha256": "0" * 64, "bytes": 1, "kind": "transcripts"}]
    path = build(arch, {}, rows=[t_row], extra_parts=parts)
    got = ci.open_archive(path)
    assert (got.transcripts_sent, got.transcripts_not_sent) == (0, 1)
    parts = [{"name": base + "-part2.zip", "sha256": "0" * 64, "bytes": 1}]
    with pytest.raises(ci.Refusal, match="part qa-collect-abababab-20261019T120000Z-part2.zip is missing"):
        ci.open_archive(build(arch, {}, rows=[], extra_parts=parts, name=NAME.replace("abababab", "cdcdcdcd")))


def test_part_names_from_the_manifest_are_read_by_form_not_as_paths(work):
    arch, _ = work
    for bad in ("../x.zip", "C:x.zip", "sub/qa-collect-abababab-20261019T120000Z-part2.zip", "evil.zip"):
        parts = [{"name": bad, "sha256": "0" * 64, "bytes": 1}]
        with pytest.raises(ci.Refusal, match="part entry"):
            ci.open_archive(build(arch, {}, rows=[], extra_parts=parts))


def test_part_count_beyond_the_limit_refuses(work, monkeypatch):
    arch, _ = work
    monkeypatch.setattr(ci, "MAX_PARTS", 1)
    parts = [{"name": NAME[:-4] + "-part2.zip", "sha256": "0" * 64, "bytes": 1}]
    with pytest.raises(ci.Refusal, match="part_count"):
        ci.open_archive(build(arch, {}, rows=[], extra_parts=parts))


def test_a_later_part_as_argument_is_absorbed_or_refused_naming_the_first(work):
    arch, _ = work
    first = arch / NAME
    later = arch / (NAME[:-4] + "-part2.zip")
    assert ci.group_args([first, later]) == ([first], [])
    firsts, refusals = ci.group_args([later])
    assert firsts == [] and "first part" in str(refusals[0][1]) and NAME in str(refusals[0][1])


def test_the_real_pack_archive_is_read_and_the_schema_pin_holds(tmp_path):
    """The intake reads the real collector's output (axis 6): the manifest keys it requires are the ones `collect_pack` writes."""
    arc = real_archive(tmp_path)
    got = ci.open_archive(arc)
    assert set(ci.REQUIRED) <= set(got.manifest) and got.manifest["schema"] == ci.collect_pack.SCHEMA
    assert got.identity.startswith(got.install8 + "-" + got.stamp + "-")
    assert len(got.project_id) == 12 and len(got.install_id) == 32


def real_archive(tmp_path):
    sys.path.insert(0, str(ci.REPO / "ai-packages" / "qa-factory" / "scripts"))
    import collect_pack as cp
    import machine_facts as mf
    root = tmp_path / "proj"
    (root / "qa-factory").mkdir(parents=True)
    cfg = json.loads((cp.PACKAGE_ROOT / "references" / "templates" / "config.json").read_text(encoding="utf-8"))
    cfg["tests_root"], cfg["app_root"] = "tests", "."
    (root / "qa-factory" / "config.json").write_text(json.dumps(cfg), encoding="utf-8")
    (root / "qa-factory" / "records").mkdir()
    (root / "qa-factory" / "records" / "project-decisions.json").write_text(fb_json(("FB-1", "`scripts/forge_thing.py` loses a line", "seen twice; idempotency:k1")), encoding="utf-8")
    story = root / "qa-factory" / "artifacts" / "TP1-12345"
    story.mkdir(parents=True)
    (story / "pipeline.json").write_text(json.dumps({"plugin_version": "0.9.0"}), encoding="utf-8")
    (story / "retro.md").write_text("# retro\n\n## What went wrong, and what to do about it\n\nthe gate said no twice, see `scripts/traceability.py`\n\n## Other\n\nx\n", encoding="utf-8")
    (tmp_path / "words.txt").write_text("the first step was slow", encoding="utf-8")
    red = mf.compile_redactor(mf.load_rules(), project_root=str(root), plugin_root=str(cp.PACKAGE_ROOT), pythons=(sys.executable,), home="C:\\Users\\Zq", tmp=tempfile.gettempdir(),
                              identities={"users": ["Zq"], "display_names": [], "emails": [], "machine": [], "domain": []}, short=lambda p: None)
    res = cp.pack(root, problems_file=str(tmp_path / "words.txt"), now=datetime.datetime(2026, 10, 19, 12, 0, tzinfo=datetime.timezone.utc), git=lambda p, *a: (124, ""),
                  redactor=red, temp_root=tmp_path / "packout", rules_sha=mf.rules_sha256())
    return Path(res["archive"])


# ---------------------------------------------------------------- the whole loop on a scratch pile tree

def test_plan_mode_writes_nothing_and_prints_the_detector_and_equality_lines(tree, work, capsys):
    scratch_tree(tree)
    arch, inbox = work
    before = kit.tree_state(tree)
    code, out, _ = run(tree, inbox, fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` loses a line", "w")]), capsys=capsys)
    assert code == 0 and kit.tree_state(tree) == before and not inbox.exists()
    assert "ARCHIVE abababab-20261019T120000Z project %s | package_modified: no | why: match | running_version: 0.9.1 | install: cache" % PID in out
    assert "ELEMENTS in=1 placed=1 unplaced=0 duplicate=0 dropped=0" in out and "SOURCES fb=1" in out and "plan only" in out


def test_apply_writes_the_inbox_and_one_finding_prints_the_rows_and_check_agrees(tree, work, capsys):
    """DoD: before the Lead's rows are inserted check (е) is red on the new finding (negative control); after, it is green."""
    scratch_tree(tree)
    arch, inbox = work
    code, out, _ = run(tree, inbox, fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` loses a line", "w")]), apply=True, capsys=capsys)
    name = "20261020-1230-collect-abababab.md"
    assert code == 0 and "wrote plans/piles/forge/findings/" + name in out
    finding = tree / "plans/piles/forge/findings" / name
    parsed = piles.parse_finding(finding.read_text(encoding="utf-8"), "plans/piles/forge/findings/" + name)
    assert parsed.pile == "forge" and parsed.source.startswith("collect abababab-20261019T120000Z-") and parsed.source.endswith("20.10.2026") and not parsed.errors
    assert piles.main(["--repo", str(tree), "check", "--all"]) == 2                      # (е): the finding is named in no row yet
    row = next(l for l in out.splitlines() if l.startswith("| ") and "Lead" in l)
    batch = tree / "plans/piles/forge/batch-2-next.md"
    text = batch.read_text(encoding="utf-8")
    batch.write_text(text.replace("\n## Ход", row + "\n\n## Ход", 1), encoding="utf-8")
    assert "NODE ROW" in out and "CONTENTS ROW" in out
    assert piles.main(["--repo", str(tree), "check", "--all"]) == 0
    assert files_under(inbox)[0].endswith("index.json") or "index.json" in " ".join(files_under(inbox))


def test_hostile_text_never_becomes_structure_of_the_finding(tree, work, capsys):
    """I8: a fence, `перенос:`, `<!--`, `id: B-999`, a table row, a heading, U+2028 and a lone CR inside an FB text: the finding keeps one
    closed fence that is longer than any backtick run, `_finding_moves` is empty and `check --all` ends as without the text."""
    scratch_tree(tree)
    arch, inbox = work
    evil = "see `scripts/forge_thing.py`\n```\nперенос: forge/x\n<!--\nid: B-999\n| a | b |\n# заголовок\nсделано: abc1234\n````````\u2028x\ry"
    code, _out, _ = run(tree, inbox, fb_archive(arch, [("FB-1", evil, "w")]), apply=True, capsys=capsys)
    path = next((tree / "plans/piles/forge/findings").glob("20261020-*"))
    text = path.read_text(encoding="utf-8")
    parsed = piles.parse_finding(text, "plans/piles/forge/findings/" + path.name)
    assert code == 0 and not parsed.errors and piles._finding_moves(parsed) == []
    fence = next(l for l in text.split("\n") if l.startswith("`"))
    assert len(fence) >= 9 and text.count(fence + "\n") == 2 and "\r" not in text and "\u2028" not in text
    assert piles.unclosed_fence(text.split("\n")) is None
    assert "перенос: forge/x" in text                              # inside the fence only: data, not a command


def test_hostile_ids_become_hashes_and_never_reach_the_key_grammar(tree, work, capsys):
    """M-6: a TASK with `=`, space, `<!--` or U+202E gets `h<sha12>`; the same raw string gives the same id."""
    scratch_tree(tree)
    arch, inbox = work
    for raw in ("a=b c", "<!--", "x\u202ey", "a" * 65):
        assert ci.safe_id(raw) == "h" + ci.sha12(raw) and ci.PLACE_KEY_RE.fullmatch("abababab:retro:" + ci.safe_id(raw))
    assert ci.safe_id("TP1-12345.a_b") == "TP1-12345.a_b" and ci.safe_id("FB-12", ci.FB_ID_RE) == "FB-12" and ci.safe_id("FB-x", ci.FB_ID_RE).startswith("h")


def test_apply_with_unplaced_writes_the_inbox_not_the_findings_and_exits_3(tree, work, capsys):
    """M-3: an unplaced element blocks the FINDINGS of the archive; the inbox (the evidence) is written; the archive is not taken."""
    scratch_tree(tree)
    arch, inbox = work
    words = {"problems": {"state": "answered", "arc": "answers/problems.txt"}, "suggestions": {"state": "blank", "arc": None}}
    path = build(arch, {"answers/problems.txt": M("it was slow", "A", flags=["answer"]), D2: M(fb_json(("FB-1", "`scripts/forge_thing.py` x", "w")), "D", D2)}, doc={"answers": words})
    code, out, _ = run(tree, inbox, path, apply=True, capsys=capsys)
    assert code == 3 and "UNPLACED abababab:answer-problems:" in out and "ELEMENTS in=2 placed=1 unplaced=1" in out
    assert not list((tree / "plans/piles/forge/findings").glob("2026102*"))
    assert (inbox / PID / ci.open_archive(path).sha[:ci.FOLDER_HEX] / "elements.json").is_file() and (inbox / PID / ci.open_archive(path).sha[:ci.FOLDER_HEX] / "members").is_dir()
    assert json.loads((inbox / "index.json").read_text(encoding="utf-8"))["archives"] == {}
    key = next(l.split(" | ")[0].split()[1] for l in out.splitlines() if l.startswith("UNPLACED"))
    code, out, _ = run(tree, inbox, path, apply=True, place=[key + "=proposals"], capsys=capsys)
    assert code == 0 and "wrote plans/piles/proposals/findings/" in out and "wrote plans/piles/forge/findings/" in out


def test_place_syntax_unknown_pile_unknown_key_and_none_with_a_reason(tree, work, capsys):
    scratch_tree(tree)
    arch, inbox = work
    path = build(arch, {"answers/problems.txt": M("slow", "A", flags=["answer"])}, doc={"answers": {"problems": {"state": "answered", "arc": "answers/problems.txt"}}})
    code, out, err = run(tree, inbox, path, capsys=capsys)
    key = next(l.split(" | ")[0].split()[1] for l in out.splitlines() if l.startswith("UNPLACED"))
    for bad, why in (("nokey", "malformed"), (key + "=Nope", "does not exist"), ("deadbeef:retro:zz=forge", "not an unplaced element"), (key + "=none:", "without a reason")):
        code, _o, err = run(tree, inbox, path, place=[bad], capsys=capsys)
        assert code == 1 and why in err
    code, out, _ = run(tree, inbox, path, place=[key + "=none:noise"], capsys=capsys)
    assert code == 0 and "dropped=1" in out


def test_a_pile_with_no_untaken_batch_prints_the_open_batch_row_and_exits_3(tree, work, capsys):
    """D-0044: report-delivery has no batch at all: the finding is written, the card row and the file name are printed, exit 3."""
    scratch_tree(tree)
    arch, inbox = work
    code, out, _ = run(tree, inbox, fb_archive(arch, [("FB-1", "`scripts/traceability.py` x", "w")]), apply=True, capsys=capsys)
    assert code == 3 and "OPEN BATCH report-delivery 1" in out and "batch-1-sbor.md" in out and "| 1 | разбор находок сбора |" in out


def test_the_same_archive_twice_is_idempotent_and_a_lost_index_finds_the_finding(tree, work, capsys):
    scratch_tree(tree)
    arch, inbox = work
    path = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")])
    run(tree, inbox, path, apply=True, capsys=capsys)
    folder = tree / "plans/piles/forge/findings"
    one = sorted(p.name for p in folder.glob("2026102*"))
    code, out, _ = run(tree, inbox, path, apply=True, capsys=capsys)
    assert code == 0 and "already taken" in out and sorted(p.name for p in folder.glob("2026102*")) == one
    (inbox / "index.json").unlink()                                   # a crash between the findings and the index
    code, out, _ = run(tree, inbox, path, apply=True, capsys=capsys)
    assert code == 0 and "already written: " + one[0] in out and sorted(p.name for p in folder.glob("2026102*")) == one and "NODE ROW" in out


def test_two_archives_of_one_installation_are_both_kept_and_dedup_works(tree, work, capsys):
    """Edge 1/2: the second archive of the same (project, install) drops the repeated FB and keeps the new one; both are taken."""
    scratch_tree(tree)
    arch, inbox = work
    a = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")])
    b = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w"), ("FB-2", "`scripts/forge_thing.py` y", "w")], name=NAME.replace("120000", "130000"),
                   doc={"collected_at": "2026-10-19T13:00:00Z"})
    code, out, _ = run(tree, inbox, b, a, apply=True, capsys=capsys)                       # given in the wrong order: collected_at decides
    assert code == 0 and "duplicate=1" in out and len(list((tree / "plans/piles/forge/findings").glob("2026102*"))) == 2
    assert len(json.loads((inbox / "index.json").read_text(encoding="utf-8"))["archives"]) == 2


def test_another_installation_of_the_same_project_is_never_a_duplicate(tree, work, capsys):
    """I4 ('две установки'): the same FB text from another install_id is new."""
    scratch_tree(tree)
    arch, inbox = work
    a = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")])
    b = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")], name=NAME.replace("abababab", "cdcdcdcd"), doc={"install_id": "cd" * 16})
    code, out, _ = run(tree, inbox, a, b, apply=True, capsys=capsys)
    assert "duplicate=0" in out and "duplicate=1" not in out


def test_an_older_archive_after_a_newer_one_does_not_roll_the_status_back(tree, work, capsys):
    """Conflict pair (1): FB status newer wins; an older archive arriving later is a duplicate, not a change."""
    scratch_tree(tree)
    arch, inbox = work
    new = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")], doc={"collected_at": "2026-10-19T14:00:00Z"}, name=NAME.replace("120000", "140000"))
    run(tree, inbox, new, apply=True, capsys=capsys)
    rows = json.loads(fb_json(("FB-1", "`scripts/forge_thing.py` x", "w")))
    rows["findings"][0]["status"] = "closed"
    old = build(arch, {D2: M(json.dumps(rows), "D", D2)}, doc={"collected_at": "2026-10-19T09:00:00Z"}, name=NAME.replace("120000", "090000"))
    code, out, _ = run(tree, inbox, old, apply=True, capsys=capsys)
    assert code == 0 and "duplicate=1" in out and "older than" in out


def test_the_residue_second_line_holds_an_element_and_no_byte_of_it_is_printed_or_written(tree, work, capsys):
    """I7: the excerpt of an element whose unpacked text still carries a secret is replaced; the text stays in the inbox only."""
    scratch_tree(tree)
    arch, inbox = work
    secret = "password: hunter2hunter2xx"
    path = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` leaks " + secret, "w"), ("FB-2", "`scripts/forge_thing.py` clean", "w")])
    code, out, _ = run(tree, inbox, path, apply=True, capsys=capsys)
    assert code == 3 and "held: secret" in out and "hunter2" not in out and "held=1" in out
    assert not list((tree / "plans/piles/forge/findings").glob("2026102*"))
    assert "hunter2" in (inbox / PID / ci.open_archive(path).sha[:ci.FOLDER_HEX] / "elements.json").read_text(encoding="utf-8")
    key = next(l.split()[1] for l in out.splitlines() if l.startswith("UNPLACED"))
    code, out, _ = run(tree, inbox, path, apply=True, place=[key + "=forge"], capsys=capsys)
    written = next((tree / "plans/piles/forge/findings").glob("2026102*")).read_text(encoding="utf-8")
    assert code == 0 and "hunter2" not in written and "(held: secret)" in written


@pytest.mark.parametrize("text", ["Bearer eyJhbGciOiJIUzI1NiJ9.abc.def", "C:\\Users\\Someone\\proj", "https://localhost:p@localhost/x", "-----BEGIN PRIVATE KEY-----"])
def test_residue_catches_the_machine_independent_leaks_and_not_a_name(text):
    assert ci.residue_category("x " + text) is not None
    assert ci.residue_category("Alexandra_Testova wrote this") is None        # the limit of this line: it knows no names (positive control of the impossible)


def test_residue_reads_a_json_shaped_key_of_an_element_with_the_detectors_on():
    """t-1206 C2-1/C2-2: an element text is read by `residue_document` (kind text, line by line): a token-shaped JSON-shaped KEY is a leak."""
    assert ci.residue_category(json.dumps({"ghp_" + "Q" * 36: 1})) == "secret"
    assert ci.residue_category(json.dumps({"region": "eu", "note": "plain"})) is None        # positive control: the same shape, clean
    assert ci.residue_category("") is None                                                    # an empty element is not a leak


def test_sources_line_detects_an_element_lost_before_the_layout(tree, work, capsys, monkeypatch):
    """M-4: the SOURCES count comes from the manifest, so a lay-out that skips a source row shows as a mismatch (exit 1)."""
    scratch_tree(tree)
    arch, inbox = work
    path = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w"), ("FB-2", "`scripts/forge_thing.py` y", "w")])
    real = ci.build_elements
    monkeypatch.setattr(ci, "build_elements", lambda arc, idx: real(arc, idx)[:-1])
    code, out, _ = run(tree, inbox, path, capsys=capsys)
    assert code == 1 and "SOURCES MISMATCH: fb" in out


def test_placement_errs_only_toward_unplaced(tree):
    """The uncomfortable inputs of t-1075 section 4: a foreign tag, words only, a bare name, `..`, an absolute path, module.func, 201 paths."""
    scratch_tree(tree)
    placer = ci.Placer(Path(tree), piles.load_tree(tree))
    def place(text):
        el = {"kind": "FB", "text": text, "place": None, "why": "", "candidates": []}
        placer.place(el)
        return el
    assert place("[F08] words about S5 gate")["place"] is None                       # a tag and words decide nothing
    assert place("controller.py is slow")["place"] is None and place("`traceability.py`")["place"] is None     # a bare name is a candidate
    assert place("`../scripts/traceability.py` `/etc/scripts/traceability.py` `json.loads`")["place"] is None
    assert place("`<project>/scripts/story_run.py`")["place"] is None
    assert place("`scripts/traceability.py`")["place"] == "report-delivery" and place("`<plugin>/scripts/forge_thing.py`")["place"] == "forge"
    many = " ".join("`dir%d/f.py`" % i for i in range(ci.MAX_PATHS)) + " `scripts/traceability.py`"
    assert place(many)["place"] is None and "too many" in place(many)["why"]                      # 201 tokens
    assert place(" ".join("`dir%d/f.py`" % i for i in range(ci.MAX_PATHS - 1)) + " `scripts/traceability.py`")["place"] == "report-delivery"     # AT 200


def test_two_piles_of_one_feature_are_told_apart_by_the_zone_with_braces(tree, work, capsys):
    """'зона со скобками': forge (zone `tools/`) and cost-dashboard (zone `scripts/{forge_thing,x}.py`) both carry F19; the zone picks exactly one."""
    scratch_tree(tree)
    arch, inbox = work
    kit.edit(tree, "plans/piles/cost-dashboard/README.md", "фичи: F14", "фичи: F14, F19")
    kit.edit(tree, "plans/piles/cost-dashboard/README.md", "зона: `tools/`", "зона: `scripts/{forge_thing,x}.py`")
    _c, out, _ = run(tree, inbox, fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w"), ("FB-2", "`scripts/traceability.py` y", "w")]), capsys=capsys)
    assert "placed=2" in out
    _c, out, _ = run(tree, inbox, fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")], name=NAME.replace("abababab", "cdcdcdcd"), doc={"install_id": "cd" * 16}),
                     apply=True, capsys=capsys)
    assert list((tree / "plans/piles/cost-dashboard/findings").glob("2026102*")) and not list((tree / "plans/piles/forge/findings").glob("2026102*"))
    kit.edit(tree, "plans/piles/cost-dashboard/README.md", "scripts/{forge_thing,x}.py", "tools/")        # both zones now `tools/`: no single zone matches -> the Lead
    _c, out, _ = run(tree, inbox, fb_archive(arch, [("FB-3", "`scripts/forge_thing.py` z", "w")], name=NAME.replace("abababab", "efefefef"), doc={"install_id": "ef" * 16}), capsys=capsys)
    assert "UNPLACED" in out and "candidates: cost-dashboard, forge" in out


def test_a_card_zone_is_read_by_parse_zone_only():
    """I3: one reader; braces expand one level, `…` and a trailing `/` mean everything below, nested braces are an error that matches nothing."""
    assert piles.parse_zone("`ai-packages/qa-factory/scripts/{a,b}.py`, `tools/`, `x/{y,z}/…`") == (["scripts/a.py", "scripts/b.py", "tools/**", "x/y/**", "x/z/**"], [])
    assert piles.parse_zone("—") == ([], []) and piles.parse_zone("") == ([], [])
    pats, errs = piles.parse_zone("`a/{b,{c}}.py`, `ok.py`, `bad name.py`")
    assert pats == ["ok.py"] and len(errs) == 2
    assert piles.parse_zone("tools/y*.py")[0] == ["tools/y*.py"]                    # a one-token zone reaches us unwrapped by header_pairs
    text = (ci.REPO / "plans/piles/codex/README.md").read_text(encoding="utf-8")
    card = piles.parse_card(text, "plans/piles/codex/README.md")
    pats, errs = piles.parse_zone(card.zone)
    assert "scripts/host_adapter.py" in pats and "references/controller-api.md" in pats and errs == []


def test_inbox_doors_in_tree_absent_and_unreadable_index(tree, work, capsys, tmp_path):
    scratch_tree(tree)
    arch, inbox = work
    path = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")])
    code, _o, err = run(tree, tree / "inbox", path, apply=True, capsys=capsys)
    assert code == 1 and "inside the repository" in err and "--inbox" in err and not (tree / "inbox").exists()
    code, _o, err = run(tree, None, path, apply=True, capsys=capsys)
    assert code == 1 and "no inbox is configured" in err and "QA_COLLECT_INBOX" in err
    code, out, _ = run(tree, None, path, capsys=capsys)
    assert code == 0 and "dedup not checked: no inbox" in out                       # plan with no inbox: an empty index, said aloud
    inbox.mkdir()
    (inbox / "index.json").write_text("{broken", encoding="utf-8")
    code, _o, err = run(tree, inbox, path, apply=True, capsys=capsys)
    assert code == 1 and "cannot be read" in err and (inbox / "index.json").read_text(encoding="utf-8") == "{broken"


def test_an_inbox_inside_another_git_tree_is_refused_and_unknown_is_refused(tmp_path, monkeypatch):
    other = tmp_path / "other"
    other.mkdir()
    kit.git(other, "init", "-q")
    assert "inside a git work tree" in ci.inbox_problem(other / "deep" / "inbox", tmp_path / "repo")
    assert ci.inbox_problem(tmp_path / "plain", tmp_path / "repo") is None
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))                              # m-5: the environment must not steer the probe
    assert ci.inbox_problem(tmp_path / "plain", tmp_path / "repo") is None
    monkeypatch.setattr(ci.gitcmd, "git", lambda *a, **k: (-1, b"", b"no git"))
    assert "could not say" in ci.inbox_problem(tmp_path / "plain", tmp_path / "repo")


def test_the_finding_name_carries_the_intake_time_not_the_archive_stamp(tree, work, capsys):
    """M-1 / second archive of a day: two archives of one install in one minute get `-2`, never an exit 2."""
    scratch_tree(tree)
    arch, inbox = work
    a = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")])
    b = fb_archive(arch, [("FB-2", "`scripts/forge_thing.py` y", "w")], name=NAME.replace("120000", "120001"), doc={"collected_at": "2026-10-19T12:00:01Z"})
    code, _o, _ = run(tree, inbox, a, b, apply=True, capsys=capsys)
    names = sorted(p.name for p in (tree / "plans/piles/forge/findings").glob("2026102*"))
    assert code == 0 and names == ["20261020-1230-collect-abababab-2.md", "20261020-1230-collect-abababab.md"]


def test_limits_excerpt_and_elements_per_finding_at_and_beyond():
    assert ci.excerpt("x" * 200) == "x" * 200 and ci.excerpt("x" * 201) == "x" * 200 + "…[+1]"
    assert ci.excerpt("a\u2028b\rc") == "a?b?c"
    arc = type("A", (), {"install8": "abababab", "stamp": "20261019T120000Z", "identity": "i", "project_id": PID, "sha": "s" * 64})()
    mk = lambda n: [{"pkey": "abababab:FB:FB-%d" % i, "kind": "FB", "status": "new", "text": "t", "held": None} for i in range(n)]
    at = ci.finding_text(arc, "forge", mk(50), "20.10.2026")
    beyond = ci.finding_text(arc, "forge", mk(51), "20.10.2026")
    assert "more:" not in at and "1 more: " in beyond and "FB-49 |" in beyond and "FB-50 |" not in beyond
    assert "- 1 more: %s/%s/elements.json" % (PID, "s" * ci.FOLDER_HEX) in beyond.split("\n")         # F-10: the pointer is relative to the inbox


def test_the_intake_does_not_shadow_a_tools_module():
    """m-16: `collect_pack` puts the package scripts/ first on sys.path; the two folders must share no module name (control: a folder with itself)."""
    tools = {p.name for p in TOOLS.glob("*.py")}
    scripts = {p.name for p in (ci.REPO / "ai-packages/qa-factory/scripts").glob("*.py")}
    assert tools & tools and tools & scripts == set()


def test_unknown_set_and_old_archive_without_the_new_fields(tree, work, capsys):
    """Temporal (a): an archive of the older collector has no `_why`/`_detail`: the detector line says absent, nothing is invented."""
    scratch_tree(tree)
    arch, inbox = work
    rows = [{"arc": "Z/x", "src_rel": "z", "set": "Z", "bytes": 1, "sha256": sha(b"x"), "flags": []}]
    path = build(arch, {"Z/x": M("x", "Z")}, rows=rows, doc={"package_modified": "unknown", "package_modified_why": None, "package_modified_detail": None})
    code, out, _ = run(tree, inbox, path, capsys=capsys)
    assert code == 0 and "package_modified: unknown | why: absent | running_version: absent | install: absent" in out
    assert "unknown set Z: 1 rows" in out and "ELEMENTS in=0 placed=0 unplaced=0 duplicate=0 dropped=0" in out


def test_ansi_in_a_printed_value_is_neutralised(tree, work, capsys):
    scratch_tree(tree)
    arch, inbox = work
    path = build(arch, {"A/x": M("x")}, doc={"package_modified_detail": {"running_version": "\x1b[2J" + "9" * 10000, "install": "cache"}})
    _c, out, _ = run(tree, inbox, path, capsys=capsys)
    line = next(l for l in out.splitlines() if l.startswith("ARCHIVE"))
    assert "\x1b" not in out and len(line) < 400


def test_a_story_that_looped_is_laid_out_like_a_stalled_one(tree, work, capsys):
    """CL3-9 (AR-22): the reader of the packer's new `looped` / `loop_signals`. Not stalled but looped, or looping unknown: one `stall`
    element each; looped False, and an archive of an older packer with no `looped` key: nothing, as before."""
    scratch_tree(tree)
    arch, inbox = work
    stories = [{"task": "T1", "stalled": False, "looped": True, "loop_signals": [{"id": "L2", "where": "driver-state.json window_rounds", "at": None}]},
               {"task": "T2", "stalled": False, "looped": None, "loop_signals": []},
               {"task": "T3", "stalled": False, "looped": False, "loop_signals": []},
               {"task": "T4", "stalled": False}]
    path = build(arch, {}, doc={"stories": stories})
    _code, out, _ = run(tree, inbox, path, capsys=capsys)
    assert "ELEMENTS in=2" in out and "stall=2 " in out
    assert ci.stall_laid_out(stories[0]) and ci.stall_laid_out(stories[1])
    assert not ci.stall_laid_out(stories[2]) and not ci.stall_laid_out(stories[3])


def test_the_layout_text_of_a_looped_only_story_says_stalled_no(monkeypatch):
    """CL3-9 B-1 (AR-22, FR-41): the TEXT, not the count. Looped and not stalled is `stalled: no`, never `unknown`; stalled None is
    `unknown`; stalled True is `yes`."""
    texts = {}
    monkeypatch.setattr(ci, "make_element", lambda arc, kind, raw_id, text, origin, **kw: texts.setdefault(raw_id, text))
    arc = types.SimpleNamespace(manifest={"stories": [
        {"task": "T1", "stalled": False, "looped": True, "loop_signals": [{"id": "L1", "where": "w", "at": "x"}]},
        {"task": "T2", "stalled": None, "looped": False}, {"task": "T3", "stalled": True, "looped": None}]})
    ci.stall_elements(arc)
    assert texts["T1"] == "stalled: no\nlooped: yes\nL1 | w | x"
    assert texts["T2"].splitlines()[0] == "stalled: unknown" and texts["T3"].splitlines()[0] == "stalled: yes"
    assert texts["T3"].splitlines()[1] == "looped: unknown"


def test_a_stalled_story_and_a_retro_become_elements_with_safe_ids(tree, work, capsys):
    scratch_tree(tree)
    arch, inbox = work
    retro = "# r\n\n## What went wrong, and what to do about it\n\nit stalled at `scripts/traceability.py`\n\n## Next\n\nz\n"
    rel = "artifacts/TP1-12345/retro.md"
    stories = [{"task": "a=b c", "stalled": True, "stall_signals": [{"id": "K1", "where": "S5", "at": None}]}, {"task": "T2", "stalled": None, "stall_signals": []},
               {"task": "T3", "stalled": False}]
    path = build(arch, {rel: M(retro, "F", rel)}, doc={"stories": stories})
    code, out, _ = run(tree, inbox, path, capsys=capsys)
    assert "ELEMENTS in=3" in out and "SOURCES fb=0 retro=1 (no_section=0) stall=2 answers=0 -> elements 3" in out
    assert "abababab:stall:h" in out and "abababab:retro:TP1-12345" not in out.replace("UNPLACED", "")[:0]
    no_section = build(arch, {rel: M("# r\n\nnothing\n", "F", rel)}, name=NAME.replace("abababab", "cdcdcdcd"), doc={"install_id": "cd" * 16})
    _c, out, _ = run(tree, inbox, no_section, capsys=capsys)
    assert "retro=0 (no_section=1)" in out


# ---------------------------------------------------------------- the fix round (t-1099 / attempt 2 of t-1066): t-1094 F-1..F-5, F-10

def apply_fb(tree, work, capsys, **kw):
    scratch_tree(tree)
    arch, inbox = work
    path = fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` loses a line", "w")])
    return path, inbox, run(tree, inbox, path, apply=True, capsys=capsys, **kw)


def forge_findings(tree):
    return sorted(p.name for p in (tree / "plans/piles/forge/findings").glob("2026102*"))


def rewrite_index(inbox):
    """What a parallel run does to the inbox while this one works: the index is replaced by other bytes."""
    Path(inbox).mkdir(parents=True, exist_ok=True)
    (Path(inbox) / "index.json").write_text(json.dumps({**ci.EMPTY_INDEX, "places": {"p/i/FB/FB-9": {"slug": "forge", "why": "a parallel run"}}}), encoding="utf-8")


def test_an_index_that_changed_is_found_before_a_single_finding_is_written(tree, work, capsys, monkeypatch):
    """F-1 / P4: the sha is compared BEFORE `write_findings` runs (a spy proves the call never happens), so 'no finding is kept' is true
    without a rollback; the refusal keeps the FR-1 form (what; expected; door)."""
    scratch_tree(tree)
    arch, inbox = work
    real_inbox, real_findings, calls = ci.write_inbox, ci.write_findings, []
    monkeypatch.setattr(ci, "write_inbox", lambda *a, **k: (real_inbox(*a, **k), rewrite_index(inbox))[0])
    monkeypatch.setattr(ci, "write_findings", lambda *a, **k: calls.append(1) or real_findings(*a, **k))
    code, _out, err = run(tree, inbox, fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")]), apply=True, capsys=capsys)
    assert code == 1 and calls == [] and forge_findings(tree) == []
    assert "REFUSED" in err and "the inbox index changed during the run" in err and "expected the index as it was read" in err and "run the intake again" in err


def test_an_index_that_changes_after_the_findings_takes_this_archives_findings_back(tree, work, capsys, monkeypatch):
    """F-1 / P4 (the race that is left): the findings are on disk when `save_index` refuses; they are removed and the refusal names them."""
    scratch_tree(tree)
    arch, inbox = work
    real_findings = ci.write_findings
    def racing(*a, **k):
        got = real_findings(*a, **k)
        assert forge_findings(tree) == ["20261020-1230-collect-abababab.md"]            # the control: the file really was there
        rewrite_index(inbox)
        return got
    monkeypatch.setattr(ci, "write_findings", racing)
    code, _out, err = run(tree, inbox, fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")]), apply=True, capsys=capsys)
    assert code == 1 and forge_findings(tree) == []
    assert "the inbox index changed during the run" in err and "expected" in err and "removed again: plans/piles/forge/findings/20261020-1230-collect-abababab.md" in err
    assert [f for f in files_under(inbox) if f.endswith(".tmp")] == []


def test_an_oserror_on_the_index_is_a_refusal_with_the_findings_taken_back_and_no_debris(tree, work, capsys, monkeypatch):
    """F-1 / P4b + F-4: `os.replace` of the index fails -> an FR-1 refusal (no traceback), this archive's finding is gone, the index file is
    absent (never half written), and no `*.tmp` stays in the inbox (the shared atomic writer unlinks its temp)."""
    scratch_tree(tree)
    arch, inbox = work
    real_replace = os.replace
    def failing(src, dst):
        if os.path.basename(str(dst)) == "index.json":
            raise OSError("disk full (probe)")
        return real_replace(src, dst)
    monkeypatch.setattr(os, "replace", failing)
    code, _out, err = run(tree, inbox, fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")]), apply=True, capsys=capsys)
    assert code == 1 and forge_findings(tree) == [] and not (inbox / "index.json").exists()
    assert "the inbox index could not be saved (disk full (probe))" in err and "expected a writable inbox folder" in err and "run the intake again" in err
    assert "removed again: plans/piles/forge/findings/20261020-1230-collect-abababab.md" in err
    assert [f for f in files_under(inbox) if f.endswith(".tmp")] == [] and "Traceback" not in err


def test_a_finding_that_cannot_be_removed_is_named_in_the_refusal(tree, work, capsys, monkeypatch):
    """F-1 'best effort, the refusal lists them': when the unlink itself fails the refusal says which file to delete by hand."""
    scratch_tree(tree)
    arch, inbox = work
    real_replace, real_unlink = os.replace, Path.unlink
    monkeypatch.setattr(os, "replace", lambda s, d: (_ for _ in ()).throw(OSError("boom")) if os.path.basename(str(d)) == "index.json" else real_replace(s, d))
    monkeypatch.setattr(Path, "unlink", lambda self, *a, **k: (_ for _ in ()).throw(PermissionError("locked")) if self.name.endswith("-collect-abababab.md") else real_unlink(self, *a, **k))
    code, _out, err = run(tree, inbox, fb_archive(arch, [("FB-1", "`scripts/forge_thing.py` x", "w")]), apply=True, capsys=capsys)
    assert code == 1 and "could NOT be removed, delete them by hand: plans/piles/forge/findings/20261020-1230-collect-abababab.md" in err


def test_sources_count_the_raw_findings_so_a_dropped_row_is_a_real_mismatch(tree, work, capsys):
    """F-2 / P6: D2 with 3 findings rows, 2 of them not objects -> SOURCES fb=3 with unreadable=2 against 1 element: the mismatch is shown,
    exit 1, and one WARNING names the cause. (The old count came from the filtered list the elements come from: fb=1, silence.)"""
    scratch_tree(tree)
    arch, inbox = work
    row = json.loads(fb_json(("FB-1", "`scripts/forge_thing.py` x", "w")))["findings"][0]
    code, out, _ = run(tree, inbox, build(arch, {D2: M(json.dumps({"findings": [row, "junk", 7]}), "D", D2)}), capsys=capsys)
    assert code == 1 and "SOURCES fb=3 " in out and "-> elements 1 | raep=0 unreadable=2" in out and "SOURCES MISMATCH: fb" in out
    assert [l for l in out.splitlines() if l.startswith("WARNING D2 (records/project-decisions.json) has 2 findings row(s) that are not objects")]


def test_a_d2_that_does_not_parse_is_said_aloud_and_d1_is_counted_by_its_raw_lines(tree, work, capsys):
    """F-2: D2 present but not JSON -> WARNING 'D2 present, unreadable' (never fb=0 in silence); the fall-back D1 is counted as the `| FB-n`
    lines of its raw text, so a row the table reader skips (outside its section) is a mismatch, not a silent drop."""
    scratch_tree(tree)
    arch, inbox = work
    code, out, _ = run(tree, inbox, build(arch, {D2: M("{broken", "D", D2)}), capsys=capsys)
    assert code == 0 and "WARNING D2 present, unreadable" in out and "SOURCES fb=0 " in out
    table = "| id | essence | scope | witness/details | created | status | decision |\n|---|---|---|---|---|---|---|\n"
    row = "| FB-1 | `scripts/forge_thing.py` x | local-calibration | w | 2026-10-19 | open | — |\n"
    d1 = lambda tail: "# backlog\n\n## Findings about the factory\n\n" + table + row + tail
    good = build(arch, {D2: M("{broken", "D", D2), "factory-backlog.md": M(d1(""), "D", "factory-backlog.md")}, name=NAME.replace("abababab", "cdcdcdcd"), doc={"install_id": "cd" * 16})
    code, out, _ = run(tree, inbox, good, capsys=capsys)
    assert code == 0 and "WARNING D2 present, unreadable" in out and "SOURCES fb=1 " in out and "MISMATCH" not in out
    stray = d1("\n## Other\n\n| FB-2 | stray | local-calibration | w | 2026-10-19 | open | — |\n")
    bad = build(arch, {"factory-backlog.md": M(stray, "D", "factory-backlog.md")}, name=NAME.replace("abababab", "efefefef"), doc={"install_id": "ef" * 16})
    code, out, _ = run(tree, inbox, bad, capsys=capsys)
    assert code == 1 and "SOURCES fb=2 " in out and "-> elements 1" in out and "SOURCES MISMATCH: fb" in out


def test_ra_ep_records_join_the_sources_and_a_record_outside_the_id_form_is_a_warning(tree, work, capsys):
    """F-2: RA/EP are counted in SOURCES from the lists of the record files; an id outside RA|EP-n gets no element and is NAMED."""
    scratch_tree(tree)
    arch, inbox = work
    ra, ep = "records/report-adaptations.json", "records/environment-properties.json"
    members = {ra: M(json.dumps({"schema_version": 1, "rows": [{"id": "RA-1", "kind": "x"}, {"id": "zzz-9", "kind": "y"}, {"kind": "no id"}]}), "D", ra),
               ep: M(json.dumps({"schema_version": 1, "properties": [{"id": "EP-4", "subject": {"a": 1}}]}), "D", ep)}
    code, out, _ = run(tree, inbox, build(arch, members), capsys=capsys)
    assert code == 0 and "raep=2 unreadable=0" in out and "ELEMENTS in=2 placed=2" in out and "MISMATCH" not in out
    warn = next(l for l in out.splitlines() if l.startswith("WARNING " + ra))
    assert "2 record(s) with an id outside the form RA-n / EP-n get no element (first: zzz-9, absent)" in warn
    broken = build(arch, {ra: M("{no", "D", ra)}, name=NAME.replace("abababab", "cdcdcdcd"), doc={"install_id": "cd" * 16})
    code, out, _ = run(tree, inbox, broken, capsys=capsys)
    assert code == 0 and "WARNING %s present, unreadable" % ra in out and "raep=0" in out


@pytest.mark.parametrize("spelling", ["native-sub", "posix-sub", "tree"])
def test_git_ceiling_directories_cannot_hide_a_git_tree_from_the_inbox_probe(tmp_path, monkeypatch, spelling):
    """F-3 / P5 (I2): the three spellings of a ceiling above the inbox. The control proves the variable DOES hide the tree from a plain git
    call; the probe, which clears it, still refuses; the environment is put back afterwards."""
    other = tmp_path / "other"
    deep = other / "sub" / "deep"
    deep.mkdir(parents=True)
    kit.git(other, "init", "-q")
    ceiling = {"native-sub": str(other / "sub"), "posix-sub": (other / "sub").as_posix(), "tree": str(other)}[spelling]
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", ceiling)
    monkeypatch.setenv("GIT_DISCOVERY_ACROSS_FILESYSTEM", "0")
    assert ci.gitcmd.git(deep, "rev-parse", "--is-inside-work-tree", stderr=True)[0] != 0                       # control: the ceiling works on a plain call
    assert "inside a git work tree" in ci.inbox_problem(deep / "inbox", tmp_path / "repo")
    assert os.environ["GIT_CEILING_DIRECTORIES"] == ceiling and os.environ["GIT_DISCOVERY_ACROSS_FILESYSTEM"] == "0"
    assert {"GIT_CEILING_DIRECTORIES", "GIT_DISCOVERY_ACROSS_FILESYSTEM"} <= set(ci.GIT_VARS)


def test_there_is_one_atomic_writer_and_it_is_the_piles_one():
    """F-4: the intake keeps no writer of its own (the copy used a fixed `<name>.tmp`); the index goes through `piles.write_bytes_atomic`."""
    assert not hasattr(ci, "write_bytes")
    source = (TOOLS / "collect_intake.py").read_text(encoding="utf-8")
    assert "piles.write_bytes_atomic(inbox / \"index.json\"" in source and ".tmp\"" not in source


def two_member_archive(arch, name=NAME):
    return build(arch, {"A/x": M("12345"), "A/y": M("12345")}, name=name)


def test_archive_max_bytes_is_the_door_of_the_archive_ceiling_at_and_beyond(tree, work, capsys):
    """F-5 Q1: 10 bytes of members: --archive-max-bytes 10 passes (AT), 9 refuses (BEYOND) and the text names the flag; a member over its OWN
    cap does not name it (no flag helps); a bad value is an argparse error (exit 2); the table is put back after every run."""
    scratch_tree(tree)
    arch, inbox = work
    path = two_member_archive(arch)
    prior = ci.limits()["archive_max_bytes"]
    code, out, _ = run(tree, inbox, path, capsys=capsys, extra=["--archive-max-bytes", "10"])
    assert code == 0 and "ARCHIVE abababab" in out and ci.limits()["archive_max_bytes"] == prior
    code, _out, err = run(tree, inbox, path, capsys=capsys, extra=["--archive-max-bytes", "9"])
    assert code == 1 and "together are larger than the archive ceiling" in err and "--archive-max-bytes N (now 9)" in err and "expected" in err
    assert ci.limits()["archive_max_bytes"] == prior
    ci.limits()["file_max_bytes"] = 4
    code, _out, err = run(tree, inbox, path, capsys=capsys, extra=["--archive-max-bytes", "100"])
    assert code == 1 and "is larger than the manifest declares" in err and "--archive-max-bytes" not in err
    for bad in ("0", "-5", "ten", "1.5"):
        with pytest.raises(SystemExit) as exc:
            run(tree, inbox, path, capsys=capsys, extra=["--archive-max-bytes", bad])
        assert exc.value.code == 2
        capsys.readouterr()


def test_an_unknown_part_kind_points_to_the_update_door_not_to_the_sender(work):
    """F-5 Q2: a well-formed part of a kind this intake does not know comes from a NEWER packer -> DOOR_UPDATE; a malformed part entry still
    goes back to the sender (control)."""
    arch, _ = work
    part = {"name": NAME[:-4] + "-part2.zip", "sha256": "0" * 64, "bytes": 1}
    with pytest.raises(ci.Refusal) as exc:
        ci.open_archive(build(arch, {}, rows=[], extra_parts=[{**part, "kind": "video"}]))
    text = str(exc.value)
    assert "of the kind video, which this intake does not read" in text and "expected kind absent or transcripts" in text and ci.DOOR_UPDATE in text and ci.DOOR_SENDER not in text
    with pytest.raises(ci.Refusal) as exc:
        ci.open_archive(build(arch, {}, rows=[], extra_parts=[{**part, "sha256": "zz"}], name=NAME.replace("abababab", "cdcdcdcd")))
    assert ci.DOOR_SENDER in str(exc.value) and ci.DOOR_UPDATE not in str(exc.value)


def test_the_finding_holds_inbox_relative_pointers_and_no_path_of_the_machine(tree, work, capsys):
    """F-10: the `Свидетель:` line and the key lines point `<project_id>/<sha24>/elements.json[#<pkey>]` relative to the inbox; the written
    file has no absolute path: no drive letter, no home directory, no part of the inbox's own path."""
    path, inbox, (code, out, _) = apply_fb(tree, work, capsys)
    assert code == 0
    text = (tree / "plans/piles/forge/findings" / forge_findings(tree)[0]).read_text(encoding="utf-8")
    pointer = "%s/%s/elements.json" % (PID, ci.open_archive(path).sha[:ci.FOLDER_HEX])
    assert "- abababab:FB:FB-1 | FB | new | %s#abababab:FB:FB-1" % pointer in text.split("\n")
    assert next(l for l in text.split("\n") if l.startswith("Свидетель: ")).startswith("Свидетель: " + pointer + " в inbox")
    for machine in (str(inbox), inbox.as_posix(), str(inbox.parent), inbox.parent.as_posix(), str(Path.home()), Path.home().as_posix()):
        assert machine not in text
    import re
    assert re.search(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]", text) is None and "/home/" not in text and "\\Users\\" not in text
    assert (inbox / PID / ci.open_archive(path).sha[:ci.FOLDER_HEX] / "elements.json").is_file()                   # and the pointer leads to a real file of the inbox


def test_the_s9_human_feedback_row_and_a_change_request_row_are_adaptations_and_nothing_else_is(work):
    """CL2-3 (t-1195): the S9 answer the analyst records (`idempotency:<T>:human-feedback`) is an `adaptation` like a `change-request:` row (AR-24/AR-27); the
    classifier reads ONLY the stored witness key (FR-12). Error direction: toward `adaptation` (visibility). Negative controls: no token, empty, `-human-feedback`,
    `change-requests:`, a token only in the essence."""
    arch, _ = work
    rows = [("FB-1", "e", "answered at S9; idempotency:TP1-12345:human-feedback"), ("FB-2", "e", "words in file; idempotency:change-request:TP1-12345"),
            ("FB-3", "e", "idempotency:change-request:TP1-12345; idempotency:TP1-12345:human-feedback"), ("FB-4", "e", "idempotency:launch-TP1-12345"), ("FB-5", "e", ""),
            ("FB-6", "e", "idempotency:TP1-12345-human-feedback"), ("FB-7", "e", "change-requests:TP1-12345"), ("FB-8", "asked about :human-feedback", "w")]
    want = {"FB-1": "adaptation", "FB-2": "adaptation", "FB-3": "adaptation", "FB-4": "FB", "FB-5": "FB", "FB-6": "FB", "FB-7": "FB", "FB-8": "FB"}
    els = ci.build_elements(ci.open_archive(fb_archive(arch, rows)), ci.EMPTY_INDEX)
    assert {e["id"]: e["kind"] for e in els} == want and len(els) == 8                 # FB-3 (both tokens) is ONE element
    table = "| id | essence | scope | witness/details | created | status | decision |\n|---|---|---|---|---|---|---|\n"
    d1 = "# backlog\n\n## Findings about the factory\n\n" + table + "| FB-1 | e | local-calibration | answered at S9; idempotency:TP1-12345:human-feedback | 2026-10-19 | open | — |\n"
    d1_els = ci.build_elements(ci.open_archive(build(arch, {"factory-backlog.md": M(d1, "D", "factory-backlog.md")}, name=NAME.replace("abababab", "cdcdcdcd"),
                                                    doc={"install_id": "cd" * 16})), ci.EMPTY_INDEX)
    assert [(e["id"], e["kind"]) for e in d1_els] == [("FB-1", "adaptation")]            # the marker survives the D1 reader (parse_findings)


def test_the_witness_classifier_is_a_substring_test_so_a_longer_token_and_a_declined_answer_are_still_adaptations(work):
    """CL2-3 edges: `:human-feedbacks` (the token inside a longer word) matches the substring -> `adaptation` (errs toward visibility; the Lead re-places with
    `--place`); a `declined` S9 answer row is read by no one's words (FR-12) and is still an element, an `adaptation`."""
    arch, _ = work
    rows = [("FB-1", "e", "idempotency:TP1-12345:human-feedbacks"), ("FB-2", "the person declined to answer", "idempotency:TP1-12345:human-feedback; declined")]
    els = ci.build_elements(ci.open_archive(fb_archive(arch, rows)), ci.EMPTY_INDEX)
    assert {e["id"]: e["kind"] for e in els} == {"FB-1": "adaptation", "FB-2": "adaptation"}
