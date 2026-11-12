# t-113 E1 code review (critic, diff gate): dispatch_manifest siblings + designer form check

Under review: the uncommitted diff in `C:\QAFactory\forge-repo\.claude\worktrees\agent-ab34f93d7b2e3d9ba`
(worktree HEAD 25174f7; files `tools/dispatch_manifest.py`, `tools/test_dispatch_manifest.py`, `tools/test_dispatch_cut.py`,
`tools/test_owns_gate.py`, `tools/test_dispatch_gate.py`, `tools/dispatch_gate.py` (one literal); no fixture file changed).
Spec: `docs/tasks/specs/fg-context-and-hygiene.md` §6 E through E1, the two Lead acceptance sections (F-E7 = (b) narrowed).

**Verdict: NEEDS WORK** -- 2 blocking findings (B1, B2), 8 non-blocking (F1-F8). The acceptance decision is the Lead's.

## Control runs (verbatim closing lines)

1. The DoD set (cheap control of the round-2 witness):
   `python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_cut.py tools/test_owns_gate.py tools/test_handoff_gate.py tools/test_dispatch_gate.py -q -p no:cacheprovider` (cwd = worktree)
   -> `735 passed in 31.25s` (matches the round-2 witness `735 passed in 38.13s`).
2. Readers of `dispatch_manifest` OUTSIDE the DoD's five (found by grepping `tools/*.py` for `dispatch_manifest` / `DoD:` / `edges:`):
   `python -m pytest tools/test_owns_gate_retry.py tools/test_owns_gate_md.py tools/test_dispatch_gate_md.py tools/test_wiring_check.py tools/test_r3_integration_check.py tools/test_owns_verify.py tools/test_hop_metrics.py tools/test_dod_track.py -q -p no:cacheprovider --tb=line`
   -> `3 failed, 399 passed in 118.48s`:
   `FAILED tools/test_owns_gate_md.py::test_decide_normal_declaration_registers_and_no_warn`,
   `FAILED tools/test_dispatch_gate_md.py::test_dod_quoted_warn_still_reachable_with_a_verification_header_and_a_fenced_dod`,
   `FAILED tools/test_dispatch_gate_md.py::test_write_manifest_dod_quoted_warn_silent_on_a_full_form_dispatch`
3. `python -m pytest tools/test_exam_runner.py tools/test_collect_intake.py tools/test_negative_lint.py tools/test_md_regions.py tools/test_journal_echo_escalation.py tools/test_journal_echo_noteslen.py tools/test_journal_validator_merge.py tools/test_hook_liveness_probe.py -q -p no:cacheprovider --tb=line`
   -> `5 failed, 521 passed, 34 warnings in 156.67s`: all five in `tools/test_hook_liveness_probe.py`
   (`test_first_run_has_no_claim_folder_and_the_gate_creates_it`, `test_full_probe_run_from_another_cwd_is_ok_on_the_post_merge_settings`,
   `test_live_run_of_all_cases_is_ok`, `test_main_cli_exit_code_zero_on_live_gates`, `test_main_cli_json_flag_produces_parseable_json`);
   `test_live_run_of_all_cases_is_ok` -> `'name': '2-dispatch_gate-in-process-owns-registration', ... 'verdict': 'MISMATCH'` with the INCOMPLETE text.
4. `python -m pytest tools/test_agent_budget.py tools/test_mechanism_gate.py -q -p no:cacheprovider` -> `570 passed in 14.02s`.
5. Attribution of 2-3 (pure read, `dm.check` on the two fixtures' prompts: `test_owns_gate_md.py:261-268` and
   `hook_liveness_probe._complete_builder_prompt`): both -> `siblings (no line)`. The `test_dispatch_gate_md.py` failures show
   `assert (2, 'DISPATCH... -- <reason>') == (0, '')` on `_FORM_NO_DOD + "DoD: ..."` (`:289-292`), a full six-key form with no siblings line.
