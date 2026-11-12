# t-113 E1 round 3 report (escalated fix round on the critic verdict t-113-e1-code.md)

Worktree `C:\QAFactory\forge-repo\.claude\worktrees\agent-ab34f93d7b2e3d9ba`, uncommitted, nothing committed. The shell cwd was never changed.

## Items

1. **B1 -- DONE.** A `siblings: none -- ...` line was added to three fixtures: `hook_liveness_probe._complete_builder_prompt` (its docstring now names siblings and says why no designer line is owed: 1 owned path), `test_owns_gate_md.py::test_decide_normal_declaration_registers_and_no_warn`, and `test_dispatch_gate_md.py::_FORM_NO_DOD`. None of them is over the designer threshold, so none needs a `designer:` line. The reader search is listed below.
2. **B2 -- DONE.** New `_REL_PATH_RE`, a pure regex: one or more `segment/` followed by a last segment with an extension, or a trailing slash for a folder (`and/or` and `tools/x` are not paths). `_siblings_state` accepts it on a continuation line. Rows: `sib-empty-relative-path-line` (comma-separated), `-spaces`, `-backticked`, `sib-empty-relative-folder-line` (all pass); `sib-empty-prose-with-slash-word` and `sib-empty-prose-dir-without-ext` (refused). The module still does no I/O.
3. **F1 -- DONE.** New `_is_header(line, m)` in `section_cut`. For the keys in `_BARE_HEADER_ITEMS = ("siblings", "designer")`, a line is a header only when the gap between the key word and the colon passes `_GAP_RE.fullmatch`. The six older keys always return True, so their grammar is unchanged. `SECTION_STOP_RE` is unchanged, so owns still stops at such a line. The K3 DoD verdict is back to pre-E1 and the named-limit pin is removed. New rows:
   - `sib-bullet-prose-inside-dod-not-a-header` (the K3 shape: DoD header, then `- neighbours once at the end: ...`, then the command -> passes)
   - `sib-header-with-parenthetical` and `sib-header-bold` (pass)
   - `des-prose-key-not-a-header` (refused: no designer line)
   - `des-header-with-parenthetical` (passes)

   The module docstring now states this rule.
4. **F2 -- DONE.** `test_dispatch_gate.py::test_builder_without_siblings_line_is_refused_end_to_end_and_passes_with_it`: through `dispatch_gate.decide`, `_manifest(siblings=None)` gives exit 2, and the message starts with the INCOMPLETE first sentence and contains `Missing: siblings (no line).`. The same dispatch with the line gives `(0, "")`.
5. **F3 -- DONE.** Both items are always computed (`_form_missing`). With `DISPATCH_FORM_REFUSES = False`, any still-missing siblings/designer item that no skip line waives goes into a note, never a refusal. The note uses the new `FORM_NOT_ENFORCED_NOTE_TEMPLATE`: `SIBLINGS/DESIGNER NOT ENFORCED (DISPATCH_FORM_REFUSES is off): this dispatch went out missing {items}; add the line(s) in the form the INCOMPLETE text names.` The wording is mine, from the critic's proposal; the Lead may change it. The six older items are still refused, and the refusal names only them. Row: `test_form_switch_off_still_checks_both_items_and_notes_them`.
6. **F4 -- DONE.** The designer hint takes `% (DESIGNER_THRESHOLD, DESIGNER_THRESHOLD)`. **F5 -- DONE.** The label names the count that triggered the line, e.g.:
   - `designer (no line; over the threshold by 5 numbered items)`
   - `... by 3 owned paths`
   - `... by 3 owned paths and 3 numbered items`

   The three accepted forms are still in the Expected part. Row: `test_designer_refusal_names_the_triggering_count_and_the_three_forms` (it also pins the threshold text from the constant).
7. **F6 -- DONE.** `_BARE_NONE_WORDS = ("none", "n/a", "-", "–", "—")`, a data tuple that builds `_BARE_NONE_RE`, refused as `bare none`. `_NONE_ANSWER_RE` = `none` + one of the spec's separators (`--`, `—`, `.`, `(`), and it passes only when the reason contains a `\w` character. `none, x`, `none: x` and `none of these` are unchanged: they pass as entries, because the Lead did not decide on the extra separators. Rows: `sib-bare-na`, `sib-bare-na-upper-dot`, `sib-bare-hyphen`, `sib-bare-emdash`, `sib-none-reason-no-word` (`none -- -`), `sib-none-empty-bracket` (`none ()`) are refused; `sib-hyphen-then-path` (`- tools/x.py`) passes. The door test is `test_the_siblings_door_names_the_none_with_reason_form`.
8. **F7/F8 parts inside the owns -- DONE:**
   - `_section_paths` now reads through `_extent_lines`, so there is one extent walk.
   - One separator constant, `_SEP = r"--|—"`, feeds `_SKIP_SEP_RE`, `_NONE_ANSWER_RE` and `_DESIGNER_SKIP_RE`.
   - F8: the two `if item == ...: continue` special cases left the generic loop. They are now one `_FORM_ITEMS` skip plus `_form_missing`, `_designer_trigger` and `_items_text`.

   **Not touched, for the Lead:** `tools/hop_metrics.py:187-196` `_section_lines`, a clone of `section_extent` (F7, FG7-29).

