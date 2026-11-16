# t-902 — plan critic: Architect tier spec (20261116-architect-tier-spec.md)

Reviewer: critic (opus), 17.11.2026. Object: `docs/tasks/specs/20261116-architect-tier-spec.md` (678 lines), read whole,
together with its "Lead decisions on the forks" section. Tree: root checkout, HEAD = origin/main = `0d6f61b1`
(checked: `git rev-parse HEAD origin/main` returned the same sha twice).

**Verdict: GO WITH FIXES.** The design is sound. It has one ladder home, ranks by function, `by` stays a model word,
Fable unavailability is not a degradation, and the Architect is never a subagent. Four findings block every builder
dispatch. Each fix is a few spec lines and none needs a redesign. My recommendation: the Lead edits the spec itself as
a continuation, then the dispatches go out. Accepting this verdict is the Lead's decision, not mine.

---

## Premise re-check (empirics first; 20 premises, one command each)

| # | result | command → output |
|---|---|---|
| P1 | holds | `delegation.config.yaml:21` `model: claude-fable-5-1` (Read) |
| P5 | holds | grep mechanism_gate.py → `208:LEAD_FAMILIES = ("fable", "opus", "sonnet", "haiku")`, `673:ROLE_RANKS = {"scout": 0, "builder": 1, "critic": 2, "lead": 3, "reserve": 4}` |
| P6 | holds | grep → `592/596: return "fable"`, `600: return model or "fable"` |
| P7 | holds, and LOAD-BEARING for B1 | probe `tier_declared_ok(d, resolve_lead_binding(cfg), cfg)` on the live config → `opus False`, `claude-opus-5-5 False`, `fable True`, `sonnet False` |
| P8 | holds | `mechanism_gate.py:790 return max(exact_matches)` |
| P10 | holds | `grep -n '^#' CURRENT_CONTEXT.md` → only `Current Context / Maintenance Rule / Current Milestone / Current Task`; note text `mechanism_gate.py:866` |
| P11 | holds | `MECHANISM_PREFIXES` (209-285) holds `PROCESS/`, `tools/journal_validator.py`, `logs/journal-letters.json`... and no `delegation.config.yaml`. Its only hits are the docstring `:98` and `CONFIG_PATH :206` |
| P12 | holds | `journal_validator.py:345 TIER_ORDER = {...}`, `:346 AGENT_TIER`, `:366 QUEUED_TO_LEAD_AGENTS = {"critic", "designer"}` |
| P13 | holds | read 660-800: `:676 if agent == "lead": return None`; unknown-`by` FAIL; `:762 TIER_ORDER["opus"] > agent_tier`; `:780 by in ("sonnet", "opus")` |
| P14 | holds | `:1100-1102` «HEAD and seed lines contribute their ids ... none of them is judged» |
| P15 | holds | `:1287-1297` an `escalated` whose task_id is not in `seen_task_ids` is a violation |
| P16 | holds (lines drifted) | `session_context.py:222 ("fable", "Lead(top)")`; text now at `:1045` (spec says 1031-1033) |
| P17 | holds (lines drifted) | `:183 MAX_LINES = 25`; `:2192 lines = [now_line(now), model_line(stdin_payload)]` (spec says 2180) |
| P18 | holds (line level) | `.claude/settings.json:2 "model": "claude-fable-5-1"`. `git grep settings.json` over 16 non-test tools gives no line that also says model |
| P19 | holds, with one carrier missing | `git grep -i '"fable"'` over non-test tools finds every carrier the spec lists, plus `token_usage_stats.py:119 FAMILY_ORDER = ["Haiku", "Sonnet", "Opus", "Fable"]`, which the spec does not list (M7) |
| P20 | holds | `journal_write.py:75 LEAD_ROWS = {"lead_degraded": ...}` |
| P22 | holds (growing) | `cat logs/journal/*.jsonl \| grep -c -E` → `by fable 663` (spec 656), `by opus 278`, `queued-to-lead 73`; only one journal file exists (`dev1.jsonl`) |
| P23 | holds | `grep -rln -i lead-queue docs/tasks/*.md tools/*.py` → none. Control: `grep -rl lead-queue-fable docs` → 2 files (snapshot, this spec), so the tool works. Title read at `lead-queue-fable.md:1` |
| P30/P31 | holds | `git grep -i -E 'next-task\|skills/onboarding\|onboarding skill'` outside history → exactly the readers listed in P30. `install_parity_anchors.json` has no onboarding hit (`git grep -c -i skills` → 3, dir unit) |
| P33 | holds, but see M3 | `batch-7-vhodyashchie-4.md:3` «статус: ожидает \| взял: —»; rows FG7-14 `:37`, FG7-33 `:56`. **FG7-54 already exists at `:77`** |
| P34 | holds | `docs/TESTING.md` «новый тестовый файл не создаётся» |

