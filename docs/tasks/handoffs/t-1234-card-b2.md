# t-1234 Card B2 (FG7-58) -- report

All paths under the integration worktree `C:/QAFactory/forge-repo/.claude/worktrees/wb-int/` (`tools/`). No git state change. No live hook file edited (the ten `.py.next` copies were made by byte copy, then edited).

## Behaviour items

1. Copies: `tools/{dispatch_manifest,dispatch_gate,journal_write,journal_validator,journal_hooks,journal_echo,claim_control_gate,search_control_gate,owns_gate,handoff_gate}.py.next` made with `cp` from the live files (LF files; edits preserved LF).
2. Section 4.1 B2 retargets landed (quoted below). Rows: claim_control 99, search_control 21, handoff_gate 42 -> `CLAUDE.md § Worker duties`; owns_gate 5, journal_write 58/422, journal_hooks 41, journal_validator 17/153/315/679, journal_echo 1526/1541/1574/1815, judge_calib_sanitize 3, calibration_counts 79/494/829, test_journal_echo_escalation 6 -> `COORDINATOR.md`; dispatch_gate 3-5 -> "CLAUDE.md rule 11 ... COORDINATOR.md rule 7".
3. `ROOT_FILES += "COORDINATOR.md"` in `claim_control_gate.py.next`; test row `assert m._in_scope("COORDINATOR.md")` in `test_in_scope_prefixes` (test_claim_control_gate.py).
4. F13 facts header:
   - `dispatch_manifest.py.next`: `FACTS_KINDS = ("designer",)` beside HANDOFF_DIRS; `("facts","facts",r"facts")` appended to KEY_GROUPS (so ITEMS gains `facts`, `manifest-skip: facts -- <r>` is a valid item, one cut); `_FORM_GROUPS` (KEY_GROUPS without facts) now feeds INCOMPLETE_TEMPLATE's expected form and UNCHECKED note, so the builder's form text is unchanged; facts is a bare-header item (`Facts about X:` prose is not a header), is in ITEM_EXCLUDED_SECTIONS and in SECTION_STOP_RE; `check_cut` skips it in the per-item loop; new reader `facts_state(cut)` (None | 'no line' | 'empty' | 'bare none'; extent = tail + lines to first blank line; non-empty passes, `none` passes only as `none -- <word>`; same grammar as siblings).
   - `dispatch_gate.py.next`: `facts_check(payload, cut, dm)` + FACTS_MISSING text verbatim from spec 5.3 (kind formatted in), run in `decide_full` after the handoff block (completeness -> handoff -> facts -> path -> label). Unknowns (no cut, degraded cut, manifest without FACTS_KINDS) = note + pass; waiver = pass with note; non-FACTS_KINDS kind = (0,"","").
   - `dispatch_new.py`: `--facts` (list, one line each under `facts:`); an empty item is refused like given/owns; printed whenever given (any kind); a designer without it is refused by the hook's own decision.
   - Rows added: test_dispatch_gate.py `_FACTS_ROWS` (14 rows: line, block, none-why, no line, empty, bare none, none with empty why, waiver, handoff wins, quoted, prose, degraded, critic untouched, builder untouched) + one test of the unknowns; test_dispatch_manifest.py `_FACTS_STATE_ROWS` (13 rows); test_dispatch_new.py 6 rows (designer ok / none-why / absent / bare none / empty item / builder untouched). Existing pins updated: K6 items text (+facts), ITEM_EXCLUDED_SECTIONS set, ITEMS tuple, `_reading_dispatch` (designer gets `facts: none -- ...`).
5. conftest loader (`tools/conftest.py`): `next_copy_map(environ, tools_dir)` (pure) + `_NextCopyFinder` MetaPathFinder at front of sys.meta_path, installed by `install_next_copies()` at import. `<NAME>_PATH` ending `.py.next` must name an existing file and `tools/<name>.py` must exist, else RuntimeError naming the variable (t-1202 fix 4); `.py` and other values ignored. Rows (test_dispatch_manifest.py `test_next_copy_loader`, 4 cases: next maps, `.py` ignored, missing file loud, no live module loud).

## Witness (one run after all edits; first run before the pin fixes showed 4 failed, all four pins/helper now updated)

Command (subshell in the worktree):
`DISPATCH_MANIFEST_PATH=tools/dispatch_manifest.py.next DISPATCH_GATE_PATH=tools/dispatch_gate.py.next CLAIM_CONTROL_GATE_PATH=tools/claim_control_gate.py.next python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_gate.py tools/test_dispatch_new.py tools/test_claim_control_gate.py tools/test_journal_echo_escalation.py tools/test_dispatch_cut.py tools/test_dispatch_gate_md.py tools/test_owns_gate.py tools/test_handoff_gate.py -q -p no:cacheprovider`

