# FG7-52 - pointer_lint: paths, FR/P/rules ranges, gate numbers and TOC anchors in rule texts checked against their home (draft card)

task: t-1437 | node: forge/7/FG7-52 | feature: F19 | designer draft, forks returned (section 8), nothing decided for the Lead.
Sources: batch-7 row FG7-52 (`plans/piles/forge/batch-7-vhodyashchie-4.md:77`), finding 20261116 item 3, finding 20261112 (class "a pointer outlives its object").
Dependency FG7-50: accepted (`263809e8`, t-891, batch file line 75). FG7-51 (boot rebuild by topics): pending, named dependency only (F12).

## 0. Target on main, measured (file:symbol)

What does not exist yet:
- `tools/pointer_lint.py` and `tools/test_pointer_lint.py`: Glob gives nothing. Control: the same Glob finds `tools/language_sites.py`, `tools/md_table.py` and `tools/agents_md.py`.

What already exists: hand-held pointer checks, all in ONE test file; nothing scans the texts by code:
- `tools/tests/test_role_carriers_one_owner.py::POINTERS`: 34 hand rows (:75-108).
- `::TOC_POINTERS`: 51 hand rows (:119-155, :157-170), one per cell of `COORDINATOR.md` § Contents (:17-53) and `PROJECT.md` § Оглавление (:18-35); comment :112 "FG7-52 later scans them by code"; `docs/SIBLING_MAP.md:492` "until FG7-52".
- `::main_documents`: the MAIN register (axis-31 table via `md_table.table_after`, rows whose "Owner / pointer" cell starts with owner/procedure).
- `::STALE_RES` (K-STALE): `CLAUDE.md rule N` with N != 11.
- `::DELETED` + `::forbidden_hits` (K-NOBRIEF): deleted files by path or stem; row :360 says "fences are not exempt".

Homes and the numbers counted in them:
- FR: `ai-packages/qa-factory/design/factory-rules.md`, 59 openers `**FR-n ` (Grep count). FR-58 and FR-59 are present (:271, :289).
- P: `docs/OWNER_PRINCIPLES.md`, 31 lines `- **Pn.**` (Grep count).
- rules: `COORDINATOR.md` headings `### Rule 1` … `### Rule 13`. Rule 11 is a pointer heading (:278) to `CLAUDE.md` § The dispatch form.

Constants: `tools/dispatch_manifest.py:115 DESIGNER_THRESHOLD = 3`; `tools/dispatch_gate.py:1664 PARALLEL_CAP = 6`; `tools/agent_budget.py:109-110 WORKER_WARN = 250000`, `WORKER_STOP = 400000`.

Wiring:
- `.githooks/pre-commit` runs 6 blocking `gate` lines plus the forge_metrics WARN block (:66-77). No line pins `gates: ok (N checks)`: Grep `gates: ok` over tools/ gives 0 hits; the same pattern finds 3 in `.githooks/pre-commit`.
- `.github/workflows/forge-check.yml` job forge-check: its run steps are pinned in order by `tools/test_workflows.py::FORGE_CHECK_RUNS` (:140-161).
- `tools/mechanism_gate.py::MECHANISM_PREFIXES` (:216-289) must name every tools/*.py that pre-commit runs. This is enforced by `tools/test_mechanism_gate.py` (:943 reads the live pre-commit; :1031 checks the import closure).

Sibling model: `tools/language_sites.py` is INERT (docstring :5; Grep `escape_check|language_sites` over workflows and `.githooks/*` hits escape_check only, the control). Its design is the model (exit 2 = cannot judge, no `--update`), not its wiring; FG7-27 (`docs/tasks/specs/20261118-fg7-27-language-sites-one-road-card.md` D2-D4) wires it at the same three points.

Map dead paths belong to F6-10 (`plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:55`, pending); `piles.py` does not read `SIBLING_MAP` (Grep over tools/*.py hits mechanism_gate.py and others, not piles.py).

### 0.1 Stale today (measured; the rest is an estimate)

Path pointers. The measured sample is the backticked tokens of CLAUDE.md, COORDINATOR.md, `.claude/agents/*.md`, `.claude/skills/*/SKILL.md`, PROJECT.md, docs/TESTING.md and docs/TEAMWORK.md: about 330 tokens. Each candidate was checked by Glob.

| id | carrier:line | pointer | state |
|---|---|---|---|
| S1 | docs/TESTING.md:30 | `docs/tasks/handoffs/t-1467-f6-42-test-volume.md` | dead: Glob `docs/tasks/**/*t-1467*` gives none; the control `*t-1233*` finds `t-1233-card-a.md`. The 20261116 finding listed it, and it is still there. |
| S2 | .claude/skills/permission-audit/SKILL.md:56 | `logs/routing-log.jsonl` (the journal) | stale: the file is not in the tree, the journal is `logs/journal/<dev>.jsonl` |
| S3 | PROJECT.md:191 | `logs/routing-log.jsonl` "история до 08.10, только чтение" | the file is not in the tree (Lead file) |
| S4 | .claude/agents/critic.md:60 | PROCESS/CRITIC_EXAM.md (bare, not backticked) | absent: the rule asks for an exam that is not registered (F10) |
| S5 | PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:535 | "more than 4 WRITING workers" | number stale vs PARALLEL_CAP 6. The 20261112 finding p.4 named it, and it is still unfixed. |

Absent, but legitimately so (exemption candidates, F7/F8):
- CLAUDE.md:106 `logs/routing-log.jsonl`: a refused target of hygiene point 5.
- critic-exam-gen SKILL.md: `PROCESS/CRITIC_EXAM.md` on 8 lines. scout-exam-gen SKILL.md: `PROCESS/SCOUT_GOLDEN_SET.md` on 8 lines. Both are outputs the skill writes.
- critic.md:270 `tools/language-sites-baseline.json`: "Once … exists". FG7-27 creates it.
- permission-audit:90 `.claude/settings.local.json`: a host file, absent.
- `tools/dev.config.yaml` at COORDINATOR.md:353, PROJECT.md:191 and session-retro:32: gitignored (`.gitignore:13`). It exists locally but is absent on CI.

Slash tokens that are not paths: `Xartaxana/QAFactory`, `origin/main`, `pile/<slug>/batch-<N>`, `experiment/thinking-roles`, `forge/5/F5-2`.

Bare names: `test-layers.json`, `selftest.py`, `classes.md`, `wiring_check.py`. Package-relative: `scripts/tests/fixtures/judgment-census.json`, `fixtures/env-facts-baseline.json`. All live by suffix.

Not measured (estimate, not verified). The builder's first `--check` gives the count:
- docs/RUNBOOK.md: 100 pointer lines.
- docs/SIBLING_MAP.md: 234 lines. The 20261112 finding lists about 10 dead paths; still present on main: :140 `skills/qa-story/index.yaml`, :172 `experiments/driver-golden*` and `freeze_package.sh`, :224 `references/controller-paths`, :158/:264 `onboarding-hooks/`, :171 `logs/routing-log.jsonl`.
- PROCESS/*.md and the other MAIN docs: 97 lines.
- Package design/*.md: 514 lines over 17 files. architecture.md alone holds 34 `dev:` pointers (Grep counts).

Ranges (pattern `FR-1…FR-N`, `P1–PN`, `rules 1-N` over the tree minus worktrees, logs, specs and piles):
- These match their homes: PROJECT.md:8 FR-1…FR-59; PROJECT.md:23, :54, :65 P1–P31; SIBLING_MAP.md:94, :496 P1…P31/P1–P31; DELEGATION_TABLE.md:4 "COORDINATOR.md rules 1-13".
- Same form, not a claim about the home: SIBLING_MAP:325 "P1–P23" (dispatch_gate path checks); critic.md:144 "rules 1-16" (its own); OWNER_PRINCIPLES.md:5 `### P1–P9` (heading); COORDINATOR.md:344 "rules 1-12" (rule 13 citing the rules before it, no file named); WEEKLY_CALIBRATION:6 "rules 1–10" (no home); SIBLING_MAP:492 "routing rules 1-10, 11a, 12, 13" (enumeration, union 1-13).
- 0 stale today among home-named ranges. The class is real: old `.claude/worktrees/*/DELEGATION_TABLE.md:4` read "CLAUDE.md rules 1-13" / "rules 1-11".

