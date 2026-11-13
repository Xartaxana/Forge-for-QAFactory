"""Gate for rule 10(b): a commit touching mechanism files must carry an
axis block.

Called by the commit-msg hook (.githooks/commit-msg) with the path to
the commit message file. Logic (entirely in a pure decide(), testable
without git):

1. Staged paths don't touch any mechanism prefix -> the gate is silent.
2. A merge commit (MERGE_HEAD exists) -> the gate is silent: merged
   commits already passed this gate individually; blocking the merge's
   auto-message would be a false positive that trains toward
   --no-verify.
3. Skip line "axes: not a mechanism (<reason>)" (this template's
   English phrasing, CLAUDE.md rule 10) works ONLY from the commit
   message -- a written statement by the committer, the same pattern
   as `dispatch_skipped`. Not looked up in the diff: decision text that
   quotes the skip syntax would otherwise bypass the gate. Inside the
   message itself the line counts ONLY as its OWN separate line
   (^...$ anchor with MULTILINE, indentation by spaces allowed) --
   otherwise an inline quote of the skip syntax in the middle of the
   message's prose would silence the whole gate (a finding from a
   sibling deployment's own commit-message review); the same anchor
   already used by TIER_LINE_RE below.
4. Axis block -- lines "axis N: <verdict>" for EVERY axis of the
   current docs/SIBLING_MAP.md -- looked up in the commit message PLUS
   in the staged diff of ONE file, DECISIONS.md (this template ships a
   single decisions file; the source deployment's two-file split
   (DECISIONS.md summary + docs/DECISIONS_FULL.md detail) collapses to
   just DECISIONS.md here -- template dependency, toolkit transfer).
   The whole diff is not scanned: unrelated staged content with a
   literal "axis N:" would close axes fictitiously. Axis count and
   numbers are read from the map on every run -- the map grows and
   changes, the gate follows it.
4a. Axis LABELS (forge/5 F5-6, t-773; the finding "the axis block is checked
   against the map by number only"): every "## Axis N <dash|colon> <title>"
   heading defines the axis KEY -- the title cut at its FIRST colon (a colon
   inside quotes counts: the cut is textual), normalised: lower-case,
   whitespace collapsed, em/en dashes and hyphen runs read as one hyphen,
   quotes and backticks stripped; a title with no colon is the whole key --
   and its SHORT form, the first three words of that key (t-783, F1: the
   map's "name: description" titles would otherwise put the colon or a
   volatile count into the key). A message line carries the key
   before the verdict word: "axis N (<key>): covered / queued / n/a <why>" or
   "axis N -- <key>: ...". A label CONTAINING the short key of axis N is
   accepted; any other label is REFUSED (the refusal prints the real heading
   and the accepted forms; a label that is the key of ANOTHER axis is named
   as that axis's), and there is NO door for a wrong label -- "axes: not a
   mechanism (<reason>)" stays the only waiver. A line with no label
   ("axis N: n/a", the form of every block until now) is accepted before
   LABEL_REQUIRED_FROM (2026-10-16 00:00, the clock read through _now()) and
   refused from then on. A heading with no title has no key (nothing to
   compare). Two headings of one number: refused, both named. Labels in a
   fenced/quoted region of the message are not read (the label layer is
   region-aware, unlike the legacy "axis N:" counting of find_missing()). The
   calibration reader is `python tools/mechanism_gate.py --audit --since
   <date>` (audit_labels()): per mechanism commit of the window, every axis
   line whose label mismatches the current map. Detector of the mechanism's
   own failure: that audit, named in calibration check 8.
5. The map can't be read / has zero axes -> fail-closed (a silent skip
   of the check is indistinguishable from passing it).
6. Net: known homes of mechanisms in this template (CLAUDE.md,
   DECISIONS.md, docs/SIBLING_MAP.md, PROCESS/, .claude/agents/,
   .claude/skills/, BOOT.md) plus self-protection of the enforcement
   chain itself -- NAMED, one entry per script this template's OWN
   live wiring (.claude/settings.json's hook commands, .githooks/
   pre-commit and commit-msg) actually points at: this file, the
   SessionStart hook (tools/session_context.py), the PreToolUse
   Task|Agent hooks (tools/dispatch_gate.py, tools/critic_snapshot.py),
   the PreToolUse Bash|PowerShell hook (tools/hygiene_gate.py), the
   PostToolUse hooks (tools/dod_track.py, tools/journal_echo.py), the
   SubagentStop hook (tools/dod_gate.py), the Stop hook
   (tools/main_gate.py), the pre-commit hook's own scripts
   (tools/journal_validator.py, tools/escape_check.py,
   tools/enforcement_probe.py), plus .githooks/ and
   .claude/settings.json themselves (editing the gate or the hook
   registration must not bypass the gate). TRANSITIVE closure: a
   script named directly by the wiring can itself import another
   tools/*.py module that is NOT a hook command in its own right but
   whose failure/corruption still changes what the wired hook does --
   this template's tools/session_context.py imports
   tools/preflight_quota.py and (locally, inside a function) tools/
   wiring_check.py, and tools/journal_echo.py imports tools/
   journal_validator.py (already named above) and tools/tier_echo.py --
   all three reached-but-not-directly-named modules are in the net too,
   found and verified by the self-closing AST-import-closure test
   below (test_transitive_import_closure_of_live_wiring_is_covered_by_
   mechanism_prefixes), not by hand-transcription. Wide directories
   (tools/, gateway/) are deliberately outside the net as a category --
   false positives there train toward --no-verify (the same tradeoff a
   sibling deployment's own version of this gate already records) --
   but every module the wiring ACTUALLY reaches, named or transitive,
   is named individually.
7. Tier declaration: on the "mechanism" branch (axis block already
   satisfied), the commit message must carry a SEPARATE line
   "tier: <value>" -- a self-declaration of the committer's actual
   tier, the same pattern as `dispatch_skipped`. Expected value: the
   model bound to roles.lead in this template's own
   delegation.config.yaml, resolved relative to REPO (this template's
   install root, next to this gate) -- not the caller's cwd. No file,
   or no roles.lead key -> default to the "fable" family (the
   subscription-contour default for Lead). A declaration is accepted
   on an exact match with the bound model, OR by containing its tier
   family (fable/opus/sonnet/haiku, matched as a substring) -- a
   non-Claude binding has no family, so only an exact model-id match
   qualifies for it. The skip branch ("not a mechanism") and merge
   commits do not require a tier line (same exemption net as the axis
   block). The gate does NOT verify the declaration is true --
   two-layer enforcement: code guarantees the line's presence and
   shape, truth is judged by calibration against transcripts, a tier
   above.

REGION-AWARE SKIP_RE/TIER_LINE_RE (ported from the HQ mirror's own
region-aware gate; toolkit's own md_regions scanner, already landed
standalone -- see toolkit/tools/md_regions.py). Residual gap this
closes: rules 3 and 7 above already anchor SKIP_RE/TIER_LINE_RE to
their OWN separate line (^...$/MULTILINE) against an inline quote
mid-prose -- but that anchor alone does not know whether the WHOLE
line sits inside a fenced code block or a blockquote (both still look
like "a standalone line" to ^...$/MULTILINE). Example: a commit
message that QUOTES the skip syntax as a whole line inside a triple-
backtick example (a natural shape for documentation/PR text showing
the reader "this is what a skip looks like") used to silence the gate
entirely -- a false pass of the axis-block rule.

POLICY: a SKIP_RE or TIER_LINE_RE match whose OWN position sits in a
FENCED or BLOCKQUOTE region does NOT count (filtered out before it
reaches decide()/decide_full()'s verdict). This makes the gate
STRICTER, not looser -- a quoted/fenced skip or tier line that used to
pass now needs a real, unquoted declaration instead; the gate stays
fail-closed throughout.

ALL-MUST-PASS COUNTS ONLY UNQUOTED TIER LINES: a new function,
_region_filtered_tier_declarations(), returns only the values of
TIER_LINE_RE matches sitting in PROSE; decide_full()'s existing
"every found line must pass" semantics applies to THIS filtered list.
find_tier_declarations() (public) is untouched -- region-blind,
byte for byte (kept for direct callers/back-compat, same as
find_missing() below).

THE LEGACY AXIS COUNT IS NOT FILTERED -- A DELIBERATE NON-GOAL, not a
missed symmetry: find_missing() stays byte for byte, region is never
passed to it (before 2026-10-16 an unlabelled "axis N:" inside a fence
still counts). The LABEL layer (item 4a, parse_axis_lines) IS
region-aware: a labelled line inside a fence or a quote closes nothing
and refuses nothing.

block_extra IS NEVER REGION-SCANNED: scan() runs only on `msg`, never
on `block_extra` (the diff text of DECISIONS.md) -- a unified diff has
no markdown "fence/quote" semantics in the sense this scanner parses;
scanning it would be a category error. block_extra keeps its existing
role in find_missing(msg + "\n" + block_extra, axes) only.

BRANCH ORDER UNCHANGED: hits -> merging -> skip -> fail-closed
(map/axes) -> (decide_full) tier -- no branch added, removed, or
reordered; only WHAT COUNTS as a SKIP_RE/TIER_LINE_RE match changes.

LAZINESS (Rule #1): scan(msg) runs AT MOST ONCE per decide()/
decide_full() call (one shared _maybe_scan(), reused by both the skip
check and, inside decide_full(), the tier check too) -- and only when
(a) the commit actually touches a mechanism path and isn't a merge
(every other commit -> zero scan calls, the hits/merging branches
return before _maybe_scan is even reached), (b) the message carries a
cheap marker hint (the literal "axes", "axis" or "tier", case-insensitive),
AND (c) the message carries at least one of "`>~" (without them,
md_regions.scan() would deterministically say "all prose" anyway --
the call would be wasted).

FAIL-OPEN ON SCANNER FAILURE (ANY of: module missing / scan()
raises / degraded=True): the region filter becomes a no-op --
SKIP_RE.search(msg) and find_tier_declarations(msg) (the region-blind
forms) give EXACTLY the answers the pre-region gate gave. Concretely:
if only a QUOTED skip line exists, this fallback reverts THIS FILE to
the PRE-region behavior for that one message -- the gate silences
again on the quoted example (the same residual gap the pre-region
gate always had) -- not a new code path, the same cycle with the
region branch gone dead (the same posture as owns_gate.py/
negative_lint.py's own scanner fallbacks).
"""
from __future__ import annotations

