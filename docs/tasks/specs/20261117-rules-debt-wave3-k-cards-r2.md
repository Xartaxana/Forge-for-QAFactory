# Rules-debt wave 3 — cards C3-k1..C3-k4, round 2 (t-1101, node rules-debt/1/RD1-13, F19)

Designer draft for the Lead. It REPLACES §3-§7 of `docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md` for the k cards
and is self-contained: a builder executes a card from this file alone. C3-j is HELD (it waits for the owner's J1/J2) and is
not revised here. Inputs: the plan verdict t-1092 (`docs/tasks/specs/reviews/t-1092-rules-debt-wave3-j-k-plan.md`), the
g-h verdict t-1090 (G2), the g-h round-2 cards `docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards-r2.md` §9 (edits owed to
these cards) and its Lead line G-5 (a) / G-6 (b) / G-8 (a), and the Lead decisions of 17.11.2026 in the brief.

The parent spec `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (S-a..S-f, the E-c table, the decided-branches
table) still applies; where this file states a rule, this file wins.

**Where the facts were read.** The base tree is the C3-b2 / C3-d / C3-reg-precondition / RD1-27 worktree
`C:/QAFactory/forge-repo/.claude/worktrees/agent-ac40b44fb0a175afa/ai-packages/qa-factory/` (it merges before any k builder
starts). Every `file:line` below is a line of that tree unless it says "main". C3-g is NOT on main yet: main's
`references/gate-registry.json:349` still holds `"provenance.baseline"` (grep `provenance\.baseline|baseline_identity\.readiness`,
case-insensitive, over main's package: 6 hits, all `provenance.baseline`; 0 `baseline_identity.readiness`). This dispatch had
no shell: nothing was RUN. Numbers quoted from runs are the plan critic's (t-1092 M1-M7), marked so.

---

## §0. Order, base, parallelism

### §0.1 What k1..k4 owed to C3-j, and how each stands without it

Nothing in k1..k4 depends on C3-j's code or data. The old cards named C3-j only in:
- the queue of `test_gate_registry.py` (`C3-d → C3-j → C3-k1 → …`) and the HOT queue of `gate_preflight.py`
  (`C3-rr → C3-j → C3-k2 → C3-h`);
- E-k4.5 ("deltas from the main k4 is based on, after C3-j");
- the S-f numbers (debt count, split, D13), which were deltas anyway.

Without C3-j: C3-j leaves both queues; every pin stays a DELTA from the base the card is built on (S-f), re-measured, never
copied from this file. If C3-j lands later, it is the later merger: it merges main in, re-derives its own row's pins and
re-measures D13 (D-0048). No k card reads or writes row `s5_stand_limits`.

### §0.2 Queues (the Lead's order: C3-g first)

- `gate-registry.json` / `test_gate_registry.py`: C3-g → C3-k1 → C3-k2 → C3-k3 → C3-k4 → C3-h (C3-h: row `stand_identity`
  pins only; it may also go before k1, row-disjoint, as the later merger).
- `gate_preflight.py` (HOT): C3-k2 → C3-h (C3-h edits no `gate_preflight.py` code under its card; the queue line is kept so
  no two open nodes hold the file).
- `execution_request.py`: (C3-b2, in the base) → C3-k1 (test file only) → C3-k2 → C3-k4.
- `test_execution_request.py`: C3-k1 → C3-k2 → C3-k3 → C3-k4 (the provenance matrix of §2.4 grows per card).
- The `baseline_identity` consumer block: C3-g → C3-k3 (k3's precondition, E-k3.5).

### §0.3 Parallelism (fork F-r2-3 below; the cards are executable on its recommendation)

Recommended: **serial k1 → k2 → k3 → k4**, one builder each. Why not parallel:
- k1 is the producer every later card calls (`provenance_word`, `local_source_request`): nothing can start before it.
- k2 and k3 touch disjoint CODE files, but share: row `provenance_acceptance` (`accepts`, site `allow` lists), the exact
  allow-list pin, the F1 consumer list, the K-T1.2 NEG list, the K-N2.12 callee list and `D13_ITEM_COUNT` in
  `test_gate_registry.py`, and the matrix table in `test_execution_request.py`. Every one of those is ONE statement both
  cards rewrite, so a parallel pair conflicts on each and the later merger re-derives all of them: it saves one slot and
  costs a second measuring round.
- k4 needs k2 and k3 merged (it converts with every literal gone or allowed).
k1 with C3-g in parallel is legal (row-disjoint; only `D13_ITEM_COUNT` and its comment collide), with k1 as the later
merger. One builder for a pair: not recommended (F-k7 was decided: four serial cards; k2 alone already spans five code
files and a HOT file).

---

## §1. Architecture, rules, owners (designer rule 1) — per card

Commit lines: every package commit carries `architecture:` and `judgment:` lines in the form `tools/architecture_gate.py`
accepts; that file is the only carrier of the grammar and it is not copied here. Each card gives the CONTENT.
`judgment: none` always carries its ` -- <why>`.

### §1.1 C3-k1

- FR walk: A — no refusal changes. B — no text a person reads. C — FR-13 (closed variety: the two new words are data rows),
  FR-14 (`provenance_word`'s output is a contract: one of seven words, documented). D — FR-16 (the word is resolved by its one
  producer at the moment it is judged), FR-59 (an unknown never becomes an acceptable word). E/F — not touched. G — FR-30
  (English), FR-32 (tests in a keep file).
- AR-13 kept: one producer of the provenance word (`provenance_word`), one reader of the local-source exemption
  (`local_source_request`). Change check: grep `target_kind.*local_source` over `scripts/*.py` outside tests lists exactly the
  four copies (`coverage_contract.py:824, :845`, `execution_request.py:165`, `manual_evidence.py:80`) plus the new function
  (positive control: `run_suite.py:2513` is a prose hit of the same grep); after k3 only the new function remains.
- AR-15 kept: the four copies get one survivor (wired in k2/k3).
- AR-22 kept: no consumer is added before its reader (k1 adds words, no `accepts` entry).
- AR-28 kept: absent / None / non-dict / malformed record -> `unknown`, pinned by table rows.
- AR-20 kept: D13 re-measured and named with its triple list.
- AR-29: the checks and their owners:

| check | owner | census class | blocking |
|---|---|---|---|
| `provenance_word` (new producer of a data word after the existing validation) | data | no unit: it neither raises nor refuses | no |
| `local_source_request` (new reader of two request fields) | data | no unit | no |

### §1.2 C3-k2

- FR walk: A — FR-1 (refusal sentences unchanged; F-r2-1 (a) adds one note that names the registry). B — FR-6 for the
  F-r2-1 note (plain words, no field path). C — FR-11/FR-14 (`rehearsal_probe`'s parameter changes form, every caller
  changes in this commit). D — FR-59 (every doubt refused). E — FR-41 (F-r2-1: an unjudged identity is said as a registry
  fault, not as "no identity"). F/G — FR-30, FR-32.
- AR-13 kept: every execution-side provenance acceptance reads the word through `provenance_word` and `acceptable`.
- AR-22 kept: `provenance.identity` and `provenance.run` land with their readers in this commit.
- AR-28 kept: absent, malformed, other-case, unaccepted or unreadable-registry provenance is refused, pinned.
- AR-9 / AR-18 (F-r2-1 (a) only): the registry note uses the one sentence builder `gate_template.registry_why`.
- AR-20 kept: D13 re-measured; the allow-list pin moves by the named entries (K-C1).
- AR-29:

| check | owner | census class | blocking |
|---|---|---|---|
| `validate_request` provenance acceptance via `acceptable(provenance_word(…), "provenance.automation")` | data | unchanged: `execution_request.py::validate_request` safety (`judgment-census.json:343`) | yes, as today |
| `rehearsal_probe` / `_observed_identity` / `run_suite.probe_runtime` / `execution_fingerprint.build` acceptance | data | unchanged: `run_suite.py::probe_runtime` xref (:956); the others have no row | yes, as today |
| F-r2-1 (a): the registry note at gate A | data (a reason string) | no unit (a note, not a refusal) | no |

### §1.3 C3-k3

- FR walk: A — FR-1/FR-2 (item 2b: the baseline revision refusal gains what was expected and a door). B — FR-6 for the new
  sentences of item 2b (plain words; field names only where they name what to fix). C — FR-11, FR-14. D — FR-59. E — FR-41.
  G — FR-30, FR-32.
- AR-13 kept: every manual-side provenance acceptance reads the word through `provenance_word` and `acceptable`.
- AR-15 kept: the three remaining local-source copies are replaced by `local_source_request`.
- AR-19 kept: manual capture (`stand_probe`) and manual record (`_provenance_errors`, `validate_manual_current`) keep one rule
  (axis 19, `_provenance_errors` docstring :75-76).
- AR-22 kept: `baseline_identity.capture` and `environment_preparation.deploy_proof` land with their readers; the dead
  `provenance.environment_preparation` leaves in the same commit. C3-g's `baseline_identity.readiness` is not touched.
- AR-28 kept: unaccepted, malformed (item 2b: a non-object block) or unreadable-registry provenance is a named refusal, pinned.
- AR-9 kept (item 2b): the refusal names the expected revision and a door the refused party can use.
- AR-20 kept: D13 re-measured; the allow-list pin moves by the named entries (K-C1).
- AR-29:

| check | owner | census class | blocking |
|---|---|---|---|
| `_provenance_errors`, `validate_manual_current`, `stand_probe` acceptance via the predicate | data | unchanged: `manual_evidence.py::_provenance_errors` shape (:676); the others as today | yes, as today |
| `validate_baseline_record` acceptance via `acceptable(…, "baseline_identity.capture")` | data | unchanged: `manual_evidence.py::validate_baseline_record` shape (:691) | yes, as today |
| item 2b: non-object `baseline_contract` / `runtime_before` / `runtime_after` refused by name | data (shape) | unchanged unit `validate_baseline_record` shape (an appended error, no new raise) | yes (was a crash) |
| `_run_step` deploy proof via `acceptable(…, "environment_preparation.deploy_proof")` | data | no census row (`provenance_ok` is a flag) | as today |

### §1.4 C3-k4

- FR walk: A — FR-1 (the refusal on an unreadable registry names its real cause, F-k5). B — FR-6 (that sentence). C — FR-13
  (the row converts: closed variety in data), FR-14. D — FR-58/FR-59. E — FR-41. F/G — FR-30, FR-32.
- AR-13 kept; AR-15 kept: one provenance predicate path, `provenance_word` then `acceptable`; `acceptable_provenance` is that
  composition. AR-16 / P31: the registry sentence is built by `gate_template.registry_why` (no fifth copy, K4-2).
- AR-19 kept: axis 5 prose twins walked (siblings line).
- AR-28 kept: an unknown or unreadable-registry provenance is refused and says why, pinned by the S-b row.
- AR-20 kept: debt -1, converted +1, F4 +1, D13 re-measured; the census unit of `acceptable_provenance` shrinks if its raise
  goes (named in the verdict).
- AR-29:

| check | owner | census class | blocking |
|---|---|---|---|
| `acceptable_provenance` recast to `acceptable(provenance_word(…), consumer)` | data | `profile_contract.py::acceptable_provenance` shape (:826): the `ValueError` raise (the unit) goes; `test_judgment_census.py` names the shrink; the row leaves `judgment-census.json` only if that test asks | no |
| `refusal_text` registry clause | data (a reason string) | no unit (`refusal_text` is a `library` site and raises nothing) | no |

If `test_judgment_census.py` reads any of these differently, the node stops and returns a question (spec S6 E1 precedent).

---

## §2. Shared facts (read on the base tree)

### §2.1 The accept sites of `provenance_acceptance` and what each card does

Row `provenance_acceptance`: `gate-registry.json:37-93`; `field: result`; words = `profile_contract.PROVENANCE_RESULTS`
(:21); `test: scripts/tests/test_execution_request.py` (:91); `promotable: true` (:87); status debt (B-255).

| site (registry line) | decides today (base tree) | card | after |
|---|---|---|---|
| `execution_request.validate_request` (:41) | `acceptable_provenance(provenance, ACCEPTS, task=…)` :176, or the local NA literal :177; the local test :165; refusal-sentence literals :167 (`checked['result'] == 'not_applicable'`) and :170 (`provenance.get('result') == 'person_confirmed'`) | k2 | accept: `acceptable(provenance_word(…), "provenance.automation")`; :165 -> `local_source_request(data)`; :177's literal gone; :167 and :170 get `allow` |
| `execution_request.rehearsal_probe` (:43) | `acceptable_provenance(value, accepts, rehearsal=True)` :2506, `accepts=ACCEPTS` :2486 | k2 | accept, `consumer="provenance.rehearsal"` default |
| `execution_fingerprint.build` (:44) | `acceptable_provenance(…, ACCEPTS)` or any valid NA :121-122; key literal :134 | k2 | accept `provenance.fingerprint`; :134 gets `allow` |
| `run_suite.probe_runtime` (:52) | `acceptable_provenance(value, ACCEPTS)` :928 | k2 | accept, new `provenance.run` |
| `probe_by_code.probe_runtime` (:50) | delegates to `run_suite.probe_runtime` | k2 | re-role `dispatch` (registry only) |
| `gate_preflight._observed_identity` (:53) | hands `accepts=("matched", "person_confirmed")` :3444 | k2 | re-role `dispatch`; passes `consumer="provenance.identity"` |
| `manual_evidence._provenance_errors` (:45) | :80 local test; :86 NA sentence literal; :89-90 predicate or local NA | k3 | accept `provenance.manual`; :86 gets `allow` |
| `manual_evidence._other_profile_errors` (:46) | calls `_provenance_errors` (:121); :129 skips the binding for an NA probe | k3 | re-role `validate` |
| `manual_evidence.validate_baseline_record` (:47) | :682 pc sentence; :686 valid ∧ result ∈ {matched, NA} | k3 | accept `baseline_identity.capture`; :682 gets `allow`; :686 gone |
| `coverage_contract.validate_manual_current` (:48) | :824 local test; :831-832 predicate or local NA; :839 binding skip (`!=`); :845 second NA refusal with an inline local copy | k3 | accept `provenance.manual`; :839 and :845 get `allow` |
| `manual_capture.stand_probe` (:51) | `acceptable_provenance(value, ACCEPTS, task=story)` :1612 | k3 | accept `provenance.manual_capture` (tokens tightened, F-k2 (a)) |
| `environment_preparation._run_step` (:49) | :388 `checked["valid"] and checked["result"] == "matched"` + two equalities | k3 | accept `environment_preparation.deploy_proof` |
| `profile_contract.acceptable_provenance` (:54) | token logic :908-923 | k4 | the composition (F-k3 (a)) |

Outside the row: `driver_stage_build.build_outcome` (:379-382) calls `acceptable_provenance(record, ACCEPTS, rehearsal=True)`;
it is a `dispatch` site of `stand_identity` and moves in k4 (a reader of the changed name).

Plan critic M2 (run on both trees): turning the row converted today gives F-b on all 13 accept sites and F-a on exactly the
literals of the table above; no provenance accept site is registered under a second row.

### §2.2 Why the sites call `acceptable` themselves (A26)

Once the row is `converted`, every `accept` site must call a function named exactly `acceptable` (`gate_registry.py`
F-b, pin K-T1.7), and every row word compared in an accept site must equal an `allow` entry (`_allowed`,
`gate_registry.py:772-783`: an entry is the WHOLE comparison, quote-normalised; a non-accept role or a non-converted row is
always allowed). One `allow` entry covers every comparison with that exact text in its site (`gate_registry.py:81-82`).
`gate_template.acceptable` (base :71-107) takes the word from `value[row["field"]]`, validates nothing and never raises; so
`validate_runtime_provenance`, `person_confirmed(record, task)` and `no_changed_file(record)` stay where they are, and the word
given to `acceptable` is computed after them by `provenance_word` (F-k1 (a), decided).

### §2.3 The recorded-data control (K1-2 (ii), K3-3, K4-1): the frozen vector

Plan critic M3: the 25 `evidence/runtime-provenance-*.json` are all `person_confirmed`; a walk of every fixture JSON for
provenance-shaped dicts found 133 records (79 matched, 53 person_confirmed, 1 invalid, 0 not_applicable). The control walks
all of them over every consumer.

The script below is the control. It is never committed: the builder saves it in its own scratchpad and attaches its full
source and output to the report (CLAUDE.md rule 11, DOC-DISPATCH witness form). `OLD` encodes TODAY's site predicates as
code (§B of the verdict, the left column); `NEW` is the composition.

```python
# provenance_vector.py -- C3-k recorded-data control; never committed
# usage: python -B provenance_vector.py <package root> old|new|bad|recast <consumer>[,<consumer>...]
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
REH = {"provenance.rehearsal", "provenance.identity"}
LOCAL = {"provenance.automation", "provenance.manual"}
TASKED = {"provenance.automation", "provenance.manual", "provenance.manual_capture"}


def valid_as(r, words):
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
    if MODE == "recast":
        return P.acceptable_provenance(r, c, **kw(c, t, l))
    import gate_template as G
    return G.acceptable(P.provenance_word(r, **kw(c, t, l)), "nope.x" if MODE == "bad" else c)


print("records", len(recs), sorted((str(r.get("result")), sum(1 for x in recs if x.get("result") == r.get("result")))
                                   for r in {str(x.get("result")): x for x in recs}.values()))
for c in CONSUMERS:
    bits = "".join("1" if judged(c, r, t, l) else "0" for r in recs for t in (None, "T-NOT-THIS") for l in (False, True))
    print(c, "n", len(bits), "true", bits.count("1"), "sha", hashlib.sha256(bits.encode()).hexdigest()[:16])
```

Freeze and compare:
- **k1 freezes** (before its own code, the old function is untouched until k4): `old` over all nine consumers. The nine lines
  are the FROZEN VECTOR; they go verbatim into the k1 report, and the Lead quotes them into the k2, k3 and k4 dispatches.
- Each card prints `new` for the consumers that exist in the registry at that card and compares line by line to the frozen
  vector (equal `true` and `sha`): k1 `provenance.automation,provenance.rehearsal,provenance.fingerprint,provenance.manual`;
  k2 adds `provenance.identity,provenance.run`; k3 adds `provenance.manual_capture,baseline_identity.capture,environment_preparation.deploy_proof`;
  k4 prints `new` AND `recast` for all nine.
- k2 and k3 also re-print `old` for all nine (the old function is unchanged): it must equal the frozen vector (proves the
  freeze is stable); k4 cannot (the old function is gone) — that is why the vector is frozen.
- Negative control, every card: `bad` for the same consumers. For every consumer whose frozen `true` > 0 the `sha` must
  differ from the frozen one. With 79 matched and 53 pc records, every consumer has `true` > 0 (an expectation; the run decides).
  A consumer with `true` 0 in the frozen vector is named in the report as "control void for <c>", and the synthetic matrix
  of §2.4 is its evidence.
- The record count is reported as measured; a count other than 133 is not a stop (fixtures may have grown since M3), but it is
  named, and k2..k4 must print the same count as k1 unless a fixture changed in between (then the freeze is re-taken and named).

### §2.4 The synthetic matrix (K1-2 (i)) — committed rows

One parameterised table in `scripts/tests/test_execution_request.py` (the row's own `test` file, keep `gate_named`), grown per
card. Records, built from the file's existing provenance shapes (`shapes`, near :597; the builder greps `shapes\[`):

| id | record |
|---|---|
| R1 | valid matched with an evidence file |
| R2 | matched, `observed_without_evidence: true`, `evidence_refs: []` |
| R3 | valid person_confirmed for story `T` |
| R4 | valid person_confirmed for another story |
| R5 | valid not_applicable, `reason_code: no_changed_file` |
| R6 | valid not_applicable, no `reason_code` |
| R7 | valid not_applicable, `reason_code: No_Changed_File` |
| R8 | not_applicable with `timestamp` missing (invalid) |
| R9 | R1 with `result: MATCHED` |
| R10 | R3 with `result: Person_Confirmed` |
| R11 | matched whose `provenance.deployed_source_revision` differs from `expected_source_revision` (effective mismatched) |
| R12 | person_confirmed with `technical_verification: true` |
| R13 | valid declared mismatched |
| R14 | valid declared unknown |
| R15 | `None`, `[]`, `"x"` (three sub-rows) |

k1's half — the word (`provenance_word(r, task="T")`, `local_source=False`, `rehearsal=False` unless named):
R1 matched; R2 unknown, and R2 with `rehearsal=True` matched; R3 person_confirmed; R4 unknown; R5 no_changed_file, and R5 with
`local_source=True` no_changed_file (precedence); R6 not_applicable, and R6 with `local_source=True` local_source; R7
not_applicable; R8 unknown, and R8 with `local_source=True` unknown; R9 unknown; R10 unknown; R11 mismatched; R12 unknown;
R13 mismatched; R14 unknown; R15 unknown each.

The consumer columns (expected booleans; each consumer is called with the `kw` of §2.3: rehearsal for rehearsal/identity,
task `T` for automation/manual/manual_capture, `local_source` per sub-row for automation/manual only):

| record | automation | rehearsal | fingerprint | manual | identity (k2) | run (k2) | manual_capture (k3) | baseline_identity.capture (k3) | environment_preparation.deploy_proof (k3) |
|---|---|---|---|---|---|---|---|---|---|
| R1 | T | T | T | T | T | T | T | T | T |
| R2 | F | T | F | F | T | F | F | F | F |
| R3 | T | T | T | T | T | T | T | F | F |
| R4 | F | T | T | F | T | T | F | F | F |
| R5 | T | T | T | T | F | T | T | T | F |
| R6 (local F) | F | F | T | F | F | F | F | T | F |
| R6 (local T) | T | F | T | T | F | F | F | T | F |
| R7 | F | F | T | F | F | F | F | T | F |
| R8 (local F and T) | F | F | F | F | F | F | F | F | F |
| R9-R15 | F | F | F | F | F | F | F | F | F |

Expected from: the consumers' tokens written in §3-§5 and the docstrings of `validate_runtime_provenance`,
`person_confirmed`, `no_changed_file` (R4 is T for rehearsal/identity/fingerprint/run because those sites pass no task,
today and after) — never from the new function's output. Each card adds only the columns of consumers that exist at it
(k1: the first four).

### §2.5 The exact allow-list pin (K-C1)

`test_gate_registry.py:305-312` asserts the EXACT list `[e["compare"] for r in rows for s in r["sites"] for e in s.get("allow", [])]`,
i.e. registry order: rows, then sites, then entries. Base list: the seed entry of `validate_request`, then four entries of
`test_identity` sites. The row order puts `provenance_acceptance` (row 2) before `test_identity`, and its site order is
`validate_request`, `rehearsal_probe`, `build`, `_provenance_errors`, `_other_profile_errors`, `validate_baseline_record`,
`validate_manual_current`, … So:
- after k2: seed, `checked['result'] == 'not_applicable'`, `provenance.get('result') == 'person_confirmed'`,
  `runtime.get('result') == 'person_confirmed'`, then the base's later entries unchanged;
- after k3: the k2 list with, right after `runtime.get('result') == 'person_confirmed'`:
  `probe.get('result') == 'not_applicable'` (`_provenance_errors`), `checked['result'] == 'person_confirmed'`
  (`validate_baseline_record`), `probe.get('result') != 'not_applicable'` and `probe.get('result') == 'not_applicable'`
  (`validate_manual_current`, in that order), then the base's later entries unchanged.
Any allow entry another merged card put on the base keeps its position; the list is re-derived from the merged registry
and every new entry's text is the one written here. The pin's label names the new entries' kind ("… and the non-acceptance
comparisons of the provenance sites (C3-k2, C3-k3) …").

---

## §3. Card C3-k1 — the provenance word and the local-source test (foundation)

task: given by the Lead
given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole)
- `C:/QAFactory/forge-repo/plans/builder-rules.md`
- `C:/QAFactory/forge-repo/docs/TESTING.md`
- this file §0-§3
- read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`: `scripts/profile_contract.py:15-30,700-925`, `scripts/gate_template.py` (whole), `scripts/gate_registry.py:20-90,467-560,772-784`, `references/gate-registry.json:37-93`, `scripts/tests/test_execution_request.py` (grep `shapes\[|acceptable_provenance|_READ`), `scripts/tests/test_gate_registry.py:1060-1100,1150-1180`
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/profile_contract.py` (new `provenance_word`, new `local_source_request`; nothing else)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `provenance_acceptance`: `words` +2, `verdict_map` +2, `sites` +2)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py` (one new parameterised table, §2.4, k1 half)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (D13 set and count; three live rows of the C3-0 table :1157-1162)
non-goals: every accept site (k2, k3); `acceptable_provenance` and `ACCEPTS` (k4); `accepts` (no new consumer: none has a reader yet, AR-22); status, vocabulary and field of the row (k4); `gate_template.py`; `judgment-census.json`; `scripts/tests/test_profile_contract.py` (QUARANTINED, `test-layers.json:9186`: never edited, TESTING.md «Карантин»); any new test file
handoff: report path given by the Lead
edges: E-k1.1-E-k1.7 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0 with the debt block unchanged; the §2.3 control: `old` for all nine consumers (the frozen vector), `new` and `bad` for the four k1 consumers, `new` equal to the frozen lines and `bad` different (verbatim output and the script source in the report); then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/profile_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files; `test_execution_request.py` and `test_gate_registry.py` are slow: the batch canon judges them, named in the report (`red-before: not run -- <file> судит канон`)
siblings: axis 5 (the row's words grow; prose twins walked in k4 when `decides` changes); the four local-source copies (`execution_request.py:165`, `manual_evidence.py:80`, `coverage_contract.py:824, :845`) get one survivor here, wired in k2/k3 (AR-15)
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-k-cards-r2.md` (C3-k1)

Items:
1. **`provenance_word(record, *, rehearsal=False, task=None, local_source=False) -> str`** in `profile_contract.py`, placed
   after `acceptable_provenance`; never raises. In this order (K1-1 applied):
   - a non-dict -> `"unknown"`;
   - `checked = validate_runtime_provenance(rehearsal_view(record) if rehearsal else record)`;
   - `checked["result"] == "mismatched"` -> `"mismatched"` (whatever the declared word and validity: the honest word does
     not depend on validity; no consumer takes it);
   - not `checked["valid"]`, or `checked["result"] != record.get("result")` -> `"unknown"`;
   - declared `matched` -> `"matched"`;
   - declared `person_confirmed` -> `"person_confirmed"` if `person_confirmed(record, task)` else `"unknown"`;
   - declared `not_applicable` -> `"no_changed_file"` if `no_changed_file(record)`, else `"local_source"` if `local_source`,
     else `"not_applicable"`;
   - anything else (declared `unknown`) -> `"unknown"`.

   Docstring: the seven words; the error direction (toward a word no consumer takes); that it is the ONE producer of every
   provenance consumer's word; that `person_confirmed` and `no_changed_file` read the raw record (as `acceptable_provenance`
   does today, :914-922).
2. **`local_source_request(record) -> bool`** = `isinstance(record, dict) and record.get("runtime_required") is False and
   record.get("target_kind") == "local_source"`; docstring: a property of the REQUEST (or record) that carries the probe, never
   of the probe; the one copy of the test four sites spell today.
3. **Registry row `provenance_acceptance`.**
   - `words` += `"no_changed_file"`, `"local_source"`;
   - `verdict_map` += `"no_changed_file": {"class": "not_applicable", "reason_code": "no_changed_file"}`,
     `"local_source": {"class": "not_applicable", "reason_code": "local_source"}`;
   - `sites` += `{"file": "profile_contract.py", "function": "provenance_word", "role": "produce"}` and
     `{"file": "profile_contract.py", "function": "local_source_request", "role": "validate"}`.
4. **Tests.**
   - `test_execution_request.py`: one new parameterised method holding the §2.4 table, k1 half: the word rows and the four
     k1 consumer columns, on the live registry (`gate_template.acceptable`, no registry argument).
   - `test_gate_registry.py` C3-0 table (:1157-1162) gains three live rows: `("live-ncf", "no_changed_file",
     "provenance.rehearsal", None, True)`, `("live-local", "local_source", "provenance.automation", None, True)`,
     `("live-local-not-rehearsal", "local_source", "provenance.rehearsal", None, False)`.
   - Expected from: the docstrings named in item 1, the tokens of `gate-registry.json:81-85`, FR-59.
5. **D13 (S-f).** Re-measure `GR.analyse(PLUGIN_ROOT)` before and after (`len(items)` and the triple set). Expected new
   triples: `("profile_contract.py", "provenance_word", "provenance_acceptance")` and `("profile_contract.py",
   "local_source_request", "provenance_acceptance")`. Plan critic M2 measured the words alone at +5 items (`coverage_contract.py:824`,
   `:845`, `execution_request.py:165`, `manual_evidence.py:80`, `profile_contract.py:718`); the new functions add their own.
   `D13_ITEM_COUNT` is the measurement, written in the S-f comment form with the list. A different set of NEW triples is a stop
   and a question.

architecture content: `AR-13 -- one producer of the provenance word, one reader of the local-source exemption`; `AR-15 -- four copies of the local-source test get one survivor (wired in k2/k3)`; `AR-22 -- no consumer added before its reader`; `AR-28 -- an absent or malformed record yields unknown, pinned`; `AR-20 -- D13 +2 triples, count re-measured and named`; `AR-29 -- two data functions, no census unit`. judgment content: `none -- a producer of a data word after the existing validation; no check moves into judgment`.

Edges (each with its INVARIANT):
- E-k1.1 (None / list / str / empty dict): `unknown`. INVARIANT: an absent record never yields an acceptable word.
- E-k1.2 (case): `MATCHED`, `Person_Confirmed`, `No_Changed_File` -> not the exact word. INVARIANT: only the exact word counts
  (C3-0 E3).
- E-k1.3 POSITIONAL: validity is decided BEFORE any NA reason or `local_source` is read; `mismatched` is read first only
  because no consumer takes it. INVARIANT: an invalid record never yields `matched`, `person_confirmed`, `no_changed_file` or
  `local_source`.
- E-k1.4 (conflicting pair: `no_changed_file` and `local_source` both true): `no_changed_file` wins. INVARIANT: no consumer
  takes `local_source` without also taking `not_applicable:no_changed_file` (verdict §B), so the precedence changes no decision.
- E-k1.5 TEMPORAL: after k1 no site reads the new functions. The two new words make the four `== 'local_source'`
  comparisons and `== NO_CHANGED_FILE` counted items of debt accept sites (allowed while the row is debt, M2: 0 findings).
  INVARIANT: `--check` stays green at every step.
- E-k1.6 (limit): none introduced.
- E-k1.7 (one road, P31): one producer for every provenance consumer; it reads no language, project or case name.

Error direction of the reused functions (`validate_runtime_provenance`, `person_confirmed`, `no_changed_file`, now feeding a
gate word): toward refusal only. The adversarial inputs R2 (outside rehearsal), R4, R7-R15 of §2.4 must stay on the safe side
(no acceptable word); they are rows of the table.

---

## §4. Card C3-k2 — the execution side through the predicate

task: given by the Lead
given:
- as k1 (factory-rules whole, builder-rules, TESTING.md, this file §0-§2 and §4), plus the merged k1 diff and the FROZEN VECTOR lines of the k1 report (quoted by the Lead)
- read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`: `scripts/execution_request.py:14-25,120-181,2486-2508`, `scripts/execution_fingerprint.py:25-35,104-140`, `scripts/run_suite.py:119-125,916-930`, `scripts/gate_preflight.py:85-90,3421-3447,3510-3515,3825-3870`, `scripts/gate_template.py:46-68`, `scripts/onboarding_probe.py:325-340`, `scripts/tests/test_execution_request.py:14-18,590-690,1330-1336,1610-1625`, `scripts/tests/test_gate_preflight.py:4256-4335`, `scripts/tests/test_gate_registry.py:259-330,643-668,960-1000,1060-1100`
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py` (`validate_request`: the runtime block :155-180; `rehearsal_probe`: signature, body and docstring; the `profile_contract` import line :17-19)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_fingerprint.py` (`build`: the provenance condition :113-126; the import line :30)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_suite.py` (`probe_runtime` and its docstring; the import line :124)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py` (`_observed_identity`; the import line :87; on F-r2-1 (a) also `_reporter_outcome` around the call :3855) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `provenance_acceptance`: two consumers, three allow entries, two re-roles)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py` (the import :17; K-N2.5 :1334-1335; rows of the provenance table; the §2.4 identity and run columns)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py` (the stub :4261 and its check; one row of the K30 table :4306+; on F-r2-1 (a) one note row)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (K-N2.12 callee rows :277-288 of its sites; the K-T1.2 NEG list :321-322; the allow-list pin :305-312; one new K2-2 row; F1 consumer list :654-657; D13)
non-goals: `_match`, `green_over_same_bytes`, `registry_why` (C3-b2 / RD1-27); `probe_by_code.py` code (registry re-role only); `onboarding_probe.py` (its `_observed_identity` override keeps its signature: F-r2-1 (a) changes no signature); the manual sites (k3); `acceptable_provenance` / `ACCEPTS` definitions (k4); row status, vocabulary, field (k4); `scripts/tests/test_launch_wrappers.py` (QUARANTINED, `test-layers.json:8731`; fork F-r2-2); any new test file
handoff: report path given by the Lead
edges: E-k2.1-E-k2.10 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; the §2.3 control: `old` (nine, equal to the frozen vector), `new` and `bad` for automation, rehearsal, fingerprint, manual, identity, run (new equal to the frozen lines, bad different), verbatim with the script source; then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_fingerprint.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_suite.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files; `test_execution_request.py`, `test_gate_preflight.py`, `test_gate_registry.py` are slow: canon, named
siblings: the class "a mock or pin bound to the renamed predicate" walked: `mock.patch.object(…, "acceptable_provenance")` only in `test_launch_wrappers.py:163, :167` (quarantined, F-r2-2), the `__defaults__` pin K-N2.5, the K-N2.12 callee list; `driver_stage_build.build_outcome:381` (k4); axis 5 prose twins in k4
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-k-cards-r2.md` (C3-k2)

Items:
1. **`validate_request`** (base :155-180).
   - `local_source = local_source_request(data)` replaces :165.
   - :167-169 and :170-173 stay as they are, BEFORE the predicate.
   - :176-177 become `word = provenance_word(provenance, task=data.get("task"), local_source=local_source)`,
     `taken = acceptable(word, "provenance.automation")`, and `if not (taken or said_local):` with the same refusal sentence
     (:178-180).
   - Registry `allow` entries on the `validate_request` site, appended after the seed entry in this order:
     `{"compare": "checked['result'] == 'not_applicable'", "why": "picks the refusal sentence for a not_applicable no exemption covers; the acceptance is the acceptable() call"}`,
     `{"compare": "provenance.get('result') == 'person_confirmed'", "why": "refuses a person's word on a request that skips the probe; it never lets a record through"}`.
   - Expected from: the comments :159-164, :171-175 and the tokens of `provenance.automation` (:81).
2. **`rehearsal_probe(spec: dict, consumer: str = "provenance.rehearsal") -> dict`**: `if acceptable(provenance_word(value,
   rehearsal=True), consumer): return value`; else `raise ProvenanceRefused(value)` as today. The docstring's "ONE set"
   paragraph (:2500-2502) now names the consumer and its tokens' home (the registry row).
   - `gate_preflight._observed_identity` passes `consumer="provenance.identity"` in place of `accepts=(…)` (:3444).
   - Registry: new consumer `"provenance.identity": ["matched", "person_confirmed"]`; site `_observed_identity` re-roled
     `dispatch` (it hands the consumer to the reader that accepts; no literal is left). E-c row: "hands its consumer id to
     the one rehearsal reader; it accepts nothing itself".
3. **`run_suite.probe_runtime`**: `if acceptable(provenance_word(value), "provenance.run"): return value`; docstring :917-925
   names the consumer in place of `acceptable_provenance(record, ACCEPTS)`. Registry: new consumer `"provenance.run":
   ["matched", "person_confirmed", "not_applicable:no_changed_file"]` (today's `ACCEPTS`, `profile_contract.py:877`).
   `probe_by_code.probe_runtime` re-roled `dispatch` (a pure delegate; E-c row: "delegates to run_suite.probe_runtime, which
   accepts").
4. **`execution_fingerprint.build`**: `if not acceptable(provenance_word(spec["runtime_provenance"]), "provenance.fingerprint"):`
   replaces :121-122; the `checked` local (:115) is removed if nothing else reads it. Registry `allow` on the `build` site:
   `{"compare": "runtime.get('result') == 'person_confirmed'", "why": "keys the fingerprint of a run that stands on a person's word; not an acceptance"}`.
   F-k2 (a): the bare `not_applicable` token stays (`provenance.fingerprint`, :82).
5. **Imports (K2-4).**
   - `execution_request.py`: `acceptable` is already imported at the top (:24). The `profile_contract` import (:17-19) gains
     `local_source_request, provenance_word` and drops `ACCEPTS` and `acceptable_provenance` (no reader left in the module
     after items 1-2; the docstring mention :2584 is prose and stays).
   - `run_suite.py`: top-level `from gate_template import acceptable` (no new load cost: `run_suite` already imports
     `execution_request` at the top, which imports `gate_template`); :124 becomes `from profile_contract import provenance_word`.
   - `execution_fingerprint.py`: `from gate_template import acceptable` at the point of use inside `build` (the module is
     also a standalone CLI; the lazy rule of C3-g item 2); :30 gains `provenance_word` and drops `ACCEPTS`,
     `acceptable_provenance` and any name left unused.
   - `gate_preflight.py`: :87 already imports `acceptable`; on F-r2-1 (a) it gains `registry_problem, registry_why`.
   - No name may be left imported and unused: `tools/lint-baseline.json` is a ratchet (`UnusedImport` rows, keyed by path).
6. **F-r2-1 (a) — the gate A world of an unreadable registry (K2-3).** In `_reporter_outcome` (:3825), right after
   `identity = self._observed_identity(profile_id, root)` (:3855): `if not identity and (problem := registry_problem()):
   self._note_once(check, registry_why(problem, "the stand's build is not recorded with this rehearsal"))`, using the `check`
   the function already passes to `_keep_unread`. `_observed_identity` keeps its signature (the `onboarding_probe.py:331`
   override is untouched). On F-r2-1 (b) this item is void and E-k2.2 alone states the world.
7. **Tests.**
   - `test_execution_request.py`: the import :17 (`ACCEPTS as ACCEPTS_OF_THE_PACKAGE`) is removed; K-N2.5 (:1334-1335) becomes
     `er.rehearsal_probe.__defaults__[0] == "provenance.rehearsal"`, label "K-N2.5: `rehearsal_probe`'s default consumer is
     provenance.rehearsal (its tokens live in the registry row)". Rows in the existing provenance table (:590-690): a
     local-source request with a valid bare NA -> admitted; the same with an invalid NA -> refused; `Person_Confirmed` ->
     refused; the unreadable registry (the `GT._READ` seam, saved and restored in `finally`, precedent :1616-1623) with a
     valid matched -> refused. The §2.4 table gains the identity and run columns.
   - `test_gate_preflight.py:4261`: the stub becomes `lambda spec, consumer=None: seen.append((spec, consumer)) or {…}`;
     the check at :4271-4272 reads `seen[0][0]` and adds `seen[0][1] == "provenance.identity"`. The K30 table
     (:4306+) gains one row: `result: unknown` -> identity `""`. On F-r2-1 (a): one row in the same test with the registry
     unreadable (the `_READ` seam) -> identity `""` and the gate's notes hold "the gate registry cannot be read (".
   - Expected from: items 1-6, FR-59, FR-41.
8. **Pins (`test_gate_registry.py`).**
   - K-N2.12 (:277-288): the callee of `run_suite.probe_runtime`, `execution_request.rehearsal_probe`,
     `execution_request.validate_request` and `execution_fingerprint.build` becomes `acceptable`.
   - K-T1.2 NEG list (:321-322) loses `("gate_preflight.py", "_observed_identity")` (its anchor tuple is gone).
   - The allow-list pin (:305-312): the k2 list of §2.5, whole texts.
   - K2-2, a new row beside the g7 block: `len([i for i in result["items"] if i["file"] == "execution_request.py" and
     i["function"] == "validate_request" and GR.norm(i["source"]) == GR.norm("checked['result'] == 'not_applicable'")]) == 1`,
     label "K2-2: one allow entry covers exactly one comparison in validate_request (no acceptance literal hides under it)".
     If `norm` is not the module's public name for the normaliser `_allowed` uses (:773), use that function's name; if none
     is reachable, stop with a question.
   - F1 (:654-657): the `provenance_acceptance` consumer list gains `provenance.identity`, `provenance.run` (sorted; the label's
     count word re-derived).
   - D13 re-measured. Expected: the `_observed_identity` triple leaves (:983); `validate_request` loses :165 and :177;
     `execution_fingerprint.build` loses :122; `run_suite.probe_runtime` and `rehearsal_probe` hold no comparison. Named.

architecture content: `AR-13 -- every execution-side provenance acceptance reads the word through provenance_word and the predicate`; `AR-22 -- provenance.identity and provenance.run land with their readers`; `AR-28 -- an absent, malformed, other-case, unaccepted or unreadable-registry provenance is refused, pinned`; `AR-9 -- on F-r2-1 (a) the unjudged identity is said through registry_why`; `AR-29 -- each site's census unit and class unchanged`; `AR-20 -- allow-list pin +3 named entries, D13 re-measured and named`. judgment content: `none -- a membership join of a validated data word; the validation is unchanged`.

Edges:
- E-k2.1 POSITIONAL (`validate_request`): :167 and :170 stay BEFORE the predicate, and `said_local` still suppresses the second
  sentence. INVARIANT: one sentence per refused record, the same sentence as today.
- E-k2.2 (unreadable registry, from this card on) — the worlds:
  - stage dispatch: C3-reg-precondition stops it first (`controller.py` dispatch branch);
  - inside a run: every provenance read of these sites refuses (a run, a rehearsal, a fingerprint), with today's sentence and
    `refusal_text`, a false cause until k4's F-k5;
  - gate A (K2-3, read on the base): `_observed_identity` swallows the `ProvenanceRefused` into `""` (:3446-3447); its one
    caller `_reporter_outcome` (:3855) only records it as `runtime_identity: null` in the rehearsal row, "no longer keys a
    proof" (:3854, :3537). No person-visible text says "unobserved"; the row's null is "not known". On F-r2-1 (a) a note names
    the registry.
  INVARIANT: a broken registry never admits a probe, and the gate never states an unjudged identity as a fact.
- E-k2.3 TEMPORAL: the row is still `debt`; the literals left are allowed; the allow entries are written now and inert until
  k4 (`_allowed` :775-776). INVARIANT: `--check` green at every step, and every allow entry matches a comparison (F-d).
- E-k2.4 (allow masking, K2-2): `validate_request`'s :167 and :177 printed the same text; :177 leaves in this card, so the one
  allow entry covers exactly one comparison, pinned. INVARIANT: an allow entry never covers an acceptance literal.
- E-k2.5 (consumer typo): `acceptable` is False, the probe is refused, and A26 `--check` plus the T rows of §2.4 turn red.
  INVARIANT: no false accept.
- E-k2.6 (one producer per consumer, C3-b2 E11): every provenance consumer is fed only by `provenance_word`.
- E-k2.7 (HOT): queues of §0.2. INVARIANT: no two open nodes edit `gate_preflight.py` at once.
- E-k2.8 TEMPORAL (recorded records): the §2.3 control. INVARIANT: no recorded run changes meaning.
- E-k2.9 (quarantined reader, F-r2-2): `test_launch_wrappers.py:163, :167` patches `acceptable_provenance` on RS/ER; after this
  card the names are gone (AttributeError in the quarantine-watch job). On F-r2-2 (a) the report carries one line: "expected
  quarantine-watch red: test_launch_wrappers.py other_places_use_the_one_launcher, cause the renamed predicate (C3-k2), not a
  product defect". INVARIANT: no keep or canon file is left red by a rename.
- E-k2.10 (limit): none.

---

## §5. Card C3-k3 — the manual side, the baseline capture, the deploy proof

task: given by the Lead
given:
- as k1, plus the merged k1 and k2 diffs, the merged C3-g diff (required: k3 is based after C3-g), the FROZEN VECTOR lines, this file §5
- `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards-r2.md` §9 (the edits owed to this card, built in below)
- read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`: `scripts/manual_evidence.py:15-23,74-133,658-700`, `scripts/coverage_contract.py:812-850`, `scripts/manual_capture.py:95-101,1596-1615`, `scripts/environment_preparation.py:20-24,378-398`, `scripts/gate_registry.py:724-743`, `references/gate-registry.json` (rows `provenance_acceptance`, `baseline_identity`, `environment_preparation`), `scripts/tests/test_gate_registry.py:259-330,643-668`, `scripts/tests/test_manual_evidence.py` (grep `validate_baseline_record|validate_manual_current|local_source|baseline_person`), `scripts/tests/test_manual_capture.py` (grep `stand_probe`), `scripts/tests/test_environment_preparation.py` (grep `provenance_validation`)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_evidence.py` (`_provenance_errors`; `validate_baseline_record`; the import line :17-18)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/coverage_contract.py` (`validate_manual_current`: the runtime block :818-849)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_capture.py` (`stand_probe` :1612-1613; the import line :99-100)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/environment_preparation.py` (`_run_step`: :383-394 and its point-of-use import)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `provenance_acceptance`: two consumers, four allow entries, one re-role, the `provenance.manual_capture` tokens; row `environment_preparation`: `accepts` emptied (A2); row `baseline_identity`: no edit (F-k4 (b): C3-g removed `provenance.baseline` and owns `baseline_identity.readiness`))
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py` (the §2.4 columns manual_capture, baseline_identity.capture, environment_preparation.deploy_proof)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_evidence.py` (rows: `_provenance_errors`, `validate_baseline_record` incl. item 2b, `validate_manual_current`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_capture.py` (rows: `stand_probe`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_environment_preparation.py` (rows: `_run_step` / `provenance_validation`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (K-N2.12 callee rows of its sites; g7 :266-271 and K-T1.2 NEG :321-322 lose `_run_step`; the allow-list pin; F1 :650-668; K-N2.12 NEG second case; D13)
non-goals: the execution side (k2); conversion (k4); `manual_evidence.validate`, `person_sentences`; `_other_profile_errors` code (registry re-role only); `baseline_contract.py` and every `baseline_identity` row line (C3-g); `scripts/tests/test_coverage_contract.py` (QUARANTINED, `test-layers.json:7855`: its rows go to `test_manual_evidence.py`, which already holds `validate_manual_current` rows); any new test file
handoff: report path given by the Lead
edges: E-k3.1-E-k3.9 below
DoD: precondition first (E-k3.5): `provenance.baseline` absent from the base's `gate-registry.json` and `baseline_identity.readiness` present, else stop; `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; the §2.3 control: `old` (nine, equal to the frozen vector), `new` and `bad` for the nine consumers minus none (all exist now), new equal, bad different; then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_evidence.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/coverage_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_capture.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/environment_preparation.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_evidence.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_capture.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_environment_preparation.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files; slow files named, canon
siblings: F-T3 / C3-g (the baseline consumers, F-k4 (b)); A2 (the deploy consumer); axis 19 (manual capture <-> manual record keep one rule, `_provenance_errors` docstring :75-76); the sibling sentence of item 2b (:689) fixed here (G-8 (a)); `coverage_contract.py:845`'s inline local copy (AR-15)
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-k-cards-r2.md` (C3-k3)

Items:
1. **`_provenance_errors`** (:74-96): `local_source = local_source_request(record)` replaces :80. The elif :89-90 becomes
   `elif not acceptable(provenance_word(probe, task=story, local_source=local_source), "provenance.manual"):`; the sentence
   :91-92 is unchanged; `checked` is removed if nothing else reads it. Registry `allow` on the `_provenance_errors` site:
   `{"compare": "probe.get('result') == 'not_applicable'", "why": "picks the NA-specific sentence; the acceptance is the acceptable() call"}`.
   `_other_profile_errors` re-roled `validate`; E-c row: "calls `_provenance_errors` for each pair (pinned K-N2.12 :286) and its
   :129 only skips the revision binding for a probe that bound none; it accepts nothing `_provenance_errors` refused".
2. **`validate_baseline_record` — the acceptance** (:680-687): per probe, `checked = validate_runtime_provenance(probe)` stays
   (for the sentence); then `if not acceptable(provenance_word(probe), "baseline_identity.capture"):` appends
   `say_refusal("baseline_person") if checked["result"] == "person_confirmed" else "manual baseline runtime provenance is unverified"`.
   :686 is gone. Registry `allow` on the `validate_baseline_record` site:
   `{"compare": "checked['result'] == 'person_confirmed'", "why": "picks the refusal sentence; a person's word is refused by the consumer's tokens"}`.
   - Registry: `"baseline_identity.capture": ["matched", "not_applicable"]` under `provenance_acceptance` (F-k4 (b)). Its prefix
     names `baseline_identity` (`promotable: false`), so a `person_confirmed` added later is a finding. `baseline_identity`'s
     own `accepts` (`baseline_identity.readiness`, C3-g) is not touched.
   - Expected from: the comment :683-684 and `baseline_identity.decides` ("a person's word never stands in").
   2b. **Malformed blocks and the doorless sibling** (G-8 (a), the owner's word 17.11.2026: fixed in the round; text from g-h
   r2 §9 item 7):
   - (i) `contract = record.get("baseline_contract")`: a non-dict other than None/absent appends "baseline_contract must be a
     JSON object, got <type>" and is read as `{}` for the remaining checks. `runtime_before` / `runtime_after`: a non-dict other
     than None/absent appends "runtime_before (or runtime_after) must be a JSON object (the provenance probe's record), got
     <type>" (the field's own name in each sentence) and is read as `{}` everywhere below (the probe loop :680, the identity
     comparison :690-691, the request :671-672). `<type>` is the Python type name. No `AttributeError` reaches the caller.
   - (ii) :689 "manual baseline runtime must match baseline revision" keeps its words as the prefix and appends ": the probe's
     expected_source_revision is {x!r}, the approved baseline_revision is {y!r}. Capture again on a stand that runs that
     revision, or record no baseline: missing before evidence blocks no current check".
3. **`validate_manual_current`** (:818-849):
   - the import :818 becomes `from profile_contract import local_source_request, no_changed_file, provenance_word, refusal_text`
     plus `from gate_template import acceptable` (point of use, beside it); `validate_runtime_provenance` / `checked` dropped
     if nothing else reads them;
   - `local_source = local_source_request(record)` replaces :824;
   - :831-832 become `if not acceptable(provenance_word(probe, task=story, local_source=local_source), "provenance.manual"):`;
   - :845's inline copy becomes `... and not local_source`;
   - Registry `allow` entries on the site, in this order:
     `{"compare": "probe.get('result') != 'not_applicable'", "why": "an NA probe compared nothing and binds no checkout revision"}`,
     `{"compare": "probe.get('result') == 'not_applicable'", "why": "a second refusal sentence for a not_applicable no exemption covers; never lets a record through"}`.
4. **`stand_probe`** (:1612): `if not acceptable(provenance_word(value, task=story), "provenance.manual_capture"):`.
   F-k2 (a): the consumer's tokens become `["matched", "person_confirmed", "not_applicable:no_changed_file"]`.
5. **`_run_step`** (A2, :383-394): `provenance_ok = bool(acceptable(provenance_word(receipt), "environment_preparation.deploy_proof")
   and <the two equalities, unchanged>)`; `checked` stays for `provenance_validation`.
   - Registry: `"environment_preparation.deploy_proof": ["matched"]` under `provenance_acceptance` (F-k6 (a)); its prefix
     inherits `promotable: false`.
   - `provenance.environment_preparation` is removed from row `environment_preparation` (`accepts: {}`, legal).
6. **Imports (K2-4).** `manual_evidence.py` (:17-18): gains `local_source_request, provenance_word`, drops `ACCEPTS`,
   `acceptable_provenance` and any name left unused; `from gate_template import acceptable` at the point of use in each of the
   two functions. `manual_capture.py` (:99-100): gains `provenance_word`, drops `ACCEPTS`, `acceptable_provenance` if unused;
   `acceptable` at the point of use in `stand_probe`. `environment_preparation.py`: `provenance_word` and `acceptable` at the
   point of use in `_run_step` (:23 stays). `coverage_contract.py`: item 3. No name left imported and unused.
7. **Tests (rows in existing keep tables; the builder greps the named patterns first and adds rows to the tables found).**
   - `test_manual_evidence.py` (`_provenance_errors` / `validate_manual_current`): a local-source record with a valid bare NA ->
     no provenance error; the same with an invalid NA -> the error; the unreadable registry (`GT._READ` seam) with a valid
     matched -> the error. `validate_baseline_record`: a baseline pc -> the `baseline_person` sentence; a valid bare NA ->
     no provenance error (today's rule kept); the unreadable registry -> "manual baseline runtime provenance is unverified".
     Item 2b rows: `baseline_contract = "x"` -> the named error, no exception; `runtime_before = "x"` -> the named error, no
     exception; `runtime_after = 5` -> the named error, no exception; `runtime_before` None -> today's "baseline missing
     runtime_before"; a mismatching `expected_source_revision` -> the error holds "the approved baseline_revision is" and
     "Capture again"; the matching control -> no such error.
   - `test_manual_capture.py` (`stand_probe`): a valid bare NA (no `reason_code`) -> refused (F-k2); a valid ncf NA -> taken.
   - `test_environment_preparation.py`: a deploy receipt `person_confirmed` -> `provenance_ok` False; a valid matched with both
     equalities -> True (control).
   - `test_execution_request.py`: the §2.4 columns manual_capture, baseline_identity.capture, environment_preparation.deploy_proof.
   - Expected from: items 1-5, the docstrings, FR-59, FR-1.
8. **Pins (`test_gate_registry.py`)** (g-h r2 §9 item 4, K3-1):
   - F1: the check of `provenance.environment_preparation` (:652-653) becomes `home["environment_preparation.deploy_proof"] ==
     "provenance_acceptance"`. A NEW check `home["baseline_identity.capture"] == "provenance_acceptance"` is ADDED. C3-g's
     check `home["baseline_identity.readiness"] == "baseline_identity"` stays as C3-g wrote it. The list of consumers under
     `provenance_acceptance` gains the two new ids (sorted; the label's count word re-derived from the live registry).
   - F1 "both guarding rows are promotable false" stays.
   - The F1 loop runs on three pairs: C3-g's `("baseline_identity.readiness", "baseline_identity")`, unedited;
     `("baseline_identity.capture", "baseline_identity")`; `("environment_preparation.deploy_proof", "environment_preparation")`.
     Each gives exactly one finding naming the consumer and the guarding row; for the two new pairs the check is
     `` f"gate row `{rid}`" in got[0] `` (the prefix-rule message, `gate_registry.py:740-742`), because `rid in got[0]` is
     trivially true when the consumer id starts with the row id.
   - K-N2.12 NEG: a SECOND case: `person_confirmed` appended to `baseline_identity.capture` -> exactly one finding naming the
     consumer and the word. C3-g's case on `baseline_identity.readiness` stays unedited.
   - K-N2.12 callee rows -> `acceptable` for `manual_capture.stand_probe`, `manual_evidence._provenance_errors`,
     `coverage_contract.validate_manual_current`; two rows ADDED: `manual_evidence.validate_baseline_record` and
     `environment_preparation._run_step` call `acceptable`.
   - g7 (:266-271) and K-T1.2 NEG (:321-322) lose `("environment_preparation.py", "_run_step")`.
   - The allow-list pin: the k3 list of §2.5.
   - D13 re-measured: the `_run_step` triple leaves; the other sites lose their acceptance literals (:80, :89-90, :686, :824,
     :831-832, :1612 none). Named.

architecture content: `AR-13 -- every manual-side provenance acceptance reads the word through provenance_word and the predicate`; `AR-15 -- the last three local-source copies wired to local_source_request`; `AR-19 -- manual capture and manual record keep one rule`; `AR-22 -- baseline_identity.capture and environment_preparation.deploy_proof land with their readers, provenance.environment_preparation leaves in the same commit; baseline_identity.readiness untouched`; `AR-28 -- unaccepted, malformed or unreadable-registry provenance is a named refusal, pinned`; `AR-9 -- the baseline revision refusal names what was expected and a door`; `AR-29 -- units and classes unchanged`; `AR-20 -- allow-list pin +4 named entries, D13 re-measured`. judgment content: `none -- a membership join of a validated data word, and shape refusals of malformed blocks`.

Edges:
- E-k3.1 POSITIONAL: the NA-specific sentence (:86) stays before the predicate (elif). INVARIANT: one sentence per refused probe.
- E-k3.2 (the baseline): a person's word is refused by the tokens, and the sentence still says why (`baseline_person`).
  INVARIANT: a person's word never stands in for the old build.
- E-k3.3 (manual capture tightened, F-k2 (a); M4: 0 recorded NA): the code already refused a bare NA; the registry now says
  so. INVARIANT: no probe refused today is taken after.
- E-k3.4 (deploy proof): only `matched`. INVARIANT: a person's word never stands in for the deploy's proof (F1).
- E-k3.5 TEMPORAL (C3-g, F-k4 (b), Lead 17.11.2026): k3 is based after C3-g. C3-g removed `provenance.baseline` and added
  `baseline_identity.readiness` (under `baseline_identity`, reader `baseline_contract.deployment_readiness`) with its F1 and
  K-N2.12 NEG pins. k3 adds `baseline_identity.capture` (under `provenance_acceptance`, reader
  `manual_evidence.validate_baseline_record`) with its own pins. If the base still holds `provenance.baseline` (C3-g not
  merged), k3 stops with a question and removes nothing. INVARIANT: after C3-k3, both `baseline_identity.readiness` and
  `baseline_identity.capture` exist with their F1 pins; k3 adds its pin beside C3-g's and never replaces it; k3 writes no line
  of row `baseline_identity`; no consumer exists without a reader; every guard pin (F1, K-N2.12 NEG) counts exactly one
  finding per consumer.
- E-k3.6 (unreadable registry): every site of this card refuses (`acceptable` False); the sentence is today's until k4's
  F-k5. INVARIANT: a broken registry never admits a probe.
- E-k3-g8 (outside input: a hand-written manual record, item 2b): a non-object block is a named error and is read as `{}`;
  None/absent keeps today's "baseline missing …"; a mismatching revision names both revisions and the door. INVARIANT: a
  malformed manual baseline is a named refusal, never a crash and never a pass.
- E-k3.7 (conflicting pair in item 2b: a non-dict block AND the missing-field loop): `"x"` is truthy, so the loop :662-665 does
  not fire for it; only the type sentence does. INVARIANT: one sentence per fault.
- E-k3.8 (limit): `{x!r}` / `{y!r}` print the revisions whole (a 40-hex sha or a short tag; no cut introduced). The record is
  outside input: the type sentence names only the type, never the value, so a huge or binary value is never echoed.
- E-k3.9 (one road, P31): the manual capture and the manual record take the same consumer road (`provenance.manual` /
  `provenance.manual_capture`, one producer); no project, language or case is named.

---

## §6. Card C3-k4 — the conversion

task: given by the Lead
given:
- as k1, plus all merged k1-k3 diffs, the FROZEN VECTOR lines, this file §6
- read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`: `scripts/profile_contract.py:877-925,1065-1108`, `scripts/gate_template.py:46-68`, `scripts/driver_stage_build.py:370-390`, `scripts/tests/test_execution_request.py:590-690,1610-1625`, `scripts/tests/test_runtime_probe_onboarding.py:815-830,1270-1395`, `scripts/tests/test_role_commands.py:955-970`, `scripts/tests/test_gate_registry.py` (S-f lines, :277-292, :705-716, :1150-1180), `scripts/tests/fixtures/judgment-census.json:826`
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `provenance_acceptance`: `status`, `debt_ref`, `vocabulary`, `field`, `decides`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/profile_contract.py` (`acceptable_provenance` recast; `ACCEPTS` deleted; `refusal_text`'s registry clause)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py` (the import line, only if `ACCEPTS` / `acceptable_provenance` are still named there)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_build.py` (`build_outcome`: the one call :381)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py` (rows :682-686; the S-b rows)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_runtime_probe_onboarding.py` (:823, :1277, :1389 calls only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_role_commands.py` (:964 only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (S-f pins of `provenance_acceptance`; F2 live check :709-716; K-N2.12 positive control :291-292; C3-0 `live-record` :1162; D13)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` (the `acceptable_provenance` row :826 only, and only if `test_judgment_census.py` names it as gone)
non-goals: any site's acceptance logic (k2, k3); `gate_template.py` (`registry_why` exists on the base, RD1-27); C3-reg-precondition's block; `scripts/tests/test_profile_contract.py` and `scripts/tests/test_launch_wrappers.py` (QUARANTINED; F-r2-2); prose files outside owns (siblings: a line per hit)
handoff: report path given by the Lead
edges: E-k4.1-E-k4.8 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0, `provenance_acceptance` absent from the debt block, no F-b line names any of its accept sites; the §2.3 control: `new`, `recast` and `bad` for all nine consumers, `new` and `recast` equal to the FROZEN VECTOR lines, `bad` different (verbatim, script source attached); then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/profile_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_build.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_runtime_probe_onboarding.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_role_commands.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` and the printed non-slow files; slow files (incl. `test_judgment_census.py`) named, canon
siblings: axis 5 (`decides` changes): grep `acceptable_provenance|ACCEPTS|not_applicable` over `references/execution-lifecycle.md`, `references/manual-evidence.md`, `references/environment-preparation.md`, `skills/qa-story/phases/s5.md`, `skills/qa-story/phases/s6.md` (positive control: the same grep over `references/gate-registry.json` finds `decides`), a line per hit "checked, no edit (meaning unchanged)" or an edit inside owns; prose hits of the renamed names outside owns, read on the base: `runtime_probe.py:57` (`acceptable_provenance(rehearsal=True)` still exists: true), `gate_registry.py:42` (generic `ACCEPTS = (...)` example: true), `gate_registry.py:360` (historical comment naming `profile_contract.ACCEPTS`: the builder reports it as "historical, no edit" or as a finding line in the report — not edited, it is not owned); quarantined readers (F-r2-2): `test_profile_contract.py` (12 hits), `test_launch_wrappers.py` (2)
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-k-cards-r2.md` (C3-k4)

Items:
1. **Row.** `status: converted`, `debt_ref: ""`, `vocabulary: code`, `field: null` (F-k1 (a)). `decides`: "the probe's record is
   good enough for this use: `profile_contract.provenance_word` validates it and names its word, and `gate_template.acceptable`
   takes it for the consumer; per consumer: the run, the rehearsal and the S5 launch take matched, the person's word for the
   story and a probe that compared nothing; automation and the manual record also take a local-source request's
   not_applicable; the fingerprint takes any valid not_applicable; manual capture takes matched, the person's word and a probe
   that compared nothing; gate A's identity read takes matched or the person's word; baseline capture takes matched or any
   not_applicable, a person's word never; the deploy proof takes matched only". `unknown_branch` / `on_no_answer` / `waits_at`
   keep `question / wait / stage_entry`.
2. **`acceptable_provenance(record, consumer, *, rehearsal=False, task=None, local_source=False) -> bool`** =
   `acceptable(provenance_word(record, rehearsal=rehearsal, task=task, local_source=local_source), consumer)`, with
   `from gate_template import acceptable` at the point of use (K4-2: `profile_contract` is imported at load by most scripts).
   Docstring: the composition, the error direction, "an unknown consumer is False". `ACCEPTS` deleted. Readers changed in
   this commit:
   - `driver_stage_build.py:381` -> `profile_contract.acceptable_provenance(record, "provenance.rehearsal", rehearsal=True)`;
   - `test_execution_request.py:682-683` -> consumer `"provenance.run"`; `:686` (the `ValueError` row) becomes
     `acceptable_provenance(shapes["M"], "nope.x") is False`, label "an unknown consumer is False (C3-0 item 3)";
   - `test_runtime_probe_onboarding.py:823` `P.ACCEPTS` -> `"provenance.run"`; `:1277` `("matched",)` ->
     `"environment_preparation.deploy_proof"` with a comment line "the one consumer whose tokens are exactly `matched`: the
     strictness row needs a matched-only reader, not a deploy" (K4-3); `:1389` `("matched",)` -> same consumer, `("matched",
     "person_confirmed")` -> `"provenance.identity"`;
   - `test_role_commands.py:964` `PC.ACCEPTS[:2]` -> the two words read from the registry: `[w for w in ("matched",
     "person_confirmed")]` replaced by the `provenance.run` tokens without a `not_applicable` prefix, read through
     `gate_registry.load_registry` (if that read is not available in the test's imports, the literal `["matched",
     "person_confirmed"]` with a comment naming the consumer);
   - `execution_request.py`: nothing left (k2 dropped the names) — verify by grep and write "no edit" in the report.
3. **`refusal_text`** (F-k5 (a), G-5 (a) family form): at its start, `from gate_template import registry_problem, registry_why`
   (point of use); `problem = registry_problem()`; the sentence built as today is `text`; when `problem` is non-empty, return
   `registry_why(problem, f"the probe's answer was not judged (it said: {text})")`. Otherwise `text` as today. No fifth copy of
   the prefix (K4-2); `registry_why` is the RD1-27 builder on the base (`gate_template.py:60-68`).
4. **S-b rows (`test_execution_request.py`, the row's `test` file).** A request whose provenance is valid `unknown` -> refused,
   nothing runs; the unreadable registry (`GT._READ` seam) with a valid matched -> refused, and the refusal holds "the gate
   registry cannot be read (" and "the probe's answer was not judged". Expected from FR-59, FR-41 and item 3.
5. **S-f pins.**
   - `EXPECTED_DEBT` loses the row and `EXPECTED_CONVERTED` gains it, with an AR-20 comment naming C3-k4 and the task; K-T1.2
     `"N gate(s) left as debt:"` N-1; the split converted +1 / debt -1 with its comment and label count words; the F4 `code`
     list +1.
   - K-N2.12 positive control (:291-292): reads `"provenance_word" in called_names(..., "acceptable_provenance")` and
     `"validate_runtime_provenance" in called_names(..., "provenance_word")`.
   - The F2 live check (:713-716) on `profile_contract.ACCEPTS` is re-pointed: the `profile_contract.py` `<module>` item whose
     source names `PROVENANCE_RESULTS`' words (`person_confirmed` in `source`, `rows == ["provenance_acceptance"]`), label "F2
     and --sites lists profile_contract.PROVENANCE_RESULTS, attributed". If `--sites` shows no `<module>` item of
     `profile_contract.py` after the deletion, the vocabulary site registration (:64) and this check are a stop and a question.
   - C3-0 `live-record` (:1162) -> expected `False` (`field: null`), label naming F-k1 (a).
   - D13 re-measured: the `<module>` item of `ACCEPTS` leaves; `acceptable_provenance`'s token comparisons (:908-922) leave.
     Named.

architecture content: `AR-13 -- the provenance word is read only through provenance_word and acceptable`; `AR-15 -- one provenance predicate path; acceptable_provenance is its composition`; `AR-16 -- the registry sentence is built by registry_why, no fifth copy`; `AR-28 -- an unknown or unreadable-registry provenance is refused and says why, pinned by the S-b rows`; `AR-29 -- acceptable_provenance's census unit shrinks with its raise (named)`; `AR-19 -- axis 5 prose twins walked`; `AR-20 -- debt -1, converted +1, F4 +1, D13 named`. judgment content: `none -- the row converts; every acceptance is a data join after the unchanged validation`.

Edges:
- E-k4.1 TEMPORAL: before k4 the row is debt and literals are allowed; after it every accept site needs `acceptable` and every
  literal an `allow`; k2/k3 did both (M2: the convert-now list minus k2/k3's removals equals the allow set). INVARIANT:
  `--check` green on k4's tree.
- E-k4.2 (field null): a record passed whole to `acceptable` under a provenance consumer is False. INVARIANT: no unvalidated
  record is ever accepted.
- E-k4.3 (unreadable registry): the refusal names the registry and keeps the probe's own answer (item 3). INVARIANT: FR-41 —
  never a false cause, never a lost door.
- E-k4.4 (stories in flight, E-a): a probe record written before k4 is judged by the same rules. INVARIANT: the frozen vector
  equals `new` and `recast` (§2.3).
- E-k4.5 (S-f TEMPORAL): deltas from the main k4 is based on (C3-j not in it, §0.1). INVARIANT: S-f.
- E-k4.6 (readers of `ACCEPTS`): every keep-file and package reader changes in this commit; grep `\bACCEPTS\b` over
  `scripts/*.py` and the keep test files returns only prose (positive control: the same grep before the edit finds
  `profile_contract.py:877`). INVARIANT: no import of a deleted name survives in a keep or package file (an `ImportError` at
  import breaks a whole script).
- E-k4.7 (quarantined readers, F-r2-2 (a)): `test_profile_contract.py` and `test_launch_wrappers.py` still name the old forms;
  the report carries the expected quarantine-watch red line for each. INVARIANT: no canon file is red by the rename.
- E-k4.8 (limit): the registry sentence quotes `text` whole (no cut introduced; `refusal_text`'s own parts keep their
  existing cuts).

---

## §7. Forks (returned with a recommendation; the cards execute on the recommendation until the Lead decides)

- **F-r2-1 (K2-3) — the gate A world of an unreadable registry.** Read on the base: the unjudged identity becomes
  `runtime_identity: null` in the rehearsal row (informational; "no longer keys a proof"), never a person-visible
  "unobserved". The verdict's "gate A shows an unobserved stand identity" is stronger than the code. Per the Lead's rule
  the remark lies in k2's own file:
  - (a) **Recommended**: k2 item 6 — one `_note_once` via `registry_why` in `_reporter_outcome`, no signature change (the
    `onboarding_probe.py:331` override untouched). Cost: 3 lines, one import extension, one test row.
  - (b) No code; E-k2.2 states the measured world (null = "not known" is honest under FR-41; the dispatch stop names the
    registry). Cost: none; the gate's own output says nothing about the registry.
- **F-r2-2 (K2-1, K4-3, K3-2) — readers of the renamed predicate in QUARANTINED files.** `test_launch_wrappers.py`
  (`test-layers.json:8731`), `test_profile_contract.py` (:9186) and `test_coverage_contract.py` (:7855) sit in `quarantine`
  (from :7208). TESTING.md «Карантин»: a quarantined test "в каноне не запускается, не чинится и не правится". The verdict's
  K2-1 fix ("k2 owns test_launch_wrappers.py") and the old k1/k4 owns of `test_profile_contract.py` contradict that rule.
  - (a) **Recommended**: never edit them; the k1 matrix and k3 rows go into keep files (`test_execution_request.py`,
    `test_manual_evidence.py`); k2/k4 reports carry an "expected quarantine-watch red" line per file, for the `judge` role.
    Cost: two expected reds in the quarantine-watch job, judged once.
  - (b) Edit the quarantined files minimally (patch `acceptable` / consumer ids). Cost: an exception to the owner's
    quarantine rule — the owner's word is needed.
- **F-r2-3 (the brief's parallelism question) — §0.3.** (a) **Recommended**: serial k1 → k2 → k3 → k4. (b) k2 ∥ k3 after
  k1, k3 the later merger, its §2.4 columns moved to `test_manual_evidence.py`, every shared pin re-derived after merging
  k2. (c) k1 ∥ C3-g (row-disjoint; k1 the later merger on `D13_ITEM_COUNT`). (c) combines with (a) or (b).
- **G-6 (b) of the g-h round 2** (`load_receipts`, one road for receipts) is not a k-card edit: no k card touches
  `baseline_contract.py`, `controller.py` or `delivery_summary.py`. Noted, no fork.

No other fork remains: F-k1..F-k7 stand as the Lead decided them (F-k4 = (b) from 17.11.2026).

## §8. Small technical choices closed

- The committed matrix (§2.4) carries EXPLICIT expected booleans written from the tokens and docstrings; "today's predicate as
  code" (the verdict's wording) lives in the uncommitted control (§2.3). Reason: k4 deletes the old function, so a committed
  table that calls it breaks at k4; and a committed expectation taken from code is an oracle (P20). Both halves of K1-2 (i)
  are therefore present.
- The vector is frozen at k1 (not at k3 as the verdict proposed): the old site predicates are encoded in the script and the
  old function is untouched until k4, so the k1 freeze holds for every later card and does not depend on the k2/k3 order.
- k1's table lives in `test_execution_request.py` (the row's `test` file, keep) instead of the quarantined
  `test_profile_contract.py`.
- `validate_manual_current` rows go to `test_manual_evidence.py` (keep, `detector`; it already holds 9 `validate_manual_current`
  hits) instead of the quarantined `test_coverage_contract.py` (K3-2).
- The F1 loop's new pairs check `` gate row `<rid>` `` because `rid in got[0]` is trivially true for a consumer id that starts
  with the row id.
- The K2-2 pin counts items by the normalised source text, the same normaliser `_allowed` uses.
- Import placement per file (§4 item 5, §5 item 6, §6 items 2-3): top only where the module already loads `gate_template`
  at the top (`execution_request`, `run_suite` via `execution_request`, `gate_preflight`); point of use everywhere else.
- `refusal_text` on an unreadable registry returns one `registry_why` sentence whose tail keeps the probe's own answer, so the
  door of a real mismatch is not lost.
- `test_role_commands.py:964` reads the words from the registry, with a literal fallback named in the card.

## §9. Readers of every touched file (designer rule 7)

Commands (Grep tool, on the root checkout; counts are the tool's):
- file names `profile_contract|gate-registry|test_execution_request|test_gate_registry|execution_request|execution_fingerprint|run_suite|gate_preflight|test_gate_preflight|manual_evidence|coverage_contract|manual_capture|environment_preparation|test_manual_evidence|test_manual_capture|test_environment_preparation|driver_stage_build|test_runtime_probe_onboarding|test_role_commands|gate_template`
  over `tools/`: 25 hits in 10 files (12 of them `tools/source_split.py`).
- changed names `acceptable_provenance|\bACCEPTS\b|provenance_word|local_source_request|rehearsal_probe|refusal_text|_observed_identity|registry_why`
  over `tools/`: 1 hit, `tools/test_piles_door.py:88` (`test_check_refusal_text_…`, a substring: false positive; re-read
  case-insensitively, the same single line).
- the file names (case-insensitive) over `.githooks/`: 0 (positive control, same path and tool: `architecture_gate` -> 1 in
  `.githooks/commit-msg`); over `.claude/settings.json`: 0 (control `hygiene_gate` -> 1); over `.claude/agents/`: 0 (control
  `designer` -> 3 in `designer.md`).

| touched file (card) | reader | verdict |
|---|---|---|
| `references/gate-registry.json` (k1-k4) | `tools/source-split-carriers.json:15, :35`, `tools/source_split.py` (registry carrier), `tools/test_quarantine.py:2199` (path); package: `gate_registry.py`, `gate_template.py`, `test_gate_registry.py`, `test-layers.json` (`gate_named` rows keyed by the row `test`) | unchanged: file name, row form and `test` field unchanged; pins per card (S-f) |
| `scripts/tests/test_gate_registry.py` (k1-k4) | `tools/source-split-carriers.json:25` (D13 py-triple carrier), `tools/source_split.py` | unchanged: triples keep the `(file, function, row)` form |
| `scripts/execution_fingerprint.py` (k2) | `tools/dup-baseline.json:109` (a clone group), `tools/controller-blocks-gen.py:191` (text) | unchanged: `build`'s provenance condition only |
| `scripts/tests/test_execution_request.py` (k1, k2, k3, k4) | `tools/lint-baseline.json:223-226` (`UnusedImport` `execution_request as er`, keyed by path/class/args, not line) | unchanged; k2 removes the `ACCEPTS` import, adding no unused import |
| `scripts/tests/test_role_commands.py` (k4) | `tools/lint-baseline.json:259` (`HandReaderInput`), `tools/test_forge_metrics.py:285` (prose) | unchanged |
| `scripts/coverage_contract.py` (k3) | `tools/story_capture.py:500` (`coverage_contract_revisions`, a key name: false positive) | unchanged |
| `scripts/manual_capture.py` (k3) | `tools/test_piles_split.py:86` (a glob string) | unchanged |
| `tools/fixtures/dispatch_manifest/K8.txt` | a fixture string naming a path | unchanged |
| `scripts/profile_contract.py`, `run_suite.py`, `gate_preflight.py`, `manual_evidence.py`, `environment_preparation.py`, `driver_stage_build.py`, the other test files | no hit in `tools/`, `.githooks/`, `.claude/` beyond the rows above | unchanged |
| package readers of the changed names | `acceptable_provenance`: the sites of §2.1, `driver_stage_build.py:381`, tests `test_execution_request.py`, `test_runtime_probe_onboarding.py`, `test_gate_registry.py`, quarantined `test_profile_contract.py`, `test_launch_wrappers.py`; `ACCEPTS`: `execution_request.py:17`, `coverage_contract.py:818`, `execution_fingerprint.py:30`, `manual_capture.py:99`, `manual_evidence.py:17`, `run_suite.py:124`, `driver_stage_build.py:381`, tests `test_execution_request.py:17`, `test_role_commands.py:964`, `test_runtime_probe_onboarding.py:823`; `rehearsal_probe`'s parameter: `gate_preflight.py:3438-3444`, `test_gate_preflight.py:4261`, `test_launch_wrappers.py:168` (one positional arg: unaffected); `execution_request.py:3324` (the function object: unaffected); `_observed_identity`: `onboarding_probe.py:331` (override, signature unchanged), `test_gate_preflight.py:5221` (`lambda *a, **k`: unaffected); `refusal_text`: every provenance refusal site (text changes only on an unreadable registry); `judgment-census.json:826` (k4) | change in k2 (rehearsal_probe and its callers; site imports), k3 (site imports), k4 (`ACCEPTS`, `acceptable_provenance`, `refusal_text`, census row); quarantined files: F-r2-2 |

## §10. Closing table — remark -> where applied

| remark (source) | where applied |
|---|---|
| K-C1 (t-1092) allow-list pin, exact entries | §2.5 (both lists, whole texts, order rule); k2 item 8; k3 item 8 |
| K1-1 a mismatched record gets two words | §3 item 1 (mismatched read first, independent of validity); §2.4 R11/R13; E-k1.3 |
| K1-2 (i) per-consumer matrix | §2.4 (records × nine consumers, explicit expectations), grown per card (k1 item 4, k2 item 7, k3 item 7); §8 first bullet |
| K1-2 (ii) / K3-3 the 133-record walk over every consumer | §2.3 script (all fixture JSON, nine consumers, task and local grid) in every card's DoD |
| K4-1 (iii) frozen vector for k4 | §2.3 (frozen at k1, quoted into k2-k4; k4 compares `new` and `recast`); E-k4.4; §8 second bullet |
| K2-1 `test_launch_wrappers.py` breaks | not edited: the file is quarantined (TESTING.md); fork F-r2-2 (a) recommended; E-k2.9 report line; §4 non-goals; §9 corrected (":168 positional" kept, patches named) |
| K2-2 masking allow entry | k2 item 8 (exactly-one pin); E-k2.4 |
| K2-3 the gate A world | E-k2.2 rewritten from the base code (the identity is informational; measured world); fix as k2 item 6 on fork F-r2-1 (a) — in k2's own file, per the Lead's rule (no finding) |
| K2-4 import placement; k2 drops `ACCEPTS` from `execution_request` | k2 item 5 (per file); k3 item 6; k4 item 2 (point of use) and k4 owns "only if still named" |
| K3-1 the collision (F-k4 (b)) | k3 owns (row `baseline_identity`: no edit), k3 given (C3-g diff required), k3 item 2 registry bullet, k3 item 8 (F1, loop, NEG), E-k3.5; k4 item 1 `decides` names the capture consumer; the C3-g side is the g-h r2 card's |
| K3-2 owns by pointer | k3 owns name four test files inline; `test_coverage_contract.py` is quarantined, so its rows go to `test_manual_evidence.py` (§8) |
| K4-2 fifth copy of the registry prefix; lazy import | k4 item 3 uses `gate_template.registry_why` (RD1-27, on the base: no new copy, the standing finding's builder); point-of-use import |
| K4-3 readers list; the `("matched",)` mapping | k4 item 2 (every reader, incl. `test_launch_wrappers.py` via F-r2-2), the comment line for `test_runtime_probe_onboarding.py:1277`; §9 |
| D standing: duplication (four local copies, one survivor) | k1 item 2; k2 item 1; k3 items 1, 3 (incl. `:845`'s inline copy); §1.1 change check |
| D standing: code quality (K1-1, K2-2) | as above |
| D standing: P31 (`build_outcome` stays a `stand_identity` dispatch, reaches the predicate through the composition) | k4 item 2 (`build_outcome` calls the composition with a consumer id) |
| D standing: tests (J9 n/a; K2-1, K2-2, K-C1, K1-2) | as above; every row in a keep file; no new test file |
| E class completeness: mocks/pins bound to the renamed predicate | k2 siblings line (walked: the two mocks, K-N2.5, K-N2.12); K-C1 |
| t-1090 G2 invariant (both consumers with their F1 pins after k3) | E-k3.5 |
| Lead: F-k4 = (b), both worlds of the order | E-k3.5 (precondition: C3-g merged; otherwise stop, remove nothing); §0.2 |
| Lead: C3-j out of the queue; what depended on it | §0.1; §0.2; E-k4.5 |
| Lead: pins by measurement | every D13 / count line says "re-measured, named"; no number is prescribed |
| Lead: parallelism per card | §0.3; fork F-r2-3 |
| g-h r2 §9 items 1-5, 7 (owns, given, item 2, item 7, E-k3.5, E-k3-g8) | k3 owns and given; k3 item 2 registry bullet; k3 item 8; E-k3.5; k3 item 2b + item 7 rows + E-k3-g8 |
| G-8 (a) non-dict crash and the doorless sentence :689 | k3 item 2b, item 7 rows, E-k3-g8, E-k3.7, E-k3.8 |
| G-5 (a) in-line `registry_why(problem, tail)` family form | k2 item 6 (F-r2-1 (a)); k4 item 3 |
| G-6 (b) one road `load_receipts` | n/a to k cards (no k card touches those files); §7 last bullet |

## §11. Reading trail

- Given: the j-k cards (whole: :1-893); verdict t-1092 (whole); verdict t-1090 (whole); g-h r2 §2 header/owns (:140-304 of
  the round-1 file for C3-g items; r2 owns lines :194-198, :518-522, :677-679), r2 §9-§11 and its Lead lines (:893-1005).
- Base tree (`.claude/worktrees/agent-ac40b44fb0a175afa/ai-packages/qa-factory/`):
  - `scripts/gate_template.py` (whole); `scripts/gate_registry.py:74-87, 726-743, 772-784` (+ grep `promotable`);
  - `scripts/profile_contract.py:700-939, 1060-1111` (+ def grep);
  - `scripts/execution_request.py:14-27, 155-184, 2484-2513` (+ grep of the provenance names, `rehearsal_probe` callers);
  - `scripts/execution_fingerprint.py:108-139`; `scripts/run_suite.py:912-933` (+ import grep);
  - `scripts/manual_evidence.py:72-133, 658-697`; `scripts/coverage_contract.py:812-853`; `scripts/manual_capture.py:1596-1616`;
    `scripts/environment_preparation.py:378-397`; `scripts/driver_stage_build.py:370-387`;
  - `scripts/gate_preflight.py:3418-3467, 3516-3546, 3835-3870` (+ def list, `_observed_identity` grep);
  - `references/gate-registry.json:37-96`;
  - `scripts/tests/test_gate_registry.py:255-334, 640-719` (+ grep of the pins: D13 :1069, live rows :1157-1162);
  - `scripts/tests/test_launch_wrappers.py:140-184`; `scripts/tests/test_gate_preflight.py:4252-4331`;
  - `scripts/tests/test_execution_request.py` (grep `ACCEPTS_OF_THE_PACKAGE|__defaults__|_READ`);
  - greps: `acceptable_provenance|\bACCEPTS\b` over the package (count) and over tests (content); `target_kind.*local_source`;
    `validate_manual_current` over tests (count); `local_source|provenance_validation|baseline_person|no_changed_file` over
    five test files (count); `runtime_identity` readers; `judgment-census.json` rows; `registry_why` files;
  - `plans/piles/rules-debt/findings/20261117-c3-odin-stroitel-teksta-reestr-ne-chitaetsya.md`;
    `changelog.d/rd1-27-30-31.md` (RD1-27 built `registry_why`).
- Main: `ai-packages/qa-factory/scripts/tests/test-layers.json` (section keys :36 keep, :7208 quarantine; rows of eleven test
  files); `docs/TESTING.md:100-129`; `tools/lint-baseline.json:218-265`; grep `provenance\.baseline|baseline_identity\.readiness`
  over main's package; the rule-7 greps of §9.
- Not established: no run (`--check`, `--sites`, `GR.analyse`, the §2.3 control, any test); the D13 deltas and the record count
  are the builders' measurements; whether `gate_registry` exposes `norm` publicly (k2 item 8 has its stop); which keep files
  `--witness-for` prints for each card (the builder runs it; owns name the files that hold the rows today); whether C3-g /
  C3-h r2 add allow entries on the base (§2.5 keeps their positions).

## Lead decisions on the forks of round 2 (17.11.2026)

- F-r2-1 = (a), F-r2-2 = (a), F-r2-3 = (a): by recommendation; k1 -> k2 -> k3 -> k4 run serially, after C3-g, on main once the C3 wave branch is merged.
- No second plan-critic pass: the round applies verdict t-1092's K-remarks and the §9 edits of the g-h r2 cards; no architecture change. C3-j stays held on the owner's answer (J1).
