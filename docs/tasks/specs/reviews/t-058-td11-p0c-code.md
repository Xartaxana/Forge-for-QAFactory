# t-058 — critic gate on TD-11 phase 0, node P0-C (builder t-049 / report t-046)

Diff under review: uncommitted changes in worktree `C:\QAFactory\forge-repo\.claude\worktrees\agent-ad3321fcff754c33f`
(HEAD eb9f82e), 17 files, +110 / -191. Spec: `td-11a-driver-split.md` §4 (P0-C table, rule F3) as overridden by
`td-11-lead-brief.md` «Сведение спек» (item 1: no patch helpers, P0-B and P0-D dropped; item 12) and «Правки после критика на
план» (item 3: `test_story_run_s6.py:2039`, `test_driver_chain.py:1104`).

**Verdict: NEEDS WORK (fit_with_fixes). 0 blockers on the diff as it stands today, 1 fix that must land before P1-2 (F1),
3 small fixes for this round (F2-F4), 2 nodes proposed for the Lead to open (N1, N2).** The ports are equivalent or
stronger over today's three-file set (`story_run.py`, `driver_chains.py`, `driver_timing.py`). I traced each one and re-ran
the source-only ones. The deletions are source pins under rule F3. One deletion takes the only check on a piece of wiring
(N1). The node's purpose is not complete in one owned file: the `test_words_doors` inventory goes red at the cut, and it
was queued to P0-D, a node the brief has dropped (F1).

## (a) Ported functions: one line per row of the builder's table

