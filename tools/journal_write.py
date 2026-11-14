#!/usr/bin/env python3
"""The ONE writer of the journal (offload spec r2, §3.B1; M3): a library (`write_event`, used by the hooks) and a CLI.

    python -B tools/journal_write.py next [--n K]                      reserve K ids (1..20), print them
    python -B tools/journal_write.py delegated --agent A --model M --worker W --notes N [--task t-NNN]
    python -B tools/journal_write.py returned --task t-NNN --worker W
    python -B tools/journal_write.py accept --task t-NNN --agent A --model M --by B --notes N
                                       (--run "<cmd>" | --witness-file <path> | --witness "<text>")
    python -B tools/journal_write.py reject|skip|escalate|defect|decomposable|degraded|restored|calibrated ...
    python -B tools/journal_write.py event --json '<object without ts>'   a rare or retro line
    python -B tools/journal_write.py clone --claim | --show              this clone's letter (registry row)

Each call writes at most ONE line, to `journal_keys.current_path(root)` of the repository holding `--repo` (or the cwd).
Order of one write (POSITIONAL, BL-2): arguments are checked; the witness is produced OUTSIDE the lock (`--run` executes,
`--witness-file` is read); the `journal` machine lock is taken; the journal and the counter are read; the id is issued and
`ts` stamped; `journal_validator` judges the line (a violation writes nothing, exit 2); the line is appended through
`hooklib.append_jsonl_line` and the counter updated; the lock is released; only then the echo and the warnings are made.
The lock is never held across a subprocess, a file read other than the journal / the registry-free counter, or the echo.

Exit codes: 0 written, 2 refused (nothing written; the text names the door), 3 the lock timed out or `--run` timed out.
What the writer prints never echoes a witness or notes (E-B1-16): the outcome line, the validator's own texts, the echo's
WARN lines, and for `--run` one line `run: exit=<rc>`."""
from __future__ import annotations

import argparse
import contextlib
import datetime
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import uuid
from dataclasses import dataclass, field
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import journal_keys as jk  # noqa: E402
import journal_lock  # noqa: E402
import journal_validator as jv  # noqa: E402

REPO = _TOOLS.parent
PACKAGE_SCRIPTS = REPO / "ai-packages" / "qa-factory" / "scripts"

CLI_LOCK_TIMEOUT = 15.0            # seconds; the hooks pass 5
NOTES_MAX = 300                    # CLAUDE.md rule 12
NEXT_MAX = 20
WITNESS_LINES = 40
WITNESS_CHARS = 6000
WITNESS_FILE_MAX = 1 << 20
RUN_TIMEOUT = 600                  # seconds (module constant: a test moves it)
PROBE_TIMEOUT = 30
ID_NUMBER_MAX = 999_999_999
REGISTRY_REL = "logs/journal-letters.json"
COUNTER_NAME = "counter.json"
CLONE_ID_NAME = "clone-id"
ID_GRAMMAR_TEXT = "expected a task id t-NNN (3-9 digits, optional lower-case letter)"
CLAIM_DOOR = "python -B tools/journal_write.py clone --claim"

# data rows (AR-1): the category of an event by the agent that did the work, and of the lead's own events
AGENT_ROWS = {"scout": "recon", "builder": "implementation", "critic": "review", "designer": "spec"}
LEAD_ROWS = {"lead_degraded": "coordination", "lead_restored": "process", "calibrated": "calibration"}
CONTROL_RE = re.compile("[\x00-\x1f\x7f\x85  ]")
WITNESS_CONTROL_RE = re.compile("[\x00-\x08\x0b-\x1f\x7f]")
TASK_IN_JSON_RE = re.compile(r'"task_id"\s*:\s*"(t-[^"]*)"')


class Refused(Exception):
    """A refusal: nothing was written; `code` is the exit code (2 refused, 3 busy / timed out)."""

    def __init__(self, code: int, text: str):
        super().__init__(text)
        self.code = code
        self.text = text


@dataclass
class Result:
    written: bool
    line_no: int = 0
    messages: list = field(default_factory=list)      # lines for stdout (written) or stderr (refused)
    errors: list = field(default_factory=list)        # notes for stderr in any case
    code: int = 0
    task_id: str | None = None
    path: str = ""
    ids: list = field(default_factory=list)


# ---------------------------------------------------------------- small pure helpers

