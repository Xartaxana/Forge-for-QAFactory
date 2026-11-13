# t-515 — code critic, FV1-19 N1 (diff f4dfd07..c498f19, branch wip/fv119-n1)

Critic (Opus). Spec: `docs/tasks/specs/20261113-fv1-19-obligation-refs-spec.md` (§3, §4 M1/M2, §5 E1-E29, §6 N1 (a)-(r), §8c F7/F8/F9).
Worktree HEAD verified `c498f1996358edcb33541b8b0463ce16cebeb817`. This verdict is an input to the Lead's acceptance, not an
acceptance.

**Verdict line: ACCEPT WITH FIXES (NEEDS WORK) — 1 BLOCKER (B1), 2 FIX (F1, F2), 3 QUEUE (Q1-Q3).** B1 must land in N1's fix round
before N2/N3 start; F1/F2 should land in the same round.

## Findings

### B1 (BLOCKER) — the stamp re-validates a STALE stored binding when a code writer sends a hash-less binding patch (AR-28 false pass)

Surface: the binding branch of `stamp_obligation_refs`, `contract.py:5396-5411`, combined with the key-wise binding merge
`manifest_put.py:1941-1943` (`by_id[id] = dict(stored, **incoming)`).

The stamp writes `obligation_hash = content_hash(<current plan obligation>)` onto EVERY incoming binding that names a plan id and carries no
hash. The merge then overwrites the stored binding's hash with it. Three production code writers send hash-less binding PATCHES that are not a
re-judgment of the binding, only a receipt:
- `probe_by_code.publish_binding` → `_binding_items` `probe_by_code.py:7544-7549`, sent at `:7628`;
- `red_sandbox` probe `red_sandbox.py:1863-1866`, sent at `:1880-1886`;
- `window_record.publish_review_receipt` `window_record.py:1857-1858` (`{"obligation_id", "review_receipt_ref"}` only).

Before N1 a stored binding whose hash no longer matches the plan (re-plan, E15) stayed stale: `coverage_contract.py:580`
`current = binding["obligation_hash"] == content_hash(ob)` is False, and `:581`, `:594`, `:595`, `:597` then force design `unknown`, validity
`unverified`, sensitivity `missing`, witnessed False. After N1 any of the three receipt publishes refreshes the hash, `current` becomes True and
the binding's OLD `design_assessment` / `code_validity` / `sensitivity` — judged against the pre-re-plan obligation text — count again toward
`verified` (`:627-628`). A previously refused state becomes accepted by a code writer, with no role act. That is the window K1 asks about,
and it contradicts the commit's own `architecture:` claim ("an unknown or stale reference is named, never stored as valid").

Witness (pure probe at c498f19, `stamp_obligation_refs` + `manifest_put.merge`; script in the scratchpad, output verbatim):
```
stored binding current vs plan: False
problems: []
stamped binding: {'obligation_id': 'OB-1', 'review_receipt_ref': 'state/r.json', 'obligation_hash': 'ef9700dc...5655'}
after merge current: True design: sufficient
pre-N1 (unstamped) merge current: False
```
Neighbouring classes on this surface (rule 14):
- **the null-drop of a binding hash (D7, row (f))**: `{"obligation_id": "OB-1", "obligation_hash": null}` — after the null drop the stamp
  stamps the CURRENT plan hash, so "null = not sent, the stored value stays" holds only when the stored hash already equals the plan's. Row
  `(f) a binding obligation_hash: null keeps the stored binding hash` (`test_manifest_put_merge.py`, fv1_19_obligation_stamp) passes by
  coincidence (stored == current) and cannot catch this.
- **a fresh binding (no stored row)**: stamped → current, but no design field → design `unknown`, validity `unverified`: harmless.
- **tests[] rows**: not affected — the stamp touches only rows that SEND `obligation_refs` (`contract.py` step 2), and none of the three writers
  send refs (`red_sandbox.py:1876-1877` sends `sensitivity_proof` only). Checked.
- **the role's binding patch**: a role adding an instance id to a stale binding gets the same silent refresh; spec F5 meant a role-sent binding
  to be stamped, but not to resurrect judgment fields it did not resend.

Fix (direction for the Lead; the exact rule is a spec decision that belongs to the Lead tier): the stamp must not write a binding hash over a
STORED binding of that id whose hash differs from the plan unless the incoming binding re-sends the judgment the hash certifies (e.g. carries
`design_assessment`); simplest form: `manifest_put.run` passes the stored bindings to the stamp, and for an incoming hash-less binding the hash
is stamped only when no stored binding exists, or the stored one has no hash, or its hash already equals the plan's. Rows to add: a stale stored
binding + a hash-less `review_receipt_ref` patch → stored hash unchanged (still not current); row (f) re-seeded with a stale stored hash.

