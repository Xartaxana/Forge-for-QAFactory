"""Forge metrics -- feature attribution of the work done on the QA Factory package,
derived from what every developer already produces through the committed process
(plans/BACKLOG.md rows, logs/routing-log.jsonl events, git commits), so that a
fresh clone collects it without being asked.

"Forge" = this repository's system of working on the factory (the name is
provisional, see plans/feature-fragility-reading-2026-10-02.md section 5).

Inputs (read only): plans/features.json (the registry), plans/BACKLOG.md,
logs/routing-log.jsonl, `git log` over ai-packages/qa-factory, and optionally the
hand-made seed plans/feature-fragility-2026-10-02.md (Table A, for rows older than
the registry). Since the BACKLOG freeze of 08.10.2026 new work arrives as FINDING files
(plans/piles/<slug>/findings/*.md), read through tools/piles.py (load_tree, the one reader of
the piles tree) and counted next to the rows: attribution = a Fnn tag in the finding's text, else
the first feature of its pile card's `фичи:` line, else unclassified. An unclassified finding is a
Forge metric printed in --check, never an offender (CLAUDE.md host adaptation 4). Without a
plans/piles directory both the report and --check read as they did before findings existed.
The tree is loaded tolerantly: a finding that is not UTF-8 is ONE warning and unclassified (the card is not asked for it).
A finding RENAMED since the base (`yyyymmdd-<slug>.md` -> `B-nnn-<slug>.md`, same pile) is not new: paired on (pile, slug)
only when each side holds exactly one candidate, never for a base file whose id the BACKLOG closed. A bracketed tag the
registry does not know ([F99]) is ignored by attribution and named in a WARN: on a NEW backlog row and on a finding that
also carries a registered tag (the report names it on any row, it has no base to call a row new).

Modes:
  python tools/forge_metrics.py                  the report to stdout
  python tools/forge_metrics.py --write          writes plans/forge-metrics.md
  python tools/forge_metrics.py --json           the same data as JSON
  python tools/forge_metrics.py --check [--base REF] [--warn]
        merge/commit gate: names every NEW backlog row, NEW package file and NEW
        journal event that carries no feature attribution, each with its door.
        Writes nothing. --warn prints the same text and always exits 0.

Exit codes: 0 ok; 1 --check found offenders; 2 the registry is missing/malformed or
the --check base cannot be resolved (nothing is written, no silent empty table).

A NEW feature announces itself: a package file matching no feature is UNCLASSIFIED
and is printed first; register it in plans/features.json.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

import gitcmd

try:
    import journal_validator as _jv
except Exception:  # the check constants then fall back to the same values
    _jv = None

# B-402: the task key. Two clones issue the same t-NNN; tools/journal_keys.py keys an event by
# (label, task_id) through logs/journal-segments.json. Without the module every id is bare
# (the reading before the declaration existed) -- the hook that runs this must not crash on it.
try:
    import journal_keys as _jk
except Exception:
    _jk = None

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "ai-packages/qa-factory"
REGISTRY_REL = "plans/features.json"
BACKLOG_REL = "plans/BACKLOG.md"
JOURNAL_REL = "logs/routing-log.jsonl"
SEED_REL = "plans/feature-fragility-2026-10-02.md"
OUT_REL = "plans/forge-metrics.md"
DEFAULT_WINDOW = "2026-09-26"
TOP_N = 10                  # how many names an unclassified bucket prints
WIDE_COMMIT_FILES = 100     # a commit touching this many package files is named in a footnote
PROCESS_DOC_PREFIXES = ("docs/", "plans/")   # "F19 docs" of the process-tax metric

# The events that must carry a `feature` field and the day it starts to be asked
# (single source: tools/journal_validator.py).
FEATURE_EVENTS = set(getattr(_jv, "FEATURE_WARN_EVENTS", {"delegated", "accepted", "defect_found"}))
FEATURE_FROM = getattr(_jv, "FEATURE_WARN_FROM", "2026-10-02")
TASK_EVENTS = {"delegated", "accepted", "rejected", "escalated", "defect_found"}

EXPECTED_SHAPE = (
    '{"schema_version": 1, "features": [{"id": "F01", "name": "...", "root": "package"|"repo", '
    '"globs": ["..."], "stages": ["S0"], "words": ["..."]}, ...]}'
)

# --- the word lists (the carriers are named in the report) ---------------------------------
LIVE_WORDS = ("живьём", "live run", "репетиц", "rehearsal", "прогон")
FIXFIX_WORDS = ("после t-", "после B-", "fix-of-fix", "регресс")
CLOSED_WORDS = (r"закрыт", r"сделан", r"снят", r"\bclosed\b", r"\bdone\b")
LIVE_RE = re.compile("|".join(re.escape(w) for w in LIVE_WORDS), re.I)
FIXFIX_RE = re.compile("|".join(re.escape(w) for w in FIXFIX_WORDS), re.I)
CLOSED_RE = re.compile("|".join(CLOSED_WORDS), re.I)

TAG_RE = re.compile(r"(?<![A-Za-z0-9_-])F(\d\d)(?![0-9A-Za-z_])")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")
BARE_PATH_RE = re.compile(r"(?<![\w./-])([\w./-]*[\w-]\.(?:py|md|json|jsonl|yaml|yml|cmd|sh))(?::\d+(?:-\d+)?)?(?![\w-])")
STAGE_RE = re.compile(r"\bS(\d)\b")
DATE_RE = re.compile(r"(?<![\d.$A-Za-z])(0[1-9]|[12]\d|3[01])\.(09|10)(?!\d)")
ROW_ID_RE = re.compile(r"^\| (B-\d+)\s*\|")
PILES_REL = "plans/piles"
# a finding file of a pile (the same exclusion of `_template` / dot folders as piles._is_pile_dir)
FINDING_PATH_RE = re.compile(r"^plans/piles/[^/_.][^/]*/findings/[^/]+\.md$")
BRACKET_TAG_RE = re.compile(r"\[F(\d\d)\]")      # the explicit tag form: only this one can be called unknown

DOOR_ROW = "add [Fnn] to the row (e.g. at the end of the text) or name the file in backticks"
DOOR_FILE = ("register the feature in plans/features.json (a new feature = a new row, "
             "e.g. F21 Codex integration)")
DOOR_EVENT = "add the feature field (the id from plans/features.json, e.g. \"feature\":\"F07\")"


class RegistryError(Exception):
    """plans/features.json is missing or malformed (exit 2, nothing written)."""


class BaseError(Exception):
    """--check could not resolve its base (exit 2)."""


# ============================================================================================
# registry and globs
# ============================================================================================

def compile_glob(glob: str):
    """Glob -> (compiled regex, specificity). * = run without '/', ** = run with '/',
    ? = one char. Specificity = number of literal characters (wildcards do not count)."""
    out = []
    i = 0
    n = len(glob)
    while i < n:
        c = glob[i]
        if c == "*":
            if glob[i:i + 3] == "**/":
                out.append("(?:.*/)?")
                i += 3
                continue
            if glob[i:i + 2] == "**":
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
        elif c == "?":
            out.append("[^/]")
        else:
            out.append(re.escape(c))
        i += 1
    spec = len(glob) - glob.count("*") - glob.count("?")
    return re.compile("^" + "".join(out) + "$"), spec


def _fail_registry(path, why: str):
    raise RegistryError(f"{path}: {why}; expected shape: {EXPECTED_SHAPE}")


def load_registry(path) -> list:
    """Reads and validates the registry. Returns the features list (each with compiled
    globs under '_globs'), registry order preserved. Raises RegistryError."""
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        _fail_registry(path, f"cannot be read ({e})")
    except UnicodeDecodeError as e:
        _fail_registry(path, f"is not UTF-8 ({e})")
    try:
        data = json.loads(text)
    except ValueError as e:
        _fail_registry(path, f"is not valid JSON ({e})")
    if not isinstance(data, dict) or not isinstance(data.get("features"), list) or not data["features"]:
        _fail_registry(path, "must be an object with a non-empty 'features' list")
    feats = []
    seen = set()
    for i, f in enumerate(data["features"]):
        if not isinstance(f, dict):
            _fail_registry(path, f"features[{i}] is not an object")
        fid = f.get("id")
        if not isinstance(fid, str) or not re.fullmatch(r"F\d\d", fid):
            _fail_registry(path, f"features[{i}].id must look like F07, got {fid!r}")
        if fid in seen:
            _fail_registry(path, f"duplicate feature id {fid}")
        seen.add(fid)
        name = f.get("name")
        if not isinstance(name, str) or not name:
            _fail_registry(path, f"{fid}.name must be a non-empty string")
        root = f.get("root", "package")
        if root not in ("package", "repo"):
            _fail_registry(path, f"{fid}.root must be 'package' or 'repo', got {root!r}")
        globs = f.get("globs")
        if not isinstance(globs, list) or not globs or not all(isinstance(g, str) and g for g in globs):
            _fail_registry(path, f"{fid}.globs must be a non-empty list of strings")
        stages = f.get("stages", [])
        words = f.get("words", [])
        if not isinstance(stages, list) or not all(isinstance(s, str) for s in stages):
            _fail_registry(path, f"{fid}.stages must be a list of strings")
        if not isinstance(words, list) or not all(isinstance(w, str) for w in words):
            _fail_registry(path, f"{fid}.words must be a list of strings")
        feats.append({
            "id": fid, "name": name, "root": root, "globs": list(globs),
            "stages": list(stages), "words": [w.lower() for w in words],
            "_globs": [(g,) + compile_glob(g) for g in globs],
        })
    return feats


def split_root(repo_rel: str):
    """repo-relative path -> (root kind, path relative to that root)."""
    p = repo_rel.replace("\\", "/").lstrip("/")
    if p.startswith(PACKAGE + "/"):
        return "package", p[len(PACKAGE) + 1:]
    return "repo", p


def feature_hits(features: list, repo_rel: str) -> list:
    """[(registry index, best specificity)] of every feature whose globs match the path."""
    kind, rel = split_root(repo_rel)
    hits = []
    for i, f in enumerate(features):
        if f["root"] != kind:
            continue
        best = -1
        for _g, rx, spec in f["_globs"]:
            if rx.match(rel) and spec > best:
                best = spec
        if best >= 0:
            hits.append((i, best))
    return hits


def classify_path(features: list, repo_rel: str):
    """First feature in registry order that matches, else None."""
    hits = feature_hits(features, repo_rel)
    return features[hits[0][0]]["id"] if hits else None


def find_overlaps(features: list, repo_paths) -> list:
    """Paths that are ambiguous: 'overlap' = two features match with the SAME best
    specificity (the winner is the first in registry order); 'shadowed' = the first
    match is LESS specific than a later one (order does not put specific before general)."""
    found = []
    for p in repo_paths:
        hits = feature_hits(features, p)
        if len(hits) < 2:
            continue
        top = max(s for _i, s in hits)
        tied = [features[i]["id"] for i, s in hits if s == top]
        if len(tied) >= 2:
            found.append({"path": p, "kind": "overlap", "features": [features[i]["id"] for i, _s in hits]})
        elif hits[0][1] < top:
            found.append({"path": p, "kind": "shadowed", "features": [features[i]["id"] for i, _s in hits]})
    return found


# ============================================================================================
# files: index, walk, git
# ============================================================================================

def _run_git(root, *args, check_text=True):
    rc, out = gitcmd.git(root, *args)
    if rc != 0:
        return None
    return gitcmd.as_text(out)


def walk_files(root, rel_dir: str) -> list:
    """Sorted repo-relative files under rel_dir (skips __pycache__ and .pyc)."""
    base = Path(root) / rel_dir
    out = []
    if not base.is_dir():
        return out
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in ("__pycache__", ".pytest_cache", ".git", "node_modules"))
        for fn in filenames:
            if fn.endswith(".pyc"):
                continue
            full = Path(dirpath) / fn
            out.append(full.relative_to(root).as_posix())
    return sorted(out)


def package_files(root) -> list:
    return walk_files(root, PACKAGE)


def tracked_files(root):
    """git ls-files (tracked) as a sorted list, or None when git is unavailable."""
    out = _run_git(root, "ls-files")
    if out is None:
        return None
    return sorted(l for l in out.split("\n") if l)


class FileIndex:
    """Repo-relative paths for resolving a token named in a row/event to real files."""

    def __init__(self, paths):
        self.paths = sorted(set(paths))
        self.pset = set(self.paths)
        self.by_name = {}
        for p in self.paths:
            self.by_name.setdefault(p.rsplit("/", 1)[-1], []).append(p)

    @staticmethod
    def _candidates(token: str):
        t = token.strip().strip("`'\"").replace("\\", "/")
        t = re.sub(r"\(.*\)$", "", t)
        t = re.sub(r":\d+(?:-\d+)?$", "", t).rstrip(".,;:")
        if t.startswith("./"):
            t = t[2:]
        if not t:
            return []
        cands = [t]
        if "/" not in t and "." in t:
            head = t.split(".", 1)[0]
            if head:
                cands.append(head)       # module.function -> module
        return cands

    def resolve(self, token: str) -> list:
        for c in self._candidates(token):
            if c in self.pset:
                return [c]
            if (PACKAGE + "/" + c) in self.pset:
                return [PACKAGE + "/" + c]
            if "/" in c:
                hit = [p for p in self.paths if p.endswith("/" + c)]
                if hit:
                    return hit
                continue
            names = self.by_name.get(c) or self.by_name.get(c + ".py") or []
            if names:
                real = [p for p in names if "/fixtures/" not in p]
                return real or names
        return []


# ============================================================================================
# backlog rows
# ============================================================================================

def parse_backlog_text(raw: bytes):
    """-> (rows, skipped_line_numbers). A row is a line starting '| B-nnn |'; sub-items
    '(а)...' stay inside their row (one row). A row with non-UTF-8 bytes is skipped."""
    rows, skipped = [], []
    for lineno, bline in enumerate(raw.split(b"\n"), 1):
        if not bline.startswith(b"| B-"):
            continue
        try:
            line = bline.decode("utf-8").rstrip("\r")
        except UnicodeDecodeError:
            skipped.append(lineno)
            continue
        m = ROW_ID_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)][1:]
        if cells and cells[-1] == "":
            cells.pop()
        rows.append({
            "id": m.group(1), "line": lineno, "line_text": line, "cells": cells,
            "text": cells[1] if len(cells) > 1 else "",
            "source": cells[2] if len(cells) > 2 else "",
            "status": cells[3] if len(cells) > 3 else "",
        })
    return rows, skipped


def parse_backlog(path):
    try:
        raw = Path(path).read_bytes()
    except OSError:
        return [], []
    return parse_backlog_text(raw)


def row_date(row):
    """Last DD.MM (month 09/10, 2026) scanning the cells from the last backwards, or None."""
    for cell in reversed(row["cells"][1:]):
        ms = list(DATE_RE.finditer(cell))
        if ms:
            m = ms[-1]
            return f"2026-{m.group(2)}-{m.group(1)}"
    return None


def parse_seed(path):
    """Seed Table A1 -> {B-id: {'F': 'F06', 'date': '2026-09-29'|None}}; a split parent
    (B-190) takes its first sub-item. Empty dict when the seed is absent."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}
    seed = {}
    rx = re.compile(r"^\| (B-\d+)([^\s|]*) \| ([^|]*?) \| (F\d\d) \|")
    for line in text.split("\n"):
        m = rx.match(line)
        if not m:
            continue
        bid = m.group(1)
        if bid in seed:
            continue
        d = re.fullmatch(r"(\d\d)\.(\d\d)", m.group(3).strip())
        seed[bid] = {"F": m.group(4), "date": f"2026-{d.group(2)}-{d.group(1)}" if d else None}
    return seed


