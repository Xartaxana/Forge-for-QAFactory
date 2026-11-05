"""hop_metrics.py -- characters and tokens per HOP of a task chain, from the journal and the transcripts
(t-797 F5-2 M3, feature F19; SIBLING_MAP axis 14). A measurer: it prints, it never gates and never writes.

    python tools/hop_metrics.py [--node <slug>/<N>/<id>] [--window YYYY-MM-DD] [--json]
                                [--root DIR] [--projects-root DIR]

A HOP is one `delegated` journal line (a worker launched by the Lead). A CHAIN is the hops of the tasks that
share one pile node `<slug>/<N>/<id>` (journal_keys.node_of: the `node` field, else the node token of the
notes); a task with no node is UNLINKED -- its link is never guessed (I4). Per hop:
  worker side  kind, brief_chars (the dispatch text), brief_prose_lines (the Lead's prose in it, F1),
               handback_chars + form/flags (the report and its digest form), units (the worker's usage);
  Lead side    lead_intake_chars (the hand-back arriving in the Lead's context as a message),
               lead_read_chars (what the Lead read of the report afterwards), lead_write_chars (what it wrote
               into the report file: the Edit/Write text of the spec of a designer hop).
`chars` of a hop = brief_chars + lead_intake_chars + lead_read_chars + lead_write_chars (what crossed to or
from the Lead; handback_chars is the report's own size, already inside lead_intake_chars, so it is shown but
not added). A hop with an `n/d` column among those four prints `chars` as PARTIAL -- the table `51120+`, the JSON
`chars_partial: true` -- the known part is never lost and never passed off as the whole (FR-41); with every
column `n/d`, `chars` is `n/d`. The total of a chain is TWO sums, `chars` and `units`, never one (I7: characters
and tokens are not the same unit); no money is printed anywhere (P18).

UNIT_WEIGHTS is the ONE carrier of the weights in code. They are the weights of calibration check 17 (cache-read
0.1, cache-write 2, output 5) and the ASSUMPTION `input` = 1, for which that check has no carrier of its own.

An unknown is never printed as zero (I3, FR-41): an unread carrier is `n/d` with a reason code; a MEASURED
zero (the transcript was read and holds no Read of the report) is `0`. The summary names the number of hops that
carry an `n/d` and the reasons. Reason codes: bad_ref (worker_ref is not agent:<id>), no_transcript (no single
agent-<id>.jsonl), unreadable, no_brief (the transcript holds no user line), prose_error (the prose lines were
not counted: a failed sibling import; the chars stay), no_usage, bad_usage (a non-numeric usage value), no_text
(the transcript holds no hand-back), form_error (digest_form is unavailable or failed on the hand-back), no_main
(the parent session's main transcript is absent), no_intake (no hand-back message for this agent in the parent
session, in either carrier), no_origin (no counted intake, and a queued-command attachment that carries this
agent's tag has no `origin.kind`: it is not counted, the code says why), no_launch (no launch line for this agent
in the parent session).

Only the PARENT session's main transcript is scanned (the line `scanned: parent sessions only`): a hand-back or a
Read in another session is invisible and shows as no_intake. The main transcript is read ONCE per session per run
in one STREAMING pass (transcripts.iter_lines); a line cut by a write is skipped by parse_line; the pass has no
size ceiling. The harness RE-WRITES records of that file under the same `uuid` (E32; measured: 11 282 of 14 256
uuids in one session): a record whose `uuid` was seen in the pass is skipped -- the FIRST copy wins, even if a
later copy differs --, and a tool_use is taken once per id; a record with no `uuid` is its own record (counted,
keyed by its line number). The hand-back reaches the Lead in one of TWO carriers (E20 with the L-5 amendment): a
`user` line (its text) or a queued-command `attachment` whose `origin.kind` is `peer` or `task-notification` (its
`attachment.prompt`) -- never an `instructions` attachment, a `tool_result` block, a queue-operation record or a
human prompt that merely quotes the tag; a MESSAGE counts once (by uuid, then by equal text between the carriers
and between two attachments of one agent), different messages of one agent in different carriers all count.
A tool_use on a report path goes to the LAST hop that launched before it among the hops naming that
path (E24); one before any launch goes to nobody. The stored text of one tool_use input is capped at _TEXT_CAP
characters: a Bash command longer than that names its file only if the name is in the first part (an under-count
of lead_read_chars, named here).

Exit codes: 0 the report was printed (an empty chain too, and an EMPTY journal: the line `journal: empty (0 events)`,
`journal_empty: true`); 1 a call error (the --node form, the date, no folder); 2 the journal cannot be read (no
file, a directory in its place, an unreadable file). `--root` and `--projects-root` are parameters of the functions too: a test never
touches the home folder. stdout only.
"""
import argparse
import json
import posixpath
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))
import dispatch_manifest  # noqa: E402
import handback_extract  # noqa: E402
import journal_keys  # noqa: E402
import journal_validator  # noqa: E402  (extract_replaces_worker: the gate's own reader of the marker)
import streams  # noqa: E402
import transcripts  # noqa: E402
try:
    import digest_form  # noqa: E402
