# t-2031 — live proof of the mutation-probe batch (spec t-1968 §6), on a copy

Package: `D:/ws1/exp-thinking-roles\pkg-proof\ai-packages\qa-factory` (bc1ab486b). Copy: `D:/ws1/mybooks-stand\tr-probe` (robocopy of `tr-arm-b` minus `node_modules`, which is a junction to the source's). Stand `http://localhost:3000` answered 200. No code change, no `claude` call. Env of every command: `CLAUDE_PROJECT_DIR=tr-probe`, `CLAUDE_PLUGIN_ROOT=pkg-proof`, `QA_FACTORY_RUN_MODE=driver` (see "Setup"), cwd by `Start-Process -WorkingDirectory`.

## Verdict per step

| step | result |
|---|---|
| Setup: open S5 critic dispatch | PROVED (reached in one command, no `invalidate` needed) |
| 1a. re-probe TC_001 in-stock | PROVED (marker, M-TS1, restore verified, hash equal), target `false` as predicted |
| 1b. re-probe TC_002 out-of-stock | PROVED (marker, M-TS1, restore verified, hash equal), target `false` |
| 1c. `--at <Then line>` for TC_001 | NOT PROVED: first divergence below (manifest `assertion_id` points at a blank line; the Then-line probe is `no_failure`) |
| 2. window of TC_001, TC_002 `approved` | NOT PROVED: two gaps per instance, listed below |
| 3. `--judge` on a `cause: judgment` record | NOT REACHED: no record with that cause exists, and 17 probes did not produce one |
| M-TS1 live | PROVED (14 probes) |
| M-TS2 live | NOT REACHED live (no unprobed one-argument `expect` in the stand); offline replay only |

## Setup

`story_step.py start --task LOCAL-1 --stage S5 --role qa-code-critic --scope LOCAL-1_TC_001,LOCAL-1_TC_002` first refused: the story was started in `driver` mode and the call ran in `desktop` mode. I set `QA_FACTORY_RUN_MODE=driver` (the variable `launch_card.RUN_MODE_ENV` reads; "run it the way it was started" is the refusal's own first door), no waiver. Second call: `dispatched S5-qa-code-critic-15 (revision 314)`. S5 was `done` and no `invalidate` was needed; `controller.json` was not touched by hand. The command printed `project: the stored path (D:/ws1/mybooks-stand\tr-arm-b) is not the project this story is in here; using ...\tr-probe`, so the copy's absolute paths stored in the old dispatches did not send writes to the source. Checked: a listing of all 3637 files of `tr-arm-b` (path, size, mtime ticks) before and after is identical (0 differing lines). `start` also ran `probe_debt --settle` (62 s); the test file hash did not change.

## Step 1a. TC_001 in-stock (instance `@regression LOCAL-1_TC_001 in-stock add shows success toast, badge 1 and one cart line`)

Source file `tests/e2e/cart/add_to_cart.spec.ts` sha256 before = after = `5F9C736EFDC6B8DDA0ECDF4C2809DBCCC2DACD23CD08CAE02FC0DD71E94CBA87` (Get-FileHash, before and after the run).

Record fields, verbatim from `--json`:
- `verdict`: `intended_failure`; `proved_by`: `marker`; `failure_kind`: `assertion`
- `mutation_detail.message_form`: `M-TS1`; `mutation_detail.message_marker`: `qa-probe-be3398b8cfe6`; `message_note`: `""`
- `mutation_detail.statement_after`: `expect(catalog.cartBadge, ['qa-probe', 'be3398b8cfe6'].join('-') + ' ' + 'step 1: badge empty before the add').not.toHaveCount(0);` (the runtime join, never a contiguous literal)
- the marker line of the failure, in `evidence/runs/25549356f4326c0b8a93/red_probe-...083419.junit.xml` line 7: `Error: qa-probe-be3398b8cfe6 step 1: badge empty before the add`; the call log (line 17) echoes `- qa-probe-be3398b8cfe6 step 1: badge empty before the add with timeout 5000ms`
- `restore`: `{"verified":true,"sha256":"5f9c...cba87","restored_from":"copy","copy_kept":false}`
- `target`: `{"line":43,"end_line":43,"assertion_id":"tests/e2e/cart/add_to_cart.spec.ts:46","is_assertion_id":false}`
- note: `this probe broke line 43, not the obligation's check at tests/e2e/cart/add_to_cart.spec.ts:46: it does not prove that check; probe the Then's line with `--at 46`; or, when no check of the Then can be inverted here, report the item `unverified` with the reason`
- live receipt written: `work/sensitivity-receipts/regression--LOCAL-1_TC_001--in-stock-...-ca298e42-live-ade3423154369a8a.json`, `proved_by: marker`, same `target`.

## Step 1b. TC_002 out-of-stock (instance `@regression LOCAL-1_TC_002 out-of-stock book: button disabled, no POST /api/cart, no cart line`)

File hash before = after = `5F9C...CBA87`.
- `verdict`: `intended_failure`; `proved_by`: `marker`; `message_form`: `M-TS1`; `message_marker`: `qa-probe-8567dccdcc68`
- `statement_after`: `expect(detail.addButton, ['qa-probe', '8567dccdcc68'].join('-') + ' ' + 'Then 4: Add is disabled on B').not.toBeDisabled();`
- marker in the failure text: `Error: qa-probe-8567dccdcc68 Then 4: ...` (junit `evidence/runs/c60ba42085866d620fd9/...083617.junit.xml` line 110 and call log line 120)
- `restore.verified`: `true`
- `target`: `{"line":105,"end_line":105,"assertion_id":"tests/e2e/cart/add_to_cart.spec.ts:104","is_assertion_id":false}`
- receipt written, `proved_by: marker`.

## Step 1c. `--at <Then line>` for TC_001 — FIRST DIVERGENCE

The spec expected `--at` to the Then line to give `target.is_assertion_id: true`. The manifest's `assertion_id` for this instance is `add_to_cart.spec.ts:46`, and line 46 of the file is a BLANK line (Read tool, lines 43-47: 43 `step 1` expect, 44 blank, 45 `clickAdd`, 46 blank, 47 `Then 1`). The same for TC_002 out-of-stock: `assertion_id` `:104` is `await detail.open(B);`; the `Then 4` expect is line 105. So the manifest points one line before the Then in both cases and `is_assertion_id` can never become `true` through `--at` for these two. (The file hash equals the one recorded by the earlier arm-b probes, so this is not drift of the file in the copy.)

What the probes did:
- `--at 47` (the real `Then 1` line): `verdict: no_failure`, no `proved_by`, `target.is_assertion_id: false` (47 != 46), `receipt: null`. Mutated statement `expect(catalog.successToast, [...].join('-') + ' ' + 'Then 1: a success toast after Add on A').not.toBeVisible();` — the success toast vanishes by itself, so the inverted check passes. This is exactly the case the new craft bullet names ("an element that vanishes by itself may pass when inverted").
- `--at 46` (the manifest's number): `already_probed` — "the probe of these bytes said no_failure ... Change the test before probing it again; a person's word passes a repeat (waiver.py, stage S5, block "already probed on these bytes")". No person in this run, so no further `--at` on TC_001 in-stock is possible. Side effect to know: the `no_failure` record at :47 replaced the `intended_failure` record at :43 as the instance's record; the :43 receipt (`proved_by: marker`) still stands in `sensitivity-receipts/` and the window reads it.

## Step 2. Window state (`window_record.py --task LOCAL-1 --dispatch S5-qa-code-critic-15`, exit 1)

Output, gaps for the two instances asked about (the window also holds 2 more instances of the scope):
- `review:@regression LOCAL-1_TC_001 in-stock ...` — `the manifest row carries no critic_verdict; the critic records its verdict through manifest_put.py`
- `review:@regression LOCAL-1_TC_002 out-of-stock ...` — same
- `semantic_sensitivity:@regression LOCAL-1_TC_001 in-stock ...` — `the probe broke line 43, not the obligation's check at tests/e2e/cart/add_to_cart.spec.ts:46; ... for a probe of another line: probe the Then's line (`probe_by_code.py ... --at <n>`...); or ... return the item `unverified` with its reason ...` (the gap names `--at` and the unverified door, as N4 specifies)
- `semantic_sensitivity:@regression LOCAL-1_TC_002 out-of-stock ...` — `the probe broke line 105, not the obligation's check at ...:104; ...`
- other instances: `contradicts_requirement` (TC_001 stock-0), `probe_gap` (TC_002 success message; its record is the old `wrong_location`).
So `approved` is NOT reached and cannot be by the probe path in this copy: (a) the two `review` gaps need the critic role's verdict through `manifest_put.py` (a role action; no role ran), (b) the two `semantic_sensitivity` gaps come from the wrong `assertion_id` of the manifest. A fix of the manifest rows (author's act) was not done: it would change what is measured. The note lines also show an old person's word ("go on I accept that the three tests are not probed here ...") recorded in the copy's pipeline from the arm-b run, printed as "recorded, not read by this window".

## Step 3. `--judge`

NOT REACHED. Before the run, the stored records had `cause: data_row` on 8 instances (the old package's word, which the new package no longer writes). I re-probed all of them on the new package, plus 4 of the 7 never-probed instances:

| instance (short) | verdict | proved_by | form | target.is_assertion_id |
|---|---|---|---|---|
| TC_019 P-error500 | intended_failure | marker | M-TS1 | false (122 vs 128) |
| TC_019 P-timeout | intended_failure | marker | M-TS1 | false |
| TC_018 P-deletefail-timeout (wishlist_move) | intended_failure | marker | M-TS1 | true (143) |
| TC_020 P-addfail-error500 | intended_failure | marker | M-TS1 | false (150 vs 156) |
| TC_020 P-addfail-timeout | intended_failure | marker | M-TS1 | false |
| TC_020 P-readfail-error500 | intended_failure | marker | M-TS1 | false |
| TC_020 P-readfail-timeout | intended_failure | marker | M-TS1 | false |
| TC_018 P-postfail-timeout (unprobed) | intended_failure | marker | M-TS1 | true |
| TC_017 P-bookread-error500 (unprobed) | intended_failure | marker | M-TS1 | false |
| TC_017 P-cartread-error500 (unprobed) | wrong_location | — | M-TS1 | true |
| TC_018 P-getfail-error500 (unprobed) | wrong_location | — | M-TS1 | true |

A count over `work/probes/*.json` after all runs: records with `cause: judgment` = 0; with `message_form: M-TS2` = 0. All 8 former `data_row` records are now marker-proved, so the case the critic path was built for did not arise on this stand. Said honestly: the critic path (`--judge`, N2/N5) has no live proof from this run; its proof stays the unit tests of N2/N5. Seven stand instances stay unprobed (3 more not run: TC_017 P-cartread-timeout, TC_018 P-getfail-timeout, P-removefail-timeout).

The two `wrong_location` rows are a correct negative: both mutate an `expect.soft(...)` line (157 / 234), the inverted check passed, and the test failed at the NEXT unmutated soft check (158 / 235). The token `qa-probe-6af609dec3e3` occurs nowhere in that junit or log (grep count 0 over junit, report.junit, log), so the marker did not prove it and the run read as another line's failure (E1.7: no other check's text can carry the token).

## Facts of the new package seen live

- M-TS1 (`expect(v, 'msg')` 2-argument): message becomes `qa-probe-<hex> <author message>`; the Playwright failure body carries it as `Error: qa-probe-<hex> step 1: ...` AND in the call log; the code frame of the junit shows the source line with the runtime join (`['qa-probe', '6af609dec3e3'].join('-') + ...`), never the contiguous token — E1.3 held (the grep for the token in a case with a frame found only the runtime messages). `expect.soft` takes M-TS1 too.
- M-TS2 (one-argument `expect(v)` + Playwright import): NOT seen live. Offline replay (scratchpad `ts2_replay.py`, pure `plan_detector_mutation`, no write): `before: expect(page.locator('#x')).toBeVisible();` `after : expect(page.locator('#x'), ['qa-probe', 'abc123def456'].join('-')).not.toBeVisible();` `message_form: M-TS2`.
- `message_form` and `message_marker` live in `mutation_detail`, not at the top level of the record; the top-level record fields are `proved_by`, `target`, `restore`.
- Playwright matcher-internal errors (E1.13): not observed.

## Findings beyond the DoD (classes, not widened)

1. Manifest `assertion_id` of the add_to_cart tests is stale or wrong (46 vs Then at 47; 104 vs 105; 128 vs probed 122; 156 vs probed 150; 65 vs 59). With N4 this turns every probe of those tests into `semantic_sensitivity`, and `--at` cannot cure it. Producer: whatever wrote `assertion_id` (automator / `manifest_from_tests`), not read here. Siblings: the wishlist_move rows are right (`true`).
2. `already_probed` blocks an `--at` re-probe after a `no_failure` on the same bytes (the key is the instance + bytes, not the target). So the spec's "the critic re-probes with `--at <Then line>`" works once; a wrong first `--at` leaves only a person's waiver. Class: the repeat guard ignores the target.
3. A probe of an instance outside the dispatch's scope ran because an older person's word "go on ... three tests are not probed here" was applied as a scope waiver (note on records: `LOCAL-1_TC_017 is outside its scope of S5-qa-code-critic-15; passed on a person's word: go on ...`). The word's own text is about the tooling gap of three tests, not about scope. Class: AR-24 (a word covers only its own class).
4. `story_step.py start` for S5 on a story whose S5 is `done` works without `invalidate` and reopens a dispatch; observed only, not judged.

## Needed beyond the manifest

`launch_card.RUN_MODE_ENV` (mode refusal), `window_record.py --help`, the junit evidence files, `test_probe_marker.py` helper shape for the offline replay. The manifest's `given` was otherwise sufficient.

## Witness

Commands (all via `C:\Users\DEV1~1\AppData\Local\Temp\claude\D--ws-yml-text-factory\b3d6b861-57ff-444e-a358-7720466980d2\scratchpad\run.ps1`, which sets the three env vars and runs `python -B <pkg>\scripts\<script>` with `-WorkingDirectory` = the copy; outputs `p1..p23.out`, `w1.out` in the same folder):
- `probe_by_code.py --task LOCAL-1 --dispatch S5-qa-code-critic-15 --test "tests/e2e/cart/add_to_cart.spec.ts::<title>" --instance "<title>" --json --timeout 300` (add `--at 47` / `--at 46` for 1c)
- `window_record.py --task LOCAL-1 --dispatch S5-qa-code-critic-15`
- source hash: `Get-FileHash ...\tr-probe\tests\e2e\cart\add_to_cart.spec.ts` = `5F9C736EFDC6B8DDA0ECDF4C2809DBCCC2DACD23CD08CAE02FC0DD71E94CBA87` before step 1, after every probe, and at the end.
- source untouched: listing diff of `tr-arm-b` (3637 files) before/after = `differing lines: 0`.
