# t-1241 — critic on RD1-29 code (t-1235): the critic's review word through the row `critic_review`

Diff: `origin/main...736450f1` (merge base 4ba44d5a), branch `worktree-agent-a524698487bd0097c`, 18 files +360/-54.
Spec: `docs/tasks/specs/20261117-rd1-29-review-word-one-row-card.md` with the Lead decisions at its end (F1 B, F2 a, F3 a, F4 a, F5 a, F6 a).

## Verdict

**NEEDS WORK** — 1 blocking finding (F1, FR-30), 3 fix-before-merge findings (F2-F4), all for a fix round of the same node.
The JSON block says `blocker` because F1 blocks the merge (critic.md rule 23). Whether to accept stays with the Lead (rule 6).

Standing-question lines:
- Q1 FIT TO THE SPEC: items 1-8 are implemented as written, except item 5's E2 invariant ("report: `tests` None with the registry reason"), which does not reach the verdict block (F2).
- Q2 BUILDER'S OWN DECISIONS: all three are in the safe direction (see "Deviations").
- Q3 SEAMS: additive. The new row sits between `s5_window` and `delivery`, and the `EXPECTED_IDS` order follows the file. The D13 pins are F6's.
- Q4 CLASS-WIDE COMPLETENESS: one same-artifact sibling is missed (F2, `_r_verdict`). There is one Lead doc residual (axis 5 row, below). Analogs are listed under "Seam and class notes".
- Q5 TESTS: killing power holds. F4 covers one tautological row. No duplicates. `tests-over:` is named.
- Q6 DUPLICATION AND CONSISTENCY: one second text, inside the diff (F4). No second registry reader in production code. Grepped: `load_registry|_READ|acceptable\(` in the diff's production files, and only `gate_template` hits.
- Q7 CODE QUALITY: `review_note` is 26 lines with nesting 2, and `build` got shorter. One misleading name/text (F3). No dead branches.
- Q8 HYGIENE: FR-30 is broken (F1). CRLF and line endings are unchanged: no whole-file rewrite in `--stat`. The size caps are the canon's.
- Q9 IN-TREE RATCHETS: `D13_ITEM_COUNT` went 151 -> 150 and `D13_TRIPLES` 54 -> 53, both down, and reproduced. `EXPECTED_IDS` / `EXPECTED_CONVERTED` / code-vocabulary list / K-T1.14 converted 25 -> 26 are inventory pins of a new converted row, not ratchet raises (debt 2 and exempt 6 unchanged). `judgment-census.json` is unchanged. No dup/lint raise is visible in the diff. The `forge-check` job output is not attached, so the canon is the Lead's to read.
- Q10 ARCHITECTURE: AR-1, AR-9, AR-13, AR-15, AR-19, AR-20, AR-28 and AR-29 are named and kept. AR-18 and AR-22 are touched and kept but not named (F4, cheap). VARIETY: nothing depends on project shape. The vocabulary is the charter's closed four words. An unknown word is "not approving" plus the ledger's `review_unrecognised`. An unreadable registry is a stated unknown, and there is no new block or silent default.
- Q11 JUDGMENT: `judgment: none` holds. Code reads a token of a closed vocabulary through data. No census row, no `blocks_override`, no change to the scan constants, no craft marker.
- Q12 ONE ROAD: no exclusion found. There are two roads by stage, by design (`s5_window` inside the window, `critic_review` after it), each a data row read by its consumer key. `critic_rollcall.APPROVING_VERDICTS` is node RD1-32 (row added in 4ba44d5a). Grepped: the case-insensitive literal-comparison grep in the trail.

## Findings

**F1 — BLOCKS. A literal Cyrillic character in a package file (FR-30).**
`ai-packages/qa-factory/scripts/tests/test_case_stamp.py:220` holds the adversarial word `"аpproved"` as raw bytes `0xD0 0xB0`, which is U+0430. It is not the escape `"аpproved"` the card asks for (item 1: "written as the escape, FR-30").
- Failure scenario: `selftest.py --lang` (`cmd_lang`, regex `CYRILLIC` = `chr(0x0400)`-`chr(0x04FF)` over every file under `PLUGIN_ROOT`, `selftest.py:298-325`) reports `test_case_stamp.py` and fails. That is a canon and release-gate red.
- The report's FR-G line says "FR-29/FR-30 held (the test's non-ASCII word is a `а` escape)". That load-bearing claim does not reproduce (rule 12).
- Surface: the encoding class of the adversarial word table. Neighbouring classes walked: I scanned every package file of the diff for U+0400-U+04FF, and this is the only hit. Magnitude, nesting and empty input in the same table are written as ASCII expressions (`"approved" * 1250`, `["approved"]`, `""`, `None`).
- Fix: write `"аpproved"`, and print the label through `ascii()` or as is (the label is built at runtime and never stored).

