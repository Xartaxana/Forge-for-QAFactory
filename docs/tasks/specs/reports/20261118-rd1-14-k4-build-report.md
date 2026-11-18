# t-1492 — RD1-14d (k4, the conversion): builder report

## Plan items (card section 6, items 1, 2, 4; item 3 moved into k1 per P-7)

- 1 Row `provenance_acceptance`: DONE. `vocabulary: code`, `field: null`, `status: converted`, `debt_ref: ""`; `decides` names the producer, the predicate, each consumer's tokens and the unknown door. `references/gate-registry.json`
- 2 F-1 (a) deletion: DONE. `acceptable_provenance`, `ACCEPTS` and the registry site are gone (`profile_contract.py`, `gate-registry.json`); readers: `driver_stage_build.build_outcome` (point-of-use `from gate_template import acceptable`, `provenance.rehearsal`), `test_execution_request.py` E11 row (inline form, `provenance.run`; the `ValueError` row became "an unknown consumer is False"), `test_runtime_probe_onboarding.py` three functions (`provenance.run`; matched-only -> `environment_preparation.deploy_proof` with a comment; `("matched","person_confirmed")` -> `provenance.identity`), `test_role_commands.py` literal list with a comment naming `provenance.run`.
- 4 Census row: DONE. `judgment-census.json` row `profile_contract.py::acceptable_provenance` removed; the census test names a vanished unit `stale row ... no such check unit` (C1, `test_judgment_census.py:326-329`). The unit carried a blocking raise, so the C3 ceiling `blocking_per_role.conductor` 749 -> 748 (measured, below).
- Pins that move: DONE, `test_gate_registry.py` by symbol: `EXPECTED_DEBT = {}`; `EXPECTED_CONVERTED` +1 with AR-20 comment; `check_not_in("left as debt")`; split counts 28 / 0 / 6; F4 `code` list +1; K-N2.12 positive control on `provenance_word`; F2 live check on the `PROVENANCE_RESULTS` `<module>` item (exists, line 21: no STOP); D13 triple removed, `D13_ITEM_COUNT` 173 -> 166 (measured `GR.analyse` after: 166; the allow pin unchanged); `predicate_cases` `live-record` -> False; the `--json` debt-item key check became "debt == []" (it read `data["debt"][0]`, E-k4.3).
- Test rows: the card's two `test:` lines are covered by the moved pins (`live-record` False; the registry-unreadable row went to k1 with item 3). No new test lines; every edit is in place, so tests not written: none.

## Witness (verbatim; one run after the code edits, then the onboarding file again after its import fix)

```
## gate_registry --check
exit 0
A26 gate registry: no violations
  blind spot: a gate that compares only non-anchor words, ...
grep -c "left as debt" -> 0
## --json: debt [] findings []
## test_execution_request: exit 1, 1 FAIL, === test_execution_request: 727/728 ok ===
   FAIL B-2: the sixth is not named -- 'c5' unexpectedly found in: ... \.claude\worktrees\agent-ade9bd63928efdfc5\ai-packages\qa-fact...
## test_gate_registry: exit 0 === test_gate_registry: 559/559 ok ===
## test_runtime_probe_onboarding (first run: NameError, three imports missing; fixed, re-run): exit 0
=== test_runtime_probe_onboarding: 729/729 ok ===
PASS written-accepts (I-1): not_applicable is accepted, no unknown ever is
PASS K10 rehearsal: the STRICT validator refuses that record (no evidence file): only the rehearsal reader takes it
PASS K13: and it is NEVER taken for matched by a caller that wants a verified build
```

The one FAIL (B-2, an `AK` row about "the sixth container is not named") is an artifact of the worktree path: the path
`agent-ade9bd63928efdfc5` contains the string `c5`, which the row looks for in the message (the message carries the path; positive
check: `grep -o '.\{40\}c5.\{20\}'` on the run output finds the path). Not related to this change; it passes in a path without `c5`. Its row is
not among the DoD's named functions; `n2_k1_probe_runtime_is_the_one_predicate` and `c3_k1_one_producer_names_the_provenance_word` have no FAIL line.

Judgment census (measured read-only, `T.analyse(root, census)` of `test_judgment_census.py`, not the test run): before the ceiling edit
`{'C3': ['blocking_per_role.conductor is 748, below its ceiling 749']}`; after: `{}`. Not run locally: judgment census and role commands files, canon judges.

## Recorded-data control (DOC-DISPATCH witness; never committed)

