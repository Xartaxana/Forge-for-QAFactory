# Re-review t-1012: the fix round of the P1-b landing (CR-L)

Under review: only the fix diff. That is `6819c66d..7bfc5889` (t-1006, 14 files, +488/-352), plus commit 400cab76 (F1, F3) and commit 5c2e81d6 (F4), in worktree `.claude/worktrees/fvf3`. The worktree is at HEAD 5c2e81d6, which equals `origin/pile/live-run-fvf/batch-3`. Merge 70a9f9ac is not under review. The landing itself was not re-reviewed (cost gate). The verdict the fixes answer is `docs/tasks/specs/reviews/20261117-p1b-landing-code-critic.md`. The DoD comes from the dispatch: every CR-L finding is closed in this round; the ratchets only move down; texts stay byte-identical through D3/D4; an empty or absent input keeps its present behaviour.

## Verdict

**fit_with_fixes. There are no blocking findings.** All 18 CR-L items are closed, and every mechanical claim reproduced. I found one small behaviour drift in the Q2 split (N1, at `run_exit_row`). Three items are class or quality leftovers: N2 (the D3 class is incomplete), N3 (two helpers make the same ask record) and N4 (the `what` key is required but undocumented). N5 answers K8. All five are one-line fixes for one fresh builder round. Accepting the work is the Lead's decision.

## K1: CR-L findings, one by one

| item | status | evidence |
|---|---|---|
| B1 | closed as asked | I re-ran `tools/lint_ratchet.py --check` in fvf3: `76 findings, 76 in the baseline, 0 new, 0 stale`. No baseline raise. The 5 lines are gone: `known` in `judge_group`, `import types`, `moves = NM.move_rows`, the f-prefix, and `import dry_stub` in `main_pass` (diff hunks). |
| B2 | closed as asked | The `driver-layers.json` row is swapped to `dry_driver.py`/`main` with count 1. Re-run `test_driver_layers.py`: `283/283 ok`. |
| B3 | closed as asked | `test-layers.json` keep row `test_scenario_dry_1.py` now covers `tests/harness.py`. I did not re-run `test_selftest_slow_tests.py` (slow); the canon judges it. |
| F1 | closed as asked | 400cab76: the finding names both fields (`probes.runtime_provenance`, `handoff_check.py:551`), carries the estimate label, and item 4 has a second table row. |
| F2 | closed as asked | The form-rounds row's `raised_by` now starts with `product gap: `. |
| F3 | closed as asked | The L1 report gains a section "FR pass of the landed n2f/n2g content" with one line each for C, D and G, plus the tests-over answer. 30 of 32 commits carry no `tests-over:`, the L1 merge 8011b58b included. That is the landing's own, not this round's; see K7. |
| F4 | closed as asked | 5c2e81d6 has an axis block (38 lines), a `tier:` line and the four questions. K6: the two member lists match. |
| F5 | closed | I re-ran `tools/dup_ratchet.py --check`: `scripts: 9 groups, 8 known, 0 new, 0 grown, 1 carried, 1 shrunk/gone (1 diverged)` and `tools: 16 groups, 16 known, 0 new, 0 grown`. This is byte-equal to the builder's witness. |
| F6 | closed as asked | The `selftest.py:115-117` comment states the stop at S5 and the measured 138.0 / 210.8 / 304.8 s. |
| F7 | closed as asked | `witness_for` now matches folders. Two rows were added to `test_scenario_walk.py` (`x` covers it; `xy` does not). Re-run: `95/95 ok`. `--witness-for .../driver-exits/s5.json` now gives `keep test_scenario_dry_1.py`. The control `driver-exitsX/a.json` still falls to the whole layer. |
| D1 | closed as asked | There is one `dry_stub.cut` (now `str(text)`). `dry_exits._cut` and `dry_world.cut` are deleted. K3 lists every call. |
| D2 | closed as asked | `run_script(..., *, both=False)`. The identity test `run is run_script` is gone. The single call is `run(..., both=True)`. No caller passes a stand-in `run`: `automator_branch(` has 3 hits, and both callers use the default. |
| D3 | closed, but the class is incomplete (N2) | `_record` covers the three automator sites, with key order and text identical. `_append` covers both spies, and the stderr texts are byte-identical (`the price key {key!r}` / `the route` slot into the same sentence). The same account is still written a fourth time in `dry_stub._step`. |
| D4 | closed, one edge open (N4) | The `what` field is in the one row, and the one reader `form_filler._spread_world_rows:481` changed in the same commit. The text is identical for the existing row (`probe record`). |
| Q1 | closed | Same as B1. |
| Q2 | closed, with one drift (N1) | After the split the functions measure (AST): `walk_row_problems` 25, `judge_row` 37, `fill_role` 64, `drive_main` 71, `main_pass` 41, `walk_exits` 67, `run_exit_row` 78 lines. K2 walks the branches. |
| Q3 | closed as asked | `census` → `census_data` in `exits_part` (3 sites). |
| Q4 | closed as asked | The closing `}` of `known_red.json` is on its own line. |

