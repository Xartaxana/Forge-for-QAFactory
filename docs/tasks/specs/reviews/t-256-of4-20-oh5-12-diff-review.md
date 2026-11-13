# t-256 — critic diff review: OF4-20 + OH5-12 (wip/of4-20-oh5-12, fc9c3c9 + af512e6)

**Verdict: NEEDS WORK (fit_with_fixes): 0 blockers, 4 required fixes (F1-F4) for this node's fix round, 3 minor (F5-F7).**
This verdict is input to acceptance. Accepting it, and widening `owns` to `hooklib.py` for F2, are decisions for the Lead.

Spec used: the dispatch's inline DoD. The OF4-20 node row could not be read. `plans/piles/onboarding-forge/batch-4-*.md` is not on
`refs/remotes/origin/main` or in the main working tree (only batch-1/2/3/5 exist). OH5-12 was read at
`onboarding-hooks/batch-5-nerazlozhennye-nakhodki.md:41`, together with its finding B-298.

## Findings

**F1 (required; FR-1, FR-2, AR-9, a regression this diff introduces): `execution_scheduler.py --recover-leases` now ends in a traceback on a bad config.**
`LeaseRegistry.recover` (:155-156) now calls `hooklib.artifact_root`. `main` (:689-697) catches only `OSError, json.JSONDecodeError,
RequestError, SchedulerError`. Before this diff, `--recover-leases` never read the config. Probe output (worktree code, one blocked lease with a task and key):
- `{"artifact_root": ""}` → exit 1, `ValueError: artifact_root must be a non-empty path` (traceback)
- `[1]` → exit 1, `AttributeError: 'list' object has no attribute 'get'` (traceback)
- `{broken` → exit 2, `{"status": "invalid_schedule", "error": "Expecting property name ..."}`. The status is wrong (this is not a schedule), and the message names neither config.json nor a door.

The other caller, `execute_schedule`, already resolves `artifact_root` at :572 before it launches anything. Its in-loop `recover()` (:662) is therefore
reached only if the config changes during the run, which is acceptable.
Fix: in `main`, wrap the `--recover-leases` branch in its own `except ValueError as exc`. It prints
`{"status": "config_unreadable", "error": "qa-factory/config.json: <exc>", "door": "fix the file by hand or move it aside and run onboarding again"}` and
exits 2. Reuse the door sentence of `config_contract.read_config_file` (:1356). Add one row to `artifact_path_rows`: a subprocess run of
`--recover-leases` on `{"artifact_root": ""}` and on `[1]`, each expecting exit 2 and the status above. After F2, the list case also reaches this handler as a ValueError.

**F2 (required; spec edge "list config → reader's refusal", AR-28 and AR-9): the reader the node relies on does not refuse a non-object config. It crashes.**
`hooklib.artifact_root` (:653-654) does `cfg = json.loads(...)` and then `cfg.get(...)`. With a config of `[1]` or `null` this raises `AttributeError` (probe), not
the ValueError that every new call site, and the `except ValueError` in `source_exclusions.main` :629, expect. The node's docstrings
(`task_dir_hint`, `recover`) and its test rows claim "a broken config raises the reader's ValueError". That holds only for unparseable text.
Fix (two lines): right after the `json.loads` at `hooklib.py:653`, add
`if not isinstance(cfg, dict): raise ValueError("qa-factory/config.json is not a JSON object; fix it by hand or move it aside and run onboarding again")`.
Add a `("list", b"[1]", None)` and a `("null", b"null", None)` case to `artifact_path_rows`' `cases` tuple, so the raise rows cover them. `hooklib.py` is outside
OH5-12's owns and is a hot file. If the Lead keeps owns as they are, this goes to a node with an id instead. F1's handler should then catch `(ValueError, AttributeError)` for now.

**F3 (required; FR-37, a regression this diff introduces): `_door` builds commands that break when the artifact root has a space.**
`source_exclusions.py:558/560/581` (and the `inspect --output {inventory}` step after them) put `{folder}` into a backticked command without quotes. Before this diff the
folder was a literal with no space. Now it can be any configured root, including an absolute one outside the project (a Windows profile path).
Probe with `{"artifact_root": "my stories"}`:
`` `python ".../ticket_adapter.py" peek QA-9 --output my stories/S-1/work/source-inventory.json --summary` ``. That is two arguments, so the conductor's command fails.
The test pins this defect: the "outside the project" case uses `far away` (with a space), and `test_config_projection.py:409` asserts the
unquoted `--output <folder>/work/`.
Fix: quote every path built from the folder, the same way `--url \"{fetch}\"` is quoted on the same line. That covers `--output \"{inventory}\"` in every step and
`--output \"{folder}/work/{rel}\"`. Change :409 to expect `--output "%s/work/`. `snapshot_hint` returns a bare path and is not a command, so it stays unquoted.

