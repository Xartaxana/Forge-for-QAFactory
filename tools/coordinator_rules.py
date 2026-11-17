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
"""
import os
import re
import stat

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


def _ascii(text, max_len=200):
    """ASCII, single line, capped: the root and an exception text are not ours."""
    text = re.sub(r"[\x00-\x1f\x7f]", "", str(text).strip())
    return text.encode("ascii", "replace").decode("ascii")[:max_len]


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
