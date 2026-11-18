# t-1181 — code critic, RD1-22 / card FL9 (commit 6d05f3fd, t-1167)

Spec: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` :1497-1510 (card FL9), plus the Lead's E1 decision (17.11) as the
dispatch restates it. Branch `worktree-agent-ad30c6b4429bfe57a`, worktree `.claude/worktrees/agent-ad30c6b4429bfe57a`.

## Verdict

**NEEDS WORK** — 0 findings block the merge outright; 6 must be fixed before merge (F1-F6), and F1 needs the Lead to pick a road
first. The marker road (`.py`) works and keeps today's text. Nothing in the branch names a language (verified). The new
manifest_put road does **not** behave like the marker. If the author follows the printed door word for word, the manifest
ends up holding the Then both as proved and as declared open. The open-oracle gate then goes silent while the proof row stays.

Why this is not a REJECT: the case's ledger row still says `not_verified:expectation_unconfirmed`. `ledger.py:851-856` reads
`unconfirmed_bindings` before it looks at any covered row, so no false green reaches a person through the ledger. I did not
walk every reader of covered `then_bindings` rows, such as coverage per requirement in the report. If the Lead knows of a
reader that prints a requirement as covered from such a row, F1 moves up to blocks.

## Findings

**F1 (fix before merge; a fork for the Lead) — the manifest_put road leaves the covered row of the Then, unlike the marker road.**
Surface: `then_bindings` merge semantics, writer vs hand fragment.
- Marker road (`.py`): `manifest_from_tests._merge_bindings` claims the pair (case, then) of each marker row (`claimed = {key(r)[:2] for r in mine}`).
  So the old covered row `(TC-500, 2, <iid>)` is dropped when the writer re-runs.
- Hand road (the new door): `manifest_put._merge_then_bindings` merges BY UNIT (case, instance_id) (`manifest_put.py:1453-1457` `_in_unit`, :1539-1585).
  The door's row has `instance_id: null`, which is a unit of its own (`_in_unit` docstring). The covered row's unit `(TC-500, XTests.Foo)` is not
  named, so it stays. For a non-Python file the writer sends no `then_bindings` key at all (`manifest_from_tests.py:1539-1541`, `if bindings or whole_unresolved`),
  so "re-run manifest_from_tests.py" does not clean it either.
- Probe (pure functions, scratch script; output verbatim):
  `AFTER MERGE: [{"case": "TC-500", "then": 2, "instance_id": "XTests.Foo", ..., "status": "covered"}, {"case": "TC-500", "then": 2, "instance_id": null, ..., "status": "unresolved", "reason": "expectation_unconfirmed", "question": "Q4", ...}]`
  / `declared: [2]` / `asserting: {2: ['XTests.Foo']}`. So `check_open_oracle_asserted` skips Then 2 (`number in declared`, s5_precheck.py:1765),
  while the contract line "A Then is proved by a test or left, never both" (`references/artifact-contract-automation.md` :62-63) no longer holds. Nothing
  refuses this for `expectation_unconfirmed`: the never-both refusal at s5_precheck.py:1631 reads only `then_remainder_rows` (handed_to_person by default, contract.py:294).
  The covered row's `assertion_ref` also points at the assert the door told the author to remove.
- A road that works by data alone exists only in part. Probe 2: re-sending the instance's unit without Then 2, plus `"retract": ["then_bindings"]`,
  takes the covered row out when the unit has another Then (`(a) two-Then unit, retract: [(1,'XTests.Foo','covered'), (2,None,'unresolved')] removed 1`).
  It does NOT when Then 2 is the unit's only row (`(a) one-Then unit, retract: [(2,'XTests.Foo','covered'), (2,None,'unresolved')] removed 0`):
  a unit is named only by sending a row of it.
- Options for the Lead: (a) the door builds, from the manifest it already holds (`asserting[number]`), a fragment that re-sends each
  asserting unit without Then n plus `retract`. This fails for a one-row unit, so it needs a supplement. (b) The fragment carries a twin row ON each asserting
  instance (`instance_id: <iid>`, status unresolved, reason expectation_unconfirmed). The twin replaces the covered row in place
  (`_twin`), but the contract's ":56-57 a null instance_id" would have to change. (c) A manifest_put door that drops one Then row of a unit. Each choice
  has a cost and touches files outside this node's owns, so the Lead decides.
- Answer to the dispatch's deviation question: the row's SHAPE passes the contract and matches the marker's row field for field
  (`manifest_from_tests.py:1254-1262`: `{case, then, instance_id: None, assertion_ref: None, status: "unresolved", reason, question, observed?}`).
  `manifest_put.then_remainder_problems` does not judge it (it is not a remainder reason). `ledger.unconfirmed_bindings` (ledger.py:128-138) and the gate read it as the declared open part.
  But it is not "exactly like the marker": the marker's road also removes the proof row, and this one does not.

**F2 (fix before merge; same function, rule 9 sweep of the artifact) — the rest of door A still prints the Python forms on the manifest_put road.**
`s5_precheck.py:1721-1723`, inside `_open_oracle_door`, comes right after `bind`: "keep an assert only for the part a source establishes (bound with
`qa(then=[{number}])`; a status range keeps `# oracle_unknown: {ref}` on its line), and re-run manifest_from_tests.py". Verbatim from the probe, door for
`tests/XTests.cs`: "bind it with `manifest_put.py --task <T> --fragment <file>` with the fragment `{...}`, keep an assert only for the part a source
establishes (bound with `qa(then=[2])`; a status range keeps `# oracle_unknown: Q4` on its line), and re-run manifest_from_tests.py".
- `qa(...)` is the pytest marker, `#` is not a comment in C#/Java/TS (`detectors.json` `line_comments: ["//"]`), and the writer writes no Then rows for those files.
- One packet now contradicts itself (FR-10), and the P31 residue of the card stays in the same sentence the card targets.
- The binding of the established part belongs to "the binding road" of the card's Item. It follows the same capability: the marker
  form on a marker row, the fragment's covered-row form otherwise.

