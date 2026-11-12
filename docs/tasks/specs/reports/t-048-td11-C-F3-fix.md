# t-048 attempt 2 -- TD-11 C-F3 fix round (split-keep + K5 door)

Files changed in WT: `tools/test_quarantine.py`, `tools/test_test_quarantine.py`. No commit.

## Findings fixed

| finding | how | test |
|---|---|---|
| C-B1 shim covers | `_split_common(old)` strips `test_`: shim `covers = ["tests/<stem>_common.py"]` (e.g. `tests/k_common.py`) | `test_split_keep_with_shim_rewrites_the_old_row` (pin corrected to `tests/k_common.py`) |
| C-B2 door scope | new `_split_problems(root, sha, sold, parts, old, new, gone)` called from `check_history`; reads the commit tree through the existing `_blob_id(root, sha, rel)`. Part must be: a keep row added by this commit (in new, not in old), named `<OLD stem>_*.py`, in the tree, same layer as OLD's row. OLD: file absent from tree AND row removed; or file present AND row is a shim row (named_by empty, why starts "split shim"). Old row not a keep row in the parent: refused | `test_check_keep_split_door[...]` rows: part-not-in-keep, part-file-not-in-tree, part-is-an-older-row, part-not-old-stem, part-layer-differs, old-row-removed-file-stays-no-shim, old-file-stays-row-not-a-shim, old-file-gone-row-stays, old-not-a-keep-row, keep-split-accepted, keep-split-shim-accepted |
| decision 3 / C-F1 | command refuses a part not `<old stem>_*.py` (placed after the row-exists checks) | `test_split_keep_refusals_write_nothing[part-not-old-stem]` |
| decision 4 / C-F2 | shim row `named_by: []`; why names importers via new optional `--importers A,B` (default text "importers") | shim test above (asserts `named_by=[]` and the why with importers) |
| C-F3 | each part's covers gets `tests/<stem>_common.py` appended when the file is on disk and not already listed | `test_split_keep_adds_the_common_file_to_part_covers_when_on_disk` |
| edges | zero parts / old row absent / old in quarantine or pin_holds | `refusals_write_nothing[into-empty, old-not-a-keep-row, old-is-a-quarantine-row, old-is-a-pin-row]` |
| C-F4 | text below (commit message, SIBLING_MAP line) | -- |

Positional invariant: the door runs at the same place as before (the keep-split block of `check_history`); a plain removal with no door is still refused (`bare-removal-still-refused`), a plain keep row returning a quarantined file is still refused (`returns-from-quarantine-plain-new-file-still-refused`), keep-drop still accepted, layer change without a line unchanged.

Existing K5 code CAN see the commit's tree (`_blob_id(root, sha, rel)` = `rev-parse sha:path`), so the old-file check is on the commit that carries the line, as decided. Consequence for the closing commit: the old file must be gone (or shimmed with its row rewritten) in THAT commit.

## Witness

`python -m pytest .../tools/test_test_quarantine.py -q -k split` -> `33 passed, 235 deselected in 38.06s`
`python -m pytest .../tools/test_test_quarantine.py -q` -> `268 passed in 171.24s (0:02:51)`

`-k split` rows: refusals_write_nothing[old-not-a-keep-row, old-is-a-quarantine-row, old-is-a-pin-row, part-is-a-keep-row, part-is-a-pin-row, part-not-on-disk, part-is-quarantined, part-equals-old, part-not-old-stem, into-empty, into-empty-name, into-duplicate, reason-blank, no-shim-old-on-disk, shim-old-missing]; test_split_keep_without_shim_inherits_removes_old_and_writes_the_message; test_split_keep_with_shim_rewrites_the_old_row; test_split_keep_adds_the_common_file_to_part_covers_when_on_disk; test_check_keep_split_door[keep-split-accepted, keep-split-shim-accepted, keep-split-part-not-in-keep, keep-split-part-file-not-in-tree, keep-split-part-is-an-older-row, keep-split-part-not-old-stem, keep-split-part-layer-differs, keep-split-old-row-removed-file-stays-no-shim, keep-split-old-file-stays-row-not-a-shim, keep-split-old-file-gone-row-stays, keep-split-old-not-a-keep-row, bare-removal-still-refused, returns-from-quarantine-plain-new-file-still-refused, keep-drop-still-accepted, layer-change-without-line-is-as-before].

