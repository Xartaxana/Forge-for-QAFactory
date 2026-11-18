# FG7-78 - the driver golden measures the whole driver, and who records a golden (draft, designer t-1413)

Pile row: `plans/piles/forge/batch-7-vhodyashchie-4.md:103`. Found by builder FG7-76 (`docs/tasks/specs/reports/t-1397-fg7-76.md:45,94`
in worktree `agent-afc82ec3aefe66f27`). Status: DRAFT; forks F1-F6 are the Lead's. Line numbers below are of the FG7-76 worktree
copy of `driver_golden.py` (FG7-76 accepted, merge pending): B1 starts after FG7-76 is on main and re-reads them there.

## 0. Target on main, measured (file:symbol)

| # | fact | carrier | how measured |
|---|---|---|---|
| m1 | the MANIFEST fingerprint hashes one file: `"story_run_sha256": sha_file(root/"scripts"/"story_run.py")` | `driver_golden.py::write_golden` :525-526 | Read |
| m2 | coverage C1 reads one file: `path = root/"scripts"/"story_run.py"`, `hits.get("story_run.py")`, returns `story_run_sha256` | `driver_golden.py::coverage_report` :589-601, :679 | Read |
| m3 | the coverage console line names one file: `coverage: story_run.py {covered} of {executable} ...` | `driver_golden.py::do_record` :756-757 | Read |
| m4 | the RECORDER already collects hits for the whole driver: `ENV_MODULES = ",".join(driver_modules(root))`; `cov_files = set(self.modules)` (stem + `.py`); `on_line` keeps a line when `basename in wanted` | `driver_golden.py::run_file` :322, `driver_trace.py::Runtime.__init__` :600,:610, `driver_trace.py::_start_coverage` :1166-1171 | Read |
| m5 | so `coverage-hits/<test>.json` already holds `driver_*.py` keys; only the REPORT and the FINGERPRINT are blind (the defect is in `driver_golden.py` alone, the recorder needs no change) | m2 + m4 | inference from m2/m4 |
| m6 | `driver_modules(root)` = the flattened `layers` of the ROOT's map, else `["story_run"]` | `driver_golden.py::driver_modules` :109-114 | Read |
| m7 | `layers` = 17 `driver_*` stems + `story_run` (18 stems); `not_driver` = `driver_journal` | `scripts/tests/fixtures/driver-layers.json` :10-11 | Read |
| m8 | `scripts/driver_*.py` on disk: 18 files (17 layers + `driver_journal`) in the FG7-76 worktree; 18 in the main checkout | Glob `**/scripts/driver_*.py` under each package root | Glob, positive control `**/scripts/story_run.py` found 1 |
| m9 | `test_driver_layers` L1 refuses a `driver_*.py` that is in neither `layers` nor `not_driver` | `test_driver_layers.py::analyse` :671-675 | Read |
| m10 | the AR-13 reader of "the driver source set" is `harness.driver_sources(root, exempt)`: story_run + sorted glob minus `not_driver`; with `exempt=None` it reads the map of the TOOL's package (`DRIVER_MAP`, :51), not of `root`; importing `harness` sets `STORY_RUN_CLAUDE`, `STORY_RUN_CODEX`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD` in the importing process (:22-45) | `scripts/tests/harness.py::driver_sources` :54-68 | Read |
| m11 | no golden exists: no `experiments/driver-golden` (FG7-76 report :45), no `freeze_package.sh` anywhere (the check_root message :205 names it) | Glob `**/freeze_package.sh` (0); control: same shape `**/crap_report.py` found 1 | Glob |
| m12 | no CI job runs `driver_golden` | Grep -i `golden` in `.github/workflows/` (0); control: same call matched `artifact` 30+ times | Grep |
| m13 | a golden is bound to ONE package directory (`check_root`, MANIFEST `package_root`), ONE Python minor (`check_python`) and ONE recorder (`check_recorder`, hash includes `driver_golden.py` bytes) | `driver_golden.py` :139-167, :193-205, :694-697 | Read |
| m14 | without a golden, compare and probe already refuse by a named line: `REFUSED: no golden recorded in <dir> (no MANIFEST.json) ...`, exit 2 (`need_golden` :459-463, called by `do_compare` :773 and `do_probe` :900); without `--golden-dir`: `REFUSED: --golden-dir is required ... e.g. <repo>/experiments/driver-golden` (:1070-1072, names a directory that does not exist) | Read | Read |
| m15 | the probe uses the golden only for identity checks; its verdict compares its own in-run control with the mutant (:917-932) | `driver_golden.py::do_probe` | Read |
| m16 | `tools/crap_report.py` reads `coverage-n0.json` as one file: `GOLDEN_KEYS = ("schema","never_run","story_run_sha256")`, `GOLDEN_FILE = "story_run.py"`; `read_hits_file` takes only the `story_run.py` key; `hits_union` requires `covered_lines` = distinct story_run lines | `tools/crap_report.py` :106-107, :311-354, :365 | Read |
| m17 | test files of a record: `rules.files.rig_glob = test_story_run_*.py` (39 files on disk, 33 contain the text `run_scenarios(`; three of them twice) + 11 `files.outside`; the docstring still says "the 12" (:15) | Glob, Grep count; `driver-golden-rules.json` :5-18 | Glob/Grep |
| m18 | recording cost from the script's own text: "A full record is minutes to an hour on a loaded machine" (:9); per-file ceilings 1200 s, five infra files 2400 s (`ceiling_seconds`, rules :20); `--coverage` needs Python 3.12+ (`driver_trace.py` :1157-1158); caps: golden 48 MiB, coverage record 256 KiB (rules :21). Stand: NONE named - every recorded file runs as `python -B <file>` with the recorder on PYTHONPATH and `no_claude.py` as the host (harness :41-45) | Read | estimate for wall time: the Lead's first recording run measures it (`record cost:` line :760) |
| m19 | `test_driver_golden.py` is in `test-layers.json` `quarantine` (row :8486, section starts :7619); no keep row names `driver_golden` | Grep `driver_golden|driver_trace` in test-layers.json: 1 hit | Grep |

