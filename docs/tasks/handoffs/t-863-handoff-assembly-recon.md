# t-863 digest v1 — who assembles the handoff forms (scout, read-only; extracted by Lead, condensed)

Method: no run transcript read; "H" (the role copies by hand data that code holds) is INFERRED from contract text and
the code that fills fields, not measured. Lead spot-check (14.11 13:31): s8.md:223-224 stale `--from` call — confirmed;
handoff_check.py DERIVERS :643 / LIST_DERIVERS :638 / `_code_fills` :2814 — confirmed; BACKLOG has 0 lines on
`values_skeleton|prefill` (control `handoff_check` → 8) — confirmed.

## Facts
- Form is written BEFORE the role starts: `story_step start` → `_write_dispatch_files` → `handoff_init.py`
  (story_step.py:1168-1208). It fills only header (role/stage/window/dispatch/ticket), inlines allowed-word lists, a
  `# Fill:` line; the only row prefill is S3 rework `scope[].id` (handoff_init.py:358-380).
- `repair_carries` (index.yaml:79-95) carries values only on rework for 4 contracts (S2, S3, S4 designer→critic, S8 scribe).
- At finish `handoff_check.py --fix` writes values derived from disk: 22 DERIVERS, 2(+1) list derivers, 5 grounding
  keys, 4 BY_PATH rows, 14 verified claims (:638-686, :1028-1047); a role is not refused for leaving those blank (:2814).
- AR-22 count: 738 required handoff fields, 28 tool-made (architecture.md:237; field-producers.json says 27).
- The form file carries no required/optional marks (handoff.py infers optional from placeholder words :34-36, :422-447);
  the generated slice `references/slices/<role>/handoff-keys.md` does mark them, and it reaches the role in the start
  prompt via inject-map.json — that is the "copy in the prompt". The role also gets the form path in its brief.
- S8 bug-reporter: `start` writes its form before the work (inferred); s8.md:223-224 still tells it to run
  `handoff_init.py --from` after filing — stale second writer, wrong flag (`--role`).
- Prior art: finding plans/piles/driver-hosts/findings/20261031-zapis-znachenij-formy-vse-ili-nichego.md — rule recorded
  before measuring: if ≥ half of refusals are "not filled", handoff_init writes a `values.yaml` skeleton;
  `values_skeleton` exists only in refusal text (handoff_check.py:2848, 2911). t-631 spec introduced `prefill_rows`.

## Hand-copied data (H, inferred) — what code already holds, the role retypes
- Ids from plan/triage/gate decision: S3 scope ids (first dispatch), S4 ids/obligations/disposition/review_scope.cases,
  S5 plan scope ids, S6/S7 row ids, S8 scope ids.
- Counts/sizes: S1 diff.bytes; S2 inputs_read.handed; S3 budget.*; S4 rows/manual_rows; S6 handed counts; S7 counts.*.
- Rows from manifest / run-report / triage: S5→runner selector/profile/freshness; S6 scope rows, env_blocked, surprises;
  S7 repairs/bug_drafts data fields.
- Probe/run records: S5 critic probes.records; S6 probe_before/after; S7 verify.request/result.
- Verbatim quotes of case Then lines: S4→runner, S6 manual_observations, S7 then_lines_before.
- From bug files / ledger: S8 filed[] data fields, reasons_by_owner; S9 numbers.* (retro-numbers.json), delivery bookkeeping.
- Judgment (stays with the role everywhere): verdict, scope[].state/reason, tried, unresolved, findings, repairs'
  problem/fix, stage_acceptance, regression recommendations, etc.

## Per-stage tables (scout's, verbatim in substance)
Legend: start = handoff_init at story_step start; check = handoff_check --fix at finish; const = literal in the contract;
H = data code holds that the role types by hand (inferred). Common to all forms: header.role/stage/window/dispatch/TICKET
and vocab lists filled at start; `artifacts.*` const; `inputs_read[].version` derived at check. Judgment everywhere:
header.verdict, scope[].state/reason, tried[], unresolved[], blocked.*, non-verified claims.

