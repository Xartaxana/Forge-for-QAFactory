# FV1-6 plan critic: the door back to the author after an exhausted stage review

Under review: `docs/tasks/specs/20261113-fv1-6-s2-door-back-to-tester-spec.md` (draft, designer, 13.11.2026).
Facts checked on `.claude/worktrees/read-main` at `e4ba384` (`git -C … log -1` printed `e4ba384 wave 1 integration report`). All
file:line below are read-main lines under `ai-packages/qa-factory/scripts/` unless another path is given.
Lead's fork decisions taken as given: F1 (a), F2 (a), F3 (a), F4 (a) now plus the residual node, with the (b)/(c) choice going to
the owner; F5 and F6 filed as findings.

**Verdict: NEEDS WORK (fit_with_fixes). 4 blocking findings (B1-B4), 12 amendments (A1-A12).** All of them are spec edits the
Lead can make (they continue this draft). B2 adds one small design element: the Lead can write it, or send it back to the
designer if it wants an isolated drafting context. Accepting the spec is the Lead's decision; this verdict is input to it.

---

## Q1. Facts by trail: is the root cause as stated?

**Yes, confirmed on e4ba384.**
- `no_move.py:105-106`: `rework_blockers` adds `running` whenever `facts["running"] is not False`.
- `driver_conductor.py:389`: `running` = any controller dispatch with status `running`. The critic is not excluded.
- The critic's dispatch is still `running` while the seam asks. `stage_critic_completion.complete` (`driver_stage_plan.py:662-679`)
  is the `complete` callable that `Driver.finish` (`driver_dispatch.py:768`) evaluates BEFORE `story_step finish`. `run_role`
  calls `finish` last (`driver_dispatch.py:~766`). The last-round `reject` reaches `stage_review_exhausted` at `:678`.
- `release_and_restart` is open: `no_move.py:142-143` (`_restart`: the dispatch is live and `attempts == 0`).
- The data row says the same: `references/conductor-actions.json:73` ("no dispatch running") and `:74` ("a dispatch is running").
- §8's open question is now answered: the controller DOES refuse any new dispatch while another one runs. In `apply`, the
  `dispatch` branch (`controller.py:5468-5483`) raises "sequential task already has an active dispatch". A rework registers
  through it (`Driver.rework` -> `controller("rework")`, `driver_dispatch.py:2671`). `controller.rework` itself
  (`controller.py:3677`, `build_rework_request`) does not check running dispatches, so the refusal comes at apply time. The
  design's reliance on `owed_rework` waiting (`driver_s0.py:557`) is therefore load-bearing and correct, and it also makes
  B2 real.

**Stale references** (the designer read the root checkout at f52faed). Spec value, then the read-main value:

| Spec | read-main |
|---|---|
| `driver_machine.py:573-611` (`seam_rework_step`) | def `:578`; preface `:606-607`; `ReworkRefused` road `:611-614` |
| `driver_machine.py:2288-2339` (`take_seam_answer`) | `:2335-2386`; the `unread` call `:2371` (spec `:2323-2324`) |
| `driver_machine.py:2379-2380` / `:2385-2388` (`seam_chosen`) | `record_seam_rework` `:2426-2427`; the `why: chosen` call `:2429-2436` (`no_move` at `:2432`) |
| `driver_machine.py:2695` (exploratory preface road) | `record_seam_rework(clean, …, self._bug_preface(…))` `:2742` |
| `driver_machine.py:41-44` | `:44-45` |
| `driver_dispatch.py:2639-2641` | cut `reason[:1500]` `:2660`; the long-words `line` `:2681-2683` |
| `driver_dispatch.py:629-630` / `:696` | `rework.get("line") or "Rework reason: …"` `:638`; `lines += list(extra)` `:704` |
| `driver_dispatch.py:3010-3035`, `:3057` (S5 `repair_limit_gate`) | def `:3052`; offer `:3099`; `round` passes `:3198-3200` |
| `no_move.py:417-423` (lone rule) | `:419-421` |
| `judgment-census.json:1001` (`no_move_facts` row) | `:1005` |
| `question-prices.json:161-166` / `:181-186` | `s5.repair_limit` `:155`; `exit.resume_limit` `:175`; `s7.repair_limit` `:187` |
| `controller.py:3665-3668` (a rework with words re-runs later stages) | `build_rework_request` `:3677`; the `rerun_after` rule in its docstring `:3690-3693` |

