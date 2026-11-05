"""tools/hook_liveness_probe.py -- liveness probe for ALL 13 hook gates
registered in .claude/settings.json of THIS kit (a port, batch v0.8.0
"full-mirror", D-0101). Mirrors the composition-checking pattern of
tools/wiring_check.py / tools/enforcement_probe.py (dynamic composition,
verified against the live source instead of a hardcoded list -- see
those files' own docstrings) applied to the whole hook family instead of
one pre-commit gate.

MOTIVE: several of these gates detect their OWN failure only by reading
their OWN trail (a sidecar file, a track record, a printed marker) --
"probe silence" and "nothing to report" are indistinguishable from the
OUTSIDE without an independent fact-trigger. This probe feeds each gate
a deliberately triggering stdin payload inside an isolated temporary
tree and asserts the expected trail. "Probe fed -> trail must exist" --
a gate's silence becomes distinguishable from "nothing happened".

SCOPE LIMITATION (read this before treating a clean run as "the gates
are wired correctly"): this probe proves the LIVENESS OF THE GATE'S
OWN CODE -- that tools/<gate>.py, invoked directly with a triggering
payload, produces the trail its own source promises. It does NOT prove
WIRING liveness: registration in .claude/settings.json, matcher
correctness, an active hooksPath, or that the harness actually invokes
this script on the events it claims to. Wiring is the zone of
tools/wiring_check.py and check 19(a) of
PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md -- a clean run of THIS probe
with a broken/unregistered hooksPath still reports every case OK,
because every case here invokes the script directly by path, never
through the harness's own hook dispatch. Composition coverage
(CASE-MISSING/STALE-CASE below) checks that every hook COMMAND named
in .claude/settings.json has a matching case and vice versa -- this is
a manifest-consistency check, not a wiring-liveness check either: it
never asserts the harness actually calls these commands on the events
it says it does.

NON-GOAL: no byte of any tools/<gate>.py is touched by this file (a
gate producing a wrong/missing trail is a live finding to report, never
silently patched here). .claude/settings.json is read-only.

WHY A DECLARATIVE CASES TABLE: each case names its target script, the
kind of trail it produces (a printed response, a written artifact, or
both), a short LITERAL anchor baked into this probe (independent of any
import), and -- where the gate exposes one -- the NAME of a public
constant/message string the case also verifies is still a non-empty
string via direct import (D-0043 "fix the class, not the instance" /
single source of truth: if the gate's own wording constant goes empty
or the import breaks, that is itself a finding, not something this
probe should paper over with its own copy of the string). A broken
import of a gate module is caught, printed as a finding (informational),
and does NOT crash the probe -- the case still runs on its baked
literal anchor alone.

ADAPTATION OF COMPOSITION (this kit's own hook set, not a mirror of any
source deployment's list): the registered commands in THIS kit's
.claude/settings.json are session_context, dispatch_gate,
critic_snapshot, owns_gate, hygiene_gate, claim_control_gate,
dod_track, journal_echo, search_control_gate, negative_lint, dod_gate,
main_gate -- plus the PreCompact hook compact_snapshot (case 13, added
t-390: it was registered in settings.json without a case, CASE-MISSING) --
the CASES table below targets exactly these 13 scripts,
using each gate's ACTUAL message constants/anchors as read from its own
source (several differ from a source deployment's wording -- e.g. this
kit's dod_gate.BLOCK_MESSAGE/main_gate.BLOCK_MESSAGE/
hygiene_gate.MSG_JOURNAL_BLOCK are plain English, with no Cyrillic
literal, unlike a bilingual source deployment's equivalents). owns_gate
carries its own overlap-warning trail (OWNS_OVERLAP, verified by
reading its source) in addition to its registration-artifact trail --
per this port's own design decision (checked, not assumed), this earns
a SECOND case ("2a") on the SAME script, exactly the same shape a
source deployment's own probe already uses for its own owns_gate.py:
CASES.script is not required to be unique, and the composition check
below operates on the SET of scripts, so one script backed by two cases
produces neither CASE-MISSING nor STALE-CASE. CASE COUNT: 20 cases: 18 over
15 distinct Claude-hook scripts (case 0: the cost gate tools/agent_budget.py, D-0035; cases 16 and 16a: the
PreToolUse Edit|Write hook tools/handoff_gate.py, forge/5 F5-1 -- a critic-kind worker writing a non-handoff path
is refused, and the control: its own handoff path passes) plus two GIT-hook cases
("wiring": "githooks", outside the settings.json sverka): 14 tools/piles.py check refuses a broken tree and names
its item letter, 15 a commit-msg hook that runs mechanism_gate and then the piles check still refuses a mechanism
commit without an axis block (the `set -e` text of critic t-587 P1; the text is the probe's copy, not the live hook).

ONE-PROCESS TRACE WRITERS (t-802, forge/5 F5-8): since t-796 tools/dispatch_gate.py runs critic_snapshot and
owns_gate IN-PROCESS on an allowed dispatch (a refused one writes no trace), so cases 2 (owns registry row), 2a
(overlap warn) and 10 (critic snapshot) feed the GATE a complete allowed dispatch and look for the readers' outputs
AND their claim file `.claude/dispatch_claims/<tool_use_id>.<reader>` (dispatch_gate.claim_trace) in the case's own
tree; the standalone scripts have no case of their own and settings.json is expected to list only the gate for the
Task|Agent matcher. Two composition findings, outside the per-case verdicts: DOUBLE-RUN (critic_snapshot.py or
owns_gate.py still listed in settings.json -- the stale double-run world; a WARN line while POST_MERGE_DEFAULT is
False, a FAIL under `--post-merge` or once the Lead flips the default at the merge) and GATE-MATCHER (dispatch_gate.py
not listed under a PreToolUse matcher naming Task and Agent -- both traces silently gone; always a FAIL).
`--settings PATH` reads another settings.json (a what-if copy), read-only.

ISOLATION: every stateful case gets its OWN tempfile.mkdtemp() tree,
OUTSIDE this kit's own directory tree -- session_id values carry the
"liveness-probe-" prefix so a stray artifact is unmistakably this
probe's, not a real session's. Stateful gates that could otherwise
collide (owns_gate's two cases, dod_gate vs main_gate) get DIFFERENT
temp trees AND different session_id values. The invoked subprocess
itself always runs with cwd=<this kit's root> (the same shape every
registered hook command already uses, "python tools/<name>.py" from
the kit root) -- isolation from the LIVE tree is achieved through each
gate's own env-var override seams (SEARCH_CONTROL_GATE_LEDGER_DIR /
SEARCH_CONTROL_GATE_SAMPLE_PATH) and through the payload's own
"cwd"/"file_path" JSON fields, which is exactly how the gates already
source their own state-file locations -- not by changing the
OS-level working directory of the child process.

PRE/POST LIVE-STATE CHECK: before and after the whole case run, this
probe fingerprints (exists, size, mtime_ns, sha256) every real state
path a gate could have touched had isolation failed --
.claude/critic_snapshot.json, .claude/dod_track/ and
logs/.search-ledger/ (recursively, but ONLY files named with a
"liveness-probe-" session id: a live session's hooks write the files of
every OTHER session id at any moment, so those are outside the bracket;
a changed file under a probe id still fails),
logs/owns_registry.jsonl,
logs/routing-log.jsonl, logs/posttooluse-schema-sample.json,
docs/tasks/compact-snapshots/ (recursively), all under
THIS kit's own root (the directory containing this file's own
tools/ parent). Any difference -> LIVE-STATE-TOUCHED, overall run is
non-OK regardless of individual case verdicts -- a passing case that
quietly touched the live tree is a WORSE finding than a case that
plainly failed.

VERDICTS (per case): OK, DEAD (a trail was expected -- neither output
nor artifact appeared), MISMATCH (output/artifact appeared but the
anchor is missing, or the declared exit code does not match, or an
imported constant went empty), CRASH (an unhandled Python traceback
escaped the gate -- these gates are all documented fail-open; an
escaping traceback is itself the finding), HUNG (killed on timeout,
partial output reported), MISSING (the target script file does not
exist on disk). Composition-level findings: CASE-MISSING (a hook
command in .claude/settings.json has no matching case -- FAIL),
STALE-CASE (a case names a script no hook command in
.claude/settings.json references), SETTINGS-UNREADABLE
(.claude/settings.json missing/unparsable -- cases still run, overall
result is non-OK), NO-CASES (the CASES table itself is empty -- a
defect of this probe, not of any gate).

Fixing a gate producing an unexpected trail is NEVER done here (see
"NON-GOAL" above): a MISMATCH is a finding to report against the named
gate, and per this kit's routing rule (a builder never edits a
different worker's owned path) it goes back as a report line, not a
patch.

EXIT CODE: 0 iff every case is OK AND composition checks are clean AND
settings.json was readable AND no live-state drift was detected; 1
otherwise.

LIMITS (builder-role rule 6a -- boundary tests live in
tools/test_hook_liveness_probe.py): PER_CASE_TIMEOUT_SECONDS=20 is a
parameter of the runner (not a hardcoded literal at every call site),
overridable per case invocation; OUTPUT_EXCERPT_MAX_CHARS=500 truncates
any captured output/detail text embedded in a report line -- exactly
500 chars is kept whole, 501 is truncated with a trailing marker.
"""

