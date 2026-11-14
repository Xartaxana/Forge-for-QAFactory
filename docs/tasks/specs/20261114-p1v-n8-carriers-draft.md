# t-794 — P1-v N8: Lead-tier carrier texts (DRAFT for the Lead)

designer, 14.11.2026. Repo read: `C:\QAFactory\forge-repo\.claude\worktrees\wave13` (origin/main, N0-N7 merged). Every code fact below
was read in that tree; line numbers are of that tree. Nothing was written except this file; nothing was run.
Spec: `docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md` §8.1 (:455-473), N8 row :453, §9 (:490-522); amendment
`docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md` (§8.1 item 4 re-worded at :494, K3 at :482, money at :476-478);
topic critic `docs/tasks/specs/reviews/20261114-p1v-tail-topic-critic.md` (P1 :50, answer 8 a-g :67-74).

## 0. Where the merged code differs from the spec (the carriers follow the code)

| # | Spec says | Merged code does | Consequence for the carriers |
|---|---|---|---|
| D1 | §8.1 item 4 / spec K3: release check = "no red norm (or the owner's word)" | `release_lines` prints a red unratcheted norm as `release: warning -- <row> red: ...` (`scoreboard_bar.py:325-333`); `release_check` exits 1 ONLY on `release: owner's word needed -- ...` lines (`:390-413`), which come from `ratchets` elements (`:305-311`) and OQ2 bars. The amendment already re-worded item 4 this way (amendment :494, :482). | The PROJECT.md line and check 47 say "red norm = warning; a ratcheted row worse/unknown/absent = owner's word" |
| D2 | §3 item 2: `scoreboard.py bar --transcript --result` measures wall, turns, tool calls, person rounds, refused calls | no `bar` subcommand: `scoreboard.py` has assemble/compare/norms/release-check (`scoreboard.py:1013`); `scoreboard_bar.py price` only PRINTS a price line (`scoreboard_bar.py:448-456`); nothing writes `bar-<model>.yaml` (readers only: `_bars` `:227-235`, `_judge_one` `scoreboard.py:610-633`, `assemble --bar` `:826`) | Fork 7(a); AR-12 line names "the bar has no writer" |
| D3 | §8.1 item 1 (v): the `unknown` check SHARE and `unclassified` resume kinds of the window's scoreboards | the scoreboard file carries row `G1u` = `G1.unknown_check.returns` (`rows.json:21`) and `U1` = count of `U1.lines` (`rows.json:28`); NOT the share (`G1.unknown_check.share`, `run_counters.py:376-377`) nor `U1.unclassified_resume_kinds` (`run_counters.py:667`) | Check 47 (e) reads G1u from the file and the other two from `run_counters.py --json` while the task root exists; fork 7(d) adds two data rows |
| D4 | N3/N4: `brief-sizes.jsonl` rows carry `budget_bytes`, `ceiling`; B1 = briefs over the ceiling | FV1-4 (accepted f3167f3, `plans/piles/live-run-fvf/batch-1-live-run-fvf.md:37`) reshaped the writer to `{ts, stage, role, dispatch, bytes}` (`brief_pack.py:4289-4300`, docstring: "which no reader in the package reads" — false); `run_counters._briefs` still reads `budget_bytes`/`ceiling` (`run_counters.py:553`) and counts a row without them as `unreadable_rows`, returning `state: measured` with `over: 0` (`:564-565`) | **Finding F-1** (below): an unknown reported as a measured 0 (FR-41, AR-22, AR-28). The axis-29 row says so |
| D5 | §2 T9/T10 from N4b `friction.call_spans` | `run_counters` sets T9/T10 `unknown` "not read here" on every non-simulated run (`run_counters.py:636-638`) although `friction.call_spans` exists (`friction.py:373`) | Finding F-2 (rows T9/T10 are always unknown on the factory arm) |
| D6 | README: "`pytest` over `test_measurers.py` collects no tests" (`experiments/measurers/README.md:55`) | 18 parameterised `test_scoreboard_*` functions (`test_measurers.py:3107-3193`, pytest optional `:1653-1662`); the self-running `main` runs the same tables (`:3197-3207`, `:3353`) | Finding F-3 (stale README line); fork 7(b) uses the self-running form |
| D7 | §9(b): "map of 36 axes" | `docs/SIBLING_MAP.md` has 37 axes (axis 37 at :620) | item 8 enumerates 37 |

## 1. Calibration check 47 — `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`

**Target**: `C:\QAFactory\forge-repo\PROCESS\WEEKLY_CALIBRATION_PROTOCOL.md`.
**Anchor**: after the line that begins `46. **Task id race: dispatch id differs from its journal line (F6-58, ...` (ends `...this check is its leak detector.`), before the blank line and `## Closing out a run`. One blank line before, as between 45 and 46.
**Exact text** (one paragraph line, the form of 43-46):

