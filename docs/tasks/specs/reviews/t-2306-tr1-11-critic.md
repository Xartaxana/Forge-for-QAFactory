# t-2306: critic diff gate on TR1-11 (thinking-roles/1/TR1-11, builder t-2295)

Reviewed: `git -C D:/ws1/wt-tr1-11 diff 990ce334d..4d17a11c2` (one commit, branch tr/tr1-11). Checked against: node row TR1-11
(`plans/piles/thinking-roles/batch-1-ruchnoj-prohod.md:32`), section TR1-11 of `findings/20261106-analitik-prohodit-mesta-ostatki.md`,
review t-2010 F6/F13/F14/F16/F17, the builder's report t-2295.

**Verdict: fit with notes (`fit_with_fixes`). 2 blockers (B1, B2) for this node's fix round, 1 open-point answer that needs a queue
line or a fix (P1), 5 notes (N1-N5).** The refactor parts (F16, F17, the `places` split) are correct. The F13 lift has the right error
direction. The F13 "settled" half and the F14 join key are not done yet.

## Lead's points, by name

**1. The open point: `contract.bug_confirmation` for an absent word. Answer: YES, there are readers that take a DRAFT through it and
read a draft with no word as `confirmed_by_person`. The point is not closed.** Every one of them goes through `bug_records.confirmation_of`
(`bug_records.py:1134` calls `C.bug_confirmation(data)` and returns `_PERSON` before any receipt check). I probed it on a `TP.story()` with
one draft `n.json` that has no `confirmation` key (scratchpad probe1.py):
```
confirmation_of: ('confirmed_by_person', [], [])
PA._confirmation: ('unconfirmed', [], [])
story_bugs: [('n', 'confirmed_by_person', 'confirmed')]
gate_brief.bug_rows: [('Total has one decimal', 'confirmed_by_person')]
DS._bug_confirmation(draft): ('confirmed_by_person', [], [])
```
The draft readers:
- `gate_brief.bug_rows` (`gate_brief.py:4129`), the gate B packet. At `gate_brief.py:4545` the words "nobody has reproduced it"
  (`reproduction_words`) are printed only for `unconfirmed` / `reproduced_by_factory`. So at gate B the person sees a word-less draft
  as an ordinary bug, with no line saying nobody reproduced it.
- `bug_records.story_bugs`, the draft branch (`bug_records.py:1605`), gives `state: "confirmed"`. traceability, the report and the
  dashboard read these records.
- `bug_records.write_texts` (`bug_records.py:362`) writes the readable bug text with that word.
- `delivery_summary` draft rows (`delivery_summary.py:330` -> `_bug_confirmation` -> fallback `BR.confirmation_of(task, data)` at
  line 105, because a `.json` ref is not a `.md`).
- `factory_dashboard.story_bug_rows` drafts (`factory_dashboard.py:1315` -> `_bug_step`).

None of these SKIPS the place: the place side is held by `place_answers._confirmation` and the two guards in
`settled_answer` / `_settled_through`. None files a bug by itself either: filing needs the person's choice at gate B. But the packet that
choice is made on drops the "unconfirmed" line, and the delivery and the report count the draft as confirmed by a person. That is the
AR-28 / FR-41 leak the Lead's decision in the section was written against ("отсутствие поля — неизвестное ... не становится пропуском").
So option 1 meets the node row's own words ("черновик без `confirmation` — место") but not the section's decision.
**Recommended fix:** option 2, with the keyword on `confirmation_of` (THE reader, AR-13). Do not put it only on `bug_confirmation`.
The dispatch suggested `absent="unconfirmed"` on `bug_confirmation`; that alone reaches only the dashboard's no-root branch and
traceability, and those read filed bugs. Two shapes would work. (a) `confirmation_of(task, data, ..., draft=True)` reads an absent word
as `unconfirmed`, and the five draft callers above plus `place_answers` pass it. (b) A `bug_records.draft_step(...)` wrapper that they
call. Either way the three hand-copies of "a draft with no word" in `place_answers` (`_confirmation` :212, `_settled_through` :588,
`settled_answer` :626) collapse into that one call. Filed bugs keep the legacy default, so the three pinned tests named in the report
stay. The callers are in `gate_brief.py`, `delivery_summary.py` and `factory_dashboard.py`, which are outside this node's `owns`.
So: widen `owns` for the fix round, or open a node. **Suggested amendment of the finding text:** "the contract default for FILED bugs
stays (a bug filed before 0.7.16); a DRAFT with no word is `unconfirmed` for every reader of a draft's step — the place list (done,
TR1-11), the gate B packet, story_bugs/report, delivery and dashboard (node <id>)".