except Exception:  # degraded, loudly: form/flags of every hop say n/d
    digest_form = None

UNIT_WEIGHTS = {"input": 1, "cache_write": 2, "cache_read": 0.1, "output": 5}
_USAGE_FIELD = {"input": "input_tokens", "cache_write": "cache_creation_input_tokens",
                "cache_read": "cache_read_input_tokens", "output": "output_tokens"}
NOT_READS = frozenset({"Edit", "Write", "Agent", "Task", "SendMessage"})  # "Task": the legacy name of Agent
CHAR_COLUMNS = ("brief_chars", "lead_intake_chars", "lead_read_chars", "lead_write_chars")
LEAD_COLUMNS = CHAR_COLUMNS[1:]
WARN_REASONS = frozenset({"node_not_string", "node_not_form", "node_token_differ"})
EXIT_OK, EXIT_CALL, EXIT_JOURNAL = 0, 1, 2
AGENT_REF_RE = re.compile(r"^agent:([A-Za-z0-9_-]+)$")
_LAUNCH_RE = re.compile(r"agentId: ([A-Za-z0-9_-]+)")
_WRITTEN_RE = re.compile(r"written (.+?) bytes=\d+")
_INTAKE_RES = (re.compile(r'<agent-message from="([A-Za-z0-9_-]+)"'), re.compile(r"<task-id>([A-Za-z0-9_-]+)</task-id>"))
_PREFILTER = ("tool_use", "tool_result", "agent-message from=", "<task-id>", "agentId: ")
_TEXT_CAP = 50_000
ATTACHMENT_KINDS = frozenset({"peer", "task-notification"})  # origin.kind of a queued_command that is an intake
_TABLE_HEAD = ("task", "kind", "mark", "session", "form", "flags", "brief_chars", "prose", "handback_chars",
               "units", "intake", "read", "write", "chars")
_UNLINKED_SHOWN = 10


# --- 1. the journal: tasks, nodes, hops ------------------------------------------------------------------

def load_chains(root):
    """(journal, tasks, warnings): `delegated` lines grouped by task key (label, task_id) -- two clones' t-050 are
    two tasks (E28) --, each {"key", "node", "reason", "delegated": [event]}. The node of a task is the first node
    of any of its delegated lines (journal_keys.node_of); with none, the most telling reason of its lines
    ("no_node" when the node is simply absent, "two_tokens", "node_not_form" ...). A line whose node field is
    bad, or names another node than its notes token, is a WARNING line (E26, E27), never a TypeError. The window
    is applied by select, not here: a hop outside it still competes for a report path (E24). Never raises
    (journal_keys.load_all does not)."""
    j = journal_keys.load_all(root)
    tasks, warnings = {}, []
    for obj in j.events():
        key = journal_keys.task_key(obj, j.segments)
        if key is None or obj.get("event") != "delegated":
            continue
        task = tasks.setdefault(key, {"key": key, "node": None, "reason": None, "delegated": []})
        node, reason = journal_keys.node_of(obj)
        task["node"] = task["node"] or node
        task["reason"] = reason if task["reason"] in (None, "no_node") else task["reason"]
        task["delegated"].append(obj)
        if reason in WARN_REASONS:
            warnings.append("%s: %s" % (journal_keys.display(key), reason))      # t-007, or t-007@label of another clone
    for task in tasks.values():
        task["reason"] = None if task["node"] is not None else (task["reason"] or "no_node")
    return j, tasks, warnings


def _blank_hop(task, ev):
    """A hop with every measured field unmeasured (None) -- filled by worker_side and lead_side."""
    ref = ev.get("worker_ref")
    m = AGENT_REF_RE.match(ref) if isinstance(ref, str) else None
    replaces = journal_validator.extract_replaces_worker(ev.get("notes"))      # the gate's reader: ONE rule
    hop = {"task_id": task["key"][1], "label": task["key"][0], "node": task["node"], "unlinked_reason": task["reason"],
           "ts": ev.get("ts") if isinstance(ev.get("ts"), str) else "", "worker_ref": ref if isinstance(ref, str) else None,
           "agent_id": m.group(1) if m else None, "kind": ev.get("agent") if isinstance(ev.get("agent"), str) else None,
           "replaced": replaces is not None, "replaces": replaces, "session": None, "cut": None,
           "form": None, "flags": None, "shares_report_path_with": [], "nd": {}, "notes": [],
           "_located": False, "_path": None, "_main": None, "_paths": set()}
    hop.update({f: None for f in ("brief_chars", "brief_prose_lines", "handback_chars", "units", "requests", "chars")})
    hop["chars_partial"] = False
    hop.update({f: None for f in LEAD_COLUMNS})
    return hop


def hops_of(tasks):
    """Every `delegated` line is a hop, oldest first: with a worker_ref `agent:<id>` it can be measured; any
    other ref (cli:, retro:, none) is a hop that is n/d with a reason (E16). A repeat that carries
    `replaces_worker:<ref>` is its OWN hop, marked `replaced` (E28)."""
    hops = [_blank_hop(task, ev) for task in tasks.values() for ev in task["delegated"]]
    hops.sort(key=lambda h: (h["ts"], h["label"], h["task_id"]))
    return hops


