# Critic on PLAN — FV1-6 re-cut (S4 only), spec `docs/tasks/specs/20261114-fv1-6-s4-only-spec.md`

Reviewer: critic (Opus), 14.11.2026. One pass. Facts checked on `C:\QAFactory\forge-repo\.claude\worktrees\read-main` (origin/main);
every `file:line` below is under `ai-packages/qa-factory/scripts/` on read-main unless another path is given.

F1 is DECIDED by the owner (14.11.2026, «ок» to (a), relayed by the coordinator during this review): code asks the closed, priced
question itself at S4 round exhaustion, on the S5/S7 road, one road for all stages, no paid conductor call; the conductor only for
free words and unreadable states. The plan is judged on (a) as decided. Option (b) is no longer weighed.

**Verdict: NEEDS WORK (fit_with_fixes). 5 blocking findings (B1-B5) and 11 amendments (A1-A11).** The direction is right. F2 (a),
F3 (a), F4 (a), F6 (a) and F7 (a) hold, with the amendments below. F5 (a) does not hold; take F5 (b) (B4). The old draft's
root-cause finding (a conductor `rework` refused beside the running critic, old verdict B2) does not come back. Under the decided F1
(a) the `round` answer only records the passes. The designer's round starts after the critic has been accepted with
`cases_in_repair`, so no dispatch runs beside a running critic. Every blocker is a spec edit the Lead can make as a continuation of
this draft.

---

## K1. Facts (spot-checks)

| §2 claim | read-main | verdict |
|---|---|---|
| `stage_S4` loop, `last_round` (`driver_stage_plan.py:526-554`, `:537-539`) | `:537-539` exactly | holds |
| `s4_critic_completion` order: no dispatch -> seam; unknown word -> seam; record written; verdict not concerns/review -> None; last round -> seam | `:806-821`. A guard the spec does not mention: `if not self.stage_acceptor("S4"): return None` at `:817-818` | holds; see A8 |
| `stage_review_exhausted`, `person_closes`, the conductor and the fallback (`:691-747`) | `:691-747` exactly | holds |
| the S4 digest-row state word | the charter says `reject` (`agents/qa-case-critic.md:128`). The code compares `rejected` (`:829`). `role_digest` accepts every word in `ROW_STATES` (`role_digest.py:94-97`), which includes `contract.CRITIC_VERDICTS` = `approved`, `approved_with_fixes`, `rejected` (`contract.py:2211`) | §12 is right that the word is in doubt. The consequence is worse than §12 says: see B1 |
| `_answer_repair_limit`, `repair_pass_keys`, `repair_store_name`, `repair_limit_raise` / `_person` | they exist, but at `driver_dispatch.py:3295`, `:3287`, `:3347`, `:3235`, `:3244`, not at the lines the spec gives (`:3216`, `:3207`, `:3267`, `:3156`, `:3165`): a drift of about 79 lines. `waiver.py ... --stage S5` is a literal (`:3326`). `repair_pass_keys` indexes `passes["qa-automator"]` (`:3292`) | names hold, lines are stale (A11). Two hidden S5 literals: see B2 |
| S7's waiver `--stage S5` is correct | S7 reworks dispatch at stage S5 (`driver_stage_s7.py:992`, `:1090`) | so S4 really needs `waiver_stage` (S4 dispatches carry stage S4, and `_passed_by_person(p["stage"])` at `controller.py:5665` filters by stage through `waiver.split_overridden` `waiver.py:210`). No S7 sibling defect |
| the passes exist for S4 | `REPAIR_PAIRS` (`controller.py:702`). `repair_passes` builds both roles' keys with round number n (`controller.py:754-767`, `:751`), and they are carried in the packet (`:2201`) | holds. One key per round, so a second `round` gets a new key and no duplicate override arises |
| `critic_rollcall._read_round` keeps only `approve_with_concerns`, lists all reviewed rows (`:406-433`, `:424-426`) | exactly | holds |
| `s5_plan._file_concerns`: the latest listing round decides (`s5_plan.py:1120-1149`) | exactly. Numbering `number + len(out)` (`:1146`) | holds |
| `report_facts.py` reads no `plan_remarks` / concern | Grep `plan_remarks\|case_concerns\|concern_report`, case-insensitive, over `scripts/*.py`: 13 files, no `report_facts.py`. Positive control from the same call: `brief_pack.py`, `s5_precheck.py`, `manifest_put.py` | holds. Note that `manifest_put.py` also carries `plan_remarks` (the merged store, A2) |
| `controller._passed_by_person` is how the rework passes the cap | `controller.py:2456-2468`, the cap refusal `:5653-5677` | holds |
| no `FINISHING_WHYS` / `asked_why` | not re-grepped (the design under (a) needs neither) | — |

