"""Tests for tools/compact_snapshot.py (the PreCompact hook) and for the
`compact` branch of tools/session_context.py (the snapshot pointer line).
No network, no LLM; every test builds a tmp repo-shaped directory.

Run from the repo root: python -m pytest tools/test_compact_snapshot.py -q
"""

import datetime
import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import compact_snapshot as cs
import gitcmd
import session_context as sc

NOW = datetime.datetime(2026, 10, 2, 13, 31, 5)


def _git(args, cwd):
    return subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"] + args,
        cwd=str(cwd),
        check=True,
        capture_output=True,
    )


def _init_repo(root: Path):
    _git(["init", "-q"], root)
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(["add", "seed.txt"], root)
    _git(["commit", "-q", "-m", "seed commit"], root)


def _journal(root: Path, events):
    (root / "logs").mkdir(parents=True, exist_ok=True)
    with open(root / "logs" / "routing-log.jsonl", "w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")


def _ev(event, tid=None, ts="2026-10-02T10:00:00", **kw):
    e = {"ts": ts, "event": event, "agent": "builder", "category": "implementation", "notes": "n"}
    if tid:
        e["task_id"] = tid
    e.update(kw)
    return e


def _snap_text(root: Path, source="manual", now=NOW) -> str:
    text, _facts = cs.build_snapshot(root, source, now)
    return text


# ---- content ----------------------------------------------------------


def test_snapshot_has_all_six_sections_and_verbatim_reminder(tmp_path):
    _init_repo(tmp_path)
    _journal(tmp_path, [_ev("delegated", "t-001")])
    text = _snap_text(tmp_path)
    for heading in ("## 1. Header", "## 2. UNCOMMITTED", "## 3. OPEN DISPATCHES",
                    "## 4. Last 8 journal events", "## 5. Carriers to read after the compact",
                    "## 6. Reminder"):
        assert heading in text
    assert cs.REMINDER in text
    assert "seed commit" in text  # HEAD line
    assert "- branch:" in text and "- origin:" in text


def test_uncommitted_groups_package_forge_untracked(tmp_path):
    _init_repo(tmp_path)
    (tmp_path / "ai-packages" / "qa-factory").mkdir(parents=True)
    pkg = tmp_path / "ai-packages" / "qa-factory" / "a.py"
    pkg.write_text("1\n", encoding="utf-8")
    _git(["add", "."], tmp_path)
    _git(["commit", "-q", "-m", "pkg"], tmp_path)
    pkg.write_text("2\n", encoding="utf-8")  # package, tracked change
    (tmp_path / "seed.txt").write_text("changed\n", encoding="utf-8")  # Forge, tracked change
    (tmp_path / "new.txt").write_text("x\n", encoding="utf-8")  # untracked
    text, facts = cs.build_snapshot(tmp_path, "manual", NOW)
    assert facts["pkg"] == 1 and facts["forge"] == 1
    assert "### package (ai-packages/**), tracked changes: 1" in text
    assert "ai-packages/qa-factory/a.py" in text
    assert "### Forge (everything else), tracked changes: 1" in text
    assert "### untracked: 1" in text and "?? new.txt" in text


def test_file_list_cap_60_then_and_n_more(tmp_path):
    _init_repo(tmp_path)
    for i in range(65):
        (tmp_path / f"f{i:03d}.txt").write_text("x", encoding="utf-8")
    text = _snap_text(tmp_path)
    assert "### untracked: 65" in text
    assert text.count("?? f") == 60
    assert "and 5 more" in text


def test_exactly_60_entries_no_more_line(tmp_path):
    _init_repo(tmp_path)
    for i in range(60):
        (tmp_path / f"f{i:03d}.txt").write_text("x", encoding="utf-8")
    text = _snap_text(tmp_path)
    assert text.count("?? f") == 60
    assert "and 0 more" not in text and " more" not in text.split("## 3.")[0]


def test_open_dispatches_and_next_free_id(tmp_path):
    _init_repo(tmp_path)
    _journal(tmp_path, [
        _ev("delegated", "t-001", worker_ref="agent:aaa", model="m1"),
        _ev("accepted", "t-001", ts="2026-10-02T10:05:00"),
        _ev("delegated", "t-002", worker_ref="agent:bbb", model="m2", notes="x" * 300),
        _ev("delegated", "t-003", worker_ref="agent:ccc"),
        _ev("rejected", "t-003", ts="2026-10-02T10:06:00"),
        _ev("delegated", "t-310", worker_ref="agent:ddd", ts="2026-10-02T10:07:00"),
    ])
    text, facts = cs.build_snapshot(tmp_path, "manual", NOW)
    assert facts["open"] == 2 and facts["next"] == "t-311"
    assert "NEXT FREE ID: t-311" in text
    block = text.split("## 3. OPEN DISPATCHES")[1].split("## 4.")[0]
    assert "t-002 agent=builder model=m2" in block and "worker_ref=agent:bbb" in block
    assert "t-310" in block and "t-001" not in block and "t-003" not in block
    assert "x" * 121 not in block and "x" * 120 in block  # notes cut at 120


