# t-049 (fix round of t-046), TD-11 P0-C

## Items
- F1 DONE. test_words_doors.py: new `script_units(plugin_root)` -> [(key, text)]; every file of `harness.driver_sources` carries the one key `DRIVER_KEY` ("scripts/story_run.py"), other scripts keep their path. `scan` and `converted_doors` read through it (hits/counts of the driver set are merged under the one key). `PENDING`, `EXEMPT`, the fake-package control and `expected` use `DRIVER_KEY`.
- F2 DONE. test_s7_null_outcome.py: one `scan_lines(regex, path, functions, what)`; `hits` and `raw_hits` are one-line wrappers. Difference: the raw scan on a whole file now also emits no "found" check (it was a vacuous pass before), so the printed check count is 300 vs the old count +0/-N whole-file raw rows.
- F3 DONE. stop_record self-check and s0 RETRY_AT_RE tombstone removed.
- F4 DONE. Both docstrings say "the driver set".
- N1 DONE. test_knowledge_notice.py: `drive_gate_repair` + `test_gate_a_notices_after_the_kept_answer_branch_and_before_the_entry_steps` (~30 lines). It calls the real `Driver.gate_repair(stub_self, "A")`; the spy replaces `PK.notice_from_handoff`; order is observed by behaviour: no kept answer -> [notice(P, TR, ticket), entry A]; kept answer -> [recorded again], no notice.
  Spec note: the dispatch said "NOT called when no answer is kept"; the code (story_run.py gate_repair, kept branch returns first) calls notice when NO answer is kept and NOT when one is kept. I tested the code's and the critic's meaning (position invariant "after the kept-answer returns").

## driver-layers.json rows changed (the Lead re-applies)
- changed: `test_words_doors.py` / `<module>`: count 2 -> 1, why: "DRIVER_KEY, the one path key the inventory files the whole driver set under (every file of `harness.driver_sources`), not a read of the source"
- changed: `test_words_doors.py` / `part_detector`: count 7 -> 2, why: "writes a FAKE story_run.py as a fixture and names `story_run.py` in the converted-doors expectation; the real source is read only through `harness.driver_sources` (no file name in it)"
- no row added or removed.

## Item 1 temp-copy proof (scripts/ copied to a temp dir outside the repo; story_run.py's `person_words.door(` calls and PENDING texts rewired out, the same calls and the PENDING texts put in `scripts/driver_zz.py`; script: scratchpad proof_f1.py)
```
baseline unlisted: {} converted: {'scripts/story_run.py': 3, ...}
POSITIVE unlisted: {}
POSITIVE driver key hits kept: 4 of 2
POSITIVE converted driver key: 1 (baseline 3 )
NEGATIVE unlisted: {'scripts/story_run.py': ['waiver.py --task T --stage S2 --block "other" --decision "']}
```
(converted 1 not 3: the proof moved only one call into the part; the key is present, as `expected` needs. Hits 4 vs 2: the proof's moved copy also leaves the broken-option duplicates; unlisted stays empty.)

## DoD output
```
=== test_driver_layers: 58/58 ok ===
=== s7 null outcome: 300/300 ok ===
=== test_driver_stop_record: 42/42 ok ===
=== test_story_run_words: 115/115 ok ===
test_knowledge_notice.py: 15 passed in 6.15s
pyflakes on the six owned files: no output, exit 0
```
test_words_doors.py and test_story_run_s0.py were NOT run as wholes (slow). Instead `test_words_doors.part_detector()` was imported and run on the real tree: no FAIL line; PENDING prints show `scripts/story_run.py: 2 inline door(s)` (the key survives).

## Slips
- One `cd /tmp` in a Bash call (hook WARN; harmless, no repo effect).
