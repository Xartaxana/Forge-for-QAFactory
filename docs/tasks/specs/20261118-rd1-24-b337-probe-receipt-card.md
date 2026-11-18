# RD1-24 (B-337) card: a product probe of a test with no probe row leaves a receipt that counts

task: t-1337 | node: rules-debt/1/RD1-24 | feature: F19 | status: DRAFT (designer). The Lead decides; forks are in §9.
Pile row: `plans/piles/rules-debt/batch-1-phase-2.md` row RD1-24 (owns there: `red_sandbox.py`, `reporters.py`,
`test_probe_by_code.py`, "the exact file list is the plan's"). Finding: `plans/piles/rules-debt/findings/20261117-rd2-b337-raspiska-proby-dlya-ne-python.md`.

## 0. What this card answers

1. **Where the assertion site is read** for a `junit-xml` row of a non-pytest runner when the test's suffix has no
   `assertion_probes` row: in `reporters.py` (the one report-row reader, SIBLING_MAP row "Report-row readers"), through a
   **pinned-location grammar**. The probe already knows where the assertion should fail (the target's `expected_location`,
   written by the critic in the mutation request). The new step does not try to parse an unknown runtime's stack. It only
   checks whether the failure text names that exact `<path>:<line>` as a path inside the clone, using the existing frame
   walk (`reporters._frame_site` -> `frame_matches`). Recommended in F1 (a).
2. **How the receipt reaches `proof_level.reached`**: no new road. Once `target_result` returns a read site, `verify`
   accepts the proof as it does for any language. `write_sensitivity_receipts` writes the receipt with
   `scope: whole_unlisted`, because `_receipt_scope` finds no AST row and no suffix entry for `.kt`. `probe()` publishes a
   `whole_unlisted` receipt to the manifest (`tests[].sensitivity_proof.receipt_ref` and `obligation_bindings`), and
   `proof_level.reached` counts it. Everything after the site read already exists and is unchanged.
3. **The safety rule of the new step** (the invariant the whole card protects): a site found by the pinned step is used
   only when it would make a **full proof**: row `failed`, kind `assertion`, location equal to the pinned one, and the
   message matching `expected_reason` by `reason_matches`. In every other case the answer stays the typed `site_unread`
   (`incomplete`). So a weaker read can only turn `incomplete` into `accepted`. It can never turn it into `survived`
   (a verdict on the test, a blocked repeat, an author sent to repair a healthy test) or into `probe_defect`.

What it does NOT reach (said plainly; F3): runtimes whose frames name the file by basename (JVM Kotlin/Scala/Groovy
`at Pkg.Cls.m(Calc.kt:12)`), or in a non-`path:line` spelling (`File "x", line 5`, Dart `x.dart 12:5`). These stay
`incomplete` as today. The C4 row's world writes a path-form frame (`tests/Calc.kt:5: AssertionError`), so it goes green.
A real Gradle Kotlin report would not. The residual is node RD1-24b (F3), a role-judgment door.

## 1. Architecture (designer rule 1)

AR-n touched, each with the change check the DoD runs:

| AR | how it is touched | change check (in DoD) |
|---|---|---|
| AR-1 | the step is keyed on a state (`site_unread`), never on a language name or suffix literal | `git diff` of `red_sandbox.py`/`reporters.py` adds no suffix or language literal (grep `'\.(kt|java|cs|ts|py)'` and language names in the added lines: 0 hits, positive control = the same grep finds `.py` in `red_sandbox.py:51`) |
| AR-2 | a project shape with no probe row stops being a dead end for path-form runtimes; the residual keeps the factory's tooling note (F3 residual node) | the C4 row runs the changed road on a `.kt` world (a fixture unlike the default) and it reports `accepted`, not a halt |
| AR-13 | no second frame parser: the pinned grammar goes through `reporters.assertion_site(..., frames=...)` -> `_frame_site` -> `frame_matches` (THE one frame walk) | the added code holds no `splitlines()`/own regex walk over failure text outside `reporters.pinned_frames` building ONE pattern |
| AR-22 | producer `red_sandbox` -> receipt -> readers `proof_level.reached`, `window_record._probe_from_receipt`: no new field, no new reader | the receipt keys stay the same (C4 row checks `scope`, `proof_level`, `probe_tool`; `reached` reads it) |
| AR-28 | an unknown never becomes a pass: the pinned step confirms or leaves `incomplete`; a mismatch of message, path or line is unread, never accepted | variant rows E6-E9 of §4 |
| AR-29 | one altered check: `target_result`'s site decision gains a cross-reference of report text with the pinned location | class **xref**, owner **data** (code joins two artifacts: the critic's request and the runner's report). No refusal site is added (`refusal_registry.sites()` scans raises; the step raises nothing), so no census row is expected. If the census asks for one: `xref`/`data` |

