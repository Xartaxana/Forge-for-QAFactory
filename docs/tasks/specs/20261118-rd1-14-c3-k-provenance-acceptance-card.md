# RD1-14 (C3-k) — provenance_acceptance: four builder steps on today's main (t-1353, rules-debt/1/RD1-14, F19)

Designer draft. Base: root `main` 239b94ff, read 18.11.2026; no shell, nothing RUN (every run number is the builder's).
This is the C3-k sketch (cards spec :1350-1377) re-anchored on main. It keeps the design the Lead accepted in
`docs/tasks/specs/20261117-rules-debt-wave3-k-cards-r2.md` ("r2": F-k1..F-k7, F-r2-1/2/3 (a), :935-938) and changes only
what main or a newer rule broke (F-1..F-3). On F-5 (a) it replaces r2 as the `designer:` line of the four dispatches.
`P` = `C:/QAFactory/forge-repo/ai-packages/qa-factory`. `N(mod: calls)` = narrow call of a script-style test file:
`python -B -c "import sys;sys.path[:0]=[r'P/scripts/tests',r'P/scripts'];import harness,<mod> as T;<calls>;harness.finish('n')"`.

## §0. Q1 — the state on main (measured)

Row `provenance_acceptance` (`gate-registry.json:37-93`): `debt`, `B-255`, the LAST debt row (`test_gate_registry.py:68-69`,
`:263` "1 gate(s) left as debt:"); `field: result`, `vocabulary: target`, `promotable: true`, `question/wait/stage_entry`,
`question_kind: null`. Its consumers `provenance.{automation,fingerprint,manual,manual_capture,rehearsal}` (:81-85) have
NO reader (Grep `"provenance\.[a-z_]+"` over `scripts/`: only `tests/test_gate_registry.py:1249`). Every site decides through
`profile_contract.acceptable_provenance` (:895-923) + `ACCEPTS` (:877): it validates, binds a word to its story, reads
`reason_code` from the RECORD; `gate_template.acceptable` (:70-106) reads it from the row's `verdict_map`, so it refuses a
`no_changed_file` probe on the live row (`test_gate_registry.py:1232`). Hence F-k1 (a): a producer of the word.

| site | unknown / absent / malformed provenance today | counted literals |
|---|---|---|
| `scripts/execution_request.py::validate_request` (:151-180) | non-dict -> "runtime_provenance is required"; else `acceptable_provenance(.., task)` :176 or the local NA literal :177; refusal + `refusal_text` | :167, :170, :177; seed :297 allowed |
| `scripts/execution_request.py::rehearsal_probe` (:2486-2508) | `acceptable_provenance(value, accepts, rehearsal=True)` else `ProvenanceRefused` | none |
| `scripts/gate_preflight.py::_observed_identity` (:3485-3511) | `accepts=("matched", "person_confirmed")` :3508; any refusal -> `""` | tuple :3508 |
| `scripts/run_suite.py::probe_runtime` (:926-940) | `acceptable_provenance(value, ACCEPTS)` :938 else `ProvenanceRefused` | none |
| `scripts/probe_by_code.py::probe_runtime` (:2880-2887) | delegate to `run_suite.probe_runtime` | none |
| `scripts/execution_fingerprint.py::build` (:104-138) | non-dict -> problem; predicate or ANY valid NA :121-122 | :122, :134 |
| `scripts/manual_evidence.py::_provenance_errors` (:74-96) | NA sentence :86; predicate or local NA :89-90 | :86, :90 |
| `scripts/manual_evidence.py::_other_profile_errors` (:99-133) | calls `_provenance_errors` :121; :129 skips an NA probe's binding | :129 |
| `scripts/manual_evidence.py::validate_baseline_record` (:680-687) | pc -> `baseline_person` :682; valid and in {matched, NA} :686 | :682, :686 |
| `scripts/coverage_contract.py::validate_manual_current` (:842-869) | predicate or local NA :855-856; skip :863; NA refusal :869 | :856, :863, :869 |
| `scripts/manual_capture.py::stand_probe` (:1649-1679) | refusal -> `EnvBlocked`; predicate :1676 | none |
| `scripts/environment_preparation.py::_run_step` (:383-398) | valid and `== "matched"` and two equalities :388-391; bad stdout -> False | :388 |
| `scripts/profile_contract.py::acceptable_provenance` | token logic; unknown token -> `ValueError` :908-910 | its own |
| `scripts/driver_stage_build.py::build_outcome` (:388-391, row `stand_identity`) | `acceptable_provenance(record, ACCEPTS, rehearsal=True)` | (other row) |

Moved by earlier C3 cards: no provenance accept site. C3-0 built `gate_template.acceptable` (a `library` site here); C3-a,
C3-b, C3-j touch none (C3-b: `_match` :2102, row `test_identity`); C3-f converted row `environment_preparation`, leaving
`provenance.environment_preparation` (:387) dead (words `blocked`/`unknown`); C3-g added `baseline_identity.readiness`
(`test_gate_registry.py:708`); C3-h converted `stand_identity`, whose question is the provenance question (§1.2); RD1-25: a
converted accept site's `acceptable` call names a LITERAL key of its own row (`gate_registry.py::_consumer_problem` :426-444);
RD1-27 built `registry_why`. Nothing of r2 is built: Grep -i `provenance_word|deploy_proof` over `P` = 0 (same call:
`baseline_identity\.readiness` 7).

## §1. Q2 — the target; architecture (designer rule 1)

**§1.1 Row after k4.** `converted`, `debt_ref: ""`, `vocabulary: code`, `field: null` (F-k1 (a): a whole record is refused);
`words` = the five class words + `no_changed_file`, `local_source` (class `not_applicable`, that `reason_code`). Consumers, all
under this row, all literal: `provenance.automation` (validate_request), `provenance.rehearsal` (rehearsal_probe,
build_outcome), `provenance.identity` (gate A, new), `provenance.run` (run path, new), `provenance.fingerprint` (bare NA kept,
F-k2 (a)), `provenance.manual`, `provenance.manual_capture` (tightened to no_changed_file, F-k2 (a)),
`baseline_identity.capture` `[matched, not_applicable]` and `environment_preparation.deploy_proof` `[matched]` (prefixes
inherit `promotable: false`, F-k4 (b), F-k6 (a)). Row `environment_preparation`: `accepts: {}`.

**§1.2 Who asks, the wait, the answer (unchanged here).** The branch stays `question / wait / stage_entry` on ONE road: the
build question of row `stand_identity`. At each stage entry `driver_stage_build.build_check` (:300-350) rehearses the probe;
`build_outcome` (:369-431) turns `unknown` + `asks_person` or `mismatched` into a `Person` of kind `stand_identity` and the
stage waits; `take_build_answer` (:557ff) records the word in `artifacts/<T>/state/stand-confirmations.jsonl` or
`records/stand-identity.json` (`stand_identity.py:11, :55, :597`); the next probe answers `person_confirmed`
(`runtime_probe.py:43-48`), taken bound to the story (not by the baseline or the deploy proof). Text owner:
`references/build-identity-methods.json` via `stand_identity.data()`. Accept sites never ask: they refuse with `refusal_text`,
whose door names that question (`REFUSAL_DEFAULTS` :932-939). No new question (F-4).

**§1.3 AR invariants and the change check each DoD carries.**
- AR-13: one producer (`provenance_word`), one predicate (`acceptable`). Check after k4: Grep
  `acceptable_provenance|\bACCEPTS\b` over `P/scripts/*.py` = prose only.
- AR-15: the local-source copies (`execution_request.py:165`, `manual_evidence.py:80`, `coverage_contract.py:848, :869`) ->
  `local_source_request`. Check after k3: Grep `target_kind.*local_source` over `P/scripts/*.py` = that function (before: 4).
- AR-22: each consumer lands with its reader; the dead consumer leaves in k3. AR-28: every doubt -> a word no consumer takes.
- AR-19: manual capture and manual record keep one rule. AR-20: D13, allow pin, split re-measured and named. AR-9/AR-16:
  refusals keep the expected value and the door; the registry sentence is `registry_why`.
- AR-29: every check added or altered is owner **data**; census classes unchanged except
  `profile_contract.py::acceptable_provenance` (`judgment-census.json:830`, `shape`), which leaves with it in k4 (F-1 (a)).
- Commit lines: `architecture:` / `judgment:` in the form of `tools/architecture_gate.py` (the only carrier, not copied).

Variety walk (`design/architecture.md` § A):
- `axis 7: held by table|key -- build-identity-methods.json, records/stand-identity.json, the stand_identity question; unknown value -> the stage-entry question, every provenance accept site refuses with that door`
- `axes 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13: n/a -- existing provenance decisions re-routed through the registry; no language, surface, tracker, host or project shape is read`

## §2. Shared to the four steps

**Order** (F-r2-3 (a)): k1 -> k2 -> k3 -> k4 serial, each on main after the previous merged. `gate_preflight.py`: C3-j and
C3-h are merged, k2 is its only open holder; the card's "C3-k -> C3-h" is stale (C3-h landed first, fb9e79c2). Before each
launch the Lead reads the open TAKEN batches holding the step's files (cards spec §4).

**Shared edges** (each step pins those its code reaches):
- E-S1 unknown (declared, or validating to it): word `unknown`, every consumer False, refusal names the build question.
  INVARIANT: an unknown never reaches a run, capture, fingerprint or proof (FR-59).
- E-S2 absent / None / non-dict / `{}`: each site's own shape sentence stays first (validate_request :153-154, fingerprint
  :111-112, manual :844-845, baseline k3 2b); `provenance_word` gives `unknown`. INVARIANT: never a crash, never a pass.
