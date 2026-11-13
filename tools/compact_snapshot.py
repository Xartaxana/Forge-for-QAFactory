"""PreCompact hook: writes a FACTS-ONLY snapshot of the working state to
docs/tasks/compact-snapshots/<YYYY-MM-DD-HHMM>-<source>.md and prints a
one-line summary to stdout (the harness shows it in the transcript).

Why it exists: a compaction cannot be paused by a hook, so the hook has
to DO the saving, not merely remind. The snapshot automates the FACTUAL
part of the hand-written "State at HH:MM" section of
docs/tasks/factory-fixes.md (uncommitted files, open dispatches, next
free task id, the journal tail, the carriers to re-read). It holds no
prose from the model: a hook sees only the disk, never the conversation.
The narrative stays the Lead's hand-written section; this file is what
that section must not contradict.

Sources of facts: `git status --porcelain`, `git log -1`, the rev-list
count against the upstream, logs/routing-log.jsonl, and file mtimes.

Invocation (settings.json, PreCompact, no matcher):
    python tools/compact_snapshot.py
The source (manual / auto) comes from the harness's stdin payload
("trigger"), then "unknown"; --source overrides the payload for a manual
run.

Contract: NEVER blocks a compaction. Any failure -> one printed line,
exit 0. Missing git / unreadable journal are stated inside the snapshot,
which is still written. Retention: when the folder holds 50+ snapshots
the oldest beyond the newest 30 are deleted ONLY if committed (tracked
and clean); an uncommitted file is never deleted (sessions never delete)
-- the count of kept-because-uncommitted is printed instead.

Time (t-323 B5, critic t-322 C-F1..C-F3): the git facts are collected under
ONE total deadline (GIT_TOTAL_DEADLINE, not one 15 s timeout per call - the
collection makes up to seven calls); past it the remaining facts are not
collected and the snapshot names them. The snapshot is written, and its
summary printed, BEFORE the retention work (two more git calls) starts, so a
hook cut off there has already done its job. After a stdin deadline the
process leaves with os._exit(0), as tools/session_context.py does: a reader
thread still blocked in a platform read can turn a normal exit into a crash.
The deadline never changes the exit code (always 0) and never adds a line to
what the hook prints (the summary, and the retention line when one is due).
"""

import argparse
import datetime
import json
import os
import re
import sys
import threading
import time
from pathlib import Path

import gitcmd

SNAPSHOT_DIR = Path("docs") / "tasks" / "compact-snapshots"
JOURNAL_REL = Path("logs") / "routing-log.jsonl"

LIST_CAP = 60  # per file list (package / Forge / untracked), then "and N more"
HEAD_CAP = 100
JOURNAL_TAIL = 8
NOTE_CAP_JOURNAL = 100
NOTE_CAP_DISPATCH = 120
PRUNE_TRIGGER = 50  # prune only when the folder holds this many snapshots or more
PRUNE_KEEP = 30
GIT_TIMEOUT = 15  # the ceiling of ONE git call (retention's calls); collect_git's calls share GIT_TOTAL_DEADLINE
GIT_TOTAL_DEADLINE = 10  # seconds for ALL the git facts of one snapshot together
GIT_FACTS = ("HEAD", "branch", "origin", "UNCOMMITTED")  # what collect_git can fail to collect, in the snapshot's words
_deadline_at = None  # time.monotonic() at which collect_git stops asking; None outside collect_git
_STDIN_STATE = {"hit": False}  # the stdin deadline passed: a reader thread may still be blocked (see the bottom)

_SKIP_DIRS = {"__pycache__", ".git", "node_modules"}
_TID_RE = re.compile(r"^t-(\d+)$")

REMINDER = (
    "After the compact: read CURRENT_CONTEXT.md, then the newest hand-written narrative of "
    "docs/tasks/compact-snapshots/ (the newest file of that folder whose first line is not a hook header, "
    "whatever its name; the SessionStart line COMPACT NARRATIVE names it when it is newer), then this snapshot's OPEN DISPATCHES (accept them in a batch; "
    "a dead worker is a `replaces_worker` dispatch). The Lead writes the narrative by hand; "
    "this file holds the facts the hand-written one must not contradict."
)

