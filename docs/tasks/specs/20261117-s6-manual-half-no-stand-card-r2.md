# FV3-21 / FV3-21b — the person's no-stand word reaches the manual half of S6, on both roads (card r2, designer t-1128)

Pile `live-run-fvf`, batch 3. Nodes: **FV3-21** (driver road + the class fix B1 + the shared homes) and **FV3-21b** (skill road).
Sources: card r1 `docs/tasks/specs/20261117-s6-manual-half-no-stand-card.md` (t-1110), plan critic verdict
`docs/tasks/specs/reviews/t-1118-fv3-21-plan.md` with its section "Lead decisions on the verdict" (B1 = (b2), B2 as written,
F1 recommended form, F2-F9 as written), diagnosis `docs/tasks/specs/reviews/t-1106-dry-s6-manual-half-diagnosis.md`.
Designer: opus, t-1128, 2026-11-17. Status: DRAFT r2 for Lead acceptance. No second plan critic unless the Lead finds the
architecture changed (dispatch non-goal); the one architectural addition is named in §1.4 so the Lead can judge that.

This card is SELF-CONTAINED: a builder reads r2 alone. All package paths are relative to `ai-packages/qa-factory/`. Line numbers
are of the root checkout `main` (HEAD `b89871b3`) read 2026-11-17; every function cited was re-read for this round (trail at the end).

---

## 0. The two builder cards, owns, order

| node | owns (repo-relative; the Lead prints them absolute with `tools/dispatch_new.py`) | starts | merges |
|---|---|---|---|
| FV3-21 | `ai-packages/qa-factory/scripts/driver_stage_s6.py`, `ai-packages/qa-factory/scripts/driver_stage_build.py`, `ai-packages/qa-factory/scripts/waiver.py`, `ai-packages/qa-factory/scripts/manual_evidence.py`, `ai-packages/qa-factory/scripts/driver_dialog.py`, `ai-packages/qa-factory/design/state-exits.md`, `ai-packages/qa-factory/scripts/tests/test_story_run_s6.py`, `ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json`, `ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red.json`, `ai-packages/qa-factory/changelog.d/fv3-21-no-stand-manual-half.md` (new) | from `origin/main` AFTER the FV3-20 branch (5979acb4 + the J2 fix round t-1109) is merged (Lead decision F-4 = (a)) | wave W |
| FV3-21b | `ai-packages/qa-factory/scripts/story_step.py`, `ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py`, `ai-packages/qa-factory/skills/qa-story/phases/s6.md`, `ai-packages/qa-factory/changelog.d/fv3-21b-no-stand-skill-road.md` (new) | from the FV3-21 branch head once FV3-21's builder reports K1.e (the shared functions in `waiver.py` / `manual_evidence.py` / `driver_dialog.py`) green — it IMPORTS them | the same wave W, after FV3-21 |

The owns are DISJOINT: no file is in both. The one dependency is by import (FV3-21b calls `waiver.stand_passing_word`,
`manual_evidence.no_stand_refusal`, `manual_evidence.write_case_refusal`, whose exact signatures are fixed in §2 K1.e), hence the
start order. Both merge in one wave (`tools/wave.py merge`), FV3-21 first.

Common header lines for both (the Lead prints them; never typed by hand):
- given: this card; `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md`;
  `ai-packages/qa-factory/references/human-questions.md`; `ai-packages/qa-factory/design/architecture.md` (the AR rows of §1.2/§3.2).
- non-goals: §7.
- handoff: builder report per `.claude/agents/builder.md` rule 7 + the FR walk (§9) + the witness (§8).
- designer: this file's absolute path once accepted.
- siblings: §6.

---

## 1. FV3-21 — what changes, invariants, owners

### 1.1 The defects (re-read on main)

(a) `stage_S6` (`scripts/driver_stage_s6.py:480`) reads the person's no-stand word once (`no_stand = self.s6_no_stand()`, `:519`)
and only the automation half uses it (K4 `:565`, `s6_reentry` `:585`, `s6_reprove_before_manual` `:587`).
`run_manual_block` (`:1566`) -> `manual_lane_plan` (`:1304-1336`) never reads it: it asks the gate-A-dry question
(`manual_gate_note`, `:1313`), prepares every case (`manual_plan`, `:1314`), may ask the sign-in question (`stand_login_gate`,
`:1319`), and a manual walk is then dispatched that can only fail.