**F4 (required; sweep the same branch first, AR-13): `app_card._test_data` hides `unknown` values but still prints blank and `None` values.**
The builder switched to `test_data_states` but uses only one of its non-value statuses. Probe:
`_test_data(None, "x", {"test_data": {"seeds": "", "accounts": None, "x": "unknown"}}, "")` gives
`['- config test_data.seeds: ', '- config test_data.accounts: ', '- config test_data.x: not set (recorded as unknown)']`. The first two print an empty
"value". The reader returns `not_recorded` for both, and the card ignores it.
Fix at `app_card.py:261`: add `elif status == "not_recorded": lines.append(f"- config test_data.{key}: not set")`, next to the `unknown` branch. Add
`"blank": ""` and `"nil": None` to the config in `test_test_data_goes_through_the_reader`, and assert `test_data.blank: not set`.

**F5 (minor): `_project_parallel_defaults`' new docstring overstates what it does.** It says "a block of the wrong shape: the fixed defaults". Probe:
`{"execution": []}` returns `{}`, and `{"execution": {"parallel": [["mode","off"]]}}` returns `{'mode': 'off'}`, because a list of pairs is accepted as a block. The caller
(:274-283) falls back per key through `.get`, so `{}` is harmless. The list of pairs is behaviour this diff did not change.
Fix: either make the function return the fixed defaults when `execution` or `parallel` is not a dict (one `isinstance` check), or reword the docstring.

**F6 (minor): `ticket_adapter.py:1873-1874` self-check now depends on the cwd's project.** `snapshot_hint("QA-1")` with no root resolves `project_root()`. In a
project that has its own `artifact_root`, the assertion `== "qa-factory/artifacts/QA-1/..."` goes red. Fix: drop this check (the
`artifact_path_rows` table covers the function), or pass an explicit temp project.

**F7 (minor, code quality and test hygiene):**
- (a) `test_config_projection.py:436` uses `"mode": "off"` as the project's own value. `prepare_schedule` refuses this value (:276, `mode must be auto or serial`). Use `"serial"`.
- (b) `artifact_path_rows` copies the try/except "got = ..." block twice, and the `acquire({...})` dict twice. Fold each into a local helper.
- (c) The `scheduler_config_rows` folder name `abs(hash(name))` changes between processes under hash randomisation. Use the loop index.
- (d) `ticket_adapter.snapshot_hint` reaches the artifact root through `source_exclusions.task_dir_hint`. A generic story-folder display helper now lives in a module about
  source exclusions, and the brief_pack sibling (below) will need it too. Move it next to `hooklib.artifact_root` when that sibling node runs. Queue this, not a fix now.
- (e) The commit names AR-16 for the app card. That is a misattribution: the card is not a person-facing question. The invariant that applies is AR-13 (already named). AR-9 is touched (F1) and not named. Name it in the fix-round commit.

## Red-first check (the dispatch's question)

The rows the builder did not observe red do fail against the old code. I re-ran `git show origin/main:.../execution_scheduler.py` from scratch, with the worktree modules on the path:
`old BOM parallel: {'mode': 'auto', 'min_selected_instances': 8, 'max_workers': None}` (the row expects `own`, so it is red), and
`old recover configured: ['blocked_orphan']` (the row expects `recovered_child`, so it is red). No row in the diff can only pass. The `default` lease case
passes on both old and new code by design: it is the byte-equal control.

## Answers to the dispatch's questions

1. **Correctness and edges.**
   - BOM is fine at all sites: scheduler through `read_config_file`; artifact_root uses `utf-8-sig`, and the probe gives `st/S-1`.
   - `{}` and an absent config are fine (defaults, byte-equal `qa-factory/artifacts/S-1`).
   - Unknown test_data values are fine.
   - Unparseable text: ValueError at the path sites (fine); declared defaults at the scheduler (fine, FR-59 safe default).
   - A list or null config at the path sites: AttributeError, **F2**.
   - A root outside the project gives an absolute posix path, including the relative `../x` form (probe), which is fine. Spaces: **F3**.
   - Windows slashes: `Path` normalises them and `as_posix` prints forward slashes. Fine.
