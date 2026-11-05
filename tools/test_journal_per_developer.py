"""Tests of the per-developer journal (t-581 / t-585, node F0-4): integration on a temporary git
repository. The validator runs as the pre-commit hook would (the CLI, cwd = the repo, the index staged),
and as CI would (`--all --base <ref>`).

K1 two developer files merge (union); K3 the history is frozen after the switch; K6 the NEGATIVE control (a
broken second file is refused BY NAME, in pre-commit and in --all); K9 --all (ts drift off, deleted file,
not a prefix, the argument errors, a base ahead of HEAD); K10 one writer per file; the line-1 rules and the
two-successor refusal through git; K11 the echo matcher, root and CRLF; K15 main_gate / claim_control_gate /
critic_snapshot / r3_integration_check; K16 the pins (hygiene_gate, warn_density, the probe, mechanism_gate).
The pure halves of K2, K4, K7, K17 are in test_journal_keys.py, K8 in test_journal_validator.py, K5 in
test_session_context.py, K12 in test_forge_metrics.py, K13 in test_compact_snapshot.py, K14 in
test_calibration_counts.py; they import the fixture builders of this module.

Run from the repo root: python -m pytest tools/test_journal_per_developer.py
"""
from __future__ import annotations

import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import journal_keys as jk

TOOLS = Path(__file__).resolve().parent
REPO_ROOT = TOOLS.parent
VALIDATOR = TOOLS / "journal_validator.py"

HISTORY = "logs/routing-log.jsonl"
DEV1 = "logs/journal/dev1.jsonl"
DEV2 = "logs/journal/dev2.jsonl"

try:
    subprocess.run(["git", "--version"], capture_output=True, check=True)
    _HAS_GIT = True
except (OSError, subprocess.CalledProcessError):
    _HAS_GIT = False
needs_git = pytest.mark.skipif(not _HAS_GIT, reason="git is not available")

_GIT_ENV_KEYS = ("GIT_DIR", "GIT_INDEX_FILE", "GIT_WORK_TREE", "GIT_PREFIX", "GIT_OBJECT_DIRECTORY",
                 "GIT_COMMON_DIR", "QA_DEV_CONFIG")


def clean_env(**extra) -> dict:
    """The environment of a child process: no GIT_* location variables (a hook of an outer commit
    exports them and a child would work on the OUTER repository), no GITHEAD_*, no QA_DEV_CONFIG."""
    env = {k: v for k, v in os.environ.items() if k not in _GIT_ENV_KEYS and not k.startswith("GITHEAD_")}
    env.update(extra)
    return env


# ---- the lines ----------------------------------------------------------------------------------

def ev(event: str, ts: str, task_id=None, agent="builder", **kw) -> dict:
    d = {"ts": ts, "event": event, "agent": agent, "category": "implementation", "notes": "n"}
    if task_id is not None:
        d["task_id"] = task_id
    d.update(kw)
    return d


def delegated(tid: str, ts: str, **kw) -> dict:
    return ev("delegated", ts, tid, model="sonnet", worker_ref=f"agent:{tid}-{ts[-8:]}", **kw)


def accepted(tid: str, ts: str, **kw) -> dict:
    return ev("accepted", ts, tid, **{"model": "sonnet", "by": "opus", "witness": "pytest: 1 passed", **kw})


def created(ts: str, continues=None, **kw) -> dict:
    d = ev("journal_created", ts, agent="lead", category="process", notes="the journal of this clone")
    if continues:
        d["continues"] = continues
    d.update(kw)
    return d


def jtext(*objs) -> str:
    return "".join((o if isinstance(o, str) else json.dumps(o)) + "\n" for o in objs)


# the history: t-001 closed, t-002 open (the owner's open task at the switch, E-14)
H1 = delegated("t-001", "2026-10-01T09:00:00")
H2 = accepted("t-001", "2026-10-01T09:30:00")
H3 = delegated("t-002", "2026-10-01T10:00:00")
HISTORY_TEXT = jtext(H1, H2, H3)
# the owner's file, the successor of the history
M_CREATED = created("2026-10-02T08:00:00", continues=HISTORY)
# the second developer's file, her own namespace from t-001
N_CREATED = created("2026-10-02T08:10:00")
N1 = delegated("t-001", "2026-10-02T09:00:00")


def write(root: Path, rel: str, text: str) -> None:
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:      # exact bytes: no newline translation
        f.write(text)


def make_root(tmp_path: Path, *, history=HISTORY_TEXT, files=None, slug=None, config=None) -> Path:
    """A plain directory shaped like a clone: the history, the developer files (`files`: rel -> text)
    and tools/dev.config.yaml (`slug`, or `config` = the raw text). No git."""
    root = Path(tmp_path)
    if history is not None:
        write(root, HISTORY, history)
    for rel, text in (files or {}).items():
        write(root, rel, text)
    if config is not None:
        write(root, jk.DEV_CONFIG_REL, config)
    elif slug is not None:
        write(root, jk.DEV_CONFIG_REL, f"developer: {slug}\n")
    return root