import bisect
import datetime
import re
import subprocess
import sys
from pathlib import Path

import yaml

try:
    from tools.md_regions import scan, KIND_FENCED, KIND_BLOCKQUOTE  # package-style
except ImportError:
    try:
        from md_regions import scan, KIND_FENCED, KIND_BLOCKQUOTE  # sibling-module fallback
    except ImportError:
        scan = None
        KIND_FENCED = "fenced"
        KIND_BLOCKQUOTE = "blockquote"

REPO = Path(__file__).resolve().parents[1]
MAP_PATH = REPO / "docs" / "SIBLING_MAP.md"
# Template dependency (toolkit transfer): this template has ONE decisions
# file, DECISIONS.md -- not the source deployment's docs/DECISIONS_FULL.md.
DECISIONS_FULL = "DECISIONS.md"
# This template's install root, next to this gate -- not the caller's cwd.
CONFIG_PATH = REPO / "delegation.config.yaml"

LEAD_FAMILIES = ("fable", "opus", "sonnet", "haiku")
TIER_LINE_RE = re.compile(r"^\s*tier\s*:\s*(\S.*?)\s*$", re.IGNORECASE | re.MULTILINE)

MECHANISM_PREFIXES = (
    "CLAUDE.md",
    "DECISIONS.md",
    "docs/SIBLING_MAP.md",
    "PROCESS/",
    ".claude/agents/",
    ".claude/skills/",
    "BOOT.md",
    "tools/mechanism_gate.py",
    ".githooks/",
    # SessionStart hook duties are future-session obligations too.
    "tools/session_context.py",
    ".claude/settings.json",
    # Named net, not a directory (point 6 above): every tools/*.py this
    # template's OWN .claude/settings.json / .githooks/ actually wires
    # in -- verified live by test_every_live_settings_hook_command_is_
    # covered_by_mechanism_prefixes / test_every_githooks_script_
    # reference_is_covered_by_mechanism_prefixes in the test twin. Wide
    # directories (tools/, gateway/) stay outside the net as a category
    # (point 6) -- naming is per-file, not per-directory.
    "tools/agent_budget.py",        # PreToolUse hook on every tool (the cost gates, D-0035)
    "tools/dispatch_gate.py",       # PreToolUse Task|Agent hook
    "tools/critic_snapshot.py",     # PreToolUse Task|Agent hook
    "tools/owns_gate.py",           # PreToolUse Task|Agent hook
    "tools/hygiene_gate.py",        # PreToolUse Bash|PowerShell hook
    "tools/claim_control_gate.py",  # PreToolUse Edit|Write hook
    "tools/handoff_gate.py",        # PreToolUse Edit|Write hook (forge/5 F5-1 N3: a reading worker writes only its handoff: path)
    "tools/dod_track.py",           # PostToolUse hook
    "tools/journal_echo.py",        # PostToolUse hook
    "tools/search_control_gate.py", # PostToolUse Bash|PowerShell|Grep|Glob|Read hook
    "tools/negative_lint.py",       # PostToolUse Task|Agent hook
    "tools/dod_gate.py",            # SubagentStop hook
    "tools/main_gate.py",           # Stop hook
    "tools/journal_validator.py",   # .githooks/pre-commit
    "tools/journal_keys.py",        # imported by journal_validator / session_context / forge_metrics (B-402)
    "tools/dev_config.py",          # imported by tools/journal_keys.py (the developer slug, F0-4/F0-6)
    "tools/escape_check.py",        # .githooks/pre-commit
    "tools/enforcement_probe.py",   # .githooks/pre-commit
    "tools/factory_rules_index.py", # .githooks/pre-commit (project layer: FR index)
    "tools/architecture_gate.py",   # .githooks/commit-msg (architecture gate, F6-29)
    "tools/architecture_index.py",  # .githooks/pre-commit (architecture index, F6-29)
    "tools/compact_snapshot.py",    # PreCompact hook (0b20099)
    "tools/forge_metrics.py",       # .githooks/pre-merge-commit (Forge attribution, 6ba43b6)
    "tools/piles.py",               # .githooks/pre-commit + commit-msg + pre-merge-commit (piles check, F0-2)
    "tools/gitcmd.py",              # the one git runner imported by piles.py, compact_snapshot.py, forge_metrics.py (t-601)
    "tools/piles_split.py",         # the one-shot `split` that fills plans/piles from the backlog (F0-2b)
    # Transitive closure (point 6): reached by AST import from an
    # already-named module above, not itself a direct hook command --
    # test_transitive_import_closure_of_live_wiring_is_covered_by_
    # mechanism_prefixes is the machine check that this list stays
    # complete against that closure as the wiring drifts.
    "tools/tier_echo.py",           # imported by tools/journal_echo.py
    "tools/ci_read.py",             # imported by tools/test_quarantine.py, which session_context.py imports (the quarantine line of SessionStart, TD-15)
    "tools/ci_read_common.py",      # imported by tools/ci_read.py
    "tools/preflight_quota.py",     # imported by tools/session_context.py
    "tools/test_quarantine.py",     # imported by tools/session_context.py (the TEST QUARANTINE line, TD-15.7)
    "tools/wiring_check.py",        # imported by tools/session_context.py
    "tools/md_regions.py",          # imported by THIS file (region scanner)
    "tools/md_table.py",            # imported by tools/piles.py (the table reader, t-797 F5-2 N3) - live wiring closure
    "tools/dispatch_manifest.py",   # imported by tools/dispatch_gate.py (completeness check)
    "tools/transcripts.py",         # imported by dispatch_gate, journal_echo, tier_echo, agent_budget (B-467, F2-11)
    "tools/agents_md.py",           # run by .githooks/pre-commit (AGENTS.md --check)
    "tools/worktree_sweep.py",      # run by .githooks/post-merge (F6-38; self-activating, placed by the Lead) and imported by session_context.py / piles.py
    "tools/worktree-junk.json",     # DATA that decides what worktree_sweep.py deletes (untracked traces, protected branches): an edit widens the deletion set
)

