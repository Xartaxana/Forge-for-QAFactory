# t-1195 — critic on plan: FV3-22 (FV3-21c) card, the skill road closes S6's manual half

Reviewed: `docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card.md` (whole, Lead decisions included).
Base: `main` da47f648 + branch head a1e9a77a (FV3-21b), and the UNCOMMITTED fix round t-1186 in worktree
`.claude/worktrees/agent-af279738b46568113` (HEAD 80923ed2 = a1e9a77a merged with origin/main; dirty: `story_step.py`,
`driver_stage_s6.py`, `known_red.json`, two tests, a changelog fragment). Line numbers below are at a1e9a77a unless "WT" (worktree).

**Verdict: NEEDS WORK (fit_with_fixes): 5 findings block the builder dispatch, 7 minor fixes.** The design is
sound and doable: F1 (a) one survivor over a road, F2 (a) the close inside the same `start`, Driver methods that keep their
names. What blocks the dispatch is the card text: one Lead decision (F3) is not carried into the card, one gate predicate is
narrower than the shared one, one import edge is not named, re-entry after a close is not specified, and the fix round now
in progress moves exactly the code this card moves.

## 1. Load-bearing facts checked by trail

| claim of the card | checked | result |
|---|---|---|
| X1 `not block` :1045-1047; X2 word branch :1059-1076; X3 every-refused :1084-1090; `start` :913-916; `_manual_block_door` "nothing was dispatched" :1108-1111 | read `story_step.py` 905-925, 995-1130 at a1e9a77a | hold |
| `manual_close` :1050-1075 (head :1058-1066, tail :1067-1075); `consumer_need_record` :313-347; `CONSUMER_ROUTES` :148-160; `consumer_pending` :172-181; `accepted_at` :224-234; `consumer_person_pass` :236-269; `person_pass` :271-311; `file_passed_over` :1972-1992; `stage_S6` auto_done :512-514; `run_manual_block` → `manual_close` :1642-1645 | read `driver_stage_s6.py` 140-355, 500-520, 600-612, 1040-1080, 1628-1645, 1965-1995 | hold |
| `close_by_code` `driver_stage_s7.py:763-786` (completed check first, then finalize, fresh, receipt, passed_over, record) | read 755-790 | holds |
| `code_only` :2536-2551 / `close_receipt` / `record_close` :2565-2581 | read `driver_dispatch.py` 2530-2585 | hold |
| `controller(...)` = CLI subprocess `driver_runner.py:391-405` | read | holds; in-process `Controller.apply("code_only")` does the same passed_over enrichment (`controller.py:5125-5133`), so `SkillRoad.controller` = `apply` is equivalent |
| `driver-layers.json:5-8` allowed_importers = two rows (story_step→driver_timing, run_counters→driver_timing); rows :664, :698-704, :733, :1069 | read lines 1-14 + row grep | hold. **But see F4: the fix round adds a third need** |
| test-layers keep rows `test_story_run_s6.py` :6174, `test_story_step_manual_block.py` :6360, quarantine head :7208 | grep at a1e9a77a | hold |
| census row `_manual_block_check` (shape/data) | `judgment-census.json:1124` | holds |
| "story_step writes no code_only" | `git grep -c "code_only\|code-only"` over story_step.py + stage_done.py | story_step 0 hits; positive control stage_done.py 1 hit |
| "the driver never runs `start --execution-kind manual`" | `git grep -i execution-kind` over `driver_*.py`, `story_run.py` | only `driver_dispatch.py:666` (automation) + a docstring at `driver_stage_s6.py:1630` |
| `where` moves past an awaiting stage | `controller.py:9241-9271` | holds (`awaits_acceptance` moves `i`) |
| `stage_done --status done` refuses S6 without consumer record / controller acceptance | `stage_done.py:1213-1252` | holds |
| test helpers `real_story` :48, `start` :80, `accept` :113, `main` :815; K-R/K-P2/FV3-21b rows have no automation runner | read the def list + awk over 355-421, 668-812 | hold (only manual blocks are accepted there, so they hit E1) |
| s6.md card line 6 / line 10; `CARD_MAX_BYTES` 4000 | read s6.md 1-12, `story_step.py:3210` | hold; the card section is 3168 bytes today (awk byte count), so K5.i's ~430 bytes fit |

## 2. Blocking findings

