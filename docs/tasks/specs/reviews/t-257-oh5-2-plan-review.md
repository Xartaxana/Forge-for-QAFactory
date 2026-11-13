# t-257 — critic on PLAN: OH5-2 spec t-254 (`docs/tasks/specs/t-254-oh5-2-plugin-root-given.md`)

Reviewer: critic (Opus), 13.11.2026. Base: `refs/remotes/origin/main` = `1fe6fde` (2026-11-13 02:59 +0100), extracted
whole with `git archive` into a scratch folder; every fact below comes from that extract, not from the stale local checkout.

**Verdict: NEEDS WORK (fit_with_fixes): 3 blocking findings (B1-B3) and 6 non-blocking ones (N1-N6).** Every finding comes
with the exact spec edit. Most of the plan holds: the facts are right, the survivor design is sound, Parts A/B/C don't share
files with each other, and F2/F3/F4/F6/F8 are correct. The blockers are a ratchet Part B will turn red without owning its
file, a batch-freeze breach in F1, and F5's root half resting on an unmeasured property while ignoring an existing survivor.
Whether to accept is decided by the coordinator, or by the full Lead for F7 (rule 6).

## Key 1 — facts by trail (checked against origin/main)

| Claim in spec | origin/main | Status |
|---|---|---|
| Guard sites :771, :823, :875, :1086, :1107, :1231, :1273, :1275, :1286, :1299, :1616 (11) | the same 11 lines, `grep -ni claude_plugin_root scripts/guard_pre_tool.py` | exact |
| `runtime_paths.package_root()` :229, `Path(__file__).resolve().parent.parent` | :229, same body | exact |
| `hooklib.PLUGIN_ROOT` :30 `parents[1]`, same value | :30 | exact |
| `brief_pack.SCRIPTS = HERE.as_posix()` :72; card head :3675, :4260 | :72, :3675, :4260 | exact |
| TOOLING lines: runner `manual_evidence.py prepare|validate|write-block`, analyst `bug_snapshot`/`bug_records`, scribe `report_facts`, retro `retro_numbers`; TOOLING_MANUAL build/rejudge | present (:263, :279-280, :287, :301; TOOLING_MANUAL :332-) | exact |
| refusal_registry `SCANNED` :56 (3 files), `findings()` | :56, `findings` :888 | exact |
| `launch_card.desktop_story` :165-176, false for any non-empty `QA_FACTORY_RUN_MODE` | def :165, the check at :169 | exact |
| run_headless :65 `env = dict(os.environ, CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS="0")` | :65 | exact |
| `test_charters_s5_s9.py:223` key `'python "${CLAUDE_PLUGIN_ROOT}/scripts/manual_evidence.py" validate'` | :223 | exact |
| K9 `test_brief_pack_roles.py` :286-303, :300 expects `[["bug_records.py","bug_snapshot.py"], True]` | yes; traced: after Part B `charter_scripts` returns `[]` -> K9 red as predicted | exact |
| `test_package_generation.py` P4 :489, P5 :492/:494 | P4 :489-490, P5 :492-495 | exact |
| census: 417 hits in 84 files | `grep -rio` over origin: **420** in 84 files (local: 419); the extra hit is `skills/qa-onboarding/phases/p4-generate.md` (conductor-read, OH5-2e). The role-read classes (5 charter, 10 slice, 11 guard, 8 code, 5 data) are unchanged | holds for every class a Part touches |
| `judgment-census.json` runtime_paths rows :710-712 | :712-714 (drift); still no `refusal_registry.py` row | immaterial |
| quarantine: `test_brief_pack_roles.py`, `test_package_generation.py` quarantined; `test_ahead_cards.py`, `test_charters_s5_s9.py`, `test_refusal_registry.py` keep | confirmed in `test-layers.json` | exact |
| node row OH5-2 and B-142 / B-166 | origin batch-5 :31; both findings files exist; the B-166 text "не экспортирует ни `CLAUDE_PLUGIN_ROOT`, ни `QA_FACTORY_RUN_MODE`" confirmed | exact |
| Part B: "`role_rules.WITH_BASH`" exists | **does not exist**: `WITH_BASH` lives only in `scripts/tests/role_replay.py:49` (imported as `RR` by `test_brief_pack_roles`); `role_rules.py` has no such name. `host_adapter.role_has_bash` :519 exists | **wrong**: N2 |

