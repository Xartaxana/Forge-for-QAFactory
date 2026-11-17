# t-1091 — code review of T9c (TBW1-11): the conductor's launch section "What code will check in this launch"

Commits under review, in tree `C:/QAFactory/forge-repo/.claude/worktrees/agent-a8e7e4c769ef59136`: `0defa3ed` (builder t-1079), `f75c63a0`
(follow-up t-1087). Files were read at HEAD `d440db2c` (a merge of origin/main). Spec: card T9c and "Lead decisions on T9c at the build"
in `docs/tasks/specs/20261117-told-before-work-finish-spec.md`, mech §2.8-§2.9. Paths below are relative to `ai-packages/qa-factory/` in
the tree W unless a path is given in full.

## Verdict

**ACCEPT WITH FIXES.** No finding blocks the merge. F1-F3 are wrong or missing told text in the rows: fix them before merge in one fix
round. Under EC-8 the Lead accepts a row sentence, so the three proposed sentences below go to the Lead first. F4 is a one-line FR-1 fix
in an owned function. F5 is queued. N1 and N2 are proposed nodes. The coordinator of the proper tier opens them; I do not.

## Findings

**F1 (fix before merge): the `no_move:args` row claims more than `check_args` checks, and in the same prompt it says the opposite of
`rework_args_list`.** Location: `references/stage-joints.json:8226` (row `no_move:args`). The row says the args name "the work to redo as
one kind only: cases ..., plan row ids (S1-S3), or bug candidates ...". That means one kind is required. `check_args`
(`scripts/no_move.py:238-280`) accepts S1-S3 args that name none of the three. Probe:
`check_args({'stage':'S2','role':'qa-test-strategist','cause':'test_defect'}, facts)` returned `({... no cases/rows ...}, '')`, so it was
accepted. The same prompt also prints `rework_args_list` (`no_move.py:233`), which is in the moves section above the new one:
`rows (S1-S3, instead of cases, or neither)`. One requirement is now told twice in two wordings that disagree (P31 / key 1). Proposed
sentence (the Lead accepts it, EC-8): "... a cause from the list, and at most one kind of work to redo: cases inside the approved scope (at
least one from S4 on), plan row ids (S1-S3, where none is also accepted), or bug candidates the story lists (S7 only, instead of cases)."
Test: add a row `"none-at-S2": ({}, "S2", True)` to `ARGS_KINDS` (`scripts/tests/test_controller_doors.py:282-290`). The present check
`args-row` (`:313`) only tests that words are present, so it passes the over-claim.

**F2 (fix before merge): `no_move:options` does not tell the whole `story` requirement.** Location: `references/stage-joints.json:8145`.
The row asks for "a `story` object". `validate_options` (`no_move.py:489-491`) refuses an object whose `unverified`/`report`/`delivery`
are all empty or `none`, because `story_line` returns `''`. Probe: options with `"story": {}` and `"story": {"unverified": "none"}` were
refused: `the option \`retry\` lacks its says / factory / person / story lines (story is a dict)`. A conductor that obeys the row is
refused (FR-38, AR-10). Proposed wording: "... and a `story` object with at least one of `unverified`, `report`, `delivery` that is not
empty or `none`." Add one `REFUSALS` row.

**F3 (fix before merge, small): an empty question is refused with a bare text, and no row tells it.** Location: `no_move.py:389`
`return "the question is empty"`, a branch of `prose_refusal`. The report (§2) labels it "E6 (code)". That label is wrong: the input is
the conductor's own answer, so this is a launch-known refusal (§2.8 O1) that the conductor is never told in the launch. Fix: site it as
`DV.refusal("no_move:prose", "the question is empty")`, keeping the text byte-identical, and start the row sentence (`:8172`) with "The
question is not empty and names, ...". The `refusal-text/empty-question` row then expects id `no_move:prose`. Another option: the Lead
keeps it bare and gives a reason that holds. "(code)" is not that reason.

**F4 (fix, one line): the refusal for a `ROLE_FILES` role names the wrong expected file.** Location: `scripts/stage_joints.py:704-705`.
When `references/conductor.md` is missing, the refusal says "role `conductor` has no agents/conductor.md", but `agents/` was never what
it looked for (FR-1: it must say what it expected). Fix: `f"role \`{r}\` has no {ROLE_FILES.get(r, f'agents/{r}.md')}"`. Rows for
`agents/` roles keep their text byte for byte.