6. Probe battery (pure read; `dispatch_manifest.check` on dispatch shapes, results quoted in the answers below).

## Blocking

**B1. Readers outside the DoD's five go red, and the live liveness probe breaks; the round-2 claim "the probe still matches" is false.**
Evidence: control runs 2, 3, 5. `tools/hook_liveness_probe.py:633-646` `_complete_builder_prompt` builds the "COMPLETE builder dispatch"
used by case `2-dispatch_gate-in-process-owns-registration`; it has no `siblings:` line, so the gate now refuses it and the probe
reports MISMATCH (5 tests red; on the live path the probe itself would report the gate as broken after the merge). Round 2's report
says "hook_liveness_probe.py: pins only anchor ... the probe still matches" -- it checked the anchor text, not the probe's complete
payload. Same cause in `tools/test_owns_gate_md.py:261-268` and `tools/test_dispatch_gate_md.py:289-292` (`_FORM_NO_DOD`, used at
`:318` and `:325`). The DoD named five files; the reader set of `dispatch_manifest` is wider (16 files import it or build its form),
so the DoD set was green while the CI canon would be red (8 failures).
Fix (this round, same merge): add `"siblings: none -- a probe fixture\n"` to `hook_liveness_probe.py:645` (one owned path: below the
designer threshold, no `designer:` needed); add a `siblings:` line to `test_owns_gate_md.py:266` and to `_FORM_NO_DOD`
(`test_dispatch_gate_md.py:291`). Witness: the three files plus `test_hook_liveness_probe.py`. Class: "a fixture that builds a
COMPLETE writing dispatch" -- the scan above found these three carriers beyond round 2's; the Lead should extend the E1 DoD with
`tools/test_owns_gate_md.py tools/test_dispatch_gate_md.py tools/test_hook_liveness_probe.py`.

**B2. A well-formed `siblings:` block with repo-relative paths on the continuation line is refused, and labelled "empty".**
Probe: `siblings:` + next line `tools/owns_gate.py, tools/handoff_gate.py` -> `code=2 missing=[siblings (empty)]`; the same paths on
the tail (`siblings: tools/owns_gate.py, ...`, row `sib-paths`) pass; bulleted pass; backticked (`` `tools/owns_gate.py` ``) pass.
Code: `tools/dispatch_manifest.py` `_siblings_state`, the continuation test
`_BULLET_OR_NUMBER_RE.match(line) or path_candidates(line) or _AXIS_RE.search(line)` -- `path_candidates(line)` with no
`top_entries` does not read a bare relative path. Siblings are repo-relative by nature (the spec's own carrier list is relative; the
refusal hint says "paths or 'axis N'"), so the gate refuses exactly the entry form its own hint asks for, breaking the §6 invariant
"never refuses a well-formed line", and the label `empty` lies about a non-empty line. The spec's entry definition is "holds a path
candidate"; it did not mean "an absolute or backticked path only" (the builder flagged it as a question; it is not answered by the spec).
Fix: in `_siblings_state` also accept a continuation line holding a relative path token, a pure regex such as
`(?<![\w/])[\w.-]+/[\w./-]*[\w-]` or a word with a file extension (`\b[\w-]+\.[A-Za-z]{1,5}\b`), keeping plain prose ("the usual ones")
refused; add the row `sib-empty-relative-path-line` (pass). Purity is kept (no root listing needed).

## Non-blocking (fix this round unless the Lead queues it)

