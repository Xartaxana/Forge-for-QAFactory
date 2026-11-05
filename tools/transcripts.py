"""transcripts.py -- the ONE reader of subagent transcripts (B-467, t-612/t-623, feature F19).

The harness writes a worker's transcript to <projects root>/<project slug>/<session id>/subagents/
agent-<agent id>.jsonl, one JSON object per line. Four hooks (dispatch_gate, agent_budget, journal_echo,
and tier_echo as journal_echo's import) used to read that file each in its own way: the layout was
encoded three times, the JSON line parser twice, the line splitter three times. This module is the
leaf they share (SIBLING_MAP Axis 14): the layout, the line splitter, the tail read, the usage and
tool_use readers, the model stream and the live-worker count. Since t-797 (F5-2) also the streaming line
reader `iter_lines`, the per-request usage join `request_parts` (one part per model of a request; since t-882,
F6-23) with its fold `request_usages`, and the worker -> session link `main_transcript_of` (tools/hop_metrics.py
and tools/usage_report.py read through them). Standard library only, nothing from
tools/, no I/O at import.

ERROR DIRECTION is the consumer's, not the module's -- the module raises (OSError on an unreadable
file, ValueError/TypeError on a mistyped usage value) or returns None/[] and each consumer keeps its
own side of the line:
  * dispatch_gate's parallel cap may count a dead worker as live (bounded by the window) and must never
    count an unreadable or live worker as finished;
  * agent_budget fails open (exit 0, silent) and must never STOP on a call that is not a worker's;
  * journal_echo and tier_echo stay silent and must never print a MISMATCH measured on another
    worker's transcript.

LINES are split on "\\n" ONLY (split_lines): JSONL records are separated by "\\n" (json.org, the harness
writer), and U+2028 / U+0085 / U+001C-1E inside a JSON string are legal content, not a line end. This
differs on purpose from the \\r\\n|\\r|\\n split of human text in SIBLING_MAP Axis 7. A trailing "\\r" of a
CRLF file stays on the line and is JSON whitespace, so CRLF files parse unchanged. Before this module
agent_budget and journal_echo/tier_echo used str.splitlines() / universal newlines and read a line
holding a U+2028 as two broken halves.

TAIL: the last TAIL_BYTES of a file, the first (possibly cut) line dropped, and the file's LAST line
always whole: a last line longer than the window (or starting before it) grows the window backwards
(t-840, F6-7; it closes the off-by-one of the moved code, where a last line of exactly TAIL_BYTES,
newline included, was dropped with the cut one). Only the last line has that guarantee: an earlier line
longer than the window, followed by another line, is still cut and dropped by tail_lines.
is_finished does not stop at the last line: it grows the same window backwards until the newest line
that carries a tool_use is whole, up to TAIL_SCAN_MAX (t-857, F6-19).
"""

import json
import re
from pathlib import Path

SUBAGENTS = "subagents"
AGENT_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")
TAIL_BYTES = 64 * 1024
# The bound of is_finished's backward growth (t-857, F6-19): a hand-back line followed by more than this many
# bytes is not looked for -- the answer is "not finished", never a raise. 4 MB covers a 70 KB hand-back behind
# the harness's result/queue lines with a wide margin; a live worker's dispatch must never read the whole
# 200 MB file for one flag.
TAIL_SCAN_MAX = 4 * 1024 * 1024
USAGE_KEYS = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
# Harness-internal stop-sequence lines carry model == "<synthetic>": not a real turn.
SKIP_MODELS = frozenset({"<synthetic>"})
HANDBACK = "SubagentHandback"


def projects_root() -> Path:
    """Where Claude Code keeps session folders; raises RuntimeError when there is no home."""
    return Path.home() / ".claude" / "projects"


def agent_file_name(agent_id):
    """agent-<id>.jsonl; None for a non-string, empty or unsafe id (a glob metacharacter, a separator)."""
    if isinstance(agent_id, str) and AGENT_ID_RE.fullmatch(agent_id):
        return "agent-%s.jsonl" % agent_id
    return None