## Blocking findings

### B1. The question's list of rejected cases is read from the wrong carrier, with an over-broad predicate (K1, K4, K6, AR-13, FR-41)

§3.1.2a takes the rows from the DIGEST: every row whose state word is not in `APPROVING_VERDICTS`. There are three defects.

1. **Wrong output on a known input.** A digest row `TC-1 · approved (approve_with_concerns)` (the run-12586 spelling that
   `_row_state` handles, `role_digest.py:159-173`) parses to the state `approved`, because both words are known states and the first
   wins. `approved` is not in `APPROVING_VERDICTS` (`critic_rollcall.py:44`), so the question tells the person "the reviewer still
   rejects TC-1" about a case the reviewer approved. The same happens to `reviewed`, `ok` and `passed`, all of which are row states.
   The rig of `test_repair_route.py:518` uses `TC-1 · ok · reviewed` as an approving row.
2. **There is no "note" in the digest.** A digest row has `reason`, at most 80 characters (`role_digest.py:116`, `:218`). So
   "the reviewer's note whole up to 300 characters", E-N1-10 and rows Q4a/Q4b cannot be built from it.
3. **Two readers of one fact (AR-13).** The person is told which cases go to the test writer (from the digest), but the test writer
   receives N2's list (from the roll-call of the findings file). The two can differ, for example when the digest omits a row. The
   promise in the `go on` option is then false (FR-10).