def test_journal_tail_is_last_eight_with_notes_cut_at_100(tmp_path):
    _init_repo(tmp_path)
    _journal(tmp_path, [_ev("calibrated", f"t-{i:03d}", notes="y" * 150) for i in range(1, 13)])
    block = _snap_text(tmp_path).split("## 4.")[1].split("## 5.")[0]
    rows = [l for l in block.splitlines() if l.startswith("- ")]
    assert len(rows) == 8
    assert "t-005" in rows[0] and "t-012" in rows[-1]
    assert "y" * 101 not in block and "y" * 100 in block


def test_journal_missing_is_stated_and_snapshot_still_built(tmp_path):
    _init_repo(tmp_path)
    text, facts = cs.build_snapshot(tmp_path, "manual", NOW)
    assert "journal missing" in text
    assert facts["open"] is None and facts["next"] is None


def test_journal_malformed_lines_skipped_and_counted(tmp_path):
    _init_repo(tmp_path)
    (tmp_path / "logs").mkdir()
    with open(tmp_path / "logs" / "routing-log.jsonl", "w", encoding="utf-8") as f:
        f.write(json.dumps(_ev("delegated", "t-007", worker_ref="w")) + "\n")
        f.write("{not json\n")
        f.write("[1, 2]\n")
    text, facts = cs.build_snapshot(tmp_path, "manual", NOW)
    assert "2 malformed journal line(s) skipped" in text
    assert facts["open"] == 1 and facts["next"] == "t-008"


def test_journal_unreadable_is_stated(tmp_path, monkeypatch):
    _init_repo(tmp_path)
    _journal(tmp_path, [_ev("delegated", "t-001")])
    real_open = open

    def _boom(path, *a, **k):
        if str(path).endswith("routing-log.jsonl"):
            raise PermissionError("denied")
        return real_open(path, *a, **k)

    monkeypatch.setattr("builtins.open", _boom)
    text, facts = cs.build_snapshot(tmp_path, "manual", NOW)
    monkeypatch.undo()
    assert "journal unreadable" in text and facts["open"] is None


def test_no_git_is_stated_and_snapshot_still_written(tmp_path, monkeypatch):
    monkeypatch.setattr(cs, "run_git", lambda args, root: (False, ""))
    _journal(tmp_path, [_ev("delegated", "t-001", worker_ref="w")])
    line = cs.run(tmp_path, "manual", NOW)
    files = list((tmp_path / cs.SNAPSHOT_DIR).glob("*.md"))
    assert len(files) == 1
    body = files[0].read_text(encoding="utf-8")
    assert "git: unavailable" in body and "git unavailable -- not collected" in body
    assert "uncommitted package ? / forge ?" in line and "open dispatches 1" in line


def test_carriers_section_lists_mtimes_and_counts(tmp_path):
    _init_repo(tmp_path)
    (tmp_path / "CURRENT_CONTEXT.md").write_text("# c\n", encoding="utf-8")
    (tmp_path / "docs" / "tasks" / "specs").mkdir(parents=True)
    (tmp_path / "docs" / "tasks" / "factory-fixes.md").write_text(
        "# x\n\n## State at 13:20 (02.10) -- morning\n\n## State at 06:55\n", encoding="utf-8")
    (tmp_path / "plans").mkdir()
    (tmp_path / "plans" / "BACKLOG.md").write_text(
        "| B-001 | a |\n| B-002 | b |\n| not a row |\n|---|---|\n", encoding="utf-8")
    for i in range(5):
        p = tmp_path / "docs" / "tasks" / "specs" / f"s{i}.md"
        p.write_text("s", encoding="utf-8")
        os.utime(p, (1_700_000_000 + i * 100, 1_700_000_000 + i * 100))
    (tmp_path / "experiments" / "e1").mkdir(parents=True)
    (tmp_path / "experiments" / "e1" / "r.md").write_text("r", encoding="utf-8")
    block = _snap_text(tmp_path).split("## 5.")[1].split("## 6.")[0]
    assert "- CURRENT_CONTEXT.md -- mtime 20" in block
    assert "line 3: State at 13:20 (02.10) -- morning" in block
    assert "2 rows" in block
    assert "docs/tasks/specs/s4.md" in block and "s2.md" in block and "s1.md" not in block
    assert "experiments/e1/r.md" in block


def test_carriers_missing_files_do_not_crash(tmp_path):
    _init_repo(tmp_path)
    block = _snap_text(tmp_path).split("## 5.")[1]
    assert "CURRENT_CONTEXT.md -- mtime missing" in block
    assert "no `## State at` heading found" in block or "unreadable" in block


