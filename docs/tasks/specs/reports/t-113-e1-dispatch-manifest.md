# t-113 E1 report: dispatch_manifest siblings + designer form check

Worktree: C:\QAFactory\forge-repo\.claude\worktrees\agent-ab34f93d7b2e3d9ba (nothing committed).
Edited: tools/dispatch_manifest.py, tools/test_dispatch_manifest.py, tools/test_dispatch_cut.py, this report.

## Behaviour items (spec E1)
1. KEY_GROUPS + siblings (`siblings?|neighbou?rs`), designer: DONE.
2. Templates derive items from KEY_GROUPS (`_expected_forms()`, `ITEMS`, display names); first sentence of each byte-identical: DONE (pinned in a test).
3. SECTION_STOP_RE gains `siblings?|neighbou?rs|designer`: DONE.
4. `section_extent(cut, sec)` added, `_section_paths` calls it (behaviour unchanged): DONE.
5. `check_cut`: siblings form check (every checked dispatch) and designer check (over threshold), each a missing item in the INCOMPLETE text: DONE.
6. `designer_threshold(cut) -> (owns_count, items_count)`, `ITEM_EXCLUDED_SECTIONS` (F-E7: dod not in; given, owns, non-goals, handoff, edges, siblings, designer), `DISPATCH_FORM_REFUSES = True`, `DESIGNER_THRESHOLD = 3`: DONE. Module stays pure.

## Choices I made where the spec was silent (please confirm or overrule)
- `DISPATCH_FORM_REFUSES = False` => neither siblings nor designer is checked (no note). The spec names the switch, not its False behaviour.
- `designer:` is read over its extent (tail + continuation lines, unquoted), like siblings: so `designer:` then a path on the next line passes. Accepted forms: `skip -- <reason>` / `skip \u2014 <reason>` (non-empty reason), `resubmission t-<digits>`, an absolute path (via path_candidates). `designer: skip` with no reason, `resubmission` with no id, a relative path: missing.
- `designer: skip -- r` passes with a note `DESIGNER-SKIP: ... a dispatch_skipped(agent=designer) event is owed (CLAUDE.md rule 2).` (`DESIGNER_SKIP_NOTE_TEMPLATE`); the spec said "the note says ...", wording is mine.
- Missing labels: siblings -> `no line` / `empty` / `bare none`; designer -> `no line` / `empty` / `no absolute path, 'skip -- <reason>' or 'resubmission t-<id>'`.
- siblings tail text that is not a bare `none` is an entry, including `none of these` (no separator) -- spec: "any non-empty tail text other than a bare none".
- Siblings continuation "path candidate" uses `path_candidates(line)` with NO top_entries (module is pure): an absolute path or a backticked span with a slash counts; a bare relative `tools/x.py` in a non-bullet prose line does NOT (bulleted/numbered lines and `axis N` do). QUESTION for Lead: is that the intended reach, or should the gate (E2) pass top_entries? check_cut cannot list the root.
- `manifest-skip:` items now accept `siblings` and `designer` (ITEMS-derived).

## Findings (not fixed, for the Lead)
- Named limit has a real consequence: fixture K3 contains the bullet `- neighbours once at the end: ...` inside its DoD section; it is now read as a siblings header and ends the DoD section above it, so K3 is refused for `DoD` as well as `owns`. I pinned that in test K2/K3 (`["owns","DoD"]`). Real dispatches with a prose bullet "Neighbours ...:" / "Designer ...:" inside DoD will be falsely refused for DoD; a door (manifest-skip) exists.
- K1 and K7 (real prompts) carry 3+ numbered items, so the designer line is owed for them; tests updated.
- `tools/dispatch_gate.py:1873-1878` `_UNCHECKED_NOTE_FALLBACK` copy of UNCHECKED_NOTE_TEMPLATE now differs (node E2 owns dispatch_gate.py; test `test_unchecked_note_fallback_template_equals_the_modules` is red for this reason).
- `tools/hop_metrics.py:189` `_manifest_lines` repeats the stop rule (docstring only seen; FG7-29 owns it; not edited): it will not stop at siblings/designer until FG7-29 updates it.
- tools/dispatch_gate.py main()-level text: `docs/tasks/specs/t-090-dispatch-manifest.md` pins the old template wording (docs only, historical).

## Sibling sweep (fix-the-class)
Neighbours in the artifact: test_dispatch_cut.py `_REST` and P2c prompt (updated, they build complete dispatches); test_dispatch_manifest.py PARTS (siblings added); every other builder-complete fixture in reader tests (see below) is the same class and not mine.

## Reader tests (not edited) -- QUESTION
`python -m pytest tools/test_owns_gate.py tools/test_handoff_gate.py tools/test_dispatch_gate.py`: test_handoff_gate.py all green. test_owns_gate.py 13 red, test_dispatch_gate.py 87 red = 100 failures, all one cause: their "complete builder dispatch" fixtures have no `siblings:` line, so the dispatch is now refused (`Missing: siblings (no line)`) and, for owns_gate, nothing is registered (e.g. `FileNotFoundError ... owns_registry.jsonl`). One more cause: `test_unchecked_note_fallback_template_equals_the_modules`. Examples: `test_owns_gate.py::test_decide_bold_marker_writes_declared_paths_to_sidecar` (`assert None is not None`), `test_dispatch_gate.py::test_main_full_manifest_builder_exit_0_silent` (`assert 2 == 0`, message "Missing: siblings (no line)"). The spec says "a reader test red for a reason outside E1's owns is returned as a question": who owns the fix of these 100 rows (add a `siblings:` line to their shared builders)? test_dispatch_gate.py is E2's; test_owns_gate.py is not in E1's or E2's owns as the spec lists them (estimate, not checked against other nodes).

## Verification (witness)
Owned files only:
`python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_cut.py -q --tb=short` -> `293 passed in 3.43s`
Plus handoff reader: `python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_cut.py tools/test_handoff_gate.py -q` -> `351 passed in 6.04s`
The DoD command as written (all five files):
`python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_cut.py tools/test_owns_gate.py tools/test_handoff_gate.py tools/test_dispatch_gate.py -q --tb=no`
closing line: `100 failed, 635 passed in 23.19s` (all 100 failures in test_owns_gate.py / test_dispatch_gate.py, see above; DoD NOT green as written).

Table: `FORM_ROWS` in test_dispatch_manifest.py (one parametrized table, 51 rows: siblings 26, designer 16 owns/line rows, 9 numbered-item rows). The refused rows are the negative control (e.g. `sib-absent`, `sib-bare-none`, `des-3-owns-no-line`). F-E7 rows as corrected: `des-3-items-only-in-dod` REFUSED, `des-3-items-only-in-edges` passes. test_dispatch_cut.py: `test_section_extent_ends_at_the_first_blank_line_never_past_the_next_header` (5 rows) and `test_stop_at_siblings_keeps_the_owned_paths_above_it`.

## Needed beyond the manifest
Fixtures tools/fixtures/dispatch_manifest/K1-K7 (read to explain K1/K2/K3/K7); md_regions-free; reader test files' failure output.