(b) THE CLASS B1 (critic t-1118 Key 4, established by a run of today's code): when every manual case is refused for ANY reason
(prepare, the stand-login `go on`, `walk_refuse_gaps`, the gate-A-dry `go on`, and after (a) is fixed: the no-stand word) after the
automation runner was accepted `complete=False` (`:573`: with a consumer and a manual half the runner goes `complete=False`, so no
awaits word), `manual_close` (`:1025`) -> `consumer_need_record("S6", "manual_close")` (`:309-326`) finds the author
`S6-qa-runner-1` with no accept record and RAISES `Refusal("S6 cannot be closed at manual_close: no accept record of
qa-failure-analyst stands for S6-qa-runner-1 ...")`. Nothing in the factory ever asks the analyst for that runner: the story stops.

### 1.2 AR-n touched (rule 10; the `architecture:` line names these)

| AR | how FV3-21 keeps it | change check written into the DoD |
|---|---|---|
| AR-1 (closed variety is a data row) | the close sites that may AWAIT the consumer are a data key `await_at` of the existing table `CONSUMER_ROUTES` (`:146-156`), never a site literal in an `if` | DoD grep: the string `"manual_close"` appears in `consumer_need_record`'s body only as today's Refusal text argument (`site`), not in a comparison; positive control: the same grep finds `"await_at": ("manual_close",)` in `CONSUMER_ROUTES` |
| AR-13 (a fact with a reader is read only through it) | the no-stand word: ONE pure reader `waiver.stand_passing_word(pipeline)` (K1.a), used by `Driver.s6_stand_word` (driver) and by `story_step` (FV3-21b); the awaiting state: read only through `acceptance.awaits_acceptance` (the marker is CHECKED through it before it is written, K6) | DoD grep: `stage_overrides` and the literal `"stand not confirmed"` do not appear in new code of `driver_stage_s6.py`; positive control: the same grep finds `waiver.stand_block` in `waiver.py` |
| AR-14 (one artifact, one writer) | `{refused: {reason, door, by}}` keeps ONE writer: the file write moves from `Driver.refuse_case` into `manual_evidence.write_case_refusal` (K1.e), and `refuse_case` delegates; the S6 marker in `pipeline.json` is written by `consumer_need_record` only | K1 row W1 asserts the record bytes via `json.loads`; DoD grep: no `_write_json`/`atomic_json` on a `request.json` path anywhere in the diff except inside `write_case_refusal` |
| AR-15 (one survivor) | "the cases still to walk" through one helper `manual_todo` (used by `manual_plan` and the branch); "the live S6 dispatches" through one helper `s6_live_scopes` (used by `s6_settling_lanes` and the branch); the reason/door of the no-stand refusal through one builder `manual_evidence.no_stand_refusal` (both roads) | `manual_plan` rows of `t261_k2_...` stay green; W1 asserts site `s6.manual_close` on the second entry |
| AR-16 (text through one question form) | the `says` clause goes through `closed_question("s6.stand_confirm", ...)` like every option | K2 rows: `human_broken(text) == []` |
| AR-19 (stage twins change together) | S6's awaiting entry at `manual_close` is the twin of S7's `s7_await_scribe` (`driver_stage_s7.py:173-207`): the same marker key, the same reader, the reduction BEFORE the marker | §6 names the twin; `driver_stage_s7.py` is NOT changed (reason in §6) |
| AR-21 (what a stage gathers travels whole) | the run report is reduced (`finalize_task`) BEFORE the marker, so the analyst judges the report that holds the refused cases | W13 asserts `moves == ["finalize"]` before the marker |
| AR-22 (every field produced has a reader) | `pipeline.acceptance_awaits.S6` gets a second producer (the driver at `manual_close`); its readers already exist (`acceptance.awaits_acceptance:1496`, hence `controller.py:5591`, `:9260`, `driver_stage_s7.py:57`, `brief_pack.py:3728`, `stage_guard.py:830`) | the real-controller pin K6.T-RC asserts `next` names S7 and the analyst's dispatch is admitted |
| AR-24 (words reach the executor, whole) | the `go on` word now reaches the manual half; each refused case's `request.json` quotes the words whole (one line, whitespace squashed, never cut); the `go on` option says what it does to manual cases | W1-W5a; K2 rows |
| AR-25 (every recorded state has a way out) | (i) a new ENTRY into the existing refused-case state (`by: left_unchecked`, no-stand words), (ii) a new ENTRY into the existing "S6 awaits its consumer" state; that state has NO row in `design/state-exits.md` today (positive control of the search: `stand login missing` found at `:71`) — the row is added (defect in reach, fixed here) | `test_state_exits.py` green with both rows |
| AR-27 (a finding reaches the report under its own owner) | a case `prepare` refuses for its OWN reason keeps that record and its door (F2) | W14 |
| AR-28 (an unknown never becomes a pass) | an unreadable manual scope SAYS the clause (K2); a live or unreadable S6 dispatch state at entry = branch not taken, today's road (F1); a marker that would not make the wait hold, or an unreadable `pipeline.json`, = today's Refusal, never a close | T6, T7, W12, W13c, W13e |
| AR-29 (code judges data) | §1.3 | `test_judgment_census.py` green, no census row added or changed |

### 1.3 Checks FV3-21 adds or alters: owner and census class (AR-29, P27)

| check | owner it serves | census class | census row? |
|---|---|---|---|
| the branch "a live no-stand word stands, no stand is confirmed, no live S6 dispatch" in `manual_lane_plan` | intent (executes the person's recorded decision; judges no role output) | shape (presence of a word, of dispatch statuses) | none: no refusal transport (`refuse_case` writes a record; `plan["refused"]` is the list transport) |
| `waiver.stand_passing_word` (the reader) | data | shape | none (no refusal site) |
| the `says` clause condition in `stand_check` | intent (the person's price, FR-9) | shape | none |
| the await branch of `consumer_need_record` (an accepted, not judged author with nothing left to dispatch -> S6 awaits the consumer) | data (it routes by the presence of a record and of dispatch statuses; the JUDGMENT stays the analyst's, accepted by the tier above it — the consumer reads the runner's handoff from its own form) | shape | none today (grep of `judgment-census.json` for `consumer_need_record`: no row; its `Refusal` is a raise the scanner does not see as a unit, the census `about` blind-spot list). The branch adds NO raise: the existing raise stays the only one. If `test_judgment_census.py` reports a new unit, the builder STOPS and asks |

Commit lines: the builder's commit carries the `architecture:` line naming the AR-n of §1.2 with how each is kept, and the
`judgment:` line in the `none` form WITH its ` -- <why>` (why: the change executes a person's recorded word and routes a close by
the presence of data; the consumer's judgment of the runner's handoff is untouched). The ONLY carrier of both forms is
`tools/architecture_gate.py` (its docstring): copy the form from there, not from this card.

### 1.4 The one architectural addition (for the Lead's "does the architecture change" judgment)

(b2) adds no new mechanism: it reuses the X7-6b marker `pipeline.acceptance_awaits[<stage>] = <author's last dispatch>` that S7
already writes (`driver_stage_s7.py:201-205`) and that `acceptance.awaits_acceptance` already reads for every stage
(`acceptance.py:1494-1499`). New is only WHO may write it for S6 (`consumer_need_record` at the sites `await_at` lists). Carriers
checked for (b2), each read for this round:
- the reader honours the marker for any stage, bound to the author's last non-discounted dispatch (`acceptance.py:1471-1502`);
- the controller's dispatch gate admits the consumer role while a prior stage awaits it (`controller.py:5586-5593`), and `next`
  moves to the consumer's stage (`controller.py:9257-9261`);
- `stage_S7` reads `awaits_acceptance(state, "S6", ...)` and settles it (`driver_stage_s7.py:57-62`; with no failure it still
  dispatches the analyst: `:96-97`); `brief_pack.reviewed_dispatch_lines` names the awaited handoff (`brief_pack.py:3728`);
- after the analyst's accept record, `consumer_settled` returns and S6 "closes by it on the loop's next entry"
  (`driver_stage_s6.py:437`): S6 is re-entered, the branch refuses the same cases again (idempotent records), `manual_close` finds
  `consumer_pending("S6")` True and closes at `s6.manual_close` — the full receipt with the refused cases;
- a reject record: `consumer_settled` reworks the runner or takes the gap road (`:461-478`), as for any awaited runner;
- the real controller completes S6 by `code_only` with a manual-agent case never dispatched (`test_story_run_s6.py:546-567`).
(b2) HOLDS; no fork is returned for it.

---

## 2. FV3-21 — items (file, function, exact behaviour, test row)

### K1.a — the one reader of the no-stand word: `waiver.stand_passing_word`

File `scripts/waiver.py`, right after `stand_block` (`:378-380`). Add:

```python
STAND_STAGES = ("S5", "S6")      # the stages whose word passes the stand block: one word covers both (read in this order)


def stand_passing_word(pipeline) -> str:
    """The words of the person's live word that passes the stand block for this story; "" when a stand is confirmed (a name and
    `environment_pending` false) or no such word stands. THE one reader (AR-13, axis 26) for both roads: `Driver.s6_stand_word`
    and `story_step` (FV3-21b). Reads `split_overridden([stand_block(environment)], pipeline, stage)` over STAND_STAGES in order.
    ERROR DIRECTION: "" (no word) sends the story to the stand question; a confirmed stand is never read as "no stand";
    a pipeline that is not a dict reads "" (no word)."""
    if not isinstance(pipeline, dict):
        return ""
    environment = str(pipeline.get("environment") or "")
    if environment and not pipeline.get("environment_pending"):
        return ""
    block = stand_block(environment)
    for stage in STAND_STAGES:
        passed = split_overridden([block], pipeline, stage)[1]
        if passed:
            return str(passed[0].get("decision") or "")
    return ""
```

Update `stand_block`'s docstring callers list to "(`Driver.stand_check`, `stand_passing_word`)". In
`scripts/driver_stage_build.py:31` replace the literal by `STAND_STAGES = waiver.STAND_STAGES` (the module already imports
`waiver`); `stand_check`'s own loop (`:169-175`) stays (it prints the block and the words of the pass).

### K1.b — `Driver.s6_stand_word` and `s6_no_stand`

File `scripts/driver_stage_s6.py`, next to `s6_no_stand` (`:672`). New method:

```python
def s6_stand_word(self) -> str:
    """The words of the person's live no-stand word for this story ("" = none, or a stand is confirmed): `waiver.stand_passing_word`."""
    return waiver.stand_passing_word(self.pipeline())
```

`s6_no_stand` becomes `return bool(self.s6_stand_word())`, docstring kept plus one sentence "the words: `s6_stand_word`".
Equivalence: `contract.live_stage_overrides` drops a record whose `decision` is empty or whitespace (`contract.py:169`), so a pass
always carries words; the bool is unchanged in every world (P11 rows `test_story_run_s6.py:2463-2487` are the control).

### K1.c — `manual_todo` and `s6_live_scopes` (one predicate each, AR-15)

`manual_todo(self, cases, skip=()) -> list` next to `manual_plan` (`:926`): exactly `manual_plan`'s expression `:934-938`:

```python
again = {case for case, entry in ((getattr(self, "state", None) or {}).get("walk_retry") or {}).items()
         if isinstance(entry, dict) and entry.get("open")}
gone = (self.manual_done() - again) | {str(c) for c in skip}
return [c for c in self.manual_order(cases) if c not in gone]
```

and `manual_plan` loops `for case in self.manual_todo(cases, skip):` (its comments stay).

`s6_live_scopes(self) -> list` next to `s6_settling_lanes` (`:1641`): the predicate `:1645-1649` lifted out:

```python
import dispatch_identity
ctl = self.controller_state()
rows = dispatch_identity.records(ctl.get("dispatches") if isinstance(ctl, dict) else None)
return [{str(c) for c in r.get("scope") or [] if c} for r in rows
        if r.get("stage") == "S6" and r.get("status") in ("running", "blocked", "paused")]
```

`s6_settling_lanes` then starts `scopes = self.s6_live_scopes()` (the rest unchanged, same result). It raises with its readers, as
today. `s6_serial_reason` (`:1631`) is NOT changed (twin of `s5_serial_reason`, axis 19; §6).

### K1.d — the branch in `manual_lane_plan` (F1 recommended form, F2 second form)

POSITION: right after `waiting = self.deferred_waiting(cases)` (`:1311`) and BEFORE the `manual_gate_note` test (`:1312`).
POSITIONAL INVARIANT: under a live no-stand word with no live S6 dispatch, nothing in `manual_lane_plan` raises a `Person`
(no gate-A-dry question, no sign-in question), and the returned plan has no block (so `run_manual_block` registers and launches
nothing and goes to `manual_close`); a case a deferred question holds is never refused by the branch.

```python
words = self.s6_stand_word()
if words:
    try:
        live = bool(self.s6_live_scopes())
    except Exception:       # noqa: BLE001 - an unreadable dispatch state is an unknown: today's road this entry (AR-28)
        live = True
    if not live:
        return self.manual_no_stand(cases, waiting, words), waiting
    print("S6: no stand is confirmed and the person said to go on, but an S6 walk is under way or stopped; the manual half "
          "goes on as before this entry, and the person's word is applied at the next entry")
```

New method `manual_no_stand(self, cases, waiting, words) -> dict` (home `driver_stage_s6`, after `manual_lane_plan`), returns
the plan always (no None):

1. `import manual_evidence as ME`; `reason, door = ME.no_stand_refusal(words)` (K1.e).
2. `plan = {"blocks": [], "refused": [], "unprepared": []}`.
3. For each `case` of `self.manual_todo(cases, skip=[c for c, _n in waiting])`:
   - `got = self.manual_prepare(case)`; `why = got[1]`;
   - if `why` (prepare refused it for its OWN reason, F2): `plan["refused"].append((case, why))` and
     `print(f"S6: {case}: not checked by hand — {why}")`; its `request.json` keeps prepare's record (no second write);
   - else (prepared, or unprepared by the factory): `self.refuse_case(plan, case, reason, door, "left_unchecked")` and
     `print(f"S6: {case}: not checked by hand — not checked by an agent: no stand is confirmed for this story; the person said: "
     f"\"{self.s0_quote(words)}\"")`.
4. `self.walk_assign_clear()` (an earlier entry's assignment is settled, as the old road does when it makes none).
5. Return `plan`.

`run_manual_block` is unchanged: `plan["blocks"] == []` -> `manual_close(cases, plan["refused"])` (`:1581-1583`); `manual_close`
refuses the waiting cases itself with its deferred reason (`:1036-1039`), so a waiting case is refused ONCE.

### K1.e — the shared homes both roads read (B2(2))

File `scripts/manual_evidence.py`, after `_write_refused` (`:1272`). Exact signatures (FV3-21b imports them):

```python
NO_STAND_DOOR = "record a stand for this project with the onboarding; the next run checks it by hand"


def no_stand_refusal(words) -> tuple:
    """`(reason, door)` of a manual-agent case left unchecked by the person's no-stand word, for BOTH roads (the driver's
    `manual_no_stand`, `story_step start`): the words on one line, whitespace squashed, every character kept, never cut (AR-24)."""
    said = " ".join(str(words or "").split())
    return f"not checked by an agent: no stand is confirmed for this story; the person said: \"{said}\"", NO_STAND_DOOR


def write_case_refusal(task_root, case, reason, door, by, by_first=False) -> bool:
    """THE writer of `{"refused": {reason, door, by}}` in a case's request.json (AR-14), for both roads; `Driver.refuse_case`
    delegates its file write here. `by_first` keeps the key order of the one driver caller that wrote `by` before `door`.
    True when written; False when the write failed (OSError), nothing raised."""
    record = {"reason": reason, "by": by, "door": door} if by_first else {"reason": reason, "door": door, "by": by}
    try:
        path = request_path(task_root, case)
        path.parent.mkdir(parents=True, exist_ok=True)
        atomic_json(path, {"refused": record})
    except OSError:
        return False
    return True
```

File `scripts/driver_dialog.py`, `refuse_case` (`:227-241`): keep the `plan` append; replace the record/`_write_json` lines by
`return ME.write_case_refusal(self.task_root, case, reason, door, by, by_first)`. Bytes on success are unchanged (both publish
through `event_store.atomic_json`). Docstring: "the file write is `manual_evidence.write_case_refusal`, the one writer".

The door drops "and confirm it" (F5; the owner's word 17.11.2026: a stand we are given is a ready test stand unless the person
says otherwise — a confirmation step is not owed).

### K1 — test row (one parameterised scenario in `scripts/tests/test_story_run_s6.py`)

New function `fv3_21_the_stand_word_reaches_the_manual_half`, registered in `main()` next to
`hf2_11b_without_a_stand_nothing_is_run_or_proved`. Rig: `d2_seed(task, environment=..., pending=...)`, `d2_pipeline(task_root,
stage_overrides=...)`, `manual_rig(root, env, task, cases, refused=...)`, `enter_manual(driver, world, cases)`;
`driver.close_by_code` wrapped to record `site` (as `reprobe_rig` does, `:2142`); `driver.manual_prepare` wrapped to count calls.
`WORD = {"stage": "S6", "match": "stand not confirmed", "decision": "go on", "at": "2026-11-17T10:00:00+00:00", "by": "human"}`.
Expected texts are LITERALS in the test (never derived from the source):
`REASON = 'not checked by an agent: no stand is confirmed for this story; the person said: "go on"'`,
`DOOR = "record a stand for this project with the onboarding; the next run checks it by hand"`.

Branch-taken worlds (each asserts: `launched == []`; no new key in `world.dispatches`; `manual_prepare` called once per todo case;
no `Person` raised; `c16b_refused_by(task_root, cases) == ["left_unchecked"] * n`; each request's `refused == {"reason": REASON (or
the words variant), "door": DOOR, "by": "left_unchecked"}`; `[m[0] for m in moves] == ["finalize", "code_only", "stage_done"]`;
sites `== ["s6.manual_close"]`; printed `S6: <case>: not checked by hand — not checked by an agent: no stand is confirmed`):

| row | world |
|---|---|
| W1 | `environment=None, pending=True`, `WORD` on S6, cases `[TC_001, TC_002]` (FIRST check = `launched == []`) |
| W2 | as W1, the word on S5 (`stage: "S5"`) |
| W3 | `environment="Local", pending=True` (named, not confirmed), `WORD` on S6 (Lead decision E2; see §OQ) |
| W4 | as W1, `decision = "go on\n  " + chr(0xE9) + " later"`: reason quotes `go on ` + chr(0xE9) + ` later` on one line |
| W5 | as W1, `decision` = 2 000 characters: the reason holds all of it; the console line ends with `driver.CUT` |
| W5a | as W1, `decision` = exactly `driver.QUOTE_LIMIT` characters (no whitespace): the console line holds all of them and does NOT end with `driver.CUT`; the reason is whole (F4) |
| W6 | as W1, `match: "*"` on S6 (a pass of every S6 block is the stand word too, as `stand_check` reads it) |

Case-level rows (W1's world unless said):

| row | world | expected |
|---|---|---|
| W7 | `world.dispatches["S6-qa-runner-1"] = {"stage": "S6", "role": "qa-runner", "status": "accepted", "execution_kind": "manual", "manual_case_ids": ["TC_003"], "scope": ["TC_003"]}`, plus `record_failure_analyst_accept(driver, "S6-qa-runner-1")`; cases `[TC_001, TC_002, TC_003]` (F-3 correction of the critic) | `TC_003` has no `refused` written; the close reason holds `1 case(s) checked by an agent by hand, 2 not checked` |
| W8 | `driver.state["deferred"] = [{"n": 1, "kind": "walk_account", "holds": ["TC_002"]}]` | `TC_002` refused ONCE, reason `not checked yet: it waits for your answer to question 1, asked before gate B` (never `REASON`); `manual_prepare` not called for it |
| W12 | `world.dispatches["S6-qa-runner-5"] = {status: "running", stage: "S6", scope: ["TC_002"], execution_kind: "manual"}` (F1: a live S6 dispatch at entry) | call `driver.manual_lane_plan([TC_001, TC_002])`: NO request holds `REASON`; the printed line holds `an S6 walk is under way or stopped`; today's road ran (`manual_prepare` called) |
| W12b | as W12 with `scope: []` | same as W12 |
| W12c | `driver.s6_live_scopes = lambda: (_ for _ in ()).throw(RuntimeError("state down"))` | same as W12 (unknown = today's road) |
| W13 | an ACCEPTED automation author with no record and no awaits word: `world.dispatches["S6-qa-runner-1"] = {"stage": "S6", "role": "qa-runner", "status": "accepted", "execution_kind": "automation", "scope": ["TC_900"]}`; cases `[TC_001, TC_002]` (B1) | first entry: no Refusal, no Person; `[m[0] for m in moves] == ["finalize"]` (reduced, NOT closed); `pipeline.json` `acceptance_awaits == {"S6": "S6-qa-runner-1"}`; printed `S6: nothing is left to dispatch; S6 awaits the acceptance of qa-failure-analyst for S6-qa-runner-1`; both requests hold `REASON`. Then `record_failure_analyst_accept(driver, "S6-qa-runner-1")` and enter again: moves end `["finalize", "code_only", "stage_done"]`, site `s6.manual_close`, reason holds `0 case(s) checked by an agent by hand, 2 not checked` |
| W13b | as W13 but every case refused by prepare (`manual_rig(..., refused=cases)`) and NO stand word (C2-style world with a confirmed stand: `environment="Local", pending=False`) — the class sibling "prepare refused all" | same as W13 first entry (marker, no Refusal), the requests hold prepare's reasons |
| W13c | as W13 plus a NEWER `S6-qa-runner-2` `status: running` (registered after runner-1); call `driver.manual_close([TC_001], [])` directly | `Refusal` whose text holds `no accept record of qa-failure-analyst stands for S6-qa-runner-1`; `pipeline.json` holds no `acceptance_awaits` (the marker would not hold: error direction) |
| W13d | as W13 plus a live person's pass `{"stage": "S6", "match": "stage acceptance", "decision": "accept the run", "at": <a time after the runner's acceptance>, "by": "human"}` in `stage_overrides` | no marker; the close goes on (moves end `stage_done`): a person's word is never overruled by an await |
| W13e | as W13 with `driver.pipeline = lambda: {}` (unreadable) for the close | `Refusal` as W13c; `pipeline.json` bytes unchanged (hash before/after) |
| W14 | W1 with `manual_rig(..., refused=[TC_002])` (prepare refuses TC_002 for its own reason) (F2) | `TC_002`'s request holds the rig's refusal (no `by`, not `REASON`); printed with that reason; `TC_001` holds `REASON` |
| W14b | W1 with `driver.manual_prepare` returning `(["OB-x"], "", "factory failed")` for TC_002 (unprepared) | `TC_002` holds `REASON` (nothing is walked) |

Branch-not-taken worlds (control; each asserts exactly one manual dispatch as today, and no request holds `REASON`):

| row | world |
|---|---|
| C1 | `environment="Local", pending=False` (confirmed) with `WORD` on file |
| C2 | `environment=None, pending=True`, no word (`stage_overrides=[]`) |
| C3 | `WORD` with `revoked_at` set |
| C4 | `WORD` with `stage: "S4"` |
| C5 | `stage_overrides = "broken"` (not a list) |
| C6 | `WORD` with `match: "stand login missing"` |

(C2-C6 enter `run_manual_block` directly: they prove the BRANCH is not taken. That `stand_check` asks before S6 runs anything in
those worlds is pinned by the P11 controls `test_story_run_s6.py:2483-2487`.)

PROBES (each by byte copy, hygiene point 7, hash comparison in the witness): (p1) delete the `return self.manual_no_stand(...)`
line -> W1's first check goes red; (p2) pass `skip=()` in step 3 -> W8 goes red; (p3) replace the `await_at` membership test by
`False` -> W13 goes red with the Refusal text.

### K2 — the stand question says what `go on` does to the manual cases

File `scripts/driver_stage_build.py`.

**K2.a** `stand_question_text` (`:38`) gains a keyword `manual: bool = False` (last parameter; every current caller and test
keeps its bytes). The `go on` option (`:129-131`) becomes:

```python
options.append({"answer": "go on", "token": "go on",
                "says": "go on without a stand" + ("; the tests are still written, but none is run on a stand" if stage == "S5" else "")
                        + ("; an agent checks no case by hand" if manual else "")
                        + ", and the story carries a line saying it was your decision"})
```

Exact texts: S6 manual: `go on without a stand; an agent checks no case by hand, and the story carries a line saying it was your
decision`; S5 manual: `go on without a stand; the tests are still written, but none is run on a stand; an agent checks no case by
hand, and the story carries a line saying it was your decision`; `manual=False`: today's text byte for byte. The clause claims no
count, so it is true in every world it is said in (FR-41).

**K2.b** `stand_check` (`:139`), on the question path ONLY (right before `site_seam_person`, `:201`) (F3 applied):

```python
try:
    got = self.stage_scope("S6", "manual")
    scope = got.get("scope") if isinstance(got, dict) else None
    manual = not isinstance(scope, list) or bool(scope)
except Exception:      # noqa: BLE001 - a doubt says the clause (the person's price, FR-9); the clause is true in every world
    manual = True
```

and pass `manual=manual` to `stand_question_text`. POSITIONAL INVARIANT: a confirmed stand, a passed word and a probe that exits 0
return BEFORE this line, so they cost no controller call; only a question about to be raised reads the scope.

**Test row K2** — extend `c16b_stand_confirm_is_priced_and_its_answers_have_executors` (`test_story_run_s6.py:1804`) with one table:

| row | call | expected `go on` line |
|---|---|---|
| T1 | `stand_question_text("S6", "Local", ["Local"], "manual", manual=True)` | holds `an agent checks no case by hand` |
| T2 | same with `manual=False` | does not hold it; equals today's text |
| T3 | `stand_question_text("S5", "", [], manual=True)` | holds `none is run on a stand; an agent checks no case by hand, and the story` |
| T4 | `stand_check("S6", "automation")` with `driver.stage_scope = lambda s, k="": {"scope": ["TC-2"]}` | the raised Person's text holds the clause |
| T5 | as T4 with `{"scope": []}` | no clause |
| T6 | as T4 with `stage_scope` raising `Refusal` | clause said |
| T7 | as T4 with `{"stage": "S6"}` (no `scope` key) (F3) | clause said |

Every row also asserts `human_broken(text) == []` and `c16b_price_lines(text, n)` unchanged. PROBE: `if manual` -> `if False`:
T1 red. Census of question texts: `test_human_questions.py` calls `stand_question_text` positionally without `manual` -> unchanged;
its `stand_check("S5")` row patches `driver.py` so `stage_scope` raises inside the new `try`; it checks only `offered` and
`answer_note` -> unchanged. `test_story_run_words.py` (`UPSTREAM_INLINE_DECISION_SITES = 2`): no new words-carrying command ->
unchanged.

### K3 — `known_red.json`: `main/S6` leaves; the next stop is measured; the pin stays 1

File `scripts/tests/fixtures/driver-exits/known_red.json` (read ONLY by `scripts/tests/known_red.py`). After K1-K6 the builder runs
`python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part main` in its worktree.
EXPECTED from the decided road (B1 = b2): S6's manual half takes the branch (the dry world has no stand and the person's `go on`,
t-1106), every manual case is `left_unchecked`, `manual_close` reduces and writes `acceptance_awaits.S6 = S6-qa-runner-1`, `next`
names S7, and the dry pass STOPS AT S7 at the missing `qa-failure-analyst@S7` stub row. The builder:
1. removes the `main/S6` row;
2. writes ONE new row keyed by the walk-row id the run prints for the S7 stop, `{node, raised_by, note}`: `raised_by` QUOTES the
   measured stop line verbatim and names this card (FV3-21); `node` = the node the Lead names for the S7 analyst stub before
   FV3-21 merges (F-5, axis 18); until named: `FV3-21` with `note: "the owning node of the S7 analyst stub is owed (Lead)"`;
3. keeps `pins.known_red` at 1.
If the stop is anywhere else than that S7 analyst stub (in particular a Refusal at S6), the builder writes no row and returns the
measured line as a question. Control: `test_field_producers.py` `red_rows_equal_the_known_red_ledger` (`:1529`) green.

### K5 — `design/state-exits.md`: two rows (AR-25 change check; F7 applied)

(i) Insert right after the stand-login row (`:71`), same table, same shape:

`| manual-agent cases left unchecked by the person's no-stand word (\`stand not confirmed\` in \`stage_overrides[]\` for S5 or S6 while no stand is confirmed; their \`request.json\` then holds \`{refused: {reason, door, by: left_unchecked}}\` with the person's words; a case \`prepare\` refused keeps its own record) | the person's answer \`go on\` to the stand question, recorded by \`waiver.py --stage S5\` or \`--stage S6 --block "stand not confirmed"\`; the driver refuses the cases at its S6 manual entry when no S6 walk is under way, before anything is asked or dispatched (the skill road: \`story_step.py start --execution-kind manual\`) | a stand recorded for the project and confirmed by the stand check, or \`waiver.py --revoke --stage S6 --block "stand not confirmed"\` (or \`--stage S5\`; the stand question speaks again): either takes effect in the NEXT run of the story — S6, once closed, does not reopen by itself; within the closed story the person's word at gate B carries the cases as not checked by hand | \`test_story_run_s6.py\`, \`test_state_exits.py\` |`

(ii) Insert as the last row of the same table (after the `first_look_continue` row, `:76`):

`| a stage awaits its consumer (\`pipeline.acceptance_awaits[S6 or S7]\` names the author's last dispatch, or that dispatch finished with the open-work word \`stage_awaits_acceptance\`; read only by \`acceptance.awaits_acceptance\`; S6 is judged by the failure analyst, S7 by the doc scribe) | the author's finish with \`--not-complete --unresolved stage_awaits_acceptance\`; the driver's marker: S7 after its repairs (\`s7_await_scribe\`), S6 at \`manual_close\` when nothing is left to dispatch and the runner's last accepted dispatch has no accept record | the consumer's accept record (\`stage_done.py --task <T> --stage <S> --acceptance work/handoffs/<consumer dispatch>.yaml\`): the stage closes at its next entry; a reject record: the author's repair round or the gap road; the person's word \`waiver.py --task <T> --stage <S> --block "stage acceptance"\`; a newer running author dispatch ends the wait | \`test_story_run_s6.py\`, \`test_state_exits.py\` |`

Test: `test_state_exits.py` (checks every door the walk names exists).

### K6 — the class fix B1 = (b2): `consumer_need_record` routes S6 to await the consumer at `manual_close`

File `scripts/driver_stage_s6.py`.

**K6.a** `CONSUMER_ROUTES` (`:146-156`): add `"await_at": ("manual_close",)` to the S6 row and `"await_at": ()` to the S7 row
(S7 keeps its own road `s7_await_scribe`). Comment: "the close sites where a missing record means AWAIT the consumer, not refuse
(B1, t-1128): nothing is left to dispatch there, so no other road would ever ask the consumer".

**K6.b** `consumer_need_record(self, stage, site) -> bool` (`:309-326`). Same signature (two positional args — callers and test
stubs that pass two args keep working); returns False wherever it returns today; the new branch sits right BEFORE the `raise`:

```python
route = self.CONSUMER_ROUTES.get(stage) or {}
if site in route.get("await_at", ()):
    pipeline = self.pipeline()
    if isinstance(pipeline, dict) and pipeline:
        marks = pipeline.get("acceptance_awaits") if isinstance(pipeline.get("acceptance_awaits"), dict) else {}
        marked = dict(pipeline, acceptance_awaits=dict(marks, **{stage: author}))
        if acceptance.awaits_acceptance(state, stage, marked) == author:
            if acceptance.awaits_acceptance(state, stage, pipeline) != author:
                from event_store import atomic_json
                atomic_json(self.task_root / "pipeline.json", marked)
            print(f"{stage}: nothing is left to dispatch; {stage} awaits the acceptance of {consumer} for {author} "
                  f"(the {route.get('who', 'consumer')} is let in; its record closes {stage})")
            return True
raise Refusal(...)        # today's text, unchanged
```

Docstring gains: "At a site the route's `await_at` lists (S6 `manual_close`), a missing record makes the stage AWAIT the consumer
instead of refusing (B1): the marker `pipeline.acceptance_awaits[stage] = author` is written only when `awaits_acceptance` (the one
reader) would then name exactly `author`, and only over a readable pipeline; otherwise today's Refusal. True = the stage awaits;
nothing is closed."

POSITIONAL INVARIANT: the branch comes AFTER `consumer_pending` and `consumer_person_pass` (a record or a person's word always wins
and the close goes on), and BEFORE the raise (it replaces the raise only when the wait demonstrably holds). A stage with a consumer
is never closed without the record or a person's pass.

**K6.c** `manual_close(self, cases, refused)` (`:1025-1046`): new ORDER (the docstring says it):
1. the deferred-waiting refusals (`:1036-1039`, unchanged lines);
2. `finalize_task.py` and its Refusal on failure (`:1042-1044`, moved up);
3. `if self.consumer_need_record("S6", "manual_close"): return` (moved down from `:1030`);
4. `gone`/`done`/`reason` and `close_by_code(...)` as today.
POSITIONAL INVARIANT: the marker is written only over a run report the reducer has just written (AR-21, the S7 twin's B3 order);
a reducer failure writes no marker and closes nothing.

**K6 error direction (a reused function in a more consequential role: a gate that refused becomes a router).** It may err toward
REFUSING (today's Refusal) whenever it cannot show the wait holds; it must never err toward CLOSING without a record or a pass.
Adversarial inputs that stay on the safe side: a newer running/blocked/paused author dispatch (W13c: the reader names no awaiting
author -> Refusal); an unreadable or empty `pipeline.json` (W13e -> Refusal, file unchanged); a marker already present for the same
author (no second write, True); a marker for an EARLIER author dispatch (the reader binds to the last one; overwritten with the
current author); the author's own awaits word already present (True, no write); a person's live `stage acceptance` word written
after the acceptance (W13d: the pass is recorded, the close goes on); no consumer in the table (`consumer_of` "" -> False, today);
a reject record for the author (`consumer_pending` False -> marker; `stage_S7`'s `consumer_settled` then reworks or takes the gap
road, as for every awaited runner); `site` not in `await_at` (`s6_reentry`, `s6_reprobed_close`, S7's `s7_close`: today's Refusal).

**Real-controller pin T-RC** — extend `t261_the_real_controller_refuses_a_completion_over_an_undispatched_case_and_takes_the_code_only_receipt`
(`test_story_run_s6.py:546`) with a SECOND world in the same function (fresh `harness.temp_dir`, `c2 = F.s6_story(root2)`):
`F.runner(c2, root2, "S6-auto", "automation", ["TC-1"], False)` (accepted not-complete, no record, no awaits word). Assert:
(1) `acceptance.awaits_acceptance(c2.state(), "S6", <pipeline without marker>) == ""` (control: today nothing awaits);
(2) write `acceptance_awaits = {"S6": "S6-auto"}` into `root2 / "pipeline.json"` (read it first when present, utf-8-sig JSON dict,
else `{}`); then `awaits_acceptance(...) == "S6-auto"` and `c2.next_action().get("stage") == "S7"`;
(3) `c2.apply("dispatch", {"id": "S7-qa-failure-analyst-1", "stage": "S7", "role": "qa-failure-analyst", "scope": ["TC-1"],
"input_hash": "s7", "budget": {}, "known_paths": {}, "idempotency_key": "d-an1"})` is NOT refused (no `required prior logical stage
incomplete`). Control in the same world: the same dispatch with `"role": "qa-doc-scribe"` IS refused.

### K7 — `driver-layers.json` rows for the new names

File `scripts/tests/fixtures/driver-layers.json`. Next to `Driver.s6_no_stand` (`:646`), kind `method`, home `driver_stage_s6`,
row 74: `Driver.s6_stand_word` (note: "FV3-21: the words of the person's no-stand word (waiver.stand_passing_word); s6_no_stand is
its bool"). Next to `Driver.manual_plan` (`:655`), row 75: `Driver.manual_todo` ("FV3-21: the cases still to walk, manual_plan's
expression, shared with manual_no_stand"), `Driver.manual_no_stand` ("FV3-21: the manual half under the person's no-stand word:
prepare, keep prepare's own refusals, the rest left_unchecked in the person's words; no block"). Next to `Driver.s6_settling_lanes`
(`:1038`): `Driver.s6_live_scopes` (no row number, as its neighbour; note "FV3-21: the scopes of running, blocked or paused S6
dispatches; read by s6_settling_lanes and manual_lane_plan"). Test: `test_driver_layers.py`.

### K8 — changelog fragment

New `changelog.d/fv3-21-no-stand-manual-half.md`, ASCII, two bullets in the style of `changelog.d/fv1-5-stand-check-words.md`:
(1) with the person's `go on` on the stand question (no stand confirmed), the manual-agent cases of S6 are no longer dispatched to
a walk that cannot run: each is recorded as not checked by hand with the person's words and the door "record a stand for this
project with the onboarding; the next run checks it by hand" (a case the preparation refused keeps its own reason), and the
stand question's `go on` says so when the story has such cases; (2) when nothing is left to dispatch in S6's manual half and the
runner's work has no acceptance record yet, S6 now waits for the failure analyst's acceptance instead of stopping with a refusal.

---

## 3. FV3-21 — edges: every row decided, with the invariant it protects

WHOLE-CARD INVARIANTS: **(I-1) no manual walk is dispatched by the branch under a person's word that declined the stand, and the
branch never writes the request of a case a live S6 dispatch may carry (it is not taken while any S6 dispatch is live). (I-2) A
stage with a consumer is never closed without the consumer's record or a person's pass; a story whose manual half has nothing
left to dispatch is never stopped by a Refusal when the wait for the consumer can hold.**

| # | edge | behaviour | invariant protected | where |
|---|---|---|---|---|
| E1 | no stand + `go on` (word on S5 or S6, environment empty) | branch: prepare, no question, no dispatch; cases `left_unchecked` with the words; `manual_close` | I-1 (FR-36) | W1, W2 |
| E2 | stand named, `environment_pending` true + `go on` | the same branch (Lead decision, FR-36; the option chosen says "go on without a stand") — **§OQ point 2** | I-1 | W3 |
| E3 | no stand + `stop` | no word recorded: `stand_check` raises before S6 runs; nothing is written | the branch never acts without a recorded word | C2 + P11 controls |
| E4 | confirmed stand, any words on file | `stand_passing_word` "" -> today's road | a walk that CAN run is never refused by the branch | C1 |
| E5 | a manual-human case | not in the manual scope (`stage_scope` `manual` = manual-agent only); untouched | the branch refuses only what the factory would have walked | by construction |
| E6 | a case done by an accepted manual dispatch (earlier life or entry) | stays done (`manual_todo` = `manual_plan`'s formula) | an accepted record is never overwritten by a refusal | W7 |
| E7 | a case a deferred question holds | not prepared, not refused by the branch; `manual_close` refuses it once with its deferred reason | one open question per case; one refusal per case | W8 |
| E8 | a consumer and an accepted author dispatch with no record (the dry world; B1 DECIDED = b2) | `manual_close` reduces, then `consumer_need_record` writes `acceptance_awaits.S6 = <author>` (only if the reader would then name it) and returns; S7's analyst judges the runner's handoff; after its accept record S6 re-enters and closes at `s6.manual_close` with the full receipt; a reject record -> rework / gap road | I-2 | W13, W13c-e, T-RC |
| E9 | word on S5 vs S6 | both count; S5 read first (`STAND_STAGES` order) | one word covers both stages | W2 |
| E10 | environment empty vs pending | empty -> the word decides; named + pending true -> the word decides; named + pending false/absent -> confirmed, never no-stand | the same reading as `stand_check:167` | W1, W3, C1 |
| E11 | a word for another stage (S4, S7) | not a word -> branch not taken | an unrelated word never declines the stand | C4 |
| E12 | `stage_overrides` broken / revoked / empty decision / placeholder match | no pass -> branch not taken; `stand_check` asks (AR-28) | an unreadable word is no word | C3, C5 |
| E13 | a `*` pass on S6 | counts (it passes the stand block in `stand_check` too) | one reader, one reading | W6 |
| E14 | the person's words: multi-line, non-ASCII, very long, exactly at `QUOTE_LIMIT` | request reason: one line, every character kept, never cut; console line: `s0_quote` (cut only BEYOND `QUOTE_LIMIT`) | the words reach the record whole (AR-24) | W4, W5, W5a |
| E15 | TEMPORAL — a story whose earlier life already dispatched a manual block before this code existed | (a) block accepted -> its cases stay done (E6); (b) any S6 dispatch running/blocked/paused at entry, whatever its scope -> branch NOT taken this entry, one printed line, today's road (which may register a lane, as today — not a regression; F1); (c) the dispatch state unreadable -> same as (b); (d) the next entry with no live S6 dispatch takes the branch | I-1: the branch never writes a request a live walk may carry | W12, W12b, W12c |
| E16 | TEMPORAL (rule 11 i) — artefacts this card brings into existence: the `says` clause, the two state-exits rows, `acceptance_awaits.S6` written by the driver, `waiver.STAND_STAGES` | before: no clause; S6 stops with the manual_close Refusal; after: the clause only when the S6 manual scope is non-empty or unreadable; S6 awaits the analyst. A story stopped TODAY at the manual_close Refusal: its next driver entry reaches `manual_close` again and now awaits (no re-ask). Stories that recorded the word before the upgrade get the branch at their next S6 manual entry; nothing re-asks them (D-0047) | a person is never asked again for a word they gave; a stopped story resumes by the new road | K2 T1-T7; W1; W13 |
| E17 | conflicting pair: K1 refuses while K2's `says` was not shown (word recorded before the upgrade, or by the conductor from free words) | the branch applies the word (D-0047); printed line and record say it was the person's word; the door names the way back | the word moves the factory (P13); its consequence is said | W1 |
| E18 | manual scope non-empty, all refused, automation half not yet run | the automation runner still goes first (`:520-583`); the manual half closes on the re-entry (non-goal 7.2) | the automation half is untouched | non-goal |
| E19 | a `write_case_refusal` write fails (OSError) | False returned; the printed line still names the case; `manual_close`'s receipt still lists it | a failed write never stops the close nor hides the case | by construction |
| E20 | a case `prepare` refuses for its OWN reason (scope, P20 "expectation unconfirmed — Q-n", no current gate A, gate A recorded dry) (F2) | it keeps prepare's record and door, printed with its reason, listed in `plan["refused"]`; NOT overwritten by the no-stand refusal | AR-27: a finding reaches the report under its own owner; FR-2: the door is the real door | W14 |
| E21 | a case the FACTORY failed to prepare (unprepared marker) | refused with the no-stand reason (nothing is walked under the word) | I-1 | W14b |
| E22 | the gate-A-dry world under the word | `manual_gate_note` is not reached (the branch comes first): no gate-A question; each case keeps prepare's gate-A reason (E20) | no question about cases that will not be walked; the gate-A reason stays the case's own | W14 (shape) |
| E23 | (b2) siblings — every case refused by prepare / by the stand-login `go on` / by `walk_refuse_gaps` / by the gate-A-dry `go on`, after an accepted not-complete runner | all reach `manual_close` -> the same await (one change at the one site) | I-2, class-wide | W13b (prepare); the others share the site — no separate row (one site, one behaviour) |
| E24 | `--dry-run` (`self.dry`) reaching `manual_close` with no record | the marker is written as S7's twin writes it today (no dry exception on either twin); see fork R2-F3 | twin parity (axis 19) | fork |

### 3.1 `s6_no_stand` / `stand_passing_word` in a more consequential role (advice -> the branch that decides not to dispatch)

Before: `s6_no_stand` only changed what the automation half PROBES (K4). Now its words decide that no manual walk is dispatched.
ERROR DIRECTION tolerated: toward NOT dispatching only when a live word stands, no stand is confirmed and no S6 dispatch is live;
cost: a case left unchecked with a door back. Toward dispatching: only when the state cannot be read or a walk is already live
(today's road, said in one line). A false "no stand" over a CONFIRMED stand is unreachable (first `return ""`).
Adversarial inputs (each decided above): revoked word (E12); word on another stage (E11); word for another block (C6); placeholder
match, empty decision (E12); `*` (E13, counts); confirmed stand with words (E4); named + pending (E2); broken overrides (E12);
S5-only word (E9, counts); a pipeline that is not a dict (`""`).

---

## 4. FV3-21b — the skill road says the same and does the same (B2)

### 4.1 Defect and scope

On the skill road the orchestrator starts a manual block with `story_step.py start --execution-kind manual --scope <ids>`
(`phases/s6.md:10`). `story_step._manual_block_check` (`scripts/story_step.py:1005-1074`) prepares each case through
`manual_evidence.prepare_for_block` and refuses a block whose cases prepare refused, but reads no stand word (a case-insensitive
`stand` grep over `story_step.py` finds only unrelated lines; the critic's control: 19 lines, all unrelated). So under the
person's `go on` the skill road prepares and dispatches a walk that can only fail.
FV3-21b brings the SAME refusal to the skill road: same reader, same reason/door, same record writer (all from FV3-21 K1.e).
The CLOSE of an all-refused manual half on the skill road does not exist today for ANY refusal reason (§4.5, fork R2-F1); it is
node FV3-21c, not this card.

### 4.2 AR-n, owners, census

| AR | how kept | change check |
|---|---|---|
| AR-13 | the word through `waiver.stand_passing_word` only | DoD grep: no `stage_overrides` / `"stand not confirmed"` literal in the diff of `story_step.py`; positive control: the same grep finds `MODE_SWITCH = waiver.MODE_SWITCH_BLOCK` (`:701`) |
| AR-14 | the record through `manual_evidence.write_case_refusal` only | DoD grep: no `atomic_json`/`write_text` on a request path in the diff |
| AR-15 / P31 | reason and door from `manual_evidence.no_stand_refusal`, the driver's own builder | row S1 asserts byte-equal reason/door with the driver's W1 literals |
| AR-9 (a refusal names its door) | the refusal's last line is a `door:` line naming what the person can do | row S1 |
| AR-24 | the words whole in the record | S1, S3 |
| AR-27 | prepare's own refusal keeps its record | S4 |
| AR-28 | no word / confirmed stand / unreadable pipeline -> today's start | S5-S7 |
| AR-29 | the new branch: owner intent, class shape; it returns refusal LINES with exit 2 from `_manual_block_check` exactly like the existing branches — if `test_judgment_census.py` reports a new unit or a changed class, the builder STOPS and asks | census test green |

Commit lines: as §1.3 (the `architecture:` line naming AR-9, AR-13, AR-14, AR-15, AR-24, AR-27, AR-28, AR-29; `judgment: none -- <why>`),
form from `tools/architecture_gate.py`.

### 4.3 Items

**K4.b1** `scripts/story_step.py`, `_manual_block_check`, the `kind == "manual"` road. POSITION: after
`validate_manual_runner_block` succeeds (a malformed block is refused as today, first) and in place of the plain prepare loop
`:1059-1066`. POSITIONAL INVARIANT: under a live no-stand word, `start` writes no dispatch, no stamp, no brief (it returns before
anything is written, as every refusal of this function does) and every case of the block has a refused record afterwards.

```python
import manual_evidence
words = waiver.stand_passing_word(<the story's pipeline.json, read with the module's existing pipeline reader — the one `_next` uses>)
if words:
    reason, door = manual_evidence.no_stand_refusal(words)
    lines = []
    for case in block:
        why = manual_evidence.prepare_for_block(_task_root(args.task), case)[1]
        if why:                                     # prepare refused it for its own reason: that record stays (AR-27)
            lines.append(f"{case}: not checked by hand - {why}")
        else:
            manual_evidence.write_case_refusal(_task_root(args.task), case, reason, door, "left_unchecked")
            lines.append(f"{case}: not checked by hand - {reason}")
    return None, ["story_step: refused - no case is checked by an agent by hand: no stand is confirmed for this story and the "
                  "person said to go on", *lines,
                  f"door: {door}; or the person's word is taken back: "
                  f"waiver.py --task {args.task} --revoke --stage S6 --block \"stand not confirmed\""], 2
```

If the builder finds no existing pipeline reader in `story_step.py`, it STOPS and asks (no new reader is invented).

**K4.b2** `skills/qa-story/phases/s6.md`. Card line 5, after `already covers this stage`, insert: `; with that word \`start
--execution-kind manual\` dispatches no case: each is recorded as not checked by hand, in the person's words (a case the
preparation refuses keeps its own reason)`. § "The stand, before the first dispatch" (`:22-28`), after `already covers this stage
— do not ask again`, the same sentence. The sentence claims NOTHING about how S6 then closes (FV3-21c).

**K4.b3** changelog `changelog.d/fv3-21b-no-stand-skill-road.md`, ASCII, one bullet: the skill road's manual `start` now records
each case as not checked by hand in the person's words under the no-stand word, as the driver does, and dispatches nothing.

### 4.4 FV3-21b test rows (one table added to `scripts/tests/test_story_step_manual_block.py`)

New function `fv3_21b_the_stand_word_on_the_skill_road`, registered in `main()` (`:749`), over `real_story(root, MIXED_7)` and
the module's `start(root, ctl, scope, kind="manual", prepare=...)` helper; the word is put into the story's `pipeline.json` as
`stage_overrides` (`WORD` of K1, `environment` absent, `environment_pending: true`). Literals `REASON`/`DOOR` as in K1.

| row | world | expected |
|---|---|---|
| S1 | WORD, scope `TC-2,TC-3`, prepare ready for both | exit 2; text holds `no case is checked by an agent by hand`, `TC-2: not checked by hand - ` + REASON, the `door:` line holds DOOR and `--revoke --stage S6`; both requests `json.loads == {"refused": {"reason": REASON, "door": DOOR, "by": "left_unchecked"}}`; `c.state()["revision"]` unchanged (nothing dispatched) |
| S2 | as S1, the word on S5 | as S1 |
| S3 | `decision` = `"go on\n " + chr(0xE9)` | the reason holds `go on ` + chr(0xE9) on one line |
| S4 | as S1, prepare refuses TC-3 for its own reason | TC-3's line holds that reason; TC-3's request is prepare's (no `by`); TC-2 holds REASON |
| S5 | confirmed stand (`environment: "Local"`, `environment_pending: false`) + WORD (control) | today's behaviour: block accepted (registered), no REASON anywhere |
| S6 | no word (control) | today's behaviour |
| S7 | WORD revoked (`revoked_at`) (control) | today's behaviour |

PROBE (byte copy): delete `if words:` branch's `return` -> S1 red.

### 4.5 FV3-21c — the residual of the P31 class, a named node (fork R2-F1 decides its timing)

Evidence: on the skill road an S6 manual half whose cases are ALL refused (by prepare today; by the no-stand word after FV3-21b)
has no close: `_manual_block_door` prints `no manual-agent case is left for a block: nothing was dispatched` (`story_step.py:1093`);
`stage_done.py --status done` refuses a stage the controller has not accepted and names a `code_only` receipt (`stage_done.py:1241-1250`);
no skill-road command writes `code_only` (grep `code_only` over `story_step.py`, `stage_done.py`: only that sentence; the driver's
`close_receipt` -> `controller("code_only", ...)`, `driver_dispatch.py:2549`, is the one writer). Node FV3-21c: "the skill road
closes S6's manual half when nothing is left to dispatch, by the same steps as `manual_close` (reduce; record or person's pass ->
code-only close; else S6 awaits the consumer through `consumer_need_record`'s rule)". owns: `scripts/story_step.py`,
`scripts/tests/test_story_step_manual_block.py`, `skills/qa-story/phases/s6.md` (sequential after FV3-21b: same files). Test row
(in `test_story_step_manual_block.py`): a real story with the automation runner accepted not-complete and every manual case
refused -> the skill-road command reduces and leaves S6 awaiting the analyst (`awaits_acceptance` names the runner), and with an
accept record closes S6 code-only. Its spec is drafted after one scout question: "which command of the skill road can carry the
close (a `story_step.py` subcommand, or the S6 card's exit line), and what does `story_progress`/`where` show the orchestrator
when S6 has nothing to dispatch?"

---

## 5. Readers of every touched file (designer rule 7)

Commands (Grep tool, this round): (r1) pattern
`driver_stage_s6|driver_stage_build|waiver\.py|manual_evidence|state-exits\.md|test_story_run_s6\.py|driver-layers\.json|known_red|changelog\.d|story_step|test_story_step_manual_block|phases/s6\.md`
over `tools/` = 41 hits in 11 files; over `.githooks/` = 0; over `.claude/agents` = 2 hits, both the `SIBLING_MAP` alternative added
as a positive control of the same call (`designer.md`, `critic.md`), 0 for the file names; over `.claude/skills` = 0; over
`.claude/settings.json` (pattern `driver_stage|waiver|manual_evidence|story_step|known_red`) = 0, positive control `tools/` in the
same file = 37 hits. (r2) changed names
`consumer_need_record|s6_stand_word|s6_no_stand|stand_passing_word|no_stand_refusal|s6_live_scopes|manual_no_stand|manual_todo|stand_question_text|STAND_STAGES|acceptance_awaits|manual_close|_manual_block_check|manual_lane_plan`
over `tools/` = 0; `CONSUMER_ROUTES|refuse_case|write_case_refusal|await_at` over `tools/` = 0 (positive control:
`journal_write|dispatch_new` over `tools/` = 128 hits). `.claude/hooks` does not exist (`Glob .claude/*`: 4 files, no folder).

| file touched | readers found | verdict |
|---|---|---|
| `scripts/driver_stage_s6.py` | `driver-layers.json` (homes); `test_walk_account.py:449-450` (source order of `manual_lane_plan`: the branch holds neither text); `test_s6_reprove_manual.py:118` (stubs `s6_no_stand`; QUARANTINED, see F8 below); `test_stage_acceptance_consumer.py:150` (calls `consumer_need_record` for three sites with a fake; QUARANTINED; its "no record" world raises at `s6_reentry` first, so `manual_close` is never reached there; `Rig` copies `CONSUMER_ROUTES`: the new key is inert); `test_refuse_case.py:87` (stubs `consumer_need_record` with a 2-arg lambda returning None; QUARANTINED; signature kept, None = close goes on: bytes unchanged); `tools/` 0 | layers: changes in FV3-21 (K7); others unchanged |
| `scripts/driver_stage_build.py` | `driver-layers.json:619,623` (`STAND_STAGES` classconst row, `stand_question_text`): the constant keeps its name and value | unchanged |
| `scripts/waiver.py` | every `import waiver` in the package (names added only); `story_step.py:699` (FV3-21b reads the new reader) | unchanged / FV3-21b reads it |
| `scripts/manual_evidence.py` | `story_step.py:1059` (FV3-21b), `driver_stage_s6`, `driver_dialog`, `test_manual_evidence.py` (keep, detector); names added only | unchanged / FV3-21b reads it |
| `scripts/driver_dialog.py` | `test_refuse_case.py` (QUARANTINED; byte pins: the success path publishes through the same `atomic_json`, bytes equal) | unchanged |
| `design/state-exits.md` | `test_state_exits.py` (doors); `tools/test_test_quarantine.py:863` (a fixture string) | unchanged |
| `scripts/tests/test_story_run_s6.py` | `test-layers.json` (keep, `gate_named`); `tools/lint-baseline.json:271` (pyflakes ratchet: no new finding); `test_conductor_doors.py` (names the file for `s6.stand_confirm`) | unchanged |
| `scripts/tests/fixtures/driver-layers.json` | `test_driver_layers.py`, `driver_golden.py`, `tools/test_quarantine.py:2173` (purge on deletion) | unchanged |
| `scripts/tests/fixtures/driver-exits/known_red.json` | `scripts/tests/known_red.py` only | unchanged; FV3-20 also writes it (hence the start order) |
| `changelog.d/*.md` (2 new) | `tools/architecture_gate.py:12` (a package path: the commit needs the `architecture:` line), `tools/test_volume.py:16` (excluded dir), `tools/test_piles_form.py:58` | unchanged |
| `scripts/story_step.py` (FV3-21b) | `tools/story_capture.py:518` (docstring), `tools/test_dispatch_gate.py:2302` (a fixture string), `tools/controller-blocks-gen.py` (door texts naming `story_step.py start/finish`: no text of theirs changes); in package: `test_story_step_manual_block.py` (keep), `test_s6_lane_admission.py` and the `test_controller_rework` parts (import its test module) | unchanged |
| `scripts/tests/test_story_step_manual_block.py` (FV3-21b) | `test-layers.json` (keep, `data_join`), its importers | unchanged |
| `skills/qa-story/phases/s6.md` (FV3-21b) | `test_words_doors.py` map names `phases/s5.md` for the stand door, not s6.md (r1 trail) | unchanged |

**F8 as written conflicts with a standing rule — applied in its intent, see fork R2-F2.** `test_s6_reprove_manual.py` is in the
`quarantine` section of `test-layers.json` (`:9799`, cohort 8073673; the section starts at `:7208`), and `docs/TESTING.md:107-108`
says a quarantined test "в каноне не запускается, не чинится и не правится". After K1.b its stub `s6_no_stand = lambda: True` still
drives the stage to the stubbed `run_manual_block` (green). The critic's concern (an impossible stub world and a stale comment) is
answered in the keep file instead: row W1 runs the real `s6_stand_word` through the real stage entry of `manual_lane_plan`.

---

## 6. Siblings (rule 9; SIBLING_MAP)

- Axis 26 (the no-stand word): the manual half (driver) and `story_step` (skill road) become readers through ONE reader
  `waiver.stand_passing_word`. **Lead places** (mechanism commit, `docs/SIBLING_MAP.md:455`, with the merge of wave W): replace
  `` `Driver.stand_check` (`driver_stage_build.py`, S5) and `Driver.s6_no_stand` (`driver_stage_s6.py`, S6) call (HF8-4 P8) `` with
  `` `Driver.stand_check` (`driver_stage_build.py`, S5) and `waiver.stand_passing_word` (S6: `Driver.s6_stand_word`, whose bool is `Driver.s6_no_stand`; the skill road's `story_step start`) call (HF8-4 P8) ``,
  and in the readers list replace `` `Driver.stand_check` and `Driver.s6_no_stand` (the S5 and S6 stand sites) `` with
  `` `Driver.stand_check` and `waiver.stand_passing_word` (the S5 and S6 stand sites; through it the automation half (`s6_no_stand`, K4), the manual half (`manual_lane_plan` -> `manual_no_stand`) and the skill road's manual `start` (FV3-21b): no walk, the cases `left_unchecked` in the person's words) ``.
- Axis 19 / AR-19 (stage twins): S6's await at `manual_close` and S7's `s7_await_scribe` write the same marker read by the same
  reader. `driver_stage_s7.py` is NOT changed: lifting the three marker lines into a shared method would break the quarantined
  `Rig` of `test_stage_acceptance_consumer.py`, which binds driver methods by name (`:372-375`) and cannot be edited (TESTING.md);
  the copy is three lines, both sites are named here and in the new state-exits row.
- Axis 5 (S5/S6 twins): S5 has no manual half; its `go on` text is the same site (K2).
- Sweep of the artifact (rule 9) — the refused-case family in `driver_stage_s6.py`: `stand_login_gate` (`:1249`) — applied pattern
  (words, `left_unchecked`, prepare before refuse); `walk_refuse_gaps` — n/a (account, not stand), but its all-refused road is
  B1's class: covered by K6 (E23); `gate_a_dry_person` `go on` — n/a for the word, covered by K6 for the close (E23);
  `deferred_decision` — n/a. The close sites of `consumer_need_record`: `manual_close` — applied (`await_at`); `s6_reentry`,
  `s6_reprobed_close` — not applicable: there the runner was dispatched with `consumer_awaits("S6", True)` (`:573`, no manual
  half), so it already awaits by its own word; S7 `s7_close` — n/a (its road is `s7_await_scribe`).
- The skill road (P31): FV3-21b (word, reason/door, record) in this wave; FV3-21c (the close) — fork R2-F1.
- S0 `go on without a stand for now` (`driver_s0.py:2361`): n/a — S0's word is "for now" and is asked again before any test.
- Noticed analog, another zone: `check_delivery.stand_word` reads the bare `STAND_NOT_CONFIRMED_BLOCK` while the driver reads
  `stand_block(environment)` (critic F6). F6 = the Lead writes the finding (below); §6 points at it.

**F6 (applied as a pointer).** The finding file is the Lead's to write before dispatch (dispatch rule: designer writes only this
file), in the pile that owns delivery: class "two readers of one word disagree on a `match` form" (AR-13, axis 26): a word whose
`match` is the whole text `stand not confirmed: no stand is confirmed for this story` passes the driver's `split_overridden`
(`names_whole`) and not `check_delivery.py:1625`'s bare block. Executor: the delivery pile's node; the natural fix is that
`check_delivery.stand_word` reads `waiver.stand_passing_word` (the one reader this card creates). §6 of this card points at that
finding by its path once the Lead names it: `<finding path, filled by the Lead>`.

---

## 7. Non-goals

7.1 The automation half (K4 of HF2-11b stays). 7.2 A code-only close of the whole S6 when every automated result stands and all
manual cases are refused by no stand (`:523` still dispatches the runner because `manual_scope` is non-empty). 7.3 The walk-retry
versus coverage-gate interplay. 7.4 `docs/SIBLING_MAP.md` (the Lead places §6's lines). 7.5 `references/question-prices.json`
(F-2 = (a), confirmed by the critic: no residual). 7.6 The FV3-20 stub key (J2-1) and the `main/S6` label (J2-2): FV3-20's round.
7.7 `driver_stage_s7.py` (§6 axis 19). 7.8 The skill road's close (FV3-21c). 7.9 Mocks for the manual half, and whether a named
stand may sit in `environment_pending` (§OQ).

### §OQ — the owner's open question (17.11.2026), today's behaviour, and the ONE place the answer changes the card

The owner's words: «любой стенд который нам дали мы считаем готовым тестовым стендом если человек не скажет чего-то
дополнительного (например … на этом стенде этого доступа в принципе нет) И то можем предложить моки». Carried to the owner by the
Lead (critic t-1118 Key 3).
TODAY'S BEHAVIOUR, which this card keeps: (1) mocks — the factory offers no mock for the manual half; `go on` leaves the
manual-agent cases unchecked in the person's words; (2) a NAMED stand with `environment_pending: true` — `stand_check` probes it;
exit 0 confirms it (`stage_done --set environment_pending=false`); otherwise the person is asked; a `go on` then takes the same
branch as no stand (E2/W3).
**THE ONE PLACE THE ANSWER CHANGES THE CARD: E2 / W3 and the `go on` option text (K2.a).** If the owner says mocks apply to the
manual half, the `go on` option and `NO_STAND_DOOR` gain a mock road (a NEW node: a mock walk does not exist); if the owner says a
named stand is never pending, E2/W3 become unreachable for named stands (the row stays as a guard) and the change belongs to S0 /
`stand_check` (a NEW node). Neither answer changes K6 (B1) or FV3-21b's mechanics. The card does not wait for the answer.

---

## 8. Witness (narrowed, `plans/builder-rules.md` 7b)

FV3-21: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_stage_s6.py ai-packages/qa-factory/scripts/driver_stage_build.py ai-packages/qa-factory/scripts/waiver.py ai-packages/qa-factory/scripts/manual_evidence.py ai-packages/qa-factory/scripts/driver_dialog.py ai-packages/qa-factory/design/state-exits.md ai-packages/qa-factory/scripts/tests/test_story_run_s6.py ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red.json`
then EVERY command it names, verbatim output (F9: with `phases/s6.md` out of FV3-21 the "run the whole scenario layer" line is
gone; `driver_stage_s6.py` still fans out to the scenarios and keep files the walk names — all of them are run). Expected among
them; any the walk does not name the builder adds and says so: `test_story_run_s6.py`, `test_human_questions.py`,
`test_story_run_words.py`, `test_state_exits.py`, `test_driver_layers.py`, `test_walk_account.py`, `test_walk_lanes.py`,
`test_walk_lanes_parallel.py`, `test_manual_evidence.py`, `test_judgment_census.py`, `test_field_producers.py`,
`test_scenario_dry_1.py --part main` (K3), `selftest.py --lang`. NOT run (quarantined, TESTING.md): `test_s6_reprove_manual.py`,
`test_refuse_case.py`, `test_stage_acceptance_consumer.py`, `test_consumer_close_route.py`, `test_walk_road.py`. Plus the three
probes of K1/K6 and the one of K2, each by byte copy with the hash comparison. Never CI, never a full set.

FV3-21b: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/story_step.py ai-packages/qa-factory/scripts/tests/test_story_step_manual_block.py ai-packages/qa-factory/skills/qa-story/phases/s6.md`
then every command it names: `phases/s6.md` has no scenario or keep row, so the walk demands THE WHOLE SCENARIO LAYER (the six
scenario files the critic's run listed) — that is part of FV3-21b's witness (F9). Plus `test_story_step_manual_block.py`,
`test_judgment_census.py`, `selftest.py --lang`, and the probe of §4.4.

DoD lines for the headers: FV3-21: `the witness-for output above, every named command green, K3 measured row or the measured line returned as a question, the 4 probes red-then-restored with hashes`.
FV3-21b: `the witness-for output above incl. the whole scenario layer, rows S1-S7 green, the probe red-then-restored with hashes`.

---

## 9. FR sections to walk (PROJECT.md package item 1; one line each, both nodes)

A (FR-1/FR-2: reason and door name a road the person can take; FR-4: the branch and the await are informed, never silent — the
printed lines; FR-57: the awaiting stage is no dead end); B (FR-6 the `says` clause, the reason, the door against
`human-questions.md`; FR-9 the price of `go on`; FR-10 the packet does not contradict itself — F-2 = (a)); C (FR-8 the words carried
to the executor; FR-11 FV3-21b's sentence ships with its executor; FR-42 every returned state has a move: the Refusal of K6 stays
only where the wait cannot hold); D (FR-40 the two new state-exits rows; FR-59 the unknown branches E15(c), W13e); E (FR-36 the
standing decision is not probed; FR-23 a null outcome recordable); F (n/a — no measurement changed); G (FR-30 English, no Cyrillic in
fixtures — `chr(0xE9)`; FR-32 root cause with test; FR-33 closed by code, not proved: a `live-runs` row is owed by the Lead for
both nodes).

---

## 10. Closing table: verdict items -> where applied in r2

| item | applied | where in r2 |
|---|---|---|
| B1 = (b2) | applied (checked against the carriers: holds) | §1.1(b), §1.4 (carrier check), K6 (a-c, error direction, T-RC), K1 rows W13-W13e, E8 rewritten as the decision, E23 (the all-refused siblings closed by the same change, W13b), K3 expectation rewritten from the decided road, W7 fixture corrected (stage, role, scope, accept record), K5(ii) state row |
| B2 | applied | §0 (two cards, disjoint owns, start order, one wave), K1.e (shared reader/builder/writer in `waiver.py` / `manual_evidence.py` / `driver_dialog.py`), §4 FV3-21b (K4 moved there with its executor), §4.5 FV3-21c (the close residual, fork R2-F1) |
| F1 | applied (recommended form) | K1.d (live S6 dispatch or unreadable state = branch not taken, one line), K1.c `s6_live_scopes`, E15(b)(c), W12/W12b/W12c; r1 step 8 and W9 deleted |
| F2 | applied (second form) | K1.d step 3, E20, E21, E22, W14, W14b; FV3-21b S4 |
| F3 | applied | K2.b, T7 |
| F4 | applied | W5a, E14 |
| F5 | applied | K1.e `NO_STAND_DOOR`, the `DOOR` literal (K1, §4.4), K8 |
| F6 | applied as far as this role may (the finding file is the Lead's write) | §6 "F6" paragraph with the finding's class, evidence and executor; pointer slot for its path |
| F7 | applied | K5(i) way-out cell: "takes effect in the NEXT run of the story — S6, once closed, does not reopen by itself" |
| F8 | applied in intent; as written it conflicts with TESTING.md quarantine | §5 "F8" paragraph; fork R2-F2 |
| F9 | applied | §8 (FV3-21 without s6.md; FV3-21b carries the whole scenario layer); the quarantined files listed as not run |

---

## 11. Forks (recommendation first)

**R2-F1 — when FV3-21c (the skill road's close of an all-refused manual half) is done.** Evidence §4.5: today no skill-road
command closes S6 when every manual case is refused, for any reason; FV3-21b adds one more reason, not the gap. Options:
(a, recommended) FV3-21c is a named node with the owns and test row of §4.5, drafted after its scout question, sequential after
FV3-21b in the same pile; FV3-21b's s6.md sentence claims nothing about the close meanwhile (true to its executor, FR-11);
(b) fold the close into FV3-21b now — blocks the wave on a design not yet drafted (the scout question is open);
(c) FV3-21b waits for FV3-21c — the skill road keeps dispatching failing walks under the word meanwhile. Cost of covering the
left-out side: one scout + one designer + one builder node on `story_step.py`.

**R2-F2 — F8 vs the quarantine rule.** `test_s6_reprove_manual.py` is quarantined (`test-layers.json:9799`); TESTING.md forbids
editing it. Options: (a, recommended) do not edit it; the concern is covered by W1 in the keep file (§5); (b) edit it as the
critic wrote — breaks "не чинится и не правится" and needs the owner's word. Note: the critic's verdict did not mention the
quarantine.

**R2-F3 — `--dry-run` writes the awaiting marker (both twins).** `person_pass` says a dry run writes nothing (B-20 F2,
`driver_stage_s6.py:300-302`), but `s7_await_scribe` writes the marker without a dry check (`driver_stage_s7.py:201-205`), and K6
copies it for parity. Options: (a, recommended) parity now (K6 as written); the Lead files one finding for both twins (S6 and S7)
in the pile that owns the driver's dry mode; (b) K6 skips the write under `self.dry` — S6 and S7 then differ in dry mode (axis 19).

## 12. Small choices the designer closed (the Lead can stop any)

- The no-stand reader's home is `waiver.py` (`stand_passing_word`, `STAND_STAGES`), beside `stand_block`, not `manual_evidence.py`:
  both roads already import `waiver` at module level (`story_step.py:699`, `driver_stage_build.py`), and `Driver.STAND_STAGES`
  becomes `waiver.STAND_STAGES` so the pair has one definition. The Lead's B2 home (`manual_evidence.py`) holds the reason/door
  builder AND the record writer.
- The record writer moved into `manual_evidence.write_case_refusal` (AR-14 for two roads); its OSError path returns False instead
  of the driver's in-place fallback write (`driver_core._write_json:322-324`): a case whose record could not be written is still
  printed and listed in the receipt (E19).
- (b2) placed INSIDE `consumer_need_record` (data key `await_at`, same signature, returns bool) rather than a new method: the
  quarantined stubs (`test_refuse_case.py:87` 2-arg lambda; the `Rig` binding list) keep working, and the one close-needs-record
  rule stays in one function.
- `manual_close` reorders to: deferred refusals -> reduce -> consumer step -> close (the S7 twin's B3 order).
- `s6_unsettled_cases` of r1 replaced by `s6_live_scopes` (F1 needs only "any live S6 dispatch"; `s6_settling_lanes` reuses it);
  `s6_serial_reason` untouched (twin of `s5_serial_reason`).
- The real-controller pin extends the existing `t261_the_real_controller_...` function (keep file) with a second world, not a new
  file; `test_consumer_close_route.py` (where a similar world exists) is quarantined.
- The FV3-21b refusal line and door are new English text in the style of the function's existing refusals; the door names the
  record's own door plus the revoke command.
- The clause text `an agent checks no case by hand` and the console quote through `s0_quote` kept from r1.

## Reading trail

Read this round: card r1 (whole); verdict t-1118 (whole, incl. "Lead decisions on the verdict"); `scripts/driver_stage_s6.py`
130-339 (`CONSUMER_ROUTES`, `consumer_awaits`, `consumer_pending`, `consumer_close_words`, `consumer_word_step`, `person_pass`,
`consumer_need_record`), 339-478 (`consumer_gap`, `consumer_completion`, `consumer_settled`), 478-607 (`stage_S6`), 895-1019,
1015-1069 (`manual_close`), 1240-1349 (`stand_login_gate`, `manual_lane_plan`), 1560-1659 (`run_manual_block`, `s6_serial_reason`,
`s6_settling_lanes`); `scripts/acceptance.py` 1390-1589 (`awaits_acceptance`, `stage_author_dispatch`, `author_dispatches`,
`consumer_of`, `consumer_close_refusal`); `scripts/controller.py` 5570-5604, 9240-9272; `scripts/driver_stage_s7.py` 40-99,
160-207, 763-786; `scripts/driver_stage_build.py` 20-219; `scripts/driver_dialog.py` 222-243, 770-781; `scripts/driver_core.py`
313-324 (grep); `scripts/waiver.py` 362-386; `scripts/manual_evidence.py` imports (grep), 1268-1322; `scripts/story_step.py`
990-1110 + grep (`manual_evidence|waiver`); `scripts/stage_done.py` 1220-1264; `skills/qa-story/phases/s6.md` (whole);
`design/state-exits.md` 1-80; `scripts/tests/test_story_run_s6.py` 420-567; `scripts/tests/test_consumer_close_route.py` 1-200;
`scripts/tests/test_stage_acceptance_consumer.py` 138-167, 360-584; `scripts/tests/test_stage_done.py` 160-183;
`scripts/tests/test_fixes_13797.py` 227-270; `scripts/tests/test_refuse_case.py` 1-104; `scripts/tests/test_story_step_manual_block.py`
grep of defs, 395-421; `scripts/tests/fixtures/driver-layers.json` 618-657 + grep; `scripts/tests/fixtures/judgment-census.json` 1-14 +
grep; `scripts/tests/test-layers.json` section heads (grep) and rows of the files named in §5/§8; `docs/TESTING.md` 100-139.
Greps (Grep tool): `acceptance_awaits` over scripts (writers: only `driver_stage_s7.py:204`; readers: `acceptance.py:1496`);
`awaits_acceptance\(` over scripts (the reader's callers, §1.4); `code_only` over the package's `*.md` and selected scripts (§4.5);
the reader greps of §5.

Negative claims and their controls: "no state-exits row for the awaiting state" — `(?i)acceptance_awaits|awaits_acceptance|consumer|stand login missing`
over `state-exits.md` finds only `:71` (the control term); "no census row for `consumer_need_record`" — the same grep finds the
`stand_check` row `:1117`; "no skill-road writer of `code_only`" — the same glob-filtered grep finds `stage_done.py:1247`'s
sentence; "no tools/ reader of the changed names" — control `journal_write|dispatch_new` = 128 hits; "no settings.json reader" —
control `tools/` = 37 hits in the same file; "`test_s6_reprove_manual.py`, `test_refuse_case.py`, `test_stage_acceptance_consumer.py`,
`test_consumer_close_route.py`, `test_walk_road.py` are quarantined" — their rows sit after `"quarantine": {` (`:7208`), while
`test_story_run_s6.py` (`:6174`), `test_story_step_manual_block.py` (`:6360`), `test_manual_evidence.py` (`:3042`) sit in `keep`
(`:36`).

Brief contradictions noticed: F8 as written conflicts with TESTING.md quarantine (R2-F2); the brief's (b2) phrase "no manual
dispatch" is read as "nothing left to dispatch at `manual_close`" (the site's own definition), which also covers an earlier
accepted manual block followed by all-refused cases — the same class, the same site.

## Lead decisions on r2 (architect-rank session, 17.11.2026; by recommendation, until the owner's word)

- R2-F1: FV3-21c (the skill road's close of an all-refused manual half) is a named node of the same pile, opened after one
  scout question; it does not hold FV3-21 and FV3-21b.
- R2-F2: `test_s6_reprove_manual.py` stays untouched (quarantine); its case is covered by row W1.
- R2-F3: dry-run marker parity on both twins now, plus one finding (the Lead files it).
- No second plan critic: B1 = (b2) was the critic's own class fix and the designer checked it against the carriers; the
  code critic judges the result (one pass for FV3-21 + FV3-21b).
- Dispatch: after the S6 stub branch (t-1098, t-1109) is on main.

## The owner's answers to §OQ (владелец, 17.11.2026, verbatim)

On «можем предложить моки» and the manual half of S6: «да, но это предложение распростроняется на весь стенд, а не для
одного прохода ручного агента. То есть мы такой стенд встретили в первые и спрашиваем исключать проход и кейс передавать
человеку или построить моки для стенда (предлагаем только если это возможно). Если человек соглашается на моки, то это
единые моки всего проекта, они не удаляются по прохождении кейса и потдерживаются и развиваются вместе с проектом и
другими стори. Это как тестовый фреймворк - техническая основа нашего проекта. Если в проекте уже есть понятие моков и их
организация, то мы ей следуем, если нету, то надо создавать систему моков с ноля. Как именно создавать моки, как их
потдерживать, какую технологию выбрать это надо продумать как отдельную идею. Пока создание моков с ноля не реализованно
в фабррике, фабрика может предлагать моки, только если в проекте уже есть для них основа и мы знаем как создавать
дополнительные моки для нашей стори».

On a named stand sitting in "waiting for the environment": «В каком случае например? Если человек сказал "сейчас настрою"
то мы ждём настройки и дальше не идём. Если он настраивал 2 дня, то он просто сново запускает ту же стори и она
продолжается с остановленного момента».

What follows for FV3-21 / FV3-21b (Lead): nothing in these two nodes offers mocks — the offer is stand-wide, belongs to the
moment the stand's missing access is first met, and until "mocks from scratch" exists it is made only when the project
already has a mock base the factory knows how to extend. That is a NEW IDEA of the owner (project-wide mocks as technical
base), opened by the idea procedure (PROJECT.md), not a line of this card. "Waiting for the environment" is a legal state
with a way out: the person says they are setting it up, the story stops, and re-running the same story continues from the
stop; the cards keep today's behaviour and the code critic checks that the resume road holds (AR-25).
