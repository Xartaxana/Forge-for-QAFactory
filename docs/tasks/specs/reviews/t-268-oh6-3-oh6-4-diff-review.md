# t-268 — critic diff review, topic onboarding-hooks/6: OH6-3 (wip/oh6-3 fd1aeac) and OH6-4 (wip/oh6-4 15469d1)

Critic (Opus), 13.11.2026. One pass for the topic (R13-g). Base: `origin/wip/oh6-5` 5e2af3e. Spec:
`docs/tasks/specs/t-263-oh6-3-oh6-4.md` (Part A, Part B, the Coordinator decision: F-0 (b), F-6 (a)). The worktrees
`.claude/worktrees/oh6-3` and `oh6-4` are checked out at fd1aeac / 15469d1 (`git rev-parse HEAD`). This verdict is input
to acceptance. Accepting the work is the coordinator's call.

## Verdict

- **OH6-3: fix round, 1 item (A-1). Nothing blocks on correctness.**
- **OH6-4: fix round, 2 items (B-1, B-2). Nothing blocks on correctness. One proposed node (P-1) goes to the coordinator.**
- **Merge: clean.** `git merge-tree` reports no conflict at all, and the narrow tests pass on the merged tree (Q5).
- Blocking findings: 0.

## Fix items

**A-1 (OH6-3, fix before merge, cheap).** Location: `scripts/tests/test_event_store.py:274-343` (`test_publish_temp_name_table`).
- Problem: the rows E-1, E-2a, E-2b, E-2c, E-3 and E-4 run as plain sequential asserts with no `subTest`. Spec §A.3 asks for
  "subTest per row id", and P29 says independent checks must not stop one another.
- Effect: the first red row hides the rest. That is why the attached red control (r1, `TEMP_NAME_HEX=32`) can only show
  E-1. Spec §A.3 says r1 turns E-1, E-3 and A1 red, but E-3 never runs once E-1 fails.
- Also: E-3 and E-4 take `suffix` from E-1's recorded name, so even with subTests they depend on E-1.
- Fix:
  - wrap each row in `with self.subTest(row=...)`;
  - get E-3/E-4's suffix from a separate publish, or as `"." + "0"*event_store.TEMP_NAME_HEX + ".tmp"` checked against
    the recorded name;
  - re-run r1 and quote E-1 and E-3 both red.

