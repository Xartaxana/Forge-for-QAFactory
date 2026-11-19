#!/usr/bin/env python3
"""The journal hooks (offload spec r2, §3.B23): the dispatch record, the end-of-dispatch record, the by-hand-edit gate.

    python -B tools/journal_hooks.py post-agent   PostToolUse Task|Agent  -> `delegated` (+ `returned` when a stop came first)
    python -B tools/journal_hooks.py post-send    PostToolUse SendMessage -> `resumed` (a stopped worker of this session gets a new round)
    python -B tools/journal_hooks.py pre-edit     PreToolUse  Edit|Write  -> a journal file edited by hand: WARN (or deny)
    journal_hooks.record_returned(payload)        called by tools/dod_gate.py on every exit-0 decision of a SubagentStop

Every line goes through the ONE writer (`journal_write.write_event(..., via="hook", lock_timeout=5)`): the machine lock, the
validator and the counter are its; this module reads the payloads and decides WHAT to write. A hook never blocks a tool by
error: exit 0 always (the deny of `pre-edit` in "refuse" mode is an answer on stdout, exit 0 too), and a launched dispatch
is never left unrecorded SILENTLY -- every road that does not write says so in one line carrying the door
(`python -B tools/journal_write.py delegated ...`).

The two stores that join a stop to its launch live in `<git common dir>/forge-journal/`: `open/<agent_id>` (the absolute
path of the journal copy that holds the `delegated`; written with it) and `pending-returns/<agent_id>` (a stop that found
no `delegated` yet; consumed by `post-agent`). Markers older than 24 h and index entries older than 7 days are pruned by the
next hook call, each prune a WARN line (calibration check 48). The stop side runs inside dod_gate, whose stderr on exit 0
reaches no reader: its WARN lines are ALSO appended to `<common>/forge-journal/warn.log` (check 48(c) reads it), and a
refused `returned` leaves its pending marker, which the next `post-agent` for that agent retries.

This file is a mechanism-chain link; its stdout is set by the one helper tools/streams.py (itself a link)."""
from __future__ import annotations

import json
import os
import re
import sys
import threading
import time
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import streams  # noqa: E402 -- the one helper (axis 15; streams.py is a link of the chain since B23)
import tier_ladder  # noqa: E402 -- the ladder home (a leaf): the family words of the door text

JOURNAL_EDIT_MODE = "warn"          # "warn" (shipped) | "refuse" (node B23-S): the ONE constant that decides (E-B23-13)
HOOK_LOCK_TIMEOUT = 5               # seconds: a hook never waits longer
NOTES_MAX = 300                     # COORDINATOR.md rule 12 (the CLI refuses longer notes; the hook cuts)
LINE_MAX = 700                      # one hook line is cut here, whatever a validator text says
SCAN_LINES = 3000                   # the tail of a journal copy read to find a delegated (X-8)
PENDING_MAX_AGE = 24 * 3600         # seconds
INDEX_MAX_AGE = 7 * 24 * 3600
OPEN_DIR, PENDING_DIR = "open", "pending-returns"
WRITER = "python -B tools/journal_write.py"
DELEGATED_DOOR = f"write it: {WRITER} delegated …"
EDIT_DOOR = (f"the writer is {WRITER} <event> … (event --json for a retro line)")
WARN_LOG = "warn.log"               # <common>/forge-journal/warn.log: the stop-side WARN lines, read by calibration check 48(c)
SESSION_RE = re.compile(r"^[A-Za-z0-9-]{1,16}$")


# ---------------------------------------------------------------- small helpers

def one_line(text, limit: int = LINE_MAX) -> str:
    """`text` on one line (every whitespace run a space), at most `limit` characters (the last one `…` when cut)."""
    flat = re.sub(r"\s+", " ", str(text)).strip()
    return flat if len(flat) <= limit else flat[:limit - 1] + "…"


