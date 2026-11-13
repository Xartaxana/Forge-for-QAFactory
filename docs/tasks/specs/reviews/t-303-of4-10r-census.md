# t-303: scout census of `artifact_root(` entry points for the residual node OF4-10r

This is the digest of scout t-303, condensed by the coordinator. The scout read origin/main at ca2f04a through the worktree `read-main`.

The coordinator spot-checked two claims:
- `worker_lifecycle.py` has 0 hits for `artifact_root` (case-insensitive), against 9 hits for `artifact`, which is the positive control;
- `exit_gate.py:287` calls `art_root = artifact_root()` outside any try;
- in addition, `config_contract.py:1321 class ConfigUnreadable(ValueError)` was confirmed.

The predecessor scout t-302 read a stale checkout and was rejected.

## Count

The exact token `artifact_root(` gives **118 lines** outside tests/:
- 106 standalone: 5 non-calls (hooklib:359 docstring, hooklib:691 def, vcs_evidence:584, controller:2481, red_sandbox:126) and 101 calls;
- 12 alias: execution_request imports `artifact_root as _artifact_root` (:3217) and makes 10 calls; collect_pack has a method call at :489 and the def at :494.

The §8 line numbers of t-289 are stale against main (guard_pre_tool 2269 -> 2277, 1395 -> 1403, 1535 -> 1543; runtime_paths 731 -> 766). Every site §8 names exists.

## Hook paths: uncaught tracebacks (priority)

| site | path | catch |
|---|---|---|
| `exit_gate.py:287` `_identity` | `exit_gate.main:1922` and `subagent_journal.main:207`; only when the event has no input_fingerprint | none: traceback, exit 1 (in OF4-10 scope, F-4 (a)) |
| `exit_gate.py:759` `_ticket_for_stage` | `main:1994` via `awaiting_source_review:1519` (stage S1, unknown-task) | none on that path (in OF4-10 scope, F-4 (a)) |
| `host_dispatch.py:286`/`:311` `record` (Codex hook per hooks/codex.json, file not opened) | `resolve_ticket` / `artifacts_dir` | none: traceback |

## Hook paths: fail-open or silent

- `guard_pre_tool`:
  - :2277 `_stand_record_matcher`: caught by `stand_record_write_check` at :2333-2334, passes silently. The "no try" in §8 is wrong.
  - :609 and :1403: return False silently.
  - :738: returns "not exempt" silently.
  - :1543: writes `_window_note`, then returns [].
- `guard_app_under_test:264` (reached via guard_pre_tool): `except Exception: return False`. This keeps the boundary closed, the refuse direction.
- `stage_guard`:
  - :463, :600, :1375, :1570 and :1834: `check()` at :1240-1245 returns ALLOW (DENY if LAST_DENIAL is set) and sends the person_signal `guard_crashed`.
  - :1692: returns ALLOW silently, with no signal.
  - :1421 and :1668: caught silently, and the refusal still goes out.
- `inject_context:325`/`:330` `note_denial`: `except Exception: pass` drops the denial record. main :552 ALLOWs and sends an inject signal.
- `gate_shown:186`, `agent_autobind:98` and `conductor_stop:46` (both via `host_dispatch:23` `controller_record`), and the exit_gate sites reached through `all_errors`: exit 0 with the `gate_unreadable` signal.
  - §8 note (d) is refuted: `enrich` never calls artifact_root.
- `cost_capture` via `dashboard_refresh:30`:
  - its own `json.loads` at :29 raises first;
  - the cost_capture `__main__` at :3824 writes stderr and exits 0, with no signal;
  - other callers: project_decisions:364 (caught), run_suite:910 (pass), bug_snapshot:38 (none).
- `validate_artifacts:356`: blocks on the hook path (main :2771-2777). The `--check` CLI at :2737 has no catch.
- `dispatch_liveness:771`, a library function reached from conductor_stop: its callers :938 and :1040 catch `(OSError, ValueError, AttributeError)` and give None / UNKNOWN.

## Non-hook

- **No catch:**
  - `run_suite:3037`: catches only MineRefusal.
  - `execution_request`: 10 alias calls.
  - `red_sandbox:1412`.
  - `vcs_evidence:628`: catches OSError only. It is in OF4-10 scope.
  - `stage_guard:2996`: the `--stories` CLI.
  - `execution_scheduler:156`: a library; its callers are not traced.
  - `execution_scheduler:359`/`:577`: writers that raise on purpose (F12); main :685 has no run_guarded.
