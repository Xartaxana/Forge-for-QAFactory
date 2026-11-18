# FG7-81 - named_by pointers in test-layers.json: a check that the carrier names the key, and the re-pointing (draft card)

task: t-1424 · node: forge/7/FG7-81 · feature: F19 · designer draft, 18.11.2026 · decisions are the Lead's (forks in section 8)

## 0. Target on main, measured

Tree: root checkout, `main` = `origin/main` = `de7761a7` (read from `.git/refs/heads/main` and `.git/refs/remotes/origin/main`).
FG7-79 is in: row `test_handoff_values_refusal.py` -> `design/state-exits.md:125`, and line 125 names that file (positive control).
Whether the working tree of the files I read is clean was NOT measured (no shell): `estimate` - the Lead runs
`git -C C:/QAFactory/forge-repo status --short ai-packages/qa-factory/scripts/tests/test-layers.json ai-packages/qa-factory/design`.

Code target:
- `ai-packages/qa-factory/scripts/selftest.py::layers_problems` lines 610-614: a `detector` row needs a non-empty `named_by`
  LIST and the key `replaced_by`. Nothing reads what an entry says (the brief's ":614-616" is :611-612 today).
- `selftest.py::test_layers` raises `TestLayersError` on the FIRST `layers_problems` sentence. Its callers include
  `selftest.canon_class` (dispatch gate, witness command), `scenario_walk.witness_for`, `tools/test_quarantine.py::_layers`,
  `tools/test_redundancy.py`.
- `selftest.py::_listing_ok` (:757-774) prints the keep-wide FAIL lines once per pipeline (`keep row names no file`).
- `tools/test_quarantine.py::cmd_check` (:1781-1794) sums its problem lists into `N violation(s)`; `FORGE_CARRIERS` (:51) and
  `forge_texts` (:222) pass forge texts to `selftest.gate_named_files(extra_texts)` (the package does not read `docs/`, AR-4).
- `tools/test_split.py` :1837 tells each split part to INHERIT `named_by`; `docs/TESTING.md` :239-241 says the same.

Data measured: Grep `-o -n` of `test_[a-z0-9_]+\.py` over each carrier, joined by hand to Grep `-B4/-B5` of
`test-layers.json` (a hand join, not a script run):

| carrier of the entry | entries `path:N` | line N names the key | carrier names the key on SOME line |
|---|---|---|---|
| `design/state-exits.md` | 71 (69 rows) | 18; **53 stale** | 69 of 71; the 2 that do not: `test_story_run_loop_b_threshold.py`, `test_story_run_loop_b_answers.py` (both -> :57; only `..._loop_b_loop.py` is named, :58 and :197) |
| `design/architecture.md` + `factory-rules.md:432` | 39 | 2 (`factory-rules.md:432`, `architecture.md:125` for `..._s0_snapshot.py`); 37 stale | all but 4 rows: `test_story_run_s0_source_list.py`, `_s0_paste_owners.py`, `_s0_c29.py` (TD-11c parts; :125 names only `_s0_snapshot`), `test_gate_preflight_question_status.py` (layer `data_join`, -> :161) |
| `scripts/refusal_registry.py` | 32 | 0; 32 stale (e.g. `test_brief_pack.py` -> :490 names `test_doctor_context.py`; brief_pack is :756) | 32 of 32 (each row's `"test":` field) |
| `scripts/tests/test_*.py` (the detector's own file or a split sibling) | 17 (11 rows) | 0: the line holds a census/ratchet, not a test name (e.g. `test_story_run_refusals_core.py:472/475`, 6 rows) | not the meaning of these entries |
| forge `docs/...` | 52 (`SIBLING_MAP.md` 50, `t-2147` spec 2) + 1 bare `docs/TESTING.md` | not measured (AR-4) | not measured; 24 rows have ONLY forge carriers |

Total line entries 211 (Grep count of `^\s+"[A-Za-z0-9_./-]+:\d+",?$`), 162 non-empty `named_by` arrays + 6 empty (shims).
One entry has no line (`test_story_step.py` -> `docs/TESTING.md`). Drift is uniform per carrier (state-exits +1..+43,
architecture +39 = the variety map inserted 17.11, refusal_registry +33 or more to the nearest naming line): the pointers were taken on older bytes.
The package already states the principle twice: `test_state_exits.py:10-11` "Keyed on names, never on line numbers" and
`test_profile_reader.py:564` "Not line numbers: another change to the file moves them". `CLAUDE.md` rule 11 points at code by
`path::symbol`, never by line.

## 1. Architecture

Package files are release files: every string the cards add (FAIL lines, notes, carrier cells) is English, no Cyrillic;
`python -B scripts/selftest.py --lang` is in card A's DoD.

| AR | how it is touched | change check written into the DoD |
|---|---|---|
| AR-4 | the package check reads only package files; an entry outside the package is counted, never read; the forge passes its own texts (prior art `gate_named_files(extra_texts)`). Entries are package-relative carrier paths, not stored project paths: no resolver, no K7 row | grep the new function for `docs/` or a forge root: 0 hits besides the note text |
| AR-13 | `test-layers.json` stays read only through `selftest.test_layers()`; carriers through `selftest._carrier_text`; the forge calls the package function, it does not parse entries | grep `tools/` for a second `named_by` entry parser: only `test_quarantine.py` calling `named_by_problems` |
| AR-14 | no new writer: under F1 (b) there is no repoint door; keep rows are hand-edited as today; quarantine/cohorts stay `test_quarantine.py`'s | diff of card A touches `named_by` entries and one row's key only |
| AR-25 | two proven-by cells of `state-exits.md` gain the part names | `test_state_exits.py` whole (named test files exist on disk) |
| AR-29 | see the census table below | the census row; `test_judgment_census.py::test_c1_...` narrow |

AR-29 census of every check the change adds or alters:

| check | owner | class |
|---|---|---|
| K1 `selftest.named_by_problems`: an in-package carrier names the key (bounded token) or holds the `::symbol` | data (code) | xref |
| K2 same function: entry form (string, relative, `/`, no `..`, no `:N`, `::` only on `scripts/tests/test_*.py`, non-empty symbol) | data (code) | shape (row takes the higher class: xref) |
| K3 `tools/test_quarantine.py::cmd_check` named_by lines for forge carriers (card B) | data (code) | xref (forge tool, outside the package census) |
| whether a `::symbol` is the RIGHT census for the detector | judgment: the critic (rule 22), accepted by the Lead | not code; code checks presence only |
| `layers_problems` presence check | data | unchanged |

Commit lines: the package commit carries the lines `tools/architecture_gate.py` checks (that file is the only carrier of their
form); its `judgment:` line is the `none` kind with ` -- the new check is xref/shape over the package's own registry; it refuses no role's output`.

`variety: none -- the check joins the package's own test registry to its own design carriers at selftest time; no project value is read and no axis is met`

## 2. Design (written for F1 (b), the recommendation; the (a) delta is in 2.4)

### 2.1 The entry form after the move

A `named_by` entry is one of:
- `<rel>` - the carrier file names the key;
- `<rel>::<symbol>` - only when `<rel>` is `scripts/tests/test_*.py`: the detector's census/ratchet lives at `<symbol>` in that file.

`<rel>` is relative, `/`-separated, no `..`, no drive, no leading `/`. `<symbol>` matches `[A-Za-z_][A-Za-z0-9_]*`. No `:<digits>`.

### 2.2 The check (package, card A)

`selftest.named_by_problems(keep: dict, extra: dict | None = None) -> tuple[list[str], list[str]]` returns (problems, outside):
for every `keep` row that HAS `named_by` (any layer: one road), sorted by key then entry:
1. `named_by` is not a list -> problem. An entry that is not a non-empty string, or breaks 2.1 -> problem naming the entry
   and the door (`write the carrier path; a test-file census as <path>::<symbol>; no line numbers`).
2. Resolve `<rel>`: a file under the package root (`PLUGIN_ROOT / rel`), else a key of `extra` (forge texts), else -> `outside`.
   An in-package file that cannot be read -> problem naming the OSError class (never a pass).
3. No symbol: the text holds the key as a bounded token, regex `(?<![A-Za-z0-9_])` + `re.escape(key)` + `(?![A-Za-z0-9_])`,
   case-sensitive -> ok; else problem `<key> -> <entry>: the carrier does not name <key>`.
4. Symbol: the text holds the symbol as a bounded identifier -> ok; else problem.

`_listing_ok`, inside its `once` block right after the `keep row names no file` loop: one FAIL line per problem
(`tests: named_by: <problem>`), and when `outside` is non-empty ONE note line
`tests: named_by: <K> entr(ies) name a file outside this package, not checked here (the forge checks them)` (a PASS/note, not FAIL).

Positional invariant: the call is NEVER inside `test_layers`/`layers_problems` - a stale or malformed entry must not make
`test_layers` raise, so the dispatch gate's `canon_class`, `witness_for`, `test_quarantine` and `test_redundancy` keep reading
the file; it runs only where `enforce_listing` is true and once per pipeline (shard 2 never repeats the lines), as its sibling does.

Direction of error (a presence check becomes a content gate): the function may err toward a FAIL (a doubtful match is
refused), never toward passing an entry whose carrier lacks the bounded key. Adversarial inputs that must stay refused:
key `test_files.py` with the carrier naming only `test_test_files.py` (architecture.md:90 does); key
`test_story_run_loop_b.py` (a parent) with the carrier naming `test_story_run_loop_b_loop.py`; the key without `.py`; the key
in another case; `design/state-exits.md:57`; `C:/x.md`, `/x.md`, `../docs/x.md`, `design\\x.md`; `""`, `5`, `null`;
`scripts/tests/test_x.py::`; `design/state-exits.md::provisional`; a symbol that is a prefix of a longer identifier (`NO_CARD` vs `NO_CARD_BASELINE`).

### 2.3 The re-pointing (card A, same commit)

- Every `<rel>:<N>` -> `<rel>` (line-local text edit of the entry lines; the rest of the file byte-identical); same carrier
  twice in one row -> one entry (e.g. `test_provisional.py` :95/:96, `test_question_register.py` :140/:141). Forge entries
  are rewritten the same way (a form edit reads no `docs/` file).
- The 11 test-file rows -> `<rel>::<symbol>`: `test_stage_cards.py::NO_CARD` (:41), `test_profile_reader.py::CENSUS_EXEMPT`
  (:566), the 6 rows on `test_story_run_refusals_core.py` -> `::refusal_every_action_has_a_move` (:446, holds :472/:475);
  `test_onboarding_markers.py`, `test_silent_passes.py`, `test_role_commands.py`: the builder names the census symbol the
  row's `why` describes; none found -> a question in the report, the row unchanged (not guessed).
- The 6 in-package rows whose carrier names no key (F4, recommended): `state-exits.md` line 58 proven-by cell adds
  `` `test_story_run_loop_b_threshold.py` ``, `` `test_story_run_loop_b_answers.py` `` beside `..._loop_b_loop.py`;
  `architecture.md` :125 (AR-6 Detector) adds the three `test_story_run_s0_*` parts beside `_s0_snapshot`;
  `test_gate_preflight_question_status.py` (`data_join`, no named_by needed) loses its `named_by` key.
- After the edit the narrow call prints `problems 0`.

### 2.4 Delta if the Lead picks F1 (a) - line pointers kept and checked

Step 3 becomes "line N (1-based over `text.split("\n")`, not `splitlines()`, which also breaks on `\x0c`, `\x1c`, `\u2028`)
names the key"; N past the end -> problem `line N past the end (M lines)`; the 17 test-file entries need the symbol form
anyway. Re-pointing 159 in-package entries by nearest naming line. Recurring cost: every edit above a named row of any of four
carriers (refusal_registry.py gains rows often) turns the canon red after merge with up to 32 lines, so (a) needs a repoint
door that writes keep rows: a second writer of keep (AR-14) and its own node.

### 2.5 Card B (forge): the forge carriers, split parts

`cmd_check` adds `named_by` problems: `extra` = the text of every `outside` entry's file that exists under the forge root;
any entry still outside -> `named_by: <key> -> <entry>: the file is in neither the package nor the forge`. `test_split.py`
:1837 and `docs/TESTING.md` :239-241 gain one clause: each carrier the part inherits names the part beside its siblings.

## 3. Edges, each with its invariant

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | a pointer to a line past the end | (b): `<rel>:<N>` is refused by form whatever N is; (a): problem `past the end` | no line pointer is accepted, valid or not (b); a pointer to nothing never counts (a) |
| E2 | the line/carrier names the key's stem, not the full key | refused (bounded full key only, F2) | a carrier naming only a parent, a sibling part or a longer name never counts as naming the key |
| E3 | a carrier other than state-exits.md | the same rule for every in-package carrier; `docs/...` -> counted as outside by the package, checked by card B; in neither -> card B refuses | the package never reads `docs/` (AR-4); an entry that resolves nowhere is refused somewhere |
| E4 | a key with no named_by | detector: refused by `layers_problems` :611-612, unchanged; other layers: nothing to check; `named_by: []` (shims): nothing to check | presence stays in the shape reader; the content check never raises from `test_layers` |
| E5 | TEMPORAL: 53 stale state-exits pointers (211 line entries) at landing | one move (F5): card A lands check + re-pointing + 6 carrier fixes in one commit, `problems 0` in its witness. Before: no check, `:N` entries. After: no `:N` entry; a branch cut earlier that adds `x.md:N` merges into a FAIL line with the door | the canon is never red on the move itself; no line pointer re-enters after it |
| E6 | line drift when state-exits.md is edited later | (b): cannot happen (no lines); a carrier edit that DROPS a name -> FAIL; (a): see 2.4 | a carrier that stops naming the key is refused; an edit that only moves lines is never refused (b) |
| E7 | a key named on two lines | (b): any bounded occurrence counts; duplicate entries collapse in the migration; (a): a pointer to either line passes | one carrier, one entry; which row is irrelevant to "the carrier names it" |
| E8 | a split part inherits named_by (TD-11c) | the inherited carrier must name the part, else FAIL (the 5 cases above) | `TESTING.md` :240 "parts together cover the parent" is kept honest: a part nobody names is not a named detector |
| E9 | a test-file carrier without `::symbol`, or `::symbol` on a prose carrier | first: passes only if the file names the key; second: refused by form | a symbol stands in for the key only where a census lives (a test file); prose must name the key |
| E10 | `test-layers.json` absent / `enforce_listing` false / shard 2 | no named_by lines (as its sibling `keep row names no file`) | the absent world is today's; lines print once per pipeline |
| E11 | quarantine rows | not read | a quarantined file is not a canon detector |
| E12 | between A and B | forge entries form-checked by A, content unchecked until B | no forge entry keeps a line number after A |

## 4. Builder cards (R11-f)

### Card A - package: the check and the re-pointing

given: this file (sections 0-3 and 2.3); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/selftest.py::layers_problems, ::_listing_ok, ::_carrier_text; C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_selftest_shard.py::layers_cli_cases, ::layers_doc, ::cli; C:/QAFactory/forge-repo/docs/TESTING.md
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/selftest.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_selftest_shard.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/state-exits.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
non-goals: no edit under tools/ or docs/ (card B); no change to layers_problems or test_layers; no repoint door; no CHANGELOG line (the Lead's release step); no other test-layers.json key than named_by (and the one row's named_by removal)
handoff: the worktree branch and a report: witness tails, the narrow call's two numbers, the symbol picked per test-file row (or the question), `tests not written:` lines
edges: E1-E12 of section 3 (E3 package side, E5 one move, E9, E10 binding for this card)
DoD: `python -B ai-packages/qa-factory/scripts/tests/test_selftest_shard.py; python -B ai-packages/qa-factory/scripts/tests/test_state_exits.py; python -m pytest "ai-packages/qa-factory/scripts/tests/test_judgment_census.py::test_c1_every_unit_has_a_row_and_every_row_a_unit" -q; python -B ai-packages/qa-factory/scripts/selftest.py --lang`
siblings: selftest.layers_problems (presence, unchanged), selftest._listing_ok lines `keep row names no file` / `unlisted:` (the new lines sit beside them, same once-gate), selftest.gate_named_files (reads the same carriers by name, unchanged), tools/test_quarantine.py split-keep shim check (`named_by` empty, unchanged)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-81-named-by-pointer-check-card.md

Acceptance:
1. `named_by_problems` as 2.2; called from `_listing_ok` as 2.2; never from `test_layers`/`layers_problems`.
2. The re-pointing as 2.3; `git diff --stat` of test-layers.json touches only `named_by` lines.
3. Narrow call on the real tree from the worktree root prints `0 <K>` (K = distinct forge entries, reported):
   `python -B -c "import sys; sys.path.insert(0, 'ai-packages/qa-factory/scripts'); import selftest as S; p, o = S.named_by_problems(S.test_layers()['keep']); print(len(p), len(o)); print(*p[:5], sep='\n')"`
4. A census row `{"file": "selftest.py", "function": "named_by_problems", "class": "xref", "roles": ["conductor"], "owner": "data"}`
   if the census lists the function as a unit (the C1 node says); `test_judgment_census.py` whole is canon-judged: report
   `not run locally: test_judgment_census.py, canon judges`.

Test lines, strongest first, each a row of the `label, doc, want` table in `test_selftest_shard.py::layers_cli_cases`
(`bodies=` writes the carrier into `scripts/tests/`):
- test: test_selftest_shard.py::layers_cli_cases row "carrier names only a longer name" - key `test_det.py`, carrier body names `xtest_det.py` and `test_det_part.py`: one `FAIL tests: named_by:` line, files still run, exit 1 | expected from: section 2.2 step 3, E2
- test: same table row "a line number" - entry `scripts/tests/carrier.md:3` whose carrier names the key: one FAIL line with the no-line-numbers door, exit 1 | expected from: 2.1, E1, E5
- test: same table rows "symbol" - `scripts/tests/test_det.py::MARK` with MARK in the body: no named_by FAIL; without it: one FAIL; `scripts/tests/carrier.md::MARK`: one FAIL | expected from: 2.1, 2.2 step 4, E9
- test: same table row "outside and control" - entries `docs/OUT.md` plus a carrier that names the key: the one note line, no FAIL, exit 0 | expected from: 2.2 step 2, E3

### Card B - forge: forge carriers, split advice (after A merges)

given: this file (2.5, E3, E8, E12); C:/QAFactory/forge-repo/tools/test_quarantine.py::cmd_check, ::forge_texts, ::FORGE_CARRIERS; C:/QAFactory/forge-repo/tools/test_test_quarantine.py (ROW :875, the row at :820, the check tables :979-1126); C:/QAFactory/forge-repo/tools/test_split.py:1837 region; C:/QAFactory/forge-repo/docs/TESTING.md:239-241
owns:
C:/QAFactory/forge-repo/tools/test_quarantine.py
C:/QAFactory/forge-repo/tools/test_test_quarantine.py
C:/QAFactory/forge-repo/tools/test_split.py
C:/QAFactory/forge-repo/docs/SIBLING_MAP.md
C:/QAFactory/forge-repo/docs/TESTING.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test-layers.json
non-goals: no package code; SIBLING_MAP and test-layers.json edits only for an entry whose forge carrier does not name its key; no new subcommand or CI job (F3)
handoff: the worktree branch and a report: the first-run list of failing forge entries, what each became, witness tails
edges: E3 forge side, E8, E12; fixture constants that carry `design/state-exits.md:34` / `a:1` are rewritten to the new form with a carrier the fixture writes, no expected count changes
DoD: `python -m pytest tools/test_test_quarantine.py -q; python -B tools/test_quarantine.py check`
siblings: tools/test_quarantine.py::_rebase_problems and check_history (the same violation count), ::forge_texts (the same forge texts gate_named_files gets)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-fg7-81-named-by-pointer-check-card.md

Acceptance: `cmd_check` as 2.5; real-repo `check` ends `0 violation(s)`; each forge entry that failed the first run is fixed
by naming the key in the carrier where the carrier already describes that test's subject, else dropped when the row keeps
another carrier, else a question (24 rows have only forge carriers: none loses its last carrier silently); the
`test_split.py` advice and `TESTING.md` clause as 2.5 (F6).
- test: tools/test_test_quarantine.py check table row "forge carrier does not name the key" - fixture `docs/SIBLING_MAP.md` naming another test: exit 1, one `named_by:` violation; naming it: `0 violation` | expected from: 2.5, E3
- test: same table row "a file found nowhere" - entry `docs/NOPE.md`: exit 1, the neither-nor line | expected from: 2.5, E3
- test: none -- the split advice is prose read by a person; no reader parses it (Grep `inherit layer` over tools/: 1 hit, the line itself) | expected from: 2.5

## 5. Readers of every touched file (rule 7)

The `tools/owns_readers.py` block was NOT attached (`facts: none`): the Lead runs
`python -B tools/owns_readers.py --paths <the owns of A and B> --names named_by_problems,_listing_ok,named_by` and the plan
critic answers any line this table lacks (Q13 (d)). Hand greps (Grep tool, worktrees excluded by path):
`named_by` over `tools/*.py` -> test_quarantine.py 4, test_split.py 1, test_test_quarantine.py 5, plus homonyms test_digest_form.py:148,
test_workflows.py:285; over package `scripts/*.py` -> selftest.py :611-612 plus homonyms (probe-gap `named_by` in contract.py,
window_record.py, report_facts.py, source_exclusions.py, stage_guard.py, infra_failure.py); `.githooks/`: 0 (control: `python` 16 hits);
`.claude/agents`: `named_by|test-layers.json` 2 (rule text). `test-layers.json` over `tools/*.py`: 11 files.

| touched file | reader | verdict |
|---|---|---|
| selftest.py (`_listing_ok`, new `named_by_problems`) | `selftest.main` :923 (only caller of `_listing_ok`); `test_selftest_shard.py` via CLI | changes in A (new lines); its fixture `named_by: ["x"]` (:275) becomes one outside note, no FAIL: existing counts hold |
| test-layers.json | `selftest.test_layers` and through it `canon_class`, `scenario_walk.witness_for`, `test_quarantine`, `test_redundancy`, `lint_ratchet` (quarantine), `dispatch_manifest` (canon class), `source_split` (covers rewrite, dumps the loaded object), `owns_readers` | unchanged: none reads entry text; `test_quarantine` :1698 reads truthiness only, still truthy |
| test-layers.json | `tools/test_quarantine.py::cmd_check` | changes in B |
| state-exits.md | `test_state_exits.py`, `selftest.gate_named_files` (backticked proofs), tests reading substrings (`test_controller_resume.py` :575, `test_question_register.py` :1694, `test_manual_evidence.py` :162, `test_red_window.py` :583, `test_exploration.py` :554) | unchanged: two names added to a cell, no substring removed; the parts exist on disk |
| architecture.md | `selftest.gate_named_files` (`_PROSE_CARRIERS`), `test_quarantine` `PACKAGE_PROSE` (`_prose_mentions`, `_purge_named_in_text`), `tools/architecture_gate.py`, `tools/architecture_index.py` | unchanged; the three parts become prose-named (they are keep rows already; a later quarantine of them lists the mention) |
| judgment-census.json | `test_judgment_census.py` | changes in A (one row) |
| test_selftest_shard.py | canon | changes in A |
| test_quarantine.py / test_test_quarantine.py / test_split.py | CI `quarantine-check` job; their tests | changes in B |
| TESTING.md :239-241 | every builder and critic (rule text) | changes in B (F6) |
| SIBLING_MAP.md | `test_quarantine.FORGE_CARRIERS`, the critic | changes in B only where an entry fails |

## 6. Test cost (docs/TESTING.md)

Whole-run witness files: A - `test_selftest_shard.py`, `test_state_exits.py` (neither in `slow_tests.json` - Grep of the
four names found only `test_judgment_census.py` 96.9 and `test_refusal_registry.py`; neither matches a `canon_only` glob);
`test_judgment_census.py` is slow -> its C1 node only. B - `tools/test_test_quarantine.py` (forge). No new test file:
every case is a row of an existing table (A: the `label, doc, want` loop at :300-306; B: the check tables). Volume: A's code
is one function (~30 lines) and a call; its four rows fit under it; B's two rows under ~15 lines of code. No
adversarial battery: `test-layers.json` is internal repo data, not outside input (rule 11); the adversarial list of 2.2 is
for the critic and the implementation, not test rows.

## 7. Small choices closed by the designer

- Bounded match, case-sensitive, `/` allowed before the key (`scripts/tests/test_x.py` in a registry field counts).
- Duplicate entries are collapsed by the migration and not refused by the check (harmless).
- Problems sorted by key, then entry; one FAIL line each; one note line for all outside entries.
- The function lives in `selftest.py` next to `gate_named_files` (same carriers, same `_carrier_text`).
- test-layers.json edited line-locally (no load/dump), so the diff is the entries only.
- Symbol grammar is an identifier only; dotted or file tokens are not allowed.

## 8. Forks (the Lead decides)

- F1 entry form. (a) keep `path:N`, check line N names the key (the row's literal ask) - 159 in-package entries to repoint,
  red canon on every line move in four carriers, needs a repoint door = a second keep writer (AR-14); (b) `path` and
  `path::symbol` for test-file carriers, the carrier names the key - 6 rows to fix, drift impossible, matches
  `test_state_exits.py:10-11`, `test_profile_reader.py:564`, rule 11 `path::symbol`; (c) keep `path:N` as an unchecked
  hint and check the file - a line known wrong in 53+ rows stays in data. Recommended: (b).
- F2 stem. Full key only (recommended: the stem `test_story_run_loop_b` is a prefix of its part's name, so a stem match
  would pass parents and siblings) vs key-or-stem as the row says (no package carrier writes a test name without `.py`).
- F3 forge carriers. (i) card B in `cmd_check` (recommended; fixture constants change, no CI wiring); (ii) a new
  subcommand + a line in the CI `quarantine-check` job; (iii) leave forge entries unchecked - a `narrows` (24 rows named
  only by forge carriers keep unchecked claims), a rule 6 defect.
- F4 the 6 in-package rows with no naming carrier: name the parts in the cells that name their siblings (precedent:
  state-exits :32 and :125 name every part; architecture :231 names all 5 no-move-seam parts) and drop `named_by` from the
  `data_join` row (recommended) vs repoint them elsewhere / change their layers (judgment per row).
- F5 temporal: one move (recommended: the re-pointing is mechanical under (b)) vs the check starting as a WARN (lines nobody
  acts on; the 53 grew under exactly that silence).
- F6 the `TESTING.md` :239-241 clause (split parts: the inherited carrier names the part): card B edits it (recommended,
  the Lead accepts the rule text) vs the Lead edits it at acceptance.
- F7 `::symbol` scope: test files under `scripts/tests/` only (recommended) vs any `.py` (then
  `scripts/refusal_registry.py::REGISTRY` would pass for every key).

## 9. Noticed, not widened

- CHANGELOG 0.11.0 (:380) says "the `named_by` lines count line breaks the way an editor does": no code in tools/ or the
  package counts named_by lines today (Grep `way an editor|like an editor`: only CHANGELOG); the sentence describes a
  one-off and becomes obsolete under (b) - the Lead's release note.
- `test_onboarding_markers.py` and `test_silent_passes.py` rows say "NO_CARD in the file"; Grep found `NO_CARD` in
  `test_stage_cards.py` only among the three (head-limited read; the builder confirms) - the symbol question of 2.3.
- The review's script `crit1409_namedby.py` is not on disk (Glob over the repo: none; the temp tree timed out), so the
  57/53 figures were re-measured by hand, not by re-running it.

## 10. Reading trail

plans/piles/forge/batch-7-vhodyashchie-4.md:106 (row); reviews/t-1409-...-code.md :126-142, :220-235; selftest.py
:563-664, :685-692, :730-774, Grep `named_by|test-layers` (:58-1413), `_listing_ok(` :923; test-layers.json :1-42 and Grep
listings (pointer lines, `-B4/-B5` contexts, multiline counts 162/6/42/1, `:N` total 211, docs-only arrays 24); state-exits.md
:1-24, Grep `-o` test names, `loop_b|threshold`; architecture.md :28-72, :108-113, :173-212, Grep `-o` test names and the four
missing keys; factory-rules.md Grep `-o`; refusal_registry.py :660-687, Grep `-o`; test_state_exits.py :1-80;
test_story_run_refusals_core.py :468-477 and defs; test_stage_cards.py NO_CARD; test_profile_reader.py :560-567;
test_role_commands.py :1-6; test_selftest_shard.py :98-144, :262-321; test_judgment_census.py defs; slow_tests.json Grep;
judgment-census.json selftest rows :1017-1022; tools/test_quarantine.py :48-54, :222-228, :1155-1170, :1300-1315,
:1369-1377, :1772-1794, Grep `FORGE_CARRIERS`, `_prose_mentions`; tools/test_split.py :1832-1840; tools/test_test_quarantine.py Grep
`check|violation`; docs/TESTING.md :75-114, :213-242, Grep `named_by|detector`; Grep `layers_problems|.test_layers(|TestLayersError`
repo-wide; Grep `named_by` over tools/, package scripts, `.githooks`, `.claude/agents`; `.git/refs/heads/main`,
`.git/refs/remotes/origin/main`.

## 11. Lead decisions (18.11, Lead 501cb4e0, accepted)

- F1 (b) `path` and `path::symbol` for test-file carriers; no line numbers. F2 full key only. F3 (i) card B in `cmd_check`. F4 name the parts in the cells that name their siblings; drop `named_by` from the `data_join` row. F5 one move. F6 card B edits the TESTING.md clause (the Lead accepts the text at review). F7 `::symbol` only for test files under `scripts/tests/`.
- Order: card A, then card B after A merges.