def cut_notes(text, suffix: str = "") -> str:
    """The description as hook notes: `text` + `suffix` in at most NOTES_MAX characters; the TEXT is cut (its last
    character `…`), the suffix (a `replaces_worker:<ref>` token) is kept whole."""
    flat = re.sub(r"\s+", " ", text if isinstance(text, str) else "").strip()
    room = max(1, NOTES_MAX - (len(suffix) + 1 if suffix else 0))
    if len(flat) > room:
        flat = flat[:room - 1] + "…"
    return f"{flat} {suffix}".strip() if suffix else flat


def _door(reason) -> str:
    return f"JOURNAL: delegated NOT written -- {one_line(reason, 500)}; {DELEGATED_DOOR}"


def _imports():
    """(journal_write, journal_lock, journal_keys, transcripts) -- lazy: a broken helper is a door line, not a crash."""
    import journal_keys
    import journal_lock
    import journal_write
    import transcripts
    return journal_write, journal_lock, journal_keys, transcripts


def _forge_dir(root, sub: str) -> Path:
    import journal_lock
    path = journal_lock.lock_dir(root) / sub
    path.mkdir(parents=True, exist_ok=True)
    return path


def _tail_objs(path: Path, lines: int = SCAN_LINES) -> list:
    try:
        text = path.read_bytes().decode("utf-8", errors="replace")
    except OSError:
        return []
    import journal_write
    return journal_write._objs(text.splitlines()[-lines:])       # the ONE line parser (critic F7)


def _journal_file(root) -> Path | None:
    import journal_keys
    rel, _why = journal_keys.current_path(Path(root))
    return Path(root) / rel if rel else None


def _root_of_journal(path: Path) -> Path | None:
    """The repository folder a journal file lives in (`<root>/logs/journal/<dev>.jsonl` or `<root>/logs/routing-log.jsonl`)."""
    if path.parent.name == "journal" and path.parent.parent.name == "logs":
        return path.parents[2]
    if path.parent.name == "logs":
        return path.parents[1]
    return None


def _find_delegated(objs: list, ref: str):
    """(delegated object, returned?) for the LAST `delegated` with this worker_ref in `objs`; (None, False) when none."""
    found, done = None, False
    for obj in objs:
        if obj.get("worker_ref") != ref:
            continue
        if obj.get("event") == "delegated":
            found, done = obj, False
        elif obj.get("event") == "returned" and found is not None and obj.get("task_id") == found.get("task_id"):
            done = True
        elif obj.get("event") == "resumed" and found is not None and obj.get("task_id") == found.get("task_id"):
            done = False                # FG7-88: a resume opens a new round (the validator's _round_step rule)
    return found, done


# ---------------------------------------------------------------- the stores: open/ index, pending-returns/ markers

def prune(root, now: float | None = None) -> list:
    """Delete pending markers older than 24 h and index entries older than 7 days; one WARN line per prune."""
    now = time.time() if now is None else now
    lines = []
    for sub, age, template in ((PENDING_DIR, PENDING_MAX_AGE,
                                "JOURNAL: returned lost for agent:{id} (stop at {ts}, no delegated found in 24 h)"),
                               (OPEN_DIR, INDEX_MAX_AGE, "JOURNAL: open-dispatch index entry for agent:{id} pruned")):
        try:
            folder = _forge_dir(root, sub)
            entries = sorted(folder.iterdir())
        except Exception:  # noqa: BLE001
            continue
        for entry in entries:
            try:
                mtime = entry.stat().st_mtime
                if now - mtime <= age:
                    continue
                ts = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(mtime))
                entry.unlink()
                lines.append(template.format(id=entry.name, ts=ts))
            except OSError:
                continue
    return lines


def _write_index(root, agent_id: str, journal_path: Path) -> None:
    try:
        (_forge_dir(root, OPEN_DIR) / agent_id).write_text(str(journal_path), encoding="utf-8")
    except Exception:  # noqa: BLE001 -- the index is an accelerator: the scan finds the copy without it
        pass


def _drop(path: Path) -> None:
    try:
        path.unlink()
    except OSError:
        pass


# ---------------------------------------------------------------- post-agent: `delegated`

