"""The coordinator's rule files: the one owner of the list and of the SessionStart line that names them.

CLAUDE.md is the worker block (auto-loaded into every worker); the coordinator's rules live in
COORDINATOR.md, PROJECT.md and the three indexes, which no worker loads at boot. A session that
is the coordinator learns of them from this line, printed by tools/session_context.py:

    COORDINATOR RULES: read <files> (<n> files, <bytes> bytes) before your first dispatch, acceptance or commit; ...

The three readers of the list -- the hook line, the boot-budget arithmetic of session_context.py and
the Codex AGENTS.md generator (tools/agents_md.py) -- take it from COORDINATOR_FILES, never from a copy.

Edges (spec worker-boot r2 section 6): a file that is absent, empty, a directory or unreadable is a
MISSING line with the git door (e1; presence by stat, never by decoding, and any doubt reads as
MISSING, so no session silently runs without its rules); coordinator_lines() never raises and prints
ASCII only (e2); stdlib only, so the S4 stream gate (tools/streams.py reaches only the sanctioned
road) stays closed (e16). Library only: no CLI.

The read check (FG7-89): read_state / read_warn judge from the main transcript whether each present file was
Read (structural Read results, line ranges that together cover the file) since the newest start, compaction
or clear; dispatch_gate and hygiene_gate append the WARN at a dispatch, a verdict and a commit. WARN only.
"""
import os
import re
import stat

import ascii_line  # noqa: E402  the one ASCII line helper (FG7-56), a stdlib leaf; plain sibling import (card F2 b)

COORDINATOR_FILES = (
    "COORDINATOR.md",
    "PROJECT.md",
    "docs/FACTORY_RULES_INDEX.md",
    "docs/ARCHITECTURE_INDEX.md",
    "docs/OWNER_PRINCIPLES_INDEX.md",
)

_TAIL = "workers do not read these at boot -- a role reads only the section its role file names"
_WHEN = {
    "resume": "re-read only if your context no longer holds them",
}
_WHEN_DEFAULT = "before your first dispatch, acceptance or commit"


# ASCII, single line, capped (the cap is required): the root and an exception text are not ours.
_ascii = ascii_line.clip  # the replace profile is clip's defaults: no keywords to bind


def _probe(root, name):
    """(size, None) for a file with bytes; (0, reason) otherwise. stat only, never a decode."""
    try:
        st = os.stat(os.path.join(str(root), name))
    except FileNotFoundError:
        return 0, "absent"
    except (OSError, ValueError):  # ValueError: an embedded NUL in the root
        return 0, "unreadable"
    if stat.S_ISDIR(st.st_mode):
        return 0, "directory"
    if not stat.S_ISREG(st.st_mode):
        return 0, "unreadable"
    if st.st_size == 0:
        return 0, "empty"
    return st.st_size, None


def _git_prefix(root):
    """`git -C "<root>"` when the root prints as ASCII whole; plain `git` otherwise (t-1250 F3).

    A space split the unquoted root into two git arguments, a cap cut it, a non-ASCII root became `?`:
    each named a door the reader could not use. The session cwd stays the repo root (hygiene point 3),
    so a bare `git` reaches the same repo."""
    text = str(root).strip()
    if not text or '"' in text or not re.fullmatch(r"[\x20-\x7e]+", text):
        return "git"
    return 'git -C "%s"' % text


def _unavailable(exc):
    try:
        detail = _ascii("%s: %s" % (type(exc).__name__, exc), 160)
    except Exception:  # noqa: BLE001 -- a pathological __str__; the line must still print
        detail = "%s: <unprintable exception>" % type(exc).__name__
    return "COORDINATOR RULES: unavailable (%s) -- read %s yourself" % (detail, ", ".join(COORDINATOR_FILES))


