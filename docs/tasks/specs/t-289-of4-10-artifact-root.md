# t-289 — OF4-10: a broken project config never ends in a traceback or a pass at `hooklib.artifact_root()` and its callers; an `--output` inside `artifacts/` is no story (DRAFT, designer)

Status: DRAFT for Lead acceptance. The forks are in §9. Nothing here is decided for the Lead. Items marked `[F-n]` follow the
recommendation of that fork. The spec can be executed on the recommendations before the Lead answers (PROJECT.md «Командная
работа» item 11). If the Lead picks another option, the item is struck or swapped as §9 says.

Node: `onboarding-forge/4/OF4-10` (batch file `plans/piles/onboarding-forge/batch-4-hvosty-onbordinga-i-forzha.md:39`). Finding:
`plans/piles/onboarding-forge/findings/20261112-artifact-root-brosaet-na-bitom-konfige-a-vyzyvayushchie-lovyat-ne-to.md`.
Snapshot read: `C:\QAFactory\forge-repo\.claude\worktrees\oh7-5` (origin/main 0a0db4f). All line numbers below come from that snapshot,
read for this draft on 13.11.2026.

## Dispatch header (builder; rule 11 R11-f)

given: this spec (the enumeration is §0 and §2, one hop); `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md`; `docs/TESTING.md`; `ai-packages/qa-factory/design/architecture.md` (AR-4, AR-9, AR-12, AR-13, AR-15, AR-18, AR-24, AR-28, AR-29); `docs/SIBLING_MAP.md` axes 8, 16, 17, 32, 34; the finding above; `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` §4 rows :315-:318 and item 7 (:410-:447); the scripts `hooklib.py`, `config_contract.py` (:1321-:1374), `vcs_evidence.py`, `exit_gate.py`, `role_cli.py` (:134-:172), `source_exclusions.py` (:294-:331); the tests `test_read_json.py`, `test_vcs_evidence.py`, `harness.py` (:257-:318)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\hooklib.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\config_contract.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\vcs_evidence.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\exit_gate.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\tests\test_read_json.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\tests\test_vcs_evidence.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\changelog.d\of4-10-artifact-root.md
non-goals: the U rows of the census in §8 (they belong to residual node OF4-10r, fork F-11); `hooklib.is_one_component`, `hooklib.is_story_folder` and `exit_gate._named_ticket` (owned by OH6-1, t-282); `hooklib.load_config` (it keeps `{}`); `test-layers.json`; `judgment-census.json`; `references/*`; `driver_sources.py:356` (the hard-coded `qa-factory/artifacts/{task}` path, an analog in §8); `exit_gate.all_errors` (fork F-4 (b)); a new test file
handoff: the builder report (rule 7 of `.claude/agents/builder.md`) with the verbatim witness of §6, the FR walk, the `architecture:` and `judgment:` lines, and the list "needed beyond the manifest"
edges: §4 (table, with the invariant of each row) and §5 (positional invariants)
DoD: §6. The verification command is `python -B C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/hooklib.py ai-packages/qa-factory/scripts/config_contract.py ai-packages/qa-factory/scripts/vcs_evidence.py ai-packages/qa-factory/scripts/exit_gate.py ai-packages/qa-factory/scripts/tests/test_read_json.py ai-packages/qa-factory/scripts/tests/test_vcs_evidence.py ai-packages/qa-factory/changelog.d/of4-10-artifact-root.md`, then every file it prints (scope in §6)
siblings: axis 8 (the story on disk: `artifact_root`, the story predicate of `_story_root_of`); axis 16 (`artifact_root`'s own `json.loads` goes; the config is read by the one config reader); axis 17 (`unreadable_record` is the shape `grounding_errors` returns); axis 32 (census rows `hooklib.artifact_root`, `exit_gate.grounding_errors`); axis 34 (one road: one config reader, one story predicate for both recognitions); the other `artifact_root` callers are in §8 with a verdict each
designer: (Lead fills in at dispatch: the accepted draft's path)

## §0. Facts this draft rests on (each read in its carrier)

- F-1 `hooklib.artifact_root(event=None, root=None)` :691-706. The project is `root` or `project_root(event)`, resolved. The config is
  `<project>/qa-factory/config.json`. Line :697 reads it with its own `json.loads(config.read_text(encoding="utf-8-sig"))` when the file
  `exists()`, else `{}`. A non-object raises `ValueError` with a door (:698-699). A missing or `None` key gives
  `<project>/qa-factory/artifacts` (:701-702). A non-string or blank key raises `ValueError("artifact_root must be a non-empty path")`
  (:703-704), which has no door. Otherwise the value is resolved against the project (:705-706). Raw exceptions that escape today:
  `JSONDecodeError` (the text names no file), `UnicodeDecodeError`, `OSError` (a folder named `config.json`, no rights), and
  `RecursionError` on deep nesting, which is NOT a `ValueError`. The comment at :695-696 says the raise is intended (AR-28, AR-4).
  The finding says a JSON list gives `AttributeError` (finding :9). That is stale: :698-699 now raise `ValueError` for it.
- F-2 `config_contract.ConfigUnreadable(ValueError)` :1321 and `read_config_file(root)` :1349-1374 already exist. This is the config
  reader of the package (OF3-1 AR-13 row, t-129 :205: "config through `read_config_file`"). It returns None for an absent file. For a
  present file that cannot be read, it raises `ConfigUnreadable` with one door sentence: "fix the file by hand, or move it aside (...)
  and run onboarding again". The cases are OSError/UnicodeDecodeError :1361, an empty file :1365, not JSON :1368, not an object :1371.
  Gap: `json.loads` at :1367 can raise `RecursionError`, which the `except ValueError` at :1368 does not catch (fork F-3).
  `hooklib` already imports `config_contract` lazily at :2737. `config_contract` imports `hooklib` only lazily (:272, :939), so there
  is no import cycle at load.
- F-3 `role_cli.run_guarded` :134-172 turns a `ValueError` into `refuse(command, str(exc))` (:163-164). So every CLI that runs under
  `run_guarded` already prints a refusal, not a traceback, when the locator raises a `ValueError`. Today that refusal carries the raw
  text (`Expecting value: line 1 column 2 (char 1)`). An `OSError` gets the generic OS sentence (:170-172), and a `RecursionError` is
  not caught at all.
- F-4 `vcs_evidence._story_root_of` :581-604. Branch (1), the configured root, is OF3-1 d. It narrows to `<root>/<T>` only when
  `is_story_folder(root, T)` is true and `pipeline.json` is a file. It catches `(OSError, ValueError, AttributeError)` and falls
  through (:598-599). Branch (2), the path parts (:600-603), returns `Path(*parts[:index + 2])` for the deepest
  `qa-factory/artifacts/<x>` with NO story test. With `--output .../qa-factory/artifacts/x.json` it returns the FILE
  `artifacts/x.json` as the story. `left_out_by_person` then reads `artifacts/x.json/work/source-exclusions.json`, which is absent:
  `source_exclusions.read_record` :298-299 gives None, `live` :330-331 gives []. The result is None, so the tool reads, and the
  person's "do not read" word recorded in a real story is skipped. Proven by reading, not by running.
- F-5 `vcs_evidence.left_out_by_person` :607-649. When no story is known, :628
  `sorted_paths(p for p in Path(artifact_root()).iterdir() if p.is_dir())` sits inside `except OSError: return None` (:629-630).
  Today: (a) an invalid JSON, a list or a bad key raise `ValueError`, which escapes `main` as a traceback with exit 1. (b) A config
  that is a FOLDER raises `OSError` inside `artifact_root`, which :629 catches, so the result is None and the MR is read. That is a
  silent pass on an unknown, proven by reading. `main` :652-676 prints every refusal with `"status": "excluded"`,
  `"error": "left_out_by_person"` (:662-663). That includes the existing "record of the asking story is unreadable" refusal (:636),
  whose exclusion id is `""`.
- F-6 `exit_gate.grounding_errors` :1551-1618. Line :1560 resolves the ticket, through `_ticket_for_stage` (:754-770, whose
  `artifact_root()` at :759 is outside its try) when `task` is unknown. Line :1563 is `root = artifact_root() / ticket / "work"`
  outside any try. The "safe read" the finding means is :1569-1573 (`load_config` / `project_root` in a try). Census row:
  `judgment-census.json:288` (`grounding_errors`, class `shape`, owner `data`).
- F-7 `exit_gate.all_errors` :1828-1869 runs `scoped_errors` first, and `collect_errors` :1279 calls `artifact_root()` with no guard.
  So with a broken config `all_errors` raises before `grounding_errors` runs. All three callers of `all_errors` catch `Exception` and
  record an unknown: the hook `main` :1999-2008 (`_unreadable_stop`, exit 0), `driver_dispatch` :295-304 (`crash` leads to
  `gate_unreadable`), and `story_step` :2087-2092 (exit 2 `_gate_unreadable`). Inside `all_errors`, a broken config is therefore
  already an unknown, not a traceback.
- F-8 The hook tracebacks that ARE reachable with a broken config are outside `all_errors`:
  `exit_gate._identity` :287 `art_root = artifact_root()` sits outside the try at :292-299. It runs whenever the event carries no
  `input_fingerprint`, and it is called from `main` :1922 and from `subagent_journal` :207, so two hooks are affected. Second,
  `exit_gate.awaiting_source_review` :1519 calls `_ticket_for_stage("S1")` outside its try (:1522-1528), from `main` :1994, outside any
  try. With a broken config, `_identity` always yields `unknown-task` unless the event names the story (:255-273), so an S1 role's stop
  reaches :1519.
- F-9 Test homes, from `scripts/tests/test-layers.json` (the `quarantine` section starts at :7004): `test_read_json.py` :4083 is `keep`
  (layer `data_join`, covers `exit_gate.py` and `hooklib.py`, not `vcs_evidence.py`). `test_vcs_evidence.py` :6425 is `keep` (layer
  `detector`, covers `vcs_evidence.py`, named by `design/state-exits.md:192`). `test_exit_gate_grounding.py` :8026 is QUARANTINED, so
  it is never run, fixed or edited. Neither owned test file is quarantined, so no other home is needed. `test_judgment_census.py`
  :2708 is `keep`.
- F-10 `test_vcs_evidence.py` `ROOT_ROWS` :167-190 is the existing table of item 7, and the loop is :191-210. Its `story()` helper :40-47
  builds `qa-factory/artifacts/<T>/work` WITHOUT `pipeline.json`. The rows at :77, :104, :109 and :144 rely on branch (2) naming such
  a folder. `test_read_json.py` :598-693 holds `CONFIG_STATES` × `SITES` (GW1-38). Its `_site_report_adapt` :631-637 pins the project
  by patching `hooklib.project_root`, which is the precedent for the drivers here.
- F-11 Dependency "after the OF3-1 merge". `git log --grep OF3-1` was NOT run: this designer has no shell tool. Indirect evidence:
  (a) the main snapshot carries OF3-1 d's code: `vcs_evidence.py:581-604` configured-root recognition, `env_probe.py:693`
  "(OH1-6, AR-4)", `execution_scheduler.py:359`/`:577` "F12"; (b) `.git/logs/refs/heads/pile/onboarding-forge/batch-3` records merges
  of `wip/of3-1b`, `of3-1d`, `of3-1e`, and `conv/accepted-nodes` merges `origin/wip/of3-1c`; (c) OF4-22 ("после слияния OF3-1") is
  `принято: 073bca8`. **Estimate, not verified.** The Lead runs
  `git -C C:\QAFactory\forge-repo log refs/remotes/origin/main --oneline --grep OF3-1` before dispatch. Note that batch 3 still reads
  `в работе` in `plans/PILES.md:88`.
- F-12 Concurrent nodes. OH6-1 (`docs/tasks/specs/t-282-oh6-1-one-component.md` §7 :185-192) owns `hooklib.is_one_component`,
  `hooklib.is_story_folder`, `exit_gate._named_ticket`, and a new top-level `import hooklib` line beside `exit_gate.py:31/:39`.
  OF4-26 (`batch-4…md:55`, `ожидает`) also owns `scripts/tests/test_read_json.py`.

## §1. Architecture, owners, census (designer rule 1; CLAUDE.md rule 10)

| AR-n | how this node touches it | change check, written into the DoD |
|---|---|---|
| AR-28 an unknown never becomes a pass | a broken config becomes a refusal with a door (`left_out_by_person`, writers) or an `unreadable` record (`grounding_errors`). It is never `None` / `[]` / a default folder. F-5 (b) silent pass closed | DoD 3: the §7 rows "broken × site" read `refused` / `unreadable`, never the pass value. Each new read's behaviour on missing / unreadable / empty is stated in §4 |
| AR-9 every refusal names what it expected and a door | ONE refusal text for the whole class: `ConfigUnreadable` (what is wrong, what was expected, the door: fix the file or move it aside and re-onboard). `left_out_by_person` adds the role's own door (`--output` under the story folder, or say so in the handoff) | DoD 5: `python -B scripts/refusal_registry.py --check` green. If it names a new site, the builder RETURNS the question (A24 row, `controller-blocks.md`), because neither is in owns |
| AR-13 a fact with a reader is read only through it | `artifact_root` stops parsing `config.json` itself and reads it through `config_contract.read_config_file` [F-1] | DoD 4: `grep -n "json.loads" scripts/hooklib.py` (positive control: `read_json` :765 must hit) shows no hit in `artifact_root`; `test_read_json.py` G5 census green |
| AR-15 one survivor | one exception class and one text for "config unreadable" (`ConfigUnreadable`); one story predicate `_story_at` for both recognitions of `_story_root_of` | DoD 4: every site of §8 is listed with its verdict (done in this spec; the builder re-runs the grep with the positive control `def artifact_root`) |
| AR-18 one output shape | `grounding_errors` returns the existing `unreadable_record` (a `DV.Record`, kind `unreadable`) | DoD 5: `test_detector_verdict.py` green if `--witness-for` prints it; no new parser |
| AR-24 a person's words reach whatever acts on them | the "do not read this MR" word is never skipped: not by a file in `artifacts/`, not by a plain folder, not by a broken config | §7 rows V1-V3, V4-V8 |
| AR-4 nothing tied to one layout | a configured `artifact_root` keeps being honoured; an outside path stays legal [F-7] | §7 row "outside" |
| AR-29 a code check judges data | no check judges a role's content; owners and classes are in the table below | DoD 5: `test_judgment_census.py` green with no row added, removed or raised. If C1 names a unit, the builder RETURNS the question with the class below (the census file is not in owns) |
| AR-12 friction | hooks now import `config_contract` lazily on every `artifact_root` call [F-1 (a)] | report line: `code_friction` "not measured"; plus the one import-time measurement of fork F-1 (Lead, before acceptance) |

Every check the node adds or alters, with the owner it serves and its census class:

| check (file: function) | added / altered | owner it serves | census class | census row |
|---|---|---|---|---|
| `hooklib: artifact_root`: a present config that cannot be read, or a bad `artifact_root` value, raises `ConfigUnreadable` | altered (text and class of the raise; same direction) | data (code: where the story folders are) | shape | existing `judgment-census.json:398`, unchanged |
| `config_contract: read_config_file`: nesting too deep for the parser raises `ConfigUnreadable` [F-3] | altered | data | shape | the builder checks with `test_judgment_census.py` whether a row exists; no class change |
| `vcs_evidence: left_out_by_person`: no story known and the root cannot be found leads to a refusal | added (a new refusal branch) | intent: the person's recorded "do not read" word | safety (it protects the person's words, AR-29 last sentence) | none today for this function; if C1 asks for one, the builder returns the question |
| `vcs_evidence: _story_root_of` / `_story_at`: narrows only to a real story | altered (branch (2) gains the predicate) | intent (the same word; the error direction protects it) | shape (presence of a folder and its marker) | not a refusal unit; no row expected |
| `exit_gate: grounding_errors`: root unknown leads to one `unreadable` record | altered | data | shape | existing `:288`, unchanged |
| `exit_gate: _identity` / `awaiting_source_review` (fork F-4) | altered (no raise) | data | not a check (a key / an identity read) | none |

FR walk (PROJECT.md acceptance item 1, the sections touched): A: FR-1, FR-2, FR-4, FR-46 (the class stays `ValueError`), FR-57.
C: FR-14 (the stdout shape of `vcs_evidence`). D: FR-59. E: FR-41 (a stdout status that is unknown is not reported as `excluded`
[F-5]). G: FR-30, FR-32. B: no text a person reads changes, so one line in the report.

## §2. Per caller: current line, current behaviour, new behaviour, error direction

### 2.1 `hooklib.artifact_root` :691-706 (the locator; hot file)

Current behaviour on a broken config: F-1.

New behaviour:
1. The config is read by `config_contract.read_config_file(project)` [F-1 (a): `import config_contract` inside the function]. None
   (no file) becomes `{}`, the default world. A present file that cannot be read raises `ConfigUnreadable` with its own text.
2. A `RecursionError` is a `ConfigUnreadable` too. [F-3 (a): fixed inside `read_config_file`, the survivor. Under F-3 (b), the same
   wrapping sits in `artifact_root`.]
3. The value is `cfg.get("artifact_root")`. `None` (absent or JSON `null`) gives `<project>/qa-factory/artifacts`, as today [F-8]. Any
   other non-string, a blank string, or a string with `\x00` raises
   `ConfigUnreadable("qa-factory/config.json: `artifact_root` must be a non-empty folder path (got <type name or 'a blank string'>). Remove the key to keep the story folders in qa-factory/artifacts, or set it to a folder path.")`.
   The value itself is not echoed, so a byte of it never reaches a refusal.
4. `(path if absolute else project / path).resolve()`. An `OSError` or `ValueError` from `resolve` becomes a `ConfigUnreadable` with
   the same sentence.
5. The comment at :695-696 stays in substance: a broken config raises here and never becomes the default folder.

Error direction: refuse. The locator may refuse a config a person would call fine. That can only happen with a blank, NUL or
non-string value, and in each case the text names the key and the fix. It never returns a folder after a read or parse failure.
Adversarial inputs that must stay on the refusing side: an empty file; a whitespace-only file; a BOM-only file; `{not json`; `{} x`
(trailing garbage); `[1, 2]`; `[]`; `"str"`; `null`; non-UTF-8 bytes; `"[" * 300000`; a folder named `config.json`; and for the key:
`""`, `"   "`, `5`, `["a"]`, `{}`, `"a\u0000b"`.

A reused function in a new, more consequential role (designer rule 1): `read_config_file` used to serve onboarding and the doctor.
Now it decides the artifact root for every writer, hook and reader. It may err only toward `ConfigUnreadable` for a present file.
None means "no file" only, and nothing that exists becomes None or `{}`. A dangling symbolic link named `config.json` reads as absent
(`Path.exists()` is false). That is today's behaviour too and is kept; it is listed as an analog in §8.

### 2.2 `vcs_evidence._story_root_of` :581-604

Current behaviour: F-4. Broken config: branch (1) is skipped and branch (2) still names `qa-factory/artifacts/<x>` for any `<x>`, a
file included.

New behaviour: one private predicate `_story_at(parent, name) -> Path | None`. It returns `parent / name` when
`hooklib.is_story_folder(parent, name)` is true AND `(parent / name / "pipeline.json").is_file()`. Any `OSError` or `ValueError` gives
None. Branch (1) calls it, which keeps today's semantics. Branch (2) calls it for the deepest `qa-factory/artifacts/<T>` whose
`--output` lies BELOW `<T>`, so at least one part follows `<T>`, mirroring (1). If the deepest match is not a story, the answer is
None, and no outer match is tried.

Error direction: "not a story", which leads to every story being consulted. It never names a file, a plain folder, a folder without
`pipeline.json`, an alias, or a missing folder. Adversarial inputs: `artifacts/x.json`, `artifacts/maintenance/x.json` (a real
non-story folder, `factory_dashboard.py:493`), `artifacts/S-2/x.json` where S-2 has no `pipeline.json`, `artifacts/S-2 /x.json`, a
case variant, `artifacts/S-2/../tmp/x.json` (resolved first), and `--output` equal to `artifacts/S-2` itself.

### 2.3 `vcs_evidence.left_out_by_person` :607-649

Current behaviour: F-5.

New behaviour: a story is known (`_story_root_of` not None) means its own list is consulted, as today. That needs no artifact root,
so a broken config does not matter. No story known means `root = artifact_root()` inside
`try ... except (OSError, ValueError) as exc`, which returns
`(2, "vcs_evidence: " + str(exc) + " No story is named by --output, so the list of sources the person left out must be read for every story, and the story folders cannot be found: nothing was fetched. Run it with --output under the story's own folder (qa-factory/artifacts/<story>/work/), or say so in your handoff.", "")`.
Then the listing is made. `FileNotFoundError` or `NotADirectoryError` (no story folder at all) returns None, as today. Any other
`OSError` returns a refusal of the same form that names the folder that could not be listed [F-6].

Error direction: toward not reading. The cost is that a broken config refuses a probe-only read even when nobody recorded anything.
The door is the `--output` of a story, the handoff, or fixing the file. Adversarial inputs: every broken state of 2.1, a folder named
`config.json`, probe-only, and `--output` outside every story.

### 2.4 `vcs_evidence.main` :652-676

Current: every refusal prints `"status": "excluded"`. New [F-5 (a)]: a refusal whose exclusion id is empty is "could not check". It
prints `{"url", "status": "unknown", "error": "not_checked", "exclusion": "", "fetched": false}`. This holds for the broken config and
equally for the existing unreadable-record refusal at :636. A refusal with an id keeps `excluded` / `left_out_by_person` unchanged.
Exit code 2 in both cases. stderr carries the text.

Readers of the stdout: in the package, `driver_sources.py:355-363` runs the tool and reads the RECEIPT FILE (absent in both cases),
not the stdout status, and roles read the stdout. A complete census of subprocess readers was not made: this is an estimate, and the
builder greps `"vcs_evidence.py"` with the positive control `driver_sources.py:355`.

### 2.5 `exit_gate.grounding_errors` :1551-1618

Current: F-6, F-7.

New: right after the role check (:1558-1559), and before the ticket is resolved (:1560) and before the register is tested (:1565),
the ticket resolution and `artifact_root()` go inside
`try ... except (OSError, ValueError) as exc: return [unreadable_record("grounding_errors", f"the story folders could not be found ({exc})", "requirements-register.md")]`.
The rest is unchanged. `import hooklib` stays local, and no top-level import is added (D-0048, §3).

Error direction: unknown, never `[]`. `[]` meaning "no register" is reachable only after the root was read. Another role keeps `[]`.

### 2.6 `exit_gate._identity` :287 [F-4] and `exit_gate.awaiting_source_review` :1519 [F-4]

Current: F-8, which leaves hook tracebacks in two hooks.

New: in `_identity`, `art_root = artifact_root()` and the `scan_root` lines :287-290 move inside the existing try at :292-299. On an
exception, `file_state = []`, and every other field of the scope and the key stays as computed. In `awaiting_source_review`, the
ticket resolution :1519-1521 moves inside the existing try at :1522-1528, so an exception returns `False`.

Error direction: `_identity` gives a fingerprint without the artifact state. This is harmless because the fuse holds only
`blocked` / `incomplete` (:1982), and with a broken config the gate's own status is `unreadable` (F-7). `awaiting_source_review`
errs toward `False`, so the gate runs and records the unknown. It never records `awaiting_human` on an unknown.

### 2.7 The writers

Current: F-3. A writer under `run_guarded` prints a refusal with the raw text. A writer outside it prints a traceback.
`execution_scheduler.py:359`/`:577` raise on purpose (OF3-1 F12).

New: through 2.1 alone, every writer under `run_guarded`, and every site that catches `ValueError` or `Exception` and prints
`str(exc)`, prints the ONE finished text (FR-1, AR-9). That is one road and needs no per-caller edit [F-12]. The `RecursionError` and
`OSError` cases now arrive as `ValueError`, so `run_guarded` gives them the same refusal. The writers outside `run_guarded` still
print a traceback, and the last line is now the finished text. They are the U rows of §8, and their entry points are residual node
OF4-10r [F-11].

Error direction: a writer refuses before it reads, creates or launches anything (F12 unchanged). It never falls back to the default
folder.

## §3. Hot files: D-0048 function lists

| file | hot | functions this node touches | outside a function | the concurrent node's list (disjoint) |
|---|---|---|---|---|
| `scripts/hooklib.py` | yes | `artifact_root` | none | OH6-1: `is_one_component`, `is_story_folder` |
| `scripts/exit_gate.py` | shared with OH6-1 | `grounding_errors`; `_identity` and `awaiting_source_review` [F-4] | none (no new top-level import; `grounding_errors` already imports `hooklib` locally :1568) | OH6-1: `_named_ticket`, plus one top-level `import hooklib` beside :31/:39 |
| `scripts/vcs_evidence.py` | no | `_story_root_of`, new `_story_at` (directly above it), `left_out_by_person`, `main` | none | — |
| `scripts/config_contract.py` | no | `read_config_file` [F-3] | none | the Lead checks that no open node owns it |
| `scripts/tests/test_read_json.py` | no | a NEW function `test_the_artifact_root` after `test_the_config_readers`, and one call line in `__main__` | the new tables `ROOT_STATES`, `ROOT_SITES` placed beside that function | OF4-26 (`ожидает`) owns this file too. This node does not touch `SITES` / `CONFIG_STATES` / `test_the_config_readers` |
| `scripts/tests/test_vcs_evidence.py` | no | `story()` (writes `pipeline.json`), `ROOT_ROWS` and its loop | — | — |

`_identity` calls `_named_ticket` at :270, but this node edits only :287-299. The hunks are far apart.

## §4. Edges, each with the invariant it protects

| # | input | behaviour | invariant (what must stay unreachable or refused) |
|---|---|---|---|
| E1 | config absent (no file; not onboarded) | `artifact_root` gives `<project>/qa-factory/artifacts`. `left_out_by_person` with no story and no such folder gives `FileNotFoundError`, then None, so it reads as today. `grounding_errors` gives `[]` when there is no register | absent ≠ unreadable: absent never refuses, unreadable never reads as absent |
| E2 | config unparsable: `{not json`, `{} x`, non-UTF-8 bytes, `"[" * 300000` | `ConfigUnreadable`, then: writer refusal; `left_out_by_person` (no story) refusal with exit 2; `grounding_errors` returns `unreadable` | no default folder, no `None`, no `[]` after a failed read; a `RecursionError` never escapes as a non-`ValueError` |
| E3 | config not an object: `[1, 2]`, `[]`, `"s"`, `null`, `5` | as E2 (the text names the JSON type, `read_config_file` :1372-1373) | as E2 |
| E4 | config empty: a 0-byte file, whitespace only, BOM only | as E2 ("is empty", :1365) | an empty file is unreadable, never "no config" |
| E5 | a folder named `config.json`, or a file without read rights | as E2. F-5 (b) silent pass closed | an `OSError` of the config never reaches an `except OSError` that means "no folder" |
| E6 | key of a wrong type: `5`, `["a"]`, `{}`, `true` | `ConfigUnreadable` naming `artifact_root` and the fix | a value that is not a non-empty string never becomes a path |
| E7 | key empty: `""`, `"   "` | as E6 | an empty key never becomes the project folder (`project / ""`) |
| E8 | key with `\x00` | as E6 (an explicit test, not left to `resolve`) | one answer on every platform |
| E9 | key `null` | the default folder [F-8] | only a non-empty string names another folder |
| E10 | key a path outside the project (`"../outside"`, an absolute path on another drive) | accepted and resolved, as today [F-7]. `_story_root_of` (1) narrows only below that root | a configured root is honoured (AR-4); an outside root never widens or narrows anything but its own stories |
| E11 | `--output` directly in `qa-factory/artifacts/` (`artifacts/x.json`) | not a story, so every story is consulted, and a recorded word refuses | a file is never a story; the word is never skipped |
| E12 | `--output` under a folder of `artifacts/` without `pipeline.json` (`maintenance/`, a half-made story) | not a story, so every story is consulted | a narrowed consultation is reached only for a real story |
| E13 | `--output` under a real story of the old default folder (`pipeline.json` present) | the story is named; its own list is consulted | the narrowing that works today keeps working |
| E14 | `--output` equal to the story folder itself (`artifacts/S-2`) | not named (nothing below `<T>`), so every story is consulted | the same rule as branch (1) (`len(parts) >= 2`) |
| E15 | broken config, story known by branch (2) | its own list is consulted, so it reads unless the word refuses (existing rows :186, :188) | a known real story needs no artifact root |
| E16 | broken config, probe-only or `--output` outside every story | refusal, exit 2, nothing fetched, stdout `status: unknown` [F-5] | an unknown root is never `None` |
| E17 | the artifact root cannot be listed (`PermissionError`) | refusal naming the folder [F-6] | only "no folder" means "nothing recorded" |
| E18 | a broken config at an S1 role's stop (no `input_fingerprint`, no task in the event) | hook exit 0 with `gate_unreadable` and the crash text; no traceback [F-4] | a hook never ends in a traceback on a broken config |
| E19 | `grounding_errors` for a role other than `qa-requirements-tester`, broken config | `[]` | a role is never judged by a check that is not its own |
| E20 | the change brings nothing into existence (no file, flag or config) | no temporal edge: `ConfigUnreadable` and `read_config_file` exist today | — |
| E21 | limits | the node adds none. The parser's nesting limit is a BEYOND row (E2 deep). An AT row does not apply: the limit is Python's, not ours | — |

Conflicting requirement pairs, resolved:
- "Never a traceback" against OF3-1 F12 "writers raise on purpose": writers still raise, now with the finished text. Whether a
  traceback is printed is decided by the entry point (`run_guarded` refuses). The remaining entry points are OF4-10r [F-11].
- "An unknown is never a pass" against "probe-only works on a project with no stories": absent leads to E1 (reads), broken leads to
  E16 (refuses).
- Branch (2) gaining the `pipeline.json` marker against the old fixtures without it: the fixture `story()` writes `pipeline.json`, as
  S0 does for every real story. That claim comes from the marker of branch (1) (t-129 F-6b), not from a fresh read of S0's writer:
  estimate.

## §5. Positional invariants (rule 11 (ii))

- P1 `artifact_root`: the config read comes first. The default folder is returned ONLY when the file is absent or the key is
  absent/`null`, and never after an exception of the read, the parse, the key check or `resolve`.
- P2 `_story_root_of`: the order is (1), then (2), then None. Both branches decide through `_story_at` alone. Any exception inside (1)
  falls to (2), and any inside (2) falls to None. A narrowed answer is unreachable unless `_story_at` returned a folder.
- P3 `left_out_by_person`: the import guard (:621-625) stays first and unchanged. `_story_root_of` comes next. The config guard sits
  ONLY on the no-story branch, before the listing. A known story's own list is consulted without touching the root. With no story,
  an unknown root is a refusal, and `None` is unreachable from any exception except "no folder".
- P4 `vcs_evidence.main`: `"status": "excluded"` is printed only when the exclusion id is non-empty [F-5].
- P5 `grounding_errors`: the guard comes after the role check and before `_ticket_for_stage` and before `register.is_file()`. Another
  role still gets `[]`. "No register" `[]` is unreachable when the root was not read.
- P6 `_identity` [F-4]: only the file-state scan is inside the try. `task`, `dispatch`, `attempt`, `hook` and `agent` are computed
  exactly as today, and no exception from :287 leaves the function.
- P7 `awaiting_source_review` [F-4]: `True` is unreachable unless the source inventory was read.

## §6. DoD

Acceptance criteria:
1. §2 is implemented in the owned files only, inside the §3 function lists.
2. The §7 table exists as specified: one new table in `test_read_json.py`, and new rows in the existing `ROOT_ROWS` of
   `test_vcs_evidence.py`. The existing rows of both files keep their expected values. In `test_vcs_evidence.py` this holds AFTER
   `story()` writes `pipeline.json`, and any row whose expectation would change is returned as a question, not edited.
3. No row of §7 shows a traceback or an exception class other than the expected one. Every "broken" cell is `refused` / `unreadable`,
   never a pass value.
4. `grep -n "json.loads" ai-packages/qa-factory/scripts/hooklib.py` has no hit inside `artifact_root`. The positive control is the hit
   in `read_json`. `grep -n "artifact_root(" ai-packages/qa-factory/scripts --include=*.py` (positive control: `def artifact_root`)
   returns the §8 list plus nothing new, and any new call site is a report line.
5. AR detectors: `python -B <wt>\ai-packages\qa-factory\scripts\tests\test_judgment_census.py` and
   `python -B <wt>\ai-packages\qa-factory\scripts\refusal_registry.py --check` are green and unchanged. A unit or site they name is
   returned as a question.
6. Commit message: `architecture: AR-28, AR-9, AR-13, AR-15, AR-18, AR-24, AR-4, AR-29, AR-12 -- <how kept, one clause each>`, a
   `judgment:` line (`none -- the artifact_root and grounding_errors rows keep class shape, owner data`, unless DoD 5 says otherwise),
   the FR walk of §1, and `code_friction: not measured`.
7. The changelog fragment `changelog.d/of4-10-artifact-root.md`, in English: what a person sees when `config.json` is broken.

Verification run (`plans/builder-rules.md` 7b): the command on the `DoD:` line. Then each file it prints, as
`python -B <wt>\ai-packages\qa-factory\scripts\tests\<file>.py`, except a quarantined file and the big files 7b excludes
(`test_story_step.py`, `test_story_run_*`). Each skipped file is a report line. The printed set is large because `hooklib.py` is in
every scenario closure (the same note as t-282 F-5). The output is pasted verbatim. `<wt>` = `C:\QAFactory\forge-repo\.claude\worktrees\of4-10`.

## §7. The parameterised test table

### T1, new: `test_read_json.py` `test_the_artifact_root(scratch)`. `ROOT_STATES` × `ROOT_SITES`, one `check_eq` per cell, row id `OF4-10 <site> x <state>`

`ROOT_STATES` (the bytes written to `<root>/qa-factory/config.json`; `None` means no file; `DIR` means a folder of that name):
`absent` None · `no_key` `{"schema_version": 1}` · `key` `{"artifact_root": "stories"}` · `bom_key` BOM + `key` · `null_key`
`{"artifact_root": null}` · `outside` `{"artifact_root": "../outside"}` · `empty_file` `b""` · `blank_file` `b"   "` · `invalid`
`{not json` · `list` `[1, 2]` · `latin1` `{"artifact_root": "\xe9"}` as raw bytes · `deep` `DEEP` (:51) · `dir` DIR · `key_empty`
`{"artifact_root": ""}` · `key_blank` `{"artifact_root": "   "}` · `key_number` `{"artifact_root": 5}` · `key_list`
`{"artifact_root": ["a"]}` · `key_nul` `{"artifact_root": "a\u0000b"}`.

`ROOT_SITES` (each driver returns a token; any other exception returns `crash:<Type>`, so the cell shows red):
- `locator`: `hooklib.artifact_root(root=root)`. Returns its POSIX path relative to `root`, else `outside:<name>`, or `refused` when it
  raises `ConfigUnreadable` whose text contains `config.json`.
- `writer`: `role_cli.run_guarded("of4-10 writer", lambda: (hooklib.artifacts_dir("S-1"), 0)[1], stream=buf)` with the project pinned
  by patching `hooklib.project_root` (precedent :631-637). Returns `ok` on 0, or `refused` on `EXIT_REFUSED` with `config.json` (or
  `artifact_root` for the key states) in `buf` and no `Traceback`.
- `grounding`: a story `S-1` with `work/requirements-register.md` at `qa-factory/artifacts/S-1` AND at `stories/S-1`, the project
  pinned the same way. `exit_gate.grounding_errors("qa-requirements-tester", "S-1")` returns `[]`, or `unreadable` when the answer is
  exactly one record of kind `unreadable` whose text contains `grounding_errors: unreadable`.

Expected:

| state | locator | writer | grounding |
|---|---|---|---|
| absent, no_key, null_key | `qa-factory/artifacts` | `ok` | `[]` |
| key, bom_key | `stories` | `ok` | `[]` |
| outside | `outside:outside` | `ok` | `[]` |
| empty_file, blank_file, invalid, list, latin1, deep, dir, key_empty, key_blank, key_number, key_list, key_nul | `refused` | `refused` | `unreadable` |

Plus one check: "every site has a cell per state". Writer and grounding pin the project by patching, not through
`CLAUDE_PROJECT_DIR`, because `absent` and `dir` carry no marker file, and `project_root` would walk to another project (`hooklib.py:35-41`, :98-104).

### T2, rows added to the existing `test_vcs_evidence.py` `ROOT_ROWS` (:167-190)

The tuple gains an 8th column `needle` (text stderr must contain; `""` means no check), and `output` may be `None` (no `--output`,
probe-only). For exit 2 with a needle, the loop also checks the stdout `status == "unknown"` [F-5 (a); under F-5 (b): `excluded`] and
that `calls == []`. The existing rows get `needle = ""`.

| id | config | stories at | S-2 marker | output | exit | needle |
|---|---|---|---|---|---|---|
| V1 an output file directly in the old default folder: every story consulted | `{}` | `qa-factory/artifacts` | yes | `qa-factory/artifacts/x.json` | 2 | — |
| V2 a folder of the old default folder without pipeline.json: every story consulted | `{}` | `qa-factory/artifacts` | no | `qa-factory/artifacts/S-2/work/x.json` | 2 | — |
| V3 a real story of the old default folder is still named | `{}` | `qa-factory/artifacts` | yes | `qa-factory/artifacts/S-2/work/x.json` | 0 | — |
| V4 broken config (bad JSON), output outside every story: refused, the config named | `{not json` | `qa-factory/artifacts` | yes | `tmp/x.json` | 2 | `config.json` |
| V5 broken config (a JSON list), output outside every story | `[]` | `qa-factory/artifacts` | yes | `tmp/x.json` | 2 | `config.json` |
| V6 empty artifact_root, output outside every story | `{"artifact_root": ""}` | `qa-factory/artifacts` | yes | `tmp/x.json` | 2 | `artifact_root` |
| V7 broken config, probe-only | `{not json` | `qa-factory/artifacts` | yes | None | 2 | `config.json` |
| V8 an empty config file, probe-only | `` (0 bytes) | `qa-factory/artifacts` | yes | None | 2 | `config.json` |

V1 and V2 read `0` today (F-4). V4-V8 end in an exception today (F-5 (a)). Under F-6 (a), one more row is possible only with a
platform-portable unlistable folder. None is known, so E17 is pinned by reading only, which is a report line.

## §8. Every `artifact_root(` call the grep finds, with a verdict

Grep: `artifact_root\(` over `ai-packages/qa-factory` excluding `tests/`, run in the snapshot: 120 lines in 51 files. The positive
control is `hooklib.py:691 def artifact_root`. The 197 matches of `artifact_root\(|artifacts_dir\(` include `artifacts_dir`, whose
callers are TRANSITIVE and belong to the census of OF4-10r. Legend:
- E: edited here.
- C: the call sits inside an `except` that catches `ValueError` or `Exception`, verified by reading the lines. The direction is
  unchanged, and the text now names the file.
- P: it propagates into `all_errors`, whose three callers catch `Exception` (F-7), so it ends as an unknown with no traceback.
- L: a hooklib resolver; it propagates by design to its caller.
- F12: a writer that raises on purpose.
- X: not a call (a definition, docstring or comment).
- U: not verified at site level, classified by line text only. It goes to OF4-10r.
- Uc: a catch claimed by an accepted spec or node, not re-read here.

| file: lines | verdict |
|---|---|
| hooklib :282 `artifacts_dir` | L |
| hooklib :378 `story_root` | L |
| hooklib :397 `_example_folder` | C (`except (OSError, ValueError)` :398) |
| hooklib :359, :691 | X |
| vcs_evidence :628 | E (2.3) |
| vcs_evidence :593 | C (:598) |
| vcs_evidence :584 | X |
| exit_gate :1563 (and :1560 through :759) | E (2.5) |
| exit_gate :287 | E [F-4] (2.6) |
| exit_gate :759 `_ticket_for_stage` | callers: `_identity` C (:255-266); `grounding_errors` E; `awaiting_source_review` :1519 E [F-4] |
| exit_gate :207 `_named_ticket` | C (called in the try :269-272; OH6-1 owns the function) |
| exit_gate :816, :818 | C (:814-820) |
| exit_gate :1161 | C (:1160-1164) |
| exit_gate :1201 | C (:1200-1202) |
| exit_gate :1257 | C (:1255-1258) |
| exit_gate :1461 | C (both callers in a try: :255-266, :1486-1506) |
| exit_gate :1499, :1500 | C (:1486-1506) |
| exit_gate :1512 | C (called in the try :1856-1858) |
| exit_gate :1524 | C (:1522-1528) |
| exit_gate :120, :677, :903, :1063, :1109, :1124, :1125, :1253, :1279, :1366, :1405, :1431, :1666 | P |
| exit_gate :165, :167, :181 | P: reached from `main` :2041 only after `all_errors` returned, which a broken config prevents (it raises at :1279 first) |
| guard_pre_tool :609, :738, :1395, :1535 | C (the excepts :620, :744, :1402, :1536) |
| guard_pre_tool :2269 | U, hook path, no try in :2265-2271: a likely traceback (OF4-10r, priority) |
| guard_app_under_test :265 | C (:266-267, fail-closed) |
| waiver :1160, :1168 | C (`except (OSError, ValueError)` :1171) |
| execution_scheduler :359, :577 | F12 |
| execution_scheduler :156 | U |
| dispatch_liveness :771 | Uc (OF4-22 accepted 073bca8: "broken config, `unknown`") |
| env_probe :693 | Uc (OF3-1 c reader catch, t-129 item 7) |
| role_load :538 | Uc (OF3-1 d) |
| local_keys :131 | Uc (OF3-1 d) |
| local_keys :70 | U |
| gate_shown :186 | Uc (its docstring: "`artifact_root` raises on a broken config: `main` says so"; `main` not re-read) |
| inject_context :325, :330 | Uc (indented inside a block that looks guarded; not re-read) |
| run_suite :3037 | U (the try catches `MineRefusal` only: a likely traceback) |
| collect_pack :489 (a method call), :501 | U |
| collect_pack :494 | X (a method named `_artifact_root`) |
| controller :2491 | U |
| controller :2481 | X |
| red_sandbox :133, :1412 | U |
| red_sandbox :126 | X |
| host_dispatch :23 | U (`read_json(..., errors=Exception)` is evaluated after `artifact_root` raises; reached from `read_event` → `enrich`, whose `except Exception` returns None, i.e. "fail closed" for every guard; an analog) |
| stage_guard :463, :600, :1375, :1421, :1570, :1668, :1692, :1834, :2996 | U (the hook library; a crash in a PreToolUse guard may ALLOW a dispatch, compare the comment at :484) |
| archive_task :146, :194, :235; baseline_contract :66; audit_factory :454, :528, :586, :1502, :1514; check_coverage :97; dashboard_refresh :30; driver_journal :346; estimate_record :44; factory_dashboard :400, :475, :493, :675, :1029, :1245, :3061, :3915; execution_request :3246, :3248, :3252, :3253, :3258, :3260, :3262, :3265, :3267, :3881; planning_contract :362; probe_by_code :4750, :6959, :7799; runtime_paths :731; source_exclusions :540; stand_identity :178, :210; traceability :1842; validate_artifacts :356 (P when reached through `all_errors`); window_budget :301 | U |

Analogs noticed and reported, not widened (rule 9):
- (a) `vcs_evidence.left_out_by_person` :621-625: an import failure gives `None`, "feature absent". That is a pass on an unknown,
  kept as written (P3).
- (b) `driver_sources.py:356` writes `--output qa-factory/artifacts/{task}/...` with a literal path, not through `artifact_root`
  (axis 8). With a configured root it is still named, by branch (2) (E13), but only while the story also exists in the old folder.
- (c) A dangling symbolic link named `config.json` reads as absent (2.1).
- (d) `host_dispatch:23`: a broken config makes `read_event` return None for every hook.
- (e) `stage_guard` crash, so a possible ALLOW.

(d) and (e) are hook-safety questions for OF4-10r.

## §9. Forks (each with a recommendation; the Lead decides)

- **F-1 How `artifact_root` reaches the config reader.**
  - (a) `import config_contract` inside `artifact_root` and call `read_config_file`. This is one road, and its cost is the import of a
    ~3,000-line module once per hook process. `guard_pre_tool` runs on every tool call, and it imports `config_contract` only on one
    branch (:1587).
  - (b) Move `ConfigUnreadable` and `read_config_file` into `hooklib`, and have `config_contract` re-export them (the same objects).
    This has no import cost, but the diff in the hot file grows and `config_contract.py` gets a one-line re-export.
  - (c) Keep `artifact_root`'s own `json.loads` and copy the texts. That is a second parser of the same bytes, an AR-13 breach and a
    second road (P31).

  **Recommendation: (a)**, after ONE measurement by the Lead before acceptance (CLAUDE.md hygiene 6a):
  `python -X importtime -B -c "import sys; sys.path.insert(0, r'C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts'); import config_contract"`.
  If the import adds noticeable latency per hook call (the threshold is the Lead's word), take (b). A judgment is needed here, so I
  did not pick a number.
- **F-2 The finding's own owner question**: "one wrapper in hooklib, or a catch at each caller". It is replaced by F-12 below and kept
  here only so that the question is closed by name.
- **F-3 The `RecursionError` gap of the survivor.**
  - (a) Fix it in `config_contract.read_config_file`. `config_contract.py` joins owns, and every reader of the survivor gains the
    fix.
  - (b) Catch it in `artifact_root` only. That leaves the survivor's other readers (onboarding, the doctor,
    `import_test_receipt`) with a raw `RecursionError`.

  **Recommendation: (a)**, the one road. The cost is one more owned file. The Lead confirms that no open node owns
  `config_contract.py`.
- **F-4 How far into `exit_gate` this node goes.**
  - (a) `grounding_errors` (the batch row), plus `_identity` :287 and `awaiting_source_review` :1519. These are the only places where
    a broken config ends in a real hook TRACEBACK (F-8), and two hooks (`exit_gate`, `subagent_journal`) are cured by the
    `_identity` edit.
  - (b) (a) plus a front probe in `all_errors` that returns one typed `unreadable` record instead of a "gate crashed" text, which is
    cleaner for the person.
  - (c) `grounding_errors` only, the letter of the batch row. The hook traceback stays. And `grounding_errors`' new record is never
    seen in a real stop, because `collect_errors` raises first (F-7).

  **Recommendation: (a).** It widens the batch row's `exit_gate.py (grounding_errors)` by two functions, both disjoint from OH6-1.
  (b) costs one more function and changes the text of every gate crash, which is a separate decision.
- **F-5 The stdout of `vcs_evidence` on a refusal that checked nothing.**
  - (a) A refusal with an empty exclusion id prints `status: unknown`, `error: not_checked`. This covers the broken config AND the
    existing unreadable-record refusal :636, which is one road for "could not check".
  - (b) Keep `status: excluded` for both. There is no contract change, but an unknown is printed as if it were the person's
    exclusion (FR-41).

  **Recommendation: (a).** No code reader of this stdout status was found (`driver_sources` reads the receipt file). The census of
  subprocess readers is an estimate, and the builder re-greps it.
- **F-6 A root that exists but cannot be listed** (`PermissionError` from `iterdir`, :629).
  - (a) Only `FileNotFoundError` / `NotADirectoryError` mean "nothing recorded" (None). Any other `OSError` is a refusal.
  - (b) Keep `except OSError: return None`.

  **Recommendation: (a)** (FR-59). The cost is a few lines in a function already owned. No portable test row exists, so the edge is
  proven by reading.
- **F-7 `artifact_root` pointing outside the project** (`../x`, another drive). (a) Keep accepting it (today's behaviour; a project
  may keep stories on a shared drive). (b) Refuse it. **Recommendation: (a).** The brief names the edge but no defect, and refusing
  would be a new rule that is the owner's to give.
- **F-8 `{"artifact_root": null}`.** (a) Unset, giving the default folder (today). (b) A broken key. **Recommendation: (a).** JSON
  `null` is the usual "unset", and the config template does not carry the key (t-129 F-10).
- **F-9 Test homes.** (a) One NEW table in `test_read_json.py` (T1), plus rows in the EXISTING `ROOT_ROWS` of `test_vcs_evidence.py`
  (T2). `vcs_evidence.py` stays judged by its own keep file. (b) Put everything in `test_read_json.py` and add `vcs_evidence.py` to
  its `covers`. That makes `test-layers.json`, a shared file, an owned path. **Recommendation: (a).** Neither file is quarantined
  (F-9 of §0), so there is no quarantine fork. If "one table" in the DoD is meant literally, (b) is the way, at the price of the
  shared file.
- **F-10 The `pipeline.json` marker for branch (2).** (a) `is_story_folder` AND `pipeline.json`, the one predicate of branch (1).
  `story()` in the test then writes `pipeline.json`. (b) `is_story_folder` alone. This keeps the fixtures, but a plain folder
  (`maintenance/`) under `artifacts/` would still narrow the consultation and skip the word. **Recommendation: (a)** (P31, AR-24).
- **F-11 The U rows of §8** (writer entry points outside `run_guarded`, hook paths without a catch). A residual of this class must be
  a node with owns and a test (designer rule 6). Proposal: node OF4-10r. A scout census first (per U site: the entry point, its
  catch, hook or CLI), then builder nodes cut by file. The test is a row per fixed entry in T1 (`ROOT_SITES`), and the owns are the
  files of the U rows. The priority is the hook paths (`guard_pre_tool:2269`, `stage_guard`, `host_dispatch:23`, `run_suite:3037`).
  **Recommendation:** the Lead opens it as a batch row in the same move as this node. Its owns cannot be final before the census,
  which is why it starts with a scout.
- **F-12 The writer form** (replaces the finding's owner question).
  - (a) The locator raises one typed, finished `ConfigUnreadable`, and `run_guarded` already turns it into a refusal. This needs
    zero per-caller edits for guarded CLIs, and the unguarded ones go to F-11.
  - (b) A wrapper `artifact_root_or_refusal()` that prints and exits, which needs an edit at every writer.
  - (c) A catch at each caller.

  **Recommendation: (a).** It is one survivor (AR-15), and `run_guarded` is the existing door of the class. (b) and (c) are many roads
  to one text.

## §10. Small technical choices closed by the designer (no design weight)

- The new predicate's name is `_story_at`, placed directly above `_story_root_of`.
- In branch (2) the deepest `qa-factory/artifacts/<T>` match decides. When it is no story, the answer is None and no outer match is
  tried.
- The `grounding_errors` unknown record uses script name `grounding_errors` (the word that passes it is `grounding_errors: unreadable`)
  and owner file `requirements-register.md`, the same file its finding text starts with (:1612).
- The key-error text does not echo the value, only its type or "a blank string".
- The changelog fragment name is `changelog.d/of4-10-artifact-root.md`. The builder's task id is not known at draft time.
- The T1 drivers pin the project by patching `hooklib.project_root`, as `_site_report_adapt` does.
- The T2 loop: the `needle` column and `output = None` for probe-only. The existing rows get `""`.

## §11. Reading trail

The snapshot `C:\QAFactory\forge-repo\.claude\worktrees\oh7-5` was read for this draft.

Plans and specs:
- `plans/piles/onboarding-forge/batch-4-hvosty-onbordinga-i-forzha.md`: :1-30, :39, :51, :55
- the finding (whole)
- `plans/piles/onboarding-forge/README.md`: :21, :169
- `plans/PILES.md`: :88
- `plans/builder-rules.md`: :14-73
- `docs/SIBLING_MAP.md`: headings; axes 8, 16, 17, 32-34
- `ai-packages/qa-factory/design/architecture.md`: :105-292
- `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md`: :310-318, :410-449, grep `artifact_root`
- `docs/tasks/specs/t-282-oh6-1-one-component.md` (in the main tree): grep owns / §7

Scripts:
- `hooklib.py`: :28-127, :252-400, :660-870
- `config_contract.py`: :16-30, :1315-1380
- `vcs_evidence.py`: :560-681
- `exit_gate.py`: :19-39, :60-318, :1245-1320, :1455-1640, :1800-2064, plus the function/try index
- `driver_dispatch.py`: :290-314
- `story_step.py`: :2080-2104
- `role_cli.py`: :100-198
- `source_exclusions.py`: :72-77, :290-331
- `driver_sources.py`: :352-416
- `subagent_journal.py`: :195-224 and a grep
- `stage_guard.py`: grep, :3538-3557
- `guard_pre_tool.py`: grep plus four context windows
- `scenario_walk.py`: :14, :45, :833-931

Tests and fixtures:
- `test-layers.json`: :1-36, :4083-4122, :6425-6439, grep (the quarantine section starts at :7004; `test_exit_gate_grounding.py` is at :8026)
- `test_read_json.py`: function index, :595-708
- `test_vcs_evidence.py`: :27-211
- `harness.py`: :257-318
- `judgment-census.json`: grep (rows :288, :396-401, :936)
- `references/config-keys.json`: :783

Git:
- the reflogs under `C:\QAFactory\forge-repo\.git\logs`, grep for OF3-1 (F-11)

Greps with positive controls:
- `artifact_root\(` (control: `def artifact_root`)
- `run_guarded\(` (control: `role_cli.py`)
- `left_out_by_person|"excluded"` (control: `vcs_evidence.py:607`)
- `ConfigUnreadable` (control: `config_contract.py:1321`)

Needed beyond the manifest: `config_contract.py`, `role_cli.py`, `source_exclusions.py`, `driver_dispatch.py`, `story_step.py`,
`driver_sources.py`, `subagent_journal.py`, `harness.py`, `scenario_walk.py`, `judgment-census.json`, the t-129 and t-282 specs, and
`.git/logs`.

Not done: `git log --grep OF3-1` (no shell). The import-time measurement of F-1.

## §12. Coordinator decision (Opus coordinator, degraded window, 2026-11-13; решила сама / по рекомендации, до слова владельца)

**F-1 measurement.** Run on main at 06:38:

`python -X importtime -B -c "import sys; sys.path.insert(0, r'<scripts>'); import hooklib; import config_contract"`

Its last lines:
- `hooklib` cumulative 137829 us;
- `config_contract` self 91177 us, cumulative 139258 us.

So the import roughly doubles a hook process's import time, about +0.14 s on every tool call that reaches `artifact_root`. **F-1 (b) is decided:**
- move `ConfigUnreadable` and `read_config_file` into `hooklib`;
- `config_contract` re-exports the same objects (`config_contract.ConfigUnreadable is hooklib.ConfigUnreadable` holds, pinned by one row in T1);
- the hooklib function list for D-0048 becomes `artifact_root`, `ConfigUnreadable`, `read_config_file`, still disjoint from OH6-1;
- edge: if `read_config_file` needs `config_contract` internals beyond itself and its exception, the builder stops and reports them, and does not move a chain.

**The other forks** take the recommendations:
- F-3 (a): applied to the moved `read_config_file`.
- F-4 (a).
- F-5 (a): the builder re-greps the subprocess readers of the stdout status.
- F-6 (a).
- F-7 (a): whether a root outside the project is allowed goes to the morning list for the owner.
- F-8 (a).
- F-9 (a).
- F-10 (a).
- F-11 (a): residual node OF4-10r, opened by the coordinator as a batch row with a scout census first. That is written in the next doc batch, in the same move as this node's dispatch.
- F-12 (a).
- F-2 is closed by F-12.

`config_contract.py`: no open node owns it (journal and in-work batch owns checked by the coordinator).

**Critic on plan.** This spec carries forks and serves as the spec for more than 30 minutes of work (CLAUDE.md rule 3), so a critic reviews the plan before the build. One critic pass covers this spec and t-290 (OF4-21) together. Both are about the story's location under a configured `artifact_root`, so they count as one topic (R13-g).