# Template dependency (toolkit transfer, empirically verified against
# toolkit/docs/SIBLING_MAP.md and toolkit/CLAUDE.md rule 10): this
# template's map headings and its axis-answer/skip-line vocabulary are
# English ("## Axis N", "axis N: covered", "axes: not a mechanism
# (<reason>)") -- the source deployment's original regexes matched on
# its own non-English heading text and silently matched zero axes
# against this template's own map (fail-closed on every mechanism
# commit); ported as English to match the artifact these regexes
# actually run against.
# Line anchor: without ^...$/
# MULTILINE the phrase matched via .search() ANYWHERE in the message --
# an inline quote of the skip syntax in the middle of prose ("...the
# line \"axes: not a mechanism (example)\" would bypass...") silenced
# the whole gate. Symmetric with the already-anchored TIER_LINE_RE.
SKIP_RE = re.compile(r"^\s*axes\s*:\s*not\s+a\s+mechanism\s*\(", re.IGNORECASE | re.MULTILINE)

# --- region predicate (see module docstring, "REGION-AWARE SKIP_RE/
# TIER_LINE_RE") ---------------------------------------------------------

# Fail-closed asymmetry (see the docstring section "POLICY"): only
# FENCED and BLOCKQUOTE exclude a SKIP_RE/TIER_LINE_RE match --
# inline_code is not imported at all: a backtick (opening or a lone
# one mid-word) cannot structurally sit at the position where
# ^\s*(axes|tier) expects literal text with no leading backtick, so
# KIND_INLINE_CODE is structurally inapplicable to these two
# whole-line-anchored regexes.
_EXCLUDED_KINDS = ("fenced", "blockquote")

_REGION_MARKER_CHARS = ("`", ">", "~")
_MARKER_HINT_RE = re.compile(r"axes|axis|tier", re.IGNORECASE)


def _has_region_marker_chars(text: str) -> bool:
    return any(ch in text for ch in _REGION_MARKER_CHARS)


def _safe_scan(text: str):
    """Fail-open on scanner failure: None on a missing module / an
    exception from scan() / degraded=True -- the region filter becomes
    a no-op (see the docstring section "FAIL-OPEN ON SCANNER
    FAILURE")."""
    if scan is None:
        return None
    try:
        result = scan(text)
    except Exception:
        return None
    if result.degraded:
        return None
    return result


def _region_at(scan_result, offset: int):
    regions = scan_result.regions
    if not regions:
        return None
    starts = [r.start for r in regions]
    idx = bisect.bisect_right(starts, offset) - 1
    if idx < 0:
        return None
    region = regions[idx]
    if region.start <= offset < region.end:
        return region
    return None


def _classify(region) -> str:
    """See the docstring section "POLICY": fenced (including an
    unterminated fence -- no priority rule "unterminated -> prose",
    the same fail-closed choice as elsewhere: the content of an
    ambiguously-closed fence does NOT get "prose" status) > blockquote
    > prose."""
    if region is None:
        return "prose"
    if KIND_FENCED in region.kinds:
        return "fenced"
    if KIND_BLOCKQUOTE in region.kinds:
        return "blockquote"
    return "prose"


def _is_prose_position(scan_result, offset: int) -> bool:
    if scan_result is None:
        return True  # fail-open: no-op
    return _classify(_region_at(scan_result, offset)) not in _EXCLUDED_KINDS


def parse_axes(map_text: str) -> list[int]:
    """Axis numbers from the map's headings; order and gaps in the
    numbering don't matter. Derived from axis_headings(): ONE heading reader."""
    return [h["number"] for h in axis_headings(map_text)]


def _matches(path: str, pref: str) -> bool:
    # Prefix boundary: directories match by startswith, files match
    # exactly (CLAUDE.md.bak is not a mechanism path).
    if pref.endswith("/"):
        return path.startswith(pref)
    return path == pref


def mechanism_paths(staged: list[str]) -> list[str]:
    return [p for p in staged
            if any(_matches(p, pref) for pref in MECHANISM_PREFIXES)]