### F1 (FIX) — the two retraction sites: forwarding refs at all turns stale refs valid and makes a formerly committing retraction refuse

`migrate_artifacts.py:229` and `:313` resend the covering rows only to MATCH their identity (docstring `:189-197`: "a tests[] patch matched
by identity is never dropped"); `_merge_entry` (`manifest_put.py:1383-1386`) is a patch, so keys absent from the resend keep their stored
values. `_forwardable` (`:166-177`) instead resends `obligation_refs` without hashes, so the stamp (a) silently restamps a stale ref to the
current plan hash — the row (p) result "the covering row's refs carry the current plan hash" is a stale reference made valid without the role,
against §3 req 6 ("never a silent pass") and E7's invariant ("a reference measured on other bytes never counts"); and (b) refuses the whole
retraction when a covering row cites an id the plan no longer names (row (p) second half: "nothing committed, the row stays"), where before
N1 that retraction committed. Both are prescribed by the spec (E29, row (p)), so this is a spec defect that the builder followed correctly —
the decision is the Lead's. Proposal: at the two retraction sites send the covering rows WITHOUT `obligation_refs` / `obligation_ids` /
`obligation_hash` (identity only); stored refs then stay as they are (stale stays stale → the precheck door of N2), and the retraction no longer
depends on the plan. `_forwardable` stays for the two rename sites, where the ids change and must be resent. Rows (p) re-pinned accordingly.

### F2 (FIX) — duplication inside the diff (brief item 6/7)

- Two copies of the ref shape rules: `obligation_ref_problems` `contract.py:5278-5294` and `_stamp_row_refs` `contract.py:5324-5340` (non-list,
  non-dict item, non-string id, duplicate id, non-string hash) with diverging wording ("appears twice" vs "appears twice in one row"). The
  difference is one flag (the stamp accepts a missing hash). One private shape helper with `hash_required: bool` serves both; otherwise a
  later edit to one copy (new shape rule) silently diverges the writer from the reader — exactly the AR-13 class this node exists to close.
- `plan_obligation_map` `contract.py:5247-5263` re-implements the path resolution of `_plan_rows_of` (`contract.py:5179-5183`) and parses the
  plan twice (once to detect the error, once inside `_plan_rows_of`). A `_plan_rows_of(task_root, errors=None)` variant (or a shared
  `_plan_path`) removes the second resolver and the double read.
- `manifest_from_tests.build` (`manifest_from_tests.py:1543`) reads the plan map a third time although `Story.obligation` cached it on the
  story (`:749-750`); minor.

### Q1 (QUEUE, proposed node, owner Lead) — two membership readers inside one writer (P31 / brief item 12)

`manifest_put.run` now judges "is this id the plan's" twice: refs through `obligation_map` (ALL plan rows, `contract.py:5234-5244`) and bindings
through `unknown_obligation_refusal` → `C.unknown_obligation_ids` → `plan_obligations` (schema-2 rows only, `contract.py:5192-5216`). On a plan
with an obligation on a schema-1 row, a ref to it is accepted and stamped while a binding to it is refused (word road). Spec E23 / plan-critic K2
kept the binding reader deliberately, so this is not this diff's defect; it is a residual of class "one action, two roads" and needs a node
(converge the binding membership on `obligation_map`, keeping the word road) — the Lead opens it.

### Q2 (QUEUE → N2) — a doc carrier still tells the role the ref shape includes a hash

`references/artifact-contract-automation.md:157` ("Each instance carries `obligation_refs` (`[{obligation_id, obligation_hash}]`)") and `:161`
(binding `obligation_hash (sha256 of the approved obligation)`), and the same lines in its slices
`references/slices/qa-automator/artifact-contract-automation.md:141,145` and `references/slices/qa-code-critic/...:129,133`. After N1 a role
that follows it and computes a hash differently is refused. SIBLING_MAP axis 36 names this file (+ slices) as a doc carrier of manifest writer
contracts; the spec's §3 req 2 render-site list does not name it (Grep -i `artifact-contract|qa-automator\.md` over the spec: hits only the
charter line `:48,198,343,364,631` — positive control). Add to N2's owns (one clause: "the code writes each hash; send ids") or queue by name.

### Q3 (QUEUE, note) — predicate texts carry no door yet

