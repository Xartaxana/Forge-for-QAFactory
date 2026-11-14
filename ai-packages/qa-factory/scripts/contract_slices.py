"""Role slices of the references: one source of truth, one injected file per reader.

A reference stays ONE file per subject — the truth about that subject is in one place and is
edited in one place. What a role is injected is a SLICE of it: the file's lead plus only the
sections marked for that role.

Markup (its own line directly above a `##`/`###` heading of `references/*.md`):

    <!-- roles: qa-automator, qa-code-critic -->
    ## `automation-manifest.json`

    <!-- roles: all -->
    ## Design review

The marker sits ABOVE the heading and never inside it, so that the heading line stays byte
for byte what it was: several checks match section headings exactly (`test_stages.py` reads
the artifact tree out of "## Where artifacts live", `critic_rollcall.py` reads
"## Gate A debts"), and marking a section must never be able to break one of them.

`all` means every role that has a slice of this file. A `###` heading with no marker of its
own belongs to its `##` parent; a marked `###` is its own section and is not repeated under
the parent. Text before the first heading is the lead and is in every slice: it says what the
subject is, and a slice that opens mid-rule reads as a different document.

Generation is a build step, not runtime: `--write` renders `references/slices/<role>/<subject>.md`
and the files are COMMITTED. The injection hook has no time to render anything (TP1-15045:
a dispatch pays for every byte on every turn and the hook must fail open in milliseconds), so
`--check` is what keeps a slice honest — selftest and audit A9 run it, and a stale slice is a
red build, never a silent half-truth delivered to a role.

Why slices at all (owner's decision of 21.09): the audit capped what one role is
injected at 42,000 bytes (since RC1-14 audit A22 judges the role's whole start load in tokens,
`role_load.py`), and five roles sat within a thousand bytes of the cap while four of
them were writing fields out of documents nobody delivered to them. Splitting a subject into
one file per reader would have given the same fact two owners (audit A21); splitting by
section keeps one owner and pays only for what the reader acts on.

CLI:
  --write     render every slice named in references/inject-map.json, and the one generated
              line of every charter (the digest form is `common-rules.md`'s fact, not theirs)
  --check     exit 2 with the reason when any slice or generated charter line is missing,
              stale, empty or orphaned
  --report    per-role injected bytes, whole sources vs slices, and the common layer (`common_layer`)
  --selftest  unit checks of the parser and the freshness rules on synthetic text
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from content_size import content_bytes  # noqa: E402
from hooklib import read_json, sorted_paths  # noqa: E402

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SLICES_REL = "references/slices"
PLUGIN_PREFIX = "plugin:"
SLICE_PREFIX = PLUGIN_PREFIX + SLICES_REL + "/"
ROLE_MARKER = re.compile(r"<!--\s*roles:\s*([^>]*?)\s*-->")
KIND_LINE = re.compile(r"<!--\s*kind:\s*[A-Za-z0-9_-]+\s*-->")      # role_load.KIND_MARKER: craft/process, no meaning to a slice
HEADING = re.compile(r"^(#{2,3})\s+(.*)$")
WRITER = re.compile(r"\*\*Writer\*\*\s+`(qa-[a-z-]+)`")
# The subjects of the COMMON layer: each role's slice of them is delivered in every mode, so the
# per-role catalogue never names them (inject_context.collect_blocks keeps them out of `on_demand`
# by the same list) and `common_layer` weighs them. The one owner of the list (AR-13).
COMMON_LAYER_SUBJECTS = ("common-rules.md",)
# The generated page of the keys a role hands over (spec t-1765 X1-7): it has no source file to cut from, so
# `targets` skips it and `keys_targets` / `keys_findings` / `keys_write` own it.
KEYS_NAME = "handoff-keys.md"
# A key page that outgrew `W` continues on `handoff-keys-<n>.md`, n >= 2 (§2.6a of the told-before-work spec): the generator owns every
# one of them, the map lists them by a HAND line, and each is injected whole like the first.
KEYS_CONTINUATION = re.compile(r"^handoff-keys-([2-9]|[1-9][0-9]+)\.md$")
# The generated pages are injected inline in EVERY mode: a role is not told to look them up (the rules it must obey are in its prompt).
# `inject_context` reads this one list (`named_instead`, `_dropped_headings`, `map_problems`) and so does the on_demand weight report.
INLINE_SUBJECTS = COMMON_LAYER_SUBJECTS + (KEYS_NAME,)


def keys_page_number(name: str):
    """1 for `handoff-keys.md`, n for the continuation `handoff-keys-<n>.md` (n >= 2), None for any other name."""
    name = Path(str(name)).name
    if name == KEYS_NAME:
        return 1
    found = KEYS_CONTINUATION.match(name)
    return int(found.group(1)) if found else None


def inline_subject(name: str) -> bool:
    """True for the name of an entry that is delivered inline whatever `config.prompts.slices` says: the common-rules slice, the
    key page and a continuation page of it. The one owner of the question (AR-13)."""
    name = Path(str(name)).name
    return name in INLINE_SUBJECTS or keys_page_number(name) is not None


def _provenance(subject: str, role: str) -> str:
    """The first line of every slice. It names the source in the same `plugin:` spelling the
    map uses, so a role that needs the whole subject knows the one file to open and an
    operator reading a dispatch prompt can tell a slice from a source at a glance."""
    return (f"<!-- generated from {PLUGIN_PREFIX}references/{subject} for {role} by "
            "scripts/contract_slices.py; edit the source, never this file -->")


class Section:
    __slots__ = ("heading", "roles", "lines")

    def __init__(self, heading: str, roles: list, lines: list) -> None:
        self.heading, self.roles, self.lines = heading, roles, lines

    @property
    def title(self) -> str:
        return HEADING.match(self.heading).group(2).strip() if HEADING.match(self.heading) else self.heading

    def text(self) -> str:
        return "\n".join([self.heading] + self.lines).rstrip() + "\n"

    def bytes(self) -> int:
        return len(self.text().encode("utf-8"))

    def wants(self, role: str) -> bool:
        return "all" in self.roles or role in self.roles


def parse(text: str) -> tuple:
    """(lead, sections). A heading without a marker keeps the roles of the `##` it sits under,
    which is how a long `##` can be split into `###` parts for the readers that differ without
    re-marking the parts that do not."""
    lead: list = []
    sections: list = []
    current: Section | None = None
    inherited: list = []
    pending: list | None = None
    fence = False
    for line in text.replace("\r\n", "\n").split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            fence = not fence
        if not fence and stripped.startswith("<!--") and ROLE_MARKER.fullmatch(stripped):
            # Held for the next heading, and never written into a slice: the marker is
            # bookkeeping for the generator, not a rule the role has to read.
            pending = [r.strip() for r in ROLE_MARKER.fullmatch(stripped).group(1).split(",") if r.strip()]
            continue
        m = None if fence else HEADING.match(line)
        if m:
            inline = ROLE_MARKER.search(line)
            if inline:  # accepted, but the markup writes the marker above the heading
                roles = [r.strip() for r in inline.group(1).split(",") if r.strip()]
            elif pending is not None:
                roles = list(pending)
            else:
                roles = list(inherited)
            pending = None
            if m.group(1) == "##":
                inherited = list(roles)
            heading = ROLE_MARKER.sub("", line).rstrip()
            current = Section(heading, roles, [])
            sections.append(current)
            continue
        if pending is not None and stripped and not KIND_LINE.fullmatch(stripped):
            # A marker that turned out to head nothing: keep the text, drop the claim. A `<!-- kind: ... -->` line
            # (role_load's craft marker) is not text: the roles marker above it still heads the heading below (t-1793 F6).
            pending = None
        (current.lines if current is not None else lead).append(line)
    return "\n".join(lead).rstrip() + "\n", sections


def marked(text: str) -> bool:
    """A file carrying at least one role marker is a sliced subject: it is injected through
    slices only, so that adding a section for one reader cannot quietly grow every reader."""
    return bool(ROLE_MARKER.search(text))


# A reference may name the closed words of the vocabulary with this token. The role it is injected to
# cannot open `handoffs/vocabulary.yaml` (the pre-tool guard lets a role read only `references/`), so
# "see `vocabulary.<list>`" hands it a name and no word (OH3-14). The slice carries the words
# themselves, written in by the ONE line builder `handoff.grounding_vocabulary_line` (AR-13) - never
# a list typed into the reference. `--check` compares the slice with the CURRENT vocabulary, so a
# vocabulary change makes the slice stale until `--write`: that is the ratchet, the same one the
# charters' digest line has.
GROUNDING_WORDS_TOKEN = "<!-- gen:grounding-words -->"


def grounding_words() -> str:
    """The closed words of `work/grounding.yaml` as one line, from `handoff.grounding_vocabulary_line`. An unreadable
    vocabulary or an empty list is declared inside that line ("NONE READABLE"); a reader that cannot even be imported is
    declared the same way here. Never blank, never raises."""
    try:
        import handoff
        return handoff.grounding_vocabulary_line()
    except Exception as exc:
        return f"NONE READABLE (the vocabulary reader failed: {type(exc).__name__})."


def render(subject: str, role: str, text: str) -> str:
    lead, sections = parse(text)
    chosen = [s for s in sections if s.wants(role)]
    body = "".join("\n" + s.text() for s in chosen)
    out = _provenance(subject, role) + "\n" + lead + body
    return out.replace(GROUNDING_WORDS_TOKEN, grounding_words()) if GROUNDING_WORDS_TOKEN in out else out


def targets(plugin_root: Path) -> list:
    """Every (role, subject) pair inject-map.json asks for, as
    {role, subject, source, slice, entry}. The map is the declaration: a slice exists because
    a role is injected it, never because a marker mentions a role."""
    try:
        imap = json.loads((plugin_root / "references" / "inject-map.json").read_text(encoding="utf-8"))
    except Exception:
        return []
    out = []
    for role, entries in (imap.get("roles") or {}).items():
        for entry in entries or []:
            if not str(entry).startswith(SLICE_PREFIX):
                continue
            rel = str(entry)[len(PLUGIN_PREFIX):]
            parts = Path(rel).parts
            subject = parts[-1]
            if keys_page_number(subject) is not None:   # generated from the contracts, not cut from a source: `keys_targets`
                continue
            out.append({"role": role, "subject": subject, "entry": str(entry),
                        "slice_role": parts[-2],
                        "source": plugin_root / "references" / subject,
                        "slice": plugin_root / rel})
    return sorted(out, key=lambda t: (t["role"], t["subject"]))


def direct_entries(plugin_root: Path) -> list:
    """(role, entry, path) for plugin references injected whole."""
    try:
        imap = json.loads((plugin_root / "references" / "inject-map.json").read_text(encoding="utf-8"))
    except Exception:
        return []
    out = []
    for role, entries in list((imap.get("roles") or {}).items()) + [("common", imap.get("common") or [])]:
        for entry in entries or []:
            e = str(entry)
            if e.startswith(PLUGIN_PREFIX) and not e.startswith(SLICE_PREFIX) and e.endswith(".md"):
                out.append((role, e, plugin_root / e[len(PLUGIN_PREFIX):]))
    return out


def findings(plugin_root: Path) -> list:
    """Everything that makes a slice untrustworthy, in the words the fixer needs."""
    errors: list = []
    wanted = targets(plugin_root)
    for t in wanted:
        if t["slice_role"] != t["role"]:
            errors.append(f"{t['entry']}: injected to {t['role']} but lives in the {t['slice_role']} folder")
        if not t["source"].exists():
            errors.append(f"{t['entry']}: no source references/{t['subject']} to render it from")
            continue
        text = t["source"].read_text(encoding="utf-8")
        if not marked(text):
            errors.append(f"references/{t['subject']}: no `<!-- roles: ... -->` marker anywhere, "
                          f"so the slice for {t['role']} would be the lead alone — mark the sections")
            continue
        fresh = render(t["subject"], t["role"], text)
        if not t["slice"].exists():
            errors.append(f"{t['entry']}: missing — run `python -B scripts/contract_slices.py --write`")
            continue
        if t["slice"].read_text(encoding="utf-8").replace("\r\n", "\n") != fresh:
            errors.append(f"{t['entry']}: stale — the source changed; run "
                          "`python -B scripts/contract_slices.py --write`")
        _, sections = parse(text)
        if not [s for s in sections if s.wants(t["role"])]:
            errors.append(f"{t['entry']}: {t['role']} is marked on no section of references/"
                          f"{t['subject']} — it would be injected a title and nothing else")
        # A role that WRITES an artifact must be injected the section that defines it: the
        # deferred findings of 0.7.7 were four roles writing fields out of contracts nobody
        # delivered (code critic and failure analyst on the automation manifest, case critic
        # on the findings file, doc scribe on coverage links).
        for s in sections:
            writers = set(WRITER.findall(s.text()))
            if t["role"] in writers and not s.wants(t["role"]):
                errors.append(f"references/{t['subject']} `{s.title}` names {t['role']} as its "
                              "**Writer** but the marker leaves it out of that role's slice")
    declared = {t["slice"].resolve() for t in wanted}
    slices_dir = plugin_root / SLICES_REL
    for path in sorted_paths(slices_dir.rglob("*.md")) if slices_dir.exists() else []:
        # The per-role catalogue is this generator's own file, not a slice: it is injected only
        # when `config.prompts.slices` is `on_demand`, so the map never names it.
        if path.name == CATALOGUE_NAME or keys_page_number(path.name) is not None:   # the key pages: `keys_findings` judges them
            continue
        if path.resolve() not in declared:
            errors.append(f"{SLICES_REL}/{path.relative_to(slices_dir).as_posix()}: a slice no "
                          "role is injected — delete it or point inject-map.json at it")
    for role, entry, path in direct_entries(plugin_root):
        if path.exists() and marked(path.read_text(encoding="utf-8")):
            errors.append(f"{entry}: {role} is injected the whole marked subject — point the map "
                          f"at {SLICE_PREFIX}{role}/{path.name}")
    return errors + keys_findings(plugin_root)


def write(plugin_root: Path) -> list:
    """Render every declared slice. Returns the paths that changed."""
    changed = []
    for t in targets(plugin_root):
        if not t["source"].exists():
            continue
        fresh = render(t["subject"], t["role"], t["source"].read_text(encoding="utf-8"))
        old = t["slice"].read_text(encoding="utf-8").replace("\r\n", "\n") if t["slice"].exists() else None
        if old != fresh:
            t["slice"].parent.mkdir(parents=True, exist_ok=True)
            t["slice"].write_text(fresh, encoding="utf-8", newline="\n")
            changed.append(t["slice"])
    return changed


# --- the charters' mechanical line (P7.2/P7.3) ---------------------------------------------------
# The digest FORM belongs to one layer - `references/common-rules.md`, which the injection hook
# delivers to every dispatch. Eleven of the twelve charters restated it anyway, and five of those
# restated a shape the common layer had already replaced: `<role> S8 done|halt · <path> · <one
# fact>`, two parts where the form has three. `role_digest.py` tolerates the old spelling on
# purpose, so nothing was ever red - a story in flight must not be refused over a role file nobody
# updated - and the drift simply stood, in the layer the audit puts its tightest cap on.
#
# So the line is generated from the owners it was copied out of: `role_digest.ROLE_ITEM` for what
# one row is about, `handoffs/vocabulary.yaml` (through `handoff.options_for_role`) for the words
# this role may write in that row, and `references/stages.json` for the artifact path. The charter
# keeps the part that is genuinely its own - everything outside the markers.
CHARTER_OPEN = "<!-- gen:digest contract_slices.py -->"
CHARTER_CLOSE = "<!-- /gen -->"


def _role_states(role: str) -> list:
    """The row states this role may write, from the vocabulary that owns them."""
    try:
        import handoff
        vocab = handoff.vocabulary()
        states = vocab.get("row_states")
        if not isinstance(states, dict):
            return []
        out = []
        for word, spec in states.items():
            spec = spec if isinstance(spec, dict) else {}
            used_by = spec.get("used_by") or ""
            restricted = spec.get("restricted_to") or ""
            if restricted and role not in str(restricted):
                continue
            if used_by and role not in str(used_by) and "all" not in str(used_by):
                continue
            out.append(str(word))
        return out
    except Exception:
        return []


def charter_line(plugin_root: Path, role: str) -> str:
    """The one bullet the generator owns, or "" when this role is not one of the twelve."""
    try:
        sys.path.insert(0, str(plugin_root / "scripts"))
        from role_digest import ROLE_ITEM
    except Exception:
        return ""
    item = ROLE_ITEM.get(role)
    if not item:
        return ""
    # The WORDS are not listed here either, and that is the same rule one layer down: which row
    # states this role may write is `handoffs/vocabulary.yaml`'s fact, narrowed per role by
    # `handoff.options_for_role`, and printed by the check itself the moment a value is wrong. A
    # copy in the charter is a second answer as soon as a word is added - and it cost more bytes
    # than the whole rule it was copied from.
    states = _role_states(role)
    # Whose artifact the path is: `artifact-writers.json` is where that is decided ("one
    # artifact, one writer"), so the charter quotes the owner rather than a guess from the stage
    # table - which gave the bug reporter `work/ledger.json`, a file it does not own.
    artifact = ""
    try:
        writers = json.loads((plugin_root / "references" / "artifact-writers.json")
                             .read_text(encoding="utf-8")).get("artifacts") or {}
        mine = [name for name, spec in writers.items()
                if str((spec or {}).get("writer") or "").split()[0:1] == [role]]
        artifact = mine[0] if mine else ""
    except Exception:
        artifact = ""
    # A role that owns no artifact of its own - the two critics write a findings file, the
    # automator and the runner write into files code owns - is not given a path GUESSED from its
    # stage: the stage table hands both S4 roles `work/test-cases/`, which is the designer's. What
    # it writes is its own Outputs block, one section above, and that is where the charter points.
    # A role that may be dispatched for the S5 PLAN as well as for a window ends its digest on a
    # different file by purpose (the plan, or the window's own artifact) and counts a different
    # unit (a case, or a test instance): one generated line cannot name either truthfully, so it
    # names no path and its item word covers both. The fact is `controller.S5_PLAN_ROLES`, the
    # survivor that already gates `--purpose s5_plan` (AR-13); no second list here.
    try:
        from controller import S5_PLAN_ROLES
    except Exception:
        S5_PLAN_ROLES = ()
    if role in S5_PLAN_ROLES:
        artifact = ""
        item = f"{item} (a plan dispatch: per case)"
    where = (f"`{artifact}`" if artifact else "what you wrote (your `Outputs` above)")
    parts = [f"- Digest: the common form (`common-rules.md`), one line per {item}, then {where}."]
    if not states:                                    # a role the vocabulary gives no word to
        parts.append("  Your states are the ones your artifact's contract names.")
    return "\n".join(parts)


def charter_targets(plugin_root: Path) -> list:
    """[(role, path)] of the charters the generator owns a block in."""
    out = []
    for path in sorted_paths((plugin_root / "agents").glob("qa-*.md")):
        if charter_line(plugin_root, path.stem):
            out.append((path.stem, path))
    return out


def charter_block(plugin_root: Path, role: str) -> str:
    return "\n".join([CHARTER_OPEN, charter_line(plugin_root, role), CHARTER_CLOSE])


def charter_rendered(plugin_root: Path, role: str, text: str) -> str:
    """`text` with the generated block put where it belongs: replacing the block that is there,
    or replacing the hand-written `- Digest:` bullet the first time."""
    block = charter_block(plugin_root, role)
    if CHARTER_OPEN in text:
        head, _, rest = text.partition(CHARTER_OPEN)
        _, _, tail = rest.partition(CHARTER_CLOSE)
        return head + block + tail
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if not line.startswith("- Digest:"):
            continue
        end = i + 1
        while end < len(lines) and lines[end].startswith("  ") and lines[end].strip():
            end += 1
        return "\n".join(lines[:i] + block.split("\n") + lines[end:])
    return text


def charter_findings(plugin_root: Path) -> list:
    out = []
    for role, path in charter_targets(plugin_root):
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        if CHARTER_OPEN not in text:
            out.append(f"agents/{path.name}: restates the digest form by hand — the form belongs "
                       "to references/common-rules.md; run "
                       "`python -B scripts/contract_slices.py --write`")
            continue
        if charter_rendered(plugin_root, role, text) != text:
            out.append(f"agents/{path.name}: the generated digest line is stale (the vocabulary or "
                       "the stage table moved) — run "
                       "`python -B scripts/contract_slices.py --write`")
    return out


def charter_write(plugin_root: Path) -> list:
    changed = []
    for role, path in charter_targets(plugin_root):
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        fresh = charter_rendered(plugin_root, role, text)
        if fresh != text:
            path.write_text(fresh, encoding="utf-8")
            changed.append(f"agents/{path.name}: digest line generated")
    return changed


# --- the key page: what a role hands over, generated from the carriers (spec t-1765 X1-7) --------
# A role's file used to say which artifacts it writes, which witness it leaves and which fields its handoff form has - a
# copy of tables other files own. The page is those tables read for ONE role and printed: `artifact-writers.json` (who
# writes what, and why), `validate_artifacts.PHASE_JSON_KEYS` (the keys the validator requires), `stages.json` (the stage's
# required outputs, the gate's detectors, the witness), `stage-joints.json` (what else a gate reads of the role) and the
# handoff form of the role's stage (`handoff.spec_of`, so a field added to the form is on the page by itself). The role
# gets it as one slice in `inject-map.json`; `--check` refuses a page that is missing or stale, so it is never edited by hand.
def _json_of(path: Path):
    # THE reader (AR-13); errors=Exception keeps this caller's outcome (anything unreadable is "nothing there", a
    # nesting too deep for the parser included), kind=dict because every caller below goes on with `.get`.
    return read_json(path, kind=dict, errors=Exception)


def keys_targets(plugin_root: Path) -> list:
    """[(role, entry, path)] of the key pages inject-map.json names (the first page and its continuations): the map is the
    declaration, as for slices."""
    imap = _json_of(plugin_root / "references" / "inject-map.json") or {}
    out = []
    for role, entries in (imap.get("roles") or {}).items():
        for entry in entries or []:
            e = str(entry)
            if e.startswith(SLICE_PREFIX) and keys_page_number(e) is not None:
                out.append((role, e, plugin_root / e[len(PLUGIN_PREFIX):]))
    return sorted(out, key=lambda t: (t[0], keys_page_number(t[1]), t[1]))


def _listed_pages(plugin_root: Path, role: str) -> list:
    """The page numbers of `role` that inject-map.json lists, sorted (a number listed twice stands once)."""
    return sorted({keys_page_number(e) for r, e, _p in keys_targets(plugin_root) if r == role})


def _consecutive(numbers: list) -> int:
    """How many pages 1, 2, 3 ... the sorted `numbers` hold without a gap (0 when page 1 is not listed)."""
    count = 0
    while count < len(numbers) and numbers[count] == count + 1:
        count += 1
    return count


def _keys_outputs(plugin_root: Path, role: str, stage, writers: dict) -> list:
    """The `## Outputs` lines: the artifacts the role writes, the stage's required outputs, the gate's re-runs and the extra
    demands the joints registry makes of this very page. An unknown is declared, never left out (AR-28)."""
    lines = ["## Outputs", ""]
    mine = [(name, spec) for name, spec in writers.items()
            if str((spec or {}).get("writer") or "").split()[0:1] == [role]]
    keys = {}
    try:
        import validate_artifacts
        keys = validate_artifacts.PHASE_JSON_KEYS
    except Exception as exc:
        lines += [f"- NOT KNOWN: the validator's key table could not be read ({type(exc).__name__})."]
    for name, spec in mine:
        lines.append(f"- `{name}` - {' '.join(str(spec.get('why') or '').split())}")
        required = keys.get(Path(name).name)
        if required:
            lines.append("  Keys the validator requires: " + ", ".join(f"`{k}`" for k in required) + ".")
    if not mine:
        lines.append("- You write no artifact of your own: what you hand over is your handoff form and what your brief names.")
    if stage is None:
        lines += ["", f"NOT KNOWN: {role} is in no stage of stages.json, so its required outputs are not listed."]
        return lines
    lines += ["", f"Required at your stop (stage {stage.get('id')}): "
              + (", ".join(f"`{o}`" for o in stage.get("required_outputs") or []) or "nothing") + "."]
    ran = (stage.get("detectors") or {}).get(role) or []
    advice = {str(s) for s in stage.get("advice") or []}
    if ran:
        lines.append("Re-run by the gate at your stop: "
                     + ", ".join(f"`{s}`" + (" (advice only)" if s in advice else "") for s in ran) + ".")
    import stage_joints
    joints = stage_joints.load_rows(plugin_root / "references" / "stage-joints.json")[0] or {}   # THE reader of the rows (AR-13)
    page = f"references/slices/{role}/{KEYS_NAME}"
    extra = []
    for joint in joints.get("joints") or []:
        for producer in joint.get("producers") or []:
            if role not in (producer.get("roles") or []):
                continue
            if not any(str(t.get("path") or "").replace("<role>", role) == page for t in producer.get("told") or []):
                continue
            extra += [f"- {producer.get('field')}: `{token}`" for token in producer.get("demands") or []]
    if extra:
        lines += ["The gate also reads:"] + list(dict.fromkeys(extra))
    return lines


def _keys_form(role: str, stage) -> list:
    """The `## Handoff form` lines: every field of the role's handoff form that it fills, with the word `required` or
    `optional` and the form's own hint (and a trailing `# Fill:` comment of the form, when it has one)."""
    lines = ["## Handoff form", ""]
    try:
        import handoff
        contract = handoff.contract_of(str(stage.get("id")), role) if stage else ""
        if not contract:
            return lines + [f"NOT KNOWN: no handoff contract is registered for {role} in handoffs/index.yaml."]
        doc = handoff.template(contract)
        spec = handoff.spec_of(doc)
        first = {}
        for path, node in doc.nodes.items():
            first.setdefault(re.sub(r"\[\d+\]", "[]", path), node)
        lines += [f"Contract `{contract}` (fill `work/handoffs/<dispatch>.yaml`; `handoff_check.py` reads it):", ""]
        for generic, field in spec.items():
            node = first.get(generic)
            if handoff.owned_by_contract(generic) or node is None or not handoff.is_placeholder(node.value):
                continue
            fill = (node.comment or "").lstrip("#").strip()
            fill = f" {fill}" if fill.startswith("Fill:") else ""
            # `handoff_check.check` never refuses an unfilled `blocked.*` field: it is filled only when the role is blocked
            word = "only when blocked" if generic.startswith("blocked.") else ("optional" if field.optional else "required")
            lines.append(f"- `{generic}` ({word}) - "
                         f"{' '.join(str(field.hint).split())}{fill}")
        shape = handoff.index().get("common_shape")
        if isinstance(shape, dict):
            lines += ["", "Every handoff form shares one skeleton (`common_shape` of handoffs/index.yaml): "
                      + ", ".join(f"`{k}`" for k in shape) + "."]
    except Exception as exc:
        lines.append(f"NOT KNOWN: the handoff form could not be read ({type(exc).__name__}).")
    return lines