**F5 (queue): the sentence "stage-joints.json `joints` is not a list" is written twice.** Locations: `no_move.py:320-321` re-checks the
shape that `stage_joints._rows_data` (`stage_joints.py:463-464`) already checks, with the identical sentence. Why it happened: the builder
could not add a public `(rows, why)` reader, because `stage_joints.py` was owned only for `_producer_leg`. Queue it for the next node that
owns `stage_joints.py`: one public reader that returns the reason, and `moves_section` calls it.

**N1 (proposed node; the residual of Q1/Q3, key 6).** Location: `no_move.py:283`. The heading `## What code will check in this launch`
reads as a complete list. When a rework is open, the code also checks the command the move runs (`controller:rework.call/.args/
.runner_half/.cap`, and others, 14 rows in all). None of them is listed until a siting node lands, so on a rework launch the section
implies more completeness than it has. `NOTHING_CHECKED` (`:284`, "code checks nothing of this launch beyond your answer's form above")
claims completeness outright. It is unreachable with the real file, because the three `conductor_answer` rows always hold. It would be
false if those rows were ever dropped while command rows stayed unsited. The Lead decision says these wait for "a siting node", but no
node id or owner is named. Rule 19: open the node (owner: Lead of told-before-work, pile TBW) with the 14 command rows +
`planning_contract:plan.unmarked_revision`. Until it lands, the gap is known and in the report. It does not block T9c.

**N2 (proposed node; class completeness, key 8, P31 / AR-15).** Mech §2.9 says: "every driver conductor launch carries it". In the
code, two driver conductor launches do not go through `moves_section`:
- `driver_conductor.py:807-826` `no_move_legacy` (kind `s1_review`, `NM.EXCLUDED_KINDS`, `no_move.py:37`) launches with the site's text
  only. Its answer is still judged by the `no_move:class` requirement at `driver_conductor.py:203` (`PO.question_rule`). That launch is
  told the requirement only by the static `references/conductor.md:99` ("Without a `why_person` class or with an empty `checked`, it is
  refused once."), which words it differently from the row: one requirement, two wordings.
- `driver_stage_s8s9.py:450-452`: the S8 delivery conductor (`run_claude("conductor", ..., system_file=.../conductor.md)`) gets no
  section. Its answer's `action` is judged (`:465`) and so is its `mr` record (`mr_record`).

The card scoped T9c to `moves_section`, and both sites are outside its owns, so this is not a defect of this diff. It is a spec claim that
does not hold. Proposed node: either the section on both launches (rows whose `when` fits them), or the §2.9 sentence corrected to the
launches it covers, with the exclusion named as such. The `s1_review` exclusion is an exclusion that stays (brief item 12(c)). Its carrier
is `no_move.py:37` with the comment "until C1-3 gives it an executor".

Checked and not a finding:
- `driver_machine.py:2753` and `:3629` call `check_args` bare. Those args are built by code (gate B bug rework, the deferred `retry`), not
  produced by the conductor or a role, so no row is owed there. The builder's EC-2 choice (the id is written at the conductor-facing
  caller) is right.
- `validate_options`' action branch (`no_move.py:466-467`) cannot be reached from the one driver caller, which passes only
  `ask_person`/`stop` (`driver_conductor.py:704`). It is defensive code, and leaving it bare is right.

## Keys

1. **Row ↔ site.** `no_move:class` matches `person_owned.class_rule` (`person_owned.py:95-111`), and the lone chosen-rework exemption is
   covered by "A question". `no_move:prose` covers the vocabulary and site-door tokens but not the empty question (F3). `no_move:options`
   matches every other branch I read (count, lone rework, token unique/non-empty/own, site door, not open, never offerable) but under-tells
   `story` (F2). `no_move:args` claims more than is checked at S1-S3 and contradicts `rework_args_list` (F1). Analogs: driver_conductor:203
   is N2. The driver_machine callers need no row (see above).
