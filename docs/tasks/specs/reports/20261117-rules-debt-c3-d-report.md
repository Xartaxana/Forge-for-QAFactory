# Report: card C3-d (RD1-7, task t-1081) - the critic's review word accepted through the predicate

Builder, branch `worktree-agent-ac40b44fb0a175afa`, one commit, not pushed. Direction (i) + F-T9 (a), as the card governs.

## 1. Done

1. Registry row `s5_window` (only that row) of `references/gate-registry.json`: `vocabulary: code`; `decides` = card item 1 text;
   sites `acceptance.py:validate_window` `accept` (unchanged, now calls `acceptable`), `window_record.py:verdict` re-roled `produce`,
   `window_record.py:build` registered `produce`; `field: null`; `words: [approved, unverified]`; `verdict_map` approved -> matched,
   unverified -> not_applicable / `static_review`; `accepts` the three consumers `s5_window.review: [matched]`,
   `s5_window.static_review: [not_applicable:static_review]`, `s5_window.handed_review: [matched, not_applicable:static_review]`;
   `promotable false`, `unknown_branch` / `on_no_answer` / `waits_at` unchanged; `status: converted`, `debt_ref: ""`.
2. `acceptance.py`: `from gate_template import acceptable` (the form `gate_preflight.py:87` uses); the four review comparisons of
   `validate_window` are `acceptable(item.get("review", {}).get("verdict"), "<consumer>")` (stopped and gapped `static_review`, handed
   `handed_review`, ran `review`); branch order, `_bound_to`, `stale_review:`, `mechanical_green:` untouched; `HANDED_REVIEW_VERDICTS`
   deleted (Grep over `ai-packages` and the whole tree: no reader left; `BLOCKED_REVIEW_VERDICT` kept, `window_record.py:75` imports it).
   C3-b1's `novelty_question` block is byte-identical (diff touches only lines 11, 34-35 and the four review lines).
3. Behaviour preservation: six-window control below, EQUAL.
4. Unreadable registry: `acceptable` returns False for every word, so `validate_window` gives `review:<iid>` for every kind (table rows
   "E3"). See question Q1 about the words "the gap names the registry".
5. ONE table `c3_d_review_word_through_the_registry` in the existing `test_window_record.py` (24 kind/word rows + the E3 rows for every
   word the table closes), called first in `pure_group`. Expectations from the card item 5, the corrected `decides`, the charter
   (`agents/qa-code-critic.md:76,84`) and FR-59, not from the code. Added beyond the card's list: `approved_with_fixes` on handed, `""`
   and the absent key on stopped / gapped / handed, `" approved"`, `["approved"]`, `None` on ran (edges E2, E5). Item 6: no row (the
   pin exists, `test_window_record.py` `expectation changes not measured: ` lines).
6. S-f pins of `test_gate_registry.py` (own row only): `EXPECTED_DEBT` loses `s5_window`; `EXPECTED_CONVERTED` gains it;
   K-T1.2 `"5 gate(s) left as debt:"`; K-T1.14 split 22 / 5 / 6 with its comment line; the F4 `code` list gains `s5_window`;
   `D13_TRIPLES` + `("window_record.py", "build", "s5_window")`; `D13_ITEM_COUNT` 145 -> 146 with a comment in the form of the file's
   other lines. D13 measured with `GR.analyse` AFTER: 146 items / 50 triples; the s5_window items are exactly one:
   `window_record.py:1649 build  item['review']['verdict'] != 'approved'` (card: "exactly :1532 ..."; the line moved with C3-b1). The
   base 145 / 49 is the pin on the base main (the test passed on it before my edit; I did not re-run a "before" `analyse`).
   The F4 flip control already runs on an in-memory copy row (C3-0), untouched.
7. Census untouched: `validate_window`'s unit and class unchanged (no refusal site added: the gaps are list transport);
   `test_judgment_census.py` run, see section 3.