def _repeat_fields(objs: list, task: str, agent: str) -> dict:
    """The fields a REPEAT `delegated` needs, computed from the journal (the validator judges them): a task already
    delegated to this agent and rejected N >= 1 times is a retry -> attempt = N + 1; a first delegation, a critic entry
    (another agent) and a replacement (the `replaces_worker:` token in the notes) need none."""
    prior = [o for o in objs if o.get("event") == "delegated" and o.get("task_id") == task]
    if not prior or agent not in {o.get("agent") for o in prior}:
        return {}
    rejected = sum(1 for o in objs if o.get("event") == "rejected" and o.get("task_id") == task)
    return {"attempt": rejected + 1} if rejected >= 1 else {}


def _session(payload: dict):
    session = payload.get("session_id")
    short = session[:8] if isinstance(session, str) else ""
    return short if SESSION_RE.match(short) else None


def post_agent(payload) -> list:
    """The lines (for additionalContext) of one PostToolUse(Task|Agent) call; writes `delegated`, and `returned` after it
    when a stop came first. Never raises."""
    try:
        return _post_agent(payload)
    except Exception as exc:  # noqa: BLE001 -- the contract: a hook never raises
        return [_door(f"the hook failed ({type(exc).__name__})")]


def _post_agent(payload) -> list:
    if not isinstance(payload, dict):
        return [_door("the payload is not a JSON object")]
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return [_door("the payload has no tool_input")]
    jw, _jl, jk, transcripts = _imports()
    agent_id = transcripts.launch_agent_id(payload.get("tool_response"))
    if agent_id is None:
        return [_door("the launch result carries no agent id")]
    import dispatch_gate
    import journal_validator
    agent = tool_input.get("subagent_type")
    if not isinstance(agent, str) or not agent.strip():
        return [_door("the dispatch names no subagent_type")]
    try:
        root = jw.repo_root(payload.get("cwd") or os.getcwd())
    except jw.Refused as exc:
        return [_door(exc.text)]
    # D-0016: the model is the ROLE's binding, never read from the label; an explicit Agent `model` parameter wins (F5).
    declared = tool_input.get("model")
    if isinstance(declared, str) and declared.strip():
        bound, road = declared.strip(), "the dispatch's model parameter"
    else:
        bound, road = dispatch_gate.role_bound_model(agent, journal_validator.read_config_text(root))
    if bound is None:
        return [_door(f"the dispatch's role '{agent.strip()}' has no bound model ({road}), and the hook writes no model it did not read")]
    model = tier_ladder.family_of(bound) or bound
    by_default = road.startswith("default bindings")
    prompt = tool_input.get("prompt") if isinstance(tool_input.get("prompt"), str) else ""
    ids, skip_reason = {}, None
    try:
        import dispatch_manifest
        _builder, cut = dispatch_manifest.cut_payload({"tool_input": tool_input})
        if cut is None:        # cut_payload's cheap exit (a scout / critic prompt with no `owns`/`handoff` word): the same ONE cut
            cut = dispatch_manifest.section_cut(prompt)
        ids = dispatch_manifest.header_ids(cut)
        skip_reason = dispatch_manifest.designer_skip_reason(cut)
    except Exception:  # noqa: BLE001 -- the ids are help: without them the writer issues a task id
        ids, skip_reason = {}, None
    ref = f"agent:{agent_id}"
    journal = _journal_file(root)
    if journal is None:
        return [_door("this repository has no journal file (journal_keys.current_path)")]
    lines = prune(root)
    objs = _tail_objs(journal, 10 ** 9)
    known, returned = _find_delegated(objs, ref)
    if known is not None:                                # E-B23-12: a completion event, a replay -- already recorded
        if not returned:                                 # a stop whose `returned` was refused left its marker (F2): retry it now
            lines.extend(_flush_pending(jw, root, journal, agent_id, known.get("task_id"), known.get("agent"), known.get("model")))
        return lines
    obj = {"event": "delegated", "agent": agent.strip(), "model": model, "worker_ref": ref,
           "category": jw._category(agent.strip())[0]}
    for key in ("feature", "node"):
        if ids.get(key):
            obj[key] = ids[key]
    session = _session(payload)
    if session:
        obj["session"] = session
    task = ids.get("task")
    if task:
        obj["task_id"] = task
        obj.update(_repeat_fields(objs, task, agent.strip()))
    replaces = journal_validator.extract_replaces_worker(prompt)
    obj["notes"] = cut_notes(tool_input.get("description"), f"replaces_worker:{replaces}" if replaces else "")
    res = jw.write_event(root, obj, via="hook", lock_timeout=HOOK_LOCK_TIMEOUT)
    if not res.written:
        return lines + [_door(" / ".join(res.messages) or "the writer refused")]
    path = root / res.path
    _write_index(root, agent_id, path)
    done = f"JOURNAL: delegated {res.task_id} written ({res.path}:{res.line_no})"
    if not task:
        done += f"; task id issued by the hook: {res.task_id} (the dispatch named none)"
    if by_default:
        done += "; model by default bindings (delegation.config.yaml absent or unreadable)"
    lines.append(done)
    lines.extend(one_line(m, 300) for m in res.messages[1:] if m)
    if skip_reason:
        lines.extend(_designer_skip(jw, root, journal, res.task_id, skip_reason, obj.get("feature")))
    lines.extend(_flush_pending(jw, root, path, agent_id, res.task_id, agent.strip(), model))
    return lines