## Blocking findings

### B1 — Part B turns the keep test `test_role_load.py` red (process ratchet, slack 0) and does not own `references/role-load.json`

Evidence. Four parts of the code fit together:
- `role_load.process_ratchet_problems` (`role_load.py:259-282`) says a role whose process load is **below** its row is a
  problem: "below its row X: lower to Y (... the slack is 0)".
- `test_role_load.py:541-546` (a keep file) runs it against the shipped package and expects `[]`; audit A22 runs it too
  (`audit_factory.py:1310-1316`).
- The `## Tools` sections Part B edits sit under `<!-- kind: process -->` (qa-runner :56; the same structure in the other three).
- The legend line edit shrinks every regenerated `common-rules.md` slice, and that slice is part of each role's delivered load.

Failure scenario: the builder applies §3.2 as written. All four charters and the ten slices get shorter, so each affected
role's `process_tokens` drops below `process_ratchet_tokens[role]` (for example qa-runner 14432, qa-retro-analyst 13206).
`test_role_load` K10-b then fails with "below its row: lower to N", and so does A22. The witness doesn't show it:
`scenario_walk --witness-for` over Part B's paths (run on origin, below) never prints `test_role_load.py`. So Part B ships
"green" and the BATCH CANON goes red. Spec §1 row AR-20 ("role-load bytes only shrink") gets the ratchet wrong: here a
shrink is also a required edit.
Also: `references/role-load.json` is touched by in-flight `origin/conv/wave-3` and `origin/wip/hf84-p11` (the qa-automator row).

Spec edit (Part B):
- `owns:` add `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/role-load.json`.
- DoD add (5): "`process_ratchet_tokens` rows of every role whose measured process load fell (expected: the 4 charter roles
  plus every role whose `common-rules.md` slice changed) are lowered to the value `python -B <pkg>/scripts/role_load.py --all
  --json` prints; no row is raised; `ratchet_tokens` untouched unless the test demands it".
- Verification run: add `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_role_load.py`.
- `edges:` add E23 "a shrink below a slack-0 ratchet: the row is lowered in the same commit (AR-20)".
- §1 AR-20 row: replace "expected: none" with "process ratchet rows lowered (slack 0); no raise".
- §4: name the overlap "role-load.json: conv/wave-3, hf84-p11 (qa-automator row); Part B merges after them or resolves
  that one row's conflict itself".

### B2 — F1(a) opens OH5-2d / OH5-2e as rows of batch-5, which is taken and therefore frozen

Evidence: origin batch-5 header: `статус: в работе | взял: dev1 (Opus coord), 12.11.2026`. PROJECT.md «Командная работа» п.2
says a taken batch changes only its progress, statuses and `очередь:` lines; anything new on the topic goes into a
`findings/` file plus a row in an **untaken** batch of the pile (D-0044) and a row in the card's «Содержание». Batch-6 of
`onboarding-hooks` is `статус: ожидает` (origin, header line 3), so it is the legal carrier. Failure: rows written into
batch-5 get refused by `piles.py check` (в) at commit-msg. That leaves the residual without a carrier, which is exactly
the condition rule 19 forbids.

Spec edit: in §6 F1 and in the coordinator-decision paragraph, replace "opened as named nodes of this batch now (rows in
batch-5 + residual table §4)" with "each opened as a `findings/` file of onboarding-hooks, a node row in
`batch-6-ostatki-t-203-i-t-227.md` (status ожидает) and a «Содержание» row in the pile README, in the same move as Part A's
acceptance (D-0044)". In §4 "Residual nodes", replace "of this batch" with "batch-6".

### B3 — F5's root half: it sets `CLAUDE_PLUGIN_ROOT` from an unmeasured premise, and Part C writes a second road for the env of a `claude -p` child

There are two defects in one fork.

