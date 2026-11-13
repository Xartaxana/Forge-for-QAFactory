# t-300: critic on plan, one topic (R13-g): where the story lives under a configured artifact_root

Specs under review:
- `docs/tasks/specs/t-289-of4-10-artifact-root.md` (OF4-10), with the coordinator decision in §12 (F-1 (b), the rest as recommended)
- `docs/tasks/specs/t-290-of4-21-brief-pack-paths.md` (OF4-21), with the coordinator decision in §11 (every fork as recommended)

Critic: Opus, 2026-11-13. The verdict is an input to acceptance. Accepting the specs and opening the nodes is the coordinator's decision, not mine (critic rule 6).

## Which tree I read

The local `main` checkout (`C:\QAFactory\forge-repo\ai-packages\...`) has drifted away from origin: local `main` eb6b624 is 196 commits behind `refs/remotes/origin/main` and 34 ahead of it. It lacks 0a0db4f, PR #7, wave 6 and PR #11. For example, local `hooklib.artifact_root` sits at :647 and has no non-object check. I noticed this before the coordinator's correction arrived. So every claim below was checked against `refs/remotes/origin/main` = **ca2f04a** (through `git show`, and through the `read-main` worktree once the correction came). That worktree is detached at ca2f04a; I confirmed with `git -C …/read-main rev-parse --short HEAD`, which printed `ca2f04a`.

Between my first extraction (c97dd95) and ca2f04a, the package diff touches only these files: `brief_pack.py`, `guard_pre_tool.py`, `refusal_registry.py`, `runtime_paths.py`, and the tests `test_ahead_cards`, `test_brief_pack`, `test_charters_s5_s9`, `test_guard_big_read_sections`, `test_refusal_registry`, `test_runtime_paths` and `test_walk_plan_fields`. I re-read every claim that touches those files at ca2f04a. The t-289 files (`hooklib`, `config_contract`, `vcs_evidence`, `exit_gate`, `test_read_json`, `test_vcs_evidence`) are byte-identical between the two commits.

Side note for the coordinator: the §12 import-time measurement says "Run on main". If it ran in the stale local tree, the number came from the wrong code. I re-ran it on ca2f04a (Reruns) and it holds, so F-1 (b) stands.

## Verdicts

- **t-289 (OF4-10): fit_with_fixes.** The blocking findings are B1-B3.
- **t-290 (OF4-21): fit_with_fixes.** The blocking findings are B4-B6.

Machine verdict for the pair: `fit_with_fixes` (block at the end).

---

## Key 1. Facts by trail (all at ca2f04a)

### t-289

| claim | carrier | result |
|---|---|---|
| F-1: `artifact_root` :691-706, its own `json.loads` at :697, a non-object raises `ValueError` at :698-699, the key check at :703-704, and the finding's "AttributeError" is stale | `hooklib.py:691-706` | holds |
| F-2: `ConfigUnreadable(ValueError)` :1321, `read_config_file` :1349-1374, the `except ValueError` at :1368 misses `RecursionError`, lazy `import hooklib` at :272 and :939, and hooklib's lazy `import config_contract` at :2737 | `config_contract.py`, `hooklib.py` | holds |
| F-4: branch (2) of `_story_root_of` returns `Path(*parts[:index+2])` with no story test, so `artifacts/x.json` is returned as the story | `vcs_evidence.py:581-604`, traced by hand: index = len-2 is `artifacts`, so the slice is the file | holds |
| F-5: :628 sits in `except OSError: return None` (:629-630); `main` :652 prints `excluded` for every refusal | `vcs_evidence.py:607-676` | holds |
| F-6 / F-8: `grounding_errors` :1563 is outside any try; `_identity` :287 is outside the try at :292; `awaiting_source_review` :1519 is outside its try | `exit_gate.py` | holds |
| F-12: OH6-1 owns `is_one_component`, `is_story_folder`, `_named_ticket` and a top-level `import hooklib` | `git diff 7e1ddab wip/oh6-1` | holds (Key 6) |
| AR-13 row: "positive control: `read_json` :765" | `hooklib.py` | **stale**: `read_json` is at :751. The grep control still works, so this does not block |
| F-9: test homes | `test-layers.json` at ca2f04a | holds: `test_read_json` and `test_vcs_evidence` are keep, `test_exit_gate_grounding` is quarantine |

### t-290