# The identity of a hook snapshot is its FIRST line (an HTML comment): a file name cannot tell a hook snapshot from a
# hand-written narrative of the same name family. This module is the ONE writer (header_line) and the ONE reader
# (snapshot_identity) of that line; tools/session_context.py imports them (AR-22).
HOOK_HEADER_PREFIX = "<!-- compact-snapshot: hook"
HEADER_READ_BYTES = 512
SESSION_UNKNOWN = "unknown"
_SESSION_CHARS_RE = re.compile(r"[^A-Za-z0-9_.-]+")
_SESSION_CAP = 64
_HEADER_FIELD_RE = re.compile(r"(?:^|;)\s*(session|trigger|written):\s*([^;>]*?)\s*(?=;|-->|$)")


def clean_session_id(value):
    """A session id as the header carries it: only [A-Za-z0-9_.-], at most 64 characters (a header stays one line and
    never holds `;` or `-->`); None when `value` is no usable id. Never raises."""
    try:
        if not isinstance(value, str):
            return None
        cleaned = _SESSION_CHARS_RE.sub("", value)[:_SESSION_CAP]
        return cleaned or None
    except Exception:
        return None


def header_line(session, trigger: str, written: datetime.datetime) -> str:
    """The first line of a hook snapshot (the one writer of the form)."""
    trig = trigger if trigger in ("manual", "auto") else "unknown"
    return (f"{HOOK_HEADER_PREFIX}; session: {clean_session_id(session) or SESSION_UNKNOWN}; "
            f"trigger: {trig}; written: {written.strftime('%Y-%m-%dT%H:%M:%S')} -->")


def snapshot_identity(path):
    """{"session", "trigger", "written"} of a hook snapshot, or None when the first line is no hook header (a
    hand-written narrative, an old file written before the header existed). Reads at most HEADER_READ_BYTES bytes.
    A header whose prefix is present but whose fields are missing or odd is still a hook snapshot: the missing field
    reads "unknown". A read failure raises OSError (the caller decides: the file is skipped)."""
    with open(path, "rb") as f:
        raw = f.read(HEADER_READ_BYTES)
    first = raw.decode("utf-8", "replace").lstrip("﻿").split("\n", 1)[0].strip()
    if not first.startswith(HOOK_HEADER_PREFIX):
        return None
    fields = {k: v for k, v in _HEADER_FIELD_RE.findall(first[len(HOOK_HEADER_PREFIX):])}
    return {
        "session": fields.get("session") or SESSION_UNKNOWN,
        "trigger": fields.get("trigger") or "unknown",
        "written": fields.get("written") or "unknown",
    }


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def one_line(value, cap: int) -> str:
    """Single-line, whitespace-collapsed, length-capped text; never raises."""
    try:
        text = " ".join(str(value if value is not None else "").split())
    except Exception:
        text = "<unprintable>"
    if len(text) > cap:
        text = text[:cap]
    return text


def fmt_mtime(path: Path) -> str:
    try:
        ts = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        return ts.strftime("%Y-%m-%d %H:%M")
    except OSError:
        return "missing"


# -- git ---------------------------------------------------------------


def run_git(args: list, root: Path):
    """(ok, stdout). ok False when git cannot run, exits non-zero or does not
    answer in time. Never raises. Inside collect_git the time allowed is what
    is left of the total deadline (at most GIT_TIMEOUT), never a fresh one."""
    timeout = GIT_TIMEOUT
    if _deadline_at is not None:
        timeout = max(0.05, min(GIT_TIMEOUT, _deadline_at - time.monotonic()))
    try:
        rc, raw = gitcmd.git(root, *args, timeout=timeout)
    except Exception:
        return False, ""
    if rc == -1:                                       # git could not run or timed out: the message is not output
        return False, ""
    return rc == 0, raw.decode("utf-8", "replace")


def group_status(entries: list) -> dict:
    """package = tracked changes under ai-packages/, forge = tracked
    changes elsewhere, untracked = `??` entries (any path)."""
    groups = {"package": [], "forge": [], "untracked": []}
    for xy, path in entries:
        if xy == "??":
            groups["untracked"].append((xy, path))
        elif path.replace("\\", "/").startswith("ai-packages/"):
            groups["package"].append((xy, path))
        else:
            groups["forge"].append((xy, path))
    return groups