def find_missing(text: str, axes: list[int]) -> list[int]:
    # Deliberate non-goal (see the docstring section "AXIS LINES ARE NOT
    # FILTERED"): byte for byte, region is never passed here.
    return [n for n in axes
            if not re.search(rf"axis\s+{n}\s*:", text, re.IGNORECASE)]


# --- axis LABELS (forge/5 F5-6, t-773; see the docstring, item 4a) ---------

LABEL_REQUIRED_FROM = datetime.datetime(2026, 10, 16, 0, 0)

_HEADING_FULL_RE = re.compile(
    r"^##[ \t]+Axis[ \t]+(\d+)[ \t]*(?:—|–|:|-+)?[ \t]*(.*?)[ \t]*$",
    re.MULTILINE)
_AXIS_NOLABEL_RE = re.compile(
    r"^[ \t]*(?:[-*+][ \t]+)?axis[ \t]+(\d+)[ \t]*:", re.IGNORECASE | re.MULTILINE)
_AXIS_LABELED_RE = re.compile(
    r"^[ \t]*(?:[-*+][ \t]+)?axis[ \t]+(\d+)[ \t]*([(—–\-].*?)[ \t]*:[ \t]*"
    r"(?:covered|queued|n/a)\b", re.IGNORECASE | re.MULTILINE)


def _now() -> datetime.datetime:
    """The ONE clock of the label-transition rule; a test pins it."""
    return datetime.datetime.now()


def label_required() -> bool:
    return _now() >= LABEL_REQUIRED_FROM


def _norm_key(text: str) -> str:
    # Quotes and backticks are typography of the heading, not part of the key
    # (axes 9, 10, 11, 14, 16 start with a quoted phrase) - the Lead's line at the
    # merge of F5-6 (t-773, question 2).
    t = text.replace("—", "-").replace("–", "-")
    t = re.sub(r"-{2,}", "-", t)
    t = re.sub(r"[\"'`«»“”‘’]", "", t)
    return " ".join(t.lower().split())


def axis_headings(map_text: str) -> list[dict]:
    """One dict per "## Axis N" heading of the map, in file order:
    number, heading (the line), title, full, short. full = the title cut at
    its FIRST colon, normalised (the cut is textual: a colon inside quotes
    cuts too); short = its first three words. full/short are None for a
    heading with no title (or one that is only a colon)."""
    out = []
    for m in _HEADING_FULL_RE.finditer(map_text):
        title = m.group(2).strip()
        full = _norm_key(title.split(":", 1)[0]) or None
        short = " ".join(full.split()[:3]) if full else None
        out.append({"number": int(m.group(1)), "heading": m.group(0).strip(),
                    "title": title, "full": full, "short": short})
    return out


def duplicate_headings(headings: list[dict]) -> dict[int, list[str]]:
    seen: dict[int, list[str]] = {}
    for h in headings:
        seen.setdefault(h["number"], []).append(h["heading"])
    return {n: hs for n, hs in seen.items() if len(hs) > 1}


def _line_at(text: str, start: int) -> str:
    end = text.find("\n", start)
    return text[start:end if end >= 0 else len(text)].strip()


def parse_axis_lines(text: str, scan_result=None) -> list[dict]:
    """Axis lines of a text, in order: number, label, shape_ok, line, offset.
    label is None for a line with no label ("axis N: ..."), else the
    normalised label body; shape_ok is False when the label is neither
    "(...)" nor led by a dash. A line inside a fenced/quoted region of
    scan_result is not read."""
    found = []
    for m in _AXIS_NOLABEL_RE.finditer(text):
        if _is_prose_position(scan_result, m.start()):
            found.append({"number": int(m.group(1)), "label": None, "shape_ok": True,
                          "line": _line_at(text, m.start()), "offset": m.start()})
    for m in _AXIS_LABELED_RE.finditer(text):
        if not _is_prose_position(scan_result, m.start()):
            continue
        raw = m.group(2).strip()
        if raw.startswith("("):
            shape_ok = raw.endswith(")") and len(raw) > 2
            body = raw[1:-1] if shape_ok else raw
        else:
            shape_ok = True
            body = raw.lstrip("—–- \t")
        found.append({"number": int(m.group(1)), "label": _norm_key(body),
                      "shape_ok": shape_ok, "line": _line_at(text, m.start()),
                      "offset": m.start()})
    return sorted(found, key=lambda d: d["offset"])


def label_problem(line: dict, headings: list[dict]) -> str | None:
    """None when the labelled line's label is acceptable for its axis, else
    the reason. The label must CONTAIN the short key of the axis (the short
    key is the head of the full one); an axis whose heading has no title has
    no key, nothing to compare."""
    head = next((h for h in headings if h["number"] == line["number"]), None)
    if head is None:
        return f"the map has no axis {line['number']}"
    if head["short"] is None:
        return None
    if line["shape_ok"] and head["short"] in line["label"]:
        return None
    for other in headings:
        if (other["number"] != line["number"] and other["short"]
                and other["short"] in line["label"]):
            return (f"that label is the key of axis {other['number']} "
                    f"(\"{other['short']}\"), not of axis {line['number']}")
    if not line["shape_ok"]:
        return "the label is not in an accepted form"
    return "the label matches no key of this axis"


def _label_refusal(hits: list[str], problems: list[tuple[dict, str]],
                   headings: list[dict]) -> str:
    out = ["commit touches mechanism files:\n  " + "\n  ".join(hits),
           "Rule 10(b)'s axis block names an axis by a label the map does not carry:"]
    for line, why in problems:
        out.append(f"  line: {line['line']}\n    why: {why}")
        for h in headings:
            if h["number"] == line["number"]:
                out.append(f"    the real heading of axis {line['number']} in "
                           f"docs/SIBLING_MAP.md: \"{h['heading']}\"")
                break
    out.append("Accepted forms (the key is the heading title up to its first colon, or "
               "the first three words of that; case, spacing, quotes and dash forms do "
               "not matter):\n"
               "  axis N (<key>): covered / queued / n/a <why>\n"
               "  axis N -- <key>: covered / queued / n/a <why>\n"
               "There is no door for a wrong label -- write the label from the map "
               "(the only waiver is the commit-message line \"axes: not a mechanism "
               "(<reason>)\").")
    return "\n".join(out)


def _added_lines(diff_text: str) -> str:
    """The added lines of a unified diff, without the leading '+'."""
    return "\n".join(l[1:] for l in diff_text.splitlines()
                     if l.startswith("+") and not l.startswith("+++"))


