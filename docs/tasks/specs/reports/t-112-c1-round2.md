# t-112 / C1 round 2: fix round for the critic's verdict (builder)

Worktree: `C:\QAFactory\forge-repo\.claude\worktrees\agent-a26b94d005f6a80c8` (uncommitted, nothing committed).
Files written: `tools/hygiene_gate.py`, `tools/permission_audit.py`, `tools/test_hygiene_gate.py`, `tools/test_permission_audit.py`, `tools/hook_liveness_probe.py` (anchor only), this report. `gitcmd.py`, `test_warn_messages.py`, `warn_layers.json` needed no change.

## Per item

- B-1 FIXED. `_neutralize_regions` blanks `<`/`>` inside `(( ))`, `$(( ))`, `for (( ))` (one stack pass over the parentheses) and `[[ ]]` (forward find); gated by capability row key `arith_regions` (Bash true, PowerShell false). A redirect after the closing bracket still refuses (rows `b1-redirect-after-*`).
- B-2 FIXED. `sig["rollback_forms"]` is a list (every git shape of the command); `decide()` measures each, the first that hits a dirty tree refuses and names its own directory; markers are collected (deduplicated). `permission_audit.classify_hygiene` and `test_permission_audit._gate_attribution` re-keyed in the same change (AR-22).
- B-3 FIXED. `_Walker` keeps a stack of directory scopes per `( )` / `$( )` group (`_Stmt.depth`): a literal cd extends the group's prefix (tuple), the group inherits the parent's prefix on open and loses its own on close; absolute components restart; targets (redirect, tee, in-place, payload, journal) are composed as strings in the pure walk (`_compose`), the rollback form gets the prefix in front of its `-C` chain. A non-literal cd (variable, `-`, bare, `popd`, `eval`) makes that group unresolved: relative targets are dropped (no refusal, no journal flag), payload -> the existing WARN, rollback -> the existing `rollback not checked: unresolvable` marker. It never leaks outside the group.
- B-4 FIXED. `tools/hook_liveness_probe.py` case `11-hygiene_gate-journal-bypass-deny`: anchor is now `the journal is written only through Edit/Write at the file's tail` (a substring of `MSG_JOURNAL_BLOCK`); the other anchor and `const_ref` untouched. `test_hook_liveness_probe.py` passes.
- F-1 FIXED. `_TEE_LIKE` is a data row name -> `"all"|"first"`; `tee` writes every non-option operand, no operand passes.
- F-2 FIXED. `sc`/`ac` rows; `$name = ` is a statement-start prefix (capability key `assign_prefix`, PowerShell true).
- F-3 FIXED. Capability key `dq_escape` (Bash `\`, PowerShell backtick); `_Rules` (built from it) is read by the mask and the tokenizer; the PowerShell dynamic-char set excludes the backtick (it is the escape). Doubled quotes in PowerShell read as two adjacent strings (same mask, same statements; the literal quote char is dropped from a word's text).
- F-4 FIXED. `_mask_quoted_segments` is a linear scanner (a quote kind with no closer is retired after its first failure; unrolled-loop regex for the closer); `QUOTED_SEGMENT_RE` removed; `_is_python_dash_c_certain` uses it. 64 KB of escape pairs: new test, <1 s (measured in the run below).
- F-5 FIXED. `_measure_rollback` resolves each `-C` component through `_absolute_target` (MSYS `/c/dir` -> `C:/dir`, `~`, absolute restart); a directory still absent -> existing marker (pass).
- F-6 FIXED. `_gate_call`: `attr == "open" or dotted in _FREE_OPEN_DOTTED_NAMES`.
- F-7 FIXED. `_first_path_arg` splits `-Path:value` (`_bound_value`); a colon-bound value parameter is skipped whole.
- F-8 FIXED (Lead's decision). `_JOURNAL_RE`: only `logs/journal/*.jsonl` and `logs/routing-log.jsonl` (any prefix, either slash); `logs/out.jsonl` falls to the general tree check. Docstring updated.
- F-9 FIXED. `SHOWN_TARGET_CHARS = 40`, `_clip` shows the tail for the mutation target and the rollback directory; formatted worst cases 339 and 290 characters; test measures the formatted text.
- F-10 FIXED. `permission_audit.py` module docstring and `classify_hygiene` docstring rewritten (no old classes, no `_classify`, no scrubs).
- F-11 FIXED. `_collect_signals` is a 12-line wrapper over `class _Walker` (methods `run`, `_enter_scope`, `_content_start`, `_cd_class`, `_move_scope`, `_add_target`, `_write_classes`, `_redirect_path`, `_payload`, `_rollback`, `_dotnet`, `_bare_return`), each under 60 lines; still pure (test patches subprocess, `os.path.exists/isdir/lexists`, `os.stat/getcwd/listdir`, `time.time/monotonic`, `gitcmd.git` to raise and walks a nested-group sample under both rows).
- F-12 FIXED. One `_PYTHON_NAME` spelling read by the payload-interpreter row and by `_PY_HEAD`; `python3.12 -c` is now "M" for the advisory classifier.
- F-13 FIXED. The dead `!= "SetCurrentDirectory"` condition is gone with the old loop; `decide()` indexes `SHELL_CAPABILITIES[tool_name]` (only the two rows' tools reach it); `_Walker` keeps a `.get(..., PowerShell)` default with a comment (the audit may call with another name).
- F-14 FIXED. Rows `bash|sh|zsh|dash|ksh` (`-c`) and `cmd` (`/c`, `/k`) in `PAYLOAD_INTERPRETERS`, `payload_classifier: None`; docstring names the residual.

## Red-before proof (the round-1 module was overwritten in place, so the fix was neutered IN MEMORY by a scratchpad pytest plugin, `scratchpad/redprobe.py`, env `RED=<id>`; the repo file is never touched). Failing rows per neutered fix:

```
RED=B1: b1-arith-if, b1-arith-subst, b1-arith-and, b1-dbl-bracket, b1-for-arith, b1-arith-ge  (7 failed, 257 passed)
RED=B2: b2-clean-then-hard, b2-clean-repo-then-dirty-repo, test_chained_rollback_names_the_first_dirty_target  (3 failed)
RED=B3: b3-subshell-cd-clean-repo, b3-subshell-cd-rel-rollback, b3-subshell-cd-journal, b3-nonliteral-cd-rollback,
        b3-nonliteral-cd-redirect, b3-nonliteral-cd-journal, b3-absolute-cd-in-group + 5 test_cd_scope_per_group rows (12 failed)
RED=F1: f1-tee-devnull-first, f1-tee-two-files, f1-tee-journal-second  (3 failed)
RED=F2: f2-sc-alias, f2-ac-alias-journal, f2-assign-prefix-cd, f2-assign-prefix-write  (4 failed)
RED=F3: f3-ps-trailing-backslash-cd, -redirect, -journal, f3-ps-backtick-escaped-quote  (5 failed)
RED=F5: f5-msys-git-C, f5-msys-redirect  (2 failed)
RED=F7: f7-path-colon-scratch  (1 failed)
RED=F8: f8-scratch-jsonl-outside, f8-other-jsonl-in-tree, f8-routing-log-lookalike  (3 failed)
```
Not neutered (no clean in-memory switch): F-4 (the old regex is gone; the 64 KB test is the proof, it was 4.4 s at 32 KB per the verdict), F-6, F-9, F-10..F-14 (structural; their tests assert the new shape: `_clip` length, `_Walker` method sizes, `_classify_pyc_payload("python3.12 ...")`, the interpreter rows). The B-4 anchor is proven by `test_hook_liveness_probe.py` going green.

## The 16 pass-silently commands of the verdict (decide(), cwd = main clone)

```
python -B scratchpad/silent16.py
SILENT <- Bash 'grep -n x logs/journal/dev1.jsonl 2>/dev/null'
SILENT <- Bash "awk 'END{print NR}' logs/journal/dev1.jsonl"
SILENT <- Bash 'git -C C:\\QAFactory\\...\\agent-a26b94d005f6a80c8 diff HEAD -...   (backslash redirect to scratchpad)
SILENT <- Bash 'git -C C:/QAFactory/...  diff HEAD --bina...   (forward-slash redirect)
SILENT <- Bash 'git log --oneline -3 | cut -c1-80'
SILENT <- Bash 'python -B tools/ci_read.py jobs 123'
SILENT <- Bash 'git add a b && git commit -q -F ...\\msg.txt | grep -i fatal; git push -q origin main'
SILENT <- Bash 'git cherry-pick pile/x/batch-1 | tail -2'
SILENT <- Bash 'cp C:/.../docs/x.md docs/x.md'
SILENT <- Bash 'git stash list'
SILENT <- Bash 'git checkout -b new-branch'
SILENT <- Bash 'git restore --staged f'
SILENT <- Bash "python -B - <<'EOF' ... open('logs/journal/dev1.jsonl').read().count('>') ... EOF"
SILENT <- Bash 'python -B -c "import json,sys; print(json.load(open(\'a.json\'))[\'k\'])"'
SILENT <- PowerShell 'Get-Content f | Select-Object -First 5'
SILENT <- PowerShell 'git status 2>&1'
not silent: 0
```

## DoD run (verbatim, from the main clone cwd, absolute targets)

```
python -m pytest C:/QAFactory/forge-repo/.claude/worktrees/agent-a26b94d005f6a80c8/tools/test_hygiene_gate.py C:/QAFactory/forge-repo/.claude/worktrees/agent-a26b94d005f6a80c8/tools/test_permission_audit.py C:/QAFactory/forge-repo/.claude/worktrees/agent-a26b94d005f6a80c8/tools/test_warn_messages.py C:/QAFactory/forge-repo/.claude/worktrees/agent-a26b94d005f6a80c8/tools/test_hook_liveness_probe.py -q -p no:cacheprovider
........................................................................ [ 13%]
........................................................................ [ 27%]
........................................................................ [ 41%]
........................................................................ [ 55%]
........................................................................ [ 69%]
........................................................................ [ 82%]
........................................................................ [ 96%]
.................                                                        [100%]
521 passed in 28.87s
```
(`test_hygiene_gate.py` alone: `264 passed`; 147 old table rows + 56 new rows + the new tests.)

## Question for the Lead (an item that reads two ways, not decided silently)

Edge (3) says an unresolved target is "fail open with no message"; the verdict's B-3 fix says "the rollback marker for rollback, WARN for payloads, as now". I kept the marker / WARN (both are existing, non-refusing notes; FR-59: a gate names what it could not establish). If the Lead wants literal silence for a rollback behind a non-literal cd, it is one line in `_Walker._rollback` (skip appending the form) and the row `b3-nonliteral-cd-rollback` flips from marker to silent.

## Analogs noticed, not fixed (outside owns or scope)

- `permission_audit.classify_hygiene(command)` replays with the Bash row only; a PowerShell call gets Bash quote rules in the audit (the gate itself is right). Pass the tool name when `iter_tool_calls` carries it.
- `_net_target` (the .NET literal reader) and the unquoted `_DYNAMIC_RUN_RE` still use `$`/backtick as Bash does; PowerShell here-strings (`@' ... '@`) are not masked like heredocs.
- `_mask_heredoc_bodies` (regex, advisory) beside `_scan_heredocs` (linear) remain two instruments (spec-sanctioned, as the verdict says).
- `(( x << y ))` is read as a heredoc opener by `_scan_heredocs` before regions are neutralised (under-detection after it, never a refusal).
- Queue items Q-1..Q-5 untouched (non-goal).

Needed beyond the manifest: none read beyond `tools/test_permission_audit.py` lines 575-625 (the re-keyed attribution helper, same owned file), the scratchpad plugin/script (not committed).