# ---- git ----------------------------------------------------------------------------------------

def git(root: Path, *args: str, check=True) -> subprocess.CompletedProcess:
    proc = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                           "-c", "core.autocrlf=false", *args], cwd=root, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=clean_env())
    if check:
        assert proc.returncode == 0, (args, proc.stdout, proc.stderr)
    return proc


def commit_all(root: Path, message: str, *paths: str) -> str:
    git(root, "add", "--", *(paths or (".",)))
    git(root, "commit", "-q", "-m", message)
    return git(root, "rev-parse", "HEAD").stdout.strip()


def init_repo(root: Path, *, slug="dev1") -> Path:
    """A git repo whose first commit holds the history and .gitattributes (the union merge of the
    journal files, as in the real repository); tools/dev.config.yaml is written but NEVER committed
    (it is untracked in the real repository too)."""
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q", "-b", "main")
    write(root, ".gitattributes", "logs/journal/*.jsonl merge=union text eol=lf\n")
    write(root, HISTORY, HISTORY_TEXT)
    if slug:
        write(root, jk.DEV_CONFIG_REL, f"developer: {slug}\n")
    commit_all(root, "history", ".gitattributes", HISTORY)
    return root


def switched_repo(root: Path, *, slug="dev1", with_dev2=True) -> Path:
    """init_repo, then the switch commit: the owner's file (continues the history, one delegated of its
    own) and, when asked, the second developer's file."""
    init_repo(root, slug=slug)
    write(root, DEV1, jtext(M_CREATED, delegated("t-003", "2026-10-02T08:30:00")))
    paths = [DEV1]
    if with_dev2:
        write(root, DEV2, jtext(N_CREATED, N1))
        paths.append(DEV2)
    commit_all(root, "switch", *paths)
    return root


def set_slug(root: Path, slug) -> None:
    p = Path(root) / jk.DEV_CONFIG_REL
    if slug is None:
        p.unlink()
    else:
        write(root, jk.DEV_CONFIG_REL, f"developer: {slug}\n")


def append(root: Path, rel: str, *objs) -> None:
    p = Path(root) / rel
    with open(p, "a", encoding="utf-8", newline="") as f:
        f.write(jtext(*objs))


def validate(root: Path, *args: str) -> subprocess.CompletedProcess:
    """journal_validator.py as a hook runs it: its own process, cwd = the repository."""
    return subprocess.run([sys.executable, str(VALIDATOR), *args], cwd=root, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=clean_env())


def stage(root: Path, *paths: str) -> None:
    git(root, "add", "--", *paths)


# ================================ K3: the history is frozen after the switch =========================

@needs_git
def test_k3_before_the_switch_a_history_line_passes(tmp_path):
    root = init_repo(tmp_path / "r")
    append(root, HISTORY, delegated("t-003", "2026-10-02T08:00:00"))
    stage(root, HISTORY)
    proc = validate(root)
    assert proc.returncode == 0, proc.stderr


@needs_git
def test_k3_after_the_switch_a_history_line_is_refused_and_names_the_new_path(tmp_path):
    root = switched_repo(tmp_path / "r")
    append(root, HISTORY, delegated("t-004", "2026-10-02T09:00:00"))
    stage(root, HISTORY)
    proc = validate(root)
    assert proc.returncode == 1, proc.stderr
    assert "logs/routing-log.jsonl FAILED validation" in proc.stderr
    assert "takes no new lines" in proc.stderr and "write the line into logs/journal/dev1.jsonl" in proc.stderr


@needs_git
def test_k3_after_the_switch_without_a_slug_the_refusal_carries_the_door_for_the_slug(tmp_path):
    root = switched_repo(tmp_path / "r")
    set_slug(root, None)
    append(root, HISTORY, delegated("t-004", "2026-10-02T09:00:00"))
    stage(root, HISTORY)
    proc = validate(root)
    assert proc.returncode == 1, proc.stderr
    assert "takes no new lines" in proc.stderr
    assert "there is none to write to yet" in proc.stderr and "developer: <slug>" in proc.stderr
    assert "tools/dev.config.yaml" in proc.stderr


@needs_git
def test_k3_the_switch_commit_itself_may_carry_the_last_history_lines(tmp_path):
    # the freeze is read from the tree of HEAD, not from the index: the commit that creates the first
    # developer file may still append to the history
    root = init_repo(tmp_path / "r")
    append(root, HISTORY, delegated("t-003", "2026-10-02T07:00:00"))
    write(root, DEV1, jtext(M_CREATED, delegated("t-004", "2026-10-02T08:30:00")))
    stage(root, HISTORY, DEV1)
    proc = validate(root)
    assert proc.returncode == 0, proc.stderr


@needs_git
def test_k3_a_deleted_history_tail_is_still_refused_after_the_switch(tmp_path):
    # the freeze must not turn "the history takes no new lines" into "the history may shrink"
    root = switched_repo(tmp_path / "r")
    write(root, HISTORY, jtext(H1, H2))
    stage(root, HISTORY)
    proc = validate(root)
    assert proc.returncode == 1 and "FEWER lines" in proc.stderr