## 2. Six-window control (before = byte copy of the old `acceptance.py`, sha256 `eb0e4315d9608bf4ea778dae7e93dd3431cd38d9af8ed0cab1b6ad09936b2a56`)

Script `scratchpad/control.py`: loads the BEFORE copy and the live `acceptance.py` side by side, calls
`validate_window(window, fixtures/stories/cart-1)` over `fixtures/stories/cart-1/work/windows/S5-qa-code-critic-{2..7}.json`.

```
before 6 windows gaps: 20 sha256 1a7bcdb1754ef8e17e0887fade02fb975366558a9a0fb83c01fe4d8ac7cf45b9
after 6 windows gaps: 20 sha256 1a7bcdb1754ef8e17e0887fade02fb975366558a9a0fb83c01fe4d8ac7cf45b9
EQUAL
(-2 equal 12, -3 equal 4, -4..-7 equal 1 each)
```

Limit (as the card says): the recorded windows exercise the probe-gapped branch and one ran instance; stopped and handed rest on the table.

NEGATIVE control (the consumer broken: `"s5_window.review": ["matched"]` narrowed to `[]` in the registry, on the live file with a byte
copy taken before, `registry_good.json`):

```
before 6 windows gaps: 20 sha256 1a7bcdb1...45b9
after 6 windows gaps: 21 sha256 9e6cef2d67b0a1f868a9286d49ae92417ca9d7d2e016b9de9a205e33d8809138
DIFFER      (S5-qa-code-critic-6.json DIFFER 1)
FAIL C3-d ran / 'approved': review gap -- expected False, got True      (test_window_record.py pure: 537/538)
```

Restore by `cp registry_good.json <registry>`: `sha256sum` of both = `8d12df74ba347c7907f1f7d2fe78b1eedec4be5d6ebd9e013d7f4a6a3713a945`,
`cmp` -> IDENTICAL.

## 3. Verification (verbatim tails)

```
$ python -B ai-packages/qa-factory/scripts/gate_registry.py --check            exit=0
A26 gate registry: no violations
  5 gate(s) left as debt:  stand_identity, provenance_acceptance, test_identity, baseline_identity, s5_stand_limits   (s5_window absent; no F-b)
$ python -B .../scenario_walk.py --witness-for <acceptance.py, gate-registry.json, test_window_record.py, test_gate_registry.py>
  printed 34 files; slow among them: test_window_record, test_gate_registry, test_blocked_by_env_window, test_needs_author, ... (not run, canon),
  non-slow each run ALONE:
    test_check_witness 34/34 | test_handed_to_person 58/58 | test_interim_packet 54/54 | test_manifest_put_merge 481/481
    test_probe_by_code_languages_plan 502/502 | ..._ts_playwright 189/189 | test_probe_not_proved 47 passed | test_probe_readers 16 passed
    test_probe_target_fact 13 passed | test_quality_demand 84/84 | test_run_freshness 96/96 | test_s5_precheck_sides 201/201
    test_scenario_walk 95/95 | test_scenario_world 33/33        (all exit=0)
  as this change's own judges, though slow:
    test_window_record.py   === window record: 722/722 ok ===   exit=0
    test_gate_registry.py   === test_gate_registry: 494/494 ok === exit=0
    test_judgment_census.py === judgment_census: 25/25 ok ===   exit=0
$ python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang       exit=0
PASS limits: every mandatory role rule of design/role-rules.json holds in its carrier
=== qa-factory selftest: 4/4 ok ===
```

## 4. FR walk (touched sections)