| Function | Over today's set | After the cut | Note |
|---|---|---|---|
| walk_lanes `story_run_makes_no_new_thread_site` | stronger. Old: `story_run.py` count == 1. New: set count == 2. Re-run: `story_run.py:1954, driver_chains.py:394` | holds: the watcher site moves to a part and is still counted | equality on a count, not on identity: a lane thread that replaces a deleted site keeps the count at 2. Same weakness as before. The sites are printed in the check name, so not a finding. `run_chains(items` checks deleted per the spec row |
| stop_record `story_run_has_no_private_appender` | stronger (every file, file:line in the message) | holds | the added `len(sources) >= 1 and all(text …)` check is redundant: `driver_sources` already raises on a missing `story_run.py`. It is also a self-check of the kind TESTING.md l.98 lists as "not written". It makes nothing vacuous -> F3 |
| refusals `refusal_every_action_has_a_move` (census half) | equivalent (`driver_text()`) | holds | the deleted tail (literal `kind ==` inside `dispatch_action`) was the census's guard against vacuity for 11 kinds. Without it, a `kind == "x"` anywhere in the set satisfies the census. It is a source pin of one member under F3, so the deletion follows the spec. Recorded as a weakening the spec chose, not a defect of the diff |
| refusals `cc9_findings` / CC9 census | equivalent. The list-of-texts form parses each file on its own; `functions` is the union. Re-run green. Planted control in a SECOND text: `['site:other:3:close_by_code']` (seen) | holds: watched methods in any part are found; `missing:` works over the union | problem strings lose the file name (line only). Cosmetic |
| refusals F-3 counts (1, 4) | equivalent over `driver_text()` | holds: the count is over the set, not tied to one file | — |
| s0 `k5_the_agent_is_never_called` | equivalent | holds | — |
| s6 `d1_texts` | equivalent. Nodes of all files are kept in one list, so the `id()` dedup of f-string parts stays sound. Re-run 8/8 | holds: `count == 2` is over the set, both S5 repair texts are counted wherever they land | — |
| s6 `t329_b270_g` | equivalent. Re-run 5/5 | holds as a joined-text check | if the cut tool rewrites line 72 (`from controller import MANUAL_WINDOW_CASES, lane_keys, …`) into an import whose first name is not `MANUAL_WINDOW_CASES`, the substring check goes red. Loud, not vacuous. Tell the P1-2 builder |
| s6 `c16b` SITE_MOVES (brief item 3, :2039) | stronger: every `SITE_MOVES = ` assignment in the set, with a non-empty guard (`len >= 1`, so `all()` of nothing cannot pass) | holds | — |
| words `words_no_other_site_hands_the_words_over_inline` | equivalent. Regex counts only, no `ast.parse` of the joined text (checked: `count_sites`, `FILE_READER`, `inline_option_sites` at test_story_run_words.py:127-138) | holds | module docstring l.18 still says "no other site of story_run.py" -> F4 |
| words_doors `driver_inline_calls` | equivalent. Re-run: `['story_run.py:20794', 'story_run.py:20839']`. Its only caller (l.394) uses `len`/`str`; no other caller in the worktree (grep over the tree) | holds | but see F1: the rest of `part_detector` does not hold |
| window_record S10 | stronger (every file of the set) | holds | changed function not run (slow file, the Lead's list); module imports clean |
| s7 `hits` / `raw_hits` with `DRIVER` | stronger: `found == len(functions)` over the set, so a second definition of `failures_to_triage` in another part turns red. Re-run of the function: all PASS | holds | the two scanners are near-copies, and the diff grew both the same way -> F2 |
| ticket_adapter FEFF | stronger | holds | — |
| driver_chain `scheduler_module_knows_no_stage` (brief item 3, :1104) | stronger: identity + `__module__` + MRO `vars`. Control: a subclass that redefines `run_chains` gives `['Bad', 'DriverChains']` and identity `False`, so it fails as DoD 5 asks | holds after the cut, where `Driver.__dict__` is empty of mixin members | — |
| s6 `_words_door` member getsource (:2027), LEFT | n/a | does not break: inherited members resolve to function objects, and `inspect.getsource` follows `co_filename` | an F3-class source pin left alive -> N2 |

No port weakens a census over today's set. None is tied to a count in one file. None becomes vacuous.

## (b) Deleted checks

| Deleted | Source pin? | Behaviour left / lost |
|---|---|---|
| knowledge_notice `test_gate_repair_calls_notice_after_kept_answer_branch` | yes (order inside `Driver.gate_repair`) | **lost: the wiring.** Grep `notice_from_handoff` over `scripts/`: the only test callers are test_knowledge_notice.py:87 and :181, which call `PK` directly. No test drives `gate_repair("A")` and sees the notice. A case-insensitive grep for `project_knowledge` / `knowledge` over `test_story_run*.py` finds no such scenario. Per F3 the deletion stands; the uncovered wiring -> N1 |
| walk_lanes `run_chains(items` checks | yes | the lanes' scheduler behaviour is covered by test_driver_chain (170/170) |
| refusals `dispatch_action` literal tail | yes (one member) | see (a): the census is weaker, as the spec chose |
| conductor_doors c26 (2 lines) | yes (prompt text of `Driver.conductor`) | the rest reads data (conductor.md, `rework_stage` row, `no_move.moves_section`): not vacuous |
| gate_brief t409_h3 (3 checks) | yes | the driver's use of `relay_card_line` is still proved by behaviour in the next function, `test_t667_d17…` (l.2357-2376): it calls `Driver._relay_note` and asserts `takes every option above`. The remaining `relay_card_line`/s4.md checks are real. Not vacuous |
| s0 k6 source check | yes | kept `not hasattr(story_run.Driver, "RETRY_AT_RE")` is a tombstone. It fails only if the name comes back as a CLASS attribute (after the cut a module-level constant in a part would pass). The behaviour (F3 negative control: the time in the sentence is not read) is the check above it -> F3 |
| s0 `s0_owners_of_a_failed_read` K-F10 | yes | `driver.direct_api_usable() == True` kept (behaviour). Not vacuous |
| s0 `s0_unread_road_units` G1 | yes (caller shape) | the F4 `s0_doors` behaviour checks stay. Not vacuous |
| stand_identity k37 tail | yes | the order "stand before build" is proved by behaviour in the kept part (l.914: an unconfirmed stand asks `environment`, no build probe; l.918, l.926). Not vacuous |
| words `words_the_arrival_road_hands_no_words_over_inline` | yes (five member bodies) | removed from `main` too; no other reference in the tree |
| controller_gate `rn1_20_k_d2` (fork 2) | **yes, both halves.** The controller half pinned the body shape of `Controller.accept_order` (`self.store.read()`, no `json.loads`) | the behaviour behind it is covered: K-D1 E-D3 in the same file (l.741-755: an unreadable log, no log, a corrupt tail line and an incomplete final event each give `{}`), and test_story_run_gate_repair.py:819-825 (`Driver.accept_order` through the controller's verified read; a broken chain gives `{}`). **Fork 2: leave it deleted** (proposal; the Lead decides) |

Fork 1: deleting only the source read and keeping the behaviour checks is the right reading. Nothing vacuous is left, apart
from the k6 tombstone (F3).

## (c) The six slow files plus the two that timed out

- `python -m pyflakes` over all 16 changed test files: no `undefined name`, no `imported but unused`. Positive control of the
  same tool via `pyflakes.api.check` on an inline bad snippet reported both kinds.
- Imported in one process: test_story_run_refusals, _s0, _s6, _stand_identity, test_words_doors, test_gate_brief_and_retro,
  test_controller_gate_decision, test_window_record: `imports ok`.
- Call signatures: `driver_sources(plugin_root)` (positional root) matches `harness.driver_sources(root=PLUGIN_ROOT,
  exempt=None)`. `driver_text()` takes no argument at every site. `harness` is imported where `harness.` is used
  (stop_record, walk_lanes added it; refusals/s0/s6 already had it); the others import the name.
- The CC9, d1, t329 and thread functions ran green from the imported modules (Trail).
- Not run: k5's rig half, c16b's rig half, window_record S10, and the CI files as wholes.

## (d) Remaining readers and the builder's analogs

- **F1 (must land before P1-2, owned file, recommended this round).** test_words_doors.py `scan()` (l.194) and
  `converted_doors()` (l.237) read every `scripts/*.py` by glob and key the results by file path. `PENDING` (l.81) and
  `expected` (l.389) name `scripts/story_run.py`. Every `person_words.door(` call (story_run.py:9641, 20175, 21845) and
  both PENDING waiver texts sit inside `class Driver` (l.1081-22092), so the cut moves them into `driver_*.py` parts. Two
  failures follow: (1) `unlisted` gains `scripts/driver_<part>.py`, so "no inline door outside the exemption and the
  pending list" goes red; (2) `expected` misses `story_run.py`, so "the files whose doors were converted call
  person_words.door()" goes red. The loop also prints a false "clean now: remove scripts/story_run.py". These are loud
  failures, not blind ones, but they are certain. The builder queued them to "P0-D or P1". P0-D no longer exists (brief
  «Сведение спек» item 1, «Правки» item 12), so the queue pointer leads nowhere (rule 5: not queued). Direction (the Lead
  decides): one key for the driver set, e.g. map every path in `driver_sources(plugin_root)` to `scripts/story_run.py`,
  or to a named key `driver set`, in both `scan` and `converted_doors`. Leave the synthetic fake-package control as it is
  (`driver_sources(fake)` works: the fake has `story_run.py`).
- conductor_doors l.108, 465, 467, 534-535 and s6 l.2027 (`inspect.getsource(story_run.Driver.<member>)`) do not break and
  do not go blind after the cut. They can stay through P1-2. The same form exists in roughly 20 more sites in other files
  (case-insensitive grep: test_first_look_step:376, test_place_session:381-541, test_manual_actor:375,
  test_s8_reporting_regressions:671, test_walk_supply:341-434, test_walk_account:178-451, test_unprepared_outcome:213).
  All are F3-class pins outside this node -> N2.
- test_answer_rework_pairs.py:148 (`Driver.__dict__["answer_pairs_owed"]`) raises KeyError after the cut. It is
  quarantined and, per brief item 3, the Lead marks it. Listed here so it stays tracked.
- Seam for the controller wave (not P0-C): refusals l.453-455 reads `controller.py` by path and cuts at
  `\n    @staticmethod`. It breaks when spec B cuts `controller.py`. The owner is the controller mirror node.
- No other reader in the 16 files: grep for `story_run.py`, `getsource`, `__dict__`, `vars(`, `__file__`, `co_filename`
  over them. The remaining hits are command text (`run_script("story_run.py" …)`), docstrings and instance dicts.

## (e) Standing items

- **Fit to spec**: all rows of §4 done. Patch rows were dropped by «Сведение» item 1, correctly not done. Spec l.232 says
  "harness's reader becomes one row"; not done, but moot: `harness.py` is in `L8_SKIP` (test_driver_layers.py:36-37,
  P0-A). The report says 22 rows were removed; the diff removes 21 `source_readers` rows (23 `-` row lines, 2 re-added:
  the `test_story_run_codex` row moved, `part_detector` 8 -> 7). Minor inaccuracy in the report.
- **Ratchets (item 9)**: driver-layers L8 rows shrink only (21 removed, one mention 8 -> 7). No raise.
- **DUPLICATION AND CONSISTENCY**: every port goes through the one reader, `harness.driver_sources`/`driver_text` (grep of
  `driver_sources|driver_text` over the 16 files: 13 call sites, none bypasses it). Inside the diff, s7 `hits` and
  `raw_hits` (test_s7_null_outcome.py:1033-1047, 1074-1085) are the same loop with a different regex and label -> F2.
  Consistency: F3 was applied to `read_text` pins in conductor_doors and s6 but not to member `getsource` pins in the same
  two files. The spec scoped the node by L8 literal rows, so this is not the builder's defect -> N2.
- **CODE QUALITY**: no new function over 60 lines or nested more than three levels. Stale module docstrings:
  test_driver_stop_record.py:12 ("left in story_run.py") and test_story_run_words.py:18 -> F4. The redundant self-check
  in stop_record -> F3.
- **ARCHITECTURE**: AR-13 kept: one reader of the driver set, and the ported sites go through it. Exception: F1's
  inventory, which reads `scripts/*.py` (a different fact, but keyed by the driver's file). AR-15 kept: the thread census
  survives as a set census. AR-22 kept: map rows match the literals, L8 green on re-run. The report names all three. The
  package commit still needs its `architecture:` and `judgment:` lines (no commit yet).
- **JUDGMENT**: none. No package code changed, no census row, no role text.
- **ONE ROAD**: none found. Grepped the diff for language/project/case branches; it has none. All censuses take one road
  (`driver_sources`).
- **Tests (item 5)**: the deletions REMOVE TESTING.md l.94 pins. No pin is added, except the stop_record self-check (F3).

## Fixes (this round; fresh worker with this verdict and the diff)

- **F1** test_words_doors.py l.81, 194-213, 237-252, 389: key the inventory's driver entries by the driver set so that
  `unlisted` and `expected` survive the cut. Witness: `part_detector` green today. A planted control is also welcome: a
  copy of a PENDING driver text under a fake `scripts/driver_x.py` must count as listed. Blocks P1-2, not this merge.
- **F2** test_s7_null_outcome.py l.1033-1085: one scanner taking `(pattern, path, functions, label)` instead of the two
  copies. Fix before merge if cheap; otherwise queue.
- **F3** test_driver_stop_record.py l.327: drop the `len(sources) >= 1 and all(text…)` self-check.
  test_story_run_s0.py l.854: drop the `RETRY_AT_RE` tombstone, or keep it with a reason (the Lead's choice).
- **F4** docstrings test_driver_stop_record.py:12 and test_story_run_words.py:18: say "the driver set".

## Proposed nodes (the Lead opens them; rule 6)

- **N1** behaviour scenario for the gate-A notice wiring. Drive `Driver.gate_repair("A")` with a kept answer in a rig. Spy
  `project_knowledge.notice_from_handoff`: called exactly once, with `pipeline.ticket or <folder>`. A raise inside it does
  not break the gate. Owner: TD-11 batch (Lead), or the project-knowledge pile.
- **N2** the member-level `inspect.getsource(story_run.Driver.<m>)` pins (about 26 sites, listed in (d)): classify them
  under F3 after the cut. Delete them, or port them to behaviour. Owner: Lead; not blocking P1-2.

## Not checked

The slow files as wholes (CI judges them). The rig halves of k5/c16b/window_record S10. `tools/dup_ratchet.py` (not run
here). Whether the cut tool's emitted imports keep `from controller import MANUAL_WINDOW_CASES` as a prefix (t329 note).
Readers outside the 16 files that do not carry a `story_run.py` literal (L8 cannot see them); only the getsource form was
grepped repo-wide. A scout is needed for glob-based readers if the Lead wants them enumerated.

## Trail

Read: the full diff (`git -C <wt> diff`); report t-046; td-11a §4 l.191-254; td-11-lead-brief l.158-255; harness.py
l.54-73; test_driver_layers.py L8 l.30-37, 564-622; driver-layers.json `not_driver`, harness rows; critic-diff-brief
l.25-101; TESTING.md l.80-110; test_words_doors.py l.36-405; test_story_run_refusals.py l.450-479, 3100-3178;
test_story_run_s6.py l.240-273; test_story_run_stand_identity.py l.886-960; test_gate_brief_and_retro.py l.2330-2376;
test_story_run_words.py l.47, 127-138. Greps: `threading.Thread(`/`run_chains(` over story_run+driver_*; `notice_from_handoff`;
`accept_order`; `take_stand_gap_answers`; `record nothing for another word`; `relay_card_line`; `getsource`/`__dict__`/`vars(`
(16 files, then all tests, case-insensitive); `story_run.py` literals in the 16 files; deleted function names over the tree;
SIBLING_MAP for driver-set readers (no axis for test readers of the driver source; the census lives in driver-layers.json).
One slip in my own commands: one Bash call carried a no-op `cd /dev/null` (it failed; no effect).

Re-runs (verbatim tails):
- `python -B …/tests/test_driver_layers.py` -> `=== test_driver_layers: 58/58 ok ===`
- in-process import of the 8 slow or timed-out modules -> `imports ok`; CC9 census + 9 controls PASS; `d1_texts` 8 PASS;
  t329 5 PASS; `PASS AR-15: the driver set has TWO threading.Thread( sites …: story_run.py:1954, driver_chains.py:394`;
  `inline calls ['story_run.py:20794', 'story_run.py:20839']`; `cc9 planted 2nd text ['site:other:3:close_by_code']`
- in-process `scheduler_module_knows_no_stage`, `story_run_has_no_private_appender`, `one_definition_no_local_set_building`
  -> no non-PASS line; subclass control `['Bad', 'DriverChains'] False`
- `python -m pyflakes <16 files>` -> no output; control `pyflakes.api.check` on a bad snippet -> `'os' imported but unused`,
  `undefined name 'y'`, `warnings 2`

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 test_words_doors.py l.81/194-213/237-252/389: scan() and converted_doors() key the driver by scripts/story_run.py; after the cut the door() calls (story_run.py:9641,20175,21845) and the PENDING texts move to driver_*.py parts, so unlisted and expected go red. Key the driver set as one entry. Must land before P1-2; the builder queued it to P0-D, which the brief dropped.",
    "F2 test_s7_null_outcome.py l.1033-1085: hits and raw_hits are one loop copied; make one scanner parameterised by pattern and label (fix if cheap, else queue).",
    "F3 test_driver_stop_record.py l.327: drop the redundant non-empty self-check (driver_sources raises already); test_story_run_s0.py l.854: drop the RETRY_AT_RE tombstone or give it a reason.",
    "F4 docstrings test_driver_stop_record.py:12 and test_story_run_words.py:18 still name story_run.py: say the driver set."
  ],
  "class_completeness": "Within the 16 owned files every story_run text reader is ported or deleted except the test_words_doors inventory (F1). The member-level inspect.getsource(story_run.Driver.<m>) pins (conductor_doors 108/465/467/534/535, s6 2027, and about 20 more in other files) do not break after the cut; proposed node N2. The quarantined test_answer_rework_pairs.py:148 Driver.__dict__ read breaks and stays with the Lead per brief item 3. SIBLING_MAP has no axis for test readers of the driver source; the census lives in driver-layers.json source_readers (L8 green, rows shrink only). The gate-A notice wiring lost its only check with the deleted pin; proposed node N1.",
  "trail": {
    "read": [
      "git -C .claude/worktrees/agent-ad3321fcff754c33f diff (17 files)",
      ".claude/worktrees/agent-ad3321fcff754c33f/docs/tasks/specs/reports/t-046-td11-P0-C.md",
      "docs/tasks/specs/td-11a-driver-split.md l.191-254",
      "docs/tasks/specs/td-11-lead-brief.md l.158-255",
      "ai-packages/qa-factory/scripts/tests/harness.py l.54-73",
      "ai-packages/qa-factory/scripts/tests/test_driver_layers.py l.30-37, 564-622",
      "ai-packages/qa-factory/scripts/tests/test_words_doors.py l.36-405",
      "ai-packages/qa-factory/scripts/tests/test_story_run_refusals.py l.450-479, 3100-3178",
      "ai-packages/qa-factory/scripts/tests/test_story_run_s6.py l.240-273",
      "ai-packages/qa-factory/scripts/tests/test_story_run_stand_identity.py l.886-960",
      "ai-packages/qa-factory/scripts/tests/test_gate_brief_and_retro.py l.2330-2376",
      "docs/tasks/critic-diff-brief.md l.25-101",
      "docs/TESTING.md l.80-110",
      "docs/SIBLING_MAP.md (grep driver set readers)"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_driver_layers.py (worktree)", "result": "=== test_driver_layers: 58/58 ok ==="},
      {"command": "python -B -c import of 8 slow/timed-out test modules + CC9 census, d1_texts, t329, thread sites, driver_inline_calls, cc9 planted in a second text", "result": "imports ok; all PASS; story_run.py:1954, driver_chains.py:394; inline calls story_run.py:20794, story_run.py:20839; planted site:other:3:close_by_code"},
      {"command": "python -B -c scheduler_module_knows_no_stage, story_run_has_no_private_appender, one_definition_no_local_set_building + subclass redefining run_chains", "result": "no non-PASS line; subclass MRO list Bad, DriverChains; identity False"},
      {"command": "python -m pyflakes on the 16 changed test files, with a pyflakes.api.check control", "result": "no findings; control reports unused import and undefined name"}
    ]
  }
}
```
