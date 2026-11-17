# Critic verdict t-1121: TBW1-11 stream A (builder t-1113), code gate

Under review: `origin/main...origin/worktree-agent-afbc9dbe1e07ce3be` (commit 01e57060, 10 files +413/-74), against card r2
`docs/tasks/specs/20261117-tbw-conductor-launches-siting-card-r2.md` §0a, §2, §3, §3a, §3b, §5, §7 A, §15.

**Verdict: ACCEPT WITH FIXES (fit_with_fixes). No blocking finding. Two fixes to make before merge (F1, F2) and one fix that needs the Lead to widen owns (F3). Q5 (`_noted`) stays out of this node and goes to a proposed node.**
The decision to accept is the Lead's.

## Findings

**F1 (fix before merge): the AST site-count table pins the source.** In `scripts/tests/test_detector_verdict.py::tbw_siting_command_sites`, the block from `sites = (("controller.py", "build_rework_request", "controller:rework.args", 16), ...` to its `check_eq(... is written at {count} refusing site(s)`) counts `DV.refusal("<id>"` literals per function, using the AST. `docs/TESTING.md:136` («Что не пишется», «Пин исходника … подсчёт вхождений … в коде») bans this form. A structural invariant goes in the shared ratchet: here, `refusal_registry` sites and `told_ratchet`, which stream B arms with the rows. A node's own test may not carry it. The table also breaks on unrelated edits: a new `rework.args` check added by T9a or C3 turns it red. It picks `fn` as the first BFS `FunctionDef` with the name, so a module-level `validate` or `main` added later would be picked silently. Its two `main` rows also duplicate the driven `main_with` rows just above (brief 5(e)). Fix: delete the block, about 22 lines. Nothing at a door is lost: the ids have no runtime reader on these roads (Q2).

**F2 (fix before merge): the `tests-over:` line names no reason.** `tests-over: one table of sites in test_detector_verdict, one wrapped/bare table in each walker test` describes the tests. It does not say why they exceed the volume. Test lines are about 290 added; product lines are about 195. Fix, in the amended commit message: `tests-over: card r2 §7 A items prescribe a per-site table (rows per branch of 6(i)/5(b), E7 rows) and mirrored walker tables in both walkers (F-10 (a))`.

**F3 (fix of this round; the Lead widens owns to `stage_done.coerce_value`; does not block): an install-state refusal gets the call id.** `stage_done.parse_sets` wraps EVERY `ValueError` of `coerce_value` as `stage_done:set`. That includes the branch `` `{key}`: the words a reality may take cannot be read from references/side-realities.json - repair that file (a change to the factory)… ``, which is a broken plugin file (FR-3). It is not the caller's shape. Once B lands the row, this Record carries the door "give the value in the key's form, or have the script that owns the field write it". Neither works for a broken reference file (FR-2). This also contradicts the card's own rule that state refusals stay bare (§3 head, F-P2 (a)). Card row 14 prescribed the blanket `except`, so this is a spec gap that the builder executed faithfully. Fix: `coerce_value` raises that one branch as a `ValueError` subclass (for example `UnreadableReference`), and `parse_sets` re-raises it unchanged before the wrap. The selection is by type, never by text (FR-12). Stderr bytes and the exit code stay the same. Add one row next to the `stage_done` siting rows.

## Questions of the dispatch

