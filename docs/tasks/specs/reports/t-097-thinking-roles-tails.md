# t-097 report: thinking-roles tails and live proofs moved

## Items
1. DONE: `batch-5-hvosty-p2.md` (14 rows, П2) and `batch-6-hvosty-p3.md` (5 rows, П3) created from batch 4's structure; rows moved verbatim; order chains written. Header-only live-proofs table accepted by `piles check` (form of package-ci/2).
2. DONE: batches 1, 2, 4: rows cut, two «Остатки» lines each (batch 1: П2 x4 ids, П3 x1; batch 2: П2 x8, П3 x2; batch 4: П2 x2, П3 x2), «Ход» line added (batch 4: tails only).
3. DONE: «Живые доказательства» status cells transferred in batch 1 (2 rows), 2 (3 rows), 3 (2 rows); batch 3 «Ход» line added.
4. DONE: 10 rows appended to `live-runs/batch-2-live-proofs.md`.
5. DONE: README: table rows 5, 6; «Бриф пачки 5/6»; «Содержание» status cells corrected (also added TR2-16 to the odna-doroga finding row: `в пачке 5, TR2-16`).
6. DONE: board regenerated, DoD run.

Counts: moved rows 14 -> batch 5, 5 -> batch 6; live rows appended 10 (7 thinking-roles + 3 package-ci/2).

## Deviations / findings
- DEVIATION (form): the prescribed `перенос: thinking-roles/5` was refused by `piles check` (д): "`перенос: thinking-roles/5` is none of findings/<file> | пачка N | <slug>/findings/<file>". Used `перенос: пачка 5` / `пачка 6` in all six «Остатки» lines.
- PC2-4, PC2-6, PC2-7 rows describe canon fixes ("Канон красный: ..."), none mentions a live proof; the live-row wordings are my reading of the rows' own content (receipt once per walk and corrupted record does not answer a repeat; brief above 6 KB keeps the gate refusal line and the human-walk part, cut last; own side answer does not switch off default `product`), suffixed per spec, stand `MyBooks`. Package-ci/2 «Живые доказательства» table is header-only, so no live proof exists there: the Lead should confirm these three are wanted.
- Order chains: kept `gate_preflight.py: TR2-9 → TR2-2` although TR2-2's «Пишет в» does not list it (the old batch stated it). TR2-10 is noted as after TR2-5 (batch 5) in batch 6.
- Finding TR2-16 had no README row naming it; added to row 77.
- `board` warns that batch-5/6 are untracked (`git add` needed before commit).
- needed beyond the manifest: `python tools/piles.py` messages only.

## Witness
```
$ python tools/piles.py check --all | tail
(д) form: ok (32 piles, 90 batches)
(е) findings: ok (913 findings read, 0 dated from 2026-10-13 on are orphans, 167 older are the baseline)
piles check: ok
$ python tools/piles.py board --check
piles board: up to date (32 piles, 90 batches, 432 ids)
$ python -m pytest tools/test_pile_cards_contents.py -q
131 passed in 1.61s
$ python -B keys_t097.py
rows b5 14 b6 5
live thinking-roles 7 package-ci/2 3
POSITIVE: OK
FAIL id TR9-99 0
FAIL not in 5 TR9-99
rows b5 14 b6 5
live thinking-roles 7 package-ci/2 3
NEGATIVE (TR9-99 added, must FAIL): FAILED-as-expected
$ git show HEAD:plans/piles/live-runs/batch-2-live-proofs.md | grep -c "перенесён из package-ci/2"
0
```

## Script source (scratchpad `keys_t097.py`, not committed)
```python
import re, sys
R = "C:/QAFactory/forge-repo/plans/piles/"
tr = R + "thinking-roles/"
files = {n: open(tr + f, encoding="utf-8").read() for n, f in {
    1: "batch-1-ruchnoj-prohod.md", 2: "batch-2-proby-drajver-shvy.md", 3: "batch-3-parallelnost.md",
    4: "batch-4-ostatki.md", 5: "batch-5-hvosty-p2.md", 6: "batch-6-hvosty-p3.md"}.items()}
live = open(R + "live-runs/batch-2-live-proofs.md", encoding="utf-8").read()
b5 = "TR1-5 TR1-6 TR1-8 TR1-10 TR2-2 TR2-3 TR2-4 TR2-5 TR2-6 TR2-9 TR2-11 TR2-16 TR4-14 TR4-15".split()
b6 = "TR1-7 TR2-10 TR2-13 TR4-16 TR4-17".split()

def run(b5, b6):
    ok = True
    def starts(i):
        return sum(len(re.findall(r"^\| %s \|" % re.escape(i), t, re.M)) for t in files.values())
    for i in b5 + b6:
        if starts(i) != 1:
            print("FAIL id", i, starts(i)); ok = False
    n5 = len(re.findall(r"^\| TR\d-\d+ \|", files[5], re.M)); n6 = len(re.findall(r"^\| TR\d-\d+ \|", files[6], re.M))
    for i in b5:
        if not re.search(r"^\| %s \|" % re.escape(i), files[5], re.M): print("FAIL not in 5", i); ok = False
    for i in b6:
        if not re.search(r"^\| %s \|" % re.escape(i), files[6], re.M): print("FAIL not in 6", i); ok = False
    print("rows b5", n5, "b6", n6)
    if n5 != 14 or n6 != 5: ok = False
    a = live.count("перенесён из thinking-roles/"); b = live.count("перенесён из package-ci/2")
    print("live thinking-roles", a, "package-ci/2", b)
    if a != 7 or b != 3: ok = False
    return ok

print("POSITIVE:", "OK" if run(b5, b6) else "FAIL")
print("NEGATIVE (TR9-99 added, must FAIL):", "FAILED-as-expected" if not run(b5 + ["TR9-99"], b6) else "NOT DETECTED")
```
