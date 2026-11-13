"""How much of a role's work went into fighting the factory's own code (FR-55), measured on every run.

Import-only: no CLI, nothing here writes a file. `retro_numbers.numbers()` calls `story_friction` for
the S9 retro; the development repository's experiment tool (`experiments/measurers/code_friction.py`)
imports `classify`, `turns_of` and `friction` from here so the two never drift apart.

A turn is friction when the tool call the role made came back as one of

  crash      a traceback out of one of our scripts
  stand      a traceback inside a typed `broken_run` result: the STAND failing, not our shape
  guard      a pre-tool guard or hook refusal
  usage      argparse's own dump: twenty lines of flag soup, no form to copy
  validator  a refusal of our own artifact, read only from the head of the result
  adhoc      the role wrote itself a helper script (what the factory failed to give it)
  recovery   a retry of a refused script whose result was not recorded (a retry with a recorded
             result closes the repair and is not friction)

The turn carries its own price from the transcript's usage block, so a friction turn weighs the full
context it had to re-read. That price is the package's own valuation of the turn's `message.model`
(`cost_capture.value_usage`), NOT the CLI's `total_cost_usd` in `driver-runs.jsonl`: the journal
records what the CLI charged, the transcript is priced against the rate catalogue, and the two
disagree (FR-25). A turn the catalogue cannot price is UNPRICED: it counts as a turn, is printed in
the unpriced line, and is left out of every dollar figure, never priced at a fallback (FR-41).

Which spellings count is data: `references/friction-markers.json` (FR-13). Code decides nothing about
what a role's words mean, and never raises into the retro: a measurement that cannot be taken says
`unknown` and why.
"""
import collections
import json
import re
from pathlib import Path

MARKERS_PATH = Path(__file__).resolve().parents[1] / "references" / "friction-markers.json"
_MARKERS_CACHE: dict = {}

# The shape of a script name inside a command line; it is what ties a refusal to the next attempt at
# the same script. A shape, not a vocabulary, so it stays here.
SCRIPT = re.compile(r"([a-z_]+\.py)")


def _bookkeeping_rows(raw):
    """{script name: why} from the `bookkeeping_scripts` rows, or None when the key is absent, is not a
    list, or holds no usable row. Optional on purpose (TEMPORAL): a markers file older than the writer of
    this key has none, and every reader of the older keys keeps working; the reader of THIS key says
    `unknown: no bookkeeping list`, never zero bookkeeping."""
    if not isinstance(raw, list):
        return None
    rows = {str(r["script"]).strip().lower(): str(r.get("why") or "")
            for r in raw if isinstance(r, dict) and isinstance(r.get("script"), str) and r["script"].strip()}
    return rows or None


def load_markers(path=None) -> dict:
    """The marker table, read once per path. A file that is absent or unreadable raises with what is
    expected (FR-1): the retro's wrapper turns that into `unknown` with this text as the reason."""
    key = str(path or MARKERS_PATH)
    if key not in _MARKERS_CACHE:
        try:
            raw = json.loads(Path(key).read_text(encoding="utf-8"))
            markers = {
                "traceback": str(raw["traceback"]).lower(),
                "stand_markers": [str(x) for x in raw["stand_markers"]],
                "guard_markers": [str(x).lower() for x in raw["guard_markers"]],
                "usage_regex": re.compile(raw["usage_regex"]),
                "validator_head_phrases": [str(x).lower() for x in raw["validator_head_phrases"]],
                "validator_head_chars": int(raw["validator_head_chars"]),
                "listing_prefix": str(raw["listing_prefix"]),
                "adhoc_path_regexes": [re.compile(x) for x in raw["adhoc_path_regexes"]],
                "project_test_regex": re.compile(raw["project_test_regex"]),
                "bookkeeping_scripts": _bookkeeping_rows(raw.get("bookkeeping_scripts")),
            }
        except (OSError, ValueError, KeyError, TypeError, re.error) as exc:
            raise ValueError(
                f"friction markers unreadable: {type(exc).__name__}: {exc} - expected the package file "
                f"references/friction-markers.json with the keys traceback, stand_markers, "
                f"guard_markers, usage_regex, validator_head_phrases, validator_head_chars, "
                f"listing_prefix, adhoc_path_regexes, project_test_regex; restore it from the package"
            ) from exc
        _MARKERS_CACHE[key] = markers
    return _MARKERS_CACHE[key]


