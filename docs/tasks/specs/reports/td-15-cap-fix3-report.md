# TD-15 cap-fix3 - text-derived ids follow the scrub (builder report)

Branch `td/15-cap-fix3`, one commit. Items 1-8: see the table. Never changed the shell's cwd on purpose; two read-only Bash calls began with `cd` out of habit (hook warned, nothing broke; the shell resets per call).

| item | status | where |
|---|---|---|
| 1 text-derived ids follow the rewrites | DONE | `tools/story_capture.py:274` `text_id_map`, `:313` `rekey_ids`, call `:409-412`, README line, `report["ids"]` |
| 2 version from the SOURCE before drops | DONE | `tools/story_capture.py:364` (`recorded_version(source)`) |
| 3 `expected()` writes `options` when recorded | DONE | `tools/story_capture.py:546-549`; walker `scenario_walk.py:583-586` (question facet: kind only + NOTE `options not recorded`) |
| 4 `SCENARIO_FULL=1` full refusal text | DONE | `scenario_walk.py:461` `_shown`, used in `_compare`, `_judge`, names checks, variants, start refusal, facet crash |
| 5 re-capture local-1-arm-b | DONE | same command as the report minus `pipeline.json` drop; `expected` re-run; `by: lead` rows kept; gate A `question` facet restored in `walk` (its not_walked row removed) |
| 6 (C-2) `example-url` keeps the `/browse/<KEY>` tail | DONE | `tools/story-scrub-rules.json` example-url (`pattern` with a `tail` group, replacement `https://example.invalid/<n><tail>`), `Cleaner.rewrite` |
| 7 (C-1) pairing method | DONE, method used = the critic's | see 1 |
| 8a W-3 `names` on a decision facet | DONE (already held via `_judge`, test added) | test row in `test_scenario_walk.py` |
| 8b W-1 `handed` by TODAY's template | DONE (about 15 lines) | `scenario_walk.py:359` `required_today`, `door_handed` |

