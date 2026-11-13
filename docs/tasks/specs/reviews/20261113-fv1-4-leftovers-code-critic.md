# Code critic — FV1-4 leftover cuts, nodes L1, L2, L3+L4, L5 (one pass for the topic)

Spec: `docs/tasks/specs/20261113-fv1-4-leftover-cuts-spec.md` (Lead forks F1-F7 = a; F6 became L5). Base f988794.
Trees: L1 `.claude/worktrees/fv14-l1` e4a6d88; L2 `fv14-l2` f3b3b78; L3+L4 `fv14-l34` 8dffab3 (f789896, 1724840); L5 `fv14-l5` 2e9d646.

## Verdict

**NEEDS WORK — fit_with_fixes. Blocking findings: 0. Non-blocking: 4 to fix before merge (F1-F4), 5 for the queue (Q-A…Q-E), 1 topic-level red the Lead owns (R3).**

| Node | Verdict |
|---|---|
| L1 | accept — every §3 row C1-C22 applied or kept as written; no value left cut by characters |
| L2 | accept with fixes F1, F2 (a docstring that now lies; one row not red-before) |
| L3+L4 | accept — edges met; a process note on how the edit was made (P-1) |
| L5 | accept with fixes F3, F4 (stale docstring; the sibling line, Q4 answer) |

## Findings

**F1 (L2, fix before merge).** `fv14-l2/.../scripts/brief_pack.py:1699-1703`: the `_words_block` docstring still says the multi-line form holds "the words as given (CRLF -> LF only)" and that wrapping happens only with "no line break and longer than the width". After L2, a long line of a multi-line text is wrapped too (`:1709-1714`). The name lies to the next reader. Fix: one clause, "a line of either form longer than the width is wrapped (`_wrapped`), and the head ends WORDS_WRAPPED_NOTE".

**F2 (L2, fix before merge).** `fv14-l2/.../tests/test_brief_pack.py:1893-1897` Q1-BACKTICK-RUN never asserts that the wrap happened. On the base, the 1 505-character line stays whole, so `"".join(body[1:]) == ticks` and "no body line equals the fence" both hold trivially. That is why the row is green on the base. The builder's reason ("cannot be red") is wrong for this row: it could be red-before, and the spec asks for that (DoD (1)). Fix: add `len(body) > 2` (or `"<decisions>" in entry[0]`) to the compared tuple. After the change the row then proves the fence survives an ACTUAL split (E5).

**F3 (L5, fix before merge).** `fv14-l5/.../scripts/report_facts.py:937-938`: the docstring still shows the line as `..., +K more; they are left in place.` It should be `+K more: state/created-accounts.json;`.

**F4 (L5, fix round, the sibling).** `report_facts.py:984` `unconfirmed_accounts_line` ends with a bare `, +K more`. That is the topic's class (a count cap that names no place). Fix in the same fix round — form per Q4 below. Update the pin `tests/test_account_word.py:299-312` (`test_unconfirmed_line_at_5_and_6_names`) in the same round.

**R3 (topic-level, owned by the FV1-4 topic, not by these nodes).** `test_audit_rules.py` is 367/375 on the base f988794 (control run below). Besides the K10-class A22 rows, the base has an **A27 red**. The door `# remains:` at `driver_machine.py:3890` no longer touches its counted site, because the line `note = _answer_note(...)` (a83b5f3, FV1-4 N0) was inserted between them and `notes_args` (ea79861, FV1-4 Q2/Q3) was changed. Result: census 56 vs baseline 55. On origin/main be2c988 the file is 375/375. The L3+L4 builder reported "367/375, not examined". That is a witness gap, but the reds are identical on the base (my run). Owner: FV1-4 N0 / Q2-Q3. Fix before the topic merges: move the door next to the site, or re-door the site. A raise of `NO_MOVE_BASELINE` is not an answer.

**P-1 (L3+L4, process, non-blocking).** The report says `driver_sources.py` was rewritten through a `python -c` payload, and the hygiene hook warned. CLAUDE.md command hygiene point 4 allows file edits only through Edit/Write. The diff itself is three removed slices, read whole by me. For the Lead's calibration log, not a code defect.

## Answers 1-7

