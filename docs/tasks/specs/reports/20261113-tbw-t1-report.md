# T1 report (told-before-work, rows v2 + reader + gate) -- PARTIAL, context cap reached; remainder listed

Branch `wip/tbw-t1`. Commit: see the final message (hash of the commit that carries this file).

## 1. What is done (committed, green)
1. T0-gate change (1), the FIRST step: `refusal_registry._scan_wide` -- a stderr print/write is a refusal site only when the NEXT
   statement of the same block is a failing `return` (non-zero / `EXIT_*` name), `sys.exit(<non-zero>)` or `raise`
   (`_fails_stmt`, `_stderr`, `followed`). Any other stderr text is the counted blind spot "stderr text not followed by a failing
   return, sys.exit or raise in its block (a note, a progress line)". The old `fails` / `returns_expr` sets are gone.
2. T0-gate change (3): `refusal_registry.check_of(entry)` = `<file stem>:<id>`, census row
   `refusal_registry.py::check_of` (class `shape`, roles `["conductor"]`, owner `data`) added to `judgment-census.json`.
3. Tests (`test_refusal_registry.py`): the stderr rows re-cut to the new rule (6 "not a site, counted" rows, a `raise` row, the
   `EXIT_`/`sys.exit(2)`/`-1` site rows kept, the `h` fixture row) and `part_check_of` (4 rows).
4. changelog fragment `changelog.d/tbw-t1-rows-v2.md`.

## 2. Join numbers (verbatim tool output; command
`python -B scripts/refusal_registry.py --sites --wide --census scripts/tests/fixtures/judgment-census.json --json`)
BEFORE (T0 report, base c973298): `sites 3117, units 848, units_with_row 732, units_no_row 116, join_share 0.8632, role_reachable_units 170, per_transport stderr-print+return 328`.
AFTER change (1), this branch: `'sites': 3030, 'units': 836, 'units_with_row': 723, 'units_no_row': 113, 'join_share': 0.8648325358851675, 'role_reachable_units': 168, 'conductor_only_units': 555, 'role_reachable_sites': 687, 'stderr-print+return': 241, 'stderr-write+return': 0, 'walk_errors': 0, 'check_arg_errors': 1`.
Blind spot now counted: `stderr text not followed by a failing return, sys.exit or raise ...: 213`.
113 units are still rowless; ALL are units that exist only through the new transports (stderr-print+return and `refuse`), e.g.
`arch_check.py::main, archive_task.py::{cmd_archive,cmd_undo,main}, artifact_supersede.py::main (11 refuse), plan_row.py::{add_row,main,put_row,set_fields,...}, stage_done.py::{main,record_acceptance,set_facts}, ticket_adapter.py::{_query,fail,_accept_gap_kind}, walk_session.py::{call,main,open_walk}, handoff_check.py::_apply_one, ...` (full list: the `units` array with `roles: null` of the command above).

