# t-2000 critic on the probe batch (head 46d7e4672), extracted by the coordinator

# t-2000 — critic on the mutation-probe batch (spec t-1968), head 46d7e4672 of fb-fix

**The report is NOT on disk.** `tools/handoff_gate.py` refused the path on `handoff:` (`docs/tasks/reviews/...`), because it accepts only `docs/tasks/specs/reviews`. Per critic rule 16 the full verdict is here. Extract it with `tools/handback_extract.py`, and use `docs/tasks/specs/reviews/` on the next dispatch.

**Verdict: fit_with_fixes.** 3 blocking findings (F1, F2, F3), 5 to fix in the same round (F4-F8), 3 SPEC items for the Lead (S1-S3), 2 low (L1, L2).
The core stands: the marker, the critic's judgment and the separate question all work, and code never records a foreign message at the mutated line as proved.
Acceptance is the Lead's decision. Line numbers are of head 46d7e4672; `PKG` = `ai-packages/qa-factory/scripts/`.

## Findings

**F1 (blocks) — a `probe gap: <case>` word closes a test the critic has not judged.** `PKG/window_record.py:696` `probe_gap_block` (the equality `named = next(...)` after the cannot-judge branch) and its twin `PKG/acceptance.py:908-913` `probe_gap_named`. Surface: the person's word over a probe record.

Scenario: the case got `probe gap: CASE-A` for a tooling probe. The stand is fixed, and the re-probe of the same case ends `incomplete`, `cause: judgment`, no judgment. Run (temp dir, real functions):
```
owes: unjudged could_not_run: False
1 unjudged block: {'verdict': 'incomplete', ... 'named_by': 'CASE-A', 'words': 'go on', 'at': '2026-11-05T09:59:59+00:00'}
1 named: {'the test': {'key': 'CASE-A', 'words': 'go on', ...}}
1c cannot_judge control: None
```
- **Effect:** the window closes with no `--judge`, on a word about other facts (no `at` check here).
- **Breaks:** «про мутационные пробы должен решать критик», spec N2 item 7 ("an unjudged record is the critic's") and E3.1 ("no gap is named for it"). F4 makes it reachable by following a refusal.
- **Fix:** in both twins read `probe_owes_judgment` first; `unjudged` means no block and not named, whatever the word. Add a test in `test_probe_not_proved.py` beside `test_go_on_for_tooling_never_covers_cannot_judge`. Executor: fix round of this batch, not a queue line.
- **Neighbours walked:**
  - instance word: same hole, same fix
  - `tooling:` word: closed, `tooling_gap_key` is "" for `judgment`
  - class word: closed, `probe_could_not_run` is False
  - older word: the fix covers it
  - broken stamp: closed for the new word

**F2 (blocks) — `--judge` accepts any open dispatch, including the test's author.** `PKG/probe_by_code.py:4254-4258` `judge_record` calls `_dispatch_context`, whose `find_active_dispatch` (`PKG/execution_request.py:871`) answers only "there is one". Its refusal says "not the open code-critic dispatch", but the check never looks at the role. Spec N2 item 3: "`--dispatch` not the open S5 critic dispatch of the instance's window". Run:
```
5 running: ['S5-qa-automator-1']
5 fad: qa-automator          (scope ["OTHER"], asked for case CASE-A)
```
- **Consequences:** an automator, or a running S6 dispatch (`s6_reprove` passes one, G9), can write `fires` and a live receipt for its own test. A critic of another window can too.
- **Guard:** none found. `grep -ln probe_by_code references/*.json hooks/*` lists reference data only (positive control: `ahead-cards.json` matched) and no hook path. I did not read the hook directory separately. Only the critic's charter names the tool among agents, so what remains is discipline.
- **Why tests miss it:** `test_probe_marker_judgment.py:78` stubs `_dispatch_context`.
- **Fix:** `judge_record` takes the dispatch row from `find_active_dispatch` and requires `role == qa-code-critic`, stage S5 and the record's case in `scope` (a `parent_retry` ancestor keeps working through the same reader). This is a data check (AR-29), with a door in the refusal. Add an unstubbed test per refusal.