**B-1 (OH6-4, fix before merge, cheap; the spec's defect, not the builder's).** Location:
`scripts/tests/test_doctor_context.py:530-535` (`test_one_a24_row_per_native_refusal` parts (c) and (d)).
- (d) patches `RR.SCANNED` and expects the entries to show up as stale. That is a "negative control inside a test", a row of
  the `docs/TESTING.md:98` table «Что не пишется, а найденное — удаляется». That table says to delete it ("найденное —
  удаляется"). The red control r2 already proves the scan is real, outside the test.
- (c) `RR.findings(PLUGIN_ROOT) == []` repeats `test_refusal_registry.py:70` ("the shipped package has no unregistered
  refusal") word for word.
- Spec §B.3 (c)/(d) prescribed both, so the builder followed the spec. Fix: drop (c) and (d) and keep (a)/(b). Those are the
  junction of the three NC rows: each entry covers exactly one live site in `native_context.stage`.

**B-2 (OH6-4, fix before merge, trivial; code quality, brief item 7).** Location: `test_doctor_context.py:456`.
- Problem: `tearDown_story` reads like a unittest lifecycle hook. It actually runs at the START of each row (`:438`) and
  resets state, so the name says the wrong thing.
- Fix: rename it to `reset_story_state` or similar.

**P-1 (proposed node for the coordinator; not a fix of this round).**
- Problem: `inject_context.refuse_native_packet` (`inject_context.py:505`, unchanged by the diff) always writes a NAMED row.
  Suppose `native_context.stage` raises an `OSError` while a packet of the same key is pending. That `OSError` can come from
  the pending read `path.read_text` (`native_context.py:187`) or from a `LockBroken` at the lock's open stage
  (`event_store.py:556-559`). The refusal then writes a named row, and `recover` may close the live pending launch on it.
- This is the same class as OH6-4's B.4 conflict ("a launch pending under the refused key is never closed as `never_started`
  on this hook's row"). Spec §B.2's siblings line marked `refuse_native_packet` n/a because "already writes the row", so the
  pending case was never asked.
- The trigger is rare.
- Proposed direction: `note_denial(..., name_dispatch=not native_context.launch_pending(root, session, task_name))` in
  `refuse_native_packet`, plus one table row.
- Owner: the coordinator opens it as a node (in OH6-4's fix round, or onboarding-hooks batch-7). Deciding which belongs to
  the tier above.

## Q1. OH6-3 `event_store._publish`

- **Positional invariant holds.** Traced `event_store.py:172-193` on fd1aeac:
  - the `for` loop opens with `"x"` and catches only `FileExistsError`;
  - on the 8th attempt it `raise`s (`attempt == TEMP_NAME_ATTEMPTS`);
  - otherwise it `continue`s without touching `tmp`;
  - `break` happens only after a successful open;
  - the `try/finally: tmp.unlink` begins after the loop, so `tmp` and `stream` are always the names this writer created.
- A `PermissionError` (delete-pending) is not caught, so it is raised at once. `stream` is never unbound: the loop either
  breaks with it bound or raises.
- E-2a/E-2b/E-2c cover a collision (the other writer's `b"other"` stays), the 8th attempt AT, and BEYOND: `FileExistsError`,
  target absent, 8 temps byte-identical, no extra `.tmp`.
- r2 (`"w"`) giving ERROR is consistent with the trace: `"w"` overwrites `aaaaaaaa`, then replaces it into the target, so the
  later `read_bytes` of the temp raises `FileNotFoundError`.
- **Callers relying on the old behaviour: none found.**
  - Grep `\{32\}.{0,4}tmp|glob\([^)]*tmp|endswith\(.\.tmp|\*\.tmp|uuid4\(\)\.hex.{0,20}tmp` (case-insensitive) over
    `scripts/`.
  - Every consumer is an emptiness check: `glob("*.tmp") == []` or `endswith(".tmp")` in about 20 tests. Plus
    `test_config_view.py:268`, which checks only the `t.txt.` prefix, the `.tmp` suffix and uniqueness.
  - Nothing keys on the length. Positive control: the same grep hit the known `factory_dashboard.py:4170` and
    `migrate_coverage.py:25`.
  - Over `tools/`, `experiments/` and `scripts/`, the only length-aware reader is `driver-golden-rules.json` N8a. Control: the
    same grep hits main's N8a, the line this diff changes.
- No test patches `event_store.uuid`, `Path.open` or `builtins.open` (grep `patch\([^)]*uuid|event_store\.uuid|Path\.open|builtins\.open`).

## Q2. OH6-3 numbers

- `\qa-factory\state\native-context\` is 1+10+1+5+1+14+1 = 33, and 33+32+1+32+5+13 = 116, so 259-116 = **143**.
- The binding path (`host_dispatch.py:10-11`, `qa-factory/state/host-dispatches/<sha256 64>.json`): `\qa-factory\state\host-dispatches\`
  is 34, and 34+64+5+13 = **116**. Correct.
- `TEMP_NAME_EXTRA = len('.') + TEMP_NAME_HEX + len('.tmp')` is derived from the imported `event_store.TEMP_NAME_HEX`
  (`native_context.py:8,20`): AR-13 holds. The limits stay literal and are pinned by A1/E-3 (C-A2).
- **N8a vs N24 order.** N8a is row 35 and N24 row 54 of the fixture. `driver_trace.compiled_rows` (`:163-167`) builds
  `[_Row(r) for r in rules["rows"]]` in file order, and `Registry.normalise` (`:281-282`) applies rows in that order. So an
  all-digit 8-hex token goes to N8a first. The 8-digit pid residual is accepted in the spec (§A.4).
- Alternation: for a 32-hex name, `{8}` fails at `\.tmp` and backtracks to `{32}`. A 31/33-hex name or a 9-digit name cannot
  match `{8}`, because `\.` must sit directly before the 8 and `\.tmp` directly after.
- **The quarantined `test_driver_golden.py` stays consistent** (read, not run):
  - `:51` 32 hex AT gives `<UUID-1>` (kept by the `{32}` branch);
  - `:53-54` 31/33 hex are kept;
  - `:115-116` `x.4321.tmp` is a pid;
  - `:135-136` `.15820.tmp` is `<PID>`, and `.123456789.tmp` (9 digits) is kept.
- The other changed constants are all moved: test pins A1/A2/A4/A5 and both changelog fragments (FR-10: oh3-36 now says 143).

## Q3. OH6-4 semantics

- **FR-12.** `refuse_native_stage` (`inject_context.py:509-522`) decides `named` from `isinstance(exc, StateConflict)` and
  `native_context.launch_pending(...)` only. No message text is read.
- `launch_pending` (`native_context.py:94-108`) keys on the same `(session_id, raw task_name)` through the same `_slot` as
  `stage` (`:174-185`). Its error direction is right:
  - an exception, a non-object or undecodable file all answer True;
  - an empty session or an absent file answers False.
- **`recover` never closes a pending launch from an inert row.** Every reader of `DENIALS_FILE` goes through
  `Controller._denial_times` (`controller.py:7739`; `_denied` at `:7838-7842`; `launch_card` evidence at `:8700-8713`). Grep
  `DENIALS_FILE|dispatch-denials` over scripts: the only other writers are `worker_lifecycle.py:132` and `stage_guard`'s
  comment. An inert row has `dispatch_id` None, so it skips `:7752`. Its `stage` is None, so it fails `:7755-7756`, which
  needs `role and stage` and an equal stage. The row belongs to no dispatch. B-3..B-6b prove it with the real reader.
- **Refusal outcomes byte-unchanged.**
  - The native branch still prints `'INJECT: ' + str(exc)` and exits 2.
  - `check_override` (`:670-672`) and `rewritten_input` (`:737-739`) print `str(exc)`, then call the best-effort `note_denial`
    (`try/except Exception: pass`, `:319-340`), then exit 2.
  - `ticket` is bound at both sites (`:631`).
  - B-1..B-9 assert stderr byte-equal and exit 2.
- **The A24 key** `block(NATIVE_PACKET_UNWRITTEN.format(**parts))` (`:506`) is untouched. The diff hunk around `refuse_native_packet`
  only adds lines after it.
- **The registry rows (form D)** key on the literal prefixes "Native context exceeds", "Native context requires host session" and
  "A factory launch is awaiting SubagentStart" of the raises at `native_context.py:173,176,188`. `StateConflict` is in
  `REFUSAL_RAISES`. Control rerun: `refusal_registry.py --check` exits 0 and lists the three NC entries.
- The sweep of the artifact (every `sys.exit(2)`/`block(` in `inject_context.py`) is complete: `:455-456`, `:505-506`, `:521-522`,
  `:671-672`, `:683-684` and `:738-739` all write a row. The pending case of the packet refusal is P-1.

## Q4. Census (axis 18, brief item 9; named row by row)

`judgment-census.json` `ratchet.blocking_per_role`, +1 each, reason: the new blocking unit `inject_context.refuse_native_stage`
(OH6-4, a silent denial-less refusal given a denial row):

| role | old → new |
|---|---|
| qa-automator | 168 → 169 |
| qa-bug-reporter | 134 → 135 |
| qa-case-critic | 159 → 160 |
| qa-case-designer | 134 → 135 |
| qa-code-critic | 133 → 134 |
| qa-doc-scribe | 134 → 135 |
| qa-failure-analyst | 135 → 136 |
| qa-requirements-tester | 152 → 153 |
| qa-retro-analyst | 134 → 135 |
| qa-runner | 135 → 136 |
| qa-scout | 134 → 135 |
| qa-test-strategist | 166 → 167 |
| conductor | 473 → 474 |

- The 13 roles equal the new row's `roles`, which are those of `refuse_native_packet`.
- No other ratchet key moved (the diff line shows only `blocking_per_role` values changed). The commit message names every key
  under `architecture: AR-20`.
- Why `native_context.py::stage` did not add another +1: `units_of` reads `refusal_registry.sites(files=all trees)`
  (`test_judgment_census.py:209`), independent of `SCANNED`. So `stage` was already a u3 blocking unit. The density check
  (`compare`, `:368-376`) demands equality, and the rerun is green.
- The row gains `ref: A24:NC-*`, and its class stays `shape`. JUDGMENT (item 11): no class lowered, no `blocks_override`, no
  edit to the scan constants. `judgment: adds data check` is honest, because the check judges an exception type and the
  presence of a file.

## Q5. Merging the two branches

- `git merge-tree --write-tree --name-only origin/wip/oh6-3 origin/wip/oh6-4` gives tree 21cd5f8, rc=0, with **no conflicted
  files**. The coordinator expected "resolves the two files". In fact the hunks are disjoint:
  - `native_context.py`: constants `:8-27` vs a new function after `pending_path`;
  - `test_doctor_context.py`: `PacketNameLength` `:169-275` vs a new class after `:332`.
- No semantic interaction:
  - `launch_pending` reads `_slot` (packet name, `NAME_HEX`), never the temp suffix;
  - OH6-4's tests stage under a short temp root through `atomic_json`, which now uses the `"x"` mode.
- On the merged tree, extracted with `git archive` into the scratchpad:
  - `test_doctor_context.py -k "NativeStageRefusal or PacketNameLength"`: 11 passed, 35 subtests;
  - `test_event_store.py -k temp_name`: 1 passed;
  - `refusal_registry.py --check`: exit 0.
- The integrator can merge mechanically.

## Q6. Class completeness (SIBLING_MAP)

- Axis 18: the census raise is named above.
- Axis 29: `note_denial`'s `open("a")` is pre-existing and not touched.
- Axis 34 (one road), brief item 12: F-6 put `check_override`/`rewritten_input` on the same denial road. All six refusal exits of
  `inject_context` now write a row. None found beyond P-1. Grep: `sys.exit(2)|block(|deny(|note_denial(` in `inject_context.py`.
- Axis 32 (judgment): covered by Q4.
- Residuals already filed in `batch-7-ostatki-t-263.md` on origin/main are not re-raised:
  - OH7-1: the 32-hex publishers;
  - OH7-2: A24 rows for `check_override`/`rewritten_input`;
  - OH7-3: non-dict pending, `AttributeError`;
  - OH7-4: the pending door;
  - OH7-5.
- New: P-1.

## Standing lines

- **Fit to spec:** both diffs follow the spec, with these exceptions: A-1 (no subTest) and B-1 (a spec defect).
- **Builder decisions:**
  - OH6-4 added row B-6b (a list pending file gives an inert row, safe side);
  - `test_launch_pending_table` (absent / no session / other key / delivered / undecodable / raising) adds rows the spec did not
    ask for;
  - both are in the safe direction.
- **Seams:** additive. `note_denial`'s new kwarg defaults to the old behaviour.
- **DUPLICATION AND CONSISTENCY:**
  - `raw = (event.get("_qa_host") or {}).get("input") or {}` now has a third copy (`inject_context.py:481,515`,
    `native_context.py:177`). It is a pre-existing pattern and not material.
  - B-1(c) duplicates `test_refusal_registry.py:70`.
  - Otherwise none found. Grepped: `launch_pending|pending_path|_session_packets` (the one packet reader family in
    `native_context`), `note_denial(` (one writer), `_temp_token|uuid4().hex` (one temp-name producer, plus OH7-1).
- **CODE QUALITY:** new functions are short: `_publish` 22 lines, `refuse_native_stage` 14, `launch_pending` 15. No nesting
  beyond 3. B-2 is the naming finding. No dead branches.
- **ARCHITECTURE:**
  - OH6-3 names AR-4/13/14/20/22, and the walk is done: producer = the temp name; readers = N8a and `TEMP_NAME_EXTRA`, all
    changed in one commit.
  - OH6-4 names AR-9/13/18/20/25/28. Its single-reader claim was verified (Q3).
  - Not named but touched: none found.
  - Observation: OH6-4's `axes:` line says "not a mechanism". The diff does alter a machine check (`SCANNED`, three registry
    rows). That is rule 10 recognition, but package commits are gated by `architecture_gate`, not `mechanism_gate`. Not a
    finding against the builder; noted for the coordinator.
- **JUDGMENT:**
  - OH6-3: `judgment: none` is correct.
  - OH6-4: `adds data check` is correct (Q4).
- **Hygiene:** changelog fragments are English. selftest `--lang` 4/4 is attached by the builders and was not re-run.
- **Witness consistency:**
  - The builder reported `test_judgment_census 22/22`, and my rerun prints `21 passed`. The load-bearing claim (green, +1×13
    only) is reproduced. The count differs by one and is not load-bearing.
  - The other attached numbers match the diff: 47 tests in `test_event_store` = old count + 1; 27 in `test_doctor_context` on
    OH6-3; 7 PacketNameLength-filtered.

## Trail

Read:
- the spec t-263 (whole);
- `docs/tasks/critic-diff-brief.md` 25-100;
- `docs/SIBLING_MAP.md` axis list, axes 18, 29, 34;
- `docs/TESTING.md` 89-111;
- both diffs (full);
- `event_store.py` 160-215, 262-285, 535-562;
- `native_context.py` 46-58, 171-211 (oh6-4);
- `inject_context.py` 302-345, 470-522, 600-739 (oh6-4);
- `controller.py` 7719-7760, 7830-7846, 8700-8715;
- `host_dispatch.py` 1-20;
- `driver_trace.py` 163-167, 273-283;
- `driver-golden-rules.json` N7-N9b, N24, N31;
- `test_driver_golden.py` grep hits 51-54, 114-136;
- `test_judgment_census.py` 200-240, 368-377;
- `test_refusal_registry.py` grep `findings(`;
- `test_config_view.py` 250-275;
- `batch-7-ostatki-t-263.md` on origin/main (OH7 rows);
- both commit messages.

Reruns (verbatim tails):
- oh6-3 `pytest -q test_event_store.py -k "temp_name or publish"`: `1 passed, 46 deselected in 0.73s`
- oh6-3 `pytest -q test_doctor_context.py -k "PacketNameLength and (arithmetic or unwritten)"`: `2 passed, 25 deselected, 14 subtests passed in 0.42s`
- oh6-4 `python -B refusal_registry.py --check; echo exit=$?`: `A24 refusal registry: no violations` ... `exit=0`
- oh6-4 `pytest -q test_judgment_census.py`: `21 passed in 21.67s`
- oh6-4 `pytest -q test_doctor_context.py -k NativeStageRefusal`: `4 passed, 27 deselected, 13 subtests passed in 1.74s`
- `git merge-tree --write-tree --name-only origin/wip/oh6-3 origin/wip/oh6-4`: `21cd5f8e39a8c1c1b72a1112fe14f6e030f4879a` rc=0 (no conflicted paths listed)
- merged tree (scratchpad): `11 passed, 20 deselected, 35 subtests passed in 2.18s`; `1 passed, 46 deselected in 0.83s`; `registry_exit=0`

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Covered: axis 18 (census +1 x13 named row by row), axis 34 (all six inject_context refusal exits now write a denial row; F-6 swept), axis 32 (no judgment moved), AR-22 producer/readers of the temp name changed in one commit. Already filed: OH7-1..OH7-5 (batch-7-ostatki-t-263). New residual proposed as node P-1: refuse_native_packet writes a NAMED row even when an OSError arises while a same-key launch is pending; owner: coordinator.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-263-oh6-3-oh6-4.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md (axes 18, 29, 34)",
      "docs/TESTING.md 89-111",
      "ai-packages/qa-factory/scripts/event_store.py",
      "ai-packages/qa-factory/scripts/native_context.py",
      "ai-packages/qa-factory/scripts/inject_context.py",
      "ai-packages/qa-factory/scripts/controller.py 7719-7846, 8700-8715",
      "ai-packages/qa-factory/scripts/host_dispatch.py 1-20",
      "ai-packages/qa-factory/scripts/tests/driver_trace.py 163-167, 273-283",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-golden-rules.json",
      "ai-packages/qa-factory/scripts/tests/test_driver_golden.py (N8/N24 rows)",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py 200-240, 368-377",
      "ai-packages/qa-factory/scripts/tests/test_event_store.py 274-343",
      "ai-packages/qa-factory/scripts/tests/test_doctor_context.py (NativeStageRefusal, PacketNameLength)",
      "plans/piles/onboarding-hooks/batch-7-ostatki-t-263.md (origin/main)"
    ],
    "reruns": [
      {"command": "oh6-3: python -B -m pytest -q test_event_store.py -k \"temp_name or publish\"", "result": "1 passed, 46 deselected"},
      {"command": "oh6-3: python -B -m pytest -q test_doctor_context.py -k \"PacketNameLength and (arithmetic or unwritten)\"", "result": "2 passed, 25 deselected, 14 subtests passed"},
      {"command": "oh6-4: python -B refusal_registry.py --check; echo exit=$?", "result": "A24 refusal registry: no violations; exit=0"},
      {"command": "oh6-4: python -B -m pytest -q test_judgment_census.py", "result": "21 passed (builder reported 22/22; green reproduced)"},
      {"command": "oh6-4: python -B -m pytest -q test_doctor_context.py -k NativeStageRefusal", "result": "4 passed, 27 deselected, 13 subtests passed"},
      {"command": "git merge-tree --write-tree --name-only origin/wip/oh6-3 origin/wip/oh6-4", "result": "21cd5f8 rc=0, no conflicted paths"},
      {"command": "merged tree: pytest test_doctor_context -k NativeStageRefusal or PacketNameLength; test_event_store -k temp_name; refusal_registry --check", "result": "11 passed 35 subtests; 1 passed; exit 0"}
    ]
  },
  "fixes": [
    "A-1 (OH6-3) test_event_store.py:274-343: wrap rows E-1..E-4 in subTest per row id (spec A.3, P29); make E-3/E-4 independent of E-1's recorded suffix; re-run red control r1 showing E-1 and E-3 red",
    "B-1 (OH6-4) test_doctor_context.py:530-535: drop part (d) (a negative control inside a test, TESTING.md:98 table, found means deleted) and part (c) (duplicates test_refusal_registry.py:70); keep (a)/(b). Spec defect of B.3, Lead decides",
    "B-2 (OH6-4) test_doctor_context.py:456: rename tearDown_story (runs at the start of each row, reads as a unittest hook) to a name that says it resets state"
  ]
}
```