def parse_seed_table_c(path):
    """Seed Table C -> [(package-relative path, F or 'n/c')]."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    out = []
    in_c = False
    rx = re.compile(r"^\| `([^`]+)` \| \d+ \| \d+ \| (F\d\d|n/c) \|")
    for line in text.split("\n"):
        if line.startswith("## "):
            in_c = line.startswith("## 3. Table C")
            continue
        if in_c:
            m = rx.match(line)
            if m:
                out.append((m.group(1), m.group(2)))
    return out


# ============================================================================================
# attribution
# ============================================================================================

def _tags(text: str, ids: set) -> list:
    seen = []
    for m in TAG_RE.finditer(text):
        t = "F" + m.group(1)
        if t in ids and t not in seen:
            seen.append(t)
    return seen


def _file_tokens(text: str, bare: bool) -> list:
    toks = [m.group(1) for m in BACKTICK_RE.finditer(text)]
    if bare:
        toks += [m.group(1) for m in BARE_PATH_RE.finditer(text)]
    return toks


def _features_of_tokens(tokens, index: FileIndex, features: list):
    """-> sorted registry indexes of the features the tokens' files belong to."""
    order = {f["id"]: i for i, f in enumerate(features)}
    found = set()
    for tok in tokens:
        for p in index.resolve(tok):
            fid = classify_path(features, p)
            if fid:
                found.add(order[fid])
    return sorted(found)


