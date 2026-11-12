# t-142 — critic on plan, second narrow pass: OF3-1 spec after fix round t-139

Critic (Opus), 12.11.2026. Plan gate, PROJECT.md "new idea" step 6 (second pass, narrow). Spec under review:
`docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` (564 lines, working tree on `main`, uncommitted edit). First pass:
`docs/tasks/specs/reviews/t-137-of3-1-plan-critic.md`. Scope as dispatched: §1, §5 "Nodes and owns", §6 F4.1 and F7-F10 (F11 framing
only), §7; plus closure of the seven t-137 blockers. Owner's word F3 (a), F6 (b) not reviewed.

**Verdict: ACCEPT WITH FIXES — 3 fixes block dispatch of the node they name (X-1 node c, X-2 node a, X-3 node d); 7 more are edits of
the same round (X-4..X-10).** All seven t-137 blockers are closed in the text, not only logged in §8. The a-f cut is sound except one
collision with the live stream "tests" that §5's no-write list does not name. This verdict is an input; accepting the spec and
dispatching nodes is the coordinator's/Lead's decision.

---

## Q1 — the seven t-137 blockers, closed in the text?

| fix | closed? | where in the spec (line) |
|---|---|---|
| F-1 `KEYS` readers | yes | §0 F-1b :51-54 names all readers; §3 :238-241 derived `KEYS`, same five keys/order, `record_problems`, `report_facts` :1991/:1993/:2180 and `test_gate_role_accounts.py:82` not edited; §2 :221 row order; item 2 :297 behaviour row replaces the pin |
| F-2 STOP clause | yes | DoD :385-387 carves out `test_config_migration.py:374-375`, `test_reinstall_equals_fresh.py:150`, the G5 rows; node a owns `test_reinstall_equals_fresh.py` :399 |
| F-3 artifact_root edges | yes | item 7 :361 three classes; :364 project-root source for vcs; :367 old-default `--output` row; digest :38-40; §4 :277-279; dispatch_liveness half in §7 :480 with `unknown` |
| F-4 test ownership / collision | yes for what t-137 named | covers in a :400; R2/R3 moved to f :415; `очередь: small → OF3-1d2` :480; announcement :488-489. (A new collision this pass found: X-1) |
| F-5 artifact_root class | yes | item 7 :362-371 (`_case_needs`, scheduler in c; vcs, local_keys, role_load in d); B-348 -> N-r5 :485; axis 8 :371. (One site's fact is wrong: X-6) |
| F-6 R2/R3 scoping | yes | item 3b :305-313: R2 bound to the NAME holding a reader's return value plus declared `carriers`; miss direction "BLIND TO"; R3 as (file, function, key) triples; §4 :267-269 |
| F-7 data_cleanup mapping | yes | item 6 table :342-351 (adds falsy non-list and non-object rows); keep tests named :355-358 (`test_config_projection.py` covers env_probe — confirmed by rerun) |

## Q2 — the a-f cut

**Owns disjoint among parallel nodes.** Verified on §5 :395-421. Only shared production file among b/c/d/e: `env_probe.py`, c =
`CLEANUP_UNKNOWN`, `data_cleanup`, `_case_needs`, the import line; e = `parse_env_file`. Function-disjoint, later merges `main`: the
D-0048 form, ACCEPTABLE (no other env_probe function moves; `manual_capture`/`stand_health` import env_probe lazily inside functions,
grep :498/:544, :428-:803, so e's call from `manual_capture._env_values` adds no import-time cycle). `test-layers.json`,
`test_config_migration.py`, `config-keys.json` are a -> f serial. OK.

**No node writes a live stream's file — one miss (X-1).** Stream plan `docs/tasks/onboarding-streams-2026-11-12.md:15-21` plus the
node rows' "Пишет в" (batch-1/batch-2): handoff (`handoff_init.py`, `handoff_check.py`, `test_handoff_init.py`, `test_handoff_values.py`),
hooklib (`hooklib.py`, `install_smoke.py`, `run-py.cmd`, `launch-causes.json`, `cost_capture.py`, `factory_dashboard.py`,
`test_cost_capture_*`), hot (`stage_guard.py`, `controller.py`, `story_run.py`, `question_register.py`), small (`dispatch_liveness.py`,
`story_progress.py`, `codex_usage.py`, four references), hooks4 (`gate_brief.py`, `test_gate_brief_and_retro.py`): none in a-f owns.
**But stream "tests" (t-135) runs OH3-25, whose row** (`batch-2-onboarding-roles-forge-p3.md:61`) **writes 13 test files including
`test_brief_pack.py`** — node c owns `P\scripts\tests\test_brief_pack.py` (§5 :409). §5's no-write list :391-393 omits stream "tests".
Also `test_report_facts.py` is in OH3-25 — node a does not write it (item 2 :300 keeps it unchanged): fine.
Note for the coordinator (not a finding): EP1-19's row says `references/` wholesale and DC1-27/28 rows say `scripts/tests/`; the stream
plan narrows them to named files, which do not include `config-keys.json`, `templates/config.json` or any a-f test file.

**Each node has a test:** a (items 1, 2, 3a, 4 rows), b (`test_read_json.py` rows), c (`test_config_projection.py`, `test_audit_rules.py`,
`test_brief_pack.py`), d (`test_vcs_evidence.py`, `test_local_keys.py`, `test_role_load.py`), e (`test_manual_capture.py`), f (R2, R3).
All keep files; rerun of `--witness-for` confirms each covers its production file (trail).

**Executable by a weaker model** (PROJECT.md «Командная работа» 11): mostly yes; three gaps — the vcs story recognition under a
configured root is under-specified in the unsafe direction (X-3), `local_keys._taken` is described as a hard-code it is not (X-6), and
F4.1's chosen sentence is not in node a's item list (X-7). Minor: node a must fill `needed_by` "every reader R2's scan finds" (§2 :216)
before R2 exists (it lands in f); say a fills it from its own grep and f reconciles (f already owns `needed_by` values :416) — fold into X-7.

## Q3 — forks

- **F4.1 (a) — agree, with X-7.** p4-generate.md is the phase that writes the config, read by the onboarding role, which is how the person
  learns; it is already in a's owns. But the sentence is not in items 1-4 or 7 — a builder executing node a from its items will not write
  it.
- **F7 a-f + OF3-1d2 — agree, with X-1.** Moving R2/R3 to f removes the shared-baseline writer problem (t-137 F-4 (b)); c taking
  `_case_needs` keeps env_probe at two writers; `test_config_projection.py` is the only keep row covering `execution_scheduler.py`
  (rerun confirms) and c owns it.
- **F8 (a) — agree.** A `store: record:<file>` row with no phase-1 reader through the one reader is exactly the AR-22 strain t-137 F-12
  removed elsewhere; the move list (§2 :226-230) gives each carrier a phase and reason. Deviation from the node row is recorded (:507-508).
- **F9 (a) — agree with the recommendation; its load-bearing fact is FALSE (X-4).** §6 :444 says "the revert code reads `written_by` to
  decide what a story may keep — config_contract.py:2530". Read: :2530 is `restore_config`'s docstring ("except what a recorded writer
  wrote in the window"); the "recorded writers" are computed by `recorded_writes` :2381-2410 from the approvals log, report adaptations
  and project-decision receipts, and the runtime probe by its entry's note (:2386-2387, `SUGGEST_SOURCE` :2239). Case-insensitive grep
  `written_by` in config_contract.py: 0 hits (positive control: same file, `_write_config|written` found :2190, :2231). The
  `written_by` table (config-keys.json:705-714) is read by onboard_apply.py:973 (the "changed since install" check) and pinned by
  test_config_migration.py:193-197 — and it ALREADY carries `execution.runtime_probes -> runtime_probe.py`, so one of the three writers
  is already recorded there. (a) still wins on its other reason (folding writers changes write paths and the revert's kept-pointer logic,
  not a refactor), but the stated reason must be replaced.
- **F10 (a) — agree.** Verified vcs_evidence.py:581-615: `_story_root_of` :611 outside any try; :613 `artifact_root()` inside `except
  OSError` only; the docstring :599-605 says "Nothing recorded anywhere: None, and the tool runs" and "must not be the door around the
  word" — so (b)'s `return None` on a broken config would skip the person's word: unsafe, correctly rejected. The pre-existing traceback
  goes to finding (2) of §7 (a refusal with a door is the real FR-1 fix, outside node d's owns): correct routing.
- **F11 framing — adequate, one gap (X-9).** Framed as a question with both sides cited (B-319 BACKLOG.md:327 "обратный приоритет" vs
  env_probe.py:116-119 "a local setting beats the shared one") and the node stays executable ("nothing changes until"). It carries no
  recommendation; «Командная работа» 11 asks for one.

## Q4 — §7 entries: owns + test + satisfiable when

| id | owns | test | when | verdict |
|---|---|---|---|---|
| OF3-1d2 | yes | yes | `очередь: small → OF3-1d2` — satisfiable | ok; but shares `dispatch_liveness.py` with N-r4 (X-8) |
| N-r1 | partly by pointer to c's census (stand_gaps, env_probe named) | yes | phase 3.2 — satisfiable | ok for a queue entry |
| N-r2 | `hooklib.py`, `manual_capture.py` + "the callers in the census" | yes | after streams hooklib, hot — but the census is node c's output | add "after node c's census is accepted" (X-8) |
| N-r3 | yes | yes | after a | ok |
| N-r4 | yes (writes hot/hooklib/small files) | yes | after those streams | needs order with OF3-1d2 (dispatch_liveness) and OF1-1 (env_probe) (X-8) |
| N-r5 | yes | yes (`test_bug_records.py` covers traceability, :404) | after d (no real dependency, harmless) | ok |
| N-r6 | `project_decisions.py`, `runtime_probe.py` only | test in `test_config_migration.py` (a/f's file; serial after them, fine) | phase 2 | owns misses `config_contract.py`: `_write_config` needs an `approval_ref`/`input_hash` the probe does not have, and `recorded_writes`/`_kept_pointers` :2381-2470 key the revert on approvals/receipts; also `restore_config` writes config.json itself (:2604 via `_replace_bytes`) — a write site F-8b does not name (X-5) |

Target batch: §7 :476 says "the not-taken batch of `onboarding-forge`". All three onboarding-forge batches are taken (commit 8241f75;
batch-3 header :3 "статус: в работе | взял: dev1"); a taken batch is frozen to new nodes (PROJECT.md «Командная работа» 2). The
coordinator must open `batch-4` (D-0044) — X-8.

## Q5 — AR-14 and AR-9 claims

- **AR-14 holds** for nodes a-f: no node writes `config.json` (owns checked); a changes the template shape only. The writer census is
  incomplete by one site inside the writer module (`restore_config` :2604), which does not break the claim "adds no writer" — folded into X-5.
- **AR-9 holds on the healthy path, NOT on the damaged-catalogue edge the spec itself creates (X-2).** §4 :270: damaged
  `config-keys.json` -> `rows()` `[]` -> `KEYS` `{}` -> "`record_problems` refuses every key". The refusal then reads
  ``the key 'product.roles' is not a project-knowledge key (the keys: ); nothing was recorded`` (project_knowledge.py:356 with an empty
  `KEYS`): it states a false cause and names an empty door, while the true cause sits unused in `CATALOGUE_PROBLEM` (§3 :235). FR-1
  (say what is wrong and how to satisfy it). Before this spec the state could not occur (the literal cannot be damaged): it is a new edge,
  so the §1 AR-9 row "keeps its text and door byte-equal" is true only while the catalogue reads.

---

## Findings and fixes

**Blocking dispatch of the named node:**

- **X-1 (§5 Nodes and owns, node c; Q2)** — node c owns `scripts/tests/test_brief_pack.py`, which stream "tests" (t-135, OH3-25,
  batch-2 :61) also writes. Either add `очередь: tests → OF3-1c` (or OH3-25 → OF3-1c) in both carriers, or declare the D-0048 split in
  c's owns (`test_brief_pack.py` — the new strategy-row function only; the later node merges `main` first), and add stream "tests"' files
  to §5's no-write list :391-393.
- **X-2 (§1 AR-9 / §3 / §4 :270; node a)** — when `KEYS` is empty because `CATALOGUE_PROBLEM` is set, `record_problems` returns the
  catalogue problem (its message names the door "reinstall the plugin") instead of the "not a project-knowledge key (the keys: )" text;
  one row in item 2's `test_project_knowledge.py` set (damaged catalogue -> refusal names the damage, nothing recorded). Correct the §1
  AR-9 row to say so.
- **X-3 (§5 item 7 node d / §1 AR-28 row; node d)** — "a story is `<configured root>/<T>` when `output` lies under the configured root"
  (:365) narrows consultation to a folder that need not be a story. Scenario: `artifact_root: "."`, story `<project>/S-1` records "do
  not read MR U", call with `--output <project>/tmp/x.json`. Today: no `qa-factory/artifacts` parts -> no story -> every dir under
  `artifact_root()` (the project) consulted -> S-1's word refuses. After: story = `<project>/tmp`; `SE.live` on a folder without the
  record returns `[]` (source_exclusions.py:324-331) -> no match -> the tool reads U. The person's word is skipped — exactly the §4 :279
  invariant. Fix: recognise `<root>/<T>` only when it is an existing story folder (state the marker the spec uses, e.g. `pipeline.json`
  or `work/`), else fall to today's recognition and then to the all-stories path; add the row "output under a configured root but not in
  a story folder: every story consulted" to `test_vcs_evidence.py`. (The same defect exists today for an `--output` file placed directly
  in `qa-factory/artifacts/`: name it in finding (2), not in d.)

**Same round (non-blocking for dispatch, required before acceptance of the spec):**

- **X-4 (§6 F9 :444, :462-463)** — replace the false reason (config_contract.py:2530 does not read `written_by`; the revert reads
  `recorded_writes` :2381) with the real readers: `written_by` -> onboard_apply.py:973 and test_config_migration.py:193-197; note that
  `execution.runtime_probes -> runtime_probe.py` is already a `written_by` row; drop "UNVERIFIED".
- **X-5 (§7 N-r6, §0 F-8b)** — N-r6 owns add `config_contract.py` (`_write_config` signature, `recorded_writes`, `_kept_pointers`) and
  its test names "the revert keeps each writer's pointers as today (`restore_config`)"; F-8b names `restore_config` :2604 as a second
  write site of the writer module.
- **X-6 (§0 F-18b, digest item 7 :38, item 7 node d)** — `local_keys._taken` ALREADY reads `hooklib.artifact_root(root=project)`
  (local_keys.py:130-133); the literal at :133 is its fallback on `(OSError, ValueError)`. Node d's change there is only adding
  `AttributeError` (a JSON-list config crashes today); the digest must not list it as "now looks under the configured root", and its
  test row "configured root honoured" is a today-behaviour row, not a new one (keep only the broken-config-as-list row).
- **X-7 (§5 item 4 / node a; F4.1, §2 `needed_by`)** — put F4.1's sentence into node a's items (file `p4-generate.md`, where, the text:
  optional key, default `qa-factory/artifacts`), with "doc line, no test" stated; and say node a fills `needed_by` from its own grep,
  f reconciles through R3.
- **X-8 (§7)** — target: open `onboarding-forge` batch-4 (all three batches are taken); queue lines `OF3-1d2 → N-r4`
  (dispatch_liveness) and `OF1-1`/`N-r4` order on `env_probe.py`; N-r2's when adds "after node c's census is accepted".
- **X-9 (§6 F11)** — add a recommendation (e.g. keep file-over-process as the docstring states, and close B-319's sub-claim as "by
  design" on the owner's yes) so the question reaches the owner in the «Командная работа» 11 form.
- **X-10 (§5 item 7, node c; P31)** — `execution_scheduler._apply_budget`/`execute_schedule` (:354, :574) WRITE job stores under the
  story folder; item 7 has them fall back to the default folder on a broken config, while `hooklib.artifact_root`'s own comment
  (hooklib.py:640-641) says a broken config "must raise ... not ... silently put the artifacts into the default root (AR-28, AR-4)" and
  every hooklib-routed writer raises. Today's scheduler writes there anyway, so the fallback is byte-for-byte today's, but the spec must
  state this writer-site direction and why it differs from the other writers (or let it raise) — one action, two directions, unstated.

## Standing questions

- **DUPLICATION AND CONSISTENCY:** one inconsistency (X-10: writer-site fallback vs hooklib writers' raise). `local_keys` already had a
  two-class catch; the spec unifies to three classes — good (X-6). Grepped: `"qa-factory" / "artifacts"` sites read (execution_scheduler
  :345-360, :565-580; local_keys :125-140; role_load :530-545; env_probe :670-685), `written_by` over the package, config.json writers
  (`write_text`/`_replace_bytes`/`_atomic`) over scripts.
- **CODE QUALITY:** plan gate, no code. Spec-level: X-3 (under-specified recognition), X-6 (stale fact). Nothing else in scope.
- **ONE ROAD (P31, brief item 12):** no language/project exclusion; the shared mechanism `hooklib.artifact_root` is reached at every
  item-7 site; X-10 is a direction split to be stated or removed. Residuals leave as §7 nodes (once X-8 gives them a batch).

## Class completeness (SIBLING_MAP)

Axis 8 (story on disk): six sites in c/d + OF3-1d2 + N-r5 — complete by the t-139 grep; the vcs recognition class gains X-3. Axis 16:
unchanged since t-137, residual N-r4 (ordering X-8). The `KEYS` reader class: complete on the healthy path; the damaged edge X-2.
C18 writers: `restore_config` added (X-5).

## Trail

Read: the spec whole (:1-564); t-137 review whole; stream plan whole; batch-2 :61 (OH3-25); stream node rows (LR1-5, CD1-11, OH3-37,
SC2-42, HF8-28/29, DC1-27/28, CX2-12, TQ1-28, RC1-15, EP1-19) owns columns via grep over `plans/piles/onboarding-forge/*.md`; batch-3
header :1-19 and rows :25-28; vcs_evidence.py:570-630; source_exclusions.py:324-331; hooklib.py:630-655; config_contract.py:2228-2239,
:2380-2410, :2515-2549 and greps (`written_by` 0 hits, writer grep); config-keys.json:700-715; onboard_apply.py:962-983;
project_decisions.py:440-465 + `_atomic` grep (:489 config write); runtime_probe.py:1478-1497; execution_scheduler.py:345-360, :565-580;
local_keys.py:125-140; role_load.py:530-545; env_probe.py:100-130, :670-685; project_knowledge.py `KEYS`/import grep (:32, :46-49, :98,
:136, :268, :349-368, :383); BACKLOG.md:325-330.
Searches (positive controls): `written_by` -i in config_contract.py [0; control `_write_config|written` same file: :2190, :2231];
`written_by` -i over the package [config-keys.json:705, onboard_apply.py:973]; `import env_probe` in manual_capture/stand_health [found].
Reruns: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/env_probe.py scripts/execution_scheduler.py
scripts/audit_factory.py scripts/brief_pack.py scripts/vcs_evidence.py scripts/local_keys.py scripts/role_load.py scripts/manual_capture.py
scripts/stand_health.py` — env_probe and execution_scheduler covered by `test_config_projection.py`; audit_factory by `test_audit_rules.py`;
brief_pack by `test_brief_pack.py`; vcs_evidence by `test_vcs_evidence.py`; local_keys by `test_local_keys.py`; role_load by
`test_role_load.py`.
Not read: dispatch_liveness.py:955 (`in_flight_entry` catch — t-137 verified), config-keys.json:465; sections outside scope (§2-§4 except
lines cited above); the hooklib stream's own test list beyond the node rows.
needed beyond the manifest: scripts/vcs_evidence.py, scripts/source_exclusions.py, scripts/hooklib.py, scripts/config_contract.py,
references/config-keys.json, scripts/onboard_apply.py, scripts/project_decisions.py, scripts/runtime_probe.py,
scripts/execution_scheduler.py, scripts/local_keys.py, scripts/role_load.py, scripts/env_probe.py, scripts/project_knowledge.py,
plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md, plans/BACKLOG.md.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "X-1 node c owns scripts/tests/test_brief_pack.py, also written by live stream tests (OH3-25, batch-2 :61); spec section 5 no-write list omits that stream",
    "X-2 damaged catalogue: KEYS empty makes record_problems refuse with a false cause and an empty key list (project_knowledge.py:356) while CATALOGUE_PROBLEM holds the real one; the section 1 AR-9 claim holds only on the healthy path",
    "X-3 node d vcs story recognition under a configured root accepts any folder under the root; with artifact_root '.' and an output outside a story, consultation narrows to a non-story folder and the person's do-not-read word in another story is skipped"
  ],
  "fixes": [
    "X-1 queue line tests to OF3-1c in both carriers or a D-0048 function split in c's owns; add stream tests files to the section 5 no-write list",
    "X-2 record_problems returns CATALOGUE_PROBLEM with its door when KEYS is empty for that reason; one test_project_knowledge row; correct the section 1 AR-9 row",
    "X-3 recognise configured-root stories only for an existing story folder with a named marker, else today's recognition then all-stories; add a test_vcs_evidence row",
    "X-4 section 6 F9: replace the false config_contract.py:2530 reason; real written_by readers are onboard_apply.py:973 and test_config_migration.py:193; runtime_probe already a written_by row",
    "X-5 section 7 N-r6: owns add config_contract.py (recorded_writes, _kept_pointers, _write_config); F-8b names restore_config :2604",
    "X-6 local_keys._taken already reads hooklib.artifact_root (local_keys.py:130-133); node d only adds AttributeError; correct digest item 7 and the test row",
    "X-7 put the F4.1 sentence into node a's items with its place and text; state node a fills needed_by by grep and f reconciles",
    "X-8 section 7: open onboarding-forge batch-4 (all three taken); queue OF3-1d2 before N-r4 and order N-r4 with OF1-1 on env_probe.py; N-r2 waits for node c's census",
    "X-9 section 6 F11: add a recommendation for the owner",
    "X-10 item 7 node c: state the fallback direction for execution_scheduler as a writer site versus hooklib writers that raise, or let it raise"
  ],
  "class_completeness": "Axis 8 artifact_root sites complete by the t-139 grep (six in c/d, OF3-1d2, N-r5); new edge X-3 in the vcs recognition. Axis 16 residual N-r4 needs ordering (X-8). KEYS reader class complete on the healthy path, damaged edge X-2. C18 writer census misses restore_config :2604 (X-5).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-129-of3-1-knowledge-catalog.md:1-564",
      "docs/tasks/specs/reviews/t-137-of3-1-plan-critic.md",
      "docs/tasks/onboarding-streams-2026-11-12.md",
      "plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md:61",
      "plans/piles/onboarding-forge/batch-3-znaniya-o-proekte-fazy-1-6.md:1-28",
      "ai-packages/qa-factory/scripts/vcs_evidence.py:570-630",
      "ai-packages/qa-factory/scripts/source_exclusions.py:324-331",
      "ai-packages/qa-factory/scripts/hooklib.py:630-655",
      "ai-packages/qa-factory/scripts/config_contract.py:2228-2239,2380-2410,2515-2549",
      "ai-packages/qa-factory/references/config-keys.json:700-715",
      "ai-packages/qa-factory/scripts/onboard_apply.py:962-983",
      "ai-packages/qa-factory/scripts/project_decisions.py:440-465",
      "ai-packages/qa-factory/scripts/runtime_probe.py:1478-1497",
      "ai-packages/qa-factory/scripts/execution_scheduler.py:345-360,565-580",
      "ai-packages/qa-factory/scripts/local_keys.py:125-140",
      "ai-packages/qa-factory/scripts/role_load.py:530-545",
      "ai-packages/qa-factory/scripts/env_probe.py:100-130,670-685",
      "plans/BACKLOG.md:325-330"
    ],
    "reruns": [
      {
        "command": "python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/env_probe.py scripts/execution_scheduler.py scripts/audit_factory.py scripts/brief_pack.py scripts/vcs_evidence.py scripts/local_keys.py scripts/role_load.py scripts/manual_capture.py scripts/stand_health.py",
        "result": "env_probe and execution_scheduler covered by test_config_projection.py; audit_factory by test_audit_rules.py; brief_pack by test_brief_pack.py; vcs_evidence by test_vcs_evidence.py; local_keys by test_local_keys.py; role_load by test_role_load.py"
      }
    ]
  }
}
```