(a) Unmeasured premise and a broken baseline. The node direction says run_headless gives "what the host would give". For
the run mode, the spec emulates the DESKTOP host (removes the variable). For the root, it emulates the DRIVER (sets it),
and §6 F5 admits this hides the very class OH5-2e has to measure. Whether a desktop host puts `CLAUDE_PLUGIN_ROOT` into the
conductor's Bash is the open question of OH5-2e (CLAUDE.md hygiene 6a: measure first). I measured the current baseline. A
forge desktop session (the place run_headless is launched from) has, in its Bash, `CLAUDE_PLUGIN_ROOT=[]` and
`QA_FACTORY_RUN_MODE=[]` (`echo` run below). So every past headless baseline ran with an empty root. Setting it would change
the conditions of comparison runs against those baselines, and it is not what the host is known to give.

(b) Duplicate of an existing survivor (P31 / AR-15). The package already has the one road for "the env of a `claude -p`
child": `infra_failure.child_env(base, rules, driver_cfg)` (`infra_failure.py:133`, data `references/driver-infra.json`
`child_env`), used by `driver_core.py:500-501`. It strips `CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH`,
`CLAUDE_CODE_CHILD_SESSION`, `CLAUDE_CODE_MESSAGING_*` and others, the vars behind "Not logged in" on TP1-13877. My
measurement of this forge session's env shows exactly those names present. So run_headless launched from it hands them to
its child today. A new hand-written `run_headless.child_env` that leaves them in is a second, weaker road for the same
action. The spec's `siblings:` line names only `driver_core.py:501`.

Spec edit (§3.3, Part C, §5 E16, §6 F5):
- `child_env(base, plugin)` becomes:
  `env = infra_failure.child_env(base, infra_failure.rules()[0], {})[0]`, then `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS="0"`,
  then `QA_FACTORY_RUN_MODE` removed and `CLAUDE_PLUGIN_ROOT` **removed**. That is the desktop road the run mode already
  assumes, and no stale copy can reach the child, so B-014/R6b are covered. Import it through `paths.PACKAGE / "scripts"`
  as the other measurers reach package code, or report the import door if none exists.
- F5 recommendation text: "(d) remove both variables and strip what `infra_failure.child_env` strips; set
  `CLAUDE_PLUGIN_ROOT` only after OH5-2e has measured that the desktop host gives it (then OH5-2e changes run_headless)".
  Report the deviation from B-166's wording ("не экспортирует CLAUDE_PLUGIN_ROOT") in §8 alongside the run-mode deviation.
  F5 is a fork the coordinator decided by recommendation; this change goes back to the coordinator, or to the Lead tier,
  for the decision.
- E16 row: base `{"QA_FACTORY_RUN_MODE": "driver", "CLAUDE_PLUGIN_ROOT": "/other/copy", "CLAUDE_CODE_CHILD_SESSION": "1",
  "X": "1"}` -> none of the first three, `X` kept, ceiling `"0"`, `base` unchanged. E17 (spaces in the plugin path) then
  covers `--plugin-dir` only, not the env.
- Part C `given:` add `ai-packages/qa-factory/scripts/infra_failure.py` (:133-170) and `references/driver-infra.json`
  (read only). `siblings:` add `infra_failure.child_env`, the survivor.
- If the coordinator keeps "set the root", (b) still stands: compose on `infra_failure.child_env`, and write the
  measured-baseline change into §8 as a known break of comparability.

## Non-blocking findings

### N1 — Part A puts the survivor's case table in the wrong test file; `test_runtime_paths.py` is the module's table

`test-layers.json` keep: `test_runtime_paths.py` has `layer: table, why: "table (B.2 criterion 5): runtime paths"` and covers
`runtime_paths.py`. `test_refusal_registry.py` is `layer: register`: "registry matches the shipped sources". TESTING.md
layer 3 allows one table per module, on the Lead's list. Rows E1-E8 of a `runtime_paths` function inside the registry test
would form a second table for that module, in a file whose layer doesn't fit, which is the "mini-battery on an internal
function" TESTING.md forbids. Spec edit (Part A): DoD (1): "one table **in `test_runtime_paths.py`**". `owns:` add
`.../scripts/tests/test_runtime_paths.py`, keeping `test_refusal_registry.py` for DoD (3)-(4). §4 overlap: in-flight
`origin/wip/of4-17b` edits `test_runtime_paths.py` (2 lines, fix round 2): merge after it.