def _word_scores(text: str, features: list) -> list:
    low = text.lower()
    stages = [f"S{m.group(1)}" for m in STAGE_RE.finditer(text)]
    scores = []
    for f in features:
        s = 0
        for st in stages:
            if st in f["stages"]:
                s += 1
        for w in f["words"]:
            if w and w in low:
                s += 1
        scores.append(s)
    return scores


def attribute_text(text: str, features: list, index: FileIndex, *, bare_paths=False,
                   allow_words=True, seed_feature=None):
    """Order: (1) F\\d\\d tag, (2) files named, (3) stage/feature words, (4) the seed,
    (5) none. Returns {'feature', 'by', 'also'}."""
    ids = {f["id"] for f in features}
    tags = _tags(text, ids)
    if tags:
        return {"feature": tags[0], "by": "tag", "also": tags[1:]}
    idxs = _features_of_tokens(_file_tokens(text, bare_paths), index, features)
    if idxs:
        return {"feature": features[idxs[0]]["id"], "by": "files", "also": [features[i]["id"] for i in idxs[1:]]}
    if allow_words:
        scores = _word_scores(text, features)
        best = max(scores) if scores else 0
        if best > 0:
            i = scores.index(best)
            return {"feature": features[i]["id"], "by": "words", "also": []}
    if seed_feature and seed_feature in ids:
        return {"feature": seed_feature, "by": "seed", "also": []}
    return {"feature": None, "by": "none", "also": []}


def attribute_rows(rows: list, features: list, index: FileIndex, seed: dict) -> list:
    out = []
    for r in rows:
        s = seed.get(r["id"])
        full = " ".join([r["text"], r["source"], r["status"]])
        a = attribute_text(full, features, index, seed_feature=s["F"] if s else None)
        d = row_date(r) or (s["date"] if s else None)
        rec = dict(a)
        rec.update({
            "id": r["id"], "line": r["line"], "date": d,
            "closed": bool(CLOSED_RE.search(full)),
            "live": bool(LIVE_RE.search(r["text"] + " " + r["source"])),
            "fixfix": bool(FIXFIX_RE.search(r["text"])),
            "seed": s["F"] if s else None,
        })
        out.append(rec)
    return out


def row_tag_warnings(rows: list, ids: set) -> list:
    """One WARN line per backlog row that carries a bracketed tag ([F99]) the registry does not know. The row is attributed
    as if the tag were not there (the tag is ignored, never an offender); the line says so, as a finding's does."""
    out = []
    for r in rows:
        unknown = unknown_bracket_tags(" ".join([r["text"], r["source"], r["status"]]), ids)
        if unknown:
            out.append(f"WARN row {r['id']} (line {r['line']}): unknown feature {', '.join(unknown)} (not in {REGISTRY_REL}) "
                       "-- the tag is ignored; register the feature or fix the tag")
    return out


# ============================================================================================
# findings (plans/piles/<slug>/findings/*.md) -- the rows of the world after the BACKLOG freeze
# ============================================================================================

def unknown_bracket_tags(text: str, ids: set) -> list:
    """The bracketed tags ([F99]) in the text that the registry does not know, sorted. Only this form can be called unknown:
    a bare F12 in prose is no claim of a feature. Attribution ignores them; the callers warn."""
    return sorted({"F" + n for n in BRACKET_TAG_RE.findall(text)} - ids)


def attribute_finding(text: str, card_feature, ids: set) -> dict:
    """Order: (a) a Fnn tag of the registry in the text, (b) the pile card's first feature,
    (c) none = unclassified. A bracketed tag the registry does not know ([F99]) is returned in `unknown` either way;
    with no registered tag beside it the finding ends in (c) -- the card is not asked then.
    Returns {'feature', 'by', 'unknown'}."""
    tags = _tags(text, ids)
    unknown = unknown_bracket_tags(text, ids)
    if tags:
        return {"feature": tags[0], "by": "tag", "unknown": unknown}
    if unknown:
        return {"feature": None, "by": "none", "unknown": unknown}
    if card_feature:
        return {"feature": card_feature, "by": "card", "unknown": []}
    return {"feature": None, "by": "none", "unknown": []}


def _card_feature(pile, ids: set, warnings: list):
    """The first feature of the pile card's `фичи:` line (piles.Card.features), or None: no card, `фичи: —`,
    or a first feature the registry does not know (one warning per pile, then its findings are unclassified)."""
    feats = pile.card.features if pile.card is not None else []
    if not feats:
        return None
    if feats[0] not in ids:
        warnings.append(f"WARN pile {pile.slug}: its card names feature {feats[0]} which is not in {REGISTRY_REL} "
                        "-- its findings are attributed by their own tags only")
        return None
    return feats[0]


def _finding_record(f, slug: str, card_feature, ids: set) -> dict:
    """One finding (piles.Finding) as a record. An unreadable one is unclassified and the card is not asked for it; it carries
    ONE warning (not also the header one). Otherwise the text is the Finding's own (f.text) -- no file is opened here."""
    if f.unreadable:
        a, warns = {"feature": None, "by": "none", "unknown": []}, [
            f"WARN finding {f.path}: unreadable ({f.unreadable}) -- unclassified; save it as UTF-8"]
    else:
        a, warns = attribute_finding(f.text, card_feature, ids), []
        if f.errors:
            warns.append(f"WARN finding {f.path}: header problem(s) -- " + "; ".join(f.errors))
        if a["unknown"]:
            warns.append(f"WARN finding {f.path}: unknown feature {', '.join(a['unknown'])} (not in {REGISTRY_REL}) -- "
                         + (f"ignored; attributed by tag {a['feature']}" if a["by"] == "tag" else "unclassified"))
    return {"path": f.path, "pile": slug, "name": f.name, "feature": a["feature"], "by": a["by"], "warnings": warns}


