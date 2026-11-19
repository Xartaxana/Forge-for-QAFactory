# t-1525 S-B report (builder)

## Question (blocks T6)
E-B5: the sentence ending «does not execute it.» is GONE from COORDINATOR.md (FG7-62 squeeze). Rule 3 (lines 123-125) now reads
«...the critic's VERDICT layer and its control re-run: `.claude/agents/critic.md` rule 21.» Per E-B5 I stopped: T6 NOT written.
Needed from the Lead: the exact insertion (my suggestion, not applied: append to that sentence « The critic's own run beyond
that is the bounded probe of `.claude/agents/critic.md` rule 21 (its runner, its cap, Bash only).» after «rule 21.», plus the
POINTERS row `(COORD, "`.claude/agents/critic.md` rule 21", CRITIC, CRIT_21)`). Until then the doc key
«the bounded probe of `.claude/agents/critic.md` rule 21» is MISSING (the witness shows it).

## Plan items
- T1, T2, T3, T4, T5 DONE: `.claude/agents/critic.md` (rules 17, 20, 21, 22 Q5 (a)); T4 carries F-2 (a): reason named in the `accepted` event's notes.
- T6 NOT DONE (above).
- T7 DONE: CLAUDE.md R11-h. T8 DONE: tools/handoff_gate.py docstring only. T9 DONE: builder.md rule 8. T10 DONE: designer.md rule 1.
- T11 DONE: PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md 13(j) and new check 50 (spec section 9 text, with the (a) opener, rule 21/22 Q5 substitutions; one line like its neighbours).
- T12 DONE: docs/SIBLING_MAP.md axis 31 (TESTING row, critic.md row).
- AGENTS.md regenerated (`agents_md.py --repo .`).
- Test: one OWNER_KEYS row `review:probe` in tools/tests/test_role_carriers_one_owner.py (1 line). The POINTERS row waits for T6.
- Not done, not in T1-T12: spec section 10.2's SIBLING_MAP axis 38 block (card R5 mentions it; no text given). Question for the Lead if wanted.

## Staged/commit
Nothing committed or staged by me (edits are in the worktree). Mechanism files (critic/builder/designer.md, CLAUDE.md, COORDINATOR.md untouched, AGENTS.md, handoff_gate.py, calibration, SIBLING_MAP) are for the Lead. The report, test file and changelog fragment `ai-packages/qa-factory/changelog.d/test-rules-sb-probe-and-test-line.md` are mine.

## Boot bytes (E-B7)
CLAUDE.md 14011 -> 14136 (+125). COORDINATOR.md 43156 unchanged (T6 not written; ~120 B to come). `session_context.py`:
`BOOT BUDGET: 109064 bytes / 120000 (9 files) | CLAUDE.md: 14136/16700` -- below 110000 (936 B headroom; T6 adds ~120 B, still under).

## Witness (one run after all edits)
```
python -m pytest tools/tests/test_role_carriers_one_owner.py tools/test_handoff_rule_anchors.py tools/test_handoff_gate.py -q
222 passed in 1.91s
python -B tools/install_parity.py --check   -> MISSING (0)   (also UNKNOWN (0))
python -B tools/agents_md.py --check        -> AGENTS.md: up to date (114667 bytes)
python -B tools/pointer_lint.py --check     -> pointer_lint: ok (34 files, 1974 pointers)
python -B tools/registry_preflight.py check lint --paths tools/handoff_gate.py -> registry preflight: lint ok (0.1 s)
```
Doc-dispatch witness (script `sb_witness.py` in full below; keys verbatim from card section 3, whitespace squashed):
```
OK  - **The probe** ... (16 more OK lines, all present keys except one)
MISSING the bounded probe of `.claude/agents/critic.md` rule 21      <- T6, see Question
OK absent -- judged by reading it. / not a new file (the one exception / a DoD never asks for a new test file outside the keep rows / a docker run or a mutation RUN is the leak / critic-diff-brief
negative control key present? False (False => a required key absent reports MISSING)
FAILURES 1   rc=1
```
The single MISSING is itself the live negative control (a key absent gives failure, rc=1); a deliberately absent control key `ZZZ-no-such-key` is also reported absent.