- E-S3 malformed (`MATCHED`, invalid matched, effective mismatched, pc with `technical_verification`, a word for another
  story): `unknown`/`mismatched`. INVARIANT: only the exact validated word counts; story A's word never admits story B.
- E-S4 an answer that never comes: no accept site waits or times out into a pass; the question is re-raised at each entry
  while the probe says `unknown` + `asks_person`; an `unknown` without it (docker silent, probe stopped,
  `runtime_probe.py:1300-1302`) is a status line at entry and a refusal at the run (row stand_identity, unchanged).
  INVARIANT: silence is never an acceptable word.
- E-S5 second ask on re-entry: a recorded word that still binds makes the probe say `person_confirmed`, so no re-ask; a word
  whose commit moved is `voided` and asked again (C3-h). INVARIANT: a binding word is never re-asked; a stale one never counts.
- E-S6 known at one stage, unknown at the next: each consumer judges the record handed to it now (the run re-probes at
  launch; the manual record demands before == after, :93-95; the fingerprint keys the runtime); this card adds no reuse of a
  stored verdict. INVARIANT: a provenance measured on another stand or moment never counts later.
- E-S7 unreadable registry: `acceptable` False, every site refuses; from k4 the refusal says so. INVARIANT: a broken registry
  never admits a probe.
- E-S8 one road (P31): one producer, one predicate, literal consumers; no language/project/case name read.