## K2: Q2, is behaviour preserved?

Selftests I re-ran in fvf3: `dry_exits selftest: 154/154 cases`, `dry_stub --selftest: 189/189 ok`, `dry_exits --check: 0 discrepancies`, and the matching NOTE ratchet lines (live_only 31 above 0, unwalked 227 above 58, all named).

Reading of every moved branch:
- **`walk_row_problems`**: order kept: unknown fields → subject → `start` → expect → answer → seed/stub. The subject refusal used to be `bad(...)` followed by `out[-1] += "; a route, joint or kind id …"`. It is now one string, and the bytes are identical. `runnable` is returned by `_walk_expect_problems` and passed to the answer and seed helpers, as before.
- **`judge_row`**: the two early returns (over_cap, seed not reached) are kept in order. The listed checks still run in `checks` order. An id outside `JUDGE_CHECKS` (C7/C8/C10) yields nothing, as the old `elif` chain did. The always-checks run after the loop, in the old order (K15, route, joint, E18, turns). `put` still cuts at 300. `changed` is still passed to every `Outcome`. Each `_check_*` returns exactly the old `(status, detail)`, and its `if` order matches the old `elif` order.
- **`fill_role`**: order kept: form → window-1 grounding → automator → S1 steps → outputs → after-steps → `--fix`. The old double guard (`ROLE_STEPS … if stage == "S1"` and `stage == "S1" and role in ROLE_STEPS`) is now `if stage == "S1": _s1_steps` with `if role in ROLE_STEPS` inside, which is equivalent. `_step` builds the old dict `{"output", "why"}` with the old text. The `command:` branch names `kind[8:]`, which is the script name, as before.
- **`drive_main`**: `_turn_carriers` returns `class_seen` from its own local copy. The run-class failure and the carrier exception both still break with the old `stop` text. Overwriting `stop` with `""` is safe, because `stop` is always `""` at that point of a turn: every earlier assignment is followed by `break`. `_answer_took` keeps the old condition, the `unchanged` reset to 0, the once-only details note (2400) and the stop at 3. The conductor (6000) and no-answer (1600) texts are unchanged through `_details_text`.
- **`main_pass`**: order kept: ledger lines → stop line → stub gaps → snapshots → closing. `total` is still taken after the snapshot lines, because the argument is evaluated at the call.
- **`walk_exits`**: `_row_not_run` is the old closure, verbatim. `_run_judged_row` keeps the scoreboard note/fail split, the class only for C4, and the carrier FAIL text (`{row['id']}` equals `rid`; cut at 300). The `say` lambda is called synchronously inside the loop iteration, so `rid` binds correctly.
- **`run_exit_row`**: there is ONE drift, N1 below. The C9 block is unchanged: `_rework_facts` computes `stage` from `ask`, which is non-None there because the condition already calls `ask.get`.