**F3 (fix before merge; Q6) — the road prints `--task <T>` although the task is known.**
`s5_precheck.py:1720` uses raw `FRAGMENT_ROAD`. The helper `_road(task)` (s5_precheck.py:664-666) fills the slot. The same door fills
`--task {task_name}` in its `question_register.py` half (probe: `task in door road: False True`). That leaves a door the author must complete when the
code could complete it (FR-2), and an existing helper is not reused.

**F4 (fix before merge; Q6/Q7) — `_oracle_binding_form` reaches into the private `assertion_detectors._document`, and on an unreadable table it is silent.**
- Every other caller of `_document` is inside `assertion_detectors.py` (:250, :296, :334; grep `_document(` over `scripts/*.py`, which finds those three as the positive control).
- The sibling reader in the same file, `_baseline_tokens` (s5_precheck.py:2646-2658), uses the public `AD.shape_patterns` and appends a NOTE when the key is unusable.
  The new reader returns `''` with no note. For a `.py` file, a broken table therefore changes the printed road with nothing said (FR-59: name what could not be established).
- Fix: a public reader in `assertion_detectors` (the one reader, AR-13) plus a note in the caller. That file is outside the node's owns, so the Lead widens owns.
  F7 may move the reader anyway.

**F5 (fix before merge; error direction) — `"observed": "<what the test saw>"` in the JSON row is a valid string.**
- If the author pastes the marker form verbatim, `observed=<what the test saw>` is a Python SyntaxError, so it fails loudly.
- If the author pastes the JSON row verbatim, manifest_put accepts it, and the ledger shows the person "observed: <what the test saw>"
  (`ledger.unconfirmed_detail`, ledger.py:141-152). The contract's absent form is "observed: not recorded", never a guess.
- Fix: leave `observed` out of the row and say "add `\"observed\": <value>` when the test saw one".