**F1 — the Lead decided F3 = (a), but the card never adopted it (spec defect, CLAUDE.md rule 11).** The decision adds an
`awaits` position to `story_progress.progress`, for both roads, S6 and S7. The card still says the opposite. §0 `non-goals:`
reads "story_progress.py (fork F3)". `owns:` has no `scripts/story_progress.py`. No K-item, edge, test row or F5 split
assignment carries it. A builder dispatched from §0 can't write the file (owns is normative), and nobody has stated which
node (-1 or -2) does the work. **Fix:** add a K-item (K5.k) for the position kind. It reads `acceptance.awaits_acceptance`
(the one reader) and takes its words from `stage_close.CONSUMER_ROUTES[...]["who"]`. Also state:
- its edges: S6 and S7 both awaiting; an unreadable state;
- the driver road, where the same line shows;
- its test row (in `test_story_step_manual_block.py`, which already imports `story_progress`);
- the owns line and the non-goals edit;
- the node that carries it (FV3-22-2).

**F2 — the "live S6 dispatch" check (step 4 of K5.e, E4, C11) looks only at `status == "running"`. The one shared predicate
counts running, blocked and paused (AR-15, AR-28/FR-59).** The fix round makes `live_s6_scopes(state)` the one predicate
(WT `driver_stage_s6.py`, a new module function). It covers `("running", "blocked", "paused")` and is already called by the
skill road's word branch (WT `story_step._no_stand_refusal`). The controller's own close refusal counts only `running`
(`controller.code_close_facts:916-918`), so it is no backstop. Concrete scenario:
1. World W, plus a manual block TC-2..TC-4 that is `paused`.
2. `manual_done_cases` does not count TC-2..TC-4 as done, so step 6 calls `prepare_for_block` on them. That rewrites their
   `request.json` (`manual_evidence.prepare_for_block` → `prepare_to_file`). Under the word it overwrites them with a
   `left_unchecked` refusal.
3. If they all refuse, `manual_half_close` runs and the `code_only` receipt lists the paused walk as passed over.
4. S6 closes by code over a walk that is only paused.

The card's ERROR DIRECTION paragraph says the gate may err only toward "something is left". This case errs toward closing.
**Fix:** CK3/step 4/E4 use the one predicate (`live_s6_scopes(state)` non-empty → None). C11 gets a `paused` variant. See F5
for where the predicate lives.

**F3 — the moved bodies depend on `driver_core`, which contradicts "stage_close imports no driver_*" and "AR-20: no ratchet
raised". The card never names this edge (rule 11: an edge its own requirements create).**
- `person_pass` writes `--quote f"{BY_PERSON} - ..."`. `BY_PERSON` is defined at `driver_core.py:411`, and its layer-map row
  (`driver-layers.json:82`) says "writer and reader share it". The reader `consumer_close_words` stays in the Driver.
- `code_only` hashes evidence with `driver_core._sha` (`driver_core.py:303`, imported at `driver_dispatch.py:18`).

K5.a says "bodies moved verbatim". That leaves the builder three bad options:
- import `driver_core` from `stage_close`: an L11 refusal (`test_driver_layers.py:l11_problems`), or a new `allowed_importers`
  row, which raises the AR-20 ratchet;
- copy the constant: two definitions of one contract string (AR-13);
- STOP.

**Fix:** state the home. Recommended: `BY_PERSON` moves to `stage_close`, and `driver_core` re-imports it (a family module
importing a non-family one is legal, as `waiver`); the `driver-layers.json:82` row is updated in the same commit if L-checks
require it. `code_only_request` hashes with `hashlib.sha256(path.read_bytes()).hexdigest()` through one helper in
`stage_close`, which `driver_core._sha` may delegate to (or the copy is named in the clone ratchet answer). Name both in §2.1
and in the AR-13/AR-20 rows.