def select(hops, node=None, window=None):
    """The hops of the report: the chain `node` (all hops of its tasks) or every hop, and those whose `ts`
    day is not before `window`. A hop with no ts is outside any window."""
    return [h for h in hops if (node is None or h["node"] == node) and (window is None or h["ts"][:10] >= window)]


# --- 2. the worker side ----------------------------------------------------------------------------------

def _nd(hop, field, code, why):
    hop["nd"][field] = {"code": code, "why": why}


def locate(hop, projects, found=None):
    """Find the hop's transcript and its parent session's main transcript (once). A hop with no agent ref, or
    with no single transcript (none, or two in two sessions: a measurement on the wrong file is worse than none,
    E16), is n/d as a whole: field `worker`. `found`: {agent id: path} from ONE walk
    (transcripts.find_agent_transcripts) when many hops are located; else one glob for this hop."""
    if hop["_located"]:
        return hop
    hop["_located"] = True
    if hop["agent_id"] is None:
        _nd(hop, "worker", "bad_ref", "worker_ref %r is not agent:<id>" % (hop["worker_ref"],))
        return hop
    path = found.get(hop["agent_id"]) if found is not None else transcripts.find_agent_transcript(hop["agent_id"], projects)
    if path is None:
        _nd(hop, "worker", "no_transcript", "no single transcript for agent %s" % hop["agent_id"])
        return hop
    hop["_path"] = path
    hop["_main"] = transcripts.main_transcript_of(path)
    hop["session"] = Path(hop["_main"]).stem if hop["_main"] else None
    return hop


def _section_lines(cut, sec):
    """The 0-based lines of one section that are manifest: its header and the lines under it up to the first
    blank line, never past the section (the stop rule of dispatch_manifest._section_paths, repeated -- queued to
    become one function there)."""
    lines = {sec.header_line}
    for li in range(sec.header_line + 1, sec.last_line + 1):
        if not cut.lines[li].strip():
            break
        lines.add(li)
    return lines


def _manifest_lines(cut):
    """The 0-based lines of the dispatch that are manifest: a manifest-skip line and every section's lines
    (_section_lines)."""
    lines = set(cut.skips)
    for sec in (s for sections in cut.sections.values() for s in sections):
        lines |= _section_lines(cut, sec)
    return lines


def prose_lines(prompt):
    """(count, degraded, handoff paths) of a dispatch text. The count is the Lead's PROSE in the 25-line rule's
    unit (handback_extract.count_lines per line): every non-blank line of the WHOLE text that is not a manifest
    line, not inside a fence or a quote, not a manifest-skip line -- prose AFTER the manifest block counts (E12);
    prose glued to a header with no blank line is read as manifest, an under-count named by calibration 34(b) (E13).
    A degraded cut has no quoted flags: everything outside the manifest is prose and `degraded` is True (E14).
    Raises what section_cut raises (a failed sibling import); the caller makes it n/d."""
    cut = dispatch_manifest.section_cut(prompt)
    manifest = _manifest_lines(cut)
    count = sum(handback_extract.count_lines(line) for li, line in enumerate(cut.lines)
                if line.strip() and li not in manifest and not cut.quoted[li])
    return count, bool(cut.degraded), dispatch_manifest.handoff_paths(cut)


def dispatch_facts(hop):
    """The facts of the hop's dispatch text, read once: chars, prose lines, cut state, handoff paths -- or the
    error. Cached on the hop; the hop must be located first."""
    if "_facts" in hop:
        return hop["_facts"]
    facts = {"chars": None, "prose": None, "degraded": None, "handoff": [], "error": None}
    hop["_facts"] = facts
    if hop["_path"] is None:
        return facts
    try:
        prompt = transcripts.first_user_text(hop["_path"])
    except OSError as exc:
        facts["error"] = ("unreadable", "transcript unreadable: %s" % exc)
        return facts
    if prompt is None:
        facts["error"] = ("no_brief", "the transcript holds no user line")
        return facts
    facts["chars"] = len(prompt)
    try:
        facts["prose"], facts["degraded"], facts["handoff"] = prose_lines(prompt)
    except Exception as exc:  # noqa: BLE001 -- a failed sibling import: the prose is n/d, the chars stay
        facts["error"] = ("prose_error", "prose lines not counted (%s)" % type(exc).__name__)
    return facts


def _usage_units(path):
    """(units, requests, None) or (None, None, (code, why)): the worker's usage joined per request
    (transcripts.request_usages, MAX per field) and weighed by UNIT_WEIGHTS."""
    try:
        requests = transcripts.request_usages(path)
    except OSError as exc:
        return None, None, ("unreadable", "transcript unreadable: %s" % exc)
    except (ValueError, TypeError):
        return None, None, ("bad_usage", "bad usage value")
    if not requests:
        return None, None, ("no_usage", "the transcript holds no usage")
    total = sum(UNIT_WEIGHTS[w] * r[_USAGE_FIELD[w]] for r in requests for w in UNIT_WEIGHTS)
    return round(total, 1), len(requests), None


