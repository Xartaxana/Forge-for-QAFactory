# t-1349 - critic review of E7-2 (commit 638b1887, branch worktree-u7-e7-2, base c5ec1192)

Verdict: NEEDS WORK (rule 6 words). In the dispatch's words: ACCEPT WITH FIXES, but two findings block the merge. B1 is a
one-line code fix in `app_card.py`. B2 needs no code change: it is a merge-order condition. Everything else in the commit is
correct. Per critic rule 23 the JSON block says `blocker` because a finding blocks; failure_class: code (B1) / order (B2).
Accepting the work is the Lead's decision, not mine.

## Blockers

**B1 - On a project with two or more stands, the walk card never carries the `- Another instance` line (the spec's one-road
invariant is broken; P31, Q12).**
- Where: `scripts/app_card.py::_stand_lines` calls `BP.manual_stand_lines(task_root, project, cfg, [], "", None)`. It passes `""` as
  `env_name`. The manual brief passes `pipeline.environment` (`brief_pack.py` ~4708).
- What goes wrong: with an empty name, `_stand_pick` returns `said = "- Stand: not named in pipeline.json"` whenever the config has
  more than one row, even when `pipeline.json` does name the stand. The `else` branch that appends `instance_lines` (brief_pack.py:2948)
  never runs.
- Reproduction (scratch `e72.py`, real `PK.record`): config `environments=[A, B]`, `pipeline.json {"environment": "B"}`, a yes
  recorded for B.
  - `manual_stand_lines(..., "B")` -> `["- Another instance on B: allowed (the person's answer, given in S-1 on 2026-11-18)"]`
  - `app_card._stand_lines(...)` -> `['- Stand: not named in pipeline.json']`, with no instance line.
- What a person sees: on a two-stand project the walker of every later story never sees `allowed`, so it records the need again.
  On the driver road (3b) the answer is already known, so S7 does not ask. The need is newer than the answer, so no re-walk is owed.
  Delivery says "the person allowed it, but the runner could not start one", although the person said `start it` "now and in later
  stories". This is the safe direction (nothing starts unasked), but the person's answer is starved on one road. The spec's edge says
  "the line in both roads' stand text (INV: one road, P31)", and L8 says "its runner brief says `allowed`".
- Cause: the stand pick of the card predates this commit; the lessons line has the same gap. This commit makes it carry an answer the
  person was promised is honoured.
- Fix (inside owns, ~2 lines): pass the story's environment, e.g.
  `str((_read_json(task_root/"pipeline.json") or {}).get("environment") or "")` through the card's existing JSON reader, in place of
  `""`. Add one card row to `ss1_11_stand_lessons` with two stands. This also corrects the false "not named in pipeline.json" line on
  the card.

**B2 - Against origin/main plus this branch, the page's last sentence ("The factory asks the person once and remembers the answer") is
false on the driver road (A3).**
- Evidence: `grep -rln "s7_extra_instance|extra_instance_outcomes|extra-instance.json" <worktree>/scripts` finds nothing. Branch
  `worktree-u7-e7-3b` points at c5ec1192 (no commits of its own). `merge-base --is-ancestor` shows 3a in origin/main and no 3b commit.
- Why it matters: merged now, the page and help start telling runners to record needs, and the driver's S7 asks nobody. That is the
  window spec §3 rules out by its order (E7-1 -> 3a -> 3b -> E7-2: "the flag is in no page and no help until E7-2").
- Remedy: no code change. Merge E7-2 only after E7-3b is on origin/main (rebase, then re-measure role-load if the base moved). The
  ordering is the Lead's to decide.

## Fixes before merge (non-blocking)

- **F1 - The skill twin leaves out the story-only and stop worlds of §2.4/§2.5** (`skills/qa-story/phases/s7.md:17`).
  - When `project_knowledge.py instance` refuses (no stand chosen, or a story that leaves no trace: `cmd_instance` -> `_story_stand` /
    `_write_prologue` refusal), the page does not say what follows. The driver keeps the answer for this story (`extra_instance_held`)
    and uses the story-only lead ("Your answer holds for this story only").
  - On the skill road the yes is then not recorded. The rework runner's brief shows no line, or `not answered yet`, so the runner does
    not start an instance and records the need again. The next S7 entry finds "no answer" in `show` and asks again. A person feels
    this as being asked twice.
  - `stop` has no stated effect (driver: nothing recorded, the question is held).
  - Add one clause for each.
