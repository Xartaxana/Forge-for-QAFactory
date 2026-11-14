# Critic review t-717 — topic A "stage critics S2/S3 removed" (A1a, A1b, A2, A3), one pass

Spec: `docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md` (read whole). Diffs: A1a `a9d69a5..85dba1a`, A1b `85dba1a..08b2b1c`,
A2 `a9d69a5..91ab1f3`, A3 `85dba1a..c8a1ec2`. Recon t-682 (`docs/tasks/specs/recon/20261114-s3-window1-closing-role-recon.md`) read and
spot-checked. No code edited.

## Verdict per node

| node | verdict | why, in one line |
|---|---|---|
| A1a | fit_with_fixes | fits the spec and its edges; the data change makes S3 window 1 a "closing role" at 7 sites (only `stage_repairs` fixed) — must reach `main` together with A1c (B2) |
| A1b | fit_with_fixes | every deleted producer's live reader is gone or re-pointed; pins move exactly with the deleted rows; leftovers are text/test hygiene (N1-N4) |
| A2 | unfit (one line) | the register-remainder Tools line orders the case critic to run `exploratory_findings.py add`; the role has no shell (B1). The rest of A2 fits |
| A3 | unfit as designed | the card and rows build a producer road nobody can walk at S4 (B1); the epilog, census rows and X1/X2 are sound as code |

Topic verdict: **blocker** (B1 is a spec defect of F7 (a): `failure_class: spec`, returned to the Lead as a fork; not a builder error).

## Blocking findings

