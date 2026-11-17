# Rules-debt fix — draft spec (t-924, F19)

Designer draft for the Lead. Owner's word 17.11.2026, verbatim: «давай починим сейчас, правила это важно».
Subject: `ai-packages/qa-factory/design/factory-rules-debt.md` (the debt file). Decisions are the Lead's;
forks are in §6. Owns paths are written against the main checkout `C:/QAFactory/forge-repo/`; in a worktree
dispatch the Lead substitutes the worktree root (same relative path).

Freshness: local `refs/heads/main` = `refs/remotes/origin/main` = `e246a9cb` (read from `.git/refs`), so the
root checkout was read, not `.claude/worktrees/read-main` (that worktree does not exist today; Glob, positive
control: the same Glob shape found 60+ other worktrees' copies of the debt file).

## §0. Row ids used here

The scout's ids (t-921), mapped to the debt file as it stands on `e246a9cb`:

- R1-R11: table "Measured in run 5, still open", lines 21-31 in file order (FR-11, FR-16/17, FR-21, FR-22,
  FR-23, FR-23+FR-5, FR-31, FR-36, FR-37, FR-41, FR-43).
- W1-W3: "Found by this walk", lines 35-72 (FR-13 candidate_evidence, FR-1/FR-2 command blocks, FR-41 witness).
- X1-X18: table "Open under the rules added on 29.09", lines 82-99 in file order.
- G1-G16: table "Open under FR-59", lines 112-127 (G1-G13 the thirteen gates in file order, G14 ANCHOR_FLOOR,
  G15 reader heads, G16 shell substitution).
- N1: FR-42 row, line 135. P1: FR-7 row, line 141.

Open rows of the file: **50** (11 + 3 + 18 + 16 + 1 + 1). The header's "Twenty-five rows are open today" (line
5) is stale. Closed sections: 18 entries "Fixed since this walk", 6 "Checked and clean" (not re-walked).

## §1. Architecture, rules, owners (package spec duty, designer rule 1)

FR sections touched across the streams: A (FR-2 door of a refusal: W3, X10), B (FR-6/FR-7 text to a person:
R9, X10), C (FR-13 closed variety: W1, X9, G15; FR-38: W3), D (FR-59: G4, G1-G13), E (FR-37 path named = path
written: R9), F (FR-41 unknown never a fact: G4, W3), G (FR-31: R7; FR-47: X16; FR-30 English: every stream).
Per stream below: the sections it touches and the AR-n with the change check written into its DoD.

