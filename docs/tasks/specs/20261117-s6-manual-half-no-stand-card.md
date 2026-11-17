# FV3-21 — the person's no-stand word reaches the manual half of S6 (designer draft, t-1110)

Pile `live-run-fvf`, batch 3, node FV3-21. Source: critic diagnosis
`docs/tasks/specs/reviews/t-1106-dry-s6-manual-half-diagnosis.md` (Q1-Q3). Designer: opus, t-1110, 2026-11-17.
Status: DRAFT for Lead acceptance, then plan critic (PROJECT.md "package change" item 6: this card changes a MEANING -
what the person's `go on` on the stand question does to the manual half).

All package paths below are relative to `ai-packages/qa-factory/`. Line numbers are of `main` as read on 2026-11-17
(root checkout); they match the critic's tree for every function cited.

---

## 0. Dispatch header (for `tools/dispatch_new.py`; the Lead prints it, never types it)

- given: this card; `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md`;
  `docs/tasks/specs/reviews/t-1106-dry-s6-manual-half-diagnosis.md` (Q1-Q3);
  `ai-packages/qa-factory/references/human-questions.md`; `ai-packages/qa-factory/design/architecture.md` (AR-13, AR-14,
  AR-15, AR-16, AR-24, AR-25, AR-28, AR-29).
- owns (repo-relative; the Lead turns them into absolute worktree paths in the header):
  - `ai-packages/qa-factory/scripts/driver_stage_s6.py`
  - `ai-packages/qa-factory/scripts/driver_stage_build.py`
  - `ai-packages/qa-factory/skills/qa-story/phases/s6.md`
  - `ai-packages/qa-factory/design/state-exits.md`
  - `ai-packages/qa-factory/scripts/tests/test_story_run_s6.py`
  - `ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json`
  - `ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red.json`
  - `ai-packages/qa-factory/changelog.d/fv3-21-no-stand-manual-half.md` (new)
- non-goals: listed in section 6 (Q3's non-goals stand, Lead decision).
- handoff: builder report per `.claude/agents/builder.md` rule 7 + the FR walk (section 8) + the witness (section 7).
- designer: this file's absolute path once accepted.
- siblings: section 5.
- DEPENDENCY (see fork F-4): start from `origin/main` only AFTER the FV3-20 branch (t-1098, commit 5979acb4 plus the
  J2-1/J2-2 fix round) is merged. On `main` today `known_red.json` `main/S6` is still the t-1088 row (stop at the
  runner-1 handover form) and `dry_stub.py` has no `resolve_newest` (read 2026-11-17: `STUB_KEY` at `dry_stub.py:749`
  is the old `#[0-9]` form). Without FV3-20 the dry pass never reaches the manual half and item K3 cannot be measured.

---

## 1. What changes, which invariants, who owns each check

### 1.1 The defect (from t-1106 Q1/Q2, re-read on main)

`stage_S6` (`scripts/driver_stage_s6.py:480`) reads the person's no-stand word once (`no_stand = self.s6_no_stand()`,
`:519`) and only the automation half uses it (K4 `:565`, `s6_reentry` `:585`, `s6_reprove_before_manual` `:587`).
`run_manual_block` (`:1566`) -> `manual_lane_plan` (`:1304-1336`) never reads it: it asks the gate-A-dry question
(`manual_gate_note`), prepares every case (`manual_plan`), may ask the sign-in question (`stand_login_gate`), and then a
manual walk is dispatched that can only fail (no `environments[]` -> every `manual_capture` call refuses).

### 1.2 AR-n touched (rule 10; the `architecture:` line names these)

| AR | how this card keeps it | change check written into the DoD |
|---|---|---|
| AR-24 (words reach the executor, whole) | the `go on` word now reaches the manual half; each refused case's `request.json` quotes the words whole (one line, whitespace squashed, as `stand_login_gate` `:1288` does); the question's `go on` option says what it does to the manual cases (item K2) | K1 rows W1-W3 assert the exact reason with the words; K2 rows assert the `says` clause |
| AR-25 (every recorded state has a way out) | a new ENTRY into an existing state (a manual-agent case whose `request.json` holds `{refused: {reason, door, by: left_unchecked}}`); way out: a confirmed stand (the next entry reads `s6_no_stand` False and walks the case) or `waiver.py --revoke --stage <S5/S6> --block "stand not confirmed"` (the stand question speaks again); a new `design/state-exits.md` row names both | `test_state_exits.py` green with the new row (it checks every door the walk names) |
| AR-13 (a fact with a reader is read only through it) | the word is read only through `waiver.split_overridden([waiver.stand_block(environment)], ...)`, now inside ONE helper `s6_stand_word`; `s6_no_stand` delegates to it; no second reader of `stage_overrides[]`, no literal of the block name | grep in K1 DoD: `stage_overrides` and `"stand not confirmed"` do not appear in the new code of `driver_stage_s6.py` (positive control: the same grep finds `waiver.stand_block` at the helper) |
| AR-14 (one artifact, one writer) | `request.json` `refused` is written only by `refuse_case` (`driver_dialog.py:227`) | code review; no `_write_json` on a request path in the diff |
| AR-15 (one survivor) | the close goes through `manual_close` (`:1025`) unchanged; "the cases still to walk" through ONE helper `manual_todo` used by `manual_plan` and the new branch | K1 row W1 asserts site `s6.manual_close`; `manual_plan` rows of `t261_k2_...` stay green |
| AR-16 (text through one question form) | the `says` clause goes through `closed_question("s6.stand_confirm", ...)` like every option | K2 row: `human_broken(text) == []` |
| AR-28 (unknown never a pass) | the stand question's clause: a manual scope that cannot be read SAYS the clause (toward telling the price); the branch with a running/blocked/paused S6 dispatch whose scope is empty (unknown cases) is NOT taken this entry (declared safe default: today's road) | K1 row W12; K2 row "scope unreadable" |
| AR-29 (code judges data) | see 1.3 | `test_judgment_census.py` green, no census row added or changed |

### 1.3 Checks this card adds or alters: owner and census class (AR-29, P27)