1. **Fit to the card.**
   - Sites, verified hunk by hunk: every hunk only wraps the existing literal, with the ids of §3.
     - Row 2: 16 `rework.args` appends: stage, purpose, reopen, blank reason, cause, three `--candidates`, cases S4+, outside scope, plan rows, S5 plan, S5 window, live, none, S5 spans.
     - Row 3: one `runner_half` extend.
     - Row 4: three `rework.cap` raises.
     - Row 5: three `release.call` sites.
     - Rows 1 and 5 in `main`: two each.
   - The builder's count corrections are right. 16, not "every literal" read loosely: the card's list names 15 kinds, and the plan / window / live / none group is 4 appends. In `main`, 2 = the comprehension plus the words re-raise.
   - Left bare as the card says (all checked):
     - the two `StateConflict` holds in `build_rework_request`;
     - `_rework_block_problems` / `_half_membership_problems` extends, and `_rework_kind` internals;
     - `_cli_story_root`'s `StateConflict` "initialize task before work" (excluded by the `cls is ValueError` identity);
     - the release "holds nothing back";
     - the `waiver` revoke/gate `ap.error`, `BlockNamesError` and no-pipeline prints;
     - "no record, nothing to revoke";
     - `current_code_diff_refusal`.
   - Key-4 tail: true in code. `Driver.s3_rework_completion` calls `s3_project(claims=False)`, which calls `PC.project_plan`, and that writes the mark. It is a door the refused party can use: the line reaches the conductor and the person through `gate_preflight.check_planning_contract`, and `rework_stage` is a conductor move. FR-1 holds: it says what is wrong and the road. FR-2 holds. The prefix `missing coverage_contract_revision` is untouched (E26).
2. **F-2 (a): exactly as §3a.**
   - Tracing `_merged` gives:
     - a single Record goes through with its `check`;
     - a folded message is a plain `f"{text} (×K)"`;
     - a non-`str` message is stringified as before.
   - In `_raise_all`, one problem gives `raise cls(Record)`. Several give the COMPOUND text plus `exc.records` set as an attribute.
   - Readers of `records` exist on main: `role_cli.run_guarded` → `refuse(records=…)` → `_extra_record_lines`, and `DV._records_in` / `told_fields`.
   - None of them is reached by a controller exception on any road:
     - `controller.__main__` prints `json.dumps({"error": str(exc)})`;
     - `story_step` (in-process `build_rework_request` / `validate`) prints `f"…{type(exc).__name__}: {exc}"`;
     - the driver runs `controller.py` as a process;
     - `stage_guard` only builds `Controller(root).state()`;
     - `apply`'s `StateConflict` handlers select by `IdempotencyKeyReused` type and re-raise.
   - So no id is printed twice, and no `expected` / `door` field leaks into text a person reads.
   - Additive side effect (safe direction): the second `_merged` caller (S5 window problems, controller.py about :7188) now also keeps the Records it already received. The text is identical.
