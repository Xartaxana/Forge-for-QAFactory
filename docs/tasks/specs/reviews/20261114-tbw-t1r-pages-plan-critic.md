# Critic on plan — T1r-pages (told-before-work), task t-716

Plan under review: `docs/tasks/specs/20261114-told-before-work-t1r-pages-spec.md` (revision 2, with §9 Lead decisions).
Tree: `.claude/worktrees/tbw-t1r`, branch `wip/tbw-t1r`, HEAD `caa4af4` (read only; `git status` clean before and after every run).
One pass, no code edits. `W` = `.claude/worktrees/tbw-t1r/ai-packages/qa-factory`.

**Verdict: NEEDS WORK (fit_with_fixes) — 4 blocking findings (B1-B4), all closable by Lead text edits and one Lead decision
before dispatch; 9 non-blocking fixes (N1-N9); 2 owner questions.**

The design direction (output checks on the page, pre-action checks at the call, one index line per family, data-driven, no
ceiling raise) is sound and fits P31/AR-1/AR-29. What breaks: the card cannot reach its own DoD (A22 ratchets, B1); the family
granularity puts finished-work judges on the call list (B2); the "one data edit back" claim that licenses an owner-away decision
is false as designed (B3); the base of all measurements is 43 commits behind main (B4).

---

## Blocking findings

### B1. The DoD is unreachable for all 12 roles: A22 ratchets are red and the card forbids every raise

- Spec lines: §3 non-goals "any raise of `native_headroom`, `process_ratchet_tokens`, `ratchet_tokens`"; §3.4 key (6) "no raise in
  role-load.json"; §3.4 command 6 runs `test_role_load.py`; P-10 STOPs only on K10. §2.3, §3.3 and the STOP rule never mention A22.
- Carrier evidence (my run, pure read, `audit_factory._a22_findings(W, require_settings=True)` at caa4af4): **every one of the 12
  roles is over `ratchet_tokens`** (e.g. qa-runner ~27,977 tokens vs 16,382; qa-case-critic 22,312 vs 19,846; qa-strategist 20,960
  vs 17,276) **and over `process_ratchet_tokens`** (slack 0; e.g. qa-runner 26,368 vs 14,773; qa-case-designer 15,164 vs 12,423).
  `test_role_load.py:562-566` asserts the shipped process rows are "tight and not exceeded" and `:597-598` asserts
  `_a22_findings(PLUGIN_ROOT, require_settings=True) == []` — both red now.
- After the default, by my count from the measured page bytes (Q4 table) the best case is the runner, −38.8 KB ≈ −9,700 tokens:
  ~18,300 tokens, still over its 16,382 row. Roles with few call-told rows (case-critic, case-designer, strategist: −4.9..−5.2 KB)
  stay ~1,000-2,500 tokens over. So **command 6 stays red for all 12 roles** whatever the STOP list says. The builder has two moves:
  raise (a non-goal) or loop.