### N2 — Part B's DoD names a reader that does not exist

DoD (3) says "through the existing reader `role_rules.WITH_BASH` / `host_adapter.role_has_bash`". `role_rules.WITH_BASH` is
not defined anywhere in `scripts/` (Grep over origin; positive control: the same Grep finds `WITH_BASH` in
`scripts/tests/role_replay.py:49`). A weaker model will either invent it or regex the role file. Spec edit: "through
`role_replay.WITH_BASH` (`scripts/tests/role_replay.py:49`, the test helper K9 already uses) or
`host_adapter.role_has_bash(role)` (`host_adapter.py:519`)".

### N3 — the legend replacement puts "the paths on your brief" in the installed-plugin frame, but a brief names project paths too

`common-rules.md:112` (origin) is the row `| ${CLAUDE_PLUGIN_ROOT}, ${CLAUDE_SKILL_DIR}, references/…, scripts/… | the
**installed plugin**, never the project |`. §3.2 rewrites the first cell to "`references/…`, `scripts/…`, the paths on your
brief". But a brief also carries `<task root>`, `project:` doors and `work/...` files. So a role reading the table literally
resolves a project path against the plugin, which is the exact confusion this table exists to prevent. Spec edit (§3.2 and
Part B DoD (2)): first cell becomes "`references/…`, `scripts/…`, the script paths of your brief card (`python
\"<path>/scripts/<script>\"`)".

### N4 — the survivor's quoting differs from the card for E3 roots; P31 "one spelling" holds only for ordinary roots

The card head is hand-built `python "{SCRIPTS}/<script>"` (`brief_pack.py:3675`, `:4260`), always double-quoted. The guard
door uses single quotes for a root holding `$`/backtick/`"` (E3a) and no command at all for E3b. So for those roots the
card and the door disagree, and the card prints a double-quoted path the shell will expand. F8 moves only the value of
`SCRIPTS`, not its quoting. The card can't call `script_command("<script>")` because the existence check sends it to the
E4 branch. Spec edit (§3.1): `script_command(name, root=None, *, must_exist=True)`. With `must_exist=False` it skips the
E4 branch, and the card head is built as `RP.script_command("<script>", must_exist=False)`. Part A owns `brief_pack.py`,
so this costs one line. Add an E3a row: card head and door use the same quote character. Alternatively, state in §5 E3
that the card keeps double quotes and queue it in OH5-2d. The lighter fix is fine as long as it is written down.

### N5 — the E4/E3b replacement text is spliced in front of argument tails

At :1273/:1275/:1286/:1299/:1616/:823/:875/:1086/:1107, the sites append arguments after the command (`... --task <TICKET>
--row <TS-n> --set ...`). In the E4 or E3b form, the result reads "`` `plan_row.py` (missing from the plugin copy at X; the
conductor runs qa-doctor ...) --task <TICKET> --row ... ``": a sentence with stray flags after it. That's harmless, since
the door is still named, but the spec should say it is intended. Spec edit (§3.1, E4 row): "the site keeps its argument
tail after the replacement text; the built-text row of DoD (3) pins one E4 rendering of `plan_write_check` so the form is
deliberate". Or have the survivor return the text with a trailing "; once repaired: python … " and let the tail follow.
Either way, write one line.

### N6 — §4 claims "None owns an in-flight file", but two of Part A's owns are in flight

`origin/conv/wave-3` (20 commits, which includes `wip/oh3-36` t-232) adds 15 lines to `scripts/refusal_registry.py` (a
REGISTRY entry) and 1 row to `scripts/tests/fixtures/judgment-census.json`. Both files are in Part A's `owns:`. Different
regions are likely, so the conflict should be mechanical. Still, the overlap has to be declared (PROJECT.md «Командная
работа» п.3; CLAUDE.md rule 4). Spec edit §4: "Part A shares `refusal_registry.py` and `judgment-census.json` with conv/wave-3
(oh3-36): Part A branches after wave-3 merges, or merges main and resolves the REGISTRY/census hunks itself; Part B shares
`role-load.json` (B1); a relocated survivor table shares `test_runtime_paths.py` with of4-17b (N1)". No overlap was found for
the other in-flight work the dispatch named: `wip/of4-20-oh5-12` (source_exclusions/ticket_adapter/execution_scheduler/app_card),
`wip/of4-1-4` (install_paths), SC2-43 (handoff_check/handoff_init), `wip/hf84-p2` (controller.py), wave-2 fix
(onboard_apply/check_coverage). OH5-2e will meet `source_exclusions.py:516` later: name it in OH5-2e's row.