def subagents_dir_of(transcript_path: str) -> Path:
    """The subagents folder that belongs to a session transcript (or the folder the path is already in)."""
    p = Path(transcript_path)
    return p.parent if p.parent.name == SUBAGENTS else p.with_suffix("") / SUBAGENTS


def find_agent_transcript(agent_id, root=None):
    """The ONE match of <root>/*/*/subagents/agent-<id>.jsonl as a str; None for an unsafe id, no match,
    two or more matches (ambiguous: a measurement on the wrong file is worse than none) or any glob error."""
    name = agent_file_name(agent_id)
    if name is None:
        return None
    try:
        base = projects_root() if root is None else root
        matches = list(base.glob("*/*/%s/%s" % (SUBAGENTS, name)))
    except Exception:
        return None
    return str(matches[0]) if len(matches) == 1 else None


def find_agent_transcripts(agent_ids, root=None) -> dict:
    """{agent id: path or None} for MANY ids with ONE walk of <root>/*/*/subagents -- the same answer per id as
    find_agent_transcript (an unsafe id, no match, two or more matches, any glob error: None). One glob per id costs
    ~0.1 s on a real projects folder; a report over a whole journal (tools/hop_metrics.py, 959 hops) pays once."""
    wanted = {}
    for agent_id in agent_ids:
        name = agent_file_name(agent_id)
        if name is not None:
            wanted[name] = agent_id
    found = {agent_id: [] for agent_id in agent_ids}
    try:
        base = projects_root() if root is None else root
        for match in base.glob("*/*/%s/agent-*.jsonl" % SUBAGENTS):
            if match.name in wanted:
                found[wanted[match.name]].append(str(match))
    except Exception:
        return {agent_id: None for agent_id in agent_ids}
    return {agent_id: (paths[0] if len(paths) == 1 else None) for agent_id, paths in found.items()}


def split_lines(text: str) -> list:
    """The lines of a JSONL text: split on "\\n" only, no trailing empty line; a "\\r" stays on its line."""
    parts = text.split("\n")
    if parts and parts[-1] == "":
        parts.pop()
    return parts


def _newline_before_last_line(data: bytes) -> bool:
    """True when `data` holds a "\\n" that ends a line before its last line (a final "\\n" is the last line's own)."""
    end = len(data) - 1 if data.endswith(b"\n") else len(data)
    return data.rfind(b"\n", 0, end) >= 0


def _read_back(path, enough, limit=None):
    """(data, start): the bytes from file offset `start` to the end of the file. The window is the last
    TAIL_BYTES, then grows backwards -- doubling, each step reads only the bytes it adds, the chunks are joined
    once -- until `enough(chunks, start)` says so (chunks[0] is the file's end, chunks[-1] the newest read), the
    file start is reached, or the window is `limit` bytes (the last step is clipped to it; None = no bound).
    The ONE backward-growth loop: tail_lines and is_finished differ only in `enough`. Raises OSError; a file
    that changes while it is read may give a stale window, never an error."""
    path = Path(path)
    size = path.stat().st_size
    floor = 0 if limit is None else max(0, size - limit)
    start = max(floor, size - TAIL_BYTES)
    with open(path, "rb") as fh:
        fh.seek(start)
        chunks = [fh.read()]
        while start > floor and not enough(chunks, start):
            new_start = max(floor, start - (size - start))
            fh.seek(new_start)
            chunks.append(fh.read(start - new_start))
            start = new_start
    # `chunks` dies on return: a 20 MB last line is held about twice at a time, not four times
    return (b"".join(reversed(chunks)) if len(chunks) > 1 else chunks[0]), start


def _last_line_whole(chunks, _start) -> bool:
    """tail_lines' stop: the window holds a "\\n" before its last line. The first window is looked at whole,
    every later step only at the bytes it added (the older ones were already looked at)."""
    return _newline_before_last_line(chunks[0]) if len(chunks) == 1 else b"\n" in chunks[-1]


