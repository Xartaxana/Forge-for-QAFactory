"""The intake of the COLLECT skill (CL1-6; t-1075 with its §L and §L-2): a `qa-collect-*.zip` sent by a person is UNTRUSTED data. It is
verified without being extracted, its members are stored by sha256 in an inbox OUTSIDE git, its elements are laid out
item -> feature -> pile, and `--apply` writes findings (whole or nothing) and prints the Lead's rows.

    python tools/collect_intake.py <archive.zip>... [--inbox DIR] [--apply] [--place <install8>:<kind>:<id>=<slug|none:why>]... [--archive-max-bytes N]

Plan mode (no `--apply`) writes nothing anywhere. The inbox is `--inbox` or the environment variable QA_COLLECT_INBOX (no config key,
M-7): it must lie outside the repository and outside any git work tree (I2: when git cannot say, the answer is a refusal).
Exit codes: 0 done / plan with nothing for the Lead; 1 a refusal (archive, inbox, index, unknown `--place` key or pile); 2 argparse
only; 3 the Lead is needed (an `unplaced` element, or a pile with no untaken batch). With several archives each one runs to its end
and the worst code wins (1 > 3 > 0).

Why it looks the way it does.
* I1: no string of the archive becomes a file system path. Members are stored as `members/<sha256>`; the inbox folder of an archive
  is `<project_id>/<sha256 of its first part>` with `project_id` checked against `[0-9a-f]{12}`; `collected_at` is checked by form
  and appears only in text. Every name is checked on `ZipInfo.orig_filename` (the raw name: Windows turns `\\` into `/` in `.filename`).
* M-2: a member is read in chunks up to min(its declared bytes, `file_max_bytes`), the whole archive up to `archive_max_bytes`; the
  header size is never believed (a zip bomb stops at the cap).
* I3/I8: the card's zone is read by `piles.parse_zone` only; a text of the archive reaches a finding only as ONE sanitised line inside
  ONE fence that grows with the longest backtick run, and ids built from untrusted names are `[A-Za-z0-9._-]{1,64}` or `h<sha12>`.
* I4: the key of an element holds (project_id, install_id); another installation of the same project is never a duplicate.
* I5/M-4: `ELEMENTS in= placed= unplaced= duplicate= dropped=` (+ `held`, a part of `unplaced`) and a `SOURCES` line counted from the
  manifest independently of the lay-out.
* M-3: with `--apply` the inbox (the evidence store) is ALWAYS written; whole-or-nothing is for the FINDINGS: an archive with an
  `unplaced` element writes none.
* Placement errs only toward `unplaced` (I10): tags are masked, words are off, a bare file name is only a candidate.
"""
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime
import hashlib
import json
import os
import re
import stat
import sys
import unicodedata
import zipfile
import zlib
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import forge_metrics  # noqa: E402
import gitcmd  # noqa: E402
import piles  # noqa: E402
import streams  # noqa: E402

REPO = _TOOLS.parent
# The package is imported AFTER every tools module: `collect_pack` puts the package `scripts/` first on sys.path (m-16), and a name
# the two folders share would then shadow a tools module (test_no_shadow pins that the sets are disjoint).
sys.path.insert(0, str(REPO / "ai-packages" / "qa-factory" / "scripts"))
import collect_pack  # noqa: E402
import collect_stall  # noqa: E402
import machine_facts  # noqa: E402
import project_decisions  # noqa: E402

# ---- seam constants (the limits of the spec; tests move them) ----------------------------------------------------------------
MAX_PARTS = 100                    # parts of one archive, the first included
ARCHIVE_MAX_BYTES = 256 << 20      # all members of one archive together, unpacked (M-2); the spec names a ceiling, not its size
EXCERPT_CHARS = 200
MAX_ELEMENTS_PER_FINDING = 50
MAX_PATHS = 200                    # file tokens of one element
NAME_SHOWN = 80
VALUE_SHOWN = 80
FUTURE_SLACK = datetime.timedelta(days=1)
CHUNK = 1 << 16
ID_RE = re.compile(r"[A-Za-z0-9._-]{1,64}")
FB_ID_RE = re.compile(r"FB-\d{1,6}")
RAEP_ID_RE = re.compile(r"(?:RA|EP)-\d{1,6}")
PROJECT_RE = re.compile(r"[0-9a-f]{12}")
INSTALL_RE = re.compile(r"[0-9a-f]{32}")
SHA_RE = re.compile(r"[0-9a-f]{64}")
COLLECTED_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
SCHEMA_RE = re.compile(r"qa-collect/(\d+)")
PLACE_KEY_RE = re.compile(r"[0-9a-f]{8}:[A-Za-z-]+:[A-Za-z0-9._-]{1,64}")
RETRO_REL_RE = re.compile(r"artifacts/([^/]+)/retro\.md")
RETRO_HEAD = "## What went wrong, and what to do about it"
REQUIRED = ("schema", "project_id", "install_id", "collected_at", "files", "parts")
GIT_VARS = ("GIT_DIR", "GIT_INDEX_FILE", "GIT_WORK_TREE", "GIT_PREFIX", "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY",
            "GIT_CEILING_DIRECTORIES", "GIT_DISCOVERY_ACROSS_FILESYSTEM")      # everything that steers where git looks for a repository (I2, m-5)
ZIP_ERRORS = (zipfile.BadZipFile, zlib.error, EOFError, NotImplementedError, RuntimeError, UnicodeDecodeError, ValueError,
              OverflowError, OSError)
DOOR_SENDER = "ask the sender to collect again with the current plugin"
DOOR_UPDATE = "update tools/ (git pull) or ask the sender for the factory version"
DOOR_INBOX = "pass --inbox <folder outside any git tree> or set QA_COLLECT_INBOX"
LIMITS: dict = {}                  # filled from references/collect-sets.json on first use; tests overwrite single keys
EMPTY_IDENTITIES = {"users": [], "display_names": [], "emails": [], "machine": [], "domain": []}   # m-9: no machine-dependent names


class Refusal(Exception):
    """A refusal in FR-1 form (what is wrong; what was expected; the door). Exit code 1."""


def refuse(what: str, expected: str, door: str) -> Refusal:
    err = Refusal("%s; expected %s; %s" % (what, expected, door))
    err.parts = (what, expected, door)          # kept so a caller can add to `what` and stay in the FR-1 form
    return err


def limits() -> dict:
    if not LIMITS:
        LIMITS.update(collect_pack.load_sets()["limits"])
        LIMITS.setdefault("archive_max_bytes", ARCHIVE_MAX_BYTES)
    return LIMITS


def clean(value, limit: int = 0) -> str:
    """Printable, one line: every non-printable character (control, bidi, U+2028, a lone CR) becomes `?` (m-4: the one sanitizer)."""
    text = piles.printable("absent" if value is None else str(value))
    return text[:limit] if limit else text


def now() -> datetime.datetime:
    return datetime.datetime.now()


# ================================================================================================
# A. verify an untrusted archive without extracting it
# ================================================================================================

def name_problem(name: str):
    """Why a member name is refused (checked on the RAW name), else None. The name never becomes a path; this is the refusal of
    what no honest packer writes. Long, deep and case-twin names are legal (m-1): the packer's own `_arc` allows them."""
    if not name:
        return "an empty name"
    if any(unicodedata.category(c) == "Cc" for c in name):
        return "a control character or NUL in the name"
    if name[0] in "/\\" or re.match(r"[A-Za-z]:", name):
        return "an absolute, drive-letter or UNC name"
    parts = re.split(r"[/\\]", name)
    if ".." in parts:
        return "a `..` segment (zip-slip)"
    if "." in parts or "" in parts:
        return "an empty or `.` segment"
    return None


def info_problem(info: zipfile.ZipInfo):
    mode = info.external_attr >> 16
    if info.is_dir():
        return "a directory entry"
    if stat.S_IFMT(mode) not in (0, stat.S_IFREG):
        return "not a regular file (a link or a device)"
    if info.flag_bits & 0x1:
        return "encrypted"
    if info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
        return "a compression method this intake does not read"
    return name_problem(info.orig_filename)


class _TooBig(Exception):
    """`why` is "member" (over its own cap: no flag helps) or "archive" (over the archive's budget: `--archive-max-bytes` is the door)."""

    def __init__(self, why: str = "member"):
        super().__init__(why)
        self.why = why


