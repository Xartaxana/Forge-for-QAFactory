#!/usr/bin/env python3
"""Capture a story (a scrubbed slice of a real run of a SYNTHETIC task) and extract what the run recorded (TD-15.3).

    python tools/story_capture.py capture --source DIR --id ID [--cut-after-seq N] [--drop GLOB ...] [--package DIR]
    python tools/story_capture.py expected --id ID [--package DIR]
    python tools/story_capture.py residue --source DIR [DIR ...] --id ID [--drop GLOB ...] [--lines] [--package DIR]
    python tools/story_capture.py rescrub --id ID [--package DIR]

`capture` copies the task root (events up to the cut), turns Cyrillic into Latin, replaces the machine's absolute prefix by
`<stand>` and the home folder by `<home>`, re-chains the events through the package's `event_store.content_hash`, re-binds the
gate A decision through `Controller.gate_inputs` (when the root holds one), checks the result against
`tools/story-scrub-rules.json` and writes `story.json` and `README.txt`. Every refusal exits 1 and names file:line, the rule id
and the door. `expected` reads the recorded carriers of the story into `expected.json`. `rescrub` applies the repository-handle class
(`github.com/<handle>` -> `github.com/person-<n>`) and the rewrite rows flagged `residue` (the agent project folder name) to a
story already captured, in place; `residue` also counts those two classes (`residue-handle`, `residue-agent-project-folder`).
"""
import argparse
import fnmatch
import hashlib
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
RULES_PATH = TOOLS / "story-scrub-rules.json"
DEFAULT_PACKAGE = TOOLS.parent / "ai-packages" / "qa-factory"
LIMIT_BYTES = 4 * 1024 * 1024
STORIES = ("scripts", "tests", "fixtures", "stories")
FOLLOW_PASSES = 5    # the bound of the sha256 follow (a fixpoint, or a refusal naming the files still changing)
OWN_FILES = ("README.txt", "story.json", "expected.json")    # the tool's own files at the story root: not counted by the cap
ID_OK = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
# the Russian alphabet by code point, so this tool carries no Cyrillic character (FR-30)
LATIN = dict(zip(map(chr, range(0x430, 0x450)),
                 ["a", "b", "v", "g", "d", "e", "zh", "z", "i", "i", "k", "l", "m", "n", "o", "p",
                  "r", "s", "t", "u", "f", "kh", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya"]))
LATIN[chr(0x451)] = "e"
CYRILLIC = re.compile("[Ѐ-ӿ]")
DRIVE_PATH = re.compile(r"(?<![A-Za-z0-9_])[A-Za-z]:[\\/]")
STAND = re.compile(r"[A-Za-z]:[\\/]+AI[\\/]+Factory[\\/]+testproject1-dev-\d+")
HOME = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[^\\/\"\s]+|(?<![\w.>-])/(?:home|Users)/[^\\/\"\s]+", re.I)
# any other absolute root: a drive path (or its git-bash /c/ form) and up to three folders under the drive; the tail stays
_SEP = r"[\\/]+"
_COMP = r"[^\\/\"'\s:*?<>|,;()\[\]{}`]+"
FOREIGN = re.compile(r"(?:(?<![A-Za-z0-9_])[A-Za-z]:|(?<![\w.>-])/[a-z](?=/AI/))" + _SEP + _COMP + "(?:" + _SEP + _COMP + "){0,2}")
STAGES = ["S%d" % n for n in range(10)]
TEXT_SUFFIXES = (".json", ".jsonl", ".md", ".txt", ".yaml", ".yml")
ID_TOKEN = re.compile(r"\b[UG]-[0-9a-f]{12}\b")    # the shape of branch_accounting.unit_id / group_id
SNAPSHOT_KEYS = ("description", "acceptance_criteria", "comments")


class Refusal(Exception):
    def __init__(self, lines):
        super().__init__("\n".join(lines))
        self.lines = lines


def latin(text):
    out = []
    for ch in text:
        low = ch.lower()
        if low in LATIN:
            word = LATIN[low]
            out.append(word.upper() if ch != low else word)
        else:
            out.append(ch)
    return "".join(out)


def path_regex(path):
    """A regex for an absolute path in either slash form (a JSON-escaped backslash pair included)."""
    parts = list(Path(path).parts)
    drive = Path(path).drive
    head = re.escape(drive) + r"[\\/]+" if drive else "/"
    return re.compile(head + r"[\\/]+".join(re.escape(p) for p in parts[1:]), re.I)


DERIVED_IDS = ("person", "mail", "project-key", "handle")    # the counters of the classes built from the source (README lines)
SEP = r"[\s._-]*"    # between the characters of a person value: its spellings differ only by these
MAIL = re.compile(r"(?<![A-Za-z0-9._%+-])([A-Za-z0-9._%+-]+)@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}")
HOME_USER = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+([^\\/\"\s]+)|(?<![\w.>-])/(?:home|Users)/([^\\/\"\s]+)", re.I)
PERSON_MARK = re.compile(r"person-[0-9]+\Z")
YAML_PERSON = re.compile(r"^\s*(?:-\s+)?(\w+)\s*:\s*(.+?)\s*$")


def norm(value):
    return re.sub(r"[\s._-]+", "", value.lower())


def load_derived(path=None):
    """The classes of the scrub that are built from the SOURCE (person fields, mail, logins, project keys): their field names and
    marks live in the rules file, the values never do."""
    path = Path(path or RULES_PATH)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))["derived"]
        for key in ("person_keys", "user_marker_keys", "user_value_keys", "project_object_keys", "non_person_values",
                    "min_length", "person_mark", "mail_mark", "project_mark", "handle_url", "residue_detectors"):
            data[key]
        for d in data["residue_detectors"]:
            re.compile(d["pattern"], re.I), re.compile(d["ok"]), d["id"]
        return data
    except (OSError, ValueError, KeyError, TypeError, re.error) as exc:
        raise Refusal(["refused: the `derived` section of %s is absent or unreadable (%s: %s); person, mail, login and project-key "
                       "classes cannot be scrubbed without it (FR-59). Door: restore tools/story-scrub-rules.json."
                       % (path.name, type(exc).__name__, exc)])


class Registry:
    """The values of the person-ish classes found in ONE source root, and the marks they get: `person-<n>` (a stable number per
    distinct value, the spellings of one value share it), `person-<n>@example.invalid` for a mail address, one bare mark for a project
    key. A class of value: person (a person field, a display name), mail (a mail local part), login (a user object's login, a home
    folder's user), project (a tracker project key seen as the prefix of a rewritten ticket key, or the key/name of a project object)."""

    def __init__(self, derived, ticket=None, keep=(), base=0, rows=()):
        self.cfg, self.ticket, self.keep = derived, ticket, set(keep)
        self.people, self.projects = {}, {}    # norm key -> {"n", "cls", "form"}; lower key -> {"cls": "project", "form"}
        self.handles = {}    # norm key of a repository handle that is no collected person -> its number (one counter with `people`)
        self.last = base    # the last number given; a `rescrub` starts above the marks already in the story
        self.handle = re.compile(derived["handle_url"]["pattern"], re.I)
        self.rows = list(rows)    # [(id, pattern, exclude)]: the rewrite rows flagged `residue` in the rules file, scanned like a class
        self.detectors = [(d["id"], re.compile(d["pattern"], re.I), re.compile(d["ok"])) for d in derived["residue_detectors"]]    # (class id, pattern with a `seg` group, full-match of the allowed segment)
        self._patterns = None
        for key in derived.get("known_project_keys", []):    # the internal keys the critic named: bare in a run that never wrote them with a number
            self.add_project(key)

    # -- collecting ------------------------------------------------------------------------------------------------------------
    def take(self):
        self.last += 1
        return self.last

    def usable(self, value):
        value = value.strip()
        if len(value) < self.cfg["min_length"] or value in self.keep or value.lower() in self.cfg["non_person_values"]:
            return None
        return None if value.startswith(("<", "person-")) or "@" in value else value

    def add(self, value, cls):
        value = self.usable(latin(value)) if isinstance(value, str) else None
        if value and norm(value) not in self.people:
            self.people[norm(value)] = {"n": self.take(), "cls": cls, "form": value}

    def add_project(self, value):
        value = self.usable(latin(value)) if isinstance(value, str) else None
        if value and value.lower() not in self.projects:
            self.projects[value.lower()] = {"cls": "project", "form": value}

    def read_handles(self, text):
        for m in self.handle.finditer(latin(text)):
            key = norm(m.group("handle"))
            if key and not PERSON_MARK.match(m.group("handle")) and key not in self.people and key not in self.handles:
                self.handles[key] = self.take()

    def read_text(self, text):
        text = latin(text)
        self.read_handles(text)
        for m in MAIL.finditer(text):
            self.add(m.group(1), "mail")
        for m in HOME_USER.finditer(text):
            self.add(m.group(1) or m.group(2), "login")
        if self.ticket:
            pattern, exclude = self.ticket
            for m in pattern.finditer(text):
                if m.group(0) not in self.keep and not (exclude and exclude.fullmatch(m.group(0))):
                    self.add_project(m.group(0).rsplit("-", 1)[0])

    def read_data(self, node, parent_key=None, user=False):
        cfg = self.cfg
        if isinstance(node, str):
            self.read_text(node)
            if parent_key in cfg["person_keys"]:
                self.add(node, "person")
        elif isinstance(node, list):
            for item in node:
                self.read_data(item, parent_key, user)
        elif isinstance(node, dict):
            user = user or any(k in node for k in cfg["user_marker_keys"])    # a user object: given by its parent key or by its markers
            if parent_key == "project":
                for key in cfg["project_object_keys"]:
                    self.add_project(node.get(key))
            for key, value in node.items():
                if user and key in cfg["user_value_keys"]:
                    self.add(value, "login" if key in ("key", "login", "name") else "person")
                self.read_data(value, key, key in cfg["person_keys"])

    def read_yaml(self, text):
        for line in text.split("\n"):
            m = YAML_PERSON.match(line)
            if m and m.group(1) in self.cfg["person_keys"]:
                self.add(m.group(2).strip("'\""), "person")

    def read_file(self, rel, body):
        body = body.lstrip("﻿")
        try:
            if rel.endswith(".jsonl"):
                for row in (json.loads(x) for x in body.split("\n") if x.strip()):
                    self.read_data(row)
                return
            if rel.endswith(".json"):
                self.read_data(json.loads(body))
                return
        except ValueError:
            pass
        self.read_text(body)
        if rel.endswith((".yaml", ".yml")):
            self.read_yaml(body)

    # -- rewriting -------------------------------------------------------------------------------------------------------------
    def regex(self, key):
        return re.compile(r"(?<![A-Za-z0-9])" + SEP.join(re.escape(c) for c in key) + r"(?![A-Za-z0-9])", re.I)

    def patterns(self):
        if self._patterns is None:
            order = sorted(self.people, key=lambda k: (-len(k), k))
            self._patterns = ([(k, self.regex(k)) for k in order],
                              re.compile(r"(?<![A-Za-z0-9])(?:%s)(?![A-Za-z0-9])" % "|".join(
                                  re.escape(k) for k in sorted(self.projects, key=lambda k: (-len(k), k))), re.I)
                              if self.projects else None)
        return self._patterns

    def rewrite_handles(self, value, cleaner):
        """`github.com/<handle>` -> `github.com/person-<n>`: the number of a collected person with that handle, else the handle's own
        number (one handle, one number); the repository name after the handle stays. No judgment: an organisation is a handle too."""
        def one(m):
            handle = m.group("handle")
            if PERSON_MARK.match(handle):
                return m.group(0)
            key = norm(handle)
            n = self.people[key]["n"] if key in self.people else self.handles.setdefault(key, self.take())
            cleaner.numbers.setdefault("handle", {}).setdefault(key, n)
            cleaner.counts["handle"] = cleaner.counts.get("handle", 0) + 1
            return (m.group(0)[:m.start("handle") - m.start(0)] + self.cfg["person_mark"].replace("<n>", str(n))
                    + m.group(0)[m.end("handle") - m.start(0):])
        return self.handle.sub(one, value)

    def rewrite(self, value, cleaner):
        value = self.rewrite_handles(value, cleaner)
        people, projects = self.patterns()
        cfg = self.cfg

        def mark(cls, key, template):
            numbers = cleaner.numbers.setdefault(cls, {})
            numbers.setdefault(key, self.people[key]["n"])
            cleaner.counts[cls] = cleaner.counts.get(cls, 0) + 1
            return template.replace("<n>", str(self.people[key]["n"]))

        def mail(m):
            key = norm(m.group(1))
            return mark("mail", key, cfg["mail_mark"]) if key in self.people else m.group(0)

        value = MAIL.sub(mail, value)
        for key, pattern in people:
            value = pattern.sub(lambda m, key=key: mark("person", key, cfg["person_mark"]), value)
        if projects:
            def project(m):
                cleaner.numbers.setdefault("project-key", {}).setdefault(m.group(0).lower(), len(cleaner.numbers["project-key"]) + 1)
                cleaner.counts["project-key"] = cleaner.counts.get("project-key", 0) + 1
                return cfg["project_mark"]
            value = projects.sub(project, value)
        return value

    # -- the residue scan ------------------------------------------------------------------------------------------------------
    def residue(self, rel, text):
        """[(rel, line, class)] of every collected value left in a RESULT file name or text (case-insensitive, any separator spelling).
        Never the value itself."""
        hits = []
        people, _ = self.patterns()
        searches = [(self.people[k]["cls"], p) for k, p in people]
        searches += [("project", self.regex(k)) for k in sorted(self.projects)]
        for where in (rel, text):    # a handle left in a repository URL, and what a flagged rewrite row would still rewrite

            def line_of(m, where=where):
                return 0 if where is rel else where.count("\n", 0, m.start()) + 1
            rule = []
            for m in self.handle.finditer(where):
                if not PERSON_MARK.match(m.group("handle")):
                    rule.append((line_of(m), "residue-handle"))
            for rid, pattern, exclude in self.rows:
                for m in pattern.finditer(where):
                    if not (exclude and exclude.fullmatch(m.group(0))):
                        rule.append((line_of(m), "residue-" + rid))
            # the INDEPENDENT detectors (a broader reading than the rewrite patterns, so a form the rewrite misses is still found):
            # a hit they add on top of what the rewrite patterns already counted for the same line and class is reported too
            seen = {}
            for key in rule:
                seen[key] = seen.get(key, 0) + 1
            extra = []
            for did, pattern, ok in self.detectors:
                for m in pattern.finditer(where):
                    if not ok.fullmatch(m.group("seg")):
                        extra.append((line_of(m), "residue-" + did))
            for key in extra:
                if seen.get(key):
                    seen[key] -= 1
                else:
                    rule.append(key)
            hits += [(rel,) + key for key in rule]
        for cls, pattern in searches:
            for m in pattern.finditer(rel):
                hits.append((rel, 0, "residue-" + cls))
            for m in pattern.finditer(text):
                hits.append((rel, text.count("\n", 0, m.start()) + 1, "residue-" + cls))
        return hits


def collect(source, derived, rewrites=(), drop=(), keep=(), rows=()):
    """The Registry of a source root: every person field, mail, login, home user and ticket project key of the files the capture keeps
    (files it drops never reach the result, so their values are not searched for)."""
    ticket = next(((p, ex) for rid, p, _r, ex in rewrites if rid == "ticket-key"), None)
    registry = Registry(derived, ticket, keep, rows=rows)
    source = Path(source)
    for path in sorted(p for p in source.rglob("*") if p.is_file()):
        rel = path.relative_to(source).as_posix()
        if dropped(rel, drop):
            continue
        try:
            registry.read_text(rel)
            registry.read_file(rel, path.read_bytes().decode("utf-8"))
        except UnicodeDecodeError:
            continue
    return registry


class Cleaner:
    def __init__(self, source, rewrites=(), keep=(), registry=None):
        self.registry = registry
        self.keep = set(keep)    # the story's own task key: never rewritten (the capture refuses a non-synthetic one earlier)
        source = Path(source).resolve()
        top = source.parents[2] if len(source.parents) > 2 and source.parent.name == "artifacts" else source
        self.prefixes = [path_regex(top)] + ([path_regex(source)] if top != source else [])
        self.rewrites = list(rewrites)
        self.counts, self.numbers, self.foreign = {}, {}, {}
        self.only = None    # a set of rewrite-row ids: `rescrub` applies only these rows and the repository handles

    def foreign_root(self, m):
        key = re.sub(r"[\\/]+", "/", m.group(0)).lower()
        key = re.sub(r"^/([a-z])/", r"\1:/", key)
        return "<path-%d>" % self.foreign.setdefault(key, len(self.foreign) + 1)

    def rewrite(self, rid, replacement, m):
        """`<n>` is the number of the matched text; a row whose pattern has a `tail` group keeps that tail text (`<tail>`) and numbers
        the match WITHOUT it, so one host is one number whatever the keys behind it (the ticket-key row then rewrites the key in the tail)."""
        numbers = self.numbers.setdefault(rid, {})
        tail = m.groupdict().get("tail")
        basis = m.group(0)[:m.start("tail") - m.start(0)] if tail else m.group(0)
        n = numbers.setdefault(basis.lower(), len(numbers) + 1)
        self.counts[rid] = self.counts.get(rid, 0) + 1
        return replacement.replace("<n>", str(n)).replace("<tail>", tail or "")

    def narrow(self, value):
        for rid, pattern, replacement, exclude in self.rewrites:
            if rid in self.only:
                value = pattern.sub(lambda m, rid=rid, replacement=replacement, exclude=exclude:
                                    m.group(0) if exclude and exclude.fullmatch(m.group(0)) else self.rewrite(rid, replacement, m), value)
        return self.registry.rewrite_handles(value, self)

    def text(self, value):
        if self.only is not None:
            return self.narrow(value)
        value = latin(value)
        for prefix in self.prefixes:    # the source root first: a path that is also a home path becomes <stand>
            value = prefix.sub("<stand>", value)
        value = HOME.sub("<home>", STAND.sub("<stand>", value))
        value = FOREIGN.sub(self.foreign_root, value)
        for rid, pattern, replacement, exclude in self.rewrites:
            value = pattern.sub(lambda m, rid=rid, replacement=replacement, exclude=exclude:
                                m.group(0) if m.group(0) in self.keep or (exclude and exclude.fullmatch(m.group(0)))
                                else self.rewrite(rid, replacement, m), value)
        return self.registry.rewrite(value, self) if self.registry else value    # after the ticket keys: a project key alone is what is left

    def json_text(self, original):
        """The cleaned text of a JSON / JSONL file by walking its strings (escaping stays valid); None when it does not parse."""
        body = original.lstrip("﻿")
        try:
            if body.strip() and "\n" in body.strip() and not _is_indented(body):
                rows = [json.loads(x) for x in body.split("\n") if x.strip()]
                cleaned = [self.walk(r) for r in rows]
                if cleaned == rows:
                    return original
                return "\n".join(json.dumps(r, ensure_ascii=False) for r in cleaned) + "\n"
            data = json.loads(body)
        except ValueError:
            return None
        cleaned = self.walk(data)
        if cleaned == data:
            return original
        indent = _is_indented(body)
        return json.dumps(cleaned, ensure_ascii=False, indent=indent or None) + ("\n" if body.endswith("\n") else "")

    def walk(self, value):
        if isinstance(value, str):
            return self.text(value)
        if isinstance(value, list):
            return [self.walk(v) for v in value]
        if isinstance(value, dict):
            return {self.walk(k): self.walk(v) for k, v in value.items()}
        return value


def _is_indented(body):
    m = re.match(r"\s*[\[{]\n( +)", body)
    return len(m.group(1)) if m else 0


def load_rewrites(path=None):
    path = Path(path or RULES_PATH)
    try:
        rows = json.loads(path.read_text(encoding="utf-8")).get("rewrites", [])
        return [(r["id"], re.compile(r["pattern"], re.I if r.get("ignore_case") else 0), r["replacement"],
                 re.compile(r["exclude"]) if r.get("exclude") else None) for r in rows]
    except (OSError, ValueError, KeyError, re.error) as exc:
        raise Refusal(["refused: the rewrite rows of %s are unreadable (%s: %s). Door: restore tools/story-scrub-rules.json."
                       % (path.name, type(exc).__name__, exc)])


def load_residue_rows(path=None):
    """[(id, pattern, exclude)] of the rewrite rows flagged `"residue": true`: the scan looks for what such a row would still rewrite."""
    path = Path(path or RULES_PATH)
    try:
        rows = json.loads(path.read_text(encoding="utf-8")).get("rewrites", [])
        return [(r["id"], re.compile(r["pattern"], re.I if r.get("ignore_case") else 0),
                 re.compile(r["exclude"]) if r.get("exclude") else None) for r in rows if r.get("residue")]
    except (OSError, ValueError, KeyError, re.error) as exc:
        raise Refusal(["refused: the rewrite rows of %s are unreadable (%s: %s). Door: restore tools/story-scrub-rules.json."
                       % (path.name, type(exc).__name__, exc)])


def load_rules(path=None):
    path = Path(path or RULES_PATH)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return [(r["id"], re.compile(r["pattern"], re.I if r.get("ignore_case") else 0),
                 re.compile(r["exclude"]) if r.get("exclude") else None) for r in data["rules"]]
    except (OSError, ValueError, KeyError, re.error) as exc:
        raise Refusal(["refused: the scrub rules file %s is absent or unreadable (%s: %s); a capture never passes without it "
                       "(FR-59). Door: restore tools/story-scrub-rules.json." % (path.name, type(exc).__name__, exc)])


def scan(rel, text, rules):
    """Hits over the RESULT text only (after transliteration, path replacement and rewrites)."""
    hits = []
    for number, line in enumerate(text.split("\n"), 1):
        for rule_id, pattern, exclude in rules:
            for m in pattern.finditer(line):
                if not (exclude and exclude.fullmatch(m.group(0))):
                    hits.append((rel, number, rule_id, m.group(0)[:40]))
        if CYRILLIC.search(line):
            hits.append((rel, number, "cyrillic", "a Cyrillic letter that has no Latin twin"))
        if DRIVE_PATH.search(line):
            hits.append((rel, number, "abs-path", DRIVE_PATH.search(line).group(0)))
    return hits


def valid_json(rel, text):
    """True when a .json file parses whole (a .jsonl file: line by line); other files are not judged (True)."""
    body = text.lstrip("﻿")
    try:
        if rel.endswith(".json"):
            json.loads(body)
        elif rel.endswith(".jsonl"):
            for line in body.split("\n"):
                if line.strip():
                    json.loads(line)
    except ValueError:
        return False
    return True


def read_events(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_chain(events, target, content_hash):
    previous, lines = "", []
    for event in events:
        event = dict(event)
        event.pop("event_hash", None)
        event["previous_hash"] = previous
        previous = event["event_hash"] = content_hash(event)
        lines.append(json.dumps(event, ensure_ascii=False))
    (target / "state" / "events.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def rebind_gate_a(target, content_hash):
    """Put the bindings of the current approved gate A decision back to what the controller computes over these files."""
    events = read_events(target / "state" / "events.jsonl")
    gate_a = [e for e in events if e.get("type") == "decision" and (e.get("payload") or {}).get("gate") == "A"
              and e["payload"].get("status") == "approved"]
    if not gate_a or not (target / "work" / "test-plan.json").is_file():
        return False
    from controller import Controller
    try:
        bindings = Controller(target).gate_inputs()
    except Exception as exc:    # the package's own function refused: say so, never pass
        raise Refusal(["refused: state/events.jsonl: gate A bindings cannot be recomputed (%s: %s). Door: --cut-after-seq "
                       "before the gate A decision, or --drop the files the plan reads is not possible; fix the source "
                       "outside the repository." % (type(exc).__name__, exc)])
    for key in ("plan_content_hash", "plan_semantic_hash", "oracle_content_hashes", "coverage_contract_revisions",
                "lifecycle_actions_hash", "source_inventory_hash"):
        if key in bindings:
            gate_a[-1]["payload"][key] = bindings[key]
    write_chain(events, target, content_hash)
    return True


def package_scripts(package):
    scripts = str(Path(package) / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import event_store
    return event_store.content_hash


def recorded_version(root):
    """The package version the RUN was made under, never the current package's: `pipeline.json` `run_mode.plugin_version` (the
    stamp `story_step start` writes), else "unknown"."""
    try:
        value = json.loads((Path(root) / "pipeline.json").read_text(encoding="utf-8-sig")).get("run_mode", {}).get("plugin_version")
    except (OSError, ValueError, AttributeError):
        return "unknown"
    return value.strip() if isinstance(value, str) and value.strip() else "unknown"


def dropped(rel, globs):
    return any(fnmatch.fnmatch(rel, g) or fnmatch.fnmatch(rel.rsplit("/", 1)[-1], g) for g in globs)


def load_accounting(package):
    """The package's own `branch_accounting` (the one function that derives U- and G- ids from text), imported by path (AR-13)."""
    path = Path(package) / "scripts" / "branch_accounting.py"
    if not path.is_file():
        raise Refusal(["refused: the package has no scripts/branch_accounting.py, and a ticket snapshot the scrub changed needs its "
                       "unit_id / group_id to follow the text-derived ids. Door: pass --package with scripts/branch_accounting.py."])
    spec = importlib.util.spec_from_file_location("story_capture_branch_accounting", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot_shaped(data):
    return isinstance(data, dict) and all(k in data for k in SNAPSHOT_KEYS)


def text_id_map(pairs, accounting):
    """{old id: new id} of every U- / G- id the package derives from a snapshot text the scrub changed. `pairs` = (file, source
    snapshot, scrubbed snapshot): the units of both come from `snapshot_units`, are paired by position, and the ids of both sides are
    computed by the package's own functions. A count or field that differs, two old ids met on one new id (or one old on two), is a
    refusal naming the lines: never a silent merge."""
    remap, owner = {}, {}

    def put(old, new, line):
        if new in owner and owner[new][0] != old:
            raise Refusal(["refused: two different ids of the recorded run became one after the rewrites: %s (%s) and %s (%s) are both %s. "
                           "Door: --drop the snapshot, or fix the source outside the repository." % (owner[new][0], owner[new][1], old, line, new)])
        if old in remap and remap[old] != new:
            raise Refusal(["refused: one id of the recorded run, %s (%s), became two after the rewrites: %s and %s. Door: --drop the snapshot."
                           % (old, line, remap[old], new)])
        owner[new] = (old, line)
        remap[old] = new

    for rel, source, scrubbed in pairs:
        title = rel.rsplit("/", 1)[-1] == "ticket-snapshot.json"
        a, b = accounting.snapshot_units(source, title_counts=title), accounting.snapshot_units(scrubbed, title_counts=title)
        if a["state"] != b["state"] or len(a["units"]) != len(b["units"]) or [u[0] for u in a["units"]] != [u[0] for u in b["units"]]:
            raise Refusal(["refused: %s: the scrub changed the units of the snapshot (%s: %d units, then %s: %d units); the ids derived "
                           "from its text cannot be paired. Door: --drop the snapshot, or fix the source outside the repository."
                           % (rel, a["state"], len(a["units"]), b["state"], len(b["units"]))])
        for n, (old, new) in enumerate(zip(a["units"], b["units"]), 1):
            put(accounting.unit_id(old[1]), accounting.unit_id(new[1]), "%s: %s unit %d" % (rel, old[0], n))
            if old[2] and new[2]:
                put(old[2], new[2], "%s: %s unit %d, its comment group" % (rel, old[0], n))
    return {old: new for old, new in remap.items() if old != new}


def follow_hash(hash_map, before, after):
    """A file changed from `before` to `after` (sha256): every recorded hash that pointed at `before` points at `after`."""
    for key, value in list(hash_map.items()):
        if value == before:
            hash_map[key] = after
    hash_map.setdefault(before, after)


def rekey_ids(partial, remap, hash_map):
    """Replace every old id of `remap` by its new one in every captured text file; {kind: [replacements, distinct ids]}."""
    stats = {"U": [0, set()], "G": [0, set()]}

    def swap(m):
        new = remap.get(m.group(0))
        if new is None:
            return m.group(0)    # an id-like token the package function does not produce from a captured text: untouched
        stats[new[0]][0] += 1
        stats[new[0]][1].add(m.group(0))
        return new

    for path in sorted(p for p in partial.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES):
        raw = path.read_bytes()
        body = raw.decode("utf-8")
        text = ID_TOKEN.sub(swap, body)
        if text != body:
            path.write_text(text, encoding="utf-8", newline="\n")
            follow_hash(hash_map, hashlib.sha256(raw).hexdigest(), hashlib.sha256(path.read_bytes()).hexdigest())
    return {kind: [n, len(ids)] for kind, (n, ids) in stats.items()}


def follow_all(partial, snapshots, snapshot_changed, hash_map, package, content_hash):
    """After the rewrites, in this order: the text-derived ids are re-keyed, the recorded sha256 values follow the new bytes to a
    fixpoint, the events are re-chained, gate A is re-bound. Returns (id_stats, sha256 replacements, gate A rebound)."""
    # ids the package derives from a text follow the rewrites. This runs BEFORE the sha256 follow: the re-keyed files are new bytes
    # whose own hashes the follow below then carries to every file that records them.
    id_stats, hash_fixed = {"U": [0, 0], "G": [0, 0]}, 0
    if snapshot_changed:
        remap = text_id_map(snapshots, load_accounting(package))
        if remap:
            id_stats = rekey_ids(partial, remap, hash_map)
    # a file a door compares by its recorded sha256 changed: the record follows the new bytes. A file that changes BECAUSE a hash
    # inside it was remapped has a new hash of its own, so the pass repeats to a fixpoint (bound: FOLLOW_PASSES).
    for number in range(1, FOLLOW_PASSES + 2):
        if not hash_map:
            break
        pattern, moved = re.compile("|".join(hash_map)), []
        for path in sorted(p for p in partial.rglob("*") if p.is_file()):
            body = path.read_bytes().decode("utf-8", "replace") if path.suffix in (".json", ".jsonl", ".md", ".txt", ".yaml", ".yml") else ""
            if body and pattern.search(body):
                before = hashlib.sha256(path.read_bytes()).hexdigest()
                body, n = pattern.subn(lambda m: hash_map[m.group(0)], body)
                hash_fixed += n
                path.write_text(body, encoding="utf-8", newline="\n")
                after = hashlib.sha256(path.read_bytes()).hexdigest()
                if after != before:
                    for key, value in list(hash_map.items()):
                        if value == before:
                            hash_map[key] = after
                    hash_map.setdefault(before, after)
                    moved.append(path.relative_to(partial).as_posix())
        if not moved:
            break
        if number > FOLLOW_PASSES:
            raise Refusal(["refused: the sha256 follow did not converge in %d passes; still changing: %s. Door: --drop <glob> for "
                           "the files that embed each other's hashes." % (FOLLOW_PASSES, ", ".join(moved[:10]))])
    write_chain([json.loads(x) for x in (partial / "state" / "events.jsonl").read_text(encoding="utf-8").splitlines()], partial, content_hash)
    return id_stats, hash_fixed, rebind_gate_a(partial, content_hash)


def capture(source, story_id, cut=None, drop=(), package=None, rules_path=None, report=None):
    package = Path(package or DEFAULT_PACKAGE)
    rules = load_rules(rules_path)
    rewrites = load_rewrites(rules_path)
    source = Path(source)
    jira = next(p for i, p, _ in rules if i == "jira-tp3")
    events_file = source / "state" / "events.jsonl"
    if not events_file.is_file():
        raise Refusal(["refused: %s has no state/events.jsonl: not a task root. Door: pass the task root." % source.name])
    if not ID_OK.match(story_id):
        raise Refusal(["refused: the story id %r is not a plain name (letters, digits, . _ -)" % story_id])
    events = read_events(events_file)
    task = str((events[0] if events else {}).get("task_id") or source.name)
    for key in (story_id, source.name, task):
        if jira.search(key):
            raise Refusal(["refused: not synthetic: internal ticket key (%s). A corpus of internal tickets is not a story; "
                           "no door." % key])
    target = package.joinpath(*STORIES, story_id)
    if target.exists():
        raise Refusal(["refused: the target %s exists. Door: a new --id." % "/".join(STORIES + (story_id,))])
    content_hash = package_scripts(package)
    if not ID_OK.match(task):
        raise Refusal(["refused: the task id %r is not a plain name (letters, digits, . _ -)" % task])
    # gate A is re-bound by the package's Controller, which requires the root folder to be named after the task id:
    # the work happens in a temp folder with that last component and moves into the target only on success
    registry = collect(source, load_derived(rules_path), rewrites, drop, keep=(task, story_id), rows=load_residue_rows(rules_path))    # from the SOURCE, before anything is written
    scratch = Path(tempfile.mkdtemp(prefix="story-capture-"))
    partial = scratch / task
    cleaner, changed, skipped, hits, sizes = Cleaner(source, rewrites, keep=(task, story_id), registry=registry), [], [], [], {}
    hash_map, hash_fixed, snapshots, snapshot_changed, written = {}, 0, [], False, set()
    version = recorded_version(source)    # read from the SOURCE, before any drop: dropping pipeline.json must not give "unknown"
    try:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            rel = path.relative_to(source).as_posix()
            new_rel = cleaner.text(rel)    # a file name is scrubbed like a text: the lists below name the NEW names only
            if dropped(rel, drop):
                skipped.append(new_rel)
                continue
            if new_rel in written:
                raise Refusal(["refused: two files of the run became one name after the rewrites: %s. Door: --drop one of them." % new_rel])
            written.add(new_rel)
            raw = path.read_bytes()
            out = partial.joinpath(*new_rel.split("/"))
            out.parent.mkdir(parents=True, exist_ok=True)
            try:
                original = raw.decode("utf-8")
            except UnicodeDecodeError:
                hits.append((new_rel, 0, "binary", "not text; scrub cannot judge it"))
                continue
            if rel == "state/events.jsonl":
                kept = [e for e in events if cut is None or int(e.get("sequence", 0)) <= cut]
                text = "\n".join(json.dumps(cleaner.walk(e), ensure_ascii=False) for e in kept) + "\n"
            else:
                text = cleaner.json_text(original) if rel.endswith((".json", ".jsonl")) else None
                if text is None:
                    text = cleaner.text(original)
            text = text.replace("\r\n", "\n")
            if text != original.replace("\r\n", "\n") or new_rel != rel:
                changed.append(new_rel)
            if valid_json(rel, original.replace("\r\n", "\n")) and not valid_json(rel, text):
                hits.append((new_rel, 0, "json-broken", "a replacement made the file invalid JSON"))
            out.write_text(text, encoding="utf-8", newline="\n")
            if rel.endswith(".json"):    # a ticket snapshot: its source and scrubbed units give the text-derived ids their new keys
                try:
                    before_data, after_data = json.loads(original.lstrip("﻿")), json.loads(text.lstrip("﻿"))
                except ValueError:
                    before_data = after_data = None
                if snapshot_shaped(before_data) and snapshot_shaped(after_data):
                    snapshots.append((new_rel, before_data, after_data))
                    snapshot_changed = snapshot_changed or before_data != after_data
            if rel != "state/events.jsonl" and out.read_bytes() != raw:
                hash_map[hashlib.sha256(raw).hexdigest()] = hashlib.sha256(out.read_bytes()).hexdigest()
            hits += scan(new_rel, text, rules)
        if not (partial / "state" / "events.jsonl").is_file():
            raise Refusal(["refused: state/events.jsonl was dropped; a story needs its events."])
        id_stats, hash_fixed, rebound = follow_all(partial, snapshots, snapshot_changed, hash_map, package, content_hash)
        for path in partial.rglob("*"):    # the cap counts the captured run files only, never the tool's own three
            rel = path.relative_to(partial).as_posix()
            if path.is_file() and rel not in OWN_FILES:
                sizes[rel] = path.stat().st_size
        # the residue scan runs on the RESULT as it will ship, after every rewrite, re-key and hash follow
        for path in sorted(p for p in partial.rglob("*") if p.is_file()):
            hits += [h + ("a value collected from the source (never printed)",)
                     for h in registry.residue(path.relative_to(partial).as_posix(), path.read_bytes().decode("utf-8", "replace"))]
        if hits:
            hits = sorted(set(hits), key=lambda h: (h[0], h[1], h[2]))
            lines = ["refused: %s:%s: rule %s: %s" % h for h in hits[:50]] + (["... +%d more" % (len(hits) - 50)] if len(hits) > 50 else [])
            raise Refusal(lines + ["Door: --drop <glob> for a file the walked stages do not need, or fix the source outside "
                                   "the repository."])
        if sum(sizes.values()) > LIMIT_BYTES:
            big = sorted(sizes.items(), key=lambda kv: -kv[1])[:5]
            raise Refusal(["refused: the captured run files are %d bytes, over the %d limit (README.txt, story.json, expected.json are not counted). Largest files:" % (sum(sizes.values()), LIMIT_BYTES)]
                          + ["  %s  %d" % kv for kv in big] + ["Door: --drop <glob> (the dropped files are listed in README.txt)."])
        story = {"id": story_id, "task": task, "synthetic": True, "package_version": version, "cut_after_seq": cut,
                 "walk": [], "not_walked": [], "dropped": skipped}
        story_body = json.dumps(story, indent=1) + "\n"
        readme = (
            "Story %s: a scrubbed slice of a real run of the synthetic task %s.\n"
            "Source: the task root folder %s (path not kept). Cut: %s.\n"
            "Changed (%d files, listed): Cyrillic turned into Latin, absolute paths replaced by placeholders, rewrites applied,\n"
            "events re-chained through event_store.content_hash%s (every hash a stage door compares is recomputed AFTER all rewrites).\n"
            "Placeholders: <stand> = the source's own root; <home> = a home folder; <path-N> = any other absolute root\n"
            "(drive plus up to three folders), numbered by first appearance, %d of them, one number per root in any slash/case\n"
            "spelling; the originals are not kept. Relative tails are intact.\n"
            "Recorded sha256 values of changed files followed the new bytes: %d replacements.\n"
            "Text-derived ids re-keyed to the scrubbed text (branch_accounting unit_id / group_id, snapshot units paired by position),\n"
            "ids and replacements: U- %d ids %d replacements, G- %d ids %d replacements.\n"
            "Rewrites (numbered by first appearance; the originals are not kept):\n%s\n%s\n"
            "Dropped (%d files, listed):\n%s\n"
            % (story_id, task, source.name, "events up to sequence %d" % cut if cut is not None else "none",
               len(changed), ", gate A bindings recomputed by Controller.gate_inputs" if rebound else "", len(cleaner.foreign), hash_fixed,
               id_stats["U"][1], id_stats["U"][0], id_stats["G"][1], id_stats["G"][0],
               "\n".join("  changed: %s x %d (%d distinct)" % (rid, cleaner.counts.get(rid, 0), len(cleaner.numbers.get(rid, {})))
                         for rid in [r[0] for r in rewrites] + list(DERIVED_IDS)),
               "\n".join("  changed: " + c for c in changed), len(skipped), "\n".join("  dropped: " + s for s in skipped)))
        late = [(name, line, cls, "a value collected from the source (never printed)")
                for name, body in (("story.json", story_body), ("README.txt", readme)) for _n, line, cls in registry.residue(name, body)]
        if late:    # the tool's own two files name file paths: the same scan covers them
            raise Refusal(["refused: %s:%s: rule %s: %s" % h for h in late[:50]]
                          + ["Door: --drop <glob> for the file whose name carries it."])
        (partial / "story.json").write_text(story_body, encoding="utf-8", newline="\n")
        (partial / "README.txt").write_text(readme, encoding="utf-8", newline="\n")
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(str(partial), str(target))
        except BaseException:
            shutil.rmtree(target, ignore_errors=True)
            raise
        if report is not None:
            report.update(size=sum(sizes.values()), rewrites=dict(cleaner.counts),
                          dropped=list(skipped), paths=len(cleaner.foreign), ids=id_stats)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return target


def rescrub(story_id, package=None, rules_path=None, report=None):
    """Apply the repository-handle class and every `residue` rewrite row to a story ALREADY captured, in place (the source run is not
    needed): the same Cleaner and Registry functions, then the same id re-key, sha256 follow, re-chain and gate A re-bind as a capture.
    Numbers start above the `person-<n>` marks the story already carries. Every file is written only when its bytes change; any
    refusal leaves the story as it was. Hand-written content of story.json / expected.json changes only where a rewrite changes it."""
    package = Path(package or DEFAULT_PACKAGE)
    root = package.joinpath(*STORIES, story_id)
    if not (root / "story.json").is_file():
        raise Refusal(["refused: no story %s under %s. Door: capture it first." % (story_id, "/".join(STORIES))])
    task = str(json.loads((root / "story.json").read_text(encoding="utf-8")).get("task") or story_id)
    if not ID_OK.match(task):
        raise Refusal(["refused: the task id %r is not a plain name (letters, digits, . _ -)" % task])
    rewrites, rows, content_hash = load_rewrites(rules_path), load_residue_rows(rules_path), package_scripts(package)
    scratch = Path(tempfile.mkdtemp(prefix="story-rescrub-"))
    partial = scratch / task    # the Controller wants the root folder named after the task id
    try:
        shutil.copytree(root, partial)
        files = sorted(p for p in partial.rglob("*") if p.is_file())
        texts = {}
        for path in files:
            try:
                texts[path] = path.read_bytes().decode("utf-8")
            except UnicodeDecodeError:
                continue    # a binary file is never rewritten (a capture refuses one, so a story holds none; this keeps it byte-equal)
        base = max([int(n) for body in texts.values() for n in re.findall(r"person-([0-9]+)", body)] or [0])
        registry = Registry(load_derived(rules_path), base=base, rows=rows)
        for body in texts.values():
            registry.read_handles(body)
        cleaner = Cleaner(partial, rewrites, registry=registry)
        cleaner.only = {rid for rid, _p, _e in rows}
        changed, snapshots, snapshot_changed, hash_map = [], [], False, {}
        for path, original in texts.items():
            rel = path.relative_to(partial).as_posix()
            text = cleaner.json_text(original) if rel.endswith((".json", ".jsonl")) else None
            if text is None:
                text = cleaner.text(original)
            if text == original:
                continue
            if valid_json(rel, original) and not valid_json(rel, text):
                raise Refusal(["refused: %s:0: rule json-broken: a replacement made the file invalid JSON" % rel])
            changed.append(rel)
            path.write_text(text, encoding="utf-8", newline="\n")
            if rel.endswith(".json"):
                try:
                    before_data, after_data = json.loads(original.lstrip("﻿")), json.loads(text.lstrip("﻿"))
                except ValueError:
                    before_data = after_data = None
                if snapshot_shaped(before_data) and snapshot_shaped(after_data):
                    snapshots.append((rel, before_data, after_data))
                    snapshot_changed = snapshot_changed or before_data != after_data
            if rel != "state/events.jsonl":
                hash_map[hashlib.sha256(original.encode("utf-8")).hexdigest()] = hashlib.sha256(path.read_bytes()).hexdigest()
        id_stats, hash_fixed, rebound = follow_all(partial, snapshots, snapshot_changed, hash_map, package, content_hash)
        if changed:
            note = ("Rescrub (in place, TD-15): the repository-handle class and the rows flagged `residue` were applied to the files below;\n"
                    "ids and replacements: U- %d ids %d replacements, G- %d ids %d replacements; sha256 replacements: %d%s.\n%s\n"
                    % (id_stats["U"][1], id_stats["U"][0], id_stats["G"][1], id_stats["G"][0], hash_fixed,
                       "; gate A bindings recomputed" if rebound else "",
                       "\n".join("  changed: %s x %d (%d distinct)" % (rid, cleaner.counts.get(rid, 0), len(cleaner.numbers.get(rid, {})))
                                 for rid in sorted(cleaner.only) + ["handle"])
                       + "\n" + "\n".join("  changed: " + c for c in changed)))
            readme = partial / "README.txt"
            readme.write_text(readme.read_text(encoding="utf-8") + note, encoding="utf-8", newline="\n")
        sizes, hits = {}, []
        for path in sorted(p for p in partial.rglob("*") if p.is_file()):
            rel = path.relative_to(partial).as_posix()
            if rel not in OWN_FILES:
                sizes[rel] = path.stat().st_size
            if path in texts:    # a binary file was never judged
                hits += [h + ("a leftover of a rewrite row (never printed)",) for h in registry.residue(rel, path.read_bytes().decode("utf-8"))]
        if hits:
            hits = sorted(set(hits), key=lambda h: (h[0], h[1], h[2]))
            raise Refusal(["refused: %s:%s: rule %s: %s" % h for h in hits[:50]])
        if sum(sizes.values()) > LIMIT_BYTES:
            raise Refusal(["refused: the captured run files are %d bytes, over the %d limit (README.txt, story.json, expected.json are not counted)."
                           % (sum(sizes.values()), LIMIT_BYTES)])
        written = []
        for path in sorted(p for p in partial.rglob("*") if p.is_file()):
            rel = path.relative_to(partial).as_posix()
            target = root.joinpath(*rel.split("/"))
            if not target.is_file() or target.read_bytes() != path.read_bytes():
                target.write_bytes(path.read_bytes())
                written.append(rel)
        if report is not None:
            report.update(written=written, counts=dict(cleaner.counts), ids=id_stats, size=sum(sizes.values()))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return root


def load_walker(package):
    """The walker's module (scenario_walk.py), imported by path from the package: it owns the vocabulary `expected` writes in
    (gate decision tokens, question kinds, what a handoff form requires), so the two sides read one table, not two."""
    import importlib.util
    path = Path(package) / "scripts" / "tests" / "scenario_walk.py"
    if not path.is_file():
        raise Refusal(["refused: the walker %s is missing under --package. Door: pass the package that holds "
                       "scripts/tests/scenario_walk.py." % "/".join(("scripts", "tests", "scenario_walk.py"))])
    for folder in (str(path.parent), str(Path(package) / "scripts")):
        if folder not in sys.path:
            sys.path.insert(0, folder)
    spec = importlib.util.spec_from_file_location("scenario_walk", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["scenario_walk"] = module
    spec.loader.exec_module(module)
    return module


def expected(story_id, package=None):
    package = Path(package or DEFAULT_PACKAGE)
    root = package.joinpath(*STORIES, story_id)
    if not (root / "story.json").is_file():
        raise Refusal(["refused: no story %s under %s. Door: capture it first." % (story_id, "/".join(STORIES))])
    walker = load_walker(package)
    story = json.loads((root / "story.json").read_text(encoding="utf-8"))
    events = read_events(root / "state" / "events.jsonl")
    stage_of = {e["payload"]["id"]: e["payload"].get("stage") for e in events if e.get("type") == "dispatch"}
    stages, refusals, words = {}, [], sorted(p.name for p in (root / "state" / "words").glob("*")) if (root / "state" / "words").is_dir() else []
    for e in events:
        p, seq = e.get("payload") or {}, e.get("sequence")
        if e.get("type") == "stage_transition" and p.get("status") == "done" and p.get("stage") not in stages:
            stages[p["stage"]] = {"outcome": "accepted", "handed": [], "source": "events.jsonl seq %s stage_transition done" % seq}
        elif e.get("type") == "accept" and stage_of.get(p.get("id")):
            form = root / "work" / "handoffs" / ("%s.yaml" % p["id"])    # what the walker's `handed` facet compares with
            handed = walker.required_inputs(form.read_text(encoding="utf-8")) if form.is_file() else []
            stages[stage_of[p["id"]]] = {"outcome": "accepted", "handed": handed, "dispatch": p["id"],
                                         "source": "events.jsonl seq %s accept; handed: required inputs of work/handoffs/%s.yaml"
                                                   % (seq, p["id"])}
        elif e.get("type") == "decision" and p.get("gate") in ("A", "B"):
            gate = "gate" + p["gate"]
            mine = [w for w in words if gate.lower().replace("gate", "gate-") in w.lower() or gate.lower() in w.lower()]
            try:
                token = walker.decision_of(p.get("action"), p.get("status"))
            except KeyError:
                raise Refusal(["refused: events.jsonl seq %s: the decision action %r is no row of GATE_ACTIONS in the walker "
                               "(scripts/tests/scenario_walk.py). Door: add the row there; a guess is never written." % (seq, p.get("action"))])
            stages[gate] = {"decision": token, "recorded_action": p.get("action"), "status": p.get("status"), "words": mine,
                            "source": "events.jsonl seq %s decision%s" % (seq, "; " + ", ".join("state/words/" + w for w in mine) if mine else "")}
        elif e.get("type") == "checkpoint" and p.get("status") in ("incomplete", "blocked"):
            refusals.append({"stage": p.get("stage"), "seq": seq, "status": p["status"], "reason": str(p.get("reason", ""))[:200]})
    questions = root / "state" / "driver-questions.jsonl"
    if questions.is_file():
        for row in (json.loads(x) for x in questions.read_text(encoding="utf-8").splitlines() if x.strip()):
            kind = walker.question_kind_of(row.get("kind", ""))    # written exactly as the question door returns it
            if kind and "gate" + kind[-1].upper() in stages:
                entry = stages["gate" + kind[-1].upper()]
                entry["question_kind"] = kind
                if isinstance(row.get("options"), list) and row["options"]:    # the carrier records them: written; else NO key (the walker NOTEs it)
                    entry["options"] = sorted(str(o) for o in row["options"])
    summary = root / "work" / "delivery-summary.json"
    if summary.is_file():
        verdict = json.loads(summary.read_text(encoding="utf-8-sig")).get("delivery_verdict")
        if verdict:
            stages.setdefault("S8", {})["delivery"] = verdict
            stages["S8"]["source"] = "work/delivery-summary.json delivery_verdict"
    for item in refusals:
        if item["stage"] in stages:
            stages[item["stage"]].setdefault("refused", []).append(item)
    previous = root / "expected.json"    # a re-run keeps the accepted amendments (decisions of the Lead), rewrites the rest
    kept = []
    if previous.is_file():
        try:
            kept = list(json.loads(previous.read_text(encoding="utf-8-sig")).get("amendments") or [])
        except (ValueError, AttributeError, TypeError):
            kept = []
    out = {"stages": stages, "amendments": kept}
    loose = [r for r in refusals if r["stage"] not in stages]
    if loose:
        out["refusals"] = loose
    (root / "expected.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    walked = [{"stage": s, "facet": "accepted", "why": "no carrier: the run recorded no accept for %s" % s} for s in STAGES if s not in stages]
    for s, entry in stages.items():    # ONE row per (stage, facet, reason): a count and at most three sample paths
        trimmed = [path for path in story.get("dropped", []) if entry.get("dispatch") and entry["dispatch"] in path]
        if trimmed:
            walked.append({"stage": s, "facet": "digest", "why": "trimmed: files of this dispatch dropped by the capture",
                           "count": len(trimmed), "samples": trimmed[:3]})
    by_lead = [r for r in story.get("not_walked") or [] if isinstance(r, dict) and r.get("by") == "lead"]
    story["not_walked"] = walked + by_lead    # hand-written rows of the Lead survive a re-run
    (root / "story.json").write_text(json.dumps(story, indent=1) + "\n", encoding="utf-8", newline="\n")
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    cap = sub.add_parser("capture")
    cap.add_argument("--source", required=True)
    cap.add_argument("--id", required=True)
    cap.add_argument("--cut-after-seq", type=int)
    cap.add_argument("--drop", nargs="+", action="extend", default=[])
    exp = sub.add_parser("expected")
    exp.add_argument("--id", required=True)
    res = sub.add_parser("residue", help="count the values collected from a source that remain in a captured story (counts, never values)")
    res.add_argument("--source", required=True, nargs="+", action="extend", help="task roots whose values are searched (one or several)")
    res.add_argument("--id", required=True)
    res.add_argument("--drop", nargs="+", action="extend", default=[], help="the globs the capture dropped (default: collect from every file)")
    res.add_argument("--lines", action="store_true", help="also print file:line and class of every hit")
    rsc = sub.add_parser("rescrub", help="apply the repository-handle class and the `residue` rewrite rows to a story already captured, in place")
    rsc.add_argument("--id", required=True)
    for p in (cap, exp, res, rsc):
        p.add_argument("--package")
    args = parser.parse_args(argv)
    try:
        if args.cmd == "residue":
            root = Path(args.package or DEFAULT_PACKAGE).joinpath(*STORIES, args.id)
            registry = None
            for source in args.source:    # several sources: the values of all of them are searched in the one story
                found = collect(source, load_derived(), load_rewrites(), args.drop, keep=(args.id,), rows=load_residue_rows())
                if registry is None:
                    registry = found
                for key, value in found.people.items():
                    registry.people.setdefault(key, value)
                for key, value in found.projects.items():
                    registry.projects.setdefault(key, value)
            hits = [h for path in sorted(p for p in root.rglob("*") if p.is_file())
                    for h in registry.residue(path.relative_to(root).as_posix(), path.read_bytes().decode("utf-8", "replace"))]
            for cls in ("person", "mail", "login", "project", "handle") + tuple(r[0] for r in registry.rows):
                print("residue-%s: %d hits" % (cls, sum(1 for h in hits if h[2] == "residue-" + cls)))
            print("values collected: person %d, mail %d, login %d, project %d" % tuple(
                [sum(1 for v in registry.people.values() if v["cls"] == c) for c in ("person", "mail", "login")] + [len(registry.projects)]))
            if args.lines:
                print("\n".join("%s:%d %s" % h for h in hits))
            return 1 if hits else 0
        if args.cmd == "rescrub":
            info = {}
            rescrub(args.id, args.package, report=info)
            print("rescrubbed: %s; files written: %d; rewrites: %s" % (args.id, len(info["written"]), ", ".join(
                "%s x %d" % kv for kv in sorted(info["counts"].items())) or "none"))
            print("text-derived ids re-keyed: U- %d (%d replacements), G- %d (%d replacements)"
                  % (info["ids"]["U"][1], info["ids"]["U"][0], info["ids"]["G"][1], info["ids"]["G"][0]))
            print("\n".join("  written: " + w for w in info["written"]))
        elif args.cmd == "capture":
            info = {}
            print("captured:", capture(args.source, args.id, args.cut_after_seq, args.drop, args.package, report=info).name)
            print("size: %d bytes" % info["size"])
            print("foreign roots: %d" % info["paths"])
            print("rewrites: " + (", ".join("%s x %d" % kv for kv in sorted(info["rewrites"].items())) or "none"))
            print("text-derived ids re-keyed: U- %d (%d replacements), G- %d (%d replacements)"
                  % (info["ids"]["U"][1], info["ids"]["U"][0], info["ids"]["G"][1], info["ids"]["G"][0]))
            print("dropped globs matched %d files" % len(info["dropped"]))
        else:
            print("expected.json: %d stages" % len(expected(args.id, args.package)["stages"]))
    except Refusal as exc:
        print("\n".join(exc.lines), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
