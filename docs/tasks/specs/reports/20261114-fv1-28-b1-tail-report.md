# FV1-28 card B1 tail - builder report (t-798)

Branch `wip/fv1-28-b1`, commit `c57afcc5` (merge of origin/main eefe80e6 + the tail; pushed to origin). The merge had no conflicts (card A1's `first_look.py` / statuses file and `brief_pack.py` merged cleanly). One commit hook line was a WARN only (`forge_metrics --check`: `references/login-roads.json` matches no feature, a file of the merged main, not mine).

## Status per item

| item | status |
|---|---|
| 5 all-access line (s4, s5) | done: data key `gap_rows` + `first_look.gap_rows()` + `brief_pack._fl_all_access_line` |
| 6 `sign_in_lines` + two call sites | done (`build` right after `first_look_lines`; end of `first_look_runner_lines`) |
| join row (3) | done: `test_own_way_in_join` (A1 `put` -> `read` -> S5/S6/S3/S7 line) |
| `test_first_look_wiring.py` | 102/102 ok (the three checks rewritten to the GAP texts) |
| `test_brief_pack.py` rows (old 2966, 2994-2997) | rewritten by reading, NOT run |

## What was built

- `references/first-look-statuses.json`: only `"gap_rows": {"status": ["unreachable"], "blocked_by": ["access"]}`. The `note` text was left alone.
- `first_look.py`: only `gap_rows()` (returns `{}` when the key is absent, not a dict, or either list is empty).
- `brief_pack.py`: `FIRST_LOOK_ALL_ACCESS_TAIL`, `_fl_all_access_line`, `FIRST_LOOK_WALKER = ("S3","qa-runner")`, `sign_in_lines`, one call line in `build`, one at the end of `first_look_runner_lines`.
- Item 5 text: `First look: the walker could not reach these requirements (access): R-1: <why>; R-2: <why>; a gap you close with your own look` (s5) / `...; name it as a gap` (s4). The `(access)` word comes from the data list. It replaces ONLY the "no row of the record names such a path" line (it never hides item lines a row does carry). `why` goes through `app_card.scrub`, whole (no clip). Rows are those shown (after the window filter).
- Item 6 line: `Way in found by this story's first look (walk <W>, <surface>, as <actor>): url <url>; fields user <sel>, secret <sel>, submit <sel>; steps: a; b; it worked then - if it fails now, find the way yourself and record it.` http: `access <kind> at <access url>, key names <user_key>/<secret_key>` replaces the `fields` part. Every value through `scrub(tokens=False)`. Printed fields only: walk, surface, actor, url, fields.user/secret/submit, steps, the http access kind/url/user_key/secret_key. Never `why`, `landed`, `evidence`, `quote`, `req`. Longer than 600: `line[:597] + "..."` (so exactly 600) followed by `whole: work/first-look.yaml`.
- The http way's own key (the word `access` as a sign_in key) is read from the data key `sign_in_surface_keys` through `FL.data()`, not written as a literal, because `test_red_words_come_from_the_data_file` forbids a quoted `"access"` in that block of `brief_pack.py` (it failed once on my first version; fixed).

## Where the card and the merged A1 code disagree / where the card was silent

- Card says "`first_look.read(task_root).get("sign_in")`"; the merged code agrees (`read()` returns `sign_in`, `{}` when none). Card field names match A1 (`surface, actor, url, steps, fields{user,secret,submit}, landed, access{kind,url,user_key,secret_key}`). No divergence of field names. `walk` is a field of `read()`, not of `sign_in`; I used `read()["walk"]`.
- SILENT: which fields of a stale/null/absent/unreadable record -> no line (card CONFLICT line says stale; I applied the same to null/absent/unreadable via `FL.state(...)["kind"] == "ok"`).
- SILENT: the s4 "all-access" when the window filter is on is s5 only; s4 has no window.
- SILENT: the walker call site passes the pair `("S3","qa-runner")` (new constant `FIRST_LOOK_WALKER`), because `sign_in_lines(task_root, stage, role)` needs a pair and `FIRST_LOOK_KIND` has no S3 qa-runner.

## Question (returned, not decided)

1. A conflict of two requirements of the card: item 6 says the call at the end of `first_look_runner_lines` exists so "a re-walk on new heads sees the way the last walk found", while CONFLICT says a STALE record gives no sign-in line ("a stale walk's way is history"). A re-walk on new heads is exactly a stale record, so as built the runner line prints only when the record is CURRENT (it never does for a real re-walk). I built the explicit CONFLICT rule (no line when stale, both call sites). If the walker's brief should show a stale record's way, it needs a keyword on `sign_in_lines` (e.g. `stale_ok` for the runner call only) - a design decision I did not take.

## FR pass (B, C, E)

- B: the lines go to a role's brief, not to a person; no question to a person added. n/a.
- C: FR-13 closed variety in data: the two words of item 5 are `gap_rows` of the statuses file, read through `first_look.gap_rows`; no quoted `"unreachable"`/`"access"` in `brief_pack.py` (test `test_red_words_come_from_the_data_file` ok). FR-15 no path searched. FR-38: the line names only what the form holds. FR-56: no line names a script.
- E: FR-41/FR-59 unchanged: a missing look stays a GAP; a stale/empty/non-dict `sign_in` is no line (never a fact "no way in"). FR-23: absent/empty/not-a-dict/stale/null each have one outcome (no line).
- architecture: AR-1 (closed words as data `gap_rows`), AR-13 (`sign_in` read only through `first_look.read`/`state`), AR-21 (the own way in travels to the briefs; a cut names the record), AR-23 (empty outcomes stated). judgment: none -- brief lines carry data; whether the way is right stays the role's.
- INVARIANT (no account value reaches a brief): the lines print only fields A1's guard judged; `scrub` applies to each; row `password: hunter2hunter2` in a hand-edited step is scrubbed (test row). `sign_in_secret_faults` was not touched.

## Siblings

Every (stage, role) kind calling `first_look_lines` keeps byte-identical output when the new data key / sign_in are absent: `first_look_lines` itself was not edited in this tail; the only change in its body path is `_fl_body`'s fall-back line (it differs only when every shown row of s4/s5 is an unreachable+access row; with `gap_rows` absent or empty it is the old text - tested: variants `key_absent`, `empty_lists`, `one_list_empty`, `one_row_product`). `sign_in_lines` returns `[]` when `sign_in` is absent, so `build` output of every kind is unchanged for records without it (the 261 rows of `test_first_look_briefs.py` and `test_ahead_cards` / `test_brief_s3_roster` / `test_codex_tool_guidance` / `test_field_producers` ok).
Analog noticed (not touched): `app_card._first_look` still says "there was no first look" as a fact (B2's file); `FIRST_LOOK_HEADS["s5"]` text is FV1-29's.

## Witness (verbatim)

`python -B scripts/tests/scenario_walk.py --witness-for scripts/brief_pack.py scripts/first_look.py` printed 3 scenario files + keep files (list in the run); each fast file run ONCE from `ai-packages/qa-factory` (slow ones are judged by the batch canon; `test_brief_pack.py` and `test_judgment_census.py` NOT run):

```
test_first_look_briefs: === test_first_look_briefs: 261/261 ok ===
test_first_look_wiring (7s): === test_first_look_wiring: 102/102 ok ===
test_first_look (8s): === test_first_look: 450/450 ok ===
test_first_look_step (10s): === test_first_look_step: 105/105 ok ===
test_first_look_code_look (3s): === test_first_look_code_look: 127/127 ok ===
test_ahead_cards (19s): === test_ahead_cards: 265/265 ok ===
test_brief_s3_roster (5s): 12 passed in 3.53s
test_codex_tool_guidance (14s): === test_codex_tool_guidance: 217/217 ok ===
test_field_producers (16s): === test_field_producers: 885/885 ok ===
test_fit_targets (5s): === test_fit_targets: 116/116 ok ===
test_flow_requests (4s): === flow requests: 93/93 ok ===
test_regression_scope (23s): === test_regression_scope: 93/93 ok ===
test_role_load (3s): === role_load (the one measure of a role's start load): 186/186 ok ===
test_story_run_s6_w1_frozen (16s): === test_story_run_s6_w1_frozen: 6/6 ok ===
test_walk_plan_fields (3s): === test_walk_plan_fields: 123/123 ok ===
test_whole_identifier (3s): === whole identifier and the revoked word: 166/166 ok ===
python -B scripts/selftest.py --limits --lang  ->  PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier ... === qa-factory selftest: 4/4 ok ===
```

New rows in `test_first_look_briefs.py` (all ok, in the 261): `all_access` (s4, s5, `one_row_product`, `key_absent`, `empty_lists`, `one_list_empty`), `own_way_in` (join through A1 `put`: ui and http, S5/S6/S3/S7, outside role -> none, no why/quote/evidence printed, no sign_in -> none), `own_way_in_edges` (absent, empty, not_a_dict, a_list, stale, null, `line_600` whole, `line_601` and `line_2000` cut at 600 + `whole:`, a password pair scrubbed, the walker's brief with a current record, control without).

Judged by the batch canon (not run): `test_brief_pack.py` (rows at old 2966 and 2994-2997 rewritten by reading to the GAP texts; the 2994-2997 row now expects the literal sentence `First look: a GAP - what the stand shows is not known for this story (the record cannot be read: <problem>); it is not a fact that there is no stand.` for the clause-less `_fl_state(Path("."))` call), `test_judgment_census.py`, the slow scenario/story files. Quarantined `test_brief_pack_manual.py:237` (old file line text) not edited, not run (named in the first report).

## Byte measure

S5 first-look block of the first report's fixture (window = TC-001 -> R-1): unchanged by this tail, 781 bytes / 9 lines (the first report). The tail adds, only when the record holds a `sign_in`, one line: the A1-form ui example above is 297 bytes; the hard bound is 600 characters + `whole: work/first-look.yaml` (27 bytes). `role_load` static total is not touched (`test_role_load.py` 186/186 ok).

## Needed beyond the manifest

`app_card.py` (`scrub`), `tests/test_first_look.py` (`Story`, `_good_ui`, `_good_http`, imported by the new join row), `tests/harness.py`, A1 reports not needed.