# ================================ K6: the negative control ============================================

BROKEN = "{this is not json"


@needs_git
def test_k6_control_a_valid_line_in_the_second_file_passes_in_precommit_and_in_all(tmp_path):
    root = switched_repo(tmp_path / "r", slug="dev2")
    base = git(root, "rev-parse", "HEAD").stdout.strip()
    append(root, DEV2, delegated("t-002", "2026-10-02T09:30:00"))
    stage(root, DEV2)
    assert validate(root).returncode == 0
    commit_all(root, "dev2 t-002", DEV2)
    proc = validate(root, "--all", "--base", base)
    assert proc.returncode == 0, proc.stderr


@needs_git
def test_k6_a_broken_line_in_the_second_file_is_refused_by_name_in_precommit(tmp_path):
    root = switched_repo(tmp_path / "r", slug="dev2")
    append(root, DEV2, BROKEN)
    stage(root, DEV2)
    proc = validate(root)
    assert proc.returncode == 1, proc.stderr
    assert "logs/journal/dev2.jsonl FAILED validation" in proc.stderr
    assert "invalid JSON" in proc.stderr and "line 3" in proc.stderr          # the file's own line number
    assert "dev1.jsonl FAILED" not in proc.stderr                            # the first file is not blamed


@needs_git
def test_k6_a_broken_line_in_the_second_file_is_refused_by_name_in_all(tmp_path):
    root = switched_repo(tmp_path / "r")
    base = git(root, "rev-parse", "HEAD").stdout.strip()
    append(root, DEV2, BROKEN)
    commit_all(root, "broken", DEV2)
    proc = validate(root, "--all", "--base", base)
    assert proc.returncode == 1, proc.stderr
    assert "logs/journal/dev2.jsonl FAILED validation" in proc.stderr and "invalid JSON" in proc.stderr
    assert "dev1.jsonl FAILED" not in proc.stderr


@needs_git
def test_k6_a_broken_line_in_the_first_file_is_not_attributed_to_the_second(tmp_path):
    root = switched_repo(tmp_path / "r")
    base = git(root, "rev-parse", "HEAD").stdout.strip()
    append(root, DEV1, BROKEN)
    commit_all(root, "broken", DEV1)
    proc = validate(root, "--all", "--base", base)
    assert proc.returncode == 1
    assert "logs/journal/dev1.jsonl FAILED validation" in proc.stderr
    assert "dev2.jsonl FAILED" not in proc.stderr


# ================================ K9: --all (CI) ======================================================