def post_send(payload) -> list:
    """FG7-88: the lines of one PostToolUse(SendMessage) call. A send to a worker of THIS session whose round has ended (a
    `returned` since its last start, task not accepted) writes `resumed`; every other send is not a resume and owes nothing
    (`[]`, silent). Never raises."""
    to = "?"
    try:
        tool_input = payload.get("tool_input") if isinstance(payload, dict) else None
        to = tool_input.get("to") if isinstance(tool_input, dict) else None
        return _post_send(payload, to)
    except Exception as exc:  # noqa: BLE001 -- the contract: a hook never raises
        return [f"JOURNAL: resumed NOT checked for agent:{one_line(to, 60)} -- the hook failed ({type(exc).__name__})"]


def _post_send(payload, to) -> list:
    jw, _jl, jk, transcripts = _imports()
    if transcripts.agent_file_name(to) is None or "agent_id" in payload:
        return []                    # not an agent id (a peer pipe, junk), or a send made inside a worker (X3)
    try:
        root = jw.repo_root(payload.get("cwd") or os.getcwd())
    except jw.Refused:
        return []                    # no repository: no journal to hold a round
    ref = f"agent:{to}"
    state = _locate(jw, jk, root, to, ref)
    if state is None:
        return []
    copy, delegated, done = state
    session = _session(payload)
    if delegated.get("session") and session and delegated.get("session") != session:
        return []                    # F3 (b): another session's worker is not this session's round
    task = delegated.get("task_id")
    if not done or any(o.get("event") == "accepted" and o.get("task_id") == task for o in _tail_objs(copy)):
        return []                    # an open round: a course correction; a closed task: no round (E5, E6)
    obj = {"event": "resumed", "task_id": task, "agent": delegated.get("agent"), "worker_ref": ref,
           "category": delegated.get("category") or jw._category(delegated.get("agent"))[0],
           "notes": cut_notes(f"{ref} resumed by SendMessage")}
    if delegated.get("model"):
        obj["model"] = delegated["model"]
    if delegated.get("session"):
        obj["session"] = delegated["session"]
    target = _root_of_journal(copy) or root
    res = jw.write_event(target, obj, via="hook", lock_timeout=HOOK_LOCK_TIMEOUT)
    if not res.written:
        return [f"JOURNAL: resumed NOT written for {ref} -- {one_line(' / '.join(res.messages), 400)}; "
                f"write it: {WRITER} event --json '{one_line(json.dumps(obj), 300)}'"]
    _write_index(root, to, copy)
    return [f"JOURNAL: resumed {task} written ({res.path}:{res.line_no})"]


