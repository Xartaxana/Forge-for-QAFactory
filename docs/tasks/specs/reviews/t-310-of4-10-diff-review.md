# t-310: diff gate for OF4-10 (commit 36083da on wip/of4-10, builder t-308)

Reviewer: critic (Opus). Spec: `docs/tasks/specs/t-289-of4-10-artifact-root.md`, where §12 and §13 override §9 and F-1 is decided (b). Diff: `git -C <wt> diff origin/main...36083da`, 7 files, +264/-77. Worktree HEAD = 36083da5, tree clean.

**Verdict: fit_with_fixes.** No blocking findings. Two fixes are cheap and should land in this round. F1 is a refusal text that says something false. F2 is a test check that cannot fail.

## Findings

### F1 (fix before merge, not blocking): the NUL refusal says "a blank string"

`hooklib.artifact_root` (commit :735-739):

```python
if not isinstance(value, str) or not value.strip() or "\x00" in value:
    shown = type(value).__name__ if not isinstance(value, str) else "a blank string"
```

Probe at 36083da: `{"artifact_root": "a\u0000b"}` gives `ValueError: qa-factory/config.json: `artifact_root` must be a non-empty folder path (got a blank string). ...`. The value is not blank. The text misstates the cause, which breaks FR-1 / AR-9 ("says what is wrong"). A person told "blank" goes looking for an empty value and finds `"a\u0000b"`.

The spec's form `(got <type name or 'a blank string'>)` did not foresee the E8 branch. The builder added E8 correctly but reused the blank label for it.

- Surface: the key-value refusal texts of `artifact_root`.
- Neighbours walked:
  - non-string types: probe gives `bool` for `true`, `dict` for `{}`, `int` for `5`, all correct;
  - blank: `""` and `" \t"` give "a blank string", correct;
  - NUL gives the wrong text (this finding);
  - unresolvable: the second raise says "got an unresolvable path", correct.

Fix: give NUL its own label, for example `"a blank string" if not value.strip() else "a path with a NUL character"`. In T1, assert that the `key_nul` text does not contain `blank`. Today `_root_locator` checks only that `config.json` is in the text, which is why the row passes. Both literal `raise ValueError` sites stay inside `artifact_root` (P1c).

### F2 (fix before merge, not blocking): the "every site has a cell per state" check cannot fail

`test_read_json.py` `test_the_artifact_root`:

```python
check_eq("OF4-10 every site has a cell per state", [len(ROOT_EXPECT)] * len(ROOT_SITES), [len(ROOT_STATES)] * len(ROOT_SITES))
```

This compares only the two dict lengths, three times over. A renamed state passes it: ROOT_EXPECT and ROOT_STATES keep the same size but hold different keys. Today that case dies earlier with a bare `KeyError` at `ROOT_EXPECT[state]`, outside `_crash`, which aborts the run instead of naming a row. The check's name promises something its body does not test (brief item 7: a name that lies).

Fix: `check_eq("OF4-10 every site has a cell per state", sorted(ROOT_EXPECT), sorted(ROOT_STATES))`, placed before the loop.

### Observations (no action this node)

- O1. The two literal texts in `artifact_root` (:737-739 and :743-745) are near copies. P1c and the census unit (B1) require literal `raise ValueError(...)` at both sites. `refusal_registry.sites()` lists both (lines 738, 745). The copy is the price of the census rule, so it is accepted.
- O2. `_story_at` catches `AttributeError`, as the code it replaced did. This is inherited, not new.
- O3. A matched exclusion with an empty `id` would now print `status: unknown` instead of `excluded`. Exit 2 and `fetched: false` are unchanged, so this errs on the safe side. This is what P4 prescribes.
- O4. `read_config_file`'s `path.exists()` can still raise a raw `PermissionError` on an unreadable parent folder on Python versions before 3.14. The original code had the same call. Every edited site catches `OSError` or `Exception`, so no new pass is reachable. Its other callers are in the OF4-10r census (OF5-12).

## Key 1: §4 edge rows and §5 positional invariants

