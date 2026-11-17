# t-1243 Card B1 (FG7-59) report: hook line, generators, gates, pins

Tree: `C:/QAFactory/forge-repo/.claude/worktrees/wb-int` (head d6cdb4bd). Nothing committed, staged or reset; `.githooks/pre-commit`
untouched; `.githooks/pre-commit.next` created as a byte copy with the retargets. No `*_PATH` variables used. Never `cd`: every run
was a `( cd <wt> && ... )` subshell.

## Behaviours (1)-(9)

1. DONE `tools/coordinator_rules.py` (new): `COORDINATOR_FILES` (5 names, spec order), `coordinator_lines(root, source)`: stdlib only
   (os, re, stat; e16), never raises, ASCII only, presence by `stat` (absent / empty / directory / unreadable, all MISSING lines with
   the git door; good files still listed; no good file -> no read line). Resume prints "re-read only if your context no longer holds
   them" in place of "before your first dispatch, acceptance or commit".
2. DONE `tools/session_context.py`: `main()` appends `coordinator_rules_lines()` after layer A, before the compact pointer, outside
   `build_context_lines` (e6, e7); import/run failure -> `COORDINATOR RULES: unavailable (<exc>) -- read <literal> yourself` with
   `_COORDINATOR_FALLBACK_FILES` (e2, pinned equal to the module's tuple); `boot_path_files` appends `COORDINATOR_FILES` after
   BOOT.md's names and before CLAUDE.md (dedupe kept, e17); `CLAUDE_WARN` 58500 -> 16700 = ceil(14495 x 1.15 / 100) x 100 (CLAUDE.md
   measured 14495 bytes on this tree), comment names the LOWERING and its cause.
3. DONE `tools/agents_md.py`: `build_body` = `build_claude_body` + `build_coordinator_blocks` (each coordinator file under
   `<!-- begin X -->` / `<!-- end X -->`; a missing one is exit 2 naming it). `AGENTS.md` regenerated: 117130 bytes.
4. DONE `tools/mechanism_gate.py`: MECHANISM_PREFIXES += `COORDINATOR.md`, `tools/coordinator_rules.py`; docstring line 14 -> COORDINATOR.md
   rule 10, net list (point 6) names COORDINATOR.md; `test_mechanism_gate.py` (docstring + variant rows in the template-homes and
   boundary tests), `test_mechanism_gate_md.py` (one row).
5. DONE `tools/install_parity_anchors.json` (CRLF kept): `routing-policy` keeps 29 anchors; new unit `routing-policy:coordinator`
   (host COORDINATOR.md, kit_path `toolkit/CLAUDE.md`) takes 60; lead-ranking-exam item 2 anchor retargeted per A's report.
6. DONE `tools/tests/test_role_carriers_one_owner.py`: OWNER_KEYS routing:rule-9, rule-9-exit, cost:cap -> COORDINATOR.md; POINTERS
   retargeted; the `CLAUDE.md -> PROJECT.md § Сессия форджа` pointer dropped; TOC rebuilt (COORDINATOR.md carrier; Command hygiene and
   Language rows; PROJECT.md `Язык → CLAUDE.md § Язык`; `Все темы → COORDINATOR.md § Contents`); `need` += COORDINATOR.md; K-STALE
   (four regexes of the card, 16 rows incl. positive control and the two negatives, scan of the whole tracked tree, a row that
   SIBLING_MAP.md and TWO_VOCABULARIES.md are scanned) and K-WORKER (no `^@`, no `read COORDINATOR`, 5 negative-control rows).
7. DONE AGENTS.md regenerated with `agents_md.py --repo <wb-int>` (above).
8. DONE `.githooks/pre-commit.next`: whole file copy, comments of the factory-rules-index gate (lines 50-52) and the AGENTS.md gate
   retargeted. The architecture-index comment (line 55) names no CLAUDE.md, so no change there. Not placed.
9. DONE `tools/architecture_index.py` docstring: no longer imported, cap 3072 kept.

