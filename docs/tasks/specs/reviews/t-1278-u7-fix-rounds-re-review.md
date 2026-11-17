# t-1278 - re-review of the U7 fix rounds (stream 1, 5a, 5b, 7a) against verdict t-1271

Input: the four fix diffs `git -C <tree> diff <reviewed>..HEAD`, the Findings and K3 sections of `t-1271-u7-code-streams-1-5a-5b-7a.md`, and the Lead decisions in the dispatch. What t-1271 already judged was not re-reviewed.

**Verdict: NEEDS WORK** (JSON `blocker`, because one finding blocks a merge). Per stream:
- **7a: accept with fixes. A-1 BLOCKS.** The F7a-1 dry print raises NameError. It is a one-line fix, so this is not a REJECT.
- **5a: accept with fixes** (A-2 and A-3, fix before merge).
- **stream 1: accept** (A-4 and A-5 are low and do not block).
- **5b: accept.**

Acceptance stays with the Lead (rule 6).

## Findings

**A-1 (7a, BLOCKS the merge; K3).** `driver_machine.py:4212` (`DriverMachine.describe`, the `--dry-run` S7 branch) calls `acceptance.awaits_acceptance(...)`. `acceptance` is not bound anywhere in that function or module. `driver_machine.py` imports it only locally, inside two other methods (lines 2118 and 2258). `stage_S7` does its own local `import acceptance` (driver_stage_s7.py:55).
- Probe, after `import story_run` (the facade is installed): `eval('acceptance.awaits_acceptance', DriverMachine.describe.__globals__)` gives `NameError: name 'acceptance' is not defined`. Positive control: `DV` resolves to `detector_verdict`. `describe.__code__`: `acceptance` is in `co_names` and not in `co_varnames`.
- Failure scenario: `story_run.py --dry-run` on a story whose next action is `prepare_stage S7` (no `s7_life`) dies with a NameError traceback. NameError is not a `Refusal`, so the existing `except Refusal` does not catch it, and `story_run.main` (173) has no catch either. The old line could not raise this.
- Fix: add `import acceptance` before line 4212, as `stage_S7` does.
- Related, fix before merge: the new dry-print behaviour is a door (CLI output) with no row (Q5(c)), which is why this passed. Add one row driving `describe()` at S7 in the S7 story file. That row is the canon's to run.