def tail_lines(path) -> list:
    """Complete lines of the last TAIL_BYTES of the file (the first, possibly cut, line dropped), and the
    LAST line of the file WHOLE whatever its length: when the window holds no "\\n" before its last line (that
    line is longer than the window or starts before it) the window grows backwards -- doubling, each step
    reads only the bytes it adds -- until that "\\n" is found or the file start is reached (t-840, F6-7).
    A file whose last line fits the window is read once and returns what it always did. Raises OSError; a
    file that changes while it is read may give a stale tail, never an error."""
    data, start = _read_back(path, _last_line_whole)
    text = data.decode("utf-8", errors="replace")
    data = None  # a 20 MB last line is not held three times
    lines = split_lines(text)
    return lines[1:] if start > 0 else lines


def parse_line(line: str):
    """The JSON object of one line; None for anything that is not one (a ValueError, a RecursionError on a
    line of 200,000 '[', a non-dict value)."""
    try:
        obj = json.loads(line)
    except (ValueError, RecursionError):
        return None
    return obj if isinstance(obj, dict) else None


def content_blocks(obj) -> list:
    """message.content of a parsed line when it is a list, else []."""
    msg = obj.get("message") if obj else None
    content = msg.get("content") if isinstance(msg, dict) else None
    return content if isinstance(content, list) else []


def usage_total(line: str):
    """Context tokens of one transcript line; None when it carries no usage (or a zero one).
    A non-numeric usage value RAISES: agent_budget turns that into its fail-open."""
    obj = parse_line(line) if '"usage"' in line else None
    msg = obj.get("message") if obj else None
    usage = msg.get("usage") if isinstance(msg, dict) else None
    if not isinstance(usage, dict):
        return None
    total = sum(int(usage.get(k) or 0) for k in USAGE_KEYS)
    return total if total > 0 else None


def last_usage(lines):
    """The context size of the newest line that carries usage; None when none does."""
    for line in reversed(list(lines)):
        total = usage_total(line)
        if total is not None:
            return total
    return None


def context_size(path):
    """Tokens in context at the last turn that carries usage in the tail; None when no such line is there."""
    return last_usage(tail_lines(path))


def last_tool_use_names(lines):
    """The tool_use names of the newest assistant line that has any; None when no line does."""
    for line in reversed(list(lines)):
        obj = parse_line(line) if '"tool_use"' in line else None
        if not obj or obj.get("type") != "assistant":
            continue
        names = [b.get("name") for b in content_blocks(obj)
                 if isinstance(b, dict) and b.get("type") == "tool_use"]
        if names:
            return names
    return None


def _names_in_window(data: bytes, start: int):
    """last_tool_use_names of the complete lines of a window that begins at file offset `start` (its first
    line is cut unless the window is the whole file)."""
    lines = split_lines(data.decode("utf-8", errors="replace"))
    return last_tool_use_names(lines[1:] if start > 0 else lines)


def _tool_use_line_whole(chunks, start) -> bool:
    """is_finished's stop: the window holds a COMPLETE assistant line with a tool_use. Every line after the
    cut first one is whole and newer than it, so the newest such line decides and nothing older can change it."""
    return _names_in_window(b"".join(reversed(chunks)), start) is not None


def is_finished(path) -> bool:
    """True when the newest assistant tool_use line of the file names SubagentHandback. Raises OSError.
    The ONE reader of "did this worker hand back". The window of tail_lines grows backwards (doubling) until
    that newest tool_use line is whole, so a hand-back of any length is seen whatever short lines the harness
    wrote after it (t-857, F6-19). The growth stops at TAIL_SCAN_MAX: a tool_use line not whole by then, and
    a file with no tool_use line at all, is "not finished" -- never a raise, never a parse of a cut line."""
    data, start = _read_back(path, _tool_use_line_whole, TAIL_SCAN_MAX)
    names = _names_in_window(data, start)
    return bool(names) and HANDBACK in names