Tests changed: `test_session_context.py` (helpers `_nf`, `_CB`, `_seed_coordinator`; BOOT BUDGET pins compute counts and bytes from the
fixture; real-repo imports row -> `[]`; agents_md agreement test uses `build_claude_body`; new rows: line present per source
(startup/None/clear/compact/resume), 5 files x 3 damages (absent/empty/directory), all absent + non-ASCII root, import fails, run
fails, fallback == COORDINATOR_FILES, hostile root, MAX_LINES + compact order, boot_path_files dedupe); `test_agents_md.py`
(fixture carries coordinator files; `claude_part()`; list-order row; missing-file row per name; size tuner moved to COORDINATOR.md).

## Witness (one run after all edits; the test file edits of the last step were included)

`( cd <wb-int> && python -B -m pytest tools/test_session_context.py tools/test_session_context_layer_a.py tools/test_compact_snapshot.py tools/test_agents_md.py tools/test_mechanism_gate.py tools/test_mechanism_gate_md.py tools/test_streams.py tools/test_install_parity.py tools/tests/test_role_carriers_one_owner.py -q )`

```
FAILED tools/test_install_parity.py::test_k4b_regression_fixture_reports_all_five_outbound_markers
1 failed, 1455 passed, 2 skipped in 476.73s (0:07:56)
```

The one failure is outside my owns (`tools/test_install_parity.py`), see "Needed from integration". Every other file is green.

Other DoD commands (each in wb-int, subshell):

```
$ python -B tools/agents_md.py --check          AGENTS.md: up to date (117130 bytes)
$ python -B tools/install_parity.py --check     CLEAN units (47) / MISSING (0) / UNKNOWN (0) / informational (0)
$ python -B tools/architecture_index.py --check architecture index: up to date (29 invariants, 2682 bytes)
$ python -B tools/factory_rules_index.py --check factory rules index: up to date (59 rules) / (31 rules)
$ python -B tools/session_context.py </dev/null
MODEL: not provided by hook input -- verify tier yourself
BOOT BUDGET: 117987 bytes / 120000 (9 files) WARN | CLAUDE.md: 14495/16700
COORDINATOR RULES: read COORDINATOR.md, PROJECT.md, docs/FACTORY_RULES_INDEX.md, docs/ARCHITECTURE_INDEX.md, docs/OWNER_PRINCIPLES_INDEX.md (5 files, 92579 bytes) before your first dispatch, acceptance or commit; workers do not read these at boot -- a role reads only the section its role file names
```

Divergence from the spec's estimate: BOOT BUDGET is 117,987 (spec amendment 8: about 117.1 KB), headroom 2,013 bytes, because
COORDINATOR.md is 44,038 bytes (estimate 43.4 KB) and CLAUDE.md 14,495. Still under the 120,000 breach line.

## Needed from integration

1. `tools/test_install_parity.py` (outside owns; the test names `install_parity_anchors.json`): in
   `test_k4b_regression_fixture_reports_all_five_outbound_markers`, the `_tree(...)` dict needs a second entry
   `"COORDINATOR.md": fixture_text,` next to `"CLAUDE.md": fixture_text,`. Why: the five outbound markers (DRAFTING, TWO-LAYER CRITIC
   ENTRY, ...) now live in unit `routing-policy:coordinator`, whose host file the fixture tree lacks, so the run reports the
   unit as "file/dir not found" instead of the markers. Checked outside the repo (a temp tree with both files, the shipped manifest):
   `rc=1`, all five markers present in the output.
2. Place `.githooks/pre-commit.next` over `.githooks/pre-commit` (Lead, step 4); stage `AGENTS.md`.

## Deviations and decisions (each a one-line revert)

- K-STALE EXCLUDED list also holds `docs/PROJECT_FULL.md` (a snapshot "as it stood 11.11.2026") and `plans/BACKLOG.md` (frozen), which
  quote 1-9 rule numbers of their own day (Russian pattern hits); the spec named only `docs/ADOPTION_LEDGER.md`. Decided by me;
  tell me if the two should instead be retargeted.
- With no coordinator file present, `coordinator_lines` prints MISSING lines only (no read line); the spec did not say.
- Resume wording: "re-read only if your context no longer holds them" replaces the "before your first dispatch, acceptance or commit" clause.
- Hygiene: none to confess (no `git` state change, no file outside owns edited).

## Analogs noticed, not widened