**Recorded-data control** (DOC-DISPATCH witness, never committed): r2 §2.3's script (r2 :200-290) in the builder's
scratchpad, source and output in the report; edits: `provenance.identity` judged after `provenance.rehearsal` (F-1 (a));
`recast` (k4) = inline `acceptable(provenance_word(..), c)`. `old` frozen at k1, quoted by the Lead into k2-k4; it holds the
record x consumer matrix (r2 §2.4 R1-R15 + 133 fixture records) on F-2 (a). `new` != frozen: stop and ask.

**Test budget** (TESTING.md «Бюджет / Объём»): `test:` lines are in strength order; the builder writes top-down until test
lines reach code lines and reports the rest `tests not written: <line> -- over budget`. "Pins that move" keep main green: they
are written first and are not behaviour lines.

## §3. Step k1 — RD1-14a: the word and the local-source test

given: this file (the sites and windows of §0, the pins of §3); r2 §2.3; `P/scripts/tests/test_execution_request.py:570-692`; `P/scripts/tests/test_gate_registry.py:1023-1260`
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/profile_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
non-goals: every accept site (k2, k3); `acceptable_provenance`/`ACCEPTS` (k4); any `accepts` entry (AR-22); row status/vocabulary/field (k4); quarantined `test_profile_contract.py`; any new test file
handoff: report path given by the Lead
edges: E-S1-E-S3, E-S8, E-k1.1-E-k1.4
DoD: `python -B P/scripts/gate_registry.py --check` exit 0, still "1 gate(s) left as debt:"; the control (`old` all consumers = frozen; `new`/`bad` automation, rehearsal, fingerprint, manual); `N(test_execution_request: T.c3_k1_one_producer_names_the_provenance_word())`; `N(test_gate_registry: T.part_predicate();T.part_site_attribution())`; line `not run locally: test_execution_request.py, test_gate_registry.py, canon judges`
siblings: the local-source copies (AR-15, wired k2/k3); quarantined `test_profile_contract.py` (F-r2-2 (a))
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-rd1-14-c3-k-provenance-acceptance-card.md (k1)

1. `provenance_word(record, *, rehearsal=False, task=None, local_source=False) -> str`, after `acceptable_provenance`, never
   raises: non-dict -> `unknown`; `checked = validate_runtime_provenance(rehearsal_view(record) if rehearsal else record)`;
   effective `mismatched` -> `mismatched`; invalid or effective != declared -> `unknown`; `matched` -> `matched`;
   `person_confirmed` -> itself if `person_confirmed(record, task)` else `unknown`; `not_applicable` -> `no_changed_file` if
   `no_changed_file(record)`, else `local_source` if `local_source`, else `not_applicable`; else `unknown`.