def classify(text, markers=None):
    """crash / stand / guard / usage / validator, or None for a result that is not friction."""
    m = markers or load_markers()
    t = text or ""
    low = t.lower()
    if m["traceback"] in low:
        # A traceback inside a typed result is the STAND failing, not our shape: run_suite.py already
        # called it `broken_run` and lifted the useful lines into `error_head`. Counting it as a crash
        # of ours sent us looking for a refusal to fix in run_suite.py, where the real defect was a
        # pytest interpreter without the project's dependencies.
        if any(s in t for s in m["stand_markers"]):
            return "stand"
        return "crash"
    if any(s in low for s in m["guard_markers"]):
        return "guard"
    if m["usage_regex"].search(t):
        # argparse's own dump. A hand-written `usage: x.py diff --old <path> --new <path>` is the
        # opposite of friction - it is the form - and counting it inflated the scout's row to 16.
        return "usage"
    # Only the head of the result, and never a numbered file listing: `Read` returns the file's own
    # text, and a reference that happens to contain "refuses" was counted as a validator rejection
    # of it (`Read - validator - 22`: twelve were the plugin guard already counted, four were
    # documents about refusals).
    head = low[:m["validator_head_chars"]]
    if not t.lstrip().startswith(m["listing_prefix"]) and any(
            p in head for p in m["validator_head_phrases"]):
        return "validator"
    return None


def is_project_test(name, markers=None) -> bool:
    """A script name that is the story's own test: a red run of it is the work, not friction with the
    factory. Counted as ours it put 13 events on the automator and the code critic."""
    return bool((markers or load_markers())["project_test_regex"].match(name or ""))


def turns_of(path, price, markers=None):
    """Unique assistant turns with their price and tool calls, plus every tool result by call id.

    `price(model, usage) -> float | None` is injected; `cost` is None for a turn it cannot price. The
    turn is keyed by the assistant message id, so the several transcript lines one streamed message
    leaves count once. Lines that do not parse are skipped, not fatal."""
    msgs, order = {}, []
    results = collections.defaultdict(list)
    by_id = collections.defaultdict(list)     # tool_use id -> its call dicts (a repeated line repeats the call)
    last_ts = None                            # the `timestamp` of the previous user/assistant line
    with Path(path).open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                r = json.loads(line)
            except Exception:
                continue
            if not isinstance(r, dict):
                continue
            before = last_ts
            if r.get("type") in ("assistant", "user"):
                last_ts = r.get("timestamp")
            m = r.get("message") or {}
            if not isinstance(m, dict):
                continue
            if r.get("type") == "assistant":
                u, mid = m.get("usage"), m.get("id")
                if not u or not mid:
                    continue
                if mid not in msgs:
                    # `prev_ts`: the line before this message's first line (the start of its turn window).
                    msgs[mid] = dict(cost=price(m.get("model"), u), calls=[], prev_ts=before)
                    order.append(mid)
                for c in m.get("content") or []:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        i = c.get("input") or {}
                        call = dict(
                            id=c.get("id"), name=c.get("name"),
                            arg=str(i.get("command") or i.get("file_path") or i.get("pattern") or ""),
                            ts=r.get("timestamp"), result_ts=None, has_result=False, is_error=False)
                        msgs[mid]["calls"].append(call)
                        by_id[c.get("id")].append(call)
            elif r.get("type") == "user":
                content = m.get("content")
                for c in content if isinstance(content, list) else []:
                    if isinstance(c, dict) and c.get("type") == "tool_result":
                        txt = c.get("content")
                        if isinstance(txt, list):
                            txt = " ".join(str(x.get("text", "")) for x in txt if isinstance(x, dict))
                        results[c.get("tool_use_id")].append(str(txt or ""))
                        for call in by_id.get(c.get("tool_use_id"), ()):
                            if not call["has_result"]:
                                call["has_result"], call["result_ts"] = True, r.get("timestamp")
                            # the host's structured flag only: absent is not an error
                            call["is_error"] = call["is_error"] or c.get("is_error") is True
    return [dict(msgs[mid], mid=mid) for mid in order], results