- Why this is a plan defect, not just a number: the owner's idea INSERTS output rows into every role's injected text; a shrink-only
  token ratchet measured before T1r (T3a) cannot stay green under it. The AR-20 / SIBLING_MAP axis 18 road for that is a **named
  raise** (row by row, key old → new, reason, in the critic verdict of the merge). Main itself did this in wave 8 (`ae41e2b` "named
  ratchet raises (AR-20)": qa-failure-analyst and qa-doc-scribe rows raised). The plan treats every raise as owner-only and mixes two
  limits of different kinds: `ratchet_tokens` / `process_ratchet_tokens` are COST budgets (`threshold_confirmed_by: null`, info
  only); `native_headroom` (K10) is a RUN-FAILURE ceiling (Codex refuses the role).
- Minimal fix (Lead decision, Lead-closable under AR-20): add to P-10 and §3.4: "A22 `ratchet_tokens` and `process_ratchet_tokens`:
  set every row to the measure after this node's default (lower where it fell, a NAMED raise where it grew), each row listed in the
  report (key, old → new, reason 'told-before-work output rows, tbw'); the critic of the merge names them (axis 18). `native_headroom`
  stays no-raise; K10 alone drives the STOP list." Add A22 green to the acceptance keys, and the A22 numbers to the §2.3 table.

### B2. `call_told_families` at family granularity puts judges of finished work on the call list; F8's "every refusal" is false for `manifest_put`

- Spec lines: §2.2 (f) "a family whose every refusal happens at the call ... no work is lost"; initial list includes `manifest_put`,
  `role_cli`, `execution_request`, `stage_guard`; §3.1 P-3 converts EVERY producer `told` of a listed row; §9 makes only `manifest_put`
  and `role_cli` conditional on N-9; the index line promises "nothing you have written is lost by them".
- FR-38's own check (factory-rules.md:209-214): "for each new check on a role's ARTIFACT, name where the role is told its requirement
  before working". Rows in the list that judge an artifact the role composed (my read of `stage-joints.json`, `field` and requirement):
  - `manifest_put:*` (13 automator rows + `critic_approval` for qa-code-critic): `field` "the manifest fragment sent to
    manifest_put.py" — `obligation_bindings`, `then_remainder`, `expectation_changes`, `assertion_line`, `critic_approval`: this is
    the automator's S5 deliverable and the code-critic's verdict. Pure output judges.
  - `execution_request:no_test`, `selector_args`, `place_rows`, `profile`, `case_entries`: `field` "the `--mine` call and its manifest
    rows" — for qa-automator they judge ITS manifest rows, refused only when somebody runs; for runner/analyst/code-critic they are
    pre-action call checks. One row, two classes, split by ROLE.
  - `execution_request:purpose..instance_contracts` (10 automator rows): judge the `--request` FILE the role wrote (door `--template
    request` exists — a before-work door, so these can stay call-told if the index line names the template).
  - `stage_guard:SG-command.commit.manifest` (manifest unresolved reasons at commit) and `SG-command.delivery` (ledger word of the
    delivery form): judges of finished work met at commit time.
  - `role_cli:*`: every card judges a file the role wrote BEFORE the call (`artifact_producer.py publish` publishes the register /
    cases / bugs; `walk_session.py verdict`; `plan_row.py`). The "nothing you have written is lost" sentence is false for this family.
    It stays FR-38-compliant only by the `--help` pointer told on the page (all 16 scripts contain `epilog(`: my grep below), i.e.
    told before work by a pointer, not by the refusal.
- F8 checked at its carrier: `role_cli.refuse` (role_cli.py:79-104) prints the card when it is CALLED; `manifest_put.py` has 1 `refuse(`
  call and 17 direct `return EXIT_BAD_FRAGMENT` / exit refusals (e.g. :2390-2395 prints its own text for `retract`) — those print
  neither the card nor the row's expected/door, and `manifest_put` is not one of T2's three transports (F18). So for `manifest_put`
  the row sentence reaches the role NOWHERE — not on the page, not at the call — while K2 (P-3) and K5 (P-8) would count it told.
- N-9 is not a measurement: by construction a fragment / input file is written before the call. Leaving it to the builder hands a
  design decision to a weaker model (PROJECT.md «Командная работа» 11), and §3 P-3 does not even carry §9's condition (card and §9
  disagree).
- Minimal fix (Lead text): (1) `manifest_put` off the list — its rows stay on the page (+2.6 KB automator, +0.17 KB code-critic);
  (2) `role_cli` stays on the list with the `--help` clause MANDATORY in its index line, worded as an instruction before writing:
  "run `<script> --help` before you write an input file; it prints what each command checks" (P-1 then only verifies the 16 scripts
  pass `epilog` to the parser); (3) the five manifest-row `execution_request` rows and `SG-command.commit.manifest` stay page-told for
  qa-automator only (split the producer: automator producer keeps its page item, the others take the call item) — this per-producer
  split is already expressible in `told`; (4) drop "nothing you have written is lost by them" from the index line, or keep it only for
  `guard_pre_tool` / `host_adapter` / `stage_guard`; (5) K2/K5 accept a call item only for a row whose refusal is sited on a T2
  transport (not in `told_ratchet.unsited` and not a direct-print site); otherwise the row is `unsited` and K5 does not count it.
  Delete N-9 from §8 and §9's condition.

### B3. "One data edit back" is false as designed — the owner-away licence rests on it

