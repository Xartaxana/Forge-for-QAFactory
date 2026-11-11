# t-2010 — critic on the analyst batch so far (spec t-1991, nodes U1, U2, U3a)

Critic (Opus), 06.11.2026. Tree read and probed: `D:/ws1/wt-fb5` at `971c40661` (merge of U1 `cf382be51`, U2 `9550d027d`, U3a `deb1b702d`, plus `cf8f83ee8` t-2003), clean. Below `PKG` = `ai-packages/qa-factory`; `PA` = `PKG/scripts/place_answers.py`. U0, U3b, U4 and U2b are not built and are judged as owed. Line numbers are of that tree. The acceptance decision belongs to the Lead.

**Verdict: NEEDS WORK (`fit_with_fixes`). 5 blocking findings (F1-F5), 7 to fix before merge (F6-F12), 3 SPEC items that go with owed nodes (F13-F15), 2 to queue (F16-F17).**

The core holds: one join, one record per place, code checks keys and joins, the walk receipt goes down on every forged input I tried. What fails is the register side around a `bug` answer and around a place with several sources: the person can lose a question or be asked one the analyst has already answered, and a suspicion can reach no register line. No redesign is needed; the fixes are in two functions and one packet line.

How probed: real functions on harness temp stories (the fixtures of `test_place_answers.py` / `test_walk_receipt.py`), output quoted. The handoff gate refused a scratch script, so the probes ran inline through `python -B -c`; they wrote only to temp stories. Slow files were not run. Each witness in a finding is verbatim, cut only at the ends.

---

## Blocking

**F1 (Q1, high; SPEC + code). A `--replace` to `bug` withdraws the chain before the carrier stands, and the suspicion reaches no register line.** `PA:646`; spec §3.2 table, row `bug`. Probe (register place; requirement_silent, then `--replace` bug, the draft has no walk receipt):
```
{'record': ..., 'line': None, 'withdrawn': 'EX-2', 'refusal': '', 'installed': True}
('carrier missing', 'no draft carries this walk receipt')
close [...] ['req-R-1: its chain was withdrawn; the gap cannot be written']
active []
```
On an `open` place the same withdraw makes `unresolved_targets` (ii) resolve the target (`investigation.py:394-395`), so neither the investigation nor `close_unsettled` writes anything. What is left: one stdout line and the scribe's `(carrier missing)`; the report and gate B show nothing (AR-27, AR-28). **This is the road §3.4 prescribes after a person's gate-B `bug`** (question line -> S7 rework -> `--replace` to `bug`), so the person's own word is what triggers it whenever the draft's receipt does not hold (no `reproduction` written, no APP_BUG row, F-J).
Fix direction: (a) in `write`, after the record lands, withdraw only if `settled_answer(...)` says `settled`; otherwise leave the active line, and `close_unsettled` already corrects an active line into the `carrier missing` gap; (b) `close_unsettled` also walks settled `bug` places and withdraws an active line (`by_close`), which covers a draft repaired after the write; (c) for a chain that is already withdrawn and now unsettled, write the gap under a separate target (for example `place-gap-<id>`), never `printed` only. Tests: replace-to-bug with a void receipt leaves a gap line; replace-to-bug with a lifting receipt withdraws; a withdrawn chain whose capture later changes still gets a line.

**F2 (high). A stale "not settled" gap survives a first `bug` answer.** `PA:646` (`and old`; builder deviation 7). Scenario: first close gaps the place, the scribe rejects, the rework's FIRST answer is `bug` with a lifting walk. Probe:
```
('settled', '') ('reproduced_by_factory', ['walk'])
close2 []
active [('coverage_gap', 'none', False, 'code:place_answers.close_unsettled', "not settled by the analyst - the analyst's dispatch ended wi")]
```
The report says "the run left this suspicion unchecked" beside "the analyst walked it". This breaks §3.4 re-entry and the E3.4 invariant ("a stale gap is corrected by a later answer"); `test_stale_gap_corrected_by_later_answer` covers only `requirement_silent`. Fix: F1 (a)+(b), dropping `and old`. Test: gap, then first `bug`, no active line.

