# FV1-24 K1 — diff critic (t-769) on builder t-760

Diff: worktree `.claude/worktrees/fv1-24-k1`, `wip/fv1-24-k1` = 525f719 (code) + 4bb6329 (table) against origin/main
(merge base 1a00352). Spec: card K1 of `docs/tasks/specs/20261114-fv1-24-bug-drafts-verdict-spec.md` as amended by §11; plan
review `reviews/20261114-fv1-24-plan-critic.md` (Key 2, Key 8, A1-A4).

**Verdict: accept with fixes (fit_with_fixes). One fix is BINDING before merge (F1). K1 may merge before K1g once F1 is in AND the
Lead has written the K1g node row (F2): gate B blocks the place-born draft before and after K1 with the same findings (measured,
key g).**

## Key (a) — empirics on a byte copy of ARM LOCAL-1

Copied with `cp -r` into the scratch folder (project layout kept: `proj/qa-factory/{config.json,artifacts/LOCAL-1}`). Ran once with
the K1 worktree package and once with read-main (bug_records/place_answers/contract are byte-equal between the merge base and
read-main: `git diff --stat 1a00352 ba903eb -- <3 files>` empty). Verbatim, K1:

```
qty-input-product-page.json triage_ref= {'instance_id': 'TC-008#obs1', 'attempt_id': 'a1'}
  confirmation_of: ('reproduced_by_factory', ['walk'], [])
  no_run_target: True
  reproduction_problems: ['walk'] []
qty-input-cart-page.json triage_ref= {'instance_id': 'TC-009#obs1', 'attempt_id': 'a1'}
  confirmation_of: ('reproduced_by_factory', ['walk'], [])
  no_run_target: False
  reproduction_problems: ['walk'] []
settled_answer case-TC-008 -> (..., 'settled', '')
settled_answer draft-qty-input-cart-page -> (..., 'settled', '')
```

main:

```
qty-input-product-page.json  confirmation_of: ('unconfirmed', [], ['no APP_BUG triage row'])
qty-input-cart-page.json     confirmation_of: ('reproduced_by_factory', ['walk'], [])
settled_answer case-TC-008 -> (..., 'carrier missing', 'no draft carries this walk receipt (no APP_BUG triage row)')
settled_answer draft-qty-input-cart-page -> (..., 'settled', '')
```

The plan critic's simulation holds: product page -> `reproduced_by_factory` [walk]; cart unchanged. The walk record of
case-TC-008 still stands NOW (capture hash, quote, R-3). Control for "TC-008 is in no run": `grep -c TC-008 run-report.json` = 0
(also case-insensitive 0); control `TC-009` = 144.

## Findings

**F1 (BINDING, fix before merge) — `no_run_target` lifts drafts whose instance the report DOES hold.** Surface: the "held ids" set
of `bug_records.no_run_target` (`bug_records.py:978-982`). It is built only from `instance_results` keys, `current_instance_results`
keys and `triage_failures` names. A green manual check, a result row's `case`, a non-failing row's `test_id`, and a surprise line
past the cap are held by the report but not in that set. Probe (in memory, K1 package), `no_run_target(draft, report)`:

```
True   green manual check, draft names its case          (manual_checks [{case TC-9, result pass}])
True   red automated row carries case TC-1, draft names case
True   green automated row carries case TC-1, draft names case
False  #sur within cap
True   #sur past cap (overflow)                            (report holds TC-9#sur-overflow; 99 surprises, cap 30)
True   #obs index past the list                            (TC-9#obs5, the check has 2 observations)
False  #obs within list
True   lower-case spelling                                 (e2e::X vs e2e::x)
False  report holds [chromium], draft bare
False  later attempt only in history
False  stale history row
True   diagnostic row in history only
True   manual_human case
False  test-only row (no instance_id), draft names test
True   test_id-only row, draft names test_id               (that row is PASSED)
True   current_manual_checks present, legacy manual_checks holds case
```

Each True above (except `manual_human` and lower-case) breaks §11's binding K1-a invariant: "a draft whose instance the current
report holds (any attempt, any spelling) keeps both facts". Old code never lifted these (APP_BUG fails, because finalize archives a
row that binds to no failure). K1 lifts them on a walk alone, skipping the triage verdict and the red-now fact. The worst row is a
draft on a case the runner ran and found green (a green manual check, or a passed row named by its `test_id`).