Script: the k1 report's "Updated control script" (`docs/tasks/specs/reports/t-1361-rd1-14a.md` lines 326-441), extracted verbatim by
`sed -n '326,441p'` to the scratchpad `provenance_vector.py`; the frozen vector is that report's lines 265-274 (171 records, 684 bits per consumer).
`recast` and `new` take the same inline branch in that script (as k1 wrote it). Run: `python -B provenance_vector.py ai-packages/qa-factory <new|recast|bad> <nine consumers>`.

```
new / recast (identical), all nine consumers:
provenance.automation n 684 true 486 sha 1d79f21fcc3fd23d
provenance.rehearsal n 684 true 596 sha e99875bc172e64fa
provenance.fingerprint n 684 true 600 sha bbe713dc387e7f10
provenance.manual n 684 true 486 sha 1d79f21fcc3fd23d
provenance.identity n 684 true 592 sha 3486d67a5e9442aa
provenance.run n 684 true 592 sha d47681b725c88c33
provenance.manual_capture n 684 true 482 sha 554618fee50c364c
baseline_identity.capture n 684 true 376 sha 8092e3a43dbcd52e
environment_preparation.deploy_proof n 684 true 364 sha eada1a419cf92c25
diff --strip-trailing-cr frozen.txt out_new.txt -> "new == frozen"; same for recast -> "recast == frozen"
bad (consumer nope.x), all nine: true 0 sha 5aeb13c43524c909 (differs from every frozen sha; no frozen `true` is 0)
```
Negative control: `bad` is the control; every frozen sha differs. `old` cannot run (the function is gone), as the card says.
Script source: see the k1 report lines 326-441 (the same bytes; attached by reference to the frozen file, not retyped).

## Greps

- E-k4.5, `acceptable_provenance|\bACCEPTS\b` over `scripts/*.py` (control: the same call found the pre-edit hits): no import of a deleted name in a keep or package file. Remaining hits: prose `execution_request.py:2586`, `runtime_probe.py:57` (docstrings naming `acceptable_provenance`; not in owns), `gate_registry.py:42,406` (non-goal); `profile_contract.py:913` (mine, says "deleted"); `test_gate_registry.py:630,763-785` (synthetic source text of scanner tests); quarantined readers (report line, F-r2-2 (a)): `test_profile_contract.py:142,291,292,296,340,385,471,479,500,504,505` and `test_launch_wrappers.py:163,167` (a `mock.patch.object(.., "acceptable_provenance")` that already named nothing after k2).
- Axis 5 prose twins (`execution-lifecycle.md`, `manual-evidence.md`, `environment-preparation.md`, `phases/s5.md`, `s6.md`): zero hits for the old names (control: Grep over `*.md` found two sibling hits, below). Other `.md` hits: `design/factory-rules-debt.md:101` (non-goal, S1b/RD1-23), `CHANGELOG.md:5309` (history).

## Test volume (commit 3fbce261)

The commit hook WARNs `+37 test lines vs +9 product lines` (added-lines count; the product side is mostly deletions: about 40 lines of `acceptable_provenance`/`ACCEPTS` leave). All 37 are pins that move and in-place rewrites of existing readers (card: "pins that move ... are not behaviour lines"); no new behaviour row was written. A `tests-over:` word is the Lead's.

## Needed from integration

- `ai-packages/qa-factory/scripts/runtime_probe.py:57`: `profile_contract.acceptable_provenance(rehearsal=True)` -> `acceptable(provenance_word(rehearsal=True), "provenance.rehearsal")` (docstring, names a deleted function). Also `execution_request.py:2586`: the docstring word `acceptable_provenance` -> `provenance_word`. Neither is in owns.
- `design/factory-rules-debt.md:101` row FR-59 still says "conversion owed ... `acceptable_provenance`" (S1b / RD1-23).
- Quarantined `test_profile_contract.py` and `test_launch_wrappers.py` still name the deleted function and `ACCEPTS` (listed above); never run or edited here.

## Config keys

None.

## Changelog fragment

`ai-packages/qa-factory/changelog.d/rd1-14-k4-provenance-acceptance-converted.md`.

## Decided differently from the plan / divergences

- Census ceiling `blocking_per_role.conductor` 749 -> 748: not named in the card; the census analyse measured it and the test says "lower the ceiling". Item 4's "names it gone" condition holds (C1 stale-row text).
- `decides` text lists tokens by consumer name in words; the `identity` entry is spelled "matched and person_confirmed only".
- F2 live check source test: the `<module>` item's `source` is the bare set (no variable name), so the check reads `startswith("{'matched', 'mismatched'")`.
- A shell edit by `sed -i` was refused by the worktree guard once, so the three imports in `test_runtime_probe_onboarding.py` were added by Edit after a first NameError (lines 787, 1246, 1370 after edit).

## Same-class notes (no edit)

`test_gate_registry.py` K-T1.7 line 630 keeps the name `acceptable_provenance` as the "a call to a different function is not the predicate" sample; harmless synthetic text.

