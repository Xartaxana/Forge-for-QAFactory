# RD1-35 — one node-id road for the writer's and the hand's `tests[]` rows (draft card, designer, t-1351)

Node: `plans/piles/rules-debt/batch-1-phase-2.md` row RD1-35 (line 63; named RD1-19b in FL1 card F4). Feature F19.
Status: DRAFT. Executable BY THE RECOMMENDATIONS of §7 (F1 (b), F2 (a1), F3 (a), F4 (a)). Every fork is the Lead's.
Brief questions: Q1 -> §2, Q2 -> §3, Q3 -> F1 in §7, Q4 -> §4, Q5 -> §5.

## §0 Facts (measured by Read/Grep, 18.11.2026; code named path::symbol, all under `ai-packages/qa-factory/scripts/`)

1. `manifest_from_tests.py::resolve_through_pytest` (called only from `::main`, only under `--collect`): asks `<file>::<iid>` per row
   and NOT the file alone, so it cannot tell "file yielded no test" (E7) from "missing"; refuses on ANY `missing` (`Refusal`,
   exit 2, nothing written); a collect that cannot answer gives notes only (no refusal, no mark); rewrites `tests[]` and
   `then_bindings[]` only (not `unresolved[].instance_ids`, written by `::build`, see `instance_ids` at :1294); maps back by
   `rsplit("::", 1)[-1]`; no same-file check; timeout = `node_ids.check_request` default 180; argv = the command after `--`,
   cwd = `--cwd` (default `.`), while the rows' `file` is project-root relative (`::_relative`, `::_files`).
2. `manifest_from_tests.py::collect_refusal`: refuses `--collect` for any file whose name does not end in `.py` (a language read by
   its name). Readers: `::main` (:1917), `::resolve_through_pytest` (:1827), `test_manifest_from_tests.py::ep1_37` (:2314-2319).
3. `manifest_put.py::stamp_node_ids`: `_drop_role_marks` runs on EVERY row first (a `node_id_check` on a writer row is dropped
   too), then `_asked_map` (E8), then `_eligible_rows`, which skips any row carrying `WRITER_MARK` (`generated_from`).
   `::_ask_collect`: argv `gate_preflight.collect_base(config)`, cwd project root, `execution.node_id_collect_timeout_s`,
   switch `execution.verify_node_ids`; asks nodes AND files. `::_read_collect`: missing in a file that yielded no test ->
   `not_verified` (E7); missing -> problem; no answer -> `not_verified` with the collect's word. `::_stamp_rows`: another-file
   resolution -> `not_verified`; a missing id a person's recorded S5 word covers -> `passed_by_person`.
4. `manifest_put.py::run` stamps at :2893, before `stamp_provisional` and the lock; a problem is refused as
   `manifest_put:node_id` naming the waiver door; `id_notes` are printed at :2977.
5. The writer already calls the store in-process: `manifest_from_tests.py::main` :1962 `manifest_put.run(...)`, stdout captured
   into `put_output`, any non-zero code -> `EXIT_PUT_FAILED` (3); the fragment file is written before the call.
6. `manifest_from_tests.py::_form_after_write` asks `_row_form` for the FRAGMENT's ids; `contract.py::instance_id_aliases`
   (:4075-4106) holds no `node_id_check.asked`. `probe_debt.py::_rebind` runs the writer `--dry-run --json` WITHOUT
   `--collect` and refuses to write when a dry-run id is not in `::_live_ids` (aliases, same function).
7. Slow class (`scripts/slow_tests.json` `files`, `slow_over_s` 10): `test_manifest_from_tests.py` 79.0 (:69),
   `test_node_ids.py` 14.3 (:78), `test_probe_debt.py` 19.8 (:87). Not listed (fast, no `canon_only` mask):
   `test_manifest_put_assertion_line.py` (pytest-style, holds the RD1-19 table `NODE_ROWS`), `test_manifest_put_keep_unsent.py`,
   `test_manifest_put_merge.py` (script-style, `harness.finish`).