import argparse
import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(REPO, "tools")
SETTINGS_PATH = os.path.join(REPO, ".claude", "settings.json")

PER_CASE_TIMEOUT_SECONDS = 20
OUTPUT_EXCERPT_MAX_CHARS = 500

# --- verdict vocabulary --------------------------------------------------
OK = "OK"
DEAD = "DEAD"
MISMATCH = "MISMATCH"
CRASH = "CRASH"
HUNG = "HUNG"
MISSING = "MISSING"
CASE_MISSING = "CASE-MISSING"
STALE_CASE = "STALE-CASE"
LIVE_STATE_TOUCHED = "LIVE-STATE-TOUCHED"
NO_CASES = "NO-CASES"
SETTINGS_UNREADABLE = "SETTINGS-UNREADABLE"
DOUBLE_RUN = "DOUBLE-RUN"
GATE_MATCHER = "GATE-MATCHER"

# --- the ONE-PROCESS shape of the Task|Agent trace writers (t-802, forge/5 F5-8) ----------------------------
# dispatch_gate.main() runs critic_snapshot.run_after_gate and owns_gate.run_after_gate in-process on an
# ALLOWED dispatch (t-796), so settings.json lists ONLY dispatch_gate for the Task|Agent matcher. The two
# standalone scripts stay runnable (and are still registered until the merge deletes their entries), but a
# registration of either next to the gate is the stale double-run world: the gate and the hook both write the
# trace (claim_trace keeps it from being written twice; it is still two processes where one is meant).
IN_PROCESS_TRACE_SCRIPTS = ("tools/critic_snapshot.py", "tools/owns_gate.py")
# Until the merge deletes the two entries a listing is a WARN line (the probe stays OK); with `--post-merge`
# (or this flag set True by the Lead at the merge) a listing FAILS the run. Not a code-liveness fact: a
# composition fact about settings.json, like CASE-MISSING.
POST_MERGE_DEFAULT = True  # flipped by the Lead at the F5-8 merge (settings.json lists dispatch_gate.py alone)
GATE_SCRIPT = "tools/dispatch_gate.py"
GATE_MATCHER_ALTERNATIVES = ("Task", "Agent")
CLAIMS_REL_PARTS = (".claude", "dispatch_claims")  # dispatch_gate.CLAIMS_REL_DIR, split for os.path.join

_TRACEBACK_MARKER = "Traceback (most recent call last):"

# --- pre/post live-state fingerprint --------------------------------------
_LIVE_STATE_TARGETS = (
    ("file", os.path.join(REPO, ".claude", "critic_snapshot.json")),
    ("dir-own", os.path.join(REPO, ".claude", "dod_track")),
    ("file", os.path.join(REPO, "logs", "owns_registry.jsonl")),
    ("dir-own", os.path.join(REPO, "logs", ".search-ledger")),
    ("file", os.path.join(REPO, "logs", "routing-log.jsonl")),
    ("dir", os.path.join(REPO, "logs", "journal")),
    ("file", os.path.join(REPO, "logs", "posttooluse-schema-sample.json")),
    ("dir", os.path.join(REPO, "docs", "tasks", "compact-snapshots")),
)


# Every session_id the probe's own cases use starts with this prefix
# (see the _case_* builders). A "dir-own" target (per-session state: the
# dod_track and search-ledger folders) is fingerprinted ONLY for files
# whose name carries such an id: a live session's hooks write files under
# any OTHER session id at any moment, so those are outside the bracket.
PROBE_SESSION_PREFIX = "liveness-probe-"


def _is_probe_session_file(filename: str) -> bool:
    return filename.startswith(PROBE_SESSION_PREFIX)


def _file_fingerprint(path):
    """(size, mtime_ns, sha256) of *path*, or None if it does not exist
    or cannot be read (a permission error is itself a fingerprint change
    relative to a readable "before" state, so it is not swallowed --
    None differs from any real tuple)."""
    try:
        st = os.stat(path)
    except OSError:
        return None
    try:
        with open(path, "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        digest = None
    return (st.st_size, st.st_mtime_ns, digest)


def snapshot_live_state() -> dict:
    """Fingerprints every real state path a gate could touch (see module
    docstring, "PRE/POST LIVE-STATE CHECK"). Directory targets are
    walked recursively; a missing directory contributes nothing (no key
    for it), same as a missing file contributing one key mapped to
    None -- both are DIFFERENT from "a file appeared there later" in the
    diff step (a new key appearing is itself a difference)."""
    snap = {}
    for kind, path in _LIVE_STATE_TARGETS:
        if kind == "file":
            snap[path] = _file_fingerprint(path)
        elif os.path.isdir(path):
            for dirpath, _dirnames, filenames in os.walk(path):
                for name in filenames:
                    if kind == "dir-own" and not _is_probe_session_file(name):
                        continue
                    fp = os.path.join(dirpath, name)
                    snap[fp] = _file_fingerprint(fp)
    return snap


def diff_live_state(before: dict, after: dict) -> list:
    """Sorted list of paths whose fingerprint changed OR that appeared/
    disappeared between the two snapshots."""
    keys = set(before) | set(after)
    return sorted(k for k in keys if before.get(k) != after.get(k))


# --- output excerpt truncation (rule 6a boundary) -------------------------


def format_excerpt(s, max_chars: int = OUTPUT_EXCERPT_MAX_CHARS) -> str:
    """"" for None; *s* unchanged when len(s) <= max_chars (500 kept
    whole); truncated with a trailing marker when len(s) > max_chars
    (501 -> 500 chars + marker) -- see module docstring "LIMITS"."""
    if s is None:
        return ""
    s = str(s)
    if len(s) <= max_chars:
        return s
    return s[:max_chars] + " …[truncated]"


# --- gate module imports (for the const-non-empty sanity check) ----------

# Canonical guard form (tools/owns_gate.py:278) -- .resolve() + a
# conditional insert, so a second import of this module (or a caller
# that already put tools/ on sys.path itself) never grows sys.path
# with a duplicate entry.
_TOOLS_DIR_RESOLVED = str(Path(TOOLS_DIR).resolve())
if _TOOLS_DIR_RESOLVED not in sys.path:
    sys.path.insert(0, _TOOLS_DIR_RESOLVED)

import streams  # noqa: E402 -- after the sys.path bootstrap above

_GATE_MODULE_NAMES = (
    "agent_budget",
    "dispatch_gate",
    "dispatch_manifest",
    "owns_gate",
    "claim_control_gate",
    "search_control_gate",
    "negative_lint",
    "dod_gate",
    "main_gate",
    "handoff_gate",
    "journal_echo",
    "hygiene_gate",
    "dod_track",
    "critic_snapshot",
    "session_context",
)

_GATE_MODULES = {}
IMPORT_FINDINGS = []


def _import_gate_modules():
    """Imports every gate module once, catching failures individually --
    see module docstring, "WHY A DECLARATIVE CASES TABLE": a broken
    import is a finding (recorded to IMPORT_FINDINGS), never a crash of
    this probe. Idempotent -- safe to call more than once (tests call it
    fresh per-test via importlib.reload where needed)."""
    for name in _GATE_MODULE_NAMES:
        try:
            _GATE_MODULES[name] = importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001 -- deliberate catch-all, see docstring
            _GATE_MODULES[name] = None
            IMPORT_FINDINGS.append(
                f"import {name} failed: {type(exc).__name__}: {exc}"
            )


_import_gate_modules()


def _verify_const(module_name, const_name):
    """Returns "" when *const_name* on the (already-imported) module
    named *module_name* is a non-empty string; otherwise a short finding
    string describing why (module not imported / attribute missing /
    not a non-empty string). Never raises."""
    mod = _GATE_MODULES.get(module_name)
    if mod is None:
        return f"module {module_name} not importable"
    value = getattr(mod, const_name, None)
    if not isinstance(value, str) or not value:
        return f"{module_name}.{const_name} is empty/missing"
    return ""


# --- settings.json composition sverka (both directions) ------------------

import re  # noqa: E402 -- after sys.path manipulation, same style as sibling gates

# Recognizes both legal hook-command shapes (same two forms
# tools/wiring_check.py's own _HOOK_COMMAND_RE and
# tools/enforcement_probe.py's own _PY_TOOL_CMD_RE recognize): the flat
# "python tools/<name>.py" form, and the $CLAUDE_PROJECT_DIR-qualified
# quoted form 'python "$CLAUDE_PROJECT_DIR/tools/<name>.py"'. Unlike
# enforcement_probe.py (which scans RAW file text and therefore needs to
# tolerate JSON-escaped quotes), this module's caller
# (load_settings_hook_commands) already runs settings.json through
# json.loads() first -- the command strings this regex sees are
# already-decoded Python strings with plain, unescaped quotes, the same
# shape wiring_check.py's own parser sees. Group 1 matches the flat
# form's filename; group 2 matches the qualified form's filename --
# exactly one is non-None on any successful match.
_PY_TOOL_CMD_RE = re.compile(
    r'python\s+(?:tools/([A-Za-z0-9_./\\-]+\.py)'
    r'|"\$CLAUDE_PROJECT_DIR/tools/([A-Za-z0-9_./\\-]+\.py)")'
)


def _read_text_best_effort(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except Exception:
        return None


def load_settings_hook_commands(settings_path: str = SETTINGS_PATH):
    """Returns (event_name, command) pairs for every command hook found
    in *settings_path*'s "hooks" object, or None if the file is missing/
    unparsable (SETTINGS-UNREADABLE, see module docstring)."""
    text = _read_text_best_effort(settings_path)
    if text is None:
        return None
    try:
        data = json.loads(text)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    hooks = data.get("hooks")
    if not isinstance(hooks, dict):
        return []
    pairs = []
    for event_name, entries in hooks.items():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            for h in entry.get("hooks", []) or []:
                if isinstance(h, dict) and isinstance(h.get("command"), str):
                    pairs.append((event_name, h["command"]))
    return pairs


def classify_settings_commands(pairs):
    """Splits (event, command) pairs into (referenced_scripts: set of
    "tools/<name>.py", info_lines: list of str) -- a non-python-tool
    command is informational, never a failure."""
    scripts = set()
    info_lines = []
    for event_name, cmd in pairs:
        m = _PY_TOOL_CMD_RE.search(cmd)
        if m:
            filename = m.group(1) or m.group(2)
            scripts.add(("tools/" + filename).replace("\\", "/"))
        else:
            info_lines.append(f'{event_name}: non-python hook command (informational): "{cmd}"')
    return scripts, info_lines


# --- subprocess case runner ------------------------------------------------


def run_subprocess_case(script_rel: str, payload: dict, env_overrides: dict = None,
                         timeout: int = PER_CASE_TIMEOUT_SECONDS, args=None) -> dict:
    """Invokes `python <repo>/<script_rel>` with *payload* fed as raw
    UTF-8 bytes on stdin (no text=True -- the real harness feeds raw
    bytes, not a text stream), cwd=<this kit's root> (the same shape
    every registered hook command already uses), env = os.environ
    copied + *env_overrides*. Returns a dict: {"missing": True} if the
    script file does not exist (no subprocess launched); {"hung": True,
    "stdout":..., "stderr":...} on timeout (subprocess.run already kills
    the child and returns whatever partial output it collected);
    otherwise {"returncode":..., "stdout":..., "stderr":...}.

    *args* (optional) are extra command-line arguments appended after the
    script path -- only a hook that has NO env/payload seam to redirect its
    own state (tools/compact_snapshot.py: `--root <tmp>`) needs them.

    *script_rel* is normally repo-relative ("tools/<name>.py", the shape
    every real case in CASES uses); an ALREADY-ABSOLUTE path (used by
    this file's own test suite for synthetic scripts living under
    pytest's tmp_path -- which may sit on a DIFFERENT drive than REPO,
    making os.path.relpath raise) is used as-is, never joined with REPO
    -- naive `os.path.join(REPO, *script_rel.split("/"))` on a split
    absolute path silently produces a WRONG relative path on Windows."""
    if os.path.isabs(script_rel):
        script_path = script_rel
    else:
        script_path = os.path.join(REPO, *script_rel.split("/"))
    if not os.path.isfile(script_path):
        return {"missing": True}

    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)

    input_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    try:
        proc = subprocess.run(
            [sys.executable, script_path] + [str(a) for a in (args or ())],
            input=input_bytes,
            capture_output=True,
            cwd=REPO,
            env=env,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "hung": True,
            "stdout": (exc.stdout or b"").decode("utf-8", errors="replace"),
            "stderr": (exc.stderr or b"").decode("utf-8", errors="replace"),
        }
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", errors="replace"),
        "stderr": proc.stderr.decode("utf-8", errors="replace"),
    }