def _adhoc(arg, markers) -> bool:
    return any(rx.search(arg) for rx in markers["adhoc_path_regexes"])


def _helper_paths(call, markers) -> list:
    """The paths of a helper script a call wrote or ran: a Write's own file path, or the words of a
    Bash command that an adhoc pattern matches. A Read or a Grep of such a name is counted as adhoc
    (as the experiment always has) but is not a script the role wrote, so it lists nothing."""
    arg = call["arg"] or ""
    if call.get("name") == "Write":
        return [arg] if _adhoc(arg, markers) else []
    if call.get("name") == "Bash":
        words = (w.strip("\"'`;&|()<>") for w in arg.split())
        return [w for w in words if w and _adhoc(w, markers)]
    return []


def friction(path, price, markers=None):
    """One transcript: {turns, cost, fric_turns, fric_cost, tally, money, unpriced, helpers}.

    `cost` and `fric_cost` are priced turns only; an unpriced friction turn is still a friction turn
    and only its dollars are unknown. `helpers` is [{path, call}]: each distinct helper script the role
    wrote or ran, with the tool that named it."""
    m = markers or load_markers()
    rows, results = turns_of(path, price, m)
    tally, money = collections.Counter(), collections.Counter()
    fric_turns, fric_money = 0, 0.0
    unpriced = sum(1 for r in rows if r["cost"] is None)
    open_repairs = {}          # script name -> turns still owed to its repair
    helpers = {}
    for r in rows:
        kinds = set()
        for c in r["calls"]:
            arg = c["arg"] or ""
            if _adhoc(arg, m):
                kinds.add("adhoc")           # a helper the factory failed to provide
                for p in _helper_paths(c, m):
                    helpers.setdefault(p, c.get("name") or "")
            got = results.get(c["id"], [])
            names = set(SCRIPT.findall(arg.lower()))
            bad = None
            for txt in got:
                bad = classify(txt, m) or bad
            if bad:
                kinds.add(bad)
                for n in names:
                    open_repairs[n] = 0
            elif got:
                for n in names & set(open_repairs):
                    open_repairs.pop(n, None)   # this script finally worked
            if not bad and names & set(open_repairs) and not kinds:
                kinds.add("recovery")           # another go at a script that had refused
        if kinds:
            fric_turns += 1
            cost = r["cost"] or 0.0
            fric_money += cost
            for k in kinds:
                tally[k] += 1
                money[k] += cost / len(kinds)
    return dict(turns=len(rows), cost=sum(r["cost"] or 0.0 for r in rows), fric_turns=fric_turns,
                fric_cost=fric_money, tally=tally, money=money, unpriced=unpriced,
                helpers=[dict(path=p, call=c) for p, c in helpers.items()])


REFUSED_UNNAMED = "failed, cause not recorded"

CALL_TIME_METHOD = (
    "Per tool call, from the host transcript's own fields (no reading of result text to decide an error). "
    "Execution seconds: the `tool_use` line's timestamp to its `tool_result` line's timestamp. "
    "Turn-attributed seconds: from the previous user/assistant line to the `tool_result` - what the role "
    "spent on the call, its own model time included; an assistant message that made several calls has its "
    "window (to its last measured result) split evenly among those calls, an even split being a convention. "
    "A call is bookkeeping when a Bash command names, by the shape of a script name, a script of "
    "`bookkeeping_scripts` in references/friction-markers.json. A call is refused/failed when its "
    "`tool_result` carries `is_error: true`, split by `classify` where it names a kind. A refused "
    "bookkeeping call is in both rows. A call with no result, or a line with no readable timestamp, is "
    "counted and its seconds are unknown, never 0.")


