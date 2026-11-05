"""Gate for the architecture rule: a commit touching the factory package names the AR-n invariants it
touches and how each is kept (F6-29; the rule sentence is in CLAUDE.md, the invariants in
ai-packages/qa-factory/design/architecture.md, their generated index in docs/ARCHITECTURE_INDEX.md), and --
since t-1765 node A5 -- states what it does to the judgment in the package's code (`judgment:` line, with a
cross-check of the judgment census).

Called by the commit-msg hook (.githooks/commit-msg) with the path to the commit message file.

1. No staged path starts with `ai-packages/qa-factory/` -> silent, exit 0 (nothing is read: not even the
   index). The staged paths are listed with `--no-renames -z` (as piles.staged_paths), so a rename out of or
   into the package lists BOTH paths and is a package change. A path under
   `ai-packages/qa-factory/changelog.d/` is a package path like any other: the `none` form with a reason is
   its door.
2. A package path is staged -> the message must carry at least one own line of these forms:
       architecture: AR-n[, AR-m] -- <how each is kept>
       architecture: none -- <reason the change touches no invariant>
   every id exact (`AR-`, a digit 1-9, digits: no case folding, no leading zero) and present in
   docs/ARCHITECTURE_INDEX.md read from the repository root; the text after `--` non-empty.
   A MERGE COMMIT (MERGE_HEAD exists) is exempt, exactly as tools/mechanism_gate.py exempts it: merged
   commits already passed this gate individually, and a merge's auto-message must not train toward
   --no-verify (critic t-1177, fork K-1).
3. Which lines count: the rule COPIED from tools/mechanism_gate.py (SKIP_RE / region-aware policy) -- the line
   must stand alone (^...$ per message line, indentation by spaces or tabs allowed), and a match whose own
   position sits in a FENCED block or a BLOCKQUOTE (tools/md_regions.py) counts as absent; the scan runs only
   when the message carries one of the characters "`>~". Fail-open on a scanner failure, as there (the region
   filter becomes a no-op; a missing module, an exception or degraded=True). A `# ...` comment line of git's
   template never matches (the line must START with the word). One function serves both kinds of line
   (`_prose_matches(msg, line_re=...)`).
4. Two or more such lines: EVERY counted line is judged; any bad line refuses, and the refusal names each bad
   line (one line per invariant is the natural form for a commit touching several). There is no cross-line
   rule, so a squash message carrying the branch's earlier lines passes when each is good.
5. The index file missing, or listing no `- AR-n — ` line -> refusal naming the generator (never a silent
   pass). The staged paths cannot be listed, or the message file cannot be read -> exit 1.
6. The `judgment:` line (t-1765 2.4). A package commit also carries at least one own line of
       judgment: none -- <why the change moves no judgment>
       judgment: adds data check <unit> -- <why this is a data check or a guard, not judgment>
       judgment: moves <what> to role -- <why>
       judgment: moves <what> to code -- <why>
   a `moves` without `to role|to code`, an `adds data check` without `<unit>`, or any form with empty text after
   `--` is refused with the forms. Every counted line is judged for its form.
7. The census cross-check. The ceilings of the judgment census (CENSUS_REL, object `ratchet`) are compared
   between the HEAD blob and the index blob; both come in as ARGUMENTS of decide() (main() reads them with
   `git show HEAD:<P>` and `git show :<P>`; an ABSENT blob is None, a blob git FAILED to give is an Unread and refuses naming "could not be
   read", whatever the `judgment:` line says -- AR-28). Worlds:
     (i)   neither has the census            -> silent (the form of the line is still required);
     (ii)  none in HEAD (or HEAD unreadable), present in the index -> creation is not a raise; an unreadable
           HEAD adds a WARN "census in HEAD unreadable; treated as absent (world ii): the index census becomes
           the base";
     (iii) in HEAD, gone from the index      -> only `moves <what> to code` passes ("census deleted by this commit");
     (iv)  equal                             -> silent;
     (v)   differ: a raise of word-list|meaning-proxy|meaning|breach|blocks_overrides (or of any key this gate
           does not know) needs `moves <what> to code`; a raise only of blocking_per_role.* and/or safety needs
           `adds data check` or `moves <what> to code`. A raise is a ceiling whose integer grew, or a NEW key
           above 0; a new key at 0 and a vanished key are not raises.
   An index blob that is not JSON, has no `ratchet` object, or holds a ceiling that is not an integer >= 0 is
   refused naming the file path, whatever the `judgment:` line says (AR-28).
8. Position inside decide() (t-1765 E-A12): no package path -> `0, ""` before any read; the merge exemption stays
   in main(), before the message is read, common to both lines; the problems of `architecture:` and of
   `judgment:` are collected INDEPENDENTLY, and any problem of either kind gives ONE refusal naming all of them
   with both forms (a missing index never leaves `judgment:` unchecked; an unreadable census never removes an
   `architecture:` refusal).

The refusal says what is wrong, what is expected (the line forms, the ids known) and the door (FR-1, FR-57):
the `none` forms with a reason are open unless the census ceilings rose, and then the refusal names the form that
is; the gate never asks for a tool or a path the committer cannot use. It judges the form of a line and the growth
of numbers, not whether a `none` is true (calibration 41 and the critic's question 11 do).
Exit codes: 0 pass (or not a package commit), 1 refusal. Detector of the mechanism's own failure: a calibration
check counting `architecture: none` lines on package commits against findings of the breakage class.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

import gitcmd

try:
    from md_regions import scan, KIND_FENCED, KIND_BLOCKQUOTE
except ImportError:                       # the region filter becomes a no-op, as in mechanism_gate
    scan = None
    KIND_FENCED, KIND_BLOCKQUOTE = "fenced", "blockquote"

PACKAGE_PREFIX = "ai-packages/qa-factory/"
INDEX_REL = "docs/ARCHITECTURE_INDEX.md"
GENERATOR = "python tools/architecture_index.py"
CENSUS_REL = "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json"

LINE_RE = re.compile(r"^[ \t]*architecture[ \t]*:(.*)$", re.IGNORECASE | re.MULTILINE)
JUDGMENT_RE = re.compile(r"^[ \t]*judgment[ \t]*:(.*)$", re.IGNORECASE | re.MULTILINE)
ID_RE = re.compile(r"AR-[1-9]\d*")
# The twin of architecture_index.render()'s "- AR-%d — %s"; test_architecture_gate pins the pair.
INDEX_ID_RE = re.compile(r"^- (AR-[1-9]\d*) — ", re.MULTILINE)
ADDS_RE = re.compile(r"adds data check[ \t]+(\S.*)")
MOVES_RE = re.compile(r"moves[ \t]+(\S.*?)[ \t]+to[ \t]+(role|code)")
EXCLUDED_KINDS = (KIND_FENCED, KIND_BLOCKQUOTE)
MARKER_CHARS = ("`", ">", "~")
SHOWN_PATHS = 5
# Ceilings that also grow from an honest data check: `adds data check` answers their raise too. Every other
# raised key (the five named in the docstring, and any key this gate does not know) needs `moves ... to code`.
WEAK_KEYS = ("safety",)
WEAK_PREFIXES = ("blocking_per_role.", "safety.")


def package_paths(staged):
    return [p for p in staged if p.startswith(PACKAGE_PREFIX)]


def known_ids(index_text):
    """The AR-n ids of the index, in file order."""
    return INDEX_ID_RE.findall(index_text)


def _prose_matches(msg, line_re=LINE_RE):
    """The `line_re` matches whose own position is prose (docstring item 3)."""
    matches = list(line_re.finditer(msg))
    if not matches or scan is None or not any(ch in msg for ch in MARKER_CHARS):
        return matches
    try:
        result = scan(msg)
    except Exception:
        return matches
    if result.degraded:
        return matches

    def in_prose(offset):
        for region in result.regions:
            if region.start <= offset < region.end:
                return not any(kind in EXCLUDED_KINDS for kind in region.kinds)
        return True

    return [m for m in matches if in_prose(m.start())]


def declared_lines(msg):
    """The text after `architecture:` of every counted line, in message order, stripped."""
    return [m.group(1).strip() for m in _prose_matches(msg)]


def judgment_lines(msg):
    """The text after `judgment:` of every counted line, in message order, stripped."""
    return [m.group(1).strip() for m in _prose_matches(msg, JUDGMENT_RE)]


def _forms(ids):
    shown = ", ".join(ids) if ids else "(none found)"
    return ("Expected, as its own line of the commit message (a line inside a fenced block or a quote is not read):\n"
            "  architecture: AR-n[, AR-m] -- <how each is kept>      ids known: " + shown + "\n"
            "  architecture: none -- <reason the change touches no invariant>\n"
            "Door: the `none` form with a reason is always open; the invariants are described in "
            "ai-packages/qa-factory/design/architecture.md, and `none` is counted at calibration against the "
            "breakage findings, so say why.")


def _judgment_forms():
    return ("Expected, as its own line of the commit message (a line inside a fenced block or a quote is not read):\n"
            "  judgment: none -- <why the change moves no judgment>\n"
            "  judgment: adds data check <unit> -- <why this is a data check or a guard, not judgment>\n"
            "  judgment: moves <what> to role -- <why>\n"
            "  judgment: moves <what> to code -- <why>\n"
            "Door: `judgment: none -- <reason>` is open, unless the census ceilings rose in this commit; then the "
            "refusal above names the form that is open (`moves <what> to code`, and for a data check "
            "`adds data check <unit>`).")


def _problem(line, ids):
    """None when the declared text is acceptable, else what is wrong with it."""
    head, sep, how = line.partition("--")
    head, how = head.strip(), how.strip()
    if not sep:
        return "the line `architecture: %s` has no ` -- <how each is kept>` part" % line
    if head == "none":
        return None if how else "`architecture: none --` carries no reason after the dashes"
    tokens = [t.strip() for t in head.split(",")]
    bad = [t for t in tokens if not ID_RE.fullmatch(t)]
    if bad:
        return ("not an invariant id: %s (an id is `AR-` and digits, case exact; `none` stands alone)"
                % ", ".join("`%s`" % t for t in bad))
    unknown = [t for t in tokens if t not in ids]
    if unknown:
        return "unknown invariant id(s): %s (not in %s)" % (", ".join(unknown), INDEX_REL)
    if not how:
        return "`architecture: %s --` carries no text on how each is kept" % head
    return None


def judgment_form(line):
    """(form, problem): form is 'none' | 'adds' | 'moves-role' | 'moves-code' for an acceptable line, else None
    with what is wrong."""
    head, sep, why = line.partition("--")
    head, why = " ".join(head.split()), why.strip()
    if not sep:
        return None, "the line `judgment: %s` has no ` -- <why>` part" % line
    if head == "none":
        return ("none", None) if why else (None, "`judgment: none --` carries no reason after the dashes")
    m = ADDS_RE.fullmatch(head)
    if head.startswith("adds data check") and not m:
        return None, "`judgment: adds data check` names no <unit> (expected `adds data check <unit> -- <why>`)"
    if m:
        return ("adds", None) if why else (None, "`judgment: %s --` carries no text after the dashes" % head)
    m = MOVES_RE.fullmatch(head)
    if m:
        form = "moves-" + m.group(2)
        return (form, None) if why else (None, "`judgment: %s --` carries no text after the dashes" % head)
    if head.startswith("moves"):
        return None, "`judgment: %s` is not `moves <what> to role` or `moves <what> to code`" % head
    return None, "`judgment: %s` is none of the four forms" % head


# ---- the census cross-check ---------------------------------------------------------------------------------

def _flat_ceilings(blob):
    """(dict dotted-key -> int, None) for a readable census blob, else (None, what is wrong)."""
    try:
        data = json.loads(blob)
    except (ValueError, TypeError):
        return None, "is not JSON"
    ratchet = data.get("ratchet") if isinstance(data, dict) else None
    if not isinstance(ratchet, dict):
        return None, "has no `ratchet` object"
    flat = {}

    def walk(prefix, node):
        for key, value in node.items():
            name = prefix + str(key)
            if isinstance(value, dict):
                walk(name + ".", value)
            elif isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                flat[name] = value
            else:
                raise ValueError("ceiling `%s` is not an integer >= 0" % name)

    try:
        walk("", ratchet)
    except ValueError as exc:
        return None, str(exc)
    return flat, None


def _is_weak(key):
    return key in WEAK_KEYS or key.startswith(WEAK_PREFIXES)


def census_state(head_blob, index_blob):
    """(problems, need, need_text, warns). problems: refusals that no `judgment:` line answers. need: None,
    'data' (adds data check or moves to code) or 'code' (moves to code only); need_text says why."""
    problems, warns = [], []
    for where, blob in (("HEAD", head_blob), ("the index", index_blob)):
        if isinstance(blob, Unread):                               # AR-28: an unread census is never world (ii)
            problems.append("census in %s could not be read: %s -- the gate cannot compare the ceilings, and an "
                            "unknown is not a pass; fix the git problem named and commit again" % (where, blob.reason))
    if problems:
        return problems, None, "", warns
    if index_blob is None:
        if head_blob is None:
            return problems, None, "", warns                       # world (i)
        return problems, "code", ("the census (%s) is deleted by this commit -- census deleted by this commit "
                                  "counts as every ceiling raised to unknown" % CENSUS_REL), warns   # world (iii)
    new, why = _flat_ceilings(index_blob)
    if new is None:
        problems.append("the census in the index (%s) %s -- expected a JSON object with a `ratchet` object of "
                        "integer ceilings >= 0 at %s; the gate cannot compare the ceilings, and an unknown is not a "
                        "pass. Door: fix the file (or restore it from HEAD) and stage it again"
                        % (CENSUS_REL, why, CENSUS_REL))
        return problems, None, "", warns
    if head_blob is None:
        return problems, None, "", warns                           # world (ii): creation is not a raise
    old, _why = _flat_ceilings(head_blob)
    if old is None:
        warns.append("census in HEAD unreadable; treated as absent (world ii): the index census becomes the base")
        return problems, None, "", warns                           # world (ii) with a broken HEAD
    raised = []
    for key in sorted(new):
        if key in old:
            if new[key] > old[key]:
                raised.append((key, str(old[key]), new[key]))
        elif new[key] > 0:
            raised.append((key, "(new)", new[key]))
    if not raised:
        return problems, None, "", warns                           # world (iv), or no raise in (v)
    need = "code" if any(not _is_weak(r[0]) for r in raised) else "data"
    naming = ", ".join("%s %s → %d" % r for r in raised)
    return problems, need, "the census ceilings rose in this commit: %s" % naming, warns


def _judgment_problems(msg, head_blob, index_blob):
    """(census_problems, problems, warns) of the `judgment:` side, independent of the `architecture:` side.
    census_problems are answered by no `judgment:` line (they carry their own door and show no line forms)."""
    census_problems, need, need_text, warns = census_state(head_blob, index_blob)
    problems = []
    lines = judgment_lines(msg)
    forms = []
    if not lines:
        problems.append("Its message carries no `judgment:` line.")
    else:
        judged = [(line,) + judgment_form(line) for line in lines]
        wrong = [(line, why) for line, _form, why in judged if why]
        forms = [form for _line, form, why in judged if not why]
        if wrong:
            named = "\n".join("  `judgment: %s` -- %s" % item for item in wrong)
            problems.append("The `judgment:` line is wrong (%d of %d judged):\n%s" % (len(wrong), len(lines), named))
    if need == "code" and "moves-code" not in forms:
        problems.append("%s; only `judgment: moves <what> to code -- <why>` answers that (not `none`, not "
                        "`adds data check`, not `moves ... to role`)." % need_text)
    elif need == "data" and not ({"adds", "moves-code"} & set(forms)):
        problems.append("%s; `judgment: none` does not answer that -- name `judgment: adds data check <unit> -- "
                        "<why>` if it is a data check, or `judgment: moves <what> to code -- <why>`." % need_text)
    return census_problems, problems, warns


def _architecture_problems(msg, ids, index_text):
    if not ids:
        return ["%s is %s -- fail-closed. Generate it with `%s` and stage it."
                % (INDEX_REL, "missing" if index_text is None else "listing no `- AR-n — ` line", GENERATOR)]
    lines = declared_lines(msg)
    if not lines:
        return ["Its message carries no `architecture:` line."]
    wrong = [(line, why) for line in lines for why in [_problem(line, ids)] if why]
    if not wrong:
        return []
    named = "\n".join("  `architecture: %s` -- %s" % item for item in wrong)
    return ["The `architecture:` line is wrong (%d of %d judged):\n%s" % (len(wrong), len(lines), named)]


def decide(msg, staged, index_text, head_blob=None, index_blob=None):
    """Pure decision: (exit code, text for stderr -- refusal and/or WARN lines, '' when silent).
    index_text is None when the index file is absent; head_blob / index_blob are the census text in HEAD and in
    the index (None when absent)."""
    hits = package_paths(staged)
    if not hits:
        return 0, ""
    ids = known_ids(index_text) if index_text is not None else []
    arch = _architecture_problems(msg, ids, index_text)
    broken, judg, warns = _judgment_problems(msg, head_blob, index_blob)
    warn_text = "".join("architecture_gate: WARN: %s\n" % w for w in warns)
    if not arch and not judg and not broken:
        return 0, warn_text
    shown = hits[:SHOWN_PATHS]
    touched = "commit touches the package:\n  " + "\n  ".join(shown) + (
        "\n  ... and %d more" % (len(hits) - len(shown)) if len(hits) > len(shown) else "")
    parts = ["architecture_gate: %s" % touched]
    if arch:
        parts.append("\n".join(arch))
        parts.append(_forms(ids))
    if broken:
        parts.append("\n".join(broken))          # no `judgment:` line answers these: no line forms, no `none` door
    if judg:
        parts.append("\n".join(judg))
        parts.append(_judgment_forms())
    return 1, warn_text + "\n".join(parts)


class Unread:
    """A census blob git failed to give (not an absent one): carries the first line of git's reason."""

    def __init__(self, reason):
        self.reason = reason