Tail:
```
...............................                                          [100%]
1111 passed in 31.34s
```
`python -B -m py_compile tools/*.py.next` -> `compiled` for all ten files (claim_control_gate, dispatch_gate, dispatch_manifest, handoff_gate, journal_echo, journal_hooks, journal_validator, journal_write, owns_gate, search_control_gate).

Negative control (same facts test selection, NO `*_PATH` variables, so the live files are tested): `python -m pytest tools/test_dispatch_gate.py -q -k facts_check` -> `9 failed, 6 passed, 349 deselected` (the new behaviour exists only in the copy; the loader really swaps it in).

Extra, outside the DoD (live files, no variables): `python -m pytest tools/test_journal_validator.py tools/test_journal_write.py -q` -> `415 passed`. This does NOT judge the journal copies (they are comment/message-text only; their tests were not run through the loader because no `JOURNAL_*_PATH` is in the DoD).

## Live-vs-copy diff stats (`git diff --no-index --stat`)

dispatch_manifest 38+/7-; dispatch_gate 45+/4-; journal_write 2+/2-; journal_validator 4+/4-; journal_hooks 1+/1-; journal_echo 4+/4-; claim_control_gate 2+/1-; search_control_gate 1+/1-; owns_gate 1+/1-; handoff_gate 1+/1-. Live files edited in place (tracked diff): judge_calib_sanitize 1/1; calibration_counts 3/3; test_journal_echo_escalation 1/1; test_claim_control_gate 1+; dispatch_new 7+/1-; conftest 55+; test_dispatch_manifest 56+/3-; test_dispatch_gate 43+; test_dispatch_new 8+.

Changed lines of the comment/text-only copies (each holds `COORDINATOR.md` or `CLAUDE.md §`):
```
journal_write:      # COORDINATOR.md rule 12   |  characters (COORDINATOR.md rule 12); got ...
journal_validator:  spec / COORDINATOR.md's "Routing  |  ...deployment, COORDINATOR.md rule 13), before |  ...rule 13; FG7-16). |  "deployment (COORDINATOR.md rule 13); accept ...
journal_hooks:      # COORDINATOR.md rule 12 (the CLI refuses longer notes; the hook cuts)
journal_echo:       # GAP (R6, COORDINATOR.md "Routing rules", rule 6 here) | (COORDINATOR.md rule 6 / | COORDINATOR.md's Routing log section, | # COORDINATOR.md's typed-fields rule)
claim_control_gate: path by its own builder -- CLAUDE.md § Worker duties, the   (+ "COORDINATOR.md", in ROOT_FILES)
search_control_gate: path by its own builder -- CLAUDE.md § Worker duties, the
owns_gate:          (COORDINATOR.md rule 4: "parallel
handoff_gate:       MECHANISM_PREFIXES (CLAUDE.md § Worker duties: a self-activating enforcement file ...
judge_calib_sanitize: (COORDINATOR.md rule 13, judge acceptance)
calibration_counts: (see COORDINATOR.md's "Routing | (COORDINATOR.md's journal mermaid diagram) | (rule 8 of COORDINATOR.md: from the SECOND
test_journal_echo_escalation: GAP (COORDINATOR.md rule 6, this repo)
```
Note: journal_write 422 and journal_validator 679 are runtime message strings, not comments (the spec row lists them as retargets; no test pins them, per grep of `tools/test_*.py`).

## Deviations / decisions to check

- `facts` joined KEY_GROUPS/ITEMS (spec: "joins the cut's header vocabulary"); the key is `facts` only (not `fact`) and a bare header only. Also added `facts` to SECTION_STOP_RE and ITEM_EXCLUDED_SECTIONS (not named in the spec; kept so a facts block below owns is not read as owns paths and numbered facts do not count to the designer threshold). Lead to confirm.
- Effect on builder dispatches: a line `facts: ...` now ends the section above it (it was a continuation before).
- `manifest-skip: facts` for a designer dispatch with no owns line: `check_cut` returns early for non-owning dispatches, so a malformed skip line there is not refused by completeness (existing behaviour for every item); `facts_check` reads valid waivers only.
- `dispatch_new --facts` prints for any kind; values cannot hold backticks (existing forbidden-char rule), so a fact command in backticks cannot be passed through this tool.
- Refusal text for FACTS MISSING is the spec's verbatim; it names the door `facts: none -- <why>` but not `manifest-skip: facts -- <reason>` (spec-silent).
- Loader test rows are 4 (spec says three; an extra row for the missing-live-module error).