2. **Every caller's path to the person.**
   - `source_exclusions --revoke`: `_task_root` → `story_root` → `artifact_root` raises first and is caught at :629, so `_door` adds no new exposure for a ValueError.
     The list config is still a pre-existing traceback (fixed by F2).
   - `ticket_adapter.snapshot_hint` has no caller ("Nothing calls this today").
   - `execute_schedule` fails at :572 first.
   - `--recover-leases` is a new traceback, **F1**.
3. **One road in the touched files.** No direct config read remains in the four touched source files. Grep `config.json|qa-factory/artifacts` over them:
   only usage and help strings (`app_card.py:584`, `ticket_adapter.py:1480,2440,2614`) and the self-check :1874 (F6). `app_card._read_config` (:112-118)
   still reads the whole file through `hooklib.read_json` (axis 16's one JSON reader, BOM-tolerant), not through `read_config_file`. That is the
   project-config reader class queued on axis 16 ("the project-config reader class"), not a regression of this node. Item 12 (language, project or case exclusions):
   none found. The diff has no language, runner or project branch (grep of the diff for language and runner names).
4. **Duplication and consistency:** see F7(b) and F7(d). `task_dir_hint` does not duplicate `runtime_paths.rel_text` (:182), which handles record names, or
   `hooklib.story_root`, which requires the folder to exist and so cannot serve a hint for a folder that may not exist yet. I ran a grep of the same shape for
   `relative_to(...).as_posix()` over hooklib, runtime_paths and story_run. **Code quality:** no new function exceeds 60 lines or 3 nesting levels. See F7(a)-(c).
5. **Class completeness:** see the next section.
6. **AR-n.** AR-13 and AR-4 are kept at the four sites. AR-28 is kept for unparseable text but not for list or null (F2). AR-9 is broken on `--recover-leases` (F1).
   AR-16 is a misattribution (F7(e)). Judgment: none moved. This is correct: the diff only reads paths and data, and it adds no census row.
   Ratchets (item 9): the diff touches no ratchet file (stat: 8 files, none of them a baseline).

## Sibling verdicts (class: "story folder built from a literal, not the reader": axis 8; config reader: axis 16)

| Sibling | Verdict |
|---|---|
| `execution_scheduler --recover-leases` without a ValueError catch | fix in this round (F1) |
| `source_exclusions._door` unquoted paths | fix in this round (F3) |
| `app_card._test_data` printing `not_recorded` | fix in this round (F4) |
| `hooklib.artifact_root` on a list or null config | fix in this round if the Lead widens owns, else a node with an id (F2) |
| `brief_pack.py` literals | separate node. The builder's list of 8 understates it: grep `qa-factory/artifacts` shows about 25 sites (:1135, 1248, 1443, 1494, 1607, 1758, 1783, 1852, 3206, 3332, 3674, 3733, 3747, 3851, 3981, 4068, 4235, 4261, 4333, 4379-4380, plus docstrings :11, :194). The sites are text that roles read, so FR-37 applies. A finding is needed, with the helper move F7(d) |
| help and usage strings `ticket_adapter :1480, :2440, :2614`, `app_card :584` | not applicable as a fix: they are examples in `--help`. They should go to the brief_pack node's finding as a low-priority line (FR-37 wording "the default `qa-factory/artifacts`") |
| `dispatch_liveness.py:790, :927`, `env_probe.py:695` | already queued (B-370 → onboarding-forge/1 OH1-6; B-298 lists env_probe and dispatch_liveness). B-298 is wider than OH5-12, so when OH5-12 closes, the B-298 remainder (env_probe, dispatch_liveness, `hooklib.artifacts_dir`) must be named in «Остатки» with a node. Otherwise it is lost |

## Trail

Read:
- the full diff `git diff refs/remotes/origin/main...HEAD` (8 files, 139+/14-) and the commit bodies (`architecture:` and `judgment:` lines)
- `hooklib.py` :54-70, :310-384, :647-661
- `config_contract.py` :893-927, :1321, :1349-1374
- `execution_scheduler.py` :84-160, :226-237, :270-290, :640-700
- `source_exclusions.py` :530-700
- `app_card.py` :108-118, :235-271
- `ticket_adapter.py` :146-180, :753-761
- `docs/SIBLING_MAP.md` axes 8 and 16; `docs/tasks/critic-diff-brief.md`; `tools/critic_verdict.schema.json`
- the OH5-12 row (batch-5 :41) and the B-298 finding

Reruns:
- `python -B -m pytest scripts/tests/test_app_card.py -q` → `22 passed in 6.92s`
- `python -B scripts/tests/test_source_exclusions.py` → `=== test_source_exclusions: 434/434 ok ===`
- probe script `scratchpad/probe/p.py` (outputs quoted in F1-F5)
- old-code red check `scratchpad/probe/q.py` (outputs quoted above)

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 execution_scheduler.py main :689-697: catch ValueError on --recover-leases, print status config_unreadable naming qa-factory/config.json and the read_config_file door, exit 2; add a subprocess row for empty-string and list configs",
    "F2 hooklib.py :653: refuse a non-object config with ValueError (list/null now AttributeError); add list and null cases to artifact_path_rows; Lead decides owns widening, else a node with an id",
    "F3 source_exclusions.py :558/:560/:581 and the inspect step: quote every --output path built from the artifact folder; update test_config_projection.py :409 expectation",
    "F4 app_card.py :261: print not_recorded keys (blank/None) as not set; extend test_test_data_goes_through_the_reader",
    "F5 execution_scheduler._project_parallel_defaults: make wrong-shape execution/parallel return the fixed defaults or correct the docstring (minor)",
    "F6 ticket_adapter.py :1873-1874: drop or root-pin the cwd-dependent snapshot_hint self-check (minor)",
    "F7 test hygiene: mode serial not off at :436; fold the duplicated raise and acquire blocks; deterministic folder names; name AR-9 and drop AR-16 in the fix commit (minor)"
  ],
  "class_completeness": "Axis 8 literal sites: the four named sites converted; _door quoting, recover-leases refusal, app_card not_recorded and artifact_root non-object config are fix-this-round siblings; brief_pack has about 25 literal sites (builder listed 8) and needs a finding plus the task_dir_hint move to hooklib; help strings join that finding; dispatch_liveness and env_probe are queued under B-370/OH1-6 and B-298, and the B-298 remainder must be carried in the OH5-12 Ostatki at close. Axis 16: app_card._read_config uses hooklib.read_json, within the queued project-config reader class.",
  "trail": {
    "read": [
      "git diff refs/remotes/origin/main...HEAD on wip/of4-20-oh5-12 and commit bodies",
      "ai-packages/qa-factory/scripts/hooklib.py 54-70, 310-384, 647-661",
      "ai-packages/qa-factory/scripts/config_contract.py 893-927, 1321, 1349-1374",
      "ai-packages/qa-factory/scripts/execution_scheduler.py 84-160, 226-237, 270-290, 640-700",
      "ai-packages/qa-factory/scripts/source_exclusions.py 530-700",
      "ai-packages/qa-factory/scripts/app_card.py 108-118, 235-271",
      "ai-packages/qa-factory/scripts/ticket_adapter.py 146-180, 753-761",
      "docs/SIBLING_MAP.md axes 8 and 16",
      "docs/tasks/critic-diff-brief.md",
      "plans/piles/onboarding-hooks/batch-5-nerazlozhennye-nakhodki.md row OH5-12 and findings/B-298"
    ],
    "reruns": [
      {"command": "python -B -m pytest scripts/tests/test_app_card.py -q", "result": "22 passed in 6.92s"},
      {"command": "python -B scripts/tests/test_source_exclusions.py", "result": "=== test_source_exclusions: 434/434 ok ==="},
      {"command": "probe p.py: recover-leases on empty-string / list / broken config", "result": "exit 1 ValueError traceback / exit 1 AttributeError traceback / exit 2 invalid_schedule"},
      {"command": "probe p.py: _door with artifact_root my stories", "result": "--output my stories/S-1/work/source-inventory.json unquoted"},
      {"command": "probe q.py: old origin/main scheduler on BOM config and configured-root lease", "result": "defaults (row red) and blocked_orphan (row red)"}
    ]
  }
}
```
