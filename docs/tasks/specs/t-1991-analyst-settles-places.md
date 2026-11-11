# t-1991 — the analyst settles every suspicious unconfirmed place — REVISED SPEC (designer, revision of t-1986 by critic verdict t-1987)

Status: **draft for the Lead's acceptance** (designer, 05.11.2026). Replaces the draft `docs/tasks/specs/t-1986-analyst-walks-unconfirmed-places.md`
(left untouched) by the critic-on-plan verdict `docs/tasks/specs/reviews/t-1987-critic-on-plan-t-1986.md` (`fit_with_fixes`, 6 blockers, 15 fixes).
Amends `docs/tasks/specs/t-1957-fast-manual-walker.md` (not edited here): its node N6 (Slice 3) is RETIRED and replaced by this batch; its node
N1a is NOT changed (§3.6, U0). Package: worktree `D:/ws1/wt-fbfix` (below `PKG\` = `D:/ws1/wt-fbfix\ai-packages\qa-factory`). Every
file:line below was re-read by this designer in that tree on 05.11.2026 (the critic's numbers were not copied; where they moved, the new ones are
given); what was not read is marked **estimate** or **could not establish**. No compatibility with stories, plans or evidence of an older package
version (owner's decision): temporal edges cover one run on the new version, before and after each node's merge.

Owner's word (05.11.2026 ≈21:40, `experiments/mybooks/thinking-roles/thinking-roles.md:177`): «Вот ты сейчас проверил 24 подозрительных места и
сказал как обстоят дела на самом деле. Вот так и аналитик должен проходить все подозрительные неподтверждённые места и выяснять правду. С одного
прогона их будет не 26, а всего 3-5». Owner, 05.11.2026 22:07, on Q1: «Только неподтверждённые» — only the unconfirmed suspicions are walked;
oddities the analyst already cleared by reading the records are not walked again.

**What changed against t-1986, in one paragraph.** The core stands (one data join, one record per place, the role answers, code carries and
checks keys and cross-references). Changed: a settled `open` place is resolved for the investigation by a new clause (iv) of the ONE resolution
reader (fix 1); every register line names every field `append` needs, with `add`/`correct`/`withdraw` by the chain rule and a `carrier missing`
state when a line could not be written (fix 2); a `bug` answer has a stated draft form per source, and a fork where none exists (fix 3, F-J); the
walk session of an S7 lane takes the stand lease PER REQUEST and does not die of idleness inside a dispatch (fix 4); the walk receipt re-runs the
answer check and keeps the APP_BUG fact for every triage-road draft (fix 5); a new expectation source `person` reads the words of the rework built
from a person's gate-B answer (fix 6); place ids never change in a run (fix 7); the module is `place_answers.py` (fix 15); and the nodes are re-cut
so that U1, U2 and U3a start NOW on today's recorder, with no walker code (fix 14).

---

## §1 Goal, AR-n / FR touched, owner and census class of every check

**Goal.** At S7 the failure analyst owes, for every suspicious unconfirmed place of the run, an answer it found out on the stand — `bug` /
`not_a_bug` / `requirement_silent` (a question for the person who decides the expected behaviour, never a bug) / `impossible` (with why) —
that quotes what the stand showed in a capture the factory's recorder wrote, and names the SOURCE of its expectation (`requirement` R-n, a
settled `question`, the `person`'s recorded words, or `none`). Code assembles the places from records that already exist, checks the keys and
cross-references of an answer, carries it to the readers that already exist (the draft's step, the findings register, the report, gate B, the
investigation's resolution, the scribe's acceptance), and turns every place nobody settled into a named gap. Code never decides which answer is
right (AR-29). The walker of t-1957 makes the walk FASTER; the road itself works today through `manual_capture.py ui|http` (§3.6).

| AR | how touched | change check written into the DoD of node |
|---|---|---|
| AR-2 open variety is the role's | what is suspicious beyond the joined records, the order, the steps, the answer — the analyst's; `--place new-<slug>` for its own | U1 `test_places_is_a_join_only`, `test_new_place_accepted` |
| AR-7 / AR-29 code = instrument, role = judgment | `place_answers.py` checks keys and cross-references, never truth; the answer is accepted by the S8 scribe (X7-6b) | census rows below; U1 `test_answer_never_judged_by_words` |
| AR-10 a check's requirement reaches the role first | the answer keys, sources and refusal doors are in the brief lines (U3a/U3b) and `place_answers.py --help` | U3a `test_brief_names_places_and_answer_keys` |
| AR-11 only the context and tools the work needs | charter cuts (§3.5); the analyst gains `place_answers.py list|write` and, by fork F-M, `manual_capture.py ui|http` for a `settle-<place>` case only | U4 role-load not above its rows; U1 role-commands rows |
| AR-13 / AR-15 one reader, one survivor | ONE join `place_answers.places`; ONE "is settled" predicate `place_answers.settled_answer` read by the place list AND by `investigation.unresolved_targets` (iv); the draft's step only through `bug_records.confirmation_of`; contradictions only through `branch_accounting.code_says_contradicts`; draft folders through `bug_records.draft_listing`; quotes through `manual_evidence._quote_in`; the attempt root through `manual_capture.case_root` | U1, U2 |
| AR-14 one artifact, one writer | `evidence/place-answer-<id>.json` writer `place_answers.py` (code sets `writer`, `written_at`); register lines only through `exploratory_findings.append`; drafts stay the analyst's | U1 `artifact-writers.json` row |
| AR-17 a state code has no move for goes to the conductor | none added: every state has a code move (gap line) or a role door | — |
| AR-19 stage twins | `phases/s7.md` names the same list, answer, and `place_answers.py close-unsettled` step as the driver | U4 E4.4 |
| AR-20 shrink-only ratchets | `blocking_per_role.qa-failure-analyst` 131 -> 132 (ONE named raise: `place_answers.py::_refuse`); analyst `role-load.json` rows never raised | U1, U4 |
| AR-21 / AR-22 producer and reader together | record -> `bug_records.reproduction_problems` (kind `walk`) -> report/gate B; record -> register line -> `report_facts.exploratory_gate_parts`; record -> `investigation.unresolved_targets` (iv); record -> the scribe line; `written_at`, `walk`, `replaces` declared terminal in `references/place-answers.json` | U1, U2, U3a |
| AR-23 empty outcome declared | no place: "Places to settle: none in this run"; a place list that cannot be computed whole is said so, never "none" | U1 E1.1/E1.2, U3a |
| AR-25 every state a way out | place states `open` -> `settled` / `carrier missing` / `conflict` -> a gap line at the close (code) or a new `write` (role) | U1 E1.11-E1.13 |
| AR-26 requirements are the unit | an expectation is an R-n, a settled question or a person's words; `none` is never `bug` | U1 E1.5, E1.6 |
| AR-27 a finding reaches the report under its owner | `requirement_silent` -> `unresolved_question` (owner `investigation.OWNER_WORDS`); `not_a_bug` -> `observation`; unsettled -> `coverage_gap` | U1 |
| AR-28 / FR-59 unknown never a pass | an unreadable source makes the list "not computed whole"; an unchecked receipt reads `unconfirmed`; an invalid record resolves no investigation target | U1, U2 |

FR touched: FR-1, FR-2, FR-57 (every refusal of `place_answers.py` names a door the analyst can use), FR-10 (a draft standing against its own
answer is a conflict with its own gap text; the charter's new bullet is scoped to a triage), FR-12, FR-13 (answers, sources, gap texts are data),
FR-18 (a walk is evidence of THIS place only), FR-21/FR-22 (a `bug` answer has a road: the draft form per source, F-J), FR-23 (`impossible`),
FR-38, FR-41, FR-47, FR-48 (P22), FR-58 (`none` is never a bug), FR-8 (`person`: the person's words carried whole), FR-33 (live proof).
Principles: P20, P22, P26, P27, P23, P28, P9 (the `question` field is plain words).

**Checks added or altered: owner served and census class** (class words `PKG\scripts\tests\test_judgment_census.py:60` `CLASS_ORDER`; unit names
`UNIT_NAME_RE` :58 — `*_problems`, `_?refuse`, … ; a neutral name is no unit).

| check (file :: function) | node | added/altered | owner served | class | blocks? | why not a judgment |
|---|---|---|---|---|---|---|
| `place_answers.py :: answer_problems` (§3.2 keys; source membership in register / question register / words file of THIS dispatch; F-D: R not in `contract.unconfirmed_requirements`; capture row in THIS place's attempt index with its `content_hash` equal to the bytes now; quote in the capture; `question`/`why`/`draft` present where the answer needs them) | U1 | added | data | xref | no (returns a list) | membership, joins, quoted bytes found; never reads what the words mean |
| `place_answers.py :: _refuse` (the ONE raise of `write` / `close-unsettled` CLI) | U1 | added | data | shape | **yes**: `blocking_per_role.qa-failure-analyst` 131 (`judgment-census.json:4`) -> 132, the ONE named raise | formats what `answer_problems` returns |
| `place_answers.py :: places`, `place_of_draft`, `settled_answer`, `unsettled`, `close_unsettled`, `write` | U1 | added | data | — (neutral names: no unit, no row) | no | joins and presence; `close_unsettled` closes no obligation, it records that it was not met |
| `investigation.py :: unresolved_targets` (+ resolution (iv)) | U1 | altered | data | — (not a unit: `unresolved_targets` is in no census row; Grep of `judgment-census.json` for `unresolved_targets` found nothing while the same call found `reproduction_problems` :58) | no | a presence join of a record that passed a data check |
| `bug_records.py :: reproduction_problems` (+ kind `walk` through `_walk_receipt_problem`) | U2 | altered | data | xref (unchanged row, `judgment-census.json:58`) | no | a join of receipt -> record -> capture; error direction DOWN (§3.3). `_walk_receipt_problem` ends in `_problem` (singular): no unit |

**Ratchet verdict (AR-20) for the Lead:** ONE raise, `qa-failure-analyst` 131 -> 132 (`place_answers.py::_refuse`, roles `["qa-failure-analyst"]`,
F-H (a) as decided). No honest offset. `close-unsettled` is called by the driver and the conductor's skill road; its refusals go through the same
`_refuse`, so no second row.

---

## §2 Facts (file:line, re-read in `wt-fbfix` on 05.11.2026)

The critic CONFIRMED S1, S3, S6, S8 (with additions), S10, S11, S12 and the negatives N1, N2 of t-1986 (verdict §A); they are kept by reference to
t-1986 §2 and not re-litigated. Below: the facts the revision rests on, every one re-read.

### The investigation's resolution (fix 1)
- **F1.** `investigation.unresolved_targets` (`PKG\scripts\investigation.py:371-424`) resolves a target ONLY by: (ii) a withdraw (:394-395) or a
  non-code active line of kind `coverage_gap` (:396, :399-400); (i) a non-code active line with `verification_status != "unverified"` AND
  `probe.runs >= 1` (:401-402); (iii) a triage row with a `resolving_verdicts` verdict and evidence under `work/evidence/` (:409-417). "Code line" =
  `recorded_by` starts with `code:investigation.` (`CODE_PREFIX` :36, `is_code_line` :79-80). `exploratory_findings.append` refuses any status
  above `unverified` on a line with no probe (`exploratory_findings.py:310-313`). So an analyst's `unresolved_question` or `observation` line
  never resolves its target; only a `coverage_gap` does. `open_targets` (:460-463) is the one entry; `close_gaps` (:468-519) walks EVERY chain
  (`for target in sorted(chains)` :494) and corrects every all-code chain to "not investigated" (:499-518); `decision` (:538-558) returns
  `dispatch` while anything is unresolved and no pass exists.
- **F2.** `investigation.project` runs INSIDE `s7_investigation_gate` (`story_run.py:12863`) and adds a `code:investigation.project` line for each
  target with no chain (`investigation.py:319-327`), skips a chain a role touched (:321-323).

### The register writer (fix 2)
- **F3.** `exploratory_findings.append` (`exploratory_findings.py:277-393`) requires `title`, `statement`, `why_not_a_bug` (`REQUIRED_TEXT` :57,
  :325-327); `question` AND `owner_role` for `unresolved_question` (:328-329); `missing_prerequisite` for `coverage_gap` (:330-331); a non-empty
  `evidence_refs` of files under the story, each judged by `contract.evidence_ref_issue` (:335-338, `_judge_refs` :234-252); `origin` needs both
  `dispatch` and `target` (:265-274); an `add` on a target that has ANY chain — even a withdrawn one — is refused (:344-349); a `correct`/`withdraw`
  must name the ACTIVE line of the same target (:350-359); `pipeline.json` unreadable -> ValueError (`_window` :190-196). A refused call writes
  nothing (docstring :278-279). `oracle_status: person_confirmed` is written only by the driver on a person's `intended` at gate B (:39, :319-322).
- **F4.** Gate B shows a register line as a question only when it is ACTIVE with `oracle_status == owner_question`; it is ADDRESSABLE (answerable as
  `<case>: intended|bug|open`) only when `_annotate_cases` finds a case for it; an active `coverage_gap` that is no question is shown as a gap
  with its `statement` and `missing_prerequisite` (`report_facts.py:2852-2898`, :2876, :2886-2894). **Could not establish** how `_annotate_cases`
  derives a line's case (not read): a `req-<R>` place's question line may be shown but not addressable; then the person's free words reach the
  conductor (the live proof checks it, §4).

### Drafts and their step (fixes 3, 5, 7)
- **F5.** Triage-road draft: `BUG_DRAFT_REQUIRED = ("title","impact","violates","case","triage_ref","manual_steps")` (`contract.py:1832`).
  Code-reading draft: `evidence: "code-reading"` (`bug_records.is_code_reading` :482-485), `BUG_DRAFT_CODE_READING_REQUIRED` incl. `oracle`, `fact`,
  `check_state` (`contract.py:1881`), `CODE_READING_CHECK_STATES = ("not_executed","unverifiable")` (:1882); the comment says "where no run spoke"
  (:1878-1880) and the refusal says "a code-reading draft exists only where no run spoke" (`bug_records.py:658-660`). Its oracle (`_oracle_problems`
  :585-635): question form = `branch_accounting._confirmed` + the quote in the answer (:596-617); requirement form = the register row of the
  draft's R says `code_says: contradicts: <this draft's fact id>` (:618-632) — a code place `{path,line,quote}` without a fact id cannot satisfy the
  requirement form (`fid` empty, :629-630). One code-reading draft per R (`R_CR_TWICE` :672-678).
- **F6.** `reproduction_problems` (`bug_records.py:756-828`) voids EVERY entry unless the draft's triage row says APP_BUG (:776-777) and, when the
  report is readable, the instance's CURRENT result is red (:778-790). `draft_triage_key` (:319-328). `contract.triage_failures` (:4497-4555) is the
  one binding unit: kinds `result` (automated rows of `current_results`), `manual` (manual checks `fail`/`inconclusive`/unprepared), `observation`
  (`<case>#obs<n>`, `<case>#sur-<id>`). A manual or observation instance has no row in `current_instance_results` -> R_NO_CURRENT (derived from
  the code, not run, as the critic traced).
- **F7.** `bug_records.draft_paths` (:204-212) drops an unlistable folder silently "for a reader that only walks the drafts"; a reader that gives a
  verdict asks `draft_listing` (:212, returning `(paths, unreadable)` :195-201).
- **F8.** Nothing stops a role's FIRST Write of a file: `guard_pre_tool.artifact_rewrite_check` returns for a file that does not exist yet
  (`guard_pre_tool.py:1211-1212`). No write log of role Writes exists: Grep `writes\.jsonl|role-writes|tool-writes|written_paths` over
  `PKG\scripts\*.py` -> nothing; positive control, same tool and glob, `driver-answers\.jsonl|captures\.jsonl` -> 5 files. Precedent of a
  code-owned evidence file a role could also write: `evidence/diagnostic-*.json` ("code's file, never the role's", `contract.py:2333-2334`) is
  trusted by name and presence (:2361-2372).

### Captures and the evidence roots (fixes 5, 12)
- **F9.** `manual_capture.case_root(task, case)` = `<task>/work/evidence/manual/<case_dir_name(case)>` (`manual_capture.py:100`, :291-292);
  `attempts_of(root)` lists `aN` (:300-304); every capture is a row of `<attempt>/captures.jsonl` with a task-relative `path` and the
  `content_hash` (sha256) of the file (:1132, :1138-1145). `manual_capture.py ui|http` take `--case` (required) checked only by `case_dir_name`
  (`_run_http` :4427-4429; parser :4634-4663) and root the attempt at `case_root` — so `--case settle-<place id>` lands under
  `work/evidence/manual/settle-<place id>/aN/` with no code change (**estimate**: `run_http` was read to :4461; whether a later step refuses a case
  with no `request.json` was not established — the account then defaults to the stand's, per the `--as` help :4644-4647). `http` holds the stand
  lease per call with job `manual:<case>:…` (:4415). `manual_evidence._safe_evidence_path` accepts `work/evidence/…` and `evidence/…`
  (`manual_evidence.py:56-62`); `_quote_in(root, ref, quote)` (:176-178); `_jsonl(path)` (:1339).
- **F10.** The pattern "a file inside an attempt of THIS case, quote in it" already exists once: `contract.triage_contradiction_problems`
  (`contract.py:2286-2317`: `MC.case_root` + `evidence_ref_issue(..., under=)` + `MC.attempt_number` + `ME._quote_in`).

### The stand lease (fix 4)
- **F11.** `stand_lease._try_acquire` re-enters only for the same `job_id` AND the same pid (`stand_lease.py:167-168`); `hold` waits up to
  `wait_s` then raises `StandBusy` (:195-243). `run_suite.hold_stand` takes it only when the stand is serial (`run_suite.py:1373`), waits
  `run.stand_wait_s`, default 1 800 s (:1381-1383), and exits 3 `stand_busy` (:1387-1391). `manual_capture._hold_stand` is "ONE lease helper for
  the suites and the captures" (`manual_capture.py:3911-3913`).
- **F12.** t-1957 §3.2: the server "holds TODAY's exclusive stand lease for its whole life" (`t-1957…md:333`); exits after `idle_s` 900 / `max_s`
  5 400 / parent gone (:400-403); data rows in N1a's owns (:589); E1.7 (:629-630), E1.16 reopen for the same W (:646-647); Slice 1: "One walker;
  today's exclusive lease; no new config key" (:571). N1a has NO `--place` argument (its owns :587-591 list none) — `--place` is introduced by U0.

### The person's words after gate B (fix 6)
- **F13.** A `bug` answer at gate B on a register question line is carried out by ONE rework of S7 (`story_run.py:16739-16748`:
  `record_seam_rework(args, self.answer_file(), preface)`); `answer_file` is `state/words/driver-answer-<ms>.txt` (:4898-4907, written by
  `words_file` :1378-1409, created with "x", never overwritten). `seam_rework_step` (:6852-6890) calls `rework(..., words_file=rel)` (:6883-6884);
  `rework` passes `--words-file` INSTEAD of `--reason` (:9869-9870) and runs the role through `run_role(..., rework=given)` (:9889), NOT through
  `stage_S7`. The controller reads the reason from that file whole (`controller.py:8917-8919`, `person_words.read`), stores it as the request's
  `reason` (:3428) and marks `person_words: True` (:3465-3466). A free-words answer the conductor turns into a rework goes through
  `chosen_rework` -> `record_seam_rework` with the question's words file (:5422-5426) — the same mark.

### The S7 driver (fixes 8, 9, 14)
- **F14.** `run_role` (`story_run.py:2790-2864`): the dispatch id is known at :2799 (rework) / :2834 (fresh); `lines += list(extra)` :2842; the role
  runs only when no saved result exists (:2851-2856); `bind` :2860. Every S7 analyst dispatch — fresh triage (`stage_S7` :12438), scribe-reject
  rework, seam rework (F13), investigation (:12896, `purpose="investigation"`) — passes here. `investigation.pass_members` (:524-535) uses
  `controller.s7_part_of(d) == "investigation"`, the one predicate of an investigation dispatch.
- **F15.** Closers: `s7.no_failures` (:12379-12391) and `s7.pretriaged` (:12412-12422) inside `stage_S7`, each calling `s7_investigation_gate`
  first; `s7_close` (:12805-12843) calls the gate (:12811) then `s7_await_scribe` (:12818). Fresh triage lines `told` (:12424-12432). The
  investigation brief `investigation_lines` (:12912-12969) carries "Record what the product does; never compare it with an expected value; never
  write a bug or a triage row; only `investigation_probe.py` reaches the stand" (:12959-12960). The scribe's acceptance lines: `stage_S8`, the
  `if awaiting:` block (:13404-13410) — this names the function the critic's G2 asked for.
- **F16.** `role-commands.json`: `manual_capture.py ui|http` rows have roles `["qa-runner"]` only (:40-53); `red_sandbox.py --diagnostic` is the
  analyst's (:135-141). **Could not establish** whether a guard refuses a role a command its row does not list (`role-commands.json` is read by
  `role_cli.py` and `brief_pack.py`; the guard path was not read): fork F-M and U1's rows make it explicit either way.

### Negative claims (each with its search and a positive control of the same form)
- **N3.** No reader walks every folder under `work/evidence/manual/` as a case: Grep `"evidence" / "manual"|evidence/manual/\*|case_root\(.*\)\.parent|\.parent\.iterdir`
  over `PKG\scripts\*.py` -> one production hit, `brief_pack.py:3001` (a glob of `*/tried.md`, harmless for a `settle-` folder); the same call
  found it, so the pipe works. **Estimate**, not proof: another spelling of such a scan may exist; U1's fixture runs `finalize_task` /
  `gate_preflight` readers are NOT re-run (CI), and the live proof watches for a `settle-` folder named as an unknown case.
- **N4.** No existing word for a role's own suspicion beyond the joined records: kept from t-1986 N1 (confirmed by the critic).

---

## §3 Design

### 3.1 The places — ONE join, data only (U1)

`place_answers.places(task_root) -> {"places": [place], "unreadable": [(record, why)]}`; a place is `{id, sources, refs, title, expectation_hint}`.

**Sources and the readers (fix 12):**

| source | from (existing reader) | listed when |
|---|---|---|
| `register` | `contract.register_rows` over `work/requirements-register.md` | `branch_accounting.code_says_contradicts(row)` (`branch_accounting.py:1240-1243`, the reader gate A uses at `gate_brief.py:2000`) |
| `open` | `investigation.open_targets(task, budget)` -> `unresolved` PLUS the new key `settled` (§3.4, fix 1) | listed there |
| `draft` | `bug_records.draft_listing(task)` (its "not read" list feeds `unreadable`) + `bug_records.confirmation_of(task, draft, rows, report)[0]` with `step_facts` read once | the derived word is `unconfirmed` |

**Place ids — never change during a run (fix 7).** An id is derived from a record that exists BEFORE S7 (register row, investigation target) or,
failing that, from the draft itself; a draft written later JOINS an existing place and never renames it.
- register row R -> `req-<R>`.
- investigation target -> its id unchanged (`case-<C>`, `obs-<dispatch>-<i>`; `investigation.py:170`).
- a draft -> `place_answers.place_of_draft(task, name, draft, rows, targets)`, pure, the ONE reading of "which place a draft belongs to" (U2 reads
  it too): (1) a code-reading draft -> `req-<R>` of its first `violates` R (unique per R, `R_CR_TWICE`), whether or not the register row still
  contradicts; (2) a triage-road draft whose `case` equals the `case` of an investigation target (`investigation.investigation_targets`, ALL
  targets, never only the unresolved ones, so a resolution never moves a draft) -> that target id; (3) a triage-road draft whose `violates` names
  an R whose row `code_says_contradicts` -> `req-<R>` of the first such R (`contract.REQ_ID_RE` order); (4) else `draft-<file stem>`.
- the role's own suspicion -> `new-<slug>` (`[a-z0-9-]{1,40}`), listed from its own record (it exists only once written).
- Two pre-existing places are NEVER merged with each other (a `case-C` target and a `req-R` row stay two places even when one draft touches both;
  fork F-L). A place appears once; its `sources` list every source joined into it; `refs.draft` names the joined draft(s).

`refs` carry what the role needs to find the place: draft `triage_ref`, `violates`, `manual_steps`, `red_test`, `fact`; target `then`, `observed`
(verbatim), `evidence`, `case`; register row `requirement`, `code_says`. `expectation_hint` = the R the record already names (draft `violates`,
target `requirements`, row `r`) — a hint, never the answer's source. A triage verdict the analyst gave with evidence (`NO_DEFECT` quoting the
recorded line, `TEST_BUG`, `FLAKY` with three reruns, `ASSERT_STRICTER` with its control) is NOT a place (owner, Q1: only the unconfirmed).

