# t-1252 - plan critic, second pass, on spec U7 r2 (fix round t-1249 of t-1240)

Under review: `docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r2.md` (the whole file; it replaces r1). Input: the first verdict
t-1242 and the brief. Base: HEAD = origin/main = 44585bce. Package paths below are under `ai-packages/qa-factory/`.

**Verdict: NEEDS WORK.** 3 findings block dispatch of the streams they name: N1 (node 4b), N2 (stream 7, and stream 1 item 4
behind it) and N3 (stream 5b). 9 findings must be fixed before dispatch (M-a .. M-i). Streams 2, 3, 4a and 6 are dispatchable as
written. 5a can go once M-a, M-b and M-c are fixed. The whole round-1 list was taken up, and B3, B4, B6 and M1-M7 are fixed in
code-true form. All three meaning changes the round introduced stop short of the reader that decides the story's outcome. The
reducer would rewrite a log verdict to `inconclusive`. Delivery would refuse the `not_executed` report that S7 now accepts. And
the S5 close would write a manifest that the witness readers then refuse. No path gets stuck any more. But every all-manual story,
and every undriven case F-3 sends to the agent, ends at delivery as a factory-owned `no`. Accepting the plan, and any change to
a fork, is the Lead's or the Architect's decision (rule 6).

## Blocking findings

**N1 - node 4b / F-13(a): a log verdict can never count, and the record type is the wrong carrier (K2b, K7).**
The spec says the record "joins `current_manual_checks` with `judged_from: log` (the reducer already counts manual results:
`finalize_task.py:622, 631`)". Its non-goals include "reducer changes". The facts:
- `manual_evidence.py` writes only `schema_version: 2` records (1403, 1536, 1945). The reducer sends every v2 record through
  `coverage_contract.validate_manual_current` (`finalize_task.py:563-571`). On any error it rewrites the record to
  `result="inconclusive", evidence_validated=False` (571).
- `validate_manual_current` errors on every `automate` obligation: "manual capture not authorized by planned scope/oracle"
  unless `decision` is `manual-agent`/`manual-human` (`coverage_contract.py:794-796`). It also requires runtime before/after
  provenance, `gate_a_decision_ref`, `approved_policy_hash`, the pinned `case_version` and a current S6 dispatch (812-856). A
  record built from a log has none of these.
- So `log-verdict --result pass` lands as `inconclusive`. Execution stays `not_executed` (`finalize_task.py:632-637`). The DoD
  row "reporter none + log verdicts pass -> S7 entry accepts (`passed`)" cannot be reached, and neither can L6. The error
  direction is safe, but a builder cannot meet the DoD without editing `coverage_contract.py`, which no stream owns. The
  alternative is a non-v2 record, which goes down the legacy branch (`finalize_task.py:547-549`) with no validation at all: a
  role's pass counted with no evidence check.
- Readers of `current_manual_checks` (`contract.triage_targets` 4655, `s7_pretriage`, the ledger and the check_delivery
  coverage) read a row there as MANUAL evidence for its obligation. An automate case "covered by a manual check" bypasses the
  manifest's then-bindings and probe chain. That is FR-18: a log line is evidence the test ran, not that its Thens were
  asserted. The new `judged_from` field has no named reader (AR-22).

Fix: return F-13 to its decider with these facts, because (a) as written is not executable. Whichever option stands, the spec
names (i) the record's shape and the reducer branch it takes, (ii) the validation it passes, in which owned file, and (iii) how
the coverage readers count an automate obligation answered by a log verdict, together with the reader of `judged_from`. It also
says whether the verdict is per case or per instance: `--case` takes one verdict, while the admission binds "the case's
instance's" block.