Commit lines: the builder's commit carries the `architecture:` and `judgment:` lines in the form `tools/architecture_gate.py`
checks (the only carrier of that form; not copied here). Content: architecture names AR-1, AR-2, AR-13, AR-22, AR-28, AR-29.
The judgment line is `none`, with its `-- <why>`: "the new step is a data cross-reference (xref, owner data); no role
judgment is classified or refused".

Variety walk (`design/architecture.md` § A):
- `axis 3: held by table -- references/detectors.json assertion_probes (frame grammar per suffix), then the pinned-location
  confirmation in reporters.py; unknown value -> a failed row whose text names the pinned <path>:<line> inside the clone with
  the pinned message is read; any other stays incomplete with the factory's reason (never survived)`
- `axes 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13: n/a -- the change reads one report row's failure text at a location the
  critic already pinned; it meets no product build, surface, flow, source, delivery, stand, host, people, artifact language,
  size, check kind or project age`
- No `narrows` line under F2 (a). F2 (b) would add `axis 3: narrows -- row suffixes whose grammar refuses keep no
  confirmation`, which is a fork.

Axis 3's map cell changes how an unknown value is held, so the same commit edits that cell (map rule, § A "How the map is
walked"). This is a closed choice C7.

## 2. Facts (load-bearing; measured or cited with carrier)

- `facts:` (Lead): `--probe` answers `incomplete` for `.kt` + non-pytest + junit-xml and writes no receipt (t-961).
  `test_probe_by_code.py` times out at 300 s on main canons.
- `red_sandbox.py::_frame_grammar` (read, :1186-1202) returns `{}` when `AD.entry_for_suffix` has no entry, so no
  `frames` keyword is passed.
- `reporters.py::assertion_site` (read, :346-352): `junit-xml` and not pytest and `frames is None` and status
  failed/error gives `{"site_unread": "junit-xml/<runtime>", "reason": "...not read yet (B-337)"}`. With `frames` given it
  calls `_frame_site` (:429-485). That function returns `kind assertion` only when the resolved path equals the test file.
  It refuses paths outside the clone, ambiguous relative tails, and relative paths that name no file.
- `red_sandbox.py::target_result` (:1205-1236) copies `site_unread` and `site_unread_reason`. `verify` (:692-743) turns
  that into `incomplete`, and `probe_defect` takes precedence. `product_verdict` (:1478-1489): an invalid proof WITHOUT
  `site_unread`/`baseline_status` is **`survived`**. This is the danger the safety rule in §0.3 closes.
- `_receipt_scope` (:789-814): no AST row and no suffix entry gives `whole_unlisted`. `probe()` (:1855) publishes only
  `whole_unlisted` refs to the manifest. `one_check` refs are held back.
- Production callers of `target_result`: `red_sandbox.py:1744` (the probe) and `:2203` (the diagnostic variant). Both
  pass `clone_root` = sandbox and `command`.
- `test_red_sandbox_reports.py::junit_runner_that_is_not_pytest_is_incomplete` (:631-674): its fake runner writes
  `at Object.<anonymous> (<clone>/backend/Tests/XTests.cs:5:20)`, which IS the pinned location (`XTESTS_LOCATION`
  :254). The message `expect(received).toBe(expected)` is not the pinned `Assert.Equal() Failure` (:318). Under §0.3 it
  stays `incomplete`, and its `check_in` substrings hold because the reason is appended (C4).
  Without the message guard it would become `survived`. This existing test is the end-to-end witness of the guard.
- `site_unread_is_incomplete` (:983-1030) pins the `.kt` no-row unread answer with text naming `x.test.ts`, which is not
  the pinned file. It stays green.