def clean(text, *, keep_newline: bool = False) -> str:
    """Control characters become a space (a witness keeps its tab and line breaks: JSON escapes them, one event stays one
    physical line)."""
    text = text if isinstance(text, str) else str(text)
    if keep_newline:
        return WITNESS_CONTROL_RE.sub(" ", text.replace("\r\n", "\n").replace("\r", "\n"))
    return CONTROL_RE.sub(" ", text)


def cut_witness(text: str, max_lines: int = WITNESS_LINES, max_chars: int = WITNESS_CHARS) -> str:
    """The last `max_lines` lines of `text`, at most `max_chars` characters, cut from the START with `[… N lines cut]`."""
    lines = text.split("\n")
    while lines and lines[-1] == "":
        lines.pop()
    total = len(lines)
    keep = lines[-max_lines:] if total > max_lines else lines

    def render(kept: list) -> str:
        cut = total - len(kept)
        return (f"[… {cut} lines cut]\n" if cut else "") + "\n".join(kept)

    while len(keep) > 1 and len(render(keep)) > max_chars:
        keep = keep[1:]
    out = render(keep)
    if len(out) > max_chars:                       # one giant line: keep its tail, say the whole line's start was cut
        marker = f"[… {total} lines cut]\n"
        out = marker + keep[0][-(max_chars - len(marker)):]
    return out


def fmt_id(number: int, letter: str) -> str:
    return f"t-{number:03d}{letter}"


def _now() -> datetime.datetime:
    return datetime.datetime.now()


def _category(agent, override=None):
    """(category, warn-or-None)."""
    if override:
        return override, None
    if agent in AGENT_ROWS:
        return AGENT_ROWS[agent], None
    return "other", f"agent {str(agent)[:40]!r} has no category row (scout, builder, critic, designer); wrote category 'other'"


# ---------------------------------------------------------------- the repository, the registry, the counter

def repo_root(directory) -> Path:
    try:
        return Path(journal_lock.git_out(Path(directory).resolve(), "rev-parse", "--show-toplevel"))
    except journal_lock.LockError as exc:
        raise Refused(2, f"{exc}; nothing written (a line is never written without the lock)") from None


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_registry(path: Path) -> list:
    """The rows of one logs/journal-letters.json ([] when the file is absent); Refused when it cannot be read."""
    if not path.is_file():
        return []
    try:
        rows = _read_json(path)["letters"]
        if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
            raise ValueError("letters is not a list of objects")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise Refused(2, f"{path} cannot be read ({type(exc).__name__}); nothing written -- restore it from git") from None
    return rows


def dump_registry(rows: list) -> str:
    rows = sorted(rows, key=lambda r: (len(str(r.get("letter", ""))), str(r.get("letter", "")), str(r.get("slug", ""))))
    return '{"letters": [\n' + ",\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + ("\n" if rows else "") + "]}\n"


def worktrees_of(root: Path) -> list:
    """The worktree folders of this clone (`git worktree list --porcelain`), the root first; [root] when git says nothing."""
    try:
        out = journal_lock.git_out(root, "worktree", "list", "--porcelain")
    except journal_lock.LockError:
        return [root]
    paths = [Path(line[len("worktree "):].strip()) for line in out.splitlines() if line.startswith("worktree ")]
    return [p for p in paths if p.is_dir()] or [root]


def clone_id(forge: Path) -> str:
    """The clone's uuid, created once (exclusive create; a reader of a half-written file waits for the writer)."""
    path = forge / CLONE_ID_NAME
    for _attempt in range(80):
        try:
            text = path.read_text(encoding="utf-8").strip()
        except OSError:
            text = ""
        if text:
            return text
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        except FileExistsError:
            import time
            time.sleep(0.025)
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            new = str(uuid.uuid4())
            handle.write(new + "\n")
        return new
    raise Refused(2, f"{path} stays empty; nothing written")


def letter_of(root: Path, forge: Path):
    """(letter, None) for this clone, or (None, reason-with-the-door) when the registry has no row for it."""
    cid = clone_id(forge)
    for row in read_registry(root / REGISTRY_REL):
        if row.get("clone") == cid and isinstance(row.get("letter"), str):
            return row["letter"], None
    return None, (f"this clone has no letter in {REGISTRY_REL} (clone {cid[:8]}); run `{CLAIM_DOOR}`, commit the row, "
                  "then issue ids")