2. **One call and its cost.** The only caller of `moves_section` is `driver_conductor.py:692` (`_conductor_text`), so the section enters
   through one seam for the `_no_move` road (the two other launches are N2). Size, measured with `rows_for` + `told_line` on the real file:
   750 chars (3 rows, no rework) or 1133 chars (4 rows, rework open), plus the heading and blank lines, about 40 chars. That is about 200
   or 300 tokens at 4 B/token on every conductor call, and again on the refused re-ask, which re-sends `text`. No ratchet covers the
   conductor prompt: `role-load.json` `process_ratchet_tokens` has rows only for the 12 `agents/*.md`, and `git diff 0defa3ed^ f75c63a0`
   shows no change to `role-load.json` or `told-ratchet.json`. The report does not state the size (AR-12). Here it is.
3. **Refusal form at the converted sites.** `DV.refusal` returns a `Record` whose `str` is the problem only (`detector_verdict.py:149-176`).
   The re-ask (`driver_conductor.py:677`) joins `rule` as a str, and journal/defect sinks (`:422-425`) do too. I found no `spoken`/
   `told_fields` on these paths (grep over driver_conductor, story_run*, driver_machine, no_move). So the texts are byte-identical (EC-1
   battery of 17, plus the `REFUSALS` table). The row's sentence reaches a refused conductor through the section in the re-sent `text`
   (`told_line` → `told_text`), the same composer `refusal()` uses: one source. The exit codes come from `_no_move`, which the diff did
   not touch.