def _looks_like_traceback(text: str) -> bool:
    return _TRACEBACK_MARKER in (text or "")


def check_response(result: dict, expected_exit, anchors=(), forbidden=()) -> tuple:
    """Verdict logic for a "response" trail -- see module docstring,
    "VERDICTS". Returns (verdict, detail)."""
    if result.get("missing"):
        return MISSING, "script file not found"
    if result.get("hung"):
        return HUNG, format_excerpt("HUNG -- partial stdout=%r stderr=%r" % (
            result.get("stdout", ""), result.get("stderr", "")))

    out = result.get("stdout", "")
    err = result.get("stderr", "")
    combined = out + err

    if _looks_like_traceback(out) or _looks_like_traceback(err):
        return CRASH, format_excerpt(combined)

    if not out.strip() and not err.strip():
        return DEAD, "no output at all (a trail was expected)"

    reasons = []
    rc = result.get("returncode")
    if expected_exit is not None and rc != expected_exit:
        reasons.append(f"exit {rc} != expected {expected_exit}")
    for anchor in anchors:
        if anchor not in combined:
            reasons.append(f"anchor missing: {anchor!r}")
    for bad in forbidden:
        if bad in combined:
            reasons.append(f"forbidden substring present: {bad!r}")

    if reasons:
        return MISMATCH, format_excerpt("; ".join(reasons) + " | output: " + combined)
    return OK, format_excerpt(combined)


def check_artifact_only(result: dict, expected_exit, artifact_ok: bool, artifact_detail: str) -> tuple:
    """Verdict logic for a pure "artifact" trail (kind=="artifact") --
    empty stdout/stderr is the documented NORM here (dod_track.py's own
    contract), so silence alone is never DEAD by itself; the artifact's
    own presence/content is the trail."""
    if result.get("missing"):
        return MISSING, "script file not found"
    if result.get("hung"):
        return HUNG, format_excerpt("HUNG -- partial stdout=%r stderr=%r" % (
            result.get("stdout", ""), result.get("stderr", "")))

    out = result.get("stdout", "")
    err = result.get("stderr", "")
    if _looks_like_traceback(out) or _looks_like_traceback(err):
        return CRASH, format_excerpt(out + err)

    rc = result.get("returncode")
    if expected_exit is not None and rc != expected_exit:
        return MISMATCH, f"exit {rc} != expected {expected_exit}"

    if not artifact_ok:
        return DEAD, format_excerpt(artifact_detail)
    return OK, format_excerpt(artifact_detail)


def check_response_and_artifact(result: dict, expected_exit, anchors, forbidden,
                                 artifact_ok: bool, artifact_detail: str) -> tuple:
    """kind=="response+artifact": both the printed trail AND the on-disk
    trail are required. The response check runs first (missing/hung/
    crash there wins outright); if the response is OK, a missing/wrong
    artifact downgrades the verdict to MISMATCH (we DID get a trail --
    a partial one -- so DEAD would understate what happened)."""
    verdict, detail = check_response(result, expected_exit, anchors, forbidden)
    if verdict != OK:
        return verdict, detail
    if not artifact_ok:
        return MISMATCH, f"{detail} | artifact check failed: {format_excerpt(artifact_detail)}"
    return OK, f"{detail} | artifact: {format_excerpt(artifact_detail)}"


# --- individual case builders ----------------------------------------------
# Each _case_N_* function returns a dict: {"payload":..., "env": {...}|None}.
# Called fresh at RUN time (never at import time) so every invocation gets
# its own tempfile.mkdtemp() tree -- see module docstring, "ISOLATION".

_TS_FORMAT = "%Y-%m-%dT%H:%M:%S"


def _mkdtemp(label: str) -> str:
    return tempfile.mkdtemp(prefix=f"hook-liveness-probe-{label}-")


def _fwd(path: str) -> str:
    return path.replace("\\", "/")


def _case_1_dispatch_gate():
    tmp = _mkdtemp("dispatch-gate")
    payload = {
        "tool_name": "Task",
        "cwd": tmp,
        "session_id": "liveness-probe-dispatch",
        "tool_input": {
            "subagent_type": "builder",
            "description": "sonnet: quick fix",
            "prompt": (
                "Please implement the quick fix and merge it into main "
                "without delay, thanks."
            ),
        },
    }
    return {"payload": payload, "env": None, "extra": {"tmp": tmp}}