**EMPTY / unreadable (AR-23, AR-28):** no place and nothing unreadable -> `{"places": [], "unreadable": []}`, the list line "Places to settle:
none in this run". A source that cannot be read — a draft folder `draft_listing` could not list, a draft JSON that does not parse, a register
whose table `register_rows` refuses (ValueError), an investigation budget `load_budget` refuses (then `open_targets` resolves nothing, F1), an
exception of `investigation_targets` — is one `unreadable` entry with why, and the list line says "the list of places could not be computed
whole: <why>"; never "none".

### 3.2 The answer — the role's, carried by code (U1)

The analyst writes `work/place-answers/<place id>.json` (its scratch; any name) and runs
`place_answers.py write --task-root T --dispatch <its dispatch id> --place <id> --file <f> [--replace]`. The answer:

```
{"place": "req-R-12", "answer": "bug|not_a_bug|requirement_silent|impossible",
 "expectation": {"source": "requirement|question|person|none", "id": "R-12 | Q7 | state/words/driver-answer-<ms>.txt | ", "quote": "<verbatim>"},
 "seen": {"quote": "<words the stand showed>", "capture": "<task-relative path of the capture>"},
 "question": "<requirement_silent only: the question for the person who decides, plain words, P9>",
 "why": "<impossible: what the stand lacks | not_a_bug: why, in the role's words>",
 "draft": "<bug only: the file name of the draft under work/bug-drafts/ that carries this record as its walk receipt>",
 "walk": "<the walk id, when the walk session was used>"}
```