def read_capped(zf: zipfile.ZipFile, info: zipfile.ZipInfo, cap: int, budget: list) -> bytes:
    """The member's bytes, read in chunks: more than `cap` bytes, or more than the archive's remaining budget, raises _TooBig. The
    size in the header is never consulted (M-2)."""
    buf = bytearray()
    with zf.open(info) as handle:
        while True:
            chunk = handle.read(CHUNK)
            if not chunk:
                return bytes(buf)
            buf += chunk
            budget[0] -= len(chunk)
            if len(buf) > cap:
                raise _TooBig("member")
            if budget[0] < 0:
                raise _TooBig("archive")


@contextlib.contextmanager
def as_refusal(path):
    try:
        yield
    except Refusal:
        raise
    except ZIP_ERRORS as exc:
        raise refuse("%s is not a valid collect archive (%s)" % (clean(Path(path).name, NAME_SHOWN), type(exc).__name__),
                     "a zip written by the qa-collect skill", DOOR_SENDER) from None


@dataclasses.dataclass
class Member:
    part: Path
    index: int
    sha: str
    size: int
    cap: int
    name: str

    def read(self) -> bytes:
        with as_refusal(self.part), zipfile.ZipFile(self.part) as zf:
            data = read_capped(zf, zf.infolist()[self.index], self.cap, [limits()["archive_max_bytes"]])
        if hashlib.sha256(data).hexdigest() != self.sha:
            raise refuse("the archive changed while it was read (member %s)" % clean(self.name, NAME_SHOWN), "the file as first verified",
                         "run the intake again")
        return data


@dataclasses.dataclass
class Archive:
    path: Path
    sha: str
    manifest: dict
    raw_manifest: bytes
    members: dict
    rows: list
    parts: list
    project_id: str
    install_id: str
    collected_at: str
    stamp: str
    ref_time: object                 # collected_at as the "newer" reference, None when the sender's clock is in the future (m-8)
    transcripts_sent: int
    transcripts_not_sent: int
    unknown_sets: dict
    warnings: list

    @property
    def install8(self) -> str:
        return self.install_id[:8]

    @property
    def identity(self) -> str:
        return "%s-%s-%s" % (self.install8, self.stamp, self.sha[:8])


def part_form():
    prefix = re.escape(collect_pack.load_sets()["archive"]["prefix"])
    return re.compile(r"%s-[0-9a-f]{8}-\d{8}T\d{6}Z(?:-\d+)?(?P<tail>-part\d+|-transcripts(?:-part\d+)?)?\.zip" % prefix)


def parse_manifest(raw: bytes) -> dict:
    try:
        doc = json.loads(raw.decode("utf-8-sig"))
    except (ValueError, RecursionError):
        raise refuse("manifest.json is not JSON (or nests too deep)", "a JSON object", DOOR_SENDER) from None
    if not isinstance(doc, dict):
        raise refuse("manifest.json is not a JSON object", "a JSON object", DOOR_SENDER)
    current = int(SCHEMA_RE.fullmatch(collect_pack.SCHEMA).group(1))
    got = SCHEMA_RE.fullmatch(str(doc.get("schema")))
    if got is None:
        raise refuse("unknown archive schema %s" % clean(doc.get("schema"), NAME_SHOWN), "this intake reads %s" % collect_pack.SCHEMA, DOOR_UPDATE)
    if int(got.group(1)) < current:
        raise refuse("the archive schema %s is older than this intake reads" % clean(doc["schema"]), collect_pack.SCHEMA, DOOR_SENDER)
    if int(got.group(1)) > current:
        raise refuse("unknown archive schema %s" % clean(doc["schema"]), "this intake reads %s" % collect_pack.SCHEMA, DOOR_UPDATE)
    return doc


def _time_of(text):
    return datetime.datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ")


def check_identity(doc: dict) -> tuple:
    """-> (stamp, ref_time, warnings). Every field is checked by FORM before it is used anywhere (M-1)."""
    missing = [k for k in REQUIRED if k not in doc]
    if missing:
        raise refuse("the manifest has no field %s" % ", ".join(missing), "the fields " + ", ".join(REQUIRED), DOOR_SENDER)
    for key, rx in (("project_id", PROJECT_RE), ("install_id", INSTALL_RE), ("collected_at", COLLECTED_RE)):
        if not isinstance(doc[key], str) or not rx.fullmatch(doc[key]):
            raise refuse("manifest field %s is malformed" % key, "the form " + rx.pattern, DOOR_SENDER)
    try:
        when = _time_of(doc["collected_at"])
    except ValueError:
        raise refuse("manifest field collected_at is not a date", "a UTC date like 2026-10-19T12:00:00Z", DOOR_SENDER) from None
    if not isinstance(doc["files"], list) or not isinstance(doc["parts"], list):
        raise refuse("manifest fields files and parts are not lists", "lists", DOOR_SENDER)
    stamp = when.strftime("%Y%m%dT%H%M%SZ")
    if when > datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + FUTURE_SLACK:
        return stamp, None, ["collected_at %s is in the future: the sender's clock is ahead, it is not used as the 'newer' reference" % doc["collected_at"]]
    return stamp, doc["collected_at"], []


def check_rows(rows: list) -> dict:
    """-> {arc: row} for the rows that carry data; every row is checked by form (a malformed row refuses the archive)."""
    by_arc = {}
    for i, row in enumerate(rows):
        ok = isinstance(row, dict) and isinstance(row.get("set"), str) and isinstance(row.get("src_rel"), str) and isinstance(row.get("flags", []), list)
        arc = row.get("arc") if ok else None
        if ok and arc is not None:
            ok = (isinstance(arc, str) and isinstance(row.get("bytes"), int) and not isinstance(row.get("bytes"), bool) and row["bytes"] >= 0
                  and isinstance(row.get("sha256"), str) and SHA_RE.fullmatch(row["sha256"]) is not None and arc not in by_arc)
        if not ok:
            raise refuse("manifest row %d of files[] is malformed or repeats an arc" % i, "set, src_rel, flags, and for data arc/bytes/sha256", DOOR_SENDER)
        if arc is not None:
            by_arc[arc] = row
    return by_arc


def check_parts(doc: dict, first: Path) -> list:
    """-> [(name, row, path)] of the declared parts (names checked by form, not by the first part's name: m-2)."""
    parts, form, seen = doc["parts"], part_form(), set()
    if len(parts) + 1 > MAX_PARTS or doc.get("part_count") != len(parts) + 1:
        raise refuse("part_count %s does not match the %d parts listed (or exceeds %d parts)" % (clean(doc.get("part_count")), len(parts) + 1, MAX_PARTS),
                     "part_count = parts listed + 1, at most %d" % MAX_PARTS, DOOR_SENDER)
    out = []
    for row in parts:
        name = row.get("name") if isinstance(row, dict) else None
        good = (isinstance(name, str) and (m := form.fullmatch(name)) is not None and m.group("tail") and name not in seen
                and isinstance(row.get("sha256"), str) and SHA_RE.fullmatch(row["sha256"]) is not None)
        if not good:
            raise refuse("a part entry of the manifest is malformed (%s)" % clean(name, NAME_SHOWN), "<base>-part<n>.zip or <base>-transcripts[-part<n>].zip, a sha256, kind absent or transcripts", DOOR_SENDER)
        if row.get("kind") not in (None, "transcripts"):         # a well-formed part of a kind this intake does not know: a NEWER packer wrote it (Q2)
            raise refuse("part %s is of the kind %s, which this intake does not read" % (clean(name, NAME_SHOWN), clean(row.get("kind"), NAME_SHOWN)),
                         "kind absent or transcripts", DOOR_UPDATE)
        seen.add(name)
        out.append((name, row, first.with_name(name)))
    return out


def is_transcript(row: dict) -> bool:
    return row.get("set") == "H" and "transcript" in row.get("flags", [])


