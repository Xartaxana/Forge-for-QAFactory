# t-768 — critic on the SC-N7 diff (builder t-758): `exploratory_findings.append` refuses every problem of a line at once

Under review: worktree `C:\QAFactory\forge-repo\.claude\worktrees\sc-n7`, commit 3ae834f on `wip/sc-n7`, compared against merge base 1a00352. The merge base and origin/main e4df9c0 hold the same `exploratory_findings.py`: `git diff <mb> origin/main -- <file>` is empty.
Brief: `docs/tasks/critic-diff-brief.md`, all standing questions. Spec/DoD: items 1-7 and the non-goals of the dispatch.

## Verdict

**ACCEPT WITH FIXES (fit_with_fixes): 0 merge blockers, 4 binding fixes for one fix round.** Fixes 1 and 2 break DoD item 1 ("a line with ONE problem gives a message byte-identical to before") on 6 of the 27 single-problem lines I probed. Fix 3 breaks DoD item 1 ("ONE ValueError whose message carries every problem found"): one evidence-ref input throws away every problem already collected. Fix 4 adds the test rows that would have caught all three. The architecture is sound: the stoppers, the dependants that get skipped, the OSError path and the callers all check out. The decision to accept stays with the Lead.

## Findings

**F1 — `oracle_status: confirmed` alone now gives two sentences (DoD item 1; fix before merge).** `exploratory_findings.py` lines 348-351: the new code appends the "confirmed oracle is a case check" sentence and then also runs `_closed(problems, "oracle_status", ...)`. `"confirmed"` is not in `ORACLES`, so a second sentence is added. Before the diff, the first `raise` returned before `_closed` ran. Probe output (old module from git, new module, same temp story):
```
old: a confirmed oracle is a case check: it goes through the case and S7, not this register
new: a confirmed oracle is a case check: it goes through the case and S7, not this register; `oracle_status` is `confirmed`; expected one of none, documented_text_only, owner_question, person_confirmed
```
The existing CLI row (test line 126) matches with `needle in err`, so it stays green.

**F2 — an excluded key nested in a sub-object is reported twice (DoD item 1; fix before merge).** Surface: the walk that maps each problem to one sentence. The excluded-key walk (`_walk_excluded`) already finds `EXCLUDED` keys at any depth. `_nested_keys` reports the same key again as "not a field of `<label>`". The top level is protected (`key not in found`, line 323); the four nested carriers are not. Probe, 5 single-problem lines that differ:
```
evidence ref {path, severity}: old = the excluded sentence; new = it + "`severity` is not a field of the findings register; the fields of `evidence_refs[]` are path, sha256"
probe {..., impact}       : + "... the fields of `probe` are method, runs, reproduced, environment, safe_to_break"
origin {..., bug}         : + "... the fields of `origin` are dispatch, target"
corrects {..., priority}  : + "... the fields of `corrects` are id, reason"
impact in probe AND origin: excluded sentence once + two nested sentences
```
Same surface, neighbours walked:
- unknown vs excluded at the top level: already guarded.
- withdraw "not carried" vs unknown: guarded by `key in FIELDS`.
- withdraw "not carried" vs code-set: guarded by `CODE_SET`.
- capture-less vs a closed status: guarded by the `_closed` return value.
- `person_confirmed` vs closed: the value is in the list, so only one sentence.
- an empty `evidence_refs` gives the required sentence only, because the judge loop is empty.
- an excluded key inside a `refs` item: two genuine problems, since the item is not an id either way.

Only F1 and F2 duplicate.

