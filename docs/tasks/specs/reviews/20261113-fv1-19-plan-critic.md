Critic on plan, FV1-19 (t-490), 13.11.2026 - extracted from the worker's hand-back

NOTE: the handoff gate refused writing `C:\QAFactory\forge-repo\docs\tasks\specs\reports\20261113-fv1-19-plan-critic.md`. It only accepts a path inside `docs/tasks/specs/reviews`. So the FULL verdict is below, per critic rule 16; the coordinator can extract it with `tools/handback_extract.py`.

# Critic on the PLAN — FV1-19 obligation_refs spec (task t-490)

**VERDICT: ACCEPT WITH FIXES** (`fit_with_fixes`). Blocking findings: 0. Fix-before-dispatch: 7 (D1–D7). Minor: 4 (m1–m4).

The design holds: one stamp in `contract.py`, called from `manifest_put.run` before the row-hash check; the carrier flipped to `automator`; the finish judged through one predicate. The facts check out (K1: 14 of 14 hold; the §2 negative reproduces). Nothing needs a redesign.

D1–D4 break the spec's own DoD lines ("one door named the same for every language", "one predicate", "nothing becomes a trap"), so N2 and N3 must not be dispatched before they are fixed. Whether to accept the plan is the Lead's decision.

Reviewed: the spec (whole, incl. §8a). Code read only from read-main; `S\` = `ai-packages/qa-factory/scripts/`. No tests run.

## Defects

### Fix before dispatch

**D1. Missed render sites for the ids door; some still tell every language to use the marker (req 2, FR-2, FR-11, axis 28).**
M3 and N2 cover two render sites (`s5_precheck._row_fields_text`, `manifest_from_tests._legend_line`). Axis 28 (`SIBLING_MAP.md:454`) lists more. A case-insensitive Grep of `qa\(obligations|written by the marker` over the package (tests excluded) finds sites that no node owns:
- **`agents/qa-automator.md:69`** — the role charter says "`obligation_refs`: `qa(obligations=)`". After N2 it still sends a TS/Java/C# automator down a road its language lacks. That is the very defect FV1-19 exists to close.
- **`window_record.py:138-141`** — `ORIGIN["obligation_refs"]` and `ORIGIN["obligation_ids"]` say "the automator writes the plan's obligation ids **and hashes** there". This contradicts F2 (a typed wrong hash is refused). The file is in N2, but these entries are not in N2's function owns.
- **`brief_pack.py:2009-2010`** — the marker `else` branch of `_row_field_lines`. It goes dead after M3. T3b ports it into `window_record.row_field_lines`. The AR-22 grep in §4.1 misses it, because the branch is written `== "automator"` + `else`.
- **`skills/qa-story/phases/s5.md:292-299`** — describes the manifest as coming from Python markers. Lower severity.

Fix:
- Add `agents/qa-automator.md:69` and the two `ORIGIN` entries to N2's owns, with a test row each. The charter edit needs a `live-runs` row (FR-33) and the role-load ratchet named.
- Queue line to T3b: "`row_field_lines`: no marker branch (FV1-19)".
- Add a Crossings row: T3b × `test_window_record.py`, FV1-19 first.
- Name `s5.md` as queued.

**D2. The finish's empty-map behaviour flips to a silent pass (AR-28; contradicts E3 and §9.2 "byte-for-byte").**
- Today (`controller.py:7291-7293`, `:7315-7317`): with `approved_obligations == {}`, `.get(id) != hash` is true for every ref, so the finish refuses with StateConflict "do not match".
- M1 defines `unknown` only for a NON-empty map, and `stale` needs the id to be in the map. So through M5 an empty map gives no problem, and every ref passes.
- It is rare in practice, because v2 plans are validated to carry obligations (`coverage_contract.py:333-343`). It is still a semantic change to a core gate.

Fix: add a `strict` flag to `obligation_ref_problems`. The finish passes `strict=True`, and an empty or missing map then makes every ref `unknown`. Add an N3 row: empty map → the same text as `:7317` today.

**D3. One predicate, two verdicts: the precheck never judges refs that ARE present on a row it does not demand them from (req 3, П1-б C10).**
- `window_record.py:233-236` returns `''` before reading refs whenever `owed` is empty: a case owing only `manual-*` obligations, a handed case, or a row outside the scope. M4 keeps this gate in front of `unknown`/`stale`.
- The finish judges every v2 instance (`:7298`, `:7315`).
- Example: the case owes `[{"obligation_id":"OB-M","decision":"manual-run"}]`; the row carries `[{"obligation_id":"OB-M","obligation_hash":"<pre-replan>"}]`. The precheck says nothing; the finish refuses with "do not match the current approved plan".
- So E19's invariant is false for these rows, and N3 (c) tests only owed rows. This is not F3: F3 is about *demanding* refs, this is about judging refs that are *present*.

Fix: the demand rule governs only `missing`. Refs that are present are always judged for shape, unknown and stale. Add N2 rows: a non-owed row with a stale ref → `stale`.

**D4. Code writers that forward stored hashes would be refused by the new stamp (FR-5/FR-57 on old data; a sibling of the class).**
`migrate_artifacts.py` writes through `manifest_put` (`:91-110`):
- `_legacy_obligation_patches` `:347-348` uses `dict(r, obligation_id=new)` and keeps the OLD per-ref hash.
- `_rename_legacy_obligations` `:395` keeps the old binding hash, and F5 stamps bindings too.
- Ghost retraction (`:211-226`, and its twin `:302-310`) resends whole stored rows with their stored refs and hashes; after a re-plan those hashes are stale.

F2 then refuses each call with "leave `obligation_hash` out", a door this code cannot use. The migration lands in `left`, and the TP2-2553 repair stops working.

Fix: one rule — a code writer that forwards stored refs or bindings drops `obligation_hash` and lets the stamp write it. Put those four sites in N1's owns with a keep-test row, or queue them with a pointer. E7 should also name the refusal a role gets when it copies a whole stored row back; that one has a door.

**D5. N3 (c) cannot go green while N2 runs in parallel.**
N3 (c) expects a stale hash to be refused by both the precheck (via N2) and the finish. Before N2 merges, the precheck reads no hash at all (`window_record.py:237-244`). The files are disjoint, but this row is not.

Fix: move N3 (c) to whichever of N2/N3 merges later, or test it against `C.obligation_ref_problems` on the finish side only.

**D6. Owns given by pointer, and crossings missing.**
- N2 owns "the П1-а walker row file, path at merge time". CLAUDE.md R11-m requires owns inline. N2's DoD (C3 green in the same commit) also depends on П1-а's walker work under F6 (a), which N2 does not own. Fix: give the path inline, or make N2 depend on that П1-а node, or move the `known_red` removal to П1-а.
- N4 (held, so this is feasibility only) owns `driver_dispatch.handoff_ladder` and `exit_limit`. Both are also owned by P1-v N0 and P1-v N2 (`20261113-p1v-run-scoreboard-spec.md:444,446`). The Crossings table has no P1-v row. Add `очередь:` lines before N4 is dispatched.

**D7. E14's `null` is decided against how the merge actually works.**
- E14 and N1 (e) say "`null` = untouched".
- But `manifest_put._merge_entry` (`:1385-1386`, `result.update(patch)`) stores `obligation_refs: None` over the stored refs. `manifest_from_tests.py:1699-1700` documents exactly this wipe.
- After M3, the row form prints a null slot for `obligation_refs` (N2 (b)). A role that sends the form with that slot still null wipes its refs.

Fix: decide one way and write the row: either the stamp drops an `obligation_refs: null` key, or `null` clears the refs and E14 says so.

### Minor

**m1. Two map conventions are presented as one.**
- M1 says "first occurrence wins". The finish's dict comprehension (`:7291-7293`) means last wins. The marker hashes its own row's object (`manifest_from_tests.py:753-759`).
- Plan ids are unique only across schema-2 rows (`coverage_contract.py:321-344`). So the readers diverge only on an invalid plan or a schema-1 row that carries obligations — but on that input §9.2's "byte-for-byte" is false.
- Req 4 cites the schema-2 filter (`contract.py:5210-5216`), while M1 reads all rows.

Fix: use last-wins (or name the edge), and align req 4 with M1.

**m2. The two id roads judge membership differently (P31, inside F1).**
- The marker refuses an id that is not in the case's own row (`:755-758`). The fragment stamp refuses only ids absent from the whole plan.
- This should go back to the Lead as a fork: under P17, should a test be allowed to prove another row's obligation?
- F1 (a) also promises an `obligation_marker` data row that no node creates. Add it to a node, or strike it.

**m3. Smaller silences.**
- (a) E16 says "no truncation" and N1 (g) says "a 3-line refusal". In fact `_problems_text` (`manifest_put.py:1119-1123`) writes one joined line up to a ceiling and spills the rest to `state/findings/manifest-put-<name>.txt`. Name the ceiling and add AT/BEYOND rows.
- (b) The stamp silently overwrites a role-sent `obligation_ids` that differs from the refs, while F2 refuses a differing hash. Pick one direction for both.
- (c) A row-level `obligation_hash` stored on the row survives an ids-only repair, and `probe_by_code.py:2854` prefers the stored value. The stamp should recompute or drop it.
- (d) When the plan is unreadable at the writer, the stamp says nothing (E3). AR-23/FR-41 call for a note line.
- (e) Non-string truthy id/hash values: today the finish refuses at `:7317` with StateConflict; under the new predicate it refuses at `:7302` with ValueError. Name this in N3 (a).
- (f) "An item that is not a dict → shape" makes the precheck stricter than `build`, which drops such items (`:1299`). `[{"obligation_id":"o1"},"junk"]` becomes a precheck finding while the finish passes. That is the safe direction, but name it.

**m4. Existing rows that N2 must flip are not named.**
- `test_manifest_from_tests.py:1848-1852` asserts that the legend names `qa(obligations=` and that `obligation_refs` gets no slot. List these as rows to rewrite.
- `controller.py` imports `contract` only lazily (33 in-function imports, none at top level). N3 needs a lazy import inside `_s5_v2_collect`; §9.1's wording should say so.

## Cross-spec gap (for the Lead)
After FV1-30a, `row-fields-missing` becomes word-passable (`p1-specs-amendment:330-332`). A person's word then passes the precheck on an `obligation_refs` gap, but the finish (`controller.py:7298-7317`) refuses the same refs and reads no word. FV1-30a's lower-readers table (`:398-404`) has no row for this. One of the two specs should name it.

## Per-key verdicts

**K1 — facts by trail: holds (14 checked).**
- `manifest_put.py`: `:2407` `unknown_obligation_refusal`, `:2408` `_passed_by_word`, `:2416` the return, `:2426` the EP1-38 comment, `:2427` the `obligation_hash_problems` call. `:592-622` checks the row hash only. `:2466-2468` is `stamp_provisional`.
- `manifest_from_tests.py`: `:1462-1465` builds the ids plus per-ref `content_hash(ob)`. Also confirmed: `:1385`, `:1628`, `:1324`, `:1674-1685`, `:1720`, `:1779`, `:1700-1701`.
- `window_record.py`: `:173-189` has `obligation_refs` as `"marker", MARKER_DOOR, True`; `:175` is `MARKER_DOOR`; `:192-196` `window_text_fields` filters on `window and automator`. Also confirmed: `:226-244`, `:270-292`, `:1299-1312`, `:1346-1350`.
- `controller.py:7289-7323`: five texts, order shape → fingerprint → plan → ids → row hash, `continue` per instance.
- `contract.py`: `_plan_rows_of` `:5178`, schema-2 filter `:5192-5203`, `:5210-5216`, `legacy_obligation_map` `:5219` — all exist. `event_store.py:106-108` confirmed. `s5_precheck.py`: `:82`, `:3768-3795`, `:3798-3840` confirmed.
- §2 negative reproduced: 6 hits, all `annotations.push`. There are 12 TS/Java/C# files in the package; the Java/C# ones are only synthetic `probe-languages` fixtures, so the "real data" premise rests on two TS files.

**K2 — feasibility: holds, given D2 and D7.**
- The stamp fits between `:2425` and `:2426`. `fragment` is rebound there, so the row-hash check, `validate`/`_refuse_unmergeable` (`:2485`) and `fragment_key` (`:2477`) all see stamped refs.
- `unknown_obligation_refusal` reads only bindings (`:1031-1033`). So a word-passed `obligation-id` never covers refs, and E17 holds.
- Under F5, unknown binding ids are skipped by the stamp, so the word road at `:2408` survives. The spec should say this explicitly.
- No import cycle: `event_store` imports no package module (`:6-16`). `manifest_put` never imports `window_record` (one docstring hit, `:595`).
- `window=False` is safe: `window_text_fields` is the only reader of `.window`, `test_window_record.py:1773` still sees four fields, and `build` copies refs as a list (`:1310`).
- One reader of the carrier that M3 changes is not named: `brief_pack._row_field_lines` (D1).

**K3 — edges decided right:**
- E3: defect (D2).
- E7: holds, except on the code-writer road (D4).
- E10: holds (same direction as `:619-621`).
- E11: holds.
- E12: holds as named; a door exists (refs naming the manual obligation).
- E14: defect (D7).
- E17: holds.
- E18: holds, apart from m3 (e).
- E19: defect (D3). Where the row is owed and `known` is given, all six adversarial inputs are refused: another obligation's hash, a trailing space and uppercase hex → stale (`hexdigest` is lowercase); an id with different case → unknown; an id twice → shape; `obligation_hash: null` → shape.
- E20: holds for roles, broken for code writers (D4).

**K4 — temporal: defect (D4), otherwise holds.**
Rows written before the change (missing or stale hash) get a precheck finding with an ids-only door. The stamp sits only in `run`, so `merge`, `fold` and `--recover` replays stay pure. That is enough for replay purity, but not for code writers that replay stored rows through `run`. See also m3 (c) and the FV1-30a gap.

**K5 — architecture: holds, given D1/D2/D3/D4/m1/m2.**
- AR-13/AR-15: given m1 and D3.
- AR-14: given D4.
- AR-22: given D1.
- AR-23: m3 (d).
- AR-28: D2.
- AR-29: every check is shape or join against the plan; no judgment is dressed as data.
- FR-2/FR-11: broken by the charter line until D1 is fixed.
- FR-5: D4.
- FR-38: holds — the brief line prints only `what` for automator fields (`brief_pack.py:2008`), and M3's `what` carries the ids-only shape.
- P31 / F1 (a): **not a block under critic rule 19.** Every language reaches the shared stamp and one named door, and the role step is the same. The Python marker is an extra authoring form that ends in the same stamp. The residual leaves as the proposed F1 (c) node (owner: Lead of `live-run-fvf`). Gaps inside it: m2.

**K6 — nodes: defect (D5, D6, m4); file, function, behaviour and test are named per item.**
- Keep files are confirmed under `"keep"` in `test-layers.json` (`:2912`, `:2841`, `:4770`, `:6865`, `:1078`, `:6927`). The quarantined files (`:9489`, `:7572`, `:8092`) are not edited.
- N1's `build` and N2's `_legend_line`/`_row_form` are disjoint functions in one file; merge order N1 → N2.
- N3's `_s5_v2_collect` is disjoint from FV1-30a's and FV1-30b's functions.
- T5 is queued after FV1-19, consistent with `told-before-work:374,396,621`.
- T3b overlaps with N2 (D1).
- The order N1 → (N2 ∥ N3) is sound on files, but not for row N3 (c) (D5).

**K7 — class completeness: queue candidates, not widening this spec.**
- `assertion_id`: code computes it for Python (`manifest_put.py:2443-2444` tells the role to copy it); for TS, `trace_binding.assertion_refs` is `[]` (`manifest_from_tests.py:1377`).
- Row-level `obligation_ids` and `obligation_hash`.
- `obligation_bindings[].instance_ids` (that is F1 (c)).
- `novelty` is never measured for non-Python rows (`:1386`) and is refused from a role (`:2386-2394`), which is an axis-34 road difference.
- Not in this class (role judgment): `defect_location`, `change_disposition`, `change_basis_ref`, `profile_id`.

**K8 — silences:** D7, D3, m3 (a)–(f), m1, and the FV1-30a word-pass gap.

## Rule 18 and rule 19
- **Duplication and consistency:** the spec removes the finish's inline check. Divergences left unnamed: the precheck's demand gate (D3), first-wins vs last-wins (m1), marker row-scope vs fragment plan-scope (m2). Searched: `obligation_refs|obligation_hash`, `qa\(obligations|written by the marker` (case-insensitive), `REQUIRED_ROW_FIELDS|filled_by|window_text_fields`.
- **Code quality:** there is no code yet. The plan-level risks are D2 (one predicate shared by an advisor and a gate, with no strictness parameter) and D7 (the stamp and the merge disagree on `null`).
- **One action, one road:** not a block, for the reasons under K5. Fix this round: D1 and m2. The residual is the F1 (c) node; the Lead opens it.

## Trail
- **Read (read-main):** `manifest_put.py:585-624, 1015-1059, 1119-1144, 1383-1407, 2340-2489`; `contract.py:5170-5249`; `event_store.py:100-111`; `controller.py:514-527, 2245-2264, 7230-7330`; `manifest_from_tests.py:700-769, 1338-1389, 1440-1479, 1660-1799`; `window_record.py:127-141, 160-294, 1290-1354, 1845-1864`; `s5_precheck.py:3764-3843`; `brief_pack.py:212-235, 1995-2024`; `coverage_contract.py:270-285, 312-349, 570-589`; `migrate_artifacts.py:196-230, 315-414`; `planning_contract.py:2580-2601`; `story_step.py:2815-2832`; `probe_by_code.py:7545-7564`; `agents/qa-automator.md:60-74`; `s5.md:292-301`; `test_manifest_from_tests.py:1825-1854`; `test_manifest_put_merge.py:712-750`; `test-layers.json` keep/quarantine rows; `SIBLING_MAP.md:432-454, 582-593`.
- **Read (neighbour specs):** told-before-work `:390-397` plus Grep; p1-specs-amendment `:296-405`; p1a (Grep FV1-19); p1v `:444, 446`.
- **Re-runs:** (1) Grep -i `obligation|annotation|@OB|OB-`, glob `*.{ts,java,cs}`, over the fixtures → 6 hits, all `annotations.push`, matching §2; the control is in the same call. (2) Glob of TS/Java/C# over the package → 12 files. (3) Grep -i for marker texts outside tests → `brief_pack:226, 2010`, `agents/qa-automator.md:69`, `manifest_from_tests:15, 1679`, `s5_precheck:3789, 3791`, `window_record:175`.
- **Not checked:** the driver claims in §1.4 and N4's internals (F4 is held); the `judgment-census.json` vocabulary.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 23/28 and 34 walked. Missed render sites: agents/qa-automator.md:69, window_record.ORIGIN obligation_refs/obligation_ids, brief_pack._row_field_lines marker branch (T3b), s5.md:292-299 (queue). Class sibling: migrate_artifacts forwards stored hashes through manifest_put at 4 sites. Queue candidates: assertion_id (Python computable, TS assertion_refs empty), row obligation_ids/obligation_hash, binding instance_ids (F1 c), novelty for non-Python rows.",
  "fixes": [
    "D1: N2 owns gain agents/qa-automator.md:69 and window_record.ORIGIN entries with rows; queue line to T3b; crossing T3b x test_window_record.py; s5.md queued",
    "D2: strict flag on obligation_ref_problems; the finish passes strict=True so an empty map refuses as at :7317; N3 row",
    "D3: demand governs only missing; present refs always judged; N2 rows for a non-owed stale ref",
    "D4: migrate_artifacts forwarding sites drop obligation_hash (N1 owns or queued with pointer); E7 names the whole-row copy-back",
    "D5: move N3 (c) to the later of N2/N3 or test it against the predicate only",
    "D6: inline the П1-а owns path or move known_red removal; P1-v N0/N2 crossing with an очередь line for N4",
    "D7: decide null vs _merge_entry semantics and write the N1 (e) row accordingly",
    "m1-m4: map convention and req 4 aligned; obligation_marker data row added or struck; membership-scope fork returned; _problems_text ceiling rows; obligation_ids direction; stored row hash recomputed; unreadable-plan note; test_manifest_from_tests.py:1848-1852 named; lazy contract import in N3"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-19-obligation-refs-spec.md",
      "read-main S/manifest_put.py, contract.py, event_store.py, controller.py, manifest_from_tests.py, window_record.py, s5_precheck.py, brief_pack.py, coverage_contract.py, migrate_artifacts.py, planning_contract.py, story_step.py, probe_by_code.py (ranges in Trail)",
      "read-main agents/qa-automator.md:60-74, skills/qa-story/phases/s5.md:292-301",
      "read-main tests: test_manifest_from_tests.py:1825-1854, test_manifest_put_merge.py:712-750, test-layers.json",
      "read-main docs/SIBLING_MAP.md:432-454,582-593",
      "neighbour specs: told-before-work, p1-specs-amendment, p1a, p1v"
    ],
    "reruns": [
      {"command": "Grep -i 'obligation|annotation|@OB|OB-' glob '*.{ts,java,cs}' over fixtures", "result": "6 hits, all annotations.push; matches section 2"},
      {"command": "Glob '**/*.{ts,java,cs}' over the package", "result": "12 files; Java/C# synthetic only"},
      {"command": "Grep -i marker texts outside tests", "result": "brief_pack:226,2010; qa-automator.md:69; manifest_from_tests:15,1679; s5_precheck:3789,3791; window_record:175"}
    ]
  }
}
```