**F6 (fix before merge; Q5(c)) — the non-Python road has no row through the gate.**
- The new table calls `P._open_oracle_door` directly, so `_binding_file` (the join from the manifest to the test file) is never driven for a non-`.py` entry.
- K-DOORA (test_s5_precheck.py:2014-2017) drives `.py` through `P.run`. A `_binding_file` that ignores the instance and returns any `.py`-looking file would pass every row.
- Fix: one row through `P.run` with a `.cs` `tests[]` entry (the same story builder, `oa_story`). It should assert the fragment road, plus F1's chosen removal.

**F7 (non-blocking; a judgment on the Lead's E1 decision, for the Lead) — `oracle_binding_forms` is a second suffix→kind map.**
- It passes Q12(a): a data row with a default, no language name in code.
- But the card itself says "a capability key of the test file's language row". Axis 34's intended road is a capability key on the
  `assertion_probes` / `assertion_probes_ast` row, with `marker_read` as the precedent (assertion_detectors.py:83, :119, :496).
- The new key carries its own `suffixes`, which `_claims_once` (assertion_detectors.py:222-245) never sees. A language then needs two rows in two tables, and they can drift.
- Proposal: an optional field (e.g. `binding_form`) on the language entries, read by a public reader beside `marker_read`. This also removes F4. Otherwise the Lead states why a separate table is kept.

**F8 (non-blocking, Q6) — `_binding_file` matches by exact `test_instance_id`.**
The file's own convention is `C.instance_id_aliases` (s5_precheck.py:924, 1012, 1231, 1434, 1581; contract :45-47). A row bound under an older spelling gets
`''`, so a `.py` file falls onto the manifest_put road and loses today's text. That is the safe direction, but it is inconsistent: match by aliases in the same fix round.

## Builder notes, answered

- Private `_document`: F4 (and F7).
- Multi-instance Then takes the first asserting row's file: acceptable as an edge. A Then asserted in a `.py` and a `.cs` instance gets the first one's form.
  With F1 fixed, the door must name the removal for EVERY asserting instance anyway (`asserting[number]` is a list). So the file pick matters less than the removal list.
- `qa_unresolved` at s5_precheck.py:1189 (partial-green door, handed_to_person) and :1607 (malformed remainder row): YES, the same P31 class.
  The binding road is named by the pytest marker whatever the test file's kind. My grep of the file adds :4562 ("tag the test with the planned shape in its `qa(...)` marker").
  They sit outside this node's owns but in this pile's file, so per critic rule 22 Q4 the Lead widens the fix round or sends a sibling builder.
  The current table row cannot serve them: it holds one form with `reason="expectation_unconfirmed"` fixed. Their forms need `owner=`, `part=`, `detail=` or `shape`.
  The key's shape (a form per reason, or per action) should be decided ONCE before they reuse it, or a second key duplicates it.
  Line for «Остатки» if the Lead does not widen: `s5_precheck :1189/:1607/:4562 print the pytest marker for every test-file kind | узел: <Lead opens, rules-debt>`.

## Standing questions (critic.md rule 22)

- Q1 fit to the spec: the road by data row — yes; no language name in the branch — yes (the code reads `Path.suffix.lower()` and the row); E2's road for a file with no row is printed —
  yes, but it does not lead to a correct manifest (F1); the rest of the door is not by capability (F2).
- Q2 builder's own decisions: the then_bindings row instead of `unresolved[]` — the right row by contract :56-57 (an `unresolved[]` row would be a whole-case row);
  the incomplete part is F1. The silent `''` — F4. The placeholder `observed` — F5.
- Q3 seams: additive. `check_open_oracle_asserted` gains one argument; `detectors.json` gains one key plus a note.
- Q4 class completeness: F2 (same function), the siblings :1189/:1607/:4562 (above). SIBLING_MAP axis 34 is the class axis. Axis 5's assertion-probe row is touched through F7.
- Q5 tests: (a) the `.py` and no-row choice are killed by the table and K-DOORA; the non-Python join is not (F6). (b) The expected marker text is today's text (the Lead's E1). The
  row fields trace to contract :56-57. (c) F6. (d) None rewritten. (e) None duplicated through the same door. (f) Test lines 39 < product 56: no `tests-over:` owed. (g) No new file.