- **F1 (question d): the new keys turn common prose into headers that cut an existing section.** Probe: DoD header, then
  `- neighbours once at the end: run the reader tests`, then the command -> `missing=[DoD (empty)]`; the same bullet after the command
  passes. K3 (a real dispatch) hits it. The spec names the limit ("ends the section above it"), so the builder followed the spec; but
  the limit now contradicts the invariant for an OLD item (DoD), and "neighbours"/"designer"/"sibling" open prose lines often in this
  repo's own node texts (grep of `docs/tasks/**`, `plans/piles/**`: e.g. "Neighbours on this surface: ...", "designer п. 4: ...",
  "Sibling specs: ...", "Sibling not red but worth a look: ..."), and node texts are pasted into builder dispatches. Proposal (spec
  edit, Lead decides): for the two NEW keys only, a header is a bare declaration -- only a parenthetical / markup between key and colon
  (`_GAP_RE`, already in the module, used by `unsure_reason`); `Siblings (axis 13):` stays a header, `neighbours once at the end:` and
  `Siblings of X:` do not. `SECTION_STOP_RE` keeps stopping owns at them (precedes-kept edge unchanged). K3 returns to `["owns"]`.
- **F2 (question e): no end-to-end row proves a missing `siblings:` is refused through `dispatch_gate`.** `test_dispatch_gate.py` never
  calls `_manifest(siblings=None)` (grep: the only `siblings` hits are the defaults at `:59`, `:73-74`, `:516`, `:1645`, `:2971`);
  `test_owns_gate.py` likewise. Add one gate row: `decide_full(_builder_payload(_manifest(siblings=None)))` -> code 2, message contains
  `siblings (no line)`, and (owns_gate) nothing registered. No test I read passes for the wrong reason: the defaults add lines AFTER
  the DoD line, `suffix=` carries only skip lines / extras (`:1964`, `:2584-2586`), and no assertion was edited (diff read).
  Side effect to know: every gate fixture now carries `designer: skip -- a test fixture`, so no gate-level test runs without a
  designer line; harmless below the threshold, but the gate-level designer rows belong to E2's test list (spec E2 "Tests").
- **F3 (question c): `DISPATCH_FORM_REFUSES = False` makes both checks silent.** `check_cut` (`if item == "siblings": state = ... if
  DISPATCH_FORM_REFUSES else None`) emits nothing, so flipping the switch in an incident violates the §6 invariant "never goes out
  silently" (FR-4: a check stops a silent pass, not an informed one). Fix: with the switch off, compute the states and append one note
  ("SIBLINGS/DESIGNER NOT ENFORCED: ... missing: ...") to `skip_notes` instead of refusing; one row.
- **F4: the threshold number is hard-coded in the refusal text.** `_FORM_HINTS["designer"]` says "from 3 owned paths or 3 numbered
  items" while `DESIGNER_THRESHOLD = 3` is the constant; build the hint from the constant (AR-1).