**F4 — what happens when `start` runs again after the close is not specified, and the card's own rows E9, E14 and C9 make it
unsafe.** `story_step.start` has no guard for a completed stage before `_manual_block_check` (read 887-916). On re-entry:
- **(a) E14/C9:** `manual_half_close` runs `finalize_task.py` again before `close_by_code` sees `completed`. That rewrites
  `work/run-report.json`, whose sha256 the receipt already holds (`code_only`'s `evidence_refs`). By then S7 may be working
  from it. The driver never re-enters `manual_close` after S6 completes; the skill road can, every time the orchestrator
  re-runs `start`.
- **(b) E9 then a later `start`:** the receipt is written, then `stage_done --status done` is refused (exit 2 with the door).
  Run `start` again: `close_by_code` sees `completed`, prints "completed already" and returns True without `record_close`
  (`driver_stage_s7.py:772-775`). `_s6_manual_close` then prints "S6 is closed by code", exit 0. The stage record was never
  written. That is a false success. The driver avoids it with `Refusal.retry` / the deferred record (C2-8). The skill road has
  neither. The orchestrator is likely to re-run `start`, because E8's door says "run this start again".

**Fix:** a step 1b in K5.e. With the controller holding S6 `completed`: no reducer, no plan. If the pipeline's S6 record is
done, print one line ("S6 is completed already") plus the S7 card door, exit 0. Otherwise print the E9 door (the exact
`stage_done.py ... --status done ...` command), exit 2. C9 asserts that `finalize_task.py` is NOT called again. Add a C9b row
(E9, then `start` again → the record door, never "closed").

**F5 — the fix round t-1186 (WT, uncommitted) moves code this card moves. The card was drafted against an earlier state; give
the builder merge instructions.**
- (a) `consumer_need_record` has been split: the marker writer and the awaits print now live in a new
  `Driver.consumer_await(stage, author, state, route)`. The print now uses `acceptance.consumer_of(stage)`. The card's
  `need_record` row (":313-347, the one marker writer lives here") and the road members must take `consumer_await` too: move
  its body to `stage_close` as well (one `atomic_json`). A name collision is waiting: `Driver.consumer_awaits` (a different
  method, `driver_stage_s6.py:163`, layer row :697) already exists.
- (b) The X2 word branch is now `story_step._no_stand_refusal(task, state, block)` (WT). It skips cases already in
  `manual_done_cases` ("checked already by an accepted block") and returns [] under a live S6 dispatch. So the card's X2
  `spent` must hold ONLY the cases that got a refusal line, never the "checked already" ones. Otherwise they are counted as
  "not checked" in the close reason and their request paths become receipt evidence. K5.e's planned `_refuse_by_word` should
  reuse the per-case body `_no_stand_refusal` already holds, through one neutrally named helper (see m3).
- (c) `story_step` now does `from driver_stage_s6 import live_s6_scopes` (WT). That is a non-family script importing a family
  part. L11 refuses it unless the fix round adds an `allowed_importers` row (none added in the WT diff yet). FV3-22 is the
  natural place to undo it: move `live_s6_scopes` into `stage_close` (pure, non-driver). `Driver.s6_live_scopes` and
  `story_step` both import it from there. Delete any `story_step.py → driver_stage_s6` row the fix round added (a shrink, AR-20).
  Then the F2 predicate has one home both roads already import.
- (d) The line numbers of §1.1, K5.e, K5.f and the X2 span move with (a)-(c). The builder starts from the fix round's merged
  head, not a1e9a77a.

## 3. Minor fixes (in this round, not deferred)

- **m1 — stub invariant.** `manual_half_close` computes evidence "via `manual_evidence.request_path`". `Driver.manual_request_paths` is stubbed in tests
  (`test_story_run_s6.py:343`, `test_walk_lanes_parallel.py:124`, `test_story_run_s6_w1_frozen.py:134`, `test_silent_passes.py:723/737`).
  §2.1's own rule ("every step through the road's member") requires `road.manual_request_paths(cases)`. Add it to the road
  members; `SkillRoad` implements it with `manual_evidence.request_path`.
- **m2 — the K5.e return shapes disagree.** The signature says `-> tuple | None`, but step 5 returns the str `"automation"`.
  Step 7's success value `("done", [lines], <line>, 0)` has 4 elements, while the error value and K5.f's unpacking
  `("done", lines, code)` have 3. Pick one shape (e.g. always `(kind, lines, code)`) and write it out.
- **m3 — census.** The helper name `_refuse_by_word` matches `UNIT_NAME_RE` `^_?refuse` (`test_judgment_census.py:77`). That
  creates a new census unit, which the card itself says makes the builder STOP. Use a neutral name, or reuse the fix round's
  `_no_stand_refusal` body.
- **m4 — ordering of the printed lines.** `stage_close` prints directly (the awaits line from `need_record`/`consumer_await`,
  "completed already", the dry line). `start` prints the returned lines afterwards. So the §2.3 order ("case lines, then the
  awaits line, then next") is reversed. State the order the code actually gives, or have the module return lines on the skill
  road.
- **m5 — Q-a3 / AR-25.** The awaiting state's only stated exit on the skill road is "after its record, run the same start".
  Nothing on the skill road is known to record the analyst's S6 acceptance. `--acceptance` occurs in `phases/s2-s4.md` and
  not in `s7.md` (case-insensitive grep over the package `*.md`; positive control `s4.md:27`). The person's word
  (`waiver.py --stage S6 --block "stage acceptance"`, row C3) is a real exit, but the awaiting lines and K5.i never name it.
  Fix: the awaiting `next:` text and K5.i also name the person's-word door, so the state has a door that works today.
  Q-a3 itself can stay with FV3-24, as the Lead decided.
- **m6 — node ids.** §0 still reads `node: live-run-fvf/3/FV3-21c`, and F5/§0 say FV3-21c-1/-2, FV3-21d. Per the Lead decision
  they become FV3-22-1/-2 and FV3-24. The batch file has no FV3-22-1/-2 rows (`batch-3-live-run-fvf.md:51-53`). Either add
  them, or run one node with two task_ids. Also: under the F5 split, node -1 owns `test-layers.json`, but the `covers` edit is
  in K5.j (node -2). Node -1's `--witness-for stage_close.py` then has no row naming the tests that judge the new file. Move
  the `covers` edit into node -1.
- **m7 — detector reach.** Audit A27 (U: a `self.py` result that is dropped) scans only the driver set
  (`audit_factory.py:1652, 2381`). The `road.py` calls moved into `stage_close` leave its reach. No baseline row is affected:
  grep finds none for the moved names. Name this in §1.3 (AR-18/AR-29 row): either add `stage_close.py` to A27's file set or
  state it as a residual.

## 4. Feasibility of the move (DoD key 2)

The move is feasible, and Driver behaviour can stay the same, subject to F3, F5(a) and m1:
- Every member the free bodies use exists on the Driver today: `task`, `task_root`, `project`, `dry` via getattr,
  `controller_state`, `pipeline`, `py(check, expect)`, `owe_row(what, stage)` (`driver_runner.py:263`, never raises),
  `close_receipt`, `record_close`, `file_passed_over`.
- `Refusal.__init__` takes `title: str = ""` (`driver_core.py:114`), so `raise Refusal(str(exc), title=exc.title)` gives the
  same object as the bare raise today.
- `close_receipt` reads `refusal.title == "code_only_evidence"` after the `code_only` delegate converts, so it is preserved.
- Moving `consumer_person_pass`'s retry into the delegate is equivalent. The only Refusal source inside is `road.person_pass`
  → `road.py(check=True)`; `owe_row` and `accepted_at` never raise.
- The stubs in the test suite are on Driver attributes (`code_only` ×13, `person_pass`, `record_close`, `consumer_need_record`
  in the quarantined `test_refuse_case.py`). They keep working as long as the free bodies call `road.<member>`.
- `SkillRoad.controller` = `Controller.apply`: the passed_over enrichment of `code_only` is in `apply` (`controller.py:5125`),
  not in the CLI, so both roads get the same receipt.

## 5. The Lead decisions

- **Node ids:** OK, but the card body was not updated (m6).
- **F1 = (a):** agree. (b) costs three importer rows (AR-20); (c) adds a conductor command (FR-48). Conditions: F3, F5(c).
- **F2 = (a):** agree. FR-48/AR-17: the stage's own call does the close. `where` is read-only. K5.h's widened test changes no
  existing outcome: every refusal return of `_manual_block_check` has code 2 (read 1028-1091).
- **F3 = (a):** acceptable in substance, but not carried into the card (F1).
- **F4 = (a):** acceptable. FV3-24 is a row in the SAME batch with an executor (`batch-3-live-run-fvf.md:53`), so nothing
  leaves the round (rule 9). Note: the FV3-24 row text names only the re-proof and Q-a3. It should point to the five §7
  sites by name, so `s6.nothing`, `s6.results_stand`, `s6.accepted` and `s6_reentry` are not dropped at close.
- **F5 = (a):** agree, with the m6 split correction. One critic pass after node -2 (R13-g).
- **Q-a3 → FV3-24:** acceptable only together with m5 (a door that works now, in the awaiting state).

## 6. AR-n named and kept

- **AR-13:** kept, provided F3 (one `BY_PERSON`) and F2 (one live predicate) are fixed.
- **AR-15:** kept by the design. Weak spots: CK3 (F2), the X2 word loop (F5b), and step 6's remaining-cases list duplicating
  `_manual_block_door`'s (`story_step.py:1104-1106`): one helper.
- **AR-20:** "ratchets raised: none" holds only with F3 and F5(c) fixed. Otherwise either an importer row is added, or the fix
  round's row is kept when it could shrink.
- **AR-22:** kept. The producers now exist on the skill road; the readers are unchanged.
- **AR-21:** broken on re-entry (F4a).
- **AR-25:** depends on m5.
- **AR-28:** broken by F2 and F4b.
- Other AR rows (9, 14, 17, 19, 23, 24, 27, 29): consistent with the design. AR-29 needs m3 and m7.

## 7. Edges complete per rule 11?

No: F2, F3, F4 and F5(b) are edges the card's own requirements create and leave silent.
- TEMPORAL: E15 covers the module being absent or present. It misses the temporal world the card itself creates: the second
  `start` after a close (F4).
- POSITIONAL: K5.f's invariant is right for X1-X3. But at X1 the change now runs `prepare_for_block`, which WRITES
  `request.json`, where X1 wrote nothing before (the FB-9 "nothing written before a refusal" invariant at
  `story_step.py:909-910`). State that X1's `left` outcome now writes the request files of the cases it prepared, up to the
  first ready one, and that this is accepted.

## 8. Standing questions

- **DUPLICATION AND CONSISTENCY:** findings F2, F3 (a copied constant/helper is the fallback the card does not forbid), F5(b),
  and the AR-15 note on step 6. `SkillRoad.py` beside `story_step._run` is a justified second runner (opposite error
  direction, named in §9).
- **CODE QUALITY:** m2 (mixed return shapes), m4 (output order).
- **ONE ROAD (P31/Q12):** the shared close is reached by both roads. The skill-road plan (step 6) is a branch serving its own
  condition: `walk_retry` and deferred questions are driver state the skill road does not have. So it is not an exclusion.
  But inside `story_step` it should share `_manual_block_door`'s remaining-cases computation. FV3-24 carries the other S6
  sites as a node with an executor.
- **TESTS (Q5):**
  - The DoD has no `test: <file::row> | expected from: <§>` line per behaviour item (TESTING.md «Строка теста в DoD»).
    K5.e-K5.i each need one (→ C1-C11, §2.3/§4). K5.a-K5.d need `test: none -- поведения нет | expected from: §2.1`.
  - Rows to add: C9b (F4b), a C11 `paused` variant (F2), and the F3 position row.
  - The volume rule: §5 adds 12 rows against ~300 moved/added code lines. Volume looks inside budget. The builder reports
    the `in N.NNs` tail of `test_story_step_manual_block.py` (10 s file budget, 12 `real_story` worlds).

## 9. Class completeness (SIBLING_MAP)

- **axis 5:** covered. The "Code-only stage closes" row (:130) and "Skill phase <-> driver" (:133) are edited in K5.j. The
  other S6 code steps are node FV3-24.
- **axis 26** (the stand word: one reader ↔ the places that ask): **not covered.** The card adds a new site that reads the
  word (`_s6_manual_close` step 6, via `waiver.stand_passing_word`). Axis 26's text still lists neither
  `stand_passing_word` nor its skill-road callers (`grep -c stand_passing_word` docs/SIBLING_MAP.md = 0 on main and on
  a1e9a77a). FV3-22 owns `docs/SIBLING_MAP.md`, so K5.j adds one clause naming `waiver.stand_passing_word` as the reader for
  both roads, with its callers (`Driver.s6_stand_word`, `story_step._no_stand_refusal`, `story_step._s6_manual_close`) —
  unless t-1186 already does.
- **axis 19** (a role file's `tools:` line): n/a. No role file or tools line is touched.
- **axis 34:** covered by FV3-24 as a named node.
- **axis 38** (driver-exits dry census): no row of `driver-exits/*.json` names a moved site (grep of the fixtures for
  `consumer_need_record|manual_close|close_by_code|code_only_evidence|finalize_task.py exit` hits only `known_red.json:6`,
  the FV3-21 label).

## 10. Trail

Read (worktree and a1e9a77a via `git show`):
- the card, whole;
- `story_step.py` 140-152, 318-347, 862-925, 995-1130, 3210, 3255-3300;
- `driver_stage_s6.py` 1-20, 140-355, 500-520, 600-612, 946-975, 1040-1080, 1333-1400, 1628-1645, 1965-1995;
- `driver_stage_s7.py` 755-790; `driver_dispatch.py` 1-20, 2530-2585; `driver_runner.py` 263-275, 380-406;
  `driver_core.py` 100-125, 300-310, 391-412;
- `controller.py` 890-975, 5073-5150, 9241-9272; `acceptance.py` 1471-1504; `manual_evidence.prepare_for_block`;
  `stage_done.py` 1213-1252; `waiver.stand_passing_word`;
- `driver-layers.json` 1-17 + row grep; `test_driver_layers.py` 528-580; `test_judgment_census.py` 14-40, 77;
  `judgment-census.json` 1-14, 1122-1126; `test-layers.json` row grep; `test_story_step_manual_block.py` def list + world
  greps; `test_silent_passes.py` 715-750;
- `audit_factory.py` 1645-1670, 2370-2392; `docs/SIBLING_MAP.md` axis heads, 128-134, axis 26, axis 34;
- `phases/s6.md` 1-12; `batch-3-live-run-fvf.md` 51-53; `docs/TESTING.md` 55-90, 204-218;
- the WT diff of `story_step.py` / `driver_stage_s6.py` (fix round t-1186).

Greps, each with a positive control:
- `code_only|code-only` count: story_step 0 / stage_done 1;
- `execution-kind` (-i) over the driver set: only `:666` automation;
- `--acceptance` (-i) over package `*.md`: s2/s3/s4 hit, s7 none;
- `BY_PERSON` definition: driver_core only, acceptance none;
- test stubs of the moved members: 30 lines;
- A27 baseline for the moved names: none (control: the baseline rows read at :1668+);
- `stand_passing_word` in SIBLING_MAP: 0 on both trees (control: the axis 26 head found at :453).

No test runs: a plan review, so no mechanical layer applies. `UNIT_NAME_RE` was read from the file, not executed.

The decisions on these findings belong to the Lead (rule 6). The card's resubmission is a Lead edit under the same task (rule 2).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1: Lead decision F3=(a) is not carried into the card: non-goals still exclude story_progress.py, owns lacks it, and there is no K-item, edge, test row or F5 node assignment",
    "F2: the live-S6-dispatch gate (K5.e step 4, E4, C11) checks only running; the one predicate live_s6_scopes (running/blocked/paused) is required; a paused walk is re-prepared, its request overwritten, and S6 closed by code over it",
    "F3: the moved bodies need driver_core.BY_PERSON (person_pass) and driver_core._sha (code_only) while stage_close may import no driver_*; the home or the delegation must be named, or AR-13/AR-20 break",
    "F4: re-entry after the close is unspecified: start re-runs finalize_task over a hashed run-report on a completed S6 (E14/C9), and after an E9 record refusal a second start reports closed without ever writing the stage_done record",
    "F5: the uncommitted fix round t-1186 moves the same code (consumer_await split, _no_stand_refusal with the done skip, story_step importing driver_stage_s6.live_s6_scopes); the card needs merge instructions, X2 spent must exclude the checked-already cases, and live_s6_scopes should move to stage_close"
  ],
  "fixes": [
    "F1: add K5.k (awaits position via acceptance.awaits_acceptance, words from stage_close.CONSUMER_ROUTES) with edges, a test row, owns story_progress.py, non-goals edited, node FV3-22-2",
    "F2: CK3/E4/step 4 use live_s6_scopes(state); add a C11 paused variant",
    "F3: home BY_PERSON in stage_close with driver_core re-importing it (layer row :82 updated if required); one sha helper in stage_close; name both in section 2.1 and the AR-13/AR-20 rows",
    "F4: K5.e step 1b: S6 completed -> no reducer; pipeline record done -> completed line plus the S7 door, exit 0; else the E9 stage_done door, exit 2; C9 asserts no second finalize; add C9b",
    "F5: rebase the card on the fix-round head: move consumer_await with need_record; X2 spent = refused lines only; reuse _no_stand_refusal's per-case body; move live_s6_scopes into stage_close and drop any story_step->driver_stage_s6 importer row",
    "m1: add road member manual_request_paths(cases); manual_half_close calls it",
    "m2: one return shape for _s6_manual_close; fix the 4-element success tuple",
    "m3: a helper name outside UNIT_NAME_RE (not _refuse_*), or reuse _no_stand_refusal",
    "m4: state the actual print order (module prints first) or return lines",
    "m5: the awaiting next line and the K5.i text also name the person's-word door (waiver --block stage acceptance)",
    "m6: update node ids to FV3-22-1/-2 and FV3-24 in section 0/F5, add batch rows or use one node; move the test-layers covers edit into node -1",
    "m7: name the A27 reach for stage_close (add it to the scanned set or state the residual)",
    "axis 26: K5.j names waiver.stand_passing_word and its callers on axis 26 unless t-1186 does",
    "tests: add test/expected-from DoD lines per behaviour item (K5.e-K5.i, F3) and test: none for K5.a-K5.d; builder reports the test file's timing tail",
    "positional: state that X1's left outcome now writes request.json for the prepared cases (FB-9 note)",
    "FV3-24 row text: name the five section-7 sites, not only the re-proof and Q-a3"
  ],
  "class_completeness": "axis 5 covered (rows :130, :133 in K5.j; other S6 code steps are node FV3-24 in the same batch); axis 26 NOT covered: the new stand-word reader site and waiver.stand_passing_word are absent from the axis text (0 hits on main and a1e9a77a); axis 19 n/a (no role tools line touched); axis 34 covered via FV3-24; axis 38 no fixture row names a moved site; in-artifact: the X2 word loop and the remaining-cases list duplicate existing story_step code (F5b, AR-15 note)",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-fv3-21c-skill-road-s6-close-card.md",
      "ai-packages/qa-factory/scripts/story_step.py@a1e9a77a 140-152,318-347,862-925,995-1130,3210,3255-3300",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py@a1e9a77a 1-20,140-355,500-520,600-612,946-975,1040-1080,1333-1400,1628-1645,1965-1995",
      "ai-packages/qa-factory/scripts/driver_stage_s7.py@a1e9a77a 755-790",
      "ai-packages/qa-factory/scripts/driver_dispatch.py@a1e9a77a 1-20,2530-2585",
      "ai-packages/qa-factory/scripts/driver_runner.py@a1e9a77a 263-275,380-406",
      "ai-packages/qa-factory/scripts/driver_core.py@a1e9a77a 100-125,300-310,391-412",
      "ai-packages/qa-factory/scripts/controller.py@a1e9a77a 890-975,5073-5150,9241-9272",
      "ai-packages/qa-factory/scripts/acceptance.py@a1e9a77a 1471-1504",
      "ai-packages/qa-factory/scripts/manual_evidence.py@a1e9a77a prepare_for_block",
      "ai-packages/qa-factory/scripts/stage_done.py@a1e9a77a 1213-1252",
      "ai-packages/qa-factory/scripts/waiver.py@a1e9a77a stand_passing_word",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json@a1e9a77a 1-17 + row grep",
      "ai-packages/qa-factory/scripts/tests/test_driver_layers.py 528-580",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py 14-40,77",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json@a1e9a77a 1-14,1122-1126",
      "ai-packages/qa-factory/scripts/tests/test-layers.json@a1e9a77a row grep",
      "ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py@a1e9a77a def list and world greps",
      "ai-packages/qa-factory/scripts/tests/test_silent_passes.py@a1e9a77a 715-750",
      "ai-packages/qa-factory/scripts/audit_factory.py@a1e9a77a 1645-1670,2370-2392",
      "ai-packages/qa-factory/skills/qa-story/phases/s6.md@a1e9a77a 1-12",
      "docs/SIBLING_MAP.md@main axis heads,128-134,axis 26,axis 34",
      "plans/piles/live-run-fvf/batch-3-live-run-fvf.md 51-53",
      "docs/TESTING.md 55-90,204-218",
      "worktree agent-af279738b46568113 uncommitted diff of story_step.py and driver_stage_s6.py (fix round t-1186)"
    ],
    "reruns": []
  }
}
```