## Fix round (critic t-1501; Lead picks F1-F7)

- Step 0: `git merge origin/main` done (merge commit 28e8c73a; RD1-41 and FG7-93 in; the commit hook printed WARNs only).
- F1 DONE: `driver_stage_build.build_outcome`: when `acceptable` is False and `gate_template.registry_problem()` is non-empty, the line is `line("probe_failed", why=registry_why(problem, "the probe's answer was not judged"))`. Row: `test_runtime_probe_onboarding.py` K10 function (`K10 F1`): the rehearsal record is taken with a readable registry, and with `_registry_and_reason` forced to `(None, "boom")` the line holds "the gate registry cannot be read (boom)" and not "not one I know".
- F2 DONE: docstrings only, `runtime_probe.py:57` and `execution_request.py:2586` now name `acceptable(provenance_word(..), "provenance.rehearsal")`. No code change in those files.
- F3 DONE: the duplicate `provenance.nobody` row removed from `test_execution_request.py`; the import stays.
- F4 DONE: full control source below, with its negative control.
- F5: no amend. The next commit's message carries the `architecture: AR-16 -- correction: ...` line.
- F6 DONE: `test_execution_request.py` B-2 asserts `c5` absent from the names segment only (`six.split("could be the stand (")[1].split("(+1 more)")[0]`); the former path-dependent FAIL is gone in this very worktree (path ends `fc5`).
- F7: no edit (Lead opens a node).
- Pin: `D13_ITEM_COUNT` 166 -> 167. The merge brought it (inference, not bisected: `build_outcome` still counts 5 items, no triple changed; RD1-41 edited `proof_level.py`). The fix round adds no comparison.

### Witness (one run after all edits; the gate-registry file re-run once after the D13 constant)

```
gate_registry.py --check: exit 0, "A26 gate registry: no violations"
=== test_execution_request: 727/727 ok ===
=== test_runtime_probe_onboarding: 730/730 ok ===     (includes "PASS K10 F1: ...")
=== test_gate_registry: 559/559 ok ===                (first run 557/559 on D13 167 vs 166; after the constant: exit 0)
```

### Recorded-data control: full source and negative control (never committed; the scratchpad `provenance_vector.py`, byte-identical to the k1 report's lines 326-441)

Run: `python -B provenance_vector.py ai-packages/qa-factory <new|recast|bad> <the nine consumers>`. `new` and `recast` take the same inline branch (as k1 wrote it). Results (unchanged by this round, taken in the first round): `new` and `recast` equal the frozen vector on all nine consumers (`diff --strip-trailing-cr`), and the negative control `bad` (consumer `nope.x`) prints `true 0 sha 5aeb13c43524c909` for all nine, differing from every frozen sha (the frozen shas are listed in the section above).