def _three_hours_ahead() -> str:
    return (datetime.datetime.now() + datetime.timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S")


@needs_git
def test_k9_a_ts_three_hours_ahead_passes_in_all_and_fails_in_precommit(tmp_path):
    # the CI runner's clock (UTC) is not the writer's: drift is off in --all, on at the commit
    root = switched_repo(tmp_path / "r", slug="dev2")
    base = git(root, "rev-parse", "HEAD").stdout.strip()
    append(root, DEV2, delegated("t-002", _three_hours_ahead()))
    stage(root, DEV2)
    pre = validate(root)
    assert pre.returncode == 1 and "later than now+10min" in pre.stderr
    commit_all(root, "ahead", DEV2)
    ci = validate(root, "--all", "--base", base)
    assert ci.returncode == 0, ci.stderr
    assert "later than now+10min" not in ci.stderr


@needs_git
def test_k9_all_refuses_a_ts_that_goes_backwards_even_with_drift_off(tmp_path):
    root = switched_repo(tmp_path / "r")
    base = git(root, "rev-parse", "HEAD").stdout.strip()
    append(root, DEV2, delegated("t-002", "2026-10-02T08:00:00"))         # N1 is 09:00
    commit_all(root, "back", DEV2)
    ci = validate(root, "--all", "--base", base)
    assert ci.returncode == 1 and "not monotonic" in ci.stderr and "dev2.jsonl" in ci.stderr


@needs_git
def test_k9_a_deleted_journal_file_fails_all(tmp_path):
    root = switched_repo(tmp_path / "r")
    base = git(root, "rev-parse", "HEAD").stdout.strip()
    git(root, "rm", "-q", "--", DEV2)
    git(root, "commit", "-q", "-m", "delete")
    ci = validate(root, "--all", "--base", base)
    assert ci.returncode == 1
    assert "logs/journal/dev2.jsonl" in ci.stderr and "exists in the base and not in the tree" in ci.stderr


@needs_git
def test_k9_a_file_that_does_not_keep_the_base_as_a_prefix_fails_all(tmp_path):
    root = switched_repo(tmp_path / "r")
    base = git(root, "rev-parse", "HEAD").stdout.strip()
    text = (root / DEV2).read_text(encoding="utf-8").replace('"notes": "n"', '"notes": "edited"', 1)
    write(root, DEV2, text)
    commit_all(root, "edit", DEV2)
    ci = validate(root, "--all", "--base", base)
    assert ci.returncode == 1
    assert "logs/journal/dev2.jsonl FAILED validation" in ci.stderr
    assert "append-only" in ci.stderr and "unchanged prefix" in ci.stderr


@needs_git
def test_k9_all_arguments(tmp_path):
    root = switched_repo(tmp_path / "r")
    head = git(root, "rev-parse", "HEAD").stdout.strip()
    no_base = validate(root, "--all")
    assert no_base.returncode == 1 and "--all needs --base" in no_base.stderr
    merge_parent = validate(root, "--all", "--base", head, "--merge-parent", head)
    assert merge_parent.returncode == 1 and "cannot be combined" in merge_parent.stderr
    unknown = validate(root, HISTORY)                      # the old CI line: a path, silently ignored once
    assert unknown.returncode == 1 and "unknown argument" in unknown.stderr and HISTORY in unknown.stderr
    base_alone = validate(root, "--base", head)
    assert base_alone.returncode == 1 and "--base is for --all" in base_alone.stderr
    not_a_ref = validate(root, "--all", "--base", "no-such-ref")
    assert not_a_ref.returncode == 1 and "does not resolve to a commit" in not_a_ref.stderr and "no-such-ref" in not_a_ref.stderr
    ok = validate(root, "--all", "--base", head)
    assert ok.returncode == 0, ok.stderr


@needs_git
def test_k9_a_base_that_is_ahead_of_head_has_a_message_of_its_own(tmp_path):
    root = switched_repo(tmp_path / "r")
    older = git(root, "rev-parse", "HEAD").stdout.strip()
    append(root, DEV2, delegated("t-002", "2026-10-02T09:30:00"))
    newer = commit_all(root, "later", DEV2)
    git(root, "checkout", "-q", older)
    proc = validate(root, "--all", "--base", newer)
    assert proc.returncode == 1
    assert f"--all: {newer} is ahead of HEAD; fetch or choose the base of this branch" in proc.stderr
    assert "FEWER" not in proc.stderr
    same = validate(root, "--all", "--base", older)          # HEAD itself is not "ahead of" HEAD
    assert same.returncode == 0, same.stderr


@needs_git
def test_k9_all_on_a_history_frozen_by_the_base_refuses_new_history_lines(tmp_path):
    root = switched_repo(tmp_path / "r")
    base = git(root, "rev-parse", "HEAD").stdout.strip()
    append(root, HISTORY, delegated("t-004", "2026-10-02T09:00:00"))
    commit_all(root, "history again", HISTORY)
    ci = validate(root, "--all", "--base", base)
    assert ci.returncode == 1 and "takes no new lines" in ci.stderr


# ================================ K10: one writer per file ============================================

@needs_git
def test_k10_control_a_line_in_the_own_file_passes(tmp_path):
    root = switched_repo(tmp_path / "r")                    # the clone is dev1
    append(root, DEV1, delegated("t-004", "2026-10-02T09:00:00"))
    stage(root, DEV1)
    assert validate(root).returncode == 0


@needs_git
def test_k10_a_line_in_the_file_of_another_writer_is_refused_with_the_door(tmp_path):
    root = switched_repo(tmp_path / "r")                    # the clone is dev1, the line goes to dev2's file
    append(root, DEV2, delegated("t-002", "2026-10-02T09:30:00"))
    stage(root, DEV2)
    proc = validate(root)
    assert proc.returncode == 1, proc.stderr
    assert "logs/journal/dev2.jsonl FAILED validation" in proc.stderr
    assert "one file has one writer" in proc.stderr
    assert "write the line into your own file logs/journal/dev1.jsonl" in proc.stderr
    assert "closes:t-NNN@dev2" in proc.stderr


@needs_git
def test_k10_a_new_line_with_the_slug_unknown_is_refused_with_the_door_for_the_slug(tmp_path):
    root = switched_repo(tmp_path / "r")
    set_slug(root, None)
    append(root, DEV1, delegated("t-004", "2026-10-02T09:00:00"))
    stage(root, DEV1)
    proc = validate(root)
    assert proc.returncode == 1 and "developer slug is unknown" in proc.stderr and "tools/dev.config.yaml" in proc.stderr


def _diverged(root: Path, own_line: dict, other_line: dict) -> None:
    """main appends `own_line` to the owner's file, the branch `other` appends `other_line` to it
    too (one slug on two machines); `git merge --no-commit other` leaves the union staged."""
    git(root, "checkout", "-q", "-b", "other")
    append(root, DEV1, other_line)
    commit_all(root, "other tail", DEV1)
    git(root, "checkout", "-q", "main")
    append(root, DEV1, own_line)
    commit_all(root, "main tail", DEV1)
    assert git(root, "merge", "--no-commit", "--no-ff", "other", check=False).returncode == 0


@needs_git
def test_k10_a_merge_that_brings_lines_to_one_file_from_both_sides_is_a_warn_not_a_fail(tmp_path):
    root = switched_repo(tmp_path / "r")
    _diverged(root, delegated("t-004", "2026-10-02T10:00:00"), delegated("t-005", "2026-10-02T10:05:00"))
    proc = validate(root)                                      # MERGE_HEAD is present: the merge mode applies
    assert proc.returncode == 0, proc.stderr
    assert "written by two clones" in proc.stderr and "logs/journal/dev1.jsonl" in proc.stderr
    assert "one file has one writer" in proc.stderr and "a warning only" in proc.stderr


# ================================ the line-1 rules through git =========================================

@needs_git
def test_line1_not_a_journal_created_is_refused_naming_line_1(tmp_path):
    root = init_repo(tmp_path / "r", slug="dev2")
    write(root, DEV2, jtext(delegated("t-001", "2026-10-02T09:00:00")))
    stage(root, DEV2)
    proc = validate(root)
    assert proc.returncode == 1, proc.stderr
    assert "logs/journal/dev2.jsonl line 1 is not a journal_created event" in proc.stderr


@needs_git
def test_continues_on_line_1_of_the_first_file_passes_and_on_line_2_is_refused(tmp_path):
    root = init_repo(tmp_path / "r", slug="dev2")
    write(root, DEV2, jtext(N_CREATED, created("2026-10-02T08:20:00", continues=HISTORY)))
    stage(root, DEV2)
    proc = validate(root)
    assert proc.returncode == 1 and "`continues` is allowed on line 1 only" in proc.stderr


@needs_git
def test_two_files_that_continue_the_history_are_refused_naming_both(tmp_path):
    root = switched_repo(tmp_path / "r", slug="dev2", with_dev2=False)
    write(root, DEV2, jtext(created("2026-10-02T08:10:00", continues=HISTORY)))
    stage(root, DEV2)
    proc = validate(root)
    assert proc.returncode == 1, proc.stderr
    assert "more than one journal file continues the history" in proc.stderr
    assert DEV1 in proc.stderr and DEV2 in proc.stderr


@needs_git
def test_a_journal_file_that_is_removed_or_renamed_is_refused_in_precommit(tmp_path):
    root = switched_repo(tmp_path / "r")
    git(root, "mv", DEV2, "logs/journal/dev4.jsonl")
    proc = validate(root)
    assert proc.returncode == 1 and "is removed or renamed" in proc.stderr and DEV2 in proc.stderr


@needs_git
def test_a_file_with_an_illegal_name_is_refused_when_staged(tmp_path):
    root = init_repo(tmp_path / "r")
    write(root, "logs/journal/Dev2.jsonl", jtext(N_CREATED))
    stage(root, "logs/journal/Dev2.jsonl")
    proc = validate(root)
    assert proc.returncode == 1 and "Dev2.jsonl cannot be a journal file" in proc.stderr


@needs_git
def test_a_closes_label_that_names_no_file_is_a_warn_in_precommit(tmp_path):
    root = switched_repo(tmp_path / "r")
    append(root, DEV1, ev("dispatch_skipped", "2026-10-02T09:00:00", agent="scout",
                            notes="closes:t-001@ghost"))
    stage(root, DEV1)
    proc = validate(root)
    assert proc.returncode == 0, proc.stderr
    assert "'t-001@ghost' names the label 'ghost'" in proc.stderr and "closes nothing" in proc.stderr


# ================================ K1: two developer files merge ========================================

@needs_git
def test_k1_two_developer_files_merge_without_a_conflict_and_without_identity_lines(tmp_path):
    root = switched_repo(tmp_path / "r", with_dev2=False)
    base = git(root, "rev-parse", "HEAD").stdout.strip()
    git(root, "checkout", "-q", "-b", "dev2-branch")
    write(root, DEV2, jtext(N_CREATED, N1, delegated("t-002", "2026-10-02T09:10:00"),
                               delegated("t-003", "2026-10-02T09:20:00")))
    commit_all(root, "dev2", DEV2)
    git(root, "checkout", "-q", "main")
    append(root, DEV1, delegated("t-004", "2026-10-02T10:00:00"), accepted("t-002", "2026-10-02T10:10:00"))
    commit_all(root, "dev1", DEV1)
    merge = git(root, "merge", "--no-edit", "--no-ff", "dev2-branch", check=False)
    assert merge.returncode == 0, (merge.stdout, merge.stderr)
    assert not (root / "logs" / "journal-segments.json").exists()               # no identity lines needed
    assert sorted(git(root, "ls-files", "logs").stdout.split()) == sorted([HISTORY, DEV1, DEV2])
    ci = validate(root, "--all", "--base", base)
    assert ci.returncode == 0, ci.stderr
    j = jk.load_all(root)
    assert j.problems == []
    keys = {r.key for r in j.rows if r.key}
    assert ("", "t-004") in keys and ("dev2", "t-001") in keys and ("dev2", "t-003") in keys
    assert ("", "t-001") in keys and ("dev2", "t-004") not in keys
    assert jk.display(("dev2", "t-001")) == "t-001@dev2" and jk.display(("", "t-004")) == "t-004"


@needs_git
def test_k1_the_same_task_number_in_two_files_is_two_tasks_not_a_duplicate(tmp_path):
    # dev1's t-003 (the switch commit) and dev2's t-003 may both exist: the gate counts per file
    root = switched_repo(tmp_path / "r")
    base = git(root, "rev-parse", "HEAD").stdout.strip()
    append(root, DEV2, delegated("t-002", "2026-10-02T09:10:00"), delegated("t-003", "2026-10-02T09:20:00"))
    commit_all(root, "dev2 t-003", DEV2)
    assert validate(root, "--all", "--base", base).returncode == 0
    keys = {r.key for r in jk.load_all(root).rows if r.key}
    assert ("", "t-003") in keys and ("dev2", "t-003") in keys


# ================================ K11: the write-moment echo =============================================

import journal_echo as je

ECHO = TOOLS / "journal_echo.py"


@pytest.mark.parametrize("path,rel", [
    ("logs/routing-log.jsonl", HISTORY),
    ("logs/journal/../routing-log.jsonl", HISTORY),            # normalised first: the history
    ("C:\\r\\Logs\\Routing-Log.JSONL", HISTORY),
    ("Logs\\Journal\\Dev1.jsonl", "logs/journal/Dev1.jsonl"),      # a wrong-case slug is still a journal: the validator names it
    ("logs/journal/x.JSONL", "logs/journal/x.JSONL"),
    ("/abs/r/logs/journal/dev2.jsonl", DEV2),
    ("logs/journal/sub/x.jsonl", None), ("logs/journal-segments.json", None), ("xlogs/routing-log.jsonl", None),
    ("logs/not-routing-log.jsonl", None), ("logs/journal/.jsonl", None), ("logs/journal/x.txt", None),
    ("logs/journal", None), ("", None), (None, None), (7, None),
])
def test_k11_the_matcher(path, rel):
    assert je._journal_rel(path) == rel
    assert je._is_journal_path(path) == (rel is not None)


def test_k11_the_repo_root_is_the_directory_that_holds_logs(tmp_path):
    for sub in (HISTORY, DEV1):
        write(tmp_path, sub, "")
        assert je._repo_root(str(tmp_path / sub)) == tmp_path.resolve()


def echo(root: Path, rel: str) -> subprocess.CompletedProcess:
    payload = {"tool_name": "Write", "tool_input": {"file_path": str(Path(root) / rel)}}
    return subprocess.run([sys.executable, str(ECHO)], input=json.dumps(payload), capture_output=True, text=True,
                          encoding="utf-8", env=clean_env(), cwd=str(root))


@needs_git
def test_k11_a_clean_line_in_a_developer_file_is_silent_and_crlf_on_disk_is_not_an_edit(tmp_path):
    root = switched_repo(tmp_path / "r")
    append(root, DEV1, delegated("t-004", "2026-10-02T09:00:00"))
    # the fixture ts are fixed in the past, so the echo's own TS DRIFT layer speaks: only the journal layer is judged here
    clean = echo(root, DEV1)
    assert clean.returncode == 0 and "JOURNAL ECHO:" not in clean.stdout, (clean.stdout, clean.stderr)
    p = root / DEV1
    p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))             # a checkout with core.autocrlf=true
    crlf = echo(root, DEV1)
    assert crlf.returncode == 0 and "JOURNAL ECHO:" not in crlf.stdout, (crlf.stdout, crlf.stderr)
    assert "append-only" not in crlf.stdout + crlf.stderr