`obligation_ref_problems` texts (`unknown` "(the plan names none)", `stale` "...hashes to <h>") name no door; that is acceptable only because
N2 (M4 wording) and N3 (the `:7302`/`:7317` texts) wrap them. N2/N3 critics must check the wrap; noted so it is not lost.

## Keys

**K1 — one writer, one reader.** In the diff's files: `manifest_from_tests.py` has no `obligation_hash` write left (Grep -i `obligation_hash`
over the five production files of §4.1: `manifest_from_tests.py` — none; positive control: same call finds 10 hits in `manifest_put.py`);
`manifest_put.py:592-623` `obligation_hash_problems` (row-level, kept by §4.1) is the only remaining own comparison, and it runs after the stamp
on stamped refs (`:2438-2439`); `migrate_artifacts.py` writes none (drops via `_forwardable`). Per-ref and binding hashes have one writer
(`stamp_obligation_refs`). `obligation_ref_problems` has NO production caller in this diff (Grep -i over `scripts/`: definition +
census row + tests only) → reader side unchanged until N2/N3, so no reader window. Writer window: (1) new refusals — a role-typed wrong hash
(before: stored, refused at the finish `controller.py:7315`; now refused earlier with a door — safe direction); a code writer forwarding stored
hashes — only `migrate_artifacts` does (all production `--fragment` / in-process `manifest_put.run` callers enumerated: migrate_artifacts,
window_record, story_step, red_sandbox, probe_by_code, planning_contract, manifest_from_tests; story_step/planning_contract send `unresolved`
only); (2) new ACCEPTANCE — **yes, B1** (stale binding refreshed by three receipt writers) and F1(a) (stale covering refs restamped by the
migration). Leaving `window_record.py`, `probe_by_code.py:2854`, `controller.py:7300-7323`, `coverage_contract.py`, `manual_evidence.py` for
N2/N3 creates no further window: they read; none writes per-ref/binding hashes into the manifest.

