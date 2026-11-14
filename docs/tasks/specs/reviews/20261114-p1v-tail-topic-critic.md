# t-709 critic: P1-v run scoreboard tail (N6, N7, N6b), one pass for the topic

Tree `.claude/worktrees/p1v-n6b` at `79fbbaa` (clean). Spec: run-scoreboard spec §3, §5, §7, §8 (N6/N7 rows, K2/K3/K5); amendment B1 (:516-562), B2 (:564-621), OQ2 (:908-913).

## Verdicts

- **N6** (assemble/compare/norms, X1 row): **fit_with_fixes**. Two blocking findings: B1 (X1 states) and B2 (`compare` reads a range overlap as "not worse").
- **N7** (bar price, release-check): **fit_with_fixes**. One blocking finding (B4, `--lines` passes a needed line), one fix for this round (F5, a second price formula), one proposed node (P1, the bar file has no writer).
- **N6b** (norms/2, K5 ratchet, compare/release-check --release): **fit_with_fixes**. One blocking finding (B3, the owner's word for a ratchet cannot be recorded on any real row), fixes F1-F4.
- **Topic: fit_with_fixes (NEEDS WORK).** 4 blocking findings, 8 fixes for one round, 2 proposed nodes, 2 questions for the owner or the Lead. Lead owes the carrier lines (Q8) before the merge. This verdict is an input to acceptance; the Lead decides.

## Blocking findings

**B1. N6 `scoreboard.py:317-335 price_row`: the X1 states of amendment B1 are not produced.** Control run with `task_price` faked per status:
`agrees -> measured 0.4` (ok); `differs -> state=measured value={low,high}` (B1 asks for `range`); `incomplete -> state=unknown` (asks for `at_least`); `not_cross_checked -> state=measured value=0.4` (asks for `one_source`).
The consequence is real. `release_lines` proposes `can ratchet:` for any `measured` scalar (`scoreboard_bar.py:284-289`), so a one-source price is offered for ratcheting, which B2 and B2-E9 forbid. `at_least` can never give "worse" (B1-E2). The consumer `_element_line` handles `one_source`/`at_least`/`range`, but only on hand-built boards: those states are read and never written (AR-22). The test table `SB_MONEY_CASES` (test_measurers.py:1802-1813) has no `not_cross_checked` row, and amendment N6 rows (1) and (4) are missing.
Fix: map the four statuses to the four B1 states with the B1 value shapes (`{"at_least": low, "note"}`, `{"low","high","note"}`, `{"value", "note": "one source"}`). Add the four status rows plus "`one_source` is never proposed" on a board built by `assemble`.

**B2. N6 `scoreboard.py:628-636 build_compare`: an undecided range reads as "not worse".** Control run, lower is better:
`prev 10, now 10..12 -> worse=False` and `prev 8..12, now 8..14 -> worse=False` (B1 table: `not decided: range`).
`compare --release` judges the same pair as `not decided: range (10..12)`, so the two judges of one table disagree. The opposite also happens: `prev 10, now 7..10` gives compare `undecided` but release `ok`. With `worse=False`, `compare --findings` drafts no finding: an unknown becomes a pass (FR-41, AR-28). X1 `differs` produces such ranges routinely.
Fix: one judge (see F1) used by `build_compare`. Add test rows for these three pairs.

**B3. N6b K5 (`check_norms` + `_ratchet_problems`, `scoreboard.py:439-537`): the amendment's raise form is refused on every real row.** All 11 rows of the shipped `norms.json` carry a `kind`, so their `raises` go through the norm-raise checks. Control runs (`norms --check --against`):
- K5: ratchet 10->11 plus raise `{raised_by, reason, word}` (the amendment form :577) -> `RED: raise 0 (N-questions): from and to must be numbers`.
- K6: the same with `from/to = 40/40` -> `RED: a raise to 40 is not looser than 40`.
- K7: `from/to = 40/41` while the norm stays 40 -> `norms: green`.

So the owner's word for a worsened ratchet can be recorded only by inventing a norm loosening. There is also a pair cross-match (critic rule 15): `_worded(new) > _worded(old)` counts any worded raise on the row, so one word for a norm raise also silently legalises removing or worsening every ratchet element of that row. Rows without a `kind` take a raise of `{word: "x"}` alone (K8b green); K5 asks for `raised_by` + `reason` + `word`.
Fix: scope a ratchet raise to its element, for example `{"ratchet": "<pair>@<factory_model>", raised_by, reason, word}` with no `from/to`. Keep it out of the norm-raise chain, and check its three text keys on every row. The tests (`SB_RATCHET_ELEMENT_CASES`) use only kind-less rows; add the same rows on a row with a `kind`. The data form is the Lead's call (Q-b).

**B4. N7 `scoreboard_bar.py:321-352 release_check` with `--lines`: a needed line passes as ok.** Control runs (one element, no pass, needed line `release: owner's word needed -- Q1 claude-sonnet-5-5/add-to-cart was 10 (1.0.0) now 12 (1.1.0)`):
`plain -> exit 1` (ok); `UTF-8 BOM -> exit 0 release-check: ok`; `a text file with no release line -> exit 0 release-check: ok`; `"Release:" upper-case -> exit 0`; `UTF-16 -> exit 2` (ok).
The BOM case is the ordinary Windows road. On this machine, Windows PowerShell 5.1.26100 `Out-File -Encoding utf8` writes `b'\xef\xbb\xbf'`, which I measured. An unknown input becomes `ok` (FR-59).
Fix: decode `--lines` with `utf-8-sig`, and refuse (exit 2, naming the line) any non-empty line that is not one of the producer's shapes (`release: ...`, `can ratchet: ...`). Add rows for BOM, wrong file and case.

## Fixes for one round (not blocking alone)

- **F1. Duplication: one B1 judge.** The rule "worse / not worse / not decided by direction and ranges" is written five times: `build_compare` (sb:628-636), `_element_line` (bar:221), `beats` (bar:136-142), `_ratchet_problems` (sb:459, far end), and `_judge_one` (sb:569, scalar). Two of them disagree (B2). One function `judge(better, state, value, against) -> worse|not_worse|better|not decided: range|lower bound|unknown` should serve all five; `beats` = its `better` outcome.
- **F2. N6b B2-E4 is printed by nobody (AR-22).** W11: an unratcheted row with an `unknown` norm verdict gives `compare --release` no stdout and `release-check: ok`. B2-E4 asks for a warning. The removed norms/1 `render_compare` line `release: warning -- unknown norm(s)` was its only producer (divergence 9). Fix: `release: warning -- <row> unknown: <why>` in `release_lines` (bar:263-279 condition `verdict != "red"`).
- **F3. N6b `_boards` (bar:157-178) picks the newest factory board of any class and model.** W9: an older live board on the ratchet's model fm-sonnet and a newer fm-terra board give `no comparable measurement (factory model fm-sonnet vs fm-terra)`, although B2-E8 says the line applies only if that model is not measured. W10: a newer dry board hides an older live one and gives `(run class dry vs live)`. Both are false blocks, in the safe direction. Fix: per element, take the newest LIVE board whose `run.models` holds `factory_model`; keep the current lines when none exists.
- **F4. N6b OQ2 is silent when the factory value is `one_source` or `range`** (bar:252-253 requires `measured`). W13: factory `one_source` 6 with a new bar at 3 gives `release-check: ok`, while W14 (`measured` 6) gives exit 1. After B1 lands, every non-agreeing X1 skips OQ2. Fix: judge OQ2 with the F1 judge on `measured|one_source|range`, so that "not decided" also prints the OQ2 line. Also key `oq2` by `(row, bar)`, not by bar alone: a second ratcheted row beaten by the same bar is dropped today (the line text names the row; the exit code is unaffected).
- **F5. N7 `bar_price` (bar:114-115) prices with `compare.price`, a second valuation formula.** The package's per-request valuation is `cost_capture.value_usage` (:235: long-context tariff, provider, date window). Control: one `gpt-5.6-terra` request with 300,000 input tokens and 1,000 output tokens gives `bar_price 0.612` against `value_usage 1.218 (context_band long)`. One request, two prices: this breaks amendment B1's "same cfg and catalogue as the factory" and P18. Claude rows agree, as the hand checks P1-P3 show. Fix: per request, `value_usage(add_usage(zero(), usage), model, cfg, catalogue, model_provider(model), parse_ts(timestamp))`, with coverage != complete counted as unpriced. Add a long-context test row.
- **F6. N6b: `release-check: ok` when nothing was measured.** W12: no factory board of V exists and an older live release does, so the output is empty and the verdict is `release-check: ok`. "Nothing to compare" reads as a pass in the text (B1-E3, B2-E1 invariant). Fix: `release: warning -- no live factory scoreboard of <V>: nothing judged` (a warning, so the exit is unchanged, per the owner's "only a warning now"). Divergence 5 stays otherwise.
- **F7. FR-25 in `price_line` (bar:127-131):** both figures are printed, but not the gap. Print `gap: <host - re-priced>` when both are known.
- **F8. Code quality.** `release_lines` (bar:229-290) is 62 lines with 4-5 nesting levels (for row, for element, for bar, try/if); split it into element lines / OQ2 / warnings / proposals. `check_norms` (sb:465-537) is 73 lines; queue it. `ratcheted_since` now has no judging reader, only a shape check and a print (dead key); N8 retires it. The `_cost_capture` docstring (bar:37-39) says the deferred import keeps the WARN off the other commands, but every command still prints the WARN line on stderr (seen in every run below).

## Proposed nodes

- **P1 (N7 spec fit, AR-22).** The N7 row says "§3 items 2, 4": the bar's wall, turns, tool calls, person rounds and refused calls, stored as `bar-<model-id>.yaml`. Nothing writes a bar file: `git grep` shows readers only (`judge_norms` via `--bar`, `_bars`, OQ2, `can ratchet`), and `ls-tree experiments/scoreboards` holds only norms.json and rows.json. Until a writer exists, `can ratchet:`, OQ2, N-wall and N-quality are inert (they read `unknown`, the safe direction). This is a node for the bar writer (X1 = `bar_price`), unless the Lead re-scoped N7. In that case the re-scope gets a written line.
- **P2 (duplication, queue).** `_requests` (bar:53-67) copies the loop of `compare.scan` (compare.py:142-160). Expose `compare.unique_requests` and use it from both (a compare.py edit outside these nodes' owns).

## Questions for the owner or the Lead

- **Q-a (Lead; N6b divergence 4).** The amendment says a ratcheted row's worsening "судится против прошлого РЕЛИЗА" (B2-E2), with `was <v_prev> (<ver_prev>)` and a previous range possible (:594). The builder judges against the element's own `value`/`since` and reads no previous board. This is stricter: after a worded worsening, the next release is still judged against the ratchet value until a raise moves it. It is coherent with K5. I recommend accepting it and writing one sentence into the spec. As built, the rule "диапазон против диапазона" applies only to a range-valued element.
- **Q-b (Lead/owner).** The `worsened_passes` form carries no `factory_model`. W16: one pass for `(row, pair, version)` clears the elements of BOTH factory models (`release: owner's word recorded` twice). If the owner's word is per factory model, the form needs that key. The B3 raise scoping is the same data-form decision.

## Answers to the dispatch questions

1. **Empirics.** W1-W8b match the amendment's exact texts. `release-check` exits 1 exactly when a needed line has no matching pass: W8a another pair -> 1, W8b same pair and version -> 0. These paths turn an unknown into `ok`: B4 (`--lines`), F2 (an unknown norm), F4 (OQ2 on one_source), F6 (nothing measured, text only), and B2 in `compare`.
2. **N6b divergences.** (1) right. (2) right, except the per-bar key (F4). (3) acceptable: the line is informative only, either way exit 0. (4) Q-a. (5) right with F6. (6) right. (7) right. (8) right. (9) wrong as to B2-E4 (F2); the other removed lines are superseded by the amendment. (10) a hygiene WARN outside the package, no finding.
3. **One parser.** `load_norms`/`load_old_norms` -> `_read_norms` -> `legacy_to_v2` (one conversion). A case-insensitive grep over all `*.py` of the tree for `norms\.json|NORMS_FILE|norms/[12]|load_norms|legacy_to_v2` finds no second parser; the positive control is that the same grep hits `load_norms` itself. Old K5 refusals still fire (K2: a looser norm without a raise is refused twice; 16 old rows are green per the report). Removed and worsened ratchets are refused (K3, K4). The word road is broken (B3).
4. **N7 price.** A single rate on Claude: P1 0.0818 = hand 0.0818; P2 0.1635 = 2x hand; P3 overrides x2 0.1635 = hand. The formula diverges on long-context models (F5). `not_recomputed -> unknown` is the right direction (P5 absent, P6 unpriced -> unknown, never 0, never the host figure). A real `free-N.log` must confirm three things: the result object is one JSON line with `type: result` and `total_cost_usd`; whether a resumed free run appends a SECOND result line to the same log (today the last one wins: P9 `1.0` then `2.0` -> `2.0`, not 3.0); whether non-JSON progress lines precede it (P7/P8 show both orders are read).
5. **P18 / FR-24 / FR-25.** Money is written only into the forge scoreboard YAML (X1), and later as an X1 ratchet `value` in norms.json. Both are legal by the owner's word of 13.11 (amendment :476-478, :504). `price`, `compare --release` and `release-check` write nothing. A disagreement inside the factory is a range with task_price's note. Bar against host: both are printed, the authoritative one is named, the gap is not printed (F7).
6. **Outside input.** Present: the version (empty, `../x`, `a/b`, `a\b`, `..` -> exit 2), the list cap AT 20 / BEYOND 21, 10,000 lines, non-JSON and non-UTF-8 norms, rows as a list, NaN/bool values filtered by `_num`. Missing: `--lines` BOM, wrong file and case (B4); a row id with a space or an empty row id in norms.json (traced: the `PAIRED` fullmatch fails, the line stays open, a false block, no row); an unreadable NEW bar file (OQ2 silently skipped, only a `release: note`); a two-result-line log (P9).
7. **Duplication and code quality.** One judge with two inputs for release-check: yes (`release_check(lines, version, norms, produced)`). One formatter per line shape: yes (`NEEDED`, one place per text). But the comparison rule is written five times (F1), the price formula twice (F5) and the request loop twice (P2). Code-quality verdict: F8.
8. **N8 owes these lines:**
   - (a) `docs/SIBLING_MAP.md` axis 18: a member row for `experiments/scoreboards/norms.json` (`rows.<id>.norm` tighten-only; `ratchets[]` never removed or worsened; `raises`/`worsened_passes`/`bar_changes` need the owner's word; checker `scoreboard.py norms --check --against <origin/main norms.json>`). It is overdue: fix №23 put it in the N6 commit, and c1620cc touched only experiments/.
   - (b) `docs/tasks/critic-diff-brief.md` item 9: norms.json in the ratchet list, so that a looser `norm`, a removed or worsened ratchet, or a new `worsened_passes`/`bar_changes` entry is named row by row with its word.
   - (c) RUNBOOK §9.5: `assemble` (+ `--model`, `--bar`, `--truth/--judgment`), then `compare <file> --findings`. In the release section: `scoreboard.py release-check --release vX.Y.Z` must exit 0, and the Lead commits `ratchets` from `can ratchet:` lines of the RELEASED version.
   - (d) Calibration §8.1 item 1, (i)-(vi) plus the amendment's "every `owner's word needed` line in the window has `worsened_passes`/`bar_changes`".
   - (e) CI: no workflow runs anything under `experiments/`. The Grep for `experiments` in `.github/workflows` is empty; the positive control (`python` in the same folder) hits 78 times. So K5 "refuses the norms edit (forge-check)" has no code on the path: forge-check needs `norms --check --against` the base's norms.json, plus `test_measurers.py`.
   - (f) PROJECT.md «Релиз», one line (§8.1 item 4).
   - (g) The axis 6 row (`scoreboard.py`, `scoreboard_bar.py`, `run_counters.py`) and the AR-12 Detector line (§8.1 items 2-3).

## Standing questions

- **Fit:** B1, B2, B3, B4, F2, P1.
- **Builder decisions:** divergences above; F3 and F4 for the unsafe or false paths.
- **Seams:** additive. `scoreboard.py` gains only the release-check subparser and `compare --release`; nothing in the package changes.
- **Class completeness:** class "an undecided/unknown comparison reads as not worse or is silent". Sweep of the artifact, all five comparators: `build_compare` B2 (applied), `_element_line` ok, OQ2 F4, `can ratchet` B1, `_judge_one` ok (ranges -> unknown). The axis 18 member line is owed (Q8a). The axis 6 row is owed (Q8g).
- **Tests:** they kill the named defects (the reports' negative controls are consistent). Gaps: not_cross_checked, build_compare ranges, kind rows in K5, `--lines` encodings.
- **DUPLICATION AND CONSISTENCY:** F1, F5, P2. Grepped: the range comparisons in both files, `price(`/`value_usage`, the `seen` loops.
- **CODE QUALITY:** F8.
- **IN-TREE RATCHETS (q9):** norms.json is a new ratchet with no norm raised, and all `ratchets`/`raises`/`worsened_passes` are empty. It has no axis-18 line yet (Q8a).
- **ARCHITECTURE:** AR-20 (K5, B3), AR-22 (B1, F2, P1), AR-28/FR-41/FR-59 (B2, B4, F4, F6), AR-13 (one norms reader: kept). The node commits say `axes: not a mechanism`, which is debatable for K5 (a machine check); the Lead decides.
- **JUDGMENT:** none found. The code compares data only; ratchet commits and passes stay with the Lead and the owner.
- **ONE ROAD:** none found. A case-insensitive grep of `scoreboard*.py` for `mybooks|add-to-cart|java|playwright|codemie|sonnet|terra` has zero hits; the positive control `python` hits.

## Trail (control runs, verbatim excerpts)

- `( cd .../p1v-n6b && python -m pytest experiments/measurers/test_measurers.py -q -p no:cacheprovider )` -> `221 passed in 7.34s` (matches the Lead's 221).
- The worlds script (stdin python, temp dir in the scratchpad; boards and norms built by hand; CLI `scoreboard.py compare --release 1.1.0` and `release-check --release 1.1.0` with `--norms --root`):
  - W1 `owner's word needed -- Q1 claude-sonnet-5-5/add-to-cart was 10 (1.0.0) now 12 (1.1.0)`, check exit 1.
  - W2 `release: ok -- ... not worse`, exit 0.
  - W3 `not decided: range (9..11)`, exit 1.
  - W4 `was 8..12 (1.0.0) now 13..15 (1.1.0)`, exit 1.
  - W5 `unknown: task_price failed`, exit 1.
  - W6 `no value in this release (no scoreboard for the pair)`, exit 1.
  - W7 `no comparable measurement (factory model fm-sonnet vs fm-terra)`, exit 1.
  - W8a exit 1.
  - W8b `owner's word recorded ... (owner, 14.11.2026)`, exit 0.
  - W9 and W10: see F3.
  - W11 `<no stdout>` / `release-check: ok`.
  - W12 `<no stdout>` / `release-check: ok`.
  - W13 `release: ok` only, exit 0.
  - W14 adds the `... ratcheted, new bar mybooks/add-to-cart/bar-claude-opus-5.yaml is better than the factory` line, exit 1.
  - W16: two `owner's word recorded`, exit 0.
  - `--lines`: plain 1, BOM 0, utf-16 2, wrong file 0, leading spaces 1, `Release:` 0.
- K5 script: K0 real `norms: green`; K1 vs `git show c1620cc:norms.json` (norms/1) green; K2 looser norm red ×2; K3, K4 red; K5, K6 red; K7 green; K8b green. Conversion: v1 -> `--convert` differs from the shipped file only by the added `unit`/`better` of QA1-QA6.
- Price script: P1-P9 as quoted in answer 4 and F5.
- `price_row` / `build_compare` script: as quoted in B1 and B2.
- `powershell.exe 'release: x' | Out-File -Encoding utf8` -> `5.1.26100.9818`, bytes `b'\xef\xbb\xbfrel'`.
- Read: the amendment :476-478, :501-621, :900-915; the spec :306-325, :344-474; critic-diff-brief whole; scoreboard.py :1-345, :425-958; scoreboard_bar.py whole; test_measurers.py :1802-1840, :2380-2680; compare.py :1-170; cost_capture.py :137-173, :225-299, :520-545, :3227-3252; norms.json; the N6b and N7 reports; `git show --stat c1620cc`; origin/main SIBLING_MAP/RUNBOOK/calibration greps.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 N6 scoreboard.py price_row: task_price statuses differs/incomplete/not_cross_checked are not mapped to range/at_least/one_source; a one-source price is proposed by can ratchet (B2, B2-E9); test rows (1),(4) missing",
    "B2 N6 scoreboard.py build_compare: prev 10 now 10..12 and prev 8..12 now 8..14 read worse=False (not worse) instead of not decided; disagrees with compare --release; no finding drafted (FR-41)",
    "B3 N6b check_norms/_ratchet_problems: on every real (kind) row the amendment raise {raised_by,reason,word} for a ratchet is refused; green only with an invented norm loosening (from 40 to 41); a worded norm raise also silently legalises any ratchet removal on the row; kind-less rows accept {word} alone",
    "B4 N7 release_check --lines: a UTF-8 BOM file (PowerShell 5.1 Out-File default, measured), a file with no release line, or Release: upper-case gives exit 0 release-check: ok over an owner's-word-needed line (FR-59)"
  ],
  "fixes": [
    "F1 one B1 judge function replacing the five comparators (build_compare, _element_line, beats, _ratchet_problems, _judge_one)",
    "F2 release_lines: warning for an unratcheted row with an unknown norm (B2-E4), printed by nobody since render_compare lines were removed",
    "F3 _boards: per element take the newest LIVE board whose run.models holds factory_model (W9, W10 false blocks)",
    "F4 OQ2 judged on measured, one_source and range via the one judge; key oq2 by (row, bar)",
    "F5 bar_price: value each request with cost_capture.value_usage (long-context, provider, date window) instead of compare.price; terra 300k request 0.612 vs 1.218",
    "F6 release_lines: warning when no live factory scoreboard of the version exists (nothing judged)",
    "F7 price_line prints the gap between the host figure and the re-priced value (FR-25)",
    "F8 split release_lines (62 lines, 4-5 nesting levels); queue check_norms (73 lines); retire ratcheted_since; correct the _cost_capture docstring"
  ],
  "class_completeness": "Class: an undecided or unknown comparison reads as not worse or stays silent. Artifact sweep over five comparators: build_compare B2 applied, _element_line ok, OQ2 F4, can ratchet B1, _judge_one ok. Map: axis 18 member line for experiments/scoreboards/norms.json owed (fix 23, not in c1620cc); axis 6 row owed; both are N8 Lead lines (answer 8). Proposed nodes: P1 bar file writer (spec section 3 items 2 and 4), P2 compare.unique_requests.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md:476-478,501-621,900-915",
      "docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md:306-325,344-474",
      "docs/tasks/critic-diff-brief.md",
      ".claude/worktrees/p1v-n6b/experiments/measurers/scoreboard.py:1-345,425-958",
      ".claude/worktrees/p1v-n6b/experiments/measurers/scoreboard_bar.py",
      ".claude/worktrees/p1v-n6b/experiments/measurers/test_measurers.py:1802-1840,2380-2680",
      ".claude/worktrees/p1v-n6b/experiments/measurers/compare.py:1-170",
      ".claude/worktrees/p1v-n6b/ai-packages/qa-factory/scripts/cost_capture.py:137-173,225-299,520-545,3227-3252",
      ".claude/worktrees/p1v-n6b/experiments/scoreboards/norms.json",
      ".claude/worktrees/p1v-n6b/docs/tasks/specs/reports/20261114-p1v-n6b-report.md",
      ".claude/worktrees/p1v-n6b/docs/tasks/specs/reports/20261114-p1v-n7-report.md"
    ],
    "reruns": [
      {"command": "( cd .claude/worktrees/p1v-n6b && python -m pytest experiments/measurers/test_measurers.py -q -p no:cacheprovider )", "result": "221 passed in 7.34s"},
      {"command": "worlds script: scoreboard.py compare --release 1.1.0 / release-check --release 1.1.0 on 16 hand-built worlds", "result": "W1-W8b match amendment texts and exits; W9/W10 false blocks; W11, W12 release-check ok with nothing said; W13 OQ2 silent on one_source; W16 one pass clears two factory models"},
      {"command": "release-check --version 1.1.0 --lines <file> with an un-passed needed line", "result": "plain 1, UTF-8 BOM 0, utf-16 2, wrong file 0, leading spaces 1, Release: upper-case 0"},
      {"command": "norms --check --against: K0-K8b worlds on the shipped norms.json", "result": "K0, K1 green; K2, K3, K4 red; K5 red (from/to must be numbers); K6 red (not looser); K7 green with invented 40 to 41; K8b green with raise {word} only"},
      {"command": "bar_price control values P1-P9", "result": "P1 0.0818 = hand; P2 0.1635 = hand; P3 0.1635 = hand; P4 terra 300k 0.612 vs value_usage 1.218; P5, P6 unknown; P9 last result line wins (2.0)"},
      {"command": "price_row with faked task_price per status; build_compare on three range pairs", "result": "differs measured-range, incomplete unknown, not_cross_checked measured; 10 vs 10..12 and 8..12 vs 8..14 worse=False"},
      {"command": "powershell.exe Out-File -Encoding utf8, read first bytes", "result": "5.1.26100.9818, first bytes EF BB BF"}
    ]
  }
}
```
