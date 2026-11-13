# t-505 — critic re-review, FV1-19 N1 fix round (diff c498f19..5f47f7b, branch wip/fv119-n1)

Critic (Opus). Re-review per rule 12: only the fix diff and the t-515 verdict
(`docs/tasks/specs/reviews/20261113-fv119-n1-code-critic.md`). Worktree HEAD verified `5f47f7b`. This verdict is an input to the
Lead's acceptance, not an acceptance.

**Verdict line: ACCEPT — 0 blocking findings.** B1, F1, F2 land correctly and completely; no new defect found. Two QUEUE notes (QA, QB) for
N2 / the Lead; neither is a regression of this round.

## Per item

- **B1 — landed.** `contract.py:~5359-5366` `_binding_stamp_allowed` (stamp allowed only when: no stored binding / stored hash absent or `""`
  / stored hash == plan hash / incoming non-null `design_assessment`); `contract.py:~5416-5421` the binding branch pops the incoming hash
  first, then stamps only if allowed, so a disallowed patch reaches `merge` with NO hash key and `manifest_put.py:1941-1943`
  `dict(stored, **incoming)` keeps the stale hash → `coverage_contract.py:580` `current` stays False. `manifest_put.py:2435` passes
  `_current_rows(task_root, "obligation_bindings")`. Positional invariants kept: membership test still precedes the stamp (unknown id left
  alone, refused earlier by `unknown_obligation_refusal` `manifest_put.py:2407`); a sent wrong hash still a problem (`contract.py:5423`).
  Stored-read semantics match the merge: `stored_by_id` (`contract.py:~5389-5390`) is a dict comprehension, last row of an id wins —
  identical to `by_id` at `manifest_put.py:1941`. All three receipt writers named in t-515 go through `manifest_put.run`, the only stamp
  caller that sees stored bindings; the other stamp caller, `manifest_from_tests.build:1543`, emits no `obligation_bindings` (Grep -i
  `obligation_bindings|stamp_obligation_refs` over `scripts/*.py`: in `manifest_from_tests.py` only the stamp call, no bindings key; positive
  control: hits in `manifest_put.py`, `contract.py`), so no pre-stamped binding can bypass the stored-aware check. Row (f) re-seeded with a
  stale stored hash (`test_manifest_put_merge.py:~885-897`); run-level rows for receipt and sensitivity patches (`:~934-956`); the mutation
  witness in the report turns 4 rows red (329/333), consistent with the diff. Control re-run: 333/333.
- **F1 — landed.** `migrate_artifacts.py:~176-177` `_forwardable(row, refs=False)` drops `obligation_refs`, `obligation_ids`,
  `obligation_hash`; used at the two retraction sites only (`:236`, `:320`); rename sites (`_legacy_obligation_patches`,
  `_rename_legacy_obligations`) unchanged with `refs=True` (read `:340-430`). Rows (p) re-pinned for both sites and both ids
  (`test_obligation_join.py:~271-287`): retraction commits, refs/ids/row hash equal to stored (`"stale"`, `"stale-row"`), also for
  TS-9-O9 (a plan-unknown id) — the retraction no longer depends on the plan. Matches the t-515 proposal and the Lead's override of E29 /
  row (p) (report line 141).
- **F2 — landed.** (1) One shape helper `contract.py:~5267-5291` `_ref_shape_problems(refs, where, hash_required)` used by
  `obligation_ref_problems` and `_stamp_row_refs`; traced the old two loops against it: the only behavioural deltas are wording (unified,
  `; send <shape>` door added — FR-1/FR-2 better) and at most one problem per ref (old reader could emit "appears twice" plus "no hash" for
  one ref); irrelevant to the outcome since any shape problem returns alone. Empty-string id: old stamp added `""` to `seen`, new does not —
  unreachable difference, an empty id is already flagged. Pinned by the row "F2 one shape wording" (5 inputs, text equality reader vs stamp
  modulo prefix). (2) `_plan_rows_of(task_root, errors=None)` reports read failures; `plan_obligation_map` reads once — second resolver and
  double parse gone. (3) `manifest_from_tests.py:1543` reuses `Story._obligation_map` with a fallback; an empty cached map re-reads without
  `notes` (no duplicate note), harmless.

## Deviations (builder's own choices)

1. **Only a non-null `design_assessment` counts as a re-judgment — agree.** By the node's convention null = not sent (stamp step 1 for hashes),
   so a null cannot be read as a judgment act; treating it as one would revalidate the stale binding with `design_assessment: None` stored
   via the merge. Safe direction (FR-59/AR-28): the uncertain case stays not current. Production check: no code writer sends the key
   (Grep -i `design_assessment` over `scripts/*.py`: only `contract.py` (the predicate), `coverage_contract.py`, `ledger.py`,
   `metrics_projection.py`, a comment in `manifest_put.py` — all readers; positive control = those reader hits), and the only code forwarding
   whole stored bindings, `_rename_legacy_obligations`, targets a NEW id with no stored binding (`new in existing` → `left`), so the
   predicate is not satisfiable by a code writer over a stale stored binding.
