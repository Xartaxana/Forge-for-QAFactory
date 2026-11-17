# RD1-26 + RD1-28 card (draft): the identity word and the probe word read through their own registry rows

Designer draft for task t-1237, nodes `rules-debt/1/RD1-26` then `rules-debt/1/RD1-28`, feature F19. Sources: findings
`plans/piles/rules-debt/findings/20261117-c3-bound-to-priyom-ne-preobrazovan.md` (verdict t-1084, fix 1) and
`plans/piles/rules-debt/findings/20261117-c3-slova-probe-verdict-vnutri-preobrazovannyh-sajtov.md` (fix 3 (a)). Form model: the RD1-29 card.
The Lead decides the forks in §3; until then items follow the recommended option and say where they depend on one.
Order: RD1-29 lands -> RD1-26 -> RD1-28 (shared `acceptance.py`, `gate-registry.json`, `test_proof_level.py`, `test_gate_registry.py`;
each later node merges `main` and remeasures D13 on the merged tree).

## 0. The two builder dispatches: header lines (R11-f)

### 0.1 RD1-26

```
task: <new id at dispatch>
node: rules-debt/1/RD1-26
feature: F19
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rd1-26-28-registry-words-card.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_template.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/proof_level.py
C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_history.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
non-goals: rows of gate-registry.json other than `test_identity`; `proof_level.py` (RD1-28 owns it; `same_test` and `compare_identity` are read, never edited); `validate_window`'s probe condition (RD1-28); `gate_template.py` (no grammar change, fork F3 (b)); `run_history._make_pair` (reads the producer's own output word, §9); the quarantined files `test_acceptance_semantics.py`, `test_run_history_identity.py`, `test_receipts_per_function.py` (not run, not edited: TESTING.md «Что запускать»); `docs/SIBLING_MAP.md` (Lead, item 26-6); no new test file
handoff: a report with the FR walk (sections A-G), `gate_registry.py --sites` item and triple counts before and after with the moved triples named, the witness output, the `architecture:` / `judgment:` lines
edges: §6.1 of the card (E26-1 ... E26-8, each with its invariant) -- the Lead copies them inline into the dispatch
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path above>` and every non-slow, non-quarantined file it prints; `python -B ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` green; red-before: not run -- test_proof_level.py and test_gate_registry.py are judged by the batch canon (batch file, line «Скоуп свидетеля»)
siblings: axis 25 (the "same test" predicates outside proof_level named on its line: this node converts them); axis 34 (one road for the identity word: the row, read by consumer key); RD1-28 (probe words, next node); RD1-29 (s5_window / critic_review rows, lands first)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rd1-26-28-registry-words-card.md
```

### 0.2 RD1-28

```
task: <new id at dispatch>
node: rules-debt/1/RD1-28
feature: F19
given:
C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rd1-26-28-registry-words-card.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_template.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/red_sandbox.py
C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/proof_level.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/acceptance.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_proof_level.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_window_record.py
non-goals: rows other than `probe_verdict`; `red_sandbox.py` code (registered as a produce site only, F2 (a)); `probe_record_state`, `tooling_gap_key`, `PROBE_JUDGED_VERDICTS` and the probe-word readers in other files (fork F5); `gate_template.py` (fork F1 (b)); a second predicate or registry reader in production code; no new test file
handoff: as RD1-26 (FR walk, `--sites` before/after, witness, `architecture:` / `judgment:` lines)
edges: §6.2 of the card (E28-1 ... E28-9) -- copied inline by the Lead
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <every owns path above>` and every non-slow, non-quarantined file it prints; `python -B ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` green; red-before: not run -- test_proof_level.py, test_window_record.py, test_gate_registry.py are judged by the batch canon
siblings: axis 34 (one road for the probe word: one row for both probe tools, F2); the row's own `decides` ("readers ... are not sites yet": F5); RD1-26 (same files, lands first); RD1-29 (test_window_record.py, lands first)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rd1-26-28-registry-words-card.md
```

Owns versus the batch rows: RD1-26 is the batch row exactly. RD1-28 adds `test_window_record.py` (fork F4): the window's probe decision
has its behaviour table there, and RD1-29 holds that file until it lands.

## 1. Measured facts (read from the carriers 17.11.2026, tree with RD1-25 = 9e21d266)