- **F2 - The `(date not known)` edge (plan review E7-2 (b)) has no row.** The behaviour is correct (my reproduction, below). The test
  never reaches the branch.
- **F3 - Three of the four states have rows on the manual brief only.** `no`, `revoked` and `unreadable` are checked at `[0]`, the
  manual brief, and never on the card (`instance_row(...)[1]`). The card only filters by prefix, so the `yes` row (`manual == card`)
  carries it today. Spec Tests asks for both carriers per state: compare the full tuple, as the `none` row does. This costs no
  extra lines.

## Notes

- N1 (A6): the role-rules anchor `instance of the stand or device` appears exactly once in `agents/qa-runner.md` (count 1, both
  case-sensitive and case-insensitive), so it pins this bullet. It pins the topic, not the rule: deleting "if it says not allowed, or
  says nothing, do not start it" would still pass. A 6-word anchor such as `or says nothing, do not start` would pin the rule. The spec
  named the topic phrase, so this is not a finding against the builder.
- N2 (Q6): the "given in <story> on <date>" clause is a second formatter next to `project_knowledge._lesson_line` (project_knowledge.py
  ~458-460). The two differ on purpose: the date is checked and `(date not known)` is shown. Two cross-module calls of private
  `PK._plain` exist. Minor.
- N3: the outer `except` of `instance_lines` prints `{stand}` raw, not `_plain(stand)`. This path is reached only on an unexpected
  exception. Cosmetic.
- N4 (A5): the skill lead shows `need_why` with no masking (§2.4 / M18: `Driver.masked_words`) and with no cap of 10 cases. The
  skill's "`show` has no answer" makes the conductor apply newest-row-wins by hand: `_newest_answer` counts a revoked newest row as no
  answer, with no fall back to an older live row, and `show` lists both. Lead's call whether to add "(a `taken back` newest row is no
  answer)".
- N5: the E7-1 ordering is as accepted. A row with an unparseable `at` sorts at -inf, so an older parseable row beats it: with a
  revoked older row plus a newer live row with a bad date, the line reads `not answered yet`. That is the safe direction and lies
  outside E7-2.

## Per-key table

| key | answer | evidence |
|---|---|---|
| A1 | holds | `brief_pack.py::instance_lines` reads `PK.instance_answer` only (`_plain` and `INSTANCE_NEEDS` are display/constant); the outer try returns the `could not be read` line. Scratch with real `PK.record`/`PK.revoke`: none -> `not answered yet`; yes -> `allowed (... given in S-1 on 2026-11-18)`; no -> `not allowed (...)`; revoked -> `not answered yet`; `{not json` -> `could not be read (... cannot be read (Expecting property name ...))`; undecodable bytes -> `could not be read (... 'utf-8' codec ...)`; wrong schema -> `could not be read (... schema_version None, not 1)`; untyped value `"yes"` -> `not answered yet`; stand `""` / placeholder -> `[]`. No unreadable or revoked state showed `allowed`. Bad `at` (`garbage`, None, 12345, `2026-13-40`) -> `(date not known)`; empty story is left out (`given (date not known)`). |
| A2 | partial -> B1 | Manual brief: brief_pack.py:2948. Card: `app_card._stand_lines` keeps the prefix. Other roads: the S5 head (`brief_pack.py:4572`, automator/code critic: no runner there); `first_look` (no stand section); the stand-not-selected branch (`said or why`: no line = silence = do not start, safe). A runner on a manual check can be on the walk-card road of a multi-stand project, which has no line: B1. |
| A3 | flags hold; one sentence false on the driver road -> B2 | `manual_evidence.py --help`: `--needs {another_instance}` "the need of a check that wants another instance of the stand or device", `--need-why` "what you would start and why". CLI: `--need-why` without `--needs` is refused; with a need and no walk, `not_walked` defaults to `need_why` (write_unprepared). Walk verdict: `walk_session.py:645-648` closed word; `manual_evidence.py:1725-1729`/`1750-1755` `needs` + `limitation` -> `need_why`, a pass/fail Then refused (NEED_THEN_PROBLEM). `project_knowledge.py instance --help`: `--task --allowed {yes,no} --stand --need --words-file`. `controller.py --help`: `--operation --stage --role --cases --cause {...question_answer...} --words-file --brief`. `show` exists (`ER.command_parser`). |
| A4 | no contradiction | Page line 72 ("Access a person could give is a question") covers access, not starting an instance; line 74 (`env_blocked`) covers a failed preflight or a repeated environment failure. The new bullet is specific and names its own record. Charter line 37 agrees with page line 75 (same closed word, same `limitation`, no pass/fail). Grep (case-insensitive) of the package `*.md` for another/second instance or starting a stand/device: only state-exits rows, changelog, `human-questions.md:100-106` (the stand-not-up question, a different subject). |
| A5 | lead and doors match §2.4; differences -> F1, N4 | The question, the doors and their `says` match §2.4's stand variant almost word for word. The S7 close with no question happens only when an answer exists (yes/no), which matches the driver. Differences a person would feel: F1 (story-only/refused write -> asked again; `stop` unstated), N4 (no masking, no cap). |
| A6 | holds | Anchor count 1 in qa-runner.md; `"needs": "another_instance"` count 1 in walk-charter.md; `test_role_rules.py`: 458 rows, 0 findings. Weakness: N1. |
| A7 | holds | `role_load.py --role qa-runner --json`: `tokens 19065`, `process_tokens 17456` = the new rows. Base process row 17247 (slack 0) + 209 = 17456; base total measure 18856 (row 18906 sat 50 above, within slack 1000) + 209 = 19065. The raise is named in the commit (AR-20). |
| A8 | partial -> F2, F3 | Rows: none (both carriers), yes (both, `manual == card`), no / revoked / unreadable (manual only), no stand (formatter). No `(date not known)` row. The wrapper asserts on `harness.RESULTS[n:]` only (`check` appends `(ok, name)`, harness.py:115-116). Budget: test +22 vs product +33 (`brief_pack` 29, `app_card` 1, `manual_evidence` 3): within. |
| A9 | none outside | numstat: 10 files, all on the dispatch's list (qa-runner.md, walk-charter.md, s7.md, brief_pack.py, app_card.py, manual_evidence.py (two `help=` values plus the comment), role-load.json, role-rules.json, test_brief_pack.py, changelog fragment). |

