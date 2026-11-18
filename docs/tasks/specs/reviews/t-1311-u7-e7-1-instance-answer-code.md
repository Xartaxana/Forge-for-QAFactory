# t-1311 - code review of node E7-1 (another-instance answer: key, reader, verb, conductor row)

Reviewed: commit `cf5a9bf6` on branch `worktree-u7-e7-1` (worktree `C:/QAFactory/forge-repo/.claude/worktrees/u7-e7-1`), builder t-1306.
Spec: `docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md`, card "E7-1" (Work 1-5, Edges, Tests), context sections 1, 2.5, 2.8, 6.
Merge base `25fbd8bc`; origin/main is `ef3e8a26`, but no touched file (nor `guard_pre_tool.py`) changed between them (`git diff --stat 25fbd8bc ef3e8a26 -- <files>` printed nothing).

Terms used below. The **registry** is `qa-factory/records/project-knowledge.json`, an append-only list of rows ("facts"), each with a key,
a stand (`environment`), an element, a `value`, the person's words and a time `at`; a **revoked** row keeps its place and gains `revoked_at`.
The **reader** is the new `project_knowledge.instance_answer(root, stand, need)`; `authorized: None` means "no answer, ask the person".
The **verb** is the new CLI subcommand `project_knowledge.py instance`. A **role** is a factory sub-agent (runner, critic, ...); the
**conductor** is the orchestrator session that runs registry verbs on a person's answer.

## Verdict

**NEEDS WORK** (one blocking finding, F1; F2, F3 and F5 to fix before merge; F4, F6-F8 notes). The decision to accept belongs to the Lead.