def collect_git(root: Path, total_s: float = None) -> dict:
    """The git facts of the snapshot, under ONE total deadline (`total_s`,
    default GIT_TOTAL_DEADLINE). `missed` lists the facts (GIT_FACTS) that were
    not collected because the deadline passed - a fact that was asked and
    simply failed is not "missed", it is stated as failed where it is used.
    Never raises beyond what run_git never raises."""
    global _deadline_at
    total_s = GIT_TOTAL_DEADLINE if total_s is None else total_s
    end = time.monotonic() + total_s
    info = {"available": False, "head": None, "branch": None, "sync": None, "entries": None,
            "missed": [], "deadline_s": total_s}

    def ask(args, *facts):
        """(ok, out), or None when the deadline had passed before the call or ended it."""
        if time.monotonic() >= end:
            info["missed"] += [f for f in facts if f not in info["missed"]]
            return None
        ok, out = run_git(args, root)
        if not ok and time.monotonic() >= end:  # the call was cut by the deadline (or failed right at it)
            info["missed"] += [f for f in facts if f not in info["missed"]]
            return None
        return ok, out

    _deadline_at = end
    try:
        got = ask(["rev-parse", "--is-inside-work-tree"], *GIT_FACTS)
        if got is None or not got[0] or got[1].strip() != "true":
            return info
        info["available"] = True
        got = ask(["log", "-1", "--format=%h %s"], "HEAD")
        if got:
            ok, out = got
            info["head"] = one_line(out, HEAD_CAP) if ok and out.strip() else None
        got = ask(["rev-parse", "--abbrev-ref", "HEAD"], "branch", "origin")
        if got:
            ok, out = got
            info["branch"] = out.strip() if ok and out.strip() else None
        got = ask(["rev-list", "--left-right", "--count", "HEAD...@{u}"], "origin")
        if got:
            ok, out = got
            if not ok and info["branch"]:
                got = ask(["rev-list", "--left-right", "--count", f"HEAD...origin/{info['branch']}"], "origin")
                ok, out = got if got else (False, "")
            if ok and len(out.split()) == 2:
                ahead, behind = out.split()
                info["sync"] = f"ahead {ahead}, behind {behind}"
        got = ask(["status", "--porcelain", "-z"], "UNCOMMITTED")
        if got and got[0]:
            info["entries"] = gitcmd.parse_status_z(got[1])
        return info
    finally:
        _deadline_at = None


# -- journal -----------------------------------------------------------


def read_journal(root: Path):
    """(events, bad_lines, error). A malformed line is skipped and counted;
    an unreadable file gives error text and no events. Never raises."""
    path = root / JOURNAL_REL
    if not path.exists():
        return [], 0, f"missing ({JOURNAL_REL.as_posix()})"
    events, bad = [], 0
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    bad += 1
                    continue
                if isinstance(obj, dict):
                    events.append(obj)
                else:
                    bad += 1
    except Exception as e:
        return [], 0, f"unreadable ({type(e).__name__}: {one_line(e, 80)})"
    return events, bad, None


def journal_view(root: Path):
    """(journal_keys, Journal) of `root` through the one loader of the per-developer journal (t-581),
    or None when journal_keys cannot be imported or loaded -- the caller then reads the history alone
    (read_journal), as before. Never raises."""
    try:
        import journal_keys as jk

        return jk, jk.load_all(root)
    except Exception:
        return None


def open_dispatches_with_source(events: list, journal=None):
    """(open dispatches, used_fallback). The SessionStart hook's own function
    when importable (one definition of 'open', closes:t-NNN markers included);
    else a plain fallback: the last delegated/accepted/rejected of a task is
    `delegated` - and `used_fallback` is True, so the snapshot can say that
    its list was computed by the weaker rule (t-323 B5). `journal` (t-581): the
    Journal the events came from, so that the tasks of several files are keyed by file."""
    try:
        import session_context  # same directory; guarded imports inside

        if journal is not None:
            return session_context.open_dispatches(events, journal.segments, journal=journal), False
        return session_context.open_dispatches(events), False
    except Exception:
        last = {}
        for e in events:
            tid = e.get("task_id")
            if tid and e.get("event") in ("delegated", "accepted", "rejected"):
                last[tid] = e
        return [e for e in last.values() if e.get("event") == "delegated"], True


