# t-1230 — code review of T1r-cards-a (TBW1-13), branch `worktree-agent-a1bfa3bfdead0ba50`

Diff under review: `git diff origin/main...541bec6b` (merge base `b5fca9bd`, 39 files; commits `ba946ab6` + report `541bec6b`).
Spec: `docs/tasks/specs/20261117-told-before-work-t1r-cards-spec-r3.md` §1, §3, §4, §5, §6 -a, plus the Lead decisions at its end
(ra-2 dropped, so its absence is intended and is not counted as a defect).

**Verdict: NEEDS WORK — 1 blocking finding (F1).** One data line in `stage-joints.json` needs fixing, and the Lead has to
allow it, because the line sits against spec rule R-3. Everything else matches the spec exactly. The JSON verdict is
`blocker` because critic.md rule 23 says "blocker when any finding blocks". The fix needs no rework of the diff, so this is
not a reject. Accepting the work is the Lead's decision, not mine.

## Findings

**F1 (BLOCKS the merge): `stage_joints.py --check` reports a second finding that the DoD forbids.**
I ran it on the clean worktree at `541bec6b`:
```
REJECT — 2 finding(s):
- stage-joints: exit_gate:case_identity producer[0]: qa-case-designer is not told `= the file name` in any of its told files
- stage-joints: told_ratchet.unsited is 11 but 17 rows have no site in code (... the 6 ids of §4.4 + 11 stored first_look:put.* ...)
```
The DoD says: "its ONLY finding is ... unsited ...; any other finding (a missing door, a shape) is a defect of -a".
- Cause: the M2 conversion (R-3) set the producer's `told` to `[{"page": true}]` and kept `demands: ["= the file name"]`.
  The token used to sit on the page's `## Outputs` "The gate also reads:" line, and that line is generated only for rows told
  by path. After `contract_slices.py --write` the line is gone (diff of `slices/qa-case-designer/handoff-keys.md`: `-- a case
  file whose id is its file name: \`= the file name\``). The cd-1 text says "IS its file name", so the token appears nowhere.
  `stage_joints._demands_leg` (`stage_joints.py:904-937`) matches tokens as case-sensitive substrings of the page texts
  (:935-936).
- I checked the other three M2 rows the same way. `exit_gate:grounding` keeps `["derived"]` and the rt-2 text holds
  `derived`: green. `critic_rollcall:*` and `check_coverage:*` use `demands_from: check:script`: green. Only case_identity is red.
- Convention: 262 page-told producers in the new file carry `demands: []`. Only 2 carry a token (grounding, case_identity),
  as counted by my script below. `_demands_leg` :916-923 says a page-only entry with no tokens owes nothing ("the page carries
  the sentence: no tokens are owed (T1r)").
- Fix (one line, inside -a's owns): set `exit_gate:case_identity` `producers[0].demands` to `[]`, or to a token the cd-1 text
  holds (e.g. `"IS its file name"`). Then `stage_joints.py --check` must again show the unsited finding as its only finding.
  R-3 says "`demands` and `demands_from` stay", so this is a spec exception, and the Lead decides it in the fix-round
  dispatch. The spec missed this: §3.5 checked the M2 rows for doors but not for demand tokens.

**F2 (a witness I could not reproduce; rules 7/12): the report's `stage_joints.py --check` tail does not match the commit.**
The report says "REJECT - 1 finding(s)" and "the ONLY finding: unsited 11 -> 17". At `541bec6b` with a clean tree, the same
command prints 2 findings (F1). The likeliest cause is a run made before the final `contract_slices.py --write`. Either way,
this witness line does not describe the committed tree. The fix round re-runs it once, after all edits, and attaches the
output verbatim. I reproduced every other witness line (see the trail).

**F3 (fix before merge; spec-level, E-8): three rows now carry two sentences that disagree on one page line.** Each A-append
adds a clause that corrects or narrows the row's old sentence, and the old sentence stays (R-2 forbids the builder to reword
it):
- `validate_artifacts:check_run_report_v0`: the old sentence says "... and `blocked` when `env_preflight` is blocked". ru-3b
  says "A blocked `env_preflight` means `execution_status` is env_blocked". The body requires `env_blocked`
  (`validate_artifacts.py:2437-2439`).
- `validate_artifacts:check_bug_filing_header`: the old sentence says "carries non-empty `cases`". br-4a says "(or `cases: []`
  with `no_case_reason`)". The body accepts the latter (`validate_artifacts.py:434-437`).
- `validate_artifacts:check_result_rows`: the old sentence says "naming one case or a test id". ru-4a says "Every `results[]`
  row names ONE case". The body accepts a row with only `test_id` (refusal "has neither test_id nor case", :2469-2471), so ru-4a
  read alone over-claims (AR-29).