**F2 — fix before merge. The verdict block names the wrong cause when the registry cannot be read (same-artifact sibling of item 5).**
On an unreadable registry, `report_facts._tests` now returns None with `unknown["tests"]` and `unknown["tests_code"] = "tool"`. `_count_by_tests` then sets `counts["proven"] = None` (`report_facts.py:1622-1627`). Only `_r_proven` was taught the new key (`:3671`). `_r_verdict`, the head a person reads, still reads the `ledger` key, which is absent here because the ledger was readable:
- `:3551`: `"proven by tests: unknown — " + facts["unknown"].get("ledger", "the factory's record of the checks was not readable")`
- `:3570`: `"Tests: unknown — " + facts["unknown"].get("ledger", "not readable")`

Input → output: the test world of `test_report_facts.py::proven_rules` with `GT._READ` set to an unreadable registry. `RF.render(unread)["verdict"]` says "Tests: unknown — not readable." and "proven by tests: unknown — the factory's record of the checks was not readable". The real cause is the registry, and the factory-tool owner is not named. So the text is false (FR-41, FR-19) and E2's "report: the registry reason" is half done. The card's §7 listed `_count_by_tests`, `_changes` and `_r_proven` as the readers of `facts["tests"]` None and missed `_r_verdict`. The card under-enumerated, and the fix belongs in this round.

