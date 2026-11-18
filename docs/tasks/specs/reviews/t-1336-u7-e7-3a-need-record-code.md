# t-1336 - code review of E7-3a (need record), branch `worktree-u7-e7-3a`, commit 939fae9f over origin/main 1278f0dc

## Verdict

**REJECT** (`failure_class: code` for B1 and B3; B2 is `spec`: M3 and the item-4 invariant conflict). There are three blocking findings, and each has a local fix. The design is sound: the one rule, the validator branch, the M14 refusal road and the Q-B words. In the dispatch's three words this is REJECT. Once B1-B3 are fixed, the remaining items are fixes and notes.

Blocking: B1 (the G5 JSON-reader census goes red on `prepared_request`), B2 (a stale or refused need record on a PREPARED case tells the person "the factory could not prepare this check"), B3 (the `write-block` hand road gets an honoured need record on a prepared case, with `walked: true` on the runner's word and no recorder step, so the case becomes `after_checks`).
Fix before merge: F1-F5. Notes: N1-N7.

## DoD items 1-6

1. `manual_evidence.py`: **holds, except B1/B3.** `NEED_REASON` is byte-equal to spec §2.2. `prepared_request` matches its contract but trips G5 (B1). `need_record_problems` never raises on junk (probe (c) below). The one new raise: `write_unprepared` raises a single `ValueError("; ".join(problems))` before any write. `_cut` at 300/301 holds. The record shape holds for no marker, for a factory marker (its reason stays, the need is added; probe) and for a need with no walk (`not_walked` = `need_why`). `unprepared_rows` follows M3. A record without a need is byte-identical: the dict, the key order and `source` = marker are all the same as before. The CLI flags are hidden (`argparse.SUPPRESS`). `record_from_walk`: the kwargs are passed only with `needs`, M14 holds (see (e)), and `walk_rule_errors` uses the need branch instead of `_result_errors` (live rig probe). The CLI wiring has no test row (F3).
2. `_validate_unprepared` (N6): **holds.** It refuses: other ids, an edited reason, a need outside the set, a need with a result, a refused / missing / unreadable request, and junk needs (`[]`, `{}`, `0`, `""`; probe). It never verifies `walked` or `need_why`, which leads to B3.
3. `walk_session.py`: **holds.** None, a list, 1, "other" and "" are all refused (test row). A str `needs` is copied.
4. Q-B words: **text holds** (`check_delivery.py::unprepared_records` matches §2.6 for HEAD, WORLD and the not-walked tail). **The INVARIANT is broken in the M3 world (B2).**
5. `state-exits.md`: **holds.** The row sits in § The run's own records with its way out, and `test_state_exits.py` gives 142/142.
6. Ratchets (Q9): **holds.** `told-ratchet.json` `manual_evidence.py::write_unprepared` bare 4 -> 5, the one new refusal. The diff greps to exactly one `+ raise` line. The census row `need_record_problems` is class shape, roles qa-runner. No other raise was added in `coverage_contract.py` or `walk_session.py`. The commit message does not name the raise; no builder report was attached (see "Mechanical layer").

## Edges

- Old records read as today: **holds** (byte-identity traced; the "no need" row).
- A markerless need over a missing / refused / other-ids request -> issue: **holds** (rows, plus my probe on an unreadable request.json).
- CLI battery: through the function, **holds**: 300 kept whole, 301 -> 299 + "…", nothing written on refusal, whitespace why refused. Through `main`, **not tested** (F3). A blank `--need-why ""` without `--needs` is accepted silently (N3).
- Walk verdict battery: `verdict_problems` **holds** (row). `walk_rule_errors` with needs + a pass Then, or needs with no limitation, is refused while the session lives: **holds by probe, no row** (F2).
- Factory-unprepared + need keeps the marker: **holds** (probe: `{'reason': 'no driver', 'need': ..., 'walked': False, 'not_walked': 'two phones'}`, validator `[UNPREPARED]`). No row; the card dropped it by budget.
- M3, stale / refused -> no need keys: **holds** in `unprepared_rows`. The delivery words that follow from it are false on a prepared case (B2).

## The doubts (a)-(g)

(a) **Holds.** Walked through `check_delivery.assess` (scratch, the 7c world with a need marker on TC-002): walked -> `after_checks`, reasons `[]`, the obligation excused. Not walked -> `no`, coverage reason kept. Stale / refused -> `no`. That is 7c's rule. `_unprepared_scan` adds no `evidence_errors` test, but a refused row always carries `result` (finalize_task.py:571), so it stays out.
(b) The words in the window are true except in the B2 case. A need record can do what a plain unprepared record cannot: put a PREPARED case on `after_checks`. On the code road that is the softening §3 accepted. On the `write-block` road it needs no walk at all (B3).
(c) **Holds**: no raise for None / list / dict / int / bytes, or for an unreadable request. A dict `need_why` passes as "said why" (`_squash(str(dict))`), but the walk road always gives a str (`walk_session._joined_limitation`), and so does the CLI. Note only.
(d) `_cut` is identical to the old expression for every length 0-699 (probe). The whitespace rule exists only on the CLI/function road: on the walk road, `limitation` without `needs` is an ordinary field, so the rule never applies there. A blank `""` without a need is accepted while `"   "` is refused (N3).
(e) **Holds.** The pass/fail check runs before `write_unprepared`, on both request kinds (row with a None and a dict marker). `{"refused": ...}` reaches `driver_dispatch.py:1480` -> `walk_refusal` -> `walk_retry`, today's road.
(f) Changelog: **change it.** It names the hidden flags, while §3 says "in no page and no help until E7-2". It also says the record is honoured "only over a prepared request", but a need over a factory-unprepared request is honoured too. Suggested text: "manual runs: the run record and delivery words know a check that needs another instance of the stand or device (no role is told of it yet; nobody is asked)". The file is outside the owns; keeping it is the Lead's call (Q3).
(g) **Holds.** Readers checked (the grep is below; it found every known reader, which serves as its own positive control): `coverage_contract.py:663-667,703` (reads `reason` only), `:757,790`; `contract.py:4694` (`is not None`); `finalize_task.py:543,553,556,569`; `manual_evidence.py:1274,1319,1349,1476`; `s7_pretriage.py:163`; `ledger.py:1709`; `check_delivery.py:1991`; `driver_dispatch.py:1485` (the build answer, not the marker). No `marker ==`, `.keys()`, `.items()` or iteration over an unprepared marker. The same regex found `red_sandbox.py:459` `for target in marker.get(...)`, which is the positive control of its shape.

## Findings

**B1 (blocks) - `manual_evidence.py::prepared_request` is a new raw JSON-reader twin (SIBLING_MAP axis 16; `test_read_json.py` G5 goes red).** The body is one Try (`json.loads(... .read_text())`) plus `return`, with a quiet handler, so `_reader_shaped` is True and the function is not in `KEPT`. Repro: `census()` on base `manual_evidence.py` -> `{}`; on the branch -> `{'manual_evidence.prepared_request': 'manual_evidence.py:1281'}`. `census_verdict(found, KEPT)` over the worktree scripts gives `(['manual_evidence.prepared_request'], [])`. The narrow DoD does not include `test_read_json.py`, so CI's batch would go red. Fix: `data = hooklib.read_json(request_path(task, case), None, kind=dict, errors=Exception)`. This also answers Q6: it reuses the one reader instead of adding a fourth reader of request.json.

**B2 (blocks; spec conflict) - a stale or refused need record on a prepared case gets "the factory could not prepare this check" (`manual_evidence.py::unprepared_rows` + `check_delivery.py::unprepared_records`).** Under M3 the row carries neither `need` nor `prepared`, so it takes today's branch. Repro (scratch `assess_need.py`, run on the 7c world): row `unprepared={reason: NEED_REASON, need, need_why, walked: True}` with `current_reason: "stale"`, or with `result: inconclusive, evidence_errors`. Output: `to_check: "the factory could not prepare this check and the agent walked it without a result: needs another instance ..."`, verdict `no`. On main this row cannot exist, because a prepared case never holds an honoured unprepared marker. So 3a creates the false sentence that item 4's INVARIANT forbids. M3 ("today's delivery words") and the invariant contradict each other for prepared cases. Proposed fix, which needs the architect's word since it amends M3: keep `prepared` (reason == NEED_REASON) on every row whose marker carries a need, and withhold only `need`/`need_why`/`ended_at`, the keys the S7 step acts on. In `unprepared_records` a `prepared` row without `need` then gets a true head, e.g. "the factory prepared this check; the runner's record that it needs another instance was not accepted: <reason>".

**B3 (blocks) - the hand road honours a need record with `walked: true` on the runner's word (`coverage_contract.py::_validate_unprepared`, `manual_evidence.py::write_block`).** Repro (scratch `hand.py`): prepared case, `_recorded_walks` = `[]`, `write_block(task, [{..., "obligation_ids": ["OB-7"], "unprepared": {"reason": NEED_REASON, "need": "another_instance", "walked": True}}], declared=True)` -> written. The same record with a plain marker -> refused "unprepared marker without an unprepared request". `_unprepared_scan` then counts the case as walked, so it becomes `after_checks` and the obligation is excused, with no step on disk and no `need_why`. This breaks P26 / the `_unprepared_scan` premise ("`write_unprepared` always writes a bool" from disk) and AR-28. The same hand-road gap already exists for factory-unprepared markers (7c); 3a extends it to every prepared manual case. Fix inside the owns: for a markerless need, the validator requires `walked is True` only when `_recorded_walks(task, case)` is non-empty, and requires a non-blank `need_why`, i.e. it asks `need_record_problems` as that function's docstring already claims. Closing the older factory-unprepared twin is a node for the Lead (Q4).

**F1 (fix) - `need_record_problems` docstring says "the CLI, the walk rule and the validator ask it", but `_validate_unprepared` does not call it.** Either the docstring is a false claim or the validator is missing the call. B3's fix makes the docstring true.

**F2 (fix) - no row for `walk_rule_errors`' need branch** (the verdict door while the session lives: needs + pass -> `NEED_THEN_PROBLEM`; needs with no limitation -> "a need says why"; `_result_errors` skipped). The card's edge names this branch. I checked it by probe (`wre.py`: the four verdicts give exactly those lines and `[]`). Deleting the branch would fail no test.

**F3 (fix) - the "CLI battery" rows call `write_unprepared`, not `main`.** `--needs` choices, `--needs ""` / `ANOTHER_INSTANCE`, and `need=args.needs or ""` wiring (`manual_evidence.py::main`) have no row. If the wiring were dropped, no test would fail. Fold one `main([...])` call into the existing loop. Budget room: tests 81 vs product 118 added lines.

**F4 (fix) - unexplained edit to 7c's row** (`test_check_delivery.py` line 2339: `"plan_row": "TS-2"` removed from the TC-003 manifest entry). The 7c scenario passes on the branch both with and without it (my two runs: 0 fails each). Revert it, or name why (Q5 d).

**F5 (fix) - changelog fragment text**, see (f).

**N1** `record_from_walk` with `needs: ""` (only possible when the session check is skipped) leaves today's road: a factory-unprepared case with no walk is refused ("say why with --not-walked") where today it would write "the walker ran no step for this case"; a prepared case is refused instead of built. Safe direction. Use `if needs:` instead of `isinstance(needs, str)`.
**N2** `--needs` over a refused request answers "has no prepared request" and loses the refusal's own door words (`_load_request`).
**N3** `--need-why ""` without `--needs` is accepted, while `"   "` is refused and `--not-walked ""` is refused at the CLI. Make it one rule.
**N4** A later need record (CLI) supersedes an earlier `fail` build of the same case and obligation (finalize: latest per `case::oid`). That turns a red into `after_checks` when walked, which goes beyond what an inconclusive rebuild does today (`no`). Architect question Q2.
**N5** Duplication inside the diff: the obligation-id comparison is repeated in `_validate_unprepared`, and the success dict is repeated in `record_from_walk`. `verdict_problems`' message hardcodes `another_instance` instead of naming `INSTANCE_NEEDS`.
**N6** The commit's `architecture:` line omits AR-28 (an unknown never becomes a pass: `after_checks` on a prepared case) and AR-27 (delivery words). `judgment: none` while adding a census row; `adds data check` would be the exact form (the row is honestly shape).
**N7** 7c's `current_unprepared` docstring ("the factory could not prepare") is now incomplete. It is outside the owns (non-goal), so this is a note.

Seam (Q3): additive in all seven owned files. `test_check_delivery.py` (Q-B moved it in) and `changelog.d` are outside the card's owns. Q4: axis 16 (B1); the factory-unprepared hand-road twin of B3 is a node for the Lead. Q6: B1 (the reader), N5. Q7: no new function over about 60 lines (`write_unprepared` is about 55). Q8: the ellipsis predates this diff; no Cyrillic in the diff. Q10 VARIETY: a project with no stand or device gets no new block; the closed word is a data tuple. Q11: one shape row, honest. Q12: none found. I read the whole product diff for language, runner or project names; there are none.

## Questions for the architect

1. B2: amend M3 so that `prepared` survives on refused or stale need rows (true words), or accept another wording for them?
2. N4: may a need record supersede an earlier pass/fail record of the same case, or should `write_unprepared` with a need refuse when a current result record exists?
3. B3: is the validator's walked-versus-disk check also wanted for factory-unprepared markers (7c's twin), as a node?