8. `references/templates/config.json` :19-20: `test_command_templates` `suite`/`quiet` empty -> a harness stand has no
   pytest-shaped command, so the store marks `not_verified` with no subprocess (estimate that `harness.temp_project` copies
   the template; the builder's witness run shows it).

## §1 Architecture, census, variety (designer rule 1)

- AR-15 (one survivor): `manifest_put.py::stamp_node_ids` becomes the ONE asker for every manifest `tests[]` id; the writer's
  own site goes. Change check: list every site of the problem (§6); the node-id survivor has no SIBLING_MAP axis yet (Grep
  `(?i)node.id` in `docs/SIBLING_MAP.md`: 0 hits; control `hooklib.read_json` found at :368) - FL1 F8's axis, the Lead's.
- AR-14 (one writer): `node_id_check` stays the store's alone; `generated_from` no longer exempts a row. Check: no other
  code writes the mark (the writer never did).
- AR-13 (one reader): `node_id_check.asked` is read only through one public `manifest_put.asked_spellings` (§2).
  Check: Grep `"asked"` reads of the mark in the package with a positive control (`_asked_map` itself).
- AR-28 (unknown is no pass): any collect that cannot answer -> `not_verified` with its reason, never `verified`, never a
  refusal. Check: §4 E4-E6 pinned by T1/T4.
- AR-1: the `.py`-suffix refusal (`collect_refusal`) is removed, not moved: no row is branched on a language name.
- AR-29 census, every check the change adds or alters (owner / class): `manifest_put._eligible_rows` widened to writer rows -
  data / xref; `manifest_from_tests.resolve_through_pytest` refusal removed - data / xref; `manifest_from_tests.collect_refusal`
  removed - data / shape; `probe_debt._rebind` known-id check reads asked spellings - data / xref. Census rows: none exist
  for these functions (Grep in `scripts/tests/fixtures/judgment-census.json`: 0; control: :601-605 rows of
  `manifest_from_tests.py`); `test_judgment_census.py` is canon class: canon judges. Commit line: the `judgment:` line in the
  form `tools/architecture_gate.py` accepts; content `judgment: none -- every altered check joins an id to the project's
  collect or to a stored spelling (xref, owner data)`.
- Variety walk (`design/architecture.md` § A):
  - `axis 3: held by key -- test_command_templates via gate_preflight.collect_base and the runner row via node_ids.runner_form; unknown value (no pytest-shaped command, another runner) -> every row stored not_verified with the reason, never refused`
  - `axis 3: narrows -- a project whose test_command_templates is empty but whose automator passed --collect -- <cmd> loses the verification it had; its rows read not_verified until the key is set` (fork F2)
  - `axis 13: held by key -- the stored row's node_id_check and spellings; unknown value (a row written before this change, no mark) -> not asked again on a same-spelling re-send, stays as stored`
  - `axes 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12: n/a -- the change moves where a test id meets the project's own collect; no product language, surface, flow, source, delivery, stand, host, people, artifact language, size or check kind meets it`

## §2 Q1 — the ONE road

`manifest_put.py::stamp_node_ids`, called by `manifest_put.py::run`, is the road for every `tests[]` row, the writer's and the
hand's. No new helper and no new module: the writer reaches the store already (§0 fact 5), so the one road is reached by
REMOVING the writer's ask, not by sharing a second one. Takes (unchanged): the fragment, the task root, the project root,
`words`; argv/timeout/switch from config (`::_ask_collect`). Returns (unchanged): (fragment with ids resolved and marked,
problems, notes).

Callers and how each reads the answer:
- `manifest_put.py::run` (hand and writer fragments alike): problems -> `manifest_put:node_id` refusal; notes printed.
- `manifest_from_tests.py::main`: reads `put_code` (non-zero -> exit 3, `ok: false`) and prints `put_output` (the store's
  rename and `not_verified` lines); after a real write it maps the fragment's ids through `manifest_put.asked_spellings` before
  `_row_form` (F3).
- `probe_debt.py::_rebind`: maps the dry run's ids through `manifest_put.asked_spellings` before its alias and ghost checks (F3).

New public reader `manifest_put.py::asked_spellings(stored_tests) -> {author spelling: stored id}`: the body of `_asked_map`
(an `asked` no stored row answers to itself), plus: a spelling two stored rows claim maps to NONE (ambiguous). `_asked_map`
delegates to it. Direction of error: toward "no mapping" (the caller treats the id as unknown), never toward a row the
spelling was not asked for. Adversarial inputs that must stay on the safe side: two rows with the same `asked`; `asked` equal
to a live spelling of another row; `asked` not a string / blank; a `node_id_check` that is not a dict; a non-dict row.

## §3 Q2 — the conflicting pairs (behaviour under §2)

- (a) refuse vs E7: the store's reading wins for writer rows. Missing in a file that collected -> refusal (writer exit 3,
  manifest unchanged) unless a person's recorded S5 word passes it (`passed_by_person`); missing in a file that yielded no
  test -> `not_verified`. Invariant: an id pytest does not collect from a file that did collect is never stored without a
  person's word; no id is `verified` without a collected match in its own file.
