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

## Forks (for a tier above)
- Where code writes more: at start (handoff_init) or at finish (`--fix` derivers).
- Whether the role's file stays a form it fills, or one code completes first and the role adds judgment only.

## Not done
Code filling S0 not read; gate A/B forms partly; handoff_help.py, exit_gate.py beyond grep hits; no transcripts.
Full digest with per-stage tables and 30-row trail: the scout's hand-back in session 9408e840 (t-863).