A (refusals): no refusal text touched; the review gap and its door are as before. FR-4: a person's word on `review:<iid>` is S9's road,
untouched. C (contracts): FR-13 the accepted words are data (the row), not a code list (AR-1, AR-13); FR-38 n/a. D: FR-59 / FR-58 the
unknown (absent, other word, unreadable registry) is never a pass, pinned by the table; the expectations are from the card and the
charter, not the implementation (FR-58). E, F: no report text or measurement changed (FR-41: the unmeasured detector's INFO line stays INFO,
direction (i)). G: FR-30 changelog fragment ASCII English (`selftest --lang` exit 0); FR-31 the table is deterministic (temp dir, patched
readers restored in `finally`); FR-32 root cause = a literal word list beside the registry; FR-54 siblings by the map: below.
B: no human-facing text changed.

## 5. Siblings and waiting findings (not fixed, not in owns)

axis 25: `run_freshness_of(item)[0] == "stale"` named, unchanged (C3-b2's). axis 32: census unchanged. axis 34: S9's road untouched. A1's class:
`window_record.build` registered `produce`. axis 5 prose twins walked (each checked, no edit - meaning unchanged):
`skills/qa-story/phases/s5.md:162` (`unverified` for a probe that cannot run) and `:184` (the critic's `approved` stands);
`references/code-review-rubric.md:92-93` (`unverified` is not a pass). Further hits of the row id: `design/factory-rules-debt.md:106` still lists
gate `s5_window` as debt ("conversion owed ... owner B-179") - STALE after this node; the card's S-d says the debt file is not edited, S1b moves
the row: finding for S1b. `docs/SIBLING_MAP.md:161,589` hit `s5_window` only as function names (`branch_accounting._s5_window`): not the row.
R12 waiting findings (reported, not fixed): (a) `probe_verdict` words accepted in `validate_window` (`probe.get("verdict") != "intended_failure"`)
and in `proof_level` need a function split (`gate_registry.py:831-836`); (c) the critic's review word is read outside the registry:
`check_delivery.py:860`, `case_stamp.APPROVING`, twin `report_facts.APPROVING` accept `{approved, approved_with_fixes}`, and
`window_record.build` (`!= 'approved'`, now a registered produce site and a counted D13 comparison) plus `window_record.py:1641,1742`
(`!= BLOCKED_REVIEW_VERDICT`, invisible to A26) and `GAP_ORIGIN["review"]` carry the per-kind rule as door text: copies beside the registry.
Same-class note found while reading: `acceptance.validate_window` uses `item.get("review", {}).get("verdict")`, which raises
AttributeError for a `review` that is not an object (as before; not changed, behaviour-preserving).

## 6. Deviations, questions, telemetry

- Deviation from the card text: D13 line number of the new comparison is `window_record.py:1649`, not `:1532` (the file moved with C3-b1);
  the triple and count are as the card expects (+1, 145 -> 146).
- Q1 (a card/dispatch wording, left as the card's item 4 / E3 says): the dispatch's restatement (4) says "the gap names the registry". The card's
  items 4 and E3 give the gap `review:<iid>` for an unreadable registry ("the per-site why branches are belt-and-braces"), and I implemented
  that: a gap string is a `kind:instance` token on the window's word road, so naming the registry (`gate_template.registry_problem()`) in it
  would need a new gap shape or a changed door text in `window_record.py` (not owned). Decision wanted: is `review:<iid>` enough
  (C3-reg-precondition stops the stage before it), or should the review gap's door text name the registry?
- tests-over: the row table of card C3-d item 5 (+52 lines in `test_window_record.py`, one function, no new file).
- Needed beyond the manifest: `scripts/gate_preflight.py:87,3844` (the import form of C3-rr), `scripts/tests/test_gate_preflight.py:5199-5234`
  (the `GT._READ` seam), `scripts/proof_level.py` (`proof_required`), `scripts/slow_tests.json`, `docs/SIBLING_MAP.md`,
  `skills/qa-story/phases/s5.md`, `references/code-review-rubric.md`, `design/factory-rules-debt.md`, `changelog.d/README.md` and
  `rules-debt-c3-rr-rehearsal-reuse.md`.
- Hook/permission refusals: none against the work (the Bash tool refused only chained commands that moved cwd or used a form it could not
  verify; I split them).