**B1 — the S4 case critic cannot produce the register remainder (FR-11, FR-56, AR-22, P15).** `agents/qa-case-critic.md:4`
`tools: Read, Grep, Glob, Write, Edit` (no Bash). The brief tells the role exactly that: `brief_pack.TOOLING_NO_SHELL["qa-case-critic"]`
= "your findings file is read by code at the exit gate (the roll-call); you run nothing" (`brief_pack.py:385-387`) under `NO_SHELL_HEAD`
"The scripts of the plugin are run for you by the orchestrator" (`:370-373`); on Codex `host_adapter.role_policy` refuses the call
(`brief_pack.py:129-130`). A2 adds (`qa-case-critic.md:96` on sc-a2): "...is recorded once ... with `exploratory_findings.py add --task-root
<T> --by ...`". Scenario: S4 critic finds a sentence no requirement holds -> charter says run the command -> no tool (Claude) / refused
(Codex) -> the remainder never reaches the report; the brief and the charter contradict each other. A3's card row naming `qa-case-critic`
(`role-commands.json` +9) advertises the same unrunnable command; X1 (`by="S4-qa-case-critic-1"`) pins a road no S4 actor takes. Spec
§A.2.4/A3 edge 1 checked only "a permission carrier", not the role's tool set; the A3 builder measured "the card permits nothing" and
missed the same fact. Minimal fix (Lead fork, F7 re-decided; recommended **(c')**, the existing O4 pattern — "the designer has no Bash, so
... it writes ... and code raises", `contract.py:1547`, `critic_rollcall --apply-fixes`): the critic writes rows in a NEW optional form
section (e.g. `register_gaps[]`: `refs`, `statement`, `missing_prerequisite`; empty outcome declared, AR-23) of
`s4-case-critic-to-designer.yaml`; the driver, in the S4 critic finish next to `stage_acceptance_write` (`driver_stage_plan.py` S4 path),
calls `exploratory_findings.py add --kind coverage_gap --by <critic dispatch> --evidence <its findings file>` per row (one writer kept,
AR-14; reader `report_facts` exploratory block unchanged). Then: A2's line says "write it in `register_gaps`"; A3's card drops
`qa-case-critic` (runner/analyst keep it: both have Bash); X1 keeps its writer half, a new driver row pins form -> register. Alternative
(b): `questions[]` only (loses answered gaps from the report — owner's F3 word «остальное доходит до отчёта» would then hold only
partly; owner question). Giving the critic Bash is not recommended (P14/FR-56).

**B2 — merge condition: A1a must not reach `main` without A1c.** After A1a S3's last role is the strategist, so
`contract.stage_closes_with("S3", strategist)` is True for window 1 at every role-only site. Traced: `story_step._halt_doors`
(`story_step.py:1904`) offers `decide --close` on a window-1 halt; `finish` then sets `complete = True` from the recorded `close`
(`story_step.py:2494-2504`, overriding `--not-complete --unresolved plan_pending`), and `_s3_completion_gate` (`controller.py:7528`)
refuses "a window-1 dispatch cannot close the stage" — a door into a refusal and a stuck finish until `decide --open` (FR-2, FR-57).
`controller.py:5849-5858` gives window 1 `--not-complete` without `unresolved` a false text + a refused door. The normal live road is safe
(`s3_window_completion` returns `OpenWork("plan_pending")`, `driver_stage_plan.py:485-488`, so `finish` sends `--unresolved`). Fix: A1c
(list in Q8) merged in the same wave as A1a/A1b, before any stand run off `main`.

## Non-blocking findings (fix in A1c unless said otherwise)

- N1 (A1a, AR-13) — T2 rule reads the purpose with `stage_guard._record_purpose` (`driver_stage_plan.py:904-907`), a PRIVATE helper whose
  top-of-record fallback (`stage_guard.py:243-247`) differs from `story_step._purpose_of` (binding only, `story_step.py:382-385`) and
  `controller.s3_window_of` ("never the top of the record"). No wrong output found (an undeclared role must still match the row's role),
  but three purpose readers now; and the model dict is rebuilt as in `story_step._optional_row` (`:118-122`). Fix: one public purpose reader.
- N2 (A1a, item 7) — copy inside `stage_critic_names`: the outputs filter (`brief_pack.py:3664` and `:3680`) and the advice name (`:3665`,
  `:3683`). Fix: one local `_parts(row, stage, parts)` used for own stage `("outputs","advice")` and each earlier stage.
- N3 (A1a/A1b tests, item 5) — `test_story_run_s3_windows.py:183,208,1008` assign `driver.stage_critic_route = lambda ...` and assert the
  list stays empty: vacuous after A1b (nothing can call it). `hasattr(...) is False` checks (`:142`, `test_first_look_step.py:634`) pin
  the absence of code (TESTING «не пишется»); the latter is spec-prescribed. Fix: drop the stubs and absence pins.
- N4 (A1b, item 7) — `test_null_outcomes.py` label "homes: one declared, 20 never_empty" now checks `(1, 18, 52)`: the label lies.
- N5 (A1b, sweep-the-artifact) — `stage_done.py:1537` `--acceptance` help "(S2-S4)" in the same file as the fixed `:975`/`:1551`;
  `acceptance.py:1273` (A1b file). Both role-visible or carrier text; see Q6.
- N6 (A1b witness, critic rule 7) — DoD key `python tools/test_quarantine.py check` NOT witnessed (rc=127, then >10 min). "The commit
  hook accepted it" is not that check: `test_quarantine.py check` runs only in `nightly.yml:240`, not in `.githooks`. Consistency check
  done: the `quarantine-edit: test_stage_critic_route.py -- ...` line is in 34fabea's message verbatim per §A.4.1. Owed: the nightly
  `quarantine-check` result after merge (coordinator).
- N7 (A3, proposed node) — GUARDED row `("open", "append raises the first ValueError only")` is a named residual: `exploratory_findings.append`
  refuses one problem at a time (FR-1 sibling). Needs a node with an owner, not a line.

## Answers

**1) Fit per node.** A1a: W1/SC-1..3/W5/T2/T4/S-R8..10 green on CI 43529128188 (report); T1, T1-b, J1, J2 present; `roles[-1]` gone from
`driver_s0.py`; T2 positioned after the S1 rules, before `ticket_changed`; `acceptance_reads` edges (absent / unknown part / unknown stage
/ non-list / non-mapping) print one line, no crash (J2 rows). Fix-round edit of `stage_repairs` (outside A1a owns, Lead round t-654) is
correct: `s3_window_of(last) != "labelling"`; the builder's Q (absent purpose -> closes) is right: the exit window is registered with no
purpose (`driver_stage_plan.py:128`), so "absent -> not closing" would never close S3. A1b: matches A.4 row by row; A1b Q1 (bare `return`)
is exactly A.3 "returns at once"; W2 present. A2: all keys present (re-read the lines), form rows `required: false`, `advice_read` one
string; fails only on B1. A3: on F7 (a) as written, fails B1.

**2) Readers of A1b's deleted producers (AR-22, FR-13).** Grep over the package at 08b2b1c (names of every deleted method, both contract
names, NE34/NE35; positive control: hits in quarantined files and comments). Live code readers: none. Left: comments
`exit_gate.py:820`, `driver_stage_s6.py:344`; vacuous test stubs (N3); quarantined readers `test_controller_stage_acceptance.py:279-284`
(AttributeError), `test_handoff_init_author.py` (10 lines), `test_rows_owed.py:46,112` — allowed by §O, the Lead tells the owner (watch
red). `stage_acceptance_verdicts: ok` keeps a producer (S7/S8 consumer forms). Pin move 08b2b1c is a legitimate consequence, no hidden
lost row: `scope 19->17` and K0.4/K0.12 `-2` = the two index rows of kind review; `never_empty 20->18` and K0.6 list minus NE34/NE35 = the
two deleted rows; `handoff index 23->21` = the same two index rows. Ratchets (AR-20): shrunk — driver-layers rows, NO pins, index count;
raised and named — `ROLE_BRIEF_BYTES_MAX qa-case-critic 6130->6580` (A1a fix, Lead), `role-load` six rows (A2 report table); census
`ratchet` untouched (builder's local 25/25; slow, CI owed).

**3) S3 window 1 as a closed stage.** No site CLOSES S3 on window 1: `_s3_completion_gate` (a) refuses any window-1 claim of completeness,
and `stage_repairs` now excludes it. But `_s3_completion_gate` is not enough by code: it is the last word, not the predicate, so the sites
that ASK "is this the closing role" answer yes for window 1 — `controller._closes_stage` (`:7566`; it already exempts S5 plan and S7
investigation, so the S3 labelling exemption belongs there), its callers `:5098` and `:5851`, and `story_step.py:1904, 2494, 2812, 2943`
(B2). `_is_review_of` `:4080`: not applicable to the strategist.

**4) Judgment.** No judgment moved into code: the register checks are craft text in the S4 charter; the strategist's four checks are its
own reminder; A3 adds a card and two census rows (shape/told), no refusal on content. No code check left without an owner: the removed
`stage_critic_completion` was a seam carrier, the S4 one stays. States the removed critic returned: accept -> now the author's own close;
reject with a round (`stage_in_repair`) -> T3 road; reject on last round / unreadable -> no seam needed (no acceptor); critic `questions[]`
-> S2/S3 authors' own open questions + S4 critic `questions[]` (still raised by `stage_acceptance_write`); in-flight T1-T4 handled (A1a
rows). Old `pipeline.acceptance.S2|S3` records: readers gate on `consumer_of`/`acceptance_by` (`controller.py:3929`, `acceptance.py`),
inert. Exception: B1 — the new S4 state "a remainder exists" has no move the role can take (AR-25).

**5) Duplication and quality.** DUPLICATION: N1 (purpose reader, model build), N2 (filter copy); grepped `startswith("project:")` over
`brief_pack.py`, `_purpose_of|_record_purpose|s3_window_of` over scripts. CODE QUALITY: N2, N3, N4; no new function over 60 lines
(`stage_critic_names` ~30, T2 rule 8 lines); no dead branch in product code after A1b (`stage_repair_owed` keeps its S4 caller).

**6) Stale text.** In this topic, to A1c: `acceptance.py:1273`, `stage_done.py:1537` (help), `handoffs/vocabulary.yaml:121` ("S2-S4" ->
"S4, S6, S7"; merge after wave 8, which edits the same file), `handoff.py:406`, `handoff_init.py:435` (help), `story_step.py:365`,
`brief_pack.py:3693` (`reviewed_dispatch` docstring "(S2-S4)"), `exit_gate.py:820`, `test_first_look_wiring.py:99` label, N3, N4, the
"S7 skeleton Reviewed dispatch" comment (not located by my grep of `Reviewed dispatch` over scripts/references — A1c locates it).
To topic B (B2 owns `consumer_completion`): `driver_stage_s6.py:344`. To node D (spec): `skills/qa-story/phases/s2.md:117`, `s3.md:60`,
`controller-blocks.md`, AR-29 `:138`. Not stale: `exit_gate.py:646` (advice files S2-S4 exist), halt texts "S2-S4" (`driver_dialog.py:121`,
`driver_dispatch.py:1833`), `question_register.ROLE_QUESTION_STAGES`.

**7) Merge.** `git merge-tree --write-tree` (exit 0, no conflict lines) for every pair: main a3f9a49 x {85dba1a, 08b2b1c, 91ab1f3, c8a1ec2};
wave8 ae41e2b x {08b2b1c, 91ab1f3, c8a1ec2}; 08b2b1c x c8a1ec2; 08b2b1c x 91ab1f3; c8a1ec2 x 91ab1f3. Shared files with wave 8:
`driver_stage_plan.py` (wave 8 edits `stage_acceptance_write`, `stage_verdict_known`; A1b deletes neighbours), `stage_done.py`, `acceptance.py`,
`handoff_init.py`, `driver_machine.py`, `driver_dispatch.py`, `driver-layers.json`, `test-layers.json`, `test_field_producers.py`,
`test_handoff.py`, `role-load.json` (A2: three roles; wave 8: other rows — slack-0 process rows are per role, disjoint). Grep of the
merged tree wave8+A1b (d49b37…) for every deleted name: no live reader; wave 8's additions name no S2/S3 critic. Canon risks after merge
(not run here; slow): `test_role_commands.py` (A3's package-full not read), `test_driver_layers.py` (A1b rows + wave 8 rows; also red on
main L8 before), `test_brief_pack.py` 6580 and `test_no_move_seam_c26_g27_f2.py` (A1a fix values never re-run on CI at 85dba1a),
`test_story_run_s3_windows.py` W2, `test_judgment_census.py`; pre-existing reds: `test_forge_metrics` k1, `test_selftest_slow_tests`.
Quarantine-watch will turn the four quarantined readers red (§O). Order: wave 8 -> A1a+A1b (as one chain, with A1c) -> A3 (after the B1
re-decision) -> A2 (re-cut line; re-measure `role-load.json` after wave 8). A2 and A3 must land together (FR-39).

**8) A1c must contain.**
1. One predicate "this dispatch can close its stage" = `stage_closes_with` and not an S3 labelling window (`s3_window_of`), in
   `controller._closes_stage` beside the S5-plan / S7-investigation exemptions; wired at `controller.py:5098`, `:5851`, `stage_repairs`
   (replace the inline A1a test), `story_step.py:1904, 2494, 2812, 2943` (through `C.` the same reader). Rows: window-1 halt offers no
   `--close`; `decide --close` on window 1 is refused with its door; `--not-complete` without `unresolved` on window 1 gets the true text.
2. N1 (one public purpose reader, used by T2 and story_step) and N2.
3. Stale text of Q6 (topic-A part) incl. N5.
4. Tests: N3, N4.
5. Not in A1c: B1's re-cut (A2/A3 after the Lead's F7 decision); N7 as its own node; `driver_stage_s6.py:344` to B2.

## Proposed nodes (for the Lead to open)
- F7 re-cut (B1): form section + driver writer + A2 line + A3 card roles; owner question only if (b) is chosen.
- N7: `exploratory_findings.append` reports every problem of a line (FR-1), owner: package pile.
- Quarantine notice (§O): four readers go red at the next watch; door `test_quarantine.py judge ... --verdict stale`.

## Spot-checks (claims verified)
- Builder A1b "pins follow the deleted rows": verified by diff arithmetic (above) and re-run.
- A3 "the card permits nothing": confirmed — and that is the B1 problem (no other carrier gives the critic a shell; frontmatter read).
- Recon t-682 site list: `_closes_stage` `:7566-7600`, `story_step.py:1904`, `:2484-2504` read on the carrier; matches.
- Negative "no live reader of deleted names": `git grep -i -E` over `ai-packages kb plans/piles tools`; positive control: hits in the
  quarantined files and comments listed.

## Trail
Read: the spec whole; `critic-diff-brief.md`; recon t-682; reports sc-a1a (+fix), sc-a1b, sc-a2, sc-a3; diffs of all four nodes; wave 8
diff of `driver_stage_plan.py`, `stage_done.py`; `controller.py:85-100, 5080-5105, 5835-5870, 7510-7600`; `stage_guard.py:219-255`;
`story_step.py:360-370, 382-386, 1895-1912, 2470-2530`; `driver_stage_plan.py:60-135, 470-500, 880-925`; `brief_pack.py:94-130, 368-395,
3661-3700`; `exit_gate.py`/`driver_stage_s6.py` grep hits; `vocabulary.yaml:20-28, 118-126`; agents frontmatter `tools:` (12 files);
`role-commands.json:185-210`; `test_validator_class.py` diff; `.githooks` + workflows grep for `test_quarantine`.
Commands: `python -B test_null_outcomes.py` (sc-a1b tests dir) -> `=== test_null_outcomes: 327/327 ok ===`; `python -B test_handoff.py` ->
`=== test_handoff: 596/596 ok ===`; `git merge-tree --write-tree` x10 -> clean (rc 0); `git grep` of deleted names on 08b2b1c and on the
merged tree d49b37120889.

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 (A2+A3, spec F7 (a)): qa-case-critic has no shell (agents/qa-case-critic.md:4; brief says 'you run nothing', brief_pack.py:385-387) yet A2 charter line and A3 card make it run exploratory_findings.py add: the register remainder can never reach the report (FR-11, FR-56, AR-22). Lead re-decides F7; recommended: form section register_gaps[] written by the critic, the driver calls exploratory_findings.py add at the S4 critic finish (O4 pattern).",
    "B2 (A1a merge condition): S3 window 1 now reads as the closing role at controller._closes_stage callers and story_step.py:1904/2494/2812/2943 (decide --close door refused by _s3_completion_gate, finish stuck until decide --open); A1a must reach main only together with A1c."
  ],
  "fixes": [
    "A1c: one predicate in controller._closes_stage (stage_closes_with and not s3_window_of == labelling), wired at controller.py:5098, :5851, stage_repairs, story_step.py:1904, 2494, 2812, 2943, with rows",
    "A1c: one public purpose reader for the T2 rule and story_step (N1); local helper for the copied outputs/advice lines in stage_critic_names (N2)",
    "A1c: stale text acceptance.py:1273, stage_done.py:1537, vocabulary.yaml:121, handoff.py:406, handoff_init.py:435, story_step.py:365, brief_pack.py:3693, exit_gate.py:820, test_first_look_wiring.py:99; driver_stage_s6.py:344 to B2",
    "A1c: drop vacuous stage_critic_route stubs in test_story_run_s3_windows.py:183,208,1008 and absence pins; fix the test_null_outcomes label '20 never_empty'",
    "Coordinator: attach nightly quarantine-check result after merge (A1b DoD key not witnessed); read CI for test_role_commands, test_driver_layers, test_brief_pack 6580, test_no_move_seam C26 at the merged heads",
    "Proposed node N7: exploratory_findings.append reports every problem of a line (the open GUARDED row)"
  ],
  "class_completeness": "Class 'role-only closing predicate meets a two-window stage': A1a fixed one site (stage_repairs) of eight; the rest named and queued to A1c with file:line (axis 25 state exits, axis 5 twins S5-plan/S7-investigation already exempt in _closes_stage). Class 'charter names a command the role cannot run' (axis 30/31): B1, one instance; runner/analyst rows of the same card checked (both have Bash). Dead-route readers (AR-22): all live readers gone; quarantined readers named for the owner notice.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-stage-critics-s2-s3-removed-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/recon/20261114-s3-window1-closing-role-recon.md",
      ".claude/worktrees/sc-a1a/docs/tasks/specs/reports/20261114-sc-a1a-report.md and -fix-report.md",
      ".claude/worktrees/sc-a1b/docs/tasks/specs/reports/20261114-sc-a1b-report.md",
      ".claude/worktrees/sc-a2/docs/tasks/specs/reports/20261114-sc-a2-report.md",
      ".claude/worktrees/sc-a3/docs/tasks/specs/reports/20261114-sc-a3-report.md",
      "diffs a9d69a5..85dba1a, 85dba1a..08b2b1c, a9d69a5..91ab1f3, 85dba1a..c8a1ec2, a3f9a49..ae41e2b (driver_stage_plan, stage_done)",
      "controller.py 85-100, 5080-5105, 5835-5870, 7510-7600; story_step.py 360-386, 1895-1912, 2470-2530; stage_guard.py 219-255",
      "driver_stage_plan.py 60-135, 470-500, 880-925; brief_pack.py 94-130, 368-395, 3661-3700; agents/*.md tools lines; role-commands.json 185-210"
    ],
    "reruns": [
      {"command": "python -B test_null_outcomes.py (sc-a1b at 08b2b1c, tests dir)", "result": "=== test_null_outcomes: 327/327 ok ==="},
      {"command": "python -B test_handoff.py (sc-a1b at 08b2b1c, tests dir)", "result": "=== test_handoff: 596/596 ok ==="},
      {"command": "git merge-tree --write-tree for 10 branch pairs incl. ae41e2b x 08b2b1c", "result": "all clean, rc 0, tree d49b37120889 for wave8+A1b"}
    ]
  }
}
```