- **F5 (question b, the refusal text's door): say what triggered the designer line.** The 5-item fix-round probe gets
  `Missing: designer (no line)` and the generic hint; a Lead sending a numbered "The fixes" list does not learn that those five lines
  are what counted. Make the label carry the counts: `designer (no line; 1 owned path, 5 numbered items)`. The door itself is named
  (`designer: resubmission t-<id>` is exactly the right one for a fix round, plus `manifest-skip:`).
- **F6 (question c): bare-none synonyms pass as entries.** `siblings: n/a`, `siblings: -`, `none, standalone`, `none: standalone`,
  `none of these` all pass. `n/a` and `-` are the bare-none class (no reason) and pass only by the letter of "any non-empty tail";
  `none, ...` / `none: ...` carry a reason with a separator the grammar does not list. Proposal: treat `n/a`, `-`, `—` like bare
  `none` (refused), and accept `,`/`:`/`;` as separators of the reason form. Lead decision (closed grammar of the spec); a data tuple, not
  more regex branches.
- **F7 (brief item 6, duplication): two copies of the extent walk and three copies of the separator set.** `_section_paths` re-walks
  the extent (header tail, skip quoted) that `_extent_lines` now provides -- it should call `_extent_lines`; the separator `--|—`
  lives in `_SKIP_SEP_RE`, `_NONE_WITH_REASON_RE` and `_DESIGNER_SKIP_RE`. Outside the diff: `tools/hop_metrics.py:187-196`
  `_section_lines` is now a verbatim clone of `section_extent` (its docstring says "queued to become one function there" -- the
  function now exists); FG7-29 owns it: a one-line replacement `range(sec.header_line, dm.section_extent(cut, sec) + 1)`, queue it on
  FG7-29. It does NOT break on rollout: it iterates `cut.sections.values()`, so the new sections are already counted as manifest.
- **F8 (brief item 7, quality):** `check_cut` now carries two `if item == ...: continue` special cases inside the generic item loop;
  acceptable at this size, but a third item should become a per-item checker table. No dead branches; `_idx` unused names only.
  The `UNCHECKED_NOTE_TEMPLATE` join (`KEY_GROUPS[:-1]` + "and" + last) is fine; the `dispatch_gate._UNCHECKED_NOTE_FALLBACK`
  literal copy is the pre-existing pinned-twin pattern (test keeps them equal).

## Answers a-f

**a. Behaviour 1-6 and edges.** 1 KEY_GROUPS: met (`test_templates_list_every_item...` pins ITEMS). 2 templates derived, first sentence
byte-identical: met (`_EXPECTED_INCOMPLETE` verbatim row; prefix pins for all three). 3 SECTION_STOP_RE: met
(`test_stop_at_siblings_keeps_the_owned_paths_above_it`). 4 `section_extent` + `_section_paths` calls it: met (5-row extent test;
behaviour unchanged -- the old in-loop blank-line break is exactly the new bound). 5 check_cut: met, both items named with their
form (FORM_ROWS 51 rows). 6 `designer_threshold`, `ITEM_EXCLUDED_SECTIONS` (dod out, edges in, per F-E7), `DISPATCH_FORM_REFUSES`:
met (`test_designer_threshold_counts`, `test_module_constants_of_the_form_check`, rows `des-3-items-only-in-dod` refused,
`des-3-items-only-in-edges` passes). Edges: non-writing -> `test_non_writing_dispatches_get_neither_check` (scout/critic/designer);
degraded -> `test_degraded_cut_is_unchecked_note_never_a_refusal_for_the_new_items`; fence -> `sib-in-fence`, `des-3-owns-in-fence`;
relative designer path -> `des-3-owns-relative-path`; prose "Siblings ...:" after owns -> `sib-prose-after-owns-paths` and
`test_prose_siblings_line_after_owns_paths_keeps_every_owned_path`. All met, each with a row. Pure: yes -- the new code calls only
`path_candidates`/regexes over the cut; no stat, no listing (the designer path's existence is E2's stat, temporal per the spec).

**b. Invariants and real shapes.** Reading dispatches are never refused for these lines (probes: critic/scout/designer, handoff-only
general-purpose with 3 numbered questions -> pass; a critic prompt with an absolute `owns:` is refused, but that is the pre-existing
"writing dispatch" rule, not E1). Sufficiency is never judged (`none of these`, prose tails with paths pass). Wrong refusals found:
B2 (relative paths on the continuation line), F1 (prose "neighbours ...:" bullet inside DoD cuts the DoD). Shapes that pass as they
should: `siblings:` with a prose tail holding paths -> pass; DoD with `(a)-(d)` items -> pass and not counted (only `^\s*\d+[.)]\s`
counts); `**siblings**: none -- x`, `## Siblings:` + bullet -> pass; `designer: resubmission t-113@dev1` / `T-113` -> pass.
Refused by the closed grammar (correct per spec, the text names the forms): `designer: skip - small`, `designer: skip: small`,
`designer: resubmission of t-113`, `designer: none -- fix round`, `1. siblings: x` (numbered items are not header prefixes -- the
existing grammar for all keys). The 5-item "The fixes" prompt without `designer:`: refused `designer (no line)`; the door is named
(three forms + `manifest-skip:`), but see F5 for what triggered it.

**c. The builder's calls.** FORM_REFUSES False -> nothing: wrong, F3 (silent pass). `designer:` over its extent: right -- the one
extent definition the spec mandates for "the designer line", and `designer:` + path on the next line is a natural form.
DESIGNER-SKIP wording: right -- names the owed `dispatch_skipped(agent=designer)` and rule 2, quotes the reason, goes to the Lead
note only on a pass. `none of these` as an entry: right by the spec's letter ("any non-empty tail text other than a bare none"); the
weaker cases are F6. Relative `tools/x.py` in plain prose under an empty tail not counting: wrong, B2 -- the purity worry does not
force it, a relative-path regex needs no root.

**d.** See F1: acceptable only as a stopgap; a cheap guard exists in the module (`_GAP_RE` bare-declaration for the two new keys) and
removes the K3 regression; frequency is real (K3 is a real dispatch; node texts in this repo open lines with these words often).
Spec edit -> the Lead's call; recommended this round.

**e.** No assertion weakened (diff read: only fixture defaults, three bypassing literals, `_SKIP_LINE` widened so skip-note tests still
describe a fully skipped dispatch). But no end-to-end gate row for a missing `siblings:` remains -- F2.

**f. Rollout.** Placing E1 on the live path refuses every writing dispatch lacking `siblings:` (K7, a real well-formed dispatch, is now
refused) and every one over the threshold lacking `designer:`. SAME merge as E1: B1's three fixture fixes including
`hook_liveness_probe.py:645` (otherwise the probe reports the gate broken and CI canon is red); the dispatch habit of the Lead (the
refusal text names the door, so a re-send costs one turn -- acceptable per §6 (a)). The spec puts E4 (CLAUDE.md R11-f gains the two
lines) in wave 3, after C2: between E1's merge and E4's, CLAUDE.md R11-f lists six header lines while the gate demands eight -- a rule
text that contradicts its gate. Recommend the Lead either land the R11-f row edit with E1's merge (it is one row; C2 touches a different
section of CLAUDE.md, "Command hygiene") or hold E1's merge until E4; and node P's check 1 (c) with E1's merge as §7 already says.
CAN follow: `hop_metrics._section_lines` (F7, not broken), role files (designer rule 1 points to R11-f, per E4), E2's stat of the
designer path and the NOTE block.