## Key 2 — feasibility and edge resolution (each §5 edge)

- E1, E2, E7, E8, E9: resolved right (posix path, quoted, `resolve()`), the same as the card does today.
- E3a/E3b: correct for bash and PowerShell (single quotes are literal in both). The card mismatch is N4.
- E4: correct per FR-59/FR-57. The text form is N5.
- E5, E6: right. The root comes from the running file; `hooks/*.json` are untouched.
- E10: right. The doors are built only on the way to `block` (the ORDER rule, `guard_pre_tool.py:839-841`).
- E11: right. Traced: the A24 keys are the first 90 characters of `block(...)`'s first argument (`_key_text`). Every one of
  the 11 sites is in a `door`/`shell`/`free` variable or past character 90 (:1086 and :1107 sit inside `block(f"PRE-TOOL
  GUARD: {waiting} is waiting..."` well past the key prefix). So no REGISTRY key changes, as §1 AR-9 claims.
- E12: verified. `stage_guard.py`, `inject_context.py` and `refusal_registry.py` have 0 hits on origin.
- E13/E14/E15: an acceptable error direction, named.
- E16/E17: see B3.
- E18-E21: right. The join finds exactly 5 names: report_facts, bug_records, bug_snapshot, retro_numbers, manual_evidence
  (traced against §3.2's five lines; qa-runner's unmarked `manual_capture.py`/`walk_session.py` stay outside the join, as
  intended).
- E22: right (K9, P4, P5 go red in quarantine; traced above).
- Missing edge: the slack-0 process ratchet (B1).
- `test_package_generation` P6 (`"`scripts/"` not in retro/analyst) stays green under §3.2's spelling.

## Key 3 — architecture and P31

- AR-15: the survivor is right. The axis is queued to the Lead (F7). The Part A commit's `architecture:` line must not
  claim AR-15 "kept" while the axis is queued. It should read "AR-15 -- survivor added, axis queued to Lead (F7)".
- AR-8, AR-9, AR-13: kept as specced. Optional: `_config_door`'s `(PLUGIN_ROOT / "scripts" / "config_view.py").is_file()`
  could be `RP.script_path("config_view.py")`, the same value with one reader.
- AR-29: the census class `shape`/`data` is right for a token-presence finding. The conditional census row is correct:
  `findings()` is not a census unit, and a helper named `*_problems` would become one (UNIT_NAME_RE,
  `test_judgment_census.py` docstring).
- AR-20: wrong as written (B1).
- P31 on F1's split: OH5-2d is the same class as Parts A/B, and OH5-2e must be measured first. A split with a named node,
  owns and a test is a legitimate residual under rule 19, not an exclusion, provided the nodes actually get a legal carrier
  (B2). Part C's hand-made env is a P31 defect (B3b).

## Key 4 — the coordinator's fork decisions

- F1: right in substance, wrong carrier (B2).
- F2, F3, F4, F6, F8: right.
- F5: run-mode half right. Verified: no measurer or test in `experiments/` reads `QA_FACTORY_RUN_MODE`. Grep over
  `experiments/`: 0 hits; positive control, the same Grep for `run_headless`, found 3 files. `story_step.current_run_mode`
  (:703-705) stamps `desktop` when the variable is empty, which agrees with `launch_card.desktop_story`. The root half is
  wrong or unmeasured, and the env build is a second road (B3).
- F7: correctly handed to the full Lead.

## Key 6 — executable by a weaker model (pile rule 11)

- Part A is executable once N1, N4 and N5 are written in. The sites, survivor, detector and DoD commands are concrete.
- Part B needs B1 and N2, otherwise the builder hits a red it doesn't own, or a name that doesn't exist.
- Part C needs B3's direction chosen, not left open.

## Standing questions

- DUPLICATION AND CONSISTENCY: B3b (`run_headless.child_env` beside `infra_failure.child_env`) and N4 (card quoting beside
  survivor quoting). Grepped: `def child_env` over `ai-packages/qa-factory/scripts` and `experiments/`, and `SCRIPTS` /
  `python \"{` spellings in `brief_pack.py`. The hand-made `HERE.as_posix()` script spellings in
  `story_step.py:276`/`handoff_check.py:2796` are already queued to OH5-2d.
- CODE QUALITY: none beyond N5 (text form). Checked: the survivor's signature and the lazy import pattern (as at
  `guard_pre_tool.py:554`/`:726`).