def load_findings(root, ids: set):
    """-> (records | None, warnings, closed ids). None = no finding to speak of: no plans/piles directory (old clones,
    tmp trees) or a tree piles.load_tree cannot read (that one reason comes back as a warning, never a
    crash). A record per finding file: {'path', 'pile', 'name', 'feature', 'by', 'warnings'}; a finding
    with header errors (piles.Finding.errors) is a record like any other, carrying ONE warning that names
    the file. The tree is read by piles.load_tree (tolerant: a finding that is not UTF-8 is named, the others are read);
    the closed ids are the BACKLOG's (a closed id's finding file was deleted by a close, not renamed)."""
    root = Path(root)
    if not (root / PILES_REL).is_dir():
        return None, [], set()
    import piles    # lazy: tools/piles.py imports this module at load time
    try:
        tree = piles.load_tree(root, tolerant=True)
        out, load_warnings = [], []
        for slug in sorted(tree.piles):
            pile = tree.piles[slug]
            card_feature = _card_feature(pile, ids, load_warnings)
            out += [_finding_record(f, slug, card_feature, ids) for f in pile.findings]
        return out, load_warnings, set(tree.backlog.closed_ids)
    except piles.CannotRun as e:
        return None, [f"WARN findings not read: {e}"], set()


def renamed_finding_paths(current, base_paths: set, closed_ids: set) -> set:
    """The current finding paths that are the RENAME of a base path, not a new finding (a finding gets `B-nnn-<slug>.md` for
    its `yyyymmdd-<slug>.md` when a batch is assembled). Paired on (pile, slug) -- the slug is a group of
    piles.FINDING_NAME_RE -- and ONLY when that (pile, slug) has exactly one unmatched current path and exactly one unmatched base
    path: with two on a side the pairing would be a guess, and both count as new. An empty slug or a name the pattern rejects is
    never paired; a base file whose id the BACKLOG has closed was deleted by a close, it is no rename source."""
    import piles
    ours, theirs = set(current), set(base_paths)

    def parts(path):
        """-> (pile, slug, the B-id of the name or "")"""
        m = piles.FINDING_NAME_RE.match(path.rsplit("/", 1)[-1])
        return (path.split("/")[2], m.group("slug") or "", m.group(1) or "") if m else (None, "", "")

    added, gone = {}, {}
    for p in sorted(ours - theirs):
        added.setdefault(parts(p)[:2], []).append(p)
    for q in sorted(theirs - ours):
        if parts(q)[2] not in closed_ids:
            gone.setdefault(parts(q)[:2], []).append(q)
    return {ps[0] for (pile, slug), ps in added.items() if slug and len(ps) == 1 and len(gone.get((pile, slug), [])) == 1}


def base_finding_paths(root, sha) -> set:
    """The finding files of the base commit (git ls-tree); empty when the base predates plans/piles."""
    out = _run_git(root, "ls-tree", "-r", "--name-only", sha, "--", PILES_REL)
    return {l for l in (out or "").split("\n") if FINDING_PATH_RE.match(l)}


# ============================================================================================
# journal
# ============================================================================================