**2. F14: is `case` == `obs-<dispatch>-<index>` the field drafts really carry? No. It is a guess.** Drafts are written by the analyst
(`references/artifact-writers.json:237`, writer "qa-failure-analyst (the role)"). The draft contract (`references/artifact-contract-run.md`
around line 102) defines `case` as a case id (`"case": "TC-004"`), and `cases` as the cases the draft covers. Neither the contract nor the
analyst charter, nor `references/place-answers.json` (only `place_id_note`), nor the `_bug_list` refusal (`place_answers.py:471`, "answer
that place with this draft, or name the draft of this place") tells the role to write a place id into `case`. The id is produced only by
`investigation.py:170`. So no writer produces the join today. It is reachable only by an instruction that does not exist yet (AR-10/FR-38:
the requirement reaches the role before the work), and it overloads `case`. A draft with `case: obs-…` loses its real case:
`C.case_ids('obs-S6-qa-runner-4-0')` -> `[]` (probe), so `draft_cases` is empty, `factory_dashboard.py:1311` drops the draft from the
story's bug rows, and the traceability case join gets nothing. See B2.

**3. F13: error direction of the multi-draft lift. It goes down.** Traced `_walk_receipt_problem` (`bug_records.py:912-939`) and probed:
- A draft of another place, citing the record: `place f: req-R-2`, `('unconfirmed', [], ['the walk was of another place'])`
  (probe3, with a valid APP_BUG triage row for TC-2, so the place check is what voids it).
- A record naming an unlisted draft: `('unconfirmed', [], ['the walk was of another place'])` (probe2 c).
- A record naming a draft of another place: `R_WALK_PLACE` (builder's test, re-read).

"A draft the walk never saw" can be lifted only if that draft itself carries a `walk` entry citing this place's record. That entry is the
role's own claim about this draft, written into this draft, so the lift is the role's word plus the place record. It is not a key
join closing the role's obligation (AR-29 holds). `record.place` must equal the place of THIS draft as `place_of_draft` computes it, and
`_draft_is_of_place` returns False on any exception (down).

**4. F17: `index == 0` versus `first[1].startswith("no draft file")`. Same semantics on every input.** The sentinel is the only text that
starts with "no draft file". `_walk_receipt_problem`'s details start with "the walk record …" or with "the walk answer does not stand:"
(answer problems are prefixed), and the place_answers text "`draft` … is no draft file" is never returned unprefixed (grep, 2 hits). So the
old condition was true exactly on the first iteration. Empty list: the loop never runs and the sentinel stands in both versions.

**5. F16: did a refusal text or an error class change for a caller?** No error CODE or class changed. The texts changed in two ways:
(a) `bug_records`: a walk record that parses to a non-object used to say "the walk record is not an object written by place_answers.py".
Now it says "the walk record is not readable JSON (an object was expected)" (probe2 d). Same code `R_WALK_RECORD`. `confirmation_of`
returns codes only, so only the detail-level readers of `reproduction_problems` see it.
(b) `place_answers` readers now accept a BOM (`utf-8-sig`). A record or draft with a BOM used to be "cannot be read (JSONDecodeError)"
and is now read. This matches `hooklib.read_json`, the safe direction.
The `(ExcName)` texts of `_read_record` / `_records` and "not a JSON object" are unchanged (`why.split(':')[0]` is the type name).

**6. Analogs: defects for this round, or queue lines.**
- `settled_answer` reads one draft per `bug` answer. This is a **defect for this round (B1)**, not a queue line. It is the second half of
  F13, it is in an owned file, and probe2 (a) reproduces F13's original state on the new code.
- `_names_of_draft` content equality: **no defect.** Two byte-identical drafts have the same content and so the same step. Each is tried,
  and a failure goes down (t-2010 Q3). No line needed.

## Blockers

**B1 (fix round, `place_answers.py:619-632`). A `bug` answer settles its place while a sibling draft of the same place stands
unconfirmed.** Scenario: `W.world("manual")` plus `TP.draft(task, "e.json", title="Another defect of R-1")` (same place, no walk entry):
```
a) e step: ('unconfirmed', [], []) | place of e: req-R-1
a) settled_answer req-R-1: ('settled', '')
```
The place drops out of the unsettled list, so e.json has no road. That is the exact F13 state t-2010 reported
(`('settled', '')` beside `e.json ... unconfirmed`). The node's key "два черновика одного места поднимаются одним ответом" holds only when
the role also happens to write the walk entry into every sibling. Fix: in the `bug` branch, after the named draft lifts, run the same
loop as the `not_a_bug` branch (:633-639). A sibling of the place with `_confirmation == "unconfirmed"` gives `carrier missing` naming
that draft and the door ("add the `walk` entry citing evidence/place-answer-<id>.json to it, or answer its own place"). The data text
goes into `place-answers.json` `line_texts`. Test: two drafts, entry in one only -> not `settled`; entry in both -> `settled`.

**B2 (Lead's fork before the fix round, `place_answers.py:198`). The F14 join reads a field no writer fills.** See point 2. The fix round
needs the Lead to choose the key, and the choice has to reach the role in the same move (the analyst's contract and the place list line;
TR2-13 is named for the charter text). The options I see:
- (a) keep `case` == obs id, document it, and make the reporter / `draft_cases` not lose the real case;
- (b) a dedicated draft key such as `place: <place id>`, read FIRST by `place_of_draft` and checked against `place_id_pattern`
  (a new field: producer = role, reader = place_of_draft; AR-22);
- (c) join by the target's `dispatch` + `index` against the draft's `triage_ref`, if the obs row's triage instance carries them (not
  verified; scout question).

Until that choice the line is unreachable, but harmless: a draft that does not match still gets its own `draft-<stem>` or `req-` place,
so nothing is lost silently. The docstring of rule (2) (`place_answers.py:179-180`) was not updated to name the id match (N2).

## Open-point action

**P1 (queue line or fix).** Point 1 above: the draft readers outside `place_answers` read a word-less draft as `confirmed_by_person`.
Line for «Остатки», if not fixed in this round: `a DRAFT with no confirmation reads confirmed_by_person in gate_brief.bug_rows,
story_bugs, write_texts, delivery_summary draft rows, dashboard drafts — keyword on confirmation_of for drafts | узел: <new node>`.

## Notes

- **N1 (tests, fix before merge, cheap).** `test_second_draft_of_another_place_not_lifted_by_the_answer` (test_walk_receipt.py) asserts
  only `("unconfirmed", [])`. Its f.json has `triage_ref: TC-2@a1` and `world("manual")` writes no TC-2 triage row. So the draft is void by
  `no APP_BUG triage row` whatever the place check does (probe2 b: `['no APP_BUG triage row']`), and the test cannot kill the defect it is
  named for. Add the TC-2 APP_BUG row and the manual check (as in probe3) and assert `BR.R_WALK_PLACE in problems`.
- **N2 (code quality, fix before merge).** `place_of_draft` docstring rule (2) still says "`case` is the `case` of an investigation target".
  The code now also matches the target's `id`, so the annotation lies.
- **N3 (duplication / consistency, fix before merge or queue).** `place_answers._json_object` (:49) is a new package-level JSON reader beside
  THE reader `hooklib.read_json` (`hooklib.py:694`, B-309), and it has the same name as `bug_records._json_object` (`bug_records.py:1196`),
  which has a different contract (`(dict, bool)`). place_answers imports bug_records as BR, so two same-named readers with two return shapes
  sit one hop apart. The test name "two_json_readers_are_one" is true inside the module only. Either use `hooklib.read_json(..., kind=dict)`
  and keep a why-less text, or extend hooklib with the `why` (a seam outside owns: queue). `_draft_json` is now a bare pass-through (:170).
- **N4 (code quality, queue).** `from investigation import _s` and `from manual_evidence import _squash` import private names across modules,
  and the second makes `place_answers` load `manual_evidence` (2236 lines, plus profile_contract, grammar, detector_verdict, event_store) at
  import time for a one-line squash. No cycle: manual_evidence does not import place_answers, and investigation imports it lazily. A public
  home (`hooklib` / `grammar`) is the AR-13 survivor.
- **N5 (seam).** `_draft_is_of_place` re-lists the drafts for every walk entry of every draft (`draft_listing` per call): O(drafts²) reads
  per `confirmation_of` sweep. That is fine at today's sizes. Pass the listing in if `story_bugs` grows.

## Standing questions (brief items 1-11)

1. Fit to spec: F13 lift yes (error direction down); F13 "settled" half missing (B1); F14 join on a guessed key (B2); F16/F17 yes; point 1 returned (correct to return; answer P1).
2. Builder's own decisions: returning point 1 as a question is right; requiring each draft's own walk entry is the safe direction; `_squash` None-wrapper kept correctly (`str(None)` would be "None").
3. Seams: additive; `places` split preserves order register -> targets -> drafts -> records; no caller signature changed.
4. Class completeness: draft-step readers (P1) queued/fix; `settled_answer` sibling (B1); `_names_of_draft` no defect; JSON readers (N3); private-helper imports (N4).
5. Tests: F13 lift test kills (RED quoted); another-place test does not kill (N1); F14 test pins the join but `obs in ids(places)` was already true before the diff; no junction test for the gate B packet (P1, not this diff).
6. DUPLICATION AND CONSISTENCY: N3 (`place_answers._json_object` beside `hooklib.read_json:694` and same-named `bug_records._json_object:1196`), N4; three hand-copies of "draft with no word" in place_answers (P1 collapses them). Grepped `def [a-z_]*json[a-z_]*(` over scripts/*.py.
7. CODE QUALITY: new functions all under 60 lines (`places` 21 lines, `_draft_places` 23, `_target_places` ~20); N2 docstring lie; `_draft_json` pass-through; no dead branches found.
8. Hygiene: CRLF kept (place_answers 920->943 CR lines = all lines; bug_records 2241->2253); selftest `--limits --lang` 4/4 per builder.
9. In-tree ratchets: none touched (census file not in the diff; `test_judgment_census.py` green in the builder's run). Branch `forge-check` (dup/lint) not read: no pipeline id given.
10. ARCHITECTURE: commit names AR-13, AR-22, AR-28. Touched and NOT named: AR-10 (the F14 join's requirement does not reach the role, B2) and AR-26/AR-27 marginally via the overloaded `case`. AR-13 is weakened by N3/N4 (a second reader).
11. JUDGMENT: none moved into code. The F13 lift stands on each draft's own role-written walk entry; the F14 join is a key equality. `judgment: none` is accurate.

## Trail

Read: the diff (all 6 files); `place_answers.py` 28-60, 170-330, 454-472, 570-648; `bug_records.py` 340-370, 896-945, 1040-1060,
1110-1150, 1190-1210, 1585-1660; `contract.py` 1910-1920, 2717-2722; `hooklib.py` 694-711; `gate_brief.py` 4099-4185, 4535-4552;
`delivery_summary.py` 78-106, 318-340; `factory_dashboard.py` 1274-1316; `investigation.py` 71-72, 140-200; `manual_evidence.py` 136-138;
`references/place-answers.json` 10-11; `references/artifact-writers.json` 237-240; `references/artifact-contract-run.md` (draft example
~102, fields 118-136); `agents/qa-failure-analyst.md` (grep place/case); `validate_artifacts.py` 413-480 (grep); the node row; the
finding section TR1-11; t-2010 F6, F13, F14, F16, F17, Q3; the builder report; the commit message.

Re-runs and probes:
- `python -B -m pytest D:/ws2/wt-tr1-11/ai-packages/qa-factory/scripts/tests/test_place_answers.py -q -p no:cacheprovider`
  -> `71 passed in 130.65s (0:02:10)`.
- probe1.py (word-less draft through the readers): output quoted under point 1.
- probe2.py (a sibling with no entry / another place / ghost record / list record): output quoted in B1, N1, point 3, point 5.
- probe3.py (another-place draft with a valid triage row): `place f: req-R-2`, `b) f step: ('unconfirmed', [], ['the walk was of another place'])`, `d step: ('reproduced_by_factory', ['walk'], [])`.
- `C.case_ids('obs-S6-qa-runner-4-0'), C.case_ids('TC-1'), C.case_ids('')` -> `[] ['TC-1'] []`.

The probes are in the session scratchpad
(`C:\Users\DEV1~1\AppData\Local\Temp\claude\2427f02dec2e7e5b\75598493-312c-4abf-a704-5a873b8f65b8\scratchpad\probe{1,2,3}.py`).

Negatives with their controls:
- "No writer puts an obs id in `case`": grep `obs-` over the package md/json returns place-answers.json and the changelog only. The same
  grep shape finds the producer `investigation.py:170` in the .py set.
- "No detail starts with 'no draft file'": case-insensitive grep returns 2 hits, the sentinel and a `_p(...)`-wrapped text.

The first pass's verdict block (superseded by the re-review block at the end of this file; kept for the record, fence tag removed so the
last block is the one checked):

    {"verdict": "fit_with_fixes",
     "blockers": ["B1 place_answers.py:619-632 settled_answer settles a bug place while a sibling draft of the same place stands unconfirmed; F13 second half",
                  "B2 place_answers.py:198 F14 joins on draft case == obs id, a field no writer fills; Lead picks the key"],
     "fixes": ["B1 sibling check in settled_answer", "B2 Lead fork on the join key", "P1 draft=True on confirmation_of for draft readers",
               "N1 TC-2 triage row and R_WALK_PLACE assert", "N2 docstring", "N3 one JSON reader", "N4 public home for _s/_squash"],
     "trail": {"reruns": [{"command": "pytest test_place_answers.py", "result": "71 passed in 130.65s"}]}}

## Re-review (fix round t-2299, `git -C D:/ws1/wt-tr1-11 show 9d81bad46`; branch head a345d0478 adds the report only)

**Verdict: not fit yet (`fit_with_fixes`). Two small items remain for the same node, R1 and R2, both text or data edits. One queue
line, Q1, and one note on TR4-15.** P1, B1, B2, N1, N2 and N3 are closed in code. My control re-run is quoted at the end. The
mechanical layer the worker attached is consistent with the diff: the red lines name the new test and the new keyword.

### (1) Point 1: closed for all five readers. No filed bug gets `draft=True`. No draft call is missed.
After the fix I re-grepped every caller of `confirmation_of(`, `_bug_confirmation(` and `_bug_step(` (non-test scripts). Draft calls with
`draft=True`:
- `bug_records.py:362` (`write_draft_texts`)
- `bug_records.py:1610` (`story_bugs`, the draft branch)
- `gate_brief.py:4129` (`bug_rows`)
- `delivery_summary.py:330` (the `draft_paths` loop)
- `factory_dashboard.py:1317` (draft rows, both the root and the no-root branch)
- `place_answers.py:212` (`_confirmation`)

Filed-bug calls stay on the default:
- `bug_records.py:1646` (`{confirmation, source_draft}` of a filed record)
- `delivery_summary.py:305` (proposals with `bug_file`)
- `delivery_summary.py:103` (the `.md` front-matter word; it returns before the keyword is used)
- `factory_dashboard.py:1308` (filed `b`)

Two remaining calls without the keyword, `place_answers.py:599` and `:640`, read drafts. Both sit behind the hand guard "no word ->
carrier missing" that the worker kept (:597, :638), so a word-less draft never reaches them. That is not a hole, but they are the two
copies the worker named (Q1). The keyword is decided by the caller, never guessed from the content. That direction is right: a filed
record with no word keeps `confirmed_by_person` (R12 pins this both on the board and in delivery).

### (2) B1: the error direction of `carrier missing`. Not a trap, but the door is wrong (R1).
- **Way out (FR-40):** an unsettled place does not hang. `close_unsettled` (`place_answers.py:745-785`) writes a `coverage_gap` for
  every non-settled place of source `draft` / `register`, and for `open` places in `carrier missing`. So S7 can close and the place ends
  as a named gap. Order of the close: the first loop (:717) withdraws the register line only for `settled` places, so the lifted draft's
  line is not withdrawn while a sibling stands. That is the safe side.
- **The door is not real in two of its cases.** Probe 4 (scratchpad probe4.py): a sibling `e.json` of `req-R-1` that already carries the
  walk entry but whose `triage_ref` has no APP_BUG row:

      place e: req-R-1 step e: ('unconfirmed', [], ['no APP_BUG triage row'])
      state: carrier missing
      why: another draft of this place, e.json, still stands unconfirmed: add the `walk` entry citing evidence/place-answer-req-R-1.json to it, or answer its own place

  "Add the walk entry" is false here: the entry is there, and the real reason (no APP_BUG triage row) is not named. "Or answer its own
  place" can never be used: by construction the sibling's own place IS this place (`place_of_draft(...) == place` is the join), and a
  place has one record. FR-1/FR-2: the refusal says what is wrong and names a door the receiver can use.
  **R1 (fix before merge, `place_answers.py:_unconfirmed_sibling` + `references/place-answers.json` `sibling_unconfirmed`):** name the
  sibling's own reasons, as `no_draft_carries` already does (`_confirmation(task, draft)[2]`, joined by "; "). Offer only doors that
  exist:
  - when the sibling has no walk entry: add one citing the record;
  - when it has one and still fails: its reasons;
  - in every case: merge it into the named draft when it is the same bug (the merged-draft road `_absorbs_place_draft` / `from_draft`
    exists), or leave it, and the close names the place as a gap.

  Drop "answer its own place". Test: the probe-4 world gives `carrier missing`, and `why` holds "no APP_BUG triage row" and not
  "answer its own place".
- Cost: `_unconfirmed_sibling` calls `_confirmation` with no rows/report for every draft, and `settled_answer` runs for every place in
  list / close / story_run. So triage facts are read about places x drafts times. Fine at today's sizes; pass the facts in when this is
  next touched (note, no line).

### (3) B2: the revert is complete. TR4-15 is executable with two gaps.
- **Code:** `place_answers.py:194` compares `case` only with `target.case`. The docstring says a target with no pinned case joins no draft.
  The test pins the revert (`case: obs-...` -> `draft-o`, test_place_answers.py:1012-1019). Re-grep: no other reader of the target id as a
  case.
- **R2 (fix before merge, `ai-packages/qa-factory/changelog.d/tr1-11-bug-draft-places.md`, not in the fix diff).** The fragment still
  says "a draft whose `case` is the key of an unpinned observation (`obs-<dispatch>-<index>`) now belongs to that observation's place".
  That behaviour is reverted, so the release note would describe something the package does not do. The note is also missing the two
  changes users will see: a draft with no `confirmation` word now reads "unconfirmed" in the gate B packet, the report, delivery and the
  board; and a `bug` answer no longer settles a place while another draft of it stands unconfirmed. The fragment is English-only (FR-30).
- **TR4-15 (`plans/piles/thinking-roles/batch-4-ostatki.md` row, finding `20261110-tr1-11-chernovik-nablyudeniya-klyuch-svyazi.md`).**
  It names the field `observation`, the files, the function, the rule's position (between the case rule and `violates`), the form check
  (`place_id_pattern`), the writer and the reader (AR-22), who writes the charter phrase (TR2-13), and four tests. A weaker model can do
  it, with two gaps the Lead should close in the node text before it is taken:
  - (a) "validate_artifacts.py: the field is optional". `validate_artifacts.py` validates FILED bug markdown (`check_bug_filing_header`
    :412, `check_bug_form` :429). It does not validate a draft JSON form. A weaker model would invent a draft validator. Say "no change
    in validate_artifacts.py" or name the exact function.
  - (b) "the analyst's contract slice". `references/slices/qa-failure-analyst/artifact-contract-run.md` is GENERATED by
    `python -B scripts/contract_slices.py --write` (`contract_slices.py:25`). Name the command so the slice is regenerated, not
    hand-edited.

### (4) The `sibling_unconfirmed` text against human-questions.md: it fails if a person reads it, and a person can.
The `why` of `carrier missing` becomes the `missing_prerequisite` of the `coverage_gap` line the close writes:
`state_texts.carrier_missing` = "the analyst's answer did not reach its record: {why}" (`place_answers.py:751`). Register lines are what
the report lists as gaps, so the text is person-facing. It carries three things human-questions.md «What the text may never carry»
forbids:
- a JSON draft file name (`e.json`);
- a factory record path (`evidence/place-answer-req-R-1.json`);
- a field name in code quotes (the walk word in backticks);
- and it is also a role instruction ("add ... to it").

On top of that, the frame "the analyst's answer did not reach its record" is false in this case: the answer did reach it. The texts
`no_confirmation` / `no_draft_carries` that were already there have the same defect (the confirmation field in quotes in a gap line),
so this is a class, not this line alone.
**Q1 (queue line, class across the carrier-missing family):** `carrier missing reasons (no_confirmation, no_draft_carries,
sibling_unconfirmed) are role refusals copied into the person-facing coverage_gap text: split a role why from a story-worded gap text;
plus the two hand copies of the no-word guard (place_answers.py:597, :638) collapse into draft=True | узел: <new node>`. The R1 rewrite
should already keep the role text and the gap text apart if that is cheap, but it is not required for this node.

### (5) Fixtures in the unrun files that write a word-less draft and expect `confirmed`: none found by reading.
I searched the unrun test files that write `bug-drafts` and mention a confirmation word or count (test_gate_brief_and_retro,
test_bug_filing, test_bug_link_s9, test_human_reading, test_report_facts, test_validate_artifacts_report, test_gate_preflight,
test_handoff, test_bug_manifestations, test_bug_neighbours):
- The `confirmed_by_person` expectations are on FILED markdown bugs: test_validate_artifacts_report :895 BUG-1.md, test_report_facts
  :190 / :1233 BUG-1.md, and test_bug_link_s9's HEAD.
- test_bug_filing F5 (:313) writes its draft WITH `"confirmation": "unconfirmed"`.
- test_bug_link_s9's word-less `DRAFT` (:36) is paired with a filed BUG-1.md, so `story_bugs` skips it in the draft branch, and L7
  checks `state`, not the word.

What WILL change in CI: the word-less draft fixtures of **test_gate_brief_and_retro.py** now render the gate B tail " · unconfirmed —
nobody has reproduced it" on their rows. These are `_merged_fixture` qty/cart (:511-528), the drafts at :633 / :649, sixth-tag (:794)
and one.json (:1019). By grep I found no exact-line or check_not_in("nobody...") expectation on those rows. The golden at :640-641
compares two renders under the same code. `TECHNICAL` in test_human_reading (:34) does not match the tail. So I expect them green, but
this is the file CI must judge. If a row-length cap or a byte-golden against a stored file fails there, the fix is
`"confirmation": "unconfirmed"` in the fixture, never `draft=False`.

### Re-review trail
- Read: the fix diff (13 files); the fix report's claims checked against the diff.
- Re-grepped callers: `confirmation_of(|_bug_confirmation(|_bug_step(` over scripts/*.py (the positive control finds the 6 draft calls
  and 4 filed calls listed above).
- Read code: `place_answers.py` 563-645, 694-785; `references/place-answers.json` 42-56; `references/human-questions.md` 25-60;
  `validate_artifacts.py` 412-431 (grep); `contract_slices.py:25`; the TR4-15 finding and row.
- Read the unrun fixtures named in (5).
- Re-run: `python -B -m pytest .../test_walk_receipt.py -q -p no:cacheprovider` -> `26 passed in 23.19s`.
- probe4.py: output quoted in (2).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "R1 place_answers.py _unconfirmed_sibling + place-answers.json sibling_unconfirmed: the door says add the walk entry when the sibling already has it and offers answer its own place, which cannot exist (the sibling's place is this place); the sibling's own reasons (probe4: no APP_BUG triage row) are not named (FR-1, FR-2)",
    "R2 changelog.d/tr1-11-bug-draft-places.md still announces the reverted obs join and omits the draft=True reading and the sibling refusal"
  ],
  "fixes": [
    "R1: name the sibling's reasons from _confirmation, offer only real doors (add the entry when absent, merge into the named draft, or leave it as a gap), drop answer its own place; test on the probe4 world",
    "R2: rewrite the changelog fragment to the shipped behaviour, English only",
    "Q1 queue: carrier missing reasons are role refusals copied into the person-facing coverage_gap text (file names, record path, field in quotes, false frame); collapse the two hand no-word guards into draft=True",
    "TR4-15 node text: validate_artifacts.py has no draft-form validator (say no change or name the function); name contract_slices.py --write for the analyst slice"
  ],
  "class_completeness": "Point 1 closed: all six draft readers pass draft=True, four filed-bug calls keep the default, two guarded draft calls remain (queued Q1). B1 closed with a real way out (close writes a gap); door text wrong (R1). B2 revert complete, the need carried by TR4-15 with two text gaps. carrier missing text family person-facing defect queued (Q1). Unrun fixtures: none expects confirmed for a word-less draft; test_gate_brief_and_retro word-less fixtures change their gate B tail, CI judges.",
  "trail": {
    "read": [
      "git show 9d81bad46 (wt-tr1-11)",
      "docs/tasks/specs/reports/t-2299-tr1-11-fix-report.md claims vs diff",
      "ai-packages/qa-factory/scripts/place_answers.py 563-645 694-785",
      "ai-packages/qa-factory/scripts/bug_records.py 355-365 1116-1140 1600-1650",
      "ai-packages/qa-factory/scripts/delivery_summary.py 78-106 292-335",
      "ai-packages/qa-factory/scripts/factory_dashboard.py 1270-1318",
      "ai-packages/qa-factory/references/place-answers.json 42-56",
      "ai-packages/qa-factory/references/human-questions.md 25-60",
      "ai-packages/qa-factory/changelog.d/tr1-11-bug-draft-places.md",
      "plans/piles/thinking-roles/findings/20261110-tr1-11-chernovik-nablyudeniya-klyuch-svyazi.md and row TR4-15",
      "scripts/tests test_gate_brief_and_retro, test_bug_filing, test_bug_link_s9, test_human_reading, test_report_facts, test_validate_artifacts_report fixtures"
    ],
    "reruns": [
      {"command": "python -B -m pytest wt-tr1-11/ai-packages/qa-factory/scripts/tests/test_walk_receipt.py -q -p no:cacheprovider", "result": "26 passed in 23.19s"},
      {"command": "scratchpad probe4.py sibling with walk entry and no APP_BUG row", "result": "carrier missing; why tells to add the walk entry it already has and to answer its own place; real reason no APP_BUG triage row not named"}
    ]
  }
}
```