**N1 (fix): the author dispatch of the first ask changed at one edge.** Before the split it was `author_hashes(copy, str(ask.get("dispatch") or ""))`. It is now `_ask_of(copy, record, …, dispatch=ask.get("dispatch"))`, and inside `_ask_of` a `dispatch` of `None` means "read the record's own dispatch". The pending ask always carries the key `dispatch` (`driver_dialog.py:319-320`, `"dispatch": person.dispatch`), and it can be `None`. When it is, the new code reads `questions[-1]["dispatch"]` instead of `""`. The two values differ whenever the last question record is not the pending ask's own. That happens on a deferred re-ask (`driver_dialog.py:549` restores `asked` and appends no record), or when `judge_own_question` returned early without writing the record (`driver_dialog.py:407-409`). Probe, with `author_hashes` stubbed to echo its argument and the record `{"dispatch": "S5-qa-code-critic-1"}`: `_ask_of(None, rec, [], dispatch=None)` → `A:S5-qa-code-critic-1`; `dispatch=""` → `A:`; the old formula → `A:`. The impact is the C5 loop key (`loop_problem` over author/form hashes) on that edge only. No selftest covers it.

## K3: D1, the limit of every former `cut` call

Old `dry_world.cut` defaulted to 300, old `dry_exits._cut` to 300, and `dry_stub.cut` to 400 (unchanged). Here is each former call against the new one, from `git show 6819c66d:` and the new tree:
- `dry_world`: `gate_ready` 200/200 → 200/200; `scoreboard` `cut(exc)` (300) → 300; C3-details 2400 → 2400; conductor 6000 → 6000; no-answer 1600 → 1600; first_ref `cut(first_ref)` (300) → 300; stub-wrote 300 → 300; live_only 80/400 → 80/400; stub-fix 500 → 500; `run_seed` 400 → 400; `walk_exits` stop 200 → 200; row carrier `cut(exc)` (300) → 300.
- `dry_exits`: seed detail `_cut(...)` (300) → 300; `put` `_cut(detail)` (300) → 300.
- No bare `cut(` or `_cut(` is left in `dry_world.py` or `dry_exits.py`, which the grep confirms; the same grep found all 15 old calls in the old blobs. Nothing outside these files called the deleted helpers (case-insensitive grep over `ai-packages`, `tools`, `docs`; the only hits are old reports and the CR-L verdict).

**No call's effective limit changed.** The added `str(text)` in `dry_stub.cut` does not change the output for text input. It lets an exception object be cut, which the old copies already did.

## K4: D2, D3, D4

- **D2**: with `both=True` the text is `(stdout or "") + (stderr or "")`, which is byte-equal to the old `run_script_both`. The default stays `stderr or stdout`, and the timeout text is unchanged.
- **D3**: `_record`. The live_only dict is built as `{"output"[, "case"]}` and then `why`, so the key order is the old `output, case, why`. The fragment row is `output, why`, as before. The texts are `"{why_head} exit {code}: {cut(text)}"` with `why_head` equal to the old literal (`manifest_from_tests.py`, `manifest_put.py`, `manifest_put.py (story fragment {at})`). `_append` keeps the mkdir, the append and the OSError text exactly.
- **D4**: an absent `what` → `KeyError: 'what'`, a traceback, on the empty-folder branch only (`form_filler.py:481`). With files present the key is never read. This is the same contract strength as `root`/`dir`/`glob`, which `world_list` already indexes directly (`form_filler.py:451-457`), and today the file has exactly one row and it carries `what`. So it is no regression, but the row shape gained a required key that the file's `_about` text does not name (N4).

**N4 (fix, docs of the data row):** the `_about` of `form-fill-rules.json` describes `world_list_tokens` rows as `dir` / `root` / `glob` and does not mention `what`. Whoever adds the next token row has no hint, and the empty case then crashes instead of returning `Unfillable`.

## K5: F7 and how wide the folder match is

- Prefix confusion is tested (`fixtures/x` covers `x/a.json`, not `xy/a.json`).
- **A file entry treated as a folder**: `"z.py".rstrip("/") + "/"` is `z.py/`, and no real path starts with that. Harmless.
- **Trailing slash**: handled by `rstrip("/")`.
- **Windows separators**: changed paths are normalised by `_relative` (`replace("\\", "/")`, `scenario_walk.py:864`). I checked the covers entries with a script over all 4332 entries of `test-layers.json` keep rows: 0 contain a backslash, and 0 are empty or only `/`.
- The one remaining over-wide form is a theoretical empty `""` cover. It would yield the prefix `/` and match an absolute POSIX path given outside the package. None exists, so this is not a finding.
- Folder entries that now take effect: 5. They are `driver-exits` plus the 4 story folders, and the story folders were already matched by the story-folder rule. No other keep row widened.

