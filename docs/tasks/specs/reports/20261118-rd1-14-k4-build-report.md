# t-1492 — RD1-14d (k4, the conversion): builder report

## Plan items (card section 6, items 1, 2, 4; item 3 moved into k1 per P-7)

- 1 Row `provenance_acceptance`: DONE. `vocabulary: code`, `field: null`, `status: converted`, `debt_ref: ""`; `decides` names the producer, the predicate, each consumer's tokens and the unknown door. `references/gate-registry.json`
- 2 F-1 (a) deletion: DONE. `acceptable_provenance`, `ACCEPTS` and the registry site are gone (`profile_contract.py`, `gate-registry.json`); readers: `driver_stage_build.build_outcome` (point-of-use `from gate_template import acceptable`, `provenance.rehearsal`), `test_execution_request.py` E11 row (inline form, `provenance.run`; the `ValueError` row became "an unknown consumer is False"), `test_runtime_probe_onboarding.py` three functions (`provenance.run`; matched-only -> `environment_preparation.deploy_proof` with a comment; `("matched","person_confirmed")` -> `provenance.identity`), `test_role_commands.py` literal list with a comment naming `provenance.run`.
- 4 Census row: DONE. `judgment-census.json` row `profile_contract.py::acceptable_provenance` removed; the census test names a vanished unit `stale row ... no such check unit` (C1, `test_judgment_census.py:326-329`). The unit carried a blocking raise, so the C3 ceiling `blocking_per_role.conductor` 749 -> 748 (measured, below).
- Pins that move: DONE, `test_gate_registry.py` by symbol: `EXPECTED_DEBT = {}`; `EXPECTED_CONVERTED` +1 with AR-20 comment; `check_not_in("left as debt")`; split counts 28 / 0 / 6; F4 `code` list +1; K-N2.12 positive control on `provenance_word`; F2 live check on the `PROVENANCE_RESULTS` `<module>` item (exists, line 21: no STOP); D13 triple removed, `D13_ITEM_COUNT` 173 -> 166 (measured `GR.analyse` after: 166; the allow pin unchanged); `predicate_cases` `live-record` -> False; the `--json` debt-item key check became "debt == []" (it read `data["debt"][0]`, E-k4.3).
- Test rows: the card's two `test:` lines are covered by the moved pins (`live-record` False; the registry-unreadable row went to k1 with item 3). No new test lines; every edit is in place, so tests not written: none.

## Witness (verbatim; one run after the code edits, then the onboarding file again after its import fix)

```
## gate_registry --check
exit 0
A26 gate registry: no violations
  blind spot: a gate that compares only non-anchor words, ...
grep -c "left as debt" -> 0
## --json: debt [] findings []
## test_execution_request: exit 1, 1 FAIL, === test_execution_request: 727/728 ok ===
   FAIL B-2: the sixth is not named -- 'c5' unexpectedly found in: ... \.claude\worktrees\agent-ade9bd63928efdfc5\ai-packages\qa-fact...
## test_gate_registry: exit 0 === test_gate_registry: 559/559 ok ===
## test_runtime_probe_onboarding (first run: NameError, three imports missing; fixed, re-run): exit 0
=== test_runtime_probe_onboarding: 729/729 ok ===
PASS written-accepts (I-1): not_applicable is accepted, no unknown ever is
PASS K10 rehearsal: the STRICT validator refuses that record (no evidence file): only the rehearsal reader takes it
PASS K13: and it is NEVER taken for matched by a caller that wants a verified build
```

The one FAIL (B-2, an `AK` row about "the sixth container is not named") is an artifact of the worktree path: the path
`agent-ade9bd63928efdfc5` contains the string `c5`, which the row looks for in the message (the message carries the path; positive
check: `grep -o '.\{40\}c5.\{20\}'` on the run output finds the path). Not related to this change; it passes in a path without `c5`. Its row is
not among the DoD's named functions; `n2_k1_probe_runtime_is_the_one_predicate` and `c3_k1_one_producer_names_the_provenance_word` have no FAIL line.

Judgment census (measured read-only, `T.analyse(root, census)` of `test_judgment_census.py`, not the test run): before the ceiling edit
`{'C3': ['blocking_per_role.conductor is 748, below its ceiling 749']}`; after: `{}`. Not run locally: judgment census and role commands files, canon judges.

## Recorded-data control (DOC-DISPATCH witness; never committed)

Script: the k1 report's "Updated control script" (`docs/tasks/specs/reports/t-1361-rd1-14a.md` lines 326-441), extracted verbatim by
`sed -n '326,441p'` to the scratchpad `provenance_vector.py`; the frozen vector is that report's lines 265-274 (171 records, 684 bits per consumer).
`recast` and `new` take the same inline branch in that script (as k1 wrote it). Run: `python -B provenance_vector.py ai-packages/qa-factory <new|recast|bad> <nine consumers>`.