- Fixes that block the merge: F1 (`project_knowledge.py::instance_answer`, and the assertion at `test_project_knowledge.py:1345`).
- Fixes before merge: F2 (`guard_pre_tool.py:1869`, outside the node's owns: the Lead widens the round), F3 (`project_knowledge.py::_story_stand`), F5 (module docstring, `project_knowledge.py:18-25`).

## Keys

**K1 - the reader's error direction: holds.** I probed it with a scratch script (Trail, run 3). Every broken input gave `authorized: None`, and none raised:
schema 2 gave a `problem`; `facts` not a list gave a `problem`; a top-level list gave a `problem`; `{not json` gave a `problem` (the committed test);
`root=None` gave a `problem` (TypeError, caught); `{"authorized": 1}` and `{"authorized": "no"}` gave None; an element with a trailing space gave None;
`need=None` and `need=["another_instance"]` gave None; `stand=object()` gave None; the placeholder stand gave `no_stand: True`; a newer bad-valued row over an older yes gave None (the safe direction).
A missing catalogue row returns `CATALOGUE_PROBLEM`, the same code shape as `lessons`.
Two weak points did not break the key: a DIRECTORY at the registry path reads as an absent file (no `problem`), which is `environment_record.load_rows`' shared behaviour (`is_file()`), so it is not this node's;
and rows in a state other than `known` are read (F4).
The one way I found to get a True from input that should read as unknown goes through revoke, not through a broken file: F1.

**K2 - the latest row wins, same answer twice, revoke, other stand: fails (F1).** What holds: the latest row wins (yes then no reads False). The same answer twice gives `already recorded` and no second row (the test checks `len(proj.rows()) == 2` after yes, yes, no).
`Dev` vs `dev`, a stand with a trailing space (written or read) and a non-ASCII stand (`стенд-1` recorded, read True; `СТЕНД-1` read None) are never read for one another. All of these lean toward asking.
What fails: revoking the NEWEST row brings back an OLDER live answer. yes (PK-3), then no (PK-4), then `revoke PK-4` (the person's `ask again`) makes the reader return **True**.
The printed line at the same time says "it is asked again where it is needed". So a revoke that should leave no answer turns into a yes. Reproduced in Trail, run 4; the committed test asserts this behaviour as intended (line 1345).

**K3 - the verb as outside input: holds, with weak asserts (F7).** The DoD run is green. Every refusal row of `INSTANCE_CLI` (empty, BOM-only, whitespace, UTF-16, invalid UTF-8, `--stand " "`, no stand, no-trace) asserts
`not proj.path().exists()`, so "nothing written" really is checked and not only the exit code. The 210 KB row checks that the words are recorded whole, and the BOM row checks that the BOM is stripped.
The three argparse rows (`--need bogus`, `--allowed YES`, `--allowed ""`) check `SystemExit` and the absent file, but not exit code 2 and not which option was refused. The "no stand" row checks only `pass --stand`, not the stand list.
The list is printed (`... (the stands: `dev`, `prod`)`, Trail run 4), and `test_project_knowledge.py:899` already asserts it through the shared `_story_stand`.

**K4 - the `record_problems` position: holds.** The new branch is one `elif key == EXTRA_INSTANCE_KEY` inside the existing chain (`project_knowledge.py:772`), placed after `LESSONS_KEY` and before `SIGN_IN_KEY` and the role rules.
Because the chain is keyed by `key`, no other key can reach it, and the extra-instance key never reaches the role rules. That is the invariant the position must keep: every other key's rows are judged exactly as before.
The 171 existing and new tests of the file are green, including the lesson, side, sign-in and role refusals.
The committed test asserts refusal for `{"authorized": "yes"}`, an extra key, `None`, `{}`, `[True]` and element `""` (lines 1347-1351).

**K5 - `cmd_revoke`: holds.** The only change is the tuple `(ROLES_KEY, ACCOUNTS_KEY, EXTRA_INSTANCE_KEY)` at `project_knowledge.py:1067`; both printed sentences are byte-identical to before. But the "asked again" sentence is false for this key until F1 is fixed (see F6).

**K6 - one writer, one reader, one home: holds.** I ran a case-insensitive Grep over the worktree's `ai-packages` for `extra_instance|another_instance|INSTANCE_NEEDS|EXTRA_INSTANCE_KEY|instance_answer`.
Hits: `config-keys.json` 1, `project_knowledge.py` 17, `test_project_knowledge.py` 8, the changelog fragment 1. The other three hits are unrelated identifiers: `test_controller_state.py:964,2881` (`no_instance_needs`), `test_obligation_receipt_contract.py:260` and `test_probe_alternative_road.py:313` (`another_instances`/`another_instance` in other meanings).
The design texts carry prose only ("another instance"), not the literal. `--need` takes its choices from `INSTANCE_NEEDS`. No second copy.

**K7 - `needed_by` names two absent functions: confirmed, and no canon test turns red.** `def (s7_extra_instance_step|instance_lines)\b` over the package finds 0 hits. The same call shape for `def (stand_lesson_lines|check_stand_lessons)\b` finds 2, so the search works.
The only code reader of `knowledge.*.needed_by` is `test_config_migration.py:405-407` ("every row carries a reader list and a null ask_when"), which checks only `isinstance(list)`. I ran `knowledge_rows()` by import: every line PASS.
The other `needed_by` hits are unrelated: `env_probe.needed_by`, a `gate_preflight` docstring, `readiness.py:943`. `tools/` holds no reader of `config-keys`.
The existing entry `"brief_pack.py:S3-S7 briefs"` is not a symbol either, which is more proof that nothing resolves these names.

**K8 - texts: holds for words; the pins hold.** No text a person or the conductor reads uses "authorized". The single exception is the refusal at `project_knowledge.py:776`, which names the data key `{"authorized": true|false}`; no CLI input reaches it, because the verb always passes a typed bool. Spec section 6 keeps `authorized` as the data key. No platform or brand word.
The conductor row has the same shape as the stand-lesson row (`says` "... meant for later stories too"; `run` "... --words-file <file holding their words>; a story that leaves no trace refuses it"), and `actions_problems` on the live file returns `[]`.
Pins: both design edits are one-line in-place replacements (`@@ -53 +53 @@` and `@@ -167 +167 @@`), so no line moved. No `test-layers.json` pin names `architecture.md:53` or `state-exits.md:167` (0 hits; the same grep finds `architecture.md:256` twice).
The builder is right that the axis 7 row is at line 53. Line 256 is a dev-tools bullet, so the spec's pin was wrong.
The `state-exits.md` sentence "revoking an `instance` answer makes the question speak again at the next need" is false until F1 is fixed.

**K9 - tests against the budget: holds on volume, fails on one expected value.** numstat: product +76 (70 code, 6 text and data), tests +61 (-2). Rows, strongest first: the round trip (yes, read back, same twice, the other answer wins, other stand, revoke), the value-shape loop, unreadable registry, the CLI battery.
The value-shape loop kills a reader that does not check `value` (it would return `"yes"`).
The expected value at line 1345 (`ask()["authorized"] is True # the older live row reads again`) traces to no spec clause. The spec says "revoked -> None (INV: revoke makes it ask again)" and, in 2.8, "the row reads as nothing, the next need asks": a Q5(b) finding, part of F1.
No row fails to assert anything. Edges with no row: a non-ASCII stand and `--stand ""` are both listed as "not written, by budget" in the spec card itself (line 256), so they are not findings. I probed both (Trail, run 4): the non-ASCII stand is recorded and read exactly; `--stand ""` falls back to the chosen stand and is refused with the stand list when none is chosen.

**K10 - readers of the touched files: holds.**
- `test_config_migration.py::knowledge_rows` (lines 389-411): the new key has a dot, so it is outside the top-level template comparison (line 376), and its `needed_by` list and null `ask_when` pass line 405. Run by import: all PASS.
- `test_conductor_doors.py`: `actions_problems` (line 287) needs `says` without `.py` or `--x`; the new `says` has neither, and the live call returns `[]`. Lines 978 and 913 read rows by id or move, `NM.reserved_tokens` reads `moves` only, and the new row has no id.
- Other readers of `conductor-actions.json` `actions` pick rows by content: `test_walk_supply_config.py:315` (ids), `test_probe_container_answer.py:244` ("names the container"), `test_probe_gap_door.py:115` ("probe gap"), `test_needs_author.py:396`, `test_check_delivery.py:485` ("--operation rework"), `test_words_doors.py:1751` (id). None counts all rows, and the new rows match none of their patterns.
- `config-keys.json` `knowledge` key lists: `test_project_knowledge.py:987-1003` (updated, green). One reader not named by the spec or the builder: `report_facts.py:2227` iterates `PK.KEYS`, so a known extra-instance row becomes a reach entry. Its `used` is unmeasured (line 2250), so `available_unused` is None and the row is never counted as a fact nobody used (line 2207). No red, and no false signal.

## Findings

**F1 - blocking. `ask again` after a changed answer reads the older answer: a revoke becomes a yes.** Surface: the reader's choice of row (`instance_answer` -> `_latest`, which skips revoked rows and so falls through to an older live row).
Reproduction (Trail, run 4): `instance --allowed yes --stand dev` (PK-3), `instance --allowed no --stand dev` (PK-4), `revoke --id PK-4`.
The verb prints "PK-4 is taken back (environments.extra_instance another_instance): it is asked again where it is needed; ...", yet `instance_answer(root, "dev", "another_instance")["authorized"]` is `True`.
This breaks the card's edge "revoked -> None (INV: revoke makes it ask again)", section 2.8, the builder's own `state-exits.md` sentence and the revoke line. Once E7-3b reads the key, a person who said yes, then no, then `ask again` gets another instance started without being asked.
Neighbouring classes walked: revoking the older row instead of the newer leaves the newer answer in force (correct). Revoking the only row gives None (correct). Two revokes give None (correct). A newer row with an unparseable `at` loses to an older yes (`_latest` treats it as the oldest; existing rule, hand-edit only).
Smallest fix: in `instance_answer`, pick the newest row of the subject INCLUDING revoked ones (same key, stand, element and the same `(at, index)` order), and return None when that row has `revoked_at`; otherwise use it as now. Change line 1345 to expect `None`, which is the spec's value.
Alternative (a fork for the architect, below): the revoke of this key takes back every live row of the subject.

**F2 - fix before merge (outside the node's owns: the Lead widens the round). A role can record the answer itself.** Surface: the role guard on registry write verbs, `guard_pre_tool.py:1869`, `registry_write_call(low, "project_knowledge.py", ("account", "role", "revoke", "side", "lesson", "remember", "kind"))`. `instance` is missing.
Reproduction (Trail, run 5): `G._blocked(G.human_word_check, {"agent_type": "qa-factory:qa-runner", "tool_name": "Bash", "tool_input": {"command": "python -B scripts/project_knowledge.py instance --task T --allowed yes --stand dev --words-file w.txt"}}, {})` returns ALLOWED. The same call with `lesson` returns BLOCKED.
The sibling verb `lesson` is closed to roles. A runner that needs another instance could write its own "yes" and turn its inference into the person's word, the class the guard text names ("a role running them would turn its own inference into a project fact").
In the E7-1 window nothing reads the key, so the door does nothing yet. It must be closed before E7-3b merges. The spec does not name `guard_pre_tool.py` (0 hits in the spec; the same Grep finds `project_knowledge.py` 13 times), so this is also a spec miss.
Smallest fix: add `"instance"` to the tuple at line 1869 and a clause to the refusal text near line 1786 ("`project_knowledge.py instance` stores the person's answer about starting another instance; a role running it would allow itself"). Add `"instance"` to `test_guard_project_knowledge.py:23` and `:54`.

**F3 - fix before merge (low). `--stand "this stand"` prints `recorded (PK-n)` for a row the one reader never reads.** Reproduction (Trail, run 4): `instance --allowed yes --stand "this stand"` gives exit 0 and "another_instance on this stand: environments.extra_instance recorded (PK-1)". Then `instance_answer(root, "this stand", ...)` gives `no_stand: True, authorized: None`.
The person is told the answer is kept and is asked again at the next need. That is the safe direction, but the writer produces work nobody reads (Q7), and the line it prints is not true.
The sibling `lesson` has the same gap (`lessons()` treats the placeholder as no stand). Smallest fix for the class: in `_story_stand` (`project_knowledge.py:1076`, within owns), refuse an explicit `--stand` equal to `PLACEHOLDER_STAND` with the same "pass --stand <name> (the stands: ...)" sentence. This covers both verbs.

**F4 - note (cheap fix). The reader accepts rows in states other than `known`.** Reproduction (Trail, run 3): a hand-written row in state `noticed_unconfirmed` (or `not_needed`) with `{"authorized": true}` reads True. The writer refuses such rows for stand keys (`record_problems` line 752), so only a hand edit can produce one.
Fix: `_latest(rows, EXTRA_INSTANCE_KEY, stand, need, states=(KNOWN,))`.

**F5 - fix before merge (text). The module's usage block does not list the new verb.** `project_knowledge.py:18-25` lists `show`, `account`, `role`, `revoke`, `side`, `lesson`, `lessons`; `instance` is missing. Fix: one line `project_knowledge.py instance --task T --allowed yes|no [--stand N] [--need another_instance] --words-file F`.

**F6 - note. The revoke line for this key carries the account clause** ("an account value in the project's settings stays until ..."), which means nothing for an instance answer. This is inherited from the roles branch. After F1 is fixed, its "asked again" part is true.

**F7 - note (tests).** The argparse rows check only `SystemExit`, not exit 2 and not the option named. The new tests are appended below the `if __name__ == "__main__":` block (line 1322); pytest collects them, and the script form re-runs pytest on the file, so they still run, but they sit outside the file's order.

**F8 - note (Q6 duplication).** `instance_answer` repeats the ~10-line prologue of `lessons` and `sign_in` (stand or placeholder check, catalogue check, `load`, `except` to problem). The spec prescribed "shape of `lessons`" for this node. Merging the three readers would touch two readers outside the node's purpose: a proposed node for the Lead, not a fix here. I did not re-derive the clone ratchet; its result is the branch's `forge-check` job.

## Standing questions

- Q1 fit to the spec: fails on the revoke edge (F1); every other Work item, edge and printed form is as written.
- Q2 the builder's own decisions: the `--need` default `another_instance`, `already recorded` on the same answer with different words, and the empty-words door text are all in the safe direction.
- Q3 seams: additive one-line edits, nothing reordered; the conductor row is inserted before the revoke row, and readers select by content.
- Q4 class-wide completeness: the sibling guard tuple (F2), the `_story_stand` placeholder gap shared with `lesson` (F3) and the usage block (F5) are left open. Names for the Lead: `guard_pre_tool.py:1869` and `test_guard_project_knowledge.py:23,54`.
- Q5 tests: (a) the tests kill a reader without value checks and a writer without the need check, but not F1 (they assert it). (b) Line 1345 has no source (F1). (c) The verb's door has rows. (d) No test rewritten. (e) No duplicate through the same door. (f) Within budget. (g) No new file.
- Q6 DUPLICATION AND CONSISTENCY: F8 (proposed node). The writer is the shared `record`; words come through `_write_prologue` and stands through `_story_stand`; no second reader or writer.
- Q7 CODE QUALITY: F3 (a written row nobody reads). No new function is over 60 lines or nested more than 3 deep (`instance_answer` 25 lines, `cmd_instance` 18).
- Q8 hygiene: no non-ASCII added (the `…` on `state-exits.md:167` was already there); LF kept (0 CR at main and at HEAD for all four files I checked).
- Q9 IN-TREE RATCHETS: no ratchet file touched.
- Q10 ARCHITECTURE: the commit names AR-3, AR-13, AR-24, AR-25. AR-1 holds (no platform word).
  VARIETY: an unknown stand, an unknown need or an unreadable registry leaves no answer, and the question is asked. There is no block, no silent default and no hand-off to a person beyond the question.
  The one exception to "unknown never becomes a yes" is F1.
- Q11 JUDGMENT: the `record_problems` branch is a shape check (a closed need list and a typed bool). No census or `blocks_override` edit; `judgment: none` holds.
- Q12 ONE ROAD: none found. Grep for language, runner or platform names in the diff: none; the verb goes through the shared `record`, `_write_prologue` and `_story_stand`.

## Questions for the architect

1. F1's fix: should `ask again` on this key mean "no answer" (the reader returns None when the subject's newest row is revoked: my recommendation, it matches 2.8 and the card's edge), or "take back every live answer of the subject" (the revoke verb revokes all live rows of the key, stand and need)?
   With the first, the lesson and side "previous row shows again" rule stays as it is for those keys. With the second, the reader stays generic.
2. F2 lies outside E7-1's owns: should it widen this round (recommended: two tokens and two test tokens), or become a gate on E7-3b's dispatch?

## Trail

Read: the spec card E7-1 and sections 1-2.8, 5-8 (lines 48-257, 435-514); the full diff; `project_knowledge.py` 1-44, 83-262, 440-530, 620-860, 944-1140; `guard_pre_tool.py` 1765-1879; `test_guard_project_knowledge.py` 1-60; `environment_record.load_rows` 208-228; `test_config_migration.py` 368-412; `test_conductor_doors.py` 284-295, 905-935; `report_facts.py` 2033-2041, 2205-2252; the conductor-actions readers in `test_walk_supply_config`, `test_probe_container_answer`, `test_probe_gap_door`, `test_needs_author`, `test_check_delivery`; `test-layers.json` pins (grep).

Runs:
1. `python -m pytest .../test_project_knowledge.py -q -p no:cacheprovider` -> `171 passed in 20.21s`.
2. `python -B .../test_state_exits.py` -> `=== test_state_exits: 142/142 ok ===`.
3. scratch `probe1.py` (reader probes) -> `schema 2: None + problem`; `yes,no,revoke no (ask again): {'authorized': True ...}`; `noticed state yes: True`; `not_needed state yes: True`; `root None: None + problem (TypeError)`; `dir instead of file: None, problem ''`; all other rows None.
4. scratch `test_probe_cli.py` (CLI) -> `PLACEHOLDER rc 0 another_instance on this stand: environments.extra_instance recorded (PK-1)`; `PLACEHOLDER read {'authorized': None, 'problem': '', 'no_stand': True}`; `EMPTY stand rc 2 ... (the stands: `dev`, `prod`); nothing was recorded`; `NONASCII rc 0 True None`; `REVOKE printed: PK-4 is taken back ... it is asked again where it is needed ...`; `AFTER ask-again read: True (yes row PK-3 )`.
5. guard probe -> `'instance' ALLOWED`, `'lesson' BLOCKED`.
6. `test_config_migration.knowledge_rows()` by import -> 8 lines PASS, including "every row carries a reader list and a null ask_when".
7. `test_conductor_doors.actions_problems(live)` -> `[]`, 37 actions.
8. `git diff -U0 -- design` -> `@@ -53 +53 @@`, `@@ -167 +167 @@`; pin grep `architecture.md:53|state-exits.md:167` -> 0, control `architecture.md:256` -> 2.

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1: instance_answer falls through to an older live row when the newest row of the subject is revoked: yes, no, revoke(no) reads authorized True while the revoke line says asked again; violates card edge 'revoked -> None' and spec 2.8; test_project_knowledge.py:1345 asserts the wrong value"
  ],
  "fixes": [
    "F1 (blocks): project_knowledge.py::instance_answer - return None when the newest row of the subject (revoked rows included) is revoked; test line 1345 expects None",
    "F2 (before merge, outside owns): guard_pre_tool.py:1869 add instance to the project_knowledge.py write verbs and a refusal clause near line 1786; test_guard_project_knowledge.py:23 and :54 add instance",
    "F3 (before merge): project_knowledge.py::_story_stand refuse an explicit --stand equal to PLACEHOLDER_STAND (covers lesson too)",
    "F5 (before merge): project_knowledge.py:18-25 usage block add the instance line",
    "F4 (note): instance_answer pass states=(KNOWN,) to _latest"
  ],
  "class_completeness": "Siblings by the map: the role guard tuple guard_pre_tool.py:1869 lacks the new write verb (F2, outside owns, Lead widens); the _story_stand placeholder gap is shared with lesson (F3); the module usage block (F5). One home for need words holds (K6). Report reader report_facts.py:2227 reads the new key harmlessly (K10).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md:48-257,435-514",
      "git diff origin/main...HEAD (worktree u7-e7-1)",
      "ai-packages/qa-factory/scripts/project_knowledge.py:1-44,83-262,440-530,620-860,944-1140",
      "ai-packages/qa-factory/scripts/guard_pre_tool.py:1765-1879",
      "ai-packages/qa-factory/scripts/tests/test_guard_project_knowledge.py:1-60",
      "ai-packages/qa-factory/scripts/environment_record.py:208-228",
      "ai-packages/qa-factory/scripts/tests/test_config_migration.py:368-412",
      "ai-packages/qa-factory/scripts/tests/test_conductor_doors.py:284-295,905-935",
      "ai-packages/qa-factory/scripts/report_facts.py:2033-2041,2205-2252",
      "ai-packages/qa-factory/scripts/tests/test-layers.json (pin grep)"
    ],
    "reruns": [
      {"command": "python -m pytest worktree/.../tests/test_project_knowledge.py -q", "result": "171 passed in 20.21s"},
      {"command": "python -B worktree/.../tests/test_state_exits.py", "result": "142/142 ok"},
      {"command": "scratch probe1.py (reader probes)", "result": "yes,no,revoke(no) reads True; noticed/not_needed state rows read True; all broken files read None with problem"},
      {"command": "scratch test_probe_cli.py (CLI probes)", "result": "placeholder stand recorded PK-1 but read no_stand; --stand empty refused with stand list; non-ASCII exact; revoke of newer row then read True"},
      {"command": "guard_pre_tool human_word_check probe as qa-runner", "result": "instance ALLOWED, lesson BLOCKED"},
      {"command": "test_config_migration.knowledge_rows() by import", "result": "all PASS"},
      {"command": "test_conductor_doors.actions_problems(live conductor-actions.json)", "result": "[] with 37 actions"}
    ]
  }
}
```
