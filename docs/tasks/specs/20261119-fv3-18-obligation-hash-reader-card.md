# FV3-18 (t-1546): `row_field_gaps` demands a per-ref `obligation_hash` the code could not have written

Draft by designer, 2026-11-19. Node `live-run-fvf/3/FV3-18`, feature F19. Finding:
`plans/piles/live-run-fvf/findings/20261117-p1b-2f-obligation-refs-hesh-trebuet-i-otkazyvaet.md`.
Decisions are the Lead's: §7 holds the forks (F1 changes the Lead's suggested mechanism; read it first).

## §0 Measurement on main (static; the builder repeats it as a run)

Two hashes exist and the brief mixes them: (a) the PER-REF hash `tests[].obligation_refs[].obligation_hash`, written by
`contract._stamp_row_refs` (contract.py:5447-5448) only `if plan_map:`; (b) the ROW hash `tests[].obligation_hash` =
`content_hash(refs)`, written by the same stamp (:5461-5462) and checked by `manifest_put.obligation_hash_problems`
(manifest_put.py:602-632). FV3-18 is about (a). `row_field_gaps` does not read (b) (REQUIRED_ROW_FIELDS, window_record.py:180-193).

Call path that reproduces (every hop read):
`window_record.row_field_gaps(entry, None, OWED, None)` -> :295 `_obligation_refs_problem(entry, plan, known)` -> :244 refs
hold an id-bearing object -> :245 `C.obligation_ref_problems(list(refs), known)` -> contract.py:5408
`_ref_shape_problems(refs, "obligation_refs", hash_required=True)` -> :5392-5394 `"obligation_refs[0]: OB-1 has no
obligation_hash (missing hash)"` -> returned as `shape` -> window_record :248-250 appends REF_REPAIR.
Minimal ref list: `[{"obligation_id": "OB-1"}]` with no plan map.

Pinned by an existing test row: `scripts/tests/test_manifest_put_merge.py:830-831` (`fv1_19_predicate`), third element:
`kinds([{"obligation_id": "OB-1"}], None) == ["shape"]` - the reader, not strict, no map, id-only ref -> shape.
Pinned at reader level: the `known_red` row `form-rounds.json:70` (`obligation_refs <- manifest_row@all ->
window_record.row_field_gaps`, node FV3-18); its feed `test_field_producers.py::_f_row_fields` (:1231-1242) passes the
filler's raw row with NO map (`obj(entry, None, plan)`).
Status: `estimate, not verified by a run` (designer has no shell). The builder runs the narrow call of the DoD BEFORE
editing and pastes its output as the red-before witness (FR-32).

When the defect bites in a real story: a stored row whose refs went through the stamp while the plan could not be read
(contract.py:5362-5367: refs "stored as sent, without hashes"), or the raw role row of the form round. With a readable
plan every road that stores a row (manifest_put.py:2848-2853; manifest_from_tests.py:1561; dry story
dry_stub.py:640 through manifest_put) stamps the hash first.

Counter-evidence that shapes F1: `test_s5_precheck.py:4818-4852` (FV1-19b N2 (c), (n)) pins that, WITH a plan map, a
stored id-only ref IS refused `(missing hash)` by the precheck (through `row_field_gaps`) and agrees with the strict
predicate. A blanket `hash_required=False` in window_record turns those rows red and removes a closable demand.

## §1 Architecture walk

- AR-22 (every field read has a producer): the reader demands the per-ref hash only where its producer (the stamp) can
  run - the producer's own condition (`plan_map` truthy). Change check: grep the readers of the changed names (§6);
  `test_field_producers.py` judges the round (canon judges; the builder deletes the `known_red` row in the same commit).
- AR-13 (one reader): `contract.obligation_ref_problems` stays the ONE predicate; window_record passes a flag, it gains
  no second parser. Change check: no new reading of `obligation_refs` outside `contract`; SIBLING_MAP axis 23 grepped.
- AR-15 / AR-28 (the stamp is the one road; an empty map never passes): unchanged - the window finish
  (controller.py:7509, `strict=True`, default `hash_required`) still refuses every hash-less ref. Change check: the
  controller and coverage_contract.py:596 calls are byte-identical in the diff.