def iter_lines(path):
    """Every line of the whole file (utf-8, undecodable bytes replaced), split like split_lines: on "\\n"
    only, no trailing empty line, a "\\r" stays on its line, a last line without "\\n" is a line, an empty
    file has none. A generator: an unreadable file raises OSError on the first next().

    STREAMING (t-797 F5-2, F4): the file is read line by line in binary mode, never whole -- the main
    transcript of a session is 200-700 MB. The result is IDENTICAL to split_lines(data.decode("utf-8",
    errors="replace")) of the whole file (pinned by a differential test): iterating a binary file splits
    on b"\\n" only, "\\n" is never part of a multi-byte sequence, and a sequence cut by "\\n" decodes to the
    same U+FFFD per line as in the whole text. Four hooks read this function; their behaviour is the
    contract. A file that grows while it is read: the line a write has cut is a line (it fails parse_line
    and is skipped by every reader), and nothing caps the pass."""
    with open(path, "rb") as fh:
        for raw in fh:
            yield (raw[:-1] if raw.endswith(b"\n") else raw).decode("utf-8", errors="replace")


def iter_models(path):
    """One model string per assistant turn, in file order; a malformed line, a non-string/empty model
    and a SKIP_MODELS one are skipped and break nothing."""
    for line in iter_lines(path):
        obj = parse_line(line)
        if obj is None or obj.get("type") != "assistant":
            continue
        message = obj.get("message")
        model = message.get("model") if isinstance(message, dict) else None
        if isinstance(model, str) and model and model not in SKIP_MODELS:
            yield model


REQUEST_USAGE_KEYS = USAGE_KEYS + ("output_tokens",)


def request_key(obj, line_no):
    """The key a transcript line's request is joined by: (`requestId`, value), else (`uuid`, value) (non-empty
    strings), else ("line", line number): a line with neither id is its own request (an over-count is allowed,
    an under-count is not). The ONE key of a request: request_parts joins by it and
    usage_report.iter_assistant_turns builds its dedupe_key from it (forge/6 F6-23)."""
    for name in ("requestId", "uuid"):
        value = obj.get(name)
        if isinstance(value, str) and value:
            return (name, value)
    return ("line", line_no)


def cache_write_1h(usage):
    """The 1-hour part of a usage dict's cache writes (usage.cache_creation.ephemeral_1h_input_tokens), or None
    when the line carries no such number (an old transcript, a broken value, a bool, a negative): None means
    "split unknown" -- the consumer prices the whole write as a 5-minute write, never guesses."""
    split = usage.get("cache_creation")
    value = split.get("ephemeral_1h_input_tokens") if isinstance(split, dict) else None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _usage_int(value) -> int:
    """int(value or 0); an infinite float (JSON allows Infinity) is a ValueError like any mistyped value."""
    try:
        return int(value or 0)
    except OverflowError as exc:
        raise ValueError("usage value out of range: %r" % (value,)) from exc


def _iteration_part(entry):
    """One part from one `usage.iterations` entry (the provider's own record of one message of a request: the
    entry carries the usage fields itself, plus `model` and `type`), or None when the entry is unusable: not
    an object, no non-empty str `model`, none of the usage keys, or a mistyped value."""
    model = entry.get("model") if isinstance(entry, dict) else None
    if not isinstance(model, str) or not model or not any(k in entry for k in REQUEST_USAGE_KEYS):
        return None
    try:
        values = {k: _usage_int(entry.get(k)) for k in REQUEST_USAGE_KEYS}
    except (ValueError, TypeError):
        return None
    return {"model": model, **values, "cache_creation_1h_tokens": cache_write_1h(entry)}


def _iteration_parts(usage):
    """(parts, bad) of a usage dict's `iterations`: parts = one part per entry when the list holds 2 or more
    usable entries (a SKIP_MODELS entry is not one), else None; bad = True when `iterations` is present but
    malformed (not a list, or an entry with no usable model/usage) -- the line's iterations are then ignored.
    A list of 0 or 1 entries is ordinary (every single-model request carries one): no carrier, not bad.
    Never raises: iterations are a refinement, the MAX reader below is the fallback."""
    entries = usage.get("iterations")
    if entries is None:
        return None, False
    if not isinstance(entries, list):
        return None, True
    if len(entries) < 2:
        return None, False
    parts = []
    for entry in entries:
        part = _iteration_part(entry)
        if part is None:
            return None, True
        if part["model"] not in SKIP_MODELS:
            parts.append(part)
    return (parts, False) if len(parts) >= 2 else (None, False)


