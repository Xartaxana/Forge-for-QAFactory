# t-936 -- Architect stream C (session_context.py)

DoD: `python -m pytest tools/test_session_context.py -q -p no:cacheprovider`

## Output
```
........................................................................ [ 23%]
........................................................................ [ 47%]
........................................................................ [ 70%]
........................................................................ [ 94%]
.................                                                        [100%]
305 passed in 49.65s
```
(An earlier run of the same command failed once on `test_main_stdout_deadline_timeout_exits_immediately_via_subprocess`, a wall-clock test: 13.1s vs < 10s. The same test also failed when run against the untouched main checkout's file, 12.6s, so it is load/machine-dependent and not caused by this diff; the final run above is green.)

Changes are STAGED (`tools/session_context.py`, `tools/test_session_context.py`), no commit.

## Item -> change -> test rows
| item | what changed | test row ids |
|---|---|---|
| C1 | `model_line(stdin_payload, config_text=None)` now `MODEL: <id> -> function <f>[ (<note>)] (declared by harness, not measured; lead = <L>, architect = <A or unbound>)` from `tier_ladder.function_of_session`; `above lead (no architect binding)`, `below builder`, `function none (matches no binding in delegation.config.yaml) -- coordinate under the below-lead rules until verified`, `(config unreadable: default bindings)`; `_MODEL_TIER_SUBSTRINGS` and `model_tier` deleted; `tier_ladder` imported fail-open; config read once from `<root>/delegation.config.yaml` (64 KB cap) | `test_model_line_function_by_ladder[exact-lead, exact-architect, exact-builder, family-match-live-case, above-lead-no-architect-key, unbound-family-weaker, unrecognised-model, config-unreadable, config-absent]`; old tier tests replaced; not-provided/whitespace/sanitize rows kept |
| C2 | `architect_line()`: `ARCHITECT SESSION: start with PROCESS/ARCHITECT_START.md; queue docs/tasks/architect-queue.md (<N> open \| queue file absent \| queue unreadable: <reason>)`, printed only when function = architect and note is not `no architect binding`; counts `- [ ]` lines; inserted right after MODEL | `test_architect_line_in_context[architect-family-queue-3-open, architect-exact-queue-0-open, architect-queue-absent, architect-queue-unreadable (queue path is a directory), lead-session-no-line, builder-session-no-line, fable-no-architect-key-no-line, unrecognised-model-no-line]`; `test_architect_and_pin_lines_survive_the_25_line_cut` (30 filler candidates) |
| C3 | `settings_pin_lines()`: WARN on exact-string difference vs lead binding; absent / no `model` / non-string model / config unreadable -> none; unparsable or non-object -> `WARN: .claude/settings.json unreadable (<reason>)`; placed after the ARCHITECT slot | `test_settings_pin_line_in_context[equal-no-line, differ-warn, settings-without-model, settings-absent, settings-unparsable, model-not-a-string, config-unreadable-no-pin-line]`; cut test above |
| C4 | `last_calibration_line(events, now, function=None)`; suffix when displayed `days` > 7 or NONE; architect -> `run the calibration (PROCESS/ARCHITECT_START.md step 6)`, otherwise Lead suffix; unparsable ts -> none; `build_context_lines` passes the session function | `test_last_calibration_overdue_suffix[none-lead, none-architect, 8-days-lead, 8-days-no-function, 8-days-architect, exactly-7-days, unparsable-ts]`; `test_build_context_lines_calibration_suffix_follows_session_function` |

Both worlds for the stream-F files: queue absent (tested, `(queue file absent)`) and present (tested, counts); the pointer to `PROCESS/ARCHITECT_START.md` is printed without reading or checking the file.

## Deviations
1. The Lead overdue suffix. Spec 4.6 gives the Russian phrase `«лучше позвать Архитектора»`. This hook's output is ASCII-only by pinned tests (`test_build_context_lines_malicious_stdin_payload_stays_ascii_single_line`, `test_main_with_a_cyrillic_import_on_a_cp1252_stdout_keeps_the_whole_context`; a stdout write error discards the whole context). I first emitted the Cyrillic and both tests went red, so the suffix is now ASCII English `"better call the Architect"` (constant `_CALL_ARCHITECT`). See question 1.
2. `above lead (no architect binding)` is rendered as `function above lead (no architect binding)` (keeps the `function <f>` frame of 5.4).
3. The `function none` line carries no `declared by harness` / `lead =` suffix (spec text taken verbatim).
4. `function_of_session` returns `architect` for the above-lead case; the ARCHITECT line is suppressed on its note (`no architect binding`), as 4.4 requires.
5. "Overdue" = displayed whole days > 7 (so 7 days 12 h is not overdue).

## Questions
1. Lead suffix wording: ASCII English (now), a transliteration, or lift the ASCII invariant for this one phrase (needs the two pinned tests changed and a stdout-encoding decision)? Spec 4.6 text and the module invariant conflict.
2. Unreadable settings reasons / unreadable queue reasons are `ExceptionName: message` truncated to 100 chars; acceptable?

## Needed beyond the manifest
`C:/QAFactory/forge-repo/delegation.config.yaml`, `.claude/settings.json` (to learn live values), the existing ASCII/cp1252 tests in `tools/test_session_context.py`.

## Siblings noticed
`tools/test_session_context.py` header comment mentions staged draft `session_context_b402`; untouched. Same ASCII-only hazard applies to any later Cyrillic line added to this hook.

## Fix round (critic t-946)

1. cap re-derived at session_context.py `_read_capped` (~:1028) -> now `cap=None` reads `_tl.MAX_CONFIG_BYTES` (one home, AR-13); with tier_ladder unimportable it returns `(None, "tier_ladder unavailable")` (nothing reads the config then; model_line returns before using it). Absent/oversize/unreadable behaviour unchanged. Sibling grep: the only other 64 KB hit is the message string "over 64 KB" (:1041, text, kept; matches tier_ladder's own wording). No other literal 65536.
2. Two MODEL table rows, test_session_context.py `_MODEL_ROWS`: `today-config-family-match-lead` (claude-fable-5-2 vs lead=claude-fable-5-1, no architect -> `function lead (family match: claude-fable-5-1) ... architect = unbound`; wording from spec 5.4 form `<f> (family match: <binding>)` line 538, not from code output) and `between-families-unbound` (opus vs lead fable + builder haiku -> `builder (unbound family)`, spec :543). Both passed immediately (pins of existing behaviour).
3. `last_calibration_line(..., architect_bound=True)`; build_context_lines passes `_tl.architect_binding(config_text) is not None` (True if tier_ladder missing). Unbound -> " -- overdue: run the calibration (no architect is bound; calibration and mechanism review)". Bound: suffixes unchanged. Test: `test_calibration_suffix_without_architect_binding_never_sends_to_an_architect` (2 params: lead + fable sessions).
   red-before: both params FAILED, got `... -- overdue: run the calibration (PROCESS/ARCHITECT_START.md step 6)` for fable (and the Architect suffix for lead) vs expected unbound suffix.
4. Numstat (`git diff --cached --numstat`, total staged vs main): session_context.py 147+/42-, test_session_context.py 183+/46-. This round alone: product 12+/5-, tests 20+/0-. Total test lines still exceed product lines: proposed `tests-over: stream C covers 4 behaviours (ladder line, pin, architect line, suffix) as table rows over a file that had no ladder rows`.

DoD output: `python -m pytest tools/test_session_context.py -q` -> `1 failed, 308 passed in 124.69s` (run before the last small edit, the tier_ladder-None guard); the narrow rerun after it: `1 failed, 13 passed, 295 deselected` (calibration/new rows green). The one failure `test_main_stdout_deadline_timeout_exits_immediately_via_subprocess` is a 15 s subprocess timeout: measured `python -B tools/session_context.py` takes 16.4 s in W and 17.4 s on the unmodified main checkout (`time` output) -> pre-existing slowness of this machine, not this change. Staged (git add of the two files), not committed. Handoff file itself left untracked.