**A-2 (5a, fix before merge; F5a-1 left half-fixed, Q4 neighbour in the same finding).** The fix text now says "the install command" for a table-sourced command (gate_preflight.py:2941). But the same finding's statement, one line below (2942, `f"{statement}; the project names a command that installs what its environment lacks"`), still says the project names it. With `source: "table"` (dependency_drift.py:129), the project named nothing. The 5a changelog bullet 1 carries the same phrase ("and the project names a command that installs ...").
- Fix: both should say "a command is known that installs ..." (or name the source).
- Pre-existing analog outside the 5a owns: `references/conductor-actions.json:34`, the `install_dependencies` row (on origin/main since bd99d856): "the factory has the project's own install command (the gate card or the S5 note names it)". Proposed line for the Lead's «Остатки»: `install_dependencies "says" claims the project's own command for a table-guessed one | узел: <the Lead opens it, with the K2 road-3 node>`.

**A-3 (5a, fix before merge; Q5(a), killing power).** The F5a-2 row was changed to `check_in(..., f"; {clause}", api["message"])` (test_gate_preflight.py:2882/2888). The old text, `"...; <clause>: it could not be read"`, also contains `"; <clause>"`. The count row (`message.count(clause) == 1`) is 1 on the old text too. So no row goes red on the defect F5a-2 fixed.
- Fix: assert `api["message"].endswith(f"; {clause}")` on that row. The message ends with the clause (gate_preflight.py:2950).

**A-4 (stream 1, low, does not block; F1-2).** The plural branch fixes the verbs but keeps the singular pronouns: "stands a, b name no address and do not say **it** runs in-process: **it** was taken as in-process" (readiness.py:889-893). Make these "they run" / "they were taken" when `len(by_default) > 1`.

**A-5 (stream 1, low, does not block; K6).** Two remaining test rows overlap other rows:
- test_readiness.py:874-880 (7 lines). "a broken table is refused, not defaulted" checks the internal `declared_surfaces` raise. The door row at 890-892 ("record: an unreadable table is `unknown`") reaches the same raise through the record. Cut it.
- 5a, test_gate_preflight.py, the `r8 M-a` loop (2 lines). It pins four words of the fix text. One of them ("end the turn without asking the person") is asserted again through the door by the rig row ("the conductor was told ..."). Cut the loop, or keep only the `poetry install` word.
- 7a, test_check_delivery.py, the `"the refusal is today's text"` check_in (2 lines). It pins unchanged text that `bool(said)` already decides. Optional cut.

**A-6 (7a, low, fix before merge; Q7).** `stage_closed_by_code` (s7_pretriage.py:326-329) calls `stage_status` and then `_stage_record`. That is two full `Controller.state()` projections (controller.py:2055: an event-store projection plus a directory scan) per call on a completed stage, and the two reads can disagree. A miss is still False, so the error direction holds. Fix: read the record once, as in `r = _stage_record(...); return r.get("status") == "completed" and r.get("code_only") is True`.

**Note (stream 1, not a fix).** `undeclared` now carries `hands: "role"`, while every surface entry is `agent|person` (the `declared_surfaces` docstring names those two). This follows the Lead decision ("stays as reviewed"). Its only reader of `hands`, `unsupported`, filters `== "person"`, so nothing misreads it. Node 1b should settle the vocabulary.

## K1 - the verdict's fixes, one line each

- **F1-1: fixed, option (i).** I checked `git diff origin/main...HEAD` (merge base 1323da2b). surfaces.py shows only the `UNDECLARED` constant, the docstring lines and the `if not named and not capabilities` return. surfaces.json shows only the `undeclared` word: `unknown_word`, `no_stand`, cli and desktop are byte-identical to main, and `_who` plus the three literals are back to `"person"`. Changelog bullet 2 is gone.
  - Consistency: the architecture.md axis 2 cell ("cases of any other surface go to a person") now agrees with the code. No role word is left. The record says `hands: role` only for `undeclared` (see the Note).
- **F1-4: not taken, as decided.** `unsupported` is byte-identical to main.
- **F1-2: fixed.** There is one `names_no_address` helper (readiness.py:883-884). The plural form is half done (A-4).
- **F1-3: fixed in 5a** (gate_preflight.py:826, the false clause removed).
- **F5a-1: fixed at 2941, but its neighbour at 2942 and the changelog are not** (A-2).
- **F5a-2: code fixed** (2960-2961; the r3 §2 r8 edge line is a spec file outside these trees and was not checked). The row does not kill the old text (A-3).
- **F5a-3: fixed.** The test and its `__main__` call are cut.
- **F5b-2: fixed** (see K4).
- **F7a-1: fixed wrongly.** The argument is right, but the module is unbound (A-1).
- **F7a-2: fixed.** test_check_delivery keeps one admit row and the broken-half row. test_story_run_s7 drops "no target" and "S6 not finished". The reader-does-not-write row of test_s7_pretriage is cut.
- **F5b-1, the s7_pretriage half: fixed as decided.**
  - `_stage_record`, `stage_status`, `stage_closed_by_code` are added; `s6_closed_by_code` is now a wrapper.
  - Rule 2 goes through `stage_status`, and there is no inline `Controller(...)` read left in s7_pretriage outside `_stage_record` (grep shown in the trail).
  - The `acceptance._s5_closed_by_code` half is still in 5b, as decided.
- **K3 cuts:**
  - stream 1: the text pins, the `row_for_profile` rows and the `unsupported` row are cut. The cli/desktop/zzz/native rows went with F1-1.
  - 5a: F5a-3 is cut, and the `tests-over:` line is amended.
  - 5b: the underived `stage_scope` row is cut.
  - 7a: the F7a-2 rows are cut.

## K2 - nothing beyond the verdict

Every hunk maps to a fix.
- stream 1: changelog, json and surfaces.py map to F1-1; readiness.py maps to F1-2; the test_readiness edits map to F1-1 and the K3 cuts.
- 5a: 826 maps to F1-3, 2940-2944 to F5a-1, 2960-2961 and the test row at 2882 to F5a-2, and the cut test to F5a-3.
- 5b: the doc row and the generator key map to F5b-2; the test cut maps to K3.
- 7a: driver_machine maps to F7a-1; s7_pretriage maps to F5b-1 (the `isinstance(record, dict)` and `isinstance(status, str)` guards are within the Lead's K3 "non-dict record" clause); the three test cuts map to F7a-2.

No unprescribed logic.

## K3 - the 7a logic, input by input (4b8dac2b vs 86dea617)

`s6_closed_by_code`:
- controller raises / unreadable: False / False.
- `stages` absent or S6 absent: False / False.
- `stages` not a dict: False (caught) / False.
- status not a string, or not `completed`: False / False.
- `code_only` not `True`: False / False.
- **S6 record not a dict (truthy, e.g. a string): the old code RAISED AttributeError**, because `stage.get` sat outside its try. The new code returns False. This is the only difference, and it moves toward False, as the dispatch's clause expects.

`triageable_not_executed`, rule 2: every case above was False on both sides. The old non-dict case fell into the function's own `except Exception -> False`, so there is no difference. The awaiting path is unchanged. Witness: the predicate table passes, 468/468.

The dry print: `awaiting` is computed exactly as `stage_S7:60` computes it (`controller_state()`, `"S6"`, `self.pipeline()`). `controller_state` and `pipeline` are `_read_json` reads, the same calls the live path makes. **But it raises NameError outside `except Refusal` (A-1).** K3 fails on this point only.

## K4 - the 5b generator key

- `git diff origin/main...HEAD` of controller-blocks.md: in the fix round, only the `_s5_code_only_problems` row (line 128) changed. The other changed lines are the 5b counts and the `validate` head, which t-1271 judged.
- The door names "rework S3 or record dispositions, then S5 runs again; or S5 runs its author and critic". Both doors appear in the refusal text (controller.py:4304-4310). It names nothing the refusal does not.
- The lookup takes the first match (`for key, door in COMMAND.items(): ... return`, gen:323-325), and the key sits before the general one.
- grep -ic "only over its own empty derived" over the document gives 1 (line 128). Positive control: "only over its own empty" gives 2 (lines 128 and 248, the `validate` head, which is cut before "derived" and keeps its role door, correctly for a role stage).
- Regenerating into scratch (`python -B tools/controller-blocks-gen.py <scratch>`, exit 0) gives a file identical to the committed one.

## K5 - the two spots the 5a builder left unread

- `changelog.d/universality-1-missing-launcher-one-road.md` carries the F5a-1 phrase ("the project names a command that installs ...", bullet 1): A-2. It does not carry "it could not be read". Bullet 3 says "adds one clause with the reason", which is true when a reason exists. Optional: "with its reason, when one is given".
- `references/conductor-actions.json:34` (`install_dependencies`) carries "the project's own install command". It is pre-existing on main and outside the owns: the A-2 analog line. It has no "could not be read" (grep -ic gives 0; positive control: "install" matches that line).

## K6 - test volume (`git diff --numstat origin/main...HEAD`, added lines)

| stream | test | code | `tests-over:` (quoted) | judged |
|---|---|---|---|---|
| 1 | 80 | 35 (incl. json/md/changelog) | "the readiness record rows (undeclared, unknown, legacy keys absent) and the in-process note rows each need a built config or stand; test setup, not code, is most of the lines" | holds; cut A-5 row (7) |
| 5a | 295 | 176 (171 .py) | "the test lines are the launcher rig (about 45 lines, reused by a later node) and the rows of the two roads built (executor, toolchain); road 3 is not built" | holds; cut the M-a loop (2) |
| 5b | 159 | 132 | "branch test lines still exceed code lines; the rows left are the five parameterised behaviours spec r11 names" | holds (t-1271 agreed); no row left to cut |
| 7a | 156 | 102 (97 .py) | "the predicate table is the only judge of the 7a predicate; each door keeps one admit and one refuse row" | holds (one admit and one refuse row in check_delivery confirmed); optional 2-line pin; missing dry-print row (A-1) |

Beyond A-5, no remaining row is a pin, a row of unchanged behaviour, a duplicate or an internal-boundary row.

## K7 - merge

- Current origin/main is 30a5ee2d. `git merge-tree --write-tree` exits 0 for each of 86dea617, 68d741eb, 3393e782 and 41b3ad41.
- I chained them in the order 7a -> 5a -> stream 1 -> 5b, with temporary commit-tree objects and no refs: every step exits 0. The total is 32 files, +1135/-63.
- The four trees touch disjoint files, so the order holds. Only the later F5b-1 acceptance node depends on 7a.

## For the canon

- test_story_run_s7.py (the cut rows; the A-1 row once added)
- test_check_delivery.py and test_gate_preflight.py (both on the slow list)
- test_readiness.py
- test_controller_state.py (the cut row)
- the forge-check ratchets

## Spot-checks

- No other `Controller(` read in s7_pretriage outside `_stage_record`: the grep of `get("stages")` over s7_pretriage, check_delivery and driver_stage_s7 shows s7_pretriage:314 as its only hit in s7_pretriage. The driver_stage_s7 hits read the driver's own controller.json and are pre-existing.
- `source` exists on the gate's command: executor_install returns `command.get("source")` (gate_preflight.py:606), and dependency_drift sets `profile` / `table` / `none` (124-130).

## Trail

- Read:
  - the t-1271 file, lines 1-201;
  - the four `diff <reviewed>..HEAD`;
  - `diff origin/main...HEAD` of surfaces.py, surfaces.json, the changelog, architecture.md, readiness.py, controller-blocks.md, check_delivery and driver_stage_s7, plus the added test lines of 5a and 7a;
  - test_readiness.py:838-917;
  - test_gate_preflight.py:2866-2905;
  - gate_preflight.py:591-607 and 2925-2962;
  - dependency_drift.py:105-135;
  - controller.py:2055-2067, 4300-4330 and 6125-6140;
  - controller-blocks-gen.py:300-340 and 465-495;
  - s7_pretriage.py:339-390, plus the old version at 322-350;
  - driver_machine.py:4155-4220;
  - driver_stage_s7.py:10-30 and 50-62;
  - story_run.py:160-180.
- Commands:
  - `python -B tests/test_s7_pretriage.py` (7a tree): `=== s7 pretriage: 468/468 ok ===`, exit 0.
  - `python -B tests/test_check_witness.py` (5b tree): `=== check witness: 53/53 ok ===`, exit 0.
  - The NameError probe (above): `NameError: name 'acceptance' is not defined`; control `detector_verdict`.
  - Regenerating controller-blocks: exit 0, `IDENTICAL`.
  - merge-tree: 4 x exit 0; the chain 4 x rc=0.

```json
{
  "verdict": "blocker",
  "blockers": [
    "A-1 (7a): driver_machine.py:4212 DriverMachine.describe uses `acceptance` which is unbound in that module (imported only locally at 2118/2258); story_run --dry-run at prepare_stage S7 raises NameError outside `except Refusal`. Fix: `import acceptance` before the call."
  ],
  "fixes": [
    "A-1 (7a, blocks): add `import acceptance` in describe's S7 branch; add one row driving describe() at S7 in the S7 story file (canon-run).",
    "A-2 (5a, before merge): gate_preflight.py:2942 statement and changelog bullet 1 still say 'the project names a command' for a table-sourced command; reword both. Analog outside owns: references/conductor-actions.json:34 install_dependencies 'says' -> a Lead-opened node.",
    "A-3 (5a, before merge): test_gate_preflight.py:2882/2888 F5a-2 row passes on the old tautology; assert api['message'].endswith('; ' + clause).",
    "A-4 (stream 1, low): readiness.py:889-893 plural form keeps 'it runs' / 'it was taken'.",
    "A-5 (low): cut test_readiness.py:874-880 (internal raise row duplicated by the record row 890-892); cut the 5a r8 M-a text-pin loop (2 lines).",
    "A-6 (7a, low): s7_pretriage.stage_closed_by_code reads Controller.state() twice; read the record once."
  ],
  "class_completeness": "F5a-1 left its neighbour in the same finding (statement, gate_preflight.py:2942) and the changelog unfixed; the pre-existing analog conductor-actions.json:34 is named for a Lead node. F5b-1 s7_pretriage half complete: no inline Controller stage read left in s7_pretriage; the acceptance half is the Lead's later node. F1-1 byte-for-byte return verified against origin/main.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1271-u7-code-streams-1-5a-5b-7a.md",
      "stream1: surfaces.py, surfaces.json, readiness.py, test_readiness.py, architecture.md, changelog (diffs vs f6fa3c74 and origin/main)",
      "5a: gate_preflight.py 591-607 2925-2962, test_gate_preflight.py 2866-2905, dependency_drift.py 105-135, changelog, conductor-actions.json:34",
      "5b: controller-blocks.md, tools/controller-blocks-gen.py 224-230 300-340 465-495, controller.py 4300-4330 6125-6140",
      "7a: s7_pretriage.py 306-390 (old and new), driver_machine.py 4155-4220, driver_stage_s7.py 10-62, story_run.py 160-180, check_delivery diff, test diffs"
    ],
    "reruns": [
      {"command": "python -B tests/test_s7_pretriage.py (7a tree)", "result": "468/468 ok, exit 0"},
      {"command": "python -B tests/test_check_witness.py (5b tree)", "result": "53/53 ok, exit 0"},
      {"command": "eval acceptance in DriverMachine.describe globals after import story_run", "result": "NameError: name 'acceptance' is not defined; control DV resolves"},
      {"command": "python -B tools/controller-blocks-gen.py <scratch> and diff with committed doc (5b tree)", "result": "exit 0, identical"},
      {"command": "git merge-tree --write-tree origin/main(30a5ee2d) <head> for 4 heads, and chained 7a->5a->1->5b", "result": "all exit 0"}
    ]
  }
}
```