def _assistant_lines(path, skipped, all_lines):
    """(line number, obj, model, info) of every `assistant` line of the file in file order -- the ONE parse of
    a usage line (read_requests reads through it). The model is a str or None (a missing or non-str `model`);
    a SKIP_MODELS line is not yielded. info = (values, 1-hour split, iteration parts or None, iterations
    bad) for a line with a readable usage dict, None for a line with no usage at all (yielded only when
    `all_lines`; otherwise such a line is skipped before it is parsed). A usage that is present but not an
    object, and (with `skipped` given) a mistyped value, are appended to `skipped` as their line number and
    not yielded; without `skipped` a non-object usage is skipped silently and a mistyped value raises
    (ValueError/TypeError)."""
    for n, line in enumerate(iter_lines(path), start=1):
        obj = parse_line(line) if all_lines or '"usage"' in line else None
        if obj is None or obj.get("type") != "assistant":
            continue
        message = obj.get("message")
        usage = message.get("usage") if isinstance(message, dict) else None
        model = message.get("model") if isinstance(message, dict) else None
        model = model if isinstance(model, str) else None
        if model in SKIP_MODELS:
            continue
        if usage is None and all_lines:
            yield n, obj, model, None
            continue
        if not isinstance(usage, dict):
            if skipped is not None and usage is not None:
                skipped.append(n)
            continue
        try:
            values = {k: _usage_int(usage.get(k)) for k in REQUEST_USAGE_KEYS}
        except (ValueError, TypeError):
            if skipped is None:
                raise
            skipped.append(n)
            continue
        carrier, bad = _iteration_parts(usage)
        yield n, obj, model, (values, cache_write_1h(usage), carrier, bad)


def read_requests(path, skipped=None, counts=None, meta=None):
    """(requests, lines) from ONE pass over the file (a live transcript grows between two passes: a line
    appended between them has no part -- t-886 F-2). requests = request_parts' records; lines = [(line number,
    request key tuple, model, meta(obj)), ...] of every non-skipped `assistant` line, with or without usage,
    when `meta` (a function obj -> a small record, so no parsed line is kept) is given, else []. `counts`
    receives "bad_iterations" (a line whose `usage.iterations` is malformed) and "split_missing" (a part of a
    chosen iterations carrier with no 1-hour split: its cache writes are priced as 5-minute writes). Errors
    are request_parts'."""
    counts = {} if counts is None else counts  # a dict or a Counter: bumped with .get, no collections import
    states, lines = {}, []
    for n, obj, model, info in _assistant_lines(path, skipped, meta is not None):
        key = request_key(obj, n)
        if meta is not None:
            lines.append((n, key, model, meta(obj)))
        if info is None:
            continue
        values, split, carrier, bad = info
        state = states.setdefault(key, {"models": {}, "carrier": None})
        part = state["models"].setdefault(
            model, {"model": model, **{k: 0 for k in REQUEST_USAGE_KEYS}, "cache_creation_1h_tokens": None})
        for k, v in values.items():
            part[k] = max(part[k], v)
        if split is not None:
            part["cache_creation_1h_tokens"] = max(split, part["cache_creation_1h_tokens"] or 0)
        if bad:
            counts["bad_iterations"] = counts.get("bad_iterations", 0) + 1
        state["carrier"] = carrier or state["carrier"]
    requests = []
    for key, state in states.items():
        parts = state["carrier"]
        if parts is None:
            parts = list(state["models"].values())
        else:
            rank = {m: i for i, m in enumerate(state["models"])}  # the models the lines are labelled with come first
            parts = sorted(parts, key=lambda p: rank.get(p["model"], len(rank)))
            missing = sum(1 for p in parts if p["cache_creation_1h_tokens"] is None)
            if missing:
                counts["split_missing"] = counts.get("split_missing", 0) + missing
        requests.append({"key": "%s:%s" % key, "parts": parts})
    return requests, lines


