# Told before work: node T1r-pages — the 227 rows reach each role without blowing its context (draft, designer, t-708)

Status: DRAFT for Lead acceptance, revision 2 (folds in the coordinator's two inputs: plan critic t-703 on T1r-cards, findings B1 and
B4, `docs/tasks/specs/reviews/20261114-tbw-t1r-cards-plan-critic.md`; and T1r round 2's measure that `selftest.py --limits` refuses 12
generated pages over the 12,000-byte per-slice cap). Forks are returned (§5) and decided nowhere here. Owner forks are marked
**OWNER** and carry a plain-words question (§5.1). The card (§3) runs on the safest reversible option of every fork: NO ceiling, cap or
baseline raise by default, nothing told less than today's main. Where even that option cannot bring a role under its headroom, the card
STOPS for that role and names the number (§2.3); it never raises by default.

Order of nodes (B4): **T1r (rows, WIP 705837d) -> T1r-pages (this card, on the SAME branch `wip/tbw-t1r`, before any merge) -> one green
merge of the branch -> T1r-cards from main (its own delta only).** No node waits on a later one: T1r-pages owns the K8/K10/limits doors
(`inject-map.json`, `role-load.json`, the partition) that T1r lacked; T1r-cards starts from a green main.

Parents: `docs/tasks/specs/20261113-told-before-work-mechanism-spec.md` ("parent": §2.0 survivor, §2.6, §2.6a K8, §2.6b K10,
Appendix A); `docs/tasks/specs/20261114-told-before-work-t1r-t2-dispatch-spec.md` ("dispatch": §2, §8, Lead decisions F-3 (b),
F-8 (a)); `docs/tasks/specs/20261114-told-before-work-t1r-cards-spec.md` ("cards"); the T1r report
`.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-t1r-report.md` ("report"); the T3a report (same folder); the cards plan
critic ("critic").
Read base: worktree `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r` at WIP `705837d` (read only). `W` = its `ai-packages\qa-factory`.

---

## §0 Facts read on the carrier (load-bearing)

| # | fact | carrier |
|---|---|---|
| F1 | The key page tells a role every row of `rows_for(role, <all stages of the role>, None)`: capability-only rows first, then one block per dispatch group (`plan`, `window`, `manual`, `first_look`, `not_first_look`, `walk`). `dispatch=None` = every group: the page is per ROLE, not per dispatch | `W\scripts\contract_slices.py` 637-660 (`_told_units`), 589-590 (`GROUPS`) |
| F2 | Every listed key page (page 1 and every `handoff-keys-<n>.md`) is an inline subject: injected whole into every dispatch of the role, never named instead, never cut by a `kinds` row. A split lowers no load | `contract_slices.py` 71-77, 89; `W\scripts\inject_context.py` 164-179, 244-289 |
| F3 | `inject_context` knows only the dispatch KIND (`first` / `repair` / `rework`); `entries_for` returns the same list for every kind; no dispatch-group fact reaches the injection | `inject_context.py` 137-161 |
| F4 | K10: `U` = bytes of layers charter + injection_common + injection_role of `static_load(role, "first")`; `H` = 100000 - 26000 x P - `allowances.packet` (5400) - 200; red when `U > H` and `U` > the role's `native_headroom` baseline. H is the room under the Codex ceiling with worst-case project files: over H = crosses the ceiling in the worst case (critic B1; `native_context.py:174` `if len(context) > 100000`) | `W\scripts\role_load.py` 296-346 |
| F5 | Baselines today: `native_headroom` = {qa-test-strategist: 46008} (set by T3a equal to the strategist's measured U then: ANY growth of that role's plugin text is over it); `process_ratchet_tokens` (slack 0) / `ratchet_tokens` (slack 1000) are the T3a measures | `W\references\role-load.json` 9-40; T3a report §2 |
| F6 | P (project entries): qa-requirements-tester 2, qa-test-strategist 2; qa-automator, qa-code-critic, qa-runner, qa-failure-analyst, qa-scout 1; case-designer, case-critic, bug-reporter, doc-scribe, retro-analyst 0. H = 42400 / 68400 / 94400 | `W\references\inject-map.json` 19-121 |
| F7 | A `requirement_from: role-commands.json` row renders the command's whole card (`input` + `"; how to prove it: "` + `verify`) | `W\scripts\stage_joints.py` 562-567 |
| F8 | `role_cli.refuse` prints the SAME card on every refusal of the command, and skips the row's expected/door when the record's check is the command's own `role_cli:<command>` row; `RefusingParser.error` refuses through it; `epilog(script)` is the `--help` text | `W\scripts\role_cli.py` 64-71, 79-104, 121-130 |
| F9 | The brief's `## Commands` is a per-role tooling card naming these commands; the brief reaches the role as a PATH | `W\scripts\brief_pack.py` 139-151, 4544; parent fact 0.5 |
| F10 | `exit_gate:EG-digest-form` and `exit_gate:digest` render the same ~820-character sentence on every page | runner page lines 79, 134; automator 69, 126 |
| F11 | `row_for` falls back only to `<stem>:*`, never `<id>.<part>` -> `<id>` | `stage_joints.py` 460-471 |
| F12 | K5 counts only rows that STATE a requirement, unioned per unit; a sentence-less row whose leg is the role's key page is not counted | `W\scripts\tests\test_stage_joints.py` 744-769, 835-837 |
| F13 | Runner page: 24 `role_cli` lines (walk_session 10, manual_evidence 7, manual_capture 3, first_look 2, reference_snapshot 1, execution_fingerprint 1; the report counts 22 rows: N-1), 20 PT, 21 handoff_check, 6 HA, 8 SG, 13 execution_request, 4 run_suite, 6 validate_artifacts, 11 first_look (group), 3 exit_gate, the card | runner page 79-196 |
| F14 | Automator page: 22 PT, 19 handoff_check, 6 HA, 8 SG, 3 exit_gate, 23 execution_request (10 `validate_request` rows with one door), 12+1 manifest_put, 8+4 s5_precheck, 6 run_suite, 5 validate_artifacts, 3 role_cli, 3 plan-group, the card | automator page 69-200 |
| F15 | Analyst page: same universal block, 14 execution_request, 1 run_suite, 11 role_cli, 2 validate_artifacts | Grep on `...\qa-failure-analyst\handoff-keys.md` 62-147 |
| F16 | Four HA rows say "On Codex, ..." | runner page 122-125 |
| F17 | `selftest.py --limits`: `REFERENCE_MD_MAX_BYTES = 12_000`, applied to EVERY `references/slices/**/*.md` (key pages included), message "a generated slice: move the section to the roles that act on it"; its comment: "a reference is INJECTED: it bounds what one role is handed ... The total a role pays is still A22's business". K8's W (20800 chars) and L (26000) judge the same file | `W\scripts\selftest.py` 355-403; `contract_slices.py` 598-602, 765-775 |
| F18 | T2 is merged: `hooklib.block` / `stage_guard.deny` / `role_cli.refuse` print a Record's expected and door; guard (PT/SG/HA) sites print their own FR-1 text today and are switched to `refusal(...)` by T4 (unsited until then: report §2) | dispatch spec §0.1/§3; report §2 |