AR-n touched (change check from `design/architecture.md`, quoted in each stream's DoD where it applies):
AR-1 (closed variety is a data row: W1, X9, G15), AR-13 (a fact with a reader is read only through it: W1,
X9), AR-18 (one detector output shape, one reader `detector_verdict`: W3), AR-20 (shrink-only ratchets:
X16, N1), AR-28 (unknown never a pass: G4, W3, G1-G13), AR-29 (code judges data; role judgment by a tier
above: X16, W3), AR-9 (refusal names a door: X10), AR-24 (a person's words reach what acts on them: X10),
AR-37/FR-37 path agreement is FR, not AR (R9: AR-13 only for the path fact).

Checks added or altered, with owner and census class (AR-29):

| check | stream | owner | census class | blocking |
|---|---|---|---|---|
| `candidate_evidence.assess_candidate` level-set membership (now read from `contract.PLAN_LEVELS`) | S3 | data | shape (unchanged class) | refuses a candidate (structural `valid: False`), as today |
| `run_suite.verify_node_ids` collect-error note wording | S5 | data | none (a note, never a stop) | no |
| `validate_artifacts.check_behaviour_claims` re-class | S6 | data | `meaning-proxy` -> `xref` (presence of a claim per computed R, closed `origin`/`differs`/`before_ref` forms, joins to `requirements-readiness.json`; no wording judged: read in `contract.claim_row_errors`, contract.py:1467-1512) | yes, as today |
| `check_witness.main` "no rule" outcome | S7 (after F-L3) | data (presence of a contract) | shape | no (advice, never a block) |
| `project_decisions` scope membership read from data | S8 | data | shape (unchanged) | refuses an unknown scope, as today |
| window gate reading a person's word for a `review` gap | S9 (after plan critic) | intent (the person's word, P13) | xref | lifts a block |
| read-head / reader-command membership from data | S10 (after F-L6) | data | safety | refuses, as today |

Commit-line templates: every package commit carries the `architecture:` and `judgment:` lines in the form
`tools/architecture_gate.py` accepts (the only carrier of that grammar; it is not copied here).
`judgment: none` is never written bare: it always carries ` -- <why>`. S6 lowers the census ceilings
(`meaning-proxy`, and `breach` if the row is the one counted there), so no raise form is owed; S2, S4, S5
change no check's judgment and write `judgment: none -- <why>`.

## §2. Verdict for every open row (50 of 50)

Verdict words: CLOSE (close by text, evidence named) / FIX <stream> / FORK-O (owner) / FORK-L (Lead) /
LIMIT (real limit, stays with its reason) / REF (an existing pile node covers it, referenced not duplicated).

| row | rule | verdict | evidence / note |
|---|---|---|---|
| R1 | FR-11 | FORK-O F-O2 | code part done (`probe_by_code.py` refuses a suffix with no `assertion_probes` row with its door `red_sandbox.py --probe`; detectors.json:85 holds csharp…, :325 python AST). Live proof already queued: `plans/piles/live-runs/findings/B-373-pereotkryto-06-10-2026-d-0025.md` |
| R2 | FR-16/17 | FORK-L F-L1 | direction not chosen by the entry |
| R3 | FR-21 | FORK-L F-L2 (+ text in S1) | the row's "G2-2 is grounding batch 2" is stale: G2-2 and G2-3 are `принято, слито (релиз 0.10.8)` (`plans/piles/grounding/batch-2-grounding-measure.md:112-113`); `skipped` -> `planned_skip` (`references/delivery-verdict-kinds.json:21,95`) is still open |
| R4 | FR-22 | FORK-L F-L4 | controller schema (S7 rework with no case) - plan critic; live proof -> live-runs |
| R5 | FR-23 | CLOSE | `driver_stage_s8s9.py:370-379` null outcome `nothing_outward`, first in `delivery()` |
| R6 | FR-23, FR-5 | stays open; FORK-L F-L12 for the Check-line amendment | pending rows each at a named node, held by `test_null_outcomes.py` (keep, gate_named). Count not recomputed here (estimate, not verified): S1 prints it from the test |
| R7 | FR-31 | FIX S2 | `scripts/tests/test_stand_lease.py:320` asserts `waited_s == 15` |
| R8 | FR-36 | CLOSE | all three sites gate before the probe: S0 `driver_s0.py:2367-2369` (`--no-trace` to `readiness.py`, which closes at `readiness.py:958-960`), gate B `gate_preflight.py:5817-5821`, packet text `gate_brief.py:4968-4977` ("closed for this run") |
| R9 | FR-37 | FIX S4 (+ FORK-O F-O6) | `driver_stage_s8s9.py:278` "proposal under qa-factory/bugs" vs the charter `agents/qa-bug-reporter.md:57` `<task root>/bugs/` (OH5-9) |
| R10 | FR-41 | LIMIT | the row itself names the real limit (no evidence of liveness -> `unknown`, only a person settles it); S1 moves it to a new "Real limits" section |
| R11 | FR-43 | CLOSE | `story_run.py:105` `console_io.utf8_stdio(line_buffering=True)` |
| W1 | FR-13 | FIX S3 | `candidate_evidence.py:7` own copy; owner of the automated levels in code is `contract.PLAN_LEVELS` (contract.py:2175) |
| W2 | FR-1, FR-2 | FORK-O F-O5 (+ count in S1) | `command` routes are **221** today (`design/controller-blocks.md:21`), not 109; `test_controller_blocks.py` holds the route map only (ROUTES, :31), no door is executed |
| W3 | FR-41 | FORK-L F-L3, then S7 | `check_witness.py:301-305` prints `OK (no rule …)` exit 0; registry row `witness_backstop` (gate-registry.json:361-374) says "`no rule` must read not checked, never OK" |
| X1 | FR-47 | FORK-L F-L8 | no editor script for `context-manifest.json`, `requirements-register.md`, `understanding.md`, `test-report.md` (Glob `scripts/*{manifest,register,understanding,report_row,row}*.py`; positive control in the same call: `plan_row.py`, the editor of the plan, found; `manifest_view.py` is read-only, :17-18) |
| X2 | FR-13 | CLOSE stale parts; residue FORK-L F-L9 | case id is data (B-013); `manifest_from_tests.py:347-352,1629` reads every language through `assertion_probes` (a language with no row is a note with a door); `cost_capture.py` holds no `testproject1` regex (the same Grep found only a comment at :568). Residue: `s5_precheck.py:1661` names a pytest marker as the door for any test file |
| X3 | FR-48 | infra half CLOSE; prompt half FORK-O F-O4 | `driver_runner.py:845` is the one recogniser of an infrastructure failure (B-012); `driver_runner.py:606-607` still `--append-system-prompt-file` for `references/conductor.md` (`driver_conductor.py:337`, `driver_stage_s8s9.py:451`) |
| X4 | FR-50 | FORK-L F-L10 (cannot tell) | MR-route provenance not verified by this draft; `source_inventory.py:369-420,767` carries `auth_lost` for sources, the MR route was not read |
| X5 | FR-53 | CLOSE | `driver_stage_s8s9.py:342-379` (`outward_rule` reads `external_writes`, null state) |
| X6 | FR-54 | CLOSE | `factory-rules.md:498-503`: FR-54 now names `docs/SIBLING_MAP.md` axis 5 and AR-19 (F6-29) |
| X7 | FR-56 | FORK-L F-L7 | the missing direction is checked (A2 write verbs, A23 run verbs: `role_permissions.py:1-25`; A2b excess write right); the excess direction (a granted tool no phase names) is not |
| X8 | FR-57 | CLOSE | `guard_pre_tool.py:1302-1312` door (continue / `artifact_supersede.py`) for a role with Bash; Edit door for a role without |
| X9 | FR-13 | FIX S8 on recommendation (+ FORK-O F-O3) | `project_decisions.py:43-50`; template `references/templates/factory-backlog.md:9-16` copies the meanings; dashboard `factory_dashboard.py:31,3644,3648,3679-3681` spells words |
| X10 | FR-57 | FIX S9 after the plan critic (F-L13) | `window_record.py:1741` `WORD_READ_KINDS = ("quality", PROBE_GAP_KIND)`; `:1766` "recorded, not read by this window"; the word reader is `controller.py` (`_s5_word_index` :7425, `_s5_gap_problems` :7444) |
| X11 | FR-6 | halt/resume CLOSE; rest FORK-L F-L10; REF GW1-4 | `driver_dialog.py:61-89` halt text: plain words, the message to the details file; S0 texts and the `run`/guarded-step stops not verified; `plans/piles/words-gates/batch-1-slova-i-gejty.md:30` GW1-4 (B-292 texts, ожидает) |
| X12 | FR-47 | CLOSE | the row says "Closed by X7-2" |
| X13 | FR-47 | CLOSE | "Closed by X2-3" |
| X14 | FR-47 | CLOSE | "Closed by X7-2" |
| X15 | FR-47 | CLOSE | "Closed by X7-2" |
| X16 | FR-47 | FIX S6 | `check_behaviour_claims` still blocking (validate_artifacts.py:656,690; exit_gate.py:1338), census row `judgment-census.json:1187` class `meaning-proxy`; its body checks presence/forms/joins only (see §1) |
| X17 | FR-47 | CLOSE | "Closed by X7-5" |
| X18 | FR-47 | CLOSE | "Closed by X7-5" |
| G1 | FR-59 | FORK-O F-O1 | `stand_identity` debt B-257; declared branch `question`/`wait`/`stage_entry` (gate-registry.json:28,35) |
| G2 | FR-59 | FORK-O F-O1 | `provenance_acceptance` B-255; `question` (:87,91) |
| G3 | FR-59 | FORK-O F-O1 | `test_identity` B-217; `rerun` (:144,148) |
| G4 | FR-59 | FIX S5 (note) + FORK-O F-O1 (branch) | `run_suite.py:1850` "collect failed: …" lacks "not verified"; registry `unknown_branch: debt` (:166,170) |
| G5 | FR-59 | FORK-O F-O1 | `live_check_demand` B-279; `debt` (:204,208) |
| G6 | FR-59 | FORK-O F-O1 | `s5_coverage` B-221; `question`/`window_acceptance` (:225,229) |
| G7 | FR-59 | FORK-O F-O1 | `s5_window` B-179; `question` (:247,251) |
| G8 | FR-59 | FORK-O F-O1 | `delivery` B-061; `debt` (:270,274) |
| G9 | FR-59 | FORK-O F-O1 | `case_preconditions` B-280; `question`/`gate_a` (:310,314) |
| G10 | FR-59 | FORK-O F-O1 | `environment_preparation` B-255; `question`/`authorization` (:332,336) |
| G11 | FR-59 | FORK-O F-O1 | `baseline_identity` B-281; `refuse_with_door` (:354,358) |
| G12 | FR-59 | FORK-O F-O1 | `s5_stand_limits` B-282; `debt` (:497,501) |
| G13 | FR-59 | FORK-O F-O1 | `reporter_rehearsal_identity` B-283; `rerun` (:520,524) |
| G14 | FR-13 | FORK-L F-L5 | `gate_registry.py:33-35` the floor is deliberate (a data edit must not blind the scan) |
| G15 | FR-13 | FORK-L F-L6, then S10 | `host_adapter.py:452` `_READ_HEAD`; `stage_guard.py:2509-2512` `READER_COMMANDS` (HOT) |
| G16 | FR-59 | LIMIT | the AR-28 exception decided in `docs/tasks/specs/r0107-s4a-cx2-27-oh3-22-32.md` E7 (row's own text); stays, S1 moves it to "Real limits" |
| N1 | FR-42 | text in S1; FORK-L F-L11 | the baseline is **55** sites, not 105 (`audit_factory.py:1716` `NO_MOVE_BASELINE_MAX = 55`); the named converting nodes (conductor/1, conductor/2) are closed; no open node converts the 55 |
| P1 | FR-7 | REF | `plans/piles/words-gates/batch-1-slova-i-gejty.md:35` GW1-36 (designer -> plan critic -> builder -> critic; ожидает) is exactly this fix |

Count check: CLOSE (whole) 12 = R5 R8 R11 X5 X6 X8 X12 X13 X14 X15 X17 X18; FIX 8 = R7 W1 R9 X16 X9 X10 G4 G15
(the last three gated); FORK-O primary 17 = R1 W2 X3 G1-G3 G5-G13 (G4 counted under FIX); FORK-L primary
10 = R2 R3 R4 W3 X1 X2 X4 X7 X11 G14 N1 R6 minus double counts — per row the table above is the authority:
every one of the 50 rows has exactly one primary verdict in the third column.

Not in the file, found by the scout and confirmed: registry row `environment_property_cover`
(gate-registry.json:527-548, `status: debt`, `debt_ref: B-283`, branch `question`/`wait`/`gate_a`) — the 14th
`debt` row; the file lists 13. S1 adds it to the FR-59 table (it joins F-O1).

## §3. Streams

Hot files (PROJECT.md «Командная работа» п. 3): `story_run.py`, `hooklib.py`, `stage_guard.py`,
`gate_preflight.py`, `install_smoke.py`, `controller.py`. No stream of phase 1 touches one.

Pile overlaps found (case-insensitive Grep of `plans/piles/**/batch-*.md`, positive control: the same call
found `controller-blocks` and `NO_MOVE_BASELINE` rows): `thinking-roles/batch-6` TR4-17 owns `check_witness.py`
(S7), TR4-16 owns `project_decisions.py`, `gate_preflight.py` (S8, FR-59 nodes), TR6-3 owns `host_adapter.py`
(S10); `onboarding-forge/batch-2` SC2-26 owns `check_witness.py`, `factory_dashboard.py` (S7, S8);
`words-gates/batch-1` GW1-36 owns `run_suite.py` (`blocked_by_env` row) and `gate_preflight.py` (S5 is
function-disjoint: `verify_node_ids` only, D-0048 form). All those batches read `статус: ожидает` (not taken)
in their headers. Queue lines are in each stream's `siblings:`/`edges:`.

### S1 — the debt file itself (two passes, one owner)

S1a runs now; S1b runs after S2-S6 (and later S7-S10) are accepted, so the debt file has one writer at a time.

```
given: C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md (whole), C:/QAFactory/forge-repo/plans/builder-rules.md, C:/QAFactory/forge-repo/docs/TESTING.md, C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-fix-spec.md (§0, §2 - the verdict table is the input)
```
given: the four files above; this spec §0 and §2 (the per-row verdict and evidence column is the edit list)
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules-debt.md
non-goals: any code; any row's meaning beyond the verdict table; `factory-rules.md` (unless the Lead accepts F-L12, then S1b also owns C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md, Check lines of FR-5 and FR-23 only)
handoff: report under C:/QAFactory/forge-repo/docs/tasks/handoffs/ (path given by the Lead)
edges: see the list below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/design/factory-rules-debt.md` plus `python -B ai-packages/qa-factory/scripts/tests/test_null_outcomes.py` and `python -B ai-packages/qa-factory/scripts/tests/test_s1_s2_contract.py` (the two package readers), and `python -m pytest tools/test_piles_close_id.py -q`
siblings: none -- one file; its readers are listed under "Readers" below

Items (S1a):
1. Header (lines 3-7): the open count made true and computed from the tables after the edit (state each
   table's count in the sentence, as now). Expected: the sentence's numbers equal the rows under the open
   headings. Test: none (doc; TESTING.md "тест документа рабочего процесса" is not written).
2. Move to "Fixed since this walk", one bullet each with the evidence of §2: R5, R8, R11, X5, X6, X8, X12, X13,
   X14, X15, X17, X18; X2's stale parts and X3's infra half and X11's halt/resume half are narrowed IN their
   rows (the row keeps only the residue, with the §2 evidence).
3. A new section "Real limits, kept with their reason" holding R10 and G16 (their text whole, plus one line
   "why this is not fixable here").
4. Stale numbers: W2 "109" -> the count `design/controller-blocks.md` states for `command` (221 on
   `e246a9cb`; re-read line 21 before writing); N1 "105 sites" -> the value of `NO_MOVE_BASELINE_MAX`
   (`audit_factory.py:1716`, 55 on `e246a9cb`); R3's "is grounding batch 2 (G2-2)" -> "landed in G2-2 (0.10.8);
   what is left: …" (the `skipped` sentence stays).
5. FR-59 section: line 104 "Thirteen gates" -> fourteen; add the row for `environment_property_cover` (debt
   B-283, branch `question` at gate A) in the table's form; each G1-G13 row's "no unknown branch yet" is
   replaced by the branch the registry declares (§2 column) and "conversion owed (T2, `gate_template.acceptable`)".
6. P1 row: one line "node: words-gates/1 GW1-36". X11 row: "texts: words-gates/1 GW1-4".
Items (S1b, after each fix stream is accepted): move R7, W1, R9 (driver half), X16, G4 (note half), and later
the S7-S10 rows, to "Fixed", each "closed by code; proven by a live run (FR-33)" where §7 lists it for
live-runs; R6 Check-line amendment only on F-L12.

Edges (S1):
- E1 (reader K0.15, `test_null_outcomes.py:589-595`): exactly ONE table row containing both `FR-23` and `FR-5`
  must remain, and it must keep the four needles `references/null-outcomes.json`, `` `pending[]` ``, `t-305`,
  `B-253`. INVARIANT: the null-outcome walk keeps its single debt carrier; a row edit that drops a needle is
  refused by the test.
- E2 (reader G1-10, `test_s1_s2_contract.py:319-325`): exactly ONE line starting `| FR-21 |`, and its
  statements about the kinds file must still match `fr21_row_mismatch` (do not reword what it says
  `pending_implementation`/`impossible` map to). INVARIANT: the debt row cannot drift from
  `delivery-verdict-kinds.json`.
- E3 (reader `tools/piles.py` `DEBT_REL`, :2381): debt entries that name a `B-nnn` are what `piles.py close --id`
  warns about; a row moved to "Fixed" keeps its B-id inside the bullet (the warning then points at a fixed
  bullet - acceptable), and no B-id is invented. INVARIANT: a B-id closed in the backlog is still findable here.
- E4 (empty): a table left with no open row keeps its heading and gets the line "Nothing open." (FR-23 shape),
  never a deleted heading.
- E5 (conflict: "entries are removed when the fix lands" (line 10) vs "what left the list … is at the end,
  not deleted" (line 7)): moved, never deleted - line 7 decides.
- E6 TEMPORAL: rows of S2-S10 are moved only in S1b, after their stream is accepted; before that they stay open.
- FR-30: the file is in the package - English, no Cyrillic (`selftest.py --lang` judges at the canon).

### S2 — R7, the load-sensitive lease test (FR-31)

given: factory-rules.md (whole), builder-rules.md, TESTING.md; `scripts/stand_lease.py` (read)
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_stand_lease.py
non-goals: `stand_lease.py`; any other assertion of the file
handoff: report path given by the Lead
edges: E1-E3 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/test_stand_lease.py` and `python -B ai-packages/qa-factory/scripts/tests/test_stand_lease.py` (keep row, layer `detector`)
siblings: `test_stand_lease.py:386` (`(clock.sleeps, busy.waited_s) == ([5, 2], 7)`) — the same shape; verdict per neighbour is owed in the report (applied / not applicable: the holder there is not a killed process, so no extra poll can occur - builder confirms by reading)

Item: the takeover check (:317-323) asserts `waited_s` by bound, not equality: `15 <= waited_s <= 1800`
(the holder was killed inside the third poll; one or more extra polls under load are legitimate) AND
`waited_s % 5 == 0` (poll_s=5), with `queued_behind == "child-job"` and `took_over.job_id == "child-job"`
unchanged. Test row: the same check, rewritten in place (no new test). FR: G (FR-31). AR: none --
`architecture: none -- <why>`; `judgment: none -- a test assertion bound, no check of the package moves`.
- E1 (limit): the upper bound is the call's own `wait_s=1800`; a value above it means the wait ignored its
  limit - the check must stay red for that. INVARIANT: a lease that waits past its limit is never green.
- E2: a takeover with `took_over` absent stays red (unchanged). INVARIANT: a takeover is always said.
- E3: wall time is never asserted (TESTING.md "Пин измеренной константы"); the FakeClock's value is a count of
  polls, which is why the bound and the modulo are legitimate.

### S3 — W1, the second copy of the level set (FR-13)

given: factory-rules.md (whole), builder-rules.md, TESTING.md; `scripts/contract.py` (`PLAN_LEVELS` :2175,
`TRACE_LEVELS` :594), `references/vocabularies.md` (Level, :89)
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/candidate_evidence.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/profile_contract.py
non-goals: the vocabulary itself; `TRACE_LEVELS`; any reader of `assess_candidate`'s output
handoff: report path given by the Lead
edges: E1-E4 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/candidate_evidence.py ai-packages/qa-factory/scripts/profile_contract.py` plus `python -B ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (profile_contract.py `<module>` is a registered `vocabulary` site, gate-registry.json:64). `test_candidate_evidence.py` is QUARANTINED (test-layers.json:7412): not run, not edited
siblings: `profile_contract.py:25` `LEVELS = {"unit","component","api","integration","e2e-ui"}` — the third copy of the same five words (found by this draft; included as item 2, rule 9 sweep); `gate_preflight.py:153` `E2E_LEVEL` (one word, HOT file: not applicable - a single level name read for a branch, not a set copy; queued nowhere)

Items:
1. `candidate_evidence.EXECUTION_BOUNDARIES` = `set(contract.PLAN_LEVELS) | {"unknown"}`; a comment says
   `unknown` is the declared "not stated" outcome (AR-23) and that manual levels do not apply to an existing
   test FILE candidate (a manual level has no test file). Behaviour: identical for every input today (the same
   six words) — no new test (TESTING.md "«Как раньше»" is not written); the witness is the scenario walk.
2. `profile_contract.LEVELS` = `frozenset(contract.PLAN_LEVELS)` (or a set; membership use only, :186-209).
FR: C (FR-13). AR-1, AR-13 — change check (AR-13): "grep SIBLING_MAP for the file or fact; if an axis names a
survivor, call it; grep the package for the same shape with a positive control" — the builder greps
`"e2e-ui"` over `scripts/*.py` (this draft's hits: candidate_evidence.py:7, contract.py:594/2175,
profile_contract.py:25, plus single-word uses) and reports each. `judgment: none -- the same set, read from its one owner`.
- E1 (import): if `import contract` in either module creates an import cycle (profile_contract is imported
  early by gate code), the builder does NOT work around it with a local copy: it stops and reports the cycle
  (a question). INVARIANT: no third copy is born to dodge a cycle.
- E2 (absent field): `execution_boundary` absent -> `"unknown"` as today (a gap, `valid: True`).
- E3 (outside input): a candidate comes from the scout's artifact (a role's output, not outside input): no
  adversarial battery (TESTING.md: internal boundary).
- E4: `manual-agent`/`manual-human` as a boundary stay refused ("invalid"), as today. INVARIANT: a manual
  level never makes a test-file candidate `sufficient`.

### S4 — R9, the bug path the S8 prompt names (FR-37)

given: factory-rules.md (whole), builder-rules.md, TESTING.md; `agents/qa-bug-reporter.md:57`,
`scripts/brief_pack.py:298`, `changelog.d/oh5-9-publish-path.md`
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_stage_s8s9.py (`Driver.run_bug_reporter` only)
non-goals: `references/common-rules.md` and its slices (F-O6), `bug_records.py`, `artifact_producer.py`, any other function
handoff: report path given by the Lead
edges: E1-E2 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/driver_stage_s8s9.py` plus `python -B ai-packages/qa-factory/scripts/tests/test_driver_layers.py` (driver layer file, builder-rules 7c). `test_story_run_delivery*.py` are quarantined/slow: judged by the batch canon, named in the report
siblings: `references/common-rules.md:116` and the 11 `references/slices/*/common-rules.md` copies (F-O6, not touched); `bug_records.py:10` docstring (F-O6); `factory_dashboard.py:1225,1266` (reads both homes - correct, not touched)

Item: the sentence at :276-280 names `<task root>/bugs/` (the charter's and `brief_pack`'s spelling) in place
of "qa-factory/bugs"; nothing else in the prompt changes. Test: the scenario walk's S8 rows, if any print the
reporter's dispatch; otherwise "no scenario or keep row covers" is a report line (no new test: the prompt is
a role text, guarded by the role-rules registry, TESTING.md). FR: E (FR-37), B. AR-13 (the path is read from
the charter's one spelling). `judgment: none -- prompt wording, no check moves`. Role behaviour: closed by code,
not proven (§7).
- E1: the experiment line (`self.no_trace()`, :272-273) is unchanged. INVARIANT: an experiment still forbids a
  tracker proposal.
- E2 (conflict R9 vs F-O6): if the owner answers F-O6 "the project's `qa-factory/bugs/` is the home", S4 is
  reverted together with the charter (OH5-9) — one road; S4 never makes the prompt disagree with the charter.

### S5 — G4 residue, the collect-error note (FR-59, FR-41)

given: factory-rules.md (whole), builder-rules.md, TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/run_suite.py (`verify_node_ids` only)
non-goals: the registry row's `unknown_branch` (F-O1); `blocked_by_env` code (GW1-36); any exit code
handoff: report path given by the Lead
edges: E1-E3 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/run_suite.py` plus `python -B ai-packages/qa-factory/scripts/tests/test_node_ids.py` (keep, `gate_named` for `collected_ids`) and `python -B ai-packages/qa-factory/scripts/tests/test_console_encoding.py` (a printing script changed, builder-rules 7b). `test_run_suite_*.py` are quarantined: canon
siblings: the other notes of the same function all start "node ids were not verified" (:1674, :1743, :1753, :1840) — the item makes :1850 the fifth of the same form

Item: :1850 note becomes `"node ids were not verified: collect failed: " + <the error, cut as today>`.
Behaviour: a pytest collect error is reported as "not verified", never as a fact about the ids; the run still
goes on. Test row: one row in `test_node_ids.py`'s existing table (a collect error -> the note starts "node ids
were not verified"), red before the change. FR: D (FR-59), F (FR-41). AR-28 - change check: "the spec states
each new gate read's behaviour on missing, unreadable and empty input, and a test pins it" (E1-E2 below).
`judgment: none -- a note's words, the run's decision is unchanged`.
- E1 (limit): the existing `[:400]` cut stays; text at and beyond 400 characters is cut as today (the note
  carries the head, the full error is not lost: it is in the collect's own output) — one table row AT 400 and
  one beyond (the collect error is outside input: the framework's output).
- E2 (empty): `collect_error` empty/absent -> no note (unchanged).
- E3 (conflict with GW1-36, which owns the same file): function lists are disjoint (`verify_node_ids` vs the
  `blocked_by_env` row); the later merge resolves; queue line `очередь: S5 → GW1-36` if both run the same week.

### S6 — X16, the census class of `check_behaviour_claims` (FR-47, AR-29)

given: factory-rules.md (whole), builder-rules.md, TESTING.md; `design/architecture.md` AR-29;
`scripts/contract.py:1457-1512` (read)
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
non-goals: `validate_artifacts.py` (no code change); `told-ratchet.json` unless the census test demands it (then a question)
handoff: report path given by the Lead
edges: E1-E3 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json` plus `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` (keep, `register`)
siblings: `references/stage-joints.json:4225-4239` (names the check, not its class: unchanged); `scripts/tests/fixtures/told-ratchet.json:655` (an entry keyed by the function: unchanged unless the census test reads it)

Item: row :1187 -> `"class": "xref", "owner": "data"`, with a `note` naming why (presence of a claim per
computed R; closed forms; joins to the readiness file; no wording judged, contract.py:1467-1512); the
`ratchet` block (:4) lowered to the new totals (`meaning-proxy` 8 -> 7; `breach` 1 -> 0 only if this row is the
one `breach` counts - the builder reads `test_judgment_census.py` to confirm and reports which). FR: G (FR-47).
AR-29 — change check: "for every check the change adds or alters, name its class" (named above); AR-20 —
"list every row added or raised (key, old -> new, reason)": lowered only, listed in the report.
- E1: if the census test COMPUTES the class from code (not from the row), and its computation says
  `meaning-proxy`, the builder stops and returns it as a question (the class is then a code fact, and the
  re-class is wrong or the classifier is). INVARIANT: the census never says something the classifier refutes.
- E2: lowering is shrink-only legal (AR-20); a raise anywhere is refused by `tools/architecture_gate.py`.
- E3: the acceptor of the class judgment is a tier above (critic), per AR-29.

### S7 — W3, "no rule" is not "OK" (after F-L3; queue after TR4-17/SC2-26 if they are taken)

given: factory-rules.md (whole), builder-rules.md, TESTING.md; `scripts/detector_verdict.py:1-50` (the contract)
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/check_witness.py (`main`)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/exit_gate.py (`witness_errors`)
non-goals: new RULES (option (a) of F-L3); `detector_verdict.py`'s contract
handoff: report path given by the Lead
edges: E1-E4 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/check_witness.py ai-packages/qa-factory/scripts/exit_gate.py` plus `python -B ai-packages/qa-factory/scripts/tests/test_check_witness.py` (keep, scenario) and `python -B ai-packages/qa-factory/scripts/tests/test_gate_registry.py`; `test_exit_gate*` judged by the canon
siblings: `check_delivery.py:716-724` (runs check_witness on the manifest, which HAS a rule: unchanged); `artifact_producer.py:79` (imports RULES: unchanged); registry row `witness_backstop` (`exempt_reason` text updated to "prints not checked" in the same commit — then gate-registry.json joins owns)

Item (recommended option (b') of F-L3): for a name with no rule, `check_witness.main` exits 0 and prints an
`ADVICE — 1` block (form 1 (e) of `detector_verdict`): `- not checked: no evidence contract for <name>`;
`exit_gate.witness_errors` prints "witness not checked: <name> has no evidence contract" instead of "witness OK"
when the parsed verdict carries that advice, and files the advice as the gate files advice. Test row: one row in
`test_check_witness.py` (a `test-plan.md` artifact -> ADVICE "not checked", exit 0), red before the change.
FR: A, D (FR-59), F (FR-41), C (FR-38: no new requirement, so no ahead-card change). AR-18 — change check:
"consumers parse only through `detector_verdict`; a contract change updates the reader, every producer and
the test in one commit" (no contract change: the existing advice form is used); AR-28; AR-29 (shape, owner
data, non-blocking). Role-visible text -> §7.
- E1: exit code stays 0 (fail-open by design, registry `exempt_reason`); INVARIANT: "no contract" is never
  printed or recorded as "OK"/acceptance.
- E2: a malformed advice block is a `defects` entry of `parse`, never silence (contract).
- E3: `code-review.md` path unchanged.
- E4 TEMPORAL: stories in flight that already recorded "witness OK" for a no-rule artifact are not rewritten.

### S8 — X9, the finding scopes as one data file (FR-13; on recommendation of F-O3)

given: factory-rules.md (whole), builder-rules.md, TESTING.md
owns: C:/QAFactory/forge-repo/ai-packages/qa-factory/references/finding-scopes.json (new)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/project_decisions.py (`FINDING_SCOPES`, `scope_refusal`)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/factory_dashboard.py (`SCOPE_COLOR` reads, legend, `scope_span`, the render count)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/templates/factory-backlog.md
non-goals: `SKILL.md` (integrator-only, builder-rules 1), the command doors that spell the words (`conductor-actions.json`, `ticket_adapter.py:2947`, phases, `qa-retro-analyst.md`) - they name words, not meanings: unchanged; project-added addressees (F-O3)
handoff: report path given by the Lead
edges: E1-E5 below
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for <the four owns>` plus `python -B ai-packages/qa-factory/scripts/tests/test_conductor_doors.py` (keep, reads `PD.FINDING_SCOPES`) and `python -B ai-packages/qa-factory/scripts/tests/test_project_decisions_change_request.py` (keep); `python -m pytest tools/test_collect_intake.py -q` (forge reader, see Readers)
siblings: axis of "one artifact one writer"/AR-13 — the dashboard reads the writer's list today (`factory_dashboard.py:27`); the template is the second carrier of meanings

Items:
1. `references/finding-scopes.json`: `{word: {"meaning": ..., "urgent": bool}}` for the three words
   (meanings verbatim from `project_decisions.py:44-49`).
2. `project_decisions.FINDING_SCOPES` is built from it through the package's JSON loader
   (`hooklib.load_ref_json` or the module's existing reader); same dict shape for every importer.
3. Dashboard: the legend and `scope_span` read the words from `FINDING_SCOPES`; the "urgent" styling and the
   render-findings count key on the row's `urgent` capability, never on the literal `local-urgent` (AR-1);
   colours stay presentation in code with the grey fallback (:30).
4. Template: the meanings list keeps its prose (a human reads it) and one data-join row (layer 2) checks that
   the template's three `- \`word\` — meaning` lines equal the data file — the join row goes into an existing
   keep test that already reads the template or `FINDING_SCOPES` (`test_conductor_doors.py`); no new file.
FR: C (FR-13), A (FR-1: refusal unchanged). AR-1 - change check "grep `scripts/` for the shape of the problem
(a tuple of words), not for the helper"; AR-13; AR-3 (default for every key: E1). `judgment: none -- the same
words, read from data`.
- E1 (absent/unreadable data file): the loader's failure is a refusal of the CLI with its door (FR-59: never a
  silent empty list); it is NOT a fallback copy in code (that would be the copy this row removes).
  INVARIANT: an unknown scope is never accepted, and the list is never empty.
- E2 (conflict with E1 and `tools/collect_intake.py` importing `project_decisions` at module level): loading
  must not raise at import (the forge tool imports it for `parse_findings`); load lazily or at first use.
- E3 (limit): `SCOPE_SHOWN = 60` cut of a refused word unchanged; outside input (`--scope` from a CLI) keeps
  its existing cases; one row AT 60 and one beyond, if the existing table lacks them.
- E4 TEMPORAL: the data file does not exist before S8; after S8 the module requires it. Projects' existing
  `factory-backlog.md` copies are not rewritten (builder-rules 9).
- E5: a new `references/*.json` may need a home row (`selftest.py --homes`, FR-44) — if the narrow witness or
  the canon names it, the builder adds the row the refusal names.

### S9 — X10, the person's word on a `review` gap (FR-57) — after the plan critic (F-L13)

Changes a meaning (a person's word lifts a gap no word lifts today): PROJECT.md «Как принимается изменение
пакета» п. 6 — (а) measure the premise first on a real story artifact (one `window_record.py` run on a
fixture story with a `review` gap and a recorded word: the "recorded, not read" line must appear), (б) critic
on the plan before the builder, (в) the reused reader `waiver.split_overridden` moves from advice
(`_unread_words`, reporting only) into a gate role: its error direction must be "does not match" — a word
that names a different gap, a revoked word, a word for another stage, `*` used where the block names the
review gap of a DIFFERENT instance must all stay unread; (г) an owner idea? No — the direction is the debt
row's own (Q7 A); the Lead confirms.
owns (for the plan): C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/window_record.py (`WORD_READ_KINDS`, `verdict`)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py (`_s5_word_index`, `_s5_gap_problems`) — HOT: one stream on it at a time
Test: `test_probe_gap_word.py` (keep, detector) and `test_window_record.py` (keep, gate_named) — a row each: a
recorded word for a `review` gap passes and the pass is recorded; the adversarial rows above stay blocked.
AR-9, AR-24, AR-25 (`design/state-exits.md` row for the pass), AR-28. Design detail is the plan's (Lead or
designer), not drafted here.

### S10 — G15, reader heads as data (after F-L6) — `stage_guard.py` HOT; queue after TR6-3 (`host_adapter.py`)

owns (for the plan): C:/QAFactory/forge-repo/ai-packages/qa-factory/references/launch-causes.json (a `read_heads` / `reader_commands` table)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/host_adapter.py (`_READ_HEAD`, `_read_refusal` text)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/stage_guard.py (`READER_COMMANDS`, `_is_reader`)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/role_replay.py (derives `_READ_ALTS` from `_READ_HEAD.pattern`, :30-34 — must follow)
Reused function in a more consequential role: `hooklib.reader_runs` keeps judging launches; the new table only
lists heads. Error direction: toward refusal. Adversarial inputs that must stay refused: a head named in the
table that is also a launcher (`python`, `bash`, `pwsh`, `node`), a head with a path (`/usr/bin/rg`), `.exe`
and case variants, an empty/unreadable table (falls back to the built-in floor = today's list, never to "any
head"), a table row that widens `READER_COMMANDS` with a writer (`cp`/`mv` are already there: they are
"mention" heads for the runner guard only, not read heads — the two lists must stay separate).
Test: `test_guard_*`/`test_hooks_wiring.py` rows as witness-for prints; canon for the slow ones.

### FR-59 conversion nodes (after F-O1) — one node per gate, owns = the registry row's sites, test = its `test`

| node | gate | owns (sites, gate-registry.json) | test |
|---|---|---|---|
| Q-G1 | stand_identity | runtime_probe.py, driver_stage_build.py (`build_outcome`), gate_preflight.py (`_derive_probe`, `named_container_said`) | test_stand_identity.py |
| Q-G2 | provenance_acceptance | execution_request.py, execution_fingerprint.py, manual_evidence.py, coverage_contract.py, environment_preparation.py (`_run_step`), probe_by_code.py, manual_capture.py, run_suite.py (`probe_runtime`), gate_preflight.py (`_observed_identity`), profile_contract.py | test_execution_request.py |
| Q-G3 | test_identity | proof_level.py, execution_request.py (`_match`, `green_over_same_bytes`) | test_proof_level.py |
| Q-G4 | collected_ids | run_suite.py (`verify_node_ids`, `ids_pytest_did_not_find`) | test_node_ids.py |
| Q-G5 | live_check_demand | proof_level.py (`proof_required`, `novelty_of`) | test_proof_level.py |
| Q-G6 | s5_coverage | s5_precheck.py (`run`) | test_s5_precheck.py |
| Q-G7 | s5_window | acceptance.py (`validate_window`), window_record.py (`verdict`) | test_window_record.py |
| Q-G8 | delivery | delivery_verdict.py (`decide`), check_delivery.py (`assess`, `ledger_reasons`) | test_check_delivery.py |
| Q-G9 | case_preconditions | gate_preflight.py (5 functions), planning_contract.py (`_unmet_preconditions`) | test_gate_preflight.py |
| Q-G10 | environment_preparation | environment_preparation.py (`plan_environment`, `_facts`) | test_environment_preparation.py |
| Q-G11 | baseline_identity | baseline_contract.py | test_baseline_contract.py |
| Q-G12 | s5_stand_limits | gate_preflight.py (`check_s5_stand_limits`) | test_gate_preflight.py |
| Q-G13 | reporter_rehearsal_identity | gate_preflight.py (`_rehearse_reporter`), driver_gates.py (`hand_to_conductor`) | test_gate_preflight.py |
| Q-G14 | environment_property_cover | gate_preflight.py (`_rehearse_reporter`, `check_case_preconditions`), stand_gaps.py (`gate_b_split`) | test_environment_record.py |

Each node: also `references/gate-registry.json` (status -> `converted`) and `test_gate_registry.py`. Queue
on `gate_preflight.py`: Q-G9 → Q-G12 → Q-G13 → Q-G14 → Q-G2 → Q-G1, and all after words-gates/1 GW1-36 and
GW1-24 if those are taken first (`очередь:` lines). Shared files: Q-G3/Q-G5 (`proof_level.py`) one after the
other; Q-G2/Q-G3 (`execution_request.py`), Q-G2/Q-G4 (`run_suite.py`), Q-G7/S9 (`window_record.py`)
likewise. These nodes are drafted per gate by the designer after the owner's answer (they are a NEW owner
decision applied: PROJECT.md п. 6 (г), a new node each), not here.

## §4. Edges common to every stream

- Outside input in these streams: only S5 (a framework's collect output) and S8 (`--scope` CLI): their limits
  get rows AT and BEYOND (named in their edges). Everything else is internal: no battery.
- Every stream writes English only in the package (FR-30).
- A stream that finds its premise false on reading (a line moved, a function renamed) returns a question,
  never re-targets itself.

## §5. Readers of every touched file

Command (Grep tool, one call over `tools/*.py`, `.githooks/*`, `.claude/settings*.json`, `.claude/hooks/**`,
`.claude/agents/**`, pattern = the touched file names): 36 hits in 12 files. Second call over the package
(`ai-packages/qa-factory`, `*.{py,json}`) for `factory-rules-debt`: 8 hits. A third call for the debt file
over `tools/.githooks/.claude/**` hit its time limit inside `.claude/worktrees/` copies (other sessions'
trees, not readers); the live readers found are listed.

| touched file | reader | verdict |
|---|---|---|
| design/factory-rules-debt.md | `scripts/tests/test_null_outcomes.py:589-595` (K0.15) | unchanged — S1 edge E1 keeps its row |
| | `scripts/tests/test_s1_s2_contract.py:319-325` (G1-10) | unchanged — S1 edge E2 |
| | `tools/piles.py:2381` `DEBT_REL` (+ `tools/test_piles_close_id.py:87-89`) | unchanged — S1 edge E3; witness `pytest tools/test_piles_close_id.py` |
| | `scripts/tests/test_stand_gap_carry.py:1383` (docstring mention of the FR-7 row) | unchanged (GW1-36 changes it) |
| | comments: `gate_preflight.py:5267`, `project_decisions.py:39`, `window_record.py:317`, `references/field-producers.json:9` | `project_decisions.py:39` comment changes in S8; `window_record.py:317` in S9; others unchanged |
| | `scripts/tests/test-layers.json:3413` (a covers list) | unchanged |
| design/factory-rules.md (only if F-L12) | `tools/factory_rules_index.py:24` (index from titles), `tools/test_factory_rules_index.py:11`, `tools/test_quarantine.py:52`, `.githooks/pre-commit:52` | unchanged — a Check line is not a title; `factory_rules_index.py --check` stays green |
| scripts/tests/test_stand_lease.py | none outside the package | — |
| scripts/candidate_evidence.py | `context_bundle.py:164-176`, `coverage_contract.py:57` (read the output dict) | unchanged (same output) |
| scripts/profile_contract.py | gate-registry rows (sites), many importers of its functions | unchanged (membership only) |
| scripts/driver_stage_s8s9.py | none in tools/.githooks/.claude | — |
| scripts/run_suite.py | `tools/controller-blocks-gen.py` mentions other scripts, not this one | unchanged |
| scripts/tests/fixtures/judgment-census.json | `tools/architecture_gate.py:88` `CENSUS_REL` (HEAD vs index), `.githooks/commit-msg:36`, `tools/source_split.py:48` | unchanged — a lowered ceiling passes the gate |
| scripts/check_witness.py, exit_gate.py (S7) | `check_delivery.py:716`, `artifact_producer.py:79`, `references/ahead-cards.json`, `references/delivery-reason-owners.json:19,27` | unchanged (exit 0 path only gains an advice block; `delivery-reason-owners` matches `check_witness.py` at the start of a reason — the manifest path, which has a rule) |
| scripts/project_decisions.py (S8) | `tools/collect_intake.py:61,609-610,757` imports it and calls `parse_findings` | unchanged API — S8 edge E2 (no raise at import); witness `pytest tools/test_collect_intake.py` |
| scripts/factory_dashboard.py (S8) | none in tools/.githooks/.claude | — |
| references/templates/factory-backlog.md (S8) | `tools/collect_intake.py` / `tools/test_collect_intake.py:798-916` read PROJECT copies named `factory-backlog.md` | unchanged (they parse the findings table, which S8 does not touch) |
| window_record.py, controller.py (S9) | `tools/controller-blocks-gen.py:145,186-194,342` (route texts naming `window_record.py`) | changes in S9 if a block route changes: regenerate `design/controller-blocks.md` (AR-9 change check) |
| stage_guard.py, host_adapter.py (S10) | `tools/controller-blocks-gen.py:342` (`stage_guard.dispatch_errors`), `tools/test_collect_intake.py:543` (path pattern only) | unchanged by S10's own change (names, not functions) |

## §6. Forks (returned, not decided)

### Owner (product behaviour, priorities, process risk) — one list

**F-O1 — the unknown branch of each FR-59 debt gate (G1-G13 + `environment_property_cover`).** The registry
already DECLARES a target branch for ten of fourteen; the conversion (T2, `gate_template.acceptable` at the
literal sites) is what is owed. Four have no target (`debt`). Per gate:

| gate | declared now | recommendation | consequence for the run |
|---|---|---|---|
| stand_identity | question, wait at stage entry | keep | a stand that cannot be identified asks the person before the stage, never runs on a guess |
| provenance_acceptance | question, wait at stage entry | keep | as above, per use |
| test_identity | rerun | keep | an unknown identity means "run again", never reuse |
| collected_ids | **debt** | **rerun** (the run itself checks the ids: pytest exit 4 -> `node_id_mismatch`) | no extra question; an id that does not exist is said by the run |
| live_check_demand | **debt** | **question at window acceptance, to the code critic** (novelty unknown -> the critic decides whether a probe is owed) | one more critic judgement on legacy rows; never a silent pass |
| s5_coverage | question, window acceptance | keep | |
| s5_window | question, window acceptance | keep | |
| delivery | **debt** | **refuse_with_door**: a kind the kinds file does not hold makes the verdict `no` and names the unrecognised kind as a factory defect (FR-19) | as today in effect, now stated |
| case_preconditions | question at gate A | keep | |
| environment_preparation | question at authorization | keep | |
| baseline_identity | refuse_with_door | keep | |
| s5_stand_limits | **debt** | **question at stage entry** (an unmeasured limit is asked, as stand_identity) | one more question when a limit cannot be measured |
| reporter_rehearsal_identity | rerun | keep | |
| environment_property_cover | question at gate A | keep | |

Executable on the recommendation? The registry edits are reversible; the conversions are code nodes (§3
table) — safe to draft on the recommendation, built after the answer.

**F-O2 — R1: add probe rows for languages without `assertion_probes` (Kotlin, Go, Ruby …) now?** Options: (a)
none now — the door `red_sandbox.py --probe` and the data-gap refusal stand, a row is added when a project of
that language arrives (TESTING.md: the case comes from a defect); (b) write rows now for a named list. Rec (a):
a row written without a live project is unproven and a wrong row writes false receipts. Cost of (b): a row per
language plus a live proof each (FR-33). One road holds either way (data row read by suffix, P31).

**F-O3 — X9: may a PROJECT bring a fourth finding addressee?** (a) no — the three words are the factory's own
process contract; S8 moves them to a package data file (FR-13 satisfied); (b) yes — a project config key with
the package file as default (AR-3). Rec (a). S8 is executable on (a) and reversible.

**F-O4 — X3: the conductor's prompt replaces the default system prompt instead of being appended?** (a) switch
`--append-system-prompt-file` to a replacing flag for the conductor only — cheaper turns, but the conductor
loses the host's default tool guidance (behaviour risk); (b) keep, and record as a real limit. Rec: neither
blind — ONE measured experiment first (PROJECT.md п. 6 (а), CLAUDE.md pt. 6 a): one conductor call each way on
a recorded question, compare turns and outcome; then decide. Not executable before the answer (behaviour risk).
Not a host/gateway setting (P25): it is the driver's own argument.

**F-O5 — W2: how many of the 221 `command` doors get an executed test?** (a) all; (b) the four repeating
families (`--operation checkpoint`, `gate-decision`, `semantic_reopen`, `recover`) as ONE parameterised table
in an existing keep test, one row per family on a real story fixture; (c) none — the route map stays, a door
test is added only when a door is found broken. Rec (b): the class already produced two real defects
(controller-blocks walk), and TESTING.md allows a case from a defect; (a) contradicts the owner's word of
10.11.2026 on test volume. Executable on (b) after the answer (it adds test lines).

**F-O6 — R9: which is the home of a bug file?** `bug_records.py:10` says the project's `qa-factory/bugs/` is
canonical ("owner, 30.09"); the reporter's charter (OH5-9) and `publish` use `<task root>/bugs/`; readers read
both. Options: (a) the task root is where the reporter writes, the project home is read for older bugs — align
`common-rules.md:116` (+ 11 slices) and the `bug_records` docstring; (b) the project home is canonical — revert
OH5-9 and S4 together. Rec (a) (it is what the code accepts today). S4 is safe on (a) and reverted with OH5-9
on (b).

### Lead (technical)

- **F-L1 (R2)**: (a) `manifest_put.py` resolves a hand-typed pytest id through `node_ids` at store time
  (FR-16 "at the moment it is stored"), "not verified" where no collect is possible; (b) `s5_precheck._why_no_row`
  asks pytest. Rec (a). `manifest_put.py` is in TR4-17's owns: queue after it.
- **F-L2 (R3)**: where "skipped because the product has no such surface" is typed: (a) a closed skip-reason word
  on the run row mapped to `pending_implementation` in `delivery-verdict-kinds.json`; (b) the analyst's S7
  verdict. Rec (a) with the role choosing the word (P27); plan critic (meaning of a delivery word).
- **F-L3 (W3)**: (a) a rule per artifact (five contracts to design); (b') "not checked" ADVICE at exit 0 (S7).
  Rec (b') — it uses the existing contract and matches the registry row.
- **F-L4 (R4)**: the S7 rework door for a case-less `bug_candidate` (controller schema). Rec: a typed
  `--candidate <K-n>` in place of `--cases` for that route; designer + plan critic; `controller.py` HOT.
- **F-L5 (G14)**: (a) real limit — the floor protects the detector from a data edit (gate_registry.py:33-35);
  (b) move to data with a schema "may only add". Rec (a): move the row to "Real limits".
- **F-L6 (G15)**: (a) data table with the in-code floor and refusal direction (S10); (b) real limit (a safety
  allowlist is not "variety"). Rec (a) for package data only (no project key), with the adversarial list of S10.
- **F-L7 (X7)**: widen TR6-3 (thinking-roles/6, not taken) with the excess direction as a data join:
  a role granted Bash with no `role-commands.json` row is reported. Rec: yes (data join, class xref, owner data).
- **F-L8 (X1)**: re-measure hand-patching of the four artifacts in the next live run (FR-55) before building an
  editor; one `live-runs` line. Rec: yes.
- **F-L9 (X2 residue)**: `s5_precheck._open_oracle_door` names the binding road by a capability key of the
  file's language row (marker form vs `manifest_put` fragment), never by the language name (AR-1, P31). Rec:
  a node in this topic after S3 (it needs the capability key confirmed in `detectors.json`).
- **F-L10 (X4, X11 rest)**: one scout dispatch: "does the MR route record its provenance and tell a lost login
  from not found?" and "which S0 / `run` / guarded-step texts still relay raw output?" with trails.
- **F-L11 (N1)**: a node converting the 55 A27 sites (or a written decision that the ratchet is the residue's
  owner). Rec: a node in an untaken driver-hosts batch.
- **F-L12 (R6)**: amend the FR-5 and FR-23 *Check* lines to name `references/null-outcomes.json` and
  `test_null_outcomes.py` (S1b). Rec: yes — it names an existing check's carrier, no meaning change.
- **F-L13 (X10)**: confirm the debt row's direction (Q7 A) and send S9 to the plan critic.

## §7. Order, phases, live-runs

Phase 1, now, in parallel (six disjoint writers): S1a, S2, S3, S4, S5, S6.
Phase 2 after the forks: S7 (F-L3), S8 (F-O3), S10 (F-L6; after TR6-3 if taken), S9 (plan critic first,
F-L13), F-L1/F-L2/F-L4/F-L9 nodes (designer), the FR-59 nodes Q-G1..Q-G14 (F-O1; designer per gate).
Phase 3: S1b moves the fixed rows; the batch canon on CI (builder-rules 7b).
Meaning changes needing the plan critic before code: S9, F-L2, F-L4, and each FR-59 conversion.
One critic pass per topic after the code (R13-g): topic "rules debt, phase 1" for S1a-S6.

Closed by code, not proven — rows for the `live-runs` pile (FR-33): R9 (reporter prompt path), S7's text to
the role at the exit gate, S8 (template words a role reads), S9 (a person's word on a review gap), plus the
already-queued R1 (B-373) and R4.

## §8. Small technical choices I closed

- S1 runs in two passes so the debt file has one writer at a time.
- S3 includes `profile_contract.LEVELS` (same class, same five words; rule 9 sweep).
- S5's new test case is a row of `test_node_ids.py`, the registry-named test.
- S7 uses the existing ADVICE form rather than a new exit code (no contract change).
- S8 keeps the template's prose and adds a data-join row instead of deleting the meanings humans read.

## §9. Reading trail

Read: debt file (whole); `plans/builder-rules.md`, `docs/TESTING.md` (whole); `driver_stage_s8s9.py:140-419`;
`bug_records.py:1-40`; `gate_brief.py:4962-5001`; `gate_preflight.py:5755-5829`; `driver_s0.py:2360-2389`;
`guard_pre_tool.py:1290-1319`; `validate_artifacts.py:640-749`; `contract.py:1457-1512`; `check_witness.py:270-319`;
`exit_gate.py:112-161`; `detector_verdict.py:1-60`; `gate_registry.py:1-110`; `gate-registry.json:1-360,483-548`;
`stage_guard.py:2500-2594`; `host_adapter.py:440-549`; `driver_runner.py:580-629`; `run_suite.py:1785-1864`;
`window_record.py:1725-1774,1870-1913`; `audit_factory.py:1667-1717`; `candidate_evidence.py` (whole);
`project_decisions.py:36-75`; `templates/factory-backlog.md` (whole); `manifest_view.py:1-25`;
`role_permissions.py:1-30`; `s5_precheck.py:315-339,1640-1667`; `driver_dialog.py:61-91`;
`test_controller_blocks.py:1-40`; `test_s1_s2_contract.py:316-329`; `test_null_outcomes.py:586-595`;
`tools/piles.py:2376-2400`; `factory-rules.md` FR-54 (:498-503); `architecture.md` change-check lines;
pile files: `thinking-roles/batch-6` (:1-30), `words-gates/batch-1` (:20-39), `conductor/batch-5` (:1-24),
`grounding/batch-2` status lines. Greps (all with the call shape noted in §2/§5; negatives carry a positive
control of the same call: X1 Glob found `plan_row.py`; X2 Grep found the `testproject1` comment; A23 absence
in `audit_factory.py` checked against `A27` found in the same file earlier).

## §10. Noticed, not widened

- `profile_contract.LEVELS` third copy (taken into S3 by the sweep).
- `s5_precheck.py:1661` pytest-only door for every language (F-L9; a P31 sibling).
- FR-54 in the released package names `docs/SIBLING_MAP.md`, which the release repository does not carry
  (FR-37/FR-44 sibling) — a finding for the Lead, not this spec.
- `environment_property_cover` shares `debt_ref` B-283 with `reporter_rehearsal_identity`.
- `witness_backstop.exempt_reason` promises a T3 node "makes it print not checked" — S7 is that node's content.
- `test_controller_blocks.py:14` docstring says 81 command blocks; `controller-blocks.md:21` says 221.
- The debt file's run-5 table rows R5/R8/R11 were closed in code months ago and nothing moved them: the debt
  file has no detector for "row closed in code, still listed" (a calibration-check candidate, not proposed here).

## The owner's word on forks F-O1..F-O6 (17.11.2026, Lead session) — binds §6

- **F-O6** (home of a bug file): «ок» to (a) — the reporter writes under the task root, the project home is read for
  older bugs. S4 stands; `common-rules.md:116` (+ slices) and the `bug_records` docstring are aligned by a follow-up stream.
- **F-O5** (command doors): «ок» to (b) — the four repeating families as ONE parameterised table.
- **F-O4** (conductor prompt replaces the default): «ок и учти что мы планируем оркестратора полностью заменить
  дирежёром. Надо что бы он справлялся» — one measured experiment both ways first; the measure also judges whether the
  conductor still copes without the host's default tool guidance (it is to replace the orchestrator entirely).
- **F-O2** (probe rows for languages without `assertion_probes`): «если не пишем, то значит критик должен ломать код и
  смотреть что тест падает, то есть делать мутантов. Иначе фабрика встанет на любом проекте с не учтённым языком» —
  (a) is taken ONLY with its condition: on a language with no row the role's own probe (`red_sandbox.py --probe`,
  P30: the role breaks the code and sees the test fall) must be a working road end to end, proven by a scenario row
  "suffix with no probe row -> the role's probe road, the stage does not stop" and by the queued live proof B-373.
  A language with no row that stops the factory is a defect (P22).
- **F-O3** (a fourth finding addressee) and **F-O1** (`s5_stand_limits` and the other three unknown branches): the owner
  asked what these are; explained in chat 17.11, her word is pending. S8 stays executable on (a).