2. **Incoming binding `"obligation_hash": ""` popped — agree.** Before the fix `""` was overwritten by the stamp anyway (`sent in (None, "")`);
   popping in both outcomes prevents `""` from erasing the stored hash through the merge when the stamp is disallowed, and is symmetric with
   the null drop. No legitimate "clear the hash" use exists (the hash is the code's alone, AR-14).
3. **Census row `_ref_shape_problems`, class `shape` — agree.** The helper judges list/item/type shape only; the plan join stays in
   `obligation_ref_problems` (row `xref`). Roles mirror the `obligation_ref_problems` row. Not a judgment class, no ratchet key moved; the
   census test itself demanded the row (u1), the dispatch allows it. Edit outside owns is justified and minimal.

## Queue notes (not blocking, not regressions of this round)

- **QA (neighbour on the B1 surface, owner Lead).** `obligation_hash` gates not only `design_assessment` but also `code_validity`, `sensitivity`
  and `witnessed` (`coverage_contract.py:581, 594-597`). After a re-plan, an automator re-sending only `design_assessment` refreshes the hash,
  so the stored `code_validity` / `sensitivity` / receipts judged on the OLD obligation text count again until their writers re-run. This was
  the same before N1 (the role wrote the hash) and is the direction t-515 itself proposed, so it is not this round's defect; whether a hash
  refresh should reset the other judgment fields is a spec decision — proposed node, the Lead opens it or declines.
- **QB (door, → N2).** A stale binding now stays stale until a `design_assessment` is re-sent; no script text names that door (Grep -i
  `design_assessment` over `scripts/*.py`: readers only, positive control as in Deviation 1; `references/` not searched). N2's
  precheck/wording must say it (same class as t-515 Q3). Also the `changelog.d/fv1-19a-obligation-refs-stamp.md` fragment carries no
  stale-binding or identity-only-retraction clause (builder noticed; verified: grep -i `stale|retract|identity` on the fragment: no hit,
  positive control `obligation` on the same file: 1 hit); outside owns.
- Observation, no finding: `_current_rows` reads the projection outside the commit lock, as the pre-existing `_current_tests` does; the only
  race outcome I can construct leaves a binding not current (safe direction), so no failure scenario.

## Standing questions

- **DUPLICATION AND CONSISTENCY:** the two shape copies and the second plan resolver are gone (F2); none new found: grepped
  `def _ref_shape_problems|def _plan_rows_of|plan_obligation_map|stamp_obligation_refs` in the diff and `scripts/*.py`.
- **CODE QUALITY:** new functions small (`_binding_stamp_allowed` 8 lines, `_ref_shape_problems` 25), nesting ≤ 3, docstrings truthful
  (the "null = not sent: the merge keeps the stored value" claim flagged in t-515 is now true on the binding axis). Minor: `getattr(story,
  "_obligation_map", None)` reads a private lazy cache; acceptable, one line.
- **ARCHITECTURE (q10):** AR-28 now kept on the binding axis (B1); AR-14/AR-15 kept (one stamp).
- **JUDGMENT (q11):** none moved; one `shape` census row.
- **ONE ROAD (q12):** one shape reading for reader and writer; no language/project branch added.

## Trail

Read: t-515 verdict whole; fix diff `c498f19..5f47f7b` (all 8 files); report section "Fix round after the code critic (t-515)" whole;
`manifest_put.py:1925-1950, 2286-2301, 2405-2470, 2490-2515`; `migrate_artifacts.py:340-430`; `coverage_contract.py:574-600`.
Searches (Grep -i over `scripts/*.py`, positive control in the same shape): `design_assessment`; `stamp_obligation_refs|obligation_bindings`;
`_obligation_map` in `manifest_from_tests.py`; `stale|retract|identity` on the changelog fragment.
Rerun: `test_manifest_put_merge.py` at 5f47f7b → `=== test_manifest_put_merge: 333/333 ok ===` (all B1 and F2 rows PASS). Other attached
witnesses checked for consistency only (48/48 join rows match the re-pinned (p) block; mutation 329/333 matches the 4 stale-binding rows).
Line numbers marked `~` are taken from diff hunks, not re-read. Not read: spec §6/§8 beyond what the verdict quotes (re-review scope).

```json
{
  "verdict": "fit",
  "blockers": [],
  "class_completeness": "B1 closed at the one stamp for every binding writer: manifest_put.run is the only stamp caller seeing stored bindings, manifest_from_tests emits no bindings, and no production code writer sends design_assessment (rename forwards to new ids only). F1 applied to both retraction sites, rename sites intentionally unchanged. F2: one shape helper for reader and stamp, one plan read. Residual neighbours queued: QA (hash refresh by design re-send revives code_validity/sensitivity, pre-existing, Lead decides), QB (door text for stale bindings and changelog clause, N2).",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/20261113-fv119-n1-code-critic.md",
      "git diff c498f19 5f47f7b (8 files)",
      ".claude/worktrees/fv119-n1/docs/tasks/specs/reports/20261113-fv119-n1-report.md fix-round section",
      "scripts/manifest_put.py:1925-1950,2286-2301,2405-2470,2490-2515",
      "scripts/migrate_artifacts.py:340-430",
      "scripts/coverage_contract.py:574-600"
    ],
    "reruns": [
      {
        "command": "( cd <worktree>/ai-packages/qa-factory && python -B scripts/tests/test_manifest_put_merge.py )",
        "result": "=== test_manifest_put_merge: 333/333 ok === at 5f47f7b, all B1/F2 rows PASS"
      }
    ]
  }
}
```