def _handback_facts(hop, path):
    """handback_chars, form and flags of the worker's last hand-back (handback_extract.extract, digest_form)."""
    try:
        found = handback_extract.extract(path)
    except OSError as exc:
        _nd(hop, "handback_chars", "unreadable", "transcript unreadable: %s" % exc)
        return
    if found is None:
        _nd(hop, "handback_chars", "no_text", "the transcript holds no final assistant text")
        return
    text = found[0]
    hop["handback_chars"] = len(text)
    try:
        d = digest_form.parse(text)
        hop["form"], hop["flags"] = ("none", None) if d is None else ("v1", len(digest_form.flags(d)))
    except Exception as exc:  # noqa: BLE001 -- the reader is an advisor: n/d, never a failure
        _nd(hop, "form", "form_error", "digest_form unavailable (%s)" % type(exc).__name__)


def worker_side(hop, projects):
    """Fill the worker side of a hop in place: kind (the meta's agentType, else the journal's agent), the brief
    (chars, prose lines, cut), units, the hand-back (chars, form, flags). A hop with no transcript stays n/d
    as a whole (field `worker`). Every other failure is n/d of ITS field only; the rest is still counted."""
    locate(hop, projects)
    path = hop["_path"]
    if path is None:
        return hop
    hop["kind"] = transcripts.agent_type(path) or hop["kind"]
    facts = dispatch_facts(hop)
    hop["brief_chars"], hop["brief_prose_lines"] = facts["chars"], facts["prose"]
    hop["cut"] = None if facts["degraded"] is None else ("degraded" if facts["degraded"] else "ok")
    if facts["error"]:
        _nd(hop, "brief", *facts["error"])
    hop["units"], hop["requests"], err = _usage_units(path)
    if err:
        _nd(hop, "units", *err)
    _handback_facts(hop, path)
    return hop


# --- 3. the Lead side: ONE streaming pass over the parent session's main transcript ---------------------------

def _plain(path):
    """A path as the matching key: forward slashes, normalized, lower case."""
    return posixpath.normpath(str(path).replace("\\", "/")).lower()


def _leaves(value, out):
    """Every str leaf of a JSON value, appended to `out`."""
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, dict):
        for v in value.values():
            _leaves(v, out)
    elif isinstance(value, list):
        for v in value:
            _leaves(v, out)


def _call_record(n, block):
    """The record of one tool_use block: line, id, name, file_path, the plain text of the input (not for the
    NOT_READS names and not for Read, which are matched by file_path), the chars it writes (Edit new_string /
    Write content)."""
    name, inp = block.get("name"), block.get("input")
    inp = inp if isinstance(inp, dict) else {}
    leaves = []
    if name not in NOT_READS and name != "Read":
        _leaves(inp, leaves)
    written = inp.get("new_string") if name == "Edit" else inp.get("content") if name == "Write" else None
    file_path = inp.get("file_path")
    return {"line": n, "id": block.get("id"), "name": name, "file": file_path if isinstance(file_path, str) else None,
            "text": "\n".join(leaves).replace("\\", "/").lower()[:_TEXT_CAP],
            "new_chars": len(written) if isinstance(written, str) else 0}


def _take_results(idx, n, content):
    """tool_result blocks of a user line: the chars per tool_use_id; the launch line of an agent (`agentId: <id>`);
    the out path of a handback_extract call (`written <out> bytes=`)."""
    for block in content:
        if not isinstance(block, dict) or block.get("type") != "tool_result":
            continue
        text, tid = transcripts.content_text(block.get("content")) or "", block.get("tool_use_id")
        idx["results"][tid] = len(text)
        m = _LAUNCH_RE.search(text) if "agentId: " in text else None
        if m:
            idx["launch"].setdefault(m.group(1), n)
        m = _WRITTEN_RE.search(text) if "bytes=" in text else None
        if m:
            idx["written"][tid] = m.group(1)


def _intake_agent(text):
    """The agent id named by the first intake tag of `text` (`<agent-message from="<id>"` or
    `<task-id><id></task-id>`), else None."""
    hits = [m for m in (rx.search(text) for rx in _INTAKE_RES) if m]
    return min(hits, key=lambda m: m.start()).group(1) if hits else None


def _count_intake(idx, aid, text, carrier):
    """Credit the chars of one hand-back MESSAGE to its agent, ONCE per message. `carrier` is "user" (a user
    line) or "attachment". idx["msgs"][(agent, text)] remembers which carrier counted the text: an attachment whose
    text is already counted (by a user line or by an earlier attachment) adds nothing; a user line whose text an
    attachment counted first takes the message over and adds nothing; two user lines are two records (the harness's
    re-writes are already dropped by uuid). Different texts of one agent all count, in either carrier."""
    key = (aid, text)
    counted = idx["msgs"].get(key)
    if counted is None or (carrier == "user" and counted == "user"):
        idx["msgs"][key] = carrier
        idx["intake"][aid] = idx["intake"].get(aid, 0) + len(text)
    elif carrier == "user":                     # an attachment counted this message first: the user line takes it over
        idx["msgs"][key] = "user"


