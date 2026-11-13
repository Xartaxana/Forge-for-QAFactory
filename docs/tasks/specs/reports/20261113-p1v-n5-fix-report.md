# Node N5 fix report: bugs by root, card 20 class (П1-в)

## What changed (only the two data files)

1. `experiments/mybooks/truth/add-to-cart.yaml`, owner version `v2026-11-05-owner`: new field `bugs_by_root: 6` right after `stated_count`; `root_of` kept.
2. Same file, owner version: cards 11, 13, 20 all `class: not_bug` and `withdrawn_by_owner: true`. Cards 11 and 13 already shared the token `not_bug` before the edit (no fork). Card 20 changed `unknown` -> `not_bug`; its `why` now quotes `SUMMARY.md:70` and `SUMMARY.md:86` («снято владельцем 3 (11, 13, 20)»). The lead (history) version is untouched. Card 24 stays `class: unknown`.
3. `experiments/mybooks/factory-vs-free-agent/judgment.yaml`: QA7 of each arm has 6 sub-rows (bugs 1, 3, 9, 14, 15, 18); the row of the shared root is `{bug: 3, cards: [3, 23], ...}`; the `bug: 23` rows are removed; comment above `test_quality` updated. All still `state: unknown`, `why: 'blind evaluation not run yet'`.

Keys added, for N6 (`scoreboard.py`): truth `bugs_by_root` (version level), `withdrawn_by_owner` (card level); judgment QA7 sub-row `cards` (list, present only on the shared-root row; `bug` is the root id). Class token of withdrawn cards in the owner version is `not_bug`, flagged by `withdrawn_by_owner: true`.

Note: card 20's class change affects the owner-version class counts (not_bug cards now 11, 13, 16, 17, 20, 21, 10 = 7 cards; unknown only 24). Bug count by cards (7) and by roots (6) unchanged.

## Verification

Script (kept outside the repo, not committed): `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\61b75a79-16bf-492f-9cd2-02266607001d\scratchpad\check_n5b.py`

Command: `python -B <script> <truth.yaml> <judgment.yaml>`

Full source:

```python
import sys
import yaml

truth_path, judg_path = sys.argv[1], sys.argv[2]
truth = yaml.safe_load(open(truth_path, encoding="utf-8"))
judg = yaml.safe_load(open(judg_path, encoding="utf-8"))
fail = []

ids_by_version = {}
judged_versions = []
roots_of_judged = set()
judged_ver = None
for v in truth["versions"]:
    ids = [c["id"] for c in v["cards"]]
    ids_by_version[v["id"]] = ids
    bugs = [c for c in v["cards"] if c["class"] == "bug"]
    roots = {c.get("root_of", c["id"]) for c in bugs}
    print(f"version {v['id']}: cards={len(ids)} class=bug cards={len(bugs)} bug roots={len(roots)} "
          f"judged={v['judged']} carrier={'yes' if v.get('carrier') else 'NO'}")
    if len(ids) != 24:
        fail.append(f"{v['id']}: {len(ids)} cards, expected 24")
    if not v.get("carrier"):
        fail.append(f"{v['id']}: no carrier")
    if v["judged"]:
        judged_versions.append(v["id"])
        judged_ver = v
        roots_of_judged = roots
    for c in v["cards"]:
        if c["class"] == "unknown" and not c.get("why"):
            fail.append(f"card {c['id']} unknown without why")
vs = list(ids_by_version.values())
if any(x != vs[0] for x in vs):
    fail.append("card ids differ across versions")
print("judged: true in:", judged_versions)
if len(judged_versions) != 1:
    fail.append("judged:true must be on exactly one version")

print(f"bugs by root (judged version) = {len(roots_of_judged)}; bugs_by_root field = {judged_ver.get('bugs_by_root')}")
if judged_ver.get("bugs_by_root") != len(roots_of_judged) or len(roots_of_judged) != 6:
    fail.append("bugs_by_root field / computed roots / 6 mismatch")

oc = {c["id"]: c for c in judged_ver["cards"]}
cls = {i: oc[i]["class"] for i in (11, 13, 20)}
print("owner-version classes of cards 11, 13, 20:", cls)
if len(set(cls.values())) != 1:
    fail.append("cards 11, 13, 20 do not share one class token")
for i in (11, 13, 20):
    if oc[i].get("withdrawn_by_owner") is not True or not oc[i].get("why"):
        fail.append(f"card {i}: withdrawn_by_owner/why missing")

rows = judg["card_rows"]
for arm in ("X", "Y"):
    ar = [r for r in rows if r["arm"] == arm]
    uns = [r for r in ar if r["unsure"]]
    cards = sorted(r["card"] for r in ar)
    print(f"arm {arm}: judgment rows={len(ar)} unsure rows={len(uns)} distinct cards={len(set(cards))}")
    if cards != sorted(vs[0]):
        fail.append(f"arm {arm}: rows do not cover the truth card ids once each")
tq = judg["test_quality"]
for arm in ("X", "Y"):
    present = [q for q in ("QA7", "QA8", "QA9", "QA10") if q in tq[arm]]
    print(f"arm {arm}: test_quality present={present}")
    if len(present) != 4:
        fail.append(f"arm {arm}: QA7..QA10 incomplete")
    sub = tq[arm]["QA7"]
    print(f"arm {arm}: QA7 sub-rows={len(sub)} vs bugs by root of judged version={len(roots_of_judged)}")
    if len(sub) != len(roots_of_judged) or {s["bug"] for s in sub} != roots_of_judged:
        fail.append(f"arm {arm}: QA7 sub-rows do not match roots of judged version")
    shared = [s for s in sub if s["bug"] == 3]
    if not shared or shared[0].get("cards") != [3, 23]:
        fail.append(f"arm {arm}: root 3 sub-row does not name cards [3, 23]")
    for q in ("QA8", "QA9", "QA10"):
        if tq[arm][q]["state"] != "unknown":
            fail.append(f"{arm} {q} not unknown")
    if any(s["state"] != "unknown" or s["why"] != "blind evaluation not run yet" for s in sub):
        fail.append(f"{arm} QA7 sub-row not unknown")
if "key" not in judg:
    fail.append("no key block")
leak = [r for r in rows if "free" in str(r["arm"]).lower() or "factory" in str(r["arm"]).lower()]
if leak:
    fail.append("arm name leak in rows")
if fail:
    print("FAIL:")
    for f in fail:
        print(" -", f)
    sys.exit(1)
print("OK")
```

