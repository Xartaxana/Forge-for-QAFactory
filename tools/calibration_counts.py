"""Counting script for the weekly calibration's field-completeness and
duplicate-task checks, plus the rejected/escalated pairing check. Takes
manual counting of journal counters off the reviewer's plate:
deterministically decidable work (counting, grouping, position in the
file) goes into code; VERDICTS (is this actually a violation, e.g. "the
thread was explicitly continued under a different task_id") stay with
the human reviewer. The script prints CANDIDATES, not verdicts.

Works with EITHER routing-journal formatting style:
  - compact JSON, no spaces after colons, task_id format t-NNN;
  - JSON WITH SPACES after colons, descriptive task_id strings (e.g.
    a slug like "at-bug-004").

Parsing is json.loads, line by line, ONLY (a lesson from an earlier
calibration run: grepping the spaced-JSON format gave a false empty
result because of the spaces after ':'; json.loads doesn't care about
whitespace). A line that fails to parse is a candidate violation in the
report, never a silent skip.

Exit code is always 0, except for IO/argument errors -- this script is
a measurement tool, not a gate (unlike tools/journal_validator.py,
which blocks the commit).

CLI:
    python tools/calibration_counts.py [--journal PATH [--journal PATH ...]] [--root DIR]
        [--window-start ISO] [--window-end ISO] [--by-since ISO] [--json]
Without --journal every journal file of the root is loaded through journal_keys.load_all (the history
logs/routing-log.jsonl and logs/journal/*.jsonl) and the text report opens with the list of the files read
and their event counts; --journal PATH is an explicit override (only those files, no list).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# B-402: the task key. Two clones issue the same t-NNN and merge=union joins their journals;
# tools/journal_keys.py keys an event by (label, task_id) through the declaration that sits beside
# the journal (logs/journal-segments.json). Sections 2 (escalation pairing) and 10 (unclosed tasks)
# are keyed; section 5 (repeated delegated) stays BARE on purpose: an id reused after an accepted
# is always a candidate. Without the module the script still runs, ANNOUNCED on stderr: every id
# reads bare and `closes:t-NNN@label` reads as `closes:t-NNN` (the pre-B-402 reading).
try:
    import journal_keys as _jk
except ImportError as _jk_error:
    _jk = None
    print(f"calibration_counts: journal_keys is not importable ({_jk_error}) -- task ids are read as bare "
          "and `closes:t-NNN@label` as `closes:t-NNN`", file=sys.stderr)

# t-852 (F6-3): the dead-worker replacement marker `replaces_worker:<ref>` is read by the VALIDATOR's own
# tokenizer (journal_validator.extract_replaces_worker: the first non-whitespace token after the colon), imported,
# not copied. Without the module the marker is not read at all, ANNOUNCED on stderr: a replacement then
# classifies as it did before this branch existed (the pre-t-852 reading, "other").
try:
    import journal_validator as _jv
except ImportError as _jv_error:
    _jv = None
    print(f"calibration_counts: journal_validator is not importable ({_jv_error}) -- a `replaces_worker:` "
          "marker is not read and a dead-worker replacement classifies as before", file=sys.stderr)

# Output safe on Windows consoles with a non-UTF8 codepage (B-449: tools/streams.py). Guarded like the
# journal_keys import above: this script may run outside this tree, and without the module the stream
# setup is a no-op (I1: a tool never crashes because of its stream setup).
try:
    import streams
except ImportError:
    streams = None
if streams:
    streams.utf8_stdio()

# Migration cutovers. A FRESH install enforces every typed field from
# day one -- leave both at the epoch. If you are adopting the policy on
# an EXISTING journal, set these to your own cutover moments: events
# earlier than the cutoff are read manually, append-only, and excluded
# from the field-completeness candidate count (see CLAUDE.md's "Routing
# log" section and the weekly calibration protocol).
DEFAULT_BY_SINCE = "1970-01-01T00:00:00"
LEGACY_CUTOFF = "1970-01-01T00:00:00"

MODEL_REQUIRED_EVENTS = {"delegated", "escalated", "accepted", "rejected"}
TASK_ID_REQUIRED_EVENTS = {"delegated", "accepted", "rejected", "escalated", "defect_found"}
FAILURE_CLASSES = {"spec", "capability", "recon", "tooling"}
LIFECYCLE_EVENTS = {"delegated", "accepted", "rejected", "escalated"}
ALWAYS_REQUIRED_FIELDS = ("agent", "category", "notes")

# Unclosed-tasks fix (a prior review finding): literal mirror of
# tools/session_context.py's _CLOSES_RE -- the same shape the
# SessionStart hook reads (left-anchored \b so "discloses:t-001"/
# "encloses:t-133" do not match as a substring; the value is ONLY
# t-\d+, not an arbitrary non-whitespace token -- this IS the scanner's
# actual shape, not literally "the first non-whitespace fragment":
# trailing punctuation like "closes:t-042;" is naturally excluded by
# \d+ itself, no separate trimming needed). Deliberately duplicated,
# not imported: this script works standalone across journal formats
# (see module docstring) and does not depend on session_context.py,
# which is specific to the harness's SessionStart hook.
# B-402: the optional `@label` names a declared instance (see tools/journal_keys.py). The
# tokenizer is journal_keys.closes_tokens; this regex is the fallback copy for a failed import of
# journal_keys (a test pins its pattern equal to journal_keys.CLOSES_RE). A token whose `@...` is
# not a valid label closes NOTHING (t-525 F1).
CLOSES_RE = re.compile(r"(?<!\w)closes:(t-\d+)(@[A-Za-z0-9_-]*)?")
_LABEL_RE = re.compile(r"^[a-z0-9-]{1,24}$")


def extract_closes_tokens(notes: Optional[str]) -> List[str]:
    """closes:t-NNN[@label] tokens from a notes field -- mirrors
    session_context._closes_task_ids: an empty list for a non-string/
    missing notes, never raises."""
    if not isinstance(notes, str):
        return []
    if _jk is not None:
        return _jk.closes_tokens(notes)
    out: List[str] = []
    for m in CLOSES_RE.finditer(notes):
        at = m.group(2)
        if at is None:
            out.append(m.group(1))
        elif _LABEL_RE.match(at[1:]):
            out.append(m.group(1) + at)
    return out


def _load_segments(path: str):
    """(segments, reason) of the declaration beside the journal `path`; never raises. Without
    journal_keys: (None, reason) and every id reads bare."""
    if _jk is None:
        return None, "journal_keys is not importable"
    return _jk.load_segments(path)


def _key(d: Dict[str, Any], segs) -> Optional[Tuple[str, str]]:
    """The task key of an event: (label, task_id); None when the event has no task_id."""
    tid = d.get("task_id")
    if not isinstance(tid, str) or not tid:
        return None
    if _jk is None or segs is None:
        return ("", tid)
    return _jk.task_key(d, segs) or ("", tid)


def _closes_key(token: str, carrier: Dict[str, Any], segs) -> Tuple[str, str]:
    """The key a closes: token names. Without journal_keys, `t-NNN@label` reads as `t-NNN`; a token
    journal_keys cannot parse (a legacy short id) keeps the bare reading."""
    if _jk is not None and segs is not None:
        key = _jk.ref_key(token, carrier, segs)
        if key is not None:
            return key
    return ("", token.split("@", 1)[0])


def _display(key: Tuple[str, str]) -> str:
    return _jk.display(key) if _jk is not None else key[1]


class CrossFile:
    """What the task-level sections need from ALL journal files (t-581): the keys closed by a
    `closes:` token (resolved by the carrier's file: journal_keys.ref_key), the keys with an accepted,
    and the keys escalated per file; t-852: the worker_refs of every delegated per key (a replacement whose
    original sits in another file). Built from a journal_keys.Journal."""

    def __init__(self, journal) -> None:
        self.tokens: set = set()
        self.accepted: set = set()
        self._escalated: Dict[str, set] = {}
        self._refs: Dict[Tuple[str, str], List[Tuple[str, Optional[datetime], str]]] = {}
        for r in journal.rows:
            if r.obj is None:
                continue
            ref = r.obj.get("worker_ref")
            if r.key is not None and r.obj.get("event") == "delegated" and isinstance(ref, str) and ref:
                self._refs.setdefault(r.key, []).append((r.path, parse_ts(r.obj.get("ts")), ref))
            for token in extract_closes_tokens(r.obj.get("notes")):
                key = _jk.ref_key(token, r.obj, journal.segments, journal.label_ids, journal.aliases)
                self.tokens.add(key or ("", token.split("@", 1)[0]))
            if r.key is not None and r.obj.get("event") == "accepted":
                self.accepted.add(r.key)
            if r.key is not None and r.obj.get("event") == "escalated":
                self._escalated.setdefault(r.path, set()).add(r.key)

    def escalated_outside(self, path: str) -> set:
        """The keys escalated in a file other than `path` (a system path ending is compared)."""
        norm = path.replace("\\", "/")
        out: set = set()
        for rel, keys in self._escalated.items():
            if not norm.endswith(rel):
                out |= keys
        return out

    def refs_outside(self, path: str, key: Tuple[str, str], before: Optional[datetime]) -> set:
        """The worker_refs of the delegated lines of `key` written in a file other than `path` and not later
        than `before` (a delegated or a `before` with no parseable ts counts: nothing decides against it)."""
        norm = path.replace("\\", "/")
        return {ref for rel, ts, ref in self._refs.get(key, ())
                if not norm.endswith(rel) and (ts is None or before is None or ts <= before)}


def parse_ts(ts: Optional[str]) -> Optional[datetime]:
    """Parses ts. Returns None if the field is missing/not a
    string/doesn't parse as ISO -- the caller decides what to do (a
    "no ts" candidate, not a crash)."""
    if not isinstance(ts, str) or not ts:
        return None
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


class ParsedLine:
    __slots__ = ("line_no", "raw", "data", "parse_error", "ts")

    def __init__(self, line_no: int, raw: str, data: Optional[Dict[str, Any]],
                 parse_error: Optional[str] = None):
        self.line_no = line_no
        self.raw = raw
        self.data = data
        self.parse_error = parse_error
        self.ts = parse_ts(data.get("ts")) if data else None


def load_journal(path: str) -> List[ParsedLine]:
    lines: List[ParsedLine] = []
    with open(path, "r", encoding="utf-8") as fh:
        for i, raw in enumerate(fh, start=1):
            stripped = raw.rstrip("\n\r")
            if not stripped.strip():
                continue
            try:
                data = json.loads(stripped)
                if not isinstance(data, dict):
                    lines.append(ParsedLine(i, stripped, None, "not a JSON object (not a dict)"))
                    continue
            except json.JSONDecodeError as exc:
                lines.append(ParsedLine(i, stripped, None, f"invalid JSON: {exc}"))
                continue
            lines.append(ParsedLine(i, stripped, data))
    return lines


def _in_window(pl: ParsedLine, start: Optional[datetime], end: Optional[datetime]) -> bool:
    """An event with no parseable ts is not excluded by the window
    (there's no data to decide on) -- it counts as "in window";
    a missing ts is not itself checked separately by this script (ts
    is structurally required in the journal from the first line, and
    counting that separately was not part of this script's brief)."""
    if pl.ts is None:
        return True
    if start is not None and pl.ts < start:
        return False
    if end is not None and pl.ts >= end:
        return False
    return True


def _task_key_fn(fixed_label: Optional[str], segs: Any):
    """The task-key reader of ONE file: (fixed_label, task_id) when the file carries a fixed label
    (t-581), otherwise _key(d, segs) -- the declaration decides. None for an event with no task_id."""
    def _k(d):
        if fixed_label is not None:
            tid = d.get("task_id")
            return (fixed_label, tid) if isinstance(tid, str) and tid else None
        return _key(d, segs)
    return _k


def _counts(in_window: List[ParsedLine]) -> Tuple[Dict[str, int], Dict[str, Dict[str, int]]]:
    """Section 1 -- counts by event type and by tier (agent x event): (by_event, by_agent_event)."""
    by_event: Dict[str, int] = {}
    by_agent_event: Dict[str, Dict[str, int]] = {}
    for pl in in_window:
        ev = pl.data.get("event", "<none>")
        by_event[ev] = by_event.get(ev, 0) + 1
        agent = pl.data.get("agent")
        if isinstance(agent, str) and agent:
            by_agent_event.setdefault(agent, {})
            by_agent_event[agent][ev] = by_agent_event[agent].get(ev, 0) + 1
    return by_event, by_agent_event


def _rule6(in_window: List[ParsedLine], parsed_lines: List[ParsedLine], k, cross: Any, path: str) -> list:
    """Section 2 -- escalation-pairing check: rule-6 candidates.
    Group rejected by (task_id, agent) among events IN WINDOW; >=2 rejected -> look for an escalated with
    the same task_id LATER than the 2nd rejected BY POSITION IN THE FILE (among ALL parsed lines, not
    just the window -- the escalation could sit outside the window's boundary).
    B-402: keyed by the task key (label, task_id): another clone's escalated no longer satisfies this
    clone's rejected pair, and vice versa."""
    rejected_groups: Dict[Tuple[Tuple[str, str], str], List[int]] = {}
    for pl in in_window:
        if pl.data.get("event") != "rejected":
            continue
        tid = pl.data.get("task_id")
        agent = pl.data.get("agent")
        if not tid:
            continue
        tkey = k(pl.data) or ("", tid)
        key = (tkey, agent if isinstance(agent, str) else "<none>")
        rejected_groups.setdefault(key, []).append(pl.line_no)

    escalated_by_task: Dict[Tuple[str, str], List[int]] = {}
    for pl in parsed_lines:
        if pl.data.get("event") == "escalated":
            tid = pl.data.get("task_id")
            if tid:
                escalated_by_task.setdefault(k(pl.data) or ("", tid), []).append(pl.line_no)

    rule6_candidates = []
    for (tkey, agent), line_nos in rejected_groups.items():
        if len(line_nos) < 2:
            continue
        second_reject_line = sorted(line_nos)[1]
        esc_lines = [l for l in escalated_by_task.get(tkey, []) if l > second_reject_line]
        if not esc_lines and cross is not None and tkey in cross.escalated_outside(path):
            continue              # t-581: an escalated of this task written in ANOTHER file (no position to compare)
        if not esc_lines:
            rule6_candidates.append({
                "task_id": _display(tkey),
                "agent": agent,
                "rejected_lines": sorted(line_nos),
                "note": (
                    "candidate; no escalated with this task_id found after the 2nd "
                    "rejected (by file position). Could be closed/superseded (the "
                    "thread continued under a different task_id) -- a human verdict, "
                    "not something this script can decide."
                ),
            })
    return rule6_candidates


def _field_violations(in_window: List[ParsedLine]) -> Tuple[list, list]:
    """Section 3 -- missing typed fields (typed-fields schema): (field_violations, legacy_events)."""
    legacy_cutoff_dt = parse_ts(LEGACY_CUTOFF)
    field_violations = []
    legacy_events = []
    for pl in in_window:
        d = pl.data
        ev = d.get("event")
        tid = d.get("task_id")
        missing = []

        for f in ALWAYS_REQUIRED_FIELDS:
            v = d.get(f)
            if not isinstance(v, str) or not v.strip():
                missing.append(f)

        if ev in MODEL_REQUIRED_EVENTS:
            v = d.get("model")
            if not isinstance(v, str) or not v.strip():
                missing.append("model")

        if ev in TASK_ID_REQUIRED_EVENTS:
            if not isinstance(tid, str) or not tid.strip():
                missing.append("task_id")

        if ev == "rejected":
            fc = d.get("failure_class")
            if fc not in FAILURE_CLASSES:
                missing.append("failure_class")
            attempt = d.get("attempt")
            if not isinstance(attempt, int) or isinstance(attempt, bool):
                missing.append("attempt")

        if ev == "accepted" and d.get("agent") == "builder":
            w = d.get("witness")
            if not isinstance(w, str) or not w.strip():
                missing.append("witness")

        if ev == "defect_found":
            ref = d.get("ref")
            if not isinstance(ref, str) or not ref.strip():
                missing.append("ref")

        if not missing:
            continue

        entry = {"line": pl.line_no, "event": ev, "task_id": tid, "missing_fields": missing}
        if legacy_cutoff_dt is not None and pl.ts is not None and pl.ts < legacy_cutoff_dt:
            legacy_events.append(entry)
        else:
            field_violations.append(entry)
    return field_violations, legacy_events


def _by_violations(in_window: List[ParsedLine], by_since: datetime) -> list:
    """Section 4 -- accepted/rejected with no 'by' relative to --by-since."""
    by_violations = []
    for pl in in_window:
        ev = pl.data.get("event")
        if ev not in ("accepted", "rejected"):
            continue
        if pl.ts is None or pl.ts < by_since:
            continue  # before the validator was activated -- legal
        by_val = pl.data.get("by")
        if not isinstance(by_val, str) or not by_val.strip():
            by_violations.append({
                "line": pl.line_no, "event": ev, "task_id": pl.data.get("task_id"),
                "ts": pl.data.get("ts"),
            })
    return by_violations


def _repeat_branch(agent: Any, prior: Optional[str], has_attempt_ge2: bool) -> str:
    """How a repeated delegated on an already-seen task_id is classified (section 5)."""
    if agent == "critic":
        return "critic-entry"
    if prior == "accepted" and not has_attempt_ge2:
        return "candidate-duplicate"
    if prior == "rejected":
        return "continuation"
    if has_attempt_ge2:
        return "retry"
    return "other"


def _replaces_ref(notes: Any) -> Optional[str]:
    """The ref of a `replaces_worker:<ref>` marker in notes, by the validator's own tokenizer; None without the
    marker (or without journal_validator -- announced at import)."""
    return _jv.extract_replaces_worker(notes) if _jv is not None else None


def _mark_replacement(entry: Dict[str, Any], marker: str, found: bool) -> None:
    """Section 5, t-852: a repeated delegated that carries `replaces_worker:<marker>`. `found` = the marker is the
    worker_ref of an EARLIER delegated of the same task key (this file before this line, or another file by key,
    whole files -- not only the window: the validator judges against the whole history, the window only picks which
    repeats are reported). Found = a legitimate dead-worker replacement, whatever else the line carries (an `attempt`
    that grew is shown by the line, not a reason to demote it). Not found stays on the branch it had; if that is
    "other" it gets the reason -- a fabricated ref is a defect worth a human verdict."""
    entry["replaces_worker"] = marker
    if found:
        entry["branch"] = "replacement"
    elif entry["branch"] == "other":
        entry["reason"] = "replaces_worker ref not found"


def _lifecycle(parsed_lines: List[ParsedLine], k, window_start: Optional[datetime],
               window_end: Optional[datetime], cross: Any = None,
               path: str = "") -> Tuple[list, Dict[Tuple[str, str], str]]:
    """Section 5 -- task_id integrity: repeated delegated. Returns (duplicate_delegates, last_status_k).
    Walk IN FILE ORDER (all distinct-parsed events, not just the window, so the "last lifecycle status"
    doesn't lose history from before the window) -- but only register a repeat in the report when its own
    delegated line falls inside the window. last_status / seen_delegated are BARE on purpose (an id reused
    after an accepted is always a candidate); last_status_k (B-402, section 10 only) is keyed
    (label, task_id) -> last lifecycle event. defect_found does not move the original task's lifecycle
    status (it has its own task_id for the new finding; ref points back to the original)."""
    last_status: Dict[str, str] = {}          # task_id -> last lifecycle event
    seen_delegated: Dict[str, bool] = {}      # task_id -> at least one delegated seen
    last_status_k: Dict[Tuple[str, str], str] = {}
    refs_seen: Dict[Tuple[str, str], set] = {}   # t-852: task key -> the worker_refs of its delegated lines so far
    duplicate_delegates = []
    for pl in parsed_lines:
        d = pl.data
        ev = d.get("event")
        tid = d.get("task_id")
        if not isinstance(tid, str) or not tid:
            continue
        if ev == "delegated":
            agent = d.get("agent")
            attempt = d.get("attempt")
            has_attempt_ge2 = (isinstance(attempt, int) and not isinstance(attempt, bool)
                                and attempt >= 2)
            prior = last_status.get(tid)
            if seen_delegated.get(tid) and _in_window(pl, window_start, window_end):
                # a repeated delegated on an already-seen task_id
                entry = {
                    "line": pl.line_no, "task_id": tid, "agent": agent,
                    "attempt": attempt, "prior_status": prior,
                    "branch": _repeat_branch(agent, prior, has_attempt_ge2),
                }
                marker = _replaces_ref(d.get("notes"))
                if marker is not None:
                    found = marker in refs_seen.get(k(d), ()) or (
                        cross is not None and marker in cross.refs_outside(path, k(d), pl.ts))
                    _mark_replacement(entry, marker, found)
                duplicate_delegates.append(entry)
            ref = d.get("worker_ref")
            if isinstance(ref, str) and ref:
                refs_seen.setdefault(k(d), set()).add(ref)
            seen_delegated[tid] = True
            last_status[tid] = "delegated"
            last_status_k[k(d)] = "delegated"
        elif ev in ("accepted", "rejected", "escalated"):
            last_status[tid] = ev
            last_status_k[k(d)] = ev
        elif ev == "decomposable":
            # Unclosed-tasks fix (a prior review finding), part (2): per the policy state machine
            # (CLAUDE.md's journal mermaid diagram), decomposable CLOSES the dispatch (a return to the
            # coordinator under the same task_id) -- it does not stay "delegated" forever.
            last_status[tid] = "decomposable"
            last_status_k[k(d)] = "decomposable"
    return duplicate_delegates, last_status_k


def _ts_anomalies(in_window: List[ParsedLine]) -> list:
    """Section 6 -- ts monotonicity."""
    ts_anomalies = []
    prev_ts = None
    prev_line = None
    for pl in in_window:
        if pl.ts is None:
            continue
        if prev_ts is not None and pl.ts < prev_ts:
            ts_anomalies.append({
                "line": pl.line_no, "ts": pl.data.get("ts"),
                "prev_line": prev_line, "prev_ts": prev_ts.isoformat(),
            })
        prev_ts = pl.ts
        prev_line = pl.line_no
    return ts_anomalies


def _false_accept(in_window: List[ParsedLine]) -> Dict[str, Dict[str, Any]]:
    """Section 7 -- false-accept rate by tier."""
    defect_by_agent: Dict[str, int] = {}
    accepted_by_agent: Dict[str, int] = {}
    for pl in in_window:
        ev = pl.data.get("event")
        agent = pl.data.get("agent")
        if not isinstance(agent, str) or not agent:
            continue
        if ev == "defect_found":
            defect_by_agent[agent] = defect_by_agent.get(agent, 0) + 1
        elif ev == "accepted":
            accepted_by_agent[agent] = accepted_by_agent.get(agent, 0) + 1
    false_accept = {}
    for agent in set(list(defect_by_agent) + list(accepted_by_agent)):
        d_count = defect_by_agent.get(agent, 0)
        a_count = accepted_by_agent.get(agent, 0)
        rate = (d_count / a_count) if a_count else None
        false_accept[agent] = {"defect_found": d_count, "accepted": a_count, "rate": rate}
    return false_accept


def _rejected_distribution(in_window: List[ParsedLine]) -> list:
    """Section 8 -- rejected distribution by failure_class x agent x model, sorted by that triple."""
    rejected_distribution: Dict[Tuple[str, str, str], int] = {}
    for pl in in_window:
        if pl.data.get("event") != "rejected":
            continue
        fc = pl.data.get("failure_class", "<none>")
        agent = pl.data.get("agent", "<none>")
        model = pl.data.get("model", "<none>")
        key = (fc, agent, model)
        rejected_distribution[key] = rejected_distribution.get(key, 0) + 1
    return [
        {"failure_class": fc, "agent": a, "model": m, "count": c}
        for (fc, a, m), c in sorted(rejected_distribution.items())
    ]


def _degradation_pairs(in_window: List[ParsedLine]) -> list:
    """Section 9 -- degradation: lead_degraded/lead_restored pairs."""
    degradation_pairs = []
    open_degraded = None
    for pl in in_window:
        ev = pl.data.get("event")
        if ev == "lead_degraded":
            if open_degraded is not None:
                degradation_pairs.append({
                    "degraded_line": open_degraded["line"], "degraded_ts": open_degraded["ts"],
                    "restored_line": None, "restored_ts": None,
                    "note": "not closed by a following lead_degraded (another degraded before a restored)",
                })
            open_degraded = {"line": pl.line_no, "ts": pl.data.get("ts")}
        elif ev == "lead_restored":
            if open_degraded is not None:
                degradation_pairs.append({
                    "degraded_line": open_degraded["line"], "degraded_ts": open_degraded["ts"],
                    "restored_line": pl.line_no, "restored_ts": pl.data.get("ts"),
                    "note": "closed",
                })
                open_degraded = None
            else:
                degradation_pairs.append({
                    "degraded_line": None, "degraded_ts": None,
                    "restored_line": pl.line_no, "restored_ts": pl.data.get("ts"),
                    "note": "lead_restored with no preceding lead_degraded in window",
                })
    if open_degraded is not None:
        degradation_pairs.append({
            "degraded_line": open_degraded["line"], "degraded_ts": open_degraded["ts"],
            "restored_line": None, "restored_ts": None,
            "note": "NOT CLOSED by the end of the window/file -- legal if the session "
                    "is still alive / recorded as the last event",
        })
    return degradation_pairs


def _unclosed(parsed_lines: List[ParsedLine], last_status_k: Dict[Tuple[str, str], str], k, segs: Any,
              cross: Any) -> Tuple[list, list]:
    """Section 10 -- unclosed tasks: (unclosed_tasks, closed_by_decomposable).
    A prior review finding: "open" is the last lifecycle status being delegated (decomposable is now also
    a lifecycle status -- it closes), AND the task is not marked by a closes: token anywhere in the
    journal's notes, AND the task carries no accepted anywhere in the journal (accepted_tids).
    closes: tokens are collected from the notes of ALL parsed lines (not just lifecycle events -- the
    token can sit in a LATER event's notes, e.g. dispatch_skipped/calibrated), across the WHOLE file,
    mirroring session_context.open_dispatches(), which likewise scans notes regardless of event type. A
    token's mere presence closes the task for this counter (this script does not attempt to reproduce
    session_context.py's full (ts, file_idx) "can a later delegated reopen past a marker" semantics -- it
    prints candidates, not a binding verdict; see the module docstring).
    Unclosed-tasks fix, part (3): mirror session_context.open_dispatches()'s JOURNAL LAW -- ANY accepted
    closes its task_id UNCONDITIONALLY, regardless of file position or ts (the journal's own append-only
    contract forbids reopening an accepted task), checked BEFORE the decomposable/delegated status
    branches. The class this catches: an orphan delegated inserted IN THE FILE after its own accepted
    (file position lies, ts is truthful) -- a plain last-write-wins-by-position scan would list that task
    "open". Collected across the WHOLE file (parsed_lines, not just the window). Applied POINTEDLY only
    here: last_status itself is NOT rewritten (the duplicate_delegates classification keys off prior_status
    as already computed; changing that is a separate question). Acknowledged divergence from
    session_context: the full (ts, file_idx) semantics for delegated/closes: tokens are not reproduced.
    B-402: the token set and the accepted set are KEYED -- an accepted / closes: token of the OTHER clone
    no longer closes this one's task; a declared instance is printed as t-NNN@label
    (journal_keys.display). t-581: with `cross` the tokens and accepted keys come from ALL the journal
    files."""
    closed_via_token: set = set()
    if cross is not None:
        closed_via_token |= cross.tokens          # t-581: resolved by FILE, over all the journal files
    else:
        for pl in parsed_lines:
            for token in extract_closes_tokens(pl.data.get("notes")):
                closed_via_token.add(_closes_key(token, pl.data, segs))
    accepted_tids: set = set(cross.accepted) if cross is not None else set()       # keys (label, task_id)
    for pl in parsed_lines:
        if pl.data.get("event") != "accepted":
            continue
        key = k(pl.data)
        if key is not None:
            accepted_tids.add(key)
    unclosed_tasks = []
    closed_by_decomposable = []
    for key, status in last_status_k.items():
        if key in closed_via_token:
            continue
        if key in accepted_tids:
            continue
        if status == "decomposable":
            closed_by_decomposable.append(_display(key))
            continue
        if status == "delegated":
            unclosed_tasks.append(_display(key))
    unclosed_tasks.sort()
    closed_by_decomposable.sort()
    return unclosed_tasks, closed_by_decomposable


def analyze_journal(path: str, window_start: Optional[datetime], window_end: Optional[datetime],
                     by_since: datetime, segments: Any = None, *, fixed_label: Optional[str] = None,
                     cross: Any = None) -> Dict[str, Any]:
    # B-402: `segments` = the Segments of tools/journal_keys.py; None = the declaration beside the
    # journal `path` (never raises: a broken one reads as none, said on stderr, never in the report)
    # t-581: `fixed_label` = the label every task key of THIS file carries (a developer file: its slug,
    # "" for the file that continues the history); None = the history, keyed by the declaration.
    # `cross` = CrossFile (see cross_file): the closes: tokens, accepted and escalated keys of ALL the
    # journal files -- the sections that are about a task (unclosed, escalation pairing) read through
    # it, the sections that are about the file's own order (ts, repeats, fields) stay per file.
    if segments is None:
        segments, segments_reason = _load_segments(path)
        if segments_reason:
            print(f"calibration_counts: the task-key declaration beside {path} is unreadable "
                  f"({segments_reason}) -- colliding task ids are read as one task", file=sys.stderr)
    segs = segments
    k = _task_key_fn(fixed_label, segs)
    all_lines = load_journal(path)
    unparsable = [
        {"line": pl.line_no, "error": pl.parse_error, "raw": pl.raw}
        for pl in all_lines if pl.data is None
    ]
    parsed_lines = [pl for pl in all_lines if pl.data is not None]
    in_window = [pl for pl in parsed_lines if _in_window(pl, window_start, window_end)]

    by_event, by_agent_event = _counts(in_window)                                         # section 1
    rule6_candidates = _rule6(in_window, parsed_lines, k, cross, path)                    # section 2
    field_violations, legacy_events = _field_violations(in_window)                        # section 3
    by_violations = _by_violations(in_window, by_since)                                   # section 4
    duplicate_delegates, last_status_k = _lifecycle(parsed_lines, k, window_start, window_end, cross, path)   # section 5
    ts_anomalies = _ts_anomalies(in_window)                                               # section 6
    false_accept = _false_accept(in_window)                                               # section 7
    rejected_distribution = _rejected_distribution(in_window)                             # section 8
    degradation_pairs = _degradation_pairs(in_window)                                     # section 9
    unclosed_tasks, closed_by_decomposable = _unclosed(parsed_lines, last_status_k, k, segs, cross)   # section 10
    return {
        "journal": path,
        "total_lines": len(all_lines),
        "parsed_lines": len(parsed_lines),
        "unparsable": unparsable,
        "in_window_count": len(in_window),
        "counts": {"by_event": by_event, "by_agent_event": by_agent_event},
        "rule6_candidates": rule6_candidates,
        "field_violations": field_violations,
        "legacy_events": legacy_events,
        "by_violations": by_violations,
        "duplicate_delegates": duplicate_delegates,
        "ts_anomalies": ts_anomalies,
        "false_accept": false_accept,
        "rejected_distribution": rejected_distribution,
        "degradation_pairs": degradation_pairs,
        "unclosed_tasks": unclosed_tasks,
        "closed_by_decomposable": closed_by_decomposable,
    }


def _fmt_section(title: str) -> str:
    return f"\n=== {title} ===\n"


def _list_section(out: List[str], title: str, items: List[Any], fmt: Callable[[Any], str], empty: str) -> None:
    """One titled block of the text report: a line per item through `fmt`, the `empty` line when there is none."""
    out.append(_fmt_section(title))
    if items:
        out.extend(fmt(item) for item in items)
    else:
        out.append(empty)


def _line_unparsable(u: Dict[str, Any]) -> str:
    return f"  line {u['line']}: {u['error']}"


def _line_rule6(c: Dict[str, Any]) -> str:
    return (f"  task_id={c['task_id']} agent={c['agent']} "
            f"rejected_lines={c['rejected_lines']} -- {c['note']}")


def _line_field_violation(v: Dict[str, Any]) -> str:
    return (f"  line {v['line']} event={v['event']} task_id={v['task_id']}: "
            f"missing {v['missing_fields']}")


def _line_by_violation(v: Dict[str, Any]) -> str:
    return f"  line {v['line']} event={v['event']} task_id={v['task_id']} ts={v['ts']}"


def _repeat_note(v: Dict[str, Any]) -> str:
    """The tail of a repeated-delegated line: the anomaly note of "other" (t-852: with its reason when the line
    carries one), the label of a replacement (with a note when its attempt grew)."""
    if v["branch"] == "other":
        reason = f": {v['reason']}" if v.get("reason") else ""
        return f" (anomalous repeat outside the canonical branches -- needs a human verdict{reason})"
    if v["branch"] == "replacement":
        attempt = v["attempt"]
        grew = (" -- attempt grew on a replacement, it should not"
                if isinstance(attempt, int) and not isinstance(attempt, bool) and attempt >= 2 else "")
        return f" (dead worker){grew}"
    return ""


def _line_repeat(v: Dict[str, Any]) -> str:
    return (f"  line {v['line']} task_id={v['task_id']} agent={v['agent']} "
            f"attempt={v['attempt']} prior_status={v['prior_status']} "
            f"-> {v['branch']}{_repeat_note(v)}")


def _line_ts_anomaly(a: Dict[str, Any]) -> str:
    return (f"  line {a['line']} ts={a['ts']} < line {a['prev_line']} "
            f"prev_ts={a['prev_ts']}")


def _line_rejected(r: Dict[str, Any]) -> str:
    return f"  {r['failure_class']} / {r['agent']} / {r['model']}: {r['count']}"


def _line_degradation(p: Dict[str, Any]) -> str:
    return (f"  degraded(line={p['degraded_line']}, ts={p['degraded_ts']}) -> "
            f"restored(line={p['restored_line']}, ts={p['restored_ts']}): {p['note']}")


def render_text(report: Dict[str, Any]) -> str:
    out = []
    out.append(f"# Journal: {report['journal']}")
    out.append(f"Total lines: {report['total_lines']}; parsed: {report['parsed_lines']}; "
               f"in window: {report['in_window_count']}")

    _list_section(out, "Unparsable lines (candidate violation)", report["unparsable"], _line_unparsable, "  (none)")

    out.append(_fmt_section("Counts by event type"))
    for ev, c in sorted(report["counts"]["by_event"].items()):
        out.append(f"  {ev}: {c}")

    out.append(_fmt_section("Counts by tier x event (agent x event)"))
    for agent, evs in sorted(report["counts"]["by_agent_event"].items()):
        out.append(f"  {agent}: " + ", ".join(f"{ev}={c}" for ev, c in sorted(evs.items())))

    _list_section(out, "Escalation-pairing candidates (a rejected pair with no escalated)",
                  report["rule6_candidates"], _line_rule6, "  (no candidates)")
    _list_section(out, "Missing typed fields (candidate violation, post-legacy)",
                  report["field_violations"], _line_field_violation, "  (none)")

    out.append(_fmt_section(f"Legacy (ts < {LEGACY_CUTOFF}, not violations)"))
    out.append(f"  {len(report['legacy_events'])} event(s) with missing fields, pre-dating the typed-fields schema")

    _list_section(out, "Missing 'by' (post by-since)", report["by_violations"], _line_by_violation, "  (none)")
    _list_section(out, "Repeated delegated by task_id (branch classification)",
                  report["duplicate_delegates"], _line_repeat, "  (no repeats)")
    n_replaced = sum(1 for v in report["duplicate_delegates"] if v["branch"] == "replacement")
    if n_replaced:
        out.append(f"  replacement (dead worker): {n_replaced} (legitimate, the validator's rule 9c2 -- not anomalous)")
    _list_section(out, "ts anomalies (informational, known non-monotonic-clock classes)",
                  report["ts_anomalies"], _line_ts_anomaly, "  (none)")

    out.append(_fmt_section("False-accept rate by tier"))
    for agent, fa in sorted(report["false_accept"].items()):
        rate_s = f"{fa['rate']:.4f}" if fa["rate"] is not None else "n/a (accepted=0)"
        out.append(f"  {agent}: defect_found={fa['defect_found']} / accepted={fa['accepted']} "
                   f"= {rate_s}")

    _list_section(out, "Rejected by failure_class x agent x model",
                  report["rejected_distribution"], _line_rejected, "  (no rejected in window)")
    _list_section(out, "lead_degraded/lead_restored pairs",
                  report["degradation_pairs"], _line_degradation, "  (no degradation events in window)")

    out.append(_fmt_section("Unclosed tasks (last lifecycle event = delegated, "
                             "no closes: token)"))
    if report["unclosed_tasks"]:
        out.append("  " + ", ".join(report["unclosed_tasks"]))
    else:
        out.append("  (none)")
    if report["closed_by_decomposable"]:
        out.append("  closed: decomposable -- " + ", ".join(report["closed_by_decomposable"]))

    return "\n".join(out)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    p.add_argument("--journal", action="append", default=None,
                    help="path to ONE journal file (repeatable); without it every journal file of "
                         "--root is read (the history logs/routing-log.jsonl and logs/journal/*.jsonl)")
    p.add_argument("--root", default=None,
                    help="the repository root for the default mode (default: the repository of this script)")
    p.add_argument("--window-start", default=None, help="ISO ts, inclusive (>=)")
    p.add_argument("--window-end", default=None, help="ISO ts, exclusive (<)")
    p.add_argument("--by-since", default=DEFAULT_BY_SINCE,
                    help="when the 'by'-field validator was activated (default "
                         f"{DEFAULT_BY_SINCE})")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    return p.parse_args(argv)


def _parse_window(args: argparse.Namespace) -> Optional[Tuple[Optional[datetime], Optional[datetime], datetime]]:
    """(window_start, window_end, by_since) from the flags, or None after naming the first invalid one on stderr
    (the order start, end, by-since is the order of the checks). An empty --window-* flag reads as not given;
    --by-since always has a value, so an empty one is invalid."""
    parsed = []
    for flag, raw, optional in (("--window-start", args.window_start, True),
                                ("--window-end", args.window_end, True),
                                ("--by-since", args.by_since, False)):
        if optional and not raw:
            parsed.append(None)
            continue
        value = parse_ts(raw)
        if value is None:
            print(f"calibration_counts: invalid {flag} {raw!r}", file=sys.stderr)
            return None
        parsed.append(value)
    return parsed[0], parsed[1], parsed[2]


def _default_reports(args: argparse.Namespace, window_start: Optional[datetime], window_end: Optional[datetime],
                     by_since: datetime) -> Optional[list]:
    """t-581: the reports of the default mode, one per journal file of the root through journal_keys.load_all; None
    after printing why there are none (the exit is 2)."""
    if _jk is None:
        print("calibration_counts: journal_keys is not importable; pass --journal PATH", file=sys.stderr)
        return None
    root = Path(args.root) if args.root else Path(__file__).resolve().parent.parent
    journal = _jk.load_all(root)
    if not journal.files and not journal.rows_of(_jk.HISTORY_REL):
        print(f"calibration_counts: no journal under {root} ({_jk.HISTORY_REL}, {_jk.JOURNAL_DIR_REL}/*.jsonl); "
              "pass --journal PATH", file=sys.stderr)
        return None
    for p in journal.problems:
        print(f"calibration_counts: journal problem: {p}", file=sys.stderr)
    cross = CrossFile(journal)
    targets = ([(_jk.HISTORY_REL, None)] if journal.rows_of(_jk.HISTORY_REL) else []) + [
        (f.path, "" if f.successor else f.slug) for f in journal.files]
    reports = []
    for rel, fixed in targets:
        try:
            reports.append(analyze_journal(str(root / rel), window_start, window_end, by_since,
                                           journal.segments if fixed is None else _jk.NO_SEGMENTS,
                                           fixed_label=fixed, cross=cross))
        except OSError as exc:
            print(f"calibration_counts: failed to read {rel!r}: {exc}", file=sys.stderr)
            return None
    return reports


def _print_loaded(reports: List[Dict[str, Any]]) -> None:
    """t-852: the header of the default mode -- WHICH files were loaded and how many events each gave (parsed lines;
    an unparsable line is counted aside, never dropped), so a calibration never silently counts one file."""
    print(f"# Journals loaded: {len(reports)} file(s)")
    for report in reports:
        bad = f", {len(report['unparsable'])} unparsable" if report["unparsable"] else ""
        print(f"  {report['journal']}: {report['parsed_lines']} events ({report['in_window_count']} in window{bad})")


def _print_summary(reports: List[Dict[str, Any]]) -> None:
    """The SUMMARY block: one line of counters per report (main prints it only for more than one)."""
    print(_fmt_section("SUMMARY across all journals"))
    for report in reports:
        n_rule6 = len(report["rule6_candidates"])
        n_field = len(report["field_violations"])
        n_by = len(report["by_violations"])
        n_dup = len(report["duplicate_delegates"])
        n_ts = len(report["ts_anomalies"])
        n_rejected = report["counts"]["by_event"].get("rejected", 0)
        print(f"  {report['journal']}: rejected={n_rejected}, rule6_candidates={n_rule6}, "
              f"field_violations={n_field}, by_violations={n_by}, "
              f"duplicate_delegates={n_dup}, ts_anomalies={n_ts}, "
              f"unparsable={len(report['unparsable'])}")


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    window = _parse_window(args)
    if window is None:
        return 2
    window_start, window_end, by_since = window

    reports = []
    if args.journal:
        for path in args.journal:
            try:
                reports.append(analyze_journal(path, window_start, window_end, by_since))
            except OSError as exc:
                print(f"calibration_counts: failed to read {path!r}: {exc}", file=sys.stderr)
                return 2
    else:
        reports = _default_reports(args, window_start, window_end, by_since)
        if reports is None:
            return 2

    if args.json:
        print(json.dumps({"journals": reports}, ensure_ascii=False, indent=2))
        return 0

    if not args.journal:
        _print_loaded(reports)         # the explicit --journal output stays byte-identical: its files are the ones named
    for report in reports:
        print(render_text(report))

    if len(reports) > 1:
        _print_summary(reports)

    return 0


if __name__ == "__main__":
    sys.exit(main())