E-8's invariant is "no page says two contradicting things about one field". The spec fixed only the ck-3b case (§3.3c). The
builder could not fix these inside R-2 and its owns scope. Road: the original-sentence sweep of node TBW-T1rc-ec8 (§7, E-4).
Proposed line: `check_run_report_v0 / check_bug_filing_header / check_result_rows: old sentence contradicts the appended
T1r clause (E-8) | узел: TBW-T1rc-ec8`. Alternatively the Lead lets this fix round replace the three old sentences.

**F4 (Lead, before the merge to main): nodes TBW-T1rc-int, TBW-T1rc-site and TBW-T1rc-ec8 are not in the pile.** I grepped
`plans/piles/told-before-work/` (root checkout) and `origin/main:plans/` for `T1rc-ec8|T1rc-int|T1rc-site`, case-insensitive:
0 hits. Positive control: the same grep for `TBW1-13` hits `batch-1-finish.md:40`. The spec says -a's `unsited` red is
cleared only by TBW-T1rc-int, "before main" (§7). The no-Bash door of `values_rename` (R4-F3) and the 6 sites wait on
TBW-T1rc-site. F3 waits on ec8. The Lead decision said "enter at the next status pass", and that pass has not happened. Until
then these residuals have no carrier (rule 19, Q12(d)).

**F5 (minor, Q10 / commit form):**
- The commit names AR-10, AR-20 and AR-29, following the dispatch. Spec §1 also lists AR-11 (the K10 `native_headroom` raises
  and the K8 splits change what each role is given) and AR-22 (new rows, producer roles). The builder reported the deviation.
  The dispatch or the commit should name all five.
- The `raise:` lines: `process_ratchet_tokens` is one combined line, not the per-role
  `raise: <role> <key> <old> -> <new> (+<n> B) -- <why>` that E-9 asks for, and the ratchet_tokens lines use "tokens" where E-9
  says "B". All values are named, so AR-20 holds. The form is a minor point; no gate parses these lines (`tools/*.py` grep for
  `raise: ` -i: only `session_context.py`).

**F6 (Q11, non-blocking, a spec placement the Lead may revisit): K lines that are key procedure sit in craft sections.** Some
K lines in `## Techniques` (`<!-- kind: craft -->`) are a procedure of keys and verdict words, not testing craft:
- ts-2b (`positive_control_ref`)
- ts-3a (`oracle_unknown: true` / `source_conflict: true`)
- cd-2k (status words)
- cd-3 (`defect_class`/`basis` inherited)
- ck-4a (`fitted_to_code` -> `test_defect`)
- fa-1ak (`NOT_EXECUTED`)
- br-2k (`confirmed_by_person` / `reproduced_by_factory`)
- ra-3k (precedent row)

