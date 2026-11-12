# t-112 / C1: code review of the hygiene_gate rewrite (critic, diff gate)

Reviewed: the uncommitted diff in `C:\QAFactory\forge-repo\.claude\worktrees\agent-a26b94d005f6a80c8` (7 files, +1553/-3159), against spec `docs/tasks/specs/fg-context-and-hygiene.md` (Lead acceptance sections, §0 F9-F11, §4 C up to C0, C1, §9), plan verdict t-098, and `docs/tasks/critic-diff-brief.md`. I worked empirically: I imported `decide()` from the worktree by absolute path and drove it with real commands. The Lead's two rows, the 16 commands in (a), purity and fail-open all behave as specified. Three defects block the merge, one of them the worst class the spec names (a calculation refused). A fourth blocking item is a pin outside C1's owns that has to change in the same merge.

**Verdict: NEEDS WORK** (`fit_with_fixes`): 4 blocking (B-1..B-4), 14 fix-before-merge (F-1..F-14), 5 queue lines (Q-1..Q-5). Acceptance is the Lead's.

## Blocking

**B-1. Bash arithmetic and `[[ ]]` comparisons are refused as content writes. This is a calculation refused (spec §4: "a read or calculation is never refused").** Surface: the M1 redirect recogniser (`_tokenize` lines 304-331, plus the redirect loop in `_collect_signals` lines 1102-1111). It treats every `>` as a redirect, including `>` inside `(( ))`, `$(( ))`, `for (( ))` and `[[ ]]`. `_split_statements` cuts at `(`, so the inner text reads as a statement with a redirect. The refusal text then says "5 is a file of a git working tree". Probe (cwd = main clone):
```
'if (( n > 5 )); then echo big; fi' -> 5 is a file of a git working tree and this command writes it
'echo $(( 3 > 2 ))' -> 2 is a file of a git working tree and this command writes it
'(( count > 0 )) && echo yes' -> 0 is a file of a git working tree and this command writes it
'[[ abc > abb ]] && echo yes' -> abb is a file of a git working tree and this command writes
'for ((i=10; i > 0; i--)); do echo $i; done' -> 0 is a file of a git working tree and this command writes it
'x=$(( a >= b ? 1 : 0 ))' -> = is a file of a git working tree and this command writes it
```
The old gate had no mutation class, so this is a regression. Proposed fix: mark arithmetic and test regions (`((`…`))`, `$((`…`))`, `[[`…`]]`) during the mask pass. This should be a Bash capability row (`arith_regions: true`; the PowerShell row false, AR-1). No `>` inside such a region is a redirect. Add one table row per form above, all silent. Neighbouring classes walked: `[ $n -gt 3 ]` is silent (correct). Process substitution `>(…)` yields a target of None (correct). `2>&-`, `>&2` and `*>&1` are not targets (correct).

**B-2. Only the first rollback shape in a command is measured, so a chained rollback passes silently.** At `_collect_signals` lines 1154-1155, `if cmd == "git" and sig["rollback_form"] is None: sig["rollback_form"] = _rollback_form(args)`: once one shape is found, later ones are never read. Probe (main clone, `docs/tasks/specs/fg7-8-b-vcs-words.md` dirty):
```
'git checkout -- README.md && git reset --hard' -> SILENT
'git status; git checkout -- docs/tasks/specs/fg7-8-b-vcs-words.md' -> DENY: 1 path(s) under C:\QAFactory\forge-repo ...
```
Invariant 4 is broken in a plain `&&` chain, a form the spec treats as certain. Proposed fix: collect `rollback_forms` as a list and measure each one in `decide()` until the first refusal. Rename the key in `permission_audit.classify_hygiene` in the same commit (AR-22). Add a row `git checkout -- <clean> && git reset --hard` (refused).