| row | verdict | evidence |
|---|---|---|
| E1 absent | kept | T1 `absent` (locator `qa-factory/artifacts`, writer `ok`, grounding `[]`). `left_out_by_person`: `FileNotFoundError`/`NotADirectoryError` give None (read at commit :651-652) |
| E2 unparsable / non-UTF-8 / deep | kept | T1 `invalid`, `latin1`, `deep` give refused / refused / unreadable. `RecursionError` is caught in the moved reader (hooklib :715-717) |
| E3 not an object | kept | T1 `list`. Text from the moved `read_config_file` (kind map) |
| E4 empty | kept | T1 `empty_file`, `blank_file`. T2 V8 (0 bytes, probe-only) gives exit 2 |
| E5 folder / no rights | kept | T1 `dir` gives refused. The `OSError` becomes `ConfigUnreadable`, which `left_out_by_person` catches as `ValueError` and turns into a refusal. The F-5 (b) silent pass is closed |
| E6 wrong key type | kept | T1 `key_number`, `key_list`. Class split: `type(exc) is ValueError`. My probe: `true` gives `bool`, `{}` gives `dict` |
| E7 empty key | kept | T1 `key_empty`, `key_blank`. T2 V6 |
| E8 NUL | kept, with a wrong text (F1) | T1 `key_nul` gives refused. The explicit `"\x00" in value` check is present. The text says "blank" |
| E9 null key | kept | T1 `null_key` gives the default |
| E10 outside | kept | T1 `outside` gives `outside:outside` |
| E11 file in artifacts/ | kept | T2 V1, exit 2. Branch (2) starts at `len(parts)-3`, so `artifacts/x.json` never matches |
| E12 folder without pipeline.json | kept | T2 V2 and the existing row "a story folder without pipeline.json" |
| E13 real story of the old default | kept | T2 V3, exit 0 |
| E14 output equal to the story folder | kept, by reading | `artifacts` at index len-2 is outside `range(len-3, 0, -1)`, which gives None. Branch (1) needs `len(relative.parts) >= 2`. There is no test row, and the spec asks for none |
| E15 broken config, story known by (2) | kept | existing rows "broken config (bad JSON)" and "(a JSON list)", exit 0 |
| E16 broken config, no story | kept | T2 V4-V8: exit 2, needle present, stdout `status: unknown`, `calls == []`, no `qa-factory/artifacts/` in stderr. The door uses the placeholder `<artifact root>/<story>/work/` (B2) |
| E17 root cannot be listed | kept, by reading | any `OSError` other than "no folder" refuses with the resolved `root_dir` (commit :653-655). Pinned by reading, as the spec allows |
| E18 S1 stop, broken config | kept, by reading plus probe | `_identity` and `awaiting_source_review` are guarded. Probe below: `_identity` returns a key for both `task=""` and `task="S-1"` with no raise. `all_errors` raises are caught by `main` (F-7) |
| E19 another role | kept | probe: `grounding_errors("qa-scout", "")` gives `[]`. The role check runs before the guard |
| E20 temporal | n/a | the change creates no file, flag or config |
| E21 limits | kept | the `deep` row is the BEYOND row |
| E22 exploration slug | kept, by reading | `scan_root = exploration.root(slug, ...)` is decided first. `artifact_root()` runs only in the `else` branch, inside the try |
| E23 re-export identity | kept | T1 pins `config_contract.ConfigUnreadable is hooklib.ConfigUnreadable` and the same for `read_config_file`. My import probe prints `True`, and `issubclass(ConfigUnreadable, ValueError)` is `True` |