**`answer_problems(task, record, *, dispatch=None)` — pure, never raises, `[]` when it stands.** It reads NO place list (so U2 and
`investigation` may call it without recursion through `places` -> `confirmation_of` -> U2). Rules, each a closed check with a door:
1. `answer` in `references/place-answers.json` `answers`; `expectation.source` in `sources`; `place` matches `^(req-R-\d+|case-.+|obs-.+|draft-.+|new-[a-z0-9-]{1,40})$`.
2. `seen.capture` is the `path` of a row of `<A>/captures.jsonl` (`manual_evidence._jsonl`) for some `A` in
   `manual_capture.attempts_of(manual_capture.case_root(task, "settle-" + place))`, AND that row's `content_hash` equals the sha256 of the file's
   bytes NOW; `seen.quote` stands in it (`manual_evidence._quote_in(task, {"path": capture}, quote)`). Required for `bug`, `not_a_bug`,
   `requirement_silent`; optional for `impossible` (a place the stand could not show may have no capture; when given it is checked the same way).
   INVARIANT: a receipt measured on other bytes never counts — another place's walk, a file the role wrote by hand, a capture changed after it was
   recorded. Captures of `walk_session.py` (U0) and of `manual_capture.py ui|http --case settle-<place>` share this one root (§3.6), so an API place
   is answered with an `http` capture (fix 12, E2).