---

## §1 Architecture invariants, owners, census class (rule 10, AR-29, P27)

| AR | how this node keeps it | change check written into the DoD |
|---|---|---|
| AR-10 a check's requirement reaches the role before the work | every row that judges the role's OUTPUT stays on an injected page; a row that refuses a tool call or a command call BEFORE any effect is told at the call by its refusal (F8, F18) and named on the page by one index line per family (F-2 (b), default) | `stage_joints.py --check` green (K2 with the call leg); rows `T1rp/index-line/<family>`, `T1rp/no-row-lost/<role>` |
| AR-11 only the context the work needs | duplicate digest sentence, 33 command cards and the pre-action guard rows leave the native load; no row leaves the registry | K10 per role before/after in the report |
| AR-12 friction / cost | U and process tokens fall per role (§2.3) | report table |
| AR-13 one reader, one composer | `told_text` stays THE composer; the command branch reads the registry through `role_cli.entry`; the slice cap is ONE constant read by both `selftest` and the partition | AR-13 grep of parent §1.1; grep `12_000\|12000` over `scripts/*.py` finds one literal |
| AR-15 one survivor | the page stays the one told carrier for output checks; the refusal (one transport per kind) for call checks; one rule decides which, by data | test rows of §3.2 |
| AR-20 shrink-only ratchets | ratchets move only DOWN by default; a raise exists only under an owner answer (F-2 (a)) and is named | ratchet rows in the report |
| AR-22 / AR-23 | an empty continuation page says so; a family index line names its count | existing T3a rows (e); `T1rp/index-line/*` |
| AR-28 an unknown never a pass | a command with no card renders the defect text; a call-told row whose family is not in the closed list stays red under K2 | `T1rp/call-leg/family-not-listed-red` |
| AR-29 code judges data | which rows are told at the call is a closed data list (families), J1 judges membership; no meaning check in code | critic question 11 |
| AR-1 closed variety in data | the call-told families are a list in `stage-joints.json`, never a name list in code | `T1rp/call-leg/*` |

Checks this node adds or alters — owner served and census class:

| check / function | change | owner it serves | census class |
|---|---|---|---|
| `stage_joints._carrier_expected` (command branch) | renders a pointer sentence instead of the card | data | renderer, no unit |
| `stage_joints._told_leg` (K2) | accepts a producer told item `{"call": true}` only when the row's family (`<stem>`) is in `call_told_families` and the row states a requirement | data (join row ↔ closed list) | existing unit, xref; no new unit |
| `contract_slices._told_units` / `requirement_section` | page skips call-told rows; adds one index line per call-told family; partition width = the stricter of K8's W and the slice cap | data (shape) | existing units |
| K5 `told_unit_rows` / `k5_problems` (test side) | counts a sentence-less row with the role's key-page leg, and a call-told row | data (join) | xref, test only |
| `selftest.cmd_limits` | reads the cap from the one constant (no value change) | data | unchanged |
| `judgment-census.json` roles of the F-5 PT units | narrowed by the guard-order rule, with a `note` | data (label fix) | no new unit |

Judgment: none moved into code. Whether call-time telling is enough for a pre-action check, and whether a pointer is enough for a
command card, is the OWNER's (F-1, F-2); membership of a family in the call-told list is J1's.

One road (P31): one rule for every role and row — output checks on the page, pre-action checks at the call with an index line —
decided by a data list of families, never by role, language or project.

---

## §2 The picture and the design

### §2.1 Measured picture per role (report §3; no shell in this pass — derived numbers labelled)

`U` plugin share after T1r (bytes), `H` headroom, `S` page 1 chars, `R` row chars for the role, `C` role_cli chars, `U0 = U - R`
(estimate of the pre-T1r share; N-2).

| role | P | H | U | over H | S (L 26000, W 20800, cap 12000 B) | rows / chars | role_cli | U0 est. |
|---|---|---|---|---|---|---|---|---|
| qa-runner | 1 | 68400 | 90414 | +22014 | 53086 red | 111 / 46200 | 22 / 23663 | 44214 |
| qa-automator | 1 | 68400 | 95217 | +26817 (crosses with NO project: 95217+5600 > 100000) | 41365 red | 122 / 35106 | 3 / 3378 | 60111 |
| qa-failure-analyst | 1 | 68400 | 86333 | +17933 | 38751 red | 86 / 32624 | 11 / 11821 | 53709 |
| qa-code-critic | 1 | 68400 | 83044 | +14644 | 27878 red | 79 / 22610 | 1 / 855 | 60434 |
| qa-test-strategist | 2 | 42400 | 60744 (baseline 46008) | +18344 | 22771 WARN | 63 / 14662 | 0 | 46082 (= baseline) |
| qa-requirements-tester | 2 | 42400 | 47004 | +4604 | 23205 WARN | N-1 | N-1 | <= 42400 (T3a) |
| qa-bug-reporter / qa-doc-scribe / qa-scout | 0/0/1 | 94400/94400/68400 | not over | — | 21498 / 21107 / 21174 WARN | — | — | — |
| case-designer, case-critic, retro-analyst | 0 | 94400 | not over | — | under W, but over the 12000-byte cap (F17: all 12 pages are over it) | — | — | — |

By family (from line lengths of the two pages read whole, ±10 %; N-3 replaces them):