def open_dispatches(events: list) -> list:
    return open_dispatches_with_source(events)[0]


def next_free_id(events: list) -> str:
    """The next id of the file's own sequence (rule 9e: journal_keys.next_ids -- a closed band is skipped, an open
    band raises the max). When journal_keys cannot be imported: max + 1 over the plain ids, as before."""
    try:
        import journal_keys

        return "t-%03d" % journal_keys.next_ids(events).main
    except Exception:
        pass
    top = 0
    for e in events:
        m = _TID_RE.match(str(e.get("task_id") or ""))
        if m:
            top = max(top, int(m.group(1)))
    return f"t-{top + 1:03d}"  # the journal's own width: t-008, t-318


def band_lines_of(events: list) -> list:
    """The `band t-A..t-B: next t-N` lines of the fallback path (rule 9e): [] when journal_keys cannot be imported."""
    try:
        import journal_keys

        return journal_keys.band_lines(journal_keys.next_ids(events))
    except Exception:
        return []


# -- carriers ----------------------------------------------------------


def newest_files(base: Path, n: int) -> list:
    found = []
    try:
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS]
            for name in filenames:
                p = Path(dirpath) / name
                try:
                    found.append((p.stat().st_mtime, p))
                except OSError:
                    continue
    except Exception:
        return []
    found.sort(key=lambda t: (t[0], str(t[1])), reverse=True)
    return [p for _, p in found[:n]]


def first_state_heading(path: Path) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for no, line in enumerate(f, 1):
                if line.startswith("## State at"):
                    return f"line {no}: {one_line(line.lstrip('# '), 140)}"
    except Exception as e:
        return f"unreadable ({type(e).__name__})"
    return "no `## State at` heading found"


FINDINGS_CAP = 240   # backlog_rows() text; the carrier line around it stays under 300 chars


def findings_summary(root: Path, cap: int) -> str:
    """The live findings (plans/piles/*/findings), read through tools/piles.py (tolerant: a finding that is not UTF-8 is
    counted as unreadable, the rest are read): how many in total and per pile, the newest one's date (Finding.date), how many
    carry `id: —` (not yet in a batch; an unreadable one has an UNKNOWN id and is not among them), how many are unreadable.
    Never raises."""
    try:
        import piles
        tree_ = piles.load_tree(root, tolerant=True)
        piles_ = tree_.piles
        unowned = len(piles.leftovers_unowned(tree_))
        counts = sorted(((len(p.findings), s) for s, p in piles_.items() if p.findings), key=lambda t: (-t[0], t[1]))
        every = [f for p in piles_.values() for f in p.findings]
        dates = [f.date for f in every if f.date]
    except Exception as e:
        return f"findings unreadable ({type(e).__name__})"
    head = f"findings: {len(every)} in {len(counts)} piles"
    broken = sum(1 for f in every if f.unreadable)
    tail = (f", newest {max(dates).isoformat()}" if dates else ", no dated finding") + \
        f", {sum(1 for f in every if not f.id and not f.unreadable)} with id: —" + (f", {broken} unreadable" if broken else "") + \
        f", {unowned} leftovers without an executor"   # never cut: only the per-pile listing shrinks under `cap`
    def line(items):
        rest = len(counts) - len(items)
        listing = ", ".join(items) + (f", +{rest} more" if rest else "")
        return head + (f" [{listing}]" if items else "") + tail

    shown = []
    for n, slug in counts:
        if len(line(shown + [f"{slug} {n}"])) > cap:
            break
        shown.append(f"{slug} {n}")
    return line(shown)