**F3 (high; SPEC). The investigation's `project` puts a person's question on a place the analyst settled `bug`.** `investigation.py:319` walks all targets; a first `bug` writes no line, so `no chain -> add`, and the gate runs `project` on every entry (`s7_investigation_gate`). Probe on `case-TC-006`:
```
('settled', '')
active [('unresolved_question', 'owner_question', True, 'code:investigation.project', '')]
```
`close_gaps` skips it as resolved, so gate B asks the person a question about a bug the analyst already walked (FR-10; the class of critic D6). The spec's `investigation.py` owns line (`unresolved_targets` only) leaves no one able to fix it. Fix: `project` skips a target whose `settled_answer` is `settled`, through the same reader; extend U1's owns by that one clause; add a twin key in `test_investigation.py` (CI) and a fast test in `test_place_answers.py`.

**F4 (high; SPEC, a miss of U2's owns; flagged by the builder as an unread analog).** A lifted code-reading draft still tells the person "by reading the code, not proven by a run". `gate_brief.py:4148` sets `code_reading=True` from `is_code_reading` alone and `:4337` takes that branch INSTEAD of `reproduction_words`, so the `elif` is never reached. Traced by reading, not run. This is the owner's main case (arm B's 7 code-reading drafts) and live-proof key (3), while `reproduction_words` says "reproduced by the factory — the analyst walked it" on the other surfaces (FR-10). Fix: at `:4336`, `if row.get("code_reading") and row.get("confirmation") != "reproduced_by_factory"`; keep the oracle and code lines. Test in the gate-brief test file that pins t-1676's text.

**F5 (high; SPEC on the rule, code on the reading). `close_unsettled` destroys a person's question.** Three routes through one site, `PA:544-566`:
- (a) A place with sources `open` + `draft` in state `open` is gapped because the filter tests `== {"open"}`. The first close `add`s a gap; `project` then skips the chain (not all code), so a type-(b) target's question NEVER reaches gate B. All seven `case-` targets of the fixture carry such a question. The §3.4 wording ("source `draft` … and, for an `open` place, ONLY …") does not say which rule wins for a place with both; the builder's reading was not flagged.
- (b) With a `project` line already there (re-entry), the probe shows `[('unresolved_question','owner_question',True,'code:investigation.project','')]` -> close -> `[('coverage_gap','none',False,'code:place_answers.close_unsettled',...)]`. By the same line, an investigator's probe-backed outcome is corrected to `probe: None` once a draft joins after a rework (traced: (i) resolves the target, the source becomes `{"draft"}`).
- (c) A `requirement_silent` answer in `conflict` loses its question the same way, and the state then flips; E1.13 "twice with the same why -> no second line" fails:
```
('conflict', 'the draft d1.json of this place still stands unconfirmed')
c1 [...] [('coverage_gap', ..., "the analyst's answer and its own records disagree: the draft")]
('carrier missing', 'no active register line of this place was recorded by the answering dispatch; ...')
c2 ['EX-4'] [('coverage_gap', ..., "the analyst's answer did not reach its record: no active reg")]
```
`s7_close` runs the close on every entry (a `wait` on a running pass, a scribe reject, a seam rework), so a second close is ordinary, and the false text is what the person reads. `close_gaps` already shows the right form: it carries `question`, `owner_role`, `oracle_status` (`investigation.py`, its `line = {key: active[key] for key in ...}`).
Fix: (1) `"open" in sources` and state `open`/`invalid` -> skip (the investigation road keeps it); (2) state `open`/`invalid` over an active line that is neither ours nor all-code -> print, do not correct; (3) a `correct` keeps `question`, `owner_role`, `oracle_status`; (4) in `settled_answer`, check `conflict` before the line check (`PA:494` before the kind test). Tests: a question survives each of the three routes; two closes on a conflict write one line.

## Fix before merge

**F6 (Q2, medium). A draft with no `confirmation` is not a place.** Probe: `('confirmed_by_person', [], [])`, and the place list omits it. An unknown reads as the top step and the suspicion drops silently (AR-28, FR-41). See Q2 for the fix and the size of the risk.

**F7 (medium; SPEC text). The door lies.** `PA:632` names `impossible`, and `PA:630` refuses `impossible` on a withdrawn chain. Probe: `REFUSED this place's line was withdrawn ... Door: answer `bug` or `impossible`, or record the question under a new place`, on an `impossible` answer (FR-2, FR-57). Fix: drop `impossible` from the door here and in §3.2. The test only asserts `new-<slug>`.

**F8 (medium; AR-28).** A corrupt record of a `new-` place vanishes and the list says none: `PA:96` `continue`. Probe: `{'places': [], 'unreadable': []} ['Places to settle: none in this run']`. Fix: add it to `unreadable` (`places` holds the list).

**F9 (medium; AR-28, traced, not run).** A walk lifts a `result` draft when the run report cannot be read: `bug_records.py:817` returns `()` for `{}`, `_walk_has_no_run` is False, `walk_wide` is empty. It is the old rule for `own_script`, but §3.3's "a `result`-kind draft keeps it" then means nothing. Fix: for a walk entry on a non-code-reading draft with no readable report, the existing `R_NO_REPORT`. Test beside `test_result_draft_keeps_current_red_fact`.

**F10 (medium; AR-10, closes U1 question 1).** The brief names only `answer` and `expectation.source` (`story_run.py:12985-12992`); `seen`, `question`, `why`, `draft` and the draft's `{kind: walk, evidence, observed}` are only in `write --help` or a refusal. U1 moved them off the key page because of the role-load ratchet, "to be in the brief", and U3a did not take them. Driver lines are not static load, so one line closes it with no ratchet raise, and the row stays off the page. `test_brief_names_places_and_answer_keys` asserts the words of the two lists only. In the same line: `manual_capture.py ... --case` omits the required `--task-root` (`manual_capture.py:4704`), and `ui` needs `--steps-file` (AR-8).

**F11 (low-medium; AR-28, AR-14).** A made-up `--dispatch` is accepted and settles. Probe: `EX-1 ('settled', '')` for `no-such-dispatch`. `s7_part_of(None)` is `""`, so rule 8's "data, not discipline" is passed by any wrong id, and `recorded_by` holds a word nobody can join. Fix: when the controller state reads and has dispatches, an unknown id is refused with a door; an unreadable state still does not lock (deviation 6 is right).

**F12 (low; Q5, code quality).** `scribe_line_max` gets a data row and the `.get(..., 1500)` goes (FR-13). Dead: `capture_optional`, `new_slug_pattern` in the data file; `STATES` (`PA:38`). `s7_gap_reason` indexes `texts[3]`, `texts[4]` (`story_run.py:13004`): a reorder silently gives a false text; use named keys. `write` computes `places` twice (`PA:621`, `:633`).

## SPEC, with the owed nodes

**F13 (two drafts of one place; goes with U2b/F-L).** One record per place names one draft, so a second observation on the same case can never lift:
```
d.json req-R-1 ('reproduced_by_factory', ['walk'], [])
e.json req-R-1 ('unconfirmed', [], ['the walk was of another place'])
('settled', '')   unsettled ['req-R-2']
```
The place reads settled with no gap while a joined draft stands unconfirmed and has no road. The draft stays visible as unconfirmed, so nothing is lost silently, but the owner's "all unconfirmed" is not met. Direction: `draft` may be a list, and U2's check becomes `name in drafts`; `settled` requires every joined draft lifted or named, otherwise `conflict`.

**F14 (F-J as written is unreachable).** §3.2 says the `bug` answer "is still written … `carrier missing`". Rule 7 / E1.8 refuse it: `REFUSED no draft ... record False`. An unpinned `obs-` target can never own a draft (`target.case` is None, `place_of_draft` rule 2 never matches): `REFUSED the draft o.json belongs to place req-R-4, not obs-S6-qa-runner-4-0`. The suspicion then ends as "not investigated", which is not silent but is the wrong words. Whatever the Lead answers on F-J must also state the join for `obs-`; option (a) alone does not give one.

**F15 (`person`: the file path reaches nobody; U3b).** `expectation.id` must be `state/words/driver-answer-<ms>.txt`. The brief carries the words, not the path: `state/words` is absent from `brief_pack.py` and `story_step.py` (the same grep finds it in `person_words.py`, `story_run.py`, `controller.py`), and the hits in `story_run.py` are docstrings. The controller stores the text and the mark, not the path. FR-15/AR-8: name it in U3b's lines, or accept the quote against the dispatch's `reason` with no file.

## Queue

**F16 (DUPLICATION, low).** `_draft_json`, `_read_record`, `_records` and `_walk_receipt_problem` parse JSON by hand (three encodings policies) beside `C.load_json` / `hooklib.read_json` (axis 16); `_s` and `_squash` repeat `investigation._s` and `manual_evidence._squash`. **F17 (CODE QUALITY, low).** `places` is about 73 lines (`PA:188-261`); `first[1].startswith("no draft file")` (`bug_records.py:922`) is control flow on a text.

---

## Answers

1. **Q1: real, F1.** Scope is wider than the report said: it also covers `req-`/`draft-` places, and it fires on the person's own `bug` road. Fix as in F1; not "U2/U3a decide": it is U1's `write` and `close_unsettled`.
2. **Q2: acceptable only as a low-probability risk, not by the "no compatibility" word.** That word removes the reason for the legacy default, it does not bless it. The form says "always `unconfirmed`", and the one real draft on the stand has the field (`real drafts 1 no confirmation field 0`: thin evidence). Fix now, in `places` (`PA:246`): an absent field is a place. `settled_answer` then needs the door "write `confirmation: unconfirmed`", since `confirmation_of` returns the person's word with no receipt check. The root, `contract.bug_confirmation`'s default for a draft, is a decision for the Lead: queue it with the owner's word as the reason.
3. **Q3: safe, both.** `_names_of_draft`: the error goes down (no file equal -> `R_WALK_PLACE`), identical twins are each tried; the callers I read (`bug_records.py:305`, `confirmation_of` through `_draft_of`) pass raw JSON, the others (`gate_brief.py:4118`, `delivery_summary.py:105`, `factory_dashboard.py:1282`) were not traced to their loader, and a loader that alters the dict would read `unconfirmed`, the safe side. A filed bug that copies `reproduction` onto itself would void the walk (down; not seen in the forms I read). It can be simpler: read `record.draft` and compare once (F17). Order: only the closed word differs; both void; `answer_problems` still runs. The builder resolved a real conflict between §3.3 and E2.3 correctly; the spec text should follow.
4. **Q4: keep the line, the pins gain it, same commit (host adaptation 9).** AR-23 and the spec state it, it costs about 10 tokens, and it tells the analyst the list ran. Two additions. The scribe's "Places of S7: none in this run" joins `stage_S8`'s `extra` too, so `test_stage_acceptance_consumer.py` / `test_s8_reporting_regressions.py` may pin it. And `told` reads `extra`, so U3b moving the line into `run_role` reverts those pins: U3b's owns must list `test_story_run_s7.py` (SPEC). The sibling convention ("no line about code rows" when empty, K5 (d)) goes the other way; the spec's explicit word wins.
5. **Q5:** the data row, F12. Private names across modules are the package's habit, and the spec names `_quote_in`, `_jsonl`, `_oracle_problems`. Renaming `_list_lines` -> `list_lines` is cheap, optional, not a finding.
6. **Q6: no judgment moved into code.** Every check in `_answer_lines` is membership, a join or quoted bytes; `conflict` is a presence join; `close_unsettled` closes nothing, it records. Census: `answer_problems` xref, `_refuse` shape, `qa-failure-analyst` 131 -> 132 named, per the report's witness and commit message. Note for the Lead, no action: the helpers `_capture_list` etc. and `_cli` are named outside `UNIT_NAME_RE` (the builder says so of `_cli`); they are reached only through the one row, so nothing is hidden today. Limit: a purely visual oddity has no quote, so its only legal answer is `impossible` (spec rule 2).
7. **Q7: errors mostly go down; five places where an unknown passes or vanishes:** F1 (withdrawn, no line), F6 (no field, not a place), F8 (corrupt record, "none"), F9 (report unreadable, lifted), F11 (unknown dispatch, settled). F13 is settled over an unconfirmed sibling. Held: unreadable register / questions / controller refuse with doors (traced `unconfirmed_requirements`, `_oracle_problems`), (iv) raising resolves nothing, an invalid record resolves nothing, a hand-written record cannot lift (tests re-run).

## Standing questions

- **Fit to the spec:** as above; otherwise implemented as written. U1 deviation 2 is closed at this head (`test_role_commands.py:51`, `:354`, t-2003).
- **Builder's own decisions:** deviation 7 wrong (F2); the two-source reading wrong (F5a); the rest safe. Report notes 4, 6, 8, 9 were honest and useful.
- **Seams:** additive; `reproduction_problems` for non-walk entries reads equal to before, and the report's `test_bug_reproduction.py` 229/229 is consistent with that (not re-run).
- **Tests:** the named mutations are killed by reading. Missing: first `bug` over a gap, `project` after `bug`, second close on a conflict, a question through `close_unsettled`, walk with no report.
- **DUPLICATION AND CONSISTENCY:** F16, plus `close_gaps`' field list not followed (F5). No second implementation of the join, the reader of the step or the receipt, by reading the diff (t-1987 N1 grep for a prior join not re-run); the new code reuses `code_says_contradicts`, `draft_listing`, `confirmation_of`, `_quote_in`, `case_root`.
- **CODE QUALITY:** F12, F17. No copy-pasted blocks found in the diff beyond those.
- **Ratchets:** one raise, named: `blocking_per_role.qa-failure-analyst` 131 -> 132 (`place_answers.py::_refuse`). Role load 17,753 at the ratchet, not raised, per the witness.
- **ARCHITECTURE:** AR-13/14/21-23/25-29 named; AR-27, AR-28 broken by F1, F5, F8. U3a's commit omits AR-19 (the spec lists it "with U4"): owed.
- **Hygiene:** FR-30 per witnesses. Not independently run.

## Class completeness (SIBLING_MAP)

Axis 5 stage twins: `s7.md` owed by U4, `close-unsettled` has no card and only U4 tells the conductor. Axis 16 JSON reader: F16, queue. Axis 18: raise named, covered. Axis 29: every line through `append`, covered. Axis 31: the investigation line added, charter owed by U4. Axis 32: no new judgment; F-D's sibling stays queued from t-1987. Surface walked for F1/F2/F5: every op of `close_unsettled` and `write` against each active-line owner (none, own, close, project, probe, person), and each source mix. Consumers of `is_code_reading` outside `bug_records` (F4): `gate_brief.py`, `gate_preflight.py`, `place_answers.py` only (grep; the same call found the known `gate_brief` site). Whether the report and summary print the walk phrase was not traced; a sweep of those surfaces is a scout question if the Lead wants it.

## Spot-checks

- **Real data (rule 13):** `captures.jsonl` of TP1-12586: `rows 161 ok 161`, keys `captured_at, command, content_hash, kind, path, phase, proves`, `path` task-relative, `content_hash` = `sha256_file`. The test fixture's row shape holds.
- **Negative "no guard refuses `manual_capture` by name" (spec F16):** 0 hits in `guard_pre_tool.py` and `stage_guard.py`; same tool on `run_suite`: 13 hits, and `manual_capture|run_suite` 21 in `stage_guard.py`. Case-sensitive grep; the guard's generic paths were not read. Whether `ui|http` itself refuses a `settle-` case with no `request.json` is NOT established: a live-proof item.
- **Witness consistency:** 63 = 17 + 46 (U2), 56 = 10 + 46 (U3a). Re-run: `test_walk_receipt.py`, `17 passed in 24.49s`.

## Trail

Read: spec t-1991 whole; t-1987; the brief; the three reports; diffs of the three commits; `PA` whole; `references/place-answers.json`; `investigation.py` :125-220, :245-340, :385-430, :470-575; `exploratory_findings.py` :185-200, :277-395; `contract.py` `bug_confirmation`, `unconfirmed_requirements`; `bug_records.py` :189-218, :590-640, :761-922, :961-1022; `controller.py` `s7_part_of`, `state`; `manual_capture.py` `case_dir_name`, parser; `manual_evidence._quote_in`; `gate_brief.py` :4108-4158, :4325-4345; `gate_preflight.py` :5083-5095, :5158-5175; `story_run.py` `s7_investigation_gate`; `test_story_run_s7.py` :74-80, :118-215; helpers of `test_place_answers.py`, `test_walk_receipt.py`, `test_place_driver.py`; `SIBLING_MAP.md` axis headers.

Needed beyond the manifest: `gate_brief.py`, `gate_preflight.py`, `exploratory_findings.py`, and a real story's captures (TP1-12586, read-only).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F1 place_answers.py:646: a replace to bug withdraws the chain before its carrier stands; a void receipt leaves no register line, close_unsettled cannot write, investigation (ii) resolves the target; fires on the person's gate-B bug road",
    "F2 place_answers.py:646 (and old): a first bug answer leaves the stale not-settled gap active beside a lifted draft",
    "F3 investigation.py:319: project adds an owner_question line on a target settled bug, so gate B asks about it",
    "F4 gate_brief.py:4337: a code-reading draft lifted by a walk still reads 'by reading the code, not proven by a run' at gate B",
    "F5 place_answers.py:544-566: close_unsettled loses a person's question three ways (open+draft gapped so project skips it; correct over a project or probe line; conflict) and the conflict state flips on the second close"
  ],
  "fixes": [
    "F1/F2: withdraw only when settled_answer says settled, dropping 'and old'; close_unsettled withdraws the active line of a settled bug place; a gap on a withdrawn chain goes under a separate target",
    "F3: investigation.project skips a settled target through settled_answer; extend U1's owns",
    "F4: gate_brief code-reading words only while the confirmation is not reproduced_by_factory",
    "F5: open in sources with state open or invalid is skipped; no correct over a foreign line in those states; a correct keeps question, owner_role, oracle_status like close_gaps; conflict checked before the line check",
    "F6: a draft with no confirmation field is a place, with a door; the contract default is queued for the Lead",
    "F7: drop impossible from the withdrawn-chain door, here and in spec section 3.2",
    "F8: a corrupt record goes to unreadable, never none",
    "F9: a walk with an unreadable report on a non-code-reading draft reads R_NO_REPORT",
    "F10: one brief line with the answer keys and the walk entry form; add --task-root and --steps-file to the capture command",
    "F11: an unknown dispatch id is refused when the controller state reads",
    "F12: scribe_line_max as a data row; remove dead capture_optional, new_slug_pattern, STATES; named gap reasons; one places call in write",
    "SPEC F13: draft may be a list; settled requires every joined draft lifted or named",
    "SPEC F14: the F-J answer states the join of an unpinned obs target and repairs section 3.2 against rule 7",
    "SPEC F15: U3b names the person's words file, or the quote is checked against the dispatch reason",
    "SPEC Q4: test_story_run_s7.py pins gain the line in the same commit; U3b's owns list that file"
  ],
  "class_completeness": "axis 5 twin owed by U4; axis 16 hand JSON parsing queued (F16); axis 18 raise 131 -> 132 named, covered; axis 29 covered; axis 31 investigation line added, charter owed by U4; axis 32 no new judgment. Neighbors of the F1 surface walked: each op of write and close_unsettled against each active-line owner and each source mix. Code-reading words on other surfaces beyond gate_brief need a scout if wanted.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-1991-analyst-settles-places.md (whole); reviews/t-1987; docs/tasks/critic-diff-brief.md; reports t-1995, t-2004, t-2005",
      "wt-fb5 PKG/scripts/place_answers.py (whole); references/place-answers.json; diffs of cf382be51, 9550d027d, deb1b702d",
      "wt-fb5 PKG/scripts/investigation.py :125-220, :245-340, :385-430, :470-575; exploratory_findings.py :185-200, :277-395",
      "wt-fb5 PKG/scripts/bug_records.py :189-218, :590-640, :761-922, :961-1022; contract.py bug_confirmation, unconfirmed_requirements",
      "wt-fb5 PKG/scripts/gate_brief.py :4108-4158, :4325-4345; gate_preflight.py :5083-5095, :5158-5175; story_run.py s7_investigation_gate",
      "wt-fb5 PKG/scripts/tests test_story_run_s7.py :74-80, :118-215; helpers of test_place_answers.py, test_walk_receipt.py, test_place_driver.py",
      "docs/SIBLING_MAP.md axis headers; tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B -m pytest -p no:cacheprovider PKG/scripts/tests/test_walk_receipt.py -q", "result": "17 passed in 24.49s"},
      {"command": "inline probes on temp stories (fixtures of test_place_answers.py, test_walk_receipt.py): withdraw, door, stale gap, conflict twice, two drafts, project after bug, close over a project line, made-up dispatch, corrupt record, obs bug, no confirmation field", "result": "each reproduced as quoted in F1, F2, F3, F5, F6, F7, F8, F11, F13, F14"},
      {"command": "real captures.jsonl of TP1-12586, path and sha256 against content_hash", "result": "rows 161 ok 161"},
      {"command": "grep manual_capture in guard_pre_tool.py and stage_guard.py; control run_suite and the alternation", "result": "0 hits; control 13 and 21"}
    ]
  }
}
```