# ---- the BACKLOG carrier after the freeze (t-598): archive rows + live findings ------------


def _frozen_tree(root: Path, piles: dict):
    """plans/BACKLOG.md with 2 archive rows and plans/piles/<slug>/findings/<name> = header line."""
    (root / "plans").mkdir(parents=True, exist_ok=True)
    (root / "plans" / "BACKLOG.md").write_text(
        "| B-001 | a |\n| B-002 | b |\n\n## Закрыто\n", encoding="utf-8")
    for slug, files in piles.items():
        d = root / "plans" / "piles" / slug / "findings"
        d.mkdir(parents=True)
        for name, header in files.items():
            (d / name).write_text(f"# t\n\n{header}\n\nbody\n", encoding="utf-8")


def _h(ident="—", frm="me, 08.10"):
    return f"id: {ident} | кучка: `x` | от: {frm} | приоритет: П2 | кандидат наверх: нет"


def test_backlog_rows_without_plans_piles_is_what_it_always_was(tmp_path):
    (tmp_path / "plans").mkdir()
    bl = tmp_path / "plans" / "BACKLOG.md"
    bl.write_text("| B-001 | a |\n| B-002 | b |\n| not a row |\n", encoding="utf-8")
    assert cs.backlog_rows(bl) == "2 rows (lines starting `| B-nnn`)"
    assert cs.backlog_rows(bl, tmp_path) == "2 rows (lines starting `| B-nnn`)"      # a root without plans/piles: same text


def test_backlog_rows_reports_the_archive_and_the_live_findings(tmp_path):
    _frozen_tree(tmp_path, {
        "alpha": {"20261008-a.md": _h(), "B-070-b.md": _h("B-070", "PLAN x, 05.10"), "B-071-c.md": _h("B-071", "PLAN y")},
        "beta": {"20261001-d.md": _h()},
        "empty": {},
    })
    text = cs.backlog_rows(tmp_path / "plans" / "BACKLOG.md", tmp_path)
    assert text.startswith("archive (frozen 08.10): 2 rows (lines starting `| B-nnn`); findings: ")
    assert "findings: 4 in 2 piles [alpha 3, beta 1]" in text          # the pile without findings is not counted
    assert "newest 2026-10-08" in text and "2 with id: —" in text


def test_finding_date_comes_from_the_file_name_else_from_the_header_and_a_bad_date_is_none(tmp_path):
    import piles
    _frozen_tree(tmp_path, {"p": {"20260930-n.md": _h(frm="x, 08.10"), "B-070-h.md": _h("B-070", "me, 05.10.2025"),
                                  "B-071-y.md": _h("B-071", "me, 05.10"), "B-072-bad.md": _h("B-072", "me, 31.02"),
                                  "B-073-none.md": _h("B-073", "PLAN 16.4Б; I-111")}})
    got = {f.name: f.date for f in piles.load_tree(tmp_path).piles["p"].findings}     # Finding.date: the one date reader (F2-8)
    assert got == {"20260930-n.md": datetime.date(2026, 9, 30), "B-070-h.md": datetime.date(2025, 10, 5),
                   "B-071-y.md": datetime.date(2026, 10, 5), "B-072-bad.md": None, "B-073-none.md": None}
    assert not hasattr(cs, "finding_date")                                           # compact_snapshot keeps no date reader of its own


def test_backlog_rows_counts_an_unreadable_finding_and_keeps_it_out_of_the_id_less(tmp_path):
    _frozen_tree(tmp_path, {"alpha": {"20261008-a.md": _h(), "B-070-b.md": _h("B-070")}})
    (tmp_path / "plans/piles/alpha/findings/20261009-bad.md").write_bytes(b"# t\n\n\xff\xfe\n")
    text = cs.backlog_rows(tmp_path / "plans" / "BACKLOG.md", tmp_path)
    assert "findings: 3 in 1 piles [alpha 3]" in text
    assert "1 with id: —" in text and text.endswith(", 1 unreadable, 0 leftovers without an executor"), text   # unknown id: not claimed to be "—"
    assert "newest 2026-10-09" in text                                               # the date of the unreadable file's NAME
    (tmp_path / "plans/piles/alpha/findings/20261009-bad.md").unlink()
    assert "unreadable" not in cs.backlog_rows(tmp_path / "plans" / "BACKLOG.md", tmp_path)       # ", N unreadable" only when N > 0


def test_the_findings_summary_opens_no_finding_file(tmp_path, monkeypatch):
    import piles
    _frozen_tree(tmp_path, {"alpha": {"20261008-a.md": _h(), "B-070-b.md": _h("B-070", "PLAN x, 05.10")}})
    loaded = piles.load_tree(tmp_path, tolerant=True)

    def no_reading(path):
        raise AssertionError("the summary reopened %s" % path)
    monkeypatch.setattr(piles, "load_tree", lambda *a, **k: loaded)
    monkeypatch.setattr(piles, "read_text", no_reading)
    text = cs.backlog_rows(tmp_path / "plans" / "BACKLOG.md", tmp_path)
    assert "findings: 2 in 1 piles [alpha 2]" in text and "newest 2026-10-08" in text


