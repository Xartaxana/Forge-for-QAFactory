# Told before work: node T1r-sites — site the refusals of `execution_request` and `run_suite` so their rows can be told at the call (draft, designer, t-737)

Status: DRAFT for Lead acceptance. Forks are in §6, each with a recommendation the node can be run on while the owner is away. Nothing
in this draft raises H, `native_headroom`, the 12,000-byte cap or any ceiling, and nothing trims a requirement sentence.

**The headline, measured against the brief's goal (§3):** siting these two families is NECESSARY, but it is ENOUGH for one of the three
STOP roles only. By arithmetic on the T1r-pages report's measured numbers: qa-code-critic comes under H by about 530 bytes (an edge; the
builder's measure decides); qa-automator falls by about 7,300 bytes and stays about 8,600 over H; qa-test-strategist holds NO row of either
family and is not moved at all (it is 9,716 over its baseline, 13,324 over H). Even putting every OUTPUT family on the call list — which
FR-38 forbids (plan critic B2, Lead §10(1)) — would not close the automator or the strategist (§3.4). The rest is F-1.

Parents: T1r-pages spec `C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-t1r-pages-spec.md` ("pages", §10 binding);
its report `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-t1r-pages-report.md` ("report"); T2 spec
`C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-t1r-t2-dispatch-spec.md` ("T2"); the mechanism spec
`C:\QAFactory\forge-repo\docs\tasks\specs\20261113-told-before-work-mechanism-spec.md` ("mechanism", node table §5.1, rows §5.4); the plan
critic `C:\QAFactory\forge-repo\docs\tasks\specs\reviews\20261114-tbw-t1r-pages-plan-critic.md` ("critic").
Read base: worktree `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r` (`W` = its `ai-packages\qa-factory`), working tree as read on
14.11.2026. **The worktree was being edited while I read it**: `stage_joints.py` moved by about 20 lines between two reads (`call_told`
first at :731, then at :751; `call_index_wording` appeared as data — the report's Question 3 is being done). Line numbers below are of the
second read; the builder cites functions, not lines.

---

## §0 Facts read on the carrier (load-bearing)

| # | fact | carrier |
|---|---|---|
| S1 | "Sited" = the row's check id is in `sited_ids(...)` = keys of the v1-derived universe (exit / detector / window members) ∪ `refusal_registry.check_of(e)` for every A24 `REGISTRY` entry ∪ every literal id the wide scanner reads from a `refusal(...)` / `with_check(...)` call bound to `detector_verdict` (`check_ids`) ∪ `role_cli:<key>` for every command | `W\scripts\stage_joints.py` `check_ids` 290-317, `sited_ids` 320-336 |
| S2 | `_is_sited(key, sited)`: in the set, OR a sub-id `<id>.<part>` of a sited id. So `execution_request:stand.probe` and `execution_request:stand.reference` count as sited as soon as `execution_request:stand` is, with no site of their own | `stage_joints.py` 339-341 |
| S3 | `call_told(row, role, families, sited)` is THE decision: family listed (and worded), row states a requirement, EVERY producer entry naming the role carries the call marker, and `_is_sited(check, real_sited())`. Any doubt = False = the row stays on the page | `stage_joints.py` 751-766; `call_families` 723-728 (a listed family with no wording is dropped) |
| S4 | `_call_leg` (K2): silent while the family is not listed; with it listed, a marker on a row with no requirement or no site is red ("has no site in code ... the page item stands") | `stage_joints.py` 769-780 and following |
| S5 | `check_ids` reads only files whose text names `detector_verdict` and `refusal(` or `with_check(` (a text pre-filter); the scanner binds the call through the file's import of `detector_verdict` (T2-8: inside a transport or not) | `stage_joints.py` 303-307; T2 lines 239, 248 |
| S6 | No literal `execution_request:` or `run_suite:` id is written anywhere in `W\scripts\*.py` (positive control of the same Grep: it finds `run_suite: this story is inside stage` at `run_suite.py:1376` and the test literals) | Grep `execution_request:|run_suite:` over `W\scripts\*.py` |
| S7 | No A24 `REGISTRY` entry names `execution_request.py`; the universe holds no `execution_request:`/`run_suite:` id (the T1r report counts all 24 + 7 rows unsited) | Grep `execution_request` in `refusal_registry.py` (hits only prose at 339, 593, 620); T1r report §2 line 14 |
| S8 | The T1r report names the siting node per group: "execution_request 24 -> T5 (validate_request rows) and T5b (the `--mine` rows); ... run_suite 7 -> T5" | `...\reports\20261114-t1r-report.md:14` |
| S9 | Mechanism node T5 owns `s5_precheck.py`, `execution_request.validate_request`, `manifest_put.py`, `run_suite.py` (`_refuse_phantom_story`, `resolve_detail_target`, `refuse_untyped_story_run`, `refuse_missing_executor`, the `invalid_*` prints); T5b owns the `MineRefusal` sites; both depend on T2 + T1r. T2's non-goal: "relabelling any refusal site to call `refusal()` (T4/T5/T7)" | mechanism 396-397; T2 line 221 |
| S10 | `refusal(check, problem)` returns a `Record` whose `str()` is the problem ONLY, with `check`, `expected` (= `told_text(row)`), `door`; an unreadable row gives `expected` = "(the factory's requirement row <id> could not be read: ...; this is a factory defect)", never an exception. `spoken(record)` = problem + `  expected:` + `  door:` + `  check:` lines | `W\scripts\detector_verdict.py` 148-191 |
| S11 | `validate_request` collects `errors` (plain strings) and raises ONE `RequestError("; ".join(errors))` | `W\scripts\execution_request.py` 115-355 |
| S12 | `run_suite.py` prints these refusals as ONE JSON line, never through a T2 sink (`block`/`deny`/`refuse`/`run_guarded`): `{"status": "invalid_request", "error": str(exc)}` on STDERR (`main` 2921-2923, `_refuse_phantom_story` 970, `resolve_detail_target` 1116), `{"status": "mine_refused", ...}` on STDOUT (2082, 3107), `invalid_recovery` (2836), `run_refused` (2881, 2912, 2945), `WindowFirst` payload (2078); `refuse_untyped_story_run` refuses through `ap.error` (1416); `refuse_missing_executor` prints a person question, exit 3 (1552-) | `W\scripts\run_suite.py` |
| S13 | A reader of that JSON: `red_sandbox.py` takes the LAST stderr line starting with `{` and accepts it only with `error` present and `execution_status` absent | `W\scripts\red_sandbox.py` 1271-1283 |
| S14 | Every ER/RS refusal comes before a launch: `validate_request` runs before the runtime probe, `store.begin`, the budget answer and the stand lease ("an answered or refused request leaves nothing behind", 2924-2927; "before a store, a key, a probe, a budget answer or a stand lease", 2873-2875); `WindowFirst`: "Nothing was launched, so no idempotency key is spent" (2076-2077); `run_suite:begin` refusals are `JobStore.begin` (execution_request.py 412-438) before any launch | `run_suite.py` 2866-2923, 2075-2084; `execution_request.py` 412-454 |
| S15 | `--template request` prints every field of a RunRequest and where its value comes from, runs nothing: a door BEFORE the request file is written | `run_suite.py` 14, 2470-2545, 2745, 2793 |
| S16 | Data today: `call_told_families` lists `execution_request` and `run_suite`; their wording is "{n} checks of your commands are told in the refusal of the call, with what they expect and the door." (no `--template request` clause, which pages §10(3) makes a CONDITION for the request-file rows); every ER/RS producer has `told: [{"page": true}]` (no call marker) | `W\references\stage-joints.json` 8057-8072; rows 3131-3400, 3752-3857, 6187-6720 |
| S17 | Producers: the 10 request rows (`purpose`…`instance_contracts`) and 4 RS rows (`phantom_story`, `detail_target`, `untyped_story_run`, `missing_executor`) name qa-automator only; the 13 `--mine` rows name automator, runner, code-critic, analyst (one entry each); `sandbox` names code-critic, analyst; `run_suite:recover` runner, automator, code-critic; `run_suite:begin` automator, runner, analyst, code-critic; `run_suite:reparse` runner | `stage-joints.json` same lines |
| S18 | K10: red when `U > H` AND `U > native_headroom.<role>` (when set). So the strategist is green at `U <= 46,008`, not only at `U <= 42,400` | `W\scripts\role_load.py` 336-339 |
| S19 | `told_ratchet.unsited` is a ceiling: a measured count BELOW it is green (only `hand_cards` is dense) | `stage_joints.py` 1124, 1129-1152 |
| S20 | Keep test files: `test_execution_request.py` (gate_named; covers `execution_request.py` AND `run_suite.py`; 20.9 s), `test_stage_joints.py` (67.6 s by `slow_tests.json`; the report ran it about 180 s), `test_contract_slices.py`, `test_detector_verdict.py`. `test_run_suite_mine.py` is QUARANTINED (never edited, never a witness) | `W\scripts\tests\test-layers.json` 852, 1250, 1499-1518, 5374, 9662; `W\scripts\slow_tests.json` 36, 125 |
| S21 | A continuation page costs about 400 bytes of fixed text (generated comment, `## ... (continued from handoff-keys.md)` heading, the `<T>/<ID>/<home>` sentence) | `W\references\slices\qa-code-critic\handoff-keys-2.md` 1-5 |

**Correction to the brief.** "qa-test-strategist +9,716" is the gap over its BASELINE 46,008 (the K10 green line, S18); over H (42,400) it is
+13,324. The report's line "gap +9,716 over H" (report §5) is a slip of the report; its table (U 55,724, H 42,400) is right.

---

## §1 Architecture invariants, owners, census class (designer rule 1, AR-29, P27)

| AR | how this node keeps it | change check written into the DoD |
|---|---|---|
| AR-9 a refusal names what it expected and a door its receiver can use | every relabelled ER/RS refusal carries the row's `expected` and `door` next to its unchanged `error` | `T1rs/told/<id>` rows (S-1) |
| AR-10 a check's requirement reaches the role before the work | output judges stay on the page (the five manifest-row ER rows for qa-automator, B2 (3)); call checks are told by the refusal, and the page keeps one index line per family that names the before-work door `--template request` (pages §10(3)) | `T1rs/index-line/*`, `T1rs/partial-family/qa-automator` (S-2) |
| AR-11 / AR-12 context and cost | the page loses the ER/RS call-check rows of four roles (§3) | K10 before/after measured in the S-2 report |
| AR-13 one reader / composer | the sentence comes only from `refusal()` -> `told_text(row)`; the JSON projection of a Record is ONE new helper `detector_verdict.told_fields`, next to `spoken` | grep in the S-1 report: `told_fields(` is the only builder of the `told` key |
| AR-15 one survivor | `refusal()` is the one constructor; no second sentence table | review |
| AR-18 one output shape | the JSON refusals of `run_suite.py` keep their shape; one additive key `told` (F-2); `error` byte-identical | `T1rs/error-bytes/<channel>` (S-1) |
| AR-16 one question form | `refuse_missing_executor`'s person question text is untouched; the `told` key sits beside it, never inside the question | `T1rs/error-bytes/missing_executor` (S-1) |
| AR-20 shrink-only ratchets | `told_ratchet.unsited` 150 -> the measure (expected 119); A22 rows of the four touched roles set to the measure (lowered); `native_headroom` untouched | ratchet rows in the S-2 report, named |
| AR-22 field producer/reader | `told` has a reader: the role (it is printed to it) and the tests; `records` on `RequestError` has one reader: `told_fields` | `T1rs/told/<id>` |
| AR-28 an unknown never a pass | a row that cannot be read gives the factory-defect sentence; exit code and `error` unchanged | `T1rs/unreadable-row` (S-1) |
| AR-29 code judges data | the node moves no meaning into code: sites write a literal id; which rows go to the call is data (`call_told_families` + markers), judged by J1 | critic question 11 |
| AR-1 closed variety in data | the index words of both families stay in `call_index_wording` (data) | `_shape_problems` (existing) |

Checks this node adds or alters — owner served and census class:

| check / function | change | owner it serves | census class |
|---|---|---|---|
| `execution_request.validate_request` | each append becomes `refusal("<id>", <same text>)`; the raise carries `records` | data (the row's words travel with the refusal) | existing census unit (if any), meaning unchanged; no new unit |
| `MineRefusal` sites (functions listed in §4.1 S-1 table) | `raise MineRefusal(refusal("<id>", <same text>))` | data | existing units unchanged; no new unit |
| `JobStore.begin` / `JobStore.recover` / `JobStore.read` | same, ids `run_suite:begin` / `run_suite:recover` | data | existing units unchanged |
| `run_suite.py` refusal printers (§0 S12) | add `**told_fields(<exc or record>)` to the printed dict / `spoken(...)` to the `ap.error` message | data (transport) | renderer, no unit |
| `detector_verdict.told_fields` (new) | the JSON projection of Records | data | renderer, not a unit (`told_fields` does not match `UNIT_NAME_RE`'s judge names: builder confirms with `test_judgment_census.py`) |
| `stage_joints.call_told` (unchanged code, new inputs) | now meets sited ER/RS rows with call markers | data (join row <-> closed list <-> site) | existing |

Judgment: none moved into code. Whether a refusal at the call is "told before work" for a call check is the owner's F-2 of the pages spec,
taken by recommendation (pages §9); which rows judge finished work (stay page-told) is the Lead's §10(3), applied here as written.

One road (P31, axis 34): one rule for every role — a call check is told by its refusal plus an index line, an output judge on the page —
read from data (producer entries and the family list), never from a role name in code. The per-role producer split of the five manifest-row
rows is a data difference of the check's CLASS for that role (it judges the automator's own manifest rows), not a road for one role.

---

## §2 Answers to the brief's questions

### Q1 What "sited" means, what is missing, who carries it

- Meaning: S1/S2. In practice for these two families: a literal `refusal("execution_request:<x>", ...)` (or `with_check(..., "<id>")`) call in
  a file that imports `detector_verdict` (S5). No universe, A24 or role_cli road applies (S7).
- Missing, per family, three things:
  1. **The refusal site in code** (all 31 rows): no literal id exists (S6). Sites: `validate_request` (10 request rows), the `MineRefusal`
     raisers (13 `--mine` rows + `sandbox`), `JobStore.begin/recover/read` (2 RS rows), four `run_suite.py` refusers (4 RS rows),
     `reparse_run_block` (1 RS row). Full map: §4.1 S-1 table.
  2. **The transport**: `run_suite.py` prints its refusals as JSON lines, not through a T2 sink (S12). Siting alone makes the scanner count
     the row sited (S5, T2-8 "inside a transport or not") while the role would still read only `error` — the row would be counted told at
     the call and told NOWHERE. So the node also adds the `told` key to every printer of a relabelled refusal (F-2). This is the part T2
     did not do and the pages spec §10(5) assumed ("sited on a T2 transport").
  3. **The producer entries**: every ER/RS page item gains `"call": true` (pages §10 B3 form), and the five manifest-row rows
     (`no_test`, `selector_args`, `place_rows`, `profile`, `case_entries`) split into two producer entries: qa-automator keeps
     `{"page": true}`, runner/code-critic/analyst take `{"page": true, "call": true}` (pages §10(3)). Plus the ER wording gains the
     `--template request` clause (S16; condition of §10(3)).
- Carrier: NOT the T2 spec (its non-goal excludes relabelling, S9). The carriers are mechanism nodes **T5** (its `validate_request` and
  `run_suite.py` parts) and **T5b** (whole), whose rows already landed (T1r). This node is T5(ER+RS part) ∪ T5b ∪ the JSON transport.
  T5 keeps `s5_precheck.py` and `manifest_put.py` (output families: siting them changes no page byte). Mechanism T5's test line "a test
  row per family 'the automator's page names it'" is superseded for ER/RS by call telling (F-8).

### Q2 Per-role arithmetic — §3.

### Q3 FR-38 direction per family — fork F-3 (§6), table in §3.3.

### Q4 Edges — §5 (E1-E3 answer the three named edges).

### Q5 Tests, witness, census, AR, axes — §4 (rows), §1 (AR, census), §7 (axes).

---

## §3 The arithmetic (bytes; per role)

Inputs: report §2 (U, H, page bytes) and §3 (page CHARACTERS per family, measured by the T1r-pages builder). Characters stand for bytes of
row text: the pages differ by 4 bytes or less per page (report §2), so the error is under 50 bytes per role. Where a number is mine it says
"est.". I had no shell in this pass: every est. is replaced by the S-2 builder's measure (S-2 item P-0 / P-6).

Index-line cost after this node (est.): `- [execution_request:*] ` + the new wording of §4.2 S-2 P-2 ≈ 226 bytes; `- [run_suite:*] ` + the
existing wording ≈ 117 bytes; with newlines ≈ 345 per role holding both.

### §3.1 qa-code-critic — under H by an edge

| term | bytes |
|---|---|
| U now (report §2) | 74,327 |
| H (P = 1) | 68,400 |
| gap | +5,927 |
| `execution_request` rows leaving (14 rows: 13 `--mine` + `sandbox`; all call checks for this role) | −6,017 |
| `run_suite` rows leaving (`recover`, `begin`) | −773 |
| two index lines | +345 (est.) |
| pages: 11,835 + 7,337 = 19,172 -> ≈ 12,727; still over the 12,000 cap -> still 2 pages | 0 |
| **U' (est.)** | **≈ 67,882 — under H by ≈ 518** |

Edge: within the error of the estimate (wording bytes, the page break). If the measure is over H, the role goes on the STOP list (no raise)
and the cheapest next lever is F-10 (b) of the pages spec (one page: −≈400, S21) or the door-drop lever (F-1 (b)).

### §3.2 qa-automator — stays over H

| term | bytes |
|---|---|
| U now | 84,240 |
| H (P = 1) | 68,400 |
| gap | +15,840 |
| `execution_request` rows leaving: 8,170 on the page minus the five manifest-row rows that STAY page-told for this role (`no_test` ≈ 406, `place_rows` ≈ 357, `case_entries` ≈ 525, `profile` ≈ 660, `selector_args` ≈ 415: ≈ 2,363 est., from the row texts at stage-joints.json 6216-6597) — 18 rows | −5,807 (est.) |
| `run_suite` rows leaving (6 rows) | −1,443 |
| two index lines | +345 (est.) |
| pages: 30,399 -> ≈ 23,494 -> 2 pages instead of 3 (one continuation header gone, S21) | −400 (est.) |
| **U' (est.)** | **≈ 76,935 — over H by ≈ 8,535: STOP stays** |

### §3.3 qa-test-strategist — not touched

It holds no ER and no RS row (report §3 line 58). Gap to green: 55,724 − 46,008 = **9,716** (to H: 13,324). This node changes nothing for it.

### §3.4 Would the other families have to follow? (the brief's Q2 second half)

`manifest_put`, `s5_precheck`, `validate_artifacts`, `coverage_contract`, `planning_contract` (and `exit_gate`, `handoff_check`) judge an
artifact the role WROTE: FR-38's own check (factory-rules FR-38 *Check*, quoted by critic B2) requires them told before the work; pages
§10(1) keeps `manifest_put` off the list. They cannot follow. Even if they did (counterfactual, to show the lever is exhausted):

| role | after this node (est.) | + manifest_put + s5_precheck + validate_artifacts (+ coverage/planning for the strategist) leaving | still over |
|---|---|---|---|
| qa-automator | 76,935 | −2,623 −3,947 −1,253 = −7,823 | ≈ +712 over H |
| qa-test-strategist | 55,724 | −1,560 −1,659 −845 = −4,064 | ≈ +5,652 over baseline |

So no call-telling lever closes these two roles. What can (none of it is this node; all named as next nodes in F-1):
- **Door-drop for SITED output rows** (critic §4: automator 2,489 B, strategist 1,922 B, code-critic 1,502 B measured at T1r; only rows
  whose refusal prints the door — so the real saving today is smaller: `handoff_check`, `validate_artifacts`, `planning_contract`,
  `coverage_contract`, `s5_precheck`, `manifest_put` are unsited until T6/T7/T5) and **`handoff_check:null_outcome.*` scoped to the contracts
  that have a null outcome** (658 B on every page). Lead-closable renderer levers.
- **Pages F-2 (c)**: a designer pass removing charter/slice prose the rows now state (opened by the Lead in parallel, pages §10 N8). The
  non-row share of U is large: automator ≈ 53.8K of charter/slices (84,240 − 30,399 page) and ≈ 7K of non-row text on its pages;
  strategist ≈ 8.5K of non-row text on its pages (17,762 page bytes − 9,291 bytes of rows) — most likely the `### Not yet in rows` card,
  which T1r-cards turns into rows (could not establish without the page read; labelled).
- Owner: pages F-2 (d) (project files by path on Codex) or a named raise (a). Never by default.

Required from those levers after this node (est.): automator ≈ 8,535; strategist 9,716.

### §3.5 The other two roles that hold these families (green already; they get lower)

| role | U now | leaving | index | U' (est.) |
|---|---|---|---|---|
| qa-runner | 59,014 | ER 5,461 (13) + RS 1,234 (3) | +345 | ≈ 52,664 |
| qa-failure-analyst | 67,058 | ER 6,017 (14) + RS 360 (1) | +345 | ≈ 61,026 |

Their A22 rows (`process_ratchet_tokens`, slack 0) must be set to the new measure in the same move (S-2 P-6), else they go red the other way.

---

## §4 The builder cards

Two SEQUENTIAL nodes with disjoint owns (F-5): **S-1 code** (sites + transport) then **S-2 data** (markers, wording, regenerate, measure).
Both on branch `wip/tbw-t1r` after T1r-pages' open items close (F-6). S-2 cannot start before S-1 is accepted: `call_told` reads the real
sites from code (S3), and a marker on an unsited row is red (S4).

### §4.1 Node S-1 — sites and transport

given: this file whole; T2 spec §2 (T2-1..T2-11, the "Record vs str" table); mechanism §5.1 rows T5/T5b and §5.4 rows 10-19, 34-37; pages
spec §10; `W\scripts\detector_verdict.py` (`Record`, `with_check`, `refusal`, `spoken`); `W\scripts\execution_request.py`
(`RequestError`, `MineRefusal`, `WindowFirst`, `validate_request`, `JobStore`, the functions of the table below); `W\scripts\run_suite.py`
(`_refuse_phantom_story`, `resolve_detail_target`, `refuse_untyped_story_run`, `refuse_missing_executor`, `reparse_run_block`, `main`, the
`--mine` builder around 2016-2102); `W\scripts\red_sandbox.py` 1260-1284 (read only: the JSON reader); `W\scripts\stage_joints.py`
(`check_ids`, `sited_ids`, `_is_sited`, `row_for`, `told_text`; read only); `W\scripts\refusal_registry.py` (`_record_kind`, `_scan_wide`; read
only); `W\references\stage-joints.json` (the 31 ER/RS rows; read only); tests `test_execution_request.py`, `test_detector_verdict.py`;
`W\scripts\tests\test-layers.json`; `design/factory-rules.md` whole; `plans/builder-rules.md`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\execution_request.py (RequestError.records; validate_request; JobStore.begin, JobStore.recover, JobStore.read; find_active_dispatch; _entries_of_case; _profile_for; _command_from_profile; sandbox_run_directory; _place_rows; _observe_precedent; _observe_stand; build_mine_request; the import of refusal)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\run_suite.py (_refuse_phantom_story, resolve_detail_target, refuse_untyped_story_run, refuse_missing_executor, reparse_run_block, main, the --mine builder's except branches; the imports)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\detector_verdict.py (new told_fields only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_execution_request.py (T1rs rows only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (T1rs/told-fields rows only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\changelog.d\tbw-t1r-sites.md
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-t1r-sites-report.md
non-goals: `stage-joints.json` (markers, wording, ratchet: S-2); any row sentence or door; generated slices; `role-load.json`;
`s5_precheck.py`, `manifest_put.py` (T5 rest); `stage_joints.py` and `contract_slices.py` code; the TEXT of any refusal (`error`, the
`ap.error` problem line, the person question of `refuse_missing_executor`, every `MINE (note)` line); refusals that map to no row (E6);
`test_run_suite_mine.py` (quarantined); a new test file; CI, mutations
handoff: the commit on `wip/tbw-t1r` plus the report in owns: the site table filled (site, id, test row), the grep witness of §4.1 P-7, the
list of sites left bare (E6) with the reason, the `stage_joints.py --check` summary line before/after (`unsited` 150 -> measured), FR walk,
verbatim witness
edges: §5 E4-E8, E12-E14 (each with its invariant)
siblings: T2 sinks `hooklib.block` / `stage_guard.deny` / `role_cli.refuse` (the text road of the same Record: `spoken`); T5 rest
(`s5_precheck`, `manifest_put`); T4 (PT/SG sites); `red_sandbox.py` and `execution_scheduler.py` (readers of the JSON lines, untouched);
SIBLING_MAP axes 17, 18, 34 (§7)
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/execution_request.py ai-packages/qa-factory/scripts/run_suite.py ai-packages/qa-factory/scripts/detector_verdict.py` — every non-slow file it lists, each alone; then `python -B ai-packages/qa-factory/scripts/stage_joints.py --check`; then `python -B ai-packages/qa-factory/scripts/selftest.py --lang`
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-t1r-sites-spec.md
architecture: AR-9, AR-13, AR-15, AR-16, AR-18, AR-22, AR-28, AR-29 -- refusals write the row id through refusal(); the JSON refusals gain one additive `told` key built by one helper; error text and person question byte-identical
judgment: none moved -- sites write a literal id; no meaning check added

| item | what | expected behaviour | test |
|---|---|---|---|
| P-0 | Measure before | verbatim `stage_joints.py --check` summary (expect `unsited 150`); list which of the 31 ids an EXISTING case of `test_execution_request.py` already provokes (by running the file once and reading its cases; a list, no change) | report §before |
| P-1 | `told_fields(source) -> dict` in `detector_verdict.py`, next to `spoken` | collects Records from: a `Record`; a list/tuple of items; an exception (its `records` attribute when non-empty, else `args[0]` when that is a Record). Returns `{"told": [{"check": c, "expected": e, "door": d}, ...]}` — one entry per distinct `check` in first-seen order, a key left out when its value is empty; `{}` when no Record has a check. Never raises (an odd source -> `{}`) | `T1rs/told-fields/record`, `/str-empty`, `/exception-records`, `/exception-arg`, `/dedupe-order`, `/odd-source` (test_detector_verdict.py) |
| P-2 | `RequestError.records` | class attribute `records: tuple = ()`; `validate_request` sets `exc.records = tuple(e for e in errors if getattr(e, "check", ""))` on the instance before raising; message `"; ".join(errors)` unchanged (Records join as their text) | `T1rs/error-bytes/invalid_request` |
| P-3 | Import | `execution_request.py` and `run_suite.py`: `from detector_verdict import refusal, spoken, told_fields` (the form T2-8's binder reads, S5). No import cycle: `detector_verdict` imports only `role_cli` at top and `stage_joints` lazily (read at 52-59) | the DoD run imports both modules |
| P-4 | Relabel sites (table below) | at each site, the problem text is wrapped, never changed: `errors.append(refusal("<id>", <old expression>))`; `raise MineRefusal(refusal("<id>", <old expression>))`; `raise WindowFirst(refusal("<id>", message), payload)`; `raise RequestError(refusal("<id>", <old>))`. EVERY site the table maps to an id is relabelled (E4) | `T1rs/told/<id>` |
| P-5 | Transport | every printer of S12 that prints a relabelled refusal adds `**told_fields(exc)` (or the record) to the SAME dict, after the existing keys: `invalid_request` (main, `_refuse_phantom_story`, `resolve_detail_target`), `mine_refused` (both), `invalid_recovery`, `run_refused` (the `reference_target_problem` print, 2881), the `WindowFirst` payload print (2078), `refuse_missing_executor`'s exit-3 JSON. `refuse_untyped_story_run`: `ap.error(spoken(refusal("run_suite:untyped_story_run", UNTYPED_STORY_RUN.format(stage=stage))))`. No new line on stdout/stderr; one JSON line stays one line | `T1rs/told/<id>`, `T1rs/error-bytes/<channel>`, `T1rs/one-json-line/<channel>` |
| P-6 | Tests (rows in keep files only) | §4.1 test table | witness |
| P-7 | Grep witness in the report | `refusal("execution_request:` and `refusal("run_suite:` occurrences, one per row id at least, and the ids with no literal (must be none of the 31); every `errors.append(` in `validate_request` that is NOT a `refusal(` call, each with its E6 reason | report |
| P-8 | Changelog | one English ASCII bullet | `selftest.py --lang` |

Site table (id -> where; read on the working tree; the builder confirms each site by its message and lists any extra site it finds that
carries the same class of problem — relabelled with the same id — or a site that fits no row — left bare, E6):

| id | function (file `execution_request.py` unless named) | sites (lines of my read) |
|---|---|---|
| `execution_request:purpose` | `validate_request` | 126, 128 |
| `execution_request:selection` | `validate_request` | 132, 135, 139, 296, 302 |
| `execution_request:budget` | `validate_request` | 141, 143 |
| `execution_request:freshness` | `validate_request` | 145 |
| `execution_request:runtime` | `validate_request` | 149, 153, 163, 168, 173, 184, 189, 193, 195 |
| `execution_request:stand.reference` | `validate_request` 180; `run_suite.main` 2877-2882 (`reference_target_problem`); `_observe_stand` 2875 | 3 sites |
| `execution_request:fingerprint` | `validate_request` | 199, 203 |
| `execution_request:command` | `validate_request` | 207, 211, 214, 220, 223, 225, 228, 230, 233, 245, 248, 256, 258, 264 |
| `execution_request:execution` | `validate_request` | 273, 280, 285, 292 |
| `execution_request:selector` | `validate_request` | 298, 306, 308, 326, 328 |
| `execution_request:instance_contracts` | `validate_request` | 336, 342, 346, 349, 352 |
| `execution_request:active_dispatch` | `find_active_dispatch` | 913, 925 |
| `execution_request:case_entries` | `_entries_of_case` | 1191, 1206, 1221 |
| `execution_request:profile` | `_profile_for` | 1719, 1728, 1733, 1748, 1754, 1772, 1779, 1792, 1797 |
| `execution_request:profile_command` | `_command_from_profile` 1826, 1837; `build_mine_request` 3433 (`selectors.join`) | 3 sites |
| `execution_request:place_rows` | `_place_rows` | 2677 |
| `execution_request:stand` | `_observe_precedent` 2825; `_observe_stand` 2869 | 2 sites |
| `execution_request:stand.probe` | `_observe_stand` | 2859 (its OWN literal: S2 would otherwise call it sited through `stand`) |
| `execution_request:mine_call` | `build_mine_request` | 3224, 3227, 3314, 3444, 3457 |
| `execution_request:scope` | `build_mine_request` 3296; `s6_close_from_state` 1012 (not in the approved scope) | 2 sites |
| `execution_request:no_test` | `build_mine_request` | 3331, 3472, 3497 |
| `execution_request:selector_args` | `build_mine_request` | 3583 |
| `execution_request:sandbox` | `build_mine_request` 3602; `sandbox_run_directory` (its refusals; not read by me — the builder lists them) | ≥ 1 |
| `execution_request:window_first` | `build_mine_request` | 3659 (`WindowFirst`) |
| `run_suite:begin` | `JobStore.begin` | 417, 436, 438 |
| `run_suite:recover` | `JobStore.read` 403 (corrupt job file), `JobStore.recover` 454 | 2 sites |
| `run_suite:phantom_story` | `run_suite._refuse_phantom_story` | 968-971 (the `StoryRootError` text) |
| `run_suite:detail_target` | `run_suite.resolve_detail_target` | 1115-1116 |
| `run_suite:untyped_story_run` | `run_suite.refuse_untyped_story_run` | 1416 |
| `run_suite:missing_executor` | `run_suite.refuse_missing_executor` | the exit-3 print |
| `run_suite:reparse` | `run_suite.reparse_run_block` | 738, 742, 746, 751, 754, 757, 760, 818 |

Left bare (E6; the report lists them): the `"<key> is required"` list (118), `validate_baseline_request` / `validate_managed_gate` (121,
123), `validate_record` (357-359), `probe_record` (108, 112), the S6-close context and story-folder refusals of `s6_close_from_state`
(955-1005) and `build_mine_request` (3234-3259), the fingerprint failure (3717), `run_refused` budget / verdict prints (2912, 2945). None is a
row's requirement today; none is on any page; nothing about them changes.

Test rows (S-1):

| id | file | expected |
|---|---|---|
| `T1rs/told/<id>` (one parameterised table, a row per id of the site table) | test_execution_request.py | the refusal, provoked as the existing case does (or by a new table row when P-0 found no case), prints `error` exactly as before AND a `told` entry whose `check` is `<id>` and whose `expected` equals `stage_joints.told_text(row)[0]`. A row is added for EVERY id; an id the builder cannot provoke in a keep file is reported (F-4 then keeps that row on the page in S-2) |
| `T1rs/error-bytes/<channel>` (invalid_request, mine_refused, invalid_recovery, run_refused, window_first, missing_executor) | test_execution_request.py | `error` (and the person question for missing_executor, the `command` key for window_first) byte-identical to the pre-change value; `execution_status` absent |
| `T1rs/one-json-line/<channel>` | test_execution_request.py | the channel's stream holds exactly one line starting with `{` for the refusal (S13's reader still picks it) |
| `T1rs/no-launch/<channel>` | test_execution_request.py | after the refusal the story's `state/execution-jobs` holds no new job (S14 holds) |
| `T1rs/unreadable-row` | test_execution_request.py | with `stage_joints.row_for` patched to return `(None, "x")`, the refusal still prints, exit code unchanged, `told[0].expected` is the factory-defect sentence (S10), no `door` key |
| `T1rs/told-fields/*` (6) | test_detector_verdict.py | P-1 |

Commands (from `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r`):
1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/execution_request.py ai-packages/qa-factory/scripts/run_suite.py ai-packages/qa-factory/scripts/detector_verdict.py` — every non-slow file it lists, each alone (`python -B <path>`); a slow or quarantined file it lists is named in the report as "judged by the batch canon"
2. `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` (expect green; `unsited` measured ≈ 119 under the stored 150, S19)
3. `python -B ai-packages/qa-factory/scripts/selftest.py --lang`
4. `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py`

Acceptance keys: every `T1rs/*` row green; `stage_joints.py --check` green with `unsited` = 150 − (number of the 31 ids sited) (expected 119);
no id of the 31 without a literal; `error` bytes unchanged on every channel; the census green.

### §4.2 Node S-2 — data, pages, measure

given: this file whole; the S-1 report and commit; pages spec §3.1 P-4, P-10 and §10; `W\scripts\stage_joints.py` (`call_told`,
`call_families`, `call_wording`, `_call_leg`, `_shape_problems`, `_told_counters`; read only); `W\scripts\contract_slices.py`
(`_told_units`, `_call_index_lines`, `requirement_section`; read only); `W\scripts\role_load.py` (`native_headroom_problems`, read only);
`W\references\stage-joints.json`, `inject-map.json`, `role-load.json`; tests `test_stage_joints.py`, `test_contract_slices.py`,
`test_role_load.py`; `design/factory-rules.md` whole; `plans/builder-rules.md`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\stage-joints.json (producers' told of the 31 ER/RS rows; the producer split of execution_request:no_test, selector_args, place_rows, profile, case_entries; call_index_wording of execution_request and run_suite; told_ratchet.unsited)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\slices\ (handoff-keys*.md and index.md of the roles that change, generated by contract_slices.py --write only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\inject-map.json (continuation page lines only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\role-load.json (ratchet_tokens and process_ratchet_tokens of qa-automator, qa-code-critic, qa-runner, qa-failure-analyst: set to the measure; native_headroom untouched)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_stage_joints.py (T1rs rows only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_contract_slices.py (T1rs rows only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-t1r-sites-report.md (section S-2)
non-goals: any code file; any row sentence or door; any family other than ER/RS (no change to `call_told_families` membership); a raise
of `native_headroom`, a cap or a ceiling; a raise of an A22 row (rows here only fall: if one would rise, STOP and report); merging the
branch; CI, mutations; a new test file
handoff: the commit plus the report: per role (12) U, H, page bytes, page count before/after; the ER/RS rows told at the call per role; the
STOP list (role, U', H or baseline, gap) — expected qa-automator and qa-test-strategist, and qa-code-critic only if its measure is over H;
ratchet rows (key, old -> new, reason "T1r-sites: ER/RS rows told at the call"); verbatim witness
edges: §5 E1-E3, E9-E11 (each with its invariant)
siblings: pages spec `T1rp/*` rows (same files); T1r-cards (§8: new rows in these families default to the call item only when sited and
split by class); SIBLING_MAP axes 18, 34 (§7)
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/references/stage-joints.json ai-packages/qa-factory/references/inject-map.json ai-packages/qa-factory/references/role-load.json` — every non-slow file it lists, each alone; then `python -B ai-packages/qa-factory/scripts/contract_slices.py --check`; `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; `python -B ai-packages/qa-factory/scripts/stage_joints.py --check`; `python -B ai-packages/qa-factory/scripts/tests/test_role_load.py`; `python -B ai-packages/qa-factory/scripts/tests/test_contract_slices.py`; `python -B ai-packages/qa-factory/scripts/tests/test_stage_joints.py` ONCE, last
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-t1r-sites-spec.md
architecture: AR-1, AR-10, AR-11, AR-12, AR-20, AR-22, AR-23 -- ER/RS call checks told at the call with an index line naming the before-work door; output judges stay on the page; unsited and A22 rows set to the measure (lowered); native_headroom untouched
judgment: none moved -- marker placement follows pages §10(3) as written; membership unchanged

| item | what | expected behaviour | test |
|---|---|---|---|
| P-0 | Measure before | per role `static_load(role, "first")` U, page bytes per file, per-family bytes (the T1r-pages builder's method); the S-1 sited list | report §before |
| P-1 | Markers | on every producer entry of the 31 rows: `{"page": true}` -> `{"page": true, "call": true}`, EXCEPT the qa-automator part of the five manifest-row rows: each of `no_test`, `selector_args`, `place_rows`, `profile`, `case_entries` gets two entries with the same `field` and `demands`: `{"roles": ["qa-automator"], "told": [{"page": true}]}` and `{"roles": ["qa-runner", "qa-code-critic", "qa-failure-analyst"], "told": [{"page": true, "call": true}]}`. A row whose id S-1 reported as not provoked by a test (F-4) keeps `{"page": true}` | `T1rs/partial-split/<row>`, `T1rs/marked-iff-tested` |
| P-2 | Wording | `call_index_wording.execution_request` = "{n} checks of your `run_suite.py` calls are told in the refusal of the call, with what they expect and the door; a refused call launches no test. Write a request file from `run_suite.py --template request`, never from memory." `run_suite` wording unchanged | `T1rs/index-line/execution_request` (holds `--template request`) |
| P-3 | Ratchet | `told_ratchet.unsited` = the measure after S-1 (expected 119) | `stage_joints.py --check` |
| P-4 | Regenerate | `contract_slices.py --write`; drop a continuation line of `inject-map.json` whose page the partition no longer makes (the automator's `handoff-keys-3.md` expected), add one it asks for; re-run until `--check` names only K10 roles | `contract_slices.py --check`, `selftest.py --limits` |
| P-5 | K10 verdict | per role: U' <= H (or <= its baseline) -> green; else STOP list, no raise | report table |
| P-6 | A22 | `ratchet_tokens` / `process_ratchet_tokens` of the four touched roles set to the measure (each a LOWERING; a rise = STOP) | `test_role_load.py` green; the A22 read of the pages DoD item 7 |
| P-7 | Changelog | append one bullet to `changelog.d/tbw-t1r-sites.md` | `selftest.py --lang` |

Test rows (S-2):

| id | file | expected |
|---|---|---|
| `T1rs/sited/<family>` (2) | test_stage_joints.py | every row id of the family is a KEY of `check_ids()` (its own literal — not `_is_sited`, S2) |
| `T1rs/partial-split/<row>` (5) | test_stage_joints.py | `call_told(row, "qa-automator", ...)` False; True for runner, code-critic, analyst |
| `T1rs/marked-iff-tested` | test_stage_joints.py | the set of ER/RS rows with a call marker == the set S-1 reported as provoked (a list constant in the test, pinned to the report) |
| `T1rs/listed-zero-sited` | test_stage_joints.py | synthetic data: a listed, worded family with two rows, no site, no marker -> `call_told` False for both, `_call_leg` returns [], and a marker added on one -> red "has no site in code" (E1) |
| `T1rs/index-line/execution_request`, `/run_suite` | test_contract_slices.py | on the four roles' key pages: one line each, count = that role's call-told rows (automator 18 / 6, code-critic 14 / 2, runner 13 / 3, analyst 14 / 1); the ER line holds `--template request` |
| `T1rs/partial-family/qa-automator` | test_contract_slices.py | the automator's pages hold the ER index line AND the five manifest-row rows as whole lines (E3) |
| existing `T1rp/no-row-lost/<role>` | test_contract_slices.py | still green (page ids ∪ call-told ids == `rows_for` ids) |

Acceptance keys: `stage_joints.py --check` clean; `selftest.py --limits --lang` green; `contract_slices.py --check` names only the STOP roles
of the report; every T1rs row green; `test_role_load.py` green with every changed A22 row LOWER; no `native_headroom` change; the §3 table
measured.

---

## §5 Edges (each with the invariant it protects)

- **E1 A listed family with zero sited rows (today's state of ER/RS).** `_shape_problems` passes (the family is the stem of rows); no marker
  exists, so `_call_leg` is silent; `call_told` is False for every row; `_call_index_lines` writes no line (no called row); every row stays
  on the page; `--check` prints nothing about the family. Kept as is (no new output: the summary line is pinned by tests). Invariant: never
  an index line counting 0, never a row in neither carrier; a marker added before its site is red (S4). Row `T1rs/listed-zero-sited`.
- **E2 A row told at the call for some roles only.** Siting is per id, global (S1); "for some roles" is the producer split of P-1:
  `call_told` checks every producer entry that names the role (S3). A role named in two entries of one row (a builder slip) needs the marker
  in both, else the row stays on its page. Invariant: a row that judges a role's finished work is never call-told for that role; any doubt
  keeps the page (more text, never less).
- **E3 The index line of a partly call-told family.** `{n}` = the call-told rows of THAT role only; the role's page-told rows of the same
  family render as whole lines beside it. The wording never says "all checks". Invariant: page ids ∪ call-told ids == `rows_for` ids
  (`T1rp/no-row-lost`).
- **E4 A row with several sites, only some relabelled.** `_is_sited` then says "sited" for the whole row (it needs one literal): the gate
  errs toward GREEN — the unsafe side. Behaviour: S-1 relabels every site of the table; P-7's grep lists every remaining bare append of
  `validate_request` with its E6 reason; S-2 marks only rows a `T1rs/told/<id>` row proves (F-4). Invariant: a row counted told at the call
  prints its sentence on every site the table maps to it. Residual: a site of the same class found later is a `defect_found` against S-1.
- **E5 The row cannot be read at run time** (file absent or broken in an install). `refusal()` gives the factory-defect sentence (S10);
  `error`, exit code and the JSON line are unchanged. Invariant: never a crash, never a pass (FR-59, AR-28).
- **E6 A site whose problem is no row's requirement** (list under the site table). Stays a bare string, its JSON carries no `told` key.
  Invariant: a refusal never prints a sentence that is not its own (no "nearest row" guess).
- **E7 Several problems in one request.** `told` holds one entry per distinct check, first-seen order; `error` is the unchanged `"; "` join.
  Bound: at most 11 entries (the ids of `validate_request`), no truncation needed. Invariant: every refused check's sentence is printed
  once.
- **E8 JSON readers.** `told` is additive inside the one JSON object; `error` byte-identical; `execution_status` never added; no extra line
  starting with `{` (S13). Invariant: no reader that takes `error` or the last `{` line sees a different value.
- **E9 TEMPORAL — between S-1 and S-2.** Sites exist, no markers: rows stay on the page AND the refusal tells them (double telling, more
  text); `unsited` stored 150 over the measured ≈ 119 is green (S19). After S-2: markers + the lowered ceiling. Wrong order (S-2 before S-1):
  every marker is red at K2 and the page item stands. Invariant: no state with a row in neither carrier.
- **E10 TEMPORAL — a story mid-run on an older installed generation.** One generation per install (B-014): its pages and its code agree.
  Invariant: no dispatch mixes a call-told page with an unsited refusal.
- **E11 K10 AT/BEYOND.** U' = H green; U' > H and over the baseline -> STOP list, no raise. Invariant: no unnamed raise; no role left over H
  silently.
- **E12 The person question of `missing_executor`.** Its text and options are unchanged; `told` is a sibling key of the printed object.
  Invariant: text a person reads still goes only through the question form (AR-16).
- **E13 `ap.error` with a multi-line message** (`untyped_story_run`). argparse prints usage + `error: ` + the spoken text, exit 2, as
  today. Invariant: the problem line is the first line, byte-identical.
- **E14 `WindowFirst`.** The payload's `status` and `command` keys are unchanged; `told` is added. Invariant: the one command the role is
  told to run stays the same string.
- **Error direction of reused functions in new roles.**
  - `_is_sited` as the gate inside `call_told`: may err toward "unsited" (the row stays on the page: safe); it errs toward "sited" on a
    partial relabel (E4) and on a sub-id (S2). Adversarial inputs that must stay on the safe side: `execution_request:stand.probe` with only
    `execution_request:stand` sited (the test reads `check_ids()` keys, not `_is_sited`); a literal that only shares a prefix
    (`run_suite:beginx`); an id in a comment or string (T2's scanner rule); `refusal(name_var, ...)` (walk error, T2).
  - `refusal()` as the call-time teller of a command refusal: may err toward the factory-defect sentence (visible), never toward silence or a
    changed `error`.
  - `told_fields`: may err toward `{}` (nothing added: today's output), never toward a `told` entry whose `check` did not produce the error.

---

## §6 Forks (returned; recommendation first; none raises anything)

- **F-1 (Lead; owner for the residual) Scope against the brief's goal.** The node cannot bring qa-automator (≈ +8,535 after) or
  qa-test-strategist (+9,716, untouched) under their lines (§3). (a) Run this node as drafted (code-critic to green by an edge, automator
  −≈7,300, runner/analyst lower), and name the next nodes: N-door "door-drop for SITED output rows + `handoff_check:null_outcome.*` scoped to
  contracts with a null outcome" (Lead-closable renderer node in `contract_slices.py`; its saving grows as T5/T6/T7 site output rows) and
  pages F-2 (c) (prose the rows now state; already opened, §10 N8), with the owner's (d) behind them; (b) widen THIS node with N-door (one
  more code file, `contract_slices.py`, which T1r-pages also owns: more conflict, no role closed by it alone); (c) put output families on the
  call list — refused by FR-38 and still insufficient (§3.4), listed only to close it. **Recommend (a).** Covering the left-out side costs
  N-door (≈ 2-3K per role, est.) plus ≈ 5-7K of prose per STOP role.
- **F-2 (Lead) The transport shape for the JSON refusals.** (a) one additive key `told: [{check, expected, door}]` inside the existing JSON
  object, built by `detector_verdict.told_fields`; (b) `error` = `spoken(record)` (changes the bytes every reader and test matches); (c)
  print the `spoken` tail lines after the JSON line (a second road beside the JSON, and readers that scan lines see extra text). **Recommend
  (a):** additive, one helper beside `spoken`, the same three field names.
- **F-3 (Lead; the owner's F-2 of the pages spec stands behind it) FR-38 direction per family.** A requirement told at the refusal is learned
  after a failed call; that is acceptable only where the call is cheap and repeatable and nothing irreversible happened (S14).

  | rows | who | cost of a refused call | recommendation |
  |---|---|---|---|
  | 10 request-file rows (`purpose`…`instance_contracts`) | automator | the request file was written by hand (work), nothing launched, no key, no budget, no lease (S14); a before-work door exists (S15) | call-told, ONLY with the `--template request` clause in the index line (pages §10(3)) |
  | 8 `--mine` call-shape rows (`active_dispatch`, `profile_command`, `stand`, `stand.probe`, `stand.reference`, `mine_call`, `scope`, `window_first`) + `sandbox` | all four roles | one call; may include a read-only stand probe or a collect (seconds), nothing launched | call-told |
  | 5 manifest-row rows (`no_test`, `selector_args`, `place_rows`, `profile`, `case_entries`) | automator | they judge the automator's own manifest rows — finished work met only when someone runs | PAGE for the automator (pages §10(3)); call-told for runner/code-critic/analyst |
  | 7 `run_suite` rows | per S17 | every one refuses before a launch; `missing_executor` is not the role's to meet (it hands to the person) | call-told |

  No row of these families spends a run when refused (S14), so none must stay on the page by cost. (b) keep every automator ER row on the
  page (automator saves only ≈ 1,400, code-critic unchanged by it). **Recommend (a) = the table.** Could not establish: for each
  `MineRefusal` site, whether it comes before or after the `--mine` collect subprocess (cost in seconds, never a run); not load-bearing for
  the recommendation.
- **F-4 (Lead) A sited row whose refusal no test row proves.** (a) S-2 puts the call marker only on rows S-1 proved by `T1rs/told/<id>`; S-1
  adds a table row for every id it can provoke in a keep file; an id it cannot is reported and keeps the page; (b) mark every sited row.
  **Recommend (a)** (the safe side of E4). Cost: a row left unproved keeps its bytes on the page (it can tip code-critic's ≈ 518 margin; the
  report names it).
- **F-5 (Lead) One node or two.** (a) S-1 code then S-2 data, sequential, disjoint owns; (b) one node (≈ 120 relabelled sites + data + slow
  test: the T1r-pages builder passed the 250K WARN with less). **Recommend (a).**
- **F-6 (Lead) Branch and gate.** (a) stack on `wip/tbw-t1r` after T1r-pages' open items close (report Questions 1, 3) — the branch cannot
  merge while K10 is red anyway, and this node is part of what greens it; (b) wait for a merge of `wip/tbw-t1r` and run from `main` —
  impossible while K10 is red. **Recommend (a).** Needed beyond the manifest: the Lead checks the piles for any running T5 / T5b node
  (`execution_request.py`, `run_suite.py` by function, PROJECT.md «Командная работа» 3) — I could not establish their status.
- **F-7 (Lead) The strategist.** Nothing here moves it. (a) name it in this node's STOP list unchanged and leave it to F-1's next nodes;
  (b) hold this node until a strategist lever is drafted. **Recommend (a).**
- **F-8 (Lead) Absorbing mechanism T5 (ER + RS parts) and T5b.** (a) this node replaces them; mechanism T5 keeps `s5_precheck.py` and
  `manifest_put.py`; its test line "the automator's page names it" no longer holds for ER/RS rows told at the call — the Lead edits the
  mechanism's node table in the same move; (b) run T5/T5b as written and do only S-2 here (then T5 must also add the JSON transport,
  which its text does not say). **Recommend (a).**

## §6a Lead decisions (14.11.2026, owner away: by recommendation, reversible — all work stays on `wip/tbw-t1r`; in the morning report)

- F-1 (a): the node runs as drafted; the residual (automator ≈ +8.5K, strategist +9,716) is NOT closed by it and is named to the
  owner in the morning report with the next nodes (N-door; the prose pass F-2 (c)). No H or headroom raise, nothing trimmed.
- F-2 (a) additive `told` key. F-3 (a) the table, "по рекомендации, до слова владельца" (the owner's F-2 of the pages spec stands
  behind it: a requirement learned at a refused call). F-4 (a) marker only on proved rows. F-5 (a) two sequential nodes S-1, S-2.
  F-6 (a) stack on `wip/tbw-t1r` after the T1r-pages fix round (t-722 attempt 2) is accepted. F-7 (a). F-8 (a): the Lead edits the
  mechanism's node table (T5/T5b) in the same move as S-1's dispatch; the piles status of T5/T5b is checked by the Lead before it.
- Before any builder: a plan critic (new transport key in refusal JSON, ~120 relabelled sites, FR-38 direction).

## §6.1 Small choices closed by the designer

- C-1 Test prefix `T1rs/`; report `20261114-t1r-sites-report.md`; changelog `tbw-t1r-sites.md`.
- C-2 Key name `told`, entry keys `check`/`expected`/`door` (the labels `spoken` already prints).
- C-3 `told` order = first-seen, one entry per check (E7).
- C-4 `RequestError.records` as a class attribute default `()`, set on the instance (no constructor change, so `MineRefusal` /
  `WindowFirst` keep their signatures).
- C-5 The ER index wording of S-2 P-2 (short: every byte counts against code-critic's margin).
- C-6 No new summary output for E1 (the summary line is pinned by tests).
- C-7 `sandbox_run_directory`'s sites are found by the builder (not read by me) and listed in the report.

---

## §7 SIBLING_MAP axes (by enumeration, both nodes)

- axis 1 (policy/role files/journal): n/a — no policy or role file. axis 2 (exam instruments): n/a. axis 3 (package/release/installed):
  covered — one generation per install (E10); no release step here. axis 4 (rules/debt/backlog): n/a — no FR changed, no debt row.
- axis 5 (stage twins): covered — ER/RS rows run in S5/S6/S7; one rule for all three stages (no stage branch). axis 6 (measurers): n/a.
- axis 7 (test identity): n/a. axis 8 (story on disk): n/a — `story_root` reads untouched. axis 9, 10, 11: n/a — no test-file, git-top or
  shell recognizer touched. axis 12 (work-plan carriers): queued — the Lead's edit of mechanism T5/T5b rows (F-8). axis 13 (dispatch text):
  n/a. axis 14 (transcripts): n/a. axis 15 (console stream): n/a. axis 16 (JSON reader): n/a — no file read added.
- axis 17 (detector verdict shape): covered — the JSON refusals are not form 1; the Record fields are projected by one helper beside
  `spoken` (AR-18); the T2 sinks are the text road of the same Record. axis 18 (shrink-only ratchets): covered — `told_ratchet.unsited`
  lowered to the measure, A22 rows lowered, each named in the report and the merge verdict; `native_headroom` untouched.
- axis 19, 20, 21, 22: n/a — no tools line, host receipt, markdown table reader or host return form. axis 23 (fields of a `tests[]` row):
  n/a — the five manifest-row rows' sentences are unchanged. axis 24 (record of an execution), 25 (freshness): n/a — no read changed.
  axis 26: n/a. axis 27 (profile of a test row): covered — the `profile` sites keep `_profile_for`'s logic; only the raise is wrapped.
- axis 28 (render site of the row form): n/a — no new render of row fields. axis 29 (jsonl writers): n/a. axis 30 (profile commands): n/a —
  `_command_from_profile` logic unchanged. axis 31 (role carriers): n/a. axis 32 (where judgment lives): covered — no unit or census label
  changes; `judgment: none moved`. axis 33 (which dispatch am I): covered — `find_active_dispatch` logic unchanged, only its raise wrapped.
- axis 34 (one road): covered — one rule for every role from data (§1, P31); the bare E6 sites are a migration state counted by T2's
  `untold`, not a second road. axis 35 (sides), 36 (substitute rows): n/a — `stand.reference` only wraps its existing refusal.
- axis 37 ("a check's requirement: one row <-> constructor <-> key page <-> transports"): not in the map yet (mechanism T10); when T10 adds
  it, `run_suite.py`'s JSON printers with `told_fields` are members of its "transports" row — note for T10.

Four questions for the mechanism this node adds (the JSON `told` transport): (a) cost: one dict merge per refusal; the role reads ≈ 300 bytes
more per refused call and ≈ 6-7K less per start; (b) axes above; (c) detector: `T1rs/told/<id>` and `T1rs/marked-iff-tested` (code), and a
`live-runs` row owed by the Lead: count refusals per ER/RS check id in a run against main's run (critic §2 N4 method); (d) on the path:
`stage_joints.py --check` K2 refuses a marker on an unsited row (S4); `call_told` keeps an unproved row on the page; whether a refused call
is "told before work" stays the owner's word (pages F-2), on discipline, detector (c).

## §8 For T1r-cards and later nodes

- A new row in `execution_request` or `run_suite` takes the call marker only when its id has its own literal site and a `T1rs/told` row;
  a row that judges the writer's own artifact keeps the page for that writer (the P-1 split).
- When T5 sites `manifest_put` / `s5_precheck` (output: page stays), N-door (F-1) can drop their `Door:` segments from the page.

---

## §9 What I did NOT establish

- U-1 Any measured number after the change: no shell in this pass; §3 is arithmetic on the report's measures with labelled estimates
  (the five automator rows, index-line bytes, the continuation header). S-2 P-0/P-5 measure.
- U-2 The refusal sites inside `sandbox_run_directory`, and whether any `MineRefusal` site sits after the `--mine` collect (F-3 note).
- U-3 Which of the 31 ids an existing case of `test_execution_request.py` already provokes (S-1 P-0).
- U-4 The status of mechanism nodes T5 / T5b in the piles (F-6).
- U-5 What the ≈ 8.5K of non-row text on the strategist's pages is (likely the `### Not yet in rows` card); not read.
- U-6 Whether `told_fields` trips any census name pattern (`test_judgment_census.py` decides; expected not).
- U-7 The working tree of `tbw-t1r` was changing during my read (see the header); the builder starts from the branch head after T1r-pages'
  fix round, and re-reads the lines of §4.1's site table.

## §10 Reading trail

- Repo root: pages spec whole (1-464); T2 spec by Grep `sited|unsited|refusal\(|Record|transport` (24-317); plan critic 40-139 and 170-249,
  Grep `sited|execution_request|run_suite|B2|N5`; mechanism spec 386-409, 525-594, Grep `T5b|\bT5\b`; T1r report 14-39; `docs/SIBLING_MAP.md`
  headings (Grep `^## `), 373-397, 582-594; `docs/TESTING.md` 1-90.
- Worktree `tbw-t1r`: T1r-pages report whole; `stage_joints.py` 270-349, 630-780 (twice; drift noted), Grep `sited|call_told|...`,
  `_ratchet`/`_told_counters` 1124-1183, imports; `detector_verdict.py` 94-191, imports; `refusal_registry.py` Grep, 1700-1729;
  `execution_request.py` 1-48, 113-132, 145-209, 268-337, 352-370, 520-539, Grep of `errors.append`, `raise MineRefusal|WindowFirst` (-A1),
  `JobStore`/`RequestError`; `run_suite.py` Grep `RequestError|validate_request|MineRefusal|--template|...`, 2070-2109, 2825-2844, 2870-2929,
  2466-2545, function heads -A14 (734, 964, 1102, 1407, 1552); `red_sandbox.py` 1265-1294; `contract_slices.py` Grep, 640-689;
  `role_load.py` 302-346; `stage-joints.json` rows 3125-3184, 3750-3861, 6180-6720, 8052-8073; code-critic `handoff-keys-2.md` 1-8;
  automator pages Grep of row lines (persisted output, first lines read); `test-layers.json` 1499-1529, 9660-9669, Grep; `slow_tests.json`
  Grep.
- Controls: a Glob with a forward-slash relative pattern returned nothing (miscall); the same Glob with `**/qa-automator/handoff-keys*.md`
  under `references` found the three pages (positive control). The negative claim S6 rests on a Grep whose same pattern hit `run_suite.py:1376`
  and test literals (positive control of the same shape); S7 rests on a Grep that hit three prose lines of `refusal_registry.py`.
