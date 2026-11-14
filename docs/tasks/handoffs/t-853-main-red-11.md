# t-853 main red 11 report

Done: edge-3 row in experiments/measurers/test_measurers.py now compares `str(PureWindowsPath(...))` for both halves (HERE not in line; runs dir in line); `PureWindowsPath` added to the pathlib import. prepare_copy.py untouched.

Commit ff564e19 on branch fix/main-red-11 (from origin/main 6d31157f), pushed, not merged.

## Witness (Windows)
`python -B experiments/measurers/test_measurers.py` tail:
```
=== test_measurers: 607/607 ok ===
PASS start line: with no runs folder named the logs go under BASE, never into the measurers' folder (edge 3)
```
No FAIL lines.

## Linux-shape control (scratchpad script, not committed; BASE set to PurePosixPath("/home/x"))
```
\home\x\runs True
\home\x\runs True False
```
Line 1: `str(PureWindowsPath("/home/x/runs"))` equals `\home\x\runs`. Line 2: the expected Windows rendering is in the product line (True); the POSIX `/home/x/runs` is not (False), which is why the old expectation failed on Linux.

## Notes
Siblings: none noticed. Needed beyond the manifest: none. Commit hooks ran green.
