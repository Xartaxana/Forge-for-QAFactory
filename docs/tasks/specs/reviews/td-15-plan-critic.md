# TD-15 plan critic (t-2281) — `docs/tasks/specs/td-15-scenarios-quarantine.md` (designer draft, commit f239ad282)

**Verdict: ACCEPT WITH FIXES — 7 blocking findings (B1–B7), 9 non-blocking (R1–R9).** The direction holds (a manifest instead of a move, a
watch outside the canon, deletion decided from data, judgment left to a role). But the keep list does not follow its own §B.2 criteria. It
quarantines the only detectors of exactly the defect classes the owner asked about. Two of the three precondition stories are compromised.
The watch's trigger and its "real catch" signal can stay silent for good. Every fix below is a spec edit and needs no new design. Whether
to accept is the Lead's call. This verdict is an input to that call, not the decision.

Tree reviewed: `wt-test-diet` at e5c085222 (branch `test-diet`). This includes TD-5.1 (1cd67fa78, merged AFTER the spec commit) and the
owner's fork decisions (982fdcd8e, `docs/tasks/test-diet.md` l.128–132: O-1 TWO releases, O-3 twice a week, O-4 the session line, O-5
no time cap).

## Blocking findings

**B1. The keep list breaks its own criteria 2 and 4 and switches off the only detectors of three named classes.**
§B.2 crit. 2 ("walks a registry of rules or sites whose loss would be silent") and crit. 4 ("a registry row and its reader;
one-reader/one-source censuses") are applied to ~12 hand-picked files, not to the 720. L-5 (spec l.243, 484) quarantines files that ARE
such walks, by their own heads:
- `test_state_exits.py:1-11`: "the states are ENUMERATED from `controller.projection([])`... both directions". This is the ONLY AR-25 detector
  besides `test_controller_state.py` (`design/architecture.md:256`). Both are quarantined, so AR-25 ("a state with no move") has **zero
  detectors**.
- `test_words_doors.py:1-10`: "ONE detector (here)". The sole AR-24 detector (`architecture.md:249`), so "a gate not understanding a
  person's words" loses its detector.
- `test_no_move_seam.py` (AR-17, `architecture.md:192`), `test_controller_blocks.py:1-8` ("a block with no row fails, a row with no
  block fails": a registry walk, 162 lines), `test_config_migration.py` (sole AR-3 detector, `architecture.md:65`).
- `test_role_commands.py`: "Every command in `references/role-commands.json`... against a deliberately broken file". A registry-row ↔
  reader walk (crit. 4). 800 lines, greedy rank 2.
- `test_state_portability.py`: the state census whose baseline `fixtures/env-facts-baseline.json` is a member of **SIBLING_MAP axis
  18** (`docs/SIBLING_MAP.md:387`). Crit. 1 names only `driver-layers.json` as "the owner file of an AR-20 ratchet". In-test shrink-only
  lists are also quarantined: `test_stage_cards.py:39` (NO_CARD), `test_onboarding_markers.py:36`, `test_profile_reader.py:565`,
  `test_silent_passes.py:1348`.
- SIBLING_MAP names 52 existing package test files as axis detectors, and **38 of them are in the would-be quarantine** (my count over
  §B.3 rows 1–81; command in the trail). The spec never treats SIBLING_MAP as a carrier.
- builder-rules 7b names `test_console_encoding.py` as a by-type-of-edit DoD witness (`plans/builder-rules.md:24`). Crit. 1 says "a
  builder-rules DoD line", but `gate_named_files()` (TD-15.1 (2)) hard-codes only 7c's `test_story_run_words.py`.
Is "mark those lines" enough (question 2)? Mechanically nothing breaks: `tools/architecture_gate.py`/`architecture_index.py` do not
open detector files (grep in the trail). That is the problem. Every later package commit writes `architecture: AR-25 -- kept` against
a detector that no longer runs, and the change checks of AR-9/17/24/25 ("Run both detectors", `architecture.md:111`) can no longer be
done. AR-20 is broken in substance: a quarantined ratchet neither shrinks nor refuses growth, so its debt can regrow unseen.
**Fix:** (a) add crit. 1b: "the file a carrier names as a Detector: `design/architecture.md`, `design/factory-rules.md`,
`docs/SIBLING_MAP.md` Detector rows, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, every builder-rules DoD line (7b and 7c), and every
owner of an axis-18 member". Compute it in `gate_named_files()` from those carriers by regex `test_[a-z0-9_]+\.py`. A forge-side carrier
is passed in by the forge tool, so the package does not read `docs/` (AR-4). (b) Before TD-15.2, add a scout node TD-15.0b: classify
all 720 heads against crit. 2/4 (pattern `registry|census|ENUMERATED|both directions|one reader|every row|shrink`, `-i`) and return a
list. The Lead decides. (c) Replace L-5's recommendation with: "keep every detector named by a carrier; quarantine only after a node
re-homes the detector into a data join (a keep row) and rewrites the carrier line in the same commit".

**B2. The precondition stories: one is legally compromised, one cannot walk what the spec says, and the capture scrub is too narrow.**
- `14857-s7` (`fixtures/investigation-14857/`) is the raw Jira corpus that the owner ordered replaced with synthetic data
  (`docs/tasks/specs/t-1855-github-move-nodes.md:485`, FK-13/F-18; `plans/piles/github-move/README.md` "в публичный пакет ушли бы сырые
  данные Jira с именами сотрудников"). On `main` it is (or will be) synthetic, which makes it NOT a story by §A.1's own rule. On this
  branch it must be replaced at the branch's move ("тем же инструментом... те же правила", t-1855:489).
- `12586-gateb` holds no `work/handoffs/` (listing in the trail; the handoff forms live at `work/handoffs/<dispatch>.yaml`,
  `scripts/handoff_init.py:99`). It also has no register, no cases and no gate A words (`state/words/` holds only
  `gate-b-decision.txt`). So the §A.2 example walk (`S3 handed`, `S5 handed`, gate A `decision` from `gate-a-decision.txt`) is
  unwalkable on it.
- `12586-redthen` (§A.1 table) is edited by hand ("Dropped... totals recomputed for the kept rows", `run-12586-red-then/README.txt`),
  and its `controller/` is cut at a different moment than its `work/`. That is a hybrid by §A.1's own definition.
- `tools/story_capture.py` scrubs machine paths and Cyrillic only (§A.1, TD-15.3). New stories from TP1 stand runs carry Jira people,
  logins, internal hosts and ticket text into a package that ships publicly. FK-11 (t-1855:484) demands person names removed everywhere.
So O-6 = 3 "two from existing fixtures + one fresh" rests on one usable story (12586-gateb, partially walkable).
**Fix:** (a) Drop `12586-redthen` and `14857-s7` as stories (keep them as variants/excerpts). Set O-6 = 3 FRESH captures, preferring
MyBooks runs (LOCAL-1, cart-1: the owner's own stand, no Jira people) plus 12586-gateb. (b) TD-15.3 capture refuses on a hit of the
migration scanner's rules (`docs/migration/scrub_rules.json` `person` and host rules) and names file:line, with the same door
`--drop`. (c) Make facets refusable per stage: a facet whose carrier is absent is `not_walked: <facet> -- <why>`, printed as a NOTE and
never green. Fix the §A.2 example to what the 12586-gateb cut actually holds.

**B3. The L-11 gate condition is a proxy that is already true and protects nothing. The rows it guards are stale.**
K4 cond. 5 (spec l.273) checks "`design/role-rules.json` exists". On the current tree it exists (TD-5.1, 1cd67fa78). The 12 pin files
of §B.3 rows 41–52 are **gone** (my disk check: all 12 missing). But the role-text pins INSIDE behaviour files (`test_gate_brief_and_retro`,
`test_question_branches`, ... spec l.245) move only in the TD-5.3 waves (`td-5-role-rules-register.md:255`, §4.6). So `enter` would
pass cond. 5 today and quarantine pins whose rules the register has not taken. That is exactly what the owner forbade («Пока реестр не
принял правило, его старый пин не удаляется», `docs/TESTING.md:90`). Also, TD-15.2 would write 12 keep rows that name no file, so
`FAIL tests: keep row names no file` turns the canon red.
**Fix:** delete rows 41–52 and the "absent today" claims (§B.3 l.208, §H l.506). Replace cond. 5 with a data join. `enter` refuses
while any would-be-quarantined file holds a role-text pin not yet in the register. The list is TD-5 §4.6's inventory, read as a data
file the TD-5.3 waves shrink (or keep those files as `register` until their wave, L-11 (b)). Name the carrier file.

**B4. The watch has no trigger it can count on, runs on the wrong host and branch, and can stay silent for good.**
- GitLab schedules are created by hand: `.gitlab-ci.yml:216-218` "once the owner creates a schedule... With neither, the job never runs".
  No in-repo carrier records that a schedule exists. `grep -i schedule` over `docs/RUNBOOK.md`, `CURRENT_CONTEXT.md` and
  `plans/builder-rules.md` gives 0 hits; the same grep finds 15 in `.gitlab-ci.yml`. The spec names nobody to create it and no check
  that it exists.
- The branch: a GitLab schedule targets one branch. The quarantine lives on `experiment/thinking-roles`/`test-diet` (upstream
  `origin/experiment/thinking-roles`), while `main` moved to GitHub on 05.11 (session root 84fe060aa; t-1855:489). `pull` "finds the
  newest schedule pipeline of the branch" (l.292) without saying which branch.
- The host: L-8 "port with the move" is stale (checklist p.5). The move is done for `main`: "short pipeline green on GitHub". The
  GitHub nightly has its trigger IN the file (`docs/migration/forge-repo/.github/workflows/nightly.yml:11-13`, `cron`), so no human step
  is needed there. It also caps minutes: "2000 Linux minutes a month" (nightly.yml:7). O-3's ~110 min per run × 2/week ≈ 950 min/month
  is half the budget. The spec states this cost for GitLab shared runners only (l.476).
- `pull` reads only `schedule` pipelines, but the RUNBOOK bullet (§D.4 (3)) orders a WEB button run after a release. Without
  `--pipeline` that run is never pulled, so R2 waits on the very run meant to satisfy it.
- Rules: "`schedule` and `web`/`api` with `QUARANTINE_WATCH == "1"`" (l.285) is ambiguous. A schedule carrying the variable also starts
  `package-full`, `install-smoke` and `crap-measure` (all `schedule` rules, `.gitlab-ci.yml:233,265,352`): 3–6 more runner hours per
  watch.
- "The watch itself stopped" is detected only as "watch age > 3 days → run pull" (l.321). That cannot tell "no schedule" from "nobody
  pulled". With O-3 twice a week, the 3-day threshold fires every cycle (noise). And `pull` on "no watch run yet" exits 0 silently
  (TD-15.6b). If nobody creates the schedule, the Lead sees "run pull" forever and the owner never learns.
**Fix:** (a) Fork L-8 is reopened for the Lead: put the watch where the quarantine's branch has its canon after the move, and prefer an
in-file `cron` (GitHub) with the minutes line stated to the owner. (b) On GitLab: `enter` refuses until a schedule for the quarantine's
branch with `QUARANTINE_WATCH=1` is visible via `GET /projects/:id/pipeline_schedules`. The door: "ask the owner to create it:
Settings → CI/CD → Schedules, cron twice a week, branch X, variable QUARANTINE_WATCH=1". (c) `pull` takes the newest `schedule` OR `web`
OR `api` pipeline with a `quarantine-watch-report` job on the named branch. (d) The other `schedule` jobs gain
`$QUARANTINE_WATCH != "1"`. (e) The stale threshold = 2 × cadence (8 days for twice a week). After 2 × cadence with no watch run on
CI (not merely not pulled: `pull` asks CI), the session line becomes an ALERT-class line: "TEST QUARANTINE ALERT: the watch has not run
since <date> -- tell the owner (schedule missing or failing)". `pull` exits non-zero on "no watch run in N days".

**B5. The coverage rules hide real catches, which is the very signal the owner asked to be told about.**
§D.2 l.299 says "`stale` covers every later streak of the same file (a file broken by a legitimate move cannot show a new catch)". That
is false for multi-check files: `test_controller_state.py` has 2423 lines, `test_words_doors.py` 1809. One check goes stale; a different
check of the same file later fails on a real regression, and that catch is masked for good. `flaky` coverage keys on `first_fail` only:
when check A (flaky) fails first and check B is a new real failure, `first_fail` is still A and B is masked. With TD-11 splitting
`story_run.py` during the quarantine, most driver-level files will go stale early. After one wave, the watch can no longer show a catch
on them, yet R3 counts them as judged. The owner would then get READY on a set that was blind.
**Fix:** record ALL FAIL lines of a red file (check names, capped at 50, 160 chars each) in the watch record. A verdict covers later
streaks only when their set of failing check names is a subset of the judged set. A new failing check name is a new streak, for every
verdict kind. `status` prints "blind: N files red since <date> with every check judged stale". The owner's sentence (B7/R-honesty)
names this.

**B6. K5 ("a quarantined file is never edited") can be bypassed. Its door is a pair detector scoped wrongly. The manifest itself is
unguarded.**
- On the batch canon (`api` pipelines) `CI_COMMIT_BEFORE_SHA` is zeros, so the base falls to `HEAD~1` (`.gitlab-ci.yml:102-106`, the
  shape §C.1 (8) copies). An edit to a quarantined file in any but the last commit of a branch is never seen.
- The door line is read from `$CI_COMMIT_MESSAGE` (the HEAD message, `install_parity.py:97`), while the diff spans `<ref>..HEAD` (rule
  15). A door in HEAD's message licenses an edit made in another commit. A merge commit ("Merge branch ...", no door) refuses a
  legitimate TD node that carried its door in its own commit. A merge from the other session's branch is therefore either refused
  wholesale or, on `api`, not seen at all.
- Nothing checks the `quarantine`/`keep` SECTIONS of `test-layers.json`. AR-20 (l.17) claims "rows leave only by purge", and §D.2 (4)
  claims "never returns to keep". But `check` diffs only file paths, and "a name in both sections is malformed" says nothing about
  history. A conflict resolution that drops quarantine rows makes those files unlisted (K1 red: visible). Moving them to `keep` is fully
  silent.
**Fix:** `check --base` walks `git rev-list <base>..HEAD` and judges each commit with its own message (`git log -1 --format=%B <c>`). On a
merge commit, judge the second-parent range by its own commits. The base for `api`/push pipelines is `origin/<target>`'s merge-base,
not `HEAD~1`. `check` also diffs `test-layers.json` at each commit: a removed quarantine row without `quarantine-purge:` is refused, an
added one without `quarantine-enter:`/`enter --add` is refused, and a keep row for a name in any earlier quarantine section is refused
(the history comes from `git log -p -- test-layers.json`).

**B7. `--witness-for` never names the gate's own test, and the owner gets no honest sentence about what goes dark.**
§A.6 matches keep rows by `covers`. TD-15.2 writes `covers` "for data_join/table rows" only (l.413). So a builder changing
`gate_preflight.py` is told to run the scenario layer and never `test_gate_preflight.py`, which is the gate-registry G13 test. And
§G/§E carry no statement of what regression classes go invisible on the day of the move. TD-12's greedy table shows the quarantine
taking `test_story_run_delivery_c.py` (30 570 lines alone, 19.4 % of all covered lines, `td-12-redundancy-8069240.md:85`),
`test_role_commands`, `test_gate_brief_and_retro`, `test_story_run_s7_live`, `test_story_run_s0` and `test_codex_host`, which are 6 of
the top 7.
**Fix:** (a) every keep row carries `covers` (gate_named and register too), computed by TD-15.2 from the file's imports. `--witness-for`
also prints every gate_named row whose import closure holds a changed module. (b) Add §G0 "What goes dark on the move", one paragraph
for the owner. It names: the driver loop (`story_run.py` outside S6/stand identity/words), S8 delivery, S0 reading and the ticket
adapter, the Codex host, onboarding/config migration, the artifact validator hook (`test_validators`), and every detector B1 does not
restore. It also gives a measured number: `tools/test_redundancy.py run --only <keep list>` on CI gives "the canon will cover X of
157 856 lines" before `enter` (the tool exists, `.gitlab-ci.yml:408` `--only`).

## Non-blocking findings

- **R1. The door call through `story_step.py finish` has side effects** (§A.3 l.99). `finish` records an accept on a world that already
  holds it, and later stages walk the SAME world. Call `exit_gate.all_errors(agent, task, digest, facts_text)` (`scripts/exit_gate.py:1763`)
  in-process instead. Name the gate-question builder function (the `question` facet names only modules). Name the
  `delivery_verdict.decide(kinds, doc)` inputs (`delivery_verdict.py:119`): where `kinds` come from. The `decision` facet re-records a
  decision already in the cut (gate B is event 148, INCLUDED): state "run on a copy of the world cut before that decision".
- **R2. Owner decisions not in the spec:** O-1 is now TWO releases. R2 (l.307) must count two distinct published versions >
  `release_at_entry`, with a complete run on the second. "Published" is not the version in `plugin.json`: the `release X` commit precedes
  the owner's publication. Read the release tag/CHANGELOG heading of the release repository, or say it is an approximation. O-3 is twice
  a week: the cadence goes into the rules, the cost and the stale threshold (B4).
- **R3. Watch shard balance:** `enter` strips quarantined rows from `slow_tests.json` (§C.1 (3)), and `shard_files` weights from that
  file (`selftest.py:617-620`). The watch's two shards then get every quarantined file at the default weight: the 200-s `story_run`
  files can land in one shard against the 3h timeout. Keep a `quarantine_seconds` map (written by `pull` from the watch's own seconds)
  and use it for `--quarantined --shard`.
- **R4. `ci-summary` completeness** (l.290) cites "a header count", but the `--watch-out` record (l.288) has no count field. Add
  `"expected": [names]` per shard. `ci-summary` must check the union against the quarantine section at that sha (read in the CI
  checkout). A `missing` file (deleted outside purge) is a red-class streak, not neutral, otherwise R3 passes over it.
- **R5. Duplicate `watch.jsonl` lines** from two sessions pulling the same pipeline on two branches are joined at merge. `status`
  dedupes by `pipeline`. Two identical verdict lines count as conflicting under R4. Say whether identical lines are one verdict, or keep
  the safe side and say so.
- **R6. Judging cost unbounded** (§D.2): up to ~640 Opus judgments, each reading a diff and a 1–3K-line test. Add a cap and a batching
  rule: one dispatch per commit range; first a single bulk pass over the list of `first_fail`/check names; open only the files that pass
  that pass. State an estimate to the owner with O-3.
- **R7. Interim safeguard:** before `enter`, compute `red_at_entry` and a flaky baseline from the last 3 `package-full` runs, not from
  one pipeline (K4 cond. 3). A file red or alternating there enters with `red_at_entry: true` or `flaky_at_entry: true`. This is cheap:
  the runs already exist.
- **R8. §F order and owns:** TD-15.1 is listed "parallel with 15.6a", yet 15.6a depends on 15.1 (l.386 vs l.391). TD-15.2 and 5 × TD-15.5.k
  all own `test-layers.json`: sorted adjacent JSON rows conflict textually, so D-0048's functions-disjoint form does not apply to JSON.
  Have the Lead add the five rows at merge, or have 15.5 nodes hand the row back in the report. TD-15.6b/6c share `build_parser`/`main`:
  15.6a writes all subcommand stubs. New files (`test-layers.json`, `scenario_walk.py`, `fixtures/stories/**`, `tools/test_quarantine.py`,
  `tools/story_capture.py`, `plans/test-quarantine/*`) need `plans/features.json` globs. `forge_metrics --check` blocks MR pipelines
  (`.gitlab-ci.yml:85-90`), yet no node owns `features.json`. TD-15.6b must also own the staged GitHub workflow copies
  (`docs/migration/forge-repo/.github/workflows/nightly.yml`), or state why not. TD-15.2 is blocked on "the Lead's resolution of `?`
  rows": give the default (`?` → keep) so the node runs by the recommendation.
- **R9. Test volume against the new rule:** TD-15.3 orders "the 2 MB cap AT (exactly 2 MB passes) and BEYOND (+1 byte refused)" (l.418).
  That is an internal boundary, which §E's own CLAUDE.md text says "gets no test". Drop it, or name why the capture tool is a table
  module. `test_scenario_walk.py` and `test_story_capture.py` are new files: give each its keep row and layer in the node (7d new text).
  Fine otherwise: the 15.6a/15.1 tables test the canon runner and a gate (table layer, crit. 5).

## Answers

**1. The scenario layer.** The oracle is honest in design: expected values are extracted from the run record (`expected` by extraction,
amendments with `ref` and `accepted_by`, §A.2 l.84-86; edge l.464 "never edits the story's artifacts"). Two caveats. "The Lead acts for
the owner" (l.63) is P20's "person accepted" only by delegation, and the owner never sees amendments; recommend a line in the session or
report when an amendment flips an outcome. Story paths: `fixtures/run-12586-gate-b/TP1-12586` exists (148 events,
`state/words/gate-b-decision.txt`, `work/{automation-manifest,ledger,source-inventory,test-plan}.json`, 2 snapshots, NO
`work/handoffs`). `fixtures/run-12586-red-then/{controller/TP1-12586,work,test-code}` exists, but it is a hybrid (B2).
`fixtures/investigation-14857/TP1-14857` exists (103 events, `work/handoffs` present), but it falls under FK-13 (B2). The excerpt
folders exist (listing). Would it catch the classes? (a) A stage losing a field at a handoff: only when the loss is in CODE that the walk
runs (`story_step start` → brief path presence, `handoff_init`). The `handed` facet checks presence and parse, not that every field is
whole. Losses in code-written artifacts between stages (snapshot, ledger, run-report reducers) are invisible, because the walk starts
from their RECORDED output (the S0 snapshot losing AC, PROJECT.md p.5, is exactly this shape). (b) A gate not understanding words:
yes, for the recorded words and for `words` variants. New phrasings only as rows. (c) A state with no move: structurally NO. A walk
covers only states the run reached and left. The detectors of this class are AR-25/AR-17 censuses, which L-5 quarantines (B1).
Structurally it also cannot catch: hosts other than the one recorded (Codex), onboarding, install, S0 reading, every rare branch no
recorded run took, timing/concurrency (the stand lease). Is three enough? Not as the SOLE precondition for ~640 files. It is enough
only together with B1's restored censuses and B7's honest sentence. With 14857 out, three means three fresh captures (B2).

**2. The keep list.** Sampled keep rows, judged against the file head:
`test_story_run_words` (words via file: gate_named, ok); `test_window_record` (G10, ok); `test_check_delivery` (G11, ok);
`test_probe_by_code_languages` (ok); `test_branch_accounting` (ok; most repaired, L-4); `test_grounding_table` (ok); `test_handoff`
(contract = schema: data_join, ok); `test_open_list_fields` (data_join plus an AR-20 tuple, ok); `test_contract_slices` (generator rules
on a synthetic plugin: table/tool, not data_join, minor); `test_s0_key_form` (`Driver.s0_key_form`, a person-question flow: NOT "table:
key forms", keep but wrong layer); `test_task_root_parsers` (34 CLIs' argparse safety: table, ok); `test_story_version` (26 lines, one
trivial reader: the "small function" test the owner named, so quarantine); `test_cost_capture_tail` (money, ok); `test_stage_guard`
(guard safety, ok); `test_external_writes` (safety, ok); `test_driver_golden` (a dev measurer, "not a real-run layer" by the spec's own
trail, l.504: weak, so quarantine); `test_event_store` (ok); `test_task_price` (ok); `test_one_source_per_fact` (FR-10 packet
consistency, not AR-13 as written: fix the reason); `test_conductor_investigates_first` ("reads the text VERBATIM", `:1-6`: a
role-text pin by TESTING.md l.74, so it belongs in the role-rules register, not `register` as a kept test); `test_resolver` (ok);
`test_gate_b_orders` (scenario, ok). Sampled quarantined files (top of TD-12 greedy plus carrier-named): `test_story_run_delivery_c`
(30 570 adds), `test_role_commands` (registry walk, B1), `test_gate_brief_and_retro` (L-11), `test_story_run_s7_live`,
`test_story_run_s0` (AR-6 K5), `test_codex_host` (AR-5), `test_probe_by_code`, `test_install_retire`, `test_words_doors` (sole AR-24),
`test_validators` (AR-26; the C0 rules of the artifact validator hook), `test_ticket_adapter` (S0 reading, P5), `test_state_exits` (sole
AR-25), `test_controller_state` (AR-25), `test_controller_blocks` (AR-9 walk), `test_no_move_seam` (AR-17), `test_config_migration` (sole
AR-3), `test_state_portability` (axis 18), `test_stage_cards`/`test_onboarding_markers`/`test_profile_reader`/`test_silent_passes`
(in-test shrink-only lists), `test_console_encoding` (builder-rules 7b DoD line). The ones that are the only detector of a gate or
invariant: see B1. Gate-registry and stage-joints: all 22+3 `test` files are in the keep list (my extraction matches §H). The two
names inside `source_freshness.exempt_reason` prose are not read by `gate_registry.py:669` (field `test` only), so §E's prose edit is
enough there. L-5: no, see B1.

**3. Mechanics.** `selftest.py`: filtering before sharding (§C.1 (1)) is consistent with `cmd_tests` (`selftest.py:609-630`: the files
are globbed, then `shard_files`, then the `fast` filter). `--contracts`/`--hooks` name kept files by K3. The shard header count changes
consistently. `slow_tests.json`/`package-full-report`: consistent after `enter` (the rows are dropped in the same commit, so drift is
0). The watch loses its weights (R3). Lint/dup ratchets: as stated (dup scope `scripts/*.py`; no `scripts/tests` row in the lint
baseline, per the designer's controlled count). `driver-layers.json` L8: quarantined files stay on disk, so the rows stay true
(`test_driver_layers.py:568-613` reads the literal in test files). Purge removes the rows. `plans/features.json`: 405 literal test
globs over 24 features, and no feature becomes empty on purge (my count). New files lack globs (R8). `install_smoke.py:467-469` names
only `test_reinstall_equals_fresh.py` (kept). The release fingerprint covers the package tree: quarantine files still ship in the
release, which is not a defect but should go in the owner's sentence (640 dead files ship until the purge). One reversible commit: yes
for `enter` (manifest plus slow_tests plus the flag). The §E carrier edits are separate Lead commits, so a revert of `enter` leaves the
carriers saying "quarantined" (say: revert both). Guard: K5 can be bypassed (B6). A builder's rename is a "rename" in the diff, refused
only if the commit is inspected (B6). TD-15.8 imports: my AST walk of the 69 existing keep files finds **31 kept → quarantined import
edges**. Examples: `test_story_run_s6 → test_fixes_13797, test_controller_state, test_controller_rework_scope`; `test_proof_level →
test_probe_binding, test_run_freshness`; `test_detector_verdict → test_words_doors`; `test_gate_b_orders → test_controller_state`;
`test_local_keys → test_external_writes_bug_refusals`. TD-15.8 "copy into `<area>_common.py`" duplicates helpers that
`test_controller_state` exports widely. With B1's restorations, several targets (`test_controller_state`, `test_words_doors`) become
kept and the edge disappears. Re-derive after B1.

**4. Watch and notification.** Is the condition checkable from data alone? Yes as written (R1–R6 over committed jsonl plus HEAD). Can it
say READY wrongly? Through B5 (stale/flaky masking: yes), through R4 (a `missing` file counted neutral: yes), and through a `web`
release run never pulled (it blocks READY: safe side). Timeout/ran-nothing runs are incomplete and never satisfy R2: correct. Reds
never judged: R3 blocks, correct. A release published before the manifest existed: `release_at_entry` comes from `plugin.json`, which
the `release X` commit bumps BEFORE publication, so an unpublished bump counts (R2). The two-sessions-judge edge: handled for verdicts;
watch duplicates are not handled (R5). Channels, and whether the trigger exists today: (1) SessionStart:
`tools/session_context.py` exists, `build_context_lines` at :2117, `last_calibration_line` called at :2184, `MAX_LINES = 25` at :175.
OPEN DISPATCH is capped at 4 (:58-60), so ≤ 15 lines come before it and the "never cut" claim holds. It reads local files only:
offline OK. Trigger: exists (`.claude/settings.json` SessionStart → `python tools/session_context.py`). But it shows only what `pull`
committed. (2) The scheduled CI job: the trigger does NOT exist in the repository. A GitLab schedule is created by hand by the owner
(`.gitlab-ci.yml:217-218`), no carrier says one exists (0 hits, controlled), the branch is unnamed, and the host is moving (B4). If
nobody creates it, the job never runs, and the only symptom is "run pull" plus `pull`'s silent "no watch run yet": silent for good
toward the owner. (3) The release checklist RUNBOOK §4: exists as a section, the bullet is to be written, and it fires only at a
release (human trigger). Detector for "the watch stopped": only the watch age (it cannot tell stopped from not pulled), plus a proposed
calibration check (§E, PROCESS) that does not exist yet (B4 fix e). Judging duty: assigned (critic-tier role via the Lead, recorded by
`judge`, accepted by the Lead). Cost unbounded (R6).

**5. Risk not stated.** On the day of the move these go dark: the driver loop outside S6/stand identity/words; S8 delivery (the
`delivery_c` family); S0 ticket reading and the adapter; the Codex host and resume isolation; onboarding and config migration; the
artifact validator hook's C0 rules; and the 38 SIBLING_MAP detectors plus the AR-3/17/24/25 detectors (B1). The spec gives the owner no
sentence about this (B7). Cheap interim safeguards: (a) the coverage number of the keep set via `test_redundancy.py --only` (B7);
(b) red/flaky baselines from the last 3 nightly runs (R7). The "watch for a week before the move" idea is already served: before
`enter`, the full canon runs every file, so its last N runs ARE that baseline, and no new job is needed. (c) Keep B1's censuses.

**6. Buildability.** Places a Sonnet builder would have to guess: TD-15.4, how to invoke the doors without side effects, which
function builds a gate question, what `decide` takes (R1), and what to do with a facet that has no carrier (B2c). TD-15.2: the `?` rows
and L-5 are unresolved (R8), and `covers` is missing on gate rows (B7). TD-15.5.k: concurrent edits of one JSON file (R8), and
scrubbing persons (B2b). TD-15.6a–c: shared parser stubs (R8). TD-15.6b: which branch and host, and whether the schedule exists (B4).
TD-15.8: owns are not absolute, and the list is unknown until `enter --dry-run` runs (acceptable if the node is dispatched after 15.6a
with the list pasted as owns). Missing from all nodes: `plans/features.json` (R8). Order: the 15.1 ∥ 15.6a contradiction (R8). Test
volume: the TD-15.3 AT/BEYOND cap contradicts the new rule (R9). The rest is table-layer and consistent.

**7. Rule carriers missed by §E** (grep pattern `мини-батаре|mini-battery|тест узла|каждое ребро|test FILE that judges|AT and
BEYOND|SCOPE CEILING`, `-i`, plus `файл области|тестовый файл изменённого`). Positive control: the same grep finds `docs/TESTING.md:56`
«мини-батареи».
- `CLAUDE.md:60-62` **host adaptation 11** ("a node's run covers the test FILE that judges each owned path") is untouched by §E and
  contradicts `--witness-for`.
- `CLAUDE.md:211` policy rule 4 ("must cover the test FILE that judges each owned path") is not in the §E override list (only rule
  11's sentences are). Add it to the host-adaptation-12 override.
- `docs/TESTING.md:115` «Билдер: ... свидетель — прогон файла области» and `:117` «Критик, вопрос 5: ловит ли тест узла» are in
  «Кто что делает», which §E does not edit.
- `docs/tasks/critic-diff-brief.md:11` (the two layers: "the changed module's test file plus the DoD keys") is missed; §E edits only q.5.
- `plans/builder-rules.md:24` (`test_console_encoding.py` by type of edit) also needs a decision (B1).
No hits in `PROJECT.md`, `.claude/agents/*.md` or `docs/RUNBOOK.md` for these patterns. The §E rows for builder.md rule 4 and designer.md
rule 1 rest on the 7b pointer, which is correct.

## Owner forks (the owner decided at 23:30; risk of each option to the owner)
- O-1 (decided: two releases): longer exposure, and with B5 unfixed the extra release adds blind time, not safety. (a) one release is
  cheaper but bets on one run. (d) restart-on-catch is the safest and can run forever.
- O-2 (decided: record, land, continue): fine once the ALERT reaches her. The risk lies in B5 masking, not in the clock choice.
- O-3 (decided: twice a week): wider commit ranges make judging dearer and coarser. On GitHub Free it is ~950 of 2000 min/month.
  Weekly halves the cost and doubles the range.
- O-4 (decided: session line): silent when no forge session runs or nobody pulls. Adding `CURRENT_CONTEXT.md` costs nothing and is
  visible on any machine.
- O-5 (decided: no cap): with slow release cadence, 640 dead files ship in every release and the watch keeps billing. A 60-day cap
  trades that for deleting on R3–R6 without release evidence.

## Trail
Read: the spec (whole); `docs/TESTING.md` (whole); `docs/tasks/test-diet.md` l.60-139 plus commit 982fdcd8e; `td-12-redundancy-8069240.md`
l.81-140; `selftest.py` l.589-658, 785-890 plus a grep of defs and flags; `.gitlab-ci.yml` l.47-117, 174-311 plus a grep of jobs and
rules; fixture listings of `run-12586-gate-b`, `run-12586-red-then`, `investigation-14857` and their READMEs; event-type counts of the 3
roots (a read-only python count); `handoff_init.py` grep; `architecture.md` Detector lines (grep) and l.110-135, 225-260;
`gate-registry.json`/`stage-joints.json` test-name extraction; `gate_registry.py:669` and the `test_gate_registry.py` grep;
`driver-layers.json` test names plus `test_driver_layers.py` L8 grep; `plans/features.json` literal-glob count; `tools/session_context.py`
l.48-63, 2117-2203; `.claude/settings.json` SessionStart; `tools/ci_read.py` and `install_parity.py` defs; `docs/SIBLING_MAP.md` axis 18
(l.383-432); `plans/builder-rules.md` l.14-24 plus a grep of test names; `CLAUDE.md` l.58-66 plus grep; `critic-diff-brief.md` grep;
`docs/migration/forge-repo/.github/workflows/nightly.yml` l.1-40; `plans/piles/github-move/README.md` l.1-25; `t-1855-github-move-nodes.md`
l.480-490; `td-5-role-rules-register.md` grep; docstrings of 22 keep and 29 quarantined test files; `design/` listing.
Searches and their positive controls: `grep -i schedule` over RUNBOOK/CURRENT_CONTEXT/builder-rules gave 0 (control: same grep, 15 in
`.gitlab-ci.yml`). The rule-carrier grep gave hits (control: `TESTING.md:56`). `find -name handoffs` over the fixtures: none under
`run-12586-gate-b` (control: same find gives `investigation-14857/.../work/handoffs`, `run-12586-red-then/controller/.../work/handoffs`).
`grep -lis ratchet|shrink` over tests gives 23 files (positive within). `architecture_gate.py` opening detector files: no `test_*.py`
read (control: the same grep finds `index.is_file()` at :410). 12 pin files absent (`os.path.isfile`, control: 69 other keep files found
by the same call). TD-5.1 not an ancestor of the spec commit (`git merge-base --is-ancestor` exit 1). The 31 import edges and the
"SIBLING_MAP 52 named / 38 quarantined" count come from read-only python AST/regex runs over the keep set of §B.3 rows 1–81.
Not done: no test runs (non-goal); GitLab schedule existence cannot be read offline, so that is stated as "no carrier", not "absent".

```json
{"verdict": "fit_with_fixes",
 "blockers": [
  "B1 keep list ignores its own criteria 2/4: quarantines sole detectors of AR-24 (test_words_doors), AR-25 (test_state_exits, test_controller_state), AR-17, AR-3, axis-18 baseline owner test_state_portability, in-test shrink-only lists, 38 of 52 SIBLING_MAP detectors",
  "B2 precondition stories: 14857 is the Jira corpus the owner ordered replaced (FK-13), 12586-gateb has no work/handoffs nor gate A words, red-then is a hybrid; capture scrubs no person names (FK-11)",
  "B3 K4 cond.5 (role-rules.json exists) is already true after TD-5.1 while behaviour-file pins wait for TD-5.3; rows 41-52 name deleted files",
  "B4 watch trigger: GitLab schedule made by hand with no carrier, branch unnamed, host moved to GitHub (in-file cron, 2000 min cap), pull ignores the web release run, other schedule jobs ride along, stale threshold cannot tell stopped from not pulled",
  "B5 stale covers every later streak of the file and flaky keys on first_fail only: real catches masked, READY on a blind set",
  "B6 K5 bypass: api pipelines check HEAD~1 only, door read from HEAD message across a range, merges, no guard on test-layers.json sections",
  "B7 witness-for skips gate_named rows (no covers); no owner sentence or coverage number on what goes dark at the move"],
 "class_completeness": "Carrier class 'a file named as a detector': spec walks gate-registry, stage-joints, CONTRACT_TESTS, install_smoke, CI, driver-layers, builder-rules 7c; misses architecture.md detectors (L-5), SIBLING_MAP detector rows (38 of 52), axis 18 members beyond driver-layers, builder-rules 7b, PROCESS calibration (test_story_step). Rule-carrier class: misses CLAUDE.md host adaptation 11, policy rule 4 sentence, TESTING.md Kto-chto-delaet, critic-diff-brief two-layers line 11.",
 "trail": {"read": [
   "docs/tasks/specs/td-15-scenarios-quarantine.md", "docs/TESTING.md", "docs/tasks/test-diet.md", "docs/tasks/specs/reports/td-12-redundancy-8069240.md",
   "ai-packages/qa-factory/scripts/selftest.py", ".gitlab-ci.yml", "ai-packages/qa-factory/references/gate-registry.json", "ai-packages/qa-factory/references/stage-joints.json",
   "ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json", "ai-packages/qa-factory/design/architecture.md", "docs/SIBLING_MAP.md", "tools/session_context.py",
   "plans/builder-rules.md", "CLAUDE.md", "docs/tasks/critic-diff-brief.md", "docs/migration/forge-repo/.github/workflows/nightly.yml", "docs/tasks/specs/t-1855-github-move-nodes.md",
   "ai-packages/qa-factory/scripts/tests/fixtures/run-12586-gate-b/README.txt", "ai-packages/qa-factory/scripts/tests/fixtures/run-12586-red-then/README.txt"],
  "reruns": [
   {"command": "python AST walk of 81 keep rows for imports of non-kept test_ modules", "result": "12 keep files absent on disk (TD-5.1); 31 kept->quarantined import edges"},
   {"command": "regex count of test_*.py named in docs/SIBLING_MAP.md vs keep set", "result": "52 named existing, 38 would be quarantined"},
   {"command": "grep -i schedule docs/RUNBOOK.md CURRENT_CONTEXT.md plans/builder-rules.md (control .gitlab-ci.yml)", "result": "0 hits; control 15"},
   {"command": "event type count over the three story roots", "result": "gate-b 148 events 3 decisions, one words file; no work/handoffs in gate-b"}]},
 "fixes": [
  "B1: criterion 1b (every carrier-named detector and axis-18 owner, computed in gate_named_files), scout node TD-15.0b to classify all heads by criteria 2/4, L-5 recommendation to keep detectors until re-homed",
  "B2: drop 14857 and red-then as stories, three fresh captures preferring MyBooks runs, capture refuses on scrub_rules person/host hits, facet-level not_walked, fix the A.2 example",
  "B3: delete rows 41-52 and stale absent claims, replace cond.5 with a join against TD-5 4.6 inventory as a data file",
  "B4: reopen L-8, schedule existence checked by enter via pipeline_schedules API with an owner door, pull reads schedule/web/api on a named branch, other schedule jobs exclude QUARANTINE_WATCH, threshold 2x cadence and an ALERT line to tell the owner, pull non-zero on no run",
  "B5: record all failing check names; a verdict covers only subsets of its judged set; status prints blind files",
  "B6: per-commit judging over rev-list with each commit's own message, merge-base base, diff of test-layers.json sections with purge/enter doors and a no-return check from history",
  "B7: covers on every keep row and gate rows in witness-for; a section G0 for the owner with a measured keep-set coverage number",
  "R1-R9 as listed in the report"]}
```
