"""The dry world (P1-b spec section 4, amendment A1): a project the REAL driver runs in, with a tracker server that answers raw
tracker answers of a story type, snapshots of the world at stage borders, and the spike that measures the road (node N0).

A helper next to the tests, not a test (like `scenario_walk.py`). Nothing here replaces driver code: the driver is the process a live
story runs (`story_run.py --project <world>`), only the executable `claude` is `dry_stub.py` (STORY_RUN_CLAUDE) and the tracker is a
server on localhost that serves the raw answers of `fixtures/stories/dry-<type>/tracker/` (AR-1: the type is a data row, never a
branch on a project name; AR-3: the tracker kind comes from the row, the project's config names the adapter).

    python -B scripts/tests/dry_world.py --spike [--type ID]      the spike: S0..S3, a snapshot, the three probe rows, one printed line

Unknown never becomes a pass (AR-28): a types file that cannot be trusted, a snapshot not made by this process, a route the world
does not hold (404) are each a named refusal or a recorded gap.
"""
import hashlib
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402
import story_run_common as T  # noqa: E402

STORIES = harness.FIXTURES / "stories"
WALK = harness.FIXTURES / "dry-walk"
TYPES_FILE = STORIES / "dry-types.json"
STUB_PATH = HERE / "dry_stub.py"
RUN_LABEL = uuid.uuid4().hex          # the label of THIS process: a snapshot made by another process is not this run's (E16)
PERSON_TOKEN_ENV = {"QA_JIRA_EMAIL": "reader@example.invalid", "QA_JIRA_API_TOKEN": "test-only-token"}
TRACKER_KINDS = ("jira", "local")
GATE = {"continue": (120, 20), "narrow": (300, 60)}   # (S0..S3 seconds, row median seconds) ceilings; above the second: stop (spec F12)
ROW_CAP = 60


class TypesError(ValueError):
    """The type table cannot be trusted: names the file and the id, and what was expected (A1-E4)."""


class SnapshotError(RuntimeError):
    """A snapshot that is missing or not made by this process (E16)."""


