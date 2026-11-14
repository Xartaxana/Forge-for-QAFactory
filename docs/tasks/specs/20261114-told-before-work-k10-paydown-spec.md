# Told before work: K10 pay-down for qa-automator, qa-code-critic, qa-test-strategist (draft, designer, t-816)

Status: DRAFT for Lead acceptance. Forks are returned (§6), decided nowhere here; the cards (§5) are buildable on the
recommendation of every fork. No raise of `native_headroom`, `MAX_BLOCK_CHARS`, the 12,000-byte cap or the 100000 mirror by
default; a raise appears only as an OWNER question with numbers (§4).

Read base: worktree `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r` (branch `wip/tbw-t1r`, head 8d71532b per the dispatch;
read only). `W` = `W\ai-packages\qa-factory`. Paths in cards are relative to `ai-packages/qa-factory`.

**Limitation stated first (rule 3, FR-41).** This pass had Read/Grep/Glob only - no shell. Every number below is labelled:
**M** = measured by a script and read on its carrier (a report's verbatim witness); **L** = a line count I measured with Grep
(`output_mode: count`, pattern `^`); **E** = my estimate (from line lengths read on the generated pages, or by subtraction of
two M numbers), with its basis. Card K0 (§5.0) replaces every E with a measure before any design is executed.

---

## §0 The numbers to beat (M)

Carrier: `W\..\docs\tasks\specs\reports\20261114-tbw-fix-round-report.md` lines 34-37 and 58 (verbatim `contract_slices.py
--check`), produced by `role_load.native_headroom_problems` (`W\scripts\role_load.py` 302-346): `U` = bytes of layers
`charter` + `injection_common` + `injection_role` of `static_load(role, "first")`; `H` = 100000 - 26000 x P - 5400 - 200; green
when `U <= H` or `U <=` the role's `native_headroom` baseline. Command that prints them (from `W`):
`python -B scripts/contract_slices.py --check` (K10 lines) and `python -B scripts/role_load.py --all --json` (layer bytes).

| role | P | U now (M) | H | baseline | needed to be green | needed to be under H |
|---|---|---|---|---|---|---|
| qa-automator | 1 | 81,385 | 68,400 | none | -12,985 | -12,985 |
| qa-code-critic | 1 | 74,417 | 68,400 | none | -6,017 | -6,017 |
| qa-test-strategist | 2 | 55,976 | 42,400 | 46,008 | -9,968 (to the baseline) | -13,576 |

Note for the Lead: the dispatch says "strategist 55,976 against 42,400". K10 turns green for the strategist at 46,008 (its
existing baseline, `role_load.py` 337-338), not at 42,400. Both targets are carried below; F-1 asks which one the pay-down owes.

---

## §1 Architecture invariants, owners, census class (rule 10, AR-29, P27)

| AR | how the recommended nodes keep it | change check in the DoD |
|---|---|---|
| AR-10 a check's requirement reaches the role before the work | every row that judges a role's OUTPUT stays on its page; a row moves off the page only to a carrier that reaches the role before the work it judges (the call refusal of a pre-action check with its index line, per the Lead's decisions in the pages spec §9/§10) or leaves a role whose contract can never trigger the check | `T1rp/no-row-lost/<role>` green; new rows `K10p/narrowed-by-contract/*` |
| AR-11 only the context the work needs | duplicate statements of one requirement collapse to one; rows a role's contract cannot trigger leave that role | K10 per role before/after in the report |
| AR-12 friction / cost | U falls per role; no extra call except where §3 names one | report table |
| AR-13 one reader / one printer | `role_cli.refuse` stays THE printer of a role CLI refusal; the per-check lines are printed by it, from `stage_joints.told_line` (the one line renderer) | grep: no second renderer of `- [<check>]` lines outside `stage_joints.told_line` |
| AR-15 one survivor | the row (page or call) is the survivor; a prose duplicate in a slice is unmarked for the role, never the reverse (path legs are a ratchet at 0: `stage_joints._legacy_legs`, 1167-1172) | `stage_joints.py --check` shows `legacy_legs 0` |
| AR-18 one output shape for refusals | `refuse` keeps its line order and its LAST line `  check: ...`; added lines stand before it | row `K10p/refuse-shape-last-line` |
| AR-20 shrink-only ratchets | `native_headroom` never raised by a card; `ratchet_tokens` / `process_ratchet_tokens`, `told_ratchet.unsited` and the census ceilings only lowered, each named | ratchet rows in the report; `test_role_load.py`, `test_judgment_census.py` green |
| AR-22 field produced has a reader | the `records` an error carries (produced by `execution_request.py` 377, `probe_by_code.py` 206-213) get their reader in `refuse` | row `K10p/refuse-prints-every-record` |
| AR-23 empty outcome declared | an error with no `records` prints as today; a role left with zero rows of a family gets no index line (existing T1rs row) | rows in §5 |
| AR-1 closed variety is data | which roles a handoff_check row tells is derived from contract data (`handoff.null_outcomes`, the contract's field list, `handoff_check.TRIED_CONTRACTS`), checked by a join test, never by a role-name list in code | `K10p/narrowed-by-contract/*` |
| AR-29 code judges data | no check moves judgment into code; the proof constants and joins are data | critic question 11 |

Checks this draft adds or alters - owner served, census class:

| check / function | change | owner it serves | census class |
|---|---|---|---|
| `role_cli.refuse` | prints one `told_line` per extra Record of `problem.records` | data (carrier of the requirement) | printer; no blocking unit |
| `T1rs/marked-by-proof` constants (`test_contract_slices.py`) | carry lists for roads `red_sandbox`, `probe_by_code`; road `import_test_receipt` proved | data (join row <-> proof) | test-only, no unit |
| new rows `K10p/narrowed-by-contract/*` (`test_contract_slices.py`) | roles of `handoff_check:null_outcome.*`, `:findings_tooling`, `:tried` == writers of contracts that carry the checked section | data (join) | test-only |
| `judgment-census.json` roles of the handoff_check units of those rows | narrowed with a `note`; dense ceilings lowered (shrink) | data (label fix) | no new unit |
| `contract_slices` continuation page | drops the `<T>/<ID>/<home>` legend line on pages 2+ | data (renderer) | renderer, no unit |
| marker lines in `references/common-rules.md`, `references/artifact-contract-plan.md` | duplicated blocks moved under their own heading, unmarked for the roles whose page carries the row | judgment (J1/designer, accepted by the Lead: "does the row say all of it") | no unit |

Judgment: none moved into code. Whether a slice block says nothing beyond its row is a judgment, written out block by block in
§5 K2 by the designer and accepted by the Lead (not left to the builder).

One road (P31): every lever is one rule for every role - a row moves by its family, its proof or its contract, never by the
role's name; the strategist's residual is not exempted, it goes to the owner as a named raise (§4) or a fork (§6).

---

## §2 Where the bytes are (item 1)

### §2.1 Per role, by source

`pages` = all `references/slices/<role>/handoff-keys*.md`. Page bytes: M from the T1r-sites S-2 report table (automator 27,572,
code-critic 19,172) and the T1r-pages report §2 (strategist 11,927 + 5,835), plus the fix round's named deltas (automator -28,
code-critic +90; the strategist's +252 is in its charter, not its pages). Everything else = U - pages (E by subtraction; split
per file by line count L, not by bytes).

| source (injection layer) | qa-automator | qa-code-critic | qa-test-strategist |
|---|---|---|---|
| key pages, all (M) | ~27,544 (3 pages) | ~19,262 (2 pages) | 17,762 (2 pages) |
| - of it: `## What code will check of you` + card (E, line lengths) | ~22,000 | ~15,700 | ~11,350 |
| - of it: `## Handoff form` (E) | ~4,600 | ~3,000 | ~6,100 |
| charter `agents/<role>.md` (L) | 87 lines | 91 lines | 85 lines |
| `references/tester-manifesto.md` (common, L) | 80 lines | 80 lines | 80 lines |
| `slices/<role>/common-rules.md` (L) | 134 | (L in §7) | 92 |
| other own slices / files (L) | artifact-contract-automation 166, execution-lifecycle 109, test-code-patterns 153, vocabularies 12 | artifact-contract-automation, execution-lifecycle, test-code-patterns (slices), `references/code-review-rubric.md` 126 | artifact-contract-plan 122, `references/risk-policy.md` 46, `references/automation-candidacy.md` 90 |
| everything but the pages (E = U - pages) | ~53,841 | ~55,155 | ~38,214 |

Command that replaces every E above (pure read, no write; K0 runs it, from `W`):
`python -B -c "import sys;sys.path.insert(0,'scripts');import role_load as R,inject_context as I;from pathlib import Path;m=R.load_imap();[print(r,[(e,R._delivered_bytes(Path('.')/e.split(':',1)[1],e,r,m,'first')[0]) for e in ['plugin:agents/'+r+'.md']+[x for x in I.entries_for(r,m,'first') if x.startswith('plugin:')]]) for r in ('qa-automator','qa-code-critic','qa-test-strategist')]"`
(`_delivered_bytes` for the charter equals `content_bytes`: no `kinds` row touches a charter.)

Growth against main, for scale (M, T1r-pages fix report §4, first-start tokens `role_load.py --all --json`): automator +6,454,
code-critic +3,804, strategist +2,784 tokens over origin/main fdc94d9. For the strategist, main's key page carried only
`Outputs / Witness / Handoff form` (read-main page: headings at 5/14/18, 90 lines; branch: 120 + 27 lines): its whole growth is
the `What code will check of you` section.

### §2.2 Per role, by family of the check section (M chars where the T1r-pages report §3 measured them; E after S-2)

| family | automator | code-critic | strategist | told where else today |
|---|---|---|---|---|
| exit_gate (incl. EG-digest-form ~830) | 1,330 | 1,330 | 1,139 | common-rules `Your handover` (digest block), refusal |
| handoff_check (universal 19 rows) | 3,326 | 3,326 | 3,326 | form file, refusal |
| execution_request | ~5,350 E (8,170 M before S-2) | 6,017 | - | refusal (sited rows), `run_suite.py --template request` |
| run_suite | ~420 E (begin only) | 773 | - | refusal |
| manifest_put | 2,623 (+ expectation_changes ~420 E) | 169 | - | refusal after the fragment is written; `manifest_put.py --help` (epilog = command card, not rows) |
| s5_precheck | 3,947 (+ window rows ~1,900 E) | - | - | exit gate refusal |
| validate_artifacts | 1,253 | 384 | 845 | validator refusal; slice contracts |
| controller / coverage / planning | 328 | 850 | 435 / 1,560 / 1,659 | refusal; strategist slice `artifact-contract-plan.md` |
| index lines (6 / 4 / 2 families) | ~1,300 E | ~700 E | ~330 E | - |
| `Not yet in rows` card | ~1,450 E | ~950 E | ~1,270 E | partly the rows above (§2.3) |

### §2.3 Duplicated between the role's injected text and what a script already prints / what another injected file states (E)

| duplicate | roles | bytes (E) | survivor |
|---|---|---|---|
| D1 EG-digest-form row vs `common-rules.md` `Your handover` digest block (the code block + "One row per item...") | all 12 | ~330 per role | the row (printed again by the exit gate's refusal) |
| D2 `coverage_contract:obligations.observation` row vs `artifact-contract-plan.md` `observation_contract (on each obligation)` bullets vs the card's no-write sentence | strategist | ~1,000 (slice bullets) + ~450 (card) | the row; the slice bullet "A ref ... names an existing check of this obligation: ..." is NOT in the row and stays |
| D3 automator card vs rows `s5_precheck:bindings/oracle/environment`, `check_manifest_invariants`, `manifest_put:expectation_changes`, charter Tools 69/72 | automator | ~800 | the rows; card text belongs to T1r-cards (F-5) |
| D4 `## Handoff form` page section vs the form file `work/handoffs/<dispatch>.yaml`, written by `story_step` through `handoff_init` before the role starts (`W\scripts\story_step.py` 311, 370-378) and named in the packet (1304-1307) | all | automator ~4,600, code-critic ~3,000, strategist ~6,100 | F-2 (owner) |
| D5 the `<T>/<ID>/<home>` legend on every continuation page (page 1 carries it, and page 1 is injected with every continuation) | roles with 2+ pages | ~190 per continuation page | page 1 |
| D6 manifest_put rows on the page vs `manifest_put.py --help` (the role_cli index line already says "run `manifest_put.py --help` before you write an input file") | automator | ~3,000 | F-3 |

### §2.4 Rows that tell a requirement no check can judge for that role (E)

| text | roles told today | judged only for | bytes per role told wrongly (E) |
|---|---|---|---|
| `handoff_check:null_outcome.*` (6 rows) | 12 (`stage-joints.json` 5458-5650: explicit 12-role lists) | the writer of the one contract that declares a null outcome: `handoffs/s7-analyst-to-automator.yaml` (Grep count `null_outcome` over `handoffs/`: that file only) | ~535 |
| `handoff_check:findings_tooling` | 12 (5384-5419) | writers of contracts with a `findings` list (`handoffs/s4-case-critic-to-designer.yaml`, `s5-critic-to-automator.yaml`, `s7-automator-to-analyst.yaml`; `handoff_check.check_findings` 1756-1787 reads `findings`) | ~110 (strategist; automator kept: it writes `s7-automator-to-analyst` per the file name - K0 confirms the writer) |
| `handoff_check:tried` | 12 (5310-5345) | contracts in `handoff_check.TRIED_CONTRACTS` (1657-1659); `s5-critic-to-automator` is not in it | ~230 (code-critic) |
| EG-digest-form clause "A verdict or a state word outside the form's list is advice, not a refusal; a reason over 80 characters, ... are mended by code when mending makes the form pass." | 12 | nothing: it says what is NOT refused | ~300 (F-4) |

---

## §3 The pay-down options (item 2)

Invariant for every option: no requirement a check judges disappears from what the role is told before the work it judges;
K10 stays shrink-only (AR-20); nothing is told less than on main.

| # | option | saves per role (E; basis) | cost to the role (P11/FR-55) | FR-38: still before the work? | invariant it must keep |
|---|---|---|---|---|---|
| L1 | Carry lists + provoked told for roads `red_sandbox`, `probe_by_code` (Lead note 2b; S-2 report Q2): name in the proof data which `execution_request` / `run_suite` ids each road carries, and provoke each road's printed `told` (`red_sandbox._carry_told` 1292-1298 into the answers at 1714 / 2198; `probe_by_code` printers 6266, 8284, 8367, 8372 via `told_fields`) by a test row; then the marker rule of `T1rs/marked-by-proof` marks the rows | code-critic -4,950 alone (14 ER + 3 RS rows ~6,860 minus the four unproved on every road ~1,470, plus 2 index lines ~440); analyst ~-5,000 (already green); automator 0 (its roads are run_suite, import_test_receipt) | first refused call shows the row (one turn) - the call launches no test | yes: a pre-action call refusal, nothing written is lost except a request file, whose before-work source is `--template request`, named in the ER index line (pages spec §10 B2 (3)) | a road marks a row only when it carries AND prints it; any doubt keeps the page (S-2 E2) |
| L2 | Per-check printer in `role_cli.refuse` (Lead note 2a): an error whose `args[0]` is a Record and which carries `records` prints one `told_line` per further sited Record, so the `import_test_receipt` road tells every refused check, not the first (`import_test_receipt._told_request_error` 260-270 keeps the rest in `records` today) | automator -2,950 (10 request rows + `stand.reference`, line lengths on page 1/2) | none extra: the same refusal, longer | yes, same reason as L1 (template door) | `refuse` keeps its order and its last line; an error with no `records` prints byte-equal to today |
| L3 | Provoke the four rows unproved on every road (`selector_args`, `window_first`: test rows written in `test_execution_request.py`, not run - S-1a "W"; `stand`: `main` site; `run_suite:begin`: launch-path printer - S-1b "N") | automator -1,110 (window_first, stand, begin; `selector_args` stays page-told for the automator by class, §10 (3)); code-critic -1,470 (all four; counted in L1+L3 = -6,420) | as L1 | as L1 | as L1 |
| L4 | Narrow `handoff_check:null_outcome.*`, `:findings_tooling`, `:tried` to the roles whose contract carries the checked section (data edit of producers' `roles`, census narrowed) | automator -535, code-critic -765, strategist -645 | none | n/a: the check can never judge those roles | roles of each row == writers of contracts with the section (join test); a role whose contract gains the section later is red until added |
| L5 | Drop the legend line from continuation pages | -190 per continuation page: automator -380, code-critic -190, strategist -190 | none | n/a (a legend, not a requirement) | a continuation page is listed only with its page 1 (`_continuation_pages`); a page 1 that is not injected keeps nothing for the continuation to rely on - K8/inject-map check already refuses that |
| L6 | EG-digest-form: drop the leniency clause (§2.4) | -300 per role, all 12 | none | n/a | the row still states every refused form error; the clause is advice about mending, judged by nothing |
| L7 | `common-rules.md` `Your handover`: move the digest code block and "One row per item in your scope, the ones that went nowhere included." under a new heading unmarked for every role that has `exit_gate:EG-digest-form` on its page (the source keeps the text for the conductor and the skills) | -330 per role, all 12 | none | yes: the row is on the page before work | unmark only for roles whose `rows_for` holds the row (join test); the anchor `Code checks: the exit gate` (role-rules `common-rules-exit-gate-checks-the-digest-shape`) stays in the SOURCE file and stays marked |
| L8 | Cut card sentences a row already states (D2 card part, D3) | automator -800, strategist -450 | none | yes | owned by the ahead-cards data and T1r-cards (F-5) |
| L9 | `artifact-contract-plan.md`: move the `observation_contract` bullets the row states (claim_kind, oracle_ref, surfaces, independent_expectations / source_conflicts, no-write, no_leak) under a sub-heading unmarked for qa-test-strategist; the bullet "A ref (...) names an existing check of this obligation: ..." and the JSON example stay marked | strategist -1,000 | none | yes: the row is on page 2, injected | the row text covers every moved bullet (designer-checked, §5 K2 item 5); role-rules anchors in the source untouched |
| L10 | Handoff form by path (D4): the key page drops `## Handoff form`; the page and the `handoff_check:field.*` rows name the form file the packet names | automator -4,600, code-critic -3,000, strategist -6,100 (minus ~150 for the pointer line) | one Read of the form at start (the role reads it anyway to fill it) | yes when the form exists before the role starts (story_step writes it before dispatch); a dispatch with no form owes no handoff_check (no requirement to tell) | F-2 (owner); role-rules carrier `blocked-row-names-every-instance` anchored on the automator key page must move to its other two carriers |
| L11 | manifest_put rows told by `manifest_put.py --help` (epilog prints the family's rows through `told_line`); the page keeps one index line "run `manifest_put.py --help` before you write a fragment" | automator -2,750 (rows ~3,000 minus ~250 line) | one `--help` call before the first fragment (already asked by the role_cli index line) | yes only if the role runs `--help` before writing (instruction on the page, no gate); else it learns at the refusal after writing a fragment - the Lead took manifest_put OFF the call list for exactly that (§10 B2 (1)) | F-3 (reverses a Lead decision) |
| L12 | Designer prose pass (F-2 (c) of the pages spec): charter/slice prose the rows now state, per section, measured | not estimated: I did not read execution-lifecycle, test-code-patterns, code-review-rubric whole (budget) | none | yes | judged per block; a separate designer node |
| L13 | F-10 (b) of the pages spec: exempt generated key pages from the 12,000-byte cap; a page splits only at K8's W | ~-250 per page removed (comment + heading): automator 3 -> 2, strategist and code-critic 2 -> 1 after K1/K2 | none | n/a | queued Lead node (changes a limit) |
| L14 | Appendix A at the source (H counts real project files) | changes H, not U | - | - | owner |
| L15 | named raise of `native_headroom` | - | Codex may refuse the role on a project whose `project:` files are large | - | owner (§4) |

---

## §4 Arithmetic, and the question for the owner (items 3 and 4)

Recommended Lead-level set = **K1 (L1+L2+L3) + K2 (L4+L5+L6+L7+L9)**; E numbers, error about +-10 % of each saving.

| role | now (M) | after K1+K2 (E) | green line | verdict (E) |
|---|---|---|---|---|
| qa-code-critic | 74,417 | 74,417 - 6,420 - 765 - 190 - 300 - 330 = **66,412** | 68,400 | **green**, margin ~2,000 (still green without L6/L7: 67,042) |
| qa-automator | 81,385 | 81,385 - 2,950 - 1,110 - 535 - 380 - 300 - 330 = **75,780** | 68,400 | **red, +7,380** |
| qa-test-strategist | 55,976 | 55,976 - 645 - 190 - 300 - 330 - 1,000 = **53,511** | 46,008 (42,400) | **red, +7,503 (+11,111)** |

With the forks on their recommendation (F-2 L10, F-3 L11, F-5 L8, L13):

| role | after K1+K2 | after + L10 + L11 + L8 + L13 (E) | verdict |
|---|---|---|---|
| qa-automator | 75,780 | 75,780 - 4,600 - 2,750 - 800 - 250 = **67,380** | green, margin ~1,000 (inside the estimate's error: K0's measure decides) |
| qa-test-strategist | 53,511 | 53,511 - 6,100 - 450 - 250 = **46,711** | **red by ~700 over its baseline, ~4,300 over H** |

Plain statement (item 4): **no set of nodes I can name brings qa-test-strategist under 46,008 - nor under 42,400 - without
dropping a requirement a check judges.** Its plugin share before this topic was already 46,008 = its baseline (T3a report line
34), and its whole growth is the check section (§2.1), which is ~11,350 bytes of mostly OUTPUT rows (planning_contract,
coverage_contract, validate_artifacts, the universal block) that must stay before the work. Only L12 (unmeasured), L14 or L15
can close it. **qa-automator closes only with an owner/Lead fork (L10 and L11)**, and then by an estimate inside its error.
**qa-code-critic closes with the Lead-level set.**

**Question for the owner (OQ-1, plain words, for the morning).** "Two roles - the test planner and the test writer - are now
too big to be sure Codex accepts them when a project's own files are at their largest. I can shrink the test writer under the
limit only if its handover form is read from the file the factory already writes for it before it starts, instead of being
copied into its prompt (it costs the role one file read). The test planner cannot be shrunk enough without hiding from it a
rule the factory checks. Options: (a) accept a recorded raise of the planner's ceiling to the size measured after this
clean-up (about 53,500 bytes; the writer about 75,800 if you also say no to the form-by-path) - Codex may then refuse these
roles on a project with very large own files; (b) let Codex hand big project files by path instead of pasting them (bigger
change, the real cure); (c) both. I recommend (b) as the cure and (a) for the planner until then."

Exact raise numbers (OQ-1 (a)): the K10 baseline row = the MEASURED U after K1+K2 (K2's report prints it), never the E above;
reason per role: strategist - "its output rows (S3 plan contract) must stay before the work; prose duplicates removed (K2);
residual is the check section itself"; automator (only if the owner refuses L10/L11) - "request/manifest rows proved at the
call; the residual is its output checks (s5_precheck, validate_artifacts, manifest rows by class) and the handoff form".

---

## §5 Builder cards (dispatch form)

Order: **K0 -> K1 -> K2 -> (K3 on F-2, K4 on F-3) -> merge**. Not parallel: K1 and K2 both write `references/stage-joints.json`,
regenerate `references/slices/**` and lower rows of `references/role-load.json` (rule 4 overlap). K3 and K4 overlap K2's
slices too. K0 is read-only and may run alone first.

### §5.0 K0 - measure (read-only; replaces every E)

given: this file; `W\scripts\role_load.py`; `W\scripts\inject_context.py`; the three key pages.
owns: `C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-k10-paydown-k0-measure.md`
non-goals: any edit under `ai-packages/`.
handoff: the report: per role per file bytes (the §2.1 command, verbatim output); per row bytes of every row §3 moves (pure read
over `contract_slices.handoff_keys_pages` or the page files: `len(line.encode()) + 1` per `- [<check>]` line); the writer role of
`s7-automator-to-analyst` (`handoff.contract_of`); whether every role's `rows_for` holds `exit_gate:EG-digest-form` (pages spec N-4);
the §4 tables recomputed with M numbers.
edges: a file that cannot be read is printed as `None`, never 0 (FR-41).
siblings: none -- read-only.
DoD: the report carries the verbatim output of the §2.1 command and of
`python -B ai-packages/qa-factory/scripts/role_load.py --all --json`; every E of §4 has its M beside it.

### §5.1 K1 - prove the call carriers (L1 + L2 + L3)

given: this file; `docs/tasks/specs/20261114-told-before-work-t1r-sites-spec.md` and the S-1a / S-1b / S-2 reports;
pages spec §9-§10; `W\scripts\role_cli.py` (`refuse`, `run_guarded`, `epilog`); `W\scripts\import_test_receipt.py`
(`_told_request_error`, `import_receipt`); `W\scripts\execution_request.py` (records at 377); `W\scripts\red_sandbox.py`
(`_carry_told`, the answers that carry `told`); `W\scripts\probe_by_code.py` (`ToolRefusal`/records 206-213, printers 6266,
8284, 8367, 8372); `W\scripts\detector_verdict.py` (`told_fields`, `refusal`); `W\scripts\stage_joints.py` (`call_told`,
`told_line`, `real_sited`); `W\references\stage-joints.json`; tests `test_contract_slices.py` (`test_t1rs`, `T1rs/marked-by-proof`),
`test_detector_verdict.py`, `test_import_test_receipt_refusal.py`, `test_execution_request.py`, `test_red_sandbox_probe.py`,
`test_probe_by_code.py`, `scripts/tests/test-layers.json` (all six are `keep`); `design/factory-rules.md` whole; `plans/builder-rules.md`.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\role_cli.py (refuse)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\stage-joints.json (call markers on producer entries of execution_request:* and run_suite:* rows only; told_ratchet.unsited lowered to the measure)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\slices\ (generated by contract_slices.py --write only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\role-load.json (ratchet_tokens, process_ratchet_tokens: LOWER only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_contract_slices.py (T1rs proof constants: road carry lists; new K10p/* rows)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_detector_verdict.py (new K10p/refuse-* rows)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_import_test_receipt_refusal.py (new row: several refused checks all printed)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_red_sandbox_probe.py (new rows: a refused request's told reaches the printed answer)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py (new rows: same, for the printed refusal JSON)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_execution_request.py (the S-1a written rows for selector_args, window_first; a provoking row for stand and run_suite:begin)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\changelog.d\tbw-k10-paydown-k1.md
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-k10-paydown-k1-report.md
non-goals: `native_headroom` (never raised; lowered only if a role's measure falls under a row); `call_told_families` membership;
`manifest_put` rows (F-3); any row sentence; refusal texts other than the extra lines of `refuse`; `inject_context.py`;
`role_load.py`; a new test file; quarantined tests; CI, mutations (PROJECT.md «Командная работа» п. 13).
handoff: branch commit + report: per role U before/after (M), rows newly call-told per role and per road, ratchet rows (key, old ->
new), the carry lists as written, FR walk, verbatim witness, slow files named "judged by the batch canon".
edges:
- (E1) `problem` is a plain `str`, or a Record with no `records`, or `records == ()`: output byte-equal to today. Invariant: no
  refusal changes for a caller that passes no records.
- (E2) `records` holds the first Record again (as `_told_request_error` builds it: `records = exc.records` whose [0] is the
  Record printed as `expected/door`): the first is not printed twice. Invariant: one line per distinct check.
- (E3) `records` holds a non-Record item (`test_detector_verdict.py` 1001 builds one with `"x"`): skipped. Invariant: never raises
  (`refuse` docstring: "Never raises").
- (E4) a Record whose check is the command's own `role_cli:<command>`: printed as today (card lines), not as an extra line.
- (E5) limit: more than `branch_accounting.limit("refusal_units_shown")` extra records: print that many, then one line
  "N more checks refused: run the command again after fixing these". AT the limit all print; BEYOND it the tail line names the
  count. Invariant: the role learns every check by repeated calls, never a silent drop.
- (E6) output order: `<command>: <problem>`, expected/door of the first, the card lines, the extra `told_line`s, `if you cannot`,
  LAST `  check: <first record's check>`. Invariant (POSITIONAL): readers of the last line (`story_run.match_known` routes on
  markers, the `check:` line is last) see the same last line; the extra lines never stand after it.
- (E7) a road's carry list names an id the road cannot raise (typo, stale): `T1rs/marked-by-proof` red naming road and id.
  Invariant: no marker on a row its road cannot carry.
- (E8) a carried id whose printed `told` is not provoked by a test row: no marker for any role using that road (E2 of S-2).
  Invariant: unproved keeps the page.
- (E9) a role with several roads: marked only when EVERY road it uses carries AND proves the row (S-2 rule). Invariant unchanged.
- (E10) the provoking rows sit in slow files (`test_probe_by_code.py` 221 s, `test_red_sandbox_probe.py` 61 s,
  `test_execution_request.py` 21 s: `scripts/slow_tests.json` 36, 78, 92): written, not run locally; the proof constants flip in
  the same commit. TEMPORAL: before the canon runs them the marker rests on an unrun row - the canon is the judge; a red canon row
  is a `defect_found` on K1 and the constant flips back with its marker in one diff. Invariant: never a marker without a written
  provoking row.
- (E11) TEMPORAL: `records` printing exists only after K1; before it the import road tells the first check only, so no
  automator request row is marked before this commit. Both worlds: the marker and the printer land in one commit.
- Error direction of reused functions in a more consequential role: `told_fields` / `_carry_told` become proof carriers for a
  call marker (advice -> gate input): they may err toward printing MORE (an extra sentence) never toward a marker on a row they do
  not print; adversarial inputs: a refusal whose Record list is empty, a summary whose `told` is not a list, two refusals of the
  same check, a refusal raised after a partial launch (`probe_by_code` walk rows at 6255: "a later row ... its own tooling
  outcome") - that one is NOT a pre-action refusal: its ids stay page-told.
tests (docs/TESTING.md layers; one table per behaviour):
- table `K10p/refuse-*` in `test_detector_verdict.py`: rows `no-records`, `records-first-repeated`, `non-record-item`,
  `own-command-check`, `at-limit`, `beyond-limit`, `last-line-is-check`.
- data join `T1rs/marked-by-proof` extended: rows `road-carries/<road>/<id>`, `road-carry-unknown-id-red`, `road-unproved-keeps-page`.
- scenario rows in the four road test files as listed in owns (one provoking row per road per family).
DoD (narrow; from the worktree root):
1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/role_cli.py ai-packages/qa-factory/references/stage-joints.json ai-packages/qa-factory/references/role-load.json` - every non-slow file it lists, each alone; slow ones named "judged by the batch canon".
2. `python -B ai-packages/qa-factory/scripts/contract_slices.py --write` then `--check`
3. `python -B ai-packages/qa-factory/scripts/stage_joints.py --check` (clean; `legacy_legs 0`; `unsited` at the measure)
4. `python -B ai-packages/qa-factory/scripts/tests/test_detector_verdict.py`, `test_import_test_receipt_refusal.py`, `test_contract_slices.py`, `test_role_load.py` (each alone)
5. `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
Expected K10 (E, K0 replaces): qa-code-critic about 68,000 (74,417 - 6,420) - green or within ~400 of H; qa-automator about
77,325 (81,385 - 2,950 - 1,110), red; strategist unchanged 55,976, red. Acceptance keys: K10 lines name only the roles still over;
no raise in `role-load.json`; every new row green or named slow.
siblings: `role_cli.epilog` (the `--help` twin of `refuse`; F-3 would use it); `hooklib.block`, `stage_guard.deny` (other T2
transports: they print one Record each, no `records` - untouched); `red_sandbox._carry_told` / `probe_by_code` `told_fields`
callers; S-2 Q1/Q2/Q3; SIBLING_MAP axis 34 (one road), axis 18 (ratchets).
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-k10-paydown-spec.md
architecture: AR-10, AR-13, AR-18, AR-20, AR-22, AR-23 -- the records an error carries reach the role at the call; one printer; the refusal's last line kept; ratchets only lowered
judgment: none -- printer and proof data only

### §5.2 K2 - one statement per requirement (L4 + L5 + L6 + L7 + L9)

given: this file; K0 and K1 reports; `W\references\stage-joints.json` rows 5310-5650 (the handoff_check rows) and the
`exit_gate:EG-digest-form` row; `W\scripts\handoff_check.py` (`TRIED_CONTRACTS` 1657, `check_findings` 1756,
`_declared_null_outcomes` 1395); `W\scripts\handoff.py` (`null_outcomes`, `contract_of`, `spec`); `W\handoffs\*.yaml`;
`W\scripts\contract_slices.py` (`requirement_section`, the continuation page writer); `W\references\common-rules.md`,
`W\references\artifact-contract-plan.md` (sources; never the slices by hand); `W\design\role-rules.json`;
`W\scripts\tests\fixtures\judgment-census.json`; tests `test_contract_slices.py`, `test_stage_joints.py`, `test_judgment_census.py`,
`test_role_load.py`; `design/factory-rules.md` whole; `plans/builder-rules.md`.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\stage-joints.json (producers' roles of handoff_check:null_outcome.*, :findings_tooling, :tried; the sentence of exit_gate:EG-digest-form per F-4)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\contract_slices.py (the continuation page writer only: no legend line on pages 2+)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\common-rules.md (heading split + marker of the digest block only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\artifact-contract-plan.md (heading split + marker of the observation_contract bullets only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\slices\ (generated only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\references\role-load.json (ratchets LOWER only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (`roles` + `note` of the units of the narrowed rows; dense ceilings lowered)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_contract_slices.py (new K10p/* rows)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\scripts\tests\test_stage_joints.py (pins that move with the narrowed rows only)
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\ai-packages\qa-factory\changelog.d\tbw-k10-paydown-k2.md
C:\QAFactory\forge-repo\.claude\worktrees\tbw-t1r\docs\tasks\specs\reports\20261114-k10-paydown-k2-report.md
non-goals: deleting any text from a source file (blocks MOVE under their own heading; the source keeps them); charters; the
handoff form section (F-2); manifest_put (F-3); ahead cards (F-5); any other row's sentence; `native_headroom`; CI, mutations.
handoff: branch commit + report: per role U before/after (M) and the §4 table with M; the narrowed rows (row, roles old -> new,
the contract fact that decides it); census rows changed; ratchet rows; the measured baseline numbers for OQ-1; FR walk; witness.
items (the direction is chosen; a builder does not judge prose - the moved blocks are exactly these):
1. L4: `handoff_check:null_outcome.{repairs,verdict,names,report,failures,listing}` roles := the writers of contracts for which
   `handoff.null_outcomes(contract)` is non-empty; `handoff_check:findings_tooling` roles := writers of contracts whose spec has a
   `findings[]` field; `handoff_check:tried` roles := writers of `TRIED_CONTRACTS`. Writers via `handoff.contract_of` over
   stages.json (as `role_load._form_candidates`). Census: the units these rows join, `roles` narrowed the same way with a `note`
   ("told only to roles whose contract carries the section; <fact>"); lower each dense ceiling the test names (a shrink).
2. L5: the continuation page omits the legend line; page 1 keeps it.
3. L6 (on F-4 (a)): `exit_gate:EG-digest-form` sentence without the clause quoted in §2.4; nothing else in it changes.
4. L7: in `references/common-rules.md` `## Your handover: the form, then the digest line`, the lines "Your final message IS the
   digest, three parts, no prose:", the fenced block, and the sentence "One row per item in your scope, the ones that went nowhere
   included." go under a new `### The digest line` heading placed right after the form paragraph, with a `<!-- roles: -->` marker
   listing only roles whose `rows_for` does NOT hold `exit_gate:EG-digest-form` (none expected: then no marker at all, the
   conductor and skills read the whole file). The sentence "Code checks: the exit gate; the refusal names what is wrong and the
   way through. What the next role or the human needs is in the FILE or the FORM: chat does not survive the dispatch." stays under
   the marked parent heading (role-rules anchor `Code checks: the exit gate`).
5. L9: in `references/artifact-contract-plan.md` `## Fields the plan validator checks`, the `observation_contract` bullets
   `claim_kind`, `oracle_ref`, `surfaces`, `independent_expectations ... source_conflicts`, `No-write`, `no_leak` move under a
   sub-heading `#### observation_contract fields the S3 row states` with a marker that excludes qa-test-strategist (keeps every
   other role the parent marker lists); the bullet "A ref (`assertion_ref`, each of `controls`, ...) names an existing check of
   this obligation: ..." and the JSON example stay under the strategist's heading. Designer check (done here): every moved
   bullet's content is in the row `coverage_contract:obligations.observation` (page 2 line 7): claim_kind list, oracle_ref joining
   requirement_refs at revision or a source-conflict decision, surfaces id/boundary/status/gap_reason/assertion_ref,
   independent_expectations triple with >= 2 for response_parity, source_conflicts ids, no-write sequence + positive_control_ref +
   reachability_assertion_ref, no_leak payload_assertion_ref.
6. Regenerate (`--write`), measure, lower ratchets; a role still over H is listed (STOP), never raised.
edges:
- (E1) a contract that gains a null-outcome declaration / a findings list / joins TRIED_CONTRACTS later: the join row is red
  naming the role to add. Invariant: a check never judges a role its rows do not tell.
- (E2) a contract with no writer in stages.json: no role added; the join row names it. Invariant: no row with an empty producer
  list (the row would state nothing to anyone; `_producer_leg` refuses `roles: []`) - if a narrowing empties a row's roles, the
  card STOPS for that row and reports it.
- (E3) a role with one page only: nothing to drop (L5). A continuation page whose page 1 is not listed: already refused by the
  map check. Invariant: the legend is on every injected page set exactly once.
- (E4) a marker that would exclude every reader of a block: no marker (whole-file readers only), stated in the report.
  Invariant: no block becomes unread by every role that is judged on it.
- (E5) POSITIONAL: the new headings sit inside their parent sections, so `contract_slices.parse` keeps every other block's
  marker scope (a marked `###` under a marked `##` ends at its sibling - `role_load.craft_split` stack rule). Invariant: no other
  block changes its role set (`--write` diff touches only the moved blocks' slices and the pages).
- (E6) role-rules: every anchor of `design/role-rules.json` still found in its carrier (`role_rules.py --check` 0 findings).
- (E7) TEMPORAL: the new headings and narrowed rows exist only after K2; pages and slices regenerate in the same commit.
siblings: the other universal handoff_check rows (`blocked_problem`, `required_rows.*`): same join question - not narrowed here
(every contract carries them; report if K0 finds one that does not); the `kb/` role-card pages quoting rows; SIBLING_MAP axis 32
(census), axis 18 (ratchets), axis 34.
tests: data join `K10p/narrowed-by-contract/<row>` (roles == contract writers, each row), `K10p/narrow-empty-roles-stops`;
table `K10p/continuation-no-legend` (1 page / 2 pages / 3 pages); `K10p/digest-block-unmarked/<role>` (the row is on the page iff
the block is unmarked for the role); `K10p/observation-bullets-moved` (strategist slice lacks the moved bullets and keeps the
"A ref" bullet; the row holds each moved field token).
DoD (narrow; from the worktree root):
1. `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/references/stage-joints.json ai-packages/qa-factory/scripts/contract_slices.py ai-packages/qa-factory/references/common-rules.md ai-packages/qa-factory/references/artifact-contract-plan.md ai-packages/qa-factory/references/role-load.json` - each non-slow file alone; slow ones named.
2. `python -B ai-packages/qa-factory/scripts/contract_slices.py --write` then `--check`
3. `python -B ai-packages/qa-factory/scripts/stage_joints.py --check`
4. `python -B ai-packages/qa-factory/scripts/role_rules.py --check` (0 findings)
5. `python -B ai-packages/qa-factory/scripts/tests/test_contract_slices.py`, `test_judgment_census.py`, `test_role_load.py` (each alone)
6. `python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang`
Expected K10 after K1+K2 (E): code-critic ~66,400 green; automator ~75,800 red (STOP); strategist ~53,500 red (STOP). The report
prints the measured numbers OQ-1 needs.
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261114-told-before-work-k10-paydown-spec.md
architecture: AR-1, AR-10, AR-11, AR-15, AR-20, AR-23 -- rows told only where a contract can trigger them; one statement per requirement, the row survives; ratchets only lowered
judgment: J1 -- which slice blocks the rows fully state was judged by the designer (item 5) and is accepted by the Lead

### §5.3 K3 - handoff form by path (L10), only on F-2 (a)

Buildable on the recommendation; outline (the Lead promotes it to full dispatch form once F-2 is answered): owns
`scripts/contract_slices.py` (`handoff_keys_page`: drop `## Handoff form`, add one line "Your handover form is the file your packet
names (`work/handoffs/<dispatch>.yaml`, written before you start): read it before the work; every field it lists is checked
(`handoff_check.py`)."), `scripts/stage_joints.py` (`FORM_TEXT`: "every `required` field of your handoff form file"),
`design/role-rules.json` (carrier `blocked-row-names-every-instance`: drop the key-page carrier, keep the two others), slices,
role-load.json (lower), test rows. Edges: a dispatch with no form owed (`story_step._form_owed` false) runs no handoff_check, so
nothing is untold (invariant: no field check without its form on disk before the role starts); a form written after dispatch
(a repair re-init, `story_step` 349-378): the page line says the packet path, the file exists before the role's first turn;
demand tokens of FORM-carried rows: K0 checks `demands_from` for a form carrier first - if a row demands a field token on the page,
K3 STOPS (owner fork, not a builder choice). Expected E: automator -4,600, code-critic -3,000, strategist -6,100.

### §5.4 K4 - manifest_put rows at `--help` (L11), only on F-3 (a)

Outline: `role_cli.epilog(script)` appends, after the command cards, `told_line` of every `stage-joints.json` row whose family
stem equals the script's registry family (data join: `manifest_put` -> `manifest_put.py`); `manifest_put` joins a new data list
`help_told_families` (NOT `call_told_families`: the moment is `--help` before writing, not the refusal) with its index line
"run `manifest_put.py --help` before you write a fragment: it prints the N checks of your rows"; the five automator manifest rows
of `execution_request` stay page-told. Expected E: automator -2,750. Edge: a script without `epilog` wired keeps its rows on the
page (pages spec §10 B2 (2) rule).

---

## §6 Forks (returned, not decided)

- **F-1 (Lead) The strategist's target.** (a) its existing baseline 46,008 (K10 green); (b) H 42,400. Recommend (a): the check
  greens at the baseline, and the baseline was set by T3a as "the measured share before rows". Error direction: (a) leaves the
  strategist up to 3,608 bytes over H - a Codex refusal only on a project whose two project files are near 26,000 each.
- **F-2 (OWNER) Handoff form by path (L10).** (a) yes - the form file (written before the role starts) is the told carrier, one
  Read; (b) no - the form stays copied in the prompt; (c) only for roles over H. Recommend (a) for all roles (one road, P31; (c) is
  a second road and is refused by rule 6). Cost of covering every role: ~3-6K saved each, one Read each. Error direction: a role
  that skips the Read learns the field list at `handoff_check`'s refusal - after its work, before its handover; K3's page line
  tells it to read first. Without (a) the automator stays red (§4).
- **F-3 (Lead; reverses pages spec §10 B2 (1)) manifest_put rows at `--help` (L11).** (a) yes, a separate `help_told_families`
  list; (b) no. Recommend (a) only if F-2 is (b) or the K0 measure shows the automator still over after K1+K2+K3; else (b).
  Error direction: a role that writes a fragment without `--help` learns at the refusal after writing it (the reason the Lead
  took manifest_put off the call list).
- **F-4 (Lead) EG-digest-form leniency clause (L6).** (a) drop it (advice, judged by nothing); (b) keep. Recommend (a). Error
  direction: a role may over-correct a line code would have mended - cost one turn, never a lost requirement.
- **F-5 (Lead) Card sentences a row states (L8).** (a) cut in this pay-down (edits the ahead-cards data, collides with
  T1r-cards); (b) leave to T1r-cards, which turns cards into rows from main. Recommend (b) unless the automator's K0 measure needs
  the 800 bytes.
- **F-6 (OWNER) The residual (OQ-1, §4).** (a) a named raise of `native_headroom` to the measured U after K1+K2 (strategist; the
  automator too if F-2 is (b)); (b) Appendix A at the source; (c) both. Recommend (b) as the cure, (a) for the strategist until then.
- **F-7 (Lead) L12 designer prose pass.** (a) open it now for the automator and the strategist (execution-lifecycle,
  test-code-patterns, artifact-contract-automation, artifact-contract-plan, code-review-rubric); (b) only if OQ-1 is refused.
  Recommend (a) in parallel with K1 (read-only design work, no owns overlap).

## §7 Small choices closed by the designer

- S-1 Test prefix `K10p/`; reports `20261114-k10-paydown-k<n>-report.md`; changelog fragments `tbw-k10-paydown-k<n>.md`.
- S-2 The extra refusal lines use `stage_joints.told_line` (the existing renderer), not a new format.
- S-3 The `refuse` tail line wording for E5.
- S-4 K1 before K2 (K1 carries the larger, code-side saving and settles code-critic first).
- S-5 New headings' wording (`### The digest line`, `#### observation_contract fields the S3 row states`).

## §8 Reading trail

- Read whole: fix-round report; pages spec (incl. §9, §10); T1r-pages report; T1r-pages fix report; T1r-sites S-2 report;
  `W\scripts\role_load.py`; `W\scripts\role_cli.py`; `W\references\inject-map.json`; key pages of qa-automator (1-3),
  qa-code-critic (1-2), qa-test-strategist (1-2); `slices/qa-automator/common-rules.md`, `artifact-contract-automation.md`;
  `slices/qa-test-strategist/artifact-contract-plan.md`; `agents/qa-automator.md`, `agents/qa-test-strategist.md`;
  `references/risk-policy.md`, `references/automation-candidacy.md`.
- Read in part: `W\scripts\stage_joints.py` 530-929, 1160-1199; `W\scripts\import_test_receipt.py` 245-344;
  `W\scripts\handoff_check.py` 1755-1794; `stage-joints.json` 5300-5500; `test-layers.json` 1-30.
- Grep: `contract_slices.py` K10 (866-868); `role_load.py` K10 defs; T3a report (46,008 line 34); role-rules.json `digest`;
  `story_step.py` `handoff_init|FORM_REL`; `.records` over scripts; `probe_by_code.py` / `red_sandbox.py` `told|records`;
  `handoffs/` counts `null_outcome` (1 file), `tooling_findings` (1 file), `cause:|findings:` (3 files); `TRIED_CONTRACTS`;
  `stage-joints.json` handoff_check rows; test-layers.json names (keep 36-7115, quarantine from 7169); `scripts/slow_tests.json`;
  line counts (`^`, count) of the three roles' slices, charters, four references, and read-main's strategist slices.
- Negative claims and their positive controls: "null_outcome is declared only in s7-analyst-to-automator.yaml" - the same Grep
  (count mode, `handoffs/`) returned that file with 2 hits, and a sibling Grep for `tooling_findings` returned
  `s5-critic-to-automator.yaml` (the form read on the code-critic page lists `tooling_findings[]`): the call works on that folder.
  "main's strategist page has no check section" - same Grep (`^## |^### `) on read-main returned 3 headings and on the branch
  page the read shows the section. Miscalls seen: Glob/Grep with a slash pattern or a brace glob at the package root returned
  nothing; re-run per directory found the files (positive control: `references/slices/qa-automator` listed 9 files) - no claim
  rests on those empty results.
- Not established (K0 measures): every E; the writer of `s7-automator-to-analyst`; whether every role holds the digest row;
  whether FORM-carried rows demand tokens on the page (K3); the content of execution-lifecycle, test-code-patterns,
  code-review-rubric (L12).
- Needed beyond the manifest: `W\scripts\handoff_check.py`, `W\scripts\story_step.py`, `W\scripts\import_test_receipt.py`,
  `W\design\role-rules.json`, `W\scripts\tests\test-layers.json`, `W\scripts\slow_tests.json`, `W\handoffs\`, read-main's strategist page.
