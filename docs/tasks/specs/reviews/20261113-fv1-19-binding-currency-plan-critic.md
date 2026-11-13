# Critic on plan — FV1-19e binding currency (designer draft t-543)

Plan: `docs/tasks/specs/20261113-fv1-19-binding-currency-spec.md`, judged with the Lead's provisional fork choices
(F1 a, F2 a, F3 b, F4 a, F5 b, F7 a, F8 a). Code read at `fv119-n2fix` (S\) and `fv119-n3` (S3\), read-only.

**Verdict: fit_with_fixes** — one blocking spec edit (B-1), seven non-blocking text edits (N-1..N-7). This verdict is an input:
accepting the draft and the fork choices stays with the Lead.

## Findings

**B-1 (blocking; §4 M3, §5 B21, T3). F7 (a) drops judgments silently, against Lead direction 2.** M3 forwards a judgment field on
rename only when current, and says itself that the precheck then names nothing ("none does, so the binding reads as 'no judgment
yet'"). B2 confirms that a missing judgment raises no finding. In practice almost every legacy binding is stale against its new id.
For example, the seed at `test_obligation_join.py:189-190` has hash `hb`, the plan hash is something else, and the rename
(`migrate_artifacts.py:416`) runs on resume with no role present. So `design_assessment` and `code_validity` disappear and nothing
names them. Direction 2 says "nothing is silently dropped". Fix: M3 states the carrier. Per renamed binding, the `changed` note
(or a `left` row, `migrate_artifacts.py:432-435`) names the fields not carried and gives the door: "judged against an earlier
text; re-judge and send through `manifest_put.py --fragment`". Add a T3 row that checks the note names `design_assessment` and
`code_validity`.

**N-1 (B6 overclaims "No ordering makes a field current whose value was written against another text").** Under F2 (a), design's
currency is the whole `obligation_hash`. `_binding_stamp_allowed` decides it from a snapshot read outside the lock
(`manifest_put.py:2435` reads before `store.commit` at `:2511`; the lock is only `event_store.py:645-646`). Trace:
1. Writer B (the automator) reads plan P1 and sends `design_assessment`, stamped H1.
2. Re-plan to P2.
3. Writer A (a receipt or probe) reads P2. No binding of the id is stored yet, so `_binding_stamp_allowed` → True
   (`contract.py:5364-5365`), and A's patch carries H2.
4. Commit order B then A. `dict(old, **binding)` (`manifest_put.py:1943`) leaves hash H2 with B's P1 design, so the design counts.

`judged_on` does not have this race, because only sent fields are stamped. The race needs a re-plan concurrent with S5 writes,
which is rare. Fix (text, Lead's choice): either name the residual in B6, or re-check inside `validate` (which runs under the lock
with `fold(events)`, `:2493-2499`): a binding the stamp hashed while it sent no `design_assessment` is refused/retried when the
folded stored binding of that id changed since the snapshot. (F2 (b) would close this by construction. I still hold F2 (a), see
below.)

**N-2 (§5 B12, empty map / unknown id).** The behaviour of a judged field sent while the map is empty is not stated. No
`judged_on` is emitted, so the merge keeps the stored per-key stamp (or, for a legacy binding, the stored hash), and the new
value inherits it. This is harmless: the stamp counts only while the text equals the stamped text. But it must be written as
the behaviour, with an r10 extension that pins it (stored `judged_on` unchanged).

**N-3 (C1 tests, F5 b).** C1 alters `_binding_stamp_allowed` under F5 (b), but T1 has no row for it. Add r16: stored
`{OB-1, design_assessment: sufficient}` with no hash, then a `review_receipt_ref` patch, then stored hash still absent and
design not current; the existing row `test_manifest_put_merge.py:816-821` (stored `{"obligation_id":"OB-1"}`, no design) still
stamps. Also align the predicate's test with the precheck's "counting value". M5 uses `not in (None, JUDGED_UNKNOWN[f])`, while
F5 (b) says "non-null". Use the `JUDGED_UNKNOWN` test in both places, so a stored `design_assessment: unknown` does not block a
stamp that nothing will ever name.

**N-4 (§5 B13, factual error).** The stamp does not read `plan_obligations`. `plan_obligation_map` → `obligation_map` takes ALL
rows "whatever their schema" (`contract.py:5238-5248, 5262`). A schema-1 row that carries `coverage_obligations` IS stamped, and
gets `judged_on`. It is harmless, because the projection skips it (`coverage_contract.py:574`) and the precheck returns early
(`s5_precheck.py:3849-3851`). Correct the B13 text.

**N-5 (§1.2, C1 owns census line).** The "only if the census test demands" condition is decidable now. `UNIT_NAME_RE`
(`test_judgment_census.py:69`) matches none of `binding_currency`, `stamp_obligation_refs` or `JUDGED_FIELDS`, so no census row
is demanded. Write that, and warn the builder that any helper named `judged_*` (for example `judged_on_of`) matches `^judged_`
and WOULD demand a row.

**N-6 (T3 / M3 wording).** "A judgment field" in M3 must be defined as the keys of `binding_currency` (design +
`JUDGED_FIELDS`). Under F3 (b) `sensitivity` is forwarded, so the existing check `test_obligation_join.py:227-229` ("the renamed
binding keeps its own fields", `sensitivity: proven`) stays green. Name it in T3 beside row (o) (`:239-240`).

**N-7 (§4 M6).** The contract line `artifact-contract-automation.md:161` still reads `obligation_hash (sha256 of the approved
obligation)`, which describes a field a role fills. Reword it in the same edit ("the code's"), or the added clause contradicts
the shape line. Also: C1 changes role-visible refusals (a `judged_on` refusal, a dropped equal hash) but owns no changelog
fragment. State that C2's fragment covers both nodes.

## Forks (judged as asked)

- **F1 (a): holds.** It has one writer and per-key fold, and it follows a package precedent (`coverage_contract.py:732-741`).
  (b) writes a role's fields from code, and (d) makes the automator send code-owned fields.
- **F2 (a): holds**, with N-1 named. (b) closes the race, but it costs two stamps of design until `witnessed` (`:281`) moves.
  That costs more than a rare residual that is named.
- **F3 (b): holds; the residual is harmless.** After a design re-send, the stale `sensitivity` word is shown (`:595`, gated by
  design's `current`). It enters `verified` only through `:602-604`, ANDed with `witnessed`. `witnessed_binding` needs window
  items whose refs hash equals the binding hash (`:280-282`). Window items take that hash from the row refs at build
  (`window_record.py:1321-1323`), so a window built on the current text is required. `proven` additionally needs the window
  item's probe `evidence_ref` (`:268-274`), and `not_required` the window's `unchanged` plus the code-measured `_proof_owed`
  (`:275-279`). No other production code reads the projection item's `sensitivity`: a Grep -i of `["']sensitivity["']` over
  `S3\*.py` finds only binding readers (`case_stamp.py:486`, `contract.py:5462`, `probe_by_code.py:7518`, `coverage_contract.py:268,275`)
  and window gap kinds. The positive control in the same call is `coverage_contract.py:595,646`. Q-d already queues the binding
  readers.
- **F4 (a): holds.** A word is informed (FR-4, P13), and AR-28 is held at the projection, which counts nothing stale whatever
  the precheck says. `PASSABLE` is at `s5_precheck.py:82`.
- **F5 (b): holds; it is the safe direction.** A hash-less binding is an unknown text. Today `_binding_stamp_allowed` returns
  True for `stored.get("obligation_hash") in (None, "")` (`contract.py:5364-5365`), so any receipt starts counting a design that
  was never tied to any text. That is an unknown becoming a pass (FR-59, AR-28). The brief's "silent" example would also leave
  the stale binding with no surface (direction 2). Fixes N-3 apply.
- **F7 (a): holds**, only with B-1.
- **F8 (a): holds; the hole exists.** In `contract.py:5416-5424` (N2fix; the same lines in N3, `:5420/5422`), `:5418` handles
  only `sent in (None, "")` and `:5422` only `sent != want`. A sent value equal to `want` falls through with the hash kept, and
  `merge` (`manifest_put.py:1943`) overwrites the stale stored hash, which revives design. The role can learn `want` from the
  stale-refs text (`contract.py:5316-5317`). With an empty map, `:5416` is false and the sent hash is stored as sent. No later
  check catches either case: `obligation_hash_problems` (`manifest_put.py:592-622`) reads only `tests[]`.

## DoD keys

1. **Load-bearing facts.** Everything below is verified at file:line. The stamp is outside the lock and `merge` is inside it
   (`manifest_put.py:2435`, `:2511`; `event_store.py:645-646`); the plan states this correctly, and N-1 corrects only its
   invariant. The writer is today a whole-dict merge (`:1941-1944`), which M2 makes per key. The C2 readers are complete. The
   Grep -i `code_validity|design_assessment` over `S\*.py` finds production readers only at `coverage_contract.py:581,594,645-646`,
   `contract.py:5366`, `metrics_projection.py:152` and `ledger.py:1740`. The last two read the projection item, which C2 makes
   current, so they need no change. The positive control is the same call's test hits. The precheck has no `obligation_hash`
   reader (the designer's count matched mine: `coverage_contract.py` 6 hits, lines 281/580/732/740/749/754). The F7 road is
   `migrate_artifacts.py:395-435` with `_forwardable` `:166-184`.
2. **AR-22/23 walk.** `judged_on` is produced by the stamp and read by `binding_currency`, by `merge` (fold and materialization)
   and by `_forwardable` (drop). `JUDGED_UNKNOWN` is a constant read by the projection and the precheck. The empty outcome is
   declared (§2: absent / `{}` / non-dict). The world-1 behaviour is stated for every reader (projection: legacy; precheck:
   legacy; merge: materialization; rename: legacy currency), except the empty-map inheritance (N-2).
3. **AR-14/AR-13 kept.** Code writers build bindings by key (`probe_by_code.py:7544-7549`, `red_sandbox.py:1863-1866`) and never
   spread a stored binding, so no `judged_on` leaks. One currency reader, `binding_currency`. The plan-reader divergence
   (`plan_rows` vs `_plan_rows_of`) is pre-existing and queued (Q-c).
4. **Forks**: above.
5. **JUDGMENT.** Every added check is hash equality or presence. No role value is classified: the `JUDGED_UNKNOWN` membership
   test is the projection's own "counts for nothing" words, not a judgment of quality. The owner (data) and the class (xref) are
   named per check; census rows: N-5.
6. **Node cut.** C1 then C2 is executable by a weaker model once B-1, N-3 and N-6 are in. The owns are function-scoped, and the
   tests are rows of keep files (`test-layers.json` rows named). Ratchets that move: `role-load.json` `process_ratchet_tokens`
   for `qa-automator` and `qa-code-critic` (the contract slice grows), named in the C2 DoD. No census row (N-5).
7. **Verdict**: fit_with_fixes.

**One road (q.12):** none found. `JUDGED_FIELDS` is a schema constant, and there is no language/project/case branch (the plan
text was grepped for language names; only the C2 DoD's own grep pattern hits). Every writer, role or code, reaches the same
stamp. **Duplication:** `binding_currency` takes over the projection's inline comparison (`:580`) rather than adding a second
one. The precedent `obligation_hashes` (`:732-741`) is a different carrier (manual records), so not a clone.

## Trail

Read: the plan (whole); `reviews/20261113-fv119-n2n3-code-critic.md:60-73`; S\`contract.py:5176-5270, 5290-5470`;
S\`coverage_contract.py:255-294, 560-660`; S\`manifest_put.py:592-631, 1021-1060, 1925-1950, 2395-2520`; S\`event_store.py:600-669`;
S\`migrate_artifacts.py:160-189, 375-444`; S\`s5_precheck.py:78-95, 3830-3888`; S\`window_record.py:228-255, 1316-1325`;
S\`probe_by_code.py:7505-7553`; S\`red_sandbox.py:1855-1884`; S\`tests/test_manifest_put_merge.py:808-967`;
S\`tests/test_obligation_join.py:177-291`; `references/artifact-contract-automation.md:156-169`;
`judgment-census.json` (rows 145-153, 896-904); `test_judgment_census.py` (grep: :18, :69); `tools/critic_verdict.schema.json`;
`docs/tasks/critic-diff-brief.md`.
Searches: the Grep -i `code_validity|design_assessment` over S\`*.py`; the Grep -i `["']sensitivity["']` over S3\`*.py` (control:
coverage_contract 595/646); the Grep -i `obligation_hash` over S\`coverage_contract.py` (6 hits); the Grep of
`_binding_stamp_allowed|elif sent != want` in S3\`contract.py` (5359/5420/5422, the same as S\); the Grep -i
`binding hash|stale binding|re-stamp|design_assessment` over the package `*.md` (contract line 162 and slices, changelog
fragment); the census Grep for the four functions (`:149`, `:900`). No test re-runs: this is a plan gate with no mechanical layer.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1: F7 (a) drops design_assessment/code_validity on rename with no surface (M3 says the precheck names nothing; B2 no finding) -- violates Lead direction 2; M3/B21/T3 must name the carrier (migrate note per renamed binding with the door) and a test row"
  ],
  "fixes": [
    "B-1 (blocking) section 4 M3 + section 5 B21 + T3: the rename's changed/left note names the judgment fields not carried and the re-judge door; T3 row pins it",
    "N-1 section 5 B6: name the race residual (snapshot outside the lock lets a receipt stamp H2 over a concurrent P1 design) or add an in-lock re-check in validate",
    "N-2 section 5 B12: state that a judged field sent with an empty map inherits the stored stamp (harmless, counts only while text equals the stamped one); extend r10",
    "N-3 section 6 T1: add r16 for the F5 (b) predicate change; align the predicate with JUDGED_UNKNOWN (counting value), not non-null",
    "N-4 section 5 B13: the stamp reads plan_obligation_map/obligation_map over all schemas (contract.py:5238-5262), not plan_obligations; correct the text",
    "N-5 section 1.2 + C1 owns: no census row is demanded (UNIT_NAME_RE test_judgment_census.py:69); warn against helpers named judged_*",
    "N-6 section 4 M3 + T3: define judgment field = keys of binding_currency; name test_obligation_join.py:227-229 as staying green under F3 (b)",
    "N-7 section 4 M6: reword artifact-contract-automation.md:161 obligation_hash as the code's; state C2's changelog fragment covers C1"
  ],
  "class_completeness": "Surface: binding currency (stamp, fold, readers). Walked: every production reader of design_assessment/code_validity/sensitivity (projection, metrics_projection, ledger read the projection item; case_stamp and binding_receipt_ref queued Q-d); every code writer of bindings (window_record, red_sandbox, probe_by_code, migrate rename) - none spreads a stored binding; the race and empty-map neighbours (N-1, N-2); schema-1 plan (N-4). Axis 28 one door text and s5.md queued; axis 34 no language branch; axis 18 role-load rows named.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-fv1-19-binding-currency-spec.md",
      "docs/tasks/specs/reviews/20261113-fv119-n2n3-code-critic.md:60-73",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/contract.py:5176-5470",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/coverage_contract.py:255-294,560-660",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/manifest_put.py:592-631,1021-1060,1925-1950,2395-2520",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/event_store.py:600-669",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/migrate_artifacts.py:160-189,375-444",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/s5_precheck.py:78-95,3830-3888",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/window_record.py:228-255,1316-1325",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/probe_by_code.py:7505-7553",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/red_sandbox.py:1855-1884",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/tests/test_manifest_put_merge.py:808-967",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/tests/test_obligation_join.py:177-291",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/references/artifact-contract-automation.md:156-169",
      ".claude/worktrees/fv119-n2fix/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json:145-153,896-904",
      ".claude/worktrees/fv119-n3/ai-packages/qa-factory/scripts/contract.py (grep 5359/5420/5422)",
      "tools/critic_verdict.schema.json",
      "docs/tasks/critic-diff-brief.md"
    ],
    "reruns": []
  }
}
```