def _case_0_agent_budget_worker_stop():
    """The cost gate (D-0035): a worker whose transcript shows a 450K context is STOPped (exit 2)
    on an Edit outside the close-out moves. The transcript tree and the sidecar folder live in
    the case's own temp tree (AGENT_BUDGET_DIR), never under this kit."""
    tmp = _mkdtemp("agent-budget")
    main = Path(tmp) / "proj" / "sess.jsonl"
    worker = Path(tmp) / "proj" / "sess" / "subagents" / "agent-w1.jsonl"
    worker.parent.mkdir(parents=True, exist_ok=True)
    main.write_text("", encoding="utf-8")
    usage = {"input_tokens": 2, "cache_creation_input_tokens": 1000, "cache_read_input_tokens": 448998,
             "output_tokens": 5}
    block = {"type": "tool_use", "id": "toolu_probe", "name": "Read", "input": {"file_path": "x"}}
    worker.write_text(json.dumps({"type": "assistant", "message": {"usage": usage, "content": [block]}}) + "\n",
                      encoding="utf-8")
    payload = {
        "tool_name": "Edit",
        "cwd": tmp,
        "session_id": "liveness-probe-budget-0",
        "agent_id": "w1",
        "transcript_path": _fwd(str(main)),
        "tool_input": {"file_path": _fwd(os.path.join(tmp, "x.py")), "old_string": "a", "new_string": "b"},
    }
    return {"payload": payload, "env": {"AGENT_BUDGET_DIR": os.path.join(tmp, "side")}, "extra": {"tmp": tmp}}


def _complete_builder_prompt(owns_path: str) -> str:
    """A COMPLETE builder dispatch (B-201): the gate refuses (exit 2, nothing registered) a builder dispatch
    missing any of given, owns, non-goals, handoff, edges, DoD (with a command in backticks), and since t-796
    the trace readers run only on an ALLOWED dispatch -- so the cases that prove the in-process trace road
    need a non-refused payload. B-245: an owns path absent under the cwd is refused unless marked (new)."""
    return (
        "Implement the probe feature.\n"
        "given: the whole repo\n"
        f"owns (ABSOLUTE write paths): {owns_path} (new)\n"
        "non-goals: no other file\n"
        "handoff: a short report\n"
        "edges: none -- a probe fixture, nothing to limit\n"
        "DoD: the probe feature is implemented; `python -m pytest tools/test_dispatch_gate.py -q` green.\n"
    )


def _claim_marker(tmp: str, tool_use_id: str, reader: str) -> str:
    """The claim file the gate's in-process call of `reader` leaves: .claude/dispatch_claims/<id>.<reader>
    (dispatch_gate.claim_trace). The folder does not exist on a first run; the gate creates it."""
    return os.path.join(tmp, *CLAIMS_REL_PARTS, f"{tool_use_id}.{reader}")


def _case_2_owns_gate_artifact():
    """t-802: owns_gate's registration is proved on the ONE-PROCESS road -- tools/dispatch_gate.py is run on an
    allowed builder dispatch and its in-process owns_gate call must leave the registry row AND its claim file."""
    tmp = _mkdtemp("owns-gate")
    owns_path = _fwd(os.path.join(tmp, "artifact_owned_file.py"))
    tool_use_id = "toolu_liveness_probe_2"
    payload = {
        "tool_name": "Task",
        "cwd": tmp,
        "session_id": "liveness-probe-owns-2",
        "tool_use_id": tool_use_id,
        "tool_input": {
            "subagent_type": "builder",
            "description": "sonnet: probe",
            "prompt": _complete_builder_prompt(owns_path),
        },
    }
    return {"payload": payload, "env": None,
            "extra": {"tmp": tmp, "owns_path": owns_path,
                      "claim_path": _claim_marker(tmp, tool_use_id, "owns_gate")}}


def _case_2a_owns_gate_overlap():
    tmp = _mkdtemp("owns-gate-overlap")
    owns_path = _fwd(os.path.join(tmp, "shared_owned_file.py"))
    owns_gate_mod = _GATE_MODULES.get("owns_gate")

    registry_path = Path(tmp) / "logs" / "owns_registry.jsonl"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    ts = now.strftime(_TS_FORMAT)
    prior = {
        "ts": ts,
        "session_key": "liveness-probe-owns-2a-prior",
        "cwd": tmp,
        "description": "prior probe write",
        "owns": [owns_path],
    }
    registry_path.write_text(json.dumps(prior, ensure_ascii=False) + "\n", encoding="utf-8")

    payload = {
        "tool_name": "Task",
        "cwd": tmp,
        "session_id": "liveness-probe-owns-2a-second",
        "tool_use_id": "toolu_liveness_probe_2a",
        "tool_input": {
            "subagent_type": "builder",
            "description": "sonnet: probe overlap",
            # complete, so the gate allows it and its in-process owns_gate call can warn (t-802)
            "prompt": _complete_builder_prompt(owns_path),
        },
    }
    return {
        "payload": payload, "env": None,
        "extra": {"tmp": tmp, "owns_path": owns_path, "owns_gate_mod": owns_gate_mod},
    }


def _case_3_claim_control_gate():
    tmp = _mkdtemp("claim-control")
    ledger_dir = os.path.join(tmp, "ledger")
    payload = {
        "tool_name": "Edit",
        "session_id": "liveness-probe-claim",
        "tool_input": {
            "file_path": "docs/probe_liveness_claim.md",
            "new_string": (
                "PROBE_TARGET_TOKEN.md does not exist anywhere in this "
                "repository."
            ),
        },
    }
    return {
        "payload": payload,
        "env": {"SEARCH_CONTROL_GATE_LEDGER_DIR": ledger_dir},
        "extra": {"tmp": tmp, "ledger_dir": ledger_dir},
    }


def _case_4_search_control_gate():
    tmp = _mkdtemp("search-control")
    ledger_dir = os.path.join(tmp, "ledger")
    sample_path = os.path.join(tmp, "posttooluse-schema-sample.json")
    session_id = "liveness-probe-search"
    payload = {
        "tool_name": "Grep",
        "session_id": session_id,
        "tool_input": {"pattern": "PROBE_LIVENESS_PATTERN_XYZ"},
        "tool_response": "",
    }
    return {
        "payload": payload,
        "env": {
            "SEARCH_CONTROL_GATE_LEDGER_DIR": ledger_dir,
            "SEARCH_CONTROL_GATE_SAMPLE_PATH": sample_path,
        },
        "extra": {"tmp": tmp, "ledger_dir": ledger_dir, "session_id": session_id},
    }


def _case_5_negative_lint():
    payload = {
        "tool_name": "Task",
        "tool_response": (
            "Checked the repository: file PROBE_MISSING_MARKER.md "
            "not found."
        ),
    }
    return {"payload": payload, "env": None, "extra": {}}


def _case_6_dod_gate():
    tmp = _mkdtemp("dod-gate")
    session_id = "liveness-probe-dodgate"
    agent_id = "liveness-probe-dodgate-agent"
    track_path = Path(tmp) / ".claude" / "dod_track" / f"{session_id}.json"
    track_path.parent.mkdir(parents=True, exist_ok=True)
    file_path = _fwd(os.path.join(tmp, "probe_target.py"))
    track = {
        "edits": [
            {
                "ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "tool_name": "Edit",
                "agent_id": agent_id,
                "file_path": file_path,
            }
        ],
        "runs": [],
        "gate_state": {"consecutive_blocks": 0, "per_agent": {}},
    }
    track_path.write_text(json.dumps(track, ensure_ascii=False), encoding="utf-8")

    payload = {
        "session_id": session_id,
        "cwd": tmp,
        "agent_id": agent_id,
        "hook_event_name": "SubagentStop",
    }
    return {
        "payload": payload, "env": None,
        "extra": {"tmp": tmp, "session_id": session_id, "track_path": str(track_path)},
    }


def _case_7_main_gate():
    tmp = _mkdtemp("main-gate")
    session_id = "liveness-probe-maingate"
    track_path = Path(tmp) / ".claude" / "dod_track" / f"{session_id}.json"
    track_path.parent.mkdir(parents=True, exist_ok=True)
    file_path = _fwd(os.path.join(tmp, "main_probe.py"))
    track = {
        "edits": [
            {
                "ts": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "tool_name": "Edit",
                "agent_id": None,
                "file_path": file_path,
            }
        ],
        "runs": [],
        "main_gate_state": {"consecutive_blocks": 0},
    }
    track_path.write_text(json.dumps(track, ensure_ascii=False), encoding="utf-8")
    # Deliberately NOT creating <tmp>/logs/routing-log.jsonl -- keeps the
    # empty-journal warning branch out of this case's scope.

    payload = {
        "session_id": session_id,
        "cwd": tmp,
        "hook_event_name": "Stop",
    }
    return {
        "payload": payload, "env": None,
        "extra": {"tmp": tmp, "session_id": session_id, "track_path": str(track_path)},
    }


def _case_8_journal_echo():
    tmp = _mkdtemp("journal-echo")
    journal_path = os.path.join(tmp, "logs", "routing-log.jsonl")
    os.makedirs(os.path.dirname(journal_path), exist_ok=True)
    with open(journal_path, "w", encoding="utf-8") as fh:
        fh.write("this is not a json line at all\n")

    payload = {
        "tool_name": "Edit",
        "tool_input": {"file_path": journal_path},
    }
    return {"payload": payload, "env": None, "extra": {"tmp": tmp}}