**Correct as cited:**
- `driver_stage_plan.py`: 583-593, 653-679, :678, :691, :713 (`since`), :728, :730, :733, :735, :744, :747, the S4 call sites 807-821,
  and 117/122/131.
- `no_move.py`: :36, :98-111.
- `driver_conductor.py`: :389, :733-752, :852-870.
- `driver_s0.py:550-559`; `driver_dialog.py:326-327` and `:622`.
- `conductor-actions.json:73-77`; `runtime_policy.py:13`; `controller.py:2197`.
- `driver_stage_s6.py`: 334-341, 358, 365.

---

## Q2. Feasibility, end to end on e4ba384

What works:
- **Recovery road.** The person's answer raises in process N; process N+1 takes it. `seam_chosen` -> `record_seam_rework`
  (`:2426-2427`) runs while the critic is still `running`. `seam_rework_step` -> `owed_rework` returns None (a dispatch is
  running, `driver_s0.py:557`). `where` -> `wait_existing_job` (`driver_machine.py:1445`) -> the saved result
  (`driver-runs/<id>.json`, `:1464-1470`) -> `_finish_saved_result` (`:1522`) -> `finish(complete=completion_for(…))`.
  `completion_for` dispatches by stage and role: S2/S3 at `driver_stage_plan.py:1036-1043`, S4 at `:1108-1114`. Both re-read the
  budget, so `last_round` is True again and the call reaches `stage_review_exhausted`, where the new branch sees the choice.
  This is the same road the existing F3 (B-6) `go on` pass already relies on.
- **After `OpenWork`.** The critic is accepted and the stage stays open. The next turn, `seam_rework_step` finds no running
  dispatch. `before` was recomputed by the re-record, so the record is not taken for a done one, and `Driver.rework` runs the
  author. Both `stage_repair_owed` and `s4_repair_owed` are gated by `not last_round` (`:612`, `:544`), so neither of them
  fires a test_defect round over the person's round.
- **The bought round.** A cause other than `test_defect` leaves `counted == cap`. The next critic is again on its last round,
  and a reject comes back to the seam (E6/F2 holds).
- **Old records.** `since` blocks an old record from holding a later review open. The re-record writes a new `at`, and the
  next critic's start comes after it (E2 holds). R8's de-duplication makes a refused-then-repeated finish idempotent.

What breaks or is missing: see B1, B2, B4 and A6, A7 below.

---

## Blocking findings

### B1. `asked_why` is lost after one re-ask
**Spec location:** §3.2, §5.1 points 3-5, E7, E8.

**Mechanism.** Every Person the seam raises stores `asked.why = state["why"]`: `driver_conductor.py:428`
(`person.why = str(state.get("why") or "")`), written at `driver_dialog.py:327` and restored at `:622`. The spec passes
`asked_why=asked["why"]` only one hop.

**Scenario.**
1. The person answers the exhausted seam with free words.
2. `unread` runs (state `why: unread_answer`, `asked_why: stage_review_exhausted`). `rework` is open.
3. The conductor asks back with options, for example `go on` / `restart` / `stop`, or a `rework` it later withdrew. The new
   `asked.why` is now `unread_answer`.
4. The person answers in words again, or picks a token whose road is the `why: chosen` call. That call carries
   `asked_why="unread_answer"`, which is not in `FINISHING_WHYS`.
5. `running` is True (the critic again), so `rework` is closed. The conductor is told "`rework` is no longer open"
   (`driver_conductor.py:715-716`).

This breaks E8's own invariant ("a `rework` choice never meets 'no longer open' because of the critic's own running dispatch")
and E7 on the second hop.

