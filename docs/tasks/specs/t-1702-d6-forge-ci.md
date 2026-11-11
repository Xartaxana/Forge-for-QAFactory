# t-1702 — P1 forge nodes F6-28, F6-30, F6-33, F6-44, F6-50: gates in `piles.py`, the batch canon in CI, role carriers (designer draft)

**Решения Lead (03.11.2026).** FK-1…FK-7, FK-9…FK-11 — по рекомендации (A); FK-8 — по рекомендации, до слова владельца (канон релиза —
пайплайн CI, локальный докер — запасной путь); вопрос владельцу задан 03.11. D6-D1 и D6-D2 — по слотам; D6-D3 — после критика на план.

**FK-8 решён ВЛАДЕЛЬЦЕМ, слово 03.11.2026: «Канон всегда на CI».** Канон пачки и релиза — пайплайн CI; слово 27.10 «докер-канон один
раз и последним» заменено этим словом; локальный докер — только запасной путь, когда CI красный (по причине раннера) или недоступен.

**Resubmission 1 (03.11, D3 only, after critic on plan t-1708 NEEDS WORK).** Changed: §1 axis lines (F8; axis 18 and axis 1 lines,
B1); §2.3 Δ4 (full new 7b: F4, F5, B2), Δ5 (full new PROJECT.md p. 2: B2, B3, F6), Δ10 (F-10 / F-12: B1, F5), Δ17 (B2), NEW Δ18
(brief, B1), NEW Δ19 (verbatim anchors of E1a / E1c / E2: B3), NEW Δ20 (the Lead's D-lines, drafted: B1); §2.4 (one owner of the
CI job map, one wording of the docker fallback: B2, F6); §3 D3 (given, handoff items for the Lead); §4 E-D3-7 (F7); §5 D3 keys
T9-T18 and the one-line anchor list (F9); «Queued» section (F10-F12). D1 and D2 are unchanged.
**Resubmission 1, addendum (FK-8 = the owner's word 03.11).** Δ5 rewrites the 27.10 passage quoting the 03.11 word; §2.4, Δ9, Δ20 (c),
E-D3-5, FK-8, keys T16/T17 and the anchor list follow; the «по рекомендации … до слова владельца» markers are gone.

Pile/batch: `onboarding-forge/1` (`plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md`, rows 47-50, 56, 60). Graph:
`docs/tasks/p1-closeout-0-10-9.md` (P-4..). Base: `origin/main` 881361da. Spec language English; Russian carrier text is quoted and
written in Russian. Line numbers are as read on 03.11.2026 and are NOT anchors: every edit is anchored on the verbatim old text.

Executable on the recommendations: every fork of §6 names its recommended variant, and §2/§3 are written for it. A fork the Lead
decides the other way changes only the lines it names.

## §0 — facts by carrier (read for this draft; the triage of the dispatch re-checked)

F0-1. F6-28 partly done (finding `plans/piles/onboarding-forge/findings/20261020-forge-check-krasnyj-tri-pusha-karta-os-20-pachki-2-session-context.md`
«Что сделано»): axis-20 heading, `## Бриф` in codex/collect batch 2, 14 «Содержание» rows, `session_context._import_size` UNC fix. Left: the
«Бриф» / «Содержание» conditions live only in `tools/test_pile_cards_contents.py:30-35, 72-106` (`CARD_HEADINGS`, `BATCH_HEADINGS`,
`LEGACY`, `coverage_problems`); `tools/piles.py` `check_form` (:1948) judges card parse errors, unreadable findings and `_view_reds`
(:1925: one file per batch, card row, status order, empty node table, `_node_reds`, `_coverage_reds`) — no «Содержание» coverage of
finding files, no batch heading. The second half of the class («platform-dependent `tools/` tests are proved on the CI image before
merge») is closed by F6-50 item 1: `forge-check` already runs on source `api` (`.gitlab-ci.yml:47-48`), so the branch pipeline IS the
Linux proof — only a text line is owed (§2.3 Δ4).
F0-2. F6-30 not done. `check_leftovers` (:2736) and `check_proofs` (:2838) are called only from `_close_batch` (:2923-2924).
`LEFTOVER_KEY_RE` (:1992) = `перенос|сделано` (no `узел`). The reader of the forms is ONE: `leftover_items` (:2619), `leftover_pairs`
(:2642), `leftover_problem` (:2655) with `DoneCarryRule` (:2587); `LEFTOVER_EMPTY_WORDS` (:2579). The board's count line is
`_count_line` (:1029); the compact snapshot's piles line is `tools/compact_snapshot.py` `findings_summary` (:320, cap 240 chars, :317).
`CHECKS` (:2141): (д) form has scope "files". `tools/piles.py` and `tools/compact_snapshot.py` are mechanism paths
(`tools/mechanism_gate.py:252, 254`). The batch template's «Остатки» comment: `plans/piles/_template/batch.md:68-80`.
F0-3. F6-33 not done. Spec `docs/tasks/specs/t-1206-f6-33-role-carriers-one-owner.md` (1007 lines) was accepted as a draft and PARKED
(journal `logs/journal/dev1.jsonl:1475`: «12 forks F-1..F-12 + host adaptation 10 decided at take time … critic-on-plan when
taken»). Since 21.10 its carriers moved: (a) `docs/SIBLING_MAP.md` now has axes 1-30 (axis 22 is «a host's return form», :414) — the new
axis is **31**; (b) `plans/builder-rules.md` gained 7c (:33-37, Lead 26.10: «Докер и храповики остаются уровнем пачки»), which
contradicts t-1206 L3/E14a («two ratchets stay with the builder»); (c) PROJECT.md p. 2 (:178-210) gained the «Тесты идут в CI» and
«Докер-канон — один раз и последним» paragraphs; (d) `docs/RUNBOOK.md` lines moved (407, 442, 617). Critic t-1708 re-ran
`git diff --stat cb88ae79 origin/main` over `.claude/agents/`, the brief, FULL, SYSTEM_PROMPT, TWO_VOCABULARIES,
`test_handoff_rule_anchors.py`, `install_parity_anchors.json`, CLAUDE.md: empty — E3-E9, E15, E17, E18 anchor as t-1206 wrote them.
The four D-0056 contradictions, item by item (`Grep` on 03.11, positive control in the same call shape noted):
  1. RUNBOOK «зелёные соседи» — STILL OPEN: `docs/RUNBOOK.md:407` and `:617` (the same grep found `CLAUDE.md:198`, the control).
  2. CURRENT_CONTEXT «builder-rules rows owed» — CLOSED: no hit in `CURRENT_CONTEXT.md`; control: `builder-rules` has 2 hits there;
     `CURRENT_CONTEXT.md:157-158` records it placed into builder-rules 7c → 52a4aab1.
  3. `docs/tasks/pre-release-0.9-brief-common.md` superseded header — STILL OPEN (line 1 is the old title, read).
  4. WEEKLY_CALIBRATION 13(j) third signature — STILL OPEN: only «SECOND SIGNATURE» at `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:362`.
  Plus the node row's fifth item, CLAUDE.md rule 4 «cover the test sets of every path» — STILL OPEN (`CLAUDE.md:198`).
  `docs/TWO_VOCABULARIES.md:11` still says «Haiku subagent | Haiku alias» (read).
  Plus a sixth, found by t-1708 B1: `docs/tasks/critic-diff-brief.md:14-15` puts «`python tools/dup_ratchet.py --check` from the
  worktree root (B-417, D-0033)» into the BUILDER's attached layer and `:21` lets the critic re-run «ratchets beyond `dup_ratchet`»
  — against 7b/7c (ratchets are batch level); D-0033 (`DECISIONS.md:46`) says «every builder's witness carries `--check`».
F0-4. F6-44 not done. `package-fast` (`.gitlab-ci.yml:161-187`) runs `--contracts`, `test_audit_rules.py`, `--fast --jobs 4`; no audit.
`audit_factory.py` already has `--agents` = A19 alone (`ai-packages/qa-factory/scripts/audit_factory.py:2360-2370`); the full audit
runs against ONE project's state (`project_root()`, docstring :104; `install_smoke.py:477` runs it after installing into a project),
so the full audit cannot run on the bare package — only project-free checks can. A2/A2b/A2c (:387-442) read no `project_root()` in
their bodies (the first project read is :443), but have no flag of their own.
F0-5. F6-50 partly. Rules today: `forge-check` MR/main/api (no web); `package-fast` MR/main with `changes:` (no api/web);
`package-full` schedule/web/api, one job, selftest then install_smoke sequentially, then the `slow_tests.json` drift step (:214-226);
`board-check` schedule/web/api; `crap-measure` schedule only (owner 28.10). Stages `[check, nightly]`: a `nightly` job waits for the
whole `check` stage (no `needs:` anywhere). `selftest.py` has no `--shard` (argparse :843-869); `cmd_tests` lists
`TESTS_DIR.glob("test_*.py")` (:487), runs each file as its own subprocess; `slow_tests.json` holds per-file seconds of the slow files
(`measured_on 2026-11-03`). `cmd_slow_tests --from` parses a saved output (`parse_durations` :613; a listed file nobody measured is
«unchanged», :631 — so a MISSING shard output would pass silently: edge E-D2-6). Last measured canon: pipelines 7988615 + 7988613
green in 18 min (`CURRENT_CONTEXT.md:88`); `package-full` alone 23 min (finding, job 27980169). No `tools/batch_canon.py` exists
(Glob). `tools/ci_read.py` has `start`, `pipelines`, `jobs`, `log`, `artifact`; it prints no durations.
Pins that read the CI file besides `tools/test_ci_layout.py`: `tools/test_dup_ratchet.py:764-775` (k23: the dup report line inside
the `package-full` selftest block, before `cd`), `tools/test_crap_report.py:778-810` (crap-measure stage/timeout/variables equal to
`package-full`'s), `tools/test_piles_gitlab.py:996-1003` (board-check rules == package-full rules), `tools/test_ci_read.py:203`
(a fixture string only).
F0-6. RUNBOOK §7 (`docs/RUNBOOK.md:317-331`) is stale: «В `.gitlab-ci.yml` одна задача, `forge-check`». No BATCH CANON recipe lives in
RUNBOOK; the canon text lives in PROJECT.md p. 2 and builder-rules 7b («докер python:3.12 (tar-копия)», :25). The CI job map is stated
today in PROJECT.md p. 2 (:186-189 «`forge-check` — … на каждый пуш и MR», which contradicts :201-202 «голый пуш ветки ничего не
запускает»), in the `.gitlab-ci.yml` header (:1-12) and, after D2 and D3, would also be in RUNBOOK §7 and 7b — four carriers (t-1708 B2).
The docker fallback is worded three ways (PROJECT.md :191-192 «CI красный или недоступен», the first draft's Δ5 and §2.4).
F0-7. DECISIONS.md D-0056 (:74) (3) still names «docker python:3.12 on a tar copy» and «no ratchets»; the owner's words of 28.10 («всё
что возможно идти в CI») and 03.11 («Канон всегда на CI») have no D-entry. D-0033 (:46) needs a refining Lead line (Δ20). Calibration
checks end at 38 (`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:1064`): the new ones are 39 and 40.
F0-8. Today's `plans/builder-rules.md`: p. 7 = line 14 (one line); 7b = :15-32 (:27-32 the SLOW_TESTS tail); 7c = :33-37; 7a = :38-48
(from «7a. **Цена проверки**» to «лучше запускать его синхронно.»; :44-47 carry «Из файлов `test_story_run_*.py` … все — только если
трогал `story_run_common.py`»). PROJECT.md p. 2 = :178-210: :178-199 from «2. **Свидетель билдера**» to «(builder-rules п. 11).»,
:200-204 «**Тесты идут в CI…**», :205-207 «**Докер-канон — один раз и последним**…», :208-210 the SLOW_TESTS sentence.

## §1 — mechanisms: the four questions, AR-n, and the axis block

Five mechanisms ride this spec: **M1** (F6-28) the «Содержание»/«Бриф» conditions move into `piles.py check` (д); **M2** (F6-30) an
«Остатки» item carries an executor from the moment it is written; **M3** (F6-33) one owner per aspect of a role, axis 31; **M4**
(F6-44) A19 over the real package on every package MR; **M5** (F6-50) the BATCH CANON is a CI pipeline on the branch, under an hour
(the owner's words 28.10 and 03.11.2026).

| | (a) cost, who pays | (c) detector of its failure (registered) | (d) what stops it being skipped |
|---|---|---|---|
| M1 | the writer of a finding stages the card's «Содержание» row in the same commit (already owed by D-0044 and CI pytest; now seen at commit time) — seconds | the gate itself; `tools/test_pile_cards_contents.py` on the real tree in CI `forge-check`; calibration check 33 | `.githooks/commit-msg` → `piles.py check --msg-file` (д); CI `piles.py check --all --base` |
| M2 | the integrator / Lead: one decision per leftover line WHEN it is written (open a node row, or a carry with a reason) instead of at `close`; ~150 lines in `piles.py` | the board count «остатков без исполнителя: N» + the compact-snapshot line; NEW calibration check 39 | commit-msg (д) on every staged batch file; CI `check --all --base`; door `piles-skip: д -- <reason>` |
| M3 | t-1206 §2 (~19 files of text) + Δ18-Δ20; every later change to a role walks the axis-31 rows; the builder no longer attaches ratchet runs (FK-9) — the critic reads them from `forge-check` | `tools/tests/test_role_carriers_one_owner.py`, `tools/test_handoff_rule_anchors.py`, `tools/install_parity.py --check`, calibration 28 (a)/(d) and 13(j) (third signature); for the ratchets: the `forge-check` job and critic question 9 | `pytest tools/` in CI `forge-check` on every MR; `install_parity --check` in `forge-check` |
| M4 | seconds of CI per package MR (measured in the DoD, §5 D2-M) | the `package-fast` job itself (red); the nightly `install-smoke` audit stays the second layer | `package-fast` rule on every MR touching `ai-packages/**` |
| M5 | runner minutes: 2 selftest shards + `install-smoke` + the clock per canon; the integrator waits ≤ 60 min instead of hours | the `canon-clock` job (red over 60 min); NEW calibration check 40 | the canon starts by code (`tools/ci_read.py start`), `canon-clock` runs in EVERY `api`/`web` pipeline (`when: always`) |

AR-n (designer rule 1; only D2 writes in `ai-packages/qa-factory/`, the file `scripts/selftest.py` and a new test):
- **AR-1** (closed variety is a data row): the shard weights come from `scripts/slow_tests.json` through the existing loader
  `slow_tests()`, never a list of file names in code. Change check (DoD): `git grep -n "test_story_step" -- ai-packages/qa-factory/scripts/selftest.py`
  shows no new hit.
- **AR-23** (every required list declares its empty outcome): a shard with no test file prints `tests: shard I/N: 0 test files
  (explicit note)` and passes. Change check: test S3 pins it.
- **AR-28** (an unknown never becomes a pass): an incomplete set of shard outputs given to `--slow-tests --from` is exit 2, never
  «unchanged». Change check: the spec states missing / duplicate / mixed-N behaviour (E-D2-6) and test S7 pins each.
- AR-12 (friction): not measured — no role calls `selftest.py` (it is the integrator's and CI's tool). AR-18, AR-20: not touched (no
  detector output shape changes; no ratchet row is raised).
Commit line for D2's package part: `architecture: AR-1, AR-23, AR-28 -- shard weights read from slow_tests.json; an empty shard prints
its note; an incomplete shard set is exit 2, never a pass`. D1 and D3 touch no package file: `architecture: none -- tools/ and docs only`.

FR walk for D2's package part (PROJECT.md «Как принимается изменение пакета» p. 1): A — FR-1 (a bad `--shard` value says the expected
form `I/N, 1 <= I <= N`); B — no person text; C — FR-14 (the PASS/FAIL line shape unchanged; one header line added, documented in the
docstring); D — FR-59 (incomplete shards → exit 2); E — n/a; F — FR-28 (the measurer gets a test), FR-41; G — FR-30 (English, no
Cyrillic), FR-31 (no wall clock in tests: the partition is pure), FR-32.

Axis block — one block, every line closes each mechanism by name, in the LABELLED form `tools/mechanism_gate.py` accepts (`axis N
(<label>): …`, the label containing the axis's gate key = the heading text after «Axis N — » up to its first colon; the Lead runs the
gate on the commit message). The map has 30 axes today and 31 after D3: the commit that adds axis 31 carries all 31 lines.
- axis 1 (Policy <-> role files <-> journal): M3 covered (role files, CLAUDE.md rule 4 + host adaptation 10, the brief's two layers —
  Δ18; D-0033 refined by the Lead's D-line, Δ20); M2 covered (critic brief question 4 gains the leftover form); M1, M4, M5 n/a (no
  role text, no journal event).
- axis 2 (Per-tier exam instruments): M3 queued — critic.md is edited without `PROCESS/CRITIC_EXAM.md` (absent): FK-10 / t-1206 F-6,
  the Lead's D-line (Δ20); M1, M2, M4, M5 n/a.
- axis 3 (Factory package <-> its release copy <-> the installed plugin): M5 covered (`--shard` ships in the package; `--hygiene`
  unchanged); M1-M4 n/a.
- axis 4 (Factory rules <-> their debt <-> the backlog <-> the principles): n/a for all five (no FR changes; no BACKLOG row — frozen).
- axis 5 (Stage twins inside the package): n/a for all five (no stage code).
- axis 6 (Measurement tools <-> the package they measure): M5 covered (the drift measurement reads the joined shard outputs; the
  shard header makes the join checkable); M1-M4 n/a.
- axis 7 (Per-test identity <-> every scope a test's behaviour depends on): M5 covered — a test file's verdict does not depend on its
  shard (each file is its own subprocess in its own checkout; the partition never splits a file); M1-M4 n/a.
- axis 8 (Where the story is on disk): n/a for all five.
- axis 9 ("is this a test file"): M5 covered — the shard partitions the same `TESTS_DIR.glob("test_*.py")` list, no second
  recognizer; M1-M4 n/a.
- axis 10 ("git-top readers"): n/a for all five — M2 reads a base text through the git helper (в) already uses, not the repository top.
- axis 11 ("shell-command recognizers"): n/a for all five.
- axis 12 (carriers of the work plan): M1, M2 covered (the gate, the board count line, the compact snapshot through piles' reader;
  D3 adds the axis-12 sentence of Δ15); M3-M5 n/a.
- axis 13 (the dispatch text): n/a for all five.
- axis 14 (readers of agent transcripts): n/a for all five.
- axis 15 (console stream setup): n/a for all five — `tools/canon_clock.py` prints ASCII only.
- axis 16 (one JSON reader of the package): M5 covered — weights through `slow_tests()`, no new `json.loads` in the package; M1-M4 n/a.
- axis 17 (detector verdict shape): n/a for all five (tools gates, not package detectors).
- axis 18 (in-tree shrink-only ratchets): M3 covered — FK-9 moves WHO runs `dup_ratchet --check` / `lint_ratchet --check` (the
  `forge-check` job, not the builder's witness; the brief Δ18, D-0033 refined Δ20); no baseline row raised; M1, M2, M4, M5 n/a.
- axis 19 (one reader of a role file's `tools): n/a for all five (not touched).
- axis 20 (host receipt names): n/a for all five (not touched).
- axis 21 (readers of the package's markdown tables): n/a for all five (not touched).
- axis 22 (a host's return form): n/a for all five (not touched).
- axis 23 (fields of a `tests[]` row): n/a for all five (not touched).
- axis 24 (the record of an execution): n/a for all five (not touched).
- axis 25 (freshness of a run and of a live check): n/a for all five (not touched).
- axis 26 (the word `stand not confirmed`): n/a for all five (not touched).
- axis 27 (the profile of a test row): n/a for all five (not touched).
- axis 28 (the render site of the row form): n/a for all five (not touched).
- axis 29 (append-only jsonl writers): n/a for all five (not touched).
- axis 30 (the commands of a profile): n/a for all five (not touched).
- axis 31 (Role carriers, NEW by M3): M3 covered (creates it); M2 covered (critic brief q. 4 is the brief's own text, owner = the
  brief); M5 covered (the CI job map owner = the `.gitlab-ci.yml` header; the canon procedure and the docker fallback owner = RUNBOOK
  §7; the canon content owner = builder-rules 7b; PROJECT.md p. 2 = pointers); M1, M4 n/a.

Tier line for the mechanism commits: `tier: fable` (the Lead commits the staged mechanism paths, §3).

## §2 — per node: what, where, behaviour, test

### §2.1 — D1: `tools/piles.py` gates (F6-28 remainder + F6-30)

**F6-28 (M1).** In `check_form`'s per-pile loop add `_contents_reds(tree, pile)` (+new) and, per batch file, `_heading_reds(b)` (+new):
1. For a pile whose card has `## Содержание` (`card.contents` True): every finding file name of the pile occurs EXACTLY once in the
   «Содержание» section, counted as a whole token by the existing `_name_re`; every member id of every card row occurs exactly once
   (by `WHAT_ID_RE`). Red text: `<card>: «Содержание» names findings/<file> <k> times, want exactly 1 -- add its row (path, type,
   суть, файлы, узел, решение владельца, связи) or remove the duplicate`; carriers `(card_rel, finding path)` (for an id: `(card_rel,)`).
2. A batch file whose status is «ожидает» (or empty) lacks a `## Бриф` or a `## Узлы` line → red `<batch>: an untaken batch has no
   «## Бриф» heading -- write it from plans/piles/_template/batch.md`; carrier `(batch path,)`. A taken batch (в работе / сдано /
   принято / закрыта) is not judged (its text is frozen by (в)).
3. `tools/test_pile_cards_contents.py`: `coverage_problems` is deleted and the test calls the gate's pure function
   `contents_problems(contents_text, row_ids, finding_names)` (+new, public; the reds of item 1 are built from it) — one reader; the
   batch-heading assertion calls `batch_heading_problems(text)` (+new). `CARD_HEADINGS`, `LEGACY`, the node-id test stay in pytest.

**F6-30 (M2).** New `_leftover_write_reds(ctx)` (+new), called from `check_form`:
4. Items judged: the «Остатки» items (`leftover_items`, unchanged) of every batch file that is not «закрыта», that are NEW or CHANGED
   against the base text of the same file — staged mode: `HEAD:<path>`; `--base REV`: `REV:<path>`; `--all` without `--base`: `HEAD`.
   An item is «old» when its stripped text equals the stripped text of an item of the base file. The base text is read through the
   same git helper (в) uses for its base (no new git call shape). A file absent at the base → all its items are new.
5. A judged item passes when its pairs (`leftover_pairs`, unchanged) carry ONE of:
   - `сделано: <7-40 hex | t-nnn>` — `LEFTOVER_DONE_RE.fullmatch`;
   - `узел: <id>` (+new key) — `<id>` resolves to a node row (`BatchFile.nodes`) of a batch file of the SAME pile, or
     `<slug>/<N>/<id>` to a node of batch N of pile `<slug>`, whose batch is not «закрыта» and whose «Исполнитель» is not in `NO_VAL`;
   - `перенос: <target> | обоснование: <why> | подтвердил: <кто, дата | —>` — target by `LEFTOVER_TARGET_RE`, `обоснование` non-empty
     and not in `LEFTOVER_EMPTY_WORDS`; `подтвердил:` present, and MAY be a placeholder (a person confirms later; close still demands
     a real one).
   Otherwise red: `<batch>: «Остатки» line <n> "<item, 80 chars>": <why> -- an item is written with its executor: сделано: <hash |
   t-nnn>, узел: <node id> (a node row of an untaken batch, D-0044), or перенос: <target> | обоснование: <why> | подтвердил: <кто,
   дата | —>`; carrier `(batch path,)`. Door: the existing `piles-skip: д -- <reason>`.
6. `LEFTOVER_KEY_RE` gains `узел`: `(?:перенос|сделано|узел):` (a `узел:` line under «Остатки» places a finding for (е), the same
   key-position rule).
7. `leftovers_unowned(tree) -> list[(path, line_no, item)]` (+new, public): items of not-closed batches that carry none of the three
   forms of item 5 (no base diff — every item counts). `_count_line` appends `; остатков без исполнителя: N` (N may be 0; it is
   always printed). `compact_snapshot.findings_summary` appends to its never-cut tail `, N leftovers without an executor`.
8. `check_leftovers` / `check_proofs` / `_close_batch`: unchanged (FK-1 A). Its refusal text gains one sentence for an item that
   carries only `узел:`: `a «узел:» item is closed by «сделано: <hash | t-nnn>» when the node merges, or carried`.
9. `plans/piles/_template/batch.md` «Остатки» comment: a third form line `  - <что осталось> | узел: <id узла в невзятой пачке>`
   and one sentence «строка пишется сразу с исполнителем — `piles.py check` (д)».
10. `plans/PILES.md` regenerated (`python tools/piles.py board`).

### §2.2 — D2: CI (F6-44 + F6-50) and `selftest.py --shard`

11. `.gitlab-ci.yml`:
   - `stages: [check, nightly, report, clock]`.
   - `forge-check` rules gain `- if: $CI_PIPELINE_SOURCE == "web"`.
   - `package-fast` rules gain `- if: $CI_PIPELINE_SOURCE == "api"` and `- if: $CI_PIPELINE_SOURCE == "web"` (no `changes:` on them:
     a canon always runs it). Script: after the `--fast` line a last step
     ```
     - |
       t0=$(date +%s)
       python -B scripts/audit_factory.py --agents
       echo "audit_factory --agents wall time: $(( $(date +%s) - t0 )) s"
     ```
     (A19 over the real `agents/`; FK-4 A).
   - `package-full`: `parallel: 2`, `needs: []`; its script block keeps `mkdir -p "$CI_PROJECT_DIR/ci-out"`, then the dup report line
     guarded to the first shard — `if [ "$CI_NODE_INDEX" = "1" ]; then python tools/dup_ratchet.py --report "$CI_PROJECT_DIR/ci-out" ||
     echo "dup report: exit $? (a report, not the release verdict)"; fi` — then `cd ai-packages/qa-factory`, then
     `python -B scripts/selftest.py --jobs 4 --shard "$CI_NODE_INDEX/$CI_NODE_TOTAL" > "$CI_PROJECT_DIR/ci-out/selftest-shard-$CI_NODE_INDEX-of-$CI_NODE_TOTAL.txt" 2>&1 || rc=1`,
     the tail of that file, `exit $rc`. No install_smoke and no drift step in it any more. Rules, image, timeout (3h), stage
     (`nightly`), variables, artifacts unchanged.
   - NEW `install-smoke`: extends `.factory-job`, stage `nightly`, `needs: []`, image python:3.12, timeout 3h, the rules of
     `package-full`, before_script as `package-full`'s (pytest + `.git-identity`), script: mkdir ci-out, `cd ai-packages/qa-factory`,
     `python -B scripts/install_smoke.py > "$CI_PROJECT_DIR/ci-out/install_smoke.txt" 2>&1 || rc=1`, tail 25, `exit $rc`; artifacts
     `ci-out/` 2 weeks.
   - NEW `package-full-report`: stage `report`, `needs: [package-full]` (the artifacts of both shards), the rules of `package-full`,
     timeout 10m, no pip; script: `cat ci-out/selftest-shard-*.txt > ci-out/selftest.txt` then
     `cd ai-packages/qa-factory` and `python -B scripts/selftest.py --slow-tests --from "$CI_PROJECT_DIR/ci-out/selftest.txt"`;
     artifacts `ci-out/selftest.txt` 2 weeks (the fix command in the job comment stays valid).
   - `board-check`: `needs: []` (it waits for no one).
   - NEW `canon-clock`: stage `clock`, rules `api` and `web` ONLY, `when: always` on each rule, timeout 5m, no pip, script
     `python tools/canon_clock.py`. No `needs` (the last stage waits for every earlier job).
   - Header comment (lines 1-12) is the ONE owner of the CI job map (which job runs what, on which pipeline source; §2.3, t-1708 B2):
     it names every job, its sources and «the batch canon and the release canon = an api/web pipeline on the branch (the owner's
     words 28.10.2026 and 03.11.2026 «Канон всегда на CI»)»; `crap-measure` untouched (schedule only, not in the canon).
12. NEW `tools/canon_clock.py`: reads `CI_PIPELINE_CREATED_AT` and `CI_COMMIT_MESSAGE` from the environment (`--created-at`, `--message`,
   `--now` override them, for tests); `LIMIT_S = 3600`. Elapsed = now − created (wall time, runner queueing included — the norm is
   wall time). Prints ONE line `canon wall time: <M> min <S> s (limit 60 min) -- <verdict>`; exit 0 at elapsed ≤ 3600; elapsed > 3600:
   exit 1 with `-- over the hour: the owner's norm (28.10.2026) is a batch canon within 60 minutes; find the longest job in
   ci_read.py jobs <pipeline>; door: a line "canon-over-hour: <reason>" in the head commit message`, unless the message holds a door
   line `^canon-over-hour:[ \t]*(\S.*)$` whose reason is not in `("—", "-", "n/a", "none", "tbd", "?")` → exit 0, `-- over the hour,
   passed by "canon-over-hour: <reason>"`. Start unknown (variable absent, unparseable, or elapsed < 0) → exit 2 `canon wall time:
   unknown -- <why>; the same door passes it` (exit 0 with the door). Parses `Z`, `+00:00` and fractional seconds.
13. `ai-packages/qa-factory/scripts/selftest.py` `--shard I/N`:
   - argparse type: `I/N` integers, `1 <= I <= N`; anything else → `ap.error("--shard expects I/N with 1 <= I <= N, e.g. 1/2; got <v>")`
     (exit 2). Combined with `--fast` or `--slow-tests` → `ap.error` («--shard splits a full run's test files; --fast is one tier,
     --slow-tests measures a whole run: concatenate the shard outputs and pass --from»). With flags that do not include `--tests`
     (and are not the flagless run) → `ap.error("--shard splits the test files: use it with --tests or with no check flag")`.
   - Partition (pure function `shard_files(files, weights, n) -> list[list[Path]]`, +new): longest-processing-time greedy — files
     sorted by (−weight, name); weight = seconds from `slow_tests()["files"]` when listed, else `slow_tests()["thresholds"]["fast_under_s"] / 2`;
     each file goes to the shard with the least total weight, ties to the lowest index. Shard I runs `parts[I-1]`. The partition depends
     only on the file list and the data file (identical in every shard of one pipeline).
   - `cmd_tests(..., shard=None)` prints first `selftest shard I/N: K of M test files` (the header; also printed for K = 0 with
     `tests: shard I/N: 0 test files (explicit note)` and a PASS).
   - Flagless run with `--shard I/N`: shard 1 runs every check of the flagless run; shard I > 1 runs only its tests and `--hygiene`.
     Summary line `=== qa-factory selftest (shard I/N): a/b ok ===`.
   - `cmd_slow_tests(from_file)`: when the saved text holds header lines `^selftest shard (\d+)/(\d+): `, all must name the same N and
     the set of I must be exactly {1..N}, each once — else exit 2, stderr `slow tests: the saved output holds shards <list> of <N>;
     missing <list> / repeated <list> / mixed totals -- concatenate every shard's output once`. No header → today's behaviour.
   - Docstring (:44-49 block) gets the `--shard` paragraph; FR-30 (English).
14. NEW `ai-packages/qa-factory/scripts/tests/test_selftest_shard.py` (harness style of `test_selftest_slow_tests.py`, temp package for
   the command line; no clock).
15. `ai-packages/qa-factory/changelog.d/onboarding-forge-1-f6-50.md`: one English line for `--shard`.
16. `tools/test_ci_layout.py`: `STAGES`, `GOLDEN` (forge-check, package-fast, package-full, board-check; new install-smoke,
   package-full-report, canon-clock), `IDENTITY_USERS` (+ `install-smoke`) — the deliberate edit the module's docstring names.

### §2.3 — D3: role carriers (F6-33 = t-1206 rebased) and the text of F6-28 / F6-30 / F6-50

D3 executes t-1206 §2 (E1-E20), §3 (axis text), §4 (the detector test) and its §5 keys, **anchored on each item's verbatim OLD text**
(Δ19 gives the anchors that moved), with the deltas below. An E-item whose old text is not found verbatim and is not covered by a
delta is NOT DONE and named in the handoff — never re-written from memory (edge E-D3-1).

**One owner per aspect of the CI text (t-1708 B2).** (i) Which CI job runs what and on which pipeline source: the header comment of
`.gitlab-ci.yml` (written by D2 in the same commit as the jobs; `tools/test_ci_layout.py` holds the jobs' golden beside it). (ii) How to
run a branch pipeline, the BATCH CANON procedure, what stays local and the ONE wording of the docker fallback: `docs/RUNBOOK.md` §7.
(iii) What the canon covers (content): `plans/builder-rules.md` 7b. PROJECT.md p. 2 holds the owner's words and pointers, no job list.
The docker fallback wording, used nowhere else: «только когда CI недоступен или красный по причине раннера, а не кода».

- Δ1. The axis is **31**, not 22: heading `## Axis 31 — Role carriers: one owner per aspect <-> pointers (onboarding-forge/1 F6-33,
  t-1206/t-1702, 03.11)`; every «axis 22» of t-1206 that D3 writes into a carrier (E8a, E16b, the §3 axis text and closing rule, the
  §4 test docstring) reads «axis 31»; key K15's count is `docs/SIBLING_MAP.md:31`. Insert it after axis 30 (before «## Keeping the
  map up to date», :460).
- Δ2. Ratchets (FK-9 A): t-1206 L3/E1b «**Два храповика в дереве** … входят в свидетель» is NOT written; E14a is dropped (D-0056
  «no ratchets» stays as is); t-1206 key K12's third grep is dropped. The ratchets are canon content (Δ4); the brief follows (Δ18);
  D-0033 is refined by the Lead (Δ20).
- Δ3. E1a (p. 7): the anchor is the WHOLE current line 14 of `plans/builder-rules.md` (Δ19); it is replaced by t-1206 E1a's new text
  verbatim (it keeps «size pin is a cap»; the ratchet and console-scan sentences of today's p. 7 move per Δ4).
- Δ4. E1b (7b): the anchor is today's 7b from «7b. **Уровень билдера и уровень пачки**» to «…читает ночной `package-full` в начале
  каждого дня.» (:15-32, Δ19). It is replaced by this text, verbatim (F-1 A and F-2 A written in; the console scan kept by type, t-1708
  F5; «докер, храповики — билдер НЕ гоняет» kept, t-1708 F4; no job list, t-1708 B2):
  ```
  7b. **Уровень билдера и уровень пачки** (слово владельца 21.10.2026 18:3x, D-0056; замер: у фикс-раундов 69–85 % стены —
     ожидание прогонов, правки кода 1–4 %). П. 7 и 7a переписаны под этот пункт (F6-33, 21.10.2026). У билдера — только
     **точечные проверки своей правки**: тестовый файл изменённого модуля (при разделённых файлах — тот, что судит
     изменённую команду/стадию; для `story_run.py` это один `test_story_run_<область>.py`, судящий тронутую область, если DoD
     его называет, и файлы п. 7c; тронут `story_run_common.py` — все `test_story_run_*.py` идут в каноне, в отчёте строка
     «тронут story_run_common.py»), тестовый файл каждого другого пути своего `owns` (правило 4 `CLAUDE.md`) и ключи своего
     DoD; `--limits --lang` и `test_audit_rules.py` — только если правка их касается (лимит размера, правило аудита); так же по
     типу правки: `test_hooks_wiring.py` — хуки; `test_null_outcomes.py` — обязательный список, выход стадии или поле
     инструмента (реестр `references/null-outcomes.json`, t-305 N0); `test_gate_registry.py` — гейт, его ключ или слово-исход
     (реестр `references/gate-registry.json`, t-302 T1); `python -B scripts/tests/test_console_encoding.py` — добавлен или
     изменён скрипт, печатающий в консоль (B-413). **Не регрессия, не соседи, не большие файлы**: импортёры, файлы дольше
     ~5 минут или больше ~500 проверок (`test_story_step.py`, все `test_story_run_*.py` разом, полный `selftest.py`), докер,
     храповики — билдер НЕ гоняет (прежний п. 7 «`lint_ratchet --check` + the console scan» разделён: храповики — уровень
     пачки, сканирование консоли — по типу правки, выше); «сверх списка» — строка отчёта, не прогон. **Мутации** билдер не
     прогоняет: он называет в отчёте для каждой мутации одну строку/ключ теста, которая её убивает (самый узкий тест), и
     однострочную правку-мутант. **Всё это делается один раз на пачку**, не на каждое изменение: после схождения веток пачки
     (или на границе стадии, если пачка живёт дни) интегратор делает один прогон BATCH CANON — соседи, большие файлы,
     храповики и аудит идут в пайплайне CI на ветке пачки (как его запустить и прочитать — `docs/RUNBOOK.md` §7), и один
     мутационный проход по спискам мутаций всех узлов (каждая — своим узким файлом); красное на каноне — `defect_found`
     против узла (правило 4 CLAUDE.md). CI на каждом MR остаётся регрессией за бесплатно. Тест из `SLOW_TESTS` идёт только в
     полном уровне CI (быстрый его пропускает), поэтому зелёный свидетель с Windows его не доказывает: Linux отдаёт другой
     errno (`Path.unlink(missing_ok=True)` под путём, где папка — файл, на Linux `NotADirectoryError`, на Windows проглоченный
     `FileNotFoundError`; релиз 0.9.0 нашёл красный `test_probe_by_code_copy.py` лишь при пуше), CI идёт под root, хук,
     записанный тестом, требует `chmod 0o755`. Такой файл — и тест `tools/`, чей результат зависит от платформы (F6-28), —
     доказывает пайплайн ветки (канон в CI, образ python:3.12), не билдер; Lead в списке передачи называет затронутые
     `SLOW_TESTS`-файлы и читает ночной `package-full` в начале каждого дня.
  ```
  7c (:33-37) stays untouched between 7b and 7a (its «Докер и храповики остаются уровнем пачки (7b)» now holds in 7b).
- Δ5. E2 (PROJECT.md p. 2): the anchor is :178-210, from «2. **Свидетель билдера**» to «`package-full` в начале каждого дня.» (Δ19).
  It is replaced by this text, verbatim. FK-8 is the OWNER's word of 03.11.2026 («Канон всегда на CI»): it replaces the 27.10
  paragraph «Докер-канон — один раз и последним», which goes, and the new paragraph quotes the 03.11 word; no job list (B2):
  ```
  2. **Свидетель билдера** — вывод проверки, а не пересказ. Объём проверки билдера и канон пачки — D-0056 (слово владельца
     21.10.2026: все тесты и проверки — на уровне пачки), текст правила — `plans/builder-rules.md` п. 7b; что прикладывается
     критику и каким бывает его контрольный перепрогон — `docs/tasks/critic-diff-brief.md` («The two layers»). **Полный
     `selftest.py` и `install_smoke.py` на машине владельца больше не гоняются — их гоняет CI** (владелец, 03.10; какие задачи
     что гоняют и когда — шапка `.gitlab-ci.yml`). Интегратор перед коммитом гоняет только свидетелей узлов и `--limits --lang`;
     после пуша читает пайплайн, красный пайплайн на `main` — строка `B-nnn` и починка до следующего пуша. Локальный прогон —
     только запасной путь (когда и как — `docs/RUNBOOK.md` §7) и никогда не параллельно с другим. Задача на один инструмент в
     `tools/` не требует полного `pytest tools/`: свидетель — тест инструмента, полный прогон — при интеграции. Форма отчёта —
     правило 7 `.claude/agents/builder.md`, содержание — builder-rules п. 11.
     **Тесты идут в CI, не на машине разработчика** (слово владельца 06.10.2026: CI затеян, чтобы не занимать тестами эту
     машину). Голый пуш ветки ничего не запускает; прогнать ветку и прочитать результат — `docs/RUNBOOK.md` §7.
     **Канон всегда на CI** (слово владельца 03.11.2026: «Канон всегда на CI»; заменяет слово 27.10.2026 о докер-каноне релиза;
     слово 28.10.2026 — «Когда всё реализовано, конечные проверки пачки должны занимать не больше часа и всё что возможно идти
     в CI»): BATCH CANON пачки и канон релиза — пайплайн CI на ветке (образ python:3.12), процедура — `docs/RUNBOOK.md` §7;
     локальный докер — только запасной путь (там же).
     Тест из `SLOW_TESTS` — `plans/builder-rules.md` п. 7b.
  ```
  The 27.10 ordering of a release («узлы → кучки → `main` → публикация → канон», «не стоит гейтом ни на MR, ни на публикации») is
  NOT carried into the new paragraph: the owner's 03.11 word supersedes the 27.10 passage as a whole (the coordinator's addendum);
  whether the ORDER survives is fork FK-12.
- Δ6. E10 (RUNBOOK): anchors are at :407, :442, :617 today; same texts. PLUS the §7 rewrite: lines 317-331 («## 7. CI на GitLab
  (forge-check)» through «Пуш в git.example.com только под VPN (раздел 4).») are replaced by the text of §2.4 below.
- Δ7. E11 (CURRENT_CONTEXT): dropped — contradiction 2 is closed (F0-3); CURRENT_CONTEXT.md is the Lead's file (state of `main`).
  t-1206 key K8 is dropped.
- Δ8. E13 (13(j)): unchanged text; it lands at :362 today.
- Δ9. E14b (D-0056 axes line): kept (see Queued F10). D-0056 (3)'s «docker python:3.12 on a tar copy» is NOT edited by D3 — the
  owner's word of 03.11 gets its own D-entry from the Lead (Δ20 (c)).
- Δ10. t-1206 forks F-1..F-12: written by their recommended variants — F-1 A, F-2 A (both inside Δ4's text), F-3 A, F-4 A, F-5 A,
  F-6 A (needs the Lead's D-line, Δ20 (b)), F-7 A, F-8 A, F-9 A, F-10 read as «the brief's two layers follow FK-9» (Δ18 — NOT
  «brief:14 word for word»), F-11 A as a follow-up row only (no model-family check in this node), F-12: the console scan stays a
  builder duty BY TYPE of change (Δ4's by-type list) and the pinned phrase «`lint_ratchet --check` + the console scan» stays in 7b
  (pin `br-lint-console` of `tools/tests/test_integration_batch_0_9_forge.py:51` green).
- Δ11. Install parity: run `python tools/install_parity.py --check` BEFORE the first edit and after the last; any anchor turned
  MISSING other than t-1206 E18's two designer anchors is a stop-and-report, not an anchor rewrite.
- Δ12. `tools/test_handoff_rule_anchors.py`: anchor E17's edits by the function names (`test_brief_what_comes_back`,
  `test_builder_rules_p11`), not line numbers.
- Δ13. `docs/tasks/critic-diff-brief.md` question 4 (F6-30): after «a sibling neither fixed nor queued is a finding.» append:
  «An analog outside the node's `owns` that this round does not fix comes back as a line the Lead writes into «Остатки» as is:
  `<what> | узел: <node id>` (a node row the Lead opens in an untaken batch, D-0044) or `<what> | перенос: <findings/<file> | пачка N> |
  обоснование: <why> | подтвердил: —`; a bare queue line is refused by `piles.py check` (д) (F6-30).»
- Δ14. `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: after check 38 append checks 39 and 40, verbatim:
  «39. **«Остатки» items carry an executor (onboarding-forge/1 F6-30; the owner's word 21.10.2026, PROJECT.md «Командная работа» п.
  9).** Mechanism: `piles.py check` (д) refuses a NEW or CHANGED «Остатки» item without `сделано:` / `узел:` / `перенос:` (commit-msg;
  CI `check --all --base`); the board's count line and the compact snapshot print «остатков без исполнителя: N». Check: (a) N at the
  window's end, by pile — each item is either older than the gate's commit (the baseline) or a leak: count the `piles-skip: д` doors in
  the window's commit messages; (b) `перенос: … | подтвердил: —` items older than 48 hours (`git log -S "<item text>"`) — a carry
  waiting for a person goes into the morning report; (c) `узел:` items whose node is still «ожидает» after its batch closed. An empty
  window (no item, no door) is noted explicitly.»
  «40. **BATCH CANON within the hour, always in CI (onboarding-forge/1 F6-50; the owner's words 28.10.2026 and 03.11.2026 «Канон
  всегда на CI»).** Mechanism: the `canon-clock` job of every `api`/`web` pipeline (`tools/canon_clock.py`) is red over 60 minutes
  unless the head commit carries `canon-over-hour: <reason>`. Check: for every batch and release accepted in the window, its canon
  pipeline id in the last `accepted` witness and that pipeline's `canon-clock` line (`python tools/ci_read.py jobs <id>`,
  `log <job_id> --grep "canon wall time"`); a batch or release accepted with no canon pipeline, a canon without a green `canon-clock`,
  every `canon-over-hour:` door and every local docker canon (with why CI could not run) are listed. An empty window is noted
  explicitly.»
- Δ15. `docs/SIBLING_MAP.md` axis 12: append to its closing paragraph «The «Остатки» item forms have ONE reader, `piles.leftover_pairs`
  / `leftover_problem`: the write-time keys of check (д) (`сделано:` / `узел:` / `перенос:`, F6-30), the close gate
  (`check_leftovers`, `check_proofs`), the placement rows of (е) (`LEFTOVER_KEY_RE`), the board's count «остатков без исполнителя»
  and `compact_snapshot.findings_summary`; a new key changes all of them in one commit.»
- Δ16. PROJECT.md «Командная работа» п. 9: after «…подтверждает **человек**, не агент сам;» insert «строка «Остатков» с ЗАПИСИ несёт
  исполнителя — `сделано:`, `узел: <id узла>` или `перенос: … | обоснование: … | подтвердил: <кто, дата | —>`, голую строку отказывает
  `piles.py check` (д) (F6-30);».
- Δ17. axis-31 table (t-1206 §3): the `PROJECT.md` row's last cell becomes «owner of p. 1, 3-6 and of the owner's words in p. 2; p. 2
  otherwise holds pointers: scope → D-0056 + builder-rules 7b; CI job map → `.gitlab-ci.yml` header; branch run, canon procedure,
  docker fallback → RUNBOOK §7; critic re-run → the brief; report → builder.md 7 + builder-rules 11»; the `.gitlab-ci.yml` row →
  «owner of the CI job map (its header comment, written with the jobs; golden `tools/test_ci_layout.py`)»; the `docs/RUNBOOK.md` row
  → «procedure; owner of the branch-run recipe, the BATCH CANON procedure and the docker-fallback wording (§7); package fix →
  builder-rules 7b; parallel launch → CLAUDE.md host 6»; the `plans/builder-rules.md` row gains «canon content (7b)»; a new row
  `tools/canon_clock.py` | integrator | canon wall time | machine; the limit moves with the owner's norm (RUNBOOK §7).
- Δ18 (t-1708 B1). `docs/tasks/critic-diff-brief.md` «The two layers», two spots, verbatim:
  (a) :14-15, old «`python tools/dup_ratchet.py --check`\n  from the worktree root (B-417, D-0033);» → new «the ratchets
  (`dup_ratchet --check`, `lint_ratchet --check`) are NOT in the builder's layer: their result is the `forge-check` job of the
  branch or MR pipeline (batch level, `plans/builder-rules.md` 7b/7c; D-0033 as refined by the Lead), which the critic reads, never
  re-runs;» (keep the bullet's indentation and the rest of the bullet).
  (b) :21, old «ratchets beyond `dup_ratchet` and mutation runs are not» → new «ratchets and mutation runs are not».
  critic.md rule 18 → pointer (t-1206 E4c) is unchanged; after Δ18 the brief is the one owner of the two layers and agrees with 7b/7c.
- Δ19 (t-1708 B3). Verbatim anchors that replace t-1206's line ranges:
  E1a — the whole line 14 of `plans/builder-rules.md`, from «7. **Обязательная проверка перед отчётом**: свои тесты;» to «…(пин байт
  `SKILL.md` сломался на законной строке B-412, B-410).»;
  E1b — from «7b. **Уровень билдера и уровень пачки**» to «…читает ночной `package-full` в начале каждого дня.» (:15-32);
  E1c — from «7a. **Цена проверки**» to «лучше запускать его синхронно.» (:38-48), replaced by t-1206 E1c's new text; 7c (:33-37,
  from «7c. **`story_run.py` и слои драйвера**» to «Докер и храповики остаются уровнем пачки (7b).») is NOT inside any anchor and
  stays between 7b and 7a. The story_run rule of old 7a (:44-47) lives on in Δ4 (area file, `story_run_common.py` → canon).
  E2 — PROJECT.md from «2. **Свидетель билдера**» to «`package-full` в начале каждого дня.» (:178-210), replaced by Δ5.
- Δ20 (t-1708 B1; for the Lead — D3 writes NONE of these; its handoff lists them under «Needed from the Lead before the commit»).
  Drafts (English, the DECISIONS.md form; the ids are the next free ones):
  (a) «- D-NNNN — D-0033 refined: the clone and lint ratchets stay a merge gate in `forge-check` (every MR push, `main`, every
  `api`/`web` branch pipeline); a builder's witness no longer carries `--check` — the critic reads the ratchets from the `forge-check`
  job of the branch or MR pipeline (`docs/tasks/critic-diff-brief.md` «The two layers»; `plans/builder-rules.md` 7b/7c). D-0033's
  clause «every builder's witness carries `--check` and the critic reads it as the mechanical layer» is superseded (the Lead,
  03.11.2026, t-1702 FK-9; builder-rules 7c, the Lead 26.10.2026; D-0056's batch canon names «храповики»). Detector: the
  `forge-check` job and `tools/test_dup_ratchet.py` (unchanged); critic question 9. Axes: axis 1 (Policy <-> role files <-> journal)
  covered (brief, builder-rules); axis 18 (in-tree shrink-only ratchets) covered (who runs them; no baseline change); the other axes
  n/a. Tier: fable.»
  (b) «- D-NNNN+1 — critic.md is edited by F6-33 (t-1206 E4: pointers to CLAUDE.md hygiene 6 and to the brief; no duty added or
  removed) without the exam its rule 10 demands, because `PROCESS/CRITIC_EXAM.md` does not exist; the pass is recorded like D-0037
  (the Lead, <date>). Detector: calibration check 12 (exam currency). Tier: fable.»
  (c) «- D-NNNN+2 — The canon is always CI (the owner's word 03.11.2026, in chat, verbatim: «Канон всегда на CI»; with the word of
  28.10.2026: «Когда всё реализовано, конечные проверки пачки должны занимать не больше часа и всё что возможно идти в CI»): the BATCH
  CANON of a batch and the canon of a release are a CI pipeline on the branch (`api`/`web`, `tools/ci_read.py start`), within 60
  minutes (`canon-clock`, door `canon-over-hour:`); a local docker run is only the fallback when CI is unavailable or red for the
  runner's reason (`docs/RUNBOOK.md` §7). Supersedes D-0056 (3)'s «docker python:3.12 on a tar copy» and the word of 27.10.2026
  «докер-канон один раз и последним» (PROJECT.md p. 2). Detector: calibration check 40. Axes: axis 31 (Role carriers) covered
  (RUNBOOK §7 owner, PROJECT p. 2 pointer); axis 3 covered (the release canon); the others n/a. Tier: fable.»

### §2.4 — the new RUNBOOK §7 (D3 writes it verbatim; Russian carrier; the one owner of the branch run, the canon procedure and the docker fallback)

```
## 7. CI на GitLab и BATCH CANON

CI репозитория живёт на git.example.com, проект 100001 (пространство владельца, общие раннеры, `main` защищена). Какие задачи что
гоняют и при каком источнике пайплайна — шапка `.gitlab-ci.yml` (снимок задач — `tools/test_ci_layout.py`); здесь — как ими
пользоваться. Голый пуш ветки не запускает ничего.

**Прогнать ветку.** Запушить ветку, затем `python tools/ci_read.py start --ref <ветка>` (пайплайн источника `api`; токен со scope
`api`, имя переменной — `gitlab_token_env`, «Командная работа» п. 7 `PROJECT.md`); результат — `python tools/ci_read.py jobs <id>`,
красное — `log <job_id>`, файлы — `artifact <job_id> <путь>`.

**BATCH CANON — пайплайн CI на ветке пачки** (слово владельца 03.11.2026: «Канон всегда на CI»; слово 28.10.2026: «Когда всё
реализовано, конечные проверки пачки должны занимать не больше часа и всё что возможно идти в CI»). Канон пачки и канон релиза —
один и тот же ход: после схождения веток интегратор прогоняет ветку, как выше. Последняя задача пайплайна, `canon-clock`
(`tools/canon_clock.py`), печатает `canon wall time: …` и краснеет после 60 минут; дверь — строка `canon-over-hour: <причина>` в
сообщении головного коммита ветки (проходы считает калибровка, проверка 40). Свидетель канона — id пайплайна, статусы задач и
строка `canon wall time`, дописанные в `witness` последнего `accepted` пачки с меткой BATCH CANON (правило 4 `CLAUDE.md`). Что
канон покрывает — `plans/builder-rules.md` п. 7b.

**Что остаётся локально и почему.** (1) Мутационный проход по спискам мутаций узлов — каждая своим узким файлом (D-0056 (3)):
список мутантов живёт в отчётах узлов, CI его не знает. (2) Локальный прогон (докер) — запасной путь, только когда CI недоступен
или красный по причине раннера, а не кода (слово владельца 03.11.2026: канон — на CI). Тогда исходники — клон ветки без перевода
строк (`git -c core.autocrlf=false clone --branch <ветка> <репозиторий> <папка>`; рецепт архива и `eol` — узел F6-43),
смонтированный ТОЛЬКО на чтение и скопированный ВНУТРЬ контейнера: bind mount Windows → Linux медленнее в 5+ раз и даёт ложные
таймауты (замер 28.10, `plans/piles/onboarding-forge/findings/20261028-kanon-pachki-ne-dolshe-chasa-v-ci.md`):
`MSYS_NO_PATHCONV=1 docker run --rm -v "<папка>:/src:ro" python:3.12 bash -c "cp -a /src/. /repo && cd /repo && git config --global user.name forge-ci && git config --global user.email forge-ci@invalid.example && git config core.hooksPath .githooks && pip install -q pytest pyflakes==3.2.0 pyyaml openpyxl && python -m pytest tools/ -q; cd ai-packages/qa-factory && python -B scripts/selftest.py --jobs 4; python -B scripts/install_smoke.py"`
(рецепт ещё не прогонялся: первый запуск — его проверка; `cd` здесь — внутри контейнера, не в шелле сессии).

Пуш в git.example.com только под VPN (раздел 4).
```

## §3 — builder dispatches (non-overlapping owns; one writer of `.gitlab-ci.yml`)

All three may run in parallel (3 writing slots of 6). Owns are disjoint; checked pairwise: D1 ∩ D2 = ∅, D1 ∩ D3 = ∅, D2 ∩ D3 = ∅.
`tools/piles.py` has ONE writer (D1), so no function split is needed. Mechanism paths are left STAGED for the Lead's commit
(`tools/mechanism_gate.py` prefixes: D1 `tools/piles.py`, `tools/compact_snapshot.py`; D3 `CLAUDE.md`, `DECISIONS.md`,
`docs/SIBLING_MAP.md`, `PROCESS/`, `.claude/agents/`). Branch: the batch branch the Lead names (`pile/onboarding-forge/batch-1` after
`piles.py take`), each builder in its worktree cut from the pushed branch head. Critic: D3 has forks → critic-on-plan of t-1206 + §2.3
before its builder (host adaptation 6; done: t-1708); D1 + D2 → one critic pass on the diff (FK-11 A). **Merge order: D3 merges
after D2** (E-D3-7).

**D1 — piles gates (F6-28 + F6-30), builder (sonnet).**
given: this spec §0 F0-1, F0-2, §2.1, §4 E-D1-*, §5 D1; `tools/piles.py` (docstring :1-74, :1186-1215, :1860-2210, :2569-2930);
`tools/test_pile_cards_contents.py`; `tools/test_piles_form.py`; `tools/test_piles_findings.py`; `tools/test_piles_close_gate.py`;
`tools/test_piles.py`; `tools/compact_snapshot.py` :317-347; `tools/test_compact_snapshot.py`; `plans/piles/_template/batch.md`;
`plans/builder-rules.md`; PROJECT.md «Командная работа» п. 2, 9.
owns:
D:/ws2/yml-text-factory/tools/piles.py (functions: check_form, _leftover_target unchanged, +_contents_reds, +_heading_reds, +contents_problems, +batch_heading_problems, +_leftover_write_reds, +leftovers_unowned, _count_line, check_leftovers (refusal text only), LEFTOVER_KEY_RE, the module docstring)
D:/ws2/yml-text-factory/tools/compact_snapshot.py (findings_summary)
D:/ws2/yml-text-factory/tools/test_piles_form.py
D:/ws2/yml-text-factory/tools/test_piles_findings.py
D:/ws2/yml-text-factory/tools/test_piles_close_gate.py
D:/ws2/yml-text-factory/tools/test_piles.py
D:/ws2/yml-text-factory/tools/test_pile_cards_contents.py
D:/ws2/yml-text-factory/tools/test_compact_snapshot.py
D:/ws2/yml-text-factory/plans/piles/_template/batch.md
D:/ws2/yml-text-factory/plans/PILES.md (generated by `python tools/piles.py board`, never by hand)
non-goals: no change to the close gate's forms; no edit of any real batch file or card (the grandfathered bare items stay); no new
check letter; no `.gitlab-ci.yml`; no docs/PROCESS text (D3 writes it); no `--update` of a ratchet.
handoff: D:/ws2/yml-text-factory/docs/tasks/handoffs/t-NNNN-d1-piles-gates.md (the Lead names the id).
edges: §4 E-D1-1..E-D1-10.
DoD: keys K1-K16 of §5 D1 and the run `python -m pytest tools/test_piles_form.py tools/test_piles_findings.py tools/test_piles_close_gate.py tools/test_piles.py tools/test_pile_cards_contents.py tools/test_compact_snapshot.py -q`, plus `python tools/piles.py board --check` and `python tools/piles.py check --all`, outputs verbatim.

**D2 — CI canon and A19 (F6-44 + F6-50), builder (sonnet).**
given: this spec §0 F0-4, F0-5, §1 (AR-n, FR walk), §2.2, §4 E-D2-*, §5 D2; `.gitlab-ci.yml`; `tools/test_ci_layout.py`;
`tools/test_dup_ratchet.py` :762-776; `tools/test_crap_report.py` :775-811; `tools/test_piles_gitlab.py` :996-1003; `tools/ci_read.py`;
`ai-packages/qa-factory/scripts/selftest.py` (:1-60, :473-724, :837-951); `ai-packages/qa-factory/scripts/tests/test_selftest_slow_tests.py`;
`ai-packages/qa-factory/scripts/slow_tests.json`; `ai-packages/qa-factory/scripts/audit_factory.py` :2357-2399;
`ai-packages/qa-factory/design/factory-rules.md` (whole); `ai-packages/qa-factory/design/architecture.md` AR-1, AR-23, AR-28;
`plans/builder-rules.md`; finding `plans/piles/onboarding-forge/findings/20261028-kanon-pachki-ne-dolshe-chasa-v-ci.md`.
owns:
D:/ws2/yml-text-factory/.gitlab-ci.yml
D:/ws2/yml-text-factory/tools/test_ci_layout.py
D:/ws2/yml-text-factory/tools/canon_clock.py (new)
D:/ws2/yml-text-factory/tools/test_canon_clock.py (new)
D:/ws2/yml-text-factory/tools/test_dup_ratchet.py (k23 only, and only if it turns red)
D:/ws2/yml-text-factory/tools/test_crap_report.py (the CI-pin tests only, and only if they turn red)
D:/ws2/yml-text-factory/ai-packages/qa-factory/scripts/selftest.py (main's argparse, cmd_tests, cmd_slow_tests, +shard_files, the docstring)
D:/ws2/yml-text-factory/ai-packages/qa-factory/scripts/tests/test_selftest_shard.py (new)
D:/ws2/yml-text-factory/ai-packages/qa-factory/changelog.d/onboarding-forge-1-f6-50.md (new)
non-goals: no `audit_factory.py` change (FK-4 B is a separate row); no `tools/batch_canon.py` (F6-34); no `ci_read.py` change; no
change to `crap-measure`; no `slow_tests.json --update`; no RUNBOOK/PROJECT text (D3); no full `selftest.py`, no `install_smoke.py`,
no docker on the builder's machine (D-0056) — the branch pipeline proves the CI change.
handoff: D:/ws2/yml-text-factory/docs/tasks/handoffs/t-NNNN-d2-ci-canon.md.
edges: §4 E-D2-1..E-D2-10.
DoD: keys S1-S8, C1-C6, L1-L6, M1-M2 of §5 D2; runs `python -m pytest tools/test_ci_layout.py tools/test_canon_clock.py -q`,
`python -m pytest tools/test_dup_ratchet.py -q -k k23`, `python -m pytest tools/test_crap_report.py -q -k "crap_measure_job or ci_header"`,
`python -m pytest tools/test_piles_gitlab.py -q -k ci_job_is_a_nightly`, `python -B ai-packages/qa-factory/scripts/tests/test_selftest_shard.py`,
`python -B ai-packages/qa-factory/scripts/tests/test_selftest_slow_tests.py`, `python -B ai-packages/qa-factory/scripts/selftest.py --lang`;
then the live proof `python tools/ci_read.py start --ref <branch>` (after the push) and its `jobs` / `log` lines.

**D3 — role carriers and the canon / leftovers text (F6-33 + text of F6-28/F6-30/F6-50), builder (sonnet), after critic-on-plan.**
given: this spec §0 F0-3, F0-6, F0-7, F0-8, §2.3 (Δ1-Δ20), §2.4, §4 E-D3-*, §5 D3; `docs/tasks/specs/t-1206-f6-33-role-carriers-one-owner.md`
(whole); the critic's review `docs/tasks/specs/reviews/t-1708-d6-d3-plan.md`; `docs/tasks/handoffs/t-1205-verification-carriers.md`;
every file of t-1206 §2 plus `docs/RUNBOOK.md` §7 (:317-331), `docs/tasks/critic-diff-brief.md` :8-22, `PROJECT.md` :178-210,
`plans/builder-rules.md` :14-48; `tools/tests/test_integration_batch_0_9_forge.py` :47-56; `tools/install_parity.py`; `tools/agents_md.py`;
`tools/mechanism_gate.py` :211-260, 403-572; `plans/builder-rules.md` p. 2, 17, 18.
owns:
D:/ws2/yml-text-factory/plans/builder-rules.md
D:/ws2/yml-text-factory/PROJECT.md
D:/ws2/yml-text-factory/.claude/agents/builder.md
D:/ws2/yml-text-factory/.claude/agents/critic.md
D:/ws2/yml-text-factory/.claude/agents/designer.md
D:/ws2/yml-text-factory/docs/tasks/critic-diff-brief.md
D:/ws2/yml-text-factory/CLAUDE.md
D:/ws2/yml-text-factory/docs/CLAUDE_HOST_ADAPTATIONS_FULL.md
D:/ws2/yml-text-factory/SYSTEM_PROMPT.md
D:/ws2/yml-text-factory/docs/RUNBOOK.md
D:/ws2/yml-text-factory/docs/tasks/pre-release-0.9-brief-common.md
D:/ws2/yml-text-factory/PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md
D:/ws2/yml-text-factory/DECISIONS.md (t-1206 E14b only)
D:/ws2/yml-text-factory/docs/TWO_VOCABULARIES.md
D:/ws2/yml-text-factory/docs/SIBLING_MAP.md
D:/ws2/yml-text-factory/tools/test_handoff_rule_anchors.py
D:/ws2/yml-text-factory/tools/install_parity_anchors.json
D:/ws2/yml-text-factory/tools/tests/test_role_carriers_one_owner.py (new)
D:/ws2/yml-text-factory/AGENTS.md (generated by `python tools/agents_md.py --repo D:/ws2/yml-text-factory`, never by hand)
non-goals: no package file; no CURRENT_CONTEXT.md (Δ7); no new D-entry — the three of Δ20 are the Lead's; no scout.md, judge.md,
skills, BOOT.md, DELEGATION_TABLE.md, `.gitlab-ci.yml`, `tools/*.py` code; no rule meaning beyond t-1206 §2 + the deltas; no commit
of a mechanism path (left STAGED); no exam invented for critic.md.
handoff: D:/ws2/yml-text-factory/docs/tasks/handoffs/t-NNNN-d3-role-carriers.md — it ends with «Needed from the Lead before the
commit»: the Δ20 (a), (b), (c) D-lines (drafts in this spec); FK-12; the E-D3-7 reconciliation at merge.
edges: t-1206 §5 E1-E14 + §4 E-D3-1..E-D3-7.
DoD: t-1206 keys K1-K20 with the deltas (K8 dropped, K12 = its first two greps, K15 = 31) + keys T1-T18 of §5 D3; runs R1-R7 of
t-1206 §5 + `python -m pytest tools/test_mechanism_gate.py tools/tests/test_integration_batch_0_9_forge.py -q`.

## §4 — edges (behaviour + the invariant it protects)

D1:
- E-D1-1 (empty / absent) A card with no «## Содержание» → item 1 is not judged (older form). Invariant: a real card without the
  section is still refused — by `test_pile_cards_contents.py::test_every_id_and_findings_file_once_in_contents` in CI.
- E-D1-2 (count, AT and BEYOND) a finding name 1× → ok; 0× → red; 2× → red. Whole-token count (`_name_re`): `x.md` inside
  `ax.md` does not count. Error direction of the reused `_name_re` in a gate role: it may only UNDER-count a name glued to a longer
  token (a false red, safe); it never counts a different file as this one. Adversarial inputs that must stay red: the name only
  inside a fence or a comment of «Содержание», the name as a substring of a longer name, the name in another pile's card.
- E-D1-3 (positional) a taken batch without «## Бриф» → not judged. Invariant: no untaken batch is born without the heading; a frozen
  text is never asked to change (no red that only a (в) door could pass).
- E-D1-4 (temporal) BEFORE D1 merges, the real tree may hold bare «Остатки» items; AFTER, they stay legal (old) and are counted.
  Builder step 0: run `leftovers_unowned` on the untouched tree and print N per pile in the handoff (the baseline the calibration
  reads). Invariant: a NEW or CHANGED bare item never passes a commit without the (д) door.
- E-D1-5 an old bare item edited without adding a key → red (changed). An old item moved to another line unchanged → old. Two
  identical item texts in one file → matched as a multiset (one old copy does not legalize a second new one).
- E-D1-6 base unreadable (`--base` rev missing, a git failure other than «path absent at rev») → every item of the staged file is judged
  and one note line says why. Invariant: an unreadable base never makes a new bare item «old». Path absent at the base → new file.
- E-D1-7 `узел:` resolution: unknown id → red naming where it looked; node with empty «Исполнитель» → red; node only in a «закрыта» batch
  → red; `<slug>/<N>/<id>` with an unknown pile or batch → red; a `узел:` value with trailing text (`узел: XX1-3 (later)`) → red (the
  value stands alone, the same rule as `сделано:`). Invariant: `узел:` passes only when a worked node row exists right now.
- E-D1-8 conflicting pair «write-time `подтвердил: —` allowed» vs «close demands a person» → resolved by scope: (д) accepts the
  placeholder, `close` still refuses it (unchanged). Invariant: an agent never confirms its own carry-over at close.
- E-D1-9 the count line at 0 → `остатков без исполнителя: 0` (always printed). The compact snapshot's cap (240): the counter is in
  the tail that is never cut; only the per-pile listing shrinks. Invariant: the counter is never truncated away.
- E-D1-10 a «закрыта» batch's «Остатки» → never judged by (д) (its close already judged it).

D2:
- E-D2-1 `--shard` boundaries: `1/1` = the full list; `N/N` valid; `0/2`, `3/2`, `1/0`, `2`, `a/b`, `1/2/3`, `-1/2` → exit 2 with the
  expected form. Invariant: an invalid shard never runs a partial set as if it were whole.
- E-D2-2 N > number of test files → empty shards print the explicit note and PASS. Invariant (AR-23): an empty shard is a declared
  outcome, never a silent zero.
- E-D2-3 partition invariants: for every N in 1..5 the shards are pairwise disjoint and their union equals the full list; shard I's
  list does not depend on which I is asked. A file listed in `slow_tests.json` but absent on disk is not partitioned (it does not
  exist); a file on disk not listed gets the default weight.
- E-D2-4 conflicting flags (`--fast`, `--slow-tests`, check flags without `--tests`) → refused at argparse. Invariant: `--fast` stays
  the one per-MR tier; a measurement never reads a partial run as whole.
- E-D2-5 non-test checks: only shard 1; `--hygiene` in every shard. Invariant: every check of the flagless run runs exactly once per
  pipeline (hygiene once per checkout — each shard has its own).
- E-D2-6 joined outputs: headers {1..N} each once → measured; a missing shard, a repeated shard, mixed N → exit 2 naming them; no
  header → today's behaviour. Invariant (AR-28): a missing shard output never becomes «unchanged». Named blind spot: a shard that
  printed its header and crashed before its duration lines passes the join — its own job is red.
- E-D2-7 clock boundary: 3600 s → ok, 3601 s → red; the door with a real reason → exit 0; with a placeholder reason → not a door.
  Start unknown / elapsed < 0 → exit 2 (the same door passes it). Invariant: a canon over the hour is never green without the
  person's or Lead's written reason.
- E-D2-8 `package-full-report` with no shard artifact → `cat` fails (bash `-e` of the runner) → red. Invariant: no drift verdict
  without both shards.
- E-D2-9 (environment unknown) the GitLab instance's support of `needs: []`, `parallel:`, `needs` on a parallel job and
  `CI_PIPELINE_CREATED_AT` is not measured here (estimate: all exist since GitLab 13.10). The branch pipeline is the experiment
  (command hygiene p. 6 (a)): `ci_read.py start` refused with a YAML error → the builder reports the verbatim message and stops; the
  fallback (stages instead of `needs`) is the Lead's call.
- E-D2-10 the A19 step on a package where A19 is red → `package-fast` red (that is the point); `--agents` on the bare package must
  need no project: the builder runs it once locally (D2-M1) and reports its exit; non-zero for a reason other than an A19 finding →
  stop and report (FK-4).

D3:
- E-D3-1 an E-item whose verbatim old text is gone and no delta covers it → NOT DONE, named; never re-written from memory; a line
  range is never used as an anchor (Δ19). Invariant: no rule text changes meaning by a stale quote, and 7c is never deleted.
- E-D3-2 install parity: only the two designer anchors of t-1206 E18 may move. Invariant: `install_parity --check` exit 0 with no
  `parity-skip:` door.
- E-D3-3 axis count: after D3, `^## Axis ` = 31; a parallel branch that adds axis 31 first → renumber this axis to the next free number
  at merge (the integrator), K15 follows. Same for calibration 39/40.
- E-D3-4 (temporal) before D3 merges, mechanism commits carry 30 axis lines; after, 31 (`tools/mechanism_gate.py` reads the map's
  headings). The commit that adds axis 31 itself carries 31.
- E-D3-5 FK-8 is the owner's word (03.11.2026 «Канон всегда на CI»): Δ5 removes the 27.10 «Докер-канон — один раз и последним»
  paragraph and writes the new paragraph quoting the 03.11 word verbatim; RUNBOOK §7 cites the same word. Invariant: every carrier
  that states the canon's place quotes the owner's word it rests on, and no carrier still says the release canon is a local docker
  run (T17). The release ORDER of 27.10 is not restated anywhere until FK-12 is answered.
- E-D3-6 the docker recipe of §2.4 is unrun → its text says so. Invariant: no unverified recipe is presented as proven.
- E-D3-7 (temporal, t-1708 F7) D3's texts name artefacts that only D2 creates: `canon-clock`, `tools/canon_clock.py` (§2.4, check 40,
  Δ17), the `--shard` split (none — D3 names no job list, B2). BEFORE D2 merges, these names do not exist on `main`: D3 is never merged
  ahead of D2 (merge order, §3). AT the convergence of D2 and D3, the integrator runs `git grep -n "^canon-clock:" -- .gitlab-ci.yml`
  and `git ls-files tools/canon_clock.py` — both must print one line; if D2 renamed or dropped them (E-D2-9, FK-7 B), §2.4, check 40
  and the axis-31 row are corrected in the same merge commit (a Lead step, named in D3's handoff). Invariant: no carrier names a
  CI job or tool that the merged tree lacks.

## §5 — witness (exact commands; keys quoted before any run)

**D1** (from the worktree root):
- Step 0 (baseline): a one-off call of `leftovers_unowned` through the test file's helper or `python -c` READ-ONLY payload (a pure read,
  hygiene pt. 4 (b)) — output N per pile, verbatim.
- K1 staged finding not in «Содержание» → (д) red naming finding and card; K2 named twice → red; K3 card without «Содержание» → no
  red from item 1; K4 untaken batch without «## Бриф» → red, taken one → none; K5 a row id absent from «Содержание» → red; K6
  `x.md` vs `ax.md` whole token; K7 new bare item → red with the three forms and the door; K8 `сделано: t-12` ok, `сделано: —` red;
  K9 `узел:` own-pile ok / unknown red / empty executor red / closed-only red / cross-pile `slug/N/id` ok; K10 `перенос … подтвердил: —`
  passes (д) and is still refused by `close`; K11 old bare item unchanged → no red, edited → red; K12 closed batch skipped; K13 file
  absent at base → all items judged; K14 count line `остатков без исполнителя: N` (0 printed) and the snapshot tail; K15 `узел:` line
  places a finding for (е), `узел:` mid-sentence does not; K16 unreadable base → all judged + note.
- Run: `python -m pytest tools/test_piles_form.py tools/test_piles_findings.py tools/test_piles_close_gate.py tools/test_piles.py tools/test_pile_cards_contents.py tools/test_compact_snapshot.py -q`
- `python tools/piles.py board` then `python tools/piles.py board --check` (exit 0); `python tools/piles.py check --all` (exit 0: the
  real tree's old items are «old» against HEAD).
- Negative control: a temp copy test where one bare item is appended to a staged batch → (д) red (part of K7; a gate that cannot fail
  is not a gate).
- Mutations NAMED, not run (D-0056 (2)): M-a `_leftover_write_reds` treats every item as old → killed by K7; M-b drop the
  `NO_VAL` executor check → K9 (empty executor); M-c `LEFTOVER_KEY_RE` without `узел` → K15; M-d count `>= 2` instead of `!= 1` in
  `contents_problems` → K1.

**D2** (from the worktree root):
- S1 `--shard 1/1` = full list; N in 1..5 disjoint + union; S2 the invalid values of E-D2-1 → exit 2 with the form; S3 N > files →
  explicit note + PASS; S4 the refused combinations; S5 shard 1 runs the non-test checks, shard 2 only tests + hygiene (spy on the
  `cmd_*`); S6 the header line text; S7 the join: complete / missing / repeated / mixed / no header; S8 LPT order and the tie by name.
- C1 3600 → 0, 3601 → 1; C2 door with reason → 0, door `canon-over-hour: —` → 1; C3 absent / unparseable start → 2, with door → 0;
  C4 elapsed < 0 → 2; C5 `Z`, `+00:00`, fractional parse; C6 the printed line shape.
- L1 GOLDEN equals the effective jobs; L2 `package-full` has `parallel: 2`, `needs: []` and `--shard "$CI_NODE_INDEX/$CI_NODE_TOTAL"`;
  L3 `install-smoke` and `package-full-report` carry `package-full`'s rules, the report `needs: [package-full]`; L4 `canon-clock` rules
  are api/web only with `when: always`, stage `clock` is last; L5 `package-fast` has api/web rules and the `audit_factory.py --agents`
  step after `--fast`; L6 `forge-check` has the web rule. (`test_ci_layout.py` is itself the negative control: a golden that differs
  is red.)
- M1 (F6-44 measurement, local, once): `time python -B ai-packages/qa-factory/scripts/audit_factory.py --agents` (bash builtin
  `time`) — the exit code, the `=== Result:` line and the real time, verbatim. M2 (CI): the `audit_factory --agents wall time: N s`
  line of the branch pipeline's `package-fast` log. Over 60 s → a line to the Lead (an estimate today: seconds).
- Runs: `python -m pytest tools/test_ci_layout.py tools/test_canon_clock.py -q`; `python -m pytest tools/test_dup_ratchet.py -q -k k23`;
  `python -m pytest tools/test_crap_report.py -q -k "crap_measure_job or ci_header"`; `python -m pytest tools/test_piles_gitlab.py -q -k ci_job_is_a_nightly`;
  `python -B ai-packages/qa-factory/scripts/tests/test_selftest_shard.py`; `python -B ai-packages/qa-factory/scripts/tests/test_selftest_slow_tests.py`;
  `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
- Live proof (the CI change is proved by a pipeline on the branch): push, then `python tools/ci_read.py start --ref <branch>`;
  `python tools/ci_read.py jobs <id>` must list forge-check, package-fast, `package-full 1/2`, `package-full 2/2`, install-smoke,
  board-check, package-full-report, canon-clock; `python tools/ci_read.py log <canon-clock job> --grep "canon wall time"` and
  `python tools/ci_read.py log <package-fast job> --grep "wall time|Result"` — verbatim. A red job: its `log` lines verbatim, no fix
  by guess.
- Mutations NAMED, not run: M-e `shard_files` assigns by index modulo N ignoring weights → S8; M-f the join ignores a missing shard →
  S7; M-g `>=` instead of `>` at the limit → C1; M-h the door accepts an empty reason → C2.

**D3** (from the worktree root): t-1206 §5 K1-K20 with Δ7 (K8 dropped), Δ2 (K12 = `git grep -n -F "no docker, no ratchets" -- DECISIONS.md`
must now print ONE line — it stays — and `git grep -n -F "axis 5 covered (the critic" -- DECISIONS.md` none), Δ1 (K15 count 31), plus:
- T1 `git grep -c -F "## Axis 31 — Role carriers: one owner per aspect <-> pointers" -- docs/SIBLING_MAP.md` → `docs/SIBLING_MAP.md:1`
- T2 `git grep -c -F "узел: <node id>" -- docs/tasks/critic-diff-brief.md` → `:1`
- T3 `git grep -c -F "39. **«Остатки» items carry an executor" -- PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` → `:1`;
  `git grep -c -F "40. **BATCH CANON within the hour, always in CI" -- PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` → `:1`
- T4 `git grep -n -F "одна задача, \`forge-check\`" -- docs/RUNBOOK.md` → none; `git grep -c -F "canon-over-hour:" -- docs/RUNBOOK.md` → `:1`
- T5 `git grep -n -F "докер python:3.12 (tar-копия)" -- plans/builder-rules.md` → none; `git grep -c -F "\`lint_ratchet --check\` + the console scan" -- plans/builder-rules.md` → `:1`
- T6 `git grep -c -F "BATCH CANON — пайплайн CI на ветке пачки" -- docs/RUNBOOK.md` → `:1`; the same in `PROJECT.md` → none (pointer only)
- T7 `git grep -c -F "The «Остатки» item forms have ONE reader" -- docs/SIBLING_MAP.md` → `:1`
- T8 (negative control) `git grep -c -F "BATCH CANON — пайплайн ~deliberately broken~" -- docs/RUNBOOK.md` → no output, exit 1.
- T9 `git grep -c -F "строка «Остатков» с ЗАПИСИ несёт" -- PROJECT.md` → `PROJECT.md:1`
- T10 `git grep -c -F "Тесты идут в CI, не на машине разработчика" -- PROJECT.md` → `PROJECT.md:1`
- T11 `git grep -c -F "доказывает пайплайн ветки" -- plans/builder-rules.md` → `:1`
- T12 `git grep -c -F "tools/canon_clock.py" -- docs/SIBLING_MAP.md` → `:1`
- T13 (B1) `git grep -n -F "from the worktree root (B-417, D-0033)" -- docs/tasks/critic-diff-brief.md` → none;
  `git grep -n -F "ratchets beyond" -- docs/tasks/critic-diff-brief.md` → none
- T14 (B1) `git grep -c -F "their result is the \`forge-check\` job of the" -- docs/tasks/critic-diff-brief.md` → `:1`
- T15 (B2) `git grep -n -F "на каждый пуш и MR" -- PROJECT.md` → none; `git grep -c -F "прогнать ветку и прочитать результат — \`docs/RUNBOOK.md\` §7" -- PROJECT.md` → `:1`
- T16 (B2) `git grep -c -F "только когда CI недоступен или красный по причине раннера, а не кода" -- docs/RUNBOOK.md` → `:1`; the same
  string in `PROJECT.md plans/builder-rules.md` → none; `git grep -n -F "CI красный или недоступен" -- PROJECT.md` → none
- T17 (FK-8, the owner's word) `git grep -c -F "**Канон всегда на CI** (слово владельца 03.11.2026: «Канон всегда на CI»" -- PROJECT.md`
  → `:1`; `git grep -n -F "Докер-канон — один раз и последним" -- PROJECT.md docs/RUNBOOK.md plans/builder-rules.md` → none;
  `git grep -c -F "слово владельца 03.11.2026: «Канон всегда на CI»" -- docs/RUNBOOK.md` → `:1`;
  `git grep -n -F "до слова владельца — FK-8" -- PROJECT.md docs/RUNBOOK.md` → none
- T18 (B3, F4, F5) `git grep -c -F "7c. **\`story_run.py\` и слои драйвера**" -- plans/builder-rules.md` → `:1`;
  `git grep -c -F "храповики — билдер НЕ гоняет" -- plans/builder-rules.md` → `:1`;
  `git grep -c -F "test_console_encoding.py" -- plans/builder-rules.md` → `:1`
- One-line anchors (t-1206 §5 E4 list, extended — never wrapped across a line by a re-wrap): «`lint_ratchet --check` + the console
  scan», «BATCH CANON — пайплайн CI на ветке пачки», «The «Остатки» item forms have ONE reader», «строка «Остатков» с ЗАПИСИ несёт»,
  «Тесты идут в CI, не на машине разработчика», «доказывает пайплайн ветки», «храповики — билдер НЕ гоняет», «their result is the
  `forge-check` job of the», «прогнать ветку и прочитать результат — `docs/RUNBOOK.md` §7», «только когда CI недоступен или красный по
  причине раннера, а не кода», «**Канон всегда на CI** (слово владельца 03.11.2026: «Канон всегда на CI»», «слово владельца 03.11.2026:
  «Канон всегда на CI»».
- Runs: t-1206 R1 (before the edits: red on its six keys; after: green), R2-R7; `python -m pytest tools/test_mechanism_gate.py tools/tests/test_integration_batch_0_9_forge.py -q`.

**Batch canon** (the Lead, after D1-D3 converge): the pipeline of D2's live proof on the converged branch; its id, job statuses and
`canon wall time` line appended to the batch's last `accepted` witness labeled BATCH CANON.

## §6 — forks (returned; recommendation first)

- **FK-1** (F6-30) `узел:` at `close`. A: close unchanged — `узел:` is a write-time key; the integrator turns it into `сделано:` when the
  node merges, or carries it with a person. B: close accepts `узел:` when the node lives in an open batch of ANOTHER pile (a machine-
  verified executor, no person). **Recommend A** — the owner's word 08.10 «перенос подтверждает человек»; B would make `узел:` a
  person-less carry.
- **FK-2** (F6-30) old bare items. A: judge only new/changed items; the board counts the old ones (the baseline of check 39). B: judge
  every item of open batches now and fix them in the same batch. **Recommend A** (+ step 0 measures N; with a small N the Lead may
  clean them by hand in the batch's «Остатки», which A then judges as changed).
- **FK-3** (F6-30) where a `узел:` node may live. A: any not-closed batch whose node has an executor. B: only an UNTAKEN batch (the
  finding's words). **Recommend A** — a node of a taken batch is being worked; B would refuse the most common case (the Lead's own
  open batch).
- **FK-4** (F6-44) scope of the fast-tier role check. A: A19 via the existing `--agents` (no package change). B: a new
  `audit_factory.py --roles` = A2 + A2b + A2c + A19 (project-free, F0-4) — a package change outside this dispatch. **Recommend A now,
  B as a new row** of `onboarding-forge` (the class the finding names — «родственные проверки» — is not fully closed by A).
- **FK-5** (F6-50) canon on MR pipelines. A: canon = `api`/`web` pipeline on the branch, started once after convergence; MR pipelines
  stay the fast tier. B: `package-full` also on every MR push. **Recommend A** (D-0056: once per batch).
- **FK-6** (F6-50) ref filter. A: `api`/`web` on any ref (pile/*, release `claude/*`, `local/*` merge branches). B: only `pile/*` and
  `main`. **Recommend A** — MR !13's branch was `claude/release-10-9-706cee`; the start is a deliberate act of a token holder.
- **FK-7** (F6-50) shard now or later. A: `--shard` + `parallel: 2` now. B: only `needs: []` + the clock now (today's canon is 18-23
  min, F0-5); shard when the clock first passes 45 min. **Recommend A** — the owner named sharding; it is cheap and buys margin for
  growth; n = 2 because the wall is bounded by `forge-check` anyway.
- **FK-8** — CLOSED by the OWNER, word of 03.11.2026: «Канон всегда на CI». The batch canon and the release canon are the CI pipeline
  on the branch; the 27.10 «докер-канон один раз и последним» is superseded; local docker is only the fallback when CI is unavailable or
  red for the runner's reason. Written into Δ5, §2.4, check 40 and the Lead's D-line Δ20 (c).
- **FK-9** (F6-33) the ratchets. A: batch level (7c, Lead 26.10; CI `forge-check` runs both on every MR and canon) — reverses t-1206
  L3/E14a; the brief follows (Δ18) and D-0033 is refined by a Lead D-line (Δ20 (a)). B: t-1206 L3 (the builder runs `dup_ratchet
  --check` and `lint_ratchet --check`) — then Δ18 is dropped and 7b/7c change instead. **Recommend A** — the newer Lead text and CI
  already run them.
- **FK-10** (F6-33) t-1206 F-1..F-12 as Δ10 states them (F-10 read through FK-9, F-12 = the console scan by type); F-6 A needs the
  Lead's D-line (Δ20 (b)) before D3's commit. **Recommend: accept as Δ10.**
- **FK-11** critic layout. A: critic-on-plan for D3 (t-1206 + §2.3), then ONE critic pass on the D1 + D2 diffs (one forge topic,
  R13-g). B: a critic pass per dispatch. **Recommend A** (host adaptation 6: one pass per topic).
- **FK-12 — ANSWERED, A (owner's word 03.11.2026: «Да» to «канон один раз на релиз, последним и не гейт на MR»).** The RUNBOOK §7
  sentence of option A goes in with D6-D2.
- **FK-12** (NEW, from FK-8's answer; an interpretation of the owner's words — the owner's or the Lead's call) does the 27.10 release
  ORDER survive the 03.11 word? The superseded passage also said: when several batches make one release, the canon runs ONCE for the
  whole release, in the order nodes → piles → `main` → publication → canon, and is a gate neither on the MR nor on the publication. A:
  the order survives (the 03.11 word replaced WHERE the canon runs, not WHEN): the Lead adds one sentence to RUNBOOK §7 after
  «Канон пачки и канон релиза — один и тот же ход:» — «для релиза из нескольких пачек — один раз по всему релизу и последним (узлы →
  кучки → `main` → публикация → канон), не гейт ни на MR, ни на публикации (слово владельца 27.10.2026)». B: the whole 27.10 passage is
  gone; the release canon runs before publication like any branch canon. **Recommend A** (the 03.11 word is about the place; the
  order is a separate decision nobody revoked). As written, D3 states neither (E-D3-5), so D3 is executable before the answer.

## Small choices closed (no design weight)

S1. LPT greedy with default weight `fast_under_s / 2` for unlisted files; ties to the lowest shard index, files ordered by name.
S2. Shard output name `ci-out/selftest-shard-<I>-of-<N>.txt`; the joined file keeps the old name `ci-out/selftest.txt`.
S3. The dup report runs in shard 1 only (k23's shape kept: mkdir < report < cd, `||` without `|| rc=1`).
S4. `install-smoke` and `package-full-report` take `package-full`'s rules, image, variables; `install-smoke` keeps timeout 3h (no
new limit introduced); the report and the clock get short timeouts (10m, 5m — runner limits, not norms; not tested).
S5. The clock is a committed script with a test (FR-28), not an inline shell block.
S6. Stage names `report` and `clock`; `crap-measure` keeps stage `nightly` (its pin compares with `package-full`).
S7. The count line text «остатков без исполнителя: N» (Russian, like the rest of `_count_line`); the snapshot text English (its
carrier is English).
S8. Calibration numbers 39 and 40 (next free; E-D3-3 renumbers on collision).
S9. RUNBOOK §7 is rewritten rather than appended (its old content is stale, F0-6).
S10. The owner of the CI job map is the `.gitlab-ci.yml` header, not RUNBOOK §7 (t-1708 B2 offered either): it is written by the one
writer of the jobs in the same commit, so it cannot lag behind them; RUNBOOK §7 owns the procedure and the fallback wording.
S11. The fallback wording «только когда CI недоступен или красный по причине раннера, а не кода» reads the addendum's «when CI is red
or unavailable» narrowly: a red caused by the code is fixed, not re-run in docker.

## Queued (from critic t-1708; not fixed in this resubmission)

- F10: the axis-31 closing rule (t-1206 §3: records «are never edited to follow») vs E14b, kept by Δ9, which corrects D-0056's axes line
  in place. To decide: drop E14b for a Lead D-line, or add «an error correction marked inline» to the closing rule.
- F11: the §2.4 docker recipe returns install_smoke's exit code and hides a red pytest/selftest — the recipe should track `rc`
  (`rc=0; … || rc=1; …; exit $rc`). The recipe is declared unrun (E-D3-6); fix with F6-43 or at its first use.
- F12: t-1206 also says «axis 22» in its edges E5, E9, E11 («22 lines») and R7 — those are spec text, not carriers; Δ1 covers only what
  D3 writes into a carrier. If the builder is unsure about one, it reads 31 and names it in the handoff.

## Noticed analogs and contradictions (reported, not in scope)

A1. The batch row says `tools/tests/test_piles.py` (F6-30 «Пишет в»); the file is `tools/test_piles.py` (Glob). A2. Memory notes
`package-tests-proved-in-docker-before-merge` and `slow-tests-proved-on-ci-image` (outside the repo) still say «docker per batch» —
the Lead's fix now that the owner said «Канон всегда на CI». A3. D-0056 (3) and builder-rules 7b name «docker python:3.12 (tar-копия)»;
D3 fixes 7b, D-0056 needs the Lead's D-entry (Δ20 (c)). A4. F6-34 (`tools/batch_canon.py`) should be re-scoped to «start the pipeline
and read it» (finding F6-50 item 6) — its row is not edited here. A5. `forge-check` (`pytest tools/`, 7155 tests) may become the
canon's longest job once the selftest is sharded; the clock line shows it — a candidate for `pytest -n`/sharding if it nears the hour.
A6. RUNBOOK §7 named `experiments/dev-speed/gitlab_ci_check.py`; the rewrite drops it in favour of `ci_read.py` (the tool every
session uses). A7. The release runbook text (PROJECT.md «Релиз», RUNBOOK §4) may still name a docker canon before publication — not
read here; the Lead checks it against the 03.11 word.

## Reading trail

Read in full: `docs/tasks/p1-closeout-0-10-9.md`; the five findings (F6-28 `20261020-forge-check-krasnyj-…`, F6-30
`20261021-ostatki-pachki-…`, F6-33 `20261021-nositeli-roli-…`, F6-44 `20261027-a19-nad-realnym-paketom-…`, F6-50
`20261028-kanon-pachki-ne-dolshe-chasa-v-ci.md`); `docs/tasks/specs/t-1206-f6-33-role-carriers-one-owner.md` (1-1007);
`.gitlab-ci.yml`; `docs/TWO_VOCABULARIES.md`; `tools/ci_read.py` 1-210; resubmission: `docs/tasks/specs/reviews/t-1708-d6-d3-plan.md`
(whole). By range: batch file rows 40-61; `tools/piles.py` 25-74,
925-1060, 1186-1215, 1855-2240, 2560-2930; `tools/test_pile_cards_contents.py` 1-120; `tools/test_ci_layout.py` 1-90 + grep of tests;
`tools/test_crap_report.py` 775-811; `tools/test_dup_ratchet.py` 762-776; `tools/test_piles_gitlab.py` 990-1003;
`tools/compact_snapshot.py` 300-360; `tools/mechanism_gate.py` 211-260; `ai-packages/qa-factory/scripts/selftest.py` 20-80,
473-535, 679-738, 837-951 + greps; `scripts/slow_tests.json` 1-30; `scripts/tests/test_selftest_slow_tests.py` 1-40;
`scripts/audit_factory.py` 1-30, 120-160, 2357-2399 + greps; `plans/builder-rules.md` 14-48; `DECISIONS.md` 46, 74; `CURRENT_CONTEXT.md`
150-164; `docs/RUNBOOK.md` 317-331 + greps; `PROJECT.md` 178-210; `docs/tasks/critic-diff-brief.md` 8-22;
`PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` greps (checks 33-38, :362);
`docs/tasks/pre-release-0.9-brief-common.md` 1-6; `plans/piles/_template/batch.md` grep; `ai-packages/qa-factory/design/architecture.md`
greps (AR-12/18/23/28 and change checks). Greps with positive controls: «cover the test sets» (CLAUDE.md hit = control for the
RUNBOOK/CURRENT_CONTEXT negatives), «builder-rules» in CURRENT_CONTEXT (2 hits = control for «builder-rules rows owed» absent),
`^## Axis \d+` in SIBLING_MAP (30 headings), `package-full` across tools/ (6 files), journal `t-1206` (parked status, line 1475).
Not read: `tools/test_piles*.py` bodies (the builder reads them), `.claude/agents/*.md` beyond what t-1206 quotes (critic.md:150 and
designer rule 1 confirmed still in the old form), `tools/install_parity_anchors.json` (t-1206 F0-4 relied on), `tools/mechanism_gate.py`
`label_problem` body (the labelled form is taken from t-1708 (4) and F8), PROJECT.md «Релиз» and RUNBOOK §4 (A7).