The docstring says "matches NO id the report holds in ANY attempt and ANY spelling". For these inputs that sentence is false: a
name that lies.

Fix, about 6 lines, error toward "is a target":
- (i) `wanted` also holds the case of an `<case>#obs<n>` / `#sur-…` instance, read through `C.target_parts` (the ONE reader of
  that name, `contract.py:4828`);
- (ii) `held` also takes `instance_id`, `test_instance_id`, `test_id`, `test` and `case` of every `results` / `current_results`
  row, and `case`, `instance_id` and `test` of every `current_manual_checks` and `manual_checks` entry, whatever the result.

The ARM lift survives the fix: TC-008 appears nowhere in the report (grep above). Add ONE row per new class to the K1 table:
- a green manual check of the case;
- the case of a red result row;
- `#sur-<id>` past the cap.

These are defect-born rows (TESTING.md :56), not edge receipts.

Not findings:
- **Lower-case ids.** The contract's own `same_id` / `id_spellings` are case-sensitive everywhere (bind_triage, finalize).
  Widening here alone would be a second spelling rule.
- **`manual_human` / `impossible` cases.** The runner never executes them, which is the place-born class by definition.

**F2 (Lead, precondition of merging before K1g) — the gate B twin is not queued on a carrier.** §11 says K1g, N-a, N-b, N-c and A12
are "rows in an untaken live-run-fvf batch". `git grep -i K1g origin/main -- plans/piles/live-run-fvf`: 0 hits. Control
`FV1-24` hits README:70 and batch-1:53. Whole repo: only the spec and a compact snapshot. Working tree: only the journal. The
local `batch-2-live-run-fvf.md` has no `check_bug_drafts` row either. Rule 9 / D-0044 needs a node row. Line for «Остатки»:
`gate B gate_preflight.check_bug_drafts exempts a no-run-target draft by bug_records.no_run_target | узел: K1g` (Lead opens the
row in batch-2 of live-run-fvf; same for N-a, N-b, N-c, A12).

**F3 (queue, not blocking) — `_walk_has_no_run(..., no_run: bool = False)`.** The default lets a future caller skip the
computed value silently. The only caller passes it, and the error of the default is the safe one. Drop the default in the
fix round if it is touched anyway.

## Keys (b)-(h)

- **(b) Direction of error.** Red test, runner observation within its list, `[chromium]` both ways, a later attempt, stale
  history, `test`-named rows, a `#sur-` within the cap: all keep both facts (probe above, and table rows 2, 3, 6). The holes
  are F1.
- **(c) Positional invariant, read at `bug_records.py:1034-1054`.** `wide` is unchanged. The early `if wide and not has_walk:
  return` is unchanged. `no_run` is computed only inside `if has_walk:`. The per-entry `wide and not walking` skip is unchanged, so
  a non-walk entry keeps both facts. Table rows 4 and 7 confirm it, and row 7 checks that R_NO_TRIAGE is still reported for the
  fresh entry beside the lifted walk.
- **(d) Computed once, one reader.** `no_run_target` is called once at `:1040`. Both the APP_BUG decision (`:1042`) and
  `_walk_has_no_run(..., no_run)` (`:1043`) read the value. Grep `no_run_target|_walk_has_no_run` (case-insensitive) over the
  package finds only these sites plus the changelog. The function is public and pure, `(draft, report)`: K1g can import it with
  the `step_facts` report it already reads (`gate_preflight.py:5893`).
- **(e) The walk record in the table is real.** `_k1_world` writes the record through `place_answers.write`: capture in
  `captures.jsonl` with its sha256, quote in the capture, requirement quote in the register. Cheap control on the ONE function:
  - as committed: 14/14 PASS;
  - capture bytes changed after the write: row "place-born walk lifts" FAIL (step and reason), row "non-walk beside walk" FAIL
    (step);
  - answer flipped to `not_a_bug`: the same 3 FAIL;
  - total over the three runs: 36/42. The table kills both.
- **(f) TESTING.md.** One parameterised table, ids name the case, no negative control inside, no pin. It is a table of id
  membership (layer 3 in kind), placed in the `detector` keep file by the Lead's decision after the variant route was shown
  impossible. Test lines (72) outnumber product lines (~39), with the reason named: the world builder. Missing: the defect-born
  rows of F1.