Craft sections are outside `process_ratchet_tokens`. The builder followed spec §3.1/S-2 exactly, and plan critic t-1046
accepted the placement, so this is not a builder defect. I name it because Q11 asks for it ("a process section marked craft
escapes the process ratchet"). If the Lead moves the lines to `## Tools`, the process ratchet is raised by measure and named.

## Spec items

| item | verdict |
|---|---|
| A-1 measure before | fit (report :13-20) |
| A-2 A / M2 / ROLE+ clauses | fit: my script checked 46 row keys for exact text and order. Each existing row = old sentence + one space + the §3.4 texts in key order; replaced rows = the §3.4 text; manifest_put = words swapped + au-2b + ck-3b. 0 mismatches. 61 changed-row × role pairs are all on the role's page (`handoff_keys_pages`) |
| A-3 §3.3 / §3.3b / §3.3c | fit (exact) |
| A-4 12 NEW rows, M2 doors | rows fit: stages, roles, field, when, door_needs and role_rule all match §4.1; 17 door keys exact. **DEFECT F1** on the M2 row `exit_gate:case_identity` (`stage-joints.json`, row `exit_gate:case_identity`, `producers[0].demands`) |
| A-5 K lines | fit: ra-2 dropped by the Lead. The ds-4b skip is legal under R-5: the fact `left_items` stands in `agents/qa-doc-scribe.md:23` ("One item for every entry of `left_items`"); the builder reported it |
| A-6 pages / splits | fit: `contract_slices --check` clean, 20 key pages; `selftest --limits --lang` 4/4 |
| A-7 caps | fit: every raise named; largest U is 79,970 B, under 100,000. Form: F5 |
| A-8 changelog | fit (one ASCII bullet; `--lang` PASS) |
| A-9 census | fit: 12 rows, 12 `raised_by` entries, bases unchanged; `dry_exits --check` 0 discrepancies, 231 -> 243 |
| owns scope | fit: role-load changes only the 3 keys; inject-map only the 2 continuation lines; driver-exits only the joints and raised_by entries; `told_ratchet` untouched; no test or script touched |

## Standing questions

- Q1 fit to spec: one defect (F1); the rest fit (table above).
- Q2 builder's own decisions: K-line form `- <text>`, a bullet after `<!-- /gen -->` as the last line of `## Tools`. That is
  the existing pattern (`qa-code-critic.md`, "The state word ..." already stands there). Safe.
- Q3 seams: the driver-exits files and inject-map change only by additions at the ends of lists. The new rows sit next to
  their parent or family rows. Nothing was reordered.
- Q4 class-wide / siblings:
  - The class of F1 is "a demand token on a row whose told carrier moved". I walked all 4 M2 rows; only case_identity fails.
  - The class of F3 is "an appended clause disagreeing with the old sentence". I walked all 30 appended rows against the E-4
    list; 3 fail.
  - Axis 38 (census): covered. Axis 18 (raises): covered and named (except `unsited`, which TBW-T1rc-int owns). Axis 34:
    covered by ROLE+ and family rows.
  - The dispatch asked about the siblings TBW1-11 (T9c, accepted 8c0c75e0) and TBW1-12 (T3b). Neither is missed by -a. The
    cards stay as told text until -b, and every one of the 12 pages still carries `### Not yet in rows` (E-2). The reader of
    the same page text that -a missed is `stage_joints._demands_leg` (F1). The builder named the pin
    `test_charters_s5_s9::test_retro_reads_only_the_numbers`, and the Lead has settled it.
- Q5 tests: no committed test (R3-F3' (a)). The new rows describe checks that already exist, behind existing doors, and the
  keep tests judge them (`--witness-for`). There are no test lines, so no `tests-over:` line is needed.
- Q6 DUPLICATION AND CONSISTENCY: several appended rows restate their old sentence on the same line (e.g.
  `check_understanding`, `check_register`). The spec routes that sweep to the named node TBW-T1rc-ec8, so per Q6 it is not a
  finding here, but see F4: that node does not exist in the pile yet. No second reader: the S-K check uses
  `contract_slices.handoff_keys_pages`, as spec P-4 asks.
- Q7 CODE QUALITY: none found (no code in the diff; JSON and markdown only).
- Q8 hygiene: `selftest.py --limits --lang` 4/4 ok; ASCII.
- Q9 ratchets: ratchet_tokens raised for 6 roles, process_ratchet_tokens for 12, native_headroom for 3; driver-exits
  `unwalked` +12 by name. All named; `judgment-census.json` untouched.
- Q10 architecture: see F5.
- Q11 judgment: no check added, so `judgment: none` holds. No `<!-- kind: craft -->` marker added. Placement point: F6.
- Q12 ONE ROAD: `values_rename` goes to the 9 Bash roles only. That is FR-2 / E-10, and the 3 no-Bash roles get their door
  through TBW-T1rc-site, a node that has not been entered (F4). No language or project exclusion was added (grep of the diff
  for language or runner names: none).

## Trail

Read: spec r3 whole; builder report whole; critic.md rules 21-23; `stage_joints.py:895-937`; `validate_artifacts.py`
`check_run_report_v0` :2429-2441, `check_bug_filing_header` :427-441, `check_result_rows` :2443-2473 (grep);
`check_witness.py:228-256`; constants `UNDERSTANDING_MAX_LINES`/`TEST_REPORT_MAX_BYTES` (:1760-1761), `THEN_QUOTE_MAX`
(`manual_evidence.py:40`), `MIN_WITNESS_LEN` (`check_witness.py:70`); the charter diffs; the section structure of
`qa-scout.md` and `qa-code-critic.md`; `agents/*.md:4` tools lines; the driver-exits, inject-map and role-load diffs;
the slices diff (removed lines); `plans/piles/told-before-work/batch-1-finish.md:19,38-40,49`.

Re-runs (worktree `.claude/worktrees/agent-a1bfa3bfdead0ba50`, HEAD `541bec6b`, clean):
- `t1rc_keys.py <wt>` (taken verbatim from spec :619-673) -> `FAIL ra-2 ... | t1rc keys: 108 checked, 1 failed` (ra-2 dropped
  by the Lead). With `--negative` -> 109 checked, 3 failed (NEG fires twice).
- `stage_joints.py --check` -> `REJECT — 2 finding(s)` (F1 + the expected unsited finding).
- `dry_exits.py --check` -> `raised 243 row(s) above the base 39 ... | 0 discrepancies`.
- `contract_slices.py --check` -> `44 declared, all present and fresh; 20 key pages`.
- `role_rules.py --check` -> `457 rows, 546 carriers checked, 0 finding(s)`.
- `selftest.py --limits --lang` -> `4/4 ok`.
- My own scripts (scratchpad `rows.py`, `exact.py`, plus inline): row diff 273 -> 285, 12 added, 0 removed, 34 changed, no
  top-level key changed; 46 row keys exact and 17 doors exact; 12 new rows match §4.1; 61/61 role-row page lines present;
  2 of 264 page-told producers carry demands.

```json
{
  "verdict": "blocker",
  "blockers": [
    "F1: stage_joints.py --check at 541bec6b prints a second finding: exit_gate:case_identity producer[0]: qa-case-designer is not told '= the file name'. The M2 row went page-told and kept demands ['= the file name'], which the cd-1 text lacks; the DoD forbids any finding besides unsited"
  ],
  "fixes": [
    "F1: stage-joints.json row exit_gate:case_identity producers[0].demands -> [] (or a token the cd-1 text holds); this is a spec exception to R-3 and needs the Lead's word; then re-run stage_joints.py --check: the unsited finding must be the only one",
    "F2: re-run the witness once after all edits and attach the stage_joints --check tail verbatim; the reported '1 finding' tail does not reproduce at 541bec6b",
    "F3: the old sentences of check_run_report_v0 (blocked vs env_blocked), check_bug_filing_header (non-empty cases vs cases: [] with no_case_reason) and check_result_rows (case or test id vs names ONE case) contradict the appended clauses (E-8): a line for node TBW-T1rc-ec8, or the Lead allows replacing them in this round",
    "F4: the Lead enters nodes TBW-T1rc-int, TBW-T1rc-site and TBW-T1rc-ec8 into plans/piles/told-before-work before the merge to main",
    "F5: name AR-11 and AR-22 too; write the process_ratchet_tokens raises per role in the E-9 form (minor)",
    "F6: optional Lead decision: move the key-procedure K lines (ts-2b, ts-3a, cd-2k, cd-3, ck-4a, fa-1ak, br-2k, ra-3k) from Techniques to Tools and raise the process ratchet by measure"
  ],
  "class_completeness": "F1 class (a demand token on a row whose told carrier moved to the page): all 4 M2 rows walked, only case_identity is red. F3 class (an appended clause contradicting the old sentence): 30 appended rows walked against the report's E-4 list, 3 found. Axis 38 census covered (12 rows, 12 raised_by). Axis 18 raises named. Axis 34 covered by ROLE+ and family rows. Siblings TBW1-11 and TBW1-12 not missed: the card text stays told until -b (E-2: Not yet in rows on 12 pages). The missed reader is stage_joints._demands_leg (F1)",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-told-before-work-t1r-cards-spec-r3.md",
      ".claude/worktrees/agent-a1bfa3bfdead0ba50/docs/tasks/specs/reports/20261117-tbw-t1r-cards-a-report.md",
      ".claude/agents/critic.md:178-287",
      "ai-packages/qa-factory/scripts/stage_joints.py:895-937",
      "ai-packages/qa-factory/scripts/validate_artifacts.py:427-441,1760-1761,2429-2473",
      "ai-packages/qa-factory/scripts/check_witness.py:70,228-256",
      "ai-packages/qa-factory/agents/*.md (diff, tools lines, section markers)",
      "git diff origin/main...541bec6b (stage-joints.json via script, slices, driver-exits, inject-map, role-load, changelog)",
      "plans/piles/told-before-work/batch-1-finish.md:19,38-40,49"
    ],
    "reruns": [
      {"command": "python -B t1rc_keys.py <worktree>", "result": "FAIL ra-2 (dropped by the Lead); t1rc keys: 108 checked, 1 failed"},
      {"command": "python -B t1rc_keys.py <worktree> --negative", "result": "109 checked, 3 failed (NEG fires twice)"},
      {"command": "python -B ai-packages/qa-factory/scripts/stage_joints.py --check", "result": "REJECT - 2 findings: exit_gate:case_identity demand '= the file name' not told; unsited 11 vs 17"},
      {"command": "python -B ai-packages/qa-factory/scripts/tests/dry_exits.py --check", "result": "raised 243 above base 39; 0 discrepancies"},
      {"command": "python -B ai-packages/qa-factory/scripts/contract_slices.py --check", "result": "44 declared, all present and fresh; 20 key pages"},
      {"command": "python -B ai-packages/qa-factory/scripts/role_rules.py --check", "result": "457 rows, 546 carriers, 0 findings"},
      {"command": "python -B ai-packages/qa-factory/scripts/selftest.py --limits --lang", "result": "4/4 ok"},
      {"command": "scratchpad exact.py / rows.py (row diff, exact texts, new-row shapes, page lines)", "result": "12 added, 34 changed, 46 row keys + 17 doors exact; 61/61 role-row page lines; 2 page-told producers carry demands"}
    ]
  }
}
```