def _case_8b_journal_echo_developer_file():
    """The same hook on a file of the per-developer journal (t-581): a broken line in
    <tmp>/logs/journal/probe.jsonl must reach the echo through the matcher for that path."""
    tmp = _mkdtemp("journal-echo-dev")
    journal_path = os.path.join(tmp, "logs", "journal", "probe.jsonl")
    os.makedirs(os.path.dirname(journal_path), exist_ok=True)
    with open(journal_path, "w", encoding="utf-8") as fh:
        fh.write("this is not a json line at all\n")
    payload = {"tool_name": "Edit", "tool_input": {"file_path": journal_path}}
    return {"payload": payload, "env": None, "extra": {"tmp": tmp}}


def _case_9_dod_track():
    tmp = _mkdtemp("dod-track")
    session_id = "liveness-probe-dodtrack"
    file_path = _fwd(os.path.join(tmp, "probe_edit.py"))
    payload = {
        "tool_name": "Edit",
        "session_id": session_id,
        "cwd": tmp,
        "tool_input": {"file_path": file_path},
    }
    track_path = Path(tmp) / ".claude" / "dod_track" / f"{session_id}.json"
    return {
        "payload": payload, "env": None,
        "extra": {"tmp": tmp, "track_path": str(track_path), "file_path": file_path},
    }


def _case_10_critic_snapshot():
    tmp = _mkdtemp("critic-snapshot")
    # A non-empty tiny tree -- not required for correctness, but keeps
    # the snapshot's files_count meaningfully non-zero.
    (Path(tmp) / "probe_file_a.txt").write_text("probe content a\n", encoding="utf-8")

    # t-802: the snapshot is proved on the ONE-PROCESS road -- tools/dispatch_gate.py is run on an allowed
    # critic dispatch (R11-h: the report path on handoff:, a DoD with a command) and its in-process
    # critic_snapshot call must leave the snapshot AND its claim file.
    tool_use_id = "toolu_liveness_probe_10"
    payload = {
        "tool_name": "Task",
        "cwd": tmp,
        "session_id": "liveness-probe-critic-10",
        "tool_use_id": tool_use_id,
        "tool_input": {
            "subagent_type": "critic",
            "description": "opus: probe review",
            "prompt": (
                "Review the probe diff.\n"
                "given: the probe diff\n"
                f"handoff: {_fwd(os.path.join(tmp, 'review.md'))}\n"
                "DoD: the verdict names every finding; `python -m pytest tools/test_dispatch_gate.py -q` attached.\n"
            ),
        },
    }
    snap_path = Path(tmp) / ".claude" / "critic_snapshot.json"
    return {"payload": payload, "env": None,
            "extra": {"tmp": tmp, "snap_path": str(snap_path),
                      "claim_path": _claim_marker(tmp, tool_use_id, "critic_snapshot")}}


def _case_11_hygiene_gate():
    payload = {
        "tool_name": "Bash",
        "tool_input": {"command": "echo probe_marker >> logs/routing-log.jsonl"},
    }
    return {"payload": payload, "env": None, "extra": {}}


def _case_12_session_context():
    tmp = _mkdtemp("session-context")
    return {"payload": None, "env": None, "extra": {"tmp": tmp}}


def _case_13_compact_snapshot():
    """PreCompact hook. It has no env/payload seam for its output folder
    (the default root is the live kit root), so the case redirects it with
    `--root <tmp>`; the payload carries the harness's own `trigger` field."""
    tmp = _mkdtemp("compact-snapshot")
    payload = {"hook_event_name": "PreCompact", "trigger": "manual"}
    return {
        "payload": payload, "env": None, "args": ["--root", tmp],
        "extra": {"tmp": tmp, "snap_dir": str(Path(tmp) / "docs" / "tasks" / "compact-snapshots")},
    }


def _write_tmp(root: str, rel: str, text: str) -> None:
    path = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def _case_14_piles_check_refuses_broken_tree():
    """tools/piles.py (F0-2) is wired from .githooks/commit-msg, not from settings.json: the case feeds `check --all`
    a tree where one B-id has a finding file in TWO piles and expects the refusal to name item (а) and the id."""
    tmp = _mkdtemp("piles-check")
    _write_tmp(tmp, "plans/BACKLOG.md", "# B\n\n## 7. X\n\n| id | что сделать | почему | источник | принципы |\n|---|---|---|---|---|\n"
                                        "| B-135 | **Строка.** | п | и | п |\n\n## Закрыто\n\n| id | что сделать | почему | источник | принципы |\n|---|---|---|---|---|\n")
    card = ("# %s (`%s`)\n\nприоритет: П1 | фичи: F19 | стенд: не нужен | зона: `tools/`\n\n## Пачки\n\n"
            "| № | Что | Строки | Размер | Статус | Взял | Ветка | MR |\n|---|---|---|---|---|---|---|---|\n")
    for slug in ("alpha", "beta"):
        _write_tmp(tmp, "plans/piles/%s/README.md" % slug, card % (slug.title(), slug))
        _write_tmp(tmp, "plans/piles/%s/findings/B-135-x.md" % slug,
                   "# Находка\n\nid: B-135 | кучка: `%s` | от: probe | приоритет: — | кандидат наверх: нет\n\nЧто не так: x\n" % slug)
    return {"payload": {}, "env": None, "args": ["--repo", tmp, "check", "--all"], "extra": {"tmp": tmp}}


# The text the Lead places in .githooks/commit-msg (critic t-587, P1): `set -e` makes the hook exit with the FIRST failing
# gate, so a passing piles check cannot mask a mechanism_gate refusal. Tool paths are absolute here (the probe's repo).
_COMMIT_MSG_HOOK = """#!/bin/sh
set -e
python "{tools}/mechanism_gate.py" "$1"
python "{tools}/piles.py" --repo "{tmp}" check --msg-file "$1"
"""


def _case_15_commit_msg_hook_keeps_mechanism_refusal():
    tmp = _mkdtemp("commit-msg-hook")
    return {"payload": {}, "env": None, "extra": {"tmp": tmp}}