**F3 — an evidence path that `resolve()` cannot stat throws away every collected problem (DoD items 1-2; fix before merge).** Line 254, `candidate = (root / raw).resolve()`, raises `ValueError: stat: path too long for Windows` (also `embedded null character`). It is raised from inside `_judge_refs`, so `append` propagates it bare. Probe, "everything broken" line (a bad kind, missing texts, a bad origin, and so on, plus one ref whose path is 40,000 characters):
```
old: `severity` is not a field of the findings register: ...
new: stat: path too long for Windows
```
Traceback: `exploratory_findings.py line 254 in _judge_refs -> pathlib.resolve -> os.stat`. On a single-problem line the text is unchanged (the probe rows "evidence path long" and "evidence path NUL" are SAME), so catching it is byte-safe. It is a ValueError, so "no non-ValueError escapes" holds. What breaks is "one message carrying every problem".

Neighbours on that surface, the evidence-ref measurement step:
- magnitude and encoding: this finding.
- empty path: skipped; the judge speaks.
- path as an int or a list: `_text` gives "", the judge speaks.
- PermissionError from `sha256_file`: an OSError that was already there before. The spec keeps OSError behaviour unchanged, so it is a note, not a fix.

**F4 — the tests do not hold DoD item 1 for single problems (fix before merge).** Only one row of the new table pins a single-problem message exactly (`kind: bug`). The older single-problem rows match by substring, which is how F1 and F2 passed 314/314. This is not a request for "a missing pin": these rows judge the behaviour the node exists for.