**F3 (blocks) — an off-target probe still publishes `sensitivity: proven`, and the case stamp counts it.** `PKG/probe_by_code.py:4099` `_binding_items`; `publish_binding` has no off-target check. The `receipt_off_target` call sites are `acceptance.py:1095`, `probe_by_code.py:4046`, `proof_level.py:1441`, `window_record.py:565` (the positive control of that grep).
- **Reader:** `PKG/case_stamp.py:486` `_sensitivity_receipt` asks `reached` first (off-target gives no level), then falls through to any `proven` binding and returns its `probe_receipt_ref`.
- **Effect:** a test whose probe broke another line can be stamped `Automated` with that receipt, against spec §1 ("a probe of another line never counts") and N4 item 2 ("a binding publication never counts it"). Traced by reading, not run.
- **Not a second leak:** `coverage_contract.witnessed_binding` re-validates the window, so I do not count it.
- **Fix at the root:** `_binding_items` does not set `proven` when `receipt_off_target(record)`. The row's `sensitivity_proof` stays, so the window keeps its off-target door. Test: off-target record gives a fragment with no `proven`; on-target has it.

**F4 (fix now) — the refusal names the wrong door.** `PKG/controller.py:6386-6391` and `:6569-6573` print `PROBE_GAP_RECORD` ("passed only by the person's word") for every owed green item, `cannot_judge` and unjudged included. For `cannot_judge` the word does nothing (FR-2, FR-37, a wasted round). For unjudged it is the road of F1. Answer to Q3(b): the N5 builder is right, and it is worse than a missing line.
Fix: build the door from the window: the critic's `JUDGE_DOOR` for unjudged, `NOT_PROVED_RECORD` plus a keys line (from `probe_judgment_cases`) for `cannot_judge`, the old door only for the rest. One helper in `window_record` beside `probe_gap_keys_line`.

**F5 (fix now) — the person reads the factory's own marker expression instead of the check.** `PKG/story_run.py:5977` over `statement_after`. Rendered with the real statement of `add_to_cart.spec.ts:43`, marked as N1's test pins it:
```
the check broken at line 43 (`await expect(catalog.cartBadge, ['qa-probe', 'abc123def456'].join('-') + ' ' + 'step 1: badge empty before the add').to…`)
```
About 47 of the 120 characters are ours, and the cut eats the matcher, the one thing that says which check was broken. Owner's word: with the facts (which check was broken); P9. `human_text.shape_problems` returns `[]`, so nothing catches it.
Fix: `judgment_facts` also carries `statement_inverted`; `cannot_judge_facts` and `probe_judgment_cases` hand it to the lead. Update the key-set pin `test_judgment_facts_shape_and_cut` and add a test with a marked statement.

**F6 (fix now) — dead readers of the removed producer (AR-22).** `PKG/controller.py:6632,6637` filter `key` by `startswith("factory:")`; `PKG/window_record.py:1669,1681` hold `by_factory`. N2 removed the factory branch that produced these keys. `test_no_reader_of_data_row_left` scans other words, so it missed them. Fix: remove both and add `factory:` to the scan. Also in the Q5 class.

**F7 (fix now) — docs do not name the new word.**
- `skills/qa-story/phases/s5.md` names the question but not `probe not proved:`, and by the spec's exact text it carries the literal "(N5)", a spec node nobody reading the package can resolve.
- `design/state-exits.md:71` has the row for an accepted probe gap and none for the new word (positive control: the same grep matched `probe gap` there, `probe not proved` nothing). A person's change of mind has no named exit (FR-40, AR-25).
- Fix: a sentence in s5.md, a row in state-exits.

**F8 (fix now) — the N1 report's environment negative is false, and E1.13 can be closed.** t-1977 says "no Playwright install on this machine". `mybooks-stand/tr-arm-b/node_modules/playwright` exists, version 1.56.0. What its source says:
- `lib/matchers/expect.js:237-238`: only Jest-shaped errors get the custom message, so a throw inside the arguments has no marker (safe).
- `toMatchText.js:37,67` + `matcherHint.js:51`: an engine `errorMessage` goes inside the Jest-shaped error, so it may carry the marker. That is the named residual; I read this and did not run it.