Extra measurements the spec lacks:

- **(E1)** Session model ids in the journal: `grep -o '"model": *"claude-fable-[0-9-]*"' dev1.jsonl | sort | uniq -c` → `4 "claude-fable-5-2"`. The live Fable sessions run `claude-fable-5-2`. The config binds `claude-fable-5-1` (`:21`) and so does `settings.json:2`.
- **(E2)** Existing `escalated` lines: 5 of them, for example `{"event":"escalated","agent":"builder","model":"opus","task_id":"t-133",... "attempt 3 on an opus builder"}`. The convention is that `agent` names the role escalated and `model` names the model the work moves TO.
- **(E3)** `queued-to-lead` clearing practice: a script over dev1.jsonl → `queued tasks 71 with a second accepted 2`. The 16.11 `lead_restored` notes accept the window as a whole.
- **(E4)** `handoff_gate.py:144` gates only `WRITE_TOOLS`. `journal_write.py` has no `agent_id` or subagent check: grep found nothing, while the same grep finds `agent_id` in `journal_echo.py:622` and other files.

---

## BLOCKERS (change the spec before any builder starts)

### B1 — §7 order and the committer: as written, the Opus Lead cannot commit streams A-F

- **What is wrong.** §7 says builders hand over content and "the Lead (Opus, after the critic of the topic) commits" the
  mechanism-path commits of A, B, C, D and F. Stream L flips `roles.lead` to Opus LAST.
- **Evidence.** Until L lands, `delegation.config.yaml` binds lead to Fable. The tier gate then refuses `tier: opus`
  and `tier: claude-opus-5-5` (probe output: `opus False`, `claude-opus-5-5 False`, `fable True`). Every owned file of
  A-D, and `PROCESS/` plus `docs/SIBLING_MAP.md` of F, is in `MECHANISM_PREFIXES`.
- **Consequence.** As planned, each mechanism commit is refused, or someone writes a false `tier: fable` line.
- **Fix (pick one, state it in §7):**
  - **(a) [recommended]** A-F and L are committed by a **Fable** session (`tier: fable`). The current coordinator is
    Fable: the journal's last accepteds carry `by: fable`. This is the concept `mechanism_gate.py:820-833` already
    encodes: "the transitional commit re-binding Lead is committed BY a session of the old, higher tier". There is no
    transitional window at all.
  - **(b)** Flip the config first, as move L0. It is ungated today, because the config is not a mechanism path until
    stream A adds it. Then STATE the transitional world (rule 11 (i)). The old validator still ranks by family, so the
    Opus Lead accepts critic/designer work only through `basis: queued-to-lead`. That is legal at `by: opus` (`:780`),
    but each such line is the Lead queuing work to itself, and somebody must clear those lines after B lands.
- **Also state:** the gate reads the WORKING-TREE config (`CONFIG_PATH = REPO / "delegation.config.yaml"`, `:206`). So
  under (b), or for the L commit itself, an Opus `tier:` passes only once the flipped file is on disk.

### B2 — §5.4 / §4.4 (D4 execution path): the ARCHITECT line is not printed for the model id that actually runs

