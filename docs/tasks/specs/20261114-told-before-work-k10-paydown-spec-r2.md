# Told before work: K10 pay-down, r2 (designer, t-825; revises r1 of t-816)

Status: DRAFT r2 for Lead acceptance. A REVISION of `20261114-told-before-work-k10-paydown-spec.md` (r1): it applies the plan
critic's verdict `reviews/20261114-tbw-k10-paydown-plan-critic.md` (t-821) and the Lead's decisions 1-8 of the t-825 dispatch.
Everything the verdict did not fault is kept from r1 (r1 §2 tables stay the history; their E numbers are superseded by the
verdict's measures, cited below). ONE fork is returned (§6, F-KR); the cards are buildable on its recommendation.

Base: worktree `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r` (branch `wip/tbw-t1r`, 8d71532b). `W` =
`C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory`. Numbers: **M** = measured by the critic (verdict
line cited); **E(M)** = a sum of M parts done by me (no new measure; error = the parts' own); **E** = estimate with basis.

Build order: **K1a -> K2 -> KR -> (batch canon) -> K1b**. K1a and K2 have DISJOINT owns (K1a writes no `stage-joints.json`
in r2: every proof flip moved to K1b by decision 1), so they may be dispatched in parallel; KR needs both merged; K1b needs
KR merged and the canon output.

---

## §0 What changed against r1

| item | what r2 does | where |
|---|---|---|
| B1 (proof rule changed silently; hidden-raise rollback; stand/begin with no design) | Decision 1 (a): K1 split. K1a = `refuse` printer (named helper) + provoking rows, flips NOTHING; K1b = proof constants + markers, dispatched only after the canon ran K1a's rows green; the rule "proved = provoked by a test that RAN" unchanged. K1b's rollback is a NAMED raise. `execution_request:stand`, `run_suite:begin` dropped from L3; queue Q1 | §5 K1a, K1b (edges K1b-E5, rollback); §7 Q1 |
| B2 (writer join via `_form_candidates` drops `tried` for the analyst) | writers = every `from` of `handoffs/index.yaml` rows (secondary and purpose rows included) through `handoff.index()`, the module's one reader of the index; join-test row on the secondary contract `s7-analyst-to-scribe` | §5 K2 item 1, tests `K10p/narrowed-by-contract/*`, `K10p/secondary-writer` |
| B3 (L7 saves 0; E4 wrong way) | `<!-- roles: -->` (verified: `ROLE_MARKER` group is empty -> `[]`, `contract_slices.py` 61, 141, 148-149; the form is already used at `references/common-rules.md` 130 and 167) on a new `### The digest line`; E4 rewritten; test that the strategist slice (and every role's) lacks the block | §5 K2 item 4, edge K2-E4, test `K10p/digest-block-on-page-only/*` |
| B4 (`####` is no heading; parent marker is strategist-only; `surfaces` loss) | two `###` headings in the verdict's order: kept bullets (incl. `surfaces`) -> `<!-- roles: -->` moved block -> `<!-- roles: qa-test-strategist -->` re-opened block for the JSON example; `surfaces` KEPT (saving 765 B, M, verdict line 89) | §5 K2 item 5, test `K10p/observation-bullets-moved` |
| B5 (OQ-1 false on measured numbers) | OQ-1 withdrawn; the raise is settled by the owner's word (decision 7, card KR); the only owner question left is K3 yes/no with measured savings | §4, appendix A |
| S1 (arithmetic; §2.4 automator claim) | §1 is the verdict's measured table; findings_tooling leaves the automator too (`s7-automator-to-analyst` has only `rounds[].finding`, verdict C5) | §1, K2 item 1 |
| S2 (`controller:s5_plan_gaps.rework_rows` misassigned) | K2 item 6: stages `S5`, producer `qa-automator`, `when` `plan` (controller.py 6919-6940 read: fires only for the automator plan dispatch); walk of other `controller:*` rows queued to a scout (Q3) | §5 K2 item 6; §7 Q3 |
| S3 (red_sandbox cost; 1430-1431 carrier) | cost stated (clone(s) before the refusal, `red_sandbox.py` 1645-1664); the in-process sites 1431 and 2041 are advisory (the probe goes on) and never count as carriers | §2 AR-12; K1a-E8 |
| S4 (K4 NO-GO) | K4 dropped (decision 6); not a fallback in r2 | §4 |
| S5, S6 (K3 road walk, required marks) | K3 not built; appendix A names both as its conditions | appendix A |
| S7 (baseline lowering required) | every card: `process_ratchet_tokens` set to the measure (slack 0, already enforced by `role_load.process_ratchet_problems`), `ratchet_tokens` lowered where `ratchet_excess` names a role, `native_headroom` lowered (or removed when U <= H) wherever U falls below its row; KR edits the pin `test_contract_slices.py` 865; K2 lowers `COMMON_LAYER_CAP_BYTES` (same class, axis 18) | K2 item 8, KR, K1b item 5 |
| S8 (slow file in the DoD) | no card runs a file listed in `scripts/slow_tests.json`; listed files are named "judged by the batch canon" (`test_judgment_census.py`, `test_stage_joints.py`, `test_audit_rules.py`, `test_red_sandbox_probe.py`, `test_probe_by_code.py`, `test_execution_request.py`) | every DoD |
| S9 (K0 done by the review) | K0 dropped (decision 5); each DoD prints U before/after | §1, DoDs |
| S10 (untraceable "Lead note 2a/2b") | citations replaced: L1 = S-2 report Q2 (`docs/tasks/specs/reports/20261114-t1r-sites-s2-report.md` line 79, in the worktree); L2 = the comment of `test_contract_slices.py` 980 ("`import_test_receipt` prints the FIRST check only") | §5 K1a given |
| Decision 6 (K3) | appendix A, measured 3,686 / 3,182 / 5,576 B | appendix A |
| Decision 7 (owner's word) | card KR; code-critic between K2 and K1b: §6 F-KR | §5 KR, §6 |
| designer, not from the verdict | (1) census edit removed from K2: its only real change (`check_findings` roles) needs the dense `blocking_per_role` ceilings recomputed by a slow file the builder may not run; `tried_errors` already lists exactly the 10 writers; queued Q4. (2) `test_stage_joints.py` removed from K2 owns: no pin names the narrowed rows (Grep over `scripts/tests` for the row ids: no hit; positive control: the same Grep found `EG-digest-form` in `test-layers.json` 4617). (3) the import road's records reach `refuse` through `run_guarded` (the Record is `exc.args[0]`; `records` sits on the exception, `role_cli.py` 181-185, `import_test_receipt.py` 268-269), so K1a also changes `run_guarded`. (4) edge: a key page left with no row is unlisted | K2, K1a, K1b-E6 |

r1 forks the decisions did not name, carried unchanged (cards built on r1's recommendation; Lead acceptance of r2 accepts
them): F-4 (a) drop the EG-digest-form leniency clause (L6, 257 B per role, M); F-5 (b) card sentences left to T1r-cards
(L8 not built); F-7 L12 prose pass: queued (Q5), no longer on the critical path once KR exists. F-1 is closed by decision 7
(the strategist's row becomes its measured U). F-2/F-3/F-6: decisions 6 and 7.

---

## §1 The numbers (M, verdict lines 25-109; nothing re-measured)

U = bytes of layers charter + injection_common + injection_role of `role_load.static_load(role, "first")`; H = 100000 - 26000 x P -
5400 - 200; K10 green when U <= H or U <= the role's `native_headroom` row (`role_load.py` 334-338).

| role | P | U now (M) | H | row now | after K1a | after K2 (E(M)) | after K1b (E(M)) |
|---|---|---|---|---|---|---|---|
| qa-code-critic | 1 | 74,417 | 68,400 | none | 74,417 | 72,829 (verdict line 104: -877 -176 -257 -278) | 67,012: -5,817 = L1+L3 6,480 (line 80) minus stand+begin 663 (line 133); green only if every ER/RS id it holds is proved on all three roads (K1b-E7) |
| qa-automator | 1 | 81,385 | 68,400 | none | 81,385 | 79,914: -799 -352 -257 -278 +215 (S2, line 105) | 76,486: -3,056 (L2, line 81) -372 (window_first, line 82) |
| qa-test-strategist | 2 | 55,976 | 42,400 | 46,008 | 55,976 | 53,489: -799 -176 -257 -278 -765 -212 (lines 83-89, 106), plus the new `### Example of one obligation` heading in its slice (E, about +32 B) | 53,489 (holds no ER/RS row) |

Price of a row at U (the verdict's formula, lines 363-365): Codex refuses the role when its `project:` files together exceed
94,400 - U characters (each also capped at 26,000). At the E(M) sizes: automator after K2 ~14,486 (`framework-rules.md`),
after K1b ~17,914; strategist ~40,911 (`test-strategy.md` + `project-profile.md`); code-critic at 72,829 ~21,571
(`framework-rules.md`). KR and K1b print the price from the MEASURED U, never these E(M) values.

---

## §2 Architecture invariants, owners, census (designer rule 1; CLAUDE.md rule 10; AR-29, P27)

| AR | touched by | how kept | change check in the DoD |
|---|---|---|---|
| AR-10 requirement before the work | K1a, K2, K1b | a row leaves a page only (a) for a pre-action call refusal that a RUN test proved prints it (K1b), or (b) for a role no check of that row can judge (K2 L4, S2), or (c) where the same requirement stays on the page (K2 L7/L9: the row is on the page); `surfaces` bullet kept (B4); `tried` stays told to the analyst (B2) | `T1rp/no-row-lost/<role>`, `K10p/narrowed-by-contract/*`, `K10p/secondary-writer`, `K10p/digest-block-on-page-only/*` |
| AR-11 only needed context | K2, K1b | one statement per requirement; rows a role cannot be judged on leave it | U before/after in each report |
| AR-12 friction | K1b | the code-critic learns a call-told ER/RS row at the refusal of `red_sandbox.py`, which refuses only AFTER `prepare()` cloned the sandbox (and a second clone with install budget for an own baseline, `red_sandbox.py` 1645-1664): the price is that wall time, not "one turn"; `probe_by_code` pre-action refusals touch nothing | K1b report states it |
| AR-13 one reader / one renderer | K1a, K2 | `role_cli.refuse` stays THE printer; extra lines are rendered by `stage_joints.told_line` (THE line renderer); the index is read only through `handoff.index()` | grep in K1a report: no `- [` literal in `role_cli.py` |
| AR-15 one survivor | K2 | the row survives; the slice duplicate is unmarked, the source keeps it for whole-file readers | `--write` diff touches only the moved blocks' slices and the pages |
| AR-18 one refusal shape | K1a | `refuse` keeps its line order; LAST line stays `  check: <first check>` | row `K10p/refuse-*/last-line-is-check` |
| AR-20 shrink-only | K2, KR, K1b | every ratchet lowered to the measure where it falls; KR's raises and K1b's rollback raise are NAMED (commit message + changelog) | `test_role_load.py` 566 (process exact), `contract_slices.py --check` K10 lines |
| AR-22 field has a reader | K1a | `records` of a `RequestError` (producer `execution_request.py` 377, `import_test_receipt.py` 269) get their reader in `refuse` | `K10p/refuse-*/records-printed` |
| AR-23 empty outcome | K1a, K2 | no records -> output byte-equal to today; a family with 0 rows -> no index line (existing T1rs row) | `K10p/refuse-*/no-records` |
| AR-1 closed variety is data | K2 | which roles a handoff_check row tells is computed from contract data (`handoff.index()`, `handoff.null_outcomes`, `handoff.spec`, `handoff_check.TRIED_CONTRACTS`), never a role-name list | `K10p/narrowed-by-contract/*` |
| AR-29 code judges data | all | no judgment moves into code; the proof constants are data; the J1 judgment (which slice block the row fully states) is the designer's, corrected for `surfaces`, accepted by the Lead | critic question 11 |

Checks added or altered, the owner each serves, census class:

| check / function | change | owner served | census class |
|---|---|---|---|
| `role_cli.refuse`, new `role_cli._extra_record_lines`, `role_cli.run_guarded` | print every distinct further refused check | data (carries the requirement to the role) | printer; not a judging unit (if the census scanner lists it, class `shape`, owner `data`, unchanged) |
| `T1rs/marked-by-proof` constants (`test_contract_slices.py` 977-981, 969) | proved sets per road | data (join proof <-> marker) | test-only |
| `K10p/*` rows | joins and renderer tables | data | test-only |
| `stage-joints.json` roles of `handoff_check:null_outcome.*`, `:findings_tooling`, `:tried`; `controller:s5_plan_gaps.rework_rows` stages/producer | narrowed / corrected | data (label fix) | no unit |
| `contract_slices._section_lines` | no legend on page 2+ | data (renderer) | no unit |
| markers in `common-rules.md`, `artifact-contract-plan.md` | blocks unmarked for roles whose page holds the row | judgment (designer; accepted by the Lead) | no unit |
| `exit_gate:EG-digest-form` sentence | clause dropped (F-4 (a)) | judgment (designer: the clause states what is NOT refused; Lead accepts) | no unit |
| `native_headroom` rows (KR) | named raise to measured U | intent (the owner's word, 14.11.2026) | no unit (a ratchet value) |
| `audit_factory.COMMON_LAYER_CAP_BYTES` | lowered | data (ratchet) | no unit |

One road (P31): every lever is one rule for every role (family, proof, contract data); no role is exempted by name; the raise
applies the one K10 rule to every role over H at its measured size.

---

## §3 Levers in r2 (r1 §3 kept; changes only)

L1 (code-critic roads): carry tables per road + provoking rows (K1a), flip after canon (K1b). L2 (import road prints every
check): K1a printer, K1b flip. L3 reduced to `selector_args`, `window_first` (rows already written: `test_execution_request.py`
`t1rs_sites_after_the_probe`, labels `T1rs selector_args` / `T1rs window_first`, lines 2135-2210, "WRITTEN, NOT RUN"); stand,
begin dropped. L4-L7, L9 in K2 as fixed by B2-B4. L6 per F-4 (a). S2 lever in K2. L8, L10 (K3), L11 (K4), L12, L13: not built.

---

## §4 What the owner is asked (replaces OQ-1)

Nothing about the ceiling: decision 7 is the owner's word («если не получится, то поднимай», 14.11.2026). KR's report gives
the owner, in plain words, the measured sizes and the price (§1 formula). One owner yes/no remains, appendix A (K3).

---

## §5 Builder cards

Common to every card (not repeated): given also `W\design\factory-rules.md` whole, `C:\QAFactory\forge-repo\plans\builder-rules.md`,
`C:\QAFactory\forge-repo\docs\TESTING.md`, `W\design\architecture.md`; the builder works and commits in the worktree; it does
NOT run CI, wait for a pipeline, run mutations, or run any file listed in `W\scripts\slow_tests.json` - such a file is
written and named "judged by the batch canon"; U is printed by this pure-read command, from any cwd (call it U-CMD):
`python -B -c "import sys;sys.path.insert(0,r'C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts');import role_load as R;[print(r,sum(l['bytes'] for l in R.static_load(r,'first')['layers'] if l['name'] in R.NATIVE_LAYERS)) for r in ('qa-automator','qa-code-critic','qa-test-strategist')]"`.
Report: `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-k10-paydown-<card>-report.md`
with U-CMD output before and after, FR walk (sections A-G), verbatim witness, slow files named.

### K1a - the refusal prints every refused check; provoking rows (no flip)

given: this file §2, §5 K1a; `W\scripts\role_cli.py` (`_is_record` 74, `refuse` 79-104, `run_guarded` 152-193);
`W\scripts\import_test_receipt.py` (`_told_request_error` 260-270); `W\scripts\execution_request.py` (`RequestError` 31-35, 375-377);
`W\scripts\stage_joints.py` (`told_text` 581, `told_line` 603, `row_for`); `W\scripts\red_sandbox.py` (`_carry_told` 1292-1301,
refused-run sites 1701-1714 and 2190-2198, advisory sites 1425-1432 and 2035-2042); `W\scripts\probe_by_code.py` (`Refusal` 205-213,
printers 8283-8285, 8364-8373, post-launch sites 4693-4695 and 6255-6266, the `refusal("execution_request:...")` construction at
2695-2698); `W\scripts\branch_accounting.py` (`limit` 96) and `W\references\branch-accounting.json` (`refusal_units_shown` 20);
the S-2 report line 79 and S-1b question 3 (worktree `docs\tasks\specs\reports\`); tests `test_detector_verdict.py`,
`test_import_test_receipt_refusal.py`, `test_red_sandbox_probe.py`, `test_probe_by_code.py` (all `keep` in `test-layers.json`).
owns:
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\role_cli.py (refuse, run_guarded, new _extra_record_lines)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (new table K10p/refuse-*)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_import_test_receipt_refusal.py (rows K10p/import-prints-every-check/*; an existing row pinning "first check only" is updated)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_red_sandbox_probe.py (rows K10p/rs-told-passes-through/*)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py (rows K10p/pbc-told/*)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\changelog.d\tbw-k10-paydown-k1a.md
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-k10-paydown-k1a-report.md
non-goals: `stage-joints.json`, `slices/`, `role-load.json`, `test_contract_slices.py` (all K1b); any row sentence; `red_sandbox.py`
and `probe_by_code.py` code; `hooklib.block`, `stage_guard.deny` (one Record each, no `records`); `role_cli.epilog`; a new test file.
handoff: commit + report: the carry table (below), the verbatim witness, the K10p row labels K1b will look for in the canon.
What changes:
1. `role_cli.refuse(command, problem, stream=None, *, check=None, records=())`: after `how to prove it` and before `if you
   cannot`, print `_extra_record_lines(records, first, own)`, one per line. `first` = `problem.check` when `problem` is a
   Record, else `""`; `own` = `role_cli:<command>`.
2. new `_extra_record_lines(records, first, own) -> list` (the helper the verdict's CODE QUALITY line asks for): walk `records`
   when it is a list or tuple (anything else: `[]`); keep items for which `_is_record` is true; drop a check equal to `first`,
   to `own`, or already kept (first-seen order); render each kept check as `"  " + stage_joints.told_line(row)` where `row =
   stage_joints.row_for(check)[0] or {"check": check}` (import `stage_joints` INSIDE the helper: `stage_joints` imports
   `role_cli` lazily, a top-level import would be a cycle). Cap: `n = branch_accounting.limit("refusal_units_shown")`, imported
   inside the helper; when more than `n` lines remain, keep the first `n` and add `f"  {rest} more refused checks are not
   shown: fix these and run the command again; it names the rest"`. If the import or `limit` raises, no cap (print all).
   Never raises (wrap the body; on any exception return what was built so far).
3. `run_guarded`, the `ValueError` branch: pass `records=getattr(exc, "records", ())` to `refuse`.
4. Provoking rows (written; the slow files are judged by the canon):
   - `test_import_test_receipt_refusal.py` (fast, RUN by the builder): a request failing at least three distinct request checks
     of `validate_request` goes through the real CLI road (`run_guarded`); assert every check id appears as a `- [<id>]` line,
     once, and the last line is `  check: <first id>`.
   - `test_red_sandbox_probe.py` (slow): table `K10p/rs-told-passes-through/<case>`: cases `one-entry`, `three-entries`,
     `repeated-check` - a parsed `run_suite.py --mine` refusal summary with that `told` list reaches the refused answer of the
     probe road (site 1707-1714) and of the diagnostic road (site 2195-2198) with every distinct entry, in order.
   - `test_probe_by_code.py` (slow): table `K10p/pbc-told/<printer>/<case>`: printers `plan` (8284), `tool` (8367), `refusal`
     (8372); cases `one-record`, `two-records`, `repeated-check` - a `Refusal`/`ToolRefusal` with those records, raised into the
     printer, prints JSON whose `told` holds every distinct check; plus one row per `execution_request:*` / `run_suite:*` id
     cited in a pre-action `Refusal(...)` construction of `probe_by_code.py` (today at least `execution_request:profile`,
     2697), provoked through its real function.
5. Carry table in the report (data for K1b), built by reading code, every entry with file:line: for `red_sandbox` and
   `probe_by_code`, each site that prints an `execution_request:*` / `run_suite:*` `told`, classed **P** (a pre-action refusal
   of the call: printed by 1707-1714 / 2195-2198, or by 8284 / 8367 / 8372) or **L** (printed after a launch: 4693-4695,
   6255-6266) or **A** (advisory, the call goes on: 1425-1432, 2035-2042); and per id: carried at P only / at L too / not
   carried. Commands: Grep `refusal\("(execution_request|run_suite):` and `told_fields|_carry_told` over both files.
edges:
- E1 `problem` a plain `str`, or `records` empty / absent / not a list or tuple: output byte-equal to today. Invariant: no
  refusal changes for a caller with no records.
- E2 `records[0]` is the first Record again (as `_told_request_error` builds it): not printed twice. Invariant: one line per
  distinct check.
- E3 a non-Record item: skipped. Invariant: `refuse` never raises.
- E4 a record whose check is `role_cli:<command>`: skipped (the card lines say it).
- E5 cap: AT `n` extra lines all print; at `n+1` the first `n` print plus the tail line naming 1. Invariant: never a silent
  drop; the role learns the rest by the next call.
- E6 POSITIONAL: extra lines stand after `how to prove it` and before `if you cannot`; the LAST line is `  check: <first
  record's check>`. Invariant: `story_run.match_known` and every reader of the last line see what they saw.
- E7 a row id `row_for` cannot read: `told_line({"check": id})` prints the "could not be read" sentence (`told_text` 593).
  Invariant: an unknown is said, never a pass, never a crash (FR-41).
- E8 TEMPORAL: before K1a the import road prints the first check only; after it every check. No marker moves in K1a, so no
  page changes and no U changes. Invariant: a row leaves a page only in K1b, after the canon.
- E9 the A sites (1431, 2041) are never counted as carriers (S3): the call goes on, the told is printed only if a later run
  is refused. The L sites carry nothing for K1b (r1 rule: ids printed only after a launch stay page-told).
- Error direction (reused functions in a gate-input role, rule 1): `told_fields`, `_carry_told`, `told_line` may err toward
  printing MORE, never toward a carrier the carry table claims and the code does not print; adversarial inputs that must stay
  on the safe side: an empty record list, a summary whose `told` is not a list, two refusals of one check, a refusal after a
  partial launch (class L).
tests: `test_detector_verdict.py` table `K10p/refuse-<case>`: `no-records`, `records-not-a-list`, `first-repeated`,
`non-record-item`, `own-command-check`, `unreadable-row`, `at-limit`, `beyond-limit`, `last-line-is-check`, `records-printed`
(run with a patched `limit` of 2 for the limit rows). Rows of item 4.
DoD (from the worktree root):
1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/role_cli.py ai-packages/qa-factory/scripts/tests/test_detector_verdict.py ai-packages/qa-factory/scripts/tests/test_import_test_receipt_refusal.py ai-packages/qa-factory/scripts/tests/test_red_sandbox_probe.py ai-packages/qa-factory/scripts/tests/test_probe_by_code.py` - every printed file not in `slow_tests.json` run alone; the rest named "judged by the batch canon".
2. `python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py` and `python -B ai-packages/qa-factory/scripts/tests/test_import_test_receipt_refusal.py` (each alone, green).
3. `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
4. U-CMD before and after: identical (E8).
siblings: `role_cli.epilog` (twin of `refuse`, untouched); `hooklib.block`, `stage_guard.deny` (one Record, untouched);
`red_sandbox._carry_told` / `probe_by_code` `told_fields` callers; SIBLING_MAP axis 34 (one printer), axis 18.
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-k10-paydown-spec-r2.md
architecture: AR-13, AR-18, AR-22, AR-23 -- the records an error carries reach the role through the one printer and the one line renderer; the last line kept; no records, no change
judgment: none -- printer and test rows only

### K2 - one statement per requirement (L4, L5, L6, L7, L9, S2)

given: this file §2, §5 K2; `W\references\stage-joints.json` rows `handoff_check:tried` (5310), `:findings_tooling` (5384),
`:null_outcome.*` (5458-5680), `exit_gate:EG-digest-form` (1106-1110), `controller:s5_plan_gaps` (2818) and
`.rework_rows` (2896-2920); `W\handoffs\index.yaml`; `W\scripts\handoff.py` (`index` 320, `null_outcomes` 515, `spec` 662);
`W\scripts\handoff_check.py` (`TRIED_CONTRACTS` 1657, `check_findings` 1756-1790); `W\scripts\controller.py` 6912-6944;
`W\scripts\contract_slices.py` (`ROLE_MARKER` 61, `HEADING` 63, `parse` 124-164, `SECTION_LEGEND` 581, `_section_lines` 698-715,
`requirement_section` 718-749); `W\references\common-rules.md` 69-90; `W\references\artifact-contract-plan.md` 110-155;
`W\scripts\role_load.py` (`ratchet_excess` 145, `process_ratchet_problems` 267); `W\references\role-load.json`;
`W\scripts\audit_factory.py` 1218-1223; `W\design\role-rules.json` (anchor `Code checks: the exit gate`, line 290);
tests `test_contract_slices.py` (`test_common_rules_slices` 312, `test_t1rp` 870, `test_native_headroom` 828), `test_role_load.py`, `test_audit_rules.py` 764.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\stage-joints.json (roles of the 8 handoff_check rows named; the EG-digest-form requirement; the rework_rows row)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\contract_slices.py (_section_lines and the unreadable branch of requirement_section only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\common-rules.md (the `## Your handover` section only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\artifact-contract-plan.md (the `## Fields the plan validator checks` section only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\slices\ (generated by --write only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\inject-map.json (only to unlist a key page left with no row, edge E6)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\role-load.json (process_ratchet_tokens, ratchet_tokens: to the measure, never up)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\audit_factory.py (COMMON_LAYER_CAP_BYTES and its comment only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_audit_rules.py (the A-K1 pin of COMMON_LAYER_CAP_BYTES only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_contract_slices.py (new K10p/* rows)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\changelog.d\tbw-k10-paydown-k2.md
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-k10-paydown-k2-report.md
non-goals: `native_headroom` (KR); `judgment-census.json` (Q4); charters; `## Handoff form` (appendix A); manifest_put rows;
ahead cards; any other row's sentence or roles; the universal handoff_check rows `blocked_problem`, `claims`, `required_rows.*`;
other `controller:*` rows (Q3); deleting text from a source file (blocks move under a heading; one phrase edit in item 5).
handoff: commit + report: U-CMD before/after; per narrowed row: roles old -> new and the contract fact; the shared-layer
bytes before/after (`contract_slices.py --report`); ratchet rows changed (key, old -> new); K10 lines verbatim.
What changes:
1. L4. Writers of a contract `c` := sorted roles `r` with a row of `handoff.index()["handoffs"]` whose `contract == c` and
   `from == r`, secondary and purpose rows included, `r` restricted to the stems of `agents/*.md` (drops `person`,
   `qa-story`, `project`). Set the single producer entry's `roles` of:
   - each `handoff_check:null_outcome.{repairs,verdict,names,report,failures,listing}` := writers of every `c` with
     `handoff.null_outcomes(c)` non-empty (verdict C5: only `s7-analyst-to-automator` -> `["qa-failure-analyst"]`);
   - `handoff_check:findings_tooling` := writers of every `c` whose `handoff.spec(c)` holds the path `findings[].cause` (C5:
     only `s5-critic-to-automator` -> `["qa-code-critic"]`);
   - `handoff_check:tried` := writers of every `c` in `handoff_check.TRIED_CONTRACTS` (10 roles; `qa-failure-analyst` through
     the secondary `s7-analyst-to-scribe`; leaves `qa-case-critic`, `qa-code-critic`; equals the census row of
     `tried_errors`, `judgment-census.json` 487).
2. L5. `_section_lines`: page 1 = `[SECTION_HEAD, "", SECTION_LEGEND]`; page n >= 2 = `[f"{SECTION_HEAD} (continued from
   ...)"]` only. Same rule in the unreadable branch of `requirement_section` (730).
3. L6. `exit_gate:EG-digest-form` requirement: delete exactly the sentence beginning "A verdict or a state word outside the
   form's list is advice" through "when mending makes the form pass." (and the space before it). Nothing else.
4. L7. In `references/common-rules.md`, inside `## Your handover: the form, then the digest line` (`<!-- roles: all -->`),
   order becomes: the form paragraph (72-76, unchanged); blank; the sentence "Code checks: the exit gate; the refusal names what
   is wrong and the way through. What the next role or the human needs is in the FILE or the FORM: chat does not survive the
   dispatch." (verbatim, its own paragraph: the role-rules anchor stays in the source); blank; `<!-- roles: -->`; `### The
   digest line`; "Your final message IS the digest, three parts, no prose:"; the fenced block (verbatim); "One row per item
   in your scope, the ones that went nowhere included."; then the existing `<!-- roles: qa-scout, ... -->` `## No writes`.
   Why `<!-- roles: -->`: all 12 roles hold `exit_gate:EG-digest-form` on their pages (verdict C6), so the marker that
   excludes every role whose page holds the row lists no role.
5. L9. In `references/artifact-contract-plan.md`, `## Fields the plan validator checks (coverage-observation-v1)`: after the
   `coverage_delta` bullets, `` `observation_contract` (on each obligation): `` followed by the KEPT bullets `surfaces` and
   "A ref (...)" (in that order; in "A ref" replace "the refs below" by "every other `*_ref` of the observation contract");
   blank; `<!-- roles: -->`; `### observation_contract fields the S3 row states`; the MOVED bullets `claim_kind`,
   `oracle_ref`, `independent_expectations ... source_conflicts`, `No-write`, `no_leak` (verbatim); blank;
   `<!-- roles: qa-test-strategist -->`; `### Example of one obligation`; the JSON block (verbatim). The designer's check
   (accepted J1, corrected by B4): each moved bullet's content is in the row `coverage_contract:obligations.observation`; the
   `surfaces` clause "`gap_reason` only on a `gap`" is not, so `surfaces` stays.
6. S2. Row `controller:s5_plan_gaps.rework_rows`: `stages` `["S5"]`, `when` `["plan"]` (as its sibling `controller:s5_plan_gaps`),
   producer `roles` `["qa-automator"]`, `field` "the reworked rows of `work/s5-plan.json`"; requirement and door unchanged.
7. `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`.
8. Ratchets (S7): from `python -B ai-packages/qa-factory/scripts/role_load.py --all --json`, set every
   `process_ratchet_tokens.<role>` to its printed process tokens (all 12 move: L6, L7); lower `ratchet_tokens.<role>` to the
   printed tokens for every role whose row is more than `ratchet_slack_tokens` (1000) above it; `COMMON_LAYER_CAP_BYTES` :=
   the `shared` bytes `contract_slices.py --report` prints, rounded UP to a multiple of 250, only if that is below 10,750
   (then the A-K1 pin and the comment's measured number move with it).
edges:
- E1 a contract later gains a null outcome / `findings[].cause` / a TRIED entry: the join row is red naming the role to add.
  Invariant: a check never judges a role its row does not tell.
- E2 a predicate with no writer, or `handoff.index()` unreadable: the join row is red naming why; never read as "no writers".
  If a narrowing would leave a row with `roles: []`, the card STOPS for that row and reports (measured: none does).
- E3 `stage_joints.py --check` names a narrowed row: STOP, report its line verbatim.
- E4 (rewritten, B3) no block becomes unread by a role that is judged on it and has no row for it: a block is unmarked for a
  role only when that role's `rows_for` holds the row stating it. Today `<!-- roles: -->` is that set for L7 (all 12 hold
  EG-digest-form); a role gaining an agent file without that row would be red in `K10p/digest-block-on-page-only`.
- E5 POSITIONAL: a `###` marked `<!-- roles: -->` under a `##` keeps `inherited` of the `##` for the next unmarked `###`
  (`parse` sets `inherited` only on `##`, 153-154); the re-opened strategist block is marked explicitly. Invariant: no other
  block changes its role set; the `--write` diff touches only `common-rules.md` slices (12), the strategist's
  `artifact-contract-plan.md` slice and key pages.
- E6 dropping 176 B per continuation page (and moving rows) can leave a listed key page with no row (`NONE_CONTINUED`): remove
  that page's line from `inject-map.json` roles.<role> and `--write` again (it deletes the file); a page count pinned in a test
  moves to the measure. Invariant: `T1rp/pages-listed/<role>` and `T1rp/no-row-lost/<role>` green.
- E7 TEMPORAL: before K2 the rows/blocks are as today; after it the narrowed rows, headings and pages land in ONE commit with
  regenerated slices.
- E8 role-rules: `role_rules.py --check` 0 findings (anchors live in source files, unchanged).
- E9 K10 after K2 is still red for all three roles (§1); K2 never touches `native_headroom` (KR does).
tests (`test_contract_slices.py`, fast): `K10p/narrowed-by-contract/<row>` (8 rows: roles == writers by the predicate);
`K10p/secondary-writer` (`qa-failure-analyst` in roles of `handoff_check:tried`, and `handoff.contract_of("S7",
"qa-failure-analyst") != "s7-analyst-to-scribe"`: it reaches `tried` only through the secondary row); `K10p/continuation-no-legend/
<1|2|3 pages>`; `K10p/digest-block-on-page-only/<role>` (12 roles: slice lacks "Your final message IS the digest" iff the
page holds `exit_gate:EG-digest-form`; `qa-test-strategist` named) + negative control (source with the marker removed -> the
strategist slice has the block); `K10p/observation-bullets-moved` (strategist slice lacks the five moved bullets, holds
`surfaces` with "only on a `gap`", holds "A ref" and the JSON example; the row holds each moved field token);
`K10p/rework-rows-on-automator` (row on the automator's pages, not on the strategist's).
DoD (from the worktree root):
1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/references/stage-joints.json ai-packages/qa-factory/scripts/contract_slices.py ai-packages/qa-factory/references/common-rules.md ai-packages/qa-factory/references/artifact-contract-plan.md ai-packages/qa-factory/references/role-load.json ai-packages/qa-factory/scripts/audit_factory.py` - files not in `slow_tests.json` run alone; `test_stage_joints.py`, `test_judgment_census.py`, `test_audit_rules.py` and every other listed file named "judged by the batch canon".
2. `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`, then `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` (only K10 lines may remain, for the three roles).
3. `python -B ai-packages/qa-factory/scripts/stage_joints.py --check`
4. `python -B ai-packages/qa-factory/scripts/role_rules.py --check` (0 findings)
5. `python -B ai-packages/qa-factory/scripts/tests/test_contract_slices.py` and `python -B ai-packages/qa-factory/scripts/tests/test_role_load.py` (each alone; the only red allowed: `T3a (h)` keys_findings and `T3a (j)` shipped green, both K10, closed by KR).
6. `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; U-CMD before/after.
siblings: the universal handoff_check rows (`blocked_problem`, `claims`, `required_rows.*`) - not narrowed, every contract carries
them; `exit_gate:digest` restates EG-digest-form (196 B, Q2); the three `field.*` rows (Q2); other `controller:*` rows (Q3);
`kb/` pages quoting rows; SIBLING_MAP axis 18 (ratchets), axis 32 (census: Q4), axis 34.
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-k10-paydown-spec-r2.md
architecture: AR-1, AR-10, AR-11, AR-15, AR-20, AR-23 -- rows told exactly to the roles whose contract a check can judge; one statement per requirement, the row survives; ratchets lowered to the measure
judgment: J1 -- which slice blocks a row fully states was judged by the designer (corrected for `surfaces`), accepted by the Lead

### KR - named raise of the K10 rows to the measured size (owner's word)

given: this file §1, §5 KR, §6; `W\references\role-load.json` (`native_headroom` 38-40, `note` 2); `W\scripts\role_load.py`
302-346; `W\scripts\tests\test_contract_slices.py` 828-865; the K2 report.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\role-load.json (native_headroom only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_contract_slices.py (the pin at 864-865 only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\changelog.d\tbw-k10-paydown-kr.md
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-k10-paydown-kr-report.md
non-goals: any text, row or page; `ratchet_tokens`, `process_ratchet_tokens`; `role_load.py` code; H, `MAX_BLOCK_CHARS`, the
12,000-byte cap.
handoff: commit + report: U-CMD output; the rows written; the price per role in plain words.
What changes (precondition: K1a and K2 merged into the branch):
1. Run U-CMD. For each of `qa-automator`, `qa-test-strategist`, `qa-code-critic` whose U > H (68,400 / 42,400 / 68,400): set
   `native_headroom.<role>` = exactly its printed U (keys sorted). A role with U <= H gets no row.
2. The pin at 865: the expected list = the sorted roles now in `native_headroom`; its message names the K10 rows of KR.
3. Commit message carries: the owner's word verbatim «если не получится, то поднимай» and "owner, 14.11.2026"; per role
   `<role>: <old row or none> -> <U> (named raise, AR-20)`; the code-critic line adds "TEMPORARY until K1b (fork F-KR)";
   the price per role: "Codex refuses the role when its project files together exceed <94,400 - U> characters (<files>)".
   The changelog fragment says the same in English.
edges:
- E1 TEMPORAL: before KR K10 is red for the three roles (`contract_slices.py --check` exits 2); after KR it is silent. KR
  runs only after K2 is merged (the raise is to the post-K2 measure, never the pre-K2 one).
- E2 U differs from §1's E(M) by more than 10 %: write the measured U anyway (the owner's word is "to the measured size") and
  report the gap with its cause.
- E3 the code-critic row exists only under F-KR (b); under (a) it is not written and the branch stays red until K1b; under
  (c) KR runs after K1b and writes no code-critic row.
- E4 a raise for a role the owner's word does not cover: none (the word covers every role the pay-down cannot bring under H;
  the code-critic's temporary row is the fork).
tests: none new (the shipped rows are judged by the existing `T3a (j)` rows 863-865).
DoD (from the worktree root):
1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/references/role-load.json` - non-slow files alone, slow named.
2. `python -B ai-packages/qa-factory/scripts/contract_slices.py --check` (exit 0, no K10 line)
3. `python -B ai-packages/qa-factory/scripts/tests/test_contract_slices.py` and `python -B ai-packages/qa-factory/scripts/tests/test_role_load.py` (each alone, green)
siblings: `COMMON_LAYER_CAP_BYTES` and the A22 ratchets (not raised); axis 18.
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-k10-paydown-spec-r2.md
architecture: AR-20 -- a named raise of native_headroom to the measured U by the owner's word, the price stated
judgment: none -- a ratchet value set by the owner's word

### (batch canon)

The coordinator runs the BATCH CANON on the branch (RUNBOOK §7) after KR and hands its verbatim output to K1b. K1b is
dispatched only for what the canon shows green: the K1a rows `K10p/rs-told-passes-through/*`, `K10p/pbc-told/*`,
`K10p/import-prints-every-check/*`, and `T1rs selector_args`, `T1rs window_first` (`test_execution_request.py`
`t1rs_sites_after_the_probe`). A red row is a `defect_found` on K1a; its id/road stays unproved in K1b.

### K1b - flip the proof constants after the canon

given: this file; the K1a report (carry table); the BATCH CANON output (verbatim, from the coordinator); `W\scripts\tests\
test_contract_slices.py` (`test_t1rs` 957-1038, the pin 864-865); `W\references\stage-joints.json` (the 31 ER/RS rows,
`told_ratchet`); `W\scripts\stage_joints.py` (`call_told`, `call_families`); `W\references\role-load.json`.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_contract_slices.py (test_t1rs constants and the `counted` pins; the pin 864-865)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\stage-joints.json (`told` call markers of producer entries of execution_request:* / run_suite:* rows, entry splits; told_ratchet.unsited only down)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\slices\ (generated by --write only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\inject-map.json (only to unlist a key page left with no row)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\role-load.json (native_headroom, ratchet_tokens, process_ratchet_tokens: down to the measure)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\changelog.d\tbw-k10-paydown-k1b.md
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-k10-paydown-k1b-report.md
non-goals: `role_cli.py`; any row sentence; `call_told_families`; manifest rows (`manifest` set stays page for the automator);
`execution_request:stand`, `run_suite:begin` (stay in `unproved_site`, Q1); a new test file.
handoff: commit + report: per road the proved ids as written (with the canon line that proves each), U-CMD before/after, K10
lines, ratchet rows (key, old -> new), the code-critic's state (green and row removed, or STOP).
What changes:
1. `unproved_site` (969): remove `execution_request:selector_args` and `:window_first` only if the canon shows their rows
   green; `stand`, `begin` stay.
2. Constants beside `roads_of`: `PROVED_ROAD = {"import_test_receipt": request, "red_sandbox": <"pass-through" when every
   `K10p/rs-told-passes-through/*` row is green, else empty>, "probe_by_code": <the ids of the K1a carry table carried at P
   sites only and provoked by a green `K10p/pbc-told/*` row>}`; `CARRIED` per road from the carry table (`probe_by_code`: ids
   carried at P or L; `red_sandbox`: every id, since it reprints whatever `run_suite --mine` refuses with); `carries(check,
   road)` reads `CARRIED`; `proved(check, road)` := `run_suite`: check not in `unproved_site`; `import_test_receipt`: check in
   `request` and check not in `unproved_site`; `red_sandbox`: pass-through green and `proved(check, "run_suite")`;
   `probe_by_code`: check in `PROVED_ROAD["probe_by_code"]` and `proved(check, "run_suite")`. Comments and the docstring of
   `test_t1rs` say where each set comes from (report and canon run).
3. Edit `stage-joints.json` producer entries until `T1rs/marked-by-proof` and `T1rs/entry-uniform` are green (the test names
   each `(row, role)` to change); update the `counted` pins (1020) and `T1rs/partial-split` expectations to the measure.
4. `contract_slices.py --write`; `stage_joints.py --check` (`legacy_legs 0`; `unsited` lowered if it reports below its row).
5. Ratchets (S7): `process_ratchet_tokens` to the measure for the roles that moved (automator, code-critic; runner and analyst
   if their pages moved); `ratchet_tokens` lowered by `ratchet_excess`; `native_headroom.qa-automator` := its new U (a
   lowering); `native_headroom.qa-code-critic`: deleted if U <= 68,400, else lowered to U and STOP (edge E7); the pin 865
   follows the keys.
edges:
- E1 TEMPORAL: before K1b every ER/RS row the code-critic holds is on its page; after it, those proved on all its roads leave
  for the index line. The markers, constants, slices and ratchets land in ONE commit.
- E2 a canon row red for an id/road: that id stays unproved on that road (page). Invariant: never a marker without a
  provoking row that RAN green.
- E3 the carry table names an id the road cannot raise (no cited site): `CARRIED` omits it only with the file:line reason in
  the report; an id with no reason stays carried. Invariant (error direction): a carry list errs toward MORE ids (more page),
  never fewer.
- E4 an id carried at an L site of `probe_by_code`: not proved there (page for the code-critic). Invariant: a row printed only
  after a launch never counts as told before the work.
- E5 ROLLBACK (named, B1): if a later canon shows a K1b-proving row red, the fix commit flips that id back, regenerates, and
  RAISES `process_ratchet_tokens` / `native_headroom` to the measure, naming each raise in the commit message (AR-20) - the
  rollback is a named raise, never a silent one; the event is a `defect_found` on K1b.
- E6 a key page left with no row: as K2-E6.
- E7 the code-critic still over H after K1b (the carry table proved fewer ids than the verdict's measure assumed): its row is
  lowered to the measured U, K1b STOPS and reports; the Lead takes it to the owner as a measured residual (decision 7 then
  applies to it by name).
tests: the existing `T1rs/*` rows with the new constants; new rows `T1rs/road-carries/<road>/<id>`, `T1rs/road-unproved-keeps-page/<road>`,
`T1rs/l-site-keeps-page` in `test_t1rs`.
DoD (from the worktree root):
1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/references/stage-joints.json ai-packages/qa-factory/references/role-load.json ai-packages/qa-factory/scripts/tests/test_contract_slices.py` - non-slow alone, slow named.
2. `python -B ai-packages/qa-factory/scripts/contract_slices.py --write`, then `--check` (exit 0, no K10 line, unless E7)
3. `python -B ai-packages/qa-factory/scripts/stage_joints.py --check`
4. `python -B ai-packages/qa-factory/scripts/tests/test_contract_slices.py` and `python -B ai-packages/qa-factory/scripts/tests/test_role_load.py` (each alone, green)
5. `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`; U-CMD before/after.
siblings: qa-runner and qa-failure-analyst hold the same rows (`roads_of`): their markers move by the same rule (the analyst's
roads `run_suite`, `red_sandbox`); S-2 Q1-Q3; axis 34, axis 18.
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-k10-paydown-spec-r2.md
architecture: AR-10, AR-12, AR-20 -- a row leaves a page only for a pre-action refusal a test that ran proved; ratchets and K10 rows lowered to the measure, a rollback is a named raise
judgment: none -- proof data from a run, joined by a test

---

## §6 The one fork

**F-KR (Lead; touches the owner's word) What the code-critic's K10 is between K2 and K1b.** After K2 it is 72,829 (M, verdict
line 104), over H 68,400, with no row: `contract_slices.py --check` and `test_contract_slices.py` `T3a (h)`/`(j)` are red,
and the batch canon that K1b waits for runs on that state. The owner's word covers a role the pay-down "cannot" bring under;
the code-critic can, but only after the canon.
- (a) no row: the branch stays red on K10 until K1b; the canon is read row by row with two known red K10 assertions.
- (b) KR writes a TEMPORARY named row at its measured U (~72,829), K1b removes it (or lowers it, K1b-E7); both named.
- (c) reorder K1a -> K2 -> canon -> K1b -> KR: no code-critic row ever; the canon runs with the three K10 roles red.
**Recommended: (b).** It keeps one road (the same K10 rule for every role over H, AR-20 named raise), gives the canon a green
branch, and the K1b DoD forces the lowering; the batch cannot close with the row standing (a `Остатки` line with `узел: K1b`).
Error direction: if K1b never lands, the row stays as a named raise with its price (~21,571 characters of `framework-rules.md`)
- visible, never silent. Cost of (b): one row and one pin edit twice.

## §7 Queue lines

- Q1 `execution_request:stand`, `run_suite:begin`: fixture design for a provoking row (S-1b report 41-42: a live probe / the whole
  launch); measured 663 B each for automator and code-critic. A designer node of the told-before-work pile.
- Q2 duplicates the verdict found (Q4/DUPLICATION): `exit_gate:digest` restating EG-digest-form (196 B, all 12), the three
  `handoff_check:field.*` rows with one sentence (~380 B, renderer change), the strategist card's no-write sentence (355 B, F-5).
- Q3 scout: every `controller:*` row of `stage-joints.json` against the role/dispatch its check fires for (the S2 class).
- Q4 `judgment-census.json` `check_findings` roles -> `qa-code-critic`, `conductor`, with a note and the dense
  `blocking_per_role` ceilings recomputed (needs `test_judgment_census.py`, slow: a node judged by the canon).
- Q5 L12 designer prose pass (r1 F-7) for automator and strategist: would let a later card lower their KR rows.
- Q6 K10 tightness in code: a `native_headroom` row above the measured U is red (as `process_ratchet_problems`); changes the
  pinned behaviour `T3a (j)` 854 - a Lead node.
- Q7 Appendix A of the mechanism spec (project files by path to Codex): the real cure of the KR price.

## §8 Small choices closed by the designer

- C1 test prefix `K10p/`; reports `20261114-k10-paydown-<card>-report.md`; fragments `tbw-k10-paydown-<card>.md`.
- C2 extra refusal lines are `"  " + told_line(row_for(check))` (the page's own line, unfilled, two-space indent); tail line wording.
- C3 heading words `### The digest line`, `### observation_contract fields the S3 row states`, `### Example of one obligation`.
- C4 "the refs below" -> "every other `*_ref` of the observation contract" (the strategist slice no longer has the refs below).
- C5 `when: ["plan"]` for the rework_rows row, by its sibling `controller:s5_plan_gaps`.
- C6 `COMMON_LAYER_CAP_BYTES` rounding: up to 250, as its own comment states.
- C7 `records` passed to `refuse` as a keyword (not read off the Record): the records live on the exception.

## Appendix A - K3 (handoff form by path): open owner yes/no, not built

Measured savings (verdict line 90-92, C3): automator 3,686 B, code-critic 3,182 B, strategist 5,576 B; cost one Read of the
form per role. Conditions before any build: (S5) the S8 road - `skills/qa-story/phases/s8.md` 223-224 tells `qa-bug-reporter` to
run `handoff_init.py --stage S8` itself after filing, so its field list would arrive after the work: confirm `start` already
writes that form (then the phase text is a stale second writer, a finding) or K3 STOPs; (S6) the written form has no
required/optional marks (`handoff_init.py` 191, 522) while `handoff_check:field.*` judge "every `required` field": K3 adds the
mark through `handoff_init`'s renderer, or keeps the list. Plain words for the owner: "Each role could read its handover form
from the file the factory writes before it starts, instead of a copy in its prompt: one file read per role, 3-6 thousand
characters saved each. Yes or no?" A yes lowers the KR rows by a later card.

## Reading trail

Read: r1 whole; the verdict whole; `W\scripts\contract_slices.py` 40-190, 225-285, 575-749, 790-869; `W\references\role-load.json`
whole; `W\references\common-rules.md` 60-99, 125-174; `W\references\artifact-contract-plan.md` 105-156;
`W\scripts\role_cli.py` 1-219; `W\scripts\import_test_receipt.py` 245-304; `W\scripts\execution_request.py` 28-39;
`W\scripts\detector_verdict.py` 90-224; `W\scripts\stage_joints.py` 581-608 (and its imports); `W\scripts\handoff.py` 315-389;
`W\handoffs\index.yaml` whole; `W\scripts\handoff_check.py` 1650-1794; `W\references\stage-joints.json` 1104-1111, 2816-2930,
5305-5500; `W\scripts\controller.py` 6912-6949; `W\scripts\role_load.py` 140-159, 262-354; `W\scripts\audit_factory.py`
1205-1256; `W\scripts\red_sandbox.py` 1288-1301, 1405-1439, 2030-2046; `W\scripts\probe_by_code.py` 2688-2700, 4755-4772,
8352-8361 and the `told_fields` hits; `W\scripts\tests\test_contract_slices.py` 312-375, 820-1060;
`W\scripts\tests\test_judgment_census.py` 368-435; `W\scripts\slow_tests.json` whole; `W\references\inject-map.json` 20-84;
`plans/builder-rules.md` 7b (grep); worktree S-2 report (grep).
Grep (with positive controls): `<!--\s*roles:\s*-->` over the package (hits common-rules 130/167, execution-lifecycle,
vocabularies: the empty marker is an existing form); "final message IS the digest" (source 78 + 12 slices, no test);
the narrowed row ids over `scripts/tests` (no test pin; control: `EG-digest-form` found in test-layers.json 4617);
`COMMON_LAYER_CAP_BYTES` (audit_factory 1223, test_audit_rules 764); `native_headroom|46008` over the package (role-load.json,
role_load.py, contract_slices.py 866, test_contract_slices.py, a changelog fragment, census 949: no other K10 carrier);
census `handoff_check.py` units (no null-outcome unit; `tried_errors` already 10 roles; `check_findings` 12 + conductor);
keep rows in test-layers.json for the seven test files (all before `quarantine` at 7169); `t1rs_sites_after_the_probe`.
A Glob miss: `docs/tasks/specs/reports/*t1r-sites*` in the ROOT checkout found nothing; the same Glob in the worktree found the
three reports (they live on the branch only) - no claim rests on the miss.
Not established (stated as edges): the exact ids `probe_by_code` carries at P vs L sites (K1a item 5 builds the table); hence
the code-critic's green after K1b is E(M) under the verdict's assumption (K1b-E7 covers the other world).
Needed beyond the manifest: `W\scripts\handoff_check.py`, `W\scripts\handoff.py`, `W\handoffs\index.yaml`,
`W\scripts\controller.py`, `W\scripts\audit_factory.py`, `W\scripts\red_sandbox.py`, `W\scripts\probe_by_code.py`,
`W\scripts\detector_verdict.py`, `W\scripts\import_test_receipt.py`, `W\scripts\execution_request.py`,
`W\scripts\tests\test_judgment_census.py`, `W\scripts\tests\test_execution_request.py`, `W\references\inject-map.json`,
`W\design\role-rules.json`, `plans/builder-rules.md`.