| invariant | verdict | evidence |
|---|---|---|
| P1 config read first; default only for absent file or absent/null key | kept | `cfg = read_config_file(project) or {}` comes first. `None` means no file only. Every read failure raises `ConfigUnreadable`. The default branch is `value is None` |
| P1b placement; no module-level config_contract import in hooklib; re-export after imports | kept | the class is at hooklib :691 and the function at :696, directly above `artifact_root`, far from OH6-1's :269-320. config_contract :32 is the re-export, after `from typing import Any`. Probe: `import hooklib` alone leaves `config_contract` out of `sys.modules` |
| P1c literal `raise ValueError` inside `artifact_root` | kept | `refusal_registry.sites(files=['hooklib.py'])` gives `artifact_root` at lines 738 and 745 |
| P2 order (1), (2), None through `_story_at` | kept | both branches return only what `_story_at` returned |
| P3 import guard first; config guard only on the no-story branch | kept | commit :633-656 |
| P4 `excluded` only for a non-empty id | kept | `main` :689-694 |
| P5 guard after the role check, before `_ticket_for_stage` and `register.is_file()` | kept | exit_gate :1561-1568 |
| P6 slug decides first; `task`/`dispatch`/`attempt`/`hook`/`agent` unchanged | kept | only the `file_state` block moved, into the existing try |
| P7 `True` only after the inventory was read | kept | ticket resolution moved inside the `try ... except Exception: return False` |

## Key 2: FR-59 / AR-28

- `left_out_by_person`, the OSError split:
  - `artifact_root()` failures (`ConfigUnreadable`, the literal `ValueError`, an `OSError` from `project_root`) all go to a refusal with exit 2;
  - in the listing, only `FileNotFoundError` and `NotADirectoryError` give None, and every other `OSError` refuses;
  - None is reachable only from "no folder", from the inherited import guard (analog (a), queued), or from "nothing matched".
  Kept.
- `_identity`, slug first: yes. On a broken config `file_state = []`, so the fingerprint carries no artifact state. That is the spec's stated error direction (§2.6). The fuse holds only `blocked`/`incomplete`, and the gate status is `unreadable` then. No unknown becomes a pass. Kept.
- `grounding_errors`: one `unreadable` record, never `[]`, on an unknown root. `[]` is reachable only after the root was read. T1 grounding column. Kept.

## Key 3: census untouched (B1)

- `git diff --stat origin/main...36083da -- '*judgment-census.json' '*test-layers.json' '*refusal*'` gives an empty diff.
- Census row `hooklib.py / artifact_root / shape / data` is present and unchanged. Neither `read_config_file` nor `ConfigUnreadable` has a census row (case-insensitive grep, 0 hits). The moved raises are `raise ConfigUnreadable`, not literal `ValueError`, so no new unit appears.
- `test_judgment_census.py` gives 22/22 ok. `refusal_registry.py --check` gives `A24 refusal registry: no violations`, rc=0.

Kept.

## Key 4: import cycle

| order | result |
|---|---|
| `config_contract` first | ok, identity `True` |
| `hooklib` first | ok |
| `import hooklib` alone | does not pull `config_contract` (the lazy import holds) |
| `exit_gate` and `vcs_evidence` | import fine |

No `spec_from_file_location` load of `config_contract` exists. Control: 11 such loads of other modules. No `scripts.hooklib` package-path import exists, which would split the identity. Control: 2 `import hooklib` hits in vcs_evidence.py.

Kept.

## Key 5: the builder's deviations

- T2 checks only rows with a needle: this is literally the spec's T2 wording ("For exit 2 with a needle"). V1 and V2 exit 2 through a recorded word, with id S-2's, so `excluded` is right and is not what B2 targets. Accepted.
- V6 trailing slash: the key text "Remove the key to keep the story folders in qa-factory/artifacts" is the spec's verbatim §2.1 item 3. It is true: removing the key yields exactly that folder. So it is a resolved default, not the B2 class. The check against `qa-factory/artifacts/` still catches the B2 class `qa-factory/artifacts/<story>`. Accepted.
  - The forward-slash needle does not see a Windows-resolved path. That matters only for E17's `root_dir` text, which no row drives.
- The `root_dir` text naming the default folder: the code resolved that folder (FR-37). It is the E17/F-6 "refusal naming the folder" the spec asks for. Accepted.

## Key 6: class-wide completeness (axes 8, 16, 17, 32, 34)

