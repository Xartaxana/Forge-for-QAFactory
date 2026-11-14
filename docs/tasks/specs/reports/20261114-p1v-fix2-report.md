# t-714 report: P1-v fix round (B1-B4, F1-F7) after the topic critic t-709

Worktree `.claude/worktrees/p1v-fix2`, branch `wip/p1v-fix2`, from 79fbbaa. Outside the package: no FR walk, no `architecture:` line.

## Witness (verbatim)

```
( cd .claude/worktrees/p1v-fix2 && python -m pytest experiments/measurers/test_measurers.py -q )
........................................................................ [ 25%]
........................................................................ [ 51%]
........................................................................ [ 76%]
..................................................................       [100%]
282 passed in 9.38s            (221 before; +61 rows)

python -B experiments/measurers/scoreboard.py norms --check                       -> norms: green   (exit 0)
python -B experiments/measurers/scoreboard.py norms --check --against <scratch copy of the pre-edit norms.json>  -> norms: green   (exit 0)
```

The shipped `norms.json` holds NO ratchet element, NO raise, NO `worsened_passes` entry and no `bar_changes` (all arrays empty), so no row needed migrating; only its `_comment` text was updated to the new raise / pass forms (a comment key, read by nobody). The scratch copy was byte-copied before the edit.

## Verdict item -> what changed -> file:line -> test row

| item | what changed | file:line | test row (test_measurers.py tables) |
|---|---|---|---|
| B1 | `price_row` maps agrees -> `measured` scalar, differs -> `range {low, high, note}`, incomplete -> `at_least {at_least, note}`, not_cross_checked -> `one_source {value, note: "one source"}`, other status -> `unknown` naming it; `agrees` with low != high -> `range` (not a scalar) | scoreboard.py:317 | SB_MONEY_CASES: the four status rows, "a status task_price does not define", "agrees but the ends differ"; SB_REL_CASES "release: a scoreboard built by `assemble` with one_source X1 is never proposed by `can ratchet:`; the same with agrees is" (runs `assemble` for all four statuses, positive control `agrees`) |
| B2 / F1 | ONE `judge(better, state, value, against)` returning `worse / not_worse / better / not decided: range / not decided: lower bound / unknown`; `build_compare` uses it, entries gain `outcome`; the three pairs are rows | scoreboard.py:671 (judge), :697 (build_compare) | SB_COMPARE_CASES "B2 pair: was 10, now 10..12", "was 8..12, now 8..14", "was 10, now 7..10" + one_source / at_least rows |
| F1 | the same `judge` serves `_element_line`, `beats` (= outcome `better`), `bar_better_line`, `_ratchet_problems`, `_judge_one` (norm limit and bar comparisons) | scoreboard_bar.py:238, :158, :167; scoreboard.py:455, :602 | SB_REL_JUDGE_CASES (21 old rows, 6 new on the `assemble` value shapes); SB_RATCHET_ELEMENT_CASES; SB_NORM_CASES (unchanged, green) |
| B3 / Q-b | ratchet raise `{"ratchet": "<pair>@<factory_model>", raised_by, reason, word}` lives outside the norm-raise chain (`_v2_view` drops it from the norm raises); its three text keys are checked non-blank on every row, with or without `kind` (a kind-less row checks ALL its raises); a norm raise legalises no ratchet change and the reverse; ratchet raises append-only; `worsened_passes` entries need `factory_model` when NEW (absent in `--against`; with no `--against` every entry is new) | scoreboard.py:455 (`_ratchet_problems`), :489 (`_row_problems`), `_v2_view` raises filter | SB_RAISE_SCOPE_CASES (15 rows: K5, K6, K7 on a row WITH a kind; another factory model; missing reason; kind-less `{word}` K8b; bad `ratchet` text; appended / removed; new pass with / without / blank factory_model; old pass read as before; no `--against`); SB_RATCHET_ELEMENT_CASES (WORD in the new form) |
| Q-b release side | element lines carry ` [factory model <fm>]`; `release_check` clears a line by a pass with the same row, version, pair AND factory model; a pass with no `factory_model` (old entry) clears as before | scoreboard_bar.py:50 (FM_TAG), :238, :375-400 | SB_REL_CASES W16 and W16b |
| Q-a | divergence 4 kept: a ratcheted row is judged against the ratchet's own value/since; no previous board read | (no change) | SB_REL_JUDGE_CASES |
| B4 | `--lines` decoded `utf-8-sig` (stdin: a leading BOM stripped); every non-empty line must start `release: ` or `can ratchet: ` (exact lower-case) else exit 2 naming line number and line; empty / BOM-only / blank-only input exit 2 "no lines"; UTF-16 stays exit 2 | scoreboard_bar.py:51, :375-386, :438; scoreboard.py `_read_text(encoding)` | SB_LINES_CASES (14 rows: BOM + needed -> 1, BOM + ok -> 0, wrong file, line 3, upper case, no space, empty, BOM only, blank only, UTF-16, 10,000 lines + one wrong) |
| F2 | `release: warning -- <row> unknown: <why>` for an unratcheted row with an unknown norm verdict; exit unchanged | scoreboard_bar.py:290 (release_lines, second loop) | SB_REL_CASES W11, W11b |
| F3 | `_boards` keeps every board of the version; per element `_board_for`: newest LIVE board holding the factory model, else newest live (names the model mismatch), else newest of any class (names the class), else none | scoreboard_bar.py:183, :212, :221 | SB_REL_CASES W9, W9b, W10 |
| F4 | OQ2 judged by `judge` on `measured / one_source / range`; `worse` or any `not decided` prints the line; `done` keyed by `(row, bar)` | scoreboard_bar.py:167, :269 | SB_OQ2_CASES (rewritten overlap row), SB_REL_CASES W13, W13b, "OQ2 is keyed by (row, bar)" |
| F5 | `bar_price` values each request with `cost_capture.value_usage(add_usage(zero(), usage), model, cfg, catalogue, model_provider(model), parse_ts(timestamp))`; coverage != complete = unpriced | scoreboard_bar.py:98, :134 | SB_BAR_CASES F5 x3 (terra 300,000 in -> 1.218, hand 1.2 + 0.018; 272,000 -> 0.556; dated before the catalogue window -> unknown), the 14 old bar rows still green |
| F6 | `release: warning -- no live factory scoreboard of <V>: nothing judged` when no live factory board of V exists; exit unchanged | scoreboard_bar.py:300 | SB_REL_CASES W12 and the four rows that now carry it |
| F7 | `price_line` prints `; gap: <host - re-priced> (host - re-priced)` when both known, nothing otherwise | scoreboard_bar.py:145 | SB_BAR_CASES F7 |
| compare --findings | a finding only for `worse`; every `not decided` / `unknown` row prints `no finding: <row> <outcome> (was .., now ..)` | scoreboard.py:986 | SB_CLI_CASES (existing findings rows green); SB_COMPARE_CASES outcome field |

