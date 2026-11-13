# П1-в. Run scoreboard: friction and comparison are measured by code — DRAFT SPEC

Status: designer DRAFT for Lead acceptance (13.11.2026), FIX ROUND t-401 applied (13.11.2026, see the closing section «Fix round
t-401»). Not a dispatch. Forks are returned (§11), none is decided by the designer.
Source: Lead plan `docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md` §3 «П1-в» points 1–6 (owner's word 13.11.2026
«Да, дизайнеру»), context §1, §5, §6, §8; critic-on-plan verdict `docs/tasks/specs/reviews/t-401-p1-layers-plan-review.md`
(findings №14–19, №23, №29–37) and the Lead's decisions on it (plan §10). Siblings drafted in parallel: П1-а (writer → reader
round), П1-б (dry story) — not designed here; §7.9 states only what the dry story must emit.

Package facts are read from the `origin/main` tree `.claude/worktrees/read-main/ai-packages/qa-factory/` (written below as
`pkg:`). Run facts of LR2-1 are read from the arm's LIVE state folder
`C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1\state\` (written `arm:`), and from
the repo copy `experiments/mybooks/factory-vs-free-agent/runs/factory-out/state/` (written `copy:`). Role transcripts of the arm:
`C:\Users\i_mas\.claude\projects\C--QAFactory-mybooks-stand-arm-factory-test-automation-framework\` (written `tr:`; outside the
repo, read on the machine only).

## 0. Facts that correct the brief and the plan (read before the rest)

| # | Brief / plan says | Carrier says | Consequence for this spec |
|---|---|---|---|
| C-1 | `driver-timings.jsonl` does not exist; code-step time is only a residual (plan §3 П1-в «Чего нет»; t-357 `:7,:17`) | It exists in the arm's live state: `arm:driver-timings.jsonl:1-25` (steps `start`, `start.*`, `bind`, `handoff`, `finish`, with `error`). Its one writer is on main: `pkg:scripts/driver_runner.py:728-747` (`timed`, `timing_write`), timer `pkg:scripts/driver_timing.py:41-57`. The repo copy `copy:` holds ONLY `driver-runs.jsonl` (t-357 `:7`) — the copy was partial, not the run | Code-step time is a MEASURED row, not a residual; the residual is only what no timer covers ("unattributed", already computed per hop by `driver_timing.report`, `pkg:scripts/driver_timing.py:241-286`). The assembler reads the LIVE state folder, never a hand copy |
| C-2 | «All 41 briefs are above the 6144 B ceiling» (plan §1 row 5; t-357 `:162`) | The ceiling is judged on BUDGET bytes, not file bytes: `pkg:scripts/brief_pack.py:54` (`BRIEF_MAX_BYTES = 6*1024`), `:4563-4565` prints `bytes` and `budget_bytes … against the ceiling`. LR2-1 scout: `runs/factory-3.log:27` «7,451 B, 6,107 budget B against the ceiling» — UNDER the ceiling | The brief row compares `budget_bytes` to the ceiling. The plan's §1 fact is at least partly wrong; the Lead re-states it (not this spec's scope to fix) |
| C-3 | FV1-21 = the cumulative `total_cost_usd` trap | FV1-21 is «price falsely marked incomplete: `gate_repair` code steps counted as session-less calls» (`findings-1413/plans/piles/live-run-fvf/findings/20261112-cena-lozhno-nepolnaya-iz-za-shagov-koda.md:1-29`); the cumulative trap is only its side note (`:20-21`) and is ALREADY handled by the one reader `pkg:scripts/driver_journal.py:9-24, 62-70` (`driver_charged`: last usable total per session, unknown when it falls) | The scoreboard stores no money at all (P18); chat money comes only from `task_price.task_price` (the one price answer, `pkg:scripts/retro_numbers.py:20-28`). FV1-21 is a dependency of the CHAT line (it prints «incomplete» until fixed), not of the scoreboard |
| C-4 | (not in brief) | t-357 table 5 «Cost, summed from `total_cost_usd`» (`t-357:179`) sums cumulative totals naively — the very error C-3's finding names (`:20-21`) — and puts money in a repo file (P18) | Reported to the Lead; not fixed here |
| C-5 | Gate returns can be counted from the records | (a) The driver's 30 gate/critic returns of LR2-1 (t-357 `:117`) exist ONLY as free text in `resume_reason` (`copy:driver-runs.jsonl:8`); the project journal holds 3 `gate_block`/`rejected`/`reject`/`halt` events of 166 (Grep count); `retro_numbers.gate_block_classes` (`pkg:scripts/retro_numbers.py:1227-1240`) reads only `gate_block` events. (b) FIX ROUND t-401 №14: no caller "already knows" a check id. `Refusal` carries `text`, `findings`, `window_findings`, `title`, `close`, `dispatch` and no check id (`pkg:scripts/driver_core.py:117-139`); its `findings` are STRINGIFIED at `:135` (`[str(x) for x in findings]`), so any field a finding object carried is lost there. `resume_reason` is built from text by the regex table `RESUME_CLASSES` (`pkg:scripts/driver_dispatch.py:142-148, 155-174`). (c) What DOES carry a structured origin today: every exit-gate record is a `detector_verdict.Record` (a `str` with `script`, `words`, `kind`, `refused`; `pkg:scripts/detector_verdict.py:90-102`), built per detector finding by `exit_gate.detector_records` (`pkg:scripts/exit_gate.py:443-465`), and every detector finding line may carry the form-1 family label `[<check> <id>]` (`pkg:scripts/detector_verdict.py:15`, `LABEL_RE` `:74`), already read as a FIELD by `detector_verdict._link` (`:227-236`) and `exit_gate._finding_tag_of` (`pkg:scripts/exit_gate.py:1775-1782`). `s5_precheck`'s finding id is `<check>:<case>:<tag>` (`pkg:scripts/s5_precheck.py:266-268`), printed as the label (`:3917-3923`); the row-fields finding is `_finding("manifest", "", …, ROW_FIELDS_TAG)` (`:3840`, `ROW_FIELDS_TAG = "row-fields-missing"` `:3765`) — the ONLY literal `_finding("manifest"` in the file (Grep count 1; control: the same Grep shape `_(finding\|hint\|advice)\("[a-z_-]+"` counts 13) | Counting returns by gate needs a PRODUCER of a structured check id that survives to the resumed row (node N0, §2 W0) BEFORE the node that records the resume kind (N2). Parsing `resume_reason` text, or classifying the code's own refusal text with `RESUME_CLASSES`/`KNOWN_PATTERN`, is not taken (Lead decision №14) |
| C-6 | (not in brief) | `driver-answers.jsonl` has two writers: `pkg:scripts/driver_conductor.py:243-250`, `pkg:scripts/driver_s0.py:407-409`; `driver-questions.jsonl` one writer `pkg:scripts/driver_dialog.py:410-419`; both are read raw in ≥5 places (`person_owned.py:151`, `story_progress.py:535`, `collect_stall.py:690`, `driver_machine.py:1093,1201`, `driver_dialog.py:389`) — no reader function | AR-13/AR-14 siblings; §2 adds ONE reader function the scoreboard uses; the other raw readers are queued (§9 AR-13 line) |
| C-7 | (not in brief) | `test_driver_journal.py` and `test_driver_timing.py` are in the QUARANTINE section of `pkg:scripts/tests/test-layers.json:7898, 7923` (quarantine starts `:7022`, keep is `:35-6967`) | New cases go to keep rows only: `test_driver_stop_record.py` (`:1400-1417`, covers the driver set and `driver_journal.py`), `test_retro_numbers.py` (`:4429-4442`), `test_brief_pack.py` (`:277`), `test_detector_verdict.py` (`:1239-1259`, data_join), `test_friction.py` (`:1738-1753`, covers `friction.py`, `references/friction-markers.json`), `test_story_step.py` (`:6164-6175`) |
| C-8 | (not in brief) | `copy:driver-runs.jsonl` carries `total_cost_usd` on every outcome row; ESTABLISHED (fix round, №32): the copy is committed (critic t-401: `git ls-files`, commit `4e00ed7`) and holds 120 occurrences of `total_cost_usd` (re-counted this session: Grep count 120 on `experiments/mybooks/factory-vs-free-agent/runs/factory-out/state/driver-runs.jsonl`). `runs/.gitignore:1-4` ignores `*.json`, `*.log`, `*.err`, not `*.jsonl` | Money sits in a repo file today (P18) — a finding outside this spec, reported to the Lead (closing section). The scoreboard never copies raw records into the repo (§4) |
| C-9 | (not in brief) | `plans/MEASUREMENTS.md` has no LR2-1 entry (Grep `LR2` → 0; control `15045` → 7 hits) | The first scoreboard (node N8) is the first in-repo measurement of LR2-1 |
| C-10 | «24 cards, truth table» | The truth has TWO versions: Lead 05.11 «8 bugs» (`experiments/mybooks/disputed-check-plain-agent/SUMMARY.md:35`) and «after the owner's words: 6 bugs, 3 removed» (`:80-86`); t-354 had to score both (`reviews/t-354-tests-factory-vs-free.md:105, 112-113`) | Truth is a versioned data file; a scoreboard names the version it was judged against (fork F9) |
| C-11 | (fix round, №29) the draft said «`resume_reason` text stays for people; no code reads it» | WRONG: `retro_numbers.resume_metrics` groups by the text of `resume_reason` (`pkg:scripts/retro_numbers.py:1721`) | Until the F3 delegation node, `resume_metrics` is a SECOND definition of rework (AR-15) by text; this spec does not add a third — `run_counters` reads only `resume_kind` and `checks`; the delegation stays queued (F3, §10) |
| C-12 | (fix round, №16) `run_class` «live\|dry\|smoke» on W1 | No signal in the package (critic: Grep -i `run_class\|STORY_RUN_DRY` over `pkg:scripts` → 0; control `STORY_RUN_CLAUDE` → 41 in 23 files) | Source decided by the Lead: env var `STORY_RUN_CLASS` (§2 W1) |
| C-13 | (fix round, Lead bullet / №31) bookkeeping time and refused calls per role session | No row of §2 carried it: `friction` counts friction TURNS, not time, and never counts a successful bookkeeping call (`pkg:scripts/friction.py:7-15, 167-211`); its transcript reader keeps no timestamps (`turns_of`, `:107-147`). The host transcript carries a `timestamp` on its lines (`tr:18c97743-d831-453c-b754-0be038ce5fd0.jsonl`: Grep count 39) and a structured `is_error: true` on failed tool results (`tr:` folder: 70 occurrences in 27 files, Grep). No package hook/guard file searched writes a per-tool-call record: Grep `[a-z_-]+\.jsonl"` over `stage_guard.py`, `hooklib.py`, `exit_gate.py`, `role_cli.py` names only `journal.jsonl` (the same Grep is the positive control: it finds that name) | Rows T9/T10 added (§2) with source fork F15 |

The truth table of the stand: cards `experiments/mybooks/add-to-cart-disputed-places.md`, verdict column «Итог Lead»
`experiments/mybooks/disputed-check-plain-agent/SUMMARY.md:9-33`, owner revisions `:61-86`, scoring classes
`experiments/mybooks/factory-vs-free-agent/factory-vs-free-agent.md:18-24, 32-38`.

---

## 1. Architecture, FR section F, owners and census (designer rule 1; CLAUDE.md rule 10)

### 1.1 AR-n touched and how each is kept

| AR | Text (pkg:design/architecture.md) | How this spec keeps it | Change check written into the DoD |
|---|---|---|---|
| AR-12 | `:127-132` friction is measured; the weekly calibration has no friction check (`:130`) | The scoreboard is the per-run measurement; it reuses `friction.story_friction` (FR-55) for the friction row WITHOUT its money keys (fix №15) and extends the same transcript reader for bookkeeping/refused-call time (T9/T10, fork F15) — no second friction counter; the calibration check that closes the «no friction check» gap named at `:130` and the AR-12 `Detector:` edit are REQUIREMENTS to the Lead node «носители П1» (§8.1), not written by this spec's nodes | N4 DoD: the friction row's shares equal `friction.story_friction`'s, and no money key is in the row (two test rows, §8 N4); N4b DoD: T9/T10 come from `friction.py` (one transcript reader) |
| AR-13 | `:161-166` a fact with a reader is read only through it | `driver-runs.jsonl` only via `driver_journal.read_rows`/`parse_ts` (`driver_journal.py:321-360`) plus the counted variant; timings ONLY via the existing `driver_timing.report(task_root)` (`driver_timing.py:241-286`; fix №30 — no `read_timings`); questions/answers via ONE new reader function (C-6); role transcripts only via `friction.py`. The forge assembler imports the package's `run_counters`, never parses state files itself (precedent `experiments/measurers/code_friction.py:28-39`) | N4 DoD: grep `run_counters.py` for `json.loads`/`open(` with a positive control → none; N6 DoD: `scoreboard.py` contains no parser of `driver-*.jsonl` |
| AR-14 | `:168-173` one artifact, one writer | Each NEW record/field has one writer: W0 `checks` key → `run_claude` row (`driver_runner.py:901-910`); W1 `process` rows → `Driver.run` through `journal_run` (`driver_runner.py:402-404`); W2 `resume_kind` → the same `run_claude` row; W3 `state/brief-sizes.jsonl` → `brief_pack.build`; the story_step → driver `checks:` line → `story_step._gate_refusal` only (fork F17). Scoreboard YAML files → `scoreboard.py assemble` only; norms file → Lead's commit only | N3 DoD: `references/artifact-writers.json` row for `state/brief-sizes.jsonl` if state files are declared there (builder checks, positive control); N6 DoD: one write site per scoreboard file |
| AR-15 | `:175-180` one survivor | Rework / resumes: one definition (F3); friction and transcript time: `friction.py`; price: `task_price`; hung-call threshold: `driver_timing.WALL_NOTE_OVER_MS` (`driver_timing.py:36`); time parsing: `driver_journal.parse_ts`; code-step time: `driver_timing.report`; check id of a finding: ONE function `detector_verdict.check_id` over the record's fields, which `exit_gate._finding_tag_of` also reads (no second label reader) | N0 DoD: `_finding_tag_of` reads the record field; N4 DoD names each survivor called |
| AR-18 | (index) detectors and refusals have one output shape and one reader | The form-1 printed contract is NOT changed; `detector_verdict.parse` (the one reader) adds a parallel `labels` list, as it already returns `refused` parallel to `findings` (`detector_verdict.py:282-284`); handoff-form errors become `Record`s too (one shape) | N0 DoD: `test_detector_verdict.py` variant rows; SIBLING_MAP axis 17 closing rule (`docs/SIBLING_MAP.md:384`) — reader changed, contract unchanged, producers unchanged |
| AR-20 | `:210-222` shrink-only ratchets; a raise is named | Norms only tighten; a raise needs a named reason and the owner's word (§5). `norms.json` is a new ratchet: the axis-18 row and critic question 9 line land IN THE SAME COMMIT as N6 (fix №23; the Lead plants that part of the «носители П1» node with N6) | N6 DoD: `scoreboard.py norms --check` refuses a raise without `raised_by` + `word`; the commit carries the axis-18 line |
| AR-22 | `:233-238` every field read has a producer and vice versa | Every scoreboard row names its producer (§2 table); every new field (W0–W3) names its readers; the temporal gap «field written, reader not yet landed» is named per field (§7.11) | N0/N1/N2 DoD: rows without the new keys keep today's shape for every existing reader (`collect_stall`, price readers, `retro_numbers`); N4 DoD: §2 table rows each have a test variant |
| AR-23 | `:240-244` every required list declares its empty outcome | Questions = 0, returns = 0, no brief record, no truth table, no transcript: each has a named empty value (§7), never a missing key | N4/N6 table rows «empty» |
| AR-28 | (index) an unknown never becomes a pass | Unknown inputs print `unknown: <why>`; a refusal with no check id is `unknown`, counted and printed (W0); an unknown norm is not green (F7, F12); an unrecognised `STORY_RUN_CLASS` is `unknown`, never `live` (W1) | N0, N1, N7 DoD rows |
| AR-29 | `:134-157` code judges data; judgment by a tier above | Quality rows are JUDGMENT supplied in a judgment file (§1.3); code checks only shape and joins. The bookkeeping-script list (T9) is a data table signed by the Lead (F15) | N5/N6 DoD: census class named per check (§1.4) |
| AR-1 | (index) closed variety is a data row (`pkg:design/architecture.md:35-36`: «a closed set of values lives in one `references/*.json` table with one reader») | Resume kinds and run classes: `references/run-record.json` (one loader); bookkeeping scripts: a key of `references/friction-markers.json` (its one reader `friction.load_markers`); row→pile mapping, norms, truth classes: forge data files | N1, N2, N4b, N6 DoD |
| AR-4 | (index) not tied to one machine | Scoreboards store no absolute paths of the stand (paths relative to the run root, or a sha256 of the source file); the friction row drops `helpers` paths (§2 R1r) | N6 DoD row |

AR touched but not changed: AR-17 (questions are read, not asked), AR-24 (the person's words are not read by the scoreboard; only
counts, kinds and the driver's own question identity `question_sha`).

### 1.2 FR section F walk (pkg:design/factory-rules.md)

| FR | Applies | Fact |
|---|---|---|
| FR-24 (`:371-376`) | yes | Sessions counted are those `driver-runs.jsonl` names (the factory's launch record); no `by_task` tag is read |
| FR-25 (`:378-382`) | yes, chat only | Money is printed only in chat through `task_price`, which already names agreement or a range (`retro_numbers.py:20-28`) |
| FR-26 (`:384-387`) | yes | A worsened row becomes a finding draft that QUOTES the raw record rows behind it (row ids, ts) — a count alone is not a finding |
| FR-27 (`:389-393`) | yes | A comparison names the exact earlier scoreboard file and bar file it used; no implicit cache |
| FR-28 (`:395-398`) | yes | Every measurer node ships variant rows that fail without the change (§8) |
| FR-41 (`:400-404`) | yes | Every row has a distinct `unknown: <why>` state; a refusal with no check id is the counted `unknown` check, never dropped; operator-intervention time inside a gap is not split (§2 trap T-op) |
| FR-51 (`:406-409`) | yes | The scoreboard reports model seconds per stage (the LLM side); its own run time is not optimised |
| FR-55 (`:411-417`) | yes | Friction row from `friction.story_friction`, and bookkeeping/refused-call time from the same reader, on every live run |
| FR-12, FR-13 (section C) | yes | No reading of `resume_reason` wording; no classification of refusal text by `RESUME_CLASSES`; check ids are read from record FIELDS and the form-1 label structure through the one reader; closed kinds in data |
| FR-14 (section C) | yes | `detector_verdict.parse` gains an output key (`labels`) — additive, every reader of its dict unchanged; story_step's exit-3 stdout gains one machine line (F17) |
| FR-4 (section A) | yes | A red norm stops a SILENT release; an informed pass by the owner's words passes (fork F7) |
| FR-30 (section G) | yes | Package files English, no Cyrillic; forge files may be Russian |
| Sections B, D, E | B — no text shown to a person changes (the `checks:` line is stripped by the driver before any refusal text is built; on the skill road it is one machine line in story_step's stdout, F17); D — no identifier resolution changes; E — the report of a story is not changed (the scoreboard is a forge artifact) | one line each, as here |

### 1.3 P27: data rows vs judgment rows

DATA (code counts, from records): every time row, first pass vs rework by call, returns per check id and model seconds after them,
questions by kind and their gaps, question repeats, brief budget sizes, hung calls, friction share, bookkeeping and refused-call time,
process restarts, package/config changes between processes, counts of unknowns.

JUDGMENT (code never decides; it only counts the recorded answers):

| Row | Who judges | Where recorded | Accepted by |
|---|---|---|---|
| A finding of the arm is (or is not) truth card N | the blind evaluator (critic, fresh context) over `runs/outcome-X/Y.md`, as in LR2-1 (`factory-vs-free-agent.md:44-54`) | `experiments/<exp>/judgment.yaml` (schema §4.3), rows `card`, `verdict`, `by`, `evidence` | the Lead (reveals the key, walks unsure rows); disputed rows — the owner (`factory-vs-free-agent.md:54`) |
| False bug / false pass / duplicate | same | same | same |
| «Could not verify» — honest or own undone work | same (row «з», `factory-vs-free-agent.md:67`) | same | same |
| A red test is red ON a bug (not a test defect) | same evaluator, reading the arm's test run (t-354 B(2) is the model: `reviews/t-354-…:103-120`) | same, rows `red_test` | same |
| A gate's returns «caught» something real | the Lead at scoreboard acceptance (fork F4) | `judgment.yaml` rows `gate_catch` | the owner if disputed |
| Truth of a card (bug / gap / owner-decides / not a bug) | the owner (`SUMMARY.md:61-86`) | `experiments/<stand>/truth/<story>.yaml`, versioned | owner's word with date |
| Which factory scripts are «bookkeeping» (T9) | the Lead (classification of the factory's own closed script set; t-391's split is the first draft) | `references/friction-markers.json` key `bookkeeping_scripts` | the Lead's commit (F15) |

The factory arm and the free arm reach the quality rows by ONE road (P31): the same outcome normalisation, the same blind
evaluation, the same judgment file. The scoreboard never reads the factory's own S7 verdicts for quality rows.

### 1.4 Every check this spec adds: owner and census class (AR-29 `:155-157`)

| # | Check | Where | Class | Owner it serves | Blocks? |
|---|---|---|---|---|---|
| K1 | judgment file shape: every card of the named truth version has exactly one verdict row; verdict ∈ the class vocabulary of the truth file; unknown card id refused; no key of the money vocabulary (`usd`, `cost`, `price`, `money`, `priced` — fix №15 adds the last two) anywhere in a scoreboard | `scoreboard.py assemble` (forge) | shape + xref | data (code) | refuses to WRITE a scoreboard with a broken judgment file or a money key (names rows); never judges content |
| K2 | norm comparison: measured value vs norm value → green/red/unknown | `scoreboard.py compare` | xref | data (comparison); the norm VALUES serve intent (owner) | no — prints; feeds K3/K4 |
| K3 | release check: the newest live scoreboard has no red/unknown norm, or an owner pass is recorded | `scoreboard.py release-check` (forge, release procedure) | xref + presence (of the owner's word) | intent (the owner decides what blocks a release) | per fork F7 |
| K4 | worsened row → finding draft | `scoreboard.py compare --findings` | xref | data | no |
| K5 | norms file only tightens unless a raise row carries `raised_by` + `word` | `scoreboard.py norms --check` | shape + presence | intent | refuses the norms edit (forge-check) |
| K6 | «gate costs more than it catches» | `scoreboard.py compare` | xref over JUDGED rows only | judgment (Lead's `gate_catch` rows) | no — names the gate; ADVICE for the Lead |
| K7 | (fix round) `run_class` comparability: two scoreboards are compared only when both are `live` (and the same arm) | `scoreboard.py compare` | xref | data | no — prints `not comparable: run_class <a> vs <b>`, no worse flags, no finding drafts |

Census: `judgment-census.json` scans only package `scripts/*.py` (`architecture.md:146`). K1–K7 live in the forge
(`experiments/measurers/`), outside the census; classes are named here anyway. Package nodes N0–N4b add NO check unit: W0 adds a
DATA field (the origin of a finding, read from record fields), not a judgment; `run_class` is a read of an env var; each package
node's DoD states «census: no new unit» and runs `test_judgment_census.py`.

---

## 2. Every scoreboard row: source, writer, today's state, missing writer

Writers (W) to add — one each, with readers:

- **W0 — structured check id of a refusal (FIX ROUND t-401 №14; producer node N0, lands BEFORE N2).** Enumeration of every place a
  refusal or finding set leads to a role RESUME, by reading the code. Measured with two Grep runs over `pkg:scripts/[a-z]*.py`
  (non-test package files): `resume=[a-z]` → 5 package call sites of `run_claude(…, resume=…)` (`driver_dispatch.py:547, 576, 1034,
  2078`; `driver_machine.py:548`; the other hits `driver_runner.py:562, 673, 826, 853, 854, 859` are the call's own plumbing, not
  call sites); `\.resume_with\(` → 3 callers (`driver_dispatch.py:3622`, `driver_machine.py:275, 290`). Positive control: both
  runs return the known `driver_dispatch.py:547` / `driver_machine.py:275`. Plus the driver's own resume inside `run_claude`
  (`driver_runner.py:815-818`). Nine roads:

  | # | Site (pkg path:line, function) | What it resumes on | Where the check id comes from (after N0) | id carried |
  |---|---|---|---|---|
  | R-1 | `driver_dispatch.py:546-549` `handoff_ladder` (first resume) | `errors` = `exit_errors` (`:301`, `exit_gate.all_errors` records) + `form_errors` (`:352-353`, `handoff_check` problems) | each `Record`'s `check` field (exit gate records: set in `exit_gate`, see below; form errors: built as `Record`s in `form_report` with `check = "handoff_check:" + <problem path with list indices dropped>`, e.g. `handoff_check:scope[].reason`; the «no readable answer» line `:346` → `handoff_check:unreadable`) | e.g. `s5_precheck:manifest`, `handoff_check:header.verdict` |
  | R-2 | `driver_dispatch.py:575-577` `handoff_ladder` (third, mechanical turn) | the same `errors`, recomputed (`:581`) | same | same |
  | R-3 | `driver_dispatch.py:1034-1036` `resume_role` | the person's answer, no refusal | — (not a refusal) | NO `checks` key on the row (not `unknown`: there was no refusal) |
  | R-4 | `driver_dispatch.py:2077-2080` `resume_with` (the run_claude of R-5, R-6, R-7) | a `Refusal` | `refusal.checks` (new field, below) | per caller |
  | R-5 | `driver_machine.py:275` `resume_on_refusal` (first resume) | a refusal whose head is in `RESUMABLE_HEADS` (`driver_machine.py:38-39`): (i) `exit gate for <id>` = the driver's own `Refusal` at `driver_dispatch.py:587-589` (`findings=errors`, records); (ii) `story_step finish <id> (exit 3)` = `driver_dispatch.py:839` (text = story_step's stdout) | (i) computed from the record fields BEFORE `Refusal.__init__` stringifies them (`driver_core.py:135`); (ii) the `checks:` machine line that `story_step._gate_refusal` (`story_step.py:2004-2047`, which holds the same `exit_gate.all_errors` records, `:2090, 2107`) prints and the driver's `finish` (`driver_dispatch.py:820-840`) reads and REMOVES from `out` before building the `Refusal` (fork F17) | records' ids; `unknown` when the line is absent/broken |
  | R-6 | `driver_machine.py:290` `resume_on_refusal` (stand answers now) | the same refusal | same as R-5 | same |
  | R-7 | `driver_dispatch.py:3621-3625` `exit_round` (paid round) | a `Refusal` built from `lines` (strings) | the exit record: `exit_limit` (`driver_dispatch.py:3582-3607`) stores `rec["checks"]` from a new `checks=` argument that its 5 callers pass (`driver_dispatch.py:539, 2082`; `driver_machine.py:269, 299, 532`; Grep `self\.exit_limit\(` over `driver_*.py` → 5); `exit_round` passes `rec.get("checks")` to the `Refusal` | records' ids; `unknown` for a record written before N0 (TEMPORAL, §7.11) |
  | R-8 | `driver_machine.py:546-549` `handle_refusal` branch `resume_structured` | a refusal routed by `STRUCTURED_RE` (`driver_dispatch.py:36`, `story_step: refused - S\d structured .* invalid` — the controller's accept path, `controller.py`) | none: the controller prints no structured id, and `controller.py` is a hot file outside this spec (fork F18) | `["unknown"]` — counted, printed, never dropped |
  | R-9 | `driver_runner.py:815-818` `run_claude` (call cut by the service, the driver's own resume) | no refusal | — | NO `checks` key |

  The producer, field by field (one writer each; every reader changed in the SAME commit — CLAUDE.md rule 10):
  - `detector_verdict.Record` gets two attributes with class defaults `check = ""`, `tag = ""` (constructor keywords, like
    `script`/`kind`); `detector_verdict.parse` returns `labels: [(check, id) | None]` parallel to `findings`, read by the SAME
    `LABEL_RE` match `_link` already makes (one match per line, not a second parser); a new `detector_verdict.check_id(record) ->
    str` is THE function that names a record's check: `record.check` when set, else `"<script stem>:unlabelled"` when the record
    has a `script`, else `"unknown"`.
  - `exit_gate.detector_records` (`exit_gate.py:443-465`) sets `check = "<producer stem>:<label check>"` and `tag = <the third
    `:`-part of the label id, as `_finding_tag_of` splits it today, else "">` on each finding record; `<producer>` is the script
    that RAN — a new keyword `producer=` that `witness_errors` passes as `"check_witness.py"` (today it passes the artifact name as
    `script`, `exit_gate.py:151-155`, and `script` stays as it is because a person's word is judged against it); defect and
    unmigrated records get `"<producer stem>:defect"` / `"<producer stem>:unmigrated"`; `unreadable_record` (`:67-79`) gets
    `"<script stem>:unreadable"`.
  - `exit_gate.all_errors` (`exit_gate.py:1850-1891`) gives every record of its OWN producers a family when it has none — POSITION:
    right after each producer call, before `judge_words`: `scoped_errors` → `exit_gate:scoped`, `grounding_errors` →
    `exit_gate:grounding`, `case_identity_errors` → `exit_gate:case_identity`, `digest_errors` → `exit_gate:digest`,
    `required_outputs_errors` → `exit_gate:required_outputs`, `run_advisers` refusals → `exit_gate:adviser` (`:1866-1877`), through
    one helper `detector_verdict.with_check(record, check)` that returns a `Record` copy keeping `script`, `words`, `kind`, `refused`
    (a plain `str` becomes a `Record` with defaults). INVARIANT: the text of every record is byte-identical to today's (finding
    keys, `split_overridden`, the person's words see the same strings); a record that already has a `check` keeps it.
  - `exit_gate._finding_tag_of` (`:1775-1782`) reads `record.tag` (one reader of the label — AR-15). POSITIONAL INVARIANT for
    `word_class` (`:1785-1804`): every record with `words == "source"` is built by `detector_records` (the builder proves it with
    Grep `words=` over `exit_gate.py`, positive control the known `:452`), so `WAITING_FINDING_TAGS` keeps refusing exactly the
    records it refuses today.
  - `Refusal` (`driver_core.py:100-139`) gets `checks` (class default `()`, like `chain`, so a subclass that skips
    `super().__init__` reads empty): a `checks=` keyword wins; else, BEFORE `:135` stringifies `findings`, `checks` = the sorted
    unique `check_id` of each finding; a refusal with neither findings carrying ids nor `checks=` gets `("unknown",)`.
  - `story_step._gate_refusal` prints, as its LAST line, `checks: <JSON list of the sorted unique check ids of blocking>`
    (fork F17); `Driver.finish` (`driver_dispatch.py:759-858`) takes the LAST line starting with `checks: ` out of `out` (the
    `parse_next` precedent, `driver_dispatch.py:177-186`) and passes the list as `Refusal(checks=…)`; absent or broken JSON →
    `("unknown",)` + one `note:` line.
  - `run_claude` (`driver_runner.py:773-910`) gets `checks: tuple | None = None`; on a resumed row whose caller passed `checks`,
    the row carries `"checks": [<ids>]` and `"checks_n": {<id>: <findings of that id>}` beside `resume_reason`; a row with
    `checks=None` carries no key (R-3, R-9, and every non-resume call). The callers R-1, R-2, R-4 (from `resume_with`, which gets
    `refusal.checks`) pass it.
  - Readers of the row keys: `run_counters` (N4: G1). Until N4 lands no code reads them (TEMPORAL, §7.11).

  Direction of error (the id feeds the norm N-gate and, through F7, the release check K3): the producer may err toward `unknown` /
  `<producer>:unlabelled` (a finding counted under no family or a coarse one — undercount per check), NEVER toward naming a check that
  did not produce the finding. Adversarial inputs that must stay on that side, each a variant row in N0: a finding message that
  contains `[grounding R3]` in its middle (LABEL_RE is anchored at the line start after `- `; the producer's own label wins); a label
  whose id has no `:` (tag `""`, family kept); a record whose text another producer prefixed with `<script>: ` (`exit_gate.py:452`;
  the label is parsed by `parse` before the prefix); a plain `str` in `findings` (→ `unknown`); a refusal of 200 findings of one
  family (one id, `checks_n` 200); a `checks:` line with a nested object, with non-UTF-8 bytes, with an empty list, two `checks:`
  lines (the last wins; the earlier one stays in the text — only the last is the machine line).

- **W1 — `process` rows** in `state/driver-runs.jsonl`. Writer: `Driver.run` (`pkg:scripts/driver_machine.py:1770-1781`) through
  `journal_run` (`driver_runner.py:402-404`): at start `{"kind":"process","event":"start","since":<run_started>,"package":<fingerprint>,
  "config_sha":<sha256 of qa-factory/config.json bytes or null>,"answer_file":<bool>,"run_class":<driver_journal.run_class()>}`; at the
  end, in a `finally` of `run()`, `{"kind":"process","event":"end","since":<run_started>,"process_code":<int|null>,"question_kind":<kind
  of state/driver-question.md if posted, else null>}`. POSITIONAL INVARIANT: the rows carry NO `dispatch`, `dispatch_id`,
  `session_id`, `exit_code`, `is_error`, `infra`, cost key — exactly the `stopped_by_person` shape (`driver_machine.py:1787-1790`), so
  `journal_run`'s open-call matcher (`driver_runner.py:411`, keys `is_error`/`exit_code`/`infra`) and every session/price reader
  pass them by; the end key is `process_code`, never `exit_code`. Readers: `run_counters` (driver windows, gaps, restarts, run
  class); `collect_stall` K3 must stay unchanged (a test row proves a `process` row is not an outcome row). Package fingerprint: the
  value `runtime_paths` already computed for this process if exposed, else `release_fingerprint.package_fingerprint()` ONCE per
  process (its cost note `release_fingerprint.py:116-119`); an exception → `"package": null` + one `note:` line, never a stop (P1).
  **`run_class` (FIX ROUND t-401 №16/№18, Lead decision):** the ONE reader is `driver_journal.run_class(environ=None) -> str`,
  reading the environment variable `STORY_RUN_CLASS`, set by the dry-story walker (П1-б) and the smoke run (П2-г), against the closed
  table `references/run-record.json` key `run_classes` (`["dry", "smoke"]`, default `"live"`; AR-1). Behaviour: variable absent or
  empty after strip → `"live"`; exactly `dry` / `smoke` → that value; ANY other value (`DRY`, `Dry `, `test`, a 10 KB string, non-ASCII)
  → `"unknown"` + one `note:` line quoting at most 60 characters. INVARIANT: a dry or smoke scoreboard is never compared with a live
  one and never becomes «previous» of a live one — the error goes toward «not comparable», never toward `live` (a mistyped dry run
  must not count as a live measurement). Written into the `process` start row ONLY (one writer); `run_counters` reads it from there;
  the scoreboard file's `run.run_class` is copied from it. A run whose windows disagree (two start rows with different values) →
  `run_class: mixed` → not comparable. Safety net (data shape of the dry-story contract, not a name branch): a run marked `live` whose
  role rows carry `session_id` starting `stub-` → `run_class: unknown` + U1 line «stub sessions in a run marked live».
- **W2 — resume kind** on every resumed role row: `resume_kind` (closed token). FIX ROUND t-401 №14 correction: the token names the
  SITE's road (which each site does know structurally), NOT a class of the refusal text (which no site knows without regex). Writer:
  `run_claude` (`driver_runner.py:773-810`, row at `:901-910`) gets `resume_kind=` next to `resume_reason=`; `resume_with` gets
  `kind=` from its callers. Vocabulary in `references/run-record.json` key `resume_kinds` (AR-1): `handoff_findings` (R-1),
  `handoff_findings_mechanical` (R-2), `person_answer` (R-3), `refusal_resume` (R-5), `stand_answers` (R-6), `paid_round` (R-7),
  `structured_refusal` (R-8), `service_cut` (R-9, `driver_runner.py:818`), `unclassified` (a caller that names none — the driver's own
  default, like `driver_runner.py:810`; a token outside the table → `unclassified` + one note, P1). Readers: `run_counters`; later
  `retro_numbers.resume_metrics` (`retro_numbers.py:1687-1741`, queued, F3). WHAT check refused is `checks` (W0), not the kind.
  `resume_reason` text stays for people and is read today by `retro_numbers.resume_metrics` (`:1721`, C-11) — not by any new code.
- **W3 — brief size record** `state/brief-sizes.jsonl`: `brief_pack.build` when it WRITES the dispatched brief (the dict at
  `brief_pack.py:4535` already has `bytes`; `budget_bytes`, `over_ceiling` are in `result`, `:4562-4565`) appends
  `{"ts","stage","role","dispatch","bytes","budget_bytes","ceiling":BRIEF_MAX_BYTES,"over":[…]}` via `hooklib.append_jsonl_line`
  (axis 29). Not written on `--dry-run` or `--output` (not the dispatched brief). Writer placement in `build`, not `main`, so the
  skill road and the driver road write it alike (P31). Reader: `run_counters`.
- **R1 — readers**: `driver_journal.question_rows(task_root)` / `answer_rows(task_root)` → `(rows, bad_lines)` (C-6). Timings: the
  EXISTING `driver_timing.report(task_root)` (hops with `unattributed_s`, `step_totals` with `errors`, `problems` for bad lines;
  `driver_timing.py:241-286`) — FIX ROUND №30: no new `read_timings`. Runs: `driver_journal.read_rows` + a counted variant
  `read_rows_counted(path) -> (rows, bad_lines)` over the SAME line loop (today `read_rows` skips broken lines silently, `:356-360`;
  FR-41 needs the count). Transcripts: `friction.py` only (T9/T10, N4b).

Scoreboard rows (S = exists today on main, M = missing writer above):

| # | Row | Source record (file · field) | Writer (pkg path:line) | Today | Missing writer / reader |
|---|---|---|---|---|---|
| T1 | Run wall (first start → last record) | `driver-runs.jsonl` · `process` start/end; fallback first `launched.started_at` → last row `ts` | `driver_runner.py:843` (launched), `:901` (outcome); W1 | S partly (no process rows: t-357 used log file times `:13`) | W1 |
| T2 | Role model time (union of overlapping calls) and per-session sum | `driver-runs.jsonl` · `kind: role` · `ts`, `wall_ms` (start = `ts − wall_ms`, t-357 `:11`) | `driver_runner.py:901` | S | — |
| T3 | Conductor model time not overlapped by a role | `driver-runs.jsonl` · `kind: conductor` | `driver_runner.py:901` | S | — |
| T4 | Code-step time by step | `driver_timing.report` · `step_totals` | `driver_runner.py:735-747` | S (C-1) | — (existing reader, fix №30) |
| T5 | Unattributed driver time | `driver_timing.report` · `hops[].unattributed_s`, plus time inside process windows outside any hop | — | derived | W1 for exact windows |
| T6 | Waiting for a person (gap: question posted → next process start) | `driver-questions.jsonl` · `ts`,`kind`,`stage`; `process` start of the next window | `driver_dialog.py:410`; W1 | S partly (answer `ts` = taken, `driver_conductor.py:243`) | W1 |
| T7 | Operator intervention gaps | gap whose next `process.start` has a different `package` or `config_sha` than the previous window, or a start with no `answer_file` after a posted question, or a start after an `end` with no question | W1 | M (notebook only, t-357 `:85-97`) | W1; time inside such a gap is ONE row, never split (FR-41) — F2 |
| T8 | Hung calls: count and excess seconds where `wall_ms − duration_ms > driver_timing.WALL_NOTE_OVER_MS` | `driver-runs.jsonl` · `wall_ms`, `duration_ms` | `driver_runner.py:901`; threshold `driver_timing.py:36` | S | — (DC1-24 `duration_ms` meaning pending: execution-report/2 `:46`) |
| T9 | (fix round, Lead bullet) Bookkeeping calls per role session: count and seconds | role transcript (`friction.locate`, `friction.py:244-270`) · per tool call: `tool_use` id/name/command and the line `timestamp`; its `tool_result` line `timestamp`; the script named in the command by the existing shape `friction.SCRIPT` (`friction.py:39`) looked up in `friction-markers.json` `bookkeeping_scripts` | host transcript (no factory writer) | M (t-391 by hand, plan §8 `:182-195`) | N4b: `friction.call_spans` + `story_calls`; source fork F15, time definition fork F16 |
| T10 | (fix round, Lead bullet) Refused / failed calls per role session: count and seconds, split by `friction.classify` kind where it names one (`guard`, `validator`, `usage`, `crash`, `stand`), else `failed, cause not recorded` | the same transcript · `tool_result.is_error == true` (host's structured flag) | host transcript | M (t-391: 20 calls, 201 s, plan §8 `:193-195`) | N4b; NO norm until N4b's reconciliation with t-391 is accepted (§5) |
| F1 | First pass vs rework, calls and role seconds | `driver-runs.jsonl` · `resumed`, `resume_kind`; controller dispatch records (`retro_numbers.dispatch_rounds`, `:268`) for critic returns (a new dispatch, not a resume) | `:901`; W2 | M (text-only today, C-5) | W2; definition F3 |
| G1 | Returns per check: resumed calls naming the check, their role seconds, model seconds until the dispatch next passes; plus the `unknown` check as its own line | `driver-runs.jsonl` · `checks`, `checks_n` on resumed rows | W0 | M (C-5) | W0 (N0); counting rule §7.12 |
| G2 | Gate repairs by code | `driver-runs.jsonl` · `kind: gate_repair` · `gate`, `moves` | `driver_gates.py:822` | S | — |
| Q1 | Questions to the person by kind and stage | `driver-questions.jsonl` · `kind`,`stage`,`source`,`why_person` | `driver_dialog.py:410-419` | S | reader R1 |
| Q2 | Gates passed by the person's word (P13) | `state/passed-by-person.jsonl` | `controller.py:2402` | S | reader in run_counters (one site) |
| Q3 | (fix round №18, Lead decision) Question repeats, by kind: answer rows whose `question_sha` already appeared on an earlier answer row | `driver-answers.jsonl` · `question_sha`, `kind` — the driver's own FR-7 identity (`question_body_sha`, compared by `already_answered`, `driver_dialog.py:381-392`); both writers carry it (`driver_conductor.py:248`, `driver_s0.py:409`) | existing | S | reader R1 |
| B1 | Brief budget bytes vs ceiling, per role: count over, mean, max | `state/brief-sizes.jsonl` | W3 | M (stdout only, `brief_pack.py:4563`) | W3 |
| R1r | Friction share of role turns (FR-55) — FIX ROUND №15: per role and total, ONLY `turns`, `fric_turns`, `turn_share`, `kinds`, `sessions`, `sessions_unreachable`, `dispatches`, `reachable`, `status`, `reason`, plus `helpers_n` (the count of `helpers`); dropped BY NAME: `priced_cost`, `fric_cost`, `money_share`, `priced_turns`, `unpriced`, `helpers` (paths, AR-4) | role transcripts via `friction.story_friction` (`friction.py:337-427`) | `pkg:scripts/friction.py` (called at `retro_numbers.py:2043-2050`) | S (needs transcripts on the machine) | — |
| U1 | Data quality: bad lines per carrier, naive timestamps, rows with unknown kind, `unknown` check share, `unclassified` resume kinds, stub sessions in a live run | R1 counted readers, `driver_timing.report` `problems` | — | M | R1 |
| QA1 | Known bugs found (of truth version V): found / missed / false pass | `judgment.yaml` × `truth/<story>.yaml` | evaluator + Lead (§1.3) | M (markdown table only, `factory-vs-free-agent.md:56-71`) | N5 data files |
| QA2 | False bugs; duplicates of one root cause | same | same | M | N5 |
| QA3 | Owner-decides places asked / not noticed | same | same | M | N5 |
| QA4 | Red tests on bugs (of found bugs) | `judgment.yaml` · `red_test` rows | same | M (t-354 B(2) prose) | N5 |
| QA5 | «Could not verify»: count, honest / own undone work | `judgment.yaml` · `unverified` rows | same | M | N5 |
| QA6 | Delivery verdict present and right | `judgment.yaml` · `verdict` row | same | M | N5 |
| X1 | Money | `task_price.task_price` | — | chat only (P18) | never stored |

Known traps, resolved:

- **T-cum (cumulative `total_cost_usd`)**: no row reads it. Chat money: `task_price` only. A test row: a journal whose resumed
  session totals rise (0.424 → 0.455, `copy:driver-runs.jsonl:2,4`) yields no money key in the counters dict.
- **T-utc (UTC vs local)**: every stored time is ISO 8601 UTC with offset, parsed by `driver_journal.parse_ts` (`:321-336`). The
  driver writes `+00:00` (`pkg:scripts/driver_core.py:259-260`). A NAIVE stamp is read as UTC by that reader; run_counters
  COUNTS naive stamps in U1 (sibling: `pkg:scripts/s7_reorder.py:73-74` writes naive LOCAL time — reported, not fixed). Local time
  appears only in chat output.
- **T-hang (wall ≫ duration)**: T8; the call's wall still counts in T2 (the person waited), its excess is a separate row, never
  subtracted silently.
- **T-op (operator time)**: T7 by data only; the notebook is never read. A gap the data cannot class is «waiting, cause not
  recorded». Inside a gap, decision time vs patch time is `unknown` (t-357 `:97`).
- **T-money-friction (fix №15)**: `story_friction` returns money (`friction.py:372-375, 409-413`); the row keeps turn shares only
  and K1 refuses any money-vocabulary key, so a future money key added to `story_friction` is refused at write, never leaked.

### 2.1 Bookkeeping and refused calls (the Lead's bullet): where the time becomes measurable by code

- §2 had no source (C-13; critic №31).
- Three roads were weighed (fork F15):
  (a) **host transcript, structurally** — `timestamp`, `tool_use` (id, name, command), `tool_result` (`tool_use_id`, `is_error`):
  host-written structured fields, no phrase list; the script is named by the existing shape `friction.SCRIPT`; «bookkeeping» is a
  data table. Reuses the ONE transcript reader of FR-55 (`friction.turns_of`, which `experiments/measurers/code_friction.py:28-39`
  also imports — new keys are additive, that printer is unchanged). Covers guard refusals (the host returns them as failed tool
  results — ESTIMATE, NOT VERIFIED: N4b measures it on `tr:` and reconciles with t-391's 20 refused calls before any norm). Claude
  host only (`friction.locate` reads Claude's folder, `friction.py:244-270`); Codex → `unknown: no transcript reader for host codex`.
  Dry/smoke runs have no transcript → `n/a: stub roles` (by `run_class`, W1).
  (b) **the factory scripts log their own call** — one writer (a `hooklib` appender) into one record `state/script-calls.jsonl`
  (start, end, script, exit, refused): host-independent, but measures execution time only (not the model's turn around the call,
  which is most of t-391's 7.3 s per bookkeeping call, 367 s / 50 calls, plan §8 `:186`); every role-facing script must call it
  (no common entry point established in this session); a guard refusal never starts the script, so `stage_guard.py` (hot file)
  must log too; a script does not know its role session — attribution by time window inside role calls is ambiguous when S5 chains
  run windows in parallel.
  (c) **PreToolUse/PostToolUse hook records** — the host's hook events carry `session_id`, the tool and its input; whether a
  failed tool call fires a post event on this host is an UNKNOWN environment property → CLAUDE.md hygiene 6(a): one experiment
  first, not machinery.
- Recommendation (a): one road (AR-15, P31 — reuse before adding), no new writer, FR-55/AR-12 fit (bookkeeping time is exactly
  «code that makes a role's stage dearer», FR-55), the classification is data (FR-13). Its limit is stated, not hidden: Claude host
  only; refused-call cause by `friction.classify` where it can name one, else `failed, cause not recorded`.
- Relation to `friction.py` / `code_friction.py`: T9/T10 are computed BY `friction.py` (new `call_spans(path, markers)` over an
  extended `turns_of` that keeps each call's `tool_use` timestamp and its result's `timestamp` and `is_error`; new `story_calls(task_root,
  state_dir, project_root)` beside `story_friction`, same session list and `locate`). `code_friction.py` is untouched (additive keys).
  `story_friction` parses `driver-runs.jsonl` itself (`friction.py:345-364`) — an existing AR-13 sibling of `driver_journal.read_rows`;
  `story_calls` reuses `story_friction`'s session loop (one function shared inside `friction.py`), and the sibling is queued (§9).

## 3. The free-agent bar

1. **Produced**: once per (stand, story, model id) — the model id read from the free arm's transcript `message.model` (e.g.
   `claude-sonnet-5-5`), same prompt file (`experiments/mybooks/factory-vs-free-agent/free-agent-prompt.md`), same answers
   (`answers/`), plugin off — the LR2-1 procedure (`plans/piles/live-runs/batch-2-live-proofs.md:68`). A new model id or a new story
   = a new bar run (money — owner question F10).
2. **Measurable by code** (`scoreboard.py bar --transcript <abs path> --result <free-N.log>`; the transcript stays outside the
   repo, t-357 `:184`): wall (first → last transcript event), turns (`num_turns` of the result JSON), tool calls by tool name, number
   of the person rounds (user turns after the first), refused/failed tool calls (`is_error`, the same rule as T10 — one road for both
   arms). Phase split by regex (t-357 `:185`) is NOT stored: it is a heuristic classification of open variety (AR-2) — printed as
   advice only, never a scoreboard row.
3. **Quality rows** of the bar: from the same `judgment.yaml` (arm `free`), one road with the factory arm (§1.3).
4. **Stored**: `experiments/scoreboards/<stand>/<story>/bar-<model-id>.yaml`, same schema as a run scoreboard with `arm: free`;
   rows the free arm has no record for (code steps, gates, briefs, bookkeeping scripts) are `n/a: no such part in a free agent` —
   never 0.
5. **Honest comparison** (CLAUDE.md hygiene 6(b)): one metric per comparison line; a ratio is printed only between two values of
   the SAME metric and unit (wall vs wall, seconds); the factory's «wall without intervention gaps» is compared with the agent's
   wall, and the factory's whole wall separately (fork F8); quality rows compare counts against the SAME truth version.

## 4. Storage

1. **Where**: `experiments/scoreboards/<stand>/<story>/` — one YAML per run `<YYYYMMDD-HHMM>-<package-version>-<arm>.yaml`
   (UTC start), the bar files beside them, `norms.json` at `experiments/scoreboards/norms.json`, row→pile mapping
   `experiments/scoreboards/rows.json`. «Next to earlier ones» = the same folder; «previous» = the newest earlier file of the same
   folder with `run_class: live` and `arm: factory` (K7).
2. **Shape** (`schema: scoreboard/1`): `run` (stand, story, arm, run_class, package version and fingerprint, model ids, started,
   truth version, sources: list of `{file, sha256, lines, bad_lines}` relative to the run root), `rows` (id → `{value, unit,
   source, state: measured|unknown|n/a, why}`), `norms` (id → `{norm, verdict: green|red|unknown}`), `compare` (previous file,
   bar file, per row `{was, now, worse: bool}`, or `not comparable: <why>`). No money key exists in the schema; `scoreboard.py` refuses
   to write a key matching the money vocabulary (`usd`, `cost`, `price`, `money`, `priced`) — a shape check, K1 family.
3. **Raw records are not copied** into the repo (C-8, P18); only sha256 and counts (F11).
4. **Chat only**: money (`task_price`), absolute stand paths.
5. **Worsened row → finding**: `scoreboard.py compare --findings` writes one finding file per worsened row into the pile named by
   `rows.json` (default `live-runs`) in the `findings/` form of PROJECT.md «Командная работа» п. 2 (title, «Что не так» quoting the
   raw rows — FR-26, «Свидетель», «Решение владельца нужно: нет», and the field «какой слой ниже должен был поймать» once the Lead
   node «носители П1» defines it, §8.1), and prints the card/batch rows the Lead adds the same turn (F5; `tools/piles.py`
   subcommands were not established in this session).

## 5. Norms

Initial values = the LR2-1 measurement (a norm can only get stricter than the first measured run):

| Norm | Initial value | Carrier |
|---|---|---|
| N-rework: rework share of role seconds | ≤ 73 % | t-357 `:119` (8,043 of 11,064 s) — re-measured by N4 on `arm:` under the F3 definition before it is written |
| N-gate: returns naming any one check id (G1 counting rule §7.12) | ≤ 16 | t-357 `:132` (`s5_precheck` row-fields-missing = check id `s5_precheck:manifest` under F19 (a), the only finding of that family, C-5) — LR2-1 predates W0, so N4 cannot re-measure it from records: the value stands as the carrier says until the first live run after N0; the `unknown` check is never compared against this norm as green: an `unknown` count above the norm makes the verdict `unknown` (AR-28) |
| N-questions: driver questions to the person | ≤ 40 | t-357 `:57-70`; `factory-vs-free-agent.md:70` |
| N-wall: factory wall / agent wall | ≤ 35.7 (26,292 s / 737 s) | t-357 `:16`, `:184` |
| N-brief: briefs over the budget ceiling | ≤ the count N4 measures on `arm:` (not 41, C-2; the Lead counted 35 of 41) | `runs/factory-*.log` `note: brief:` lines (gitignored, read on the machine) |
| N-quality (each QA row): not worse than the bar of the same truth version | bar values | `runs/blind-eval.md`, `factory-vs-free-agent.md:60-71` |
| (no norm yet) T9 bookkeeping share, T10 refused calls, Q3 repeats | — | printed and compared run to run; a norm is added by the Lead after N4b's reconciliation with t-391 (plan §8: 34 % bookkeeping, 20 refused calls) |
| Target (not a norm): first-pass wall ≤ 2 × agent wall; quality ≥ agent on every row | plan §5 `:132` | |

- **Tighten-only**: K5. After each live run `compare` prints «can tighten: <norm> <old> → <measured>»; the tightening is a Lead
  commit of `norms.json` (F6). A raise: a row `{raised_by, reason, word: "<owner, date>"}` (AR-20); without it K5 refuses.
- **What a red norm blocks**: by default nothing in the run (P1, FR-4: the run is never stopped by a measurer); it becomes a finding
  draft (K4) and a red line in the release check K3. Release behaviour: owner's call (F7). P13: the owner's word passes any red
  norm; the pass is recorded in the scoreboard file (`passes: [{norm, word, date}]`) and counted by the calibration check the Lead
  node «носители П1» adds (§8.1).
- **«A gate whose returns cost more than it catches»** (K6): printed per check id — returns, role seconds after them (G1) — and
  named a defect only when the Lead's `gate_catch` rows judge its catches (F4). Today's candidate named by the plan:
  `row-fields-missing`.
- **Dry/smoke**: no norm is judged on a non-live scoreboard (K7); the dry story prints counters only.

## 6. Existing measurers and PROJECT.md «Как принимается изменение пакета» п. 5

| Tool | What it does (read) | Why no result exists in the repo | Verdict |
|---|---|---|---|
| `experiments/measurers/code_friction.py` | per-role friction from transcripts via the package's `friction.py` (`:2-20, 28-39`), prints a table (`:164-184`) | (1) prints to stdout only, writes nothing (`:137-185`); (2) needs `QA_RUNS_BASE`/`stand_copy_root` and a runs table (`paths.py:66-69`, README `:18-31`); (3) its run layout is hard-coded `<copy>/test-harness/qa-factory/artifacts/<task>` (`:63-65`) — the MyBooks tests root is `test-automation-framework` (RUNBOOK `:539, 577`), so it cannot find LR2-1. Whether anyone ran it after the runs-table refactor: not established | WIRE: the scoreboard's friction and call-time rows call the package `friction.py` directly; `code_friction.py` stays an ad-hoc printer, untouched by N4b's additive keys (its layout bug goes to G3-1, `live-runs/2:50`) |
| `experiments/measurers/stage_compare.py` | per-stage quality of artifacts vs baseline runs (`:1-4`) | same layout literal (`:33`), print-only (`:41-50`), baselines come from a runs table nobody committed (no `runs-table*.json` in the repo: Grep `QA_RUNS_TABLE` hits only code/docs) | KEEP for п. 5 (code step vs LLM reference — a different question from the scoreboard); not reused |
| `compare.py`, `report_run.py`, `spend_by_dispatch.py` | money by transcript / agents (README `:3-7`) | money — must not be stored (P18) | not reused (money stays chat) |
| `run_headless.py`, `prepare_copy.py` | run copy helpers | — | untouched |
| t-357 scratch scripts; t-391 transcript split | the hand prototypes (t-357 `:209-217`; plan §8, outside the repo) | scratch | REPLACED by `run_counters` + `friction.story_calls` + `scoreboard.py` |

п. 5 («a step moved from role to code is checked against the LLM reference with `stage_compare.py`») is a different check: the
scoreboard measures a run, п. 5 compares a code step's artifacts with LLM artifacts. Not replaced, not wired.

## 7. Edge behaviour (each with its invariant)

1. **Run died mid-stage** (no `process` end row; a `launched` row with no outcome): the window ends at the last record of any
   carrier inside it; the open call counts as `cut` with its known start, wall `unknown`; T1 marked `end not recorded`.
   Invariant: a dead run never reads as a finished one, and its open call never adds invented seconds.
2. **No questions**: Q1 = `0 (measured)` only when `driver-questions.jsonl` exists or the run's process rows prove the driver ran;
   absent carrier AND no process rows → `unknown: no question record`. Same for Q3 with `driver-answers.jsonl`. Invariant: a missing
   file is never «0 questions» / «0 repeats».
3. **Resumed across driver restarts**: several `process` windows; sessions reused across windows are one session (by
   `session_id`); gaps classed by T6/T7. Invariant: a session's time is counted once; a restart is never model time.
4. **Stand without a truth table**: QA rows `unknown: no truth table for <stand>/<story>`; the scoreboard is still written; quality
   norms read `unknown` (release consequence F7/F12). Invariant: no quality row is computed from the arm's own verdicts.
5. **First run, no previous scoreboard / no bar**: `compare.previous: none`, `worse` absent, no finding drafts; with no bar the
   N-wall norm is `unknown`. Invariant: «nothing to compare» is never «not worse».
6. **Partial records** (old run: no `process` rows, no `resume_kind`, no `checks`, no `brief-sizes.jsonl`; broken lines): each
   affected row `unknown: <carrier> predates <writer>` or computed from the fallback named in §2; bad lines counted in U1. Invariant:
   an old row's text is never parsed to fill a new field (FR-12) — LR2-1's `resume_reason` texts stay unread.
7. **Two arms / two stories in one folder**: file name carries the arm; `previous` only matches the same arm and run_class.
8. **Truth version changes between runs**: the comparison of QA rows across scoreboards of different truth versions prints
   `not comparable: truth v<a> vs v<b>`. Invariant: a better score from a softer truth never reads as improvement.
9. **Dry story / smoke** (requirement on П1-б and П2-г): the run emits the SAME carriers by the SAME writers — `journal_run`
   rows (launched/role/conductor with `session_id` `stub-<dispatch>-<n>` written by the П1-б stub, `wall_ms`, `resume_kind`,
   `checks`), `driver-timings.jsonl`, `driver-questions.jsonl`, `driver-answers.jsonl`, `brief-sizes.jsonl`, `process` rows whose
   `run_class` comes from `STORY_RUN_CLASS=dry|smoke` set by the walker — and `run_counters.counters(task_root)` (the ONE function П1-б
   calls, §3.5 of П1-б) returns the same counters. Time rows and transcript rows (T9, T10, R1r) of a dry run are `n/a: stub roles`
   (decided by `run_class`, never by the `stub-` prefix); counts stay: returns per check, questions by kind, question repeats, briefs
   over ceiling, first-pass share by calls. `counters` writes nothing (П1-б's requirement). Invariant: no second road emits counters
   (P31); a dry scoreboard is never compared with a live one (K7; test row in N6: a dry file next to a live file → `not comparable`,
   no worse flags, no finding drafts).
10. **Limit edges** (inputs from outside: the judgment and truth YAML written by people; the env var `STORY_RUN_CLASS`): empty file,
    a card listed twice, an unknown verdict word, a 10,000-row file, non-UTF-8 bytes, nested lists where a scalar is expected — each
    refused by K1 naming the row, nothing written; variant rows AT (exactly the truth's card count) and BEYOND (one extra card) in N6.
    `STORY_RUN_CLASS`: absent, empty, `dry`, `smoke`, `DRY`, ` dry `, `live` (not in the table → `unknown`: `live` is the DEFAULT,
    not a value to set), a 10 KB value, non-ASCII — a variant row each in N1, AT/BEYOND on the 60-character quote of the note.
11. **TEMPORAL — fields that the change itself brings into existence** (CLAUDE.md rule 11 (i)): `checks`/`checks_n` (N0),
    `process` rows and `run_class` (N1), `resume_kind` (N2), `brief-sizes.jsonl` (N3), `rec["checks"]` in the exit record (N0),
    `bookkeeping_scripts` (N4b). World BEFORE: every reader treats the absence as «predates the writer» (§7.6), never as 0 or
    green; `exit_round` on a record written before N0 → `checks: ["unknown"]`. World AFTER: present. Between a writer's node and
    N4 (the reader) the row keys exist and no code reads them — declared here as readers-pending (AR-22), closed by N4's test rows.
    A `state/driver-state.json` saved by an older driver and resumed by a newer one keeps working (the new keys are optional).
12. **Counting rule of G1 (several checks on one refusal)**: a resumed call whose `checks` names k ids counts ONE return for EACH of
    them; its role seconds are attributed in full to each (the per-check seconds are labelled `shared` and do not sum to the total);
    the de-duplicated total of resumed seconds is printed once. Invariant: no second is invented or split by a guess; a reader adding
    per-check seconds sees the `shared` label. A refusal with no id is ONE `unknown` return — never dropped, never spread.
13. **Story_step output with no `checks:` line** (an exit-3 path other than `_gate_refusal`, or a broken line): `checks:
    ["unknown"]` + one note; the text the role, the conductor and the finding key see is byte-identical to today's (the driver
    removes only the last `checks: ` line). Invariant: the machine line never reaches a role prompt, a person or `finding_key`.
14. **Transcript edges (T9/T10)**: no transcript for a session → that session `unreachable` (counted, as `story_friction` does);
    a `tool_use` with no `tool_result` (session cut) → the call counted, seconds `unknown`; a result line with no `timestamp` →
    seconds `unknown`; several calls in one assistant message → per F16. Invariant: an unmeasured call is never 0 seconds.

## 8. Builder nodes (for a weaker model; PROJECT.md «Командная работа» п. 11)

Package nodes carry in `given`: `design/factory-rules.md` whole, `plans/builder-rules.md`, this spec. Witness of package nodes:
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <owns>` (builder-rules 7b `:15-18`); forge nodes:
`python -B experiments/measurers/test_measurers.py` (self-running, README `:34-38`). No new test file: new cases are variant rows
in the keep files named (C-7). Every package node's DoD: «census: no new unit» + `test_judgment_census.py` green; its
`architecture:` commit line names the AR rows of §1.1 it touches.

| Node | Owns (absolute) | What, expected behaviour, test per item | Depends | Parallel |
|---|---|---|---|---|
| N0 W0 check id producer (fix №14) | `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\detector_verdict.py` (`Record`, `parse`, `_link`, new `check_id`, new `with_check`), `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\exit_gate.py` (`detector_records`, `unreadable_record`, `witness_errors`, `all_errors`, `_finding_tag_of`), `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_core.py` (`Refusal`), `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_dispatch.py` (`form_report`, `handoff_ladder`, `finish`, `resume_with`, `exit_limit`, `exit_round`), `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_machine.py` (`resume_on_refusal`, `handle_refusal` — only the `exit_limit` calls at `:269, 299, 532`), `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_runner.py` (`run_claude`), `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\story_step.py` (`_gate_refusal`), `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py`, `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_driver_stop_record.py`, `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_story_step.py` | §2 W0 whole. Rows: (a) `parse` returns `labels` parallel to `findings`; a record of each exit-gate family carries its `check` (one row per family of `all_errors`, `:1866-1877`); (b) every record's TEXT unchanged (byte equality against today's on the same fixture); (c) `_finding_tag_of` reads the field and `word_class` gives today's class on today's fixtures (`WAITING_FINDING_TAGS` row); (d) `Refusal(findings=<records>).checks` = sorted unique ids, computed before stringifying; plain str → `unknown`; no findings and no `checks=` → `("unknown",)`; a subclass skipping `super().__init__` reads `()`; (e) `_gate_refusal` prints the `checks:` line last; `finish` removes it and the `Refusal.text` equals today's text (byte equality) and `finding_key` is unchanged; absent/broken line → `unknown` + note; (f) resumed rows of R-1, R-2, R-4..R-8 carry `checks`/`checks_n`, R-3/R-9 and every non-resume row carry no key; (g) `exit_round` reads `rec["checks"]`; a record with no key → `unknown`; (h) the adversarial inputs of W0 (each a variant row); (i) no regex over refusal text is added (grep the diff for `re.` additions outside `parse`'s existing match — listed in the report) | — | first; with N3, N5 |
| N1 W1 process rows + run class | `…\scripts\driver_machine.py` (function `run` only), `…\scripts\driver_journal.py` (new `run_class`, new `run_record` loader), `…\references\run-record.json` (new; key `run_classes`), `…\scripts\tests\test_driver_stop_record.py` | (a) start row at `run()` entry, end row in `finally` — shape §2 W1; test row: a scenario run writes exactly one start and one end row, keys exactly as listed; (b) no forbidden key — test row asserts the absent keys and that `collect_stall` K3 is unchanged on a journal with process rows; (c) fingerprint failure → `package: null` + one note; (d) Ctrl-C: `stopped_by_person` then end row with `process_code: null`; (e) `run_class` per §2 W1 and §7.10 (one variant row per input listed there); (f) a live-marked run with `stub-` sessions → `run_class: unknown` is computed in N4 (not here) — here only the writer | N0 (same files/test) | after N0 |
| N2 W2 resume_kind | `…\scripts\driver_runner.py` (`run_claude`), `…\scripts\driver_dispatch.py` (`handoff_ladder`, `resume_role`, `resume_with`, `exit_round`), `…\scripts\driver_machine.py` (`resume_on_refusal`, `handle_refusal` — the `run_claude` at `:546-549` only), `…\references\run-record.json` (key `resume_kinds`), `…\scripts\tests\test_driver_stop_record.py` | (a) token written on every resumed row: one test row per site R-1..R-9 with its token; (b) a token outside the table → `unclassified` + one note (P1); (c) the table loaded by the one loader `driver_journal.run_record`; (d) a non-resumed row has no key; (e) the builder re-runs the two Grep enumerations of W0 with the positive control and lists the 9 roads in the report — a NEW road found is a question to the Lead, not a guess | N0, N1 | after N1 |
| N3 W3 brief sizes | `…\scripts\brief_pack.py` (`build`), `…\scripts\tests\test_brief_pack.py`, `…\references\artifact-writers.json` only if state files are declared there | (a) one line per written brief; (b) none on dry-run / `--output`; (c) write failure → note, brief still written; test rows (a)–(c), AT ceiling (6,144 budget B → `over: []`) and BEYOND (6,145) | — (queue lines §10 №34) | with N0, N5 |
| N4 run_counters | `…\scripts\run_counters.py` (new), `…\scripts\driver_journal.py` (`read_rows_counted`, `question_rows`, `answer_rows`), `…\scripts\tests\test_retro_numbers.py` (+ `run_counters.py` in its keep `covers`), `…\scripts\tests\test-layers.json` (that covers row only; queue line §8.2) | `run_counters.counters(task_root) -> dict` and `--task-root --json`; writes nothing; every row of §2 T1–U1 with state measured/unknown/n/a; timings ONLY through `driver_timing.report` (fix №30); edges §7.1–7.3, 7.6, 7.9, 7.11, 7.12 each a table row; Q3 repeats row (AT: two answers same sha → 1 repeat; different kind same sha → counted under the later row's kind); friction row (fix №15): TWO test rows — «no key of the money vocabulary anywhere in the row» and «`turn_share` equals `story_friction`'s per role and total»; no money key in the whole dict (test row); `run_class` from the process rows incl. `mixed` and the `stub-` safety net; survivors called (AR-13/15 grep row); run on the LR2-1 arm state as extra evidence in the report (output attached; numbers compared with t-357 tables 1–4, every difference explained) | N1–N3 schemas, N0 keys (can start on fixtures) | with N4b, N5 |
| N4b call time (Lead bullet) | `…\scripts\friction.py` (`turns_of` additive keys, new `call_spans`, new `story_calls`, the shared session loop), `…\references\friction-markers.json` (new key `bookkeeping_scripts`, rows signed by the Lead, F15), `…\scripts\tests\test_friction.py` | per F15/F16 as decided; rows: (a) bookkeeping count and seconds per session on a fixture transcript; (b) refused/failed by `is_error`, split by `classify` kind; (c) §7.14 edges; (d) `code_friction.py`'s imports still return their old keys (compat row); (e) run on `tr:` for the automator's first three sessions, numbers reconciled with plan §8 (367 s / 50 calls; 201 s / 20 calls) in the report, every difference explained; no norm is written | F15, F16 answered | with N4 |
| N5 truth + judgment data | `C:\QAFactory\forge-repo\experiments\mybooks\truth\add-to-cart.yaml`, `C:\QAFactory\forge-repo\experiments\mybooks\factory-vs-free-agent\judgment.yaml` | truth: 24 cards, classes, two versions (`v2026-11-05-lead` from `SUMMARY.md:9-35`, `v2026-11-05-owner` from `:80-86`) each with its carrier line; judgment: LR2-1 rows for arms X/Y transcribed from `runs/blind-eval.md` + key, unsure rows marked `unsure: true`; no new judgment is made by the builder | — | with N0, N3, N4 |
| N6 scoreboard assemble/compare/norms | `C:\QAFactory\forge-repo\experiments\measurers\scoreboard.py`, `…\experiments\measurers\test_measurers.py`, `C:\QAFactory\forge-repo\experiments\scoreboards\norms.json`, `…\experiments\scoreboards\rows.json` | K1 (incl. `money`, `priced`), K2, K4, K5, K7; schema §4.2; edges §7.4–7.10; imports `run_counters` through `paths.SCRIPTS` (precedent `code_friction.py:28-39`); the commit that creates `norms.json` carries the axis-18 line and critic question 9 line (planted by the Lead, fix №23) | N4, N4b, N5 | — |
| N7 bar + release-check | `…\experiments\measurers\scoreboard_bar.py`, `…\experiments\measurers\test_measurers.py` | §3 items 2, 4; K3 per the F7 answer; transcript absent → `unknown`, never a bar of zeros | N6 (test file) | after N6 |
| N8 Lead | `docs/RUNBOOK.md` §9.5 (assemble step), the first scoreboard of LR2-1 | Lead-tier; everything shared with П1-а/П1-б goes to §8.1 | N6, N7, §8.1 | — |

### 8.1 Requirements to the Lead node «носители П1» (fix №17, №19; this spec's nodes do NOT write these files)

1. **Calibration check (ONE number, assigned by the Lead)** in `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, the П1-в part: per window
   (i) every live run of the window (RUNBOOK §9 notebooks) has a file in `experiments/scoreboards/`; (ii) `python -B
   experiments/measurers/scoreboard.py norms --check` green; every raise named with the owner's word; (iii) every red norm has a
   finding or an owner pass; (iv) the newest release tag's commit window holds a `release-check` line (or the owner's pass);
   (v) the `unknown` check share and `unclassified` resume kinds of the window's scoreboards are printed (a rise is a finding);
   (vi) empty window — explicit line. Leak detector: a notebook «Ход прогона» dated in the window with no scoreboard file.
2. **`ai-packages/qa-factory/design/architecture.md`**: AR-12 `Detector:` line names that check and the scoreboard (closing the gap
   at `:130`); AR-18 carriers name the `labels` key of `parse` and the `check`/`tag` fields of `Record` (N0).
3. **`docs/SIBLING_MAP.md`**: axis 6 row — `scoreboard.py`, `scoreboard_bar.py` (forge) and `run_counters.py` (package, beside the
   `friction.py` paragraph); axis 17 — `Record.check`/`tag`, `parse` `labels`, the story_step `checks:` line and its one reader
   `Driver.finish`; axis 18 — `norms.json` (same commit as N6, AR-20 / fix №23); axis 29 — `brief-sizes.jsonl` writer (N3).
4. **`PROJECT.md` «Релиз»**: one line «табло без красных норм (или слово владельца) — `scoreboard.py release-check`», shared with
   П1-б's «сухая стори зелёная» (plan §6) — one line for both, written once.
5. **Plan §6 items** (critic question «подан ли читателю выход сегодняшнего писателя», finding field «какой слой ниже должен был
   поймать»): П1-в does not rely on them as its detector (its detector is item 1); `scoreboard.py compare --findings` fills the
   finding field once the node defines it (§4.5).
6. Order: the Lead node lands after the fix round; item 3's axis-18 line and critic question 9 for `norms.json` land with N6.

### 8.2 Order on shared files (fix №17, №34, №35) — proposed `очередь:` lines for the Lead

- `ai-packages/qa-factory/scripts/tests/test-layers.json`: `очередь: package-ci/4 PC4-15 → forge/7 FG7-15 → forge/7 FG7-19 → П1-а
  (N1, N2) → П1-б (N3) → П1-в N4` (Lead decision §10: П1-а → П1-б → П1-в, after PC4-15, FG7-15, FG7-19).
- `brief_pack.py` / `test_brief_pack.py` (№34): П1-в N3 owns `brief_pack.py (build)`; `roles-context/2` RC2-1 owns `brief_pack.py
  (question_answer_lines)` and RC2-2 `story_step.py (_brief)`, both with `test_brief_pack.py`
  (`plans/piles/roles-context/batch-2-slova-cheloveka-v-brife.md:28-29`); `live-run-fvf/1` FV1-4 owns `brief_pack.py` (file level,
  `plans/piles/live-run-fvf/batch-1-live-run-fvf.md:37`). Disjoint functions with RC2-1 (PROJECT.md «Командная работа» п. 3), the
  test file is shared: `очередь: RC2-1 → RC2-2 → П1-в N3` on `test_brief_pack.py`; with FV1-4 (no function list): `очередь: П1-в N3
  → FV1-4` (plan §4: FV1 fixes after the layers) — the Lead confirms.
- `driver_dispatch.py`, `driver_machine.py` (№35): П1-в N0/N2 functions listed in their owns; `live-run-fvf/1` FV1-2, FV1-3, FV1-13,
  FV1-20, FV1-22 own `driver_dispatch.py`, FV1-6 owns `driver_machine.py`, file level (`batch-1-live-run-fvf.md:35, 36, 39, 45, 51,
  56`). `очередь: П1-в N0 → П1-в N1 → П1-в N2 → live-run-fvf/1 (FV1-2, FV1-3, FV1-6, FV1-13, FV1-20, FV1-22)` — compatible with plan
  §4; `story_step.py`: `очередь: П1-в N0 (_gate_refusal) ↔ RC2-2 (_brief)` disjoint functions, no order needed.

## 9. Four questions (CLAUDE.md rule 10)

(a) **Cost**: one `scoreboard.py assemble` + `compare` per live run (seconds, no model); the blind evaluation already happens per
comparison run (one critic dispatch — the existing LR2-1 procedure); one bar run per model id × story (money, F10); the Lead
signs each scoreboard (acceptance, minutes). Package cost: append-only lines per call/brief/process and one extra machine line on a
story_step exit 3 — no model spend; one transcript pass per live run for T9/T10 (seconds).

(b) **Axes** (map of 36 axes, `docs/SIBLING_MAP.md`):
axis 1: n/a — no policy/role-file change (designer/critic texts untouched). axis 2: n/a — no exam instrument. axis 3: covered —
`run-record.json`, `run_counters.py` ship in the package and reach the release copy by the normal copy; no installed-plugin
difference. axis 4: covered — FR walk §1.2; debt: none added. axis 5: covered — the 9 resume roads (S1–S9 repair loops) are
enumerated in W0 and N2 re-enumerates them. axis 6: covered — row listed in §8.1 item 3 (written by the Lead node). axis 7: n/a —
no per-test identity. axis 8: covered — run_counters takes `--task-root` and resolves nothing itself; forge tools take the root
as an argument. axis 9: n/a. axis 10: n/a. axis 11: n/a. axis 12: covered — finding drafts follow the pile protocol (§4.5).
axis 13 (the dispatch text — FIX ROUND №33): covered — no dispatch text changes: the `checks:` line is removed before the refusal
text is built (§7.13), and the resume prompt is byte-identical (N0 row e). axis 14: covered — transcripts read only through
`friction.py`. axis 15: n/a. axis 16: covered — JSON reads via `hooklib.read_json` in package nodes. axis 17: covered — the reader
`parse` gains `labels`, the contract and the producers are unchanged (closing rule `SIBLING_MAP.md:384`); the axis row is §8.1
item 3. axis 18: covered — `norms.json` is a ratchet (tighten-only); its axis line lands with N6 (§8.1 item 6). axis 19–20: n/a.
axis 21: n/a. axis 22: n/a. axis 23–28: n/a. axis 29: covered — W0–W3 append through `journal_run`/`hooklib.append_jsonl_line`.
axis 30: n/a. axis 31: n/a. axis 32: covered — §1.3/§1.4. axis 33: n/a — no dispatch identity read beyond the row's `dispatch`.
axis 34: covered — one road for both arms (§1.3, §3.2 refused calls) and for dry/live (§7.9, by `run_class`); the `n/a` rows of the
free arm are data-shaped, not language exclusions. axis 35: n/a. axis 36: n/a.
AR-13 (not an axis — moved here from the old axis-13 line, №33): queued — the five raw readers of `driver-questions`/
`driver-answers` (C-6) move to R1, and the raw `driver-runs.jsonl` parses in `driver_timing._rows` (`driver_timing.py:255`) and
`friction.story_friction` (`friction.py:345-364`) move to `driver_journal.read_rows`, in a follow-up node (finding written by N4).

(c) **Detector**: the calibration check of §8.1 item 1 (number by the Lead), with its leak detector.

(d) **What stops skipping**: the package writers sit on the execution path (every `run_claude`, every exit-gate record, every
`brief_pack.build`, every `Driver.run`); assembling is a RUNBOOK §9.5 step and the release check is a PROJECT.md «Релиз» step — on
discipline, with the §8.1 check as the named leak detector; promotion to a code gate (e.g. a release script refusing) follows
evidence of a leak.

## 10. Overlap with work in flight (AR-15, P31)

| Pile / batch | Node | Conflict / duplicate | Proposal |
|---|---|---|---|
| `speed-cost/6` (ожидает) | SC6-2 test-run counts per stage into `retro-numbers.json` (`batch-6…:24`) | duplicate risk: test runs per stage is a counter run_counters could also own; same file `retro_numbers.py` | run_counters does NOT count test runs; SC6-2 stays the survivor; the scoreboard reads `retro_numbers.test_run_counts` later (follow-up) |
| `execution-report/2` | DC1-24 `duration_ms` is not session time (`batch-2…:46`) | T8 depends on what `duration_ms` means | T8 uses `wall_ms` for time and `duration_ms` only for the hang indicator; DC1-24's fix must keep T8's test row green (line `очередь: execution-report/2 DC1-24 → P1-в N4`) |
| `execution-report/1,2` | CD1-6, CD1-20, CD1-32, CD1-34 (`retro_numbers.py`) | hot file | this spec does not edit `retro_numbers.py` (F3 keeps it out) |
| `execution-report/2` | OH3-20 tool_use counters in `friction.py` | the friction row inherits the +1 denominator defect; N4b edits `friction.py` too | note on the row (`friction: denominator includes handbacks until OH3-20`); `очередь:` between OH3-20 and N4b on `friction.py` — the Lead orders (disjoint functions if OH3-20 stays in `friction`'s counting loop) |
| `live-runs/2` | G3-1 teaches `stage_compare`/`code_friction` a task parameter (`:50`); LR1-19 «catalogue of references in `experiments/measurers/`» (`:67`); LR1-9 hidden-fact scenario (`:57`) | G3-1 owns those two files — no overlap with `scoreboard.py`; LR1-19's reference catalogue and the truth files are siblings (both «what the right answer is») | truth files live under `experiments/<stand>/truth/`; LR1-19 points there instead of a second carrier (Lead decides) |
| `live-runs/2` | LR2-1 table `factory-vs-free-agent.md` | the hand table this spec automates | after N8, the next comparison run fills the scoreboard; the markdown table stays as history |
| `roles-context/2` (fix №34) | RC2-1 `brief_pack.py (question_answer_lines)`, RC2-2 `story_step.py (_brief)`, both `test_brief_pack.py` | shared files with N3 (and story_step with N0) | §8.2 queue lines |
| `live-run-fvf/1` (fix №34, №35) | FV1-4 `brief_pack.py`; FV1-2/3/13/20/22 `driver_dispatch.py`; FV1-6 `driver_machine.py` | shared files with N0, N1, N2, N3 | §8.2 queue lines |
| `package-ci/4`, `forge/7` (fix №17) | PC4-15/17/18, FG7-15, FG7-19 own `test-layers.json` / `scenario_walk.py` | shared `test-layers.json` with N4 | §8.2 first line |
| `cost-dashboard/1` | closed (`batch-1…:3`) | — | — |
| `run-honesty/2` | closed (`batch-2…:3`) | — | — |
| `live-run-fvf/1` | FV1-21 (`task_price`) | chat money line depends on it (C-3) | no change |
| plan siblings П1-а, П1-б | dry story emits counters | §7.9 is the requirement; the dry story spec owns its harness, the stub's `session_id: stub-<dispatch>-<n>` and setting `STORY_RUN_CLASS` | — |

## 11. Forks returned to Lead

| # | Fork | Options | Consequences | Recommendation |
|---|---|---|---|---|
| F1 | Where the assembler lives | (a) package `run_counters.py` (data) + forge `scoreboard.py` (truth, judgment, comparison, storage); (b) all in forge; (c) inside `retro_numbers.py` | (a) dry story / smoke / every real run print the same counters (plan point 5) and forge adds stand-only parts; (b) dry story in CI cannot reach a forge tool, two roads; (c) hot file in 3 piles, retro runs only at S9 | (a) |
| F2 | Operator-intervention time | (a) data classes from W1 (package/config change, restart without answer), inside-gap split `unknown`; (b) plus an operator label file read by the scoreboard; (c) everything «not established» | (b) brings back the hand notebook the goal removes; (c) loses what data can tell | (a) |
| F3 | One definition of first pass / rework | (a) by `resume_kind` + controller dispatch rounds (`retro_numbers.dispatch_rounds`, scope rule) — run_counters owns it, `retro_numbers.resume_metrics` delegates later; (b) t-357's ordinal rule (`t-357:102-106`); (c) both, labelled | (b)/(c) two roads to one number (AR-15, P31); (a) needs W2 | (a); the follow-up moving `resume_metrics` to delegate is queued to `execution-report` after CD1-* |
| F4 | What a gate «caught» | (a) Lead judgment row per gate at scoreboard acceptance; (b) code proxy (the artifact changed beyond the refused fields); (c) not judged, only cost printed | (b) is code judging meaning (AR-29 breach); (c) leaves plan point 4 unanswered | (a); absent row = `not judged`, never «caught nothing» |
| F5 | Auto-filing findings | (a) code writes the finding file into the pile from `rows.json` and prints the card/batch rows for the Lead; (b) code also edits card and batch; (c) code prints a draft only | (b) needs a `piles.py` command not established here and touches frozen-batch rules; (c) is not «automatically» | (a) |
| F6 | Tightening norms | (a) printed proposal, Lead commits; (b) automatic tightening to the best measured value on every run | (b) one lucky run sets an unreachable norm; (a) costs a Lead edit per run | (a) |
| F7 | **Owner question.** Что делает красная норма с релизом? | (а) релиз запрещён, пока все нормы не зелёные; (б) релиз запрещён, пока владелец не написал «выпускаем с красной нормой N, потому что …» (слова записываются); (в) только строка в отчёте релиза | (а) один неудачный прогон держит все релизы; (в) нормы никого не останавливают; (б) остановка с дверью (FR-4, P13) | (б) |
| F8 | **Owner question.** С чем сравнивать время фабрики? | (а) вся стена, включая починки оператора; (б) стена без промежутков вмешательства + отдельной строкой вся стена; (в) только стена первой попытки (цель плана §5: не больше чем вдвое) | (а) наказывает фабрику за правки форджа во время прогона; (в) прячет переделки | (б) как норма, (в) как цель |
| F9 | **Owner question.** Какая версия правды считается? | (а) последняя со словом владельца (05.11, 6 багов); (б) обе, табло печатает счёт по обеим; (в) владелец подписывает версию перед каждым прогоном | (б) удваивает строки; (в) лишний вопрос на каждый прогон | (а), версия названа в табло; новая версия — только словом владельца |
| F10 | **Owner question.** Планка свободного агента стоит денег на каждый новый прогон модели/стори. Делать? | (а) да, раз на версию модели и стори; (б) только по слову владельца; (в) одна планка навсегда | (в) сравнение устаревает при новой модели | (а) |
| F11 | Raw records in the repo | (a) only scoreboard YAML + sha256 of sources; (b) commit money-stripped copies of the state files for re-assembly | (b) re-assembly possible but large files and a stripping step that can leak money (C-8) | (a) |
| F12 | Release check on a stand without a truth table | (a) quality norms `unknown` count as red (owner pass needed, F7); (b) `unknown` passes silently | (b) breaks AR-28 | (a) |
| F13 | Scope: live runs in real projects (not the stand) | (a) package counters for every run; the forge scoreboard only for runs the forge drives; (b) forge scoreboard for every run including users' | (b) needs user runs' files in the forge (P8 for comparison runs; privacy) | (a) |
| F14 | The brief row's unit | (a) `budget_bytes` vs ceiling (the ceiling's own unit, C-2); (b) file bytes | (b) re-states the plan's wrong «41 of 41» | (a); the Lead corrects plan §1 row 5 |
| F15 | **NEW (fix round).** Source of bookkeeping / refused-call time per role session (§2.1) | (a) host transcript, structurally (`timestamp`, `tool_use`, `tool_result.is_error`), computed in `friction.py`; bookkeeping list a data key signed by the Lead; (b) a new self-log writer `state/script-calls.jsonl` called by every role-facing script and by the guard; (c) host PreToolUse/PostToolUse hook records, after one experiment on whether a failed call fires the post event | (a) no new writer, one road with FR-55; Claude host only (Codex `unknown`); counts time around the call as the model spends it (F16); (b) host-independent and authoritative on exit codes, but execution time only, every script and `stage_guard.py` (hot) must call it, session attribution ambiguous with parallel S5 windows; (c) an unknown host property — measurement first (hygiene 6(a)); a hook on every tool call costs every role turn a process | (a); the initial `bookkeeping_scripts` rows = t-391's split (manifest scripts, `s5_precheck.py`, `handoff_check.py`, fragment writes), signed by the Lead; (b)/(c) only on evidence that (a) misses a class |
| F16 | **NEW (fix round).** What «time of a call» is (T9/T10) | (a) execution: `tool_use` line ts → `tool_result` line ts; (b) turn-attributed: from the previous transcript event to the `tool_result`, a multi-call assistant message's time split evenly among its calls; (c) both as two rows | (a) undercounts what t-391 measured (7.3 s per bookkeeping call is mostly model time); (b) matches «what the role spent» but the even split is a convention; (c) two metrics — each its own comparison line (hygiene 6(b)) | (c), with (b) as the row a future norm is set on; N4b reconciles both with t-391 |
| F17 | **NEW (fix round).** Transport of check ids across the story_step process boundary (R-5 (ii)) | (a) one machine line `checks: <json>` as the LAST stdout line of `_gate_refusal`, removed by `Driver.finish` before the refusal text is built (`next:`/`parse_next` precedent); (b) a file `state/findings/<dispatch>-finish.checks.json` beside the `-finish.txt` story_step already writes (`story_step.py:2014`); (c) no transport: finish refusals stay `unknown` | (a) one process, no stale file; on the skill road (no driver) the orchestrator sees one extra machine line in story_step's stdout; (b) nothing in the text, but a file from an earlier exit 3 of the same dispatch can be read as fresh unless it carries the dispatch and a stamp the driver checks; (c) the plan's main target — `row-fields-missing` returns through the finish road — may land in `unknown` | (a) |
| F18 | **NEW (fix round).** Structured-artifact refusals (R-8, `controller.py` accept path) carry no id | (a) `unknown` now (counted, printed), a finding queued for a controller producer (`controller.py` is a hot file, PROJECT.md «Командная работа» п. 3); (b) this spec adds the controller producer (hot file in several piles) | (a) R-8 returns sit in the `unknown` line until the follow-up; (b) widens this spec into `controller.py` | (a) |
| F19 | **NEW (fix round).** Granularity of the counting key | (a) `<producer>:<label check>` (closed family, e.g. `s5_precheck:manifest`) with the tag (`row-fields-missing`) on the record for drill-down only; (b) `<producer>:<tag>` (e.g. `s5_precheck:row-fields-missing`) | (b) some tags carry variable parts (`relative-oracle-<file:line>`, `provisional-dependents-<id>`, `s5_precheck.py:2560, 2848, 2126`), so one gate splits into many keys and a per-gate norm stops meaning anything; (a) is closed, but today's family `manifest` equals row-fields-missing only by coincidence (one finding of that family) | (a); a family holding several findings that the norm must tell apart becomes a data row naming its stable tags (follow-up, on evidence) |

## Small technical choices closed by the designer

- All stored times UTC ISO 8601 with offset; local time only in chat.
- `process` end key `process_code`, not `exit_code` (W1 invariant).
- Package fingerprint once per process.
- `brief-sizes.jsonl` via `hooklib.append_jsonl_line`; written in `build`, not `main`.
- Scoreboard format YAML (P4); file name `<YYYYMMDD-HHMM>-<version>-<arm>.yaml`.
- Phase split of the free agent printed as advice, never stored.
- `run_counters` prints no money; the driver does not call it at exit (no new artifact; the counters are derived on demand).
- Counted reader variants added beside the existing readers instead of changing their return type (callers unchanged).
- (fix round) Resume kinds and run classes share one data file `references/run-record.json` with one loader
  `driver_journal.run_record` (the draft's `resume-kinds.json` is folded into it); bookkeeping scripts go into the existing
  `friction-markers.json` (its reader is the code that uses them).
- (fix round) The row carries check families (`checks`, `checks_n`), not tags — bounded by the closed family set, so no cap is
  needed; the tag stays on the record and in the findings files the driver already writes.
- (fix round) Handoff-form check id = `handoff_check:` + the problem's field `path` with list indices dropped (`scope[2].reason` →
  `scope[].reason`), a mechanical transform of a structured field.
- (fix round) G1 attributes a shared resumed call's seconds in full to each check, labelled `shared`, total printed once (§7.12).
- (fix round) `STORY_RUN_CLASS` value `live` is not in the table and reads `unknown`: `live` is the default, never a set value.

## Lead decisions on the forks (13.11.2026, at acceptance of draft t-398)

- F1 (a), F2 (a), F3 (a), F4 (a), F5 (a), F6 (a), F11 (a), F12 (a), F13 (a), F14 (a) — as recommended.
- F7, F8, F9, F10 — owner questions, asked 13.11; until the owner's word the nodes follow the recommendations
  (F7 (б), F8 (б) as the norm and (в) as the goal, F9 (а), F10 (а)); nothing irreversible depends on them before N8.
- §0 corrections C-1 and C-2 verified by the Lead on the carriers (the arm's state folder holds `driver-timings.jsonl`;
  35 of 41 briefs are over the ceiling in budget bytes) and carried into the Lead plan.
- Added by the Lead from recon t-391: the scoreboard carries, per role session, the time of factory bookkeeping calls and
  of refused/failed calls as rows of their own (the automator's first pass: 34 % bookkeeping, 20 refused calls) — the
  source is the role's transcript or a driver record; the critic checks whether §2 already covers it, otherwise a fix-round item.
  (Fix round: not covered before; now rows T9/T10, §2.1, node N4b, forks F15/F16.)

## Fix round t-401

One line per finding addressed to П1-в. Lead decisions applied as given (plan §10); none re-decided.

| № | What changed and where / why not |
|---|---|
| 14 | Producer node N0 (§8) before N2: W0 (§2) enumerates the 9 resume roads by two Grep runs with control (5 run_claude sites + 3 resume_with callers + the driver's own), names the id each carries, the one writer per field (`Record.check`/`tag`, `Refusal.checks`, story_step `checks:` line, `run_claude` row keys), every reader in the same commit (`_finding_tag_of`, `finish`, `resume_with`, `exit_limit`/`exit_round`, `run_claude`), edges (several checks — §7.12; no id → `unknown`, counted, printed — W0, §7.13), error direction and adversarial inputs; W2 tokens restated as SITE roads, not text classes; C-5 rewritten; no regex over refusal text (N0 row i). New forks F17, F18, F19 |
| 15 | §2 R1r: turn shares and counts only, money keys dropped by name (`priced_cost`, `fric_cost`, `money_share`, `priced_turns`, `unpriced`, `helpers` paths); K1 vocabulary + `money`, `priced`; N4 test rows «no money key in the row» and «shares equal»; §1.1 AR-12 row |
| 16 | §2 W1: `run_class` from `STORY_RUN_CLASS` (`dry`, `smoke`; absent → `live`; other → `unknown`), one reader `driver_journal.run_class`, written into the `process` start row only, invariant «a dry scoreboard is never compared with a live one» (K7, test row §7.9/N6); edge battery §7.10; C-12 |
| 17 | Shared documents moved out of N8 into requirements to the Lead node «носители П1» (§8.1); calibration check «45» replaced by «one number assigned by the Lead»; `test-layers.json` order line §8.2 |
| 18 | §7.9: stub `session_id: stub-<dispatch>-<n>` (written by П1-б); function `run_counters.counters(task_root)`; new row Q3 «question repeats» (§2) from the driver's own `question_sha` |
| 19 | §8.1 item 5: П1-в does not use plan §6 (a)/(b) as its detector; its detector is the §8.1 check; the finding field is filled by `compare --findings` once defined |
| 23 | §1.1 AR-20 row, N6 DoD, §8.1 item 6: the axis-18 line and critic question 9 for `norms.json` land in the same commit as N6 |
| 29 | C-11 added; W2 bullet corrected: `resume_reason` is read by `retro_numbers.resume_metrics` (`:1721`) — the second rework definition until F3's delegation node |
| 30 | R1: `read_timings` dropped; T4/T5 and U1 read `driver_timing.report` (`driver_timing.py:241-286`); its own raw parse of `driver-runs.jsonl` (`:255`) queued under AR-13 (§9) |
| 31 | Rows T9/T10, §2.1 (sources weighed, recommendation, relation to `friction.py`/`code_friction.py`), node N4b, forks F15/F16, C-13 |
| 32 | C-8: «established — committed (`4e00ed7`), 120 `total_cost_usd`», re-counted by Grep this session; money-in-repo reported to the Lead as a finding outside this spec |
| 33 | §9 (b): axis 13 rewritten as «dispatch text» (covered: no change, §7.13); the raw-readers line moved to an AR-13 line |
| 34 | §10 rows `roles-context/2` RC2-1/RC2-2 and `live-run-fvf/1` FV1-4; §8.2 queue lines |
| 35 | §10 row `live-run-fvf/1` FV1-2/3/6/13/20/22; §8.2 queue line; N0/N1/N2 owns carry function lists |
| 37 | Nothing to cut in П1-в beyond №30 (the critic's own words: «ничего лишнего не вижу, кроме дубля №30»); fixed by №30. N0 adds a cost the critic did not price: one story_step machine line and an exit-gate record field — no model spend (§9 (a)) |

Not addressed to П1-в (no change here): №1–13, №20–22, №24–28, №36.

New forks: F15, F16, F17, F18, F19 (§11). Owner questions F7–F10 unchanged, still open.

Reported to the Lead, not fixed (outside scope): money in a committed repo file (C-8); `s7_reorder.py:73-74` writes naive local
time (T-utc); `driver_timing._rows` and `friction.story_friction` parse `driver-runs.jsonl` raw (AR-13, §9).

## Reading trail

Draft round (t-398): `docs/tasks/specs/20261113-plan-fabrika-ne-huzhe-agenta.md:1-189`;
`docs/tasks/specs/reports/t-357-fvf-time-split.md:1-220`; `experiments/mybooks/factory-vs-free-agent/factory-vs-free-agent.md:1-82`;
`runs/outcome-factory.md:1-60`; `runs/factory-3.log:1-40`; `runs/.gitignore:1-4`; `copy:driver-runs.jsonl:1-8`;
`experiments/mybooks/disputed-check-plain-agent/SUMMARY.md:1-87`; `docs/tasks/specs/reviews/t-354-tests-factory-vs-free.md:1-202`;
`experiments/measurers/README.md:1-39`; `experiments/measurers/code_friction.py:1-190`; `experiments/measurers/stage_compare.py:1-60`;
`paths.py` (Grep lines 12-198); `arm:driver-timings.jsonl:1-25`; `arm:driver-questions.jsonl:1-6`; `arm:driver-answers.jsonl:1-4`;
`arm:` folder listing; `arm:../../records/journal.jsonl:1-5` + Grep counts; `pkg:scripts/driver_runner.py:340-430, 625-650, 720-830`;
`pkg:scripts/driver_timing.py:1-80`; `pkg:scripts/driver_journal.py:1-80, 321-360` + def list; `pkg:scripts/driver_machine.py:1760-1804`;
`pkg:scripts/retro_numbers.py:1-70, 1211-1265, 1687-1756, 1918-2142` + def list; `pkg:scripts/brief_pack.py:4540-4573` + Grep `:54, :4535`;
`pkg:design/architecture.md:120-244`; `pkg:design/factory-rules.md:371-417`; `pkg:scripts/tests/test-layers.json:30-69, 1400-1417,
1736-1753, 4425-4443` + Grep; `docs/RUNBOOK.md:17-51, 170-369, 531-578`; `plans/piles/live-runs/batch-2-live-proofs.md:1-78`;
`plans/piles/speed-cost/batch-6-tsena-i-samouluchshenie.md:1-46`; `plans/piles/cost-dashboard/batch-1-true-price.md:1-40`;
`plans/piles/run-honesty/batch-2-run-honesty.md:1-45`; `plans/piles/execution-report/*` (Grep); `findings-1413/…/live-run-fvf/README.md`,
`batch-1-live-run-fvf.md:57`, finding `20261112-cena-lozhno-nepolnaya-iz-za-shagov-koda.md:1-37`; `docs/SIBLING_MAP.md` headings + `:159-181`;
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:1087-1094` + numbering Grep; `plans/MEASUREMENTS.md` (Grep, C-9); `plans/builder-rules.md` (Grep 7b).

Fix round (t-401), read this session: the review `docs/tasks/specs/reviews/t-401-p1-layers-plan-review.md:1-431` (whole); plan
§6–§10 (`20261113-plan-fabrika-ne-huzhe-agenta.md:137-241`); П1-б `20261113-p1b-dry-story-spec.md:195-219` + Grep
(`STORY_RUN_CLASS|stub-|повтор|repeat|run_counters|counters\(` → one hit `:209`); `pkg:scripts/driver_core.py:90-159, 612-641`;
`pkg:scripts/driver_dispatch.py:130-189, 285-360, 505-594, 800-850, 1015-1044, 2040-2099, 3582-3626` + Grep `resume_reason`,
`resume=[a-z]`, `\.resume_with\(`, `self\.exit_limit\(`, `^STRUCTURED_RE`, `RESUMABLE_HEADS|resume_*` actions, def list;
`pkg:scripts/driver_machine.py:36-65, 160-309, 515-564`; `pkg:scripts/driver_runner.py:770-914`; `pkg:scripts/exit_gate.py:60-159,
430-469, 1765-1832, 1850-1939` + Grep imports/`kind=`; `pkg:scripts/detector_verdict.py:1-102, 215-344` + Grep; `pkg:scripts/s5_precheck.py:262-293,
3740-3784, 3915-3926, 4060-4079` + Grep `ROW_FIELDS_TAG`, `_finding\("manifest"`, literal/variable `_finding(` counts;
`pkg:scripts/story_step.py:2004-2113` + Grep; `pkg:scripts/friction.py:1-428` (whole); `pkg:references/friction-markers.json` (whole);
`pkg:references/role-commands.json:1-40, 170-194` + Grep; `pkg:scripts/driver_timing.py:190-300`; `pkg:scripts/driver_dialog.py:290-419`;
`pkg:scripts/driver_conductor.py:238-251`; `pkg:scripts/driver_s0.py:403-410`; Grep `question_sha`; `pkg:design/architecture.md:35-40, 233-238`
+ Grep; `pkg:scripts/tests/test-layers.json:27-35 (sections), 1239-1302, 1400-1417, 1738-1753, 6164-6175` + Grep keys;
`docs/SIBLING_MAP.md:373-385` + axis headings (36 axes); `plans/piles/roles-context/batch-2-slova-cheloveka-v-brife.md` (Grep
`brief_pack`); `.claude/worktrees/read-main/plans/piles/live-run-fvf/batch-1-live-run-fvf.md` (Grep FV1 rows); `plans/piles/forge/batch-7-vhodyashchie-4.md`
(Grep FG7-15/19); `plans/piles/package-ci/` (Grep PC4-15/17/18); `tr:` folder listing, Grep `"timestamp"` count on one file, Grep
`"is_error":true` over the folder; `experiments/.../factory-out/state/driver-runs.jsonl` Grep count `total_cost_usd`.

Negative claims with controls (fix round): «no caller knows a check id» — `Refusal` fields read whole (`driver_core.py:117-139`);
«no package hook/guard file writes a per-call record» — Grep `[a-z_-]+\.jsonl"` over four named files finds only `journal.jsonl`
(the hit is the control; scope: those four files, not the package); «only one `_finding("manifest"`» — count 1, control 13 for
the literal shape; resume-site enumeration — controls named in W0. Not verified (labelled in place): that the host marks guard
refusals `is_error` (§2.1 (a)); whether a failed tool call fires a post-tool hook event (F15 (c)); the committed status of the
copy (from the critic's `git ls-files`; this session has no git).

Not read (named so the Lead can judge sufficiency): t-391's report (only its numbers in plan §8); `notebook.md`; `runs/blind-eval.md`;
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` this round; `tools/piles.py` subcommands; `scenario_walk.py` rows for the owned paths;
`handoff_check.py`'s `--json` `problems[].path` shape beyond the driver's reader (`driver_dispatch.py:352-353`).

## Owner's word, 13.11.2026 (overrides the text above where they differ)

Recorded by the Lead from the owner's answers in session; the nodes are cut from the spec AS AMENDED here.

1. **Money is a scoreboard row** (owner: «Деньги в файл репозитория не пишутся — это правило фабрики, а не форджа. У нас для
   сравнения деньги один из самых важных критериев»). P18's ban covers what the FACTORY writes into a target project (the
   report); it does not cover the forge's own comparison data. Therefore:
   - row X1 becomes a stored, normed row: the task price from `task_price.task_price` (agreement value, or the range with its
     note — never a naive sum of cumulative `total_cost_usd`, trap T-cum stays); the bar file carries the free arm's price from
     its result JSON; one comparison line factory vs agent, same unit;
   - K1 loses the money-vocabulary refusal; §4.2's «no money key» sentence, §4.3's P18 ground and §4.4's «chat only: money» are
     void; raw records still are not copied for size and path reasons (F11 (a) stays);
   - R1r keeps turn shares; the money keys of `story_friction` (`priced_cost`, `fric_cost`, `money_share`) are no longer dropped
     by name — they are rows of the forge scoreboard; test rows «no money key» are replaced by «money row equals `task_price`»;
   - `run_counters` in the PACKAGE still prints no money into project files (P18 unchanged there); money is joined in the forge
     `scoreboard.py`;
   - C-8 / fix №32 «money in a committed repo file» is NOT a defect: `runs/factory-out/state/driver-runs.jsonl` stays.
2. **F7, red norm vs release — a ratchet, not a wall** (owner): now a red norm is a WARNING line in the release report. Once a
   row is BETTER than the free-agent bar in a released version, that row is ratcheted: a later release where it is worse than in
   the previous release goes out only with the owner's recorded word. `norms.json` carries per row `ratcheted_since: <version>`;
   `scoreboard.py compare` prints `release: owner's word needed -- <rows>` for ratcheted rows that worsened, a warning for the rest.
3. **F8** — as recommended: the norm compares wall without operator intervention gaps; the whole wall is its own row.