```
new / recast (identical), all nine consumers:
provenance.automation n 684 true 486 sha 1d79f21fcc3fd23d
provenance.rehearsal n 684 true 596 sha e99875bc172e64fa
provenance.fingerprint n 684 true 600 sha bbe713dc387e7f10
provenance.manual n 684 true 486 sha 1d79f21fcc3fd23d
provenance.identity n 684 true 592 sha 3486d67a5e9442aa
provenance.run n 684 true 592 sha d47681b725c88c33
provenance.manual_capture n 684 true 482 sha 554618fee50c364c
baseline_identity.capture n 684 true 376 sha 8092e3a43dbcd52e
environment_preparation.deploy_proof n 684 true 364 sha eada1a419cf92c25
diff --strip-trailing-cr frozen.txt out_new.txt -> "new == frozen"; same for recast -> "recast == frozen"
bad (consumer nope.x), all nine: true 0 sha 5aeb13c43524c909 (differs from every frozen sha; no frozen `true` is 0)
```
Negative control: `bad` is the control; every frozen sha differs. `old` cannot run (the function is gone), as the card says.
Script source: see the k1 report lines 326-441 (the same bytes; attached by reference to the frozen file, not retyped).

## Greps

- E-k4.5, `acceptable_provenance|\bACCEPTS\b` over `scripts/*.py` (control: the same call found the pre-edit hits): no import of a deleted name in a keep or package file. Remaining hits: prose `execution_request.py:2586`, `runtime_probe.py:57` (docstrings naming `acceptable_provenance`; not in owns), `gate_registry.py:42,406` (non-goal); `profile_contract.py:913` (mine, says "deleted"); `test_gate_registry.py:630,763-785` (synthetic source text of scanner tests); quarantined readers (report line, F-r2-2 (a)): `test_profile_contract.py:142,291,292,296,340,385,471,479,500,504,505` and `test_launch_wrappers.py:163,167` (a `mock.patch.object(.., "acceptable_provenance")` that already named nothing after k2).
- Axis 5 prose twins (`execution-lifecycle.md`, `manual-evidence.md`, `environment-preparation.md`, `phases/s5.md`, `s6.md`): zero hits for the old names (control: Grep over `*.md` found two sibling hits, below). Other `.md` hits: `design/factory-rules-debt.md:101` (non-goal, S1b/RD1-23), `CHANGELOG.md:5309` (history).

## Test volume (commit 3fbce261)

The commit hook WARNs `+37 test lines vs +9 product lines` (added-lines count; the product side is mostly deletions: about 40 lines of `acceptable_provenance`/`ACCEPTS` leave). All 37 are pins that move and in-place rewrites of existing readers (card: "pins that move ... are not behaviour lines"); no new behaviour row was written. A `tests-over:` word is the Lead's.

## Needed from integration

- `ai-packages/qa-factory/scripts/runtime_probe.py:57`: `profile_contract.acceptable_provenance(rehearsal=True)` -> `acceptable(provenance_word(rehearsal=True), "provenance.rehearsal")` (docstring, names a deleted function). Also `execution_request.py:2586`: the docstring word `acceptable_provenance` -> `provenance_word`. Neither is in owns.
- `design/factory-rules-debt.md:101` row FR-59 still says "conversion owed ... `acceptable_provenance`" (S1b / RD1-23).
- Quarantined `test_profile_contract.py` and `test_launch_wrappers.py` still name the deleted function and `ACCEPTS` (listed above); never run or edited here.

## Config keys

None.

## Changelog fragment

`ai-packages/qa-factory/changelog.d/rd1-14-k4-provenance-acceptance-converted.md`.

## Decided differently from the plan / divergences

- Census ceiling `blocking_per_role.conductor` 749 -> 748: not named in the card; the census analyse measured it and the test says "lower the ceiling". Item 4's "names it gone" condition holds (C1 stale-row text).
- `decides` text lists tokens by consumer name in words; the `identity` entry is spelled "matched and person_confirmed only".
- F2 live check source test: the `<module>` item's `source` is the bare set (no variable name), so the check reads `startswith("{'matched', 'mismatched'")`.
- A shell edit by `sed -i` was refused by the worktree guard once, so the three imports in `test_runtime_probe_onboarding.py` were added by Edit after a first NameError (lines 787, 1246, 1370 after edit).

## Same-class notes (no edit)

`test_gate_registry.py` K-T1.7 line 630 keeps the name `acceptable_provenance` as the "a call to a different function is not the predicate" sample; harmless synthetic text.
