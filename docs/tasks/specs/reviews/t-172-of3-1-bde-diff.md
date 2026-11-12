# t-172 — critic on OF3-1 nodes b, d, e (one pass per topic, R13-g)

Base `e20c3a2` (wip/of3-1a). b = wip/of3-1b 6c5a8a3; d = wip/of3-1d 86510cb; e = wip/of3-1e 2bbfce4 + da19ace.
Spec: `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` items 5, 7 (node d), 8, node table :466-512, siblings :514-519.

## Verdict

- **node b — ACCEPT** (two optional minors, b-1, b-2).
- **node d — NEEDS WORK: 1 must (d-1), 1 minor fix before merge (d-2).**
- **node e — ACCEPT** (one minor, e-1); one residual of the class proposed as a node (R-1), outside e's owns.
- Merge of the three: no conflict (trial `git merge-tree` b+d, then +e: clean; no file shared among them; none of their files changed on `main` since the base).

Overall: NEEDS WORK, 1 blocking finding (d-1). The decision to accept stays with the Lead (rule 6).

## Findings

### d-1 (MUST, blocks d's merge) — the story under a configured root breaks the receipt writer's project root

`vcs_evidence.py:667-668` (unchanged by the diff, a reader of `_story_root_of`'s output):

```python
story = _story_root_of(args.output)
record_api_receipt(story.parents[2] if story else project_root(), result)
```

`parents[2]` assumes the default layout `<project>/qa-factory/artifacts/<T>`. Before d, `_story_root_of` returned a story ONLY
in that layout, so the assumption held. After d, step (1) returns `<configured root>/<T>`:

- `artifact_root: "stories"`, story `C:\p\stories\S-2` -> `parents[2]` = `C:\` (measured: `PureWindowsPath(r'C:\p\stories\S-2').parents[2]` -> `C:\`).
  `_current_adapter(C:\)` reads `C:\qa-factory\config.json` -> None -> `record_api_receipt` returns None: the `ok`/`denied` API
  receipt of the host is silently NOT written.
- `artifact_root: "."`, story `C:\p\S-2` -> `parents[2]` raises `IndexError` (measured) -> swallowed by `except Exception` -> same loss.
- an absolute root elsewhere -> `parents[2]` is an unrelated folder; if it happens to hold a `qa-factory/config.json`, the receipt
  goes into ANOTHER project (AR-4, AR-14 writer pointed at the wrong home).

Before d all three cases fell to `project_root()` and the receipt was written. So d turns a working write into a silent loss — the
producer-reader walk of AR-22 / brief q10 was not done for the second consumer of `_story_root_of` (the spec's recognition order
names only the consultation consumer at :626). Nothing in the new `ROOT_ROWS` sees it: they assert only the exit code.
Fix: at :668 use `project_root()` unconditionally (step (1) already derives the root from the same env project root; the
default-layout case gives the same project), or `runtime_paths.project_for_task(story)`. Plus one row in `ROOT_ROWS`
or beside it: "output in a story of the configured root: the API receipt lands in `<project>/qa-factory/state/host-receipts`"
(the edit touches `main`, a line outside d's owns `_story_root_of only` — the Lead widens d's owns by this one line for the fix
round, or opens it as d's fix node).

Surface: "project root derived from a story folder by fixed depth". Neighbouring classes walked (axis 8, map only):
`walk_timing.py:172`, `:241` (`task_root.parents[2]` as project / config home) and `gate_brief.py:2303` (`task_root.parents[2]`)
carry the same defect for any story under a configured root; they are outside this diff and pre-existing (they misbehave
already on `main` once `artifact_root` is set). Proposed node (owner: Lead of the OF3 batch; `gate_brief.py` is stream hooks4's file, so after it merges):
`OF3-1d3: story -> project by depth (walk_timing :172/:241, gate_brief :2303) onto runtime_paths.project_for_task | узел: OF3-1d3`.
Also pre-existing on the same consumer: `vcs_evidence.py:628` calls `artifact_root()` under `except OSError` only — a broken config
with an `--output` outside every story raises `ValueError`/`AttributeError` as a traceback. Same class as spec finding (4) §7
(traceback instead of a refusal); fold it into OF3-1d2 with `dispatch_liveness` (same function shape) or into d's fix round — Lead's call.

### d-2 (minor, fix before merge) — a stray edit outside the owned clause

`local_keys.py:134`: `names += _listing(artifacts) + _listing(...)` became `names += _listing(artifacts)+ _listing(...)`. A
whitespace edit outside `_taken`'s except clause (owns: "except clause only") that also breaks PEP 8 spacing. Revert that line.

### b-1 (minor, optional) — dead code left by the conversion

`check_coverage.py:97-101`: after `if cfg is None: return None`, `cfg` is always a dict, so `(cfg or {})` on the next line is dead.

### b-2 (minor, optional) — test lint

`tests/test_read_json.py:11` adds `import os`, never used (grep `\bos\b` in the file: only the import line). The last check of
`test_the_config_readers` (`hasattr(config_contract, "read_config_file")`) is a pin on the source shape (brief q5, `docs/TESTING.md`
«не пишется»): the seven rows already exercise the reader; drop it.

### e-1 (minor, queue or fix) — invisible characters in test source

`tests/test_manual_capture.py`: 4 lines hold a literal U+FEFF inside string literals (grep of the byte sequence `EF BB BF`: 4). It
passes `--lang` / FR-29 (not a control byte), but a reader cannot see which rows carry a BOM; `"\ufeff"` says it. Also the
row "a lone quote kept" (`A="` -> `"`) pins a choice: in `gate_preflight.env_values` (empty values left out) such a key used to be
absent and now counts as set. Pathological input, error direction "present" on a malformed line; acceptable, named here so the
Lead sees it.

## Fit to the spec (q1)

- b: each of the seven sites takes exactly the call of item 5's table (verified line by line against :377-383, incl. `errors` and
  `kind`); `environment_record` keeps its `isinstance(cfg, dict)` coercion at the return, so the no-`kind` read still yields `{}` for a
  list (row `list -> {}` green). `import_test_receipt`: absent -> "...does not exist"; `ConfigUnreadable`/`OSError` -> refusal
  with cause; non-object -> refusal (was crash). G5 `KEPT` loses exactly `grammar.load_overrides` and `test_locations._config_of`.
- d: `role_load._task_root` and `local_keys._taken` as specified. `_story_root_of` follows the recognition order (1)(2)(3); the
  three broken-config classes skip (1) only (`artifact_root` raises `ValueError` for bad JSON / bad value, `AttributeError` for a
  list/string/null config — traced at `hooklib.py:636-649`); `is_story_folder` errs only toward "no" (`hooklib.py:255-270`) and
  the `pipeline.json` marker is required. The spec's rows are present; the case-variant deviation is sound (a case-blind FS
  resolves the existing prefix to the real spelling, so the row could not exercise the "no" side; the exact-name rule is pinned in
  hooklib's tests). Not a row: "output on another drive" (listed among adversarial inputs, not among required test rows; it falls to
  `relative_to` ValueError -> wider). Fit fails only on d-1 (a consumer the spec did not name).
- e: `parse_env_file` takes manual_capture's rules (BOM, `export `, empty name, one paired quote); `manual_capture._env_values` is a
  caller; `stand_health._env_values` reads the list through `gate_preflight.configured_env_files` (it receives the `environment`
  block at both call sites :491-492 and :809-810, which is what `configured_env_files` expects); `brief_pack` unchanged in call;
  `load_env` order untouched. The da19ace fix (`export =x` skipped) is a builder decision in the safe direction.

## e's inherited behaviour change, per caller

Diff of the parse: + BOM dropped, + `export ` dropped, + `=x` skipped; - mixed/stacked quotes no longer stripped
(`A="x'` keeps both, `A="'x'"` -> `'x'`, `A="` -> `"`).
- `gate_preflight.env_values` (:1043-1053), `_stray_env_file` (:5132), `_env_names` via `_loaded_env_files`: `export KEY=` now
  counts as set — previously "missing" for a key present in the file; strictly a fix. Only regression direction: the lone/stacked
  quote case above (e-1).
- `env_probe.load_env` (:135), `_frontend_hint` (:522), stand keys (:486): `export FRONTEND_URL=` now read — this is exactly the
  "known defect" the QUARANTINED `test_frontend_reader.py` K4 pins; re-run: 110/112, the 2 FAILs are K4 "(known)" and its note
  row, nothing else. Lead's decision (quarantine-watch catch) stands; the pin documents a defect now fixed.
- `brief_pack._env_file_key_names` (:2546): names now `API_TOKEN`, not `export API_TOKEN`; the BOM-prefixed first name is now
  matched by `SECRET_NAME` where it was `\ufeffNAME`. Better; e's own two-file row pins it.
- `project_inventory` (:401, :420): `http_address_keys` no longer offers a key named `""` or `export X`; better.
- `source_inventory` (:76): fills missing keys; gains the `export` names; no harm.
- `machine_facts._env_file_values` (:318-323): still strips `export ` itself — now dead (R-1). `test_collect_redact.py:387-390`
  still holds (key `API_KEY` either way).
No caller hurt beyond e-1's pathological case.

## Builder decisions (q2), seams (q3)

b: none beyond the table. d: `except (OSError, ValueError, AttributeError)` around the whole of step (1) also swallows a failed
`is_story_folder`/`is_file` (OSError) -> wider: safe. e: `export =x` -> skipped (safe); a missing file in `env_files` -> skipped
via `OSError` (same as the old single-file path). Seams: none of the three writes another node's or live stream's file; c and e
share `env_probe.py` (D-0048: the later merges `main` first) — c is not yet dispatched.

## Class-wide completeness (q4)

- axis 16 (config readers): b folds the seven of GW1-38; the remainder is N-r4 (spec). Covered.
- axis 8 (story on disk): d folds its three sites; OF3-1d2 queued (spec). NEW, from d-1: the depth-derived project root
  (`vcs_evidence:668` in the fix round; `walk_timing:172/:241`, `gate_brief:2303` -> proposed OF3-1d3) and `vcs_evidence:628`
  traceback (OF3-1d2 or d's round).
- env-file reading (AR-13; axis "how the stand logs in" :127 names `environment.env_file`): e folds the PARSE. R-1 (proposed node,
  owner Lead of the OF3 batch): the file LIST is still read by other roads — `machine_facts.secret_values` reads only
  `env_file` (ignores `env_files`), `source_inventory` (:60-68) reads both `env_file` AND `env_files`, `env_probe._frontend_hint`
  (:518) / stand keys (:483) / `load_env` (:131) read only `env_file`; and `machine_facts._env_file_values` keeps a dead `export ` strip.
  `load_env` order is a spec non-goal (F11), its FILE LIST is not. Line for «Остатки»:
  `env-file list read past gate_preflight.configured_env_files (machine_facts, source_inventory, env_probe._frontend_hint/stand keys/load_env) + machine_facts dead export strip | узел: OF3-1e2`.

## DUPLICATION AND CONSISTENCY (q6)

- b: none new — the seven copies are removed onto `hooklib.read_json:694` / `config_contract.read_config_file:1349`. Grepped
  `json.loads(.*config.json` shapes in the seven files after the diff: none left in the touched functions.
- d: none new — `artifact_root` / `is_story_folder` reused. Residual: d-1's depth derivation duplicates
  `runtime_paths.project_for_task` (used by `environment_record._story_context`).
- e: the manual_capture parse copy is gone (one parser left: grep `def parse_env_file|def _env_values` -> env_probe:103,
  manual_capture:607 (one-line caller), stand_health:432). Residual: `stand_health._env_values` (:432-444) and
  `gate_preflight.env_values` (:1043-1053) are two merges of "process env + files laid over" (they differ in empty values and the
  `is_file` check); folding them changes stand_health's empty-value semantics, so it belongs to R-1 / OF3-1e2, not this round.

## CODE QUALITY (q7)

No new function over ~60 lines or past three nesting levels; no copy-paste inside the diffs. Findings: b-1 (dead `cfg or {}`),
b-2 (unused import, source pin), d-2 (stray edit), e-1 (invisible chars). None blocks.

## ONE ROAD (q12)

b, d: none found — every changed site now goes through the shared reader; no language/project branch added (grepped the
diffs for language or runner names: none). e: the parse is one road now; the env-file LIST is not (R-1) — an existing multi-road
residual, proposed as node OF3-1e2 with its owner (rule 19), not a line to pass on.

## Ratchets, architecture, judgment (q9-q11)

b shrinks G5 `KEPT` by 2 (named in its commit, AR-20). No ratchet raised by d or e (no allow-list row moved; `OUTSIDE_WALKS`
untouched). Architecture lines present on all four commits; d names AR-4/AR-13/AR-28 but its AR-22 walk missed the :668 reader
(d-1). Judgment: none moved in any of the three (data reads only).

## Trail

Read: spec t-129 :350-519; `docs/tasks/critic-diff-brief.md`; `docs/SIBLING_MAP.md` :127; diffs `git -C <worktree> diff e20c3a2 HEAD`
for all three; `hooklib.py` :255-280, :636-649, :694-711; `config_contract.py` :1321-1374; `environment_record.py` :396-410;
`import_test_receipt.py` :26, :52-70; `vcs_evidence.py` :456-500, :579-630, :655-670; `role_load.py` :534-545, :598, :628;
`gate_preflight.py` :1027-1053, :4530-4540, :5120-5135; `stand_health.py` :430-444, :480-495, :800-812; `env_probe.py` :101-140,
:478-525; `machine_facts.py` :308-355; `project_inventory.py` :395-425; `source_inventory.py` :60-85; `brief_pack.py` :2546;
`test_frontend_reader.py` :170-195; the three test diffs. Greps (case-insensitive where content-negative): `parse_env_file`
over the package (16 hits, positive control = the known definition env_probe:103); `export [A-Z_]*=` over tests (8 files);
`_story_root_of|parents\[2\]` over scripts (positive control: the known :668 hit).

Re-runs (cheap control, one per verdict-bearing file):
- `python -B <of3-1b>/.../tests/test_read_json.py` -> `=== read_json: 440/440 ok ===`
- `python -B <of3-1d>/.../tests/test_vcs_evidence.py` -> `=== test_vcs_evidence: 131/131 ok ===`
- `python -B <of3-1d>/.../tests/test_local_keys.py` -> `=== test_local_keys: 199/199 ok ===`
- `python -B <of3-1d>/.../tests/test_role_load.py` -> `=== role_load (the one measure of a role's start load): 171/171 ok ===`
- `python -B <of3-1e>/.../tests/test_manual_capture.py` -> `=== test_manual_capture: 1088/1088 ok ===`
- `python -B <of3-1e>/.../tests/test_frontend_reader.py` (quarantined, read-only) -> `110/112`; FAILs: `K4 (known): export FRONTEND_URL=... is not read by the block` and `K4: ... the note says the key is not set`
- `python -c "PureWindowsPath(r'C:\p\stories\S-2').parents[2]"` -> `C:\`; `PureWindowsPath(r'C:\p\S-2').parents[2]` -> `IndexError: 2`
- `git merge-tree --write-tree wip/of3-1b wip/of3-1d` -> clean; result tree + `wip/of3-1e` -> clean; `git diff --name-only e20c3a2 main -- <each branch's files>` -> empty (positive control: the unfiltered diff lists 50 files, a-node package files among them).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "d-1: vcs_evidence.py:668 derives the project as story.parents[2]; after d a story under a configured artifact_root makes it the wrong folder (C:\\ for stories/S-2, IndexError for artifact_root '.'), so the API host receipt is silently not written (or written into another project); before d it fell to project_root() and was written"
  ],
  "class_completeness": "axis 16: b folds GW1-38's seven, remainder N-r4 (spec). axis 8: d folds three sites, OF3-1d2 queued; new from d-1: vcs_evidence:668 in d's fix round, walk_timing:172/:241 and gate_brief:2303 proposed as OF3-1d3, vcs_evidence:628 traceback into OF3-1d2 or the fix round. env-file reading: e folds the parse; the file LIST still has other roads (machine_facts env_file only, source_inventory both keys, env_probe _frontend_hint/stand keys/load_env env_file only) and machine_facts keeps a dead export strip: proposed OF3-1e2, owner Lead of the OF3 batch.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-129-of3-1-knowledge-catalog.md:350-519",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md:127",
      "ai-packages/qa-factory/scripts/hooklib.py:255-280,636-649,694-711",
      "ai-packages/qa-factory/scripts/config_contract.py:1321-1374",
      "ai-packages/qa-factory/scripts/vcs_evidence.py:456-500,579-630,655-670",
      "ai-packages/qa-factory/scripts/role_load.py:534-545",
      "ai-packages/qa-factory/scripts/gate_preflight.py:1027-1053,4530-4540,5120-5135",
      "ai-packages/qa-factory/scripts/stand_health.py:430-495,800-812",
      "ai-packages/qa-factory/scripts/env_probe.py:101-140,478-525",
      "ai-packages/qa-factory/scripts/machine_facts.py:308-355",
      "ai-packages/qa-factory/scripts/project_inventory.py:395-425",
      "ai-packages/qa-factory/scripts/source_inventory.py:60-85",
      "ai-packages/qa-factory/scripts/tests/test_frontend_reader.py:170-195",
      "diffs e20c3a2..HEAD of worktrees of3-1b, of3-1d, of3-1e"
    ],
    "reruns": [
      {"command": "python -B of3-1b/ai-packages/qa-factory/scripts/tests/test_read_json.py", "result": "read_json: 440/440 ok"},
      {"command": "python -B of3-1d/ai-packages/qa-factory/scripts/tests/test_vcs_evidence.py", "result": "test_vcs_evidence: 131/131 ok"},
      {"command": "python -B of3-1d/ai-packages/qa-factory/scripts/tests/test_local_keys.py", "result": "test_local_keys: 199/199 ok"},
      {"command": "python -B of3-1d/ai-packages/qa-factory/scripts/tests/test_role_load.py", "result": "role_load: 171/171 ok"},
      {"command": "python -B of3-1e/ai-packages/qa-factory/scripts/tests/test_manual_capture.py", "result": "test_manual_capture: 1088/1088 ok"},
      {"command": "python -B of3-1e/ai-packages/qa-factory/scripts/tests/test_frontend_reader.py", "result": "110/112; the two FAILs are the K4 known-export pin and its note row"},
      {"command": "python -c PureWindowsPath parents[2] probe", "result": "C:\\p\\stories\\S-2 -> C:\\ ; C:\\p\\S-2 -> IndexError: 2 ; C:\\p\\qa-factory\\artifacts\\S-2 -> C:\\p"},
      {"command": "git merge-tree --write-tree wip/of3-1b wip/of3-1d, then + wip/of3-1e", "result": "clean, no conflicts"}
    ]
  },
  "fixes": [
    "d-1 (must): vcs_evidence.py:668 use project_root() (or runtime_paths.project_for_task(story)) instead of story.parents[2]; add a row: output in a story of the configured root -> the API receipt lands under <project>/qa-factory/state/host-receipts (Lead widens d's owns by that line)",
    "d-2 (fix before merge): local_keys.py:134 revert the stray whitespace edit outside the except clause",
    "b-1 (optional): check_coverage.py drop the dead (cfg or {}) after the None return",
    "b-2 (optional): tests/test_read_json.py drop the unused import os and the hasattr source pin",
    "e-1 (optional): tests/test_manual_capture.py write the BOM as an escape instead of 4 literal U+FEFF characters",
    "proposed nodes for the Lead: OF3-1d3 (story to project by depth: walk_timing:172/:241, gate_brief:2303) and OF3-1e2 (env-file list readers onto configured_env_files, machine_facts dead export strip)"
  ]
}
```