- Spec line: §9 "the owner's 'whole card / whole rule on the page' is one data edit back (`call_told_families`)".
- P-3 REPLACES every producer `told` of a listed row by `[{"call": true}]` (~120 told arrays: 24 PT + 8 SG + 8 HA + 24 ER + 7 RS + 33
  role_cli + manifest_put). Removing a family from the list then turns every such row red in K2 ("a call-told row needs its family in
  call_told_families"), and the page legs are gone from the data. The reversal is: list edit + restore ~120 told arrays + regenerate
  — a git revert of the data, not one edit. PROJECT.md «Что решать самому» allows an owner-away fork to be closed by "the safest
  reversible" option; the claim of reversibility must be true.
- Minimal fix (smaller diff too): keep the existing page item and ADD the call marker on it, e.g. `{"page": true, "call": true}`;
  rule: the call marker is honoured only when the row's family is in `call_told_families`, otherwise the page item stands. Then the
  list really is the one switch (remove a family → its rows return to the page, K2 green), and B2's per-producer split still works.

### B4. All measurements and the merge plan stand on a base 43 commits behind main

- Spec: §0/§2 "Read base ... WIP 705837d"; Gate "on `wip/tbw-t1r` after T1r's WIP, before any merge"; P-0 measures on the branch.
- Carrier: `git log origin/main ^HEAD` = 43 commits; `origin/main` (`ae41e2b`) is not an ancestor of HEAD. Since the merge base main
  changed `references/role-load.json` (wave 8 named raises: qa-failure-analyst 18,426 → 18,769, qa-doc-scribe 17,944 → 17,971, both
  ratchets) and the generated `qa-failure-analyst/handoff-keys.md` and `qa-doc-scribe/handoff-keys.md`. Both are owns of this node.
  Every number in the report and every ratchet row set by P-10 (B1) is stale at the merge, and role-load.json will conflict.
- Minimal fix: new item P-(-1) "merge `origin/main` into `wip/tbw-t1r`; resolve role-load.json by taking main's rows; `--write`; then
  P-0" — measurements are taken on the tree that will merge.

---

## Answers to the eight questions

### 1) Facts (§0 checked at the carrier)

| fact | verdict | evidence |
|---|---|---|
| F1, F2, F3 | true | contract_slices.py:71-89 (`INLINE_SUBJECTS`, "each is injected whole"); inject_context.py:137-179 (`entries_for` ignores kind, `_dropped_headings` never drops an inline subject) |
| F4 | true | role_load.py:296-346, exact formula and red condition |
| F5 | true | role-load.json:38-40 `native_headroom` = {qa-test-strategist: 46008} |
| F6 | true for the 6 K10 roles | the K10 messages of my `--check` run name P=2 / 1 exactly |
| F7, F11, F12 | not re-read (designer cites lines); no contrary evidence met | — |
| **F8** | **partly false** | `refuse` prints the card on every call of `refuse` (role_cli.py:79-104), `RefusingParser.error` uses it (:121-130), `epilog` = `--help` (:64-71) — true; "on every refusal of the command" — false for `manifest_put.py` (1 `refuse(` vs 17 direct exit refusals); COMMANDS_TEXT's "the card is printed whole in every refusal" inherits the error (B2) |
| F9 | not re-read | — |
| F10 | true, number off | the two rows are 750 and 742 chars on runner/automator/strategist pages (not ~820): the saving is ≈ 630 bytes, not 760 |
| F13 | count off (already N-1) | runner page: 22 `- [role_cli:` lines, 13 execution_request, 3 run_suite (my count) |
| F14 | small counts off | automator: exit_gate 4 lines, s5_precheck 11, controller 2 |
| F15 | true | analyst: ER 14, run_suite 1, role_cli 11, validate_artifacts 2 |
| F17 | true | selftest.py:358 `REFERENCE_MD_MAX_BYTES = 12_000`, :396-400 over `slices/**/*.md` |
| "where each call-told family is told on main today" | true for the page | `origin/main` key pages hold no `- [<family>:` row line at all (runner, automator, strategist read); main tells these checks by the site's own refusal and by charter/slice prose only — "nothing told less than main" holds for the page |
| "refusal BEFORE any effect of the call" | true for PT/SG/HA (PreToolUse), `--mine` call checks, run_suite launch checks; false as "before the role's work" for manifest_put, role_cli, the request file, SG commit.manifest/delivery (B2) | stage-joints.json rows and `field`s quoted in B2 |
| missing from §0 | A22 red ×12 on both ratchets (B1); main +43 commits with role-load.json changes (B4) | runs below |

The builder's measured K10/K8 numbers reproduce exactly (my `contract_slices.py --check`, verbatim in the trail).

### 2) Principle fit

- **FR-38 / AR-10:** kept for guard / host / stage-guard shape rules and for call-shape checks (they judge the CALL, not an artifact).
  Broken for the artifact judges listed in B2 unless the fix is applied. `role_cli` keeps FR-38 only by the `--help` pointer told on
  the page before work (B2 (2)).
- **FR-1 / FR-2 / P15:** the index line is honest only for rows whose refusal prints the row (T2 transports, sited). Before T4/T5 the
  guard sites print their own FR-1 text (F18) — main's telling, acceptable — but then the line's "with what they expect and the door"
  is a promise about site text the node does not check, and K5 counts unsited rows told (N5).
- **AR-11 / AR-12:** the expected count of extra refused calls is NOT stated and no measurement is named (N4). It is measurable:
  `refuse` prints `check: <id>` last (role_cli.py:103), so a run's refusals per call-told check id can be counted against main's run.
- **P27 / AR-29:** kept — family membership is data, J1 judges it; no meaning check moves into code.
- **Is any family a judge of finished work?** Yes: `manifest_put` wholly; parts of `execution_request` (for the automator), of
  `stage_guard` (commit.manifest, delivery) and every `role_cli` card (mitigated by `--help`). B2.
- **F-2 sub-question in §9:** the safe DIRECTION (stay on the page when in doubt) is right, but (a) the criterion is not measurable,
  (b) the card does not carry it, (c) `execution_request` and `stage_guard` of the same class are missing from it. Decide it now (B2).

### 3) Feasibility for a weaker model

Edges silent or contradictory:
- E1. `role_cli` rows carry `requirement_from: role-commands.json`, no `requirement` (39 such rows in the file). P-3/`_told_leg`
  "states a requirement" is undefined for them; a literal builder turns all 33 red or drops them. Define: "a non-empty `requirement`,
  or a `requirement_from` that resolves to a card with `input` or `verify`".
- E2. §3 P-3 (unconditional list) vs §9 (manifest_put/role_cli conditional on N-9): contradiction (B2).
- E3. The AR-13 change check "grep `12_000\|12000` over `scripts/*.py` finds one literal" already finds six lines (context_bundle.py:14,
  driver_gates.py:152, driver_timing.py:36 `120000`, judge_run.py:72 `512_000`, runtime_policy.py:3, selftest.py:20/358). Replace by
  "the cap is defined once: grep `REFERENCE_MD_MAX_BYTES\s*=|SLICE_MAX_BYTES\s*=` finds one definition".
- E4. P-10 "add every continuation line K8 or `--limits` asks for": `--limits` never names a continuation line (its door is "move the
  section to the roles that act on it" — wrong for a key page). Only K8's `size_finding` names the line, at 80 % of L. A page under W but
  over 12,000 bytes gets no door. Either P-5 makes `size_finding` fire at the cap with the continuation door, or F-10 (b) now (Q5).
- E5. A22 absent (B1). E6. Base staleness absent (B4).
- "Builder measures" items that are really design decisions: **N-9** (B2 — definitional); **N-3** decides the STOP list but the list's
  consequence (who decides, which node next) is outside the card — acceptable as a measure. N-1, N-2, N-4, N-5, N-6, N-7, N-8, N-10 are
  real measurements. N-5 is already answered: all 16 command scripts contain `epilog(` (my grep below; whether each passes it to the
  parser stays P-1's check).
- **STOP-per-role and the branch:** with B1 unfixed the node can never be DONE (command 6 red), not merely "STOP for two roles". With
  B1 fixed, the node can finish and hand back a STOP list; the branch is then **not permanently red but blocked on an unopened node**:
  the strategist's STOP is certain, not an estimate (its baseline 46,008 is its pre-T1r share; after the default its U' ≈ 55,200;
  even with every output row removed from its page it would sit ≈ 45,700) and the automator's is near-certain (≈ +3,000; ≈ +5,600
  with B2's manifest rows on the page). To unblock, the Lead must (i) take B1's named A22 raise, (ii) open the F-2 (c) prose-removal
  node for qa-automator and qa-test-strategist NOW, in parallel (its owns — charters and slice SOURCES — do not overlap this card's
  generated slices except through `--write`), sized at ≥ 9.2 KB strategist and ≥ 5.6 KB automator; and the owner answers F-2 (d)/(a)
  only if (c) cannot reach that.

### 4) Numbers

Measured page bytes per family (my pure read of `references/slices/*/handoff-keys.md`, script in the trail). Estimate
`U' = U − call-family bytes + 150 × families − 630 + 450 × extra pages`, with the plan's list as written:

| role | U | call-family bytes on page | U' (mine) | plan's U' | H / baseline | verdict |
|---|---|---|---|---|---|---|
| qa-runner | 90,414 | 38,825 | ≈ 52,300 (2 pages) | 54,500 | 68,400 | green |
| qa-failure-analyst | 86,333 | 26,654 | ≈ 60,400 (2 pages) | 61,600 | 68,400 | green |
| qa-code-critic | 83,044 | 16,262 | ≈ 67,100 (page ≈ 11,900 B, 1 page) | 68,400 ± 2,000 | 68,400 | green by ≈ 1,300 |
| qa-automator | 95,217 | 24,507 | ≈ 71,400 (2 pages) | 69,500 | 68,400 | **STOP ≈ +3,000** (≈ +5,600 with B2) |
| qa-test-strategist | 60,744 | 5,224 | ≈ 55,200 | 52,000 | 46,008 | **STOP ≈ +9,200** (certain) |
| qa-requirements-tester | 47,004 | 9,935 | ≈ 36,900 | 42,000-46,000 "edge" | 42,400 | green by ≈ 5,500 |

Conclusion "runner and analyst green, automator/strategist stop" is plausible and holds by my count; the plan underestimates both STOP
gaps and overestimates requirements-tester. Note: with B2 (2)-(3) applied, code-critic keeps ≈ 2,100 B of manifest-row ER rows on its
page only if the split is by row, not by producer — the per-producer split keeps code-critic green.

What the formula omits: (1) A22 entirely (B1 — the biggest omission); (2) rows that stay on the page as b2 pointers if a family leaves
the list (≈ 230 B each); (3) the digest saving is ≈ 630, not 760; (4) the `--help` clause bytes of the role_cli index line.

Cheaper levers the plan misses or underrates:
- **Doors on the page for output rows** (`Door: …` segments): automator 2,489 B, strategist 1,922 B, code-critic 1,502 B (measured).
  FR-38 asks for the requirement before work; the door belongs to the refusal (FR-1), which T2 prints for sited rows. Dropping the door
  from the page for SITED output rows is a renderer change of the same kind as the index line, no prose edit.
- **Another contract's rows on every page:** `handoff_check:null_outcome.*` (6 rows, 658 B) render on all 12 pages — the strategist,
  case-critic and automator pages included (triage rows, run report readable). Scope them to the contracts that have a null outcome.
- Duplicate tellings beyond the digest: the 10 `execution_request` validate rows share one door (≈ 750 B automator) — moot when
  call-told.
None of these closes the strategist; door-drop plus null_outcome scoping (≈ 3,100 B) nearly closes the automator's +3,000.

### 5) The two size limits (F-10)

"(a) now, (b) later" is coherent only if (b) lands before T1r-cards. (a) adds pages (+≈ 450 B of U each, to roles already at STOP),
continuation lines in inject-map.json, and T1r-cards re-points role-rules to `handoff-keys-<n>.md` (§4). When (b) lands the pages
re-merge: the continuation lines go (else `NONE_CONTINUED` pages), role-rules pointers re-point again, and every process-ratchet row
must be re-edited (slack 0 is red both ways). F-10 (b)'s premise is true on the carrier (F2: an inline page is injected whole however
split; K8's L is the per-file run danger). Recommendation (Lead-closable, a dev-time proxy): do (b) in THIS node — `selftest.py` is
already in owns — with its four-questions block in the commit, and drop the min(W, cap) partition; with (b) every page fits under W
after the default (largest ≈ 17 KB automator), so no continuation lines are needed at all.

### 6) Order and deadlock (B4 of t-703)

The node order T1r → T1r-pages → merge → T1r-cards has no node waiting on a later node: B4 of t-703 is resolved. But (a) the merge waits
on the F-2 (c) node, which is not opened (Q3), and (b) on main's 43 commits (B4 here). §4 is incomplete — T1r-cards must also:
(1) measure its growth against A22 room as well as K10 room (B1); (2) know that new rows in a listed family default to the call item
(or not — the rule must be stated: a new PT row with only a page item renders on the page); (3) drop its role-rules re-pointing if F-10
(b) lands (Q5); (4) honour the per-producer split of B2 (3) when it appends to `execution_request` rows; (5) note SIBLING_MAP axis 28 —
`s5_precheck:row_fields` on the automator page spells the `tests[]` row fields, a fourth render site that axis 28 calls a defect (T1r's
row, not this node's: queue to T1r-cards).

### 7) Siblings by the map, the artifact sweep, the four questions for `call_told_families`

Map walk (only the relevant axes; every other axis n/a — this node touches no host, journal, path resolver or test identity):
- Axis 18 (shrink-only ratchets): `process_ratchet_tokens` is a member; a raise is named row by row — B1. `told_ratchet.unsited` and
  `judgment-census.json` (P-6) are members too: P-6's census narrowing must be named in the merge verdict.
- Axis 32 (where judgment lives): P-6 changes census `roles`/`note`; the commit's `judgment:` line says "none moved" — consistent (a label
  narrowing is not a move), but the census cross-check of `architecture_gate` will see the diff; the report should cite it.
- Axis 34 (one road): kept — one data list for all roles, no language/project branch.
- Axis 17 (detector verdict shape): the call transports are T2's three; `manifest_put` is outside them (B2).
- Axis 28: sibling observation queued (Q6 (5)).
Artifact sweep of §2.2 (f)'s list, per family: `guard_pre_tool` applied (call-shape / permission; PT-plan-rewrite, PT-manifest-shrink,
PT-artifact-rewrite refuse a whole-file Write — composed content is not saved, so the "nothing lost" clause is doubtful there too);
`stage_guard` applied except commit.manifest / delivery (B2); `host_adapter` applied; `execution_request` split (B2); `run_suite` applied
(launch/recover checks; `missing_executor` hands to the person, fine); `manifest_put` not applicable (output, B2); `role_cli` applied
only with the mandatory `--help` instruction (B2).

Four questions — the spec has none for this mechanism (a new data key + a K2 rule + a K5 count is a mechanism; CLAUDE.md rule 10):
(a) cost: each role pays one refused turn per call-told rule first broken — unstated, unmeasured (N4); (b) axes: no per-axis
enumeration in the spec (N6); (c) detector: none registered for "an output check put on the call list" or "a call-told row whose refusal
does not print it" — propose `test_stage_joints` rows (B2 (5)) plus a live-runs measurement of refusals per call-told id; (d) what stops
a skip: `stage_joints.py --check` K2 in selftest (code on the path for shape); membership meaning by the critic only — say so explicitly.

### 8) Whose forks; is "safest reversible" true

- OWNER (intent): F-1 and F-2 — they decide what "told before work" means for the owner's own idea (is a refusal at the call or a
  `--help` pointer "told before work"?). Closing them by recommendation is legal under the owner-away paragraph only for a reversible
  option: true after B3's fix, false as written. F-2's residual options (a) and (d) are owner's; (c) is Lead-closable (a designer pass
  on prose with critic, FR-33 live proof afterwards).