- Q6 DUPLICATION AND CONSISTENCY: F3 (`_road` not reused), F4 (private reader, no note vs `_baseline_tokens`), F7 (second suffix map), F8 (aliases).
  Grepped: `_document(`, `FRAGMENT_ROAD`/`_road`, `instance_id_aliases`, `marker_read`, `oracle_binding_forms` over the package.
- Q7 CODE QUALITY: none blocking. The new functions are each under 30 lines with nesting at most 3. `for row in rows[:1]` in `_binding_file` reads as a loop over one row (an `if rows:` says it); nit, no severity.
- Q8 hygiene: 91 added lines, 0 CRLF, 0 non-ASCII; the files were LF before (python check below).
- Q9 ratchets: none touched (4 files in the stat, none a ratchet).
- Q10 ARCHITECTURE: named AR-1, AR-9, AR-15. Also touched: AR-13 (the one reader of detectors.json, reached through a private function; it is in the docstring
  but not in the commit's `architecture:` line) and AR-28 (F1: the door leads to a gate silence). Name both in the fix commit.
- Q11 JUDGMENT: `judgment: none` holds. A repair text is chosen by a data row; no census row, no role output judged.
- Q12 ONE ROAD: (a) the Lead's table is a data row with a default — passes. (b) No language-named branch (read: the diff's code lines; `language_sites` baseline not consulted, the search is mine).
  (c) No exclusion kept. (d) Residuals: F2 (fix this round) and :1189/:1607/:4562 (the Lead widens or opens a node); not a line for someone to pass on.

## Spot-checks

- The builder's 40 PASS for the FL9 table: re-ran the new function alone — 40 checks, all `True` (matches).
- Census t-2046 M1 says `check_open_oracle_asserted` does not run for non-Python stories. That is stale: it runs for every case with text (s5_precheck.py:4737-4739, after the `.py` skip
  only feeds `files`), so the new road is reachable.
- Not re-run (cost): test_arch_check 42/42, test_field_producers 885/885, test_validators 579/579. Consistent with the diff: no field-producer or validator change beyond the new key.

## Trail

- `git -C <wt> show 6d05f3fd` (full diff, 4 files, +91/-5).
- Read: spec :1490-1515; `s5_precheck.py` 660-668, 1178-1194, 1600-1650, 1661-1790, 2627-2665, 4700-4745; `manifest_put.py` 1105-1160, 1453-1474, 1539-1605;
  `manifest_from_tests.py` 20-50, 340-400, 955-972, 1180-1262, 1528-1550, 1565-1610; `ledger.py` 128-153, 845-870; `contract.py` 294-316;
  `assertion_detectors.py` 180-345; `references/artifact-contract-automation.md` 45-65; `SIBLING_MAP.md` axis 34; census t-2046 M1/M6 rows; `.claude/agents/critic.md` 178-292.
- Probe 1, scratch `probe_fl9.py`: printed the door for `tests/XTests.cs` (verbatim above). `AFTER MERGE` has two rows for Then 2; `declared: [2]`;
  `asserting: {2: ['XTests.Foo']}`; `binding file: 'tests/XTests.cs'`; `task in door road: False True`.
- Probe 2, scratch `probe_fl9b.py`: `(a) two-Then unit, retract: [(1, 'XTests.Foo', 'covered'), (2, None, 'unresolved')] removed 1` and
  `(a) one-Then unit, retract: [(2, 'XTests.Foo', 'covered'), (2, None, 'unresolved')] removed 0`.