**Fix.** Carry the origin through the re-ask. In `_person_of`, write
`person.why = str(state.get("asked_why") or state.get("why") or "")`. The only reader of `asked["why"]` is the restore at
`driver_dialog.py:622`; I grepped `asked.get("why")|asked["why"]|.why\b` over `scripts/*.py` minus tests, and the positive control
is that the grep found `:327` and `:622`. Add `driver_conductor._person_of` to owns. Add a row (F8): an `asked` written by an
`unread_answer` Person whose state carried `asked_why: stage_review_exhausted` still yields `running` False. The alternative, a
separate `asked_why` key in `asked`, touches `driver_core.Person`, `driver_dialog.ask` and the restore: three more sites for no gain.

### B2. The exclusion also opens the RUN form of `rework`, which the controller refuses
**Spec location:** §3.1, §4 "Error direction", E1, E7.

**Mechanism.** `no_move.py:8-11` defines the forbidden error of this gate as "a move whose precondition is false". Once
`running` excludes the critic, `rework_stage` is listed under "Moves open here … Only these may be offered **or taken** now"
(`no_move.py:264-265`). The data row's `run` tells the conductor how to run it itself (`conductor-actions.json:71`). The seam's own
lead says "Decide: accept {stage} with the gap, **one more round on words you ground**, or ask the person"
(`driver_stage_plan.py:707`). The docstring at `:694-697` describes `rework --reason` as a conductor command. The sentence "Do not
run the rework yourself" exists only in `chosen_note` (`driver_conductor.py:719-721`), so neither the first call nor the
`unread` call carries it.