- ONE ACTION, ONE ROAD (item 12): B3b blocks (a second env road with no data row and no owner's word). The F1 split is not
  an exclusion once B2 is fixed.

## Class completeness (SIBLING_MAP)

Class: "a path a role needs is given, never an unexpanded host variable". Axis walk:
- Axis 3 (package / release copy / installed plugin): the spec's axis 37 draft is a new axis. B-166's "→ t-304 axis 8"
  points at axis 8 "where the story is on disk", which does not cover the package root. A new axis is justified, and §7
  should say in one line why axes 3 and 8 do not host it.
- Axis 19 (one reader of a role's `tools:` line): Part B's join must go through `host_adapter.role_has_bash` (N2).
- Axis 18 (in-tree shrink-only ratchets): the process ratchet, B1.
- Axis 6 (measurement tools vs the package): run_headless must use the package's `infra_failure.child_env`, B3b.

Siblings outside this node are queued in OH5-2d/OH5-2e (once B2 is fixed). Reported, not widened: `run_headless` also
passes `CLAUDECODE` and the other desktop-host `CLAUDE_CODE_*` names of the launching session (measured, below). B3b's
composition on `infra_failure.child_env` covers the data-listed ones. Any further name is a row in `driver-infra.json`,
not code.

## Trail

Read (origin/main extract): spec t-254 (whole); batch-5 header + rows OH5-2/OH5-4/OH5-13; batch-6 header; findings B-142,
B-166; `guard_pre_tool.py` :16-33, :755-830, :836-880, :1060-1112, :1195-1310, :1596-1630; `runtime_paths.py` :220-240;
`hooklib.py:30`; `brief_pack.py` :36-95, :184-305 (TOOLING), :330-345 (TOOLING_MANUAL), SCRIPTS sites; `refusal_registry.py`
:56-64, :800-996; `test_refusal_registry.py` :1-95; `test_charters_s5_s9.py` :214-230; `test_brief_pack_roles.py` :286-305;
`test_package_generation.py` :484-497; `test_ahead_cards.py` :1-60; `test_guard_command_text.py` :1-40;
`test_runtime_paths.py` def list; `test-layers.json` keep/quarantine rows; `judgment-census.json` header + runtime_paths
rows; `test_judgment_census.py` :1-40; `role_load.py` :135-175, :255-285; `test_role_load.py` :507-546; `audit_factory.py`
:1300-1325; `role-load.json` process rows; agents `## Tools` sections and `kind:` markers; `common-rules.md` :100-140;
`inject-map.json` note + common; `launch_card.py` :155-180; `story_step.py` :695-710; `driver_core.py` :488-520;
`infra_failure.py` :133-170; `driver-infra.json` child_env; `run_headless.py` (whole); `test_measurers.py` :1509-1540;
`docs/SIBLING_MAP.md` headings; `docs/TESTING.md` :1-60.

Reruns / probes:
- `grep -rio claude_plugin_root <origin>/ai-packages/qa-factory | wc -l` -> 420 (local checkout: 419; delta `p4-generate.md`).
- `grep -ni claude_plugin_root guard_pre_tool.py agents/ runtime_paths.py brief_pack.py common-rules.md` -> the 11 guard
  lines and 5 charter lines as specced; `references/slices`: 10 files, all `common-rules.md`.
- `grep -ci claude_plugin_root stage_guard.py inject_context.py refusal_registry.py hooklib.py` -> 0 each.
- `python -B <origin>/scripts/tests/scenario_walk.py --witness-for <Part A paths>` -> includes `test_role_load.py` (via
  brief_pack); `--witness-for <Part B paths>` -> no `test_role_load.py` line (basis of B1).
- branch overlap: `git diff --name-only $(merge-base origin/main B) B -- <owns>` over all remote branches -> conv/wave-3 and
  wip/oh3-36: refusal_registry.py, judgment-census.json; wip/of4-17b: test_runtime_paths.py; conv/wave-3 and wip/hf84-p11:
  role-load.json; nothing else.
- env measurement in this forge session's Bash: `CLAUDE_PLUGIN_ROOT=[] QA_FACTORY_RUN_MODE=[]`; `CLAUDE_CODE_CHILD_SESSION`,
  `CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH`, `CLAUDE_CODE_MESSAGING_*`, `CLAUDECODE` present (basis of B3).
- `grep -rn WITH_BASH scripts --include=*.py` -> only `tests/role_replay.py:49` and its users (basis of N2).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: Part B shrinks process-kind charter text and all 10 common-rules slices; role_load.process_ratchet_problems has slack 0 and keep test_role_load.py:541-546 plus audit A22 go red; references/role-load.json is not in Part B owns and test_role_load is not in its witness",
    "B2: F1(a) opens OH5-2d/OH5-2e as rows of batch-5, which is taken (frozen, PROJECT.md teamwork rule 2); the carrier must be findings files plus rows in batch-6 (status ozhidaet) and README contents rows",
    "B3: F5 sets CLAUDE_PLUGIN_ROOT in the headless child on an unmeasured premise (the forge session's Bash has it empty, so baselines change) and Part C hand-writes a child env beside the package survivor infra_failure.child_env, which strips the host-auth vars measured present in the launching session"
  ],
  "fixes": [
    "B1: Part B owns add references/role-load.json; DoD (5) lower process_ratchet_tokens rows of every role whose process load fell, no raise; verification adds test_role_load.py; edge E23; AR-20 row rewritten; overlap with conv/wave-3 and hf84-p11 named",
    "B2: F1 and the coordinator paragraph: residual nodes go as findings files plus rows in batch-6-ostatki-t-203-i-t-227.md and README contents rows, same move as Part A acceptance",
    "B3: child_env composes infra_failure.child_env(base, infra_failure.rules()[0], {})[0], sets the ceiling, removes QA_FACTORY_RUN_MODE and CLAUDE_PLUGIN_ROOT until OH5-2e measures the host; E16 row extended with CLAUDE_CODE_CHILD_SESSION; given/siblings name infra_failure.py and driver-infra.json; deviation from B-166 reported in section 8",
    "N1: survivor case table moves to test_runtime_paths.py (the module's table layer); Part A owns it; merge after wip/of4-17b",
    "N2: replace role_rules.WITH_BASH with role_replay.WITH_BASH (tests/role_replay.py:49) or host_adapter.role_has_bash",
    "N3: legend first cell reads: references/..., scripts/..., the script paths of your brief card - not 'the paths on your brief'",
    "N4: script_command gains must_exist=False for the card head, or section 5 E3 states that the card keeps double quotes and queues it to OH5-2d",
    "N5: state that the site keeps its argument tail after the E4/E3b text and pin one E4 rendering in DoD (3)",
    "N6: section 4 names the overlap of refusal_registry.py and judgment-census.json with conv/wave-3 (oh3-36), role-load.json with conv/wave-3 and hf84-p11, test_runtime_paths.py with of4-17b; OH5-2e row names source_exclusions.py vs of4-20-oh5-12"
  ],
  "class_completeness": "Class: a path a role needs is given, never an unexpanded host variable. Axis 18 (shrink-only ratchets): missed, B1. Axis 6 (measurers vs package): missed, B3b. Axis 19 (one tools-line reader): DoD names a nonexistent reader, N2. Axes 3 and 8: neither hosts the package root, so the new axis 37 is justified (Lead, F7); section 7 should say why in one line. Role-read residuals (8 code sites, 5 data sites) and conductor-read (248+1) are queued as OH5-2d/OH5-2e, legitimate once B2 gives them a legal carrier.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-254-oh5-2-plugin-root-given.md",
      "origin:plans/piles/onboarding-hooks/batch-5-nerazlozhennye-nakhodki.md",
      "origin:plans/piles/onboarding-hooks/batch-6-ostatki-t-203-i-t-227.md",
      "origin:plans/piles/onboarding-hooks/findings/B-142-desktop-rezhim-komandy-claude-plugin-root.md",
      "origin:plans/piles/onboarding-hooks/findings/B-166-koren-paketa-vo-vremya-raboty-guard-pre-tool-py.md",
      "origin:ai-packages/qa-factory/scripts/guard_pre_tool.py",
      "origin:ai-packages/qa-factory/scripts/runtime_paths.py",
      "origin:ai-packages/qa-factory/scripts/brief_pack.py",
      "origin:ai-packages/qa-factory/scripts/refusal_registry.py",
      "origin:ai-packages/qa-factory/scripts/role_load.py",
      "origin:ai-packages/qa-factory/scripts/audit_factory.py",
      "origin:ai-packages/qa-factory/scripts/infra_failure.py",
      "origin:ai-packages/qa-factory/scripts/driver_core.py",
      "origin:ai-packages/qa-factory/scripts/launch_card.py",
      "origin:ai-packages/qa-factory/scripts/story_step.py",
      "origin:ai-packages/qa-factory/references/common-rules.md",
      "origin:ai-packages/qa-factory/references/role-load.json",
      "origin:ai-packages/qa-factory/references/driver-infra.json",
      "origin:ai-packages/qa-factory/agents/qa-runner.md",
      "origin:ai-packages/qa-factory/scripts/tests/test-layers.json",
      "origin:ai-packages/qa-factory/scripts/tests/test_role_load.py",
      "origin:ai-packages/qa-factory/scripts/tests/test_refusal_registry.py",
      "origin:ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py",
      "origin:ai-packages/qa-factory/scripts/tests/test_brief_pack_roles.py",
      "origin:ai-packages/qa-factory/scripts/tests/test_package_generation.py",
      "origin:ai-packages/qa-factory/scripts/tests/test_ahead_cards.py",
      "origin:ai-packages/qa-factory/scripts/tests/test_judgment_census.py",
      "origin:experiments/measurers/run_headless.py",
      "origin:experiments/measurers/test_measurers.py",
      "origin:docs/SIBLING_MAP.md",
      "origin:docs/TESTING.md"
    ],
    "reruns": [
      {"command": "grep -rio claude_plugin_root <origin extract>/ai-packages/qa-factory | wc -l", "result": "420 (spec 417; delta in conductor-read p4-generate.md; role-read classes unchanged)"},
      {"command": "grep -ni claude_plugin_root guard_pre_tool.py (origin)", "result": "11 lines: 771 823 875 1086 1107 1231 1273 1275 1286 1299 1616, as specced"},
      {"command": "python -B <origin>/scripts/tests/scenario_walk.py --witness-for <Part A paths>", "result": "prints test_role_load.py among keep rows (via brief_pack.py)"},
      {"command": "python -B <origin>/scripts/tests/scenario_walk.py --witness-for <Part B agents + common-rules>", "result": "no test_role_load.py line"},
      {"command": "git diff --name-only merge-base..branch -- <Part owns> over all origin branches", "result": "conv/wave-3 and oh3-36: refusal_registry.py, judgment-census.json; of4-17b: test_runtime_paths.py; conv/wave-3 and hf84-p11: role-load.json"},
      {"command": "echo CLAUDE_PLUGIN_ROOT / QA_FACTORY_RUN_MODE; env | grep ^CLAUDE (forge session Bash)", "result": "both empty; CLAUDE_CODE_CHILD_SESSION, CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH, CLAUDE_CODE_MESSAGING_* present"},
      {"command": "grep -rn WITH_BASH scripts --include=*.py (origin)", "result": "only tests/role_replay.py:49 and test_brief_pack_roles users; role_rules.py has none"}
    ]
  }
}
```
