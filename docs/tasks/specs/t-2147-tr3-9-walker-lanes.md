# t-2147 — TR3-9 (t-1957 N5p) revised: S6 walker lanes on the window scheduler — DRAFT SPEC (designer)

Status: draft for Lead acceptance. Replaces t-1957 `#### N5p` (lines 992-1019) and amends its lines 205-208 and 932-934 (list in §6).
Worktree: `D:/ws1/wt-fbfix` (branch fb-fix = experiment/thinking-roles). `S` = `D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts`.
All file:line below were read by the designer in this worktree on 10.11.2026 unless marked "builder's first read".

## 0. What exists (measured) and what the old text got wrong

- The scheduler is NOT `S5Scheduler` and the lock is NOT an RLock. It is a set of `Driver` members in `story_run.py`, on the plain
  `class Driver:` (`story_run.py:1180`, no base class):
  - module level: `_CHAIN = threading.local()` :372, `once_on` :375, `ThreadSlot` :386, `ChainRecord` (dataclass: `n, boundary,
    last_dispatch, cases, exception, proc, running, done`) :411, `WindowsUnreadable(ValueError)` :429, `Drained(Exception)` :434,
    `ChainStream` :439;
  - members: `_slots` :1185, `boundary`/`last_dispatch` (ThreadSlot class attributes) :1188-1189, `as_chain` :1192, `adopt_chain` :1212;
    `GATE_POLL_S` :11558, `WAIT_POLL_S` :11559; properties `_book` (a plain `threading.Lock` via `once_on`) :11562,
    `_settling` :11567, `_cond` (Condition over `_book`) :11572, `_drain` :11576, `_interrupted` :11580; `stop_if_interrupted` :11585,
    `_chains` (registry dict) :11591, `on_chain` :11595, `unbooked` :11600, `stop_if_drained` :11622, `count_launch` :11627;
    launch gate `s5_window_files` :11635, `files_overlap_running` :11657, `session_gate` :11668, `session_running` :11685;
    `run_chains(items, launchable, chain_fn, cap)` :11929-11999 (ends by calling `self.s5_seam(...)` :11999), `_interrupt_chains` :12001,
    `_chain_thread` :12012, `s5_seam` :12028-12052 (rank closure :12035-12039, limit branch :12046-12050), `s5_launchable` :12054,
    `s5_window_chain` :12061, `run_s5_windows` :12080, `stage_S5` :12099.
- Its S5-specific texts (the three lines tests match): `"S5: the session of window {n} waits for window ..., which is working on a file of
  it"` :11680; `"S5: waiting for window ... to finish its running session before <Type> goes on"` :11986; `"S5: window {n} also ended with
  <Type>: ..."` :12044. Tests match them: `test_story_run_s5_parallel.py:358` ("also ended with Person"), `:553` ("waits for window"),
  `test_driver_chain.py:742, :751` ("S5: window 1 also ended"), `:847` ("waiting for window 1").
- The layer map `S\tests\fixtures\driver-layers.json` homes these names across FOUR planned layers (rows :871-:924): `_CHAIN`,
  `Driver.boundary` -> driver_core; `once_on`, `_book`, `_settling`, `_cond`, `_interrupted`, `stop_if_interrupted`, `_chains`, `on_chain`,
  `unbooked`, `s5_window_files`, `files_overlap_running`, `session_gate`, `session_running`, `GATE_POLL_S` -> driver_runner; `Drained`,
  `WindowsUnreadable`, `last_dispatch`, `_drain`, `stop_if_drained`, `count_launch` -> driver_dispatch; `ChainRecord`, `ChainStream`,
  `_slots`, `as_chain`, `adopt_chain`, `WAIT_POLL_S`, `say_once`, `run_chains`, `_interrupt_chains`, `_chain_thread`, `s5_seam`,
  `s5_launchable` -> driver_stages; `ThreadSlot` -> story_run. `layers` (:3): `[["driver_core"], ["driver_runner", "driver_timing"],
  ["driver_dialog"], ["driver_conductor"], ["driver_dispatch"], ["driver_s0", "driver_sources"], ["driver_stages"], ["driver_gates"],
  ["driver_machine"], ["story_run"]]`. Of these only `driver_timing.py` exists as a file (`driver_journal` is `not_driver`, :4).
- The layer test's rules that decide the extraction (`S\tests\test_driver_layers.py`): the driver set is `story_run.py` + every
  `scripts/driver_*.py` (:62-72), so the new module MUST be named `driver_<x>.py` and its class `Driver<Suffix>` (:33, :97: members of a
  `Driver*` class are censused as `Driver.<member>`); L2 (:347-357): a name whose home module EXISTS must be defined there, a name whose
  home does not exist must stay in `story_run.py`; L5/L7 (:517-540): a call/name/attribute edge to a higher layer fails; the
  `exceptions` list is pinned and shrink-only (:43-58, :546-551) — an upward edge can never be legalised; L6 (:553-566): no import of a
  higher-layer module (so `driver_chains.py` can never import `story_run`).
