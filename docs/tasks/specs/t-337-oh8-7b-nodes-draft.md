# t-337: draft carrier for OH8-7b and after (designer draft, saved by the coordinator; NOT accepted — waits for the full Lead)

The designer's handoff write was refused: my dispatch carried no `handoff:` header line. That was a dispatcher defect, and the coordinator saved this file from the designer's reply. The designer's full text is in the session transcript (agent ae788e6ec54d50001).

## 1. Measured pending list (coordinator, 2026-11-13, worktree oh8-7 staged)

The command was run from the oh8-7 worktree root:

```
import test_judgment_census as T
f = T.units_of(R, T.scan_files(R), T.refusal_registry.REGISTRY)
len(f["pending"])
```

with R = `.claude/worktrees/oh8-7/ai-packages/qa-factory`, and both `scripts/` and `scripts/tests` on sys.path.

Output: **190**. Per file:
- probe_by_code 46
- execution_request 14
- exploration 11
- environment_preparation 10
- s7_reorder 8
- import_test_receipt 7
- ticket_light 7
- onboard_apply 6
- question_register 6
- red_sandbox 6
- role_load 6
- s5_plan 6
- assertion_detectors 5
- execution_scheduler 4
- hooklib 4
- vcs_evidence 4
- grammar 3
- machine_facts 3
- manual_evidence 3
- question_stop 3
- run_suite 3
- event_store 2
- local_keys 2
- manual_capture 2
- person_words 2
- release_fingerprint 2
- selftest 2
- source_exclusions 2
- source_inventory 2
- config_view 1
- controller 1
- driver_dispatch 1
- explore_step 1
- host_adapter 1
- managed_dependency 1
- retro_numbers 1
- story_step 1
- ticket_adapter 1

The designer's four uncertain names, checked against the measurement:

| Name | In the pending list? |
|---|---|
| controller::refresh_derived | yes |
| controller::_is_replay | no |
| run_suite::main | yes |
| story_step::start | yes |

The designer's hand count (191) was wrong in places: machine_facts was 4, measured 3. The measured list is authoritative.

## 2. Provisional grouping (designer; drops to be recomputed from the measured list)

| Node | Files | Approximate drop |
|---|---|---|
| OH8-7b | probe_by_code, first half (parse_node..run_shape_checks) | 20 |
| OH8-7c | probe_by_code, second half (manifest_entry..main) | 26 |
| OH8-7d | execution_request, environment_preparation, execution_scheduler, managed_dependency, run_suite | 32 |
| OH8-7e | exploration, explore_step, import_test_receipt, red_sandbox, s7_reorder | 33 |
| OH8-7f | ticket_light, source_inventory, ticket_adapter, vcs_evidence, source_exclusions, local_keys, onboard_apply, config_view, role_load, release_fingerprint, selftest | 35 |
| OH8-7g | s5_plan, question_register, question_stop, person_words, grammar, assertion_detectors, manifest_from_tests(?), machine_facts, manual_evidence, manual_capture, project_decisions(?), driver_dispatch | ~35 |
| OH8-7h | hot files, function-disjoint owns: hooklib (4), controller::refresh_derived, story_step::start; plus event_store, baseline_contract(?), retro_numbers, host_adapter | ~11 |

Notes on the grouping:
- Every node writes judgment-census.json, so the nodes run one after another.
- The test for each node: SUBCLASS_PENDING_CEILING drops by exactly the node's measured count, and C7 stays dense.
- Each node's edges are listed in the designer's reply:
  - a function that turns out not to refuse gets no row;
  - a subclass outside the scan was never pending;
  - a hot file needs a queue line or function-disjoint owns;
  - a new pending function from another merge is red for its author.
- "(?)" marks a file that is in the designer's list but not in the measured per-file counts. Those files are manifest_from_tests, project_decisions and baseline_contract; the designer listed 1 function in each, and none of the three appears in the measured list.

## 3. Batch section: not drafted
The untaken onboarding-hooks batch has not been identified. Batches 4-8 are all taken by dev1. `piles.py take` of a new batch is blocked by the broad zones of onboarding-forge/1,2 (coordinator finding, morning list).

## 4. Forks: QUEUED FOR THE FULL LEAD

**F1 (blocking, mechanism).** Under (c1) a subclass raise never creates a census unit, so a "row for a pending function" has no unit to attach to. No road from (c1) to the end state (a) is written. The options:
- **(a)** A grow-only test constant `SUBCLASS_UNIT_FILES`. Widened sites in a listed file create units. Each node adds its files and rows and lowers the ceiling. The last node deletes both constants.
- **(b)** Data-only pending rows with no class: a second road.
- **(c)** Rename the functions onto unit names: churn.

The designer recommends (a). This changes the census mechanism (AR-20, AR-29), so the coordinator (Opus, degraded window) does not decide it.

**F3.** Node size: ~20-40 functions (recommended).

**F4.** One critic pass per node, reading every new row (critic q11).

The OH8-7b chain is blocked on two things: the full Lead's commit of OH8-7 itself (the `tier:` gate), and F1.