- (b) argv/cwd: config `collect_base`, project root. The command after `--` and `--cwd` feed nothing (F2). Invariant: an id is
  asked from the root it is spelled from, so a `--cwd` elsewhere can no longer mis-ask.
- (c) `verify_node_ids` false: writer rows like hand rows - stored `not_verified` with the switch's reason, one printed line,
  exit 0. Invariant: the switch off never yields `verified` and never a refusal.
- (d) rename note: one wording, the store's (`manifest_put.py::_verified_mark`: `node_id_check: pytest collects X as Y - the
  manifest carries the collected id`); the writer's "(a project plugin renames the parameter, not you)" goes with its function.
  The substring `pytest collects test_region[eu] as test_region[chromium-eu]` the old test pinned survives in the new line.

## §4 Q4 — edges (behaviour + the invariant it protects)

- E1 Rows written before the edit: never re-asked by replay/recover (E14 of RD1-19) nor by a same-spelling re-send of a
  stored row with no mark or a `verified` mark (`_eligible_rows`' held rule, unchanged). Invariant: a stored id changes only
  through a re-send that a collect answers; a pre-edit row is never renamed behind the role's back.
- E2 Empty `tests[]` / no `tests` / not a list: no collect, no mark (early return); a writer call with no row still prints
  "nothing written" and never calls the store. Invariant: no subprocess for a fragment with nothing to ask.
- E3 A row with no `file` or no explicit id (`instance_id`/`test_instance_id`): not asked, no mark (hand rows only; the writer's
  rows always carry both, `manifest_from_tests.py::build` entry dict). Invariant: an id derived from `function` is never asked.
- E4 A non-Python writer row (`.kt`, `.ts`, read by `test_source`): asked like any row; pytest cannot collect it -> `not_verified`
  (E7, or the collect's error); `--collect` with such a file is no longer refused. Invariant: no language name branches the
  road; a row no runner can check is never refused by the ask and never `verified` (FL1 F6).
- E5 pytest absent, not startable, or past `node_id_collect_timeout_s`: every asked row `not_verified` with the collect's own
  reason (`<ExcType>: <message>` for a raising call), one line, exit 0. Invariant: AR-28.
- E6 `verify_node_ids` false: §3 (c).
- E7 Missing in a collected file: §3 (a). The fragment file stays in `work/manifest-fragments/` as for any store refusal; exit 3
  (was 2 under `--collect`). Invariant: "Nothing was committed" stays true of the manifest and the journal.
- E8 A hand row that COPIED `generated_from`: asked like any row (the FL1 residual closed); a forged `node_id_check` on it is
  dropped. Invariant: `generated_from` never exempts a row from the ask. Its MERGE meanings (`_writer_tests`,
  `_merge_then_bindings`, `_merge` novelty/bytes) are unchanged (non-goal).
- E9 A writer re-run: a spelling a stored row answers to, or an `asked` it carries, costs no collect (E8 of RD1-19); a stored
  `not_verified` row is asked again (FR-40). Invariant: a known spelling is never collected twice.
- E10 A stored row renamed by the OLD `--collect` (collected spelling, no `asked`) and a re-run with no collect able to answer:
  the author's spelling is stored as a second row marked `not_verified`; a later re-send a collect answers renames it into
  the stored row and retracts the old spelling (`_retract_renamed`). Invariant: the extra row is never `verified`; it says why.
- E11 `--dry-run`: no collect (the store is not called); the note says ids are resolved when written; the JSON `fragment`
  carries source spellings. Invariant: a dry run starts no subprocess and writes nothing.
- E12 Row form after a real write: the fragment's ids mapped through `asked_spellings` -> the form names the stored (collected)
  id; on a dry run the source spelling with the existing "not in the manifest yet" note. Invariant: the form never reports
  "no such row" for a row the store renamed.
- E13 `unresolved[].instance_ids` and `obligation_bindings[].instance_ids` of a writer fragment are renamed with the row
  (`_rewrite_instance_ids`; the writer's road did not). Invariant: no carrier keeps a spelling the row lost.
- E14 Cost: one bounded collect per writer write that has a new spelling (was none without `--collect`, one with it).
- E15 `probe_debt._rebind`: a dry-run id mapped by `asked_spellings` to a live row counts as known; an ambiguous or unmapped
  new spelling still keeps the item ("would make a ghost row"). Invariant: a rebind never writes a spelling the store would
  add as a second row.

## §5 Builder card (under F1 (b), F2 (a1), F3 (a), F4 (a))

given: this card; `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rd1-19-fl1-pytest-id-card.md` (F4, E-numbers of RD1-19)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manifest_from_tests.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manifest_from_tests.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manifest_put.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manifest_put_assertion_line.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_node_ids.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/probe_debt.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_debt.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/skills/qa-story/phases/s5.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/artifact-contract-automation.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-automator/artifact-contract-automation.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/qa-code-critic/artifact-contract-automation.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/stage-joints.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules-debt.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/rules-debt-1-rd1-35-one-node-id-road.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manifest_put_keep_unsent.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manifest_put_merge.py
non-goals: `WRITER_MARK`'s merge meanings (E8); `contract.instance_id_aliases`; `selector`/`parameter` spellings; runners
  other than pytest (FL1 F6 node); the SIBLING_MAP axis (Lead); `CHANGELOG.md` history lines; the pile row status (Lead);
  the last two owns are touched ONLY to fix an exact-row/exact-output assertion that now meets a `node_id_check` mark or line.
handoff: the builder's report on the path `tools/dispatch_new.py` prints; commit on the node's worktree branch
edges: §4 E1-E15, §3 (a)-(d)
DoD: `python -m pytest ai-packages/qa-factory/scripts/tests/test_manifest_put_assertion_line.py -q` ; `python -B ai-packages/qa-factory/scripts/tests/test_manifest_put_keep_unsent.py` ; `python -B ai-packages/qa-factory/scripts/tests/test_manifest_put_merge.py` ; `python -B -c "import sys; sys.path[:0]=['ai-packages/qa-factory/scripts/tests','ai-packages/qa-factory/scripts']; import harness, test_manifest_from_tests as T, test_node_ids as N, test_probe_debt as P; T.fr16_store_road(); T.ep1_37(); T.hf_k7(); N.siblings(); P.rebind_writes_only_known_ids(); harness.finish('rd1-35 narrow')"` ; `python -B ai-packages/qa-factory/scripts/selftest.py --lang`
siblings: `red_sandbox.check_node_ids`, `run_suite` and `probe_by_code` node-id sites - unchanged (their own argv from a
  request/profile); `node_ids` CLI - unchanged; `test_node_ids.py::siblings` loses the writer line (its site is gone)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-rd1-35-one-node-id-road-card.md

The narrow call is an estimate: the builder confirms each named function runs standalone (module-level setup run by `main`
may be needed) and reports `not run locally: <file>, canon judges` for the three slow files beyond the narrow call.
`stage-joints.json` and the slices: run their own checks (`python -B ai-packages/qa-factory/scripts/stage_joints.py --help`,
`python -B ai-packages/qa-factory/scripts/contract_slices.py --help` for the forms - estimate, not measured).

Requirements:
1. `manifest_put.py::_eligible_rows`: drop `WRITER_MARK in r` from the skip. POSITION invariant: `_drop_role_marks` stays first
   and on every row, `_asked_map` before eligibility, the stamp before `stamp_provisional` and the lock; the rows still
   skipped are exactly: non-dict, no explicit id, no `file`, held by a stored row whose mark is not `not_verified`. Reword the
   docstrings of `_eligible_rows`, `stamp_node_ids` and the comment at `::run` :2888 from "hand-typed" to every row.
2. `manifest_put.py::asked_spellings` per §2; `_asked_map` delegates (one reader, AR-13).
3. `manifest_from_tests.py`: delete `resolve_through_pytest` and `collect_refusal`; `::main` keeps `--collect`, `--cwd` and
   the `--` command ACCEPTED and inert, printing one note when given: `--collect is no longer needed: manifest_put.py resolves
   every instance id when it stores the rows, through the project's own command (test_command_templates); the command after
   -- and --cwd are not used`; the `ap.error` for `--collect` with no command goes. The unverified note becomes: `instance ids
   are resolved when written: manifest_put.py asks the project's pytest collect (test_command_templates) and prints each
   rewrite; a dry run asks nothing`. `::_form_after_write` maps the fragment's ids through `manifest_put.asked_spellings` of
   the stored tests on a real write (E12). Docstring of the module/`--help` text naming `--collect` follows.
4. `probe_debt.py::_rebind`: map `wanted` through `manifest_put.asked_spellings(C.manifest_tests(manifest))` before the alias
   and unknown checks (lazy import, like the writer's); `REBIND_LEFT` drops "(with --collect if the ids come from a collect)".
5. Texts: `s5.md` :300-306 - the `--collect` sentence becomes "the store resolves every id through the project's collect;
   read its rewrite and `not_verified` lines, and say in the handoff which ids are `not_verified` and why"; the TP1-15045 reason
   stays. `artifact-contract-automation.md` :52 "a hand-written id" -> "every `tests[]` id (yours and the writer's)", the two
   slices regenerated. `stage-joints.json` :3601 requirement "A hand-written `tests[]` `instance_id`" -> "Every `tests[]`
   `instance_id`". `design/factory-rules-debt.md` :22 FR-16 row: the resolver is the store. The changelog.d fragment, English:
   "`manifest_from_tests.py` rows now take the same pytest id check as hand rows when `manifest_put.py` stores them (marked
   `node_id_check`, an uncollected id refused with the nearest ids, `not_verified` where no collect answers); `--collect` is no
   longer needed and is accepted with a note; a hand row carrying a copied `generated_from` is checked too (RD1-35)."
6. Tests, in this order (the builder stops when its test lines reach its code lines and reports the rest):
   test: `test_manifest_put_assertion_line.py::test_a_hand_typed_id_joins_the_collect_of_its_file` - a sender axis over
     `NODE_ROWS`: hand / writer (`generated_from`) / hand with a copied `generated_from` and a forged `verified` mark -> the same
     stored id and mark in all three | expected from: §2, §3, E8, FL1 F4
   test: `test_manifest_from_tests.py::fr16_store_road` (the FR-16 block of `::main` :440-493 moved into its own function and
     the K7 (e) block of `::hf_k7` folded into it) - an in-process real write with `node_ids.collect` stubbed and a pytest
     template: the stored row and its `then_bindings`/`unresolved[].instance_ids` carry `test_region[chromium-eu]`, the mark keeps
     `asked`, `put_output` holds the store's rename line, the row form names the collected id; a typo id -> put code non-zero,
     manifest unchanged | expected from: §3 (a), (d), E7, E12, E13
   test: `test_manifest_put_assertion_line.py::test_a_role_sent_mark_is_dropped_and_rows_not_asked_keep_their_state` - its writer
     row (:322-324) is now marked `not_verified` (no collect in that world) | expected from: E8, §3 (c)
   test: `test_manifest_from_tests.py::fr16_store_road` CLI rows and `::ep1_37` :2314-2319 - `--dry-run --collect` with no command:
     exit 0 and the inert note, no subprocess; without the flag the new note; a `.kt` with `--collect`: exit 0 with the
     language note, a `.ts` real write stored with a `not_verified` mark | expected from: F2 (a1), E4, E11
   test: `test_probe_debt.py::rebind_writes_only_known_ids` - a row stored under the collected spelling with `asked` = the dry
     run's id -> rebound; two rows claiming that `asked` -> kept | expected from: F3 (a), §2 adversarial, E15
   Removal, no test line: `test_node_ids.py::siblings` :642-646 (the writer's collect is gone; T1 is its witness).

## §6 Readers of every touched file / name (designer rule 7)

The `tools/owns_readers.py` block was NOT attached to the brief: the Lead runs
`python -B tools/owns_readers.py --paths <the §5 owns> --names resolve_through_pytest,collect_refusal,_eligible_rows,_asked_map,asked_spellings,REBIND_LEFT,WRITER_MARK`
and the plan critic answers its lines (Q13 (d)). Hand greps meanwhile (Grep tool):
- `resolve_through_pytest|collect_refusal|WRITER_MARK|_eligible_rows` over `scripts/`: 23 hits / 5 files. `manifest_from_tests.py`
  (5, this stream); `manifest_put.py` (10: `_merge_helpers` :703, `_writer_tests` :1726, `_merge` :2256/:2264 unchanged;
  `_eligible_rows` :946 this stream); `test_manifest_put_keep_unsent.py` :91/:153 (builds hand rows by dropping the mark;
  unchanged meaning, witness run); `test_manifest_from_tests.py` :470/:483/:1934 (this stream); `test_node_ids.py`
  :611/:644-646 (this stream). Same pattern over `tools/`: 0 (control: the scripts hits above).
- `--collect` (literal, package, fixtures excluded): `s5.md` :300 (this stream); `probe_debt.py` :102 (this stream);
  `design/factory-rules-debt.md` :22 (this stream); `CHANGELOG.md` :1268, :5560 (history, unchanged); tests above.
  Outside the package: `plans/piles/roles-context/findings/B-029-...md` :3/:18 names the "`--collect` half" (another pile,
  unchanged; the Lead may annotate).
- `REBIND_LEFT`: `probe_debt.py` 14 uses (text only) and `test_probe_debt.py` :509/:561/:936 by symbol - unchanged.
- `node_id_check` prose: `artifact-contract-automation.md` :52 and slices :50 x2 (this stream); `stage-joints.json` :3597-3603
  check `manifest_put:node_id` (requirement text, this stream; the door unchanged).
- `contract.instance_id_aliases`: `probe_debt._aliases`, `_form_after_write` via `_row_form` - unchanged (F3 (a) maps before).
- `manifest_put.run` callers: the writer (unchanged call) and the CLI - unchanged.
- `agents/qa-automator.md` :70/:73 name `manifest_from_tests.py` and its printed row form, not `--collect` - unchanged.

## §7 Forks (the Lead's)

- F1 — scope against FL1 F4's wider text (Q3). (a) The pile row's owns only (2 files): the writer cannot share the store's
  road without editing `manifest_put.py` - it could only call its private `_read_collect`/`_stamp_rows`, its marks are then
  dropped by `_drop_role_marks`, `--cwd`/`--` stay a second argv road, writer rows without `--collect` stay unresolved
  (FR-16 unmet by default), the copied-`generated_from` hole stays. (b) One resolver at store in this node (F4's text): owns
  14 + 2 conditional (+12/+14 over the pile row: `manifest_put.py`, `probe_debt.py`, three tests, six texts/registries, the
  changelog fragment); one collect per write; the hole closed. (c) A shared core now (`manifest_put.resolve_rows(rows, argv,
  cwd, timeout)`, writer calls it with its argv; owns ~6) and the store-of-all plus the hole in a named node RD1-36: two
  argv roads and two refusal meanings live until RD1-36, and the writer's marks are still dropped. Recommendation (b): the
  smallest change that is one road; (a) is a clone that P31 refuses, (c) pays the shared-core refactor and then deletes half.
- F2 — the `--collect` flag (with the axis-3 `narrows` line). (a1) accepted and inert with a note for old briefs; (a2) removed
  (an old brief's call dies on argparse, exit 2); (b) kept as an early check that calls `stamp_node_ids` on a dry run only
  (same road, a second collect when the role also writes). Narrows under all three: a project with no pytest-shaped
  `test_command_templates` that relied on `-- <cmd>` reads `not_verified` (covering it = a second argv road, which P31
  refuses, or the key filled at onboarding, which exists). Recommendation (a1); the note names `test_command_templates`.
- F3 — the author's spelling after a store rename (writer row form, `probe_debt._rebind`). (a) a public
  `manifest_put.asked_spellings` both call (owns +`probe_debt.py`, `test_probe_debt.py`); (b) `contract.instance_id_aliases`
  gains `asked` - every alias reader and the merge identity change (wide, needs its own reader block); (c) the writer's form
  only, `probe_debt` as a finding to its pile - but that regression is created HERE (writer rows the store renames stop
  rebinding, a stable keep), so (c) leaves this node's defect open. Recommendation (a).
- F4 — a non-pytest file asked in the same collect as Python rows. (a) accept: the store asks every row with a file
  (FL1 F6); if pytest errors on the alien path the whole batch reads `not_verified` (safe side; estimate: pytest's exit for
  a `.ts` path given on the command line was not measured - the Lead runs `python -m pytest --collect-only -q
  tests/x.spec.ts` in a stand); (b) ask only rows whose file the runner row can collect, by a capability key of
  `collect_forms` - a universality-pile node (FL1 F6's). Recommendation (a), the case attached to the F6 node.

## §8 Small choices closed

- Name `asked_spellings`; an ambiguous `asked` maps to none (safe side). - The FR-16 test block moves into `fr16_store_road` so it
  can be called narrowly. - The writer's notes keep FR-41's "say so" through the store's printed lines, not a second line.
- No new module, no new test file, no new config key.

## §9 Trail

Read: pile `batch-1-phase-2.md` (Grep RD1-35/RD1-19: :63); FL1 card :395-425, :470-484 (F3-F8, Lead decisions, node id);
`manifest_from_tests.py` :320-344, :1280-1304, :1432-1471, :1628-1657, :1706-1988; `manifest_put.py` :873-1142, :1815-1828,
:2884-2908 (+ Grep `def`/`WRITER_MARK`/`id_notes`); `node_ids.py` :740-812 (+ Grep `def`); `s5.md` :294-309;
`test_manifest_put_assertion_line.py` :200-389 (+ Grep); `test_manifest_from_tests.py` :440-505, :1915-1954, :2225-2234,
:2306-2327 (+ Grep `def`); `test_node_ids.py` :606-650; `probe_debt.py` :100-104, :523-619 (+ Grep); `contract.py` :4075-4111;
`execution_request.py` :3606-3619 (selectors are built from the request, so the author's `selector` is not this node's);
`design/architecture.md` :33-72, :173-219, :316-321; `docs/TESTING.md` :75-104; `test-layers.json` :1-40, :2925-3014,
:3382-3397; `slow_tests.json` :1-90; `templates/config.json` (Grep); `stage-joints.json` :3588-3603; judgment-census (Grep);
`changelog.d/rules-debt-1-rd1-19-fl1-pytest-id.md`. Negatives with controls: SIBLING_MAP node-id axis 0 (control
`hooklib.read_json`); census rows 0 (control :601-605); `tools/` 0 (control: scripts 23); `agents/qa-automator.md`
`(?i)collect|unverified|instance id` 0 (control: the same call on `s5.md`: 9 hits).
Not run: any test, `owns_readers.py`, `scenario_walk.py`, pytest on a `.ts` path (F4 estimate). Needed beyond the manifest
(read only): `probe_debt.py`, `contract.py`, `execution_request.py`, `stage-joints.json`, the tests and registries above.

## Lead decisions (t-1351 accepted, 18.11.2026, Lead 501cb4e0)
- F1 (b): one resolver at store in this node; owns per §5 (16 paths).
- F2 (a1): `--collect`, `--cwd` and the `--` command accepted and inert, with the note naming `test_command_templates`.
- F3 (a): public `manifest_put.asked_spellings`, read by the writer's row form and by `probe_debt._rebind`.
- F4 (a), measured: `python -m pytest --collect-only -q <dir>/test_a.py <dir>/x.spec.ts` exits 4 ("no match in any of
  [<Dir ...>]") and collects nothing, the Python file included. A mixed batch therefore reads `not_verified` as a whole: the
  safe side (never `verified` without a collected match). The builder pins this outcome in one row of the §5 tests and
  names the case for FL1's F6 node in the report.
- §6: `tools/owns_readers.py` run by the Lead on origin/main 52e412df: the name readers are test_manifest_from_tests.py,
  test_manifest_put_keep_unsent.py, test_node_ids.py, test_probe_debt.py -- all in §5 owns; nothing new.