- AR-29: the changed check judges shape/presence of a code-written field. Owner: data (code). Census rows unchanged:
  `contract.py obligation_ref_problems` class `xref`, `_ref_shape_problems` class `shape` (judgment-census.json:161,168).
  The commit carries its `judgment:` line in the form `tools/architecture_gate.py` owns (docstring item 6); the
  expected form is `none` WITH its `-- <why>` (the change narrows when a data check demands a code-written field and
  moves no judgment), never bare.
- FR-11 (a demand names a road the role has): the demand stays only where re-sending ids (REF_REPAIR) produces the hash.
- variety: axes 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13: n/a -- the change reads the presence of the plan's
  obligation map, a factory artifact identical for every product, test stack, host and language; no axis value is read.

## §2 The change

1. `contract.obligation_ref_problems(refs, plan_map=None, strict=False, *, hash_required=True)`: passes
   `hash_required` to `_ref_shape_problems`. When `hash_required` is False, a ref whose hash is absent (`None`, `""`,
   key missing) is skipped by the stale comparison at :5421 (no KeyError, no `stale`); its id is still judged
   (`unknown`). A present hash is compared exactly as today. Default True: every other caller keeps today's verdict.
2. `window_record._obligation_refs_problem` calls `C.obligation_ref_problems(list(refs), known,
   hash_required=bool(known))` - the stamp's own condition (contract.py:5443 `if plan_map:`) on the same map
   (`plan_obligation_map`). Docstring line names it. `row_field_gaps` signature and texts unchanged.
3. `_ref_shape_problems` docstring: the reader's flag is the caller's now.
4. `form-rounds.json`: the `known_red` row `"obligation_refs <- manifest_row@all -> window_record.row_field_gaps"`
   is deleted in the SAME commit (the section has no pin, form-rounds.json:4).

POSITIONAL invariant (item 2): the reader demands a per-ref hash exactly when the stamp would have written one; what
must still be refused: a wrong or non-string hash, an unknown id, a duplicate, a non-object - by every caller, and a
hash-less ref at the window finish (strict, default).
TEMPORAL: before the commit the ledger row is red-and-listed (passes); after it the round is green, so the row must
go in the same commit - left in, the reconcile fails ("a ledger row that is green", test_field_producers.py:60-72);
deleted without the fix, the round fails as new red.

## §3 Edge table (the reader `row_field_gaps` with an owed automated obligation)

| # | input | map `known` | verdict after | today | invariant protected |
|---|---|---|---|---|---|
| E1 | refs with no `obligation_id` (`[{}]`, `["junk"]`) | any | `missing` (window_record :244 treats as absent) | same | an id-less list never reads as refs |
| E1b | `[{"obligation_id":"o1"}, {}]` | any | shape (id not a non-empty string) | same | one bad item fails the list |
| E2 | `[]` | any | `missing` when owed, `''` when not | same | emptiness is the DEMAND rule's, never validity's |
| E3 | hash present and correct | present | `''` | same | a true binding passes |
| E3b | hash present, any string | absent | `''` (unverifiable, shape only) | same | no map -> no stale verdict; the strict finish refuses later |
| E4 | hash present and wrong (typed, trailing space, upper hex) | present | `stale` + REF_REPAIR | same | a hash of other bytes never counts |
| E4b | hash present, not a string (`123`, `[]`) | any | shape | same | never coerced |
| E5 | hash absent on a role-sent ref (raw row, form round) | absent or `{}` | `''` (NEW) | shape `missing hash` | the reader never demands what no road can produce |
| E5b | hash absent (`None`/`""`/no key) | present | shape `missing hash` + REF_REPAIR | same | a closable demand stays (re-send stamps it) |
| E6 | hash absent on a built (stored, stamped) row | absent | `''` (NEW) | shape | as E5; controller.py:7509 strict still refuses it |
| E6b | same row after the plan became readable | present | shape `missing hash` | same | as E5b (test_s5_precheck N2 (c)) |
| E7 | `obligation_ref_problems(..., hash_required=False)` direct, hash absent | present | no `stale`, no KeyError; `unknown` if id unknown | KeyError path unreachable today | the flag never opens the stale comparison to a missing key |
| E8 | `strict=True, hash_required=False`, no map | absent | every ref `unknown` | n/a | strict + empty map never passes (AR-28) |
| E9 | row-level `tests[].obligation_hash` absent | any | not read here | same | FV2-71's field, F2 |

## §4 Error direction of the reused function

