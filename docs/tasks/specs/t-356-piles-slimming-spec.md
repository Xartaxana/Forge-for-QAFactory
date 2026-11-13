# t-356 — piles.py slimming: no board, judge only what the commit touches, `status`, one developer's batches

Designer draft for the Lead, revised in fix round t-375 after the critic's plan review t-367
(`docs/tasks/specs/reviews/t-367-piles-slimming-plan-review.md`) and the Lead's fork decisions of 13.11.2026. Every fact
below was read on `.claude/worktrees/read-main` (origin/main at a234cc6; the review re-read the lines on 9a7f72a, same
commit message, same tree). Line numbers are on that tree. §7 records the decisions; ONE question to the owner stays open
(Q-O1, §7). Tags `(t-367 Xn)` mark where a review edit landed; the table «Review t-367 applied» at the end lists them.
Questions back to the Lead from this fix round: the section «Questions back to the Lead (t-375)» before that table.

---

## 1. Intent and the owner's decided words

The owner's words, 13.11.2026, verbatim:

- About the board, earlier in the day: «у нас сейчас нет борды, только виджет беклога. А этот скрипт ещё и мешает закрывать узлы в пачках».
- About the board, later: «Сейчас доски в гитхабе нет, можно убрать её из проджект.мд и из скрипта» (`plans/PILES.md`).
- About the zone of a batch («the script counts a batch's zone by all unaccepted nodes, so one waiting node with a zone like
  scripts/tests/ blocks the take of any other batch»): «это надо исправить» and «Это верно для двух разработчиков и не верно
  внутри одной сессии как сейчас».

What the owner looks at: the «Бэклог» pane. `tools/claude-mods/backlog/hooks/register.tsx:8` runs `tools/backlog_tree.py`,
which reads `piles.load_tree` (`tools/backlog_tree.py:34`). Nothing in that chain reads `plans/PILES.md`. The docstring
line `backlog_tree.py:1` only says the board "stays the board".

Measured by the Lead (brief, git log origin/main since 2026-10-08, journal t-350 at dev1.jsonl:896): 588 commits, 140 with
`piles-skip:`, 260 skip lines, about 240 of them "untracked foreign pile live-run-fvf" on items д and е. The critic re-measured
it (review t-367 P2: 591 / 141 / 264 / 245, a few commits newer). The mechanism behind it is in §3 B.0, read from the code.

What changes, part by part:
- A (decided): the generated board goes away. That covers its code, its gates, its file and every text that calls it the
  authority.
- B (direction decided): a red blocks only a commit (or pushed range) that touches the pile it sits in.
- C (direction decided): `piles.py status` becomes the one writer of «сдано»/«принято» (node F6-13).
- D (decided by the owner): the zone overlap rule of (б) and `take` protects one developer from another. Two batches of the
  SAME developer never block each other. The empty-token fix is part of D.
  Reading: "session" is taken as "developer slug" (every session and clone of dev1). This is wider than the word; QUESTION
  TO THE OWNER (Q-O1, §7), with a recommendation: (a) one developer = one slug (recommended: no session identity exists in
  `взял:`); (b) narrower: none available without a session id in `взял:`. The node runs on (a) until the answer
  (PROJECT.md «Командная работа» p. 11). (t-367 B2)

Package: none of these nodes touches `ai-packages/qa-factory/`, so §1 owes no AR-n list. Checks this spec adds or changes,
with their owner and census class: (б) same-developer skip, the "touched pile" scope of (а)–(е), the function-list carrier
of (б) and the `status` refusals are data checks (presence, joins, order of status words). They are code-owned, in the
forge's `tools/`, and outside the package judgment census (`judgment-census.json` covers `scripts/*.py` only). Between
DIFFERENT developers a waiting node holds its zone, as today: the owner's word 13.11.2026 («Это верно для двух
разработчиков»), F-D1 (3). (t-367 B1)

### 1.1 Owner-facing plan (PROJECT.md «новая идея», step 4) (t-367 N1)

Коротко, для владельца, до билдеров:
- Доски `plans/PILES.md` больше нет: удаляются её код, её проверки в хуках и CI и сам файл. Открытые пачки видны в панели «Бэклог».
- Скрипт `piles.py` не переписываем, а облегчаем: убираем доску, сужаем проверку, добавляем команду `status` (ответ на «Может его переписать?»).
- Меняется договорённость команды (D-0036, D-0044): коммит блокируют только красные строки тех кучек, которые он трогает. Остальные печатаются одной строкой «не блокирует», а ловит их еженедельная калибровка (проверка 33 (a)).
- Между разными разработчиками ожидающий узел держит свою зону, как сейчас (ваши слова 13.11.2026). Две пачки одного разработчика друг друга не держат.
- Вопрос вам (Q-O1): «одну сессию» мы читаем как «одного разработчика» (все сессии и клоны dev1): другой метки сессии в пачке нет. Подтвердите или скажите иначе; до ответа работаем так.

---

## 2. Inventory of readers and writers of the board (part A)

Control greps. All are case-insensitive, run with the Grep tool on read-main.
- `PILES\.md|BOARD_REL|board --check|piles board|piles\.py board`: 238 hits in 101 files.
- Positive control, same call: it finds `tools/piles.py:104 BOARD_REL = "plans/PILES.md"` and `.githooks/pre-commit:40`.
- Symbols: `render_board|rebuild_board|board_table|toc_lines|_count_line|_incoming|untracked_warning|unreadable_warning|board_triggers|cmd_board|BOARD_HEAD|_board_cells|_open_sets|_toc_text|_prio_rank|BOARD_REL|"board"`
  over `tools/*.py`. Hits are only in piles.py, piles_testkit.py and the tests listed in §5. The other reader,
  compact_snapshot.py:377, reads `leftovers_unowned`, which stays.