**Change.** The question reads the roll-call of the current S4 findings file (`self.s4_findings()`), through ONE predicate in
`critic_rollcall` shared with `_read_round`, for example `rejected_rows(rows)`: a `reviewed: yes` row whose `verdict` cell is not
in `APPROVING_VERDICTS`, an unknown word kept as written (E-N2-5's rule). The predicate goes on the receipt-measured round for the
automator, and on `parse_rollcall` of the current file for the question; the receipt is not stamped yet at finish time, which is
S4 of §11 correctly noticed. The note comes from the row's `note`, which makes the 300-character cut real. The digest is not read
for the list. §11 S4 is rewritten accordingly. N1 then depends on N2's predicate, so the order is N2 -> N1 (A9).

### B2. The budget, the passes and the unknown-count state are unspecified, and two S5 literals sit outside N1's owns (K3, K8, FR-59, FR-41)

- `s4_critic_completion(scope, counted, cap, dispatch_id)` carries no budget, yet §3.1.2e needs `passes` and
  `repair_older_controller(..., budget, ...)`. The spec does not say where the budget comes from. The recovery road re-reads it
  (`driver_stage_plan.py:1113-1114`); the live road holds it in `stage_S4` (`:537`). A Sonnet builder will guess.
- The driver's own `repair_passes(budget)` hard-codes `("qa-automator", "qa-code-critic")` (`driver_dispatch.py:3139-3143`). Built
  the way S5 builds it, the S4 `passes` is always None, so the question would always be the older-controller refusal and the road
  never works.
- `repair_older_controller` is worded for S5: "The tests of this step ..." and "controller prepare for S5 qa-automator ..."
  (`:3172-3178`). Reused at S4 it tells the person about tests, not cases (FR-37). Neither function is in N1's owns.
- **The unknown-count state is missing.** When `counted` or `cap` is not an int (an unreadable budget), `last_round` is True
  (`:539`). The new branch then asks a question with "round None+1" and "limit None", and offers `round` with no passes. Today
  that state reaches the seam; S5 maps it to the code `unknown`, offering `debt`/`stop` with no `round` (`driver_dispatch.py:3198-3199`).

**Change.** (a) Name the source: `s4_critic_completion` gains a `budget` argument, which `stage_S4` passes and `completion_for` already
holds; alternatively it calls `budget_or_none("S4", "qa-case-designer", scope)` itself. Say which. (b) `passes` = `budget["passes"]`,
valid when it holds a non-empty string for each role of the S4 pair. It is read in `s4_review_limit` (data, no role list in code
beyond the controller's pair), never through the driver's `repair_passes`. (c) An older controller at S4 gets its own words: give
`repair_older_controller` a stage-aware `said`/`text` and add it to N1's owns with E-N1-13's S5 byte-identity row. (d) A new edge
E-N1-14 for an unknown count. The decided F1 (a) keeps unreadable states on the conductor seam, so the expected answer is today's
seam: `stage_review_exhausted(..., unreadable=True, text="the repair count of the case designer could not be read")`. No number is
printed (FR-41).

### B3. No findings file on the last round: `round` buys a NEW paid critic over unchanged cases, and `go on` carries nothing it promised (K3, t-919 F-1)

`s4_review_limit` never checks `self.s4_findings()`. Trace with no findings file:
1. `round` -> `OpenWork("cases_in_repair")` -> the critic is accepted.
2. `stage_S4`'s new owed condition still requires `self.s4_findings()` (§3.1.4) -> false.
3. It falls through to `run_role("S4", "qa-case-critic")`: a NEW paid critic over unchanged cases. That breaks §3.1.5.

The bought entry never executes, and FR-40 is only escaped because the new critic becomes the newest dispatch. With `go on`, N2 has
no roll-call to carry, so the option's promise is false.

**Change.** First line of `s4_review_limit`: no findings file -> `return False`. This is the t-909 F-3 rule the non-last-round
branch already keeps at `:822-824`: one resume of the critic, who writes the findings. Never the question. Add a test row `F0
no-findings-no-question`.

### B4. F5 (a) is a silent pass decided by code; take F5 (b) (K7, K10, FR-4, FR-59, P27/AR-29, FR-41)

The case: the header says `concerns` (the critic's own request that the designer rework, `qa-case-critic.md:113-114`), yet no row is
read as rejecting. That is a contradiction inside the critic's output, an unknown. F5 (a) has the driver write `--acceptor driver
--verdict accept` with only a printed line. That is code deciding that the stage is closed (P27: code does not decide whether an
obligation is closed), with no person informed (FR-4 stops a silent pass), on an unknown (FR-59).

With the digest reader of §3.1.2a the case is also reachable when the digest simply omits the rejecting rows that the findings
file holds. The quote "named no case it still rejects" would then be false (FR-41), while N2 carries those very rows. F5 (b) is
today's road and costs no code. It is also the cheaper design (K9). It also matches the owner's F1 decision: the conductor handles
unreadable states, and a self-contradicting critic output is one.

**Change.** Take F5 (b). §3.1.2c becomes: the roll-call is readable and no row rejects -> `stage_review_exhausted(..., text="the case
critic sent the cases back on its last round and its roll-call names no case it still rejects")`. E-N1-2 and row E1 are rewritten
to expect the seam. Drop the census line for it.

### B5. N1 turns existing keep rows red that its owns do not cover (K8)

- `test_story_run_refusals.py` `refusal_c2_4_s4_keeps_open_only_when_the_round_will_run`, rows `:3584` ("T18: the last round (counted ==
  cap) -> None") and `:3585` (count/cap not numbers -> None). Both rely on the stubbed `stage_review_exhausted` (`:3568`). The digest
  `TC-1 · rejected` (`:3569`) now raises a `repair_limit` Person instead.
- `test_repair_route.py` `s4_last_round_and_text_from_the_budget`, rows `:570-575` (at and beyond the cap: `complete == [None]`) and
  `:579-581` (an unreadable budget closes). All rely on the seam stub at `:542`.

N1 owns only `refusal_s4_critic_finish_survivors`, so these keys go red on CI with no door.

**Change.** Add both functions to N1's owns, with their new expectations stated in the spec. At the cap: the `repair_limit` Person,
or the seam per B1/B4. Unreadable budget: per B2 (d). Run `grep -rn "s4_critic_completion\|stage_review_exhausted" scripts/tests/`
once more at dispatch, because A1a adds S-R8 (positive control: it finds `test_story_run_refusals.py:3570`).

## Amendments (non-blocking, fix in this round)

**A1. The question's numbers are false (K6, FR-41).** "the case reviewer has looked at them 2 times; the factory's limit for that is 2
rounds" (§4.1) is wrong. `last_round` triggers when the designer's repair count `counted == cap` (`driver_stage_plan.py:537-539`). At
cap 2 the critic has reviewed 3 times: the first review plus two repair reviews. The cap counts the designer's repair rounds
(`controller.py:5619`). Change it to: "the case designer has reworked the cases 2 times after the reviewer sent them back, which is
the factory's limit, and the reviewer still rejects 3 cases". §4.2's "looked at them 3 times" changes the same way. Q1 pins the
corrected sentence.

**A2. N3 is not dispatchable as written (K5).** The new block needs `grammar.REPORT_BLOCKS` / `REPORT_BLOCK_HEADINGS`
(`grammar.py:168-188`), `SLOTS` (`report_facts.py:76-81`) and the template. `grammar.py` is not in N3's owns, and the spec itself
marks this an ESTIMATE. A node that "stops with a question" is a Lead defect (PROJECT.md teamwork rule 11). A cheaper design fits
an existing pattern: a `### Case review remarks the automation did not act on — n` sub-section inside `_r_review_gaps`
(`report_facts.py:4114-4132`). That function already carries `### Runs left failing` and `### Windows over the cap` this way. Put
the same lines in `review_gap_sections` (`:4100-4111`), which builds the gate B packet "so the packet and the report say one thing"
(FR-10). The spec as written omits the packet entirely. This needs no `grammar.py`, no `SLOTS` change, no scribe Tools line and no
`role-load.json` move. Also read the automator's answers from the ONE merged store. `manifest_put.merge` keeps `plan_remarks` of
all windows with a corrected row replacing the old one by identity (`manifest_put.py:1521-1523`;
`test_manifest_put_keep_unsent.py:257-262`). Do not walk the window forms, which re-implements that merge in E-N3-4 (AR-13/AR-15,
duplication). Before dispatch, the Lead or a scout confirms which file and key hold the merged list; one targeted read.

**A3. Join key and renumbering (K4, TEMPORAL).** `CC-n` is one sequence across files and rounds (`s5_plan.py:1146`, `:1161`).
Interleaving the still-rejected remarks "in row order" renumbers the existing concern ids. For a story already in S5 when the
package changes, the windows' answered `CC-n` stop matching, so `remark_rows_missing` refuses, and N3's join by id pairs a reason
with the wrong case. "Row order" across two lists also needs a row index that `_read_round` does not return. **Change**: (i) state
the temporal edge for both worlds. (ii) Either number the still-rejected remarks after the concerns of the same file, or give them
their own prefix `CR-n`; first grep the id readers of `plan_remarks` (positive control `PR-1` in `test_brief_pack_s5_plan.py:485`).
(iii) N3 joins on `id` AND `case`; a mismatch is listed as "the test writer's answer could not be matched", never "acted on".

**A4. F3 (a) carries rejects of cases that no longer exist (K4).** Take a case rejected in round 1 that the designer deleted. It is
never re-listed, so the old reject stays "the latest word". `_placement` makes it `unplaced` -> every window. Every automator must
answer it, and N3 then lists it in the report as a remark not acted on. **Change**: add E-N2-8. A still-rejected remark whose case is
not in the story's current pinned case set (`contract.story_case_links`) is not carried, or is carried with the problem prefixed
"(case removed since the review)"; pick one. Add a row C10. F3 (a) otherwise holds: its error direction (carry more) is right.

**A5. Old-life remarks (K4, X-3).** The spec does not establish whether a gate A or ticket re-run of S4 leaves the earlier S4 critic
dispatches `accepted` (their rejects persist for cases the new life did not re-review) or marks them `stale` (they drop out of
`_case_critic_files`, `s5_plan.py:1104-1107`, and are lost). Either answer changes X-3's invariant. Add a test row over a state with
a stale earlier-life critic, and state the expected result.

**A6. The order promises a report line before it exists (FR-10, FR-37).** The `go on` option says "each it cannot act on is listed
in the test report". On §9, N1 can merge before N3, and for that window the text is false. **Change**: N1 waits for N3, or both land
in one merge wave. Order: N2 -> N3 -> N1 (N1 still after A1a).

**A7. `go on` when `person_pass` returns `{}` for "no author dispatch".** `return False` resumes the critic, a paid resume. The
re-finish meets the same stored `go on` and returns False again: a loop of paid resumes up to the resume cap. Dry run keeps False
(nothing is dispatched). The "no author dispatch" half goes to the unreadable seam (an unknown, FR-59; the conductor's under the
decided F1). Split E-N1-7.

**A8. Small precision items for a weaker builder.**
- State that the `stage_acceptor("S4")` guard (`:817-818`) stays in front of the new call.
- Define `line` for `person_pass` / `review_pass_finding` (`f"{acceptance.STAGE_ACCEPTANCE_PHRASE}: {text}"` as at `:705`).
- §4.2 "the case designer reworked TC-3, ..." becomes "was given TC-3, ... to rework". `rework_cases` is what the rework was given,
  not what changed (FR-41).
- `earlier` counts only entries of the current life; an entry whose critic dispatch is no longer in the controller's records does
  not count.

**A9. §9 order and crossings after the fixes.** N2 (today) -> N3 -> N1 (after A1a merges, and after N2 for the shared predicate of B1)
-> R1. N1 also owns `repair_older_controller` (B2), so the five `driver_dispatch.py` functions to check against FV1-22's in-flight owns
become six. FV1-22 lists `driver_dispatch.py` (conductor rework) in `plans/piles/live-run-fvf/batch-1-live-run-fvf.md:56`. A crossing
on `_answer_repair_limit` makes the order sequential (`очередь:` line). A1a's owns in `driver_stage_plan.py` (`completion_for`) and in
`controller.py` (`repair_passes` comment) do not cross N1. A3 and FV1-9 (`question_register.py`) are disjoint.

**A10. The `executed` flag is redundant on every traced road (K3, K9).** I traced the live road (the Person raised in `complete` ->
answer -> `run_role` finishes the saved result -> the tail sees `bought`), the recovery road (`completion_for` -> `OpenWork` ->
next `stage_S4` owed branch) and a crash after `rework` and before `save_state`. In all three, `s4_repair_owed` already makes the
round non-repeatable once a designer dispatch follows the critic. `s4_round_bought` is keyed on the NEWEST critic dispatch, so the
next critic's finish never sees the old entry. There is no double payment and no lost round on recovery once B3 is fixed. Keeping
`executed` is harmless. Cutting it, or keeping it only as a record, is a legitimate simplification; say which, so the builder does
not invent a second guard.

**A11. Line citations.** The `driver_dispatch.py` lines are stale by about 79 (K1). The builder finds functions by name, as the spec
says. Refresh the cited lines at dispatch so the DoD's "hunks only inside the owned functions" check is easy.

## K2. Fit to (1)-(5)

- (1) Closed question, two doors (+`stop`): met. The F7 (a) `stop` is the standard (`STOP_OPTION`).
- (2) Rows whole to the automator: met by N2 for the roll-call. Only partly met for the person's list (B1) and when no findings file
  exists (B3).
- (3) What was not acted on reaches the report under its owner: met in intent. Dispatchability (A2), join (A3), removed cases (A4)
  and the gate B packet (A2) need fixing.
- (4) Nothing of the removed S2/S3 critics survives: met. Only the S4 seam is used, and S2/S3 functions are untouched.
- (5) Executable by Sonnet: not yet. B2 (budget source), B1 (predicate), A2 (N3 estimate) and A3 ("row order") all leave a choice
  to the builder.

## K3. Loop invariant — traced

See A10 for the roads. A bought round is paid once and is not lost on recovery. A NEW paid critic over unchanged cases arises only
through B3. The second ask comes from a new dispatch in a new slot, so the earlier answer never answers it (E-N1-4 holds). Its text
differs (round number and counts), which satisfies FR-7 even without the `earlier` paragraph. A rerun with no answer re-shows the
same question with no conductor call (D-0041, `docs/DECISIONS_ARCHIVE.md:136`), which is correct.

## K4. The carrier

The producer and readers in §5 are named and complete, plus the gate B packet (A2). The extra key `still_rejected` is safe: no
reader enforces a nine-key set (Grep `nine keys|set\(remark\)|REMARK_KEYS`, case-insensitive: only docstrings at `s5_plan.py:900`,
`:1115`, `:1174`). Who judges that a remark was honoured is the code critic (C12), with code checking presence only. That is P27/AR-29
correct. F3 (a): see A4 and A5.

## K5. The report reader

The spec says so itself: not dispatchable as written. A2 gives a design that fits a traced pattern, which removes the ESTIMATE. AR-27
(the owner is named) is kept. P18 is untouched (no money).

## K6. The question text

The structure follows `human-questions.md:20-38`: what was done, why it cannot be decided, one question, closed answers with three
price lines each, how to answer. Case links count as explained (`human-questions.md:139-141`). Defects: the numbers (A1); the list's
source and notes (B1); "listed in the test report" before N3 (A6). The `go on` price line "a record only; no agent works" is true of
the answer itself. The automator's per-remark answer is part of S5 work it already does, so this is acceptable.

## K7. Architecture

AR-14, AR-15, AR-16, AR-21, AR-22, AR-23 and AR-25 are kept, given B1-B4. The AR-13 breach (two readers) is B1, and AR-25/FR-40 is
covered by B3/A7.

AR-17: the question goes through the one seam (`no_move(call=False, kind="repair_limit")`, `driver_dispatch.py:3240`), as S5/S7 do.
That is kept.

AR-28/FR-59: the unknown count (B2) and the empty contradiction (B4) were holes, and are fixed by the changes there.

FR-4: F5 (a) is a silent pass (B4). The `go on` road is an informed pass, which is correct. FR-7: kept (K3). FR-40: kept once B3 is
fixed.

## F1: decided (a), and what the decision now requires of the spec

The owner decided F1 = (a) on 14.11.2026. The P22/AR-17 question is closed by the owner's word, so the soundness of the reading no
longer has to be argued here. For the record: the reading was already consistent with AR-17 as applied at S5/S7 (the question passes
through the one seam with `call=False`), with D-0041 and with P31. P22's 02.11 sentence ("перед любым вопросом человеку дирижёр
читает то, что код оставил") read literally could have covered code-asked questions, and the owner's «ок» settles that it does not
cover this one.

What the decision requires of the spec text:
- §10 F1 is rewritten as decided («ок», owner, 14.11.2026). The option (b) machinery stays dropped, as §8 already says.
- §1.3 axis 34 drops its "on F1 (b) it is NOT covered" clause.
- The decision's boundary, "the conductor only for free words and unreadable states", is the rule the spec must apply consistently.
  Three places in the current draft depart from it, and the fixes above bring them in line:
  1. F5 (a) has code close the stage over a self-contradicting critic output (B4 -> seam).
  2. The unknown repair count gets no edge (B2 (d) -> seam).
  3. The "no author dispatch" half of E-N1-7 loops paid resumes (A7 -> seam).

## K8, K9, K10

- **K8.** The nodes, with the fixes, are executable by a weaker model. Edges and rows: E-N1-14 (B2), F0 (B3), E-N2-8/C10 (A4) and the
  old-life row (A5) are missing; every other §7 edge has a row. Hot files: see A9.
- **K9.** Cuts: F5 (b) instead of (a) (no code); N3 as a sub-section (A2); `executed` optional (A10); the `earlier` paragraph is
  optional for FR-7 (it is kept for the person's benefit, which is fine). Nothing else to defer.
- **K10.** New checks: (i) the slot/presence check in `s4_review_limit` — owner intent, class shape; (ii) the token check, reused;
  (iii) the shared rejecting-row predicate (B1) — a closed vocabulary read, data class, not a check (raises nothing); (iv) N3's join —
  data, not a check. The only judgment in code was F5 (a)'s driver accept, removed by B4. The census rows are named conditionally
  (AR-20), which is correct.

## Class-wide completeness (SIBLING_MAP)

Axis 5 (author + critic repair loop): S4 joins S5/S7. The S7 waiver stage was checked and is correct (K1), so no sibling is left
behind.

Axis 34 (one road): covered on the decided F1 (a). The hidden S5 literals in the shared handler (`repair_passes`,
`repair_older_controller`) are the class's remaining instances, and they are folded into N1 by B2.

Axis 17 (detector shape): the remark keeps the chain shape plus one key (K4).

No unqueued sibling found beyond these.

## Questions only the owner can answer

1. R-c reading: should the test report name only the still-rejected remarks the automator did NOT act on, or also say that S4 went on
   over the reviewer's rejection for the cases it did act on (one line per case, "went on on your word")? The spec takes the first;
   the owner's «остальное доходит до отчёта» admits both. (F1 is no longer a question: decided (a) by the owner, 14.11.2026.)

## Trail

Read in full: the spec (552 lines). Read in part: the stage-critics spec (A1a owns and rows `:569-648`; crossings grep for
S-R8/R1/A3/`stage_review_exhausted`); the old plan critic verdict (B1/B2 grep, header).

On read-main, read: `driver_stage_plan.py:520-839`; `critic_rollcall.py:380-449` and its constants `:43-44`;
`s5_plan.py:1076-1210`; `driver_dispatch.py:3060-3403`; `driver_stage_s6.py:255-309`; `controller.py:690-774`, `:2185-2209`,
`:2456-2500`, `:5610-5684`; `role_digest.py:40-219`; `agents/qa-case-critic.md` (grep: verdict/state/concerns/review);
`references/question-prices.json:150-194` plus a grep of `go on|not_known|unverified`; `references/human-questions.md:13-67` plus a
grep of `link|price|TC-`; `report_facts.py:55-114`, `:2538-2572`, `:4100-4139`; `grammar.py:165-194`; `test_repair_route.py:499-582`;
`test_story_run_refusals.py:3550-3588`; `docs/DECISIONS_ARCHIVE.md:136` (D-0041).

Searches (Grep tool):
- `APPROVING_VERDICTS|def _read_round|...` over `scripts`: found.
- `^CASE_CRITIC_VERDICTS|^CRITIC_VERDICTS|...`: found `contract.py:2211`.
- `repair_limit` in `driver_machine.py`: `:3428`.
- `_passed_by_person` in `controller.py`: 18 hits.
- `def split_overridden`: `waiver.py:202`.
- `s4_critic_completion\(` over `scripts`: hits in the stage, the recovery road and three tests.
- `stage_review_exhausted` over `scripts/tests`: 6 files.
- `rework\("S7"|...` over `scripts`: S7 reworks are stage S5.
- `plan_remarks|case_concerns|concern_report`, case-insensitive, `*.py`: 13 files, `report_facts.py` absent, control `brief_pack.py`
  present.
- `"plan_remarks"` readers: `brief_pack.py:2663`, `s5_precheck.py:4528-4582`, `manifest_put.py:1523`.
- `REMARK_KEYS|set\(remark\)|nine keys`, case-insensitive: docstrings only.
- `FV1-22|FV1-9` in `plans/piles`: `batch-1-live-run-fvf.md:42`, `:56`.
- `test_stage_review_person_pass|...` in `test-layers.json`: `:3166`, `:7410`, `:9951`, `:9977`.

Reruns: none. A plan review has no mechanical layer, and no test was run.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 the question's rejected-case list is read from digest rows with a 'not in APPROVING_VERDICTS' predicate: 'approved (approve_with_concerns)' parses to state 'approved' (role_digest.py:159-173, contract.py:2211) and is shown as still rejected; the digest has an 80-char reason, not a note; a second reader beside N2's roll-call (AR-13, FR-10)",
    "B2 budget/passes source unspecified for s4_review_limit; driver repair_passes hard-codes qa-automator/qa-code-critic (driver_dispatch.py:3139-3143) so S4 passes is always None; repair_older_controller is S5-worded (:3172-3178) and not owned; an unknown count (counted/cap not int, driver_stage_plan.py:539) gets no edge and would print 'round None+1'",
    "B3 no findings file on the last round: round -> OpenWork -> stage_S4's owed branch needs s4_findings() -> a NEW paid critic over unchanged cases (t-919 F-1 broken); go on carries nothing it promised",
    "B4 F5 (a) has code write a driver accept over a critic header 'concerns' with no person informed: a silent pass on an unknown (FR-4, FR-59, P27/AR-29), and against the owner's F1 boundary (unreadable states go to the conductor); take F5 (b), today's seam, no code",
    "B5 N1 turns red keep rows outside its owns: test_story_run_refusals.py refusal_c2_4_* :3584-3585 and test_repair_route.py s4_last_round_and_text_from_the_budget :570-581"
  ],
  "class_completeness": "Axis 5 and axis 34 (on the owner-decided F1 (a)): S4 joins the S5/S7 repair-limit road; the S7 waiver --stage S5 is correct (S7 reworks dispatch at stage S5, driver_stage_s7.py:992,1090); the remaining S5 literals of the shared handler (repair_passes, repair_older_controller) are folded into N1 by B2; axis 17: the remark keeps the chain shape plus one key. No unqueued sibling found.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-6-s4-only-spec.md (whole)",
      "docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md (A1a 569-648, crossings grep)",
      "docs/tasks/specs/reviews/20261113-fv1-6-plan-critic.md (B1/B2 grep)",
      "read-main scripts/driver_stage_plan.py:520-839",
      "read-main scripts/critic_rollcall.py:43-44,380-449",
      "read-main scripts/s5_plan.py:1076-1210",
      "read-main scripts/driver_dispatch.py:3060-3403",
      "read-main scripts/driver_stage_s6.py:255-309",
      "read-main scripts/controller.py:690-774,2185-2209,2456-2500,5610-5684",
      "read-main scripts/role_digest.py:40-219",
      "read-main scripts/report_facts.py:55-114,2538-2572,4100-4139",
      "read-main scripts/grammar.py:165-194",
      "read-main scripts/tests/test_repair_route.py:499-582",
      "read-main scripts/tests/test_story_run_refusals.py:3550-3588",
      "read-main references/question-prices.json:150-194",
      "read-main references/human-questions.md:13-67",
      "read-main agents/qa-case-critic.md (grep)",
      "read-main docs/DECISIONS_ARCHIVE.md:136",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": []
  },
  "fixes": [
    "F1 decided (a) by the owner 14.11.2026: rewrite 10 F1 as decided and drop the F1 (b) clause of 1.3 axis 34",
    "B1: read the question's rows from the current findings file roll-call through one shared rejecting-row predicate in critic_rollcall (also used by _read_round); notes from the row's note; rewrite 3.1.2a and 11 S4; order N2 before N1",
    "B2: name the budget source (a budget argument to s4_critic_completion, or budget_or_none in the finish); passes = budget['passes'] validated for the S4 pair; repair_older_controller stage-aware and owned; new edge E-N1-14 for an unknown count -> today's seam, no number printed",
    "B3: s4_review_limit returns False when s4_findings() is None (the t-909 F-3 rule); test row F0",
    "B4: take F5 (b): an empty rejecting set with header concerns goes to stage_review_exhausted; rewrite E-N1-2 and row E1",
    "B5: add refusal_c2_4_s4_keeps_open_only_when_the_round_will_run (:3584-3585) and s4_last_round_and_text_from_the_budget (:570-581) to N1 owns with stated new expectations",
    "A1: fix the question's numbers: the cap counts the designer's repair rounds; the critic reviewed counted+1 times",
    "A2: N3 as a sub-section of _r_review_gaps and review_gap_sections (report and gate B packet), reading the merged plan_remarks store of manifest_put; one targeted read before dispatch",
    "A3: state the temporal renumbering edge; number still-rejected remarks after the concerns or use their own prefix; N3 joins on id and case",
    "A4: E-N2-8 for a case no longer in the pinned case set; row C10",
    "A5: test row for an earlier-life critic dispatch (stale vs accepted) with the expected result",
    "A6: order N2 -> N3 -> N1 so the go on text never promises a report line that does not exist",
    "A7: split E-N1-7: dry run returns False, no author dispatch goes to the unreadable seam",
    "A8: keep the stage_acceptor guard explicitly; define line; 'was given ... to rework'; earlier counts the current life only",
    "A9: update 9 order and the hot-function list (six driver_dispatch.py functions vs FV1-22)",
    "A10: say whether executed stays as a record or is cut",
    "A11: refresh the driver_dispatch.py line citations"
  ]
}
```