def _when(value):
    """A transcript `timestamp` as an aware datetime, or None when it is absent or unreadable."""
    import datetime
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        got = datetime.datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return got if got.tzinfo else got.replace(tzinfo=datetime.timezone.utc)


def _seconds(start, end):
    """Seconds from `start` to `end` (raw timestamps), or None when either is unreadable or the order is
    backwards: an unmeasured span is never 0."""
    a, b = _when(start), _when(end)
    if a is None or b is None or b < a:
        return None
    return (b - a).total_seconds()


def seconds_text(total, unmeasured, calls=None) -> str:
    """A seconds figure as the reports print it: exact, `at least N s (K calls unmeasured)`, or `unknown`."""
    if unmeasured and (calls is None or unmeasured >= calls):
        return f"unknown ({unmeasured} calls unmeasured)"
    if unmeasured:
        return f"at least {total:.1f} s ({unmeasured} calls unmeasured)"
    return f"{total:.1f} s"


def _tally():
    return dict(calls=0, exec_s=0.0, exec_unmeasured=0, turn_s=0.0, turn_unmeasured=0)


def _add(tally, call):
    tally["calls"] += 1
    for key, field in (("exec", "exec_s"), ("turn", "turn_s")):
        if call[field] is None:
            tally[key + "_unmeasured"] += 1
        else:
            tally[key + "_s"] += call[field]


def call_spans(path, markers=None):
    """One transcript's tool calls with their time, and the two rows built on them (T9, T10).

    {calls: [{id, name, script, bookkeeping, is_error, kind, exec_s, turn_s}], bookkeeping: {state, reason,
     + tally}, refused: {calls, by_kind: {kind: tally}, + tally}, method}. A tally is {calls, exec_s,
    exec_unmeasured, turn_s, turn_unmeasured}: the seconds are the MEASURED ones, the unmeasured count says
    how many calls they leave out (print with `seconds_text`). With no bookkeeping list (key absent, not a
    list, or the markers file unreadable) the bookkeeping row is `state: unknown`, never 0 calls."""
    try:
        m = markers or load_markers()
    except ValueError:
        m = None
    book = m["bookkeeping_scripts"] if m else None
    rows, results = turns_of(path, lambda model, usage: None, m)
    calls, seen = [], set()
    for r in rows:
        mine = []
        for c in r["calls"]:
            if c["id"] in seen:                   # the same streamed line read twice
                continue
            seen.add(c["id"])
            mine.append(c)
        ends = [c["result_ts"] for c in mine if c["has_result"] and _when(c["result_ts"]) is not None]
        window = _seconds(r.get("prev_ts"), max(ends, key=_when)) if ends else None
        share = window / len(ends) if window is not None else None
        for c in mine:
            script = next((n for n in SCRIPT.findall(c["arg"].lower()) if book and n in book), None) \
                if c["name"] == "Bash" else None
            kind = None
            if c["is_error"]:
                if m:
                    for txt in results.get(c["id"], []):
                        kind = classify(txt, m) or kind
                kind = kind or REFUSED_UNNAMED
            measured = c["has_result"] and _when(c["result_ts"]) is not None
            calls.append(dict(
                id=c["id"], name=c["name"], script=script, bookkeeping=script is not None,
                is_error=c["is_error"], kind=kind,
                exec_s=_seconds(c["ts"], c["result_ts"]) if c["has_result"] else None,
                turn_s=share if measured else None))
    bookkeeping = dict(_tally(), state="measured" if book else "unknown",
                       reason="" if book else "unknown: no bookkeeping list")
    refused = dict(_tally(), by_kind={})
    for c in calls:
        if book and c["bookkeeping"]:
            _add(bookkeeping, c)
        if c["is_error"]:
            _add(refused, c)
            _add(refused["by_kind"].setdefault(c["kind"], _tally()), c)
    return dict(calls=calls, bookkeeping=bookkeeping, refused=refused, method=CALL_TIME_METHOD)