@needs_git
def test_k11_a_broken_line_in_a_developer_file_is_echoed(tmp_path):
    root = switched_repo(tmp_path / "r")
    append(root, DEV1, BROKEN)
    out = echo(root, DEV1)
    assert "JOURNAL ECHO:" in out.stdout and "invalid JSON" in out.stdout


@needs_git
def test_k11_a_write_to_the_history_after_the_switch_names_the_new_path(tmp_path):
    root = switched_repo(tmp_path / "r")
    append(root, HISTORY, delegated("t-003", "2026-10-02T09:00:00"))
    out = echo(root, HISTORY)
    assert "JOURNAL ECHO: 1 defect(s)" in out.stdout and "takes no new lines" in out.stdout
    assert "logs/journal/dev1.jsonl" in out.stdout
    set_slug(root, None)
    nameless = echo(root, HISTORY)
    assert "takes no new lines" in nameless.stdout and "there is none to write to yet" in nameless.stdout


@needs_git
def test_k11_a_write_to_the_history_before_the_switch_is_silent(tmp_path):
    root = init_repo(tmp_path / "r")
    append(root, HISTORY, delegated("t-003", "2026-10-02T08:00:00"))
    out = echo(root, HISTORY)
    assert out.returncode == 0 and "JOURNAL ECHO:" not in out.stdout