| check | owner it serves | census class | census row? |
|---|---|---|---|
| the branch "a live stand word stands and no stand is confirmed" in `manual_lane_plan` | intent (it executes the person's decision; it judges no role output) | shape (presence of a person's word) | none: the branch has no refusal transport (`refuse_case` writes a record; `plan["refused"]` is the list transport), so the scanner makes no unit. If the builder's diff adds any `raise`/`refuse`/`sys.exit(str)` site, a row is owed and the builder STOPS and asks |
| `s6_stand_word` (the reader) | data | shape | none (no refusal site) |
| the `says` clause condition "the story's S6 manual scope is non-empty, or cannot be read" in `stand_check` | intent (the person's price, FR-9) | shape (presence of cases in a scope the controller computed) | none |

Commit lines: the builder's commit message carries the `architecture:` line naming AR-13, AR-14, AR-15, AR-16, AR-24,
AR-25, AR-28, AR-29 with how each is kept (table 1.2), and the `judgment:` line in the `none` form with its ` -- <why>`
(why: the change executes a person's recorded word and reads data presence; no role judgment moves to code or to a role).
The ONLY carrier of both forms is `tools/architecture_gate.py` (docstring items 2 and 6): the builder copies the form from
there, not from this card.

---

## 2. Items (each: file, function, exact behaviour, test row with control and probe)

### K1 — the branch: no stand word -> the manual cases are refused before anything is prepared, asked or dispatched

File `scripts/driver_stage_s6.py`.

**K1.a New helper `s6_stand_word(self) -> str`** (home `driver_stage_s6`, next to `s6_no_stand` `:672`).
Body = today's body of `s6_no_stand`, returning words instead of a bool:

```python
def s6_stand_word(self) -> str:
    """The words of the person's live word that passes the stand block for this story, "" when a stand is confirmed or no
    such word stands. ONE reader (axis 26): `waiver.split_overridden([waiver.stand_block(environment)], ...)` over
    `STAND_STAGES` in their order (S5 first, as `stand_check` reads them). ERROR DIRECTION: "" (no word) sends the story to
    `stand_check`, which asks; a confirmed stand is never "no stand"."""
    pipeline = self.pipeline()
    environment = str(pipeline.get("environment") or "")
    if environment and not pipeline.get("environment_pending"):
        return ""
    block = waiver.stand_block(environment)
    for owner in self.STAND_STAGES:
        passed = waiver.split_overridden([block], pipeline, owner)[1]
        if passed:
            return str(passed[0].get("decision") or "")
    return ""
```

and `s6_no_stand` becomes `return bool(self.s6_stand_word())` with its docstring kept (add one sentence: "the words:
`s6_stand_word`"). Equivalence: `contract.live_stage_overrides` drops every record whose `decision` is empty or
whitespace (`contract.py:169`), so a passed record always has non-empty words; the bool is unchanged in every world.

**K1.b New helper `manual_todo(self, cases, skip=()) -> list`** (home `driver_stage_s6`, next to `manual_plan` `:926`):
the cases still to walk, in plan-row order - exactly the expression `manual_plan` uses today (`:934-938`):

```python
again = {case for case, entry in ((getattr(self, "state", None) or {}).get("walk_retry") or {}).items()
         if isinstance(entry, dict) and entry.get("open")}
gone = (self.manual_done() - again) | {str(c) for c in skip}
return [c for c in self.manual_order(cases) if c not in gone]
```

`manual_plan` then loops `for case in self.manual_todo(cases, skip):` (its comment lines stay). No behaviour change for
`manual_plan` (its K2 rows in `t261_k2_...` are the control).

**K1.c The branch in `manual_lane_plan`.** POSITION: right after `waiting = self.deferred_waiting(cases)` (`:1311`) and
BEFORE the `manual_gate_note` test (`:1312`). Code:

```python
words = self.s6_stand_word()
if words:
    return self.manual_no_stand(cases, waiting, words), waiting
```

New method `manual_no_stand(self, cases, waiting, words) -> dict` (home `driver_stage_s6`):

1. `held = self.s6_unsettled_cases()` (K1.d). If `held is None` (a running/blocked/paused S6 dispatch names no case):
   print `S6: no stand is confirmed and the person said to go on, but a walk already under way names no case; the manual
   half goes on as before and is closed by that word at the next entry` and RETURN None from `manual_no_stand`; the
   caller then falls through to today's road (write the caller as: `plan = self.manual_no_stand(...)`; `if plan is not
   None: return plan, waiting`).
2. `said = " ".join(str(words).split())`.
3. `reason = f"not checked by an agent: no stand is confirmed for this story; the person said: \"{said}\""`
4. `door = "record a stand for this project with the onboarding and confirm it; the next run checks it by hand"`
5. `plan = {"blocks": [], "refused": [], "unprepared": []}`.
6. `waiting_cases = {case for case, _n in waiting}`.
7. For each `case` of `self.manual_todo(cases, skip=list(waiting_cases))`:
   - if `case in held`: skip it here (it joins step 8);
   - else `self.refuse_case(plan, case, reason, door, "left_unchecked")` and
     `print(f"S6: {case}: not checked by hand — not checked by an agent: no stand is confirmed for this story; "
     f"the person said: \"{self.s0_quote(words)}\"")` (the console quote is cut like every console quote of the person's
     words, `s0_quote`; the request.json reason is whole).
8. `plan["blocks"] = walk_lanes(kept, lane_keys(self.task_root, kept), self.MANUAL_BLOCK_MAX)` where `kept` = the
   `manual_todo` cases that are in `held` (normally empty). Those lanes go through today's road in `run_manual_block`
   (`s6_settling_lanes` runs them first): a walk already under way settles by its own road; this branch never writes
   the `request.json` of a case a live dispatch carries.
9. `self.walk_assign_clear()` (an assignment of an earlier entry is settled, as the old road does when it makes none).
10. Return `plan`.

`run_manual_block` is unchanged: with `plan["blocks"] == []` it calls `manual_close(cases, plan["refused"])` (`:1581-1583`);
`manual_close` refuses the waiting cases itself with its own deferred reason (`:1036-1039`), so a waiting case is
refused ONCE.

**K1.d New helper `s6_unsettled_cases(self) -> "set | None"`** (home `driver_stage_s6`): the predicate of
`s6_settling_lanes` (`:1645-1651`) lifted out, used by both:

```python
import dispatch_identity
ctl = self.controller_state()
rows = dispatch_identity.records(ctl.get("dispatches") if isinstance(ctl, dict) else None)
scopes = [{str(c) for c in r.get("scope") or [] if c} for r in rows
          if r.get("stage") == "S6" and r.get("status") in ("running", "blocked", "paused")]
if any(not s for s in scopes):
    return None
return set().union(*scopes) if scopes else set()
```

`s6_settling_lanes` then reads `held = self.s6_unsettled_cases()`; `if held is None: return []`; and `named = [lane for
lane in lanes if {str(c) for c in lane} & held]` (same result as today). An exception from the readers still propagates
(the caller of `s6_settling_lanes` already catches it, `:1595`; in `manual_no_stand` it propagates like `manual_done`'s
own read would).

**Test row K1 (one parameterised scenario in `scripts/tests/test_story_run_s6.py`)** — new function
`fv3_21_the_stand_word_reaches_the_manual_half`, registered in `main()` next to
`hf2_11b_without_a_stand_nothing_is_run_or_proved`. Rig: `d2_seed(task, environment=..., pending=...)`, `d2_pipeline(
task_root, stage_overrides=...)`, `manual_rig(root, env, task, cases)` and `enter_manual(driver, world, cases)`, with
`driver.close_by_code` wrapped to record `site` (as `reprobe_rig` does, `:2142`) and `driver.manual_prepare` wrapped to
count calls. `WORD = {"stage": "S6", "match": "stand not confirmed", "decision": "go on", "at": "2026-11-17T10:00:00+00:00",
"by": "human"}`. Expected texts are written in the test as literals (never derived from the source):
`REASON = 'not checked by an agent: no stand is confirmed for this story; the person said: "go on"'`,
`DOOR = "record a stand for this project with the onboarding and confirm it; the next run checks it by hand"`.

Branch-taken worlds (every one asserts: `launched == []`; no new key in `world.dispatches`; `manual_prepare` calls == 0;
no `Person` raised; `c16b_refused_by(task_root, cases) == ["left_unchecked"] * n`; each request's `refused.reason ==
REASON` (or the words variant) and `refused.door == DOOR`; `[m[0] for m in moves] == ["finalize", "code_only",
"stage_done"]`; sites `== ["s6.manual_close"]`; the printed text holds `S6: <case>: not checked by hand — not checked by an
agent: no stand is confirmed`):

| row | world |
|---|---|
| W1 | `environment=None, pending=True`, `WORD` on S6, cases `[TC_001, TC_002]` (FIRST check = `launched == []`) |
| W2 | as W1, the word recorded on S5 (`stage: "S5"`) |
| W3 | `environment="Local", pending=True` (named, not confirmed), `WORD` on S6 (Lead decision: same branch, FR-36) |
| W4 | as W1, `decision` = `"go on\n  " + chr(0xE9) + " later"` (multi-line, non-ASCII): reason quotes `go on ` + chr(0xE9) + ` later` on one line, the character kept |
| W5 | as W1, `decision` = 2 000 characters (beyond `QUOTE_LIMIT`): `request.json` reason holds all of it; the console line ends with the cut mark (`driver.CUT`) |
| W6 | as W1, `match: "*"` on S6 (a pass of every S6 block is the stand word too, as `stand_check` reads it) |

Case-level rows inside W1's world (same entry):

| row | world | expected |
|---|---|---|
| W7 | a third case `TC_003` carried by an ACCEPTED manual dispatch in `world.dispatches` (`execution_kind: manual`, `manual_case_ids: [TC_003]`, `status: accepted`) | `TC_003` has no `refused` written (its request.json absent or untouched); the close reason says `1 case(s) checked by an agent by hand, 2 not checked` |
| W8 | `driver.state["deferred"] = [{"n": 1, "kind": "walk_account", "holds": ["TC_002"]}]` | `TC_002` refused ONCE, with `manual_close`'s reason `not checked yet: it waits for your answer to question 1, asked before gate B` (never `REASON`) |
| W9 | `world.dispatches` holds `S6-qa-runner-5` `status: running`, `scope: [TC_002]`, `execution_kind: manual` | call `driver.manual_lane_plan([TC_001, TC_002])` directly: `TC_001` refused with `REASON`; `TC_002` has no `refused`; `plan["blocks"] == [["TC_002"]]` |
| W12 | as W9 but `scope: []` | `manual_lane_plan` falls through to today's road (`manual_prepare` called for both); the printed line `a walk already under way names no case` |

Branch-not-taken worlds (control; each asserts `launched` has exactly one manual dispatch, as today, and no request.json
holds `REASON`):

| row | world |
|---|---|
| C1 | `environment="Local", pending=False` (confirmed) with `WORD` on file: today's road (the control the critic named) |
| C2 | `environment=None, pending=True`, no word (`stage_overrides=[]`) |
| C3 | `WORD` with `revoked_at` set |
| C4 | `WORD` with `stage: "S4"` |
| C5 | `stage_overrides = "broken"` (not a list) |
| C6 | `WORD` with `match: "stand login missing"` (a word for another block) |

(C2-C6 enter `run_manual_block` directly, so they prove the BRANCH is not taken; that `stand_check` asks in these worlds
before S6 runs anything is already pinned by `test_story_run_stand_b.py` R6 "S6 with manual cases only asks: exit 3"
and P11 controls `:2483-2487`.)

PROBE (one, by byte copy per hygiene point 7): delete the three lines of K1.c; W1's first check (`launched == []`) goes
red. Second mutation for W8 (attach both to the witness): pass `skip=()` instead of the waiting cases -> W8's reason
check goes red.

### K2 — the stand question says what `go on` does to the manual cases

File `scripts/driver_stage_build.py`.

**K2.a** `stand_question_text` (`:38`) gains a keyword `manual: bool = False` (last parameter; every current caller and
every direct test call keeps its bytes). The `go on` option (`:129-131`) becomes:

```python
options.append({"answer": "go on", "token": "go on",
                "says": "go on without a stand" + ("; the tests are still written, but none is run on a stand" if stage == "S5" else "")
                        + ("; an agent checks no case by hand" if manual else "")
                        + ", and the story carries a line saying it was your decision"})
```

Resulting texts (exact):
- S6, manual: `go on without a stand; an agent checks no case by hand, and the story carries a line saying it was your decision`
- S5, manual: `go on without a stand; the tests are still written, but none is run on a stand; an agent checks no case by hand, and the story carries a line saying it was your decision`
- `manual=False`: today's text, byte for byte.

The clause is TRUE in every world it is said in (it claims no count), which is why the unreadable-scope case may say it
(FR-41: no unknown said as a fact). Checked against `references/human-questions.md`: no field name, no script, no path,
no id, no stage name alone, no machine shape; "by hand" and "an agent" are the words the sign-in and gate-A-dry
questions already use (`:1245-1247`, `:1014`).

**K2.b** `stand_check` (`:139`), on the question path ONLY (after the word loop and the probe, right before
`site_seam_person`, `:201`): compute

```python
try:
    manual = bool((self.stage_scope("S6", "manual") or {}).get("scope"))
except Exception:      # noqa: BLE001 - a doubt says the clause (the person's price, FR-9); the clause is true in every world
    manual = True
```

and pass `manual=manual` to `stand_question_text`. ONE reader for all four `stand_check` sites (S5 window entry
`driver_stage_s5.py:201/330`, S6 entry `driver_stage_s6.py:517`, relaunch / never-launched dispatch
`driver_machine.py:1508/1618`): the controller's derived S6 manual scope, the same fact `stage_S6` reads at `:483`.
POSITION invariant: a confirmed stand, a passed word and a probe that exits 0 return BEFORE this line, so they cost no
controller call and nothing about them changes; only a question that is about to be raised reads the scope.

**Test row K2** — extend `c16b_stand_confirm_is_priced_and_its_answers_have_executors` (`test_story_run_s6.py:1804`)
with one table (no new function):

| row | call | expected `go on` line |
|---|---|---|
| T1 | `stand_question_text("S6", "Local", ["Local"], "manual", manual=True)` | holds `an agent checks no case by hand` |
| T2 | same with `manual=False` (control) | does not hold it; equals today's text |
| T3 | `stand_question_text("S5", "", [], manual=True)` | holds `none is run on a stand; an agent checks no case by hand, and the story` |
| T4 | `stand_check("S6", "automation")` with `driver.stage_scope = lambda s, k="": {"scope": ["TC-2"]}` (a relaunch of the automation half, manual cases exist) | the raised Person's text holds the clause |
| T5 | as T4 with `{"scope": []}` | no clause |
| T6 | as T4 with `stage_scope` raising `Refusal` | clause said (error direction) |

Every row also asserts `human_broken(text) == []` and `c16b_price_lines(text, n)` unchanged. PROBE: replace `if manual`
with `if False` -> T1 goes red.

Census of question texts: `test_human_questions.py` calls `stand_question_text` positionally without `manual` (rows at
`:216-444`) -> byte-unchanged; its `stand_check("S5")` row (`:467`) patches `driver.py`, so `stage_scope` raises inside
the new `try` and the clause is said; that row checks only `offered` and `answer_note` -> unchanged. 
`test_story_run_words.py` counts inline `--decision` sites (`UPSTREAM_INLINE_DECISION_SITES = 2`, `:47`); this card adds
no words-carrying command -> unchanged. Both run in the witness.

### K3 — `known_red.json`: `main/S6` leaves; the next stop is measured into a new row; the pin stays 1

File `scripts/tests/fixtures/driver-exits/known_red.json` (read ONLY by `scripts/tests/known_red.py`, its `_about`).

After K1/K2 the builder runs `python -B ai-packages/qa-factory/scripts/tests/test_scenario_dry_1.py --part main` in its
worktree. Expected (critic Q3, estimate): S6 closes by `s6.manual_close` and the pass stops at S7 (no
`qa-failure-analyst@S7` stub row). The builder:
1. removes the `main/S6` row;
2. writes ONE new row keyed by the walk-row id the run prints for the new stop, `{node, raised_by, note?}`, where
   `raised_by` QUOTES the measured stop line verbatim from the run (stage, dispatch, the driver's own words) and names
   this card (`docs/tasks/specs/20261117-s6-manual-half-no-stand-card.md`, FV3-21), and `node` = the node the Lead
   names for the new stop (fork F-5; until the Lead names one: `FV3-21` with a `note` saying the owning node is owed);
3. keeps `pins.known_red` at 1.
If the new stop is NOT at S7, or is at S6 again (see fork F-3: the consumer record), the builder does not invent a row:
it returns the measured line as a question.
Control: `test_field_producers.py` "the red rows of the walk are exactly the ledger" (`red_rows_equal_the_known_red_ledger`,
`:1529`) green.

### K4 — the skill road says the same (one road, P31)

File `skills/qa-story/phases/s6.md`. Two edits, same sentence:
- Card line 5, after `a person's word on the block \`stand not confirmed\` (recorded on S5 or S6) already covers this
  stage`, insert: `; with that word no manual-agent case is dispatched: each stands as not checked by hand, in the
  person's words, and the manual half closes by code`.
- § "The stand, before the first dispatch" (`:22-28`), after `already covers this stage — do not ask again`, the same
  sentence.
Test: none of its own (doc). `test_words_doors.py` reads `phases/s6.md`? (not by its map, which names `phases/s5.md` for
the stand door, `:85`) - the builder runs `python -B ai-packages/qa-factory/scripts/selftest.py --lang` (FR-30) and the
`scenario_walk.py --witness-for` row of the file. See fork F-1 for the executor of this sentence on the skill road.

### K5 — `design/state-exits.md`: the new entry into the refused state (AR-25 change check)

Insert one row right after the stand-login row (`:71`), same table, same shape:

`| manual-agent cases left unchecked by the person's no-stand word (\`stand not confirmed\` in \`stage_overrides[]\` for S5 or S6 while no stand is confirmed; their \`request.json\` then holds \`{refused: {reason, door, by: left_unchecked}}\` with the person's words and the report says "not checked by hand") | the person's answer \`go on\` to the stand question, recorded by \`waiver.py --stage S5\` or \`--stage S6 --block "stand not confirmed"\`; the driver refuses the cases at the next S6 manual entry, before anything is prepared or dispatched | a confirmed stand (the next entry reads it and walks the cases, whatever the word says), or \`waiver.py --revoke --stage S6 --block "stand not confirmed"\` (or \`--stage S5\`; the stand question speaks again) | \`test_story_run_s6.py\`, \`test_state_exits.py\` |`

Test: `test_state_exits.py` (checks every door the walk names exists: `waiver.py --revoke`, `--stage`, `--block`).

### K6 — `driver-layers.json` rows for the new names

File `scripts/tests/fixtures/driver-layers.json`. Add, next to `Driver.s6_no_stand` (`:646`), rows of kind `method`, home
`driver_stage_s6`, row 74 (the s6 block): `Driver.s6_stand_word` (note: "FV3-21: the words of the person's stand word,
the one reader; `s6_no_stand` is its bool"), `Driver.s6_unsettled_cases` (note: "FV3-21: the cases of running, blocked
or paused S6 dispatches, None when one names no case; read by `s6_settling_lanes` and `manual_no_stand`"); next to
`Driver.manual_plan` (row 75): `Driver.manual_todo`, `Driver.manual_no_stand` (notes in the same style). Test:
`test_driver_layers.py` (named by the witness command).

### K7 — changelog fragment

New file `changelog.d/fv3-21-no-stand-manual-half.md`, ASCII, one or two bullets in the style of
`changelog.d/fv1-5-stand-check-words.md`: with the person's `go on` on the stand question (no stand confirmed), the
manual-agent cases of S6 are no longer dispatched to a walk that cannot run: each is recorded as not checked by hand
with the person's words and a door, and the manual half closes by code; the stand question's `go on` option now says
so when the story has such cases.

---

## 3. Edges (rule 11): every row decided, with the invariant it protects

INVARIANT of the whole card: **no manual walk is dispatched under a person's word that declined the stand, and no case a
live walk carries is rewritten.**

| # | edge (Q3 table + the designer's) | behaviour | invariant protected | where |
|---|---|---|---|---|
| E1 | no stand + `go on` (word on S5 or S6, environment empty) | branch taken: no prepare, no question, no dispatch; cases `left_unchecked` with the words; `manual_close` | no walk is dispatched under a declined stand (FR-36) | K1 W1, W2 |
| E2 | stand named, not confirmed (`environment_pending`) + `go on` | the same branch (Lead decision, FR-36) | same | K1 W3 |
| E3 | no stand + `stop` | no word recorded: `stand_check` raises / the story stops before `manual_lane_plan`; nothing changes, no `refused` written | the branch never acts without a recorded word | K1 C2 (+ existing `test_story_run_stand_b.py` R6) |
| E4 | a confirmed stand (any words on file) | `s6_stand_word` "" -> today's road | a confirmed stand is never "no stand"; a walk that CAN run is never refused by this branch | K1 C1 |
| E5 | a manual-human case | not in the manual scope (`stage_scope` `manual` returns manual-agent only); untouched | the branch refuses only what the factory would have walked | by construction (scope); no row |
| E6 | a case already done by an accepted manual dispatch of an earlier life | stays done, not refused (`manual_todo` = `manual_plan`'s formula) | an accepted record is never overwritten by a refusal | K1 W7 |
| E7 | a case a deferred question holds | not refused by the branch; `manual_close` refuses it once with its deferred reason | one open question per case (E11); one refusal per case | K1 W8 |
| E8 | with a consumer (`acceptance.consumer_of("S6")`) | `manual_close` calls `consumer_need_record` unchanged | a stage with a consumer never closes without the record or a person's pass | fork F-3 (measure first) |
| E9 | word recorded on S5 vs S6 | both count; S5 is read first (`STAND_STAGES` order, as `stand_check` prints) | one word covers both stages (`driver_stage_build.py:29-30`) | K1 W2 |
| E10 | environment empty vs pending | empty (`pending` any) -> word decides; named + pending true -> word decides; named + pending false/absent -> confirmed, never no-stand | same as `stand_check` `:167` | K1 W1, W3, C1 |
| E11 | a word present but for another stage (S4, S7) | not a word (`live_stage_overrides(pipeline, (stage,))`) -> branch not taken; `stand_check` asks | an unrelated word never declines the stand | K1 C4 |
| E12 | `stage_overrides` broken (not a list, entries not objects, empty `decision`, `<placeholder>` match, revoked) | `live_stage_overrides` / `split_overridden` give no pass -> branch not taken; `stand_check` asks (AR-28) | an unreadable word is no word | K1 C3, C5 |
| E13 | a `*` pass on S6 | counts as the stand word (it passes the stand block in `stand_check` too) -> branch | one reader, one reading | K1 W6 |
| E14 | person's words: multi-line, non-ASCII, very long | request.json reason: one line, whitespace squashed, every character kept, never cut (AR-24); console line: `s0_quote` (cut at `QUOTE_LIMIT` with `CUT`) | the words reach the record whole | K1 W4, W5 |
| E15 | TEMPORAL: a story whose earlier life already dispatched a manual block before this code existed | (a) block accepted -> its cases stay done (E6); (b) block running/blocked/paused at entry -> its cases are not refused, they stay as lanes for today's road to settle (K1.c step 8), the rest is refused; (c) such a dispatch names no case -> branch not taken this entry, one printed line, today's road (safe default, AR-28); (d) the dry story's own pending `exit_limit` question from before the upgrade: a fresh dry walk starts a new copy, so it does not arise there; a real story stopped at that question settles it by its own road, and its next S6 entry takes the branch | the branch never writes the request of a case a live walk carries; a crash or upgrade between entries re-dispatches nothing | K1 W9, W12 |
| E16 | TEMPORAL (rule 11 i): the `says` clause and the state-exits row are brought into existence by this card | before: the `go on` text without the clause; after: with it, only when the S6 manual scope is non-empty or unreadable. Stories that already recorded the word before the upgrade get the branch at their next S6 manual entry; nothing re-asks them (D-0047: a standing decision is applied, said out loud by the printed line) | a person is never asked again for a word they gave | K2 T1-T6; K1 W1 |
| E17 | conflicting pair: K1 refuses while K2's `says` was not shown (word recorded before the upgrade, or by the conductor from free words) | the branch applies the word all the same (D-0047); the printed line and the request say it was the person's word; the door names the way back | the word moves the factory (P13); its consequence is said out loud | K1 W1 (printed line) |
| E18 | `manual_scope` non-empty, all cases refused, automation half not yet run | non-goal (Q3): the automation runner still goes first (`:523`); the manual half closes on the re-entry | the automation half is untouched by this card | non-goal 6.2 |
| E19 | `refuse_case` write fails (OSError) | swallowed by `refuse_case` (returns False); the printed line still names the case; `manual_close`'s receipt still lists it | a failed write never stops the close nor hides the case | by construction (`driver_dialog.py:239`); no row |

### 3.1 `s6_no_stand` / `s6_stand_word` in a more responsible role (advice -> the branch that decides not to dispatch)

Before: `s6_no_stand` only changed what the automation half PROBES (K4) - an advisory skip. Now its words decide that a
manual walk is NOT dispatched and the cases are recorded `left_unchecked`.

ERROR DIRECTION tolerated: toward NOT dispatching only when a live word of the person stands and no stand is confirmed;
the cost of that error is a case left unchecked with a door back (honest, reversible: confirm a stand or revoke the
word). Toward dispatching is never tolerated under a live word. A false "no stand" over a CONFIRMED stand is
unreachable (first `return ""`).

Adversarial inputs that must stay on the safe side (each decided above): revoked word (E12, no word -> ask); word on
another stage (E11); word for another block (C6); `<placeholder>` match and empty decision (E12); `*` pass (E13, a pass
by the person's own wider word - counts); confirmed stand with words on file (E4, never no-stand); stand named + pending
(E2, no-stand by Lead decision); broken `stage_overrides` (E12); a word recorded on S5 only (E9, counts).

---

## 4. Data premise for the plan critic (PROJECT.md item 6 (a))

(a1) Readers of the word today (axis 26). Measurement (Grep tool, the designer's road; no shell in this role):
pattern `stand_block\(|STAND_NOT_CONFIRMED_BLOCK|stand not confirmed`, path `ai-packages/qa-factory/scripts`, glob
`*.py` (non-test hits):
`waiver.py:373,375,378,380` (the constant and the one builder); `check_delivery.py:1621,1625` (`stand_word`);
`driver_stage_s6.py:674,680,724` (`s6_no_stand`); `driver_stage_build.py:145,169,203` (`stand_check` and its seam
person); `driver_machine.py:3962,3968,3988,3990` (`_take_stand_answer`). `driver_stage_s6.py` `manual_lane_plan`
(`:1304-1336`) and `run_manual_block` (`:1566-1605`): no hit. Positive control of the same call: the same pattern finds
`driver_stage_s6.py:680`. Shell form for the critic to re-run:
`git -C <tree> grep -n -E "stand_block\(|STAND_NOT_CONFIRMED_BLOCK|stand not confirmed" -- "ai-packages/qa-factory/scripts/*.py"`.
This matches the axis 26 list exactly (`docs/SIBLING_MAP.md:455`).

(a2) `refuse_case(..., "left_unchecked")` and `manual_close` accept a refused case with no dispatch: carriers read -
`refuse_case` checks nothing and writes `{refused: {reason, door, by}}` (`driver_dialog.py:227-241`); `manual_close`
needs no dispatch (`driver_stage_s6.py:1025-1046`); the existing rows `t261_k2_..._not_dispatched` ("0 accepted: no
runner, no dispatch" ... `["finalize", "code_only", "stage_done"]`, `test_story_run_s6.py:452-459`) and
`t261_the_real_controller_..._takes_the_code_only_receipt` (the REAL controller completes S6 by `code_only` with TC-2
never dispatched, `:546-567`) pin it. Command (NOT run by the designer - no shell in this role; the Lead or the plan
critic runs it and pastes the tail here):
`python -B ai-packages/qa-factory/scripts/tests/test_story_run_s6.py` -> expected `=== test_story_run_s6: N/N ok ===`.
Gap the premise does NOT cover: both rows run with no accepted AUTOMATION dispatch before the close; the dry world has one
(fork F-3).

---

## 5. Siblings (rule 9; SIBLING_MAP)

- Axis 26 (the word): the manual half becomes a reader through `s6_stand_word`. **Lead places** (mechanism commit,
  `docs/SIBLING_MAP.md:455`, same commit as the merge of FV3-21): replace
  `` `Driver.stand_check` (`driver_stage_build.py`, S5) and `Driver.s6_no_stand` (`driver_stage_s6.py`, S6) call (HF8-4 P8) ``
  with
  `` `Driver.stand_check` (`driver_stage_build.py`, S5) and `Driver.s6_stand_word` (`driver_stage_s6.py`, S6; `Driver.s6_no_stand` is its bool) call (HF8-4 P8) ``
  and in the readers list replace `` `Driver.stand_check` and `Driver.s6_no_stand` (the S5 and S6 stand sites) `` with
  `` `Driver.stand_check` and `Driver.s6_stand_word` (the S5 and S6 stand sites; through it the automation half (`s6_no_stand`, K4) and the manual half (`manual_lane_plan` -> `manual_no_stand`: no walk, the cases `left_unchecked` in the person's words, FV3-21)) ``.
- Axis 5 (stage twins): S5 has no manual half; its `go on` text is the same site (K2), covered.
- Sibling refusals of the same family in the same artifact (sweep, rule 9): `stand_login_gate` (`:1249`, refuses with
  words, `left_unchecked`) - applied pattern; `walk_refuse_gaps` (`:27`) - not applicable (account, not stand);
  `gate_a_dry_person` `go on` (`:1013`) - not applicable (gate A, not stand); `deferred_decision` (`driver_dialog.py:559`)
  - not applicable (deferred answers). No other reader of the stand word in the manual half.
- S0 `go on without a stand for now` (`driver_s0.py:2361`): n/a - S0's word is "for now" and asked again before any
  test (`:2324-2326`); it records no S5/S6 pass.
- Noticed analog, NOT widened (reported): `check_delivery.stand_word` reads the bare `STAND_NOT_CONFIRMED_BLOCK`, while the
  driver reads `stand_block(environment)`; a word whose `match` is the whole block text passes the driver and not the
  delivery reader. Both are legal per axis 26; whether they must agree on every `match` form is fork F-6.

---

## 6. Non-goals (Q3, Lead decision)

6.1 The automation half (K4 stays). 6.2 A code-only close of the whole S6 when every automated result stands and all
manual cases are refused by no stand (`:523` still dispatches the runner because `manual_scope` is non-empty). 6.3 The
walk-retry versus coverage-gate interplay (`driver_dispatch.py:1371-1501`, `validate_artifacts.py:2108-2157`).
6.4 `docs/SIBLING_MAP.md` (the Lead places section 5's line). 6.5 `references/question-prices.json` (fork F-2).
6.6 The FV3-20 stub key (J2-1) and the `main/S6` label (J2-2): FV3-20's round.

---

## 7. Witness (narrowed, `plans/builder-rules.md` 7b)

The verification run is what this prints, run in the builder's worktree:

`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_stage_s6.py ai-packages/qa-factory/scripts/driver_stage_build.py ai-packages/qa-factory/skills/qa-story/phases/s6.md ai-packages/qa-factory/design/state-exits.md ai-packages/qa-factory/scripts/tests/test_story_run_s6.py ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red.json`

then every command it names, verbatim output. Expected among them (if the walk does not name one, the builder adds it
and says so): `test_story_run_s6.py`, `test_human_questions.py`, `test_story_run_words.py`, `test_state_exits.py`,
`test_driver_layers.py`, `test_walk_account.py` (it reads `manual_lane_plan`'s source: `walk_refuse_gaps` must stay
before the `s6_walkers_cap() != 1` test, `:449-450`; K1.c is placed before both and contains neither text),
`test_s6_reprove_manual.py` (stubs `s6_no_stand` and `run_manual_block`; unchanged), `test_judgment_census.py`,
`test_field_producers.py`, `test_scenario_dry_1.py --part main` (K3), `selftest.py --lang`. Plus the two probes of K1 and
the one of K2, each by byte copy with the hash comparison (hygiene point 7). Never CI, never a full set.

---

## 8. FR sections to walk (PROJECT.md package item 1; one line each)

A (FR-1/FR-2: the refusal's reason and door - the door names a road the person can take; FR-4: the branch is an
informed pass, never silent - the printed line); B (FR-6 the `says` clause and the reason against `human-questions.md`;
FR-9 the price of `go on`; FR-10 the packet does not contradict itself - see F-2); C (FR-8 the words carried to the
executor; FR-42 every returned state has a move); D (FR-40 the new state-exits row; FR-59 the unknown branch E15(c));
E (FR-36 a capability the standing decision forbids is not probed; FR-23 a null outcome recordable); F (not applicable -
no measurement changed); G (FR-30 English, no Cyrillic in fixtures - W4 uses `chr(0xE9)`; FR-32 root cause with test;
FR-33 - closed by code, not proved: a `live-runs` row is owed by the Lead).

---

## 9. Readers of every touched file (designer rule 7)

Grep, Grep tool, pattern
`driver_stage_s6|driver_stage_build|phases/s6\.md|test_story_run_s6\.py|test_story_run_stand_b|known_red|driver-layers\.json|state-exits\.md|changelog\.d`:
over `tools/` = 16 hits in 8 files; over `.githooks/` = 0; over `.claude/agents` and `.claude/skills` = 0 (positive control
of the same call shape: `SIBLING_MAP|test-layers\.json` over `.claude/agents` = 3 hits). Changed names
`s6_no_stand|stand_question_text|manual_lane_plan|s6_stand_word|stand_check` over `tools/` = 0 (positive control:
`journal_write|dispatch_new` over `tools/` = 128 hits). `.claude/hooks` does not exist; `.claude/worktrees` excluded
(other sessions' copies).

| file touched | readers found | verdict |
|---|---|---|
| `scripts/driver_stage_s6.py` | in package: `driver-layers.json` (homes), `test_walk_account.py:449` (source read of `manual_lane_plan`), `test_s6_reprove_manual.py:118` (stubs `s6_no_stand`), `walk_pool.py:15` (docstring) | layers: changes in this stream (K6); others unchanged |
| `scripts/driver_stage_build.py` | `driver-layers.json:623` (`stand_question_text` row) | unchanged (no new name) |
| `skills/qa-story/phases/s6.md` | `test_words_doors.py` map names `phases/s5.md` only for the stand door | unchanged |
| `design/state-exits.md` | `test_state_exits.py` (doors), `tools/test_test_quarantine.py:863` (a fixture string) | unchanged |
| `scripts/tests/test_story_run_s6.py` | `test-layers.json` (keep row `gate_named`), `tools/lint-baseline.json:271` (pyflakes ratchet: the diff adds no pyflakes finding), `test_conductor_doors.py:671` (names the file for `s6.stand_confirm`), `driver-golden-rules.json` (patch notes, on-demand recorder) | unchanged |
| `scripts/tests/fixtures/driver-layers.json` | `test_driver_layers.py`, `driver_golden.py`, `tools/test_quarantine.py:2173` (purge on deletion) | unchanged |
| `scripts/tests/fixtures/driver-exits/known_red.json` | `scripts/tests/known_red.py` only (its `_about`) | unchanged |
| `changelog.d/fv3-21-...md` | `tools/architecture_gate.py:12` (a package path: the commit needs the `architecture:` line), `tools/test_volume.py:16` (excluded dir), `tools/test_piles_form.py:58` | unchanged |
| `docs/SIBLING_MAP.md` (Lead) | not this stream | Lead's commit |

Parallel streams that meet these readers: FV3-20 (t-1098 fix round) owns `known_red.json` and `dry_stub.py` - hence F-4.

---

## 10. Forks (returned, not decided)

**F-1 — the executor of K4 on the skill road (P31, designer rule 6).** On the skill road the orchestrator starts the
manual half with `story_step.py start --execution-kind manual` (`s6.md:10`); `story_step.py` reads no stand fact (grep
`stand`, case-insensitive, finds no stand check). K4's sentence tells it not to dispatch, but the skill road has no
command that refuses the cases with the words and writes the code-only close; the controller refuses a completion over an
undispatched manual-agent case (C4). Options: (a) K4 as written + a named node FV3-21b (owns
`scripts/story_step.py`, `scripts/tests/test_story_step_manual_block.py`; test: `start --execution-kind manual` with the
word refuses each case `left_unchecked` with the same reason/door, registers no dispatch, and prints the close door) whose
spec is drafted after one scout question: "how does the skill road close S6 today when `prepare` refuses every manual
case?"; (b) move the refusal into `manual_evidence.prepare_for_block` (shared by both roads, AR-15) in this card - but
`prepare_for_block` writes no `by` (`_write_refused`), runs AFTER `manual_gate_note` (a pointless gate-A question first),
and widens owns to `manual_evidence.py`. Recommendation: (a); the reason/door text moves to a shared home when FV3-21b is
specified. The card is executable as written under (a).

**F-2 — the price row of `s6.stand_confirm` `go on`.** `question-prices.json:248` says `delivery: not_known`,
`unverified: which stand the tests ran on`. With manual cases left unchecked the story line under-states what stays
unverified, and the measured delivery may read `no` (the stand-login `go on` row says `no`, B-F1). Options: (a) `says`
only (Q3 item 2; `not_known` stays true as a class); (b) a variant key `s6.stand_confirm.manual` with its own
`unverified` and `delivery` (census of keys, `test_conductor_doors.py` map, prices loader); (c) widen the one row's
`unverified` text for every world. Recommendation: (a) now; the plan critic judges FR-10 on the measured delivery word
of the K1 world.

**F-3 — the consumer record at `manual_close` in a world with an accepted automation runner.** In the dry world
`S6-qa-runner-1` (automation) is accepted with `complete=False` (`:573`, manual half pending), so no consumer acceptance
was asked for it. With no manual dispatch, `manual_close` -> `consumer_need_record` (`:309-326`) finds author
`S6-qa-runner-1`, no accept record, and may REFUSE (`S6 cannot be closed at manual_close: no accept record of ...`).
The critic's edge row says "no new handling"; the existing premise rows run with no accepted automation dispatch.
Options: (a) the builder adds K1 row W13 (consumer on, accepted automation author, no record) and measures; if refused,
it STOPS and returns the measured refusal as a question (no invented fix); (b) the card decides now that the branch
requests the consumer's acceptance of the automation runner before `manual_close` (new design, needs `consumer_completion`
read). Recommendation: (a); the K3 re-measure of the dry pass shows it either way.

**F-4 — sequencing after FV3-20.** FV3-21's K3 and its witness need FV3-20's merged branch (5979acb4 + J2 fixes) on
`main`. Options: (a) FV3-21 waits for that merge; (b) FV3-21 merges `main` after FV3-20 lands and resolves
`known_red.json` itself (TEAMWORK § 3). Recommendation: (a).

**F-5 — the node of the new `known_red` row** (the next stop, expected S7 stub gap). The Lead names it (an existing S7
stub node or a new one); until then the row carries `node: FV3-21` and a `note` that its owner is owed.

**F-6 — `check_delivery.stand_word` vs the driver's reading (noticed analog, another zone).** Offered as a finding for
the pile that owns delivery; not this card.

## 11. Small choices the designer closed (listed so the Lead can stop them)

- The clause text `an agent checks no case by hand` (one text, true in every world) instead of the critic's `the cases
  an agent checks by hand are left unchecked` (presupposes cases; wrong for the unreadable-scope world).
- The clause condition read once in `stand_check` through `stage_scope("S6", "manual")` for all four sites, instead of
  `kind` at S6 and plan rows at S5 (two readers; the relaunch site of the automation half would miss it).
- The door text follows the sibling shape (`stand_login_gate`, `deferred_decision`: "...; the next run checks it by
  hand") instead of the critic's "(retry at gate B)" (a gate-B retry road for these cases was not found in the carriers
  read).
- `manual_todo` and `s6_unsettled_cases` extracted (one predicate each, AR-15) rather than copied expressions.
- Console quote through `s0_quote` (as `stand_check` prints the same word), request.json reason whole.
- `waiver.py` docstring of `stand_block` ("both callers") left as is: `s6_no_stand` still reaches it, through the helper.
- `design/state-exits.md` added to owns (AR-25 change check demands the row; defect in the node's own reach).
- Test rows in `test_story_run_s6.py` only (keep row); `test_story_run_stand_b.py` is QUARANTINED (`test-layers.json:10246`
  cohort entry), so no row there.

## 12. Q3 item / edge row -> where in the card

| Q3 item / edge row | where |
|---|---|
| Q3 item 1 (`manual_lane_plan` branch, reason, door, helper) | K1 (K1.a-K1.d), test row K1 |
| Q3 item 2 (`stand_question_text` `says`) | K2, test row K2 |
| Q3 item 3 (SIBLING_MAP axis 26) | section 5, "Lead places" |
| Q3 item 4 (`phases/s6.md`) | K4; fork F-1 |
| census tests of question texts | K2 last paragraph; witness section 7 |
| `known_red.json` | K3; forks F-4, F-5 |
| changelog fragment | K7 |
| edge: no stand + go on | E1; W1, W2 |
| edge: named not confirmed + go on | E2; W3 |
| edge: no stand + stop | E3; C2 |
| edge: confirmed stand | E4; C1 |
| edge: manual-human case | E5 |
| edge: done by an earlier accepted dispatch | E6; W7 |
| edge: held by a deferred question | E7; W8 |
| edge: with a consumer | E8; fork F-3 |
| Lead (c): word on S5 vs S6 | E9; W2 |
| Lead (c): environment empty vs pending | E10; W1, W3, C1 |
| Lead (c): word for another stage | E11; C4 |
| Lead (c): broken `stage_overrides` | E12; C3, C5 |
| Lead (c): error direction of the reused function | section 3.1 |
| Lead (a): data premise | section 4 |
| Lead (b): AR-n, owner, census class | sections 1.2, 1.3 |
| temporal edge (earlier life dispatched a block) | E15, E16; W9, W12 |
| reason/door text vs `human-questions.md` | K1.c steps 3-4; K2.a |
| owns, witness, FR sections | sections 0, 7, 8 |

## Reading trail

Read: `docs/tasks/specs/reviews/t-1106-dry-s6-manual-half-diagnosis.md` (whole); `scripts/driver_stage_s6.py` 1-90,
480-699, 895-1064, 1245-1354, 1560-1667 and `consumer_need_record` 309-326, `consumer_pending`/`consumer_awaits` 158-177;
`scripts/driver_stage_build.py` 25-324; `scripts/driver_dialog.py` 215-241, 435-464, 555-583, 775-778;
`scripts/waiver.py` 150-399; `scripts/contract.py` 158-174; `scripts/driver_core.py` (`_write_json` 313-323; exception
classes); `scripts/driver_runner.py` 391-405; `scripts/driver_dispatch.py` 2937-2941; `scripts/driver_s0.py` 2310-2369;
`scripts/check_delivery.py` 995-1029, 1605-1625; `scripts/manual_evidence.py` 1282-1317; `scripts/acceptance.py`
1430-1451; `references/question-prices.json` 1-30, 240-255; `references/human-questions.md` 13-63;
`design/architecture.md` 134-181, 249-282; `design/state-exits.md` 66-73, 205-211; `skills/qa-story/phases/s6.md` 1-45,
75-124; `scripts/tests/test_story_run_s6.py` 1-75, 321-567, 1714-1803, 2123-2149, 2400-2494, 2737-2775;
`scripts/tests/story_run_common.py` 188-226, 337-351, 511-571; `scripts/tests/test_s6_reprove_manual.py` 35-40, 95-139;
`scripts/tests/test_story_run_s6_w1_frozen.py` 170-205 (+ grep: it stubs `stand_check`; its story's `environment:
"local"` is confirmed, so the branch is not taken there); `scripts/tests/test_story_run_stand_b.py` 100-189;
`scripts/tests/test_story_run_stand_identity.py` 900-934; `scripts/tests/test_human_questions.py` 455-484;
`scripts/tests/test_story_run_words.py` 1-80; `scripts/tests/test_check_delivery.py` 495-554;
`scripts/tests/test_state_exits.py` 1-40; `scripts/tests/fixtures/driver-exits/known_red.json` (whole);
`scripts/tests/fixtures/driver-layers.json` 1-20, 636-655; `scripts/tests/fixtures/judgment-census.json` 1-12 (+ grep);
`scripts/tests/test-layers.json` 6174-6229, 10240-10259 (+ grep of keep rows); `scripts/tests/test_field_producers.py`
(grep); `scripts/tests/dry_stub.py` (grep `STUB_KEY`, `resolve_newest`); `changelog.d/fv1-5-stand-check-words.md`;
`tools/architecture_gate.py` 1-45; `tools/lint-baseline.json` 1-12, 265-274; `docs/SIBLING_MAP.md` 453-455;
memory note `stale-local-main-checkout.md`.

Negative claims and their controls: "manual_lane_plan never reads the word" - grep of the word's readers lists no hit in
`:1304-1336` (control: hit at `:680`); "story_step.py has no stand check" - case-insensitive grep `stand` in
`story_step.py` returns only unrelated uses (control: same call finds 20 lines); "5979acb4 is not on main" - grep
`resolve_newest|STUB_KEY\s*=` finds only `STUB_KEY` at `:749` (control: the same call found the STUB_KEY line);
"`human-questions.md` is not under `design/`" - Glob over `design/` empty, the same Glob over `references/` finds it (the
brief says `design/human-questions.md`; the carrier is `references/human-questions.md`).

Brief contradictions noticed: the brief cites `design/human-questions.md` (actual: `references/`); the brief's
known_red consequence presumes FV3-20's row is on `main` (it is not: F-4).

## Lead decisions on the forks (17.11.2026, Lead of the batch; by recommendation, before the plan critic)

- F-1 = (a): K4 as written; the skill-road executor is node FV3-21b, drafted right after this card (same day, not parked).
- F-2 = (a) now; the plan critic judges FR-10 on the measured delivery word.
- F-3 = (a): the builder adds row W13 and measures; a refusal is returned with its text.
- F-4 = (a): the card waits for the FV3-20 branch (5979acb4 + the J2 fix round t-1109) on main.
- F-5: the new `known_red` row carries `node: FV3-21` with the note until the Lead names the S7 stub node.