## Standing questions (diff gate)

- Q1 fit: Work (1), (2), (3), (5), (7) are verbatim. The (5) anchor was shortened (N1). Edges hold except "both roads" (B1).
- Q2 builder's decisions: the `(date not known)` wording and the dropped empty story are safe.
- Q3 seams: app_card's prefix tuple is additive; the s7.md line is inserted before "Analyst"; nothing is reordered.
- Q4 class: siblings in the spec's line. `stand_lesson_lines` sits beside it (correct). The `app_card` prefix is done but the card's
  stand pick is wrong (B1). `_stand_pick` vs `stand_gaps.stand_name`: on a multi-stand project the card's empty name is a third reading
  (B1).
- Q5 tests: (a) the rows would catch a `could not be read` -> `allowed` slip and a missing card prefix. (b) Expected values trace to
  Work (3). (c) F2, F3. (e) no duplicates. (g) no new file.
- Q6 DUPLICATION AND CONSISTENCY: N2 (given-clause formatter next to `PK._lesson_line`). The reader is reused (`instance_answer`).
- Q7 CODE QUALITY: `instance_lines` is 28 lines, nesting 2. No dead branches, and no misleading names or annotations (one exception: N3 cosmetic).
- Q8 hygiene: LF kept (CR count 0), no Cyrillic in the added lines, `selftest.py --limits` PASS.
- Q9 ratchets: role-load `ratchet_tokens.qa-runner` 18906 -> 19065 and `process_ratchet_tokens.qa-runner` 17247 -> 17456 are named in
  the commit (AR-20) and equal the measured values. No other ratchet row changed.
- Q10 ARCHITECTURE: AR-13 (one reader) holds. AR-19 (the skill twin) is present with the F1 gap. AR-20 holds. VARIETY: a multi-stand
  project breaks on the walk road (B1): the person's answer does not reach the walker, and nothing blocks or silently defaults to
  starting.
