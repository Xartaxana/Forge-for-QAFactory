# t-1250 critic topic 2 (worker-boot, Card B1, FG7-59): code review

Base: wb-int worktree, HEAD d6cdb4bd + the uncommitted tree (12 tracked files, untracked `tools/coordinator_rules.py`,
`.githooks/pre-commit.next`). Spec: `docs/tasks/specs/20261117-worker-boot-and-round-rules-spec-r2.md` §1, §2 hook line,
§6 e1-e18, §8 Card B1 (1)-(9), Lead decisions on t-1239. Builder report: `docs/tasks/handoffs/t-1243-card-b1.md`.

## Verdict

**NEEDS WORK** (fit_with_fixes): 0 blocking findings, 7 fixes, all before merge. Behaviours (1)-(9) are implemented
and the mechanical layer reproduces. The gaps are in the two new detectors (K-STALE, K-WORKER), the door that the
MISSING line prints, one label that is now false, and one LF-pin sibling outside the card's owns. The accept decision
belongs to the Lead (rule 6).

## Findings

**F1 (fix before merge): K-STALE misses neighbouring citation forms and has one false red against e18.**
`tools/tests/test_role_carriers_one_owner.py::STALE_RES`. The surface is the stale-citation detector. Its neighbour
forms were walked with a probe that imports the test's own `stale_hits` (trail T3):
- miss: `CLAUDE.md § 3`, `CLAUDE.md § 9`, `CLAUDE.md § 11a`, `CLAUDE.md § Rule 4 · witness scope and the BATCH CANON`,
  `CLAUDE.md § Rule 12 · Cost gates`, `` `CLAUDE.md` § Rule 2 · drafting → designer ``, `CLAUDE.md § Cost gates`. These
  are exactly the cell grammar of the old Contents table, and the grammar FG7-52 prescribes (`<file> § <number>`), so a
  re-introduced stale TOC cell passes the pin.
- false hit: `rule 11 of CLAUDE.md` → HIT. Regex 3, `\b(?:rule \d+\w?|R13-g) of CLAUDE\.md`, has no `(?!11\b)`. This
  breaks e18 ("a citation of a rule still living in the cited file never fails the pin"). The spec's regex is defective
  here and the builder copied it as written.
- Today no live file has the missing forms: the wide scan finds 0 in the scanned set and 8 in the excluded record
  `docs/tasks/handoffs/t-1233-card-a.md`, which is the positive control. So this is a detector gap, not a stale citation
  on disk.