def test_backlog_rows_findings_part_fits_the_cap_beyond_it_names_the_rest(tmp_path):
    _frozen_tree(tmp_path, {f"pile-number-{i:02d}": {"20261008-a.md": _h()} for i in range(40)})
    text = cs.backlog_rows(tmp_path / "plans" / "BACKLOG.md", tmp_path)
    line = f"- plans/BACKLOG.md -- mtime 2026-10-08 23:59; {text}"
    assert len(line) <= 300 and "findings: 40 in 40 piles [" in text and " more]" in text
    last = cs.backlog_rows(tmp_path / "plans" / "BACKLOG.md", tmp_path)
    assert last == text                                                  # deterministic


def test_backlog_rows_counts_the_leftovers_without_an_executor_and_the_counter_survives_the_cap(tmp_path):
    """F6-30 K14 / E-D1-9: the snapshot's tail names the count (0 too); under a tight cap only the per-pile listing shrinks."""
    from piles_testkit import batch_text, node
    _frozen_tree(tmp_path, {f"pile-number-{i:02d}": {"20261008-a.md": _h()} for i in range(40)})
    assert cs.backlog_rows(tmp_path / "plans" / "BACKLOG.md", tmp_path).endswith(", 0 leftovers without an executor")
    (tmp_path / "plans/piles/pile-number-00/batch-1-x.md").write_text(
        batch_text("pile-number-00", 1, "ожидает", [node("F0-1")], pre="## Бриф\n", leftovers="- bare\n- ok | сделано: t-1\n- node | узел: F0-1"),
        encoding="utf-8")
    text = cs.backlog_rows(tmp_path / "plans" / "BACKLOG.md", tmp_path)
    assert text.endswith(", 1 leftovers without an executor") and " more]" in text, text
    assert len(f"- plans/BACKLOG.md -- mtime 2026-10-08 23:59; {text}") <= 300


def test_backlog_rows_an_unreadable_findings_tree_is_a_phrase_never_a_raise(tmp_path):
    (tmp_path / "plans" / "piles" / "p").mkdir(parents=True)
    bl = tmp_path / "plans" / "BACKLOG.md"
    bl.write_text("| B-001 | a |\n", encoding="utf-8")                 # no "## Закрыто": piles.load_tree refuses it
    assert cs.backlog_rows(bl, tmp_path).endswith("findings unreadable (CannotRun)")
    assert cs.backlog_rows(tmp_path / "gone.md", tmp_path) == \
        "archive (frozen 08.10): unreadable (FileNotFoundError); findings unreadable (CannotRun)"


# ---- file naming, retention, crash safety ---------------------------------


def test_two_runs_in_one_minute_give_distinct_files(tmp_path):
    _init_repo(tmp_path)
    p1 = cs.run(tmp_path, "manual", NOW)
    p2 = cs.run(tmp_path, "manual", NOW)
    names = sorted(p.name for p in (tmp_path / cs.SNAPSHOT_DIR).glob("*.md"))
    assert names == ["2026-10-02-1331-manual-2.md", "2026-10-02-1331-manual.md"]
    assert "2026-10-02-1331-manual.md" in p1 and "2026-10-02-1331-manual-2.md" in p2


def test_summary_line_format(tmp_path):
    _init_repo(tmp_path)
    _journal(tmp_path, [_ev("delegated", "t-317", worker_ref="w")])
    line = cs.run(tmp_path, "auto", NOW)
    assert line == (
        "COMPACT SNAPSHOT: docs/tasks/compact-snapshots/2026-10-02-1331-auto.md — "
        "open dispatches 1, uncommitted package 0 / forge 0, next free id t-318"
    )


def test_safe_source_sanitizes_filename_part():
    assert cs.safe_source("manual") == "manual"
    assert cs.safe_source("../../x y") == "xy"
    assert cs.safe_source("") == "unknown"
    assert cs.safe_source(None) == "unknown"
    assert len(cs.safe_source("a" * 99)) == 20


def _make_snapshots(folder: Path, n: int):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "README.md").write_text("r\n", encoding="utf-8")
    names = [f"2026-09-{1 + i // 24:02d}-{i % 24:02d}00-manual.md" for i in range(n)]
    for nm in names:
        (folder / nm).write_text("s\n", encoding="utf-8")
    return names


def test_prune_under_trigger_deletes_nothing(tmp_path):
    _init_repo(tmp_path)
    folder = tmp_path / cs.SNAPSHOT_DIR
    _make_snapshots(folder, 49)
    _git(["add", "."], tmp_path)
    _git(["commit", "-q", "-m", "snaps"], tmp_path)
    assert cs.prune(folder, tmp_path) == (0, 0)
    assert len(list(folder.glob("*.md"))) == 50  # 49 + README