def _designer_skip(jw, root, journal: Path, task: str, reason: str, feature) -> list:
    """`dispatch_skipped` (agent=designer) for a `designer: skip -- <reason>` header, once per task id."""
    prefix = f"designer skip for {task}:"
    if any(o.get("event") == "dispatch_skipped" and str(o.get("notes", "")).startswith(prefix) for o in _tail_objs(journal, 10 ** 9)):
        return []
    obj = {"event": "dispatch_skipped", "agent": "designer", "category": "process", "notes": cut_notes(f"{prefix} {reason}")}
    if feature:
        obj["feature"] = feature
    res = jw.write_event(root, obj, via="hook", lock_timeout=HOOK_LOCK_TIMEOUT)
    return [] if res.written else [f"JOURNAL: designer skip NOT written -- {one_line(' / '.join(res.messages), 400)}; "
                                   f"{WRITER} skip --agent designer …"]


def _flush_pending(jw, root, journal_path: Path, agent_id: str, task: str, agent: str, model: str) -> list:
    """A stop that came BEFORE this launch (a foreground dispatch) left a marker: `returned` right after `delegated`."""
    try:
        marker = _forge_dir(root, PENDING_DIR) / agent_id
        if not marker.exists():
            return []
    except Exception:  # noqa: BLE001
        return []
    return _write_returned(jw, root, marker, agent_id, task, agent, model, journal_path)


def _write_returned(jw, root, marker, agent_id: str, task: str, agent: str, model, journal_path: Path) -> list:
    ref = f"agent:{agent_id}"
    obj = {"event": "returned", "task_id": task, "agent": agent, "worker_ref": ref,
           "notes": cut_notes(f"{ref} stopped and passed the stop gate")}
    if model:
        obj["model"] = model
    target = _root_of_journal(journal_path) or root
    res = jw.write_event(target, obj, via="hook", lock_timeout=HOOK_LOCK_TIMEOUT)
    if res.written:
        if marker is not None:
            _drop(marker)
        return [f"JOURNAL: returned {task} written ({res.path}:{res.line_no})"]
    if _find_delegated(_tail_objs(journal_path), ref)[1]:   # F4: a lost race -- the other writer's `returned` is there
        if marker is not None:
            _drop(marker)
        return []
    return [f"JOURNAL: returned NOT written for {ref} -- {one_line(' / '.join(res.messages), 400)}; "
            f"write it: {WRITER} returned --task {task} --worker {ref}"]


# ---------------------------------------------------------------- record_returned: called by dod_gate (SubagentStop, exit 0)

def record_returned(payload, now: float | None = None) -> list:
    """The end of a dispatch (BL-5, X-8): find the `delegated` of this SubagentStop's agent and write `returned` into the
    SAME journal copy; none found -> a pending marker for `post-agent`. Returns the lines to show (WARNs). Never raises."""
    root_box = []
    try:
        lines = _record_returned(payload, now, root_box)
    except Exception as exc:  # noqa: BLE001 -- dod_gate's decision never depends on it (F-B3-1 (a)); but never silent (F5)
        who = one_line(payload.get("agent_id"), 60) if isinstance(payload, dict) else "?"
        lines = [f"JOURNAL: returned NOT recorded for agent:{who} -- the hook failed ({type(exc).__name__})"]
    _warn_log(root_box[0] if root_box else _guess_root(payload), lines)
    return lines


def _guess_root(payload):
    try:
        import journal_write
        return journal_write.repo_root((payload.get("cwd") if isinstance(payload, dict) else None) or os.getcwd())
    except Exception:  # noqa: BLE001
        return None


def _warn_log(root, lines: list) -> None:
    """F2: the stop path runs inside dod_gate, whose stderr on exit 0 reaches nobody. Every WARN line (anything but a
    `written (` success) is also appended to <common>/forge-journal/warn.log, which calibration check 48(c) reads."""
    warns = [x for x in lines if " written (" not in x or "NOT written" in x]
    if not warns or root is None:
        return
    try:
        stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        with open(_forge_dir(root, "") / WARN_LOG, "a", encoding="utf-8") as handle:
            handle.write("".join(f"{stamp} {one_line(x)}\n" for x in warns))
    except Exception:  # noqa: BLE001 -- the log is a second channel, never a failure
        pass