## K6: F4, member lists

Diffed from the `git show 5c2e81d6` hunks. Axis 18 «The members» adds:
1. `driver-exits/<group>.json` `ratchet` (`unwalked` / `live_only` / `after` / `hook_layer`, one `raised_by` per raise);
2. `driver-exits/known_red.json` with `pins.known_red`;
3. `stories/dry-1/selftest/known_red.json`.

Brief question 9 adds the same three, with the same paths and the same four ratchet keys. The map adds one descriptive clause (both ledgers are read through `known_red.py`, and a row leaves when green). That is a property, not a member. **The lists are the same.** Both files exist on disk (`ls` of `driver-exits/` and `stories/dry-1/selftest/`).

## K7: new defects, duplication, quality, and what the canon must still judge

**N2 (fix, D3 class completeness, rule 5/14).** The surface is "the account of one command's exit in a stub row". `dry_stub._step` (`:748`) still writes `(row["wrote"] if code == 0 else row["live_only"]).append(out if code == 0 else {"output": out, "why": f"{script} exit {code}: {cut(text)}"})`. That is the same account `_record` keeps (with `case=None` it builds the identical dict `{"output", "why"}` and the identical text). So the round leaves two helpers for one account. Grep: this is the only remaining copy of `row["wrote"] if code` across `dry_*.py`.

**N3 (fix, duplication inside the round).** `dry_world._record_ask` (`:103-110`, used in `drive_main`) and `_ask_of` (`:1213`, used in `run_exit_row`) build the same `{"ask": dict(record, offered=…), "author", "form"}` record. `_record_ask` differs only in reading `offered` from `driver-state.json` first. The clone ratchet does not see it because it is below the size threshold.

**Duplication and consistency (item 6):** N2 and N3. Searched by: grep `row\["wrote"\] if code` over `dry_*.py`; grep `author_hashes(` over `dry_world.py`; grep `cut(` / `_cut(` (K3); `dup_ratchet --check`, re-run green, 0 new.

**Code quality (item 7):** N1 (the `None` sentinel conflates "not given" with "given as None") and N4. Also N5 below: the split multiplied function-local `import dry_exits` in `dry_world.py`, which now has 9 such sites (`:801, 812, 849, 1000, 1105, 1230, 1329, 1344, 1368`).

**One road (item 12):** none found. `both=` is a parameter of the one runner, not an exclusion of a language or project. The identity test `run is run_script` is gone.

**Tests (question 5 / rule 20):** the round adds 2 rows to an existing table (`test_scenario_walk.py`), one positive and one negative of one behaviour. 7bfc5889 carries a `tests-over:` line with its reason. Within budget.

**Left for the batch canon and the Lead:**
- **Canon 44016099937 is in progress.** I read the start job: `git checkout … refs/remotes/origin/pile/live-run-fvf/batch-3` → `5c2e81d60a8f…`, which is the head under review. Note that `ci_read pipelines` prints main's sha 5751426c for this run.
- **forge-check is red on `pytest tools/`**: `test_hygiene_gate` `git-checkout-on-a-dirty-tree`, and `test_mechanism_gate` `tools/usage_report.py` outside the net. Main's push run 44016081519 fails with the same two (`ci_read why`). The branch touches no `tools/` path.
- **package-fast is red** on `test_contract_slices` K10p (`handoff_check:findings_tooling` writers) and `test_detector_verdict` t4a (`PT-plugin-read` text hash). No branch path touches these. I grepped `contract_slices|detector_verdict|guard|handoff_check|references|slices` over `git diff --name-only origin/main...branch`: 0 hits, with a positive control of 34 `scripts/tests/` paths. Whether main is red on the same two is an estimate, not verified: I did not read main's own package-fast for that sha.
- **Still owed from CR-L fix 9:** CI runs of `--part exits:s0` / `exits:s1-s4`. `walk_exits` / `run_exit_row` / `_run_judged_row` (and N1) execute only there, and the default canon does not run them.
- **The landing's own `tests-over:` gap** (F3's answer): 30 of 32 commits, the L1 merge 8011b58b included, carry none. The Lead decides whether the merge into main carries a `tests-over:` line. This is outside this round.
- The fvf3 worktree has an uncommitted `docs/OWNER_PRINCIPLES_INDEX.md`, which is not part of the diff. I did not touch it.