def label_verdict(msg: str, block_extra: str, axes: list[int], map_text: str,
                  hits: list[str], scan_result) -> tuple[int, str, set[int]]:
    """The label layer of the axis block (docstring item 4a): (1, reason,
    set()) on a duplicated heading number, on a wrong label in the message,
    or -- from LABEL_REQUIRED_FROM -- on an axis with no validly labelled
    line; else (0, "", closed), closed = the axes closed by a validly
    labelled line. Before the transition date the legacy "axis N:" coverage
    is judged by find_missing, not here."""
    headings = axis_headings(map_text)
    dups = duplicate_headings(headings)
    if dups:
        lines = [f"  axis {n}: " + "  AND  ".join(f"\"{h}\"" for h in hs)
                 for n, hs in sorted(dups.items())]
        return 1, ("the map has two headings of the same axis number -- fail-closed "
                   "(rule 10(b)); fix docs/SIBLING_MAP.md:\n" + "\n".join(lines)), set()
    msg_lines = parse_axis_lines(msg, scan_result)
    problems = []
    for line in msg_lines:
        why = label_problem(line, headings) if line["label"] is not None else None
        if why:
            problems.append((line, why))
    if problems:
        return 1, _label_refusal(hits, problems, headings), set()
    closed = {l["number"] for l in msg_lines if l["label"] is not None}
    closed |= {l["number"] for l in parse_axis_lines(_added_lines(block_extra))
               if l["label"] is not None and not label_problem(l, headings)}
    if not label_required():
        return 0, "", closed
    keyless = {h["number"] for h in headings if h["short"] is None}
    closed |= {l["number"] for l in msg_lines if l["number"] in keyless}
    missing = [n for n in axes if n not in closed]
    if not missing:
        return 0, "", closed
    unlabelled = sorted({l["number"] for l in msg_lines if l["label"] is None} & set(missing))
    out = ["commit touches mechanism files:\n  " + "\n  ".join(hits),
           "Rule 10(b)'s axis block has no labelled line (since "
           + LABEL_REQUIRED_FROM.strftime("%Y-%m-%d") + " the axis key is mandatory) for axes: "
           + ", ".join(str(n) for n in missing)]
    if unlabelled:
        out.append("lines without a label: " + ", ".join(f"axis {n}" for n in unlabelled))
    out.append("Write \"axis N (<key>): covered / queued / n/a <why>\" with the key from the "
               "map; the real headings:")
    out.extend(f"  \"{h['heading']}\"" for h in headings if h["number"] in missing)
    return 1, "\n".join(out), closed


def resolve_lead_binding(config_text: str | None) -> str:
    """The model bound to roles.lead in delegation.config.yaml. No file,
    no roles.lead key, or unparsable YAML -> default to the "fable"
    family (the subscription-contour default for Lead) -- a
    conservative (fail-closed) choice: it requires an explicit
    declaration from anyone below the top tier. The declaration itself
    is NOT checked for truth here (see tier_declared_ok) -- two-layer
    enforcement: code guarantees the shape, calibration against
    transcripts judges the truth, a tier above."""
    if not config_text:
        return "fable"
    try:
        data = yaml.safe_load(config_text) or {}
    except yaml.YAMLError:
        return "fable"
    lead = (data.get("roles") or {}).get("lead") or {}
    model = ((lead.get("subscription") or {}).get("model")
             or (lead.get("api") or {}).get("model"))
    return model or "fable"


def lead_family(binding: str) -> str | None:
    """The bound model's tier family by substring (fable/opus/sonnet/
    haiku); None -- no family recognized (a non-Claude binding), in
    which case only an exact model-id match qualifies."""
    low = binding.lower()
    for fam in LEAD_FAMILIES:
        if fam in low:
            return fam
    return None


def find_tier_declarations(msg: str) -> list[str]:
    """ALL "tier: <value>" line values in the commit message (not the
    diff) -- not just the first. Several mechanisms in one commit may
    each carry their own tier line. SAFE (fail-closed) semantics,
    chosen deliberately: every found line MUST pass tier_declared_ok
    (see decide_full below) -- reject if even ONE found line fails to
    match the binding, even when another (e.g. a real, later) line
    does match. The alternative ("passes if ANY line matches") was
    rejected: with MULTIPLE tier lines in one message, it would let one
    spoofed/quoted matching line mask a REAL mismatched value elsewhere
    in the same message.

    GUARANTEE-SCOPE CLARIFICATION (a sibling deployment's own review --
    docstring corrected, no code change): "ALL must pass" defends
    exactly that MULTI-LINE case (a real mismatched line plus a
    spoofing matching line next to it) -- a SINGLE-LINE spoofer (one
    fake tier line, no real one present) passes BOTH semantics THE
    SAME: this function never checks that the declared tier is TRUE,
    only that its declared FORM matches the binding (truthfulness of
    the declaration is calibration's job, reconciled against
    transcripts -- code guarantees the form, a tier above judges the
    meaning). The actual effect of the chosen semantics is fail-closed
    on quotes/multiple lines (a false reject is safer than a false
    accept), not a general anti-spoofing guarantee."""
    return [m.strip() for m in TIER_LINE_RE.findall(msg)]


def find_tier_declaration(msg: str) -> str | None:
    """Backward-compat convenience: the value of the FIRST "tier:
    <value>" line (see find_tier_declarations() for the full
    all-lines semantics used by decide_full())."""
    declarations = find_tier_declarations(msg)
    return declarations[0] if declarations else None


def _region_filtered_tier_declarations(msg: str, scan_result) -> list[str]:
    """A TIER_LINE_RE match counts ONLY when its own position is prose
    (see the docstring section "ALL-MUST-PASS COUNTS ONLY UNQUOTED
    TIER LINES"). scan_result is None -- fail-open, identical to
    find_tier_declarations() (every match counts)."""
    result = []
    for match in TIER_LINE_RE.finditer(msg):
        if not _is_prose_position(scan_result, match.start()):
            continue
        result.append(match.group(1).strip())
    return result


# --- config onboarding ladder (a full mirror of HQ's own gate logic):
# roles.{scout,builder,critic,lead,reserve} in delegation.config.yaml,
# in this FIXED functional order -- reserve (a Fable-class reserve
# tier) is the ONE rung STRICTLY ABOVE lead; roles.judge/roles.analyst
# are not coordination roles and are not part of the ladder.
# roles.designer is ALSO not a ladder rung -- designer is a standing
# function at the same tier as critic (see .claude/agents/designer.md)
# but is NOT a coordination role in the sense of this hierarchy (it
# coordinates specs, not dispatches work); like judge/analyst, its key
# is simply absent from ROLE_RANKS and build_role_ladder() does not
# read it by construction -- see test_build_role_ladder_ignores_designer.
ROLE_RANKS = {"scout": 0, "builder": 1, "critic": 2, "lead": 3, "reserve": 4}


def _resolve_role_model(role_data) -> str | None:
    """The model of ONE role, by the same subscription/api priority as
    resolve_lead_binding() -- but WITHOUT the "fable" default: a role
    with no model (the key is absent, or subscription.model/api.model
    are both empty) simply produces no ladder rung; that is not the
    same thing as the lead binding specifically (whose absence IS a
    meaningful subscription-contour default)."""
    if not isinstance(role_data, dict):
        return None
    model = ((role_data.get("subscription") or {}).get("model")
             or (role_data.get("api") or {}).get("model"))
    return model or None


