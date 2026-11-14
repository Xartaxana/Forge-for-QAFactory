# FV1-24 — a manual-pass bug draft reaches a verdict; a draft on an inferred expectation becomes a question

Designer draft (t-748) for Lead acceptance, 14.11.2026. Pile `live-run-fvf`, batch 1, node FV1-24 (P1), finding
`plans/piles/live-run-fvf/findings/20261113-sravnenie-chernoviki-bagov-ne-podtverzhdeny.md` (instances (б), (в) of the blind
evaluation `experiments/mybooks/factory-vs-free-agent/runs/blind-eval.md:52-53`, cards 1, 2, 3/23, 4 `:20-23`). Stands on FV1-22
(accepted 379f687, t-700; spec `docs/tasks/specs/20261114-fv1-22-recut-spec.md`).

Roots. PKG = `C:\QAFactory\forge-repo\.claude\worktrees\read-main\ai-packages\qa-factory` (origin/main as read today). ARM =
`C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1` (the LR2-1 run the finding
cites; the repo copy `experiments/.../runs/factory-out/` holds only `work/`, not `evidence/` or `state/`). Line numbers drift; a
builder finds functions by NAME. Package text English (FR-30). I had no shell: nothing below was EXECUTED; every fact is READ
(where a claim needs a run, §9 says so).

-----------------------------------------------------------------------------------------------------------------------------

## 0. Facts read on the carrier

### 0.1 The mechanism already exists (t-1991): places, three-way answers, expectation source, gap at close

- `PKG/scripts/place_answers.py` docstring `:1-17`: a PLACE is a suspicion the run left unconfirmed; the analyst answers each
  with `bug`, `not_a_bug`, `requirement_silent` (a question, never a bug) or `impossible`, quoting a recorder capture and naming
  the expectation source (`requirement`, `question`, `person`, `none`; never `none` for a bug). Code checks keys and joins only.
- `places()` `:294-319` joins FOUR sources into ONE list: `_register_places` `:240-246` (register row whose `code_says`
  contradicts), `_target_places` `:249-267` (investigation targets: `investigation.investigation_targets` `:130-217` = the
  `inconclusive`/`manual_skipped` rows of ACCEPTED S6 forms, and refused pinned cases), `_draft_places` `:270-291` (every
  draft whose step reads `unconfirmed` — red-test drafts AND manual drafts), and `new-`/`record` places `:313-318`.
- `answer_problems` / `_answer_lines` `:474-536`: membership of `answer` and `expectation.source`; `none` only for the
  `none_allowed` answers `:495-498`; `_requirement_list` `:381-395` refuses a `bug` citing an R in
  `C.unconfirmed_requirements(text, questions)` `:391-394`; `requirement_silent` owes `question` `:505-506`; `not_a_bug`
  owes `why` and `seen.quote` `:509-513`; the capture must be in the recorder index, unchanged, holding the quote
  (`capture_stands` `:334-378`, error direction DOWN); `bug` owes a draft of THIS place (`_bug_list` `:453-471`).
- `settled_answer` `:639-694`: the ONE predicate "settled"; `bug` is settled only when its draft's step is
  `reproduced_by_factory` with a `walk` receipt (`:663-678`); `not_a_bug`/`requirement_silent` with a draft of the place
  still `unconfirmed` -> `conflict` (`:679-685`); non-bug answers need their register line (`:686-694`).
- `close_unsettled` `:728-820`: every unsettled place of source `draft`/`register` gets ONE `coverage_gap` register line
  (the GAP road to the report); a `requirement_silent` answer's line is `unresolved_question` with `owner_role` =
  `investigation.OWNER_WORDS` and `oracle_status: owner_question` (`_line_for` `:825-847`).
- Driver: `Driver.s7_place_lines` `PKG/scripts/driver_dispatch.py:4026-4068` puts the list, the four answers and the four
  sources into EVERY S7 triage dispatch prompt (ONE site `:716-718`, before `extra`) — this is where the analyst learns the
  requirement before the work (FR-38). `s7_close_places` `PKG/scripts/driver_stage_s7.py:569-588` runs `close_unsettled`
  at each of the three S7 code closers (`:78`, `:110`, `:515`), BEFORE the investigation gate. `s7_places_scribe_line`
  `:590-627` gives the S8 scribe (the tier above) each settled answer WITH its expectation source.
- The step reader: `PKG/scripts/bug_records.py` `confirmation_of` `:1119-1162` (THE reader, AR-13) and
  `reproduction_problems` `:983-1079`. A `walk` entry still needs two draft-wide facts (`:1016-1020`): the draft's triage row
  says APP_BUG (`_app_bug_problem` `:941-945`; skipped only for a code-reading draft) and, unless the draft has "no run by
  construction" (`_walk_has_no_run` `:967-980`: code-reading, or a triage key that names a `manual`/`observation` failure
  of the CURRENT report), the instance is red NOW (`_current_red_problem` `:948-964`: absent -> `R_NO_CURRENT`).
- Triage rows not bound to a current failure are archived: `PKG/scripts/finalize_task.py` `refresh` `:726-746`
  (`bind_triage` against `C.triage_failures(report)`; the rest goes to `state/migration/stale-triage-*.json`,
  reason "not bound to current failure").
- Observations and recorder surprise lines are ALREADY collected by code as triage targets: `contract.triage_failures`
  `PKG/scripts/contract.py:4693-` (one `<case>#obs<n>` per observation, one `<case>#sur-<id>` per uncited surprise line up to
  `surprise.max_per_attempt`, then `#sur-overflow`, `:4621-4672`); `Driver.s7_unbound` / `s7_fresh` `driver_stage_s7.py:324-343`
  keep S7 open while a current failure has no triage row.
