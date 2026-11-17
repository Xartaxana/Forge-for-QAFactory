# RD1-19 (FL1) — a hand-typed pytest id is resolved through `node_ids` when it is stored — builder card, DRAFT

task: t-1245 (designer) | node: rules-debt/1/RD1-19 | feature: F19 | date: 17.11.2026 | status: DRAFT for Lead acceptance
intent: card FL1 of `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (:1473-1487), finding
`plans/piles/rules-debt/findings/20261117-rd2-fl1-ruchnoj-id-pytest-pri-zapisi.md`, parent F-L1 (a)
(`docs/tasks/specs/20261117-rules-debt-fix-spec.md:535-537`).

The card below is executable BY THE RECOMMENDATIONS of §6 (F1 (a), F2 (a), F4 (a) + named node RD1-19b). A fork the Lead
decides otherwise changes the items it names; each fork says which.

---

## §0 Load-bearing facts, read today on the root checkout

1. `manifest_put.py` has no id resolver. Grep `node_ids|nodeid|not verified` over the file: the only hits are unrelated
   (`critic_verdict: unverified`, :1761-1773). Positive control, same tool and pattern shape: the same Grep over
   `scripts/` finds `node_ids.` in `manifest_from_tests.py:1823-1849`, `red_sandbox.py:247-255`, `run_suite.py:1720-1845`.
2. The checkout carries FL9 (RD1-22, 714069d4): `judgment-census.json:613` holds the `claim_pair_problems` row noted
   "RD1-22", `manifest_put.py::claim_pair_problems` :1666 exists, and `fixtures/told-ratchet.json:331-333` reads
   `"manifest_put.py::run": {"bare": 17, "tagged": 0}` (the K4 raise 16 -> 17 that RD1-34 returns to 16). No git command
   was run (designer has no shell); the Lead confirms root HEAD == origin/main before the dispatch (memory note on a stale
   local main).
3. The store path: `manifest_put.run` (:2482-2706). Every refusal before the commit lives there; `merge`/`fold` stay pure
   and replay old journals (:2516-2519, :2620-2621, :2633-2639). The tool-made row stamp precedent is `stamp_provisional`
   (:830-869), called at :2622, before `fragment_key = "manifest:" + content_hash(fragment)` (:2631) and before
   `store.commit` (:2651), which takes the story lock.
4. The writer road that already exists: `manifest_from_tests.resolve_through_pytest` (:1808-1867), opt-in by `--collect`
   (:1896-1904, :1938-1946): ask `f"{file}::{iid}"`, `node_ids.runner_form` + `node_ids.check_request`, `missing` ->
   refusal "Nothing was written", rewrite of `tests[].instance_id` and `then_bindings[].instance_id`, back-spelling by
   `rsplit("::", 1)[-1]`. Without `--collect` it writes the source's ids with a note "NOT verified" (:1943-1946).
   Writer rows carry `generated_from` (`manifest_put.WRITER_MARK` :146; `_writer_tests` :1455-1458), and
   `manifest_from_tests` calls `manifest_put.run` in process (:1957-1963).
5. `node_ids.check_request` (:729-752): not pytest -> note, no ids; a collect that cannot answer -> no resolved, no
   missing, note + `collect_error`; partial (with `form`) -> `match_partial` (direction "not verified, never missing",
   :697-726); complete -> `match` (:627-674). `match` compares the asked base to the collected base EXACTLY (:649):
   `split_id("a.py::T::test_x[p-1]")` gives base `T::test_x` (:551-560), so an asked `a.py::test_x` for a class method
   comes back `missing`. A file-only ask (`not base`, :639-648) is `resolved` when anything was collected under it.
6. The manifest's instance spelling carries no class: `contract.instance_id` = `<function>[<parameter>]` (:3935-3952),
   `function_name` drops everything before the last `::` (:3906-3918); `instance_id_aliases` reads a `X::` prefix as a
   0.7.7 case prefix (:4087-4098). So the latent defect of fact 5 also sits in `resolve_through_pytest` today (estimate
   by reading, not run): a class-method row under `--collect` is refused as "not collected".
7. The project's collect command: `gate_preflight.collect_base(config)` (:440-472) — `test_command_templates`, pytest-shaped
   only, `[]` otherwise; the template ships all three templates empty (`references/templates/config.json:17-21`).
   The S5 node-id timeout key: `execution.node_id_collect_timeout_s`, default 180, and the switch
   `execution.verify_node_ids` (template :125), read by `run_suite._setting` through `config_contract.effective_config`
   over `hooklib.load_config` (:1446-1454, :1721, :1825).
8. Rows of a manifest fragment are project-root relative: `manifest_from_tests` writes `tf.rel` from
   `path.relative_to(root.resolve()).as_posix()` (:462).
9. A new refusal key needs: a `references/stage-joints.json` row (K4/E2, `test_stage_joints.py:113-115`), the K1 count pin
   (`test_stage_joints.py:76`, "273 rows ... +1 manifest_put:probe_owed"), a dry-census row in
   `scripts/tests/fixtures/driver-exits/s5.json` with the `unwalked` ratchet's `raised_by` (SIBLING_MAP axis 38,
   :640-650; ratchet `unwalked: 33` at :354-357). A SOURCED site (`refuse(..., DV.refusal("<key>", ...))`, precedent
   `manifest_put:probe_owed` at :2586-2591) is not a bare site for K4.
10. The person's word on "an id pytest does not collect" already has a road: `red_sandbox._passed_by_person` (:214-224)
    through `waiver.split_overridden` with the block words "not collected by pytest" (:263-273); `node_ids.missing_sentence`
    prints "... is not collected by pytest; nearest: ..." (:787-793).

---

## §1 Architecture, rules, owners, variety

AR-n touched and how each is kept (the change check each demands is in the DoD):
- AR-13 — the collect is read only through `node_ids` (`runner_form`, `check_request`, `match`); the project command only
  through `gate_preflight.collect_base`; the config key only through `config_contract.effective_config(hooklib.load_config())`.
  Change check: no second parser of a collect output, of `test_command_templates` or of `config.json` in the diff (grep
  the diff for `--collect-only`, `splitlines`, `json.load` on config, positive control: the same grep finds them in
  `node_ids.py`).
- AR-15 / FR-17 — `node_ids` is the survivor; the store becomes its fifth site (runner, sandbox, probe, writer, store).
  The class step is fixed IN the survivor (F2 (a)), so the runner, the sandbox and the writer get it too. Change check:
  list every caller of `match`/`check_request` (§4) and say "unchanged / changes".
- AR-14 — `node_id_check` is the code's field: a role-sent value is dropped (E10). Change check: a row the role sends
  with the key never stores the role's value.
- AR-22 — producer `manifest_put.stamp_node_ids`; readers: its own later sends read `node_id_check.asked` (E8);
  `status`/`note` are declared terminal in the artifact contract (role and critic read them; no gate does). Change check:
  the contract sentence names the field and says no gate reads it.
- AR-23 — the field is optional and its absence has one meaning, "not asked" (pre-FL1 rows, writer rows, patch rows).
  Not a required list or field: no `null-outcomes.json` row (closed choice C6).
- AR-28 / FR-59 — an unknown is never a pass: no answer -> `not_verified`, never `verified`, never `missing`; the safe
  default is declared in the field and printed. Not a stage gate: no gate-registry row (no verdict word is compared).
- AR-29 — every check the change adds or alters, with its owner and census class:
  | check | owner | census class | where |
  |---|---|---|---|
  | `stamp_node_ids`: a hand-typed id joins the collect of its file | data (code) | `xref` (blocking only through the sourced site in `run`) | new census row, roles `["qa-automator"]` (precedent `assertion_line_problems` :611) |
  | `stamp_node_ids`: a role-sent `node_id_check` is dropped with a line | data (code) | `shape` (same unit) | same row |
  | `node_ids.match` class step (F2 (a)) | data (code) | `xref`, unchanged | the existing `node_ids.py::match` row if the census has one; the builder confirms by `test_judgment_census.py` |
  | the person's word passes a `missing` (E12) | intent (the person) | — (existing `waiver.split_overridden` road, no new unit) | — |
  No check classifies a role's judgment; the refusal is a join (id <-> collected list), which AR-29 allows.
- AR-10 / FR-38 — the requirement reaches the role before the work: the stage-joints row `manifest_put:node_id` (told:
  page) and the artifact-contract sentence (axis 5 prose twin, slices regenerated).
- AR-9 / FR-1 / FR-2 / FR-57 — the refusal names what is wrong, the nearest collected ids, and doors the automator can
  use (correct the id, type the class path, retract, or the orchestrator records the person's word).
- AR-12 — a collect per call costs time: bounded (E2), asked only for new spellings (E9), one collect per call (C3), never
  under the story lock (positional invariant P1).

FR sections the builder's pass walks (PROJECT.md "Пакет: проход и свидетель" 1): A (FR-1, FR-2, FR-4, FR-57), C (FR-11,
FR-12 no phrase list, FR-13, FR-38), D (FR-16, FR-17, FR-40 way out of `not_verified`, FR-59), F (FR-41), G (FR-29, FR-30,
FR-32, FR-43 n/a); B and E: one line each if untouched.

Variety walk (`design/architecture.md` § A, the three forms):
- `axis 3: held by table|key -- the runner's collect_forms row (launch_check.runner_row via node_ids.runner_form) and test_command_templates; unknown value -> the id is stored with node_id_check not_verified and a printed line naming why (no pytest-shaped command / not a pytest command), never a block, never a silent default`
- `axis 11: held by key -- execution.node_id_collect_timeout_s (default 180, template); unknown value -> the template default 180`
- `axes 1, 2, 4, 5, 6, 7, 9, 10, 12: n/a -- the change reads no product language, surface, flow, source, delivery target, stand, process, artifact language or check kind`
- `axes 8, 13: n/a -- path spelling (backslash, spaces) is node_ids' existing normalization and argv lists, no host fact is read; an older manifest's rows carry no mark and read "not asked", no migration`
No `narrows` line; the P31 question on axis 3 is fork F6.