@needs_git
def test_k11_a_line_in_another_writers_file_is_echoed_with_the_door(tmp_path):
    root = switched_repo(tmp_path / "r")                               # the clone is dev1
    append(root, DEV2, delegated("t-002", "2026-10-02T09:30:00"))
    out = echo(root, DEV2)
    assert "one file has one writer" in out.stdout and "logs/journal/dev1.jsonl" in out.stdout


@needs_git
def test_k11_the_successor_is_validated_with_the_history_as_its_seed(tmp_path):
    root = init_repo(tmp_path / "r")
    write(root, DEV1, jtext(M_CREATED, delegated("t-003", "2026-10-02T08:30:00"), accepted("t-002", "2026-10-02T08:40:00")))
    assert "JOURNAL ECHO:" not in echo(root, DEV1).stdout            # t-003 = history max + 1, t-002 is a task of the history
    write(root, DEV1, jtext(M_CREATED, delegated("t-001", "2026-10-02T08:30:00")))
    assert "JOURNAL ECHO:" in echo(root, DEV1).stdout                 # t-001 is closed in the history: the seed is in force


@needs_git
def test_k11_a_path_that_is_not_a_journal_is_ignored_with_exit_0(tmp_path):
    root = switched_repo(tmp_path / "r")
    write(root, "logs/other.jsonl", BROKEN + "\n")
    out = echo(root, "logs/other.jsonl")
    assert out.returncode == 0 and out.stdout == "" and out.stderr == ""
    nested = echo(root, "logs/journal/sub/x.jsonl")
    assert nested.returncode == 0 and nested.stdout == ""