- Control: imported `test_s5_precheck` and called `open_oracle_door_is_chosen_by_the_binding_file()` alone; harness RESULTS held 40 entries, all True, ending `PASS door B is unchanged`.
- Hygiene: python over `git show` gave `added 91 crlf 0 nonascii 0`; old s5_precheck.py / detectors.json had 0 CRLF lines.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 s5_precheck.py:1716-1720 - the manifest_put road leaves the covered then_bindings row of the Then (hand merge by unit (case, instance_id), manifest_put.py:1453-1585), so the gate goes silent while the proof row stays; the Lead picks the removal road (re-send the unit with retract, which fails for a one-row unit; a twin row on the instance, which changes contract :56-57; or a new manifest_put door), and the door names the removal for every asserting instance",
    "F2 s5_precheck.py:1721-1723 - the rest of door A prints qa(then=[n]), the # oracle_unknown comment and re-run manifest_from_tests.py on the manifest_put road; make it follow the same capability (FR-10, P31)",
    "F3 s5_precheck.py:1720 - use _road(task_name) (s5_precheck.py:664-666) instead of raw FRAGMENT_ROAD with <T>",
    "F4 s5_precheck.py:1677-1690 - no private assertion_detectors._document; a public reader in assertion_detectors and a note on an unreadable key, like _baseline_tokens (s5_precheck.py:2646-2658); needs the Lead to widen owns",
    "F5 s5_precheck.py:1716-1718 - leave out the literal observed placeholder in the JSON row (a verbatim paste passes and the ledger shows it to a person); say how to add observed",
    "F6 test_s5_precheck.py - one row through P.run with a .cs tests[] entry, so _binding_file and the F1 removal are driven through the gate",
    "F8 s5_precheck.py:1694-1700 - match the binding row's instance through C.instance_id_aliases, as the rest of the file does",
    "Siblings s5_precheck.py:1189, :1607, :4562 print the pytest marker for every test-file kind (same P31 class): the Lead widens this fix round or opens a rules-debt node; decide the shape of the oracle_binding_forms key per reason or action before they reuse it",
    "F7 (Lead decision, non-blocking) - oracle_binding_forms is a second suffix map beside assertion_probes and assertion_probes_ast; consider an optional capability field on the language rows read beside marker_read, or state why a separate table stays"
  ],
  "class_completeness": "Axis 34 (one road): no language name in the branch (verified); same-function residue F2 is not fixed; the same-class siblings s5_precheck :1189, :1607 and :4562 are outside owns and not queued, so the Lead widens or opens a node. Axis 5's assertion-probe row is touched via F7 (a second suffix map outside _claims_once).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md:1490-1515",
      "git show 6d05f3fd (worktree agent-ad30c6b4429bfe57a)",
      "ai-packages/qa-factory/scripts/s5_precheck.py:660-668,1178-1194,1600-1650,1661-1790,2627-2665,4700-4745",
      "ai-packages/qa-factory/scripts/manifest_put.py:1105-1160,1453-1474,1539-1605",
      "ai-packages/qa-factory/scripts/manifest_from_tests.py:20-50,340-400,955-972,1180-1262,1528-1550,1565-1610",
      "ai-packages/qa-factory/scripts/ledger.py:128-153,845-870",
      "ai-packages/qa-factory/scripts/contract.py:294-316",
      "ai-packages/qa-factory/scripts/assertion_detectors.py:180-345",
      "ai-packages/qa-factory/references/artifact-contract-automation.md:45-65",
      "docs/SIBLING_MAP.md axis 34",
      "docs/tasks/specs/reports/t-2046-language-exceptions-census.md M1/M6",
      ".claude/agents/critic.md:178-292"
    ],
    "reruns": [
      {"command": "python -B -c 'import test_s5_precheck as T; T.open_oracle_door_is_chosen_by_the_binding_file()' (worktree scripts on sys.path)", "result": "40 checks, all True; last line PASS door B is unchanged (matches the builder's 40 PASS)"},
      {"command": "python -B scratchpad/probe_fl9.py (door for tests/XTests.cs, then manifest_put._merge_then_bindings of its fragment)", "result": "AFTER MERGE holds the covered row on XTests.Foo and the unresolved null row for Then 2; declared [2]; asserting {2: [XTests.Foo]}; road prints --task <T>"},
      {"command": "python -B scratchpad/probe_fl9b.py (unit re-send with retract)", "result": "two-Then unit: covered Then 2 removed 1; one-Then unit: removed 0, the covered row stays"},
      {"command": "python over git show 6d05f3fd (CRLF / non-ASCII in added lines)", "result": "added 91 crlf 0 nonascii 0"}
    ]
  }
}
```