def package_price(cfg=None):
    """`price(model, usage)` for `turns_of`, valued the way the package values every other request:
    `cost_capture.value_usage` over the turn's own usage block, with the project's rate overrides.

    A turn that used no tokens costs 0 whatever its model says (a `<synthetic>` marker has nothing to
    price). Anything the catalogue cannot price completely - no model, an unknown model, or a rate
    entry without a key the turn uses - is None: unpriced, never a fallback rate (FR-41)."""
    import cost_capture
    cfg = cfg if isinstance(cfg, dict) else {}
    catalogue = cost_capture.load_catalogue()

    def price(model, usage):
        agg = cost_capture.zero()
        cost_capture.add_usage(agg, usage or {})
        if not any(agg[k] for k in ("input", "output", "cache_read", "cache_write_5m", "cache_write_1h")):
            return 0.0
        if not model or not isinstance(model, str):
            return None
        try:
            valuation = cost_capture.value_usage(agg, model, cfg, catalogue,
                                                 cost_capture.model_provider(model))
        except Exception:
            return None
        if valuation.get("pricing_coverage") != "complete":
            return None
        return float(valuation["subtotal_usd"])

    return price


def locate(session_id, state_dir, project_root, home=None):
    """(transcript path or None, where it came from).

    The cost file `state/cost/<session>.json` names its transcript, so it goes first; the host's own
    folder `~/.claude/projects/<project slug>/<session>.jsonl` is the second road. The source is
    printed by the retro so a person can tell a located transcript from a guessed one (FR-27)."""
    sid = str(session_id or "")
    if not sid:
        return None, "no session id"
    try:
        doc = json.loads((Path(state_dir) / "state" / "cost" / f"{sid}.json").read_text(encoding="utf-8"))
        named = doc.get("transcript") if isinstance(doc, dict) else None
    except (OSError, ValueError):
        named = None
    if named and Path(str(named)).is_file():
        return Path(str(named)), "cost file"
    import cost_capture
    base = Path(home) if home is not None else Path.home()
    slugs = [cost_capture.project_slug(project_root), re.sub(r"[^A-Za-z0-9]", "-", str(project_root))]
    tried = []
    for slug in dict.fromkeys(slugs):
        candidate = base / ".claude" / "projects" / slug / f"{sid}.jsonl"
        if candidate.is_file():
            return candidate, "host projects folder"
        tried.append(str(candidate))
    return None, ("not found: the cost file " + ("names " + str(named) if named else "has no transcript")
                  + ", and " + " / ".join(tried) + " is absent")


def _share(value) -> str:
    return f"{value:.1f}%" if isinstance(value, (int, float)) else "unknown"