**B-3. A directory change inside a subshell is not carried into target resolution. The result is a false refusal in the wrong repository, plus silent passes of invariants 2, 3 and 4.** Surface: the `after_cd` flag in `_collect_signals` (lines 1054, 1083-1084, 1149-1151, 1156-1157). The flag never resets when the subshell closes. Inside the subshell the literal cd target is ignored: the rollback runs in the payload cwd, and relative targets are dropped. The `( cd <dir> && … )` subshell is the door the Bash cd refusal itself offers. Probes:
```
'( cd <SP>/cleanrepo && git reset --hard )'   [cwd = dirty main clone; cleanrepo = fresh git init, clean]
   -> DENY: 1 path(s) under C:\QAFactory\forge-repo have uncommitted changes that may be another sessi
'( cd docs && git checkout -- tasks/specs/fg7-8-b-vcs-words.md )' -> SILENT   (the path is dirty)
'( cd logs/journal && echo x >> dev1.jsonl )' -> SILENT                          (journal invariant)
'( cd sub && make ); echo x > docs/a.md' -> SILENT                               (after the subshell closed)
'd=$(cd docs && pwd); echo x > docs/a.md' -> SILENT
```
The first probe is a refusal on a target the gate could not resolve: the spec's invariant "no refusal on a target the gate could not resolve" fails, and the text names a repository the command does not address. The last two are not the spec's named residual ("a relative target inside a statement that follows a subshell directory change"). The subshell has closed, so the target resolves against the original cwd. Proposed fix, kept pure in `_collect_signals`: keep a cd scope per subshell region and drop it at the region's close. Inside a region whose cd target is literal, record it as a prefix. In `decide()`, compose cwd + prefix for relative write targets, for the journal pattern and for the rollback directory (one resolver, see F-5). A non-literal cd target makes it unresolvable: the rollback marker for rollback, WARN for payloads, as now. Add the five rows above. The spec sentence about the subshell residual (M3 bullet) needs the Lead's one-line amendment, because the target is in fact resolvable.