def test_prune_at_trigger_deletes_only_committed_oldest_beyond_30(tmp_path):
    _init_repo(tmp_path)
    folder = tmp_path / cs.SNAPSHOT_DIR
    names = _make_snapshots(folder, 50)
    _git(["add", "."], tmp_path)
    _git(["commit", "-q", "-m", "snaps"], tmp_path)
    deleted, kept = cs.prune(folder, tmp_path)
    assert (deleted, kept) == (20, 0)
    left = sorted(p.name for p in folder.glob("*.md") if p.name != "README.md")
    assert left == names[20:]  # the newest 30 stay


def test_prune_never_deletes_uncommitted_and_counts_them(tmp_path):
    _init_repo(tmp_path)
    folder = tmp_path / cs.SNAPSHOT_DIR
    names = _make_snapshots(folder, 60)
    # commit only the 5 oldest; 55 stay untracked
    _git(["add"] + [str((folder / n).relative_to(tmp_path)) for n in names[:5]], tmp_path)
    _git(["commit", "-q", "-m", "five"], tmp_path)
    (folder / names[1]).write_text("modified after commit\n", encoding="utf-8")  # tracked but dirty
    deleted, kept = cs.prune(folder, tmp_path)
    assert deleted == 4 and kept == 26  # 30 candidates: 4 clean-committed, 1 dirty + 25 untracked kept
    assert (folder / names[1]).exists()
    assert not (folder / names[0]).exists()


def test_prune_without_git_deletes_nothing(tmp_path, monkeypatch):
    folder = tmp_path / cs.SNAPSHOT_DIR
    _make_snapshots(folder, 55)
    monkeypatch.setattr(cs, "run_git", lambda args, root: (False, ""))
    deleted, kept = cs.prune(folder, tmp_path)
    assert deleted == 0 and kept == 25
    assert len(list(folder.glob("*.md"))) == 56


def test_run_prints_kept_count_line(tmp_path):
    _init_repo(tmp_path)
    _make_snapshots(tmp_path / cs.SNAPSHOT_DIR, 55)  # all untracked
    out = cs.run(tmp_path, "manual", NOW)
    assert "25 old snapshot(s)" in out or "26 old snapshot(s)" in out
    assert "NOT deleted" in out