```
47. **The run scoreboard: every live run has its file, norms only tighten, a red has an owner (P1-v, spec `docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md` §8.1 item 1; AR-12, AR-20; SIBLING_MAP axes 6, 18).** Mechanism: `experiments/measurers/scoreboard.py` (`assemble`, `compare`, `norms`, `release-check`) and `scoreboard_bar.py` over the package's `scripts/run_counters.py` and `scripts/task_price.py`; the data `experiments/scoreboards/rows.json` and `experiments/scoreboards/norms.json` (schema `norms/2`, tighten-only); the morning step of `docs/RUNBOOK.md` §9.5 that assembles a live run's file; the PROJECT.md «Релиз» line. Per window, with the command beside every number (hygiene 6(b)): (a) every live run of the window — a notebook under `experiments/` whose «Ход прогона» holds a start line dated in the window (`grep -rln "^## Ход прогона" experiments/`; positive control: `experiments/mybooks/factory-vs-free-agent/notebook.md` must hit) — has a file `experiments/scoreboards/<stand>/<story>/<YYYYMMDD-HHMM>-<version>-factory.yaml` whose UTC start is that run's; a run with none is a finding against the morning step; while `experiments/scoreboards/` holds only `rows.json` and `norms.json`, the line says "no scoreboard yet" and every live run of the window is listed as a leak — never a pass; (b) `python -B experiments/measurers/scoreboard.py norms --check --against <old>`, where `<old>` is `experiments/scoreboards/norms.json` as it stood at the window's start, saved to the scratchpad from `git -C <repo> show <sha>:experiments/scoreboards/norms.json` (`--check` alone sees only a value looser than its own `initial` or last raise; a changed `initial`, a dropped or unset norm, appended-only raises, a removed or worsened `ratchets` element need `--against`): it prints `norms: green` and exits 0 (exit 1 with `RED:` lines is a finding; exit 2 is an unreadable file, named, never a pass); then `git log -p -- experiments/scoreboards/norms.json` over the window: every `norm` tightened, `ratchets` element added, and `raises`, `worsened_passes` or `bar_changes` entry added is listed; every raise and pass carries `raised_by`, `reason` and the owner's `word`, and the word is checked against a session with the owner (PROJECT.md «Командная работа» п. 6) — a word not found there is a finding; (c) for every scoreboard of the window, `python -B experiments/measurers/scoreboard.py compare <file>`: every `norm <id> [<row>]: red` line has a finding (a `compare --findings` file or a hand-written one in `plans/piles/*/findings/`) or the owner's pass printed beside it (`passed by the owner's word: ...`, recorded by `assemble --pass NORM WORD DATE`); every `-- worse` row line has a finding; a red or worse with neither is a finding against the Lead; `unknown` and `undecided` lines are written down with their reason and counted as neither green nor red; (d) the newest release of the window (a `vX.Y.Z` tag of `Xartaxana/QAFactory`; the version argument is the `version` of `ai-packages/qa-factory/.claude-plugin/plugin.json`, with no `v`, the spelling the scoreboard file names carry): the verbatim output of `python -B experiments/measurers/scoreboard.py release-check --release <X.Y.Z>` stands in the witness of the release's `accepted` journal event with exit 0, and every `release: owner's word needed -- ...` line has its `worsened_passes` (row, version, pair, factory model) or `bar_changes` entry in `norms.json` with the owner's word; a release with no such output is a finding; `release: warning` lines (a red unratcheted norm, an unknown row, "no live factory scoreboard of <version>: nothing judged") are listed — they do not change the exit by the owner's word (amendment `docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md:482`); while `norms.json` holds no `ratchets` element the command prints `release: no previous release -- ratchet not judged` and exits 0 — written down as "nothing ratcheted", never as a pass of the release; (e) per window scoreboard, the value of row `G1u` (returns naming the `unknown` check) against the previous window's; and, while the run's task root is still on disk, `G1.unknown_check.share` and `U1.unclassified_resume_kinds` of `python -B ai-packages/qa-factory/scripts/run_counters.py --task-root <root> --json` (the scoreboard file does not carry these two); a rise is a finding; a removed root gets "not readable: task root removed", never 0; (f) a window scoreboard whose `run.run_class` is not `live` is listed with its class: it judges no norm (K7) and is never counted as a green run; (g) an empty window (no live run) gets an explicit line, not a zero. Detector of this check's own leak: a notebook «Ход прогона» start line dated in the window with no scoreboard file of that run and no line (a) in the calibration record; a window whose `git log -- experiments/scoreboards/norms.json` is not empty and whose record carries no line (b).
```

**Facts checked**
- Subcommands `assemble`, `compare`, `norms`, `release-check`: `experiments/measurers/scoreboard.py:1013-1050`; `release-check` arguments `--release`/`--version`/`--lines`/`--norms`/`--root`: `scoreboard_bar.py:420-426`.
- `norms --check [--against]`, `--norms`, `--convert`: `scoreboard.py:1042-1046`; prints `RED: <problem>` and `norms: green|red`, exit 1 on red: `:1004-1008`; refusal exit 2 via `_red`: `:923-925`.
- What `--check` alone vs `--against` enforces: `check_norms` `scoreboard.py:516-589` (alone: raises shape, value vs `initial`/last raise `:548-563`, row raises `_row_problems` `:489-513`; with `against`: raises append-only `:566-572`, ratchets `_ratchet_problems` `:455-486`, dropped norm `:574-577`, changed `initial` `:579-580`, unset value `:585-586`, looser value without new raise `:587-588`).
- File name `<YYYYMMDD-HHMM>-<version>-<arm>.yaml` from the UTC first time, folder `<out-root>/<stand>/<story>`: `scoreboard.py:818-825`; one write site `:935-936`.
- Norm verdict line `norm <id> [<row>]: <verdict>`, owner's pass suffix, `-- worse` row lines: `render_compare` `scoreboard.py:855-873`; `--pass NORM WORD DATE`: `:1025`, stored in `passes` `:833-836`.
- `compare --findings` writes one finding per worsened row into `plans/piles/<pile>/findings/`, default pile `live-runs`: `scoreboard.py:878-918`, `:887`; undecided/unknown never a finding `:984-986`.
- K7: non-live run judges no norm: `_judge_one` `scoreboard.py:603-604`.
- release lines: `no previous release -- ratchet not judged` `scoreboard_bar.py:301-302`; `warning -- no live factory scoreboard` `:303-304`; red unratcheted -> warning `:325-333`; exit codes 0/1/2 `:390-415`, `:441-445`; version matched by file-name spelling `<version>-factory` `:199`.
- `run_counters.py --task-root --json`: `run_counters.py:698-705`; `G1.unknown_check.share` `:376-377`; `U1.unclassified_resume_kinds` `:667`; rows file `G1u`/`U1`: `experiments/scoreboards/rows.json:21`, `:28`.
- Notebook heading `## Ход прогона`: `experiments/mybooks/factory-vs-free-agent/notebook.md:175`, `experiments/mybooks/thinking-roles/thinking-roles.md` (Grep hit).
- `experiments/scoreboards/` holds only `norms.json`, `rows.json` (Glob `**/*`).
- plugin version spelling `0.11.0`: `ai-packages/qa-factory/.claude-plugin/plugin.json:4`.
- Last check number 46 at `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:1108`, `## Closing out a run` at `:1110`; no check mentions friction or scoreboard (Grep `friction|scoreboard` -i: 0 lines; control `quarantine|scoreboard` -i: 1 line).

## 2. `ai-packages/qa-factory/design/architecture.md` (English, no Cyrillic)

### 2a. AR-12 `Detector:` line
**Target**: `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\architecture.md`. **Anchor**: REPLACE the whole line `:130` that begins
`- Detector: \`test_friction.py\` tests only the meter; ...` and ends `...Finding: none filed yet (census t-1160 q2-b-gap).`
**Exact text**:

```
- Detector: `test_friction.py` tests only the meter; `retro_numbers.journal_counts(...)["gate_block_classes"]` counts the exit-gate refusals of a run by class (`gate_block_class`, the first finding) and the retro says so when one class reaches `friction.same_class_gate_blocks` of `references/stage-joints.json` (`test_retro_numbers.py` R1-R6); `scripts/run_counters.py` (`counters(task_root)`, writes nothing, the driver does not call it; covered by `test_retro_numbers.py`) counts one run's time rows, returns per check, questions, briefs and the friction share of role turns (R1r), each `measured`, `unknown` or `n/a`, never 0 for an unknown; the forge's run scoreboard (`dev:experiments/measurers/scoreboard.py`, rows `dev:experiments/scoreboards/rows.json`, tighten-only norms `dev:experiments/scoreboards/norms.json`) turns them into one file per live run and judges the norms, and weekly calibration check 47 (`dev:PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`) reads every live run's file, `norms --check --against`, and the owner of every red norm. Still not gated: FR-55's before/after check of a change; assembling a run's scoreboard (a morning step, discipline; check 47 is its leak detector); `norms --check` runs on no CI job or hook; the free-agent bar file has no writer, so the norms judged against a bar read `unknown`; the scoreboard rows T9/T10 read `unknown` (run_counters does not read `friction.call_spans`). Finding: none filed for the remaining gaps (census t-1160 q2-b-gap).
```

### 2b. AR-18 `Carriers:` line
**Anchor**: REPLACE line `:198` `- Carriers: axis 17; \`detector_verdict.parse\`, \`refusal_text\`, \`render\`; producers ...`.
**Exact text**:

```
- Carriers: axis 17; `detector_verdict.parse` (with its `labels` key, `(check, id)` per finding parallel to `findings`), `refusal_text`, `render`; the `Record` fields `check` (`<producer stem>:<family>`) and `tag`, read only through `check_id` and set through `with_check`; the machine line `checks: [...]` (`CHECKS_LINE_PREFIX`), written last by `story_step._gate_refusal` and taken out by its one reader `DriverDispatch.take_checks_line` in `Driver.finish` before the refusal text is built; producers `s5_precheck.py`, `planning_contract.py`, `critic_rollcall.py`, `check_coverage.py`, `check_witness.py`, `grounding_table.py`, `exit_gate.py`.
```

**Index**: `tools/architecture_index.py` renders the title only (`TITLE_RE = r"^\*\*AR-\d+ — (.*?)\*\*"`, `tools/architecture_index.py:37`; `docs/ARCHITECTURE_INDEX.md` holds one title line per AR). Neither title changes, so the generated index does not change; `architecture_index.py --check` (pre-commit, CI `forge-check.yml:79`) stays green. Not run (estimate from the regex).

**Facts checked**
- Old AR-12 Detector text incl. "the weekly calibration has no friction check": `architecture.md:130`; AR-18 Carriers `:198`.
- `run_counters.counters` writes nothing, rows and states: `run_counters.py:1-16`, `:570-643`; keep row `test_retro_numbers.py` covers it: spec N4 row :448 and N4 report witness (`docs/tasks/specs/reports/20261113-p1v-n4-report.md:58-60`).
- T9/T10 unknown: `run_counters.py:634-638`; `friction.call_spans` exists `friction.py:373`.
- `Record` fields `check`, `tag`: `detector_verdict.py:95-114`; `check_id` `:117-128` (error direction toward `unknown`/`unlabelled` `:120-121`); `with_check` `:131-139`; `parse` `labels` `:259-273`, `:322-341`; `CHECKS_LINE_PREFIX` `:80-83`.
- Writer `story_step._gate_refusal` prints the line last: `story_step.py:2008`, `:2062-2064`.
- Reader `DriverDispatch.take_checks_line` called from `DriverDispatch.finish` on exit 3 only: `driver_dispatch.py:222` (class), `:789` (`finish`), `:856-875`, `:894-916`; `Driver` mixes `DriverDispatch` in: `story_run.py:94`. Only these three sites use `CHECKS_LINE_PREFIX` outside tests (Grep: `detector_verdict.py:83`, `driver_dispatch.py:904,908`, `story_step.py:2064`; plus `tests/test_then_remainder.py:856`).
- No CI/hook runs anything under `experiments/`: `.github/workflows` Grep `scoreboard|test_measurers|experiments` -i: 0 (control `pytest` -i: 9 hits, e.g. `forge-check.yml:96`); `.githooks` Grep `pytest|scoreboard` -i: 0 (control `python` -i: 13 hits).

## 3. `docs/SIBLING_MAP.md`

### 3a. Axis 6 — new table row
**Anchor**: after the row that begins `| The hop measurer (forge/5 F5-2 M3, t-811/t-813, 15.10) |` (`SIBLING_MAP.md:171`), before the blank line and `A package change that renames an artifact...`.

```
| The run scoreboard (P1-v N4/N6/N7, spec `docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md`) | forge: `experiments/measurers/scoreboard.py` (`assemble` / `compare` / `norms` / `release-check`) and `scoreboard_bar.py` (`price`, `release_lines` = `compare --release`, `release-check`) <-> package: `scripts/run_counters.py` (`counters(task_root)`) and `scripts/task_price.py` (`task_price`, row X1), both imported through `paths.SCRIPTS` (precedent `code_friction.py`); `scoreboard_bar` also imports `cost_capture` (`value_usage`, `load_catalogue`) and the forge `compare.is_empty_marker`. What changes together: a `run_counters` key that `experiments/scoreboards/rows.json` names by `path`/`sum_of`/`max_of`/`count_of`/`ratio`/`diff` (`T1.wall_s`, `G1.by_check`, `G1.unknown_check.returns`, `B1.over`, `R1r.total.turn_share`, `U1.lines`, ...) — a renamed or dropped key reads `unknown` in the scoreboard, never a red; the carriers `run_counters` reads under `<task_root>/state/` (`driver-runs.jsonl`, `driver-questions.jsonl`, `driver-answers.jsonl`, `passed-by-person.jsonl`, `brief-sizes.jsonl`, `driver-timings.jsonl`), their field names and the `config.json` two levels up (friction's `cost`); the four `task_price` statuses mapped by `scoreboard.price_row` (`agrees`/`differs`/`incomplete`/`not_cross_checked` -> `measured`/`range`/`at_least`/`one_source`); `cost_capture.value_usage`'s signature. Detectors: `experiments/measurers/test_measurers.py` (self-running; the scoreboard tables also under pytest) — on no CI job yet; `scripts/tests/test_retro_numbers.py` for `run_counters`. Known break: the `brief-sizes.jsonl` keys (axis 29) |
```