def request_parts(path, skipped=None, counts=None):
    """One record per API request of a worker transcript, in first-seen order: {"key": "<kind>:<id>" (see
    request_key), "parts": [part, ...]}. A part is {"model" (str or None), "input_tokens",
    "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens", "cache_creation_1h_tokens"
    (None = no split known)}. The request is the SUM of its parts, each priced by ITS OWN model; no consumer
    prices the whole request by the first or the last line's model (forge/6 F6-23, t-886).

    THE RULE. (1) When a line of the request carries `usage.iterations` with 2 or more usable entries -- the
    provider's own per-message record, written by a model fallback inside one request -- THAT is the carrier:
    one part per entry (model, usage), the entries' own models and numbers, whatever the lines' `model`
    labels say (the last such line wins; the 1-hour split is the entry's own, a missing one is None and
    counted as "split_missing"). The lines of a fallback request repeat one snapshot under a label that is
    not true (real: five lines all labelled opus-4-8, whose iterations hold a fable-5 message and an
    opus-4-8 message), so the labels cannot be the carrier. (2) Otherwise (no iterations, or one entry --
    every single-model request carries one -- or a malformed one, counted as "bad_iterations") the parts are
    one per MODEL of the lines, each the MAX per field over that model's lines (a request is written as
    several `assistant` lines, one per content block, with growing snapshots: output_tokens 17/17/17/485 in
    the measured case, scout t-794; summing would count a request four times); the 1-hour split is the
    largest KNOWN one. The parts are ordered with the models the lines are labelled with first, in the
    order they appear, then the models only the iterations name.

    Lines that are not `assistant`, or carry a SKIP_MODELS model, or carry no usage dict, join nothing. A
    request whose lines carry no usage at all does not appear; an empty file gives [].

    ERROR DIRECTION: the module raises, the consumer decides (see the module docstring). OSError on an
    unreadable file; ValueError/TypeError on a mistyped usage value (a non-numeric string, a list with
    items), as usage_total does -- unless the consumer passes a list as `skipped`: then a line with a mistyped
    value or a non-object usage is not joined and its line number is appended to the list. Iterations never
    raise. A malformed line is skipped (parse_line)."""
    return read_requests(path, skipped, counts)[0]


def request_usages(path):
    """One usage dict per API request of a worker transcript, in first-seen order: {"key", "input_tokens",
    "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"} -- every field the MAX over ALL
    the parts of the request whatever their model (the sum of tokens, not a price: hop_metrics weighs it).
    A fold of request_parts, the one reader; its errors and its empty cases are request_parts' own."""
    return [{"key": rec["key"], **{k: max(p[k] for p in rec["parts"]) for k in REQUEST_USAGE_KEYS}}
            for rec in request_parts(path)]


def main_transcript_of(worker_path):
    """The main transcript of the session a worker belongs to, as a str: the NEAREST ancestor folder named
    `subagents` (a worker may sit deeper, e.g. subagents/workflows/wf_x/), its parent is the session folder
    <project>/<session>, and the main transcript is <project>/<session>.jsonl. None when the path has no
    `subagents` ancestor. Pure: the file is not looked at (exists or not is the caller's question)."""
    sub = next((a for a in Path(worker_path).parents if a.name == SUBAGENTS), None)
    if sub is None:
        return None
    session = sub.parent
    return str(session.parent / (session.name + ".jsonl"))


def _writer_or_live(writer, path) -> bool:
    """writer(path); True (the file is kept) when the predicate raises."""
    try:
        return bool(writer(path))
    except Exception:
        return True