def section_lines(data, money) -> list:
    """The retro's friction section as markdown lines; `money` is the retro's own dollar formatter.

    Every figure that cannot be computed prints the word `unknown`, never a zero: a story with no
    journal, a role none of whose transcripts could be read, a role with no priced turn (FR-41)."""
    lines = ["", "**Friction with the factory's own code**", ""]
    status = data.get("status") if isinstance(data, dict) else None
    if status not in ("ok", "partial"):
        reason = (data or {}).get("reason") if isinstance(data, dict) else ""
        lines.append("Friction: unknown — " + (str(reason) if reason else
                     "these numbers carry no friction measurement; render them again with the "
                     "current retro_numbers.py"))
        return lines
    if status == "partial":
        lines += [f"Friction: partial — {data.get('reason')}.", ""]
    lines += ["| Role | Turns | Friction turns (share) | Priced $ | Friction $ (share) | Kinds |",
              "|---|---|---|---|---|---|"]
    rows = sorted((data.get("roles") or {}).items())
    for role, row in rows:
        if not row.get("reachable"):
            lines.append(f"| {role} | unknown | unknown | unknown | unknown | "
                         f"none of its {row.get('sessions')} session(s) could be read |")
            continue
        kinds = ", ".join(f"{k}: {n}" for k, n in (row.get("kinds") or {}).items()) or "none"
        lines.append(f"| {role} | {row['turns']} | {row['fric_turns']} ({_share(row['turn_share'])}) | "
                     f"{money(row['priced_cost'])} | {money(row['fric_cost'])} "
                     f"({_share(row['money_share'])}) | {kinds} |")
    total = data.get("total") or {}
    lines.append(f"| all read | {total.get('turns', 0)} | {total.get('fric_turns', 0)} "
                 f"({_share(total.get('turn_share'))}) | {money(total.get('priced_cost'))} | "
                 f"{money(total.get('fric_cost'))} ({_share(total.get('money_share'))}) | |")
    helpers = [f"{role} — {h['path']}" for role, row in rows for h in row.get("helpers") or []]
    lines += ["", "Helper scripts a role wrote for itself: " + ("; ".join(helpers) or "none") + ".",
              "", data.get("method") or METHOD,
              f"Unpriced turns: {data.get('unpriced', 0)} (no catalogue rate for their model; counted "
              "as turns, left out of every dollar figure)."]
    sources = data.get("sources") or {}
    lines.append(f"Sessions read: {data.get('sessions', 0) - data.get('sessions_unreachable', 0)} of "
                 f"{data.get('sessions', 0)}"
                 + (" (" + ", ".join(f"{n} via {k}" for k, n in sorted(sources.items())
                                     if k != "unreachable") + ")" if any(
                     k != "unreachable" for k in sources) else "")
                 + (f"; {data.get('sessions_unreachable')} of {data.get('sessions')} sessions "
                    "unreachable, so the shares above cover the reachable ones only"
                    if data.get("sessions_unreachable") else "") + ".")
    return lines


def _pct(part, whole):
    return round(100.0 * part / whole, 1) if whole else None


METHOD = ("Each turn of a role's own transcript is priced from its usage block by its message.model "
          "through the package's rate catalogue (cost_capture valuation), not from the CLI's "
          "total_cost_usd in the driver journal: the two records differ and this table uses the first "
          "(FR-25). Turn share is friction turns over all turns; dollar share is friction dollars over "
          "priced dollars, so an unpriced turn is in the first and in neither dollar figure. A count "
          "is a candidate, not a finding, until the tool result behind it is read (FR-26).")