- **(g) Siblings and gate B before K1g.** Measured with `Rehearsal(task,'B').check_bug_drafts()` on the ARM copy. The findings are
  IDENTICAL on main and on K1:
  - TC-009 without its cause;
  - **TC-008 bug draft without a triage verdict — TC-008 is red with no triage verdict …**;
  - TC-008 without its cause.

  K1 neither adds nor removes a gate B block. The "reproduction not checkable" finding was not raised before either (R_NO_TRIAGE
  only).

  What changes:
  - `gate_brief` (`:4664`), `delivery_summary`, `factory_dashboard` now print `reproduced_by_factory` (walk) for TC-008;
  - `settled_answer(case-TC-008)` goes from `carrier missing` to `settled`, so `investigation.unresolved_targets` (iv) resolves
    it and `close_unsettled` no longer writes its coverage gap.

  So a person reaching the packet on the waiver road reads "reproduced by the factory" beside a factory finding "TC-008 is red
  with no triage verdict". The "is red" half is already false today (TC-008 never ran), so K1 adds no new false fact, and the
  changelog says gate B still blocks. Acceptable to merge before K1g, provided F2's node row exists. No reader shows a NEW block.
- **(h) Census, architecture, judgment.** Both commits carry `architecture: AR-13, AR-19, AR-28, AR-29 -- …`, `judgment: none --
  a join …`, `tier: sonnet`. No ratchet file is touched (`git diff --stat` over census / role-load / known_red / baselines: empty).
  `reproduction_problems` stays census class xref (`judgment-census.json:76`). `no_run_target` refuses nothing, so it is not a
  unit; the census value is read from CI (slow file). AR-28 is touched and named, but F1 is its breach. AR-19: no place source is
  read by name (grep of the diff: no `case-`/`req-`/`draft-`/`new-` literal in product code). Judgment: none moved; a join on
  membership.

## Standing questions

- **Fit to spec:** NO until F1. Everything else is as written: the public name, computed once, the positional invariant, the
  changelog with the K2 sentence and gate B still blocking.
- **Builder's own decisions:**
  - adding `instance_results` (all attempts) to the held set: safe direction, good;
  - widening both sides of the spelling (`wanted & id_spellings(name)`), unlike `same_id`'s one-sided widening: safe for
    this predicate, because over-matching keeps facts;
  - the place-born world built on the register road (`req-R-1`) instead of `case-TC-008`: same draft-wide facts; acceptable,
    and covered by key (a) empirics.
- **Seams:** additive. `_walk_has_no_run` gains an optional argument. gate_preflight is not touched.
- **Class-wide completeness:** the gate B twin (K1g) is designed but has no node row (F2). The F6 branch of `_walk_has_no_run`
  (`:1000`) matches names exactly, without spellings. It is pre-existing and safe in direction, so no finding.
- **DUPLICATION AND CONSISTENCY:** `no_run_target` is a third reading of "does the report hold this instance", beside
  `_walk_has_no_run` (exact triage_failures names) and `_current_red_problem` (current_instance_results). The plan's A3 asked for
  it to be computed once, and it is. No repository helper enumerates "every id a report holds" (grep of `contract.py` for
  `def …(report…) -> set` / `*ids*` / `*cases*`: none; `triage_targets()["all"]` covers failing rows only). The F1 fix should reuse
  `C.target_parts`, not a new split. Clone ratchet: read from the branch's forge-check, not re-run.
- **CODE QUALITY:** the new function is 18 lines, with 2 levels of nesting. Its docstring sentence is false until F1. F3 is
  queued. No dead branches.
- **Hygiene:** English, no Cyrillic in the package diff; `selftest --limits --lang` 4/4 in the builder's witness.
- **IN-TREE RATCHETS:** none raised.
- **ARCHITECTURE:** see (h).
- **JUDGMENT:** none.
- **ONE ROAD:** none found. Grepped the diff for language, runner and project names and place-source prefixes: none. Every place
  source goes through the same predicate.

## Trail

Read:
- spec lines 1-466 (§11 included);
- plan critic lines 101-310;
- `critic-diff-brief.md` whole;
- builder report whole;
- `bug_records.py:370-410, 900-1189`;
- `contract.py:4300-4380, 4520-4850`;
- `gate_preflight.py:1484-1513, 5863-6023`;
- `gate_brief.py:4640-4679`;
- `TESTING.md:40-104`;
- `judgment-census.json` grep;
- `critic_verdict.schema.json`.