## 1. Architecture

- AR-1 (closed variety is data). The driver file list is read from the map's `layers`; `driver_golden.py` names no `driver_*.py`
  file except the probe's target (`driver_dispatch.py`, FG7-76). Change check (B1 DoD): `Grep -n "driver_[a-z0-9_]*\.py|story_run\.py" driver_golden.py`
  prints only docstrings/help, `package_root`'s entry check (:64-65) and the probe's lines; reported in full.
- AR-13 (one reader of a fact). Two readers of "the driver set" exist today: `harness.driver_sources` (glob minus `not_driver`) and
  `driver_golden.driver_modules` (`layers`); L1 (m9) holds them equal on main. Which one this node uses is fork F1. Noticed, not
  widened: `test_driver_layers.family_paths` (:110-115) is a third, generic reader, although td-11a §1 (:21) says `read_modules`
  calls `driver_sources`; `audit_factory.py:2382` globs `driver_*.py` with `driver_journal` included (another set, another purpose).
- AR-14 (one artifact, one writer). `MANIFEST.json`, `coverage-n0.json`, `coverage-hits/` keep one writer: `driver_golden.py::do_record`/`write_golden`.
- AR-29. Checks this node adds or alters, with owner and census class:

| check | where | class | owner | census |
|---|---|---|---|---|
| a slice whose driver fingerprint differs from the golden's MANIFEST is refused | `driver_golden.py::slice_base` | xref | data (code) | not in census scope (`scripts/tests/`; census covers `scripts/*.py` outside it) |
| a `layers` stem with no file, or no map at all, is refused (fork F4) | `driver_golden.py::driver_modules` | shape (presence) | data (code) | same |
| per-file sha of the coverage record vs the file's bytes | `tools/crap_report.py::golden_entry` (B2) | xref | data (code) | not in census (tools/) |

  No check judges a role's output. Commit lines: `architecture:` and `judgment:` in the form whose only carrier is
  `tools/architecture_gate.py` (`LINE_RE`, `JUDGMENT_RE`, :90-91); B1/B2 carry `judgment: none -- a dev-side harness check of file
  bytes and presence, no role output is judged`.
- `variety: none -- a dev-side regression harness of the package's own driver; no project reaches it and no project difference meets it`.

## 2. Design