**K2 — error direction: ok.** Probe at c498f19 over 15 inputs × map {plan, None, {}} × strict {False, True} (output in trail): None / string
/ dict / bare-string item / dict without hash / null hash / int id / duplicate with two hashes → `shape` on every map and both modes; `[]` → `[]`
(demand is the caller's, E11); stale / uppercase hex / trailing space → `stale` with a map; id of another case spelling (`ob-1`) and a foreign id
→ `unknown` with a map; with map None or `{}`: strict → every ref `unknown`, non-strict → shape only (spec M1). A wrong/stale/foreign hash is
never a pass with a non-empty map; with an empty map the non-strict pass is the spec's declared side, covered by `strict=True` at the finish
(AR-28 holds once N3 lands; today the finish's own code still refuses). Callers: none yet in this diff; spec assigns precheck `strict=False`,
finish `strict=True`. F7 (b): membership is the whole plan — `obligation_map` reads all rows with no schema filter (`contract.py:5234-5244`);
the unknown text says "is not an obligation of the plan (the plan names …)" (`:5303-5304`), and the marker says the same (`manifest_from_tests.py:754-755`).

**K3 — stamp: ok except B1.** A caller hash that disagrees with the plan is a problem, never restamped (`contract.py:5349-5350`, binding
`:5409-5410`); `manifest_put.run` returns `EXIT_BAD_FRAGMENT` before the hash check, merge view and commit (`manifest_put.py:2433-2437`);
rows (b), (c), (k) assert journal and tree unchanged. Idempotent: equal hashes kept, sent row hash kept for `obligation_hash_problems`; row
`stamp: idempotent` pins it. Unreadable plan: one note, `{}`, refs stored as sent (row (q)); the finish still refuses (E26). Purity: deepcopy per
row, input untouched (row `stamp: pure`).

**K4 — `_forwardable`: finding F1.** Forwarded: every key except row `obligation_hash`, per-ref `obligation_hash`, and `obligation_ids` on a row
with refs; bindings lose `obligation_hash` (`migrate_artifacts.py:166-177`, used at `:229`, `:313`, `:365`, `:409`). Dropped and re-stamped
from the current plan → a stale row becomes valid at the two retraction sites (F1) and at the rename (spec row (o), where it is the rename's
nature). A person's retraction (`retracted_obligations`) is not touched by `_forwardable` (the rename still sends `retract`, `:418`); F9 rows
are in `test_obligation_join.py` section 4b as decided. No loss of a person's retraction found.

**K5 — re-pinned expectations: ok.** Changed existing expectations, all three files:
1. `test_manifest_from_tests.py` "an obligation not on the plan row is refused" / "TS-9-O1 is not an obligation of TC-001's plan row TS-1
   (it has: TS-1-O1)" → "an obligation the plan does not name is refused" / "...of the plan (it names: TS-1-O1, TS-2-O1, TS-3-O1, TS-4-O1)":
   forced by F7 (b) (row (r) second half); the refusal and exit 2 stay — not weakened. The location check `tests/test_coupon.py:9` stays.
2. `test_obligation_join.py` "and so do its obligation_refs, hash untouched" (`h1`) → plan hash: spec row (o), forced.
3. `test_obligation_join.py` seed binding OB-1 gains `"obligation_hash": "hb"` (fixture extension for (o)), not an expectation change.
`test_manifest_put_merge.py`: additions only. Removed with no test: the marker's refusal "the case's plan row … is not in work/test-plan.json"
(old `manifest_from_tests.py:748-751`) — implied by F7 (b) (no plan-row notion); no existing row pinned it (Grep -i "none recorded|can only be
checked against the row" over the package: no test hit).

**K6 — census row: ok.** `class: xref` is right (a join of ids/hashes against the plan; shape is subsumed, CLASS_ORDER xref > shape); it judges
data, not meaning (question 11: no judgment moved). Roles `conductor`, `qa-automator`: the unit has no caller yet; after N2 it stands on the
automator's precheck path, so the roles are anticipatory but correct. `xref` is not a ratchet class (ratchets count the judgment classes), so
"no ratchet key changed" is consistent. Control run: `=== judgment_census: 24/24 ok ===`.

**K7 — class completeness and quality.** Twins (AR-19/AR-22): every field the stamp writes has its reader (refs/ids/row hash → precheck,
finish, `probe_by_code.py:2854`; binding hash → `coverage_contract.py:281,580`); the producers that must change in this commit changed
(marker, fragment, code writer). Missed sibling producers on the binding axis: the three receipt writers of B1 (their behaviour changed without
a row; the builder's analog list omits them). Doc carrier (axis 36): Q2. Duplication/quality: F2. No function in the new code over ~60 lines
except `stamp_obligation_refs` (`contract.py:5365-5413`, ~49 lines incl. a 13-line docstring) — ok; nesting ≤ 3.

**K8 — refusal texts: ok.** Each stamp refusal names what (`tests[i].obligation_refs[j]: …`), the expected (`REF_SHAPE`, the plan's ids,
the plan's hash) and a usable door ("send [{"obligation_id": …}]", "leave `obligation_hash` out, the code writes it"), followed by
`REPAIR_MARKER`, through `_problems_text` (ceiling/spill reused). Marker refusal names the plan's ids and "leave `obligations` out". The door
is the fragment the automator already sends — usable in every language (FR-2).

## Standing questions
- **DUPLICATION AND CONSISTENCY:** F2 (two shape implementations; second plan-path resolver); Q1 (two membership readers). Grepped:
  `def _plan_rows_of|def plan_obligation|obligation_map|unknown_obligation_ids` in `contract.py`; shape strings in `contract.py:5270-5362`.
- **CODE QUALITY:** no oversize/over-nested new function; no dead branch; one lying claim — the docstring/commit "null = not sent: the merge keeps
  the stored value" for a binding hash (B1 neighbour).
- **ARCHITECTURE (q10):** commit names AR-13/14/15/23/28 (+ AR-29 on the census commit). AR-28 is not kept on the binding axis (B1).
- **JUDGMENT (q11):** none moved; census row read; no `blocks_override`, no scan-constant edit, no craft marker.
- **ONE ROAD (q12):** marker and fragment now share one membership rule and one stamp (row (h)); no language branch in the diff (Grep -i
  `typescript|\.spec\.ts|java|csharp` over the diff: none). Residual Q1 (bindings vs refs membership) — proposed node, owner Lead.
- **Ratchets (q9):** one census row added (`obligation_ref_problems`, xref) — not a ratchet key; no raise.

## Trail
Read: the diff of all 10 files; spec §3-§6, §8c; builder report (incl. witness, mutation, fix round); `manifest_put.py:1018-1053, 1383-1406,
1930-1945, 2423-2440`; `migrate_artifacts.py:85-177, 180-429`; `coverage_contract.py:265-289, 560-628`; `probe_by_code.py:7530-7629`;
`red_sandbox.py:1595-1634, 1845-1889`; `window_record.py:1842-1874`; `story_step.py:2824-2837`; `planning_contract.py:2585-2602`;
`contract.py:5178-5216`; `references/artifact-contract-automation.md:150-167`; SIBLING_MAP axis headers + axis 36; critic-diff-brief items 6-12;
census test header.
Searches (each with a positive control in the same call shape): Grep -i `obligation_hash` over `scripts/*.py`; Grep -i production callers of
`manifest_put` (`"--fragment"`, `manifest_put.run(`); Grep -i the new function names; Grep -i `artifact-contract|qa-automator\.md` in the spec.
Reruns: census test; the B1/K2 probe.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: stamp_obligation_refs (contract.py:5396-5411) writes the current plan hash onto every hash-less incoming binding; the key-wise binding merge (manifest_put.py:1941-1943) then overwrites a STALE stored binding hash, so receipt-only patches from probe_by_code.publish_binding (:7628), red_sandbox (:1880) and window_record.publish_review_receipt (:1857) flip coverage_contract.py:580 current to True and revive old design_assessment/code_validity/sensitivity - a previously refused state accepted without a role act (AR-28). Probe: after merge current True, design sufficient; pre-N1 current False."
  ],
  "fixes": [
    "B1: do not stamp a binding hash over a stored binding whose hash differs from the plan unless the incoming binding re-sends the judgment it certifies (Lead decides the exact rule; e.g. pass stored bindings to the stamp and stamp only when none is stored, it has no hash, or it already equals the plan); add rows: stale stored binding + hash-less review_receipt_ref patch keeps the stale hash; re-seed row (f) with a stale stored binding hash.",
    "F1: at migrate_artifacts retraction sites (:229, :313) resend covering rows identity-only (no obligation_refs/obligation_ids/obligation_hash) so stale refs stay stale and the retraction no longer depends on the plan; keep _forwardable for the rename sites; re-pin rows (p). Spec E29/row (p) decision belongs to the Lead.",
    "F2: one private shape helper for obligation_ref_problems and _stamp_row_refs (contract.py:5278-5294 vs 5324-5340); plan_obligation_map reuses _plan_rows_of path resolution instead of a second resolver and double parse; build reuses the Story's cached map.",
    "Q1 (queue, Lead opens node): converge binding membership (unknown_obligation_ids, schema-2 only) with obligation_map (all rows).",
    "Q2 (to N2 owns or queue): references/artifact-contract-automation.md:157,161 and its two slices still describe refs/bindings as carrying a role-written hash.",
    "Q3 (note for N2/N3 critics): predicate texts carry no door; the wrapping texts must."
  ],
  "class_completeness": "Writer axis: marker, fragment and migrate_artifacts converge on the one stamp; but the three receipt-binding code writers (probe_by_code.publish_binding, red_sandbox probe, window_record.publish_review_receipt) change behaviour through the stamp with no row and are omitted from the builder's analog list (B1). Doc carrier axis 36: artifact-contract-automation.md + slices not in the spec's render-site list (Q2). Membership axis (P31): refs vs bindings read two different plan maps (Q1). Reader side (precheck, finish) is N2/N3 and opens no window in this diff since obligation_ref_problems has no caller yet.",
  "trail": {
    "read": [
      "git diff f4dfd07 c498f19 -- ai-packages/qa-factory (10 files)",
      "docs/tasks/specs/20261113-fv1-19-obligation-refs-spec.md (sections 3-6, 8c)",
      ".claude/worktrees/fv119-n1/docs/tasks/specs/reports/20261113-fv119-n1-report.md",
      "docs/tasks/critic-diff-brief.md items 6-12",
      "scripts/manifest_put.py:1018-1053,1383-1406,1930-1945,2423-2440",
      "scripts/migrate_artifacts.py:85-429",
      "scripts/coverage_contract.py:265-289,560-628",
      "scripts/probe_by_code.py:7530-7629",
      "scripts/red_sandbox.py:1845-1889",
      "scripts/window_record.py:1842-1874",
      "scripts/story_step.py:2824-2837",
      "scripts/planning_contract.py:2585-2602",
      "scripts/contract.py:5178-5216",
      "references/artifact-contract-automation.md:150-167",
      "docs/SIBLING_MAP.md axis list and axis 36"
    ],
    "reruns": [
      {
        "command": "( cd <worktree>/ai-packages/qa-factory && python -B scripts/tests/test_judgment_census.py )",
        "result": "=== judgment_census: 24/24 ok === at c498f19"
      },
      {
        "command": "python -B <scratchpad>/probe1.py (stamp_obligation_refs + manifest_put.merge on a stale stored binding; obligation_ref_problems over 15 inputs x 3 maps x strict)",
        "result": "stored binding current False; stamp problems []; after merge current True design sufficient; pre-N1 merge current False. K2 matrix: shape/unknown/stale exactly per spec M1; empty map strict -> unknown, non-strict -> shape only"
      }
    ]
  }
}
```
