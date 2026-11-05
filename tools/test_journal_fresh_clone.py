"""The readers of the journal on a tree that has NO journal (github-move node GM2-4, spec t-1855 4.3).

The new repository starts without `logs/` (FK-14: the history stays in the old repository's bundle). Every reader of the journal
must meet that tree without a traceback and without calling the empty tree a green count. This is a property of the forge for
good, not a one-shot test of the move: it stays.

J1 load_all: empty, no problems;  J2 current_path: no history to write to -- a door while no developer is named, the developer's
own file once `tools/dev.config.yaml` names one (never `logs/routing-log.jsonl`);  J3 a seeded first line is a legal one;
J4 a first line that is not `journal_created` is a violation (negative control);  J5 calibration_counts: exit 2 and
"no journal under";  J6 session_context: no exception, the first line starts with `NOW:`, no `JOURNAL FILES:` line;
J7 a temporary git repository of two commits without a journal: the validator's CI mode exits 0, forge_metrics names no journal
offender;  J8 journal_keys check without a declaration: 0;  J9 compact_snapshot builds and states "journal missing";
J10 main_gate resolves the journal path (None, then the developer's own file) and its empty-journal warning stays off.
"""
from __future__ import annotations

import datetime
import json
import os
import subprocess
from pathlib import Path

import pytest

import calibration_counts as cc
import compact_snapshot as cs
import forge_metrics as fm
import journal_keys as jk
import journal_validator as jv
import main_gate as mg
import session_context as sc

CREATED = {"ts": "2026-11-05T09:00:00", "event": "journal_created", "agent": "lead", "category": "process",
           "notes": "the journal of this clone"}
_LOCATION_VARS = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_PREFIX", "QA_DEV_CONFIG")


def seed_config(root: Path, slug: str = "dev1") -> None:
    p = root / jk.DEV_CONFIG_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"developer: {slug}\n", encoding="utf-8")


def clean_env() -> dict:
    return {k: v for k, v in os.environ.items() if k not in _LOCATION_VARS and not k.startswith("GITHEAD_")}


def git(root: Path, *args: str) -> None:
    proc = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false",
                           *args], cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace", env=clean_env())
    assert proc.returncode == 0, (args, proc.stdout, proc.stderr)


@pytest.fixture(autouse=True)
def _no_dev_config_variable(monkeypatch):
    monkeypatch.delenv("QA_DEV_CONFIG", raising=False)


def test_j1_load_all_of_a_tree_without_a_journal_is_empty_and_clean(tmp_path):
    j = jk.load_all(tmp_path)
    assert j.rows == [] and j.files == [] and j.problems == []


def test_j2_current_path_names_a_door_then_the_developers_own_file_never_the_history(tmp_path):
    rel, why = jk.current_path(tmp_path)
    assert rel is None and why                                                       # no developer named: a door, not a file (never the history)
    seed_config(tmp_path)
    rel, why = jk.current_path(tmp_path)
    assert rel == "logs/journal/dev1.jsonl" and "journal_created" in why             # the file does not exist yet: its first line says where it comes from


def test_j3_a_seeded_first_line_is_legal(tmp_path):
    seed_config(tmp_path)
    p = tmp_path / "logs" / "journal" / "dev1.jsonl"
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps(CREATED) + "\n", encoding="utf-8")
    assert jk.current_path(tmp_path) == ("logs/journal/dev1.jsonl", None)
    assert jv.developer_file_violations("logs/journal/dev1.jsonl", [json.dumps(CREATED)]) == []
    j = jk.load_all(tmp_path)
    assert len(j.rows) == 1 and j.problems == []


def test_j4_a_first_line_that_is_not_journal_created_is_a_violation(tmp_path):
    bad = dict(CREATED, event="delegated")
    out = jv.developer_file_violations("logs/journal/dev1.jsonl", [json.dumps(bad)])
    assert out and "journal_created" in out[0]                                       # the positive control of J3 is the same call, green


def test_j5_calibration_counts_without_a_journal_exits_2_and_says_so(tmp_path, capsys):
    assert cc.main(["--root", str(tmp_path)]) == 2
    out = capsys.readouterr()
    assert "no journal under" in out.out + out.err


def test_j6_session_context_builds_without_a_journal(tmp_path):
    lines = sc.build_context_lines(root=tmp_path)
    assert lines and lines[0].startswith("NOW:")
    assert not [l for l in lines if l.startswith("JOURNAL FILES:")]


def test_j7_a_two_commit_repository_without_a_journal_passes_the_ci_readers(tmp_path, monkeypatch, capsys):
    git(tmp_path, "init", "-q")
    for n in (1, 2):
        (tmp_path / f"f{n}.txt").write_text(f"{n}\n", encoding="utf-8")
        git(tmp_path, "add", "-A")
        git(tmp_path, "commit", "-q", "-m", f"c{n}")
    monkeypatch.chdir(tmp_path)
    assert jv._run_all("HEAD~1") == 0
    capsys.readouterr()
    offenders, _counts, _sha, _warnings = fm.run_check(tmp_path, "HEAD~1", features=[])
    assert not [o for o in offenders if "journal" in " ".join(map(str, o)).lower()]


def test_j8_check_without_a_declaration_is_ok(tmp_path, capsys):
    assert jk.cmd_check(tmp_path / "logs" / "journal" / "x.jsonl", tmp_path / "logs" / "journal-segments.json") == 0
    assert "no declaration" in capsys.readouterr().out


def test_j9_compact_snapshot_builds_on_a_tree_without_a_journal_and_says_so(tmp_path):
    git(tmp_path, "init", "-q")
    (tmp_path / "seed.txt").write_text("seed\n", encoding="utf-8")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "seed")
    text, facts = cs.build_snapshot(tmp_path, "manual", datetime.datetime(2026, 11, 5, 9, 0, 0))
    assert "journal missing" in text                                                 # the loader found no journal file: the snapshot states it
    assert facts["open"] is None and facts["next"] is None
    seed_config(tmp_path)                                                            # a named developer changes nothing about the statement
    text, _facts = cs.build_snapshot(tmp_path, "manual", datetime.datetime(2026, 11, 5, 9, 0, 0))
    assert "journal missing" in text


def test_j10_main_gate_resolves_the_journal_path_of_a_tree_without_a_journal(tmp_path):
    assert mg._journal_file(str(tmp_path)) is None                                   # no developer named: check (b) stays silent
    seed_config(tmp_path)
    path = mg._journal_file(str(tmp_path))
    assert path == tmp_path / "logs" / "journal" / "dev1.jsonl" and not path.exists()   # the developer's own file, not the history
    assert mg._journal_empty_warning_applies(str(tmp_path), {}) is False             # a missing file is not an empty journal