# --- the told section of the key page: "What code will check of you" (T3a of the told-before-work spec) -------------------
# The rows of `stage-joints.json` that state a requirement are rendered here, for ONE role, by the one line renderer
# `stage_joints.told_line`. The page is the survivor of the told carriers (the text reaches the role whole before its work); a
# row that cannot be read, a role with no rows and a card that has not yet moved to rows are each SAID on the page, never left out.
SECTION_HEAD = "## What code will check of you"
SECTION_LEGEND = ("`<T>` is your ticket, `<ID>` your dispatch id, `<home>` the project's qa-factory folder - all three stand in "
                  "your prompt (`Ticket: ... Dispatch: ...`) and in your task packet.")
NOT_YET_HEAD = "### Not yet in rows"
NONE_ROLE = "- none: code checks nothing of this role beyond the sections above"
NONE_CONTINUED = "- none: every row of this role stands on the pages before this one"
ROWS_LATER = "- the rows of this role stand on the pages after this one"
# The dispatch tokens a row's `when` can hold, in the order of their sub-headings, with the words of the heading. How a token
# relates to another (`replaces` / `replaced by`) is the DATA's (`stage-joints.json` `when_exclusive`), never written here.
GROUPS = (("plan", "Only in a plan dispatch"), ("window", "Only in a window"), ("manual", "Only in a manual block"),
          ("first_look", "Only in a first look"), ("not_first_look", "Not in a first look"), ("walk", "Only in a walk"))