Fix: a builder runs one sample on the stand and writes the result in the docstring the spec asks for. M-TS1/M-TS2 were also never run, so §6 live proof is their only witness and stays owed before the batch closes.

**S1 (SPEC) — measured: 30 of 44 real probes are off target.** `tr-arm-b/qa-factory/artifacts/LOCAL-1/work/probes/*.json`, `mutation_detail.line` vs `assertion_id`: `records 44 on-target 14 off-target 30`, e.g. `cart.spec.ts:113` (`'Then 1: VALIDATION_ERROR'`) vs probed `:112` (`'Then 1: 400'`).
- The field's semantics hold (it names a Then's own check, not the first assert). §6 predicted this for TC_001 only.
- Each such probe spends a full test run for a receipt that can never count. The fact is known at plan time: `probe_by_code.py:3273` notes it, then runs. The charter tells the critic about `--at` only afterwards.
- For the Lead: a charter or ahead-card line "aim `--at <assertion_id line>` from the first probe", or the probe stops before the run with the door (a refusal; the non-goal "no default `--at`" stays). Cost: P11, AR-12. Recommendation: the charter line now, inside the ratchet slack.

**S2 (SPEC) — "N5's word" does not close an off-target test, and on Python there is no `--at` at all.** Spec N4 item 3 and the AR-25 row say "`--at` or the person's word". Run: `4 off-target word block: None`, so the probe block stays and, by reading `validate_window`, so does `semantic_sensitivity`.
- `OFF_TARGET_DOOR` (`window_record.py:555`) says "the person decides", but the road I traced is `finish --unresolved --reason` by the role (`story_step.py:32`, `controller._s5_gap_problems`), with no person's question. Delivery then says "requires current sensitivity proof" (safe direction, not a dead end).
- `--at` is refused on Python (t-1978), so a Python test whose first assert is not its `assertion_id` loses a proof it had before.
- Lead's choice: widen the word to off-target, or say the true road in the door. Recommendation: the second, and name the Python residual to the owner.

**S3 (SPEC) — a case holding both kinds gets neither question.** Spec item 4 ("every owed green item is `cannot_judge`") conflicts with E5.4 ("both kinds owed in one window → this question first"). Run with one `cannot_judge` and one tooling test in one case: `2 mix judg: []  gap: []`, so the seam gets its fallback question with no facts. Recommendation: list the case when every owed item is `cannot_judge` or could-not-run, showing only the `cannot_judge` tests; the word names those only.

**L1** `test_probe_marker.py:346` `assert library` asserts nothing.
**L2** `judgment.facts_sha` is written and no package code reads it back (`grep facts_sha`: definition and the one write in `scripts/*.py`). Keep it for the acceptor or drop it.

## Answers

**Q1.**
- **Marker:** kept (`judge_detector`, exact token, `failed` rows, failure/error body only).
- **"Critic decides":** kept for the judgment itself, broken at two edges (F1, F2).
- **Separate question with facts:** kept (N5; the tooling word never covers it, run `1c`), but see F5 and S3.
- **Lead's correction: holds.** Failed at the mutated line + foreign text gives `incomplete`/`judgment`, never `intended_failure` (`judge_detector` last branch; `test_place_alone_is_not_a_proof` re-run green). `inside` false gives `wrong_location`.
- **Residuals:** one pre-existing and named in the `fires_on` docstring, an author's message matching a `fires_as` row. E1.13: F8.

**Q2.** No check judges a role's word.
- `judge_record` checks presence, bytes, state, word and substring; quote relevance stays with the acceptor (E2.3). `receipt_off_target` compares two numbers. After the F2 fix the role check is data too.
- Census: `judge_record` xref/judgment/critic is right. `judge_detector` shape→xref is right (a raise of class; it joins a token). `not_proved_word`, `cannot_judge_facts`, `probe_judgment_cases` have names outside `UNIT_NAME_RE`. Re-run: `judgment_census: 21/21 ok`. The N5 line `judgment: none` is honest.

