# t-289 — OF4-10: a broken project config never ends in a traceback or a pass at `hooklib.artifact_root()` and its callers; an `--output` inside `artifacts/` is no story (DRAFT, designer; fix round t-305 applied)

Status: DRAFT for Lead acceptance; fix round t-305 applied after critic t-300 (`docs/tasks/specs/reviews/t-300-of4-10-of4-21-plan-review.md`, fit_with_fixes; §13). The forks are in §9 and the coordinator's decisions are in §12. Items marked `[F-n]` follow the
decision of §12 (every fork as recommended, except F-1, which is decided (b)). The spec can be executed before the owner answers the morning-list items (PROJECT.md «Командная
работа» item 11).

Node: `onboarding-forge/4/OF4-10` (batch file `plans/piles/onboarding-forge/batch-4-hvosty-onbordinga-i-forzha.md:39`). Finding:
`plans/piles/onboarding-forge/findings/20261112-artifact-root-brosaet-na-bitom-konfige-a-vyzyvayushchie-lovyat-ne-to.md`.
Trees read:
- The first draft read `C:\QAFactory\forge-repo\.claude\worktrees\oh7-5` (origin/main 0a0db4f).
- The fix round read `C:\QAFactory\forge-repo\.claude\worktrees\read-main` (origin/main ca2f04a).
- Critic t-300 measured that the six t-289 package files are byte-identical between the two commits.

So the line numbers below hold at ca2f04a. The fix round re-checked `hooklib.py` :5, :12, :691, :751, :2737 and `config_contract.py` :1321, :1349-:1373 and :3031 in read-main.

## Dispatch header (builder; rule 11 R11-f)

