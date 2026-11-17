# t-979 — topic critic, told-before-work finish, wave A (T4a, T5r, T6, T7a-A, T7b, T7c)

Critic (Opus). Spec and DoD: `docs/tasks/specs/20261117-told-before-work-finish-spec.md` (cards, EC-1..EC-8, S-2, Lead decisions F-1..F-9, the owner's word on Q-O1). Rows: `references/stage-joints.json` and `wave0-rows.md` item 1. The diffs were read as `git diff origin/main...<head>`, and the trees were treated as read-only.

## Verdict per node (my input to the Lead's acceptance; the decision belongs to the Lead)

| node | verdict | must land before the merge |
|---|---|---|
| T7a-A (t-964) | **fit** | — |
| T7c (t-967) | **fit_with_fixes** (F7, F8) | no |
| T6 (t-963) | **fit_with_fixes** (F5) | no |
| T7b (t-966) | **fit_with_fixes** (F3, F4) | no |
| T4a (t-965) | **fit_with_fixes** (F1, F6, F9) | no (F1 must land before T4b merges) |
| T5r (t-970) | **fit_with_fixes** (F2, F10) | no |

No finding moves the `unsited` count or a printed byte, so the integrator number in K7 holds whether or not the fix rounds land.

## Findings

**F1 (T4a, K6) — the A24 key parser and the wide scan disagree about what a wrapped site is.** `refusal_registry._key_text` (T4a tree :1076-1092) unwraps only `refusal(<str Constant>, X)` called by the bare name. The wide scan's `_record_kind`/`_record_id` (:1330-1350, binding :1463-1470) also accept `DV.refusal(...)` (a module alias), `from detector_verdict import refusal as R`, a module-constant id, and `with_check(X, "<id>")`.
- Failure scenario: `stage_guard.py:80` imports `detector_verdict as DV` (and already calls `DV.spoken` at :770). If T4b writes `deny(DV.refusal("stage_guard:SG-…", text))`, the A24 key becomes `DV.refusal('stage_guard:SG-…` and `refusal_registry --check` goes red again, the same 68-violation class that round 2 fixed.
- Fix: key through the same recogniser as the wide scan (one reader, AR-13). The minimum is to accept an `ast.Attribute` whose `attr == "refusal"` and a module-constant id. Add one parameterised row to the fast `test_refusal_registry.py` covering bare / alias / attribute / non-literal id. Today the unwrap is proved only by `--check` 68 → 0 on the real tree.

**F2 (T5r) — the `s5_precheck:plan` row is sited on the wrong findings, and its own body is left bare.**
- The row reads: "On a plan-form S5, the window's tests match its slice of the plan, unless a `deviations[]` row … declares the difference".
- The findings that state exactly that are `_Window.add` (`s5_precheck.py:4447-4448`). Its callers are :4483, :4493, :4508, :4511, :4518, :4526, :4538, :4547 and :4554, all "undeclared deviation (C1/C2/C3/C12/C13)". They stay `_plan_finding` and bare.
- Only the plan-missing, plan-unreadable and form-unreadable findings carry the row (:4581-4600).
- The report's E6 line calls `_Window.add` "(code) … no row listed". That is false: the row exists.
- Every caller of `add` states the same requirement, so the Lead's EC-2 reading (t-964 answer: "both callers carry one requirement") puts the literal in `add` itself. That is the same reading T6 applied to `bad`/`refuse`/`_text_of`.
- Fix: `self.findings.append(_sited("plan", case, DV.refusal("s5_precheck:plan", message), fix, tag))`, plus one test row on a C1 deviation in `test_s5_precheck_sides.py`. `plan_result` (:4359-4374: the plan dispatch's own findings, another requirement) stays bare with a correct E6 class.

**F3 (T7b × T7c, K7 seam) — after the merge, the S3 exit relabels obligation lines.**
- `validate_plan` returns `errors + validate_obligations(...)` (`planning_contract.py:214`). After T7c, those items are `coverage_contract:obligations*` Records.
- T7b's `gate_plan_errors` wraps every line again with `refusal("planning_contract:plan", error)`.
- `refusal()` rebuilds from `str(problem)` (`detector_verdict.py:158-162`: `with_check(Record(text), check)`), so the outer id wins. The T7c id and its sentence never reach the in-process readers of `gate_plan_errors` (`gate_preflight.py:1918`, `variant_errors` :2012/:2018).
- T7b already applies the opposite policy, keeping the inner id, in `_branch_block_lines`. That gives two policies for one nesting case in one file.
- Fix: in `gate_plan_errors`, keep a line that already has a check (`error if getattr(error, "check", "") else refusal("planning_contract:plan", error)`), the same policy as `_branch_block_lines`. Add one `tbw_t7b_sites` row with a v2 row and a bad obligation, expecting `coverage_contract:obligations`.
- Not blocking: no transport prints these Records today.

**F4 (T7b, K4) — the report's EC-2 reasoning contradicts its own placement.** The report gives "`validate_plan` has 7 callers, so no literal" as the reason. Yet `gate_plan_errors`, which carries the literal, has three callers (gate_preflight:1918, variant_errors, _detector_body:4495). The placement is right under the Lead's invariant reading (one requirement for every caller). Fix: one report line that states that reading. No code change.

**F5 (T6, EC-8) — the rename failure sits under `handoff_check:cli`, and its sentence and door do not fit.** At `main` :3203-3208 the values file cannot be renamed (OSError). The `cli` row says "The call names an existing UTF-8 form … `--shorten` only with `--fix`", with the door "run `handoff_init` again". The problem's own door is "delete <values>". The id follows the rows data (`wave0-rows.md:65` lists "rename failure :3088-3091" under `cli`), so the builder was right to follow it. The mismatch is missing from the report's EC-8 list, and the report marks the site "N". Fix: one EC-8 line for T1r-cards-R. No code change.

**F6 (T4a, code quality) — a copy-pasted block in new code.** `big_read_check` (T4a diff :81-90) carries the same three-line f-string twice: once bare for the picture/PDF branch and once inside `refusal(...)`. Fix: build `text` once, then `block(text)` or `block(refusal("guard_pre_tool:PT-big-read", text))`.

**F7 (T7c, tests) — the commit has no `tests-over:` line.** The diff has +62 test lines against +49 product lines, and the report itself says "commit hook only WARNed". Fix: add the line in the fix-round commit.

**F8 (T7c, duplication) — `validate_obligations` repeats the literal 37 times.** `refusal("coverage_contract:obligations", …)` is copied on every append (diff :25-194). T6 uses one closure for the same shape. Fix: a local `bad = lambda text: errors.append(refusal("coverage_contract:obligations", text))`. The scanner still sees one literal (`unsited` is unchanged), and wave A ends up with one form.

**F9 (T4a, test hygiene) — the provocation helper does not clean up after itself.** `t4a_provoke` calls `use_project(root)` and never restores `CLAUDE_PROJECT_DIR` or `hooklib._PROJECT_ROOT_CACHE`, and `cleanup(root)` is not in a `finally`. Once T6, T7b and T7c are merged into the same `main()`, whichever function runs next inherits a deleted project root. Fix: try/finally plus a restore, following `t1rs_sites` (:871, :1012-1014).

**F10 (T5r, report) — the E6 list is not enumerated.** "unlisted helper sites in manifest_put" names no site. My AST scan of the bare text raises found:
- `_retract_obligations:891`
- `_retract_instances:943,953`
- `_retract_unresolved:988,994`
- `_merge:1938,1940`
- `_fold_step:1996,2000`
- `read_fragment:2284,2292`
- `_refuse_unmergeable:2227`

None of them is the `retract` row (that row is about the `retract` key). Fix: list each with its class.

## The keys

**K1 — text unchanged.** I read every hunk of T6, T7b, T7c, T7a-A and T4a, and the T5r hunks :354-433, :743-770 and :958-1057. Every site keeps the form `refusal("<id>", <same expression>)`.
- Restructured but identical: T4a `handoff_values_check` (local renamed to `problem_text`), T4a `big_read_check` (text split by branch, identical), T7b `gate_plan_errors` (same order: filtered errors + ours + unmarked), and T5r `_plan_finding` → `_sited("plan", …)` (`_plan_finding` is `_finding("plan", …)`, :4307-4308).
- The only output that changes is intended: T4a's stderr gains `expected:`/`door:`/`check:` after the text, through `hooklib.block` → `spoken`, and T5r's finding dicts gain `told` as the last key.

**K2 — `told` is last.** The only JSON carrier is T5r's `_sited` (`out.update(told_fields)` after `_finding`).
- Keys added later are moved behind it: `pair_at` (:1838 plus `_told_last`), `_judge_words` (`refused`, `message`) and `passed_by_judge` (`level`, `judge`).
- A grep for every other key assignment or dict copy in `s5_precheck.py` found only those. The positive control `\]\["…"\] =` found :1838.
- The widening stayed within the Lead's limit: two `_told_last(...)` wraps, labels unchanged.
- `manifest_put` only attaches `records` to `_MergeRefused`. Its printer in `run()` is not owned, so no JSON key is added there.

**K3 — leaving T6's transports alone is right for this wave.** The mech spec's AR-18 (`20261113-…-mechanism-spec.md:51`) says detector form lines stay byte-identical and expected/door travel only through in-process transports to roles (`block`/`deny`/`refuse`, :93, :166). `handoff_check`'s stdout and `--json` are none of those, and K11/K12/K-A16 lie outside the owns.
- No later card in the finish spec carries a `handoff_check` text/JSON transport. T6's Records (like T7a/T7b/T7c, T5r's `manifest_put` records and the `print(refusal(...))` sites in T6 `cli` and T7b `plan_json`) therefore have no reader of `expected`/`door` until a transport exists.
- The same goes for the counter: it counts a literal as sited "in a transport or not" (`refusal_registry` T2-8, :1511-1513).
- Proposal, for the Lead to decide: either open a node "handoff_check refusal transport + re-pin K11/K12/K-A16", or write one spec line saying these families are told by the page only. Without one or the other, this is a hole in the spec.

**K4 — EC-2 is applied as the invariant, inconsistently.** The Lead's rule (t-964 note): a helper keeps the literal when every caller states one requirement.
- T6 (`bad`, `refuse`, `_text_of`): matches the rule.
- T7a-A (`check_cell_counts`): matches.
- T7b: the placement in `gate_plan_errors` matches, but the stated reason does not (F4).
- T5r: `_Window.add` breaks the rule (F2).
- Proposal: the Lead restates the EC-2 text by that invariant, for the wave B cards.

**K5 — the two bare sites.**
- T6 `rows is None` (:1354; triage unreadable, and no row owns that requirement) and T4a picture/PDF (the PT-big-read door says `Grep -n`, offset/limit, while that branch says "do not try offset/limit"): both are right as bare plus a row split. Rows belong to T1r-cards' file.
- My AST/regex scans found no other unreported bare site in the six files, apart from F2 and F10.
- Lines for the Lead to put in «Остатки»:
  - `row handoff_check:null_outcome.triage (triage unreadable) | узел: TBW-T1rc`
  - `row split guard_pre_tool:PT-big-read.picture/.pdf with own doors | узел: TBW-T1rc`
  - `EC-8 lines of wave A (T6 null_outcome.failures/binding, claims blank, _text_of, rename→cli; T7b plan sentence; T7a-A check_case_form; T4a PT-owner door addressed to a role while owner_check refuses the orchestrator) | узел: TBW-T1rc`

**K6 — see F1.** `_expr_key` (:1322) and the wide scan bind ids through `_record_kind`, and they do not disagree with each other. `_key_text` is called once (:1270, the narrow A24 scan of `SCANNED`), so the other nodes' files (`handoff_check`, `planning_contract`, …) are unaffected. `test_doctor_context.py:582-610` (slow) reads `sites()` keys and `_covers`; it is judged by the canon.

**K7 — seams and the number.**
- Four nodes append to `test_detector_verdict.py`. Names are disjoint:
  - T4a: `tbw_t4a_sites`, `t4a_provoke`, `t4a_digest`, `T4A_OLD`
  - T6: `tbw_t6_sites`, `T6_OLD`
  - T7b: `tbw_t7b_sites`
  - T7c: `tbw_t7c_sites`, `_t7c_row`, `_t7c_ob`, `T7C_OLD`
- All four add a call after `t1rs_sites()`, and T4a, T6 and T7c insert at the same anchor. Expect three textual conflicts at merge. Resolve each by keeping both sides.
- The sited sets are disjoint by file stem. Measured: T6 −21, T7b −12, T5r −25, T7a-A −13 (control re-run: 106), T7c −2, T4a 0. That gives 119 − 73 = **46**. The spec's 45 counted T7a-A as −14, a slip: 13 + 10 + 19 = 42.
- After all six merge, the integrator sets `told_ratchet.unsited` = 46 and `UNSITED_CAP = 46` at `test_stage_joints.py:927`, and the pin tuple at :932 becomes `(46, 46, 46, [], True)`.
- Note: `_is_sited` counts a sub-id as sited through its parent literal (T7c report :26). The counter therefore does not watch `required_rows.*` (T6) or `branches.new_questions` (T7b) on their own; only their test rows do. This is accepted by the Lead for T7c, and the same holds class-wide.

**K8 — siblings (SIBLING_MAP axes 17 and 34; axis 38 is not written yet, T10).**
- F1 bears on T4b (`stage_guard`'s `DV` alias), and T4b's card does not name it.
- T7a-B/C call `check_cell_counts` (already sited by A). They must not re-wrap those errors, because of the outer-wins rule in F3.
- `validate_plan`'s other callers (`controller.py` 3258/5487/7618) stay bare. T9a's card covers only the six controller rows, so this is an E6 remainder.
- The EC-8 lines go to TBW-T1rc (K5). I found nothing else wave A should have touched.

**K9 — tests.** Each node adds one table function in an existing keep file, with no new test file (diffstats).
- The old values are the pre-change outputs from byte copies: T6 and T4a as digests, T7b, T7a-A and T7c as literals. Sentences are read from rows through `told_text`.
- `tests-over:` is present in five commits and missing in T7c (F7).
- T7b's `plan_json` row spies on `refusal` because the Record dies at `one_line`. That is acceptable under T2-8, and K3 notes the class.

## Standing questions

- Fit to the spec: yes, apart from F2 and F3.
- The builders' own decisions: safe in direction, except F2.
- Seams: K7 and F3.
- Class: F1, K4, K8.
- DUPLICATION AND CONSISTENCY: F8 and F6, plus two nesting policies in F3. Grepped: `refusal(` forms, `with_check`, `_record_kind`, `_key_text`/`_expr_key`.
- CODE QUALITY: F6 and F9. No new function over 60 lines in product code; the test tables are long by design, with `tests-over:` named.
- ARCHITECTURE: AR-9, AR-13, AR-18 and AR-29 are named in all commits. F1 touches AR-13 (a second recogniser).
- JUDGMENT: none moved. No census edit, no `blocks_override`.
- ONE ROAD: none found. Grepped the diffs for language, runner and project names; every node uses `refusal()` only, with no hand-built Record.
- IN-TREE RATCHETS: no raise. `told_ratchet`, the K12 pin and `told-ratchet.json` are untouched (they belong to the integrator).
- Hygiene: changelog fragments are ASCII. `--lang` is green per the reports (not re-run).

## Trail

- Read: the spec (whole); `critic-diff-brief.md`; the six diffs in full (T5r partly, ranges above); `detector_verdict.py` :90-234 (origin/main); `refusal_registry.py` :60-100, :1076-1110, :1235-1300, :1318-1350, :1452-1530 (T4a tree); `test_doctor_context.py` :575-610; the `harness.py` `use_project`/`cleanup`; `s5_precheck.py` :4307, :4355-4376, :4436-4450 (T5r tree); the rows of the cited ids in `stage-joints.json`; `wave0-rows.md` (grep); the T6, T7b and T4a reports; the T5r, T7a-A and T7c reports (grep); journal lines 2432 and 2437; the commit trailers of the seven heads; the SIBLING_MAP axis headings.
- Ran:
  - `stage_joints.py --check` in the T7a-A tree → `unsited 106`, `clean`.
  - An AST bare-append/`Problem` scan over the owned functions. Positive control: the same script on origin/main `check_case` printed the bare appends at :164/:170/:172.
  - Grep for key assignments in `s5_precheck.py`, with the :1838 control.
  - A grep of `manifest_put` raises.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "F1: the A24 key parser (_key_text) recognises fewer refusal call shapes than the wide scan (_record_kind): DV.refusal, aliases, module-constant ids and with_check are missed, and T4b (stage_guard imports detector_verdict as DV) would turn A24 red; fix before T4b. F3: refusal() rebuilds a Record with the outer id winning, while T7b's _branch_block_lines keeps the inner id: two policies; after the T7b+T7c merge gate_plan_errors relabels coverage_contract obligation Records. EC-2 is applied by the invariant in T6, T7a-A and T7b and broken by T5r _Window.add (F2). EC-8 lines and two row splits go to TBW-T1rc. Integrator number after all six merge: unsited 46.",
  "fixes": [
    "T4a F1: refusal_registry._key_text must recognise the same refusal call shapes as _record_kind (attribute DV.refusal, alias, module-constant id), plus one parameterised row in test_refusal_registry.py; lands before T4b merges",
    "T4a F6: big_read_check builds the message once; block(text) on the picture/PDF branch, block(refusal(id, text)) otherwise",
    "T4a F9: t4a_provoke restores CLAUDE_PROJECT_DIR and hooklib._PROJECT_ROOT_CACHE and calls cleanup in a finally (precedent t1rs_sites)",
    "T5r F2: s5_precheck _Window.add (:4447) builds DV.refusal('s5_precheck:plan', message) through _sited; one C1-deviation test row; fix the E6 class line",
    "T5r F10: the report enumerates the bare manifest_put raises (retract helpers, _merge, _fold_step, read_fragment, _refuse_unmergeable) with their class",
    "T7b F3: gate_plan_errors keeps a line that already carries a check (same policy as _branch_block_lines); one tbw_t7b_sites row with a bad obligation expecting coverage_contract:obligations",
    "T7b F4: report line states the EC-2 invariant reading (gate_plan_errors has three callers)",
    "T6 F5: report EC-8 line: the rename failure under handoff_check:cli has a sentence and door that do not fit",
    "T7c F7: tests-over line in the commit message",
    "T7c F8: one local closure for the coverage_contract:obligations literal instead of 37 copies"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-told-before-work-finish-spec.md",
      "docs/tasks/critic-diff-brief.md",
      "git diff origin/main...5062977d / e2d88c49 / 7b307f21 / 5d2b73d2 / ed9fb587 / 2d84d1f1",
      "ai-packages/qa-factory/scripts/detector_verdict.py:90-234 (origin/main)",
      "agent-a201e90fdcd751f88 refusal_registry.py:60-100,1076-1110,1235-1300,1318-1350,1452-1530",
      "agent-a201e90fdcd751f88 tests/test_doctor_context.py:575-610, tests/harness.py use_project/cleanup",
      "agent-a150f3676d6fec08e s5_precheck.py:4307,4355-4376,4436-4450",
      "references/stage-joints.json rows of the cited ids",
      "docs/tasks/specs/20261113-told-before-work-wave0-rows.md (grep), mechanism spec (grep C9/transport)",
      "reports 20261117-tbw-t6/t7b/t4a (whole), t5r/t7a-a/t7c (grep)",
      "logs/journal/dev1.jsonl lines 2432, 2437",
      "docs/SIBLING_MAP.md axis headings 17, 18, 34, 37"
    ],
    "reruns": [
      {"command": "python -B agent-a0853e07e1c62ebd6/ai-packages/qa-factory/scripts/stage_joints.py --check", "result": "told counters: hand_cards 12, legacy_legs 0, unsited 106; stage joints: clean"},
      {"command": "AST bare-append/Problem scan over the owned functions (positive control: origin/main check_case)", "result": "control printed :164/:170/:172; T7a-A owned clean; T6 bare only :1354; T5r owned clean, _Window.add and plan_result bare"},
      {"command": "grep for finding key assignments in s5_precheck.py (control ][\"..\"] =)", "result": "only :1838 pair_at and :308 _told_last"}
    ]
  }
}
```