def story_friction(task_root, state_dir, project_root, cfg=None, price=None, home=None):
    """Friction per role for the sessions the story's own driver journal names (FR-24).

    {status: ok | partial | unknown, reason, roles: {role: {...}}, total: {...}, sessions,
     sessions_unreachable, unpriced, sources, method}. `unknown` (no journal, no role session, no
     transcript reachable) carries the reason and no figure: an unmeasured story is never 0 %.
     Shares are over the reachable sessions only. A session id read twice (a resume, a repeated row)
     is read once. An unexpected failure raises: the caller turns it into `unknown` with its text."""
    role_of, dispatches, refusal = _role_sessions(task_root, METHOD)
    if refusal:
        return refusal
    markers = load_markers()
    price = price or package_price(cfg)
    roles, sources = {}, collections.Counter()
    for sid, role, measured, source in _walk_sessions(
            role_of, state_dir, project_root, home, lambda p: friction(p, price, markers)):
        row = roles.setdefault(role, dict(
            dispatches=len(dispatches[role]), sessions=0, sessions_unreachable=0, turns=0,
            fric_turns=0, priced_turns=0, priced_cost=0.0, fric_cost=0.0, unpriced=0,
            kinds=collections.Counter(), helpers={}))
        row["sessions"] += 1
        if measured is None:
            _unreachable(row, sources, sid, source)
            continue
        sources[source] += 1
        row["turns"] += measured["turns"]
        row["fric_turns"] += measured["fric_turns"]
        row["priced_turns"] += measured["turns"] - measured["unpriced"]
        row["priced_cost"] += measured["cost"]
        row["fric_cost"] += measured["fric_cost"]
        row["unpriced"] += measured["unpriced"]
        row["kinds"].update(measured["tally"])
        for h in measured["helpers"]:
            row["helpers"].setdefault(h["path"], h["call"])
    total = dict(turns=0, fric_turns=0, priced_turns=0, priced_cost=0.0, fric_cost=0.0, unpriced=0)
    for row in roles.values():
        for key in total:
            total[key] += row[key]
        row["kinds"] = dict(row["kinds"].most_common())
        row["helpers"] = [dict(path=p, call=c) for p, c in row["helpers"].items()]
        row["reachable"] = row["sessions"] - row["sessions_unreachable"]
    for row in list(roles.values()) + [total]:
        row["turn_share"] = _pct(row["fric_turns"], row["turns"])
        row["money_share"] = _pct(row["fric_cost"], row["priced_cost"]) if row["priced_turns"] else None
        row["priced_cost"] = round(row["priced_cost"], 6) if row["priced_turns"] else None
        row["fric_cost"] = round(row["fric_cost"], 6) if row["priced_turns"] else None
    out = {"sessions": len(role_of), "unpriced": total["unpriced"], "roles": roles, "total": total,
           "sources": dict(sources), "method": METHOD}
    return _status(out, roles, len(role_of), "shares")


def _role_sessions(task_root, method):
    """(session -> role, role -> dispatch ids, None) from the story's driver journal, or (None, None, the
    `unknown` answer) when the journal is absent, unreadable or names no role session. The journal is read
    here once for every measurer of a role's transcripts; a session id read twice is read once."""
    journal = Path(task_root) / "state" / "driver-runs.jsonl"
    if not journal.is_file():
        return None, None, {"status": "unknown", "reason": "this story has no driver journal",
                            "method": method}
    role_of, dispatches = {}, collections.defaultdict(set)
    try:
        lines = journal.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return None, None, {"status": "unknown", "reason": f"the driver journal cannot be read ({exc})",
                            "method": method}
    for line in lines:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if not isinstance(row, dict) or row.get("kind") != "role" or not row.get("role") \
                or not row.get("session_id"):
            continue
        sid, role = str(row["session_id"]), str(row["role"])
        role_of.setdefault(sid, role)
        dispatches[role_of[sid]].add(str(row.get("dispatch") or sid))
    if not role_of:
        return None, None, {"status": "unknown", "reason": "the driver journal names no role session",
                            "method": method}
    return role_of, dispatches, None


def _walk_sessions(role_of, state_dir, project_root, home, measure):
    """(session id, role, `measure(transcript path)` or None, source) for each role session: the one loop
    both measurers share. A transcript that cannot be found or opened is None with its reason as source."""
    for sid, role in role_of.items():
        path, source = locate(sid, state_dir, project_root, home=home)
        measured = None
        if path is not None:
            try:
                measured = measure(path)
            except OSError as exc:
                source = f"unreadable: {type(exc).__name__}: {exc}"
        yield sid, role, measured, source


def _unreachable(row, sources, sid, source):
    row["sessions_unreachable"] += 1
    sources["unreachable"] += 1
    # The first real reason per role is kept and printed: "the cost file names X and X is
    # absent" and "unreadable: OSError" tell a person what to look for; a fixed sentence
    # was sometimes false (FR-1, FR-41).
    row.setdefault("unreachable_because", f"session {sid}: {source}")