Commands (outputs verbatim above):
- `git diff origin/main...HEAD` (package);
- the ARM probe ×2 packages;
- the `no_run_target` awkward-id probe;
- `Rehearsal('B').check_bug_drafts()` ×2 packages;
- the K1 table alone plus 2 tamper controls (`( cd <pkg> && python -B - )`, temp worlds via `harness.temp_project`, worktree
  `git status` clean afterwards);
- grep K1g with control;
- grep TC-008 with control.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 bug_records.no_run_target:978-982 lifts drafts whose instance the report holds: a green manual check named by its case, the case of a red or green result row, a passed row named by test_id, a #sur-<id> past the cap (report holds #sur-overflow), #obs<n> past the list - breaks section 11 K1-a and the docstring's own claim"
  ],
  "fixes": [
    "F1 (binding, before merge): in no_run_target add the case of an observation or surprise instance via C.target_parts to the wanted spellings, and add instance_id, test_instance_id, test_id, test and case of every results/current_results row plus case, instance_id and test of every current_manual_checks and manual_checks entry (any result) to the held set; add three defect-born rows to the K1 table (green manual check of the case, the case of a red result row, #sur past the cap).",
    "F2 (Lead, before merging K1 ahead of K1g): write the K1g node row (and N-a, N-b, N-c, A12) into an untaken live-run-fvf batch; none exists on origin/main or in the working tree.",
    "F3 (queue): drop the default of no_run in _walk_has_no_run so a future caller cannot skip the computed value silently."
  ],
  "class_completeness": "Surface: the held-ids set of no_run_target. Walked: magnitude (surprise cap, obs index), spelling ([chromium] both sides, case, test vs test_id vs instance_id), attempts (history, stale, diagnostic), empty/absent (no triage_ref, empty report). Holes are F1. Map twin: gate B gate_preflight.check_bug_drafts (K1g) designed in spec section 11 but has no node row (F2). F6 branch of _walk_has_no_run matches exactly without spellings - pre-existing, safe direction, no finding.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-24-bug-drafts-verdict-spec.md",
      "docs/tasks/specs/reviews/20261114-fv1-24-plan-critic.md:101-310",
      "docs/tasks/critic-diff-brief.md",
      ".claude/worktrees/fv1-24-k1/docs/tasks/specs/reports/20261114-fv1-24-k1-report.md",
      ".claude/worktrees/fv1-24-k1/ai-packages/qa-factory/scripts/bug_records.py:370-410,900-1189",
      ".claude/worktrees/fv1-24-k1/ai-packages/qa-factory/scripts/contract.py:4300-4380,4520-4850",
      ".claude/worktrees/fv1-24-k1/ai-packages/qa-factory/scripts/gate_preflight.py:1484-1513,5863-6023",
      ".claude/worktrees/fv1-24-k1/ai-packages/qa-factory/scripts/gate_brief.py:4640-4679",
      ".claude/worktrees/fv1-24-k1/ai-packages/qa-factory/scripts/tests/test_bug_records.py (diff)",
      "docs/TESTING.md:40-104",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "ARM byte copy: confirmation_of both drafts, no_run_target, settled_answer case-TC-008 / draft-qty-input-cart-page, K1 package vs read-main", "result": "K1: product page reproduced_by_factory [walk], settled; cart reproduced [walk] both; main: product page unconfirmed no APP_BUG, carrier missing"},
      {"command": "no_run_target awkward-id probe (16 synthetic reports)", "result": "True (lifted) for green manual check case, case of red/green result row, #sur past cap, #obs past list, test_id-only passed row, diagnostic history row, legacy manual_checks under current_manual_checks; False for [chromium], later attempt, stale, test-named, #sur/#obs within list"},
      {"command": "gate_preflight Rehearsal(task,'B').check_bug_drafts() on ARM copy, K1 vs read-main", "result": "identical 3 findings incl. TC-008 bug draft without a triage verdict"},
      {"command": "test_bug_records.a_draft_of_a_place_the_runner_never_ran alone + capture-tamper + answer-flip controls", "result": "committed 14/14 PASS; each tamper fails 3 checks (lift step+reason, beside step); 36/42 total"},
      {"command": "git grep -i K1g origin/main -- plans/piles/live-run-fvf (control FV1-24)", "result": "0 hits; control hits README:70, batch-1:53"}
    ]
  }
}
```