def _take_intake(idx, content):
    """A user line whose TEXT carries an intake tag: its chars go to the agent the first tag names (the message is
    credited once, to one agent). tool_result blocks are never text (U10: a Read result that quotes the tag is not
    an intake)."""
    text = transcripts.content_text(content) or ""
    aid = _intake_agent(text)
    if aid is not None:
        _count_intake(idx, aid, text, "user")


def _take_attachment(idx, obj):
    """An `attachment` record: only a `queued_command` whose origin.kind is `peer` or `task-notification` is an
    intake (text = attachment.prompt, the same tags). Never an `instructions` attachment (CLAUDE.md text quotes the
    tag), another attachment type or a human-origin prompt. A tagged queued_command with no str origin.kind is not
    counted and is remembered in idx["no_origin"] (reason code no_origin)."""
    att = obj.get("attachment")
    if not isinstance(att, dict) or att.get("type") != "queued_command":
        return
    text = transcripts.content_text(att.get("prompt")) or ""
    aid = _intake_agent(text)
    if aid is None:
        return
    origin = att.get("origin")
    kind = origin.get("kind") if isinstance(origin, dict) else None
    if not isinstance(kind, str):
        idx["no_origin"].add(aid)
    elif kind in ATTACHMENT_KINDS:
        _count_intake(idx, aid, text, "attachment")


def _seen_before(idx, obj):
    """True when a record with this `uuid` was already taken in the pass (the harness re-writes records under the
    same uuid, E32): the first copy wins. A record with no (str) uuid is never a repeat."""
    uid = obj.get("uuid")
    if not isinstance(uid, str) or not uid:
        return False
    if uid in idx["uuids"]:
        return True
    idx["uuids"].add(uid)
    return False


def _take_calls(idx, n, obj):
    """The tool_use blocks of an assistant line, each tool_use id once (the second guard behind the uuid)."""
    for block in transcripts.content_blocks(obj):
        if not isinstance(block, dict) or block.get("type") != "tool_use":
            continue
        tid = block.get("id")
        if isinstance(tid, str):
            if tid in idx["call_ids"]:
                continue
            idx["call_ids"].add(tid)
        idx["calls"].append(_call_record(n, block))


def _scan_line(idx, n, line):
    """One transcript line of the pass: the substring prefilter, then parse_line, then the uuid dedupe, then by type."""
    if not any(s in line for s in _PREFILTER):
        return
    obj = transcripts.parse_line(line)
    if obj is None or _seen_before(idx, obj):
        return
    kind = obj.get("type")
    if kind == "assistant":
        _take_calls(idx, n, obj)
    elif kind == "user":
        message = obj.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if isinstance(content, list):
            _take_results(idx, n, content)
        _take_intake(idx, content)
    elif kind == "attachment":
        _take_attachment(idx, obj)


def session_index(path, cache=None):
    """The index of a session's main transcript, built in ONE streaming pass (transcripts.iter_lines; the file may
    be 700 MB and may grow while it is read: a cut line is skipped, there is no ceiling), cached per path in
    `cache` for the run. {"path", "lines", "error", "launch": agent id -> line of the launch result, "intake":
    agent id -> chars of its hand-back messages (user lines and peer / task-notification attachments, each message
    once), "no_origin": ids named by a queued_command attachment with no origin.kind (not counted), "calls":
    [tool_use records, one per tool_use id], "results": tool_use_id -> chars of the result, "written":
    tool_use_id -> out path of a `written <out> bytes=` result}; plus the dedupe state "uuids", "call_ids", "msgs".
    A record whose `uuid` was seen is skipped (the first copy wins). An OSError mid-pass leaves the partial index
    with `error` set; the caller shows n/d, never a half number."""
    path = str(path)
    if cache is not None and path in cache:
        return cache[path]
    idx = {"path": path, "lines": 0, "error": None, "launch": {}, "intake": {}, "no_origin": set(), "calls": [],
           "results": {}, "written": {}, "uuids": set(), "call_ids": set(), "msgs": {}}
    try:
        for n, line in enumerate(transcripts.iter_lines(path), start=1):
            idx["lines"] = n
            _scan_line(idx, n, line)
    except OSError as exc:
        idx["error"] = "main transcript unreadable: %s" % exc
    if cache is not None:
        cache[path] = idx
    return idx


# --- 4. attribution of the Lead's tool calls to hops ----------------------------------------------------------

def report_paths(hop, idx):
    """The normalized paths of the hop's report: the absolute `handoff:` paths of its dispatch, and the `<out>` of
    every `written <out> bytes=` result of a tool_use whose input names the hop's agent id (a scout's hand-back
    extracted by handback_extract)."""
    paths = {_plain(p) for p in dispatch_facts(hop)["handoff"]}
    aid = hop["agent_id"].lower()
    for call in idx["calls"]:
        out = idx["written"].get(call["id"])
        if out and aid in call["text"]:
            paths.add(_plain(out))
    return paths