- `agents_md.py` HEADER constant still reads "from CLAUDE.md (+ its imports)"; changing it moves the AGENTS.md bytes (owns allow it; left to Lead's wording).
- `.gitattributes` pins CLAUDE.md/BOOT.md/the indexes to LF because the boot budget reads on-disk size; COORDINATOR.md and PROJECT.md are
  now measured by size too and are not pinned (A's report already named it; outside owns).
- `_scan_claude_imports`/`claude_imports` and the `incl. imports` suffix machinery now has no production input (CLAUDE.md has no
  `@` lines); kept, since K-WORKER forbids the lines and a regression there is exactly what the budget line would show.

## Read beyond the manifest

`tools/test_install_parity.py` (the failing reader), `tools/fixtures/host_pre_delivery_CLAUDE.md`, `tools/session_context.py` main/boot code.

## Re-run after the Lead's answers (owns widened by `tools/test_install_parity.py`; no commit)

Edit: `"COORDINATOR.md": fixture_text,` added to the `_tree(...)` dict of `test_k4b_regression_fixture_reports_all_five_outbound_markers`, nothing else.
K-STALE EXCLUDED also names `docs/PROJECT_FULL.md` and `plans/BACKLOG.md` (accepted by the Lead as frozen records, like ADOPTION_LEDGER.md).

```
( cd wb-int && python -B -m pytest <the same 9 files> -q )
1456 passed, 2 skipped in 742.79s (0:12:22)
agents_md --check: AGENTS.md: up to date (117130 bytes)
install_parity --check: CLEAN units (47) / MISSING (0) / UNKNOWN (0)
architecture_index --check: up to date (29 invariants, 2682 bytes)
factory_rules_index --check: up to date (59 rules) / (31 rules)
BOOT BUDGET: 117987 bytes / 120000 (9 files) WARN | CLAUDE.md: 14495/16700
COORDINATOR RULES: read COORDINATOR.md, PROJECT.md, docs/FACTORY_RULES_INDEX.md, docs/ARCHITECTURE_INDEX.md, docs/OWNER_PRINCIPLES_INDEX.md (5 files, 92579 bytes) before your first dispatch, acceptance or commit; workers do not read these at boot -- a role reads only the section its role file names
```

## Fix round t-1250 (F1-F7)

- F1 DONE: `tools/tests/test_role_carriers_one_owner.py::STALE_RES` gains `CLAUDE.md `? § (Rule )?(?!11\b)\d`, `Cost gates` in regex 2, `(?!11\b)` in the "rule N of CLAUDE.md" regex; four STALE_ROWS (`§ 3` True, `§ Rule 12 · Cost gates` True, `§ 11` False, `rule 11 of CLAUDE.md` False).
- F2 DONE: one helper `k_worker_hits` read by the pin and by `test_k_worker_negative_controls`; `read\W{0,3}COORDINATOR` (re.I), inline `@x.md` tokens outside code spans; inline row flipped to True; rows for markup, code span and `a@b.md`.
- F3 DONE: `tools/coordinator_rules.py::_git_prefix`: `git -C "<root>"`, no cap; a non-ASCII or quote-bearing root prints bare `git`. Tests: expected text quoted; new rows for a space root, a Cyrillic root (parametrized), and a 250-char root (text only; Windows cannot create such a directory).
- F4 DONE: `Bad.__str__` root in `test_coordinator_lines_never_raises_on_a_hostile_root`, plus the drift pin (module line == `sc.coordinator_rules_lines` line == literal text). Note: the Bad root is caught inside `coordinator_lines` (via `_unavailable`), so the hook's own except body is reached only by the existing boom row; the pin compares the two texts.
- F5 DONE: `tools/agents_md.py` HEADER names `coordinator_rules.COORDINATOR_FILES`; AGENTS.md regenerated (117191 bytes).
- F6 DONE: `.gitattributes` text eol=lf for COORDINATOR.md, PROJECT.md, SYSTEM_PROMPT.md, DECISIONS.md, CURRENT_CONTEXT.md. No renormalize.
- F7 DONE: md-file row dropped in `tools/test_mechanism_gate_md.py::test_mechanism_paths_filters_prefixes_with_boundary`.