## Mechanical layer

No builder report, DoD tails, `red-before:` line or `forge-check` result was attached to this dispatch. **Request:** the builder's handoff. I re-ran the cheap DoD files myself (below). The ratchet job was not read, because none was attached.

## Trail

Read: both given files (§0 amendments, §2.2, §2.6, §3, card E7-3a; t-1307 M3/M10/M13/M14/Q-B/N6). Full product diff and test diff. `manual_evidence.py` 1267-1384, 1450-1490, 1587-1796. `coverage_contract.py` 300-310, 630-710, 751-800. `check_delivery.py` 1960-2015. `finalize_task.py` 520-590. `driver_dispatch.py` 1455-1500. `walk_session.py` verdict callers, `_joined_limitation`. `ledger.py` unprepared lines. `design/architecture.md` AR-13/27/28. SIBLING_MAP axis 16. `test_read_json.py` 440-505. `tools/architecture_gate.py` head.
Runs (verbatim tails):
- `python -B <wt>/scripts/tests/test_manual_evidence.py` -> `=== test_manual_evidence: 293/293 ok ===` (12.3 s)
- `pytest test_walk_record.py::test_verdict_needs_goes_to_write_unprepared_with_the_need ::test_verdict_needs_is_one_word_or_absent ::test_unprepared_goes_to_write_unprepared -q` -> `3 passed in 9.80s`
- `python -B <wt>/scripts/tests/test_state_exits.py` -> `=== test_state_exits: 142/142 ok ===`
- scratch `run7c.py` (7c scenario + Q-B rows) -> `fails []`; same with `plan_row` restored -> `fails []`
- scratch `assess_need.py` -> walked `after_checks`; not walked / stale / refused `no`; the stale and refused `to_check` start "the factory could not prepare this check" (B2)
- scratch `probe.py` -> junk never raises; `_cut identical: True`; factory+need marker kept; hand record honoured `['unprepared walk: no result is bound']` vs plain marker refused
- scratch `hand.py` -> `need, walked by word -> written ...manual-4d4f....json`; `plain marker -> refused`; `recorded walks: []`
- scratch `wre.py` -> needs+pass `['a check that needs another instance gives no Then a pass or fail']`; no limitation `['a need says why ...']`; ok `[]`
- scratch `g5.py`/`g5b.py` -> `offenders: (['manual_evidence.prepared_request'], [])`; base `{}`, branch `{'manual_evidence.prepared_request': 'manual_evidence.py:1281'}`
- grep readers: `grep -rniE "\[.unprepared.\]|get\(.unprepared.\)|unprepared_rows\(|unprepared_walks" scripts --include=*.py`; key-iteration grep `marker\s*==|marker\.(items|keys)\(\)|for \w+ in marker\b` -> only `red_sandbox.py:459` (control)
- budget: numstat product 118 added, `scripts/tests/` 81 added -> holds

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 manual_evidence.py::prepared_request is a new raw JSON reader (axis 16): test_read_json G5 census offenders ['manual_evidence.prepared_request'] - use hooklib.read_json",
    "B2 stale or refused need record on a PREPARED case: unprepared_rows drops prepared (M3) so check_delivery.unprepared_records says 'the factory could not prepare this check' - breaks the item-4 invariant; M3 amendment needs the architect",
    "B3 write-block hand road: a markerless need record with walked true and no recorder step is honoured by _validate_unprepared, so the prepared case reaches after_checks on the runner's word (P26, AR-28)"
  ],
  "fixes": [
    "F1 need_record_problems docstring claims the validator asks it; it does not",
    "F2 no test row for walk_rule_errors need branch (needs+pass, needs without limitation)",
    "F3 CLI battery rows call write_unprepared, not main: the hidden flags' wiring has no row",
    "F4 revert or explain removal of plan_row TS-2 in test_check_delivery 7c row (passes either way)",
    "F5 changelog fragment names hidden flags and says honoured only over a prepared request"
  ],
  "class_completeness": "Axis 16: prepared_request joins the JSON-reader twins (B1). B3's hand-road gap has an older twin on factory-unprepared markers (7c), a node for the Lead. Readers of the unprepared marker checked: coverage_contract 663/757/790, contract 4694, finalize_task 543-569, manual_evidence 1274/1319/1349/1476, s7_pretriage 163, ledger 1709, check_delivery 1991; none compares or iterates marker keys.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261118-u7-e7-another-instance-spec-r2.md",
      "docs/tasks/specs/reviews/t-1307-u7-e7-plan-r2.md",
      "ai-packages/qa-factory/scripts/manual_evidence.py",
      "ai-packages/qa-factory/scripts/coverage_contract.py",
      "ai-packages/qa-factory/scripts/check_delivery.py",
      "ai-packages/qa-factory/scripts/finalize_task.py",
      "ai-packages/qa-factory/scripts/driver_dispatch.py",
      "ai-packages/qa-factory/scripts/walk_session.py",
      "ai-packages/qa-factory/scripts/tests/test_read_json.py",
      "ai-packages/qa-factory/design/architecture.md",
      "docs/SIBLING_MAP.md"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_manual_evidence.py", "result": "293/293 ok"},
      {"command": "pytest test_walk_record.py (3 node ids)", "result": "3 passed"},
      {"command": "python -B scripts/tests/test_state_exits.py", "result": "142/142 ok"},
      {"command": "scratch G5 census over worktree scripts", "result": "offenders ['manual_evidence.prepared_request']"},
      {"command": "scratch assess_need.py", "result": "stale/refused prepared need row: 'the factory could not prepare this check'"},
      {"command": "scratch hand.py write_block", "result": "need record walked by word written; plain marker refused"}
    ]
  }
}
```