- Lead: F-3, F-4, F-5, F-6, F-7, F-8, F-9, F-10 — agreed; F-10 (b) can be done now (Q5). B1's named A22 raise is the Lead's under AR-20.
- "Nothing told less than main": true for the page (main has no row lines). "No raise of any ceiling": keep for K10; wrong for A22 (B1).

---

## Non-blocking fixes (text the Lead can apply)

- N1. §0 F8: "prints the card on every call of `refuse`; `manifest_put.py` refuses 17 times by direct print"; F10: 750 chars, saving 630.
- N2. E1 definition of "states a requirement" for `requirement_from` rows (P-3, `_told_leg`).
- N3. E3 AR-13 grep replaced by the definition grep.
- N4. AR-12: add to the report a measured line "call-told rows per role, and the expected first-meet refusals (one per family a role
  calls)"; add a `live-runs` row: count refusals per call-told check id (`check:` line of `refuse`, the `block`/`deny` record) against
  main's run of the same story.
- N5. K5 (P-8) counts a call-told row only when its refusal is sited on a T2 transport; unsited rows stay in `told_ratchet.unsited` and
  out of K5's told count.
- N6. Add the four-questions block for `call_told_families` with one line per SIBLING_MAP axis (rule 10 (b)).
- N7. E4: K8's `size_finding` names the continuation line at the cap too — or F-10 (b) now.
- N8. §2.3: mark the strategist's STOP as certain (≥ 9.2 KB) and open the F-2 (c) node in parallel, with its size target.
- N9. Index-line wording per family (B2 (4)); role_cli line: "run `<script> --help` before you write an input file".