- **What is wrong.** The ARCHITECT line prints only when `function_of_session(model) == "architect"`. The §5.4 cases
  are "id matches a binding" and "Claude family bound to nothing". The live case is neither: the family IS bound, but
  the id differs.
- **Evidence.** The live Fable session id is `claude-fable-5-2` (E1). The binding is `claude-fable-5-1`. Unless the
  builder invents a family match, the start checklist (D4) is never encountered.
- **Asymmetry.** `rank_of_model` §2.2 (b) already handles this case through the family. Two different matching rules
  for one fact (the function of a model) is two roads (P31 / AR-13).
- **Fix.** Define `function_of_session` as the function of `rank_of_model(model_id, config)`: exact match, else family,
  one road. Add the §5.4 case "family bound, id differs → that function, note `(family match: <binding>)`". Add a test
  row with `claude-fable-5-2` against a `claude-fable-5-1` binding.

### B3 — Work with no owner and edits left to the builder (PROJECT.md «Командная работа» п. 11, rule 11 checklist item 4)

1. **The F9 marker has no stream.** The Lead decided F9 (a): a typed field `reviewed_through` on `calibrated`. That
   needs a validator shape rule and a `journal_write.py calibrated --reviewed-through` option
   (`journal_write.py:675` today allows `opt=("agent", "model", "feature", "category")`). Neither appears in any
   stream's edges or DoD. Stream B owns `journal_write.py` "only under F6".
2. **Stream B is missing a test file in its owns.** Its DoD names `tools/test_journal_write.py`, but its `owns:` does
   not list it.
3. **CLAUDE.md's SHAPES table is not in stream L's list.** The `escalated` row says "`task_id` (must already exist
   earlier in the file)", which F6 changes. The `calibrated` row needs the new field from F9. L lists only «Tiers»,
   «Role ≠ tier», «Lead degradation» and the `by` paragraph. If those rows stay as they are, the policy text and the
   validator contradict each other.
4. **§4.5 step 4 leaves the reader undecided.** It reads "stream C extends `open_dispatch_lines` ... or a small choice:
   a grep command named here", and no stream's edges include either option.
   - Note: `escalated` is a CLOSING lifecycle event for the open-dispatch reader (`session_context.py:17,233`
     `_OPEN_LIFECYCLE_EVENTS`). So the existing reader never reports an open escalation, and a new reader is real
     work, not an extension.
   - **Fix:** decide it. Recommended: name one concrete command in the checklist, owned by stream F. Alternatively,
     give stream C an `ESCALATED TO ARCHITECT: N` count with its edges.

### B4 — §2.4, §5 (self-certification): with lead = critic = designer on one model, the guarantee rests on a "never" that no code enforces and no detector watches

- **What is wrong.** The spec rests the critic's independence on "a critic subagent never writes `accepted` lines (only
  the coordinator does) ... separate context (D2)".
- **Evidence.**
  - Nothing on the execution path enforces that "never". `handoff_gate` gates only WRITE_TOOLS (`:144`), and
    `journal_write.py` has no subagent check (E4).
  - Under F4-A an Opus subagent writing `by: opus` ranks as **lead** (P8 max rule). An Opus session can therefore
    certify Opus work with nothing distinguishing it except context. Before the switch Fable sat a model above the
    critic, so this hole did not matter. Now it is the whole guarantee.
  - Rule 10 (c)/(d) requires a registered detector and an answer to "what stops a skip". The §1 check table names
    neither for this case.