def _matched_paths(call, owners, names):
    """The report paths a tool call is on: a Read/Edit/Write by file_path (normalized equality); any other tool
    outside NOT_READS by the file NAME in the plain text of its input."""
    if call["name"] in ("Read", "Edit", "Write"):
        p = _plain(call["file"]) if call["file"] else None
        return [p] if p in owners else []
    if call["name"] in NOT_READS or not call["text"]:
        return []
    return [p for name, paths in names.items() if name in call["text"] for p in paths]


def _owner_of(call, path, owners, launch):
    """The agent id a call on `path` is credited to: the hop that launched LAST before the call among the hops
    naming the path (E24); None when none launched before it."""
    launched = [(launch[h["agent_id"]], h["agent_id"]) for h in owners[path]
                if launch.get(h["agent_id"], call["line"]) < call["line"]]
    return max(launched)[1] if launched else None


def attribute(idx, peers):
    """{agent id: {"paths", "read", "write"}} for the hops of one session. A call counts once per hop. read = the
    result chars of a Read on the path and of any other non-writing tool whose input names the file; write =
    new_string of an Edit / content of a Write on it. The owner of a call is _owner_of."""
    owners, names = {}, {}
    for peer in peers:
        for p in peer["_paths"]:
            owners.setdefault(p, []).append(peer)
            names.setdefault(posixpath.basename(p), set()).add(p)
    out = {peer["agent_id"]: {"paths": sorted(peer["_paths"]), "read": 0, "write": 0} for peer in peers}
    for call in idx["calls"]:
        credited = {_owner_of(call, p, owners, idx["launch"]) for p in _matched_paths(call, owners, names)} - {None}
        for aid in credited:
            if call["name"] in ("Edit", "Write"):
                out[aid]["write"] += call["new_chars"]
            else:
                out[aid]["read"] += idx["results"].get(call["id"], 0)
    return out


def lead_side(hop, idx, attr):
    """Fill lead_intake_chars / lead_read_chars / lead_write_chars of a hop in place from the session index and the
    attribution. No intake line -> n/d no_intake with the session named (E20); no launch line -> read/write n/d
    (the order is unknown); a hop with no report path -> read and write are a MEASURED 0 with a note (E23); Read x0
    is 0, not n/d (E22). An index with an error: n/d for the three, the worker side is untouched (E19)."""
    sid8 = (hop["session"] or "?")[:8]
    aid = hop["agent_id"]
    if idx["error"]:
        for f in LEAD_COLUMNS:
            _nd(hop, f, "unreadable", idx["error"])
        return hop
    if aid in idx["intake"]:
        hop["lead_intake_chars"] = idx["intake"][aid]
    elif aid in idx["no_origin"]:
        _nd(hop, "lead_intake_chars", "no_origin", "an attachment for this agent in session %s has no origin.kind" % sid8)
    else:
        _nd(hop, "lead_intake_chars", "no_intake", "no intake line in session %s" % sid8)
    if aid not in idx["launch"]:
        for f in ("lead_read_chars", "lead_write_chars"):
            _nd(hop, f, "no_launch", "no launch line for agent %s in session %s" % (aid, sid8))
        return hop
    mine = attr[aid]
    hop["lead_read_chars"], hop["lead_write_chars"] = mine["read"], mine["write"]
    if not mine["paths"]:
        hop["notes"] += ["lead_read_chars: 0 (no report path)", "lead_write_chars: 0 (no report path)"]
    return hop


def _lead_session(main, selected, everyone, cache):
    """lead_side for the selected hops whose worker sits in the session of the main transcript `main`. The peers
    are ALL hops of the journal in that session. An absent main transcript: the three Lead columns are n/d
    no_main (E19)."""
    mine = [h for h in selected if h["_main"] == main]
    if not Path(main).is_file():
        why = "main transcript of session %s is absent" % Path(main).stem[:8]
        for h, f in ((h, f) for h in mine for f in LEAD_COLUMNS):
            _nd(h, f, "no_main", why)
        return
    idx = session_index(main, cache)
    peers = [h for h in everyone if h["_main"] == main]
    for peer in peers:
        peer["_paths"] = report_paths(peer, idx)
    attr = attribute(idx, peers)
    for h in mine:
        lead_side(h, idx, attr)


def lead_all(selected, everyone, projects, cache):
    """lead_side for every selected hop, session by session (_lead_session); returns the main transcripts looked
    at. The peers of a session are ALL hops of the journal whose worker sits in it (a hop outside the chain or the
    window, an unlinked fix round, competes for a report path, E24). A session whose main transcript is absent:
    the three Lead columns are n/d no_main (E19)."""
    found = transcripts.find_agent_transcripts({h["agent_id"] for h in everyone if h["agent_id"]}, projects)
    for h in everyone:
        locate(h, projects, found)
    mains = {h["_main"] for h in selected if h["_main"]}
    for main in sorted(mains):
        _lead_session(main, selected, everyone, cache)
    return mains


# --- 5. the report ---------------------------------------------------------------------------------------------

