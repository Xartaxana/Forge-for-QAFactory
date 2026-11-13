# t-423: critic diff gate, pair OH8-7f / OH8-7g (judgment census rows)

Reviewed: worktree `C:\QAFactory\forge-repo\.claude\worktrees\oh8-7b`, commits 097f58d (OH8-7f, 24 rows) and a238574 (OH8-7g, 29 rows),
read only from commits (`git diff`, `git archive a238574` into the scratchpad). The working tree was never read.
Spec: t-346 §1, §2.2, §3.1, §3.3, §4, §6a, §6b. The pair review is the INPUT to acceptance. Accepting is the Lead's decision.

## Verdict per node

| node | commit | verdict | one line |
|---|---|---|---|
| OH8-7f | 097f58d | **fit** | I agree with all 24 rows. The four E3 notes hold on every call path (callers listed in K2). Clean diff: one ratchet line, 24 inserted rows |
| OH8-7g | a238574 | **fit_with_fixes** | I agree with 27 of 29 rows. F1: `question_register.py::record_case` should be xref, not shape (no ratchet change). F2: `person_words.py::_from_file` should be safety/intent, not shape (`safety` 79 -> 80) |
| pair | — | **fit_with_fixes** | Neither fix blocks the merge. Both are fixture-only and fit into the fix round 6b already plans "after OH8-7g lands" |

## Findings

**F1 (7g, fix, no ratchet change): `question_register.py::record_case` is xref, not shape.** The single raise at :1196 refuses on
an aggregated problem list. At :1185 one of those problems is `elif case_ids is not None and wanted not in set(case_ids)`: the
case id has to resolve against the story's case ids. Spec 4.2 step 3 puts "an id resolves" under xref, and the higher reading
wins. The builder wrote shape because the decision and where/by are closed tokens (rule 3). That is true of :1189-1190, but it
overlooks :1185. Concrete case: `record_case(root, "TP1-1_TC_099", "manual", ..., case_ids=["TP1-1_TC_001"])` is refused because of
the join, not because of a token. Effect: xref is not a ratchet key, and the row's roles stay the same, so no ratchet moves.

**F2 (7g, fix, `safety` 79 -> 80): `person_words.py::_from_file` is safety, owner intent, the twin of `read`.** The Lead answered
`read` = safety/intent because its :151 refusal "turns a silent truncation of a person's words into a refusal". The raising
condition at :150 is `inline is not None and str(inline).strip() and via_cmd()`. Nothing in that condition reads the words. It is
safety only because of what it protects, which is the census's own clause "a guard on ... a person's words". `_from_file`, in the
same reader and on the same carrier, refuses the same harm:
- :100-101 `if b"\x00" in raw: raise _not_utf8(...)`. The comment says UTF-16 can pass UTF-8 decoding, and "a person's words never carry one".
- :102-105 a strict decode instead of a replacement.