**Builder's flagged decision (`by` and the window first, alone): sound. No caller depends on the old order.**
- CLI: `_run` already refuses a blank or `code:` `--by` before `append` (lines 526-528), so the CLI order for `by` does not change.
- `register_gaps_write` passes `by=dispatch` (non-empty) on a story that has a `pipeline.json`. It wraps any `ValueError` whole as `{exc}. {expected} ... {door}` (`driver_stage_plan.py` 680-683).
- Other in-process callers (not in the dispatch's list): `investigation.py` 341/350/365 use `by=BY_PROJECT`; `driver_machine.py` ~2813 uses `QUESTION_ANSWER_BY`. Both are constants, and both callers show `{exc}` or let it propagate. Neither parses the text.
- Grep for consumers of the refusal texts (case-insensitive, five distinctive phrases, positive control = the module itself: count 1): only the test file matches.
- Rounds: a broken window used to cost N+1 rounds under first-error. With collection it costs 2 in either order (window then shapes, or shapes then window). Window-first is better: a wrong `--task-root` would otherwise add false "not a file under the task root" evidence sentences. No useful shape sentence is lost; it comes on the next round, all at once.

**Spec-internal conflict, noted, not against the builder.** Item 4 says "`{}` reports every missing required field". Item 2 makes an absent `op` a stopper. The builder followed item 2 (`{}` → the op sentence) and covered item 4 with `{"op":"add","kind":...}` rows, one per kind. That is the safe reading.

## Standing questions

1. **Fit to the spec**: items 2, 3, 5, 6 and 7 are met. Item 1 is not met (F1, F2, F3). Item 4 is met under item 2's precedence.
   - "No problem refused before is accepted now" holds. I diffed the refusal conditions: every old `raise` is now an `append`, and the closing `if problems: raise` covers them. Every skipped branch has a companion sentence: the oracle (bad kind), capture-less (bad status), the target comparison (broken origin), the id lookup (link not an object), the judge (evidence not a list). The stoppers and the OSError re-raise stay.
   - I ran 27 single-problem lines and 21 awkward lines (kind as a dict, op as a list, refs as nested lists, ref as None/list/int, a non-string sha, probe with an int key, corrects id as a list, origin as a list or with an int target, int top-level key, very long strings, everything broken at once). Every one of the 48 ended in a ValueError, and nothing was written (the register length is unchanged).
2. **Builder decisions**: by/window first is sound (above). Excluded keys are deduplicated with `dict.fromkeys`; one key at two depths gives one sentence, which is correct.
3. **Seams**: only `exploratory_findings.py`, its test file and one data row. The callers are untouched and still read one refusal: `run_guarded` → `refuse(command, str(exc))`, plus the registry door. No newline enters the message. FR-1, FR-2, AR-9 and AR-18 hold.
4. **Class-wide completeness (key e)**: the other `open` GUARDED rows of `test_validator_class.py`:
   - `red_sandbox.py --diagnostic` (row 348, "first error"): the same class, worth a node. Queue line: `red_sandbox.run_diagnostic refuses the request key by key (first error) | перенос: findings/<new: diagnostic-all-problems.md> | обоснование: same first-error class as SC-N7, GUARDED open row | подтвердил: —`
   - `manual_evidence.py export` and `external_writes.py --record` ("not established by t-1349"): not known to be this class. Ask a scout first. Queue line: `whether manual_evidence export / external_writes --record validators stop on the first error | перенос: findings/<new: guarded-not-established.md> | обоснование: GUARDED rows open since t-1349 | подтвердил: —`
   - `work/requirements-readiness.json`: already queued by F-8.
   - `tried.md` and `work/bug-drafts/`: a different class (no validator on write).
   - `walk_session.py claim`: owned by thinking-roles TR4-16.
   - SIBLING_MAP: no axis covers first-error validators; the census table is the carrier. Axis 29 (jsonl appender): `hooklib.append_jsonl_line` is still the writer, so it is covered.
5. **Tests (key f)**: rows sit in the existing named, parameterised table, which fits the cases-table layer of `docs/TESTING.md`. No receipt-per-key and no pin on role text. +73 test lines against about 200 product lines. The negative control is outside the test, as it should be. Gap: F4.
6. **DUPLICATION AND CONSISTENCY**: none found. `"; ".join(problems)` is the package's own idiom: 35 sites outside the tests, for example `driver_stage_plan.py:668`, `changelog_assemble.py:218`, `contract.py:6093`. No shared helper exists. I grepped `PROBLEM_JOIN|def join_problems|def refuse_all|def collect_problems` over `scripts/`; the only hits are this diff. The local constant `PROBLEM_JOIN` matches the idiom.
7. **CODE QUALITY**:
   - `append` is lines 293-430, about 138 lines (about 120 before), with 4 nesting levels at 389-397 (op ≠ add → link → acted → elif origin_ok → was ≠ target). Severity: queue (pre-existing size; a split into `_shape_problems` and `_chain_problems` is natural).
   - The `stop` list exists only to reuse `_closed`. Minor, no finding.
   - The commit's "same words per problem" and the report's "every sentence is byte-identical" are falsified by F1/F2. Correct them in the fix-round report.
8. **Hygiene**: LF kept (0 CR, old and new), no non-ASCII, no line over 160 characters.
9. **Ratchets**: none touched. The GUARDED edit closes an `open` row; it is not a raise.
10. **ARCHITECTURE**: AR-9 and AR-18 are named. Producer and reader walk: `append` (producer of the refusal) → `run_guarded`, `register_gaps_write`, investigation, driver_machine. All read `str(exc)` whole. No second form.
11. **JUDGMENT**: none moved. These are shape and identity checks, as before. `judgment: none` is true.
12. **ONE ROAD**: none found. No branch on a language, project or runner. The stoppers apply to every caller alike. Grepped the diff for language and runner names: none.

**Key (d), the GUARDED row**: `none` is the closed form the table uses for "the validator lists every problem itself" (compare `manual_capture.py ui`). The reason becomes true once F3 is fixed (today one input drops the collected problems). No edit to the row is needed beyond the fix.

## Binding fixes (fix round, fresh worker)
1. `exploratory_findings.py` 348-351: when `oracle == "confirmed"`, append only its sentence and skip `_closed("oracle_status", ...)` (elif), so a confirmed-only line gives the old single sentence.
2. `_nested_keys` (line 223): skip keys in `EXCLUDED`. The excluded walk already reports them at any depth, the same rule the top level applies with `key not in found`.
3. `_judge_refs` 253-256: catch a `ValueError` from `resolve()`/`is_file()`, append `str(exc)` as that ref's sentence and `continue`, so the problems already collected survive.
4. Add exact-equality rows to the K-M1-1 "all problems" table: confirmed oracle alone; an excluded key nested in `probe` and in an evidence ref (one sentence each); a 40,000-character evidence path plus an empty title (both sentences).

## Trail
- Read: the brief; the full diff of 3ae834f; `exploratory_findings.py` 40-299 and 404-551 (new); old module via `git show origin/main:...`; test diff and helpers 1-130; `test_validator_class.py` GUARDED 280-389; `driver_stage_plan.py` 640-690; `driver_machine.py` 2700-2830; `investigation.py` 326-372; `role_cli.run_guarded` 134-173; the builder report; the commit message; SIBLING_MAP axis list; the schema.
- Re-run: `python -B .../sc-n7/ai-packages/qa-factory/scripts/tests/test_exploratory_findings.py` → `=== test_exploratory_findings: 314/314 ok ===` (matches the witness).
- Probe: an in-memory stdin script loading the old module (from git) and the new one against a temp story, 48 rows → `single-problem diffs: 6 | register bytes: 450` (unchanged after every refused row); the diffs are listed in F1 and F2. Traceback probe for F3 → `line 254 in _judge_refs ... ValueError: stat: path too long for Windows` (Python 3.12.10).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Same artifact: the duplicate-sentence surface walked (top-level unknown vs excluded guarded; withdraw vs unknown and vs code-set guarded; capture-less guarded; nested excluded F2 and confirmed oracle F1 not). Census open rows: red_sandbox --diagnostic is the same first-error class, queue line given; manual_evidence export and external_writes --record need a scout question first; readiness F-8, tried.md and bug-drafts are a different class; walk_session claim is owned by TR4-16. SIBLING_MAP: no axis for first-error validators; axis 29 appender unchanged.",
  "fixes": [
    "exploratory_findings.py 348-351: on oracle == confirmed append only its sentence and skip the closed-list check (elif), so the single-problem message is byte-identical.",
    "_nested_keys: skip keys in EXCLUDED, which the excluded walk already reports at any depth, as the top level does with key not in found.",
    "_judge_refs 253-256: catch ValueError from resolve()/is_file(), append str(exc) as that ref's sentence and continue, so collected problems survive.",
    "Add exact-equality rows to the K-M1-1 all-problems table: confirmed oracle alone, excluded key nested in probe and in an evidence ref, a 40000-character evidence path plus an empty title."
  ],
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      ".claude/worktrees/sc-n7 git diff origin/main...HEAD (3ae834f)",
      "ai-packages/qa-factory/scripts/exploratory_findings.py (new 40-299, 404-551; old via git show)",
      "ai-packages/qa-factory/scripts/tests/test_exploratory_findings.py 1-260",
      "ai-packages/qa-factory/scripts/tests/test_validator_class.py 250-389",
      "ai-packages/qa-factory/scripts/driver_stage_plan.py 640-690",
      "ai-packages/qa-factory/scripts/driver_machine.py 2700-2830",
      "ai-packages/qa-factory/scripts/investigation.py 326-372",
      "ai-packages/qa-factory/scripts/role_cli.py 134-173",
      "docs/tasks/specs/reports/20261114-sc-n7-report.md",
      "docs/SIBLING_MAP.md axis headings",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B .claude/worktrees/sc-n7/ai-packages/qa-factory/scripts/tests/test_exploratory_findings.py", "result": "=== test_exploratory_findings: 314/314 ok ==="},
      {"command": "stdin probe: old (git show origin/main) vs new append on 27 single-problem and 21 awkward lines, temp story", "result": "single-problem diffs: 6 (confirmed oracle; nested excluded key x5); all 48 rows ValueError; register bytes unchanged 450; everything-broken row new = stat: path too long for Windows"},
      {"command": "stdin probe: traceback of a 40000-char evidence path with other problems", "result": "exploratory_findings.py line 254 in _judge_refs -> pathlib.resolve -> os.stat: ValueError: stat: path too long for Windows"}
    ]
  }
}
```