def parse_journal_text(raw: bytes):
    """-> (events, skipped_line_numbers); an event is a dict + '_line'."""
    events, skipped = [], []
    for lineno, bline in enumerate(raw.split(b"\n"), 1):
        if not bline.strip():
            continue
        try:
            obj = json.loads(bline.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            skipped.append(lineno)
            continue
        if not isinstance(obj, dict):
            skipped.append(lineno)
            continue
        obj["_line"] = lineno
        events.append(obj)
    return events, skipped


def parse_journal(path):
    try:
        raw = Path(path).read_bytes()
    except OSError:
        return [], []
    return parse_journal_text(raw)


def _task_key(e: dict, segs):
    """(label, task_id) of a task event: the declared instance's label, "" for every undeclared
    line (and for all lines when there is no declaration)."""
    tid = e.get("task_id")
    if _jk is None or segs is None:
        return ("", tid)
    return _jk.task_key(e, segs) or ("", tid)


def attribute_events(events: list, features: list, index: FileIndex, segments=None, journal=None) -> list:
    """Per task event: (1) `feature` field (an unknown value is UNCLASSIFIED, not that
    value), (2) F\\d\\d tag in notes, (3) paths in notes, (4) the task instance's other
    events (the `delegated` first), (5) unclassified. A task instance is keyed by the TASK KEY
    of tools/journal_keys.py, (label, task_id): two clones that issued the same t-NNN are two
    instances once logs/journal-segments.json declares the foreign one; an undeclared collision
    is glued into one (the same reading the hooks have), so the numbers never depend on a guess
    about worker refs. `segments` = the Segments of journal_keys (None = no declaration, every
    key bare); compute() loads them from its `root`. A defect_found `ref` resolves through
    journal_keys.ref_key."""
    ids = {f["id"] for f in features}
    own = []
    instances = {}     # key -> [event index]
    for i, e in enumerate(events):
        ev = e.get("event")
        tid = e.get("task_id")
        rec = {"line": e["_line"], "event": ev, "task_id": tid, "ts": e.get("ts") or "",
               "feature": None, "by": "none", "invalid": None, "key": None}
        if ev in TASK_EVENTS and isinstance(tid, str) and tid:
            cur = _task_key(e, segments)
            rec["key"] = cur
            instances.setdefault(cur, []).append(i)
        notes = e.get("notes") if isinstance(e.get("notes"), str) else ""
        fv = e.get("feature")
        if fv is not None and fv != "":
            if isinstance(fv, str) and fv in ids:
                rec.update(feature=fv, by="field")
            else:
                rec.update(invalid=str(fv), by="invalid")
        else:
            tags = _tags(notes, ids)
            if tags:
                rec.update(feature=tags[0], by="tag")
            else:
                idxs = _features_of_tokens(_file_tokens(notes, True), index, features)
                if idxs:
                    rec.update(feature=features[idxs[0]]["id"], by="files")
        own.append(rec)
    for key, idxs in instances.items():
        # inherit: the instance feature = the first attributed event, `delegated` preferred
        order = sorted(idxs, key=lambda i: (events[i].get("event") != "delegated", i))
        inherited = next((own[i]["feature"] for i in order if own[i]["feature"]), None)
        if inherited:
            for i in idxs:
                if own[i]["feature"] is None and own[i]["by"] == "none":
                    own[i]["feature"] = inherited
                    own[i]["by"] = "task"
    # a defect_found also inherits from the task it points at (ref)
    by_task = {}
    for i, rec in enumerate(own):
        if rec["feature"] and rec["task_id"] and isinstance(rec["task_id"], str):
            # every event that carries a task_id counts (not only the TASK_EVENTS), as before
            by_task.setdefault(rec["key"] or _task_key(events[i], segments), rec["feature"])
    for i, rec in enumerate(own):
        if rec["event"] == "defect_found" and rec["feature"] is None and rec["by"] == "none":
            ref = events[i].get("ref")
            if not isinstance(ref, str):
                continue
            if _jk is not None and segments is not None:
                ref_key = (_jk.ref_key(ref, events[i], segments, journal.label_ids, journal.aliases)
                           if journal is not None else _jk.ref_key(ref, events[i], segments))
            else:
                ref_key = ("", ref)
            if ref_key is not None and ref_key in by_task:
                rec["feature"] = by_task[ref_key]
                rec["by"] = "ref"
    return own


# ============================================================================================
# git facts
# ============================================================================================

def _since(window: str) -> str:
    return window if re.search(r"\d\d:\d\d", window) else window + " 00:00"


def collect_commits(root, window: str, pathspec):
    """git log --since=<window> --name-only over pathspec -> list of
    {'hash','date','files'} (newest first), or None when git is unavailable."""
    out = _run_git(root, "log", f"--since={_since(window)}", "--name-only", "--format=@%h %cs", "--", *pathspec)
    if out is None:
        return None
    commits = []
    cur = None
    for line in out.split("\n"):
        if not line:
            continue
        if line.startswith("@"):
            h, _, d = line[1:].partition(" ")
            cur = {"hash": h, "date": d, "files": []}
            commits.append(cur)
        elif cur is not None:
            cur["files"].append(line)
    return commits


def iso_week(date_str):
    try:
        y, w, _d = datetime.date.fromisoformat(date_str).isocalendar()
    except (TypeError, ValueError):
        return None
    return f"{y}-W{w:02d}"


# ============================================================================================
# metrics
# ============================================================================================

def average_ranks(values: list) -> list:
    """Ascending ranks (rank 1 = lowest value); ties share the average rank."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def compute(root=ROOT, window=DEFAULT_WINDOW, use_seed=True, features=None, registry_path=None):
    root = Path(root)
    if features is None:
        features = load_registry(registry_path or (root / REGISTRY_REL))
    order = {f["id"]: i for i, f in enumerate(features)}
    fids = sorted(order)

    # --- files ---
    pkg_files = package_files(root)
    tracked = tracked_files(root)
    repo_other = [p for p in (tracked or []) if not p.startswith(PACKAGE + "/")]
    index_paths = set(pkg_files) | set(tracked or [])
    if tracked is None:
        for d in ("tools", "docs", "plans", ".claude"):
            index_paths |= set(walk_files(root, d))
    index = FileIndex(index_paths)

    unclassified_disk = [p for p in pkg_files if classify_path(features, p) is None]
    unclassified_repo = [p for p in repo_other if classify_path(features, p) is None]
    overlaps = find_overlaps(features, pkg_files)

    # --- rows ---
    rows, skipped_rows = parse_backlog(root / BACKLOG_REL)
    seed_path = root / SEED_REL
    seed = parse_seed(seed_path) if use_seed else {}
    seed_note = ("used" if seed else "absent") if use_seed else "disabled (--no-seed)"
    rrows = attribute_rows(rows, features, index, seed)

    # --- findings (None = no plans/piles: every findings key below is then left out) ---
    frecs, fwarns, _closed = load_findings(root, set(order))
    # a report has no base, so every row is a current one: an unknown [Fnn] tag in any of them is named
    for w in row_tag_warnings(rows, set(order)) + fwarns + [w for r in (frecs or []) for w in r["warnings"]]:
        print(f"forge_metrics: {w}", file=sys.stderr)

    # --- journal ---
    journal = _jk.load_all(root) if _jk is not None else None
    if journal is not None:
        # t-581: every journal file through the one loader; an event keeps the label of its file
        # (journal_keys.LabeledEvent), `_line` is its line number in its own file
        events = []
        for r in journal.rows:
            if r.obj is not None:
                r.obj["_line"] = r.line_no
                events.append(r.obj)
        skipped_events = [r.line_no for r in journal.rows if r.obj is None]
        segments, segments_reason = journal.segments, journal.segments_reason
    else:
        events, skipped_events = parse_journal(root / JOURNAL_REL)
        segments, segments_reason = None, "journal_keys is not importable"
    if segments_reason:     # never raises, never blocks: a broken declaration reads as none (ids glued)
        print(f"forge_metrics: the task-key declaration is unreadable ({segments_reason}) -- colliding "
              "task ids are read as one task", file=sys.stderr)
    win_day = _since(window)[:10]
    evs = [e for e in attribute_events(events, features, index, segments, journal=journal)
           if e["event"] in TASK_EVENTS and e["ts"][:10] >= win_day]

    # --- git ---
    pkg_commits = collect_commits(root, window, [PACKAGE])
    doc_commits = collect_commits(root, window, [p.rstrip("/") for p in PROCESS_DOC_PREFIXES])
    git_ok = pkg_commits is not None
    unclassified_commit_files = set()
    rework = {fid: 0 for fid in fids}
    file_counts = {fid: {} for fid in fids}
    wide = []
    weekly_commits = {}
    if git_ok:
        for c in pkg_commits:
            touched = set()
            nfiles = 0
            for fpath in sorted(set(c["files"])):
                nfiles += 1
                fid = classify_path(features, fpath)
                if fid is None:
                    unclassified_commit_files.add(fpath)
                    continue
                touched.add(fid)
                file_counts[fid][fpath] = file_counts[fid].get(fpath, 0) + 1
            for fid in touched:
                rework[fid] += 1
            if nfiles >= WIDE_COMMIT_FILES:
                wide.append((c["hash"], nfiles))
            wk = iso_week(c["date"])
            if wk:
                weekly_commits[wk] = weekly_commits.get(wk, 0) + 1
    weekly_docs = {}
    if doc_commits is not None:
        for c in doc_commits:
            wk = iso_week(c["date"])
            if wk:
                weekly_docs[wk] = weekly_docs.get(wk, 0) + 1
    weekly_rows = {}
    undated_rows = 0
    for r in rrows:
        wk = iso_week(r["date"])
        if wk:
            weekly_rows[wk] = weekly_rows.get(wk, 0) + 1
        else:
            undated_rows += 1

    # --- per feature ---
    per = {}
    for fid in fids:
        mine = [r for r in rrows if r["feature"] == fid]
        fev = [e for e in evs if e["feature"] == fid]
        top = sorted(file_counts[fid].items(), key=lambda kv: (-kv[1], kv[0]))[:3]
        per[fid] = {
            "name": features[order[fid]]["name"],
            "rows_total": len(mine),
            "rows_open": sum(1 for r in mine if not r["closed"]),
            "found_live": sum(1 for r in mine if r["live"]),
            "fixfix_rows": sum(1 for r in mine if r["fixfix"]),
            "defect_found": sum(1 for e in fev if e["event"] == "defect_found"),
            "rejected": sum(1 for e in fev if e["event"] == "rejected"),
            "rework_commits": rework[fid] if git_ok else None,
            "top_files": [{"file": f, "commits": n} for f, n in top] if git_ok else None,
        }
        p = per[fid]
        if frecs is not None:
            p["findings_total"] = sum(1 for r in frecs if r["feature"] == fid)
        p["found_live_share"] = round(p["found_live"] / p["rows_total"], 2) if p["rows_total"] else 0.0
        p["fix_of_fix"] = p["defect_found"] + p["fixfix_rows"]

    metric_keys = ["rows_open", "found_live_share", "fix_of_fix"] + (["rework_commits"] if git_ok else [])
    rank_sum = {fid: 0.0 for fid in fids}
    for k in metric_keys:
        for fid, rk in zip(fids, average_ranks([per[f][k] for f in fids])):
            rank_sum[fid] += rk
    for fid in fids:
        per[fid]["fragility_index"] = round(rank_sum[fid], 1)
    desc = sorted(fids, key=lambda f: (-per[f]["fragility_index"], f))
    pos = {}
    prev = None
    for n, fid in enumerate(desc, 1):
        if prev is not None and per[fid]["fragility_index"] == per[prev]["fragility_index"]:
            pos[fid] = pos[prev]
        else:
            pos[fid] = n
        prev = fid
    for fid in fids:
        per[fid]["fragility_order"] = pos[fid]

    # --- unclassified rows / events ---
    unc_rows = [r["id"] for r in rrows if r["feature"] is None]
    unc_events = [f"{e['task_id'] or e['event']}@{e['line']}" for e in evs if e["feature"] is None]
    invalid_feature_events = [f"{e['task_id'] or e['event']}@{e['line']}={e['invalid']}" for e in evs if e["invalid"]]

    # seed agreement (quality line)
    comparable = [r for r in rrows if r["by"] in ("files", "words") and r["seed"]]
    agree = sum(1 for r in comparable if r["feature"] == r["seed"])

    n_pkg = len(pkg_commits) if git_ok else None
    n_doc = len(doc_commits) if doc_commits is not None else None
    tax = (round(n_doc / n_pkg, 2) if (n_pkg and n_doc is not None) else None)

    weeks = sorted(set(weekly_rows) | set(weekly_commits) | set(weekly_docs))
    data = {
        "window": window,
        "window_since": _since(window),
        "git": "ok" if git_ok else "n/d",
        "seed": seed_note,
        "registry": REGISTRY_REL,
        "features": per,
        "unclassified": {
            "package_files_on_disk": {"count": len(unclassified_disk), "names": unclassified_disk},
            "repo_files_tracked": {"count": len(unclassified_repo), "names": unclassified_repo},
            "files_in_window_commits": ({"count": len(unclassified_commit_files), "names": sorted(unclassified_commit_files)}
                                        if git_ok else None),
            "rows": {"count": len(unc_rows), "names": unc_rows},
            "events": {"count": len(unc_events), "names": unc_events},
            "events_with_unknown_feature": {"count": len(invalid_feature_events), "names": invalid_feature_events},
        },
        "overlaps": overlaps,
        "totals": {
            "rows": len(rrows), "rows_open": sum(1 for r in rrows if not r["closed"]),
            "rows_by": {k: sum(1 for r in rrows if r["by"] == k) for k in ("tag", "files", "words", "seed", "none")},
            "events_in_window": len(evs),
            "package_commits": n_pkg, "process_doc_commits": n_doc, "process_tax": tax,
            "wide_commits": [{"hash": h, "files": n} for h, n in wide],
            "skipped_backlog_lines": skipped_rows, "skipped_journal_lines": skipped_events,
            "seed_agreement": {"agree": agree, "compared": len(comparable)},
            "rank_metrics": metric_keys,
        },
        "weekly": [{"week": w, "rows": weekly_rows.get(w, 0), "package_commits": weekly_commits.get(w, 0) if git_ok else None,
                    "process_doc_commits": weekly_docs.get(w, 0) if doc_commits is not None else None} for w in weeks],
        "rows_without_date": undated_rows,
    }
    if frecs is not None:
        unc = [f"{r['pile']}/{r['name']}" for r in frecs if r["feature"] is None]
        data["unclassified"]["findings"] = {"count": len(unc), "names": unc}
        data["totals"]["findings"] = len(frecs)
        data["totals"]["findings_by"] = {k: sum(1 for r in frecs if r["by"] == k) for k in ("tag", "card", "none")}
    return data


# ============================================================================================
# report
# ============================================================================================

def _bucket(lines: list, title: str, b) -> None:
    if b is None:
        lines.append(f"- {title}: n/d (git unavailable)")
        return
    names = ", ".join(f"`{n}`" for n in b["names"][:TOP_N]) or "-"
    more = f" (+{b['count'] - TOP_N} more)" if b["count"] > TOP_N else ""
    lines.append(f"- {title}: **{b['count']}** - {names}{more}")


def _fmt(v):
    return "n/d" if v is None else str(v)


def render_markdown(d: dict) -> str:
    L = []
    L.append("# Forge metrics (generated, do not edit)")
    L.append("")
    L.append(f"Generated by `python tools/forge_metrics.py --write`; deterministic for a given repo state "
             f"(no clock in the body). Window: commits and journal events since **{d['window_since']}**. "
             f"Registry: `{d['registry']}`. Seed `{SEED_REL}`: {d['seed']}. Git: {d['git']}.")
    L.append("")
    L.append("Counting commands:")
    L.append("")
    L.append(f"- package commits: `git log --since=\"{d['window_since']}\" --name-only --format=\"@%h %cs\" -- {PACKAGE}`")
    L.append(f"- process commits: `git log --since=\"{d['window_since']}\" --name-only --format=\"@%h %cs\" -- docs plans`")
    has_f = "findings" in d["totals"]
    L.append(f"- rows: every line starting `| B-nnn |` of `{BACKLOG_REL}` (sub-items count as one row); events: every task event of `{JOURNAL_REL}` dated in the window"
             + (f"; findings: every `*.md` under `{PILES_REL}/*/findings/` (a Fnn tag in its text, else the first feature of its pile card's "
                "`фичи:` line, else unclassified)" if has_f else ""))
    L.append(f"- found live: row text or source matches `{'|'.join(LIVE_WORDS)}`; fix-of-fix: `defect_found` events + rows matching `{'|'.join(FIXFIX_WORDS)}`; "
             f"open: no closure mark (`{'|'.join(CLOSED_WORDS)}`) anywhere in the row")
    L.append("")
    L.append("## Unclassified (fix these first: a new feature announces itself here)")
    L.append("")
    u = d["unclassified"]
    _bucket(L, "package files on disk matching no feature", u["package_files_on_disk"])
    _bucket(L, "other tracked repo files matching no feature", u["repo_files_tracked"])
    _bucket(L, "files in window commits matching no feature (may include deleted files)", u["files_in_window_commits"])
    _bucket(L, "backlog rows with no attribution", u["rows"])
    if has_f:
        _bucket(L, "findings with no attribution", u["findings"])
    _bucket(L, "journal events with no attribution", u["events"])
    _bucket(L, "journal events carrying a `feature` value not in the registry", u["events_with_unknown_feature"])
    L.append("")
    L.append(f"Overlaps (two features match one package file with equal specificity, or order puts a general glob first): **{len(d['overlaps'])}**"
             + ("" if not d["overlaps"] else " - " + ", ".join(f"`{o['path']}` ({o['kind']}: {'/'.join(o['features'])})" for o in d["overlaps"][:TOP_N])))
    L.append("")
    L.append("## Per feature")
    L.append("")
    L.append("Fragility index = sum of ascending ranks (1 = fewest) over open rows, found-live share, fix-of-fix, rework"
             + ("" if "rework_commits" in d["totals"]["rank_metrics"] else " (rework left out: git n/d)")
             + "; **lower is better**; `order` 1 = the most fragile (highest index).")
    L.append("")
    L.append("| F | feature | rows |" + (" findings |" if has_f else "") + " open | found live | live % | fix-of-fix | rework commits | top 3 files (commits) | rejected | index | order |")
    L.append("|---|---|---|" + ("---|" if has_f else "") + "---|---|---|---|---|---|---|---|---|")
    tot = {"rows": 0, "open": 0, "live": 0, "ff": 0, "rw": 0, "rej": 0, "find": 0}
    for fid in sorted(d["features"]):
        p = d["features"][fid]
        pre = PACKAGE + "/"
        top = ("; ".join(f"`{t['file'][len(pre):] if t['file'].startswith(pre) else t['file']}` x{t['commits']}"
                         for t in (p["top_files"] or [])) if p["top_files"] is not None else "n/d")
        fcell = f" {p['findings_total']} |" if has_f else ""
        tot["find"] += p.get("findings_total", 0)
        L.append(f"| {fid} | {p['name']} | {p['rows_total']} |{fcell} {p['rows_open']} | {p['found_live']} | "
                 f"{round(p['found_live_share'] * 100)}% | {p['fix_of_fix']} ({p['defect_found']}+{p['fixfix_rows']}) | "
                 f"{_fmt(p['rework_commits'])} | {top or '-'} | {p['rejected']} | {p['fragility_index']} | {p['fragility_order']} |")
        tot["rows"] += p["rows_total"]
        tot["open"] += p["rows_open"]
        tot["live"] += p["found_live"]
        tot["ff"] += p["fix_of_fix"]
        tot["rw"] += p["rework_commits"] or 0
        tot["rej"] += p["rejected"]
    L.append(f"| | **total (attributed)** | {tot['rows']} |{' ' + str(tot['find']) + ' |' if has_f else ''} {tot['open']} | {tot['live']} | | {tot['ff']} | {tot['rw'] if d['git'] == 'ok' else 'n/d'} | | {tot['rej']} | | |")
    L.append("")
    t = d["totals"]
    L.append(f"Rows: {t['rows']} parsed ({t['rows_open']} open); attributed by tag {t['rows_by']['tag']}, files {t['rows_by']['files']}, "
             f"words {t['rows_by']['words']}, seed {t['rows_by']['seed']}, none {t['rows_by']['none']}. "
             f"Seed agreement on rows attributed by files/words: {t['seed_agreement']['agree']} of {t['seed_agreement']['compared']}. "
             f"Journal events in the window: {t['events_in_window']}.")
    if has_f:
        fb = t["findings_by"]
        L.append(f"Findings: {t['findings']} parsed; attributed by tag {fb['tag']}, pile card {fb['card']}, none {fb['none']}.")
    if t["skipped_backlog_lines"]:
        L.append(f"Backlog lines skipped (non-UTF-8): {t['skipped_backlog_lines']}.")
    if t["skipped_journal_lines"]:
        L.append(f"Journal lines skipped (not UTF-8 JSON objects): {t['skipped_journal_lines']}.")
    L.append("")
    if t["package_commits"] is None:
        L.append("Process tax: n/d (git unavailable).")
    else:
        L.append(f"Process tax: {t['process_doc_commits']} commits touching `docs/` or `plans/` per {t['package_commits']} package commits = "
                 f"{_fmt(t['process_tax'])}.")
        if t["wide_commits"]:
            L.append("Wide commits counted once per file they touch (they inflate rework): "
                     + ", ".join(f"`{w['hash']}` ({w['files']} files)" for w in t["wide_commits"]) + ".")
    L.append("")
    L.append("## Per week (ISO week)")
    L.append("")
    L.append("| week | new backlog rows (by row date) | package commits | process commits (docs, plans) |")
    L.append("|---|---|---|---|")
    for w in d["weekly"]:
        L.append(f"| {w['week']} | {w['rows']} | {_fmt(w['package_commits'])} | {_fmt(w['process_doc_commits'])} |")
    L.append(f"| n/d | {d['rows_without_date']} | | |")
    L.append("")
    return "\n".join(L)


# ============================================================================================
# --check
# ============================================================================================

def resolve_base(root, base):
    """Explicit --base must resolve; default = merge-base(HEAD, main), else HEAD~1."""
    def rev(ref):
        out = _run_git(root, "rev-parse", "--verify", "--quiet", ref + "^{commit}")
        return out.strip() if out else None
    if base:
        sha = rev(base)
        if not sha:
            raise BaseError(f"base {base!r} does not resolve to a commit in {root}; pass --base <ref>")
        return sha
    if rev("main"):
        out = _run_git(root, "merge-base", "HEAD", "main")
        if out and out.strip():
            return out.strip()
    sha = rev("HEAD~1")
    if sha:
        return sha
    raise BaseError("no main branch and no HEAD~1 to compare against; pass --base <ref>")


def _show(root, base, rel):
    out = _run_git(root, "show", f"{base}:{rel}")
    return out if out is not None else ""


def _journal_paths(root, sha) -> list:
    """Every journal path of the current tree (disk) and of the base commit `sha`: the history first,
    then logs/journal/<slug>.jsonl in name order. A file only the base has is listed too (its lines
    cannot be new, so nothing is reported for it)."""
    paths = {JOURNAL_REL}
    if _jk is None:
        return [JOURNAL_REL]
    cur = [f"{_jk.JOURNAL_DIR_REL}/{p.name}" for p in (root / _jk.JOURNAL_DIR_REL).glob("*.jsonl") if p.is_file()] \
        if (root / _jk.JOURNAL_DIR_REL).is_dir() else []
    base_out = _run_git(root, "ls-tree", "-r", "--full-tree", "--name-only", sha, "--", _jk.JOURNAL_DIR_REL) or ""
    paths.update(f.path for f in _jk.journal_names(cur + [l for l in base_out.split("\n") if l])[0])
    return [JOURNAL_REL] + sorted(paths - {JOURNAL_REL})


def _findings_check(root, ids: set, sha):
    """(a2) the finding files of the world after the BACKLOG freeze: -> (new findings, warning lines). The new findings are
    None when there is no plans/piles (or an unreadable tree: no findings keys, the line reads as before). Never an offender:
    an unclassified finding is a Forge metric (host adaptation 4), printed by render_check. A base that predates plans/piles
    has no finding file, so every current one is new -- correct, not a fault. A rename is not a new finding; it still warns."""
    frecs, fwarns, closed_ids = load_findings(root, ids)
    base_f = base_finding_paths(root, sha) if frecs else set()
    fresh = [r for r in (frecs or []) if r["path"] not in base_f]
    renamed = renamed_finding_paths([r["path"] for r in frecs or []], base_f, closed_ids) if fresh else set()
    new_findings = [r for r in fresh if r["path"] not in renamed]
    return (None if frecs is None else new_findings), fwarns + [w for r in fresh for w in r["warnings"]]


def run_check(root=ROOT, base=None, features=None):
    """-> (offenders: list[(kind, name, what)], counts: dict of numbers (plus the unclassified finding paths), base_sha,
    warnings: the lines render_check prints under the verdict, which never decide the exit code)."""
    root = Path(root)
    features = features if features is not None else load_registry(root / REGISTRY_REL)
    ids = {f["id"] for f in features}
    sha = resolve_base(root, base)

    cur_files = set(package_files(root))
    out = _run_git(root, "ls-tree", "-r", "--name-only", sha, "--", PACKAGE)
    base_files = set(l for l in (out or "").split("\n") if l)
    tracked = tracked_files(root) or []
    index = FileIndex(cur_files | set(tracked))

    offenders = []
    # (a) new backlog rows with neither a tag nor a file the globs match
    base_rows, _ = parse_backlog_text(_show(root, sha, BACKLOG_REL).encode("utf-8"))
    base_ids = {r["id"] for r in base_rows}
    cur_rows, _ = parse_backlog(root / BACKLOG_REL)
    new_rows = [r for r in cur_rows if r["id"] not in base_ids]
    bad_rows = 0
    for r in new_rows:
        a = attribute_text(" ".join([r["text"], r["source"], r["status"]]), features, index, allow_words=False)
        if a["feature"] is None:
            bad_rows += 1
            offenders.append(("a", r["id"], f"new backlog row {r['id']} (line {r['line']}) has no attribution (no F\\d\\d tag, no file a glob matches)"))
    row_warnings = row_tag_warnings(new_rows, ids)
    # (a2) new finding files
    new_findings, fwarns = _findings_check(root, ids, sha)
    # (b) new package files matching no feature
    new_files = sorted(cur_files - base_files)
    bad_files = 0
    for p in new_files:
        if classify_path(features, p) is None:
            bad_files += 1
            offenders.append(("b", p, f"new package file {p} matches no feature"))
    # (c) new journal events dated FEATURE_FROM or later without a feature
    # CR is stripped on both sides: a Windows checkout (core.autocrlf=true) has CRLF on disk and LF
    # in the base commit, and the same event must not read as new because of its line ending
    # t-581: EVERY journal path of the current tree and of the base -- the history and each
    # logs/journal/<slug>.jsonl; a file the base lacks has all its lines new. The history's offenders
    # keep their old name (`line N ...`), a developer file's carry the path (`<rel> line N ...`).
    new_events = 0
    bad_events = 0
    for rel in _journal_paths(root, sha):
        base_lines = {l.rstrip("\r") for l in _show(root, sha, rel).split("\n")}
        try:
            cur_lines = (root / rel).read_bytes().split(b"\n")
        except OSError:
            cur_lines = []
        prefix = "" if rel == JOURNAL_REL else rel + " "
        for lineno, bl in enumerate(cur_lines, 1):
            try:
                text = bl.decode("utf-8").rstrip("\r")
            except UnicodeDecodeError:
                continue
            if not text.strip() or text in base_lines:
                continue
            try:
                obj = json.loads(text)
            except ValueError:
                continue
            if not isinstance(obj, dict) or obj.get("event") not in FEATURE_EVENTS:
                continue
            if not isinstance(obj.get("ts"), str) or obj["ts"][:10] < FEATURE_FROM:
                continue
            new_events += 1
            fv = obj.get("feature")
            name = f"{prefix}line {lineno} {obj.get('event')} {obj.get('task_id') or ''}".strip()
            if fv in (None, ""):
                bad_events += 1
                offenders.append(("c", name, f"new journal event ({name}) has no `feature` field"))
            elif fv not in ids:
                bad_events += 1
                offenders.append(("c", name, f"new journal event ({name}) names feature {fv!r} that is not in {REGISTRY_REL}"))
    counts = {"new_rows": len(new_rows), "rows_unattributed": bad_rows,
              "new_package_files": len(new_files), "files_unclassified": bad_files,
              "new_events": new_events, "events_without_feature": bad_events}
    if new_findings is not None:       # no plans/piles (or an unreadable tree): no findings keys, the line reads as before
        unc = [r["path"] for r in new_findings if r["feature"] is None]
        counts.update({"new_findings": len(new_findings), "findings_unclassified": len(unc),
                       "unclassified_finding_files": unc})
    return offenders, counts, sha, row_warnings + fwarns


_DOORS = {"a": DOOR_ROW, "b": DOOR_FILE, "c": DOOR_EVENT}


def _findings_part(counts) -> str:
    """'new findings M (all attributed)' / 'new findings M (K unclassified)'; '' when there is no plans/piles."""
    if "new_findings" not in counts:
        return ""
    k = counts["findings_unclassified"]
    return f"new findings {counts['new_findings']} (" + (f"{k} unclassified" if k else "all attributed") + ")"


def _findings_tail(counts, warnings) -> list:
    """The lines under the verdict that never decide the exit code: the unclassified findings (a Forge metric), then the
    `warnings` (the row tag warnings, then the finding warnings)."""
    unc = counts.get("unclassified_finding_files", [])
    L = [f"  unclassified finding (a Forge metric, not an offender): {p}" for p in unc[:TOP_N]]
    if len(unc) > TOP_N:
        L.append(f"  ... and {len(unc) - TOP_N} more unclassified findings")
    return L + [f"  {w}" for w in warnings]


def render_check(offenders, counts, sha, warn=False, warnings=()) -> str:
    head = "WARN" if warn else "forge_metrics --check"
    fpart = _findings_part(counts)
    if not offenders:
        L = [f"{head}: ok (base {sha[:7]}): new rows {counts['new_rows']} (all attributed), "
             + (fpart + ", " if fpart else "")
             + f"new package files {counts['new_package_files']} (all classified), "
             f"new journal events needing a feature {counts['new_events']} (all carry one)"]
        return "\n".join(L + _findings_tail(counts, warnings))
    L = [f"{head}: {len(offenders)} offender(s) against base {sha[:7]} "
         f"(new rows {counts['new_rows']}, " + (fpart + ", " if fpart else "")
         + f"new package files {counts['new_package_files']}, new events needing a feature {counts['new_events']})"]
    for kind in ("a", "b", "c"):
        mine = [o for o in offenders if o[0] == kind]
        if not mine:
            continue
        for _k, _name, what in mine:
            L.append(f"  - ({kind}) {what}")
        L.append(f"    door ({kind}): {_DOORS[kind]}")
    return "\n".join(L + _findings_tail(counts, warnings))


# ============================================================================================
# CLI
# ============================================================================================

def _utf8_stdio():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _normalize_window(w: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?", w):
        raise SystemExit(f"forge_metrics: --window must look like 2026-09-26 (or 'YYYY-MM-DD HH:MM'), got {w!r}")
    return w


def main(argv=None, root=None) -> int:
    _utf8_stdio()
    ap = argparse.ArgumentParser(prog="forge_metrics", description="Forge metrics: feature attribution of the work on the QA Factory package.")
    ap.add_argument("--window", default=DEFAULT_WINDOW, help="start of the window (default: the first comparative run, 2026-09-26)")
    ap.add_argument("--write", action="store_true", help=f"write {OUT_REL} instead of printing")
    ap.add_argument("--out", default=None, help="with --write: another output path (default plans/forge-metrics.md)")
    ap.add_argument("--json", action="store_true", help="print the same data as JSON")
    ap.add_argument("--no-seed", action="store_true", help="do not read the hand-made seed table")
    ap.add_argument("--check", action="store_true", help="name every NEW row/file/event without a feature; exit 1 on offenders; writes nothing")
    ap.add_argument("--base", default=None, help="--check: the ref to compare against (default: merge-base with main, else HEAD~1)")
    ap.add_argument("--warn", action="store_true", help="--check: print the same text, always exit 0")
    args = ap.parse_args(argv)
    root = Path(root) if root is not None else ROOT

    if args.check:
        try:
            offenders, counts, sha, warnings = run_check(root, args.base)
        except (RegistryError, BaseError) as e:
            print(f"forge_metrics --check: {e}", file=sys.stderr)
            return 0 if args.warn else 2
        except Exception as e:  # a WARN must never block a commit
            if not args.warn:
                raise
            print(f"WARN: forge_metrics --check could not run ({type(e).__name__}: {e})", file=sys.stderr)
            return 0
        text = render_check(offenders, counts, sha, warn=args.warn, warnings=warnings)
        print(text, file=sys.stderr if offenders and not args.warn else sys.stdout)
        if args.warn:
            return 0
        return 1 if offenders else 0

    try:
        data = compute(root, _normalize_window(args.window), use_seed=not args.no_seed)
    except RegistryError as e:
        print(f"forge_metrics: {e}", file=sys.stderr)
        return 2
    text = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=1) + "\n" if args.json else render_markdown(data)
    if args.write:
        out = Path(args.out) if args.out else root / OUT_REL
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(text.encode("utf-8"))
        print(f"forge_metrics: wrote {out} ({len(text)} chars)")
        return 0
    sys.stdout.write(text if text.endswith("\n") else text + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