def build_role_ladder(config_text: str | None) -> list[tuple[int, str]]:
    """[(rank, model_id)] per ROLE_RANKS, in the fixed order
    (scout=0 ... reserve=4) -- built from roles.* in config_text; a
    role with no configured model produces no rung. An empty/broken/
    absent config_text -> an empty ladder (fails open into the
    existing family heuristic in tier_declared_ok, which knows nothing
    about the ladder and works exactly as before)."""
    if not config_text:
        return []
    try:
        data = yaml.safe_load(config_text) or {}
    except yaml.YAMLError:
        return []
    roles = data.get("roles")
    if not isinstance(roles, dict):
        return []
    ladder = []
    for role_name, rank in ROLE_RANKS.items():
        model = _resolve_role_model(roles.get(role_name))
        if model:
            ladder.append((rank, model))
    return ladder


def _resolve_ladder_rank(declared: str, config_text: str | None) -> int | None:
    """Resolves a tier declaration into a ladder rank.

    The ladder path is legal ONLY when the ladder actually HAS a
    "lead" rung (roles.lead is configured with a model) -- without it
    there is no reference rank to call "above/at lead" relative to; an
    empty ladder OR a ladder without a lead rung -> None unconditionally,
    neither (a) nor (b) below is even tried (edge: roles.lead absent
    but reserve=opus configured -- "tier: opus" does not resolve via
    the ladder at all; the non-ladder "nothing above fable" pin from
    the existing branches still holds even with a config present, not
    only with config_text=None).

    (a) An EXACT match with some rung's model_id resolves to its rank
        -- when the SAME model_id sits on SEVERAL rungs (an admin
        literally duplicated the model), the MAXIMUM rank among all
        exact matches is taken, not the first one in ladder order
        (works for a non-Claude rung too -- "tier:
        llama-3.3-70b-versatile" matches a non-Claude lead rung by
        exact id). A family-strength guard (the same one branch (b)
        below already has) also applies HERE: when BOTH the lead
        rung's family and the candidate rung's family resolve to a
        non-empty LEAD_FAMILIES value, and the candidate's family is
        WEAKER than the lead rung's family, the exact match is
        DISCARDED (a nonsense config -- e.g. reserve configured with a
        model weaker than lead -- must not silently inherit rank 4
        through an exact-id match either). When the candidate rung's
        family is UNRESOLVABLE (a non-Claude model_id that happens to
        match `declared` exactly), the guard stays silent and TRUSTS
        THE LADDER'S POSITION (the config is the operator's word: if
        the admin put exactly that id on exactly that rung, there is
        nothing to compare against -- the position is authoritative).
        Likewise, when the lead rung's OWN family does not resolve
        (a non-Claude lead), the guard stays silent too (nothing to
        compare against).
    (b) Otherwise, when declared IS a Claude model (lead_family(declared)
        is not None), a family match of EXACTLY ONE ladder rung of
        that same family resolves to its rank -- AMBIGUITY (2+ rungs
        of the same family) does NOT resolve via this path at all (a
        documented fork: "when there is exactly one such rung").
        ADDITIONALLY the candidate rung's family must be NO WEAKER (by
        LEAD_FAMILIES ordinal, where index 0 is the strongest family
        "fable") than the lead rung's OWN family -- otherwise a
        nonsense config (e.g. reserve configured with a model weaker
        than lead, even though POSITIONALLY reserve is above) must not
        silently inherit the positional rank 4 through the family
        heuristic. The guard applies ONLY when the lead rung's family
        resolves (a Claude lead); with a non-Claude lead (the lead
        rung's family unresolved) there is nothing to compare against
        -- the guard does not block (the already-covered "reserve at a
        non-Claude lead" case).
    None -- a ladder with no lead rung, or declared resolves via
    neither (a) nor (b) (including a non-Claude declared with no exact
    id match -- the family path is simply undefined for it)."""
    ladder = build_role_ladder(config_text)
    lead_rank = ROLE_RANKS["lead"]
    lead_models = [model_id for rank, model_id in ladder if rank == lead_rank]
    if not lead_models:
        return None  # no lead rung -- the ladder path resolves NOTHING
    lead_model = lead_models[0]
    lead_fam = lead_family(lead_model)

    # Family-strength guard, ALSO on the exact-id-match path -- see the
    # docstring above, "(a) An EXACT match", for the full breakdown
    # (comparable families -> guard active; an unresolvable candidate
    # family -> trust the ladder's position).
    exact_matches = []
    for rank, model_id in ladder:
        if declared != model_id:
            continue
        cand_fam = lead_family(model_id)
        if lead_fam is not None and cand_fam is not None:
            if LEAD_FAMILIES.index(cand_fam) > LEAD_FAMILIES.index(lead_fam):
                continue  # nonsense: this rung is weaker than lead by family -- discard
        exact_matches.append(rank)
    if exact_matches:
        return max(exact_matches)  # the maximum rank among exact matches

    declared_fam = lead_family(declared)
    if declared_fam is None:
        return None
    candidates = []
    for rank, model_id in ladder:
        if lead_family(model_id) != declared_fam:
            continue
        # The guard is active only when the lead rung's family is known
        # (a Claude lead) -- a candidate rung is forbidden from being
        # WEAKER than lead by LEAD_FAMILIES ordinal (a larger index =
        # weaker).
        if lead_fam is not None:
            cand_fam = lead_family(model_id)
            if LEAD_FAMILIES.index(cand_fam) > LEAD_FAMILIES.index(lead_fam):
                continue  # nonsense: positionally >= lead, but weaker by family
        candidates.append(rank)
    if len(candidates) == 1:
        return candidates[0]
    return None


