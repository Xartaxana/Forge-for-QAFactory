# t-353 — critic on the PLAN t-346 (OH8-7b..h chain spec)

Reviewed: `docs/tasks/specs/t-346-oh8-7b-chain-spec.md` (593 lines, read whole, with section 6a).
Code base: worktree `.claude/worktrees/oh8-7` at 0bc7b1d (`git log -1`: "OH8-7 (t-329): the judgment census sees refusals
raised through package subclasses (c1)..."). Pending list: scratchpad `oh8-7-pending.txt` (190 lines).
Critic tier: Opus. This verdict is an input to the Lead's acceptance, not the acceptance (rule 6).

**Verdict: fit_with_fixes** — the mechanism is feasible and measured correct on 0bc7b1d, the partition is exact; seven
blocking spec edits (all text edits to t-346, none reopens a Lead decision) must land before the first dispatch.

---

## Key 1 — Facts by trail (spot-checks)

| # | spec claim | code at 0bc7b1d | result |
|---|---|---|---|
| 1 | family + widened sites at `test_judgment_census.py:276-277` | :276 `family = refusal_registry.raise_family(...)`, :277 `wide = ...sites(..., raises=family)` | true |
| 2 | u3 creation at :246-247, per-file loop at :236, flip loop :278-289, `SUBCLASS_PENDING_CEILING` at :99 | :236 `for file, tree in trees.items()`, :246-247 `for s in sites_by_file...: add(file, s["function"], "u3")`, :281-289 pending loop, :99 `= 190` | true |
| 3 | literal sites are a subset of widened sites, asserted at :847 | :847 `assert {key(s) for s in base} <= {key(s) for s in wide}` | true |
| 4 | `sites()` reports the outermost enclosing function (E12) | `refusal_registry.py:1203-1206`: `ast.walk` from the module, `owner.setdefault(id(child), node.name)` — the outer def is visited first and claims every descendant; a method's owner is the method (a class is no FunctionDef) | true |
| 5 | gate item 7 (v): `blocks_overrides` raise needs `moves ... to code`; `blocking_per_role.*`/`safety` raise accepts `adds data check` | `tools/architecture_gate.py:51-53`; `WEAK_KEYS = ("safety",)`, `WEAK_PREFIXES = ("blocking_per_role.", "safety.")` :102-103; `census_state` :282 `need = "code" if any(not _is_weak(...))` | true (F-A's premise holds; E9 holds: word-list/meaning-proxy/meaning/breach are not weak) |
| 6 | C2 demands a `note` with `blocks_override` (:353-360) and refuses an override on a non-blocking unit | :353-360 | true |
| 7 | NEGATIVE: `subclass_pending|SUBCLASS_PENDING|pending_names` occurs only in the test, the fixture and `docs/SIBLING_MAP.md` | my own case-insensitive `grep -rli` over the oh8-7 tree (`*.py *.md *.json *.yml`, specs excluded): exactly those 3 files (positive control: the hit list itself contains the test that defines the constant at :99) | reproduced |
| 8 | critic-diff-brief q11 lists `SCAN_ROOT`..`MEANING_CEILING` but no `SUBCLASS_*` (F-B) | `docs/tasks/critic-diff-brief.md:72` lists `BLOCKING_ENTRY_FILES`, `UNIT_NAME_RE`, `JUDGE_CALLS`, `MEANING_CEILING`; grep `SUBCLASS` in the brief: no hit | true |
| 9 | axis 34 has a "known roads off it" row; `OH8-7` appears in SIBLING_MAP only on the axis-18 line 390 (C-7) | `SIBLING_MAP.md:588` (row), :390 (only `OH8-7` hit) | true |
| 10 | current ceilings: `blocks_overrides` 10, `blocking_per_role.conductor` 491 | fixture `ratchet`: blocks_overrides 10, conductor 491, safety 55 (sim output below) | true |

## Key 2 — Completeness (partition), mechanical

Command (read-only, script in scratchpad `t353_partition.py`; parses spec lines 177-228, the `**OH8-7x (N)**` blocks):
`python -B t353_partition.py <spec> oh8-7-pending.txt`

```
OH8-7b declared 23 listed 23 files 1
OH8-7c declared 23 listed 23 files 1
OH8-7d declared 38 listed 38 files 6
OH8-7e declared 32 listed 32 files 6
OH8-7f declared 24 listed 24 files 7
OH8-7g declared 29 listed 29 files 8
OH8-7h declared 21 listed 21 files 10
total listed 190 distinct 190 dups []
missing from spec []
extra in spec []
files 38
```
The script also checks every per-file `(n)` against the names on its line: no COUNT MISMATCH printed. Every one of the 190 in
exactly one node; every node 21-38 (within 20-40). DoD item satisfied.

## Key 3 — Feasibility of `SUBCLASS_UNIT_FILES` in `units_of`

Feasible, no second walk, C7 stays dense — **measured**, not argued. Simulation (scratchpad `t353_sim.py`): run the real
`units_of` on 0bc7b1d, then compute what listing ALL 38 files would create (wide-site functions in those files not already
units):

```
pending on tree: 190 == file: True
listing all 38 files would create 190 units
created - pending: []
pending - created: []
span-hit sites in the 38 files: 0 []
whole tree: wide-site functions not units and not pending (end-state extra units): []
module-level wide sites: [('metric_signals.py', 367)]
```
- AR-13: step 1 only moves the existing `raise_family`/`sites(raises=)` calls (:276-277) above the loop; `sites()` is still
  called twice as today. No `ast.Raise` in the test. Holds.
- C7 dense: a listed file's widened sites all hit their own created unit (name match at :285), so pending loses exactly the
  listed functions. Created u3 units carry no span, so they never absorb sites of other functions by line. Holds.
- The one thing that could break DoD 3 ("C1 names EXACTLY the node's N"): a widened site whose `function` is not a unit but
  whose LINE lies inside a nested unit's span is today hit by span (never pending) and would become a NEW created unit in a
  listed file — outside every node list. Count today: 0 (line "span-hit sites" above). It can appear after waves 11/12; the
  re-measure step does not look for it (B5).
- The end state (OH8-7h): no extra unit anywhere on 0bc7b1d (line "whole tree ... []"); same drift caveat (B5).
- Per-function entries: implementable as `s["file"] in unit_files or f"{s['file']}::{s['function']}" in unit_files`; the E5
  stale check reads `wide_by_file`. No problem.
- What breaks as written: the synthetic helper `_run` (:600-606) defaults only `pending_ceiling`; with
  `analyse(unit_files=None) -> SUBCLASS_UNIT_FILES` every synthetic package gets the REAL tuple, and E5 fires "lists
  `probe_by_code.py::...`, which the scan does not hold" in every synthetic run. Tests that assert no C7 / no problem at all go
  red: :823 `assert not _run(files, _census(), pending_ceiling=1)["problems"]["C7"]`, :655 `assert not any(r2["problems"][k]
  ...)`. (B4)

## Key 4 — Fork decisions of 6a

- **F-P = (a)**: sound. The extra match form lives one node (b -> c) and is covered by two C7 table rows.
- **F-Z = (b)**: sound. The scripts are read, not written; drift is detected (re-measure, E7/E8). Accept the stated cost.
- **F-D = (a)**: sound for the mechanism (E15), but it collides with section 4.3's question route (B2).
- **F-B = (a)**: sound; but 6a widens it (question 9 too) and the body was not updated: 3.3 owns says "under fork F-B (a)",
  DoD 9's doc-witness keys name only SIBLING_MAP, section 5's b/h cells lack the brief, and 1.3 axis 1 still says "n/a — no
  policy ... changes" although the critic brief (the carrier of the critic role's rule 18 / CLAUDE.md rule 3) now changes (B1).
- **F-A = (b)**: acceptable under AR-20, with two changes.
  1. The size is not caused by F-A. By construction every created unit BLOCKS (its own widened site flips it, :285-286), so
     the chain raises `blocking_per_role` by at least one per row whatever F-A says: conductor 491 -> up to ~681, and every
     role +k for each hook-path row (rule 4.2 (ii) assigns all 13 keys). F-A (b) adds only the E3 subset. The raise is a
     truthful measurement: these 190 refusals already stand on the path and were only uncounted (held by C7). AR-20 asks that
     a raise be NAMED row by row, not that it be avoided — so the size is legal.
  2. Where it does bury signal: a node that raises `conductor` by +30 can hide +1 that belongs to no new row (a class change
     on an existing row, a merge artefact), and DoD 6's form `<key>: old -> new -- census classifies ... of <files>` is per
     KEY, not per row. Fix (B3): the witness carries a reconciliation — for every raised key, delta == the number of the
     node's new rows naming that role; every other `ratchet` key unchanged — printed by the builder (mechanical layer), so
     the critic re-runs instead of counting by eye. And the E3 rows must be findable later: they carry a `note` beginning
     `E3:` without `blocks_override` (C2 permits a bare `note`; the fixture already has 18 `"note"` keys against 10
     `blocks_override`), so the queued override fix is a grep, not a memory. The finding for gate form (a) needs a named
     carrier (a pile finding path) in 6a.

## Key 5 — AR-29 / P27

The structure is right: the builder classifies only shape/xref by plain reading, everything else goes up, the pair critic
reads every row (q11), `MEANING_CEILING` and class ceilings are untouchable (E9 + gate). Two defects:
- Step 3's order lets a builder dilute a guard into `shape`. It tests "presence of a file/field/input, a parse failure ->
  shape" FIRST and lists "a guard reading (safety)" under "anything else". A Sonnet builder stops at the first match. The node
  lists are full of plausible guards whose raising condition is literally a presence/form test:
  `import_test_receipt._reject_destination_symlinks` (:189), `_safe_local`, `_trusted_producer` (:54), `_write_exclusive`;
  `red_sandbox._clone_guard`; `event_store._require_root`; `environment_preparation._claim_locked`;
  `release_fingerprint.write_release`. Diluting `safety` into `shape` is the unsafe direction the census docstring forbids
  (:30-32: "a guard is never diluted into `shape`"), and `safety` is a gate-weak key, so nothing else catches it. (B6)
- E3/4.2 step 2 still tells the builder to return non-refusing functions as questions; 6a says not to (B1).

## Key 6 — Weakest node

**OH8-7g** on judgment, **OH8-7h** on mechanics.
- g: `question_register` (6), `person_words` (2: `read`, `_from_file` — "a person's words" is literally `safety`'s
  definition), `assertion_detectors` (5: `shape_patterns` :289, `assertion_detectors` :248 — pattern tables over assertions,
  a `meaning-proxy` candidate -> E9 stop), `question_stop` (`_as_share`, `defaults`). Plausibly 10-15 of 29 go up. The spec
  gives no forecast and no rule for a node that ends with half its units as questions (is it one fix round? does f+g's critic
  wait?). The builder would have to invent the cadence (B2).
- h: classification plus the removal. Uninvented except: `_run`'s `kw.setdefault("pending_ceiling", 0)` (:602) must go when
  the keyword goes (TypeError otherwise; not in 3.5 item 2); the rewrite of `test_neg_subclass_raises_flip_blocks_or_are_pending`
  (:807-817) for "unit created" is described in prose only (which rows get a `check_f` row, what `blocking_units` becomes for
  `neutral_only`); and 3.5 item 6's zero-hit grep is unachievable (B7).

## Key 7 — Sequencing under a moving main

Step 3.2 is a good shape (I re-ran it verbatim on 0bc7b1d for OH8-7d: `node files pending: 38 | spec list: 38`, exit 0; with
one bogus name added: `missing from the tree: ['run_suite.py::nope']`, exit 2 — the stop works). It is not enough (B5):
1. It checks only the node's OWN files. A pending function that a wave adds in a 39th file (in no node) is never classified:
   each node lowers by its count from the tree's value, and OH8-7h reaches 21 -> 1, not 0, then the removal turns it into a
   rowless unit. Nothing stops earlier.
2. It does not detect span-hit sites in the node's files (key 3), which make DoD 3's "exactly N" fail after the edit, with no
   instruction.
3. OH8-7h has no whole-tree pre-check that removal creates no unit outside its list.
4. A traceback (waves change `units_of`'s shape) exits 1, a code the spec does not define.

## Duplication and consistency (rule 18, brief item 6)

None found in the plan's mechanism: the C7 list-form checks (E4/E5) do not duplicate C1's stale-row check (one judges the
tuple, the other rows); the per-function form is born and dies inside pair 1. Inconsistency found: the body vs 6a (B1).
Grepped: `SUBCLASS|pending` in the brief, SIBLING_MAP, the test.

## Code quality (rule 18, brief item 7)

Plan-level: the `unit_files` keyword mirrors `entry_files`/`pending_ceiling` (consistent). Defect: the default plumbing for the
synthetic helper is missing (B4).

## One action, one road (rule 19, brief item 12, P31)

The chain IS a temporary second road (subclass-only refusers pending in unlisted files), bounded by two constants, recorded on
axis 34 (C-7) and closed at OH8-7h with no branch left. No exclusion of a language/project/case. The per-function sub-form is
a third road for one file for one node, removed by OH8-7c. Verdict: holds, given B5/B7 so that the close is reachable.

## Class-wide completeness (rule 5, SIBLING_MAP)

Axis 18 (ratchets): covered by 3.4 item 6 / 3.5 item 5. Axis 32: covered. Axis 34: covered (C-7). Axis 1: NOT covered after
6a's F-B (a) — the critic brief is the carrier CLAUDE.md rule 3 and the critic role's rule 18 point to; 1.3 still says n/a
(part of B1). Question 9's list gap (spec §8) is closed by 6a — good, but not carried into 3.4.

---

## Blocking findings (each with the exact spec edit)

**B1. 6a is not folded into the body; a builder reading sections 2-5 follows the superseded text.**
Evidence: E3 (l.140) "until it is answered, the builder returns the function as a question"; 4.2 step 2 (l.371-372) "return
it as a question (4.3) with the proposed note"; 4.3 bullet 3 (l.396) — vs 6a F-A (l.529) "The builder does not return these
as questions". Section 5 still carries script paths in «Пишет в» (6a F-Z: "re-cut before it is pasted"). 3.3 owns (l.266)
conditional on F-B; DoD 9 keys miss the brief; 1.3 axis 1 "n/a".
Edit: (i) E3 behaviour cell: "the row is written WITHOUT `blocks_override`, class by the raising condition as for any unit,
with `note: \"E3: refuses nothing -- <why>; override queued (<finding path>)\"`; listed in the report"; (ii) 4.2 step 2:
same, no question; (iii) delete 4.3 bullet 3; (iv) section 5 re-cut to F-Z (b) now, b/h cells add
`docs/tasks/critic-diff-brief.md`; (v) 3.3 owns: brief unconditional for b and h, "questions 9 and 11 lists only"; 3.4 adds an
item 7 (add `SUBCLASS_PENDING_CEILING` to q9, both constants to q11), 3.5 the removal; (vi) DoD 9 keys add, for b: both
constant names present in the brief; for h: both absent; (vii) 1.3 axis 1: "covered — critic brief q9/q11 lists edited;
CLAUDE.md rule 10 paragraph and designer rule 1 name no constant (checked)".

**B2. The question route deadlocks against F-D's pairs.** 4.3 sends questions "to the Lead, who routes it to the critic of the
pair"; DoD 7 demands green to commit; a node with an open question is red (C1), so it cannot commit, so the next node of the
pair cannot start on its tip (F-D (a)), so the pair critic never runs. Edit to 4.3 (and 6a F-D): "Questions are answered by
the Lead (Fable, the tier above the builder) in one batch per node, or by ONE critic question-pass per node when the Lead
routes them down — not by the pair critic. A node with open questions is not committed and does not release the next node;
the answers are written in a fix round of the same task_id, then the node commits." Add a line forecasting that OH8-7e and
OH8-7g are expected to carry the most questions (guards; person's words; assertion patterns).

**B3. Raise attribution is per key, not per row.** Edit to DoD 6: "paste the output of a reconciliation (scratchpad script,
pure read, full source in the report): for each `blocking_per_role.<r>` and `safety`, old -> new, and the number of the node's
NEW rows that name `<r>` (resp. class `safety`); they must be equal; every other `ratchet` key and every EXISTING row unchanged
(`git diff` of the fixture shows only inserted rows and the ratchet lines)." Add to E10: "all created units block by
construction (their own widened site flips them), so each new row raises every role it names by 1".

**B4. `_run` does not default `unit_files`.** Edit to 3.4 item 4: "`_run` gains `kw.setdefault(\"unit_files\", ())` next to
`pending_ceiling` (:602): a synthetic package lists nothing unless the case says so; otherwise E5 fires on every synthetic run
(the real tuple names files the temp package lacks)." Edit to 3.5 item 2: "both `setdefault` lines of `_run` go."

**B5. The re-measure step misses three drift classes.** Edit to 3.2: the script takes the node's list AND the union of the
remaining nodes' lists (this one to OH8-7h) and adds three outputs, each a stop (exit 2): (a) `pending names in no remaining
node:` (must be none); (b) `listing would also create:` wide-site functions in the node's files that are neither units nor
pending (must be none); (c) for OH8-7h only, whole tree: wide-site functions that are neither units nor pending (must be
none) and `pending total == 21`. Any other exit code (a traceback) is a stop with the output. The script is the scratchpad
`t353_sim.py` logic, a pure read.

**B6. Section 4.2 step 3 tests `shape` before `safety`.** Edit: make step 3's FIRST test "Does the raise protect the
application, secrets, an outside write, a person's words or git state (a symlink or path escape, a lock or claim, a root or
clone guard, trust of a producer or signature, an exclusive write)? -> question with a `safety` proposal", then shape, then
xref; add "a condition that is both a presence test and a guard is the guard (CLASS_ORDER: safety > shape)".

**B7. OH8-7h's zero-hit grep is unachievable as scoped.** 3.5 item 6: "zero hits ... outside `docs/tasks/specs/`" — but the
batch-9 file itself (section 5's «Бриф» names `SUBCLASS_PENDING_CEILING` / `SUBCLASS_UNIT_FILES`), journal notes, compact
snapshots and pile findings will hold them. Edit: scope the grep to `ai-packages/`, `tools/`, `PROCESS/`, `.github/`,
`docs/SIBLING_MAP.md`, `docs/tasks/critic-diff-brief.md`, `CLAUDE.md`, `PROJECT.md`; history carriers (`docs/tasks/`,
`plans/piles/`, `logs/`) are excluded by name.

## Non-blocking

**N1.** 3.5 item 3: spell out the post-removal `SUBCLASS_ROWS` test body (which cases keep the `check_f` row; `neutral_only`
expects C1 `helpers_x.py::f is a check unit (u3)` and `blocking_units` 0 with no row / 1 with a row).
**N2.** 1.1 AR-22 row: the "positive control: finds the constant at :99" is a hit of the searched pattern itself, not a
control of a different known sample; acceptable as the hit list is non-empty, but name it as such.
**N3.** §8's "estimate" of ~190 can be stated as a measured lower bound: every created unit blocks (key 3), so the sum of
per-role raises over the chain is >= 190.
**N4.** 6a F-A: name the carrier of the queued gate-form finding (path under `plans/piles/<slug>/findings/`) and the
batch it goes into (D-0044), so the E3 `note`s point to it.

Owner questions: none decided here; all fork decisions remain the Lead's (6a). Acceptance of t-346 belongs to the Lead.

## Trail

Read: the spec whole (1-593); `test_judgment_census.py` 1-898 (whole); `refusal_registry.py` 1040-1219; `tools/architecture_gate.py`
whole; `design/architecture.md` 134-280 (AR-29, AR-13, AR-20, AR-22, AR-28); `tools/critic_verdict.schema.json`; greps in
`critic-diff-brief.md` (q11 list :72), `SIBLING_MAP.md` (:24 axis 1, :390, :588), fixture (`"note"` 18, `"blocks_override"`
10), `assertion_detectors.py`, `import_test_receipt.py` def lines.
Not read (outside need): t-321 part B, t-337 draft, PROJECT.md item 11 beyond the auto-loaded text — the spec's facts I
needed were verified against code directly.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 6a decisions not folded into the body: E3, 4.2 step 2, 4.3 bullet 3 still route non-refusing functions as questions; section 5 not re-cut to F-Z (b); F-B (a) brief edit not in owns/3.4/DoD 9; 1.3 axis 1 still n/a",
    "B2 question route deadlocks against F-D pairs: a node with open questions is red and cannot commit, so the pair never reaches its critic; the Lead (or one question-pass per node) answers, the node does not release the next one until answered",
    "B3 ratchet raise named per key, not per row: DoD 6 needs a reconciliation witness (delta per role == new rows naming it; no other ratchet key or existing row changed); E3 rows carry an E3 note",
    "B4 _run (test line 602) does not default unit_files to (): with analyse defaulting to the real tuple, E5 fires in every synthetic run and the no-problem assertions at lines 655 and 823 go red",
    "B5 re-measure checks only the node's own files: misses pending names in no remaining node, span-hit sites that listing would turn into extra units, OH8-7h whole-tree check, undefined exit on traceback",
    "B6 section 4.2 step 3 tests shape before safety: guards whose condition is a presence test get diluted into shape; safety first, per CLASS_ORDER",
    "B7 OH8-7h zero-hit grep outside docs/tasks/specs is unachievable (batch-9 file, journals, snapshots name the constants): scope it to package, tools, PROCESS, .github, SIBLING_MAP, critic brief, CLAUDE.md, PROJECT.md"
  ],
  "fixes": [
    "B1: rewrite E3 / 4.2 step 2 / 4.3 to F-A (b) with an E3 note; re-cut section 5; brief in owns, 3.4 item 7, 3.5, DoD 9 keys; axis 1 covered",
    "B2: 4.3 and 6a F-D: Lead answers questions per node (or one critic question-pass per node); node not committed and next node not released until answered; forecast e and g",
    "B3: DoD 6 reconciliation script output; E10 sentence that every created unit blocks",
    "B4: 3.4 item 4 adds kw.setdefault unit_files to _run; 3.5 item 2 removes both setdefault lines",
    "B5: 3.2 script takes the remaining-nodes union and stops on names in no node, on extra created units, and (h) on any whole-tree extra or pending total != 21; non-0/2 exit is a stop",
    "B6: 4.2 step 3 safety test first, then shape, then xref",
    "B7: 3.5 item 6 grep scope by named directories, history carriers excluded",
    "N1-N4 optional: SUBCLASS_ROWS post-removal body, AR-22 control wording, measured lower bound of the raise, carrier of the gate-form finding"
  ],
  "class_completeness": "Axes 18, 32, 34 covered by the plan; axis 1 not covered after 6a F-B (a) edits the critic brief (B1). Feasibility measured on 0bc7b1d: listing all 38 files creates exactly the 190 pending names, 0 span-hit extras, 0 end-state extras; drift after waves 11/12 is the open class (B5).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-346-oh8-7b-chain-spec.md (whole)",
      ".claude/worktrees/oh8-7/ai-packages/qa-factory/scripts/tests/test_judgment_census.py (whole)",
      ".claude/worktrees/oh8-7/ai-packages/qa-factory/scripts/refusal_registry.py 1040-1219",
      ".claude/worktrees/oh8-7/tools/architecture_gate.py (whole)",
      ".claude/worktrees/oh8-7/ai-packages/qa-factory/design/architecture.md 134-280",
      ".claude/worktrees/oh8-7/docs/tasks/critic-diff-brief.md (grep, line 72)",
      ".claude/worktrees/oh8-7/docs/SIBLING_MAP.md (grep, lines 24, 390, 588)",
      ".claude/worktrees/oh8-7/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json (ratchet, note/override counts)",
      "tools/critic_verdict.schema.json",
      "scratchpad oh8-7-pending.txt (whole)"
    ],
    "reruns": [
      {"command": "python -B scratchpad/t353_partition.py t-346 spec oh8-7-pending.txt", "result": "7 nodes 23/23/38/32/24/29/21; total 190 distinct 190; missing [] extra [] dups []; 38 files"},
      {"command": "python -B scratchpad/t353_sim.py oh8-7 package oh8-7-pending.txt", "result": "pending 190 equals file; listing all 38 files creates 190 units; created-pending [] pending-created []; span-hit 0; whole-tree end-state extras []; conductor 491, blocks_overrides 10"},
      {"command": "python -B scratchpad/t353_remeasure.py (spec 3.2 verbatim) for OH8-7d list", "result": "node files pending 38, spec list 38, exit 0; negative control with run_suite.py::nope added: missing listed, exit 2"},
      {"command": "grep -rli subclass_pending|pending_names over oh8-7 tree excluding docs/tasks/specs", "result": "3 files: fixture, test, SIBLING_MAP (spec's negative claim reproduced)"}
    ]
  }
}
```