def verify_part(path: Path, by_arc: dict, members: dict, budget: list, skip_manifest: bool) -> None:
    lim = limits()
    with as_refusal(path), zipfile.ZipFile(path) as zf:
        for index, info in enumerate(zf.infolist()):
            if skip_manifest and index == 0:
                continue
            label = clean(info.orig_filename, NAME_SHOWN)
            why = info_problem(info)
            row = by_arc.get(info.orig_filename)
            if why or info.orig_filename in members or row is None:
                raise refuse("member %s of %s is refused (%s)" % (label, clean(path.name, NAME_SHOWN), why or ("a repeated name" if row else "not listed in the manifest")),
                             "unique, regular, listed members", DOOR_SENDER)
            try:
                data = read_capped(zf, info, min(row["bytes"], lim["file_max_bytes"]), budget)
            except _TooBig as big:
                expected = "at most its declared bytes and %d bytes per file, %d per archive" % (lim["file_max_bytes"], lim["archive_max_bytes"])
                if big.why == "archive":                         # an honest archive of many large files can reach the budget: the flag is the informed pass (FR-4)
                    raise refuse("the members of %s together are larger than the archive ceiling (reached at %s)" % (clean(path.name, NAME_SHOWN), label), expected,
                                 "if the archive is honest, run again with --archive-max-bytes N (now %d); otherwise %s" % (lim["archive_max_bytes"], DOOR_SENDER)) from None
                raise refuse("member %s is larger than the manifest declares (or the ceilings)" % label, expected, DOOR_SENDER) from None
            sha = hashlib.sha256(data).hexdigest()
            if len(data) != row["bytes"] or sha != row["sha256"]:
                raise refuse("member %s does not match its manifest row (size or sha256)" % label, "the bytes the manifest lists", DOOR_SENDER)
            members[info.orig_filename] = Member(path, index, sha, row["bytes"], min(row["bytes"], lim["file_max_bytes"]), info.orig_filename)


def file_sha(path: Path, ceiling: int) -> str:
    h, total = hashlib.sha256(), 0
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            total += len(chunk)
            if total > ceiling:
                break
            h.update(chunk)
    return h.hexdigest()


def open_archive(path) -> Archive:
    """Verify one archive (first part + its parts) WITHOUT extracting. Raises Refusal; touches nothing outside memory."""
    lim, first = limits(), Path(path)
    label = clean(first.name, NAME_SHOWN)
    try:
        size = first.stat().st_size
    except OSError:
        raise refuse("cannot read %s" % label, "an existing archive file", "check the path") from None
    if size > lim["part_max_bytes"]:
        raise refuse("%s is %d bytes, over the part ceiling %d" % (label, size, lim["part_max_bytes"]), "a part of at most %d bytes (packed under another limit?)" % lim["part_max_bytes"], DOOR_SENDER)
    with as_refusal(first), zipfile.ZipFile(first) as zf:
        infos = zf.infolist()
        if not infos or infos[0].orig_filename != "manifest.json":
            raise refuse("%s is not a collect archive (no manifest.json as the first member)" % label, "manifest.json first", DOOR_SENDER)
        try:
            raw = read_capped(zf, infos[0], lim["part_max_bytes"], [lim["part_max_bytes"]])
        except _TooBig:
            raise refuse("manifest.json of %s is larger than a part may be" % label, "at most %d bytes" % lim["part_max_bytes"], DOOR_SENDER) from None
    doc = parse_manifest(raw)
    stamp, ref_time, warnings = check_identity(doc)
    by_arc, parts = check_rows(doc["files"]), check_parts(doc, first)
    members, budget, absent_transcripts = {}, [lim["archive_max_bytes"]], 0
    verify_part(first, by_arc, members, budget, skip_manifest=True)
    for name, row, ppath in parts:
        if not ppath.is_file():
            if row.get("kind") != "transcripts":
                raise refuse("part %s is missing" % clean(name, NAME_SHOWN), "all parts next to the first one", "ask the sender to send every part together")
            absent_transcripts += 1
            continue
        if ppath.stat().st_size > lim["part_max_bytes"] or file_sha(ppath, lim["part_max_bytes"]) != row["sha256"]:
            raise refuse("part %s is over the ceiling or does not hash as the manifest says" % clean(name, NAME_SHOWN), "the part the manifest lists", DOOR_SENDER)
        verify_part(ppath, by_arc, members, budget, skip_manifest=False)
    lost = [r for a, r in by_arc.items() if a not in members]
    real_lost = [r for r in lost if not (is_transcript(r) and absent_transcripts)]     # a deleted transcripts file is the person's choice (Q4), nothing else is
    if real_lost:
        raise refuse("members listed in the manifest are not in the archive (%s)" % clean(real_lost[0]["arc"], NAME_SHOWN), "every listed member in its part", DOOR_SENDER)
    unknown = {}
    for r in doc["files"]:
        if r["set"] not in "ABCDEFGH" or len(r["set"]) != 1:
            unknown[clean(r["set"], 20)] = unknown.get(clean(r["set"], 20), 0) + 1
    sent = sum(1 for r in doc["files"] if is_transcript(r) and r["arc"] in members)
    return Archive(first, file_sha(first, size), doc, raw, members, doc["files"], [p[0] for p in parts], doc["project_id"], doc["install_id"],
                   doc["collected_at"], stamp, ref_time, sent, len(lost), unknown, warnings)


def group_args(paths) -> tuple:
    """-> (first parts to open, [(arg, Refusal)]). An argument that is a later part is absorbed when its first part is among the
    arguments, else refused naming the first part."""
    form, firsts, refusals, args = part_form(), [], [], [Path(p) for p in paths]
    resolved = {os.path.normcase(str(p.resolve())) for p in args if not ((m := form.fullmatch(p.name)) and m.group("tail"))}
    for p in args:
        m = form.fullmatch(p.name)
        if m and m.group("tail"):
            first = p.with_name(p.name[:-len(m.group("tail")) - 4] + ".zip")
            if os.path.normcase(str(first.resolve())) not in resolved:
                refusals.append((p, refuse("%s is not the first part of its archive" % clean(p.name, NAME_SHOWN), "the first part, %s" % clean(first.name, NAME_SHOWN), "give the first part as the argument")))
        elif p.resolve() not in [q.resolve() for q in firsts]:
            firsts.append(p)
    return firsts, refusals


# ================================================================================================
# the inbox and its index
# ================================================================================================

@contextlib.contextmanager
def clean_git_env():
    saved = {k: os.environ.pop(k) for k in GIT_VARS if k in os.environ}
    try:
        yield
    finally:
        os.environ.update(saved)


def inbox_problem(inbox: Path, repo: Path):
    """Why the inbox is refused, else None (I2). Unknown is a refusal, never a pass."""
    real, top = (os.path.normcase(os.path.realpath(p)) for p in (inbox, repo))
    if real == top or real.startswith(top + os.sep):
        return "inside the repository"
    probe = Path(real)
    while not probe.exists() and probe != probe.parent:
        probe = probe.parent
    with clean_git_env():
        code, out, err = gitcmd.git(probe, "rev-parse", "--is-inside-work-tree", "--is-inside-git-dir", stderr=True)
    if code == 0:
        return "inside a git work tree" if b"true" in out.split() else None
    if code == 128 and b"not a git repository" in err.lower():
        return None
    return "git could not say whether it is inside a work tree (%s)" % clean(err.decode("utf-8", "replace").strip(), 80)


def resolve_inbox(arg, repo: Path, apply: bool):
    raw = arg or os.environ.get("QA_COLLECT_INBOX")
    if not raw:
        if apply:
            raise refuse("no inbox is configured", "an inbox folder outside any git tree", DOOR_INBOX)
        return None
    inbox = Path(raw)
    why = inbox_problem(inbox, repo)
    if why:
        raise refuse("the inbox %s is %s" % (clean(inbox), why), "a folder outside the repository and any git work tree", DOOR_INBOX)
    return inbox


EMPTY_INDEX = {"schema": 1, "archives": {}, "elements": {}, "places": {}, "sessions": {}}


def load_index(inbox):
    """-> (index, sha of the file's bytes or None). An index that exists but cannot be read refuses: a rebuilt one would write every
    finding twice and lose every remembered `--place`."""
    if inbox is None:
        return json.loads(json.dumps(EMPTY_INDEX)), None
    path = Path(inbox) / "index.json"
    if not path.exists():
        return json.loads(json.dumps(EMPTY_INDEX)), None
    try:
        raw = path.read_bytes()
        doc = json.loads(raw.decode("utf-8"))
        if not isinstance(doc, dict) or not all(isinstance(doc.get(k), dict) for k in EMPTY_INDEX if k != "schema"):
            raise ValueError("shape")
    except (OSError, ValueError, RecursionError):
        raise refuse("the inbox index %s cannot be read" % clean(path), "a JSON index written by this intake", "restore it from a copy; it is never rebuilt (a rebuilt one writes every finding twice)") from None
    return doc, hashlib.sha256(raw).hexdigest()