- Upward-edge facts that fix the module's rank: `Refusal.__init__` reads `_CHAIN` (`story_run.py:527`; `Refusal` home driver_core, map
  :49); `_launch` (runner) reads `_CHAIN` (:2057) and the launcher calls `unbooked`, `session_running`, `stop_if_interrupted` (critic
  t-2125 trail: `_launch` :2028-2068). So anything that moves must sit at rank 0 (driver_core's rank) or these edges become upward.
- Domain exceptions the seam ranks: `Refusal(Exception)` :488, `ReworkRefused(Refusal)` :547, `Person(Exception)` :580, `Stop(Exception)`
  :624, `InfraStop(Stop)` :644 — all home driver_core (map :49-57), all in `story_run.py`; a rank-0 module cannot import them (L6 + cycle).
- Tests that call the scheduler directly (`test_driver_chain.py`): `d.run_chains(items, launchable, chain_fn, cap)` positional, 4 args
  (:469); `d.s5_seam(records, cap)` (:440, :737, :748); `d.s5_window_files = lambda ...` overrides (:497, :509, :514);
  `launchable=d.s5_launchable` (:505); `d.session_running("D2")` called OUTSIDE any `run_chains`, records put into `d._chains` by hand
  (:513-533); `SR.ChainRecord`, `SR._CHAIN.record` (:714), `SR.Person`, `SR.InfraStop`. `test_story_run_s5_parallel.py:185` overrides
  `driver.s5_window_files`, `:310` overrides `driver.run_chains`.
- S6 today: `stage_S6` :12963 calls `run_manual_block(manual_scope)` :13072; `run_manual_block` :13768-13868 runs ONE lane per driver
  entry: `manual_plan` -> `stand_login_gate` -> lanes re-cut by `walk_lanes(..., lane_keys(...), MANUAL_BLOCK_MAX)` :13791 ->
  `walk_refuse_gaps` -> `block = plan["blocks"][0]` :13800 -> `complete` only for the last block :13801 -> in-process
  `Controller.prepare` / `apply("dispatch")` with `execution_kind: manual` :13823-13830 (id `S6-qa-runner-<n>` :13816) ->
  `walk_before(block, dispatch_id)` :13841 (`run-report.json` via `finalize_task.py`, `app_card.py build`, `walk_session.py open`,
  writes `self.state["walk_old_road"]`, :3609-3656) -> `record_running` -> `run_role(..., complete=run_complete, ...)` :13866.
  `walk_after` :3812. Lane key = the lane's account set (`lane_keys`; `walk_actors` :3658).
- Controller: op `dispatch` refuses any second running dispatch unless `_window_beside_running` admits it (`controller.py:5150-5162`);
  `_window_beside_running` :5958-5998 admits only S5 window dispatches with `parallel_window is True`, disjoint non-empty scopes (also
  against `returned_unaccepted` S5 siblings), count within `_parallel_cap` :5946-5956; `_resume_problems` uses it with `flagged=False`
  :6016. The flag comes from `--parallel-window` (:9249, :9349) into the request (:3670-3671). The S6 in-process dispatch passes no flag.
- Probe files (Lead decision 2): `probe_debt._item_files(item, row)` (`probe_debt.py:876-888`) = the test file of the item's manifest
  row plus the file of `--oracle f::fn` from `item["_args"]`. The gate's reader `s5_window_files` (:11635-11655) takes claims + manifest
  `tests[].file` + `generated_from`, not the oracle file (critic t-2121 Q6).
- `manual.walkers`: not in the package. Grep `walkers|parallel_windows` over `ai-packages/qa-factory` lists 30 files (positive control:
  `config_contract.py`, `config-keys.json`, `templates/config.json` are among them for `parallel_windows`); whether any of them carries a
  `manual.walkers` key is the builder's first read of those three files (designer read only the file list — see trail).
- No frozen S6 set exists: Glob `S\tests\fixtures\s5-n1-frozen` family exists for S5 only (`test_story_run_s5_n1_frozen.py`); no
  `test_walk_lanes_parallel.py` (Glob over the tests dir with the same pattern found `test_walk_lanes.py` — positive control).

## 1. Scope, AR-n touched, owners and census (designer rule 1; host adaptations 9, 10)

Touches `ai-packages/qa-factory/`. Each AR's change check is written into the DoD of the part named.

| AR | how touched | change check (in the part's DoD) | part |
|---|---|---|---|
| AR-3 config default | `manual.walkers` int >= 1, default 3 | one commit: template, `config-keys.json` row, `config_contract.walkers` reader with default + note, interview topic line; `test_config_migration.py` | D |
| AR-13 one reader | "which files may a chain mutate" (gate file set) read through `s5_window_files` only; the walkers value read through `config_contract.walkers` only (driver AND controller) | grep for a second hand-read with a positive control; report line | B, D |
| AR-14 one writer | story-wide files touched by parallel lanes (`run-report.json`, `app-card`, `created-accounts.json`, driver state) | each writes under `_book` (chain code steps), by its own lock, or is an atomic idempotent reducer (role-invoked `finalize_task`, C.5); the report names each writer with its lock or this reason | C |
| AR-15 one survivor | ONE scheduler for S5 and S6 (`driver_chains.py`); no second gate, no second seam | the S6 road calls `run_chains`; grep `threading.Thread(` in `story_run.py` finds no new site | A, C |
| AR-17 one seam | a refusal in one lane | one seam per turn on the main thread after the drain (the module's `run_chains`); `Driver.no_move` unchanged | A, C |
| AR-19 stage twins | S6 lanes = twin of S5 windows (SIBLING_MAP axis 5, axis 33) | each S5 piece named with its S6 twin or "not applicable — why" (table §4); Lead writes the map rows | C |
| AR-20 ratchets | census, `NO_MOVE_BASELINE`, layer `exceptions` | `exceptions` never grows (pinned); every census change named key, old -> new, reason | A-D |
| AR-22 producer/reader | new field `walk_lane` on the S6 dispatch request; `ChainKind` | each new field names its reader in the commit; proved by the pair `test_s6_lane_admission.py::two_lanes_disjoint_distinct_accounts_admitted` (reader) and `test_walk_lanes_parallel.py::request_carries_walk_lane_and_actor` (producer) | C, D |
| AR-25 way out | a lane drained mid-S6; claims none | `state-exits.md` row for "S6 dispatch running after a drain" (exit: the existing re-entry road) | C |
| AR-28 unknown never a pass | the S6 close with lanes open; unreadable lane state | close predicate raises on unreadable, caller treats as open | C |
| AR-29 judgment | checks below | each named with owner + class | A-D |

Checks added or altered (AR-29): none judges a role's content.

| check | where | owner | census class | part |
|---|---|---|---|---|
| launch gate: a chain's session does not start while a running chain holds a resource of it | `driver_chains.session_gate` (moved; generic through `ChainKind.holds`) | data (code) | xref (unchanged unit, moved) | A |
| start gate: a chain does not start while a live (not done) chain holds a resource of it | `driver_chains.chain_launchable` (new, generic; t-2152 B3) | data (code) | xref | A |
| S5 gate file set takes the files a replay of a recorded probe mutates (`probe_debt.record_files`) | `story_run.s5_window_files`, `probe_debt.record_files` | data (code) | xref (altered) | B |
| S6 lane holds = its cases + its account key | `story_run.s6_lane_holds` (new) | data (code) | xref | C |
| S6 close predicate `s6_open_lanes` | `story_run` (new) | data (code) | xref | C |
| S6 serial reason `s6_serial_reason` (tells, never stops) | `story_run` (new) | data (code) | shape | C |
| controller: S6 manual dispatch beside running S6 manual dispatches: flag, disjoint scopes, distinct lane accounts, count <= walkers | `controller._lane_beside_running` (new, beside `_window_beside_running`) | data (code) | xref | D |
| walkers value: not an int >= 1 -> default + note, never a stop | `config_contract.walkers` | data (code) | shape | D |
| controller: stage entry of an S6 manual lane stays `running` beside a running S6 manual sibling | `controller.stage_entry_beside_running` (S6 added; t-2152 B5) | data (code) | xref | D |

Axis 29: n/a, no new appender; existing appenders named: `driver-timings.jsonl` through `hooklib.append_jsonl_line` (:2100-2105), `app-card-notes.jsonl` under its lock, walk `timing.jsonl` through the atomic publisher.

Non-goals of TR3-9 (all parts): the accounts/data way and per-walker isolation of entities (`walk_pool`, `manual.accounts_way`,
`manual.data_way`, `walk_data`/`walk_global`, the holds-no-case question) — TR3-10 (N8); the lease (TR3-7, done); S5 behaviour other than
part B; S7 controls (Slice 3); gateway/host settings (P25); critic t-2121 Q1-Q5, Q7 (TR4-10/TR4-11).

## 2. Parts and order

Order (Lead, after critic t-2152): A ∥ D, then B, then C0, C1, C2. Part C is split: C0 = capture of the frozen set (its own commit, BEFORE any change of the S6 road), C1 = lanes, C2 = identity sites; C1 and C2 own disjoint files. One critic pass for the topic "driver scheduler" over the merged diff (cost gate R13-g; A and C1 are core and over 100 lines: critic mandatory). Estimates: A ≈ 2-3 h, B ≈ 1-1.5 h, D ≈ 2.5 h; C whole was over 3 h (critic t-2152), hence the split (estimate, not verified).

Common to every part: `given:` `ai-packages/qa-factory/design/factory-rules.md` (whole), `plans/builder-rules.md` (7b), this file,
`docs/tasks/specs/t-1937-s5-parallel-windows.md` §3.2-3.7, `docs/tasks/handoffs/20261110-lead-window-acceptance.md` §3,
`docs/tasks/specs/reviews/t-2121-critic-tr3-6.md`, `docs/tasks/specs/reviews/t-2125-rereview-tr3-6.md`. Slow files
(`test_story_run_*`) are NOT run locally (PROJECT.md «Как принимается», builder-rules 7b): the builder pushes and reads the CI lines
once per round (`docs/RUNBOOK.md` §7), one wait cap.

---

### Part A (TR3-9a) — `driver_chains.py`: the generic scheduler leaves `story_run.py`, no behaviour change (Lead decision 1)

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\driver_chains.py` (new: module names `_CHAIN`, `once_on`, `ThreadSlot`, `ChainRecord`, `Drained`, `ChainStream`, `ChainKind`; class `DriverChains` with `_slots`, `as_chain`, `adopt_chain`, `GATE_POLL_S`, `WAIT_POLL_S`, `_book`, `_settling`, `_cond`, `_drain`, `_interrupted`, `stop_if_interrupted`, `_chains`, `on_chain`, `unbooked`, `stop_if_drained`, `count_launch`, `chain_overlap_running` (was `files_overlap_running`), `chain_launchable`, `session_gate`, `session_running`, `run_chains`, `_interrupt_chains`, `_chain_thread`, `chain_pick`, `chain_seam`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (delete the moved definitions; one `from driver_chains import ...` line; `class Driver(DriverChains)`; module function `seam_rank` new; `Driver.s5_chain_kind` new; `Driver.s5_seam` body over `chain_pick`; `Driver.run_s5_windows` passes `kind=`/`seam=`; nothing else)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json` (`layers` group 0 becomes `["driver_core", "driver_chains"]`; homes of moved names -> `driver_chains`; rows for new names; `attributes` owners touched by moved code at rank 0)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_chain.py` (ONE rig line in `launch_gate_waits_then_progresses`, see edges A.6; no assertion text changes; new key `scheduler_module_knows_no_stage`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\tr3-9a-driver-chains.md` (new)

**non-goals:** any behaviour change (texts, order, timing, locks); `WindowsUnreadable` and every `s5_*` member stay in `story_run.py`
(S5 data, not scheduling); `boundary`/`last_dispatch` stay as class attributes of `Driver` in `story_run.py` (their homes driver_core /
driver_dispatch do not exist as files, so L2 keeps them there); the probe files (part B); S6.

**Required behaviour (exact):**
1. Move the names listed under `driver_chains.py` VERBATIM (bodies byte-identical) except the generic substitutions below (and the new `ChainRecord.tag` field, item 2).
   `driver_chains.py` imports only the standard library (`contextlib`, `dataclasses`, `sys`, `threading`) — never `story_run`, never a
   package module that imports `story_run`.
2. `ChainKind` (frozen dataclass, module level): `label: str = "chains"` (prefix of the scheduler's own console lines), `noun: str =
   "window"` (what one chain is called), `held: str = "a file"` (what a running session holds, in the gate's line), `holds: object = None` (callable `cases -> set`: the resources a chain's session holds, given the chain's case tuple, the same argument `s5_window_files` takes; None = nothing knowable = no gate), `tag: str = "W"` (the console prefix letter of a chain's lines: `run_chains` sets `ChainRecord.tag` from it and `ChainStream._prefix` writes `[{tag}{n}] `, so S5 stays `[W<n>]` byte-identical, `test_story_run_s5_parallel.py:301` `[W1]` holds, and S6 uses "L"; critic N2, see "Open after t-2152"). No `rank` field: the rank is the seam's business (item 5).
3. `run_chains(self, items, launchable, chain_fn, cap, *, kind=None, seam=None)`: sets `self._chain_kind = kind or ChainKind()` before
   the first thread starts and resets it to None in an OUTER `try/finally` that also wraps the seam call, so the seam still reads the kind of its own run; the three console lines take `kind.label`/`kind.noun`/`kind.held`
   (S5 passes label "S5", noun "window", held "a file", so S5 text is byte-identical); the last line becomes
   `(seam or self.chain_seam)(sorted(registry.values(), key=lambda r: r.n), cap)`.
4. Launch gate generic: `chain_overlap_running(record)` = today's `files_overlap_running` with `self.s5_window_files(x)` replaced by
   `kind.holds(x)` where `kind = getattr(self, "_chain_kind", None)`; no kind or no `holds` -> `[]`. `session_gate` prints
   `f"{kind.label}: the session of {kind.noun} {n} waits for {kind.noun} {..}, which is working on {kind.held} of it"`.
4b. `chain_launchable(record)` (generic twin of `s5_launchable`, :12054-12059): False when `kind.holds` of `record.cases` meets `kind.holds` of any OTHER registered chain that is not `done` (live, not only running); no kind or no holds -> True.
5. `chain_pick(records, kind, rank)` = today's `s5_seam` lines :12031-12045 (the failed list, then `min` by `(rank(exc), n)`, then one line per unchosen exception `f"{kind.label}: {kind.noun} {other.n} also ended with {type(...).__name__}: ..."`). It returns the picked record or None. `chain_seam(records, cap)`: `kind = getattr(self, "_chain_kind", None) or ChainKind()`; `pick = self.chain_pick(records, kind, lambda e: 0)`; None -> return; else `self.adopt_chain(pick); raise pick.exception`.
6. In `story_run.py`: `seam_rank(exc)` module function = the closure at :12035-12039 lifted verbatim (InfraStop 0; Stop or a non-domain
   exception 1; Refusal 2; Person 3). `Driver.s5_chain_kind()` returns `ChainKind("S5", "window", "a file", lambda cases: self.s5_window_files(cases))` (the lambda reads `self.s5_window_files` at call time so a rig's override is seen; the other fields default, `tag` stays "W"). `s5_seam(records, cap)` = `pick = self.chain_pick(records, self.s5_chain_kind(), seam_rank)` (`s5_seam` never depends on `_chain_kind`: a direct call, as the test and the main thread after the drain make, prints `S5: window ...`); None -> return; the limit branch :12046-12050 unchanged; `adopt_chain`; raise.
   `run_s5_windows` calls `self.run_chains(items, self.s5_launchable, self.s5_window_chain, cap, kind=self.s5_chain_kind(),
   seam=self.s5_seam)`. `s5_launchable` stays and keeps reading `s5_window_files` (S5's start gate).
7. Re-export: `from driver_chains import _CHAIN, ChainKind, ChainRecord, ChainStream, Drained, DriverChains, ThreadSlot, once_on` in
   `story_run.py`, so every `SR.<name>` a test or a sibling module reads still resolves (imports are not censused, layer test docstring
   :18-20).
8. Layer map: `driver_chains` joins group 0 (`["driver_core", "driver_chains"]`); every moved name's row gets `"home": "driver_chains"`
   with note `t-2147 A: moved to driver_chains.py (rank 0: Refusal and the launcher read it)`; new rows `ChainKind` (class,
   driver_chains), `Driver.chain_pick`, `Driver.chain_seam`, `Driver.chain_launchable`, `Driver.chain_overlap_running` (methods, driver_chains; the row
   `Driver.files_overlap_running` is deleted), `seam_rank` (func, driver_core), `Driver.s5_chain_kind` (method, driver_stages);
   `attributes`: a row `_chain_kind` (owner driver_chains, set_in_init false); every existing `attributes` row a moved function touches
   (`_launched`, `max_boundaries`, `_book_lock`, `_settle_lock`, `_book_cond`, `_drain_flag`, `_interrupt_flag`, `_chain_registry`,
   `_gate_said`, `_thread_slots`, and any other the test names) gets an owner at rank 0 (`driver_chains`, or `driver_core` where it is
   already there) — L7 demands owner <= every accessor's home. `exceptions` is not touched.

**edges (each with the invariant it protects):**
- A.1 An upward edge appears that the map cannot place (L5/L6/L7 red). INVARIANT: the pinned `exceptions` list never grows. Behaviour:
  STOP and return the edge in the report as a fork (`decomposable`); never add an exception row, never move a domain class to make it pass.
- A.2 Import cycle: `driver_chains` must import nothing from the package. INVARIANT: the scheduler module knows no stage — pinned by the
  new key `scheduler_module_knows_no_stage` (ast: no `Import`/`ImportFrom` of a non-stdlib module, no `ast.Constant` string that EQUALS `"S5"` or `"S6"` and is not a docstring (the moved docstrings are byte-identical and contain "S5", so a "contains" check would contradict item 1), no
  name starting `s5_`/`s6_` in `driver_chains.py`; a bad fixture with an `import story_run` line is reported by name).
- A.3 A test or sibling module reads a moved name through `story_run` (`SR.ChainRecord`, `SR._CHAIN`, `SR.Drained`). INVARIANT: the same
  object, not a copy — re-export by import (item 7); `SR._CHAIN is driver_chains._CHAIN` asserted in the new key.
- A.4 `run_chains` called with the old 4 positional arguments (tests :469). INVARIANT: same outcome as before for every existing caller —
  defaults give noun "window" (key :847 "waiting for window 1" holds), no gate, the generic seam (lowest number among failures; the only
  4-argument test with a failure, `seam_one_exception_after_the_drain` :535-552, has one failing chain).
- A.5 S5 console text. INVARIANT: byte-identical at the default (keys `test_story_run_s5_parallel.py:358`, `:553`;
  `test_driver_chain.py:742`, `:751`, `:847`) and at N=1 (the frozen set; N=1 never enters `run_chains`).
- A.6 `session_running` called outside a run (`test_driver_chain.py:513-533`). With no `_chain_kind` the generic gate holds nothing, so
  that key would go green-for-the-wrong-reason or red. Behaviour: the rig gets ONE line before :517, `d._chain_kind = d.s5_chain_kind()`
  (fork F1 — the only test edit of part A). INVARIANT: no assertion of the four proving files is edited.
- A.7 `_chain_kind` is per driver and set only inside `run_chains`. INVARIANT: S5 and S6 never run chains at the same time (stages are
  sequential in one driver; `run_s5_windows` may call `run_chains` twice in sequence on the F6 road :12140, :12148 — each call sets and
  resets it). A nested call is unreachable today; not guarded in A (no behaviour change).
- A.8 Ctrl-C, drain, R1/R2 interrupt roads. INVARIANT: unchanged (bodies verbatim); keys `interrupt_starts_no_new_process`,
  `interrupted_call_is_never_booked`, `interrupt_between_popen_and_registration`, `interrupt_during_the_wait_for_chains` stay green.

**tests by name:** all of `test_driver_chain.py` (unchanged keys) + new `scheduler_module_knows_no_stage`; `seam_names_what_it_does_not_choose` (:726-752, unchanged) is the named guard of items 5-6 (the seam's own kind); `test_driver_layers.py`
(real map clean in L1-L10, bad fixtures by name); CI: `test_story_run_s5_parallel.py`, `test_story_run_s5_n1_frozen.py` unchanged.

**witness (fast, local):**
`python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_chain.py`
`python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_layers.py`
plus `git -C D:/ws1/wt-fbfix diff --stat` and the diff of `test_driver_chain.py` (must show only the A.6 line and the new key);
CI lines of `test_story_run_s5_parallel.py` and `test_story_run_s5_n1_frozen.py` verbatim (read once, `docs/RUNBOOK.md` §7).
`--limits --lang` before the commit (`python -B scripts/selftest.py --lang`, FR-30). The witness also quotes the layer test's `exceptions` count (unchanged) and a grep showing `def run_chains` once, in `driver_chains.py`.

**AR-n:** AR-15 (one scheduler: grep `def run_chains` finds one definition, in `driver_chains.py`), AR-17 (one seam: `chain_seam` /
`s5_seam` re-raise to `guarded` only on the main thread — unchanged), AR-20 (`exceptions` row count before = after, printed by the
layer test), AR-13 (re-export, no copies). `architecture: AR-13, AR-15, AR-17, AR-20 -- moved verbatim, map rehomed, exceptions unchanged`.
**census:** no unit added or removed (the gate moves, its class xref unchanged; a moved refusal site keeps its row under the new file
name — the builder re-runs `test_judgment_census.py` and names any row whose file changed: key, old -> new). `judgment:` line: none.

---

### Part B (TR3-9b) — the S5 gate's file set takes what a probe can mutate (Lead decision 2; critic t-2121 Q6)

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\probe_debt.py` (`_oracle_where` (lifted from `_replay_plan`), `record_files` (new); `_item_files` unchanged)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`Driver.s5_window_files` only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_chain.py` (new key `window_files_take_the_oracle_file`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_debt.py` (new keys `oracle_from_probe_record_not_debt_file`, `gone_oracle_still_counted`; the fast file named by critic t-2152 B7)

`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\tr3-9b-gate-oracle-files.md` (new)

**Required behaviour:** `probe_debt.record_files(task_root, row) -> set` (new, public, a pure read). For every alias of the row (`_aliases`), read the probe record at `PL.probe_record_path(task_root, alias)` if it is a file (through `probe_debt._read_json_file`, the module's own reader, axis 16). From each readable record take the test file of `test_node` (before `::`), and, when `mutation_detail.oracle_function` is non-empty, the file `_oracle_where(record)`. `_oracle_where` is the `where` expression of `_replay_plan` :264-265 lifted into a helper that `_replay_plan` also calls: one reader of 'which file a replay of this record mutates'. No `_oracle_gone` check: a gone oracle still counts, because the error direction is a needless wait. `s5_window_files` adds `record_files(self.task_root, test)` for every manifest row that links a case of the window, normalised by `window_files.key_of`.

**edges:**
- B.1 Unreadable probe record -> the set without the oracle files plus the claims (today's set). INVARIANT: the gate never errs
  toward MORE concurrency than today — a read failure can only leave today's set, never shrink it below the claims.
- B.2 An oracle path outside the project or with backslashes -> normalised like `_item_files` (`_posix`, strip "/"), keyed by
  `window_files.key_of`. INVARIANT: one spelling per file, so two windows naming the same oracle meet.
- B.3 Error direction (reused function in a more consequential role: `_item_files` was a settle helper, now feeds a gate): it may report a file needlessly (a wait); it must never omit a file that a REPLAY of a recorded probe of this window mutates. An oracle the critic names fresh at run time is not knowable before the session; the guard's claim check and the settle's `running_window_words` remain the net for it (a named residual, not a gap of B). Adversarial inputs that must stay on
  the safe side: a record with an empty `oracle_function` (no oracle file, no crash); a record that is absent or not valid JSON (no file, no crash); a `test_node` with several `::` (the test file is the part before the first `::`); a row with no test file but an oracle record.

**tests by name:** `window_files_take_the_oracle_file` (two windows sharing only an oracle file are not launched together; a window whose probe record is unreadable keeps claims + manifest files; the adversarial inputs), `oracle_from_probe_record_not_debt_file`, `gone_oracle_still_counted`.
**witness:** `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_chain.py` and
`python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_probe_debt.py` (the fast file; `test_probe_debt_settle.py` does not exist: `ls scripts/tests | grep probe_debt` lists only `test_probe_debt.py`). CI: `test_story_run_s5_parallel.py`.
**AR-n:** AR-13 (one reader of "files a probe touches": grep `--oracle` parsing in `S\*.py` finds one site, positive control
`probe_debt.py:885`), AR-28 (B.1). **census:** the gate unit `story_run` launch gate stays xref; no new unit (a reader, no refusal).
Owner data (code).

---

### Part D (TR3-9d) — controller admits parallel S6 lanes; config key `manual.walkers` (runs beside A)

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\controller.py` (op `dispatch` branch :5150 condition: `or self._lane_beside_running(...)`; `_lane_beside_running` new beside `_window_beside_running` :5958; `_resume_problems` :6016 the same `or`; `_walkers_cap` new beside `_parallel_cap` :5946; `stage_entry_beside_running` :933-950: the S5 condition becomes 'S5, or S6 where both `d` and the running sibling are `execution_kind: manual` qa-runner dispatches'; the replay of a serial journal stays byte-identical)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\config_contract.py` (`walkers(config) -> (int, note)` beside `parallel_windows`)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\references\templates\config.json`, `D:/ws1/wt-fbfix\ai-packages\qa-factory\references\config-keys.json` (key `manual.walkers`, default 3; `manual` is a NEW top-level block in both files: grep `"manual"` / `"manual.` over `templates/config.json` and `config-keys.json` matches only `supported_capabilities` today; the note follows the template's sibling-note convention, `dispatch_windows_note`, template :95, and the builder names the note key beside it)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\skills\qa-onboarding\phases\p2-interview.md` (one topic line beside the `parallel_windows` one: "how many manual walkers at once; 1 = one at a time")
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_s6_lane_admission.py` (new, fast)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_config_migration.py` (rows for the key only)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (one row `controller.py::_lane_beside_running` xref, if the census counts it)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\tr3-9d-lane-admission.md` (new)

**Required behaviour:**
1. `config_contract.walkers(config)`: absent -> (3, None) (the shape of `parallel_windows`, `config_contract.py:555-570`: `(int, None)` when there is no note); an int >= 1 (bool excluded) -> (value, None); anything else -> (3, one note line
   naming the key, the value and "1 runs one walker at a time"). The ONE reader for driver and controller (AR-13).
2. `_lane_beside_running(p, state, running, flagged=True)` — True only when ALL hold: `flagged` -> `p.get("walk_lane") is True`; `p` and
   every running dispatch are stage S6, role `qa-runner`, `execution_kind == "manual"`; every scope a non-empty list of case-id strings,
   pairwise disjoint from `p`'s (also against S6 `returned_unaccepted` siblings, as the S5 clause does :5989-5991); `p` AND every running dispatch carry `walk_lane is True` and a `walk_actor` that is a string (`""` = guest); a record that lacks either -> False; the `walk_actor` values are pairwise distinct; `len(running) + 1 <= _walkers_cap()`.
   Pure, never raises (`except Exception: return False`). Same error direction as the S5 clause (docstring :5965-5967).
3. The refusal text when neither clause admits stays byte-identical (:5155-5162).
4. `controller.stage_entry_beside_running`: an accept or checkpoint of an S6 manual lane while another S6 manual dispatch is `running` leaves the stage `running` with the lowest running id; a `completed` entry is never touched.
5. The builder reads `_closes_stage` (:7115-7156; S6 is in `DERIVED_SCOPE_STAGES` :191) and adds `nonlast_lane_not_complete_beside_running_accepted`. If that key goes red, it is a fork back to the Lead, not a guess.

**edges:**
- D.1 POSITIONAL: the new clause sits in the SAME condition as `_window_beside_running` (first check of the branch, before `required`).
  INVARIANT: every check after it still runs on an admitted dispatch, and a mixed set (S5 window beside S6 lane, S6 beside a suite or
  any other stage) is refused — each clause demands ALL running dispatches be of its own kind.
- D.2 Two lanes on one account key, or a guest beside a guest. INVARIANT: two running walkers never sign in as the same account (the
  app's session would be shared). Behaviour: refused; the driver (part C) never asks for it, so the refusal is a seam, not a road.
- D.3 `walkers: 1` -> cap 1 -> the clause never admits (`len(running)+1 <= 1` false with one running). INVARIANT: `walkers: 1` keeps
  today's "one running dispatch" exactly.
- D.4 TEMPORAL: before this commit no S6 request carries `walk_lane`; old stories' dispatches have no `walk_actor`. INVARIANT: a request
  without the flag keeps the old refusal; a running record without `walk_lane: True` and a string `walk_actor` (any dispatch registered before this commit, or off the lane road) -> the clause is False: the old refusal stands. The driver adds both fields to the request dict it already builds (`story_run.py:13827-13829`); the Dispatch schema accepts extra keys (`record_schema.py:22`) and apply keeps them (`controller.py:1642` `dict(p, status="running")`); the producer is C (AR-22).
- D.5 Config unreadable / no project -> default 3 (same as `_parallel_cap` :5950-5956). INVARIANT: never a refusal from a config read.
- D.6 `walk_actor` not a string (list, None) -> the clause is False. INVARIANT: an unreadable thing is not distinct (AR-28).

**tests by name (`test_s6_lane_admission.py`):** `two_lanes_disjoint_distinct_accounts_admitted`, `shared_case_refused`,
`same_account_refused`, `guest_beside_guest_refused`, `no_flag_old_refusal_byte_for_byte`, `s6_beside_s5_window_refused`,
`over_cap_refused`, `walkers_one_never_admits`, `returned_sibling_scope_counts`, `walk_actor_not_string_refused`,
`resume_beside_running_lane`, `old_running_record_without_walk_actor_refuses`, `s6_lane_accept_beside_running_keeps_stage_running`, `s6_serial_replay_byte_identical`, `nonlast_lane_not_complete_beside_running_accepted`, `config_walkers_absent_bad_bool_zero` (absent 3; "2" 3+note; True 3+note; 0 3+note; 2 -> 2).
**witness:** `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_s6_lane_admission.py`,
`python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_s5_parallel_admission.py`,
`python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_config_migration.py`; regenerate `controller-blocks.md`
if the generator says so (`python -B tools/controller-blocks-gen.py`). CI: `test_controller_*`.
**AR-n:** AR-3 (one commit: template, keys row, reader with default, interview line), AR-13 (one reader `config_contract.walkers`),
AR-22 (`walk_lane`, `walk_actor` each name the reader `_lane_beside_running`; the pair `test_s6_lane_admission.py::two_lanes_disjoint_distinct_accounts_admitted` (reader) and `test_walk_lanes_parallel.py::request_carries_walk_lane_and_actor` (producer, C1); `test_field_producers.py` walks handoff-contract fields, not dispatch request fields), AR-28 (D.6), AR-9 (refusal
text unchanged). **census:** `_lane_beside_running` — owner data (code), class xref; walkers reader — shape, tells never stops.

---

### Part C (TR3-9c) — S6 lanes on `run_chains` (after A, B and D; the S6 twin), split into C0, C1, C2 (critic t-2152 N12)

Order (Lead): A ∥ D, then B, then C0, C1, C2; one critic on the merged diff. C1 and C2 own disjoint files.

#### C0 — the frozen S6 set (its own commit, BEFORE any change of the S6 road)

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\s6-w1-frozen\` (captured)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_story_run_s6_w1_frozen.py` (new, CI)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\slow_tests.json` (row for the frozen file)

**Required behaviour:** captured on the tree after A+B+D are merged and BEFORE any C1 or C2 byte, in its own commit, so the changed tree can never produce the fixture; the commit hash is recorded in this spec, as S5's `d005e84c5` was: `124d8c966`. C0 captures on a tree with no `manual.walkers` reader, so it needs no `seed()` pin (F6). Keys: `w1_frozen_calls`, `w1_frozen_events`, `w1_frozen_state_keys`, `w1_frozen_console`.

#### C1 — lanes (the rest of this part, items 1-8 and edges C.1-C.13, is C1's)

**owns (C1):**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\story_run.py` (`run_manual_block` — split into `manual_lane_plan` (the plan part :13777-13801) and `run_manual_lane(record, lane)` (the dispatch + walk + role part :13806-13868); `stage_S6` call site :13072; new `s6_walkers_cap`, `s6_serial_reason`, `s6_lane_holds`, `s6_chain_kind`, `s6_open_lanes`, `s6_settling_lanes`, `s6_seam`, `run_s6_lanes`; `walk_before` — item 4(d) only: on the parallel road it passes `--max-shared <s6_walkers_cap()>` to `walk_session.py open`; no other edit expected, see C.5)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json` (rows for the new members)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_lanes_parallel.py` (new, fast: `Driver.__new__` + fake `run_role`, as `test_driver_chain.py` does)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\walk_session.py` (`open --max-shared N`, int >= 1, default 1; it sets `max_shared` on the session, also in the spawned own process; nothing else)
walk_session's own fast test file (the builder names it; one key)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\design\state-exits.md` (one row)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (N13: the row for `s6_open_lanes`, which RAISES, if `test_judgment_census.py` counts it; D merges first, so it does not overlap D's owns)
`D:/ws1/wt-fbfix\ai-packages\qa-factory\changelog.d\tr3-9c-walker-lanes.md` (new)

**non-goals (C1):** accounts beyond what `lane_keys` already gives, entity isolation, the holds-no-case question (TR3-10); `stand_lease.py` (TR3-7 done: lease mode `walk`); `manual_evidence`; the S5 road; the identity sites (C2); the frozen set (C0).

**Required behaviour:**
1. `stage_S6` -> `run_manual_block(cases)` keeps its name and its serial body for `walkers == 1`, for one lane, and whenever
   `s6_serial_reason()` is non-empty: one lane per entry, verbatim (the old road; no thread, no `walk_lane` flag, no new state key). At walkers 1 none of `s6_serial_reason`, `s6_settling_lanes` or the new lane state runs; the only new read is `s6_walkers_cap()`, which prints nothing but a bad-value note.
2. Otherwise `run_s6_lanes(plan, cap)`: items = the plan's lanes in plan order, `(n, lane, lane)`; `launchable = self.chain_launchable` (A item 4b over `s6_lane_holds`: a lane does not START while a live lane holds one of its cases or its account; this is what keeps D.2 unreachable); `chain_fn = self.run_manual_lane`; `cap = min(walkers, lanes)`; `kind = s6_chain_kind()` = `ChainKind("S6", "lane", "a case or an account", lambda cases: self.s6_lane_holds(cases), tag="L")`; `seam = self.s6_seam`.
   2b. Lanes whose account key is unreadable (`account:?<case>`) and lanes that meet a running or stopped S6 dispatch run first at cap 1 (item 6); then the rest go side by side. New key `same_account_second_lane_never_registers` (fake controller: the second same-key lane's `apply` comes only after the first chain is done).
3. `s6_lane_holds(cases)` = `{"case:" + c for c in cases} | {"account:" + key}`, `key = lane_keys(self.task_root, list(cases)).get(cases[0])`; `""` -> `"account:guest"`. A key that is None or absent (an unreadable request, E5s.8) -> `"account:?" + cases[0]`. That lane never shares an account key, and it runs in the serial first round (item 2b). Two lanes on one account key therefore never run at once (they run in turn), matching the controller's D.2.
   **Rule added (Lead, 10.11.2026, from critic t-2177 B4): one hold per handle, not `+`-joined.** For a lane key of several parts (`lane_key` joins them with `+`), `s6_lane_holds` gives ONE `"account:" + <part>` hold PER part of the key (never `"account:" + <the whole key>`), so lanes whose part SETS intersect (`stand_account:admin+stand_account:user` and `stand_account:user`) hold a common string and run in turn; whole-string holds would admit both and two walkers would sign in as one account (the only net would be `walk_session open`'s refusal, which sends the lane to the recorder road, not to "in turn"). Key `overlapping_part_sets_in_turn` (`test_walk_lanes_parallel.py`). `""` stays `account:guest` until TR3-10 D (t-2174 B10) replaces it with `account:guest#<lane n>`. The controller clause (`walk_actor` compared as whole strings) is unchanged: a named residual, the driver gate keeps the overlap unreachable.
4. `run_manual_lane(record, lane)`: today's dispatch part with three differences only: (a) the id is reserved under `_book` (the
   `len(prior)+1` count :13815-13816 is read and the dispatch applied in the same booked step, so two lanes never take one id); (b) the
   request carries `walk_lane: True` and `walk_actor: <lane account key>`; (c) `complete` is a callable `lambda digest: self.consumer_awaits("S6", closes) if acceptance.consumer_of("S6") else closes`, where `closes = (not self.walk_pending(lane) if walking else True) and not refused and not waiting and not self.s6_open_lanes(excluding=lane)`. An exception from `s6_open_lanes` makes `closes` False (FR-59). `run_role` evaluates it at the finish (`story_run.py:3270`), under `_book` — the S6 twin of `s5_last_fn`; (d) on the parallel road only, `walk_before` passes `--max-shared <s6_walkers_cap()>` to `walk_session.py open`; the old road passes nothing (byte-equal at walkers 1: the frozen call sequence); keys `walk_open_carries_max_shared` (driver side) and one key in walk_session's own fast test file (the builder names it); (e) the first line of `run_manual_lane` is `self.boundary = "S6"` (the twin of `s5_window_chain` :12066). `walk_before`, `record_running`, `run_role(..., complete=...)` and its walk hook run as today; the role session runs
   unbooked through the existing `launch` -> `unbooked` / `session_running` (no new lock site).
5. `s6_open_lanes(excluding=())`: the cases of this entry's S6 manual plan, minus `controller.manual_done_cases(state)` (the ONE reader of 'accepted manual cases', AR-13), minus the lane `excluding`. Read fresh from the controller state. RAISES when the state cannot be read.
6. `s6_settling_lanes` (the settle-window twin the critic asked for, t-2125 class line "axis 5"): lanes that meet a running, blocked or
   paused S6 manual dispatch at entry; they run at cap 1 first, then the reason is re-read and the rest goes side by side (the F6 road
   of `stage_S5` :12130-12148, one round only).
7. `s6_serial_reason()` -> "" or one reason, printed once through `say_once("s6-lanes", "note: S6 lanes run one at a time: <reason>")`:
   host not Claude (`host_window_reason`, the one host reader); dispatches of S6 running or stopped at entry (S6_SETTLE_RUNNING, falls
   away per item 6); the stand not shareable (the lease answers no `walk` mode — builder's first read: `stand_lease.hold` signature of
   TR3-7 and the `run.parallel` edge E1b.2 of t-1957: `execution.parallel.mode: serial` -> 1 always); a deferred question that holds a
   case of the plan (RN1-24 `deferred_waiting`, :13780); unreadable state; a model-service limit earlier in this run.
8. `s6_seam(records, cap)` = `chain_pick(records, self.s6_chain_kind(), seam_rank)`; the limit branch sets `_s6_cap_one` (twin of `_s5_cap_one`); else adopt +
   raise.

**edges (each with its invariant):**
- C.1 `walkers: 1` -> the old road. INVARIANT: byte-for-byte today's S6 (calls, events, state keys, console) — proved by the frozen set
  `fixtures/s6-w1-frozen/` captured by C0 on the tree after A+B+D, before any C1 byte (stub call sequence, `events.jsonl` event sequence, driver-state keys, console
  text) + key `no_thread_started_at_walkers_1` (fork F3: why a frozen set and not `test_walk_lanes.py`).
- C.2 Fewer lanes than walkers, or one lane -> cap = lanes; one lane takes the old body. INVARIANT: no thread for one lane.
- C.3 A lane crashes -> drain; the others' running sessions finish and book; the seam re-raises one; the crashed lane's dispatch re-arises
  on re-entry by its saved result. INVARIANT: no other lane's accepted record is lost; one seam per turn (AR-17). A lane whose `walk_before` opened a session and that ends before `run_role` closes it (`walk_after(lane, id, {})` in the lane's `finally`); key `crashed_lane_closes_its_walk`.
- C.4 A lane's `walk_before` fails (no walk session) -> that lane runs on the recorder road as today (E5s.4); others unaffected.
  INVARIANT: FR-57, nothing locks the role.
- C.5 Story-wide writes by parallel lanes: `run-report.json` (`finalize_task.py` in `walk_before`), the app card, `walk_old_road` in
  driver state, `walk_after`'s records, `created-accounts.json`. INVARIANT: role-invoked `finalize_task` may run in two lanes at once: an atomic, idempotent reducer; the closing finalize (`walk_after`/finish, under `_book`) reduces again; the report names each writer with its lock or this reason. `finalize_task` of lane A tolerates lane B's attempts without records (t-1957 N5p). `created-accounts.json` has its own lock (TR3-8/N1c). The builder greps
  `walk_after` and `finalize_task` callers for a write outside the book and reports each.
- C.6 S6 close. INVARIANT: S6 completes only by the finish that leaves zero open lanes, exactly once whatever the finish order (the callable of item 4(c), evaluated at the finish under `_book`, makes the last finisher see zero); an unreadable lane state is open (`complete=False`, never a close). A lane that ended blocked, paused or returned counts as open until its case is accepted (item 5).
- C.7 Drain. INVARIANT: no new dispatch after the drain (`stop_if_drained` at `run_role` entry, :3106); `run_manual_lane` calls `self.stop_if_drained()` BEFORE the controller `apply("dispatch")`, so a drained lane registers nothing. That covers registration, not a chain already waiting in `session_gate` when the drain starts (t-2121 Q3 itself); with the live-chain start gate (item 2) an S6 lane never waits in the session gate (cases and account are exclusive from the start), so the residual is unreachable for S6. TR4-10's line adds: the Q3 fix lands in `driver_chains.session_gate` (generic) after TR3-9a.
- C.8 Ctrl-C. INVARIANT: no `claude` starts after it and a killed session is never booked — inherited from `_launch`/`run_chains`
  (no new launcher); key `lane_interrupt_kills_children`.
- C.9 POSITIONAL: the dispatch id reservation and `apply` are in ONE booked step, before `walk_before`. INVARIANT: two lanes never share
  a dispatch id, and the walk record is in place before the role starts (E5s.4 position invariant of `walk_before`, :3615-3616).
- C.10 TEMPORAL: a story mid-S6 from before this commit (one running S6 dispatch, no `walk_lane`) -> `s6_serial_reason` names "running
  at entry", the lane runs alone first, then the rest in parallel. INVARIANT: a registered dispatch is run once, never twice. A running dispatch with no `walk_actor` is read as an UNKNOWN account: no lane is admitted beside it (D.4, the safe side).
- C.11 The plan changes between entries (a refused case, a deferred case). INVARIANT: lanes are re-cut from the plan at each entry
  (`walk_lanes` :13791 as today); a lane in flight is never re-cut.
- C.12 An old walk session record without the `max_shared` field reads 1 (today).
- C.13 A lane's question to the person is inherited from the seam: Person is ranked last, the other Persons are named "also ended with Person" and asked on the next entry (`test_story_run_s5_parallel.py:350-362`), and `ask` runs on the main thread only, because the seam re-raises there. Key `lane_question_queued_next`.

#### C2 — S6 identity sites (axis 33, "which dispatch am I"; carried from t-1937 §3.1 row "S6 only")

**owns:**
`D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\validate_artifacts.py` (`_s6_runner_half` only)
its fast test file (the builder names it)

The list of S6 sites that pick the running dispatch by count comes from scout t-2160 (`docs/tasks/specs/reports/t-2160-s6-identity-sites.md`); the builder of C2 reads it first. `_s6_runner_half`: the record is `dispatch_identity.own(raw, role="qa-runner", stage="S6", name=dispatch_identity.named())`. With no name it is the count rule (unchanged); two running and no name -> ("", []) as today (a doubt never skips a refusal). `manual_evidence._running_dispatch` (:1393-1405): SAFE, it binds by the case, and lane scopes are disjoint (D clause); a row in the report. The `story_run` S6 close re-probe (:13224-13227, `covering or running[0]`): SAFE, it runs at the stage close after every lane joined; a row in the report. New key `s6_runner_half_by_identity_beside_a_lane`. The builder's report drafts the axis 33 row text, and the Lead places it, and re-checks in one line each the generic rows: `stage_guard.stage_of_dispatch`, `execution_request.find_active_dispatch` (safe: disjoint cases), `controller._next_action_for_state` `active[0]` (safe: serial resume), `run_suite.active_story_stage` (safe after B5). A site that cannot read the identity is a fork back, not a guess.

**tests by name (`test_walk_lanes_parallel.py`, fast):** `walkers_default_three_lanes_overlap` (fake `run_role` records overlap with a
barrier, no sleeps, FR-31), `walkers_1_takes_old_road_no_thread`, `one_lane_old_body`, `same_account_lanes_in_turn`,
`lane_crash_others_finish_one_seam`, `drained_lane_registers_no_dispatch`, `close_exactly_once_order_free`,
`unreadable_lane_state_is_open`, `ids_never_shared`, `settling_lanes_first_then_parallel`, `serial_reason_each_row`,
`lane_interrupt_kills_children`, `held_case_keeps_serial`, `same_account_second_lane_never_registers`, `walk_open_carries_max_shared`, `close_waits_for_a_blocked_lane`, `consumer_branch_never_author_close`, `lane_question_queued_next`, `crashed_lane_closes_its_walk`, `request_carries_walk_lane_and_actor`, plus one key in walk_session's own fast test file (the builder names it); C2: `s6_runner_half_by_identity_beside_a_lane`. CI (C0 captures, C1 runs it unchanged): `test_story_run_s6_w1_frozen.py` (`w1_frozen_calls`, `w1_frozen_events`,
`w1_frozen_state_keys`, `w1_frozen_console`).
**witness:** `python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_lanes_parallel.py`,
`python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_walk_lanes.py`,
`python -B D:/ws1/wt-fbfix\ai-packages\qa-factory\scripts\tests\test_driver_layers.py`; CI lines of the C0 frozen file (unchanged by C1) and
`test_story_run_s5_parallel.py` verbatim.
**AR-n:** AR-15 (no second scheduler: grep `threading.Thread(` in `story_run.py`: zero new), AR-17, AR-19 (twin table §4 in the report
and the commit; Lead writes axis 5 / axis 33 rows — decision 3, in C's commit), AR-25 (state-exits row), AR-28 (C.6), AR-14 (C.5),
AR-22 (`walk_lane`/`walk_actor` produced here, read by D). **census:** `s6_open_lanes` xref, `s6_serial_reason` shape (tells), `s6_lane_holds`
xref (a reader; no refusal) — owner data (code); a row per new unit the census counts, named in the report; `s6_open_lanes` RAISES, so its row (if counted) goes in `judgment-census.json`, which C1 owns (N13).

## 3. What TR3-9 leaves for TR3-10 (N8)

- More accounts than `lane_keys` gives (`manual.accounts_way`, `accounts_by_role`, self sign-up `obtain-account`): until TR3-10, lanes
  sharing an account key run in turn (C.3 of §2 item 3) and the run says so through the start gate's line.
- Entity isolation (`walk_data`/`walk_global`, pools, `claim`): until TR3-10 two lanes on distinct accounts MAY touch one entity —
  stated as a known gap in the C changelog fragment and in the N-LIVE list; `walk_global` / "alone" lanes are TR3-10's.
- The holds-no-case question and `deferrable`/`defer_question` (E8.0); the `s6.accounts_way` / `s6.data_way` question sites.
- Old t-1957 E5p rule "launch rule (iii) counts only LIVE questions" moves to TR3-10 (it depends on the holds-no-case flag); TR3-9's
  C keeps the current rule: a deferred question holding a case of the plan makes S6 serial (item 7).
- Guest lanes (F4, critic t-2152 N11; recommendation taken): F4 serialises GUEST lanes too (holds `account:guest`; D.2 refuses guest beside guest). Guests sign in to nothing, so on a story whose manual cases are all guest, "default 3" is 1 in practice. Kept for TR3-9 (two guests can still collide on data, which is TR3-10's); the limit is stated in C's changelog fragment and here, so that "3 walkers" is not read as a promise for guest-only stories. Running guests in parallel now is the owner's call (intent), not a technical one.

## 4. Twin table S5 -> S6 (axis 5; part C report repeats it with verdicts)

| S5 piece | S6 twin | part |
|---|---|---|
| `run_s5_windows` | `run_s6_lanes` | C |
| `s5_window_chain` | `run_manual_lane` | C |
| `s5_chain_kind` / `s5_window_files` / `s5_launchable` | `s6_chain_kind` / `s6_lane_holds` / `chain_launchable` over the same holds (A item 4b) | A, C |
| `s5_seam` (+ `_s5_cap_one`) | `s6_seam` (+ `_s6_cap_one`) | C |
| `s5_open_windows` / `s5_last_fn` / `s5_open_flag` | `s6_open_lanes` / close predicate in `run_manual_lane`; no `--open-windows` twin (S6 completion is by accepted cover, `_s6_completion_problems`) — builder confirms by reading it | C |
| `s5_settling_windows` | `s6_settling_lanes` (critic t-2125 class line) | C |
| `s5_serial_reason` | `s6_serial_reason` | C |
| `s5_parallel_cap` / `config_contract.parallel_windows` | `s6_walkers_cap` / `config_contract.walkers` | C, D |
| `_window_beside_running` | `_lane_beside_running` | D |
| `s5_release*`, window claims (`window_files`) | not applicable: S6 writes no project test files; its exclusivity is the case + account (controller + gate) | — |
| `--parallel-window` flag | `walk_lane` request field (in-process prepare, no CLI flag: S6 dispatches are registered in-process :13823) | C, D |
| `_interrupted`, R1/R2, F2 running mark | inherited unchanged from `driver_chains` (no S6 code) | A |
| `controller.stage_entry_beside_running` (S-2; S5 only today) | the same function, S6 manual lanes added (t-2152 B5) | D |
| `_closes_stage` with a not-complete lane beside a running one (t-1937 B3) | the same function; key `nonlast_lane_not_complete_beside_running_accepted`; red -> a fork back to the Lead | D |
| `_s5_running_beside_problems` (backstop) | not applicable: `_s6_completion_problems` already refuses a close over running (unaccepted) lanes | — |

## 5. Forks (returned; each part is written to the recommendation)

- **F1 — the one test edit of part A.** The generic gate reads `_chain_kind`; `test_driver_chain.py:513-533` drives `session_running`
  outside a run. (a) one rig line `d._chain_kind = d.s5_chain_kind()`, assertions untouched, diff shown in the witness [recommended];
  (b) keep `session_gate`/`session_running`/`files_overlap_running` in `story_run.py` defaulting to S5 files — refused: an S6 lane would
  then be gated on S5 claims (none), i.e. no gate, the wrong error direction; (c) a separate S6 gate — a second survivor (AR-15).
- **F2 — rank of `driver_chains` in the layer map.** (a) rank 0, joining `driver_core`'s group [recommended: `Refusal` (core) reads
  `_CHAIN` and the launcher calls `unbooked`; a higher rank makes upward edges the pinned list cannot take]; (b) its own group below
  `driver_core`: the `Refusal` and launcher edges point down, so it passes and is stricter. Either keeps `exceptions` unchanged.

### Lead decisions on the forks (10.11.2026; a critic-on-plan pass follows before any builder)

F1 = (a), the one rig line, shown in the witness. F2 = (a), rank 0 beside `driver_core` (one group fewer in the map; "below
everything" is not a property any reader needs today). F3 = (a), a captured set `fixtures/s6-w1-frozen/`, captured BEFORE part C
changes the S6 road. F4 = (a). F5 = (a). F6 = (a): default 3 lands with part C. Order as drafted: A ∥ D, then B, then C; one critic on the merged diff.

**After critic t-2152 (10.11.2026).** The critic's plan review (`docs/tasks/specs/reviews/t-2152-critic-plan-tr3-9.md`: B1-B9 blocking, N1-N14 non-blocking, each with replacement text) is applied to this spec. Lead decisions:
- B1-B9: all accepted as the critic writes them. B1 the seam reads its own kind (`chain_pick(records, kind, rank)`, no `rank` field, an outer `finally`); B2 `holds` takes CASES; B3 the S6 start gate is over LIVE LANES (`chain_launchable`, A item 4b), not running sessions; B4 `walk_session.py` joins part C1's owns (the `max_shared` flag, `open --max-shared N`); B5 `stage_entry_beside_running` covers S6 (part D); B6 `validate_artifacts._s6_runner_half` reads the dispatch through `dispatch_identity`, never by count (part C2); B7 the oracle file is read from the probe RECORDS (`probe_debt.record_files`, `_oracle_where`), not from the probe-debt files; B8 the S6 close check is a callable evaluated at finish and counts blocked, paused and returned lanes and the X7-6 consumer branch; B9 an old running dispatch with no `walk_actor` (or without `walk_lane: True`) is read as UNKNOWN account: no lane is admitted beside it (the safe side).
- Part C is split as the critic proposes: C0 (capture of the frozen set `fixtures/s6-w1-frozen/`, its own commit, BEFORE any change of the S6 road), C1 (lanes), C2 (identity sites). Order: A ∥ D, then B, then C0, C1, C2; one critic on the merged diff.
- Every non-blocking item that has replacement text is applied. A non-blocking item that needs a decision and has none is in the last section "Open after t-2152" with the critic's recommendation marked as taken.
- **F3 — how `walkers: 1` is proved.** (a) a frozen set `fixtures/s6-w1-frozen/` captured by C0 (its own commit, before any change of the S6 road), as S5's [recommended: the Lead's
  ruling in the acceptance handoff §3 row "Frozen N=1 set" — `1` is a promise of the old road and only a captured set proves it];
  (b) `test_walk_lanes.py` as is — it judges lane cutting (`walk_lanes`), not the S6 road's calls and events, so it cannot prove parity.
- **F4 — lanes on one account key.** (a) they run in turn, gate + controller refuse them side by side [recommended; TR3-10 adds
  accounts; guest lanes: one at a time until TR3-10 D (owner, 10.11.2026: guests side by side when their data is apart, t-2174 B10)]; (b) allow with a note — two walkers in one app session: wrong results, not just slower.
- **F5 — a deferred question holding a plan case.** (a) S6 runs serial while it waits [recommended until TR3-10 brings holds-no-case];
  (b) lanes not holding that case run parallel — needs the TR3-10 flag to be safe.
- **F6 — default 3 lands with C.** The owner's word is 3 (t-1957 F5, 18:55). (a) the default takes effect in C's commit, `seed()` of
  the S6 rigs pins `manual.walkers: 1` so old tests keep their meaning (as TR3-12 did for S5) [recommended]; (b) ship default 1 until
  N-LIVE — against the owner's word, needs the owner.

## 6. What changes in t-1957

- **Line 205-208 (F12):** replace "the chain runner `S5Scheduler` in `stage_S5`, one driver lock `self._book` (RLock), `launch` releasing
  it around `communicate`" and "**Not landed in wt-fbfix:** ..." with: "the scheduler `Driver.run_chains(items, launchable, chain_fn,
  cap)` (landed TR3-6, `story_run.py:11929`; moved by TR3-9a to `driver_chains.py` with `kind=`/`seam=` keywords), one driver lock
  `_book` — a plain `threading.Lock` (`story_run.py:11562`), released only by `unbooked` on a chain thread with a dispatch or a settle;
  admission `_window_beside_running` (`controller.py:5958`); config key `dispatch.parallel_windows` read by `config_contract.parallel_windows`.
  Landed in wt-fbfix."
- **Line 932-934 (Slice 2 dependency):** replace with "Dependency: TR3-6 / TR3-18 (scheduler, landed), TR3-7 (lease `walk`, landed).
  TR3-9 is specified in `docs/tasks/specs/t-2147-tr3-9-walker-lanes.md` parts A-D." Delete the "If t-1937 P1 is not landed ... walking
  with 1" sentence and its `note:` (the condition is void; E5p.1's "t-1937 absent -> 1 + the note" goes with it).
- **N5p section (992-1019):** replace whole by a pointer: "#### N5p = TR3-9 — see t-2147 parts A (extract `driver_chains.py`), B (gate
  takes probe files), C (S6 lanes), D (controller clause, `manual.walkers`)." Old owns `run_manual_block lane scheduling; a shared chain
  base extracted from S5Scheduler` -> part A/C owns; old "each lane's code steps under `self._book`, the role session outside it" stays
  true (inherited); old "Launch rule (iii) counts only LIVE questions" -> TR3-10 (§3); old test names map: `test_walkers_default_three`
  -> D `config_walkers_absent_bad_bool_zero` + C `walkers_default_three_lanes_overlap`; `test_bad_value_three_with_note` -> D;
  `test_no_t1937_one_with_note` -> deleted (void); `test_walkers_1_is_serial_parity` -> C frozen set; `test_two_lanes_distinct_accounts_overlap`
  -> C; `test_alone_lane_runs_by_itself` -> TR3-10; `test_lane_crash_others_go_on` -> C; `test_story_files_written_under_lock` -> C.5
  report + `close_exactly_once_order_free`; `test_deferred_no_hold_question_not_pending` -> TR3-10.
- **Line 1091-1093 (order inside Slice 2):** "N5p after t-1937 P1 and N1b" -> "TR3-9 (A ‖ D, then B, C0, C1, C2) after TR3-6/18 and TR3-7;
  N8 = TR3-10 after TR3-9 C".
- **Line 93, 126 (AR / check tables):** the S6 admission clause is `controller._lane_beside_running` (part D), not "inside op dispatch
  extending N-P1-1".

## 7. Small choices closed by the designer

- Module name `driver_chains.py`, class `DriverChains` (forced by the layer test's driver set and `Driver*` census; name chosen).
- `files_overlap_running` renamed `chain_overlap_running` (it no longer reads files; no test calls it by name — grep of the five test
  files above found no direct call).
- Generic defaults `label="chains"`, `noun="window"` (keeps key :847 without an edit; "window" is the scheduler's own word for a chain).
- `seam_rank` lifted to a module function in `story_run.py` (home driver_core) instead of class attributes on the exceptions: no change
  to the domain classes.
- `walk_lane` as a request field, not a CLI flag (S6 dispatches are in-process).
- Lane resource keys prefixed `case:` / `account:` so a case id can never equal an account key.

## 8. Reading trail

Read: brief; `docs/tasks/handoffs/20261110-lead-window-acceptance.md` (all); `t-1957-fast-manual-walker.md` grep for
N5p|S5Scheduler|RLock|walkers, then :195-214, :925-1099; `t-1937-s5-parallel-windows.md` headings, §1 :20-65, §3.1-§3.7 :88-211,
§5 :226-234, TR3-17/TR3-6/TR3-18 :352-395, §9-§10 :408-441; reviews t-2121 (all), t-2125 (all); `story_run.py` :360-479, :1180-1229,
:3609-3688, :11530-12199, :13768-13897, greps for the scheduler defs, `_CHAIN`, domain exception classes, the three console texts,
`run_manual_block(`/S6 helpers; `test_driver_layers.py` (all); `driver-layers.json` greps (layers, not_driver, chain rows :846-925,
homes of domain classes and S5/S6 members); `test_driver_chain.py` :1-60, :380-530, :535-579, :700-760, :760-889 and grep of its
defs; grep of scheduler names over the five test files; `controller.py` :5140-5164, :5944-6023, grep `_window_beside_running|parallel_window`;
`probe_debt.py` :832-903 (`other_windows`, `_item_files`, `running_window_words`); `plans/piles/thinking-roles/batch-3-parallelnost.md`
rows TR3-7/9/10/18 and the order line :8.
Greps with positive controls: Glob for `test_story_run_s5_equivalence.py` found nothing while the same Glob found
`test_story_run_s5_parallel.py` (the equivalence keys live in `test_story_run_s5_parallel.py:653ff`); Glob for `test_walk_lanes*.py`
found only `test_walk_lanes.py`; `walkers|parallel_windows` file list (30 files) — whether `manual.walkers` exists is NOT established
(builder's first read in part D: `config-keys.json`, `templates/config.json`, `config_contract.py`); SIBLING_MAP rows for axes 5 and 33:
my pattern `^\| *(5|33) *\|` found nothing and I ran no positive control — the map's row format is unverified; the Lead writes those rows
(decision 3), so nothing here depends on their text.
Not read (builder's first reads, named in the parts): `_launch` body (relied on t-2125's trail :2028-2068), `stage_S6` body beyond
:13072, `walk_after`, `_s6_completion_problems`, `manual_evidence._running_dispatch`, `validate_artifacts._s6_runner_half`,
`stand_lease.hold` signature, the TR3-15 per-dispatch probe-debt reader, the fast test file of `probe_debt._item_files`.
Needed beyond the manifest: `test_driver_layers.py`, `driver-layers.json`, `probe_debt.py`, `controller.py`.

## 9. Open after t-2152

Items of critic t-2152 that need a decision and carry none of their own; the critic's recommendation is marked as taken, and the Lead can overturn any line.

- N2 (console tag): recommendation TAKEN. `ChainKind.tag = "W"` (default) and `ChainRecord.tag` set by `run_chains`; S5 stays `[W<n>]` byte-identical, S6 lanes print `[L<n>]`. The alternative (state in C that lane lines carry `[W<n>]`) is not taken. Effect: `ChainKind` has five fields (label, noun, held, holds, tag), not four.
- N11 (guest lanes): recommendation TAKEN. F4 stays for TR3-9; the limit is written into §3 and C's changelog fragment; running guests in parallel is the owner's call.
- B7 witness keys: the two new B keys (`oracle_from_probe_record_not_debt_file`, `gone_oracle_still_counted`) live in `test_probe_debt.py`, the fast file the critic names; it is added to B's owns (the critic named the witness file but not the owns line).
- B AR-13 grep form: "grep `--oracle` parsing finds one site" no longer holds after B7 (`_item_files` parses `_args`, `_replay_plan` builds `--oracle`, `_oracle_where` is the ONE reader of which file a replay mutates). Recommendation TAKEN as a proposal: the builder greps the callers of `_oracle_where` / `record_files` as the one-reader check and names its grep form in the report.
- C order of C1 and C2: the critic says C1 and C2 own disjoint files; the Lead's order line reads "then C0, C1, C2". Written as the Lead's order; whether C1 and C2 may run side by side is not decided here.
- C.12 (an old walk session record without `max_shared` reads 1) carries no invariant sentence in the critic's text, and designer rule 1 asks every named edge for one: left as the critic wrote it.
- The note key for `manual.walkers` (D owns): the critic names the convention (`dispatch_windows_note`), not the key; the builder names it beside the sibling.