# ================================ K15: the other readers =================================================

import claim_control_gate as ccg
import critic_snapshot as csn
import main_gate as mg
import r3_integration_check as r3


def test_k15_main_gate_check_b_looks_at_the_file_this_clone_writes(tmp_path):
    root = make_root(tmp_path / "pre", history="")                       # before the switch: the history
    assert mg._journal_file(str(root)) == root / "logs" / "routing-log.jsonl"
    track = {"edits": [{"ts": "t1", "agent_id": None}], "runs": []}
    assert mg._journal_empty_warning_applies(str(root), track) is True
    after = make_root(tmp_path / "post", history=HISTORY_TEXT, files={DEV1: "", DEV2: jtext(N_CREATED)}, slug="dev1")
    assert mg._journal_file(str(after)) == after / DEV1
    assert mg._journal_empty_warning_applies(str(after), track) is True          # HER file is empty
    write(after, DEV1, jtext(M_CREATED))
    assert mg._journal_empty_warning_applies(str(after), track) is False         # non-empty now
    write(after, DEV1, "")
    write(after, jk.DEV_CONFIG_REL, "developer: dev2\n")
    assert mg._journal_empty_warning_applies(str(after), track) is False         # dev2's file is not empty


def test_k15_main_gate_is_silent_when_there_is_no_slug(tmp_path):
    after = make_root(tmp_path, history="", files={DEV1: "", DEV2: ""})
    assert mg._journal_file(str(after)) is None
    track = {"edits": [{"ts": "t1", "agent_id": None}], "runs": []}
    assert mg._journal_empty_warning_applies(str(after), track) is False


@pytest.mark.parametrize("path,expected", [
    ("logs/journal/dev1.jsonl", True), ("Logs/Journal/Dev2.JSONL", True), ("logs/routing-log.jsonl", True),
    ("logs/journal/sub/x.jsonl", False), ("logs/journal/x.txt", False), ("logs/other.jsonl", False), ("xlogs/journal/a.jsonl", False),
])
def test_k15_claim_control_gate_scope(path, expected):
    assert ccg._in_scope(path) is expected


def test_k15_critic_snapshot_ignores_every_journal_file_and_nothing_else(tmp_path):
    root = make_root(tmp_path, files={"code.py": "x = 1\n", DEV1: jtext(M_CREATED), DEV2: jtext(N_CREATED)}, slug="dev1")
    before = csn.compute_tree_hash(root)
    append(root, DEV1, delegated("t-003", "2026-10-02T08:30:00"))
    append(root, DEV2, delegated("t-001", "2026-10-02T09:00:00"))
    append(root, HISTORY, delegated("t-009", "2026-10-02T09:00:00"))
    write(root, "logs/journal/dev4.jsonl", "x\n")
    assert csn.compute_tree_hash(root) == before                        # a journal line is not drift of the tree under review
    write(root, "code.py", "x = 2\n")
    assert csn.compute_tree_hash(root)[0] != before[0]                  # control: a real change is
    write(root, "logs/journal/sub/x.jsonl", "x\n")
    assert csn.compute_tree_hash(root)[1] == before[1] + 1              # a nested path is not a journal file: counted


def commit_at(root: Path, date: str, message: str, *paths: str) -> None:
    env = clean_env(GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date)
    base = ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false"]
    for args in (["add", "--", *paths], ["commit", "-q", "-m", message]):
        proc = subprocess.run([*base, *args], cwd=root, capture_output=True, text=True, env=env)
        assert proc.returncode == 0, proc.stderr