- **Fix (both cheap):**
  - **(i) Code on the path.** The PreToolUse Bash hook, or `journal_write.py` itself via the hook payload's
    `agent_id`, refuses `accept`/`reject` from a subagent payload. The refusal follows FR-1/FR-2, for example: "an
    acceptance is written by the coordinator's main chain; return your verdict in your handoff file".
  - **(ii) A detector.** Either a validator WARN or a calibration check, registered in
    `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: an `accepted` with `agent ∈ {critic, designer}` at a lead-ranked `by`
    must have an earlier `delegated` of that same agent on that task with a `worker_ref` of the form `agent:<id>` (a
    real separate context). The validator already tracks `delegated_agents` and `task_worker_refs`
    (`journal_validator.py:545-547`), so the WARN is about 10 lines.
  - "Fresh context" thereby becomes checkable by code for shape. Its meaning stays with calibration (the Architect).

---

## MAJOR (fix in this round; not dispatch-blocking one by one)

- **M1 — §5.3 and rule 6, escalation and outage above Opus: a state with no move (AR-25).**
  - *Escalation.* Rule 6 says two rejected → "one tier up". For critic- or designer-class work on Opus, one tier up
    is now Lead, the same model, which is meaningless. The next model up is Fable, the Architect, which is never a
    subagent (D8). The spec does not say where a twice-rejected critic or designer task goes.
  - *Outage.* An Opus outage now removes Lead, critic and designer at once. The Sonnet coordinator may accept a
    builder diff "ONLY with critic input". `queued-to-lead` is illegal for builder (`journal_validator.py:780`), so
    every builder diff simply waits.
  - *Fix.* State both moves. Escalation above Opus is an architect-queue item plus `escalated` (the §4.3 road). During
    an Opus outage, builder diffs wait in `lead-queue.md`.
  - *Question for the owner* (an intent question, rule 11a): may a critic subagent run on Fable when Opus is down, or
    does D8's "never a subagent" cover any Fable subagent?

- **M2 — D3 "once a week": nothing on the Lead's path triggers it, and no detector is registered.**
  - Step 6 (calibration) lives only in the Architect checklist, which loads only when the owner has already switched
    to Fable. If the owner does not switch for a week, the Lead sees the generic `Last calibration` line. Under F10
    the Lead has no move but to "tell the owner"; that move is not written anywhere and nothing records it.
  - *Fix.* When overdue (more than 7 days) and the session is not an Architect session, the line says «calibration /
    Architect review overdue -- ask the owner to switch to the Architect». The Lead writes an architect-queue item.
    Register a calibration check on the age of `reviewed_through` (rule 10 (c)).

- **M3 — D7: the П3 node already exists.**
  - `batch-7-vhodyashchie-4.md:77`: «FG7-54 \| П3 \| Экзамен лида для Опуса ... (слово владельца 16.11: «запиши как
    узел П3. Когда-нибудь прогоним») \| Lead (Архитектор запускает)».
  - §6 (last row) and stream L instead create a "new П3 node + findings file + card row". That is a duplicate, and it
    drops the owner's executor note.
  - *Fix.* Reference FG7-54; drop the new node, finding and card row. Stream F's edit of `LEAD_RANKING_EXAM.md` should
    also reword `:3` («distinguish the Lead tier from the builder/critic tier»): with Lead and critic on one model,
    that purpose sentence is false.

- **M4 — F18 (Lead decided (a)): the decision should change to (b), no cutover.**
  - The legacy pair guards only against late-merged lines that were ILLEGAL under the old table. Such lines cannot be
    in a committed journal: `.githooks/pre-commit:8` runs the validator, `pre-merge-commit:18` runs `--merge-parent`,
    and CI `forge-check.yml:72` runs `--all --base "$BASE"`.
  - The spec's own pair-by-pair check (§3.4) shows every old-legal pair stays legal under the new ranks.
  - F18 (a) therefore buys protection only against `--no-verify` lines that CI would already flag. It costs a second
    table, which is two roads for one fact.
  - It also carries a temporal edge the spec leaves open: C2 says "B leaves a placeholder", but not its value or what
    it does before L. It also creates a TZ edge: `ts` is local time without a zone, compared across clones.
  - *Fix.* Take (b). If the Lead keeps (a), state the placeholder (for example `"9999-12-31"`, so everything stays
    legacy until L) and the cross-clone TZ caveat.

- **M5 — F2: a third option the fork misses.**
  - Option (c): put the home inside an existing leaf with an existing test file, for example `tools/tier_echo.py` with
    rows in `test_tier_echo.py` (tier_echo already owns `KNOWN_TIER_WORDS` and imports only stdlib plus
    `transcripts`).
  - That avoids both costs of the fork: the new test file (TESTING.md) and making the validator and hooks import the
    commit-msg gate (`mechanism_gate.py:188 import yaml` at module top).
  - Whatever the location, import `yaml` lazily inside `bindings()`. Then `tier_echo`, `dispatch_gate` and
    `journal_hooks`, which need only `FAMILIES`, take no pyyaml dependency on the hook path.

- **M6 — C3 / §2.2 against §2.4: two behaviours for a bad config.**
  - §2.2 says a config over 64 KB is "refused with a door". §2.4 says an unparsable config falls back to legacy ranks
    ("can only make acceptance STRICTER").
  - The spec does not say who is refused: the commit, the session, or the validator run. Nor does it say what the
    door is (FR-1/FR-2).
  - Separately, `yaml.safe_load` still expands aliases, so a size cap alone does not stop an alias bomb.
  - *Fix.* Oversize or alias-heavy means unparsable, which means legacy ranks plus one WARN line. No new refusal.

- **M7 — §2.3, a P31 residual.**
  - `tools/token_usage_stats.py:119 FAMILY_ORDER = ["Haiku", "Sonnet", "Opus", "Fable"]` is a second ORDER carrier.
    §2.3 lists only `family()` at `:172`.
  - *Fix.* Derive it from `FAMILIES` (display case stays local, C4). Add it to stream D's function list.

- **M8 — §4.3, the semantics of `escalated` fields.**
  - The spec sets `model` = the Lead's own model. Existing lines use `model` = the model the work moves to (E2), and
    calibration check 4 reconciles `model` against transcripts.
  - *Fix.* For `agent: architect`, `model` is the architect binding. Otherwise state the new meaning in the CLAUDE.md
    SHAPES row (together with B3.3).

- **M9 — §3.5, an invented backlog.**
  - "Every `queued-to-lead` acceptance — the 73 old ones ... — is cleared by a Lead-ranked session ... a later
    `accepted` ... as today". Measured (E3): 71 tasks, only 2 with a second accepted. Today's practice is the
    `lead_restored` window acceptance.
  - *Fix.* Old items are already closed by the written window acceptances, so no backlog is owed. For new items, name
    the carrier: one road, either a second `accepted` or a `lead-queue.md` line, not both.

- **M10 — No order is recorded against the parallel spec.**
  - `20261116-boot-by-topic-spec.md` touches `session_context.py`, `test_session_context.py`, `docs/SIBLING_MAP.md`,
    `mechanism_gate.py` and CLAUDE.md, the same files as streams A, C, F and L. Its Phase 0 (`:351`) requires this
    spec to be merged first.
  - *Fix.* Add the reciprocal order line (PROJECT.md «Командная работа» п. 3 `очередь: architect-tier → boot-by-topic`)
    to both specs, or to their nodes.

## MINOR

- **m1.** Premise line numbers drifted (P16, P17), and the P22 counts grow. Re-read them at dispatch (rule 11 checklist
  item 5).
- **m2.** §4.1 says new-idea steps 1-4 "may run in an Architect session". PROJECT.md «Как разрабатывается новая идея
  владельца» is not edited by any stream, so the owner's «большое буду сначала обсуждать с фейбл» lives only in this
  spec. Optionally add one line to PROJECT.md in L.
- **m3.** Stream D's DoD reads "green with no test edit". If the home lands under F2-b, `tier_echo` imports a gate
  module, which is fine for tests but should be said in D's edges.

---

## Fit to D1-D8

| D | verdict |
|---|---|
| D1 | kept (§1, §4.3) |
| D2 | kept in the matrix (§3.1). The "fresh context" half has no guarantee: B4 |
| D3 | kept in principle; the weekly trigger is missing: M2 |
| D4 | the list exists (§4.5); it is not on the path for the real session id: B2. Step 4's reader is undecided: B3.4 |
| D5 | kept (§5.2). F21 widens it to the Architect writing too; sent to the owner, fine |
| D6 | kept. Readers verified (P30), install parity and AGENTS.md unaffected (verified) |
| D7 | WIDENED by a duplicate node: M3 |
| D8 | kept (§4.2, F6). Rule-6 escalation above Opus has no target: M1 |

F10 (the Architect runs the whole weekly calibration) widens D3, which speaks of reviewing rule changes. It is correctly
sent to the owner.

## Lead fork decisions that should change

- **F18** → (b): M4.
- **F2**: add option (c) before asking the owner: M5. It may remove the need for the owner's TESTING exception.
- **F9** (a): keep, but assign it to stream B and to the CLAUDE.md SHAPES table (B3.1, B3.3). Cheaper alternative, if
  the Lead prefers to postpone: the window starts at the ts of the last `calibrated` line (no schema change), and the
  field is added on the first evidence of need.
- **F6** (a): keep, but stream L must edit the CLAUDE.md `escalated` row (B3.3), and the `model` meaning must be fixed
  (M8).
- All other decisions (F1, F3, F4-A, F5, F7, F8, F11, F12, F14) are sound as decided.

## What the plan does NOT need (cheapest plan that keeps D1-D8)

1. The F18 legacy pair and `LADDER_FROM` (M4).
2. The C3 64 KB refusal (M6): fold it into "unparsable".
3. The F15 SessionStart pin WARN: the `settings.json` value alone delivers F15 (a). Postpone the pin until a mismatch
   is actually seen.
4. The `--list --since` mode can be postponed, with checklist step 5 using
   `git log --since=<d> --name-only --format='%h %cd %s'` plus `mechanism_paths`. This is optional: the mode is cheap
   and is one road, so keeping it is also fine.

## Standing questions (critic-diff-brief items 6, 7, 12, 5)

- **One road (item 12, P31).** After the fix there is one home and one set of readers for the ladder, with two
  residuals: `token_usage_stats.FAMILY_ORDER` (M7) and the session-function matching (B2). If F18 (a) stays, there are
  two tables (M4). No language/project/case exclusion found.
- **Duplication and consistency (item 6).** Duplicate П3 node (M3); two clearing roads for `queued-to-lead` (M9); two
  bad-config behaviours (M6). Grepped: `"fable"` literals in tools, `opus.{0,40}sonnet` family lists, FG7-54.
- **Code quality (item 7).** Not applicable, no code yet. Design-level: lazy yaml import (M5).
- **Tests (item 5).** The plan follows TESTING.md: rows in existing tables; a new file only by the owner's word.
  Option (c) of M5 removes the exception.

## Readers spot-check (§6, three by `git grep`)

All three hold:

- `git grep -c 'delegation\.config' -- tools/` → total 29 in 12 files. Matches §6.
- `TIER_ORDER|AGENT_TIER|QUEUED_TO_LEAD_AGENTS` → 35 in 4 files. Matches.
- `Lead tier = fable|Lead\(top\)|critic-tier` → 13 in 3 files. Matches.

Streams A, B, C, D and F own disjoint files (checked from the §7 lists). The overlaps are with the parallel spec (M10).

## What I did not check

- The bodies of the two skills to be deleted.
- `install_parity` behaviour after the deletion (only the anchors were grepped).
- Whether `settings.json` carries skill permissions.
- Second-developer clones: the config is tracked, so the switch is global for every developer of the forge. I did not
  check whether another developer's Lead sessions are affected, and the Lead may want to tell them.
- The bodies of the other two parallel specs, beyond the grep in M10.
- `test_mechanism_gate.py`'s `duplicate_model_id` cases.
- P9, P21, P24-P29, P32, P35, P36 were taken from the spec without re-running.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 s7: the Opus Lead cannot commit mechanism streams A-F before L flips lead (probe: tier_declared_ok opus False with the live config); commit by Fable, or flip the config first and state the transitional world",
    "B2 s5.4/s4.4: the live session id claude-fable-5-2 differs from the binding claude-fable-5-1 and no case covers it, so the ARCHITECT line (D4) is not printed; function_of_session must use rank_of_model (exact, then family)",
    "B3: F9 reviewed_through has no stream; test_journal_write.py not in B owns; the CLAUDE.md SHAPES rows escalated/calibrated not in L; checklist step 4 reader undecided (escalated is a closing lifecycle event)",
    "B4 s2.4/s5: lead=critic=designer on one model; the claim that a critic never writes accepted lines has no code gate (handoff_gate gates write tools only; journal_write has no subagent check) and no registered detector (rule 10 c/d)"
  ],
  "class_completeness": "Ladder carriers walked by axis 34 and axis 1: all listed carriers confirmed; one missing (token_usage_stats.py:119 FAMILY_ORDER, M7). Session-function matching is a second road beside rank_of_model (B2). Rule-text carriers naming top tier or Fable grepped over live docs: covered by streams F/L except the LEAD_RANKING_EXAM purpose line (M3) and the CLAUDE.md SHAPES rows (B3).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261116-architect-tier-spec.md (whole)",
      "delegation.config.yaml (whole)",
      "tools/mechanism_gate.py:575-615, 820-885, 209-285 (grep)",
      "tools/journal_validator.py:340-370, 525-620, 660-800, 1098-1103, 1260-1300, 1780-1800",
      "tools/session_context.py:10-30, 218-228, 555-600",
      "tools/journal_write.py (grep escalate/calibrated)",
      "tools/handoff_gate.py (grep)",
      "logs/journal/dev1.jsonl (grep counts, escalated lines, lead_restored)",
      "plans/piles/forge/batch-7-vhodyashchie-4.md:3,37,56,77",
      "docs/tasks/specs/20261116-boot-by-topic-spec.md (grep)",
      ".github/workflows/forge-check.yml (grep)",
      ".githooks/pre-commit, pre-merge-commit (grep)",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B -c tier_declared_ok(d, resolve_lead_binding(cfg), cfg) for opus/claude-opus-5-5/fable/sonnet", "result": "opus False, claude-opus-5-5 False, fable True, sonnet False"},
      {"command": "grep -o model claude-fable-* dev1.jsonl | sort | uniq -c", "result": "4 claude-fable-5-2"},
      {"command": "cat logs/journal/*.jsonl | grep -c -E by fable / by opus / basis queued-to-lead", "result": "663 / 278 / 73"},
      {"command": "python q.py over dev1.jsonl (queued-to-lead tasks with a second accepted)", "result": "queued tasks 71 with a second accepted 2"},
      {"command": "git grep -c delegation.config / TIER_ORDER|AGENT_TIER|QUEUED_TO_LEAD_AGENTS / Lead tier = fable|Lead(top)|critic-tier -- tools/", "result": "29 in 12 files / 35 in 4 / 13 in 3"},
      {"command": "git rev-parse HEAD origin/main", "result": "0d6f61b1 both"}
    ]
  },
  "fixes": [
    "B1: state in s7 that A-F and L are committed by a Fable session, or move the config flip first (L0) and state the transitional validator behaviour",
    "B2: function_of_session derives from rank_of_model; add the s5.4 case 'family bound, id differs' with a fable-5-2 test row",
    "B3: put F9 (validator shape and journal_write calibrated option) and test_journal_write.py into stream B; add the CLAUDE.md SHAPES escalated/calibrated rows to L; decide the checklist step-4 reader",
    "B4: add a code refusal of accept/reject journal writes from a subagent payload, and a registered detector for critic/designer acceptances without an agent:<id> delegated",
    "M1-M10 as listed in the report (escalation above Opus, weekly trigger, FG7-54 duplicate, F18 to (b), F2 option (c) and lazy yaml, one bad-config behaviour, FAMILY_ORDER, escalated model meaning, queued-to-lead clearing, order line against boot-by-topic)"
  ]
}
```
