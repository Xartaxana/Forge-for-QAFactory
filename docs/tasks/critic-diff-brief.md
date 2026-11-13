# Standing brief for the critic gate on a builder diff

Owner's word, 06.10.2026: after the 0.8.1 clean-up (six real repeats converted to one function each,
B-309) the order is KEPT — every diff gate checks duplication and code quality, and the clone ratchet
is the deterministic layer. This brief is the rule text of the critic gate on a diff: CLAUDE.md rule 3
and the critic role file's rule 18 point here (B-419).

## The two layers (CLAUDE.md rule 3, the two-layer review rule)

- **Mechanical layer** — attached by the BUILDER to its handoff, verbatim, before the critic starts:
  the DoD run tails (D-0056, 21.10.2026: the files `scenario_walk.py --witness-for <owns>` prints — plus, until
  `scripts/tests/test-layers.json` holds quarantine rows, the changed module's test file — and the DoD keys — no
  neighbours, no big files, no docker); no mutation list (retired 10.11.2026, `docs/TESTING.md`); the ratchets
  (`dup_ratchet --check`, `lint_ratchet --check`) are NOT in the builder's layer: their result is the `forge-check` job of the
  branch or MR pipeline (batch level, `plans/builder-rules.md` 7b/7c; D-0033 as refined by the Lead), which the critic reads, never
  re-runs; the old-vs-new counts where the spec asks for them. A layer not attached
  is returned to the dispatcher as a request, never executed by the critic.
- **Verdict layer** — the critic's own zone: architecture, semantics, class-wide completeness, the
  edges' error direction, the tests' killing power, and the two standing questions below. A cheap
  control re-run of what is attached (ONE small fast test file the verdict depends on, or one guard
  selftest) is legitimate; `test_story_step.py`, `test_story_run_*.py`, full `selftest.py`, docker,
  ratchets and mutation runs are not — they are the batch canon's (D-0056);
  re-deriving the mechanics by reading everything is not.

## The standing questions (every diff gate, each with its own verdict line)

1. **Fit to the spec**: every requirement, edge and key the dispatch names — implemented as written,
   with the error direction the spec states (FR-41/FR-59: no unknown becomes a pass).
2. **The builder's own decisions** on points the spec left silent: each in the safe direction, each
   consistent with the consumers named in the spec.
3. **Seams**: the files other nodes own or follow on — additive, localized, nothing reordered.
4. **Class-wide completeness** (rule 9, FR-54): the SIBLING_MAP axes and the neighbours in the same
   artifact; a sibling neither fixed nor queued is a finding. An analog outside the node's `owns` that this round does not fix
   comes back as a line the Lead writes into «Остатки» as is: `<what> | узел: <node id>` (a node row the Lead opens in an
   untaken batch, D-0044) or `<what> | перенос: <findings/<file> | пачка N> | обоснование: <why> | подтвердил: —`; a bare queue
   line is refused by `piles.py check` (д) (F6-30).