ABSENT_MARKERS = ("does not exist in", "exists on disk, but not in", "fatal: path")


def _show(spec):
    """The text of `git show <spec>`: None when there is no such blob (git exit 128 naming the path, or an unborn
    HEAD), an Unread when git failed otherwise (timeout, exit -1, any other non-zero) -- AR-28."""
    code, raw, err = gitcmd.git(None, "show", spec, stderr=True)
    if code == 0:
        return raw.decode("utf-8-sig", "replace")
    reason = gitcmd.as_text(err).strip().split("\n")[0] if err else ""
    if code == 128 and any(m in reason for m in ABSENT_MARKERS):
        return None
    if spec.startswith("HEAD:"):                  # the first commit: no HEAD, so no census in it
        vcode, _vraw = gitcmd.git(None, "rev-parse", "--verify", "-q", "HEAD")
        if vcode == 1:
            return None
    return Unread(reason or "git show %s exited %d" % (spec, code))


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):      # the refusal quotes the committer's own text (a dash, a quote)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("architecture_gate: need a path to the commit message file", file=sys.stderr)
        return 1
    code, raw = gitcmd.git(None, "diff", "--cached", "--name-only", "--no-renames", "-z")   # as piles.staged_paths
    if code != 0:
        print("architecture_gate: cannot list the staged paths (git exit %d) -- fail-closed; run it inside "
              "the repository, from a commit-msg hook" % code, file=sys.stderr)
        return 1
    staged = [p for p in raw.decode("utf-8", "replace").split("\0") if p]
    if not package_paths(staged):
        return 0
    # TWIN of tools/mechanism_gate.py main(): a merge commit (MERGE_HEAD exists) is exempt (K-1). A failed
    # lookup leaves `merging` False, so the commit is gated (fail-closed). Common to both kinds of line.
    code, raw = gitcmd.git(None, "rev-parse", "--git-path", "MERGE_HEAD")
    merge_head = gitcmd.as_text(raw).strip() if code == 0 else ""
    if merge_head and pathlib.Path(merge_head).exists():
        return 0
    try:
        msg = pathlib.Path(argv[0]).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print("architecture_gate: cannot read the commit message file %s: %s" % (argv[0], exc), file=sys.stderr)
        return 1
    code, raw = gitcmd.git(None, "rev-parse", "--show-toplevel")
    root = pathlib.Path(gitcmd.as_text(raw).strip()) if code == 0 and raw.strip() else pathlib.Path.cwd()
    index = root / INDEX_REL
    index_text = index.read_text(encoding="utf-8", errors="replace") if index.is_file() else None
    head_blob, index_blob = _show("HEAD:" + CENSUS_REL), _show(":" + CENSUS_REL)
    code, text = decide(msg, staged, index_text, head_blob, index_blob)
    if text:
        print(text.rstrip("\n"), file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