def check_index_unchanged(inbox: Path, expected_sha) -> None:
    """Refuse when the index is no longer the bytes this run read at its start (a parallel run). It runs BEFORE the findings are written,
    so that the refusal's word 'not kept' is true without any rollback (the second call in `save_index` guards the gap that is left)."""
    path = inbox / "index.json"
    try:
        current = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    except OSError as exc:
        raise refuse("the inbox index %s cannot be read (%s)" % (clean(path), clean(exc, 120)), "a readable index", "check the inbox folder, then run the intake again") from None
    if current != expected_sha:
        raise refuse("the inbox index changed during the run", "the index as it was read at the start", "run the intake again; no finding of this archive is kept")


def save_index(inbox: Path, index: dict, expected_sha) -> str:
    check_index_unchanged(inbox, expected_sha)
    raw = json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    piles.write_bytes_atomic(inbox / "index.json", raw)
    return hashlib.sha256(raw).hexdigest()


def drop_findings(repo: Path, written: list, cause: Exception) -> Refusal:
    """The index could not be saved AFTER this archive's findings were written: remove them (best effort) and return the refusal to raise,
    in the FR-1 form, naming the files. The invariant: after a refusal of this run no finding of the archive stays (or the refusal says which)."""
    left = []
    for path in written:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            left.append(path)
    names = lambda paths: ", ".join(clean(p.relative_to(repo).as_posix(), 120) for p in paths)
    if isinstance(cause, Refusal):
        what, expected, door = getattr(cause, "parts", (str(cause), "an unchanged index", "run the intake again"))
    else:
        what, expected, door = ("the inbox index could not be saved (%s)" % clean(cause, 120), "a writable inbox folder",
                                "free space or fix the permissions of the inbox, then run the intake again")
    if left:
        what += "; the findings of this archive written in this run could NOT be removed, delete them by hand: " + names(left)
    if written and len(left) < len(written):
        what += "; removed again: " + names([p for p in written if p not in left])
    return refuse(what, expected, door)


FOLDER_HEX = 24     # hex digits of the archive sha in its folder name: the full sha keeps the Windows 260-character path limit out of reach


def archive_dir(inbox: Path, arc: Archive) -> Path:
    return inbox / arc.project_id / arc.sha[:FOLDER_HEX]


def write_inbox(inbox: Path, arc: Archive, elements: list) -> None:
    """The evidence store of an archive: members by sha, their table, the manifest, the full texts of the elements (M-3)."""
    base = archive_dir(inbox, arc)
    table, by_arc = {}, {r["arc"]: r for r in arc.rows if r.get("arc")}
    for name, m in arc.members.items():
        target = base / "members" / m.sha
        if not target.exists():
            piles.write_bytes_atomic(target, m.read())
        row = by_arc[name]
        table[name] = {"sha256": m.sha, "bytes": m.size, "src_rel": row["src_rel"], "set": row["set"], "flags": row.get("flags", [])}
    piles.write_bytes_atomic(base / "members.json", json.dumps(table, ensure_ascii=False, indent=1).encode("utf-8"))
    piles.write_bytes_atomic(base / "manifest.json", arc.raw_manifest)
    texts = {e["pkey"]: {"kind": e["kind"], "id": e["id"], "status": e["status"], "held": e["held"], "place": e["place"], "text": e["text"]} for e in elements}
    piles.write_bytes_atomic(base / "elements.json", json.dumps(texts, ensure_ascii=False, indent=1).encode("utf-8"))


# ================================================================================================
# D. elements
# ================================================================================================