- `test_run_suite_reports.py:973` reads `red_sandbox.py` SOURCE TEXT between `def bind_row` and `def _frame_grammar`.
- Canon class (`scripts/slow_tests.json` `files`): `test_probe_by_code.py` 206.8 s, `test_red_sandbox_probe.py` 60.5 s,
  `test_red_sandbox_reports.py` 48.1 s, `test_judgment_census.py` 96.9 s. Ceilings (`selftest.py::TEST_TIMEOUTS`):
  `test_red_sandbox_probe.py` 600, `test_red_sandbox_reports.py` 600, and `test_probe_by_code.py` none (default 300,
  `selftest.py:494`). `test_reporters.py` is in QUARANTINE (`test-layers.json` :9541), so no row goes there.
- The C4 row is NOT in commit dd27d27e as a test row. The t-961 handoff (read on disk in the worktree checkout
  `.claude/worktrees/agent-a72a37ff6d6ddc10a/docs/tasks/handoffs/t-961-rules-debt-c4.md`) says the row was removed
  because it was red. Its diff is at
  `C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/501cb4e0-b55f-46d8-9262-11b1caefad61/scratchpad/c4-draft.diff`
  (read, 96 lines). The worktree's `test_probe_by_code.py` has no `no_row_language` function: Grep 0 hits, and the
  positive control `def main` was found at :3247. This contradicts the coordinator's note "that same commit holds the C4
  red row". `estimate` until the Lead runs `git -C C:/QAFactory/forge-repo show dd27d27e --stat`.

## 3. The design (on the recommendations; each fork marks what changes)

**`reporters.py::pinned_frames(test_file, line) -> list | None`** (new, about 15 lines). It returns `None` when `test_file`
is empty or `line` is not a positive integer: nothing to pin. Otherwise it returns ONE regex with the named groups `path`
and `line` that matches a token:
- the token starts at the start of the line or right after one boundary character from a fixed set (whitespace, `(`, `"`,
  `'`, `<`, `>`, `[`, `=`);
- the token contains none of those characters;
- the token ends with the test file's path segments, each escaped, joined by `[/\\]`, and optionally preceded by a prefix
  that ends in a separator;
- then `:` + the exact line number, not followed by a digit.

These properties make the read **linear in the text length**: each start position scans one token. The pattern is built
from the request's own location and is not a list of languages (AR-1). It lives in the report reader (SIBLING_MAP row 147:
a site read enters the reader, never a consumer).

**`red_sandbox.py::target_result`** (body only, signature unchanged). After the grammar call
(`reporters.assertion_site(... **_frame_grammar(expected_file))`), only when the answer holds `site_unread` AND
`row["status"] == "failed"` AND `expected_location` parses by `_LOCATION_RE`:
1. `pinned = reporters.pinned_frames(expected_file, line)`; `None` -> skip.
2. `second = reporters.assertion_site(row, reporter, clone_root, expected_file, **hint, frames=pinned, skip_frames=[],
   frame_path="path")`. The resolution is `_frame_site`'s, unchanged: inside the clone, no ambiguous tail, the relative
   path must exist.
3. Use `second` (`location`, `failure_kind`, `frame`) only if `second["location"] == target["expected_location"]` and
   `second["failure_kind"] == "assertion"` and `reason_matches(entry["reason"], target["expected_reason"])`.
4. Otherwise keep `site_unread` as the grammar gave it. `site_unread_reason` = the grammar's reason + `"; "` + one clause
   naming which of the three pinned checks failed ("the failure text names no <loc>", "...names it outside the clone /
   ambiguously", "...names it, but the failure message is not the pinned one").

Untouched: `_frame_grammar`, `verify`, `product_verdict`, `request_status`, `_receipt_scope`, `write_sensitivity_receipts`,
`assertion_site`'s existing behaviour for every existing call, `probe_by_code`, and the notes text of `probe()` (still right
for the residual).
Docstrings updated: the module docstring sentence at :52-53, `target_result`, and `assertion_site`'s B-337 sentence. Each
says "read when the failure text names the pinned location; otherwise not read yet (B-337)".

## 4. Edge table (rule 11; each edge with its invariant)