3. `requirement`: `id` is an R of `contract.register_rows` (E1.14: register unreadable -> refused with "the register cannot be read: <why>; answer
   with `question`, `person`, `requirement_silent` or `impossible`"); `quote` stands in that row's `requirement` (whitespace squashed). F-D (a):
   for `answer: bug`, the R must NOT be in `contract.unconfirmed_requirements(register_text, questions)`, door: "that requirement has no confirmed
   source (derived from code or a test): answer `requirement_silent` with your question, or cite the person's words (`person`) or their settled
   question (`question`)".
4. `question`: reused, not re-implemented — `bug_records._oracle_problems(task, {"oracle": {"question": id, "quote": quote}}, "", questions, register)`
   (`bug_records.py:596-617`: `_confirmed` + the quote in the answer or the chosen reading) returns `[]`.
5. `person` (fix 6): `id` is a task-relative path under `state/words/` naming a file; `--dispatch` is given; the controller record of that
   dispatch (`controller.Controller(task).state()["dispatches"][dispatch]`, its request read through `Controller._original_request`) carries
   `person_words: true` AND its `reason` equals `person_words.read(None, <id path>, "--words")` byte for byte (F13: the controller stored exactly
   that file's text); `quote` (squashed) stands in that text. F-D NEVER refuses `person`. A dispatch that is no person-words rework -> refused,
   door: "this dispatch carries no person's words; cite `requirement`, `question`, or answer `requirement_silent`". INVARIANT: a `person` source is
   only ever a person's own recorded words that reached THIS dispatch; a file the role wrote under `state/words/` is not the `reason` of its
   controller record, so it never counts.
6. `none`: legal for `not_a_bug`, `requirement_silent`, `impossible`; refused for `bug` (FR-58).
7. Per answer: `requirement_silent` needs a non-empty `question`; `impossible` a non-empty `why`; `not_a_bug` a non-empty `why` and `seen.quote`;
   `bug` a `draft` naming an existing file of `draft_listing` whose `place_of_draft` is this `place` (rule (4) `draft-<stem>` included).
8. A dispatch that is an investigation pass (`controller.s7_part_of(record) == "investigation"`) -> refused, door: "an investigation records
   through `investigation_probe.py record`; the places are the triage's" (fix 8).

`_refuse(problems)` (ONE raise site) turns the list into exit 2 with every line's door. `write` adds, BEFORE anything is written: the place is in
`places()` or is `new-<slug>` (E1.10); a second write for the same place needs `--replace` (E1.9); the register-line rule below can be
satisfied (a withdrawn chain cannot be reopened, F3 :344-349).

**What `write` writes, in this order (fix 2 order rule):** (1) `evidence/place-answer-<id>.json` atomically — the answer plus, set by code,
`writer: "place_answers.py"`, `written_at`, `dispatch`, `replaces` (the old file's sha256 on `--replace`); (2) the register line of the answer
through `exploratory_findings.append` (table below). If (2) refuses (a ValueError of `append`: `pipeline.json` unreadable, an evidence ref,
the chain rule), the record is KEPT, the CLI prints the refusal whole and exits 2, and the place reads `carrier missing` (§3.4) until a later
`write --replace` lands a line; a findings register that is not installed (`investigation._writer()` returns None) -> the record stands, the CLI
prints "the findings register is not installed; the answer is kept in <path>", exit 0, and the place reads `carrier missing` (P1: the factory
does not stop; the gap line at the close cannot be written either, so the scribe line names it).

**The register line per answer (every field `append` requires, F3):**

| answer | line | op |
|---|---|---|
| `requirement_silent` | `kind: unresolved_question`, `title` = the place title, `statement` = `seen.quote`, `why_not_a_bug` = "the requirements are silent on this; the person who decides the expected behaviour answers it", `question` = the answer's `question`, `owner_role` = `investigation.OWNER_WORDS` (`investigation.py:54`, one spelling), `oracle_status: owner_question`, `refs` = [the R hint, the case when the place has one], `evidence_refs` = [the record path], `origin` = `{dispatch: <--dispatch>, target: <place id>}`, `by` = `<--dispatch>` | `add` when the target has no chain; `correct` of the ACTIVE line when it has one (the investigation's `project` line, a gap line of `close_unsettled`, the analyst's own earlier line), `corrects.reason` = "the analyst settled this place: requirement_silent" |
| `not_a_bug` (fix 10) | `kind: observation`, `statement` = `seen.quote`, `why_not_a_bug` = the answer's `why`, the rest as above (no `question`) | as above |
| `impossible` | `kind: coverage_gap`, `missing_prerequisite` = `why`, `statement` = `seen.quote` or "the stand could not show this place", `why_not_a_bug` = "the analyst could not check it on the stand", the rest as above | as above |
| `bug` | NO line (the register excludes `bug`, `exploratory_findings.py:55`); a `--replace` to `bug` WITHDRAWS the active line of the place (`op: withdraw`, reason "the analyst answered bug; the draft carries it"), so gate B never asks a question the analyst withdrew (critic D6) | `withdraw` |

A `--replace` whose new answer needs a line on a chain that was WITHDRAWN earlier is refused before anything is written: "this place's line was
withdrawn when you answered bug; the register keeps one chain per target: answer `bug` or `impossible`… — or record the question under a new place
`new-<slug>`" (FR-57: a door, never a lock).

**Downstream of `bug` — the draft form per source (fix 3).** The ANALYST writes or keeps a draft whose `reproduction` holds
`{kind: "walk", evidence: "evidence/place-answer-<id>.json", observed: <seen.quote>}` and names it in the answer's `draft`:
- `draft` source: the existing draft.
- `open` place whose case has a triage failure (`contract.triage_failures` key whose names include the target's `case`: a manual check
  `inconclusive`/unprepared, an observation): a TRIAGE-ROAD draft (`case`, `triage_ref` = that failure's instance@attempt) resting on the analyst's
  APP_BUG triage row for it — the triage row is owed anyway (`s7_unbound`, `story_run.py:12622-12635`).
- `register` place, or an `open` place with no triage failure: the CODE-READING form — `oracle` = the register R (requirement form, F5: the row says
  `contradicts: <fact id>` — true by construction for a `register` place) or a settled question; `fact` = the S1 fact the row cites, or a code place
  `{path, line, quote}` the analyst found; `check_state: not_executed`, whose meaning U2 rewrites to "no factory TEST ran; a walk may be its
  receipt" (the comment `contract.py:1878-1880` and the refusal text `bug_records.py:658-660`).
- An `open` place with no triage failure, no contradicting register row and no settled question has NO legal draft form today: fork **F-J**. Until
  the Lead answers, the analyst's `bug` answer there is still written (the record stands), the place reads `carrier missing` with why "no draft
  form carries this bug", and the close writes that gap (§3.4) — the suspicion reaches the report as a named gap, never silently.

### 3.3 The walk receipt in the bug's step (U2)

`contract.BUG_REPRODUCTION_KINDS` += `"walk"` (and its mirror in `handoffs/vocabulary.yaml`, held equal by the existing test).
`bug_records._walk_receipt_problem(task, draft_name, draft, entry)` -> `(code, detail)` or `("", "")`:
1. `entry.evidence` is `evidence/place-answer-<id>.json` (the existing `_evidence_problem`, `bug_records.py:721-735`: a non-empty file under
   `evidence/`); it parses as an object; `writer == "place_answers.py"`;
2. `place_answers.answer_problems(task, record, dispatch=record.get("dispatch"))` returns `[]` — the ONE judge of an answer (AR-13), imported inside
   the function (`place_answers` imports `bug_records`; a late import breaks the cycle, the codebase's pattern, e.g. `bug_records.py:598`);
3. `record.answer == "bug"`; `record.draft == draft_name`; `place_answers.place_of_draft(task, draft_name, draft, ...) == record.place`.
Codes (closed words a person may read): `R_WALK_RECORD` "the walk record cannot be read", `R_WALK_ANSWER` "the walk did not say bug, or its
answer does not stand", `R_WALK_PLACE` "the walk was of another place".

**POSITION, replacing t-1986's skip rule (fix 5).** The two draft-wide facts of `reproduction_problems` are now applied per entry kind:
- non-`walk` entries: EXACTLY as today (`bug_records.py:776-790`); a failing fact voids every non-walk entry;
- `walk` entries: the APP_BUG-row fact is skipped ONLY when `is_code_reading(draft)` (no triage row by construction); a draft with a
  `triage_ref` keeps it. The current-red fact is skipped ONLY when the draft is code-reading OR its triage key names a failure of kind `manual`
  or `observation` in `contract.triage_failures(report)` (no `current_results` row by construction, F6); a `result`-kind draft keeps it.
INVARIANT: a `fresh_data_rerun` / `own_script` entry is judged byte-for-byte as today; a walk receipt never lifts a draft other than the one its
record and `place_of_draft` name, never one whose record does not stand, and never a triage-road draft whose own row is not APP_BUG.
ERROR DIRECTION (a reused function in a more consequential role: the step now rests on a role's walk): may leave `unconfirmed` a draft a walk
did show (cost: the report says "unconfirmed" — the safe side); never lifts one without a record that passes `answer_problems` now. Adversarial
inputs that must stay `unconfirmed`: a record the role wrote BY HAND with `expectation.source: none` (void by rule 2); a hand-written record with
a capture path that is in no `captures.jsonl` of the place's root (void); a capture whose bytes changed after the recorder hashed it (void: the
row's `content_hash` no longer matches); a record naming another draft, or a draft of another place (`R_WALK_PLACE`); an observation draft whose
own triage row says `NO_DEFECT` and a walk saying `bug` (void: APP_BUG kept for a triage-road draft); a record whose `answer` is
`requirement_silent`; evidence outside `evidence/` (existing `R_OUTSIDE`).
**What the marker is and is not (the Lead's "who wrote the file").** `writer: "place_answers.py"` is set only by `write`, but it is NOT a
security boundary: a role can type it (F8, no write log exists). The data check that makes forgery pointless is rule 2: a hand-written record
that passes `answer_problems` now carries exactly the claim `write` would have accepted, resting on a capture the recorder hashed in its own
index. The marker only names the writer for a person reading the file; the check stays a DATA check and never a judgment of the walk.

`reproduction_words` gains the phrase for kind `walk`: "the analyst walked it on the stand" (one function for every surface, FR-10).

### 3.4 Settled, unsettled, and what happens to a place nobody settled (U1, U3a)

`place_answers.settled_answer(task, place) -> (record | None, state, why)` — the ONE predicate "this place is settled" (AR-13), read by
`unsettled`, `list`, the scribe line AND `investigation.unresolved_targets` (iv). States:
- `settled`: a record exists, `answer_problems(record, dispatch=record.dispatch) == []`, and its CARRIER exists — for `requirement_silent` /
  `not_a_bug` / `impossible` an ACTIVE register line of the place's chain recorded by `record.dispatch` with the kind of the table in §3.2; for
  `bug` a draft (the record's `draft`) whose `confirmation_of` is `reproduced_by_factory` with `walk` among its kinds;
- `carrier missing` (why: the append refusal / "no draft carries this walk receipt" / "no draft form carries this bug" / "the findings register
  is not installed");
- `conflict` (why): a valid record `not_a_bug` or `requirement_silent` while a joined draft still stands `unconfirmed`;
- `invalid` (the record no longer passes `answer_problems`, e.g. its capture changed) — treated as `open` with why;
- `open`: no record.

`unsettled(task)` = every place not `settled`. Code never settles a place by its verdict word (AR-29).

**Fix 1 — resolution (iv) in `investigation.unresolved_targets`** (U1 owns `investigation.py`: `unresolved_targets` only): after (i)-(iii) found
no resolution, a target whose id is a place id with `place_answers.settled_answer(task, id)[1] == "settled"` is resolved, why
`"settled by <dispatch>: <answer>"`, and is ALSO listed under a new key `out["settled"]` (the whole target dict) so that `places()` keeps listing
it as a settled place (the `open` source = `unresolved` + `settled`). INVARIANT: a place the analyst settled is never re-investigated and never
gapped "not investigated" (`decision` sees it resolved -> no pass; `close_gaps` skips it as `resolved`, `investigation.py:491-495`). ERROR
DIRECTION: a record that does not stand, or whose carrier is missing, resolves nothing — the target keeps the investigation road. `place_answers`
is imported inside the function; an exception of it resolves nothing and is one `context` line ("the analyst's answer could not be read").
`settled` is `[]` for a story with no record. The F-A (a) rationale now holds as stated: the investigation stays read-only for WHAT IS LEFT.

**Who is told (no stop of the factory, no code closing the role's obligation):**
1. **The analyst, before the work** — the brief lists every place and says an answer is owed (U3a for the fresh triage, U3b for every S7 triage
   dispatch); `place_answers.py list --task-root T` prints each place with its state.
2. **The report and gate B, as a gap** — `close_unsettled(task, why)` at the closers (§3.6 POSITION): for each unsettled place of source `draft`
   or `register` (and, for an `open` place, ONLY in the states `conflict` / `carrier missing`, because a plain `open` target keeps the
   investigation road — one place, one gap line), ONE register line: `kind: coverage_gap`, `title` = place title, `statement` = "the run left
   this suspicion unchecked: <refs summary ≤ 300 chars>", `missing_prerequisite` = the text of the state (below), `why_not_a_bug` = "a suspicion
   nobody settled on the stand; it is neither a bug nor cleared", `evidence_refs` = [the draft file, or `work/requirements-register.md`, or the
   record], `origin` = `{dispatch: "S7", target: <place id>}`, `by` = `code:place_answers.close_unsettled`. `add` with no chain; `correct` of the
   active line otherwise; nothing when the active line already says the same `missing_prerequisite`. A draft stays as it is beside the gap.
   `missing_prerequisite` texts (data, `references/place-answers.json`):
   - state `open` / `invalid`: "not settled by the analyst — <why>", `why` one of the FIVE `gap_reasons` (fix 9), chosen by the rule in §3.6;
   - state `conflict`: "the analyst's answer and its own records disagree: <why>" — never "not walked" (fix 9, B2);
   - state `carrier missing`: "the analyst's answer did not reach its record: <why>".
3. **The tier above** — the S8 scribe gets one line (U3a, `stage_S8` awaiting block): "Places of S7 (<n>): settled <k> — <id>: <answer>
   (expectation: <source> <id>); …; not settled <m>: <id> (<state>)…" (≤ 1 500 chars, then "[and <n> more: place_answers.py list]"); returning
   the triage for them is the scribe's judgment (X7-6b). This is where `expectation.source` reaches a reader beside `answer_problems` (fix 10).
P22: a place only a person can decide is ANSWERED `requirement_silent` (a question at gate B through the register), not left; the conductor is
not called for it.

**The road after a person's gate-B word (fix 6, B1).** A `requirement_silent` line at gate B -> the person writes `bug` (addressable: the
`bug` executor; not addressable: the conductor's rework) -> ONE S7 rework whose controller record holds the person's words (F13) -> the reworked
analyst walks or re-reads its capture and writes `--replace` with `answer: bug`, `expectation: {source: person, id: <the words file>, quote}`
— accepted (F-D never refuses `person`); `write` withdraws the question line (§3.2); the draft form per source carries the receipt. A person's
`intended` corrects the line to `person_confirmed` (driver, unchanged) — the place stays settled by the analyst's `requirement_silent` record
(its line is active, F3); nothing re-asks it.

**Re-entry after a scribe reject (X7-6b rework, C5).** A new analyst dispatch sees `list` with every state; a place gapped at the first close
carries an active `code:place_answers.close_unsettled` line; a new valid `write` CORRECTS that line (§3.2 table), so the stale "not settled"
gap leaves the report; at the second close, `close_unsettled` writes nothing for settled places, nothing for an unchanged text, one `correct`
for a changed one.

### 3.5 The charter — experience, scoped by dispatch purpose (U4, fix 8)

Package English; no principle numbers, no `AC`, no "must run"/"Step"; no form token in Techniques. `test_charters_s5_s9.py` pins (t-1986 S10).
- "Where bugs hide", after :43 ("A green manual check that carries an oddity"), ADD (≈ 260 B):
  > - **A suspicion left as the run left it.** A bug drafted from reading, a doubt the runner wrote down, a code place that contradicts a requirement: each stays a guess until someone does the thing on the stand. Most guesses either fall apart or turn out to rest on an expectation nobody stated.
- "Techniques", REPLACE :53 ("**Reproduce through an independent route.** Your own request against the same shape, not the test's own output.") WITH (≈ 640 B):
  > - **Find out the truth on the page.** In a triage, every suspicious place nobody has confirmed is walked before you leave it: do the thing a person would do, one step or a short obvious run at a time, look, decide the next. Through an independent route: your own steps or your own request, never the test's own output. Then say which it is: a bug, with the requirement it breaks; not a bug, with the words you saw; or a place the requirements are silent on, which is a question for the person who decides and never a bug. Name where your expectation comes from beside the answer; an expectation the factory derived itself is no requirement. A place the stand cannot show is said so, with why.
- "Techniques" :55: DELETE "A red with no field is different: the value was never received, so it is judged by the response shape, not by the
  control experiment." (≈ 150 B; the rule stays in Tools, pinned by `test_case_role_twins.py:65` — critic N2 confirmed).
- "Tools" :66: DELETE "`manifest_view.py` - a case's manifest slice; `env_probe.py` - the stand." (≈ 80 B) and ADD (≈ 200 B):
  > - `place_answers.py list|write` - the places to settle and your answer per place (keys on your key page); the walk commands your triage brief names (`walk_session.py step|look|final`, or `manual_capture.py ui|http` with `--case settle-<place>`).
- **The FR-10 clash (E1) closed by purpose:** the bullet starts "In a triage"; `investigation_lines` (U3a owns: `investigation_lines`, that line
  only) gains, right after the honesty line :12959-12960: "The places of `place_answers.py list` were the triage's to settle; you do not walk the
  page for them and do not answer them." `place_answers.py write` refuses an investigation dispatch (§3.2 rule 8) — data, not discipline.
- Net ≈ +730 B ≈ +185 tokens — **estimate**; paid only if the measured load sits ≥ that under 17 753 (`role-load.json:19`) / 16 145 (:33);
  otherwise F-I (cut :81 "Settle it yourself first: …", ≈ 170 B) is taken; if still above -> STOP and report (E4.1). Inside the ratchet.

### 3.6 The walk: today's recorder now, the walk session later (U0, U3a, U3b)

**One root for every capture of a place (fix 12).** `manual_capture.case_root(task, "settle-" + <place id>)` =
`work/evidence/manual/settle-<place id>/aN/` (F9). Today the analyst captures there with `manual_capture.py ui --case settle-<place id>
--steps-file F` and `manual_capture.py http --case settle-<place id> …` (F-M: the analyst is given these two commands for `settle-` cases);
after U0 the walk session's lane `settle` opens its item attempts under the SAME root, so a place walked partly by `http` and partly by the
session is one root, one index, one rule. (t-1986's `evidence/settle-<place>/aN/` is dropped: no recorder road could write an `http` capture
there.) The control lane keeps `evidence/control-<label>/aN/` (U0; the root `triage_control_problems` receives is pinned by test, S9 of t-1986).

**The stand lease and the lifetime of an S7 lane (fix 4, C1, G4) — U0, after N1a+N2 are merged; N1a's text and code are NOT changed.**
- `walk_session.py open --place case|settle|control` (default `case`; N1a's behaviour is `case` exactly). For `settle` and `control` the server
  takes the stand lease PER page-touching request (`item`, `step`, `look`, `final`, `close`, and the start/end probe), through the same
  `manual_capture._hold_stand` helper (F11), job `walk:<W>`, waiting at most `walk_session.request_lease_wait_s` (data, 60) and otherwise
  answering exit 3 `{"status": "stand_busy", holder}` with the door "the stand is in use by <job>; call again when your own run has ended".
  Between requests the lease is free, so the analyst's `run_suite.py --request`, `red_sandbox.py --diagnostic` and `manual_capture.py http` calls
  are never blocked by its own session. INVARIANT: no lease is held while no request runs; two page-touching requests never overlap (N1a's busy
  lock, unchanged).
- For `settle` and `control`, `idle_s` does not apply (data `walk_session.idle_places_exempt: ["settle","control"]`): the session lives for the
  dispatch; the parent check (N1a E1.7: the driver process that opened it) still ends it; `max_s` 5 400 unchanged.
- What changes in N1a's DATA: two keys added to the `walk_session` object of `manual-capture-steps.json` (`request_lease_wait_s`,
  `idle_places_exempt`). In its CODE: `open`'s argument list, the lease site in `serve`, the idle timer — all owned by U0, after N1a and N2.
  **Must it land before N1a's remainder is merged? No.** N1a has no `--place` (F12), so nothing in N1a or N5s (S6 `case` lanes) depends on it; the
  builder writing `walk_session.py` now keeps today's text. U0 restructures the lease site afterwards; the one risk (N1a holding the lease in one
  `with` around the serve loop) is U0's to move, with `test_case_lane_lease_unchanged` pinning the `case` lane byte-for-byte.

**Session failure mid-dispatch (G4).** `step` exits 3 on a `dead`/`closed` session (N1a E1.3). The brief's door (U3b): "your walk session ended:
`walk_session.py open --task-root T --walk <W> --place settle --items free` reopens it for the same walk (N1a E1.16); if it cannot open, capture
with `manual_capture.py ui|http --case settle-<place>`, or answer `impossible` with why 'the walk session could not be opened'". The role row of
`walk_session.py open` for `qa-failure-analyst` is U0's (role-commands). (F38 of t-1957: a server opened from a role's Bash may not survive the
call — then the `manual_capture` road is the door; nothing locks.)

**Brief lines** (`Driver.s7_place_lines(dispatch)`, U3a; moved to `run_role` by U3b): "Places to settle (<n>):" then one line per place
`<id> | <sources> | <state> | <title> | expectation named by the record: <hint or none> | where: <refs ≤ 300 chars>`; the four answers and the
four sources in one line; "capture each place under its own case `settle-<place id>`: `manual_capture.py ui|http --case settle-<place id>`"
(U3a) / "the walk session `<W>`: `walk_session.py step|look|final`, one step or a short obvious run per call" (U3b, when the session opened);
the commands `place_answers.py list|write --dispatch <this dispatch id>`. More than 40 places -> the first 40 by the list order and "[and <n>
more: place_answers.py list]" (limit at 40 runs whole; 41 cuts). A list not computed whole -> the line says so (§3.1).

**POSITION at the closers (U3a), with its mechanism (C4).** In `s7_close`, and inside `stage_S7` at `s7.no_failures` and `s7.pretriaged`, ONE
call `self.s7_close_places(why)` (-> `place_answers.close_unsettled`) runs BEFORE `s7_investigation_gate`. INVARIANT: a place is never both a
settle gap and an investigation gap, and `finalize_task` / the scribe read a register where every place is settled or gapped. It holds because
(1) `close_unsettled` never writes a plain `open` place, and (2) `investigation.is_code_line` matches only the prefix `code:investigation.`
(`investigation.py:36, :79-80`), so `close_gaps` and `project` treat a `code:place_answers.close_unsettled` line as a role line and skip its chain
(:321-323, :499) — `by` must stay OUTSIDE that prefix, pinned by `test_gap_line_prefix_outside_investigation`.

**The gap reason chosen by the driver (fix 9, G1)** — `references/place-answers.json` `gap_reasons`, FIVE texts:
1. "the analyst's dispatch ended without an answer for this place" — `s7_close`, and the default (true whether or not the dispatch was told);
2. "the stand could not be reached" — `s7_close` when `self.state["s7_walk"][<last S7 triage dispatch>]["failed"] == "stand"` (written by U3b);
3. "the walk session could not be opened" — the same record with `"session"`;
4. "the analyst was not dispatched: no failure to triage" — `s7.no_failures` (F-F (a));
5. "the analyst was not dispatched: every failure had a state the run recorded" — `s7.pretriaged` (no analyst runs there, `story_run.py:12412-12422`).
`close_unsettled` refuses any other text (ValueError naming the five), as `close_gaps` does (`investigation.py:478-479`).

**U3b — the one join point of every S7 triage dispatch** (after N5s, U0, U3a): in `run_role` (F14), when `stage == "S7"`, `role ==
"qa-failure-analyst"` and the dispatch record is not an investigation (`controller.s7_part_of(...) != "investigation"`): (a) `lines +=
self.s7_place_lines(dispatch)` right before `lines += list(extra)` (:2842) — and U3b REMOVES U3a's append from `stage_S7` so there is one site;
(b) only when the role will actually run (no saved result, :2851), `self.s7_settle_session(dispatch)` opens `walk_session.py open --place settle
--walk <dispatch> --items free` and records `self.state["s7_walk"][dispatch] = {"state": "ready"}` or `{"failed": "stand"|"session", "why"}`;
(c) a `finally` around `run_claude` (:2854) closes it. INVARIANT: every triage dispatch — fresh, scribe-reject rework, seam rework — gets the same
lines and session; an investigation never gets either; no session outlives its dispatch by more than N1a's `parent_check_s`.

### 3.7 Expected numbers and the honest ceiling (Q2, decided)

Per place ≈ 3–6 min, ≈ 12–20 tool calls (t-1957 §3.10 (2)) — **estimate**; per call of today's `manual_capture.py ui` a browser start
(t-1957 F8) — slower, **estimate** (not measured for S7). Places per run: the owner says 3–5; arm B would have had 7 code-reading drafts plus the
open targets — **estimate**. **No cap as a number (Q2, decided by the Lead):** what bounds a dispatch is the walk session's `max_s` (5 400 s =
90 min, t-1957 §3.2) and the dispatch's own life — at 3–6 min per place after the triage, about 15 places fit (**estimate**, the critic's
figure); a session that reaches `max_s` can be reopened once per need (E1.16, same W). Places the dispatch did not reach are `open` at the close
and get the gap line "the analyst's dispatch ended without an answer for this place" — named in the report, at gate B, and in the scribe's line;
never silent.

---

## §4 Nodes (written for a weaker model; directions chosen; forks of §6 taken at their recommendation until the Lead answers)

General: fast test files only; `test_bug_records.py`, `test_investigation.py`, `test_investigation_probe.py`, `test_story_run_s7*.py` are in
`slow_tests.json` (t-1986 N3) — CI only, never run locally, never waited for. Witnesses run from `D:/ws1/wt-fbfix`, each also
`python -B ai-packages/qa-factory/scripts/selftest.py --lang` (FR-30). Every package commit carries `architecture:` and `judgment:` lines.
Hot-file functions are named; nothing else in that file is touched.

**Order.** START NOW (no walker code, no dependency on unmerged t-1957 work): **U1** -> then **U2** ‖ **U3a** (disjoint files). WAIT FOR t-1957:
**U0** after N1a + N2 merged; **U3b** after N5s + U0 + U3a merged (`очередь: N5s → U3b` on `run_role`, PROJECT.md «Командная работа» 3); **U4**
after N4 merged (measure role-load after N4). **U2b** waits for the Lead's answer to F-J. Shared files: `artifact-writers.json` U1 then U0;
`role-commands.json` U1 then U0; `judgment-census.json` U1 only; `investigation.py` U1 only; `contract.py` and `bug_records.py` U2 only;
`story_run.py` U3a then U3b; `walk_session.py` / `manual-capture-steps.json` U0 only.

#### U1 — `place_answers.py`: places, answer, settled, gaps; resolution (iv) — START NOW
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\place_answers.py` (new: `places`, `place_of_draft`, `answer_problems`, `_refuse`, `write`, `settled_answer`, `unsettled`, `close_unsettled`, CLI `list|write|close-unsettled`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\investigation.py` (`unresolved_targets` only: resolution (iv) and the key `settled`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\place-answers.json` (new: `answers`, `sources`, `gap_reasons` (the five texts of §3.6), `state_texts` (conflict, carrier missing), `record_root` "evidence/place-answer-", `capture_case_prefix` "settle-", `terminal_fields` ["written_at","walk","replaces"], `brief_places_max` 40, a `note` per closed list)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\artifact-writers.json` (key `evidence/place-answer-*.json` writer `place_answers.py`; `work/evidence/manual/` machinery note: `settle-*` folders are written by `manual_capture.py` and, after U0, `walk_session.py`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\role-commands.json` (rows `place_answers.py write` roles `["qa-failure-analyst"]` with `input`/`verify`; `place_answers.py close-unsettled` roles `["conductor"]`; per F-M (a): `qa-failure-analyst` added to `manual_capture.py ui` and `manual_capture.py http`, their `input` text naming "an S7 analyst captures only with `--case settle-<place id>`")
`D:/ws1/wt-fbfix\ai-packages\qa-factory\handoffs\` the analyst's key page (the file `references/inject-map.json` names for qa-failure-analyst's keys; add the answer keys; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (rows `place_answers.py::answer_problems` xref non-blocking, `place_answers.py::_refuse` shape blocking, roles `["qa-failure-analyst"]`, owner data; `blocking_per_role.qa-failure-analyst` 131 -> 132)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_place_answers.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_investigation.py` (one twin test only: `test_settled_open_target_not_reinvestigated`; CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1991-u1.md` (new)
**non-goals:** the walk session (U0); the draft's step and `reproduction_problems` (U2); the driver (U3a/U3b); any other function of
`investigation.py`; any list of what is suspicious beyond §3.1; judging whether an answer is true.
**behaviour:** §3.1, §3.2, §3.4 exactly. Readers reused, never re-implemented: `bug_records.draft_listing`, `confirmation_of`, `step_facts`,
`_oracle_problems` (question form only), `is_code_reading`; `investigation.load_budget`, `open_targets`, `investigation_targets`, `OWNER_WORDS`,
`_writer`; `contract.register_rows`, `REQ_ID_RE`, `unconfirmed_requirements`, `triage_failures`, `evidence_ref_issue`, `artifact`;
`branch_accounting.code_says_contradicts`; `question_register.load`; `manual_capture.case_root`, `attempts_of`; `manual_evidence._jsonl`,
`_quote_in`; `person_words.read`; `controller.Controller(...).state()`, `Controller._original_request`, `controller.s7_part_of`;
`exploratory_findings.append`, `read`, `chains_of`; `install_paths.sha256_file`. Imports of `bug_records`, `investigation`, `controller` that could
cycle are made inside the functions.
**edges (each with its invariant):**
- E1.1 EMPTY: no place -> `places == []`, `list` prints "Places to settle: none in this run". INVARIANT: "none" only when every source was read.
- E1.2 each unreadable source of §3.1 (draft folder via `draft_listing`, a draft that does not parse, the register table refused, the budget
  refused, `investigation_targets` raising) -> `unreadable` names it; `list` prints "could not be computed whole". INVARIANT: an unknown never
  reads as "no place" (AR-28).
- E1.3 ids (fix 7): a draft written AFTER `case-C` was listed joins `case-C` (rule 2); a code-reading draft for R-12 deleted after its answer ->
  `req-R-12` stays, still settled by its record. INVARIANT: a place id never changes during a run; a settled place never reappears unsettled
  because a draft came or went.
- E1.4 a draft whose `confirmation_of` word is `reproduced_by_factory` / `confirmed_by_*` is no `draft` source. INVARIANT: the step is read only
  through `confirmation_of` (AR-13); a word the role typed without a receipt is `unconfirmed` and IS a place.
- E1.5 `bug` with `expectation.source: none` -> refused: "a bug needs the requirement it breaks, a settled question or the person's words; with
  none, answer `requirement_silent` with your question". INVARIANT: code is never the oracle (FR-58).
- E1.6 F-D (a): `bug` on an R in `unconfirmed_requirements` -> refused with the door of §3.2 rule 3. Error direction: may refuse a bug a person in
  fact confirmed in words the register does not link (cost: the role cites `person` or `question`); never accepts `bug` on an R that set lists.
  Adversarial inputs that stay refused: `r-12` / `R-012` (not the register's R: "not in the register"); a `question` id that exists but is
  open/deferred (`_confirmed` false); a requirement quote not in the row's text.
- E1.7 `seen.capture` outside `case_root("settle-"+place)`'s attempts, or not a `path` of that attempt's `captures.jsonl`, or its bytes no longer
  match the row's `content_hash`, or `seen.quote` not in it -> refused naming the place's root and attempts. INVARIANT: a receipt measured on
  other bytes never counts. A place with no attempt yet -> "capture first: `manual_capture.py ui|http --case settle-<place>`".
- E1.8 `requirement_silent` without `question`; `impossible` without `why`; `not_a_bug` without `why` or `seen.quote`; `bug` without `draft`, or a
  `draft` that is no file of `draft_listing`, or whose `place_of_draft` is another place -> refused. INVARIANT: every answer carries its evidence,
  its reason and its carrier.
- E1.9 a second `write` without `--replace` -> refused naming `--replace`; with it -> replaced, `replaces` = old sha256; the register line follows
  the table (correct / withdraw). INVARIANT: one active answer per place; a change of mind is visible; gate B never asks a withdrawn question.
- E1.10 an unknown place id -> refused, door `place_answers.py list`; `new-<slug>` accepted; `new-` with a slug outside `[a-z0-9-]{1,40}` -> refused
  (at 40 chars accepted, 41 refused). INVARIANT: the role is never locked out of recording its own suspicion (AR-2).
- E1.11 `append` refuses after the record is written -> record kept, exit 2 with the refusal whole, state `carrier missing`. INVARIANT: an answer
  never silently fails to reach the report or gate B (AR-27); presence of a record alone never settles a place.
- E1.12 `--replace` needing a line on a withdrawn chain -> refused before anything is written, door of §3.2. INVARIANT: the register's one-chain
  rule is kept and the role has a door.
- E1.13 `close_unsettled` twice with the same why -> no second line; with another why -> one `correct`; a plain `open` place -> nothing; an
  `open` place in `conflict` / `carrier missing` -> its gap; `why` outside the five -> ValueError naming them. INVARIANT: one active line per
  place; a plain `open` target keeps the investigation road.
- E1.14 the register unreadable inside `answer_problems` -> `requirement` refused with "the register cannot be read: <why>" naming the doors
  `question`, `person`, `requirement_silent`, `impossible`. INVARIANT: an unknown register never accepts and never locks.
- E1.15 `person`: a dispatch with no `person_words`, a file outside `state/words/`, a file whose text differs from the record's `reason`, a quote
  not in it -> refused, each with its door; an unreadable controller state -> refused "where the story stands could not be read". INVARIANT: only
  the person's own words that reached THIS dispatch count; F-D never refuses them.
- E1.16 resolution (iv): a settled `open` place -> in `resolved` and `settled`, not in `unresolved`; a record with `carrier missing` or that does
  not stand -> stays `unresolved`; `place_answers` raising -> nothing resolved, one context line. INVARIANT and error direction as §3.4.
- E1.17 a `write` from an investigation dispatch -> refused (rule 8). INVARIANT: the investigation stays read-only and never answers a place.
- E1.18 TEMPORAL (within the run): a place appearing after the triage started (a draft written in the dispatch) is in `places` at the next call
  and seen by `close_unsettled`. INVARIANT: a draft written in the dispatch is never missed by the close. TEMPORAL (merge): before U2 is merged a
  `bug` answer's draft receipt of kind `walk` is refused by today's `reproduction_problems` (`R_KIND`) -> the place reads `carrier missing` with
  why "no draft carries this walk receipt" and is gapped — honest in both worlds; after U2 it settles.
**DoD — `test_place_answers.py` (fast; a temp task with fixture drafts, register, S6 handoff rows, question register, captures written as
`manual_capture` writes them — `captures.jsonl` rows with `path` and `content_hash` under `work/evidence/manual/settle-<id>/a1/` —, a
`pipeline.json`, and for `person` a controller state built the way `test_investigation.py`'s `_accepted_s6` fixtures build one):**
`test_places_is_a_join_only`, `test_empty_says_none`, `test_unreadable_source_never_none` (one case per source of E1.2),
`test_draft_listing_unreadable_folder_named`, `test_contradiction_read_by_code_says_contradicts`, `test_deleting_code_reading_draft_keeps_place_settled`,
`test_id_stable_when_draft_written_for_open_place`, `test_two_places_never_merged`, `test_reproduced_draft_not_a_place`,
`test_role_word_without_receipt_is_a_place`, `test_bug_without_source_refused`, `test_bug_on_unconfirmed_requirement_refused`,
`test_unsettled_question_refused`, `test_bug_on_person_words_after_gate_b_accepted`, `test_person_quote_not_in_words_refused`,
`test_person_file_not_the_dispatch_reason_refused`, `test_capture_of_other_place_refused`, `test_capture_not_in_index_refused`,
`test_capture_bytes_changed_refused`, `test_http_capture_of_place_accepted`, `test_quote_not_in_capture_refused`, `test_answer_keys_required`
(E1.8 table), `test_second_write_needs_replace`, `test_new_place_accepted_and_slug_boundary` (40 / 41), `test_requirement_silent_line_fields`
(every field of §3.2, `append` accepts), `test_not_a_bug_writes_observation_line`, `test_impossible_writes_gap_line`,
`test_write_corrects_existing_chain`, `test_replace_withdraws_question_line`, `test_withdrawn_chain_replace_refused_with_door`,
`test_append_refusal_keeps_place_unsettled`, `test_register_not_installed_keeps_record`, `test_conflict_draft_stands`,
`test_conflict_gap_text_is_not_not_walked`, `test_close_unsettled_once_per_place`, `test_close_unsettled_skips_plain_open_targets`,
`test_close_unsettled_unknown_why_refused`, `test_gap_line_prefix_outside_investigation` (`investigation.is_code_line` False on the line),
`test_stale_gap_corrected_by_later_answer`, `test_settled_open_target_resolved_iv`, `test_carrier_missing_resolves_nothing`,
`test_register_unreadable_names_doors`, `test_investigation_dispatch_refused`, `test_answer_never_judged_by_words` (two records differing only in
the words of `why` get the same problem list), `test_every_refusal_names_a_door`.
Negative control (shown red once): with E1.5's check removed, `test_bug_without_source_refused` fails; with (iv) removed,
`test_settled_open_target_resolved_iv` fails.
Witness: `python -m pytest ai-packages/qa-factory/scripts/tests/test_place_answers.py ai-packages/qa-factory/scripts/tests/test_artifact_writers.py ai-packages/qa-factory/scripts/tests/test_judgment_census.py -q`
(CI: `test_investigation.py`, `test_role_commands.py`, `test_bug_records.py`). `architecture:` AR-2, AR-13, AR-14, AR-15, AR-20 (raise named),
AR-21, AR-22, AR-23, AR-25, AR-26, AR-27, AR-28, AR-29.

#### U2 — the walk receipt in the bug's step — START NOW, after U1
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\contract.py` (`BUG_REPRODUCTION_KINDS` + `"walk"`; the comment :1878-1880 "where no run spoke" -> "where no factory test spoke; a walk of the analyst may be its receipt"; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\handoffs\vocabulary.yaml` (the mirror of `BUG_REPRODUCTION_KINDS`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\bug_records.py` (`reproduction_problems`, `_walk_receipt_problem` new, `reproduction_words` (the `walk` phrase), the text of the `R_CR_CHECK_STATE` refusal :658-660 ("a code-reading draft exists only where no factory test spoke"); nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_receipt.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1991-u2.md` (new)
**non-goals:** `confirmation_of`'s person words; `code_reading_problems` / `_oracle_problems` rules (F-J, U2b); filing; gate B; `place_answers.py`.
**behaviour:** §3.3 exactly. **edges:** E2.1 POSITIONAL (§3.3): the two facts per entry kind. INVARIANT: every non-walk entry is judged
byte-for-byte as today (`test_bug_records.py` unchanged, CI). E2.2 a record whose `answer_problems` is not `[]`, or whose answer is not `bug` ->
`R_WALK_ANSWER`. E2.3 the record names another draft, or `place_of_draft` differs -> `R_WALK_PLACE`. E2.4 record missing / not JSON / `writer`
absent -> `R_WALK_RECORD`. E2.5 evidence outside `evidence/` -> existing `R_OUTSIDE`. INVARIANT for E2.2–E2.5: the error goes DOWN, and the reason
is a closed word (no path, AR-4). E2.6 TEMPORAL: a draft written before U2 carries no `walk` entry -> unchanged. E2.7 `place_answers` cannot be
imported -> `R_WALK_RECORD` "the walk record cannot be checked". INVARIANT: an unknown never lifts.
**DoD — `test_walk_receipt.py` (fast):** `test_code_reading_draft_lifted_by_walk`, `test_manual_check_draft_lifted_by_walk`,
`test_observation_draft_lifted_by_walk`, `test_walk_on_no_defect_observation_void`, `test_hand_written_record_source_none_void`,
`test_record_capture_not_in_index_void`, `test_walk_capture_changed_void`, `test_walk_of_other_draft_void`, `test_walk_answer_not_bug_void`,
`test_walk_outside_evidence_void`, `test_result_draft_keeps_current_red_fact`, `test_rerun_entry_still_needs_red_now`,
`test_register_place_bug_has_a_draft_form` (a `register` place: code-reading draft, `check_state: not_executed`, walk receipt -> lifted and
`code_reading_problems == []`), `test_words_name_the_walk`, `test_kinds_mirror_vocabulary`. Negative control: with the APP_BUG skip widened to
every walk entry, `test_walk_on_no_defect_observation_void` fails (shown red once).
Witness: `python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_receipt.py ai-packages/qa-factory/scripts/tests/test_place_answers.py -q`
(CI: `test_bug_records.py`). `architecture:` AR-13, AR-22, AR-28, AR-29.

#### U2b — a `bug` on a place with no draft form (F-J) — WAITS for the Lead's answer
Written only after F-J is decided; by recommendation (a): `bug_records._oracle_problems` requirement form also accepts, instead of `code_says:
contradicts: <fact id>`, a walk receipt on the same draft whose record's `expectation` is that `requirement` and stands (§3.3). Owns
`bug_records.py` (`_oracle_problems` only) and a test file `test_walk_oracle.py`; error direction and adversarial inputs to be written with the
answer (P5 of PROJECT.md «Как принимается изменение пакета», item 6(в)).

#### U3a — the S7 driver without the walker: lines, closers, scribe line, investigation line — START NOW, after U1
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`stage_S7`: `told += self.s7_place_lines(None)` after :12432, and ONE `self.s7_close_places(<text 4>)` before the gate at `s7.no_failures` (:12384) and `self.s7_close_places(<text 5>)` before the gate at `s7.pretriaged` (:12415); `s7_close`: ONE `self.s7_close_places(self.s7_gap_reason())` before :12811; `stage_S8`: inside the `if awaiting:` block :13404-13410, `extra += self.s7_places_scribe_line()`; `investigation_lines`: the one line of §3.5 after :12960; new `s7_place_lines`, `s7_close_places`, `s7_gap_reason`, `s7_places_scribe_line`; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_place_driver.py` (new; `Driver` stubbed as in `test_manual_window.py`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1991-u3a.md` (new)
**non-goals:** `run_role` (U3b, N5s); the walk session; the investigation pass and its rule; repairs; the scribe's verdict.
**behaviour:** §3.4 points 1–3, §3.6 (brief lines without the session, POSITION, gap reasons). `s7_gap_reason()` returns text 1 unless
`self.state.get("s7_walk", {}).get(<last S7 triage dispatch>, {}).get("failed")` names `stand` / `session` (texts 2 / 3; the record exists only
after U3b). Every call into `place_answers` is inside `try`: an exception is ONE printed line and S7 goes on (P1).
**edges:** E3.1 POSITIONAL: `s7_close_places` before `s7_investigation_gate` at all three closers. INVARIANT and mechanism: §3.6 POSITION.
E3.2 `places` raising or returning `unreadable` -> one printed line, the brief says "could not be computed whole", the close still runs
`close_unsettled` on what it read. INVARIANT: an exception of this code never stops S7 and never reads as "none". E3.3 `s7.no_failures` /
`s7.pretriaged` with `register` / `draft` places -> gapped with texts 4 / 5. INVARIANT: a register contradiction never vanishes because no
analyst ran. E3.4 a re-triage (`s7_retriage_once`) or a scribe-reject rework -> the list recomputed; records already written stay valid; a stale
gap is corrected by a later answer (U1). INVARIANT: a settled place is never walked again because the triage restarted. E3.5 the scribe line
over 1 500 chars -> cut with "[and <n> more: place_answers.py list]" (at 1 500 whole). E3.6 TEMPORAL: before U3b, a rework dispatch (seam or
scribe reject, F13) carries no place lines (they come only through `stage_S7`'s `told`); its places get text 1, which stays true. After U3b every
triage dispatch carries them. E3.7 the brief over 40 places -> 40 lines and "[and <n> more …]" (40 whole, 41 cut).
**DoD — `test_place_driver.py` (fast):** `test_close_places_before_investigation_gate` (a stub gate records whether the register already holds
the settle gaps), `test_no_failures_gaps_register_places`, `test_pretriaged_gap_text`, `test_gap_reason_default_and_session_failure`,
`test_places_error_one_line_and_close_still_runs`, `test_brief_names_places_and_answer_keys`, `test_brief_cut_at_40`,
`test_scribe_brief_names_settled_and_unsettled` (incl. the expectation source and the cut at 1 500), `test_investigation_brief_excludes_settle`,
`test_settled_open_place_no_investigation_dispatch` (stub `investigation.decision` input: a settled `open` place -> `none`).
Negative control: the call moved after the gate makes `test_close_places_before_investigation_gate` fail.
Witness: `python -m pytest ai-packages/qa-factory/scripts/tests/test_place_driver.py ai-packages/qa-factory/scripts/tests/test_place_answers.py -q`
(CI: `test_story_run_s7.py`, `test_story_run_s7_live.py`). Critic mandatory (core). `architecture:` AR-10, AR-14, AR-19 (with U4), AR-25, AR-27,
AR-28, AR-29.

#### U0 — S7 lanes of the walk session (`settle`, `control`): roots, per-request lease, lifetime — after t-1957 N1a + N2
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_session.py` (`open`: `--place case|settle|control`; the lease site in `serve` (per request for `settle`/`control`); the idle timer (exempt places); the item root of `settle`/`control`; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\manual-capture-steps.json` (`walk_session.request_lease_wait_s` 60, `walk_session.idle_places_exempt` ["settle","control"], their `does` text)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\artifact-writers.json` (`work/evidence/manual/settle-*`: `walk_session.py` beside `manual_capture.py`; `evidence/control-*/` writer `walk_session.py` — the directory only: NO `evidence/control-*.json` key, nothing writes such a file (fix 13))
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\role-commands.json` (row `walk_session.py open` gains `qa-failure-analyst`, its `input` naming `--place settle --walk <W>` for a reopen)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_places.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1991-u0.md` (new)
**non-goals:** step calls, verdicts, S6 records (t-1957); the `case` lane's lease and lifetime; the answer record (U1); N1b's shared lease mode.
**behaviour:** `case` -> N1a unchanged; `settle` -> item `i` opens attempts under `manual_capture.case_root(task, "settle-" + i)`; `control` ->
`evidence/control-<i>/aN/` resolved exactly as `contract.triage_control_problems` resolves `control.evidence` for its callers (asserted by
test, never assumed); per-request lease and idle rule of §3.6.
**edges:** E0.1 an item id with `/`, `..`, a drive or `__` -> refused through N1a's `_refuse` naming `[A-Za-z0-9._-]+` (N6's
`test_work_evidence_path_refused` maps here). INVARIANT: an attempt never lands outside its root. E0.2 TEMPORAL: the root absent before the first
`item`, created by it; a second open -> next `aN`; captures `manual_capture.py http --case settle-<i>` made earlier are attempts of the same root
(next `aN`). INVARIANT: evidence on disk is never rewritten. E0.3 `--place` unknown -> refused, door lists the three. E0.4 a page-touching request
while the analyst's own `run_suite` holds the lease -> waits ≤ 60 s, then exit 3 `stand_busy` with the holder; between requests the lease file
holds no `walk:<W>` entry. INVARIANT: the session never blocks its own role's runs; at 60 s it waits, beyond it answers. E0.5 no request for longer
than `idle_s` on a `settle` session -> still `ready`; parent gone -> `dead` (N1a E1.7). INVARIANT: an S7 session dies only with its dispatch, its
parent or `max_s`. E0.6 a `case` lane -> lease for its whole life and `idle_s` 900 exactly as N1a. INVARIANT: S6 is unchanged.
**DoD — `test_walk_places.py` (fast, fake backend):** `test_case_root_unchanged`, `test_case_lane_lease_unchanged`, `test_settle_root_is_case_root_settle`,
`test_settle_root_shared_with_http_capture`, `test_control_root_passes_triage_control_problems`, `test_item_id_escape_refused`,
`test_unknown_place_refused`, `test_next_attempt_on_reopen`, `test_suite_run_not_blocked_by_settle_session` (a lease taken by another job
between two `step`s succeeds), `test_step_waits_then_stand_busy` (fake clock: 60 s waits, 61 answers), `test_settle_session_not_idle_killed`,
`test_settle_session_dies_with_parent`. Negative control: with the lease held for the session's life, `test_suite_run_not_blocked_by_settle_session`
fails. Witness: `python -m pytest ai-packages/qa-factory/scripts/tests/test_walk_places.py ai-packages/qa-factory/scripts/tests/test_walk_session.py ai-packages/qa-factory/scripts/tests/test_stand_lease.py ai-packages/qa-factory/scripts/tests/test_artifact_writers.py -q`
(CI: `test_triage_control.py`, `test_role_commands.py`). `architecture:` AR-4, AR-14, AR-21, AR-25.

#### U3b — every S7 triage dispatch: the place lines and the walk session in `run_role` — after N5s, U0, U3a
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`run_role`: the three insertions of §3.6 U3b only (lines before :2842, open before :2854 when no saved result, `finally` close); `stage_S7`: REMOVE U3a's `told += self.s7_place_lines(None)`; `s7_place_lines`: the session line; new `s7_settle_session`; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_place_session.py` (new)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1991-u3b.md` (new)
**non-goals:** N5s's `after=` and S6 lanes; the investigation; everything of U3a besides the moved line.
**edges:** E3b.1 POSITIONAL: lines appended before `extra` for every S7 analyst dispatch that is not an investigation (`controller.s7_part_of`).
INVARIANT: one site; a seam rework and a scribe-reject rework get the same lines as a fresh triage. E3b.2 POSITIONAL: the session opens only when
the role will run (no saved result) and closes in a `finally` (role crash, Refusal). INVARIANT: no session outlives its dispatch (N6's
`test_close_all_after_role` maps to `test_session_closed_when_role_crashes`). E3b.3 the session cannot open (stand down, lease busy past the wait,
walker absent) -> `s7_walk[dispatch].failed` = `stand` / `session` with why; the line says "no walk session: <why>; capture with
`manual_capture.py ui|http --case settle-<place>`, or answer `impossible` with that why". INVARIANT: «Фабрика не должна вставать»; the role always
has a door. E3b.4 the session dies mid-dispatch -> the reopen door of §3.6 (`test_dead_session_reopen_door`). E3b.5 TEMPORAL (resume within the
run): a resumed triage dispatch whose session is not `ready` -> reopened before the resume words (t-1957 E1.16). E3b.6 an investigation dispatch
-> no lines, no session.
**DoD — `test_place_session.py` (fast):** `test_lines_for_fresh_and_rework_dispatches`, `test_no_lines_no_session_for_investigation`,
`test_session_opened_only_when_role_runs`, `test_session_closed_when_role_crashes`, `test_session_failure_recorded_for_gap_reason`,
`test_dead_session_reopen_door`, `test_resume_reopens_session`, `test_one_site_for_place_lines` (`stage_S7` no longer appends them). Negative
control: the `finally` removed makes `test_session_closed_when_role_crashes` fail. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_place_session.py ai-packages/qa-factory/scripts/tests/test_place_driver.py -q`
(CI: `test_story_run_s7.py`). Critic mandatory (core). `architecture:` AR-10, AR-14, AR-19, AR-25, AR-28.

#### U4 — the analyst's charter, the skill road, role-load — after t-1957 N4
**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\agents\qa-failure-analyst.md` (the §3.5 edits only; F-I :81 only if E4.1 fires)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\skills\qa-story\phases\s7.md` (one paragraph after "## Dispatch": `place_answers.py list|write`, the four answers and sources, the capture root `settle-<place>`, and the close step `place_answers.py close-unsettled --task-root T --why "<one of gap_reasons>"` BEFORE the section Investigation — the skill-road twin, AR-19, fix 11)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\role-load.json` (analyst rows: lowered to the measured value if lower; NEVER raised)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_charters_s5_s9.py` (KEYS `qa-failure-analyst` += "Find out the truth on the page", "In a triage, every suspicious place", "never a bug", "an expectation the factory derived itself is no requirement"; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\t-1991-u4.md` (new)
**behaviour:** run `python -B ai-packages/qa-factory/scripts/role_load.py --role qa-failure-analyst` on the tree AFTER N4, attach; apply §3.5; run
again, attach. **edges:** E4.1 total or process above its row -> take F-I; still above -> STOP, revert, report both numbers (no raise, AR-20).
E4.2 a form token in Techniques -> `test_m1_form_tokens_stand_in_tools` red. E4.3 a principle number, `AC`, "must run", "Step N" -> red. E4.4 the
skill road and the driver name the same close order (U3a E3.1). **DoD:** `test_charters_s5_s9.py` and `test_case_role_twins.py` green with the
new keys (negative control: a copy without "never a bug" fails `test_craft_keys_stand_verbatim`); both `role_load.py` outputs attached. Witness:
`python -m pytest ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py ai-packages/qa-factory/scripts/tests/test_case_role_twins.py ai-packages/qa-factory/scripts/tests/test_role_load.py ai-packages/qa-factory/scripts/tests/test_charter_form.py -q`
`architecture:` AR-2, AR-10, AR-11, AR-19, AR-20.

#### What happens to t-1957 N6 (fix 13)
Retired. `walk_session.py --place control` roots -> U0; `test_work_evidence_path_refused` -> U0 E0.1 (`test_item_id_escape_refused`);
`test_control_record_under_evidence` / `test_triage_control_accepts_walk_record` -> U0 `test_control_root_passes_triage_control_problems`; its
`stage_S7` `finally` close -> U3b (`run_role`, one session serves control experiments and settle walks); `test_close_all_after_role` -> U3b
`test_session_closed_when_role_crashes`; its charter Tools line and the `manifest_view.py`/`env_probe.py` cut -> U4; role-commands / role-load
rows -> U0/U1/U4; edges E6.1–E6.4 hold (E6.1 `impossible` with why = this spec's `impossible`). Slice 3 keeps only N7.

#### Live proof (FR-33) on MyBooks LOCAL-1
Stage 1 (after U1, U2, U3a; today's recorder): in a stand copy, rerun S7 of arm B's tree copy (7 code-reading drafts, R-12/13/14). Accept: (1)
`place_answers.py list` shows the places (3–7 — **estimate**); (2) every place ends `settled` or as a named gap line; (3) at least one `bug`
lifts its draft to "reproduced by the factory — the analyst walked it on the stand", at least one `requirement_silent` shows as a question at
gate B (and whether it is ADDRESSABLE — F4 could not be established), no `bug` on `expectation.source: none`; (4) a `settle-` folder under
`work/evidence/manual/` is named by no reader as an unknown case (N3); (5) the Lead cross-checks each answer's expectation source against the
register and lists disagreements. Stage 2 (after U0, U3b): the same with the walk session; time and cost per place by `walk_timing.py --summary`
grouped by place `settle` against §3.7. Expected wall ≈ 30–60 min of S7 per stage — **estimate**.

---

## §5 Questions for the owner

None new. Decided: Q1 — «Только неподтверждённые» (owner, 05.11.2026 22:07). Q2 — no cap as a number (Lead); the honest ceiling (§3.7) is said
to the owner in plain words when the Lead reports this batch: «Предела по числу мест нет; одна сессия прохода живёт до 90 минут, поэтому за один
диспатч реально около 15 мест; что не успели — в отчёте отдельной строкой "не проверено", никогда молча».

---

## §6 Forks for the Lead (the nodes are written to the recommendation)

- **F-J. A `bug` answer on a place no draft form can carry** (an `open` place with no triage failure — a case refused before any capture, an
  unpinned `obs-` target with no manual-check row —, no contradicting register row, no settled question; F5). (a) U2b: the code-reading
  requirement form also accepts a standing walk receipt whose record cites that requirement (the walk IS the contradiction; F-D already refused an
  unconfirmed R) — a reused checker in a more consequential role, so its error direction and adversarial inputs are written with the answer;
  (b) a third draft form "walk" with its own checker; (c) no draft: such a `bug` stays `carrier missing` and is reported as a gap.
  **Recommendation (a):** one clause, the existing form, and the owner's «баг, проверено» gets a carrier. Until answered, behaviour (c) holds.
- **F-L. Two pre-existing places that one draft touches** (`case-C` and `req-R`). (a) They stay two places, each owes an answer (ids stable); (b)
  merge them into one place when a draft joins them (an id would change: the D4 defect returns). **Recommendation (a).** Cost: an occasional
  second answer, which may cite a capture of its OWN root only.
- **F-M. The analyst's capture commands before the walker lands.** (a) Give `qa-failure-analyst` `manual_capture.py ui|http` (role-commands rows,
  U1), restricted by the brief to `--case settle-<place>`; the settle road works now and API places have a road at all (E2); (b) wait for U0/U3b
  and answer `impossible` until then. **Recommendation (a)** (P14/AR-11: the tool is needed by the work; the restriction is a brief line, not code —
  a code restriction would need the guard path F16 could not establish; queue it if a leak is seen).
- Standing, unchanged: F-A (a), F-C (a), F-D (a) + the `person` door (§3.2 rule 5), F-E (a) driver-opened with the per-request lease (§3.6),
  F-F (a), F-H (a), F-I (conditional, §3.5).

**Small choices closed by the designer:** module `place_answers.py` (fix 15; `settle` keeps only t-1957's walk lane name `--place settle`),
data `references/place-answers.json`, record `evidence/place-answer-<id>.json`, capture root `case_root("settle-<id>")`, `new-<slug>` form and its
40-char limit, brief cut at 40 places and scribe line at 1 500 chars, `request_lease_wait_s` 60, `owner_role` = `investigation.OWNER_WORDS`, the
current-red skip read through `contract.triage_failures` kinds rather than the `#obs`/`#sur-` name (the same direction as the critic's fix 5, and
it also covers an `inconclusive` manual check, F6), the order "record first, then the line" with `carrier missing` (instead of a second validator
of `append`'s rules, which would duplicate them, AR-13).

**Found while revising, for the Lead (not widened here):** (1) F-D's sibling at draft creation (`_oracle_problems` / APP_BUG rows on an
unconfirmed R) — queued by the critic, axis 32. (2) `investigation.unresolved_targets` (iii) passes `task / "work"` as the root with
`under="evidence"` (`investigation.py:409-410`) while the triage validator uses the task root — the S9 question of t-1986, untouched here. (3)
`reproduction_words` lists kinds by a fixed `if` chain (`bug_records.py:922-924`); a fourth kind will need the same edit — a data row would close
the class (AR-1), not this batch.

---

## Critic fix -> where applied

| fix | applied in |
|---|---|
| 1 settled `open` place resolved, no re-investigation | §2 F1-F2; §3.4 "Fix 1 — resolution (iv)"; U1 owns `investigation.py::unresolved_targets`; E1.16; tests `test_settled_open_target_resolved_iv`, twin `test_settled_open_target_not_reinvestigated` (CI), U3a `test_settled_open_place_no_investigation_dispatch` |
| 2 every `append` field; add/correct/withdraw; refused append; stale gaps; prefix | §2 F3; §3.2 table + order rule; §3.4 re-entry; §3.6 POSITION mechanism; U1 E1.9, E1.11-E1.13; tests named in U1 DoD |
| 3 the draft form of a `bug` per source | §3.2 "Downstream of `bug`"; U2 owns the two texts (contract.py:1878-1880, bug_records.py:658-660); `test_register_place_bug_has_a_draft_form`; the no-form case returned as fork F-J (U2b) |
| 4 lease per request, idle for the dispatch, reopen door | §2 F11-F12; §3.6 "The stand lease…" and "Session failure"; U0 E0.4-E0.6; U3b E3b.3-E3b.4; N1a unchanged, U0 after N1a+N2 (answer to the Lead) |
| 5 receipt cannot be forged into a lift; NO_DEFECT stays void | §3.3 (re-runs `answer_problems`, APP_BUG kept for triage-road drafts, the marker's honest scope); U2 DoD |
| 6 the road after a person's gate-B word | §2 F13; §3.2 rule 5 (`person`); §3.4 "The road after…"; U1 E1.15 and tests |
| 7 stable place ids | §3.1 ids + `place_of_draft`; U1 E1.3; fork F-L |
| 8 FR-10 charter vs investigation brief | §3.5 (bullet "In a triage…", `investigation_lines` line); §3.2 rule 8; U1 E1.17; U3a `test_investigation_brief_excludes_settle` |
| 9 five gap reasons with a rule; conflict text | §3.4 point 2; §3.6 "The gap reason…"; U3a `s7_gap_reason`; `test_conflict_gap_text_is_not_not_walked` |
| 10 `not_a_bug` reaches a surface; terminal fields; source shown | §3.2 table (`observation`); §3.4 point 3 (scribe line); `terminal_fields` in `place-answers.json` (U1) |
| 11 CLI `close-unsettled` for the skill road | U1 CLI; U4 s7.md paragraph |
| 12 `draft_listing`; `code_says_contradicts`; captures index; API places; register unreadable | §3.1 table; §3.2 rule 2 (root shared with `manual_capture http`), rule 3 / E1.14; §3.6 "One root" |
| 13 drop `evidence/control-*.json`; map N6 tests | U0 owns (`artifact-writers.json` directory only); "What happens to t-1957 N6" |
| 14 order; name the scribe function | §4 "Order" (U1 → U2 ‖ U3a now; U0, U3b, U4 later); §2 F15 / U3a owns `stage_S8` :13404-13410 |
| 15 rename the module | `place_answers.py` throughout |

Findings not applied as written: **fix 3**, for an `open` place with no S1 fact: the critic's "`fact` = the walk's capture" cannot stand — a
code-reading `fact` must be an S1 fact `{id,path,line}` or a verified code place (`bug_records.py:547-582`), and the requirement form needs the
fact id (:629-630). Returned as fork F-J. **Fix 12, API places**: the critic's "a `manual_capture.py http` attempt rooted under
`evidence/settle-<place>/`" needs a new root option in `manual_capture`; applied instead by moving the settle root to
`case_root("settle-<place>")`, which `http` already writes (F9). **Fix 2, order**: "validated before the record is written" is applied for the
answer's own keys (`answer_problems`); `append`'s own rules are not re-implemented (AR-13) — the refused-after case is the `carrier missing` state
the same fix asks for.

---

## Reading trail

Given, read whole: the verdict `docs/tasks/specs/reviews/t-1987-critic-on-plan-t-1986.md`; the draft
`docs/tasks/specs/t-1986-analyst-walks-unconfirmed-places.md`. `t-1957-fast-manual-walker.md` (grep of headings/lease; :325-445 §3.2-§3.5;
:584-705 N1a). Tree `wt-fbfix\ai-packages\qa-factory`: `scripts/investigation.py` :25-124, :124-219, :300-569; `exploratory_findings.py` :25-415;
`bug_records.py` :195-234, :310-355, :480-940; `contract.py` :1815-1895, :2268-2398, :4398-4557, :5405-5444 (+ greps :1173, :1415, :2151-2204,
:2679); `story_run.py` :1378-1409 (grep), :2790-2865, :4890-4925, :5420-5480, :6852-6921, :9854-9893, :12354-12969, :13372-13421, :16640-16839
(+ greps); `controller.py` :3259-3298, :3415-3499, :8895-8984 (+ greps); `stand_lease.py` :150-249; `run_suite.py` :1360-1399;
`manual_capture.py` :285-315, :1120-1147, :4402-4461, :4630-4703 (+ greps :32, :100, :3911); `manual_evidence.py` :56-62, :155-194, :1339-1347,
:1603-1662; `branch_accounting.py` (grep :1224-1243, :2118-2122); `gate_brief.py` :1117-1124 (+ grep :2000); `report_facts.py` :2852-2900 (+ grep);
`guard_pre_tool.py` :1150-1240; `references/role-commands.json` :1-144; `references/artifact-writers.json` :1-40 (+ grep `evidence/`);
`agents/qa-failure-analyst.md` (grep :14-81); `scripts/tests/fixtures/judgment-census.json` (grep :4, :54-58); `scripts/tests/test_judgment_census.py`
(grep :17-60). NOT read (stated where used): `walk_session.py` (not on the branch); `_annotate_cases` (F4); the guard path of role-commands (F16);
`run_http` beyond :4461 (F9); `skills/qa-story/phases/s7.md`; `references/role-load.json` (the critic confirmed :9/:19/:33); `role_load.py` not run.
Needed beyond the manifest: `controller.py`, `manual_capture.py`, `manual_evidence.py`, `report_facts.py`, `gate_brief.py`, `guard_pre_tool.py`,
`references/role-commands.json`, `references/artifact-writers.json`, `scripts/tests/test_judgment_census.py`.