def _any_journal(jw, jk, root) -> bool:
    """True when some worktree of this clone (the stop's own included) has a journal file name."""
    for tree in [root, *jw.worktrees_of(root)]:
        rel, _why = jk.current_path(Path(tree))
        if rel:
            return True
    return False


def _ensure_marker(root, agent_id: str) -> Path:
    marker = _forge_dir(root, PENDING_DIR) / agent_id
    try:
        fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(time.strftime("%Y-%m-%dT%H:%M:%S"))
    except FileExistsError:
        pass
    return marker


def _record_returned(payload, now, root_box) -> list:
    if not isinstance(payload, dict):
        return []
    agent_id = payload.get("agent_id")
    jw, jl, jk, transcripts = _imports()
    if not isinstance(agent_id, str) or not transcripts.AGENT_ID_RE.match(agent_id):
        return []
    try:
        root = jw.repo_root(payload.get("cwd") or os.getcwd())
    except jw.Refused:                                     # not inside a git repository: no journal to hold a `delegated`
        return []
    root_box.append(root)
    # F1: the stop's own cwd may be a linked worktree with no tools/dev.config.yaml (untracked: none has one). The index
    # and the markers live in the common dir, so the judgement is over EVERY worktree of the clone, after nothing else.
    if not _any_journal(jw, jk, root):                    # no tree of this clone has a journal: nothing to record, nothing to lose
        return []
    lines = prune(root, now)
    ref = f"agent:{agent_id}"
    state = _locate(jw, jk, root, agent_id, ref)
    if state is None:                                      # (3) no delegated yet: the marker; one re-look for the race window
        _ensure_marker(root, agent_id)
        state = _locate(jw, jk, root, agent_id, ref)
        if state is None:
            return lines
    copy, delegated, done = state
    if done:                                               # already returned: nothing (idempotent); the index entry is spent
        _drop(_forge_dir(root, OPEN_DIR) / agent_id)
        _drop(_forge_dir(root, PENDING_DIR) / agent_id)
        return lines
    out = _write_returned(jw, root, _forge_dir(root, PENDING_DIR) / agent_id, agent_id, delegated.get("task_id"),
                          delegated.get("agent"), delegated.get("model"), copy)
    if out and out[0].startswith("JOURNAL: returned") and "NOT written" not in out[0]:
        _drop(_forge_dir(root, OPEN_DIR) / agent_id)
    elif out:                                              # F2: refused -- keep a marker so the next post-agent retries it
        _ensure_marker(root, agent_id)
    return lines + out


def _locate(jw, jk, root, agent_id: str, ref: str):
    """(journal file, delegated object, returned?) of the copy holding this agent's `delegated`: (1) the index entry's
    path, (2) the last SCAN_LINES of every worktree's copy; None when no copy has one."""
    indexed = _forge_dir(root, OPEN_DIR) / agent_id
    if indexed.is_file():
        try:
            path = Path(indexed.read_text(encoding="utf-8").strip())
        except OSError:
            path = None
        if path is not None and path.is_file():
            found, done = _find_delegated(_tail_objs(path), ref)
            if found is not None:
                return path, found, done
    for tree in jw.worktrees_of(root):
        rel, _why = jk.current_path(tree)
        if not rel or not (tree / rel).is_file():
            continue
        found, done = _find_delegated(_tail_objs(tree / rel), ref)
        if found is not None:
            return tree / rel, found, done
    return None


# ---------------------------------------------------------------- pre-edit: the by-hand edit of a journal

def _file_path(payload):
    tool_input = payload.get("tool_input") if isinstance(payload, dict) else None
    path = tool_input.get("file_path") if isinstance(tool_input, dict) else None
    return path if isinstance(path, str) and path else None