| # | Fact | Carrier |
|---|---|---|
| m1 | `test_identity` row: words raw, instance, instance_code, file_code, same (all `matched`), different (`mismatched`), unknown (`unknown`, owner environment); consumers probe_repeat, run_reuse, run_fresh, receipt_holds, all ["matched"]; `already_probed` and `_product_receipt_repeat` are its converted accept sites | `references/gate-registry.json:124-166` |
| m2 | `probe_verdict` row: words intended_failure (matched), no_failure, wrong_location (mismatched), not_executed (unknown, environment), incomplete (unknown, factory); `accepts: {}`; sites only the two producers in `probe_by_code.py`; `decides` ends "The readers of the record ... are not sites yet" | `gate-registry.json:590-613` |
| m3 | `acceptable` is case-exact, no strip; `matched` is accepted iff the token `matched` is listed - a reason code narrows only `not_applicable`; a `mismatched` or `unknown` word is never acceptable whatever the consumer lists | `gate_template.py:9-13, 91-104` |
| m4 | `_bound_to` decides by the TRUTHINESS of `same_test(...)`; `same_test` returns raw / instance / instance_code / file_code / "" only, so truthiness == the matched set exactly | `acceptance.py:204-216`; `proof_level.py:887-929` |
| m5 | `green_on_current_bytes_why` accepts ONLY `raw` (`!= "raw"`, E11), pinned by the quarantined test "E11: only `raw` counts here" (same_test patched to `instance` -> not green) | `acceptance.py:175-180`; `tests/test_acceptance_semantics.py:593-595` |
| m6 | `_job_contract` accepts only `("same", "content")`, pinned by K-R6 (`("same", "code")` -> `{}`); `_compare_shas` maps same/different/unknown and falls to the file sha on unknown; `compare_identity` returns basis "" exactly when the verdict is unknown | `run_history.py:218-223, 248-262`; `proof_level.py:871-884`; `tests/test_run_history_identity.py:107-122` (quarantined) |
| m7 | Probe words compared inside converted sites of OTHER rows: `_product_receipt_repeat:1422` (`== "intended_failure"`), `already_probed:1508` (`behind ... == "intended_failure"`), `:1536` (`in ("no_failure", "wrong_location")`), `:1552` (`== "survived"`, a product-record word); `acceptance.validate_window:1227` (`!= "intended_failure"`, the finding said :1211 - lines drifted) | the files at those lines |
| m8 | The product record (`red_sandbox._write_product_records`) holds `product_verdict`'s words: intended_failure, probe_defect, incomplete, survived. `survived` and `probe_defect` are words of no registry row | `red_sandbox.py:1478-1489, 1511-1542`; Grep `survived` in gate-registry.json: 0 rows (control `killed` hit :705) |
| m9 | The window's probe block verdict can also be `partial_product` / `model_changed` (window_record constants); `acceptance.py` names neither (Grep 0; control `BLOCKED_OUTCOME` 5 hits), so they reach the window only as "not intended_failure" -> `sensitivity:` | `window_record.py:803-828`; Grep over `acceptance.py` |
| m10 | A26 counts a comparison only when its words meet the anchors or the words of the rows its function is registered under; a Name operand is resolved to the constants bound to it. So the probe words in `already_probed` / `validate_window` are invisible today, and a word moved into a constant is still seen | `gate_registry.py:350-363, 916-950` |
| m11 | A function registered under two rows with one a converted accept site is a finding ("give each row its own function"); RD1-25 (landed): every `acceptable(...)` call of a converted accept site must name, as a plain literal, a consumer of ITS row | `gate_registry.py:898-913, 426-444` |
| m12 | D13: `D13_ITEM_COUNT = 151`, the triple set pinned; the allow-set pin lists 5 entries | `tests/test_gate_registry.py:1020-1126, 309-316` |
| m13 | `test_proof_level.py` is a keep file (`gate_named`) covering `acceptance.py` and `run_history.py`; its C3-b2 table (`c3_b2_a_reuse_is_accepted_through_the_registry_row_and_an_unknown_runs_again`) already swaps the registry cache to unreadable and has rows for no_failure / survived / product intended_failure | `test-layers.json:4125-4143`; `test_proof_level.py:1794-1865` |
| m14 | `test_acceptance_semantics.py`, `test_run_history_identity.py`, `test_receipts_per_function.py` are in `quarantine` (not run by the canon, not edited by a builder); `test_window_record.py`, `test_blocked_by_env_window.py`, `test_s5_process.py`, `test_probe_binding.py` are keep rows | `test-layers.json` (quarantine section from :7209) |
| m15 | `window_record.py:2004` prints `green_on_current_bytes_why(...)[1]` to the window's reader | `window_record.py:2004` |

## 2. Section 1 - invariants, owners, census, variety, commit lines

AR-n touched (`design/architecture.md`), with the change check each demands in the DoD:

- AR-13 (one reader): `same_test` / `compare_identity` stay the one comparison; their word is now judged through the row. Check: the
  axis 25 line of `docs/SIBLING_MAP.md` that lists these sites as "queued" is rewritten (Lead, item 26-6); Grep `same_test\(|compare_identity\(`
  over `scripts/*.py` (positive control `proof_level.py:917`) and name each call site in the report as converted or "not an acceptance - why".
- AR-15 (one survivor): every accept site of the two words calls `gate_template.acceptable` through its own consumer. Check: `gate_registry.py --check` exits 0
  (RD1-25 judges the consumer scope); the "no probe word in the three old functions" row (item 28-5).
- AR-1 (closed variety in data): the matched words leave code. Two literals stay by decision and are VISIBLE to A26: the E11/K-R6
  narrowing (F3) and the mismatched repeat-block (F1). Check: each is a counted `--sites` item at a site of its own row, never hidden in a constant.
- AR-20 (ratchets): D13 count and triples RISE (inventory steps, new sites registered). Estimate, not verified: RD1-26 +2 to +4 items, +2 triples;
  RD1-28 +2 items, +2 triples (F1 (a), F2 (a)). The builder measures `--sites` before/after and writes each raise row by row in the comment block above
  `D13_ITEM_COUNT`, in its own form; the allow-set pin moves with its new entries named.
- AR-28 (an unknown never becomes a pass): an unreadable registry gives a stated unknown at every converted site (E26-2, E28-2).
- AR-29 (code judges data): every check here reads a code-produced token or compares identities; none reads a role's content.

Owner and census class of every check the card adds or alters (P27, AR-29):

