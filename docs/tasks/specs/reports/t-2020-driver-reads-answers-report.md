# t-2020 report: the driver reads a script's answer by one reader

Branch dfix in wt-fb6. Architecture: AR-13 (one reader), AR-18 (one output shape, one reader), AR-28 (an unknown is never a pass). FR-41.

## What changed (story_run.py)
- New `_read_answer(out)` (module level, beside `_read_jsonl`): last line of stdout+stderr that parses as a JSON object, else `None`. Mapped in `fixtures/driver-layers.json` (home driver_core).
- `Driver.controller`: no JSON line -> `Refusal` naming the operation and the first 300 characters that came back. `{"raw": ...}` is gone from this road.
- `Driver.stage_S6`: an answer of `stage-scope` without a `scope` list (either half) -> `Refusal`; "nothing to execute" is reachable only over a scope the controller said was empty.
- `gate_answer_told`: its private copy of the same loop replaced by `_read_answer` (same behaviour).

## Sites (all `splitlines()[-1]` / last-line reads of story_run.py, story_step.py, walk_session.py)
story_run.py:
1. controller() (was :1511) - APPLIED: `_read_answer`; Refusal when none.
2. handover form note (~2413 `(out).splitlines()[-1][:200]`) - not applicable: shows the last line of a failing script as text; it reads no answer. (The `json.loads(out)` just above it reads the WHOLE output - see analogs.)
3. environment_selection (was :9067) - APPLIED: `_read_answer(out) or {"status": "unknown", "raw": out}`. A deliberate named `raw`: status `unknown` is handled as an unknown by the S0 branches below, never a pass.
4. walk_session open (:3404, `(text.splitlines() or ["{}"])[-1]`) - APPLIED: `_read_answer(text) or {}`; exit 0 only, and the result is a hint sentence (signed in / landed on), not a gate.
5. S6 "nothing to execute" finalize_task exit text (~11988) - not applicable: display of a failing script's last line in a Refusal.
6. S6 freshness finalize_task print (~12025) - not applicable: display.
7. s6_reprove probe tail (~12257) - not applicable: display fallback after `record.get("error")`; the record itself is read by `raw_decode` from the first `{`, not by last line.
8. s6_reprobed_close tail (~12278) - not applicable: display.
9. S6 manual half finalize_task (~12532) - not applicable: display in a Refusal.
10. S7 awaiting the scribe finalize_task (~13052) - not applicable: display in a Refusal.
11. stage close finalize_task (~13676) - not applicable: display in a Refusal.
12. check_traceability.py (~14069) - not applicable: display.
13. ledger.py (~14077) - not applicable: display.
14. gate B check_traceability.py (~14137) - not applicable: display.
15. gate B ledger.py (~14149) - not applicable: display.
(The brief said 14 `[-1]` sites; the grep finds 14 `splitlines()[-1]` plus the two JSON readers 3404 (`or ["{}"]`) and the `gate_answer_told` loop, which are listed above/below.)
16. gate_answer_told loop - APPLIED: now `_read_answer`.

story_step.py (all display of a script's last line as a note, none reads a JSON answer by last line):
- :415 handoff_check failure note - not applicable (display; the JSON read is whole-output, see analogs).
- :440, :441 brief_pack note - not applicable: display.
- :460 `_derive_before` note - not applicable: display.
- :555 probe_debt tail - not applicable: display.
- :929 stage_done note - not applicable: display (note: the expression `"..." + out.splitlines()[-1] if out else "..."` binds the `+` first, so with empty output the note is the failure text only; harmless, left).
- :2838 window_record note - not applicable: display.

walk_session.py: no last-line read of a script's output (its `json.loads` sites read a socket line :1259, :1132, and a verdict file :1382) - not applicable.

## Analogs noticed, not fixed (outside "last line", non-goals)
- story_run.py ~2411 `json.loads(out)` of `handoff_check.py --json` and story_step.py :413 the same: they parse the WHOLE output, so a stderr warning makes them read "unparsable" (story_run: form problems unread -> `None`; story_step: status `none` with the note). Same class, a different shape (whole text, not last line). Suggest routing both through `_read_answer`.
- story_run.py ~12241 `raw_decode(out[out.index("{"):])` of probe_by_code: warning-tolerant unless the warning itself contains `{`.
- `runtime_paths.py:378` warning: left as is (non-goal).

## Witness
See the closing lines in the final message: pytest of the new file (4 passed), test_driver_layers 52/52, test_read_json 382/382, test_audit_rules 328/328. Red-first: the new tests were run against `git show HEAD:...story_run.py` placed over the file from a byte copy: 4 failed; restored, sha256 identical (e8ce11d2...0b0e).