## Decisions the verdict forced (look at these)

1. Q-b release side needs the factory model IN the line, or one pass cannot tell two identical-looking lines apart. Every `owner's word needed -- <row> <pair> ...` ELEMENT line now ends with ` [factory model <fm>]` (OQ2 lines and `release: ok` lines unchanged). That departs from the amendment's exact text (B2 line list) by one suffix; `PAIRED` already allowed trailing text. If the Lead prefers another carrier, `FM_TAG` and `_element_line` are the two places.
2. F5 date edge: a transcript line with no or unreadable `timestamp` is asked with no date window (`parse_ts` -> None), which is the package's own `resolve_rate` rule ("with no timestamp the window is not checked"); the fields CAN be supplied from a bar log, so no question is returned. Provider comes from the package's `model_provider(model)`. A request dated before the catalogue window is `unpriced` (test row).
3. F6 is literal: the warning prints whenever no LIVE factory board of V exists, also next to the element lines "no value in this release" and next to `release: no previous release`; four existing rows of SB_REL_CASES now expect it.
4. B3 without `--against`: every `worsened_passes` entry counts as new (the file cannot say otherwise), so `norms --check` alone refuses an entry with no `factory_model`. The shipped file holds none.
5. `_judge_one` (norm verdicts) now reads state `one_source` as a value (B2-E9 "compared as a value"), and a `range` / `at_least` X1 is `unknown` there; before, a one-source price was `measured` and judged. No norm of the shipped file names X1.
6. K5 ratchet check: an UNCHANGED element value is skipped; a changed range that the judge cannot show not worse (`not decided`) is refused as "cannot be shown not to have worsened" (safe direction; ratchets are scalars in practice because `can ratchet:` proposes `measured` scalars only).
7. `OQ2`/`beats`: a `not decided` overlap prints the OQ2 line (F4, edge 8); the old test row that said overlap gives no line was rewritten.

## Not done, by the dispatch

F8 (split `release_lines`, queue `check_norms`, retire `ratcheted_since`, the `_cost_capture` docstring that wrongly says the WARN is kept off other commands: still wrong), proposed nodes P1 (bar writer: nothing writes `bar-<model>.yaml` yet, so `can ratchet:`, OQ2 and N-wall stay inert), P2 (`compare.unique_requests`; `_requests` still copies the loop of `compare.scan`), the Lead's carrier lines (answer 8).

## Analogs noticed (not widened)

- `_requests` (scoreboard_bar.py:57) still duplicates `compare.scan` (P2); it now also keeps `timestamp`, so P2's shared helper should return it.
- `price_row` and `bar_price` are now two writers of two states of one quantity; both are read only through `judge`, so a sixth copy of the rule was not found. Searched for other `<`/`>` comparisons on row values in both files: `render_compare` "can tighten" compares a norm value to a measured value (a norm check, not a B1 comparison, left as is).
- `compare.py` `price`/`price_seen` remain the second valuation formula for the factory-vs-agent compare tables outside the scoreboard (not in owns).
- `scoreboard.py` `cmd_compare` prints "undecided" in the per-row line and the new "no finding" line in `--findings` mode: two texts for one outcome.

## Needed beyond the manifest

`ai-packages/qa-factory/scripts/cost_capture.py` (value_usage / resolve_rate / add_usage / model_provider), `ai-packages/qa-factory/references/model-rates.json` (the terra long-context control), the amendment `docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md:500-621` (the manifest named the run-scoreboard spec, whose B1/B2 live in the amendment).