def load_counter(path: Path):
    """(dict, None) | (None, None) when absent | (None, note) when damaged (non-JSON, not an object, a key that is not a
    letter, a value that is not an integer >= 0)."""
    if not path.is_file():
        return None, None
    try:
        data = _read_json(path)
        if not isinstance(data, dict):
            raise ValueError("not an object")
        for key, value in data.items():
            if not (isinstance(key, str) and re.fullmatch(r"[a-z]{0,2}", key)):
                raise ValueError("bad key")
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError("bad value")
        return data, None
    except (OSError, ValueError, TypeError):
        return None, f"{COUNTER_NAME} is damaged; rebuilt from the worktree copies of the journal"


def save_counter(path: Path, counter: dict) -> None:
    tmp = path.with_name(f"{COUNTER_NAME}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(counter, sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def scan_worktrees(root: Path) -> dict:
    """{letter: highest number} over the journal files of EVERY worktree of this clone (first use of the counter, or a
    damaged one -- the safe direction is higher). Outside the lock: it runs a subprocess and reads many files."""
    out: dict = {}
    for wt in worktrees_of(root):
        files = list((wt / jk.JOURNAL_DIR_REL).glob("*.jsonl")) + [wt / jk.HISTORY_REL]
        for path in files:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for match in TASK_IN_JSON_RE.finditer(text):
                parsed = jk.parse_id(match.group(1))
                if parsed is not None:
                    out[parsed[1]] = max(out.get(parsed[1], 0), int(parsed[0]))
    return out


def read_journal(root: Path, rel: str):
    """(text, file_lines, seed_lines) of the logical journal: the file, and the history when the file continues it."""
    path = root / rel
    try:
        text = path.read_bytes().decode("utf-8", errors="replace") if path.exists() else ""
    except OSError as exc:
        raise Refused(2, f"{rel} cannot be read ({type(exc).__name__}); nothing written") from None
    seed: list = []
    if rel != jk.HISTORY_REL and jk.continues_value(text) == jk.HISTORY_REL:
        try:
            hist = root / jk.HISTORY_REL
            seed = jk.split_lines(hist.read_bytes().decode("utf-8", errors="replace")) if hist.exists() else []
        except OSError:
            seed = []
    return text, jk.split_lines(text), seed


def _objs(lines: list) -> list:
    out = []
    for line in lines:
        try:
            obj = json.loads(line)
        except ValueError:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out


def _hooklib():
    if str(PACKAGE_SCRIPTS) not in sys.path:
        sys.path.append(str(PACKAGE_SCRIPTS))            # appended: a package name never shadows a tools module
    import hooklib
    return hooklib


# ---------------------------------------------------------------- the id state shared by `next` and write_event

@dataclass
class _Pre:
    forge: Path
    letter: object
    letter_why: object
    counter_path: Path
    scan: object
    notes: list


def _pre_lock(root: Path, need_counter: bool) -> _Pre:
    forge = journal_lock.lock_dir(root)
    letter, why = letter_of(root, forge) if need_counter else (None, None)
    counter_path = forge / COUNTER_NAME
    scan, notes = None, []
    if need_counter:
        peek, note = load_counter(counter_path)
        if peek is None:
            scan = scan_worktrees(root)
            if note:
                notes.append(note)
    return _Pre(forge, letter, why, counter_path, scan, notes)


def _counter_in_lock(pre: _Pre) -> dict:
    counter, _note = load_counter(pre.counter_path)
    if counter is None:
        if pre.scan is None:
            raise Refused(3, "the id counter changed while this call waited; run it again (nothing written)")
        counter = dict(pre.scan)
    return counter


def _need_letter(pre: _Pre):
    if pre.letter is None:
        raise Refused(2, str(pre.letter_why))
    return pre.letter


def _journal_path(root: Path) -> str:
    rel, why = jk.current_path(root)
    if rel is None:
        raise Refused(2, f"{why}; nothing written")
    return rel


def reserve_ids(root, n: int = 1, *, lock_timeout: float = CLI_LOCK_TIMEOUT) -> Result:
    """`next`: reserve `n` ids (1..20) of this clone's letter and return them; writes no journal line."""
    try:
        if not isinstance(n, int) or isinstance(n, bool) or not 1 <= n <= NEXT_MAX:
            raise Refused(2, f"--n must be a whole number from 1 to {NEXT_MAX}")
        root = Path(root)
        rel = _journal_path(root)
        pre = _pre_lock(root, True)
        letter = _need_letter(pre)
        with journal_lock.machine_lock("journal", lock_timeout, repo=root):
            _text, file_lines, seed = read_journal(root, rel)
            counter = _counter_in_lock(pre)
            fmax = jk.max_by_letter(_objs(seed + file_lines))
            first = max(counter.get(letter, 0), fmax.get(letter, 0)) + 1
            if first + n - 1 > ID_NUMBER_MAX:
                raise Refused(2, f"the id numbers of letter {letter or '(none)'} are used up")
            counter[letter] = first + n - 1
            save_counter(pre.counter_path, counter)
        return Result(True, ids=[fmt_id(first + i, letter) for i in range(n)], errors=pre.notes)
    except Refused as exc:
        return Result(False, code=exc.code, messages=[exc.text])
    except journal_lock.LockBusy as exc:
        return Result(False, code=3, messages=[str(exc) + "; nothing reserved"])
    except journal_lock.LockError as exc:
        return Result(False, code=2, messages=[f"{exc}; nothing reserved"])
    except Exception as exc:  # noqa: BLE001 -- the contract: never raises
        return Result(False, code=2, messages=[f"journal_write failed ({type(exc).__name__}: {str(exc)[:160]}); nothing reserved"])


# ---------------------------------------------------------------- the one write

def write_event(root, obj: dict, *, via: str = "cli", lock_timeout: float = CLI_LOCK_TIMEOUT) -> Result:
    """Write ONE line for `obj` (no `ts`: it is stamped here) under the machine lock. A `delegated` with no `task_id` gets a
    new one from the counter. NEVER raises: any failure is `written=False` with the reason in `messages` and `code`."""
    try:
        return _write_event(Path(root), dict(obj), via, lock_timeout)
    except Refused as exc:
        return Result(False, code=exc.code, messages=[exc.text])
    except journal_lock.LockBusy as exc:
        return Result(False, code=3, messages=[str(exc) + "; nothing written"])
    except journal_lock.LockError as exc:
        return Result(False, code=2, messages=[f"{exc}; nothing written (a line is never written without the lock)"])
    except Exception as exc:  # noqa: BLE001
        return Result(False, code=2, messages=[f"journal_write failed ({type(exc).__name__}: {str(exc)[:160]}); nothing written"])


def _prepare(obj: dict, via: str) -> dict:
    obj.pop("ts", None)
    for key, value in list(obj.items()):
        if isinstance(value, str):
            obj[key] = clean(value, keep_newline=(key == "witness"))
    notes = obj.get("notes")
    if not isinstance(notes, str) or not notes.strip():
        raise Refused(2, "notes are required: one non-empty line saying what happened and why")
    if via == "cli" and len(notes) > NOTES_MAX:
        raise Refused(2, f"notes are at most {NOTES_MAX} characters (CLAUDE.md rule 12); got {len(notes)} -- shorten them, "
                         "the long text goes into a file the notes name")
    obj["via"] = via
    return obj


def _check_new_task(tid, pre: _Pre, counter: dict) -> None:
    """E-B1-2 / E-B1-13: an id given for a NEW task is canonical, carries THIS clone's letter, and was issued."""
    parsed = jk.parse_id(tid)
    if parsed is None:
        raise Refused(2, f"task id {str(tid)[:40]!r}: {ID_GRAMMAR_TEXT}")
    if not jk.is_canonical(tid):
        raise Refused(2, f"{tid} is not canonical (3 digits zero-padded, or 4-9 digits with no leading zero); "
                         f"take one from `{jk.JOURNAL_WRITE_DOOR}`")
    letter = _need_letter(pre)
    if parsed[1] != letter:
        raise Refused(2, f"{tid} carries the letter {parsed[1] or '(none)'!r}, and this clone's letter is {letter or '(none)'!r}; "
                         f"a new task takes an id from `{jk.JOURNAL_WRITE_DOOR}`")
    if int(parsed[0]) > counter.get(letter, 0):
        raise Refused(2, f"{tid} was not issued; take one from `{jk.JOURNAL_WRITE_DOOR}`")


DOOR_TEXT = ("nothing was written; fix what is named above and run the call again (a rare or retro line goes through "
             "`python -B tools/journal_write.py event --json '<object without ts>'`; an `order-known:<ts>` token in its notes "
             "declares a known order defect)")


def _write_event(root: Path, obj: dict, via: str, lock_timeout: float) -> Result:
    obj = _prepare(obj, via)
    rel = _journal_path(root)
    issuing = obj.get("event") == "delegated" and not obj.get("task_id")
    need_counter = issuing or bool(obj.get("task_id"))
    pre = _pre_lock(root, need_counter)
    result = Result(False, errors=list(pre.notes), path=rel)
    with journal_lock.machine_lock("journal", lock_timeout, repo=root):
        text, file_lines, seed = read_journal(root, rel)
        state = seed + file_lines
        counter, dirty = {}, False
        if need_counter:
            counter = _counter_in_lock(pre)
            if issuing:
                letter = _need_letter(pre)
                fmax = jk.max_by_letter(_objs(state))
                number = max(counter.get(letter, 0), fmax.get(letter, 0)) + 1
                if number > ID_NUMBER_MAX:
                    raise Refused(2, f"the id numbers of letter {letter or '(none)'} are used up")
                obj["task_id"] = fmt_id(number, letter)
                counter[letter], dirty = number, True
            else:
                tid = obj["task_id"]
                if not (isinstance(tid, str) and tid in jv.extract_task_ids(state)):
                    _check_new_task(tid, pre, counter)
        now = _now()
        ordered = {"ts": now.isoformat(timespec="seconds")}
        for key in ("event", "agent", "model", "task_id"):      # the order the journal's own lines read in
            if key in obj:
                ordered[key] = obj[key]
        ordered.update(obj)
        line = json.dumps(ordered, ensure_ascii=False, separators=(",", ":"))
        violations = jv.validate_new_lines([line], file_lines, now, seed_lines=seed)
        if violations:
            raise Refused(2, "\n".join(str(v) for v in violations) + "\n" + DOOR_TEXT)
        _hooklib().append_jsonl_line(root / rel, line)
        if dirty:
            save_counter(pre.counter_path, counter)
        line_no = text.count("\n") + (1 if text and not text.endswith("\n") else 0) + 1
    tid = ordered.get("task_id")
    messages = [f"journal: {ordered.get('event')} {tid or '-'} written ({rel}:{line_no})"]
    with contextlib.suppress(Exception):
        messages.extend(jv.feature_warnings([line], file_lines))
        messages.extend(jv.node_warnings([line], file_lines))
    with contextlib.suppress(Exception):
        import journal_echo
        echo = journal_echo.echo_for_lines([line], file_lines)
        if echo:
            messages.append(echo.strip())
    result.written, result.line_no, result.messages, result.task_id = True, line_no, messages, tid
    return result


# ---------------------------------------------------------------- the witness (outside the lock)

def witness_from_file(path_text: str) -> str:
    path = Path(path_text)
    if not path.exists():
        raise Refused(2, f"--witness-file {path_text!r} does not exist; nothing written")
    if not path.is_file():
        raise Refused(2, f"--witness-file {path_text!r} is not a file; nothing written")
    try:
        size = path.stat().st_size
        if size > WITNESS_FILE_MAX:
            raise Refused(2, f"--witness-file is {size} bytes; at most {WITNESS_FILE_MAX} (1 MB) -- pass the tail of it; nothing written")
        raw = path.read_bytes()
    except OSError as exc:
        raise Refused(2, f"--witness-file cannot be read ({type(exc).__name__}); nothing written") from None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise Refused(2, "--witness-file is not UTF-8 text; nothing written -- save the output as UTF-8") from None
    text = clean(text, keep_newline=True)
    if not text.strip():
        raise Refused(2, "--witness-file is empty; nothing written")
    return cut_witness(text)


def _find_bash(root: Path) -> str:
    door = "no bash that sees this repo; run the witness yourself and pass --witness-file <path>"
    bash = shutil.which("bash")
    if not bash:
        raise Refused(2, door)
    try:
        probe = subprocess.run([bash, "-c", "test -f tools/journal_write.py"], cwd=str(root), capture_output=True,
                               timeout=PROBE_TIMEOUT)
    except (OSError, subprocess.SubprocessError):
        raise Refused(2, door) from None
    if probe.returncode != 0:
        raise Refused(2, door)
    return bash


def _kill_tree(proc: subprocess.Popen) -> None:
    with contextlib.suppress(Exception):
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True, timeout=30)
        else:
            os.killpg(proc.pid, signal.SIGKILL)
    with contextlib.suppress(Exception):
        proc.kill()


