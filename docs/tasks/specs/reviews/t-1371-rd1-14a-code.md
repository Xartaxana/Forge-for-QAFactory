# t-1371 — code review of RD1-14a (rules-debt/1/RD1-14, step k1), critic

Branch `worktree-agent-a7d9058c432ebf6a9`, work commit 01d39275, head 7e7067eb (the report), merge base 65bc13ce (= the
report's base). Spec: card `docs/tasks/specs/20261118-rd1-14-c3-k-provenance-acceptance-card.md` §2, §3 (k1), Lead amendments
P-3 and P-7. Report: `docs/tasks/specs/reports/t-1361-rd1-14a.md`.

**Verdict: NEEDS WORK** — 0 blocking, 5 fixes before merge (F1-F4, F6; F1 touches only the report), 1 note against the
spec for the Lead (F5). The code does what items 1-3 and P-7 say, and the witness reproduces. The gaps: the frozen vector
has no not_applicable record; one half of E-k1.2 has no row that would catch it; the raise class is fixed in one reader
only. Accepting stays with the Lead (rule 6).

## Findings

**F1 — the frozen vector has no not_applicable record (fix before merge; report only).** Card §2 says the control "holds
the record x consumer matrix (r2 §2.4 R1-R15 + 133 fixture records)". F-2 (a) moves that matrix into the uncommitted
control. The builder's script walks only the fixtures: `records 152 [('None', 8), ('matched', 90), ('person_confirmed', 54)]`,
zero `not_applicable` (I re-ran it and got the same lines). R1-R15 sit only in the committed table, with four columns,
not nine. The vector the Lead quotes into k2-k4 therefore never exercises `no_changed_file`, `local_source` or a bare NA.
Those are the words this card adds and the decisions k2/k3 move: fingerprint bare NA, the manual_capture tightening,
baseline NA. Failure scenario: a k3 builder gives `provenance.manual` the token `not_applicable` instead of
`not_applicable:local_source`. `new` stays equal to frozen (no NA record exists), the control is green, and a bare NA
without local source is admitted. In k4 `old` is deleted, so this vector is the only witness. Fix: add the R1-R15 records
and their variants to `recs` (inline, or `provenance_shapes` from `test_execution_request.py`), re-take `old` for all nine
consumers and `new`/`bad` for the four, and replace the vector in the report before it is quoted into k2.

**F2 — E-k1.2's `no_changed_file` half has no row that would catch it (fix before merge; one row).** I ran a mutation
in memory (the function source copied and exec'd into the module; the file on disk was untouched). It reads
`no_changed_file(record)` before validity, right after the non-dict check. It survives: **0 red of 48**. R8 and R8-local
are built from `NA2`, which has no `reason_code`, so an invalid NA that carries `no_changed_file` is in no row. Failure
scenario for the mutant: `{**NA1}` without `timestamp` (invalid) gives `no_changed_file`, and automation, rehearsal and
manual accept an invalid record. That breaks E-k1.2's INV. The same harness does catch the `local_source` half (M2: R8-local
goes red) and the precedence rule (M3: R5 and R5-local go red). Fix: add one row to the c3_k1 table,
`("R8-ncf E-k1.2", {k: v for k, v in s["NA1"].items() if k != "timestamp"}, {}, "unknown", no)`. Expected value from:
item 1 and E-k1.2.

**F3 — the raise class is fixed in one reader only (Q4; fix before merge, or a node row).** Surface: the field types of a
probe record as `validate_runtime_provenance` reads them. Measured (`raises.py`; the field set the validator reads was
walked):

| shape | validator | provenance_word | refusal_text |
|---|---|---|---|
| `provenance: "x"` / `["x"]` | AttributeError | unknown | AttributeError |
| `result: ["matched"]` / `{..}` | TypeError | unknown | TypeError |
| `expected_source_revision: ["a"]`, `mr_source_revision: ["a"]` | TypeError | unknown | TypeError |
| `provenance.source_linkage: ["exact"]` | TypeError | unknown | TypeError |
| nested `verified_source_revisions`, list `deployed_source_revision`, list `person_confirmation.kind` | ok | unknown / mismatched / unknown | ok |

`refusal_text` is edited in this diff (P-7). It is the next call a site makes on exactly the records `provenance_word`
now calls `unknown`. Scenario after k2: `validate_request` gets `runtime_provenance` = a valid matched record with
`provenance: "x"`. `provenance_word` returns `unknown`, so the request is refused. Then `refusal_text(provenance)` raises
AttributeError, and the person sees a traceback instead of the refusal. This is not a regression: today
`acceptable_provenance` raises first. But the report names the sibling with no fix and no node line, which Q4 does not
allow. k2's owns do not hold `profile_contract.py`, so k2 cannot close it. Fix, either:
- (a) in this round (k1 owns the file): `validate_runtime_provenance` reads a non-dict `provenance` as an error plus `{}`,
  and guards the unhashable `result` and revision values. This is in the direction of refusal, adds no D13 item, and makes
  `provenance_word`'s catch unnecessary (see F4).
- (b) the Lead writes `refusal_text / validate_runtime_provenance raise on wrong-typed record fields | узел: <id>` with an
  owner holding `profile_contract.py` (k4 or a new node).

**F4 — answer to question 2: narrow the catch (fix before merge, low; the Lead's decision stands, this is a
recommendation).** What `except Exception` hides: NameError, KeyError, ValueError and RecursionError raised by
`provenance_word` itself or by the validators. Each turns into `unknown`, which means a refusal. For a bug in a branch the
table covers, the rows still go red: a typo in the NA branch turns R5/R6 red. For a branch with no row (for example a
future raise inside `person_confirmed_problems`' `content_accepted` path), the word is quietly `unknown`, and the
traceback appears later, inside `refusal_text`. The two narrower forms:
- A shape check on `provenance` first (the builder's measured case only) is **not** equivalent. Five of the seven raising
  shapes above raise TypeError, so "never raises" would break on `result: ["matched"]`.
- `except (AttributeError, TypeError)` is equivalent. It covers all seven shapes measured, and the c3_k1 table stays green
  under it: M5, **0 red of 48**.

Recommendation: `except (AttributeError, TypeError):`. If F3 (a) is taken, drop the catch and keep R15-4 as the row.

**F5 — P-7's temporal window (note against the spec, does not block; the Lead decides).** P-7 moved k4 item 3 into k1
without saying how it behaves in both worlds (rule 11 (i)). From k1 until a site moves (k2/k3), the six `refusal_text`
callers (`execution_request.py:102`, `:180`, `execution_fingerprint.py:124`, `manual_evidence.py:92`,
`coverage_contract.py:857`, `manual_capture.py:1677`) still judge through `acceptable_provenance`, which reads no
registry. Scenario: the registry is unreadable and `validate_request` refuses a valid mismatched record. The text now says
"...a factory defect, the probe's answer was not judged (it said: the stand runs build ...)". In fact the record was
judged and refused on its merits. The impact is small: the dispatch stop `REGISTRY_BLOCK` (`controller.py:5635`) probably
stops a run before any site; that is an estimate, not verified. Proposed: the Lead names the window at acceptance. No
code change.

**F6 — AR-16 is not named (Q10; fix before merge, low).** The moved item 3 carried `AR-16 -- registry_why` in k4's
architecture line, and the new `refusal_text` docstring itself cites "(RD1-14, AR-16)". The commit's `architecture:` line
names only AR-13, AR-22, AR-28 and AR-20. Fix: name `AR-16 -- refusal_text names an unreadable registry via registry_why`
in the line carried to the merge.

## The dispatch's questions

1. **Fit — yes.**
   - `provenance_word` (profile_contract.py, after `acceptable_provenance`) follows item 1's order exactly: non-dict ->
     unknown; validate (on `rehearsal_view` when rehearsal); effective mismatched -> mismatched; invalid or effective !=
     declared -> unknown; matched; person_confirmed only if `person_confirmed(record, task)`; NA -> no_changed_file >
     local_source > not_applicable; else unknown.
   - E-k1.2 POSITIONAL holds in the code: no NA reason or `local_source` is read before the validity return. The
     `local_source` half is pinned; the `no_changed_file` half is not (F2).
   - `local_source_request` = dict, `runtime_required is False`, `target_kind == "local_source"`. That is the predicate of
     the four copies (`execution_request.py:165`, `manual_evidence.py:80`, `coverage_contract.py:848`, `:869`) plus the
     dict guard.
   - Registry: `words` +2, `verdict_map` +2 (class `not_applicable`, matching reason_code), `sites` +2 (`produce`,
     `validate`). `accepts`, `status`, `vocabulary` and `field` are untouched (AR-22).
   - E-k1.4: the new names have no reader outside profile_contract.py and the two tests (positive control:
     `acceptable_provenance` found in coverage_contract, driver_stage_build, execution_fingerprint). `--check` is green
     and still says "1 gate(s) left as debt".
2. **The catch:** F4 (narrow it) and F3 (the class).
3. **P-7 — holds.** A readable registry: `registry_problem()` returns "" and `_unjudged_or` returns `text` unchanged
   (`gate_template.py:46-56`; row "P-7 control" green). An unreadable one: `registry_why(problem, "the probe's answer was
   not judged (it said: <text>)")`, the k4 item 3 text word for word. All five returns are wrapped. Only the
   `not_applicable` exit has a row (M6 and M7, unwrapping the mismatched and the "other" exits, survive at 0 red). I
   accept that within the budget: each wrap is one call, and putting the body in a helper would add an unregistered site
   and a D13 triple (the report's reason, plausible).
4. **D13 — reproduced** on the branch's own base with an archive of 65bc13ce: `items 160 triples 61` -> `items 170
   triples 63`. The triple diff is exactly the two triples `profile_contract.py` / `local_source_request` and
   `provenance_word`, all allowed (the row is debt). No other triple. The item list matches the report: four
   `target_kind` copies, `no_changed_file:718`, four in `provenance_word`, one in `local_source_request`. The pin comment
   gives before/after, the measurement and the reason (S-f form). `D13_TRIPLES` +2 in sorted order.
5. **Tests.**
   - (a) Killing power: c3_k1 catches M2, M3, M8 (task dropped -> R4 red) and M4 (no catch -> raise). It misses M1 (F2).
   - (b) Every column of R1-R14 and R15 matches r2 §2.4's table (R4 `F T T F`, R6 `F F T F`, R6-local `T F T T`, R8 all
     F); the words match r2's "k1's half". The three predicate rows trace to the row's tokens.
   - (c) `local_source_request` reaches no door yet, so it needs no row.
   - (e) Note against the spec, not the builder: `live-ncf`, `live-local` and `live-local-not-rehearsal` assert through
     `gate_template.acceptable` with the live registry what the c3_k1 columns R5/rehearsal, R6-local/automation and
     R6-local/rehearsal already assert (4 lines). The card named them.
   - (f) Volume: tests 47 + 13 = 60, product 59 + 6 + 1 = 66 (numstat). Within budget. No new file, no quarantined file
     edited.
6. **R11 negative control — present.** The script has `bad` (consumer `nope.x` -> `true 0`; all four shas differ from the
   frozen ones, and every frozen `true` > 0). The full source is in the report; it is not committed. The comparison is
   made by the reader, not printed by the script, which is the form r2 §2.3 prescribed. Its gap is coverage (F1), not the
   control.

## Standing questions

- Q1 fit: above. Q2: the catch (F4); the `_unjudged_or` placement is toward refusal.
- Q3 seams: the two sites are inserted, nothing is reordered; `part_live_registry` + `part_fix_pass` 292/292 (my run).
- Q4 class: F3; local-source copies wired k2/k3 per plan.
- Q5: above.
- DUPLICATION AND CONSISTENCY (Q6): none found beyond the node named in the spec (`acceptable_provenance` duplicates
  `provenance_word`'s branch until k4 deletes it). `registry_why` is reused (17 callers grepped); no second registry
  sentence.
- CODE QUALITY (Q7): `provenance_word` is 33 lines with nesting 3; no dead branch (`checked["result"] != declared` is
  redundant to validity on every path I traced, but item 1 asks for it); no names that lie.
- Q8 hygiene: 0 Cyrillic in the diff; CRLF kept (CRLF delta = net added lines in all four files); changelog fragment
  present.
- Q9 ratchets: `D13_ITEM_COUNT` 160 -> 170, named and reproduced; no other ratchet row. The forge-check pipeline was not
  read (no pipeline named in the dispatch).
- Q10: F6. VARIETY: no unknown value blocks or defaults; an unknown is `unknown` and is refused (no consumer reads it yet).
- Q11 JUDGMENT: none. A data word after unchanged validation; census and scan constants untouched.
- ONE ROAD (Q12): none found. I read the whole diff (126 added lines): no language, runner or project name and no
  exclusion.

## Trail

Read: card (whole); report (whole); r2 :195-345; `git diff 65bc13ce 01d39275` (all five files); profile_contract.py
:690-740, :732-925, :1095-1165; gate-registry.json :37-100; test_execution_request.py :570-610, :1612-1626, the new
function; gate_template.py :31-68; harness.py :110-160, :225-231; TESTING.md :40-99; design/architecture.md AR-16;
SIBLING_MAP axis headings; refusal_text callers (grep); `_READ[` seams in tests (grep).

Runs (verbatim tails):
- `python -B P/scripts/gate_registry.py --check` -> "A26 gate registry: no violations ... 1 gate(s) left as debt:
  provenance_acceptance ...", exit 0.
- `N(test_execution_request: T.c3_k1_one_producer_names_the_provenance_word())` -> `=== n: 48/48 ok ===`.
- `N(test_gate_registry: T.part_predicate();T.part_site_attribution())` -> `=== n: 62/62 ok ===`.
- `N(test_gate_registry: T.part_live_registry();T.part_fix_pass())` -> `=== n: 292/292 ok ===` (38 s).
- scratchpad `d13.py` (GR.analyse) on archive 65bc13ce and on head -> `items 160 triples 61 findings 0` / `items 170
  triples 63 findings 0`; diff = the two triples.
- the report's `provenance_vector.py`: `old` nine and `new` four on head -> identical to the report's vector (152
  records, 0 NA). The archive base gives 114 records because of a MAX_PATH artefact of the scratch path (FileNotFoundError
  on 19 long fixture paths, per-file diff), not a fixture change.
- scratchpad `raises.py` -> the F3 table.
- scratchpad `mut.py` (in-memory copies, disk untouched) -> M0 0/48 red, M1 0, M2 2, M3 4, M4 raised AttributeError, M5
  0, M6 0, M7 0, M8 2.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "F3: validate_runtime_provenance raises AttributeError/TypeError on wrong-typed record fields (7 shapes measured); provenance_word catches, refusal_text (edited in this diff, next call at every refusing site) does not; no node line in the report. Fix in this round (validator shape-safe, owns) or a node row with an owner holding profile_contract.py. Local-source copies are wired in k2/k3 per plan.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-rd1-14-c3-k-provenance-acceptance-card.md",
      "docs/tasks/specs/reports/t-1361-rd1-14a.md",
      "docs/tasks/specs/20261117-rules-debt-wave3-k-cards-r2.md:195-345",
      "git diff 65bc13ce 01d39275 (5 files)",
      "ai-packages/qa-factory/scripts/profile_contract.py:690-925,1095-1165",
      "ai-packages/qa-factory/references/gate-registry.json:37-100",
      "ai-packages/qa-factory/scripts/tests/test_execution_request.py:570-610,1612-1626,c3_k1",
      "ai-packages/qa-factory/scripts/gate_template.py:31-68",
      "docs/TESTING.md:40-99",
      "ai-packages/qa-factory/design/architecture.md AR-16"
    ],
    "reruns": [
      {"command": "python -B P/scripts/gate_registry.py --check", "result": "exit 0, 1 gate(s) left as debt: provenance_acceptance"},
      {"command": "N(test_execution_request: T.c3_k1_one_producer_names_the_provenance_word())", "result": "48/48 ok"},
      {"command": "N(test_gate_registry: T.part_predicate();T.part_site_attribution())", "result": "62/62 ok"},
      {"command": "N(test_gate_registry: T.part_live_registry();T.part_fix_pass())", "result": "292/292 ok"},
      {"command": "scratchpad d13.py (GR.analyse) base archive vs head", "result": "160/61 -> 170/63; two new triples, provenance_word and local_source_request"},
      {"command": "report provenance_vector.py old (9) and new (4) on head", "result": "identical to the report; 152 records, 0 not_applicable"},
      {"command": "scratchpad mut.py in-memory mutations", "result": "M1 ncf-before-validity survives 0/48; M2 2 red; M3 4 red; M5 narrow catch 0 red; M6/M7 unwrapped refusal exits survive"}
    ]
  },
  "fixes": [
    "F1 (report only): add R1-R15 and variants to the control's records, re-take old for nine consumers and new/bad for four, replace the frozen vector before it is quoted into k2",
    "F2: test_execution_request.py c3_k1 table: add row R8-ncf E-k1.2 = NA1 without timestamp -> unknown, all four consumers False",
    "F3: profile_contract.py::validate_runtime_provenance reads wrong-typed fields as errors (non-dict provenance -> error + {}, unhashable result/revisions guarded), or the Lead opens a node row with an owner holding profile_contract.py",
    "F4: profile_contract.py::provenance_word narrow except Exception to except (AttributeError, TypeError), or drop it if F3 (a) lands",
    "F6: name AR-16 -- refusal_text names an unreadable registry via registry_why in the architecture line carried to the merge"
  ]
}
```