def backlog_rows(path: Path, root: "Path | None" = None) -> str:
    """The BACKLOG carrier text. `path` = plans/BACKLOG.md (the archive since the freeze of 08.10.2026);
    `root` = the repo root: given, and holding plans/piles, the live findings join it. Without `root` or
    without plans/piles the text is what it always was (an old clone has no freeze)."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            n = sum(1 for line in f if re.match(r"^\|\s*B-\d+", line))
        archive = f"{n} rows (lines starting `| B-nnn`)"
    except Exception as e:
        archive = f"unreadable ({type(e).__name__})"
    if root is None or not (Path(root) / "plans" / "piles").is_dir():
        return archive
    prefix = f"archive (frozen 08.10): {archive}; "
    return prefix + findings_summary(Path(root), FINDINGS_CAP - len(prefix))


def carrier_lines(root: Path) -> list:
    def rel(p: Path) -> str:
        try:
            return p.relative_to(root).as_posix()
        except ValueError:
            return p.as_posix()

    lines = []
    cc = root / "CURRENT_CONTEXT.md"
    lines.append(f"- CURRENT_CONTEXT.md -- mtime {fmt_mtime(cc)}")
    ff = root / "docs" / "tasks" / "factory-fixes.md"
    lines.append(
        f"- docs/tasks/factory-fixes.md -- mtime {fmt_mtime(ff)}; first State heading: "
        f"{first_state_heading(ff)}"
    )
    bl = root / "plans" / "BACKLOG.md"
    lines.append(f"- plans/BACKLOG.md -- mtime {fmt_mtime(bl)}; {backlog_rows(bl, root)}")
    specs = root / "docs" / "tasks" / "specs"
    newest = newest_files(specs, 3) if specs.is_dir() else []
    lines.append("- newest 3 under docs/tasks/specs/:" + ("" if newest else " none"))
    lines.extend(f"    - {rel(p)} -- mtime {fmt_mtime(p)}" for p in newest)
    exp = root / "experiments"
    subs = sorted(d for d in exp.iterdir() if d.is_dir() and d.name not in _SKIP_DIRS) if exp.is_dir() else []
    lines.append("- newest 3 under each experiments/*/:" + ("" if subs else " none"))
    for d in subs:
        files = newest_files(d, 3)
        lines.append(f"    - {rel(d)}/" + ("" if files else " (empty)"))
        lines.extend(f"        - {rel(p)} -- mtime {fmt_mtime(p)}" for p in files)
    return lines


# -- snapshot ----------------------------------------------------------


def file_list(entries: list) -> list:
    lines = [f"  {xy} {path}" for xy, path in entries[:LIST_CAP]]
    if len(entries) > LIST_CAP:
        lines.append(f"  and {len(entries) - LIST_CAP} more")
    return lines


def build_snapshot(root: Path, source: str, now: datetime.datetime, session=None, trigger=None):
    """Returns (markdown_text, facts) where facts feeds the stdout summary. The first line is the hook header
    (header_line): `session` is the PreCompact payload's session id (None -> unknown); `trigger` defaults to
    `source` when that is manual or auto."""
    git = collect_git(root)
    view = journal_view(root)
    jk = journal = None
    cur_rel, own_label = JOURNAL_REL.as_posix(), ""
    if view is None:
        events, bad, jerr = read_journal(root)
        own_events = events
    else:
        jk, journal = view
        events = journal.events()
        bad = sum(1 for r in journal.rows if r.error)
        cur_rel, _why = jk.current_path(root)
        # with no developer journal file on disk the history is THE journal (before the switch), or there is no
        # journal at all (a fresh repository after the move): its missing / unreadable states are stated as they
        # always were (read_journal); once a developer file exists, a problem of the loader is a line of its own below
        jerr = read_journal(root)[2] if not jk.disk_journal_files(root) else None
        own_label = None
        own_events = events
        if cur_rel is not None:
            own_label = journal.writer_label(None if cur_rel == jk.HISTORY_REL else Path(cur_rel).stem)
            own_events = journal.events(journal.logical(own_label))
    switched = cur_rel != JOURNAL_REL.as_posix()

    out = [header_line(session, trigger if trigger is not None else source, now),
           f"# Compact snapshot -- {source}", "", "## 1. Header", ""]
    out.append(f"- when: {now.strftime('%Y-%m-%d %H:%M:%S')} (local system clock)")
    out.append(f"- source: {source}")
    missed = git.get("missed") or []
    deadline = f"the {git.get('deadline_s', GIT_TOTAL_DEADLINE):g} s git deadline passed"
    if git["available"]:
        out.append(f"- HEAD: {git['head'] or ('not collected (' + deadline + ')' if 'HEAD' in missed else 'unknown (no commits?)')}")
        out.append(f"- branch: {git['branch'] or ('not collected (' + deadline + ')' if 'branch' in missed else 'unknown')}")
        out.append(f"- origin: {git['sync'] or ('not collected (' + deadline + ')' if 'origin' in missed else 'no upstream / origin ref found')}")
    elif missed:
        out.append(f"- git: not collected, {deadline} before git answered; "
                   "HEAD / branch / origin / UNCOMMITTED are unknown (not 'none')")
    else:
        out.append("- git: unavailable (no git repository here, or git cannot run); "
                   "HEAD / branch / origin / UNCOMMITTED not collected")
    if missed and git["available"]:
        out.append(f"- not collected, {deadline}: {', '.join(f for f in GIT_FACTS if f in missed)}")

    out += ["", "## 2. UNCOMMITTED", ""]
    pkg = frg = unt = 0
    if not git["available"]:
        out.append(f"git not collected ({deadline}) -- UNCOMMITTED unknown" if missed
                   else "git unavailable -- not collected")
    elif git["entries"] is None:
        out.append(f"`git status --porcelain` not collected ({deadline}) -- UNCOMMITTED unknown"
                   if "UNCOMMITTED" in missed else "`git status --porcelain` failed -- not collected")
    else:
        groups = group_status(git["entries"])
        pkg, frg, unt = (len(groups[k]) for k in ("package", "forge", "untracked"))
        for key, title in (
            ("package", "package (ai-packages/**), tracked changes"),
            ("forge", "Forge (everything else), tracked changes"),
            ("untracked", "untracked"),
        ):
            extra = ""
            if key == "untracked":
                n_pkg = sum(1 for _, p in groups[key] if p.replace("\\", "/").startswith("ai-packages/"))
                extra = f" (under ai-packages/: {n_pkg}, elsewhere: {len(groups[key]) - n_pkg})"
            out.append(f"### {title}: {len(groups[key])}{extra}")
            out.extend(file_list(groups[key]) or ["  (none)"])
            out.append("")
        out.pop()  # trailing blank

    out += ["", "## 3. OPEN DISPATCHES", ""]
    if jerr:
        out.append(f"journal {jerr} -- open dispatches and next free id NOT computed")
        n_open, nxt = None, None
    else:
        opens, fallback = open_dispatches_with_source(events, journal)
        n_open = len(opens)
        band_ls: list = []
        if journal is None:
            nxt, nxt_label = next_free_id(events), "NEXT FREE ID"
            band_ls = band_lines_of(events)
        elif not switched:
            nxt, nxt_label = journal.next_free_id(""), "NEXT FREE ID"
            band_ls = jk.band_lines(journal.band_state(""))
        elif cur_rel is None:
            nxt, nxt_label = "unknown -- no developer slug", "NEXT FREE ID"
        else:
            nxt, nxt_label = journal.next_free_id(own_label), f"NEXT FREE ID ({cur_rel})"
            band_ls = jk.band_lines(journal.band_state(own_label))
        if fallback:
            out.append("(note: session_context could not be imported, so this list was computed by the plain "
                       "fallback rule - a `closes:t-NNN` marker is NOT honoured here: a dispatch closed that way "
                       "may show as open)")
        if bad:
            out.append(f"(note: {bad} malformed journal line(s) skipped)")
        if not opens:
            out.append("none")
        for e in opens:
            shown_id = e.get("task_id")
            if jk is not None and not fallback:
                key = jk.task_key(e, journal.segments)      # B-454: the key on the screen, t-NNN@label for a labelled task
                shown_id = jk.display(key) if key is not None else shown_id
            out.append(
                f"- {shown_id} agent={e.get('agent')} model={e.get('model')} "
                f"ts={e.get('ts')} worker_ref={e.get('worker_ref')} | "
                f"{one_line(e.get('notes'), NOTE_CAP_DISPATCH)}"
            )
        out.append("")
        out.append(f"{nxt_label}: {nxt}")
        out.extend(band_ls)        # rule 9e: the bands with a free id, so a session keeps its band across /compact

    out += ["", f"## 4. Last {JOURNAL_TAIL} journal events", ""]
    if jerr:
        out.append(f"journal {jerr}")
    elif not events:
        out.append("journal is empty")
    else:
        for e in own_events[-JOURNAL_TAIL:]:
            out.append(
                f"- {e.get('ts')} {e.get('event')} {e.get('task_id') or '-'} "
                f"{e.get('agent')} | {one_line(e.get('notes'), NOTE_CAP_JOURNAL)}"
            )

    out += ["", "## 5. Carriers to read after the compact", ""]
    out.extend(carrier_lines(root))

    out += ["", "## 6. Reminder", "", REMINDER, ""]
    known = git["available"] and git["entries"] is not None   # an uncollected status is "?", never 0 (FR-41)
    facts = {"open": n_open, "pkg": pkg if known else None,
             "forge": frg if known else None, "next": nxt}
    return "\n".join(out), facts


def safe_source(source) -> str:
    cleaned = re.sub(r"[^a-z0-9_-]+", "", str(source or "").lower())
    return cleaned[:20] or "unknown"


def write_unique(folder: Path, stem: str, text: str) -> Path:
    """Exclusive create: a second hook run inside the same minute gets
    `-2`, `-3`, ... -- never overwrites an earlier snapshot."""
    folder.mkdir(parents=True, exist_ok=True)
    n = 1
    while True:
        name = f"{stem}.md" if n == 1 else f"{stem}-{n}.md"
        path = folder / name
        try:
            with open(path, "x", encoding="utf-8", newline="\n") as f:
                f.write(text)
            return path
        except FileExistsError:
            n += 1
            if n > 500:
                raise


def prune(folder: Path, root: Path):
    """Returns (deleted, kept_uncommitted). Acts only when the folder holds
    PRUNE_TRIGGER or more snapshots; candidates are the oldest beyond
    PRUNE_KEEP; a candidate is deleted ONLY if tracked and clean in git."""
    snaps = sorted(p for p in folder.glob("*.md") if p.name.lower() != "readme.md")
    if len(snaps) < PRUNE_TRIGGER:
        return 0, 0
    candidates = snaps[: len(snaps) - PRUNE_KEEP]
    rel = folder.relative_to(root).as_posix() if folder.is_relative_to(root) else str(folder)
    ok_t, tracked_raw = run_git(["ls-files", "-z", "--", rel], root)
    ok_s, status_raw = run_git(["status", "--porcelain", "-z", "--", rel], root)
    if not (ok_t and ok_s):
        return 0, len(candidates)  # cannot prove committed -> delete nothing
    tracked = {Path(x).name for x in tracked_raw.split("\0") if x}
    dirty = {Path(p).name for _, p in gitcmd.parse_status_z(status_raw)}
    deleted = kept = 0
    for p in candidates:
        if p.name in tracked and p.name not in dirty:
            try:
                p.unlink()
                deleted += 1
            except OSError:
                kept += 1
        else:
            kept += 1
    return deleted, kept


def _read_trigger_from_stdin(deadline: float = 2.0):
    """(trigger, session_id) of the PreCompact payload: `trigger` (manual/auto) and `session_id`, each None
    when absent or odd (the whole pair is (None, None) on anything odd). Bounded by a deadline so a never-closed
    stdin cannot hang the hook."""
    try:
        if sys.stdin is None or sys.stdin.isatty():
            return None, None
        box = []

        def _reader():
            try:
                box.append(sys.stdin.read())
            except Exception:
                pass

        t = threading.Thread(target=_reader, daemon=True)
        t.start()
        t.join(deadline)
        if t.is_alive():
            _STDIN_STATE["hit"] = True  # the reader may stay blocked in a read: the exit at the bottom must not wait for it
        if not box or not box[0]:
            return None, None
        data = json.loads(box[0])
        if not isinstance(data, dict):
            return None, None
        trig = data.get("trigger")
        return (trig if isinstance(trig, str) and trig else None), clean_session_id(data.get("session_id"))
    except Exception:
        return None, None


def emit(text: str) -> None:
    try:
        reconf = getattr(sys.stdout, "reconfigure", None)
        if reconf:
            # The harness reads a hook's stdout as UTF-8; the Windows default
            # codepage would turn the dash into a replacement char. An explicit
            # PYTHONIOENCODING is honoured; encode errors are always replaced.
            if os.environ.get("PYTHONIOENCODING"):
                reconf(errors="replace")
            else:
                reconf(encoding="utf-8", errors="replace")
        sys.stdout.write(text + "\n")
        sys.stdout.flush()
    except Exception:
        pass


def write_snapshot(root: Path, source: str, now: datetime.datetime = None, session=None):
    """Writes the snapshot FILE and returns (summary line, snapshot folder).
    `session`: the session id for the header (None -> unknown).
    Nothing here touches retention: the file and its summary are done before
    prune's git calls start (t-323 B5). May raise; main() catches."""
    now = now or datetime.datetime.now()
    text, facts = build_snapshot(root, source, now, session=session)
    folder = root / SNAPSHOT_DIR
    path = write_unique(folder, f"{now.strftime('%Y-%m-%d-%H%M')}-{source}", text)
    rel = path.relative_to(root).as_posix()
    dash = "—"
    summary = (
        f"COMPACT SNAPSHOT: {rel} {dash} open dispatches "
        f"{'?' if facts['open'] is None else facts['open']}, uncommitted package "
        f"{'?' if facts['pkg'] is None else facts['pkg']} / forge "
        f"{'?' if facts['forge'] is None else facts['forge']}, next free id "
        f"{facts['next'] or '?'}"
    )
    return summary, folder