def pre_edit(payload):
    """The hook answer (a dict for stdout) for a PreToolUse Edit|Write call, or None. A path that names a journal
    (`logs/journal/*.jsonl`, `logs/routing-log.jsonl` of ANY worktree, whatever the separators, `..` and case) is
    recognised by the ONE reader (journal_echo._journal_rel); the module constant JOURNAL_EDIT_MODE alone picks warn or deny."""
    path = _file_path(payload)
    lowered = path.lower() if path else ""
    if not path or ".jsonl" not in lowered or "logs" not in lowered:       # the cheap exit: most Edits are not journals
        return None
    import journal_echo
    if journal_echo._journal_rel(path) is None:
        return None
    if JOURNAL_EDIT_MODE == "refuse":
        text = f"JOURNAL: by-hand edit refused -- {EDIT_DOOR}"
        return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                       "permissionDecisionReason": text, "additionalContext": text}}
    text = f"JOURNAL: by-hand edit -- {EDIT_DOOR}; this becomes a refusal at node B23-S"
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": text}}


# ---------------------------------------------------------------- the entry

# --- stdin deadline (P4 class; a LOCAL copy, as in negative_lint.py / dod_gate.py: no shared module -- critic F3)

_STDIN_DEADLINE_DEFAULT = 10.0
_STDIN_DEADLINE_MAX = 600.0
_STDIN_DEADLINE_ENV = "OSLLM_STDIN_TIMEOUT"
_STDIN_DEADLINE_STATE = {"hit": False}      # the __main__ path escalates to os._exit when a reader thread is still blocked


def _stdin_deadline_seconds() -> float:
    """Env override, else the default; invalid, <= 0 or > max fall back to the default (no "wait forever" mode)."""
    try:
        value = float(os.environ.get(_STDIN_DEADLINE_ENV, ""))
    except (TypeError, ValueError):
        return _STDIN_DEADLINE_DEFAULT
    return value if 0.0 < value <= _STDIN_DEADLINE_MAX else _STDIN_DEADLINE_DEFAULT


def _read_stdin_bytes_deadline():
    """(bytes, timed_out): stdin to EOF, but no longer than the deadline (a daemon thread does the blocking read)."""
    stdin = getattr(sys, "stdin", None)
    if stdin is None:
        return b"", False
    try:
        if stdin.isatty():
            return b"", False
    except Exception:  # noqa: BLE001
        pass
    stream = getattr(stdin, "buffer", stdin)
    box = {}

    def _reader():
        try:
            box["data"] = stream.read()
        except Exception:  # noqa: BLE001
            box["data"] = b""

    thread = threading.Thread(target=_reader, name="stdin-deadline", daemon=True)
    thread.start()
    thread.join(_stdin_deadline_seconds())
    if thread.is_alive():
        return b"", True
    data = box.get("data") or b""
    return (data if isinstance(data, bytes) else str(data).encode("utf-8", "replace")), False


def _read_payload():
    """(payload or None, timed_out)."""
    raw, timed_out = _read_stdin_bytes_deadline()
    if timed_out:
        _STDIN_DEADLINE_STATE["hit"] = True
        return None, True
    try:
        return json.loads(raw.decode("utf-8", errors="replace")), False
    except (ValueError, RecursionError):
        return None, False


def main(argv=None) -> int:
    streams.utf8_stdio()
    args = sys.argv[1:] if argv is None else list(argv)
    mode = args[0] if args else ""
    try:
        payload, timed_out = _read_payload()
        if timed_out:           # post-agent says so with the door; pre-edit and post-send stay silent (they never block a tool)
            if mode == "post-agent":
                print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                         "additionalContext": _door("stdin deadline exceeded")}}))
            return 0
        if mode == "post-agent":
            lines = post_agent(payload)
            if lines:
                print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                         "additionalContext": " | ".join(lines)}}))
        elif mode == "post-send":
            lines = post_send(payload)
            if lines:
                print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                                         "additionalContext": " | ".join(lines)}}))
        elif mode == "pre-edit":
            answer = pre_edit(payload)
            if answer is not None:
                print(json.dumps(answer))
    except Exception:  # noqa: BLE001 -- a journal hook never blocks a tool by error
        pass
    return 0


if __name__ == "__main__":
    _rc = main()
    if _STDIN_DEADLINE_STATE["hit"]:        # a reader thread may still be blocked in a read syscall: exit without joining it
        for _stream in (sys.stdout, sys.stderr):
            try:
                _stream.flush()
            except Exception:  # noqa: BLE001
                pass
        os._exit(_rc)
    sys.exit(_rc)