def sha12(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()[:12]


def safe_id(raw, rx=ID_RE) -> str:
    """An element id from an untrusted string: the string when it fits the charset, else `h<sha12>` (M-6)."""
    raw = str(raw)
    return raw if rx.fullmatch(raw) else "h" + sha12(raw)


_redactor = []


def redactor():
    """The second line (I7): the package's rules, compiled with an EMPTY identity shape so the held set never depends on this machine (m-9)."""
    if not _redactor:
        _redactor.append(machine_facts.compile_redactor(machine_facts.load_rules(), identities=EMPTY_IDENTITIES))
    return _redactor[0]


def residue_category(text: str):
    """The category of the first leak the package's finder sees in `text`, read as the packer's own post-check reads a text member
    (`residue_document`, kind text: line by line), else None."""
    found = redactor().residue_document(text, "text", _first=True)
    return found[0]["category"] if found else None


def make_element(arc: Archive, kind: str, raw_id, text: str, origin: str, csha_text=None, state=None, rx=ID_RE) -> dict:
    ident = safe_id(raw_id, rx)
    return {"kind": kind, "id": ident, "key": "%s/%s/%s/%s" % (arc.project_id, arc.install_id, kind, ident), "pkey": "%s:%s:%s" % (arc.install8, kind, ident),
            "text": text, "csha": hashlib.sha256((csha_text if csha_text is not None else text).encode("utf-8", "replace")).hexdigest(), "state": state,
            "origin": origin, "held": residue_category(text), "status": "new", "place": None, "why": "", "candidates": []}


def member_text(arc: Archive, name) -> str:
    return arc.members[name].read().decode("utf-8", "replace")


def row_with(arc: Archive, set_: str, rel: str):
    return next((r for r in arc.rows if r["set"] == set_ and r["src_rel"] == rel and r.get("arc") in arc.members), None)


def fb_rows(arc: Archive) -> list:
    """The FB rows: the D2 projection when the archive has it (and it parses), else the D1 table through the package's own reader."""
    d2 = row_with(arc, "D", "records/project-decisions.json")
    if d2:
        try:
            found = json.loads(member_text(arc, d2["arc"])).get("findings")
        except (ValueError, RecursionError, AttributeError):
            found = None
        if isinstance(found, list):
            return [r for r in found if isinstance(r, dict)]
    d1 = row_with(arc, "D", "factory-backlog.md")
    return project_decisions.parse_findings(member_text(arc, d1["arc"])) if d1 else []


def fb_element(arc: Archive, row: dict) -> dict:
    cols = ("essence", "scope", "witness/details", "status", "decision", "created")
    text = "\n".join("%s: %s" % (c, row.get(c, "")) for c in cols) if any(row.get(c) for c in cols) else "(empty)"
    witness = str(row.get("witness/details", ""))
    kind = "adaptation" if "change-request:" in witness or ":human-feedback" in witness else "FB"
    body = "|".join(str(row.get(c, "")) for c in cols[:3])
    return make_element(arc, kind, row.get("id", ""), text, "fb", body, [str(row.get("status", "")), str(row.get("decision", ""))], FB_ID_RE)


def ra_ep_elements(arc: Archive) -> list:
    out = []
    for rel in ("records/report-adaptations.json", "records/environment-properties.json"):
        row = row_with(arc, "D", rel)
        try:
            doc = json.loads(member_text(arc, row["arc"])) if row else None
        except (ValueError, RecursionError):
            doc = None
        stack = [doc]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                if RAEP_ID_RE.fullmatch(str(node.get("id", ""))):
                    out.append(make_element(arc, "adaptation", node["id"], json.dumps(node, ensure_ascii=False, sort_keys=True), "ra_ep", rx=RAEP_ID_RE))
                stack += [v for v in node.values() if isinstance(v, (dict, list))]
            elif isinstance(node, list):
                stack += [v for v in node if isinstance(v, (dict, list))]
    return out


def retro_sections(arc: Archive) -> tuple:
    """-> (elements, number of retro files without the section). One element per history."""
    elements, without = [], 0
    for row in arc.rows:
        m = RETRO_REL_RE.fullmatch(row["src_rel"]) if row["set"] == "F" and row.get("arc") in arc.members else None
        if not m:
            continue
        lines, take, got = member_text(arc, row["arc"]).split("\n"), False, []
        for line in lines:
            if line.startswith("## "):
                take = line.strip() == RETRO_HEAD
                continue
            if take:
                got.append(line)
        if not any(line.strip() == RETRO_HEAD for line in lines):
            without += 1
        else:
            elements.append(make_element(arc, "retro", m.group(1), "\n".join(got).strip() or "(empty)", "retro"))
    return elements, without


def stall_laid_out(story) -> bool:
    """A story is laid out when it stalled or its stall is unknown, or it looped or its looping is unknown (CL3-9). The ONE predicate of
    `stall_elements` and `count_sources`. An archive of an older packer has no `looped` key: read as not looped (collect_stall.loop_state)."""
    return isinstance(story, dict) and collect_stall.loop_state(story) != (collect_stall.NO, collect_stall.NO)


def stall_elements(arc: Archive) -> list:
    out = []
    for story in arc.manifest.get("stories") if isinstance(arc.manifest.get("stories"), list) else []:
        if not stall_laid_out(story):
            continue
        stall, loop = collect_stall.loop_state(story)

        def ignored_lines(label, key):
            """The ignored list of the story under `key`: absent or empty prints nothing, a non-list is named, a list is counted and listed."""
            got = story.get(key)
            if key not in story or got == []:
                return []
            if not isinstance(got, list):
                return ["%s: unreadable (%s)" % (label, type(got).__name__)]
            entries = [e for e in got if isinstance(e, dict)]
            return ["%s: %d" % (label, len(entries))] + ["%s | %s" % (e.get("where"), e.get("why")) for e in entries]

        signals = story.get("stall_signals") if isinstance(story.get("stall_signals"), list) else []
        lines = ["stalled: " + stall] + ["%s | %s | %s" % (s.get("id"), s.get("where"), s.get("at")) for s in signals if isinstance(s, dict)]
        lines += ignored_lines("ignored", "ignored")
        if "looped" in story:
            loops = story.get("loop_signals") if isinstance(story.get("loop_signals"), list) else []
            lines += ["looped: " + loop] + ["%s | %s | %s" % (s.get("id"), s.get("where"), s.get("at")) for s in loops if isinstance(s, dict)]
            lines += ignored_lines("loop ignored", "loop_ignored")
        out.append(make_element(arc, "stall", story.get("task", ""), "\n".join(lines), "stall"))
    return out


def answer_elements(arc: Archive) -> list:
    out, answers = [], arc.manifest.get("answers")
    for kind in ("problems", "suggestions"):
        a = answers.get(kind) if isinstance(answers, dict) else None
        if isinstance(a, dict) and a.get("state") == "answered":
            text = member_text(arc, a["arc"]) if a.get("arc") in arc.members else "(the answer text is not in the archive)"
            out.append(make_element(arc, "answer-" + kind, sha12(text), text, "answer"))
    return out


def numbers_element(arc: Archive, index: dict):
    rows = [r for r in arc.rows if r["set"] in ("C", "G") and r.get("arc") in arc.members]
    if not rows:
        return None
    seen, new = index.get("sessions", {}), []
    for r in rows:
        if r["src_rel"].startswith("state/cost/"):
            try:
                sid = json.loads(member_text(arc, r["arc"])).get("session_id")
            except (ValueError, RecursionError, AttributeError):
                sid = None
            if isinstance(sid, str):
                new.append(sid)
    fresh = [s for s in new if "%s/%s/%s" % (arc.project_id, arc.install_id, s) not in seen]
    lines = ["C rows: %d, G rows: %d" % (sum(r["set"] == "C" for r in rows), sum(r["set"] == "G" for r in rows)), "sessions: %d new, %d seen" % (len(fresh), len(new) - len(fresh))]
    lines += ["session %s" % clean(s, 80) for s in sorted(set(fresh))] + ["file %s" % clean(r["src_rel"], 120) for r in rows]
    el = make_element(arc, "numbers", "n" + sha12(arc.sha), "\n".join(lines), "numbers")
    el["sessions"] = sorted(set(fresh))
    return el


def build_elements(arc: Archive, index: dict) -> list:
    elements = [fb_element(arc, r) for r in fb_rows(arc)] + ra_ep_elements(arc)
    elements += retro_sections(arc)[0] + stall_elements(arc) + answer_elements(arc)
    num = numbers_element(arc, index)
    return unique(elements + ([num] if num else []))


def unique(elements: list) -> list:
    """Two elements of one archive may not share a key (the evidence file is keyed by it): the same text twice is a repeat, another
    text under the same id gets an id of its own text."""
    seen = {}
    for el in elements:
        again = seen.get(el["key"])
        if again is None:
            seen[el["key"]] = el
        elif again["csha"] == el["csha"]:
            el["status"], el["why"] = "duplicate", "repeated in this archive"
            el["key"] += "#%d" % len(seen)
            el["pkey"] += "#%d" % len(seen)
            seen[el["key"]] = el
        else:
            el["id"] = "h" + el["csha"][:12]
            el["key"] = el["key"].rsplit("/", 1)[0] + "/" + el["id"]
            el["pkey"] = el["pkey"].rsplit(":", 1)[0] + ":" + el["id"]
            seen[el["key"]] = el
    return elements


FB_LINE_RE = re.compile(r"^\s*\|\s*FB-\d+\b", re.IGNORECASE | re.MULTILINE)
D2_REL, D1_REL = "records/project-decisions.json", "factory-backlog.md"
RAEP_RELS = ("records/report-adaptations.json", "records/environment-properties.json")


def raw_fb_count(arc: Archive) -> tuple:
    """-> (rows the archive carries, rows that are not objects, WARN lines). The RAW list, not the filtered one the elements come from
    (M-4, axis 6: a measure is never its own sample): every `findings` row of D2 of any type; D2 present but unusable falls to D1 (as
    `fb_rows` does) and says so; D1 is counted as its `| FB-n` lines."""
    d2, warns = row_with(arc, "D", D2_REL), []
    if d2:
        try:
            doc = json.loads(member_text(arc, d2["arc"]))
            found = doc.get("findings") if isinstance(doc, dict) else None
        except (ValueError, RecursionError):
            found = None
        if isinstance(found, list):
            bad = sum(1 for r in found if not isinstance(r, dict))
            if bad:
                warns.append("D2 (%s) has %d findings row(s) that are not objects: counted as sources, unreadable, no element is made of them" % (D2_REL, bad))
            return len(found), bad, warns
        warns.append("D2 present, unreadable (%s is not JSON or has no findings list): the findings are counted from D1" % D2_REL)
    d1 = row_with(arc, "D", D1_REL)
    return (len(FB_LINE_RE.findall(member_text(arc, d1["arc"]))) if d1 else 0), 0, warns


def raw_raep_count(arc: Archive) -> tuple:
    """-> (records whose id has the form RA|EP-n, WARN lines): the records are the objects in the lists of the record files, found
    without the walker of `ra_ep_elements`; a record whose id is outside the form gets no element and is named, never silent."""
    count, warns = 0, []
    for rel in RAEP_RELS:
        row = row_with(arc, "D", rel)
        if not row:
            continue
        try:
            doc = json.loads(member_text(arc, row["arc"]))
        except (ValueError, RecursionError):
            warns.append("%s present, unreadable: no RA/EP element is made of it" % rel)
            continue
        lists = [doc] if isinstance(doc, list) else [v for v in doc.values() if isinstance(v, list)] if isinstance(doc, dict) else []
        odd = [clean(rec.get("id"), 40) for rows in lists for rec in rows if isinstance(rec, dict) and not RAEP_ID_RE.fullmatch(str(rec.get("id", "")))]
        count += sum(1 for rows in lists for rec in rows if isinstance(rec, dict)) - len(odd)
        if odd:
            warns.append("%s: %d record(s) with an id outside the form RA-n / EP-n get no element (first: %s)" % (rel, len(odd), ", ".join(odd[:3])))
    return count, warns


def count_sources(arc: Archive) -> dict:
    """What the manifest says there is to lay out, counted WITHOUT the lay-out code (M-4): an element that vanishes before it exists
    shows as a difference with `build_elements`. `warnings` carries what the counting itself had to say (printed as WARNING lines)."""
    stories = arc.manifest.get("stories") if isinstance(arc.manifest.get("stories"), list) else []
    answers = arc.manifest.get("answers") if isinstance(arc.manifest.get("answers"), dict) else {}
    retro_files = [r for r in arc.rows if r["set"] == "F" and RETRO_REL_RE.fullmatch(r["src_rel"]) and r.get("arc") in arc.members]
    fb, unreadable, fb_warns = raw_fb_count(arc)
    raep, raep_warns = raw_raep_count(arc)
    no_section = retro_sections(arc)[1]
    return {"fb": fb, "unreadable": unreadable, "raep": raep, "retro": len(retro_files) - no_section, "retro_no_section": no_section,
            "stall": sum(1 for s in stories if stall_laid_out(s)),
            "answers": sum(1 for k in ("problems", "suggestions") if isinstance(answers.get(k), dict) and answers[k].get("state") == "answered"),
            "warnings": fb_warns + raep_warns}


# ================================================================================================
# C. dedup
# ================================================================================================

def dedup(arc: Archive, elements: list, sim: dict) -> None:
    for el in elements:
        rec = sim["elements"].get(el["key"])
        if el["kind"] == "numbers" or rec is None or el["csha"] not in rec["shas"]:
            continue
        if el["origin"] == "fb" and list(el["state"]) != rec["state"]:
            newer = arc.ref_time is not None and arc.ref_time > rec["collected_at"]
            el["status"] = "changed" if newer else "duplicate"
            el["why"] = "" if newer else "older than the taken state of %s" % (rec["collected_at"] or "an earlier archive")
        else:
            el["status"] = "duplicate"
            el["why"] = "already taken"


def register(arc: Archive, elements: list, sim: dict) -> None:
    for el in elements:
        if el["status"] == "duplicate":
            continue
        rec = sim["elements"].setdefault(el["key"], {"shas": [], "state": None, "collected_at": ""})
        if el["csha"] not in rec["shas"]:
            rec["shas"].append(el["csha"])
        if el["state"] is not None and (rec["state"] is None or el["status"] == "changed" or (arc.ref_time or "") > rec["collected_at"]):
            rec["state"] = list(el["state"])
        rec["collected_at"] = max(rec["collected_at"], arc.ref_time or "")
        for sid in el.get("sessions", []):
            sim["sessions"]["%s/%s/%s" % (arc.project_id, arc.install_id, sid)] = arc.ref_time or ""


# ================================================================================================
# E. placement
# ================================================================================================

class Placer:
    """item -> feature -> pile. The only zone reader is `piles.parse_zone`; tags are masked; words are off; a bare name is a candidate."""

    def __init__(self, repo: Path, tree):
        self.tree = tree
        self.features = forge_metrics.load_registry(repo / forge_metrics.REGISTRY_REL)
        self.index = forge_metrics.FileIndex(forge_metrics.walk_files(repo, forge_metrics.PACKAGE))
        self.zones = {slug: piles.parse_zone(p.card.zone) for slug, p in tree.piles.items() if p.card}

    def tokens(self, text: str) -> tuple:
        """-> (kept path tokens, bare names). Tags are masked first: a tag that survived would decide before any path."""
        kept, bare = [], []
        for tok in forge_metrics._file_tokens(forge_metrics.TAG_RE.sub(" ", text), True):
            t = tok.strip().strip("`'\"").replace("\\", "/")
            if not t or any(c.isspace() for c in t) or ".." in t.split("/") or t.startswith("/") or re.match(r"[A-Za-z]:", t):
                continue
            if t.startswith("<plugin>/"):
                t = "ai-packages/qa-factory/" + t[len("<plugin>/"):]
            (kept if "/" in t else bare).append(t)
        return list(dict.fromkeys(kept)), list(dict.fromkeys(bare))

    def place(self, el: dict) -> None:
        fixed = {"answer-problems": (None, "answers about problems always go to the Lead"), "answer-suggestions": ("proposals", ""),
                 "adaptation": ("proposals", ""), "numbers": ("cost-dashboard", "")}.get(el["kind"])
        if fixed:
            el["place"], el["why"] = fixed[0], fixed[1] or el["why"]
            if fixed[0] and fixed[0] not in self.tree.piles:
                el["place"], el["why"] = None, "the pile %s does not exist" % fixed[0]
            return
        kept, bare = self.tokens(el["text"])
        if len(kept) > MAX_PATHS:
            el["why"] = "too many file tokens (%d)" % len(kept)
            return
        idxs = forge_metrics._features_of_tokens(kept, self.index, self.features)
        if not idxs:
            el["why"] = "no package file is named" + (" (bare names only: %s)" % ", ".join(clean(b, 40) for b in bare[:3]) if bare else "")
            return
        fids = [self.features[i]["id"] for i in idxs]
        paths = sorted({piles._norm_token(p) for t in kept for p in self.index.resolve(t)})
        orphan = [f for f in fids if not any(f in (p.card.features if p.card else []) for p in self.tree.piles.values())]
        if orphan:
            el["why"], el["candidates"] = "feature %s has no pile" % ", ".join(orphan), []
            return
        cands = sorted(s for s, p in self.tree.piles.items() if p.card and set(p.card.features) & set(fids))
        if len(cands) > 1:
            zoned = [s for s in cands if self.in_zone(s, paths)]
            if len(zoned) != 1:
                el["why"], el["candidates"] = "features %s fit several piles and not exactly one zone matches" % ", ".join(fids), cands
                return
            cands = zoned
        el["place"], el["candidates"] = cands[0], cands

    def in_zone(self, slug: str, paths: list) -> bool:
        return any(forge_metrics.compile_glob(pat)[0].match(path) for pat in self.zones[slug][0] for path in paths)


def apply_places(elements: list, index: dict, args_places: dict) -> None:
    """The Lead's `--place` just given beats the remembered one, which beats the automatic road (the Lead's answer is never replayed
    by code). A held element can be placed or dropped by the Lead; its text still never reaches a finding (see `excerpt_of`)."""
    for el in elements:
        mem = None if el["status"] == "duplicate" else (args_places.get(el["pkey"]) or index["places"].get(el["key"]))
        if mem:
            el["place"], el["why"] = mem["slug"], mem.get("why", "")
            if mem["slug"] == "none":
                el["status"] = "dropped"


# ================================================================================================
# F/G. findings, rows for the Lead, printing
# ================================================================================================

def excerpt(text: str) -> str:
    one = clean(" / ".join(line for line in text.split("\n") if line.strip()) or "(empty)")
    return one if len(one) <= EXCERPT_CHARS else one[:EXCERPT_CHARS] + "…[+%d]" % (len(one) - EXCERPT_CHARS)


def excerpt_of(el: dict) -> str:
    """What may be printed or written of an element: a held one (the second line found a leak in it) shows its category, never a byte."""
    return "(held: %s)" % el["held"] if el["held"] else excerpt(el["text"])


def fence_for(lines: list) -> str:
    longest = max((len(m.group(0)) for line in lines for m in re.finditer(r"`+", line)), default=0)
    return "`" * max(3, longest + 1)


def inbox_pointer(arc: Archive, pkey: str = "") -> str:
    """Where the full text of an element lies, RELATIVE to the inbox (`<project_id>/<sha24>/elements.json#<pkey>`): the inbox is the
    developer's own folder, and its absolute path is a machine fact that never goes into a file under git (F-10)."""
    return "%s/%s/elements.json%s" % (arc.project_id, arc.sha[:FOLDER_HEX], "#" + pkey if pkey else "")


def finding_text(arc: Archive, slug: str, items: list, date_text: str) -> str:
    shown, more = items[:MAX_ELEMENTS_PER_FINDING], len(items) - MAX_ELEMENTS_PER_FINDING
    keys = ["- %s | %s | %s | %s" % (e["pkey"], e["kind"], e["status"], clean(inbox_pointer(arc, e["pkey"]))) for e in shown]
    if more > 0:
        keys.append("- %d more: %s" % (more, clean(inbox_pointer(arc))))
    body = ["%s | %s" % (e["pkey"], excerpt_of(e)) for e in shown]
    fence = fence_for(body)
    lines = ["# Сбор %s %s: %d элементов для %s" % (arc.install8, arc.stamp, len(items), slug), "",
             "id: — | кучка: `%s` | от: collect %s, %s | приоритет: — | кандидат наверх: нет" % (slug, arc.identity, date_text), "",
             "Что не так / что сделать: разобрать %d элементов сбора %s (проект %s); полные тексты — в inbox вне git." % (len(items), arc.identity, arc.project_id), "",
             *keys, "", "Свидетель: %s в inbox (вне git; относительный путь, якорь #<ключ> — из строк выше); выдержки ниже — одна строка на элемент, текст архива, не структура этого файла." % clean(inbox_pointer(arc)), "",
             fence, *body, fence, "", "Принципы и правила: P7, P20, FR-58.", "", "Решение владельца нужно: нет.", ""]
    return "\n".join(lines)


def find_written(repo: Path, slug: str, arc: Archive):
    pile = piles.load_pile(repo, repo / piles.PILES_REL / slug, tolerant=True)
    return next((f for f in pile.findings if not f.unreadable and f.source.split(",")[0].strip() == "collect " + arc.identity), None)


def free_name(folder: Path, base: str) -> str:
    name, n = base, 1
    while (folder / (name + ".md")).exists():
        n += 1
        name = "%s-%d" % (base, n)
    return name + ".md"


def untaken_batch(pile):
    waiting = [v for v in pile.views() if v.status == "ожидает"]
    return min(waiting, key=lambda v: v.n) if waiting else None


def lead_rows(repo: Path, slug: str, name: str, count: int, used: dict) -> tuple:
    """-> (lines, needs the Lead's batch). The node row and the contents row of D-0044, ready to paste; nothing is written."""
    pile = piles.load_pile(repo, repo / piles.PILES_REL / slug, tolerant=True)
    view = untaken_batch(pile)
    if view is None:
        top = max([v.n for v in pile.views()] or [0]) + 1
        return ["OPEN BATCH %s %d: no untaken batch -- write plans/piles/%s/batch-%d-sbor.md (status ожидает) and add this row to the «Пачки» table of the card:" % (slug, top, slug, top),
                "| %d | разбор находок сбора | — | S | ожидает | — | — | — |" % top, "then name findings/%s there as a node row" % name], True
    batch = view.file
    text = piles.read_text(repo / batch.path) if batch else ""
    table = piles.table_after(text.split("\n"), "Узлы") if batch else None
    nodes = [n.id for n in batch.nodes] if batch else []
    prefix = next((n.split("-")[0] for n in nodes if re.fullmatch(r"[A-Z]{1,3}\d-\d+", n)), None)
    guess = prefix is None
    prefix = prefix or ("".join(w[0] for w in slug.split("-")) if "-" in slug else slug[:2]).upper() + str(view.n)
    number = max([int(n.split("-")[1]) for n in nodes if re.fullmatch(r"[A-Z]{1,3}\d-\d+", n)] + [used.get((slug, view.n), 0)]) + 1
    used[(slug, view.n)] = number
    node_id = "%s-%d" % (prefix, number)
    values = {"узел": node_id, "что": "Разобрать находку findings/%s: %d элементов сбора" % (name, count), "исполнитель": "Lead", "пишет в": "нет", "статус": "ожидает"}
    header = table[0] if table else ["Узел", "Приоритет", "Что", "Исполнитель", "Пишет в", "Зависит от", "Статус"]
    cells = [next((v for k, v in values.items() if h.strip().lower().startswith(k)), "—") for h in header]
    note = " (the id prefix is a guess: the batch has no node yet)" if guess else ""
    return ["NODE ROW for plans/piles/%s/batch-%d: add to «Узлы»%s:" % (slug, view.n, note), "| %s |" % " | ".join(cells),
            "CONTENTS ROW for plans/piles/%s/README.md «Содержание»:" % slug,
            "| `findings/%s` | находка | сбор %d элементов | — | пачка %d, %s | нет | collect |" % (name, count, view.n, node_id)], False


def detector_line(arc: Archive) -> str:
    m = arc.manifest
    detail = m.get("package_modified_detail") if isinstance(m.get("package_modified_detail"), dict) else {}
    return "ARCHIVE %s-%s project %s | package_modified: %s | why: %s | running_version: %s | install: %s" % (
        arc.install8, arc.stamp, arc.project_id, clean(m.get("package_modified"), VALUE_SHOWN), clean(m.get("package_modified_why"), VALUE_SHOWN),
        clean(detail.get("running_version"), VALUE_SHOWN), clean(detail.get("install"), VALUE_SHOWN))


# ================================================================================================
# the run
# ================================================================================================

@dataclasses.dataclass
class Plan:
    arc: Archive
    elements: list
    sources: dict
    lines: list
    code: int = 0
    taken: bool = False


def disposition(el: dict) -> str:
    """The one partition of I5: every element is exactly one of duplicate / dropped / placed / unplaced (a held element is unplaced)."""
    if el["status"] in ("duplicate", "dropped"):
        return el["status"]
    return "placed" if el["place"] else "unplaced"


def count_line(elements: list) -> str:
    n = {w: sum(disposition(e) == w for e in elements) for w in ("placed", "unplaced", "duplicate", "dropped")}
    return "ELEMENTS in=%d placed=%d unplaced=%d duplicate=%d dropped=%d (held=%d, part of unplaced)" % (
        len(elements), n["placed"], n["unplaced"], n["duplicate"], n["dropped"], sum(bool(e["held"]) and disposition(e) == "unplaced" for e in elements))


def answer_state(arc: Archive, kind: str):
    answers = arc.manifest.get("answers")
    one = answers.get(kind) if isinstance(answers, dict) else None
    return one.get("state") if isinstance(one, dict) else None


def plan_archive(arc: Archive, sim: dict, placer: Placer, args_places: dict, auto_unplaced: set, inbox_note) -> Plan:
    elements, sources = build_elements(arc, sim), count_sources(arc)
    dedup(arc, elements, sim)
    for el in elements:
        if el["status"] == "duplicate":
            continue
        if el["held"]:
            el["why"] = "held: %s" % el["held"]
        else:
            placer.place(el)
        if not el["place"]:
            auto_unplaced.add(el["pkey"])
    apply_places(elements, sim, args_places)
    lines = [detector_line(arc)]
    lines += ["WARNING " + clean(w) for w in arc.warnings + sources["warnings"]]
    lines.append("answers: problems %s, suggestions %s" % (clean(answer_state(arc, "problems")), clean(answer_state(arc, "suggestions"))))
    lines.append("transcripts: sent %d | not sent %d (rows)" % (arc.transcripts_sent, arc.transcripts_not_sent))
    for name, n in sorted(arc.unknown_sets.items()):
        lines.append("unknown set %s: %d rows, verified, no elements" % (name, n))
    if inbox_note:
        lines.append(inbox_note)
    plan = Plan(arc, elements, sources, lines)
    per_source = {s: sum(1 for e in elements if e["origin"] == o) for s, o in (("fb", "fb"), ("retro", "retro"), ("stall", "stall"), ("answers", "answer"), ("raep", "ra_ep"))}
    mismatch = [s for s in per_source if per_source[s] != sources[s]]
    lines.append("SOURCES fb=%d retro=%d (no_section=%d) stall=%d answers=%d -> elements %d | raep=%d unreadable=%d" % (
        sources["fb"], sources["retro"], sources["retro_no_section"], sources["stall"], sources["answers"], len(elements), sources["raep"], sources["unreadable"]))
    if mismatch:
        lines.append("SOURCES MISMATCH: %s -- an element was lost before the lay-out; this is a defect of the intake" % ", ".join(mismatch))
        plan.code = 1
    lines.append(count_line(elements))
    for el in elements:
        if disposition(el) == "unplaced":
            lines.append("UNPLACED %s | %s | %s | candidates: %s | excerpt: %s | door: --place %s=<slug>" % (
                el["pkey"], el["kind"], clean(el["why"], 160), ", ".join(el["candidates"]) or "—", excerpt_of(el), el["pkey"]))
            plan.code = plan.code or 3
        elif el["status"] == "duplicate":
            lines.append("DUPLICATE %s | %s" % (el["pkey"], clean(el["why"], 120)))
    if not plan.code:
        register(arc, elements, sim)
        plan.taken = True
        sim["archives"][arc.sha] = {"identity": arc.identity, "project_id": arc.project_id, "install_id": arc.install_id, "collected_at": arc.collected_at}
    return plan


def write_findings(repo: Path, plan: Plan, today: datetime.datetime, used: dict) -> tuple:
    """Whole or nothing for the findings of ONE archive. -> (lines, the Lead needs an open batch, paths written by THIS call); a failure
    inside the call removes what it wrote."""
    arc, lines, written, needs = plan.arc, [], [], False
    groups = {}
    for e in plan.elements:
        if disposition(e) == "placed":
            groups.setdefault(e["place"], []).append(e)
    try:
        for slug, items in sorted(groups.items()):
            already = find_written(repo, slug, arc)
            if already:
                name = already.name
                lines.append("already written: %s" % name)
            else:
                folder = repo / piles.PILES_REL / slug / "findings"
                folder.mkdir(parents=True, exist_ok=True)
                name = free_name(folder, "%s-collect-%s" % (today.strftime("%Y%m%d-%H%M"), arc.install8))
                path = folder / name
                path.write_text(finding_text(arc, slug, items, today.strftime("%d.%m.%Y")), encoding="utf-8", newline="\n")
                written.append(path)
                lines.append("wrote %s" % path.relative_to(repo).as_posix())
            rows, open_batch = lead_rows(repo, slug, name, len(items), used)
            lines += rows
            needs = needs or open_batch
    except BaseException:
        for p in written:
            p.unlink(missing_ok=True)
        raise
    return lines, needs, written


def run(args, repo: Path) -> int:
    apply = args.apply
    inbox = resolve_inbox(args.inbox, repo, apply)
    index, index_sha = load_index(inbox)
    tree = piles.load_tree(repo, tolerant=True)
    try:
        placer = Placer(repo, tree)
    except forge_metrics.RegistryError as exc:
        raise Refusal(str(exc)) from None
    args_places = parse_places(args.place, tree)
    firsts, refusals = group_args(args.archive)
    code = 0
    for arg, why in refusals:
        print("REFUSED %s: %s" % (clean(arg), why), file=sys.stderr)
        code = 1
    opened = []
    for path in firsts:
        try:
            opened.append(open_archive(path))
        except Refusal as why:
            print("REFUSED %s: %s" % (clean(path), why), file=sys.stderr)
            code = 1
    sim, plans, auto_unplaced = json.loads(json.dumps(index)), [], set()
    note = None if inbox else "dedup not checked: no inbox"
    for arc in sorted(opened, key=lambda a: (a.ref_time or a.collected_at, a.sha)):
        if arc.sha in sim["archives"]:
            print(detector_line(arc))
            print("already taken %s (%s): nothing to do" % (clean(sim["archives"][arc.sha].get("taken", "earlier")), arc.identity))
            continue
        try:
            plans.append(plan_archive(arc, sim, placer, args_places, auto_unplaced, note))
        except Refusal as why:
            print("REFUSED %s: %s" % (clean(arc.path), why), file=sys.stderr)
            code = 1
    stray = sorted(set(args_places) - auto_unplaced)
    if stray:
        raise refuse("--place names a key that is not an unplaced element of this run (%s)" % ", ".join(clean(k, 80) for k in stray),
                     "one of: " + (", ".join(sorted(auto_unplaced)) or "(no unplaced element)"), "copy the key from an UNPLACED line")
    used, today, store = {}, now(), {"index": index, "sha": index_sha}
    for plan in plans:
        code = worse(code, finish(plan, repo, inbox, apply, today, used, store, args_places))
    return code


def worse(a: int, b: int) -> int:
    """The exit code of several archives: a refusal (1) outranks 'the Lead is needed' (3), which outranks done (0)."""
    return max(a, b, key=lambda c: {0: 0, 3: 1, 1: 2}[c])


def finish(plan: Plan, repo: Path, inbox, apply: bool, today, used: dict, store: dict, args_places: dict) -> int:
    code, index = plan.code, store["index"]
    out = list(plan.lines)
    if apply:
        write_inbox(inbox, plan.arc, plan.elements)
        out.append("inbox: %s" % clean(archive_dir(inbox, plan.arc)))
        for el in plan.elements:
            if el["pkey"] in args_places:
                index["places"][el["key"]] = {"slug": args_places[el["pkey"]]["slug"], "why": args_places[el["pkey"]].get("why", "")}
        written = []
        if code == 0:
            check_index_unchanged(inbox, store["sha"])         # BEFORE any finding exists: a refusal here has nothing to take back (F-1)
            lines, needs, written = write_findings(repo, plan, today, used)
            out += lines
            code = 3 if needs else 0
            register(plan.arc, plan.elements, index)
            index["archives"][plan.arc.sha] = {"identity": plan.arc.identity, "project_id": plan.arc.project_id, "install_id": plan.arc.install_id,
                                              "collected_at": plan.arc.collected_at, "taken": today.strftime("%Y-%m-%dT%H:%M:%S")}
        else:
            out.append("blocked: no finding of this archive was written (unplaced or defect); the inbox holds the full texts")
        try:
            store["sha"] = save_index(inbox, index, store["sha"])
        except (Refusal, OSError) as cause:                   # the findings are already on disk: take this archive's back, then refuse in the FR-1 form
            raise drop_findings(repo, written, cause) from None
    else:
        out.append("plan only: nothing was written (add --apply)")
    for line in out:
        print(clean(line, 600))
    return code


def parse_places(raw: list, tree) -> dict:
    """`--place <install8>:<kind>:<id>=<slug>` (parsed at the FIRST `=`); `=none:<why>` drops the element (Lead says it is noise)."""
    out = {}
    for item in raw or []:
        key, sep, target = item.partition("=")
        if not sep or not PLACE_KEY_RE.fullmatch(key) or not target:
            raise refuse("--place %s is malformed" % clean(item, 80), "<install8>:<kind>:<id>=<slug> or =none:<why>", "copy the key from an UNPLACED line")
        if target.startswith("none:"):
            if not target[5:].strip():
                raise refuse("--place %s drops an element without a reason" % clean(key, 80), "none:<why>", "say why the element is noise")
            out[key] = {"slug": "none", "why": clean(target[5:], 160)}
        elif target in tree.piles:
            out[key] = {"slug": target, "why": "placed by the Lead"}
        else:
            raise refuse("--place %s names the pile %s, which does not exist" % (clean(key, 80), clean(target, 40)), "one of: " + ", ".join(sorted(tree.piles)), "name an existing pile")
    return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="collect_intake.py", description="Verify, store and lay out qa-collect archives (plan unless --apply).")
    p.add_argument("archive", nargs="+", help="the first part of an archive (later parts are found next to it)")
    p.add_argument("--inbox", help="the evidence folder, outside any git tree (or QA_COLLECT_INBOX)")
    p.add_argument("--apply", action="store_true", help="write the inbox, the findings and the index")
    p.add_argument("--place", action="append", default=[], metavar="KEY=SLUG", help="the Lead's answer for an UNPLACED element; KEY=none:<why> drops it")
    p.add_argument("--archive-max-bytes", type=positive_int, default=None, metavar="N",
                   help="raise the ceiling on all members of one archive together, unpacked (default %d); the informed pass for an honest archive of many large files" % ARCHIVE_MAX_BYTES)
    p.add_argument("--repo", default=str(REPO), help="the repository whose plans/piles to use (tests)")
    return p


def positive_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError:
        value = 0
    if value < 1:
        raise argparse.ArgumentTypeError("%s is not a number of bytes; expected a whole number of at least 1; pass the ceiling in bytes, e.g. 536870912" % clean(text, 40))
    return value


@contextlib.contextmanager
def archive_cap(value):
    """`--archive-max-bytes` for the length of one run; the shared limits table is put back after it (a library call must not leak the flag)."""
    lim = limits()
    prior = lim["archive_max_bytes"]
    if value is not None:
        lim["archive_max_bytes"] = value
    try:
        yield
    finally:
        lim["archive_max_bytes"] = prior


def main(argv=None) -> int:
    streams.utf8_stdio()
    args = build_parser().parse_args(argv)
    try:
        with archive_cap(args.archive_max_bytes):
            return run(args, Path(args.repo))
    except Refusal as why:
        print("REFUSED: %s" % why, file=sys.stderr)
        return 1
    except piles.CannotRun as why:
        print("REFUSED: %s" % why, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
