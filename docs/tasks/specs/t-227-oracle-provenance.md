# t-227: where an expected value comes from (P20), implementation-only claims, answered questions re-walk the ladder

Draft: designer (Opus), 2026-10-01 11:19-11:48, returned as text; placed here by Lead. Binds P20 (PROJECT.md, the owner 01.10 11:30 + 11:35): code is never an oracle; requirements silent -> a question to the person showing BEFORE/NOW; unanswered -> `unresolved`, and at the end of the run a GAP in the report, never green or red. Section 0 (Lead's fork decisions) binds. Status: critic-on-plan next; builders after t-226 (contract.py) lands — three dispatches (F21).

## 0. Lead decisions on the forks F1-F22 (11:55)

| fork | decision | why |
|---|---|---|
| F1 oracle words | (a) `ac | spec | precedent | person | unknown`, with a mapping table to the basis prefixes in vocabularies.md | one closed vocabulary; `code` is not a word (P20) |
| F2 granularity | per Then; a Then mixing sources is split | one Then, one oracle |
| F3 recognising a literal | (a) an oracle on EVERY Then — nothing to recognise (TC_015 Then 4 has no literal and must still be refused) | FR-12 |
| F4 `precedent` | (a) an oracle only when an AC/spec NAMES the parity ("same codes as update", AC-13 style) and the ref is the base revision's behaviour (`base:<rev>:<path>:<line>`); any other precedent is a question with the precedent shown as BEFORE | P20: "precedent confirmed by a person"; MR 684's own "pre-refactor 403" label was false |
| F5 word for an answered question | `person` (exists in READING_ORIGINS) with the Q ref | |
| F6 the S5 word for an unconfirmed Then | (a) NEW reason `expectation_unconfirmed` — overrides t-223 C12 (P20 postdates it): `deferred_by_decision` would print "a person's recorded decision", which is false for an open question (FR-41) | t-219's §0c C12 is amended accordingly: B10 lives here with this word |
| F7 does the gap block `delivery_ready` | NO. The gap is reported ("Left with you": the Then, the Q, before/now); delivery readiness is not held by an unconfirmed expectation — the owner's word 11:35: "пишем как пробел в отчёте". Lead's technical reading, flagged to the owner. | an unverified check is not a found discrepancy (FR-21/FR-22 govern discrepancies) |
| F8 a question raised at S4 | a designer `--raise` in question_register (the Q enters `open_questions` with before/now from the designer's reading, `from: person-needed`) | TC_015 P-multi was never in S2 |
| F9 behaviour claims | a new register section `## Behaviour claims` (register columns untouched: position-based readers keep working) | |
| F10 implementation-only | computed by code from the register (source derived + no ac_ref + all-silent matrix + observable diff:) | FR-16 |
| F11 volume (19 claims on cmp2) | grouped per surface when `before` is `absent` (a new endpoint: all its codes in ONE question listing them), per claim where before differs from now | one stop, not nineteen; the question threshold stop still applies |
| F12 developer tests inside the MR | the implementation side, never precedent | they are the same change |
| F13 readings of a before/now question | the fixed pair, in this order and with no default and no `from: code`: (a) "intended — NOW is the expected behaviour" (b) "a regression — BEFORE is the expected behaviour"; "your own wording" stays as always | P20 |
| F14 refuse missing branches | at the S3 exit (detector_main), S4's rehearsal stays as the backstop | one stop where the author can still repair (FR-7 duplicate removed by F14's wording) |
| F15 required keys | every reading letter (or `*`) plus `not_needed` | |
| F16 own wording | apply nothing; one line names Q; the row stays unanswered and the gap lands as §1 (t-225's driver may ask once later — not here) | |
| F17 where applied answers live | (a) test-plan.json written + `answers_applied {Q: letter, at}`; the builder FIRST checks the gate's `input_revision` binding (controller.py:1286-1289) and reports what the plan hash change does to it — if the gate decision would read as stale, the applier records the new hash as the decision's `applied_revision` instead of changing the plan under the decision (fork returned to Lead by the builder with the measured effect) | |
| F18 a row that becomes automate on a manual-shaped case | the automator automates its Thens per P17; no S4 rework | |
| F19 answers after gate A / after S5 started | not applied by code; a report line + a B-line | |
| F20 coverage_contract `oracle_source_ref` on an implementation-only R | B-line | |
| F21 sequencing | after t-226 (contract.py); THREE builders in this order: (1) S2+S4 validators + register section + role texts of tester/designer (t-227a), (2) S3 missing_branch + `apply_gate_answers` + the one record_by_code call + strategist text (t-227b, after t-225 lands — story_run.py), (3) readers (traceability, ledger, report_facts "Left with you") + automator/critic/rubric texts + vocabularies (t-227c) | disjoint owns; each under one dispatch |
| F22 P19 words | `test_level_rationale` presence (code), meaning the critic's | FR-47 |

### 0c. Critic-on-plan overrides (t-228, Opus, 11:55) — binding; the builder named in brackets

| # | override |
|---|---|
| C1 (t-227b) | `apply_gate_answers` runs in `record_by_code` BEFORE `--operation gate-decision`, on the same words, and adds NO top-level key to test-plan.json (any later write makes every S5+ dispatch fail "Gate A plan content changed after approval", controller.py:1967-1983 via :2374-2375); the decision then binds the patched plan. `answers_applied` lives in `work/question-answers.jsonl` (QR.record), not in the plan. |
| C2 (t-227c) | owns += `scripts/manifest_from_tests.py` (`qa_unresolved` refuses reasons outside UNRESOLVED_REASONS :684 and has no `question`/`observed` fields — add them) and `scripts/stage_guard.py:89` (the literal copy of the list); the ledger READS then_bindings (ledger.py:43-111 never does today): the new branch `not_verified:expectation_unconfirmed` goes after failed/flaky/partial/error and BEFORE `passed_green`, so TC_015 with Thens 1-3 green and Then 4 unknown never reads passed_green. |
| C3 (F7, Lead's pick) | the gap does NOT block delivery, implemented as the person-debt extension (D-0013's non-blocking precedent): coverage_contract.py joins owns (t-227c) — an obligation whose Then is `unknown` with an open question is `unresolved` AND classed person-debt, not "blocking unresolved oracle" (:385-387, check_delivery.py:895-903); K1's fixture sets OB-15 to `unresolved` (R-19 is implementation-only — the false `resolved` is exactly F20, done here in the owned file). The owner may overturn F7 with one word. |
| C4 (t-227b) | `missing_branch` skips settled questions (`settled_question`, planning_contract.py:635 — a Q answered at an S2/S3 stop, story_run.py:1769-1813); the applier strips the applied Q from `question_refs` and `if_answered`. |
| C5 (t-227b) | ONE patch resolver: gate_brief `_patch_for` (:810-821, merges `*` with the letter) and `resolve_patch` (:503-515, replaces) are unified into `planning_contract.resolve_patch` with the MERGE semantics (`*` then the letter), and gate_brief calls it; a test pins both callers on `{"*":{disposition},"a":{reason}}`. |
| C6 (t-227a + c) | an `unknown` Then whose question is `answered` counts as `person` AT READ TIME (FR-16; no edit of the approved case after gate A), its expected value = the matching `question_thens` reading; the critic's `invented_expectation` reads the same resolver. |
| C7 (t-227b) | a missing-branch finding passed by the person's word at S3 is honoured at the S4 rehearsal: the waiver is recorded for S3 AND read by gate_preflight :1143 for `question_branches` findings (match by the row id + Q), or the S3 waiver is copied to S4 by the applier — the builder picks the cheaper and says which; FR-7 holds. |
| C8 (F4 text) | AC-13's parity is a RELATION with the post-change PUT of the same MR (F12), not the base revision: its oracle is `ac:R-13` with no literal (the Then asserts "same code as PUT", read live); `precedent` with a `base:` ref stays only for a parity an AC names against OLDER behaviour. Measured: P-multi is 403 guessed before, 400 now (manifest :1627). |
| C9 (F13) | the pair's `from` values: a new READING_ORIGIN `claim` (contract.py:201, owned) for both readings — (a) "intended: the behaviour now is the expected one" `from: claim` (NOW shown as data, never `from: code`), (b) "a regression: the behaviour before the change is the expected one" `from: claim`; when `before: unknown`, reading (b) reads "the behaviour before the change — unknown; say what it was" and the person's own wording is the door. |
| C10 (edges) | cutoff value `2026-10-02` by day (grammar.py:258) — every cmp2 artifact (01.10) stays legacy; `ac_ref` written as `—` counts as empty; an R with no matrix row counts as all-silent; letter branches also patch `coverage_obligations[].oracle_status` (else coverage_contract:382 never verifies them); test-plan.md is re-rendered after the json changes (the conditional cell). |
| C11 (tests) | K2 controls: R-27 (matrix not silent), a derived row WITH `ac_ref`, a derived row whose observable is not `diff:` — each must NOT be a claim; K1: an `unknown` Then without `question_thens` -> refused; the doc-witness keys of test_oracle_provenance.py are listed VERBATIM in this spec before the run (builder-rules: the builder quotes them from §1/§2/§3 "Role text" lines and adds the negative control). |
| C12 (class) | do now in owned files: the plan's `oracle` field (validate_artifacts.py:1400) and the case `basis` (TC_015:13) may not name an implementation-only R; queued: the bug `violates` field and S6 `expected` (manual_evidence.py:413). Per-builder owns (F21): contract.py -> t-227a only (c reads it); artifact-contract-plan.md -> t-227b only; test_oracle_provenance.py -> created by t-227a, extended by b and c in their own sections (append-only); t-227c owns traceability, ledger, check_delivery, coverage_contract, report_facts, manifest_from_tests, stage_guard, automator/critic/rubric/vocabularies texts. |
| facts | F0.6 corrected: TS-12 is R-14; R-17 is TS-10. Drifted lines: record_by_code :5787, `_case_rows` :1030, stage_scope :1623, the input binding :1304. F0.7 adds `take_question_answer` (an S2/S3-stop answer path) to the readers of question answers. |

Analogs queued (backlog, Lead): gate_brief `_patch_for` twin of `resolve_patch` (now unified by C5); judge_code.py reads then_bindings (the builder of t-227c checks it tolerates the new reason); the FR-13 house pattern (words in contract.py beside READING_ORIGINS) as a debt line; a P20 line in design/factory-rules.md (mechanism commit by Lead).

### 0d. Critic of a+b (t-254 on t-245/t-246, Opus, 16:55) — fit_with_fixes; Lead's decisions; one fix builder

The P20 chain traced on the cmp2 TC_015 shape: the dishonest paths are refused (register without a
claim row; `ac:R-19`; `basis: requirement:R-19`; a Then with no entry) and the honest path runs
(`unknown/Q7` → `Q7: a` → the resolver reads `person`). FOUR breaks, all fixed by one builder (own id;
owns contract.py, gate_brief.py, planning_contract.py, validate_artifacts.py, question_register.py,
exit_gate.py (the S2-exit re-run only), gate_preflight.py (the two card lines :2681/:2711 only),
qa-case-designer.md (`raise_questions`), the S4-exit re-pin step that applies approve_with_fixes
(critic_rollcall.py `--apply-fixes` or its caller — the builder names it), their tests):

- **O1 (P20 leak after an answer — before the run)** contract.py:431-440 treats ANY `answered` as
  confirmed: Q7 answered `b` (a regression) or in own wording makes `ac:R-19` legal again. Fix: a claim
  is confirmed only when reading = `a` ("the behaviour now is the expected one") and
  `changed_since_answer` is not True; `b` keeps the R unconfirmed with the person's value as the
  oracle (`person`, Q7) — the literal of the implementation never returns.
- **O2** contract.py:609-618 — `Q7: b` with `before: unknown` settled `person` on the designer's
  placeholder (FR-41). Fix: stays `open` with "the person's value for before is needed".
- **O3** gate_brief `_question_card` (:984-1014) prints question/source_says/readings only — the
  person never sees before/now. Fix: render `before the change: <value> — <where>` and `now: <value> —
  <where>`.
- **O4 (who runs `--raise`, decided)** the designer (no Bash) writes a one-line `raise_questions`
  entry per Then and `then_oracles` uses the ref `raise`; the validator accepts `raise` only paired with
  that entry; the S4-exit step that already applies approve_with_fixes and re-pins calls
  `question_register.raise_question`, rewrites `raise` → Q-n, drops the block, re-pins; the gate A
  rehearsal refuses any leftover `raise`; raises keyed by (case, then) — no duplicates. Invariant: no
  `unknown` reaches gate A without its Q; no case edited after gate A (C6).
- **O5 (temporal gap — before the run)** `exit_gate.collect_errors` (:458-474) re-validates JSON files
  and cases, never the register → a register written before the readiness file never has its Q ids
  checked. Fix: `check_behaviour_claims` re-run at the S2 exit.
- **O6 (FR-12/FR-9 — the owner's condition)** planning_contract.py:778-797 matches the SUBSTRING
  `accept as blocked` and blocks every case id on the line: "TC_014: do not accept as blocked" blocks
  TC_014; "TC_014: accept as blocked; TC_015 runs" blocks TC_015 too; the card's own words "TC_014:
  accept them as blocked" (gate_preflight.py:2681, :2711) apply NOTHING. Fix: a whole-line token
  `<case id>: accept as blocked` (short id allowed), a case-decision value in `QR.parse_choices`, one
  case per line; the cards print exactly that form per case; the row carries the card's partitions
  (the TC_014 card names 2 of 4 — a whole-case row would lose P-unknown/P-owner); cmp2 answers line 20
  (prose) becomes the negative fixture: one printed line naming the form, nothing applied.
- **O7 (remedy, decided)** derived from the case's precondition items behind the card: `kind` by the
  item kind (feature_flag→flag, data→data, account→credential, env→credential, service→service),
  `where` = `<case> preconditions <PC ids>`, `change` = the item's `what`; no new REMEDY kind.
- **O8** :810 "so there is nothing to block" is false for a manual-agent row (the S6 agent will try
  it) — reword; the S6 reader is t-250 B1's.
- **O9** `_rerender_plan_cells` (:482-528) rewrites only disposition + reason while the patch keys
  include `level`/`fit` (md columns) → md/json diverge (E-13 class). Fix: every md column mapped from
  a changed key; the rule "code never edits test-plan.md" stays with ONE named exception (the gate-A
  applier, these columns, these rows, before the decision).
- **O10 (F22 is a §0 decision — do now)** a letter branch of a row with `oracle_unknown: true` whose
  only open question is Q sets `oracle_unknown: false`; a `manual-*` branch carries
  `test_level_rationale`; K3: all six fixture rows carry `oracle_unknown: true`, TS-4's a/b do not clear
  it → TS-4 also fails until repaired (the cmp2 "the answer changed nothing" class).
- **O11** the S3 tail: one summary line counting errors + conflicts + missing branches.
- **O12 (decided)** `has_branch_fields` (:188) silences a plan with no branch field anywhere → gate
  `missing_branch` on the plan's `created` ≥ ORACLE_CUTOFF instead of field presence (invariant :578
  "a story with no branch field is never refused" is thereby dated, not dropped).
- Queue: `QR._answers` counts `answers_applied` as invalid (no production reader of `skipped`);
  gate_preflight reads S4-only waivers (C7 interim on discipline — detector: an S3-waived block asked
  again at S4); the 3-line `detector_errors` tail class; `revise_plan` marking patched rows overridden.

### 0e. Critic of t-255+t-256 (t-269, Opus, 19:50) — fit_with_fixes; Lead's decisions; fix builder t-271

Confirmed by the critic: the honest chain holds end to end (`raise` → `raise_pending` → Q-n with
before/now → the card → `a` → `person`; unanswered → `qa_unresolved` → ledger
`not_verified:expectation_unconfirmed` → traceability `wait` → "Left with you" → `person_debts`);
O1/O2 resolver correct; O6 parser blocks nothing on the adversarial lines. Findings and decisions:

- **F1 (HIGH, the date gate)** `after_oracle_cutoff` counts by DAY: a run started on 01.10 switches
  OFF every dated check (validate_artifacts:215/:487/:1472, exit_gate:479, planning_contract:560,
  coverage_contract:436); an unparseable date switches them off SILENTLY. Lead: the fresh run starts on
  or after 02.10 (the owner's run is tomorrow at the earliest — no re-dating); the builder makes an
  unparseable/missing `created` a REFUSAL naming the field (never a silent off), tested.
- **F2 (MEDIUM-HIGH, must fix)** a `covered` then_binding whose instance is green on a Then the
  resolver reads `open` → traceability `pass` (then_outcome:612-635), ledger `passed_green` (:147),
  report "proven", `person_debts` empty. Only the coverage projection consults the resolver. Fix:
  `traceability.then_outcome` and `ledger.plan_row_state` treat covered-on-open-oracle as unconfirmed
  (`wait` / `not_verified:expectation_unconfirmed`) with a factory-owned reason line (a ref check,
  FR-47 holds); `_names`:448 (a case whose text does not name its OB id) covered by the same rule.
- **F3 (MEDIUM, must fix)** report_facts:419 and gate_brief.still_open:1433 read the raw `answered`
  status: `Q7: b` with before unknown suppresses "Left with you" and drops the question at gate B
  (FR-41). Fix: both use the state from `resolve_then_oracle`.
- **F4 (LOW-MEDIUM, waits for t-261 — planning_contract.py held)** `_stand_remedy` (:1461) takes every
  env/http/none item, not the card's UNMET ones (blocks partitions of a met item); the fallback writes
  kind `data` + the person's token as `change` — a guess as fact. Fix: the rehearsal's unmet items,
  kind per item, fallback "kind not derivable" (FR-41). → the manual-topic follow-up after t-261.
- **F5 (LOW)** `_raise` (:694) returns the old row for the same (case, Then): a re-raise with a new
  before/now is silently dropped → refuse it naming the existing Q; `claim_confirmed` treats a record
  with NO hash (`None`) as confirmed → unconfirmed; the applier stores the hash at apply time (:1419),
  not the card's — the card's hash. Fix in t-271 (question_register.py, contract.py, gate_brief.py).
- **F6 (LOW)** a token inside a fenced block (or after an unclosed fence) applies nothing and prints
  no line (:1492) → one line "a decision inside a code block is not read". t-271.
- **D2** a whole-case `unresolved[]` row carrying the word is refused by manifest_from_tests:721;
  through manifest_put with `judge_form` on it could remap to `deferred_by_decision:judge` and hold
  delivery → add the word to `contract.UNRESOLVED_REASONS` and the five readers (judge_form:48,
  role_digest:81, check_delivery.completeness_reasons, validate_artifacts.check_manifest_v0,
  stage_guard) — t-271. **D3** FR-13 debt line for `ledger.EXPECTATION_UNCONFIRMED` — Lead at
  integration. **Axis 4**: the P20 FR line (factory-rules.md has no "oracle") + the debt line — Lead's
  mechanism commit. judge_code not checked by the critic → a scout question for the manual-topic pass.
- Plus from t-263 (B3) D5/D6, same builder: a VALID manual-agent pass record makes its R proven in the
  traceability appendix (FR-10 with the "Checked by hand" block); the `prepare` refusal door must not
  name the code word `semantic_reopen` or raw `work/` paths in a person-facing line (FR-6,
  REPORT_FORBIDDEN) — `manual_evidence.prepare` texts.

## 0b. Facts (read in the carrier by the designer; line numbers as of 01.10)
- F0.1 TC_015 (`...\work\test-cases\workflow-visual-diff\TP1-15045_TC_015.md`): Given :26 says the codes come "from the pre-refactor contract" and that P-multi gets "the code of the check order the owner confirms". Then 2 (:36) is the literal `403`. Then 4 (:38) is "equal to the expected value" and has NO literal. The residual gap :50 says "P-multi expected code needs owner". No question id, no `question_thens`. Basis `requirement:R-19` (:13).
- F0.2 The manifest (`automation-manifest.json:1625-1630`) records TC_015 P-multi as `contradicts_requirement`, "expected 403 ... owner-unconfirmed". `s5-notes.md:2`: "P-multi expected 403 is an invented value".
- F0.3 Register header :13 `R | Requirement | source | derived_from | verifiable | ac_ref | observable | impact`. R-17 (:31) is `derived`, no ac_ref, observable `diff:`, "autonomous mode 403"; matrix row :75 `silent|silent|silent|n/a`. R-16 :74 and R-19 :77 the same. 19 derived rows have an all-silent matrix: R-16..26 and R-29..36. R-27/R-28 carry `contradicts`.
- F0.4 `impl-diff-testproject1-backend.txt:984-1016`: the 403 raised INSIDE `try` (:989-995), `except Exception as e:` at :1009; the status of the re-raise is NOT in the hunk (boundary :1015). "before = 400" needs the base revision; the removed lines alone do not show it.
- F0.5 Questions live in `requirements-readiness.json` `open_questions`: Q1-Q6 (:63-226), none about PUT/validate codes. Reading (a) of Q1, Q3, Q4, Q5, Q6 is `from: code`. `contract.READING_ORIGINS` (contract.py:169-170) holds `code`, `test`, `precedent`, `person`.
- F0.6 Plan rows with `question_refs` but no `if_answered`: TS-1/Q3 (:2), TS-3/Q2 (:4), TS-6/Q1 (:7), TS-11/Q5 (:12), TS-13/Q6 (:14) — FIVE rows. TS-4 (:5) has `{"Q4":{"a":{automate},"b":{manual-agent}}}` and no `not_needed`. TS-12 (R-17) and TS-15 (R-19) obligations are `oracle_status: resolved`.
- F0.7 Nothing applies an answer today: `planning_contract.resolve_patch`/`apply_patch` (:503-521) are called only by `variant_errors` (:668, :696) (control: `gate_brief._patch_for` :810/:907). `story_run.record_by_code` (:5404-5432) calls only `controller.py --operation gate-decision`; controller.py does not import question_register (control: story_run.py:1648). `work/question-answers.jsonl` does not exist in cmp2 (glob control: two sibling files found). After gate A, Q1-Q6 are at best `named`, never `answered` (question_register.py:22-26). `cmp2-18.log:6-9` shows only "recorded by code"; TS-4/Q4 looked applied only because answer a equals the row as authored.
- F0.8 `variant_errors` skips a row with no `if_answered` (planning_contract.py:622-624). E-19 (:679-689) checks only written branches. At the S3 exit it REPORTS, never refuses (stage_done.py:340-381); the refusal sits in the S4-exit rehearsal (gate_preflight.py:1075-1140).
- F0.9 Oracle words today: `contract.ORACLE_PREFIXES` (requirement:/external:/history:, :33); `grammar.ORACLE_RE` (grammar.py:76-78) used for the case `basis` (validate_artifacts.py:266-271); plan `oracle` (:1400-1428; `history:` banned for new behaviour); `coverage_contract` `oracle_source_ref` checks presence only (:242-244). No case Then carries an oracle; `oracle_status` exists only on plan obligations (control: `question_thens` is a per-Then key, artifact-contract.md:94-108).
- F0.10 The S5 per-Then record exists: `then_bindings {case, then, instance_id, assertion_ref, status covered|unresolved, reason?, detail?}` (artifact-contract-automation.md:57-62); traceability reads it per Then (traceability.py:536-563). A `deferred_by_decision:*` reason prints `deferred` (:58, :496-499); the ledger prints `deferred_by_decision` (ledger.py:38-56) and it blocks delivery (check_delivery.py:883); `not_verified:<x>` does not block.

## 1. ORACLE PROVENANCE (S4 cases, S5 manifest, the code critic)
- **Rule.** Every Then names where its expected value comes from: `then_oracles: [{"then": n, "source": <word>, "ref": <R-n | base:<rev>:<path>:<line> | Q-n>}]` — ONE front-matter line of JSON, the form of `question_thens`. Words: `ac`, `spec`, `precedent`, `person`, `unknown` (F1, F4, F5). `code` is not a word. `ac`/`spec` with ref R-n are valid only when R-n is NOT implementation-only (§2) or its behaviour claim is confirmed. `unknown` needs a Q-n in `open_questions` that shows before/now, and an entry for the same Then in `question_thens`.
- **Required behaviour.** The designer writes one entry per numbered Then (F3); a Then mixing sources is split (F2). The automator binds by Then: for an `unknown` Then (an unanswered question) it writes `then_bindings {status: unresolved, reason: expectation_unconfirmed, question: Q-n, observed: <value seen>}`, never asserts that value and never writes a literal; for a `person` Then it asserts the answered value. The code critic: a literal in a new or changed test whose Then has no non-`unknown` oracle is `invented_expectation`, a findings entry with `cause: test_defect`; it blocks approval. This absorbs t-219 B10.
- **Position and invariant.** `validate_artifacts.check_case` runs on write, after the `preconditions` block (:197-204), gated by a new `updated` cutoff like `check_case_form` (:206). Invariant: a case written before the cutoff is never refused (builder rule 9). Invariant: an expected value whose only source is the implementation never reaches gate A looking settled.
- **Edges.** `then_oracles` absent on a new case: refused, naming every Then number. Absent on a legacy case: silent. A Then number not under `## Then`: refused (reader `s5_precheck.then_clauses`, as gate_preflight :1064). A duplicate Then: refused. Empty/broken JSON: refused, the `question_thens` text (planning_contract.py:734-738). An `ac` ref to an implementation-only R-n: refused (a code-derived R never passes as an AC). `unknown` with a Q-n absent from `open_questions`, or `requirements-readiness.json` missing: refused (an `unknown` never travels without a door). `then_oracles` says ac:R-n while `question_thens` gives the same Then readings: refused (settled or open, never both). Error direction: code checks presence and refs only; whether R-13's text supports 403 is the case critic's (FR-12/FR-47) — the adversarial input "Then 403 with {ac, R-13} where R-13 has no 403" passes code and must be a key in the K1 doc check for the case-critic rubric. A run ends with the Then still `unknown`: traceability `result: wait`, basis "expectation unconfirmed, check not executed — Q-n: before <x>, now <y>" (`traceability.unresolved_outcome`); ledger `not_verified:expectation_unconfirmed` (`ledger.plan_row_state`); report_facts class `wait` -> "## Left with you" (report_facts.py:312): "To check: <Then>. Needed: your answer to Q-n". A run stopped before S8 writes no report; the gap stays as the open question + the then_binding. An answer after S5 wrote the binding: F19. The approved case is the S5 oracle (qa-automator.md:126) and the Then is unknown: no conflict — the case says unresolved.
- **Role text (FR-38).** qa-case-designer.md 5 and Outputs: `then_oracles` with the one-line form. qa-automator.md 8/12 and Refusals: then_bindings `question`/`observed`; "never a literal for an unknown Then". qa-code-critic.md: ONE pointer; the rule in code-review-rubric.md (t-223 C13). artifact-contract.md (case), artifact-contract-automation.md (then_bindings), vocabularies.md (oracle words, `expectation_unconfirmed`). Slices regenerated.
- **One test file per mutation.** check_case -> test_validators.py; traceability -> test_traceability_report.py; ledger -> test_ledger.py; check_delivery (F7: NOT blocking — the test asserts it does not block) -> test_check_delivery.py; role and contract keys -> test_oracle_provenance.py (keys verbatim + a negative control).

## 2. REQUIREMENTS FROM THE DIFF ALONE (S2)
- **Rule.** An R is implementation-only when all hold: `source: derived`, `ac_ref` empty, every matrix cell `silent` or `n/a:*`, observable `diff:` (code computes it, F10). Such an R is a BEHAVIOUR CLAIM, never a requirement.
- **New carrier.** Section `## Behaviour claims` (F9): `| R | before | before_ref | now | now_ref | differs | question |`. `before_ref`: `diff:-<path>:<line>`, `base:<rev>:<path>:<line>`, `screenshot:<ref>`, or `absent` (a new path); `before: unknown` when nothing can be read. A claim gets a question in `open_questions` with new keys `before {value, where}` and `now {value, where}` (contract.QUESTION_FIELDS, question_errors); its readings are the F13 pair, no default. The answer becomes the oracle `{person, Q-n}`; the plan covers the R only through a Then whose oracle is that question. Grouping per F11.
- **Position and invariant.** `check_register` runs after the matrix walk (:404-413), gated by a register `created` cutoff. Invariant: an implementation-only R never reaches S3 without its before/now and its question. Invariant: the `## Register` columns are untouched.
- **Edges.** An R that is both ac and diff (ac_ref set) is not a claim; a literal in its Then absent from the AC falls to §1's critic rule. Base revision not readable (no checkout, or the hunk cuts the line, F0.4): `before: unknown`, the question still asked saying so (FR-41). `before: absent` (new endpoint/module): still a claim, still a question (P20), grouped (F11). `differs: yes` with no question: refused. A question id not in `open_questions`: refused. An unanswered claim at the end of the run: its R row in traceability reads `wait` with §1's basis (the R-without-case branch, traceability.py ~:601-625) — never `not planned`, never pass. Developer tests in the same MR (R-29..R-36): the implementation side (F12).
- **Role text.** qa-requirements-tester.md :37-42 and :60-65 (the section, before_ref forms, "never the as-built value as the intended reading"); artifact-contract-plan.md (register shape); templates/requirements-register.md; the tester slice.
- **Tests.** check_register -> test_validators.py; question_errors before/now -> test_gate_question_form.py.

## 3. ANSWERED QUESTIONS RE-WALK THE LADDER (S3 to after gate A)
- **Rule.** A row rests on Q when Q is in `question_refs`, OR Q's id token appears in `reason` (`_id_token`, structure not a phrase list, FR-12). Such a row carries `if_answered[Q]` with a key for every reading letter (or `*`) plus `not_needed` (F15). Each letter branch of a row whose only open question is Q sets `oracle_unknown: false`. A branch that leaves or sets `manual-*` carries `test_level_rationale` naming its P19 rung and why the lower rungs do not apply (presence by code, meaning the critic's, F22).
- **Position.** New finding kind `missing_branch` in `variant_errors`, before the `_carries(branches)` skip (:622); refused at the S3 exit in `detector_main` beside `contradiction_errors` (F14). Invariant: E-19's stale-reason rule and "a story with no branch field is never refused" (:578) stay; a row that names no question and whose reason names none is never touched.
- **After gate A — the ONE call site in `story_run.record_by_code`, after a successful gate A: `planning_contract.apply_gate_answers(task_root, words)`:** (1) `question_register.parse_choices` over the words, then `QR.record(..., where="gate A", by="driver")`; (2) for each answered Q, `resolve_patch` then `apply_patch` on its rows; (3) write test-plan.json and `answers_applied {Q: letter, at}` (F17, with the input_revision check); (4) print one line per row moved. Rows that become `automate` enter S5 through controller `_case_rows`/stage-scope (controller.py:1012-1045, 1620-1647) unchanged.
- **Edges.** "not needed": the `not_needed` patch with a reason not naming Q (E-19). Own wording (no token): nothing applied, one line names Q, the row stays unanswered, the gap lands as §1 (F16). Two answers for one Q: nothing applied for that Q. A letter beyond the readings: nothing applied. A question with no readings: only `not_needed` required. A DEPENDENT pair is already refused (:706-717). A branch that moves level/disposition onto a manual-shaped case: F18. An answer after S5 started or after gate A: F19. A failure inside the applier: one printed line and the story goes on (P1); the gate decision is already recorded and never undone. Reused function in a gate role (`variant_errors` from report to refusal): it errs toward sending the strategist back, never toward passing a row that rests on Q without a branch, and never decides an answer. Adversarial inputs that must be refused: `{"Q5": {}}`; `"q5"`; only `a` on a two-reading Q; a reason naming Q5 with no `question_refs`; `Q50` must NOT match Q5.
- **Role text.** qa-test-strategist.md 2b (:67-75: every reading plus `not_needed`, `oracle_unknown: false` per letter, P19 words); artifact-contract-plan.md :65-77; the strategist slice.
- **Tests.** `variant_errors` and `apply_gate_answers` -> test_question_branches.py; detector_main -> test_s3_s4_chain.py.
- **Added by Lead 01.10 14:00 (from critic t-238, FR-9 sibling of t-218 C2).** `apply_gate_answers` also
  executes the gate A stand cards' answers that today have no S5 reader: `accept as blocked` on a
  per-case card or on the `none` card (gate_preflight.py:2641/:2671 promise "S5 then reports exactly
  these as not executed") → `unresolved` rows with `reason: blocked_by_env`, the card's reason as the
  remedy text and `instance_ids` empty (filled by the automator per t-219), written at S5 start through
  `manifest_put` so the automator never runs them; `<case id>: manual` → the row's disposition `manual`
  as the per-case card already defines. The same proposal_hash/record rule as the question answers
  (recorded in `work/question-answers.jsonl`, never a plan key — C1). Test in test_question_branches.py:
  the cmp2 gate A answers file (`experiments/cmp2-15045/answers/cmp2-s4-gate-a.md`) → TC_014/TC_017
  rows blocked_by_env, TC_004/TC_008 untouched (they were answered later, in S5).

## Acceptance keys (cmp2 copied verbatim into fixtures)
- **K1.** TC_015 with no `then_oracles` is refused, naming Then 1-4. With `{"then":2,"source":"ac","ref":"R-19"}` refused because R-19 is implementation-only. With Then 4 `{"source":"unknown","ref":"Q7"}`, Q7 in the readiness fixture with before/now plus `question_thens`: accepted. A then_binding for Then 4 with `expectation_unconfirmed` renders traceability `wait` and the ledger `not_verified:expectation_unconfirmed`; never `deferred`, never pass or fail; `delivery_ready` is NOT held by it (F7).
- **K2.** The register (:13, :31, :75) is refused: "R-17 is implementation-only and has no behaviour claim". With `before: unknown` (F0.4) or `400 base:<rev>:workflow.py:<n>`, `now 403 diff:+...:158`, `differs: yes`, and `Q7`: accepted. R-1 (ac) is the negative control, never refused. A grouped question for a new surface (F11) counts as one question for the threshold.
- **K3.** The plan rows :2-14 with Q1-Q6 fail the S3 exit with `missing_branch` for TS-1/Q3, TS-3/Q2, TS-6/Q1, TS-11/Q5 (a, b, not_needed) and TS-13/Q6, plus TS-4/Q4 not_needed. After repair, `apply_gate_answers` with `answers/cmp2-s4-gate-a.md:1-8` records Q1-Q6 as `answered` and moves TS-11 by its Q5:a branch; TS-4 stays automate; the gate decision's input_revision effect is reported (F17).

## DoD (cwd ai-packages/qa-factory; each builder runs the files of its sections, the full list once at the end of t-227c)
`python -B scripts/tests/test_oracle_provenance.py`; `test_validators.py`; `test_question_branches.py`; `test_s3_s4_chain.py`; `test_gate_question_form.py`; `test_traceability_report.py`; `test_ledger.py`; `test_check_delivery.py`; `python -B scripts/contract_slices.py --check`; `python -B scripts/selftest.py --limits --lang`; `python -B scripts/tests/test_audit_rules.py`; the neighbours once at the end (builder-rules 7).

## owns (D:/ws1/yml-text-factory\ai-packages\qa-factory\ + …)
Code: scripts\validate_artifacts.py, scripts\planning_contract.py, scripts\contract.py (after t-226), scripts\traceability.py, scripts\ledger.py, scripts\check_delivery.py, scripts\question_register.py (the `--raise` of F8), scripts\report_facts.py ("Left with you" line). story_run.py: only the one call in `record_by_code` (t-227b, after t-225). References: artifact-contract.md, artifact-contract-plan.md, artifact-contract-automation.md, vocabularies.md, code-review-rubric.md, templates\requirements-register.md, slices\** (regenerated). Charters: qa-requirements-tester.md, qa-test-strategist.md, qa-case-designer.md, qa-automator.md, qa-code-critic.md. Tests: the 8 files above + test_oracle_provenance.py (new).

## non-goals
story_run.py beyond the one call (t-217/t-225/t-228); gate_preflight.py (t-218/t-224); the S5 window and s5_precheck, manifest_put, window_record, controller, acceptance (t-219/t-226/t-230); coverage_contract.py (F20); gate_brief's `_patch_for` twin (queued).

## handoff
Per builder: the diff, a FR walk line per section A-G, the verbatim DoD output, "needed beyond the manifest".

## FR walk (draft)
A. FR-1: every refusal names the Then, R or row and the expected form. FR-2: the doors are the designer, tester or strategist rework. FR-57: an informed pass by waiver stays. B. FR-6: the before/now question text follows human-questions.md. FR-7: F14 removes the duplicate stop. FR-9: the answer has an executor (apply_gate_answers). C. FR-11: every field is written by the role that is told about it. FR-12: id tokens and fields, no phrase list. FR-13: the words live in contract.py beside READING_ORIGINS (house pattern; a debt line). FR-38: role text above. FR-42: the move for own wording. D. FR-16: implementation-only computed at check time. FR-40: a gap has a way out (the answer). E. FR-20, FR-35, FR-41: unknown stays unknown, never `deferred`. F. n/a. G. FR-32: a test per fix. FR-47: code checks presence and refs, roles judge meaning. FR-54: the axes.

## SIBLING_MAP axes
1 n/a (package, not policy). 2 n/a. 3 queued with the release. 4 covered: P20 mirrored as an FR line (Lead, mechanism commit) + a debt entry for the FR-13 house pattern. 5 covered: designer/case-critic and automator/code-critic get the same oracle word; the question chain's gate_brief `_patch_for` twin queued. 6 n/a. 7 n/a.

## Forks as returned (decided in section 0): F1-F22. Designer's small choices accepted: `then_oracles` one-line JSON; `by="driver"` and the row hash as of now; new cutoffs by `updated`/`created`; the traceability basis wording.
