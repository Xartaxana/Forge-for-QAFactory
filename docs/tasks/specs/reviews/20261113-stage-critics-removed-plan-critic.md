# Critic on PLAN — stage critics S2/S3 removed; S6/S7 consumer one round, no barrier

Spec under review: `docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md` (designer draft, 623 lines, read whole).
Code: read-main `C:\QAFactory\forge-repo\.claude\worktrees\read-main` at `12317b6` (checked: `git log -1` prints `12317b6 wave 2 integration report`).
Every `file:line` below is under `ai-packages/qa-factory/` on that tree unless another path is given.
Role: critic, plan gate (PROJECT.md «новая идея», step 6). This verdict is an input to the Lead's acceptance, not the acceptance.

**Verdict: fit_with_fixes (NEEDS WORK).** The direction holds, and so do the owner-fidelity and the two Lead forks (F2 (a), F4 (a)).
Seven blockers must be fixed in the spec text before any builder starts. Each one is a text edit the Lead can make. A second critic
pass is needed only if the Lead takes B-1 by moving `TRIED_READERS` into `stages.json`, because that changes the design. Otherwise the Lead
checks the edits.

---

## BLOCKERS (fix in the spec before any builder)

**B-1. `acceptance_reads.author_form` is a second road for an action that already has a table and a reader (P31, AR-15, AR-13; brief item 12).**
`brief_pack.py:112` has `TRIED_READERS = {("S9", "qa-retro-analyst"): (("S8", "qa-doc-scribe"), ("S8", "qa-bug-reporter"))}`.
Its reader is `tried_reader_names` (`brief_pack.py:3636-3644`, docstring: "the forms whose `tried` table has a reader that is not a
stage critic"). It hands an earlier author's `last_accepted_form` to a later role's brief. A.2.3's `author_form` part does exactly
this for (S4, qa-case-critic) ← (S2, qa-requirements-tester), through a new key and a new branch inside `stage_critic_names`.
The spec never names `TRIED_READERS` (its §T search list has no `tried_reader` term).
Text to change in A.2.3: replace `"acceptance_reads": {"S2": ["outputs", "advice", "author_form"]}` with
`"acceptance_reads": {"S2": ["outputs", "advice"], "S3": ["advice"]}`, and add: "The tester's form, which holds `tried`, reaches the S4 case
critic through the ONE existing table `brief_pack.TRIED_READERS`: add the row `("S4", "qa-case-critic"): (("S2",
"qa-requirements-tester"), ("S3", "qa-test-strategist"))`. Its reader `tried_reader_names` is unchanged. No `author_form` part." Move
the J1 assertion "the tester's last accepted form" onto that road. Alternative, larger: move `TRIED_READERS` into `stages.json` beside
`acceptance_reads` and migrate the S9 row in the same node (AR-1). If the Lead takes this one, it changes the design and needs a second
critic pass. See B-1b for why S3 is in the row.

**B-1b. The S3 strategist's `tried` table and handoff form lose their only reader (AR-22).**
Today `stage_critic_names` hands the S3 critic `last_accepted_form(task_root, "S3", roles[0])` (`brief_pack.py:3576-3578`). A.2.3 hands the
S4 critic only S2's form and S3's advice. After A1, the strategist's form has no reader. Yet A.3 keeps telling the strategist "what
you tried is the `tried` table of your handoff form". §1.1's AR-21/AR-22 row names only the two advice files. Fix: put the S3
strategist in the B-1 row, as above. If the Lead declines that, write in §1.1 AR-22 why a form with no reader is legal (I see no such
reason).

**B-2. Live (non-quarantined) checks go red, and no node owns them (K8).** I grepped the S2/S3-only tokens over `scripts/tests` and
checked each file's quarantine status in `test-layers.json` (`quarantine` section; control: `test_stage_critic_route.py` is reported
QUAR, as §O says). Live files that break after A1 and are missing from A1's `owns`:
- `scripts/stage_guard.py:3088-3089`, the embedded selftest case `stages_of_role(model, "qa-case-critic") == ["S2", "S3", "S4"]`. It is run by the
  live `tests/test_stage_guard.py:2134` (`run_script("stage_guard.py", "--selftest")`). `stage_guard.py` is a hot file, so this needs a
  function-list owns line: `stage_guard.py (selftest(): the two case lines :3088-3089 only)`.
- `tests/test_handoff.py:670`: `forms = (..., "s2-stage-critic-to-tester", "s3-stage-critic-to-strategist")`. It parses the two contracts A1 deletes.
- `tests/test_question_register.py:1928`: it loads `handoffs/{name}.yaml` for the same two contracts.
- `tests/test_story_run_first_look.py:44`: it calls `d.s3_author_done()`, which A1 deletes.
- `tests/test_first_look_briefs.py:28` (`PAIRS` holds `("S3", "qa-case-critic")`), `tests/test_first_look_wiring.py:126`, `tests/test_brief_s3_roster.py:85`.
  All three iterate the `FIRST_LOOK_KIND` S3 critic row that A1 deletes. They are likely red; the node reads each one first.