Numbers:
- Right: COORDINATOR.md:32 "Six writers", :103 "3 OR MORE numbered items … 3 or more files", PROJECT.md:226 "цель держать 6 пишущих", RUNBOOK.md:257 "не больше 6 пишущих".
- Stale: S5.
- `WARN 250K, STOP 400K` (COORDINATOR rule 12) matches agent_budget.

TOC anchors: TOC_POINTERS is green by its own test (not re-run here).

## 1. Architecture

- Package reach. Card A does not touch `ai-packages/qa-factory/`: it is a forge tool over forge texts. Card B (only with F3 (a)) fixes stale pointers in package design texts, so it carries the AR lines below as its commit `architecture:` lines. Form: `tools/architecture_gate.py`.
- AR-13. The axis-31 register has ONE reader: `main_documents` moves from the test into `pointer_lint.py`, and the test imports it. Fence and table reading goes through `md_table` (`table_after`, `md_lines_outside_fences` where needed), and git calls go through `gitcmd.git`. Change check: Grep `table_after(lines, "Axis 31")` gives exactly one site, in pointer_lint.py.
- AR-15. One survivor for "a pointer in a rule text resolves". The two hand-row/regex copies (TOC_POINTERS, K-STALE) retire into the tool (F1). Change check: after the card, Grep `TOC_POINTERS|STALE_RES` over tools/ gives 0 hits outside the tool and its test.
- AR-18 / AR-9 / FR-1 / FR-2. One refusal line shape (D5). It names the carrier, the line, the pointer, what the home says and the door.
- AR-20. The exemption file only shrinks: a stale row is red, and no command writes rows. Change check: a diff that adds a row carries its `why`, and the critic sees it.
- AR-22. Every field has a producer: exemption rows are written by hand under review (the writer is the person in the diff, judged by the critic), and the tool is their one reader.
- AR-28 / FR-59. An unknown is never a pass: exit 2 on an unreadable register, a home, a constant or git (E13).
- FR-4. The informed pass is an exemption row with a reason. No silent skip.
- AR-29, the owner each check serves:
  - path exists: data (code; presence join).
  - range vs home count: data (join).
  - number vs constant: data (join).
  - anchor heading present: data (presence).
  - an exemption's `why` is good: judgment (critic, accepted by the Lead).
  - Census class: none. It is a forge tool outside the package `scripts/` census, and no check classifies a role's judgment.
- variety: none -- a forge tool over forge rule texts. It reads no project, language, host, tracker or runner value. Card B adds package texts as a scanned set, not a variety axis.
- P31 (one road). Every pointer check goes through one tool. Package texts are a named node (Card B), not an exclusion (F3).

## 2. Design

**D1 - scanned texts.**
- The set is the axis-31 MAIN register, read by `main_documents` (F2). AGENTS.md is excluded: it is a generated copy, and its sources are scanned.
- Card A drops register entries under `ai-packages/` (Card B owns them).
- The TOC tables are two data rows of the tool: `(COORDINATOR.md, "Contents", "Where")` and `(PROJECT.md, "Оглавление", "Раздел")`.