**Duplication and consistency (brief 6):** F7 -- `_section_paths` vs `_extent_lines`; the separator set x3; `hop_metrics._section_lines`
clone (FG7-29). Checked: grep of `tools/*.py` for `dispatch_manifest`, `section_extent`-like loops in `hop_metrics.py`.
**Code quality (brief 7):** F4, F8; no function over 60 lines in the new code (`check_cut` grew by 14 lines; new helpers are 10-25 lines).
**Judgment (brief 11):** none moved -- FORM only; the threshold counts shapes (owned paths, numbered lines), never content.
**One road (brief 12):** the siblings check reaches builder and general-purpose writers alike (probe P18); no exclusion found. The tail
vs continuation asymmetry for relative paths (B2) is a two-roads defect inside one section; fixed by B2.

## Class completeness (SIBLING_MAP axis 13: readers of the manifest grammar)
Readers named by the spec: `owns_gate` (green, imports SECTION_STOP_RE), `handoff_gate` (green), `dispatch_gate` (green with round 2),
`hop_metrics` (green, clone queued F7). Readers NOT named by the spec and broken: `hook_liveness_probe` + its test, `test_owns_gate_md`,
`test_dispatch_gate_md` (B1). `agent_budget`, `mechanism_gate`, `owns_verify`, `owns_gate_retry`, `wiring_check`, `r3_integration_check`,
`dod_track`, `exam_runner`, `collect_intake`, `md_regions`, journal tests: green (runs 2-4).

