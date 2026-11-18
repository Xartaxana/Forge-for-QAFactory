# RD1-32 card (draft): the S4 case critic's approving words read through one registry row

Designer draft for task t-1330, node `rules-debt/1/RD1-32`, feature F19. Source: Lead decision F3 of the RD1-29 card
(`docs/tasks/specs/20261117-rd1-29-review-word-one-row-card.md`, «Lead decisions»), pile row RD1-32 of
`plans/piles/rules-debt/batch-1-phase-2.md:60`. The Lead decides the forks in §3. Until then the items in §4 follow the
recommended options and say so where they depend on one.

## 0. The future builder dispatch: header lines (R11-f)

```
task: <new id at dispatch>
node: rules-debt/1/RD1-32
feature: F19
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261118-rd1-32-rollcall-verdicts-card.md
C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rd1-29-review-word-one-row-card.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_template.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py
C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/critic_rollcall.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_plan.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_critic_rollcall_apply_fixes.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
non-goals: rows of gate-registry.json other than the new `case_rollcall` (RD1-26 owns `test_identity`, RD1-28 owns `probe_verdict`, RD1-29's `critic_review` / `s5_window` stay byte-identical); `critic_rollcall.CASE_CRITIC_VERDICTS` stays a code list (its readers `role_digest`, `controller._later_refusal` and three tests are unchanged); per-word checks that are not the approving class (`_read_round` :462, `_level_errors` :1066, `driver_stage_plan.s4_after_critic` :941); `acceptance.py` / `handoffs/vocabulary.yaml` `stage_acceptance_verdicts` (fork F5); no second predicate or registry reader in production code (only `gate_template.acceptable` / `registry_problem` / `registry_why`); no new test file; no quarantined test file is run or edited (`test_carried_concerns.py`, `test_case_gates.py`, `test_case_merges.py`, `test_scoped_review_verdict.py`)
handoff: a report with the before/after numbers of `gate_registry.py --sites` (items, triples, allow entries), the witness output, the narrow-call output of each canon-judged file, and the `architecture:` / `judgment:` lines
edges: §5 of the card (E1-E12, each with its invariant)
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_critic_rollcall_apply_fixes.py` green; `python -B ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; narrow calls (TESTING.md «Что запускать»): `test_gate_registry.py` parts holding EXPECTED_IDS / EXPECTED_CONVERTED / the F4 `code` list / the allow pin / `part_site_attribution`, called by name; `controller.py`, `driver_stage_plan.py`: not run locally, canon judges
siblings: RD1-26 and RD1-28 (same file `gate-registry.json`, other rows; same pins in `test_gate_registry.py`): merge order §8 / F4; RD1-29 `critic_review` (the S5 twin, landed ee3d5db0); SIBLING_MAP axis 5 row 138 and axis "critic's word per plan row" row 157; axis 34
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-rd1-32-rollcall-verdicts-card.md
```

The owns are wider than the batch row (`critic_rollcall.py`, `gate-registry.json`, `test_gate_registry.py`): `controller.py` and
`driver_stage_plan.py` read the deleted constant (m2), so they are forced (designer rule 2); the witness file is the one fast `keep`
file that covers `critic_rollcall.py` (m11). `controller.py` is hot: the Lead checks the zones of batches in work (rule 4, F4).

## 1. Measured facts (read from the carriers 18.11.2026)