Fix: at both lines, read `"tests"` when it is in `facts["unknown"]` (as `:3671` does; `_unknown_line`'s owner prefix where the form allows). Add one `check_in` beside the new E2 row: `RF.render(unread)["verdict"]` contains "the gate registry cannot be read".

**F3 — fix before merge (minor). The kind `ran` says "ran with its proof" for instances that never ran.**
`build` passes `"ran"` for every instance that is neither stopped nor handed (`window_record.py:1693`). That includes `pending` instances (outcome `PENDING_OUTCOME`, `:1725-1729`) and instances with no run row (`:1730-1733`). `validate_window` routes those to `s5_window.review` as well, so the consumer is right. The text is not: `REVIEW_KIND_CLAUSE["ran"]` = ", and this instance ran with its proof", and `REVIEW_KIND_WORDS["ran"]` = "the verdict of an instance that ran with its proof is `approved`".
- Input → output: a pending instance with `critic_verdict: rejected` gets the note "... is `rejected`, and this instance ran with its proof; ...". That is a false statement in text a role reads (Q7, FR-1).
- The card's item 2 wording is the source, so this is a spec slip, fixed in the round.

Fix: a clause that claims no run, e.g. ", and this instance is closed by its own run and proof", plus matching wording in `REVIEW_KIND_WORDS["ran"]` and in `review_origin()`'s "for one that ran with its proof".

**F4 — fix before merge (minor, cheap).**
- (a) Q6: `review_origin()` (`window_record.py:333-337`) re-types the per-kind words as prose beside `REVIEW_KIND_WORDS`. The new test pins only the UNION of backticked words (`test_window_record.py`, the "person-less origin names the union" row), so a per-kind drift with an unchanged union goes unseen. Build the parenthetical from the same per-kind constants, or say in the docstring why it stays separate.
- (b) Q5(f): the row `check_eq("RD1-29 F4: GAP_ORIGIN['review'] is built by the same builder", WR.GAP_ORIGIN["review"], WR.review_origin())` pins the module's own assignment (`"review": review_origin()`). It is a pin on source and can only pass. Drop it.
- (c) Q10: add `AR-18` (the note keeps the `(identity, field, "<what>; <door>")` shape for the one reader `_explain_parts`) and `AR-22` (E10: the row and its six readers land in one commit, d97875cf) to the fix-round commit's `architecture:` line.

## Deviations named in the report — verdict on each

1. The S10 negative row became a positive one (`test_window_record.py:1601-1603`). Correct: F4 (a) makes the waiver door present on every review line, and the blanket-promise check (`BLANKET`, `:1600`) still asserts that the promise is gone. Q5(d) is answered.
2. Four extra `test_gate_registry` pins. These are inventory pins the new converted row forces. None is a quality-ratchet raise (Q9 above).
3. A blank word reads as absent ("carries no `critic_verdict`"). Safe direction: it is still not closing, and the door is the same. Accepted.
4. The handed kind is taken from `handed_ok`. Verified: `unrun` excludes `blocked` and `runs` (`window_record.py:1603-1607`), and the probe-gap block runs only for outcome `passed` (`:1785-1787`). Build's kinds therefore match `validate_window`'s precedence (stopped > handed > gapped > rest; `acceptance.py:1154-1173`).
5. `tests-over:` is on commit 736450f1 (the report commit), not on d97875cf. The branch carries it into the merge, and the reason holds (rows of existing tables, no new file, +146 test vs about +130 product). Accepted.

## Seam and class notes

- Axis 5 residual, Lead's doc edit (not package, outside owns). `docs/SIBLING_MAP.md:138`, the row "The critic's verdict word in the ledger", still lists `case_stamp not_approved` and `check_delivery` as "Neighbours by other carriers, not converted". After this diff they read `critic_review`, so the row is stale. Line for «Остатки»: `SIBLING_MAP axis 5 row :138 -- name critic_review, drop case_stamp/check_delivery from "not converted" | узел: rules-debt/1/RD1-29` (the Lead's commit in the same merge).
- Axis 34 analogs found by the literal-comparison grep (case-insensitive, `*.py`, package `scripts/`; positive control `contract.py:2212` hit):
  - `manifest_put.py:1693` (`critic_approval_problems`, `!= "approved"`): a flip detector (stored `unverified` -> `approved` with no `critic_note`), not an approving read. `approved_with_fixes` always carries `fix_notes` (`validate_artifacts.py:2199`). Not applicable. I name it for the Lead in case RD1-32's scope wants it.
  - `validate_artifacts.py:2199-2203`: a shape check of `fix_notes` (AR-29 shape). Not applicable.
  - `s5_plan.py:1071`: plan-review vocabulary. Not applicable, as the card said.
  - `critic_rollcall.APPROVING_VERDICTS`: node RD1-32.
- Stale names: `case_stamp.APPROVING` / `report_facts.APPROVING` are referenced nowhere in `ai-packages/`, `tools/` or `docs/SIBLING_MAP.md` except a historical comment in `test_case_stamp.py:212`. Positive control: `APPROVING_VERDICTS` hit at `critic_rollcall.py:44`.

## Spot-checks

- `gate_registry.py --check` exit 0 and `--sites` = 150: re-run, reproduced (trail).
- AR-1 pair grep: outside tests, only `contract.py:2212`. Reproduced.
- `ledger.test_state`: `review not in C.CRITIC_VERDICTS` is the same behaviour. `is_rejected` = `verdict_of(entry) == "rejected"` (`ledger.py:1038-1041`) returns first, and `CRITIC_VERDICTS` holds exactly the four words (`contract.py:2212-2215`).
- `_claim_rollcall` returning None goes to the existing "no verdict" road: in `_check_claims` (`handoff_check.py:2039-2043`) it is printed and neither accepted nor refused; in the fill path (`:2015`) it is a blank. That is the same road as the existing no-form None.
- E5: `detector_verdict.one_line` folds `\r\n`. The clause texts hold no `;`. `_explain_parts` splits at the first `"; "` (`window_record.py:1863`).
- E6/m8: a `review` note now exists only when `review:<id>` is raised. `stale_review` is raised only when the review is accepted (the `elif`, `acceptance.py:1165,1171`), so no review note explains it, and `GAP_ORIGIN["stale_review"]` exists (`:391`).
- The witness numbers match the diff (new rows in each owned test file). I did not re-run them, beyond the one control below.

## Trail

- Read: the card (whole); the report (whole); `git diff origin/main...736450f1` for every package file; `gate_template.py` 1-60; `handoff_check.py` 953-975, 1995-2050; `report_facts.py` 1505-1545, 1608-1630, 3090-3097, 3505-3575; `window_record.py` 1600-1608, 1690-1800, 1856-1880; `acceptance.py` 1135-1175; `ledger.py` 1027-1041, 1176-1192; `contract.py` 2212-2215; `detector_verdict.py` 236-238; `manifest_put.py` 1685-1700; `selftest.py` 295-325; `docs/SIBLING_MAP.md` :138; `tools/critic_verdict.schema.json`.
- Greps: the literal-comparison grep (case-insensitive) over package `scripts/*.py`; `APPROVING` over `ai-packages`, `tools`, `SIBLING_MAP` (control `APPROVING_VERDICTS`); `unknown\["tests` and `facts\["unknown"\]` in `report_facts.py`; `approved_with_fixes` in `test_handoff.py` / `test_report_facts.py` (Q5(e)).
- Commands (verbatim tails):
  - `git -C <wt> rev-parse --short HEAD` -> `736450f1`
  - `python -B <wt>/ai-packages/qa-factory/scripts/gate_registry.py --check` -> `A26 gate registry: no violations` ... `exit=0`
  - `python -B <wt>/ai-packages/qa-factory/scripts/gate_registry.py --sites | wc -l` -> `150`
  - Cyrillic scan (python, U+0400-U+04FF) over the diff's package files -> `ai-packages/qa-factory/scripts/tests/test_case_stamp.py 220 0x430` (only hit)
  - `grep -n ... test_case_stamp.py | od -c` -> `"   320 260   p   p   r   o   v   e   d   "` (the raw UTF-8 bytes of U+0430)

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1 FR-30: test_case_stamp.py:220 holds a literal U+0430 (bytes D0 B0) in the adversarial word, not the escape the card asks for; selftest.py --lang (cmd_lang, CYRILLIC 0x0400-0x04FF) goes red; the report's FR-G claim of an escape does not reproduce"
  ],
  "fixes": [
    "F1 test_case_stamp.py:220 write the word as the escape \\u0430pproved (blocks)",
    "F2 report_facts.py:3551 and :3570 (_r_verdict) read the unknown key tests when present, as _r_proven :3671 does; add a check_in that render(unread)['verdict'] names the gate registry (fix before merge)",
    "F3 window_record.py REVIEW_KIND_CLAUSE['ran'], REVIEW_KIND_WORDS['ran'] and review_origin(): wording that claims no run, since pending and no-run instances take this kind (fix before merge)",
    "F4 window_record.review_origin builds its per-kind words from the same constants; drop the tautological GAP_ORIGIN['review'] == review_origin() row; name AR-18 and AR-22 on the fix-round commit (fix before merge)"
  ],
  "class_completeness": "Axis 34: one same-artifact sibling missed (report_facts._r_verdict, F2); critic_rollcall.APPROVING_VERDICTS is node RD1-32; manifest_put.py:1693, validate_artifacts.py:2199-2203 and s5_plan.py:1071 are not approving reads (n/a). Axis 5: SIBLING_MAP.md:138 row is stale after the diff, a Lead doc edit in the same merge (residual line given). No stale APPROVING names left (control APPROVING_VERDICTS hit).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rd1-29-review-word-one-row-card.md",
      "docs/tasks/specs/reports/20261117-rd1-29-report.md",
      "git diff origin/main...736450f1 (all package files)",
      "ai-packages/qa-factory/scripts/gate_template.py 1-60",
      "ai-packages/qa-factory/scripts/handoff_check.py 953-975, 1995-2050",
      "ai-packages/qa-factory/scripts/report_facts.py 1505-1545, 1608-1630, 3090-3097, 3505-3575",
      "ai-packages/qa-factory/scripts/window_record.py 1600-1608, 1690-1800, 1856-1880",
      "ai-packages/qa-factory/scripts/acceptance.py 1135-1175",
      "ai-packages/qa-factory/scripts/ledger.py 1027-1041, 1176-1192",
      "ai-packages/qa-factory/scripts/selftest.py 295-325",
      "ai-packages/qa-factory/scripts/manifest_put.py 1685-1700",
      "docs/SIBLING_MAP.md 138",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B <wt>/ai-packages/qa-factory/scripts/gate_registry.py --check", "result": "A26 gate registry: no violations, exit=0"},
      {"command": "python -B <wt>/ai-packages/qa-factory/scripts/gate_registry.py --sites | wc -l", "result": "150"},
      {"command": "python Cyrillic scan U+0400-U+04FF over the diff's package files", "result": "ai-packages/qa-factory/scripts/tests/test_case_stamp.py 220 0x430 (only hit)"}
    ]
  }
}
```