E-B6: `grep -nE "copy, mutate|byte copy of the file BEFORE" critic.md TESTING.md CLAUDE.md COORDINATOR.md` -> no output, rc=1 (0 hits).
Control: `grep -nE "byte copy" tools/handoff_gate.py CLAUDE.md` -> handoff_gate.py:10 (T8 line), CLAUDE.md:83, :89, :136.

```python
import re, sys
def sq(s): return re.sub(r'\s+', ' ', s)
R = lambda p: sq(open(p, encoding='utf-8').read())
C = R('.claude/agents/critic.md'); B = R('.claude/agents/builder.md'); D = R('.claude/agents/designer.md')
CL = R('CLAUDE.md'); CO = R('COORDINATOR.md'); H = R('tools/handoff_gate.py')
W = R('PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md'); S = R('docs/SIBLING_MAP.md')
ALL = C + B + D + CL + CO + H + W + S
present = [...18 keys of the card "Doc keys present" list verbatim...]
absent = [...5 keys of the card "Absent" list verbatim...]
# loops print OK/MISSING per key, count failures, sys.exit(1 if bad else 0)
```
(Full source: `C:/Users/i_mas/AppData/Local/Temp/sb_witness.py`, outside the repo.)

## Deviations / notes
- T4 clause lands in full; it names the `mutants` field S-D (t-1522) must land in the same wave (E-B1).
- Line wrapping: T1's sentence is inserted on the existing line then wrapped by me; T3/T5 insertions make some lines longer than the 120-col neighbours (no cap checked).
- Analogs seen: none beyond the list above. Readers outside owns: not run.
- Needed beyond the manifest: COORDINATOR.md rule 3 lines 120-131 read; docs/SIBLING_MAP.md rows; the spec section 9.

## Round 2 (Lead answers)
- T6 DONE: COORDINATOR.md rule 3, sentence appended after «...control re-run: `.claude/agents/critic.md` rule 21.»; POINTERS row `(COORD, "the bounded probe of `.claude/agents/critic.md` rule 21", CRITIC, CRIT_21)` added (test file, 2 test lines total).
- Axis 38: Lead's commit block, nothing written. Changelog fragment unstaged and deleted (no package file touched).
- AGENTS.md regenerated: 114793 bytes. COORDINATOR.md 43156 -> 43282 (+126).
- Mechanism files are STAGED (builder/critic/designer.md, AGENTS.md, CLAUDE.md, COORDINATOR.md, calibration, SIBLING_MAP, handoff_gate.py); the report and test file are committed.
Witness (one run, after all edits):
```
pytest (3 files) -q            -> 223 passed in 1.54s
install_parity --check         -> MISSING (0)
agents_md --check              -> AGENTS.md: up to date (114793 bytes)
pointer_lint --check           -> pointer_lint: ok (34 files, 1976 pointers)
registry_preflight check lint  -> registry preflight: lint ok (0.1 s)
BOOT BUDGET: 109190 bytes / 120000 (9 files) | CLAUDE.md: 14136/16700
sb_witness.py                  -> all 18 present OK, 5 absent OK, FAILURES 0
negative control (key "Bash is not gated hereX") -> MISSING line, FAILURES 1
E-B6 grep (4 files)            -> no output, rc=1; control `byte copy` finds handoff_gate.py:10
```

## Round 3 (check 50 placement)
Defect was mine: `s.index('## Weekly cost review')` hit check 48 (h)'s inline mention. Fixed: check 50 removed from check 48, re-inserted as its own item after check 49, before the heading line (blank line each side). `git diff HEAD -U0 -- PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: only the 13(j) hunk (lines 397-398) and the added check 50 block at 1153. `grep -c "^## Weekly cost review"` = 1.
Witness: pytest (3 files) 223 passed in 1.86s; key run FAILURES 0; negative control FAILURES 1.
