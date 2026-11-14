# t-785 main-red4 report

## Cause (inferred; NOT provable on Windows)
Not exactly the hypothesis. The Lead's hypothesis was about `resolve()`; the read of the code gives a different seam. On Linux
`Path.resolve()` (non-strict) swallows the error, but `Path.is_file()` raises `OSError(ENAMETOOLONG)` for a 40,000-char name
(pathlib ignores only ENOENT/ENOTDIR/EBADF/ELOOP). That `OSError` is not a `ValueError`, so:
1. the test's own helper `os_text` (it caught only `ValueError`) crashed on the first os_rows row at table-building time,
   an uncaught exception 0.3 s into the file - this matches "exit 1 in 0.3 s, no failing row name";
2. the product `_judge_refs` also caught only `ValueError`, so on Linux `append` would leak the `OSError` (a P31 defect:
   one behaviour on every OS was not kept).
Proved on Windows: the new rows pass; the old code path raised `ValueError` only here. Inferred (no Linux run here): the
Linux exceptions above. The old rows also quoted the OS's wording, so they were OS-dependent by design.

## Changed
- `exploratory_findings.py`: `_judge_refs` now catches `(ValueError, OSError)` around resolve/is_file/hash. A name that
  cannot exist (ValueError, or OSError errno ENAMETOOLONG/EINVAL/ENOENT/ENOTDIR) is that ref's own sentence
  `evidence path '<path cut at 80 chars + ...>' is not a file under the task root <root>: the path cannot be read as a file`
  (the judge's "not a file under the task root" sentence plus a factory tail; no OS wording); collected with the other problems.
  Any other OSError (PermissionError, EIO) is re-raised unchanged (edge 2). New helpers `_name_cannot_exist`, `_unmeasurable_text`, `PATH_SHOWN = 80`.
- Test: `os_text`/`os_rows` (OS-dependent) replaced by rows driven by patched `Path.is_file` / `sha256_file`:
  ValueError, ENAMETOOLONG, EINVAL, ENAMETOOLONG while hashing (alone and joined with two other problems, `==`), path lengths
  79/80/81/40000 (cut, never echoed whole), PermissionError and EIO keep OSError, restore check, and the real 40,000-char and NUL
  paths asserting only the OS-independent facts (the ref's sentence present, other problems present).
  Note: the real-path rows accept either the factory sentence or the contract's plain "is not a file under the task root" (Python 3.13+ `is_file` returns False for NUL).

## Sibling rows (this file only)
Grepped for resolve/lower/upper/drive letters/sep/chmod/symlink/os.: the only OS-touching code was `os_text` (fixed, removed);
lines 18-19 `Path(__file__).resolve()` OS-independent. Rows with "a.txt is not a file" / "escapes the task root" use substring
checks and relative names: OS-independent. Message texts with the task root use `Path(task).resolve()` on both sides: OS-independent. No temp short-name or case-name rows found.

## Witness
`python -B scripts/tests/test_exploratory_findings.py` last line: `=== test_exploratory_findings: 344/344 ok ===`
`python -B scripts/selftest.py --limits --lang` last line: `=== qa-factory selftest: 4/4 ok ===`
Not run: CI, mutations, Linux.

## Fix-the-class notes
Other callers of `contract.evidence_ref_issue` (contract.py:5935-5946) use `.resolve()`/`.is_file()` with no OSError guard and echo the whole path: same class, not touched (out of owns).
