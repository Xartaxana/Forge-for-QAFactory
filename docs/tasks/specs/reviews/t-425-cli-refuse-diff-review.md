# t-425 critic diff gate: commit 606ca15 (wip/cli-refuse), refusal instead of traceback in two CLIs

Base 92fda1a, 5 files, +126/-20. Reviewer: critic (Opus). This verdict is an input to the Lead's acceptance. It does not accept the work.

**Verdict: NEEDS WORK (fit_with_fixes).** Both product changes are correct on every path I traced. One finding blocks the merge: the (A) tests sit in a quarantined file, so the canon never runs them. Five more fixes should go in before the merge. Three of them the builder cannot make inside the DoD as written, so the Lead has to amend the DoD first.

## Findings

**F1 (blocks the merge). The (A) rows were added to a quarantined file, and the commit has no `quarantine-edit:` line.**
- `scripts/tests/test-layers.json` lists `test_import_test_receipt.py` under `quarantine`. A Python check printed `quarantine test_import_test_receipt`; for comparison, `test_environment_preparation` printed under `keep`.
- docs/TESTING.md §«Карантин»: a quarantined file "в каноне не запускается, не чинится и не правится". Brief item 5: an edit to a quarantined file without a `quarantine-edit:` reason is a finding.
- Result: the CI canon never runs the 4 rows that protect (A). Only quarantine-watch runs them, twice a week.
- The cause is in the dispatch. Its DoD said "its own test file", and the builder followed it.

**F2 (fix before merge). Two of the four (A) needles can only pass.**
- `test_import_test_receipt.py` rows "request is a JSON list" and "receipt the importer refuses" use the needle `"import_test_receipt"`.
- That string is in every refusal prefix (`import_test_receipt.py: ...`). It is also in the old traceback's file path. So it was green even on the red-first run: 38/46 means 8 failures, which is exactly the exit and traceback checks of the 4 rows.
- The rows should name the actual problem. The tampered receipt reaches `receipt_sha256 does not match immutable receipt content` (`validate_receipt` checks the digest before the binding, lines 97-100; I read this, I did not run it). The list row's needle should be `AttributeError`.

**F3 (fix before merge; axis 16, standing question 6). The diff adds a new copy of the package's one JSON reader, under the same name.**
- The new nested `read_json` in `environment_preparation.main` duplicates `hooklib.read_json` (hooklib.py:873).
- SIBLING_MAP axis 16, closing rule: "a new JSON read of a package file calls `hooklib.read_json`".
- The copy also reads with `utf-8`, not `utf-8-sig`. A request file with a BOM is refused with "Unexpected UTF-8 BOM", which the shared reader accepts.
- `hooklib.read_json(path, None, kind=dict)` returns None for missing, broken, non-UTF-8 and non-object files alike. The refusal can then say what was expected: "absent, unreadable or not a JSON object". This also turns the JSON-list request (input of the wrong shape) into a refusal instead of an AttributeError traceback.
- The annotation `def stop_with(why) -> None` is wrong: the function never returns, so it should be `NoReturn` (question 7).

**F4 (fix this round, but the Lead must amend the DoD; P31 / question 12). One role-run CLI now gives two refusal shapes.**
- `main` still calls `story_cli(...)` with the default `exit=True`. A missing story is therefore a `{"error": ...}` JSON line. Every other refusal is now in the `run_guarded` shape.
- hooklib.py:570 states the contract: "With `exit=False` (a script that runs under `role_cli.run_guarded`) the `StoryRootError` is re-raised and the guard prints it in the shape of the registered command".
- The template the DoD named, manual_capture.py:5510, calls `story_of` directly under the guard. That is the same one-road shape.
- The fix is one token, `exit=False`. `StoryRootError` is a `ValueError` (hooklib.py:368), so `run_guarded` prints it with exit 2.
- The phantom-story row of test_story_root_class.py:889 still holds: non-zero exit, the key named, no traceback.
- This contradicts two DoD lines: "main's body unchanged" and "story_cli refusal (one JSON line) must keep working". The builder followed the DoD, so the fault is in the dispatch.

**F5 (fix before merge; rule 14, the encoding neighbour). A job record that is not UTF-8 still crashes `observe`.**
- `EnvironmentJobs.read` catches only `json.JSONDecodeError`.
- Probe: a job file with the bytes `\xff\xfe{}` gives `UnicodeDecodeError` and rc=1, a traceback.
- The JSON-broken twin of the same record gives `environment_preparation.py observe: corrupt environment job: Expecting property name ...` and rc=2.
- Fix: catch `ValueError` at environment_preparation.py:216. This adds no new raise site. In-process callers that catch `ValueError` behave the same as before.