**N2 - stream 7 / F-12(a): delivery's twin of the S7 entry is left unchanged (K2a, K4).**
`check_delivery.run_reasons` (1282-1297) returns "execution_status is 'not_executed' - only ['passed','failed'] can deliver" for
any `not_executed` report without an S6 code-only receipt. The kind is `run_not_deliverable` (`check_delivery.py:2623`), which
is `{"verdict": "no", "owner": "factory"}` (`references/delivery-verdict-kinds.json:41`). The two readers are twins by
construction: `_s6_closed_by_code` (1301-1308) is "read by the one reader S7 uses", `s7_pretriage.s6_closed_by_code`. Stream 7
widens only the S7 twin.

Walk 1 - an all-manual story whose rows are only `inconclusive`/`unprepared`:
- the reducer gives `not_executed` (`finalize_task.py:629-637`; `contract.result_status` leaves `inconclusive` and an empty
  result unaliased, `contract.py:4249-4265`);
- after stream 7, S7 triages, or closes by code through `s7_pretriage` (`driver_stage_s7.py:94-118`);
- S8 runs;
- `check_delivery.assess` adds a factory-owned `no`. That record hides the `unprepared_walk` -> `after_checks` record
  (`delivery-verdict-kinds.json:51`), which is exactly what F-3 aims at ("the person gets the remainder").

Nothing gets stuck, but the verdict is wrong and the owner is wrong (P21, AR-27). §3 (v) "with an empty one present no refusal
... fires; OUT of code change" is false for this story. L2 and L4 would show it live.

Walk 2 - a mixed story whose automated half broke: the `no` from `run_not_deliverable` is honest there.

Fix: one predicate in `s7_pretriage` ("`not_executed` whose deciding non-passed rows are all manual triage targets"), read by both
`failures_to_triage` and `run_reasons`, as `s6_closed_by_code` is read now. Narrowing it to "no automated instance in a
non-terminal state" also keeps Walk 2's door. `check_delivery.py` (run_reasons) goes into stream 7's owns, and a row goes into
`test_check_delivery.py` (keep, gate_named). Stream 6 owns `check_delivery.py` too (stand_word), so the spec names the order of
the two. Stream 1 item 4 waits for this fix, not only for stream 7's merge.

**N3 - stream 5b / B2: the empty manifest fails the run-witness rule at three readers (K2c).**
`acceptance.run_witness_excused` (631-649) is "the ONE reader of 'no run to witness'". It returns `""` for `{"tests": [],
"unresolved": []}`: `handed` is empty, and `ids` is empty, so `ids and ...` is False. All three of its readers then require
`run_witness`:
- `check_witness.RULES["automation-manifest.json"]` (229-234);
- `validate_artifacts` (105, 1733-1737);
- `handoff_check` (150).

`check_delivery.witness_reasons` (711-724) turns the check_witness refusal into "manifest witness: run_witness missing ...". Its
kind is `factory_record`, which is `no`/factory (`delivery-verdict-kinds.json:40`). So every all-manual story, even one whose
manual checks all pass, ends at delivery as a factory-owned `no`. The spec's "writer check" stops at the writer (`manifest_put`),
and §3 lists `check_delivery` reads of the manifest but not `witness_reasons`. The answer to "do all readers accept an empty
manifest" is no.

Fix: `run_witness_excused` gains an outcome for the derived-empty S5. It is bound to the controller's own S5 code-close receipt
(`stages.S5.code_only`, the twin of `s6_closed_by_code`), never to `tests == []` alone (AR-28: an automator that wrote nothing
must not be excused). `acceptance.py` (run_witness_excused) goes into 5b's owns, with a row in `test_check_witness.py` (keep,
scenario) or `test_check_delivery.py`: "derived-empty S5 close -> no witness owed; empty manifest without the receipt -> still
refused".

## Fix before dispatch

**M-a - r8: two person contacts for one fact.** The `install_dependencies` row (conductor-actions.json `actions`) ends a failed
install with "tell the person ... and offer: install it yourself / go on without ... / stop". The spec then gives the card at the
next rehearsal as well (§2 r8 edge "the conductor's install fails"). That is two stops for one missing binary, which
`gate_preflight.py:2968-2970` forbids in its own words, and it breaks axis 5 "one question for every stop" (FR-7). Fix: say that in
the gate-turn context the conductor ends its turn without asking, and the card is the person's one question.

