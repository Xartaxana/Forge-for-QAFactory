# t-323: scout digest for OH8-2 (NTFS alias names) and OH8-6 (json.loads outside SCANNED, stale SCOPE)

Scout (Sonnet) read `.claude/worktrees/read-main` at origin/main 303e89e. Condensed by the coordinator.

Coordinator spot-check (R1b), 2026-11-13:
- load-bearing: `host_dispatch.py:243`, `:271`, `:313` read `json.loads(...read_text())` with no try around them. Confirmed by reading the lines.
- negative: `role_load.py`, `role_digest.py` and `guard_app_under_test.py` have 0 `json.loads` hits. Confirmed with a case-insensitive grep; the positive control was `host_dispatch.py`, 6 hits.

Coverage is PARTIAL (the scout says so): most enclosing functions were not read, joins via `os.path.join` or f-strings were not searched, and several hook-wired modules were not checked for `json.loads` (see "Not done").

## Rule facts (hooklib.py:262-332)
- `is_one_component` (:269) rejects only empty, `.`, `..`, and names containing `/ \ : NUL`. It passes `T.`, `T `, `...` and other letter cases.
- `is_story_folder` (:305) also requires no blank at either end and the EXACT name in `os.listdir` of the parent, then `is_dir`. It refuses `T `, `T.`, `...` and `t` unless a folder with that exact name exists.
- `artifacts_dir` (:275-282) uses only `is_one_component`. On NTFS, `T.`, `T ` and `t` resolve to story T's folder.

## OH8-2: sites by class

**Guarded by `is_story_folder` (alias refused):**
- bug_records.py:1398;
- execution_request.py:3246, :3258, which gate the joins at 3252-3267;
- exit_gate.py:166, 817, 1126, 1254, 1500;
- inject_context.py:325;
- local_keys.py:71;
- waiver.py:1165;
- vcs_evidence.py:595;
- hooklib.py:388, :430.

**`is_one_component` only (alias RESOLVES to another story):**
- stage_guard.py:436, 463, 620, 642, 715: `(root / x / "pipeline.json").is_file()`.
- controller.py:2489-2497: `task in names` and then `os.path.samefile`. This is the "known place" in the finding.
- host_dispatch.py:21-23, which reads controller.json, and :310-313 (`artifacts_dir`).
- estimate_record.py:43-45.
- role_load.py:542; :555 is harmless.
- subagent_journal.py:107, role_digest.py:324, exploration.py:134, 537, 734: the joins were not read.
- exit_gate.py:209 is a file name, likely harmless.

**Not a story key, same filter:** the session-id sites are activity_capture.py:45, cost_capture.py:1908, :3801 and recover_codex_usage.py:17. red_sandbox.py:330 and :334 check pin keys. If `is_one_component` itself changes, these follow it.

**No helper in the hit line (callers not read):**
- archive_task.py:194, :235;
- audit_factory.py:528;
- env_probe.py:745;
- traceability.py:1839;
- execution_request.py:883;
- manual_capture.py:343-373, :3137;
- exit_gate.py 125-127, 289, 678, 904, 1064, 1110, 1281, 1367, 1406, 1432, 1513, 1525, 1564, 1667. Some of these may sit behind an earlier gate in the same function.

**`artifacts_dir()` callers with a story key:** guard_pre_tool.py:1170, 1474, 1484; stage_guard.py:2692; worker_lifecycle.py:94, 210.

## OH8-6
- `SCANNED` (refusal_registry.py:56-57) has 6 names: stage_guard, inject_context, guard_pre_tool, native_context, codex_roles, host_adapter. The SCOPE docstring (:33-35) lists only the first 4. It is stale: codex_roles.py and host_adapter.py are missing.
- Unguarded `json.loads` outside SCANNED:
  - host_dispatch.py:243, the binding receipt;
  - host_dispatch.py:271, every receipt in `qa-factory/state/host-dispatches/*.json`;
  - host_dispatch.py:313, the story's controller.json.

  All three are in `record`, outside any try. A broken file raises a bare JSONDecodeError with no file name and no door.
- Guarded or quiet:
  - worker_lifecycle.py:38 and :94;
  - exit_gate.py:350 and :391 (the gate's own state);
  - host_dispatch.py:257 (try/except ValueError).
- Not checked for `json.loads`: cost_capture, validate_artifacts, host_probe, conductor_stop, gate_shown, precompact_guard, session_env, postcompact_reload and telemetry_hook. The handlers at dispatch_liveness.py (9 sites), exit_gate.py:958 and worker_lifecycle.py:210 were not read.

## Not done (scout)
Enclosing functions were not read for most sites. Joins via `os.path.join`, f-strings or other variable names were not searched. There was no NTFS run: the alias verdicts come from reading hooklib.