**F6 (fix before merge; question 5 and TESTING.md «Бюджет»). Test size, and a row that locks in a traceback.**
- Once F1 moves the (A) rows, the budget is about 51 test lines against about 42 product lines. That is fine with the reason the builder gave.
- The environment_preparation row `plan --request [] -> "Traceback" in stderr` asserts that bad input still crashes. F3 turns that input into a refusal. The "a defect is not swallowed" property can be seen by reading the code: the only catch is `except PreparationError`. Keep the success half of that test and drop the traceback assertion, or drive a real defect some other way.

## Answers to the keys

**K1. (A) is correct on every path.**
- Success: `main` returns None, `sys.exit(None)` gives 0, and stdout is the same `json.dumps` (ASCII, so it does not depend on `utf8_stdio`).
- story_cli's `sys.exit(2)` is a SystemExit, which `run_guarded` re-raises.
- ImportError and JSONDecodeError are `ValueError` subclasses and go to `refuse` with exit 2. A missing file goes to the FileNotFoundError branch (probe output below).
- Shadowing: the module's `except ImportError` at lines 217 and 228 predate this diff and mean the module's own class, as intended. The `except ImportError` inside `run_guarded` and `role_cli.main` is resolved in role_cli's own globals, so it is the builtin. A failed `from role_cli import` would raise the builtin, which nothing catches; that is an install defect and a traceback is right for it.
- Running from another directory works. Python puts the script's directory first on `sys.path`, which is the same thing the top-level `from hooklib import` already relies on. Probe from the scratchpad: `import_test_receipt.py: nope.json: no such file...`, rc=2.

**K2. (B) is correct for plan, start, status, observe and reconcile.**
- Still escaping as a traceback:
  - TypeError/KeyError/AttributeError on a record of the wrong shape. Probe: job `[1]` gives `TypeError`, rc=1. That is a corrupt record and arguably a data refusal; it goes to the queue as Q4.
  - `OSError` from `EnvironmentJobs.__init__` mkdir. Probe: `--jobs` pointing at a file gives `FileExistsError`, rc=1.
  - UnicodeDecodeError, which is F5.
- `stop_with` raising SystemExit inside `try/except PreparationError` is fine, because SystemExit is not caught there.
- Braces: the driver only runs `observe` (driver_machine.py:1686). Every message `observe` can produce is either a constant ("unknown environment job") or CPython's JSONDecodeError text, and none of those contains a brace. So `observe` cannot be parsed as garbage today.
- The latent case: a `--request`/`--probe` path containing a valid JSON fragment, e.g. `C:/x/{}/r.json` missing. That prints `...cannot read \`C:/x/{}/r.json\`...`, and a brace-scanning caller would parse `{}`. In driver_machine.py:1692-1720 that would read as not settled and not uncertain, i.e. "waiting" for up to ENV_JOB_LOOKS rounds. No caller of plan/start/reconcile parses this way today (a grep of scripts finds no subprocess caller; the driver tells a person to run status/reconcile by hand).
- The caller's message is better than before. Old: `(exit 1) printed no readable JSON:\n<600 characters of traceback>`. New: `(exit 2) printed no readable JSON:\nenvironment_preparation.py observe: unknown environment job`. The framing "no readable JSON" stays and is now inaccurate (Q3).

**K3. The rename is honest in substance, but it is the odd one out.**
- What the census counts: u1 by name (`UNIT_NAME_RE` contains `_?refuse`) and u3 by `refusal_registry.sites` (`REFUSAL_RAISES = ("StateConflict","ValueError")` plus `deny`/`block`). `SystemExit` is not counted. Grep of refusal_registry.py for "systemexit", case-insensitive: 0 hits; positive control "StateConflict": hits at lines 37 and 60.
- `stop_with` formats existing refusals and judges nothing. The judging lives in the `PreparationError` raises, which are already invisible under the census's documented subclass blind spot. So the helper should not be a unit by meaning.
- It hides nothing from a ratchet. A `refuse` row would be class `shape`, which has no ceiling. Its unit does not block (no site in its span), so `blocking_per_role` would not move either.
- The package convention, though, is a helper named `refuse` with a `shape/data` row. Ten such rows exist: collect_pack, handoff_check, launch_check, probe_by_code, onboarding_notes (all `refuse`), and environment_record, adapter_forms, place_answers, question_register, report_adapt (all `_refuse`).
- The honest form costs nothing: the name `refuse` plus one row. Optional; I list it as a Lead decision, not a blocker.
- Blind spot for the queue: `raise SystemExit(2)` after a printed refusal is not seen by the census. 8 package files carry it. The census docstring's BLIND SPOTS does not mention it (Q1).