## Questions for the owner (plain words)

1. **Is "you learn the rule when the factory refuses your step" good enough for rules about HOW a role uses its tools** (no git config
   changes, tests only through run_suite, Codex call shapes), as long as the role's page says such rules exist? Rules about the role's
   finished work (its manifest, its published cases and bugs, its plan) stay on the page in every case. The Lead took "yes" for tonight;
   it can be undone by removing one list entry.
2. **For the commands a role feeds a file to, is "read the command's `--help` before you write the file" enough**, instead of the full
   card on every start (about 24,000 characters for the runner)? `--help` prints the same card.

---

## Trail

Read: the plan whole; role_cli.py 1-180; factory-rules.md FR-1 (32-36), FR-38 (209-214); selftest.py 355-405; role_load.py 296-346;
contract_slices.py 68-92 and its `--check`/`--write` lines; inject_context.py 137-180; role-load.json whole; stage-joints.json (all 118
rows of the seven listed families: check, stages, roles, told, door, requirement/requirement_from, field of samples); key pages of the
automator (non-row lines, handoff_check rows), and family byte counts of all 12 pages; `origin/main` key pages of automator, runner,
strategist; manifest_put.py 2370-2400 and its exit sites; SIBLING_MAP axes 18, 28, 31, 32, 34 and the axis list; the previous plan
verdict B1/B4 lines; critic_verdict.schema.json.