**Q3.**
- `probe gap` word on unjudged: **blocking, F1**.
- Controller: **fix now, F4**.
- Docs: **fix now, F7**.
- All three go to one fresh fix-round builder of this batch (owner: no leftovers, F6-30). It owns `window_record.py`, `acceptance.py`, `controller.py` (the two door functions), `s5.md`, `state-exits.md`.

**Q4.** Readers walked (grep `statement_after` over `scripts`, `references`, `handoffs`, `agents`, `skills`, without tests; positive control: the producers `:1349`, `:581`).
- Recovery texts `:2202`, `:2263` want the written bytes: right.
- `judgment_facts` `:1984` gives the critic the written statement plus `message_marker`: fine.
- **The person's lead is hurt: F5.**
- `t-1980` re-pinned the one byte comparison in tests (`statement_inverted`). `statement_inverted` has no package reader yet; F5 gives it one.

**Q5.** I found no code path whose purpose is keeping an old package's records alive. Wording that lies, or a default to drop:
- `probe_gap_block(..., proved_words=None)` "keeps every old caller": there is one production caller (`window_record.py:1219`), so make it required.
- `plan_detector_mutation` docstring "as every older caller": per t-1980 the default serves the tests' helper; I did not grep other callers.
- `window_record.py:571` and `proof_level.py:1381` "written before N4": the code is right (a receipt with no `target` reads as unknown, AR-23), change the reason.
- `story_run.py` `seam_chosen` comment "absent in an older `asked`": it is absent on any other question.
- Plus F6. All low, in the same round.

## Standing questions

1. **Fit:** N1, N2, N3, N5 as written except F1, F2, F5; N4 except F3.
2. **Builder's decisions:** `cannot_judge` quote optional, exits 0/1, `printed` joined by ` / `: safe.
3. **Seams:** additive.
4. **Class:** off-target readers F3; word readers F1/F4; AR-19 twins kept.
5. **Tests:** edges pinned except F1, F2 (stubbed), F3 and the mixed case.

6. **DUPLICATION AND CONSISTENCY.**
   - `window_record.py:799-803` `probe_judgment_cases` repeats the `owed` computation of `probe_gap_cases` (`:753-763`): extract `_word_owed`, fix now.
   - Cutting: local `cut` in `probe_judgment_lead` vs `_gap_why` vs `_printed`: queue.
   - `cannot_judge_facts`, `not_proved_word` belong in `proof_level` (the builder says so; `acceptance` imports them lazily from `window_record`, inside a loop): fix now, it is a move.
   - Clone ratchet: node witnesses say `0 new`. `forge-check` of 8042688 was running and is **not read**; the Lead reads it before acceptance.

7. **CODE QUALITY.**
   - `judge_record` `probe_by_code.py:4202-4274`, about 72 lines: split the refusals off (fix now, F2 adds to it).
   - `judge_detector` 1881-1968, about 88 lines: queue.
   - Lazy import in a loop: above. Dead branches: F6.
   - No function over three nesting levels in the new code I read.

8. **Hygiene:** `selftest --lang/--limits` in the witnesses.
9. **Ratchets:**
   - `ratchet_tokens.qa-code-critic` 18685→18669 and `process_ratchet_tokens` 17275→17199 (re-run: tokens 18669, process 17199): lowered.
   - `blocking_per_role.qa-code-critic` 130 unchanged (per the N2 witness).
   - D13 141→142: an inventory pin with a reason (t-1992), named here as a raise of that pin's count.
   - Nothing unnamed.
10. **Architecture:** AR-n named per commit; open against it: AR-22 F6, AR-25 S2, AR-13 F3, AR-9 F4.
11. **Judgment:** none moved into code. The new craft bullets are experience; the Tools lines are process and paid for by cuts.

## Spot-checks and trail

**Empirics:** `ctl.py` in the session scratchpad (temp dirs, real functions; output quoted above) and the real records of `tr-arm-b`. The stand's source line cited in S1 (`cart.spec.ts:113`) was read.