```python
# provenance_vector.py -- C3-k recorded-data control; never committed
# usage: python -B provenance_vector.py <package root> old|new|bad|recast <consumer>[,<consumer>...]
# Edits to r2 §2.3 per card §2: `provenance.identity` judged after `provenance.rehearsal` (F-1 (a): rehearsal_probe accepts on
# provenance.rehearsal, then _observed_identity judges provenance.identity); `recast` (k4) = inline acceptable(provenance_word(..), c).
import glob, hashlib, json, sys
PKG, MODE, CONSUMERS = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
sys.path.insert(0, PKG + "/scripts")
import profile_contract as P


def walk(x):
    if isinstance(x, dict):
        if "observed_runtime_identity" in x or ("result" in x and "expected_source_revision" in x):
            yield x
        for v in x.values():
            yield from walk(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk(v)


recs = []
for f in sorted(glob.glob(PKG + "/scripts/tests/fixtures/**/*.json", recursive=True)):
    try:
        recs.extend(walk(json.load(open(f, encoding="utf-8"))))
    except (OSError, ValueError, RecursionError):
        pass
FIXTURES = len(recs)
# Round 2 (critic t-1371 F1): the synthetic matrix r2 §2.4 R1-R15 and its variants join the fixture records, so the vector
# exercises not_applicable (bare, no_changed_file, the variants a local-source consumer reads) and the malformed rows; the
# records are copies of test_execution_request.provenance_shapes (that module is not imported: it makes a temp dir at import)
BASE = {"profile_id": "api", "timestamp": "2026-09-17T12:00:00Z", "environment_id": "qa", "result": "matched",
        "expected_source_revision": "source-1", "observed_runtime_identity": "build-1", "evidence_refs": ["deploy/1"],
        "provenance": {"technical_verification": True, "source_linkage": "exact", "deployed_source_revision": "source-1"}}
IMAGE = "image:sha256:" + "b" * 64


def pc_for(task):
    return {**BASE, "result": "person_confirmed", "observed_runtime_identity": IMAGE, "evidence_refs": ["evidence/pc.json"],
            "provenance": {"technical_verification": False, "identity_kind": "person_confirmed"},
            "person_confirmation": {"words": "yes, it is deployed", "at": "2026-10-02T11:00:00+00:00", "task": task,
                                    "kind": "deployed", "revision": BASE["expected_source_revision"]}}


NA1 = {**BASE, "result": "not_applicable", "observed_runtime_identity": "", "evidence_refs": [], "provenance": {},
       "reason_code": "no_changed_file"}
NA2 = {k: v for k, v in NA1.items() if k != "reason_code"}
PC = pc_for("T-NOT-THIS")   # the story the loop below passes as `t`
SYNTH = [BASE, {**BASE, "observed_without_evidence": True, "evidence_refs": []}, PC, pc_for("OTHER"), NA1, NA2,
         {**NA2, "reason_code": "No_Changed_File"}, {k: v for k, v in NA2.items() if k != "timestamp"},
         {k: v for k, v in NA1.items() if k != "timestamp"}, {**BASE, "result": "MATCHED"}, {**PC, "result": "Person_Confirmed"},
         {**BASE, "provenance": {**BASE["provenance"], "deployed_source_revision": "other-1"}},
         {**PC, "provenance": {**PC["provenance"], "technical_verification": True}},
         {**BASE, "result": "mismatched", "observed_runtime_identity": IMAGE,
          "provenance": {**BASE["provenance"], "deployed_source_revision": "d" * 40}},
         {**BASE, "result": "unknown", "observed_runtime_identity": IMAGE, "evidence_refs": [],
          "provenance": {"technical_verification": False}, "asks_person": "how"},
         None, [], "x", {}]
recs.extend(SYNTH)
REH = {"provenance.rehearsal", "provenance.identity"}
LOCAL = {"provenance.automation", "provenance.manual"}
TASKED = {"provenance.automation", "provenance.manual", "provenance.manual_capture"}


def valid_as(r, words):
    if not isinstance(r, dict):   # every site refuses a non-object before it validates (validate_request, build, manual)
        return False
    c = P.validate_runtime_provenance(r)
    return bool(c["valid"]) and c["result"] in words


def old(c, r, t, l):
    if c in ("provenance.automation", "provenance.manual"):
        return P.acceptable_provenance(r, P.ACCEPTS, task=t) or (l and valid_as(r, {"not_applicable"}))
    if c == "provenance.rehearsal":
        return P.acceptable_provenance(r, P.ACCEPTS, rehearsal=True)
    if c == "provenance.identity":
        return P.acceptable_provenance(r, ("matched", "person_confirmed"), rehearsal=True)
    if c == "provenance.run":
        return P.acceptable_provenance(r, P.ACCEPTS)
    if c == "provenance.fingerprint":
        return P.acceptable_provenance(r, P.ACCEPTS) or valid_as(r, {"not_applicable"})
    if c == "provenance.manual_capture":
        return P.acceptable_provenance(r, P.ACCEPTS, task=t)
    if c == "baseline_identity.capture":
        return valid_as(r, {"matched", "not_applicable"})
    if c == "environment_preparation.deploy_proof":
        return valid_as(r, {"matched"})
    raise SystemExit("unknown consumer " + c)


def kw(c, t, l):
    return {"rehearsal": c in REH, "task": t if c in TASKED else None, "local_source": l if c in LOCAL else False}


def judged(c, r, t, l):
    if MODE == "old":
        return old(c, r, t, l)
    import gate_template as G
    name = "nope.x" if MODE == "bad" else c
    word = P.provenance_word(r, **kw(c, t, l))
    if c == "provenance.identity" and MODE != "bad":
        # F-1 (a): the rehearsal probe takes the record first, then gate A judges its own consumer
        return G.acceptable(word, "provenance.rehearsal") and G.acceptable(word, name)
    return G.acceptable(word, name)   # new, recast and bad: the inline form


def res(x):
    return str(x.get("result")) if isinstance(x, dict) else type(x).__name__


print("records", len(recs), "fixtures", FIXTURES, "synthetic", len(SYNTH),
      sorted((w, sum(1 for x in recs if res(x) == w)) for w in {res(x) for x in recs}))
for c in CONSUMERS:
    bits = "".join("1" if judged(c, r, t, l) else "0" for r in recs for t in (None, "T-NOT-THIS") for l in (False, True))
    print(c, "n", len(bits), "true", bits.count("1"), "sha", hashlib.sha256(bits.encode()).hexdigest()[:16])
```