CARD_GROUP = "card"


def page_name(n: int) -> str:
    return KEYS_NAME if n == 1 else f"handoff-keys-{n}.md"


# The ONE literal of the per-slice byte cap (AR-13): `selftest.REFERENCE_MD_MAX_BYTES` re-exports it, `--limits` judges every slice
# file against it, and the partition of a key page keeps each page at or under it as well as under `W` (F-10 (a): both limits met).
SLICE_MAX_BYTES = 12_000


def size_limits() -> tuple:
    """`(L, W)`: `inject_context.MAX_BLOCK_CHARS` (imported, never a second literal) and 80 % of it, the split threshold of K8.
    The partition of a key page splits at the stricter of `W` (characters) and `SLICE_MAX_BYTES` (bytes)."""
    import inject_context
    limit = inject_context.MAX_BLOCK_CHARS
    return limit, (limit * 8) // 10


def ahead_card(role: str, plugin_root: Path = PLUGIN_ROOT) -> str:
    """The card this role is handed by hand (`references/ahead-cards.json`), or "" when none is there for it. The moved copy of
    `brief_pack.ahead_card`, which stays until the brief side moves to rows (T3b)."""
    cards = (_json_of(Path(plugin_root) / "references" / "ahead-cards.json") or {}).get("cards") or {}
    entry = cards.get(role) if isinstance(cards, dict) else None
    return str((entry or {}).get("text") or "").strip() if isinstance(entry, dict) else ""