def run_witness(cmd: str, root: Path, *, allow_red: str | None):
    """(witness, rc) of `cmd` run as `[bash, -c, cmd]` in the repo root; the command is judged first by
    `hygiene_gate.run_allowed`. Refused (2) on the gate's refusal, no bash, or a red run without --allow-red; 3 on timeout."""
    import hygiene_gate
    ok, reasons = hygiene_gate.run_allowed(cmd, str(root))
    if not ok:
        raise Refused(2, "--run refused by the hygiene gate: " + "; ".join(reasons)[:600] +
                         " -- run the command yourself and pass --witness-file <path>")
    bash = _find_bash(root)
    kwargs = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
    proc = subprocess.Popen([bash, "-c", cmd], cwd=str(root), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            stdin=subprocess.DEVNULL, **kwargs)
    try:
        out, _ = proc.communicate(timeout=RUN_TIMEOUT)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        with contextlib.suppress(Exception):
            proc.communicate(timeout=10)
        raise Refused(3, f"--run timed out after {RUN_TIMEOUT} s and was killed; nothing written") from None
    rc = proc.returncode
    print(f"run: exit={rc}")
    if rc != 0 and not allow_red:
        raise Refused(2, "the command exited non-zero, so nothing was written; fix it, or pass --allow-red \"<reason>\" "
                         "to record a red run knowingly")
    body = clean(out.decode("utf-8", errors="replace"), keep_newline=True)
    return f"$ {clean(cmd, keep_newline=True)}\n{cut_witness(body)}\nexit={rc}", rc