**K4. Both the misleading defect message and the missing card go to the queue; neither is a defect of this diff.**
- Defect message: the JSON-list request is the role's mistake, yet the guard calls it "a defect in import_test_receipt.py". That breaks FR-1 in the safe direction: the role records it and moves on, it does not loop.
- A shape guard in `main` would be a new raise (`ValueError` makes `main` a u3 unit and moves the census), which the DoD forbids. So this is a queue item (Q2). F3's `kind=dict` does not apply here, because main's read is unchanged by the DoD.
- Card: without one, the role gets the problem line and the halt tail. FR-2 is met (the halt door is usable). FR-1's "what expected / how to satisfy" is missing.
- Recommendation: queue the card. A card in role-commands.json makes test_role_commands.py (a keep/detector file) demand an accepted example with a signed receipt, which is not a one-line change. That node is also the right canon home for the (A) rows (F1).

**K5. Tests.**
- Every row the DoD named is present. The (B) ids name their cases.
- Red-first was shown for both files.
- Assertions that can only pass: the F2 needles.
- Subprocess per row: acceptable. The CLI's exit code and streams are what is being tested, and one temp world is built per test.
- Budget: see F6.

**K6. Confirmed: the failure exists on the base commit, and main is not red.**
- Byte copy of 92fda1a via `git archive` gives `FAIL bug_records.py: ['_story_exists'] call a driver and not artifacts_dir` and `687/688`.
- The file is in `quarantine`, so the canon does not judge it. No B-line is owed.
- One line for the Lead: quarantine-watch will report it red. bug_records.py was last touched on main by 7f10279 (OH8-2a, t-333); that commit is not verified as the cause.