def _group_heading(token: str, exclusive) -> str:
    """The sub-heading of a dispatch group; `(replaces "<other>")` / `(replaced by "<other>")` come from `when_exclusive` pairs
    (the first member replaces the second), an additive group has none."""
    names = dict(GROUPS)
    for pair in exclusive if isinstance(exclusive, list) else []:
        if isinstance(pair, list) and len(pair) == 2 and token in pair and all(str(t) in names for t in pair):
            other = pair[1] if pair[0] == token else pair[0]
            return f'### {names[token]} ({"replaces" if pair[0] == token else "replaced by"} "{names[other]}")'
    return f"### {names[token]}"


def _row_order(row: dict, order: dict) -> tuple:
    stages = row.get("stages")
    stages = [stages] if isinstance(stages, str) else [s for s in stages or [] if isinstance(s, str)]
    first = min([0 if s == "*" else order.get(s, len(order)) for s in stages] or [len(order)])
    return first, str(row.get("check"))


def _continuation_head(role: str, n: int) -> list:
    """The lines of page `n` (>= 2) before its section: the provenance comment of a generated page."""
    return [f"<!-- generated by scripts/contract_slices.py (handoff_keys_page): page {n} of the key page of {role}, the rest of "
            "its section; edit stage-joints.json, never this file -->"]