def _status(out, roles, sessions, covers):
    """`out` with its status: ok, partial (some sessions unreachable) or unknown (none readable)."""
    unreachable = sum(r["sessions_unreachable"] for r in roles.values())
    out = dict(out, sessions_unreachable=unreachable)
    why = "; ".join(f"{role}: {row['unreachable_because']}" for role, row in sorted(roles.items())
                    if row.get("unreachable_because"))
    if unreachable == sessions:
        return dict(out, status="unknown", roles={}, total={},
                    reason=f"none of the {sessions} role session transcripts could be read ({why})")
    if unreachable:
        return dict(out, status="partial",
                    reason=f"{unreachable} of {sessions} sessions unreachable ({why}); {covers} cover "
                           f"the {sessions - unreachable} reachable session(s) only")
    return dict(out, status="ok", reason="")


def story_calls(task_root, state_dir, project_root, cfg=None, home=None):
    """Bookkeeping calls and refused/failed calls per role, count and seconds (T9, T10), for the sessions
    the story's own driver journal names (FR-24), read from the roles' transcripts through `call_spans`.

    {status: ok | partial | unknown | n/a, reason, roles: {role: {sessions, sessions_unreachable, reachable,
     calls, bookkeeping, refused}}, total: {calls, bookkeeping, refused}, sessions, sessions_unreachable,
     sources, method}. `bookkeeping` and `refused` are `call_spans` rows summed over the role's reachable
     sessions (seconds: the measured ones, with their unmeasured count). Every session unreachable and
     every one of them a `stub-` session (the dry-story stub writes no transcript) is `n/a: stub roles`;
     any other unreachable set is `unknown`, as in `story_friction`: never 0 calls, never 0 seconds.
     `cfg` is accepted for the signature of `story_friction`; no price is needed here."""
    role_of, dispatches, refusal = _role_sessions(task_root, CALL_TIME_METHOD)
    if refusal:
        return refusal
    try:
        markers = load_markers()
    except ValueError:
        markers = None                      # call_spans then says `unknown: no bookkeeping list`
    roles, sources = {}, collections.Counter()
    for sid, role, measured, source in _walk_sessions(
            role_of, state_dir, project_root, home, lambda p: call_spans(p, markers)):
        row = roles.setdefault(role, dict(
            dispatches=len(dispatches[role]), sessions=0, sessions_unreachable=0, calls=0,
            bookkeeping=dict(_tally(), state="unknown", reason="unknown: no bookkeeping list"),
            refused=dict(_tally(), by_kind={})))
        row["sessions"] += 1
        if measured is None:
            _unreachable(row, sources, sid, source)
            continue
        sources[source] += 1
        row["calls"] += len(measured["calls"])
        _fold(row, measured)
    total = dict(calls=0, bookkeeping=dict(_tally(), state="unknown", reason="unknown: no bookkeeping list"),
                 refused=dict(_tally(), by_kind={}))
    for row in roles.values():
        row["reachable"] = row["sessions"] - row["sessions_unreachable"]
        total["calls"] += row["calls"]
        _fold(total, row)
    out = {"sessions": len(role_of), "roles": roles, "total": total, "sources": dict(sources),
           "method": CALL_TIME_METHOD}
    if sources.get("unreachable") == len(role_of) and all(s.startswith("stub-") for s in role_of):
        return dict(out, status="n/a", roles={}, total={}, sessions_unreachable=len(role_of),
                    reason="n/a: stub roles (the dry-story stub writes no transcript)")
    return _status(out, roles, len(role_of), "counts")


def _fold(into, part):
    """Add `part`'s bookkeeping and refused rows (a `call_spans` result or a role row) into `into`. The
    bookkeeping state stays `unknown` until a row with a list is folded in."""
    if part["bookkeeping"]["state"] == "measured":
        into["bookkeeping"].update(state="measured", reason="")
        for k in _tally():
            into["bookkeeping"][k] += part["bookkeeping"][k]
    for k in _tally():
        into["refused"][k] += part["refused"][k]
    for kind, tally in part["refused"]["by_kind"].items():
        got = into["refused"]["by_kind"].setdefault(kind, _tally())
        for k in _tally():
            got[k] += tally[k]