# ---------------------------------------------------------------- clone letter

def claim_letter(root: Path, *, lock_timeout: float = CLI_LOCK_TIMEOUT) -> Result:
    slug, why = jk.developer_slug(root)
    if slug is None:
        raise Refused(2, f"{why}; nothing written")
    forge = journal_lock.lock_dir(root)
    cid = clone_id(forge)
    others: list = []
    for wt in worktrees_of(root):                       # outside the lock: subprocess + reads of other registries
        if wt.resolve() != root.resolve():
            others.extend(read_registry(wt / REGISTRY_REL))
    with journal_lock.machine_lock("journal", lock_timeout, repo=root):
        own = read_registry(root / REGISTRY_REL)
        mine = next((r for r in own + others if r.get("clone") == cid), None)
        if mine is not None and mine in own:
            return Result(True, messages=[f"this clone is {slug} with letter {mine['letter'] or '(none)'!r}; nothing to do"])
        if mine is None:
            used = {r.get("letter") for r in own + others if r.get("slug") == slug}
            names = [""] + [chr(c) for c in range(97, 123)] + [a + b for a in map(chr, range(97, 123)) for b in map(chr, range(97, 123))]
            letter = next(n for n in names if n not in used)
            mine = {"letter": letter, "slug": slug, "clone": cid, "since": _now().isoformat(timespec="seconds")}
        path = root / REGISTRY_REL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(dump_registry(own + [mine]), encoding="utf-8", newline="\n")
    return Result(True, messages=[
        f"claimed letter {mine['letter'] or '(none)'!r} for {slug}; commit the row: "
        f"git add {REGISTRY_REL} && git commit -m \"journal letter {mine['letter'] or 'none'} for {slug}\""])