## 1 / 7 Method and the id kinds
- Method (critic's, item 7): for every snapshot-shaped JSON of the captured root (`description`, `acceptance_criteria`, `comments`) the tool calls the package's own `branch_accounting.snapshot_units` on the SOURCE snapshot and on the SCRUBBED one, pairs the units by position, and computes `unit_id` / `group_id` of both sides with the package's functions (module imported by path from `--package`, not copied; AR-13). `snapshot_units` returns the group id of every comment unit, so one pairing covers U- and G-. Recomputing from text alone would not have found the lines (the register holds ids, not texts).
- Id kinds in `branch_accounting.py` derived from text: `U-<12hex>` (`unit_id`, :218) and `G-<12hex>` (`group_id`, :222) - both followed. No other id in that file is derived from text (`_hex12` is private to those two).
- Order: the remap runs BEFORE the sha256 follow. Each re-keyed file feeds `follow_hash` (same logic as the existing loop), so a recorded sha256 of a re-keyed file (e.g. the register) follows its final bytes; test `test_text_derived_ids_follow_the_rewrites` has an `inv.json` recording the register's sha256 and asserts it equals the final register's.
- Refusals (named, no capture left): counts / fields / state of a snapshot differ after the scrub; two old ids on one new id (also an UNCHANGED id that a changed line now equals); one old id on two new ids. Test `test_two_old_ids_on_one_new_id_are_refused_by_line` names `description unit 1` and `description unit 2`.
- Untouched: an id-like token the functions do not produce from a captured text (`U-0123456789ab` in the test); a unit the scrub did not change keeps its id (asserted).
- No package function needed unless a snapshot-shaped file CHANGED under the scrub: a package without `branch_accounting.py` is refused only then (door named).
- README.txt: `U- N ids M replacements, G- N ids M replacements` (zero when none). Also printed by `capture`.
- Real data: local-1-arm-b re-capture printed `text-derived ids re-keyed: U- 1 (1 replacements), G- 0 (0 replacements)` (the one unit `U-beb44ce1686c`, as the 5-1 report predicted).

## Edge: cart-1 scratch re-capture (temp id `cart-1-scratch`, not committed, removed)
Source `mybooks-stand/archive/cart-1-run-20261031/.../CART-1`, `--drop "*.png" "*.lock"`. Output: `text-derived ids re-keyed: U- 0 (0 replacements), G- 0 (0 replacements)`. Item 1 changes no byte for cart-1 (zero ids; no `[UG]-<12hex>` token in any differing line - checked on 4 differing files). The capture is NOT byte-identical to the committed cart-1 for a different reason: item 6 changes the example URL bytes (`canonical_ref` `https://example.invalid/1` -> `https://example.invalid/1/browse/CART-1`), which cascades to recorded sha256 values (checkpoint.json, controller.json, events.jsonl, context-bundle.*, source-inventory.json, S3 handoffs, review receipt); the committed cart-1 was also captured with other drops (`*.log` files exist only in the scratch). The edge "byte-identical" held for item 1 alone; item 6 (added later) contradicts it by design. cart-1 NOT edited, as instructed.

## Item 3 detail
The carrier row key read is `options` (a list). The real carrier `state/driver-questions.jsonl` records none (kind, bytes, ...) - assumption: a future carrier would name the key `options`; spec did not name it. Walker: a gate `expected` without `options` compares the kind only and adds the NOTE `options not recorded` (the walker edit goes beyond "ONLY item 4" of the owns line; item 3 required it).

## Item 6 detail
Form kept: `https://example.invalid/<n>/browse/REF-m`. `<n>` numbers the URL WITHOUT its tail (one host one number; `.../browse/A` and `.../browse/B` share it), the `ticket-key` row then rewrites the key in the tail with the same mapping as everywhere (test: `key REF-1 ... /1/browse/REF-1 ... /1/browse/REF-2`). The query after the key is dropped; a URL with no `/browse/` is replaced whole as before; a URL with `example` only after `/browse/` falls to the old whole-URL alternative. The existing test expectation for `https://example.org/browse/CART-1` changed to `https://example.invalid/1/browse/CART-1`.

## Item 8
- W-3: `_judge` already checks an amendment's `names` for every facet that goes through it, decision included (W-2 of this branch); no walker code needed. Test row: a decision amendment with the right name passes, a wrong name fails naming it.
- W-1: `required_today(form_text, recorded)` reads the recorded form's `contract:` and takes the required rows of `handoff.template(contract)` of the package under walk (placeholders `<...>` match `.+`); a recorded-required path not matched is `retired`: a NOTE `<path> -- the recorded form required it, today's template does not`, still listed in `handed` (so the expected list is not reported missing). No readable template: the recorded form judges, NOTE says so (only when the form has required inputs). Note: today's s1-scout-to-tester template on this branch still says `required: true` for `work/impl-diff.txt` (the critic's B-1 is a package fix, not here), so W-1 alone does not turn the impl-diff row into a NOTE until B-1 lands.

## Verification (witness)
```
python -m pytest D:/ws1/wt-td\15-cap-fix3\tools\test_story_capture.py -q
19 passed in 59.34s
```
```
python -B ...\scripts\tests\test_scenario_walk.py
PASS witness_for: a keep row that does not cover the path is not named

=== test_scenario_walk: 68/68 ok ===
```
```
python -B ...\scripts\selftest.py --limits --lang
PASS limits: SKILL.md / agents / references within size caps
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier

=== qa-factory selftest: 4/4 ok ===
```
local-1-arm-b, run ONCE with `SCENARIO_FULL=1` (`python -B ...\scripts\tests\test_scenario_local_1_arm_b.py`, exit 1), summary and every FAIL line, uncut:
```
PASS local-1-arm-b/S1/accepted
FAIL local-1-arm-b/S2/accepted - outcome: expected 'accepted', got 'refused' (work/requirements-readiness.json: open_questions[11]: needs question, severity (blocker|major|minor) and owner_role (po_ba|dev_arch|qa))
PASS local-1-arm-b/S2/handed
FAIL local-1-arm-b/S3/accepted - outcome: expected 'accepted', got 'refused' (planning_contract.py: OB-14: evidence_policy is one word of api|cli|no_write|static|ui; evidence kinds, phases and the completion condition go in completion_condition and the observation fields | planning_contract.py: OB-15: evidence_policy is one word of api|cli|no_write|static|ui; evidence kinds, phases and the completion condition go in completion_condition and the observation fields | planning_contract.py: OB-16: evidence_policy is one word of api|cli|no_write|static|ui; evidence kinds, phases and the completion condition go in completion_condition and the observation fields)
PASS local-1-arm-b/S4/accepted
PASS local-1-arm-b/gateA/question
NOTE local-1-arm-b/gateA/question: options not recorded
FAIL local-1-arm-b/gateA/decision - decision: expected 'approve', got 'refused' (structured test plan invalid: OB-14: evidence_policy is one word of api|cli|no_write|static|ui; evidence kinds, phases and the completion condition go in completion_condition and the observation fields; OB-15: evidence_policy is one word of api|cli|no_write|static|ui; evidence kinds, phases and the completion condition go in completion_condition and the observation fields; OB-16: evidence_policy is one word of api|cli|no_write|static|ui; evidence kinds, phases and the completion condition go in completion_condition and the observation fields)

=== scenario local-1-arm-b: 4/7 ok ===
```
(the walker prints an em dash after the facet name; written as a hyphen here.) The S2 "U-1183f159e0ef ... has no home" part is gone; the two genuine reds stay (S2 readiness `open_questions[11]` shape; S3/gateA `evidence_policy` OB-14..16). Package version in story.json is now `0.10.9` written by the tool (pipeline.json kept).

## Analogs noticed, NOT fixed (rule 5)
- `source_inventory.stable_source_id` (`scripts/source_inventory.py:104`): `SRC-<20hex>` = sha256 of `instance + canonical_ref`, both texts the scrub rewrites; the captured `SRC-` ids are the recorded ones while the recomputed ones would differ (seen in cart-1's context-bundle.lines.md). Same class as U-/G-, outside branch_accounting and outside this spec. Other text-derived ids in the package (not checked against captured files): `ti_<20hex>` (`contract.py:3928,3964`), `media:<16hex>` (`source_inventory.py:2473`), `host-<8hex>` (`machine_facts.py:200`), `base_slice.py:402`, `project_decisions.py:169`.
- The Cleaner counts `example-url` per distinct URL-without-tail now; README counts of cart-1 would read differently.
- `scenario_walk.py:650` world-build failure text is still cut at 300 (not a refusal line; left).

## Needed beyond the manifest
`docs/tasks/specs/reviews/td-15-local-1-0108-reds.md` (sent mid-task), `ai-packages/qa-factory/scripts/handoff.py` (`template`, `parse`), `scripts/contract.py` / `grammar.py` imports and `references/` (the synthetic test package needs top-level scripts and `references/` for `branch_accounting` to import), the cart-1 report for its capture command, `source_inventory.py`.
