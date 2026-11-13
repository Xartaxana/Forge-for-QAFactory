# CL4-1 — the CL3-9 queue: one classifier for (stalled, looped), the ignored lists travel, a durable `window_round` row priced as bookkeeping, the KB says "stalled or looped"

Draft by the designer, 13.11.2026, for the Lead's acceptance; **fix round applied the same day** after the critic-on-plan verdict
`docs/tasks/specs/reviews/20261113-cl4-1-plan-critic.md` (fit_with_fixes: B1, B2, A1-A11). What changed and where: the last section,
"Fix round". Node: `plans/piles/collect/batch-4-cl3-9-ochered.md` row CL4-1.
Its finding: `plans/piles/collect/findings/20261102-cl3-9-ochered-vlozhennost-slova-petel-bez-chitatelya-i-zhurnal-raundov.md`
(section "Что именно менять": the direction is chosen, and this draft does not reopen it). Where the finding's facts are out of date
against the code on `main`, §0 lists it and the nodes follow the code. The batch file asks for `docs/tasks/specs/t-nnn-cl4-n.md`; the
dispatch names this path, and the dispatch wins.

Every node below is written for a weaker model: file, function and field are named, and so are the expected behaviour, the test row
and the decided edges. The technical forks are decided (§5, by the critic's fork table); the only open item is the owner's question
Q-1, which blocks nothing.

---

## §0 Facts (re-taken on `.claude/worktrees/read-main` = origin/main **e4ba384**, 13.11.2026)

The first draft read the root checkout (f52faed, 95 commits behind). Every file:line below is on read-main. Files that did not change
between the two (the critic's diff, verdict §1): `collect_stall.py`, `collect_pack.py`, `driver_gates.py`, `collect-loops.json`,
`test_probe_gap_door.py`, `test_probe_not_proved.py`, `SKILL.md`, `tools/collect_intake.py`, `tools/test_collect_intake.py`,
`kb/04-onboarding-doctor.xhtml`, `docs/TESTING.md`, `plans/builder-rules.md`. The lines that moved are corrected in place.

### §0.1 The code

| # | Fact | Carrier (read-main) |
|---|---|---|
| C1 | `_l_records` sits at **373-417**: a loop over the table rows, then a `rows` branch, then for the state shapes a loop over the records with three shape branches. In the `nested_records` branch two more levels sit inside (a loop over `inner`, then a condition). It defines two closures: `take(row, name, raw_time, value)` appends a signal through `_after`, and `hit(row, record)` is a string value in `row["values"]`. | `ai-packages/qa-factory/scripts/collect_stall.py:373-417` |
| C2 | The `where` of a loop signal is `f"{row['carrier']} {row.get('key') or row.get('kind') or row['field']} {name} {value}"`. A `rows` row passes `name="row"`. | `collect_stall.py:380`, `:393` |
| C3 | A record with no usable time goes to `ignored` as `{"where": <where>, "why": "no usable time, so never a signal"}`. A time that is present but cannot be read is a reason instead. | `collect_stall.py:156-168` |
| C4 | Verdict shape: `{stalled (bool), current, running_now, waiting_for_person, record, signals, unreadable_reasons, ignored, looped (True/False/None), loop_signals, loop_unreadable_reasons, loop_ignored}`. `stalled` is always `bool(...)`. | `collect_stall.py:337-340` |
| C5 | The H gate is `wants_transcripts`: `bool(verdict.get("stalled")) or verdict.get("looped", False) is not False`. A non-dict counts as `{}`. | `collect_stall.py:495-499` |
| C6 | Pair → words, site 1: `select_transcripts` `why` ("the story is stalled and looped" / "the story looped" / "the story is stalled" / "whether the story looped is not known"); its early return gives `verdict.get("record") or "the story neither stalled nor looped"`. The `why` is reached only when the story has at least one readable session (`:521-524` return first). | `collect_stall.py:515-516`, `:521-524`, `:530-532` |
| C7 | Pair → words, site 2: `Packer._pack_transcripts` gap text `{(True, True): "stalled and looping", (True, False): "stalled", (False, True): "looping"}.get((bool(stalled), looped is True), "possibly looping")`, used in `"no transcripts for the {state} story {task}"`. It runs only behind `wants_transcripts`. | `ai-packages/qa-factory/scripts/collect_pack.py:1121-1131` |
| C8 | Site 3 (`tools/collect_intake.py`, **outside the package**) renders each axis on its own: `"stalled: " + {True: "yes", None: "unknown"}.get(v, "no")`, the same for `looped` (only when the key is present). Predicate `stall_laid_out`: `stalled in (True, None) or looped(default False) in (True, None)`. Note `1 in (True, None)` is True in Python, so a manifest `stalled: 1` is laid out and rendered "yes" today. | `tools/collect_intake.py:662-679` |
| C9 | The pair decisions disagree on non-bool values: collector `looped=0` packs, intake `looped=0` is not laid out; collector `stalled="x"` is stalled, intake `stalled="x"` is not laid out. | C5, C8 |
| C10 | `ignored` / `loop_ignored` **do not travel into the manifest**. The story item is `task, plugin_version, touched, closed_at, stalled, stall_signals, looped, loop_signals, transcripts, record`; `_stall` copies `stall_signals`, `record`, `stalled`, `looped`, `loop_signals` only. | `collect_pack.py:1071-1072`, `:1108-1115` |
| C11 | No schema validator lists the story keys; precedent: `looped` / `loop_signals` added under the same `qa-collect/1`. The intake reads story keys with `.get`. | `ai-packages/qa-factory/CHANGELOG.md:652` |
| C12 | The window-round cap is `Driver.window_round_gate`, **`driver_machine.py:319-414`**. The dedup `if not any(...)` is **:363**; the stop record append and `save_state()` are **:364-365**; the question state `{"why": "threshold", "kind": "refusal", ...}` is **:384**; `self.no_move(state)` is **:404** (it raises). The round record append and `save_state()` are **:405-406**; the cause branch starts at **:408**; the refusal cause returns at **:412**, so a point between :406 and :408 covers both causes. Early returns: stage not capped **:337-338**, no key or empty set **:344-345** (docstring EDGES :330-332). `WINDOW_ROUND_CAP = 2` is **`driver_machine.py:45`**; `WINDOW_ROUND_STAGES = {"S5": "qa-code-critic"}` is `driver_dispatch.py:109`. | `ai-packages/qa-factory/scripts/driver_machine.py` |
| C13 | Outcome words the code writes: `same_set` / `cap` **:361**, `to_conductor` **:405**. The finding's `continue` is not one of them. | `driver_machine.py:361`, `:405` |
| C14 | Sibling durable row: `record_round` writes `journal_run({"kind": "gate_repair", ...})`, unguarded, after `save_state()`. | `ai-packages/qa-factory/scripts/driver_gates.py:817-825` |
| C15 | `journal_run(record)` writes `dict(ts=_now(), **record)` through `_append_jsonl` (axis 29) at **:407-409**; it keeps `_open_calls` for `launched` rows and drops entries on a row carrying `is_error`/`exit_code`/`infra` (**:412-419**). | `ai-packages/qa-factory/scripts/driver_runner.py:407-419` |
| C16 | The collector's outcome predicate `_is_outcome` (**:212**): `kind != "launched"` and any of `is_error`/`exit_code`/`infra`. The stall half reads `driver_runs` only in `_k3_k4` (launched and outcome rows, `:243-272`); `_last_activity` (`:312-320`) does not read the driver journal. So a row that is neither launched nor an outcome never touches the stall half. | `collect_stall.py:212`, `:243-272`, `:312-320` |
| C17 | The loop table is data. `rows` rows need `carrier ∈ {driver-runs.jsonl, driver-questions.jsonl}`, an optional `kind`, `values`, `time`; ids may repeat (L4 twice). `load_loops` validates the table. | `ai-packages/qa-factory/references/collect-loops.json:10-17`; `collect_stall.py:725-775` |
| C18 | Docstring "Known gap: a window-round cap question ... queued: a driver-journal row (`kind: window_round`, `outcome`) from story_run.py" is the B-6 leftover; it says "seen only through L1/L5" (correct: L7 reads only `repair_limit`/`exit_limit` question rows, and the window-cap question is `kind: refusal`, R2). | `collect_stall.py:72-74`; `collect-loops.json:16` |
| C19 | `window_round_gate` callers: the real `handle_refusal` (`driver_machine.py:574`); a real driver in `test_no_move_seam_k4s.py:240`, `:243`; the stub `refusal_rig` (`test_probe_gap_door.py:272-294`, a `SimpleNamespace` with **no `journal_run`**) used at `:301`, `:312`, `:323`, `:352` and by `test_probe_not_proved.py:281` (import `:25`); `test_silent_passes.py:623` replaces the gate by a lambda (unaffected). | critic's grep, re-read `test_probe_gap_door.py:272-294` |
| C20 | KB `kb/04-onboarding-doctor.xhtml:408` "what ran, where it stalled, what it cost"; `:417` "The transcripts of stalled stories are in a file of their own"; `skills/qa-collect/SKILL.md:4` "(what ran, where it stalled, what it cost, and your own"; the packer's summary already says "stalled or looped" (`collect_pack.py:1434`). | the three files |
| **C21** | **The journal-kind price table.** `task_price._rows_without_session` (`task_price.py:561-585`) counts every sessionless row of the task's journal unless its `kind` is in `no_call_kinds` of `references/driver-journal-kinds.json` (read by `_no_call_kinds`, `:551-558`, through `hooklib.load_ref_json`; fallback `("delivery", "launched")`). Today's list: `delivery, launched, gate_repair, trace_failed, rows_given_up, stopped_by_person, note`. Any count > 0 makes the price `incomplete`. The keep table `test_task_price.py` (layer `table`, `test-layers.json:6333`, covers `task_price.py`) pins it: `KIND_CASES` `:1049-1063`, the signed-kinds tuple `for _kind in ("trace_failed", "rows_given_up", "stopped_by_person", "note")` at **:1064-1066**, and "an unknown kind without a session still counts" → `incomplete, 1` (`:1051`). | `ai-packages/qa-factory/references/driver-journal-kinds.json:2-11`; `task_price.py:548-585`; `scripts/tests/test_task_price.py:1017-1074` |
| **C22** | **`process` rows already on main** (P1-v W1): `Driver.run` writes `{"kind": "process", "event": "start"|"end", ...}` with no `session_id` and no money (`driver_machine.py:1775-1781`; `driver_journal.process_start_row` / `process_end_row`, `driver_journal.py:552-588`). The comment `driver_journal.py:453-455` claims "every reader that binds sessions, prices or outcomes passes them by", but `process` is not in `no_call_kinds` (C21): every driver story with a process row prices `incomplete` today (critic's run: `'process' in _no_call_kinds()` → False, positive control `gate_repair` → True). | `driver_journal.py:451-455`, `:552-588` |
| **C23** | **A fourth reading of the pair** in `Packer._stall`: `if item["looped"] is None and not verdict.get("stalled") and verdict.get("loop_unreadable_reasons"): self.gap("H", f"loops of {story.name} unknown", ...)`. `item["looped"]` is `verdict.get("looped")` (`:1113`). | `collect_pack.py:1116-1117` |
| **C24** | **Redaction of the manifest.** `_manifest_bytes` passes every string of the manifest through `run.red.text` (keys stay; `sha256`, `src_sha256`, `arc`, `name` values stay), and `_verify` reads the archive back and refuses on any residue the post-check finds. So a new list of `{where, why}` strings in a story item is redacted and post-checked like `loop_signals`. At intake, `make_element` marks each element `held` by `residue_category(text)`. | `collect_pack.py:1359-1369`, `:1378-1395`; `tools/collect_intake.py:583-587` |
| **C25** | **The owner's word on loop transcripts**: «брать ли транскрипты и у стори с петлями (повторные диспатчи, исчерпанный кап)» — «да, брать» (владелец, 30.10.2026). | `plans/piles/release-next/findings/20261030-sbor-transkripty-tolko-zavisshih-petli-ne-vidny.md:11` |
| **C26** | `test_driver_layers.py` is a keep row (layer `gate_named`, "owner of the AR-20 ratchet fixture driver-layers.json; builder-rules 7c DoD row"). | `test-layers.json:28`, `:1386-1409` |

### §0.2 Tests: what exists, what may be used

| # | Fact | Carrier (read-main) |
|---|---|---|
| T1 | `test_collect_stall.py` and `test_collect_pack.py` are **quarantined** (the section starts at **:7126**; entries **:7576** and **:7559**). A builder does not run, fix or edit them (`plans/builder-rules.md` 7b). | `ai-packages/qa-factory/scripts/tests/test-layers.json` |
| T2 | The keep row that covers `collect_stall.py` is `test_driver_stop_record.py` (detector, `:1410-1419`). It holds a real Driver → real `collect_stall.judge` round trip (`round_trip_with_the_collector`, `:281`) and `story_run_has_no_private_appender` (`:329`). | `test-layers.json:1410-1419`; `test_driver_stop_record.py:281`, `:329` |
| T3 | No keep row covers `collect_pack.py` or `references/collect-loops.json`; the positive control (`"collect_stall.py"`) finds `:1418`. | `test-layers.json` (critic re-ran) |
| T4 | The window cap's own case is `s5_window_rounds_are_capped` in `test_story_run_loop_b_loop.py` (keep, detector, **`test-layers.json:5789`**): round 1 `:545-551`, same_set `:559-575`, AT cap `:577-579`, BEYOND `:580-587`, pop `:589-593`, new series `:594-595`, empty sets `:607-614`, scope unreadable `:616-622`. It measures 58.4 s (**`ai-packages/qa-factory/scripts/slow_tests.json:136`**). | `test_story_run_loop_b_loop.py:499-648` |
| T5 | `tools/test_collect_intake.py` (forge pytest, not in `test-layers.json`): the real `collect_pack.pack` → intake join (`real_archive` `:280-300`, `test_the_real_pack_archive_is_read_and_the_schema_pin_holds` `:271-277`) and the layout cases (`:614-641`). | `tools/test_collect_intake.py` |
| T6 | `docs/TESTING.md`: no new test file; a new case is a row; "like before" tests and per-key receipts are not written; outside input gets an adversarial battery. | `docs/TESTING.md:43-59`, `:89-99` |
| T7 | No keep file holds a parameterised table for the collector; rows go into existing case functions (F-8). `test_task_price.py` holds a table (`KIND_CASES`) for the price side. | T2-T5, C21 |
| T8 | Other keep callers of the gate: `test_no_move_seam_k4s.py` (detector, `test-layers.json:3245`, 32.6 s `slow_tests.json:68`); `test_probe_gap_door.py` (data_join, "held by import", `test-layers.json:3780`). | `test-layers.json`; `slow_tests.json` |

### §0.3 Real data (the owner's word, 13.11.2026) and what could not be found

**No collector output (`qa-collect-*.zip` or its manifest) was found in the repository or under `experiments/`.** The intake keeps
its inbox **outside git** (`tools/collect_intake.py:2`, `:7`: `--inbox` / `QA_COLLECT_INBOX`). These searches came back empty:
- `stall_signals|loop_signals|"looped"` in `experiments/` (positive control of the same tool: `stall_signals` in `collect_pack.py` → 2 hits);
- `experiments/**/*.zip` and `experiments/**/manifest.json` (positive control: `experiments/**/*manifest*` finds `.../factory-out/work/automation-manifest.json`);
- `qa-collect-*` in `C:\Users\i_mas\Downloads`;
- intake findings named `*collect-<install8>.md` in `plans/piles/*/findings/`.

The premises below are measured on **real story state folders** (set h); every premise about the bundle's manifest is cited from code.

| # | Premise | Real carrier | Status |
|---|---|---|---|
| R1 | A real looped story keeps only the OPEN window series in `driver-state.json`: one series, one `to_conductor` record, while 14 critic dispatches ran. Earlier series were popped. | `scripts/tests/fixtures/stories/local-1-arm-b/state/driver-state.json:247-258` (`:240-245` the critic ids) | measured |
| R2 | The window-cap question leaves a `driver-questions.jsonl` row of `kind: "refusal"` with **no `why`**; four such rows on one dispatch cannot be told from ordinary refusals. | `.../local-1-arm-b/state/driver-questions.jsonl:24-27` | measured |
| R3 | The same story is looped by other carriers anyway (L4 `repair_limit` with `token: "debt"`; L7 rows). | `.../driver-state.json:260-303`; `driver-questions.jsonl:16-18`, `:30`, `:34` | measured |
| R4 | The sibling `gate_repair` journal row: no `session_id`, no outcome keys, no `dispatch`. | `experiments/mybooks/factory-vs-free-agent/runs/factory-out/state/driver-runs.jsonl:59-61` | measured |
| R5 | Readers of `driver-runs.jsonl` on e4ba384: `collect_stall, dispatch_liveness, driver_conductor, driver_journal, driver_machine, driver_runner, driver_timing, factory_dashboard, friction, infra_failure, retro_numbers, run_counters, story_budget, story_progress, story_run, task_price, walk_timing` (critic's grep `_journal_paths|driver-runs.jsonl|RUNS_NAME|driver_runs`). `task_price` reads through `DJ._journal_paths` / `DJ.read_rows` and **counts unknown sessionless kinds** (C21, the money reader: fixed in N1). `run_counters` counts rows by kind (`NO_KIND`, `:41`). The others were measured by the first draft (`driver_journal`, `driver_timing`, `friction`, `retro_numbers`, `walk_timing`) or are not measured → N1 builder check (a). Outside the package: `experiments/measurers/report_run.journal` (`:141-158`) has no kind filter (§7). | the readers named | partly measured → N1 check (a) |
| R6 | What real `ignored` / `loop_ignored` lists hold. In `local-1-arm-b` every `window_rounds` and `repair_limit` record carries `at`. | R1, R3 lines | **not measured** → N2 builder check |
| R7 | A manifest story item carries exactly the keys in C10. | code `collect_pack.py:1071-1115` | code only → N4 J1 |
| R8 | Collector outputs from other projects exist (the owner's word). | — | **not located**: Q-1 |

---

## §1 What this spec touches (designer rule 1, CLAUDE.md rule 10, P27)

**AR-n touched, with the change check each one demands (copied into the DoD of the node that carries it).**

| AR | Where | The change check (in the DoD) |
|---|---|---|
| AR-1 closed variety is a data row | N1: the journal row's kind and loop values are a row of `collect-loops.json`; the kinds that carry no money (`window_round`, `process`) are rows of `driver-journal-kinds.json`, not literals in `task_price.py` or `collect_stall.py` | `git diff` of `collect_stall.py` in N1 touches only the docstring; `task_price.py` is not in N1's diff; the literals `window_round`, `cap`, `same_set` appear in the two data files and in the writer |
| AR-13 a fact with a reader function is read through it | N2/N4: the pair (stalled, looped) is decided by ONE function `collect_stall.loop_state`, called by the H gate, both sentence sites, `Packer._stall`'s unknown-loop gap (C23) and the intake | after N4, grep `\["looped"\]\|get\("looped"\|get\("stalled"\)` in `collect_stall.py`, `collect_pack.py`, `tools/collect_intake.py` finds only: `loop_state`'s body; `collect_pack.py` `item["stalled"] = ...` (the single-axis stall value written, `:1112`) and `item["looped"] = verdict.get("looped")` (a copy, `:1113`) |
| AR-14 one artifact, one writer | N1: the row goes through `journal_run` → `_append_jsonl` | no new `open(..., "a")`; `test_driver_stop_record.py::story_run_has_no_private_appender` stays green |
| AR-21 / AR-22 every field produced has a reader, every field read has a producer | N1: `window_round` row ↔ the `collect-loops.json` L2 row ↔ the `no_call_kinds` row (same commit). The row's other fields (`stage`, `key`, `round`, `cause`, `findings`) have no reader but the test, like the sibling `gate_repair` row's: a journal row for people reading the journal, accepted as such. N4: `ignored` / `loop_ignored` produced by `judge` → carried by the packer → read by the intake (same commit) | W4 (N1) and J1 (N4) are joins of a real producer and a real reader; P1 (N1) is the price row |
| AR-23 a required list declares its empty outcome | N4: `[]` and an absent key print no line; a non-list prints `unreadable` | rows I2, I3 |
| AR-28 an unknown never becomes a pass | N2: a `looped` that is not literally True/False is UNKNOWN and packs; a `stalled` that is not literally True/False is UNKNOWN, packs, and is worded "not known", never "stalled" (B2, FR-41). N1: an older driver's missing rows stay as today, and the blind spot is named in the docstring and the release note (F-7, A9) | D2's restated acceptance (N2); the docstring text (N1); the fragment (N3) |
| AR-29 code judges data | all: code reports stalled/looped; whether a loop was worth it is the Lead's reading at intake | census: no new unit (below) |

P18 (the price is one and true): N1 lists both bookkeeping kinds in the same commit as the producer, with the defect row P1 in
`test_task_price.py`.

**Checks this spec adds or alters, with their owner and census class (AR-29):**

| Check | Owner | Census class | Census row |
|---|---|---|---|
| L2 from the journal: a `window_round` row with `outcome ∈ {cap, same_set}` after the mark is a loop signal | data | shape (a recorded value in a closed data list) | none: `_l_records` has no raise site; the file's unit is `collect_stall.py::judge` (shape/data, `judgment-census.json:101`) |
| `no_call_kinds` gains `window_round` and `process`: such a sessionless row does not make the price `incomplete` | data | shape (a recorded kind in a closed data list) | none: `task_price.py` has no census unit (grep `task_price` in `judgment-census.json`: no hit; positive control `collect_stall` → `:101`) |
| `loop_state(record)` → (stall, loop) ∈ {yes, no, unknown}² | data | shape (classifies literals by identity) | none: no raise |
| `wants_transcripts` (the H gate) on `loop_state` | data | shape; errs only toward packing | none: no raise |
| `Packer._stall` unknown-loop gap on `loop_state` | data | shape | none (`collect_pack.py::refuse` is the file's unit, `:99`, untouched) |
| `stall_laid_out` (intake) on `loop_state` | data | shape | not a census file (`tools/`) |
| The `window_round` writer; the `ignored` / `loop_ignored` carry | not a check (data producers) | — | — |

Judgment stays where P27 puts it. FR-12: every decision reads recorded values (`True`, `False`, `"cap"`, a kind), never wording.
FR-14: shapes are listed per node. FR-49: the ignored lists travel whole. FR-41: no word claims a stall the record does not hold.

---

## §2 Design (the direction of the finding, made concrete)

1. **The `window_round` row (m-1, B-6 leftover).** `Driver.window_round_gate` writes one `driver-runs.jsonl` row for every series
   record it appends, right after `save_state()`: `{"kind": "window_round", "stage", "key", "dispatch", "round": <len(series) after
   the append>, "cause", "outcome", "findings": <len(found)>}`; `journal_run` adds `ts`. Outcome words are the series' own:
   `to_conductor | same_set | cap` (F-1). The collector reads it through one new `rows` row `L2` of `collect-loops.json`
   (kind `window_round`, field `outcome`, values `["cap", "same_set"]`, time `ts`). **The price reads it as bookkeeping**: `window_round`
   joins `no_call_kinds` in `driver-journal-kinds.json` (B1), and so does `process` (C22, the sweep of the same artifact).
   **What leaves a project changes**: a story whose only loop evidence is a window that hit its cap and was accepted before the
   collect used to be `looped: False` (no transcripts); with the row it is `looped: True` and its transcripts are packed. The owner's
   word covers the class (C25); the release note says it (N3).
2. **One classifier (m-5).** `collect_stall.loop_state(record) -> (stall, loop)`, each `"yes"`, `"no"` or `"unknown"` (F-2). The H gate,
   both sentence sites, `Packer._stall`'s unknown-loop gap and the intake use it. For every verdict `judge` and the packer's exception path
   can produce, the bytes stay; an UNKNOWN stall (hand-made or manifest values only) gets words that say it is not known (B2).
3. **`_l_records` split (m-4).** One function per record shape; the order of signals, ignored entries and reasons stays.
4. **The ignored lists travel.** The packer copies `ignored` and `loop_ignored` into the story item whole (F-3); the intake prints them.
   Content: each `where` is built by the same f-strings as the signals' `where`, which already travel (`collect_stall.py:193`, `:201`,
   `:255`, `:268`, `:284`, `:299`, `:359`, `:380`, `:433`); the only project text among them is L5's `match[:60]` (`:433`), which already
   travels for L5 signals. Each string passes the redactor and the post-check (C24).
5. **The KB says "stalled or looped"** at both places in the page and in the skill's description (F-6).

---

## §3 Nodes

Parallelism: **N1 ∥ N2 ∥ N3**, **N4 after N2** (N4 calls `loop_state`), **N3 merges last** (after N1 and N4 are accepted; A5).
Shared files, disjoint by named function (D-0048): `collect_stall.py` (N1: the module docstring paragraph `L (the loop rule, CL3-9)`
only; N2: functions only); `collect_pack.py` (N2: `_pack_transcripts` + one new constant; N4: `_stories`, `_stall`).
Crossings outside this spec: `driver_machine.py` is shared with FV1-6 (`take_seam_answer`, `seam_chosen`, `seam_rework_step`:
disjoint functions, D-0048) and with FV1-22 N3 (`docs/tasks/specs/20261113-fv1-22-s7-acceptance-loop-spec.md` §3 N3 owns
`window_round_gate`'s early return; in a fix round now): **both change `window_round_gate`, so they are sequential, CL4-1 N1 first**;
FV1-22 N3 merges main and keeps N1's two `journal_run` calls (its new stages then write rows too, and the reader has no stage filter:
intended). FV1-22 N3 also adds rows to `test_probe_gap_door.py`; N1 owns only `refusal_rig` there, and FV1-22's rows inherit its
`journal_run` stub. FV1-22 N2 changes `WINDOW_ROUND_STAGES` (`driver_dispatch.py:109`), which no CL4-1 node owns: no ordering needed.

Witness rule shared by all nodes (deterministic). Run the node's `scenario_walk.py --witness-for` command with the worktree's own
copy of the script (absolute path; it resolves the given paths against its own package, `scenario_walk.py:891-902`) and paste its
print. Then run every printed file that is NOT in the `quarantine` section of `test-layers.json` and whose `slow_tests.json` time is
≤ 60 s or absent. Each printed file above 60 s, and each "no scenario or keep row covers" line, becomes one report line ("judged by
BATCH CANON", builder-rules 7b) and is not run. A test file the DoD names is run even if the print omits it. The shell's cwd never moves.

### N1 — CL4-1a: the `window_round` row, its reader and its price row (driver + data)

given: this spec §0-§2; `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md`; `docs/TESTING.md`;
`ai-packages/qa-factory/scripts/driver_machine.py:305-415`; `driver_gates.py:817-825` (sibling); `driver_runner.py:407-419`;
`driver_journal.py:451-455`, `:552-588`; `task_price.py:548-585`; `references/driver-journal-kinds.json`; `references/collect-loops.json`;
`collect_stall.py:1-115`, `:156-168`, `:212`, `:243-272`, `:373-417`; `scripts/tests/test_story_run_loop_b_loop.py:499-648`;
`scripts/tests/test_probe_gap_door.py:272-294`; `scripts/tests/test_task_price.py:1017-1074`; `scripts/tests/test_no_move_seam_k4s.py:222-251`.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n1\ai-packages\qa-factory\scripts\driver_machine.py (function `Driver.window_round_gate` only)
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n1\ai-packages\qa-factory\references\collect-loops.json
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n1\ai-packages\qa-factory\references\driver-journal-kinds.json
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n1\ai-packages\qa-factory\scripts\collect_stall.py (module docstring, paragraph `L (the loop rule, CL3-9)`, lines 61-78 only)
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n1\ai-packages\qa-factory\scripts\tests\test_story_run_loop_b_loop.py (function `s5_window_rounds_are_capped` only)
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n1\ai-packages\qa-factory\scripts\tests\test_probe_gap_door.py (function `refusal_rig` only)
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n1\ai-packages\qa-factory\scripts\tests\test_task_price.py (the signed-kinds tuple `for _kind in (...)` at :1064 only)
Why the two price files are N1's: the producer of a new journal kind and its price row change in one commit (AR-22, P18); `process`
rides along because it is the same data row and the same test tuple (sweep of the same artifact; its producer is already on main).
non-goals: no change to the cap, the question text, `no_move`, `driver-questions.jsonl` rows, `gate_repair` rows, `task_price.py`
code, any other reader of `driver-runs.jsonl`, or any collector function; no new test file; no `CHANGELOG.md` / `changelog.d` edit (N3).
handoff: report per `.claude/agents/builder.md` rule 7, with the FR pass by section (A, C, D, F, G apply — F: FR-25/P18 the price; B: no
text a person reads changed), the witness print and runs verbatim, builder checks (a)-(c), and the §6 axis block for M1.

**What to change**

1. `driver_machine.py`, `Driver.window_round_gate`:
   - **Stop path.** Inside the dedup block `if not any(...)` (`:363`), right after `series.append({...})` (`:364`) and
     `self.save_state()` (`:365`), add
     `self.journal_run({"kind": "window_round", "stage": stage, "key": key, "dispatch": dispatch, "round": len(series), "cause": cause, "outcome": reason, "findings": len(found)})`.
   - **Round path.** Right after `series.append({... "outcome": "to_conductor" ...})` (`:405`) and `self.save_state()` (`:406`), and
     before `number = len(mine) + 1` and the cause branch (`:407-408`), add the same call with `"outcome": "to_conductor"`. One
     insertion covers both causes (the refusal cause returns at `:412`, after it).
   - Docstring, one sentence: "Every series record is mirrored by a `window_round` row of the driver journal (`journal_run`), which
     outlives the pop at acceptance; `collect_stall` reads it through `references/collect-loops.json` (L2), and `task_price` passes it by
     (`references/driver-journal-kinds.json`)."
2. `references/collect-loops.json`: append to `records`
   `{"id": "L2", "carrier": "driver-runs.jsonl", "kind": "window_round", "shape": "rows", "field": "outcome", "values": ["cap", "same_set"], "time": "ts", "what": "a window's rework rounds hit their cap or came back with the same findings - the driver journal's copy of the window_rounds record, which the driver pops when the window is accepted"}`.
   In `note`, replace "test_collect_stall.py ties them" with "test_collect_stall.py and test_story_run_loop_b_loop.py tie them".
3. `references/driver-journal-kinds.json`: append `"window_round"` and `"process"` to `no_call_kinds`, and to `why`:
   - `"window_round": "Round bookkeeping of a rework window (driver_machine.window_round_gate): the row carries no session and no money of its own; the conductor call a round precedes is journalled by its own row, which counts if it has no session."`
   - `"process": "The driver's own process start and end rows (P1-v, driver_journal.process_start_row / process_end_row): the row launches no model call and carries no session and no money; its end key is process_code, never exit_code."`
4. `collect_stall.py` module docstring, lines 72-74. Replace "Known gap: a window-round cap question (`no_move` kind `refusal`, why
   `threshold`) leaves no durable row, so a window that hit the cap and then closed is seen only through L1/L5; queued: a driver-journal
   row (`kind: window_round`, `outcome`) from story_run.py." with: "L2 reads two carriers: the open `window_rounds` of driver-state.json
   and the driver journal's `window_round` rows (`driver_machine.window_round_gate` writes one per series record; the journal outlives the
   pop). Known gap: a story run by a driver older than that row has none, so a window of it that hit the cap and closed before the
   collect is seen only through L1/L5. The rule does not read the story's `plugin_version` to tell: the version that first writes the
   row is not known when the row is written. This paragraph and the release note are the carriers of that gap (CL4-1)." Keep
   "Exceeded caps only (a cap exactly reached is not a loop)." and everything after it.
5. `test_probe_gap_door.py`, `refusal_rig`: add `d.journal_rows = []` and `d.journal_run = lambda record: d.journal_rows.append(record)`.
   No expectation of any test in that file or in `test_probe_not_proved.py` changes.
6. `test_task_price.py:1064`: the tuple becomes `("trace_failed", "rows_given_up", "stopped_by_person", "note", "window_round", "process")`.

**Edges (decided), each with the invariant it protects**

| Edge | Behaviour | Invariant |
|---|---|---|
| POSITIONAL: the stop row | inside the dedup block, after `save_state()`, before `self.no_move(state)` (`:404`) | one row per series record: a re-asked question (the same set again, FR-7) adds no row; the row is on disk before the question raises, because nothing after `no_move` runs |
| POSITIONAL: the round row | after `:406`, before `:407-408` | a round that is paid for always has its row, whatever its cause (both causes pass this point) |
| Early returns (`:337-338` stage not capped; `:344-345` no key or empty set) | no row | an empty set is never recorded (the series' own edge), and the journal mirrors the series exactly |
| Row keys | never `is_error`, `exit_code`, `infra`, `session_id`, `started_at` or `dispatch_id` | the row never clears a K3 (`collect_stall.py:212`), an `_open_calls` entry (`driver_runner.py:416-419`), never joins a session in `driver_journal`, never ends a hop in `driver_timing`, never touches the stall half (C16) |
| Price: a `window_round` or `process` row with no session | not counted (P1) | a kind is listed only when its row has no session and no money and every model call its writer starts has its own row (`task_price.py:566-570`); an unknown kind without a session still counts (`:1051`, unchanged) — an unknown is never "complete" (FR-41) |
| Price: kinds file absent / unreadable / bad key | the fallback `("delivery", "launched")`: both new kinds count → `incomplete` (existing rows `:1054-1062`) | the error direction of the reused `_rows_without_session` stays toward `incomplete`; no input makes a sessionless unknown row free |
| Price: a row of either kind that carries a `session_id` | bound like any row (existing, `:1072-1074`) | listing a kind never hides a real session |
| `journal_run` raises `OSError` | not caught (as the sibling `record_round`, C14) | one road with the sibling; a loud stop, never a silent loss |
| Limits | none added. Rows per window ≤ `WINDOW_ROUND_CAP` per cause × 2 causes + one stop per distinct (set, reason). `findings` is a count; the set is not copied (it is in the question's details and holds host paths, R1 `:253`; AR-4) | no truncation exists; the existing AT/BEYOND cap case (`:577-587`) stays as it is |
| TEMPORAL: before / after N1 | before: no `window_round` rows, the new L2 row matches nothing, every verdict byte-identical; `process` rows price `incomplete` (defect on main). After: rows from the first round of a new run on; prices with `process` rows can reach `agrees` | an older story's loop verdict never changes (F-7); a price only moves from a false `incomplete` toward the truth |
| TEMPORAL: older stories (no rows) | a window that capped and closed before the collect stays `looped: False` unless L1/L5 see it; the gap is named in the docstring and the release note, not per story | an unknown is not stated as a fact (FR-41) and nothing more leaves a project for older stories (F-7) |
| A window still open at collect time | two L2 signals for one stop (state + journal), different `where` | `looped` is True either way; nothing counts L2 signals |
| A later stage wired into the cap (FV1-22) | its rows carry its `stage`; L2 reads them (no stage filter) | a capped window on any stage is a loop; no stage literal in the data row (AR-1, P31) |
| A story both stalled and looped | the loop half adds L2; the stall half is untouched | the loop half never adds to `signals`, `unreadable_reasons` or `ignored` (`collect_stall.py:63-64`) |
| Torn journal tail / broken middle line | existing `_jsonl_rows` (`collect_stall.py:571-594`): tail left alone; a broken middle line is a loop reason → `looped` None (packs) | no new read path |

**Test rows** (existing functions in keep files; row ids are check-name prefixes; per-edge receipts are not written, A10):
- `s5_window_rounds_are_capped`. Read the rows of `<state dir>/driver-runs.jsonl` with `kind == "window_round"`; the state dir is
  `task_root / "state"` (where `held()` reads `driver-state.json`, `:536-537`). Builder check: if `driver.state_dir` is another folder, read from it.
  - **CL4-1 W1** (right after `:587`, one join check of the two carriers): `[(r["stage"], r["key"], r["dispatch"], r["round"], r["cause"], r["outcome"], r["findings"]) for r in rows]`
    equals `[("S5", key, h["dispatch"], i, h["cause"], h["outcome"], len(h["set"])) for i, h in enumerate(held(), 1)]` (4 rows; this
    also proves the person's repeats at `:573` and `:586` added none).
  - **CL4-1 W4** (right after the pop check `:593`, before `:594`): the join with the real collector —
    `CS.judge({"closed": True, "unreadable": [], "driver_runs": CS._jsonl_rows(path, "driver-runs.jsonl", []), "driver_state": dict(closer.state), "driver_state_present": True}, None, 1_900_000_000, 0, CS.load_loops())`
    gives `sorted(s["where"] for s in v["loop_signals"] if s["where"].startswith("driver-runs.jsonl window_round"))` ==
    `["driver-runs.jsonl window_round row cap", "driver-runs.jsonl window_round row same_set"]` and `v["looped"] is True`
    (`import collect_stall as CS` inside the function). This is the defect row: it fails on today's code.
  - **CL4-1 W5** (same place): every `window_round` row: `not CS._is_outcome(row)` and none of `is_error`, `exit_code`, `infra`, `session_id`.
- `test_task_price.py`: **CL4-1 P1** = the two new tuple entries; each runs `_shipped([{"ts": ..., "kind": k}])` → `agrees, 0` (the
  defect rows: `incomplete, 1` before step 3).

**DoD**
- W1, W4, W5 and P1 pass. Every check that existed in `s5_window_rounds_are_capped`, `test_probe_gap_door.py`,
  `test_probe_not_proved.py`, `test_task_price.py` and `test_no_move_seam_k4s.py` passes unchanged.
- AR-1 check: `git diff -- ai-packages/qa-factory/scripts/collect_stall.py` shows docstring lines only; `task_price.py` is not in the diff.
- AR-14 check: `test_driver_stop_record.py` passes (`story_run_has_no_private_appender` included).
- Builder checks (results in the report):
  - (a) For each reader of `driver-runs.jsonl` in R5 (17 modules, `task_price` and `run_counters` included), name (file:line) any
    reader that counts rows or reacts to a row without a `kind` filter. The money reader is fixed in this node by the data row (step 3);
    report every other reader found and fix none.
  - (b) if `test_driver_layers.py` reports a ceiling breach for `driver_machine.py`, stop and return it as a question (AR-20).
  - (c) run `python -B -c "import sys; sys.path.insert(0, r'<worktree>\ai-packages\qa-factory\scripts'); import task_price as TP; print(sorted(TP._no_call_kinds()))"` and paste the output (a pure read; it must list both new kinds).
- Witness: `python -B C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n1\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_machine.py ai-packages/qa-factory/references/collect-loops.json ai-packages/qa-factory/references/driver-journal-kinds.json ai-packages/qa-factory/scripts/collect_stall.py ai-packages/qa-factory/scripts/tests/test_story_run_loop_b_loop.py ai-packages/qa-factory/scripts/tests/test_probe_gap_door.py ai-packages/qa-factory/scripts/tests/test_task_price.py`,
  then the shared rule. Always run (absolute paths in the worktree): `test_story_run_loop_b_loop.py` (58.4 s, under the 60 s line),
  `test_probe_gap_door.py`, `test_probe_not_proved.py`, `test_task_price.py`, `test_no_move_seam_k4s.py`, `test_driver_stop_record.py`,
  `test_driver_layers.py` (7c).
- Commit lines: `architecture: AR-1, AR-14, AR-22 -- the row goes through journal_run; its loop reader and its price row are data rows in the same commit`;
  `judgment: none -- a data producer and two data rows`.

siblings: `gate_repair` (L3 reader, same writer road, already a `no_call_kinds` row: the pattern followed); `process` (folded in);
axis 29 (appender); axis 5 (twins); axis 6 (`report_run.journal`, §7). The question row's missing `why` (R2) is listed in §7.

### N2 — CL4-1b: one classifier, the H gate on it, the sentence sites, the `_l_records` split

given: this spec §0-§2; `design/factory-rules.md`; `plans/builder-rules.md`; `docs/TESTING.md`; `ai-packages/qa-factory/references/human-questions.md`;
`collect_stall.py` (whole); `collect_pack.py:1096-1140`; `scripts/human_text.py` (`problems`); the real folders
`scripts/tests/fixtures/stories/local-1-arm-b/state/` and `experiments/mybooks/factory-vs-free-agent/runs/factory-out/state/driver-runs.jsonl`.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n2\ai-packages\qa-factory\scripts\collect_stall.py (functions `_l_records`, `wants_transcripts`, `select_transcripts`; new functions `_l_rows`, `_l_state`, `_l_series`, `_l_records_flat`, `_l_nested`, `loop_state`; new constants `YES`, `NO`, `UNKNOWN`, `_WHY`; NOT the module docstring)
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n2\ai-packages\qa-factory\scripts\collect_pack.py (method `Packer._pack_transcripts` and a new module constant `_STATE_WORDS` only)
non-goals: no change to the verdict's keys or to any `where` text; no change to `Packer._stall` or `tools/collect_intake.py` (N4); no
committed test (F-4); no edit to quarantined files.
handoff: report with the FR pass (B, C, D, G apply; B: the new unknown-stall texts with their `human_text.problems` output), the
differential script in full with its output and negative control, the R6 check, and the witness.

**What to change**

1. Directly above `wants_transcripts` (`:495`):
   ```
   YES, NO, UNKNOWN = "yes", "no", "unknown"

   def loop_state(record):
       """(stall, loop) of a verdict or of a manifest story: each YES, NO or UNKNOWN. The ONE reading of the pair (CL4-1):
       True is YES, False is NO, anything else (None, a missing `stalled`, a non-bool such as 0, 1 or "x") is UNKNOWN; a
       missing `looped` is NO (an older producer). Not a dict: (NO, NO) - no record, no story."""
   ```
   Body: `if not isinstance(record, dict): return NO, NO`; `s, l = record.get("stalled"), record.get("looped", False)`; return
   `(YES if s is True else NO if s is False else UNKNOWN, YES if l is True else NO if l is False else UNKNOWN)`. Identity (`is`), never `==` (`1 == True`).
2. `wants_transcripts(verdict)`: `return loop_state(verdict) != (NO, NO)`. Keep the docstring and add: "errs only toward packing: any
   value that is not literally True or False is unknown, and unknown packs."
3. `select_transcripts`: keep the early return byte for byte. Replace the `why` expression (`:530-532`) with
   `why = _WHY[loop_state(verdict)]`, where (written with the constants)
   `_WHY = {(YES, YES): "the story is stalled and looped", (YES, NO): "the story is stalled", (YES, UNKNOWN): "the story is stalled", (NO, YES): "the story looped", (NO, UNKNOWN): "whether the story looped is not known", (UNKNOWN, YES): "the story looped; whether it stalled is not known", (UNKNOWN, NO): "whether the story stalled is not known", (UNKNOWN, UNKNOWN): "whether the story stalled or looped is not known"}`.
   `(NO, NO)` is absent on purpose: the early return in the same function precedes it.
4. `Packer._pack_transcripts` (`:1128-1131`): `state = _STATE_WORDS[collect_stall.loop_state(verdict)]` with, written with the
   `collect_stall` constants,
   `_STATE_WORDS = {(YES, YES): "stalled and looping", (YES, NO): "stalled", (YES, UNKNOWN): "stalled", (NO, YES): "looping", (NO, UNKNOWN): "possibly looping", (UNKNOWN, YES): "looping and possibly stalled", (UNKNOWN, NO): "possibly stalled", (UNKNOWN, UNKNOWN): "possibly stalled or looping"}`.
   `(NO, NO)` is absent: the only caller, `Packer._stall`, calls this method only when `wants_transcripts(verdict)` is True on the same object.
5. `_l_records` split. `_l_records(facts, floor, table, ignored, reasons)` keeps its signature and return value. It builds `state`,
   `out` and the two closures as today, then for each row in `table["records"]`: if `row["shape"] == "rows"` it calls
   `_l_rows(facts, row, take, hit)`; otherwise `_l_state(state, row, take, hit, reasons)`. `_l_state` reads `held` and `label` as today and,
   for each `(name, rec)`, checks the shape (`want`) exactly as `:397-400`. It then dispatches through
   `{"series": _l_series, "records": _l_records_flat, "nested_records": _l_nested}[row["shape"]](row, label, name, rec, take, hit, reasons)`.
   Each helper holds today's branch body unchanged. Nesting inside any function: ≤ 3 block levels (for/if/while/with/try).

**Edges (decided)**

| Edge | Behaviour | Invariant |
|---|---|---|
| Every verdict `judge` can produce (`stalled` bool, `looped` True/False/None) and the packer's exception verdict (`stalled: True, looped: None`, `collect_pack.py:1106`) | gate, `why` and gap word byte-identical to today | FR-14: the output texts are the contract |
| `looped` = 0, `""`, `[]`, `"x"` (hand-made) | UNKNOWN → packs (as today: `0 is not False`); with `stalled` True/False the words are today's | the gate errs only toward packing (AR-28, FR-59) |
| `stalled` = None, missing, 0, 1, `"x"` (hand-made; `judge` never writes them, `collect_stall.py:337`) | UNKNOWN → packs, and the words say the stall is not known ("whether the story stalled is not known", "possibly stalled", and the combined keys) | an unknown is never worded as a fact (FR-41, `collect_pack.py:26` "None is the unknown"); the gate delta is old-no-pack → new-pack only |
| Not a dict | (NO, NO) → no transcripts, `why` from the early return | as today (`{}` was "neither") |
| Missing `looped` | NO | the older producer stays read as not looped (`collect_stall.py:77`, `:497`) |
| `(NO, NO)` key | absent from both tables | unreachable: both lookups sit behind the gate on the same verdict; a KeyError there would be a gate defect, loud, never a false word |
| `_l_records` order | signals, ignored entries and reasons in the same order as today | `reasons` are deduplicated in order (`:448`); the manifest lists signals in order |
| A record in an unknown shape | a reason, the rest still read (`_not_read` at the same point) | never "no loop" on a shape the rule does not know |

**Mechanical layer (F-4: a report attachment, never committed).** A script in the scratchpad, run twice as two processes:
- **old**: a scratch folder holding `git -C C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n2 show origin/main:ai-packages/qa-factory/scripts/collect_stall.py`
  and `...collect_pack.py` (written by the Write tool into the scratchpad, outside the git tree), FIRST on `sys.path`, the worktree's
  `ai-packages/qa-factory/scripts` after it (for every other import);
- **new**: the worktree's `scripts` only.
Each run prints `collect_stall.__file__` and `collect_pack.__file__` (they must show scratch vs worktree; otherwise the run is void) and
one JSON line per grid row; a third step compares the two outputs.
- **D1** `_l_records(facts, float("-inf"), load_loops(), [], [])` → `(out, ignored, reasons)`, equal in order, over: `facts` from
  `local-1-arm-b/state/driver-state.json` and `driver-questions.jsonl`; the factory-out `driver-runs.jsonl` rows; and the shape variants
  `window_rounds` as a list; a series that is a string; a series item without `at`; `at: "yesterday"`; `repair_limit` as a list; a
  `repair_limit` record that is a list; `exit_limit` whose `rounds` is a list; a `rounds` item that is a string; `granted` ∈ {True, 0, 1, 2, "1"}.
- **D2** over `stalled ∈ {True, False, None, <missing>, 0, 1, "x"}` × `looped ∈ {True, False, None, <missing>, 0, "x"}`, plus `v = "str"`:
  - the gate `wants_transcripts(v)`;
  - the `why`: `select_transcripts(v, [{"sid": "s", "transcript": "t.jsonl", "exists": True}], [])["why"]`;
  - the pack word (A1): call `collect_pack.Packer._pack_transcripts(stub, Path(<tmp>) / "T1", v, {})` with
    `stub = SimpleNamespace(project=Path(<tmp>), gap=lambda s, what, why: gaps.append(what), _host_subagents=lambda: [], _transcript=lambda *a, **k: None)`
    and `collect_pack.collect_stall.session_transcripts` patched to `lambda project, story: []`; the captured `what` is
    `"no transcripts for the <state> story T1"`. Call it only where that version's gate is True; else record `"not called"`.
  Acceptance: (i) every row with `stalled is True or stalled is False` (identity) is identical in all three outputs; (ii) every gate delta
  is old False → new True; (iii) every `why` / word delta is on a row whose `stalled` is neither `True` nor `False`, and the script prints
  each delta row; (iv) `human_text.problems(s)` is `[]` for each of the four new `_WHY` strings and the three new `_STATE_WORDS`
  strings inside their sentence (`"no transcripts for the <state> story T1"`), output pasted.
- **Negative control**: one run where a copy of the new `_STATE_WORDS` has one word changed on a `stalled ∈ {True, False}` row; the
  compare must report a difference.

Builder check **R6**: run `collect_stall.judge(collect_stall.read_facts(<tmp project>, <fixtures/stories/local-1-arm-b>, now), None, now, 24, collect_stall.load_loops())`
(read-only) and paste `len(ignored)`, `len(loop_ignored)` and the first three entries of each.

**DoD**
- D1 and D2 pass by (i)-(iv); the negative control fails as it should (output pasted).
- AR-13 check (this node's half): grep `get\("looped"\|get\("stalled"\)` in `collect_stall.py` finds it only inside `loop_state`.
- Nesting ≤ 3 in the six functions `_l_records`, `_l_rows`, `_l_state`, `_l_series`, `_l_records_flat`, `_l_nested`, stated per function.
- Witness: `python -B C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n2\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/collect_stall.py ai-packages/qa-factory/scripts/collect_pack.py`,
  then the shared rule; `test_driver_stop_record.py` is always run.
- Commit lines: `architecture: AR-13, AR-28 -- one reader of the pair; unknown packs and is worded as not known`; `judgment: none -- data classification`.

siblings: `Packer._stall`'s unknown-loop gap and `tools/collect_intake.py::stall_laid_out` / `stall_elements` (N4, same classifier).

### N3 — CL4-1c: the KB page, the skill description, the changelog fragment (merged last)

given: this spec §0, §2; `kb/04-onboarding-doctor.xhtml:406-418`; `ai-packages/qa-factory/skills/qa-collect/SKILL.md:1-8`;
`ai-packages/qa-factory/changelog.d/README.md`.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n3\kb\04-onboarding-doctor.xhtml (lines 408 and 417 only)
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n3\ai-packages\qa-factory\skills\qa-collect\SKILL.md (line 4, and 5 only if re-wrapped)
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n3\ai-packages\qa-factory\changelog.d\collect-4-cl4-1.md (new)
non-goals: no other wording; no test that pins KB text (`docs/TESTING.md:93`, `:99`).
handoff: report with the doc-dispatch witness (CLAUDE.md rule 11: keys quoted verbatim from this DoD, the script in full, a negative control).
Order: written in parallel with N1/N2; its branch merges after N1 and N4 are accepted. If an accepted node's behaviour differs from
the fragment, the Lead edits the fragment before the merge (A5).

**What to change**
1. `kb/04-onboarding-doctor.xhtml:408`: "what ran, where it stalled, what it cost" → "what ran, where it stalled or looped, what it cost".
2. `kb/04-onboarding-doctor.xhtml:417`: "The transcripts of stalled stories are in a file of their own" → "The transcripts of stalled or looped stories are in a file of their own".
3. `SKILL.md:4`: "(what ran, where it stalled, what it cost, and your own" → "(what ran, where it stalled or looped, what it cost, and your own".
   Re-wrap lines 4-5 only if line 4 goes over 120 characters.
4. `changelog.d/collect-4-cl4-1.md`, verbatim (the Lead appends ` (B-nnn)` to the first bullet when the integrator issues the id):
   ```
   - Driver (`driver_machine.py`): every rework round of an S5 window that goes to the conductor, and the stop at the cap or at a
     repeated finding set, also writes a `window_round` row to `driver-runs.jsonl` (`stage`, `key`, `dispatch`, `round`, `cause`,
     `outcome`, `findings`). The collector reads it (`references/collect-loops.json`, L2), so a window that hit its cap and was
     accepted later still counts as a loop, and that story's transcripts are now sent with the archive, like a stalled story's.
     Stories run by an earlier version keep no such row: a capped window of theirs accepted before the collect is not seen as a loop.
   - Task price (`references/driver-journal-kinds.json`): `window_round` rows and the driver's own `process` rows are bookkeeping
     with no session and no money, so they no longer make a story's price `incomplete`.
   - Collector (`collect_stall.py`, `collect_pack.py`): each story of the manifest carries `ignored` and `loop_ignored`, the records
     the stall and loop rules could not use because they hold no time, and the intake lists them; whether a story stalled and
     whether it looped is read in one place (`collect_stall.loop_state`). qa-collect and its page say "stalled or looped".
   ```

**Edges**: the KB source stays English (FR-30); the fragment is lower-case bullets with no heading line (`changelog.d/README.md`);
the SKILL.md size cap of 19000 bytes (`plans/builder-rules.md` 5) grows by 10 bytes; no Cyrillic in the fragment (`--lang`).

**DoD**
- Keys (verbatim, checked by the script): `where it stalled or looped, what it cost` in `kb/04-onboarding-doctor.xhtml`;
  `The transcripts of stalled or looped stories are in a file of their own` in `kb/04-onboarding-doctor.xhtml`;
  `where it stalled or looped, what it cost, and your own` in `SKILL.md`; `that story's transcripts are now sent with the archive` and
  `no longer make a story's price` in the fragment; and the absence of `transcripts of stalled stories` in the KB file.
  Negative control: the same script with one key changed reports a failure.
- `python -B <worktree>/ai-packages/qa-factory/scripts/changelog_assemble.py --list` lists `collect-4-cl4-1.md` and does not mark it `REFUSED`.
- Witness: `python -B C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n3\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/skills/qa-collect/SKILL.md ai-packages/qa-factory/changelog.d/collect-4-cl4-1.md`,
  then the shared rule. Also `python -B <worktree>/ai-packages/qa-factory/scripts/selftest.py --limits --lang`. If it needs the package
  folder as cwd, run it through a `( cd <worktree>\ai-packages\qa-factory && ... )` subshell (a hygiene door).
- Commit lines: `architecture: none -- documentation, a skill description and a release note`; `judgment: none -- text`.

siblings: `collect_pack.py:1434` (already "stalled or looped"); grep `stalled` in `kb/` finds only `06-roadmap.xhtml:15` (a run, not the
collector); the critic's case-insensitive grep of `skills/`, `references/`, `kb/` found no other stalled-only text.

### N4 — CL4-1d: the ignored lists travel, the fourth pair site, the intake reads them (after N2)

given: this spec §0-§2; `design/factory-rules.md`; `plans/builder-rules.md`; `docs/TESTING.md`; `collect_pack.py:1057-1140`, `:1359-1400`;
`collect_stall.py:156-168`, `:328-340`, `:480-533` and N2's `loop_state`; `tools/collect_intake.py:28-60`, `:105-115`, `:370-385`,
`:583-592`, `:662-679`, `:720-830`; `tools/test_collect_intake.py:20-100`, `:266-300`, `:605-641`.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n4\ai-packages\qa-factory\scripts\collect_pack.py (methods `Packer._stories`, `Packer._stall` only)
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n4\tools\collect_intake.py (functions `stall_laid_out`, `stall_elements` only, and one `import collect_stall` line after `import collect_pack` at :58)
C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n4\tools\test_collect_intake.py (functions `real_archive`, `test_the_real_pack_archive_is_read_and_the_schema_pin_holds`, `test_a_story_that_looped_is_laid_out_like_a_stalled_one`, `test_the_layout_text_of_a_looped_only_story_says_stalled_no` only)
non-goals: no schema bump (C11); no sanitiser for element text (§7); no change to the `stalled`/`looped` values written in the manifest.
handoff: report with the FR pass (C, D, E apply; FR-49 named; B: the intake text is a forge report, not a person-facing factory text),
the D3 differential in full with its negative control, the witness, and the §7 analog line if confirmed.

**What to change**
1. `Packer._stories`: the initial item gains `"ignored": [], "loop_ignored": []`, placed after `"stall_signals"` and `"loop_signals"`.
2. `Packer._stall`, after `item["loop_signals"] = ...` (`:1114-1115`):
   `item["ignored"] = [{"where": e.get("where"), "why": e.get("why")} for e in verdict.get("ignored") or [] if isinstance(e, dict)]`,
   and the same for `item["loop_ignored"]` from `verdict.get("loop_ignored")` (the copy form of the signal lists, `:1109`, `:1114`).
3. `Packer._stall`, the unknown-loop gap (`:1116`, A2): `stall, loop = collect_stall.loop_state(verdict)`; the condition becomes
   `loop == collect_stall.UNKNOWN and stall != collect_stall.YES and verdict.get("loop_unreadable_reasons")`. The gap text is unchanged.
4. `collect_intake.stall_laid_out(story)`:
   `return isinstance(story, dict) and collect_stall.loop_state(story) != (collect_stall.NO, collect_stall.NO)`.
   Add `import collect_stall  # noqa: E402` right after `import collect_pack` (`:58`; the package `scripts/` is already on `sys.path`, `:57`).
   Keep the docstring and add "(collect_stall.loop_state)".
5. `collect_intake.stall_elements`. `stall, loop = collect_stall.loop_state(story)`; use `"stalled: " + stall` and `"looped: " + loop`
   (keep the `if "looped" in story` condition for the looped block). After the stall signal lines add `ignored_lines("ignored")`; after the
   looped block add `ignored_lines("loop ignored")`, from one local helper inside `stall_elements` reading `story.get(key)`:
   - key absent, or `[]` → no line;
   - not a list → one line `"<label>: unreadable (<type name>)"`;
   - a list → `"<label>: <N>"` (N counts the dict entries), then one `"%s | %s" % (e.get("where"), e.get("why"))` per dict entry; non-dict
     entries are skipped (as signal lines skip them).

**Edges (decided)**

| Edge | Behaviour | Invariant |
|---|---|---|
| TEMPORAL 1: an archive packed before N4 (no `ignored` / `loop_ignored` keys), bool/None pair | no new line; element text byte-identical | its `csha` (`collect_intake.py:586`) matches the index, so a re-run intake never sees the old story as changed |
| TEMPORAL 2: packed after N4, nothing ignored | `[]` → no line; text byte-identical to TEMPORAL 1 | the empty outcome is declared (AR-23) |
| TEMPORAL 3 (A4): a story laid out from an older archive, re-collected by the new packer with a non-empty list | new lines → its `csha` changes → the index (`:728`, `:810`, `:826`) shows it as changed **once** | expected, one time, no action: new evidence is shown, never hidden behind an old hash |
| Not onboarded / the stall rule raised (`collect_pack.py:1073`, `:1105-1107`) | the lists stay `[]` | `stalled`/`looped` None already say unknown; `[]` claims nothing more than `loop_signals: []` |
| The unknown-loop gap (step 3) on every verdict `judge` and the exception path produce | byte-identical (`looped` None ⇔ UNKNOWN; `stalled` bool ⇔ YES/NO); the exception verdict (`stalled: True`) still gets no gap | D3 (i); deltas only on hand-made values: a verdict with no `looped` key now gets no gap (read as not looped everywhere, P31), a non-bool `looped` now gets one |
| Size | carried whole, no cap (FR-49); the manifest's ceiling `part_max_bytes` (`collect_intake.py:371-380`) bounds the intake | no new limit, so no new AT/BEYOND case; the ceiling's own cases stay where they are (builder check: name them, file:line) |
| Hostile pair in a manifest (`"x"`, 0, 1) | UNKNOWN → laid out, text `unknown` (today `1` reads "yes": `1 in (True, None)`) | the intake errs toward laying a story out; collector and intake read the pair one way (P31) |
| Order in one element | `stalled:` line, stall signals, ignored block, `looped:` line, loop signals, loop ignored block | one fixed order (row I1) |
| `where`/`why` not a string (None, int, nested dict) | rendered by `%s` (`None`, `3`, `{'a': [1]}`), no crash | outside data never crashes the intake (row I7) |
| `where` with a lone surrogate or non-ASCII | rendered as is; `csha` encodes with `"replace"` (`:586`) | no crash on encoding (row I8) |
| `where`/`why` with control bytes | rendered as signal lines are today (not sanitised) | one road with the signal lines; the class is in §7 |
| Content leaving the project | the same `where` strings the signals carry (§2.4); every string passes `_manifest_bytes` and `_verify` (C24) | no new content class leaves a project (F-3) |

**Adversarial battery (outside input: a manifest from another project).** Rows I3-I9 below: broken type (I3), broken entry (I4),
hostile bools (I5, I10), non-string values (I7), encoding (I8), magnitude (I9), empty (I2). Transcripts (broken/empty/huge, wrong
encoding): **n/a** — no node changes how a transcript is found or read (`session_transcripts`, `select_transcripts`' paths, the packer's
copy), only which stories are selected.

**Test rows** (`tools/test_collect_intake.py`, existing functions):
- `test_the_layout_text_of_a_looped_only_story_says_stalled_no`: add these stories to its manifest as one list of `(story, expected)`
  pairs, each assert message naming the task id (P16):
  - **I1** T4 `{"stalled": True, "stall_signals": [{"id": "K3", "where": "w3", "at": "a"}], "ignored": [{"where": "iw", "why": "no usable time, so never a signal"}], "looped": True, "loop_signals": [{"id": "L2", "where": "lw", "at": "b"}], "loop_ignored": [{"where": "lw2", "why": "y2"}, {"where": "lw3", "why": "y3"}]}` → `"stalled: yes\nK3 | w3 | a\nignored: 1\niw | no usable time, so never a signal\nlooped: yes\nL2 | lw | b\nloop ignored: 2\nlw2 | y2\nlw3 | y3"`
  - **I2** T5 `{"stalled": False, "looped": True, "ignored": [], "loop_ignored": []}` → `"stalled: no\nlooped: yes"`
  - **I3** T6 `{"stalled": False, "looped": True, "loop_ignored": "x"}` → `"stalled: no\nlooped: yes\nloop ignored: unreadable (str)"`
  - **I4** T7 `{"stalled": False, "looped": True, "loop_ignored": [1, {"where": "w", "why": "y"}]}` → `"stalled: no\nlooped: yes\nloop ignored: 1\nw | y"`
  - **I5** T8 `{"stalled": "x", "looped": 0}` → `"stalled: unknown\nlooped: unknown"`
  - **I7** T9 `{"stalled": False, "looped": True, "loop_ignored": [{"where": None, "why": 3}, {"where": {"a": [1]}, "why": "y"}]}` → `"stalled: no\nlooped: yes\nloop ignored: 2\nNone | 3\n{'a': [1]} | y"`
  - **I8** T10 `{"stalled": False, "looped": True, "loop_ignored": [{"where": "w\ud800", "why": "\u00fc"}]}` → `"stalled: no\nlooped: yes\nloop ignored: 1\nw\ud800 | \u00fc"`
  - **I9** T11 `{"stalled": False, "looped": True, "loop_ignored": [{"where": "w%d" % i, "why": "y"} for i in range(1000)]}` → 1003 lines, the third `"loop ignored: 1000"`, the last `"w999 | y"`
  - **I10** T12 `{"stalled": 1, "looped": True}` → `"stalled: unknown\nlooped: yes"`
  - The existing T1/T2/T3 assertions stay as they are (they are the old-archive form, TEMPORAL 1).
- `test_a_story_that_looped_is_laid_out_like_a_stalled_one`: **I6** add `{"task": "T5", "stalled": "x", "looped": False}` and
  `{"task": "T6", "stalled": False, "looped": 0}`; both laid out; the expected counts become `"ELEMENTS in=4"` / `"stall=4 "`. An intended
  behaviour change of this node (TESTING.md "Когда тест покраснел" 1).
- `real_archive(tmp_path, driver_state=None)`: when given, write `driver_state` to `story / "state" / "driver-state.json"`.
  **J1** in `test_the_real_pack_archive_is_read_and_the_schema_pin_holds`: a second archive
  `real_archive(tmp_path / "loops", driver_state={"window_rounds": {"S5|c1": [{"outcome": "cap"}]}})`; its manifest story `TP1-12345` has
  `loop_ignored == [{"where": "driver-state.json window_rounds S5|c1 cap", "why": "no usable time, so never a signal"}]` and
  `isinstance(story["ignored"], list)`; its `stall_elements` text contains `"loop ignored: 1"`. The project is onboarded (config present,
  `collect_pack.py:488`); the story has no activity time, so `collect_stall.py:485-489` makes it stalled-unknown and `looped` None (a stall
  reason), so it is laid out. The pack itself passing proves the new strings went through `_manifest_bytes` and `_verify` (C24).
  Builder check: if the text is missing because the story is not laid out, report the item's `stalled`/`looped` and keep the manifest assertion.

**Mechanical layer D3 (A2; report attachment, never committed)**, the same two-process form as N2's script: call old and new
`collect_pack.Packer._stall(stub, Path(<tmp>) / "T1", item, None, 24)` with `collect_stall.stall` patched to return the grid verdict
plus `"loop_unreadable_reasons": ["r"]`, `stub = SimpleNamespace(project=..., now=datetime.datetime(2026, 11, 13, tzinfo=datetime.timezone.utc), loops=None, gap=lambda s, what, why: gaps.append(what), _pack_transcripts=lambda *a: calls.append(1))`
and `item` a fresh `_stories`-shaped dict; grid as D2. Compare the captured gaps and whether `_pack_transcripts` was called. Acceptance:
identical on every row with `stalled` ∈ {True, False} (identity) and `looped` ∈ {True, False, None}; every delta printed. Negative control:
the new condition with `stall != YES` dropped must show a delta on `stalled=True, looped=None`.

**DoD**
- I1-I10 and J1 pass; every other test of the file passes; D3 passes and its negative control fails as it should.
- AR-13 check: grep `\["looped"\]|get\("looped"|get\("stalled"\)` in `collect_stall.py`, `collect_pack.py`, `tools/collect_intake.py` finds
  only the three allowed hits of §1 (`loop_state`'s body, `collect_pack.py` `item["stalled"] = ...`, `item["looped"] = ...`).
- AR-22 check: J1 is a real producer → real reader join.
- Witness: `python -m pytest C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n4\tools\test_collect_intake.py -q` (the test file that
  judges the two forge paths; `tools/collect_intake.py` has no `scenario_walk` row, rule 4) and
  `python -B C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n4\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/collect_pack.py`, then the shared rule.
- Commit lines: `architecture: AR-13, AR-21, AR-22, AR-23 -- the ignored lists travel whole and have a reader; one reading of the pair at all four sites`;
  `judgment: none -- data carried and rendered`.

siblings: `item["stall_signals"]` / `["loop_signals"]` (same copy form); the intake's `clean()` (§7).

---

## §4 Order, parallelism, writers

| Node | Depends on | Runs with | Files (functions) |
|---|---|---|---|
| N1 CL4-1a | — | N2, N3 | `driver_machine.py` (`window_round_gate`); `collect-loops.json`; `driver-journal-kinds.json`; `collect_stall.py` (docstring ¶L); tests `test_story_run_loop_b_loop.py` (`s5_window_rounds_are_capped`), `test_probe_gap_door.py` (`refusal_rig`), `test_task_price.py` (tuple :1064) |
| N2 CL4-1b | — | N1, N3 | `collect_stall.py` (functions listed); `collect_pack.py` (`_pack_transcripts`, `_STATE_WORDS`) |
| N3 CL4-1c | — (merges after N1 and N4 accepted) | N1, N2, N4 | `kb/04-onboarding-doctor.xhtml`; `SKILL.md`; `changelog.d/collect-4-cl4-1.md` |
| N4 CL4-1d | N2 merged into its tree | N1, N3 | `collect_pack.py` (`_stories`, `_stall`); `tools/collect_intake.py` (2 functions + 1 import); `tools/test_collect_intake.py` (4 functions) |
| (outside) FV1-22 N3 | **CL4-1 N1 merged** (same function `window_round_gate`) | — | — |

At most 3 writing workers at once. One critic pass for the topic after N1, N2 and N4 converge (R13-g). The critic-on-plan has run
(verdict fit_with_fixes); per its "Who applies", no second plan pass is owed for these fixes.

**Lead action before `take` (A8, not a node: the batch is not frozen).** In `plans/piles/collect/batch-4-cl3-9-ochered.md`:
- line 25, cell «Пишет в» → `scripts/driver_machine.py (window_round_gate)`, `references/collect-loops.json`, `references/driver-journal-kinds.json`,
  `scripts/collect_stall.py`, `scripts/collect_pack.py`, `tools/collect_intake.py`, `kb/04-onboarding-doctor.xhtml`, `skills/qa-collect/SKILL.md`,
  `changelog.d/collect-4-cl4-1.md`, тесты: `scripts/tests/test_story_run_loop_b_loop.py`, `scripts/tests/test_probe_gap_door.py`,
  `scripts/tests/test_task_price.py`, `tools/test_collect_intake.py` (drop `scripts/story_run.py` and `scripts/collect_intake.py`);
- line 10 «Порядок по общим файлам» → `scripts/driver_machine.py` — непересекающиеся функции с FV1-6 (D-0048); с FV1-22 N3 —
  `очередь: CL4-1 → FV1-22` (одна функция `window_round_gate`).
This lets `piles.py check` (б) see the overlaps, which D-0048's function lists and the queue line then clear.

---

## §5 Forks — decided by the critic's fork table (technical: the Lead's), one owner question open

| Id | Fork | Decision | Why |
|---|---|---|---|
| F-1 | The row's outcome words | **(a)** the series' own `to_conductor / same_set / cap` | one record, one vocabulary (AR-13, P31); `continue` does not exist (`driver_machine.py:361`, `:405`) |
| F-2 | What "one mapping" means | **(A)** one classifier, each site keeps its own sentences, **with B2**: UNKNOWN-stall keys say "not known" | P31; the quarantined pins keep their bytes for every real verdict |
| F-3 | Which ignored lists travel | **(a)** both | no new content class (§2.4, C24); it adds fields to what leaves a project within the class the owner already sees. **Owner notice** («решила сама», data leaving projects) |
| F-4 | Proving the refactors | **(a)** one-off differentials D1-D3, never committed | TESTING.md bans "like before" tests; (b) would be the owner's (against builder-rules 7b) |
| F-5 | The H gate on `loop_state` | **(a)** yes, error direction toward packing | P31; the delta is hand-made verdicts packing |
| F-6 | `SKILL.md:4` | **(a)** fixed in N3 | the text twin of KB `:408` |
| F-7 | Older-driver stories | **(a)** no rows = no signal; the blind spot named in the docstring and the release note (A9 option "the docstring is the carrier", plus the fragment) | a per-collect gap line has no condition it could test (the first version with the row is not known when the row is written) and would be a false statement on every later collect; (b) would pack every older story's transcripts (the owner's call; not chosen) |
| F-8 | Where test rows go | **(a)** existing functions, trimmed per A10 (W1 join, W4, W5, P1; I1-I10, J1) | TESTING.md forbids a new file and per-key receipts |
| F-9 (new) | `process` in `no_call_kinds` (B1 sweep) | **fold into N1** | same artifact, same test tuple; a money defect already on main. **Owner notice** the same turn (P18, money) |

**Owner notices (the Lead tells the owner; nothing waits):** (1) F-3 — two more lists of `where` strings leave each project; (2) M1
widens which stories' transcripts leave a project (covered by the owner's word 30.10, C25); (3) F-9 — every driver story with a
`process` row prices `incomplete` on main today; N1 fixes it.

**Question to the owner (non-blocking):**
- **Q-1**: where are the real collector archives (the intake inbox, `QA_COLLECT_INBOX`)? With one manifest, R6/R7 become measured.
  Without it, N2's R6 check measures a real story folder and N4's J1 a real pack; no node waits.

## §5a Small choices closed by the designer (no design weight)

- The journal row reuses id `L2` (precedent: L4 on two carriers, `collect-loops.json:13-14`).
- `round` = the record's 1-based position in its series after the append; `findings` = a count, not the set.
- `journal_run`'s `OSError` is not caught (as the sibling).
- Helper names `_l_rows`, `_l_state`, `_l_series`, `_l_records_flat`, `_l_nested`.
- `_WHY` / `_STATE_WORDS` are keyed on the full `loop_state` pair and omit `(NO, NO)` (unreachable behind the gate).
- The unknown-stall words: "whether the story stalled is not known", "the story looped; whether it stalled is not known",
  "whether the story stalled or looped is not known"; "possibly stalled", "looping and possibly stalled", "possibly stalled or looping"
  (FR-6 checked by `human_text.problems` in D2 (iv)).
- The intake labels `ignored:` / `loop ignored:`; the fragment name `collect-4-cl4-1.md`.
- The two `no_call_kinds` `why` texts (N1 step 3).

---

## §6 Axis enumeration (CLAUDE.md rule 10 (b)), every axis of `docs/SIBLING_MAP.md` (36, `:24-606`), per mechanism

Mechanisms: **M1** the `window_round` row with its loop reader and price row (N1); **M2** `loop_state`, one reading of the pair (N2, N4
step 3-5); **M3** the ignored lists travel (N4 steps 1-2, 5).

- axis 1 (policy ↔ roles ↔ journal): M1 n/a, M2 n/a, M3 n/a — no forge policy, role file or forge journal field changes.
- axis 2 (exam instruments): M1 n/a, M2 n/a, M3 n/a — no exam.
- axis 3 (package ↔ release ↔ installed): M1 covered, M2 covered, M3 covered — they ship together in the next release copy with the fragment (N3); no installed-only path.
- axis 4 (rules ↔ debt ↔ backlog ↔ principles): M1 covered (B-6 leftover closed; P18 kept by the price row); M2 covered (FR-41 kept by the B2 words); M3 covered (FR-49); no debt row left.
- axis 5 (stage twins): M1 covered — the twin `gate_repair` (same writer road, L3 reader, a `no_call_kinds` row): `window_round` now has all three; the journal-kind data twin `driver-journal-kinds.json` ↔ `collect-loops.json` changes in one commit; the S5-windows ↔ S6-lanes row: n/a (the cap is S5-only, `driver_dispatch.py:109`; a stage FV1-22 adds writes rows with no further change). M2 n/a (the collector is not a stage). M3 n/a.
- axis 6 (measurement tools ↔ package): M1 queued — `experiments/measurers/report_run.journal` (`:141-158`) counts every non-conductor row as a "role first work" call; `launched`, `gate_repair` and `process` already inflate it, `window_round` adds more (pre-existing; candidate finding, §7); `task_price` (the package-side money reader) covered by the price row. M2 covered — the intake (the forge reader of collected archives) reads through `loop_state` (N4). M3 covered — producer `collect_pack` and forge reader `tools/collect_intake.py` change in N4, joined by J1.
- axis 7 (per-test identity): M1 n/a, M2 n/a, M3 n/a — no test identity scope.
- axis 8 (where the story is on disk): M1 n/a (the row uses the driver's existing `state_dir`), M2 n/a, M3 n/a (`read_facts` unchanged).
- axis 9 ("is this a test file"): M1 n/a, M2 n/a, M3 n/a.
- axis 10 (git-top readers): M1 n/a, M2 n/a, M3 n/a.
- axis 11 (shell-command recognizers): M1 n/a, M2 n/a, M3 n/a.
- axis 12 (work plan carriers): M1 covered, M2 covered, M3 covered — the batch row's write zone is rewritten by the Lead before `take` (§4, A8); node status moves with the journal.
- axis 13 (dispatch text): M1 n/a, M2 n/a, M3 n/a — no text sent to a role changes.
- axis 14 (transcript readers): M1 covered — M1 widens WHICH stories' transcripts are packed (a capped, since-accepted window → `looped: True`), covered by the owner's word (C25) and said in the fragment; the readers (`session_transcripts`, `select_transcripts`' paths) are unchanged. M2 covered — the gate reads through `loop_state`; equal for real verdicts; hand-made non-bool `stalled` now packs (safe side). M3 n/a — the lists carry `where` strings, no transcript.
- axis 15 (console stream): M1 n/a (no new print; the gate's prints unchanged), M2 n/a, M3 n/a.
- axis 16 (one JSON reader): M1 covered for the price row (`hooklib.load_ref_json`, the one reference reader) and queued (existing) for the collector (`collect_stall._jsonl_rows`, a known AR-13 gap; M1 adds no reader). M2 n/a, M3 n/a.
- axis 17 (detector verdict shape): M1 n/a, M2 n/a, M3 n/a — the collector verdict is not a detector verdict.
- axis 18 (in-tree ratchets): M1 covered (`test_driver_layers.py` checked, a raise → a question; no census unit); M2 covered (no census unit); M3 n/a.
- axis 19 (`tools:` line reader): M1 n/a, M2 n/a, M3 n/a — no role file.
- axis 20 (host receipt names): M1 n/a, M2 n/a, M3 n/a.
- axis 21 (markdown table readers): M1 n/a, M2 n/a, M3 n/a — no table cell is read.
- axis 22 (host return form): M1 n/a, M2 n/a, M3 n/a.
- axis 23 (`tests[]` row fields): M1 n/a, M2 n/a, M3 n/a.
- axis 24 (execution join): M1 n/a, M2 n/a, M3 n/a.
- axis 25 (freshness predicates): M1 n/a, M2 n/a, M3 n/a.
- axis 26 (`stand not confirmed`): M1 n/a, M2 n/a, M3 n/a.
- axis 27 (profile of a test row): M1 n/a, M2 n/a, M3 n/a.
- axis 28 (row form render site): M1 n/a, M2 n/a, M3 n/a.
- axis 29 (append-only jsonl writers): M1 covered (`journal_run` → `_append_jsonl`, `test_driver_stop_record.py::story_run_has_no_private_appender`); M2 n/a, M3 n/a (no writer).
- axis 30 (profile commands): M1 n/a, M2 n/a, M3 n/a.
- axis 31 (role carriers): M1 n/a, M2 n/a, M3 n/a — no role text; the skill description twin (KB `:408` ↔ `SKILL.md:4`) changes together in N3.
- axis 32 (where judgment lives): M1 covered, M2 covered, M3 covered — §1 census table, no unit added.
- axis 33 (which dispatch): M1 n/a (`dispatch` is copied from the gate's own `refusal_dispatch`), M2 n/a, M3 n/a.
- axis 34 (one road): M1 covered (one outcome vocabulary; a stage-agnostic reader; the price row the same road as `gate_repair`); M2 covered (one classifier at all four pair sites, C23 included); M3 covered (both halves' lists, one copy form, one render helper).
- axis 35 (sides of a story): M1 n/a, M2 n/a, M3 n/a.
- axis 36 (row against a substitute): M1 n/a, M2 n/a, M3 n/a.

Four questions (rule 10): (a) cost: one row per window round and per stop (N1); one classifier call per site; payers are the driver and
the collector; no role cost; two more lists in each story item. (b) above. (c) detectors: W1, W4, W5, P1 (keep files), I1-I10, J1
(forge test), the census test, `quarantine-watch` for the quarantined pins, calibration check 41 (judgment). (d) on the path:
`journal_run` sits in the gate's block (code); `load_loops` validates the data row on every collect; `_no_call_kinds` reads the kinds
on every price; `loop_state` is called by the gate itself.

## §7 Noticed, not widened (analogs and contradictions)

- The finding's stale facts: `_l_records` lines (C1); the writer is `driver_machine.py`, not `story_run.py` (C12); the `continue`
  outcome (C13); site 3 is not a pair mapping (C8); `loop_ignored` never reaches the manifest (C10); its tests are quarantined or
  misnamed (T1, T4).
- R2: the window-cap **question row** in `driver-questions.jsonl` carries no `why`; M1 makes the journal row the durable carrier, so the
  collector does not need it. Candidate finding (pile `driver-controller`), queued for the Lead.
- `collect_intake.stall_elements` renders `where` strings from an untrusted manifest without `clean()`; the class predates this node;
  candidate finding (pile `collect`) if N4's builder confirms it.
- **Axis 6**: `experiments/measurers/report_run.journal` (`report_run.py:141-158`) counts every non-conductor journal row as a "role first
  work" call (no kind filter): `launched`, `gate_repair`, `process` and now `window_round` inflate it. Pre-existing; candidate finding
  (pile of the measurers), queued for the Lead.
- `driver_journal.py:453-455` claims every pricing reader passes `process` rows by; it was false until N1 (C22). N1 makes it true; the
  comment stays.
- The batch file's write zone and order line are stale (A8): the Lead's action in §4.
- D-0052 "transcripts only of stalled" amended by the owner on 30.10 (C25): the DECISIONS.md edit is queued for the Lead, as that finding says.

## §8 Reading trail

First draft: see its trail (root checkout): `plans/piles/collect/batch-4-cl3-9-ochered.md`; the CL4-1 finding; `plans/piles/collect/README.md`;
the release-next 30.10 findings; `collect_stall.py`, `collect-loops.json`, `collect_pack.py`, `tools/collect_intake.py`,
`tools/test_collect_intake.py`, `driver_machine.py`, `driver_runner.py`, `driver_gates.py`, `driver_timing.py`, `driver_journal.py`,
the named tests, `scenario_walk.py:833-932`, `test-layers.json`, `slow_tests.json`, `judgment-census.json`, `docs/TESTING.md`,
`plans/builder-rules.md`, `docs/SIBLING_MAP.md`, KB and SKILL.md, `changelog.d/README.md`, the real fixtures.

Fix round, all on `C:\QAFactory\forge-repo\.claude\worktrees\read-main` (e4ba384) unless named:
- Read whole: the spec; the verdict `docs/tasks/specs/reviews/20261113-cl4-1-plan-critic.md`; `references/driver-journal-kinds.json`;
  `references/collect-loops.json`; `plans/piles/collect/batch-4-cl3-9-ochered.md`.
- Read in part: `driver_machine.py:300-424`, `:1774-1781`; `driver_runner.py:404-421`; `driver_journal.py:445-462`, `:550-589`;
  `task_price.py:540-599`; `tests/test_task_price.py:1010-1074`; `tests/test_story_run_loop_b_loop.py:495-654`;
  `tests/test_probe_gap_door.py:268-297`; `collect_stall.py:50-81`, `:150-169`, `:240-329`, `:373-452`, `:480-539`;
  `collect_pack.py:1055-1139`, `:1359-1400`; `tools/collect_intake.py:575-592`, `:655-684`; `tools/test_collect_intake.py:20-99`,
  `:266-300`, `:605-641`; `test-layers.json:1408-1421`, `:3778-3789`, `:5787-5798`, `:6333-6344`; `scenario_walk.py:887-936`;
  `docs/SIBLING_MAP.md:111-181`; `kb/04-onboarding-doctor.xhtml:406-418`; `skills/qa-collect/SKILL.md:1-6`;
  `experiments/measurers/report_run.py:140-159`; root `docs/tasks/specs/20261113-fv1-22-s7-acceptance-loop-spec.md:290-319`.
- Searches (Grep tool, each with a positive control of the same form):
  - `\["looped"\]|get\("looped"|get\("stalled"\)|\["stalled"\]` over read-main `scripts/*.py` → `collect_stall.py:499`, `:530-532`;
    `collect_pack.py:1112`, `:1113`, `:1116`, `:1130`; tests (quarantined) — the known sites C5-C7 are among the hits (control).
  - the same plus `stall_laid_out|def stall_elements` in `tools/collect_intake.py` → `:662`, `:665`, `:668`, `:671`, `:674`, `:677`, `:798`.
  - `^import|^from|collect_pack|collect_stall|sys.path` in `tools/collect_intake.py` → `import collect_pack` at `:58`, path insert `:57`; no `collect_stall` import yet.
  - `no_call_kinds|driver-journal-kinds` over the package → `driver-journal-kinds.json:2`, `task_price.py:551-573`, `test_task_price.py:1017-1061`, `changelog.d/fv1-21.md:2` (control: the json file itself is found).
  - `WINDOW_ROUND_CAP =|WINDOW_ROUND_STAGES =` → `driver_machine.py:45`, `driver_dispatch.py:109`.
  - `test_task_price.py|test_driver_stop_record.py|...|"quarantine"|test_collect_pack.py|test_collect_stall.py` in `test-layers.json` → `:1410`, `:3780`, `:3870`, `:5789`, `:6333`, `:7126`, `:7559`, `:7576`.
  - `test_driver_layers|driver-layers` in `test-layers.json` → `:28`, `:1386`, `:1406` (the Glob tool on `.claude/worktrees/read-main` returned nothing for `test_driver_layers.py` AND for the known `test_task_price.py`: a miscall, so the Grep form was used; no absence is claimed).
  - `"test_no_move_seam_k4s.py"|"test_silent_passes.py"` in `test-layers.json` → `:3245`, `:5203`; `slow_tests.json` → `:68` (32.6), `:136` (58.4).
  - `task_price|collect_stall|collect_pack|collect_intake` in `judgment-census.json` → `:99` (`collect_pack.py::refuse`), `:101` (`collect_stall.py::judge`); no `task_price` unit (the same search finds the collect rows: control).
  - `^## Axis` in both SIBLING_MAPs (root and read-main) → the same 36 headings, `:24-606`.
  - `window_round_gate|window_rounds|driver_machine` in the FV1-22 spec → N3 owns `window_round_gate` (`:296-300`, `:315`).
  - `self\.onboarded\s*=` in `collect_pack.py` → `:488` (`cfg_state != "absent"`).
  - `kind|driver-runs|_journal_paths|read_rows` in `run_counters.py` → counts by kind (`NO_KIND`, `:41`), process rows `:108`.
  - `брать` in the release-next 30.10 finding → `:11` (the critic cited `:9`; corrected).
- Not run: this role has no shell. `scenario_walk.py --witness-for` prints are each builder's first output; the `_no_call_kinds()`
  membership rests on the critic's run plus reading the JSON (N1 builder check (c) re-runs it); D1-D3 do not exist yet.

---

## Fix round (critic-on-plan verdict, 13.11.2026)

Verdict: `docs/tasks/specs/reviews/20261113-cl4-1-plan-critic.md` (fit_with_fixes). Every item applied; none returned as a fork.

| Item | What changed | Where |
|---|---|---|
| **B1** money: a `window_round` row priced `incomplete` | `window_round` and (sweep) `process` appended to `no_call_kinds` with `why`; `driver-journal-kinds.json` and the `test_task_price.py:1064` tuple added to **N1** owns (producer and price row in one commit, AR-22/P18); defect row P1; builder check (a) gains `task_price`, `run_counters` and "fix the money reader here by the data row; report the rest"; check (c) added; facts C21, C22; AR-1 row and P18 line in §1; census row; axis 5/16 lines; edges for the price (fallback, session id, unknown kind) with the error direction of the reused `_rows_without_session` | §0.1 C21-C22; §1; §2.1; N1 owns, steps 3 and 6, edges, test rows, DoD; §5 F-9; §6 axes 5, 6, 16 |
| **B2** FR-41: an unknown stall worded "stalled"; D2 self-contradicting | `_WHY` and `_STATE_WORDS` keyed on the full `loop_state` pair, with UNKNOWN-stall words that say "not known" / "possibly stalled"; D2 acceptance restated as (i)-(iv) (identity on `stalled`, gate deltas False→True only, word deltas only on non-bool `stalled`, `human_text.problems` = []); edge row rewritten; N2 FR pass gains B | N2 steps 3-4, edges, mechanical layer, handoff; §5a |
| A1 how to get the OLD pack word | two processes (scratch copies first on `sys.path` vs the worktree), each printing its module `__file__`; the old and the new `Packer._pack_transcripts` called on a stub `self` with `session_transcripts` patched to `[]` | N2 mechanical layer |
| A2 fourth pair site `collect_pack.py:1116` | routed through `loop_state` in N4 (`loop == UNKNOWN and stall != YES`), D3 differential; AR-13 grep widened to `\["looped"\]\|get\("looped"\|get\("stalled"\)` with the three allowed hits | C23; §1 AR-13; N4 step 3, edges, D3, DoD |
| A3 `_l_state` missing from owns | added; "six functions" in the DoD | N2 owns, DoD |
| A4 third temporal row | TEMPORAL 3: a re-collected older story with non-empty lists changes `csha` once; expected, no action | N4 edges |
| A5 N3 merge order; fragment clauses | N3 merges after N1 and N4 are accepted; the Lead edits the fragment if needed; fragment says capped-window stories now send transcripts, names the older-driver gap and the price fix; B-id appended by the Lead | §3 header, N3 order, step 4, DoD keys; §4 |
| A6 name what leaves a project | §2.1 (M1 widens the transcript set, C25), §2.4 (`where` strings of existing f-strings only), C24 (redaction answered by reading `_manifest_bytes` / `_verify`; J1 runs through them), axis 14 | §0.1 C24-C25; §2; N4 edges, J1; §6 axis 14 |
| A7 axis block form | one line per axis, every line names M1, M2 and M3; axis 6 M1 queued (`report_run.journal`); axis 14 corrected; journal-kinds twin in axis 5 | §6 |
| A8 stale batch zone | the Lead's action before `take`, with the exact cell text and the order line (outside this file's scope) | §4 |
| A9 docstring text and the blind spot | "L1/L5" kept (not L1/L5/L7); "cannot be told" replaced by "the version that first writes the row is not known when the row is written"; the docstring and the release note declared the carriers (the gap-line option rejected: no testable condition) | N1 step 4, edges; §5 F-7; N3 fragment |
| A10 trim per-edge receipts; non-string row | W1-W3 folded into one join check W1 (journal vs series), W6 and W7 dropped; W4, W5, P1 kept; intake rows I7 (non-string), I8 (encoding), I9 (magnitude), I10 (`stalled: 1`) added | N1 test rows; N4 test rows, battery |
| A11 line numbers on e4ba384; one insertion | every `driver_machine.py`, `driver_runner.py`, `test-layers.json`, `slow_tests.json` line restated; the round row sits after `:406`, before `:407-408`, covering both causes | §0 C12-C16, C19, T1-T4, T8; N1 given, step 1, edges |
| Brief: owns against the builders' worktrees | every `owns:` path is under `C:\QAFactory\forge-repo\.claude\worktrees\cl4-1-n<k>\`; witness commands use the worktree's scripts | §3 |
| Brief: crossings | FV1-6 disjoint by function; FV1-22 N3 sequential after CL4-1 N1 (same function), FV1-22 N2's constant needs no order | §3 header, §4 |
| Brief: forks | F-1..F-8 decided by the critic's table; F-9 new and decided; owner notices (F-3, M1 transcripts, F-9 money) listed; Q-1 the only open item (owner, non-blocking) | §5 |

Forks returned: **none open**. Owner question: Q-1 (non-blocking). Owner notices for the Lead to pass on: F-3, M1's transcript set, F-9.