def show_letter(root: Path) -> Result:
    slug, _why = jk.developer_slug(root)
    forge = journal_lock.lock_dir(root)
    letter, why = letter_of(root, forge)
    cid = clone_id(forge)
    if letter is None:
        return Result(True, messages=[f"clone {cid}, slug {slug or '?'}: no letter yet -- {why}"])
    return Result(True, messages=[f"clone {cid}, slug {slug or '?'}, letter {letter or '(none)'!r}"])


# ---------------------------------------------------------------- the CLI

def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--repo", default=None, help="a folder of the repository (default: the cwd)")


def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="journal_write", description=__doc__.split("\n")[0], allow_abbrev=False)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add(name, *, req=(), opt=(), flags=(), **kw):
        p = sub.add_parser(name, allow_abbrev=False, **kw)
        _common(p)
        for a in req:
            p.add_argument(f"--{a}", required=True)
        for a in opt:
            p.add_argument(f"--{a}", default=None)
        for a in flags:
            p.add_argument(f"--{a}", action="store_true")
        return p

    p = add("next", help="reserve K ids and print them")
    p.add_argument("--n", type=int, default=1)
    add("delegated", req=("agent", "model", "worker", "notes"), opt=("task", "node", "feature", "attempt", "replaces", "category"))
    add("returned", req=("task", "worker"), opt=("model", "agent", "category", "notes", "feature"))
    add("accept", req=("task", "agent", "model", "by", "notes"),
        opt=("run", "witness-file", "witness", "basis", "allow-red", "feature", "node", "category"))
    add("reject", req=("task", "agent", "model", "by", "attempt", "failure-class", "notes"), opt=("basis", "feature", "category"))
    add("skip", req=("agent", "notes"), opt=("feature", "category"))
    add("escalate", req=("task", "agent", "model", "notes"), opt=("feature", "category"))
    add("defect", req=("task", "agent", "notes"), opt=("ref", "feature", "category"))
    add("decomposable", req=("agent", "notes"), opt=("task", "feature", "category"))
    add("degraded", req=("notes",), opt=("agent", "model", "reason", "scope", "feature", "category"))
    add("restored", req=("notes",), opt=("agent", "model", "feature", "category"))
    add("calibrated", req=("notes",), opt=("agent", "model", "period", "events-reviewed", "feature", "category"))
    add("event", req=("json",))
    p = add("clone", flags=("claim", "show"))
    return ap