3. **`main`.** `WordsRefused` is a `ValueError` subclass and is re-raised as the same class with the same `str`. `__main__` catches `ValueError`, prints the same JSON and exits 2. The comprehension maps only inside `rework` / `release`, so E11 holds. The test drives `rework`, `release`, `next` and `reopen_story`.
4. **The walkers.**
   - The unwrap applies only to the message node (`exc.args[0]`, or the tuple's second element). It needs `Name refusal` or `Attribute DV.refusal`, at least 2 positional arguments, and no `Starred` in the first two.
   - Left wrapped: keywords, `self.` / `other.`, one argument, a bare Name, and starred forms.
   - `DV` bound to `delivery_verdict` elsewhere is irrelevant: both walkers read `controller.py` only, which binds `DV` once (:47). A grep for a bare `refusal(` call in controller.py, excluding `DV.refusal`, finds none.
   - What the rule could still unwrap wrongly: a future local `def refusal(a, b)` in controller.py would be read as its 2nd argument. That still yields a message head, never a hidden block. Acceptable.
   - "Unrecognised stays wrapped and fails loudly" holds:
     - the generator gives route `?`, prints UNCLASSIFIED and writes nothing ("FAILED");
     - a caller-routed function would still change `controller-blocks.md`, and the byte compare catches it;
     - the package test fails "every block has a row".
   - The two copies are identical: an AST dump compare of `unwrapped_segment` and `is_refusal_wrapper` gives True, True. The tables mirror each other: 7 wrapped pairs and 4 not-unwrapped rows in each.
5. **`_noted` (E8): correctly out of this node, but the card under-measures it.**
   - The loss is deterministic on two sites:
     - `release_dispatch` with no `--dispatch` and not exactly one open dispatch: `_noted` always runs. When the words are fine, the only problem is the dispatch one, and it ALWAYS loses its id.
     - `build_rework_request` with an invalid stage and no other problem: same.
   - This is not a hole in this node's invariant. N1 is the literal at the site, `unsited` not rising and the text byte-identical, and all three hold. No reader of a controller Record exists on any road (Q2), so no reader is starved.
   - A fix cannot go in `controller.py` alone: a `with_check(…, message.check)` is a `check_arg` walk error (`refusal_registry.py:1374`, S-11).
   - Proposed node, for the Lead of told-before-work to open: "`Controller._noted` keeps a Record's fields when it appends its note: a `detector_verdict` helper beside `with_check` that copies the fields of a record onto a new text (the check taken from the record, not a literal; registered in `CHECK_PASSTHROUGH` if the scanner needs it). Owns: `scripts/detector_verdict.py`, `scripts/controller.py::_noted`, one E8 row." Owner: Lead of told-before-work, batch 1 or next. It must land before any node adds a `told_fields` printer to `controller.py`.
6. **Analogs: none of this node's class left unsited.**
   - The class is "refusals of the command a conductor move's `run` names". I walked the moves of `references/conductor-actions.json`: `rework_stage`, `release_and_restart`, `go_on_as_is`, `story_fact` and `revoke_exclusion` are all covered by §3.
   - `approve_gate` and `resume_with_words` are run by the driver, so the `gate-decision` / `reopen_story` / `leave_unlaunched` / `settle_order` / `stop_waiting` / `first_look_continue` `person_words.read` sites are not a conductor's call. They are not this class.
   - `stand_prepare` (`stand_health:probe`) is excluded by the card (E-T9c-2).
   - `waiver --why-person` (`_classed`) is not in the move's `run`.
   - `run_stage` `BlockNamesError` / no-pipeline are state, bare by the card.
   - The six `controller:*` unsited rows are T9a's (TBW1-10).
   - SIBLING_MAP: a grep for `told|walker|controller-blocks` finds no axis for told sites. The walker twin is handled by F-10.
7. **Tests.** The driven rows and the walker tables are legitimate joins. Their expected values come from the card: the key-4 sentence, the ids from §3, and the old texts reconstructed from the unchanged literals. The AST rows are not (F1). The `tests-over` line needs fixing (F2). The flipped `tbw_t7b_sites` row and the siting planning_contract row both assert the id. The card prescribes both (E17 plus the items), so that is not a finding.
8. **Collisions.**
   - Trial merges with `git merge-tree` produce no textual conflict: A into main gives 6c43536e, A into C3 `worktree-agent-ac40b44fb0a175afa` gives f81626b2.
   - On both merged trees the generator stays byte-equal with their `design/controller-blocks.md`: 355 blocks on main+A, 356 on C3+A, and C3's new `registry_blocking` row is kept.
   - C3 changes `_passed_by_person` (it now notes passes) and adds a registry stop in `validate`'s dispatch branch. `blocking` items stay `str`, so A's `DV.refusal("controller:rework.cap", blocking[0] + …)` is unaffected. Neither diff touches `_merged`, `_raise_all` or the other's hunks.
   - Merge order is free. Whichever lands second reruns the generator byte compare (already done above). Recommendation: A first, since T9a waits on A (§0a).
   - T9c (8c0c75e0): no semantic conflict. On the merged tree, `DV.refusal` resolves as E5 says: the 14 ids get the unreadable sentence, and `planning_contract:plan.unmarked_revision` falls to the aggregator (expected ""). No printer on these roads shows either.

## Standing questions (brief items)

- **Fit (1):** yes, apart from F3, which is a spec gap.
- **Builder's own decisions (2):** `_merged` keeps only `str` instances (safe), and `release_dispatch` unpacks `_unknown_dispatch` at the caller. Both are safe.
- **Seams (3):** additive.
- **Class (4):** see Q6.
- **Tests (5):** F1, F2.
- **DUPLICATION AND CONSISTENCY (6):**
  - The unwrap in two walkers is the accepted F-10 (a), with identical copies.
  - The `except WordsRefused` re-raise appears 3 times (controller x2, waiver x1). It is card-prescribed: a helper would hide the literal (a walk error).
  - Sixteen `DV.refusal("controller:rework.args", …)` literals is the scanner's one-literal-per-site rule.
  - Otherwise none found. Grepped: `told_fields(|spoken(` over scripts, `\.records\b` / `getattr(.., "records"`, `WordsRefused` catchers.
- **CODE QUALITY (7):**
  - no new function over 60 lines;
  - the `_merged` double conditional is terse but correct (traced 4 cases);
  - the continuation lines of the re-wrapped literals keep their old indent: cosmetic, does not mask a bug.
  - None blocking.
- **Hygiene (8):** CRLF kept in all 7 package files (CR counts rise with the lines). `selftest --limits --lang` 4/4 (my rerun).
- **Ratchets (9):** no in-tree ratchet file touched. Census untouched.
- **ARCHITECTURE (10):** AR-9, 13, 15, 20, 29 are named. AR-22 (`exc.records` produced, with readers in `role_cli` / `DV._records_in`) is kept but not named. Minor; the reader exists.
- **JUDGMENT (11):** none moved. Ids attach to existing refusals.
- **ONE ROAD (12):** none found. Grepped the diff for language / runner / project branches: none. `source_exclusions` gives `revoke.call` to `--load` / `--show` refusals too, which is consistent with the row sentence (part3 :130 covers "exactly one of" and `--task`).
- **Tests over budget (20):** F2.

## Trail

- Read:
  - `docs/tasks/critic-diff-brief.md` (whole);
  - card r2 §0, §0a, §1 table, §2, §3, §3a, §3b, §5, §7 A, §9-§15;
  - the full product diff and the test diffs;
  - in tree W = `.claude/worktrees/agent-afbc9dbe1e07ce3be`: `detector_verdict.py` :95-245, `controller.py` :6150-6235, :9812-9846, :10125-10154, :5195-5240, :2858-2880, build_rework_request problem sites, :7175-7192; `role_cli.py` :190-220; `story_step.py` :2325-2375; `stage_done.py` `coerce_value`, :1555-1565; `waiver.py` :1300-1345, :1955-1980; `gate_preflight.py` :1910-1925; `planning_contract.py` :2010-2025, :4495-4500; `driver_dispatch.py` :2790-2845; `driver_stage_plan.py` :525-556; `refusal_registry.py` :81-88, :1365-1376; `references/conductor-actions.json` moves; part3 rows :25, :76, :124-131;
  - the C3 branch diff (controller hunks, generator);
  - `docs/TESTING.md` :136, :155-158.
- Control reruns (in W):
  - `python -B W/tools/controller-blocks-gen.py <scratch>/cb-after.md`: `355 blocks: caller 105, command 220, person 17, unpassable 13`; `cmp` with `design/controller-blocks.md`: BYTE-EQUAL.
  - `python -B scripts/tests/test_controller_blocks.py`: `=== test_controller_blocks: 386/386 ok ===`.
  - `python -m pytest tools/test_controller_blocks_gen.py -q`: `20 passed in 38.26s`.
  - `python -B scripts/selftest.py --limits --lang`: `=== qa-factory selftest: 4/4 ok ===`.
  - `git merge-tree --write-tree` main+A gives 6c43536e and C3+A gives f81626b2, both clean. The generator on each archived tree gives 355 / 356 blocks, both BYTE-EQUAL.
  - AST compare of the two unwrap copies: `{'unwrapped_segment': True, 'is_refusal_wrapper': True}`.
- Not rerun: `test_detector_verdict` 842/842 (consistency-checked against the diff instead) and the slow files (batch canon).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 (fix before merge): scripts/tests/test_detector_verdict.py::tbw_siting_command_sites - delete the AST site-count block (sites = ... check_eq per count): a source pin banned by docs/TESTING.md:136; duplicates the driven main rows; fragile on unrelated edits",
    "F2 (fix before merge): commit message tests-over line names a description, not a reason; reword to the card r2 section 7 A items (per-site table, mirrored walker tables F-10 (a))",
    "F3 (fix of this round, Lead widens owns to stage_done.coerce_value; non-blocking): parse_sets wraps the unreadable side-realities.json ValueError (an install-state refusal, FR-3) as stage_done:set whose door the conductor cannot use (FR-2); raise that branch as a ValueError subclass in coerce_value and re-raise it unchanged in parse_sets, one row"
  ],
  "class_completeness": "Class = refusals of commands a conductor move runs (references/conductor-actions.json moves). rework_stage, release_and_restart, go_on_as_is, story_fact, revoke_exclusion all sited per card section 3; approve_gate/resume_with_words are driver-run (gate-decision etc. person_words sites not this class); stand_prepare excluded by card E-T9c-2; controller:* unsited rows are T9a (TBW1-10). Walker twin covered both copies identical (F-10). _noted E8 loss (deterministic on release-without-dispatch and invalid-stage-alone) is out of this node: proposed node in told-before-work (detector_verdict copy helper + Controller._noted), owner Lead of told-before-work, before any told printer on controller.py. No SIBLING_MAP axis for told sites (grep told|walker|controller-blocks).",
  "trail": {
    "read": [
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/20261117-tbw-conductor-launches-siting-card-r2.md",
      "git diff origin/main...origin/worktree-agent-afbc9dbe1e07ce3be (all 10 files)",
      "W/ai-packages/qa-factory/scripts/detector_verdict.py:95-245",
      "W/ai-packages/qa-factory/scripts/controller.py _merged/_raise_all/_noted, build_rework_request, release_dispatch, _cli_story_root, main, __main__, apply StateConflict handlers, :7175-7192",
      "W/ai-packages/qa-factory/scripts/role_cli.py:190-220",
      "W/ai-packages/qa-factory/scripts/story_step.py:2325-2375",
      "W/ai-packages/qa-factory/scripts/stage_done.py coerce_value, main :1555-1565",
      "W/ai-packages/qa-factory/scripts/waiver.py run_stage, main",
      "W/ai-packages/qa-factory/scripts/gate_preflight.py:1910-1925",
      "W/ai-packages/qa-factory/scripts/driver_dispatch.py:2790-2845",
      "W/ai-packages/qa-factory/scripts/refusal_registry.py:81-88,1365-1376",
      "W/ai-packages/qa-factory/references/conductor-actions.json",
      "docs/tasks/specs/20261113-told-before-work-wave0-rows-part3.md rows 25,76,124-131",
      "origin/worktree-agent-ac40b44fb0a175afa controller.py and generator diff",
      "docs/TESTING.md:136,155-158"
    ],
    "reruns": [
      {"command": "python -B W/tools/controller-blocks-gen.py <scratch>/cb-after.md; cmp with W/ai-packages/qa-factory/design/controller-blocks.md", "result": "355 blocks: caller 105, command 220, person 17, unpassable 13; BYTE-EQUAL"},
      {"command": "(cd W/ai-packages/qa-factory && python -B scripts/tests/test_controller_blocks.py)", "result": "=== test_controller_blocks: 386/386 ok ==="},
      {"command": "(cd W && python -m pytest tools/test_controller_blocks_gen.py -q)", "result": "20 passed in 38.26s"},
      {"command": "(cd W/ai-packages/qa-factory && python -B scripts/selftest.py --limits --lang)", "result": "=== qa-factory selftest: 4/4 ok ==="},
      {"command": "git merge-tree --write-tree origin/main A; git merge-tree --write-tree C3 A; generator on each archived tree + cmp", "result": "clean 6c43536e / f81626b2; 355 and 356 blocks, both BYTE-EQUAL"},
      {"command": "AST dump compare of unwrapped_segment and is_refusal_wrapper in both walkers", "result": "{'unwrapped_segment': True, 'is_refusal_wrapper': True}"}
    ]
  }
}
```
