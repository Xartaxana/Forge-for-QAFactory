# t-112 / C1 -- hygiene_gate rewritten to four refusals (builder report)

Worktree: `C:\QAFactory\forge-repo\.claude\worktrees\agent-a26b94d005f6a80c8` (not committed).

## Built, per class
- Statement walk (own masks, F-C4): heredoc bodies blanked by ONE linear pass over the lines (`_scan_heredocs`, also returns the bodies for `python - <<`), quotes masked by the existing regex, `#` comments blanked, statements split on `; & | newline ( ) { }` (not inside `2>&1 >& &> >|`, braces only when standing alone), start words `then do else elif ! builtin command time`, `(` / `$(` mark a subshell region. A word tokenizer (quote-aware, backslash is a path character, `$`/backtick/`%VAR%` = dynamic, unquoted `* ?` = glob) gives words and redirects.
- cd: verbs `cd chdir pushd popd Set-Location sl Push-Location Pop-Location` at a statement start (leading `VAR=x` skipped), `eval "cd x"`, `[IO.Directory]::SetCurrentDirectory`, `[Environment]::CurrentDirectory =`. Legal: bare `cd <root>` as the last statement (root = basename of the folder holding the running copy, as before), subshell verb when `SHELL_CAPABILITIES[tool]["subshell_scopes_cwd"]`, verbs inside a quoted child-shell argument. Door per shell from the capability row; unknown tool -> PowerShell row.
- mutation: M1 redirects (`> >> >| &> &>> N>`, `2>&1`/`>&2` and null sinks never targets), tee / Tee-Object / Out-File / Set-Content / Add-Content (first path argument, PS named path params honoured), `[IO.File]::Write*/Append*`; M2 data row `INPLACE_EDITORS` (sed, perl, ruby, awk/gawk); M3 data row `PAYLOAD_INTERPRETERS` (python family classified, node/ruby/perl/pwsh `payload_classifier: None`) with new `_GATE_WRITE_FORMS` walker (`_gate_call`): certain write = literal `open`/`io.open`/`Path(lit).write_text|write_bytes|open`/`json|pickle.dump` onto an inline open; STDIO and FILE-LEVEL silent; everything else advisory-M/O = UNCERTAIN = one WARN. Resolution only in `decide()`: target's own `.git` ancestor walk (file or dir, missing directories walked over), not under `.git/`, `HYGIENE_IGNORE_ROWS = ("ci-out/",)`.
- journal: the SAME targets filtered by `logs/<...>/*.jsonl` or `routing-log` (pure, in `_collect_signals`), refused wherever the file lies.
- rollback: `rollback_form` (pure) from `ROLLBACK_SHAPES` data row (checkout, switch, restore, reset, clean, stash = F-C8 one row), `-C` chain composed left to right, `-c k=v`/`--no-pager`/`--literal-pathspecs` skipped, `--git-dir/--work-tree`/non-literal path -> unresolvable. Measurement in `decide()` only: `gitcmd.git(<addressed dir>, "status", "--porcelain=v1", "-z", <view>, "--", *scope, timeout=5)`; views tracked / clean (`??`, `!!` per -x/-X, dir entries dropped without -d) / stash (-u, -a). Unmeasurable -> pass + `Command hygiene: rollback not checked: <reason>`.
- WARN: one text, `Command hygiene (WARN, does not block): ` + `MSG_WARN_PAYLOAD`. Refusal order journal, rollback, cd, mutation; reason = first; context lists all + notes + WARN.
- `permission_audit`: `HYGIENE_CLASS_LABELS` = cd / content write (literal target) / journal write / rollback shape / payload uncertain; `classify_hygiene` maps the new keys (pure; one row proves no subprocess).
- `warn_layers.json` HYGIENE row: alias for the new WARN literal; reason rewritten. `gitcmd.py` docstring: caller line. `test_warn_messages.py`: six HYGIENE rows, `"HYGIENE": 6`; `WARN_TEXT_BUDGET_CHARS` stays 550.

## Removed
Constants/detectors: `MSG_CD_PREFIX`, `MSG_CD_NON_ROOT_WARN`, `MSG_REDIRECT_STDERR`, `MSG_PYTHON_DASH_C`, `MSG_PYTHON_DASH_C_OPAQUE`, `MSG_PYTHON_DASH_C_BLOCK`, `PYC_DENY_ENABLED`, the ` 2>&1` signal (`_collect_redirect_signal`), `_is_journal_bypass`, `_has_write_form`, `PRINTF_ECHO_RE`, `TEE_RE`, `SED_INPLACE_RE`, `OPEN_WRITE_MODE_RE`, `_PS_WRITE_CMDLET_RE`, `CD_PREFIX_START_RE`, `_extract_cd_prefix_target` family, `_is_cd_prefix`, `_is_python_dash_c`, and the git-commit/git-statement scrubs (`GIT_COMMIT_RE`, `COMMIT_MESSAGE_ARG_RE`, `GIT_STATEMENT_RE`, `_strip_commit_messages`, `_mask_git_statements`, `_statements`, `_heredoc_belongs_to_git_commit`). Kept: the advisory M/P/O lists and `_classify_pyc_payload` (audit instrument; regexes widened to python/python3/py with flags before `-c`), `QUOTED_SEGMENT_RE`, `COMMIT_HEREDOC_RE`, `MAX_HEREDOC_OPENERS`, `PYC_PAYLOAD_LIMIT`, the stdin reader, `_reconfigure_stdout_utf8`.

