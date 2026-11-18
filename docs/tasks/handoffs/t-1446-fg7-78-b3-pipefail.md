# t-1446 FG7-78 B3 pipefail fix (critic t-1443 F6)

DONE: driver-golden.yml.proposed gained job-level `defaults: run: shell: bash` (GitHub's explicit bash = `bash --noprofile --norc -eo pipefail {0}`), covering both tee steps. File: .github/workflows/driver-golden.yml.proposed. No other change.

## Key-presence script (full source)
```python
import sys
t = open(sys.argv[1], encoding="utf-8").read()
miss = [k for k in ("defaults:", "shell: bash") if k not in t]
print("MISSING", miss) if miss else print("ALL KEYS PRESENT")
sys.exit(1 if miss else 0)
```
Run on the file: `ALL KEYS PRESENT` rc=0
Negative control (copy without the `shell: bash` line): `MISSING ['shell: bash']` rc=1

## Step-body run (stand-in tool prints exit=2, then `| tee`, then a "compare" echo)
With `bash --noprofile --norc -eo pipefail`: output `exit=2`, job_rc=2, compare NOT reached.
Control without pipefail (-e only): `exit=2`, `REACHED compare`, job_rc=0 (the original defect).
Exit 1 of compare / only exit 0 green follow from the same pipefail semantics (not separately run).

Deviations: none. Siblings: none pipe into tee (per spec). Needed beyond manifest: none.