def _int(text, name):
    try:
        return int(text)
    except (TypeError, ValueError):
        raise Refused(2, f"--{name} must be a whole number") from None


def _base(event, agent, notes, category=None, **fields):
    cat, warn = _category(agent, category)
    obj = {"event": event, "agent": agent}
    obj.update({k: v for k, v in fields.items() if v is not None})
    obj["category"] = cat
    obj["notes"] = notes
    return obj, warn


def _lead_obj(event, a, **extra):
    agent = a.agent or "lead"
    obj = {"event": event, "agent": agent}
    if a.model:
        obj["model"] = a.model
    obj["category"] = a.category or LEAD_ROWS[event]
    if a.feature:
        obj["feature"] = a.feature
    obj.update({k: v for k, v in extra.items() if v is not None})
    obj["notes"] = a.notes
    return obj


def _delegated_obj(a) -> tuple:
    notes = a.notes
    if a.replaces:
        notes = f"{notes} replaces_worker:{a.replaces}"
    obj, warn = _base("delegated", a.agent, notes, a.category, model=a.model, task_id=a.task, worker_ref=a.worker,
                      feature=a.feature, node=a.node, attempt=_int(a.attempt, "attempt") if a.attempt is not None else None)
    return obj, warn


def _matching_delegated(root: Path, task: str, worker: str):
    rel = _journal_path(root)
    _text, file_lines, seed = read_journal(root, rel)
    found = None
    for obj in _objs(seed + file_lines):
        if obj.get("event") == "delegated" and obj.get("task_id") == task and obj.get("worker_ref") == worker:
            found = obj
    return found


def _accept_obj(a, root: Path) -> tuple:
    given = [x for x in (a.run, a.witness_file, a.witness) if x is not None]
    witness = witness_by = None
    if len(given) > 1:
        raise Refused(2, "pass exactly one of --run, --witness-file, --witness")
    if a.allow_red and a.run is None:
        raise Refused(2, "--allow-red goes with --run only")
    if a.agent == "builder" and not given:
        raise Refused(2, "accepting a builder needs a witness: exactly one of --run \"<cmd>\", --witness-file <path>, "
                         "--witness \"<text>\"")
    notes = f"{a.notes} allow-red: {a.allow_red}" if a.allow_red else a.notes
    cleaned = clean(notes)
    if not cleaned.strip():
        raise Refused(2, "notes are required: one non-empty line saying what happened and why")
    if len(cleaned) > NOTES_MAX:
        raise Refused(2, f"notes are at most {NOTES_MAX} characters (CLAUDE.md rule 12); got {len(cleaned)}")
    if a.run is not None:                              # POSITIONAL: before the lock
        witness, _rc = run_witness(a.run, root, allow_red=a.allow_red)
        witness_by = "run"
    elif a.witness_file is not None:
        witness, witness_by = witness_from_file(a.witness_file), "file"
    elif a.witness is not None:
        witness, witness_by = clean(a.witness, keep_newline=True), "text"
    obj, warn = _base("accepted", a.agent, notes, a.category, model=a.model, task_id=a.task, by=a.by, basis=a.basis,
                      feature=a.feature, node=a.node, witness=witness, witness_by=witness_by)
    return obj, warn