# The index line of a family whose rows are told at the call (T1r-pages; its family list is DATA, `call_told_families` of
# stage-joints.json). The page keeps one line per family so the role knows the checks exist; the refusal of the call tells each
# whole. Only the WORDS live here: what the family's calls are, and the closing sentence that is true for it. A listed family with
# no entry gets the plain words (`CALL_WHAT_DEFAULT`, no closing sentence) - never a line that promises more than the family keeps.
CALL_LINE = ("- [{family}:*] {n} checks of your {what} are told in the refusal of the call, with what they expect and the door"
             "{tail}.")
CALL_WHAT_DEFAULT = "commands"
CALL_WHAT = {"guard_pre_tool": "tool calls", "stage_guard": "tool calls", "host_adapter": "tool calls"}
CALL_NOTHING_LOST = ("guard_pre_tool", "stage_guard", "host_adapter")     # a refusal before any effect: nothing written is lost
CALL_NOTHING_LOST_TAIL = "; nothing you have written is lost by them"
CALL_HELP_FAMILY = "role_cli"                                              # a refusal that comes after an input file was written
CALL_HELP_TAIL = (". Run {scripts} before you write an input file: it prints what each command of the script checks")


def _call_index_lines(families, called_rows: list) -> list:
    """One line per family of `families` (in the list's order) that holds at least one of `called_rows`, with the count. The
    role_cli line names `<script> --help` for every script of its rows (the card before the file, not after the refusal)."""
    out = []
    for family in families:
        mine = [r for r in called_rows if str(r.get("check")).split(":", 1)[0] == family]
        if not mine:
            continue
        tail = CALL_NOTHING_LOST_TAIL if family in CALL_NOTHING_LOST else ""
        if family == CALL_HELP_FAMILY:
            scripts = sorted({str(r.get("check")).split(":", 1)[1].split()[0] for r in mine if ":" in str(r.get("check"))})
            tail = CALL_HELP_TAIL.format(scripts=", ".join(f"`{s} --help`" for s in scripts))
        out.append(CALL_LINE.format(family=family, n=len(mine), what=CALL_WHAT.get(family, CALL_WHAT_DEFAULT), tail=tail))
    return out


def _told_units(plugin_root: Path, role: str, model: dict) -> tuple:
    """`(units, exclusive, why)`: the pieces the section is laid from, in page order. A unit is `(group, text)`: `group` None for
    a row that holds in every dispatch (capability tokens only), a dispatch token of `GROUPS` for a row of that group (a row
    holding two dispatch tokens stands under each: more text, never a row left out), `CARD_GROUP` for the card of a role whose
    cards are not yet rows. `why` is not empty when `stage-joints.json` could not be read: no unit, never an empty section passed
    as fine."""
    import stage_joints
    data, why = stage_joints.load_rows(plugin_root / "references" / "stage-joints.json")
    if data is None:
        return [], [], why
    from stage_guard import stages_of_role
    ids = [str(s.get("id")) for s in stages_of_role(model, role)]
    order = {str(s.get("id")): i for i, s in enumerate(model.get("stages") or [])}
    rows = sorted(stage_joints.rows_for(role, ids, None, data=data), key=lambda r: _row_order(r, order))
    families = stage_joints.call_families(data)
    called = [stage_joints.call_told(r, role, families) for r in rows]
    told = [r for r, at_call in zip(rows, called) if not at_call]          # the rows the role's page tells whole
    groups = [token for token, _name in GROUPS]
    units = [(None, stage_joints.told_line(r)) for r in told
             if not [t for t in r.get("when") or [] if t in groups]]
    units += [(None, line) for line in _call_index_lines(families, [r for r, at_call in zip(rows, called) if at_call])]
    rows = told
    for token in groups:
        units += [(token, stage_joints.told_line(r)) for r in rows if token in (r.get("when") or [])]
    hand = (data.get("told_ratchet") or {}).get("hand_cards")
    card = ahead_card(role, plugin_root)
    if card and (hand is None or (isinstance(hand, int) and not isinstance(hand, bool) and hand > 0)):
        units.append((CARD_GROUP, card))
    return units, data.get("when_exclusive") or [], ""


def _page_text(lines: list) -> str:
    return "\n".join(lines).rstrip() + "\n"


def _section_lines(page: int, units: list, earlier: set, exclusive, total: int) -> list:
    """The lines of the section on page `page` (1-based) holding `units`; `earlier` is the set of groups whose rows already
    stood on a page before this one (their heading repeats with ` (continued)`); `total` is how many units the role has."""
    lines = [SECTION_HEAD if page == 1 else f"{SECTION_HEAD} (continued from {page_name(page - 1)})", "", SECTION_LEGEND]
    if not units:
        return lines + ["", NONE_ROLE if total == 0 else (ROWS_LATER if page == 1 else NONE_CONTINUED)]
    current = "-"
    for group, text in units:
        if group != current:
            current = group
            if group is None:
                lines.append("")
            elif group == CARD_GROUP:
                lines += ["", NOT_YET_HEAD, ""]
            else:
                lines += ["", _group_heading(group, exclusive) + (" (continued)" if group in earlier else ""), ""]
        lines.append(text)
    return lines