**Read:**
- the spec whole; 8 reports; the N5 diff; the delivery part of the N2 diff; the probe part of t-1999
- `probe_by_code.py` marker, judge, receipt, publish parts
- `proof_level.py:1030-1125,1192-1290,1377-1500`
- `window_record.py:552-590,690-815,1785-1835`
- `acceptance.py:874-925,955-1000,1040-1110`
- `controller.py:6380-6395,6552-6580,6625-6640`
- `case_stamp.py:462-497`
- `coverage_contract.py:216-228,260-280,585-600`
- `contract.py:5068-5095`
- commits 6e772d5a7, d942a2d2a, 78a89f626, 671e88e20 by their reports and the head code, not diff by diff

**Not traced:**
- that the report really lists an accepted `probe not proved` test (E5.8 depends on the manifest row being `unverified`)
- the `--at` re-probe end to end (read: `already_probed` does not block it)
- the slow files (CI)
- pipeline 8042688

**Needed beyond the manifest:** `execution_request.py`, `case_stamp.py`, `controller.py`, `coverage_contract.py`, `waiver.py`, stand records and Playwright source.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 window_record.py:696 / acceptance.py:908: a probe gap case word names an unjudged cause judgment record by equality, the window closes with no critic judgment",
    "F2 probe_by_code.py:4254: judge_record accepts any open dispatch; run shows a qa-automator dispatch of another scope passes the check it calls",
    "F3 probe_by_code.py:4099 / case_stamp.py:486: an off-target probe publishes sensitivity proven and the case stamp falls through to it (traced by reading)"
  ],
  "fixes": [
    "F1 read probe_owes_judgment first in both twins; unjudged is never named",
    "F2 require role qa-code-critic, stage S5, case in scope; an unstubbed test",
    "F3 _binding_items sets no proven for an off-target receipt",
    "F4 controller.py:6386,6569 door by the record state, keys line for not proved",
    "F5 lead shows statement_inverted, not the marked statement",
    "F6 remove factory: readers controller.py:6637, window_record.py:1681; widen the scan",
    "F7 s5.md and state-exits.md name probe not proved",
    "F8 measure E1.13 on the stand's Playwright 1.56; M-TS rows stay owed to the live proof",
    "Item 6: one owed helper; move cannot_judge_facts and not_proved_word to proof_level; item 7: split judge_record; Q5 wording and proved_words required"
  ],
  "class_completeness": "Word readers over a probe record: instance, case, tooling, class, older word walked (F1 open, rest closed). Off-target receipt readers: window, reached, keep_standing covered; binding publication and case stamp not (F3). Refusal doors: seam covered, controller two sites not (F4). Removed factory producer: two dead readers (F6). Spec-level remainders S1-S3 go to the Lead. Docs/SIBLING_MAP.md itself was not opened; siblings were walked by the artifact and by grep of the readers.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-1968-mutation-probe-marker-and-critic.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/tasks/specs/reports/t-1977, t-1978, t-1980, t-1981, t-1982, t-1992, t-1994, t-1999",
      "git show 3957597e5, a4dd1a6c4 (delivery part), 8f37605fb (probe part), census rows of e26c87ce2",
      "scripts/probe_by_code.py, proof_level.py, window_record.py, acceptance.py, controller.py, case_stamp.py, coverage_contract.py, contract.py, execution_request.py (ranges in the report)",
      "mybooks-stand/tr-arm-b work/probes records, tests/api/cart/cart.spec.ts, node_modules/playwright/lib/matchers"
    ],
    "reruns": [
      {"command": "pytest test_probe_marker_judgment.py -k 'place_alone or unknown_text or second_judgment or unjudged_is_not'", "result": "4 passed, 21 deselected in 7.98s"},
      {"command": "python -B tests/test_judgment_census.py", "result": "judgment_census: 21/21 ok"},
      {"command": "python -B role_load.py --role qa-code-critic --json", "result": "total_bytes 74673, tokens 18669, craft 1470, process 17199, within; rows 18669 / 17199"},
      {"command": "scratchpad ctl.py over real functions", "result": "unjudged named by case word; cannot_judge control None; mixed case lists neither; off-target word None; find_active_dispatch returns qa-automator"},
      {"command": "real records tr-arm-b, mutation_detail.line vs assertion_id", "result": "records 44 on-target 14 off-target 30"}
    ]
  }
}
```