def _run_commit_msg_hook_case(built: dict) -> dict:
    """Runs a real `git commit` in a temp repo whose commit-msg hook is the two-gate text above: CLAUDE.md (a mechanism
    path) is staged and the message carries no axis block, so mechanism_gate must still refuse the commit."""
    tmp = built["extra"]["tmp"]
    env = {k: v for k, v in os.environ.items()
           if k not in ("GIT_DIR", "GIT_INDEX_FILE", "GIT_WORK_TREE", "GIT_PREFIX", "GIT_COMMON_DIR")}
    base = ["git", "-C", tmp, "-c", "user.name=probe", "-c", "user.email=probe@example.invalid", "-c", "commit.gpgsign=false"]
    hook = _COMMIT_MSG_HOOK.format(tools=_fwd(TOOLS_DIR), tmp=_fwd(tmp))
    _write_tmp(tmp, ".githooks/commit-msg", hook.replace("python ", '"%s" ' % _fwd(sys.executable)))
    # Linux runs a hook only when its file is executable; Windows ignores the bit (CI 7885274 on 4447e08 went red
    # with "it's not set as executable" while the case passed here) -- the FR-31 Linux-vs-Windows class.
    os.chmod(os.path.join(tmp, ".githooks", "commit-msg"), 0o755)
    _write_tmp(tmp, "CLAUDE.md", "# policy\n")
    try:
        for step in (["init", "-q"], ["add", "CLAUDE.md"]):
            subprocess.run(base + step, capture_output=True, env=env, timeout=PER_CASE_TIMEOUT_SECONDS, check=True)
        proc = subprocess.run(base + ["-c", "core.hooksPath=" + _fwd(os.path.join(tmp, ".githooks")), "commit", "-q", "-m",
                                      "touch the policy, no axis block"],
                              capture_output=True, env=env, timeout=PER_CASE_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as exc:
        return {"hung": True, "stdout": (exc.stdout or b"").decode("utf-8", errors="replace"),
                "stderr": (exc.stderr or b"").decode("utf-8", errors="replace")}
    except (OSError, subprocess.CalledProcessError) as exc:
        return {"returncode": 99, "stdout": "", "stderr": "probe could not set up the temp repo: %r" % (exc,)}
    return {"returncode": proc.returncode, "stdout": proc.stdout.decode("utf-8", errors="replace"),
            "stderr": proc.stderr.decode("utf-8", errors="replace")}


_HANDOFF_AGENT_ID = "liveness-probe-handoff-w1"


def _handoff_gate_tree(label: str, session_id: str, target_name: str) -> dict:
    """tools/handoff_gate.py (forge/5 F5-1 N3): a critic-kind worker fabricated in the case's OWN temp tree
    (a main-session file, the worker's transcript with its dispatch as the first user line, and the sidecar
    meta {"agentType": "critic"}) -- the live dispatch files are never read. The dispatch names ONE handoff path
    inside docs/tasks/specs/reviews; the payload writes `target_name` ("handoff" = that path, else another
    file of the tree). The hook writes nothing, so a clean exit 0 leaves the fixture files as they were."""
    tmp = _mkdtemp(label)
    handoff = _fwd(os.path.join(tmp, "docs", "tasks", "specs", "reviews", "t-999-probe-review.md"))
    other = _fwd(os.path.join(tmp, "tools", "some_other_file.py"))
    main = Path(tmp) / "proj" / "sess.jsonl"
    sub = Path(tmp) / "proj" / "sess" / "subagents"
    sub.mkdir(parents=True, exist_ok=True)
    main.write_text("", encoding="utf-8")
    dispatch = ("Review the probe diff.\n"
                "given: the probe fixture\n"
                "non-goals: none\n"
                f"handoff: {handoff}\n"
                "edges: none -- a probe fixture\n"
                "DoD: `python -m pytest -q`\n")
    worker = sub / f"agent-{_HANDOFF_AGENT_ID}.jsonl"
    worker.write_text(json.dumps({"type": "user", "message": {"role": "user", "content": dispatch}}) + "\n",
                      encoding="utf-8")
    (sub / f"agent-{_HANDOFF_AGENT_ID}.meta.json").write_text(json.dumps({"agentType": "critic"}), encoding="utf-8")
    fixture_files = sorted(str(p) for p in Path(tmp).rglob("*") if p.is_file())
    payload = {
        "tool_name": "Write",
        "cwd": tmp,
        "session_id": session_id,
        "agent_id": _HANDOFF_AGENT_ID,
        "transcript_path": _fwd(str(main)),
        "tool_input": {"file_path": handoff if target_name == "handoff" else other, "content": "probe"},
    }
    return {"payload": payload, "env": None,
            "extra": {"tmp": tmp, "handoff_path": handoff, "fixture_files": fixture_files}}


def _case_16_handoff_gate_refuses_other_path():
    return _handoff_gate_tree("handoff-gate-refuse", "liveness-probe-handoff-16", "other")


def _case_16a_handoff_gate_passes_own_path():
    """The control of case 16: the same worker and dispatch, the file_path is the dispatch's handoff path."""
    return _handoff_gate_tree("handoff-gate-pass", "liveness-probe-handoff-16a", "handoff")


# --- artifact checkers ------------------------------------------------


def _check_claim_marker(extra: dict) -> tuple:
    """The in-process road's own fingerprint: the claim file the gate's call of the reader created. A missing
    file means the reader never ran under the gate (a stale registry row or snapshot from elsewhere cannot
    fake it: the claim is keyed by this case's own tool_use_id)."""
    claim = extra["claim_path"]
    if not os.path.isfile(claim):
        return False, f"claim file {claim} does not exist -- the gate's in-process call did not run the reader"
    return True, f"claim file {os.path.basename(claim)} present"


def _check_owns_registry_artifact(extra: dict) -> tuple:
    tmp = extra["tmp"]
    owns_path = extra["owns_path"]
    registry_path = Path(tmp) / "logs" / "owns_registry.jsonl"
    if not registry_path.exists():
        return False, f"{registry_path} does not exist"
    lines = [ln for ln in registry_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        return False, f"{registry_path} is empty"
    try:
        last = json.loads(lines[-1])
    except Exception as exc:
        return False, f"last registry line is not valid JSON: {exc}"
    owns_gate_mod = _GATE_MODULES.get("owns_gate")
    owns_list = last.get("owns") or []
    if owns_gate_mod is not None:
        match = any(owns_gate_mod.normalize_path(p) == owns_gate_mod.normalize_path(owns_path)
                    for p in owns_list)
    else:
        match = owns_path in owns_list
    if not match:
        return False, f"registered owns {owns_list!r} does not include {owns_path!r}"
    claimed, claim_detail = _check_claim_marker(extra)
    if not claimed:
        return False, claim_detail
    return True, f"registered: {owns_list!r}; {claim_detail}"


def _check_search_ledger_artifact(extra: dict) -> tuple:
    ledger_dir = extra["ledger_dir"]
    session_id = extra["session_id"]
    candidates = [
        Path(ledger_dir) / f"{session_id}.jsonl",
        Path(ledger_dir) / "unknown.jsonl",
    ]
    for path in candidates:
        if path.exists() and path.read_text(encoding="utf-8").strip():
            return True, f"{path} non-empty"
    return False, f"no non-empty ledger file among {candidates}"


def _check_dod_gate_artifact(extra: dict) -> tuple:
    track_path = Path(extra["track_path"])
    if not track_path.exists():
        return False, f"{track_path} does not exist"
    try:
        data = json.loads(track_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"track file is not valid JSON: {exc}"
    gate_log = data.get("gate_log") or []
    if not gate_log or gate_log[-1].get("action") != "blocked":
        return False, f"gate_log tail is not a 'blocked' entry: {gate_log!r}"
    return True, f"gate_log tail: {gate_log[-1]!r}"


def _check_main_gate_artifact(extra: dict) -> tuple:
    track_path = Path(extra["track_path"])
    if not track_path.exists():
        return False, f"{track_path} does not exist"
    try:
        data = json.loads(track_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"track file is not valid JSON: {exc}"
    consecutive = (data.get("main_gate_state") or {}).get("consecutive_blocks")
    if consecutive != 1:
        return False, f"main_gate_state.consecutive_blocks = {consecutive!r}, expected 1"
    return True, "main_gate_state.consecutive_blocks == 1"


def _check_dod_track_artifact(extra: dict) -> tuple:
    track_path = Path(extra["track_path"])
    if not track_path.exists():
        return False, f"{track_path} does not exist"
    try:
        data = json.loads(track_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"track file is not valid JSON: {exc}"
    edits = data.get("edits") or []
    if not edits:
        return False, "edits list is empty"
    first = edits[0]
    if first.get("tool_name") != "Edit" or first.get("file_path") != extra["file_path"]:
        return False, f"unexpected edits[0]: {first!r}"
    return True, f"edits[0]: {first!r}"


def _check_critic_snapshot_artifact(extra: dict) -> tuple:
    snap_path = Path(extra["snap_path"])
    if not snap_path.exists():
        return False, f"{snap_path} does not exist"
    try:
        data = json.loads(snap_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return False, f"snapshot is not valid JSON: {exc}"
    if "error" in data:
        return False, f"snapshot is a FAILURE document: {data!r}"
    if not isinstance(data.get("tree_hash"), str) or not data["tree_hash"]:
        return False, f"tree_hash missing/empty: {data!r}"
    if not isinstance(data.get("files_count"), int):
        return False, f"files_count missing/not int: {data!r}"
    claimed, claim_detail = _check_claim_marker(extra)
    if not claimed:
        return False, claim_detail
    return True, f"tree_hash={data['tree_hash'][:12]}... files_count={data['files_count']}; {claim_detail}"


def _check_handoff_gate_wrote_nothing(extra: dict) -> tuple:
    """The control's artifact: the pass is silent by design, so the trail is the tree itself -- the handoff
    file was not created and no file appeared or went (the hook writes nothing)."""
    if os.path.exists(extra["handoff_path"]):
        return False, f"{extra['handoff_path']} exists -- the hook (or something) wrote the report file"
    now = sorted(str(p) for p in Path(extra["tmp"]).rglob("*") if p.is_file())
    if now != extra["fixture_files"]:
        return False, f"files of the tree changed: before {extra['fixture_files']!r}, after {now!r}"
    return True, f"tree unchanged ({len(now)} fixture files), no report file written"


def _check_compact_snapshot_artifact(extra: dict) -> tuple:
    snap_dir = Path(extra["snap_dir"])
    files = sorted(snap_dir.glob("*-manual.md")) if snap_dir.is_dir() else []
    if len(files) != 1:
        return False, f"expected exactly one *-manual.md under {snap_dir}, found {[f.name for f in files]!r}"
    text = files[0].read_text(encoding="utf-8", errors="replace")
    for marker in ("# Compact snapshot -- manual", "## 3. OPEN DISPATCHES", "## 6. Reminder"):
        if marker not in text:
            return False, f"{files[0].name} lacks {marker!r}"
    return True, f"{files[0].name}: {len(text)} chars, header + dispatches + reminder present"


# --- CASES table ------------------------------------------------------
# Anchors below quote each gate's ACTUAL message constant, read from its
# own source in this kit (see module docstring, "ADAPTATION OF
# COMPOSITION") -- several differ in wording/language from a source
# deployment's equivalents; that is expected, not a porting error.

CASES = [
    {
        "name": "0-agent_budget-worker-stop",
        "script": "tools/agent_budget.py",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_0_agent_budget_worker_stop,
        "expected_exit": 2,
        "anchors": ("AGENT BUDGET STOP",),
    },
    {
        "name": "1-dispatch_gate-block-no-dod",
        "script": "tools/dispatch_gate.py",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_1_dispatch_gate,
        "expected_exit": 2,
        # B-201: the refusal text now comes from dispatch_manifest.
        "anchors": ("DISPATCH INCOMPLETE (CLAUDE.md rule 11)",),
        "const_ref": ("dispatch_manifest", "INCOMPLETE_TEMPLATE"),
    },
    {
        "name": "2-dispatch_gate-in-process-owns-registration",
        "script": "tools/dispatch_gate.py",
        "kind": "artifact",
        "isolation": "subprocess",
        "build": _case_2_owns_gate_artifact,
        "expected_exit": 0,
        "artifact_check": _check_owns_registry_artifact,
    },
    {
        "name": "2a-dispatch_gate-in-process-owns-overlap-warn",
        "script": "tools/dispatch_gate.py",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_2a_owns_gate_overlap,
        "expected_exit": 0,
        "anchors": ("OWNS OVERLAP (warn):",),
    },
    {
        "name": "3-claim_control_gate-negative-claim-warn",
        "script": "tools/claim_control_gate.py",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_3_claim_control_gate,
        "expected_exit": 0,
        "anchors": (
            "Negative claim about to be written without a matching "
            "search/read this session",
            "(command hygiene point 6)",
        ),
        "const_ref": ("claim_control_gate", "MSG_TEMPLATE"),
    },
    {
        "name": "4-search_control_gate-empty-search-warn",
        "script": "tools/search_control_gate.py",
        "kind": "response+artifact",
        "isolation": "subprocess",
        "build": _case_4_search_control_gate,
        "expected_exit": 0,
        "anchors": ("Search returned nothing.",),
        "const_ref": ("search_control_gate", "MSG"),
        "artifact_check": _check_search_ledger_artifact,
    },
    {
        "name": "5-negative_lint-warn",
        "script": "tools/negative_lint.py",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_5_negative_lint,
        "expected_exit": 0,
        "anchors": ("NEGATIVE LINT:",),
        "const_ref": ("negative_lint", "WARN_PREFIX_TEMPLATE"),
    },
    {
        "name": "6-dod_gate-block",
        "script": "tools/dod_gate.py",
        "kind": "response+artifact",
        "isolation": "subprocess",
        "build": _case_6_dod_gate,
        "expected_exit": 2,
        "anchors": ("Stop blocked: there is no green verification run after the last edit.",),
        "const_ref": ("dod_gate", "BLOCK_MESSAGE"),
        "artifact_check": _check_dod_gate_artifact,
    },
    {
        "name": "7-main_gate-block",
        "script": "tools/main_gate.py",
        "kind": "response+artifact",
        "isolation": "subprocess",
        "build": _case_7_main_gate,
        "expected_exit": 2,
        "anchors": (
            "Stop blocked: there is no green verification run after the "
            "coordinator's last edit.",
        ),
        "const_ref": ("main_gate", "BLOCK_MESSAGE"),
        "artifact_check": _check_main_gate_artifact,
    },
    {
        "name": "8-journal_echo-broken-json",
        "script": "tools/journal_echo.py",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_8_journal_echo,
        "expected_exit": 0,
        "anchors": ("JOURNAL ECHO:",),
    },
    {
        "name": "8b-journal_echo-developer-file",
        "script": "tools/journal_echo.py",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_8b_journal_echo_developer_file,
        "expected_exit": 0,
        "anchors": ("JOURNAL ECHO:",),
    },
    {
        "name": "9-dod_track-artifact-silent",
        "script": "tools/dod_track.py",
        "kind": "artifact",
        "isolation": "subprocess",
        "build": _case_9_dod_track,
        "expected_exit": 0,
        "artifact_check": _check_dod_track_artifact,
    },
    {
        "name": "10-dispatch_gate-in-process-critic-snapshot",
        "script": "tools/dispatch_gate.py",
        "kind": "artifact",
        "isolation": "subprocess",
        "build": _case_10_critic_snapshot,
        "expected_exit": 0,
        "artifact_check": _check_critic_snapshot_artifact,
    },
    {
        "name": "11-hygiene_gate-journal-bypass-deny",
        "script": "tools/hygiene_gate.py",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_11_hygiene_gate,
        "expected_exit": 0,
        "anchors": (
            "the journal is written only via Edit/Write (command hygiene "
            "point 5); shell write to the journal blocked",
            '"permissionDecision": "deny"',
        ),
        "const_ref": ("hygiene_gate", "MSG_JOURNAL_BLOCK"),
    },
    {
        "name": "12-session_context-import-only",
        "script": "tools/session_context.py",
        "kind": "response",
        "isolation": "import",
        "build": _case_12_session_context,
        "expected_exit": None,
    },
    {
        "name": "13-compact_snapshot-writes-snapshot",
        "script": "tools/compact_snapshot.py",
        "kind": "response+artifact",
        "isolation": "subprocess",
        "build": _case_13_compact_snapshot,
        "expected_exit": 0,
        "anchors": ("COMPACT SNAPSHOT: docs/tasks/compact-snapshots/",),
        "artifact_check": _check_compact_snapshot_artifact,
    },
    # The two cases below are about GIT hooks (.githooks/commit-msg), not Claude hooks: "wiring": "githooks" keeps them
    # out of the settings.json composition sverka (they would be STALE-CASE there by construction).
    {
        "name": "14-piles_check-refuses-broken-tree",
        "script": "tools/piles.py",
        "wiring": "githooks",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_14_piles_check_refuses_broken_tree,
        "expected_exit": 2,
        "anchors": ("(а) placement: RED", "B-135", "piles check: refused -- red: (а)"),
    },
    {
        "name": "15-commit_msg_hook-piles-line-keeps-mechanism_gate-refusal",
        "script": "tools/mechanism_gate.py",
        "wiring": "githooks",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_15_commit_msg_hook_keeps_mechanism_refusal,
        "runner": _run_commit_msg_hook_case,
        "expected_exit": 1,
        "anchors": ("mechanism_gate:",),
    },
    # forge/5 F5-1 N3 (t-761): the PreToolUse Edit|Write hook tools/handoff_gate.py, a refusal and its control. The control
    # is what keeps the refusal honest: a hook that refused everything would pass case 16 and fail 16a (exit 2 != 0).
    {
        "name": "16-handoff_gate-refuses-a-non-handoff-path",
        "script": "tools/handoff_gate.py",
        "kind": "response",
        "isolation": "subprocess",
        "build": _case_16_handoff_gate_refuses_other_path,
        "expected_exit": 2,
        "anchors": ("HANDOFF GATE",),
        "const_ref": ("handoff_gate", "REFUSAL_TEMPLATE"),
    },
    {
        "name": "16a-handoff_gate-passes-its-own-handoff-path",
        "script": "tools/handoff_gate.py",
        "kind": "artifact",
        "isolation": "subprocess",
        "build": _case_16a_handoff_gate_passes_own_path,
        "expected_exit": 0,
        "artifact_check": _check_handoff_gate_wrote_nothing,
    },
]


# --- per-case execution -------------------------------------------------


def run_case(case: dict) -> dict:
    built = case["build"]()
    payload = built["payload"]
    env = built.get("env")
    extra = built.get("extra") or {}

    finding = ""
    const_ref = case.get("const_ref")
    if const_ref:
        finding = _verify_const(*const_ref)

    if case["isolation"] == "import":
        verdict, detail = _run_import_case(case, extra)
    else:
        runner = case.get("runner")
        result = runner(built) if runner else run_subprocess_case(case["script"], payload, env, args=built.get("args"))
        kind = case["kind"]
        expected_exit = case.get("expected_exit")
        anchors = case.get("anchors", ())
        if kind == "response":
            verdict, detail = check_response(result, expected_exit, anchors)
        elif kind == "artifact":
            artifact_check = case["artifact_check"]
            artifact_ok, artifact_detail = artifact_check(extra)
            verdict, detail = check_artifact_only(result, expected_exit, artifact_ok, artifact_detail)
        elif kind == "response+artifact":
            artifact_check = case["artifact_check"]
            artifact_ok, artifact_detail = artifact_check(extra)
            verdict, detail = check_response_and_artifact(
                result, expected_exit, anchors, (), artifact_ok, artifact_detail)
        else:
            verdict, detail = MISMATCH, f"unknown case kind: {kind!r}"

    if finding and verdict == OK:
        verdict = MISMATCH
    if finding:
        detail = f"{detail} | const-check: {finding}" if detail else f"const-check: {finding}"

    return {
        "name": case["name"],
        "script": case["script"],
        "verdict": verdict,
        "detail": format_excerpt(detail),
        "tmp": extra.get("tmp"),
    }


def _run_import_case(case: dict, extra: dict) -> tuple:
    """Case 12 (session_context): import-only branch -- build_context_lines(
    root=<tmp outside this kit's own tree>) is called directly, never via
    subprocess (the gate writes into the LIVE tree unconditionally when
    run as a subprocess, regardless of payload -- see
    tools/session_context.py itself)."""
    mod = _GATE_MODULES.get("session_context")
    if mod is None:
        return MISSING, "session_context module not importable"
    try:
        lines = mod.build_context_lines(root=Path(extra["tmp"]))
    except Exception as exc:
        if _looks_like_traceback(repr(exc)):
            return CRASH, repr(exc)
        return CRASH, f"{type(exc).__name__}: {exc}"
    if not lines:
        return DEAD, "build_context_lines() returned no lines at all"
    first = lines[0]
    if not (isinstance(first, str) and first.startswith("NOW: ")
            and first.endswith("(local system clock)")):
        return MISMATCH, f"unexpected first line: {first!r}"
    return OK, f"first line: {first!r}"


# --- composition sverka ---------------------------------------------------


def check_composition(settings_path: str = None):
    """Returns (settings_unreadable: bool, case_missing: list, stale_case:
    list, info_lines: list) -- see module docstring, "VERDICTS".
    *settings_path* defaults to the live SETTINGS_PATH; an explicit
    value lets tests point this at a fixture settings.json under a
    temporary tree WITHOUT touching the live file (see
    tools/test_hook_liveness_probe.py's three-world composition test).

    The two IN_PROCESS_TRACE_SCRIPTS have no case of their own (t-802: their traces are proved through
    tools/dispatch_gate.py's cases 2, 2a, 10), so listing one in settings.json is never CASE-MISSING --
    it is the DOUBLE-RUN finding of check_in_process_wiring()."""
    pairs = load_settings_hook_commands(settings_path or SETTINGS_PATH)
    if pairs is None:
        return True, [], [], []
    settings_scripts, info_lines = classify_settings_commands(pairs)
    case_scripts = {c["script"] for c in CASES if c.get("wiring") != "githooks"}   # a git-hook case is not in settings.json
    case_missing = sorted(settings_scripts - case_scripts - set(IN_PROCESS_TRACE_SCRIPTS))
    stale_case = sorted(case_scripts - settings_scripts)
    return False, case_missing, stale_case, info_lines


def _matcher_covers_dispatch(matcher) -> bool:
    """True when a PreToolUse matcher string is a regex alternation naming every one of
    GATE_MATCHER_ALTERNATIVES ("Task|Agent"; "Task|Agent|Foo" too). A bare "Task" or "" does not."""
    if not isinstance(matcher, str):
        return False
    names = {part.strip() for part in matcher.split("|")}
    return all(name in names for name in GATE_MATCHER_ALTERNATIVES)


def check_in_process_wiring(settings_path: str = None):
    """Returns (double_run: list, gate_matcher_ok: bool) -- the one-process shape of the Task|Agent trace
    writers (t-802):
    - double_run: the IN_PROCESS_TRACE_SCRIPTS still listed as hook commands in settings.json (any event; the
      stale world where the gate runs the readers AND the harness runs them again);
    - gate_matcher_ok: tools/dispatch_gate.py is listed under a PreToolUse entry whose matcher covers Task AND
      Agent -- without it the in-process road never runs at all (a silent loss of both traces).
    An unreadable settings.json gives ([], True): SETTINGS-UNREADABLE already fails the run on its own."""
    pairs = load_settings_hook_commands(settings_path or SETTINGS_PATH)
    if pairs is None:
        return [], True
    listed, _info = classify_settings_commands(pairs)
    double_run = sorted(set(IN_PROCESS_TRACE_SCRIPTS) & listed)
    text = _read_text_best_effort(settings_path or SETTINGS_PATH)
    try:
        entries = json.loads(text)["hooks"].get("PreToolUse", []) if text else []
    except Exception:
        entries = []
    gate_matcher_ok = False
    for entry in entries if isinstance(entries, list) else []:
        if not isinstance(entry, dict) or not _matcher_covers_dispatch(entry.get("matcher")):
            continue
        commands = [h.get("command", "") for h in entry.get("hooks", []) or [] if isinstance(h, dict)]
        scripts, _info = classify_settings_commands([("PreToolUse", c) for c in commands if isinstance(c, str)])
        if GATE_SCRIPT in scripts:
            gate_matcher_ok = True
    return double_run, gate_matcher_ok


# --- top-level orchestration -----------------------------------------------


def run_all(settings_path: str = None, post_merge: bool = None) -> dict:
    post_merge = POST_MERGE_DEFAULT if post_merge is None else post_merge
    if not CASES:
        return {
            "no_cases": True,
            "settings_unreadable": False,
            "case_missing": [], "stale_case": [], "info_lines": [],
            "double_run": [], "gate_matcher_ok": True, "post_merge": post_merge,
            "results": [], "live_state_diff": [], "import_findings": IMPORT_FINDINGS,
        }

    settings_unreadable, case_missing, stale_case, info_lines = check_composition(settings_path)
    double_run, gate_matcher_ok = check_in_process_wiring(settings_path)

    before = snapshot_live_state()
    results = [run_case(c) for c in CASES]
    after = snapshot_live_state()
    live_state_diff = diff_live_state(before, after)

    return {
        "no_cases": False,
        "settings_unreadable": settings_unreadable,
        "case_missing": case_missing,
        "stale_case": stale_case,
        "info_lines": info_lines,
        "double_run": double_run,
        "gate_matcher_ok": gate_matcher_ok,
        "post_merge": post_merge,
        "results": results,
        "live_state_diff": live_state_diff,
        "import_findings": IMPORT_FINDINGS,
    }


def overall_ok(report: dict) -> bool:
    if report.get("no_cases"):
        return False
    if report["settings_unreadable"]:
        return False
    if report["case_missing"] or report["stale_case"]:
        return False
    if not report.get("gate_matcher_ok", True):
        return False
    if report.get("post_merge") and report.get("double_run"):
        return False
    if report["live_state_diff"]:
        return False
    return all(r["verdict"] == OK for r in report["results"])


def _cleanup_temp_dirs(report: dict) -> None:
    for r in report.get("results", []):
        tmp = r.get("tmp")
        if tmp and os.path.isdir(tmp):
            shutil.rmtree(tmp, ignore_errors=True)


def format_human_report(report: dict) -> str:
    lines = []
    if report.get("no_cases"):
        lines.append("NO-CASES: CASES table is empty -- probe defect, nothing ran.")
        return "\n".join(lines)

    if report["settings_unreadable"]:
        lines.append(f"SETTINGS-UNREADABLE: {SETTINGS_PATH}")

    for msg in report["case_missing"]:
        lines.append(f"CASE-MISSING: {msg} (hook registered, no matching probe case)")
    for msg in report["stale_case"]:
        lines.append(f"STALE-CASE: {msg} (probe case, no matching hook registration)")
    for script in report.get("double_run", []):
        if report.get("post_merge"):
            lines.append(f"{DOUBLE_RUN}: {script} is still listed in settings.json next to dispatch_gate.py -- "
                         "the gate runs it in-process (t-796); delete the entry (FAIL under --post-merge)")
        else:
            lines.append(f"{DOUBLE_RUN} (warn): {script} is still listed in settings.json next to "
                         "dispatch_gate.py -- delete the entry at the merge; --post-merge turns this into a FAIL")
    if not report.get("gate_matcher_ok", True):
        lines.append(f"{GATE_MATCHER}: {GATE_SCRIPT} is not listed under a PreToolUse matcher that covers "
                     f"{'|'.join(GATE_MATCHER_ALTERNATIVES)} -- the in-process trace road never runs")
    for msg in report["info_lines"]:
        lines.append(f"INFO: {msg}")
    for msg in report["import_findings"]:
        lines.append(f"FINDING: {msg}")

    for r in report["results"]:
        lines.append(f"[{r['verdict']}] {r['name']} ({r['script']}) -- {r['detail']}")

    for path in report["live_state_diff"]:
        lines.append(f"LIVE-STATE-TOUCHED: {path}")

    total = len(report["results"])
    ok_count = sum(1 for r in report["results"] if r["verdict"] == OK)
    dead_count = sum(1 for r in report["results"] if r["verdict"] == DEAD)
    silence_word = "no silences" if dead_count == 0 else f"{dead_count} silence(s)"
    lines.append(f"{ok_count}/{total} alive, {silence_word}")
    lines.append("SCOPE: code liveness only, not wiring liveness (see module docstring).")
    lines.append("OVERALL: " + (OK if overall_ok(report) else "NOT-OK"))
    return "\n".join(lines)


def main(argv=None) -> int:
    streams.utf8_stdio()
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--post-merge", action="store_true",
                        help="t-802: a settings.json that still lists tools/critic_snapshot.py or tools/owns_gate.py "
                             "(run in-process by dispatch_gate.py) FAILS the run instead of printing a DOUBLE-RUN warn")
    parser.add_argument("--settings", default=None,
                        help="read this settings.json instead of the kit's .claude/settings.json "
                             "(a temp copy for a what-if; the file is only read)")
    args = parser.parse_args(argv)

    report = run_all(settings_path=args.settings, post_merge=True if args.post_merge else None)
    try:
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
        else:
            print(format_human_report(report))
    finally:
        _cleanup_temp_dirs(report)

    return 0 if overall_ok(report) else 1


if __name__ == "__main__":
    sys.exit(main())