def _event_from_args(a, root: Path) -> tuple:
    cmd = a.cmd
    if cmd == "delegated":
        return _delegated_obj(a)
    if cmd == "returned":
        match = _matching_delegated(root, a.task, a.worker)
        agent = a.agent or (match or {}).get("agent")
        if not agent:
            raise Refused(2, f"no delegated of {a.task} with worker_ref {a.worker!r} is in the journal, so `returned` has no "
                             "agent to name -- check the task and the worker, or pass --agent for a repair")
        model = a.model or (match or {}).get("model") or ""
        obj, warn = _base("returned", agent, a.notes or "worker returned", a.category or (match or {}).get("category"),
                          model=model or None, task_id=a.task, worker_ref=a.worker, feature=a.feature)
        return obj, warn
    if cmd == "accept":
        return _accept_obj(a, root)
    if cmd == "reject":
        return _base("rejected", a.agent, a.notes, a.category, model=a.model, task_id=a.task, by=a.by, basis=a.basis,
                     attempt=_int(a.attempt, "attempt"), failure_class=a.failure_class, feature=a.feature)
    if cmd == "skip":
        return _base("dispatch_skipped", a.agent, a.notes, a.category, feature=a.feature)
    if cmd == "escalate":
        return _base("escalated", a.agent, a.notes, a.category, model=a.model, task_id=a.task, feature=a.feature)
    if cmd == "defect":
        return _base("defect_found", a.agent, a.notes, a.category, task_id=a.task, ref=a.ref or a.task, feature=a.feature)
    if cmd == "decomposable":
        return _base("decomposable", a.agent, a.notes, a.category, task_id=a.task, feature=a.feature)
    if cmd == "degraded":
        return _lead_obj("lead_degraded", a, reason=a.reason, scope=a.scope), None
    if cmd == "restored":
        return _lead_obj("lead_restored", a), None
    if cmd == "calibrated":
        events = _int(a.events_reviewed, "events-reviewed") if a.events_reviewed is not None else None
        return _lead_obj("calibrated", a, period=a.period, events_reviewed=events), None
    raise Refused(2, f"unknown subcommand {cmd}")


def _json_object(text: str) -> dict:
    try:
        obj = json.loads(text)
    except ValueError as exc:
        raise Refused(2, f"--json is not valid JSON ({exc.__class__.__name__}); nothing written") from None
    if not isinstance(obj, dict):
        raise Refused(2, "--json must be one JSON object; nothing written")
    if "ts" in obj:
        raise Refused(2, "--json must not carry `ts`: the writer stamps it from the system clock; nothing written")
    return obj


def _print_result(res: Result) -> int:
    for note in res.errors:
        print(note, file=sys.stderr)
    for line in res.messages:
        print(line, file=(sys.stdout if res.written else sys.stderr))
    return 0 if res.written else (res.code or 2)


def _utf8_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        with contextlib.suppress(Exception):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main(argv: list | None = None) -> int:
    _utf8_streams()
    a = _build_parser().parse_args(argv)
    try:
        root = repo_root(a.repo or os.getcwd())
        if a.cmd == "next":
            res = reserve_ids(root, a.n)
            if res.written:
                for note in res.errors:
                    print(note, file=sys.stderr)
                for tid in res.ids:
                    print(tid)
                return 0
            return _print_result(res)
        if a.cmd == "clone":
            if a.claim == a.show:
                raise Refused(2, "pass exactly one of --claim, --show")
            return _print_result(claim_letter(root) if a.claim else show_letter(root))
        if a.cmd == "event":
            obj, warn = _json_object(a.json), None
        else:
            obj, warn = _event_from_args(a, root)
        res = write_event(root, obj, via="cli")
        if res.written and warn:
            res.messages.append(f"WARN {warn}")
        return _print_result(res)
    except Refused as exc:
        print(exc.text, file=sys.stderr)
        return exc.code
    except journal_lock.LockBusy as exc:
        print(f"{exc}; nothing written", file=sys.stderr)
        return 3
    except journal_lock.LockError as exc:
        print(f"{exc}; nothing written", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