**B-4 (merge-blocking, outside C1's owns). `tools/hook_liveness_probe.py:1334-1337`, case `11-hygiene_gate-journal-bypass-deny`, anchors the old text.** The anchor is `"the journal is written only via Edit/Write (command hygiene point 5); shell write to the journal blocked"`. The new `MSG_JOURNAL_BLOCK` (`hygiene_gate.py:78-81`) does not contain it, so the four probe tests the builder lists go red on the canon. Answer to (e)(1): replace that one anchor string with a substring of the new constant, e.g. `"the journal is written only through Edit/Write at the file's tail"`. Keep `'"permissionDecision": "deny"'` and `const_ref`. Also touch line 63 if it quotes the old text (it only names the constant). Case 11's payload (`echo probe_marker >> logs/routing-log.jsonl`, no cwd) is still refused under the new gate (`routing-log` matches). The Lead adds `tools/hook_liveness_probe.py` to the owns of this round (or a sibling node) in the same merge. Witness: `python -m pytest tools/test_hook_liveness_probe.py -q`.

## Fix before merge (non-blocking)

- **F-1. `tee` reads only its first path argument.** This lets the mutation and journal invariants through. Probes: `printf x | tee /dev/null docs/a.md` -> SILENT; `printf x | tee <SP>/x docs/a.md` -> SILENT; `printf x | tee /dev/null logs/journal/dev1.jsonl` -> SILENT. The spec says "the first path argument", which is a spec defect for `tee`: tee writes every file it is given. (e)(4): every non-option argument of `tee` is a target. `Tee-Object`, `Out-File`, `Set-Content` and `Add-Content` take one path, so first-only stays right for them (`_first_path_arg`, lines 349-362).
- **F-2. PowerShell aliases and assignment forms pass silently.** `sc docs\a.md x` -> SILENT, `ac logs\journal\dev1.jsonl x` -> SILENT, `$null = Set-Location docs` -> SILENT. Add `sc`/`ac` to `_TEE_LIKE` (data, line 107). Treat `$<name> = ` as a statement-start prefix in the PowerShell row.
- **F-3. PowerShell double quotes are parsed with Bash escape rules: a backslash is taken as an escape.** `QUOTED_SEGMENT_RE` (line 132) and `_DQ_RE` (line 236) do this. In PowerShell `"C:\x\"` is a closed string, and a trailing backslash on a Windows directory is common. Probes (PowerShell): `Get-Item "C:\x\"; Set-Location docs; "y"` -> SILENT; `Get-ChildItem "C:\QAFactory\" > docs\a.md` -> SILENT; `Get-Item "C:\x\"; Add-Content logs\journal\dev1.jsonl x; "y"` -> SILENT; ``Write-Output "a`"b" > docs\a.md`` -> SILENT. Three of the four invariants are lost, and the cd loss is the one that disables every hook (PROJECT.md "Рабочий каталог шелла не меняется никогда"). One road (P31, AR-1): add a `dq_escape` capability row (`\` for Bash, `` ` `` for PowerShell) and have the masks and the tokenizer read it. The quote mask predates C1, but the new tokenizer repeats it.
- **F-4. Quadratic path in `QUOTED_SEGMENT_RE`.** It is used twice: `_mask_quoted_segments` in `_collect_signals`, and `_is_python_dash_c_certain`. An unclosed `"` followed by escape pairs makes every quote start scan to the end. Measured: `"\` x2000 (4 KB) 0.057 s; x4000 (8 KB) 0.240 s; x8000 (16 KB) 0.950 s; x16000 (32 KB) 4.44 s, split `_mask_quoted_segments` 2.24 s + `_classify_pyc_payload` 2.2 s. That extrapolates to about 45 s at 100 KB, which breaks the spec's "time bound kept". Proposed fix: a linear quote scanner (one pass, a state machine that reads F-3's capability), or a size cap with precedent `guard_pre_tool.size_check`, 64 KB (SIBLING_MAP axis 11). Past the cap, pass with a visible marker, never refuse. (c) on the builder's 1 MB = 1.47 s: my figures on linear shapes are plain words 1 MB 0.43 s, quoted commit message 1 MB 0.72 s, python payload 1 MB 0.94 s, heredoc 1 MB 0.27 s, everything at 10 KB ≤ 0.025 s. Real commands are a few KB, so cost is about 1 ms per call. Acceptable once the quadratic shape is cut.
- **F-5. Two path resolvers in one module.** `_measure_rollback` (lines 1257-1260) joins the `-C` chain without `_absolute_target`'s MSYS translation (lines 1191-1199). Probe from the scratchpad cwd: `git -C /c/QAFactory/forge-repo reset --hard` -> `rollback not checked: addressed directory absent: C:\c\QAFactory\forge-repo`, while `git -C C:/QAFactory/forge-repo reset --hard` -> DENY. Route the rollback directory through the one resolver (this also serves B-3).
- **F-6. An import alias of `open` passes silently.** `python -c "from io import open as o; o('docs/a.md','w').write('x')"` -> SILENT. `_gate_call` (line 690) keys on the raw name `attr == "open"`, not on the resolved dotted name. Test `dotted in _FREE_OPEN_DOTTED_NAMES or attr == "open"`.
- **F-7. A colon-bound PowerShell parameter produces a false refusal on the wrong word.** `Set-Content -Path:<SP>\o.txt hello` -> `DENY: hello is a file of a git working tree`. `_first_path_arg` skips `-Path:<v>` as a bare option and takes the value word as the path. Split `-Name:value` in `_first_path_arg`.
- **F-8 (spec-level, the Lead's call). The journal pattern catches scratch and stand files.** `python -B tools/x.py > <SP>/logs/out.jsonl` -> DENY (journal). The regex `(?:^|/)logs/(?:[^/]+/)*[^/]+\.jsonl$` (line 342) matches any `logs/*.jsonl` anywhere, with refusal "wherever it lies". A reading role cannot use the Edit/Write door on a scratch path (handoff_gate). Recommendation: narrow it to `logs/journal/*.jsonl` and `routing-log`.
- **F-9. Texts go over the 350-character cap once formatted.** `MSG_MUTATION` is 307 characters as a template and 379 with the allowed 80-character target. `MSG_ROLLBACK` with a worktree subdirectory measured 344, and it is unbounded. Cap the shown target and directory at about 40 characters, or measure the formatted text in the 350 test.
- **F-10. Stale docstring in an owned file.** `tools/permission_audit.py:37-52` still names the old four classes ("2>&1 / cd-Set-Location / python -c-heredoc"), "WARN to BLOCK", the git-statement and `-m` scrubs, and `_classify`, none of which exist now. Rewrite it in this commit (AR-22: producer and reader together).
- **F-11. Code quality (brief item 7).** `_collect_signals`, lines 1036-1182, is 146 lines, holds a nested `def add_target`, and nests five levels deep (for / if / if / for / if at 1123-1152). Split it into one extractor per class: cd, M1, M2, M3, rollback. B-2 and B-3 then become local edits.
- **F-12. Two python-payload recognisers in one module disagree.** `_PY_HEAD` (line 787) matches `python3?|py`, while the gate's `PAYLOAD_INTERPRETERS` (line 114) matches `python[0-9.]*|py`. So `python3.12 -c "…"` is gate-classified but the audit's `pyc_payload` reads `U`. Derive the advisory head from the data row, or name the gap in the docstring.
- **F-13. Dead conditions.** `hit["verb"] != "SetCurrentDirectory"` (line 1156) is always true inside the loop, because .NET hits are appended after it. `SHELL_CAPABILITIES.get(tool_name, …PowerShell)` (line 1315) never takes its default, because `decide()` already returns for any other tool name (line 1352). The spec states both behaviours. Drop the condition, and keep the default only with a comment saying it is unreachable now.
- **F-14. A child shell's payload is an unnamed residual.** `bash -c "echo x > docs/a.md"` -> SILENT. `bash`, `sh` and `cmd` are not rows of `PAYLOAD_INTERPRETERS`. The spec's residual list names only the `payload_classifier: none` rows, so this road is neither a data row nor named. Add the rows with `payload_classifier: None` (P31: a data row, not silence).

## Queue (outside C1, with owners)

- **Q-1.** (e)(3) HYGIENE population: add a `warn_density.py` kind and predicate for "every non-empty Bash/PowerShell call". Node on `tools/warn_density.py`, owner the Lead, `forge` pile. Keeping `unmeasured` with the rewritten reason is correct for C1.
- **Q-2.** `docs/SIBLING_MAP.md:529`: "command hygiene 3-4" becomes "3, 4, 5, 7". Node P, same merge.
- **Q-3.** `.claude/skills/permission-audit/SKILL.md:60` (the `cd X &&` / ` 2>&1` row) belongs to C2, same merge. Role files: no stale motive found (critic.md 74 and builder.md 61 point to point 6, which stays valid).
- **Q-4.** C0 has not run: there is no `fg-ctx-C0-experiments.md` in the repo. Glob `**/*C0*` over the clone is empty; positive control `**/t-114*` finds 3 files. The PowerShell child-shell door therefore ships unverified. (e)(4): dropping the parenthetical "(t-098 F14; C0.1 verifies it runs)" from the receiver text is right, but C0.1 must run before C2 publishes the door.
- **Q-5.** Axis 11 evidence: B-1 (`$(( ))` regions) and F-3 (the PowerShell dialect) are both handled by `hooklib.walk` (SIBLING_MAP:275). F-C4 "own masks" stands as the Lead's decision. This line is input for the queued convergence, not a finding against it.

## Answers a-g

**a. False refusals.** The 16 required commands all return SILENT (verbatim in the trail). This includes `grep … 2>/dev/null`, `awk` on the journal, the diff redirect to the scratchpad in both path styles, `git add && commit -F | grep; push`, `cherry-pick | tail`, `cp` into docs, `stash list`, `checkout -b`, `restore --staged`, the read-only `python -B -` heredoc, `python -B -c json.load`, PowerShell `Get-Content | Select-Object`, and PowerShell `git status 2>&1`. False refusals I found beyond the list: B-1 (arithmetic and `[[ ]]`, blocking), B-3 (a subshell rollback measured in the wrong repository, blocking), F-7 (`-Path:`), F-8 (journal pattern on a scratch path).

**b. False passes.** cd, 19 variants: refused except `$null = Set-Location docs` (F-2) and F-3. Mutation, 40 variants: refused except `tee` with multiple files (F-1), `sc`/`ac` (F-2), `bash -c` (F-14), the leaking `after_cd` flag (B-3), the `io.open` alias (F-6) and F-3. Journal, 9 variants: refused except `tee /dev/null JJ` (F-1), `ac` (F-2) and the subshell case (B-3). Rollback, 22 variants: refused except the chain (B-2), the subshell case (B-3) and MSYS `-C` (F-5, a marker rather than silence). `git stash`, `stash -u`, `stash push -- <dirty>` and `stash push -m wip <dirty>` are refused; `stash push -- README.md` (clean) passes. F-C8 is honoured.

**c. Purity and cost.** Purity holds. I patched `os.path.exists/lexists/isdir/isfile`, `os.stat`, `os.getcwd`, `os.listdir`, `os.path.realpath`, `os.path.expanduser`, `subprocess.run/Popen`, `time.time/monotonic`, `builtins.open` and `gitcmd.git` to raise, then ran 12 samples through `_collect_signals` (all four classes, a heredoc payload, a subshell cd). Result: "purity: all 12 samples ran". Cost: see F-4. There is one quadratic shape; everything else is linear.

**d. Fail-open.** Piped to `python -B <wt>/tools/hygiene_gate.py`: empty stdin, `null`, tool `Read`, unknown tool `Bashh`, a string `tool_input`, broken JSON, and a NUL in the target all gave rc=0 and silence. A BOM payload with `cd docs` gave a refusal, so the `utf-8-sig` change works. `_measure_rollback` catches everything into the marker. `_tree_display` lets non-OSError exceptions through to `decide()`'s broad except, which prints the fail-open marker. I found no exception path that refuses.

**e.** (1) B-4. (2) Acceptable against P15: the reason says what is wrong ("the journal …") and gives the door, and `additionalContext` names the target. Moving the k16 pin (`test_journal_per_developer.py:770`) to `== MSG.format(target=…)` is cheap but not required. (3) Q-1. (4) The door annotation: right to drop it. `tee a b`: a real false pass, F-1.

**f. Texts.** Every text says what is wrong, what is expected and a door. The cd doors (`git -C`, `python -B <abs>`, `--repo`, subshell) work for every role. The mutation door gives a reading role "write outside the tree" (a shell redirect to the scratchpad passes) and "your handoff file". The rollback door gives no harmful road. Over the cap once formatted: F-9. WARN: 151 characters with its prefix, within 550, and `WARN_TEXT_BUDGET_CHARS` was not raised.

**g. Stale siblings.** In this merge: F-10 (permission_audit docstring, owned), B-4 (probe anchor), Q-2 (SIBLING_MAP:529, node P), Q-3 (SKILL step 2, C2). CLAUDE.md point 3 is C2's. `tools/dup-baseline.json:366,499` lists `hygiene_gate.py` in clone groups. That is the ratchet's to read on the branch's `forge-check`; I did not re-run it (brief: read, never re-run).

## Standing questions

- **DUPLICATION AND CONSISTENCY:** F-5 (two path resolvers), F-12 (two payload heads), and `_mask_heredoc_bodies` (regex, advisory) beside `_scan_heredocs` (linear, gate). The second is spec-sanctioned (the advisory instrument is kept). Repository-wide, the tokenizer duplicates `hooklib.walk` by the Lead's decision F-C4; convergence is queued on axis 11 (Q-5). Grepped: `hygiene_gate` across `tools/`, and SIBLING_MAP axis 11.
- **CODE QUALITY:** F-11 (`_collect_signals` 146 lines, nesting 5), F-13 (dead conditions). The class recognisers are data rows (`SHELL_CAPABILITIES`, `INPLACE_EDITORS`, `ROLLBACK_SHAPES`, `PAYLOAD_INTERPRETERS`, `HYGIENE_IGNORE_ROWS`, `_TEE_LIKE`, `_CD_VERBS`), which meets AR-1. Missing rows: F-2, F-3, F-14.
- **ONE ROAD (P31):** F-3 (PowerShell quoting goes down the Bash road), F-14 (child shells are not a row). The Bash/PowerShell cd difference is a capability row, which is right.
- **ARCHITECTURE:** AR-22 is kept (`classify_hygiene` re-keyed in the same diff). AR-13: git goes through `gitcmd.git` (axis 10). AR-9 doors are kept. AR-1 has the gaps above. **JUDGMENT:** none. Every check is form, data or measured status (P27).
- **Ratchets:** `WARN_TEXT_BUDGET_CHARS` stays 550. The `"HYGIENE"` count pin goes 4 → 6 (a count, not a shrink-only ratchet). No in-tree ratchet row was raised.
- **Tests:** the 147-row table did not catch B-1..B-3 or F-1..F-3. Each fix carries its probe as a row.

## Trail

Read: `tools/hygiene_gate.py` 1-1480 (whole file); the builder report; spec lines 8-82, 198-317, 430-457; `docs/tasks/critic-diff-brief.md`; `tools/hook_liveness_probe.py` 905-912, 1324-1340; `tools/test_journal_per_developer.py` 755-776; `tools/permission_audit.py` 36-57; the diff of `permission_audit.py`, `warn_layers.json` and `gitcmd.py`; `docs/SIBLING_MAP.md` 267-280 and 522-533; `tools/install_parity_anchors.json` 555-573; `tools/critic_verdict.schema.json`.

Re-runs:
- `python -m pytest tools/test_hygiene_gate.py tools/test_permission_audit.py tools/test_warn_messages.py tools/test_gitcmd.py -q -p no:cacheprovider` in the worktree -> `359 passed in 13.41s` (matches the builder's 359).
- Probes: `python -B - <<'PYEOF' …` scripts that import `<wt>/tools/hygiene_gate.py` via `importlib` and call `decide({"tool_name", "cwd", "tool_input"})`.

(a), verbatim:
```
'grep -n x logs/journal/dev1.jsonl 2>/dev/null' -> SILENT
"awk 'END{print NR}' logs/journal/dev1.jsonl" -> SILENT
'git -C C:\...\agent-a26b94d005f6a80c8 diff HEAD --binary > C:\Users\...\scratchpad\a.patch' -> SILENT
'git -C C:/.../agent-a26b94d005f6a80c8 diff HEAD --binary > C:/Users/.../a.patch' -> SILENT
'git log --oneline -3 | cut -c1-80' -> SILENT
'python -B tools/ci_read.py jobs 123' -> SILENT
'git add a b && git commit -q -F <SP>\msg.txt | grep -i fatal; git push -q origin main' -> SILENT
'git cherry-pick pile/x/batch-1 | tail -2' -> SILENT
'cp C:\...\agent-a26b94d005f6a80c8/docs/x.md docs/x.md' -> SILENT
'git stash list' -> SILENT
'git checkout -b new-branch' -> SILENT
'git restore --staged f' -> SILENT
"python -B - <<'EOF'\nimport json\nprint(open('logs/journal/dev1.jsonl').read().count('>'))\nEOF" -> SILENT
'python -B -c "import json,sys; print(json.load(open(\'a.json\'))[\'k\'])"' -> SILENT
[PS] 'Get-Content f | Select-Object -First 5' -> SILENT
[PS] 'git status 2>&1' -> SILENT
```
(b), verbatim excerpts. Refused as expected: `cd docs && ls`, `X=1 cd docs`, `time cd docs`, `command cd docs`, `\cd docs`, `eval cd docs`, `pushd docs >/dev/null`, PS `Set-Location -Path docs`, `& { Set-Location docs }`, `$(Set-Location docs)`, `[Environment]::CurrentDirectory = 'docs'`; `echo x>docs/a.md`, `>docs/a.md`, `exec 3>docs/a.md`, `{ echo x; } > docs/a.md`, `cat <<'EOF' > docs/a.md`, `echo x > /c/QAFactory/forge-repo/docs/a.md` (from the scratchpad), `echo x > ../../../docs/a.md` (from the worktree), PS `x *> docs\a.md`, PS here-string `| Set-Content docs\a.md`, `sed -n -i`, `sed --in-place=.bak`, `perl -i -pe`, `python -X utf8 -c`, `C:/Python313/python.exe -u -B -c`, `py -3 -c "open(…,'r+')"`, the `pathlib.Path` alias, the `with open` heredoc; `echo x >> logs\journal\dev1.jsonl`, PS `Out-File -Append -FilePath logs\journal\dev1.jsonl`, `json.dump(…, open('JJ','a'))`, `sed -i '$a x' JJ`; `git checkout HEAD <dirty>`, `git checkout <dirty>`, `git checkout docs`, `git restore -W -S`, `git reset --hard HEAD~1`, `git stash` (1 path), `git stash -u` (14 paths), `git -C docs checkout -- …`, `git switch -f main`, `git checkout --force`, `git clean -f -d -x` (24 paths), PS `git checkout -- <dirty> 2>&1`.

False passes and refusals are quoted verbatim under B-1..B-3 and F-1..F-8 above.

c, verbatim: `plain words 1024KB 0.434s`; `git commit -m quoted 1024KB 0.720s`; `python -c read 1024KB 0.940s ctx`; `heredoc body 1024KB 0.267s`; `unclosed dq w/ escapes x8000 16KB 0.950s`; `32KB 4.44 s / _mask_quoted_segments 32KB 2.24 / _classify_pyc_payload 32KB 2.2`; `python -c " unclosed x4000 43KB 0.008s`; `heredoc openers 64 + unterminated 78KB 0.081s`; `PS dirs ending in backslash 47 KB 0.01 s`.

d, verbatim: `empty rc=0`, `null rc=0`, `Read rc=0`, `unknown rc=0`, `str input rc=0`, `BOM -> {"hookSpecificOutput": {… "permissionDecision": "deny" …}} rc=0`, `broken rc=0`, `NUL rc=0`.

Scratch artefact: `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\f92520fc-f552-4e47-9d06-efbc3daae572\scratchpad\cleanrepo` (a fresh `git init` with one empty commit, used for B-3's probe). No repository file was written except this report.

Needed beyond the manifest: `tools/hook_liveness_probe.py`, `tools/test_journal_per_developer.py`, `docs/SIBLING_MAP.md`, `tools/install_parity_anchors.json` (read only).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1 Bash arithmetic and [[ ]] comparisons refused as content writes: '(( n > 5 ))', 'echo $(( 3 > 2 ))', 'for ((i=10; i > 0; i--))', '[[ abc > abb ]]' -> DENY '<n> is a file of a git working tree' (tools/hygiene_gate.py _tokenize 304-331 + redirect loop 1102-1111); fix: arithmetic/test regions as a Bash capability row, no redirect inside",
    "B-2 only the first rollback shape per command is measured (hygiene_gate.py 1154-1155): 'git checkout -- README.md && git reset --hard' on a dirty tree -> SILENT; fix: rollback_forms list measured each, permission_audit re-keyed same commit",
    "B-3 subshell cd not carried into resolution (after_cd 1054/1083/1149/1156): '( cd <clean repo> && git reset --hard )' from a dirty cwd -> DENY naming the cwd repo (refusal on an unresolved target); '( cd docs && git checkout -- <dirty rel> )', '( cd logs/journal && echo x >> dev1.jsonl )', '( cd sub && make ); echo x > docs/a.md', 'd=$(cd docs && pwd); echo x > docs/a.md' -> SILENT; fix: per-region cd scope, literal prefix composed in decide()",
    "B-4 merge-blocking outside owns: tools/hook_liveness_probe.py:1334-1337 anchors the old journal text; replace with a substring of the new MSG_JOURNAL_BLOCK in the same merge (owns extended by the Lead)"
  ],
  "fixes": [
    "F-1 tee: every non-option argument is a target ('tee /dev/null docs/a.md', 'tee /dev/null logs/journal/dev1.jsonl' SILENT)",
    "F-2 PowerShell aliases sc/ac into _TEE_LIKE; '$x = Set-Location' assignment prefix",
    "F-3 PowerShell double-quote escape is the backtick: dq_escape capability row read by masks and tokenizer ('Get-Item \"C:\\x\\\"; Set-Location docs; \"y\"' SILENT)",
    "F-4 quadratic QUOTED_SEGMENT_RE (32 KB of escape pairs 4.44 s): linear scanner or a size cap passing with a marker",
    "F-5 rollback -C directory through _absolute_target (MSYS /c/... gives 'addressed directory absent')",
    "F-6 _gate_call: resolved dotted name in _FREE_OPEN_DOTTED_NAMES ('from io import open as o' SILENT)",
    "F-7 _first_path_arg: split '-Path:value' (false refusal on the value word)",
    "F-8 Lead's call: journal pattern narrowed to logs/journal/*.jsonl and routing-log (scratch logs/out.jsonl refused)",
    "F-9 formatted texts over 350: cap shown target/dir (MSG_MUTATION 379 with an 80-char target)",
    "F-10 permission_audit.py:37-52 docstring rewritten (old classes, _classify, git scrubs)",
    "F-11 split _collect_signals (1036-1182, 146 lines, nesting 5) per class",
    "F-12 advisory _PY_HEAD derived from PAYLOAD_INTERPRETERS (python3.12)",
    "F-13 dead conditions at 1156 and the unreachable capability default at 1315",
    "F-14 bash/sh/cmd as PAYLOAD_INTERPRETERS rows with payload_classifier None (bash -c write SILENT, unnamed)"
  ],
  "class_completeness": "Surfaces named and walked: the M1 redirect recogniser (B-1: arithmetic, [[ ]], process substitution, fd forms), rollback collection (B-2: chains), subshell-cd scope (B-3: M1, M3, journal, rollback, after-close leak), quoting per shell (F-3), path resolution (F-5). In-artifact neighbours enumerated in the review. SIBLING_MAP: axis 10 kept (gitcmd), axis 11 convergence queued (Q-5, hooklib.walk handles B-1/F-3), axis 18 no raise, axis 34 F-3/F-14. Outside owns: B-4, Q-1..Q-4.",
  "trail": {
    "read": [
      "C:/QAFactory/forge-repo/.claude/worktrees/agent-a26b94d005f6a80c8/tools/hygiene_gate.py (1-1480)",
      "C:/QAFactory/forge-repo/.claude/worktrees/agent-a26b94d005f6a80c8/docs/tasks/specs/reports/t-112-c1-hygiene-gate.md",
      "C:/QAFactory/forge-repo/docs/tasks/specs/fg-context-and-hygiene.md (8-82, 198-317, 430-457)",
      "C:/QAFactory/forge-repo/docs/tasks/critic-diff-brief.md",
      "C:/QAFactory/forge-repo/.claude/worktrees/agent-a26b94d005f6a80c8/tools/hook_liveness_probe.py (905-912, 1324-1340)",
      "C:/QAFactory/forge-repo/.claude/worktrees/agent-a26b94d005f6a80c8/tools/test_journal_per_developer.py (755-776)",
      "C:/QAFactory/forge-repo/.claude/worktrees/agent-a26b94d005f6a80c8/tools/permission_audit.py (36-57) and the diff of permission_audit.py, warn_layers.json, gitcmd.py",
      "C:/QAFactory/forge-repo/docs/SIBLING_MAP.md (267-280, 522-533)",
      "C:/QAFactory/forge-repo/tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_hygiene_gate.py tools/test_permission_audit.py tools/test_warn_messages.py tools/test_gitcmd.py -q (worktree)", "result": "359 passed in 13.41s"},
      {"command": "decide() probes of the 16 (a) commands", "result": "all SILENT"},
      {"command": "decide() probe: if (( n > 5 )); then echo big; fi", "result": "DENY: 5 is a file of a git working tree"},
      {"command": "decide() probe: git checkout -- README.md && git reset --hard (dirty main clone)", "result": "SILENT"},
      {"command": "decide() probe: ( cd <scratch clean repo> && git reset --hard ) from the dirty main clone", "result": "DENY: 1 path(s) under C:\\QAFactory\\forge-repo"},
      {"command": "purity: _collect_signals on 12 samples with fs/subprocess/clock/open patched to raise", "result": "purity: all 12 samples ran"},
      {"command": "timing: escape pairs after an unclosed quote x16000 (32 KB)", "result": "4.44 s"},
      {"command": "fail-open via stdin: empty, null, Read, Bashh, str input, broken, NUL", "result": "rc=0 silent each; BOM payload decoded and judged"}
    ]
  }
}
```