def tier_declared_ok(declared: str, binding: str, config_text: str | None = None) -> bool:
    """config_text (optional, default None): the config's onboarding
    ladder STRICTLY EXTENDS the existing paths below, never narrows
    them (see the docstrings of _resolve_ladder_rank/build_role_ladder
    above). The exact-match branch and the family-strictly-above-
    binding branch immediately below are a full mirror of HQ's own
    gate logic (a full-mirror-of-the-gate-logic port, not deployment
    history specific to HQ): the RESERVE-ABOVE-BINDING concept
    (a tier strictly above the current lead binding is still a full
    lead -- the same reasoning the config onboarding ladder itself
    encodes via its own "reserve" rung, one position above "lead") is
    the concept this template's own delegation.config.yaml ships too
    (roles.reserve, see CONFIG_LADDER_OPUS_LEAD_FABLE_RESERVE in the
    test twin) -- it is not gated on roles.reserve actually being
    configured. The ladder resolution (step below) is tried in
    ADDITION: a non-Claude binding with a non-Claude ladder resolves by
    exact id (see the "lead: llama-3.3-70b-versatile" case in the test
    twin)."""
    if declared == binding:
        return True
    fam = lead_family(binding)
    if fam is not None:
        if fam in declared.lower():
            return True
        # A declaration of a family STRICTLY ABOVE the binding's own
        # family is also legal -- the reserve-above-binding concept:
        # a tier above the current lead binding is a full lead itself
        # (the transitional commit re-binding Lead is committed BY a
        # session of the old, higher tier). Rank is the family's
        # position in LEAD_FAMILIES (index 0 = the strongest family,
        # "fable"); "strictly above" means a SMALLER index. A "fable"
        # binding has index 0 already -- no index is smaller than 0,
        # so this branch is silent for it without a separate check:
        # the "nothing above fable" regression pin holds automatically
        # by the index arithmetic. A non-Claude DECLARATION
        # (declared_fam is None) does not match this branch -- only an
        # exact match (step 1 above) or the ladder (step 4 below)
        # apply to it.
        declared_fam = lead_family(declared)
        if declared_fam is not None and LEAD_FAMILIES.index(declared_fam) < LEAD_FAMILIES.index(fam):
            return True
    # The config's onboarding ladder: a declared rank >= the "lead"
    # rung's FIXED position (ROLE_RANKS, independent of which rungs
    # happen to be configured today) is accepted.
    declared_rank = _resolve_ladder_rank(declared, config_text)
    if declared_rank is not None and declared_rank >= ROLE_RANKS["lead"]:
        return True
    return False


def _tier_queue_note() -> str:
    return ("a mechanism commit is Lead-tier work: a session below the "
            "lead binding's tier does NOT commit the mechanism itself -- "
            "it goes into the Lead queue in CURRENT_CONTEXT.md; a "
            "lead-tier session adds the line \"tier: <its own model>\".")


def _maybe_scan(msg: str, staged: list[str], merging: bool):
    """See the docstring section "LAZINESS": scan(msg) runs only when
    (a) the commit actually touches a mechanism path and isn't a
    merge, (b) the message carries a cheap marker hint ("axes"/
    "tier"), (c) the message carries at least one of "`>~". Returns
    None (zero scan calls) in every other case."""
    hits = mechanism_paths(staged)
    if not hits or merging:
        return None
    if not _MARKER_HINT_RE.search(msg):
        return None
    if not _has_region_marker_chars(msg):
        return None
    return _safe_scan(msg)


def _skip_declared(msg: str, scan_result) -> bool:
    """A SKIP_RE match counts ONLY when its position is prose (see the
    docstring section "POLICY"). scan_result is None -- fail-open, the
    FIRST match (if any) is immediately True -- byte for byte
    SKIP_RE.search(msg) of the pre-region gate (see the docstring
    section "FAIL-OPEN ON SCANNER FAILURE")."""
    for match in SKIP_RE.finditer(msg):
        if scan_result is None:
            return True
        if _is_prose_position(scan_result, match.start()):
            return True
    return False


def _decide_core(msg: str, block_extra: str, staged: list[str],
                  map_text: str | None, merging: bool, scan_result) -> tuple[int, str]:
    """Pure core of decide() -- the hits->merging->skip->fail-closed
    branch order is UNCHANGED (see the docstring section "BRANCH
    ORDER UNCHANGED")."""
    hits = mechanism_paths(staged)
    if not hits:
        return 0, ""
    if merging:
        return 0, ""
    if _skip_declared(msg, scan_result):
        return 0, ""
    if map_text is None:
        return 1, (f"axis map not found ({MAP_PATH}) -- fail-closed, "
                   "commit rejected (rule 10(b))")
    axes = parse_axes(map_text)
    if not axes:
        return 1, ("no axis found in the map (## Axis N) -- "
                   "fail-closed (rule 10(b))")
    code, reason, closed = label_verdict(msg, block_extra, axes, map_text, hits,
                                         scan_result)
    if code:
        return code, reason
    missing = [n for n in find_missing(msg + "\n" + block_extra, axes)
               if n not in closed]
    if missing:
        return 1, ("commit touches mechanism files:\n  " + "\n  ".join(hits)
                   + "\nRule 10(b)'s axis block is incomplete -- no verdict for axes: "
                   + ", ".join(str(n) for n in missing)
                   + "\nAdd \"axis N (<key>): covered / queued / n/a <why>\" "
                   "(<key> = the heading title in the map up to its first colon; "
                   "a line with no label is accepted only before "
                   + LABEL_REQUIRED_FROM.strftime("%Y-%m-%d") + ") for "
                   "every axis of the map (in the commit message or in the "
                   "decision text, DECISIONS.md), or an explicit skip in the "
                   "COMMIT MESSAGE: \"axes: not a mechanism (<reason>)\" "
                   "(rule 10(b)).")
    return 0, ""


def decide(msg: str, block_extra: str, staged: list[str],
           map_text: str | None, merging: bool = False) -> tuple[int, str]:
    """Pure gate decision. block_extra -- the diff of DECISIONS.md."""
    scan_result = _maybe_scan(msg, staged, merging)
    return _decide_core(msg, block_extra, staged, map_text, merging, scan_result)


def decide_full(msg: str, block_extra: str, staged: list[str],
                 map_text: str | None, config_text: str | None,
                 merging: bool = False) -> tuple[int, str]:
    """decide() plus the tier-declaration requirement (rule 7): a
    "tier: <value>" line on the "mechanism" branch (axis block already
    satisfied, not skip, not merge). config_text -- the text of
    delegation.config.yaml (or None if the file is absent), the same
    pattern as map_text. ONE _maybe_scan() call for the whole call,
    reused by both the skip check (via _decide_core) and the tier
    check below (see the docstring section "LAZINESS")."""
    scan_result = _maybe_scan(msg, staged, merging)
    code, reason = _decide_core(msg, block_extra, staged, map_text, merging, scan_result)
    if code:
        return code, reason
    hits = mechanism_paths(staged)
    if not hits or merging or _skip_declared(msg, scan_result):
        return 0, ""
    binding = resolve_lead_binding(config_text)
    # ALL found tier lines must pass -- reject if even ONE does not
    # match the binding (see find_tier_declarations()'s docstring for
    # the chosen semantics). Region-aware selection (see the docstring
    # section "ALL-MUST-PASS COUNTS ONLY UNQUOTED TIER LINES").
    declared_list = _region_filtered_tier_declarations(msg, scan_result)
    if not declared_list:
        return 1, ("commit touches mechanism files:\n  " + "\n  ".join(hits)
                    + "\nNo \"tier: <value>\" line (lead binding: "
                    + binding + ") -- " + _tier_queue_note())
    bad = [d for d in declared_list if not tier_declared_ok(d, binding, config_text)]
    if bad:
        return 1, ("commit touches mechanism files:\n  " + "\n  ".join(hits)
                    + "\nNot lead tier: \"tier: " + bad[0]
                    + "\" does not match the binding (" + binding
                    + ") -- " + _tier_queue_note())
    return 0, ""