def coordinator_lines(root, source=None):
    """The SessionStart lines for the coordinator's rule files; never raises, ASCII only.

    One `read` line listing the files that are present and non-empty (resume source: the re-read form),
    and one MISSING line per file that is not, each with the git door. No present file -> no read line."""
    try:
        good, bad, total = [], [], 0
        for name in COORDINATOR_FILES:
            size, reason = _probe(root, name)
            if reason is None:
                good.append(name)
                total += size
            else:
                bad.append((name, reason))
        when = _WHEN.get(source, _WHEN_DEFAULT)
        lines = []
        if good:
            lines.append("COORDINATOR RULES: read %s (%d files, %d bytes) %s; %s"
                         % (", ".join(good), len(good), total, when, _TAIL))
        door = _git_prefix(root)
        for name, reason in bad:
            lines.append("COORDINATOR RULES: MISSING %s (%s) -- read it from git: %s show origin/main:%s; "
                         "until then this session has no coordinator rules"
                         % (name, reason, door, name))
        return lines
    except Exception as exc:  # noqa: BLE001 -- the hook never fails the session start (e2)
        return [_unavailable(exc)]


# ---- the read check (FG7-89): did the main session Read each rule file since its newest start/compaction? ----
# Why: Lead 501cb4e0 committed after a compaction without re-reading; only the SessionStart line named the duty.
# Measured from the transcript's structural Read result, never from any text the session writes. WARN only, at
# three duty points (a dispatch, a verdict, a commit) in the two gates. Error direction: a read that cannot be
# proven inside a judged window reads as `unread` (a WARN not deserved); a window or file that cannot be
# established reads as `cannot-judge` (never `unread`, and a future refusal must keep it a pass).
BOUNDARY_SOURCES = ("startup", "compact", "clear")    # `resume` keeps the restored context, so it is no boundary
READ_SCAN_MAX = 64 * 1024 * 1024                      # bytes read backwards at most per call (E7, E17)
_HOOK_PREFIX = "SessionStart:"
_LINE_CAP = 400


def _is_boundary(obj):
    """A parsed main-thread line that starts a fresh context: top-level compact_boundary, or the SessionStart hook
    attachment of a startup/compact/clear source. Text inside content never reaches here (E9)."""
    if obj.get("isSidechain") is True:
        return False
    if obj.get("type") == "system" and obj.get("subtype") == "compact_boundary":
        return True
    att = obj.get("attachment")
    name = att.get("hookName") if isinstance(att, dict) else None
    return isinstance(name, str) and name.startswith(_HOOK_PREFIX) and name[len(_HOOK_PREFIX):] in BOUNDARY_SOURCES


def _int(value):
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _key(path):
    try:
        return os.path.normcase(os.path.realpath(path))
    except (OSError, ValueError):
        return os.path.normcase(os.path.normpath(path))


def _read_of(obj, root):
    """(path key, start, end, total) of a structural Read result, else None (E5, E10)."""
    if obj.get("isSidechain") is True:
        return None
    res = obj.get("toolUseResult")
    fil = res.get("file") if isinstance(res, dict) and res.get("type") == "text" else None
    if not isinstance(fil, dict) or not isinstance(fil.get("filePath"), str):
        return None
    start, num, total = _int(fil.get("startLine")), _int(fil.get("numLines")), _int(fil.get("totalLines"))
    if start is None or num is None or total is None or start < 1 or num < 1 or total < 1 or num > total:
        return None
    path = fil["filePath"]
    return _key(path if os.path.isabs(path) else os.path.join(str(root), path)), start, start + num - 1, total


def _covered(ranges, total):
    """The merged ranges clipped to [1, total] and whether they cover all of it."""
    merged = []
    for a, b in sorted((max(1, a), min(total, b)) for a, b in ranges):
        if a > b:
            continue
        if merged and a <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return merged, merged == [[1, total]]