5. **Tests** (`docs/TESTING.md`, the owner's word 10.11.2026): would the node's test catch the defect the node
   exists for, through the door the factory uses — judged by READING it; is there a junction test when the node
   changes a field, a refusal or a handoff form. Findings: a pin on role text, on the source of a script, on a
   measured constant, a receipt per DoD key / edge / mutation, a negative control inside a test (the table
   «не пишется» of `docs/TESTING.md`); more test lines than product lines with no reason named; a subprocess per
   check where one world per file would do. A missing pin is NOT a finding. The layers
   (`ai-packages/qa-factory/scripts/tests/test-layers.json`, spec `docs/tasks/specs/td-15-scenarios-quarantine.md`): a new
   test file with no keep row, or a keep row whose layer/why does not hold — finding; an edit to a quarantined file without a
   `quarantine-edit:` reason that holds — finding; a phase-2 move whose replacement does not catch the detector's class —
   finding.
6. **DUPLICATION AND CONSISTENCY**: does the diff implement anything the repository already has a
   reader, writer, helper, data table, refusal text builder, tokenizer or path resolver for? For
   each such place: the existing one with file:line, and whether the diff should have reused it,
   extended it, or whether the convergence is already queued (a queued analog named in the spec is
   queued, not a finding). The positive control for "no second implementation" is a grep of the
   same shape over the package; the clone ratchet's output is read, not re-derived.
7. **CODE QUALITY** beyond style-as-bug-mask: functions over roughly 60 lines or with more than three
   nesting levels in the NEW code (name them with line ranges), copy-pasted blocks inside the diff,
   dead branches, names or annotations that lie, work whose result nobody reads. Each is a finding
   with a severity — blocks / fix before merge / queue — never a style pass and never "I don't like it".
8. **Hygiene** where the diff is in the package: FR-29/FR-30, the size caps, CRLF kept.

9. **IN-TREE RATCHETS** (SIBLING_MAP axis 18, 16.10; since D-0060 the members include `scripts/tests/fixtures/judgment-census.json` `ratchet` and `role-load.json` `process_ratchet_tokens`): a diff that adds or raises a row of an
   in-tree shrink-only ratchet is named in the verdict, row by row (key, old → new count, the
   reason), and an unnamed raise is a finding. The ratchets: `audit_factory.NO_MOVE_BASELINE` /
   `NO_MOVE_BASELINE_MAX` (A27), `OUTSIDE_WALKS` / `OUTSIDE_WALKS_MAX`, `fixtures/env-facts-baseline.json`,
   the driver-layers upward edges and L8 rows, `tools/dup-baseline.json`, the lint ratchet baseline,
   A24 / A26 `ANCHOR_FLOOR`; the known-red ledger `scripts/tests/fixtures/form-rounds.json` (`known_red`,
   `not_in_world` and `pins.not_in_world`, read through `scripts/tests/known_red.py`) and the hand-input
   line of `tools/lint_ratchet.py` (`HandReaderInput`). A diff that adds a row to `known_red` or
   `not_in_world`, or raises its pin, names each raise and its existing pile node; a raise the verdict
   does not name is a blocker. A diff that DOORS a site (`# remains: <reason>`) gets its reason read.

10. **ARCHITECTURE** (D-0055; `design/architecture.md`): which AR-n invariants does the diff touch by its files and functions (grep the map), and does the commit/report name them? For each named one: is its change check done (the producer–reader walk BOTH ways with a positive control; the twins; the one-way rule — no second reader, writer, form or seam)? An AR-n touched but not named, a producer removed while a reader stays, or a second way of an existing thing is a finding with a severity (blocks when a reader is starved).
11. **JUDGMENT** (P27, AR-29): does the diff move judgment into code — a check that classifies a role's judgment, closes a role's
    obligation by a closed-list reason, or refuses a role's output on its content? Does it add text a role must read that is not
    testing craft (a procedure of keys, scripts and refusals)? Read every census row the diff adds or reclassifies (a class lowered —
    `word-list` → `shape` — is the cheap way past the ratchet), every `blocks_override: false` it adds (a computed refusal relabelled
    as non-blocking is the other cheap way), every edit of the census test's scan constants (`SCAN_ROOT`, `SCAN_EXCLUDE`,
    `BLOCKING_ENTRY_FILES`, `UNIT_NAME_RE`, `JUDGE_CALLS`, `MEANING_CEILING`), and every `<!-- kind: craft -->` marker it adds (a process
    section marked craft escapes the process ratchet). Each is a finding with a severity; a `judgment: none` or `adds data check` on a diff
    that does move judgment blocks. The census (`scripts/tests/fixtures/judgment-census.json`) and `role-load.json` `process_ratchet_tokens`
    are shrink-only ratchets of axis 18 — question 9 applies to them.

12. **ONE ROAD** (P31, AR-1, AR-2, AR-15; SIBLING_MAP axis 34; asked on a plan gate too, where there is no diff yet): does the spec or
    the diff take one action by a different road for a language, project or case: does a shared mechanism go another way for it, or not
    reach it? An ordinary condition of the task is not one. (a) A non-goal, a table row, an "unchanged" or a "not supported for X" that
    leaves a language, project or case outside a shared mechanism blocks, unless the difference is a data row with a default read by a
    capability key, one role step taken alike on every side, or the owner's word quoted with its carrier; read the carrier (a paraphrase
    by a Lead or a builder is not the word, PROJECT.md «Командная работа» п. 6). (b) A new branch, parser or runner check on a language,
    runner or project name in the diff: name its data row or its door. Once `tools/language-sites-baseline.json` exists (spec t-2065 N2),
    read its row and the `tools/language_sites.py --raises --base <merge base>` output attached by the mechanical layer, then walk the forms
    the tool cannot see (its docstring, "KNOWN MISSES"); until then the search is yours, and the verdict names it. (c) An exclusion that
    STAYS (the owner's word, or a census row of `docs/tasks/specs/reports/t-2046-language-exceptions-census.md` not yet fixed) is named
    in the verdict like a ratchet raise, row by row: what, which mechanism, its carrier or its node; an unnamed one is a finding. (d) A
    residual of this class, yours or an earlier verdict's: a fix in this round or a node with an id and an owner; a line for the
    coordinator to tell someone is itself a finding. An empty answer is explicit: "none found: <what was grepped>".

## What comes back

Verdict (accept / accept with fixes — each fix with file:line and whether it blocks the merge /
reject with `failure_class`) / Findings numbered / Seam and class notes / Spot-checks (claims verified
with their carriers; every negative with its positive control) / Trail (files, line ranges, commands
with verbatim output) — under about 1800 words, trail last, then the closing ```json block per
`tools/critic_verdict.schema.json`.

The review is a FILE at the dispatch's `handoff:` path: its form, the closing ```json block and the fallback with no path
are `.claude/agents/critic.md` rules 16-17; acceptance runs `python tools/critic_verdict_check.py <file>`, exit 0 required.