Text to add to A1's `owns`: the seven paths above (the rows named, nothing else). Add to the DoD: "the live files `scenario_walk.py
--witness-for` prints for these owns are green, or run on CI where they are slow".

**B-3. The S7 gap misses the report on three of its paths (AR-27, FR-41).** The gap for S7 is recorded inside the SCRIBE's finish
(`driver_stage_s8s9.py:80`: `consumer_completion("S7", True)`). That is after the scribe's brief was built. So B2-5's new
`not established:` brief line can never carry S7's own gap. For the 1-of-1 path, B2-5 instead relies on the scribe naming the gap
because the round line told it. That leaves three paths where the scribe was told "a round left" and the gap still lands:
the verdict word is unreadable (E-B6), the scribe's form is refused, or the brief-time count goes stale before the verdict (E-B4).
On all three, S8 closes on `own() = True`, `rebuild_report` runs, and gate B shows a report with no word of the gap. A writer for
this already exists: `stage_done.py --warn TEXT` (`stage_done.py:1533`, appended into `pipeline["warnings"]` at `:178-190`).
`brief_pack.py:1819-1824` already reads those warnings, and so does the gate packet.
Text to change in B2-3 / B2-5: "`consumer_gap` adds `--warn \"{stage} was accepted with a gap: {why}\"` to the SAME `stage_done.py
--acceptance` call. That is the one writer of `pipeline["warnings"]`. The S6 gap then reaches the scribe's brief through the existing warnings loop.
The S7 gap reaches gate B's packet through it. The node checks which label `gate_brief._not_established` gives the line. If the label
is `standing`, the scribe charter line (B3) says that a `standing:` line beginning `S6 was accepted with a gap` or `S7 was accepted
with a gap` goes under Factory defects." Then delete B2-5's second reader of the acceptance records, which duplicates the warnings road (AR-15), and
add a G6 row `s7-gap-after-scribe-brief-reaches-gate-b`. `rebuild_report` and the report_facts check stay unchanged; FR-37 is kept.

**B-4. Two in-flight states get the wrong road on the new package (K6, AR-25).**
(a) `driver_s0.py:525-541` (`ticket_rework_step`) picks the author to re-run as `roles[-1]` among the ACCEPTED dispatches of the stage. S3 is
filtered to `qa-test-strategist` and S1 to `roles[0]`; S2 is not filtered. A 0.11.0 story whose S2 COMPLETED with the critic accepted
last, and whose ticket then changes after the upgrade, therefore calls `rework("S2", "qa-case-critic", cause="ticket_changed",
complete=True)`. `story_step.start` refuses it (`story_step.py:901-905`, not a role of S2), so it becomes a refusal to the conductor.
The same `roles[-1]` choice is a live bug on main today: it re-runs the critic, not the tester. A.5's table covers only OPEN S2/S3 stages.
Fix: add `driver_s0.py (ticket_rework_step: the author filter only)` to A1's `owns`. The rule becomes ONE generic line, "the stage
author is `stages.json` `roles[0]`" (P31), in place of the S1 and S3 special cases. Add T4 to A.5: "S2/S3 completed under 0.11.0,
ticket changes later -> the author (`roles[0]`) re-runs; never the critic". Add a test row T4.
(b) The T2 rule's POSITION contradicts its own invariant. A.4/A1 put it "after `ticket_changed`, before the `rework_of` rule". But the
`ticket_changed` branch (`driver_stage_plan.py:1025-1035`) answers for ANY role at S2/S3: after A1 it returns `True` (S2) or
`s3_ticket_completion()` (S3) without checking the role. So a `qa-case-critic` dispatch with `repair_cause: ticket_changed` (exactly what
(a) creates today on main) would CLOSE S2. That breaks "a dispatch of an undeclared role never closes any stage". Text to change: "T2
sits BEFORE the `ticket_changed` branch, right after the S1 rules". Keep the INVARIANT line and add a T2 row:
`completion_for("S2", "qa-case-critic", {"repair_cause": "ticket_changed"})` is False.

**B-5. The S4 case critic is asked for things its form and its scope rule do not allow (FR-11, FR-38, AR-10; a conflicting pair, CLAUDE.md rule 11).**
(a) A.2.2 makes item 3 name `work/advice-S4.json` AND `work/advice-S2.json` (and S3 per F2). But the critic's contract
`handoffs/s4-case-critic-to-designer.yaml:105` declares `advice_read: "<work/advice-S4.json, or a dash and the reason it was absent>"`, a single
string for one file. Its `inputs` (`:17-26`) also do not list the register sources, `understanding.md` or the S2 form. No node owns this
form. Text to add to A2's `owns`: `handoffs/s4-case-critic-to-designer.yaml (advice_read placeholder names every advice file the brief
hands; inputs gain non-required rows for the S2 outputs and forms)`. Add an edge for what happens when a file is absent.
(b) The register checks are whole-register work. But the critic's scope rule (`agents/qa-case-critic.md:95`) says: "Your scope at S4 is the
plan rows whose `design_review_required` is true ... expand it only for a dependency or new risk, saying why ... on a repair review look
only at changed rows". A sentence of the sources that no requirement holds has no plan row, so it is out of scope by that line. A.2.2
does not touch `:95`. Text to add to A.2.2: "`:95` gains: the register bullet is read once, on the first review round, over the
whole register and its sources, whatever the row scope; a repair round does not repeat it." Add `:95` to A2's `owns` line list.

**B-6. A1's acceptance keys live in files the node is told not to run (CLAUDE.md rule 11, a conflicting pair).** The keys W1, W2, SC-1..3 and T2 are
in `test_story_run_s3_windows.py`, and A1 also edits `test_story_run_freshness_k6_k7.py`. The common non-goals forbid "local runs of slow files
(`test_story_run_*` slow list ...)" (PROJECT.md: `test_story_run_*` is the slow pattern). As written, the builder cannot produce the
witness the DoD asks for. Text to change in A1's DoD: "W/SC/T2 rows: the witness is the branch's CI run (RUNBOOK §7), read through
`tools/ci_read.py`. The local witness is the fast files `scenario_walk.py --witness-for` prints." Alternatively, move these rows to a fast
keep file that the witness command names.

**B-7. A crossing on the same rows is missing: FV1-12 (K9).** `plans/piles/live-run-fvf/batch-1-live-run-fvf.md:59`: FV1-12 owns
`skills/qa-story/phases/s2.md` and `references/stages.json` (the S2 row). The owner's word on S2 (13.11, finding
`20261112-s2-kartochka-i-reestr-stadij-rashodyatsya.md` on branch `wip/owner-words-1113b`, commit `f876a5c`) says: "нужен ли приёмщик у
реестра требований — владелец не говорила, стоит как есть в `stages.json`". Today's word supersedes that line. FV1-12 edits the same
S2 row as A1 and the same card as node D. Text to add to §X: "FV1-12: same `stages.json` S2 row and `phases/s2.md` -> `очередь: A1 ->
FV1-12` (or fold D's s2.md edit into FV1-12). The Lead notes in the FV1-12 finding that the S2 acceptor question is answered by the
owner's word of 13.11 (removed)."

---

## FIXES (the Lead may apply directly)

F-1. **driver-layers rows are incomplete (AR-20, axis 18).** A.4 lists `driver-layers.json:525-538` but misses `:784`
(`Driver._wait_then_critic`, home driver_machine), which A1 deletes. Part B deletes `consumer_exhausted` (`:686`) and adds
`consumer_gap` and `consumer_round_line`, but B2's `owns` has no `driver-layers.json`. Add `:784` to A.4 and A1. Add
`scripts/tests/fixtures/driver-layers.json (the driver_stage_s6 rows only)` to B2's `owns`.

F-2. **Ratchet references.** A.4's census line says "lowered to the printed count if C3 says". C3 is B1's test row, not a census
output; write "if `test_judgment_census.py` prints it below its ceiling". B2 changes `consumer_completion` and `consumer_settled` (their refusal and seam
calls go), so it can move the census too. Give B2 `judgment-census.json (ratchet values only, as printed)`, with the AR-20 line.

F-3. **Dead code left alive after A+B (K3, brief item 7).** After both parts, `stage_review_exhausted` has S4 as its only caller. That makes
`word = "cases_in_repair" if stage == "S4" else "stage_in_repair"` (`driver_stage_plan.py:744`) a dead branch, and also
`who = acceptance.consumer_of(stage) or ...` (`:702`). A.1's claim "the word stays" (`stage_in_repair`) is true after A only, not after B.
My grep shows `stage_in_repair` lives only in `driver_stage_plan.py` and two quarantined tests. Queue the simplification in node D
or as a residual line with a node id. Do not leave it unnamed.

F-4. **The rework of the author itself failing (K4 i).** In `consumer_settled` (`driver_stage_s6.py:398`), if `self.rework(...)` raises
`ReworkRefused`/`Refusal`, that is a conductor road. Add E-B10 in B.4: "the author's repair round cannot be registered (the controller refuses
`rework`) -> `consumer_gap` with why `the repair round of the {author} could not be started: <refusal[:200]>`; INVARIANT: no
seam, no question". Add a test row G9.

F-5. **On the gap road, the consumer's own completion (K4 ii).** E-B4/E-B6/form-refused: the consumer may have stopped its own work because it
expected a redo. B2-3 returns `own()`. State the invariant that makes this safe: "`own()` is the stage's unchanged rule. An analyst that did not
triage stays open by `s7_open_work`/`s7_fresh`; a scribe report that does not hold is caught by `report_facts --check` at the S9 exit.
The gap road never adds a close the stage's own rule refuses." Add a row G3b in which `own()` returns open work, and assert it passes through.

F-6. **`consumer_gap` on the unreadable path has no author dispatch named.** There `record` is None. Say the author id comes from
`acceptance.stage_author_dispatch(state, stage_def_of(stage))`. Then add the edge: when it is empty, write no record, print one line, and
return `own()`. A stage with no author run is not judged (cf. `consumer_close_refusal`, `acceptance.py:1500-1502`).

F-7. **Two homes for the quote prefixes of a driver accept (AR-13, P31).** `BY_PERSON` lives in `driver_core.py:411` and the new `GAP_PREFIX` goes to
`acceptance.py`. Both read the same field (`quote` of a driver accept). Either put `GAP_PREFIX` beside `BY_PERSON`, or move `BY_PERSON` into
`acceptance.py` with an `accepted_by_person` reader in the same node. Name the choice in B2-4.

F-8. **The reminder text overclaims a reviewer.** A.3's new strategist line says "as the case critic will at S4". After A2 the critic's S3
bullet is gone. The critic still judges coverage against the register (dimension 1, `qa-case-critic.md:40`) and the level of rows
(`:86`), but not "every row a hypothesis". Write "Before you stop, read each item against its witness yourself: no critic judges the plan;
the person reads it at gate A". In A.6, change the AR-29 replacement text in the same way: "held by its author's self-check; the case
critic at S4 sees coverage and level through the cases; the person reads it at gate A".

F-9. **B1 site details.** `stage_status.round_cap(task_root, role)` (`stage_status.py:64-71`) has no stage parameter and reads
`DEFAULT_LIMITS` only. Say what it passes, e.g. a new optional `stage` argument from its caller, or "unchanged: it prints S5/S4 caps only,
and its callers are ..." after a grep. `story_progress.py:357` is the S5 window line (`kind: window`, `round_role` critic/author of S5), so
B1 does not need to touch it; drop it from `owns`, or say why it stays. B.1 says "four sites" and then lists five; fix the count.

F-10. **B1's blast-radius stop is a dispatcher fact left to the builder (CLAUDE.md rule 11 (5)).** I grepped `rework("S6"`/`rework("S7"` in
`driver*.py`. The S7 re-judge uses `cause="reviewer_error"` (`driver_stage_s7.py:1052`, uncounted). The conductor's `seam_rework`
(`driver_machine.py:609`) takes its `cause` from the conductor's words, so it CAN spend a `test_defect` round of the S6 runner. After B2-1
that round is capped at 1. The Lead decides this before dispatch: either accept it and write it as an edge, or make the cap read only for
`consumer` rounds. Don't leave it to the builder to stop on.

F-11. **Manifest form (R11 f).** B1 and B2 `owns` contain `<the keep table file --witness-for prints ...>`, and D's owns are relative paths
with one prefix sentence. `tools/dispatch_manifest.py` refuses both. Run `scenario_walk.py --witness-for` before dispatch and write the
absolute paths.

F-12. **§O is incomplete.** Two more quarantined files go stale with A: `tests/test_handoff_init_author.py` (`:16`, `:43`, `:85-89`
name `s2-stage-critic-to-tester`) and `tests/test_rows_owed.py` (a hit in my grep, not read further). Add both to §O item 1.

F-13. **Two more crossings on shared files (K9).** FV1-25 owns `agents/qa-failure-analyst.md`, the same charter as B3
(`batch-1-live-run-fvf.md:54`). FV1-28 owns `scripts/brief_pack.py` and `first_look.py` (`:61`), next to A1's `FIRST_LOOK_KIND` edit.
FV1-6 item 14 edits `docs/SIBLING_MAP.md:122` (its spec `:314-316`), which is the same line as node D. Add the queue lines to §X.
TQ2-1: only K1 touches `qa-case-critic.md`, `role-rules.json` and `role-load.json` (`git diff --stat origin/main...wip/tq2-1-k1`). K2 touches
`critic_rollcall.py`, `s5_plan.py` and `s5_precheck.py`, so "after BOTH merge" over-constrains A2. Write "after K1".

F-14. **A1 has no test rows for T1 and T3.** §1.1 claims "A1 rows T1-T3", but A1's test list has only T2. T1's road is also unverified.
`controller.py:8549-8560` (`recover`'s second repair) closes a running stage whose LAST role (by `contract.stage_closes_with`,
`contract.py:5797-5802`) was accepted with neither `stage_complete` nor `unresolved` and nothing open. After A1 the tester and the strategist are
the last roles, so a 0.11.0 author dispatch accepted that way can be CLOSED by `recover` instead of re-run as A.5 T1 says. Both roads have a
move, so nothing is stuck, but the spec must state which one fires and add a T1 row that pins it. F4's cost line changes if `recover` closes it
(cheaper).

F-15. **The A2 DoD grep is not deterministic.** `grep -n "S2\|S3" agents/qa-case-critic.md` will hit the new text (`advice-S2.json`, "the S2
tester"). Use a key-presence run with verbatim keys per the doc-dispatch witness rule (the three register phrases present; the strings
"S2: the register", "S3: the plan" and "stage critic of S2, S3" absent; a negative control).

---

## Answers to the keys

**K1 FIDELITY — answered.** Every design choice traces to §0. Part A follows «убираем лишних критиков, оставляем как раньше»: S2/S3 close on the
author's finish, REPAIR_LOOP_ROLES go back to the pre-X2-7 set, and `_s3_completion_gate` goes back to the pre-X2-5 rule. Part B follows «один шанс» (cap 1) and «не должно быть
барьером» (no seam). Nothing new is asked of a person, and no new refusal or barrier is added. I checked the A.2.1 table line by line against
`agents/qa-case-critic.md` and every quote is accurate (`:23`, `:30-33`, `:40`, `:41-46`, `:82-84`, `:87`). After A2, all five S2 checks are
at S4: four in the new register bullet and the `tried` reading at `:33`. Two gaps remain: the form (B-5a) and the scope line (B-5b). The
tester's `tried` should travel by the existing table (B-1). The four S3 checks are a reminder in the strategist's own charter. Items 1-3
(`qa-test-strategist.md:23-25`) already say three of them; the fourth is a craft line next to `:32` (which already names changed branches).
That is text only: no code gate, no refusal. One overclaim (F-8).

**K2 FACTS — answered (16 spot-checks).** I read each one on read-main.
- verified: stages.json S2 `roles` `:62-65`, `acceptance_by` `:66`, `advice` `:91-93`; S3 `roles` `:100-103`, `acceptance_by` `:104`.
- verified: `stage_S3` `:106-137`, critic branches `:115-117`, `:121-122`, `:130-131`. `s3_author_done` `:330-339`. `stage_acceptor` `:579-581`.
  `stage_S2` `:583-593`. Route functions `:595-747`. `ticket_rerun_critic` `:962-977`. `completion_for` S2/S3 `:1025-1043`.
- verified: `driver_machine.py:1290-1291` (`_wait_then_critic`), `:1322-1323`, `:1429-1433`, `:1496`.
- verified: `driver_dispatch.s3_ticket_completion(closes=True)` `:2635-2642`; `closes=False`'s only caller is `driver_stage_plan.py:1034`.
- verified: `controller.REPAIR_LOOP_ROLES` `:235-237`. `_s3_completion_gate` X2-5 branch `:7532-7537`. `author_exit_owes_plan` `acceptance.py:1515-1521`, its
  only caller `controller.py:7535-7536` (grep of the name over `scripts`, outside tests: two hits plus the definition).
- verified: `brief_pack.stage_critic_names` `:3565-3579`, `last_accepted_form` `:3625-3633`, `FIRST_LOOK_KIND` `:4001` with the `(S3, qa-case-critic)` row.
- verified: the readers of `advice-S2.json`/`advice-S3.json`. The only file reader is `stage_critic_names` (`:3574`); the only extra line is
  `driver_stage_plan.py:618`. `exit_gate.py:103`, `contract_slices.py:486` and `stage_joints.py:120,300` read the `advice` KEY, not the file.
  The grep `advice-` over `scripts/*.py` is its own positive control: it finds `brief_pack.py:83` (S5).
- verified: `CONSUMER_ROUTES` `driver_stage_s6.py:146-156`. `consumer_counts` `:323-331`. `consumer_exhausted` `:333-341`. `consumer_completion`
  `:343-369`. `consumer_settled` `:371-401`. `person_pass` `:262-302`.
- verified: the cap sites `controller.py:2197-2198`, `:5605`, `runtime_policy.py:94`, `stage_status.py:69`, `story_progress.py:357`, and `DEFAULT_LIMITS`
  `repair_cycles: 2` at `runtime_policy.py:13`. Partly wrong: B.1 counts four and lists five, and `story_progress.py:357` is S5-only (F-9).
- verified: the scout-only facts `handoff_init.py:152-154` (`EMPTIED`), `null-outcomes.json` NE34 `:133` / NE35 `:137` (the scope carriers of the two
  forms), and `handoffs/index.yaml:44-47`.
- verified: consumer brief sites `driver_stage_s7.py:134-137` and `driver_stage_s8s9.py:76-83`; scribe `:64`; `brief_pack.py:1819-1824`.
- wrong by omission: the A.1 fact "`driver_s0.py:531-541` ... S2 `complete=True` (no acceptor branch)" is true, but it misses the `roles[-1]`
  author choice (B-4a). A.1 also does not name `TRIED_READERS` (B-1).

**K3 COMPLETENESS — answered.** I grepped all ten S2/S3-only names plus `closes=False` and `stage_in_repair` over `scripts --include=*.py`
outside tests. Every hit is inside the functions A.4 deletes, or in their callers that A.4 also edits (`driver_machine.py:1291,1323,1496`,
`controller.py:7535`, `driver_stage_plan.py:1034`). Nothing is killed while a caller survives. Left alive with no caller after A+B: the S6/S7 branches
of `stage_review_exhausted` (F-3). The data side is short of `driver-layers.json:784` (F-1), and of the live tests and the `stage_guard` selftest (B-2).
The shared pieces survive intact: `stage_acceptor` (S4 `:752,805,817`), `stage_repair_owed`/`s4_repair_owed` `:557-575`,
`stage_acceptance_write` (S4 `:811`, S6 `:359,387`), `stage_verdict_known` (S4 `:809`, S6 `:357`), `stage_review_exhausted` (S4 `:807,810,820`),
`settle_role_questions` (S4 `:753`), and `stage_done.py --acceptance`. None is in A1's delete list, and A1's non-goals name the S4 bodies.
`reviewed_dispatch` (`brief_pack.py:3582-3597`) keeps S4 and the consumers by data.

**K4 PART B — answered.**
(i) Round spent, verdict unreadable, rounds uncountable: all take the gap road, with no seam and no person question (B2-3, E-B1/E-B5/E-B6).
The rework failing is NOT covered; it goes to the conductor (F-4). A gap-record write refused goes to `handle_refusal` (E-B7). That is a conductor
road, but only on a factory defect of the writer, and it is accepted as an FR-1 refusal. Name it as the one remaining door.
(ii) S6's gap reaches the report. S7's gap does not on three paths (B-3, a blocker). It is never read as a pass: the `gap:` prefix,
`consumer_close_words` "accepted with a gap", and E-B6's invariant.
(iii) B.3 is right for every return reason the two consumer charters name. I checked `qa-runner.md:21-25`, `qa-failure-analyst.md:16-28,63,76` and
`qa-doc-scribe.md:20-31,51`. The two gaps it finds are real (analyst item 5 has no "requirement"; `:76` has no "seen value"), and so are the two
narrowings. I found no return reason without a before-the-work carrier beyond those.
(iv) The S4/S5 caps are untouched: rows without the key give today's caps (E-B2, C3/C4 rows). The S5/S7 repair-limit road is untouched
(`driver_stage_s7.py:1035` is a non-goal of B1, and re-judge uses `reviewer_error`). Residual: the conductor's `seam_rework` of the S6 runner (F-10).

**K5 ARCHITECTURE AND PRINCIPLES — answered.**
- AR-1 kept (`acceptance_rounds`, `acceptance_reads`). Caveat: `TRIED_READERS` is closed variety in code, which B-1's larger option repairs.
- AR-13: kept for the cap. Broken by `author_form` (B-1) and by the two prefix homes (F-7).
- AR-14 kept: one writer, `stage_done --acceptance`; `--warn` is the same writer.
- AR-15 NOT kept as drafted: second roads for the form hand-over (B-1) and for the gap to the brief (B-3).
- AR-17 kept. AR-19: S2+S3 leave together and S6+S7 change through one table. Kept.
- AR-20: named, but incomplete (F-1, F-2).
- AR-21/22 incomplete: the S3 form loses its reader (B-1b).
- AR-23 kept: absent advice is named.
- AR-25 incomplete: B-4, F-14.
- AR-27 incomplete: B-3. AR-28 kept. AR-29 kept: no meaning read by code, with the text fix F-8.
- P22: the gap road is a move code takes without the conductor. That is legitimate only on the owner's word «не должно быть барьером». F1 is
  correctly marked as the owner's.
- P27 kept. P31: B-1, F-7, and B-4a (S1/S3 author filters as special cases, S2 none).
- FR-11/FR-38: B-5. FR-41: three distinct `why` texts, kept. FR-59: an unknown count gives no round plus a gap, the declared safe
  default, not a pass. Kept.
- F5 is a legitimate difference by data, not a P31 exclusion. The road is chosen by `acceptance.consumer_of(stage)` (`acceptance.py:1490-1494`:
  `acceptance_by` outside the stage's own roles), a data reading. The owner's words treat the two cases apart: «оставляем как раньше» for
  what stays, and «не должно быть барьером» said of consumer acceptance only. One correction to §1.3 axis 34: the selector is the consumer
  relation, not "`acceptance_rounds` present". Write it so.

**K6 TEMPORAL — answered.** Stuck or wrong states: B-4a (S2 completed under 0.11.0, then a ticket change, re-runs the critic and the start is
refused). B-4b (a critic's `ticket_changed` dispatch closes S2). T1 is unverified (F-14). T2's controller acceptance of a not-complete finish
by an undeclared role is unverified, and the spec admits it. Its fallback (`handle_refusal`, then the conductor's `release`) is a move, so
it is acceptable under F4 (a). Make it a test row, not prose. B.5 holds: round 2 under the old cap runs, and the next verdict is "2 of 1" and
becomes a gap. A story parked at the old seam keeps its answer roads.

**K7 NODES — answered.** A1: executable once B-2, B-4, B-6, F-1 and F-14 are in; direction chosen, edges named. A2: executable once B-5 and F-15 are in.
B1: executable once F-9, F-10 and F-11 are in. B2: executable once B-3, F-1, F-2, F-4, F-5 and F-6 are in. B3: executable; it crosses FV1-25 (F-13). D: executable once F-11
and F-13 (the SIBLING_MAP:122 overlap with FV1-6) are in. Owns are disjoint where marked parallel. The hot files `controller.py` (A1:
`REPAIR_LOOP_ROLES`/`_s3_completion_gate`; B1: `prepare`/`apply` cap lines), `brief_pack.py`, `acceptance.py` and `stages.json` are split by
function or row. `role-load.json`/`role-rules.json` for A2 and B3 differ by role row. `stage_guard.py` (B-2) and `driver_s0.py` (B-4a) are new A1 lines
and touch no other node. Ratchets: role-load named with direction; census named but mis-referenced (F-2); driver-layers incomplete (F-1).
No shrink-only ratchet is raised without being named.

**K8 TESTS — answered.** The nodes ask only for table rows in keep files: TESTING.md layers, one parameterised test per behaviour, no new
file. §O's quarantined files are right on wholly dead (`test_stage_critic_route.py`) and partly stale (`test_controller_stage_acceptance.py`,
`test_brief_pack_roles.py`, `test_acceptance_semantics.py`, `test_repair_route.py`; Part B: `test_stage_acceptance_consumer.py`,
`test_consumer_close_route.py`, `test_stage_review_person_pass.py`). It misses `test_handoff_init_author.py` and `test_rows_owed.py` (F-12).
Non-quarantined files that go red with no node: seven (B-2). For Part B, the one live hit, `test_story_run_refusals.py:3568`, only stubs
`stage_review_exhausted` for S4 and stays valid.

**K9 CROSSINGS — answered.**
- FV1-6: §X is right that its seam survives for S4 only, and its R1 row (`OpenWork("stage_in_repair")` at S2) dies. Missed: the shared
  `SIBLING_MAP.md:122` edit (F-13).
- FV1-22: right. N1 is a practical prerequisite of B2. N2's consumer part dies.
- TQ2-1: right for K1. Over-constrained for K2 (F-13).
- FV1-24: right (same files as B3).
- T1: right.
- Missed: FV1-12, on the same S2 row and card, with an owner's word that today's word supersedes (B-7); FV1-25 (analyst charter) and
  FV1-28 (`brief_pack.py`) (F-13).

**K10 FEASIBILITY AND COST — answered.** There is a simpler cut for Part A. Every S2/S3 code path already gates on `acceptance_by`:
- `stage_S2` falls to `stage_simple` at `:587-588`.
- `stage_S3`'s `critic = bool(self.stage_acceptor("S3"))` at `:115`.
- `author_exit_owes_plan` returns False at `:1521`.
- `stage_acceptance_refusal` returns early at `:1532`.
- `stage_critic_names` returns `[]` at `:3570`.
So the owner's behaviour ships with the data rows, the T2/T4 rules, `REPAIR_LOOP_ROLES`, the charters and the brief hand-over. The ~180 lines
of dead route can then be removed in a second node, A1b, on the same topic. That lowers the hot-file risk on the path to the live run.
Recommended: split A1 into A1a (data, temporal rules, B-2 tests, hand-over) and A1b (dead code, driver-layers rows). One critic pass covers
both (R13-g). For Part B there is no simpler cut that keeps AR-13 and FR-10. A cap read only on the driver side (`min(cap, 1)` in
`consumer_counts`) would avoid the controller edits, but the runner's packet would then still print `repair_budget.cap: 2` beside a brief
line saying "1 of 1". Two numbers in one packet break FR-10. B1's single reader is the right cut. B2-4/B2-5 shrink once B-3 moves the gap to `--warn`.

**DUPLICATION AND CONSISTENCY (brief item 6):** `TRIED_READERS`/`tried_reader_names` (`brief_pack.py:112,3636`) duplicated by `author_form` (B-1).
The `pipeline["warnings"]` writer `stage_done.py --warn` (`:1533`) and its brief reader (`brief_pack.py:1819`) duplicated by B2-5 (B-3).
`BY_PERSON` (`driver_core.py:411`) versus `GAP_PREFIX` (F-7). Grep shapes: `TRIED_READERS|tried_reader` over `scripts/*.py` (3 hits);
`"warnings"` writers over `scripts/*.py` (the `stage_done.py:190` writer); `BY_PERSON\s*=` (1 hit).

**CODE QUALITY (brief item 7):** plan stage, no new code yet. Dead branches remain after A+B (F-3). B2's `consumer_completion` grows by one
try/except plus three gap calls; ask the builder to keep it under ~60 lines by routing all three through `consumer_gap`.

**ONE ROAD (brief item 12):** B-1 (form hand-over), B-3 (gap to the report), and B-4a (the S2 author filter missing while S1/S3 have
special-case filters) are findings. F5 is not one; it is a data relation plus the owner's quoted word (K5). No language or project exclusion was
found. Grep: stage-name literals `"S2", "S3"` over `scripts/*.py` outside tests. The hits are `driver_s0.py:473`, `question_register.py:1477`,
`report_facts.py:73` and `branch_accounting.py:70`; all are task conditions, not exclusions from a shared mechanism.

---

## The owner's forks — is each recommendation the SAFE and REVERSIBLE side?

- **F1 (a), the gap road.** Reversible: one data key plus one function. Safe only once B-3 is fixed. Until then, one S7 sub-path can deliver
  a report that is silent about the gap, which P22 forbids ("пообещала и не сделала"). With B-3 fixed it is the safe side, because the worst case
  is a consumer working on less with the report saying so.
- **F3 (a), no road back from S4.** Safe and reversible: it adds nothing and uses existing roads (S4 case repair, `questions[]` to gate A).
- **F5 (a), S4 keeps the seam.** Safe and reversible: it is today's behaviour and the S4 non-goal.
- Lead forks: F2 (a) is acceptable (AR-22 kept, one brief line). F4 (a) is acceptable with B-4 and F-14. `recover` may make T1 cheaper than F4 states.

## Questions only the owner can answer (plain words, options)

1. «Один шанс переделать» — правильно ли я понял: если потребитель (аналитик на S7 или писатель отчёта на S8) вернул работу один раз и
   после переделки всё равно не может её использовать, фабрика идёт дальше без вопросов, а в отчёте появляется строка в «Дефектах
   фабрики»? Варианты: (а) да, так (рекомендация); (б) нет, на второй раз спросить дирижёра / человека.
2. Найденную на S4 дыру в реестре требований (S2) обратно тестеру не возвращаем: она идёт вопросом на гейт A или правкой кейсов.
   Варианты: (а) да, без возврата (рекомендация); (б) возвращать S2 на переделку, хотя это перезапуск S2, S3 и S4.
3. Исчерпанное ревью кейсов на S4 по-прежнему идёт к дирижёру/человеку, а приёмка S6/S7 больше нет. Варианты: (а) да, S4 как раньше
   (рекомендация); (б) S4 тоже без барьера — фабрика идёт дальше со строкой в отчёте.

---

## Trail

Read (whole or by range, on read-main 12317b6):
- the spec, whole;
- `agents/qa-case-critic.md` (whole), `agents/qa-test-strategist.md:19-33`, `agents/qa-requirements-tester.md:19-23`, `agents/qa-runner.md:14-26`,
  `agents/qa-failure-analyst.md:14-32,54,64,74-78,91`, `agents/qa-doc-scribe.md:20-35,48-53,60-66`;
- `references/stages.json:55-160` and all ten stage rows via a parse;
- `scripts/driver_stage_plan.py:80-140,326-360,520-760,785-836,886-895,918-1145`;
- `scripts/driver_stage_s6.py:140-430`, `scripts/driver_stage_s7.py:120-150`, `scripts/driver_stage_s8s9.py:16-41,60-100`;
- `scripts/acceptance.py:1450-1570`;
- `scripts/controller.py:230-240,2188-2200,3880-3940,5080-5115,5598-5612,7505-7560,8530-8580`;
- `scripts/runtime_policy.py:1-20,85-100`, `scripts/stage_status.py:64-72`, `scripts/story_progress.py:350-360`;
- `scripts/brief_pack.py:1810-1830,3560-3644,3995-4005`;
- `scripts/story_step.py:893-908`, `scripts/driver_machine.py:600-612,1286-1326`, `scripts/driver_dispatch.py:2633-2644`, `scripts/driver_s0.py:466-545`;
- `scripts/exit_gate.py:95-112`, `scripts/contract_slices.py:470-500`, `scripts/contract.py:5797-5802`, `scripts/check_delivery.py:1905-1935,2605-2630`;
- `scripts/stage_done.py:175-195`, `scripts/stage_guard.py:159-166,3075-3092`, `scripts/handoff_init.py:150-154`;
- `handoffs/s4-case-critic-to-designer.yaml:1-50,95-115`, `handoffs/index.yaml:44-47`;
- `scripts/tests/fixtures/driver-layers.json:525-538,677-688,784`;
- `scripts/tests/test_story_run_refusals.py:3545-3600`, `test_handoff.py:660-680`, `test_question_register.py:1920-1935`;
- `docs/SIBLING_MAP.md:120-123`, the FV1-6 spec headings and seam lines, `plans/piles/live-run-fvf/batch-1-live-run-fvf.md` node rows,
  `plans/piles/test-code-quality/batch-2-...md:25,32`;
- the FV1-12 finding on `wip/owner-words-1113b`, and `git diff --stat` of `wip/tq2-1-k1`, `-k2`, `-n5`.

Searches, each with its positive control (Grep tool content searches case-sensitive on code tokens; Bash grep):
- the S2/S3 route names over `scripts` outside tests (control: definitions found);
- `acceptance_by` and S2/S3 literals (control: `acceptance.py` hits);
- `advice-` readers (control: `brief_pack.py:83`);
- `TRIED_READERS|tried_reader` (control: definition `:112`);
- `stage_in_repair` over the package (control: `driver_stage_plan.py:677`);
- `"warnings"` writers (control: `stage_done.py:190`);
- `BY_PERSON\s*=` (1 hit);
- the removed tokens over `scripts/tests`, each file checked against the `test-layers.json` `quarantine` JSON (control: `test_stage_critic_route.py` reported QUAR);
- the Part B tokens over `scripts/tests` (control: `test_story_run_refusals.py:3568` found);
- `stage-critic-to` over the package (control: the two contract files found);
- `rework("S6"|rework("S7"` over `driver*.py` (control: `driver_stage_s7.py:1052` found).

No test was run: this is a plan gate with no diff and no mechanical layer to re-run.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1: acceptance_reads.author_form duplicates brief_pack.TRIED_READERS / tried_reader_names (brief_pack.py:112,3636-3644) - P31/AR-15/AR-13; hand the S2 tester form (and the S3 strategist form) through a TRIED_READERS row instead",
    "B-1b: the S3 strategist handoff form and its tried table lose their only reader after A1 (stage_critic_names brief_pack.py:3576-3578) - AR-22",
    "B-2: seven live checks go red with no owning node: stage_guard.py:3088-3089 selftest (run by test_stage_guard.py:2134), test_handoff.py:670, test_question_register.py:1928, test_story_run_first_look.py:44, test_first_look_briefs.py:28, test_first_look_wiring.py:126, test_brief_s3_roster.py:85",
    "B-3: the S7 gap is recorded at the scribe's finish (driver_stage_s8s9.py:80), after the scribe brief; on unreadable / form-refused / stale-count paths it never reaches the report or gate B - AR-27; use the existing writer stage_done.py --warn (:1533) instead of a second brief reader",
    "B-4: in-flight roads: driver_s0.py:525-541 ticket rework picks roles[-1] among accepted S2 dispatches, so it re-runs the critic (live bug on main; refused start after the change); the T2 rule placed after the ticket_changed branch lets an undeclared-role ticket_changed dispatch close S2, against its own invariant",
    "B-5: S4 case critic: its form s4-case-critic-to-designer.yaml:105 (advice_read single S4 file, inputs) is in no node's owns - FR-11/FR-38; its scope rule qa-case-critic.md:95 (design_review_required rows only, repair rounds changed rows only) conflicts with the whole-register check A.2.2 adds",
    "B-6: A1 acceptance keys live in test_story_run_s3_windows.py / test_story_run_freshness_k6_k7.py, slow files the non-goals forbid running locally - name the CI run as their witness",
    "B-7: FV1-12 (same stages.json S2 row and phases/s2.md; owner's word of 13.11 on the S2 acceptor, superseded today) missing from the crossings"
  ],
  "fixes": [
    "F-1: driver-layers.json:784 (_wait_then_critic) missing from A.4; B2 owns driver-layers rows for consumer_exhausted (:686) and the two new methods",
    "F-2: census line references C3 (a B1 test row); B2 owns judgment-census ratchet values",
    "F-3: after A+B stage_review_exhausted has only S4: dead stage_in_repair branch (:744) and the consumer_of branch (:702) - queue or remove",
    "F-4: E-B10 - the author's rework refused in consumer_settled goes to the gap road, not the conductor; row G9",
    "F-5: state the invariant that own() on the gap road is the stage's unchanged rule; row G3b",
    "F-6: consumer_gap on the unreadable path takes the author from stage_author_dispatch; empty author -> no record, one line, own()",
    "F-7: GAP_PREFIX and BY_PERSON (driver_core.py:411) in one home",
    "F-8: strategist reminder and AR-29 text must not claim the case critic judges the plan",
    "F-9: stage_status.round_cap has no stage parameter; story_progress.py:357 is S5-only; B.1 says four sites, lists five",
    "F-10: the conductor seam_rework (driver_machine.py:609) can spend a test_defect round of the S6 runner, capped at 1 by B2-1 - decide before dispatch",
    "F-11: B1/B2 owns placeholders and D relative owns - write absolute paths after scenario_walk --witness-for",
    "F-12: section O misses quarantined test_handoff_init_author.py and test_rows_owed.py",
    "F-13: crossings FV1-25 (analyst charter), FV1-28 (brief_pack), FV1-6 item 14 (SIBLING_MAP:122 same line as D); TQ2-1 K2 does not touch A2 files",
    "F-14: A1 lacks T1/T3 rows; T1 may be closed by controller recover (controller.py:8549-8560) rather than re-run - pin which",
    "F-15: A2 DoD grep is not deterministic - use a verbatim key-presence run with a negative control",
    "K10: split A1 into A1a (data, temporal rules, tests, hand-over) and A1b (dead code), one critic pass"
  ],
  "class_completeness": "Class 'stage critic route at S2/S3' walked by SIBLING_MAP axis 5 (S4 kept, S2+S3 together) and the in-artifact sweep of driver_stage_plan.py/driver_machine.py/controller.py/acceptance.py/brief_pack.py: callers complete except driver_s0.ticket_rework_step (B-4a), the stage_guard selftest and six live tests (B-2), driver-layers :784 (F-1). Class 'consumer review exhausted' walked over CONSUMER_ROUTES S6+S7 (one table): gap road covers round-spent/unreadable/uncountable; rework-refused (F-4) and the S7 report timing (B-3) uncovered. Class 'earlier author form handed to a later reader' has an existing survivor TRIED_READERS (B-1). Axis 34 (one road): B-1, B-3, B-4a findings; F5 legitimate by data plus owner's word. Axis 18: role-load named; census mis-referenced (F-2); driver-layers incomplete (F-1).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md (whole)",
      "read-main 12317b6 ai-packages/qa-factory/agents/qa-case-critic.md (whole)",
      "agents/qa-test-strategist.md:19-33, qa-requirements-tester.md:19-23, qa-runner.md:14-26, qa-failure-analyst.md:14-32,74-78, qa-doc-scribe.md:20-66",
      "references/stages.json:55-160 and all rows parsed",
      "scripts/driver_stage_plan.py:80-140,326-360,520-1145",
      "scripts/driver_stage_s6.py:140-430; driver_stage_s7.py:120-150; driver_stage_s8s9.py:16-100",
      "scripts/acceptance.py:1450-1570; controller.py:230-240,2188-2200,5080-5115,5598-5612,7505-7560,8530-8580",
      "scripts/runtime_policy.py:1-100; stage_status.py:64-72; story_progress.py:350-360",
      "scripts/brief_pack.py:112,1810-1830,3560-3644,3995-4005",
      "scripts/story_step.py:893-908; driver_machine.py:600-612,1286-1326; driver_dispatch.py:2633-2644; driver_s0.py:466-545",
      "scripts/exit_gate.py:95-112; contract_slices.py:470-500; contract.py:5797-5802; check_delivery.py:1905-1935,2605-2630; stage_done.py:175-195,1533",
      "scripts/stage_guard.py:159-166,3075-3092; handoff_init.py:150-154; handoffs/s4-case-critic-to-designer.yaml; handoffs/index.yaml:44-47",
      "scripts/tests/fixtures/driver-layers.json:525-538,677-688,784; tests/test-layers.json quarantine section",
      "tests/test_story_run_refusals.py:3545-3600; test_handoff.py:660-680; test_question_register.py:1920-1935; test_handoff_init_author.py hits",
      "docs/SIBLING_MAP.md:120-123; FV1-6 spec headings; plans/piles/live-run-fvf/batch-1-live-run-fvf.md rows; FV1-12 finding on wip/owner-words-1113b; git diff --stat wip/tq2-1-k1/k2/n5"
    ],
    "reruns": [
      {"command": "git -C read-main log -1 --oneline", "result": "12317b6 wave 2 integration report"},
      {"command": "grep removed S2/S3 tokens over scripts/tests + quarantine membership from test-layers.json", "result": "live unowned: test_brief_s3_roster.py, test_first_look_briefs.py, test_first_look_wiring.py, test_handoff.py, test_question_register.py, test_story_run_first_look.py; QUAR: test_stage_critic_route.py (control), test_handoff_init_author.py, test_rows_owed.py and the section-O files"},
      {"command": "grep stage_guard selftest case + test_stage_guard.py runner", "result": "stage_guard.py:3088-3089 expects [S2,S3,S4]; test_stage_guard.py:2134 runs --selftest; test_stage_guard.py not quarantined"}
    ]
  }
}
```