def _judge(transcript_path, root):
    """(verdict, unread, notes), never raises: verdict read | unread | cannot-judge; `unread` the uncovered present
    files (partial coverage in parentheses) or, for cannot-judge, [reason]; `notes` one text per absent file (E3)."""
    try:
        import transcripts  # lazy: SessionStart's import cost and the stdlib-only edge (e16) stay unchanged
        present, notes = {}, []
        for name in COORDINATOR_FILES:
            _size, reason = _probe(root, name)
            if reason is None:
                present[_key(os.path.join(str(root), name))] = name
            else:
                notes.append("cannot judge %s (%s)" % (name, reason))
        if not present:
            return "cannot-judge", ["no rule file is present"], notes
        if not os.path.isfile(transcript_path):
            return "cannot-judge", ["transcript is not a file"], notes
        lines, bounded = transcripts.lines_back_to(transcript_path, _is_boundary, READ_SCAN_MAX)
        if not bounded:
            return "cannot-judge", ["no start within %d MB" % (READ_SCAN_MAX // (1024 * 1024))], notes
        ranges, totals = {}, {}
        for line in lines:
            if '"toolUseResult"' not in line:
                continue
            obj = transcripts.parse_line(line)
            got = _read_of(obj, root) if obj is not None else None
            if got is not None and got[0] in present:
                ranges.setdefault(got[0], []).append((got[1], got[2]))
                totals[got[0]] = got[3]          # lines are chronological: the newest read's total wins
        unread = []
        for key, name in present.items():
            if key not in ranges:
                unread.append(name)
                continue
            merged, whole = _covered(ranges[key], totals[key])
            if not whole:
                shown = ",".join("%d-%d" % (a, b) for a, b in merged) or "none"
                unread.append("%s (lines %s of %d)" % (name, shown, totals[key]))
        return ("unread" if unread else "read"), unread, notes
    except OSError as exc:
        return "cannot-judge", ["transcript unreadable: %s" % type(exc).__name__], []
    except Exception as exc:  # noqa: BLE001 -- the judge never raises (E12)
        return "cannot-judge", [type(exc).__name__], []


def read_state(transcript_path, root):
    """(verdict, detail), pure and never raising, detail ASCII: `read`; `unread` with the uncovered files; or
    `cannot-judge` with one reason. Absent files ride in detail as `cannot judge <name> (<reason>)` notes."""
    verdict, items, notes = _judge(transcript_path, root)
    return verdict, _ascii("; ".join(items + notes), 1000)


def read_warn(payload, trigger):
    """The WARN text of the read check for a gate payload ("" = nothing to say); main thread only, never raises.
    A payload with a non-empty str agent_id is a worker (P38) and one without a non-empty str transcript_path
    and cwd is not the harness's: both are silent (E4, E6a)."""
    try:
        if not isinstance(payload, dict):
            return ""
        agent_id, path, cwd = payload.get("agent_id"), payload.get("transcript_path"), payload.get("cwd")
        if isinstance(agent_id, str) and agent_id:
            return ""
        if not (isinstance(path, str) and path and isinstance(cwd, str) and cwd):
            return ""
        verdict, items, notes = _judge(path, cwd)
        out = []
        if verdict == "unread":
            out.append("COORDINATOR-READ WARN: no Read since the last start/compaction of %s (before this %s) -- "
                       "Read each whole with the Read tool (the COORDINATOR RULES line); WARN, does not block"
                       % (", ".join(items), trigger))
        elif verdict == "cannot-judge":
            out.append("COORDINATOR-READ: cannot judge (%s) -- not checked; read %s if unsure"
                       % (items[0], ", ".join(COORDINATOR_FILES)))
        if verdict != "cannot-judge":
            out.extend("COORDINATOR-READ: " + n for n in notes)
        return "\n".join(_ascii(t, _LINE_CAP) for t in out)
    except Exception as exc:  # noqa: BLE001 -- the gate's verdict must not depend on this layer (E12)
        return "COORDINATOR-READ: cannot judge (%s) -- not checked" % type(exc).__name__