| # | input | behaviour | invariant protected |
|---|---|---|---|
| E1 | empty report (no testcase rows) | `bind_row` binds nothing -> `not_run` -> `probe_defect` (mutated) / `not_executed` (baseline); the pinned step never runs (no row) | a run that read nothing proves nothing either way: never `accepted`, never `survived` (FR-41) |
| E2 | malformed report (XML does not parse; no `report_evidence`; unknown reporter) | `_report_rows` notes it and gives `[]` -> as E1; unchanged | same as E1; a broken input is never a receipt |
| E3 | failed row, text names no `<pinned path>:<line>` (no stack, library frames only, empty text, message only) | stays `site_unread`; reason = grammar's + "names no <loc>" -> `incomplete`, no receipt | an unread site is never a location, so never a verdict on the test (FR-59) |
| E4 | suffix WITH a row (`.cs`, `.java`, `.ts`) whose grammar READS a location (right or wrong) | the grammar's answer stands; the pinned step does not run | a vetted grammar's read is never re-read or overridden (positional invariant: the step sits after the grammar, only on `site_unread`) |
| E5 | suffix WITH a row whose grammar REFUSES (`site_unread`) | the pinned step runs (F2 a): confirmed -> read; else unread with both reasons | one road for every suffix (P31); a row never makes the factory see less than a no-row suffix |
| E6 | suffix WITHOUT a row (`.kt`), path-form text naming the pinned location, pinned message, baseline passed | read: `location` = pinned, `assertion`, `intended_failure` -> `accepted` -> receipt `scope: whole_unlisted` -> published -> `reached` = `catches_broken_product` | the role's road ends in a counted receipt (F-O2, FR-2, FR-57) |
| E7 | as E6, but the message is not the pinned one | stays `site_unread` -> `incomplete` | the pinned step never produces `survived` |
| E8 | as E6, but the path resolves outside the clone, is an ambiguous tail, or is a longer path ending in the pinned one (`src/tests/Calc.kt:5`) | stays `site_unread` | a frame of another tree (the author's own copy) or another file never proves the clone's test |
| E9 | line collisions (`Calc.kt:50` for pinned `:5`; `Calc.kts:5`) | no match -> unread | a near-miss location is never the pinned one |
| E10 | pytest report: reporter `pytest`, or `junit-xml` of a pytest command, or `command=None` | `_pytest_site` as always; never `site_unread`, so the pinned step never runs; byte for byte unchanged | pytest's rule stays pytest's |
| E11 | status `error` naming the pinned location | `_frame_site` gives kind `error` -> unread; `verify` gives `probe_defect` first (unchanged precedence) | an error is never an assertion proof |
| E12 | `expected_location` empty, without `:<line>`, `./`-prefixed or backslashed | no pin (`_LOCATION_RE` miss) or location mismatch -> unread | nothing pinned, nothing confirmed; the exact-string compare of `verify` is never loosened |
| E13 | confirmed (E6/E5) but baseline not passed | `baseline_status` -> `incomplete` (unchanged) | a red baseline never makes a red mutated run the mutation's doing |
| E14 | confirmed for a suffix WITH a row or AST row | receipt `scope: one_check` -> held back from the manifest (unchanged rule :1855) | a one-check receipt never stands for the whole test |
| E15 | `detectors.json` unreadable | `_frame_grammar` `{}` -> pinned step as E6; `_receipt_scope` -> `one_check` (its error direction) -> held back | an unreadable table never widens what a receipt claims (AR-28) |
| E16 | TRX row of a no-row suffix | built-in TRX read, unchanged (already pinned: `frames_from_the_table` `.fs` row) | L11: no grammar keyword is passed for a no-row suffix |

Temporal: the change brings no config, flag or file into existence. Only receipts, which the road already writes, now
appear for E6. Before the change: no receipt, `incomplete`. After: a receipt for E6, and E3/E7/E8 stay as before. Old
receipts are untouched.
Conflicting pairs: "reach acceptance" vs "a factory gap is never a verdict" is resolved by §0.3. "One road" (E5) vs the
existing unread pins is resolved by appending the reason (C4); both pins were read and stay green (§2).

## 5. The reused function in a gate role: error direction and adversarial inputs

`reporters._frame_site` was a reader for VETTED language grammars. Here it decides with a grammar built from the request,
for any runtime. **Allowed error direction: toward `site_unread` (`incomplete`).** A false read is possible only when the
failure text names the pinned `<path>:<line>` inside the clone AND the message matches `expected_reason` AND the baseline
passed. The remaining risk is that the pinned line is a caller frame of an exception whose message equals the pinned
reason. That is accepted and named.

Adversarial inputs that must stay unread (the variant rows draw from these):
- A1: a path outside the clone ending in the pinned path (`/elsewhere/tests/Calc.kt:5`).
- A2: a longer relative path ending in it (`src/tests/Calc.kt:5`).
- A3: `:50` / `:5x` / `Calc.kts:5`.
- A4: a path containing a boundary character (`a (1).kt`). The token cannot hold `(`, so it is unread: the safe side.
- A5: a 1 MB single line with no boundary character. The read is linear and ends unread. No timing is asserted (FR-31).
- A6: an `error` row.
- A7: the pinned location with another message.

Must be READ (positive): A8, a Windows backslash path inside the clone (`C:\sbx\tests\Calc.kt:5`); A9, a non-ASCII
directory segment in the pinned path.

## 6. Builder card (R11-f; the Lead prints the header with `python -B tools/dispatch_new.py`)

given: this card (§0-§5, §7); `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/red_sandbox.py::target_result`,
`::_frame_grammar`, `::_LOCATION_RE`, `::reason_matches`, `::_receipt_scope`;
`C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/reporters.py::assertion_site`, `::_frame_site`,
`::frame_matches`; `scripts/tests/test_red_sandbox_probe.py::project`, `::seed_green`, `::mutation_request`, `::probe`,
`::FAKE_PYTEST`; the C4 draft diff (path §2), which is the row's shape: the half-2 world only.
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/reporters.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/red_sandbox.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_red_sandbox_reports.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_red_sandbox_probe.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/design/architecture.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/changelog.d/rules-debt-1-rd1-24-b337-pinned-site.md
(F4 b: `scripts/tests/test_probe_by_code.py` in place of `test_red_sandbox_probe.py`; F5 a adds `scripts/selftest.py`)
non-goals: a judgment door (F3, node RD1-24b); basename/other frame spellings; a Kotlin or any language data row;
`node_ids.parse_collected` keeping `.py` ids only (a pytest-named command for a non-`.py` test: noticed, §11);
`probe_by_code.py`; any receipt field; `verify`/`product_verdict` precedence; `test_reporters.py` (quarantined).
handoff: `C:/QAFactory/forge-repo/docs/tasks/handoffs/<task>-rd1-24-b337.md` (the report: diff summary, witness verbatim,
the test lines written and not written, the `not run locally` lines).
edges: §4 E1-E16 and §5 A1-A9, inline in the dispatch. The positional invariant (E4) and the safety rule (§0.3) are quoted
verbatim.
DoD:
- the pinned step exists as §3 says, with the signature of `target_result` unchanged and `_frame_grammar` left in place,
  after `bind_row` (`test_run_suite_reports.py:973` slices that span);
- the C4 row (red before the fix, green after) and the variant rows pass;
- `junit_runner_that_is_not_pytest_is_incomplete` and `frames_from_the_table` pass UNEDITED;
- the AR-1 grep of §1 gives 0 added hits;
- the changelog fragment exists; the axis 3 cell is edited.
The verification run is one narrow call of the changed functions (all three files are canon class):
`python -B -c "import sys; sys.path[:0]=[r'<worktree>/ai-packages/qa-factory/scripts/tests', r'<worktree>/ai-packages/qa-factory/scripts']; import test_red_sandbox_reports as R, test_red_sandbox_probe as P; R.site_unread_is_incomplete(); R.frames_from_the_table(); R.junit_runner_that_is_not_pytest_is_incomplete(); P.no_row_language_reaches_a_counted_receipt(); P.finish('rd1-24')"`.
Plus the report lines `not run locally: test_red_sandbox_reports.py, test_red_sandbox_probe.py, test_judgment_census.py,
canon judges`, and `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
Red-before: run the C4 function once BEFORE the product edit and quote its FAIL line (`incomplete`, 0 receipts).
test lines (strongest first; one per behaviour reaching a door):
1. `test: scripts/tests/test_red_sandbox_probe.py::no_row_language_reaches_a_counted_receipt (one scenario: the C4 half-2
   world, a `.kt` test, non-pytest runner, junit-xml; accepted, one receipt whole_unlisted / catches_broken_product /
   red_sandbox.py, reached counts it through the row's receipt_ref; first check: AD has no .kt row) | expected from: §4 E6;
   finding B-337; spec 20261117 "C4 result (t-961)"; F-O2`
2. `test: scripts/tests/test_red_sandbox_reports.py::site_unread_is_incomplete (a variant table over target_result: E6
   read, E7, E8 (A1, A2), E9 (A3), E3 empty text, A5 1 MB line, A8 backslash, A9 non-ASCII; each unread row also passes
   verify -> incomplete, never survived) | expected from: §0.3, §4, §5`
3. `test: scripts/tests/test_red_sandbox_reports.py::frames_from_the_table (one variant: a .ts row whose grammar refuses
   but whose text names the pinned path is read, E5) | expected from: F2 (a), P31`
Budget: about 15 lines in reporters, 25 in red_sandbox, and 10 of docstrings, changelog and map text, against about 45 + 20
+ 6 test lines. Line 3 is the first to drop if the budget is reached («Бюджет / Объём»).
siblings: SIBLING_MAP "Report-row readers" (row 147: the site read enters `reporters.py`); "The assertion-probe table"
(row 153: a language is a data row, a factory error gives `incomplete`); axis 34 (one road): E5.
designer: C:/QAFactory/forge-repo/docs/tasks/specs/20261118-rd1-24-b337-probe-receipt-card.md

## 7. Readers of every touched file (designer rule 7)

The `owns_readers.py` block is NOT attached to the brief. Everything below is a hand grep, marked `estimate` for the
block. The Lead runs
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/red_sandbox.py ai-packages/qa-factory/scripts/reporters.py ai-packages/qa-factory/scripts/tests/test_red_sandbox_reports.py ai-packages/qa-factory/scripts/tests/test_red_sandbox_probe.py ai-packages/qa-factory/design/architecture.md --names target_result pinned_frames site_unread_reason`
and the plan critic answers the block (Q13 d).

| touched | reader (hand grep; command and count) | answer |
|---|---|---|
| `red_sandbox.py::target_result` | Grep `target_result\(` over `scripts/`: 2 production callers (`red_sandbox.py:1744`, `:2203`) + 17 calls in `test_red_sandbox_reports.py` | changes in this node (behaviour only on `site_unread` rows); existing test calls unchanged (§2 pins read) |
| `red_sandbox.py` (module) | Grep `import red_sandbox\|red_sandbox as \|from red_sandbox` over `scripts/`: 24 files, 30 hits (probe_by_code: `held_ids`, `matching_rows`, `selection_rows`; run_suite; 22 tests) | unchanged: no imported name changes |
| `red_sandbox.py` source text | `test_run_suite_reports.py:973` slices `def bind_row`..`def _frame_grammar` | unchanged if `_frame_grammar` keeps its name and its place after `bind_row` (DoD) |
| `red_sandbox.py` `site_unread_reason` | Grep count: `red_sandbox.py` 3, `test_red_sandbox_reports.py` 4; no other reader | changes in this node (appended, never replaced) |
| `reporters.py` | Grep `import reporters\|reporters as \|from reporters` over `scripts/`: 16 files (run_history, run_suite, gate_preflight, window_record, s5_precheck, probe_by_code, red_sandbox, report_adapt, 8 tests) | unchanged: only the new name `pinned_frames` is added; `assertion_site` behaviour is identical for every existing call |
| `tools/`, `.githooks/`, `.claude/` | Grep `red_sandbox\|reporters\.py\|test_probe_by_code\.py\|test_red_sandbox_probe` over `tools/`: 1 file (`tools/fixtures/dispatch_manifest/K8.txt`, a dispatch text sample) | unchanged |
| test files (2) | `test-layers.json` keep rows (:4344, :4355); `slow_tests.json` seconds (`max_drift` 5); `selftest.py::TEST_TIMEOUTS` 600 each | unchanged; +about 3 s on `test_red_sandbox_probe.py` (t-961: "about 3 s" alone, `estimate`), far under its 600 ceiling |
| `design/architecture.md` (axis 3 cell) | `dev:docs/ARCHITECTURE_INDEX.md` generator reads only the `**AR-n — title**` openers; designer/critic/Lead read the map | unchanged index; the map line changes in this node |
| `changelog.d/<fragment>` | the release assembler | new fragment; assembler unchanged |

## 8. Test plan (TESTING.md three layers) and the 300 s question

- Layer: all rows are `data_join` (the keep rows of both files say so): the report text joined with the request into a
  verdict, a receipt, and a reader. No new file. No new world beyond the C4 scenario's one world, which is the only way to
  witness `--probe` -> receipt -> `reached`. The variant rows reuse `site_unread_is_incomplete`'s `target_result` calls
  with no world (no subprocess, milliseconds).
- External-input battery (the runner's report is outside input): magnitude A5, encoding A8/A9, empty E3, broken E2
  (already pinned upstream: no new row). No limit is introduced (the read is linear), so no AT/BEYOND rows.
- **The 300 s timeout of `test_probe_by_code.py`.** The product change does not make it worse: `target_result`'s second
  call runs only on a `site_unread` row and costs one regex pass. `test_probe_by_code.py` reaches `red_sandbox` only
  through imports, and no unread row of a product probe runs there (estimate; the Lead's canon log is the measure). The
  C4 ROW does make it worse if it lands there: one more world, about 3 s, on a file at 206.8 s measured
  (`slow_tests.json`) that already crosses 300 s on loaded canons. Hence F4 (a): put the row in
  `test_red_sandbox_probe.py` (60.5 s, ceiling 600, the world's own file). Drop half 1 of the draft row, because
  `test_probe_by_code.py::non_python_test_refused` (:1084, per t-961) already pins the `.kt` refusal. The timeout itself
  is F5.

## 9. Forks (returned; not decided)

- **F1: where the site of a no-row junit-xml row is read.**
  - (a) Pinned-location confirmation, as §3 describes. Small, data-free, and reuses `_frame_site`. It covers path-form
    runtimes (pytest-shaped, Go `x_test.go:12:`, Rust `src/lib.rs:12:5`, Swift/PHP absolute `path:line`, Ruby
    `./spec/x_spec.rb:12:in`).
  - (b) A default frame-grammar data row (a new `detectors.json` key with its own reader in `assertion_detectors`). It is
    generic, and it reads the FIRST frame: JVM and Node stacks put library frames first, so it mostly reads nothing or a
    wrong frame. It needs the same full-proof guard. It must NOT be returned by `entry_for_suffix`, or `_receipt_scope`
    flips to `one_check` and the receipt is held back, which is the exact goal broken.
  - (c) The critic's judgment door only (AR-2): covers every runtime, costs a critic turn per probe, and is a new CLI.
  - **Rec (a)**, with (c) as the residual node (F3). Cost of (a): JVM-basename runtimes stay `incomplete`.
- **F2: scope of the pinned step.** (a) Every `site_unread` answer, row suffix or not: one road, P31, E5. (b) No-row
  suffixes only, which is a `narrows` line (§1). **Rec (a).** Its cost: none found. Both existing unread pins were read
  and stay green (§2).
- **F3: the residual (basename and other spellings): what closes it.**
  - (a) Node RD1-24b: the code critic's judgment of an `incomplete` product probe with failure text (AR-2 passage). It
    should be ONE door with `probe_by_code.py --judge` (`JUDGE_DOOR`: verdict `fires|other_failure|cannot_judge`, a
    quote that is a substring of the stored text, receipt `proved_by: critic`), not a second judge. Owns:
    `red_sandbox.py` (record of the text and the judge's receipt), `probe_by_code.py` (door), `proof_level.py` (if
    `proved_by: critic` needs a reader), and `test_red_sandbox_reports.py`. Test: one scenario row (`fires` -> counted
    receipt; `other_failure` -> survived; `cannot_judge` -> incomplete).
  - (b) In this node: basename confirmation when the basename is unique in the sandbox copy set
    (`receipt["original_hashes"]`). It needs plumbing the receipt into `target_result`, and a same-named file outside
    the copy set (git-ignored) would still read.
  - (c) Per-language data rows (a Kotlin row) as projects arrive. B-373 class; it never closes the open set.
  - **Rec (a) as a named node** (rule 6: a residual is a node with owns and a test). The Lead takes it to the owner if
    the owner's "separate P1" word is meant to cover it.
- **F4: where the C4 row lives.** (a) `test_red_sandbox_probe.py`, half 2 only (§8). (b) `test_probe_by_code.py` as the
  pile row says (+about 3 s on a file that times out). **Rec (a)**. The pile row's owns change (the plan's word: "the
  exact file list is the plan's").
- **F5: the 300 s timeout of `test_probe_by_code.py` (a main red in a file of this node's pile row).** (a) Widen owns
  to `selftest.py::TEST_TIMEOUTS`: the file at 600 with the class comment (FR-31: "the ceiling only keeps a green file
  green", precedent :151-159), after the Lead confirms from the canon log that it is slow-green and not a hang. (b) Its
  own node in the test-cost class (B-155). **Rec:** (a) if F4 (b); (b) if F4 (a), because the node then no longer
  touches the file. The Lead says which pile owns it.
- **F6: should a receipt say its site was read by the pinned step?** (a) No new field (rec): `scope` already says the
  factory has no reader for the language, and the result's `frame` carries the raw line. (b) A `site_read` field inside
  the receipt hash. It needs a reader (AR-22), and none exists.

## 10. Small choices closed (no design weight)

- C1: the pattern is built in `reporters.py` (SIBLING_MAP row 147), not in `red_sandbox.py`.
- C2: reuse `assertion_site(frames=...)` -> `_frame_site`. No new resolver.
- C3: `target_result` keeps its signature, so both callers and the 17 test calls are untouched.
- C4: `site_unread_reason` is appended, never replaced. Existing `check_in` substrings hold.
- C5: `_frame_grammar` keeps its name and place (the source-slice reader).
- C6: docstrings at module :52-53, `target_result`, and `assertion_site` say the new rule.
- C7: the axis 3 map cell is edited in the same commit (map rule).
- C8: a changelog fragment under `changelog.d/` (builder.md rule; `CHANGELOG.md` is untouched).
- C9: the C4 row's first check (AD has no `.kt` row) stays, so a future Kotlin row names itself instead of passing
  silently.

## 11. Noticed, not widened

- The coordinator's note vs the t-961 report about the C4 row in dd27d27e (§2): the row is in a scratchpad diff, not a
  commit.
- A pytest-named command cannot select a non-`.py` test (`node_ids.parse_collected` keeps `.py`). pytest itself collects
  `.py` only, so this is a real-world non-case. It is listed, and no fork is raised.
- `probe()`'s incomplete note ("record it as a `tooling` finding") stays right for the residual. Under F3 (a) it becomes
  "the critic judges it". That edit belongs to node RD1-24b.

## 12. Reading trail

Pile row RD1-24 (Grep with `-o` windows, :43, :51, :52). Finding B-337 rd2 (whole). Execution-probes finding B-337
(whole). Spec 20261117 :1895-1912. t-961 handoff (worktree checkout, whole). C4 draft diff (whole).
`red_sandbox.py` :44-55, :590-612, :630-831, :831-902, :970-992, :1150-1236, :1478-1517, :1725-1749, :1800-1889,
:2185-2209. `reporters.py` :300-489. `assertion_detectors.py` :248-391. `detectors.json` :325-349 + Grep of suffixes and
frames. `proof_level.py` :1700-1739 + Grep. `probe_by_code.py` :55-79, :3255-3284, :8090-8113 + Grep.
`test_red_sandbox_reports.py` :205-256, :317-327, :631-680, :975-1031, :1318-1389 + Grep of defs.
`test_red_sandbox_probe.py` :40-164, :266-283, :1015-1038 + Grep. `test-layers.json` :4-19, :3695-3714, :4340-4368,
:9538-9548. `slow_tests.json` :1-12 + Grep. `selftest.py` :108-160 + Grep. `TESTING.md` :75-114 + Grep.
`architecture.md` :1-128, :173-197 + Grep. SIBLING_MAP :147, :153. `judgment-census.json` Grep. `refusal_registry.py`
Grep. Grep counts are quoted in §7. Negative claims (no C4 row in the worktree; no census row for `target_result`) are
each paired with a positive control of the same shape (`def main` at :3247; `red_sandbox.py` rows at census :900-914).
No test was run, and no probe was needed: the t-961 run is the measurement of the red.

## Lead decisions (Lead, 18.11.2026, Opus; «решила сама»)

F1 = (a) pinned-location confirmation through `reporters._frame_site`, used only for a full proof (§0.3). F2 = (a) every
`site_unread` answer goes the one road. F3 = (a) the residual is node RD1-24b (one judgment door shared with
`probe_by_code.py --judge`), filed in the rules-debt pile in the same commit as these decisions. F4 = (a) the C4 row lives in
`test_red_sandbox_probe.py` (half 2 only), so `test_probe_by_code.py` is not touched. F5 = (b) the 300 s timeout of
`test_probe_by_code.py` is not this node's: it already sits in PC4-19 (card `20261117-pc4-19-tests-near-300s-card.md`, its
fact rows 16-22). F6 = (a) no new receipt field. Owns as §6 without the F4 (b) / F5 (a) alternates. critic on this card:
skipped -- every fork follows the designer's recommendation; the code gets the topic critic.