**K7. Class-wide.** I grepped agents/*.md, role-commands.json, skills and the driver call sites. Positive control: manual_capture shows up in 2 agents and 3 cards.

| script | run by | `ValueError` reaches `main` | queue |
|---|---|---|---|
| bug_snapshot.py | the ROLE qa-failure-analyst ("on your card", agents/qa-failure-analyst.md:78, but no card exists) | yes, `validate` raises `ValueError`; json.loads is unguarded | yes: run_guarded + card |
| manifest_view.py | the role, via a card's `verify` line | no raise/json.loads hits | low |
| delivery_manifest, interim_packet, judge_plan, role_permissions | the conductor (skills phases) | various | low |
| render_case_appendix | driver_stage_plan.py (code) | 3 hits | code-run shape, see Q3 |
| benchmark_compare, case_lifecycle, charter, form_selftest, migrate_coverage, reconcile_mutations | no role or driver reference | n/a | none |

Standing questions:
- **6 DUPLICATION:** F3 (the `read_json` copy) and K3 (the `stop_with` name against the 10 `refuse` rows). Grepped `def refuse\b|def _refuse` and `def read_json` across the package.
- **7 CODE QUALITY:** `environment_preparation.main` is 66 lines (556-621), just over the limit, held up by its nested helpers. Fixing F3 shortens it. The `-> None` on `stop_with` is wrong (F3). Nothing else found.
- **8 HYGIENE:** the changelog fragment is English and the diff is ASCII.
- **9 RATCHETS:** no census row changed. Census re-run: 22/22.
- **10 ARCHITECTURE:**
  - AR-15 is kept for (A).
  - AR-9 is half kept for (B): the line says what is wrong but not what was expected, and gives no door. The driver's no-JSON branch adds no door either; that is Q3, since driver_machine is a non-goal.
  - AR-18: (B) adds a plain-text code-run refusal shape next to story_cli's `{"error"}` stderr line. They are two shapes because the driver's brace scan would read `{"error":..}` as a result. Named as Q3.
  - AR-16/axis 16: F3.
- **11 JUDGMENT:** `judgment: none` holds. No check was added and no class moved. The only judgment-adjacent point is the K3 rename, which is not a hidden unit.
- **12 ONE ROAD:** F4 (two shapes inside one role CLI) is a fix this round. Role-run via `run_guarded` against code-run plain text is a split by receiver: the guard's tail tells a ROLE to halt, which is wrong text for code. That is a branch serving the task's condition and is acceptable. The second code-run shape against story_cli's JSON line is a residual and is proposed as node Q3, which the Lead owns.

**Class completeness (SIBLING_MAP):**
- axis 15 (console): (B) prints to stderr, and Python's stderr uses backslashreplace, so a non-cp1251 character cannot crash. Localised OSError text arrives in the driver as mojibake; this predates the diff.
- axis 16: F3.
- axis 18: unchanged.
- axis 34: F4 and Q3.
- The other axes do not apply: no stage twins, no resolver, no host.

## Fix list (one fresh builder round, owns: environment_preparation.py, import_test_receipt.py, both test files, plus whatever the Lead decides on F1)
1. F1. Test files: move the 4 (A) rows to a canon (keep) file, or add a `quarantine-edit: <reason + follow-up node>` line to the commit message. Witness: `scenario_walk.py --witness-for scripts/import_test_receipt.py` lists where the rows run.
2. F2. `test_import_test_receipt.py` rows 3-4: needles `AttributeError` and `receipt_sha256 does not match`. Witness: the file's run.
3. F3. `environment_preparation.main`: replace the nested `read_json` with `hooklib.read_json(path, None, kind=dict)`; refusal text "absent, unreadable or not a JSON object"; type `stop_with` as `NoReturn`. Witness: test_environment_preparation plus test_read_json.
4. F4 (after the Lead amends the DoD). `import_test_receipt.main`: pass `exit=False` to `story_cli`. Witness: a phantom-story subprocess row (exit 2, `run_guarded` shape).
5. F5. `EnvironmentJobs.read`: `except ValueError` instead of `json.JSONDecodeError`. Witness: an observe row on a non-UTF-8 job file (exit 2, one line).
6. F6. Drop the traceback assertion on the `[]` request, which F3 turns into a refusal row.

## Lead decisions and queue items
- D1. Amend the DoD for F4, and choose F1's form: move the rows, or a `quarantine-edit:` line.
- D2 (optional). Name the helper `refuse` and add a census row `shape/data`, following the 10 existing rows.
- Q1. The census does not see `raise SystemExit(2)` after a printed refusal (8 files). Add it to the BLIND SPOTS docstring, or teach `refusal_registry` to see it. | node: forge/judgment, owner: Lead.
- Q2. A role-commands.json card for `import_test_receipt.py`, a request-shape refusal in `main`, and its accepted example in test_role_commands.py (the canon home for the (A) rows). | owner: Lead.
- Q3. One code-run refusal shape. driver_machine.py:1688 should read stdout only, or tell a refusal (exit 2) apart from "no readable JSON" and name the status/reconcile door. Then story_cli's `{"error"}` and this plain line can converge. | P31 node, owner: Lead.
- Q4. bug_snapshot.py: run under `run_guarded`, with a card (the role is told it is "on your card"). A corrupt job record of the wrong shape (`[1]`), and `--jobs` pointing at a file, in environment_preparation should be refusals.
- Q5. test_story_root_class `_story_exists` red on base: quarantine-watch will report it.

## Trail
Read:
- the diff and the commit message
- role_cli.py (whole)
- import_test_receipt.py lines 1-60, 280-326, and its raise/except lines
- environment_preparation.py lines 200-330, 405-430, 497-520, 556-621
- driver_machine.py lines 1660-1720
- driver_runner.py `py` (lines 211-235)
- hooklib.py `story_cli` (565-580), `read_json` (873-890), `StoryRootError` (368)
- test_judgment_census.py lines 1-60 and 202-270, 337-405
- judgment-census.json (rows and ratchet)
- refusal_registry.py (grep)
- test-layers.json (sections)
- docs/TESTING.md lines 55-125
- test_story_root_class.py lines 868-900
- test_role_commands.py lines 1-40
- critic-diff-brief.md
- SIBLING_MAP.md axis list and axis 16
- agents/qa-automator.md and agents/qa-failure-analyst.md (grep)

Re-runs (output verbatim):
- `python -B .../test_environment_preparation.py` gives `Ran 25 tests in 6.890s` / `OK`
- `python -B .../test_import_test_receipt.py` gives `=== test_import_test_receipt: 46/46 ok ===`
- `python -B .../test_judgment_census.py` gives `=== judgment_census: 22/22 ok ===`
- base byte copy, `python -B <scratchpad>/base92/.../test_story_root_class.py` gives `FAIL bug_records.py: ['_story_exists'] call a driver and not artifacts_dir (the tree is green) -- expected [], got ['_story_exists']` and `=== test_story_root_class: 687/688 ok ===`

Observe probes (scratchpad job files):
- k1 `{not json` gives `environment_preparation.py observe: corrupt environment job: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)`, rc=2
- k2 `\xff\xfe{}` gives `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0`, rc=1
- k3 `[1]` gives `TypeError: list indices must be integers or slices, not str`, rc=1
- `--jobs` pointing at a file gives `FileExistsError`
- status on k1 gives `environment_preparation.py status: corrupt environment job: ...`

Other runs:
- import_test_receipt from another directory gives `import_test_receipt.py: nope.json: no such file. A path is read as given, relative to the directory you run from` plus the halt tail, rc=2
- `scenario_walk.py --witness-for` both scripts: import_test_receipt is covered by three scenarios and `keep test_read_json.py` only
- `grep -n -i systemexit refusal_registry.py`: 0 hits; control `StateConflict`: lines 37 and 60

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1: the (A) refusal rows were added to test_import_test_receipt.py, which test-layers.json lists under quarantine; the commit has no quarantine-edit line, so the canon never runs them (TESTING.md quarantine section; brief item 5)"
  ],
  "fixes": [
    "F1 test files: move the 4 import_test_receipt rows to a keep file, or add a quarantine-edit reason naming the follow-up node (Lead picks)",
    "F2 test_import_test_receipt.py rows 3-4: replace the can-only-pass needle import_test_receipt with AttributeError and receipt_sha256 does not match",
    "F3 environment_preparation.main: replace the nested read_json copy with hooklib.read_json(path, None, kind=dict) (axis 16 closing rule; BOM and JSON-list become refusals); type stop_with as NoReturn",
    "F4 import_test_receipt.main: story_cli(..., exit=False) so a missing story uses the run_guarded shape, per the hooklib.py:570 contract (Lead amends the DoD first)",
    "F5 EnvironmentJobs.read: except ValueError instead of JSONDecodeError (a non-UTF-8 job record still tracebacks on observe, rc=1, by probe)",
    "F6 test_environment_preparation: drop the Traceback assertion on the [] request once F3 turns it into a refusal; keep the success half"
  ],
  "class_completeness": "Axis 16: the diff adds a new read_json copy (F3). Axis 34 / P31: two refusal shapes inside one role CLI (F4, fix this round); the second code-run shape next to story_cli's error JSON line is proposed node Q3. Axis 18: census unchanged, re-run 22/22. Axis 15: stderr is backslashreplace, no crash. Rule 14 neighbour on the same surface: the job-record encoding (F5). Role-run analog bug_snapshot.py is queued (Q4). The census blind spot for SystemExit after a printed refusal is queued (Q1).",
  "trail": {
    "read": [
      "git diff 92fda1a 606ca15 and commit message",
      "ai-packages/qa-factory/scripts/role_cli.py",
      "ai-packages/qa-factory/scripts/import_test_receipt.py",
      "ai-packages/qa-factory/scripts/environment_preparation.py 200-330, 405-430, 497-621",
      "ai-packages/qa-factory/scripts/driver_machine.py 1660-1720",
      "ai-packages/qa-factory/scripts/driver_runner.py 211-235",
      "ai-packages/qa-factory/scripts/hooklib.py 368, 565-580, 873-890",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json",
      "ai-packages/qa-factory/scripts/refusal_registry.py (grep)",
      "ai-packages/qa-factory/scripts/tests/test-layers.json",
      "docs/TESTING.md 55-125",
      "ai-packages/qa-factory/scripts/tests/test_story_root_class.py 868-900",
      "ai-packages/qa-factory/scripts/tests/test_role_commands.py 1-40",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md axis 16 and axis list"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_environment_preparation.py", "result": "Ran 25 tests in 6.890s OK"},
      {"command": "python -B scripts/tests/test_import_test_receipt.py", "result": "46/46 ok"},
      {"command": "python -B scripts/tests/test_judgment_census.py", "result": "22/22 ok"},
      {"command": "python -B <git archive 92fda1a>/scripts/tests/test_story_root_class.py", "result": "687/688, FAIL bug_records.py _story_exists; file is in quarantine"},
      {"command": "environment_preparation.py observe on non-UTF-8 / [1] / broken job records", "result": "rc=1 UnicodeDecodeError, rc=1 TypeError, rc=2 one plain line"},
      {"command": "import_test_receipt.py from another cwd with a missing request", "result": "rc=2 no such file refusal plus halt tail"}
    ]
  }
}
```