def _finish_hop(hop):
    """`chars` of a hop: the sum of its known char columns (None when none is known), and `chars_partial` -- True
    when at least one column is n/d and at least one is known (the figure is then a lower bound)."""
    known = [hop[f] for f in CHAR_COLUMNS if hop[f] is not None]
    hop["chars"] = sum(known) if known else None
    hop["chars_partial"] = 0 < len(known) < len(CHAR_COLUMNS)      # some column is n/d: the sum is a lower bound (FR-41)
    return hop


def _totals(hops):
    """The two sums of a set of hops (I7) with the columns that make `chars`, and the n/d count."""
    cols = {f: sum(h[f] for h in hops if h[f] is not None) for f in CHAR_COLUMNS}
    units = [h["units"] for h in hops if h["units"] is not None]
    return {"hops": len(hops), "nd_hops": sum(1 for h in hops if h["nd"]), "chars": sum(cols.values()),
            "units": round(sum(units), 1), "chars_by_column": cols}


def _public(hop):
    return {k: sorted(v) if isinstance(v, set) else v for k, v in hop.items() if not k.startswith("_")}


def related_unlinked(chain, unlinked):
    """The unlinked hops that share a report path with a hop of the chain (the fix round that wrote no node, F13),
    each marked with the task ids it shares with: shown next to the chain, never added to it (I4)."""
    related = []
    for u in unlinked:
        shared = [c["task_id"] for c in chain if c["_paths"] & u["_paths"]]
        if shared:
            u["shares_report_path_with"] = shared
            related.append(u)
    return related


def collect(root, projects, node=None, window=None):
    """The whole report as plain data (the table and --json are two renderings of it). Never prints."""
    j, tasks, warnings = load_chains(root)
    everyone = hops_of(tasks)
    chosen = select(everyone, node, window)
    chain_hops = [h for h in chosen if h["node"]] if node is None else chosen
    unlinked = [h for h in chosen if not h["node"]] if node is None else []
    cache = {}
    for h in chain_hops + unlinked:
        worker_side(h, projects)
    mains = lead_all(chain_hops + unlinked, everyone, projects, cache)
    if node is not None and chain_hops:
        rest = [h for h in select(everyone, None, window) if not h["node"]]
        unlinked = related_unlinked(chain_hops, rest)
        for h in unlinked:
            worker_side(h, projects)
        mains |= lead_all(unlinked, everyone, projects, cache)
    for h in chain_hops + unlinked:
        _finish_hop(h)
    return _assemble(j, warnings, node, window, chain_hops, unlinked, mains)


def _journal_is_empty(j):
    """True when a journal file WAS read and holds no event line: no rows, no problem, and a file that exists --
    the history, or a logs/journal/<slug>.jsonl. An absent file, a directory in its place or an unreadable one is
    NOT empty: it cannot be read (a problem, or no file at all)."""
    return not j.rows and not j.problems and (bool(j.files) or (j.root / journal_keys.HISTORY_REL).is_file())


def _assemble(j, warnings, node, window, chain_hops, unlinked, mains):
    chains = {}
    for h in chain_hops:
        chains.setdefault(h["node"], []).append(h)
    every = chain_hops + unlinked
    return {"node": node, "window": window, "scanned": "parent sessions only", "journal_rows": len(j.rows),
            "journal_empty": _journal_is_empty(j), "sessions": sorted(Path(m).stem for m in mains),
            "chains": [{"node": k, "hops": [_public(h) for h in v], "totals": _totals(v)} for k, v in sorted(chains.items())],
            "unlinked": {"count": len(unlinked), "hops": [_public(h) for h in unlinked],
                         "reasons": Counter(h["unlinked_reason"] or "no_node" for h in unlinked)},
            "nd": {"hops": sum(1 for h in every if h["nd"]),
                   "reasons": Counter(code for h in every for code in {e["code"] for e in h["nd"].values()})},
            "warnings": warnings, "journal_problems": list(j.problems)}


def _cell(value):
    """One table cell: n/d for an unmeasured value, 1 decimal for units, the value otherwise."""
    if value is None:
        return "n/d"
    return ("%.1f" % value) if isinstance(value, float) else str(value)


def hop_cells(hop):
    """The cells of a hop's table row, in _TABLE_HEAD order (the same data as the JSON)."""
    flags = _cell(hop["flags"]) if hop["form"] == "v1" else ("-" if hop["form"] == "none" else "n/d")
    mark = " ".join(m for m in ("replaced" if hop["replaced"] else "", "cut=degraded" if hop["cut"] == "degraded" else "") if m)
    return [journal_keys.display((hop["label"], hop["task_id"])), hop["kind"] or "?", mark,
            (hop["session"] or "?")[:8], hop["form"] or "n/d", flags, _cell(hop["brief_chars"]),
            _cell(hop["brief_prose_lines"]), _cell(hop["handback_chars"]), _cell(hop["units"]),
            _cell(hop["lead_intake_chars"]), _cell(hop["lead_read_chars"]), _cell(hop["lead_write_chars"]),
            _cell(hop["chars"]) + ("+" if hop["chars_partial"] else "")]