- Q11 JUDGMENT: none. A formatter and role text; no census row, no scan constant, no craft marker added.
- Q12 ONE ROAD: B1 (a multi-stand project's walk road is outside the line). Grepped for language/runner/project names in the added
  lines: none.

## Trail

- Read: spec r2 §0-§2.8 and the E7-2 card (lines 31-230, 400-449); plan review t-1307 M2/M11/Q6/Q12 lines; full diff
  `git -C <wt> -c core.quotepath=false diff -M origin/main...HEAD`; `agents/qa-runner.md` (whole); `references/walk-charter.md`
  (whole); `project_knowledge.py` 440-540, 1134-1300; `brief_pack.py` 2734-2746, 2875-2960, 4550-4580, 4695-4715; `app_card.py`
  140-160, 455-485; `stand_gaps.py::stand_name`; `manual_evidence.py` 1288-1335, 1609-1660, 1720-1760, 2345-2375; `walk_session.py`
  640-660; `environment_record.py::command_parser`; `harness.py` 112-158; `role-load.json` (base and branch rows).
- Ran:
  - `git diff --stat/--numstat`: 10 files, 62+/7-.
  - `python -B tests/test_role_rules.py`: "role-rules: 458 rows, 548 carriers checked, 0 finding(s) ... === role rules: 57/57 ok ===".
  - `python -m pytest tests/test_brief_pack.py::test_ss1_11_stand_lessons -q`: "1 passed in 10.06s".
  - `python -B selftest.py --limits`: "=== qa-factory selftest: 2/2 ok ===".
  - `python -B role_load.py --role qa-runner --json`: tokens 19065, process_tokens 17456, verdict within.
  - `--help` of `manual_evidence.py`, `project_knowledge.py instance`, `controller.py` (tails above).
  - Scratch scripts `e72.py` and `e72b.py` in my temp dir (outputs quoted in A1 and B1).
  - Grep for the 3b symbols: no hit. Positive control: the same grep shape finds `instance_answer` in brief_pack and project_knowledge.
  - `git merge-base --is-ancestor` checks.

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 app_card._stand_lines passes env_name '' to manual_stand_lines: on a project with 2+ stands the walk card shows 'Stand: not named in pipeline.json' and no '- Another instance' line, while the manual brief shows 'allowed' (scratch repro); the person's yes never reaches the walker (spec edge INV one road, P31; L8). Fix: pass pipeline.json environment, plus one card row.",
    "B2 merge-order condition, no code change: E7-3b (s7_extra_instance_step) is not on origin/main; merged now, the page's 'The factory asks the person once' is false on the driver road (spec section 3 order E7-2 last). Merge after 3b."
  ],
  "fixes": [
    "F1 skills/qa-story/phases/s7.md:17 - state the refused-instance world (story-only answer, no re-ask) and the stop door's effect",
    "F2 scripts/tests/test_brief_pack.py ss1_11_stand_lessons - one row for '(date not known)'",
    "F3 scripts/tests/test_brief_pack.py ss1_11_stand_lessons - compare both carriers for the no, revoked and unreadable rows"
  ],
  "class_completeness": "Siblings named by the spec: stand_lesson_lines (beside, fine); app_card prefix filter (done) but the card's stand pick passes '' and starves multi-stand projects (B1); _stand_pick vs stand_gaps.stand_name gains a third reading on the card (B1). Skill twin present (M2) with the story-only/stop worlds missing (F1). Other brief roads: S5 head (no runner), first look (no stand), stand-not-selected (silence, safe).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md",
      "docs/tasks/specs/reviews/t-1307-u7-e7-plan-r2.md",
      "ai-packages/qa-factory/agents/qa-runner.md",
      "ai-packages/qa-factory/references/walk-charter.md",
      "ai-packages/qa-factory/skills/qa-story/phases/s7.md",
      "ai-packages/qa-factory/scripts/brief_pack.py",
      "ai-packages/qa-factory/scripts/app_card.py",
      "ai-packages/qa-factory/scripts/project_knowledge.py",
      "ai-packages/qa-factory/scripts/manual_evidence.py",
      "ai-packages/qa-factory/scripts/walk_session.py",
      "ai-packages/qa-factory/scripts/stand_gaps.py",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack.py",
      "ai-packages/qa-factory/scripts/tests/harness.py",
      "ai-packages/qa-factory/references/role-load.json",
      "ai-packages/qa-factory/design/role-rules.json"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_role_rules.py", "result": "458 rows, 548 carriers, 0 findings; 57/57 ok"},
      {"command": "python -m pytest scripts/tests/test_brief_pack.py::test_ss1_11_stand_lessons -q", "result": "1 passed in 10.06s"},
      {"command": "python -B scripts/selftest.py --limits", "result": "2/2 ok"},
      {"command": "python -B scripts/role_load.py --role qa-runner --json", "result": "tokens 19065, process_tokens 17456, within"},
      {"command": "scratch e72.py / e72b.py (real PK.record/revoke)", "result": "all registry states as spec; unreadable and revoked never allowed; two-stand card has no instance line (B1)"}
    ]
  }
}
```