**D2 - pointer kinds.**
- `P` path:
  - Backticked tokens with a file suffix or a slash.
  - With F4 (a), also bare tokens whose first segment is a tracked top-level entry of the repo and that end in a file suffix.
  - Strip a trailing `:N`, `:N-M` or `::symbol` and trailing punctuation `.,;:)`.
  - `C:/QAFactory/forge-repo/` (and `\`) prefixes are normalised to repo-relative. Other absolute paths and URLs are skipped.
- `R` range (F5):
  - `FR-1…FR-N` anywhere.
  - `P1…PN` on a line that names the P home (`OWNER_PRINCIPLES` or "principle"/"принцип").
  - `<file> rule(s) A[-B]` on a line that names a home file. For example, "COORDINATOR.md rules 1-13" is checked; "acceptance of rules 1-12" is not.
  - Separators `…`, `...`, `-`, `–`, `—`.
- `N` number: rows of the tool constant `NUMBER_PAIRS = [(constant "tools/x.py::NAME", carrier, regex with one group)]` (F6). The constant is read by `ast` (literal assignment, no import). The captured group is a digit or a number word: EN one…twelve and RU один…двенадцать / шесть, casefolded.
- `A` anchor: TOC cells split on ` + `. Each part is `<path>` or `<path> § <anchor>`. A PROJECT cell with no file names its own heading, or uses `X → <file> § <anchor>`.
- With F1 (a), the `<file> rule N` and `§ N` forms of K-STALE are R/A pointers too.

**D3 - resolution.**
- Listing: `git ls-files -z` (index, NUL-separated, so non-ASCII names are not octal-quoted).
- Path, in order:
  1. a rooted token (its first segment is a top-level repo entry) must equal a tracked path or be a tracked dir prefix;
  2. otherwise, some tracked path ends with `/` + token, or equals it;
  3. a token starting with `./` or `../` resolves from the carrier's folder. Escaping the repo root is red.
  4. a placeholder token (`<…>`, `*`, `N`/`x` segments written as `<x>`) is judged by its fixed directory prefix up to the first placeholder segment. That prefix must prefix a tracked path.
  5. not resolved, but `git check-ignore --no-index` matches (one batched call): resolved (a local-only file).
  6. otherwise, an exemption row `<carrier>|<token>`: resolved.
  7. otherwise red.
- Range: the home maximum is the largest n of its opener regex (FR: `^\*\*FR-(\d+) `; P: `^- \*\*P(\d+)\.\*\*`; rules: `^### Rule (\d+)` in COORDINATOR.md, `^\s*(\d+[a-z]?)\. ` items for a named file).
  - A range starting at 1 is a full-set claim. Its enumeration (the range plus the comma-joined items that follow on the line) must reach the home maximum.
  - Every named item must exist in the named file. So "CLAUDE.md rules 1-13" is red, because CLAUDE.md holds only item 11.
  - Heading lines are not full-set claims, and a home is not range-checked against itself.
- Number: the captured value must equal the constant. A pair whose regex finds nothing in its carrier is red.
- Anchor: there must be a heading whose text (after `#`s, whitespace squashed, casefolded, `«»` stripped) starts with the anchor. For a numeric anchor `N`, `Na` or `N-M`, each N must be a line `^\s*N[a-z]?\. ` or a heading `Rule N`/`N.`.

**D4 - exemptions.**
- Carrier: `tools/pointer-lint-exempt.json`, `{"rows": {"<carrier>|<token>": {"why": "<one line>"}}}` (F8).
- No line number in a key; one row covers every occurrence in its carrier.
- A row is red when its token no longer occurs in its carrier, when it now resolves without the row, or when `why` is empty.
- The file has no writer command.

**D5 - CLI, output, exits.**
- `python -B tools/pointer_lint.py --check [--repo PATH]`.
- Exits: 0 pass, 1 red, 2 cannot judge.
- On success stdout prints `pointer_lint: ok (F files, P pointers)`; stderr prints the wall time. Neither line carries `WARN`, which matters for the pre-commit output policy at :5-8.
- On red: `pointer_lint: N finding(s)`, then one line per finding: `<carrier>:<line>: [<P|R|N|A|X>] <pointer> -> <what the home holds> (home: <file>) -- door: fix the pointer, or add "<carrier>|<token>" with a why to tools/pointer-lint-exempt.json`.
- Exit 2 names what could not be read.
- The tool always scans the whole set: no staged-only mode, because a deleted target is not a staged text.

**D6 - wiring.** The packet follows FG7-27's pattern: enforcement files travel in a patch, and the Lead places them.
- `.githooks/pre-commit`: after `gate python tools/agents_md.py --check`, after FG7-27's language_sites line if it has landed, and before the forge_metrics WARN block, add a 2-line comment and `gate python tools/pointer_lint.py --check`.
- `forge-check.yml`: one step `- run: python tools/pointer_lint.py --check` right after `python tools/agents_md.py --check`.
- `test_workflows.py::FORGE_CHECK_RUNS`: the row at the same index, with a comment that names FG7-52 (no `.gitlab-ci.yml` mirror).
- `mechanism_gate.py::MECHANISM_PREFIXES` gains two entries:
  - `"tools/pointer_lint.py",  # .githooks/pre-commit (pointer lint, FG7-52)`
  - `"tools/pointer-lint-exempt.json",  # DATA that decides what pointer_lint.py lets pass`
  - Its imports, `md_table` and `gitcmd`, are already listed.

**D7 - the role-carriers test (F1 (a)).**
- Remove `TOC_POINTERS` (and the `POINTERS + TOC_POINTERS` join) and the K-STALE block (`STALE_RES`, `STALE_ROWS`, `stale_*`, `test_no_scanned_file_cites_a_rule_that_left_claude_md`).
- `main_documents` is imported from `pointer_lint`.
- `POINTERS`, `OWNER_KEYS`, K-NOBRIEF and K-WORKER stay: they anchor whole sentences and stems, which are not pointers.
- The STALE_ROWS samples move as rows of the D3 range/anchor table, so no lost case.
- Docstring :15-18 is updated.

**D8 - the first run (F7 (a)).**
- Fix S1, S2 and S5 in the builder's owns.
- Put S3, the SIBLING_MAP dead rows and the `docs/SIBLING_MAP.md:551` TOC_POINTERS mention into the patch (Lead files).
- Exemption rows for the legitimate absents of 0.1.
- Every other red of the first run is fixed in owns, or put into the patch (Lead files), or exempted with a why. The count of each goes in the report.

**D9 - map rows (Lead, in the patch; F11).**
- Axis 31 "Detectors" (:560-564) gains `tools/pointer_lint.py` (paths, ranges, gate numbers, TOC anchors of MAIN documents).
- Row :551 drops the TOC_POINTERS clause.
- Rows :532 (dispatch_manifest) and :533 (dispatch_gate) name their number pairs ("`DESIGNER_THRESHOLD` <-> COORDINATOR.md rule 2", "`PARALLEL_CAP` <-> COORDINATOR.md :32, PROJECT.md p. 12, RUNBOOK.md 9(i)").
- Row :492 drops "until FG7-52".

**Error direction (designer rule 1; `main_documents` moves from a test helper to a gate input).**
- `main_documents` may only err to FEWER documents, which is a false pass. The guard is the positive control: CLAUDE.md, COORDINATOR.md, docs/TESTING.md and .claude/agents/critic.md must be present, else exit 2.
- Path verdicts:
  - For rooted tokens they err to false red; the door is an exemption row.
  - For bare names they err to false pass: a same-named file elsewhere rescues them (a named KNOWN MISS, critic Q6).
- Adversarial inputs that must stay safe: `../../..` past the root: red; `tools/x.py:12`, `tools/x.py::f`: path judged, line/symbol a named miss; backslashes normalised; a backticked path with spaces judged whole if suffixed; empty backticks, URLs, `origin/main`: skipped; a non-ASCII tracked name resolves; a fenced token is judged (E6).
- KNOWN MISSES (pinned as rows that assert NOT detected):
  1. A bare name rescued by a namesake.
  2. A range or rule pointer with no home named on its line.
  3. A `:line` or `::symbol` that moved.
  4. A gate number with no NUMBER_PAIRS row.
  5. An anchor in prose outside the two TOC tables.
  6. Partially staged text: pre-commit reads the working tree, and CI judges the committed tree.

## 3. Edges, each with its invariant

- E1. A rooted path whose file was moved or deleted is red, even when a file with the same basename exists elsewhere. Invariant: a rooted pointer to a path absent from the tracked tree, not ignored and not exempt, never passes.
- E2. A bare or package-relative name resolves by suffix. Invariant: no false red on a live suffix; the lenient side is a named miss.
- E3. A carrier-relative `../` resolves from the carrier folder; past the repo root it is red. Invariant: a pointer the tree cannot hold never passes.
- E4. A placeholder or glob path is judged by its fixed directory prefix. Invariant: an example template is not red while its folder lives; a template whose folder is gone is red.
- E5. A slash token that is not a path (no tracked first segment, no suffix) is skipped. Invariant: a branch, repo slug or node id never reds a commit.
- E6. A pointer inside a code fence or a quoted example is scanned like any line. A concrete dead path in an example takes an exemption row. Invariant: a fenced command that names a deleted tool is red, the same as K-NOBRIEF row :360 "fences are not exempt". An example with placeholders is never red (E4).
- E7. A FR/P/rules range whose home moved or shrank is red, naming the home's maximum and the file. Example: `CLAUDE.md rules 1-13` today, where CLAUDE.md holds only item 11. Invariant: a range pointer never names an item its home does not hold; an enumeration is judged as its union (SIBLING_MAP:492 stays green).
- E8. A gate number in prose that differs from the constant is red, naming `path::NAME = value`. Invariant: a registered number pair never passes with a different value. A pair whose sentence disappeared is red too, never a silent pass.
- E9. A number written as a word (Six, шесть): the word table maps it. Invariant: the same pair is judged whether it is written in digits or words; an unknown word is red (the regex captured something that is not a number).
- E10. Cyrillic working docs against package texts:
  - Anchors are casefolded with Unicode rules, and `«»` are stripped. Listing uses `-z`.
  - Package texts (English) are Card B. Their `dev:` prefix resolves against the repo root, and their bare paths resolve against the package root first.
  - Invariant: a non-ASCII heading or path resolves; a package pointer is never judged against the wrong root.
- E11 (TEMPORAL, the first run on today's tree). Before the Lead places the patch, the tool exists and runs by hand only, and no gate refuses. The Lead's apply commit holds the hook line, the CI step, the FORGE_CHECK_RUNS row, the MECHANISM_PREFIXES rows, the Lead-file fixes and the map rows together. The builder's branch already holds the in-owns fixes and the exemption file. Invariant: no commit on main has the gate with a red tree. The move that creates the gate is the Lead's `git apply` commit.
- E12 (the 10 s budget). There is no internal timeout and no skip flag; the wall time is printed. Expected well under 1 s for about 30 files plus one `git ls-files` (estimate, not verified). The DoD reports the real wall time. If it exceeds 10 s, the builder stops and returns a question. Invariant: the hook never passes by timing out.
- E13 (empty or absent inputs). Each of these exits 2:
  - the register table is missing, or fewer than the four control documents parse;
  - a home has zero openers;
  - a constant is not found by `ast`;
  - git is not available;
  - the exemption JSON is malformed.

  Two cases are not exit 2:
  - A register row whose file is absent is a P finding (red).
  - An empty scanned file has 0 pointers and passes.

  Invariant: an unknown is never a pass (AR-28).
- E14. An exemption row is red when it is stale (token gone, or path now resolves) or has no why. Invariant: an exemption never outlives its reason. This includes the critic.md:270 row on the day FG7-27 lands the baseline.
- E15. Cross-branch race: branch A deletes X and branch B adds a pointer to X. Each is green alone, and the merge is red. Invariant: forge-check on a push to main scans everything, so a red main is visible, never silent.
- E16. AGENTS.md (generated) is not scanned. Invariant: a stale pointer is reported once, at its source. Fixing a source that AGENTS.md copies regenerates AGENTS.md in the same commit.
- E17 (POSITIONAL, the pre-commit line). It goes after the blocking gates and before the WARN block. Invariant: the hook exit stays the FIRST failing gate's code, the order of the existing gates is unchanged (output policy :8), and no refusal follows the non-blocking forge_metrics block.

## 4. Builder cards

### Card A - the tool, its table, the first run, the placement packet

given: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-52-pointer-lint-card.md §0-§3, §5; tools/tests/test_role_carriers_one_owner.py::main_documents, ::TOC_POINTERS, ::STALE_RES, ::STALE_ROWS, ::FORBIDDEN_ROWS; tools/md_table.py::table_after, ::md_lines_outside_fences; tools/gitcmd.py::git; tools/dispatch_manifest.py::DESIGNER_THRESHOLD; tools/dispatch_gate.py::PARALLEL_CAP; tools/agent_budget.py::WORKER_WARN, ::WORKER_STOP; tools/test_workflows.py::FORGE_CHECK_RUNS; tools/mechanism_gate.py::MECHANISM_PREFIXES; .githooks/pre-commit; .github/workflows/forge-check.yml; docs/SIBLING_MAP.md:492, :532, :533, :551, :560-564; tools/language_sites.py (exit-code and no-`--update` model only)
owns:
C:/QAFactory/forge-repo/tools/pointer_lint.py
C:/QAFactory/forge-repo/tools/test_pointer_lint.py
C:/QAFactory/forge-repo/tools/pointer-lint-exempt.json
C:/QAFactory/forge-repo/tools/tests/test_role_carriers_one_owner.py
C:/QAFactory/forge-repo/docs/TESTING.md
C:/QAFactory/forge-repo/docs/RUNBOOK.md
C:/QAFactory/forge-repo/.claude/skills/permission-audit/SKILL.md
C:/QAFactory/forge-repo/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
C:/QAFactory/forge-repo/AGENTS.md
C:/QAFactory/forge-repo/docs/tasks/handoffs/t-<task>-fg7-52-wire.patch
non-goals: no edit that stays on the live paths of `.githooks/pre-commit`, `.github/workflows/forge-check.yml`, `tools/mechanism_gate.py`, `tools/test_workflows.py`, `docs/SIBLING_MAP.md`, `PROJECT.md`, `COORDINATOR.md` or `.claude/agents/*.md` (they travel in the patch); no package file (Card B); no change to POINTERS, OWNER_KEYS, K-NOBRIEF or K-WORKER; no `--update`/`--init` writer of the exemption file; no line-number or `::symbol` checking; FG7-51's boot rebuild
handoff: report (status line, first-run counts by kind: fixed in owns / in the patch / exempted, the wall time of `--check`) + the patch path; commit shas
edges: E1-E9, E11-E17 of §3; a first-run red in a file outside owns and outside the Lead files of the patch: stop and return a question naming file and pointer, write nothing for it
DoD: `python -m pytest tools/test_pointer_lint.py tools/tests/test_role_carriers_one_owner.py -q`, then `python -B tools/pointer_lint.py --check` (exit 0, wall time from stderr), then `python -B tools/agents_md.py --check`, then under the probe below `python -m pytest "tools/test_workflows.py::test_forge_check_steps_equal_the_ordered_list_and_there_is_no_scrub_anywhere" "tools/test_mechanism_gate.py::test_every_githooks_script_reference_is_covered_by_mechanism_prefixes" "tools/test_mechanism_gate.py::test_transitive_import_closure_of_live_wiring_is_covered_by_mechanism_prefixes" -q`
siblings: FG7-27 (same insertion points in pre-commit, forge-check, FORGE_CHECK_RUNS and MECHANISM_PREFIXES: whoever lands second rebases the patch; pre-commit order language_sites then pointer_lint; its baseline makes the critic.md:270 exemption stale, and whoever lands second drops the row); FG7-81 (package `named_by` pointers, package-side, not this tool: different carrier and grammar); F6-10 (map dead paths: F9); agents_md.py (AGENTS.md regenerated when a copied source changes)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-52-pointer-lint-card.md

Work, in order:
1. The tool per D1-D5 and the exemption file. `main_documents` moves into the tool, and the test imports it (D7).
2. The table `tools/test_pointer_lint.py`: one parametrised table, with ONE tmp git repo built once per module (fixture). The rows are the test lines below.
3. The first run per D8 on the real tree:
   - fix S1, S2 and S5 and any red in owns;
   - add the exemption rows;
   - note every red that falls in a Lead file.
4. D7 edits of the role-carriers test.
5. The packet, as a probe (CLAUDE.md hygiene 7):
   - take byte copies of `.githooks/pre-commit`, `.github/workflows/forge-check.yml`, `tools/mechanism_gate.py`, `tools/test_workflows.py`, `docs/SIBLING_MAP.md`, `PROJECT.md` and of every Lead file the first run touched, FIRST;
   - edit them per D6, D8 and D9, and run the DoD's last command and `pointer_lint.py --check`, with NO commit in between;
   - write `git diff -- <those paths>` to the patch path;
   - restore every path FROM its byte copy and report the hash comparison (restored = HEAD);
   - commit the patch alone.

test lines (strongest first):
- test: tools/test_pointer_lint.py::CASES, path rows. The cases are: rooted live; rooted deleted with a namesake elsewhere (red); bare suffix live; `../` past the root (red); placeholder with a live folder; non-path slash token (skipped); gitignored; exempt; in a fence (red). | expected from: §2 D2-D3, §3 E1-E6
- test: tools/test_pointer_lint.py::CASES, range rows. The cases are: `FR-1…FR-57` against 59 (red); `COORDINATOR.md rules 1-13` (ok); `CLAUDE.md rules 1-13` (red); the enumeration `rules 1-10, 11a, 12, 13` (ok); heading `### P1–P9` (skipped); "P1–P23" with no home named (skipped); the former STALE_ROWS samples. | expected from: §2 D3, §3 E7, `test_role_carriers_one_owner.py::STALE_ROWS` (moved)
- test: tools/test_pointer_lint.py::CASES, number rows. The cases are: "more than 4 WRITING" against 6 (red); "Six writers" (ok); the sentence gone (red); an unknown word (red). | expected from: §2 D3, §3 E8-E9
- test: tools/test_pointer_lint.py::CASES, anchor rows. The cases are: `COORDINATOR.md § Rule 2 · drafting → designer` (ok); `§ 21-24` with item 23 removed (red); `PROJECT.md § Сессия форджа` (ok, Cyrillic); a renamed heading (red). | expected from: §2 D3, the TOC_POINTERS rows (moved)
- test: tools/test_pointer_lint.py::CASES, exemption rows. The cases are: token gone (red); the path now resolves (red); empty why (red). | expected from: §2 D4, §3 E14
- test: tools/test_pointer_lint.py::CASES, cannot-judge rows. The cases are: the register missing; a home with 0 openers; a constant absent; malformed JSON. Each gives exit 2. | expected from: §3 E13
- test: tools/test_workflows.py::FORGE_CHECK_RUNS, a row `"python tools/pointer_lint.py --check"` right after the agents_md row (in the patch) | expected from: §2 D6
- test: none -- the hook line is an enforcement file. The behaviour it reaches is the CASES table plus the Lead's placement probe | expected from: CLAUDE.md enforcement-file rule

Lead placement (after acceptance, in the wave merge):
1. `git apply --check` the patch, then apply it.
2. Re-run the DoD's last two commands.
3. Placement probe: in a scratch worktree of the merged tree, edit a scanned text to cite `tools/no_such_tool.py` and commit. It must exit 1 with a `[P]` line. Revert the edit and confirm `gates: ok (N checks)`.
4. Commit with the axis lines per `tools/mechanism_gate.py`.

### Card B - package design texts (only with F3 (a); after Card A merges)

given: this spec §2 D3 and E10; the Card A tool; the register rows under `ai-packages/qa-factory/design/`
owns:
C:/QAFactory/forge-repo/tools/pointer_lint.py
C:/QAFactory/forge-repo/tools/test_pointer_lint.py
C:/QAFactory/forge-repo/tools/pointer-lint-exempt.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/
non-goals: no package script; no references/, skills/ or agents/ texts of the package (they are not register rows); no change to the scan grammar beyond the package root and `dev:`
handoff: report (first-run count per design file, fixed / exempted) + commit sha with `architecture:` lines (AR-13, AR-19) per tools/architecture_gate.py
edges: E2, E10, E13, E14; a design file that is a dated record (for example `codex-scout-incident-2026-09-19.md`): return a question (the register row, or a record exemption), never a mass exemption
DoD: `python -m pytest tools/test_pointer_lint.py -q`, then `python -B tools/pointer_lint.py --check`, then `python -B ai-packages/qa-factory/scripts/selftest.py --lang`
siblings: FG7-81 (package-side pointer check of test-layers.json, its own files)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-52-pointer-lint-card.md

test lines (strongest first):
- test: tools/test_pointer_lint.py::CASES, package rows. The cases are: `dev:docs/X.md` live; `dev:` dead (red); a package-relative `scripts/x.py` resolved at the package root. | expected from: §3 E10
- test: none -- the text fixes are documents; the witness is `--check` exit 0 | expected from: §2 D8

## 5. Readers of every touched file (rule 7)

The `owns_readers.py` block was not attached (facts: none). The Lead runs:
`python -B tools/owns_readers.py --paths tools/pointer_lint.py tools/test_pointer_lint.py tools/pointer-lint-exempt.json tools/tests/test_role_carriers_one_owner.py tools/mechanism_gate.py tools/test_workflows.py .githooks/pre-commit .github/workflows/forge-check.yml docs/SIBLING_MAP.md docs/TESTING.md docs/RUNBOOK.md PROJECT.md PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md .claude/skills/permission-audit/SKILL.md --names main_documents TOC_POINTERS STALE_RES MECHANISM_PREFIXES FORGE_CHECK_RUNS`.
Hand grep, with commands, until then:
- `.githooks/pre-commit` + `forge-check.yml`: Grep `githooks/pre-commit|"pre-commit"|'pre-commit'|forge-check\.yml|workflows/forge-check` over tools/ gives 11 files, 49 hits.
  - `mechanism_gate.py`: changes in the patch (D6).
  - `test_mechanism_gate.py` (:943, :1031 read the live hook): unchanged; green with the D6 row.
  - `enforcement_probe.py`: unchanged. It walks `.githooks/`, and a staged chain change runs wiring_check.
  - `wiring_check.py` (`_REQUIRED_GITHOOKS`, tracked, executable): unchanged. `git apply` keeps the mode.
  - `session_context.py` (`_required_githooks`): unchanged.
  - `test_enforcement_probe.py`, `test_wiring_check.py`, `test_session_context.py`, `test_wave.py`: temp-repo fixtures, unchanged.
  - `test_test_quarantine.py` (job name strings): unchanged.
  - `test_workflows.py::FORGE_CHECK_RUNS`: changes in the patch.
  - canon.yml calls forge-check by `workflow_call`: unchanged. It inherits the step.
- `tools/tests/test_role_carriers_one_owner.py`: Grep `test_role_carriers_one_owner|main_documents|TOC_POINTERS|STALE_RES` over tools, *.md, docs, PROCESS, agents and workflows.
  - SIBLING_MAP:492, :551, :560: change in the patch (D9).
  - PROJECT.md:58 and WEEKLY_CALIBRATION:1065 name it for K-NOBRIEF, which stays: unchanged.
  - AGENTS.md:716 is a generated copy: unchanged unless its source changes.
- `tools/pointer_lint.py` and `tools/pointer-lint-exempt.json` (new): readers after the card are pre-commit, forge-check, MECHANISM_PREFIXES, the test file and the role-carriers import. All are in this card.
- `docs/SIBLING_MAP.md`:
  - `mechanism_gate.py` MAP_PATH reads the axis headings. No heading changes (F11 (a)): unchanged.
  - `main_documents` reads the axis-31 table. Rows change only in non-owner cells, so MAIN is unchanged.
  - `md_table`: unchanged.
- `docs/TESTING.md`, `docs/RUNBOOK.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `permission-audit/SKILL.md`, `PROJECT.md`: text fixes of single lines.
  - Their pinned readers are `test_role_carriers_one_owner.py::OWNER_KEYS` and `::POINTERS` (TESTING.md, RUNBOOK.md, PROJECT.md anchors) and `tools/install_parity_anchors.json` (presence of rule text).
  - The builder confirms that no fixed line carries an anchor of either. The DoD's first command covers OWNER_KEYS and POINTERS. The install_parity check is `python -B tools/install_parity.py --check` (KNOWN MISS of the hand grep; the Lead's block decides).

## 6. Test cost (docs/TESTING.md)

- Layer: a table of cases (layer 3) for a new forge tool. `tools/test_pointer_lint.py` is "the same rule, not an exception" (TESTING.md:236-237). No `keep` row: forge tests have none.
- One tmp git repo per module, built once. Target < 10 s (`in N.NNs` tail in the report).
- Whole-run files in the DoD: 2, `test_pointer_lint.py` and `test_role_carriers_one_owner.py`. The other two are narrow node calls. Neither is a slow-list or `canon_only` file: those lists are package-only.
- Volume: test lines ≤ code lines. The tool is estimated at a few hundred lines; the table at 6 behaviours of roughly 4 rows each, plus the fixture.
- Rows moved from TOC_POINTERS and STALE_ROWS are net-negative in the role-carriers test.

## 7. Small choices closed by the designer

- Exit 0/1/2 and no writer command, as in language_sites.
- Whole scan always; no staged mode.
- `git ls-files -z` through `gitcmd.git`.
- `check-ignore` in one batched call.
- AGENTS.md excluded.
- Headings are not full-set range claims, and homes are not checked against themselves.
- Number words EN/RU one…twelve.
- NUMBER_PAIRS lives in the tool (code-shaped regex), and exemptions in JSON (data).
- Wall time goes on stderr.
- `:line` and `::symbol` are not judged (named miss).
- The refusal line names the door (FR-2).

## 8. Forks (the Lead decides)

- F1. The role-carriers test.
  - (a) TOC_POINTERS and K-STALE retire into pointer_lint; POINTERS, OWNER_KEYS, K-NOBRIEF and K-WORKER stay.
  - (b) Additive: the test is untouched. That leaves two roads for the same check (AR-15).
  - (c) POINTERS move too. They anchor sentences, not headings, so this loses strength.
  - Rec (a).
- F2. Scanned set.
  - (a) The axis-31 MAIN register: one register, and a new owner file is scanned when it joins the table.
  - (b) The finding's fixed list. It names deleted files (`plans/builder-rules.md`, `docs/tasks/critic-diff-brief.md`).
  - Rec (a).
- F3. Package texts. The register already lists `ai-packages/qa-factory/design/*.md`: 514 pointer lines, a dated incident record among them, and 34 `dev:` pointers.
  - (a) Card B in this spec after A. This is the one road. Cost: a first-run count that is unmeasured here, and record files need a decision.
  - (b) Leave package texts out. That is a P31 exclusion, so it goes to the owner.
  - Rec (a).
- F4. Bare paths.
  - (a) Also judge unbackticked tokens with a tracked first segment and a suffix. This catches critic.md:60 and adds SIBLING_MAP table-cell paths.
  - (b) Backticks only, as in the finding.
  - Rec (a).
- F5. Range grammar.
  - (a) FR everywhere; P and `<file> rule(s)` only when the home is named on the line; an enumeration is judged as its union. The miss is an unnamed home.
  - (b) A hand registry of every range pointer.
  - Rec (a).
- F6. Numbers.
  - (a) DESIGNER_THRESHOLD, PARALLEL_CAP and agent_budget WORKER_WARN/WORKER_STOP.
  - (b) Only the two constants the finding names.
  - Rec (a). Same class, and one row each.
- F7. First run.
  - (a) Fix all, plus exemption rows for legitimate absents.
  - (b) A baseline of every current stale pointer, shrink-only. It keeps lying to readers until shrunk.
  - Rec (a). The measured stale set is small (S1-S5). The SIBLING_MAP count is unknown; if the first run exceeds about 20 reds in Lead files, the builder returns a question before packing.
- F8. Exemption carrier.
  - (a) `tools/pointer-lint-exempt.json`, keyed `<carrier>|<token>`, with a why, stale rows red.
  - (b) Inline HTML-comment markers in texts. They spread a mechanism into rule texts and the boot budget.
  - Rec (a).
- F9. F6-10 overlap (onboarding-forge, pending): its map dead-path check is this tool on SIBLING_MAP.
  - (a) pointer_lint covers it. The Lead marks F6-10's map part "closed by FG7-52" in that pile. That pile is another zone, so it is the Lead's edit.
  - (b) Exclude SIBLING_MAP from the path kind.
  - Rec (a).
- F10. critic.md:60 makes running PROCESS/CRITIC_EXAM.md mandatory before an edit of critic.md, but the file does not exist.
  - (a) An exemption row "generated by critic-exam-gen on first run".
  - (b) Change the rule text to "run critic-exam-gen first when absent". This is a mechanism file and a rule meaning, so it belongs to the Lead or owner.
  - Rec (b) by the Lead, with (a) as the stopgap row in this card.
- F11. Map rows. The finding's pair list is stale: two pairs name the deleted `plans/builder-rules.md`, and TESTING<->PROJECT p. 2 and RUNBOOK §7<->PROJECT already stand in axis 31 (:494, :497).
  - (a) No new axis; D9 edits only.
  - (b) A new axis 39 "pointers <-> homes".
  - Rec (a).
- F12. Order with FG7-51 (pending).
  - (a) FG7-52 lands first, so the rebuild's moved homes are caught by code.
  - (b) After FG7-51. Fewer reds are fixed twice.
  - Rec (a).
- F13. Hook mode.
  - (a) A blocking `gate`, with the exemption door (FR-4).
  - (b) WARN only, like forge_metrics.
  - Rec (a). CI blocks either way.

## 9. Noticed, not widened

- forge-check.yml:2-4 "STAGED COPY: lives in docs/migration/": the file is live; a stale pointer in a non-scanned file (may ride in the patch).
- docs/OWNER_PRINCIPLES.md:3 "импорт из `CLAUDE.md`": the index is read via `COORDINATOR RULES:` (PROJECT.md:54); stale prose, not a pointer kind.
- «Как пишутся правила для агентов» is a heading in both PROJECT.md:244 and boot-diet SKILL.md: a possible two-owner case (critic Q6).

## 10. Reading trail

- Batch file :1-20, :52/:75-77/:106 (rows FG7-50/51/52/81); status column by Grep `| (ожидает|принято…) |$` (FG7-50 :75 принято 263809e8; FG7-51/52 ожидает).
- Both findings, read whole.
- .githooks/pre-commit and forge-check.yml, read whole.
- SIBLING_MAP :1-30, :138-173, :474-565; Grep for ranges and DESIGNER/PARALLEL there.
- test_role_carriers_one_owner.py :1-465.
- TESTING.md :36-95, :199-248.
- language_sites.py :1-60 and the def list.
- selftest.py :595-624.
- COORDINATOR.md :1-75, plus Grep for rule headings.
- PROJECT.md :18-36, :188-192, :222-233, plus the heading Grep.
- RUNBOOK :254-259; WEEKLY_CALIBRATION :1-10, :530-539; critic.md :56-62; critic-exam-gen SKILL :5-10; permission-audit SKILL :52-57.
- architecture.md :173-188 and the index; mechanism_gate.py :215-289; test_workflows.py :137-176.
- FG7-27 card :84-113, :191-238; FG7-81 card headings.
- .gitignore, read whole.
- Globs:
  - candidate-existence globs listed in 0.1, each with a positive member found in the same call;
  - `docs/tasks/**/*t-1467*` (none) against the control `*t-1233*` (found);
  - `.claude/settings*.json`;
  - `docs/retro/**`.
- Grep counts:
  - path tokens per file (18 files, 599 lines);
  - PROCESS and other files (97);
  - design (514);
  - `dev:` (34);
  - `gates: ok` (tools 0; .githooks 6);
  - readers of the hook and workflow (11 files, 49 hits).
- No script was run (no shell). Every count is a Grep or Glob result, as named.

## 11. Lead decisions (Lead 501cb4e0, 2026-11-18)

- F1 (a): TOC_POINTERS and K-STALE retire into pointer_lint; POINTERS, OWNER_KEYS, K-NOBRIEF, K-WORKER stay.
- F2 (a): the axis-31 MAIN register is the scanned set.
- F3 (a): Card B after Card A merges.
- F4 (a): unbackticked tokens with a tracked first segment and a suffix are judged too.
- F5 (a), F6 (a), F8 (a), F9 (a), F11 (a), F13 (a): as recommended.
- F7 (a): fix all plus exemption rows; over about 20 reds in Lead files the builder returns a question before packing.
- F10: (a) the stopgap exemption row in Card A now; (b) the rule-text change is a Lead text node later.
- F12 (a): FG7-52 lands before FG7-51.
- Order with FG7-90 (in review, edits forge-check.yml and test_workflows.py): before step 5 the builder merges origin/main into its branch, so the patch is cut against the latest live files; whoever lands second rebases the patch.