def _git(*args: str) -> str:
    proc = subprocess.run(["git", *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.stdout or ""


class AuditError(RuntimeError):
    """The audit could not answer its question (git absent, not a repository,
    an unreadable date): the audit then FAILS, it never reports an empty window."""


def _git_strict(*args: str) -> str:
    """git against the repository root (never the cwd) that fails LOUD: a
    non-zero exit or a missing git is an AuditError, not an empty output
    (t-777 F2: the audit used to read a failure as '0 commits')."""
    try:
        proc = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
    except OSError as exc:
        raise AuditError(f"git is not available ({exc})") from exc
    if proc.returncode:
        first = next(iter((proc.stderr or "").strip().splitlines()), "")
        raise AuditError(f"git {args[0]} failed with exit {proc.returncode}"
                         + (f": {first}" if first else ""))
    return proc.stdout or ""


_SINCE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?)?$")


def _since_ok(since: str) -> bool:
    if not _SINCE_RE.fullmatch(since):
        return False
    try:
        datetime.datetime.fromisoformat(since)
    except ValueError:
        return False
    return True


def _log_records(log_text: str):
    """(sha, committer wall clock, message body) per record of the audit's
    `git log --format=%H%x1f%cI%x1f%B%x1e`. The committer date, read at its own
    wall clock (the first 19 characters of %cI), is what the transition rule
    judges: the author date is the committer's to set (t-777 F2)."""
    for record in log_text.split("\x1e"):
        sha, _, rest = record.strip("\n").partition("\x1f")
        committed, _, body = rest.partition("\x1f")
        if not sha.strip():
            continue
        try:
            when = datetime.datetime.fromisoformat(committed.strip()[:19])
        except ValueError as exc:
            raise AuditError(f"unreadable committer date {committed!r} of {sha.strip()[:8]}") from exc
        yield sha.strip(), when, body


def _audit_commit(sha: str, when: datetime.datetime, body: str,
                  headings: list[dict]) -> tuple[int, list[str]]:
    """(accepted unlabelled lines, mismatch lines) of one commit message. An
    unlabelled line is accepted only while the commit's committer date is
    before LABEL_REQUIRED_FROM; on/after it, it is a mismatch."""
    scan_result = _safe_scan(body) if _has_region_marker_chars(body) else None
    accepted, bad = 0, []
    for line in parse_axis_lines(body, scan_result):
        if line["label"] is not None:
            why = label_problem(line, headings)
        elif when >= LABEL_REQUIRED_FROM:
            why = (f"unlabelled after the transition: committed {when:%Y-%m-%d %H:%M:%S}, "
                   f"the axis key is mandatory from {LABEL_REQUIRED_FROM:%Y-%m-%d}")
        else:
            accepted += 1
            continue
        if why:
            bad.append(f"{sha[:8]}  {line['line']}\n          -> {why}")
    return accepted, bad


def audit_labels(since: str, map_text: str | None, git=_git_strict) -> tuple[int, str]:
    """Calibration reader (docstring item 4a, the finding's item (b)): for
    every commit of the window (git log --since) that touches a mechanism
    path -- merges included, against their first parent -- every axis line
    whose label mismatches the map, and every unlabelled line of a commit
    whose COMMITTER date is on/after LABEL_REQUIRED_FROM (the merge and replay
    road the commit-msg gate does not see). Exit 1 on a mismatch, an unusable
    map, a bad --since, or a git failure (git absent, not a repository); 0
    otherwise -- a window with no mechanism commits is "0 commits, 0
    mismatches", exit 0. Unlabelled lines of earlier commits are only counted.
    The CURRENT map is the reference, not the map of the commit's day; git runs
    against the repository root, whatever the cwd."""
    if map_text is None:
        return 1, f"axis map not found ({MAP_PATH}) -- fail-closed"
    headings = axis_headings(map_text)
    dups = duplicate_headings(headings)
    if not headings or dups:
        return 1, ("the map has no axis heading" if not headings else
                   "the map has two headings of the same axis number: "
                   + ", ".join(f"axis {n}" for n in sorted(dups)))
    if not _since_ok(since):
        return 1, (f"mechanism_gate audit: --since must be an ISO date "
                   f"(YYYY-MM-DD or YYYY-MM-DDTHH:MM), got {since!r}")
    window, commits, unlabelled, mismatches = 0, 0, 0, []
    try:
        for sha, when, body in _log_records(
                git("log", f"--since={since}", "--format=%H%x1f%cI%x1f%B%x1e")):
            window += 1
            paths = git("show", "--format=", "--name-only",
                        "--diff-merges=first-parent", sha).splitlines()
            if not mechanism_paths(paths):
                continue
            commits += 1
            accepted, bad = _audit_commit(sha, when, body, headings)
            unlabelled += accepted
            mismatches.extend(bad)
    except AuditError as exc:
        return 1, f"mechanism_gate audit: {exc}"
    head = (f"mechanism_gate audit since {since}: {commits} commits on mechanism paths, "
            f"{len(mismatches)} mismatches ({unlabelled} axis lines without a label, "
            f"accepted before {LABEL_REQUIRED_FROM:%Y-%m-%d}; {window} commits in the "
            f"window; reference: the current map)")
    return (1 if mismatches else 0), "\n".join([head, *mismatches])


def _audit_main(argv: list[str]) -> int:
    since = None
    for i, arg in enumerate(argv):
        if arg.startswith("--since="):
            since = arg.split("=", 1)[1]
        elif arg == "--since" and i + 1 < len(argv):
            since = argv[i + 1]
    if not since:
        print("mechanism_gate: --audit needs --since <date>", file=sys.stderr)
        return 1
    map_text = (MAP_PATH.read_text(encoding="utf-8", errors="replace")
                if MAP_PATH.exists() else None)
    code, report = audit_labels(since, map_text)
    print(report)
    return code


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("mechanism_gate: need a path to the commit message file", file=sys.stderr)
        return 1
    if argv[0] == "--audit":
        return _audit_main(argv[1:])
    staged = [p for p in _git("diff", "--cached", "--name-only", "--no-renames", "-z").split("\0") if p]
    merge_head = _git("rev-parse", "--git-path", "MERGE_HEAD").strip()
    merging = bool(merge_head) and Path(merge_head).exists()
    msg = Path(argv[0]).read_text(encoding="utf-8", errors="replace")
    block_extra = _git("diff", "--cached", "--", DECISIONS_FULL)
    map_text = (MAP_PATH.read_text(encoding="utf-8", errors="replace")
                if MAP_PATH.exists() else None)
    config_text = (CONFIG_PATH.read_text(encoding="utf-8", errors="replace")
                   if CONFIG_PATH.exists() else None)
    code, reason = decide_full(msg, block_extra, staged, map_text,
                               config_text, merging)
    if code:
        print("mechanism_gate: " + reason, file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