def requirement_section(plugin_root: Path, role: str, head=(), model=None, pages: int = 1) -> list:
    """The section "What code will check of you" of the key pages of `role`: a list with the lines of the section on each of
    `pages` listed pages (page 1 first). `head` is the text of page 1 before the section (the fixed sections: only its size
    matters, for the split); `model` is stages.json (read when None). The rows are laid in order and a row goes to the current
    page while the page stays at or under `W` (K8, characters) AND at or under `SLICE_MAX_BYTES` (bytes) with it, else to the
    next page; the LAST page takes every remaining row; a row is never cut. A row told at the call (`call_told_families`) is
    not laid: its family has one index line instead. A role with no rows says so (`none`), a continuation page with no rows says so, and a rows file that
    cannot be read is named on the page. Also the attribute whose presence turns the page leg of `stage_joints` on (K2)."""
    model = model if isinstance(model, dict) else (_json_of(plugin_root / "references" / "stages.json") or {})
    units, exclusive, why = _told_units(plugin_root, role, model)
    if why:
        unknown = f"NOT KNOWN: the rows of what code checks could not be read ({why})."
        return [[SECTION_HEAD if n == 1 else f"{SECTION_HEAD} (continued from {page_name(n - 1)})", "", SECTION_LEGEND, "", unknown]
                for n in range(1, max(1, pages) + 1)]
    _limit, width = size_limits()
    placed = [[] for _ in range(max(1, pages))]
    where = 0
    for unit in units:
        while where < len(placed) - 1:
            seen = {g for earlier in placed[:where] for g, _t in earlier}
            base = list(head) if where == 0 else _continuation_head(role, where + 1)
            trial = base + [""] + _section_lines(where + 1, placed[where] + [unit], seen, exclusive, len(units))
            fits = _page_text(trial)
            if len(fits.strip()) <= width and len(fits.encode("utf-8")) <= SLICE_MAX_BYTES:       # the stricter of K8's W and the slice cap
                break
            where += 1
        placed[where].append(unit)
    out = []
    for n, mine in enumerate(placed, start=1):
        seen = {g for earlier in placed[:n - 1] for g, _t in earlier}
        out.append(_section_lines(n, mine, seen, exclusive, len(units)))
    return out


def _role_pages(plugin_root: Path, role: str) -> tuple:
    """`(pages, problems)`: the text of every listed key page of `role` (page 1 first) and what is wrong while generating them
    (a rows file that cannot be read, a row longer than the split threshold on its own)."""
    model = _json_of(plugin_root / "references" / "stages.json") or {}
    writers = (_json_of(plugin_root / "references" / "artifact-writers.json") or {}).get("artifacts") or {}
    try:
        from stage_guard import stage_of_role
        stage = stage_of_role(model, role)
    except Exception:
        stage = None
    head = [f"<!-- generated by scripts/contract_slices.py (handoff_keys_page) from artifact-writers.json, stages.json, "
            f"stage-joints.json and handoffs/*.yaml for {role}; edit those, never this file -->",
            "", f"# Keys you hand over - {role}", ""]
    head += _keys_outputs(plugin_root, role, stage, writers)
    witness = (model.get("witness") or {}).get(role)
    head += ["", "## Witness", "",
             (f"Your witness artifact (stages.json `witness`): `{witness}`." if witness
              else f"NOT KNOWN: stages.json declares no witness for {role}.")]
    head += [""] + _keys_form(role, stage)
    count = max(1, _consecutive(_listed_pages(plugin_root, role)))
    sections = requirement_section(plugin_root, role, head, model, count)
    pages = [_page_text(head + [""] + sections[0])]
    for n in range(2, count + 1):
        pages.append(_page_text(_continuation_head(role, n) + [""] + sections[n - 1]))
    problems = []
    units, _exclusive, why = _told_units(plugin_root, role, model)
    if why:
        problems.append(f"references/stage-joints.json cannot be read ({why}): the key pages cannot say what code checks of a role")
    _limit, width = size_limits()
    problems += [f"K8 {role}: one row is over the split threshold ({len(text)} characters, the threshold {width}): "
                 f"shorten the sentence ({text[:60]}...)" for group, text in units if group != CARD_GROUP and len(text) > width]
    return pages, problems


def handoff_keys_pages(plugin_root: Path, role: str) -> list:
    """The generated key pages of ONE role, as many as inject-map.json lists for it (at least one): Outputs, Witness, the handoff
    form and the section of the rows. Pure and deterministic; a carrier it cannot read is named on the page, never dropped."""
    return _role_pages(plugin_root, role)[0]


def handoff_keys_page(plugin_root: Path, role: str) -> str:
    """The generated `references/slices/<role>/handoff-keys.md` (page 1): Outputs, Witness, the handoff form and the section
    "What code will check of you". The continuation pages are `handoff_keys_pages(...)[1:]`."""
    return handoff_keys_pages(plugin_root, role)[0]


def size_finding(rel: str, role: str, n: int, size: int) -> tuple:
    """K8 on one page file of `size` characters (`len(text.strip())`, the measure `inject_context.collect_blocks` applies):
    `("", "")` under `W`, `("warn", text)` from `W` to `L`, `("red", text)` over `L`. The text names the one move: the split.
    The byte cap is judged by `selftest --limits` (its door for a key page: the same split line)."""
    limit, width = size_limits()
    if size < width:
        return "", ""
    name = page_name(n)
    text = (f"K8 {rel}: {size} chars, at or over 80 % of MAX_BLOCK_CHARS ({limit}). Split: add the line "
            f'"plugin:references/slices/{role}/{page_name(n + 1)}" right after "…/{name}" in references/inject-map.json '
            f"roles.{role}, then run python -B scripts/contract_slices.py --write")
    return ("red" if size > limit else "warn"), text


def _page_sizes(plugin_root: Path) -> list:
    """[(rel, role, n, size)] of every listed key page file that exists."""
    out = []
    for role, entry, path in keys_targets(plugin_root):
        if path.parent.name == role and path.exists():
            text = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
            out.append((path.relative_to(plugin_root).as_posix(), role, keys_page_number(entry), len(text.strip())))
    return out


def keys_warnings(plugin_root: Path) -> list:
    """The K8 WARN lines (`WARN K8 ...`): a page at or over 80 % of `MAX_BLOCK_CHARS` and not over it. Not a finding: exit 0."""
    return [f"WARN {text}" for kind, text in (size_finding(*page) for page in _page_sizes(plugin_root)) if kind == "warn"]