| contract | code fills today | role copies by hand (H) | judgment (role) |
|---|---|---|---|
| S0 setup→scout | task, repositories, environment, tools, obligations "filled by code" per contract comment (code not read) | — | — |
| S1 scout→tester | implementation.source, diff.files/hunks/production_files, scope[].material_collected (check); claim implementation_source (verifier) | implementation.reference, diff.path, diff.bytes; scope[] id/relation/relevance/revision/read/attachments_inspected; person.review_recorded/words/accepted_gaps/late_sources | ac_code_conflict.* |
| S2 tester→strategist | size.computed (check); size.reasoning_ref (sizing.py path); size_* claims | inputs_read[].handed (S1 hunks; repair carry only) | inputs_read.read; scope[] register rows (typed in both register and form); contradiction_matrix, open_questions, size.override |
| S3 strategist→designer | grounding.* (5), blast_radius[] (check); scope[].id on rework (start) | budget.size/cap/planned_rows/within_cap (repair carry only); scope[].id first dispatch (test-plan.json P-n); inputs_read requirements/candidates counts | scope[] state/reason/requirements/obligations/behaviour/risk/oracle/level/coverage/environment/flags; budget.if_over; manual_policy; not_planned; regression_recommendations |
| S4 designer→critic | scope[].case_version, requirements, plan_row (check, BY_PATH) | scope[].id/obligations/disposition/design_review_required; review_scope.cases, rounds_used; inputs_read.rows (partly); artifacts.cases_root | origin/reuse_of/self_probe; review_scope.focus |
| S4 critic→designer | review.rollcall, findings_file, scope[].case_version (check); inputs_read[0] author row (start) | scope[].id | review.outcome/rounds/rubric, findings, unverified, stage_acceptance, not_looked, advice, questions, register_gaps |
| S4 designer→runner | scope[].requirements, plan_row, case_version (check) | scope[].id/obligations/executed_by; inputs_read.manual_rows; execution[].then (verbatim case quote) | execution[] steps_ref/evidence/preconditions/data/inconclusive_when/not_executable_when |
| S5 plan pair | artifacts.plan const; plan stamp at finish | scope[].id | review.outcome, remarks[], scope[].state |
| S5 automator→critic | runtime_provenance/tests/run_witness/probes, scope[].case_version (check); 2 claims | scope[].id/origin/obligations | plan_remarks, deviations, for_the_reviewer |
| S5 critic→automator | review.findings_file, receipt_ref, probes.runtime_provenance (check) | probes.records[] (instance/verdict/record); scope[].id | findings, tooling_findings, unverified, not_looked, outcome |
| S5 automator→runner | runtime.provenance, tests, run_witness, case_version (check); fingerprint claim | scope[] id/case/obligations/selector/profile/last_receipt/freshness/stale_because; runtime.environment/build/probe_command; not_in_scope; handed_profiles | — |
| S6 runner→analyst | run.execution_status/totals/window_totals/witness (check) | run.environment/build/probe_before/after; scope[] id/case/obligations/executed/rerun_reason/evidence/duration (run-report.json); manual_observations.before_change, surprises ("as built by code"); env_blocked, superseded; counts; manual then quote | manual observed/result/why_inconclusive |
| S7 analyst→automator | not_for_repair rows, null outcome only (handoff_check.py:1550-1559) | scope[] id/case/round; repairs[] id/verdict/evidence/then_lines/rerun_series (triage.json) | repairs[] problem/expected/fix/check/mechanism/kind; stage_acceptance; where_it_went |
| S7 automator→analyst | rounds[].verify.witness (check) | verify.request/result; then_lines_before; scope id/round; repairs_answered | changed, then_lines_after, fix_result, cause |
| S7 analyst→scribe | bug_drafts confirmation step derived (role writes constant `unconfirmed`); claim no_bug_without_draft | scope[] id/state/case/requirement/evidence/repaired; counts.* (7); bug_drafts ref/path/triage_ref/requirement/damage/manual_steps; env_issues/not_verified/case_defects partly | reproduction, duplicate_of, stage_acceptance, tried |
| S8 scribe→gate B | delivery.ready, blocked_by (check); message_sections, not_shown const | delivery.reasons_by_owner; rehearsal.ran/factory_fixable_open (ledger); drafts_received/rows partly | rehearsal.person_decides/factory_defect; questions; stage_acceptance |
| S8 bug-reporter→scribe | — | scope[].id (gate B decision); filed[] draft/bug/action/cases/requirements/source_draft/proposal; inputs_read version/drafts_chosen; quarantined[].debt_file | not_filed.why, no_case_reason, quarantined.trigger, tried |
| S9 retro→project | — | numbers.* (4, retro-numbers.json: "no model does this arithmetic"), retro_mode, delivery_bookkeeping.* | knowledge_fold, factory_backlog, feedback.answer, scope rows |
| Gate A / Gate B | person decisions recorded by controller gate-decision (first lines read only) | — | person |

Analog: S2 `inputs_read[].handed` names the S1 hunks but only a repair carry brings the value — same class as H.
Appendix A of K10 spec r2 (:474-483) "K3 handoff form by path": savings 3,686 B automator, 3,182 B code-critic,
5,576 B strategist; conditions S5 (S8 start writes the form) and S6 (no required/optional marks in the form).

## Forks (for a tier above)
- Where code writes more: at start (handoff_init) or at finish (`--fix` derivers).
- Whether the role's file stays a form it fills, or one code completes first and the role adds judgment only.

## Not done
Code filling S0 not read; gate A/B forms partly; handoff_help.py, exit_gate.py beyond grep hits; no transcripts.
Full digest with per-stage tables and 30-row trail: the scout's hand-back in session 9408e840 (t-863).