**M-b - r8 road 3: the one-call bound and the role-side door.** Road 3 does not read `state/executor-turns.json`. A gate-A turn,
then a mid-S5 `executor_unavailable` with `install`, pays a second install, against the stated invariant "one conductor call per
key". The spec also says road 3 "reaches the conductor through `handle_refusal`". But `run_suite.py` is run by the automator,
and `skills/qa-story/phases/s5.md:144` tells that role to "stop, quote its `question` verbatim, record the answer the way s4.md
does". That is a door to a person past the role, in a file no stream owns. Fix: `executor_install` returns no command when
`executor_turn_had` holds. Name s5.md:144 and put it in 5a's owns, or state why the role's stop still reaches the conductor first.

**M-c - stream 5a item 5 points `check_s5_credentials` the wrong way.** The conditional "if it raises a card at zero automate
rows it returns like 2841-2851" would cut a legitimate question. The check asks for the default login on `default_login_needed`,
"ONE rule with S6" (`gate_preflight.py:4627-4631`, AR-19), and manual-agent cases need that login at zero automate rows. The
conditional moves the question to S6. Fix: credentials unchanged; B-006 (iii) "keys" is OUT, for that reason.

**M-d - F-14 = (b) is decided and has no executor.** Stream 5a lists "check_s5_dependencies unknown (F-14)" as a non-goal, and no
other stream or node takes it. Assign it, or open a node with an owner (rule 9 exit form).

**M-e - r11: the derived-empty condition reads past an unknown.** `controller.stage_scope` returns `derived: True` once ANY row
has a disposition (`controller.py:4252-4275`). Rows with no disposition, and `unmapped_scope` cases, then fall into no group. A
"derived and empty" S5 could close over cases nobody disposed (AR-28). Fix: add `unmapped_scope == []` and every row disposed
to the condition, or cite the refusal that guarantees both before S5.

**M-f - Q13(d) for r2's new paths.** §8 answers the r1 block only. I ran the tool over the paths r2 adds (trail). It prints 10
`more` lines: manual_evidence.py, s6.md, driver_stage_s7.py, driver_core.py, driver_dispatch.py, run_suite.py, halts.md,
driver_gates.py, controller.py, driver_stage_s5.py. Each needs "interface kept: <why>" or a `--readers` listing. The N2/N3
fixes add check_delivery.py and acceptance.py to that run.

**M-g - texts that turn false and have no owner (FR-37, axis 1).**
- `docs/SIBLING_MAP.md:130` (axis 5 row) says "the controller refuses `code_only` S5 today" and "S5 owes the same precondition
  and bound". 5b changes the first and does not state the second.