## 3. STOPPED: questions for the Lead (the edge "join under 100 % -> stop" and gaps in the spec)
Q1 (census rows, blocks the join to 100 %). Rows for the 113 wide-only units cannot be added: `test_judgment_census._c1` reports every row
whose unit its own scan does not create as `stale row` (units come from `sites()` without the new transports; `main` is not a
`UNIT_NAME_RE` name). Landing them needs an edit of `scripts/tests/test_judgment_census.py` (`units_of` creating units from the wide
sites) -- not in my owns -- and that edit flips `blocks` on those units, so `blocking_per_role` for every non-conductor role named in
a row RISES (a shrink-only ratchet; the edge forbids it without a question). Needed from the Lead: (a) permission/owner for the
`test_judgment_census.py` edit; (b) the roles per unit (the Lead's T0-gate text says "role-reachable CLI entry points": which roles
call which CLI is judgment I did not make), or "conductor" for all with a note; (c) the named `blocking_per_role` raise per role.
Q2 (rename, item (f), underspecified). "43 rows renamed, literal at the call is the key" gives no mapping. Facts found: since P1-v N0
(merged in this base) `exit_gate.all_errors` wraps each family in `own(...)`, so `stage_joints.exit_members` now reads
`exit:own` and 3 other keys (`exit:detector_errors, exit:own, exit:text_end_after_handback, exit:witness_errors`, 4 instead of 8).
`test_stage_joints.py` is RED on this base for exactly that reason (K1/K2/K3/K6: "exit checks: 4, pinned 8", 14 FAIL of 111) --
this is NOT caused by my change (my `stage_joints.py` is HEAD; verified with `S.universe()` above). Runtime ids after N0 are
`exit_gate:scoped|grounding|case_identity|digest` (exit_gate.py:1881, f-string -- itself a walk error `check_arg` of the T0 scan, 1 on
the real tree), `<producer stem>:<label>` for detectors (`detector_records`), `<stem>:unreadable|defect|unmigrated`. Needed: the
mapping of all 43 old keys (8 exit, 8 detector, 27 window) to new keys, and whether the exit_gate f-string becomes literal calls
(exit_gate.py is not in my owns).
Q3 (K1 universe, item (c)). Universe = v1 kinds + literal ids + A24 `check_of` would make K1 red at T1 on the real tree: 102 A24 ids
have no row until T1r, and exit_gate.py:1881 is a non-literal check. What is K1's outcome for an A24 id with no row between T1
and T1r (spec E6: "before T1r no new requirement rows")? My draft makes the ids opt-in (`universe(ids=check_ids())`) -- not committed.
Q4 (confirm). `rows_for` returns only rows that carry `requirement`/`requirement_from` (schema-1 rows say no sentence; returning all 43
legacy rows would put sentence-less lines on a page). The spec says "rows naming the role in a producer". Confirm or correct.
Q5 (baselines, item (d)). K4/K6 baselines are the per-unit counts of role-reachable units by the census join; they change when Q1 is
answered, so I did not write `told_ratchet` yet (T0's numbers, recomputed: bare per role-reachable unit = 687 sites in 168 units).
Q6 (E11). Data cannot tell "never sited" from "gone after being sited" (no flag on the row); I would count by the `unsited` baseline
only (above baseline = red) -- the "red at once after sited" half needs a field. Confirm or name the field.

## 4. Remainder (not done), in order
(a) v2 migration of `references/stage-joints.json` (schema_version 2, `when_kinds`, `when_exclusive`, `told_ratchet`) + the 43
renames (Q2); (b) `stage_joints.py`: the reader/renderers are DRAFTED in full (load_rows, row_for, rows_for, fill, told_text,
told_line, check_ids, universe(ids=), `_vocabulary_problems`, v2 constants) in the scratch file
`C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\61b75a79-16bf-492f-9cd2-02266607001d\scratchpad\stage_joints.partial.py`
(NOT committed: schema constants flipped to 2 while the data is v1 and `audit`/`main`/`threshold`/`_row_problems`/`_told_leg`/
`_direction_a`/`_ratchet`/`Report` not yet adapted, so it is red alone); still to write: K3/K7/E4/E7/E11 checks in `_row_problems`,
the gated page leg (`contract_slices.requirement_section` attribute) and conductor leg in `_told_leg`, `unsited` vs stale in
`_direction_a`, `legacy_legs` (= told items whose path is not `references/slices/<role>/handoff-keys*.md`; today 9, L1-L9 of
wave0-rows item 7) and `unsited` counters in `_ratchet`/`Report`; `audit/main/threshold` through `load_rows` (note: the K13 test bodies
need `schema_version: 2`; `threshold` must read the module `DATA` at call time, `test_retro_numbers` retargets it);
(c) `contract_slices._keys_outputs` through `stage_joints.load_rows` (line ~490), `selftest.py:722` through `load_rows`; the AR-13 grep;
(d) tests rows: K1/K3/K7/E4/E7/E11 one row each, K4/K5/K6/K12 + `conductor_only` print per group (G-dispatch reasoned by the
file/function names of spec 2.8; the rest not separable by code), subprocess import row (h), page-leg gate both ways (k), `rows_for`
conductor row (l), `test_contract_slices.py` row for (i).

## 5. Verification (verbatim)
```
test_refusal_registry.py            === test_refusal_registry: 493/493 ok ===
test_judgment_census.py             === judgment_census: 24/24 ok ===
refusal_registry.py --check         A24 refusal registry: no violations   (last line of the tail shown was a registry listing; exit 0)
selftest.py --lang                  PASS lang: no control byte left by an eaten escape sequence (FR-29) / === qa-factory selftest: 2/2 ok ===
test_stage_joints.py                === test_stage_joints: 97/111 ok ===   RED on the base (Q2), not touched by this commit
```
Not run: test_stage_joints_12586.py, test_contract_slices.py (no change in their owned code), scenario_walk witness narrowed run, the
slow files. Pre-existing reds named by the Lead (role-load K10-b/c, audit-rules A22/A27) not run.

## 6. FR walk
A -- refusals: no refusal text of the package changed. B -- not applicable. C -- the wide record shape (a dev tool's output) keeps
its fields; the new blind-spot label replaces two labels (FR-14: counted, named). D -- `check_of` computes an id from the registry
entry, never typed twice (FR-16). E, F -- one line: numbers above carry their command. G -- English, no heredoc code, tests in the
keep file (FR-28/30/32).
architecture: AR-13, AR-20 -- the one scanner narrows its stderr transport in place; census rises by exactly one named row (check_of), no ratchet counter moves
judgment: none -- AST shape of a statement pair; the census row is `shape`/`data`

## 7. Needed beyond the manifest
`scripts/exit_gate.py` (own()/with_check at :1881), `scripts/detector_verdict.py`, `scripts/tests/test_judgment_census.py`, spec `reviews/`, `wave0-rows.md` item 7.