C-B2 temp-repo demo (script `scratchpad/demo_cb2.py`, repo in a temp dir; row of test_k.py removed, file stays, message `keep-split: test_k.py -> test_other.py -- not really a split`, test_other.py an older keep row), calling `tq.check_history`:
```
ON_DISK True
VIOLATIONS 1
  0841699a keep-split line for test_k.py names part test_other.py which is not a keep row added by this commit -- (python tools/test_quarantine.py split-keep writes the rows) or fix the line
```
(`check` itself needs the package selftest.py in the root, absent in the temp repo, so the door function `check_history` was called directly.) The same scenario with proper part names but the old file left on disk is the test row `keep-split-old-row-removed-file-stays-no-shim`.

## K5 door -- four questions (for the commit message)

- (a) Cost and who pays: the integrator of the closing commit runs `split-keep` (one command, writes the message file) and must delete the old file or keep it as a shim in that same commit; a node pays nothing (R-A1: nodes never write test-layers.json). Check cost: one `rev-parse` per named part plus one for OLD per keep-split line, only on commits that carry the line.
- (c) Detector of the door's failure (misuse/leak): the K5 history check itself (`tools/test_quarantine.py check` in `forge-check`), whose cases `test_check_keep_split_door` pin each refusal; a split line that passes without a tree match would show as a red row there. Recognition of an unregistered keep-row removal: `bare-removal-still-refused`.
- (d) What stops it being skipped: removing a keep row without `keep-split:`/`keep-drop:`/`quarantine-enter:` is refused by K5 in `check` (pre-commit and CI `forge-check`); the line itself is written by `split-keep` into `ci-out/keep-split-msg.txt`. A line that does not match the tree is refused. Skipped only on discipline for the human step "use -F ci-out/keep-split-msg.txt", detector: the same K5 refusal on the next check.

Axis block / mechanism: this IS a mechanism (new K5 door + commit-line convention); `axes: not a mechanism` from the first report is withdrawn. Axis lines for the Lead to fill per current SIBLING_MAP (not re-enumerated here: I did not walk all axes); axis 18 below.

## SIBLING_MAP axis 18 line (text for the Lead; row ~387)

Current: "a `keep` row leaves only through `drop-keep` or a phase-2 `enter`". Proposed: "a `keep` row leaves only through `drop-keep`, a phase-2 `enter`, or `split-keep` (one row becomes N part rows named `<old stem>_*`; the K5 door `keep-split:` is judged on the commit's tree: parts added there and on disk, the old file absent or shimmed with its row rewritten)".

## Deviations / notes

- Added optional `--importers` option (the verdict offered it or reading T-3's row block; chose the option). Remove if the Lead prefers the other.
- The door's "part added by this commit" (not in the parent's keep) comes from the verdict's C-B2 wording; decision 2 lists prefix/exists/layer/old-state only. It is additive and tested (`keep-split-part-is-an-older-row`).
- Shim recognised in the door by `named_by` empty and `why` starting "split shim" (the command's own form), not by layer change as before.
- Needed beyond the manifest: `tools/test_test_quarantine.py` helpers (`relayers`, `base_repo`, `_returns`), `_blob_id`/`_git` in test_quarantine.py.
- Same class nearby (not touched): `drop-keep` has no tree-state check of its own beyond `dropped` (file deleted in commit); fine. T-3 side: the common-file name rule exists in two places now (`_split_common` here and `common_stem_for` in test_split.py); a shared constant would belong with the T-4 shared-reader node.

## Questions

None blocking.