def _table(title, hops, totals=None):
    lines = [title, "| " + " | ".join(_TABLE_HEAD) + " |", "|" + "---|" * len(_TABLE_HEAD)]
    lines += ["| " + " | ".join(hop_cells(h)) + " |" for h in hops]
    if totals:
        lines.append("total: chars=%d units=%s (%d hops, %d n/d)" % (totals["chars"], _cell(totals["units"]),
                                                                      totals["hops"], totals["nd_hops"]))
    for h in hops:
        lines += ["  %s %s: n/d (%s) %s" % (h["task_id"], f, e["code"], e["why"]) for f, e in h["nd"].items()]
        lines += ["  %s %s" % (h["task_id"], note) for note in h["notes"]]
    return lines


def _reasons(counts):
    return ", ".join("%s x%d" % (k, counts[k]) for k in sorted(counts))


def render(report):
    """The text report: one table per chain with its two sums, the unlinked hops, and the closing lines
    `n/d hops: k (reasons)`, `unlinked: k (reasons)`, `scanned: parent sessions only`."""
    lines = []
    for chain in report["chains"]:
        lines += _table("chain %s (%d hops)" % (chain["node"], len(chain["hops"])), chain["hops"], chain["totals"]) + [""]
    un = report["unlinked"]
    if un["hops"]:
        lines += _table("unlinked hops", un["hops"]) + [""]
    if report["journal_empty"]:
        lines.append("journal: empty (0 events)")
    if not report["chains"] and not un["hops"]:
        lines.append("no hops for %s" % (report["node"] or "this window"))
    nd = report["nd"]
    lines.append("n/d hops: %d%s" % (nd["hops"], " (%s)" % _reasons(nd["reasons"]) if nd["reasons"] else ""))
    lines.append("unlinked: %d%s" % (un["count"], " (%s)" % _reasons(un["reasons"]) if un["reasons"] else ""))
    for h in un["hops"][:_UNLINKED_SHOWN]:
        shares = " [shares a report path with %s]" % ", ".join(h["shares_report_path_with"]) if h["shares_report_path_with"] else ""
        lines.append("  %s %s%s" % (h["task_id"], h["unlinked_reason"] or "no_node", shares))
    if un["count"] > _UNLINKED_SHOWN:
        lines.append("  ... and %d more" % (un["count"] - _UNLINKED_SHOWN))
    lines += ["warning: %s" % w for w in report["warnings"]] + ["journal problem: %s" % p for p in report["journal_problems"]]
    lines.append("scanned: " + report["scanned"])
    return "\n".join(lines)


# --- 6. the command line -----------------------------------------------------------------------------------------

def _args(argv):
    """(args, None) or (None, exit code). argparse exits 2 on a bad call; here 2 is "journal unreadable", a bad
    call is 1 (--help is 0)."""
    p = argparse.ArgumentParser(prog="hop_metrics.py", description=__doc__.split("\n")[0])
    p.add_argument("--node", help="<slug>/<N>/<id>, e.g. forge/5/F5-2 (a bare id is refused)")
    p.add_argument("--window", help="YYYY-MM-DD: hops from this day on")
    p.add_argument("--json", action="store_true", help="the same data as JSON (sorted keys)")
    p.add_argument("--root", help="the repository root (default: the one of this file)")
    p.add_argument("--projects-root", help="where the session folders are (default: ~/.claude/projects)")
    try:
        return p.parse_args(argv), None
    except SystemExit as exc:
        return None, EXIT_OK if exc.code in (0, None) else EXIT_CALL


def _call_error(args):
    """(root, projects, error text or None): the form of --node and --window, and the two folders."""
    if args.node is not None and journal_keys.NODE_RE.match(args.node) is None:
        return None, None, "--node %r is not a node: write <slug>/<N>/<id>, e.g. forge/5/F5-2" % args.node
    if args.window is not None:
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.window):
                raise ValueError(args.window)
            date.fromisoformat(args.window)
        except ValueError:
            return None, None, "--window %r is not a date: write YYYY-MM-DD" % args.window
    root = Path(args.root) if args.root else _TOOLS_DIR.parent
    try:
        projects = Path(args.projects_root) if args.projects_root else transcripts.projects_root()
    except RuntimeError as exc:
        return root, None, "no projects folder (%s): pass --projects-root" % exc
    for folder in (root, projects):
        if not folder.is_dir():
            return root, projects, "no folder %s" % folder
    return root, projects, None


def main(argv=None):
    args, code = _args(sys.argv[1:] if argv is None else argv)
    if args is None:
        return code
    root, projects, err = _call_error(args)
    if err:
        sys.stderr.write("hop_metrics: %s\n" % err)
        return EXIT_CALL
    report = collect(root, projects, args.node, args.window)
    if not report["journal_rows"] and not report["journal_empty"]:
        sys.stderr.write("hop_metrics: the journal of %s cannot be read: %s\n"
                         % (root, "; ".join(report["journal_problems"]) or "no journal file"))
        return EXIT_JOURNAL
    print(json.dumps(report, sort_keys=True, ensure_ascii=False, indent=2) if args.json else render(report))
    return EXIT_OK


if __name__ == "__main__":
    streams.utf8_stdio()
    sys.exit(main())