## Needed beyond the manifest
`tools/hook_liveness_probe.py`, `tools/test_owns_gate_md.py`, `tools/test_dispatch_gate_md.py`, `tools/hop_metrics.py`, and the
reader test runs 2-4 (to check axis 13 beyond the DoD's five files).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: readers outside the DoD set go red (8 tests): hook_liveness_probe.py:633-646 _complete_builder_prompt lacks siblings -> live probe case 2 MISMATCH; test_owns_gate_md.py:261-268; test_dispatch_gate_md.py:289-292. Round-2 claim that the probe still matches is false.",
    "B2: dispatch_manifest._siblings_state refuses 'siblings:' + a continuation line of repo-relative paths (tools/owns_gate.py) with the false label 'empty'; breaks the never-refuse-a-well-formed-line invariant."
  ],
  "fixes": [
    "B1: add a siblings line to hook_liveness_probe.py:645, test_owns_gate_md.py:266 and _FORM_NO_DOD in test_dispatch_gate_md.py:291; extend the E1 DoD with those three test files",
    "B2: accept a relative path token (pure regex) on a siblings continuation line; add row sib-empty-relative-path-line",
    "F1: for the two new keys only, a header must be a bare declaration (_GAP_RE); Lead decides the spec edit",
    "F2: one dispatch_gate row with _manifest(siblings=None) refused and nothing registered",
    "F3: DISPATCH_FORM_REFUSES False emits a note instead of a silent pass",
    "F4: build the designer hint from DESIGNER_THRESHOLD",
    "F5: the designer missing label carries the owned-path and numbered-item counts",
    "F6: n/a and - as bare none; comma/colon/semicolon as reason separators (Lead decision)",
    "F7: _section_paths calls _extent_lines; one separator constant; queue hop_metrics._section_lines -> section_extent on FG7-29",
    "f: land the CLAUDE.md R11-f row with E1's merge or hold E1 until E4"
  ],
  "class_completeness": "Axis 13 (manifest grammar readers): spec-named readers green; three unnamed readers broken (hook_liveness_probe, test_owns_gate_md, test_dispatch_gate_md) -> B1; hop_metrics clone queued to FG7-29 (F7); 12 other reader test files green.",
  "trail": {
    "read": [
      "worktree git diff HEAD of the six files",
      "docs/tasks/specs/fg-context-and-hygiene.md lines 8-37, 334-419",
      "docs/tasks/specs/reports/t-113-e1-dispatch-manifest.md",
      "docs/tasks/specs/reports/t-113-e1-round2.md",
      "tools/dispatch_manifest.py 148-400 and the new functions",
      "tools/hook_liveness_probe.py 630-650, 1005-1022",
      "tools/hop_metrics.py 187-211",
      "tools/test_dispatch_gate_md.py 289-331",
      "tools/test_owns_gate_md.py 259-273",
      "docs/tasks/critic-diff-brief.md items 6, 7, 11, 12",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_cut.py tools/test_owns_gate.py tools/test_handoff_gate.py tools/test_dispatch_gate.py -q", "result": "735 passed in 31.25s"},
      {"command": "python -m pytest tools/test_owns_gate_retry.py tools/test_owns_gate_md.py tools/test_dispatch_gate_md.py tools/test_wiring_check.py tools/test_r3_integration_check.py tools/test_owns_verify.py tools/test_hop_metrics.py tools/test_dod_track.py -q", "result": "3 failed, 399 passed in 118.48s"},
      {"command": "python -m pytest tools/test_exam_runner.py tools/test_collect_intake.py tools/test_negative_lint.py tools/test_md_regions.py tools/test_journal_echo_escalation.py tools/test_journal_echo_noteslen.py tools/test_journal_validator_merge.py tools/test_hook_liveness_probe.py -q", "result": "5 failed, 521 passed in 156.67s (all in test_hook_liveness_probe.py)"},
      {"command": "python -m pytest tools/test_agent_budget.py tools/test_mechanism_gate.py -q", "result": "570 passed in 14.02s"},
      {"command": "dm.check on the test_owns_gate_md fixture and hook_liveness_probe._complete_builder_prompt", "result": "siblings (no line) for both"}
    ]
  }
}
```