- False positives, kept on purpose: `ai-packages/qa-factory/scripts/onboard_apply.py:108,931,1030,1031`,
  `scripts/tests/test_install_retire.py:146,893,894`, `test_reinstall_equals_fresh.py:607` and `test_two_folders.py:93`.
  The case-insensitive pattern matched `DASHBOARD_REL` in them (the package's dashboard). Verdict: not a reader, untouched.
- The review's own grep (t-367 P3, `board-check` added) found two more lines, listed in §2.1 (t-367 N7).

### 2.1 Code and gates

| Carrier (line) | What it does with the board | Verdict |
|---|---|---|
| `tools/piles.py:1-74` docstring (lines 1, 4, 7, 19, 33-40, 58) | describes the board, the `board` usage line, its exit code and its rebuild by take/close | reworded: the board sentences go. Line 33 "The readers (board, check, …)" becomes "(check, forge_metrics, compact_snapshot, backlog_tree)". Lines 37-39 become: «The status of a batch lives in the batch header (with the card row); `take`/`status`/`close` are its one code writer». Line 58 «(the board count line, the compact snapshot)» becomes «(`piles.py summary`, the compact snapshot)» |
| `piles.py:104` `BOARD_REL` | the path | removed |
| `piles.py:908-1121`: `_esc`, `_shown`, `_same_status`, `_same_branch`, `_incoming`, `_board_cells`, `_prio_rank`, `board_table`, `_toc_text`, `toc_lines`, `BOARD_HEAD`, `render_board`, `untracked_warning`, `unreadable_warning`, `board_triggers`, `cmd_board` | build, write and check the board | removed. Exceptions: `write_atomic` / `write_bytes_atomic` (1065-1080) stay, because `write_like` and `apply_changes` use them. `_open_sets` and the id computation (`ids`, `open_ids`, `live`) that `_count_line` reads (985-1062) STAY for `summary` (F-1 (a)); `toc_lines` is split: the id computation it shares with `_count_line` stays beside `_count_line`, its table-of-contents text goes (t-367 N2). `_count_line` moves to `summary`, text unchanged. `_print_all` (1123) goes when its only caller does (grep before removing) |
| `piles.py:2449-2452` `rebuild_board` | rebuilds after take/close | removed |
| `piles.py:3026-3053` `apply_changes` | adds `BOARD_REL` to the rollback set and calls `rebuild_board` | the board lines go. The all-or-nothing contract for `writes` + `deletions` stays unchanged |
| `piles.py:2504-2505` (take), `3123`, `3155` (close) | the printed `git add … plans/PILES.md` | `BOARD_REL` is dropped from the printed command |
| `piles.py:3183-3185` `_board_args`, `3217` `COMMANDS["board"]` | the subcommand | becomes a REFUSED ALIAS exactly like `release` (3168-3171, 3202-3203, 3219, 3227, 3241) (t-367 N9, Lead 13.11.2026): `_board_args` takes no arguments; `cmd_board` raises CannotRun (exit 1): «`board` was retired (the owner, 13.11.2026: there is no board) -- the open batches are shown by the «Бэклог» pane, or run `python -B tools/backlog_tree.py`; nothing was run». `build_parser` gives it no `--help` and `main` leaves its extra arguments unread, as for `release` (`board --check --if-staged` is refused the same way) |
| `.githooks/pre-commit:38-40` | `board --check --if-staged` | removed, comment included (the Lead places it in SL-5a, enforcement file) |
| `.githooks/pre-merge-commit:19-20` | `board --check` | removed (Lead, SL-5a) |
| `.github/workflows/forge-check.yml:81` | `board --check` step | removed (Lead, SL-5a). Step 85 `check --all --base "$BASE"` becomes `check --base "$BASE"` (F-2 (a), Lead 13.11.2026), placed by the Lead in SL-2's merge (§3 SL-2) |
| `tools/test_workflows.py:154` | pins the step | the row is removed in SL-1; row 155 changes to `check --base` in SL-2 (builder edits it, the Lead commits it with the workflow line) |
| `tools/test_workflows.py:8` docstring «without `board-check`» | history of the GitLab job `board-check`, not a reader of `piles.py board` | left as history (t-367 N7) |
| `.github/workflows/nightly.yml:12` comment «board-check is not ported: it mirrors piles to GitLab issues» | history of the GitLab job, not a reader | left as history (t-367 N7) |
| `.claude/settings.json:139,158` | allow-list `board --check` | both lines removed (Lead, SL-5a) |
| `.gitattributes:21` `plans/PILES.md text eol=lf` | eol rule for the file | removed (Lead, SL-5a) (t-367 B3a) |
| `tools/mechanism_gate.py:254` comment «(piles board/check, F0-2)» | comment | reworded to «(piles check, F0-2)» (Lead, SL-5a, mechanism file) |
| `tools/backlog_tree.py:1` | «plans/PILES.md stays the board» | reworded: «… for the «Бэклог» pane (a read-only view; the one view of the piles)» |
| `tools/collect_intake.py:846,877` | reads `piles.parse_zone` and `piles._norm_token` (not the board: a reader of the producer SL-4 changes, axis 12) | pinned by SL-4 D.6 (v); no change expected (t-367 B3d) |
| `tools/test_piles_form.py:58-73` `test_check_b_token_overlap_rules` | calls `tokens_overlap(a, b)` | stays valid (`tops` is a keyword argument); SL-4 adds its rows there (t-367 B3d) |
| `plans/PILES.md` | the generated file | deleted by the Lead in SL-5a, in the SL-1 integration commit (t-367 B3a) |

### 2.2 Texts

| Carrier (line) | Verdict |
|---|---|
| `PROJECT.md:280-281, 295, 319-320, 349-350` | reworded, before/after in §6.1 (net −111 bytes) |
| `AGENTS.md:295, 310, 335, 364` | generated from CLAUDE.md + imports (`tools/agents_md.py --check` in pre-commit/CI): regenerated in the same commit as PROJECT.md, never edited by hand |
| `README.md:10, 62` | reworded, §6.3 |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:978, 983, 1011` (check 33) and `:1083` (check 39, «the board's count line») | reworded, §6.2 |
| `docs/SIBLING_MAP.md:288, 294, 296, 298, 300, 304, 307-309` (axis 12) | reworded, §6.4 |
| `plans/BACKLOG.md:7` (header pointer «оглавления — `plans/PILES.md` (генерируется …)») | reworded. The substring "`plans/PILES.md` (генерируется `python tools/piles.py board`)" becomes "`plans/piles/` (карточки, пачки, находки)". It is header prose, not a row: (г) compares rows and the lock line only (`_g_after_freeze`, piles.py:1803-1825), so the freeze holds |
| 33 pile cards + `plans/piles/_template/README.md:42,53` | one mechanical rule, §6.5 |
| batch files (`kb/1:45,71`, `live-runs/1:29`, `driver-controller/1:31`, `package-ci/1:32`, `cost-dashboard/1:30`, `onboarding-hooks/1:29`, `gates-and-words/1:29`, `stand-and-sources/1:27`, `roles-context/1:27`, `execution-probes/1:29, 2:49`, `report-delivery/1:33`, `regression/1:24`, `forge/1:5,26,27`, `forge/6:45`, `codex/1:52`, `hotfix-12586/2:439`) | every one of them is «закрыта» (header grep, §9): history, NOT edited |
| `onboarding-forge/batch-1…:57` | «в работе», so taken and frozen by (в). History, NOT edited |
| findings (`forge/findings/20261013-take-i-close…`, `forge/findings/20261015-odin-chitatel…`, `onboarding-forge/findings/20261021-…`, `20261026-…`) | history of closed work, NOT edited |
| `docs/DECISIONS_ARCHIVE.md:52, 64, 127, 142` (D-0036, D-0044) | append-only history, NOT edited. The Lead appends one new entry (§6.6). `DECISIONS.md` has no hit: the same grep found nothing there, while the control above found its own hits (re-checked by t-367 P5) |
| `docs/PROJECT_FULL.md:331, 348, 372, 405`, `docs/CLAUDE_HOST_ADAPTATIONS_FULL.md:45, 51`, `plans/team/team-work-plan.md` (12), `experiments/mybooks/thinking-roles/thinking-roles.md:155` | history snapshots, NOT edited |
| `docs/tasks/specs/**`, `docs/tasks/compact-snapshots/**`, `logs/journal/dev1.jsonl` (12) | history / append-only, NOT edited |

### 2.3 Numbers the board carried, and who reads them now

| Number (the producer today) | Reader today | Verdict |
|---|---|---|
| board table: per batch status / who / branch / MR (`board_table`) | people and scouts (journal t-338: "checked on PILES.md (all 10 are dev1)") | replaced by `tools/backlog_tree.py`, which already carries `status`, `who` and `prio` per open batch |
| «Входящие» per pile (`_incoming`) | D-0044 detector, calibration 33 | dropped. The detector is (е) itself (`check --all`); check 33 (d′) already reads it |
| B-id table of contents (`toc_lines`, its text) | lookup "where does B-nnn live" | dropped (a lookup, not a number). A person or agent uses `grep -rn "B-nnn" plans/` |
| count line: piles, batches per status, open ids split, ids without a finding, closed | the integrator via «следующий свободный B-id» | kept, printed by `piles.py summary` (F-1 (a), Lead 13.11.2026) |
| «следующий свободный B-id» | the integrator (`plans/BACKLOG.md:24`, `_template/finding.md:13`) | `piles.py summary` (F-1 (a)) |
| «остатков без исполнителя» (`leftovers_unowned`) | `compact_snapshot.findings_summary` (compact_snapshot.py:377), calibration 39 | stays with that producer (and in the `summary` line). Check 39 is reworded |
| «не-id в строках» | nobody found | stays in the `summary` line, unchanged (it is part of `_count_line`) |

The backlog pane keeps working: `tools/test_backlog_tree.py` (all four tests) is untouched and must be green in every node's
witness. It runs `backlog_tree.tree(ROOT)` on the real tree, which is the pane's only data path.

---

## 3. The nodes, written for a weaker model

Order (all four code nodes write `tools/piles.py`, so they run in a QUEUE, never in parallel): **SL-1 → SL-4 → SL-2 → SL-3**.
SL-4 goes before SL-2 because it lifts today's `take` refusals. SL-6 (cards) can run in parallel with any of them (disjoint
owns: no code node owns a card file). SL-5 is the Lead's mechanism commit(s).

Integration branch (t-367 B3a, Lead 13.11.2026): every node branch merges into `pile/forge/batch-8` (from `origin/main`,
PROJECT.md «Командная работа» p. 1); "the tree between nodes" means that branch, never `main`. The batch reaches `main` by
one PR at the end. See also the question L-1 (end of the spec) about where the hooks run.

Owns, re-checked after the moves (no file is owned by two PARALLEL nodes):
- `tools/piles.py`: SL-1, SL-4, SL-2, SL-3, in that queue.
- `tools/test_piles.py`: SL-1, SL-4, SL-2 (queue). `tools/test_piles_take.py`: SL-1, SL-4, SL-2, SL-3 (queue).
- `tools/test_piles_form.py`: SL-4, SL-2 (queue). `tools/test_piles_findings.py`: SL-1, SL-2 (queue).
- `tools/test_workflows.py`: SL-1 (row 154), SL-2 (row 155) (queue); the workflow file itself: Lead (SL-5a line 81, SL-2
  merge line 85).
- `tools/collect_intake.py`, `tools/test_collect_intake.py`: SL-4 only.
- `.gitattributes`, `plans/PILES.md` (delete), hooks, settings, `tools/mechanism_gate.py`: Lead SL-5a only.
- Cards `plans/piles/*/README.md`, `_template/README.md`: SL-6 only (parallel; disjoint from every code node).

### SL-1 (A): remove the board from code and tests (builder → critic; the diff is over 100 lines, so a critic is due)

- given: this spec §2, `tools/piles.py`, `tools/piles_testkit.py`, `tools/conftest.py`, the test files in §5.1,
  `tools/backlog_tree.py`, `tools/test_backlog_tree.py`, `docs/TESTING.md`.
- owns: `C:\QAFactory\forge-repo\tools\piles.py`, `…\tools\piles_testkit.py`, `…\tools\test_piles.py`, `…\tools\test_piles_take.py`,
  `…\tools\test_piles_close.py`, `…\tools\test_piles_close_gate.py`, `…\tools\test_piles_findings.py`, `…\tools\test_md_table.py`,
  `…\tools\test_workflows.py`, `…\tools\backlog_tree.py`. (`plans/PILES.md` and `.gitattributes` moved to SL-5a: t-367 B3a.)
  Handed over as CONTENT, not written: `.githooks/pre-commit`, `.githooks/pre-merge-commit`, `.github/workflows/forge-check.yml`
  (line 81 only), `.claude/settings.json` (enforcement files: the Lead places them in the integration commit).
- Behaviour: everything in §2.1 is removed or reworded as listed.
  - `take` and `close` write the same files as before, minus the board.
  - `apply_changes` rolls back writes and deletions exactly as before. Its rollback set is the written and deleted paths
    only.
  - `piles.py board` (with any arguments) is a refused alias: exit 1, the text of §2.1 naming the «Бэклог» pane and
    `tools/backlog_tree.py` (t-367 N9).
  - `check` output is unchanged.
  - F-1 (a) (Lead 13.11.2026): a new read-only subcommand `summary` prints the old count line (`_count_line` moved,
    unchanged text, fed by the kept `_open_sets` and id computation, t-367 N2) to stdout, writes nothing and exits 0. It
    exits 1 when the tree cannot be read (CannotRun, as `check`).
- Temporal edge (t-367 B3a, Lead 13.11.2026): before the SL-1 integration the hooks call `board --check`; after it the
  subcommand is a refused alias (exit 1). The Lead integrates SL-1 into `pile/forge/batch-8` by this procedure, step by step:
  1. `git merge --no-commit --no-ff <SL-1 node branch>` (no commit yet, so the OLD `pre-merge-commit` does not run).
  2. Place the handed-over content: `.githooks/pre-commit` without lines 38-40, `.githooks/pre-merge-commit` without lines
     19-20, `.github/workflows/forge-check.yml` without line 81, `.claude/settings.json` without lines 139 and 158;
     `tools/mechanism_gate.py:254` comment reworded.
  3. `git rm plans/PILES.md`.
  4. Edit `.gitattributes`: line 21 removed.
  5. `git commit` with the axis block of SL-5a/SL-1 (§6.7) and the `tier:` line. pre-commit then runs the NEW hook.
  A plain `git merge` auto-commits through the OLD pre-merge-commit and is refused (exit 1). Open point: L-1 (end of the
  spec) — on re-check, the builder's own commits and the "NEW hook" of step 5 depend on which checkout the hooks run from.
- Tests: §5.1.
- DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for tools/piles.py tools/backlog_tree.py`
  (expected: "no scenario or keep row covers", which is a report line) plus
  `python -m pytest tools/test_piles.py tools/test_piles_take.py tools/test_piles_close.py tools/test_piles_close_gate.py tools/test_piles_findings.py tools/test_md_table.py tools/test_workflows.py tools/test_backlog_tree.py tools/test_compact_snapshot.py -q`,
  all green.
  - Key: `grep -rni "PILES.md\|BOARD_REL\|board --check" tools/*.py` prints only the history allow-list lines of §2.2.
    That means no `tools/*.py` line apart from the test fixture strings named in §5.1.
- non-goals: the check scope (SL-2), status (SL-3), zones (SL-4), every text outside `tools/`, `plans/PILES.md` and
  `.gitattributes` (SL-5a).
- siblings: axis 12 (Lead, SL-5). `tools/piles_split.py` was checked: it imports no board symbol (symbol grep above).
- Mechanism commit: yes. The SL-1 integration commit carries the hook / CI / settings changes, the delete and
  `.gitattributes`. The Lead commits it with the axis block of §6.7 (SL-5a/SL-1) and the `tier:` line.

### SL-4 (D): batches of one developer never block each other; the empty token (builder → critic)

- owns: `tools/piles.py` (functions: `+dev_of`, `+developer_vocabulary`, `+same_developer`, `check_overlap`, `_overlap_refusal`,
  `cmd_take`, `writers_of`, `fn_lists_of`, `_norm_token`, `tokens_overlap`, `_pair_overlap`, `parse_zone`), `tools/test_piles.py`,
  `tools/test_piles_take.py`, `tools/test_piles_form.py` (the (б) tests live there), `tools/test_collect_intake.py`,
  `tools/collect_intake.py` (no change expected; pinned) (t-367 B3d).
- B.0, the fact this node rests on: (б) pairs every batch whose status is in ACTIVE (`check_overlap`, piles.py:1586-1601) and
  `take` (`_overlap_refusal`, 2461-2469). Writers are every node not in NOT_WRITING (`writers_of`, 1403-1410), so a waiting
  node of a taken batch writes. Nothing compares the two takers today. The review's probe P1: 21 of 22 waiting batches with
  nodes are refused by `take` today (by github-move/3 or onboarding-forge/1); all 10 active batches are dev1's.
- D.1, reading "the same developer" (t-367 B4, Lead 13.11.2026):
  - `developer_vocabulary(root)` returns the set of developer slugs: the slugs of `git ls-files -z logs/journal` passed
    through `journal_keys.journal_names` (journal_keys.py:447; the index: in a commit the staged tree, in CI the checkout).
    An untracked journal file is not a slug until it is committed. The set is built once per run. If git cannot list the
    index, the set is empty.
  - `dev_of(who, vocab)`: drop the trailing date (`TAKEN_DATE_RE`). Cut the text into tokens `[a-z0-9][a-z0-9-]*` after
    `casefold()`. Keep the tokens that are in `vocab`. Return the slug when EXACTLY one distinct slug remains, else None.
  - `same_developer(b1, b2) = dev_of(b1.who) is not None and dev_of(b1.who) == dev_of(b2.who)`.
  - Error direction: `dev_of` may err only toward None, which means "different developers", today's rule. It never yields
    a wrong slug from the text. Adversarial inputs that must stay on that side:
    - `dev10` with vocab {dev1}: the token is dev10, so None.
    - `dev1-old`: the token is dev1-old, so None.
    - `dev1 → dev2 (передача)`: two slugs, so None.
    - `Ира` or `владелец (Lead)`: no slug token, so None.
    - `—` or empty: None.
    - `DEV1, 13.11.2026`: dev1 (case is folded).
    - `Lead dev1 (Opus), 13.11.2026`: dev1. The tokens lead and opus are not slugs.
    - A journal named `lead.jsonl` plus the text `Lead dev1`: two slugs, so None.
    - A journal file present on disk but not in the index (`logs/journal/dev2.jsonl` untracked): dev2 is not a slug, so
      `dev2, …` reads None.
    - Real values: `dev1, 05.11.2026` (github-move/3) and `dev1 (Opus coord), 12.11.2026` (onboarding-forge/1-4,
      onboarding-hooks/4,5,8) both read dev1.
  - The two false-"same" sources, named with their accepted risk (t-367 B4):
    - two people configured with one slug: read as one developer (accepted; detector: calibration check 33 (b″), §6.2,
      t-367 N6);
    - `--who <another's slug>`: read as that developer (accepted; writer-side guard: the D.3 WARNING; detector: 33 (b″)).
  - Invariant: a pair of batches of DIFFERENT developers, or with an unreadable taker on either side, is judged exactly as
    today. Same-developer never hides a red between two people whose slugs differ.
- D.2, (б) in `check`: `check_overlap` skips a pair when `same_developer`. The item's ok line gains "; N pair(s) of one
  developer not compared (<slug>: a/1 + b/2, …; inside one developer the only guard is `owns_gate`'s WARN over live
  dispatches of one machine; two parallel sessions of one developer are no longer blocked by (б))" (t-367 B2).
  - Such a pair needs no `очередь:`, no function list and no `piles-skip: б`.
  - Existing `очередь:` lines between the same developer's batches stay legal and are simply not needed.
- D.3, `take`: `_overlap_refusal` gets `dev_of(--who)` and skips a partner batch whose `dev_of(who)` equals it.
  - `take forge 8 --who dev1` passes when every overlapping active batch is dev1's.
  - It is refused as today when one overlapping batch is another developer's or has an unreadable taker. The refusal text
    is unchanged and names that batch.
  - `--who Ира` reads None: today's rule against every overlapping batch.
  - `take` prints a WARNING when `dev_of(--who)` differs from the clone's `journal_keys.developer_slug` (journal_keys.py:509)
    (t-367 B4): «piles take: WARNING: --who reads as developer <dev_of or "none">, but this clone's tools/dev.config.yaml
    names <slug> -- batches of one developer do not block each other, so --who decides whose batches this one may share
    files with; take it again with your own slug if this is not intended». A writer-side guard: it reads dev.config only at
    the writer, so the check side stays one road. It never refuses and never changes the exit code. When the clone's slug
    cannot be read (`developer_slug` returns None), nothing is printed.
- D.4, CI: the vocabulary comes from the git index, so a commit and CI read the same set for the same tree (t-367 B4). The
  check reads no `tools/dev.config.yaml`; only the D.3 WARNING at the writer does. F-D2 records the decision.
- D.5, waiting nodes between different developers: `writers_of` is unchanged (F-D1 (3), the owner's word 13.11.2026)
  (t-367 B1). A waiting node of a taken batch keeps its zone against another developer's batches.
- D.6, the empty token. What actually happens: `parse_writers` (545) takes every backtick span, and `BACKTICK_RE` needs at
  least one character. A cell `нет` (no backticks) or an empty cell therefore yields no token today. That is already
  pinned by `_node_reds` (1860-1872).
  - The empty token in the refusal `github-move/3 and forge/7 both write:  ~ changelog.d/` comes from GM3-2's cell
    `` `ai-packages/qa-factory/` `` (github-move/batch-3:30). `_norm_token` (1322-1324) strips the package prefix and
    leaves "".
  - Then in `tokens_overlap` (1395) the branch `"/" not in x and y.rsplit("/",1)[-1] == x` matches "" against the empty
    basename of every folder token. "" matches ONLY folder tokens, so a whole-package node does not collide with a literal
    file token today (a false green, review t-367 Key 1 #4).
  - So the overlap is real (the whole package does contain `changelog.d/`), but it is expressed as an empty string and
    matched by accident. This contradicts the brief, which assumed `нет` or an empty cell.
  - Fix:
    - (i) `_norm_token` maps the package root (`ai-packages/qa-factory` with or without `/`) to the constant
      `PACKAGE_ROOT = "ai-packages/qa-factory/"`, unchanged.
    - (ii) A token that is empty after `strip()` (a backtick span of spaces) is dropped by `writers_of` / `fn_lists_of`.
      It writes nothing.
    - (iii) `tokens_overlap(a, b, *, tops=None)` (`tops` is a keyword argument, t-367 B3d): `PACKAGE_ROOT` overlaps `y`
      when y starts with `PACKAGE_ROOT`, or y's first path segment is an entry of `root/ai-packages/qa-factory/` on disk
      (`tops`, read once per run by the callers in (б) and `take`). When `tops` is None (not passed, or not readable), it
      overlaps every y. That is the safe direction already declared in the function's docstring. An empty `a` or `b`
      overlaps nothing.
    - (iv) The refusal prints `ai-packages/qa-factory/ (the whole package)`, never an empty name.
    - (v) `parse_zone` keeps reporting the package root as an unreadable zone part (today's error text, «zone part `…`
      cannot be read … it matches nothing»): never a pattern in the un-normalised space. `collect_intake.py:877` normalises
      only resolved file paths, never the bare root, so it is unaffected. (t-367 B3d)
  - Invariant: a node that writes the whole package still collides with any package path of another developer's batch; a
    token never matches by an empty string; a card zone naming the package root stays a reported error, never a silent miss.
- Edges: §4 D.
- Tests: §5.4.
- DoD: `scenario_walk.py --witness-for tools/piles.py tools/collect_intake.py` plus
  `python -m pytest tools/test_piles.py tools/test_piles_take.py tools/test_piles_form.py tools/test_collect_intake.py -q`, green.
  - Key: a run of `take` on a copy of the real tree for one of the batches refused today (probe P1) shows a pass when its
    overlaps are dev1's only. Attach the command and its output.
- Mechanism commit: yes, it changes a gate's duty. The Lead commits it with the axis block of §6.7 (SL-4). PROJECT.md
  item 3 gains one clause (§6.1 (6), mandatory), written in SL-5b.

### SL-2 (B): a check judges only the piles the commit touches (builder → critic)

- owns: `tools/piles.py` (`Ctx.touches`, `+pile_of`, `+touched_piles`, `run_check`, `cmd_check`, `_relevant`, `load_tree`,
  `load_pile`, `check_placement`, `check_form`, `check_findings`, `check_frozen`, `check_overlap`, `_pair_overlap`,
  `_list_verdicts`, `_split_reds`, `_item_lines`, `cmd_take`, `+range_paths`), `tools/test_piles.py` (gate semantics),
  `tools/test_piles_findings.py`, `tools/test_piles_placement.py`, `tools/test_piles_form.py`, `tools/test_piles_door.py`,
  `tools/test_piles_frozen.py`, `tools/test_piles_take.py`, `tools/test_workflows.py` (row 155).
  Handed over as CONTENT: `.github/workflows/forge-check.yml` line 85 (the Lead places it in SL-2's integration commit).
- B.0, why a foreign untracked pile went red:
  - `load_tree` (853-864) walks the FOLDERS on disk, so an untracked pile is read like a tracked one.
  - Two red classes carry the wildcard `CARDS_AND_FINDINGS` (1169, `Ctx.touches` 1201-1203): (а) a9 «open id placed
    nowhere» (1311-1313) and (д)'s unreadable-finding red (2040-2042). Any staged card, finding, batch file or BACKLOG.md
    then carries them.
  - Every other red is per-path, and still reaches a commit through cross-pile carriers: (е) homes via `перенос:`, (б)
    pairs.
  - The result is a red caused wholly by another session's files on any commit that touches any pile.
- B.1, the set of touched paths:
  - In a commit (`--msg-file`, the commit-msg hook): `staged_paths(root)`, as today (adds, changes, deletions; renames
    split by `--no-renames`, so a renamed batch counts both old and new paths).
  - In CI with `--base REV` and no `--all`: `range_paths(root, REV)`, which is
    `git diff --name-only --no-renames -z REV HEAD`. It is CannotRun (exit 1) when git fails, never "nothing touched".
  - With `--all`: None, meaning everything blocks.
  - `touched_piles = {pile_of(p)}` over those paths, where `pile_of("plans/piles/<slug>/…") = slug` (`_` and `.` folders
    excluded, as `_is_pile_dir`). `backlog_touched = BACKLOG_REL in paths`.
- B.2, untracked files: in a commit (not `--all`, not `--base`), `load_tree(root, tolerant=True, skip=set(untracked_piles(root)))`.
  - `load_pile` skips every path in `skip`.
  - A folder whose `README.md` and all files are skipped is not a pile at all: it is absent from `tree.piles`.
  - `--base` (CI) and `--all` read the tree as is. CI has no untracked files.
  - `--all` on a developer machine shows untracked piles too, plus one note line naming them.
  - The check reads the WORKING TREE, not the index: unstaged edits of a tracked file of a touched pile are judged as part
    of the commit, either way (pre-existing; this node does not change it) (t-367 N4).
- B.3, the decision rule replacing `Ctx.touches`: a red blocks when `staged is None` (`--all`), or when one of its carriers
  is a touched path or lies in a touched pile, or is `BACKLOG_REL` while `backlog_touched`. The wildcard
  `CARDS_AND_FINDINGS` is deleted; its two users get real carriers:
  - (а) a9: `(BACKLOG_REL,)` + the paths of the piles that named the id at the base rev (F-3 (a), Lead 13.11.2026). The base
    rev is HEAD in a commit, REV with `--base`.
  - (д) unreadable finding: `(f.path,)`, which is its pile.
  - (е): `_staged_batches(ctx, homes)` gets `homes = {slug} | set(_finding_moves(f))`, with no `in tree.piles` filter. A
    `git rm` of a whole pile that a `перенос:` named then still carries the red it causes.
  - (б) function-list verdicts read the named `.py` (`defined_names`, 1450; used by `_list_verdicts`, 1503-1529). A code
    commit that removes or renames a listed name creates a red with no pile path. Carrier = (b1.path, b2.path, the `.py`):
    every red `_list_verdicts` returns for file `x` carries `x` as its third path; the other (б) reds keep (b1.path, b2.path).
    In a commit, the check runs when a staged path is a `.py` named in an active batch's function list: `_relevant`
    (2233-2234) is extended — no pile or BACKLOG path staged, but some staged `.py` path → load the tree (as B.2) and run
    when that path equals a function-list file of an active batch (`fn_lists_of`, normalised by `_norm_token`). In CI
    `--base`, the range's paths are carriers too (B.1), so a pushed range that touches the `.py` blocks. (t-367 B3c, Lead
    13.11.2026)
  - Invariant (what stays unreachable): a red this commit CREATES always has a carrier in a pile it touches, in BACKLOG.md,
    or (for a (б) function-list verdict) in the `.py` it stages. To create a red you must change a file of that pile, the
    other pile of a pair, BACKLOG, or a listed `.py`. Each red class is enumerated in §4 B.
- B.4, per item:
  - (а) placement: judged on the whole tree. It blocks by B.3. Cross-pile reds (one id in two piles) block when any home
    pile is touched.
  - (б) overlap: a pair blocks when either batch's pile is touched (after SL-4's same-developer skip), or, for a
    function-list verdict, when its `.py` is touched.
  - (в) frozen: compares only taken batches of touched piles with origin/main (or `--base`). Pairs in untouched piles are
    not read: same verdict, less git.
  - (г) backlog: unchanged (runs when BACKLOG.md is touched).
  - (д) form: per-pile reds block when their pile is touched. `_leftover_write_reds` compares only batches of touched piles.
  - (е) findings: trigger unchanged (a finding or batch file touched). A red blocks by B.3.
  - A commit that edits pile X is judged on ALL of X. This is broader than today, where a red in X's card did not block a
    commit staging only X's batch-3.
- B.5, output: reds outside the touched piles are no longer printed one per line. One line per item:
  `(<l>) <key>: N red(s) in piles this commit does not touch (not blocking): <slug>, <slug>` (first 5 slugs, `+K more`).
  "Nothing touched" stays `piles check: no plans/piles or BACKLOG path staged -- nothing to check` (exit 0). Its reader is
  calibration check 33 (a) (§6.2), not the committer.
- B.6, `--all` afterwards: the full audit, where every red blocks. Its user is calibration check 33 (a) on origin/main, the
  ONE named reader of reds in untouched piles (F-2 (a), Lead 13.11.2026; no audit step in CI) (t-367 N3).
- B.7, doors: `piles-skip:` keeps its meaning. For a red in a touched pile it is still needed and still read from the message
  (commit) or the range's messages (`--base`).
- B.8, CI step (F-2 (a), Lead 13.11.2026): `forge-check.yml:85` `check --all --base "$BASE"` becomes `check --base "$BASE"`;
  `tools/test_workflows.py:155` pins the new line. Temporal edge: before SL-2, `check --base` without `--all` reads the
  STAGED paths (none in CI) and prints "nothing to check"; so the line changes in SL-2's integration commit, together with
  `range_paths`, never earlier.
- B.9, `take` reads like `check` (t-367 N4, Lead 13.11.2026): `cmd_take` (2472-2478) stops using the strict
  `load_tree(root)`; it calls `load_tree(root, skip=<untracked_piles(root) outside plans/piles/<slug>/>)`. Untracked files of
  OTHER piles are skipped (the same rule as check B.2), so a foreign session's untracked broken or active batch neither makes
  `take` CannotRun nor refuses it. Everything read stays strict (a writer must not act on a tree it could not read whole,
  `load_pile`'s docstring 813-816), and the pile being taken is read with its untracked files, as today.
  - Invariant: what `take` refuses on TRACKED data, and on the pile it writes, stays refused; an uncommitted foreign batch
    has no claim on a zone.
- Edges: §4 B.
- Tests: §5.2.
- DoD: `scenario_walk.py --witness-for tools/piles.py` plus `python -m pytest tools/test_piles.py tools/test_piles_findings.py tools/test_piles_placement.py tools/test_piles_form.py tools/test_piles_door.py tools/test_piles_frozen.py tools/test_piles_take.py tools/test_workflows.py -q`,
  green. Key: `tools/hook_liveness_probe.py` case 14 still refuses with the anchors at 1370 (it runs `--all`).
- Mechanism commit: yes (a gate's scope). The Lead commits it with the CI line 85 and the axis block of §6.7 (SL-2).

### SL-3 (C): `piles.py status`, the one writer of «сдано»/«принято» (node F6-13) (builder → critic)

- owns: `tools/piles.py` (`+cmd_status`, `+_status_args`, `+set_node_cell`, `STATUS_ORDER`, `COMMANDS`, docstring usage line),
  `tools/test_piles_take.py`.
- Usage:
  - `python tools/piles.py status <slug> <N> --set <сдано|принято>` writes the batch header `статус:` and the card row's
    Статус cell.
  - `python tools/piles.py status <slug> <N> <node-id> --set <в работе|сдано|принято|отклонено> [--hash <h>] [--task t-NNN]`
    writes one node row's Статус cell.
  - `--today` is hidden, as in take.
- The node cell written:
  - `в работе`, `сдано` and `отклонено` are written as the bare word.
  - `принято` with both values gives `принято: <hash> (t-NNN)`, the form the brief names.
  - Hash only gives `принято: <hash>`. Task only gives `принято (t-NNN)`.
  - `--hash` goes through `check_hash` (7-40 hex characters and a commit here). `--task` must match `t-\d{1,6}`.
- Batch level: only `сдано`/`принято`. `в работе` belongs to take and `закрыта` to close, and the refusal says so.
- Writes go through `apply_changes` (all or nothing; after SL-1, no board). The file form (CRLF, BOM) is kept by `write_like`.
- Legal in a taken batch: (в) masks the header статус, the card Статус and the Статус cells (`_frozen_lines` 1676-1690,
  `_compare_card` 1731-1741).
  - Invariant: the command never writes a cell (в) does not mask. Pin: after each write, `check --all --base HEAD` on the
    fixture shows (в) green.
- Edges, with what each protects:
  1. Unknown slug, N or node id: Refused (exit 2). It names the batch's node ids (first 10, `+K more`) and writes nothing.
     Invariant: no status reaches a row it was not named for.
  2. A node row whose Узел cell names two ids (`C1-4a + C1-4b`, split on `,`, `+`, `/` or whitespace), or two rows with the
     same id: Refused. The text says "one row, one id; split the row in an untaken batch, or write the cell by hand (the
     cell is masked by (в))". Invariant: the command never moves the status of an id it was not given.
  3. A status going backwards: Refused, naming the current cell and the hand-edit door. The order is the ONE existing table
     `STATUS_ORDER` (piles.py:108), extended with `отклонено`: it is built over `NODE_STATUSES` (107) instead of
     `BATCH_STATUSES`, so `отклонено` gets the last index and the batch uses at 1704, 1738, 1936 are unchanged (a batch
     status never holds `отклонено`). No second order table (t-367 N8). Finality: a cell in `NOT_WRITING` (110: `принято`,
     `отклонено`) is final, so `принято` → `отклонено` is Refused too. The same status again is "nothing changed", exit 0.
     `принято` again with a different hash or task is Refused ("already accepted with …").
  4. Node `принято` with neither `--hash` nor `--task`: Refused ("expected --hash <merge commit> and/or --task t-NNN").
     Invariant: no `принято` without evidence through the command.
  5. Batch `принято` while a node is neither принято nor отклонено: Refused, naming those nodes. Batch `сдано` has no node
     condition (closed choice: work handed over may still have nodes waiting for review). Invariant: the header never says
     accepted while a node is open; `close` then reads a batch whose nodes are done.
  6. Batch not taken (header «ожидает» or no status): batch-level Refused ("take it first"). Node level is allowed in any
     batch that is not «закрыта". The data has accepted nodes in an untaken batch: forge/7 FG7-4, FG7-8, FG7-9.
  7. Batch «закрыта»: Refused at both levels.
  8. Card row and batch header disagree: batch level Refused, as take (2493-2495).
  9. No node table, or a missing Статус column: Refused with `_parse_nodes`'s text.
  10. A batch file whose name or number changed (renamed): the view is found by N as in take. Two files with one N: Refused
      (`_batch_file`).
  11. A missing card README: Refused (`_find_view`).
- `status --set "в работе"` on a node runs no overlap check: a waiting node already holds its zone (F-D1 (3)), so the flip
  changes no zone.
- Prints the next step: `git add <files>; git commit -m "piles: status <slug>/<N>[ <id>] <word>"`.
- After the merge: the Lead sets F6-13 (onboarding-forge/2) through the new command, `--set принято --hash <h> --task <t>`
  (the first live use), and closes its finding's pointer.
- Tests: §5.3.
- DoD: `scenario_walk.py --witness-for tools/piles.py` plus `python -m pytest tools/test_piles_take.py -q`, green.
- Mechanism commit: yes (a new writer of a registry status). The Lead commits it with the axis block of §6.7 (SL-3);
  detector: calibration check 33 (d) (t-367 N6).

### SL-5 (Lead): mechanism commits

- SL-5a, the SL-1 integration commit into `pile/forge/batch-8` (procedure in §3 SL-1, t-367 B3a): `.githooks/pre-commit:38-40`
  and `.githooks/pre-merge-commit:19-20` removed, `forge-check.yml:81` removed, `settings.json:139,158` removed,
  `mechanism_gate.py:254` comment, `git rm plans/PILES.md`, `.gitattributes:21` removed.
- SL-2's integration commit: `forge-check.yml:85` → `check --base "$BASE"` (F-2 (a)), with SL-2's code.
- SL-5b, after SL-3:
  - `PROJECT.md` (§6.1, edits (1)-(6), (6) mandatory) and `python tools/agents_md.py` (regenerate AGENTS.md).
  - `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` checks 33 and 39 (§6.2).
  - `docs/SIBLING_MAP.md` axis 12 (§6.4) and axis 13's guard wording (§6.4, t-367 B2).
  - `README.md` (§6.3), `plans/BACKLOG.md:7` (§2.2), the DECISIONS_ARCHIVE entry (§6.6).
- Each mechanism commit carries the four questions, ITS axis block against the CURRENT 36 axes (§6.7: one block per commit,
  SL-5a/SL-1, SL-4, SL-2, SL-3, SL-5b) and a `tier:` line (t-367 N6).
- SL-5b changes meaning (PROJECT.md p. 7, the detector of D-0044, check 33), so PROJECT.md «Как принимается изменение
  пакета» item 6 applies: critic on plan of THIS spec before builders (done: review t-367).

### SL-6 (builder, doc node): card boilerplate

- owns: `plans/piles/*/README.md` (the 33 cards named by the grep in §9) and `plans/piles/_template/README.md`.
- Behaviour: the replacement rule of §6.5, nothing else.
- DoD: a key-presence run per CLAUDE.md rule 11 DOC-DISPATCH WITNESS, with keys quoted from §6.5:
  - after the run, `grep -rn "plans/PILES.md" plans/piles/*/README.md plans/piles/_template/README.md` prints only
    `onboarding-forge/README.md:87` (a history row of «Содержание»);
  - every card still contains its `## Содержание` heading;
  - a negative control (one card restored to the old line, so the script reports it).
  - Plus `python -m pytest tools/test_pile_cards_contents.py -q`, green.
- Freeze: (в) compares a taken batch's card ROW only (`_compare_card`). «Содержание» and «Входящие» prose of a card is not
  frozen. No batch file is edited (§6.5).
- Mechanism commit: no ("axes: not a mechanism (wording of pile cards)").

---

## 4. Edges

A (board):
- `piles.py board` after SL-1: exit 1, the refused-alias text naming the «Бэклог» pane and `tools/backlog_tree.py` (t-367
  N9). Hooks are fixed in the same integration commit (temporal edge, SL-1; open point L-1).
- A clone at an older commit runs its own old hooks. After a pull, the hook files and piles.py come from one commit, so they
  stay one generation.
- `plans/PILES.md` still present in a stale branch: after a merge, git resolves it as a delete/modify conflict. The
  resolution is delete, and nothing reads it.
- `apply_changes` failing midway: every written and deleted path is put back. Pin: `test_close_batch_that_fails_midway_puts_every_file_back`
  and `test_take_that_fails_after_the_card_write_puts_both_files_back` (their "board" step params die, the "write"/"batch"
  params stay).
- `piles.py summary` on an unreadable tree: exit 1 (CannotRun); on an empty tree: the count line with zeros, exit 0.

B (scope). For every red class, its carrier and the invariant that it is still red when the commit creates it:
- (а) dupes, unknown id, closed-but-placed, card/batch id mismatch, finding header vs folder: the carriers are the paths
  involved. Creating one means editing one of them.
- (а) a9 «placed nowhere»: F-3 (a). Created by deleting a finding, removing a member or closing a batch in pile X, which is
  touched at the base lookup.
- (б) pairs: both batch files. Created by editing either.
- (б) function-list verdicts (t-367 B3c): (b1.path, b2.path, the `.py`). Created by a code commit that removes or renames a
  listed name, or deletes the `.py` (then `defined_names` cannot read it: red, carrier the deleted path, which is staged).
  - A staged `.py` named in no active batch's function list: `_relevant` stays false, "nothing to check", exit 0.
  - A staged `.py` named only by a waiting or closed batch: not relevant (only active pairs are judged).
  - The same-developer pair: skipped by SL-4, so no function-list red arises between one developer's batches.
  - The tree cannot be loaded while `_relevant` looks for function lists: the check runs (safe side) and its own
    CannotRun names the failure, as today for a pile commit.
  - Cost: a code commit staging a `.py` and no pile path loads the tree once (tolerant, untracked skipped).
- (в): the taken batch and its card. Created by editing them.
- (г): BACKLOG.
- (д) all: own pile. The unreadable finding is its own path.
- (е): the finding + home piles' batches + staged deleted batches of named piles (B.3).
- Empty touched set: "nothing to check", exit 0.
- Only BACKLOG.md touched: (г) runs; a9 blocks (BACKLOG is its carrier); per-pile reds are only counted.
- A pile with no batches: card reds only.
- A whole untracked pile: invisible in a commit, visible in `--all`.
- A pile that is partly untracked (its new finding not yet added): the finding is invisible in a commit. The commit does not
  contain it, so it cannot be judged as part of it.
- Unstaged edits of a tracked file in a touched pile: judged with the commit (working tree read; pre-existing, t-367 N4).
- A renamed batch: both paths are touched, the pile is touched.
- A pile folder deleted in the commit: the deleted paths map to the slug. Reds of other piles that name it carry via B.3.
- `--base` with an empty range: nothing touched, exit 0 (one line). An unreadable range: exit 1.
- `range_paths` with a REV that does not resolve: the existing `--base` CannotRun (cmd_check 2322-2327).
- `take` with an untracked broken or active batch in ANOTHER pile: skipped, take runs on the tracked tree (B.9).
- `take` with an untracked broken file in the pile being taken: CannotRun, as today.
- `take` when `git ls-files --others` fails (`untracked_piles` returns []): everything is read, today's behaviour.

C (status): §3 SL-3 edges 1-11.

D (zones):
- Unreadable taker: different (today's rule).
- No journal folder in the index (tmp trees): the vocabulary is empty, so different everywhere, which is today's behaviour.
  The test fixture commits `logs/journal/dev1.jsonl` where a test needs the same-developer rule.
- git cannot list the index: empty vocabulary, different everywhere (safe).
- An untracked journal file (a new developer's first `journal_created` not committed yet): not a slug, so "different" in the
  commit and in CI alike (t-367 B4).
- `take --who` with a slug that has no committed journal yet (a new developer): None, today's rule. The first committed
  journal line lifts it.
- Two people configured with one slug: read as one developer; accepted risk, detector 33 (b″) (t-367 B4, N6).
- `take --who <another's slug>`: read as that developer; the D.3 WARNING prints when it differs from the clone's slug.
- The clone's `tools/dev.config.yaml` unreadable at `take`: no WARNING, take unchanged.
- Waiting nodes of a taken batch between different developers: hold their zone (F-D1 (3)).
- The package root token without `ai-packages/qa-factory/` on disk (`tops` None): overlaps everything (safe).
- A backtick span of spaces: no token. An empty token overlaps nothing.
- A card zone `` `ai-packages/qa-factory/` ``: `parse_zone` reports it as unreadable, as today (D.6 (v)).

---

## 5. Tests (no new test file; every new case is a parameter row or a case in an existing file, `docs/TESTING.md`)

### 5.1 SL-1: die with the board / change

- Die (`tools/test_piles.py`): `test_board_writes_when_absent_and_check_reports_missing`, `test_board_check_stale_then_fresh`,
  `test_board_toc_lists_every_id_form`, `test_board_closed_hash_forms`, `test_board_contradiction_open_and_closed`,
  `test_board_unassigned_finding_counted_not_listed`, `test_board_deterministic_no_clock`,
  `test_board_table_rows_order_and_pile_without_batches`, `test_board_card_and_batch_disagreement_shown`,
  `test_board_branch_compared_by_first_token`, `test_board_skips_template_and_hidden`, `test_board_empty_node_table_is_shown`,
  `test_board_duplicate_batch_numbers_both_shown`, `test_board_crlf_piles_md_not_stale`,
  `test_board_same_for_crlf_and_bom_backlog`, `test_board_if_staged_skips_unless_piles_path_staged`,
  `test_board_warns_on_untracked_pile_files`.
- Change (`test_piles.py`):
  - `test_board_pile_folder_without_readme`: keep only the `check --all` half and rename it
    `test_pile_folder_without_readme_is_red_in_check`.
  - `test_board_refusals_exit_1`: the loop keeps `("check","--all")`. Add the rows `("board",)` and
    `("board","--check","--if-staged")`, which expect exit 1 with the refused-alias text naming `backlog_tree.py`
    (t-367 N9), and rename it `test_refusals_exit_1`.
  - `test_cli_end_to_end_subprocess`: drop the board half.
- `test_piles_findings.py`:
  - Die: `test_board_exits_zero_lists_every_readable_finding_and_warns_about_the_other`,
    `test_board_check_is_up_to_date_with_the_warning_and_exit_zero`,
    `test_board_without_an_unreadable_finding_prints_no_warning`.
  - Change: `test_the_board_incoming_count_and_the_e_count_come_from_one_predicate` and
    `test_e_f4_the_board_counter_is_the_orphan_count_of_e_baseline_included` both pin `_incoming`. They die, because (е)
    itself is the one predicate and the helper at line 310 goes too.
- `test_piles_close_gate.py`:
  - `test_close_batch_that_fails_midway_puts_every_file_back`: the param "board" dies, "write" stays.
  - `test_close_id_that_fails_midway_puts_the_row_and_the_finding_back`: its failing step was `rebuild_board`. It moves to
    a failing write (monkeypatch `write_like` on the second path).
  - `test_k14_the_board_count_line_names_the_unowned_leftovers_zero_included`: retargeted to `summary` (F-1 (a), Lead
    13.11.2026).
- `test_piles_take.py`:
  - `test_take_sets_card_and_batch_and_prints_commands` (47): drop the board assert and assert that `PILES.md` is not in
    the printed command.
  - `test_take_that_fails_after_the_card_write_puts_both_files_back`: param "board" dies.
  - `test_take_preserves_crlf_and_bom` (144): drop the board assert.
  - `test_take_writes_no_board_line_with_or_without_token` (186): simplify to "no `board`, `доска` or `PILES.md` in the
    output".
  - `test_take_runs_with_no_piles_gitlab_module` (197): drop `board --check`.
  - `test_take_that_fails_and_is_rolled_back_prints_no_board_word` (227): its failing step moves from `rebuild_board` to a
    failing write.
- `test_piles_close.py`:
  - `test_close_moves_archive_rows_with_hash_and_rebuilds_board` (39): rename it `…_with_hash`, drop the board assert, and
    assert the BACKLOG row directly.
  - `test_close_writes_no_board_line_with_or_without_token` (402) and `test_close_runs_with_no_piles_gitlab_module` (412):
    drop `board --check`.
- `test_md_table.py:178,190`: the param `("board",)` dies from both parametrizations.
- `piles_testkit.py`:
  - `board_text` (194-196) is deleted.
  - The fixture node `F0-2` writing `` `plans/PILES.md` `` (127) stays. It is a token in a cell, not the board.
    `test_piles_frozen.py:33,59` edit that cell and stay.
- `test_workflows.py:154`: the row is deleted. Row 155 changes in SL-2 (§5.2).
- Stays green untouched: `tools/test_backlog_tree.py`, which proves the pane.

### 5.2 SL-2: new rows

Rows in `test_piles.py` (gate semantics), one parametrized test `test_check_scope_touched_piles` with ids:
- `foreign-untracked-pile`: an untracked pile with an orphan finding and an unreadable finding. The commit stages a card of
  another pile. Exit 0, plus one "not blocking" line.
- `foreign-tracked-red`: a committed red in pile Y. The commit touches X. Exit 0.
- `own-pile-red-elsewhere-in-pile`: a red in X's card. The commit stages X's batch only. Exit 2 (broader than today).
- `a9-removal`: removing the only placement of an open id from X blocks.
- `a9-backlog-only`: a commit staging only BACKLOG with an a9 red blocks.
- `cross-pile-dupe`: an id in X and Y blocks a commit touching Y.
- `overlap-pair-one-side`: (б) pair X/Y of two developers. Touching Y blocks.
- `fn-list-code-commit`: two active batches of different developers with disjoint function lists on `tools/x.py`; a commit
  staging only `tools/x.py` that removes a listed name blocks, and the red names `tools/x.py` (t-367 B3c).
- `fn-list-py-not-listed`: a commit staging only a `.py` no active list names: "nothing to check", exit 0.
- `fn-list-range`: `--base REV` over a range whose only change is the listed `.py`: blocks.
- `renamed-batch`: both paths touched, so the pile is judged.
- `deleted-pile-move-line`: `git rm -r` of pile Z that a finding's `перенос: Z/…` names. Blocks.
- `range-mode`: `--base REV` without `--all` on a two-commit fixture. Only the range's piles are judged.
- `range-empty`: exit 0. `range-bad-rev`: exit 1.
- `all-mode-untracked-note`: `--all` blocks and names the untracked pile.

Rows in `test_piles_take.py`, one parametrized test `test_take_reads_untracked_like_check` (t-367 N4):
- `foreign-untracked-broken-batch`: an untracked batch with an unclosed fence in another pile; take passes.
- `foreign-untracked-active-overlap`: an untracked active batch of another developer in another pile writing the same file;
  take is not refused by it.
- `own-pile-untracked-broken`: an untracked broken file in the pile being taken; CannotRun (exit 1), as today.

`tools/test_workflows.py:155`: the pinned line becomes `check --base "$BASE"` (F-2 (a)).

Existing tests whose expectation flips:
- `test_a_staged_card_alone_is_blocked_by_an_unreadable_finding_elsewhere` (findings:167): now NOT blocked when "elsewhere"
  is another pile; still blocked in the same pile. It becomes two rows, renamed `…_blocked_only_in_its_own_pile`.
- Every test asserting "carried from earlier commits" text: the line form changes to B.5.

### 5.3 SL-3

One parametrized `test_status_edges` in `test_piles_take.py`, ids:
- `unknown-node`, `two-ids-row`, `duplicate-id-rows`, `backwards`, `accepted-then-rejected` (final, N8), `same-again`,
  `accepted-other-hash`;
- `accepted-no-evidence`, `accepted-hash`, `accepted-task`, `accepted-both`;
- `batch-accepted-open-node`, `batch-accepted-all-done`, `batch-submitted`;
- `batch-untaken`, `node-in-untaken-batch`, `closed-batch`, `card-disagrees`;
- `bad-hash`, `bad-task` (magnitude: `t-` + 7 digits; empty; `t-1|x`).

Plus `test_status_keeps_crlf_bom_and_passes_frozen` (the write, then `check --all --base HEAD`, (в) green) and
`test_status_rollback_on_failed_write`.

### 5.4 SL-4

- `test_dev_of` table (in `test_piles_form.py`, beside the (б) tests), ids: the adversarial list of D.1, plus `empty-vocab`,
  `untracked-journal-not-slug` and `git-fails-empty-vocab` (t-367 B4).
- One parametrized `test_check_b_pair_by_developer` in `test_piles_form.py`, rows:
  - `same-developer`: two batches of dev1 sharing `scripts/tests/`: exit 0 and the D.2 ok note (with the `owns_gate` wording);
  - `different-developer`: dev1 vs `Ира`: red as today;
  - `waiting-node-other-developer`: a waiting node of dev1's taken batch against dev2's batch on the same file: red, as
    today (F-D1 (3));
  - `two-clones-one-slug`: both takers `dev1`: read as one developer, not compared (pins the accepted risk of D.1).
- In `test_piles_take.py`, one parametrized test with rows `take-passes-own-overlaps`, `take-refused-other-developer` and
  `take-warns-who-differs-from-clone` (the WARNING of D.3, exit unchanged) and `take-no-warning-without-dev-config`.
- Rows added to the EXISTING table `test_check_b_token_overlap_rules` (`test_piles_form.py:58-73`; no second table,
  t-367 B3d). The table gains a fourth column `tops` (existing rows get the test constant
  `PKG_TOPS = ("scripts", "references", "changelog.d")`; the call passes `tops=` by keyword):
  - `("ai-packages/qa-factory/", "changelog.d/", PKG_TOPS, True)` (the whole package against a package folder);
  - `("ai-packages/qa-factory/", "tools/x.py", PKG_TOPS, False)` (`tools` is not a package top);
  - `("ai-packages/qa-factory/", "tools/x.py", None, True)` (no tops: the safe side);
  - `("ai-packages/qa-factory/", "scripts/x.py", PKG_TOPS, True)` (a literal file, the false green of today closed);
  - `("   ", "tools/", PKG_TOPS, False)` (a span of spaces is no token and overlaps nothing).
  - The refusal text "(the whole package)" is asserted in the `different-developer` style row of
    `test_check_b_pair_by_developer` with a whole-package cell.
  - `net-cell` is not a row: a cell without backticks never yields a token (`parse_writers`, D.6), which is not new.
- `tools/test_collect_intake.py::test_a_card_zone_is_read_by_parse_zone_only` (521) gains the row
  `` `ai-packages/qa-factory/` ``: one error, no pattern (D.6 (v), t-367 B3d).
- The status-time overlap test is deleted: a waiting node keeps its zone (F-D1 (3)), so no node owes it (t-367 B1, B3b).

---

## 6. Rule texts before / after

### 6.1 PROJECT.md (boot budget 117886/120000 bytes per the brief; all six edits together are net-negative)

Byte counts are hand-counted UTF-8 (Cyrillic 2 bytes, «» 2, — 3). The Lead verifies with a pure read before and after the
commit: `python -c "print(len(open('PROJECT.md','rb').read()))"`.

(1) Lines 280-281.
- Before: `находку). Единый носитель оглавления — \`plans/PILES.md\`, собирается кодом (\`python tools/piles.py board\`),` / `руками не правится. Правила:`
- After: `находку). Правила:`
- Delta: −174.

(2) Line 295.
- Before: `   \`piles.py check --all\` (д) и счётчик «Входящие» в \`plans/PILES.md\` против файлов пачек.`
- After: `   \`piles.py check\` (е), полный аудит — \`check --all\`.`
- Delta: −59.
- Closed choice: the letter (д) becomes (е). piles.py:59 names (е) «the D-0044 detector»; (д) holds the «Содержание» rows.

(3) Lines 319-320, item 7.
- Before: `7. **Доска GitLab выключена**: назначение пачек — «Взял» в карточке и шапке пачки, статус пачки — шапка и` / `   \`plans/PILES.md\`; \`take\`/\`close\` работают с файлами, без сети и токена.`
- After: `7. **Доски нет** (владелец, 13.11.2026): «Взял» и статус — в шапке пачки и строке карточки; пишут их` / `   \`take\`, \`status\`, \`close\` — файлы, без сети и токена.`
- Delta: −44. The text names `status`, so it lands only after SL-3 (temporal).

(4) Lines 349-350, the closing line.
- Before: `Проверка на пути исполнения: \`tools/piles.py check --msg-file\` в \`.githooks/commit-msg\`, \`board --check\` в` / `pre-commit, pre-merge-commit и CI \`forge-check\` (\`check --all\`); детектор — калибровочная проверка 33.`
- After: `Проверка на пути исполнения: \`tools/piles.py check --msg-file\` в \`.githooks/commit-msg\` и CI \`forge-check\`` / `(\`check --base\`); детектор — калибровочная проверка 33.`
- Delta: −48 (F-2 (a)).

(5) Item 8, appended (B).
- Before: `8. **Двери**: строка \`piles-skip: <пункт> -- <причина>\` в сообщении коммита; её частоту считает калибровка.`
- After: the same line + ` Проверка судит только кучки, которые коммит трогает.`
- Delta: +97.

(6) Item 3, for D — MANDATORY (t-367 §6.1 (6) bullet, Lead 13.11.2026: without it item 3 states a rule the code no longer
enforces): append ` Пачки одного разработчика друг друга не держат (владелец, 13.11.2026).` Delta: +117.
(Count: Пачки 10, одного 12, разработчика 24, друг 8, друга 10, не 4, держат 12, владелец 16, spaces 8, «(», «, 13.11.2026).»
13.) If the owner's answer to Q-O1 narrows the reading, the clause changes with it in the same commit.

Net: (1)-(6) = −111 bytes, net-negative. Item 2's text has no board word apart from line 295.

### 6.2 PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md

- Check 33, line 977-979, before: «Mechanism: `tools/piles.py check` in `.githooks/commit-msg` (door `piles-skip: <item> -- <reason>`), `board --check` in pre-commit, pre-merge-commit and CI forge-check, `piles.py close` …»
  After: «Mechanism: `tools/piles.py check` in `.githooks/commit-msg` (door `piles-skip: <item> -- <reason>`; a commit is judged on the piles it touches, and on a staged `.py` an active batch's function list names) and `check --base` in CI forge-check (the pushed range), `piles.py take`/`status`/`close` as the only code writers of a batch's status, `piles.py close` (formerly `release`, now a refused alias) as the only writer of «Закрыто», …»
- 982-985, before: «(a) `python tools/piles.py check --all` and `python tools/piles.py board --check` on `origin/main` — any red or stale line is a leak past the hooks (…)»
  After: «(a) `python tools/piles.py check --all` on `origin/main` — any red line is a leak past the hooks; (a) is THE named reader of reds in piles no commit touched (t-356 SL-2: such reds never block a commit, and CI judges only the pushed range; no CI step audits the whole tree) (…)» (t-367 N3)
- New (b′) after (b): «(b′) `piles-skip:` lines whose reason names another session's or pile's files — after t-356 SL-2 such a red cannot block, so each is a leak of the scope rule (a finding against `run_check`).»
- New (b″) after (b′), the detector of t-356 SL-4 (t-367 N6): «(b″) one-developer pairs: for every pair the (б) ok line of `check --all` on origin/main names as «of one developer», read the claimed slug's journal `logs/journal/<slug>.jsonl`: it must show that clone's work on BOTH batches (an event whose `node` or notes name each batch). A pair whose second batch has no trace in that journal is a false "same" — two people under one slug, or `take --who` with another's slug — and is a finding against `piles.dev_of`.»
- Check 33 (d) «card row Статус ahead of its batch file» stays as it is and is named the detector of `piles.py status` (t-356 SL-3) (t-367 N6).
- 1010-1011, before: «a batch's status now lives in the batch header and `plans/PILES.md` only, and (a)-(d) judge those;»
  After: «a batch's status lives in the batch header and the card row only (written by `take`/`status`/`close`), and (a)-(d) judge those;»
- Check 39, 1083, before: «the board's count line and the compact snapshot print «остатков без исполнителя: N».»
  After: «`piles.py summary` (its count line) and the compact snapshot print «остатков без исполнителя: N».» (F-1 (a))

### 6.3 README.md

- Line 10, before: «- `plans/PILES.md` — the list of what to do in the factory (generated from the piles); `plans/BACKLOG.md` is …»
  After: «- `plans/piles/` — the list of what to do in the factory (cards, batches, findings; the «Бэклог» pane shows the open batches via `tools/backlog_tree.py`); `plans/BACKLOG.md` is …»
- Line 62, before: «2. Open `plans/PILES.md` and pick a batch with status "ожидает" whose "стенд" you can satisfy»
  After: «2. Open the «Бэклог» pane (or run `python -B tools/backlog_tree.py`) and pick a batch with status "ожидает" whose "стенд" you can satisfy»

### 6.4 docs/SIBLING_MAP.md axes 12 and 13

- Title (288): «… piles <-> the frozen backlog <-> the generated board …» becomes «… piles <-> the frozen backlog <-> the backlog pane …».
- Row 294, «The one table of contents (generated)»: replaced by «The one view | `tools/backlog_tree.py` (reads `piles.load_tree`) ← the «Бэклог» pane `tools/claude-mods/backlog/hooks/register.tsx`; detector `tools/test_backlog_tree.py`».
- Row 296: «… lives in two places … the batch header `статус:` (with the card row) and `plans/PILES.md` — ONE writer for `в работе`/`закрыта` … `сдано`/`принято` are hand-written …» becomes «A batch's status lives in the batch header `статус:` (with the card row) — ONE writer per word: `take` (`в работе`), `status` (`сдано`/`принято`, and node cells), `close` (`закрыта`); files only, no network; an old `issue:` pair is masked in (в)».
- Row 298 (collect_intake): «ONE zone reader `piles.parse_zone`» gains «(the package root stays an unreadable zone part after t-356 SL-4 changed `_norm_token`; pin `test_collect_intake.py::test_a_card_zone_is_read_by_parse_zone_only`)» (t-367 B3d).
- Row 300: «(board WARNING, check (д) red …)» becomes «(check (д) red …)», and «halts board, check …» becomes «halts check …».
- Row 304 queued: the `_incoming` Q8 item is struck (the code is gone).
- New row: «Who a batch belongs to (t-356 SL-4) | `piles.dev_of` over the developer slugs = the names of `logs/journal/<slug>.jsonl` in the git index (`git ls-files` through `journal_keys.journal_names`); readers (б) `check_overlap`, `take`; errs only toward "different", except two people under one slug or `--who` with another's slug (accepted; detector check 33 (b″)); between different developers a waiting node holds its zone (the owner, 13.11.2026)».
- Paragraph 307-309: «the board is generated, never edited;» is deleted, and «the board's count «остатков без исполнителя»» becomes «`piles.py summary` and `compact_snapshot.findings_summary`».
- Axis 13 (t-367 B2): wherever this spec's work is cited as guarded inside one developer, the text names the real guard:
  «inside one developer the only guard is `owns_gate`'s WARN over live dispatches of one machine (`tools/owns_gate.py`);
  two parallel sessions of one developer are no longer blocked by (б)». No change to `dispatch_manifest`.

### 6.5 Cards and batches: one mechanical rule

Card files (`plans/piles/*/README.md`, `_template/README.md`), regex over the whole file, whitespace `\s+` between words
(the sentences wrap):
- R1: `При\s+расхождении\s+авторитетна\s+доска\s+` + "`plans/PILES.md`" + `\.` becomes «При расхождении авторитетны файлы пачек.»
  Variant: the cards where it is preceded by the line break «… При» (conductor:55, forge:44, speed-cost:62, release-next:47,
  onboarding-forge:44, collect:68, github-move:40, _template:42) match the same `\s+` regex.
- R2: `(их\s+)?число\s+и\s+дату(\s+последней)?\s+показывает\s+` + "`plans/PILES.md`" + `(\s+\(собирает\s+` + "`piles.py board`" + `;\s+карточку\s+код\s+не\s+правит\))?`
  becomes «находку, не названную ни в одной пачке, называет `piles.py check` (е)».
- R3 (the leftovers):
  - `proposals/README.md:46` «(`plans/PILES.md`)» → «(карточки кучек)»;
  - `proposals:54`, the R1 form split differently: run R1;
  - `hotfix-12586/README.md:75` «… `plans/PILES.md`.» → the same as R1;
  - `codex/README.md:108` and `grounding:217` «число и дату показывает `plans/PILES.md`» match R2.
- Kept: `onboarding-forge/README.md:87` (a «Содержание» row of closed F6-30; its path list is history).

Batch files: NOT edited. Every batch file with the board boilerplate is «закрыта» (history). The one taken batch with a hit
(onboarding-forge/1:57) is frozen by (в), and the hit is history inside it.
- How (в) treats a boilerplate edit in a taken batch: a preamble line outside «Ход»/«Остатки» differs from origin/main, so
  (в) is RED (`_compare_batch` 1712-1718). Its door is `piles-skip: в`.
- This rule therefore never asks for one. If the Lead wants a taken batch's dead pointer reworded anyway, it goes as one
  line in that batch's «Ход» (free), not as a preamble edit.

### 6.6 DECISIONS_ARCHIVE (the Lead appends)

A new entry, D-next: «The generated board `plans/PILES.md` is retired (the owner's words 13.11.2026, verbatim in §1 of t-356).
The status of a batch lives in its header and card row; writers `take`/`status`/`close`; the view is the «Бэклог» pane;
`piles.py board` is a refused alias. `check` judges the piles a commit touches (and a staged `.py` a function list names);
the full audit's reader is check 33 (a). (б) and `take` protect one developer from another; between different developers a
waiting node holds its zone (the owner's words 13.11.2026); "one session" read as "one developer slug" pending the owner's
answer (Q-O1). Detectors: check 33 (a), (b′), (b″), (d); `tools/test_backlog_tree.py`.» Its placement (DECISIONS.md vs the
archive) is the Lead's.

### 6.7 Axis blocks, one per mechanism commit (the current map has 36 axes) (t-367 N6)

Each block answers every axis of `docs/SIBLING_MAP.md` by line. "package" = an axis whose carriers live only in
`ai-packages/qa-factory/`, which no node touches.

**Block SL-5a/SL-1 — the board retired (code, hooks, CI line 81, settings, `.gitattributes`, the file).**
- axis 1: n/a (no policy, role or journal text in this commit; PROJECT.md follows in SL-5b).
- axis 2: n/a (no exam instrument).
- axis 3: n/a (package release copy; nothing ships).
- axis 4: n/a (no factory rule, debt or principle).
- axis 5: n/a (package stage twins).
- axis 6: covered (forge_metrics and compact_snapshot read `load_tree`, unchanged; `test_compact_snapshot.py` in the DoD).
- axis 7: n/a (per-test identity of the package).
- axis 8: n/a (story location, package).
- axis 9: n/a (test-file leaf, not touched).
- axis 10: n/a (no new reader of the repository top).
- axis 11: n/a (no shell-command recognizer).
- axis 12: covered (producer piles.py and its readers: backlog_tree, compact_snapshot, forge_metrics, hooks, CI, settings,
  `.gitattributes`; texts follow in SL-5b).
- axis 13: n/a (dispatch text untouched).
- axis 14: n/a (no transcript reader).
- axis 15: n/a (piles.py console setup unchanged).
- axis 16: n/a (package JSON reader).
- axis 17: n/a (package detector verdict shape).
- axis 18: n/a (no ratchet).
- axis 19: n/a (package role-file reader).
- axis 20: n/a (package host receipts).
- axis 21: n/a (forge tables read by `md_table`, unchanged).
- axis 22: n/a (package).
- axis 23: n/a (package).
- axis 24: n/a (package).
- axis 25: n/a (package).
- axis 26: n/a (package).
- axis 27: n/a (package).
- axis 28: n/a (package).
- axis 29: n/a (no jsonl appender).
- axis 30: n/a (package).
- axis 31: n/a (no role file).
- axis 32: n/a (forge tools, outside the census).
- axis 33: n/a (no dispatch identity).
- axis 34: covered (`board` and `release` are retired by one road: a refused alias naming the new road, t-367 N9).
- axis 35: n/a (package).
- axis 36: n/a (package).
- Four questions: (a) cost: less — no board to stage, fewer doors; (c) detector: `tools/test_backlog_tree.py` (the pane),
  check 33 (a); (d) skip: the refused alias on the execution path, `agents_md --check` and the hooks in the same commit.

**Block SL-4 — one developer's batches; the package-root token.**
- axis 1: n/a (PROJECT.md item 3 clause lands in SL-5b).
- axis 2: n/a.
- axis 3: n/a (package).
- axis 4: n/a.
- axis 5: n/a (package).
- axis 6: n/a (forge_metrics does not read zones).
- axis 7: n/a (package).
- axis 8: n/a (package).
- axis 9: n/a.
- axis 10: n/a (`git ls-files` runs with the root the tool already holds).
- axis 11: n/a.
- axis 12: covered (readers of `_norm_token` / `parse_zone` / `tokens_overlap`: (б), `take`, collect_intake pinned,
  test_piles_form table; SIBLING_MAP row added in SL-5b).
- axis 13: covered (inside one developer the only guard is `owns_gate`'s WARN over live dispatches of one machine; two
  parallel sessions of one developer are no longer blocked by (б); `dispatch_manifest` unchanged) (t-367 B2).
- axis 14: n/a.
- axis 15: n/a.
- axis 16: n/a (package).
- axis 17: n/a (package).
- axis 18: n/a (no ratchet).
- axis 19: n/a (package).
- axis 20: n/a (package).
- axis 21: n/a.
- axis 22: n/a (package).
- axis 23: n/a (package).
- axis 24: n/a (package).
- axis 25: n/a (package).
- axis 26: n/a (package).
- axis 27: n/a (package).
- axis 28: n/a (package).
- axis 29: n/a (reads journal names, appends nothing).
- axis 30: n/a (package).
- axis 31: n/a.
- axis 32: n/a (forge tools).
- axis 33: n/a.
- axis 34: covered (one computation of "same developer" from the git index for the commit, `take` and CI; the exception by
  case rests on the owner's quoted word 13.11.2026, its reading pending Q-O1; dev.config read only by the writer-side
  WARNING).
- axis 35: n/a (package).
- axis 36: n/a (package).
- Four questions: (a) cost: fewer false reds and doors between one developer's batches; one git call per run; (c) detector:
  calibration check 33 (b″) (§6.2); (d) skip: commit-msg `check`, CI `check --base`, `take` on the execution path.

**Block SL-2 — the check's scope; the function-list carrier; take reads like check; CI line 85.**
- axis 1: n/a (PROJECT.md item 8 lands in SL-5b).
- axis 2: n/a.
- axis 3: n/a (package).
- axis 4: n/a.
- axis 5: n/a (package).
- axis 6: covered (`load_tree` gains `skip`, default empty: forge_metrics, compact_snapshot and backlog_tree calls unchanged).
- axis 7: n/a (package).
- axis 8: n/a (package).
- axis 9: n/a.
- axis 10: n/a (`git diff` / `git ls-files` with the tool's root).
- axis 11: n/a.
- axis 12: covered (every red class with its carrier, §4 B; protocol check 33 reworded in SL-5b).
- axis 13: n/a (function-list form 1 read by `dispatch_manifest` unchanged).
- axis 14: n/a.
- axis 15: n/a.
- axis 16: n/a (package).
- axis 17: n/a (package).
- axis 18: n/a.
- axis 19: n/a (package).
- axis 20: n/a (package).
- axis 21: n/a.
- axis 22: n/a (package).
- axis 23: n/a (package).
- axis 24: n/a (package).
- axis 25: n/a (package).
- axis 26: n/a (package).
- axis 27: n/a (package).
- axis 28: n/a (package).
- axis 29: n/a.
- axis 30: n/a (package).
- axis 31: n/a.
- axis 32: n/a (forge tools).
- axis 33: n/a.
- axis 34: covered (one scope rule for the commit and CI; no second audit road in CI, F-2 (a); `take` and `check` skip
  untracked foreign files by one rule).
- axis 35: n/a (package).
- axis 36: n/a (package).
- Four questions: (a) cost: about 240 skip lines a month gone; a code commit staging a listed `.py` loads the tree once;
  (c) detector: check 33 (a) (the reader of untouched-pile reds) and (b′); (d) skip: commit-msg `check`, CI `check --base`.

**Block SL-3 — `piles.py status`.**
- axis 1: n/a (PROJECT.md item 7 names `status` in SL-5b).
- axis 2: n/a.
- axis 3: n/a (package).
- axis 4: n/a.
- axis 5: n/a (package).
- axis 6: n/a (no measurer reads node cells differently).
- axis 7: n/a (package).
- axis 8: n/a (package).
- axis 9: n/a.
- axis 10: n/a.
- axis 11: n/a.
- axis 12: covered (one writer per status word; `STATUS_ORDER` the one order table; SIBLING_MAP row 296 in SL-5b).
- axis 13: n/a.
- axis 14: n/a.
- axis 15: n/a.
- axis 16: n/a (package).
- axis 17: n/a (package).
- axis 18: n/a.
- axis 19: n/a (package).
- axis 20: n/a (package).
- axis 21: covered (cells written through the existing table writer `write_like`/`apply_changes`; read back by `md_table`).
- axis 22: n/a (package).
- axis 23: n/a (package).
- axis 24: n/a (package).
- axis 25: n/a (package).
- axis 26: n/a (package).
- axis 27: n/a (package).
- axis 28: n/a (package).
- axis 29: n/a.
- axis 30: n/a (package).
- axis 31: n/a.
- axis 32: n/a (forge tools).
- axis 33: n/a.
- axis 34: covered (`take`, `status`, `close` are the one code road per status word; a hand edit stays the named door).
- axis 35: n/a (package).
- axis 36: n/a (package).
- Four questions: (a) cost: one command replaces a hand edit; (c) detector: calibration check 33 (d) «card row Статус
  ahead of its batch file»; (d) skip: on discipline alone for the hand edit (masked by (в)), with 33 (d) as the leak detector.

**Block SL-5b — texts: PROJECT.md (+AGENTS.md), protocol 33/39, SIBLING_MAP 12/13, README, BACKLOG header, decision entry.**
- axis 1: covered (PROJECT.md «Командная работа» items 3, 7, 8 and the closing line; AGENTS.md regenerated; journal unchanged).
- axis 2: n/a.
- axis 3: n/a (package).
- axis 4: n/a (no factory rule).
- axis 5: n/a (package).
- axis 6: covered (check 39 reworded: `summary` and compact snapshot).
- axis 7: n/a (package).
- axis 8: n/a (package).
- axis 9: n/a.
- axis 10: n/a.
- axis 11: n/a.
- axis 12: covered (§6.4 rows, BACKLOG header; cards in SL-6).
- axis 13: covered (the guard wording corrected, §6.4).
- axis 14: n/a.
- axis 15: n/a.
- axis 16: n/a (package).
- axis 17: n/a (package).
- axis 18: n/a.
- axis 19: n/a (package).
- axis 20: n/a (package).
- axis 21: n/a.
- axis 22: n/a (package).
- axis 23: n/a (package).
- axis 24: n/a (package).
- axis 25: n/a (package).
- axis 26: n/a (package).
- axis 27: n/a (package).
- axis 28: n/a (package).
- axis 29: n/a.
- axis 30: n/a (package).
- axis 31: n/a.
- axis 32: n/a.
- axis 33: n/a.
- axis 34: covered (the texts name one road per action: `check` scope, `take`/`status`/`close`, the refused aliases).
- axis 35: n/a (package).
- axis 36: n/a (package).
- Four questions: (a) cost: PROJECT.md −111 bytes; (c) detectors: check 33 (a), (b′), (b″), (d), check 39; (d) skip:
  `agents_md --check` in pre-commit/CI, `mechanism_gate` on the commit.

---

## 7. Forks — decided (one owner question open)

- **F-1: the producer of «следующий свободный B-id».** DECIDED (a), Lead 13.11.2026, with t-367 N2: `piles.py summary`,
  read-only, prints the old count line to stdout and writes nothing; `_open_sets` and the id computation stay for it.
  (Rejected: (b) a hand max over BACKLOG + findings, the collision class PROJECT.md item 4 guards with one issuer.)
- **F-2: the CI step `piles.py check --all --base "$BASE"` (forge-check.yml:85).** DECIDED (a), Lead 13.11.2026, with
  t-367 N3: `check --base "$BASE"`, blocking, range-scoped, the same rule as the commit. No audit step in CI; calibration
  check 33 (a) is the named reader of reds in untouched piles. `test_workflows.py:155` follows. (Rejected: (b) keep
  `--all --base`, a red anywhere on main blocks every push.)
- **F-3: who carries an a9 red («open id placed nowhere»).** DECIDED (a), Lead 13.11.2026: BACKLOG + the piles that named
  the id at the base rev, found by `git grep -l <id> <base> -- plans/piles`, run only when a9 reds exist.
- **F-D1: between DIFFERENT developers, does a WAITING node hold a zone?** DECIDED by the owner: (3) between different
  developers — every node that is not accepted holds its zone, as today (the owner's word 13.11.2026: «Это верно для двух
  разработчиков и не верно внутри одной сессии»). `writers_of` unchanged. To reopen (1) ("only nodes «в работе»/«сдано»
  hold a zone"), ask the owner; its cost: `take` never refuses, because every node of a batch being taken is «ожидает»
  (probe P1 of review t-367). (t-367 B1)
- **F-D2: how "the same developer" is read.** DECIDED (a), Lead 13.11.2026, with t-367 B4: slugs = the names of
  `logs/journal/<slug>.jsonl` in the git index (`git ls-files -z logs/journal` through `journal_keys.journal_names`),
  matched as a whole token in `взял:`; the same set in a commit and in CI for the same tree. The two false-"same" rows (two
  people under one slug; `--who` with another's slug) are named with their accepted risk (§3 D.1); `take` prints the
  writer-side WARNING (§3 D.3). (Rejected: (b) the local dev.config slug on the check side — two roads, P31.)
- **Q-O1 — QUESTION TO THE OWNER (open; t-367 B2).** The owner said «не верно внутри одной сессии»; the spec reads
  "session" as "developer slug" (every session and clone of dev1), which is wider than the word: two parallel sessions of
  one developer are then no longer blocked by (б), and inside one developer the only guard is `owns_gate`'s WARN over live
  dispatches of one machine.
  - (a) one developer = one slug. Recommended: `взял:` carries no session identity, so nothing narrower can be read.
  - (b) narrower (one session only): not available without a session id in `взял:` (a new field and its writer).
  - The nodes run on (a) until the answer (PROJECT.md «Командная работа» p. 11). If the owner chooses (b), it opens a new
    node (PROJECT.md «Как принимается изменение пакета» item 6 (г)).

---

## 8. Ready-to-paste: batch 8 of pile `forge`

Note: `forge/batch-7-vhodyashchie-4.md` is still untaken («ожидает»). The brief asks for a NEW batch, so this is batch 8. The
Lead may put the nodes in forge/7 instead, which is the D-0044 road for findings; this work is spec-born and has no finding.

Card row for `plans/piles/forge/README.md` «Пачки» (after row 7):

```
| 8 | доски нет: `piles.py` без `board`; проверка судит только тронутые коммитом кучки; команда `status` для «сдано»/«принято»; пачки одного разработчика не держат друг друга | — (спека `docs/tasks/specs/t-356-piles-slimming-spec.md`; F6-13 из onboarding-forge/2 — узлом FG8-4) | M | ожидает | — | — | — |
```

File `plans/piles/forge/batch-8-bez-doski.md`:

```
# Forge — пачка 8: без доски, проверка по тронутому, команда `status`, зоны одного разработчика

кучка: `forge` | статус: ожидает | взял: — | ветка: — | MR: — | стенд: не нужен | приоритет: П1

Открыта 13.11.2026 (Lead) по словам владельца 13.11.2026 (доска: «Сейчас доски в гитхабе нет, можно убрать её из проджект.мд и из скрипта»; зоны: «это надо исправить», «Это верно для двух разработчиков и не верно внутри одной сессии как сейчас»).

Правило готовности: пачка закрыта, когда каждый узел «принято», свидетели узлов — в журнале взявшего.

Решения: A и D — слово владельца 13.11.2026; F-D1 (3) между разными разработчиками — слово владельца 13.11.2026; F-1, F-2, F-3, F-D2 — Lead, 13.11.2026; вопрос владельцу Q-O1 («одна сессия» = «один разработчик»?) открыт, узлы идут по рекомендации (a) до ответа.
Скоуп свидетеля: `scenario_walk.py --witness-for <owns>` и тестовые файлы `tools/`, названные в DoD узла спеки; BATCH CANON — интегратор.
Ветка пачки: `pile/forge/batch-8`; узлы сливаются в неё, в `main` — одним PR.
Общий бриф: спека `docs/tasks/specs/t-356-piles-slimming-spec.md` (§3 — узлы, §5 — тесты).
Пути «Пишет в»: от корня репозитория.

## Бриф

Что сделать: убрать доску из кода, хуков и текстов; проверка судит только тронутые кучки; команда `status`; пачки одного разработчика не блокируют друг друга; пустой токен. НЕ делать: правки пакета; правки взятых и закрытых файлов пачек.

## Узлы

Исполнитель «builder → critic» — кодовый узел (спека принята, дизайнер не нужен); «builder» — узел-документ; «Lead» — коммиты механизмов. Статусы:
`ожидает` → `в работе` → `сдано` → `принято` / `отклонено`.

| Узел | Приоритет | Что | Исполнитель | Пишет в | Зависит от | Статус |
|---|---|---|---|---|---|---|
| FG8-1 | П1 | SL-1: доска уходит из `piles.py`, тестов и `backlog_tree.py`; `board` — отказной псевдоним (спека t-356 §3 SL-1, §5.1) | builder → critic | `tools/piles.py`, `tools/piles_testkit.py`, `tools/test_piles.py`, `tools/test_piles_take.py`, `tools/test_piles_close.py`, `tools/test_piles_close_gate.py`, `tools/test_piles_findings.py`, `tools/test_md_table.py`, `tools/test_workflows.py`, `tools/backlog_tree.py` | — | ожидает |
| FG8-2 | П1 | SL-4: пачки одного разработчика не держат друг друга в (б) и `take`; токен корня пакета (спека §3 SL-4, §5.4) | builder → critic | `tools/piles.py (+dev_of, +developer_vocabulary, +same_developer, check_overlap, _overlap_refusal, cmd_take, writers_of, fn_lists_of, _norm_token, tokens_overlap, _pair_overlap, parse_zone)`, `tools/test_piles.py`, `tools/test_piles_take.py`, `tools/test_piles_form.py`, `tools/test_collect_intake.py`, `tools/collect_intake.py` | FG8-1 | ожидает |
| FG8-3 | П1 | SL-2: красное блокирует только коммит, тронувший его кучку (или названный в списке функций `.py`); неотслеживаемая чужая кучка невидима коммиту и `take` (спека §3 SL-2, §5.2) | builder → critic | `tools/piles.py`, `tools/test_piles.py`, `tools/test_piles_findings.py`, `tools/test_piles_placement.py`, `tools/test_piles_form.py`, `tools/test_piles_door.py`, `tools/test_piles_frozen.py`, `tools/test_piles_take.py`, `tools/test_workflows.py` | FG8-2 | ожидает |
| FG8-4 | П2 | SL-3: команда `piles.py status` — один писатель «сдано»/«принято» (заменяет F6-13 onboarding-forge/2) (спека §3 SL-3, §5.3) | builder → critic | `tools/piles.py`, `tools/test_piles_take.py` | FG8-3 | ожидает |
| FG8-5 | П1 | SL-5: 5a — хуки, CI (строка 81), `settings.json`, `mechanism_gate.py`, удаление `plans/PILES.md`, `.gitattributes` при слиянии FG8-1; строка 85 CI при слиянии FG8-3; 5b — `PROJECT.md` + `AGENTS.md`, протокол 33/39, оси 12 и 13, README, шапка BACKLOG, запись решения (спека §3 SL-5, §6) | Lead | `.githooks/pre-commit`, `.githooks/pre-merge-commit`, `.github/workflows/forge-check.yml`, `.claude/settings.json`, `tools/mechanism_gate.py`, `plans/PILES.md`, `.gitattributes`, `PROJECT.md`, `AGENTS.md`, `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`, `docs/SIBLING_MAP.md`, `README.md`, `plans/BACKLOG.md`, `docs/DECISIONS_ARCHIVE.md` | FG8-1 (5a), FG8-3 (строка 85), FG8-4 (5b) | ожидает |
| FG8-6 | П3 | SL-6: строки карточек о доске — одно механическое правило (спека §6.5) | builder | `plans/piles/_template/README.md`, `plans/piles/*/README.md` | — | ожидает |

## Ход

## Живые доказательства

| Что | Стенд | Кто | Статус |
|---|---|---|---|

## Остатки

<!-- строка: сделано: <хэш | t-nnn> | узел: <id> | перенос: … | обоснование: … | подтвердил: <кто, дата> -->
```

Checks against the gate:
- An untaken batch needs `## Бриф` and `## Узлы` (`_heading_reds`); both are present.
- Row «Строки» `—` means no coverage check.
- Each node has an executor and backticked paths. FG8-5's «Пишет в» is a file list (the Lead's).
- FG8-2's function list uses `+` for the three names that do not exist yet (D-0048 grammar: a bare name that does not exist
  is "undefined", a red once another batch lists functions on piles.py) (t-367 N5).
- The «Живые доказательства» table is header-only, so it owes nothing (no role behaviour changes).
- The forge card's «Содержание» needs no row: there is no finding file and no row id.
- `plans/BACKLOG.md` in FG8-5 is a header-line edit, not a row (§2.2).
- Note: FG8-6's token `plans/piles/*/README.md` is a glob. Under (б) it overlaps every active batch of ANOTHER developer
  that writes a card (a waiting node holds its zone, F-D1 (3)). The Lead may write the 33 paths or take FG8-6 last.
  (t-367 B1)

---

## 9. Reading trail

- `tools/piles.py` (read-main), read: 1-160, 540-910, 908-1330, 1327-1806, 1806-2365, 2365-2564, 2800-2860, 3020-3254. Function
  map by grep `^def |^[A-Z_]+ = `.
- `tools/backlog_tree.py` (whole), `tools/test_backlog_tree.py` (whole), `tools/claude-mods/backlog/hooks/register.tsx:1-30`.
- `tools/piles_testkit.py` (whole). `tools/test_piles.py:160-374`. Test names of `test_piles_{take,close,close_gate,findings}.py`
  by grep `^def test_`. Per-file counts by grep.
- `tools/forge_metrics.py:570-630`, `tools/compact_snapshot.py:350-395`, `tools/journal_keys.py:505-534` (+ the def map).
- `.githooks/commit-msg`, `pre-commit`, `pre-merge-commit` (whole), `.github/workflows/forge-check.yml` (whole).
- `.claude/settings.json` (grep piles: 138, 139, 157, 158). `tools/test_workflows.py:154-155`,
  `tools/hook_liveness_probe.py:76,941-961,1363-1373` (grep).
- `PROJECT.md:274-353` (read-main; identical to the loaded copy).
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md:965-1024, 1080-1085`.
- `docs/DECISIONS_ARCHIVE.md:51-145`, `docs/SIBLING_MAP.md` (axis headings by grep; 286-311).
- `plans/builder-rules.md:14-49`. `ai-packages/qa-factory/scripts/tests/test-layers.json`: grep `piles|backlog_tree` found
  nothing; the control `"keep"|quarantine|tools/` found lines 3, 35, 78 … (so `tools/` tests are not in the layers file).
- `plans/piles/forge/README.md:1-50, 195-219`, `forge/batch-7-vhodyashchie-4.md:1-40`, `github-move/batch-3:29-32`,
  `onboarding-forge/batch-2:1-12, 72`, `onboarding-forge/findings/20261015-ostatki-f5-4-…md` (whole).
- Header statuses of every batch file (grep `^кучка: .*?статус:`). `взял:` values of taken batches (grep).
- The PILES/board greps of §2 with their controls. The board-symbol grep over `tools/*.py`. `logs/journal`: grep
  `journal_created` found only `dev1.jsonl` (Glob on the hidden `.claude` path returned nothing, a miscall; the Grep control
  found the file).
- Fix round t-375 (read-main, read): the review t-367 (whole); `tools/piles.py:98-113` (STATUS_ORDER over BATCH_STATUSES,
  NODE_STATUSES, NOT_WRITING), 809-891 (load_pile, load_tree, staged_paths, untracked_piles), 1088-1121 (board_triggers,
  cmd_board), 1318-1400 (`_norm_token`, `parse_zone`, `tokens_overlap`), 1500-1601 (`_list_verdicts`, `_pair_overlap`,
  `check_overlap`), 2228-2277 (`_relevant`, `run_check`), 3168-3254 (`cmd_release`, the CLI, `COMMANDS`, `main`);
  `tools/journal_keys.py:447-539` (`journal_names`, `developer_slug`, `disk_journal_files` = `os.scandir`);
  `tools/test_piles_form.py:50-80`; `tools/test_collect_intake.py:505-532`; `.githooks/pre-commit` (whole);
  `docs/SIBLING_MAP.md:288-311` and the 36 axis headings (grep `^## Axis`); `.git/config` of the root (grep `hooksPath`: line 8).

Not done, with why:
- The git-log skip counts were not re-measured by the designer (no shell); the critic re-measured them (t-367 P2).
- The test count «361» was not verified: the grep counts decorators and defs together. §5 lists tests by name instead.
- PROJECT.md byte counts are by hand. The Lead measures them (§6.1).

Contradictions with the brief, reported and not acted on:
- (i) The empty token comes from the cell `` `ai-packages/qa-factory/` ``, not from `нет` or an empty cell (§3 SL-4 D.6).
- (ii) PROJECT.md line 295 names (д) as the D-0044 detector, but the code says (е).
- (iii) The «Входящие» number has no reader besides check 33, which already reads (е).

Small choices closed by the designer (Lead may reverse):
- "Not blocking" reds are summarised per item (B.5).
- Node statuses are allowed in untaken batches, refused in closed ones.
- Batch `сдано` has no node condition.
- A two-id node row is refused.
- `принято` cell forms with one value.
- `--all` shows untracked piles with a note.
- SL-4 goes before SL-2.
- Batch files are never edited by the boilerplate rule.
- (д) → (е) in PROJECT.md line 295.
- t-375: `STATUS_ORDER` is rebuilt over `NODE_STATUSES` (one table) and finality is read from `NOT_WRITING` (N8).
- t-375: `tops` defaults to None, the safe side, so the existing two-argument calls stay valid (B3d).
- t-375: `tokens_overlap` returns False for an empty token (the invariant of D.6, pinned by the spaces row in the existing
  table; `net-cell` is not a row because it is not new behaviour).
- t-375: D.6 (v) takes the first of the review's two options — the package root stays an unreadable zone part (today's
  behaviour); "maps it to every package path" is not taken.
- t-375: the `take` WARNING prints when the clone's slug is readable and `dev_of(--who)` differs from it (None included);
  nothing when the clone's slug cannot be read.
- t-375: `take` skips untracked files of OTHER piles only; the pile being taken is read with its untracked files (B.9).
- t-375: `_relevant` with an unloadable tree runs the check (safe side).
- t-375: the (б) developer tests are rows of one `test_check_b_pair_by_developer` in `test_piles_form.py` (one behaviour,
  one parametrized test).
- t-375: `nightly.yml:12` and `test_workflows.py:8` stay as history comments (N7).
- t-375: the CI line 85 change lands in SL-2's integration commit (with `range_paths`), not in SL-5b.

---

## Questions back to the Lead (t-375)

- **L-1 — B3 (a) is applied as worded, but on re-check it is not sufficient; evidence:**
  - `.git/config:8` (root checkout): `hooksPath = C:\\QAFactory\\forge-repo\\.githooks` — absolute, so every worktree
    (builder worktrees and any batch-8 worktree) runs the ROOT checkout's hooks, i.e. those of whatever branch the root
    holds (today `main`).
  - `.githooks/pre-commit:5` `set -e` and `:40` `python tools/piles.py board --check --if-staged` run relative to the
    committing tree's cwd, so they call the committing tree's NEW piles.py.
  - In that piles.py `board` is gone or a refused alias: argparse usage error → `CannotRun` (piles.py:3179-3180) → exit 1
    (3248-3250); a refused alias is `CannotRun` too (3168-3171). The failure comes BEFORE `--if-staged` is read, so it does
    not depend on staging `plans/PILES.md` (the review's mechanism, `board_triggers` 1096-1097, is not reached).
  - Consequence: the SL-1 builder cannot commit ANY change that removes `board`, and neither can the SL-4 / SL-2 / SL-3
    builders after it, until the root checkout's `pre-commit` loses line 40; step 5 of the integration procedure runs the
    NEW hook only if that commit is made in the root checkout itself.
  - Options: (a) a pre-step on `main` before SL-1 starts: the Lead drops the three board callers (pre-commit:38-40,
    pre-merge-commit:19-20, forge-check.yml:81, settings 139/158) while `board` still exists — nothing reads the board
    (the owner's word), it just goes stale for the batch's life; then builders commit normally and SL-5a keeps only the
    delete, `.gitattributes` and the comment. Recommended. (b) Keep the --no-commit procedure, have the Lead check out
    `pile/forge/batch-8` in the root checkout for every node integration, and let builders hand SL-1..SL-3 over
    uncommitted. (c) A transitional `board` that exits 0 until SL-5a — rejected by N9 (a second road).
  - Not applied by me: the procedure in §3 SL-1 stays as the Lead decided; this needs the Lead's word.

---

## Review t-367 applied

| Item | Where it landed (section, line) |
|---|---|
| B1 | §1 l.44-47 (F-D1 (3) sentence replaces "the owner decides it"); §3 SL-4 D.5 l.252-253 (`writers_of` unchanged); §5.4 l.642-643 (waiting-node row) and l.660 (the F-D1 (1) tests deleted); §7 F-D1 l.996-1000 (decided by the owner, (1) only as "to reopen, ask the owner" with its cost); §8 FG8-6 note l.1084-1086 (the "Under F-D1 (1)" clause dropped); §3 SL-3 l.423-424 (no overlap at `status --set "в работе"`) |
| B2 | §1 D l.36-40 (reading recorded as a QUESTION TO THE OWNER, recommendation (a), nodes run on (a)); §1.1 l.55; §3 SL-4 D.2 ok line l.234-237 (`owns_gate`'s WARN named); §6.4 axis 13 l.735-737; §6.7 SL-4 axis 13 l.832-833; §7 Q-O1 l.1006-1014 |
| B3 (a) | §2.1 l.91 (`.gitattributes`) and l.96 (`plans/PILES.md`) → SL-5a; §3 l.139-141 (integration branch `pile/forge/batch-8`); SL-1 owns l.156-159; temporal edge with the step-by-step `git merge --no-commit --no-ff` procedure l.172-182; SL-5a l.435-437; §8 FG8-1 l.1056 and FG8-5 l.1060 cells; see question L-1 l.1159-1177 |
| B3 (b) | §5.4 l.660 (`test_node_status_to_v_rabote_runs_overlap` deleted); §3 SL-3 l.423-424 |
| B3 (c) | §3 SL-2 B.3 l.329-336 (carrier (b1.path, b2.path, the `.py`), `_relevant` extended, CI range paths are carriers); invariant l.337-339; B.4 (б) l.343-344; SL-2 owns l.291-294 (`_relevant`, `check_overlap`, `_pair_overlap`, `_list_verdicts`); §4 B l.485-492 (edge rows); §5.2 l.599-602 (test rows `fn-list-code-commit`, `fn-list-py-not-listed`, `fn-list-range`) |
| B3 (d) | §3 SL-4 owns l.198-201 (`test_piles_form.py`, `collect_intake.py` pinned, `test_collect_intake.py`, `parse_zone`); D.6 (iii) `tops` keyword l.270-274; D.6 (v) l.276-278; §2.1 l.94-95; §5.4 l.647-659 (rows into `test_check_b_token_overlap_rules`, collect_intake row); §6.4 row 298 l.730 |
| B4 | §3 SL-4 D.1 l.206-232 (`git ls-files -z logs/journal` through `journal_keys.journal_names`; untracked journal row; the two false-"same" rows with accepted risk l.227-231); D.3 WARNING l.244-249; D.4 l.250-251; §4 D l.518-523; §5.4 l.637-638; §7 F-D2 l.1001-1005 |
| N1 | §1.1 «Owner-facing plan» l.49-55 ("slim, not rewrite" l.53; "a commit is blocked only by reds of the piles it touches" l.54) |
| N2 | §2.1 l.79 (`_open_sets` and the id computation kept, `toc_lines` split); §2.3 l.123-127; SL-1 l.170-171; §7 F-1 l.987-989 |
| N3 | §3 SL-2 B.5 l.352-355, B.6 l.356-357 (33 (a) the one reader, no CI audit step); §6.2 l.709; §7 F-2 l.990-994 (option (c) and its false premise deleted) |
| N4 | §3 SL-2 B.2 l.319-320 (working-tree reading named); B.9 l.364-370 (`cmd_take` reads untracked foreign batches like check, in SL-2 itself, with invariant); SL-2 owns l.292-294 (`cmd_take`, `test_piles_take.py`); §4 B l.508-510 (edges); §5.2 l.609-613 (test rows) |
| N5 | §8 node preamble l.1051 (executor reconciled with the rows); FG8-2 cell l.1057 (`+dev_of`, `+developer_vocabulary`, `+same_developer`); gate note l.1079-1080 |
| N6 | §6.7 l.772-983 (one block per mechanism commit SL-5a/SL-1, SL-4, SL-2, SL-3, SL-5b, all 36 axes by line); §6.2 l.711 (new check-33 line (b″), SL-4's detector) and l.712 (33 (d), SL-3's detector); SL-3 l.430-431; SL-5 l.444-445; D.1 l.230 |
| N7 | §2 l.71; §2.1 l.88-89 (`test_workflows.py:8`, `nightly.yml:12`, verdict: history) |
| N8 | §3 SL-3 edge 3 l.404-409 (`STATUS_ORDER` extended over `NODE_STATUSES`, finality from `NOT_WRITING`; no second table); §5.3 l.625; small choices l.1140 |
| N9 | §2.1 l.83 (`board` a refused alias like `release`, naming the «Бэклог» pane and `tools/backlog_tree.py`); SL-1 l.166-167; §4 A l.468-469; §5.1 l.548-550; §6.7 SL-5a axis 34 l.812 |
| §6.1 (6) bullet | §6.1 l.697-701 (item 3 clause MANDATORY; net −111); §2.2 l.102; SL-4 l.287-288; SL-5b l.440 |