D1 (one list). `driver_golden.py` gets ONE function that returns the driver files `[(rel_path, Path)]` in list order; the
recorder's traced modules (`ENV_MODULES`), the provenance allowed set, the fingerprint and the coverage report all read it. Its
source is fork F1 (recommended: the root map's `layers`, i.e. `driver_modules(root)` turned into that function).

D2 (fingerprint). MANIFEST key `story_run_sha256` is replaced by `driver_sha256: {"scripts/<stem>.py": sha256, ...}` over the D1
list (story_run.py is one entry). `SCHEMA` 1 -> 2 (one constant, both files): a golden of the old shape is refused by the
existing schema line "re-record it" (no golden exists, m11, so the cost is nil). Reader of the new key: `slice_base` - a slice joins
only when `driver_sha256` equals the one recorded now (today driver files are in the allowed set, so a slice after a driver edit
joins silently and mixes two driver versions in one golden; the docstring :10 already demands one package state). `compare`
and `probe` do NOT read it: a compare across a driver change is the tool's purpose.

D3 (coverage). `coverage_report` walks the D1 list: one block per file under `driver_files: {"<stem>.py": {"sha256",
"executable_lines", "covered_lines", "never_run_lines", "never_run": [...]}}` (same item form as today: lines, function, home,
guard), plus totals `executable_lines`, `covered_lines`, `never_run_lines` and the existing `test_files_in_the_record`. The key
is `driver_files`, never `files` (`files` is the coverage.py JSON key `crap_report` dispatches on, m16 :367). Console: one line
`coverage: driver <N> files, <c> of <e> executable lines ran; <n> never ran -> <path>` then one line per file
`coverage:   <stem>.py <c> of <e>` in list order.

D4 (texts). The docstring's "the 12 `test_story_run_*.py`" becomes the rule (`rules.files.rig_glob` files with one
`run_scenarios` call) with no count; the `--golden-dir is required` example and the `check_root` door name what fork F2 decides.