**1. Edges and rows per node.**
- **L1.**
  - Rows C1-C22: confirmed by reading the diff. Every `_clip`/`_cut` site became `scrub(x, tokens=<the site's old flag>)`. The flags match E9: notes, test-data value and profile lines keep `tokens=True`; structural fields use `False`.
  - C7 adds a pointer: `; +K more: qa-factory/config.json \`test_data.<key>\``. C12 removes the cap. C6 now runs the secret-name test on the whole key.
  - `FORMAT` goes "1" -> "2" (E7). The docstring `:18-22` is reworded.
  - Edges: E1-E9 each have a row; I read the test diff.
  - No silent cut remains in `app_card.py`. Grep `\[:…\]|clip|truncat|\.\.\."` (case-insensitive) over the file returns only count caps that print `+N … <file>` (`:142`, `:251`/`:274-275`, `:261-262`, `:299-300`, `:327-328`, `:413-420`, `:510`) and the hash `:448`. The positive control is the same Grep: it hits these lines.
  - The quarantined `test_app_card.py`: only `:424` reads `FIRST_LOOK_LINE_CHARS`. The Grep `LINE_CHARS|NOTE_CHARS|_clip|_cut` (-i) hits `:151`, `:179` (names only) and `:424`, which matches the report.
- **L2.**
  - Q1 is implemented exactly as specified: lines are measured as given, a line of exactly 1 000 characters is not wrapped, and the fence is computed before wrapping.
  - Q6: `_Clipped` is the `_Pointer` device. Both `_fl_line` call sites (`:4094`, `:4109`) append the returned object unchanged, so the type survives to `first_look_lines:4135`.
  - Q6-COINCIDENCE is arithmetically right: body length `180 - base_len - 2` gives `text == room`, so the line is not clipped.
  - E8/E9 are met. Grep `_fl_line_clipped` over the L2 package finds nothing; the builder's positive control on the base found `:4027`.
- **L3.**
  - `[:1500]` is gone at `:87`, `:96` (F5 a) and `:142`. The rows M-*/S-* cover both callers.
  - E1 is unchanged. E7: `shown` stays bounded by the question body.
  - Not run by me (`test_story_run_*` is forbidden here). The builder's own scratch run: `46/46`, base `39/46`.
- **L4.**
  - Meets E1-E4. The check runs only when `allowances` is a dict, so E4 gives no second message.
  - `whole()` (`role_load.py:78-79`) refuses bool and float, so `True` and `6144.0` are refused.
  - The absent row is honest: the `settings_doc` fixture (`test_role_load.py:57-60`) holds no `brief` keys.
- **L5.**
  - The path comes from the writer's helper (`created_names_path`). The AT-5/EMPTY rows are guards; AT-6/AT-100 are red before.
  - No test pinned the old tail: Grep `more; they are left` over the L5 package hits only the docstring `:937`, which is also the positive control.
- **Still cut silently inside the nodes' own sites:** only `unconfirmed_accounts_line` (F4).

**2. Base reds (one control run each on a `git archive f988794` copy; the history traced by archive runs).**
- **K10-b and K10-c.** Red at f988794: `169/171`, verbatim lines in the trail.
  - Already red at the main snapshot 1b6c90e, before the topic. The cause is TR4-15 (b700f0f), which grew the qa-failure-analyst slice.
  - Main named the raise in c9f6e02 ("ratchet 18361 -> 18426, process 16322 -> 16401"), but c9f6e02 is not in the base (`merge-base --is-ancestor` says no). On origin/main be2c988 the file is `171/171`.
  - Who owes: nobody new. The topic integrator clears it by merging origin/main. A second raise inside the topic would double-name it.