def content_text(content):
    """The text of a message.content, the ONE reader of it (first_user_text, hop_metrics): a str as is, a list
    of blocks as the "\\n".join of every `text` block (none -> ""; tool_result, image and other blocks are never
    text), anything else None."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b["text"] for b in content
                         if isinstance(b, dict) and b.get("type") == "text" and isinstance(b.get("text"), str))
    return None


def first_user_text(path):
    """The text of the first `type == "user"` line of a worker transcript: the dispatch prompt (the harness
    writes it there; no role or subagent_type field exists anywhere in the file). message.content is read by
    content_text (a str as is; a list of blocks as the join of its text blocks, none -> ""). None when the
    file is empty, no user line exists before EOF (lines that are not JSON objects are skipped), or the
    first user line has no message.content of those two types. Stops at the first user line. Raises OSError."""
    for line in iter_lines(path):
        obj = parse_line(line)
        if obj is None or obj.get("type") != "user":
            continue
        message = obj.get("message")
        return content_text(message.get("content") if isinstance(message, dict) else None)
    return None


def meta_path(transcript_path) -> Path:
    """agent-<id>.jsonl -> agent-<id>.meta.json in the same folder (the sidecar the harness writes at launch)."""
    p = Path(transcript_path)
    return p.with_name(p.stem + ".meta.json")


def read_meta(transcript_path):
    """The sidecar meta of a worker transcript as a dict (keys seen: agentType, description, toolUseId,
    spawnDepth, requestShape, requestNonInteractive); None when it is missing, unreadable, not JSON or not
    an object. Never raises. The ONE json read of the meta in tools/ (permission_audit goes through here)."""
    try:
        obj = json.loads(meta_path(transcript_path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, RecursionError):
        return None
    return obj if isinstance(obj, dict) else None


def agent_type(transcript_path):
    """The worker's kind (the meta's `agentType`: builder, scout, critic, designer, Explore ...) when it is a
    non-empty str; None otherwise (no meta, a bad meta, a missing or non-str field). Never raises."""
    meta = read_meta(transcript_path)
    kind = meta.get("agentType") if meta else None
    return kind if isinstance(kind, str) and kind else None


def is_writer(path, predicate) -> bool:
    """True when the worker is a writing one. The sidecar meta decides "builder" (writer, whatever the
    prompt says: the meta is the stronger carrier). Every other kind -- and an absent or bad meta -- is
    decided by the dispatch prompt: `predicate(first user text)` (injected: this module never knows what
    makes a dispatch a writing one; the dispatch side applies the same predicate, so a reader whose prompt
    carries an owns path is a writer on both sides). When the prompt cannot be found the answer is the
    kind's: a known non-builder kind is a reader, an unknown kind is a writer -- an unknown is counted as a
    writer, the error direction of the parallel cap. Raises OSError (first_user_text); the caller decides."""
    kind = agent_type(path)
    if kind == "builder":
        return True
    text = first_user_text(path)
    if text is None:
        return kind is None
    return bool(predicate(text))


def live_worker_files(session_id, now, window, root=None, writer=None) -> list:
    """Unfinished agent-*.jsonl of a session modified within `window` seconds of `now`, newest first.

    [] for an unsafe or non-string session id. The mtime test runs BEFORE is_finished: a stale file is
    never opened, so it never blocks, and a fresh unreadable file (is_finished raises) is counted live,
    so it never lets one more worker through. A file whose stat raises FileNotFoundError vanished between
    the glob and the stat and is dropped; a stat that fails otherwise (PermissionError ...) counts the
    file live without being read. A glob error or a missing home propagates -- the caller decides.

    `writer`: an optional predicate on a path; when given, an unfinished file is kept only if writer(f) is
    true, and a writer that raises keeps the file (counted live, the same direction as is_finished raising)."""
    if not isinstance(session_id, str) or not AGENT_ID_RE.fullmatch(session_id):
        return []
    base = projects_root() if root is None else root
    found = []
    for folder in base.glob("*/%s/%s" % (session_id, SUBAGENTS)):
        for f in folder.glob("agent-*.jsonl"):
            try:
                mtime = f.stat().st_mtime
            except FileNotFoundError:
                continue
            except OSError:
                found.append((now, f))
                continue
            if now - mtime > window:
                continue
            try:
                done = is_finished(f)
            except Exception:
                done = False
            if not done and (writer is None or _writer_or_live(writer, f)):
                found.append((mtime, f))
    return [f for _m, f in sorted(found, key=lambda t: t[0], reverse=True)]