- Axis 8: both recognitions go through `hooklib.is_story_folder` (the leaf) plus the `pipeline.json` marker in one `_story_at`. I checked for a sibling path-part story recognition with a case-insensitive Grep `==\s*["']artifacts["']` over `scripts/*.py`. The only hits are `vcs_evidence.py:615` (the edited site, which is the positive control) and the test helper `tests/state_census.py:274`. There is no production twin. Covered.
- Axis 16: one config reader, now in hooklib. `artifact_root`'s own `json.loads` is gone. `load_config` (`{}`) is a non-goal. The axis 16 twins row already names the project-config reader class as queued. The test_read_json G5 census is green inside 499/499. Covered.
- Axis 17: `unreadable_record` (DV.Record). No new parser. Covered.
- Axis 32: no row added, removed or reclassified (Key 3). Covered.
- Axis 34: one road per action (one config reader, one story predicate). No language, project or case is excluded. Covered.
- Residuals: the U rows go to OF4-10r = OF5-12. The literal `qa-factory/artifacts` texts (`vcs_evidence` :646 existing text, `driver_sources:356`, hooklib's home literal, analog (f)) go to OF4-21b = OF5-13. Both are queued per the t-303 census. The new key text naming `qa-factory/artifacts` belongs to analog (f)'s list for OF4-21b. It is correct today.

## Key 7: DUPLICATION AND CONSISTENCY, CODE QUALITY, ONE ROAD, JUDGMENT

- **DUPLICATION AND CONSISTENCY**: none blocking.
  - The move deletes the config_contract copy, so there is net one reader.
  - `_story_at` folds the inline predicate of branch (1).
  - The only in-diff copy is O1's twin literal, which the census forces.
  - `tools/dup_ratchet.py --check --repo <wt>`: scripts give 0 new, 0 grown, with 1 carried group (`factory_dashboard`/`metrics_projection` `_has_factory_activity`, unrelated to this diff). tools give 0 new. rc=0.
  - The test drivers `_root_writer` and `_root_grounding` repeat the `project_root` save/patch/restore. That follows the precedent `_site_report_adapt` and is not worth a helper.
- **CODE QUALITY**:
  - No new function exceeds about 60 lines or three nesting levels. `left_out_by_person`'s new block is 20 lines at depth 2.
  - No dead branch.
  - One lying name/check (F2) and one lying text (F1), both fix-before-merge.
- **ONE ROAD** (item 12): none found. No exclusion of a language, project or case. Both story recognitions now use one predicate.
- **JUDGMENT** (item 11): none. The new checks judge data (file presence, parse, key shape), not a role's content. The `judgment: none` line is consistent with the census.

## Trail

Read:
- the spec t-289 (whole), the builder report t-308, the census t-303, the t-300 B2 lines;
- the full code and test diff `origin/main...36083da`;
- at the commit: exit_gate.py :245-320, :750-775, :1514-1535; vcs_evidence.py :593-700; test_vcs_evidence.py :25-60;
- SIBLING_MAP axes 8, 16, 17, 32, 34; critic-diff-brief items 6, 7, 11, 12; the schema; the commit message (DoD 6 lines present).

Control re-runs (worktree 36083da):
- `python -B <wt>\...\tests\test_read_json.py` gives `=== read_json: 499/499 ok ===`, which matches the witness.
- `python -B <wt>\...\tests\test_vcs_evidence.py` gives `=== test_vcs_evidence: 157/157 ok ===`, with V1-V8 PASS lines. This matches the witness.
- `python -B <wt>\...\tests\test_judgment_census.py` gives `=== judgment_census: 22/22 ok ===`.
- `python -B <wt>\...\refusal_registry.py --check` gives rc=0 and `A24 refusal registry: no violations`.
- `refusal_registry.sites(files=['hooklib.py'])` lists `artifact_root` at lines 738 and 745.
- Import-order probes: all ok, identity `True`, and hooklib alone does not load config_contract.
- Key-text probe:
  - `"a\x00b"` gives "got a blank string" (F1);
  - `true` gives `bool`, and `{}` gives `dict`;
  - `{}` config gives `qa-factory\artifacts`.
- exit_gate probe on a `{not json` config, project pinned:
  - `_identity` gives no raise for `""` and `"S-1"`;
  - `awaiting_source_review` gives False. The probe role was not an S1 role, so this probe is weak for P7, which rests on reading;
  - `grounding_errors(tester)` gives `['unreadable']`, and for another role `[]`.
- `tools/dup_ratchet.py --check` gives rc=0, 0 new.
- `git diff --stat` on the census, test-layers and refusal files gives an empty diff.

The verdict is an input to acceptance. Acceptance stays with the coordinator of the proper tier.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 hooklib.artifact_root: a key containing NUL is reported as 'got a blank string'; give it its own label (e.g. 'a path with a NUL character') keeping both literal raise ValueError sites inside artifact_root (P1c), and assert in T1 that the key_nul text does not contain 'blank'",
    "F2 test_read_json.test_the_artifact_root: 'every site has a cell per state' compares only dict lengths; compare sorted(ROOT_EXPECT) with sorted(ROOT_STATES) before the loop"
  ],
  "class_completeness": "Axes 8 (one _story_at predicate over is_story_folder plus pipeline.json; grep for path-part story recognitions finds only the edited site and a test helper), 16 (one config reader in hooklib, artifact_root json.loads gone), 17 (unreadable_record), 32 (census untouched, sites keep artifact_root at 738/745), 34 (one road, no exclusions): covered. Residual U rows queued as OF4-10r/OF5-12, literal default-folder texts as OF4-21b/OF5-13 per census t-303.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-289-of4-10-artifact-root.md",
      "docs/tasks/specs/reports/t-308-of4-10-builder-report.md",
      "docs/tasks/specs/reviews/t-303-of4-10r-census.md",
      "docs/tasks/specs/reviews/t-300-of4-10-of4-21-plan-review.md (B2 lines)",
      "git diff origin/main...36083da (all 7 files)",
      "exit_gate.py at 36083da :245-320, :750-775, :1514-1535",
      "vcs_evidence.py at 36083da :593-700",
      "tests/test_vcs_evidence.py :25-60",
      "docs/SIBLING_MAP.md axes 8, 16, 17, 32, 34",
      "docs/tasks/critic-diff-brief.md items 6, 7, 11, 12",
      "tests/fixtures/judgment-census.json :394-402",
      "commit message of 36083da"
    ],
    "reruns": [
      {"command": "python -B <wt>/ai-packages/qa-factory/scripts/tests/test_read_json.py", "result": "=== read_json: 499/499 ok ==="},
      {"command": "python -B <wt>/ai-packages/qa-factory/scripts/tests/test_vcs_evidence.py", "result": "=== test_vcs_evidence: 157/157 ok === (V1-V8 PASS)"},
      {"command": "python -B <wt>/ai-packages/qa-factory/scripts/tests/test_judgment_census.py", "result": "=== judgment_census: 22/22 ok ==="},
      {"command": "python -B <wt>/ai-packages/qa-factory/scripts/refusal_registry.py --check", "result": "rc=0, A24 refusal registry: no violations"},
      {"command": "refusal_registry.sites(files=['hooklib.py']) filtered on artifact_root", "result": "two sites, lines 738 and 745"},
      {"command": "import-order probes config_contract/hooklib/exit_gate/vcs_evidence", "result": "all import; identity True; hooklib alone does not load config_contract"},
      {"command": "artifact_root key probe", "result": "a NUL value reports 'got a blank string' (F1); true->bool, {}->dict; empty object -> qa-factory/artifacts"},
      {"command": "exit_gate probe on a {not json config", "result": "_identity no raise; awaiting_source_review False; grounding_errors tester -> unreadable, other role -> []"},
      {"command": "python -B <wt>/tools/dup_ratchet.py --check --repo <wt>", "result": "rc=0, scripts 0 new 0 grown, tools 0 new"},
      {"command": "git diff --stat origin/main...36083da -- *judgment-census.json *test-layers.json *refusal*", "result": "empty"}
    ]
  }
}
```