**Scenario.** At the first call (or the `unread` call) the conductor runs
`controller.py --operation rework --stage S2 …`. The controller refuses at apply (`controller.py:5481-5483`: "sequential task already
has an active dispatch: S2-qa-case-critic-3"). The result is a paid call spent on a refusal, and a question to the person whose
prose may then say the round is impossible. Nothing is corrupted, because the refusal comes before any event. But the gate now
offers a move whose run precondition is false, and that is exactly the direction §4 claims it never takes.

**Fix (a spec edit).** When the exclusion applies, the conductor is told that `rework` is OPTION-ONLY: "offer it; the driver runs
it after the reviewer's dispatch finishes; running it now is refused". Two options:
- (i) a `held` fact rendered by `NM.moves_section` on the `rework` line; this widens owns to `no_move.moves_section`;
- (ii) one line appended to the `text` of the three states (the first call in `stage_review_exhausted`, the `unread` state, the
  `chosen` state), all of which are already in owns.

In the same move, rewrite the lead's "one more round on words you ground" as "offer the person one more round for {author}". Also
make the data row's `precondition`/`forbidden_when` (`conductor-actions.json:73-74`) name the one exception ("other than the
reviewer whose finish asks"), so that data and code say the same (AR-1, FR-10). That is a text change to a data row the spec
lists as a non-goal; the Lead decides whether to widen owns or to file it.

### B3. On the unreadable-verdict road the preface states a reject that nobody established
**Spec location:** §5.1 point 6c, E4.

**Mechanism.** `stage_review_exhausted` is also reached with `unreadable=True` when the verdict word cannot be read:
`driver_stage_plan.py:669-670`, `:806-810`, and `driver_stage_s6.py:358`. On the recovery road it is reached the same way again,
since `stage_verdict_known` stays False. In that case point 6c's line still reads "The verdict of {who} that **sent {stage} back**
is in {form}; … this round repairs what it names". That reports an unknown as a fact (FR-41, AR-28): the critic's verdict word
was not readable, not a reject.

**Fix.** Condition the line on `unreadable`, for example "The form of {who} is in {form}; its verdict word could not be read, so
the person's words below are this round's instruction". Add an R row for `unreadable=True`.

### B4. F3 (a)'s cause rule never reaches the conductor, so E12 becomes the expected first outcome
**Spec location:** F3, E12, §3.5.

**Mechanism.** "A cause that is not `test_defect`" appears only in the docstring (`driver_stage_plan.py:694-697`). The state's
`text`, `lead` and `lines` (`:702-707`) carry nothing about the cause. Meanwhile `test_defect` is the honest word for "repair what
the critic named", and the args list offers every member of `C.REPAIR_CAUSES` (`driver_conductor.py:399`). The controller refuses
a `test_defect` round past the cap (`controller.py:5602-5609`, with the `free` sentence).

**Predictable path.** The conductor offers `rework` with `cause: test_defect`; the person chooses it; `seam_rework_step` gets
`ReworkRefused`; `seam_rework_refused` makes another conductor call; that call is not a `chosen` call, so it cannot record a lone
`rework`; the person is asked again for a choice they already made. That is friction (P11, AR-12), and the live-proof row would
mostly prove E12 rather than the door.

**Fix.** The lead of the first call names the rule in one sentence. The words stay the conductor's; for example: "a round past the
cap carries a cause other than `test_defect` (the controller refuses `test_defect` here); which cause fits is your judgment".
`check_args` keeps checking only the closed list (AR-2 unchanged).

---

## Amendments (not blocking; apply in the same edit)

- **A1, E10 (conflicting pair).** "go on wins, then the pending record still runs" means the person gets BOTH: S2 accepted with the
  gap and a finding, and then a rework that re-runs S2 (with `rerun_after`) on a choice the code just overrode. Recommendation: the
  LATER of the two recorded words wins (both carry `at`). The minimal alternative: when the pass closes the stage, drop the
  pending `seam_rework` recorded after `since`, through `drop_record`, with a printed line naming it. Either way, state the
  person-visible outcome. Which word wins is a reading of the person's intent, so this is the Lead's choice. The spec's
  invariant ("one finish never both accepts and holds open") is true but beside the point.
- **A2, duplication.** Point 6b's "parses (aware ISO) to a moment strictly later than `since` parsed the same way" asks for a second
  normaliser beside `person_pass`'s nested `stamp` (`driver_stage_s6.py:273-283`), which normalises exactly this through
  `controller.stamp_utc` and refuses naive times. Name ONE helper: hoist `stamp` to a module-level function and call it from both,
  as `stamp(chosen["at"]) > since > ""`. This widens owns to `driver_stage_s6.person_pass`. Otherwise the builder writes the second
  copy (AR-13, AR-15).
- **A3, duplication.** Point 7's `REWORK_REASON_INLINE = 1500` mirrors a literal that already appears twice in `Driver.rework`
  (`driver_dispatch.py:2660`, `:2681`). That is a third copy, free to drift. A simpler design removes both the branch and the
  constant: `seam_rework_step` always passes `reason = the person's words` and `extra = preface`. The controller never saw the
  preface anyway (with `--words-file`, `reason` is the file's text), and `extra` reaches the prompt on both lengths (`:704`).
  L1/L2 stay as AT/BEYOND rows on the words' length (inline vs the file line) with the preface present in `extra` on both; L3
  ("no preface: no `extra`") stays. This also fixes the exploratory road (`:2742`) uniformly.
- **A4, unnamed edge.** The chosen round's stage can differ from the reviewed stage: `rework_stages` at S2 holds S1 and S2; at S4,
  S1-S4; at the S6 consumer, S5-S8 (`driver_conductor.py:375-378`). State it: the choice is honoured all the same (it is the
  person's word), and the preface's wording stays true for any stage (not "this round repairs what it names" for S1).
- **A5, unnamed edge.** The re-record can raise inside the finish: `record_seam_rework` raises `held_question` when the words file
  is gone or `controller.json` is unreadable (`driver_conductor.py:741-747`). The critic's finish is then not done and the question
  comes back. That is acceptable (FR-59), but name it, with an R row if the raise path is cheap to stub.
- **A6, E7 incomplete.** If the `unread` conductor answers `continue`/`retry`, `take_seam_answer` returns False and `_file_words`
  files the words as `pending_words[<critic id>]` (`driver_machine.py:4085-4107`). `wait_existing_job` then RESUMES THE CRITIC with
  the person's words (`:1451-1453`) instead of finishing its saved result. This is existing behaviour, not introduced here, but E7
  claims the road ends at the conductor. State it, or file it as a finding.
- **A7, E12 follow-on.** After a refused rework, if the conductor answers `continue`, the stage stays open
  (`OpenWork("stage_in_repair")` was accepted). `where` -> `stage_S2` -> `stage_critic_route`: on the last round `stage_repair_owed`
  is skipped (`:612`), so a NEW paid critic runs over the unchanged artifact. Name it in E12, since this design makes the path
  reachable.
- **A8.** Replace every stale reference in the Q1 table.
- **A9, §8 / rule 10(b).** `docs/SIBLING_MAP.md` was not read. The relevant axes are:
  - Axis 5, "Author + critic repair loop": lists S4/S5/S7; add the S2/S3 stage-review line and the S6/S7 consumer reviews.
  - Axis 18: shrink-only ratchets; a census row added is a raise to name. Name AR-20 in §1 if a row is added.
  - Axis 32: where judgment lives.
  - Axis 34: one road.

  Enumerate them in §1, not left to the commit message.
- **A10, the pile.** The node row (`plans/piles/live-run-fvf/batch-1-live-run-fvf.md:39`) lists only `scripts/driver_machine.py`
  under «Пишет в». The spec owns four scripts plus a test, the census and changelog.d (and more after B1, B2, A2). Update the row:
  `piles.py check (б)` zones read it.
- **A11, tests (TESTING.md).**
  - `test_no_move_seam_n2b_n15.py` IS a keep row on e4ba384: `test-layers.json` `keep`, layer `detector`, its `covers` names all
    four scripts. The quarantine entries for `test_stage_review_person_pass.py`, `test_stage_critic_route.py` and
    `test_stage_acceptance_consumer.py` are confirmed.
  - The F table is the right detector for the gate. The R/L/A rows are rows of parameterised tables, which TESTING.md allows
    ("ключи и рёбра — строки одной параметризованной таблицы").
  - Add F8 (B1), a row for the option-only note (B2), and an `unreadable` R row (B3).
  - Under A3, L1-L3 become the two length rows plus no preface.
  - The budget rule (test lines ≤ product lines) will likely be exceeded. The builder names the reason in one line, per TESTING.md.
  - R6's ids naming the value are right. The limit rows sit AT and BEYOND 1500, as rule 11 asks for the person's words, which are
    outside input.
- **A12, F4 residual node.** It must name the exact second-road difference, not only "two question shapes". Here the cap is lifted
  by a cause LABEL (a non-`test_defect` word on a review-repair round). The S5/S7 `round` lifts it by recorded PASSES with the
  honest `test_defect` (`driver_dispatch.py:3198-3200`). That label-vs-passes split is what the owner's P31 word has to settle.

---

## Q3. Architecture

| Invariant | Holds? | Basis |
|---|---|---|
| AR-25 | yes | A reachable move; but see B2 for the run form. |
| AR-17 | yes | No new `Person(` site: `_person_of` is an existing builder; B1's edit is inside it. |
| AR-19 | yes | One function for five sites, no stage name. The S4 word stays `cases_in_repair`. |
| AR-24 | yes | The words travel by file and the form by path. A3 makes it simpler. |
| AR-14 | yes | Re-record through `record_seam_rework`. |
| AR-13 | at risk | The `running` read and `_dispatch_starts` are kept, but A2: a second time normaliser beside `person_pass.stamp`. |
| AR-28 / FR-59 | E3 yes; 6c no | B3: the preface on the unreadable road. |
| AR-29 | yes | See Q6. |
| AR-1 | partly | `FINISHING_WHYS` as a code constant is acceptable (code's own vocabulary, the `EXCLUDED_KINDS` precedent). But B2: the data row's precondition text no longer matches the code. |
| AR-20 | not named | Touched if a census row is added (A9). |
| AR-12 | not named | Touched by B4 (predictable extra round trip). |

- **P22:** kept. The conductor is called first, and a recorded choice skips only the SECOND call.
- **P13:** kept (F2 (a)).
- **P31:** the fix itself is one road for the five review sites. The remaining second road (S5/S7 `round`) is F4, with the
  difference to be named as in A12.
- **Rule 19 (one action, one road):** `FINISHING_WHYS` is a branch serving the task's own condition (the seam sits inside that
  dispatch's finish) while the shared `running` mechanism is still reached. It is not an unauthorised exclusion.
- **Sibling sweep of "a seam raised inside a finish":** the other `no_move` calls in the stage modules are
  `driver_stage_s7.py:353` and `:475`, both `call=False` thresholds (no conductor, no `rework`), plus `driver_stage_plan.py:955`
  (refusal, `dispatch=""`). So `stage_review_exhausted` is the only member today; `FINISHING_WHYS` with one word is complete.

## Q4. Error direction of the reused filter

- I traced the §4 adversarial list on `driver_conductor.py:352-407`. With `dispatch` empty, another `why`, or a missing
  `asked_why`, nothing is excluded. With another dispatch running, `running` stays True. With an unreadable controller, `held()`
  raises and `running` is None, so `rework` stays closed (`no_move.py:105`). If the named dispatch is not running there is nothing
  to exclude. The **offer** form therefore never opens beside another running dispatch or on an unknown state.
- Missing from the list:
  - (1) The RUN form (B2): the one direction in which the gate now errs.
  - (2) `asked_why` that names the seam while `dispatch` names a critic that a `restart` replaced (a new id `C'` running): `C'`
    counts, so `rework` stays closed. That is correct; add it as a row.
  - (3) A multi-hop `asked` (B1): wrong in the safe direction (too few moves), but it breaks E8's stated invariant.

## Q5. Edges E1-E12

| Edge | Verdict |
|---|---|
| E1 | Right. |
| E2 | Right, and its positional invariant is complete. |
| E3 | Right. |
| E4 | Wrong on the unreadable road (B3). |
| E5 | Right; A3 simplifies it. |
| E6 | Right. |
| E7 | Incomplete (B1, A6). |
| E8 | Invariant false after one hop (B1). |
| E9 (temporal) | Right: an `asked` written before the change already carries `why: stage_review_exhausted` (`driver_dialog.py:327`), and no record can predate the change. Both worlds are covered, and the creating move is named. |
| E10 | Decided, but to a double effect that would surprise the person (A1). |
| E11 | Right. |
| E12 | Right, but B4 makes it the common path, and A7's follow-on is unnamed. |
| New edges | A4 (the record's stage differs from the reviewed stage), A5 (the re-record raises inside the finish). |

## Q6. Judgment (P27 / AR-29)

- No new check decides a role's or the person's question. Whether to buy the round is the person's; stage, role, cases and cause
  are the conductor's (closed list only); repaired quality is the critic's. The time join is a data join.
- The census rows of §4 are right in class. Cite `judgment-census.json:1005`, not `:1001`. "Add a row only if the census test
  names the unit" is the right conditional. If a row is added, name the raise (axis 18, AR-20).
- B4's fix keeps the cause as the conductor's judgment: the lead states a constraint the controller enforces, not a choice.

## Q7. Tests

See A11. The defect the node exists for (`rework` closed at the exhausted seam) is caught by F1 and F4/F5, which failed before
the change. The cross-process flow is covered only by stubbed R rows. The live proof row in `live-runs` is the FR-33 complement;
it is correctly not a test.

## Q8. Owns and crossings

The function-level owns are exact for the draft as written. The draft's own diff needs nothing outside the list: `unread` gains a
keyword; `seam_chosen`, `take_seam_answer`, `seam_rework_step`, `stage_review_exhausted` and `no_move_facts` are all listed.

The fixes need these additions:
- `driver_conductor._person_of` (B1);
- either `no_move.moves_section` or nothing extra (B2 option ii), and optionally the text of `conductor-actions.json`
  `rework_stage` (B2);
- `driver_stage_s6.person_pass` if the helper is hoisted (A2).

Crossings: the batch-1 nodes writing `driver_dispatch.py` (FV1-2, FV1-3, FV1-13) do not meet this node, since it edits no
`driver_dispatch.py` (A3 keeps it so). I could not see the function-level owns of the other in-flight work on
`driver_stage_plan.py` / `driver_machine.py` / `driver_conductor.py`. Before launch, the coordinator needs (via a scout) the owns
lines of every in-flight dispatch on those four files, to check function overlap per PROJECT.md «Командная работа» p. 3.

## Q9. Executable by a weaker model?

Mostly yes. Every point names the file, the function, the exact expression and a test row, and the directions are chosen. The
gaps: B1 and B2 add steps the draft lacks; A1 needs a direction picked; A2 replaces an ambiguous "parsed the same way" with a
named helper. Once those are edited in, the node is executable as written.

---

## Duplication and consistency
Found: A2 (a second time normaliser beside `driver_stage_s6.py:273-283`) and A3 (a third copy of the 1500 cut). Grepped: `1500` in
`driver_dispatch.py` and `driver_machine.py`, `def person_pass` / `stamp_utc` in `driver_*.py`, and `record_seam_rework(` across
`scripts/*.py` (4 callers: `driver_conductor.py:730`, `driver_machine.py:2427`, `:2742`, `:3620`). The hoisted `word` (point 6a)
removes the one literal duplication the new branch would add.

## Code quality
No blocking concern in the drafted snippets beyond B3 (a false statement in a role-facing line) and A3 (an avoidable branch plus a
constant). The R1 snippet's args comprehension keeps `stage`, `role` and `cause`, the keys `record_seam_rework` subscripts
(`driver_conductor.py:748`).

## One action, one road (rule 19, P31)
The fix unifies the five review sites on one road. The residual S5/S7 `round` road is F4 with its node opened by the Lead; A12
names the exact difference to give the owner. No unauthorised exclusion.

## Trail
- **Read in full:** the spec under review.
- **Read on read-main e4ba384:**
  - `driver_stage_plan.py` 520-860 and 1005-1120;
  - `no_move.py` 1-160, 255-300 and 395-470;
  - `driver_conductor.py` 340-470, 560-900;
  - `driver_machine.py` 570-620, 740-775, 1440-1600, 2335-2445, 3515-3600, 3975-4025, 4085-4110;
  - `driver_dispatch.py` 455-480, 600-780 (grep), 2644-2700;
  - `driver_s0.py` 550-565; `driver_dialog.py` 300-345 and 622;
  - `controller.py`: 230-262, 1157-1163, 3677-3800, 5455-5490, 5585-5625, 6410-6430, 7735-7745, 9920-9990;
  - `driver_stage_s6.py` 262-300; `driver_stage_s7.py` 340-356;
  - `references/conductor-actions.json` 66-80; `question-prices.json` (grep); `runtime_policy.py` (grep);
  - `scripts/tests/test-layers.json` (keep and quarantine sections via a json read);
  - `scripts/tests/test_no_move_seam_n2b_n15.py` 1-45 and 455-486; `scripts/tests/fixtures/judgment-census.json` 990-1010;
  - `plans/piles/live-run-fvf/batch-1-live-run-fvf.md` 30-50, plus the finding file.
- **Also read:** `docs/TESTING.md` (whole) and `docs/SIBLING_MAP.md` (axis list, axes 5 and 13).
- **Not re-read (relied on the index):** `architecture.md` and `factory-rules.md` in full; the AR/FR one-liners are loaded in the
  session.
- **Mechanical layer:** none attached and none required for a plan review; no reruns.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 spec 3.2 / 5.1 p.3-5 / E7 / E8 -> asked_why is lost after one re-ask: _person_of stores asked.why = state why (driver_conductor.py:428, driver_dialog.py:327); carry the origin (person.why = asked_why or why), add _person_of to owns and a row F8",
    "B2 spec 3.1 / 4 / E1 / E7 -> the exclusion also opens the RUN form of rework, which the controller refuses beside the running critic (controller.py:5481-5483) while the prompt says moves may be offered or taken (no_move.py:264-265) and the lead invites a conductor-run round (driver_stage_plan.py:707); mark rework option-only when held, rewrite the lead, align conductor-actions.json:73-74",
    "B3 spec 5.1 p.6c / E4 -> on the unreadable-verdict road (driver_stage_plan.py:669-670, 806-810; driver_stage_s6.py:358) the preface claims the critic sent the stage back; condition the line on unreadable (FR-41)",
    "B4 spec F3 / E12 -> the not-test_defect cause rule lives only in the docstring (driver_stage_plan.py:694-697); the conductor will pick test_defect, the controller refuses past the cap (controller.py:5602-5609), the person is asked twice; name the rule in the first call's lead"
  ],
  "fixes": [
    "B1-B4 as listed in blockers",
    "A1 E10 -> later recorded word wins (or drop the pending record with a printed line when the pass closes the stage); state the person-visible outcome; Lead picks",
    "A2 5.1 p.6b -> reuse one time normaliser: hoist driver_stage_s6.person_pass stamp to a module helper, compare stamp(at) > since > empty; widen owns",
    "A3 5.1 p.7 / E5 -> drop REWORK_REASON_INLINE: seam_rework_step always passes reason = person's words and extra = preface; keep AT/BEYOND rows on the words length",
    "A4 new edge -> the chosen round's stage may differ from the reviewed stage (S1 at S2, S5 at S6 consumer): honoured; preface wording true for any stage",
    "A5 new edge -> record_seam_rework raising held_question inside the finish (driver_conductor.py:741-747): finish not done, question back; name it",
    "A6 E7 -> name the continue outcome: words filed to pending_words of the critic and the critic resumed with them (driver_machine.py:4085-4107, 1451-1453), existing road or a finding",
    "A7 E12 -> name the follow-on: after a refusal and a conductor continue, a fresh paid critic over unchanged work (stage_critic_route skips stage_repair_owed on the last round, :612)",
    "A8 2.1 / 2.3 / 4 / 5.2 -> replace the stale file:line references with the read-main values listed in Q1",
    "A9 1 / 8 -> enumerate SIBLING_MAP axes 5, 18, 32, 34; name AR-20 if a census row is added; name AR-12 for B4",
    "A10 node row batch-1:39 -> list every owned path in the writes column",
    "A11 5.3 -> add rows F8 (B1), option-only note (B2), unreadable preface (B3), restarted-critic id; L rows per A3; builder names the test-budget reason",
    "A12 F4 residual node -> name the exact difference: cap lifted by a cause label here vs recorded passes with test_defect at S5/S7 round (driver_dispatch.py:3198-3200)"
  ],
  "class_completeness": "Class: rounds spent at a review with no move to the author. The one function stage_review_exhausted serves S2, S3, S4 and the S6/S7 consumer reviews (call sites driver_stage_plan.py:667-678, 807-821; driver_stage_s6.py:341, 358): covered by the shared fix. The other no_move calls inside stage modules (driver_stage_s7.py:353, 475 call=False thresholds; driver_stage_plan.py:955 refusal) are not this class, so FINISHING_WHYS with one word is complete. The S5 window and S7 test repair have a door on another road (repair_limit, driver_dispatch.py:3052-3200): F4 residual node, difference to be named per A12. SIBLING_MAP axis 5 author+critic repair loop must gain the S2/S3 and consumer lines (A9).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-6-s2-door-back-to-tester-spec.md",
      "read-main ai-packages/qa-factory/scripts/driver_stage_plan.py 520-860, 1005-1120",
      "read-main ai-packages/qa-factory/scripts/no_move.py 1-160, 255-300, 395-470",
      "read-main ai-packages/qa-factory/scripts/driver_conductor.py 340-470, 560-900",
      "read-main ai-packages/qa-factory/scripts/driver_machine.py 570-620, 740-775, 1440-1600, 2335-2445, 3515-3600, 3975-4025, 4085-4110",
      "read-main ai-packages/qa-factory/scripts/driver_dispatch.py 455-480, 600-780, 2644-2700",
      "read-main ai-packages/qa-factory/scripts/driver_s0.py 550-565",
      "read-main ai-packages/qa-factory/scripts/driver_dialog.py 300-345, 622",
      "read-main ai-packages/qa-factory/scripts/controller.py 230-262, 1157-1163, 3677-3800, 5455-5490, 5585-5625, 6410-6430, 7735-7745, 9920-9990",
      "read-main ai-packages/qa-factory/scripts/driver_stage_s6.py 262-300",
      "read-main ai-packages/qa-factory/scripts/driver_stage_s7.py 340-356",
      "read-main ai-packages/qa-factory/references/conductor-actions.json 66-80",
      "read-main ai-packages/qa-factory/scripts/tests/test-layers.json keep and quarantine",
      "read-main ai-packages/qa-factory/scripts/tests/test_no_move_seam_n2b_n15.py 1-45, 455-486",
      "read-main ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json 990-1010",
      "read-main plans/piles/live-run-fvf/batch-1-live-run-fvf.md 30-50 and the FV1-6 finding",
      "docs/TESTING.md",
      "docs/SIBLING_MAP.md axis list, axes 5 and 13"
    ],
    "reruns": []
  }
}
```