Commit lines: the builder writes `architecture:` and `judgment:` in the form `tools/architecture_gate.py` carries (the one
carrier of that grammar — not copied here). Content to put in that form:
- architecture: AR-13 (one collect reader), AR-15 (node_ids wired at the store; class step in the survivor), AR-22
  (`node_id_check` producer and its readers), AR-28 (no answer -> not_verified), AR-29 (the new unit is `xref`, owner data).
- judgment: the change adds one `xref` unit owned by data; no role judgment is judged by code. (Never a bare
  `judgment: none`; if the gate's form for "adds a data check" is `none`, it carries its ` -- <why>` with this reason.)

---

## §2 The card (dispatch header lines, R11-f)

given: this card (§0-§5); `ai-packages/qa-factory/design/factory-rules.md` whole; `ai-packages/qa-factory/design/architecture.md`
(AR-13, AR-15, AR-22, AR-23, AR-28, AR-29); `docs/TESTING.md` («Что запускать по своей правке», «Строка теста в DoD», «Тест может
упасть», «Бюджет»); `manifest_put.py::run`, `::stamp_provisional`, `::_current_tests`, `::_spellings`, `::WRITER_MARK`,
`::_refuse_colliding_ids`; `node_ids.py::check_request`, `::match`, `::match_partial`, `::split_id`, `::runner_form`,
`::missing_sentence`; `manifest_from_tests.py::resolve_through_pytest` (the twin road, read-only);
`red_sandbox.py::_passed_by_person` (the person's-word road, read-only); `gate_preflight.py::collect_base`;
`run_suite.py::_setting`; `references/stage-joints.json` row `manifest_put:probe_owed` (the form to copy);
`scripts/tests/fixtures/driver-exits/s5.json` row `manifest_put:probe_owed` and its `ratchet`
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manifest_put.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/node_ids.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/stage-joints.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/artifact-contract-automation.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-automator/artifact-contract-automation.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-code-critic/artifact-contract-automation.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-failure-analyst/artifact-contract-automation.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/s5.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_stage_joints.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manifest_put_assertion_line.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_node_ids.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json
non-goals: `manifest_from_tests.py` (its road joins in node RD1-19b, F4); `thinking-roles/6` TR4-17 (not taken); other FL
cards; `assertion_line_problems` and the then/obligation `assertion_ref` checks (TR4-17 item 1); the manifest's identity
rules (`contract.instance_id`, `instance_id_aliases`) — unchanged; retro-resolving rows stored before this change;
node-id checkers for runners other than pytest (F6); `docs/SIBLING_MAP.md` (Lead, F8); in `test_stage_joints.py` only the K1
pin line; in `test-layers.json` only the `covers` of the two test rows named in owns, and only if the layer check reports
a drift; in `judgment-census.json` only the new row (and the `node_ids.py::match` row if the census asks)
handoff: the builder report (rule 7 of `.claude/agents/builder.md`) with the witness, the `red-before:` lines, the FR pass,
the `--witness-for` block verbatim, the list of slice files `contract_slices.py --write` changed, and the two commit lines
edges: §3 E1-E16 with their invariants; positional P1-P3; temporal T1
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path above>` — run every
file it prints; plus `python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check` (-> `0 discrepancies`),
`python -B ai-packages/qa-factory/scripts/contract_slices.py --check`, `python -B ai-packages/qa-factory/scripts/tests/test_console_encoding.py`
(a script that prints changed), `python -B ai-packages/qa-factory/scripts/node_ids.py --selftest`,
`python -B ai-packages/qa-factory/scripts/manifest_put.py --selftest`; a file the walk marks slow or quarantined: "judged by
the batch canon", not run
siblings: axis 34 — one road: the store calls the same `node_ids` road as the runner, the sandbox and the writer; the
writer's own twin (`resolve_through_pytest`) joins it in RD1-19b (F4); runners with no node-id checker: F6. Axis 5 prose
twin — `references/artifact-contract-automation.md` § Instance identity names the id rule: one sentence + regenerated
slices (item 5). Axis 38 — the new joint gets its dry-census row (item 4). Axis 23 — `node_id_check` is not a required row
field: `window_record.REQUIRED_ROW_FIELDS` unchanged (C6). Axis 7 — the manifest's identity unchanged.
designer: this file, once accepted by the Lead

### Items

1. **`node_ids.match` — the class step (F2 (a)).** After the exact-sibling check (:649-652) and before the parameter rules,
   an asked id whose base holds no `::` and has no exact sibling in its file is compared with the collected rows OF THE
   SAME FILE whose base's last `::` segment equals the asked base. Exactly one such row -> the asked id resolves to it
   (spelled under the asked file path, as `_spell` does), then the existing parameter rules (browser prefix) apply to
   that row's params; a note says the test sits in class `<C>`. Two or more -> `missing` with those rows as `nearest`
   and a note "N classes in <file> define <fn>; name the class: `<Class>::<fn>`". No row -> today's behaviour.
   Error direction: may resolve only to a collected id of the same file with the identical function name; never across
   files, never to another function, never when two classes match. Adversarial inputs that must stay on the safe side:
   (i) `test_y` with `TestA::test_y` and `TestB::test_y` -> missing, both nearest; (ii) `test_y` with a module-level
   `test_y` and `TestA::test_y` -> the module-level one (exact sibling wins, no class step); (iii) `TestA::TestInner::test_y`
   alone -> resolved; (iv) `test_y` vs `TestA::test_y_extra` -> no; (v) `TestA::test_y` in another file -> never; (vi)
   `test_y[p]` vs `TestA::test_y[chromium-p]` -> resolved through the class step then the browser rule; (vii) a parameter
   id holding `::` (`test_y[a::b]`) -> base `test_y` (split at the first `[`), the class step reads the base only.
   test: `scripts/tests/test_node_ids.py` — one table of match variants (rows i-vii) | expected from: §0 fact 5, FR-16/FR-17,
   the error direction of node_ids' docstring (:19-20)
   red-before: row (iii)/(vi) (a class method asked bare comes back `missing` today).

2. **`manifest_put.stamp_node_ids(fragment, task_root, project) -> (fragment, problems, notes)` — new, pure in the sense
   of `stamp_provisional` (the given fragment is not edited; a copy is returned).**
   a. Map first (no collect): from the stored rows (`_current_tests(task_root)`) build `{asked spelling -> stored id}` out
      of every stored `node_id_check.asked`; every instance-id carrier of the fragment (see d) that names an asked
      spelling is rewritten to the stored id (E8).
   b. Eligible rows: `tests[]` rows that are dicts, carry no `WRITER_MARK`, carry an explicit non-empty string
      `instance_id` (or `test_instance_id`) and a non-empty string `file`, and whose spelling is not a spelling of a stored
      row (`_spellings`) — EXCEPT a stored row whose `node_id_check.status` is `not_verified`, which is asked again when
      re-sent with `file` (E9, the FR-40 way out). None eligible -> return at once, no subprocess (E11).
   c. One ask for the call: the command is `gate_preflight.collect_base(effective config)` (lazy import); `[]` -> every
      eligible row `not_verified` "the project has no pytest-shaped command in `test_command_templates`" (E1). The switch
      `execution.verify_node_ids: false` -> `not_verified` naming the switch, no subprocess. Otherwise the ask list =
      for each eligible row `f"{file}::{bare}"` (file with `\` -> `/`; `bare` = the typed id with a legacy case prefix
      stripped when `contract.instance_case` names a case, else the typed id as is, a class path included) PLUS each
      distinct `file` alone (the file-presence probe of E7); `form, note = node_ids.runner_form(argv)`;
      `node_ids.check_request(argv, str(project_root), asks, timeout, form=form)` with `timeout` from
      `execution.node_id_collect_timeout_s` (C4). Any exception from the imports or the call -> every eligible row
      `not_verified` with `"<ExcType>: <message>"` cut to 300 chars (E1).
   d. Reading the answer, per eligible row: resolved, same spelling -> mark `verified`; resolved to another spelling ->
      the stored id becomes the typed id with ONLY the part node_ids changed replaced (the parameter part, or nothing when
      only the class was found — the manifest keeps its own spelling, the class is not added), mark `verified` with
      `asked: <typed id>`, one note "pytest collects <typed> as <stored>"; and every instance-id carrier of THIS fragment
      naming the typed id is rewritten: `tests[].instance_id`, `then_bindings[].instance_id`,
      `obligation_bindings[].instance_ids[]`, `unresolved[].instance_id` and `unresolved[].instance_ids[]` (C5);
      in `unverified` (partial collect) or no answer (`collect_error`, not pytest, notes only) -> `not_verified` with
      node_ids' own reason; in `missing` -> if the file-alone ask of its file is itself `missing` (the file yielded no
      test) -> `not_verified` "file <f> yielded no test in this collect" (E7); else a problem (item 3).
   e. The mark: `node_id_check: {"status": "verified" | "not_verified" | "passed_by_person", "note": "<one line>",
      "asked": "<typed id>" (only when rewritten)}` (C2). A `node_id_check` the role sent on ANY `tests[]` row is removed
      first, with one note "node_id_check is written by manifest_put; the value you sent was dropped" (E10).
   test: `scripts/tests/test_manifest_put_assertion_line.py` — one parameterised table, one world (a temp project whose
   config sets `test_command_templates.quiet` to `<sys.executable> -m pytest`, one test file with a module function, a
   parametrised function, a class method and two classes sharing a method name, and one test file under a folder with a
   space), rows E1-E12 below | expected from: this card §3, FR-16, FR-59, the finding's «Что именно менять»
   red-before: the row "a parametrised id pytest collects under another spelling is stored as typed" (today: stored as
   typed, no mark).

3. **`manifest_put.run` — the call and the one refusal.** Call `stamp_node_ids` right after the
   `unresolved_reason_conflicts` refusal (:2615-2619) and before `stamp_provisional` (:2622) (P1-P3). Notes are printed
   with the other stamp lines after the receipt (as `stamp_notes`, :2696-2697). Problems: if a person's recorded S5 word
   covers the refusal text (the `red_sandbox._passed_by_person` road: `waiver.split_overridden([text], pipeline, "S5")`;
   the text contains `node_ids.missing_sentence`, so the block words "not collected by pytest" cover both sites) -> the
   rows are stored with `passed_by_person` and the words in `note` (E12); else refuse through
   `refuse("manifest_put.py --fragment", DV.refusal("manifest_put:node_id", <text>))` — a SOURCED site, so K4's bare count
   of `manifest_put.py::run` does not move (§0 fact 9). The text: which ids, `node_ids.missing_sentence` (the nearest
   collected ids), "Nothing was committed", the doors — correct the id to the collected one; for a test inside a class
   send the class path `<Class>::<function>`; a row you no longer want goes out with `retracted_instances`; if the person
   has decided the id stands, the orchestrator records `waiver.py --task <T> --stage S5 --block "not collected by pytest"`
   — and `REPAIR_MARKER`.
   test: the same table as item 2, rows E4b, E5c, E12 | expected from: FR-1, FR-2, FR-57, §0 fact 10

4. **The joint and its census.** `references/stage-joints.json`: row `manifest_put:node_id`, stages `["S5"]`,
   requirement "A hand-written `tests[]` `instance_id` is the id pytest collects in the row's `file`; where no collect
   answers, the row is stored marked `not_verified`.", door "send the collected id (the refusal lists the nearest), or
   the class path `<Class>::<function>`", `door_needs`/`when`/`producers` in the form of `manifest_put:probe_owed`
   (role `qa-automator`, field "the manifest fragment sent to manifest_put.py", told page). The K1 pin of
   `test_stage_joints.py:76`: count +1 with the reason "+1 manifest_put:node_id (RD1-19)". `driver-exits/s5.json`: row
   `manifest_put:node_id` `reach: unwalked`, `why_unreached` as its neighbours, `ratchet.unwalked` +1 with a `raised_by`
   line "unwalked | joints/manifest_put:node_id | RD1-19, <date>". `judgment-census.json`: the `stamp_node_ids` row of §1.
   test: `scripts/tests/test_stage_joints.py` K1/K4 (existing pins) and `dry_exits.py --check` | expected from: axis 38,
   §0 fact 9, AR-20 (the raise named)

5. **The contract sentence.** `references/artifact-contract-automation.md` § Instance identity (:43-48), one sentence: a
   hand-written id is resolved through the project's pytest collect when `manifest_put.py` stores it — rewritten to the
   collected spelling with `node_id_check.asked` keeping yours, or stored with `node_id_check.status: not_verified` and the
   reason when no collect answers; the field is the code's, no gate reads it. Then
   `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`; the report lists the slice files it changed
   (expected: the three in owns; any other changed file -> stop, "needed beyond the manifest").
   test: none -- document text; its witness is `contract_slices.py --check` and the DOC-DISPATCH key run is not owed
   (a generated-slice check exists) | expected from: AR-10, FR-38, axis 5

---

## §3 Edges, each with the invariant it protects

- **E1 — no collect possible** (no pytest-shaped command; `verify_node_ids: false`; command not startable; collect
  exit error; unreadable output; not a pytest command; an import of `node_ids`/`gate_preflight`/`config_contract`
  fails; any exception in the call) -> the row is stored with the typed id and `node_id_check.status: not_verified`
  plus the reason; exit 0; one printed line. INVARIANT: an id nobody checked is never stored as `verified`, never
  refused, and never reported `missing` (FR-2, FR-41, FR-59).
- **E2 — the limit** `execution.node_id_collect_timeout_s` (default 180; a non-number, a bool, `<= 0` -> 180, C4); a
  collect that runs past it is stopped by `node_ids` (`kill_tree`) -> E1 with the timeout named. INVARIANT: one
  `manifest_put` call waits at most one bounded collect, and never while holding the story lock (P1). Case AT the
  limit: not owed — an internal boundary with no input from outside (TESTING «Строка теста», CLAUDE rule 11).
- **E3 — the id string is a role's output** (internal): no adversarial battery.
- **E4 — a parametrised id.** (a) `test_x[eu]` collected as `test_x[chromium-eu]` -> stored `test_x[chromium-eu]`, mark
  `verified`, `asked: test_x[eu]`, every carrier of the fragment rewritten, one note. (b) collected
  `[chromium-eu]` and `[firefox-eu]` -> `missing` (node_ids, two candidates) -> refusal naming both. INVARIANT: a rewrite
  only to a spelling `node_ids` resolved; two candidates are never chosen between by code.
- **E5 — a class method.** (a) typed `test_y`, one class defines it -> `verified`, stored `test_y` (the class is not
  added). (b) typed `TestA::test_y` -> asked as typed, `verified`, stored as typed. (c) typed `test_y`, two classes ->
  refusal whose door names `<Class>::test_y`. INVARIANT: the class step never crosses files or function names, and the
  manifest's own spelling rule is not changed by the store.
- **E6 — a path with spaces** (`tests/my dir/test_a.py`, also typed with `\`) -> one argv token, no shell; slashes
  normalized for the ask only; the stored `file` is the role's, untouched. INVARIANT: a path is never split at a space,
  and `stamp_node_ids` never rewrites `file`.
- **E7 — the file yielded no test in this collect** (the file does not exist, is not a Python file, is deselected, its
  folder failed) -> `not_verified` "file <f> yielded no test in this collect". INVARIANT: "missing" (and so a refusal) is
  said only about an id whose file yielded at least one collected test in this very collect (node_ids' direction).
- **E8 — the author's spelling re-sent after a rewrite** (a patch, a then-binding, an obligation binding in a later
  fragment) -> mapped to the stored id from `node_id_check.asked`, no collect. INVARIANT: a re-sent author spelling never
  creates a second row beside its resolved one, and never a binding that joins nothing.
- **E9 — rows not asked:** writer rows (`WRITER_MARK`), patch rows with no `file`, rows whose spelling is already stored,
  rows with no explicit `instance_id` (a derived id is not a pytest spelling) -> no collect, no mark change. A stored
  `not_verified` row re-sent WITH `file` is asked again. INVARIANT: the stored mark changes only by a new answer of the
  collect; `not_verified` has a way out (FR-40).
- **E10 — a role-sent `node_id_check`** -> removed, one note. INVARIANT: the mark is the code's alone (AR-14).
- **E11 — nothing to ask** (no `tests[]`, an empty list, only ineligible rows) -> fragment unchanged, no subprocess.
  INVARIANT: a fragment with nothing to ask never starts a process.
- **E12 — a `missing` id the person's recorded S5 word covers** -> stored, `passed_by_person`, the words in `note`.
  INVARIANT: the person's word passes the gate (P13) by the existing road; FL1 adds no matching of its own.
- **E13 — a rewrite makes two rows one id** -> the existing `_refuse_colliding_ids`/`validate` refuses (they read the
  rewritten fragment). INVARIANT: every merge refusal reads the rows as they will be stored (P2).
- **E14 — the replay** (`merge`, `fold`, `--recover`, `_seed_from_legacy` on replay) never collects. INVARIANT: a
  replayed event folds to the mark it was committed with.
- **E15 — conflicting requirements.** FR-16 (resolve at store) vs AR-12 (a collect per call): resolved by E9 + one ask
  per call + E2. "Never a refusal" for no collect vs the refusal on `missing`: separated by E7's invariant.
- **E16 — an old manifest** (rows stored before this change): no mark, read as "not asked"; no migration, no retro-collect.

Positional (rule 11 (ii)) — the call sits after the last pure refusal and before `stamp_provisional`:
- P1 — the collect runs before `store.commit` takes the story lock and before `fold(store.read())`: a minute-long collect
  never blocks another writer of the story.
- P2 — `fragment_key = content_hash(fragment)` and `validate`/`_refuse_unmergeable` see the stamped fragment: the receipt
  is the hash of the bytes stored, and collisions created by a rewrite are refused.
- P3 — every cheaper shape refusal before it (retract, claim pairs, novelty, base_outcome, obligation ids, expectation
  changes, obligation refs and hash, critic approval, probe_owed, assertion line, then remainder, unresolved reasons)
  still refuses first: no collect is spent on a fragment those refuse.

Temporal (rule 11 (i)) — T1: before this change no stored row carries `node_id_check` and no joint `manifest_put:node_id`
exists; after it, new hand rows carry the mark. Item 2 creates the field, item 4 the joint. Readers of both worlds treat
an absent mark as "not asked".

Error direction of the reused function in a more consequential role (`node_ids.check_request`, advice -> the input of a
store refusal): it may err toward `not_verified` (under-refusing), never toward `missing` for an id whose file did not
collect, and never toward `verified` without a collected match. Adversarial inputs that must stay on the safe side: class
methods (bare and typed), parametrised ids with a plugin prefix, two-browser params, a partial collect, a file that
yielded nothing, a non-Python file, a legacy `TC-n::` prefix, a path with spaces or backslashes, a derived id with a dict
parameter, a conftest that sleeps past the limit.

---

## §4 Readers of every touched file (rule 7)

The `owns_readers.py` block was NOT attached to the brief: the plan critic runs
`python -B tools/owns_readers.py --paths <owns> --names stamp_node_ids,match,node_id_check,manifest_put:node_id` (Q13 (d)).
The hand reading below covers the names this card changes; each line says unchanged / changes here.

- `manifest_put.py::run` — production callers: `manifest_from_tests.py:1957-1963` (writer rows carry `WRITER_MARK`:
  not asked — unchanged), `planning_contract.py:2607-2611` (`{"unresolved": rows}` only: no `tests[]` — unchanged);
  `outcome` importers `migrate_artifacts.py:105`, `window_record.py:2166`, `probe_by_code.py:7647`,
  `planning_contract.py:3881`, `story_step.py:2943` — unchanged (`outcome` untouched); `s5_precheck.py:1271` (`import
  manifest_put as MP`) — unchanged. Test importers (28 files by the Grep `import manifest_put` over `scripts/tests/`):
  a test that sends hand `tests[]` rows through `run` in a project whose config sets a pytest-shaped
  `test_command_templates` now starts a collect; the harness sets none (Grep `test_command_templates` in
  `tests/harness.py`: 0 hits; positive control: `config.json|tests_root` in the same file: 6 hits) and the template ships
  them empty -> E1 with no subprocess. The `--witness-for` block names the ones to run; any that slows -> report line.
- `node_ids.py::match` (item 1) — callers: `run_suite.py:1755` (`_checked_by_the_first_collect`) and `:1845` via
  `check_request` — changes: a class method asked bare now resolves and runs instead of `node_id_mismatch` exit 2;
  `red_sandbox.py:255` — changes the same way (re-pinned instead of `NodeIdMismatch`); `manifest_from_tests.py:1840` —
  changes: its latent class-method refusal (§0 fact 6) goes; its back-spelling `rsplit("::",1)[-1]` gives the bare
  function, the manifest's own spelling — unchanged otherwise; `judge_form` through `_judged` — unchanged (only
  `missing` flows there); `match_partial` calls `match` for listed ids — inherits the step. Tests pinning `match`:
  `test_judge_form.py:84-218`, `test_node_ids.py`, `test_red_sandbox_node_ids.py`, `test_run_suite_mine.py` — unchanged
  unless one pins a bare class-method `missing` (the walk runs them; a red pin there is a report line, not a fix outside
  owns).
- `references/stage-joints.json` — readers `stage_joints.py`, `dry_exits.scan_joints` via `null_outcomes.load_data`,
  `test_stage_joints.py` (K1 pin, K4) — changes here (item 4). Parallel stream: RD1-34 (rules-debt/1, `ожидает`) adds
  `manifest_put:claim_then_pairs` to the same file and moves the same K1 pin (and owes the same axis-38 row): see §5.
- `scripts/tests/fixtures/driver-exits/s5.json` — reader `dry_exits.py --check` — changes here (item 4); RD1-34 will touch
  it too if it honours axis 38 (its owns, read today, do not name it — a note for the Lead).
- `judgment-census.json` — reader `test_judgment_census.py` — changes here (one row).
- `test_stage_joints.py` — the K1 pin line only — changes here and in RD1-34.
- `references/artifact-contract-automation.md` and its slices — readers `contract_slices.py` (`--check`),
  `inject_context.py`, `stage_joints.py` (direction C: a demanded token named in a file the role receives),
  `test_contract_slices.py` — changes here (one sentence + regenerated slices).
- `tools/controller-blocks-gen.py:138,190-193` reads `manifest_put` routes (phase-2 spec readers table :1792) —
  unchanged (no block route text changes).
- `test-layers.json` — reader `tools/test_quarantine.py`, the canon's `unlisted:`/covers check — changes only if a covers
  drift is reported for the two rows named.

---

## §5 Queue and taken batches (the brief's check)

- `onboarding-forge/1` (taken, «в работе», dev1): its one row writing `scripts/manifest_put.py` is PC1-3 —
  `отклонено — перенос в 0.11.0` (`batch-1-onboarding-roles-forge.md:50`, «Остатки» :93). Not open: does not block.
  Observation (another pile's zone): the transfer reads «перенос: пачка 2», but `onboarding-forge/2` carries no D5-F /
  B-333 / `os.replace` row (Grep over `plans/piles/onboarding-forge/`: hits only in batch 1 and the README) — fork F9.
- `onboarding-forge/2` (taken, «в работе», dev1): its only `manifest_put` mention is the transfer row of RC1-10 to
  OF5-11 (`batch-2-onboarding-roles-forge-p3.md:103`), and OF5-11 is `принято: b6cbc76 (t-507)`
  (`batch-5-ostatki-hf8-4-i-oh3-42.md:38`). No open row writes `manifest_put.py`: does not block. (Positive control: the
  same Grep for `manifest_put` found that row in that file.)
- `thinking-roles/6` TR4-17 (`ожидает`, batch not taken): writes `manifest_put.py` (`assertion_line_problems` region, item
  1 of its finding) and probably `test_manifest_put_assertion_line.py`. A batch not taken holds no zone; but the rules-debt
  batch's own brief says "RD1-19 (FL1) после thinking-roles/6 TR4-17" (`batch-1-phase-2.md:18`) — fork F7.
- `rules-debt/1` RD1-34 (`ожидает`): same `stage-joints.json`, same K1 pin; one stream at a time, or the later node merges
  `main` and sets the pin to the sum (PROJECT «Командная работа» п. 3). C3-b1 owns `manifest_put.CRITIC_FIELDS`:
  function-disjoint with `stamp_node_ids` and the call site (spec :1486).

---

## §6 Forks (returned; recommendation first)

- **F1 — what happens to an id pytest does NOT collect, when its file did collect.** (a) refuse before the commit with
  the nearest ids and the doors of item 3, the person's word passing it (sibling parity: the writer and the sandbox both
  refuse; the TP1-15045 defect was exactly such an id stored); cost: one joint row, the K1 pin, one dry-census row and
  ratchet raise, a collision with RD1-34 on two files. (b) store it `not_verified` with the nearest ids in `note` — no
  new refusal, no joint, no collision, but the store keeps an id that joins nothing, which is the defect FR-16 names.
  Recommendation (a). Under (b): item 3's refusal, item 4 and E4b/E5c/E12 drop; F2 loses its urgency.
- **F2 — the class-method edge.** (a) fix it in the survivor (`node_ids.match`, item 1): every caller gains it (the
  runner and the sandbox stop refusing a bare class-method id; the writer's latent defect goes); a meaning change of a
  shared function, with its error direction and adversarial inputs stated. (b) leave `node_ids` alone; the store demotes
  every `missing` to `not_verified` (= F1 (b)). (c) a second matcher in `manifest_put` — rejected (AR-15). Recommendation
  (a). Under (b): item 1 drops, `node_ids.py` and `test_node_ids.py` leave owns.
- **F3 — where the collect command comes from.** (a) `gate_preflight.collect_base(config)` (the gate's reader of the
  project command, the same collect S5 is rehearsed with), cwd = project root (the rows' `file` is project-root
  relative, §0 fact 8), lazily imported — any import failure is E1. (b) a CLI flag `--collect -- <cmd>` like the writer:
  opt-in, so the hand path stays unresolved unless the role remembers — FR-16 not met by default. (c) a `collect` block
  in the fragment (the sandbox's form): the role supplies the command. Recommendation (a). Note for the Lead: the gate
  runs the same command with cwd = `tests_root` (`gate_preflight.py:2937-2964`); the store uses the project root
  because the ids it checks are spelled from there.
- **F4 — one road with the writer (P31, rule 6).** (a) this card resolves hand rows only (`WRITER_MARK` rows skipped),
  and a NAMED node RD1-19b in rules-debt/1 makes `stamp_node_ids` the one resolver of every `tests[]` row at store:
  `manifest_from_tests.resolve_through_pytest` reduced to it (or `--collect` kept as an early dry check only), writer rows
  without `--collect` resolved at store, the copied-`generated_from` loophole closed; owns
  `scripts/manifest_from_tests.py`, its keep test row, the automator text naming `--collect`; until then two code paths
  assemble an ask (~15 lines, a clone the ratchet may name). (b) do all of it in this card (owns +3 files, the writer's
  behaviour change measured in the same round). Recommendation (a) with RD1-19b opened in the same move (a slice is no
  exclusion when the rest is a named node, rule 6). Residual until RD1-19b: a hand row that copied `generated_from` is
  read as the writer's and not asked.
- **F5 — the reader of `node_id_check.status`.** (a) declared terminal in the artifact contract (role and critic read
  it; the run itself proves the join at S6), plus the printed line now. (b) `s5_precheck` names `not_verified` rows as
  ADVICE at hand-off (a slow-tested file, a new node). Recommendation (a); (b) if the Lead wants a stage-exit reader, as
  a later node.
- **F6 — runners with no node-id checker (P31, axis 3).** Every row takes the same road; the road can verify only where
  the runner has a checker (pytest today; `collect_forms[].node_ids` is the capability key `run_suite._runner_without_node_ids`
  already reads). For other runners the store says `not_verified` and why — no exclusion in the code path, but the
  left-out side gets no resolution. Covering it costs a node-id checker per runner row (jest, JUnit, NUnit...), a
  universality-pile node. Recommendation: accept this card on the shared road, and the Lead opens (or confirms) a node in
  the universality pile for checkers by capability key — a residual of this class is a node with owns, not a line.
- **F7 — the batch's order "RD1-19 after TR4-17".** (a) drop the wait: TR4-17's batch is not taken, its manifest_put item
  is function-disjoint (`assertion_line_problems` vs `stamp_node_ids`), the later node merges `main` (PROJECT п. 3); the
  Lead edits the batch line. (b) keep it: RD1-19 waits for a batch nobody took. Recommendation (a).
- **F8 — a SIBLING_MAP axis for the node-id survivor.** `node_ids` has no axis (Grep `node_ids` in `docs/SIBLING_MAP.md`:
  0 hits; control: the same Grep finds it in `design/architecture.md:218`); AR-15's change check asks a survivor to have
  one. (a) the Lead adds "axis 39 — one node-id resolver `node_ids` <-> its five sites (runner, sandbox, probe, writer,
  store)" in the acceptance commit; (b) leave it. Recommendation (a) (a Lead file, not the builder's).
- **F9 — another pile's zone, a finding offered:** `onboarding-forge/1` «Остатки» PC1-3 transfers to «пачка 2», where no
  node carries it. Offer: the Lead tells that batch's Lead (same developer) or writes a finding in onboarding-forge. Not
  this card's work.

---

## §7 Small choices closed by the designer

- C1 — function name `stamp_node_ids`, the `stamp_provisional` shape (copy in, copy + lines out); the refusal stays in
  `run` so the new unit is not a refusal site itself (no new blocking unit for `blocking_per_role`).
- C2 — field `node_id_check` with statuses `verified` / `not_verified` / `passed_by_person` — the words `red_sandbox`
  already records for the same fact (`node_id_check.status`, :281), not a new vocabulary; `note` one line; `asked` only on
  a rewrite.
- C3 — one ask per call over every eligible row and file (one collect, `check_request` passes only the named files).
- C4 — timeout and switch read like `run_suite._setting` (effective config); bad values fall back to the template default.
- C5 — the carriers rewritten are those the merge reads by instance id (`tests`, `then_bindings`, `obligation_bindings`,
  `unresolved`); `retracted_instances` is not rewritten (it names stored rows by their stored spelling).
- C6 — `node_id_check` is optional: no `null-outcomes.json` row, not added to `window_record.REQUIRED_ROW_FIELDS`.
- C7 — a role-sent `node_id_check` is dropped with a line, not refused (the `home_hash` precedent; a refusal would punish
  the common copy-a-stored-row-and-patch move).
- C8 — the test home is `test_manifest_put_assertion_line.py` (keep, `data_join`: the same shape — `manifest_put` joins a
  row field against a tool, the unknowns are notes), never a new file; `test_node_ids.py` (keep, `gate_named`) for item 1.
  If `--witness-for` names another keep file judging `manifest_put.run` as the closer home, the builder uses it and says so.

---

## §8 Reading trail

Read: phase-2 cards spec :1460-1540 (FL1, FL9, S1b), :112, :1571, :1597, :1621-1625, :1654, :1792, :1859 (Grep `FL1`);
the finding (whole); parent spec :533-540 and Grep `F-L1`; `factory-rules.md` :246-305 (FR-16, FR-17, FR-18, FR-40, FR-58,
FR-59); `architecture.md` :33-107 (§ A, AR-1-AR-3), :173-220 (AR-29, AR-13-AR-15), :274-287 (AR-22, AR-23), :316-321
(AR-28); `manifest_put.py` :1-130, :183-232, :830-869, :1051-1062, :2482-2706, Grep of every `def`/constant, of
`WRITER_MARK`, of `"instance_id(s)"`; `node_ids.py` :1-36, :116-165, :296-313, :502-793, Grep of every `def`;
`manifest_from_tests.py` :320-349, :1800-1978, Grep `generated_from`, `ClassDef`, `relative_to`; `run_suite.py`
:1446-1454, :1681-1860; `red_sandbox.py` :214-282; `gate_preflight.py` :436-485, :2925-2974; `contract.py` Grep of
`instance_id`, `function_name`, `test_instance_id`, `INSTANCE_SEP`; `planning_contract.py` :2596-2615; `hooklib.py`
:971-975; `references/artifact-contract-automation.md` :1-52; `references/templates/config.json` Grep (`:17-21`, `:125`);
`references/stage-joints.json` Grep `manifest_put` (:3431-3510); `driver-exits/s5.json` Grep (:218-221, :333-362);
`told-ratchet.json` :331-333; `judgment-census.json` Grep `manifest_put` (:604-624); `test_stage_joints.py` :10, :76,
:113-115, :726-738; `test_judgment_census.py` :366-385, Grep `blocking_per_role`; `test-layers.json` :2960-3009,
:3374-3389, Grep; `docs/TESTING.md` :75-152, :204-233; `docs/SIBLING_MAP.md` headings, axes 7, 23, 30, 34, 38; batches
`rules-debt/batch-1-phase-2.md` :1-20, :47, :62; `onboarding-forge` batch 1 :1-4, Grep; batch 2 :1-12, :103; batch 5 :38;
`thinking-roles` Grep `TR4-17`, finding `20261111-proby-ostatki-cepochki.md:17`.
Not run: any test, any git command (no shell). Not read: `owns_readers.py` output (not attached; §4).
Needed beyond the manifest: none to write; read beyond the given list as the trail shows.

## Lead decisions (Lead, 17.11.2026, Opus; «решила сама»)

F1-F9 = the designer's recommendations: F1 (a) refuse before the commit; F2 (a) the class step in `node_ids.match`; F3 (a)
`gate_preflight.collect_base(config)`; F4 (a) hand rows only, node RD1-19b opened in the same move as acceptance; F5 (a)
`node_id_check.status` terminal in the artifact contract; F6 accepted on the shared road, the universality-pile node is a
Lead debt for this session; F7 (a) the wait on TR4-17 is dropped (its batch is not taken); F8 (a) a SIBLING_MAP axis for the
node-id survivor, added by the Lead with the acceptance commit of the code; F9 the finding goes to onboarding-forge as a
transfer line. critic on this plan: skipped -- every fork follows the recommendation, no field changes meaning (F1 adds a
refusal the spec of FL1 already asks for); the code gets the topic critic. The builder starts after a writer slot frees.

- Node id (Lead, 17.11.2026): the node opened for F4 is **RD1-35** in `plans/piles/rules-debt/batch-1-phase-2.md` (RD1-19b broke the id form `<initials><N>-<n>`, `tools/test_pile_cards_contents.py`; main canon 44161711037 red).