| family | runner | automator | analyst est. | told where today on main |
|---|---|---|---|---|
| pre-action guards: 20-22 PT, 8 SG, 6 HA | ≈ 8200 | ≈ 8500 | ≈ 8200 | the guard's own refusal text (FR-1) |
| exit_gate (3, incl. the 820 duplicate) + handoff_check (19-21) | ≈ 4900 | ≈ 5100 | ≈ 5100 | page Outputs/Handoff form + the refusal |
| execution_request (call refusals of `--mine` / `--request`) | ≈ 5200 | ≈ 8500 | ≈ 5600 | the refusal |
| role_cli (command cards) | 23663 | 3378 | 11821 | `--help` and every refusal (F8) |
| run_suite / manifest_put (command call refusals) | ≈ 1000 | ≈ 3900 | ≈ 300 | the refusal |
| output checks: validate_artifacts, s5_precheck, first_look put, plan group, check families | ≈ 1800 | ≈ 5000 | ≈ 600 | the card / prose |

Every one of these roles runs ONE stage: a stage filter separates nothing; the separable dimensions are the dispatch group and the
moment of the check (before the work vs at the call).

### §2.2 The levers, each measured

**(a) Filter by what a dispatch can meet.** As a stage filter: 0 for every role. As a dispatch-group injection (new road: page per
group, injected only when the group holds; K10 counts `base + max over legal group combinations`): at the WORST dispatch ≈ 1000 for
the automator, ≈ 14000 for the runner only if full command cards stay (≈ 3000 with pointers). Needs `inject_context.entries_for`,
`role_load.static_load` worst case, pages by group, a facts function (T3b's `dispatch_groups`). Not tonight (F-3).

**(b) The 33 role_cli rows.** b1 keep the card: 0. b2 pointer line (≈ 230 chars): runner -18603, analyst -9291, automator -2688,
code-critic -625. b3 input only: ≈ -5000 / -2600 / -700 / -200. b4 cards on group pages (needs a). Under the default (§2.3) the
command rows are call-told (lever f), which makes b2 the text of their family index line instead of 33 lines: runner -23400,
analyst -11600, automator -3200, code-critic -700. Risk: the input fields of a command reach the role at `--help` or its first refusal
(one call), not on the page — more than main (main tells none of these rows), less than T1r WIP. Owner: F-1.

**(c) Sibling families in one sentence** (`handoff_check:field.*`, `null_outcome.*`, the four "On Codex" HA rows, 10 `validate_request`
rows): ≈ 350 + 320 + 200 (+900 automator) per role; distinct ids cannot share a row (F11) without a `row_for` parent fallback in a gate
role. Not tonight (F-7). Under the default, three of these families are call-told anyway.

**(d) Double tellings.** The digest pair (F10): -760 per role. Charter / slice prose a row now states: a judged per-section edit
(F-2 (c)), not a renderer change.

**(e) K5/real conflict, by what is true in the code.** `EG-s5-plan-outputs`: the branch is S5-plan only, so its two roles are true; the
unit's other branch is told to all 12 roles by the sentence-less `exit_gate:required_outputs` row on each key page (`## Outputs`,
"Required at your stop"); K5 must count that leg (0 chars). Widening the row would tell 10 roles a false sentence (+≈ 170 each).
`PT-plan-rewrite`, `PT-plan-md-rewrite`, `PT-manifest-shrink`, `PT-window-file`: census over-label of guard units (parent fact 0.3);
the guard-order rule decides (§3.1 P-6). Under the default these PT rows are call-told; K5 counts call-told rows too (they are told,
at the call), so the per-row census narrowing stays truth-keeping, not size-driven.

