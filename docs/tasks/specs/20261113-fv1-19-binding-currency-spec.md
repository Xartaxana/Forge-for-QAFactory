# FV1-19e — binding currency: a stale obligation binding has its own surface, and refreshing one judgment does not revive another — DESIGNER DRAFT (fix round 1)

Designer (opus), task t-543, 13.11.2026; fix round 1 after the critic-on-plan verdict t-555
(`docs/tasks/specs/reviews/20261113-fv1-19-binding-currency-plan-critic.md`, fit_with_fixes: B-1 blocking, N-1..N-7). Intent brief: the
Lead's dispatch t-543 and the fix-round brief. Source findings: re-review t-505 queue note QA
(`docs/tasks/specs/reviews/20261113-fv119-n1-fix-rereview.md:58-62`) and code critic t-533 Q-1
(`docs/tasks/specs/reviews/20261113-fv119-n2n3-code-critic.md:64-71`). Parent spec: `docs/tasks/specs/20261113-fv1-19-obligation-refs-spec.md`
(§4 M1/M2, §5, §6, §8a-§8c). Lead fork decisions taken in this round are recorded in §8; forks still open are F9 and F10 (§8), returned,
not decided. Every change of this round is listed in §11 "Fix round".

Code is cited at the tree the brief names: N1+N2+N2fix = worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv119-n2fix\ai-packages\qa-factory`
(branch `wip/fv119-n2fix` at bdd0c04; prefix `S\` = its `scripts\`), N3 = worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv119-n3\ai-packages\qa-factory`
(branch `wip/fv119-n3` at f0f1b77; prefix `S3\`). Owns lines below use the live paths under `C:\QAFactory\forge-repo\ai-packages\qa-factory\`;
the builder works in its own worktree off the base named in §6 "Bases".

## §0. The problem, restated from the carriers

1. **One hash gates four things.** `S\coverage_contract.py:580` `current = binding.get("obligation_hash") == content_hash(ob)`; `:581`
   design, `:594` `code_validity`, `:595` `sensitivity`, `:597` `witnessed` are all read only `if current`. After a re-plan the automator
   re-sends `design_assessment`; N1's stamp then writes the new plan hash onto the binding (`S\contract.py:5359-5366`
   `_binding_stamp_allowed` returns True for a non-null `design_assessment`; `:5416-5421` stamps), and `S\manifest_put.py:1941-1943`
   `dict(stored, **incoming)` keeps the stored `code_validity` / `sensitivity` — so they count again although they were judged on the old text.
2. **A stale binding has no surface.** `S\coverage_contract.py:580` projects `unknown` silently. `S\s5_precheck.py` reads no
   `obligation_hash` at all (Grep -i `obligation_hash` over `{s5_precheck,branch_accounting,window_record,acceptance,coverage_contract,check_delivery,ledger}.py`:
   0 hits in `s5_precheck.py`, positive control in the same call: hits in `acceptance.py` 3, `coverage_contract.py` 6, `window_record.py` 6).
   The only text naming the binding door is a clause inside the ROW refs finding, `S\window_record.py:248` (read this round:
   "; a stale binding hash: re-send the binding's `design_assessment` through ..."), reached only while a row ref of the same obligation is
   also stale. (The clause is N2's: absent from `S3\window_record.py`, whose `_obligation_refs_problem` is at `:226` without the `known`
   parameter `S\window_record.py:231` carries.)
3. **What the window already protects (read, load-bearing for F3).** `S\coverage_contract.py:280-282` (`witnessed_binding`): every
   instance the binding names must carry, in the ACCEPTED WINDOW, an `obligation_refs` item whose hash equals the binding's hash; the window
   is frozen at build (`S\window_record.py:1323` writes the item hash from the row refs) and validated against its receipt
   (`S\coverage_contract.py:203-206`). `sensitivity == "proven"` additionally needs `probe_receipt_ref` == the window item's probe
   `evidence_ref` (`:268-274`); `not_required` needs the window item's `change_disposition == "unchanged"` (`:275-279`). So `witnessed` —
   and through it `sensitivity` inside `verified` (`:602-604`, `:627-629`) — is bound to a window built on a specific obligation text.
   `code_validity` has no such binding: `:594` is its only gate, and `verified` reads it at `:628`. (Critic t-555 confirmed: F3 (b) residual harmless.)
4. **Who writes the fields** (Grep over `S\*.py` for `"obligation_bindings":\s*\[|\{"obligation_bindings"|obligation_bindings=`; production hits):
   - `review_receipt_ref`: `S\window_record.py:1853-1869` `publish_review_receipt` (code, through `manifest_put.py` subprocess);
   - `sensitivity: proven` + `proof_kind` + `probe_receipt_ref` (+ `instance_ids`): `S\red_sandbox.py:1863-1866`, `:1880`, and
     `S\probe_by_code.py:7526-7552` `_binding_items` (only when `_held_action` returns `set`, `:7545-7549`; on `kept: ...` the item carries
     NO sensitivity keys), both through `manifest_put.py`;
   - forwarded whole: `S\migrate_artifacts.py:416` `_rename_legacy_obligations` (via `_forwardable`, `:166-184`); on `origin/main`
     (`.claude\worktrees\read-main\...\migrate_artifacts.py:395`) the rename forwards `dict(binding, obligation_id=new)` WITH the stored hash;
   - `design_assessment`, `code_validity`, `assertion_refs`, `change_disposition`, `change_basis_ref`, `quality_receipt_refs`,
     `sensitivity: not_required`: a ROLE through a fragment. No code writer sends `code_validity` (Grep -i `code_validity` over `S\*.py`:
     only `coverage_contract.py:594, 646` (readers) and tests; positive control: those reader hits). No role text names a WRITER of
     `code_validity` either (Grep -i `code_validity` over `*.md` of the package: only the contract shape lines
     `references/artifact-contract-automation.md:164` and its two slices; positive control: those three hits). See queue line Q-b.
5. **Precedent for per-judgment currency already in the package.** A manual evidence record carries its own
   `obligation_hashes: {oid: hash}` and is refused when one is not `content_hash` of the current obligation
   (`S\coverage_contract.py:732-741`, "manual capture binds stale or missing obligation hash"); a window item carries the refs hash it was
   built on (`S\window_record.py:1323`). The binding is the one judgment carrier whose fields share ONE hash.
6. **The F8 hole in N1's B1 (confirmed by critic t-555; CLOSED by node C1, stamp step 3, F8 (a) taken).** `S\contract.py:5416-5424`
   (read this round): `:5418` handles only `sent in (None, "")`, `:5422` only `sent != want`; a binding that SENDS `obligation_hash`
   equal to the plan's hash falls through with the hash kept, the merge (`S\manifest_put.py:1943`) overwrites a stale stored hash with it
   and revives `design_assessment` with no re-judgment. The current hash is printed to the role by the stale refs finding
   (`S\contract.py:5316-5317` "the plan's obligation hashes to <h>"), so the input is reachable. With an EMPTY map (`:5416`
   `if plan_map and ...` false) a sent binding hash is stored as sent. No later check catches either (`obligation_hash_problems`,
   `S\manifest_put.py:592-622`, reads only `tests[]` — critic t-555). Pinned by T1 rows r9, r10.
7. **Race window.** `S\manifest_put.py:2429-2435` reads the plan and the stored bindings and runs the stamp BEFORE `store.commit`
   (`:2511`); `S\event_store.py:632-648` holds the lock only around `_commit_locked` (append + `validate(events, payload)` + `project`).
   The stamp's reads are outside the lock; `merge` (run by `project`/`fold`) is inside it.
8. **The rename road and its report (read this round, load-bearing for B-1 / F9).** `_rename_legacy_obligations`
   (`S\migrate_artifacts.py:378-435`) runs inside `_migrate_instance_ids` (`:475`), called by `run_if_older` (`:497-534`), which the conductor
   runs on resume (`skills/qa-story/SKILL.md:227` "migrates by code once; never ask the person about it") and whose JSON report
   (`{"changed", "left", ...}`) is printed whole on stdout (`:557`) and journalled ONCE as event `artifacts_migrated`
   (`:482-494`; vocabulary `S\log_append.py:89-93`) — with each `left` reason CUT to 80 characters (`:489` `x['reason'][:80]`) and the notes
   to 2000 (`:492`). Readers of `artifacts_migrated`: Grep over the package: only the vocabulary line and the test
   `S\tests\test_story_resume_migration.py:96` (positive control: the writer `migrate_artifacts.py:492`, same call). The stamp already
   receives the stored bindings of the fragment's ids (`S\manifest_put.py:2435` `_current_rows(task_root, "obligation_bindings")`), the
   old id's stored binding included. `manifest_put` carries no binding-key whitelist (Grep -i `binding_keys|unknown key` over
   `{manifest_put,contract,coverage_contract}.py`: 0; positive control `obligation_bindings` same call shape in `manifest_put.py`: 20).

## §1. AR-n touched, owner and census class of every check

### 1.1 AR-n, with the change check written into the DoD

| AR | How kept | Change check (DoD of the node named) |
|---|---|---|
| AR-28 (an unknown never becomes a pass) | a judgment field counts only when the hash it was stamped with equals the current obligation's; every unreadable/absent/corrupt currency reads "not current"; a re-sent field never refreshes another; a rename never writes the new plan hash onto a judgment whose stored stamp differs | C1 T1 rows r2, r4, r9, r14, r17; T3 rows t3-a, t3-c; C2 rows p3, p4 |
| AR-13 (a fact with a reader is read through it) | ONE currency reader `contract.binding_currency` and ONE counting test `contract.counting_value` for the projection, the precheck, the stamp's F5 (b) predicate and the rename report; the precheck takes plan obligations through `contract.plan_obligation_map` (-> `obligation_map`) | C2 DoD: Grep `obligation_hash` in `coverage_contract.py` and `s5_precheck.py` -> the only binding-hash comparison left is inside `contract.binding_currency` (line `:281` window-item-vs-binding comparison stays, it is not a currency read); C1 DoD: Grep `JUDGED_UNKNOWN\[` outside `contract.py` -> only `coverage_contract.py` defaults |
| AR-14 (one artifact, one writer) | `judged_on` and every binding hash are written by `stamp_obligation_refs` alone (+ `merge`'s fold of what the stamp sent); a role or code writer sending `judged_on` is refused / forwards none; `renamed_from` is an instruction the stamp consumes and pops, never stored | C1 rows r8, r13, r17 (the output never carries `renamed_from`) |
| AR-15 (one survivor) | the stale-binding door lives in ONE text (the new binding finding); the clause in `_obligation_refs_problem` is removed | C2 row p10; Grep `design_assessment` in `window_record.py` -> no hit |
| AR-22 (producer <-> reader) | new field `judged_on`: producer the stamp; readers `binding_currency` (projection, precheck, rename report), `merge`, `_forwardable` (drop); new fragment key `renamed_from`: producer `_rename_legacy_obligations`, reader the stamp (consumed); the contract text names `judged_on` in the same commit | C2 DoD: Grep -i `judged_on` over `scripts/`, `agents/`, `skills/`, `references/`, `handoffs/` with a positive control (`obligation_hash` same call) -> hits only in `contract.py`, `manifest_put.py`, `coverage_contract.py`, `s5_precheck.py`, `migrate_artifacts.py`, the contract text and its slices, tests; C1 DoD: Grep `renamed_from` over `scripts/*.py` -> only `contract.py`, `migrate_artifacts.py`, tests |
| AR-23 (empty outcome declared) | `judged_on` absent = a binding written before this node (legacy reading, §2); `judged_on: {}` = written after, no judgment field sent; a non-dict = corrupt = nothing current; a rename with no non-current counting field writes no `left` row | C1 rows r5, r10, r14; T3 rows t3-b, t3-d |
| AR-25 (every state a way out) | a stale binding has a named door (re-send the stale judgment fields) and a precheck finding naming it before the finish; a renamed binding whose judgments were made on another text gets the same door | C2 rows p1, p8, p12 |
| AR-27 (a finding, bug or gap reaches the report under its own owner) | a judgment a rename could not carry as current is named in the migration report (`left`, stdout + journal `artifacts_migrated`) with its owner (the automator) and its door, and stays on the binding for the S5 precheck to name (F9 (b)) | C1 T3 row t3-a; C2 row p12 |
| AR-9 / AR-10 (refusal names expected + door; requirement told before work) | the precheck finding text (FR-1, FR-2, FR-57), the `renamed_from` refusals, and the contract line about `judged_on` reach their reader before the work | C2 rows p1, p10; C1 r17; contract text diff |
| AR-20 (shrink-only ratchets) | the contract text grows by one clause and line 161 is reworded: `role-load.json` `process_ratchet_tokens` of the roles whose slices carry the section (`qa-automator`, `qa-code-critic`) may move; no census row (N-5, §1.2) | C2 DoD: `test_role_load.py` and `test_judgment_census.py` green in the witness; every raised row named in the commit and the critic verdict |
| AR-29 (code judges data; judgment by a tier above) | every check added is a hash equality / presence / membership-in-the-projection's-own-"counts-for-nothing"-words check; WHICH judgment is right stays the role's | §1.2 |
| AR-1 / AR-2 (variety) | no language, project or case branch; `JUDGED_FIELDS` is a schema constant of the binding contract, not project variety | C2 DoD Grep `typescript\|\.spec\.ts\|java\|csharp` in the diff -> none |

### 1.2 Owner and census class of every check added or altered (AR-29, P27, `S\tests\fixtures\judgment-census.json` vocabulary)

| Check | Owner it serves | Census class |
|---|---|---|
| `contract.binding_currency(binding, plan_hash)` (new predicate) | data (code): hash equality per field | `xref` (a join of a stored stamp against the plan); no census row demanded (below) |
| `contract.counting_value(binding, field)` (new helper: value not None and not `JUDGED_UNKNOWN[field]`) | data (code): membership in the projection's own "counts for nothing" words, not a quality judgment (critic t-555 DoD key 5) | `shape`; no census row demanded |
| `stamp_obligation_refs` binding branch (altered: refuses a sent `judged_on`; validates and consumes `renamed_from`; pops every sent binding hash per F8 (a); emits `judged_on`; carried stamps on a rename) | data (code): what the code computes is never typed | `xref`; no census row today for the stamp (Grep `stamp_obligation_refs` in the census: 0 hits; positive control `obligation_ref_problems` same call: 1 hit) and none demanded |
| `_binding_stamp_allowed` (altered, F5 (b) taken: a stored binding with no hash but a COUNTING `design_assessment` is treated like a stale one) | data (code) | unchanged (data); no row demanded |
| `manifest_put.merge` per-key fold of `judged_on` with legacy materialization | not a check: the projection writer's step | — |
| `s5_precheck.check_obligations` (altered: + the stale-binding finding) | data (code): presence + hash equality; the role decides the new judgment | unchanged row `judgment-census.json:900` (`xref`, owner `data`, roles `qa-automator`) |
| `coverage_contract.coverage_projection` validity line (altered reader) | data (code) | not a refusal; projection |
| `migrate_artifacts._rename_legacy_obligations` (altered: sends `renamed_from`; after the put, names the non-current counting fields of each renamed binding in a `left` row) | data (code): a report writer step; the naming is a currency read through `binding_currency` | not a check |

**Census rows (N-5, decided now, not conditional).** `UNIT_NAME_RE` (`S\tests\test_judgment_census.py:69`:
`^(check_|rule_|judge|judged_|_?validate|_?refuse)|^_?(check|run)$|(_check|_errors|_problems)$`) matches none of `binding_currency`,
`counting_value`, `stamp_obligation_refs`, `JUDGED_FIELDS`, `JUDGED_UNKNOWN`, `_binding_stamp_allowed`, `_rename_legacy_obligations`: no census
row is demanded and `judgment-census.json` is NOT in any owns. **Warning to the builder:** a helper whose name starts `judged_` (e.g.
`judged_on_of`), `judge`, `check_`, `rule_`, `_validate`/`validate`, `_refuse`/`refuse`, or ends `_check`/`_errors`/`_problems` WOULD demand a
row — do not name a new helper that way; if one is unavoidable, stop and return the question (the census is not in your owns).
Which judgment value is right (sufficient / valid ...) stays the automator's and the code critic's judgment (P17, P27); no code reads it.

## §2. Data shape — before / after, with the migration rule

**Before** (`references/artifact-contract-automation.md:160-166`): a binding
`{obligation_id, obligation_hash, instance_ids[], design_assessment, assertion_refs[], change_disposition, change_basis_ref, code_validity,
sensitivity, quality_receipt_refs[], quality_not_applicable_reason?, probe_receipt_ref, review_receipt_ref}`; ONE `obligation_hash` certifies
every field; line 161 describes it as `obligation_hash (sha256 of the approved obligation)` — a field a role might fill.

**After** (Lead-taken shape F1 (a) + F2 (a) + F3 (b)):
- `obligation_hash` keeps its N1 meaning and becomes, by name, the stamp of `design_assessment` (refreshed only by a re-sent non-null
  `design_assessment`, `_binding_stamp_allowed`). It also keeps feeding `witnessed` (`:281`, `:597`), unchanged. It is the code's.
- new `judged_on: {<field>: <plan hash at write time>}` for every field of `contract.JUDGED_FIELDS` (F3 (b): `("code_validity",)`).
  Written ONLY by the stamp: on every incoming binding whose id is in a non-empty plan map, the stamp sets
  `judged_on = {f: <current plan hash> for f in JUDGED_FIELDS if the binding sends f with a non-null value}` — possibly `{}` — except on a
  renamed binding (M1 step 4b), where a counting field gets the stamp the old id's stored binding held for it.
- `merge` folds `judged_on` PER KEY: `stored.judged_on ∪ incoming.judged_on`, the incoming key wins; it never replaces the whole map.
- currency per field (`binding_currency`): `design_assessment` current iff `obligation_hash` is a non-empty str equal to the plan hash; a
  `JUDGED_FIELDS` member current iff (binding has `judged_on` as a dict and `judged_on[f]` equals the plan hash) OR (binding has NO
  `judged_on` key and `obligation_hash` equals the plan hash — the legacy reading); a `judged_on` present but not a dict → not current.
- "judgment field" = a key of `binding_currency`'s result: `design_assessment` + `JUDGED_FIELDS` (N-6). Under F3 (b) `sensitivity` is NOT a
  judgment field in this sense: it keeps today's gate (design's `current`) and is forwarded on a rename like any other field.

**Migration rule (TEMPORAL: world 1 = manifests written before C1 merges; world 2 = after; C1 creates the key).**
- No stored manifest is rewritten; `merge` replays old events unchanged (they carry no `judged_on`; the new branch runs only when the
  INCOMING binding carries a `judged_on` dict).
- A world-1 binding (no `judged_on`) is read exactly as today: every field current iff `obligation_hash` is current. Nothing becomes proven
  that was not; nothing goes red that was green.
- The FIRST world-2 write to a world-1 binding carries `judged_on` (the stamp always emits it, `{}` included), so `merge` MATERIALIZES the
  legacy currency before it folds: for every `f` in `JUDGED_FIELDS` that the STORED binding carries non-null and the incoming `judged_on`
  does not name, `judged_on[f] = stored.obligation_hash` (the hash it was certified by, read BEFORE this event's hash refresh), only when that
  stored hash is a non-empty str; otherwise `f` gets no key (not current). From that write on, the binding is per-field. This runs INSIDE the
  commit lock (in `merge`), so a concurrent writer cannot interleave between the materialization and the fold.
- Consequence for the re-plan case: world-1 binding (hash H1, design, `code_validity: valid`) → plan changes to P2 → the automator re-sends
  `design_assessment` → the event carries `judged_on: {}` → merge materializes `judged_on.code_validity = H1` and the binding hash becomes
  H2 → design current, `code_validity` NOT current. The QA defect closes for world-1 and world-2 bindings alike.
- **A story renamed BEFORE C1 and read after (TEMPORAL, rename road).** The released rename (`origin/main`, `migrate_artifacts.py:395`)
  forwarded the stored hash with the binding, so such a renamed binding carries its OLD hash and no `judged_on`: world-1 reading → its
  judgments are current iff that old hash equals the new id's plan hash, and C2's precheck names the stale ones. The rename runs once per
  plugin upgrade (`story_version.check`, `S\migrate_artifacts.py:502-504`) and a renamed story holds no `OB-n` any more, so C1's rename
  never re-runs on it. N1's rename (forward without hash, stamp current) exists only on the unmerged branches, so no stored story carries
  its silent carry-over.

## §3. Requirements (numbered; N = 7)

1. **Currency per judgment.** A judgment field of a binding counts in the coverage projection only when the hash it was written against
   equals `content_hash` of the current plan obligation; writing one field never changes another field's currency (AR-28; Lead direction 1).
2. **One writer of currency.** Every binding hash and every `judged_on` stamp is written by `contract.stamp_obligation_refs` (folded by
   `merge`); a fragment that sends `judged_on` is refused with a door; code writers forward none (AR-14).
3. **One reader of currency.** `contract.binding_currency` is the only function that compares a binding's stamps with the plan; the
   projection, the precheck and the rename report call it (AR-13, AR-15; Lead direction 2).
4. **A stale binding is named before the finish.** `s5_precheck.check_obligations` names every bound obligation of the dispatch's scope
   whose binding carries a counting judgment that is not current, with the fields and the door; the binding clause leaves the row-refs finding.
5. **Migration without traps.** World-1 bindings keep today's reading until their first world-2 write; then their legacy currency is
   materialized; no stored manifest is rewritten; old journals fold unchanged.
6. **The code judges data only.** Every new check is presence or hash equality; which judgment is right stays the role's (P27, AR-29;
   Lead direction 3).
7. **No judgment disappears unnamed on a rename (B-1; Lead direction of the fix round).** On a rename a judgment field that is not current
   against the new id's plan obligation is NEVER silently dropped and NEVER silently carried over as current: it is named to the role that
   owes it again (the automator, through the S5 precheck finding of requirement 4) and in the record a report reads (the migration report's
   `left`, printed whole and journalled as `artifacts_migrated`); a judgment that IS current against the new text is carried and counts.
   (Recommended carrier F9 (b); the carrier choice is returned as fork F9.)

## §4. Mechanism

M1 — **`contract.py`** (pure; beside `stamp_obligation_refs`):
- `JUDGED_FIELDS` (tuple, F3 (b): `("code_validity",)`) and `JUDGED_UNKNOWN = {"design_assessment": "unknown", "code_validity": "unverified",
  "sensitivity": "missing"}` — the projection's "not counted" words, today literals at `S\coverage_contract.py:581, 594, 595`; the projection
  reads its defaults from it (one source).
- `counting_value(binding, field) -> bool` — `isinstance(binding, dict) and binding.get(field) is not None and binding.get(field) !=
  JUDGED_UNKNOWN.get(field)`. The ONE "counts if current" test, used by `_binding_stamp_allowed` (F5 (b)), the precheck (M5) and the rename
  report (M3) (N-3 alignment).
- `binding_currency(binding, plan_hash) -> dict` — `{"design_assessment": bool, <each JUDGED field>: bool}` per §2. Not a dict binding,
  a `plan_hash` that is not a non-empty str → every value False. Never raises.
- `_binding_stamp_allowed` (F5 (b), taken): `stored` is not a dict → True; `stored` has a non-empty str hash → today's rule (`== want` or
  the incoming binding re-sends a non-null `design_assessment`); `stored` has no / an empty hash → True only when NOT
  `counting_value(stored, "design_assessment")` or the incoming binding re-sends a non-null `design_assessment`. (The INCOMING re-send test
  stays "non-null": re-judging to `unknown` is a re-judgment and may stamp.)
- `stamp_obligation_refs` binding branch, in this order per binding (after the existing null-hash drop `:5414`):
  1. a `judged_on` key with value `None` is dropped (null = not sent, D7); any other `judged_on` value → problem
     `obligation_bindings[<at>].judged_on is the code's (the obligation hash each judgment was made against); leave it out, the code writes it`;
  2. a `renamed_from` key with value `None` is dropped; any other value is POPPED and validated: valid iff it is a non-empty str, differs
     from the binding's `obligation_id`, is listed in the same fragment's `retracted_obligations` (a list; a non-list reads as empty), and
     `stored_by_id` holds a binding of that id; otherwise ONE problem `obligation_bindings[<at>].renamed_from <value> names no stored binding
     this fragment retracts; leave it out, it is the migration's` (renamed_from is the code's rename instruction, never stored);
  3. (F8 (a), taken — closes §0 item 6) the sent `obligation_hash` is ALWAYS popped after it is compared: with a non-empty map and a known
     id, a sent value ≠ want is the existing problem (`_hash_problem`); a sent value == want is treated as not sent; with an empty map or an
     id the map lacks it is popped silently (the merge keeps the stored hash);
  4. with a non-empty map and a known id:
     a. no valid `renamed_from`: `_binding_stamp_allowed` decides the binding hash; then
        `binding["judged_on"] = {f: want for f in JUDGED_FIELDS if binding.get(f) is not None}`;
     b. a valid `renamed_from` X, `old = stored_by_id[X]` — CARRIED STAMPS (B-1, F9 (b)): the binding hash = `old["obligation_hash"]` when
        `counting_value(binding, "design_assessment")` and that stored hash is a non-empty str; no hash key when the design counts and the
        stored hash is absent/empty/non-str; `want` when the design does not count (row (o) unchanged). `judged_on[f]` for each
        `f in JUDGED_FIELDS` sent non-null: when `counting_value(binding, f)` → the old stamp of `f` (`old["judged_on"][f]` if `old` carries a
        dict `judged_on` and that value is a non-empty str; else, when `old` carries NO `judged_on` key and a non-empty str hash, that hash;
        else no key); when not counting → `want`. A carried stamp equals `want` exactly when the old judgment was made on the text the plan
        states now — then it counts; otherwise it does not, and the value stays on the binding to be named (requirement 7);
  5. with an empty map or an unknown id: no `judged_on` is emitted (nothing to stamp against); a valid `renamed_from` changes nothing
     further (popped in step 2).
  Docstring updated with steps 1-5.

M2 — **`manifest_put.merge`** binding block (`S\manifest_put.py:1941-1944`): for each incoming binding, `new = dict(old, **binding)`; when
`binding.get("judged_on")` is a dict: `base = dict(old["judged_on"])` if `old` carries a dict `judged_on`; `{}` if `old` carries a non-dict
`judged_on`; else (legacy) `{f: old["obligation_hash"] for f in C.JUDGED_FIELDS if old.get(f) is not None}` when `old["obligation_hash"]` is
a non-empty str, else `{}`; then `new["judged_on"] = dict(base, **binding["judged_on"])`. Pure; no read of the plan. (A renamed binding's
new id has no stored binding → `old = {}` → base `{}` → `judged_on` = the carried stamps.)

M3 — **code writers.**
- `migrate_artifacts._forwardable` drops `judged_on` on both its branches (like `obligation_hash`).
- `_rename_legacy_obligations` (`S\migrate_artifacts.py:378-435`) — the rename NAMES, never drops and never revives (requirement 7, F9 (b)):
  1. `:416` becomes `renamed.append(_forwardable(dict(binding, obligation_id=new, renamed_from=old)))`: every field of the stored binding is
     forwarded (as N1), the stamp writes the carried stamps (M1 step 4b);
  2. after a successful put (`ok` at `:428`), re-read the manifest (`_read_manifest(root)`) and the plan (`C.plan_obligation_map(root)`); for
     each `(old, new)` renamed, take the LAST stored binding of `new`; `stale = [f for f in ("design_assessment", *C.JUDGED_FIELDS) if
     C.counting_value(b, f) and not cur[f]]` with `cur = C.binding_currency(b, content_hash(plan_map[new]))` when `new in plan_map`, else every
     counting field is stale (safe side);
  3. for each non-empty `stale`, append ONE `left` row: `{"artifact": f"obligation_bindings[]:{new}", "reason": "not current, re-judge: "
     + ", ".join(stale) + f" (renamed from {old}; judged against another text of this obligation than the plan states now, so they count for
     nothing until the automator re-sends them through manifest_put.py --fragment; the S5 precheck names them)"}` — the field list FIRST,
     so the journal's 80-character cut (`:489`) keeps it (`"not current, re-judge: design_assessment, code_validity"` = 55 characters);
  4. the re-read raising → ONE `left` row `{"artifact": "automation-manifest.json", "reason": "renamed; the judgment currency of the renamed
     bindings could not be read back (<ExcName>: <exc>): the S5 precheck names any stale one"}`; the rename stays committed;
  5. `changed` keeps today's note (`:432-434`) unchanged.

M4 — **readers.** `coverage_contract.coverage_projection`: `cur = C.binding_currency(binding, content_hash(ob))`; `current =
cur["design_assessment"]` (replaces `:580`, same value); `:594` → `binding.get("code_validity", C.JUDGED_UNKNOWN["code_validity"]) if
cur["code_validity"] else C.JUDGED_UNKNOWN["code_validity"]`; `:595` unchanged, gated by `current` (F3 (b)); `:581` reads its default from
`JUDGED_UNKNOWN`; `:597-604` unchanged.

M5 — **precheck finding.** `s5_precheck.check_obligations` (`S\s5_precheck.py:3835-3886`): `known = C.plan_obligation_map(task_root)` once;
for each scoped case's plan obligation that is BOUND (the existing `any(...)` at `:3874-3875` is True) and whose id is in `known`: take the
binding of that id (bindings are unique by id after the merge, `S\manifest_put.py:1941`); `stale = [f for f in ("design_assessment",
*JUDGED_FIELDS) if C.counting_value(binding, f) and not cur[f]]` where `cur = C.binding_currency(binding, content_hash(known[oid]))`; when
`stale` is non-empty and the id has not yet been reported in this call → ONE finding:
- check/family `obligations` (F4 (a), taken); case = the first scoped case reaching it; tag `binding-stale-<oid>`;
- message: `<oid> (<case>): the binding's <f1>[, <f2>] <was|were> written against another text of this obligation than the plan states now
  (the plan changed, or the binding was renamed to this id, after <it|they> <was|were> judged), so the coverage map counts <it|them> as unknown`;
- fix: `read the obligation as the plan states it now, judge again, and send the field(s) you re-judged in one fragment through
  `manifest_put.py --task <T> --fragment <file>`: {"obligation_bindings": [{"obligation_id": "<oid>", "<f1>": "<v1|v2|v3>"[, ...]}]}; the
  code stamps each field you send with the current hash, a field you do not send stays uncounted, and you never send `obligation_hash` or
  `judged_on`` — `<v...>` from the contract vocabulary (`design_assessment` `sufficient|partial|unknown`, `code_validity` `valid|unverified`).
And `window_record._obligation_refs_problem` (`S\window_record.py:248`) loses the clause `; a stale binding hash: re-send ... re-stamps
the hash` — the stale refs text keeps `REF_REPAIR` only.

M6 — **contract text.** `references/artifact-contract-automation.md:160-166`: line 161 `obligation_hash (sha256 of the approved
obligation)` is reworded to `obligation_hash (the code's: the hash of the obligation text design_assessment was judged on)` (N-7), and one
clause is added after `review_receipt_ref}`: "`judged_on` is the code's too (the obligation hash each other judgment field was written
against); never send it or `obligation_hash`: re-send the fields you re-judged and the code stamps them". `renamed_from` is NOT put in
role text (a migration-only instruction the stamp consumes; closed choice §9.7). Slices regenerated with
`python -B scripts/contract_slices.py --write` (`S\contract_slices.py:816`), checked with `--check`.
Changelog: ONE fragment `changelog.d/fv1-19e-binding-currency.md`, owned by C2, covers BOTH nodes — C1's role-visible refusals (a sent
`judged_on`, an invalid `renamed_from`, an equal or empty-map binding hash now dropped) and the rename's new `left` rows, and C2's precheck
finding and contract text (N-7).

## §5. Edges (behaviour | invariant)

| # | Edge | Behaviour | Invariant protected |
|---|---|---|---|
| B1 | Binding with NO stored hash, carrying a counting judgment (real data: `S\tests\test_s5_precheck.py:3197-3200` `OB3_BINDING`, copied from TP2-2406, has `design_assessment: sufficient` and no hash) | F5 (b), taken: projection: design not current (as today, `:580`); precheck: finding naming `design_assessment` with the door; stamp: only a re-sent `design_assessment` stamps (a stored `design_assessment: unknown` does not block a stamp — `counting_value`) | a judgment never written against any recorded text never starts counting on a receipt write |
| B2 | Hash present, judgment field ABSENT (never judged) | not in `stale`; projection shows `JUDGED_UNKNOWN[f]`; no finding from this node | absence of a judgment is not staleness; no new demand (FR-5) |
| B3 | Field present with its unknown word (`design_assessment: unknown`, `code_validity: unverified`, `sensitivity: missing`) | not in `stale` (`counting_value` False); not named by the rename report | no repair asked for a value that cannot pass |
| B4 | Field sent as `null` | not stamped (stamp step 4a keys on non-null); `merge` stores null as today; projection reads null (not `valid`) | a null never counts |
| B5 | Field written by CODE (a probe's `sensitivity`, `migrate_artifacts` forwarding) vs by a ROLE | the stamp is writer-agnostic: whoever sends a `JUDGED_FIELDS` value gets the current hash on it; code writers drop `judged_on` (M3); the rename carries the OLD stamps (M1 step 4b) | a stamp says "written while this plan text was current", never "who wrote it"; a code writer never carries a judgment across a text change as current |
| B6 | Two writers racing (e.g. `probe_by_code.publish_binding` and the automator's fragment) — corrected after N-1 | the stamp (plan read, stored bindings read, `_binding_stamp_allowed`, `judged_on` emission) runs OUTSIDE the lock (`S\manifest_put.py:2429-2435`); the commit lock (`S\event_store.py:645-646`) covers append + `validate` + `project` = `merge`, so the per-key fold and the legacy materialization run INSIDE it. `judged_on` fields: each writer stamps only what it sends, so no ordering makes a `JUDGED_FIELDS` value current whose value was written against another text. **Named residual (design's stamp, F2 (a)):** writer B reads P1 and sends `design_assessment` stamped H1; the plan changes to P2; writer A (a receipt / probe) reads P2 while no binding of the id is stored yet, `_binding_stamp_allowed` → True (`S\contract.py:5364-5365`), A carries H2; commit order B then A → `dict(old, **binding)` (`S\manifest_put.py:1943`) leaves H2 over B's P1 design, which counts. Needs a re-plan concurrent with S5 writes on a never-bound id. Whether to close it in-lock is fork F10 | `judged_on`: a race only demotes (AR-28); `obligation_hash`: one named residual, closed or kept per F10 |
| B7 | Re-plan changes an obligation's text and later BACK to the old text | stamps equal the old hash again → those fields count again; fields re-judged under the intermediate text stop counting | a judgment counts exactly when the text it was judged on is the text now (no clock involved) |
| B8 | Re-plan, automator re-sends ONLY `design_assessment` (the QA defect) | design current; every `JUDGED_FIELDS` value keeps its old stamp (world 2) or gets the materialized old hash (world 1) → not current; precheck names it | refreshing one field never revives another |
| B9 | Receipt-only patch over a stale binding (`review_receipt_ref`, probe publish) | binding hash unchanged (B1 of N1); `judged_on` emitted with only the JUDGED fields it sends (none for a receipt; a probe under F3 (b) sends no JUDGED field) | a receipt never re-validates a judgment made on other text |
| B10 | A fragment sends `judged_on` (`{}`, `{"code_validity": "<h>"}`, `"x"`, `[]`, `{"a": {"b": 1}}`, a 10 000-key map) | refused, one problem per binding, through the existing `_problems_text` line (ceiling and spill file as N1 E16); `null` → dropped | a stamp the code did not compute is never stored (AR-14) |
| B11 | A fragment sends a binding `obligation_hash` EQUAL to the plan's over a stale stored binding without `design_assessment` (§0 item 6) | F8 (a): treated as not sent → `_binding_stamp_allowed` → no refresh | the role's knowledge of the current hash never revives a judgment |
| B12 | Empty plan map (no plan, unreadable plan, plan naming no obligation) — extended after N-2 | stamp: no `judged_on`, sent binding hash popped (F8 (a)), a valid `renamed_from` popped with no further effect; merge: nothing materialized (incoming carries no `judged_on`), so a JUDGED field sent now INHERITS the stored per-key stamp (world 2) or, on a world-1 binding, the stored hash (legacy reading) — the new value counts only while the plan text equals that stamped text; projection: no schema-2 rows → no item; precheck: `check_obligations` returns at `:3850` (no schema-2 obligations) | nothing unproducible is demanded (FR-5); nothing is stamped against an unknown text (AR-28); an inherited stamp counts only while its text is the text now |
| B13 | Legacy schema-1 plan — corrected after N-4 | the stamp reads `plan_obligation_map` → `obligation_map`, which takes ALL rows "whatever their schema" (`S\contract.py:5238-5248, 5262`): a schema-1 row carrying `coverage_obligations` IS stamped and gets `judged_on`; harmless — the projection skips schema-1 rows (`S\coverage_contract.py:574`) and the precheck returns early (`S\s5_precheck.py:3849-3851`) | a stamp on a row no reader projects changes no verdict |
| B14 | `manual-*` obligation | no finding (`:3872-3873` skip); projection overrides validity/sensitivity (`S\coverage_contract.py:614-626`) | manual evidence has its own currency (`:740`) |
| B15 | Case handed to a person / case not in the dispatch scope | no finding (existing skips `:3861-3862`, scope loop) | the precheck speaks only of the dispatch's own work |
| B16 | Binding absent for an owed obligation | the existing "no obligation binding" finding only; no stale finding | one finding per condition |
| B17 | One binding reached by two scoped cases | one finding (first case), not two | one repair, one finding |
| B18 | The plan file is read by two readers: precheck `_plan_rows_of` (`work/test-plan.json` then `test-plan.json`, `S\contract.py:5181-5185`) vs projection `plan_rows` (`work/test-plan.json` only, `S\coverage_contract.py:287-292`) | when only the root `test-plan.json` exists, the precheck may name a stale binding the projection does not project; the repair is harmless | pre-existing divergence of two plan readers, named, not widened (queue line Q-c) |
| B19 | Duplicate obligation id across plan rows (an invalid plan) | precheck hashes `known[oid]` (last wins, `S\contract.py:5238-5248`); projection hashes each row's own `ob` | equal on every valid plan (`S\coverage_contract.py:321-344` refuses duplicate schema-2 ids, per parent E23) |
| B20 | `judged_on` stored as a non-dict (a corrupt or hand-edited manifest) | `binding_currency` → every JUDGED field not current; next world-2 write: `merge` base `{}`; a rename from such an `old` carries no JUDGED stamp (step 4b "else no key") | corruption only demotes |
| B21 | Rename road over a legacy binding — rewritten after B-1 (requirement 7, F9 (b)) | every field of the stored binding is forwarded; a counting judgment field current against the new id's plan obligation is carried and counts; a counting judgment field NOT current is carried WITH its old stamp (never `want`), counts for nothing, is named in ONE migration `left` row per renamed binding (field list first) and by the S5 precheck finding `binding-stale-<new>`; a binding with no counting judgment field gets `want` as its hash (N1 row (o) unchanged) and no `left` row | no judgment disappears unnamed and none is carried as current across a text change |
| B22 | POSITIONAL (M1 step order): `judged_on` refusal, `renamed_from` validation and the hash pop run before `_binding_stamp_allowed`, the carried stamps and the emission; the unknown-id refusal `unknown_obligation_refusal` (`S\manifest_put.py:2407`) still runs before the stamp (`:2435`) | a fragment refused for `judged_on` or `renamed_from` writes nothing (journal unchanged); a word-passed unknown binding id gets no stamp and no `judged_on` | the stamp never stamps an id the plan does not name; a refused fragment never half-lands |
| B23 | POSITIONAL (M2): materialization reads the STORED hash before `dict(old, **binding)` replaces it | the legacy fields get the hash they were certified by, never the refreshed one | the refresh of design never certifies a legacy field |
| B24 | Error direction of the reused `obligations` precheck family in a new, gating role (F4 (a)) | a word or `*` passes the precheck finding; the projection still counts nothing stale (AR-28 holds at the projection) | a person's word passes a gate, never makes a stale judgment count |
| B25 | Error direction of `binding_currency` (new reader feeding a gate input) | may err only toward "not current". Adversarial inputs that must read NOT current: `judged_on` = `[]`, `"x"`, `None`, `{"code_validity": "<h> "}` (trailing space), uppercase hex, `{"code_validity": 123}`, `{"code_validity": ""}` with `plan_hash` `""`, binding hash `None` with `judged_on` absent, binding not a dict | a stamp measured on other bytes never counts |
| B26 | `renamed_from` adversarial (role or code): `5`, `""`, `[]`, an id not in the fragment's `retracted_obligations`, `retracted_obligations` not a list, an id retracted but with no stored binding, the binding's own id; `null` | one problem each, fragment refused (`EXIT_BAD_FRAGMENT`), journal unchanged; `null` dropped; a VALID one sent by a role yields only old stamps | error direction: the carried-stamp branch may err only toward "not current" — its stamp is either the old one (current only when equal to `want`) or none; it can never give `want` to a counting value whose old stamp differs |
| B27 | Rename report limits (pre-existing): the journal cuts each `left` reason to 80 characters (`S\migrate_artifacts.py:489`) and the notes to 2000 (`:492`); stdout is whole (`:557`) | the field list opens the reason (55 characters for both judgment fields); with many renamed bindings the journal line may lose rows past 2000 characters — the manifest still holds every stale stamp, and the precheck reads the manifest, not the journal | the naming that reaches the role does not depend on the journal's cut |
| B28 | Rename: the manifest re-read after the put fails / the plan no longer names `new` | one `left` row "renamed; ... could not be read back ..." / every counting field of that binding named stale | when currency cannot be read, the report errs toward naming, never toward silence |
| B29 | TEMPORAL, a story bound and renamed before C1, read after (§2 last bullet) | the released rename forwarded the old hash → world-1 reading → stale judgments uncounted, C2's precheck names them; C1's rename never re-runs (no `OB-n` left, version stamp) | a pre-change rename never becomes a pass after the change |

## §6. Nodes (owns by FUNCTION; for a weaker model; every test is a row of an existing keep file)

Common to both nodes: given `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md` (whole),
`C:\QAFactory\forge-repo\plans\builder-rules.md`, `C:\QAFactory\forge-repo\docs\TESTING.md`, this spec, the parent spec §4-§5. New cases
are ROWS of existing tables in keep files (`S\tests\test-layers.json`: `test_manifest_put_merge.py` `:2912` (layer `detector`, `covers`
includes `contract.py`, `manifest_put.py`, `coverage_contract.py` `:2940`), `test_s5_precheck.py` `:4770` (`gate_named`),
`test_obligation_join.py` `:3345` (`covers` includes `coverage_contract.py` `:3353`)); no new test file. The quarantined
`test_coverage_contract.py` (`test-layers.json:7693`) and `test_coverage_targeted_projection.py` (`:7701`) are NOT run or edited. FR walk
in each report: A (refusal / finding text), C (FR-11, FR-14, FR-38), D (FR-59), E (FR-41), G; B — no text a PERSON reads changes.
`judgment-census.json` is in no owns (§1.2, N-5).

### Bases (fix-round brief)

- **Both nodes are based on `wip/fv119-n2fix` at bdd0c04** (worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv119-n2fix`): it carries
  N1 + N2 + the N2 fix round, and C2 edits N2's text (`S\window_record.py:248` binding clause, present only there; `check_obligations` at
  `S\s5_precheck.py:3835`, the N2 position — `.claude\worktrees\fv119-n2\...\s5_precheck.py:3835` too, while `S3\` and `read-main` have
  it at `:3843`).
- **`wip/fv119-n3` (f0f1b77) need NOT be merged first.** Read this round: every function C1/C2 own sits at the same line in both trees
  (`contract.py` `_binding_stamp_allowed` 5359, `stamp_obligation_refs` 5369; `manifest_put.merge` 1774; `migrate_artifacts._forwardable`
  166, `_rename_legacy_obligations` 378; `coverage_projection` 560); the two differences (`check_obligations` 3835 vs 3843,
  `_obligation_refs_problem` signature) are N2's, i.e. on the n2fix side. N3's own work is the finish `_s5_v2_collect` in `controller.py`
  (journal t-527 note; NOT verified by a git diff — the designer has no shell), outside both owns; critic t-533 recorded a clean merge-tree
  of N2 + N3 (66684c8, journal t-527 `accepted`). The integrator merges N3 on its own road. If the Lead prefers one tree, merging f0f1b77
  into the C1 branch at its start is safe per that merge-tree.
- **C1 → C2 strictly sequential** (C2 calls `binding_currency`, `counting_value`, `JUDGED_UNKNOWN` from C1): C2 branches from C1's accepted
  head. Nothing inside this spec runs in parallel; both nodes may run in parallel with other topics whose owns do not cross (§6 "Crossings").

### C1 — currency writer: stamp, fold, code writers, rename naming (FV1-19e-a)
given: this spec §0-§5, §8; parent spec §4 M1/M2; `S\contract.py:5232-5426`; `S\manifest_put.py:1774-1945, 2353-2520`; `S\migrate_artifacts.py:166-184, 378-535`; `S\tests\test_manifest_put_merge.py:790-960`; `S\tests\test_obligation_join.py:177-290`; `S\tests\test_judgment_census.py:17-19, 69`
owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\contract.py` (new `JUDGED_FIELDS`, `JUDGED_UNKNOWN`, `counting_value`, `binding_currency`, placed after `_binding_stamp_allowed`; `_binding_stamp_allowed` (F5 (b)); `stamp_obligation_refs` binding branch `:5407-5425` + docstring)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\manifest_put.py` (`merge`: the `obligation_bindings` block `:1935-1944` only)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\migrate_artifacts.py` (`_forwardable` `:166-184`; `_rename_legacy_obligations` `:378-435`)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manifest_put_merge.py` (rows of table T1)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_obligation_join.py` (rows of table T3 in section 4)
non-goals: no reader change (projection, precheck, window_record are C2); no change of `run` outside the stamp call (the stamp is called where it is, `:2435`); no rewrite of stored manifests; no change of the row-refs stamp (`_stamp_row_refs`); no `probe_by_code.py` change; no change of `_journal_migration` (its 80/2000 cuts are pre-existing, §11 noticed); no census edit; no changelog (C2's fragment covers C1).
handoff: diff + report (`.claude/agents/builder.md` rule 7) with the witness output verbatim, the FR walk, the `architecture:` line (AR-13, AR-14, AR-22, AR-23, AR-25, AR-27, AR-28) and the `judgment:` line.
edges: B1 (stamp half), B4, B5, B6, B7, B8, B9, B10, B11, B12, B20, B21, B22, B23, B25, B26, B27, B28, B29 (behaviour and invariant in §5).
DoD: table T1 rows r1-r17 and T3 rows t3-a..t3-e green; Grep `renamed_from` over `scripts/*.py` -> only `contract.py`, `migrate_artifacts.py`, tests; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the owns above>` and the files it prints, output attached verbatim; `test_judgment_census.py` in the witness green with the census UNCHANGED (any helper name matching `UNIT_NAME_RE` is a stop-and-ask).
siblings: axis 34 (no language branch: covered); axis 23 n/a (no `tests[]` row field changes); the F8 hole of §0 item 6 is closed here (step 3); the rename is the one code writer that carries judgments (B5, B21).
designer: this file (accepted draft path, once accepted).

Table T1 — `test_manifest_put_merge.py`, ONE parameterised table "binding currency" (each row: name, steps through `Stand.put` / `MP.merge` /
`C.stamp_obligation_refs`, expected `C.binding_currency(<stored binding>, content_hash(<plan ob>))` and exit code):
- r1 world 2, plan P1: binding with `design_assessment: sufficient`, `code_validity: valid` → `{design: True, code_validity: True}`, stored
  `judged_on == {"code_validity": h(P1)}`;
- r2 (THE defect row, red before C1) re-plan to P2; re-send only `design_assessment` → `{design: True, code_validity: False}`;
- r3 then re-send `code_validity` → `{True, True}`;
- r4 over a stale binding: `review_receipt_ref`-only and `sensitivity`-only patches → nothing becomes current (extends the existing B1 run rows `:934-956`);
- r5 world 1: an old-shape event (binding with `obligation_hash: h(P1)`, design, validity, no `judged_on`) folded through `MP.merge` → under P1 `{True, True}`, under P2 `{False, False}`;
- r6 world 1 + a design-only re-send under P2 → stored `judged_on == {"code_validity": h(P1)}` (materialized), currency `{True, False}`;
- r7 after r6, plan back to P1 → `{False, True}` (B7);
- r8 `judged_on` sent as `{}`, `{"code_validity": h}`, `"x"`, `[]`, nested, 10 000 keys → `EXIT_BAD_FRAGMENT`, journal and tree unchanged, stderr names `judged_on` and "leave it out, the code writes it"; `null` → exit 0, key dropped;
- r9 (F8 defect row) a sent binding hash == h(P2) over a stale stored binding without `design_assessment` → stored hash unchanged;
- r10 empty map (no plan file): `code_validity` sent → exit 0, no NEW `judged_on` key written, sent binding hash not stored; extended (N-2): over a stored world-2 binding with `judged_on == {"code_validity": h(P1)}` the stored `judged_on` is unchanged after the put (the new value inherits h(P1)), and over a stored world-1 binding the stored hash is unchanged;
- r11 a journal of old events folds to the same manifest before and after C1 (merge pure); folding a world-2 journal twice gives equal results;
- r12 race shape (pure `MP.merge`): fragments A (design re-send, emitted `judged_on: {}`) and B (validity re-send, `judged_on: {"code_validity": h2}`) computed from one snapshot, applied A→B and B→A → in both orders no `JUDGED_FIELDS` value is current whose fragment did not stamp it current (the design residual of B6 is not pinned here: F10);
- r13 `_forwardable` (both `refs` values) drops `judged_on`;
- r14 `binding_currency` adversarial table (B25 inputs) → every value False;
- r15 a `JUDGED_FIELDS` value sent as `null` → not stamped, stored null, not current-and-counting;
- r16 (N-3, F5 (b)) pure `C.stamp_obligation_refs` with the `receipt` patch of `:815`: stored `[{"obligation_id": "OB-1", "design_assessment": "sufficient"}]` (no hash) → output binding has NO `obligation_hash`; stored `[{"obligation_id": "OB-1", "design_assessment": "unknown"}]` → stamped `want` (a non-counting value never blocks); stored `[{"obligation_id": "OB-1", "design_assessment": "sufficient"}]` + a re-sent `design_assessment` → stamped `want`; the existing row `:816-821` (stored `{"obligation_id": "OB-1"}`, no design, among its eight inputs) stays green unchanged;
- r17 (B-1, B26) pure `C.stamp_obligation_refs` with `retracted_obligations: ["X"]` and a binding `{"obligation_id": "OB-1", "renamed_from": "X", "design_assessment": "sufficient", "code_validity": "valid"}`; stored X variants → output: X `{hash "old", design, validity}` → `obligation_hash == "old"`, `judged_on == {"code_validity": "old"}`, no `renamed_from` key, `binding_currency(out, want) == {False, False}`; X hash == `want` → hash `want`, `judged_on {"code_validity": want}`, `{True, True}`; X with no hash and no `judged_on` → no hash key, `judged_on == {}`; X `{hash "old", judged_on {"code_validity": "jv"}}` → `judged_on == {"code_validity": "jv"}`; binding without `design_assessment` (only `sensitivity: proven`) over X hash "old" → hash `want`; adversarial `renamed_from` = `5`, `""`, `"Y"` (not retracted), `"X"` with `retracted_obligations: "X"` (not a list), `"X"` retracted but no stored X, `"OB-1"` (own id) → exactly one problem each naming `renamed_from` and "it is the migration's"; `renamed_from: null` → dropped, no problem, normal stamp (`want`).

Table T3 — `test_obligation_join.py`, rows in section 4 (the rename; `run_script("migrate_artifacts.py", "--task-root", ..., "--if-older")`
as at `:200`, report = last stdout line):
- t3-a (THE B-1 row) seed a legacy `OB-1` binding with `obligation_hash: "hb"` (≠ `content_hash(plan TS-1-O1)`), `design_assessment:
  sufficient`, `code_validity: valid` → the renamed `TS-1-O1` binding still carries `design_assessment == "sufficient"` and `code_validity ==
  "valid"` (nothing dropped), `obligation_hash == "hb"`, `judged_on == {"code_validity": "hb"}`, `C.binding_currency(b, plan_hash) ==
  {"design_assessment": False, "code_validity": False}` (nothing current); the report's `left` holds exactly one row with artifact
  `obligation_bindings[]:TS-1-O1` whose reason STARTS `not current, re-judge: design_assessment, code_validity` and contains `renamed from
  OB-1` and `manifest_put.py --fragment`; `reason[:80]` still contains `design_assessment, code_validity` (B27);
- t3-b the same seed with `obligation_hash == content_hash(plan TS-1-O1)` → both fields carried and current (`{True, True}`), no `left` row for `TS-1-O1`;
- t3-c a legacy binding with no hash and `design_assessment: sufficient` → carried, no hash stored, `{design: False}`, one `left` row naming `design_assessment`;
- t3-d the EXISTING seed (`:188-193`: `OB-1` with `sensitivity: proven`, hash `hb`, no design) → the existing checks stay green unchanged: `:227-229` "the renamed binding keeps its own fields" (`sensitivity == "proven"`) and row (o) `:239-240` "the renamed binding carries the plan's hash of its new id"; and no `left` row names `TS-1-O1` (no counting judgment field; N-6);
- t3-e a second run renames nothing and adds no `left` row (extends `:254-257`).

### C2 — currency readers: projection, precheck finding, one door, contract text (FV1-19e-b; depends C1)
given: this spec; `S\coverage_contract.py:560-660`; `S\s5_precheck.py:3835-3886`, `:82`, `:4492-4625`; `S\window_record.py:228-253`; `S\tests\test_s5_precheck.py:3191-3268, 4600-4640`; `references/artifact-contract-automation.md:150-194`; `S\contract_slices.py`
owns:
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\coverage_contract.py` (`coverage_projection`: lines `:580-581`, `:594-595` only)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\s5_precheck.py` (`check_obligations` only)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\window_record.py` (`_obligation_refs_problem` `:248` only: the binding clause removed)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\references\artifact-contract-automation.md` (section "Coverage v2 bindings and S5 review window" `:160-166` only: line 161 reworded + the added clause)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\references\slices\` (regenerated by `contract_slices.py --write` only, no hand edit)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\references\role-load.json` (`process_ratchet_tokens` rows of the roles whose load moves, by the measured delta only)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-19e-binding-currency.md` (new fragment, covering C1 and C2)
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_s5_precheck.py` (rows of table T2; the QB row `:4628-4632` rewritten; the row `:3229-3230` filtered to the unbound-finding tag (F5 (b)))
`C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_manifest_put_merge.py` (row p-proj of table T2 only)
non-goals: no change of `witnessed_binding`, of `:597-604`, of `check_row_fields`, of `PASSABLE` (`:82`) or the word road; no change of `s5.md` (queued, §7); no `probe_by_code.py` change (F3 (b) taken); no contract text for `renamed_from`.
handoff: as C1, `architecture:` line AR-9, AR-10, AR-13, AR-15, AR-20, AR-22, AR-25, AR-27, AR-28, AR-29.
edges: B1 (precheck half), B2, B3, B12-B19, B24 (§5).
DoD: table T2 rows green; Grep `design_assessment` in `window_record.py` → no hit; Grep `obligation_hash` in `coverage_contract.py` → only `:281` and the `obligation_hashes` manual lines `:732-754` remain outside `C.binding_currency`; the AR-22 Grep of §1.1 with its positive control; `python -B scripts/contract_slices.py --check` exit 0 (from the package root, in the builder's worktree); `test_role_load.py` and `test_judgment_census.py` in the witness, every raised row named in the commit; `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the owns above>` and the files it prints, verbatim; `python -B scripts/selftest.py --lang` on the changed package files (FR-30); the changelog fragment names C1's refusals and rename rows (N-7).
siblings: axis 28 (render sites of the row-form door: the binding clause leaves the refs finding, one text survives; `s5.md` queued, §7); axis 23 n/a (no carrier row changes); axis 34 covered (one door for every language, no branch).
designer: this file (accepted draft path, once accepted).

Table T2 — `test_s5_precheck.py`, rows beside the OB-3 rows (`obligation_story` / `obligation_findings`, `:3204-3220`; a plan hash
helper reads `content_hash` of the plan's OB-3):
- p1 bound OB-3, binding hash ≠ plan hash, `design_assessment: sufficient`, `code_validity: valid` → ONE finding, id ends
  `binding-stale-OB-3`, message names both fields and "written against another text", fix names `manifest_put.py --task <T> --fragment
  <file>`, the example with both fields, "never send `obligation_hash` or `judged_on`";
- p2 current binding (hash == plan hash, `judged_on` current) → no stale finding;
- p3 legacy schema-1 plan → none; p4 no plan file → none;
- p5 `manual-*` obligation → none; p6 no binding → only the existing unbound finding;
- p7 hash stale but fields absent or only unknown words → none;
- p8 F5 (b): `OB3_BINDING` (no hash, `design_assessment: sufficient`) → one finding naming `design_assessment`;
- p9 one binding reached by two scoped cases → one finding;
- p10 the stale ROW-refs finding no longer contains `design_assessment` (rewrites `:4628-4632` to `check_not_in`);
- p11 composition: for inputs {r2-state, r5-P2, r6, r7, current}, the finding's field list equals the fields where `C.binding_currency` is
  False and `C.counting_value` is True — N1-family predicate only;
- p12 (B-1, the post-rename shape) OB-3 binding as C1's rename leaves it: `obligation_hash: "hb"`, `judged_on: {"code_validity": "hb"}`,
  `design_assessment: sufficient`, `code_validity: valid` → one finding `binding-stale-OB-3` naming both fields, message contains "renamed
  to this id";
- p-proj (in `test_manifest_put_merge.py`, which covers `coverage_contract.py`): `CC.coverage_projection(task, {"current_results": []},
  <stored manifest of r2>)` → the OB item's `code_validity == "unverified"`, `design_assessment == "sufficient"` (shape of the call:
  `S\tests\test_oracle_provenance.py:764`).
FR-33: the precheck text and the rename `left` row are role-visible changes (closed by code, not proven): the Lead adds `live-runs` rows "a
re-planned story: the automator's precheck names the stale binding; one fragment re-judges; the coverage map counts the re-sent fields only"
and "a resumed legacy `OB-n` story: the migration report names the judgments not carried as current; the S5 precheck names them; one
fragment re-judges".

Crossings: `manifest_put.py` `merge` (C1) vs any open node owning `merge` — the Lead checks the board before launch;
`s5_precheck.check_obligations` is not in FV1-30a's owns (parent spec Crossings `:420`: `_passable`, `passed_by_word`, word-selection
helpers, `word_passes`, `run.word_passes`) — no overlap; T5 owns `s5_precheck.report` and family producers — `check_obligations` is a
family producer, so the parent's `очередь: FV1-19 → T5` covers C2 too (the Lead confirms on the board). `migrate_artifacts.py`
`_rename_legacy_obligations` (C1) — the Lead checks the board for another open owner.

## §7. Four questions (CLAUDE.md rule 10) and queue pointers

(a) **Cost.** Code: one more dict per binding write, one per-key fold, one predicate call per bound obligation in the precheck, one
manifest re-read per rename run — no LLM. Role, after a re-plan or a legacy rename: ONE fragment re-sending the stale judgment fields of
every stale binding (it can be the same fragment that re-sends the row refs). Before this node the role paid nothing and the coverage map lied.
(b) **Axes** (by enumeration, `docs/SIBLING_MAP.md`): axis 1-22: n/a (no forge policy, exam, release, FR, stage twin, measurer, identity,
test-file, words, hooks, money, ratchet other than 18) except axis 18: covered (role-load rows named, C2 DoD; no census row, N-5). axis 23:
n/a (no `tests[]` carrier change). axis 24-27: n/a. axis 28: covered (one door text; `s5.md` queued below). axis 29-31: n/a. axis 32:
covered (§1.2). axis 33: n/a. axis 34: covered (no language/case branch; one road for every writer: role and code writers reach the same
stamp; the rename reaches it with `renamed_from`, the same stamp, no second writer). axis 35-36: n/a.
(c) **Detectors.** T1/T2/T3 rows; `test_judgment_census.py`; calibration check 41; the two `live-runs` rows.
(d) **What stops a skip.** The stamp sits in `manifest_put.run`, the only manifest writer; the fold sits in `merge`, the only projection;
the precheck runs at the automator's exit (`stages.json`); the projection calls the one predicate; the rename's naming runs in the same
function as the rename, after its put.

Queue pointers (one line each, no design):
- Q-a (brief) `skills/qa-story/phases/s5.md:309-311` says the fragment's refusals include "an obligation not on the case's plan row" while
  N1 judges membership against the whole plan (parent F7 (b)): the parent's queued pointer `s5.md:292-299`
  (`20261113-fv1-19-obligation-refs-spec.md:430-432`) widens to `:292-311` — same F1 (c) node of `live-run-fvf`.
- Q-b `code_validity` is read (`S\coverage_contract.py:594`, `:628`) but no role text names its writer (only the contract shape lines,
  §0 item 4) — AR-22 producer question for the Lead (which role judges code validity, and is it the critic's accepted window).
- Q-c Two plan readers: `coverage_contract.plan_rows` (`:287-292`, `work/` only, raises on bad JSON) vs `contract._plan_rows_of`
  (`S\contract.py:5178-5193`) — AR-13 survivor question (edge B18).
- Q-d `case_stamp.py:483-488` and `contract.binding_receipt_ref` (`S\contract.py:5461-5462`) read a binding's `sensitivity == "proven"`
  with no currency; they bind receipt FILES (test bytes), not obligation text — consistent under F3 (b).

## §8. Forks — Lead decisions recorded; F9 and F10 RETURNED

**F1 — how currency is carried per judgment field.** Lead: (a) taken (critic t-555 holds). Options kept for the record: (a) per-field stamps
`judged_on` written by the code, folded per key, legacy materialized; (b) a hash refresh clears the other fields; (c) event-time currency in
the projection; (d) a design re-send must carry every judged field.

**F2 — the shape of the stamp.** Lead: (a) hybrid taken (critic holds, with the B6 residual named — see F10).

**F3 — which fields carry their own stamp.** Lead: (b) `code_validity` only taken (critic: the residual is harmless, §0 item 3).

**F4 — the family of the precheck finding.** Lead: (a) `obligations` taken (critic holds).

**F5 — a binding with NO stored hash that carries a counting judgment.** Lead: (b) taken (critic: the safe direction), with N-3 applied
(`counting_value` in both the stamp predicate and the precheck).

**F6 — none open.**

**F7 — the rename road.** Lead: rewritten to the fix-round direction (binding): on a rename a judgment that is no longer current is NAMED
— to the role that owes it again and in the record a report reads — never silently dropped, never silently carried over as current; a current
judgment is carried. (The draft's (a) "forward only current" dropped judgments unnamed — B-1 — and is withdrawn; N1's (b) "forward all,
stamp current" carries them as current and is excluded by the direction.) The real choice the direction leaves is F9.

**F8 — a binding hash SENT by a fragment.** Lead: (a) taken (critic: the hole exists, `S\contract.py:5416-5424`); closed by C1 step 3, rows r9, r10.

**F9 — RETURNED: on a rename, where the naming of a non-current judgment is written and who is told.**
- (a) Drop + report (critic B-1's minimal fix): the rename forwards only current judgment fields; each renamed binding with dropped fields
  gets a `left` row (or a clause in the `changed` note) naming them and the door. Told: the conductor (it reads the stdout report at resume,
  `SKILL.md:227`) and the journal (`artifacts_migrated`, no report reader today, §0 item 8). NOT told: the automator — the value is gone and
  an absent judgment raises no finding (B2), so the role that owes the judgment again never hears of it. Cost: smallest (migrate only, no
  stamp change). Falls short of the direction's "to the role that owes it again".
- (b) Carry with the old stamp + report (RECOMMENDED; written into this spec): the rename forwards every field with `renamed_from`; the
  stamp gives each counting judgment field the stamp the old binding held (M1 step 4b), so a non-current judgment stays on the binding,
  counts for nothing (projection: `unknown` / `unverified`), and C2's precheck finding names it to the automator with the door before the S5
  finish; the rename also writes a `left` row per renamed binding (field list first; stdout whole, journal cut at 80 per reason). Told: the
  automator (precheck), the conductor and the journal (report); nothing lost, nothing revived. Cost: one consumed fragment key with one
  refusal text and six adversarial rows (r17), one manifest re-read in the rename, T3 rows t3-a..t3-e, T2 p12; no role text, no census row.
  Error direction: only toward "not current" (B26).
- (c) Drop + a stored owed-list: the rename drops the non-current fields and writes a code field `rejudge_owed: [fields]` on the binding
  that the precheck reads and the stamp clears on a re-send. Told: the automator and (if added) the report. Cost: a second currency carrier
  beside the stamps (AR-13 strain), a new field with producer/reader/clear rules, the judgment values lost.
- Sub-choice F9.2 (within (a)/(b)): the report line in `left` (RECOMMENDED: it is work left, and it reaches the journal's `| left:` segment)
  or as a clause of the `changed` note (`:432-434`).
- Sub-choice F9.3: whether the DELIVERY report should also say "judged on another text" for such a field (the coverage projection item
  carries no stale marker; it shows the unknown word). RECOMMENDED: no, not in this node — the projection counting nothing is AR-28's
  guarantee, and a stale marker in the projection/report is a new reader; queued under §11 "noticed".

**F10 — RETURNED: the design-stamp race residual of B6 (critic N-1).**
- (a) Name it only (RECOMMENDED; done in B6): a re-plan concurrent with S5 writes on a never-bound id is rare; F2 (b) would remove it but
  costs two stamps of design until `witnessed` moves (critic F2 judgment).
- (b) Close it in-lock: inside `validate` (under the lock, with `fold(events)`, `S\manifest_put.py:2493-2499`), refuse/retry a binding the
  stamp hashed while it sent no `design_assessment` when the folded stored binding of that id changed since the snapshot. Cost: a snapshot
  token through `run` → `validate`, a retry path, and a T1 race row through `Stand.put`; it touches `run` outside the stamp call (a C1
  non-goal today) — choosing (b) widens C1's owns to `manifest_put.run`/`validate`.

## §9. Small technical choices closed by the designer

1. The finding lives in `check_obligations` (it already joins bindings to the scoped cases' plan rows and owns the unbound-binding finding);
   `check_row_fields` is about `tests[]` rows.
2. One finding per obligation id per precheck run (first scoped case reaching it), tag `binding-stale-<oid>`.
3. `JUDGED_UNKNOWN` holds the projection's three "not counted" words so the precheck's "counting value" test and the projection share one
   source; `counting_value` is the one test over it (N-3).
4. `binding_currency` takes a hash, not an obligation: the projection already has `ob`, the precheck has `known[oid]`; each computes
   `content_hash` once.
5. The stamp emits `judged_on: {}` on a binding that sends no judged field: it is the trigger of the legacy materialization in `merge`
   (§2), and it never makes anything current.
6. Name `judged_on` (reads as "the text each judgment was made on"); no design weight.
7. (F9 (b)) `renamed_from` is consumed by the stamp and never stored; it is not put in role text — a role that sends a valid one only demotes
   its own fields (B26), so no refusal of a valid one is needed.
8. (F9 (b)) The rename names stale fields by re-reading the STORED manifest after its put (one source: what the store holds), not by
   predicting the stamp's result before it.
9. The precheck message names both causes ("the plan changed, or the binding was renamed to this id") so one text serves both roads (AR-15).

## §10. Reading trail

Read whole or in the ranges named (draft round): the two source verdicts (whole); parent spec `:116-465`, `:548-597`;
`S\coverage_contract.py:200-292`, `:520-660`, `:715-760`; `S\contract.py:5178-5437`; `S\manifest_put.py:1925-1950`, `:2280-2520`;
`S\red_sandbox.py:1845-1894`; `S\window_record.py:96-100`, `:127-290`, `:1840-1884`; `S\probe_by_code.py:7490-7639`; `S\case_stamp.py:476-500`;
`S\s5_precheck.py:82-94`, `:266-278`, `:3785-3886`, `:4492-4636`; `S\event_store.py:632-648`; `S3\controller.py:7585-7614`;
`S\migrate_artifacts.py:166-183`, `:385-434`; `S\tests\test_manifest_put_merge.py:808-967`; `S\tests\test_s5_precheck.py:3185-3268`,
`:4620-4635`; `S\tests\test-layers.json:2869-2928`, `:3602-3613`, `:4770-4789`, `:7693-7708`; `references/artifact-contract-automation.md:145-194`;
`references/slices/qa-code-critic/artifact-contract-automation.md:120-157`; `skills/qa-story/phases/s5.md:288-313`; `design/architecture.md:140-281`;
`docs/SIBLING_MAP.md` axes 23, 28, 34; `docs/TESTING.md` (whole); `plans/builder-rules.md` 7b (line 15-18).
Read this fix round: the verdict t-555 (whole); `S\migrate_artifacts.py:150-563`; `S\tests\test_obligation_join.py:170-299`;
`S\contract.py:5230-5429`; `S\manifest_put.py:2395-2444`; `S\log_append.py:75-114`; `S\tests\test_manifest_put_merge.py:808-837`;
`references/artifact-contract-automation.md:156-169`; `skills/qa-story/SKILL.md:218-237`; `logs/journal/dev1.jsonl:1301-1359` (bases).
Searches (each negative with a positive control in the same call shape):
- Grep -i `obligation_hash` over `{s5_precheck,branch_accounting,window_record,acceptance,coverage_contract,check_delivery,ledger}.py`
  (count): `s5_precheck.py` 0; control: acceptance 3, coverage_contract 6, window_record 6.
- Grep -i `code_validity` over `S\*.py`: readers `coverage_contract.py:594, 646` + tests only; over package `*.md`: the three contract lines.
- Grep `"obligation_bindings":\s*\[|\{"obligation_bindings"|obligation_bindings=` over `S\*.py`: production writers `window_record.py:1868`,
  `red_sandbox.py:1880`, `migrate_artifacts.py:425` (+ `manifest_view.py:127` sample, `manifest_put.py:2753-2766` selftest); `probe_by_code`
  builds its fragment by key (`:7621`), read directly.
- Grep `obligation_bindings|binding.*obligation_hash` -i over `S3\controller.py`: one hit `:7598` (`review_receipt_ref` presence only).
- Grep `stamp_obligation_refs|_binding_stamp_allowed|obligation_ref_problems|check_obligations|coverage_projection` over the census:
  hits `:149`, `:900` only.
- Grep `get\("(code_validity|sensitivity|design_assessment)"\)|\["(...)"\]` over `S\*.py`: binding readers `case_stamp.py:486`,
  `contract.py:5366, 5462`, `coverage_contract.py:268, 275`, `metrics_projection.py:152`, `probe_by_code.py:7518`.
- Glob `**/changelog.d/*.md` under the package (control for the fragment path; re-run found `fv1-19a-obligation-refs-stamp.md`).
- (fix round) Grep `artifacts_migrated` over the package: `log_append.py:93`, `migrate_artifacts.py:492` (writer = positive control),
  `tests/test_story_resume_migration.py:96` — no report reader.
- (fix round) Grep `if-older|run_if_older` over the package excluding tests: `SKILL.md:227` is the one role-text caller.
- (fix round) Grep -i `BINDING_KEYS|binding_keys|unknown key|not a key of` over `{manifest_put,contract,coverage_contract}.py`: 0; control
  Grep -i `binding_keys|unknown key|obligation_bindings` count on `manifest_put.py`: 20.
- (fix round) Grep `stale binding hash` over the worktrees' `scripts/*.py`: `fv119-n2\window_record.py:146, 249`,
  `fv119-n2fix\window_record.py:248`; none in `fv119-n3` (N2's text).
- (fix round) Grep `^def (stamp_obligation_refs|_binding_stamp_allowed|obligation_map|plan_obligation_map|binding_receipt_ref|plan_obligations)`
  in S\ and S3\ `contract.py`: identical lines; Grep `^def (merge|check_obligations|coverage_projection|_obligation_refs_problem|_rename_legacy_obligations|_forwardable)\b`
  in S\ and S3\: identical except `check_obligations` 3835/3843 and `_obligation_refs_problem` 231/226; `check_obligations` 3835 in
  `fv119-n2`, 3843 in `read-main` (N2 moved it).
- (fix round) Grep `_forwardable|renamed.append` in `read-main\...\migrate_artifacts.py`: `:395` `renamed.append(dict(binding, obligation_id=new))` only.
- (fix round) Grep `UNIT_NAME_RE` in `test_judgment_census.py`: `:17-19`, `:69`, `:241`.
Not read: `acceptance.py` beyond the grep lines; `_reused_candidate_join`; the full `test_obligation_join.py`; `passed_by_word` internals;
N3's diff (no shell; its file list is taken from the journal, labelled as such in §6 "Bases").
Needed beyond the manifest: `S\red_sandbox.py`, `S\probe_by_code.py`, `S\case_stamp.py`, `S\event_store.py`, `S\migrate_artifacts.py`,
`S\log_append.py`, `skills/qa-story/SKILL.md`, `references/artifact-contract-automation.md`, `S\contract_slices.py`, `S\tests\test-layers.json`,
`judgment-census.json`, `test_judgment_census.py`, `logs/journal/dev1.jsonl`.

## §11. Fix round (after critic-on-plan t-555)

**B-1 (blocking) — answered.** Rule: requirement 7 (§3). On a rename no judgment disappears unnamed: a non-current judgment field stays on
the binding with the stamp it was judged on (M1 step 4b, never the new plan hash), counts for nothing, is named to the automator by C2's
precheck finding and named in the migration report's `left` (M3 steps 2-4); a current one is carried and counts. Where: §3 req 7; §4 M1
steps 2 and 4b, M3 rewritten; §5 B21 rewritten, new B26-B29; §6 C1 owns (`_rename_legacy_obligations` whole), T1 r17, T3 rewritten
(t3-a = the B-1 row: values kept, nothing current, `left` names `design_assessment, code_validity`), T2 p12; §1.1 AR-27 row; §8 F7 rewritten,
F9 returned (the real choice: carrier and who is told; (b) recommended).

**N-1 — applied (text) + fork.** B6 rewritten: the overclaim is withdrawn for design's stamp and the race residual is named with the
critic's trace; `judged_on` keeps the "only demotes" invariant. Closing it in-lock is returned as F10 ((a) name only, recommended).

**N-2 — applied.** B12 states the inheritance (a JUDGED field sent with an empty map inherits the stored per-key stamp / legacy hash;
counts only while the text equals the stamped one); T1 r10 extended to pin stored `judged_on` / hash unchanged.

**N-3 — applied.** T1 r16 added (no-hash stored binding with counting design + receipt → no hash; stored `unknown` design → stamped; the
existing `:816-821` row stays). New `contract.counting_value` is the one "counts" test for `_binding_stamp_allowed` (stored side), M5 and
M3; the incoming re-send test stays "non-null" (§4 M1).

**N-4 — applied.** B13 corrected: the stamp reads `plan_obligation_map` → `obligation_map` over all schemas (`S\contract.py:5238-5248,
5262`); a schema-1 row with obligations is stamped; harmless (projection `:574`, precheck `:3849-3851`).

**N-5 — applied.** §1.2 "Census rows": no row demanded (`UNIT_NAME_RE`, `test_judgment_census.py:69`), census removed from C1 owns, the
`judged_*` (and other prefix/suffix) warning written; C1 DoD requires the census unchanged.

**N-6 — applied.** §2 defines "judgment field" = keys of `binding_currency` (design + `JUDGED_FIELDS`); under F3 (b) `sensitivity` is
forwarded; T3 row t3-d names `test_obligation_join.py:227-229` and row (o) `:239-240` as staying green.

**N-7 — applied.** M6 rewords `artifact-contract-automation.md:161` (`obligation_hash` = the code's) in the same edit; C2's changelog
fragment covers both nodes (M6, C1 non-goals, C2 owns and DoD).

**Critic side answers taken as facts.** F3 (b) harmless (§0 item 3, §8 F3); F5 (b) safe (§8 F5); the F8 hole exists at
`S\contract.py:5416-5424` and is closed by C1 step 3 (§0 item 6, §8 F8, T1 r9/r10) — not queued, fixed in this spec.

**Lead fork decisions recorded (§8).** F1 a, F2 a, F3 b, F4 a, F5 b, F8 a (the draft's recommendations; the critic held each); F7 rewritten
to the binding direction. **Forks still open:** F9 (rename naming carrier; recommend (b), F9.2 `left`, F9.3 no) and F10 (B6 residual;
recommend (a) name only).

**Bases.** C1 on `wip/fv119-n2fix` bdd0c04; C2 on C1's accepted head; `wip/fv119-n3` f0f1b77 not required first (owned functions at the
same lines in both trees; N3's files outside the owns per the journal, not git-verified; merge-tree 66684c8 clean per critic t-533).
Nothing within this spec runs in parallel (C1 → C2).

**Noticed, not in scope.**
- No report reads the journal event `artifacts_migrated` (readers: the vocabulary `S\log_append.py:93` and one test,
  `test_story_resume_migration.py:96`); the migration's `left` rows reach a person or a report only through the conductor reading stdout at
  resume (`SKILL.md:227`, which says only "never ask the person about it").
- `_journal_migration` cuts each `left` reason to 80 characters and the notes to 2000 (`S\migrate_artifacts.py:489, 492`) with no marker
  that it cut — a silent cut in a record (sibling of the FV1-4 silent-cut class).
- The coverage projection item carries no "judged on another text" marker: the delivery report shows a stale judgment only as the unknown
  word (F9.3).