2. `local_source_request(record) -> bool`: dict, `runtime_required is False`, `target_kind == "local_source"` (the request's).
3. Registry: `words` += `no_changed_file`, `local_source`; `verdict_map` += both; `sites` += `provenance_word` (`produce`),
   `local_source_request` (`validate`).
- `test: test_execution_request.py::c3_k1_one_producer_names_the_provenance_word (new table: r2 §2.4 R1-R15 with rehearsal/local_source variants) | expected from: item 1, docstrings of validate_runtime_provenance / person_confirmed / no_changed_file, FR-59`
- `test: test_gate_registry.py::predicate_cases rows live-ncf (no_changed_file, provenance.rehearsal, True), live-local (local_source, provenance.automation, True), live-local-not-rehearsal (local_source, provenance.rehearsal, False) | expected from: registry tokens :81-85`
Pins that move: D13 (`:1141` and two triples `profile_contract.py` `provenance_word` / `local_source_request`; r2 M2 measured
the words alone at +5 items), `GR.analyse` before and after, S-f comment form; any other new triple: stop and ask.
Edges: E-k1.1 None/list/str/`{}` -> `unknown` (INV: absence never yields an acceptable word). E-k1.2 POSITIONAL: validity is
decided before any NA reason or `local_source` is read (INV: an invalid record never yields matched, person_confirmed,
no_changed_file or local_source). E-k1.3 pair `no_changed_file` + `local_source`: `no_changed_file` wins (INV: no consumer
takes `local_source` without `no_changed_file`, so no decision changes). E-k1.4 TEMPORAL: nothing reads the new functions yet;
the new words make local-source literals counted items of a debt row, allowed (INV: `--check` green at every step).
Error direction of the reused validators, now feeding a gate word: toward refusal only; R2 outside a rehearsal, R4, R7-R15
stay `unknown`/`mismatched` (table rows).
architecture: `AR-13 -- one producer of the word`; `AR-22 -- no consumer yet`; `AR-28 -- malformed yields unknown`; `AR-20 -- D13 named`. judgment: `none -- a data word after the unchanged validation`.

## §4. Step k2 — RD1-14b: the execution side through the predicate

given: as k1 + merged k1 + the frozen vector; §0 windows of the k2 sites; `P/scripts/gate_preflight.py:3889-3925`; `P/scripts/gate_registry.py:420-445`; `P/scripts/tests/test_gate_preflight.py:4229-4350`; `P/scripts/tests/test_gate_registry.py:266-338,700-735`
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_request.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/execution_fingerprint.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_suite.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_preflight.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
non-goals: `_match`, `green_over_same_bytes` (C3-b); `probe_by_code.py` code (registry re-role only); `onboarding_probe.py` (override keeps its signature); manual sites (k3); `acceptable_provenance`/`ACCEPTS` definitions (k4); row status; quarantined `test_launch_wrappers.py`; any new test file
handoff: report path given by the Lead
edges: E-S1-E-S8, E-k2.1-E-k2.5
DoD: `--check` exit 0; the control (`new`/`bad` + identity, run); `N(test_execution_request: r=T.base_request();T.n2_k1_probe_runtime_is_the_one_predicate(r);T.n2_k2_validate_request_takes_a_word_bound_to_the_story(r);T.n2_k3_the_fingerprint_of_a_word_is_not_the_fingerprint_of_a_reading(r);T.t300_k33_a_freshness_read_is_a_rehearsal_end_to_end())`; `python -m pytest P/scripts/tests/test_gate_preflight.py::test_w5_the_info_lines_carry_the_portable_argv_and_the_stored_one_is_read_with_this_machine P/scripts/tests/test_gate_preflight.py::test_t300_k30_the_identity_reader_of_gate_a_is_a_rehearsal_and_takes_the_fifth_word -q`; `N(test_gate_registry: T.part_live_registry();T.part_fix_pass();T.part_site_attribution())`; `not run locally:` line for the three slow files
siblings: mocks/pins on old names: `test_launch_wrappers.py:163,167` (quarantined: an expected quarantine-watch red line, F-r2-2 (a)), K-N2.5 `test_execution_request.py:1335`, K-N2.12 `test_gate_registry.py:284-297`; `driver_stage_build.build_outcome` (k4)
designer: this file (k2)

1. `validate_request`: :165 -> `local_source = local_source_request(data)`; :167-173 stay BEFORE the predicate; :176-177 ->
   `taken = acceptable(provenance_word(provenance, task=data.get("task"), local_source=local_source), "provenance.automation")`,
   `if not (taken or said_local):`, same sentence. Allow after the seed: `checked['result'] == 'not_applicable'` (why: picks the
   refusal sentence; acceptance is the acceptable() call), `provenance.get('result') == 'person_confirmed'` (why: refuses a
   word on a request that skips the probe).
2. F-1 (a): `rehearsal_probe(spec: dict) -> dict` accepts `acceptable(provenance_word(value, rehearsal=True),
   "provenance.rehearsal")` else `ProvenanceRefused`; docstring names the consumer. `_observed_identity` calls
   `rehearsal_probe(spec)`, then returns the identity only if `acceptable(provenance_word(observed, rehearsal=True),
   "provenance.identity")`, else `""`; it stays `accept`. Registry `"provenance.identity": ["matched", "person_confirmed"]`.
3. `run_suite.probe_runtime`: `acceptable(provenance_word(value), "provenance.run")`; registry `"provenance.run": ["matched",
   "person_confirmed", "not_applicable:no_changed_file"]`; `probe_by_code.probe_runtime` re-roled `dispatch`.
4. `execution_fingerprint.build`: :121-122 -> `if not acceptable(provenance_word(spec["runtime_provenance"]),
   "provenance.fingerprint")`; allow `runtime.get('result') == 'person_confirmed'` (why: keys a run on a word; no acceptance).
5. Imports: `execution_request` :17 + `local_source_request, provenance_word`, - `ACCEPTS, acceptable_provenance`; `run_suite`
   top `from gate_template import acceptable`, :124 -> `provenance_word`; `execution_fingerprint` point-of-use `acceptable`,
   :30 drops dead names. No unused import (`tools/lint-baseline.json`).
6. F-r2-1 (a): in `_reporter_outcome` after :3919, `if not identity and (problem := registry_problem()):
   self._note_once(<its check>, registry_why(problem, "the stand's build is not recorded with this rehearsal"))`.
- `test: test_execution_request.py::n2_k2_validate_request_takes_a_word_bound_to_the_story rows: local-source request + valid bare NA admitted; + invalid NA refused; Person_Confirmed refused; unreadable registry (GT._READ seam, as :1616-1623) + valid matched refused | expected from: item 1, E-S3, E-S7`
- `test: test_gate_preflight.py::test_t300_k30_... row: a no_changed_file probe and an unknown probe both give identity "" | expected from: item 2, tokens of provenance.identity`
- `test: test_gate_preflight.py::test_w5_... row: unreadable registry -> identity "" and a note with "the gate registry cannot be read (" | expected from: item 6, FR-41`
Pins that move: stub `test_gate_preflight.py:4253` -> `lambda spec: ...`; K-N2.5 `:1335` goes (no default left), covered by
K-N2.12; K-N2.12 callees -> `acceptable` for `run_suite.probe_runtime`, `rehearsal_probe`, `validate_request`,
`execution_fingerprint.build`, + `_observed_identity`; K-T1.2 NEG `:330-331` per measurement; allow pin `:314-321` +3 (§7);
F1 `:711-714` + `provenance.identity`, `provenance.run`; D13 measured (tuple :3508, :165, :177, :122 leave). r2's K2-2 row
(one allow entry covers one comparison) if the budget holds.
Edges: E-k2.1 POSITIONAL: :167/:170 stay before the predicate, `said_local` still suppresses the second sentence (INV: one
sentence per refused record, today's). E-k2.2 gate A on an unreadable registry: identity `""` -> `runtime_identity: null`,
informational, the note names the registry (INV: an unjudged identity is never stated as a fact). E-k2.3 TEMPORAL: row still
debt, allow entries inert until k4 (INV: `--check` green; every allow entry matches a comparison, F-d). E-k2.4 consumer typo:
False, refused, red in the control (INV: no false accept). E-k2.5 HOT file: one open holder (INV: no two open nodes edit it).
architecture: `AR-13 -- execution side through the predicate`; `AR-22 -- two consumers with their readers`; `AR-28 -- doubts refused, pinned`; `AR-20 -- allow pin +3, D13 named`. judgment: `none -- a join of a validated data word`.

## §5. Step k3 — RD1-14c: the manual side, the baseline capture, the deploy proof

given: as k2 + merged k1-k2; §0 windows of the k3 sites; registry rows `provenance_acceptance`, `environment_preparation`, `baseline_identity`; `P/scripts/tests/test_manual_evidence.py:763ff`; `P/scripts/tests/test_manual_capture.py:518-670`
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_evidence.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/coverage_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/manual_capture.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/environment_preparation.py C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_evidence.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_manual_capture.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_environment_preparation.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
non-goals: execution side (k2); conversion (k4); `manual_evidence.validate`, `person_sentences`; `_other_profile_errors` code (re-role only); `baseline_contract.py` and every line of row `baseline_identity`; quarantined `test_coverage_contract.py` (its rows go to `test_manual_evidence.py`); any new test file
handoff: report path given by the Lead
edges: E-S1-E-S8, E-k3.1-E-k3.7
DoD: precondition `baseline_identity.readiness` present and `provenance.baseline` absent in the base registry, else stop; `--check` exit 0; the control (all consumers); `python -B P/scripts/tests/test_manual_evidence.py`; `python -B P/scripts/tests/test_environment_preparation.py`; `N(test_manual_capture: T.n2_k8_a_capture_takes_the_persons_word_and_nothing_on_an_unknown())`; `N(test_gate_registry: T.part_live_registry();T.part_fix_pass();T.part_site_attribution())`; `not run locally:` line for the slow files
siblings: F-T3 / C3-g (`baseline_identity.readiness` untouched); A2 (deploy consumer); axis 19 (capture and record, one rule); the doorless sentence :689 (G-8 (a))
designer: this file (k3)

1. `_provenance_errors`: :80 -> `local_source_request(record)`; :89-90 -> `elif not acceptable(provenance_word(probe,
   task=story, local_source=local_source), "provenance.manual"):`; allow `probe.get('result') == 'not_applicable'` (why: picks
   the NA sentence). `_other_profile_errors` re-roled `validate`.
2. `validate_baseline_record`: per probe `if not acceptable(provenance_word(probe), "baseline_identity.capture"):` append
   `say_refusal("baseline_person")` if `checked["result"] == "person_confirmed"` else "manual baseline runtime provenance is
   unverified"; :686 goes; allow `checked['result'] == 'person_confirmed'` (why: picks the sentence). Registry
   `"baseline_identity.capture": ["matched", "not_applicable"]` under this row.
   2b (G-8 (a), outside input): a non-dict `baseline_contract`/`runtime_before`/`runtime_after` other than None/absent appends
   "<field> must be a JSON object, got <type name>" and is read as `{}` below; None/absent keeps "baseline missing <field>";
   :689 keeps its words and appends both revisions (`!r`) and the door "Capture again on a stand that runs that revision, or
   record no baseline: missing before evidence blocks no current check".
3. `validate_manual_current`: :842 -> `local_source_request, no_changed_file, provenance_word, refusal_text` + point-of-use
   `acceptable`; :848 -> `local_source_request(record)`; :855-856 -> `if not acceptable(provenance_word(probe, task=story,
   local_source=local_source), "provenance.manual"):`; :869 inline copy -> `local_source`; allow
   `probe.get('result') != 'not_applicable'` (why: an NA probe binds no revision), then `probe.get('result') ==
   'not_applicable'` (why: second NA sentence; never admits).
4. `stand_probe` :1676 -> `if not acceptable(provenance_word(value, task=story), "provenance.manual_capture"):`; tokens ->
   `["matched", "person_confirmed", "not_applicable:no_changed_file"]`.
5. `_run_step` :388 -> `provenance_ok = bool(acceptable(provenance_word(receipt), "environment_preparation.deploy_proof") and
   <the two equalities>)`; `checked` stays for `provenance_validation`. Registry `"environment_preparation.deploy_proof":
   ["matched"]` under this row; row `environment_preparation` `accepts: {}`.
6. Point-of-use imports; nothing left unused (`manual_evidence` :17 drops `ACCEPTS`, `acceptable_provenance`).
- `test: test_manual_evidence.py::n2_k9_the_persons_word_in_validate_and_the_baseline_that_refuses_it rows: baseline pc -> baseline_person; valid bare NA -> no provenance error; unreadable registry -> "unverified" | expected from: item 2, baseline_identity.decides, E-S7`
- `test: test_manual_evidence.py (same table) 2b rows: baseline_contract "x"; runtime_before "x"; runtime_after 5; a 1 MB string; a nested list -> the type sentence, no exception, value never echoed; runtime_before None -> today's sentence; mismatching revision -> both revisions and "Capture again" | expected from: item 2b, FR-1, E-k3.5`
- `test: test_environment_preparation.py (the provenance_validation rows, builder greps) rows: receipt person_confirmed -> provenance_ok False; valid matched + both equalities -> True | expected from: item 5, F1`
- `test: test_manual_capture.py::n2_k8_... rows: valid bare NA refused; valid no_changed_file taken | expected from: item 4, F-k2 (a)`
- `test: test_manual_evidence.py (validate_manual_current rows) rows: local-source valid bare NA admitted; invalid NA refused | expected from: items 1, 3, AR-19`
Pins that move: F1 `:709-710` -> `home["environment_preparation.deploy_proof"] == "provenance_acceptance"`; NEW check
`home["baseline_identity.capture"] == "provenance_acceptance"`; C3-g's `:708` unedited; list `:711-714` + both; loop
`:717-725` on three pairs (C3-g's unedited; the new two check `` f"gate row `{rid}`" ``); `:715-716` unchanged. K-N2.12 NEG
second case on `baseline_identity.capture`; K-N2.12 callees -> `acceptable` for `stand_probe`, `_provenance_errors`,
`validate_manual_current`, + `validate_baseline_record`, `_run_step`; g7 `:273-278` and K-T1.2 NEG `:330-331` lose `_run_step`
per measurement; allow pin +4 (§7); D13 measured.
Edges: E-k3.1 POSITIONAL: the NA sentence :86 stays before the predicate (INV: one sentence per refused probe). E-k3.2 a
person's word never stands in for the old build (tokens; the sentence still says why). E-k3.3 manual capture tightened: a
bare NA is refused already (INV: no probe refused today is taken after). E-k3.4 deploy proof: `matched` only (INV: a word
never replaces the deploy's proof). E-k3.5 outside input (hand-written record): non-object block -> named error, read as
`{}`, only the type named (INV: a malformed baseline is a named refusal, never a crash or a pass; no value echoed). E-k3.6
pair non-dict block + missing-field loop: `"x"` is truthy, only the type sentence fires (INV: one sentence per fault).
E-k3.7 TEMPORAL: base still holds `provenance.baseline` -> stop, remove nothing (INV: after k3 both baseline consumers exist
with their F1 pins).
architecture: `AR-13 -- manual side through the predicate`; `AR-15 -- local-source copies wired`; `AR-19 -- capture and record, one rule`; `AR-22 -- two consumers with readers, the dead one leaves`; `AR-9 -- the revision refusal has a door`; `AR-20 -- allow pin +4, D13 named`. judgment: `none -- a data join and shape refusals`.

## §6. Step k4 — RD1-14d: the conversion

given: as k3 + merged k1-k3; `P/scripts/profile_contract.py:877-925,1065-1110`; the test windows named in §6 items and pins
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/profile_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_build.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_execution_request.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_runtime_probe_onboarding.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_role_commands.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
non-goals: any site's acceptance logic (k2, k3); `gate_template.py`, `gate_registry.py`; `design/factory-rules-debt.md` (S1b, RD1-23); quarantined `test_profile_contract.py`, `test_launch_wrappers.py`; prose outside owns (a report line per hit)
handoff: report path given by the Lead
edges: E-S1-E-S8, E-k4.1-E-k4.5
DoD: `--check` exit 0, no debt block, no F-b line on a provenance site; the control (`new`, `recast`, `bad`, all consumers); `N(test_execution_request: r=T.base_request();T.n2_k1_probe_runtime_is_the_one_predicate(r);T.c3_k1_one_producer_names_the_provenance_word())`; `N(test_gate_registry: T.part_live_registry();T.part_fix_pass();T.part_site_attribution();T.part_predicate())`; `N(test_runtime_probe_onboarding: <the functions holding :823, :1277, :1389>)`; `not run locally:` line incl. `test_judgment_census.py`, `test_role_commands.py`
siblings: axis 5 prose twins (`references/execution-lifecycle.md`, `references/manual-evidence.md`, `references/environment-preparation.md`, `skills/qa-story/phases/s5.md`, `s6.md`: Grep the old names, a line per hit); prose `runtime_probe.py:57`, `gate_registry.py:42`
designer: this file (k4)

1. Row: `converted`, `debt_ref: ""`, `vocabulary: code`, `field: null`; `decides` names the producer, the predicate, each
   consumer's tokens in words and "an unknown is asked as the stand_identity build question at the stage entry; every accept
   site refuses with that door".
2. F-1 (a): `acceptable_provenance`, `ACCEPTS` and the registry site `profile_contract.acceptable_provenance` are deleted.
   Readers: `driver_stage_build.build_outcome` :390 -> `acceptable(profile_contract.provenance_word(record, rehearsal=True),
   "provenance.rehearsal")` (point-of-use import); `test_execution_request.py:682-686` -> inline form with `provenance.run`,
   the `ValueError` row -> "an unknown consumer is False"; `test_runtime_probe_onboarding.py:823, :1277, :1389` -> inline
   (`provenance.run`; matched-only -> `environment_preparation.deploy_proof` with a comment why; `("matched","person_confirmed")`
   -> `provenance.identity`); `test_role_commands.py:964` `PC.ACCEPTS[:2]` -> literal `["matched", "person_confirmed"]` with a
   comment naming `provenance.run`.
3. `refusal_text`: when `gate_template.registry_problem()` is non-empty, return `registry_why(problem, f"the probe's answer
   was not judged (it said: {text})")`; else today's text.
4. `judgment-census.json:830` leaves only if `test_judgment_census.py` names it gone; otherwise stop and ask.
- `test: test_execution_request.py::n2_k1_probe_runtime_is_the_one_predicate rows: valid declared unknown -> refused, nothing runs; unreadable registry + valid matched -> refused, text holds "the gate registry cannot be read (" and "the probe's answer was not judged" | expected from: FR-59, FR-41, item 3`
- `test: test_gate_registry.py::predicate_cases live-record -> False (field null) | expected from: F-k1 (a)`
Pins that move: `EXPECTED_DEBT = {}`; `EXPECTED_CONVERTED` +1 with an AR-20 comment; `:263` -> `check_not_in("left as debt",
...)`; split counts `:355-370` converted +1, debt 0; F4 `code` list `:811-820` +1; K-N2.12 positive control `:298-299` ->
`provenance_word` calls `validate_runtime_provenance`; F2 live check `:770` -> the `profile_contract.py` `<module>` item of
`PROVENANCE_RESULTS` (none left: stop and ask); D13 measured (the `acceptable_provenance` and `ACCEPTS` items leave).
Edges: E-k4.1 TEMPORAL: from this commit each accept site needs a literal `acceptable` and each literal an allow; a site still
flagged is a stop (INV: `--check` green). E-k4.2 field null: a whole record is False (INV: no unvalidated record accepted).
E-k4.3 the last debt row: `--check` prints no debt block, `--json` `"debt": []` (INV: an empty debt list is a state, not an
error). E-k4.4 stories in flight: older records judge the same (INV: frozen = `new` = `recast`). E-k4.5 deleted names: Grep
`acceptable_provenance|\bACCEPTS\b` over `P/scripts/*.py` and keep tests = prose (control before: `profile_contract.py:877`)
(INV: no import of a deleted name survives in a keep or package file; quarantined readers get the report line, F-r2-2 (a)).
architecture: `AR-13 -- one road to the word`; `AR-15 -- the old composition deleted`; `AR-16 -- registry_why`; `AR-28 -- unknown refused and said`; `AR-29 -- a census unit leaves`; `AR-20 -- debt 1 -> 0, D13 named`. judgment: `none -- the row converts; acceptance stays a data join`.

## §7. Q4 — readers, siblings, ratchets, pins

No `tools/owns_readers.py` block came with the brief: the Lead runs it per dispatch (`--paths <the step's owns> --names
provenance_word,local_source_request,acceptable_provenance,ACCEPTS,rehearsal_probe,refusal_text,_observed_identity`). Hand Grep
-i over `tools/`: 0 code readers (every hit is the word "accepts", which proves the call works).

| touched file (step) | other readers | verdict |
|---|---|---|
| `references/gate-registry.json` (k1-k4) | `gate_registry.py`, `gate_template.py`, `test_gate_registry.py`, `test-layers.json` gate_named rows (keyed by `test`), `tools/source_split.py` carriers (r2 §9) | `test` field unchanged; pins per step |
| `scripts/profile_contract.py` (k1, k4) | the §0 sites; `driver_stage_build.py:390`; `test_execution_request.py`, `test_runtime_probe_onboarding.py`, `test_role_commands.py:964`, `test_gate_registry.py`; quarantined `test_profile_contract.py` (12), `test_launch_wrappers.py` (2); `judgment-census.json:830` | sites in k2/k3, deletion in k4 |
| `execution_request.py::rehearsal_probe` (k2) | `gate_preflight.py:3502`, `test_gate_preflight.py:4251-4253, 4324`, `test_launch_wrappers.py:168` (positional: unaffected) | changes in k2 |
| `gate_preflight.py::_observed_identity` (k2) | `onboarding_probe.py:331` (override), `_reporter_outcome` :3919 | signature unchanged |
| `tests/test_gate_registry.py` (k1-k4) | `tools/source-split-carriers.json` (D13 triple carrier) | triple form unchanged |
| prose hits new since r2 | `test_brief_pack_roles.py:405`, `test_no_move_seam_k4s.py:252` ("ACCEPTS" as a word) | unchanged |

Ratchets and pins: D13 set and `D13_ITEM_COUNT` (every step); allow pin `test_gate_registry.py:314-321` — k2 +3
(`checked['result'] == 'not_applicable'`, `provenance.get('result') == 'person_confirmed'` after the seed;
`runtime.get('result') == 'person_confirmed'`), k3 +4 after them (`probe.get('result') == 'not_applicable'`,
`checked['result'] == 'person_confirmed'`, `probe.get('result') != 'not_applicable'`, `probe.get('result') == 'not_applicable'`),
then the test_identity entries unchanged; F1 list (k2, k3); K-N2.12 (k2-k4); split and F4 (k4); `tools/lint-baseline.json`
UnusedImport (k2-k4); judgment census (k4). Told-ratchet (`stage-joints.json` `told_ratchet`) and contract slices: unchanged
(no card, joint, question or slice text added). `test-layers.json`: no new file, no `covers` change.

## §8. Q5 — forks (returned; steps execute only after the Lead decides)

- **F-1 — RD1-25 makes r2's pass-through consumers a finding.** `_consumer_problem` (:426-444, landed after r2) refuses a
  converted accept site whose `acceptable` call names a variable consumer: r2 k2 `rehearsal_probe(spec, consumer=...)` and r2
  k4 `acceptable_provenance(record, consumer, ...)` (an `accept` site, :54). (a) **Recommended**: literal consumers only —
  `rehearsal_probe` keeps `provenance.rehearsal` inside, `_observed_identity` judges `provenance.identity` itself (same result
  on every record: `""` for ncf and unknown, as today), k4 deletes `acceptable_provenance`/`ACCEPTS` and readers inline the
  form. Cost: three keep-test readers rewritten; quarantine-watch reds for `test_profile_contract.py` (F-r2-2 (a) class). (b)
  Keep both as pass-throughs re-roled `library`: no finding, but two consumers escape the scan and two roads reach one
  predicate (P31). (c) Exempt them in `_consumer_problem`: edits `gate_registry.py` (outside the row's files) and breaks
  RD1-25's invariant.
- **F-2 — the test budget (owner 18.11.2026) vs r2's committed matrix §2.4.** (a) **Recommended**: the matrix lives in the
  uncommitted control; each step commits its strongest lines. Cost: the matrix is proven by the witness script per step, not
  by the canon. (b) Commit it; the Lead names `--tests-over` at each merge.
- **F-3 — r2's DoD lines are refused today** (`--witness-for`, >3 whole files, slow files run whole; `tools/dispatch_manifest.py`,
  TESTING.md :103-106). Rewritten here, no design weight; listed so no step is dispatched from r2.
- **F-4 — `question_kind` / `policy_file` of this row.** (a) **Recommended**: stay null; `decides` names the stand_identity
  question (one carrier; no code reads the fields: Grep `get("question_kind")|["question_kind"]` over `scripts/` hits only
  `run_counters.py`, another meaning). (b) Copy `stand_identity` / `records/stand-identity.json` here: machine-readable, a
  second carrier of one question (AR-13).
- **F-5 — the builders' document.** (a) **Recommended**: this file is the `designer:` line of all four; r2 stays the
  decision record. (b) r2 stays the card, this file its erratum (two documents per builder).
- **F-6 — card text vs main: where the deploy consumer sits.** Cards spec :1363-1367: "under a row whose `promotable` is
  false"; `acceptable` reads the words of the row holding the consumer, and row `environment_preparation` has no `matched`
  word, so a consumer there accepts nothing. (a) **Recommended**, as the Lead decided in F-k6 (a): under
  `provenance_acceptance`, the prefix inheriting `false` (`gate_registry.py:795-808`). (b) Add provenance words to row
  `environment_preparation`: rewrites C3-f's converted row.

## §9. Small choices closed

Pins first, not behaviour lines; the k1 table name; narrow calls exit via `harness.finish` (`harness.py:225-229`), pytest ids
for `test_gate_preflight.py`; the control by one-hop pointer (R11-m); `test_manual_evidence.py`, `test_environment_preparation.py`
run whole (no `slow_tests.json` key), `test_manual_capture.py` is a key (8.0 s): narrow; owns space-separated on one line.

## §10. Reading trail

Main: cards spec :1330-1377, :550-575, :1926-1936; finding (whole); pile `batch-1-phase-2.md:1-60`; r2 (whole, windows);
`reviews/t-1092-...:1-30` + Grep C3-k; `gate-registry.json:1-110, 370-400`; `gate_template.py:1-107`;
`gate_registry.py:40-130, 205-310, 420-470, 630-740, 835-850, 880-924` + Grep `left as debt`; `profile_contract.py:700-939`;
`execution_request.py:140-219, 2475-2534`; `run_suite.py:920-944`; `gate_preflight.py:3480-3540` + Grep;
`probe_by_code.py:2876-2895`; `manual_capture.py:1645-1690`; `manual_evidence.py:60-139, 662-696`;
`coverage_contract.py:835-869`; `execution_fingerprint.py:104-138`; `environment_preparation.py:378-405` + Grep;
`driver_stage_build.py:300-351, 375-431`; `runtime_probe.py:40-64, 1290-1314`; `stand_identity.py` Grep;
`test_gate_registry.py:36-75, 265-339, 690-735, 1020-1260` + Grep parts/pins; Grep of defs in `test_execution_request.py`,
`test_gate_preflight.py`, `test_manual_capture.py`, `test_manual_evidence.py`; `slow_tests.json:1-12` + Grep; `test-layers.json`
keys/rows; `harness.py:225-229`; `docs/TESTING.md:75-148, 213-250`; `design/architecture.md:33-72`. Greps with controls:
provenance consumers, `gate_template` callers, `acceptable_provenance|ACCEPTS` over tests, the r2 names (0; control 7),
`tools/` readers, told-ratchet. Not established (no shell): every D13 delta; whether the dict display in `_run_step` (:397) is a
counted item; the frozen vector; whether `test_judgment_census.py` names the census row — each a builder measurement with a stop.

## Lead decisions (18.11.2026, Lead 501cb4e0, «решила сама»; before the plan critic)
- F-1 (a): literal consumers only; k4 deletes `acceptable_provenance`/`ACCEPTS`, readers inline the form; the three keep-test
  readers are rewritten in their step.
- F-2 (a): the matrix lives in each step's uncommitted control (witness script attached in full with its negative control);
  each step commits its strongest lines within the test budget.
- F-3: noted; no step is dispatched from r2.
- F-4 (a): `question_kind` / `policy_file` stay null.
- F-5 (a): this file is the `designer:` line of all four steps; r2 stays the decision record.
- F-6 (a): the deploy consumer sits under `provenance_acceptance` (as F-k6 (a)).

## Lead amendments after the plan critic t-1357 (18.11.2026, Lead 501cb4e0, «решила сама»; override the step text above)
- P-1 (k1): the k1 DoD's report line is written UNQUOTED: not run locally: test_execution_request.py, test_gate_registry.py, canon judges.
- P-2 (k4): the runtime-probe part of the k4 DoD names three functions: `every_answer_leaves_one_record_and_a_rehearsal_none`,
  `k10_a_label_equal_to_head_is_matched_and_remembered`, `k13_a_person_confirms_stand_reads_nothing_and_binds_the_word`.
- P-3 (all steps): every `test_gate_registry.py` line anchor in this card is void; the dispatch and the builder point by symbol:
  the `part_live_registry` K-T1.2 / K-N2.12 block (positive control, allow pin, NEG), the `part_fix_pass` F1 block (checks,
  list, loop), `D13_ITEM_COUNT`, `part_predicate`; the registry row by its id. §7 reads "then the test_identity and
  case_rollcall entries unchanged" (the allow pin now holds 9 entries).
- P-4 (k2): pins add `test_execution_request.py` top import `from profile_contract import ACCEPTS as ACCEPTS_OF_THE_PACKAGE`,
  removed together with K-N2.5 (its only reader).
- P-5 (k3): item 6 also names `manual_capture.py`'s top import of `ACCEPTS, acceptable_provenance` (only reader: the site item 4 changes).
- P-6: the AR-15 check reads: Grep `get("target_kind") == "local_source"` over `P/scripts/*.py`; before 4 sites, after k3 the one
  in `local_source_request`. (The looser `target_kind.*local_source` also hits a run_suite.py help-table tuple: 5 before, 2 after.)
- P-7 (accepted): k4 item 3 (`refusal_text` naming the unreadable registry via `registry_why`) moves into k1, which owns
  `profile_contract.py`; its row moves with it into k1's tests. k4 keeps items 1, 2, 4.