Not read (cited only): parent and dispatch specs, the T1r and T3a reports, F7/F9/F11/F12 carriers, guard_pre_tool order (N-6).

Runs (all read-only; `git -C <tree> status --short` empty before and after):
1. `python -B W/scripts/contract_slices.py --check` → 4 SLICE K8 (automator 41365, code-critic 27878, analyst 38751, runner 53086 chars),
   6 SLICE K10 (requirements-tester 47,004 / 42,400; strategist 60,744 / 42,400 baseline 46,008; automator 95,217 / 68,400; code-critic
   83,044 / 68,400; runner 90,414 / 68,400; analyst 86,333 / 68,400), 5 WARN K8 (bug-reporter 21498, doc-scribe 21107,
   requirements-tester 23205, scout 21174, strategist 22771). Matches the builder's numbers exactly.
2. Pure read `audit_factory._a22_findings(W, require_settings=True)` → 24 ratchet_tokens lines (12 roles × first/repair, all over) and
   12 process-ratchet lines (all over), e.g. "qa-runner (first) starts with ~27,977 tokens, over its shrink-only ratchet 16,382";
   "qa-runner carries 26,368 process tokens, over its shrink-only process ratchet 14,773".
3. Pure-read byte count per family of every `handoff-keys*.md` (regex `^- \[(\w+):`, `len(line.encode())+1`): call-family bytes runner
   38,825 / analyst 26,654 / automator 24,507 / code-critic 16,262 / requirements-tester 9,935 / strategist 5,224; door segments of output
   rows automator 2,489 / strategist 1,922; `null_outcome` rows 658 on every listed page.