| claim | carrier | result |
|---|---|---|
| 27 literal lines at the listed numbers, unchanged after OH5-2 | `grep -n -i "qa-factory/(artifacts\|strategy)" brief_pack.py` at ca2f04a | holds: 27 lines, same numbers |
| OH5-2 edits `command_card_lines` :3675 and `build` :4260 through `RP.script_command(...)` | `git diff c97dd95 ca2f04a -- brief_pack.py` | holds, and it is now ON main (wave 6 = PR #11 merged, `80e0e19`), so §11 Q2's precondition is met |
| `_bundle_view` passes `task_root` as `project` (:1151) | `brief_pack.py:1137-1155` | holds |
| `case_paths` :1248 and `_excluded_files` :1443 are prefix parsers | `brief_pack.py` | holds |
| "`command_card_lines`: no caller outside `brief_pack`" | `git grep "command_card_lines("` at ca2f04a | **FALSE**: `scripts/tests/test_refusal_registry.py:145` calls `brief_pack.command_card_lines("T-1", "walk-1", (), "")`. Wave 6 added it after the designer's snapshot (B4) |
| `runtime_paths.py (:38-188, :715-799)`: `project_for_task` at :739 | `runtime_paths.py` | **shifted**: wave 6 added `package_root` and `script_command` (:229, :248); `_admits` is now :752 and `project_for_task` :774 (B5) |
| layer status of the 11 named tests | `test-layers.json` | holds, re-checked at ca2f04a |

## Key 2. Feasibility against the AR-n each spec names, and P31

### t-289 F-1 (b): can `read_config_file` move into hooklib?

Yes. It is self-contained. Its body (`config_contract.py:1349-1374`) depends on only three things:
- `pathlib.Path`, already imported by hooklib :12;
- `json`, already imported by hooklib :5;
- the class `ConfigUnreadable` (:1321), which moves with it.

It touches no other `config_contract` name: not `KEYS_PATH`, not `config_keys`, not `effective_config`. The §12 edge "stop if it drags a chain" therefore does not fire.

The re-export carries no cycle risk. hooklib's top-level imports are stdlib only, and its one `config_contract` import is lazy (:2737). So `config_contract` may import from hooklib at top level.

Consumers of the re-export: `onboard_apply`, `onboarding_probe`, `config_view`, `exploration`, `project_knowledge`, `import_test_receipt`, `controller`, `execution_scheduler`, `judge_code`, `brief_pack`, and `config_contract:3031` itself. They all use `C.ConfigUnreadable` / `C.read_config_file` as attributes. No test monkeypatches either name (searched for `monkeypatch|setattr`). No test reloads hooklib or config_contract (only `test_project_knowledge` reloads its own module).

The feasibility problem is the census, not the move. That is **B1**.

### t-289: the other AR-n

- **AR-28** holds (§4 and §5 are sound).
- **AR-24**: F-10 is the right call. I traced the file-as-story hole myself.
- **AR-18** holds: `unreadable_record(script, reason, owner_file)` exists at :66, and its text contains `grounding_errors: unreadable` as T1 expects.
- **P31**: F-1 (b) plus F-12 (a) is one road.
- **AR-29**: blocked by B1.

### t-290

- **AR-13 and AR-15** are feasible. `project_for_task` → `_admits` catches `Exception` around `artifact_root` (`runtime_paths.py:752-771`), so `story_text` will never raise, whatever OF4-10 does to the exception class.
- **AR-4 / F5**: the absolute form for an outside root is reasonable, and it is correctly queued as an owner question.
- **P31**: one survivor; the residual is the named node OF4-21b.

## Key 3. Edges: blocking findings with fix lines

### B1 (t-289). The census row of `artifact_root` loses its unit, so DoD 5 cannot pass as written

**Surface:** the judgment census's unit recognition (u3 = a literal `raise ValueError|StateConflict` that `refusal_registry.sites()` sees).

**Measured:** at ca2f04a, `refusal_registry.sites(files=['hooklib.py','config_contract.py'])` sees `artifact_root` only at :699 and :704, the two literal `raise ValueError`. It sees nothing in `read_config_file`.

**What breaks:** §2.1 turns both raises into `ConfigUnreadable` and moves the non-object raise into `read_config_file`. After that, `artifact_root` is no longer a unit (no u1 name match, no u2 judge call, no u3 site). Census row `judgment-census.json:398` is orphaned and C1 ("every row a unit") goes red. That contradicts §1, which says ":398, unchanged", and DoD 5, which says "green with no row added, removed or raised". The census file is a non-goal.

The census docstring (`test_judgment_census.py:34-37`) names this exact blind spot: "a subclass of ValueError raised by its own name is invisible… a subclass chosen to keep a ratchet down is not seen — the critic's question 11 … catch it". Deleting the row would hide a refusal that reaches every role, so the row must stay alive.

**Neighbours on the same surface:**
- `hooklib.read_config_file` (moved): not a unit before or after. No change.
- `artifacts_dir` :239: keeps its literal `ValueError`. No change.
- `config_contract`: loses only a non-unit. No change.

**Fix line (paste into §2.1 item 3 and §1 AR-29 row):**
> Census (B1, t-300): the key-value and `resolve` refusals inside `artifact_root` stay a literal `raise ValueError(<the finished text of item 3>)` (class `ValueError`, `ConfigUnreadable` is not used for them), so `refusal_registry.sites()` keeps seeing `artifact_root` and census row `judgment-census.json:398` keeps its unit; read and parse failures arrive as `ConfigUnreadable` from `read_config_file`. T1 `locator` token `refused` = raises a `ValueError` (ConfigUnreadable included) whose text contains `config.json`. If `test_judgment_census.py` C1 still names `hooklib.py: artifact_root`, the builder RETURNS the question; deleting row :398 is out of bounds.

### B2 (t-289). The new refusal text in `left_out_by_person` adds a new instance of the literal that OF4-21 removes

§2.3 writes the text "…Run it with --output under the story's own folder (qa-factory/artifacts/<story>/work/)…". That branch runs exactly when the artifact root is unknown, so naming the default folder is a guess (FR-37, AR-28). It is also a new sibling of the class this topic is removing; t-290 §6 already queues `vcs_evidence.py:646` for OF4-21b. Under rule 9 / P31, the same topic must not grow the class.

**Fix line (§2.3):**
> The refusal text names no default folder: "...Run it with `--output` under the story's own folder (`<artifact root>/<story>/work/`), or say so in your handoff." (B2, t-300; the placeholder form of `hooklib._example_folder`; the existing :646 text stays for OF4-21b.)

### B3 (t-289). The body of the spec still prescribes F-1 (a), which contradicts §12

Two places still prescribe the lazy import:
- §2.1 item 1: "[F-1 (a): `import config_contract` inside the function]";
- the §1 AR-12 row: "hooks now import `config_contract` lazily on every `artifact_root` call [F-1 (a)]".

§12 decides (b), but nowhere states the structural invariants of (b). A Sonnet builder reads contradictory instructions and an unstated positional edge (rule 11 (ii)).

**Fix line (append to §12 F-1, and strike the F-1 (a) clauses of §2.1 item 1 and the AR-12 row):**
> F-1 (b) shape (B3, t-300): `ConfigUnreadable` and `read_config_file` move VERBATIM into `hooklib` (they need only `Path`, `json` and the class: no other `config_contract` name; checked at ca2f04a), with the F-3 `RecursionError` catch added there; `artifact_root` calls `read_config_file(project)` directly, so no import is added to it. `config_contract.py` replaces its two definitions with ONE top-level line `from hooklib import ConfigUnreadable, read_config_file  # re-export (OF4-10)`; its own uses (`:3031`) keep the bare name. Invariant: `hooklib` never imports `config_contract` at module level (the lazy import at :2737 stays lazy); the T1 row pins `config_contract.ConfigUnreadable is hooklib.ConfigUnreadable` and `config_contract.read_config_file is hooklib.read_config_file`. The `ConfigUnreadable` docstring widens to "cannot be read as one JSON object, or names an unusable `artifact_root`" only if B1's alternative is ever taken; under B1 it stays as is. AR-12 row: "no import added on the hook path; the measured +0.13 s of `config_contract` is avoided (F-1 (b))".

### B4 (t-290). C5 breaks a keep test outside the owns that the witness will not run

`command_card_lines` gains a leading `task_root` parameter (§3.3, C5). But `scripts/tests/test_refusal_registry.py:145` (keep, layer row :4254) calls `brief_pack.command_card_lines("T-1", "walk-1", (), "")`; wave 6 added that call after the designer's snapshot. Its `covers` is `guard_pre_tool.py, refusal_registry.py, stage_guard.py, waiver.py, tests/harness.py`, not `brief_pack.py`. So `scenario_walk --witness-for scripts/brief_pack.py` does not print it, and the break would surface only in the batch canon.

**Fix line (owns + DoD of §7):**
> owns += `C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\test_refusal_registry.py` (only the `command_card_lines` call at :145, given a `task_root` built under a `harness.mark_project` project; nothing else in the file); DoD (5): `python -B <wt>\ai-packages\qa-factory\scripts\tests\test_refusal_registry.py` green, named explicitly because its `covers` does not list brief_pack.py (B4, t-300). Before the build the builder greps `command_card_lines(\|request_lines(\|_rel(` over `scripts/` INCLUDING `tests/` (positive control: `brief_pack.py:3671 def command_card_lines`) and returns any further caller as a question.

### B5 (t-290). The dispatch header points at the wrong tree and at stale line windows

1. The DoD verification command is relative: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/...`. The shell's cwd never moves (CLAUDE.md hygiene 3), so this runs the MAIN checkout's `scenario_walk` against `PACKAGE` derived from its own `__file__`. That checkout is the stale local tree, 196 commits behind. The witness would describe the wrong code. t-289 uses the absolute worktree path correctly.
2. `given` names `runtime_paths.py (:38-188, :715-799)`, but after wave 6 `_admits` is at :752 and `project_for_task` at :774-835.

**Fix line (§7):**
> DoD verification run: `python -B C:\QAFactory\forge-repo\.claude\worktrees\of4-21\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/brief_pack.py ai-packages/qa-factory/scripts/tests/test_brief_pack.py ai-packages/qa-factory/scripts/runtime_paths.py ai-packages/qa-factory/scripts/tests/test_runtime_paths.py ai-packages/qa-factory/scripts/user_path_failures.py ai-packages/qa-factory/scripts/tests/test_flow_requests.py ai-packages/qa-factory/scripts/tests/test_walk_plan_fields.py ai-packages/qa-factory/scripts/tests/test_refusal_registry.py`, then each printed non-quarantined file as `python -B <wt>\ai-packages\qa-factory\scripts\tests\<file>.py`. given: `runtime_paths.py (:38-260, :750-835)` at origin/main ca2f04a (B5, t-300).

### B6 (t-290). The parser sites #4 and #5 inherit the PRINT-side fallback, which inverts the B-231 direction

§3.1 states the error direction of `project_for_task` for PRINTING only: "rejects a valid project → absolute path, longer, still true". Sites #4 (`case_paths`) and #5 (`_excluded_files`) are PARSERS of stored text and get a prefix built from `S("")`.

When `project_for_task` fails, `S("")` is absolute. That happens in the cases E4b names: a markerless folder, a config broken after `build` started, a share it will not probe. Then a stored story-prefixed ref in project-relative spelling (`qa-factory/artifacts/<T>/work/sources/...`, which today's literal matches) no longer matches. `_excluded_files` turns it into `work/qa-factory/...`, misses the excluded file, and `source_material` hands it on.

So the change turns a match into a leak, and in the person's-word direction (B-231, AR-24): an excluded file is handed on. #4 has fallbacks (E13). #5 has none. The same leak applies to a ref written under the default root before the person switched `artifact_root` (the #5 twin of E13, not named).

**Surface:** `brief_pack`'s stored-path parsers. Neighbours walked:
- #4: fallbacks cover it, but still state the edge;
- #5: the leak;
- no other parser in `brief_pack` (§2.1 marks only #4 and #5 as **P**).

Outside the file: `cost_capture:939`, `validate_artifacts:1830/:2631`, `stage_guard:1215` and `check_coverage:249` are the OF4-21b list already.

**Fix line (add an edge E17 to §4 and a row T6b to §5):**
> E17 (B6, t-300): the parser sites #4/#5 do not take the print fallback as their only prefix. `_excluded_files` recognises a story-prefixed `local_ref` when it starts with `S("") + "/"` OR with any `<head>/<task_root.name>/` whose remainder starts with `work/`; the error direction is "skip more" (an excluded file is never handed on; B-231, AR-24). `case_paths` keeps its fallbacks (E13). Row T6b: a markerless story (no `qa-factory/config.json` above it) and a configured-root story whose item has `local_ref: "qa-factory/artifacts/QA-9/work/sources/S1/mr-1.json"` with that file on disk under the story: `source_material` does not list it in either world.

## Key 3 (continued). Non-blocking edges and notes

- **N1 (t-289 §2.6).** Moving :287-290 into the try also moves the `if slug: scan_root = exploration.root(...)` reassignment. A broken config then drops an exploration's own file state too, although the slug branch never needed `artifact_root`. It is harmless today, because `main` exits exploration stops before the fuse. Cleaner: compute `scan_root` from the slug first, and call `artifact_root()` only when there is no slug.
- **N2 (t-289 F-5 (a)).** No code reader of the vcs_evidence stdout `status` exists. I searched the package for `left_out_by_person|not_checked`; the positive control (vcs_evidence's own hits) worked, and no `references/` file names it. The existing unreadable-record row (`test_vcs_evidence.py:131-134`) checks the exit code and stderr only, so F-5 (a) changes no existing expectation there.
- **N3 (t-290 E1).** E1 says `test_story_step_start` stays green, but it is not in the witness unless `--witness-for` prints it. Either name it in the DoD run or drop the claim.
- **N4 (t-290 C3).** `story_text` calls `project_for_task` about 25 times per brief, each with a `nearest_project` walk and an `_admits` config read. The wall-time report covers this; under F-1 (b) of OF4-10, each read stays cheap.
- **N5.** t-290 §6 notes hooklib's own `project / "qa-factory"` home literal (:694, :702). OF4-10 edits that very function but owns no `runtime_paths` import. That is correct for now; the note goes to OF4-21b's list.
- **N6 (environment).** Local `main` has diverged from origin: its journal commits are duplicates with other hashes. The coordinator should reset or rebase local `main` before any further "main" measurement or dispatch that uses relative paths.

## Key 4. Fork decisions

None is wrong.
- **F-1 (b)** is justified by the measurement, which I reproduced on ca2f04a: `config_contract` cumulative 131 ms, `hooklib` 142 ms. It is feasible (Key 2), given B1 and B3.
- **F-5 (a)**: no reader breaks (N2).
- **F-10 (a)** is required for AR-24.
- **t-290 F3 (b)** and **F4 (a)** are sound.
- **F5 (a)** and **F-7 (a)** are correctly routed to the owner.

One coupling for the coordinator: B1 narrows how AR-15's "one exception class" applies. The class family stays `ValueError`, read failures are `ConfigUnreadable`, and key refusals are a literal `ValueError`. That is a fix inside the decision, not a reversal of it.

## Key 5. The two specs together

- **Files owned by both: none.** t-289 owns `hooklib`, `config_contract`, `vcs_evidence`, `exit_gate`, `test_read_json`, `test_vcs_evidence` and a changelog fragment. t-290 owns `brief_pack`, `runtime_paths`, `user_path_failures` and their tests, plus `test_refusal_registry` after B4.
- **Semantic coupling: none that orders them.** `story_text` reaches `artifact_root` only through `_admits`, which catches `Exception`. A broken config's E4 raise in `build` comes from `story_root` → `artifact_root` and stays a `ValueError` under both specs. t-290's C1 (`--output <task root>/work/sources/...`) lands under the configured root, where t-289's branch (1) and the new `_story_at` both recognise it.
- **Order: independent.** They may run in parallel. The later node merges `origin/main`, with textual conflicts expected nowhere. Wave 6 is already merged (PR #11), so t-290's "after wave 6" precondition is met.
- **Follow-on order:** OF4-21b (vcs_evidence :646 and the driver lines) goes after OF4-10, because both edit `vcs_evidence.left_out_by_person`. Put an `очередь: OF4-10 → OF4-21b` line on OF4-21b when it is opened.

## Key 6. Hot files against OH6-1 (`wip/oh6-1` 33b31ee; diff from base 7e1ddab)

- **hooklib**: OH6-1 edits `is_one_component` and `is_story_folder`. t-289 edits `artifact_root` and adds `ConfigUnreadable` and `read_config_file`. Disjoint.
- **exit_gate**: OH6-1 edits `_named_ticket` and adds `import hooklib` at module level after :31. t-289 edits `_identity` :280-299, `awaiting_source_review` and `grounding_errors`. Disjoint.
- **Shared import block**: t-289 adds no top-level import there.
- **Semantics**: OH6-1 makes `is_story_folder` delegate to `is_one_component` (NUL added). The `_story_at` predicate of t-289 is unaffected for valid names, and its error direction stays "no".
- OH6-1 also edits `test-layers.json`, which is a non-goal of both specs. Fine.

## Key 7. Quarantined tests in a DoD

- **t-289**: no violation. `test_exit_gate_grounding.py` is named only as quarantined and not run. The DoD runs `test_judgment_census` (keep), `refusal_registry --check` and `test_detector_verdict` (keep).
- **t-290**: no violation. Quarantined files (`test_project_approach`, `test_exploration_perturbations`, `test_brief_pack_roles`, `test_brief_pack_manual`, `test_walk_brief`) appear only in non-goals and in the handoff's list of expected red pins. §11 keeps `test_project_approach.py` out of the DoD. All DoD-named tests are keep at ca2f04a.

## Standing questions (critic rules 18, 19)

- **DUPLICATION AND CONSISTENCY:**
  - t-289 removes a second config parser (AR-13) and adds no copy, provided F-1 (b) is a move plus a re-export (B3).
  - t-290 adds one survivor and leaves five twins queued to OF4-21b.
  - The one new duplicate is B2's literal.
  - Searched: `read_config_file|ConfigUnreadable` across the package; `command_card_lines(|request_lines(|_rel(` across `scripts/`.
- **CODE QUALITY:** none beyond B1-B6 and N1.
- **ONE ACTION, ONE ROAD (P31):** no exclusion without data. The OF4-10r and OF4-21b residuals are proposed nodes with owners and tests; the coordinator opens them.

## Trail

**Read at ca2f04a:**
- `hooklib.py` :225-300, :640-710, :2730-2742;
- `config_contract.py` :1315-1380, plus a grep of `ConfigUnreadable`;
- `vcs_evidence.py` :575-680;
- `exit_gate.py` :19-39, :60-80, :192-320, :362-400, :754-770, :1505-1620, :1894-2070;
- `refusal_registry.py` :25-60, :884-1010;
- `test_judgment_census.py` :10-40, function index;
- `judgment-census.json` rows :288 and :398;
- `brief_pack.py`: the literal grep, :1120-1160, :1236-1262, :1430-1460, and the c97dd95..ca2f04a diff;
- `runtime_paths.py`: function index, :752-835;
- `harness.py` :257-320;
- `test_brief_pack.py` :60-80, :2781-2802;
- `test_vcs_evidence.py` :125-137, plus a grep;
- `test_first_look_wiring.py` `Project`;
- `test_first_look_briefs.py` (grep);
- `test_refusal_registry.py` :135-152;
- `scenario_walk.py` :833-931;
- `test-layers.json` (keep and quarantine membership, by script);
- `tools/critic_verdict.schema.json`.

**Git:**
- `rev-parse` of local `main` and `origin/main`, `rev-list` counts, `merge-base --is-ancestor` for wave 6 and OH5-2 A/B/C;
- `git diff 7e1ddab wip/oh6-1` on `exit_gate`, `hooklib`, `host_dispatch` and `red_sandbox`;
- `git diff --stat c97dd95 ca2f04a`.

**Greps with positive controls:**
- `read_config_file|ConfigUnreadable` (control: config_contract hits);
- `read_config_file|artifact_root` in design, tools and fixtures (control: census :398);
- `monkeypatch|setattr` × `read_config_file` (empty; the same pipeline found the 21 files above);
- `importlib.reload` (control: `test_project_knowledge`);
- `command_card_lines(|request_lines(` (control: `brief_pack` definitions);
- `left_out_by_person|not_checked` (control: many hits).

**Not done:** I ran no builder tests. That is the mechanical layer and belongs to the builder.

## Reruns

- `python -B -c "...refusal_registry.sites(<read-main pkg>, files=['hooklib.py','config_contract.py'])..."` gave `[('artifact_root', 699), ('artifact_root', 704)]`. `read_config_file` is not a site.
- `python -B -X importtime -c "...import hooklib; import config_contract"` (read-main, ca2f04a) gave `hooklib` cumulative 141868 us and `config_contract` self 85294 us, cumulative 131149 us.
- `git -C …/read-main rev-parse --short HEAD` gave `ca2f04a`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 t-289: switching artifact_root's raises to ConfigUnreadable removes its only u3 refusal sites (refusal_registry.sites sees :699 and :704 only), orphaning census row judgment-census.json:398; DoD 5 cannot pass and deleting the row hides a role-facing refusal",
    "B2 t-289: the new left_out_by_person refusal text names qa-factory/artifacts/<story>/work/ in the branch where the root is unknown, adding a new instance of the literal class OF4-21 removes",
    "B3 t-289: section 2.1 item 1 and the AR-12 row still prescribe F-1 (a); section 12 decides F-1 (b) without stating its shape (verbatim move, top-level re-export line in config_contract, no module-level config_contract import in hooklib, identity pins)",
    "B4 t-290: C5 changes command_card_lines' signature but keep test test_refusal_registry.py:145 (added by wave 6) calls it with the old shape, and its covers do not list brief_pack.py, so the witness never runs it",
    "B5 t-290: the DoD verification command is repo-relative and runs the stale main checkout's scenario_walk; the given windows of runtime_paths.py are stale after wave 6 (project_for_task now :774)",
    "B6 t-290: the parser sites case_paths and _excluded_files inherit story_text's absolute print fallback; when project_for_task fails, a stored project-relative story-prefixed local_ref stops matching and an excluded file is handed on (B-231 direction inverted); edge and test missing"
  ],
  "fixes": [
    "B1: artifact_root's key-value and resolve refusals stay a literal raise ValueError with the finished text; read and parse failures come as ConfigUnreadable from read_config_file; T1 locator token refused = a ValueError whose text names config.json; if C1 still names hooklib.py artifact_root, return the question; deleting row :398 is out of bounds",
    "B2: the refusal text uses the placeholder <artifact root>/<story>/work/ instead of the default folder",
    "B3: append the F-1 (b) shape paragraph to section 12 and strike the F-1 (a) clauses in section 2.1 item 1 and the AR-12 row",
    "B4: owns += tests/test_refusal_registry.py (only the call at :145); DoD names python -B <wt>/.../test_refusal_registry.py; pre-build grep of command_card_lines(, request_lines(, _rel( including tests/",
    "B5: absolute worktree path for scenario_walk with repo-relative --witness-for paths plus test_refusal_registry.py; given windows runtime_paths.py :38-260 and :750-835 at ca2f04a",
    "B6: new edge E17 plus test row T6b: _excluded_files also recognises any <head>/<task name>/work/ prefix (skip more); markerless and switched-root worlds do not list the excluded file"
  ],
  "class_completeness": "t-289: config-read class closed through one reader (F-1 b) with the U rows queued to OF4-10r; the census unit loss (B1) is the uncovered neighbour on the census-recognition surface. t-290: 27 literal sites plus 8 home literals swept in-file (F1 a); the parser sub-class of the same file (#4, #5) lacks its fallback edge (B6); out-of-file twins and parsers queued to OF4-21b; B2 is a new instance of the same class in OF4-10. Axis 8 survivor row queued to the full Lead.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-289-of4-10-artifact-root.md",
      "docs/tasks/specs/t-290-of4-21-brief-pack-paths.md",
      "origin/main ca2f04a: scripts/hooklib.py, config_contract.py, vcs_evidence.py, exit_gate.py, refusal_registry.py, brief_pack.py, runtime_paths.py",
      "origin/main ca2f04a: scripts/tests/test_judgment_census.py, fixtures/judgment-census.json, test-layers.json, harness.py, test_brief_pack.py, test_vcs_evidence.py, test_refusal_registry.py, test_first_look_wiring.py, test_first_look_briefs.py, scenario_walk.py",
      "git diff 7e1ddab..wip/oh6-1 (exit_gate, hooklib, host_dispatch, red_sandbox)",
      "git diff --stat c97dd95..ca2f04a",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B -c refusal_registry.sites(read-main package, files=[hooklib.py, config_contract.py]) filtered to artifact_root/read_config_file", "result": "[('artifact_root', 699), ('artifact_root', 704)]"},
      {"command": "python -B -X importtime -c 'import hooklib; import config_contract' (read-main, ca2f04a)", "result": "hooklib cumulative 141868 us; config_contract self 85294 us, cumulative 131149 us"},
      {"command": "git -C .claude/worktrees/read-main rev-parse --short HEAD", "result": "ca2f04a"}
    ]
  }
}
```
