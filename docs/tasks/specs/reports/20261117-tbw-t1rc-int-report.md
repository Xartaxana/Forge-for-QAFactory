# TBW-T1rc-int (t-1236) report

Base: 0c37b5da on worktree-agent-a1bfa3bfdead0ba50. Status: pins done; T1rs x3 NOT done -- question below.

## Pins (old -> new, reason)
| pin | old | new | reason |
|---|---|---|---|
| stage-joints.json told_ratchet.unsited | 11 | 17 | measured by `stage_joints.py --check` (11 stored vs 17 rows with no site: the 6 ids of spec s4.4) |
| test_stage_joints UNSITED_CAP + K12 literal | 11 / (11,11,11,[],True) | 17 / (17,17,17,[],True) | same measure; comment line added |
| K1 row count | 273 | 285 | T1r-cards-a landed 12 rows (measured len(REAL["joints"])) |
| rows-for/real runner rows | 108 | 112 | measured, +4 rows of -a |
| K6/E1 demands + K6 informed-pass | grounding demands=[] | grounding told by a path + demands=[] on a mutated copy | page-only entries owe no tokens (T1r) and F1 left no real path-told entry; the lines now judge the demands leg on a path-told copy (subject kept) |
| test_contract_slices X1-7 designer page | token `= the file name` | `id` IS its file name` | F1 demands [] ; the cd-1 row text on the page is the new carrier |

raise: told_ratchet.unsited 11 -> 17 -- T1r-cards-a rows wait for TBW-T1rc-site
(Note: the spec text said 46 -> 52; real stored base on this branch is 11 after T9a, so 11 -> 17.)

## QUESTION (T1rs x3, not edited)
test_contract_slices.py has no baseline/exception mechanism for T1rs. Reds:
- `T1rs/sited/execution_request`: `check_eq("...every row id is the literal key of a site...", sorted(r["check"] for r in rows if r["check"].startswith(fam + ":") and r["check"] not in sited), [])` got ['execution_request:fingerprint.build', 'execution_request:profile.none']
- `T1rs/marked-by-proof` (expected [], got those 2 ids x roles qa-automator/qa-runner/qa-failure-analyst, False)
- `T1rs/entry-uniform` (expected [], got those 2 ids)
Per the edge, STOP: how should the 2 ids be excepted (add a named exception set pointing to TBW1-17 in the 3 tests, or wait for TBW1-17)?

## Witness
`python -B ai-packages/qa-factory/scripts/stage_joints.py --check`: tail `... told counters: hand_cards 12, le[gacy_legs 0, unsited 17]` / `stage joints: clean`, exit 0.
`python -B .../tests/test_stage_joints.py`: `=== test_stage_joints: 340/340 ok ===`
`python -B .../tests/test_contract_slices.py` (run after the X1-7 edit, before nothing else changed): `=== contract slices ...: 528/531 ok ===`; the 3 FAILs are the T1rs ones above only.

Beyond manifest: stage_joints.py (_demands_leg), spec s4.4.
Class: other pins with `= the file name` none seen elsewhere (grep of tests not exhaustive).

## Lead decision on the question (t-1236, "решила сама") and its witness
Decision: a named shrink-only set `NOT_YET_SITED` = {execution_request:fingerprint.build, execution_request:profile.none} in test_contract_slices.py, folded into `unproved_site` (so marked-by-proof and entry-uniform expect not-call-told) and excluded from T1rs/sited; comment names TBW1-17 (TBW-T1rc-site) as the node that empties it; new row `T1rs/sited/not-yet-sited` proves a third unsited id is still refused.
Witness: `python -B .../stage_joints.py --check` -> `stage joints: clean`; `python -B .../tests/test_contract_slices.py` -> `=== contract slices (markup, generation, freshness, shipped map): 532/532 ok ===`, exit 0.