Fix: (a) add `(?<!toolkit/)CLAUDE\.md`?\s*§\s*(?:Rule\s+)?(?!11\b)\d` and extend regex 2's alternation with `Cost gates`;
(b) regex 3 → `\b(?:rule (?!11\b)\d+\w?|R13-g) of CLAUDE\.md`; (c) add STALE_ROWS for `CLAUDE.md § 3` (True),
`CLAUDE.md § Rule 12 · Cost gates` (True), `CLAUDE.md § 11` (False) and `rule 11 of CLAUDE.md` (False).

**F2 (fix before merge): the K-WORKER negative controls test a copy of the check, and the check misses two forms.**
`test_k_worker_negative_controls` re-types both regexes inline. `test_k_worker_claude_md_has_no_import_and_no_coordinator_read_duty`
holds the real ones. If the production regex is edited, the controls stay green, so they cannot catch a regression
(Q5(a)). Neighbour forms that escape:
(i) `` Read `COORDINATOR.md` `` and `read [COORDINATOR.md](...)`. `read\s+COORDINATOR` allows no markup between the
two words.
(ii) An inline `@COORDINATOR.md`. Claude Code memory imports also work inside a sentence: the documented example is
"See @README for project overview". The row `("# T\ntext @PROJECT.md\n", False)` pins the opposite belief. This comes
from documentation and was NOT measured here (rule 13). The fix errs toward a false red, which is the allowed side.
CLAUDE.md has no such token today (grep: 0 hits).
Fix: one helper `k_worker_hits(text)` read by both tests. Widen to `read\W{0,3}COORDINATOR` (re.I) and to an `@path.md`
token outside code spans. Flip the inline row to True.

**F3 (fix before merge): the MISSING line's git door does not work on some roots.**
`tools/coordinator_rules.py::coordinator_lines` prints `git -C %s` with `_ascii(root)` (200-character cap, `?` for
non-ASCII characters, no quotes). Probe (T4):
`git -C C:/My Projects/forge show origin/main:COORDINATOR.md` is two arguments to git. A 250-character root is cut, so
the door names a path that does not exist. A Cyrillic root becomes `?????`. This is FR-2 by analogy: the door must be
one the reader can use.
Fix: quote the root and drop the cap. When the root is not ASCII-clean, print the door without `-C`: hygiene point 3
keeps the session cwd at the repo root. Add one variant row, a root with a space, to
`test_coordinator_line_names_a_missing_empty_or_directory_file_with_the_git_door`.

**F4 (fix before merge): two builders of the `unavailable` line, and the module branch is untested (Q6/Q7).**
`coordinator_rules._unavailable` (:60-65) and the except body of `session_context.coordinator_rules_lines` (:270-279)
both format `COORDINATOR RULES: unavailable (...) -- read ... yourself`. The structure is forced: e2 needs the fallback
when the import fails, and "never raises" needs the in-module branch. The module branch is reachable only by a root
whose `__str__` raises (probe T4: it does fire). No row covers it. The precedent in the same file is
`_layer_a_unavailable_line`: one text, "rather than risking two messages that drift apart".
Fix: add a `Bad.__str__` root to `test_coordinator_lines_never_raises_on_a_hostile_root`, and assert that its line
equals `sc.coordinator_rules_lines` under the same exception text. That row is the drift pin.

**F5 (fix before merge): `agents_md.HEADER` is now false (Q7).**
`tools/agents_md.py:43` says "from CLAUDE.md (+ its imports), .claude/settings.json and .claude/agents/*.md". AGENTS.md
now also carries the five coordinator files (`AGENTS.md:156-1091`). The builder flagged this and left it.
Fix: name `coordinator_rules.COORDINATOR_FILES` in HEADER and regenerate AGENTS.md (`--check` keeps them in step).

**F6 (fix before merge, outside the card's owns: the Lead widens commit #2): no LF pin for the files now measured by
size.** `.gitattributes` says it pins to LF "the boot files [...] session_context.py measures BY ON-DISK BYTE SIZE".
Behaviour (2) makes `COORDINATOR.md` and `PROJECT.md` budget files, and neither is pinned:
`git check-attr eol` = unspecified, and `core.autocrlf` = true on this machine. Today both are LF on disk (44038 / 35072
= blob size). A fresh checkout here gets CRLF: +499 and +276 bytes, which cuts the 2013-byte headroom to about 1238.
The same class already shows on the BOOT.md list: SYSTEM_PROMPT.md, DECISIONS.md and CURRENT_CONTEXT.md are CRLF on
disk (+18/+45/+26 over the blob) and unpinned. Card A's report raised it too ("B1 / Lead").
Fix: add `COORDINATOR.md`, `PROJECT.md`, `SYSTEM_PROMPT.md`, `DECISIONS.md` and `CURRENT_CONTEXT.md` with
`text eol=lf` to `.gitattributes`, same commit.

**F7 (fix before merge, minor): a duplicate row (Q5(e)).**
`tools/test_mechanism_gate_md.py:132-133` adds COORDINATOR.md to `test_mechanism_paths_filters_prefixes_with_boundary`.
It asserts what `tools/test_mechanism_gate.py::test_mechanism_paths_template_homes_and_self_protection` (the `extra`
list, about :109-111) already asserts through the same `mg.mechanism_paths` door. Card (4) asks for one variant row.
Fix: drop the md-file row.

## Standing questions

- **Q1 fit to spec:** (1) done: stdlib only (`os, re, stat`, e16), stat presence, ASCII; door defect F3. (2) done: the
  call sits after layer A and before `compact_snapshot_lines`, outside `build_context_lines` (main, read);
  `boot_path_files` appends after BOOT.md's names with dedupe; CLAUDE_WARN = ceil(14495×1.15/100)×100 = 16700, checked
  by hand (16669.25 → 16700), with comment and NAMED LOWERING present. (3) done. (4) done: prefixes, and docstring
  points 3 and 6 retargeted (:14, :62). (5) done: install_parity CLEAN 47 (T2). (6) done; detector gaps F1 and F2.
  (7) done: AGENTS.md up to date (T2). (8) done: the diff against pre-commit is comments only (:50-53, :59), ASCII and
  LF; judged as live code, the gate set is identical, and `agents_md.py --check` stays unconditional, so a COORDINATOR.md
  edit without regeneration is refused. (9) done, cap 3072 kept.
- **Q2 the builder's own decisions:** no present file → MISSING lines only. That is safe: every line carries the duty
  and the door. The resume form replaces the "when" clause, consistent with §2. EXCLUDED += `docs/PROJECT_FULL.md` and
  `plans/BACKLOG.md`: PROJECT.md calls both frozen records, so this is safe, and the Lead has accepted it.
- **Q3 seams:** `session_context.py` changes are additive: one call in main, one loop, two helpers.
  `agents_md.build_body` keeps its name and its one caller (:318); the split-out `build_claude_body` is read by the
  tests only. Nothing is reordered.
- **Q4 class completeness:** axis 31: pins done; K-STALE and K-WORKER gaps are F1 and F2. Axis 18: CLAUDE_WARN lowered
  and named. Axis 1: AGENTS.md regenerated, header F5. Axis 34: Codex gets the same list from the same generator. The
  byte budget measured on disk vs `.gitattributes` (named in its own header, not on a map axis) is F6, file named. The
  artifact sweep of `coordinator_lines`' surface walked magnitude (long root: F3), encoding (non-ASCII: F3), broken
  input (None/5/NUL: rows exist; raising `__str__`: F4) and empty input (`Path("")` cannot reach it: main resolves the
  root).
- **Q5 tests:** (a) the line rows, the MAX_LINES/compact-order row (it would catch a move into `build_context_lines`)
  and the fallback pin all have killing power; the K-WORKER controls do not (F2). (b) Expected values come from the
  fixture (7 bytes per file) and from §2's literal text. (c) Every door has rows; door usability does not (F3).
  (d) The rewritten tests (`build_claude_body`, `claude_part`, real-repo imports → `[]`) and the dropped CLAUDE.md →
  PROJECT.md pointer are covered by Card A's move. (e) F7. (f) `tools/test_volume.py` counts root `AGENTS.md` (+938) as
  product ("Unsure -> product"), so the diff is not over volume and no `tests-over:` is owed. (g) No new test file.
- **Q6 duplication:** `unavailable` builder twice (F4). `_COORDINATOR_FALLBACK_FILES` is the copy the spec mandates and
  is pinned equal. `_coordinator_files` follows the existing `_required_githooks` pattern (:1484). `_ascii` is one more
  copy of an existing class (`session_context._ascii_sanitize:1064`, `tier_echo:141`, `journal_echo:487`,
  `wiring_check:261`, ...). It is forced locally by e16 (stdlib-only; session_context cannot be imported). Proposed node
  for the Lead to open (owner Lead, forge/7): one stdlib ASCII-line helper adopted by those copies. The clone ratchet:
  the `forge-check` job has not run (tree uncommitted), so the Lead reads it after commit #2.
- **Q7 code quality:** no new function over 60 lines or 3 nesting levels (`coordinator_lines` is 26 lines). False
  label: F5. Branch reachable only by a hostile input and untested: F4.
- **Q8 hygiene:** forge only. `install_parity_anchors.json` is CRLF on disk and LF in the blob (713/0 CR), the usual
  autocrlf checkout; the diff is 38/30 lines, with no EOL churn.
- **Q9 in-tree ratchets:** `CLAUDE_WARN` 58500 → 16700 is a lowering (tighter), named in the comment. No ratchet row
  raised. dup/lint: read from `forge-check` after commit.
- **Q10 architecture:** no file under `ai-packages/` (diff stat), so no AR-n. VARIETY: forge-only; on a tree without
  the coordinator files the hook prints MISSING with a door, never a silent default.
- **Q11 judgment:** K-STALE and K-WORKER are shape checks on citation strings. No census applies (package-only); no
  judgment moved into code.
- **Q12 one road:** Codex and Claude Code read the one list `COORDINATOR_FILES`. None found: grep of the added lines for
  `python|java|kotlin|language|lang` gives 1 hit, the TOC row `| Language | CLAUDE.md § Язык |`, which is not a branch.

**For the Lead, not a finding against B1:** BOOT BUDGET is now WARN at every session start (117987 > BOOT_WARN 110000)
and prints a top-3 breakdown each time. Spec amendment 8 foresaw the total (about 117.1 KB) but not a WARN that is
always on. Proposed: a forge/7 node, owner Lead, to re-derive or diet. The last BOOT_WARN raise rested on the owner's
word, so this may need it again.

## Spot-checks

- Witness numbers ↔ diff: BOOT BUDGET 117987 = 3 BOOT.md files + 5 coordinator files + CLAUDE.md (9 files). Live hook
  output reproduces the head line and the breakdown COORDINATOR.md 44038, PROJECT.md 35072, CLAUDE.md 14495.
- Builder's negative "no other caller of build_body": own grep over tools/*.py + .githooks → only agents_md.py:318
  (positive control: the same grep finds the definitions at :102/:127).
- "CRLF kept" for the anchors file: checked by CR count (above).

## Trail

- Read: spec r2 §1, §2 (hook line), §6, §8 B1, Lead decisions (lines 34-100, 281-320, 476-512, 626-667); handoff
  t-1243 (whole); `tools/coordinator_rules.py` (whole); diffs of session_context.py, agents_md.py, architecture_index.py,
  mechanism_gate.py, test_role_carriers_one_owner.py, test_session_context.py (new rows), test_agents_md.py,
  test_mechanism_gate*.py, test_install_parity.py; session_context.py :195-210, :1205-1235, :1407-1418, :1434-1460,
  :2700-2760; `.githooks/pre-commit.next` :40-90 and its diff against pre-commit; `.gitattributes`; test_volume.py
  header; BOOT.md Read lines; COORDINATOR.md/PROJECT.md/CLAUDE.md `^@` grep.
- T1 `( cd wb-int && python -B tools/agents_md.py --check )` → `AGENTS.md: up to date (117130 bytes)`.
- T2 `python -B tools/install_parity.py --check` → `CLEAN units (47)` / `MISSING (0)` / `UNKNOWN (0)`;
  `python -m pytest tools/tests/test_role_carriers_one_owner.py -q` → `210 passed in 13.29s`.
- T3 scratch probe `probe_stale.py` / `probe_stale2.py` (imports the test's `stale_hits`): misses and the false hit as
  listed in F1; wide-form scan: scanned set 0, control record 8.
- T4 scratch probe `probe_root.py`: `Bad()` root → `unavailable (RuntimeError: bad str)`; space root → unquoted
  `git -C C:/My Projects/forge`; 250-character root → truncated door.
- T5 `git check-attr eol` COORDINATOR.md/PROJECT.md → unspecified; `core.autocrlf` → true; sizes on disk vs blob for the
  six boot files as in F6.
- `python -B tools/session_context.py </dev/null` (wb-int) → `BOOT BUDGET: 117987 bytes / 120000 (9 files) WARN |
  CLAUDE.md: 14495/16700`, breakdown 44038/35072/14495.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axis 31 pins done, but the K-STALE neighbour forms (CLAUDE.md section-number and Rule-heading cells, Cost gates; false red on rule 11 of CLAUDE.md) are F1 and the K-WORKER forms are F2. Axis 18: CLAUDE_WARN lowered and named. Axis 1: AGENTS.md regenerated, HEADER label F5. Axis 34: one list for Codex and Claude Code. Byte budget measured on disk vs .gitattributes LF pins: F6, outside owns, the Lead widens commit #2.",
  "fixes": [
    "F1 tools/tests/test_role_carriers_one_owner.py::STALE_RES: add the section-number/Rule-heading form and Cost gates; add (?!11) to regex 3; four STALE_ROWS",
    "F2 same file: one k_worker_hits helper read by both K-WORKER tests; widen to read with markup between and inline @path.md tokens; flip the inline row",
    "F3 tools/coordinator_rules.py::coordinator_lines: quote the root in the git door, no 200-char cap, omit -C for a non-ASCII root; a space-root variant row",
    "F4 tools/test_session_context.py::test_coordinator_lines_never_raises_on_a_hostile_root: add a raising __str__ root and pin its line equal to session_context.coordinator_rules_lines",
    "F5 tools/agents_md.py:43 HEADER: name the coordinator files; regenerate AGENTS.md",
    "F6 .gitattributes (Lead, commit #2): text eol=lf for COORDINATOR.md, PROJECT.md, SYSTEM_PROMPT.md, DECISIONS.md, CURRENT_CONTEXT.md",
    "F7 tools/test_mechanism_gate_md.py:132-133: drop the COORDINATOR.md row that duplicates test_mechanism_gate.py template-homes"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-worker-boot-and-round-rules-spec-r2.md",
      ".claude/worktrees/wb-int/docs/tasks/handoffs/t-1243-card-b1.md",
      ".claude/worktrees/wb-int/tools/coordinator_rules.py",
      ".claude/worktrees/wb-int/tools/session_context.py",
      ".claude/worktrees/wb-int/tools/agents_md.py",
      ".claude/worktrees/wb-int/tools/mechanism_gate.py",
      ".claude/worktrees/wb-int/tools/architecture_index.py",
      ".claude/worktrees/wb-int/tools/tests/test_role_carriers_one_owner.py",
      ".claude/worktrees/wb-int/tools/test_session_context.py",
      ".claude/worktrees/wb-int/tools/test_agents_md.py",
      ".claude/worktrees/wb-int/tools/test_mechanism_gate.py",
      ".claude/worktrees/wb-int/tools/test_mechanism_gate_md.py",
      ".claude/worktrees/wb-int/.githooks/pre-commit.next",
      ".claude/worktrees/wb-int/.gitattributes"
    ],
    "reruns": [
      {"command": "python -B tools/agents_md.py --check (wb-int)", "result": "AGENTS.md: up to date (117130 bytes)"},
      {"command": "python -B tools/install_parity.py --check (wb-int)", "result": "CLEAN units (47), MISSING (0), UNKNOWN (0)"},
      {"command": "python -m pytest tools/tests/test_role_carriers_one_owner.py -q (wb-int)", "result": "210 passed in 13.29s"},
      {"command": "python -B tools/session_context.py </dev/null (wb-int)", "result": "BOOT BUDGET: 117987 bytes / 120000 (9 files) WARN | CLAUDE.md: 14495/16700"},
      {"command": "scratch probes probe_stale.py, probe_stale2.py, probe_root.py", "result": "K-STALE misses and false hit as in F1; door defects as in F3; raising __str__ root reaches the module unavailable branch"}
    ]
  }
}
```