`obligation_ref_problems` moves from one fixed strictness to a caller-chosen one. With `hash_required=False` it may err
ONLY toward "accept" and ONLY on an absent per-ref hash. Adversarial inputs that must stay refused with the flag False:
a non-string hash (`123`, `{}`, `[]`, `True`); a wrong string hash with a map (trailing space, uppercase hex, another
obligation's hash); a duplicate id with two hashes; an id of another case; `obligation_id` `""`/`7`; a non-list;
a non-object item. window_record's own direction is "not demanded" (its docstring :287-289, s5_precheck.py:3876-3877);
the gate behind it (controller window finish, strict, default flag) is not touched.

## §5 Builder card (R11-f header lines)

given: C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-18-obligation-hash-reader-card.md (§0, §2, §3, §4 - this file); C:/QAFactory/forge-repo/plans/piles/live-run-fvf/findings/20261117-p1b-2f-obligation-refs-hesh-trebuet-i-otkazyvaet.md; C:/QAFactory/forge-repo/plans/piles/live-run-fvf/findings/20261114-row-field-gaps-i-kontrakt-rashodyatsya-ob-obligation-hash.md (sibling, read only); ai-packages/qa-factory/scripts/contract.py::obligation_ref_problems, ::_ref_shape_problems, ::_stamp_row_refs; ai-packages/qa-factory/scripts/window_record.py::_obligation_refs_problem, ::row_field_gaps; ai-packages/qa-factory/scripts/tests/test_manifest_put_merge.py::fv1_19_predicate; ai-packages/qa-factory/scripts/tests/test_s5_precheck.py::fv1_19_obligation_refs_at_the_precheck (must stay green); ai-packages/qa-factory/scripts/tests/test_field_producers.py::_f_row_fields
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/contract.py (obligation_ref_problems, _ref_shape_problems docstring only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py (_obligation_refs_problem only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json (the one known_red row of FV3-18 only)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manifest_put_merge.py (fv1_19_predicate rows only)
non-goals: acceptance.py and the row-level `tests[].obligation_hash` (FV2-71, F2); artifact-contract-automation.md (F3); manifest_put.py; the stamp's behaviour; controller.py and coverage_contract.py call sites; the quarantined test_row_fields.py; any new test file
handoff: report C:/QAFactory/forge-repo/docs/tasks/specs/reports/20261119-fv3-18-report.md + one commit on the node branch; the report carries the red-before and green-after outputs of the narrow call, the DoD run tail, and the line `not run locally: test_field_producers.py, test_s5_precheck.py, test_window_record.py, canon judges`
edges: §3 rows E1-E9 and §4 adversarial list of this card are the expected values; POSITIONAL: the reader's flag is `bool(known)`, the stamp's own condition on the same map - a wrong/non-string hash, unknown id, duplicate, non-object stay refused by every caller and a hash-less ref stays refused at the window finish; TEMPORAL: the known_red row is deleted in the same commit as the fix, never before or after; a ref list the predicate cannot read (non-list) stays shape regardless of the flag
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manifest_put_merge.py` green; plus the narrow call (canon-class readers) `python -B -c "import sys; sys.path.insert(0, r'C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts'); import window_record as WR; ow=[{'obligation_id':'OB-1','decision':'new'}]; r={'assertion_id':'a','defect_location':'d','change_disposition':'unchanged','change_basis_ref':'b','obligation_refs':[{'obligation_id':'OB-1'}]}; print(WR.row_field_gaps(r, None, ow, None)); print(WR.row_field_gaps(r, None, ow, {'OB-1': {'obligation_id':'OB-1','decision':'new'}}))"` run before the edit (both lines show `(missing hash)`) and after it (first line `[]`, second line still `obligation_refs ... (missing hash)`); the diff shows the controller.py and coverage_contract.py calls untouched
test: ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json known_red row deleted - the FV3-18 round of test_field_producers.py turns green (canon judges) | expected from: finding item 2; §2 item 4 and TEMPORAL of this card
test: ai-packages/qa-factory/scripts/tests/test_manifest_put_merge.py::fv1_19_predicate, variant rows beside the table at :830-831 - `hash_required=False`: id-only ref with no map -> `[]`, with the map -> `[]`; a wrong string hash with the map -> `["stale"]`; a non-string hash -> `["shape"]`; unknown id hash-less -> `["unknown"]` | expected from: §3 E5, E7, E4, E4b and §4
test: ai-packages/qa-factory/scripts/tests/test_s5_precheck.py::fv1_19_obligation_refs_at_the_precheck - no new row; its N2 (c)/(n) `missing hash` rows must stay green unedited (canon judges) | expected from: §3 E5b, E6b
siblings: FV2-71 (same files window_record.py, acceptance.py, contract doc; row-level hash; touch no line of it); SIBLING_MAP axis 23 (`REQUIRED_ROW_FIELDS` carrier - unchanged, no edit); FV1-19 b/e stamp tests in test_manifest_put_merge.py (unchanged rows)
readers: §6 of this card; owns_readers block not attached - the Lead runs `python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/contract.py ai-packages/qa-factory/scripts/window_record.py ai-packages/qa-factory/scripts/tests/fixtures/form-rounds.json --names obligation_ref_problems _obligation_refs_problem` before dispatch
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261119-fv3-18-obligation-hash-reader-card.md

Test budget: code lines ~8-12 (signature, one condition, one call argument, docstrings); test lines must not exceed
them - the second `test:` line is at most one `check_eq` over five calls. Commit: AR-22, AR-13 and the `judgment:` line
per §1; release files in English (FR-30, `python -B scripts/selftest.py --lang` is CI's).

## §6 Readers of every touched file / changed name (hand grep; owns_readers block missing)

| reader | reads | after the change |
|---|---|---|
| controller.py:7509 window finish | `obligation_ref_problems(refs, map, strict=True)` | unchanged (default flag) |
| coverage_contract.py:596 | `obligation_ref_problems(refs, plan_map, strict=True)` | unchanged |
| window_record.py:245 `_obligation_refs_problem` | the predicate | changes in this stream (flag `bool(known)`) |
| manifest_from_tests.py:1736 `_row_form` | `row_field_gaps(entry, cfg, owed, known)` | unchanged code; form stops asking a hash-less ref when no map (E5) |
| s5_precheck.py:3905 `check_row_fields` | `row_field_gaps` | unchanged code; with a map same verdict, without a map E5/E6 |
| contract.py:5436 `_stamp_row_refs` | `_ref_shape_problems(..., False)` | unchanged |
| judgment-census.json:161,168 | rows of both contract functions | unchanged (class, owner, roles) |
| test_manifest_put_merge.py:814-882 | default-flag rows | unchanged; new variant rows in this stream |
| test_s5_precheck.py:4850 | predicate strict | unchanged, must stay green |
| test_controller_state.py:611,618 | predicate strict | unchanged |
| test_field_producers.py (via form-rounds.json:29 reader row, :70 ledger) | the round + ledger | ledger row deleted in this stream |
| tools/lint_ratchet.py:69, tools/test_lint_ratchet.py | `form-rounds.json` `hand_inputs` only | unchanged |
| scripts/tests/form_filler.py | `form-rounds.json` (languages_source) | unchanged |
| test_row_fields.py (quarantined) | `row_field_gaps` | unchanged; already stale on main (K1 `marker`, K2 (o) junk) - not this node |

Commands (Grep tool, ripgrep): `obligation_ref_problems|_ref_shape_problems|stamp_obligation_refs\(` over
`ai-packages/qa-factory` -> code callers above; `row_field_gaps\(` over `ai-packages/qa-factory/scripts` -> 2 code
callers + tests; `form-rounds` over `tools/` -> lint_ratchet.py, test_lint_ratchet.py; `obligation_ref_problems|
row_field_gaps|_obligation_refs_problem` over `tools/` -> 0 hits, positive control `form-rounds|lint_ratchet` same
tool/dir -> 38 hits in 9 files.

## §7 Forks (questions for the Lead)

- F1 (mechanism; changes the brief's suggestion). Options: (A) window_record always passes `hash_required=False`;
  (B) passes `bool(known)` - demand the hash exactly when the stamp would have written it; (C) window_record stamps a
  copy of the refs itself before judging. Recommend (B): it clears the FV3-18 round (no map), keeps
  test_s5_precheck N2 (c)/(n) green (with a map a stored hash-less ref is closable by REF_REPAIR - the stamp now
  writes it), and adds no second stamp road (C breaks AR-15). (A) turns N2 (c)/(n) red and lets a closable defect
  pass the precheck to the strict finish, a later and costlier refusal. "Role-sent vs built" is not readable from a
  row (a stamp with no map also writes `obligation_ids` and a row hash, :5460-5462); the map is.
- F2 (acceptance.py:1218). It reads the ROW/instance `obligation_hash` that `window_record.build` writes
  (`content_hash(refs) if refs else ""`, window_record.py:1648); it fires only when the instance has NO refs - which
  also fires `obligation_binding` (:1214-1217). That is FV2-71's class and subject (finding 20261114, "a row with no
  refs, nothing to hash"), not FV3-18's per-ref hash. Recommend: OUT of scope; FV2-71 keeps it with its real-run
  measurement first.
- F3 (contract text). artifact-contract-automation.md:159 says each instance "carries `obligation_refs`
  (`[{obligation_id, obligation_hash}]`)" without saying the code writes the hash; :168-170 "never send it or
  `obligation_hash`" belongs to `obligation_bindings[]`. The role's ids-only rule lives in REQUIRED_ROW_FIELDS.what
  (window_record.py:190) and the printed form. Options: add one clause "send ids only; the code writes each hash" at
  :159 (owns widen; role-load text grows); or leave it. Recommend: leave it in this node (no reader is wrong); offer
  the clause to the next contract edit.
- F4 (release bookkeeping). Whether this node carries a CHANGELOG line / version bump is the Lead's process; the card
  owns neither file.

## §8 Small choices closed by the designer

- `hash_required` is keyword-only (`*,`) so the existing positional calls `(refs, m, strict)` cannot shift.
- The flag's name is `hash_required`, mirroring `_ref_shape_problems`.
- Empty map `{}` counts as no map (`bool({})` is False), matching the stamp's `if plan_map:`.
- Test place: `fv1_19_predicate` in test_manifest_put_merge.py (fast: absent from slow_tests.json, not a
  `canon_only` mask), not test_window_record.py (slow, 77.0) nor test_row_fields.py (quarantined).
- REF_REPAIR and every refusal text unchanged.

## §9 Contradictions in the brief

- "manifest_put.py refuses a role-sent hash": `obligation_hash_problems` refuses a WRONG row hash and accepts a
  correct one (manifest_put.py:611-631); the stamp accepts a correct per-ref hash and refuses a wrong one
  (contract.py:5447-5450). The Lead's invariant "present but wrong stays refused" holds; "never sends" is a door, not
  a refusal of a correct value.
- The contract line cited (:168-170) is about bindings, not refs (F3).
- The FV3-18 red row is on main (form-rounds.json:70), not only on `wip/p1b-n4m` as the finding's "source not found"
  says.

## §10 Reading trail

Read: finding FV3-18 (whole); finding FV2-71 (whole); contract.py:5360-5468; window_record.py:130-329, :1630-1651;
manifest_from_tests.py:1548-1568, :1700-1787; s5_precheck.py:3870-3913; controller.py:7500-7515;
acceptance.py:1190-1229; manifest_put.py:602-632 and grep :2846-2862; artifact-contract-automation.md:150-177;
form-rounds.json:1-12, :66-73; test_field_producers.py:40-72, :1225-1248; test_manifest_put_merge.py:800-882,
:1598-1635; test_row_fields.py:30-170; test_s5_precheck.py:4786-4865; dry_stub.py:596-645; docs/TESTING.md:75-106
and greps; architecture.md:44-72, :173-186, :200-205, :274-279; tools/architecture_gate.py grep `judgment`.
Greps (Grep tool): `def obligation_ref_problems|def _ref_shape_problems|hash_required` (contract.py, 6 hits);
`obligation_ref_problems|_ref_shape_problems|stamp_obligation_refs\(` (package); `row_field_gaps\(` (scripts);
`obligation_hash` (acceptance.py: :1218, :1219, :1270) and (window_record.py); slow list
`"test_s5_precheck.py"|"test_controller_state.py"|"test_manifest_put_merge|"test_coverage_contract.py"` -> 2 hits
(controller_state, s5_precheck), control: the same file found test_field_producers.py and test_window_record.py with
the same form; `canon_only` (test-layers.json:13-18); census `window_record\.py.*(obligation_refs|row_field_gaps)|
contract\.py.*obligation_ref_problems` -i -> only contract row :168 (window_record functions have no census row).
Not measured (no shell): any run; owns_readers block; wall time of test_manifest_put_merge.py (estimate: fast class).