def keys_findings(plugin_root: Path) -> list:
    out = []
    declared, cache = set(), {}
    listed = {}
    for role, entry, _path in keys_targets(plugin_root):
        listed.setdefault(role, []).append(keys_page_number(entry))
    for role, numbers in sorted(listed.items()):
        numbers = sorted(set(numbers))
        have = _consecutive(numbers)
        if have != len(numbers):
            gap = next(n for n in range(1, numbers[-1] + 1) if n not in numbers)
            out.append(f"references/inject-map.json roles.{role}: the key pages are not consecutive - {page_name(gap)} is not "
                       f"listed but {page_name(numbers[-1])} is; list every page from the first, or none after the gap")
    for role, entry, path in keys_targets(plugin_root):
        declared.add(path.resolve())
        n = keys_page_number(entry)
        if path.parent.name != role:
            out.append(f"{entry}: injected to {role} but lives in the {path.parent.name} folder")
        elif not path.exists():
            out.append(f"{entry}: missing - run `python -B scripts/contract_slices.py --write`")
        else:
            if role not in cache:
                cache[role] = _role_pages(plugin_root, role)
            pages = cache[role][0]
            if n <= len(pages) and path.read_text(encoding="utf-8").replace("\r\n", "\n") != pages[n - 1]:
                out.append(f"{entry}: stale - a carrier changed; run `python -B scripts/contract_slices.py --write`")
    for rel, role, n, size in _page_sizes(plugin_root):
        kind, text = size_finding(rel, role, n, size)
        if kind == "red":
            out.append(text)
    out += list(dict.fromkeys(p for _pages, problems in cache.values() for p in problems))
    slices_dir = plugin_root / SLICES_REL
    for path in sorted_paths(slices_dir.rglob("handoff-keys*.md")) if slices_dir.exists() else []:
        if keys_page_number(path.name) is not None and path.resolve() not in declared:
            rel = f"{SLICES_REL}/{path.relative_to(slices_dir).as_posix()}"
            out.append(f"unlisted generated page {rel}: a key page no role is injected - delete it (`--write` does) "
                       "or point inject-map.json at it")
    try:
        import role_load
        out += role_load.native_headroom_problems(plugin_root)       # K10: the plugin share against the Codex native ceiling
    except Exception as exc:
        out.append(f"K10 native headroom could not be judged ({type(exc).__name__}: {exc})")
    return out


def keys_write(plugin_root: Path) -> list:
    """Write every listed key page that is not fresh and delete every generated page no role lists; the relative paths written,
    and `deleted <path>` for each deletion."""
    changed, declared, cache = [], set(), {}
    for role, entry, path in keys_targets(plugin_root):
        declared.add(path.resolve())
        if path.parent.name != role:
            continue
        if role not in cache:
            cache[role] = handoff_keys_pages(plugin_root, role)
        n = keys_page_number(entry)
        if n > len(cache[role]):
            continue                                     # a gap in the list: `keys_findings` names it, nothing is guessed
        fresh = cache[role][n - 1]
        old = path.read_text(encoding="utf-8").replace("\r\n", "\n") if path.exists() else None
        if old != fresh:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(fresh, encoding="utf-8", newline="\n")
            changed.append(path.relative_to(plugin_root).as_posix())
    slices_dir = plugin_root / SLICES_REL
    for path in sorted_paths(slices_dir.rglob("handoff-keys*.md")) if slices_dir.exists() else []:
        if keys_page_number(path.name) is not None and path.resolve() not in declared:
            path.unlink()
            changed.append(f"deleted {path.relative_to(plugin_root).as_posix()}")
    return changed


# --- the catalogue: slices named instead of delivered (P7.4) -------------------------------------
# The heaviest layer of a dispatch is the slices: 23,626 bytes for the code critic against 8,881 of
# charter. The plan's proposal is to hand a role their PATHS and one line of what is in each, the
# way the brief already hands it files and commands, and let it read what it needs - 15-20 KB off
# every dispatch, more than the whole charter budget.
#
# It is generated here and it is OFF by default, and the reason is a measurement this factory was
# built on: `inject_context.py`'s own note records that 0 of 290 dispatched subagents opened a file
# they were told to read. The brief is not a counter-example - it names files the role needs FOR
# its work (the diff, the plan), not rules it must obey. So the saving is real and the risk is
# real, and which one wins is not a thing to assume: `config.prompts.slices: on_demand` turns it
# on, `stage_compare` on a real story says whether the artifacts got worse, and until that number
# exists the default stays `inline`.
CATALOGUE_NAME = "index.md"
CATALOGUE_HEAD = """# Your rule files — paths, not copies

Each line is a file of YOUR rules and the sections it carries. They are not in this prompt: read
the ones your work touches BEFORE you write your artifact, the way you read the files the brief
names. A rule you did not read is still a rule the exit gate checks.
"""


def catalogue(plugin_root: Path, role: str) -> str:
    """The role's slices as paths plus what each carries."""
    lines = [CATALOGUE_HEAD]
    for t in targets(plugin_root):
        if t["role"] != role or not t["slice"].exists():
            continue
        if t["subject"] in COMMON_LAYER_SUBJECTS:      # always delivered, so never "named instead"
            continue
        text = t["slice"].read_text(encoding="utf-8")
        heads = [HEADING.match(ln).group(2).strip()
                 for ln in text.split("\n") if HEADING.match(ln)]
        rel = t["slice"].relative_to(plugin_root).as_posix()
        lines.append(f"- `{rel}` ({content_bytes(t['slice']):,} B) — "
                     + (", ".join(heads[:6]) + ("…" if len(heads) > 6 else "")
                        if heads else "one subject, no sections"))
    for _role, _entry, page in keys_targets(plugin_root):
        if _role == role and page.exists():
            heads = [HEADING.match(ln).group(2).strip() for ln in page.read_text(encoding="utf-8").split("\n")
                     if HEADING.match(ln)]
            lines.append(f"- `{page.relative_to(plugin_root).as_posix()}` ({content_bytes(page):,} B) — "
                         + ", ".join(heads))
    return "\n".join(lines) + "\n"


def catalogue_path(plugin_root: Path, role: str) -> Path:
    return plugin_root / SLICES_REL / role / CATALOGUE_NAME


def catalogue_roles(plugin_root: Path) -> list:
    return sorted({t["role"] for t in targets(plugin_root)})


def catalogue_write(plugin_root: Path) -> list:
    changed = []
    for role in catalogue_roles(plugin_root):
        path = catalogue_path(plugin_root, role)
        fresh = catalogue(plugin_root, role)
        old = path.read_text(encoding="utf-8").replace("\r\n", "\n") if path.exists() else None
        if old != fresh:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(fresh, encoding="utf-8", newline="\n")
            changed.append(path.relative_to(plugin_root).as_posix())
    return changed


def catalogue_findings(plugin_root: Path) -> list:
    out = []
    for role in catalogue_roles(plugin_root):
        path = catalogue_path(plugin_root, role)
        if not path.exists():
            out.append(f"{SLICES_REL}/{role}/{CATALOGUE_NAME}: missing — run "
                       "`python -B scripts/contract_slices.py --write`")
        elif path.read_text(encoding="utf-8").replace("\r\n", "\n") != catalogue(plugin_root, role):
            out.append(f"{SLICES_REL}/{role}/{CATALOGUE_NAME}: stale — run "
                       "`python -B scripts/contract_slices.py --write`")
    return out