**(f) Told at the call for pre-action checks (default of this revision).** A pre-action check refuses a tool call or a command call
BEFORE it has any effect: no work is lost, and the refusal is the in-process transport that, after T2, prints the row's expected and
door (and before T4/T5 sites them, prints the site's own FR-1 text, which is what main tells today). FR-38 speaks of a check that
judges the role's OUTPUT. The rule: a family whose every refusal happens at the call goes into a closed list
`call_told_families` (data, `stage-joints.json`; initial list: `guard_pre_tool`, `stage_guard`, `host_adapter`, `execution_request`,
`run_suite`, `manifest_put`, `role_cli`); its rows carry the told item `{"call": true}`; the page shows one index line per family
(`- [<family>:*] <n> checks of your <tool calls | commands> are told in the refusal of the call, with what they expect and the door;
nothing you have written is lost by them.`), so the role knows they exist. Output families (`exit_gate`, `handoff_check`,
`validate_artifacts`, `s5_precheck`, `first_look`, `planning_contract`, `coverage_contract`, `check_*`, `controller`, `acceptance`,
`branch_accounting`, `critic_rollcall`) stay on the page. Savings per role (sum of the call-told families of §2.1, minus ≈ 150 per index
line): runner ≈ -37300, analyst ≈ -25500, automator ≈ -26300, code-critic ≈ -15500 (est., N-3). Risk: a role learns a guard rule or a
command's input at its first refused call (one turn each); `manifest_put` and `role_cli` refusals come after the role has WRITTEN an
input file — the file is not lost, but writing it is work: J1 judges whether those two families belong to the list (F-2 sub-question).
This reverses the parent's road-(a) page telling and the critic's alternative F-4 (b) "narrow `*` rows behind capability tokens" is a
weaker form of it (capability tokens do not remove a row from a role that has the capability).

**(g) The two size limits of one page (F17).** K8 (W 20800 chars, L 26000 = `MAX_BLOCK_CHARS`, a run ceiling) and the per-slice cap
(12000 bytes, a dev-time proxy for "what one role is handed") judge the same generated file. Since key pages are inline and every
listed page is injected (F2), a split at 12000 lowers no load: for a key page the cap measures nothing about cost that K10/A22 do not
already measure, and the per-file run danger is `MAX_BLOCK_CHARS`. Meeting both today: partition width = min(W, 12000 bytes) — more
pages (≈ +450 bytes each to U), no cap raise. Which limit is wrong for key pages: F-10.

**(h) Appendix A at the source (OWNER).** `H` assumes every `project:` entry at 26000; a run-time move delivering project files over a
share by path would let `H` count the real share.

### §2.3 Default set and expected numbers

Default (card §3; no raise, nothing less than main): **(f) call-told families + (b2) as the role_cli index text + (d) digest once +
(e) K5 truth + (g) split at min(W, 12000 B).** A role still over H after it: the card STOPS for that role (P-8) and the residual goes to
the owner (F-2 options (c), (d), or a named raise (a)).

Formula: `U' = U - Σ_call-told rows len_bytes(line) + Σ_families len_bytes(index line) - 760 + 450 x (pages added)`; pages
added = `ceil(page bytes / 12000) - 1` after the cut. Room on Codex with an empty project = `94400 - U'`.

| role | U | U' est. | H (baseline) | over H after | pages est. | K10 verdict on default |
|---|---|---|---|---|---|---|
| qa-runner | 90414 | ≈ 54500 | 68400 | — | 2 | green |
| qa-failure-analyst | 86333 | ≈ 61600 | 68400 | — | 2 | green |
| qa-code-critic | 83044 | ≈ 68400 ±2000 | 68400 | ≈ 0 (edge) | 2-3 | edge: N-3 decides |
| qa-automator | 95217 | ≈ 69500 | 68400 | ≈ +1100 | 2-3 | **STOP** unless the measure is lower (N-2, N-3) |
| qa-test-strategist | 60744 | ≈ 52000 | 42400 (46008) | ≈ +6000 over baseline | 2 | **STOP**: its baseline equals its pre-T1r share (F5), so any output row is a raise |
| qa-requirements-tester | 47004 | ≈ 42000-46000 (no-shell role: few guard rows; N-1) | 42400 | edge | 2 | edge: N-1/N-3 decide |
| bug-reporter, doc-scribe, scout, case-designer, case-critic, retro-analyst | under H | lower by their call-told rows | — | — | 1-2 (cap) | green |

Reading: the default brings the runner and the analyst well under H and removes the automator's Codex crossing with an empty project
(room ≈ 24900 instead of none), but the automator, the strategist (and possibly code-critic, requirements-tester) stay at or over H by
estimate: their OUTPUT rows plus the existing charter/slices exceed the room under the ceiling with worst-case project files. No text
lever that keeps output checks on the page and raises nothing closes that; only F-2 (c) (remove prose the rows now state), F-2 (d)
(Appendix A at the source) or a named raise (a) does. The card therefore finishes every role it can and stops, naming the number, for
the rest; the branch cannot merge green until the owner answers F-2 for those roles (or N-3 measures them under H).

---

## §3 Builder card (dispatch-ready on the default options)

given: this file; parent spec §2.6, §2.6a, §2.6b, Appendix A; dispatch spec §2, §8 with its Lead decisions; the T1r report, the T3a
report, the cards plan critic B1/B4; `W\scripts\stage_joints.py` (`_carrier_expected`, `told_text`, `told_line`, `_told_leg`,
`_page_leg`, `_is_page`, `_demands_leg`, `rows_for`); `W\scripts\contract_slices.py` (`_told_units`, `requirement_section`, `_role_pages`,
`size_limits`, `size_finding`, `keys_findings`, `keys_write`); `W\scripts\selftest.py` (`REFERENCE_MD_MAX_BYTES`, `cmd_limits`);
`W\scripts\role_load.py` (`static_load`, `native_headroom_problems`); `W\scripts\role_cli.py`; `W\scripts\guard_pre_tool.py` (guard order,
read only); `W\references\stage-joints.json`, `inject-map.json`, `role-load.json`, `role-commands.json`; tests `test_stage_joints.py`,
`test_contract_slices.py`, `test_role_load.py`, `test_role_commands.py`, `fixtures\judgment-census.json`; `design/factory-rules.md`
whole; `plans/builder-rules.md`
owns:
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\stage_joints.py (_carrier_expected, _told_leg, _is_page callers only as needed for the call leg; new constant COMMANDS_TEXT)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\contract_slices.py (_told_units, requirement_section, size_limits; new SLICE_MAX_BYTES if the constant moves here per P-5)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\selftest.py (REFERENCE_MD_MAX_BYTES read from the one constant only; no value change)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\stage-joints.json (new top key `call_told_families`, `when_kinds` untouched; producers' `told` of rows of the listed families -> `[{"call": true}]`; row `exit_gate:digest` requirement)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\inject-map.json (continuation page lines only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\role-load.json (ratchet_tokens, process_ratchet_tokens, native_headroom: LOWER only by default)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\slices\ (every handoff-keys*.md and index.md, generated by contract_slices.py --write only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_stage_joints.py (told_unit_rows, k5_problems, told-text/role-commands.json, the 14 pinned rows of report §4 per F-6, new T1rp rows)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_contract_slices.py (new T1rp/* rows only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (`roles` and `note` of plan_write_check, manifest_write_check, window_file_check only, per P-6)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\changelog.d\tbw-t1r-pages.md
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-t1r-pages-report.md
non-goals: `inject_context.py` and any per-dispatch injection (F-3); `role_load.py` code; any raise of `native_headroom`,
`process_ratchet_tokens`, `ratchet_tokens`, `MAX_BLOCK_CHARS`, the 12000 cap or the 100000 mirror (only on an owner answer, F-2 (a) /
F-10); `role-commands.json` text; any row sentence other than `exit_gate:digest`; merging sibling rows (F-7); charter / slice prose
(F-2 (c)); the 12 ahead cards (T1r-cards); refusal text or sites; quarantined tests; a new test file; merging the branch (Lead)
handoff: the branch commit plus the report in owns: per-role table of §2.3 with MEASURED U, U', H, page bytes/chars, page count, room;
per-role per-family chars (N-3); the call-told rows per role; ratchet rows (key, old -> new, reason); the STOP list (role, U', H, gap);
the guard order per P-6 unit; FR walk; verbatim witness
edges: §3.3 (each with its invariant)
siblings: `role_cli.epilog` / `refuse` (the card's printers); `hooklib.block` / `stage_guard.deny` (the call transports, T2); T4/T5/T5b
(siting the call-told rows: their refusals then print the row); `brief_pack` `## Commands` (T3b twin, untouched); `contract_slices.catalogue`
(T3a sibling); `selftest.cmd_limits` (the second size limit, F-10); T1r-cards (§4); SIBLING_MAP axis 34 (one road); axis 37 if added by T10
DoD: §3.4 (inline, exact commands)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-t1r-pages-spec.md
architecture: AR-1, AR-10, AR-11, AR-12, AR-13, AR-15, AR-20, AR-22, AR-23, AR-28, AR-29 -- output checks on injected pages, pre-action checks told at the call by a closed family list with an index line; one size constant; ratchets only lowered; K5 counts real legs
judgment: none moved -- the call-told family list is data judged by J1; whether call-time telling suffices is the owner's (F-1, F-2)

Gate: on `wip/tbw-t1r` after T1r's WIP, before any merge (B4). The branch merges only when `contract_slices.py --check` and
`selftest.py --limits` are clean — i.e. after the STOP list is empty by measure or by the owner's answer to F-2.

### §3.1 Items

| item | what | expected behaviour | test |
|---|---|---|---|
| P-0 | Measure before | verbatim: `stage_joints.py --check`; `contract_slices.py --check`; `selftest.py --limits`; per role `static_load(role, "first")` U and process tokens; per role per family chars (N-3) | report §before |
| P-1 | `--help` fact | for every role-commands key: Grep `epilog(` in its script. All present -> the index line and COMMANDS_TEXT carry the `--help` clause; any absent -> left out for every command, list reported | report table |
| P-2 | Pointer rendering | `_carrier_expected` command branch: no entry -> unchanged defect why; empty `input` and `verify` -> why `command `<key>` has no card`; else COMMANDS_TEXT = "`{command}` checks its input against its command card (what to write, how to prove it); the card is printed whole in every refusal of the command, and by `{script} --help` before your first call" (clause per P-1). Used by the refusal path's I-S and by any page that still renders a command row | `told-text/role-commands.json` rewritten; `T1rp/role-cli-pointer/absent`, `/empty-card`, `/subcommand` |
| P-3 | Call leg (F-2 (b) default) | `stage-joints.json`: new top key `call_told_families` = the list of §2.2 (f) (add it to `TOP_KEYS`/`_shape_problems` in `stage_joints.py` as needed); every producer `told` of a row whose stem is listed and that states a requirement -> `[{"call": true}]`. `_told_leg`: `{"call": true}` is green only when the row's stem is in the list and the row states a requirement; else red "a call-told row needs its family in call_told_families and a requirement". A call item is not a legacy leg (`_legacy_legs` unchanged count 0) | `T1rp/call-leg/listed-ok`, `/family-not-listed-red`, `/no-requirement-red`, `/legacy-still-0` |
| P-4 | Page: output rows + index lines | `_told_units` skips rows whose every producer item for this role is `{"call": true}`; adds, after the capability rows, one line per call-told family with >= 1 row for the role: `- [<family>:*] <n> checks of your <tool calls|commands> are told in the refusal of the call, with what they expect and the door; nothing you have written is lost by them.` (`tool calls` for guard_pre_tool/stage_guard/host_adapter, `commands` for the others; the role_cli line adds P-2's `--help` clause) | `T1rp/index-line/<family>`; `T1rp/no-row-lost/<role>` = page ids ∪ call-told ids == `rows_for(role, stages, None)` ids |
| P-5 | One size constant; split at both limits (F-10 (a)) | the cap is ONE literal: keep `selftest.REFERENCE_MD_MAX_BYTES` as owner if `import selftest` inside `size_limits` has no side effect, else move it to `contract_slices.SLICE_MAX_BYTES` and `selftest` reads it. `requirement_section` places a row on the current page while `len(text.strip()) <= W` AND `len(text.encode()) <= cap`; K8 messages unchanged | `T1rp/split-at-cap` (fixture: page under W but over cap -> next page); existing T3a (d)/(e) green |
| P-6 | PT one-role rows (F-5) | read the guard order of `guard_pre_tool` for the four PT units; owner check first and refusing every non-owner -> census `roles` of the unit = union of its rows' roles, `note` "guard order: PT-owner refuses every non-owner before this branch (<file>:<line>)"; else widen the row's roles | `K5/real` green; `test_judgment_census.py` green |
| P-7 | Digest once (F-4 (a)) | `exit_gate:digest` requirement = "Your final message has the digest form stated in the row [exit_gate:EG-digest-form] of this section." | `T1rp/digest-once/<role>` |
| P-8 | K5 counts real legs | `told_unit_rows` also takes a sentence-less row whose producer leg for a role is that role's key-page path, and a call-told row; `k5_problems` counts only roles whose expanded path is their own page, or roles of a call-told producer | `K5/key-page-leg-counts`, `K5/other-role-page-not-counted`, `K5/call-told-counts`; `K5/real` green |
| P-9 | Pinned rows (F-6 (a)) | the 14 rows of report §4 updated to the landed data; no assertion weakened | `test_stage_joints.py` green |
| P-10 | Regenerate, split, measure, STOP | `contract_slices.py --write`; add every continuation line K8 or `--limits` asks for (the page that stays over the cap after the partition names its role); re-run until clean; then per role: `U' <= H` (or `<=` its existing baseline) -> lower `native_headroom` / ratchets to the measure where the slack rule says (named); `U' > H` -> NO raise: the role goes on the STOP list (role, U', H, gap) and the node hands back with that list | `contract_slices.py --check`, `selftest.py --limits` |
| P-11 | Changelog | one English ASCII bullet | `selftest.py --lang` |

### §3.2 Test rows (variant rows in keep files; no new file)

| id | file | expected |
|---|---|---|
| `told-text/role-commands.json` (rewritten), `T1rp/role-cli-pointer/absent`, `/empty-card`, `/subcommand`, `T1rp/refusal-keeps-card` | test_stage_joints.py | pointer for a real key; defect text for absent / empty card; script = first token; `refuse` still prints the card's `input` |
| `T1rp/call-leg/listed-ok`, `/family-not-listed-red`, `/no-requirement-red`, `/legacy-still-0` | test_stage_joints.py | §3.1 P-3 |
| `K5/key-page-leg-counts`, `/other-role-page-not-counted`, `/call-told-counts` | test_stage_joints.py | §3.1 P-8 |
| `T1rp/index-line/<family>` | test_contract_slices.py | one line per call-told family with its count; none for a family with 0 rows for the role |
| `T1rp/no-row-lost/<role>` (12) | test_contract_slices.py | page ids ∪ call-told ids == rows_for ids |
| `T1rp/digest-once/<role>` (12) | test_contract_slices.py | the EG-digest-form sentence once |
| `T1rp/pages-listed/<role>` (12) | test_contract_slices.py | listed pages == generated pages; each `< W` chars and `<= cap` bytes |
| `T1rp/split-at-cap` | test_contract_slices.py | fixture: under W, over cap -> two pages |
| K8 AT/BEYOND, K10 AT/BEYOND (T3a (d), (j)) | test_contract_slices.py | unchanged, re-run |

### §3.3 Edges (each with its invariant)

- **K8 AT/BEYOND and the cap AT/BEYOND.** A page at W WARNs, over L red; a page at 12000 bytes passes, 12001 is refused by `--limits`; the
  partition keeps both. Invariant: no row cut or dropped; every page-told row on a listed page (`no-row-lost`).
- **K10 AT/BEYOND.** `U' = H` green; `U' > H` and over the baseline red -> STOP list, no raise. Invariant: no unnamed raise, no raise without
  the owner; no role left crossing the ceiling with an empty project silently (the STOP list names it).
- **One row bigger than the stricter width.** Red "one row is over the split threshold: shorten the sentence" (J1). Invariant: no truncation.
- **A role with zero page rows but call-told rows.** Its section holds only index lines (not the `none` line, which would under-tell).
  A role with neither: `NONE_ROLE`. A listed page with no row: `NONE_CONTINUED`. Invariant: every empty outcome is stated.
- **A row with no stage.** Red at `_row_problems`; on no page and not counted as call-told. Invariant: refused at dev time.
- **A continuation page nobody names / listed pages not consecutive.** Existing deletion + red / gap red. Invariant: no stale page injected.
- **A call-told row whose site is not yet sited (T4/T5 pending, `unsited`).** Its refusal prints the site's own FR-1 text (main's telling)
  until the siting node switches it to `refusal(...)`. Invariant: the role is never told less than on main; the row is counted unsited.
- **A family wrongly in the list** (its refusal comes after work). J1 removes it; the row returns to the page in the same diff. Invariant:
  an output check is never call-told by code's own decision.
- **Command with no card / empty card.** Defect text. Invariant: no pointer to a card that does not exist (AR-28).
- **TEMPORAL — story mid-run whose brief was built before the split.** The brief (a path) is untouched; each dispatch reads inject-map.json
  and all pages of one installed generation in one `collect_blocks` call (B-014). Invariant: no dispatch mixes generations; no row is in
  neither carrier (page or call).
- **TEMPORAL — continuation lines and `call_told_families` absent before, present after.** Created by this node's commit with the files;
  a line without its file is red "missing - run --write"; an older reader sees an unknown top key -> `_shape_problems` red (one generation
  per install). Invariant: never a half state shipped.
- **Error direction of reused functions in new roles.** `_told_leg` (gate): may err toward red (a call item refused), never toward green for
  an unlisted family or a sentence-less row; adversarial: stem spelled with a different case, a `<stem>:*` row, a row mixing page and call
  items for different roles (each item judged for its role). `_told_units` (page renderer): may err toward MORE text (a row on the page and
  in an index count), never toward a row in neither. `told_unit_rows` (K5): may err toward not counting; adversarial: another role's page
  path, `<role>` placeholder, anchor absent, call item on an unlisted family. `_carrier_expected`: defect text over pointer when in doubt.

### §3.4 DoD (narrow; no CI, no mutation pass — PROJECT.md «Командная работа» п. 13)

Acceptance keys: (1) `contract_slices.py --check` clean (no K8 WARN/red, K10 green) or the STOP list in the report for exactly the roles
K10 names; (2) `selftest.py --limits --lang` green (no slice over the cap); (3) `stage_joints.py --check` clean; (4) `test_stage_joints.py`
green once; (5) every T1rp row green; (6) no raise in role-load.json; (7) the §2.3 table measured.

Commands (from `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r`):
1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/stage_joints.py ai-packages/qa-factory/scripts/contract_slices.py ai-packages/qa-factory/scripts/selftest.py ai-packages/qa-factory/references/stage-joints.json ai-packages/qa-factory/references/inject-map.json ai-packages/qa-factory/references/role-load.json` — every non-slow file it lists, each alone.
2. `python -B ai-packages/qa-factory/scripts/contract_slices.py --write` then `--check`
3. `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
4. `python -B ai-packages/qa-factory/scripts/stage_joints.py --check`
5. `python -B ai-packages/qa-factory/scripts/role_rules.py --check`
6. `test_contract_slices.py`, `test_role_load.py`, `test_role_commands.py`, `test_judgment_census.py` (each alone, `python -B <path>`)
7. audit A22 as T3a ran it (pure read of `audit_factory._a22_findings(PLUGIN_ROOT, require_settings=True)`), output pasted
8. `python -B ai-packages/qa-factory/scripts/tests/test_stage_joints.py` — ONCE (about 180 s), last.

census: no new blocking unit.

---

## §4 Order, and what T1r-cards must change

- Order (B4): T1r WIP -> T1r-pages on the same branch -> one merge when green -> T1r-cards from main. T1r-cards waits only on an EARLIER
  node.
- Cards §0.2 A4/A7 are false: pages are regenerated and split here; cards measures its "before" on the merged tree. Its F-4 (named raise)
  is replaced by: "K10 green on entry; this node's own growth per role is at most the room left (H - U' of this node's report), else STOP"
  (critic B1 fix).
- The cards' growth is near size-neutral (the card text is already on every page under `### Not yet in rows`, critic B1), plus the 4
  held-out rows (≈ +1.5K automator) — which may not fit the automator's room: measured, never raised by default.
- Cards M1 appends to rows of OUTPUT families only (validate_artifacts, s5_precheck, exit_gate, ...); a segment whose target is a call-told
  row (e.g. `manifest_put:expectation_changes`, ck-3 / ck-4; `guard_pre_tool:PT-external-writes`, br-3) lands by M3 on an output row or a
  sub-id with `{"page": true}` — never into a call-told row (the page would not show it).
- The fragile one-page roles split by the cap anyway; role-rules re-points target `handoff-keys-<n>.md` where `--write` puts the row.
- Owns overlap (stage-joints.json, inject-map.json, role-load.json, slices, test_contract_slices.py, test_stage_joints.py): strictly after.

---

## §5 Forks (returned, not decided)

- **F-1 (OWNER) How a role is told a command's input.** (a) whole card on the page (runner +23.7K, analyst +11.8K); (b) pointer / call-told
  index line, the card whole at `--help` and every refusal; (c) input only; (d) whole cards on dispatch-group pages (needs F-3). Recommend (b).
  Card follows (b).
- **F-2 (OWNER) Pre-action checks and the residual over H.** (a) named raises = measured U (crosses the ceiling in the worst case: critic B1);
  (b) pre-action families told at the call with an index line (default; sub-question: do `manifest_put` and `role_cli`, whose refusal comes
  after an input file is written, belong to the list?); (c) a designer pass removing charter/slice prose the rows now state, per role,
  measured; (d) Appendix A at the source (project files over a share by path; H counts the real share). Recommend (b) now, then (c) for the
  automator and the strategist (and code-critic / requirements-tester if N-3 shows them over), (d) as the owner's longer answer; (a) never
  by default. Card follows (b) and STOPs per role on the rest.
- **F-3 (Lead) Dispatch-group injection.** (a) later node after T3b's `dispatch_groups`; (b) tonight. Recommend (a). Card: none.
- **F-4 (Lead) Which digest row keeps the sentence.** (a) EG-digest-form keeps it, `exit_gate:digest` points (card); (b) reverse; (c)
  sentence-less key-page path (red risk under T1r-3). Recommend (a).
- **F-5 (Lead) K5/real.** (a) K5 counts key-page and call legs + the guard-order census rule for the PT one-role rows; (b) a `*` sentence on
  `exit_gate:required_outputs` (+≈ 150/role); (c) widen `EG-s5-plan-outputs` (false for 10 roles). Recommend (a). T4 later merges the census.
- **F-6 (Lead) The 14 pinned rows.** (a) this node; (b) another node. Recommend (a): the branch cannot merge red.
- **F-7 (Lead) Sibling families in one row.** (a) not tonight; (b) do it. Recommend (a).
- **F-8 (Lead) `--help` clause.** (a) only when every script wires `epilog`, else for none; (b) per command. Recommend (a).
- **F-9 (Lead) "On Codex" HA rows on Claude pages.** Moot under F-2 (b) (host_adapter is call-told); otherwise (a) keep.
- **F-10 (Lead) Two size limits on one generated key page (12000-byte cap vs K8 W/L).** (a) meet both now: partition at the stricter (card;
  more pages, ≈ +450 bytes of U each, no raise); (b) exempt `handoff-keys*.md` from the 12000 cap in `cmd_limits` — the cap's own comment
  says it bounds what one role is handed, but an inline key page is handed whole however it is split (F2), so for key pages the cap measures
  nothing K10/A22 do not, and costs U per extra page; the run danger per file is `MAX_BLOCK_CHARS`, which K8 already holds; (c) drop K8's W
  in favour of the cap. Recommend (a) tonight and (b) as the Lead's correction (the cap is the wrong limit for an inline generated page; it is
  the right one for a slice a source section feeds). Not an owner fork: no telling/cost trade, a dev-time proxy.

### §5.1 Owner questions (plain words, for the morning)

**F-1.** The runner and the analyst use many factory commands. Each command has a "card" saying what file to write. Tonight's rows put
every full card on the role's page — about 24,000 extra characters for the runner on every start, even when it uses two commands. I
propose one line saying these commands check their input and print the full card with `--help` and with every refusal; the role sees a
card at most one call later. Or keep the full cards, only in the dispatches that use them (a bigger change, later). Which do you want?

**F-2.** The new rows made several roles too big for the Codex limit; the automator now crosses it in every project, so on Codex it
would refuse to start. My default for tonight: the rules that refuse a tool call or a command BEFORE anything is done (like "never change
git config", "run tests only through run_suite", the command input checks) are no longer copied onto the page; the role is told each one
by the refusal at the moment it tries, and the page keeps one line per group saying these rules exist. Rules that judge the role's
finished work stay on the page. This fixes the runner and the analyst and removes the "crosses in every project" problem, but the
automator and the strategist still stay a little over the room left when project files are at their largest. For those two: (1) a
careful pass removing from their role texts what the new rows now say, or (2) on Codex, hand big project files by path instead of pasting
them, or (3) accept a raise knowing Codex may refuse them on a big project. Do you agree with the default, and which of the three for the
remaining two?

---

## §6 Small choices closed by the designer

- S-1 Report `20261114-t1r-pages-report.md`; changelog `tbw-t1r-pages.md`; test prefix `T1rp/`.
- S-2 Pointer, index-line and digest-pointer wordings (P-2, P-4, P-7).
- S-3 STOP instead of raise; `94400` (= 100000 - 5400 - 200) as the "crosses with an empty project" figure in the report.
- S-4 Continuation overhead 450 bytes in the formula (estimate; the measure replaces it).
- S-5 Index line uses the existing `<stem>:*` id form for its bracket (no new id; it is not a row and has no refusal).

## §7 Reading trail

- Repo root: mechanism spec 1-120, 120-359, 360-409, 686-715; dispatch spec 1-210, 296-345; cards spec whole; cards plan critic Grep `B1|B4`
  and 21-50.
- tbw-t1r: T1r report whole; T3a report whole; `inject-map.json` whole; `role-load.json` whole; runner and automator `handoff-keys.md` whole;
  analyst page by Grep `^- \[[a-z_]+:[^\]]*\]` (62-147); `contract_slices.py` def Grep and 465-943; `role_load.py` 255-354, 440-597;
  `inject_context.py` def Grep and 137-296; `stage_joints.py` def Grep and 276-605; `role_cli.py` 1-180; `test_stage_joints.py` Grep `K5` and
  700-840; `brief_pack.py` Grep and 120-179; `agents/qa-runner.md` Grep (54, 61, 62); `walk-charter.md` Grep (12, 17, 19); runner
  `common-rules.md` term count 14; `selftest.py` Grep `12000|12_000|SLICE_MAX|slice.*cap` (20, 358, 387) and 350-409.
- Controls: a Glob under the worktree and a Grep with a slash brace glob returned nothing (miscalls); the same files were then read by absolute
  path / Grep per file (positive control: `agents/qa-runner.md` count 3). No negative claim of this draft rests on an empty search.

## §8 What I did NOT establish (builder measures before the design is confirmed)

- N-1 Exact role_cli counts per role (runner page 24 lines vs report 22); the requirements-tester's rows by family and whether it has a shell.
- N-2 U0 per role on T1r's parent commit (the table uses `U - R`).
- N-3 Per role per family bytes: a `python -B -c` pure read over `contract_slices.handoff_keys_pages(PLUGIN, role)` summing
  `len(line.encode()) + 1` per `^- \[(\w+):` family — decides the STOP list (automator, strategist, code-critic, requirements-tester are within
  the estimate's error of H).
- N-4 That both digest rows name all 12 roles.
- N-5 Whether every command script wires `role_cli.epilog` (P-1).
- N-6 The guard order for the four PT units (P-6).
- N-7 Whether `import selftest` inside `contract_slices.size_limits` is side-effect free (P-5).
- N-8 Real page counts and U' after `--write` (the 450-byte overhead too).
- N-9 Whether every refusal of `manifest_put` and `role_cli` comes before or after the role's input file is written (F-2 sub-question; J1).
- N-10 Whether A22 runs in CI (T3a open question); the size of real projects' `framework-rules.md` (the automator's real Codex margin).

## §9 Lead decisions on the forks (14.11.2026, owner away — by recommendation, until the owner's word; listed in the morning report)

- **F-1 (b)** and **F-2 (b)** — taken as the default the card already follows, "по рекомендации, до слова владельца". Why this is
  the safest reversible option: every row stays in `stage-joints.json` with its sentence; only WHERE it is told moves (page -> the
  call, with an index line on the page), so the owner's "whole card / whole rule on the page" is one data edit back
  (`call_told_families`). Nothing is told less than on main today (main tells these checks only by the refusal). No raise of any
  ceiling, cap or ratchet. The F-2 sub-question: `manifest_put` and `role_cli` join the call-told list ONLY if N-9 shows their
  refusal comes before any effect on the role's work; otherwise they stay on the page.
- Residual roles over H after the default (automator, strategist, maybe code-critic / requirements-tester): the builder STOPS per
  role with the measured gap; the next node is F-2 (c) — a designer pass removing charter/slice prose the rows now state. (d) and
  (a) wait for the owner. The branch does not merge while a role is over H.
- **F-3 (a), F-4 (a), F-5 (a), F-6 (a), F-7 (a), F-8 (a), F-9 moot, F-10 (a)** now; F-10 (b) (exempt generated key pages from the
  12000-byte cap) is queued as a Lead node — it changes a limit, so it gets its own four questions.
- Order (critic t-703 B4, road (a)): T1r WIP -> T1r-pages on `wip/tbw-t1r` -> merge when green -> T1r-cards redraft from main.
- Plan critic before the builder (new idea of the owner, a spec that changes where a requirement is told).

## §10 Lead amendments after the plan critic (t-716, `docs/tasks/specs/reviews/20261114-tbw-t1r-pages-plan-critic.md`) — BINDING over §3 and §9

Where §3, §8 or §9 disagree with this section, this section wins. The verdict's findings B1-B4 and N1-N9 are given to the builder.

- **P-(-1) first (B4).** Merge `origin/main` into `wip/tbw-t1r` before anything else; `references/role-load.json` conflicts are
  resolved by taking main's rows; then `contract_slices.py --write`; then P-0. Every number in the report is measured on that tree.
- **A22 ratchets (B1).** `ratchet_tokens` and `process_ratchet_tokens` are COST budgets: after this node's default every row is set
  to the measure — lowered where it fell, a NAMED raise where it grew (key, old -> new, reason "told-before-work output rows, tbw"),
  each row listed in the report and in the commit message (AR-20, SIBLING_MAP axis 18; the critic of the merge names them).
  `native_headroom` (K10, the run-failure ceiling) stays NO-RAISE and alone drives the STOP list. A22 green
  (`test_role_load.py`) joins the acceptance keys. This replaces the non-goal "any raise of ... `process_ratchet_tokens`,
  `ratchet_tokens`" and §3.4 key (6). Lead decision under AR-20; the numbers go to the owner's morning list.
- **The call list (B2).** (1) `manifest_put` is OFF `call_told_families`: its rows stay on the page. (2) `role_cli` stays on the
  list; its index line is an instruction before writing: "run `<script> --help` before you write an input file; it prints what each
  command checks" — P-1 verifies that every role_cli script passes `epilog` to its parser; a script that does not keeps its card on
  the page. (3) Per-producer split: the five manifest-row `execution_request` rows (`no_test`, `selector_args`, `place_rows`,
  `profile`, `case_entries`) and `stage_guard:SG-command.commit.manifest` and `SG-command.delivery` stay PAGE-told for the role
  whose finished work they judge (qa-automator; the delivery form's role), call-told for the others. The `--request` file rows of
  `execution_request` stay call-told only if their index line names the `--template request` door. (4) The sentence "nothing you
  have written is lost by them" is printed only for `guard_pre_tool`, `host_adapter`, `stage_guard` index lines. (5) K2/K5 accept a
  call item only for a row whose refusal is sited on a T2 transport; an unsited or direct-print row stays in
  `told_ratchet.unsited` and is not counted told by K5 (N5). N-9 and §9's condition on it are deleted: nothing here is left to
  measure-and-decide by the builder.
- **Reversibility (B3).** P-3 does NOT replace a producer's `told`: it keeps the existing page item and ADDS the call marker on it
  (`{"page": true, "call": true}` or the equivalent on the existing item shape). The call marker is honoured only while the row's
  family is in `call_told_families`; a family removed from the list returns its rows to the page with K2 green. Test row: remove one
  family in a scratch copy -> its rows render on the page and `--check` K2 is green.
- **Text fixes** N1, N2, N3, N7, N9 as written in the verdict. **N4**: the report carries "call-told rows per role and the expected
  first-meet refusals (one per family a role calls)"; a `live-runs` row is owed by the Lead. **N6**: the commit message carries the
  four-questions block for `call_told_families` with one labelled line per SIBLING_MAP axis; the Lead supplies the block at
  acceptance (the builder hands the mechanism files over, the Lead commits them — tier line). **N8**: the strategist's STOP is
  expected; the F-2 (c) node (prose the rows now state) is opened by the Lead in parallel.
- F-10 stays (a) tonight; (b) remains a queued Lead node.
- Owner questions 1 and 2 of the verdict are the plain-words form of F-1 / F-2; tonight's "yes" is undone by removing one list entry
  (true after the B3 fix).