def test_main_exits_zero_and_prints_error_on_crash(tmp_path, monkeypatch, capsys):
    def _boom(*a, **k):
        raise RuntimeError("kaput")

    monkeypatch.setattr(cs, "build_snapshot", _boom)
    assert cs.main(["--source", "manual", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "COMPACT SNAPSHOT: failed (RuntimeError: kaput)" in out


def test_main_exits_zero_when_folder_cannot_be_created(tmp_path, monkeypatch, capsys):
    (tmp_path / "docs").write_text("a file where a folder should be", encoding="utf-8")
    assert cs.main(["--source", "manual", "--root", str(tmp_path)]) == 0
    assert "COMPACT SNAPSHOT: failed" in capsys.readouterr().out


def test_main_survives_bad_arguments(tmp_path, capsys):
    assert cs.main(["--nonsense", "--source"]) == 0  # argparse error must not escape


def test_main_writes_file_and_prints_summary(tmp_path, capsys):
    _init_repo(tmp_path)
    assert cs.main(["--source", "manual", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert out.startswith("COMPACT SNAPSHOT: docs/tasks/compact-snapshots/")
    assert len(list((tmp_path / cs.SNAPSHOT_DIR).glob("*-manual*.md"))) == 1


def test_source_falls_back_to_stdin_trigger(tmp_path, monkeypatch, capsys):
    _init_repo(tmp_path)

    class _Stdin:
        def isatty(self):
            return False

        def read(self):
            return json.dumps({"trigger": "auto", "custom_instructions": ""})

    monkeypatch.setattr(sys, "stdin", _Stdin())
    assert cs.main(["--root", str(tmp_path)]) == 0
    assert len(list((tmp_path / cs.SNAPSHOT_DIR).glob("*-auto*.md"))) == 1


def test_emit_default_is_utf8_and_never_raises(monkeypatch):
    monkeypatch.delenv("PYTHONIOENCODING", raising=False)
    raw = io.BytesIO()
    monkeypatch.setattr(sys, "stdout", io.TextIOWrapper(raw, encoding="cp437", errors="strict"))
    cs.emit("COMPACT SNAPSHOT: x — привет")  # em dash + Cyrillic
    sys.stdout.flush()
    got = raw.getvalue().replace(b"\r\n", b"\n")  # Windows newline translation
    assert got == "COMPACT SNAPSHOT: x — привет\n".encode("utf-8")


def test_emit_with_explicit_encoding_replaces_unencodable(monkeypatch):
    monkeypatch.setenv("PYTHONIOENCODING", "cp437")
    raw = io.BytesIO()
    monkeypatch.setattr(sys, "stdout", io.TextIOWrapper(raw, encoding="cp437", errors="strict"))
    cs.emit("COMPACT SNAPSHOT: x — привет")
    sys.stdout.flush()
    assert raw.getvalue().startswith(b"COMPACT SNAPSHOT: x ")  # no UnicodeEncodeError


def test_snapshot_file_is_utf8_and_survives_non_ascii_notes(tmp_path):
    _init_repo(tmp_path)
    _journal(tmp_path, [_ev("delegated", "t-001", worker_ref="w", notes="привет — ok")])
    cs.run(tmp_path, "manual", NOW)
    f = next((tmp_path / cs.SNAPSHOT_DIR).glob("*.md"))
    assert "привет" in f.read_text(encoding="utf-8")


# ---- t-323 B5: time (critic t-322 C-F1..C-F3) -------------------------------


class _Done:
    """What subprocess.run gives back, for a fake git."""

    def __init__(self, out=b"", code=0):
        self.stdout, self.stderr, self.returncode = out, b"", code


def test_git_facts_share_one_total_deadline(tmp_path, monkeypatch):
    """Not 15 s per call (seven calls): each call gets what is left of the one deadline, and the calls stop when it is
    gone. The fake git takes 0.2 s per call; the deadline is 0.7 s (the sixth and last call would start at 1.0 s)."""
    asked = []

    def fake_run(argv, **kw):
        asked.append((argv[-1], kw["timeout"]))
        time.sleep(0.2)
        return _Done(b"true\n" if "--is-inside-work-tree" in argv else b"x\n")

    monkeypatch.setattr(gitcmd.subprocess, "run", fake_run)      # the one git runner makes the call now
    started = time.monotonic()
    info = cs.collect_git(tmp_path, total_s=0.7)
    elapsed = time.monotonic() - started
    timeouts = [t for _a, t in asked]
    assert all(t <= 0.71 for t in timeouts), timeouts  # none gets the old 15 s (the clock reads a hair after `end` was set)
    assert timeouts == sorted(timeouts, reverse=True) and timeouts[0] > timeouts[-1]  # what is left shrinks
    assert elapsed < 5.0  # nowhere near seven calls of the old 15 s; a loose bound, so a busy machine does not fail it
    assert "UNCOMMITTED" in info["missed"], info["missed"]  # the last fact never got its call


def test_a_passed_deadline_is_said_in_the_snapshot_and_never_breaks_the_hook(tmp_path, monkeypatch, capsys):
    _init_repo(tmp_path)
    _journal(tmp_path, [_ev("delegated", "t-001", worker_ref="w")])
    monkeypatch.setattr(cs, "GIT_TOTAL_DEADLINE", 0.25)
    calls = []

    def slow_git(args, root):
        calls.append(args[0])
        time.sleep(0.12)
        return True, "true\n" if "--is-inside-work-tree" in args else "abc\n"

    monkeypatch.setattr(cs, "run_git", slow_git)
    assert cs.main(["--source", "manual", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1 and out[0].startswith("COMPACT SNAPSHOT: docs/tasks/compact-snapshots/"), out  # the summary only
    assert "uncommitted package ? / forge ?" in out[0]  # an uncollected status is "?", never 0
    body = next((tmp_path / cs.SNAPSHOT_DIR).glob("*.md")).read_text(encoding="utf-8")
    assert "not collected, the 0.25 s git deadline passed: " in body and "UNCOMMITTED" in body
    assert "UNCOMMITTED unknown" in body
    assert len(calls) < 6, calls  # the later calls were not made
    # control: with time enough nothing is said to be missing
    monkeypatch.setattr(cs, "GIT_TOTAL_DEADLINE", 10)
    monkeypatch.setattr(cs, "run_git", lambda args, root: (True, "true\n" if "--is-inside-work-tree" in args else ""))
    assert cs.main(["--source", "auto", "--root", str(tmp_path)]) == 0
    capsys.readouterr()
    again = next((tmp_path / cs.SNAPSHOT_DIR).glob("*-auto*.md")).read_text(encoding="utf-8")
    assert "git deadline passed" not in again


def test_the_summary_is_printed_before_retention_starts(tmp_path, monkeypatch, capsys):
    _init_repo(tmp_path)
    seen = []

    def prune_spy(folder, root):
        seen.append(capsys.readouterr().out)  # what the hook had printed when retention began
        return 0, 0

    monkeypatch.setattr(cs, "prune", prune_spy)
    assert cs.main(["--source", "manual", "--root", str(tmp_path)]) == 0
    assert seen and seen[0].startswith("COMPACT SNAPSHOT: docs/tasks/compact-snapshots/"), seen
    assert len(list((tmp_path / cs.SNAPSHOT_DIR).glob("*-manual*.md"))) == 1


def test_exit_is_zero_and_quiet_after_a_stdin_deadline(tmp_path):
    """A stdin nobody closes: the hook waits its 2 s, writes the snapshot and leaves with exit 0 and ONE line on
    stdout - through os._exit, like session_context (a reader thread still inside a read must not decide the exit)."""
    _init_repo(tmp_path)
    proc = subprocess.Popen([sys.executable, "-B", str(Path(cs.__file__)), "--root", str(tmp_path)],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        code = proc.wait(timeout=60)  # stdin stays open: only the deadline lets it go
        out = proc.stdout.read().decode("utf-8", "replace")
        err = proc.stderr.read().decode("utf-8", "replace")
    finally:
        proc.stdin.close()
        proc.stdout.close()
        proc.stderr.close()
        if proc.poll() is None:
            proc.kill()
    assert code == 0, (code, err[-300:])
    assert len(out.splitlines()) == 1 and out.startswith("COMPACT SNAPSHOT:"), out
    assert len(list((tmp_path / cs.SNAPSHOT_DIR).glob("*-unknown*.md"))) == 1
    source = Path(cs.__file__).read_text(encoding="utf-8")
    tail = source.split('if __name__ == "__main__":')[1]
    assert 'if _STDIN_STATE["hit"]:' in tail and "os._exit(_rc)" in tail and "sys.exit(_rc)" in tail


def test_the_fallback_open_list_says_so(tmp_path, monkeypatch):
    _init_repo(tmp_path)
    _journal(tmp_path, [_ev("delegated", "t-001", worker_ref="w")])
    block = _snap_text(tmp_path).split("## 3. OPEN DISPATCHES")[1].split("## 4.")[0]
    assert "plain fallback rule" not in block  # control: the SessionStart hook's own function was importable
    monkeypatch.setitem(sys.modules, "session_context", None)  # `import session_context` now fails
    text, facts = cs.build_snapshot(tmp_path, "manual", NOW)
    block = text.split("## 3. OPEN DISPATCHES")[1].split("## 4.")[0]
    assert "session_context could not be imported" in block and "plain fallback rule" in block
    assert "`closes:t-NNN` marker is NOT honoured" in block
    assert facts["open"] == 1 and "- t-001" in block  # the list itself is still given


# ---- session_context: the pointer line on source `compact` ---------------


class _FakeStdin:
    def __init__(self, text, tty=False):
        self._text, self._tty = text, tty

    def isatty(self):
        return self._tty

    def read(self):
        return self._text


def test_compact_snapshot_line_none_when_folder_absent_or_only_readme(tmp_path):
    assert sc.compact_snapshot_line(tmp_path) == "COMPACT SNAPSHOT: none"
    folder = tmp_path / cs.SNAPSHOT_DIR
    folder.mkdir(parents=True)
    (folder / "README.md").write_text("r", encoding="utf-8")
    assert sc.compact_snapshot_line(tmp_path) == "COMPACT SNAPSHOT: none"


def test_compact_snapshot_line_names_newest_and_age(tmp_path):
    folder = tmp_path / cs.SNAPSHOT_DIR
    folder.mkdir(parents=True)
    old, new = folder / "2026-10-02-1000-manual.md", folder / "2026-10-02-1300-auto.md"
    old.write_text("o", encoding="utf-8")
    new.write_text("n", encoding="utf-8")
    base = datetime.datetime(2026, 10, 2, 13, 0, 0).timestamp()
    os.utime(old, (base - 10800, base - 10800))
    os.utime(new, (base, base))
    now = datetime.datetime.fromtimestamp(base + 7 * 60 + 30)
    assert sc.compact_snapshot_line(tmp_path, now) == (
        "COMPACT SNAPSHOT: docs/tasks/compact-snapshots/2026-10-02-1300-auto.md (7 min old)"
    )


def test_compact_snapshot_line_never_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(sc.Path, "is_dir", lambda self: (_ for _ in ()).throw(OSError("boom")))
    assert sc.compact_snapshot_line(tmp_path).startswith("COMPACT SNAPSHOT: unavailable")


def test_main_on_compact_source_prints_snapshot_line(tmp_path, capsys, monkeypatch):
    (tmp_path / "logs").mkdir()
    folder = tmp_path / cs.SNAPSHOT_DIR
    folder.mkdir(parents=True)
    (folder / "2026-10-02-1331-manual.md").write_text("s", encoding="utf-8")
    monkeypatch.setattr(sys, "stdin", _FakeStdin(json.dumps({"source": "compact"})))
    assert sc.main(tmp_path) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[-1].startswith("COMPACT SNAPSHOT: docs/tasks/compact-snapshots/2026-10-02-1331-manual.md (")
    assert out[-1].endswith(" min old)")


def test_main_on_compact_source_with_no_snapshot_says_none(tmp_path, capsys, monkeypatch):
    (tmp_path / "logs").mkdir()
    monkeypatch.setattr(sys, "stdin", _FakeStdin(json.dumps({"source": "compact"})))
    assert sc.main(tmp_path) == 0
    assert capsys.readouterr().out.splitlines()[-1] == "COMPACT SNAPSHOT: none"


def test_main_on_other_sources_prints_no_snapshot_line(tmp_path, capsys, monkeypatch):
    (tmp_path / "logs").mkdir()
    for payload in ({"source": "startup"}, {"source": "resume"}, {}):
        monkeypatch.setattr(sys, "stdin", _FakeStdin(json.dumps(payload)))
        assert sc.main(tmp_path) == 0
        assert "COMPACT SNAPSHOT" not in capsys.readouterr().out


# ---- K13 (t-581, F0-4): the next free id and the open tasks of the writer's logical journal ----

from test_journal_per_developer import (DEV1, DEV2, M_CREATED, N_CREATED, accepted as _acc13,
                                        delegated as _dl13, ev as _ev13, jtext as _jt13, make_root as _root13)

_HIST13 = [_dl13("t-001", "2026-10-01T09:00:00"), _acc13("t-001", "2026-10-01T09:30:00"), _dl13("t-002", "2026-10-01T10:00:00")]


def _k13(tmp_path, slug, dev2_extra=(), dev1_extra=()):
    root = _root13(tmp_path, history=_jt13(*_HIST13), slug=slug, files={
        DEV1: _jt13(M_CREATED, _dl13("t-003", "2026-10-02T08:30:00"), *dev1_extra),
        DEV2: _jt13(N_CREATED, _dl13("t-001", "2026-10-02T09:00:00"), _dl13("t-002", "2026-10-02T09:10:00"), *dev2_extra)})
    return cs.build_snapshot(root, "manual", NOW)


def test_k13_the_owner_next_id_is_the_max_of_the_history_and_her_file_plus_one(tmp_path):
    text, facts = _k13(tmp_path, "dev1")
    assert "NEXT FREE ID (logs/journal/dev1.jsonl): t-004" in text and facts["next"] == "t-004"


def test_k13_another_writers_next_id_is_by_her_own_file(tmp_path):
    text, facts = _k13(tmp_path, "dev2")
    assert "NEXT FREE ID (logs/journal/dev2.jsonl): t-003" in text and facts["next"] == "t-003"


def test_k13_without_a_slug_the_next_id_is_unknown_not_a_guess(tmp_path):
    root = _root13(tmp_path, history=_jt13(*_HIST13), files={DEV1: _jt13(M_CREATED), DEV2: _jt13(N_CREATED)})
    text, facts = cs.build_snapshot(root, "manual", NOW)
    assert "NEXT FREE ID: unknown -- no developer slug" in text and facts["next"] == "unknown -- no developer slug"
    assert "t-00" not in text.split("NEXT FREE ID:")[1].splitlines()[0]


def test_k13_before_the_switch_the_label_is_the_old_one(tmp_path):
    root = _root13(tmp_path, history=_jt13(*_HIST13))
    text, facts = cs.build_snapshot(root, "manual", NOW)
    assert "NEXT FREE ID: t-003" in text and "NEXT FREE ID (" not in text and facts["next"] == "t-003"


def test_k13_open_tasks_are_shown_by_their_key_and_a_labelled_close_removes_the_other_writers(tmp_path):
    text, facts = _k13(tmp_path, "dev1")
    opens = [l for l in text.splitlines() if l.startswith("- t-")]
    assert [l.split(" agent=")[0] for l in opens] == ["- t-002", "- t-003", "- t-001@dev2", "- t-002@dev2"]
    assert facts["open"] == 4
    carrier = _ev13("dispatch_skipped", "2026-10-02T10:00:00", agent="scout", notes="closes:t-001@dev2")
    text, facts = _k13(tmp_path / "c", "dev1", dev1_extra=[carrier])
    opens = [l.split(" agent=")[0] for l in text.splitlines() if l.startswith("- t-")]
    assert opens == ["- t-002", "- t-003", "- t-002@dev2"] and facts["open"] == 3


def test_k13_the_last_events_are_the_writers_own_logical_journal(tmp_path):
    text, _ = _k13(tmp_path, "dev1", dev2_extra=[_dl13("t-003", "2026-10-02T12:00:00", notes="DEV2-LATE")])
    tail = text.split("journal events", 1)[1]
    assert "t-003" in tail and "DEV2-LATE" not in tail
    dev2, _ = _k13(tmp_path / "n", "dev2", dev2_extra=[_dl13("t-003", "2026-10-02T12:00:00", notes="DEV2-LATE")])
    assert "DEV2-LATE" in dev2.split("journal events", 1)[1]