### 3b. Axis 17 — new table row
**Anchor**: after the row `| The one reader | \`scripts/detector_verdict.py\` — \`parse\`, \`Record\`, ...` (`SIBLING_MAP.md:379`), before `| Consumers | ...`.

```
| The check id (P1-v W0, spec `docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md` §2 W0) | the `Record` fields `check` (`<producer stem>:<family>`) and `tag` (`detector_verdict.py` `Record`), read only through `detector_verdict.check_id` (error direction toward `unknown` / `<stem>:unlabelled`, never a check that did not refuse) and set only through `with_check`; `parse` returns `labels` parallel to `findings`; the machine line `checks: [...]` (`detector_verdict.CHECKS_LINE_PREFIX`) has ONE writer, `story_step._gate_refusal` (printed LAST, exit 3 only), and ONE reader, `DriverDispatch.take_checks_line`, called from `DriverDispatch.finish` (`scripts/driver_dispatch.py`, a mixin of `story_run.Driver`), which takes it out before the refusal text is built (the text, `finding_key` and the resume prompt stay byte-identical); downstream the ids travel as `Refusal.checks` / `checks_n` into the `checks` / `checks_n` keys of resumed `driver-runs.jsonl` rows, read by `run_counters` (row G1). A second reader of the line, or a line appended after it, breaks the byte identity; detectors `test_driver_stop_record.py` (`take_checks_line_cases`), `test_then_remainder.py` (the line is last), `test_detector_verdict.py` |
```

### 3c. Axis 18 — member sentence inside the `The members` cell
**Anchor**: inside row `| The members | ...` (`SIBLING_MAP.md:390`), after its last words `...a raise is \`--update\` with an \`added:\` reason in the commit)` and before the closing ` |`. Insert:

```
; since P1-v N6 (spec `docs/tasks/specs/20261113-p1v-run-scoreboard-spec.md` §8.1 item 3; AR-20) the forge's `experiments/scoreboards/norms.json` (schema `norms/2`), TIGHTEN-only: a row's `norm` is never looser than its `initial` or the `to` of its last `raises` element (each raise carries `from`, `to`, `raised_by`, `reason` and the owner's `word`); against the file as it was, a set `initial` never changes, raises are only appended, a dropped or unset norm is a loosening, a `ratchets` element is never removed and its `value` never worsens without a new `{ratchet: "<pair>@<factory model>", raised_by, reason, word}` raise, and a new `worsened_passes` entry names its `factory_model`; checker `python -B experiments/measurers/scoreboard.py norms --check --against <old norms.json>` (`check_norms`; exit 1 with `RED:` lines) — run by NO CI job or hook today, so the in-tree half of this axis holds only when the command is run (calibration check 47 (b) runs it per window); a tightened `norm` and a new `ratchets` element are Lead commits, a `worsened_passes` or `bar_changes` entry carries the owner's word
```

### 3d. Axis 29 — sentence in the paragraph (the axis has no table)
**Anchor**: inside the paragraph at `SIBLING_MAP.md:458`, after `...pinned by \`test_driver_stop_record.py\`; its analog \`story_run._read_jsonl\` still splits with \`splitlines()\`, queued).` and before ` Siblings NOT yet adopted`. Insert:

```
 Adopted by P1-v N3 (reshaped by FV1-4): `scripts/brief_pack.py` `_record_brief_size`, called from `build` once per written brief, appends one line to `state/brief-sizes.jsonl` through `hooklib.append_jsonl_line`; a write failure is one stderr note and never changes or fails the brief; its one reader is `run_counters._briefs` (scoreboard row B1). The writer's keys `{ts, stage, role, dispatch, bytes}` and the reader's `budget_bytes` / `ceiling` disagree since FV1-4, so B1 reads a measured 0 over rows it could not read — a finding (P1-v N8 draft, F-1), not a member that is in order.
```

**Facts checked (3a-3d)**
- Axis 6 table and rows: `SIBLING_MAP.md:159-180`; friction paragraph `:178-180`. Imports through `paths.SCRIPTS`: `scoreboard.py:33-44`; `scoreboard_bar.py:33-45` (`compare`, `paths`, `scoreboard`, deferred `cost_capture`), `value_usage` call `:141`, `is_empty_marker` `:69`.
- rows.json value forms and paths: `experiments/scoreboards/rows.json:3`, `:8-35`; a missing counter -> `unknown`: `_counter_row` via `assemble` `scoreboard.py:814-817` and module docstring `:18-21`.
- Carriers read: `run_counters._carrier` `run_counters.py:92-96`, names `:36-38`, questions/answers `:512-514`, timings through `driver_timing.report` `:623`, friction `config.json` at `task_root.parent.parent` `:491-493`, task_price at `task_root.parent.parent` `scoreboard.py:323`.
- `price_row` status mapping: `scoreboard.py:317-343`.
- Axis 17 table: `SIBLING_MAP.md:373-384`; code facts as in 2b.
- Axis 18 table: `SIBLING_MAP.md:386-396`; `check_norms` facts as in 1; norms.json shape `experiments/scoreboards/norms.json:1-34`.
- Axis 29 paragraph: `SIBLING_MAP.md:456-458`. Writer: `brief_pack.py:4289-4302` (append through `hooklib.append_jsonl_line` `:4300`), call site `:4652`. Reader: `run_counters.py:547-565` (reads `budget_bytes`, `ceiling` `:553`; returns `measured` `:564`). Grep `bytes|budget_bytes` in run_counters: only `:553`, `:562` — no reader of `bytes`.
- Absence of any scoreboard/norms/run_counters mention in SIBLING_MAP: Grep `scoreboard|norms\.json|run_counters` -i: 0 (control `hop_metrics|scoreboard|norms\.json` -i: 5).

## 4. `docs/tasks/critic-diff-brief.md` question 9

**Target**: `C:\QAFactory\forge-repo\docs\tasks\critic-diff-brief.md`. **Anchor**: line `:59`, inside the parenthesis
`(SIBLING_MAP axis 18, 16.10; since D-0060 the members include \`scripts/tests/fixtures/judgment-census.json\` \`ratchet\` and \`role-load.json\` \`process_ratchet_tokens\`)`.
Replace the closing `)` of that parenthesis by:

```
; since P1-v N6, `experiments/scoreboards/norms.json` (tighten-only: a looser `norm`, a removed or worsened `ratchets` element, a new `raises`, `worsened_passes` or `bar_changes` entry is named with its owner's `word`))
```

(The brief said question 9 is at :79; :79 is question 11's sentence about the census. Question 9 is at :59-68.)

**Facts checked**: question 9 text `critic-diff-brief.md:59-68`; question 11's census sentence `:78-79`; norms.json not named in the brief (Grep `scoreboard|norms\.json|judgment-census` -i: only :59, :78 — the census hits are the positive control).

## 5. `docs/RUNBOOK.md` §9.5 «Утром»

**Target**: `C:\QAFactory\forge-repo\docs\RUNBOOK.md`. **Where and why**: a NEW step 5 between step 4 (`4. Потом смотреть результат: ...`, ends `...на живом прогоне**).` at `:327`) and the current step 5 (`5. Утренний разбор записать в тетрадь эксперимента: ...` `:328`), which becomes 6. Reason: assembling needs the run to have ended (step 3 may restart it) and the result read (step 4); the write-up (new 6) then cites the `compare` lines and the finding drafts.

**Exact text** (insert as step 5; then renumber the old `5.` to `6.`):

```
5. **Собрать табло прогона**, когда стори закрыта (выход 0) или прогон брошен; прогон, который ещё стоит на вопросе, собирается
   после закрытия (повторная сборка того же прогона переписывает тот же файл):
   `python -B experiments/measurers/scoreboard.py assemble --task-root <корень проекта в копии>\qa-factory\artifacts\<ТИКЕТ> --stand <стенд> --story <стори> --arm factory --version <X.Y.Z> --model <id модели ролей>`,
   плюс `--truth experiments/<стенд>/truth/<стори>.yaml --judgment experiments/<эксп>/judgment.yaml`, когда есть слепая оценка, и
   `--bar <файл планки>`, когда планка есть. `--task-root` — папка стори в копии проекта, вне репозитория; `--version` — `version`
   из `.claude-plugin/plugin.json` пакета прогона, без `v` (то же написание ждёт `release-check --release`, иначе выпуск табло не
   найдёт). Файл ложится в `experiments/scoreboards/<стенд>/<стори>/<ГГГГММДД-ЧЧММ>-<версия>-factory.yaml` (старт по UTC) того
   дерева, откуда запущен скрипт; при отказе (пустая папка, битый файл суждений, нет времени старта — тогда `--started <ISO>`)
   не пишется ничего, причину называет строка `RED:`. Затем
   `python -B experiments/measurers/scoreboard.py compare <файл> --findings`: строка `-- worse` — черновик находки в
   `plans/piles/<кучка>/findings/` (кучка из `rows.json`, по умолчанию `live-runs`) и строка карточки, которую кладёт Lead
   (PROJECT.md «Командная работа» п. 2); строка `norm <id> [...]: red` — находка или слово владельца, записанное пересборкой с
   `--pass <норма> "<слово>" <дата>`; `unknown` и `undecided` — не зелёное и не красное, причина в той же строке. Прогон, чей
   `run_class` не `live` (сухой, дымовой, без строк процесса), норм не судит. Строка цены X1 в файле табло — по слову владельца
   13.11.2026 (`docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md:476`), исключение из «Деньги в файлы репозитория не
   пишутся» (9.6).
```

**Same-carrier edit owed by this step** (the step creates a contradiction with §9.6 `:339-340`): append to the 9.6 bullet `**Цена**: ... Деньги в файлы репозитория (отчёт, тетрадь) не пишутся.` the words ` Исключение — строка X1 табло (9.5 п. 5), по слову владельца 13.11.2026.`

**Facts checked**
- §9.5 has 5 steps, no assemble: `RUNBOOK.md:310-329`; story folder `qa-factory/artifacts/<ТИКЕТ>`: `:312`; §9.6 money line `:339-340`; no `scoreboard` in RUNBOOK (Grep `scoreboard|norms\.json|stage_compare` -i: only `:356`, the stage_compare control).
- Required `assemble` args `--task-root --stand --story --arm --version`; optional `--truth --judgment --truth-version --bar --model (repeatable) --pass NORM WORD DATE --started --rows --norms --out-root`: `scoreboard.py:1014-1029`.
- `--truth` and `--judgment` go together: `:802-804`; empty/absent folder refusal: `:795-798`; start unknown -> `--started`: `:818-820`; out path default `paths.REPO/experiments/scoreboards`: `:47`, `:824`; nothing written on a refusal: `:928-936`.
- File name from the run's first time, so a re-assembly of the same run hits the same name: `:818-825` (`T1.first`).
- `compare <file> --findings` and the pile default: `:1031-1041`, `:878-918`; card lines printed for the Lead: `:916-917`, `:982-983`.
- Owner's word on money in the forge file: amendment `:476-478`.

## 6. `PROJECT.md` «Релиз» — the one line of §8.1 item 4

**Target**: `C:\QAFactory\forge-repo\PROJECT.md`. **Anchor**: after the paragraph line that begins `Проверенная версия уходит в \`Xartaxana/QAFactory\`: ...` and ends `...Публикация — только по слову владельца.` (`PROJECT.md:368`), as a new line before `Запись CHANGELOG собирается из фрагментов: ...` (`:369`).

**Recommended text** (follows the merged code and the amendment's re-wording at :494, not the spec's original):

```
Перед PR: `scoreboard.py release-check --release X.Y.Z` даёт 0 (закреплённое хуже — словом владельца); сухая стори зелёная.
```

Size: 182 bytes UTF-8 + 1 newline = 183 bytes (hand count: Cyrillic letters 2 bytes, `—` 3 bytes; estimate, not measured — the Lead measures with a byte count before placing). The boot budget figures (121405 / 120000) are from the brief, not verified here.

Longer variant, if the Lead wants the red-norm rule visible (≈ 245 bytes, estimate): `Перед PR: \`scoreboard.py release-check --release X.Y.Z\` даёт 0: красная норма — предупреждение, закреплённая строка хуже или неизвестна — только словом владельца; сухая стори зелёная.`

**Facts checked**: «Релиз» `PROJECT.md:364-371`, no `сухая|табло|release-check` there (Grep: only the heading `:364`, the control). `release-check` exit semantics: `scoreboard_bar.py:375-415`. The dry-story half has no merged release command: `.github/workflows/canon.yml:35-37`, `:64-80` carry only a `dry-story-spike` job (P1-b N0) — see fork 7(f).

## 7. Forks (decisions owed; recommendation and error direction each)

**7(a) The bar-file writer.** Options: (1) a NEW node N9 under a new task id; (2) extend N7 (accepted and merged; reopening a closed task is forbidden, CLAUDE.md rule 4), (3) re-scope N7 in writing and keep the bar norms `unknown`. **Recommendation: (1).** Error direction the writer must keep: toward `unknown` / `n/a` — a missing transcript, an unreadable result file, a row the free arm has no part for is never 0 and never the host's figure; a bar file that is absent stays "no bar file" (`scoreboard.py:612-613`, `:630-631`), the safe side.
Card for a weaker builder (if (1)):
- owns: `C:\QAFactory\forge-repo\experiments\measurers\scoreboard_bar.py` (new function `bar_doc`, new subcommand `bar` in `main`), `C:\QAFactory\forge-repo\experiments\measurers\test_measurers.py` (a new table `SB_BAR_FILE_CASES` + its `_parametrize` test + an entry in `SB_GROUPS`; no new test file).
- what: `python -B experiments/measurers/scoreboard_bar.py bar --stand S --story T --model <model id> --transcript <abs> [--transcript ...] --result <free-N.log> [--result ...] [--truth F --judgment F] [--cfg cost.json] [--out-root DIR]` writes `<out-root>/<stand>/<story>/bar-<model id>.yaml` (default `experiments/scoreboards`), schema `scoreboard/1` with `run.arm: free`, `run.run_class: live`, `run.truth_version` from the judgment, `run.models: [<model id>]`. Rows: `X1` = `bar_price(...)` (state `measured`/`unknown`, the host figure NOT in the value); `T1` = first -> last transcript event (seconds; `unknown` when no readable timestamp); turns = `num_turns` of the result JSON (shape read as `host_total` does, `scoreboard_bar.py:74-95`); tool calls by name and refused calls through the package's `friction.call_spans` (`friction.py:373`, the T10 rule, one road for both arms) — never a private transcript loop; QA rows through `scoreboard.read_judgment(..., arm="free", ...)` and `quality_rows` (one road with the factory arm); every other row of `rows.json` = `{state: "n/a", why: "no such part in a free agent"}`. One write site; nothing written on a refusal; bad `--model`/`--stand`/`--story` -> `SB._safe` refusal; the model id must equal a `message.model` of the transcript (else refusal naming both).
- tests (variant rows): transcript absent / empty / unreadable -> `X1 unknown`, file still written with the reason; result with no `total_cost_usd`; two transcripts summed; model mismatch refused; `n/a` rows never 0; `--model` with `/` or `..` refused; the written file read back by `assemble --bar` and `compare --release` (`_bars`) without refusal.
- DoD: `python -B experiments/measurers/test_measurers.py` prints `=== test_measurers: N/N ok ===`.
- who runs it: the Lead once per (stand, story, model id) after a free-arm run (spec §3 item 1); money: the bar run itself (owner question F10, spec §3).

**7(b) CI for `experiments/measurers/test_measurers.py` and `norms --check`.** Options: (1) two steps in `.github/workflows/forge-check.yml` job `forge-check` after `python -m pytest tools/ -q` (`:96`): `python -B experiments/measurers/test_measurers.py` and `git show "$BASE":experiments/scoreboards/norms.json > "$RUNNER_TEMP/norms-base.json" 2>/dev/null && python -B experiments/measurers/scoreboard.py norms --check --against "$RUNNER_TEMP/norms-base.json" || python -B experiments/measurers/scoreboard.py norms --check` (with an explicit echo when the base has no file); (2) a separate job gated by a `changes`-style path filter on `experiments/`; (3) stay local (discipline, check 47 (b) as detector). **Recommendation: (1)** — it puts K5 on the execution path where the spec said it would be (critic answer 8(e), `reviews/...tail-topic-critic.md:72`) and the deps are already installed (`pyyaml`, `forge-check.yml:52`). Cost: estimate, not measured — the scoreboard tables took 7.34 s under pytest (critic trail `:92`); the whole self-running file is unmeasured (one measurement on CI's first run, hygiene 6(b)). Risk to verify on that first run: the measurers' `paths.py` reads `tools/dev.config.yaml`, absent on CI (`tools/test_dev_config.py:543` says the import works with no table — not verified for the full file). Error direction: a CI red that is a test-environment defect blocks merges (false block, safe side); with (3) a loosened norm reaches main until the weekly check (unsafe side). The workflow file is a mechanism path: the Lead places it.

**7(c) The first scoreboard of LR2-1.** The in-repo folder `experiments/mybooks/factory-vs-free-agent/runs/factory-out/state/` holds ONLY `driver-runs.jsonl` (Glob); questions, answers, passed-by-person and timings are absent, and `config.json` at `task_root.parent.parent` (friction) is absent, so Q1-Q3, T4/T5 and R1r would read `unknown`. The arm state outside the repo, `C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1\state`, holds `driver-runs.jsonl`, `driver-questions.jsonl`, `driver-answers.jsonl`, `passed-by-person.jsonl`, `driver-timings.jsonl` (Glob `*.jsonl`); N4 already measured it (`reports/20261113-p1v-n4-report.md:36-54`). Both journals have 81 `role` rows and 0 `process` rows (Grep, same shape), so `run_class` = `unknown` (`run_counters.py:140-141`): the scoreboard judges NO norm (K7), is never picked as a "previous" live file, and `release-check` will not count it as live. **Recommendation**: assemble it on the arm state as a historical record (not a baseline; the norms' `initial` values already carry LR2-1 through t-357), and do not add a run-class override (code would then assert a fact no carrier holds). Command (writes one file; not run):
`python -B experiments/measurers/scoreboard.py assemble --task-root C:\QAFactory\mybooks-stand\arm-factory\test-automation-framework\qa-factory\artifacts\LOCAL-1 --stand mybooks --story add-to-cart --arm factory --version 0.11.0 --model sonnet --truth experiments/mybooks/truth/add-to-cart.yaml --judgment experiments/mybooks/factory-vs-free-agent/judgment.yaml`
then `python -B experiments/measurers/scoreboard.py compare experiments/scoreboards/mybooks/add-to-cart/<printed name>`.
Unknowns: (i) K1 may refuse the judgment: `evaluated_against_version: v2026-11-05-lead` (`judgment.yaml:13`) while the file's comment says every card of the OWNER version has a row (`:6`); `read_judgment` needs exactly one row per card of the named version (`scoreboard.py:367-413`) — a refusal writes nothing and names the row; fallback: drop `--truth/--judgment` (QA rows `unknown`). (ii) `rows.json` `verdicts` is empty (`rows.json:5-6`), so QA1-QA6 read `unknown` either way. (iii) `--model sonnet` is the driver's model word (`driver-runs.jsonl` row `"model": "sonnet"`), not a full model id; the Lead may give the id from a transcript instead. Version 0.11.0: `notebook.md:147-151`. Error direction: the record is all-`unknown` where data is missing, never a green.

**7(d) Check 47 (e) reads two numbers the scoreboard file does not keep.** Options: (1) two data rows in `experiments/scoreboards/rows.json`: `"G1us": {"name": "Share of returns naming the unknown check", "unit": "%", "path": "G1.unknown_check.share", "better": "lower"}` and `"U1u": {"name": "Resumed calls of the unclassified resume kind", "unit": "calls", "path": "U1.unclassified_resume_kinds", "better": "lower"}` (data only, no code, AR-1; a Lead edit or a one-line builder node with a `test_measurers.py` assemble row); (2) keep reading `run_counters --json` while the root exists (loses the number once the copy is removed). **Recommendation: (1).** Error direction: a missing key reads `unknown`, never 0 (`scoreboard.py:18-21`).

**7(e) The carrier of the release-check line (check 47 (d)).** Options: (1) the witness of the release's `accepted` journal event; (2) the release commit message in this repo; (3) a file under `experiments/scoreboards/`. **Recommendation: (1)** — the witness field already carries verbatim runs (CLAUDE.md rule 2) and is append-only. Error direction: a release with no line is a finding, never "probably ran".

**7(f) The shared PROJECT.md line — the dry-story half.** P1-b's "сухая стори зелёная" has no merged release command (only the `dry-story-spike` input of `canon.yml`). Options: (1) write the shared line now with both halves (the dry half is a statement with no command until P1-b lands its gate); (2) write only the scoreboard half now and let P1-b extend the same line; (3) hold the whole line for the owner (boot budget breached). **Recommendation: (3)** with the 183-byte text of §6 ready, because §8.1 item 4 says "one line for both, written once" and the budget blocks any addition; if the owner frees bytes, (1).

**Finding F-1 (not a fork; the Lead files it): B1 reads a measured 0 over rows it cannot read.** Writer `brief_pack._record_brief_size` writes `{ts, stage, role, dispatch, bytes}` since FV1-4 (`brief_pack.py:4289-4300`); reader `run_counters._briefs` needs `budget_bytes` and `ceiling` (`run_counters.py:553`) and returns `state: measured, over: 0, unreadable_rows: N` (`:564-565`); scoreboard row B1 = `B1.over` (`rows.json:26`). Invariant to protect: a brief-size row the reader cannot judge is never counted as "not over" — B1 is `unknown` when no row carries a ceiling (FR-41, AR-22, AR-28). Proposed node (owns `scripts/run_counters.py` `_briefs`, `scripts/tests/test_retro_numbers.py`): B1 `unknown` when every row lacks a ceiling, `measured` only over rows that carry one, `unreadable_rows` kept; where the ceiling now lives after FV1-4 ("длину держит фордж") is a question to the Lead. Also stale: `brief_pack.py:4292-4293` docstring ("no reader in the package reads"), `changelog.d/p1v-n3-brief-sizes.md:2` (critic `20261113-fv14-topic-code-critic.md:46`).

## 8. Four questions for the commit (CLAUDE.md rule 10)

Mechanisms: M1 = calibration check 47; M2 = `experiments/scoreboards/norms.json` as an axis-18 ratchet member (with the critic question 9 line).

(a) Cost and who pays. M1: the Lead (calibration run) — per window one `norms --check --against` and one `compare` per scoreboard (seconds, no model), one `release-check` per release, reading notebooks and `git log -p` of one file (minutes); per live run the morning `assemble` + `compare --findings` (seconds) paid by the run's operator. M2: every critic on a diff touching `norms.json` names each change row by row (minutes, inside the existing one-pass critic); the owner gives a word per raise or pass.

(b) Axes (every heading of the current `docs/SIBLING_MAP.md`, 37 axes):
- axis 1: n/a — no policy/role-file/journal change (critic brief q9 gains a member, its rule text unchanged).
- axis 2: n/a — no exam instrument.
- axis 3: n/a — nothing under the package changes except `design/architecture.md` text, which reaches the release copy by the normal copy.
- axis 4: n/a — no factory rule or debt changes; AR-12/AR-18 text only.
- axis 5: n/a — no stage twin touched.
- axis 6: covered — row 3a (scoreboard.py, scoreboard_bar.py <-> run_counters.py, task_price.py, cost_capture).
- axis 7: n/a — no per-test identity.
- axis 8: covered — `--task-root` is given by the operator, the tools resolve no story themselves (`scoreboard.py:1015`, `run_counters.py:703`).
- axis 9: n/a.
- axis 10: n/a.
- axis 11: n/a.
- axis 12: covered — red/worse rows become finding drafts in `plans/piles/*/findings/` by the pile protocol (`compare --findings`, the Lead places the card row).
- axis 13: n/a — no dispatch text changes.
- axis 14: queued — the bar writer (fork 7(a)) must read transcripts through `friction.call_spans`, not a private loop; `scoreboard_bar._requests` duplicates `compare.scan` (critic P2).
- axis 15: n/a.
- axis 16: n/a — forge tools; `run_counters` reads JSON through `hooklib.read_json` / `driver_journal` (`run_counters.py:492`).
- axis 17: covered — row 3b (Record.check/tag, parse labels, the `checks:` line and its one reader).
- axis 18: covered — member sentence 3c and critic q9 line 4; the gap (no CI runs `norms --check`) is named and queued as fork 7(b).
- axis 19: n/a.
- axis 20: n/a.
- axis 21: n/a.
- axis 22: n/a.
- axis 23: n/a.
- axis 24: n/a.
- axis 25: n/a.
- axis 26: n/a.
- axis 27: n/a.
- axis 28: n/a.
- axis 29: covered — sentence 3d; the producer/reader break is finding F-1, queued as a node.
- axis 30: n/a.
- axis 31: n/a — no role carrier.
- axis 32: covered — no judgment moves to code: `norms --check` judges data (shape, numbers, presence of a word); whether a red is acceptable stays with the Lead and the owner (check 47 (c)). Census class: forge tool outside the package census — n/a.
- axis 33: n/a.
- axis 34: covered — one road for both arms (`read_judgment(arm=...)`, the bar card's `friction.call_spans`) and for dry/live (`run_class`, K7); noticed, not widened: on the skill (interactive) road no reader takes the `checks:` line out of `story_step finish` output (only `Driver.finish` does) — reported below for the Lead.
- axis 35: n/a.
- axis 36: n/a.
- axis 37: n/a.

(c) Detector registered: M1 is itself registered as check 47 of `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, its own leak named in its last sentence (a notebook run with no file and no line (a); `norms.json` commits with no line (b)). M2: check 47 (b) plus check 35 (b)'s standing sentence "the same reading applies to every member of SIBLING_MAP axis 18" (`WEEKLY_CALIBRATION_PROTOCOL.md:1077-1078`).

(d) What stops a skip: M1 — the weekly calibration (`calibrated` event; the Boot Report's Last Calibration line is the outside detector of a missed calibration). Assembling per run is on discipline (RUNBOOK §9.5 step 5), with check 47 (a) as the named leak detector. M2 — on discipline today (no CI or hook runs `norms --check`); promotion to a code gate is fork 7(b), recommended now because the spec promised K5 on forge-check (critic answer 8(e)) — the Lead decides whether the promise counts as the evidence rule 10(d) asks for.

Commit lines owed: `architecture: AR-12 -- detector line names run_counters, the scoreboard and check 47, gaps kept; AR-18 -- carriers name Record.check/tag, parse labels and the checks: line`; `judgment: none` (text only); `tier: <Lead model>`.

## Small choices closed by the designer

- Check number 47 (last is 46, `:1108`); placed before `## Closing out a run`; English like 43-46.
- Axis 29 has no table: the addition is a sentence in its paragraph, in the "Adopted since" place.
- Axis 17 gets a new row (not edits of existing cells), axis 18 a sentence at the end of the members cell, as earlier members were added.
- RUNBOOK step number 5 (old 5 -> 6); the 9.6 exception sentence added because the new step would otherwise contradict it.
- PROJECT.md line follows the amendment's re-wording (:494), not the spec's original (:468).

## Noticed, not widened (for the Lead)

- F-2: `run_counters` T9/T10 always `unknown` although `friction.call_spans` exists (D5).
- F-3: `experiments/measurers/README.md:55` stale ("pytest collects no tests"; D6).
- Brief inaccuracy: "critic-diff-brief question 9 at :79" — q9 is at :59; :79 is q11.
- Axis 34 analog: the `checks:` machine line reaches the orchestrator as text on the skill road (no reader strips it there); `story_step._gate_refusal` prints it for every caller (`story_step.py:2064`).
- The spec's axis count (36) is stale; the map has 37.
- Money in `runs/factory-out/state/driver-runs.jsonl` (`total_cost_usd`) is NOT a defect by the owner's word 13.11 (amendment :478) — checked, no finding.

## Trail (read and searched; every "absent" with its positive control)

Read: spec `:430-539`; amendment `:472-481` + Grep `предупрежд|warning` (:33, :482, :494, :567, :592, :597, :605); critic review whole; `scoreboard.py` `:1-70`, `:317-343`, `:366-395`, `:440-644`, `:770-1058`; `scoreboard_bar.py` whole; `run_counters.py` `:1-70`, `:92-96`, `:137-162`, `:355-379`, `:460-711`; `brief_pack.py:4285-4309`; `detector_verdict.py:76-139`; `story_step.py:2040-2066`; `driver_dispatch.py:835-924`; `friction.py:373-402`; `norms.json`, `rows.json` whole; `test_measurers.py` `:1-40`, `:1650-1664`, `:3195-3234`, `:3330-3364`; measurers README whole; `forge-check.yml` whole; `architecture.md:120-209`; `SIBLING_MAP.md` `:159-182`, `:329-346`, `:373-397`, `:456-459`; `critic-diff-brief.md:59-89`; `RUNBOOK.md:148-372`; `PROJECT.md:362-375`; calibration protocol `:1000-1122`; `judgment.yaml:1-22`; `notebook.md:160-219`; N4 report `:36-60`; LR2-1 `driver-runs.jsonl:1-3`.
Searches (Grep unless noted): calibration `friction|scoreboard` -i -> 0, control `quarantine|scoreboard` -i -> 1; SIBLING_MAP `scoreboard|norms\.json|run_counters` -i -> 0, control `hop_metrics|scoreboard|norms\.json` -i -> 5; architecture.md `scoreboard|run_counters|code_friction` -i -> code_friction only (control in the same call); RUNBOOK `scoreboard|norms\.json|stage_compare` -i -> :356 only (control); critic brief `scoreboard|norms\.json|judgment-census` -i -> :59, :78 (control); PROJECT.md `сухая|табло|^## Релиз|release-check` -> :364 only (control); `.github` `scoreboard|test_measurers|experiments` -i -> 0, control `pytest` -i -> 9; `.githooks` `pytest|scoreboard` -i -> 0, control `python` -i -> 13; `CHECKS_LINE_PREFIX` in scripts -> 5 sites; `take_checks_line` -> 3 files; `brief-sizes|BRIEF_SIZES|append_jsonl_line` in brief_pack -> :31, :57, :4290, :4300; `bytes|budget_bytes` in run_counters -> :553, :562; `budget_bytes` *.md -> 17 files (fv14 critic :46, fix report :6 — neither names run_counters); `"kind": "process"` in both LR2-1 journals -> 0, control `"kind": "role"` same files -> 81 each; `^## Ход прогона` in experiments -> 2 files; `dry.story|dry_story` -> canon.yml, dry_exits.py, run_counters.py, friction.py; `^def test_` test_measurers -> 18; `"version"` plugin.json -> :4. Glob: `experiments/scoreboards/**/*` -> norms.json, rows.json; `factory-out/state/*` -> driver-runs.jsonl only; arm `LOCAL-1/state/*.jsonl` -> 8 files (no brief-sizes.jsonl); `factory-vs-free-agent/**/*` listing. A first Glob with a `experiments/...`-prefixed pattern returned nothing — a miscall (the same files were then found with the folder as `path`), not an absence.
Needed beyond the manifest: the arm state folder outside the repo (read-only Glob/Grep), the N4 report, `friction.py`, `brief_pack.py`, `driver_dispatch.py`, `story_run.py:94`, `canon.yml`.