4. `grep 'epilog('` over the 16 scripts of role-commands.json → present in all 16 (positive: role_cli.py itself defines it).
5. `grep -c 'refuse('` / direct exit returns: manifest_put 1 / 17; walk_session 8 / 0; manual_evidence 14 / 0; artifact_producer 3 / 0;
   first_look 3 / 0.
6. `git log origin/main ^HEAD | wc -l` → 43; `merge-base --is-ancestor origin/main HEAD` → not ancestor; diff since merge base on
   role-load.json: analyst and doc-scribe rows raised in both ratchets.
7. `grep -n '12_000\|12000' W/scripts/*.py` → six hits (E3).
8. `origin/main` key pages: `grep -o '^- \[[a-z_]*:'` → no row lines on automator, runner, strategist pages (positive control: the same
   grep on the branch pages counted the families above).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 DoD unreachable: audit A22 is red for all 12 roles on ratchet_tokens and process_ratchet_tokens at caa4af4 (test_role_load.py:562-566, 597-598 assert green) and stays red after the default by measured page bytes; the card forbids every raise and STOPs only on K10. Fix: named A22 raise row by row per AR-20 / axis 18 (Lead), native_headroom stays no-raise; A22 green in the acceptance keys",
    "B2 call_told_families at family granularity puts finished-work judges on the call list: manifest_put (automator deliverable, 17 direct-print refusals that print neither card nor row), execution_request manifest-row rules for the automator, SG-command.commit.manifest / delivery; role_cli FR-38-compliant only by a mandatory --help instruction; N-9 is definitional, not a measure, and section 3 P-3 does not carry the section 9 condition. Fix: manifest_put off the list, per-producer split for the automator, mandatory --help clause, call item counted only when sited",
    "B3 one data edit back is false: P-3 replaces about 120 told arrays by the call item, so removing a family turns K2 red and the page legs are gone. Fix: keep the page item and add the call marker, honoured only when the family is listed",
    "B4 base 43 commits behind origin/main, which changed role-load.json (wave 8 named raises) and two generated key pages in this node's owns. Fix: merge origin/main into wip/tbw-t1r before P-0"
  ],
  "fixes": [
    "P-10 and section 3.4: set A22 rows to the measure after the default, named raises listed in the report; A22 green as an acceptance key",
    "Remove manifest_put from call_told_families; split execution_request no_test/selector_args/place_rows/profile/case_entries and SG-command.commit.manifest so the automator producer stays page-told",
    "role_cli index line: run <script> --help before you write an input file; drop nothing-you-have-written-is-lost except for guard families",
    "Call marker added beside the page item; honoured only when the family is listed; K2 and K5 count a call item only for a sited row",
    "New item P-(-1): merge origin/main, take main's role-load.json rows, --write, then measure",
    "Define states-a-requirement for requirement_from rows; replace the 12000 grep by a definition grep; K8 size_finding names the continuation at the cap or do F-10 (b) now",
    "State the strategist STOP as certain (at least 9.2 KB) and open the F-2 (c) node now in parallel; add the four-questions block with an axis enumeration for call_told_families; add the refusal-count measurement for AR-12",
    "Consider the cheaper levers: drop Door segments of sited output rows from the page; scope handoff_check null_outcome rows to contracts with a null outcome",
    "Section 4: T1r-cards measures A22 room too, states the default told item for new rows of listed families, and takes the axis 28 row_fields observation"
  ],
  "class_completeness": "Map walked on axes 17, 18, 28, 32, 34 (others n/a: no host, journal, path, test identity touched). Axis 18: process_ratchet_tokens, told_ratchet.unsited and the judgment census are members, raises named row by row (B1). Artifact sweep of the seven listed families done with a verdict each (section 7); same-class rows missing from the F-2 sub-question: execution_request and stage_guard (B2). Axis 28 sibling (s5_precheck:row_fields as a fourth render site) queued to T1r-cards.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-told-before-work-t1r-pages-spec.md",
      "docs/tasks/specs/reviews/20261114-tbw-t1r-cards-plan-critic.md (B1, B4 lines)",
      "W/scripts/role_cli.py 1-180",
      "W/design/factory-rules.md FR-1, FR-38",
      "W/scripts/selftest.py 355-405",
      "W/scripts/role_load.py 296-346",
      "W/scripts/contract_slices.py 68-92",
      "W/scripts/inject_context.py 137-180",
      "W/scripts/manifest_put.py 2370-2400 and exit sites",
      "W/references/role-load.json",
      "W/references/stage-joints.json rows of the seven listed families",
      "W/references/slices/*/handoff-keys.md",
      "origin/main key pages of automator, runner, strategist",
      "W/scripts/tests/test_role_load.py 527-598",
      "docs/SIBLING_MAP.md axes 18, 28, 31, 32, 34",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B W/scripts/contract_slices.py --check", "result": "4 SLICE K8, 6 SLICE K10 with the builder's exact numbers, 5 WARN K8"},
      {"command": "pure read audit_factory._a22_findings(W, require_settings=True)", "result": "all 12 roles over ratchet_tokens (first and repair) and over process_ratchet_tokens"},
      {"command": "pure-read byte count per family of handoff-keys pages", "result": "call-family bytes runner 38825, analyst 26654, automator 24507, code-critic 16262, req-tester 9935, strategist 5224"},
      {"command": "grep epilog( over the 16 command scripts; grep -c refuse( and direct exits", "result": "epilog in 16 of 16; manifest_put 1 refuse vs 17 direct exits"},
      {"command": "git log origin/main ^HEAD; diff since merge base on role-load.json", "result": "43 commits; analyst and doc-scribe ratchet rows raised on main"}
    ]
  }
}
```