4. **Q5.** Every whole-file failure of `load_rows` gives NOT KNOWN: absent, OSError, not JSON (0 bytes included), not an object, and
   schema mismatch (that is the reader's own branch, not a table row). `joints` that is not a list gives NOT KNOWN too. A readable file
   with no rows gives `NOTHING_CHECKED`. No code reads the section: grep for `WHAT_CODE_CHECKS|NOTHING_CHECKED|What code will check` finds
   only tests and the unrelated page heading in contract_slices, so NOT KNOWN is never a decision. Remaining runtime gap: rows that are not
   dicts, or a broken `when`, are dropped silently and could print `none`. `stage_joints.py --check` guards that at dev time. Note only.
5. **Q2.** `unwalked` is the honest label. The dry gate rows do reach the conductor, and the why string says the joints are reached but
   not judged by a row of their own. The credit is where the ledger's own check expects it: four `raised_by` entries in
   `fixtures/driver-exits/gates.json`, while the group's base stays where it was (the report explains the "stale raise credit" red). I re-ran
   the check: `dry_exits --check: 0 discrepancies`, and the NOTE line lists the four `no_move:*` entries.
6. **Q1/Q3 gap.** What the section lists is true, apart from F1-F3. It implies completeness through its heading, and `NOTHING_CHECKED`
   claims it outright: N1.
7. **Tests.** There is one parameterised table per behaviour: `SECTION_ROWS`, `UNREADABLE_ROWS`, `ARGS_KINDS`, `REFUSALS`, plus junction
   rows (the `none` line, the prompt). Expected values come from mech §2.9/§5.5, from EC-1 (the OLD file's output from a byte copy), and
   from the spec branches. The negative controls in the report kill the new behaviours. Weak spots: `args-row` (`:313`) checks that words
   are present, so it cannot catch F1. `ARGS_KINDS` tests `check_args`, which this diff did not change, as a premise check, and its
   `none-at-S5` row nearly repeats `test_controller_rework_window_words.py:1067-1069` (B-K16): minor, no fix demanded. Census: notes only
   on three `no_move` units, classes and roles unchanged, no change to `blocking_per_role`. `prose_refusal` has no row of its own and
   `test_judgment_census` is green: right. `tests-over:` lines are in both commits, and their reasons (rows per card item, the NOT KNOWN
   table) hold.
8. **Class completeness:** N2. `docs/SIBLING_MAP.md` has no axis 39 yet (grep `^## Axis 39` found nothing at HEAD). The closing wave of
   the spec opens it (finish spec :211), so no axis is owed by T9c.

## Standing questions

- **DUPLICATION AND CONSISTENCY:** F1 (the args requirement in two wordings that disagree: the row vs `rework_args_list:233`); F5 (the
  shape sentence twice); N2 (the class requirement in `conductor.md:99` and in the row). Grepped: `is not a list"` in no_move/stage_joints,
  `references/conductor.md` over scripts (other carriers: driver_conductor:337, driver_stage_s8s9:451; `ROLE_FILES` is a new data constant
  for the walker and does not compete with them).
- **CODE QUALITY:** `moves_section` stays under 60 lines with nesting at most 2. No dead code is added. The comment
  "every launch has the section" (`no_move.py:315-317`) is true only for the `_no_move` road (N2). F4 is a refusal that names the wrong
  file. Nothing else found.
- **ONE ROAD (P31):** N2. The `s1_review` exclusion stays, with its carrier at `no_move.py:37`. The S8 delivery launch takes another road
  for the same action. Both go into a proposed node. Neither is a branch this diff added.
- **TESTS:** key 7. `tests-over:` is present, and the reason holds.
- **ARCHITECTURE (10):** AR-15/AR-17 hold for the `_no_move` road, with one caller. AR-13 holds: `load_rows`, `rows_for` and `told_line`
  are the only readers used. AR-10 is partly broken by F1-F3. AR-28: NOT KNOWN holds (key 4). AR-12: the cost was not stated in the report
  and is measured here (key 2). AR-20: raises are named below.
- **JUDGMENT (11):** no check added. The ids ride the Records and the texts are unchanged. The census rows changed only by `note`.
  `judgment: none` holds.
- **RATCHETS (9), each named:** stage-joints rows 269 → 273 (K1 pin, "+4 T9c conductor rows"); `told_ratchet.unsited` 17 → 17;
  `fixtures/driver-exits/gates.json` `unwalked` credit +4 `raised_by` (227 → 231 per the report; base unchanged; reason "T9c conductor
  rows, 2026-11-17"); `judgment-census.json`: no class or ceiling change; `role-load.json`: untouched.

## Spot-checks (the report's claims, reproduced)

- "unsited 17 → 17, rows 273": re-run, `stage joints: clean ... rows 273 ... unsited 17`.
- "dry_exits 0 discrepancies after Q2": re-run, `dry_exits --check: 0 discrepancies`.
- "the args sentence names every kind check_args accepts": true for the kinds. It is wrong about whether one kind is required (F1, probe).
- "check_args has 3 callers": confirmed by grep (driver_machine 2753, 3629; no_move 494). Positive control: the same grep found the
  `validate_options` call.
- "one caller of moves_section": confirmed by grep over scripts (not tests). The only non-test hit is driver_conductor:692.

## Trail

Read: the report (whole); `git show 0defa3ed`, `git show f75c63a0` (the code, json and census diffs); `no_move.py:200-330, 330-520`;
`stage_joints.py` `load_rows`/`_rows_data`/`rows_for`/`told_text`/`told_line`/`_producer_leg`; `null_outcomes.load_data`;
`detector_verdict.py:95-200` (Record, refusal, spoken); `person_owned.py:95-115`; `driver_conductor.py:185-225, 263-300, 422-490,
625-720, 795-830`; `driver_machine.py:2740-2765, 3620-3640`; `driver_stage_s8s9.py:420-480`; `references/conductor.md` (grep:
why_person lines 75, 91, 99); the four rows in `references/stage-joints.json`; `test_controller_doors.py:230-420`;
`references/role-load.json` head; finish spec card T9c :445-480 and Lead decisions :698-706; mech spec §2.8-§2.9 (:284-313);
`docs/tasks/critic-diff-brief.md`.

Commands (verbatim tails):
```
( cd W/ai-packages/qa-factory && python -B scripts/tests/dry_exits.py --check | tail -1 )
dry_exits --check: 0 discrepancies
python -B scripts/stage_joints.py --check | tail -2
stage joints: walked exit 8, detector 5, window 28 | rows 273, gaps 4 (producer 2, told 1, demands 1), joints held 4 of 273 | ... | told counters: hand_cards 12, legacy_legs 0, unsited 17
stage joints: clean
probe (python -I, W scripts on sys.path):
check_args({'stage':'S2','role':'qa-test-strategist','cause':'test_defect'}, f) -> ({'stage': 'S2', 'role': 'qa-test-strategist', 'cause': 'test_defect'}, '')
check_args({... 'stage':'S5', 'rows':['r1'], 'cases':[]}, f) -> (None, '"args" names no case, and S5 needs at least one of the approved scope')
validate_options(options with story {} / {'unverified':'none'}) -> (None, 'the option `retry` lacks its says / factory / person / story lines (story is a dict)')
size probe: rows_for('conductor',['*'],{'moves':[]}) -> 3 rows, 750 chars; {'moves':['rework_stage']} -> 4 rows, 1133 chars
git diff 0defa3ed^ f75c63a0 --stat -- role-load.json told-ratchet.json judgment-census.json -> judgment-census.json | 6 +++--- (only)
```

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "N2: two driver conductor launches bypass moves_section - no_move_legacy (driver_conductor.py:807-826, s1_review, class rule checked at :203, told only by conductor.md:99) and the S8 delivery launch (driver_stage_s8s9.py:450-452); mech 2.9 'every driver conductor launch carries it' does not hold; outside T9c owns, proposed node. N1: the 14 command rows and unmarked_revision need a siting node with an id. driver_machine check_args callers need no row (code-built args). SIBLING_MAP axis 39 not yet open (closing wave).",
  "fixes": [
    "F1 references/stage-joints.json:8226 no_move:args claims one kind of work is required, while check_args accepts none at S1-S3 and rework_args_list (no_move.py:233) says 'or neither'; reword (Lead accepts, EC-8) and add ARGS_KINDS row none-at-S2 -> accepted",
    "F2 references/stage-joints.json:8145 no_move:options says 'a story object' while no_move.py:489-491 refuses a story whose unverified/report/delivery are all empty or none; reword and add a REFUSALS row",
    "F3 no_move.py:389 'the question is empty' is refused bare and untold; site it under no_move:prose with the text byte-identical and extend the row sentence, or the Lead names a reason that holds (not 'E6 code')",
    "F4 stage_joints.py:704-705 the refusal for a ROLE_FILES role names agents/<r>.md; name ROLE_FILES.get(r, agents/<r>.md)",
    "F5 (queue) no_move.py:320-321 repeats the joints-not-list sentence of stage_joints._rows_data:463-464; one public (rows, why) reader when stage_joints.py is next owned"
  ],
  "trail": {
    "read": [
      "W/docs/tasks/specs/reports/20261117-tbw-t9c-report.md",
      "git show 0defa3ed / f75c63a0",
      "W/ai-packages/qa-factory/scripts/no_move.py:200-520",
      "W/ai-packages/qa-factory/scripts/stage_joints.py load_rows/_rows_data/rows_for/told_text/told_line/_producer_leg",
      "W/ai-packages/qa-factory/scripts/detector_verdict.py:95-200",
      "W/ai-packages/qa-factory/scripts/person_owned.py:95-115",
      "W/ai-packages/qa-factory/scripts/driver_conductor.py:185-225,263-300,422-490,625-720,795-830",
      "W/ai-packages/qa-factory/scripts/driver_machine.py:2740-2765,3620-3640",
      "W/ai-packages/qa-factory/scripts/driver_stage_s8s9.py:420-480",
      "W/ai-packages/qa-factory/references/stage-joints.json no_move rows",
      "W/ai-packages/qa-factory/references/role-load.json",
      "W/ai-packages/qa-factory/scripts/tests/test_controller_doors.py:230-420",
      "docs/tasks/specs/20261117-told-before-work-finish-spec.md card T9c and Lead decisions",
      "docs/tasks/specs/20261113-told-before-work-mechanism-spec.md 2.8-2.9",
      "docs/tasks/critic-diff-brief.md"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/dry_exits.py --check (in W package)", "result": "dry_exits --check: 0 discrepancies"},
      {"command": "python -B scripts/stage_joints.py --check (in W package)", "result": "stage joints: clean; rows 273; unsited 17"},
      {"command": "probe check_args S2 with no work kind", "result": "accepted - row no_move:args over-claims"},
      {"command": "probe validate_options story {} and {unverified: none}", "result": "refused - row no_move:options under-tells"},
      {"command": "size probe rows_for conductor", "result": "750 chars (3 rows) / 1133 chars (4 rows, rework open)"}
    ]
  }
}
```