Verbatim output:

```
=== POSITIVE ===
version v2026-11-05-lead: cards=24 class=bug cards=9 bug roots=8 judged=False carrier=yes
version v2026-11-05-owner: cards=24 class=bug cards=7 bug roots=6 judged=True carrier=yes
judged: true in: ['v2026-11-05-owner']
bugs by root (judged version) = 6; bugs_by_root field = 6
owner-version classes of cards 11, 13, 20: {11: 'not_bug', 13: 'not_bug', 20: 'not_bug'}
arm X: judgment rows=24 unsure rows=2 distinct cards=24
arm Y: judgment rows=24 unsure rows=6 distinct cards=24
arm X: test_quality present=['QA7', 'QA8', 'QA9', 'QA10']
arm X: QA7 sub-rows=6 vs bugs by root of judged version=6
arm Y: test_quality present=['QA7', 'QA8', 'QA9', 'QA10']
arm Y: QA7 sub-rows=6 vs bugs by root of judged version=6
OK
exit=0
=== NEGATIVE (copy in scratchpad, first QA7 sub-row bug 18 removed) ===
version v2026-11-05-lead: cards=24 class=bug cards=9 bug roots=8 judged=False carrier=yes
version v2026-11-05-owner: cards=24 class=bug cards=7 bug roots=6 judged=True carrier=yes
judged: true in: ['v2026-11-05-owner']
bugs by root (judged version) = 6; bugs_by_root field = 6
owner-version classes of cards 11, 13, 20: {11: 'not_bug', 13: 'not_bug', 20: 'not_bug'}
arm X: judgment rows=24 unsure rows=2 distinct cards=24
arm Y: judgment rows=24 unsure rows=6 distinct cards=24
arm X: test_quality present=['QA7', 'QA8', 'QA9', 'QA10']
arm X: QA7 sub-rows=5 vs bugs by root of judged version=6
arm Y: test_quality present=['QA7', 'QA8', 'QA9', 'QA10']
arm Y: QA7 sub-rows=6 vs bugs by root of judged version=6
FAIL:
 - arm X: QA7 sub-rows do not match roots of judged version
exit=1
```

`git diff --stat`:

```
 experiments/mybooks/factory-vs-free-agent/judgment.yaml |  9 ++++-----
 experiments/mybooks/truth/add-to-cart.yaml              | 10 ++++++----
 2 files changed, 10 insertions(+), 9 deletions(-)
```

Full diff: truth file adds `bugs_by_root: 6`, `withdrawn_by_owner: true` on cards 11, 13, 20, card 20 `class: unknown` -> `not_bug` with the new `why`; judgment file changes the comment, the `bug: 3` rows gain `cards: [3, 23]`, the two `bug: 23` rows are deleted (as printed by `git diff` in the session; reproducible with `git -C <worktree> diff HEAD~1`-style on the fix commit).

## Needed beyond the manifest

none.