- Charter: `PKG/agents/qa-failure-analyst.md:56` already says "Find out the truth on the page ... a bug, with the requirement it
  breaks; not a bug, with the words you saw; or a place the requirements are silent on: a question ... never a bug. Name where
  your expectation comes from; one the factory derived itself is no requirement." Also `:26`, `:46`, `:59`, `:74`.
  `PKG/agents/qa-runner.md:24`, `:43` (every doubt an observation; every `surprise:` line recorded).

### 0.2 What happened in LR2-1 (measured on ARM; positive controls named)

| item | carrier read | fact |
|---|---|---|
| L1 | `ARM/work/handoffs/S7-qa-failure-analyst-1.yaml:70,107-118,208-211` | runner never ran TC-008/TC-010; analyst-1 walked them, wrote triage row `TC-008#obs1` APP_BUG -> `qty-input-product-page.json`, and an `unresolved` row "confirmation of the two quantity-field drafts" handed to the person |
| L2 | `ARM/evidence/place-answer-case-TC-008.json` | place `case-TC-008`, answer `bug`, expectation `requirement` R-3 (quote = register text), capture `settle-case-TC-008/a1/008-look-main.txt`, dispatch analyst-1 |
| L3 | `ARM/work/triage.json` (whole list: TC-009 rows + TC-005 TEST_BUG; grep `TC-008` = 0 hits; control: grep `TC-009#` hits `:6,15,...`) | the final triage holds NO `TC-008#obs1` row |
| L4 | `ARM/state/migration/stale-triage-7b2b5f8638725cec.json:1-14` | that row was ARCHIVED by `finalize_task.refresh`, reason "not bound to current failure" (TC-008 has no run-report target: `ARM/work/run-report.json` `manual_checks` holds only TC-009, `:7897-7900`; grep `TC-008` over `ARM/work/run-report.json` = 0, control `TC-009` hits) |
| L5 | `ARM/work/bug-drafts/qty-input-product-page.json:9` | its `walk` receipt cites the standing place record; by `reproduction_problems` the receipt is void (`_app_bug_problem` -> "no APP_BUG triage row"; `_current_red_problem` -> "not known"), so `confirmation_of` = `unconfirmed` (READ, not executed) — card 1 "found, unconfirmed draft" |
| L6 | `ARM/evidence/place-answer-draft-qty-input-cart-page.json` | analyst-2 answered `bug`, expectation R-3, seen quote `spinbutton "Quantity": "1"`; the draft's own receipt says "The typed 13 was not reproduced from start 3" (`ARM/work/bug-drafts/qty-input-cart-page.json:34`) — card 3/23: the symptom was NOT reproduced, the answer still says bug |
| L7 | `ARM/work/bug-drafts/qty-input-cart-page.json:3-6,17-19` | the cart draft carries `requirements: [R-3, R-11]`; the "PUT 400, no message" part rests on R-11 |
| L8 | `ARM/work/requirements-register.md:5,15,24` | `by_source: {story 5, ac 3, derived 5}`; R-3 `ac`; R-11 `derived` (`aspect:failure and error paths`, observable `current-code:...cartService.ts:33`) — card 4: the expectation the factory derived rode into a bug draft through a SECOND R the answer never cited (the answer cited R-3) |
| L9 | `blind-eval.md:23` | "сообщения нет" contradicts card 4 (there is a toast): the observation of an ABSENCE was wrong |
| L10 | `ARM/evidence/place-answer-*.json` (5 files) | the analyst DID answer places (req-R-2, req-R-5, case-TC-010 `not_a_bug`; case-TC-008, draft-cart `bug`); S7 never closed (FV1-22 loop), so `s7_close_places` never ran: no gap line was written |

Losses, by class: (A) a place-born draft (a case the runner did not run, walked by the analyst) can never reach
`reproduced_by_factory`: the two draft-wide facts need a run-report target that does not exist by construction, and
`finalize_task` archives the analyst's own triage row for it (L1-L5). (B) A `bug` answer's expectation check reads only the ONE
R the answer cites, not the other Rs its draft names; a factory-derived R rides in (L7-L8). (C) Judgment: a `bug` answer on a
walk that did not show the symptom (L6); an absence observed once and written as fact (L9). (D) S7 never closed, so nothing
turned the unsettled places into gaps (L10) — FV1-22's class, fixed there.

-----------------------------------------------------------------------------------------------------------------------------

## 1. Package header (designer rule 1; CLAUDE.md rule 10; P27, AR-29)

### 1.1 AR-n touched, how kept, the change check in the DoD