## Questions returned / deviations (all minor; nothing blocked)
1. **Journal text vs the existing pins.** The spec text has `<target>`; `tools/test_journal_per_developer.py` (k16) asserts `permissionDecisionReason == hg.MSG_JOURNAL_BLOCK`, so the constant carries no placeholder; the target goes into `additionalContext` as `journal target: <path>`. Lead to confirm or to move the pin.
2. **`tools/hook_liveness_probe.py` case 11 anchors the OLD journal text** ("the journal is written only via Edit/Write (command hygiene point 5); shell write to the journal blocked"). Not owned by C1; it now fails: `test_hook_liveness_probe.py::test_live_run_of_all_cases_is_ok`, `test_full_probe_run_from_another_cwd_...`, `test_main_cli_exit_code_zero_on_live_gates`, `test_main_cli_json_flag_produces_parseable_json` (4 failed; the detail line shows verdict MISMATCH for `11-hygiene_gate-journal-bypass-deny`). One anchor line needs the new text (e.g. "the journal is written only through Edit/Write at the file's tail"); a node for the Lead.
3. **HYGIENE population in `warn_layers.json`.** The spec says the row "gets its population (every Bash/PowerShell call)"; `warn_density.POPULATION_KINDS_MEASURED` is a closed tuple outside C1's owns, so the row stays `unmeasured` with a reason naming the gap and gains the WARN alias. Needs a node on `tools/warn_density.py` (new kind + predicate) if the Lead wants it measured.
4. PowerShell cd door: dropped the spec's parenthetical "(t-098 F14; C0.1 verifies it runs)" from the shipped text (a spec annotation, not receiver text). Door itself kept.
5. stdin: `utf-8-sig` decode (the old `utf-8` left a BOM in front of the JSON so the whole call passed silently).
6. `tee`: first path argument only (as the spec says); `tee a b` leaves `b` a residual.
7. A statement over the heredoc cap: heredoc-bearing statements yield no write targets (spec); cd detection still runs on them.
8. Bare-return `cd` keeps "as today" basename comparison with the running folder's name.
9. Stale text outside C1's owns: `permission_audit.py` module docstring (lines 39-40, 51-52) still names the old four classes and the git scrubs; SKILL.md step 2 (C2); `docs/SIBLING_MAP.md:528`; `tools/dup-baseline.json` may need a clone-ratchet refresh for the new file (not run).

## Test table summary (`tools/test_hygiene_gate.py`, ONE table `test_decide_table` over `decide()`, 147 rows)
silent 53 / WARN only 5 / refused mutation 27 / refused journal 7 / refused cd 19 / refused rollback 17 / markers 4 / adversarial 15 (100 KB, 1 MB x2, 20K statements, 65 heredoc openers, nested quotes/heredocs, CRLF, Cyrillic, NUL, unclosed quote, 5000 unclosed `python -c "`). Each refusal row asserts its door text in the reason AND the context; WARN rows assert the exact text. Both Lead rows pass silent; stash row (dirty scope refused, clean scope passes, `drop` silent) present. Outside the table: order of several refusals, WARN never the reason, rc -1 marker, raising measurement marker, classifier-exception marker, unreadable input (10 shapes), 350-char budget of each text, removed-names check, `_collect_signals` purity (subprocess/gitcmd/lexists patched to raise), relative target after subshell cd, process reader (plain, BOM, empty, broken JSON, binary, `null`), 100 KB/1 MB ratio.
`test_permission_audit.py`: one parametrised row per label, labels pin, no-subprocess replay row, matrix updated. `test_warn_messages.py`: six HYGIENE verb rows, count 6.

## Timing, 1 MB adversarial row
`python -m pytest tools/test_hygiene_gate.py -q -s -k perf` -> `hygiene_gate decide: 100KB 0.1306s, 1MB 1.4654s, ratio 11.2` (command = 1 MB redirect line + a 1 MB python payload; linear, ratio bound < 40).

## Witness (DoD)
```
python -m pytest tools/test_hygiene_gate.py tools/test_permission_audit.py tools/test_warn_messages.py tools/test_gitcmd.py -q
........................................................................ [ 80%]
.......................................................................  [100%]
359 passed in 16.64s
```
Neighbours: `python -m pytest tools/test_journal_per_developer.py tools/test_streams.py tools/test_agents_md.py -q` -> `169 passed in 96.29s`; `test_warn_density.py`, `test_enforcement_probe.py` pass; `test_hook_liveness_probe.py` 4 failed (question 2).
Live smoke: my own shell calls ran under the worktree's new gate (hooks are cwd-relative): a `cd tools && ...` was refused with the new Bash door text, and a `python -c` with `getattr` got the one WARN.

## Fix the class (analogs noticed)
`hook_liveness_probe` anchors (question 2) and `warn_density` kinds (question 3); permission_audit module docstring and SIBLING_MAP:528 (question 9); `agent_budget.PLAIN_GIT_RE` unchanged.

## Needed beyond the manifest
Read: `tools/hook_liveness_probe.py` (anchors), `tools/test_journal_per_developer.py` (k16 pins), `tools/test_streams.py` and `tools/test_agents_md.py` (the gate must import alone beside permission_audit; docstring first paragraph pinned), `tools/warn_density.py` (population kinds), `tools/test_hook_liveness_probe.py`.