| # | Fact | Carrier |
|---|---|---|
| m1 | `APPROVING_VERDICTS = ("approve", "approve_with_fixes", "approve_with_concerns")` beside `CASE_CRITIC_VERDICTS` (the same three plus `partial`, `reject`) | `critic_rollcall.py:43-44` |
| m2 | Readers of `APPROVING_VERDICTS`, all membership tests `in` / `not in`: `critic_rollcall._row_outcome` :251, :255; `_round_word_rule` :299; `scoped_verdict` :362; `findings_errors` :607; `_merge_concern_errors` :1007, :1009; `controller.Controller._declared_review_verdict` :3566 (import), :3571; `driver_stage_plan.DriverStagePlan.s4_limit_unknowns` :819. No reader in `scripts/tests/`, `tools/`, `.githooks/`, `.claude/agents` (§7 greps with controls) | Grep `APPROVING_VERDICTS` over the package and the repo |
| m3 | How the word reaches each site: `parse_rollcall` cells are stripped, backticks off, lower-cased (:128-129); `VERDICT_RE` is `(?im)...([a-z_]+)` so `Approve` matches, and `declared_verdict` does NOT lower (:63, :160-164); `scoped_verdict` (:347) and `s4_limit_unknowns` (:818) lower it; `findings_errors` (:585) and `_declared_review_verdict` (:3567) do not | the lines named |
| m4 | `acceptable` is case-exact, no strip, never raises; a dict value reads `value[row["field"]]`, a row whose `field` is null gives False for a dict; every doubt is False | `gate_template.py:9-13`, `:70-106` |
| m5 | Registry today: `critic_review` (RD1-29, row 273-300) has six consumers all `["matched"]`, `field: critic_verdict`, `unknown_branch: refuse_with_door`; `s5_window` (246-271) unchanged by RD1-29 except one site; `probe_verdict` (620-643) still `accepts: {}` (RD1-28 not landed); no site in `critic_rollcall.py`, `controller.py` or `driver_stage_plan.py` | `references/gate-registry.json`; Grep `"controller\.py"` 0 hits, control `"case_stamp\.py"` 1 hit |
| m6 | The scanner counts a comparison when a word is an anchor anywhere, or a word of a row's `words` inside a function that row registers; a Name assigned a token display at module level resolves to it; a bare tuple display (e.g. a `return "partial", ...`) and a Name assigned a conditional of words count too. In a converted `accept` site a counted comparison is a finding unless an `allow` entry equals it whole; `validate` sites are allowed | `gate_registry.py:21-45`, `:915-950` |
| m7 | RD1-25: every `acceptable(...)` call in a converted accept site must pass a literal consumer that is a key of its own row's `accepts`, through gate_template's own binding | `gate_registry.py:426-444`, `:898-913` |
| m8 | Pins: `D13_ITEM_COUNT = 150` (after RD1-29), the triple set, `EXPECTED_IDS` / `EXPECTED_CONVERTED` / the F4 `code` list name `critic_review`; the allow pin is an ordered list of five entries | `tests/test_gate_registry.py:38-85`, `:312-319`, `:804-817`, `:1129-1133` |
| m9 | Callers that reach the sites: `findings_errors` <- `_detector_body` :1141, `main` :1258, `validate_artifacts.py:2660` (on write); `merge_candidate_errors` <- `_detector_body` only; `current_rejected` <- `s4_limit_unknowns` :814; `accepted_rounds` <- `s5_plan._file_concerns` :1145; `scoped_verdict` <- `controller` :3611; `_declared_review_verdict` <- `_dispatch_review_verdict` :3656 | Grep of the callers |
| m10 | `_detector_body` prints `REJECT` with the person's waiver door (exit 1); a check that could not run is `DV.unreadable_line`, `DV.EXIT_UNREADABLE` (RH1-5) | `critic_rollcall.py:1122-1158` |
| m11 | Test layers: `test_critic_rollcall_apply_fixes.py` is a `keep` row covering `critic_rollcall.py`, not slow; `test_gate_registry.py` (19.7 s), `test_handoff.py` (40.6 s), `test_judgment_census.py` (96.9 s) are slow; `test_controller_*` is `canon_only`; `test_carried_concerns.py`, `test_case_gates.py`, `test_case_merges.py` are quarantine | `test-layers.json:1208-1217`, `:13-18`, `:7464`, `:7488`, `:7545`; `slow_tests.json:46, 52, 68` |
| m12 | `_declared_review_verdict` returns `"accepted"` on `ImportError, OSError, ValueError, TypeError` around `from critic_rollcall import APPROVING_VERDICTS, ...` | `controller.py:3565-3570` |
| m13 | Census rows exist for `findings_errors` and `_merge_concern_errors` (`xref`, owner data); none for the other sites | `fixtures/judgment-census.json:260, 263` |
| m14 | `handoffs/vocabulary.yaml:124` `stage_acceptance_verdicts` maps `approve`, `approve_with_fixes` to accept and has no `approve_with_concerns` | the line |

## 2. Section 1: invariants, owners, census, commit lines, variety

AR-n touched (`design/architecture.md`) and the check each demands in the DoD:

- AR-1 (closed variety is a data row): the approving class leaves code for the row `case_rollcall`. Check: Grep
  `APPROVING_VERDICTS` over `ai-packages/qa-factory/scripts` gives 0, with the positive control `CASE_CRITIC_VERDICTS` (stays).
- AR-13 / AR-15 (one reader, one survivor): every site asks `gate_template.acceptable`. Change check: SIBLING_MAP axis 5 row 138
  names "the `critic_rollcall` / `controller` readers (RD1-32)" as neighbours not converted; after the change that clause names the
  row `case_rollcall` (a doc edit for the Lead, outside owns, as RD1-29 did).
- AR-9 (a refusal names what it expected and a door): every unreadable-registry text goes through `gate_template.registry_why`.
- AR-20 (ratchets): D13 count and triples RISE (new registered sites with counted comparisons). Estimate, not verified, under F1 (b):
  +6 items (150 -> 156), +4 triples, +2 allow entries. Raised row by row in the comment block above `D13_ITEM_COUNT`, in its form.
- AR-22 (a producer and its readers change together): the row, the deletion of the constant and its two foreign importers land in one commit (E10).
- AR-28 (an unknown never becomes a pass): an unreadable registry never yields `accepted`, a clean detector, or a skipped refusal (E2).
- AR-29 (code judges data): the verdict word stays the case critic's judgment; code reads a token of a closed vocabulary through data.