| AR | card | how kept | DoD check |
|---|---|---|---|
| AR-13 | K1, K2 | the step stays read ONLY by `bug_records.confirmation_of`; "which Rs a draft names" ONLY by `bug_records.draft_requirements`; "is this R inferred" ONLY by the NEW `place_answers.inferred_requirements` (its readers: `_requirement_list` and the new draft check); place membership ONLY by `place_of_draft` | grep in DoD (K2): `unconfirmed_requirements(` has no new caller outside `inferred_requirements` |
| AR-1 | K2 | the register sources the factory counts as "inferred" are a data row (`references/place-answers.json` `inferred_sources`, default `["derived", "assumption"]`), never a list in code | row K2-d |
| AR-22 | K2 | producer (the data row) and reader (`inferred_requirements`) in one commit | K2 DoD |
| AR-26 | K2 | the unit stays the register requirement; a source is read per R | rows K2-a..c |
| AR-28 / FR-59 | K1, K2 | an unreadable report, register or question list never lifts a draft and never grounds a bug (error direction DOWN) | rows K1-e, K2-f |
| AR-29 / P27 | all | code checks joins and presence (a target exists, an R's source cell, an oracle question stands); bug / not a bug / question stays the analyst's word, accepted by the scribe (`s7_places_scribe_line`) | critic question 11 |
| AR-10 / FR-38 | K2 | the new refusal is told before the work in the ONE brief site `s7_place_lines` | DOC key in K2 DoD |
| AR-27 | (F-2) | an unsettled draft reaches the report under its place as a gap — today's `close_unsettled`; the report-side reading is fork F-2, not drafted | — |
| AR-19 | K1 | the walk receipt is read the same for every place source (open target, register, draft, new) | row K1-c |

### 1.2 Checks added or altered: owner and census class

| check | where | owner | census class |
|---|---|---|---|
| a `walk` receipt of a draft with no run target needs no APP_BUG row and no red-now fact (ALTERED: an exemption) | `bug_records.reproduction_problems` (K1) | data (code) — the analyst's judgment is the place answer, accepted by the scribe | shape (join) |
| a `bug` answer whose draft names an inferred R is refused unless the draft's `oracle` question stands (NEW) | `place_answers._answer_lines` via `_inferred_draft_list` (K2) | data (code); "is it a bug" stays judgment | shape (join) |
| a `bug` answer citing an inferred R is refused (ALTERED: the set widens from `unconfirmed_requirements` to `inferred_requirements`) | `place_answers._requirement_list` (K2) | data (code) | shape (join) |
| bug / not a bug / question; whether a walk reproduced the symptom | the analyst (K5 charter), accepted by the scribe (tier above) | judgment | — |
| a requirement-silent place | the person who decides (P20), through the question line `close_unsettled`/`_line_for` already write | intent | — |

Census: K1 and K2 change raising units of existing checks; if `test_judgment_census.py` (as `--witness-for` prints it) names a
row, the builder updates it in the same commit and names it (AR-20: a raise is named in the verdict).

-----------------------------------------------------------------------------------------------------------------------------

## 2. Instance map (completeness criterion)

| instance | class | card |
|---|---|---|
| (б) card 1: product-page draft found but "unconfirmed" | A (L1-L5) | K1 |
| (б) card 3/23: cart "3 -> 13" not reproduced on the second pass, answer still `bug`, draft stays | C (L6) | K5 (charter); the scribe's acceptance is the tier-above check (no code: AR-29); not covered by code — why: whether a walk reproduced a symptom is meaning |
| (в) card 4: "PUT 400, no message" on an inferred expectation, no question | B (L7-L8) | K2 |
| (в) card 4: "no message" was a wrong observation (a toast) | C (L9) | K5 (analyst and runner lines on observing an absence); the walker's mechanics are out of scope |
| (в) card 2: "erase, type 3 -> 13" on the product page, "under question" | C | not covered — why: the evaluator itself could not classify it (`blind-eval.md:78`); K5's start-state line and K2 apply if its draft names an inferred R |
| S7 never closed, places never gapped (L10) | D | FV1-22 (accepted); no card |
| "the draft stays 'not confirmed' to the report" | report reading | fork F-2 (not drafted: §9) |

-----------------------------------------------------------------------------------------------------------------------------

## 3. Cards

Common to every card:
- given: this spec; `PKG/design/factory-rules.md` WHOLE; `plans/builder-rules.md`; `docs/TESTING.md`; `PKG/design/architecture.md`
  (rows of §1.1); `PKG/scripts/slow_tests.json`; `PKG/scripts/tests/test-layers.json`; the owned files as they stand in the worktree.
- non-goals (all): FV1-25 (the automator's failing test), FV1-20, stage critics, the walker's mechanics (`walk_session.py`,
  `manual_capture.py`), `finalize_task.py` (its binding stays: fork F-4), `s7_close_places`/`close_unsettled` behaviour, the S8
  filing and report readers (F-2), any new test FILE, any edit or run of a quarantined file, any local run of a `slow_tests.json`
  file (named "judged by CI"), CI runs, mutation runs (builder-rules 7b, PROJECT.md «Командная работа» п. 13); hot files
  `story_run.py`, `controller.py`, `hooklib.py`, `stage_guard.py`, `gate_preflight.py`.
- handoff: builder report per `.claude/agents/builder.md` rule 7, verbatim witness, FR pass over sections A-G.
- witness: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the card's owns>` and every non-slow
  file it prints; a slow file it prints is named for CI; "no scenario or keep row covers X" is a report line, never a new file.

### K1 — a place-born draft is lifted by its walk  [builder -> critic]

owns (worktree `fv1-24-k1` from origin/main):
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k1\ai-packages\qa-factory\scripts\bug_records.py (`reproduction_problems` and `_walk_has_no_run` only; NEW helper `_no_run_target` beside `_walk_has_no_run`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k1\ai-packages\qa-factory\scripts\tests\<the keep file `--witness-for bug_records.py` prints that holds the walk-receipt table; expected `test_walk_receipt.py`> (new rows in its existing parameterised walk-receipt function only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k1\ai-packages\qa-factory\changelog.d\fv1-24-place-born-draft-walk.md (new)

What to change:
1. NEW `_no_run_target(draft, report) -> bool`: True ONLY when the report is a readable non-empty dict AND the draft's triage
   instance (`draft_triage_key(draft)[0]`) is non-empty AND it is NOT a key of `C.current_instance_results(report)` AND NOT a
   name in any `C.triage_failures(report)[0]` entry's `names`. Any exception -> False. Docstring: "the draft speaks for no
   execution of this run (a place the analyst walked: a case the runner did not run, a register contradiction); its walk is
   its only evidence".
2. `_walk_has_no_run`: return True also when `_no_run_target(draft, report)` (the red-now fact is then skipped for a `walk`).
3. `reproduction_problems`, the `walk_wide` line: the APP_BUG fact is skipped for a code-reading draft (today) OR when
   `_no_run_target(draft, report)`. Nothing else changes; non-walk entries keep BOTH facts (`wide`) exactly as today.
4. Changelog: one paragraph naming the archived-row cause (`finalize_task` binding) and that the walk record is now the step.

Edges (each with its invariant):
- K1-a A draft whose triage instance IS a current failure or a current result (a red test, a runner observation) keeps both
  facts. INVARIANT: a draft that speaks for a run failure is never lifted while that failure is green, absent from its attempt,
  or lacks an APP_BUG row.
- K1-b A non-walk entry (`fresh_data_rerun`, `own_script`) on a place-born draft keeps both facts. INVARIANT: only a standing
  walk record (`_walk_receipt_problem`: writer, answer `bug`, this place, `answer_problems` passing NOW) lifts it.
- K1-c Every place source alike (open target, register, draft, `new-`). INVARIANT: no source is read by name (AR-1, P31).
- K1-d Empty/absent triage instance (`triage_ref` missing): `_no_run_target` False -> today's behaviour (APP_BUG fact fails).
  INVARIANT: a draft that names no instance is not "no run" by default (FR-59). The door stays the place's `observation`
  field (`place_of_draft` (2b)); see fork F-5.
- K1-e Report unreadable or `{}`: False -> today's `no_report` problem. INVARIANT: an unknown never lifts (AR-28).
- POSITIONAL: the exemption sits inside the `has_walk` branch only. INVARIANT: the `wide and not has_walk` early return
  (`:1014-1015`) is unchanged, so no non-walk draft gains a road.
- TEMPORAL: works on today's stories with no migration (the archived row is not needed). A story like ARM: the product-page
  draft would read `reproduced_by_factory` after the commit IF its walk record still stands NOW (capture hash, quote, R-3
  source) — not executed (§9). Before the commit: today's `unconfirmed`. The move that changes it: this commit.
- Reused function in a more consequential role (`current_instance_results`/`triage_failures` membership from "advice which
  facts apply" to "the gate that drops two facts"): it may err only toward "is a target" (keep the facts). Adversarial inputs
  that must stay on the safe side: an instance id spelled differently from the report's (`[chromium]` suffix: use
  `C.same_id`/the report's own spelling reader if `triage_failures` names carry spellings — the builder reads
  `C.id_spellings` and, if a draft id matches any spelling of a target, it IS a target); a report holding the case in a
  later attempt; an observation `#sur-overflow` instance.

Test rows (one parameterised table, ids name the case): `K1 place-born walk lifts` (instance absent from report, valid walk
record -> `reproduced_by_factory`, kinds `[walk]`); `K1 red test walk keeps facts` (instance is a current failure, no APP_BUG
row -> unconfirmed `no APP_BUG triage row`); `K1 green now keeps facts` (current result passed -> `the test is green now`);
`K1 non-walk on place-born` (`fresh_data_rerun` only -> unconfirmed); `K1 no triage_ref` (-> unconfirmed); `K1 report
unreadable` (-> unconfirmed); `K1 spelling variant is a target`.
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/bug_records.py`
and every non-slow file it prints green; rows above green; `architecture: AR-13, AR-19, AR-28, AR-29 -- the walk record is the
step of a draft with no run target; one step reader; unknown never lifts`; `judgment: none (a join)`.
siblings: `place_answers.settled_answer` (reads `confirmation_of`: no edit, gains the lift); `investigation.unresolved_targets`
(iv) (reads `settled_answer`: no edit); gate B `gate_preflight.check_bug_drafts` (hot file, not edited — reads the same
reader); `finalize_task.refresh` binding (unchanged, F-4).

### K2 — a draft on an inferred expectation cannot be a bug; that part is a question  [builder -> critic]

owns (worktree `fv1-24-k2`):
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k2\ai-packages\qa-factory\scripts\place_answers.py (NEW `inferred_requirements`, NEW `_inferred_draft_list`; `_requirement_list`: the `unconfirmed_requirements` call only; `_answer_lines`: one call after `_bug_list`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k2\ai-packages\qa-factory\references\place-answers.json (NEW key `inferred_sources`; NEW `line_texts` entry `inferred_in_draft`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k2\ai-packages\qa-factory\scripts\driver_dispatch.py (`s7_place_lines`: one sentence appended to the answer-rules line only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k2\ai-packages\qa-factory\scripts\tests\<the keep file `--witness-for place_answers.py` prints that holds the answer-refusal table; expected `test_place_answers.py`> (new rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k2\ai-packages\qa-factory\changelog.d\fv1-24-inferred-expectation-question.md (new)

What to change (written on fork F-3 (a); under F-3 (b) item 1 drops the source-cell part):
1. NEW `inferred_requirements(task) -> tuple[set, str]`: `(ids, why)`. Reads the register through `_register(task)`; `ids` =
   `C.unconfirmed_requirements(text, _questions(task))` UNION the R of every register row whose `source` cell (read through
   `C.register_rows`; the builder confirms the key name on the row dict) is in `_data()["inferred_sources"]` (strings,
   compared stripped and lower-case). A register that cannot be read -> `(set(), why)` and the CALLERS treat a non-empty
   `why` as "refused" (error direction DOWN). No register file -> `(set(), "")`. Docstring: "the requirements whose expectation
   the factory inferred and no person confirmed; THE reader (AR-13)".
2. `_requirement_list`: the `rid in C.unconfirmed_requirements(...)` test becomes `rid in inferred_requirements(task)[0]`;
   the refusal text says "{rid} is an expectation the factory inferred (no confirmed source)" with the same doors.
3. NEW `_inferred_draft_list(task, record) -> list` (called from `_answer_lines` only for `answer == "bug"` and `place_ok`, after
   `_bug_list`, only when `_bug_list` returned nothing): read the named draft (the same listing `_bug_list` uses);
   `named = set(bug_records.draft_requirements(draft))`; `ids, why = inferred_requirements(task)`; `why` -> one refusal "the
   register cannot be read, so the draft's requirements cannot be checked" with door "answer `requirement_silent` or
   `impossible`"; `hit = sorted(named & ids)`; when `hit` and the draft's `oracle` does not stand
   (`bug_records._oracle_problems(task, {"oracle": draft.get("oracle")}, "", _questions(task), None)` non-empty, or no `oracle`
   with a `question`), one refusal from `line_texts.inferred_in_draft` formatted with the ids: "the draft rests on {ids}, an
   expectation the factory inferred and no person confirmed. Door: put the part that rests on it in its own place `new-<slug>`
   answered `requirement_silent` with your question and take {ids} out of the draft's `requirements`, `violates` and
   `expected`; or cite the person's answered question in the draft's `oracle` (`question`, `quote`)".
4. `place-answers.json`: `"inferred_sources": ["derived", "assumption"]` with a `note` sentence; the `inferred_in_draft` text.
5. `s7_place_lines`, the answer-rules line (`:4057-4061`): append "A `bug` whose draft names a requirement the factory inferred
   (register source derived or assumption, or one no source confirms) is refused unless the draft's `oracle` cites the
   person's answered question; otherwise that part is a `requirement_silent` place of its own." (FR-38, AR-10.)

Edges:
- K2-a Draft names only confirmed Rs (`ac`, `story`) -> unchanged. INVARIANT: no confirmed bug is refused by this check.
- K2-b Draft names a confirmed R AND an inferred R (ARM cart: R-3 + R-11) -> refused (the L7-L8 case). INVARIANT: an expectation
  the factory inferred never rides into a bug beside a confirmed one.
- K2-c Draft names an inferred R and its `oracle.question` is answered and quoted -> accepted. INVARIANT: the person's word
  grounds the expectation (P20); code checks the join, never the meaning.
- K2-d `inferred_sources` absent or not a list of strings -> default `["derived", "assumption"]` (said once on stderr);
  `[]` -> only `unconfirmed_requirements`. INVARIANT: a broken data row never widens what counts as confirmed.
- K2-e Draft names no R at all (`draft_requirements` -> `[]`) -> nothing from this check (the answer's own expectation
  check stands). INVARIANT: this check adds refusals only.
- K2-f Register or question list unreadable -> refused with the door above. INVARIANT: an unknown never grounds a bug (AR-28).
- K2-g Conflicting pair (resolved): `_requirement_list` (the answer's cited R) and `_inferred_draft_list` (the draft's Rs)
  may both refuse; both lines are printed, each with its door.
- POSITIONAL: after `_bug_list` and only when it passed. INVARIANT: a draft of another place is refused for that reason first,
  never read for its Rs.
- TEMPORAL: `answer_problems` is re-run NOW by `settled_answer` (`:650`) and `_walk_receipt_problem` (`bug_records.py:935`).
  A `bug` record written before this commit on a draft naming an inferred R reads `invalid` after it; at the next S7 close
  `close_unsettled` writes its gap (the place is NOT silently settled). Before the commit: today's reading. The move: this
  commit. Stated in the changelog. This is the safe direction (a lifted step can drop back to `unconfirmed`).
- Adversarial (input written by an LLM role): `requirements: "R-11"` (a string), `requirements: [R-11, R-11]`, an R in
  `expected` prose only, lower-case `r-11`, a draft id with `..`. `draft_requirements` decides what is named (its own reading);
  `expected` prose is NOT read (FR-12) — the refusal door asks to remove it, the check reads only the fields the reader reads.

Test rows (one parameterised table): `K2 confirmed only passes`; `K2 confirmed plus derived refused` (ARM-shaped fixture:
R-3 `ac`, R-11 `derived`); `K2 derived with answered oracle passes`; `K2 derived with unanswered oracle refused`;
`K2 cited derived refused` (`_requirement_list`); `K2 assumption refused`; `K2 sources row broken uses default`; `K2 sources
row empty`; `K2 register unreadable refused`; `K2 draft names no R`; `K2 requirements as string`.
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/place_answers.py ai-packages/qa-factory/references/place-answers.json ai-packages/qa-factory/scripts/driver_dispatch.py`
and every non-slow file it prints green; DOC key run on `driver_dispatch.py` (key verbatim: "is refused unless the draft's
`oracle` cites the person's answered question"; script in full; negative control); grep `git -C <worktree> grep -n
"unconfirmed_requirements(" -- ai-packages/qa-factory/scripts/place_answers.py` shows only `inferred_requirements`;
`python -B ai-packages/qa-factory/scripts/selftest.py --lang` green. `architecture: AR-1, AR-10, AR-13, AR-22, AR-26, AR-28,
AR-29 -- ...`; `judgment: none (joins); bug vs question stays the analyst's, accepted by the scribe`.
siblings: gate B `gate_preflight.check_bug_drafts` and S8 filing (do they let a draft on an inferred R through as a bug? not
read — queue line, §8); triage rows APP_BUG on an inferred R (the triage verdict is not a draft step; F-3 cost line).

### K3 — (reserved for fork F-1 (b); not drafted)

### K5 — charter lines (experience of a tester)  [builder -> critic or Lead; AFTER stage-critics B3]

owns (worktree `fv1-24-k5`, from main after B3 merges — `очередь: stage-critics/B3 -> FV1-24/K5`, same file and lines, spec
`20261113-stage-critics-s2-s3-removed-spec.md:833-845`, `:940`):
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k5\ai-packages\qa-factory\agents\qa-failure-analyst.md (section "Where bugs hide": one bullet appended; section "Techniques": the bullet "Find out the truth on the page" only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k5\ai-packages\qa-factory\agents\qa-runner.md (section "Where bugs hide": one bullet appended)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k5\ai-packages\qa-factory\references\role-load.json (the two roles' rows, as the witness prints)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-24-k5\ai-packages\qa-factory\design\role-rules.json (rows whose carrier line changes, if any)

Text (verbatim keys; each line is craft, not form procedure; the form fields stay on the key page and in the brief):
1. Analyst, "Find out the truth on the page", append: "A walk that did not show the symptom is not a bug for that symptom: try the
   other starts first; if it still does not show, say not a bug with what you saw, or ask the person. One draft carries one
   expectation source: a part that rests on what the factory inferred goes to the person as a question, never into the bug."
2. Analyst, "Where bugs hide", new bullet: "**An absence seen once.** \"No message\" after an action is a claim like any other: a
   message can come and go before the look. Look right after the action and once more, and quote what was on the page."
3. Runner, "Where bugs hide", new bullet: "**An absence seen once.** A message that is not in one look may have come and gone;
   look right after the action and again before writing that nothing was shown."
Edges: no line restates a form field or a refusal (P27); the B3 lines (`:27`, `:28`, `:51`, `:76`) are untouched; the role-load
ratchet raise, if printed, is named in the verdict (AR-20).
DoD: DOC-DISPATCH key-presence run (keys verbatim: "A walk that did not show the symptom is not a bug for that symptom", "One
draft carries one expectation source", "An absence seen once" in both charters; script in full; negative control), plus
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/agents/qa-failure-analyst.md ai-packages/qa-factory/agents/qa-runner.md ai-packages/qa-factory/references/role-load.json ai-packages/qa-factory/design/role-rules.json`
and the non-slow files it prints; `selftest.py --lang`. `architecture: AR-10, AR-29 -- craft told before the work; judgment
stays the role's`.

-----------------------------------------------------------------------------------------------------------------------------

## 4. The road of "requirement is silent" (scope item; mostly EXISTS)

- The analyst answers `requirement_silent` with `question` (refused without it, `place_answers.py:505-506`); `write` lands an
  `unresolved_question` line with `owner_role` = "the person who decides the story's expected behaviour" and
  `oracle_status: owner_question` (`_line_for` `:837-839`). K2 adds the second entrance: an inferred part refused as a bug
  is told to become exactly such a place.
- To the person: the register line is what gate B and the report read (the investigation module's comment
  `investigation.py:51-52`: lines reach the report and gate B, words a person may read). Whether the question is put to the
  person through `references/human-questions.md` (AR-16) at gate B or only listed in the report: NOT read (§9). No card here
  changes that road; if the reading shows a second road, it is a P31 residual (fork F-6).
- Into the report as a GAP until answered: an unsettled place gets `coverage_gap` at the S7 close (`close_unsettled`); a
  `requirement_silent` place is an open question line. P21: open questions and gaps are delivery facts, read by the existing
  report code (not changed here).

## 5. FV1-25's carrier (named, not designed)

FV1-25 reads a manual-pass bug through: the place record `evidence/place-answer-<place id>.json` (answer `bug`,
`expectation.source/id/quote`, `seen.capture/quote`) as judged by `place_answers.settled_answer(task, place)` == `settled`
(THE predicate), and the draft `work/bug-drafts/<file>.json` named by its `draft`, whose step `bug_records.confirmation_of`
reads `reproduced_by_factory` with kind `walk` (after K1, also for place-born drafts). It never reads a draft's literal
`confirmation` word.

## 6. Order and parallelism

- K1 ∥ K2: disjoint files (K1 `bug_records.py`; K2 `place_answers.py`, `place-answers.json`, `driver_dispatch.s7_place_lines`).
  K2 calls `bug_records.draft_requirements` and `_oracle_problems` (read, unchanged by K1).
- K5 after stage-critics B3 (same charter lines region); FV1-25 also touches the analyst charter (`очередь: B3 -> FV1-24/K5 ->
  FV1-25`, or the later merges main and re-measures `role-load.json`).
- `driver_dispatch.py`: FV1-22 N2/N3 own `finish`, `handoff_ladder`; FV1-3 owns `take_question_answer` — disjoint from
  `s7_place_lines`.
- One critic pass for the topic (R13-g): K1 + K2 (+ K5 if the Lead routes it to critic).
- Critic on plan: required before code (PROJECT.md package change item 6: K1 and K2 change what a receipt and a bug answer
  MEAN; premise measured in §0.2).

## 7. Four questions (rule 10), per mechanism

K1 (walk lifts a place-born draft): (a) cost: one membership read per walk entry; paid by code. (c) detector: rows K1-a..e;
calibration check 41 (judgment census) for the altered unit; live row §7b. (d) on the path: `confirmation_of` is called by
every reader of the step (report, gate B, `settled_answer`), so the rule is met wherever the step is read; meaning stays with
the scribe.
K2 (inferred expectation refused as a bug): (a) cost: more `requirement_silent` questions — every bug resting on a derived norm
becomes a question unless the person confirmed it (ARM: 5 of 13 Rs derived, `requirements-register.md:5`); paid by the person's
attention at gate B, saved in false bugs. (c) detector: rows K2-a..g; calibration check 41; live row §7b. (d) on the path:
`write` refuses before anything is written; `settled_answer` re-judges NOW.
K5 (charter lines): (a) a few lines of role context (role-load measured by the witness). (c) detector: the live row; critic
standing question 10/11. (d) on discipline alone — explicit line: the leak detector is the live-runs row and the blind
comparison's row (б).

Axes (current map, axes 1-37):
axis 1: n/a — no policy/role/journal file changes. axis 2: n/a — no exam instrument. axis 3: queued — release copy at the next
release (normal path). axis 4: covered — no FR changes; no debt row; P20/P26 kept. axis 5: covered — S7 is the only stage
reading place answers; S6 runner charter line is the twin of the analyst's absence line (K5). axis 6: n/a — no measurer edits.
axis 7: n/a. axis 8: n/a — paths unchanged. axis 9: n/a. axis 10: n/a. axis 11: n/a. axis 12: covered — node row FV1-24
exists; status moves with the journal. axis 13: covered — K2 edits the one brief site `s7_place_lines`. axis 14: n/a.
axis 15: n/a. axis 16: covered — K2 reads data through `_data()`/`hooklib.read_json`. axis 17: n/a — no detector verdict shape.
axis 18: covered — census / role-load raises named (AR-20). axis 19: n/a. axis 20: n/a. axis 21: covered — register cells read
only through `C.register_rows`. axis 22: n/a. axis 23: n/a. axis 24: n/a — run rows read through existing readers. axis 25:
n/a. axis 26: n/a. axis 27: n/a. axis 28: covered — the rule reaches the role in `s7_place_lines` (K2 item 5). axis 29: n/a —
no new jsonl writer. axis 30: n/a. axis 31: covered — charter lines are craft; form rules stay on the key page (K5). axis 32:
covered — §1.2 census classes; judgment stays the analyst's, accepted by the scribe. axis 33: n/a. axis 34: covered — K1/K2
read no language, project or case name; one road for every place source. axis 35: n/a. axis 36: n/a. axis 37: n/a — no
repeat stop added.

### 7b. FR-33 live proof row (goes to `live-runs` by the batch's close rule)

"A story where the runner leaves a manual case unrun and the analyst walks it: the draft's step reads `reproduced_by_factory`
(walk) in the report; a draft that names a register `derived` requirement with no answered question is refused as a bug and
appears as the person's question (`unresolved_question`), not as a bug." Plan it with the FV1-22 rows (one stand run).

-----------------------------------------------------------------------------------------------------------------------------

## 8. Forks (returned; none decided here)

- F-1 (Lead; owner if it changes P1's reading) — the exit rule when places stay unanswered after the analyst's finish.
  (a) RECOMMENDED: today's rule kept — the brief says an answer is owed (FR-38), every unsettled place becomes a named
  `coverage_gap` at the S7 close (`close_unsettled`), never a barrier (owner 13.11: S6/S7 acceptance never a barrier; P1).
  Executable now; nothing to build. (b) one bounded resume: `Driver.s7_open_work` returns `OpenWork("places_unanswered")`
  once per analyst life when `place_answers.unsettled` holds a place in state `open` (no record), then the close gaps the rest
  (the finding's own test line "S7 не закрывается без вердикта"). Cost: one extra analyst turn per run with unanswered
  places; needs a recon of how an `OpenWork` from `s7_open_work` resumes the SAME analyst (not read), then card K3.
- F-2 (Lead; may need the owner: changes what a person reads) — how the report/S8 treat a draft whose place is unsettled at
  the close. (a) RECOMMENDED: the bug reporter files (and the report counts as a bug) only a draft whose place is settled
  `bug` or whose step is not `unconfirmed`; an unsettled draft appears only as its place's gap ("a suspected bug the factory
  could not settle: <why>"). (b) today: the draft is filed with the words "unconfirmed, nobody reproduced it" AND its gap
  line exists. Not drafted: the S8 filing and report readers were not read (§9). What stays executable before the answer:
  K1, K2, K5.
- F-3 (Lead; owner if the cost of questions matters) — what "inferred by the factory" means for the bug gate. (a) RECOMMENDED:
  `unconfirmed_requirements` UNION register rows whose source is in the data row `inferred_sources` (`derived`,
  `assumption`), unless the person's answered question is the draft's oracle — P20/P26 literal; cost: more questions (ARM: 5
  of 13 Rs derived). (b) today's set only (code-sourced / implementation-only after the cutoff); whether ARM's R-11 is in that
  set was NOT executed. K2 is written on (a); under (b) only items 2-3 and 5 remain (the draft-side check still closes L7).
- F-4 (Lead) — K1 vs keeping the analyst's triage row. (a) RECOMMENDED: K1 (the walk record is the evidence of a place-born
  draft; `finalize_task`'s binding stays one rule). (b) `finalize_task.refresh` keeps analyst rows whose instance names a
  place the analyst answered — a second binding rule (AR-13 risk) and the red-now fact would still fail.
- F-5 (Lead) — the triage key of a place-born draft. (a) RECOMMENDED: keep `triage_ref` as the analyst writes it (K1 reads
  "no run target"); (b) the draft names its place in `observation` and K1 keys on `place_of_draft` sources — cleaner, but
  `place_of_draft` would become a gate input (advice -> gate) and old drafts carry no `observation`.
- F-6 (Lead) — whether a `requirement_silent` line reaches the person through `human-questions.md` (AR-16) at gate B or only
  as a report line: not read; if two roads exist, a P31 residual node with owns and a test.

Small choices closed by the designer: worktree names `fv1-24-k1/-k2/-k5`; helper names `_no_run_target`,
`inferred_requirements`, `_inferred_draft_list`; the data key `inferred_sources` in `place-answers.json` (the existing home of
place-answer vocabulary); `expected` prose not read (FR-12); K3 number reserved for F-1 (b).

Analogs noticed (not widened): gate B `gate_preflight.check_bug_drafts` and the S8 bug filing read drafts — whether they let a
draft on an inferred R through is unread (queue with F-2); triage APP_BUG rows may cite an inferred R in `reason`
(`ARM/work/triage.json:11` cites R-11) — triage is not a step, so K2 does not reach it; the scribe charter (B3's lines) could
name "a `bug` answer whose seen quote does not show the symptom" as a return reason — judgment of the tier above, a sibling for
B3/FV1-24 K5 if the Lead wants it.

## 9. What I did NOT establish

- Nothing was EXECUTED (no shell): `confirmation_of` on the ARM drafts (L5 reasoned from code), whether ARM's place records
  still stand NOW (capture hashes), whether R-11 is in `C.unconfirmed_requirements` of the ARM register (cutoff and
  `code_sourced_requirements` not run), the key name of a row's source cell in `C.register_rows`.
- How the S8 bug reporter, `report_facts`, `delivery_summary` and gate B present an `unconfirmed` draft (F-2 not drafted).
- Whether a `requirement_silent` register line is asked of the person through `human-questions.md` at gate B (F-6).
- How an `OpenWork` from `s7_open_work` resumes the analyst (F-1 (b) / K3).
- `references/stage-joints.json` S6/S7 rows and `design/state-exits.md` were not read (budget); no card edits a state or a
  joint, so no exit row is owed by this draft — the critic on plan should confirm.
- The exact keep test file names for K1/K2 rows (`test_walk_receipt.py`, `test_place_answers.py` are the likely ones; the
  builder takes the file `--witness-for` prints).
- The S7 prompt of the ARM run (place lines are in the session prompt, not in `work/briefs/`; the briefs carry none — not a
  proof of absence).

## 10. Reading trail

Forge (read-main): finding (whole); `batch-1-live-run-fvf.md` grep FV1-22/24/25 (`:53-56,87-94`); FV1-22 re-cut spec (whole);
stage-critics spec `:800-959`; plan `20261113-plan-fabrika-ne-huzhe-agenta.md` grep (`:119` K5 row only; no FV1-24 text);
amendment grep (no FV1-24 hit; control: the grep hit its own title line); `SIBLING_MAP.md` axis headings.
Package: `agents/qa-failure-analyst.md` (whole), `agents/qa-runner.md` (whole); `scripts/place_answers.py` (whole);
`scripts/investigation.py:1-230` + grep; `scripts/bug_records.py:800-1180`, grep `draft_requirements` `:1766-1774`;
`scripts/driver_dispatch.py:700-730,4015-4189`; `scripts/driver_stage_s7.py:40-190,270-344,500-635`;
`scripts/driver_stage_plan.py:897-946`; `scripts/finalize_task.py:690-758`; `scripts/exit_gate.py:900-1019`; grep `place_answers`
(non-test), `triage_has_no_repair`, `#sur-`, `DRAFT_REQUIREMENT_FIELDS`, `unconfirmed_requirements` (`contract.py:1443-1453`),
`question_register.py` defs.
Experiments: `runs/blind-eval.md:1-86`; `runs/factory-out/work/bug-drafts/*.json` (both).
ARM: `evidence/place-answer-*.json` (glob 5; read 4); `work/requirements-register.md` grep; `work/triage.json:1-40,195-274` +
grep; `work/run-report.json` grep (`manual_checks` `:7897`); `work/handoffs/` glob, `S7-qa-failure-analyst-1.yaml` (whole),
`-2.yaml` grep; `work/briefs/` grep (controls in-line); `state/migration/` grep + `stale-triage-7b2b5f8638725cec.json` (whole).
Searches with controls: TC-008 absent from `triage.json` (control TC-009 hits); TC-008 absent from `run-report.json` (control
TC-009 hits); "Places" absent from S7 briefs (control: `settle` hits the same files — and the reason is that the lines go into
the prompt, `driver_dispatch.py:713-724`).
Needed beyond the manifest: the ARM copy `C:\QAFactory\mybooks-stand\arm-factory\...\LOCAL-1` and the root-checkout
`experiments/.../runs/` (gitignored, absent from read-main).