- **Tuple catch** naming `(OSError, ValueError[, AttributeError])`. `ConfigUnreadable` must stay a ValueError subclass, or these are bypassed.
  - Silent fall back to the default folder: `hooklib:398`, `env_probe:694`, `role_load:539`, `local_keys:132`.
  - Refusal: `waiver:1171`.
  - Silent: `vcs_evidence:598`.
- **Catch-all:**
  - `collect_pack:501`: records gap B and falls back.
  - `controller:2491`: silent.
  - `red_sandbox:133`: silent default.
  - `local_keys:70`: silent False.
- **Unverified (32 lines; only the line text was read):**
  - archive_task 146, 194, 235;
  - audit_factory 454, 528, 586, 1502, 1514;
  - check_coverage 97;
  - factory_dashboard 400, 475, 493, 675, 1029, 1245, 3061, 3915;
  - estimate_record 44;
  - probe_by_code 4750, 6959, 7799;
  - planning_contract 362;
  - runtime_paths 766;
  - source_exclusions 540;
  - stand_identity 178, 210;
  - traceability 1842;
  - window_budget 301;
  - baseline_contract 66;
  - driver_journal 346.
- `run_guarded` (role_cli.py:134): none of the 19 files that use it holds a direct site. `hooklib:282` `artifacts_dir` and `:378` `story_root` are reached from run_guarded CLIs.

## Out of scope, noted

`hooklib.artifacts_dir(` has many more call sites, including hooks:
- guard_pre_tool:1170, :1474, :1484;
- inject_context:495, :641;
- stage_guard:1286, :1296, :1845;
- guard_app_under_test:65;
- host_dispatch:311.

They raise the same way via :282 and are not in this census.

## Proposed cut (facts; the coordinator decides)

1. Hook files: `exit_gate.py` (OF4-10 covers :287/:759), `host_dispatch.py` record (Codex), `stage_guard.py`, `guard_pre_tool.py`, `inject_context.py`, `gate_shown.py`, `dashboard_refresh.py` + `cost_capture.py`.
2. Non-hook CLIs without a catch: one wrap per CLI, or `role_cli.run_guarded`.
3. Catch-alls and tuple catches: decide per site whether the silent default is acceptable (FR-59: an unknown is not a pass).
4. The 32 unverified lines need a second scout pass before the builder nodes are cut. This was done by t-312; see below.

## Second pass: scout t-312 (2026-11-13, read-main at origin/main 58b3667)

The heading's "32" is a miscount: the list names **30** lines, and all 30 are classified. No line has drifted. The coordinator spot-checked two rows: window_budget:301 (S, falls back to `base/"artifacts"`) and stand_identity:191-192 (S, `return {}`).

| class | sites |
|---|---|
| T: traceback on a CLI | archive_task 146, 194, 235; audit_factory 454, 528, 586, 1502, 1514 (`main` runs a1..a24 with no try); check_coverage 97; factory_dashboard 400, 475, 493, 675, 1029, 3915 (direct CLI); probe_by_code 4750 (catches MineRefusal only; `story_root` at :8339 may refuse first; not settled); source_exclusions 540 (`--revoke`; contradicts the intent pinned at test_config_projection.py:410-427); traceability 1842 |
| S: silent default | factory_dashboard 1245 (no bugs); factory_dashboard 3915 on the **cost_capture hook** route (dashboard_refresh re-raises; cost_capture `__main__` prints "COST CAPTURE INCOMPLETE", exit 0, no signal); stand_identity 178 (`{}`), 210 (`""`); window_budget 301 (**hook** precompact_guard; falls back to `<root>/artifacts`); driver_journal 346 (`[]`) |
| P: unknown passed on | factory_dashboard 3061 ("not available"); probe_by_code 6959 (`""` read as a role, the refusal side); planning_contract 362 (five detectors give UNREADABLE exit 3, run by exit_gate); runtime_paths 766 (the reason ends in `project_for_task`'s ValueError with a door); baseline_contract 66 (an error string in the list) |
| R: refusal | probe_by_code 7799 (door JUDGE_DOOR); estimate_record 44 (JSON `invalid_estimate`, exit 2, no door) |

Not traced (one hop only): the callers of `collect_cases`, `project_for_task` and `execution_request:123`; `gate_brief:3787` into gate_shown; how exit_gate reads exit 3.

Forks for the node's Lead:
1. Which S and P sites stay as they are (FR-59).
2. Whether the CLI tracebacks are wrapped one by one or through `role_cli.run_guarded`.