## K8: the builder's reported analogs

- **Function-local imports in `dry_world.py`: fix now (N5).** `dry_exits` imports only the stdlib at module level (`dry_exits.py:20-28`; its own heavy imports are lazy, and it imports `dry_world` only inside selftest functions `:2353-2409`). So one top-level `import dry_exits  # noqa: E402` next to `import dry_stub` creates no cycle and removes 9 local imports that the split multiplied. Leave `known_red` and `scenario_walk` local; that is outside this ask.
- **The repeated `row["wrote"] if code == 0 else row["live_only"]`: fix now (N2).** It is the D3 class itself: one copy is left in `_step`, and `_record` already holds the identical account.

## Fixes (one fresh builder round; witness: `dry_stub.py --selftest` 189/189, `dry_exits.py --selftest` 154/154, `tools/lint_ratchet.py --check` 0 new, `tools/dup_ratchet.py --check` 0 new)

1. **N1:** `dry_world.run_exit_row`: replace `dispatch=ask.get("dispatch")` with `dispatch=str(ask.get("dispatch") or "")`. Witness: the probe above gives `A:` for a `None` ask dispatch.
2. **N2:** `dry_stub._step` body becomes `code, text = run_script(project, script, argv)` / `_record(row, code, text, out, script)` / `return code, text`.
3. **N3:** `dry_world._record_ask` keeps its `offered` read and returns `_ask_of(world, q, offered)`. The output is the same: `offered` from JSON is a list or `[]`, so `list(offered or [])` is equal.
4. **N4:** add to the `_about` of `form-fill-rules.json`, inside the `world_list_tokens` clause: "`what`: the name of the file kind the empty-folder refusal names (e.g. `probe record`), required like `root`, `dir`, `glob`".
5. **N5:** `dry_world.py`: add `import dry_exits  # noqa: E402` after `import dry_stub` at the top and delete the 9 function-local `import dry_exits` lines.

## Trail