def common_layer(plugin_root: Path) -> dict:
    """What every role is handed ALIKE, in bytes - the one measurer (AR-13) A22 and `--report` both call.

    {"list": the bytes of the `common` entries of the map,
     "shared": list + the bytes every role's slice of a common-layer subject has in common: the lead and
               the `all` sections, WITHOUT the provenance line (it names the role, so it is never alike),
     "per_role": {role: list + the bytes of that role's own slice of the common-layer subjects},
     "errors": [why a number could not be measured]}.

    The map unreadable -> {}. A common-layer source or slice that is missing while the map names a slice of it
    is an ERROR, never a zero: an unmeasured layer must not read as an empty one (AR-28)."""
    try:
        imap = json.loads((plugin_root / "references" / "inject-map.json").read_text(encoding="utf-8"))
    except Exception:
        return {}
    listed = sum(content_bytes(plugin_root / e[len(PLUGIN_PREFIX):])
                 for e in (imap.get("common") or [])
                 if str(e).startswith(PLUGIN_PREFIX) and (plugin_root / str(e)[len(PLUGIN_PREFIX):]).exists())
    errors: list = []
    per_role: dict = {}
    shared_rules = 0
    wanted = [t for t in targets(plugin_root) if t["subject"] in COMMON_LAYER_SUBJECTS]
    for subject in COMMON_LAYER_SUBJECTS:
        if not any(t["subject"] == subject for t in wanted):
            continue
        source = plugin_root / "references" / subject
        try:
            text = source.read_text(encoding="utf-8")
        except Exception as exc:
            errors.append(f"references/{subject}: cannot be read ({type(exc).__name__}) - the common layer is not measured")
            continue
        shared_rules += len(render(subject, "", text).split("\n", 1)[1].encode("utf-8"))
    for t in wanted:
        if not t["slice"].exists():
            errors.append(f"{t['entry']}: missing - the weight of {t['role']}'s common layer is not measured "
                          "(run `python -B scripts/contract_slices.py --write`)")
            continue
        per_role[t["role"]] = per_role.get(t["role"], listed) + content_bytes(t["slice"])
    return {"list": listed, "shared": listed + shared_rules, "per_role": per_role, "errors": errors}


def report(plugin_root: Path) -> str:
    """Per role: what the map delivers now, and what the same entries would weigh unsliced."""
    try:
        imap = json.loads((plugin_root / "references" / "inject-map.json").read_text(encoding="utf-8"))
    except Exception:
        return "inject-map.json is unreadable"
    layer = common_layer(plugin_root)
    common = layer["list"]
    lines = [f"common layer: list {common:,} bytes, shared with every role {layer['shared']:,} bytes"]
    lines += [f"common layer NOT MEASURED: {why}" for why in layer["errors"]]
    lines += [f"common list (every role): {common:,} bytes",
              f"{'role':24} {'now':>8} {'unsliced':>9} {'saved':>8} {'on_demand':>10} {'would save':>11}"]
    for role, entries in sorted((imap.get("roles") or {}).items()):
        now = common
        before = common
        for entry in entries or []:
            e = str(entry)
            if not e.startswith(PLUGIN_PREFIX):
                continue
            path = plugin_root / e[len(PLUGIN_PREFIX):]
            source = (plugin_root / "references" / Path(e).name) if (e.startswith(SLICE_PREFIX)
                                                                      and keys_page_number(e) is None) else path
            now += content_bytes(path) if path.exists() else 0
            before += content_bytes(source) if source.exists() else 0
        # What `config.prompts.slices: on_demand` would deliver instead: everything that is not a
        # slice, plus the catalogue. The saving is the largest one available in a dispatch prompt,
        # and it is printed here so it is a number rather than an argument (P7.4).
        named = common
        for entry in entries or []:
            e = str(entry)
            # an inline subject (the common-layer slice, the key page and its continuations) is delivered in every mode: it
            # stays in the `on_demand` weight and is never counted as named
            if not e.startswith(PLUGIN_PREFIX) or (e.startswith(SLICE_PREFIX) and not inline_subject(e)):
                continue
            path = plugin_root / e[len(PLUGIN_PREFIX):]
            named += content_bytes(path) if path.exists() else 0
        index = catalogue_path(plugin_root, role)
        if any(str(e).startswith(SLICE_PREFIX) and not inline_subject(str(e))
               for e in entries or []) and index.exists():
            named += content_bytes(index)
        lines.append(f"{role:24} {now:8,} {before:9,} {before - now:8,} {named:10,} "
                     f"{now - named:11,}")
    return "\n".join(lines)


def dropped(plugin_root: Path, role: str, count: int = 3) -> list:
    """The largest sections this role's slices leave behind — the report of what the saving
    actually was, section by section, not as a lump of bytes."""
    out = []
    for t in targets(plugin_root):
        if t["role"] != role or not t["source"].exists():
            continue
        _, sections = parse(t["source"].read_text(encoding="utf-8"))
        for s in sections:
            if not s.wants(role):
                out.append((s.bytes(), f"{t['subject']} `{s.title}`"))
    return [f"{name} ({size:,} B)" for size, name in sorted(out, reverse=True)[:count]]


def _selftest() -> int:
    doc = ("# Subject\n\nThe lead.\n\n"
           "<!-- roles: qa-automator -->\n## Kept\n\nkept body\n\n"
           "<!-- roles: all -->\n## Shared\n\nshared body\n\n"
           "### Inherited\n\ninherited body\n\n"
           "<!-- roles: qa-runner -->\n### Split\n\nsplit body\n\n"
           "## Gone <!-- roles: qa-runner -->\n\n```\n## not a heading <!-- roles: all -->\n```\n")
    bad = 0

    def check(name: str, ok: bool, detail: str = "") -> None:
        nonlocal bad
        print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | " + detail))
        bad += 0 if ok else 1

    lead, sections = parse(doc)
    check("lead is everything before the first heading", lead.strip().endswith("The lead."), lead)
    check("a fenced line is not a heading", [s.title for s in sections].count("not a heading") == 0,
          str([s.title for s in sections]))
    automator = render("subject.md", "qa-automator", doc)
    check("the marked section is in the slice", "kept body" in automator)
    check("an `all` section is in every slice", "shared body" in automator)
    check("an unmarked `###` inherits its `##`", "inherited body" in automator)
    check("a marked `###` leaves the parent's readers", "split body" not in automator)
    check("another role's section is dropped", "Gone" not in automator)
    check("the marker itself never reaches the role", "roles:" not in automator.split("\n", 1)[1])
    check("the slice names its source", "plugin:references/subject.md" in automator.split("\n")[0])
    runner = render("subject.md", "qa-runner", doc)
    check("the split `###` goes to its own role", "split body" in runner and "kept body" not in runner)
    unnamed = render("subject.md", "qa-scout", doc)
    check("a role named on no marker still gets the `all` sections and nothing else",
          "shared body" in unnamed and "kept body" not in unnamed and "split body" not in unnamed)
    print(f"contract_slices selftest: {'ok' if not bad else str(bad) + ' failed'}")
    return 1 if bad else 0


def main() -> int:
    try:
        import console_io
        console_io.utf8_stdio()
    except ImportError:
        pass
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--plugin-root", default=str(PLUGIN_ROOT))
    args = ap.parse_args()
    root = Path(args.plugin_root).resolve()
    if args.selftest:
        return _selftest()
    if args.write:
        changed = write(root)
        for path in changed:
            print("wrote " + path.relative_to(root).as_posix())
        print(f"slices: {len(targets(root))} declared, {len(changed)} rewritten")
        for line in keys_write(root):
            print(line if line.startswith("deleted ") else "wrote " + line)
        for line in keys_warnings(root):
            print(line)
        for line in charter_write(root):
            print("wrote " + line)
        for line in catalogue_write(root):
            print("wrote " + line)
        problems = findings(root) + charter_findings(root) + catalogue_findings(root)
        for line in problems:
            print("STILL WRONG: " + line)
        return 2 if problems else 0
    if args.report:
        print(report(root))
        return 0
    problems = findings(root) + charter_findings(root) + catalogue_findings(root)
    for line in problems:
        print("SLICE: " + line)
    for line in keys_warnings(root):
        print(line)
    if not problems:
        print(f"slices: {len(targets(root))} declared, all present and fresh; "
              f"{len(keys_targets(root))} key pages; "
              f"{len(charter_targets(root))} charters carry a generated digest line")
    return 2 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