- `design/architecture.md` §A map lines for axis 2 ("an undeclared surface takes the web road silently") and axis 7 ("a row with
  no URL passes S0 as in-process, silently") turn false after stream 1. "How the map is walked" requires the line to be edited in
  the same commit, but the brief's non-goals say «Не менять architecture.md». That conflict is a fork for the Lead.
- The `driver_stage_s7.py:87-93` position-invariant comment ("a halted run is never triaged") turns false after stream 7. It
  sits in stream 7's owns.

**M-h - census and ratchet ownership.** 5a's DoD requires `dry_exits.py --check` to show 0 discrepancies. A new gate-to-conductor
road may need its `driver-exits/<group>.json` row, and 5a does not own that file. §1.2 also has no row for the new admission
check of `manual_evidence.py log-verdict` (owner and census class).

**M-i - variety walk labels.** Axis 13 is filed with r9's capabilities, which belong to axes 8 (git on PATH), 3 (tests_root)
and 5 (tracker credentials). Axis 13's real content in this spec is F-1(a), the legacy config with no `profiles`. Its stated
unknown value -> outcome for axes 2, 3 and 4 depends on N1-N3.

Line drift, not findings (the spec cites `path::symbol`): controller `code_only` stage set is now at 6097-6098; "Capture first"
is at `manual_evidence.py:1877`.

## K1 - fix completeness (checked against code)

- **B1: partly.** r4 is re-classed B, node 4b exists, and the S7 premise reproduces (`driver_stage_s7.py:13-20`). The new
  carrier fails at the reducer (N1).
- **B2: partly.** The writer check holds: `manifest_put.run` refuses only the no-key fragment (2498-2501), and the remaining
  checks iterate lists. The readers fail (N3), and so does the delivery leg of §3 (N2). M-e and M-g are also open.
- **B3: fixed.** `install_dependencies` and `stand_prepare` rows exist, r9 is cut, and AR-12 is restated per site. M-a remains.
- **B4: fixed.** Every named home is in `keep` (the test-layers lookup in the trail); `test_surfaces.py` is in quarantine and
  is not edited.
- **B5: fixed.** The three roads are in 5a. M-b remains (s5.md:144).
- **B6: fixed.** It follows `close_reporter_bound` (`driver_gates.py:1024-1073`). The `no_move` stop goes to
  `hand_to_conductor` (947-952, 1022). The record states absent, unreadable and write-fails are stated.
- **M1: fixed.** `NM.EXCLUDED_KINDS = ("s1_review",)` (`no_move.py:37`); `_no_move` skips the call only on `call is False`
  (`driver_conductor.py:646`).
- **M2: fixed.**
- **M3: fixed.**
- **M4: fixed.**
- **M5: fixed.** "Capture first" refusal at 1877; the `unprepared` row is a triage target (`contract.py:4659-4662`).
- **M6: fixed.**
- **M7: fixed.** The five new keys are absent from p1/p2 (0 hits each); control "The names are examples, not a list": 1 hit.
- **M8: partly** (M-h).
- **Q13(d): partly** (M-f).
- **Q12: fixed.** A class A note is planned; Q-U8 is the U8 node.

## K2 - meaning changes

**(a) F-12:**
- Premise measured: `finalize_task.py:629-637` and `driver_stage_s7.py:13-20`.
- Error direction: correct for S7. `execution_status` is not rewritten.
- Downstream: delivery reads `not_executed` as a factory `no` (N2). That is not a pass and not a stuck stage, but it is a
  wrong-owner verdict for (i) and an honest one for (ii).
- Gate B / handoff_check only carry the field (`handoff_check.py:357-359, 745`).
- The S8 `stage_done` does not call `check_delivery` (0 hits; control `factory_fixable` -i: 4 hits).

**(b) F-13:**
- The admission is tight on the four adversarial inputs named (fabricated path, another case's block, a reporter, a stale
  fingerprint).
- P27/AR-29 holds in intent: the role judges, code checks shape.
- The reducer count and FR-18 fail (N1). `judged_from` has no reader (N1).

**(c) 5b:**
- The writer can produce the empty manifest.
- Its readers refuse it (N3). Apart from that, no reader reads it as "automation done and green" (the `_completeness` plan-row
  walk; `stage_guard.manifest_unread` wants only presence).
- The S6 twin is unchanged and correct: `s6.nothing` cites the manifest as evidence, `driver_stage_s6.py:542`.
- Axis 38 is named.

## K3 - stream 5a

The positional invariant is sufficient:
- the `run` tuple is at `gate_preflight.py:6086-6094`;
- `check_s5_dependencies` sets `self._drift = []` before anything that can raise (2889), so a failing or switched-off check
  reads as "no install known", which gives the card;
- `run`'s docstring ("read-only except ONE file") stays true, because the turn record is written by the driver.

AR-25: absent, unreadable and write-fails each have an exit. AR-12: the paid call fires only on a known install command. One
observation, not a finding: when the drift is about packages other than the launcher, the turn may install and still end in the
card. This is bounded at one per key.

## K4 - class walk (verdict per item)

1. `executor_question` callers: gate 2871 and 2974, run_suite 1566. All are in 5a.
2. `run_suite.executor_gap` 1648-1670: the detector feeding road 3. Its behaviour does not change: n/a.
3. `s5.md:144` role door: unfixed (M-b).
4. halts.md:28 row: in 5a.
5. S7 entry `failures_to_triage`: stream 7.
6. Delivery `run_reasons`: unfixed (N2).
7. Manifest witness readers (check_witness, validate_artifacts, handoff_check, check_delivery.witness_reasons): unfixed (N3).
8. `stage_guard.manifest_unread`: accepts a present manifest: n/a.
9. `s6.nothing`: unchanged twin: n/a.
10. `check_s5_credentials`: wrongly targeted (M-c).
11. `check_s5_dependencies` unknown: decided, unowned (M-d).
12. SIBLING_MAP axis 5 row: unowned (M-g).
13. Axes 18 and 38: M-h.
14. Axis 34 (one road): Q-U8 node.

## K5 - executability

Files, functions and rows per item are named, and every test home is a keep file. Overlaps:
- 4b and 7 share `test_story_run_s7.py` (sequenced, stated);
- N2's fix puts `check_delivery.py` in both 7 and 6;
- stream 1's whole-file `planning_contract.py` sits beside OF5-1 (cross-batch, stated).

The order is consistent: RD1-24 before 4a; RD1-13 and RD1-14 (rules-debt/1, which touch gate_preflight.py and run_suite.py)
before 5a; FV3-21 and OF5-5 before 6; PC4-2 and PC4-4 owner-blocked, U7 first. Not executable as written: 4b (N1), 5b (N3),
7 (N2), and 5a's item 5 (M-c).

## K6 - architecture and principles

The AR list is right, plus AR-27: §1.1 says "not met", but N2 and N3 are owner-of-verdict breaks. AR-2's passage clause holds
per site. P2 is kept (no platform word; E7 waits). P27 holds, except for N1.

VARIETY: on an all-manual project (axis 4), on a project with an undriven surface (axis 2) and on a `reporter: none` project
(axis 3), the plan now reaches delivery with no stuck stage. But it ends in a factory-owned `no` (N2, N3, and N1 for axis 3),
where a free agent would report "checked by hand / could not check". That is worse than the bar until N1-N3 are fixed. Web/API
projects are unchanged.

## K7 - forks

- **F-11 (a): consistent.** No row settles a missing folder.
- **F-12 (a): consistent in direction, incomplete** (N2). I would not reverse it.
- **F-13 (a): inconsistent with `coverage_contract.py:794-796` and `finalize_task.py:563-571`** (N1). This is a finding that
  names the fact. The decision stays with the Architect/Lead.
- **F-14 (b): consistent, unowned** (M-d).
- **Q-U8: consistent.** `collect_base` keys on `PYTEST_TOKENS` (151, 440).

## Spot-checks and negatives

- The five K3/K4 keys are absent from p1/p2; positive control: 1 hit.
- `check_delivery` is absent from stage_done.py; positive control: `factory_fixable` -i, 4 hits in the same file.
- No `run_witness` excuse exists for an empty manifest: read through the function body, `acceptance.py:631-649`.

## Trail

Read:
- the spec r2 (whole), verdict t-1242 (whole), the brief (whole);
- `driver_stage_s7.py` 1-139;
- `finalize_task.py` 525-669;
- `contract.py` 4235-4284, 4595-4691;
- `coverage_contract.py` 771-857;
- `s7_pretriage.py` (whole);
- `manual_evidence.py` 1010-1054, plus Grep `schema_version: 2|RESULTS`, `Capture first`;
- `run_suite.py` 340-389, 1545-1584, 1645-1674, plus Grep `no_report_words(`;
- `check_delivery.py` 700-739, 1270-1319, 2590-2649, plus Grep `not_executed`, `run_reasons(`;
- `delivery-verdict-kinds.json` (Grep);
- `check_witness.py` 88-113, 225-239;
- `acceptance.py` 631-661;
- `validate_artifacts.py` 105, 152, 1733-1737, 2680-2709;
- `stage_guard.py` 1005-1034;
- `manifest_put.py` 2480-2708, 2950-2993;
- `driver_stage_s5.py` 180-249;
- `controller.py` 4225-4279, 6070-6109;
- `driver_stage_s6.py` 495-544;
- `driver_core.py` CODE_CLOSE_SITES (Grep);
- `gate_preflight.py` 2815-2994, 4603-4652, 6078-6110;
- `driver_gates.py` 20-59, 890-1073;
- `driver_conductor.py` (Grep `no_move`);
- `no_move.py:37`;
- `conductor-actions.json` (rows install_dependencies, stand_prepare);
- `skills/qa-story/phases/s5.md` 138-153;
- `driver_dispatch.py` 3100-3124;
- `import_test_receipt.py` 1-60;
- `design/architecture.md` 20-72;
- `docs/SIBLING_MAP.md:130`;
- the pile rows of RD1-13, RD1-14, RD1-24, FV3-21, OF5-5, PC4-2 and PC4-4.

Commands:
- test-layers lookup: all 14 named homes are `keep`; `test_surfaces.py` is `quarantine`.
- `git rev-parse HEAD origin/main` -> 44585bce, both.
- `owns_readers.py --paths <10 r2 paths> --names log-verdict judged_from executor_install executor_turn_had close_executor_bound s5.nothing`
  -> "readers: 598 outside owns, 10 lines below -- base origin/main 44585bce" (10 `more` lines, M-f).
- the M7 key grep -> 0 hits on each of the five keys, control 1.

```json
{
  "verdict": "blocker",
  "blockers": [
    "N1 node 4b / F-13(a): manual_evidence writes v2 records; finalize_task.py:563-571 sends them through coverage_contract.validate_manual_current, which refuses an automate obligation (794-796) and requires capture provenance (812-856), so a log pass becomes inconclusive; DoD row 'S7 accepts (passed)' unreachable with reducer changes a non-goal; a legacy-shape record would skip validation; coverage readers would read it as manual evidence (FR-18); judged_from has no reader (AR-22)",
    "N2 stream 7 / F-12(a): check_delivery.run_reasons (1282-1297), the twin of failures_to_triage through s6_closed_by_code, still gives run_not_deliverable = no/factory (delivery-verdict-kinds.json:41) for not_executed after a real S6, masking unprepared_walk after_checks; every all-manual story with an inconclusive/unprepared row and every F-3 undriven case ends a factory-owned no; section 3 (v) premise false",
    "N3 stream 5b / B2: acceptance.run_witness_excused (631-649) returns empty for tests [], so check_witness RULES (229-234), validate_artifacts (1733-1737) and handoff_check require run_witness; check_delivery.witness_reasons (711-724) gives factory_record no for every all-manual story; the excuse must bind the S5 code-close receipt, never the empty list alone"
  ],
  "fixes": [
    "M-a r8: conductor install_dependencies fallback asks the person and the next rehearsal cards again; one question per fact (gate_preflight.py:2968-2970, axis 5)",
    "M-b r8 road 3: executor_install must honour executor_turn_had; skills/qa-story/phases/s5.md:144 (automator stops and asks) is an unowned door past the role",
    "M-c stream 5a item 5: check_s5_credentials stays (default_login_needed shared with S6, AR-19); B-006 (iii) keys OUT",
    "M-d F-14 (b) decided but excluded by 5a and owned by no stream or node",
    "M-e r11: derived-empty must also require unmapped_scope empty and every row disposed (controller.py:4252-4275)",
    "M-f Q13(d): answer the 10 more-lines of owns_readers over r2's new paths (base 44585bce), plus check_delivery.py and acceptance.py",
    "M-g stale texts: SIBLING_MAP.md:130 axis 5 row (5b), architecture.md section A axes 2 and 7 lines vs brief non-goal (Lead fork), driver_stage_s7.py:87-93 invariant comment (stream 7)",
    "M-h 5a DoD dry_exits --check needs a driver-exits group file in owns; section 1.2 lacks the log-verdict admission unit",
    "M-i variety walk: axis 13 holds r9 capabilities that belong to axes 3/5/8; axis 13 content is F-1(a)"
  ],
  "class_completeness": "Not complete. Fixed in plan: the three executor_question roads (gate 2871, 2974; run_suite 1566), halts.md:28, S7 entry, S6 twin unchanged. Unfixed siblings: check_delivery.run_reasons (twin of failures_to_triage via s6_closed_by_code), the three run_witness readers behind acceptance.run_witness_excused, skills/qa-story/phases/s5.md:144 role-side executor door, check_s5_credentials wrongly targeted, F-14 unowned, SIBLING_MAP axis 5 row and architecture.md axis 2/7 lines. Axes walked: 1, 5, 18, 34, 38 and the 13 variety axes.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-u7-pass-without-stuck-spec-r2.md",
      "docs/tasks/specs/reviews/t-1242-u7-pass-without-stuck-plan.md",
      "docs/tasks/specs/20261117-u7-pass-without-stuck-brief.md",
      "ai-packages/qa-factory/scripts/driver_stage_s7.py",
      "ai-packages/qa-factory/scripts/finalize_task.py",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/coverage_contract.py",
      "ai-packages/qa-factory/scripts/s7_pretriage.py",
      "ai-packages/qa-factory/scripts/manual_evidence.py",
      "ai-packages/qa-factory/scripts/run_suite.py",
      "ai-packages/qa-factory/scripts/check_delivery.py",
      "ai-packages/qa-factory/references/delivery-verdict-kinds.json",
      "ai-packages/qa-factory/scripts/check_witness.py",
      "ai-packages/qa-factory/scripts/acceptance.py",
      "ai-packages/qa-factory/scripts/validate_artifacts.py",
      "ai-packages/qa-factory/scripts/stage_guard.py",
      "ai-packages/qa-factory/scripts/manifest_put.py",
      "ai-packages/qa-factory/scripts/driver_stage_s5.py",
      "ai-packages/qa-factory/scripts/controller.py",
      "ai-packages/qa-factory/scripts/driver_stage_s6.py",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/driver_gates.py",
      "ai-packages/qa-factory/scripts/driver_conductor.py",
      "ai-packages/qa-factory/scripts/no_move.py",
      "ai-packages/qa-factory/references/conductor-actions.json",
      "ai-packages/qa-factory/skills/qa-story/phases/s5.md",
      "ai-packages/qa-factory/design/architecture.md",
      "docs/SIBLING_MAP.md",
      "plans/piles/rules-debt/batch-1-phase-2.md",
      "plans/piles/onboarding-forge/batch-5-ostatki-hf8-4-i-oh3-42.md",
      "plans/piles/package-ci/batch-4-dieta-testov-td-11-td-15.md"
    ],
    "reruns": [
      {"command": "python -B tools/owns_readers.py --repo C:/QAFactory/forge-repo --paths <10 r2 paths> --names log-verdict judged_from executor_install executor_turn_had close_executor_bound s5.nothing", "result": "readers: 598 outside owns, 10 lines below -- base origin/main 44585bce"},
      {"command": "python -B -c <test-layers.json lookup of 15 named test files>", "result": "14 keep (gate_preflight gate_named, story_run_s7 data_join, manual_evidence detector, s5_window_leftovers detector, controller_state detector, question_branches data_join, no_move_seam_sites detector, story_run_s6 gate_named, human_questions table, probe_by_code data_join, readiness detector, null_outcomes gate_named, check_delivery gate_named, check_witness scenario); test_surfaces.py quarantine"},
      {"command": "grep -c -i <five stream-2 keys> p1-discovery.md p2-interview.md; control 'The names are examples, not a list'", "result": "0 hits each; control 1"},
      {"command": "git -C C:/QAFactory/forge-repo rev-parse --short HEAD origin/main", "result": "44585bce 44585bce"}
    ]
  }
}
```