- **Read:** the CR-L verdict (whole); `git diff 6819c66d 7bfc5889` per file (`dry_stub.py`, `dry_exits.py`, `dry_world.py` whole hunks; the 11 small files); `git show 400cab76`, `git show 5c2e81d6` (message and hunks); new `dry_exits.py` 1036-1130, 1325-1390; new `dry_world.py` 896-925, 1120-1135, 1226-1300; `scenario_walk.py` 863-925; `form_filler.py` 440-482; `driver_dialog.py` 305-335, 405-420; the import lines of `dry_exits.py`, `dry_stub.py`, `dry_world.py`.
- **Re-runs (fvf3, HEAD 5c2e81d6):** listed in the json block.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "N1 dry_world.run_exit_row: replace dispatch=ask.get(\"dispatch\") with dispatch=str(ask.get(\"dispatch\") or \"\") so a None pending-ask dispatch keeps the old empty author source instead of falling back to questions[-1] (deferred re-ask, unwritten record)",
    "N2 dry_stub._step body: code, text = run_script(project, script, argv); _record(row, code, text, out, script); return code, text (the last copy of the D3 account)",
    "N3 dry_world._record_ask: keep the offered read from driver-state.json, return _ask_of(world, q, offered) (one ask-record builder)",
    "N4 form-fill-rules.json _about, world_list_tokens clause: name `what` (the file kind the empty-folder refusal names, e.g. probe record), required like root, dir, glob",
    "N5 dry_world.py: one top-level import dry_exits (noqa E402) after import dry_stub; delete the 9 function-local import dry_exits lines (dry_exits imports only stdlib at module level, no cycle)"
  ],
  "class_completeness": "D3 class (the account of one command exit in a stub row): 3 automator sites and 2 spy sinks closed; one copy left in dry_stub._step (N2). D1 class (cut helpers): closed, 15 old calls enumerated with unchanged limits, no external caller. F7 folder covers: one matcher; 5 folder entries in 4332, none empty or with backslash. Axis 18 / brief question 9: the member lists are equal (3 members each). The ask-record builder class: two helpers in dry_world (N3).",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/20261117-p1b-landing-code-critic.md whole",
      "git diff 6819c66d 7bfc5889: dry_stub.py, dry_exits.py, dry_world.py, dry_driver.py, selftest.py, form_filler.py, scenario_walk.py, test_scenario_walk.py, test_scenario_dry_1.py, test-layers.json, driver-exits/known_red.json, driver-layers.json, form-fill-rules.json, form-rounds.json",
      "git show 400cab76 and 5c2e81d6 (message, hunks of SIBLING_MAP.md axis 18 and critic-diff-brief.md question 9)",
      "new dry_exits.py 1036-1130, 1325-1390; new dry_world.py 896-925, 1120-1135, 1226-1300; scenario_walk.py 863-925; form_filler.py 440-482; driver_dialog.py 305-335, 405-420"
    ],
    "reruns": [
      {"command": "python -B tools/lint_ratchet.py --check (fvf3 root)", "result": "76 findings, 76 in the baseline, 0 new, 0 stale"},
      {"command": "python -B tools/dup_ratchet.py --check (fvf3 root)", "result": "scripts: 9 groups, 8 known, 0 new, 0 grown, 1 carried, 1 shrunk/gone (1 diverged); tools: 16 groups, 16 known, 0 new, 0 grown"},
      {"command": "python -B scripts/tests/dry_exits.py --selftest", "result": "dry_exits selftest: 154/154 cases"},
      {"command": "python -B scripts/tests/dry_stub.py --selftest", "result": "dry_stub --selftest: 189/189 ok"},
      {"command": "python -B scripts/tests/test_scenario_walk.py", "result": "95/95 ok"},
      {"command": "python -B scripts/tests/test_form_selftest.py", "result": "26/26 ok"},
      {"command": "python -B scripts/tests/test_driver_layers.py", "result": "283/283 ok"},
      {"command": "python -B scripts/tests/dry_exits.py --check", "result": "0 discrepancies; NOTE ratchet live_only 31 above base 0 and unwalked 227 above base 58, all named"},
      {"command": "python -B scripts/tests/scenario_walk.py --witness-for .../driver-exits/s5.json .../driver-exitsX/a.json", "result": "s5.json -> keep test_scenario_dry_1.py; control driver-exitsX/a.json -> whole scenario layer"},
      {"command": "scratchpad probe: dry_world._ask_of with author_hashes stubbed, record dispatch S5-qa-code-critic-1", "result": "dispatch=None -> A:S5-qa-code-critic-1; dispatch='' -> A:; old formula -> A: (N1)"},
      {"command": "scratchpad script over test-layers.json keep covers", "result": "4332 entries; 5 folder entries; 0 empty, 0 backslash"},
      {"command": "scratchpad AST sizes of the Q2 functions", "result": "walk_row_problems 25, judge_row 37, fill_role 64, drive_main 71, main_pass 41, walk_exits 67, run_exit_row 78"},
      {"command": "python -B tools/ci_read.py pipelines; jobs 44016099937; log 133814322441 (checkout); log 133814322817 --tail; log 133814511341 --grep FAIL; why 44016081519", "result": "canon in progress on 5c2e81d6 (checkout line); forge-check red on tools tests also red in main push run 44016081519; package-fast red test_contract_slices K10p, test_detector_verdict t4a, no branch path touches them"},
      {"command": "git merge-base --is-ancestor 5751426c origin/pile/live-run-fvf/batch-3", "result": "NOT-ancestor (the sha ci_read prints is not the run's checkout)"}
    ]
  }
}
```