D5 (who records, where). Fork F2. Recommended: a CI workflow records on the base commit and compares the head commit in the
same runner path (stable `package_root`, one Python 3.12, nobody's machine), uploading the golden and the compare log as an
artifact; triggered by hand (`workflow_dispatch`, input: base ref). It is a producer, so it is node B3 with owns.

D6 (crap_report). Fork F3. Recommended: `tools/crap_report.py` reads the D3 shape (node B2): one Entry per `driver_files` key,
basename-attributed as today's `story_run.py` key is, each with its own sha check and hits union.

## 3. Edges, each with its invariant

| # | edge | behaviour | invariant |
|---|---|---|---|
| E1 | a `driver_x.py` added after the split | L1 (canon) forces it into `layers` or `not_driver` in the same change; once in `layers` it is traced, fingerprinted and covered with no code edit | no driver file name is written in code; the list has one source |
| E2 | a driver file removed, its `layers` stem left | refused (F4 a): `REFUSED: driver-layers.json layers names <stem>, which has no scripts/<stem>.py ...`, exit 2, before any run | a file that is not there is never reported as "0 of 0 ran" or hashed as empty |
| E3 | the map missing or `layers` empty | F4: (a) refused naming the map path; (b) today's `story_run` fallback with a named line | a one-file set never passes for the whole driver silently |
| E4 | a `driver_*.py` on disk not yet in `layers` (L1 red) | the golden does not see it (it reads one list); L1 in canon refuses that tree | the golden never runs a second reader of the set to catch it |
| E5 | `not_driver` (`driver_journal`) | not in the list: not traced, not hashed, not covered | a module that only carries the prefix never counts as driver |
| E6 | hits keyed by a basename not in the list (only possible from an old slice) | not counted, one line `coverage: hits for <name> are no driver file of the list, not counted` | a line of a file outside the list never raises coverage |
| E7 | a slice recorded after a driver file changed | refused naming the changed files; door: delete the golden dir or record from a frozen copy | lines and traces measured on other driver bytes never join one golden |
| E8 | a driver file with zero executable lines | its block reads `0 of 0`, totals unchanged; no division | an empty module is visible, never an error |
| E9 | the coverage record over `caps.coverage_bytes` (256 KiB) with 18 files | the existing refusal names bytes and cap (:753-754); no truncation, no partial file | a coverage record is whole or absent (F6 decides the cap) |
| E10 | CRLF vs LF working tree | sha over the bytes as read (`sha_file`); crap_report keeps its line-ending tolerance per file | the same file in another newline form is not a different driver; one changed byte is |
| E11 | no golden in `--golden-dir` | compare and probe keep `REFUSED: no golden recorded in <dir> (no MANIFEST.json) ...` exit 2 (m14) | no verdict line, never exit 0, without a recorded golden |
| E12 | no `--golden-dir` | refused; the example path names what F2 decides, never a directory that does not exist | the door named in a refusal is a real one |
| E13 | a golden of schema 1 (story_run fingerprint) | refused by the schema line, "re-record it" | a fingerprint of the facade alone never vouches for a split driver |
| E14 | `discover` on today's 33 rig files (m17: three files hold the text twice) | B1 runs `discover` by a narrow call (ast only, no test run) and reports the count; a refusal is a stop line for the Lead, not fixed in B1 | the docstring count is never asserted from memory |
| E15 | the recording run (F2) | no stand; Python 3.12+ for `--coverage`; over 15 min (docstring: minutes to an hour; ceilings 1200/2400 s per file); never run by a builder or the designer | a builder's witness never waits on a recording run |

## 4. Builder cards

### B1 - driver_golden measures the D1 list

task: <Lead> | node: forge/7/FG7-78 | depends: FG7-76 merged
given:
C:\QAFactory\forge-repo\docs\tasks\specs\20261118-fg7-78-driver-golden-coverage-card.md (§0 m1-m19, §2 D1-D4, §3 E1-E14)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\driver_trace.py
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\driver_golden.py
non-goals: no recording, compare, stability or probe run over the rig; no edit of driver_trace.py, the rules file, the map, harness.py or test_driver_golden.py (quarantine: not run, not fixed); no CI file
handoff: C:\QAFactory\forge-repo\docs\tasks\specs\reports\t-<id>-fg7-78-b1.md
edges: E1-E14 of the spec; F1/F4 as the Lead closed them
DoD: `python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\driver_golden.py --golden-dir <empty tmp dir> compare` prints `REFUSED: no golden recorded in` and exits 2; plus the narrow witness script (full source and output in the report, never committed): (1) the D1 function on the package root returns the 18 stems of `layers` in order; (2) `coverage_report(root, {"driver_core.py": [<one executable line>], "story_run.py": [<one>]}, rules)` has 18 `driver_files` blocks, `driver_core.py` covered 1, totals equal the sum of blocks; (3) a temp root whose map copy adds `driver_ghost` -> Refusal naming `driver_ghost` (negative control); (4) `slice_base` on a temp golden whose MANIFEST `driver_sha256` differs in one entry -> Refusal naming that file; (5) `discover(root, rules)` count printed (E14); (6) the AR-1 Grep of §1 printed
test: none -- the harness's only test file is in quarantine (test-layers.json `quarantine` :8486) and no keep row covers driver_golden.py; a narrow call of the changed functions is the witness (docs/TESTING.md «Что запускать по своей правке») | expected from: spec §2 D1-D3, §3 E2, E7
siblings: harness.driver_sources (AR-13 reader, unchanged unless F1 b); tools/crap_report.py (reader of coverage-n0.json, B2); driver_trace.py (consumes ENV_MODULES, unchanged)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261118-fg7-78-driver-golden-coverage-card.md
witness scope: the DoD command and script only; `scenario_walk.py --witness-for` blocks it prints for driver_golden.py are a report line (estimate: none in keep)

### B2 - crap_report reads the per-file driver record (if F3 = a)

task: <Lead> | node: forge/7/FG7-78 | depends: B1 accepted (it reads the shape B1 writes)
given:
C:\QAFactory\forge-repo\docs\tasks\specs\20261118-fg7-78-driver-golden-coverage-card.md (§0 m16, §2 D3, D6, §3 E6, E10, E13)
C:\QAFactory\forge-repo\tools\test_crap_report.py::make_golden
owns:
C:\QAFactory\forge-repo\tools\crap_report.py
C:\QAFactory\forge-repo\tools\test_crap_report.py
non-goals: no change to the coverage.py-JSON road or to CRAP arithmetic; no package file
handoff: C:\QAFactory\forge-repo\docs\tasks\specs\reports\t-<id>-fg7-78-b2.md
edges: E6, E10, E13; a hits file whose key set misses a listed file -> that file's union is its lines from the other hits files (a test that never touched it is no error); the union per file must equal that file's `covered_lines`, else that file is refused (errs toward more CRAP, the tool's stated safe side, crap_report.py:63-64)
DoD: `python -m pytest tools/test_crap_report.py -q`
test: tools/test_crap_report.py::make_golden variant row "two driver files in `driver_files` -> each function measured on its own file's lines" | expected from: spec §2 D3, D6
test: same table row "one file's `sha256` differs from its bytes -> that file refused naming `driver_files.<name>.sha256`, the other measured" | expected from: §3 E10, crap_report.py:57
test: same table row "a schema-1 record (`story_run_sha256`, no `driver_files`) -> refused with re-record, unmeasured" | expected from: §3 E13
siblings: driver_golden.py::coverage_report (the writer, B1)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261118-fg7-78-driver-golden-coverage-card.md
witness scope: tools/test_crap_report.py

### B3 - the recording workflow (if F2 = a)

task: <Lead> | node: forge/7/FG7-78 | depends: B1 accepted
given:
C:\QAFactory\forge-repo\docs\tasks\specs\20261118-fg7-78-driver-golden-coverage-card.md (§2 D5, §3 E11, E12, E15)
C:\QAFactory\forge-repo\.github\workflows\nightly.yml (form of a 180-minute job, Python 3.12, upload-artifact@v7)
owns:
C:\QAFactory\forge-repo\.github\workflows\driver-golden.yml.proposed
non-goals: no trigger on push or pull_request (F2 sub-choice); no run of the workflow by the builder; the Lead moves the file to its live name at acceptance (enforcement-file rule)
handoff: C:\QAFactory\forge-repo\docs\tasks\specs\reports\t-<id>-fg7-78-b3.md
edges: E11, E12, E15; the base and head checkouts use ONE path (check_root, m13); a refused record (exit 2) stops the job red before compare and still uploads its log; compare exit 1 (a difference) uploads the diff and is red; only exit 0 is green; `timeout-minutes` 180 (two runs of up to an hour each, estimate)
DoD: `python -B -c "import sys,yaml;d=yaml.safe_load(open(sys.argv[1],encoding='utf-8'));print(sorted(d['jobs']))" C:\QAFactory\forge-repo\.github\workflows\driver-golden.yml.proposed` and `python -m pytest tools/test_workflows.py -q` (the reader of the folder stays green)
test: none -- a CI file has no test set of its own; its proof is the first dispatched run, which the Lead triggers | expected from: §2 D5
siblings: .github/workflows/nightly.yml, scenario-clock.yml (artifact form)
designer: C:\QAFactory\forge-repo\docs\tasks\specs\20261118-fg7-78-driver-golden-coverage-card.md
witness scope: the two DoD commands

## 5. Readers of every touched file

`tools/owns_readers.py` block: NOT attached to the brief (`facts: none`). The Lead runs
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/tests/driver_golden.py tools/crap_report.py tools/test_crap_report.py .github/workflows/driver-golden.yml --names driver_modules coverage_report write_golden slice_base SCHEMA story_run_sha256 GOLDEN_KEYS GOLDEN_FILE`
and the plan critic checks it against this table. Hand Grep below (worktree `agent-afc82ec3aefe66f27`; `driver_golden` over
`*.{py,json,yml,sh}`: 32 hits in 10 files; `story_run_sha256|coverage-n0` on main outside worktrees: 32 hits in 14 files).

| touched | reader | how it reads | verdict |
|---|---|---|---|
| driver_golden.py | test_driver_golden.py | imports it; :731 reads coverage-n0.json | quarantine: unchanged, not run (its old-shape assertions go stale; restoration owes them) |
| driver_golden.py | its own `recorder_hash` (RECORDER_FILES :139) | hashes its bytes | changes in B1: any older golden is refused as another recorder (none exists, m11) |
| driver_golden.py | tools/test_language_sites.py :266,:395 | the name as a fixture path | unchanged |
| driver_golden.py | story_run_common.py :746,:756; driver_trace.py (1 docstring hit); driver-layers.json :4,:9; driver-golden-rules.json (3); features.json (1); test-layers.json :8486 | prose / skip lists / quarantine row | unchanged |
| MANIFEST.json (shape) | driver_golden.py only (`need_golden`, `slice_base`, `provenance`, checks) | keys | changes in B1 |
| coverage-n0.json (shape) | tools/crap_report.py (`GOLDEN_KEYS`, `golden_entry`, `hits_union`, `read_hits_file`) | keys, sha, hits | changes in B2 (F3 a); with F3 b/c it stays unchanged and refuses the new shape as "unknown shape" (unmeasured, errs to more CRAP) |
| coverage-n0.json | tools/test_crap_report.py :436,:481 (fixture of the old shape) | builds the record | changes in B2 |
| coverage-n0.json | docs (td-11a :182, SIBLING_MAP :172, BACKLOG :532, calibration/review reports) | prose | unchanged (td-11a row 17's debt line is closed by this node: the Lead notes it) |
| ENV_MODULES value | driver_trace.py `Runtime` :600 | stems | unchanged values (same list); changes only with F4 a on a broken map (refused before any run) |
| crap_report.py | tools/test_crap_report.py | imports | changes in B2 |
| .github/workflows/ (new file) | tools/test_workflows.py (asserts three named workflows exist), tools/ci_read.py, tools/owns_readers.json, tools/test_quarantine.py, usage_report/transcripts/journal_echo (Grep `\.github/workflows|workflows/` in tools/: 12 files) | folder scans | unknown per file (estimate: a fourth file is ignored); B3 runs test_workflows.py; the owns_readers block decides the rest |

## 6. Test cost (docs/TESTING.md)

- B1: no test line (quarantined harness test, no keep row); the witness is one CLI refusal (seconds: `discover` parses ~44 files
  with ast, then `need_golden` refuses before any run) and one narrow script over pure functions on temp trees (seconds). No
  slow-list or canon-only file is run; none is named in `DoD:`.
- B2: three table rows in an existing forge test file, strongest first; `tools/test_crap_report.py` runs in seconds (estimate).
  Rows stop where B2's test lines reach its code lines («Бюджет / Объём»); the rest are reported as not written.
- B3: no test; the two DoD commands take seconds. The real proof - one dispatched CI run - costs two recording runs: estimate
  30-120 min of CI (docstring "minutes to an hour" each); the Lead triggers it, no builder waits on it.
- Nobody runs `record` locally in this node.

## 7. Forks (returned, not decided)

- F1 - which reader gives the driver list. (a) RECOMMENDED: the root map's `layers` (today's `driver_modules`), the one list the
  recorder already traces and collects hits for (m4); bound to the disk by L1 (m9); reads the ROOT's map, right for `--package <copy>`.
  Cost: a second reader of the set stays (AR-13), held by L1. (b) `harness.driver_sources(root, exempt=<root map not_driver>)` for
  all four uses: one reader per AR-13; cost: importing `harness` sets three env variables in the recorder's parent that every test
  child inherits (m10) - possibly another trace shape; needs a measured stability run before it is trusted.
- F2 - where a golden lives and who writes it. (a) RECOMMENDED: a hand-triggered CI workflow, base record + head compare in one
  runner path, golden as an artifact (B3); fits m13 (one root, one Python) and "the canon runs in CI". Sub-choice: also on
  pull_request touching `scripts/driver_*.py|story_run.py` (cost: ~1-2 h CI per such MR, estimate). (b) the Lead records locally per
  change from a frozen copy at a fixed path; needs a producer for the missing `freeze_package.sh` (a node with owns) and an hour of
  this machine. (c) a golden committed to the repo (`experiments/driver-golden/`): comparable only from the recording directory
  (check_root), up to 48 MiB, stale after any non-allowed file change (finding `plans/piles/package-ci/findings/20261009-driver-golden-manifest-hash.md`); not recommended.
- F3 - crap_report. (a) RECOMMENDED: widen it in this node (B2), same forge zone, one road for the driver's coverage. (b) keep
  top-level `story_run_sha256`/`never_run` for the facade beside `driver_files` (crap_report unchanged, still blind to the driver:
  the same defect left in tools/). (c) leave it; it refuses the new record as "unknown shape".
- F4 - a missing map or a `layers` stem with no file. (a) RECOMMENDED: refuse before any run, naming the map or the stem (no silent
  default, architecture.md § A). Cost: the quarantined test builds a temp package with no map (test_driver_golden.py :682); its
  restoration needs a map there. (b) keep the `story_run` fallback with a named line.
- F5 - the probe without a golden (m15: its verdict is its own control vs the mutant). (a) RECOMMENDED: keep `need_golden` (no
  change; the identity checks keep the probe on a known package). (b) let the probe run with a named line `no golden: identity
  checks skipped`; cost: a probe verdict on an unidentified package.
- F6 - `caps.coverage_bytes` 256 KiB over 18 files. (a) RECOMMENDED: keep; the first coverage record (F2) shows the size, a
  refusal there comes back to the Lead. (b) raise the cap now in `driver-golden-rules.json` (that file is not in any card's owns;
  a cap is the Lead's word, rules :21 / write_golden :510). Estimate input: total lines of the driver files, by the Lead:
  `python -B -c "import pathlib;print(sum(len(p.read_text(encoding='utf-8').splitlines()) for p in pathlib.Path('ai-packages/qa-factory/scripts').glob('driver_*.py')))"`.

## 8. Small choices closed by the designer

- `SCHEMA` 1 -> 2 for both MANIFEST and coverage record (one constant; no golden exists).
- Record key `driver_files` (not `files`, which crap_report reads as coverage.py JSON).
- MANIFEST key `driver_sha256` as a map path -> sha (not one combined hash): a refusal can name the file.
- `slice_base` refuses a fingerprint mismatch (E7): implements the docstring's "one package state" for the driver files too.
- Console: one total line + one line per file, in list order.
- B3 written under `.proposed`: the Lead puts it live (a CI file that can go red is treated as an enforcement file).

## 9. Reading trail

Read: driver_golden.py (worktree) :1-160, :160-239, :313-376, :440-699, :708-801, :897-936, :1064-1103; driver_trace.py :1155-1184;
harness.py :1-70; test_driver_layers.py :100-124, :660-679; driver-layers.json (Grep, :2-64); driver-golden-rules.json :1-20;
test-layers.json :8486-8499 + top-level keys; tools/crap_report.py :40-69, :305-374; tools/test_crap_report.py :425-483;
t-1397 report :1-48; td-11a (Grep); architecture.md :33-72, :173-212; TESTING.md :75-148, :213-250; pile row :103.
Glob: `**/scripts/driver_*.py` (worktree 18, main 18); `**/scripts/story_run.py` (control, 1); `**/fixtures/driver-*.json` (2);
`**/scripts/tests/test_story_run_*.py` (39); `**/freeze_package.sh` (0; control `**/crap_report.py` 1); `experiments/*/*.md` (4,
no driver-golden). Grep: `run_scenarios\(` in test_story_run_*.py (33 files, 36 hits); `golden` -i in .github/workflows (0;
`artifact` matched); `glob\(["']driver_` in scripts (2: audit_factory :2382, harness :67); `not_driver|driver_sources` in
test_driver_layers.py; `\.github/workflows|workflows/` in tools (12 files).
Contradiction noticed: td-11a §1 AR-13 row says `test_driver_layers.read_modules` calls `harness.driver_sources`; it calls its own
`family_paths` (:110-121). Not widened; offered to the Lead as a finding for the td-11 zone.

## 10. Lead decisions (18.11, Lead 501cb4e0, accepted)

- F1: (a) the root map's `layers` (today's `driver_modules`) is the one D1 list; L1 in canon binds it to disk.
- F2: (a) a hand-triggered CI workflow (`workflow_dispatch`, input base ref), base record + head compare in one runner path,
  golden and log as an artifact (B3). No pull_request trigger now: its cost (1-2 h CI per driver MR, estimate) is not
  bought before the first dispatched run shows the real time.
- F3: (a) crap_report reads `driver_files` in this node (B2).
- F4: (a) a missing map or a `layers` stem with no file is refused before any run.
- F5: (a) the probe keeps `need_golden`.
- F6: (a) keep the 256 KiB cap; the first recorded run shows the size, a refusal there comes back to the Lead.
Order: B1 (from the FG7-76 branch until it merges), then B2 and B3 in parallel after B1 is accepted.