def _r3_report(root: Path, monkeypatch, capsys) -> str:
    """r3.main on a tmp repo: git runs in the cwd, the journal is read from _repo_root() (the repository
    of the script itself, so both are pointed at the fixture)."""
    for k in _GIT_ENV_KEYS:
        monkeypatch.delenv(k, raising=False)
    monkeypatch.chdir(root)
    monkeypatch.setattr(r3, "_repo_root", lambda: root)
    assert r3.main(["--since", "2020-01-01"]) == 0
    return capsys.readouterr().out


@needs_git
def test_k15_r3_integration_check_finds_a_critic_trail_in_a_developer_file(tmp_path, monkeypatch, capsys):
    root = switched_repo(tmp_path / "r")
    (root / "small.txt").write_text("x\n", encoding="utf-8")
    commit_at(root, "2030-01-01T10:00:00", "prior", "small.txt")
    (root / "big.txt").write_text("".join(f"line {i}\n" for i in range(300)), encoding="utf-8")
    append(root, DEV2, delegated("t-002", "2030-01-01T11:00:00", agent="critic", category="review"),
           accepted("t-002", "2030-01-01T11:20:00", agent="critic", category="review", by="fable"))
    commit_at(root, "2030-01-01T12:00:00", "big", "big.txt", DEV2)
    found = _r3_report(root, monkeypatch, capsys)
    big = found.split("ts=2030-01-01T12:00:00", 1)[1].split("\n", 3)
    assert "NOT FOUND" not in big[1], found                       # the trail sits in dev2.jsonl, not in the history
    # control: the same commit with the trail outside its window is reported as a candidate
    root2 = switched_repo(tmp_path / "r2")
    (root2 / "small.txt").write_text("x\n", encoding="utf-8")
    commit_at(root2, "2030-01-01T10:00:00", "prior", "small.txt")
    (root2 / "big.txt").write_text("".join(f"line {i}\n" for i in range(300)), encoding="utf-8")
    append(root2, DEV2, delegated("t-002", "2029-12-31T11:00:00", agent="critic", category="review"))
    commit_at(root2, "2030-01-01T12:00:00", "big", "big.txt", DEV2)
    assert "critic trail NOT FOUND" in _r3_report(root2, monkeypatch, capsys).split("ts=2030-01-01T12:00:00", 1)[1]


def test_k15_r3_integration_check_reads_every_journal_file(tmp_path):
    root = make_root(tmp_path, files={DEV1: jtext(M_CREATED, delegated("t-003", "2026-10-02T08:30:00")),
                                      DEV2: jtext(N_CREATED, delegated("t-001", "2026-10-02T09:00:00"))}, slug="dev1")
    lines = r3.read_all_journal_lines(root)
    assert len(lines) == 3 + 2 + 2 and json.loads(lines[0])["task_id"] == "t-001"
    texts = "\n".join(lines)
    assert "t-003" in texts and '"t-001"' in texts and texts.count("journal_created") == 2
    assert r3.read_all_journal_lines(tmp_path / "nothing") == []


# ================================ K16: the pins ===========================================================

import hygiene_gate as hg
import warn_density as wd


@pytest.mark.parametrize("command", [
    "echo done >> logs/journal/dev2.jsonl", "printf '{}' > logs/journal/dev1.jsonl",
    "sed -i 's/x/y/' logs/journal/dev1.jsonl", "tee -a logs/journal/dev4.jsonl",
])
def test_k16_hygiene_gate_refuses_a_shell_write_into_a_developer_file(command):
    exit_code, output = hg.decide({"tool_name": "Bash", "tool_input": {"command": command}})
    assert exit_code == 0 and output["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert output["hookSpecificOutput"]["permissionDecisionReason"] == hg.MSG_JOURNAL_BLOCK


def test_k16_hygiene_gate_lets_a_read_of_a_developer_file_through():
    exit_code, output = hg.decide({"tool_name": "Bash", "tool_input": {"command": "sed -n '1p' logs/journal/dev1.jsonl"}})
    assert exit_code == 0 and not (output or {}).get("hookSpecificOutput", {}).get("permissionDecision") == "deny"


@pytest.mark.parametrize("tool,path,expected", [
    ("Edit", "logs/journal/dev2.jsonl", True), ("Write", "logs/journal/dev1.jsonl", True),
    ("Edit", "logs/routing-log.jsonl", True), ("Read", "logs/journal/dev1.jsonl", False),
    ("Edit", "logs/journal/sub/x.jsonl", False), ("Edit", "tools/other.py", False),
])
def test_k16_warn_density_population_includes_the_developer_files(tool, path, expected):
    assert wd._population_journal_path(tool, {"file_path": path}) is expected


def test_k16_the_mechanism_closure_gains_no_module_but_dev_config():
    # journal_keys is stdlib plus ONE sibling, dev_config (the one reader of the config file), which imports
    # no tools module itself: the transitive closure of the live wiring grows by exactly that file
    import ast
    local = {p.stem for p in TOOLS.glob("*.py")}

    def siblings(path):
        tree = ast.parse(Path(path).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names.add(node.module.split(".")[0])
        return names & local
    assert siblings(TOOLS / "journal_keys.py") == {"dev_config"}
    assert siblings(TOOLS / "dev_config.py") == set()
