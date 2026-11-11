# t-1986 — the analyst walks every suspicious unconfirmed place and finds out the truth — SPEC AMENDMENT (designer draft)

Status: **draft for the Lead's acceptance** (designer, 05.11.2026). Amends `docs/tasks/specs/t-1957-fast-manual-walker.md` (not edited
here): node N6 of its Slice 3 is REPLACED by this batch, built right after Slice 1 (N1a, N2, N3, N4, N5s) and before Slice 2.
Package under change: worktree `D:/ws1/wt-fbfix` (below `PKG\` = `D:/ws1/wt-fbfix\ai-packages\qa-factory`). Every file:line in §2
was read in that tree on 05.11.2026; anything not read is marked **estimate** or **could not establish**. No compatibility with stories,
plans or evidence of an older package version (owner's decision, t-1957 status block): temporal edges cover only one run on the new version.

Owner's word (05.11.2026 ≈21:40, `experiments/mybooks/thinking-roles/thinking-roles.md:177`): «Вот ты сейчас проверил 24 подозрительных места и
сказал как обстоят дела на самом деле. Вот так и аналитик должен проходить все подозрительные неподтверждённые места и выяснять правду. С одного
прогона их будет не 26, а всего 3-5».

---

## §1 Goal, AR-n / FR touched, owner and census class of every check

**Goal.** At S7 the failure analyst owes, for every suspicious unconfirmed place of the run, a WALKED answer — `bug` / `not_a_bug` /
`requirement_silent` (a question for the product owner, never a bug) / `impossible` (with why) — that cites evidence the walker recorded and
names the SOURCE of its expectation (a register requirement `R-n`, a person-settled question, or `none: derived`). Code assembles the list of
places from records that already exist (data), carries the answers to the readers that already exist (bug drafts' confirmation step, the
findings register, the report, gate B), and turns every place nobody settled into a named gap — it never decides which answer is right.

| AR | how touched | change check in the DoD of node |
|---|---|---|
| AR-2 open variety is the role's | what is suspicious beyond the joined records, which places to walk first, how many steps per call, which answer — the analyst's | U1: no phrase list, no reading of any wording; `test_places_is_a_join_only` |
| AR-7 / AR-29 code = instrument, role = judgment | `settle.py` checks keys and cross-references of an answer, never its truth; the analyst's answer is accepted by the S8 scribe (X7-6b consumer) | census rows below; U1 `test_answer_never_judged_by_words` |
| AR-10 a check's requirement reaches the role first | the answer keys and the refusal reasons are in the triage brief lines and `settle.py --help` before the walk | U3 `test_brief_names_places_and_answer_keys` |
| AR-11 only the context the work needs | analyst charter cuts (§3.5); the walk brief lines replace no injection | U4: `role_load.py --role qa-failure-analyst` not above its rows |
| AR-13 / AR-15 one reader, one survivor | ONE join `settle.places`; drafts' step read only through `bug_records.confirmation_of`; register through `contract.register_rows`; unconfirmed R through `contract.unconfirmed_requirements`; investigation targets through `investigation.open_targets`; quotes through `manual_evidence._quote_in`; the walk through t-1957's `walk_session.py` | U1, U2, U3 |
| AR-14 one artifact, one writer | `evidence/settle-<place>.json` writer `settle.py` (from the role's answer file); register lines only through `exploratory_findings.append`; drafts stay the analyst's files | U1, `artifact-writers.json` row |
| AR-20 shrink-only ratchets | `blocking_per_role.qa-failure-analyst` +1 (ONE named raise: `settle.py::_refuse`); analyst `role-load.json` rows do not grow | U1, U4 |
| AR-21 / AR-22 producer and reader together | settle record -> `bug_records.reproduction_problems` (kind `walk`) -> report / gate B; settle record -> register line -> `report_facts` (:356) ; `settle.places` -> triage brief + `close_unsettled` | U1, U2, U3 |
| AR-23 empty outcome declared | a run with no place: one brief line "Places to settle: none" and no gap; a place list that cannot be computed is one printed line + a brief line, never "none" | U1, U3 |
| AR-25 every state a way out | place states `open` -> `settled` (answer record) or `gap` (code line at the close); a conflict (draft stands against a `not_a_bug` answer) is `open` with its why | U1 |
| AR-26 requirements are the unit | the expectation source of an answer is a register `R-n` or a settled question; `none: derived` can never be `bug` | U1 (fork F-D) |
| AR-27 a finding reaches the report under its owner | `requirement_silent` -> `unresolved_question` line (owner: the person who decides the story's expected behaviour); unsettled -> `coverage_gap` line | U1 |
| AR-28 / FR-59 unknown never a pass | an unreadable source makes the place list "could not be computed", never empty; an unchecked walk receipt reads `unconfirmed` | U1, U2 |
| AR-19 stage twins | the skill road `phases/s7.md` names the same list, answer and close step as the driver | U4 |

FR touched: FR-1, FR-2 (every refusal of `settle.py` names its door), FR-10 (a draft standing against its own walked answer is shown as a
conflict), FR-12, FR-13 (the answer words and the sources are data), FR-18 (a walk is evidence of THIS place only), FR-21/FR-22 (a `bug`
answer has its road: the draft's step), FR-23 (`impossible` is a recordable null outcome), FR-38, FR-41, FR-47, FR-48 (P22: settle first,
then ask), FR-58 (code is never the oracle; `none: derived` is never a bug), FR-33 (§4 live proof). Principles: P20, P22, P26, P27, P23, P28.

**Checks added or altered: owner served and census class** (class words: `PKG\scripts\tests\test_judgment_census.py:74`; ONE class per function,
`CLASS_ORDER` :60; a unit counts toward `blocking_per_role` only with a refusal site or on the blocking path — t-1957 §1 explains the census rule).

| check (file :: function) | node | added/altered | owner served | class | blocks? | why not a judgment |
|---|---|---|---|---|---|---|
| `settle.py :: answer_problems` (the answer word is one of `references/settle.json` `answers`; `expectation.source` is `requirement` with an `R-n` that `contract.register_rows` holds, or `question` with an id `branch_accounting._confirmed` holds settled, or `none`; for `bug`: source not `none` and (fork F-D) the R not in `contract.unconfirmed_requirements`; `seen.capture` is a capture row of an attempt of THIS place's walk; `seen.quote` stands in it (`manual_evidence._quote_in`); `impossible` has `why`; `not_a_bug` has `quote`) | U1 | added | data | xref | no (returns a list) | membership, joins to the register / question register / capture index, quoted bytes found; never reads what the words mean |
| `settle.py :: _refuse` (the ONE raise of `settle.py write`) | U1 | added | data | shape | **yes** — `blocking_per_role.qa-failure-analyst` 131 (`judgment-census.json:4`) -> 132, the ONE named raise | formats and raises what `answer_problems` returns |
| `settle.py :: places` (the join, §3.1) | U1 | added | data | — (no unit: name outside `UNIT_NAME_RE` :58, no refusal site) | no | joins existing records by their existing state words |
| `settle.py :: unsettled` (a place with no valid answer, or whose answer conflicts with a standing draft) | U1 | added | data | — (no unit) | no | presence and a join; the conflict is two of the role's own records disagreeing (FR-10), not a verdict |
| `bug_records.py :: reproduction_problems` (new kind `walk`: the entry's `evidence` is a settle record that names THIS draft as its place and says `bug`) | U2 | altered | data | xref (unchanged, census `:58`) | unchanged (returns a list) | a join of the receipt to the draft; error direction DOWN (§3.3) |

**Ratchet verdict (AR-20), for the Lead:** ONE raise, `blocking_per_role.qa-failure-analyst` 131 -> 132 (`settle.py::_refuse`, roles
`["qa-failure-analyst"]`, because only the analyst calls `settle.py write`). No honest offset: nothing the analyst calls today goes away.
If the Lead prefers `["conductor"]` by the recorder convention (t-1957 §1), the raise moves to `conductor` (466 + Slice 1's +1) — fork F-H.

---

## §2 Facts (file:line, read in `wt-fbfix` on 05.11.2026)

### What the run already lists (inputs)
- **S1. Red tests, failing/inconclusive manual checks, observations and recorder surprise lines are ALREADY one list:** `contract.triage_targets`
  (`PKG\scripts\contract.py:4398-4494`) is "THE ONE definition of a failure that needs triage": failed/error results (:4441-4457), manual checks
  `fail`/`inconclusive`/unprepared (:4458-4493), one `<case>#obs<n>` per observation whatever the check's result (:4469-4478) and one
  `<case>#sur-<id>` per surprise line no observation cites, capped at `surprise.max_per_attempt` = 30 (`manual-capture-steps.json:65`) plus one
  `#sur-overflow` (:4473-4476). `triage_failures` (:4497-4555) turns them into `(kind, name)` keys bound by `bind_triage`. Producer of the
  `surprises[]` field: `manual_evidence._surprise_fields` (`manual_evidence.py:350-359`) over `surprises_of` (:295-305, "the ONE reader of the
  lines"); producer of the lines: `manual_capture` (`Attempt.surprise` :1104; the per-call file :3240). Reader: the analyst's triage (driver
  `stage_S7` -> `failures_to_triage`, `story_run.py:12375`). A failure without a triage row keeps S7 open (`s7_unbound` :12617-12627).
- **S2. What the run left OPEN is a second list:** `investigation.investigation_targets` (`PKG\scripts\investigation.py:130-217`): (a) the
  `inconclusive` / `manual_skipped` rows of `manual_observations` in accepted S6 forms (:161-179), (b) pinned cases whose `request.json` holds
  `refused` with an open expectation gap (:181-216). Resolution `unresolved_targets` (:371-424): a role line with `probe.runs >= 1` or a role
  `coverage_gap` or withdrawal, or a triage verdict of `investigation-budget.json` `resolving_verdicts` (`references/investigation-budget.json:8`)
  with an evidence file. `open_targets` (:460-463) is the one entry. Readers: `story_run.s7_investigation_gate` (:12840-12905), `s7_open_work`
  (:12586-12606), `investigation_lines` (:12907-12964), `investigation_probe._targets` (`investigation_probe.py:327`).
- **S3. That pass is read-only and forbids comparing with an expectation:** the brief line "Record what the product does; never compare it with
  an expected value; never write a bug or a triage row; only `investigation_probe.py` reaches the stand" (`story_run.py:12954-12955`); methods
  `GET, HEAD, OPTIONS` (`investigation-budget.json:4`); ONE pass per S7 chain (`investigation.decision` :538-558; `s7.md:256-261`); it runs only
  at the three code closers (`story_run.py:12379, :12410, :12806`).
- **S4. Bug drafts and their step:** every draft carries `confirmation: unconfirmed` (`s7.md:202-204`); the step `reproduced_by_factory` is
  DERIVED by code from typed `reproduction` receipts, the one reader `bug_records.confirmation_of` (`bug_records.py:868-906`); kinds
  `contract.BUG_REPRODUCTION_KINDS = ("fresh_data_rerun", "own_script")` (`contract.py:1827`); `reproduction_problems` (`bug_records.py:756-828`)
  voids EVERY entry unless the draft's triage row says APP_BUG (:776-777) and the instance's CURRENT result is red (:778-790). Consequences
  (read from the code, not run): a code-reading draft has no `triage_ref` (`contract.py:1878-1881`) and so can never reach the step today
  (R_NO_TRIAGE); a draft resting on an observation target `<case>#obs<n>` has no current result row of that name, so the step is void
  (R_NO_CURRENT) — **derived from the code, not run**. Code-reading drafts: `evidence: "code-reading"`, `check_state` `not_executed|unverifiable`
  (`contract.py:1881-1882`), checker `bug_records.code_reading_problems` (:638-686). Reader of the sentence for a person:
  `bug_records.reproduction_words` (:913-931) — "unconfirmed — nobody has reproduced it; it counts toward nothing".
- **S5. Arm B rerun (05.11.2026):** 7 unconfirmed P2 drafts, all code-reading, class "call error not shown", R-12/13/14
  (`thinking-roles.md:103`); S7 investigation sent 0 probes (`thinking-roles.md:140`, t-1954 :66); S7 triage $0.85 on 20 cases with no stand
  call (`thinking-roles.md:140`).
- **S6. Register contradictions:** `contract.register_rows` (`contract.py:1173-1204`) is THE reader of the register and of the `code_says`
  column (`meets: <fact>` | `contradicts: <fact>` | `unknown`, `contract.py:1883-1885`). R ids whose expectation no source confirms:
  `contract.unconfirmed_requirements` (:1415-1425; implementation-only claims nobody confirmed plus code- or test-sourced rows; errs toward
  "not confirmed"). The lesson of the plain-agent check: 9 «bugs» moved to «decide by the product owner» because the expectation was
  derived by the factory (`experiments/mybooks/disputed-check-plain-agent/SUMMARY.md:5, :20-28`); the owner dropped two more (:80-86).
- **S7. Triage verdict words** `contract.TRIAGE_VERDICTS` (`contract.py:2094-2122`) have NO word for "the requirement is silent, a person must
  say" on a red or an observation except `ASSERT_STRICTER` (a red test, control experiment required, `triage_control_problems` :2151-2214) —
  for an observation the charter says "else a question" (`agents\qa-failure-analyst.md:56`). **Could not establish** where such a question is
  recorded by the triage dispatch (a Grep for `S7|qa-failure-analyst` in `question_register.py` found nothing; positive control: the same tool
  found `def confirmation_of` in `bug_records.py`).
- **S8. The findings register** `exploratory_findings` (`PKG\scripts\exploratory_findings.py:36-46`): kinds `observation | unresolved_question |
  coverage_gap`, statuses `unverified | reproduced | not_reproduced | environment_event`, oracles incl. `owner_question`; it EXCLUDES `bug`,
  `triage_ref`, `confirmation` (:55); one writer `append` (:277); read by the report (`report_facts.py:356-361`).
- **S9. Control experiment record:** `control` block on a triage row, results `effect_without_change | no_effect_without_change | impossible`
  (`contract.py:2133`), evidence a file under `evidence/` (`:2197-2207`). **Could not establish** from the read lines whether `evidence/` there
  resolves against the task root or `work/` (the investigation reader passes `task / "work"`, `investigation.py:409`; the triage validator
  passes the caller's task root, `validate_artifacts.py:2363`); U0 pins it by calling `contract.evidence_ref_issue` with the same root the
  reader uses, not by assuming.

### Negative findings (each with its search and a positive control)
- **N1. No function joins drafts, triage targets, investigation targets and register contradictions into one "places to settle" list.** Grep
  (case-insensitive) `def [a-z_]*(place|settle|unconfirmed)[a-z_]*\(` over `PKG\scripts\*.py` found only unrelated names
  (`user_path_failures._register_places` :235, `ledger.unconfirmed_bindings` :128, `contract.unconfirmed_requirements` :1415, ...);
  `def [a-z_]*(targets|confirmation)[a-z_]*\(` found the two lists above (`investigation.py:130, :371, :460`) and `bug_records.confirmation_of`
  :868 — positive control of the same form. So the list must be assembled, by ONE new function (§3.1).
- **N2. The cut phrases of §3.5 are pinned by no test.** Grep for "a case's manifest slice|`env_probe.py` - the stand|Reproduce through an
  independent route|Your own request against the same shape" over `PKG` -> only `agents\qa-failure-analyst.md`; Grep for "the value was never
  received" -> the charter and `test_case_role_twins.py`, whose only pin (:65) is the Tools sentence "a field_absent row is judged by its
  shape_ref, not by the control experiment" (kept). Positive control: "the same action without the change under test" is found in
  `test_charters_s5_s9.py` and `test_s7_control_experiment_texts.py`.
- **N3. Slow or fast:** `test_bug_records.py`, `test_investigation.py`, `test_investigation_probe.py`, `test_story_run_s7.py` ARE in
  `PKG\scripts\slow_tests.json` (:19, :72, :73, :163) — CI only; `test_charters_s5_s9.py`, `test_case_role_twins.py` are not (same Grep).

### The analyst today
- **S10.** Charter `agents\qa-failure-analyst.md` (85 lines): craft sections "Where bugs hide" (:31-43) and "Techniques" (:46-57); Tools (:60-72)
  names `manifest_view.py` and `env_probe.py` (:66); "Reproduce through an independent route" (:53); "Settle it yourself first" (:81). Pins:
  `test_charters_s5_s9.py` KEYS (:58-59), phrases kept (:229-237), form tokens that must stay in Tools and out of Techniques (:252-253, incl.
  "`evidence/`" and "`TEST_BUG`"), craft share ≥ 0.40 (:50, :141-148), no `P<n>`, no `AC`, no "must run"/"Step N" (:73-76, :124-127).
- **S11.** Role-load ratchets (`references/role-load.json`): analyst total 17 753 (:19), process 16 145 (:33), slack 1 000 (:9). The live value
  was NOT measured by this designer (no shell run) — U4 measures it first.
- **S12.** S7 dispatch shape: `stage_S7` (`story_run.py:12349-12440`) runs ONE triage `run_role` (:12433-12436) with `told` lines; repairs in
  `s7_repairs`; the close `s7_close` (:12800-12838) calls `s7_investigation_gate` FIRST (:12806), then `s7_await_scribe` (:12813; the S8 scribe
  accepts S7, X7-6b). Walker: t-1957 Slice 1 (`walk_session.py`, N1a/N2) — **not on the branch yet**; t-1957 F38: a server opened from a role's
  Bash surviving the tool call is UNMEASURED.

---

## §3 Design

### 3.1 The places — ONE join, data only (U1)

`settle.places(task_root) -> {"places": [place], "unreadable": [(record, why)]}`; a place is `{id, sources, refs, title, expectation_hint}`:

| source | id | from (the existing reader) | joined when |
|---|---|---|---|
| `draft` | `draft-<file stem>` | `bug_records.draft_paths` + `bug_records.confirmation_of(...)[0]` | the derived word is `unconfirmed` (incl. every code-reading draft, S4) |
| `open` | the investigation target id (`case-<C>` / `obs-<d>-<i>`) | `investigation.open_targets(task, budget)["unresolved"]` | listed there (S2) |
| `register` | `req-<R>` | `contract.register_rows` | `code_says` starts with `contradicts:` AND no draft names that R (`contract.REQ_ID_RE` over the draft's `violates`) |

`refs` carry what the walker needs to find the place: for a draft its `triage_ref`, `violates`, `manual_steps`, `red_test`, `fact`; for an
`open` target its `then`, `observed` (verbatim), `evidence`; for a register row its requirement text and fact id. `expectation_hint` is the
requirement id the record ALREADY names (draft `violates`, target `requirements`, register `r`) — a hint, never the answer's source (the role
names the source). Red tests, observations and surprise lines enter through these sources: an `APP_BUG` red / observation / surprise has a
draft (source `draft`); what the runner left open is source `open`; everything the analyst judged with evidence (`NO_DEFECT` with a quote
that stands in the recorded line, `TEST_BUG`, `FLAKY` with three reruns, `ASSERT_STRICTER` with its control) is NOT a place — owner question
Q1 (§5) asks whether `NO_DEFECT` judgments by reading should be walked too. Nothing else is in code: no list of words, no kinds of
suspicion (AR-2); the analyst may walk any other place it judges suspicious and record it the same way (`settle.py write --place new-<slug>`).

EMPTY outcome (AR-23): no place -> `{"places": [], "unreadable": []}`, the brief line "Places to settle: none in this run". A source that
cannot be read (draft folder, register, investigation budget) -> `unreadable` with why; the brief says "the list of places could not be
computed whole: <why>" and never "none" (AR-28). Two sources naming the same place (an `open` target whose case has a draft) -> ONE place with
both sources (the draft id wins as the id; the target id is kept in `refs.target`).

### 3.2 The answer — the role's, carried by code (U1)

The analyst writes `work/settle/<place id>.answer.json` (its scratch) and runs `settle.py write --task-root T --place <id> --file <f>`:

```
{"place": "draft-BUG-3", "answer": "bug|not_a_bug|requirement_silent|impossible",
 "expectation": {"source": "requirement|question|none", "id": "R-12|Q7|", "quote": "<the requirement / the person's words, verbatim>"},
 "seen": {"quote": "<words the walk captured>", "capture": "<path of the capture>"},
 "walk": "<walk id>", "why": "<impossible: what the stand lacks | not_a_bug: why, with the quote>"}
```

`answer_problems` (§1) refuses through `_refuse` (exit 2, every line names its door). Written: `evidence/settle-<place id>.json` (the answer
plus `written_at`, `walk` record path, capture sha256), atomically, ONE file per place; a second `write` for the same place REPLACES it only
with `--replace` (the role's correction; the old file's sha is kept as `replaces`). Downstream, by answer:

| answer | carried to | by whom |
|---|---|---|
| `bug` | the draft's `reproduction` gets `{kind: "walk", evidence: "evidence/settle-<id>.json", observed}` — the ANALYST writes it into its own draft (AR-14); `confirmation_of` derives `reproduced_by_factory` (U2); report / gate B sentence "reproduced by the factory — the analyst walked it on the stand; no person has confirmed it yet" | role writes, code derives |
| `not_a_bug` | the analyst withdraws the draft (deletes the draft file) and, when a triage row rests on it, changes the row as its words allow (`NO_DEFECT` on an observation; `TEST_BUG`/`ASSERT_STRICTER` on a red with their own evidence); a draft that still stands -> `unsettled` conflict (§3.4) | role |
| `requirement_silent` | `settle.py write` appends ONE register line through `exploratory_findings.append` (`kind: unresolved_question`, `oracle_status: owner_question`, `statement` = `seen.quote`, `why_not_a_bug` = "the requirements are silent on this; the product owner decides", `evidence_refs` = the settle record, `origin.target` = place id, `by` = the analyst's dispatch id) -> report and gate B (S8); a draft that still stands -> conflict (never a bug, P20) | code carries the role's answer |
| `impossible` | the same writer, `kind: coverage_gap`, `missing_prerequisite` = `why` -> report as a gap | code carries |

Expectation `none` is legal for `not_a_bug`, `requirement_silent`, `impossible` and refused for `bug` (FR-58: a bug needs a requirement or a
person's settled words). Fork F-D: whether a `bug` resting on an R listed by `contract.unconfirmed_requirements` is refused (recommended) or
only flagged.

### 3.3 The walk receipt in the bug's step (U2)

`contract.BUG_REPRODUCTION_KINDS` += `"walk"` (and `handoffs/vocabulary.yaml` mirror). In `bug_records.reproduction_problems` an entry of
kind `walk` is judged by `_walk_receipt_problem(task, draft_name, entry)`: the evidence is `evidence/settle-<id>.json`, readable, its `place`
is THIS draft's place id (`draft-<stem>`), its `answer` is `bug`, its `seen.capture` still exists with the recorded sha256. POSITION: the two
draft-wide facts (APP_BUG triage row :776-777, current result red :778-790) are NOT asked of a draft whose ONLY entries are `walk` receipts
(a code-reading draft has no triage row; an observation draft has no current result row); they stay asked of every other entry kind.
INVARIANT: a `fresh_data_rerun` / `own_script` entry is judged exactly as today; a walk receipt never lifts a draft other than the one its
place names, never one whose walk said anything but `bug`, never on a capture whose bytes changed. ERROR DIRECTION (a reused function in a
more consequential role: the step now also rests on a role's walk): may leave a draft `unconfirmed` that a walk did show (cost: the report
says "unconfirmed" — the safe side); never lifts one without a settle record that passed `answer_problems`. Adversarial inputs that must stay
`unconfirmed`: a receipt naming another draft's settle file; a settle file whose `answer` is `requirement_silent`; a settle file edited after
`write` (sha mismatch on its capture); a receipt whose evidence is outside `evidence/`; a `walk` entry beside a `fresh_data_rerun` whose
attempt is not red (the rerun entry is void, the walk entry stands on its own).

### 3.4 What happens to a place nobody settled (U1, U3)

`settle.unsettled(task_root)` = the places with no valid settle record, plus the places whose record conflicts with a standing record of the
role: a draft that still stands while its answer is `not_a_bug` or `requirement_silent`, or an `open` target whose register chain the role
withdrew while a `bug` answer stands. Code never decides that a place is settled by its verdict word (AR-29): presence of a valid answer
record is the ONLY settling fact.

Who is told (no code closes the role's obligation, no stop of the factory):
1. **The analyst, before the work** — the triage brief lists every place (§3.6) and says the answer is owed; `settle.py list --task-root T`
   prints the same list with each place's state (`open` / `settled: <answer>` / `conflict: <why>`).
2. **The report and gate B, as a gap** — at the S7 close, BEFORE the investigation gate (§3.6 POSITION), `settle.close_unsettled(task, why)`
   writes for each unsettled place of source `draft` or `register` ONE register line `kind: coverage_gap`, `title` = the place's title,
   `missing_prerequisite` = "not walked by the analyst — <why>", `why_not_a_bug` = "a suspicion nobody has checked on the stand; it is
   neither a bug nor cleared", `evidence_refs` = the draft / register file, `by` = `code:settle.close_unsettled`; a draft stays as it is and
   its sentence stays "unconfirmed — nobody has reproduced it" (S4) beside the gap. Places of source `open` keep their EXISTING road
   (`s7_investigation_gate` -> pass or `close_gaps`, S2-S3): INVARIANT — one place, one gap line (no double gap). `why` is one of
   `references/settle.json` `gap_reasons` (data): "the analyst's dispatch ended before this place", "the stand could not be reached",
   "the walk session could not be opened".
3. **The tier above** — the S8 scribe, who accepts S7 (`s7_await_scribe`, S12), gets one brief line "Places the analyst did not settle: <n>
   (<ids>)" from `settle.unsettled`; returning the triage for them is the scribe's judgment (X7-6b rework road), never code's.
P22: a place the analyst cannot settle because only a person knows (the requirement is silent) is ANSWERED `requirement_silent`, not left —
the conductor is not called for it; it reaches the person at gate B through the register.

### 3.5 The charter — experience, not procedure (U4)

Proposed text (package English; no principle numbers, no `AC`, no "must run"/"Step"; no form token in Techniques):

In "Where bugs hide", after "A green manual check that carries an oddity" (:43), ADD (≈ 260 B):
> - **A suspicion left as the run left it.** A bug drafted from reading, a doubt the runner wrote down, a code place that contradicts a requirement: each stays a guess until someone does the thing on the stand. Most guesses either fall apart or turn out to rest on an expectation nobody stated.

In "Techniques", REPLACE "**Reproduce through an independent route.** Your own request against the same shape, not the test's own output." (:53) WITH (≈ 620 B):
> - **Find out the truth on the page.** Every suspicious place nobody has confirmed is walked before you leave it: do the thing a person would do, one step or a short obvious run at a time, look, decide the next. Through an independent route: your own steps, never the test's own output. Then say which it is: a bug, with the requirement it breaks; not a bug, with the words you saw; or a place the requirements are silent on, which is a question for the product owner and never a bug. Name where your expectation comes from beside the answer; an expectation the factory derived itself is no requirement. A place the stand cannot show is said so, with why.

In "Techniques" (:55), DELETE the sentence "A red with no field is different: the value was never received, so it is judged by the response
shape, not by the control experiment." (≈ 150 B; its rule stays in Tools :71, pinned by `test_case_role_twins.py:65`).
In "Tools" (:66), DELETE "`manifest_view.py` - a case's manifest slice; `env_probe.py` - the stand." (≈ 80 B) and ADD (≈ 170 B):
> - `settle.py list|write` - the places to settle and your answer per place (keys on your key page); `walk_session.py step|look|final` - the walk session your brief names.

Net ≈ +700 B ≈ +175 tokens on the total (craft +≈ 600 B, process +≈ 90 B) — **estimate**. It is paid only if the live load sits ≥ 175 tokens
under 17 753 (S11, not measured); otherwise U4 STOPS and reports (no raise, E4.1). Further cut offered (fork F-I, not taken by default):
the "When to ask" bullet "Settle it yourself first: ... a control experiment." (:81, ≈ 170 B) is covered by the new technique. Pins checked
(N2). Craft share rises (craft grows, process shrinks).

### 3.6 The driver (U3) and the walk session (U0)

- **Session:** the S7 driver opens ONE walk session `walk_session.py open --task-root T --walk <triage dispatch id> --place settle --items
  <place ids | "free">` BEFORE the triage `run_role` (`stage_S7`, after the dispatch is registered and only when the stand lease can be taken),
  as t-1957 N5s does for S6, and closes it in a `finally` after `run_role` returns (fresh, reused, crashed). Fork F-E: driver-opened
  (recommended; works whether or not a server opened from the role's Bash survives — F38) vs role-opened. A session that cannot open ->
  the brief says "no walk session: <why>; answer `impossible` with that why for places that need the page, or use `run_suite.py --request` /
  HTTP where the place is an API one" (FR-57: a door, never a lock).
- **Evidence roots:** place `settle` items open attempts under `evidence/settle-<place id>/aN/` and place `control` under
  `evidence/control-<label>/aN/` (N6's convention, S9), so every capture a settle record cites is a file the RUN wrote under `evidence/`.
- **Brief lines** (`Driver.s7_settle_lines`, appended to `told`): "Places to settle (<n>): one line per place `<id> | <sources> | <title> |
  expectation named by the record: <hint or none> | where: <refs>`"; the four answers and the expectation-source rule in one line; the walk
  line "walk one step or a short obvious run per call, look, decide (references/walk-charter.md, how many steps per call)"; the commands
  `settle.py list|write`, `walk_session.py step|look|final`. A list that could not be computed -> the line says so (§3.1).
- **POSITION at the close:** in `s7_close` and the code closer `s7.pretriaged`, `settle.close_unsettled` runs BEFORE `s7_investigation_gate`.
  INVARIANT: the investigation pass and `close_gaps` see the register with the settle lines already in it, so a place is never both a settle
  gap and an investigation gap, and `finalize_task` / the scribe read a register in which every place is settled or gapped. At `s7.no_failures`
  (no analyst ran) the places of source `register` get their gap with "the analyst was not dispatched: no failure to triage" — fork F-F.
- **Shared hot files:** `story_run.py` (`stage_S7`, `s7_close`, new `s7_settle_lines`, `s7_settle_session`; nothing else), `walk_session.py`
  (`_place_roots` only, after t-1957 N1a and N2).

### 3.7 Expected numbers (estimates)

Per place: §3.10 (2) of t-1957 — ≈ 3–6 min, ≈ 12–20 tool calls, ≈ 6–10 recorder calls (steps found on the page, one step per call) — **estimate**.
Places per run: the owner says 3–5; arm B would have had 7 (the 7 code-reading drafts, S5) plus the open targets — **estimate**. S7 triage
grows by ≈ 10–30 min per run (3–5 places) and ≈ $0.4–1.5 (t-1957 §3.10 control row ≤ $0.40 per place) — **estimate**; measured by
`walk_timing.py --task T --summary` grouped by place `settle` (t-1957 N2).

---

## §4 Nodes (written for a weaker model; direction chosen; forks of §6 taken at their recommendation until the Lead answers)

General: fast test files only (N3); slow files are CI's. Witnesses run from `D:/ws1/wt-fbfix`. Every package commit carries
`architecture:` and `judgment:` lines; `python -B ai-packages/qa-factory/scripts/selftest.py --lang` in each witness (FR-30). Hot-file
functions are named; nothing else in that file is touched. Order: t-1957 Slice 1 merged -> S0 (any time) -> U0 ‖ U1 ‖ U4 -> U2 (after U1) ->
U3 (after U0, U1). Shared: `artifact-writers.json` U0 then U1; `judgment-census.json` U1 only; `contract.py` U2 only; `walk_session.py` U0 only.

#### S0 — pre-measurement (Lead, environment run; t-1957 F38) — informational, gates nothing under F-E (a)
In a stand COPY, one live S7 analyst dispatch runs `walk_session.py open ... --place settle` from its Bash and a `status` in its next call
and after the session ends. Written to `experiments/mybooks/thinking-roles/walker-call-overhead.md` (section "server from a role's Bash"):
survives the tool call yes/no, survives the session end yes/no. If F-E (b) is chosen, U3 waits for "yes, yes".

#### U0 — place roots of the walk session (`settle`, `control`)
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_session.py` (`_place_roots` new; `open` takes `--place case|settle|control`, default `case`; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\artifact-writers.json` (keys `evidence/settle-*/` and `evidence/control-*` (dir + `.json`) writer `walk_session.py`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_places.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1986-u0.md` (new)
**non-goals:** step calls, verdicts, records of S6 cases (t-1957); the settle record itself (U1).
**behaviour:** `case` -> `work/evidence/manual/<case>/aN/` (t-1957 unchanged); `settle` -> `evidence/settle-<item>/aN/`; `control` ->
`evidence/control-<item>/aN/`, where `evidence/` is resolved exactly as `contract.evidence_ref_issue(..., under="evidence")` resolves it for
its callers (S9: the test asserts the path passes that function with the root `triage_control_problems` receives — never an assumed root).
**edges:** E0.1 an item id with `/`, `..` or a drive -> refused through `_refuse` naming the allowed form `[A-Za-z0-9._-]+`. INVARIANT: an
attempt never lands outside its root. E0.2 TEMPORAL: `evidence/settle-<id>/` absent before the first `item`, created by it; a second open
of the same item -> next `aN` (t-1957 E1.9). INVARIANT: evidence on disk is never rewritten. E0.3 `--place` unknown -> refused, door lists the
three. **DoD — `test_walk_places.py`:** `test_case_root_unchanged`, `test_settle_root_under_evidence_passes_evidence_ref_issue`,
`test_control_root_under_evidence_passes_triage_control_problems` (a `control` block citing a capture of this root -> `[]`),
`test_item_id_escape_refused`, `test_unknown_place_refused`, `test_next_attempt_on_reopen`. Negative control: with `settle` rooted under
`work/evidence/manual/`, `test_settle_root_under_evidence_passes_evidence_ref_issue` fails (shown red once).
Witness: `python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_places.py ai-packages/qa-factory/scripts/tests/test_walk_session.py ai-packages/qa-factory/scripts/tests/test_triage_control.py ai-packages/qa-factory/scripts/tests/test_artifact_writers.py -q`
`architecture:` AR-4, AR-14, AR-21.

#### U1 — `settle.py`: the places, the answer, the unsettled, the gaps
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\settle.py` (new: `places`, `answer_problems`, `_refuse`, `write`, `unsettled`, `close_unsettled`, CLI `list|write`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\settle.json` (new: `answers` [bug, not_a_bug, requirement_silent, impossible], `sources` [requirement, question, none], `gap_reasons` (the three texts of §3.4), `answer_root` "evidence/settle-", a `note` saying why each list is closed)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\artifact-writers.json` (key `evidence/settle-*.json` writer `settle.py` — after U0)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\role-commands.json` (rows `settle.py list`, `settle.py write`, roles qa-failure-analyst)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\handoffs\` the analyst's key page (the file `inject-map.json` names for qa-failure-analyst's keys — the builder reads `inject-map.json` and adds the settle answer keys there; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows `settle.py::answer_problems` xref non-blocking, `settle.py::_refuse` shape blocking, roles `["qa-failure-analyst"]`, owner data; `blocking_per_role.qa-failure-analyst` 131 -> 132)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_settle.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1986-u1.md` (new)
**non-goals:** the walk (t-1957); the draft's step (U2); the driver (U3); `investigation.py` (read only through `open_targets`); any list of
what is suspicious beyond §3.1's three sources; judging whether an answer is true.
**behaviour:** §3.1, §3.2, §3.4 exactly. Readers reused, never re-implemented: `bug_records.draft_paths`, `bug_records.confirmation_of`
(with `bug_records.step_facts` read once), `investigation.load_budget` + `open_targets`, `contract.register_rows`, `contract.REQ_ID_RE`,
`contract.unconfirmed_requirements` (with `question_register.load`), `branch_accounting._confirmed`, `manual_evidence._quote_in`,
`contract.evidence_ref_issue`, `exploratory_findings.append`. `write` order: `answer_problems` -> `_refuse` on any -> atomic write of the
settle record -> the register line for `requirement_silent` / `impossible` (a register that is not installed -> the record stands and the
CLI prints "the findings register is not installed; the answer is kept in <path>", exit 0 — P1).
**edges (each with its invariant):**
- E1.1 EMPTY: no place -> `places == []`, `list` prints "Places to settle: none in this run". INVARIANT: "none" is printed only when every
  source was read.
- E1.2 a source unreadable (draft JSON broken, register without `Requirement` column — `register_rows` raises, investigation budget broken)
  -> `unreadable` names it; `list` prints "could not be computed whole". INVARIANT: an unknown never reads as "no place" (AR-28).
- E1.3 two sources, one place (an `open` target whose case has an `unconfirmed` draft) -> one place, both sources, id `draft-…`. INVARIANT:
  one place, one answer, one gap at most.
- E1.4 a draft whose `confirmation_of` word is `reproduced_by_factory` / `confirmed_by_*` -> not a place. INVARIANT: the step is read only
  through `confirmation_of` (AR-13); a word written by the role without a receipt is `unconfirmed` and IS a place.
- E1.5 `bug` with `expectation.source: none` -> refused: "a bug needs the requirement it breaks or a person's settled words; with neither,
  answer `requirement_silent`". INVARIANT: code is never the oracle (FR-58) — no `bug` stands on a derived expectation.
- E1.6 (fork F-D, recommended): `bug` whose `R-n` is in `contract.unconfirmed_requirements` -> refused with the door "that requirement has no
  confirmed source (derived from code or a test): answer `requirement_silent`, or cite the person's settled question". Error direction: may
  refuse a bug a person in fact confirmed in words the register does not link (cost: the role cites the question); never accepts a bug on an
  R the set lists. Adversarial inputs that stay refused: an R written `r-12`/`R-012` that `REQ_ID_RE` reads as another id (refused as "not in
  the register"); a `question` id that exists but is `open`/`named`/`b` (`_confirmed` false); a quote that is not in the requirement text.
- E1.7 `seen.capture` outside this place's walk attempts, or not in that attempt's capture index, or `seen.quote` not found in it -> refused
  naming the place's attempts. INVARIANT: a receipt measured on other bytes never counts (another place's walk, a file the role wrote).
- E1.8 `impossible` without `why`; `not_a_bug` without `seen.quote` -> refused. INVARIANT: every answer carries its evidence or its reason.
- E1.9 a second `write` for the same place without `--replace` -> refused naming `--replace`; with it -> replaced, `replaces` = old sha.
  INVARIANT: one active answer per place; a change of mind is visible.
- E1.10 place id unknown -> refused, door `settle.py list`; `--place new-<slug>` (the role's own suspicion) is accepted. INVARIANT: the
  role is never locked out of recording a suspicion the join did not list (AR-2).
- E1.11 `unsettled`: a valid record + a standing draft with answer `not_a_bug` or `requirement_silent` -> `conflict` with why.
  INVARIANT: one packet never says "bug" and "not a bug" about one place (FR-10).
- E1.12 `close_unsettled` called twice -> no second line for a place already gapped with the same why (the register chain is read first).
  INVARIANT: one gap line per place; a place of source `open` is never written here (its road is `investigation.close_gaps`).
- E1.13 TEMPORAL (within the run): a place that appears AFTER the triage started (the analyst wrote a draft during the dispatch) is in
  `places` at the next call; `close_unsettled` at the close sees it. INVARIANT: a draft written in the dispatch is never missed by the close.
**DoD — `test_settle.py` (fast; temp task with fixture drafts, register, investigation stub through `open_targets`'s inputs):**
`test_places_is_a_join_only` (the three sources; a fourth record kind present in the folder adds nothing), `test_empty_says_none`,
`test_unreadable_source_never_none`, `test_one_place_two_sources`, `test_reproduced_draft_not_a_place`, `test_role_word_without_receipt_is_a_place`,
`test_bug_without_source_refused`, `test_bug_on_unconfirmed_requirement_refused`, `test_unsettled_question_refused`, `test_capture_of_other_place_refused`,
`test_quote_not_in_capture_refused`, `test_impossible_needs_why`, `test_second_write_needs_replace`, `test_new_place_accepted`,
`test_requirement_silent_writes_one_question_line`, `test_impossible_writes_one_gap_line`, `test_conflict_draft_stands`,
`test_close_unsettled_once_per_place`, `test_close_unsettled_skips_open_targets`, `test_answer_never_judged_by_words` (two answers that differ
only in the words of `why` get the same problem list), `test_every_refusal_names_a_door`.
Negative control: with E1.5's check removed, `test_bug_without_source_refused` fails (shown red once). Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_settle.py ai-packages/qa-factory/scripts/tests/test_artifact_writers.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`
(CI: `test_investigation.py`, `test_bug_records.py`, `test_role_commands.py`). `architecture:` AR-2, AR-13, AR-14, AR-15, AR-20 (raise named),
AR-22, AR-23, AR-25, AR-26, AR-27, AR-28, AR-29.

#### U2 — the walk receipt in the bug's step
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\contract.py` (`BUG_REPRODUCTION_KINDS` only: + `"walk"`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\handoffs\vocabulary.yaml` (the mirror of `BUG_REPRODUCTION_KINDS`, as the existing test holds them equal)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\bug_records.py` (`reproduction_problems`, `_walk_receipt_problem` new, `reproduction_words` (one phrase for kind `walk`: "the analyst walked it on the stand"); nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_receipt.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1986-u2.md` (new)
**non-goals:** `confirmation_of`'s person words; filing; gate B; the settle record's checks (U1 — reused through `settle.answer_problems`?
NO: U2 reads the written record only; it does not re-run U1's checks, it checks the join and the capture sha).
**behaviour:** §3.3 exactly. **edges:** E2.1 POSITIONAL (§3.3): the APP_BUG-row and current-red facts are skipped only when EVERY entry is
`walk`. INVARIANT: every other entry kind is judged byte-for-byte as today (`test_bug_records.py` unchanged, CI). E2.2 a walk receipt whose
settle record says anything but `bug` -> void, code `R_WALK_ANSWER` "the walk did not say bug". E2.3 the record names another place -> void
`R_WALK_PLACE`. E2.4 capture sha changed or file gone -> void `R_WALK_CAPTURE`. E2.5 evidence outside `evidence/` -> existing `R_OUTSIDE`.
INVARIANT for E2.2–E2.5: the error goes DOWN (`unconfirmed`), and the reason is a closed word a person may read (no path, AR-4).
**DoD — `test_walk_receipt.py` (fast):** `test_code_reading_draft_lifted_by_walk`, `test_observation_draft_lifted_by_walk`,
`test_walk_of_other_draft_void`, `test_walk_answer_not_bug_void`, `test_walk_capture_changed_void`, `test_walk_outside_evidence_void`,
`test_rerun_entry_still_needs_red_now` (a `fresh_data_rerun` beside a `walk`: the rerun judged as today), `test_words_name_the_walk`,
`test_kinds_mirror_vocabulary`. Negative control: with the "every entry is walk" condition replaced by "any entry is walk",
`test_rerun_entry_still_needs_red_now` fails. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_receipt.py ai-packages/qa-factory/scripts/tests/test_settle.py -q` (CI:
`test_bug_records.py`). `architecture:` AR-13, AR-22, AR-28, AR-29.

#### U3 — the S7 driver: session, brief lines, the close
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`stage_S7` — the session open before and the `finally` close after the triage `run_role` at :12433, and `told += self.s7_settle_lines()`; `s7_close` — one `settle.close_unsettled` call BEFORE `s7_investigation_gate` (:12806); the `s7.pretriaged` and `s7.no_failures` closers — the same call before their gate (:12410, :12379); `s7_settle_lines` new; `s7_settle_session` new; the scribe's acceptance brief line "Places the analyst did not settle" where `s7_await_scribe` lets the scribe in — the builder names the exact function of the scribe's brief it touches in the report; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_settle_driver.py` (new; `Driver` stubbed as in `test_manual_window.py`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1986-u3.md` (new)
**non-goals:** the investigation pass and its rule (S3) — unchanged; repairs; the scribe's verdict; t-1957 N5s's S6 lanes.
**behaviour:** §3.4 points 2–3, §3.6. **edges:**
- E3.1 POSITIONAL: `close_unsettled` before `s7_investigation_gate` at all three closers. INVARIANT: no S7 close or awaiting over a place
  that is neither settled nor gapped; the investigation never re-gaps a settle place (U1 E1.12).
- E3.2 POSITIONAL: the session opens after the dispatch is registered and before `run_role`; closes in a `finally` (role crash, Refusal,
  reused saved result). INVARIANT: no walk server or stand lease outlives the triage dispatch (t-1957 E1.7).
- E3.3 the session cannot open (lease held, stand down, Slice 1 absent) -> the brief line of §3.6 and a printed line; the triage runs.
  INVARIANT: «Фабрика не должна вставать»; a place that needed the page is answered `impossible` by the role or gapped by code — never
  silently unconfirmed.
- E3.4 `settle.places` raises or returns `unreadable` -> one printed line, the brief says "could not be computed whole", the close still
  calls `close_unsettled` on what it can read. INVARIANT: an exception of the settle code never stops S7 (P1) and never reads as "none".
- E3.5 TEMPORAL (resume within the run): a resumed / relaunched triage dispatch whose session is not `ready` -> reopened before the resume
  words (t-1957 E1.16). INVARIANT: a resumed analyst never holds a dead walk id.
- E3.6 `s7.no_failures` (no analyst) with `register` places -> gapped with "the analyst was not dispatched: no failure to triage" (F-F (a)).
  INVARIANT: a register contradiction never vanishes from the report because nothing failed.
- E3.7 a re-triage (`s7_retriage_once`) -> the same places list recomputed; settle records already written stay valid. INVARIANT: a settled
  place is never walked again because the triage restarted.
**DoD — `test_settle_driver.py` (fast):** `test_close_unsettled_before_investigation_gate` (stub gate records whether the register already holds
the settle gaps), `test_session_opened_before_role_closed_after`, `test_session_closed_when_role_crashes`, `test_session_failure_brief_line`,
`test_places_error_one_line_and_close_still_runs`, `test_brief_names_places_and_answer_keys`, `test_no_failures_gaps_register_places`,
`test_scribe_brief_names_unsettled`, `test_resume_reopens_session`. Negative control: the call moved after the gate makes
`test_close_unsettled_before_investigation_gate` fail. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_settle_driver.py ai-packages/qa-factory/scripts/tests/test_settle.py -q`
(CI: `test_story_run_s7.py`, `test_story_run_s7_live.py`). Critic mandatory (core). `architecture:` AR-14, AR-17, AR-19, AR-25, AR-27, AR-28, AR-29.

#### U4 — the analyst's charter, the skill road, role-load
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-failure-analyst.md` (the §3.5 edits only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\skills\qa-story\phases\s7.md` (one paragraph after "## Dispatch" naming `settle.py list|write`, the four answers, the expectation-source rule, and the close step `settle close-unsettled` before section Investigation; the skill road twin, AR-19)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\role-load.json` (analyst rows: lowered to the measured value if lower; NEVER raised)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_charters_s5_s9.py` (KEYS `qa-failure-analyst` += "Find out the truth on the page", "never a bug", "an expectation the factory derived itself is no requirement"; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1986-u4.md` (new)
**non-goals:** the runner's walk charter (t-1957 N4); the scribe's charter; other analyst sections.
**behaviour:** first run `python -B ai-packages/qa-factory/scripts/role_load.py --role qa-failure-analyst` on the UNCHANGED tree and attach it;
apply §3.5; run it again. **edges:** E4.1 the total or process load rises above its row (17 753 / 16 145) -> STOP, revert, report both numbers
(no raise, AR-20). E4.2 a form token (`evidence/`, `TEST_BUG`, ...) written into Techniques -> `test_m1_form_tokens_stand_in_tools` red.
INVARIANT: experience in Techniques, form in Tools. E4.3 a principle number, `AC`, "must run" or "Step N" -> red (K-C1/C3/C4). E4.4 the skill
road and the driver name the same close order (U3 E3.1). **DoD:** `test_charters_s5_s9.py` and `test_case_role_twins.py` green with the new
keys (negative control: the run on a copy without "never a bug" fails `test_craft_keys_stand_verbatim`); both `role_load.py` outputs attached.
Witness: `python -m pytest ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py ai-packages/qa-factory/scripts/tests/test_case_role_twins.py ai-packages/qa-factory/scripts/tests/test_role_load.py ai-packages/qa-factory/scripts/tests/test_charter_form.py -q`
`architecture:` AR-2, AR-10, AR-11, AR-19, AR-20.

#### What happens to t-1957 N6
N6 is RETIRED from Slice 3 and replaced: its `walk_session.py --place control` roots -> U0 (with `settle`); its `stage_S7` `finally` close ->
U3's `s7_settle_session` (one session serves control experiments and settle walks: the item is the control label or the place id); its
charter Tools line and the deletion of `manifest_view.py`/`env_probe.py` (:66) -> U4; its role-commands and role-load rows -> U1/U4; its
tests `test_control_record_under_evidence` / `test_triage_control_accepts_walk_record` -> U0's two root tests; its edges E6.1–E6.4 hold
unchanged (E6.1 `impossible` with why = this spec's `impossible`). Dependency on Slice 1: N1a (server, `step` of 1..N steps — the analyst
sends one step or a short obvious run, owner's word 21:20), N2 (`_quote_in` over the item's attempt; the verdict record is NOT used by a
settle walk — the settle answer is its record), N4 (the step-call paragraph the brief points to), N5s (the `run_role` hook precedent; U3
does not reuse `after=`, it closes in a `finally` because nothing must bind before `bind` here). Slice 3 keeps only N7.

#### Live proof (FR-33) on MyBooks LOCAL-1
In a stand copy, after t-1957 Slice 1 is proved: rerun S7 of arm B's tree copy (the 7 code-reading drafts R-12/13/14, S5) or a fresh LOCAL-1
run to S7. Accept: (1) `settle.py list` shows the places (expected 3–7 — **estimate**); (2) every place ends `settled` or as a named gap line;
(3) at least one `bug` answer lifts its draft to "reproduced by the factory" in the report, at least one `requirement_silent` shows as a
question in gate B's packet, and no `bug` stands on `expectation.source: none`; (4) the Lead cross-checks each answer's expectation source
against the register (the plain-agent lesson, S6) and lists disagreements; (5) time and cost per place by `walk_timing.py --summary` grouped
by place `settle` against §3.7 (≈ 3–6 min, ≤ $0.40 per place; **estimate**, basis t-1957 §3.10 (2)). Expected wall of the proof: ≈ 30–60 min
of S7 for 3–7 places plus setup — **estimate**.

---

## §5 Questions for the owner (only what only she knows)

- **Q1 — ANSWERED by the owner 05.11.2026 22:07: «Только неподтверждённые» (only the unconfirmed suspicions; the recommendation stands).** Should the analyst also walk the oddities it already cleared by reading?** Today, when the runner noted something strange and the
  analyst says "not a bug" quoting the recorded line, nobody goes back to the page. Walk those too (more certainty, but a run with 30 recorder
  oddities would mean 30 walks — far more than your 3–5), or only the suspicions nobody has confirmed (bug drafts, what the run left open,
  code places that contradict a requirement)? **Recommendation: only the unconfirmed suspicions;** the analyst may still walk any oddity it
  doubts.
- **Q2. A cap per run?** If a run produces many more suspicious places than usual (say 15), should the analyst walk them all (≈ 3–6 min and up
  to $0.40 each — estimate), or walk the first N by severity and list the rest as "not checked" in the report? **Recommendation: no cap
  for now; measure on the first runs, and add a cap only if a run goes over ≈ 10 places.**

---

## §6 Forks for the Lead (the nodes are written to the recommendation)

- **F-A. Where the walk happens.** (a) Inside the TRIAGE dispatch: the analyst who writes the verdicts and drafts walks the places, the
  investigation pass stays read-only for what is left; (b) widen the existing investigation pass into a "settle pass" (lift its "never compare
  with an expected value" rule, S3; the pass cannot write drafts, so a `bug` found there needs a re-triage); (c) a new third S7 pass.
  **Recommendation (a):** one author, one context for verdict, draft and walk; no new dispatch; the investigation's read-only honesty and its
  one-pass rule stay as they are.
- **F-C. A place the analyst did not settle.** (a) A named gap line in the register (report + gate B) and a line in the scribe's acceptance
  brief; the scribe judges whether to return the triage; (b) also keep S7 open once for a second analyst dispatch on the unsettled places
  (like `investigation_pending`). **Recommendation (a):** the acceptance by a tier above already exists (X7-6b); (b) doubles the S7 spend for
  what the scribe can return anyway.
- **F-D. A `bug` resting on a requirement no source confirms** (`contract.unconfirmed_requirements`). (a) Refused by `answer_problems`
  (xref against a code-derived set; error direction toward a question); (b) accepted, the report marks "expectation not confirmed".
  **Recommendation (a):** this is exactly today's lesson (9 + 2 «bugs» on derived expectations, S6); the door is `requirement_silent`.
- **F-E. Who opens the walk session.** (a) The S7 driver, before the triage dispatch, closed in a `finally`; (b) the analyst from its Bash
  (needs S0 "survives: yes, yes"). **Recommendation (a):** independent of the unmeasured host behaviour (t-1957 F38); S0 stays informational.
- **F-F. Register contradictions when nothing failed** (`s7.no_failures`, no analyst runs). (a) Gap line "the analyst was not dispatched";
  (b) dispatch the analyst to settle them. **Recommendation (a)** for this batch; (b) is a change of "nothing to triage" and wants a
  measurement of how often it happens (a row for the Lead's pile).
- **F-H. Census label of `settle.py::_refuse`.** (a) `["qa-failure-analyst"]` (+1 there); (b) `["conductor"]` by the recorder convention.
  **Recommendation (a):** only the analyst calls `settle.py write`.
- **F-I. One more charter cut** ("Settle it yourself first: ... a control experiment.", :81). Recommendation: take it only if U4's E4.1 fires.

Small choices closed by the designer: module name `settle.py`, data file `references/settle.json`; answer words `bug | not_a_bug |
requirement_silent | impossible`; place ids `draft-<stem>`, `req-<R>`, the investigation target id unchanged, `new-<slug>` for the role's own;
record path `evidence/settle-<place>.json` beside the diagnostic/control convention (S9); the draft id wins when two sources meet; `--replace`
for a correction; the gap reasons as data; U2 reads the written record (no re-run of U1's checks) and checks the capture sha; the register
line of a `requirement_silent` answer is written with the analyst's dispatch id as `by` (a role line, so `investigation.unresolved_targets`
reads it as resolved for an `open` place, S2 (ii)).

Found while drafting, for the Lead (not widened here): (1) observation-based and code-reading drafts can never reach `reproduced_by_factory`
today (S4) — U2 opens the step only through a walk; whether `own_script` should also skip the current-red fact for them is a separate row.
(2) Where a triage dispatch records "a question with both readings" for an observation (S7) could not be established — `requirement_silent`
gives it a carrier; a sibling of the same class may live in the S6 runner's `expectation_unconfirmed` road (`vocabulary.yaml:109`).
(3) The investigation brief's "never compare with an expected value" (S3) and this spec's "name the expectation source" now coexist in one
stage; the charter tells them apart by dispatch purpose — the critic should check the two brief texts do not contradict (FR-10).

---

## Reading trail

Given, read: t-1957 spec :1-1335 (whole §1–§4, §6, §7, trail); `disputed-check-plain-agent/SUMMARY.md` whole; `thinking-roles.md` :134-177;
`agents/qa-failure-analyst.md` whole; `skills/qa-story/phases/s7.md` whole; `handoffs/s7-analyst-to-automator.yaml` whole; `references/role-load.json`
whole; `references/investigation-budget.json` whole. Code (wt-fbfix): `investigation.py` :1-559; `story_run.py` :12349-12628, :12780-12964 (+ grep of
S7/investigation sites); `contract.py` :1160-1219, :1330-1429, :1810-1900, :2094-2214, :4398-4555, :4815-4854 (+ greps); `bug_records.py` :310-359,
:480-686, :686-931 (+ def grep); `manual_evidence.py` :295-365; `validate_artifacts.py` :2334-2380; `exploratory_findings.py` (constants grep);
`investigation_probe.py` (def grep); `vocabulary.yaml` (grep :30-110); `manual-capture-steps.json` (grep surprise); `judgment-census.json` (grep :4,
:54-60, :416-419); `test_judgment_census.py` (grep); `test_charters_s5_s9.py` :1-294; `test_case_role_twins.py` (grep :65); `slow_tests.json` (grep).
NOT read (stated where used): `walk_session.py` (not on the branch; t-1957 is the source); `question_register.py` beyond one grep; the analyst's
key page file; `report_facts.py` beyond :351-361; `s7_await_scribe`'s scribe brief function; `artifact-writers.json`; `role-commands.json`.
`role_load.py` was not run (no shell) — the live analyst load is unknown (S11). Needed beyond the manifest: `investigation.py`,
`exploratory_findings.py`, `bug_records.py`, `validate_artifacts.py`, `test_charters_s5_s9.py`, `test_case_role_twins.py`, `slow_tests.json`.
