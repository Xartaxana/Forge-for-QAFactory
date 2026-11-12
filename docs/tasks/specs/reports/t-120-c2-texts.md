# t-120 C2 + node P (C-merge paragraphs) -- report

Uncommitted, unstaged edits in the main clone. No code, no test file, nothing in the worktree.

## Per file: what changed (old -> new)

CLAUDE.md (section "Command hygiene" only)
- preamble: `Every "custom" form of a command is a permission request to the operator. For all sessions and subagents here:` -> `The deployment runs in auto mode; four behaviours are refused by tools/hygiene_gate.py, every other form is allowed.` + one "Doors:" line (`git -C <dir> <cmd>`, `python -B <abs path>`, a Bash `( cd <dir> && ... )` subshell, a PowerShell child shell, a byte copy (`cp`/`Copy-Item`) and its restore). `git stash push` is NOT in the list.
- point 1: permission motive absent; narrow-target rule and "full sets run on CI, never on this machine" kept (shortened); added the defining sentence `the canonical form of a tool = its correctly invoked form, the invocation that finds a known sample`. Anchor `1. Tests -- the canonical form, from the repo root:` still matches.
- point 2: byte-identical (not edited). Point 6 and the pt.6 table: byte-identical (not edited).
- point 3: `Don't prefix commands with cd ... and don't append 2>&1 -- both break the allowlist match` -> `The shell's working directory never moves (cd, Set-Location): refused.` (doors are the "Doors:" line; "allowlist match" removed).
- point 4: `not python - <<EOF, not python -c "...replace..."` -> content-write refusal (redirect, tee, sed -i, python -c writing a git-tree file's literal path is refused); header `4. File edits -- only via Edit/Write tools` kept.
- pt.4 table, rows a/b kept: a -> `legitimate: committed and reviewable` (col 2 unchanged); b -> `outside this point's scope, the gate stays silent; an unresolvable payload gets one WARN`.
- point 5: `not printf with $(date)` -> `other writes to logs/journal/*.jsonl or logs/routing-log.jsonl are refused` (gate file scope, see disagreement 2).
- point 7: (a), (c), (d) keep their meaning (shortened); (b) rewritten: the gate refuses checkout/restore/reset --hard/clean -f/stash push of a dirty path whatever its status was before, so the byte copy is the only road for a probe. Intro "(a mutation probe, a red-probe, "corrupt and restore")" shortened to "(a probe)".
- bytes (`wc -c`): file 41725 before -> 41688 after (net -37; only this section changed, so the section is 37 bytes smaller).

SKILL.md: step 2 table: removed rows `grep/cat/python -c` reading, `cd X &&`/`2>&1`, canonical pytest form, poll loop (3 rows kept: python edit, journal, git push); added a note under the table naming what left and why (poll loops -> cost finding, CLAUDE.md rule 7). Step 3 head: new sentence `Steps 3-5 apply to a deployment that runs with permission prompts; in auto mode they are not a hygiene duty.`

PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:
- check 27 (hygiene breakdown): `FOUR classes (2>&1, cd, python -c, journal)` -> `four REFUSAL classes of tools/hygiene_gate.py (cd, content write, journal, rollback)`; SHAPES from `--summary` (`HYGIENE_CLASS_LABELS`), VERDICTS from the gate's denials in transcripts; baseline 12.11 (39/68/58/1 unique) not comparable, new baseline recorded.
- check 27 (a): violation = a refusal-class call NOT refused, or a named residual (file-level copies onto tree files, non-literal targets, scripts outside the repo writing into it, unclassified interpreters) found by reading suspects; compound commands, `2>&1` in Bash, `python -c` reads, poll loops not counted (poll loops = check 17 cost). "ad-hoc read bypassing Read/Grep" and "bypassing the canonical pytest form" removed. RELATIVE NUMBER / REGISTRY STATUS items kept.
- check 27 (c): from `git checkout --`/`restore` search -> the gate's dirty-path refusals counted from transcripts + every `rollback not checked` marker read by hand.
- check 11 (one sentence): `Command hygiene -- tools/hygiene_gate.py.` -> adds `(declared population: every non-empty Bash/PowerShell command string, the HYGIENE row of tools/warn_layers.json; no measured kind yet, so its share is "n/a (population not measured)")`.

docs/SIBLING_MAP.md:
- row `tools/hygiene_gate.py`: `command hygiene 3-4` -> `command hygiene 3, 4, 5, 7`.
- axis 11: one "Queued (C1, F-C4, t-120)" paragraph (own masks and recognizers, not `hooklib.walk`; moving them queued).
- axis 10: one reader line (`hygiene_gate._tree_root`, a `.git` path walk).
- axis 34: one row "A content write into a git tree (C1, t-120)" (one refusal in every syntax; non-python interpreters = named residuals as data rows).

## Spec items (spec 309-312, section 8 "Check 27" / "Check 11", four SIBLING_MAP items)
309 preamble: present. 310 points 1-7: present (numbers 1-7 unmoved). 311 ready list: present, no stash. 312 skill step 2 + scope sentence: present. Check 27: present. Check 11 hygiene population: present. SIBLING_MAP row, axis 11, axis 10, axis 34: present.

## Disagreements spec vs gate file (gate wins)
1. Rollback class: gate docstring and `ROLLBACK_SHAPES` include `stash` (push/save) and `switch --discard-changes`/`checkout -f`; spec line 310 names only checkout/restore. CLAUDE.md point 7 (b) names stash push; `switch --discard-changes` omitted for bytes (the "these" in 7 (b) is wider than the list).
2. Journal refusal covers only `logs/journal/*.jsonl` and `logs/routing-log.jsonl` (`_JOURNAL_RE`); point 5 says so. A "rollback not checked" marker exists (`MSG_ROLLBACK_NOT_CHECKED`); named in check 27 (c), not in CLAUDE.md (bytes).
3. HYGIENE row of warn_layers.json: `reachable: unmeasured` (no measured kind in warn_density.py), so check 11's population sentence says "declared population" with "n/a" density, not a measured share.
4. Gate cd door for PowerShell is a child shell `powershell -NoProfile -Command "Set-Location <dir>; <cmd>"`; CLAUDE.md says just "a PowerShell child shell".

## Anchors of tools/install_parity_anchors.json
Checked by script (every anchor of CLAUDE.md and PROCESS units tested as literal substring): exactly ONE no longer matches.
- CLAUDE.md: old `3. Don't prefix commands with \`cd <dir> && ...\`` -> proposed `3. The shell's working directory never moves` (`3. The shell's working directory never moves (\`cd\`, \`Set-Location\`): refused.` is the line).
- Check 27 anchors (`27. **Permission/hygiene audit of the window.** Run`, `ITS OWN`, `RELATIVE NUMBER`, `WITH NO NAMED BASE, a REGISTRY ENTRY'S STATUS CLAIMED FROM`, `PARTIAL READ`, `UNSAFE ROLLBACK OF CORRUPTION:`, `THE "TRUNCATED REGISTRY WINDOW -> STATUS CLAIM" LINK:`, `HONEST CAVEAT:`): all still match. Other CLAUDE.md anchors incl. points 4a/4b, 5, 6, 7 (`BYTE COPY,`, `FROM IT;`): all still match.

## Pointers checked (read-only)
- builder.md:61 "CLAUDE.md command hygiene point 6" -> point 6 exists, unchanged. critic.md:67/74, designer.md:43 "hygiene point 6" -> resolve. Point 6 "canonical form (point 1)" -> point 1 keeps the defining sentence. SKILL.md "command hygiene point 6" (adjacent-class section) resolves. SKILL.md steps 4/5/6 text still mentions allowlist (kept by spec, scoped by the step-3 sentence). PROJECT.md names hygiene points only via pointer lines; numbers 1-7 unmoved. AGENTS.md not touched. Protocol check 27 still mentions "the skill's steps 3-5" (check 27 (b)) -- resolves.

## Witness (key-presence script, never committed)
Script: `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\f92520fc-f552-4e47-9d06-efbc3daae572\scratchpad\keys_c2.py` (reads each file, asserts a key present or absent; last row is a deliberately absent control key).
Source:
```
import sys
R = "C:/QAFactory/forge-repo/"
CHECKS = [
    ("CLAUDE.md", "four behaviours are refused by", True),
    ("CLAUDE.md", "the canonical form of a tool", True),
    ("CLAUDE.md", "git -C <dir>", True),
    ("CLAUDE.md", "python -B <abs path>", True),
    ("CLAUDE.md", "allowlist match", False),
    ("CLAUDE.md", "permission request to the operator", False),
    (".claude/skills/permission-audit/SKILL.md", "in auto mode they are not a hygiene duty", True),
    ("PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md", "four REFUSAL classes", True),
    ("docs/SIBLING_MAP.md", "command hygiene 3, 4, 5, 7", True),
    ("CLAUDE.md", "THIS KEY IS DELIBERATELY ABSENT", True),   # negative control
]
fails = 0
for f, key, want in CHECKS:
    text = open(R + f, encoding="utf-8").read()
    ok = (key in text) == want
    fails += not ok
    print(("PASS" if ok else "FAIL"), f, repr(key), "want_present=%s" % want)
print("total FAIL:", fails, "(expected 1: the negative control)")
sys.exit(1 if fails else 0)
```
Run `python -B <that path>` output:
```
PASS CLAUDE.md 'four behaviours are refused by' want_present=True
PASS CLAUDE.md 'the canonical form of a tool' want_present=True
PASS CLAUDE.md 'git -C <dir>' want_present=True
PASS CLAUDE.md 'python -B <abs path>' want_present=True
PASS CLAUDE.md 'allowlist match' want_present=False
PASS CLAUDE.md 'permission request to the operator' want_present=False
PASS .claude/skills/permission-audit/SKILL.md 'in auto mode they are not a hygiene duty' want_present=True
PASS PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md 'four REFUSAL classes' want_present=True
PASS docs/SIBLING_MAP.md 'command hygiene 3, 4, 5, 7' want_present=True
FAIL CLAUDE.md 'THIS KEY IS DELIBERATELY ABSENT' want_present=True
total FAIL: 1 (expected 1: the negative control)
```
(First run failed on `the canonical form of a tool` because of a capital T at a sentence start; fixed, rerun above.) `wc -c CLAUDE.md`: 41725 before, 41688 after.

## Needed beyond the manifest
`tools/install_parity_anchors.json` (read-only, anchors), `.claude/agents/{builder,critic,designer}.md` (pointer grep), `tools/install_parity.py` header (matching = literal substring), `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` check 17 existence not verified (check 27 points poll loops there per spec).
Analogs noticed (not edited): SKILL.md header description and its "Boundaries" still speak of prompts/allowlist (scoped by the step-3 sentence only); check 17 cost wording should receive poll loops (node P later wave owns check 17 (d) already).