- **`Driver.take_checks_line`.** Red at f988794: `282/283`.
  - Green at 5c16666, red at 079dc63 (P1-v N0). That commit added `driver_dispatch.py:874 take_checks_line` with no row in `fixtures/driver-layers.json`. Neither is on main yet; origin/main is `283/283`.
  - Who owes: the P1-v N0 node (or its fix round bea0bb0's owner). Add the row before the P1-v line merges. Not these nodes.
- **A27 (R3, found by this pass).** Owed by FV1-4 N0 / Q2-Q3 (see R3).

**3. L2's three rows green on the base.**
- Q1-AT-1000: the reason is right. E2 demands output byte-identical to the base.
- Q6-CUT-AWAY: the reason is right. The base reader also looks only at `lines[:FIRST_LOOK_LINES_MAX]`, so E8 already held.
- Q1-BACKTICK-RUN: the reason is wrong (F2).

**4. L5 sibling `unconfirmed_accounts_line`.**
- There is no single existing reader or line shape for "a list from two files". The package's count tails come in two wordings: `+K more: <path>` (brief_pack, app_card, now L5) and `and K more (<place>)` (C3-8/9 sites, `tests/test_whole_list_sites.py`). Neither has a two-file form.
- A static pointer naming both files is not quite right. `items` is created-first (`:977-981`). With 3 unconfirmed sign-ups and 10 doubts, every hidden item is a doubt, so a fixed two-path tail would send the reader to a file that holds none of them.
- Recommended form, in the L5 wording: count the hidden tail per source and name only the files whose items were cut, each through its own path helper (`created_names_path`, `manual_capture.account_doubts_path:876-880`, `.relative_to(art).as_posix()`). Example: `, +8 more: state/account-doubts.json (8)`, or `, +K more: state/created-accounts.json (i), state/account-doubts.json (j)`.
- Cost: one tuple per item `(text, source)`. This is the Lead's decision.

**5. Remaining cuts, bounded to the touched files and their axis-5 twins** (each verified by Grep plus a read of the line):
- `report_facts.py:205-209` `_person_build_words`: **a person's words cut at `PERSON_WORDS_LIMIT` 120** (`:164`), with an ellipsis and no place (reader `:3444`). This breaks the topic's own rule "a person's words are never cut".
- `report_facts.py:3285`: the person's quoted words, `_cut(…)` at 200.
- `report_facts.py:3246`, `:3250`: `BA.cut` of a branch unit, plus `and k more`. The docstring says the whole is in the ledger's `lines`, but the output names no place.
- `report_facts.py:3879` `_overflow`: names "the factory's record of the checks" in words, with no path.
- `report_facts.py:4082` `_names_shown`: `and k more` with no place. Callers: `:4098`, `:4106`, `:4109`, `:4122`, `:4134`, `:4248`, `:4260`, `:4264`, `:4266`.
- `report_facts.py:869-872`, `:1302`, `:1309`, `:3031`, `:4253`: the designed first-reason `_cut` ("the one truncation the blocks make", `:99-102`). The Lead decides whether it stays.
- `driver_sources.py:363`, `:387`, `:415`, `:450`: a tool's output tail `out[-200:]` printed to the person. The spec's §8.4 names only `:450`; the other three are its siblings.
- `driver_sources.py:594-597` `name_list` `(+K more)` with no file, plus the `GAP_NAME_MAX` byte clip: that is F7, which goes to a finding by the Lead's decision.
- `brief_pack.py:4036` `_fl_line`: names where (`whole:`) but not how much (spec §8.3; T3b).
- `app_card.py`: none. `role_load.py`: not applicable.

Proposal (the Lead opens it, rule 6): one node "report_facts: every cut names where the whole is; a person's words are never cut", covering the first six bullets. Plus the `driver_sources` output tails as a line in F7's finding.

**6. Merge.**
- The four branches share no file. Package files: L1 `app_card.py` and its keep test; L2 `brief_pack.py` and `test_brief_pack.py`; L3+L4 `driver_sources.py`, `role_load.py`, `test_role_load.py`, `test_story_run_refusals.py`; L5 `report_facts.py`, `test_account_word.py`. The changelog fragments and reports have distinct names.
- origin/main has not touched any of these files since the merge base 5c16666 (`git diff --stat` is empty).
- Semantic seam: after merge, the card (L1, C14) shows L5's tail `+K more: state/created-accounts.json`, which is task-root-relative like the card's other pointers. No L1 row pins a created line with more than 5 names, so nothing goes red.
- Queue: `brief_pack.py` is a hot file (L2 before T3b, spec §4).
- The F4 (a) keep-row `why` reword of `test-layers.json:77-84` is the Lead's integration edit. No builder touched it.

**7. Duplication and code quality.**
- **DUPLICATION AND CONSISTENCY:** none introduced. L1 renders through the existing `scrub`. L2 reuses `_wrapped` and the `_Pointer` device. L4 reuses `whole`. L5 reuses `created_names_path`.
  - The two literal note lines `driver_sources.py:87` and `:142` stay twins by the spec's closed choice §7.
  - Pre-existing, outside these diffs: two count-tail wordings (`+K more: <path>` vs `and K more (<place>)`) and no shared tail helper. Grep `def (_?more|_?tail|_?listed|_?counted)\w*\(` over scripts finds about 12 local `_listed`/`listed` functions and no common one. Queue item Q-E: a convergence question, not this pass's.
- **CODE QUALITY:**
  - No new function over 60 lines or 3 nesting levels.
  - Findings: F1 and F3 (stale docstrings), F2 (a row without killing power).
  - The L1 test file adds 350 lines for 74 product lines. The reason is named: the spec's roughly 30-row list.
  - The L1 keep file imports three more helpers (`fl_row`, `headers`, `write_first_look`) from the quarantined `test_app_card.py`. When quarantine deletes that file, the keep file breaks. Queue item Q-D: move the helpers when quarantine is cleared.
  - The L3 row's `except Exception: pass` (`test_story_run_refusals.py`, the S-rows) is acceptable: an early raise leaves `argv` empty and fails loudly at `argv[0]`.

**Standing lines.**
- Ratchets (item 9): no row in any diff. Base reds: answer 2.
- Architecture (item 10): the AR-n named in each commit match spec §1. The L1 and L4 commits say "axes: not a mechanism", while spec §5 calls M1/M4 mechanisms with axis blocks. The blocks live in the spec, so this is non-blocking. Noted.
- Judgment (item 11): no census row moved. L4 stays inside row `:858` (`shape`); the builder ran `test_judgment_census` 24/24.
- One road (item 12): none found. The diffs, read whole, contain no language, runner or project branch.

## Pin changes (old -> new)
- `app_card.FORMAT` "1" -> "2".
- Deleted from `app_card`: `_clip`, `_cut`, `LINE_CHARS`, `LESSON_LINE_CHARS`, `NOTE_CHARS`, `FIRST_LOOK_LINE_CHARS`.
- C7 line: `(names: …)` -> `(names: …; +K more: qa-factory/config.json \`test_data.<key>\`)`.
- Deleted from `brief_pack`: `_fl_line_clipped`; added `_Clipped`.
- `created_accounts_line` tail: `, +K more` -> `, +K more: state/created-accounts.json`.
- `role_load._settings_problems`: + `allowances.brief` / `allowances.brief_charter_head` message.
- Test counts:
  - `test_brief_pack`: 1117/1125 on the base with a stub -> 1125/1125.
  - `test_app_card_stand_lessons`: 1 -> 37.
  - `test_role_load`: 169/171 -> 184/186 (the same two base reds).

## Spot-checks and trail
- Read: the brief; the spec (whole); all four diffs (whole); `app_card.py:340-540` (L1); `brief_pack.py:1670-1733`, `:425-446`, `:1125-1140` (L2); `report_facts.py:900-1009`, `:194-210`, `:3225-3290`, `:3822-3880`, `:4060-4134` (L5); `manual_capture.py:757-760`, `:876-895`; `test_role_load.py:57-80`; `test_account_word.py` tail; `test_whole_list_sites.py:1-40`; the four reports; the commit messages.
- Control re-runs and history (verbatim tails):
  - `pytest fv14-l1/.../test_app_card_stand_lessons.py -q`: `37 passed in 4.72s`.
  - Base copy `test_role_load.py`: `FAIL K10-c …18,426 … over … 18,361`, `FAIL K10-b …16,401 … 16,322`, `=== role_load …: 169/171 ok ===`.
  - Base copy `test_driver_layers.py`: `FAIL driver-layers.json L1 holds on the real family (1 problem(s))`, `=== test_driver_layers: 282/283 ok ===`.
  - Base copy `test_audit_rules.py`: 8 FAIL (A22, A-K1, A22-K4 x2, A27 x3 "driver_machine.py:3890 … census … expected 55, got 56", K15), `=== … 367/375 ok ===`.
  - origin/main be2c988: `role_load 171/171`, `test_driver_layers 283/283`, `audit rules 375/375`.
  - History: `test_driver_layers` 5c16666 `283/283` -> 079dc63 `282/283`. K10 already red at 1b6c90e, 079dc63, a83b5f3, cf4dede, 8207150^1, 8207150. `git log -S take_checks_line` -> 079dc63. `git blame -L 3884,3893 f988794 driver_machine.py` -> `:3891` a83b5f3, `:3893` ea79861.
- Negative claims and their positive controls:
  - "No other count-tail pin": control is the docstring hit `:937`.
  - "`app_card.py` has no character cut": control is the same Grep hitting the count lines.
  - "Main did not touch the nodes' files": control is `diff --stat` over the same paths, which shows c9f6e02's file when given `role-load.json`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 L2 brief_pack.py:1699-1703 _words_block docstring: say a long line of the multi-line form is wrapped too (fix before merge)",
    "F2 L2 test_brief_pack.py:1893-1897 Q1-BACKTICK-RUN: assert the wrap happened (len(body) > 2 or <decisions> in head) so the row is red-before (fix before merge)",
    "F3 L5 report_facts.py:937-938 created_accounts_line docstring: +K more: state/created-accounts.json (fix before merge)",
    "F4 L5 report_facts.py:984 unconfirmed_accounts_line: per-source count naming only the files whose items were cut, through created_names_path and account_doubts_path; update test_account_word.py:299-312 (fix round)",
    "R3 topic FV1-4 N0/Q2-Q3: A27 red at base, driver_machine.py:3890 door separated from its site by a83b5f3/ea79861 (census 56 vs 55); fix before the topic merges, no baseline raise"
  ],
  "class_completeness": "Nodes' own sites: only unconfirmed_accounts_line left (F4). Bounded residuals for a Lead node: report_facts.py:205-209 person's words cut at 120, :3285 quote cut at 200, :3246/:3250 branch units, :3879 _overflow with no path, :4082 _names_shown with 9 callers, first-reason _cut sites :869-872/:1302/:1309/:3031/:4253; driver_sources.py:363/:387/:415/:450 out[-200:] tails (add to F7 finding); brief_pack.py:4036 whole: without how-much (spec 8.3). app_card.py none. Axis 5 card-brief twins C2/C3/C17/C18 render whole.",
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/20261113-fv1-4-leftover-cuts-spec.md",
      "git diff f988794..e4a6d88 (fv14-l1), f988794..f3b3b78 (fv14-l2), f988794..8dffab3 (fv14-l34), f988794..2e9d646 (fv14-l5)",
      "fv14-l1 ai-packages/qa-factory/scripts/app_card.py:340-540",
      "fv14-l2 ai-packages/qa-factory/scripts/brief_pack.py:425-446,1125-1140,1670-1733",
      "fv14-l5 ai-packages/qa-factory/scripts/report_facts.py:194-210,900-1009,3225-3290,3822-3880,4060-4134",
      "fv14-l5 ai-packages/qa-factory/scripts/manual_capture.py:757-760,876-895",
      "fv14-l34 ai-packages/qa-factory/scripts/tests/test_role_load.py:57-80",
      "fv14-l5 ai-packages/qa-factory/scripts/tests/test_whole_list_sites.py:1-40",
      "the four builder reports and five commit messages"
    ],
    "reruns": [
      {"command": "python -B -m pytest fv14-l1/ai-packages/qa-factory/scripts/tests/test_app_card_stand_lessons.py -q", "result": "37 passed in 4.72s"},
      {"command": "python -B <git archive f988794>/scripts/tests/test_role_load.py", "result": "FAIL K10-c, FAIL K10-b; 169/171 ok"},
      {"command": "python -B <git archive f988794>/scripts/tests/test_driver_layers.py", "result": "FAIL driver-layers.json L1 (1 problem); 282/283 ok"},
      {"command": "python -B <git archive f988794>/scripts/tests/test_audit_rules.py", "result": "8 FAIL incl. A27 driver_machine.py:3890, census 56 vs 55; 367/375 ok"},
      {"command": "same three files on git archive origin/main be2c988", "result": "171/171, 283/283, 375/375"},
      {"command": "test_driver_layers on archives 5c16666 and 079dc63", "result": "283/283 then 282/283"},
      {"command": "test_role_load on archives 1b6c90e, 079dc63, a83b5f3, cf4dede, 8207150^1, 8207150", "result": "169/171 at every one (K10 red before the topic)"}
    ]
  }
}
```