given: this spec (the enumeration is §0 and §2, one hop); `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md`; `docs/TESTING.md`; `ai-packages/qa-factory/design/architecture.md` (AR-4, AR-9, AR-12, AR-13, AR-15, AR-18, AR-24, AR-28, AR-29); `docs/SIBLING_MAP.md` axes 8, 16, 17, 32, 34; the finding above; critic t-300 (Key 2, Key 3 B1-B3, N1); `docs/tasks/specs/t-129-of3-1-knowledge-catalog.md` §4 rows :315-:318 and item 7 (:410-:447); the scripts, at origin/main ca2f04a: `hooklib.py` (:1-30, :691-706, :751, :2737), `config_contract.py` (:1321-:1374, :3031), `vcs_evidence.py`, `exit_gate.py`, `role_cli.py` (:134-:172), `source_exclusions.py` (:294-:331), `refusal_registry.py` (`sites()`); the tests `test_read_json.py`, `test_vcs_evidence.py`, `test_judgment_census.py` (:10-40), `harness.py` (:257-:318)
owns:
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\hooklib.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\config_contract.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\vcs_evidence.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\exit_gate.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\tests\test_read_json.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\tests\test_vcs_evidence.py
C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\changelog.d\of4-10-artifact-root.md
non-goals: the U rows of the census in §8 (they belong to residual node OF4-10r, fork F-11); `hooklib.is_one_component`, `hooklib.is_story_folder` and `exit_gate._named_ticket` (owned by OH6-1, t-282); `hooklib.load_config` (it keeps `{}`); `test-layers.json`; `judgment-census.json` (deleting or changing row :398 is out of bounds, B1); `references/*`; `driver_sources.py:356` and the existing `vcs_evidence.py:646` text (both literal `qa-factory/artifacts` paths, queued to OF4-21b); `exit_gate.all_errors` (fork F-4 (b)); any other edit of `config_contract.py` beyond the move of §2.1 item 0; a new test file
handoff: the builder report (rule 7 of `.claude/agents/builder.md`) with the verbatim witness of §6, the FR walk, the `architecture:` and `judgment:` lines, and the list "needed beyond the manifest"
edges: §4 (table, with the invariant of each row) and §5 (positional invariants)
DoD: §6. The verification command is `python -B C:\QAFactory\forge-repo\.claude\worktrees\of4-10\ai-packages\qa-factory\scripts\tests\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/hooklib.py ai-packages/qa-factory/scripts/config_contract.py ai-packages/qa-factory/scripts/vcs_evidence.py ai-packages/qa-factory/scripts/exit_gate.py ai-packages/qa-factory/scripts/tests/test_read_json.py ai-packages/qa-factory/scripts/tests/test_vcs_evidence.py ai-packages/qa-factory/changelog.d/of4-10-artifact-root.md`, then every file it prints (scope in §6)
siblings: axis 8 (the story on disk: `artifact_root`, the story predicate of `_story_root_of`); axis 16 (`artifact_root`'s own `json.loads` goes; the config is read by the one config reader, which now lives in `hooklib`); axis 17 (`unreadable_record` is the shape `grounding_errors` returns); axis 32 (census rows `hooklib.artifact_root`, `exit_gate.grounding_errors`); axis 34 (one road: one config reader, one story predicate for both recognitions); the other `artifact_root` callers are in §8 with a verdict each
designer: (Lead fills in at dispatch: the accepted draft's path)

## §0. Facts this draft rests on (each read in its carrier)

- F-1 `hooklib.artifact_root(event=None, root=None)` :691-706. The project is `root` or `project_root(event)`, resolved. The config is
  `<project>/qa-factory/config.json`.
  - :697 reads it with its own `json.loads(config.read_text(encoding="utf-8-sig"))` when the file `exists()`, else `{}`.
  - A non-object raises `ValueError` with a door (:698-699).
  - A missing or `None` key gives `<project>/qa-factory/artifacts` (:701-702).
  - A non-string or blank key raises `ValueError("artifact_root must be a non-empty path")` (:703-704), which has no door.
  - Otherwise the value is resolved against the project (:705-706).

  Raw exceptions that escape today: `JSONDecodeError` (no file named), `UnicodeDecodeError`, `OSError` (a folder named `config.json`,
  no rights), and `RecursionError` on deep nesting, which is NOT a `ValueError`. The comment at :695-696 says the raise is intended
  (AR-28, AR-4). The finding's "`AttributeError` on a JSON list" (finding :9) is stale: :698-699 now raise `ValueError`.
  `refusal_registry.sites()` sees the literal `raise ValueError` at :699 and :704. These are the census unit of row
  `judgment-census.json:398` (critic t-300 B1, measured at ca2f04a).
- F-2 `config_contract.ConfigUnreadable(ValueError)` (:1321) and `read_config_file(root)` (:1349-1374) already exist. This is the
  package's config reader (OF3-1 AR-13 row, t-129 :205).
  - An absent file gives None.
  - A present file that cannot be read raises `ConfigUnreadable` with one door sentence: OSError/UnicodeDecodeError :1361, an empty
    file :1365, not JSON :1368, not an object :1371.
  - Gap: `json.loads` at :1367 can raise `RecursionError`, which the `except ValueError` at :1368 misses (fork F-3).
  - Dependencies: only `Path`, `json` and the class itself. No other `config_contract` name is used (critic t-300 Key 2). `hooklib`
    already imports `json` (:5) and `Path` (:12).
  - `hooklib` imports `config_contract` only lazily (:2737), and `config_contract` imports `hooklib` only lazily (:272, :939).
  - Consumers use `C.ConfigUnreadable` / `C.read_config_file` as attributes; `config_contract`'s own use is `:3031`. No test
    monkeypatches or reloads either name (critic t-300 Key 2).
- F-3 `role_cli.run_guarded` :134-172 turns a `ValueError` into `refuse(command, str(exc))` (:163-164). So every CLI under `run_guarded`
  already prints a refusal, not a traceback, when the locator raises a `ValueError`. Today it prints the raw text
  (`Expecting value: line 1 column 2 (char 1)`). An `OSError` gets the generic OS sentence (:170-172), and a `RecursionError` is not
  caught.
- F-4 `vcs_evidence._story_root_of` :581-604.
  - Branch (1), configured root (OF3-1 d), narrows to `<root>/<T>` only when `is_story_folder(root, T)` holds and `pipeline.json` is a
    file. It catches `(OSError, ValueError, AttributeError)` and falls through (:598-599).
  - Branch (2), path parts (:600-603), returns `Path(*parts[:index + 2])` for the deepest `qa-factory/artifacts/<x>`, with NO story
    test.

  With `--output .../qa-factory/artifacts/x.json`, branch (2) returns the FILE `artifacts/x.json` as the story. `left_out_by_person`
  then reads `artifacts/x.json/work/source-exclusions.json`, which is absent: `source_exclusions.read_record` :298-299 gives None, and
  `live` :330-331 gives []. The result is None, so the tool reads and the person's word is skipped. Proven by reading; critic t-300
  traced it by hand too.
- F-5 `vcs_evidence.left_out_by_person` :607-649. With no story known, :628 `sorted_paths(p for p in Path(artifact_root()).iterdir() if p.is_dir())`
  runs inside `except OSError: return None` (:629-630).
  - (a) Invalid JSON, a list, or a bad key raise `ValueError`, which escapes `main` as a traceback with exit 1.
  - (b) A config that is a FOLDER raises `OSError` inside `artifact_root`, which :629 catches. The result is None and the MR is read:
    a silent pass on an unknown.

  `main` :652-676 prints every refusal with `"status": "excluded"`, `"error": "left_out_by_person"` (:662-663). That includes the
  existing unreadable-record refusal at :636 (exclusion id `""`). The existing text at :646 names the literal
  `qa-factory/artifacts/<that story>/work/`, which is queued to OF4-21b and not touched here.
- F-6 `exit_gate.grounding_errors` :1551-1618.
  - :1560 resolves the ticket. When `task` is unknown this goes through `_ticket_for_stage` (:754-770), whose `artifact_root()` at
    :759 is outside its try.
  - :1563 `root = artifact_root() / ticket / "work"` is outside any try.
  - The "safe read" the finding means is :1569-1573.
  - Census row: `judgment-census.json:288` (class `shape`, owner `data`).
- F-7 `exit_gate.all_errors` :1828-1869 runs `scoped_errors` first, and `collect_errors` :1279 calls `artifact_root()` with no guard.
  So with a broken config `all_errors` raises before `grounding_errors` runs. All three callers catch `Exception` and record an
  unknown: the hook `main` :1999-2008, `driver_dispatch` :295-304, and `story_step` :2087-2092.
- F-8 The hook tracebacks that are reachable with a broken config:
  - `exit_gate._identity` :287 `art_root = artifact_root()` is outside the try at :292-299. This runs when the event has no
    `input_fingerprint`. Callers: `main` :1922 and `subagent_journal` :207.
  - `exit_gate.awaiting_source_review` :1519 calls `_ticket_for_stage("S1")` outside its try (:1522-1528), from `main` :1994.
- F-9 Test homes (`test-layers.json`; the `quarantine` section starts at :7004):
  - `test_read_json.py` :4083 is `keep` (layer `data_join`, covers `exit_gate.py` and `hooklib.py`).
  - `test_vcs_evidence.py` :6425 is `keep` (layer `detector`).
  - `test_exit_gate_grounding.py` :8026 is QUARANTINED and is never run, fixed or edited.
  - `test_judgment_census.py` :2708 is `keep`.

  Critic t-300 re-checked this at ca2f04a.
- F-10 `test_vcs_evidence.py`: `ROOT_ROWS` :167-190 with its loop at :191-210; the `story()` helper :40-47 builds no `pipeline.json`.
  `test_read_json.py` :598-693: `CONFIG_STATES` × `SITES`. `_site_report_adapt` :631-637 pins the project by patching
  `hooklib.project_root`.
- F-11 The dependency "after the OF3-1 merge" is indirect evidence only. The designer could not run `git log --grep OF3-1` (no shell).
  Evidence: the snapshot carries OF3-1 d's code, the batch-3 branch reflog shows the merges, and OF4-22 is accepted.
  **Estimate, not verified.** The Lead runs `git -C C:\QAFactory\forge-repo log refs/remotes/origin/main --oneline --grep OF3-1`
  before dispatch.
- F-12 Concurrent nodes:
  - OH6-1 (t-282 §7) owns `hooklib.is_one_component`, `hooklib.is_story_folder`, `exit_gate._named_ticket`, and one top-level
    `import hooklib` in `exit_gate.py`. Critic t-300 Key 6 confirms it is disjoint from this node.
  - OF4-26 (`ожидает`) also owns `test_read_json.py`.

## §1. Architecture, owners, census (designer rule 1; CLAUDE.md rule 10)

| AR-n | how this node touches it | change check, written into the DoD |
|---|---|---|
| AR-28 an unknown never becomes a pass | a broken config becomes a refusal with a door (`left_out_by_person`, writers) or an `unreadable` record (`grounding_errors`). It is never `None` / `[]` / a default folder. F-5 (b) silent pass closed | DoD 3: the §7 rows "broken × site" read `refused` / `unreadable`, never the pass value. Each new read's behaviour on missing / unreadable / empty is stated in §4 |
| AR-9 every refusal names what it expected and a door | two finished texts, one per cause, both naming `config.json`, what was expected and the door: (i) read/parse failures, as `ConfigUnreadable` from `read_config_file` (fix the file or move it aside and re-onboard); (ii) an unusable `artifact_root` value, as a literal `ValueError` (remove the key or set it to a folder path). `left_out_by_person` adds the role's own door (`--output` under the story folder, or say so in the handoff), with no default folder named (B2) | DoD 5: `python -B scripts/refusal_registry.py --check` green. If it names a new site, the builder RETURNS the question (A24 row, `controller-blocks.md`), because neither is in owns |
| AR-13 a fact with a reader is read only through it | `artifact_root` stops parsing `config.json` itself and reads it through `read_config_file`, which moves into `hooklib` with `config_contract` re-exporting it [F-1 (b)] | DoD 4: `grep -n "json.loads" scripts/hooklib.py` (positive control: the hit in `read_json` :751 and in the moved `read_config_file`) shows no hit in `artifact_root`; `grep -n "def read_config_file\|class ConfigUnreadable" scripts/config_contract.py` gives no hit (positive control: the same grep on `hooklib.py` gives two); `test_read_json.py` G5 census green |
| AR-15 one survivor | one config reader (`hooklib.read_config_file`); one story predicate `_story_at` for both recognitions of `_story_root_of`. Coupling (critic t-300 Key 4, B1): the class family stays `ValueError`, read failures are `ConfigUnreadable`, and key refusals are a literal `ValueError` | DoD 4: every site of §8 is listed with its verdict; the builder re-runs the grep with the positive control `def artifact_root` |
| AR-18 one output shape | `grounding_errors` returns the existing `unreadable_record` (a `DV.Record`, kind `unreadable`) | DoD 5: `test_detector_verdict.py` green if `--witness-for` prints it; no new parser |
| AR-24 a person's words reach whatever acts on them | the "do not read this MR" word is never skipped: not by a file in `artifacts/`, not by a plain folder, not by a broken config | §7 rows V1-V3, V4-V8 |
| AR-4 nothing tied to one layout | a configured `artifact_root` keeps being honoured; an outside path stays legal [F-7, on the owner's morning list] | §7 row "outside" |
| AR-29 a code check judges data | no check judges a role's content; owners and classes are in the table below. Census (B1, t-300): the key-value and `resolve` refusals inside `artifact_root` stay a literal `raise ValueError(<the finished text of item 3>)` (class `ValueError`, `ConfigUnreadable` is not used for them), so `refusal_registry.sites()` keeps seeing `artifact_root` and census row `judgment-census.json:398` keeps its unit; read and parse failures arrive as `ConfigUnreadable` from `read_config_file`. T1 `locator` token `refused` = raises a `ValueError` (ConfigUnreadable included) whose text contains `config.json`. If `test_judgment_census.py` C1 still names `hooklib.py: artifact_root`, the builder RETURNS the question; deleting row :398 is out of bounds. | DoD 5: `test_judgment_census.py` green with no row added, removed or raised; `refusal_registry.sites()` still lists `artifact_root`. A unit C1 names is returned as a question (the census file is not in owns) |
| AR-12 friction | no import added on the hook path; the measured +0.13 s of `config_contract` is avoided (F-1 (b)) | report line: `code_friction` "not measured" |

Every check the node adds or alters, with the owner it serves and its census class:

| check (file: function) | added / altered | owner it serves | census class | census row |
|---|---|---|---|---|
| `hooklib: artifact_root`: an unusable `artifact_root` value (non-string, blank, NUL, unresolvable) raises a literal `ValueError` with the finished text; a config that cannot be read raises `ConfigUnreadable` from `read_config_file` | altered (texts; the same direction; the literal `raise ValueError` sites stay) | data (code: where the story folders are) | shape | existing `judgment-census.json:398`, keeps its unit (B1) |
| `hooklib: read_config_file` (moved verbatim from `config_contract`): nesting too deep for the parser raises `ConfigUnreadable` [F-3] | moved + altered | data | shape | not a unit before or after (critic t-300 B1 neighbours); no row |
| `vcs_evidence: left_out_by_person`: no story known and the root cannot be found leads to a refusal | added (a new refusal branch) | intent: the person's recorded "do not read" word | safety (protects the person's words, AR-29 last sentence) | none today for this function; if C1 asks for one, the builder returns the question |
| `vcs_evidence: _story_root_of` / `_story_at`: narrows only to a real story | altered (branch (2) gains the predicate) | intent (the same word; the error direction protects it) | shape (presence of a folder and its marker) | not a refusal unit; no row expected |
| `exit_gate: grounding_errors`: an unknown root gives one `unreadable` record | altered | data | shape | existing `:288`, unchanged |
| `exit_gate: _identity` / `awaiting_source_review` (fork F-4) | altered (no raise) | data | not a check (a key read, an identity read) | none |

FR walk (PROJECT.md acceptance item 1, the sections touched):
- A: FR-1, FR-2, FR-4, FR-46 (the family stays `ValueError`), FR-57.
- C: FR-14 (the stdout shape of `vcs_evidence`).
- D: FR-59.
- E: FR-37 (a refusal names no path the code did not resolve, B2) and FR-41 (an unknown stdout status is not reported as `excluded`, [F-5]).
- G: FR-30, FR-32.
- B: no gate or question text changes, so one line in the report.

## §2. Per caller: current line, current behaviour, new behaviour, error direction

### 2.1 `hooklib.artifact_root` :691-706 (the locator; hot file), with the move of the config reader [F-1 (b)]

Current behaviour on a broken config: F-1.

New behaviour:

0. **The move.** F-1 (b) shape (B3, t-300): `ConfigUnreadable` and `read_config_file` move VERBATIM into `hooklib` (they need only
   `Path`, `json` and the class: no other `config_contract` name; checked at ca2f04a), with the F-3 `RecursionError` catch added
   there; `artifact_root` calls `read_config_file(project)` directly, so no import is added to it. `config_contract.py` replaces its
   two definitions with ONE top-level line `from hooklib import ConfigUnreadable, read_config_file  # re-export (OF4-10)`; its own
   uses (`:3031`) keep the bare name. Invariant: `hooklib` never imports `config_contract` at module level (the lazy import at :2737
   stays lazy); the T1 row pins `config_contract.ConfigUnreadable is hooklib.ConfigUnreadable` and
   `config_contract.read_config_file is hooklib.read_config_file`. The `ConfigUnreadable` docstring widens to "cannot be read as one
   JSON object, or names an unusable `artifact_root`" only if B1's alternative is ever taken; under B1 it stays as is.

   Placement: the class and the function go directly above `artifact_root`. They go nowhere near `is_one_component` /
   `is_story_folder` (OH6-1, :269-320). Stop edge (§12): if the moved body needs any other `config_contract` name, the builder
   stops and reports it. Critic t-300 found none at ca2f04a.
1. The config is read by `read_config_file(project)`, the moved function, in the same module. None (no file) becomes `{}`, the default
   world. A present file that cannot be read raises `ConfigUnreadable` with its own text.
2. A `RecursionError` is a `ConfigUnreadable` too [F-3 (a)]. It is caught inside the moved `read_config_file`, next to the existing
   `except ValueError` of the parse, with a text of the same form ("is nested too deeply to read").
3. The value is `cfg.get("artifact_root")`. `None` (absent or JSON `null`) gives `<project>/qa-factory/artifacts`, as today [F-8]. Any
   other non-string, a blank string, or a string with `\x00` raises a **literal**
   `raise ValueError("qa-factory/config.json: `artifact_root` must be a non-empty folder path (got <type name or 'a blank string'>). Remove the key to keep the story folders in qa-factory/artifacts, or set it to a folder path.")`.
   The value itself is not echoed. Census (B1, t-300): the key-value and `resolve` refusals inside `artifact_root` stay a literal
   `raise ValueError(<the finished text of item 3>)` (class `ValueError`, `ConfigUnreadable` is not used for them), so
   `refusal_registry.sites()` keeps seeing `artifact_root` and census row `judgment-census.json:398` keeps its unit; read and parse
   failures arrive as `ConfigUnreadable` from `read_config_file`. T1 `locator` token `refused` = raises a `ValueError`
   (ConfigUnreadable included) whose text contains `config.json`. If `test_judgment_census.py` C1 still names
   `hooklib.py: artifact_root`, the builder RETURNS the question; deleting row :398 is out of bounds.
4. `(path if absolute else project / path).resolve()`. An `OSError` or `ValueError` from `resolve` becomes the same literal
   `raise ValueError(<the text of item 3>)` (B1).
5. The comment at :695-696 stays in substance: a broken config raises here and never becomes the default folder. The non-object check at
   :698-699 goes, because `read_config_file` raises `ConfigUnreadable` for it (:1371-1373). The census unit survives at the item 3 and
   item 4 raises.

Error direction: refuse. The locator may refuse a config a person would call fine, but only for a blank, NUL or non-string value, and
the text then names the key and the fix. It never returns a folder after a read or parse failure.

Adversarial inputs that must stay on the refusing side:
- the file: empty; whitespace only; BOM only; `{not json`; `{} x`; `[1, 2]`; `[]`; `"str"`; `null`; non-UTF-8 bytes;
  `"[" * 300000`; a folder named `config.json`;
- the key: `""`, `"   "`, `5`, `["a"]`, `{}`, `"a\u0000b"`.

A reused function in a new, more consequential role (designer rule 1): `read_config_file` used to serve onboarding and the doctor.
Now it decides the artifact root for every writer, hook and reader. It may err only toward `ConfigUnreadable` for a present file. None
means "no file" only, and nothing that exists becomes None or `{}`. A dangling symbolic link named `config.json` reads as absent, as it
does today. This is kept, and it is an analog in §8.

### 2.2 `vcs_evidence._story_root_of` :581-604

Current behaviour: F-4. With a broken config, branch (1) is skipped and branch (2) still names `qa-factory/artifacts/<x>` for any
`<x>`, a file included.

New behaviour: one private predicate `_story_at(parent, name) -> Path | None`. It returns `parent / name` when
`hooklib.is_story_folder(parent, name)` holds AND `(parent / name / "pipeline.json").is_file()`; any `OSError` / `ValueError` gives
None.
- Branch (1) calls it, which keeps today's semantics.
- Branch (2) calls it for the deepest `qa-factory/artifacts/<T>` whose `--output` lies BELOW `<T>` (at least one part follows `<T>`,
  mirroring (1)).
- When the deepest match is not a story, the answer is None, and no outer match is tried.

Error direction: "not a story", so every story is consulted. It never names a file, a plain folder, a folder without
`pipeline.json`, an alias, or a missing folder.

Adversarial inputs: `artifacts/x.json`; `artifacts/maintenance/x.json` (`factory_dashboard.py:493`); `artifacts/S-2/x.json` with no
`pipeline.json`; `artifacts/S-2 /x.json`; a case variant; `artifacts/S-2/../tmp/x.json`; `--output` equal to `artifacts/S-2`.

### 2.3 `vcs_evidence.left_out_by_person` :607-649

Current behaviour: F-5.

New behaviour:
- A story is known (`_story_root_of` not None): its own list is consulted, as today. That needs no artifact root.
- No story is known: `root = artifact_root()` runs inside `try ... except (OSError, ValueError) as exc`. On an exception the function
  returns `(2, "vcs_evidence: " + str(exc) + " No story is named by --output, so the list of sources the person left out must be read
  for every story, and the story folders cannot be found: nothing was fetched." + <the door sentence below>, "")`.
  The refusal text names no default folder: "...Run it with `--output` under the story's own folder (`<artifact root>/<story>/work/`),
  or say so in your handoff." (B2, t-300; the placeholder form of `hooklib._example_folder`; the existing :646 text stays for
  OF4-21b.)
- Then the listing is made:
  - `FileNotFoundError` / `NotADirectoryError` (no story folder at all) give None, as today.
  - Any other `OSError` gives a refusal of the same form, naming the folder that could not be listed [F-6].

Error direction: toward not reading. The cost: a broken config refuses a probe-only read even when nobody recorded anything. The door
is the `--output` of a story, the handoff, or a fixed file.

### 2.4 `vcs_evidence.main` :652-676

Current: every refusal prints `"status": "excluded"`.

New [F-5 (a)]: a refusal whose exclusion id is empty is "could not check". It prints
`{"url", "status": "unknown", "error": "not_checked", "exclusion": "", "fetched": false}`, both for a broken config and for the existing
unreadable-record refusal at :636. A refusal with an id keeps `excluded` / `left_out_by_person`. Both cases exit with code 2.

Readers: critic t-300 N2 found no code reader of the stdout `status`. The control was `vcs_evidence`'s own hits. The existing
unreadable-record row (`test_vcs_evidence.py:131-134`) checks the exit code and stderr only, so no existing expectation changes. The
builder re-greps `"vcs_evidence.py"` (control: `driver_sources.py:355`), per §12.

### 2.5 `exit_gate.grounding_errors` :1551-1618

Current: F-6, F-7.

New: right after the role check (:1558-1559), and before :1560 and :1565, the ticket resolution and `artifact_root()` go inside
`try ... except (OSError, ValueError) as exc: return [unreadable_record("grounding_errors", f"the story folders could not be found ({exc})", "requirements-register.md")]`.
`import hooklib` stays local.

Error direction: unknown, never `[]`. "No register" `[]` is reachable only after the root was read. Another role keeps `[]`.

### 2.6 `exit_gate._identity` :287 [F-4] and `exit_gate.awaiting_source_review` :1519 [F-4]

Current: F-8.

New:
- In `_identity`, `scan_root` is computed from the slug FIRST (`exploration.root(slug, project_root(event))` when `slug` is set).
  `artifact_root()` is called only when there is no slug, inside the existing try at :292-299, together with the
  `art_root / task` choice (N1, t-300). On an exception, `file_state = []`. Every other field of the scope, and the key, is unchanged.
  An exploration's own file state is therefore never dropped by a broken config.
- In `awaiting_source_review`, the ticket resolution at :1519-1521 moves inside the existing try at :1522-1528, so an exception
  returns `False`.

Error direction:
- `_identity`: a fingerprint without the artifact state. The fuse holds only `blocked` / `incomplete` (:1982), and with a broken config
  the gate's status is `unreadable` (F-7).
- `awaiting_source_review`: `False`, so the gate runs and records the unknown. It never records `awaiting_human` on an unknown.

### 2.7 The writers

Current: F-3. A writer under `run_guarded` prints a refusal with the raw text; one outside it prints a traceback.
`execution_scheduler.py:359` and `:577` raise on purpose (OF3-1 F12).

New: through 2.1 alone, every writer under `run_guarded`, and every site that catches `ValueError` / `Exception` and prints
`str(exc)`, prints a finished text: the `ConfigUnreadable` text or the key text (FR-1, AR-9). This needs no edit at any caller
[F-12]. The `RecursionError` and `OSError` cases now arrive as `ValueError`. The writers outside `run_guarded` still print a
traceback, now with the finished text in its last line. Those are the U rows of §8 and the entry points of OF4-10r [F-11].

Error direction: a writer refuses before it reads, creates or launches anything. F12 is unchanged.

## §3. Hot files: D-0048 function lists

| file | hot | functions this node touches | outside a function | the concurrent node's list (disjoint) |
|---|---|---|---|---|
| `scripts/hooklib.py` | yes | `artifact_root`; new `read_config_file` and class `ConfigUnreadable`, moved in directly above `artifact_root` | the class definition `ConfigUnreadable` (top level, above `artifact_root`); no new import (`json`, `Path` are already there); the lazy `import config_contract` at :2737 is untouched | OH6-1: `is_one_component`, `is_story_folder` (:269-320) |
| `scripts/config_contract.py` | no | `read_config_file` and `ConfigUnreadable` are DELETED (moved) | ONE new top-level line `from hooklib import ConfigUnreadable, read_config_file  # re-export (OF4-10)`; `:3031` and every other use are unchanged | the Lead checked: no open node owns it (§12) |
| `scripts/exit_gate.py` | shared with OH6-1 | `grounding_errors`; `_identity` and `awaiting_source_review` [F-4] | none (no new top-level import) | OH6-1: `_named_ticket`, plus one top-level `import hooklib` |
| `scripts/vcs_evidence.py` | no | `_story_root_of`; new `_story_at` (directly above it); `left_out_by_person`; `main` | none | — |
| `scripts/tests/test_read_json.py` | no | a NEW function `test_the_artifact_root`, after `test_the_config_readers`, and one call line in `__main__` | the new tables `ROOT_STATES` and `ROOT_SITES`, beside that function | OF4-26 (`ожидает`) also owns this file. This node does not touch `SITES`, `CONFIG_STATES` or `test_the_config_readers` |
| `scripts/tests/test_vcs_evidence.py` | no | `story()` (writes `pipeline.json`); `ROOT_ROWS` and its loop | — | — |

## §4. Edges, each with the invariant it protects

| # | input | behaviour | invariant (what must stay unreachable or refused) |
|---|---|---|---|
| E1 | config absent | `artifact_root` gives `<project>/qa-factory/artifacts`. `left_out_by_person` with no story and no such folder: `FileNotFoundError`, so None and it reads. `grounding_errors` gives `[]` without a register | absent ≠ unreadable: absent never refuses, unreadable never reads as absent |
| E2 | config unparsable: `{not json`, `{} x`, non-UTF-8 bytes, `"[" * 300000` | `ConfigUnreadable`. Then: writer refusal; `left_out_by_person` (no story) refusal with exit 2; `grounding_errors` gives `unreadable` | no default folder, `None` or `[]` after a failed read; `RecursionError` never escapes as a non-`ValueError` |
| E3 | config not an object: `[1, 2]`, `[]`, `"s"`, `null`, `5` | as E2 (`read_config_file` :1371-1373) | as E2 |
| E4 | config empty: 0 bytes, whitespace, BOM only | as E2 | an empty file is unreadable, never "no config" |
| E5 | a folder named `config.json`, or no read rights | as E2; the F-5 (b) silent pass is closed | an `OSError` of the config never reaches an `except OSError` that means "no folder" |
| E6 | key of a wrong type: `5`, `["a"]`, `{}`, `true` | a literal `ValueError` naming `config.json`, `artifact_root` and the fix (B1) | a non-string never becomes a path; the census unit stays |
| E7 | key empty: `""`, `"   "` | as E6 | an empty key never becomes the project folder |
| E8 | key containing `\x00` | as E6 (an explicit check, not left to `resolve`) | one answer on every platform |
| E9 | key `null` | the default folder [F-8] | only a non-empty string names another folder |
| E10 | key a path outside the project | accepted and resolved, as today [F-7, owner's morning list] | a configured root is honoured (AR-4) |
| E11 | `--output` directly in `qa-factory/artifacts/` | not a story, so every story is consulted and a recorded word refuses | a file is never a story |
| E12 | `--output` under a folder of `artifacts/` with no `pipeline.json` | not a story, so every story is consulted | a narrowed consultation is reached only for a real story |
| E13 | `--output` under a real story of the old default folder | the story is named | today's narrowing keeps working |
| E14 | `--output` equal to the story folder itself | not named | the same rule as branch (1) |
| E15 | broken config, story known by branch (2) | its own list is consulted (existing rows :186, :188) | a known real story needs no artifact root |
| E16 | broken config, probe-only or `--output` outside every story | refusal, exit 2, nothing fetched, stdout `status: unknown`, the door names `<artifact root>/<story>/work/` (B2) | an unknown root is never `None`; a refusal never names a folder the code did not resolve |
| E17 | the artifact root cannot be listed | refusal naming the folder [F-6] | only "no folder" means "nothing recorded" |
| E18 | broken config at an S1 role's stop | hook exit 0 with `gate_unreadable`; no traceback [F-4] | a hook never ends in a traceback on a broken config |
| E19 | `grounding_errors` for another role, broken config | `[]` | a role is never judged by a check that is not its own |
| E20 | the change creates no file, flag or config | no temporal edge | — |
| E21 | limits | none added; the parser's nesting limit is a BEYOND row (E2 deep) | — |
| E22 | exploration stop (`slug` set), broken config | `scan_root` comes from the slug and its file state is scanned as today (N1) | an exploration's identity never depends on the story root |
| E23 | a consumer of `config_contract.ConfigUnreadable` / `read_config_file` after the move | the same objects through the re-export (`is` identity) | an `except C.ConfigUnreadable` keeps catching what `hooklib` raises |

Conflicting requirement pairs, resolved:
- "Never a traceback" against F12 "writers raise on purpose": writers still raise, now with the finished text. The entry point decides
  whether a traceback appears. The remaining entry points are OF4-10r [F-11].
- "An unknown is never a pass" against "probe-only works on a project with no stories": absent goes to E1, broken goes to E16.
- "One exception class" (AR-15) against the census unit (AR-29): resolved by B1. The family is `ValueError`, read failures are
  `ConfigUnreadable`, and key refusals stay a literal `ValueError`.
- The branch (2) marker against the old fixtures: `story()` writes `pipeline.json`, as S0 does. This rests on t-129 F-6b and is an
  estimate.

## §5. Positional invariants (rule 11 (ii))

- P1 `artifact_root`: the config read comes first. The default folder is returned ONLY for an absent file or an absent/`null` key, and
  never after an exception.
- P1b The move (B3): the class and the function sit in `hooklib` above `artifact_root`. `hooklib` has no module-level
  `config_contract` import (only the lazy one at :2737). `config_contract`'s re-export line is top-level and comes after its own
  imports.
- P1c The census (B1): the literal `raise ValueError(...)` for the key and for `resolve` stays inside `artifact_root`. It is not
  moved into a helper, and it is not swapped for a subclass raised by name.
- P2 `_story_root_of`: the order is (1), then (2), then None. Both branches decide through `_story_at` alone, and a narrowed answer is
  unreachable unless `_story_at` returned a folder.
- P3 `left_out_by_person`: the import guard (:621-625) stays first and unchanged, then `_story_root_of`. The config guard sits ONLY on
  the no-story branch, before the listing. `None` is unreachable from any exception other than "no folder".
- P4 `vcs_evidence.main`: `"status": "excluded"` is printed only for a non-empty exclusion id [F-5].
- P5 `grounding_errors`: the guard comes after the role check, before `_ticket_for_stage` and before `register.is_file()`.
- P6 `_identity` [F-4]: the slug decides `scan_root` before any `artifact_root()` call (N1). Only the no-slug root lookup and the scan
  are inside the try. `task`, `dispatch`, `attempt`, `hook` and `agent` are computed exactly as today.
- P7 `awaiting_source_review` [F-4]: `True` is unreachable unless the source inventory was read.

## §6. DoD

Acceptance criteria:
1. §2 is implemented in the owned files only, inside the §3 function lists. `config_contract.py` changes ONLY by the deletion of the
   two definitions and the one re-export line.
2. The §7 table exists as specified. The existing rows of both test files keep their expected values; in `test_vcs_evidence.py` this
   holds after `story()` writes `pipeline.json`. A row whose expectation would change is returned as a question.
3. No row of §7 shows a traceback or an unexpected exception class. Every "broken" cell is `refused` / `unreadable`.
4. Greps, each with its positive control:
   - `grep -n "json.loads" ai-packages/qa-factory/scripts/hooklib.py` has no hit inside `artifact_root`. Control: the hits in
     `read_json` (:751) and in the moved `read_config_file`.
   - `grep -n "def read_config_file\|class ConfigUnreadable" ai-packages/qa-factory/scripts/config_contract.py` gives no hit. Control:
     the same grep gives two hits on `hooklib.py`.
   - `grep -n "^import config_contract\|^from config_contract" ai-packages/qa-factory/scripts/hooklib.py` gives no hit. Control: the
     lazy `import config_contract` at :2737 is found by `grep -n "import config_contract"`.
   - `grep -n "artifact_root(" ai-packages/qa-factory/scripts --include=*.py` returns the §8 list plus nothing new. Control:
     `def artifact_root`.
5. AR detectors, both green and unchanged:
   - `python -B <wt>\ai-packages\qa-factory\scripts\tests\test_judgment_census.py`;
   - `python -B <wt>\ai-packages\qa-factory\scripts\refusal_registry.py --check`.

   `refusal_registry.sites()` still lists `artifact_root` (B1); the builder pastes the one-line check
   `python -B -c "import sys; sys.path.insert(0, r'<wt>\ai-packages\qa-factory\scripts'); import refusal_registry as R; print([s for s in R.sites(files=['hooklib.py']) if 'artifact_root' in str(s)])"`,
   or the equivalent call the module's signature takes. A unit or site they name is returned as a question. Deleting census row :398
   is out of bounds.
6. The commit message carries:
   - `architecture: AR-28, AR-9, AR-13, AR-15, AR-18, AR-24, AR-4, AR-29, AR-12 -- <how kept>`;
   - `judgment: none -- the artifact_root and grounding_errors rows keep class shape, owner data; artifact_root keeps its literal ValueError unit`,
     unless DoD 5 says otherwise;
   - the FR walk of §1;
   - `code_friction: not measured`.
7. The changelog fragment `changelog.d/of4-10-artifact-root.md`, in English.

Verification run (`plans/builder-rules.md` 7b): the command on the `DoD:` line, then each printed file, run as
`python -B <wt>\ai-packages\qa-factory\scripts\tests\<file>.py`. Two kinds of file are not run, and each is a report line instead:
a quarantined file, and the big files 7b excludes (`test_story_step.py`, `test_story_run_*`). The output is pasted verbatim.
`<wt>` = `C:\QAFactory\forge-repo\.claude\worktrees\of4-10`.

## §7. The parameterised test table

### T1, new: `test_read_json.py` `test_the_artifact_root(scratch)`. `ROOT_STATES` × `ROOT_SITES`, one `check_eq` per cell, row id `OF4-10 <site> x <state>`

`ROOT_STATES` (the bytes written to `<root>/qa-factory/config.json`; `None` means no file; `DIR` means a folder of that name):
- `absent`: None
- `no_key`: `{"schema_version": 1}`
- `key`: `{"artifact_root": "stories"}`
- `bom_key`: BOM + `key`
- `null_key`: `{"artifact_root": null}`
- `outside`: `{"artifact_root": "../outside"}`
- `empty_file`: `b""`
- `blank_file`: `b"   "`
- `invalid`: `{not json`
- `list`: `[1, 2]`
- `latin1`: `{"artifact_root": "\xe9"}`, raw bytes
- `deep`: `DEEP` (:51)
- `dir`: DIR
- `key_empty`: `{"artifact_root": ""}`
- `key_blank`: `{"artifact_root": "   "}`
- `key_number`: `{"artifact_root": 5}`
- `key_list`: `{"artifact_root": ["a"]}`
- `key_nul`: `{"artifact_root": "a\u0000b"}`

`ROOT_SITES` (each driver returns a token; any exception that is not a `ValueError` becomes `crash:<Type>`):
- `locator`: `hooklib.artifact_root(root=root)`. It returns:
  - the POSIX path relative to `root`;
  - else `outside:<name>`;
  - or `refused` when it raises a `ValueError` (ConfigUnreadable included) whose text contains `config.json` (B1).
- `writer`: `role_cli.run_guarded("of4-10 writer", lambda: (hooklib.artifacts_dir("S-1"), 0)[1], stream=buf)`. The project is pinned by
  patching `hooklib.project_root` (precedent :631-637). It returns `ok` on 0, or `refused` on `EXIT_REFUSED` with `config.json` in
  `buf` and no `Traceback`.
- `grounding`: story `S-1` with `work/requirements-register.md` at `qa-factory/artifacts/S-1` AND at `stories/S-1`, with the project
  pinned the same way. `exit_gate.grounding_errors("qa-requirements-tester", "S-1")` returns `[]`, or `unreadable` when the answer is
  exactly one record of kind `unreadable` whose text contains `grounding_errors: unreadable`.

Expected:

| state | locator | writer | grounding |
|---|---|---|---|
| absent, no_key, null_key | `qa-factory/artifacts` | `ok` | `[]` |
| key, bom_key | `stories` | `ok` | `[]` |
| outside | `outside:outside` | `ok` | `[]` |
| empty_file, blank_file, invalid, list, latin1, deep, dir, key_empty, key_blank, key_number, key_list, key_nul | `refused` | `refused` | `unreadable` |

Additional checks in the same function:
- "every site has a cell per state".
- B3 identity pins: `config_contract.ConfigUnreadable is hooklib.ConfigUnreadable` and
  `config_contract.read_config_file is hooklib.read_config_file`. These replace the existing `hasattr` check at :692-693 only as an
  addition; that check stays.
- B1 class split: for `invalid`, the locator's exception `isinstance(exc, hooklib.ConfigUnreadable)`. For `key_number`, it is
  `type(exc) is ValueError`.

The writer and grounding drivers pin the project by patching, because `absent` and `dir` carry no marker (`hooklib.py:35-41`,
:98-104).

### T2, rows added to the existing `test_vcs_evidence.py` `ROOT_ROWS` (:167-190)

The tuple gains an 8th column `needle` (text stderr must contain; `""` means no check), and `output` may be `None` (probe-only). For
exit 2 with a needle, the loop also checks:
- the stdout `status == "unknown"` [F-5 (a)];
- `calls == []`;
- that stderr does NOT contain `qa-factory/artifacts/<story>` (B2).

Existing rows get `needle = ""`.

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

V1 and V2 read `0` today (F-4); V4-V8 end in an exception today (F-5 (a)). E17 is pinned by reading only, which is a report line.

## §8. Every `artifact_root(` call the grep finds, with a verdict

Grep: `artifact_root\(` over `ai-packages/qa-factory`, excluding `tests/`. It gives 120 lines in 51 files at 0a0db4f. The t-289 files
are byte-identical at ca2f04a. Of the files that differ, `guard_pre_tool.py` and `runtime_paths.py` changed between the snapshots (critic
t-300), so their line numbers below may have shifted. OF4-10r re-greps them. The positive control is `hooklib.py:691 def artifact_root`.
The callers of `artifacts_dir` are transitive and belong to the OF4-10r census.

Legend:
- E: edited here.
- C: inside an except that catches `ValueError` / `Exception`, verified by reading.
- P: propagates into `all_errors`, whose three callers catch `Exception` (F-7).
- L: a hooklib resolver, which propagates by design.
- F12: a writer that raises on purpose.
- X: not a call.
- U: not verified at site level; goes to OF4-10r.
- Uc: a catch claimed by an accepted spec or node, not re-read.

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
| exit_gate :207 `_named_ticket` | C (called in the try :269-272; OH6-1) |
| exit_gate :816, :818 | C (:814-820) |
| exit_gate :1161 | C (:1160-1164) |
| exit_gate :1201 | C (:1200-1202) |
| exit_gate :1257 | C (:1255-1258) |
| exit_gate :1461 | C (callers in a try) |
| exit_gate :1499, :1500 | C (:1486-1506) |
| exit_gate :1512 | C (:1856-1858) |
| exit_gate :1524 | C (:1522-1528) |
| exit_gate :120, :677, :903, :1063, :1109, :1124, :1125, :1253, :1279, :1366, :1405, :1431, :1666 | P |
| exit_gate :165, :167, :181 | P (reached only after `all_errors` returned, which a broken config prevents) |
| guard_pre_tool :609, :738, :1395, :1535 | C (excepts :620, :744, :1402, :1536; may have shifted at ca2f04a) |
| guard_pre_tool :2269 | U, hook path, no try: a likely traceback (OF4-10r, priority) |
| guard_app_under_test :265 | C (:266-267) |
| waiver :1160, :1168 | C (`except (OSError, ValueError)` :1171) |
| execution_scheduler :359, :577 | F12 |
| execution_scheduler :156 | U |
| dispatch_liveness :771 | Uc (OF4-22, 073bca8) |
| env_probe :693 | Uc (OF3-1 c) |
| role_load :538 | Uc (OF3-1 d) |
| local_keys :131 | Uc (OF3-1 d) |
| local_keys :70 | U |
| gate_shown :186 | Uc (its docstring) |
| inject_context :325, :330 | Uc |
| run_suite :3037 | U (catches `MineRefusal` only) |
| collect_pack :489, :501 | U |
| collect_pack :494 | X |
| controller :2491 | U |
| controller :2481 | X |
| red_sandbox :133, :1412 | U |
| red_sandbox :126 | X |
| host_dispatch :23 | U (analog (d)) |
| stage_guard :463, :600, :1375, :1421, :1570, :1668, :1692, :1834, :2996 | U (analog (e)) |
| runtime_paths :731 (shifted at ca2f04a; `_admits` catches `Exception`, critic t-300 Key 2) | Uc |
| archive_task :146, :194, :235; baseline_contract :66; audit_factory :454, :528, :586, :1502, :1514; check_coverage :97; dashboard_refresh :30; driver_journal :346; estimate_record :44; factory_dashboard :400, :475, :493, :675, :1029, :1245, :3061, :3915; execution_request :3246, :3248, :3252, :3253, :3258, :3260, :3262, :3265, :3267, :3881; planning_contract :362; probe_by_code :4750, :6959, :7799; source_exclusions :540; stand_identity :178, :210; traceability :1842; validate_artifacts :356 (P through `all_errors`); window_budget :301 | U |

The re-export consumers of §2.1 item 0 are `onboard_apply`, `onboarding_probe`, `config_view`, `exploration`, `project_knowledge`,
`import_test_receipt`, `controller`, `execution_scheduler`, `judge_code`, `brief_pack` and `config_contract:3031` (critic t-300 Key 2).
None needs an edit, and the identity pin of T1 covers them.

Analogs noticed and reported, not widened:
- (a) `left_out_by_person` :621-625: an import failure gives `None`.
- (b) `driver_sources.py:356` and `vcs_evidence.py:646` write or name the literal `qa-factory/artifacts/{task}`. Both are queued to
  OF4-21b, with `очередь: OF4-10 → OF4-21b` per critic t-300 Key 5.
- (c) A dangling symbolic link named `config.json` reads as absent.
- (d) `host_dispatch:23`: a broken config makes `read_event` return None for every hook.
- (e) A `stage_guard` crash may let a dispatch through (ALLOW).
- (f) `hooklib.artifact_root`'s own `project / "qa-factory"` home literal (:694, :702), for OF4-21b's list (critic t-300 N5).

## §9. Forks (with the designer's recommendations; the decisions are in §12)

- **F-1 How `artifact_root` reaches the config reader.**
  - (a) Import `config_contract` lazily in `artifact_root`.
  - (b) Move `ConfigUnreadable` and `read_config_file` into `hooklib`, and have `config_contract` re-export them.
  - (c) Keep its own `json.loads`.

  The recommendation was (a) after a measurement. **Decided (b) in §12** on the measured +0.14 s; critic t-300 reproduced +0.13 s at
  ca2f04a. The body prescribes (b) (fix round t-305, B3).
- **F-2** closed by F-12.
- **F-3 The `RecursionError` gap of the survivor.**
  - (a) Fix it in the survivor.
  - (b) Fix it in `artifact_root` only.

  Recommendation (a). §12: (a), applied to the moved `read_config_file`.
- **F-4 How far into `exit_gate`.**
  - (a) `grounding_errors`, `_identity` and `awaiting_source_review`.
  - (b) (a) plus a front probe in `all_errors`.
  - (c) `grounding_errors` only.

  Recommendation (a). §12: (a).
- **F-5 The stdout on a refusal that checked nothing.**
  - (a) `status: unknown`, `error: not_checked`, for both empty-id refusals.
  - (b) Keep `excluded`.

  Recommendation (a). §12: (a).
- **F-6 A root that cannot be listed.**
  - (a) Only "no folder" gives None.
  - (b) Keep `except OSError: return None`.

  Recommendation (a). §12: (a).
- **F-7 A root outside the project.**
  - (a) Keep accepting it.
  - (b) Refuse it.

  Recommendation (a). §12: (a), with the question on the owner's morning list.
- **F-8 `{"artifact_root": null}`.**
  - (a) Unset.
  - (b) Broken.

  Recommendation (a). §12: (a).
- **F-9 Test homes.**
  - (a) A new table in `test_read_json.py` plus rows in `ROOT_ROWS`.
  - (b) Everything in `test_read_json.py` with a `covers` edit.

  Recommendation (a). §12: (a).
- **F-10 The marker for branch (2).**
  - (a) `is_story_folder` AND `pipeline.json`.
  - (b) `is_story_folder` alone.

  Recommendation (a). §12: (a).
- **F-11 The U rows.** Residual node OF4-10r: a scout census first, then builders by file. Recommendation: open it. §12: (a).
- **F-12 The writer form.**
  - (a) A finished raise, which `run_guarded` already refuses.
  - (b) A wrapper.
  - (c) Per caller.

  Recommendation (a). §12: (a).

## §10. Small technical choices closed by the designer (no design weight)

- The new predicate is named `_story_at` and placed directly above `_story_root_of`.
- In branch (2) the deepest match decides; when it is not a story, the answer is None.
- The `grounding_errors` unknown record uses script `grounding_errors` and owner file `requirements-register.md`.
- The key-error text does not echo the value.
- The changelog fragment is `changelog.d/of4-10-artifact-root.md`.
- The T1 drivers pin the project by patching `hooklib.project_root`.
- The T2 loop: the `needle` column and `output = None`.
- Fix round: the text of the moved `RecursionError` catch is "is nested too deeply to read", followed by the existing door sentence of
  `read_config_file`.

## §11. Reading trail

**First draft** (tree `oh7-5`, 0a0db4f):
- `plans/piles/onboarding-forge/batch-4-hvosty-onbordinga-i-forzha.md` :1-30, :39, :51, :55; the finding (whole);
- `plans/piles/onboarding-forge/README.md` :21, :169; `plans/PILES.md` :88; `plans/builder-rules.md` :14-73;
- `docs/SIBLING_MAP.md` axes 8, 16, 17, 32-34; `design/architecture.md` :105-292;
- the t-129 spec (:310-318, :410-449) and the t-282 spec §7;
- scripts: `hooklib.py` :28-127, :252-400, :660-870; `config_contract.py` :16-30, :1315-1380; `vcs_evidence.py` :560-681;
  `exit_gate.py` (as listed in the first draft); `driver_dispatch.py` :290-314; `story_step.py` :2080-2104; `role_cli.py` :100-198;
  `source_exclusions.py` :72-77, :290-331; `driver_sources.py` :352-416; `subagent_journal.py` :195-224; `stage_guard.py`;
  `guard_pre_tool.py`; `scenario_walk.py` :833-931;
- tests and fixtures: `test-layers.json`; `test_read_json.py`; `test_vcs_evidence.py`; `harness.py` :257-318;
  `judgment-census.json`; `references/config-keys.json` :783; `.git/logs`.

**Fix round t-305** (tree `read-main`, ca2f04a):
- the critic report t-300 (whole);
- `hooklib.py`: a grep for `^import json|^from pathlib|^def read_json|^def artifact_root|import config_contract`, which hit :5, :12,
  :691, :751, :2737;
- `config_contract.py`: a grep for `class ConfigUnreadable|def read_config_file|ConfigUnreadable`, which hit :1321, :1349, :1362-:1373,
  :2757, :3031;
- this spec's §12.

**Needed beyond the manifest:** the critic report.

**Not done:** `git log --grep OF3-1` (no shell). I did not re-run `refusal_registry.sites()`; I rely on critic t-300's measured
rerun.

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

F-1 (b) shape (B3, t-300; appended by fix round t-305, verbatim; the decision above is unchanged): `ConfigUnreadable` and `read_config_file` move VERBATIM into `hooklib` (they need only `Path`, `json` and the class: no other `config_contract` name; checked at ca2f04a), with the F-3 `RecursionError` catch added there; `artifact_root` calls `read_config_file(project)` directly, so no import is added to it. `config_contract.py` replaces its two definitions with ONE top-level line `from hooklib import ConfigUnreadable, read_config_file  # re-export (OF4-10)`; its own uses (`:3031`) keep the bare name. Invariant: `hooklib` never imports `config_contract` at module level (the lazy import at :2737 stays lazy); the T1 row pins `config_contract.ConfigUnreadable is hooklib.ConfigUnreadable` and `config_contract.read_config_file is hooklib.read_config_file`. The `ConfigUnreadable` docstring widens to "cannot be read as one JSON object, or names an unusable `artifact_root`" only if B1's alternative is ever taken; under B1 it stays as is. AR-12 row: "no import added on the hook path; the measured +0.13 s of `config_contract` is avoided (F-1 (b))".

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

## §13. Fix round t-305 (critic t-300 → this spec)

| item | status | how |
|---|---|---|
| B1 census unit of `artifact_root` | applied | The critic's fix line is pasted verbatim into the §1 AR-29 row and §2.1 item 3. Item 4 (`resolve`) also raises a literal `ValueError`. Added: P1c, the census-table rows, E6, the DoD 5 `sites()` check, and the T1 class-split check. Non-goals forbid touching census row :398. The coupling of Key 4 (the family stays `ValueError`, read failures are `ConfigUnreadable`, key refusals are a literal `ValueError`) is stated in the §1 AR-15 row and among the §4 conflicting pairs |
| B2 the default folder in the `left_out_by_person` refusal | applied | The fix line is pasted verbatim into §2.3. E16 is updated, and T2 checks that stderr does not contain `qa-factory/artifacts/<story>`. The existing :646 text is a non-goal, queued to OF4-21b (analog (b)) |
| B3 the body prescribed F-1 (a) | applied | The fix line is pasted verbatim as §2.1 item 0 and appended to §12 under the F-1 decision, which is otherwise unchanged. The F-1 (a) clauses are struck from §2.1 item 1 and from the AR-12 row; the AR-12 row now carries the critic's text. Header: `given` names the read-main tree and lines; owns unchanged (`config_contract.py` stays owned, for the deletion and the re-export line). §3: the hooklib row lists `artifact_root`, `read_config_file`, `ConfigUnreadable`, and the config_contract row lists the deletion plus one re-export line. Added P1b, E23, DoD 1, the DoD 4 greps and the T1 identity pins |
| AR-13 row stale control `read_json` :765 | applied | Corrected to :751 (critic Key 1). Fix-round read: `hooklib.py:751` |
| N1 `_identity` slug branch | applied | §2.6, P6 and new edge E22: the slug decides `scan_root` first, and `artifact_root()` is called only without a slug |
| N2 no stdout reader | applied as evidence | §2.4 cites it. The builder's re-grep stays, per §12 F-5 |
| N3 (t-290 E1) | declined | It concerns t-290, not this spec |
| N4 (t-290 C3) | declined | It concerns t-290; F-1 (b) here already keeps the read cheap |
| N5 hooklib's own `project / "qa-factory"` literal | applied as a note | Analog (f) in §8, for OF4-21b's list. No owned change, because the critic agrees it is correct for now |
| N6 the local `main` diverged | declined here | An environment step for the coordinator. This spec now cites the read-main tree, and its DoD uses absolute worktree paths only |
| Key 5 order | applied as a note | Analog (b): `очередь: OF4-10 → OF4-21b` |
| §8 line drift in `guard_pre_tool` / `runtime_paths` | applied as a note | The §8 preamble says their numbers may have shifted and OF4-10r re-greps them. `runtime_paths :731` is `Uc` per critic Key 2 |