def retention_line(folder: Path, root: Path) -> str:
    """Prunes (see prune) and returns the retention line when something was
    kept because it is uncommitted, else "". Never raises."""
    try:
        deleted, kept = prune(folder, root)
    except Exception:
        kept = 0
    if kept:
        return (
            f"COMPACT SNAPSHOT: {kept} old snapshot(s) beyond the newest {PRUNE_KEEP} are "
            f"uncommitted and were NOT deleted (commit them, then they can be pruned)"
        )
    return ""


def run(root: Path, source: str, now: datetime.datetime = None) -> str:
    """Writes the snapshot, prunes, returns the summary line (plus a
    retention line when something was kept). May raise; main() catches."""
    summary, folder = write_snapshot(root, source, now)
    note = retention_line(folder, root)
    return summary + ("\n" + note if note else "")


def main(argv=None, root: Path = None) -> int:
    try:
        ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
        ap.add_argument("--source", default=None, help="manual | auto (default: stdin trigger)")
        ap.add_argument("--root", default=None, help="repo root (default: this file's parent's parent)")
        ap.add_argument("--session", default=None,
                        help="session id for the header (overrides the payload's; the door of a MISSING snapshot)")
        args, _unknown = ap.parse_known_args(argv)
        payload_trigger, payload_session = _read_trigger_from_stdin()
        source = args.source or payload_trigger or "unknown"
        session = clean_session_id(args.session) or payload_session
        use_root = Path(args.root) if args.root else (Path(root) if root else repo_root())
        summary, folder = write_snapshot(use_root, safe_source(source), session=session)
        emit(summary)  # out BEFORE retention: a hook cut off in prune's git calls has already reported
        note = retention_line(folder, use_root)
        if note:
            emit(note)
    except SystemExit:
        pass  # argparse exits on --help; never let the hook fail
    except BaseException as e:  # a hook crash must never block the compaction
        emit(f"COMPACT SNAPSHOT: failed ({type(e).__name__}: {one_line(e, 200)}) -- nothing saved")
    return 0


if __name__ == "__main__":
    _rc = main()
    if _STDIN_STATE["hit"]:
        # A stdin-reader thread may still be blocked deep inside a platform read - normal interpreter shutdown can
        # crash on that ("Fatal Python error: _enter_buffered_busy", a non-zero exit). Flush both streams, then leave
        # without the normal shutdown, as tools/session_context.py does after its own stdin deadline.
        for _stream in (sys.stdout, sys.stderr):
            try:
                _stream.flush()
            except Exception:
                pass
        os._exit(_rc)
    sys.exit(_rc)