Owner and census class of every check the card alters (P27, AR-29):

| Check | Owner it serves | Census class |
|---|---|---|
| `critic_rollcall._row_outcome`, `scoped_verdict` approving test | data (code reads the critic's token) | shape (no census row; none added unless the census asks) |
| `_round_word_rule`, `findings_errors`, `_merge_concern_errors` approving test | data; the verdict is the case critic's judgment, accepted at S4 by gate A | `xref` rows 260, 263 unchanged |
| `_detector_body` registry stop (new) | data | shape; a census row only if `test_judgment_census.py` asks |
| `_read_round` registry doubt (F3 (a)) | data | shape |
| `controller._declared_review_verdict`, `driver_stage_plan.s4_limit_unknowns` | data | shape |

Commit lines: the only carrier of their form is `tools/architecture_gate.py`. In that form:
`architecture: AR-1, AR-9, AR-13, AR-15, AR-20, AR-22, AR-28, AR-29 -- <how each is kept, one clause each>` and
`judgment: none -- the case critic's verdict word stays the critic's judgment; code reads its token through the registry row instead of a literal list, and no check reads a role's content`.

Variety walk (`design/architecture.md` § A): `variety: none -- the S4 case critic's verdict words are the factory's own role vocabulary, one for every project and language; no project, language or tool axis is read`.

## 3. Forks (the Lead decides; recommendations marked)

**F1 - which words the row holds (the brief's edge: "one registry row ... without changing what is accepted").** Both options accept
exactly today's three words (m1, m4); they differ in what the scanner counts (m6).
- (a) All five words of `CASE_CRITIC_VERDICTS` (three `matched`, `reject` `mismatched`, `partial` `unknown`/role), pinned set-equal, as
  RD1-29 did with four. Cost: `partial` and `reject` are returned as tuple displays and conditionals inside the two accept sites
  (`_row_outcome` :249, :259; `scoped_verdict` :333-381, :372), so about ten more counted comparisons, each an `allow` entry with a
  `why` that says "a state returned, not an acceptance"; the registry check this card adds to `_row_outcome` would itself need one.
- (b, recommended) The three approving words only, all `matched`; `CASE_CRITIC_VERDICTS` stays the code list of known words (its
  three other readers keep it). A test pins `set(CASE_CRITIC_VERDICTS) - set(row["words"]) == {"partial", "reject"}`, so a new
  critic word cannot be added to the code list without deciding whether it approves (E11). Cost: the vocabulary is split, approving
  class in data and the two refusing words in code; two `allow` entries (`row['verdict'] in CASE_CRITIC_VERDICTS`,
  `declared not in CASE_CRITIC_VERDICTS`, known-word checks).

**F2 - not a fork: closed in §9 (one consumer per site function, roles).**

**F3 - what the round reader gives on an unreadable registry.** `_read_round` reaches the approving class only through
`rejected_rows` -> `_row_outcome`; with a registry problem every reviewed row would be listed as "still rejected" with its own word
`approve` (over-list), and `s5_plan._file_concerns` would hand the automator `CR-<case>` remarks for approved cases.
- (a, recommended) `_read_round` returns its existing doubt (`silent(...)` with the `registry_why` reason) before the rows: the round
  lists nothing, `current_rejected` is None, and `s5_plan` names the file as not carried (FR-41 path, `s5_plan.py:1129-1132`).
- (b) Leave the over-list: safe for acceptance, wrong text for the automator and the person.

**F4 - merge order with RD1-26 and RD1-28.** RD1-32 shares no code file with them (they own `acceptance.py`, `run_history.py`,
`proof_level.py`); it shares `gate-registry.json` (other rows) and the pins of `test_gate_registry.py` (EXPECTED lists, the ordered
allow pin, D13 count, triples and comment block).
- (a, recommended) RD1-32 may build now. Merge order is acceptance order with RD1-26 first (in critic review); whichever of RD1-28 /
  RD1-32 merges later merges `main` and remeasures D13, the triples and the allow pin on the merged tree (batch «Порядок по общим
  файлам», TEAMWORK §3). The new row goes right after `critic_review` in the file, far from the `test_identity` / `probe_verdict` hunks.
- (b) Strict RD1-29 -> RD1-26 -> RD1-28 -> RD1-32: no remeasure race, but RD1-32 waits for RD1-28, which has not started.

**F5 - `vocabulary.yaml` `stage_acceptance_verdicts` has no `approve_with_concerns` (m14).** A second data carrier of the S4 critic's
words gives another answer: an S4 digest saying `approve_with_concerns` (a word `role_digest.py:84-89` accepts) gets no stage
acceptance record. Different gate, `acceptance.py` is RD1-26/RD1-28's file.
- (a, recommended) Not in this node: a finding for the Lead (zone of `acceptance.py`), or a scout question in RD1-33's sweep.
- (b) Widen RD1-32 to it.

**F6 - `_declared_review_verdict` turns an `ImportError` into `accepted` (m12).** The card edits that import line; a factory defect
reaching acceptance is an AR-28 road in the node's own reach.
- (a) Keep the except as it is; only the registry check stays outside it (E12).
- (b, recommended) Drop `ImportError` from the `accepted` branch: a failed import returns `partial` (the factory's own defect is never
  an acceptance, FR-59). `OSError` (the documented legacy "absent file") stays. Cost: one test row.

## 4. Builder items (numbered; each: file, function, expected behaviour, test row)

1. `references/gate-registry.json`: add the row right after `critic_review` (F1 (b), F4 (a)). Fields not named take
   `critic_review`'s row form:
   ```json
   {"id": "case_rollcall", "inventory": "RD1-32", "vocabulary": "code",
    "decides": "the S4 case critic's verdict word - a roll-call row's `verdict` cell, or the round's `Verdict:` line where the table has no such column - approves: `approve`, `approve_with_fixes` and `approve_with_concerns` approve (the row is `accepted`, gate A's design review reads `accepted`, an approving round over unreviewed rows or over a merge without its concern is refused). Every other word or none does not approve: `partial` and `reject` (the critic's other words, `critic_rollcall.CASE_CRITIC_VERDICTS`) and an unknown word, which the roll-call names as no word of the critic's list (FR-35). Case-exact: each site reads the word as it does today (`parse_rollcall` lower-cases a cell; `scoped_verdict` and the S4 limit lower-case the `Verdict:` line; `findings_errors` and gate A's fallback do not). Per-word checks that are not this class (the concern carrier, the fixes block, the level rows) are not sites",
    "sites": [
      {"file": "critic_rollcall.py", "function": "_row_outcome", "role": "accept", "allow": [
        {"compare": "row['verdict'] in CASE_CRITIC_VERDICTS", "why": "a known-word check of the critic's list (an unknown word is kept as written, FR-35), not an acceptance"}]},
      {"file": "critic_rollcall.py", "function": "scoped_verdict", "role": "accept", "allow": [
        {"compare": "declared not in CASE_CRITIC_VERDICTS", "why": "a known-word check of the critic's list (an unknown declared word is kept as written, FR-35), not an acceptance"}]},
      {"file": "critic_rollcall.py", "function": "_round_word_rule", "role": "validate"},
      {"file": "critic_rollcall.py", "function": "findings_errors", "role": "validate"},
      {"file": "critic_rollcall.py", "function": "_merge_concern_errors", "role": "validate"},
      {"file": "controller.py", "function": "_declared_review_verdict", "role": "accept"},
      {"file": "driver_stage_plan.py", "function": "s4_limit_unknowns", "role": "validate"}
    ],
    "field": null,
    "words": ["approve", "approve_with_fixes", "approve_with_concerns"],
    "verdict_map": {"approve": {"class": "matched"}, "approve_with_fixes": {"class": "matched"}, "approve_with_concerns": {"class": "matched"}},
    "accepts": {"case_rollcall.row": ["matched"], "case_rollcall.round_word": ["matched"], "case_rollcall.word_rule": ["matched"],
                "case_rollcall.findings_check": ["matched"], "case_rollcall.merge_concern": ["matched"],
                "case_rollcall.design_review": ["matched"], "case_rollcall.limit_question": ["matched"]},
    "promotable": false, "unknown_branch": "refuse_with_door", "on_no_answer": "refuse_with_door", "waits_at": null,
    "closed_by": [], "addressee": ["role:qa-case-critic"], "person_subject": null,
    "policy_file": null, "scope_keys": [], "binding_keys": [], "question_kind": null,
    "test": "scripts/tests/test_critic_rollcall_apply_fixes.py", "status": "converted", "debt_ref": "", "exempt_reason": ""}
   ```
   The `allow` texts are written in the `ast.unparse` form the builder reads from `gate_registry.py --sites`; if the scan prints another
   counted comparison in an accept site, the builder converts it or reports it (never an `allow` without a `why`).
   - `test_gate_registry.py`: `case_rollcall` joins EXPECTED_IDS (after `critic_review`), EXPECTED_CONVERTED and the F4 `code` list; the
     allow pin gains the two entries at the row's position; D13 count and triples remeasured with `gate_registry.py --sites` before
     and after, written in the comment block above `D13_ITEM_COUNT` in its own form (AR-20).
   - Test row T1 (`test_critic_rollcall_apply_fixes.py`, one parameterised table): for every consumer of `case_rollcall` and every word
     of `R.CASE_CRITIC_VERDICTS` plus `"Approve"`, `" approve"`, `"approve "`, `""`, `None`, `["approve"]`, `{"verdict": "approve"}`,
     `"\u0430pprove"` (the escape, FR-30), `"approve;reject"`, `"approved"` and a 10,000-character string:
     `GT.acceptable(w, c) is (w in ("approve", "approve_with_fixes", "approve_with_concerns"))`. The same table on an unreadable
     registry, and on an injected registry without the row: all False; without `approve_with_concerns` in `words`: that word False.
     Pin: `set(R.CASE_CRITIC_VERDICTS) - set(row["words"]) == {"partial", "reject"}` and `set(row["words"]) <= set(R.CASE_CRITIC_VERDICTS)`
     (E11), the row read through `gate_registry.load_registry` (a test is not a production reader).

2. `scripts/critic_rollcall.py`
   - Delete `APPROVING_VERDICTS` (:44); the comment above `CASE_CRITIC_VERDICTS` names the row for the approving class. Add
     `import gate_template` at module level beside the other imports.
   - `_row_outcome`: after the `not row["reviewed"]` return (:248-249), when `gate_template.registry_problem()` is non-empty return
     `("partial", "unreadable", gate_template.registry_why(reason, f"whether the case critic's word for {case} approves is not known"))`.
     `:251` becomes `word = "accepted" if gate_template.acceptable(declared, "case_rollcall.row") else declared`; `:255` becomes
     `if gate_template.acceptable(row["verdict"], "case_rollcall.row"):`. `:257` stays (allowed).
   - `_round_word_rule` :299: `row["verdict"] not in APPROVING_VERDICTS` becomes `not gate_template.acceptable(row["verdict"], "case_rollcall.word_rule")`.
   - `scoped_verdict` :362: `declared not in APPROVING_VERDICTS` becomes `not gate_template.acceptable(declared, "case_rollcall.round_word")`. No own registry check (E2).
   - `findings_errors` :607: `if gate_template.acceptable(verdict, "case_rollcall.findings_check"):`. After the verdict checks (:589-592),
     when `verdict` is non-empty and `registry_problem()` is non-empty, append exactly one line
     `f"{name}: " + gate_template.registry_why(reason, "whether the verdict approves cannot be judged - repair the package install, then write the file again")`.
   - `_merge_concern_errors` :1007, :1009: `rnd["word"] not in APPROVING_VERDICTS` / `word not in APPROVING_VERDICTS` become
     `not gate_template.acceptable(..., "case_rollcall.merge_concern")`.
   - `_detector_body`: after `if not files: ... return 0` and before the `findings_errors` loop, when `registry_problem()` is non-empty:
     `print(DV.unreadable_line(gate_template.registry_why(reason, "the case critic's verdict words cannot be judged")))` and
     `return DV.EXIT_UNREADABLE`.
   - `_read_round` (F3 (a)): first line inside `try`, when `registry_problem()` is non-empty,
     `return silent(gate_template.registry_why(reason, "which cases this round approves is not known"))`.
   - Test row T2 (same file, one table, readable registry, behaviour kept): `_row_outcome` for column words of `CASE_CRITIC_VERDICTS`
     plus `"zzz"` and `""`, and for `verdict None` with each declared word, equals today's tuples (`accepted`/`column`, the word as
     written, `partial`/`unreadable`); `_round_word_rule` for `reject` over all-approving rows gives the rule, over a `partial` row None;
     `findings_errors` on a round with an unreviewed row says the "not semantically reviewed" line for each approving verdict and not for
     `partial` / `reject`, and on `Approve` reports "outside" as today (m3); `_merge_concern_errors` refuses an `approve` row of a merged
     pair and skips a `reject` row. Built with the file's `_roll` helper (:217).
   - Test row T3 (same file, the unknown branch; unreadable registry through the `GT._READ` seam, restored after): `_row_outcome` of an
     `approve` row is `("partial", "unreadable", <names "the gate registry cannot be read">)`; an unreviewed row keeps `no_review`;
     `findings_errors` has exactly one registry line; `detector_main` on a story with an `approve` findings file prints an `UNREADABLE`
     line, no waiver door, and returns `DV.EXIT_UNREADABLE`; `current_rejected` is None and `accepted_rounds` lists nothing.

3. `scripts/controller.py::Controller._declared_review_verdict` (F6 (b))
   - The import line drops `APPROVING_VERDICTS`. `ImportError` leaves the `accepted` except: a failed import returns `"partial"`.
   - After `declared` is read and outside every except: when a non-empty declared word exists and
     `gate_template.registry_problem()` is non-empty, return `"partial"` (a local `import gate_template`, not inside the try).
   - `:3571`: `word not in APPROVING_VERDICTS` becomes `not gate_template.acceptable(word, "case_rollcall.design_review")`.
   - Test row T4 (`test_critic_rollcall_apply_fixes.py`, narrow; `controller.py` canon judges): `Controller._declared_review_verdict(root)`
     over findings files declaring `approve` -> `accepted`, `reject` -> `reject`, `Approve` -> `Approve` (kept reading), none ->
     `accepted` (legacy); `approve` on an unreadable registry -> `partial`.

4. `scripts/driver_stage_plan.py::DriverStagePlan.s4_limit_unknowns`
   - Before `critic_rollcall.current_rejected` (:814), when `gate_template.registry_problem()` is non-empty, return
     `None, (self.stage_review_exhausted(*unknown, unreadable=True, text=gate_template.registry_why(reason, f"which cases the case critic still rejects in {path} is not known")),)`.
   - `:819`: `declared not in critic_rollcall.APPROVING_VERDICTS` becomes `not gate_template.acceptable(declared, "case_rollcall.limit_question")`.
   - Test row T5 (same test file, narrow, a `SimpleNamespace` stub for `self` with `task_root` and a recording
     `stage_review_exhausted`): unreadable registry -> one seam call, `unreadable=True`, text naming the registry, `current_rejected`
     never called; readable registry, `reject` over an all-approving table -> today's seam text; `approve` -> falls through.

T1-T5 stand in the order worth writing (strongest first); the builder stops when its test lines reach its code lines and reports the rest.

## 5. Edges and their invariants

- E1 readable registry: every site decides as today for every word of T1/T2. Invariant: no word that did not approve yesterday does
  today, and the reverse; the rows of `test_carried_concerns.py` / `test_case_merges.py` (quarantine) stay green on the canon.
- E2 unreadable registry. `_row_outcome`: `partial`/`unreadable` naming the registry; `scoped_verdict`: `partial` through it;
  `_round_word_rule`: None (unreachable from `scoped_verdict` then, since no row is `accepted`); `findings_errors`: one registry line;
  `_detector_body`: UNREADABLE exit 3 before any check; `_merge_concern_errors`: reached only through `_detector_body`, so never on an
  unreadable registry; `_read_round`: doubt; `_declared_review_verdict`: `partial`; `s4_limit_unknowns`: the conductor seam.
  Invariant: an unreadable registry never yields `accepted`, an `OK` detector, a waivable `REJECT` for a factory defect, a skipped
  refusal, or a list of approved cases shown as rejected (AR-28, FR-59, FR-3). The story-level stop stays `REGISTRY_BLOCK` (unchanged).
- E3 word absent, None, `""`, a list or a dict: not approving. Invariant: the empty outcome is never approval (AR-23); a dict never
  reads a key because `field` is null.
- E4 padded or case-variant word (`Approve`, `" approve"`): each site keeps its reading (m3). Invariant: no site widens or narrows what it
  accepts in this node; `findings_errors` still names `Approve` as outside the list, `_declared_review_verdict` still returns it as refusing.
- E5 an unknown declared word (`looks_fine`): `scoped_verdict` returns it as written (:359-361), before the approving test. Invariant: an
  unknown word is never rewritten (FR-35).
- E6 a row that is not reviewed: `no_review` precedes the registry check in `_row_outcome`. Invariant: an unreviewed row's reason is the
  same on either registry state.
- E7 S4 vs S5 vocabulary: `case_rollcall` consumers are called only from S4 readers, `critic_review` / `s5_window` consumers only from
  theirs. Invariant: `approve` never closes an S5 review and `approved` never approves an S4 roll-call row.
- E8 consumer scope (RD1-25): each accept site's literal consumer is a key of `case_rollcall.accepts`. Invariant: a site cannot borrow
  another row's `accepts`.
- E9 a word in two rows: none (`approve*` vs `approved*` are different strings). Invariant: one word never has two classes.
- E10 TEMPORAL: item 1 creates `case_rollcall`; item 2 deletes `APPROVING_VERDICTS`. Before the row exists every approving test is False
  (no case accepted); with the constant gone but the controller import unchanged, the `ImportError` branch would make every gate A
  design review `accepted`. Hence the row, the deletion and both importers land in ONE commit. Test: T1 (no row -> False) and T4
  (`reject` -> `reject`, which an import failure would turn into `accepted` under F6 (a)).
- E11 a new word added to `CASE_CRITIC_VERDICTS` without a decision is red (the complement pin). Invariant: whether a new critic word
  approves is decided in data, never by default.
- E12 POSITIONAL: `_detector_body`: the registry stop after "no findings file" (nothing to judge stays exit 0) and before
  `findings_errors` / `merge_candidate_errors`; invariant: no detector line is computed from a word the registry could not judge.
  `_declared_review_verdict`: the registry check outside the `accepted` except; invariant: a registry or import problem never becomes
  `accepted`. `s4_limit_unknowns`: after the repair-count check, before `current_rejected`; invariant: the person is never shown a
  rejected-case list built on an unjudged word.

## 6. The reused function in a more consequential role (designer rule 1)

`gate_template.acceptable` moves into the S4 gate-A road. Its error direction is toward "not acceptable", never raising (m4). Per site:

| Site | `False` means | Safe? | What keeps it safe |
|---|---|---|---|
| `_row_outcome`, `scoped_verdict` | not `accepted` | yes | E2 reason names the registry |
| `_declared_review_verdict` | refusing word | yes | E2 `partial`, E12 |
| `_round_word_rule` | rule not fired | yes (declared `reject` stands) | — |
| `findings_errors` :607 | refusal skipped | NO on an unknown registry | E2 registry line; `_detector_body` stop |
| `_merge_concern_errors` | refusal skipped | NO on an unknown registry | E12 `_detector_body` stop before it |
| `s4_limit_unknowns` :819 | seam (unreadable) | yes | E12 registry text first |

Adversarial inputs that must stay on the safe side: the T1 list, an unreadable registry, a registry without the row or the word.

## 7. Readers of every touched file (designer rule 7)

The `owns_readers` block was not attached to the brief. The Lead runs:
`python -B tools/owns_readers.py --paths <the seven owns of §0> --names APPROVING_VERDICTS,_row_outcome,_round_word_rule,scoped_verdict,findings_errors,_merge_concern_errors,_detector_body,_read_round,_declared_review_verdict,s4_limit_unknowns,D13_ITEM_COUNT`
and the plan critic checks every line against this table. Hand greps (Grep tool):

- `critic_rollcall|APPROVING_VERDICTS|_declared_review_verdict|s4_limit_unknowns|case_rollcall` in `tools/`: 1 hit
  (`tools/lint-baseline.json:211`, the path of the test file).
- `controller\.py|driver_stage_plan` in `tools/`: 14 hits in 6 files. `gate-registry\.json|gate_registry` in `tools/`: 17 hits in 4 files.
- `.githooks/`: 0 for `critic_rollcall|APPROVING_VERDICTS|gate-registry|driver_stage_plan`; control `python|tools`: 25 hits.
- `.claude/agents`: 0 for the same set; control `scenario_walk`: 2 hits. `.claude/settings.json`: 0; control adding `hooks`: 16 hits.
- A whole-`.claude/` grep timed out in `.claude/worktrees/` (other sessions' copies, not live readers).

| Touched file / name | Reader | Verdict |
|---|---|---|
| `gate-registry.json` | `gate_registry.load_registry` (the one reader), `gate_template` | unchanged |
| | `test_gate_registry.py` pins | changes in this stream; also RD1-26, RD1-28 (F4) |
| | `tools/source_split.py`, `tools/source-split-carriers.json`, `tools/test_quarantine.py`, `tools/controller-blocks-gen.py` | unchanged (path strings, a comment) |
| `APPROVING_VERDICTS` (deleted) | `controller.py:3566, 3571`, `driver_stage_plan.py:819` | change in this stream (items 3, 4) |
| `_row_outcome` | `rejected_rows`, `scoped_verdict` | unchanged code; new reason on an unreadable registry |
| `scoped_verdict` | `controller._read_findings_ref` :3611, `_later_refusal` via it | unchanged; same word on a readable registry |
| `findings_errors` | `_detector_body`, `main`, `validate_artifacts.py:2660` | unchanged code; one new line on an unreadable registry |
| `_read_round` -> `current_rejected`, `accepted_rounds` | `s4_limit_unknowns`, `s5_plan._file_concerns` :1145 | unchanged code; doubt on an unreadable registry (F3) |
| `_detector_body` / `detector_main` | the S4 exit gate | exit 3 on an unreadable registry (new) |
| `_declared_review_verdict` | `_dispatch_review_verdict` :3656; `test_scoped_review_verdict.py:440` (quarantine) | unchanged code; `partial` on registry/import problem |
| `s4_limit_unknowns` | `s4_review_limit` :914; `tests/fixtures/driver-layers.json:537` (name listing) | unchanged |
| `CASE_CRITIC_VERDICTS` (kept) | `role_digest.py:89`, `controller._later_refusal` :3625, `test_ahead_cards.py:76`, `test_handoff.py:101`, `test_exit_gate_digest_source.py:100` | unchanged |
| `controller.py` (module) | `tools/controller-blocks-gen.py:22` (parses refusals) | unchanged: no raise added |
| `test_critic_rollcall_apply_fixes.py` | `tools/lint-baseline.json:211` (HandReaderInput count 1) | unchanged if no hand reader is added |
| `judgment-census.json` | `test_judgment_census.py`, `tools/architecture_gate.py` | a row only if the census asks |

## 8. Siblings

- Sweep of the artifact (rule 9): every reader of `APPROVING_VERDICTS` is converted (m2). Other comparisons of single critic words in
  the same module are per-word roles (the concern carrier `_read_round` :462, the fixes block `findings_errors` :628/:632, the level rows
  `_level_errors` :1066, `driver_stage_plan.s4_after_critic` :941 regex), not the approving class: not applicable, named in `decides`.
- Axis 34 (one road): after the change the critic's approval has one road per stage: `case_rollcall` at S4, `s5_window` inside the S5
  window, `critic_review` after it; each is a data row read by a consumer key. No literal approving list is left (AR-1 grep, §2).
- Axis 5 row 138 names this node; row 157 ("the critic's word per plan row") names `_declared_review_verdict` among the whole-file
  readers (CX2-25): that axis is about rounds, not words; unchanged.
- RD1-26 / RD1-28: `gate-registry.json` row-separated; `test_gate_registry.py` pins shared. Merge order F4 (a): RD1-26 first, then the
  later of RD1-28 / RD1-32 remeasures on the merged tree. RD1-33 (the scout of probe/identity readers) is unrelated in files.
- Analogs, reported and not taken: `contract.GATE_APPROVED_WORDS` and `controller.py:5456` (the person's gate decision words);
  `vocabulary.yaml` `stage_acceptance_verdicts` (F5); `role_digest` reading `CASE_CRITIC_VERDICTS` as known digest words.

## 9. Small choices closed by the designer

1. One consumer per site function (two calls in `_row_outcome` share `case_rollcall.row`): the registry's pattern and RD1-29's choice 1.
2. Roles: `accept` where the function decides `accepted` (`_row_outcome`, `scoped_verdict`, `_declared_review_verdict`); `validate`
   where it refuses or routes (`_round_word_rule`, `findings_errors`, `_merge_concern_errors`, `s4_limit_unknowns`), as RD1-29 choice 3.
3. `field: null`, so a dict passed by mistake reads no key (E3).
4. `_declared_review_verdict` consults the registry only when a non-empty declared word exists: with no word, the legacy "no findings
   file -> accepted" rule is outside this node.
5. Unreadable-registry texts reuse `registry_why` (RD1-27's one sentence), and the detector uses `DV.unreadable_line` (RH1-5).
6. The witness file is `test_critic_rollcall_apply_fixes.py` (fast, `keep`, covers `critic_rollcall.py`); the controller and driver rows
   are narrow calls placed there, not new files.

## 10. Reading trail

- Read: the RD1-29 card whole; batch rows 53-60 of `batch-1-phase-2.md`; RD1-26/28 card (Grep: order, m2, m12, readers);
  `critic_rollcall.py` 1-166, 225-374, 405-486, 578-656, 985-1019, 1091-1160, 1175-1184; `controller.py` 3545-3663;
  `driver_stage_plan.py` 800-829, 935-975; `gate_template.py` whole; `gate_registry.py` 20-79, 425-445, 596-705, 860-993;
  `gate-registry.json` 120-300, 618-647; `test_gate_registry.py` 25-94, 312-319, 800-824, 1100-1149; `test-layers.json` 10-19,
  1206-1217, 2038-2049, 2308-2331, 7460-7559; `TESTING.md` 90-164; `s5_plan.py` 1120-1164; `validate_artifacts.py` 2648-2663;
  `vocabulary.yaml` (Grep 69-77, 116-124); SIBLING_MAP rows 138, 157; `architecture.md` (Grep of headings and § A forms).
- Greps: `APPROVING_VERDICTS` (package, repo without worktrees: code only in the three files); `CASE_CRITIC_VERDICTS`; quoted
  `approve*` literals over `scripts/*.py`; callers of the site functions; `import gate_template` in the touched modules; census rows
  (control `critic_rollcall` hit); slow list (control `test_handoff`/`test_gate_registry` hit); the §7 greps with their controls.
- Not measured (no shell): the D13 after-values and the exact counted comparisons per site (estimate +6 items / +4 triples under F1 (b),
  +about 16 under F1 (a)); the zones of batches in work for `controller.py` (F4, rule 4); the `owns_readers` block (§7).
- Contradictions with the brief: the brief lists three readers files; the counted reads are nine sites in three files (m2). RD1-29
  has landed (ee3d5db0) and `critic_review` exists, so "after RD1-29" holds. RD1-28 has not landed (`probe_verdict.accepts` is `{}`).

## Lead decisions (18.11.2026, Lead session 501cb4e0, «решила сама»)

- F1 = (b): the three approving words only, all `matched`; `CASE_CRITIC_VERDICTS` stays the code list of known words; the
  set-difference pin `{"partial", "reject"}` (E11) is a test row.
- F3 = (a): `_read_round` returns its existing doubt with the `registry_why` reason before the rows on an unreadable registry.
- F4 = (a): RD1-32 builds now. Merge order = acceptance order with RD1-26 first; the later of RD1-28 / RD1-32 and C3-j (which
  also touches `gate-registry.json`, `judgment-census.json`, `test_gate_registry.py` on its branch) merges `main` and remeasures
  D13, the triples and the allow pin on the merged tree.
- F5 = (a): not in this node; a finding in the zone of `acceptance.py` (Lead writes it).
- F6 = (b): `ImportError` leaves the `accepted` branch and returns `partial`; `OSError` stays; one test row.
- §7: `tools/owns_readers.py` run by the Lead on origin/main b6682c31: 519 readers outside owns (the table of §7 stands);
  the `--names` list was passed comma-joined and read as ONE name (reported "absent"), so the name check is the designer's hand
  greps, not the tool; `test_gate_registry.py` is slow (canon judges). Accepted on basis lead.