## Siblings (rule 9) and needed beyond the manifest

- `search_control_gate.py` header line 17 "(3) the CLAUDE.md rule reference below points at this template's own command hygiene point 6": a hygiene citation, valid under (d), left.
- Analogs noticed, not changed: `claim_control_gate.py` lines 32, 210, 268 and `search_control_gate.py` lines 2, 74 cite CLAUDE.md for command hygiene / Windows guidance (valid under (d)). `test_journal_validator.py` has a `rule 12)` string (grep hit) that did not fail on live.
- Needed beyond the manifest: `tools/dispatch_manifest.py` / `dispatch_gate.py` live files (read), spec sections 5.3/6/7/8, `tools/test_dispatch_gate.py` helpers (`_reading_dispatch`).

## Fix round (attempt 2, one fresh worker for t-1233 and t-1234; critic verdict t-1239 F1-F13)

Nothing committed, no `.py.next` placed. Tree wb-int at 26aa2064.

- F1 DONE: COORDINATOR.md:313-326. The three patterns (line-start, anywhere, write list) are each one unbroken line in a fenced block (COORDINATOR.md:322-324). Probe: the rendered write pattern matches `out.mkdir(parents=True)`, `fh = open(p,"w")` and `p.touch()`, and not `x = 1`.
- F2 DONE: COORDINATOR.md:3-9 intro rewritten to the verdict's wording (worker block named as CLAUDE.md, auto-loaded; "Without this policy in context (the `COORDINATOR RULES:` line)").
- F3 DONE: COORDINATOR.md:11 and :15 end with a period.
- F4 DONE: COORDINATOR.md:335 "The Lead compacts" capitalised, block left in place.
- F5 DONE: SIBLING_MAP.md:28/37/40/97/99/105/548/550/668, PROJECT.md:28/79, delegation.config.yaml:4/7/70, TWO_VOCABULARIES.md:4/11/18 retargeted (CLAUDE.md -> COORDINATOR.md, or both where the worker block also applies; row 97 "imported by CLAUDE.md" -> "read with COORDINATOR.md (the `COORDINATOR RULES:` line)"; PROJECT.md:28 names the shell bullet as living in CLAUDE.md; SIBLING_MAP:105 gains COORDINATOR.md in the AGENTS.md regeneration list).
- F6 DONE: dispatch_gate.py.next:777-780 FACTS_MISSING ends with the manifest-skip door sentence; test_dispatch_gate.py "no-line" row asserts it.
- F7 DONE: dispatch_gate.py.next:796-797 returns FACTS_NOTE_UNCHECKED "dispatch_manifest has no FACTS_KINDS"; OldManifest assertion updated (test_dispatch_gate.py, test_facts_check_unknowns_are_a_note_and_a_pass).
- F8 DONE (docstring): tools/under_test.py docstring names the split. The convergence node is for the Lead to file (forge/7, owner Lead): not filed by me.
- F9 DONE: tools/conftest.py:33-40 raises on a file name starting with `<name>.py` that is neither `<name>.py` nor `<name>.py.next`; ORIGINAL_PATH-like values untouched. Rows "typo-loud" and "other-values-ignored" in test_dispatch_manifest.py::test_next_copy_loader.
- F10 DONE: test_facts_state, _FACTS_STATE_ROWS and the FACTS_KINDS pin deleted from test_dispatch_manifest.py. Moved into the gate `_FACTS_ROWS`: empty-then-blank, bare-none-synonym (n/a), none-why-below, none-then-a-fact, block-two-facts (the one-fact `block` was the same as `ok-block`). test_dispatch_new.py: rows facts-builder-untouched and facts-designer-bare-none deleted.
- F11 DONE: tools/dispatch_new.py:62-69 `--facts` is exempt from the backtick ban (newline and CR stay banned); rows facts-designer-backtick and facts-designer-newline. Residual: a fact holding a triple backtick opens a fence in the cut, so a header written after it reads as quoted.
- F12 DONE: docs/tasks/handoffs/t-1233-card-a.md: byte 51537 repaired (the cut `\xe2\x80` completed to an em dash), all CRLF turned to LF; valid UTF-8, 0 CR.
- F13 DONE: CLAUDE.md:83 R11-h gains "a designer dispatch also carries `facts:` (COORDINATOR.md rule 2)".