## Reader test files (item 1 search)

The search ran over `tools/` with the Grep tool:
- test files naming `dispatch_manifest|dispatch_gate|owns_gate|handoff_gate|hook_liveness_probe` (21 files);
- production importers of those modules (`agent_budget`, `critic_snapshot`, `hop_metrics`, `owns_verify`, plus the gates), and the test files of those importers;
- multiline literals with `owns...:` ... `DoD|verification...:`, case-insensitive (10 files).

Positive control: the first form (`owns:` ... `DoD:`) missed `hook_liveness_probe.py`, whose header is `owns (ABSOLUTE write paths):`. The widened pattern found it.

Complete-dispatch literals found outside the earlier fixes: only the three B1 fixtures. `test_owns_gate_retry.py` and `test_handoff_gate.py` matched the literal pattern but stayed green.

| set | files | result |
|---|---|---|
| DoD `-k` run | test_dispatch_manifest, test_dispatch_cut, test_dispatch_gate, test_dispatch_gate_md, test_owns_gate, test_owns_gate_md, test_owns_gate_retry, test_handoff_gate, test_hook_liveness_probe (+ `-k` matches elsewhere) | 1032 passed |
| missed by `-k` | test_warn_messages, test_warn_density, test_transcripts, test_p4_stdin_deadline, test_negative_lint, test_mechanism_gate, test_hygiene_gate, test_hop_metrics, test_enforcement_probe, test_dod_track, test_critic_snapshot, test_agent_budget, test_owns_verify, test_wiring_check, test_r3_integration_check | 1632 passed |

No red file outside the owns, so there are no questions.

One flake: the first DoD run went concurrently with the "missed" run and got 1 failure, `test_hook_liveness_probe.py::test_main_cli_exit_code_zero_on_live_gates` (`assert 1 == 0`). The test passed alone (2 passed with its `--json` twin). The full DoD re-run, with nothing else running, was 1032 passed. My reading: both runs drove live gate state at the same time. That is an inference, not proven.

## Changed expectations (old -> new)

- `test_dispatch_manifest.py::test_K2_K3_relative_owns_paths_are_blocked_on_owns_only`: K3 `["owns", "DoD"]` -> `["owns", "siblings"]` (item 3; K2 unchanged `["owns", "siblings"]`). The named-limit comment is replaced.
- FORM_ROWS `sib-prose-after-owns-paths`: `[]` -> `["siblings"]` (item 3: `Siblings of X:` is no longer a header, so the dispatch has no siblings line; the owned paths above it are still kept).
- `test_form_switch_off_checks_neither_item` -> renamed `test_form_switch_off_still_checks_both_items_and_notes_them`: `== (0, "", "")` -> `(0, "")` plus the NOT ENFORCED note text (item 5).

No test was deleted or skipped. The three templates' first sentences and the six older keys' grammar are unchanged; `_EXPECTED_INCOMPLETE` still passes verbatim.

## Analogs noticed (not edited)

- `tools/hop_metrics.py` `_section_lines` (F7, above). It also repeats the stop rule (`_manifest_lines`). Because of F1, a prose `Siblings of X:` line is no longer a cut header but still a `SECTION_STOP_RE` stop. hop_metrics counts by `cut.sections`, so it follows the cut automatically.
- `tools/dispatch_gate.py` passes the check's note to the Lead. The new NOT ENFORCED note travels the same road as the skip notes. No code change was needed, and none was made (E2 non-goal).

## Needed beyond the manifest

`tools/fixtures/dispatch_manifest/K3.txt` (read), the production importers' import lines (grep), `tools/test_quarantine.py` (to confirm the `tools/` tests are not quarantined: it reads only the package's `test-layers.json`).

## Witness

`python -m pytest C:/QAFactory/forge-repo/.claude/worktrees/agent-ab34f93d7b2e3d9ba/tools/ -q -k "dispatch or owns_gate or handoff or liveness" --rootdir C:/QAFactory/forge-repo/.claude/worktrees/agent-ab34f93d7b2e3d9ba -p no:cacheprovider --tb=short`
```
1032 passed, 7039 deselected in 49.33s
```
`python -m pytest <worktree>/tools/test_warn_messages.py test_warn_density.py test_transcripts.py test_p4_stdin_deadline.py test_negative_lint.py test_mechanism_gate.py test_hygiene_gate.py test_hop_metrics.py test_enforcement_probe.py test_dod_track.py test_critic_snapshot.py test_agent_budget.py test_owns_verify.py test_wiring_check.py test_r3_integration_check.py --rootdir <worktree> -q -p no:cacheprovider --tb=short` (absolute paths)
```
1632 passed in 98.30s (0:01:38)
```
Owned files alone (`test_dispatch_manifest.py test_dispatch_cut.py`): `313 passed in 2.04s`.
