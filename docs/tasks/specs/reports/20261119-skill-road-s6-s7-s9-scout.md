# Skill road S6/S7/S9 close gaps (scout t-1586, Lead digest 19.11.2026)

Nodes: FV3-24 (S6 code steps), FV3-26 (S7, S9), FV3-29 (A27 reach). P = `ai-packages/qa-factory/scripts`.

## Q1 FV3-24: driver S6 steps the skill road does not run
- q1a `s6.results_stand` freshness close, P/driver_stage_s6.py::DriverStageS6.stage_S6 / `s6_freshness`: NO.
- q1b `s6_reprove` (probe replay via probe_by_code.py): NO; story_step names probe_by_code only in a comment.
- q1c `s6_reprobed_close` (site `s6.reprobed`): NO.
- q1d driver `s6_reentry`: NO (story_step::_s6_reentry is a different guard on a completed code_only S6).
- q1e `s6_reprove_before_manual` (HF8-18): NO.
- q1f `s6.nothing` and q1g `s6.accepted`: NO; story_step::_s6_manual_close returns None on an empty manual half.
- q1i/q1j manual half close: YES (story_step::_s6_manual_close -> stage_close::manual_half_close).
- q1q analyst acceptance (`need_record`): only at the manual_close site.

## Q2 FV3-26: S7 and S9
- q2d/q2e: the skill road closes S7 and S9 by prose only (s7.md, s9.md tell the conductor to run stage_done.py by hand).
- q2f: story_step has no S7/S9 code; stage_close::close_by_code is stage-agnostic, so SkillRoad could run it.
- q2g: CONSUMER_ROUTES["S7"] exists as data; nothing calls need_record for S7.
- q2h: card r2 says no run verified a skill-road S7 close.
- Driver sites: S7 `s7.no_failures`, `s7.pretriaged`, `s7.accepted`, `s7.after_repairs`, `s7_await_scribe`; S9 `s9.skip`, `s9.numbers` (record_close), full via the retro role.

## Q3 FV3-29: A27 and stage_close.py
- q3a/q3b: A27 scans story_run.py + driver_*.py only (audit_factory.py A27 block); stage_close.py is outside it.
- q3c: stage_close::SkillRoad.record_close tail loop `self.py("log_append.py", *row)` DROPS its result (the only dropped result found); reached when `tail` is non-empty (S7 sites).
- q3d/q3f/q3g: other calls bind or raise; owe_row prints a note, never raises.
- q3j: A27_BLIND B1 names "a receiver other than self" as blind.

## Lead decisions (19.11.2026)
- Q3 fork: FV3-29 = bind/check the log_append result in SkillRoad.record_close plus a test row; widening A27 to stage_close.py is a separate later node (class fix), not this one.
- Q2 fork: S7 first in its own node (FV3-26), smallest step `s7.no_failures`; S9 after it in the same node only if the S7 part lands green.
- Q1: FV3-24 first move = `s6.nothing`/`s6.accepted` through close_by_code at the empty-manual-half point; reprove family follows as FV3-24b.

## Not verified by the scout
controller.py code_only projection; whether Driver.record_close equals SkillRoad.record_close.