| Check | Owner it serves | Census class |
|---|---|---|
| `acceptance._bound_to` (identity of a review/probe vs the test) | data | xref (a join of identities); no census unit today (no refusal site) |
| `acceptance.green_on_current_bytes_why` (raw bytes of the author's run) | data | xref |
| `run_history._job_contract` (twin contracts of one function) | data | xref |
| `run_history._compare_shas` (red/green pair same or changed) | data | xref |
| `proof_level.probe_fired` (new: the probe's broken check fired) | data (a code-produced verdict token) | shape |
| `proof_level.probe_found_defect` (new, F1 (a): a judged defect blocks a repeat) | data | shape |
| `acceptance.validate_window` probe condition | data | shape (census row `validate_window` class `shape` unchanged) |
| `already_probed`, `_product_receipt_repeat` | data | not census units today; unchanged |

No census row is added unless `test_judgment_census.py` demands one (none of the new functions raises).

Variety walk: `variety: none -- the change moves two closed code vocabularies (the identity words of same_test/compare_identity and the probe verdicts of probe_by_code/red_sandbox) from literals into their registry rows; no value varies by project, language, stack or host`.

Commit lines: the only carrier of their form is `tools/architecture_gate.py` (docstring points 1 and 6). In that form, per node:
`architecture: AR-1, AR-13, AR-15, AR-20, AR-28, AR-29 -- <how each is kept, one clause each>` and
`judgment: none -- the identity word and the probe verdict are tokens produced by code (same_test, compare_identity, probe_by_code, red_sandbox); code now reads them through their registry rows, and no check reads a role's content`.

## 3. Forks (the Lead decides; recommendations marked)

**F1 (RD1-28) - the mismatched repeat-block cannot go through `acceptable`.** `already_probed` blocks a repeat on `no_failure` /
`wrong_location` (and `survived`): words of class `mismatched`, which `acceptable` never accepts and the registry check refuses as a
consumer token (m3). The finding's direction ("call through acceptable") does not fit this half.
- (a, recommended) New `proof_level.probe_found_defect(record)`, registered under `probe_verdict` as role `validate` (it refuses a
  repeat, it lets nothing through). Its one literal comparison of the row's mismatched words stays in code, counted by A26 at a site of its
  own row (+1 item, +1 triple). Cost: AR-1 is met only as far as "visible at its own row", not "in data".
- (b) A refusing predicate beside `acceptable` (e.g. a `refuses` map read by a second function in `gate_template`). This puts the
  list in data, but changes the C3-0 grammar (one predicate, `_token_problem`, the C3-0 tables). It needs a mechanism node with a plan critic.
- (c) Leave the block inside `already_probed` and name the reason in the row's `decides`. The finding's class stays open for it.

**F2 (RD1-28) - the product record's words (m8).** `:1508` reads either tool's record, and `:1552` reads `survived`.
- (a, recommended) One row for "what a probe proves" across both probe tools (P31). Add `survived` (`mismatched`) and `probe_defect` (`unknown`,
  owner `factory`) to `probe_verdict.words` / `verdict_map`. Register `red_sandbox.py:product_verdict` as a `produce` site, and let `decides` name
  both producers. Cost: +1 counted item at `product_verdict` (`proof["verdict"] == "probe_defect"`, estimate). `request_status` stays an unregistered reader (F5).
- (b) A separate row `product_probe_verdict`. RD1-25 then forbids one `probe_fired` from serving both, so two functions are needed, and
  `intended_failure` sits in two rows (a same-class pin is owed).
- (c) Leave `survived` a literal in the block function. `intended_failure` still goes through `probe_fired` unchanged (it is already a row word).

**F3 (RD1-26) - the narrowing sites (m5, m6).** `matched` carries no reason code in `acceptable`, so a consumer cannot say "raw only"
or "content basis only".
- (a, recommended) The predicate plus a declared narrowing at the site. `green_on_current_bytes_why` asks `acceptable(word,
  "test_identity.mechanical_bytes") and word == "raw"`, and the second comparison is an `allow` entry whose `why` names E11. `_job_contract` asks
  `acceptable(verdict, "test_identity.contract_twin") and basis == "content"` (`content` is a basis word of no row: not counted). This keeps
  E11 and K-R6, adds the unreadable-registry safety, and makes the narrowing visible to A26.
- (b) Extend the grammar so that `matched:<reason_code>` tokens are honoured (gate_template + registry check + C3-0 tables). The
  narrowing then lives in data, but this is a C3-0 mechanism change: another node, with a plan critic.
- (c) Name both sites "not an acceptance" and leave them unregistered. They stay invisible to A26, and the finding's class stays open for them.

**F4 (RD1-28 owns) - the window's probe row.** The behaviour table of `validate_window` lives in `test_window_record.py` (its `pure_window`
helper). RD1-29 holds that file until it lands.
- (a, recommended) Widen RD1-28's owns to `test_window_record.py`. The Lead checks rule 4 zones: it is sequential after RD1-29, so the
  two nodes do not overlap.
- (b) Pin `validate_window` structurally in `test_proof_level.py`. An AST row checks that its probe condition calls `proof_level.probe_fired` and
  compares no probe word. This is weaker: it proves no gap.

**F5 (class scope) - probe and identity words read outside any registered site.** The quoted-word Grep
`"(intended_failure|no_failure|wrong_location|not_executed)"` over `scripts/*.py` (non-test) hits check_delivery 4, contract 4, probe_debt 9,
retro_numbers 5, report_facts 3, run_suite 4, window_record 3, proof_level 11, red_sandbox 25, probe_by_code 57, and one each in 6 more
files. This is an upper bound: several are other vocabularies (receipt core, semantic_verdict). The row's `decides` already declares these readers
"not sites yet". The finding's class is narrower: a word accepted inside ANOTHER row's converted site. The two nodes close that class.
- (a, recommended) A new rules-debt node, scout first, that inventories the readers. Each reader gets a verdict: converted, registered as
  produce/measure, or "not this vocabulary".
- (b) Widen RD1-28 now. The scope is unbounded and the node is not drafted for it.

## 4. RD1-26 items (numbered; each: file, function, expected behaviour, test row)

26-1. `references/gate-registry.json`, row `test_identity`:
   - `sites` gains:
     - `{"file": "acceptance.py", "function": "_bound_to", "role": "accept"}`;
     - `{"file": "acceptance.py", "function": "green_on_current_bytes_why", "role": "accept", "allow": [<the narrowing, F3 (a)>]}`;
     - `{"file": "run_history.py", "function": "_job_contract", "role": "accept"}`;
     - `{"file": "run_history.py", "function": "_compare_shas", "role": "accept", "allow": [<the returned unknown state>]}`.
   - Each `allow` is `{"compare": <the exact ast.unparse text the scan prints>, "why": ...}`. The two `why` texts are "E11: a
     mechanical round is bound to the raw bytes the reviewer saw; the row's class matched does not separate raw from instance" and "a
     state the function returns to its caller, not an acceptance of an identity word" (the `_run_freshness` form).
   - `accepts` gains `test_identity.window_bound`, `.mechanical_bytes`, `.contract_twin`, `.pair_same`, all `["matched"]`.
   - `decides` gains one clause: "a red/green pair of the same test owes no expectation change; twin contracts count as one function
     only on equal code and content".
   - test: `test_gate_registry.py` D13 pins (count, triples, the allow-set pin at :311), remeasured with `--sites`, comment rows in the
     block's own form | expected from: card §2 AR-20.

26-2. `scripts/acceptance.py::_bound_to`
   - The first test becomes `if acceptable(proof_level.same_test(proof_level.proof_identity(item), proof_level.proof_identity(proof)),
     "test_identity.window_bound"): return True`. The docstring names the row. The import comment at :11 names `test_identity` beside
     `s5_window`.
   - test: `test_proof_level.py::c3_b2_...` gains a `_bound_to` table, called directly as `acceptance._bound_to(item, proof, {}, None)`:
     - pairs giving each same_test answer (raw equal; identity equal by content; equal by code only; legacy `test_code_sha` equal) ->
       True;
     - different identities, two empty sides, a None or `{}` proof -> False;
     - the same table under `unreadable_registry()` -> all False.

     | expected from: m4 (the matched set), row decides, FR-59.

26-3. `scripts/acceptance.py::green_on_current_bytes_why`
   - `word = proof_level.same_test(...)`. When `acceptable(word, "test_identity.mechanical_bytes") and word == "raw"` holds, return
     `True, ""`.
   - Else, when `registry_problem()` is non-empty, return at once `False, registry_why(problem, "whether the author's green run used these
     bytes is not known")`.
   - Else keep today's bytes reason and `continue`. Import `registry_problem, registry_why` beside `acceptable`.
   - test: the same table, using a temp root with one run block and one job, as `test_acceptance_semantics.py:572-583` builds:
     - raw equal -> `(True, "")`;
     - raw differs -> False, with the bytes reason;
     - `same_test` patched to `instance` -> False (E11);
     - `""` -> False;
     - unreadable -> False, a why that starts `the gate registry cannot be read` and does not contain `ran the test file as sha256` (FR-41).

     | expected from: E11 (m5), FR-41, card E26-5.

26-4. `scripts/run_history.py::_job_contract`
   - The comparison becomes: for each candidate, `verdict, basis = PL.compare_identity(found[0], c)`, and it matches only when
     `acceptable(verdict, "test_identity.contract_twin") and basis == "content"`.
   - Add `from gate_template import acceptable, registry_problem` at module top, as `acceptance.py` and `proof_level.py` do.
   - test: rows in the same table:
     - equal code and content -> the first;
     - `compare_identity` patched to `("same", "code")`, `("unknown", "")` or `("different", "code")` -> `{}`;
     - unreadable registry with equal shas -> `{}`.

     | expected from: K-R6 (m6), card E26-4.

26-5. `scripts/run_history.py::_compare_shas`
   - `verdict, decided_on = PL.compare_identity(*pair)` and `problem = registry_problem()`.
   - When `decided_on and not problem`: basis as today, and the verdict is `"same" if acceptable(verdict, "test_identity.pair_same")
     else "changed"`.
   - The file basis applies only when `not problem`.
   - Otherwise there is ONE return of today's unknown tuple. No literal `verdict != "unknown"` / `== "same"` is left: the routing reads
     `decided_on`, the comparator's own basis (m6).
   - test: rows in the same table:
     - a sample of the K-R1 grid (code equal; code differs with raw equal; no code with raw differing; file only; nothing) equals
       the values K-R1 names;
     - unreadable registry with equal code shas, and with equal file shas only -> `("unknown", "unknown")` as the first two.

     | expected from: K-R1 (m6), card E26-2 / E26-5.

26-6. (Lead, at acceptance, not the builder) The axis 25 line of `docs/SIBLING_MAP.md` changes. Its "queued (batch 3 ...)" clause for
   `same_test`, `acceptance.green_on_current_bytes_why` and `run_history` is replaced by: these sites accept through the `test_identity`
   row (RD1-26), with the two narrowings named. It is a mechanism path: the commit carries `tier:` at the lead binding and the axis block or
   its "axes: not a mechanism" line.

## 5. RD1-28 items

28-1. `references/gate-registry.json`, row `probe_verdict`:
   - `sites` gains:
     - `{"file": "proof_level.py", "function": "probe_fired", "role": "accept"}`;
     - `{"file": "proof_level.py", "function": "probe_found_defect", "role": "validate"}` (F1 (a));
     - `{"file": "red_sandbox.py", "function": "product_verdict", "role": "produce"}` (F2 (a)).
   - `accepts`: `{"probe_verdict.fired": ["matched"]}`.
   - F2 (a): `words` gains `survived` and `probe_defect`. `verdict_map` maps `survived: {"class": "mismatched"}` and `probe_defect:
     {"class": "unknown", "owner": "factory"}`.
   - `decides`: the last sentence ("not sites yet") is replaced. The new text names `probe_fired` (the accept site that window, repeat and
     product-receipt reads share), `probe_found_defect` (the repeat refusal) and `red_sandbox.product_verdict` (the second producer). It
     keeps "the remaining readers of the record are not sites yet" (F5).
   - test: D13 and allow pins as in 26-1 | expected from: card §2 AR-20.

28-2. `scripts/proof_level.py` - two new top-level functions, next to `PROBE_JUDGED_VERDICTS`:
   - `probe_fired(record) -> bool` returns `isinstance(record, dict) and acceptable(record, "probe_verdict.fired")`. The row's field
     `verdict` is read by the predicate. It has no literal.
   - `probe_found_defect(record) -> bool` returns `isinstance(record, dict) and record.get("verdict") in (<the row's mismatched words:
     no_failure, wrong_location, survived>)`.
   - Both docstrings state the error direction (E28-1, §7).
   - test: `test_proof_level.py::c3_b2_...` gains one table. The record is `{"verdict": w}` for w in:
     - the row's words, plus `partial_product`, `model_changed`, `incomplete_or_wrong_failure`;
     - `"Intended_failure"`, `" intended_failure"`, `""`, None, `["intended_failure"]`, `"\u0438ntended_failure"` (written as the
       escape, FR-30), a 10,000-character string;
     - a record without `verdict`, and the non-dicts None and `"intended_failure"`.

     The rows:
     - `probe_fired` is True only for `intended_failure`; under `unreadable_registry()` all False; an injected registry whose
       `probe_verdict.words` lacks `intended_failure` gives False;
     - `probe_found_defect` is True only for no_failure / wrong_location / survived, readable or not;
     - every word `red_sandbox.product_verdict` can return (intended_failure, probe_defect, incomplete, survived) is a word of the row
       (F2 (a)).

     | expected from: row decides, m3, m8, FR-59.

28-3. `scripts/proof_level.py::_product_receipt_repeat` and `::already_probed`
   - `:1422` `record.get("verdict") == "intended_failure"` becomes `probe_fired(record)`.
   - `:1508` `behind.get("verdict") == "intended_failure"` becomes `probe_fired(behind)`; the order of the `and` chain is kept.
   - `:1536` `record.get("verdict") in ("no_failure", "wrong_location")` and `:1552` `record.get("verdict") == "survived"` become
     `probe_found_defect(record)`.
   - The hit dicts keep their `prior_verdict` values.
   - test: the existing rows at `test_proof_level.py:1819-1849` stay green. Added rows:
     - a `wrong_location` record of the same bytes -> probed True;
     - `not_executed` / `incomplete` / `probe_defect` records of the same bytes -> probed False;
     - a receipt with no `mutated_file(s)` whose behind record says `intended_failure` -> hit `by: receipt`; the same with behind
       `no_failure` -> no receipt hit (build them with the file's `put` / `live` helpers).

     | expected from: `already_probed` docstring items 1-4, card E28-1.

28-4. `scripts/acceptance.py::validate_window` (`:1227`): `probe.get("verdict") != "intended_failure"` becomes `not
   proof_level.probe_fired(probe)`. It stays the first disjunct of that condition, and nothing else in the function changes.
   - test (F4 (a)): `test_window_record.py` gains a table beside `c3_d_review_word_through_the_registry`, using the same patches and the
     same registry swap. The item is a ran, `new_or_changed`, schema-1 item with a probe whose location, reason and `failure_kind:
     assertion` pass, bound by `input_hash`. The rows:
     - `intended_failure` -> no `sensitivity:A`;
     - `no_failure`, `partial_product`, `model_changed`, `""`, absent -> `sensitivity:A`;
     - unreadable registry with `intended_failure` -> `sensitivity:A`.

     | expected from: row decides, m9, AR-28.

28-5. `scripts/tests/test_gate_registry.py`: one row (one parameterised check) for E28-6. For `(proof_level.py, already_probed)`,
   `(proof_level.py, _product_receipt_repeat)` and `(acceptance.py, validate_window)`: no item of `GR.scan_package(PLUGIN_ROOT)[file]["items"]`
   whose `function` is that function has words meeting `probe_verdict.words`. Positive control: the same query on `(proof_level.py,
   probe_found_defect)` finds its one item.
   | expected from: finding fix 3 (a), m10.

## 6. Edges and their invariants

### 6.1 RD1-26

- E26-1 readable registry:
  - `_bound_to` is True iff `same_test` gives raw / instance / instance_code / file_code, or the mechanical branch holds;
  - green is True only on `raw`;
  - `_job_contract` takes the first only on `("same", "content")`;
  - `_compare_shas` equals the K-R1 grid.

  Invariant: no review, probe, run, contract or pair of other bytes counts that did not count before, and the reverse.
- E26-2 unreadable registry:
  - `_bound_to` is False, the mechanical branch included;
  - green gives `(False, <registry why>)`;
  - `_job_contract` gives `{}`;
  - `_compare_shas` gives `("unknown", "unknown", ...)`, with no file basis.

  Invariant: an unreadable registry never binds a proof, never closes a mechanical round, never drops a red/green pair, never picks a
  stranger's contract (AR-28, FR-59), and never states a measured-looking fact (FR-41). In the window the review gap comes first (C3-d E3).
  A probe-owing item gains `sensitivity:` where today `_bound_to` passed on truthiness. The story-level door is the existing dispatch stop
  `REGISTRY_BLOCK` (unchanged).
- E26-3 absent or empty input: two empty shas, a None or `{}` proof, a non-dict contract -> not the same, as today. Invariant: two
  absent things are never "the same" (AR-23).
- E26-4 the narrowing (F3 (a)): `instance` / `instance_code` / `file_code` never close a mechanical round; `("same", "code")` never picks a
  contract. Invariant: the narrowing is kept and visible to A26, and the registry's class never widens it.
- E26-5 POSITIONAL:
  - in green, the registry check sits after the job's raw sha is read and before the bytes reason. Invariant: earlier measured reasons
    (no run block, no job) read as today, and no reason claims the bytes differ on an unreadable registry;
  - in `_compare_shas`, the registry check comes before both bases. Invariant: the file basis never answers for a pair the registry
    could not judge.
- E26-6 TEMPORAL: item 26-1 creates the four consumers. Before they exist, every call is False (every window gaps, every pair is owed).
  Hence the row and the sites land in ONE commit (AR-22). Test: an injected registry without `test_identity.window_bound` -> `_bound_to`
  False.
- E26-7 consumer scope: each site names only its own literal consumer of `test_identity` (RD1-25). Invariant: no site borrows
  `probe_repeat` or another site's consumer.
- E26-8 scanner visibility: no word is moved into a constant or helper to avoid a count (m10 resolves names anyway). Invariant: every new
  counted item is converted or allowed with its `why`, and the D13 raise is named row by row (AR-20).

### 6.2 RD1-28

- E28-1 readable registry, behaviour kept for each of these words:
  - `intended_failure` fires;
  - no_failure / wrong_location / survived block a repeat on the same bytes;
  - not_executed / incomplete / probe_defect / partial_product / model_changed / `incomplete_or_wrong_failure` / `""` / None / absent
    neither fire nor block.

  Invariant: no probe counts, and no repeat is blocked, that did not before.
- E28-2 unreadable registry: `probe_fired` is False everywhere, so the window gives `sensitivity:`, the product-receipt repeat is None,
  and `own` is None. `probe_found_defect` reads no registry (a refusal stays a refusal). `already_probed` already runs the probe because
  the identity acceptance refuses first (rows :1826-1829). Invariant: an unreadable registry never closes sensitivity and never answers
  a repeat from a record (AR-28).
- E28-3 a non-dict record, a missing or non-str verdict: neither fires nor blocks. Invariant: the empty outcome is never "fired" (AR-23).
- E28-4 case, padding, homoglyph: exact match only. Invariant: no site widens what it accepts.
- E28-5 a window verdict that is no row word (`partial_product`, `model_changed`): not fired, so `sensitivity:` as today. Invariant: a
  one-check product receipt or a stale model never closes the window as a full probe.
- E28-6 one row per function (m11): `probe_fired` and `probe_found_defect` sit only under `probe_verdict`; `already_probed` and
  `_product_receipt_repeat` stay under `test_identity`, `validate_window` under `s5_window`. Invariant: no function sits under two rows,
  and no probe word is compared in the three old bodies (item 28-5).
- E28-7 TEMPORAL: `probe_verdict.fired` is created by item 28-1. Without it every window gaps and no repeat is answered from a record.
  Hence one commit.
- E28-8 POSITIONAL: in `validate_window`, `probe_fired` keeps the first-disjunct place; in `already_probed`, `own`'s chain order is kept
  (`behind is not None and probe_fired(behind) and ...`). Invariant: the result is the same OR/AND of the same facts.
- E28-9 the vocabulary (F2 (a)): `probe_by_code` compares neither new word (Grep `survived|probe_defect` in probe_by_code.py: 3 hits, all
  prose or f-strings). Invariant: one word has one class, and no producer's word lies outside the row (item 28-2 test).

## 7. The reused function in a more consequential role (designer rule 1)

`gate_template.acceptable` becomes the gate at eight new sites. Its error direction is fixed: toward "not acceptable", never raising
(`gate_template.py:9-13`). The reused producers `same_test` and `compare_identity` err toward `""` / `unknown`. The safe side per site:

| Site | `False` means | Safe? | What keeps it honest |
|---|---|---|---|
| `_bound_to` | stale_review / sensitivity gap | yes | — |
| `green_on_current_bytes_why` | the round is not green | yes | E26-5: the why names the registry |
| `_job_contract` | no contract, a coarser sha | yes | unknown counts as changed (existing) |
| `_compare_shas` (pair_same) | changed, so a pair is owed (a question to the critic) | yes | E26-2: unknown on an unreadable registry |
| `probe_fired` at the window | sensitivity gap | yes | — |
| `probe_fired` at `own` / product receipt | the probe runs | yes | `already_probed` errs only toward "not probed" (its docstring) |
| `probe_found_defect` (literal) | no block, the probe runs | yes; True = a refusal with the person's door | — |

Adversarial inputs that must stay on the safe side:
- the probe records: the item 28-2 battery;
- the identity dicts: None, `{}`, empty or whitespace-only shas (the strip reads them as none), an identity with only `job_id`, a legacy
  carrier with only `input_hash`, a review measured on other bytes;
- the registry: unreadable, without the consumer, without the word.

## 8. Readers of every touched file (designer rule 7)

The `tools/owns_readers.py` block is NOT attached to the brief. The Lead attaches
`python -B tools/owns_readers.py --paths <the owns of §0> --names _bound_to,green_on_current_bytes_why,_job_contract,_compare_shas,already_probed,_product_receipt_repeat,probe_fired,probe_found_defect,D13_ITEM_COUNT`
before dispatch; the plan critic re-runs it (Q13 (d)). Hand greps meanwhile:
- the names above plus `acceptance\.py|run_history|proof_level|gate-registry\.json|probe_verdict|test_identity` over `tools/`: 20 hits in 7
  files;
- the same over `.githooks/`: 0 (control: `python|tools` gave 24 hits);
- the same over `.claude/agents`: 0 (control: `scenario_walk` gave 3);
- the same over `.claude/settings.json`: 0 (control: `hooks` gave 16).

| Touched file / name | Reader | Verdict |
|---|---|---|
| `gate-registry.json` | `gate_registry.load_registry` (the one reader), `gate_template` | unchanged |
| | `test_gate_registry.py` D13 and allow pins | changes in RD1-26 and RD1-28; also RD1-29 (`s5_window`, `critic_review`) and RD1-32 - sequential, each remeasures |
| | `tools/source-split-carriers.json:15,35`, `tools/source_split.py` (fixtures), `tools/test_quarantine.py:2199` (path list), `tools/controller-blocks-gen.py:352` (comment) | unchanged |
| `acceptance._bound_to` | `validate_window` (:1165, :1171, :1175, :1228); `test_receipts_per_function.py:194`, `test_acceptance_semantics.py:386` (quarantined) | unchanged code; same answer on a readable registry (E26-1) |
| `acceptance.green_on_current_bytes_why` | `green_on_current_bytes` -> `_bound_to`; `window_record.py:2004` (prints the why); `controller.py:7426` (comment); `test_blocked_by_env_window.py:630`, `test_s5_process.py:311` (keep); `test_acceptance_semantics.py` (quarantined); `test_proof_level.py:1439` K-C (a) (must still call `same_test`: it does) | unchanged; the printed why names the registry on an unreadable one (E26-5) |
| `run_history._job_contract`, `_compare_shas` | `_shas`, `_make_pair` (internal); `test_run_history_identity.py` (quarantined: K-R1, K-R5, K-R6 stay true by E26-1 / E26-4); `test_proof_level.py:1439` K-C (a); `proof_level.py:870` (docstring) | unchanged |
| `run_history.py` (module, new import of `gate_template`) | its importers (s5_precheck and others); `tools/lint-baseline.json:63-81` (other names) | unchanged; `gate_template` -> `gate_registry` imports no package module (no cycle) |
| `proof_level.already_probed`, `_product_receipt_repeat` | `red_sandbox.py` (1 call), `probe_by_code.py` (2), keep tests (`test_probe_binding.py` and others) | unchanged answers (E28-1) |
| `proof_level.probe_fired`, `probe_found_defect` (new) | `already_probed`, `_product_receipt_repeat`, `acceptance.validate_window` | new readers in this stream |
| `acceptance.validate_window` probe condition | window_record.verdict, controller window acceptance | unchanged gaps on a readable registry |
| `red_sandbox.product_verdict` (registered, not edited) | `_write_product_records`, `request_status` | unchanged |
| `test_window_record.py` | RD1-29 (owns it now) | changes in RD1-28 after RD1-29 lands (F4) |
| `docs/SIBLING_MAP.md` axis 25 | `tools/mechanism_gate.py` (MAP_PATH) | changes by the Lead (item 26-6) |

## 9. Siblings

- Sweep of the artifact (rule 9), the enclosing blocks:
  - `acceptance.py` 130-216 (`green_on_current_bytes_why`, `green_on_current_bytes`, `run_freshness_of`, `_bound_to`):
    - two sites applied (26-2, 26-3);
    - `green_on_current_bytes`: not applicable, no comparison;
    - `run_freshness_of`: not applicable, it calls `proof_level.run_freshness`, already a converted site.
  - `run_history.py` 203-262:
    - `_job_contract` and `_compare_shas` applied;
    - `_shas`: not applicable, no word.
  - `proof_level.py` 1092-1580:
    - `_product_receipt_repeat` and `already_probed` applied (four comparisons);
    - `tooling_gap_key:1105` and `probe_record_state:1149-1156` with `PROBE_JUDGED_VERDICTS:1116`: not applicable to the finding's class.
      They are unregistered state mappings that err toward `""` / `not_run`, not accepts inside another row's site; they belong to F5.
  - `validate_window` probe block 1219-1234: the one probe word applied (28-4).
- Axis 25: its line names exactly these "same test" predicates as queued, and RD1-26 converts them (26-6 rewrites the line).
  `execution_request._same_identity_for_count` (a budget, the opposite safe side, folds `unknown` itself per `compare_identity`'s
  docstring): not applicable.
- Axis 34 (one road): after the change, each word has one road, its row read by consumer key. The F2 (a) single probe row keeps both
  probe tools on one road. F1 and F3 name the two literals that stay and why.
- `run_history._make_pair:701` (`verdict == "same"`): it reads the producer's own output word; the decision is made once in
  `_compare_shas`. Not applicable.
- Analogs reported, not taken:
  - `validate_window` calls `probe.get(...)` on a non-dict probe in its schema-2 block (pre-existing, raises);
  - the FR-41 residue of `_match` named by t-1084 :63 (a low node the Lead may open).

## 10. Small choices closed by the designer

1. One consumer per site; names `window_bound`, `mechanical_bytes`, `contract_twin`, `pair_same`, `fired`. The finding's `review_bound` was an
   example, and `_bound_to` binds probes too.
2. `_compare_shas` routes on `compare_identity`'s basis (`decided_on`), not on a literal `"unknown"`. Same answers (m6), one counted item fewer.
3. An unreadable registry in `_compare_shas` returns the existing unknown tuple, with no new basis word. Its one reader `_make_pair` already
   treats unknown as owed.
4. `probe_fired` / `probe_found_defect` guard non-dicts. A bare word is not a record.
5. `probe_found_defect` is role `validate` (F1 (a)): it refuses a repeat and accepts nothing.
6. `probe_verdict.test` stays `test_probe_by_code_languages_plan.py`. The consumer table lives in `test_proof_level.py`.
7. The axis 25 edit goes to the Lead, not the builder. `docs/SIBLING_MAP.md` is a mechanism path whose commit needs `tier:` at the lead binding.
8. All new rows go to keep files (`test_proof_level.py`, `test_gate_registry.py`, `test_window_record.py`). The quarantined pins are not
   edited and stay true by the kept behaviour.

## 11. Reading trail

- Read:
  - both findings;
  - t-1084 review (Grep);
  - the RD1-29 card;
  - `gate-registry.json` 1-30, 120-179, 244-278, 585-629;
  - `gate_template.py` whole;
  - `gate_registry.py` 200-259, 340-449, 780-995;
  - `acceptance.py` 1-230, 1130-1259;
  - `proof_level.py` 845-989, 1090-1169, 1400-1589, 503-517 (Grep);
  - `run_history.py` 136-265, 689-733;
  - `red_sandbox.py` 1465-1544;
  - `window_record.py` 803-870;
  - `test_gate_registry.py` 300-324, 695-724, 1016-1155;
  - `test_proof_level.py` 1425-1445, 1794-1865;
  - `test_window_record.py` 2820-2879;
  - `test_acceptance_semantics.py` 380-419, 570-600;
  - `test_run_history_identity.py` 1-135;
  - `test-layers.json` (Grep, 2033, 4125-4143, 7205-7216, 9690-9699);
  - `docs/TESTING.md` 68-159;
  - `docs/SIBLING_MAP.md` 449-451, 589-600;
  - `design/architecture.md` 40-74, 173-199 (Grep of change checks);
  - batch file `batch-1-phase-2.md` 1-60;
  - `tools/architecture_gate.py` (Grep);
  - `tools/mechanism_gate.py` (Grep);
  - `test_judgment_census.py` (Grep).
- Greps, with their controls:
  - `survived|killed` in the registry;
  - `PARTIAL_PRODUCT|MODEL_CHANGED` in acceptance (control `BLOCKED_OUTCOME`);
  - the quoted probe words over `scripts/*.py`;
  - callers of `_bound_to` / green / `_job_contract` / `already_probed`;
  - the rule 7 greps of §8.
- Not measured:
  - the D13 after-values (estimates);
  - other piles' batch zones for `proof_level.py`, `acceptance.py`, `run_history.py`, `test_window_record.py` (the Lead's rule 4 check).
- Contradictions with the brief or the finding:
  - the finding's `validate_window:1211` is now `:1227`;
  - the finding's direction "call through acceptable" cannot hold for the mismatched words (F1) or for the raw / content narrowings (F3);
  - the batch row names `test_proof_level.py`, while today's pins of these behaviours sit in quarantined files (m14): the rows go into
    `test_proof_level.py`, which covers both scripts.

## Lead decisions (Lead, 17.11.2026, Opus; «решила сама»)

F1 = (a) `proof_level.probe_found_defect(record)` registered under `probe_verdict` as role `validate`, its one literal comparison counted by A26 at its own row; F2 = (a) one row for what a probe proves across both tools (`survived` mismatched, `probe_defect` unknown/factory, `red_sandbox.py:product_verdict` a `produce` site); F3 = (a) the predicate plus a declared narrowing at the site (`allow` entry whose `why` names E11); F4 = (a) RD1-28 owns widen to `test_window_record.py`, sequential after RD1-29; F5 = (a) a scout-first node for probe and identity words read outside registered sites (the Lead files it). Both builders start after RD1-29 lands on main (shared `gate-registry.json`, `test_gate_registry.py`); RD1-26 first, RD1-28 after it. critic on this plan: skipped -- every fork follows the designer's recommendation and each rejected option (b) is exactly the C3-0 grammar change; no meaning of an existing field changes; the code gets the topic critic.