The module docstring at :27-29 says these refusals exist because replacement "would store a different text than the person's".
If the first is safety and the second shape, the same guard has two classes in one reader (P31, one road), and the count errs on
the unsafe side of a shrink-only ratchet (6b's reason for keeping rule 2). Classifying `_from_file` purely by its raising
condition (NUL, not decodable, empty) would also strip `read` of safety. One of the two rows has to move. Of the two, `_from_file`
moving up is the safe direction. The empty-file refusal (:111) and the path refusals (:82-96) are presence checks and lose to the
guard (CLASS_ORDER). If the Lead prefers to restate rather than fix, the restatement has to cover both rows the same way.

No other row differs. The class-wide notes (K6) and the Lead items (K8b) are not builder fixes.

## K1: all 53 rows

Every raise site was read in the byte copy at a238574, together with its function. Read whole: every safety row, every E3 row,
and every row on the K2 lists, which together cover 33 of the 53. The other 20 were read whole as well, since all are under 130
lines, except `ticket_light.py::project` and `::references`, where I read the guard block and the raise lines. Columns: written
class / roles / owner | my reading at the raise sites | verdict.

### OH8-7f (24), all `[conductor]`. The roles follow the same-file precedent per 6b (not reopened here)

| row | written | my reading (file:line) | |
|---|---|---|---|
| ticket_light::_id_list | shape/data | :697-698 list of str ids | agree |
| ::_load_table | shape/data | :78 readable, :84 JSON, :87 object | agree |
| ::_need_list | shape/data | :95 list of str, :98 non-empty | agree |
| ::_norm_names | shape/data | :371 list of str, :375 non-empty after normalising | agree |
| ::project | shape/data | :730-731 raw issue is an object with a `fields` object | agree |
| ::references | shape/data | :1071-1072 `FORMS_DAMAGE` (the forms table is damaged) | agree |
| ::ticket_url_regex | shape/data | :1014-1015 the table has a `ticket` kind (presence) | agree |
| ticket_adapter::write_paste_references | shape/data | :1635-1636 FormsTableError re-raised as TableError | agree |
| source_inventory::_extra_headings | shape/data | :957-958 list of str | agree |
| ::attachment_policy_for | shape/data | :1376-1377 object, :1387-1390 rules/suffixes shape | agree |
| source_exclusions::read_record | shape/data | :306 readable, :309-320 schema_version, list, kind in KINDS, id present (whole) | agree (K2) |
| ::write_record | safety/data | :454-457 a different list over an existing record (rule 1: refuses an overwrite); :461-462 inventory exists (an ordering precondition, loses to the guard) (whole) | agree |
| vcs_evidence::api | shape/data E3 | :57 CLI present, :62 timeout, :64 OSError, :65-69 return code and HTTP code read from glab's output (program output, not words), :73 JSON (whole) | agree (K2) |
| ::collect | xref/data E3 | :126 revision present, :132 diff truncated, :134-135 sha/updated_at equal before and after the read (a join); all inside try :118, caught :138 (whole) | agree (K2) |
| ::pages | xref/data E3 | :101 a list, :103-104 the page signature seen twice (a join) (whole) | agree (K2) |
| ::readiness | shape/data E3 | :198-199 host form (present, no leading `-`, no `/`), caught at :208 in the same function (whole) | agree (K2) |
| local_keys::_local_row | shape/data | :95 forms table readable, :97 `ticket.local` row present | agree |
| ::mint | safety/data | :154 text, :159-160 tracker prefix (xref), :166-180 the O_EXCL claim: `:180` refuses when every attempted number is held by another writer (rule 1) (whole) | agree |
| onboard_apply::_load_json | shape/data | :1806 JSON readable | agree |
| ::_proposal_for | shape/data | :1869-1870 a proposal is present | agree |
| ::apply | safety/intent | :1483 phase, :1488 blocked, :1497-1498 a live writer (rule 1), :1499-1500 self-hash, :1501-1504 a recorded approval of THIS proposal (a person's word), :1507-1508 answers, :1517-1518 drift outside the home (rule 2) (whole) | agree (K2) |
| ::main | safety/intent | :1948-1949 one approval = one key (scope of a person's word), :1965 blocked, :1970-1971 drift (rule 2), :1976-1977 ref presence; caught at :1991 and turned into exit 1/2 (a CLI refusal, not E3) (whole) | agree (K2) |
| ::plan | xref/data | :890-891 presence, :900-903 sealed `input_hash` vs the hash of the config on disk; writes nothing (FR-45) (whole) | agree; consistent with 7d `execution_request.begin` (a digest join = xref) |
| ::set_login_ui | shape/data | :1839-1840 recipe problem, :1842-1843 config presence, :1854-1856 validate | agree |

### OH8-7g (29), all `[conductor]`

| row | written | my reading (file:line) | |
|---|---|---|---|
| s5_plan::_dispatches | shape/data | :277-278 state is a mapping, :281-282 dispatches is a mapping | agree |
| ::_scope | shape/data | :269-270 `derived` flag | agree |
| ::_words | shape/data | :475-476 vocabulary readable, :483-484 three lists present; this is the factory's own file, not a person's or role's words (whole) | agree |
| ::load | shape/data | :99-100 JSON object, :102-103 schema | agree |
| ::refresh | shape/data | :371-372 `cases` is a list | agree |
| ::remarks_of | shape/data | :1084-1086 a chain element flagged `unreadable`; no remark text is read (whole) | agree |
| question_register::_raise | xref/data | :1267 Then number in the case's Thens, :1273-1276 an oracle already present, :1277 claim form, :1286/:1289/:1292 register file, :1301-1303 same (case, Then) with a different `_shown` sentence (whitespace-collapsed equality) (whole) | agree; see K6 (1) |
| ::answers_lock | safety/data | :803-804 LockBusy (another writer holds it), :806-807 LockBroken (whole) | agree |
| ::raise_question | shape/data | :1240-1241 case file readable as UTF-8 | agree |
| ::raise_role_question | xref/data | :1519-1521 role_question_errors, :1527/:1530/:1533 register, :1535-1539 same `raised_from` with another text (`_same_question`, whitespace-collapsed equality, :1509-1510) (whole) | agree; see K6 (1) |
| ::record | safety/intent | :910 aggregates :884 (id resolves), :885-887 a settled row with another (status, reading) (guard on a person's recorded answer), :889, :892-898, :902 one Latin letter (token form), :905 (whole) | agree (K2) |
| ::record_case | shape/data | :1196 aggregates :1184 blank, **:1185 id in `case_ids` (a join)**, :1189-1190 decision in the vocabulary, :1193 hash form (whole) | **differ: xref (F1)** |
| question_stop::_as_count | shape/data E3 | :67/:70/:73 number, whole, non-negative (whole) | agree (K2) |
| ::_as_share | shape/data E3 | :82-106 number or `n/d`, finite, 0..1 (whole) | agree (K2) |
| ::defaults | shape/data E3 | :119-120 `reason_words` is a str->str map, caught at :122 and re-raised as RuntimeError (whole) | agree on the class; E3 is the programming-error arm (K2) |
| person_words::_from_file | shape/data | :82-96 path readable, **:100-101 NUL, :102-105 strict UTF-8 (refuses storing a text other than the person's)**, :110-111 empty (whole) | **differ: safety/intent (F2)** |
| ::read | safety/intent | :145-146 both carriers given (shape), :150-151 inline words on the cmd route, where they would be cut (guard on a person's words) (whole) | agree (K2) |
| grammar::find_blocks | shape/data | :666-667 damaged markers | agree |
| ::render_block | shape/data | :695-696 name in the closed `REPORT_BLOCKS` | agree |
| ::replace_block | shape/data | :685-686 block present in the text | agree |
| assertion_detectors::_claims_once | xref/data | :238-240 a suffix claimed by entries of two keys (a join across entries; precedent `gate_registry._no_duplicates` xref) | agree |
| ::_document | shape/data | :203-204 readable JSON | agree |
| ::_keyed_table | shape/data | :212-213 key present, :217-218 non-empty object | agree |
| ::assertion_detectors | xref/data | :256-257 a suffix claimed twice within the key | agree |
| ::shape_patterns | shape/data | :297-298 key, :302-303 non-empty list of str, :306-309 each compiles; the patterns are compiled, never run over test code here (whole) | agree |
| machine_facts::_check_scalar | shape/data E3 | :942-943 non-finite number, :945-948 lone surrogate (whole) | agree (K2) |
| ::_json_line | shape/data E3 | :1002-1003 line over the parse limit (whole) | agree (K2) |
| ::_parse | shape/data E3 | :915-920 JSON decode / recursion / value refusal (whole) | agree (K2) |
| driver_dispatch::s5_open_windows | shape/data | :2720-2739 windows / dispatches / scopes present and typed; it leaves the module (callers driver_stage_s5.py:79, :103, :116; driver_stage_plan.py:1090), so not E3 (whole) | agree |

## K2: the open questions answered by the Lead

### 7f
- `read_record` = shape: **agree.** The raising conditions are parse, schema, closed kind and id presence. What the function
  protects (the person's exclusion word) does not move it under rule 1 as restated in 6b. `manifest_problems` has a different
  raising condition: it refuses citing an excluded source, a guard on a person's word. So they are not one guard shape.
- `readiness` = shape, E3: **agree, E3 verified.** The raise at :199 is caught at :208 in the same function. The re-raise at :206
  sits inside the outer try and is caught at :208 too. The only caller is readiness.py:1249 (`from vcs_evidence import readiness
  as api_readiness`), which gets a dict. Option-injection reading of the leading-`-` test: the host comes from the project's own
  `git remote get-url origin` and goes in as one list-argv element after the value-taking flag `--hostname`. The test refuses
  nothing (E3), and its condition is the form of a host name. My view that a dash value after a value-taking flag is not parsed as
  a new option is an estimate: I did not verify it against glab. Shape stands. The argv-guard class is a Lead note (K8b 5), not a fix.
- `apply` = safety/intent: **agree.** :1498 is rule 1 (a live writer). :1504 requires a recorded approval of THIS sealed proposal (a
  person's word, so intent). :1518 is rule 2 (drift of written paths outside the home). Context, not a finding: for an install
  proposal, `main` records a headless approval itself when `--approval-ref` is absent (:1975-1979). config_contract.py:2045-2049
  refuses headless only for one-command proposals, so this is the designed road. The intent guard still tests a recorded approval
  of this proposal hash.
- `main` = safety/intent: **agree** (:1949 the scope of one approval, :1971 drift). Its refusals are caught at :1991 and printed
  with exit 1/2. That is a CLI refusal to the role, not E3.
- The four E3 rows, caught on every call path (callers found by a case-insensitive grep of `vcs_evidence` over scripts/ outside
  tests/. Positive control: the same grep found the `readiness as api_readiness` import):
  - `api`: called at :201 and :207, both inside readiness's try :194-208, caught at :208. It is also the default `read=` of
    `collect` (:119, :121, :123, :133, inside try :118, caught at :138) and of `pages` (:99, only reached from collect :130).
    No external importer of `api`: the importers take `mr_iid`, `api_capability`, `read_api_receipts`, `git_readiness`, `readiness`.
  - `collect`: :126, :132 and :135 inside try :118, caught at :138. Its one caller, `main` at :696, gets a record. `parse_mr` at
    :113 is outside the try, but it is its own unit and raises plain ValueError.
  - `pages`: one caller, collect at :130, inside the try. Holds.
  - `readiness`: above. Holds.

### 7g
- `record` = safety/intent: **agree** (:885-887 refuses a second, different answer on a settled row; a person's word). The
  wording of the Lead's reason needs one restatement (K6 (1), K8b 1).
- `person_words.read` = safety/intent: **agree.** Consequence: F2.
- `answers_lock` = safety/data: **agree** (:804 refuses while another writer holds the lock, rule 1).
- `record_case` = shape: **differ: xref (F1)**, no ratchet change. The builder's analog: there is NO settled-answer guard, confirmed
  (:1174-1202 have nothing like :885-887). This is a behaviour question for the Lead queue, not a defect of the row. The row
  classifies what the function refuses today. Whether a second, different case decision splits the readers the way H6 did for
  answers is a factory question (K8b 2).
- `defaults` = shape with E3 although it re-raises RuntimeError: **agree; keep the note.** The family exception `_Invalid` is
  caught at :122 inside the function. The RuntimeError is spec E3's second arm, "guards a programming error": an unusable
  shipped data file, never a project's value. The note says this already. For the queued override node it is not "refuses
  nothing" in the caught sense. Its RuntimeError reaches `_limits` :148 and driver_dispatch.py:1601 with no handler, so the override
  node must judge it under the programming-error arm, not mark it non-blocking by analogy with readiness (K8b 4).
- `_from_file` = shape: **differ: safety/intent (F2).**
- E3 checks:
  - `machine_facts._parse`: callers `_leaves_of` :839 (caught :840 -> None), `json_text` :997. `json_text`'s callers are
    `_json_line` :1004 -> `jsonl_text` :1015 (caught :1016) and the redaction run :1072 (caught :1075/:1077/:1079).
  - `_check_scalar`: reached only through `_check` :934 <- `_parse` :921, so the same catch sites apply.
  - `_json_line`: one caller, :1015, caught at :1016.
  - No external caller of the three: `collect_pack.py` and `audit_factory.py` use other names (load_rules, compile_redactor, CATEGORIES ...).
  - `_as_count` / `_as_share`: callers `defaults` :116/:117 (caught :122) and `_limits` :170/:176 (caught :171/:178); the
    `raise` at `_as_share` :101 sits inside its own try and propagates to those two. No external caller (grep of
    `_as_count|_as_share|_Invalid` over scripts/ outside tests/). E3 holds for all five.

## K3: E9 (words and content)

Rows walked, with the condition quoted:

| row | condition |
|---|---|
| `person_words._from_file` | `b"\x00" in raw`, `raw.decode("utf-8-sig")`, `not text.strip()` |
| `person_words.read` | `path is not None and inline is not None`, `str(inline).strip() and via_cmd()` |
| `question_register._raise` | `then not in numbers`, `str(entry.get("source")) != "unknown"`, `old != new` over `_shown`, whitespace collapse only |
| `raise_role_question` | `_same_question`: `" ".join(a.split()) == " ".join(b.split())` |
| `record` | `(status, reading or "") != (row["status"], row["reading"])`, `re.fullmatch(r"[a-z]", reading)` (a letter token) |
| `record_case` | `wanted not in set(case_ids)`, `decision not in vocab["case_decisions"]` |
| `_common_problems` (called by both; existing row) | blankness and vocab membership of where/by |
| `s5_plan._words` | `not (shapes and fit_map and strategies)` |
| `s5_plan.remarks_of` | `element["unreadable"]` |
| `assertion_detectors.*` | key presence, list/object shape, `re.compile(pattern)`, suffix collisions |
| `vcs_evidence.api` | `re.search(rf"\b{n}\b", error)` over glab's stderr/stdout, plus `classify_failure`, a regex over program output, not a person's or role's words |

**None found.** No raising condition of the 53 depends on what free words say or what content means. The only text comparisons
are whitespace-collapsed equality (a join, the same reading as 6b rule 3 for `record_answer`) and closed-token membership.

## K4: AR-20 and byte hygiene

Recomputed by a scratchpad script (`k4.py`) from the three parsed fixtures (3589f5b, 097f58d, a238574):

| commit | new rows | removed | changed | ratchet keys moved, against the new rows naming them |
|---|---|---|---|---|
| 7f | 24 | 0 | 0 | `blocking_per_role.conductor` 606 -> 630 (24 rows name it); `safety` 72 -> 76 (4 rows: write_record, mint, apply, main) |
| 7g | 29 | 0 | 0 | `blocking_per_role.conductor` 630 -> 659 (29 rows); `safety` 76 -> 79 (3 rows: answers_lock, record, read) |

- No other key moved in either commit.
- Class tallies: 7f 17 shape / 3 xref / 4 safety; 7g 22 / 4 / 3. Both match the commit messages.
- `blocks_override` added: 0 in both commits. E3 notes: 7f `api`, `collect`, `pages`, `readiness`; 7g `_check_scalar`, `_json_line`,
  `_parse`, `_as_count`, `_as_share`, `defaults`.
- Both commit messages carry the raise lists, and they match the recomputation.
- F2 would add `safety` 79 -> 80 (named in K8a).
- Byte hygiene: `git diff --numstat` gives 25+/1- (7f fixture) and 30+/1- (7g fixture). The single `-` line in each is the
  `"ratchet"` line. Every new row sits in sorted position between its neighbours (`ord.py`), and the count of order inversions in
  the whole file is 21 before and after both commits (pre-existing). The `about` text is unchanged. The 7c class (13 rows
  rewritten byte-wise) does not recur in these two commits. Its own fix (F1 of t-411) is still pending in 6b's fix round.

## K5: §3.1 lists against the rows

- 7f added == the §3.1 block (24/24); 7g added == its block (29/29). No unlisted rows, none missing (`k4.py`).
- `SUBCLASS_UNIT_FILES` at a238574 has 28 entries, no duplicates and no `::` entries: 1 + 6 + 6 + 7 + 8. The 7f and 7g files
  are whole-file entries.
- Ceiling: 74 -> 50 at 7f, 50 -> 21 at 7g. The control re-run at a238574 prints `subclass_pending=21 (ceiling 21)`. I did not
  re-run at 097f58d. 50 is checked by arithmetic (74 - 24) together with 7g's dense 21 (50 - 29).
- The test diffs change only the ceiling line and the tuple lines: grepping the changed lines minus those two patterns gives nothing.

## K6: class-wide

1. **Same guard shape, two classes inside 7g: `record` (safety/intent) against `_raise` / `raise_role_question` (xref).** All three
   refuse a second, different entry for a key that already stands (:885-887, :1301-1303, :1535-1539). The Lead's answer calls
   `record`'s class "the chain's standing answer for that guard shape". Read literally, that moves the other two to safety
   (+2 safety). My reading: what separates them is the carrier, not the shape. `record` guards a PERSON's recorded answer (the
   census safety clause); the other two guard a role's question text against a silent drop (a join), so xref is right. I propose
   the Lead restate the answer as "a guard on a person's recorded word" (K8b 1). No row moves.
2. **`person_words._from_file` against `read`**: F2.
3. `source_exclusions.read_record` (shape) against `manifest_problems` (safety/intent): different raising conditions (parse against
   a citation of an excluded source). Consistent.
4. `onboard_apply.plan` (xref, input_hash) against 7d `execution_request.begin` (xref, digest): consistent. `local_keys.mint` (safety,
   the refusal IS the failed claim) against `begin` (an O_EXCL claim that refuses only on the digest): consistent under rule 1 by
   raising condition. `answers_lock` against 7d `_claim_locked` (both safety/data): consistent.
5. E3 siblings outside the diff: the EXISTING row `machine_facts.py::_check` (shape, no note) raises TooDeep at :937 on exactly the
   `_parse` catch path, so it is a non-refusing unit with no E3 mark. It is named for the override finding (K8b 4).
6. The builders' analogs:
   - Copied register-read block: **confirmed twice, not three times.** `_raise` :1283-1292 and `raise_role_question` :1524-1533
     carry identical texts. `raise_from_handoff` reads the handoff FORM (:1576-1580) and delegates to `raise_role_question`; it
     carries no third copy of the register read. claim_projector.py:278 holds a third text of the same register refusal (another
     reader). Queue (K8b 6).
   - `via_cmd` and a missing `run_py_entry`: **not confirmed as a defect.** On the cmd route run_py_entry.py is the process entry
     and aliases itself into `sys.modules["run_py_entry"]` at :159-162. hooks/run-py.cmd:40 starts it by path, so on that route
     the import never fails. `ImportError` is reachable only when run_py_entry.py is absent, and then the cmd route itself cannot
     run. False is then the true answer. No item.
   - Goto-by-exception in `defaults`: **confirmed** (:120 raised, :122 caught). Same in 7f `vcs_evidence.readiness` (:199/:208).
     Code quality, queue.
   - `record_case` has no settled guard: confirmed (K2), a Lead queue question.
   - `onboard_apply.main` gives exit 1 against exit 2 (7f note): confirmed at :1993. Queue.
7. Roles (6b keeps the same-file precedent; new instances for the roles class node, one line each):
   - `question_register.raise_question` / `_raise`: run by the S4 case author (docstring :1222-1226).
   - `vcs_evidence.*`: on qa-scout's card (agents/qa-scout.md:70).
   - `s5_plan.*`: `s5_plan.py --check` is on qa-automator's card (agents/qa-automator.md:68).
   - references/role-commands.json names none of the 15 files. Positive control: it names manual_evidence.py 7 times.
8. Written-path class node (6b): no new instance in these two nodes. `onboard_apply.apply`/`main` drift is already counted as
   safety. Factory-function blind spot (6b): no new instance checked; not in scope.

## K7: standing questions

- **6 DUPLICATION AND CONSISTENCY: none found in the diff.** The diff adds data rows and tuple entries and no code. Grep of the
  test diff for changed lines other than `SUBCLASS_PENDING_CEILING =` and the tuple strings: empty. Positive control: the same
  pipeline without the filter shows those lines. The duplications found in the READ scripts are queued (K6 6).
- **7 CODE QUALITY: none in the diff** (no new code). The scripts' own observations are confirmed and queued: K6 6.
- **9 IN-TREE RATCHETS:** named row by row in K4. Both commit messages carry the lists. F2 adds `safety` 79 -> 80.
- **10 ARCHITECTURE:**
  - AR-29, AR-20, AR-13, AR-22 and AR-28 are named in both messages.
  - `refusal_registry.py` is not in either diff (`git diff --stat 3589f5b a238574`: two files).
  - `ast.Raise` occurs 0 times in test_judgment_census.py and once in refusal_registry.py (the control).
  - AR-22: the producer constant and its one reader both live in the test, unchanged in shape.
- **11 JUDGMENT:**
  - No class lowered: 0 changed rows.
  - No `blocks_override` added.
  - The only scan constants edited are `SUBCLASS_UNIT_FILES` and `SUBCLASS_PENDING_CEILING`.
  - `judgment: adds data check test_judgment_census.SUBCLASS_UNIT_FILES` is the gate form for a raise of only
    `blocking_per_role.*` / `safety` (spec E10). It is true here.
  - The two class judgments I differ on are F1 and F2.
- **12 ONE ROAD:**
  - No new exclusion. The temporary second road shrinks 50 -> 21, and OH8-7h closes it.
  - One residual of this class found and fixed this round: F2 (one guard on a person's words, two classes).
  - One proposed node with an owner: K8b 2, the settled guard for case decisions (the same protection as H6, one road for both
    answer kinds). The owner is the Lead.
  - The roles and written-path residuals are already 6b nodes.

## K8: fix lists

### K8a: for one fresh builder round (fixture only; fits into the 6b round "after OH8-7g lands")
1. `question_register.py::record_case`: shape -> **xref**, roles and owner unchanged. Ratchet: none. Why: F1. The raise at :1196
   carries the join :1185 (the case id resolves against the story's case ids).
2. `person_words.py::_from_file`: shape -> **safety**, owner **intent**, roles unchanged. Ratchet: `safety: 79 -> 80 -- census
   classifies subclass refusers of person_words.py (OH8-7g fix round): _from_file`, named in the commit message. Why: F2. The
   :100-105 refusals are the twin of `read` :150-151, which the Lead answered as safety/intent.

### K8b: for the Lead (decisions and queue; none is a builder's to take)
1. Restate the `record` answer as "a guard on a person's recorded word", not "that guard shape". Otherwise `_raise` and
   `raise_role_question` follow (+2 safety). Recommendation: restate, move nothing.
2. Queue finding (question_register): `record_case` accepts a second, different decision for a case already decided (no guard
   like :885-887). Does a reader take the last record while the plan follows the first (the H6 split)? If yes, the guard is one
   road with `record`'s.
3. Roles class node (6b): add `question_register.raise_question`/`_raise` (S4 author), `vcs_evidence.*` (qa-scout card :70) and
   `s5_plan.*` (qa-automator card :68).
4. E3 override finding (`20261113-gate-form-...`): add the existing `machine_facts.py::_check` (same catch path, no note). Mark
   `question_stop.py::defaults` as the programming-error arm (its RuntimeError leaves the module unhandled), not as "refuses nothing".
5. The argv-option guard (`vcs_evidence.readiness` :198, a leading `-` in a value passed to a subprocess): if the Lead reads
   argv-injection guards as safety, that is a class across subprocess callers and needs a scout first. Recommendation: shape stands.
6. Queue, code quality:
   - The register-read block is duplicated (`_raise` :1283-1292 / `raise_role_question` :1524-1533; claim_projector.py:278 is a
     third text of the refusal).
   - Goto-by-exception in two places: `vcs_evidence.readiness` :199/:208 and `question_stop.defaults` :120/:122.
   - `onboard_apply.main` splits refusals into exit 1 and exit 2 (:1993) against the module docstring's one refusal form.

## Trail

Read (all from commits; package byte copy of a238574 under the scratchpad `g/`, fixtures of 3589f5b and 097f58d under `f/`, `f7/`):
- t-346 spec §1-§4, §6, §6a, §6b, §7-§10 (whole); t-411 review (structure, K2, verdict block); critic-diff-brief.md (two layers, 6-12).
- Both commit messages; `git diff 3589f5b 097f58d` and `git diff 097f58d a238574` (both files, whole).
- Scripts read whole or at the raise sites, as stated per row in K1:
  - ticket_light.py :74-100, :369-378, :694-700, :713-838, :1008-1017, :1050-1269
  - ticket_adapter.py :1623-1663; source_inventory.py :955-961, :1364-1393
  - source_exclusions.py :294-321, :446-473, :922-969; local_keys.py :91-99, :148-181
  - vcs_evidence.py :1-230, :680-711; onboard_apply.py :844-1044, :1464-1552, :1802-1872, :1925-2000; config_contract.py :2045-2050 (grep)
  - s5_plan.py :89-105, :266-284, :353-381, :469-486, :1077-1092
  - question_register.py :372-376, :788-811, :832-921, :1174-1312, :1509-1600
  - question_stop.py :1-200; person_words.py :1-170; run_py_entry.py (grep of VIA_CMD / sys.modules)
  - grammar.py :659-697; assertion_detectors.py :190-312; machine_facts.py :830-1085 (the catch paths)
  - driver_dispatch.py :1595-1606, :2703-2750
- Greps (each with its positive control in the text):
  - callers of vcs_evidence, question_stop, `_as_*`, `_raise`, s5_open_windows, machine_facts, `_from_file`
  - `ast.Raise`; role-commands.json; agents/*.md
  - the E3 findings file: present on read-main, absent at a238574, as the builder said

Re-runs:
- `python -B <scratchpad>/g/ai-packages/qa-factory/scripts/tests/test_judgment_census.py` -> `=== judgment_census: 26/26 ok ===`, exit 0.
  Totals line: `census: 279 files scanned, 1120 units; shape=816 xref=193 ... safety=79; ... conductor=659 ...; subclass_family=55 subclass_pending=21 (ceiling 21)`.
- `sites.py` (refusal_registry.sites with raise_family over the byte copy): the raise-site lines of every function in K1.
- `k4.py`: `7f added 24 removed 0 changed 0 spec 24 added==spec True`; `blocking_per_role.conductor: 606 -> 630 | new rows naming it: 24`;
  `safety: 72 -> 76 | new rows naming it: 4`; `7g added 29 removed 0 changed 0 spec 29 added==spec True`;
  `blocking_per_role.conductor: 630 -> 659 | 29`; `safety: 76 -> 79 | 3`; `overrides added: []` in both commits; `about same: True`.
- `ord.py`: `local misorder of new rows: []`, inversions 21/21 for both commits.
- `git diff --numstat`: fixture 25/1 and 30/1, test 8/1 and 9/1. The tuple check: 28 entries, 0 duplicates, no `::` entries.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 (OH8-7g): question_register.py::record_case shape -> xref (the raise at :1196 carries the join :1185, case id must resolve against the story's case ids); no ratchet change",
    "F2 (OH8-7g): person_words.py::_from_file shape -> safety, owner intent (the NUL and strict UTF-8 refusals :100-105 are the twin of read :150-151 which the Lead answered safety/intent; one guard on a person's words, one class); raise ratchet.safety 79 -> 80 named in the commit message"
  ],
  "class_completeness": "Rows 24/24 and 29/29 match spec 3.1; ratchet raises equal new rows per key (k4.py); no existing row changed; byte diff holds only inserted rows and the ratchet line. Inside the pair: record (safety/intent) vs _raise/raise_role_question (xref) share a guard shape; the carrier (a person's word) separates them, so the Lead should restate its answer, no row moves. _from_file vs read: one guard, two classes, fixed by F2. Outside the diff for the Lead queue: existing machine_facts._check lacks the E3 mark on the same catch path; question_stop.defaults is the programming-error arm of E3; record_case has no settled-answer guard (one road with record, H6); new instances for the 6b roles node (question_register.raise_question/_raise, vcs_evidence, s5_plan); argv-option guard in vcs_evidence.readiness is a Lead call. Builder analog via_cmd not confirmed (run_py_entry.py:162 aliases itself); register-read copy is two copies, not three.",
  "trail": {
    "read": [
      "C:/QAFactory/forge-repo/docs/tasks/specs/t-346-oh8-7b-chain-spec.md",
      "C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-411-oh8-7cde-diff-review.md",
      "C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md",
      "git show 097f58d / a238574 commit messages; git diff 3589f5b 097f58d; git diff 097f58d a238574",
      "a238574:ai-packages/qa-factory/scripts/{ticket_light,ticket_adapter,source_inventory,source_exclusions,vcs_evidence,local_keys,onboard_apply,s5_plan,question_register,question_stop,person_words,grammar,assertion_detectors,machine_facts,driver_dispatch,run_py_entry,config_contract}.py at the raise sites and catch paths named in K1/K2",
      "a238574:ai-packages/qa-factory/agents/qa-scout.md:70, agents/qa-automator.md:68, references/role-commands.json",
      "fixtures judgment-census.json at 3589f5b, 097f58d, a238574"
    ],
    "reruns": [
      {"command": "python -B <scratchpad>/g/ai-packages/qa-factory/scripts/tests/test_judgment_census.py (byte copy of a238574)", "result": "=== judgment_census: 26/26 ok === exit 0; safety=79 conductor=659 subclass_pending=21 (ceiling 21)"},
      {"command": "python -B -I <scratchpad>/tools/k4.py <scratchpad>", "result": "7f added 24 removed 0 changed 0 added==spec True; conductor 606->630 (24); safety 72->76 (4); 7g added 29 removed 0 changed 0 added==spec True; conductor 630->659 (29); safety 76->79 (3); overrides added none"},
      {"command": "python -B -I <scratchpad>/tools/ord.py <scratchpad>", "result": "local misorder of new rows: [] for both commits; inversions 21/21"},
      {"command": "python -B -I <scratchpad>/tools/sites.py <byte copy> <15 files>", "result": "raise-site lines per function as cited in K1"},
      {"command": "git -C <wt> diff --numstat 3589f5b 097f58d; git -C <wt> diff --numstat 097f58d a238574", "result": "fixture 25/1 and 30/1 (the one deletion is the ratchet line), test 8/1 and 9/1"}
    ]
  }
}
```
