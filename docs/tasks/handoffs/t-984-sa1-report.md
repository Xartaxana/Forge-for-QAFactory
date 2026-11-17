# t-984 S-A1 report (builder)

Commit (worktree branch, not pushed): `c640bf13` (amended once, own unpushed commit, to add the `tests-over:` line). The
commit-msg gate asked for no axis block and no `tier:` line (output: `gates: ok (7 checks)` / `gates: ok (4 checks)`), so the
work is COMMITTED, not staged; the message carries no `axes:` line (it claims neither a mechanism nor a non-mechanism).

## What was inserted where
All spec texts were taken from the spec file BY SCRIPT (line ranges of its code fences), not retyped; CRLF kept (0 LF-only lines).

`docs/TESTING.md`
- `:55` «Чего больше нет»: «(исключение — «Бюджет / Файлы»)» -> «вместо строки в историю (когда новый файл верен — «Бюджет / Файлы»)» (2.5 row 1).
- after `:59`, before «### Карантин старых тестов» (new `:61-103`): the three subsections of §2.1, §2.2, §2.3 as written.
- «Бюджет / Файлы» bullet (was `:117`, now `:160-172`): replaced by the §4.1 text; the offload-only exception (was `:124-127`) removed; the ticket-named and split-part sentences (was `:118-123`) untouched.
- how-to item 1 (was `:141`): «нового файла нет («Бюджет / Файлы»)» -> «новый файл — только по цели «Бюджет / Файлы»» (2.5 row 4).
- «Кто что делает»: Designer bullet and Critic bullet as §2.4 (the critic bullet is the pointer, names no probe); detector sentence ends «; строки `test:`, пробы критика и `red-before:` — калибровочная проверка «Forge test discipline» (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`).» (inserted before the sentence's final period; named by title, no number).

`docs/tasks/critic-diff-brief.md`
- mechanical layer `:11`: after «(the scope: `plans/builder-rules.md` 7b);» inserted «for a defect item, the `red-before:` line (`docs/TESTING.md` «Тест может упасть»);»; the clause «no mutation list (retired 10.11.2026, `docs/TESTING.md`)» stays; `:14-15` sentence untouched.
- verdict layer (was `:16-21`): replaced by the first (S-A1) bullet of §3.2 only; NO «The probe» bullet.
- question 5 (was `:35-46`): replaced by the §3.1 text with (a) «-- judged by reading it.» (no probe clause).

`tools/tests/test_role_carriers_one_owner.py` (variant rows, no new function/file): OWNER_KEYS + `tests:oracle`, `tests:line`, `tests:files`; POINTERS + `("docs/TESTING.md", "`docs/tasks/critic-diff-brief.md` «The two layers»", BRIEF, "## The two layers")`.

## Witness 1: pytest (DoD 1)
```
$ python -m pytest tools/tests/test_role_carriers_one_owner.py -q
...........................................                              [100%]
43 passed in 0.73s
```

## Witness 2: doc-dispatch (DoD 2), script NOT committed (kept in the session scratchpad)
Keys quoted from card §7.2 «Doc keys (verbatim)» / «absent keys»; whitespace is squashed in the files before matching (as the carrier test does), because several keys sit across a wrapped line in the files.

Full source:
```python
import pathlib, sys
ROOT = pathlib.Path(sys.argv[1])
NEG = len(sys.argv) > 2 and sys.argv[2] == "--negative"
FILES = ["docs/TESTING.md", "docs/tasks/critic-diff-brief.md"]
squash = lambda s: " ".join(s.split())
text = squash("\n".join((ROOT / f).read_text(encoding="utf-8") for f in FILES))
PRESENT = ["### Откуда берётся ожидаемое значение", "### Строка теста в DoD", "### Тест может упасть",
           "red-before:", "(e) DUPLICATE", "A missing PIN", "-- judged by reading it.",
           "решает цель, а не запрет и не слово владельца",
           "Строка `keep` в `test-layers.json` — учёт файла пакета",
           "калибровочная проверка «Forge test discipline»"]
ABSENT = ["Исключение (слово владельца 14.11.2026", "новый тестовый файл не создаётся; случай идёт",
          "ratchets and mutation runs are not", "1–3 места", "- **The probe**",
          "by the probe of «The two layers»"]
if NEG:
    PRESENT[3] = "red-before-NOT-IN-FILES:"   # deliberate: a key that is not in the files
bad = 0
for k in PRESENT:
    ok = squash(k) in text
    print("present-key", "OK  " if ok else "FAIL", k)
    bad += not ok
for k in ABSENT:
    ok = squash(k) not in text
    print("absent-key ", "OK   " if ok else "FAIL", k)
    bad += not ok
print("RESULT:", "FAILURE (%d)" % bad if bad else "all keys as expected")
sys.exit(1 if bad else 0)
```
(Note: the report copy has one cosmetic whitespace difference in the `absent-key` print literal; the logic is identical to what ran.)

Run (`PYTHONIOENCODING=utf-8 python -B witness.py <worktree>`):
```
present-key OK   ### Откуда берётся ожидаемое значение
present-key OK   ### Строка теста в DoD
present-key OK   ### Тест может упасть
present-key OK   red-before:
present-key OK   (e) DUPLICATE
present-key OK   A missing PIN
present-key OK   -- judged by reading it.
present-key OK   решает цель, а не запрет и не слово владельца
present-key OK   Строка `keep` в `test-layers.json` — учёт файла пакета
present-key OK   калибровочная проверка «Forge test discipline»
absent-key  OK   Исключение (слово владельца 14.11.2026
absent-key  OK   новый тестовый файл не создаётся; случай идёт
absent-key  OK   ratchets and mutation runs are not
absent-key  OK   1–3 места
absent-key  OK   - **The probe**
absent-key  OK   by the probe of «The two layers»
RESULT: all keys as expected
exit=0
```
NEGATIVE control (`... --negative`: the present key `red-before:` replaced by `red-before-NOT-IN-FILES:`):
```
present-key OK   ### Откуда берётся ожидаемое значение
present-key OK   ### Строка теста в DoD
present-key OK   ### Тест может упасть
present-key FAIL red-before-NOT-IN-FILES:
present-key OK   (e) DUPLICATE
(... the other present and absent lines OK, as above ...)
RESULT: FAILURE (1)
exit=1
```

## Witness 3: anchors (DoD 3), grep count in `git show HEAD:<file>` (before) vs the tree (after), plus the diff hunk list
```
critic-diff-brief.md   ## The two layers                         before=1 after=1
critic-diff-brief.md   6. **DUPLICATION AND CONSISTENCY**        before=1 after=1
critic-diff-brief.md   7. **CODE QUALITY**                       before=1 after=1
critic-diff-brief.md   12. **ONE ROAD**                          before=1 after=1
TESTING.md             Бюджет / Объём                            before=1 after=1
TESTING.md             Как писать эффективный тест на нашем проекте  before=1 after=1
TESTING.md             Бюджет / Файлы                            before=3 after=5   (the heading-level mention is the bullet «- **Файлы**»; the phrase count grows by the new pointers of 2.2/2.4)
```
`git diff -U0` hunks on the brief: `:11`, `:17`, `:20-21`, `:35-46` only (the headings «6.», «7.», «12.» and the OWNER keys of q7 «functions over roughly 60 lines…» and q12 «a line for the coordinator to tell someone is itself a finding» sit outside every hunk; both keys still pass in the pytest run above: `review:critic`, `review:one-road`). The three TESTING headings of card 7.2 are not in any hunk. «Бюджет / Файлы» is quoted by every pointer as a name, and the «Файлы» bullet's own text is the only edited part of that section.

## Questions returned
None. No item needed a design decision. Two small placement facts (not decisions, both are the spec's words applied literally): (1) the §2.4 detector append has no stated insertion point relative to the sentence's final period; I put it before the period so the sentence stays one sentence. (2) The spec's verdict-layer text says «the standing questions below» (was «the two standing questions»); placed as written.

## Deviations / findings
- Test volume WARN of the commit hook (+4 test lines, +0 product lines): the 4 lines are the card-7.2 rows. `tests-over:` line is in the commit message.
- Spec vs reality: none found. All `:NN` anchors of the spec matched the live files (TESTING `:55,:117,:124-127,:141,:174,:176-178,:181-182`; brief `:11,:16-21,:35-46`).
- The gate asked for no axis block / `tier:`: TESTING.md and the brief are not on the mechanism net by the gate's own run, so nothing was staged-only. The Lead may still want to paste the §10.2 block when merging.

## Analogs noticed outside owns (report only)
- `docs/tasks/critic-diff-brief.md` item 13 (d) is cited by `owns_readers.py:26` (spec-facts stream L, already in the spec's siblings line).
- `plans/builder-rules.md` 7b/7d/16 (б), `docs/RUNBOOK.md:115`, `PROJECT.md` п. 13 still say «мутации судит канон пачки» / «новый тестовый файл не создаётся» — the S-A2 window of spec §4.5, open now by design.
- `.claude/agents/designer.md` rule 1 and `builder.md:51-52` still forbid a new test file outside keep rows — the S-A1 -> S-B window of §4.5, open by design.
- `.claude/agents/critic.md` rule 20 (`:173-174`) still cites only «Бюджет» — S-B.

## Needed beyond the manifest
None beyond reading the spec's §0/§10 and `git`; the spec file itself was read in full where the dispatch named sections, plus §8's window paragraph.