# ------------------------------------------------------------------------------------------------ the type table (A1)
def load_types(path=None, base=None) -> tuple:
    """`(types, gaps)` of the table `fixtures/stories/dry-types.json`: the ONE reader of it. An empty or unreadable file, a type
    with no folder, two types with one id, a `default` that is not among the types, a tracker kind or a routes file that does not
    exist: a `TypesError` naming the file and the id. `base` is the folder the types' `input` names live in (the file's own by default)."""
    path = Path(path or TYPES_FILE)
    base = Path(base) if base else path.parent
    name = path.name
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise TypesError(f"{name}: cannot be read ({type(exc).__name__}); expected the table of story types") from None
    if not text.strip():
        raise TypesError(f"{name}: the file is empty; expected an object with `default`, `types` and `gaps`")
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise TypesError(f"{name}: not valid JSON ({' '.join(str(exc).split())}); expected an object with `default`, `types` and `gaps`") from None
    if not isinstance(data, dict) or not isinstance(data.get("types"), list) or not data["types"]:
        raise TypesError(f"{name}: `types` is missing or empty; expected at least one type row")
    gaps = data.get("gaps", [])
    if not isinstance(gaps, list) or not all(isinstance(g, dict) and g.get("id") for g in gaps):
        raise TypesError(f"{name}: `gaps` is not a list of rows with an id")
    seen = set()
    for row in data["types"]:
        tid = row.get("id") if isinstance(row, dict) else None
        if not isinstance(tid, str) or not tid.strip():
            raise TypesError(f"{name}: a type row has no id; expected a non-empty string")
        if tid in seen:
            raise TypesError(f"{name}: two types share the id {tid!r}; expected each id once")
        seen.add(tid)
        for key in ("input", "task"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise TypesError(f"{name}: type {tid!r} has no `{key}`; expected a non-empty string")
        if not (base / row["input"]).is_dir():
            raise TypesError(f"{name}: type {tid!r} names the folder {row['input']!r}, which is not in {base}; expected the type's input folder there")
        tracker = row.get("tracker")
        kind = tracker.get("kind") if isinstance(tracker, dict) else None
        if kind not in TRACKER_KINDS:
            raise TypesError(f"{name}: type {tid!r} tracker kind {kind!r}; expected one of {list(TRACKER_KINDS)}")
        if kind == "jira" and not (base / row["input"] / str(tracker.get("routes") or "")).is_file():
            raise TypesError(f"{name}: type {tid!r} names the routes file {tracker.get('routes')!r}, which is not in {row['input']}")
        check_stub(name, tid, row.get("stub"))
    if data.get("default") not in seen:
        raise TypesError(f"{name}: `default` is {data.get('default')!r}, which is not the id of a type; expected one of {sorted(seen)}")
    return data["types"], gaps


RELEVANCE_VALUES = ("relevant", "not_relevant", "unknown")


def check_stub(name: str, tid: str, stub, what: str = "type") -> None:
    """The declared judgments of a type row or a probe row (`stub`, E-R3; `what` names which): a row without `stub` is `{}`; `stub` is a mapping;
    `source_relevance` is a mapping of ticket key -> `{relevance: relevant|not_relevant|unknown, reason: <non-empty>, from: <non-empty: where the value
    was recorded>}`, a key once (case-folded). A value outside the closed list or with no provenance never reaches the factory (AR-28, AR-29): a
    `TypesError` naming the file, the row and the key."""
    if stub is None:
        return
    if not isinstance(stub, dict):
        raise TypesError(f"{name}: {what} {tid!r} `stub` is not a mapping; expected an object (role controls, `source_relevance`)")
    declared = stub.get("source_relevance")
    if declared is None:
        return
    if not isinstance(declared, dict):
        raise TypesError(f"{name}: {what} {tid!r} `stub.source_relevance` is not a mapping; expected ticket key -> judgment")
    folded = set()
    for key, judgment in declared.items():
        where = f"{what} {tid!r} `stub.source_relevance[{key!r}]`"
        if key.casefold() in folded:
            raise TypesError(f"{name}: {where} repeats a key (case-folded); expected each ticket key once")
        folded.add(key.casefold())
        if not isinstance(judgment, dict):
            raise TypesError(f"{name}: {where} is not a mapping; expected relevance, reason, from")
        if judgment.get("relevance") not in RELEVANCE_VALUES:
            raise TypesError(f"{name}: {where} relevance {judgment.get('relevance')!r}; expected one of {list(RELEVANCE_VALUES)}")
        if not isinstance(judgment.get("reason"), str) or not judgment["reason"].strip():
            raise TypesError(f"{name}: {where} has no `reason`; expected a non-empty sentence")
        if not isinstance(judgment.get("from"), str) or not judgment["from"].strip():
            raise TypesError(f"{name}: {where} has no `from`; expected where the value was recorded (a file and line of a real run)")


def load_rows(path=None) -> list:
    """The probe rows (`seeds/probe.json`), each row's `stub` checked by `check_stub` BEFORE any world is built (E-R3): a bad entry is a `TypesError`
    naming the file, the row id and the key, never a crash of the stub inside a driver turn. A row with no `stub` is unchanged."""
    path = Path(path or WALK / "seeds" / "probe.json")
    try:
        rows = json.loads(path.read_text(encoding="utf-8")).get("rows")
    except (OSError, ValueError, AttributeError) as exc:
        raise TypesError(f"{path.name}: cannot be read as an object with `rows` ({type(exc).__name__})") from None
    if not isinstance(rows, list):
        raise TypesError(f"{path.name}: `rows` is not a list")
    for row in rows:
        if not isinstance(row, dict) or not row.get("id"):
            raise TypesError(f"{path.name}: a row has no id; expected a mapping with `id`")
        check_stub(path.name, row["id"], row.get("stub"), what="row")
    return rows


def merge_stub(base, over) -> dict:
    """The control the stub reads: the type's `stub` overlaid by a row's `stub`, the row winning key by key (one level below the top: a role, a ticket key)."""
    merged = {k: dict(v) if isinstance(v, dict) else v for k, v in (base or {}).items()}
    for key, value in (over or {}).items():
        merged[key] = {**merged[key], **value} if isinstance(merged.get(key), dict) and isinstance(value, dict) else value
    return merged


def type_row(type_id=None, path=None) -> dict:
    types, _gaps = load_types(path)
    wanted = type_id or json.loads(Path(path or TYPES_FILE).read_text(encoding="utf-8"))["default"]
    for row in types:
        if row["id"] == wanted:
            return row
    raise TypesError(f"{Path(path or TYPES_FILE).name}: no type {wanted!r}; expected one of {[r['id'] for r in types]}")


# ------------------------------------------------------------------------------------------------ the tracker server (A1-E8, A1-E9)
class TrackerServer:
    """A tracker on localhost: the first route whose `match` is in the request path answers its file (200), none answers 404 (the world
    holds no such answer: a gap, never an invented one). A repeated request gets the same answer; `log` holds every path and `counts`
    how often (A1-E9)."""

    def __init__(self, routes: list, folder: Path):
        self.routes = [(r["match"], (folder / r["file"]).read_bytes()) for r in routes]
        self.log, self.counts = [], {}
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                owner.log.append(self.path)
                owner.counts[self.path] = owner.counts.get(self.path, 0) + 1
                body = next((b for needle, b in owner.routes if needle in self.path), None)
                if body is None:
                    self.send_response(404)
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *_args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()

    def direct_api(self) -> dict:
        return {"base_url": self.base_url, "api_version": "2", "auth_type": "basic_token", "username_ref": "QA_JIRA_EMAIL",
                "secret_ref": "QA_JIRA_API_TOKEN", "acceptance_criteria_fields": [], "custom_fields": []}

    def summary(self) -> str:
        missing = sorted(p for p in self.counts if not any(n in p for n, _b in self.routes))
        return f"{len(self.log)} requests, {len(self.counts)} distinct, {len(missing)} without a route (404): {missing}"


def mr_diff(row: dict) -> str:
    """The text of the type's merge request diff: the file of the one route row that says `serves: mr_diff` (a raw VCS answer of the snapshot,
    read as bytes so no line ending changes); "" when the type holds none - the caller says so, it never writes a stand-in."""
    folder = (STORIES / row["input"] / row["tracker"]["routes"]).parent
    routes = json.loads((STORIES / row["input"] / row["tracker"]["routes"]).read_text(encoding="utf-8"))["routes"]
    served = [r for r in routes if r.get("serves") == "mr_diff"]
    return (folder / served[0]["file"]).read_bytes().decode("utf-8") if served else ""


def tracker_server(row: dict) -> TrackerServer:
    folder = STORIES / row["input"]
    routes = json.loads((folder / row["tracker"]["routes"]).read_text(encoding="utf-8"))
    return TrackerServer(routes["routes"], (folder / row["tracker"]["routes"]).parent)


# ------------------------------------------------------------------------------------------------ the world
class World:
    def __init__(self, row: dict, root: Path, env: dict, server, snaps: Path):
        self.row, self.root, self.env, self.server, self.snaps = row, Path(root), env, server, snaps
        self.task = row["task"]
        self.task_root = self.root / "qa-factory" / "artifacts" / self.task

    def control(self, stub: dict | None = None) -> None:
        """The stub's own control file (the stub is a process: this file is how a row steers it)."""
        (self.root / "dry-stub-control.json").write_text(json.dumps(
            {"task": self.task, "type": self.row["id"], "stub": merge_stub(self.row.get("stub"), stub)}), encoding="utf-8")

    def close(self) -> None:
        if self.server is not None:
            self.server.stop()
        harness.cleanup(self.root)
        shutil.rmtree(self.snaps, ignore_errors=True)


def build_world(row: dict) -> World:
    """A fresh project whose ticket is read by REST from the type's tracker server: the adapter is the one the row's kind names
    (a config row, AR-3), the probe receipt lets readiness find the tracker proven, `claude` is `dry_stub.py`."""
    kind = row["tracker"]["kind"]
    if kind != "jira":
        raise TypesError(f"type {row['id']!r}: the tracker kind {kind!r} is built by node N3t; node N0 builds `jira`")
    server = tracker_server(row)
    direct = server.direct_api()
    ticket = {"kind": "jira", "method": "agent", "invoke": "jira-assistant", "direct_api": direct}
    root, _task_root, env = T.s0_project(row["task"], config={"adapters": {"ticket": ticket}})
    env.update(PERSON_TOKEN_ENV)
    receipt = root / "qa-factory" / "state" / "integrations" / "jira-direct-probe.json"
    receipt.parent.mkdir(parents=True, exist_ok=True)
    receipt.write_text(json.dumps({
        "status": "available", "checked_at": datetime.now(timezone.utc).isoformat(), "base_url": direct["base_url"],
        "auth_type": direct["auth_type"], "secret_ref": direct["secret_ref"], "username_ref": direct["username_ref"],
        "api_version": direct["api_version"],
        "checks": [{"name": n, "status": "available"} for n in
                   ("authenticated_identity", "sample_issue", "paginated_comments", "attachment_original")]}), encoding="utf-8")
    env.update(STORY_RUN_CLAUDE=str(STUB_PATH), STORY_RUN_CLASS="dry", DRY_STUB_CONTROL=str(root / "dry-stub-control.json"))
    env.pop("STUB_CONTROL", None)
    world = World(row, root, env, server, Path(tempfile.mkdtemp(prefix="qa-dry-snap-")))
    world.control()
    return world


# ------------------------------------------------------------------------------------------------ snapshots (E16)
def _rewrite(root: Path, old: str, new: str) -> None:
    """The copy of a world holds absolute paths of its source (controller.json known_paths, the config): they are the copy's own now."""
    olds = {old.encode("utf-8"): new.encode("utf-8"), old.replace("\\", "\\\\").encode("utf-8"): new.replace("\\", "\\\\").encode("utf-8")}
    for path in root.rglob("*"):
        if ".git" in path.parts or not path.is_file() or path.stat().st_size > 5_000_000:
            continue
        if path.name == "events.jsonl":       # a hash chain: rewriting a path inside an event breaks the chain (`story_step: refused - corrupt event 2`), and the old path in it is only history
            continue
        data = path.read_bytes()
        changed = data
        for a, b in olds.items():
            changed = changed.replace(a, b)
        if changed != data:
            path.write_bytes(changed)


def snapshot(world: World, name: str) -> Path:
    """A byte copy of the world's project, named `<type>/<name>`, marked with this process's label. Lives only in this run's temp
    folder and is never committed (a committed world is a hand-written input)."""
    dest = world.snaps / world.row["id"] / name
    shutil.copytree(world.root, dest, symlinks=True)
    (dest / ".dry-snapshot.json").write_text(json.dumps({"label": RUN_LABEL, "name": name, "type": world.row["id"],
                                                         "from": str(world.root)}), encoding="utf-8")
    return dest


def from_snapshot(world: World, name: str) -> World:
    """A COPY of the snapshot (the snapshot itself never changes) as a world of its own, sharing the tracker server. A missing
    snapshot is a `SnapshotError` the caller turns into `after:<finding>`; one not made by this process is red (E16)."""
    src = world.snaps / world.row["id"] / name
    marker = src / ".dry-snapshot.json"
    if not marker.is_file():
        raise SnapshotError(f"snapshot {world.row['id']}/{name} not found: the main pass did not reach it")
    meta = json.loads(marker.read_text(encoding="utf-8"))
    if meta.get("label") != RUN_LABEL:
        raise SnapshotError(f"snapshot not from this run: {world.row['id']}/{name} carries label {meta.get('label')!r}, this run is {RUN_LABEL!r}")
    root = Path(tempfile.mkdtemp(prefix="qa-dry-row-")) / "project"
    shutil.copytree(src, root, symlinks=True)
    (root / ".dry-snapshot.json").unlink()
    _rewrite(root, meta["from"], str(root))
    env = {k: v.replace(meta["from"], str(root)) if isinstance(v, str) else v for k, v in world.env.items()}
    return World(world.row, root, env, None, world.snaps)


# ------------------------------------------------------------------------------------------------ driving the real driver
class Run:
    def __init__(self, rc, out, seconds, marks):
        self.rc, self.out, self.seconds, self.marks = rc, out, seconds, marks      # marks: [(seconds since start, line)]


def drive(world: World, *args, timeout: int = 900) -> Run:
    """ONE driver process (`story_run.py --project <world>`, as `story_run_common.run_driver`), its lines stamped as they arrive."""
    cmd = [sys.executable, "-B", str(harness.SCRIPTS / "story_run.py"), "--project", str(world.root), "--task", world.task, *map(str, args)]
    env = dict(world.env, PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1")
    started = time.monotonic()
    proc = subprocess.Popen(cmd, cwd=str(world.root), env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            encoding="utf-8", errors="replace")
    marks = []

    def pump():
        for line in proc.stdout:
            marks.append((time.monotonic() - started, line.rstrip("\n")))

    reader = threading.Thread(target=pump, daemon=True)
    reader.start()
    try:
        proc.wait(timeout=timeout)
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        proc.kill()
        rc = -9
        marks.append((time.monotonic() - started, f"dry_world: the driver was killed after {timeout} s"))
    reader.join(5)
    return Run(rc, "\n".join(m[1] for m in marks), time.monotonic() - started, marks)


def pipeline(world: World) -> dict:
    path = world.task_root / "pipeline.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def statuses(world: World) -> dict:
    stages = pipeline(world).get("stages") or {}
    return {s: (stages.get(s) or {}).get("status", "absent") for s in ("S0", "S1", "S2", "S3")}


def jsonl(path: Path) -> list:
    out = []
    for line in (path.read_text(encoding="utf-8").splitlines() if path.is_file() else []):
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def stub_rows(world: World) -> list:
    return jsonl(world.task_root / "state" / "dry-stub.jsonl")


def question_kinds(world: World) -> list:
    return [r.get("kind") for r in jsonl(world.task_root / "state" / "driver-questions.jsonl")]


def stage_seconds(run: Run) -> dict:
    """Seconds per stage from the driver's own progress lines: a stage runs from its first line (`[S1] ...` / `S1: ...`) to the first
    line of the next one; the lines before the first stage line are the driver's start."""
    spans, current, since = {}, "start", 0.0
    for at, line in run.marks:
        found = re.match(r"\[?(S[0-9])\b", line)
        if found and found.group(1) != current:
            spans[current] = spans.get(current, 0.0) + (at - since)
            current, since = found.group(1), at
    spans[current] = spans.get(current, 0.0) + (run.seconds - since)
    return {k: round(v, 1) for k, v in spans.items()}


def first_refusal(text: str) -> str:
    """The first line the driver printed when it sent a role's work back (`resume <dispatch>: <the refusal>`), when a code step of its own refused
    (`review --record failed ...`) or when it stopped (`story_run: stopped ...`), verbatim; "" when it printed none."""
    return next((line for line in text.splitlines() if line.startswith(("resume ", "review --record failed", "story_run: stopped"))), "")


def stage_outcomes(world: World, stop: str = "", refusal: str = "") -> dict:
    """`stage -> one outcome line`: done, or the status with the label that explains it - `live_only` with the reason the stub logged (or the
    question no row answers: `stop`), the first refusal of the driver verbatim, never a red with no name (a red stage is `UNLABELLED RED` and
    the report asks the Lead for the row)."""
    state, rows = statuses(world), stub_rows(world)
    gaps = {}
    for row in rows:
        for item in row.get("live_only") or []:
            gaps.setdefault(row.get("stage") or "?", []).append(f"{item['output']}: {item['why']}")
    out = {}
    stuck = next((s for s in ("S0", "S1", "S2", "S3") if state[s] != "done"), None)
    for stage in ("S0", "S1", "S2", "S3"):
        said = f"; first refusal: {refusal}" if refusal and stage == stuck else ""
        if state[stage] == "done":
            note = f" (live_only: {len(gaps.get(stage, []))} output(s) the filler cannot write)" if gaps.get(stage) else ""
            out[stage] = "done" + note
        elif gaps.get(stage):
            out[stage] = f"{state[stage]} - live_only: " + "; ".join(gaps[stage][:4]) + said
        elif stage == stuck and "has no answer in the probe rows" in stop:
            out[stage] = f"{state[stage]} - live_only: {stop}" + said
        elif state[stage] in ("pending", "absent") and any(state[s] != "done" for s in ("S0", "S1", "S2", "S3") if s < stage):
            out[stage] = "not reached - after an earlier stage that did not close"
        else:
            out[stage] = f"{state[stage]} - UNLABELLED RED (no known_red / not_in_world / live_only row names it)"
    return out


# ------------------------------------------------------------------------------------------------ the probe rows
def run_row(world: World, row: dict) -> dict:
    """One probe row: a COPY of the snapshot `start`, the real driver until it asks, the row's words, one more driver turn."""
    started = time.monotonic()
    try:
        copy = from_snapshot(world, row["start"])
    except SnapshotError as exc:
        return {"id": row["id"], "outcome": f"after: {exc}", "seconds": round(time.monotonic() - started, 1)}
    try:
        copy.control(row.get("stub"))
        first = drive(copy, "--until", "gate_A", "--max-boundaries", "12", timeout=ROW_CAP * 4)
        kinds = question_kinds(copy)
        kind = kinds[-1] if kinds else None
        outcome = f"no question: driver exit {first.rc}, stages {statuses(copy)}"
        if kind and row.get("expect") not in ("any", kind):
            outcome = f"live_only: expected a {row.get('expect')} question, the road meets {kind} first (stub journal: {stub_rows(copy)[-1:]})"
        elif kind:
            words = (row.get("answers") or {}).get(kind)
            if words is None:
                outcome = f"red: no answer for {kind} in type {world.row['id']}"
            else:
                (copy.root / "answer.md").write_bytes(words.encode("utf-8"))
                second = drive(copy, "--answer", str(copy.root / "answer.md"), "--max-boundaries", "1", timeout=ROW_CAP * 4)
                met = "as expected" if row.get("expect") in ("any", kind) else f"expected {row.get('expect')}"
                outcome = f"asked {kind} ({met}); answered; next turn exit {second.rc}"
        return {"id": row["id"], "outcome": outcome, "seconds": round(time.monotonic() - started, 1)}
    finally:
        harness.cleanup(copy.root)


def closed_answers(rows: list) -> dict:
    """`{question kind: the person's words}` the probe rows name (the first row that names a kind): the ONLY words the main pass gives a question
    of the real driver - a closed answer a row holds, never one made up here (A1-E3). A kind no row names stops the road."""
    words: dict = {}
    for row in rows:
        for kind, text in (row.get("answers") or {}).items():
            words.setdefault(kind, text)
    return words


class Road:
    """The main pass S1..S3: one driver process per turn, the real driver's own questions answered with `closed_answers`, until the stage S3 is
    done (the next question is gate A) or the road meets a question no row answers, or the driver ends with no question."""

    def __init__(self):
        self.turns, self.stages, self.seconds, self.stop = [], {}, 0.0, ""
        self.last_out, self.first_refusal = "", ""

    def drive(self, world: World, answers: dict, max_turns: int = 12) -> "Road":
        asked = 0
        for turn in range(max_turns):
            if turn == 0:
                run = drive(world, "--until", "gate_A", "--max-boundaries", "40", timeout=600)
            else:
                run = drive(world, "--answer", str(world.root / "answer.md"), "--until", "gate_A", "--max-boundaries", "40", timeout=600)
            self.seconds += run.seconds
            self.last_out = run.out
            self.first_refusal = self.first_refusal or first_refusal(run.out)
            for name, secs in stage_seconds(run).items():
                self.stages[name] = round(self.stages.get(name, 0.0) + secs, 1)
            kinds = question_kinds(world)
            state = statuses(world)
            self.turns.append({"turn": turn, "rc": run.rc, "seconds": round(run.seconds, 1), "question": kinds[-1] if len(kinds) > asked else None, "stages": state})
            for name in ("S1", "S2", "S3"):
                if state[name] == "done" and not (world.snaps / world.row["id"] / name).is_dir():
                    snapshot(world, name)
            if len(kinds) <= asked:
                self.stop = f"driver exit {run.rc} with no new question"
                break
            asked, kind = len(kinds), kinds[-1]
            if kind == "gate_A" or state["S3"] == "done":
                break
            if kind == "conductor":      # a state the code has no move for: the road ends there and says so (a row may answer the conductor, the main pass does not)
                self.stop = "the road met the conductor: a state the driver has no move for (stub journal and first refusal name it)"
                break
            words = answers.get(kind)
            if words is None:
                self.stop = f"question {kind!r} has no answer in the probe rows (A1-E3): the road stops there"
                break
            (world.root / "answer.md").write_bytes(words.encode("utf-8"))
        else:
            self.stop = f"{max_turns} turns without reaching gate A"
        return self


def gate_verdict(total: float, median: float, worst: float) -> str:
    if total > GATE["narrow"][0] or worst > GATE["narrow"][1]:
        return "stop"
    if total > GATE["continue"][0] or median > GATE["continue"][1]:
        return "narrow"
    return "continue"


def stage_ended(state: dict) -> str:
    """The stage the road ended at (the first not `done`), `S3` when all are done: the last stage that actually ran."""
    return next((s for s in ("S0", "S1", "S2", "S3") if state.get(s) != "done"), "S3")


def row_reached(result: dict) -> bool:
    """True when the row met the question it names AND was answered (`run_row`'s own outcome form); any other outcome measured nothing the gate may count."""
    outcome = str(result.get("outcome", ""))
    return outcome.startswith("asked ") and "(as expected); answered" in outcome


def gate_line(state: dict, outcomes: dict, total: float, median: float, worst: float, results=(), reds=()) -> str:
    """The gate line (AR-28): a numbers verdict only when S3 is `done` AND there is at least one probe row AND every row reached its question AND no
    snapshot is red; otherwise `undecided` naming the first stage or row that fell short (its outcome cut at 160, the stub journal and the row lines hold
    the whole text) and what was measured. A row that never reached its question never counts in a median that decides the gate."""
    if state.get("S3") != "done":
        stuck = stage_ended(state)
        return (f"gate: undecided -- the road ended at {stuck}: {' '.join(str(outcomes.get(stuck, '')).split())[:160]}; "
                f"measured: S0..{stuck} {total:.1f} s, row median {median:.1f} s")
    measured = f"measured: S0..S3 {total:.1f} s, row median {median:.1f} s"
    if not results:
        return f"gate: undecided -- no probe row: the row median has nothing to rest on; {measured}"
    short = next((r for r in results if not row_reached(r)), None)
    if short:
        return f"gate: undecided -- row {short['id']} did not reach its question: {' '.join(str(short.get('outcome', '')).split())[:160]}; {measured}"
    if reds:
        return f"gate: undecided -- {reds[0]}; {measured}"
    return f"gate: {gate_verdict(total, median, worst)} (S0..S3 {total:.1f} s, row median {median:.1f} s, worst row {worst:.1f} s)"


def tree_hash(root: Path) -> str:
    """sha256 over the sorted relative paths and the bytes of every file under `root` (lives only in this run, S-2)."""
    digest = hashlib.sha256()
    root = Path(root)
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def snapshot_red(name: str, before: str, root: Path) -> str:
    """"" when the tree under `root` still has the hash taken before the row `name`, else the red line (E-R8, E16)."""
    return "" if tree_hash(root) == before else f"red: snapshot changed by a row: {name}"


def unused_judgments(declared: dict, rows: list) -> list:
    """The NOTE lines for declared ticket keys the road never ASKED for (E-R2): a stale or mistyped key never vanishes without a line. A key whose command
    was refused was asked for and already has its own `live_only` row (it carries the key), so it gets no note here."""
    asked = {k for r in rows for k in r.get("judged") or []}
    asked |= {i["key"] for r in rows for i in r.get("live_only") or [] if isinstance(i, dict) and i.get("key")}
    return [f"NOTE: unused judgment {key} (the road never asked for a source with that key)" for key in declared if key not in asked]


def tail(text: str, n: int = 40) -> str:
    return "\n".join(text.splitlines()[-n:])


def spike(type_id=None, local_label: str = "") -> int:
    row = type_row(type_id)
    types, gaps = load_types()
    rows = load_rows()          # red before any world is built (E-R3)
    for gap in gaps:
        print(f"NOTE: gap {gap['id']}: {gap['note']} - {gap['why']} (waits {gap['waits']})")
    built = time.monotonic()
    world = build_world(row)
    print(f"world built in {time.monotonic() - built:.1f} s (project {world.root})")
    try:
        s0 = drive(world, "--max-boundaries", "0")
        snap_at = time.monotonic()
        key = None
        try:
            key = json.loads((world.task_root / "work" / "ticket-snapshot.json").read_text(encoding="utf-8")).get("key")
        except (OSError, ValueError):
            pass
        print(f"S0 driver exit {s0.rc} in {s0.seconds:.1f} s; work/ticket-snapshot.json key = {key!r}")
        snapshot(world, "S0")
        snap_seconds = time.monotonic() - snap_at
        road = Road()
        road.drive(world, closed_answers(rows))
        for t in road.turns:
            print(f"turn {t['turn']}: driver exit {t['rc']} in {t['seconds']} s; question {t['question']}; stages {t['stages']}")
        print(f"S1..S3 {road.seconds:.1f} s in {len(road.turns)} driver process(es); seconds per stage {road.stages}; stop: {road.stop or 'none'}")
        outcomes = stage_outcomes(world, road.stop, road.first_refusal)
        starts = {r["start"]: world.snaps / world.row["id"] / r["start"] for r in rows}
        hashes = {name: tree_hash(path) for name, path in starts.items() if path.is_dir()}
        results, reds = [], []
        for r in rows:
            results.append(run_row(world, r))
            if r["start"] in hashes:
                red = snapshot_red(r["id"], hashes[r["start"]], starts[r["start"]])
                if red:
                    reds.append(red)
                    hashes[r["start"]] = tree_hash(starts[r["start"]])
        seconds = [r["seconds"] for r in results]
        median = statistics.median(seconds) if seconds else 0.0
        total = s0.seconds + road.seconds
        print("::group::driver tail (last turn)")
        print(tail(road.last_out, 60))
        print("::endgroup::")
        print("::group::stub log and questions")
        for r in stub_rows(world):
            print(json.dumps(r)[:600])
        print("questions:", question_kinds(world))
        print("::endgroup::")
        for stage, line in outcomes.items():
            print(f"outcome {stage}: {line}")
        for note in unused_judgments((row.get("stub") or {}).get("source_relevance") or {}, stub_rows(world)):
            print(note)
        for r in results:
            print(f"row {r['id']}: {r['seconds']} s - {r['outcome']}")
        for red in reds:
            print(red)
        print(f"tracker: {world.server.summary()}")
        print(f"spike[{row['id']}]: S0..{stage_ended(statuses(world))} {total:.1f} s; snapshot {snap_seconds:.1f} s; row median {median:.1f} s; rows {len(results)}"
              + (f" ({local_label})" if local_label else ""))
        print(gate_line(statuses(world), outcomes, total, median, max(seconds or [0]), results, reds))
        return 1 if reds else 0
    finally:
        world.close()


def main(argv: list) -> int:
    if "--spike" in argv:
        wanted = argv[argv.index("--type") + 1] if "--type" in argv else None
        label = argv[argv.index("--label") + 1] if "--label" in argv else ""
        return spike(wanted, label)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
