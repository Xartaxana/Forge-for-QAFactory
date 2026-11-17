# t-990 critic: code gate of topic «forge test rules» (S-C t-988, S-E t-982)

Spec/DoD: `docs/tasks/specs/20261117-forge-test-rules-spec.md` §5.1, §5.3, §7.1, §7.5, §10, Lead decisions L-1..L-9.
Diff 1 is STAGED in `.claude/worktrees/agent-ade5415f4e3e60c56` (read by `git -C … diff --cached`). Diff 2 is
`5af9e10c` + `fe0a3b17` on origin/main.

**Verdict per diff:**
- **S-C (the `test:` line gate): fit_with_fixes.** One BLOCKING false refusal (C-F1, `**test**:`) and one smaller
  false refusal (C-F2, a WHERE path starting with `none-`). Both must be fixed before the Lead commits this
  self-activating file. The rest are fix-this-round items.
- **S-E (the probe runner): fit_with_fixes.** The restore invariant holds empirically for pass, fail, timeout with a
  live grandchild, KeyboardInterrupt and pre-touch refusals. Two exception paths break the spec's outcome contract:
  a failed RESTORE write leaves the tree mutated and exits 1 (the `survived` code) with a traceback instead of 2
  `restore-mismatch` (E-F2), and a failed child start exits 1 with a traceback while the `invalid` branch written for
  it is dead (E-F1).

Accepting either diff is the coordinator's decision (critic role rule 6). This verdict is an input to it.

---

## Diff 1 — S-C

### K2 The gate's two errors (empirics first)

Probe: `scratchpad/k2/probe.py` calls `dispatch_manifest.check()` from the worktree on hand-built payloads. The
over-threshold base has 3 absolute owns, `designer: skip -- small` and `siblings: none -- standalone`. Verbatim
outcomes (exit, and the head of the message or note):

| case | exit | outcome |
|---|---|---|
| below threshold (1 owns), no test line | 0 | `''` |
| over, with `test: tools/test_x.py::tbl \| expected from: spec 5.1` | 0 | DESIGNER-SKIP note only |
| over, without | 2 | `Missing: test (no line)` |
| `manifest-skip: test -- spec accepted before the test line (x)` | 0 | `MANIFEST-SKIP: dispatch sent without test on purpose: …` |
| `manifest-skip: TEST -- r` | 0 | skip note |
| `manifest-skip: test` (no reason) | 2 | `MANIFEST-SKIP REFUSED: … no reason after --. … items: given, …, designer, test` |
| `manifest-skip: tests -- r` | 2 | `unknown item 'tests' … items: …, test` (the door can be copied) |
| line only inside a fence | 2 | `test (no line)` |
| line only in a `> ` quote | 2 | `test (no line)` |
| `test:` empty | 2 | `test (ill-formed: test:)` |
| `test: none -- doc only \| expected from: spec 2` | 0 | pass |
| `test: none -- doc only` (no source) | 2 | ill-formed |
| `test: none \| expected from: x` | 2 | ill-formed |
| `test: none.py \| expected from: x` | 0 | pass (reason read as `py`) |
| **`test: none-left.py::t \| expected from: x`** | **2** | **`ill-formed` — FALSE REFUSAL (C-F2)** |
| `test: none_x.py \| …` | 0 | pass |
| **`**test**: tools/t.py::a \| expected from: s`** | **2** | **`test (no line)` — FALSE REFUSAL (C-F1)** |
| **`- **test**: …`** | **2** | **`test (no line)` — FALSE REFUSAL (C-F1)** |
| `**test:** …` | 0 | pass |
| `` `test: … \| expected from: s` `` and `` `test:` … `` | 0 | pass |
| CRLF line ends | 0 | pass |
| `test: a \| b \| expected from: s`, `Expected From:` | 0 | pass |
| `test: tools/x.py` / `… \| expected from:   ` / `… expected from: **` | 2 | ill-formed |
| `… expected from: -` | 0 | pass (nonsense source: a false pass the spec accepts, q5 catches it) |
| `Test row: …` | 2 | no line |
| line after `siblings:`, line under the owns paths, indented 2/3/4 spaces, tab, under a numbered item | 0 | pass (`scratchpad/k2/probe6.py`) |
| `### test: …`, `1. test: …` | 2 | no line (not in the spec's pass list; the header grammar takes `###`, see C-F1) |
| critic / designer / scout kinds (3 numbered items, no test line) | 0 | `''` — untouched |
| `designer: resubmission t-123`, no test line | 2 | `test (no line)` (E-C1: refused like any other) |
| resubmission + `manifest-skip: test -- spec accepted before the test line (docs/x.md)` | 0 | skip note (E-C1 door works) |

The full gate path was also checked: `dispatch_gate.decide_full` refuses the same over-without dispatch with code 2
and the same INCOMPLETE text (`probe2.py`). A `test:` line with an absolute path placed directly under `handoff:`
joins `handoff_paths` (`['…/r.md', '…/tools/test_a.py']`). On a real root, `decide_full` still lets a builder dispatch
built that way go out with code 0 (`probe4.py`), so this is no refusal today (see K7).

**Refusal form (FR-1/2, P15):** the refusal says what is wrong (`Missing: test (no line | ill-formed: <line>)`), what
is expected (the `test:` hint, verbatim from spec item 4) and both doors (`manifest-skip:` and `dispatch_new.py`).
`dispatch_new.py` prints it whole even with `PYTHONIOENCODING=cp1252` (run witnessed). The gate itself reconfigures
stderr to utf-8 (`dispatch_gate._reconfigure_stderr_utf8`). Builder question 2 is closed: no crash.

### K1 Fit to §5.1, item by item
1. `test_lines` / `_test_candidates`: unquoted lines only ✓, first `| expected from:` splits ✓, source must be non-empty ✓.
   **Deviation (C-F1):** the spec says "optional `**`" and its pass list includes "a bulleted / bold / backticked key".
   `_TEST_KEY_RE` takes `**test:**` but not `**test**:`. That is the most common markdown bold key, and the sibling
   grammar accepts it: `_IDS_HEADER_RE` (`dispatch_manifest.py:768`) has `(?:\*\*)?(task|node|feature)(?:\*\*)?[ \t]*:`,
   and `_HEADER_RE` (`:185`) has `\b[^\n:]{0,160}:`. **Deviation (C-F2):** the none-form trigger
   `_TEST_NONE_WORD_RE = none(?!\w)` catches any WHERE that starts with `none` followed by punctuation. Then
   `_NONE_ANSWER_RE` refuses `none-left.py::t` (a single `-` is not a separator).
2. Threshold, kinds and degraded cut ✓: over at 3 owns / 3 numbered items; not under it; not for critic, designer or
   scout; the degraded cut returns early with the unchecked note.
3. One token ✓ (`SKIP_ONLY_ITEMS`, `_DISPLAY`).
4. Iteration sites ✓. Each one the builder lists was checked in the diff: `_parse_skip_line`, `SKIP_REFUSED_TEMPLATE`,
   `newly`, `still`, `_DISPLAY`, `_FORM_HINTS`, `_expected_forms`. There is one display site over `KEY_GROUPS` that the
   spec list does not name: `UNCHECKED_NOTE_TEMPLATE` (`:165-167`, "check … by eye"). It does not name `test` (C-F6).
5. Door ✓. 6. Switch ✓ (`TEST_LINE_REFUSES = True`; with it off you get a note, exit 0; the builder's test covers it).
7. `dispatch_new --test` ✓: repeatable, printed right after `DoD:`, empty and backtick values refused.
- E-C1/E-C4 ✓ (shown in K2). E-C3 ✓: the report lists the turned cases, and the test PARTS default gained a line, so no
  check was weakened.

**Builder questions:**
- **q1 (the note text for the switch-off state):** it is not dead by design. Spec item 6 requires the note, so the
  branch stays. The text is wrong, though: it says "add the line in the form the INCOMPLETE text names", and with the
  switch off no INCOMPLETE text is printed. The sibling `FORM_NOT_ENFORCED_NOTE_TEMPLATE` (`:173-176`) has the same
  defect. Both are fixed in C-F5.
- **q2:** closed above.
- **q3 (`none.py` takes the none-form):** passing `none.py` is harmless, since a path line should pass. The actual
  hole is the opposite direction: `none-left.py` is falsely refused (C-F2). The right reading: WHERE is the none-form
  only when it is the bare word `none` followed by whitespace, `--`, `—` or the end
  (`none(?=\s|--|—|$)`). With that trigger, `none.py`, `none-left.py` and `none_x.py` are paths, and bare `none` and
  `none -- -` stay refused.

### K4 Tests (S-C)
- Expected values come from §5.1, and the ids name the case ✓. Control re-run: 790 passed (below).
- Gaps: there is no row for `**test**:` (the bold key the spec lists, only `**test:**` is tested), no designer-kind
  row (critic and scout only), no resubmission rows (E-C1), and no AT row for the 80-char cut. The report claims
  "AT (74 w's … makes 80) and beyond (200)", but the table has only the 200-w row (`refuse-ill-formed-label-cut-at-80`):
  **that report claim is not backed by a row**.
- `pass-huge-line-at-limit` names a limit that does not exist (`md_regions.MAX_TEXT_CHARS = 2_000_000`; the 100k
  row is not degraded, as `probe5.py` shows `degraded False`). The label is wrong.
- `test_test_line_skip_door_and_reader_and_switch` holds 6 behaviours in one unparameterised test: unknown item,
  no reason, the skip note, the reader, the switch, the degraded cut. A red line does not name the case (P16
  condition, TESTING.md). Fixed in C-F4.

### K5 Duplication and code quality (S-C)
- DUPLICATION: `_TEST_KEY_RE` is a third key-prefix regex beside `_HEADER_RE` (`:185`) and `_IDS_HEADER_RE` (`:768`),
  each with its own prefix grammar. The divergence is exactly what produced C-F1. Reuse: `_NONE_ANSWER_RE`,
  `_WORD_CHAR_RE`, `cut.quoted`, `_parse_skip_line` and the one cut ✓. There is no second parser of the header
  section grammar: the test line deliberately stays outside `KEY_GROUPS`, per the spec. Grepped:
  `re.compile(r"^[ \t]*(?:[-*•]` shapes in `dispatch_manifest.py`.
- CODE QUALITY:
  - `designer_threshold(cut)` is now computed twice per check (in `_form_missing` and in `check_cut`). Work is
    repeated, and two readers of the same counts can drift.
  - `WHAT_DEGRADED ="…"` lost its space (a whitespace regression in the diff).
  - The test hint text is fine.
  - No new function is over 60 lines.

### K6 Mechanism form (S-C)
- (a) cost: true. (d) on the path: true. `dispatch_gate.decide_full` → `check_cut`, witnessed by `probe2.py` code 2.
- (c) detector: «Forge test discipline» (a) is **not registered yet**. `git grep -i "forge test discipline" origin/main
  -- PROCESS` finds 0; the same call over `docs/TESTING.md` finds `:234` (positive control). It lands with S-B (§9).
  The S-C commit must land with or after S-B's calibration check, or name the gap in its commit message. Otherwise
  (c) is false at commit time.
- Axis block, the «covered» lines checked against the diff:
  - axis 13: true for the cut and the skip vocabulary. But a new cut reader (`test_lines`) is not added to
    SIBLING_MAP axis 13 «Readers of the cut» (rule 9: a new symmetry goes into the map in the same commit) → C-F9.
  - axis 34: true literally ("every builder dispatch"), but see the one-road question (rule 19 line).
  - axes 1/31/32: their truth depends on S-B landing (designer.md rule 1, the SIBLING_MAP row).
  - axis 12: n/a for S-C itself.

### K7 Class completeness (S-C)
Siblings walked per SIBLING_MAP axis 13:
- The other header checks in `check_cut` share the same refusal shape (INCOMPLETE + `_items_text`) ✓. The
  manifest-skip refusal lists `test` ✓.
- `UNCHECKED_NOTE_TEMPLATE` does not name `test` → C-F6.
- The two "NOT ENFORCED" note templates → C-F5.
- `dispatch_gate.py`: no code change needed. It calls `check_cut` (witnessed).
- `hook_liveness_probe.py:1274` references `INCOMPLETE_TEMPLATE` by name only; it is unaffected.
- `dispatch_new.py` prints the line ✓, and its usage docstring is updated ✓.
- `test:` is not in `SECTION_STOP_RE`, so the line is absorbed into the extent of the section above it. An absolute
  WHERE right under `handoff:` becomes a second handoff candidate (`probe2.py`). That is harmless for builders today
  (code 0 on a real root, `probe4.py`). It is a known trait of every non-header line, and the spec keeps the grammar
  (non-goal). It goes into the C-F9 map row as a stated trait, not a fix.
- CLAUDE.md R11-f: after S-C it no longer lists every line the gate refuses without. L-9 (b) accepted this knowingly
  (the boot budget). It is not reopened here.

**What S-B must carry so that text and gate agree:** designer.md rule 1 states:
- the two forms verbatim: `test: <file::table> | expected from: <source>` and `test: none -- <why> | expected from:
  <source>`;
- the trigger: a builder dispatch at 3 owned paths or 3 numbered items;
- the line stands outside fences and blockquotes, as a plain or bulleted line (not numbered, not a heading);
- the transition door `manifest-skip: test -- spec accepted before the test line (<spec path>)`;
- `dispatch_new.py --test`.

S-B also needs: the calibration check «Forge test discipline» landing with or before S-C, the axis 31 SIBLING_MAP
row, and the axis 13 reader row of C-F9 (S-B owns `docs/SIBLING_MAP.md`). AGENTS.md is generated. It needs no change
for S-C because CLAUDE.md R11-f is unchanged.

### S-C fixes (exact instructions for a Sonnet builder; owns: `tools/dispatch_manifest.py`, `tools/test_dispatch_manifest.py`)
- **C-F1 (BLOCKING):** in `dispatch_manifest.py`, define one prefix constant
  `_KEY_PREFIX = r"^[ \t]*(?:[-*•][ \t]+)?(?:\*\*)?"` and use it in both `_IDS_HEADER_RE` and `_TEST_KEY_RE`.
  `_TEST_KEY_RE` becomes `_KEY_PREFIX + r"(?P<tick>`)?test(?:\*\*)?[ \t]*:(?:\*\*)?(?P<rest>.*)$"` (IGNORECASE).
  Rows in `_TEST_LINE_ROWS`: `pass-bold-key-inner` (`**test**: tools/t.py::a | expected from: spec`) → None, and
  `pass-bullet-bold-key-inner` (`- **test**: tools/t.py::a | expected from: spec`) → None. Existing rows stay green.
- **C-F2:** `_TEST_NONE_WORD_RE = re.compile(r"none(?=\s|--|—|$)", re.IGNORECASE)`. Rows: `pass-where-path-none-dash`
  (`test: none-left.py::t | expected from: s`) → None, and `pass-where-path-none-dot` (`test: none.py | expected from:
  s`) → None. Keep `refuse-none-without-reason-sep` and `refuse-none-reason-no-word-char` green, and add
  `refuse-none-trailing-space` (`test: none  | expected from: x`) → `ill-formed: test: none  | expected from: x`.
- **C-F3 rows:**
  - `pass-designer-kind-not-checked` (`_over(test=None)`, kind `designer`) → None.
  - `refuse-resubmission-without-line` (`build(owns=OWNS3, designer="designer: resubmission t-123", test=None)`) →
    `no line`.
  - `pass-resubmission-with-skip-door` (the same, plus tail
    `manifest-skip: test -- spec accepted before the test line (docs/x.md)\n`) → None.
  - `refuse-ill-formed-label-at-80` (`test: ` + `w`*74, exactly 80 chars) → the label is the whole line, uncut.
  - Rename `pass-huge-line-at-limit` → `pass-huge-source-100k`.
- **C-F4:** split `test_test_line_skip_door_and_reader_and_switch` into a parameterised table of door rows with ids:
  - `skip-unknown-item-tests` (code 2, `unknown item 'tests'`, `designer, test; the reason`);
  - `skip-no-reason` (code 2, `MANIFEST-SKIP REFUSED:`);
  - `skip-note-names-test` (code 0, the exact note line).

  Add separate small tests `test_test_lines_reader_reads_unquoted_well_formed_only`, `test_test_line_switch_off_is_a_note`
  and `test_test_line_degraded_cut_unchecked`. Each asserts one behaviour.
- **C-F5:** `TEST_LINE_NOT_ENFORCED_NOTE_TEMPLATE` replaces "add the line in the form the INCOMPLETE text names" with
  "add a line `test: <file::table> | expected from: <source>` or `test: none -- <why> | expected from: <source>`
  (docs/TESTING.md «Строка теста в DoD»)". Same class: `FORM_NOT_ENFORCED_NOTE_TEMPLATE` names its forms inline,
  reusing `_FORM_HINTS["siblings"]` and `_FORM_HINTS["designer"]` through `_items_text`'s items. Rows: the switch-off
  test asserts `expected from:` in the note. The existing `test_form_switch_off…` asserts the siblings form appears in
  its note.
- **C-F6:** build `UNCHECKED_NOTE_TEMPLATE`'s list over `[_DISPLAY[i] for i in _ALL_ITEMS]`, so that it names `test`.
  The degraded-cut test asserts `test` in the note.
- **C-F7:** restore `WHAT_DEGRADED = "…"`. Compute `counts = designer_threshold(cut)` once in `check_cut` and pass it
  to `_form_missing(cut, missing, counts)`.
- **C-F8:** report line plus commit line `tests-over: the spec's pass/refuse list for outside input (dispatch text) and
  the E-C3 expectation edits` (test diff 133 lines vs code+text 93, counted from `--stat`).
- **C-F9 (owner: S-B / the Lead at commit, not this builder):** in SIBLING_MAP axis 13, the row «Readers of the cut»
  gains `dispatch_manifest.test_lines` (the one reader of the `test:` line, a skip-only item outside the header
  grammar; the line is absorbed into the extent of the section above it).

---

## Diff 2 — S-E

### K3 The restore invariant (empirics first)
Every probe ran on a fresh temp directory (`scratchpad/k3/probe.py`), never on the repo tree. The target was a
BOM+CRLF `mod.py`; "identical" means the sha256 before equals the sha256 after:

| case | exit | outcome | identical | wall |
|---|---|---|---|---|
| pass (equivalent mutant) | 1 | survived | True | 0.1 s |
| fail | 0 | killed | True | 0.1 s |
| timeout (TIMEOUT_S=1) with a live grandchild holding the output | 3 | invalid | True | 1.0 s |
| pytest, fixture error only (exit 1, errors only) | 3 | invalid | True | 0.6 s |
| `Popen` raises OSError | **traceback (OSError), CLI exit 1** | none | True | — |
| KeyboardInterrupt in `wait` | propagates | none | True | — |
| **restore `write_bytes` raises PermissionError** | **traceback, CLI exit 1** | **none** | **False** | — |
| `--old "-y"` | 64 | `refused: bad arguments: argument --old: expected one argument; …` (does not name `--old=`) | — | — |

The outcome table of §5.3 is kept for every row it lists. An `invalid` is never reported as killed: the crash,
import-break and no-tests rows are covered by the builder's table, and my errors-only row agrees. Two departures:
- **E-F2:** when the restore itself fails, the target stays mutated. The run ends in an uncaught exception, so
  `python -B mutate_once.py` exits 1, the `survived` exit code. No sha line and no `outcome:` are printed. §5.3 says
  "sha256 after != before → 2 restore-mismatch (wins over every other outcome)", and E-R1 says "exit 2 when not
  [byte-identical]". Nor can the original bytes be recovered: the copy is in memory only. E-R7's
  `git status --porcelain` would catch it in a tree, but the runner itself breaks its own table.
- **E-F1:** when `open`/`Popen` raises, `finally` restores the target (verified), but the exception propagates:
  exit 1 again, no outcome line. The `elif unreadable or not started_ok` branch ("the child did not start") is
  **dead**, because `started_ok` is False only on a path that has already raised. That is a dead branch with a lying
  label (brief item 7).

### K1 Fit to §5.3; the builder's minimum readings
- Interface, `--root` on both forms, the usage text names `--root`, argv/cwd, Popen to ONE temp file in
  `TemporaryDirectory(ignore_cleanup_errors=True)`, `wait(TIMEOUT_S=60)`, kill + restore at once, reap `wait(5)` after
  the restore, the output read only after the restore and sha, the pre-touch checks, `compile()` on the mutated bytes,
  E-R2 bytes ✓. Deviations: E-F1 and E-F2 above.
- Readings:
  1. The inline form requires `--root`: right (AR-4; the paths are "relative to --root").
  2. A bad spec file or id → 64: right (the table's "bad arguments" row).
  3. `--old=<text>` for a leading dash: right as the mechanism, but the refusal must name that door, which today
     only the usage docstring does (FR-1 "which argument fixes it") → E-F3.
  4. Unreadable output → `invalid` even on exit 0: right (the table row has no exit qualifier, and the error
     direction toward invalid is allowed).
- The t-971 R1 shape (no pipe, restore never waits) is kept, judged against spec §5.3 r3, which incorporates R1. The
  t-971 review file itself was not reopened.

### K4 Tests (S-E)
- Expected values come from the §5.3 table ✓. One parameterised table plus a usage row ✓; the ids name the case ✓.
  My run: 29 passed in 5.10 s (< 10 s).
- Missing rows:
  - an exception mid-run (E-F1);
  - a real restore failure (E-F2) — `restore-mismatch-wins-over-killed` patches `sha` only, so it pins the
    classification, not the restore;
  - the table's "pytest exit 1 with errors only";
  - the leading-dash refusal (E-F3).
- The adversarial list is otherwise complete: syntax error, broken import, endless loop, grandchild, wrong test path,
  no tests, crash before the summary, unreadable output.

### K5 Duplication and code quality (S-E)
- DUPLICATION: none blocking. `selftest.py:443 _PYTEST_SUMMARY` counts passed/failed for another reader. Reusing it
  would import selftest into a test helper. Grepped: `failed\|passed` + `re.compile` over `scripts` and `tools`, 2 hits.
- One road for a probe ✓: no other runner exists. `git grep -i mutate_once origin/main -- tools .githooks
  .claude/settings.json` finds 0; the positive control (`dispatch_manifest` in `tools`) finds hits.
- CODE QUALITY: `run_probe` is about 55 lines; nesting is fine. One dead branch (E-F1).

### S-E fixes (owns: `ai-packages/qa-factory/scripts/tests/mutate_once.py`, `test_mutate_once.py`)
- **E-F1:** in `run_probe`, wrap the `open(out_path, "wb")` + `Popen` in `try/except OSError as exc`. Set
  `started_ok = False` and remember `start_error = f"{type(exc).__name__}: {exc}"`. Do not re-raise. The restore,
  the sha and the outcome then run as usual, and the existing `not started_ok` branch gives `invalid`, exit 3, with
  the error in its text. Row: `popen-raises-is-invalid-restored` (monkeypatch `MO.subprocess.Popen` to raise
  `OSError`) → exit 3, `outcome: invalid`, target byte-identical.
- **E-F2:** the restore in `finally` becomes a helper `_restore(target, original)`:
  - It tries `write_bytes` up to 3 times, 0.2 s apart. On a final `OSError` it writes `original` to
    `tempfile.mkstemp(prefix="mutate_once-original-", suffix=target.suffix)` (outside the root, not deleted) and
    returns `(error_text, saved_path)`.
  - The `after` read is guarded: an `OSError` gives `after = "unreadable"`.
  - When `before != after`, print `    restore failed: <error>; the original bytes are in <saved_path>` (when there is
    an error) before `outcome: restore-mismatch`, exit 2. This must never raise.

  Row: `restore-write-fails-is-restore-mismatch` (monkeypatch `Path.write_bytes` to raise `PermissionError` on the
  second write to `mod.py`) → exit 2, `outcome: restore-mismatch`, and the saved file's bytes == the original. Adapt
  the row's final identity assert for this row.
- **E-F3:** `_Parser.error` appends `; a value that starts with '-' is written --old=<text> (or --new=<text>)` when
  `message` contains `expected one argument`. Row: `old-value-starting-with-dash-is-refused-naming-the-equals-form`
  (argv `--old -y` on a target holding `-y`) → 64, the `refused:` line contains `--old=`. Also a row
  `old-value-equals-form-runs` (`--old=-y --new=-z`) → its outcome by the table.
- **E-F4:** row `pytest-errors-only-is-invalid` (test file with a fixture whose body asserts `mod.VALUE == 1`, test
  depends on it, `--pytest`) → exit 3, `invalid` (§5.3 "pytest form: exit 1 with errors only").

---

## Standing questions (critic rules 18-20)
- **DUPLICATION AND CONSISTENCY:**
  - S-C: a third key-prefix regex (C-F1 merges it with `_IDS_HEADER_RE`).
  - S-E: none found. Grepped: pytest summary regexes over `scripts`/`tools`, and `mutate_once` readers.
- **CODE QUALITY:**
  - S-C: the double `designer_threshold`, the whitespace regression, two note texts pointing at an unprinted
    INCOMPLETE text (C-F5, C-F7).
  - S-E: a dead `not started_ok` branch with a lying label (E-F1).
- **ONE ACTION, ONE ROAD (P31):**
  - S-E: one runner for package and forge tests ✓.
  - S-C: the gate applies to `is_builder` only, while the rest of the manifest (designer included: `probe.py`
    `general-purpose-owns` carries the DESIGNER-SKIP note) also judges WRITING dispatches (non-builder with absolute
    owns). §5.1 item 2 scopes it to builders, and TESTING.md «Строка теста в DoD» says "Пункт спеки билдеру". So this
    is a documented scope, not a silent exclusion, but it has no data row and no owner's word.
  - Proposed node for the Lead (decision is the Lead's): either apply the test line wherever `check_cut` checks
    (`kind_word` in builder/writing) — a one-condition change plus rows `refuse-writing-kind-no-line` /
    `pass-writing-kind-with-line` — or record the builder-only scope as a decision line.
- **TESTS (TESTING.md «Бюджет»):**
  - S-E's `tests-over:` reason holds: outside CLI input, an outcome table the spec demands.
  - S-C names no reason; one holds → C-F8.
  - Gaps: C-F3 and C-F4 for S-C, E-F1..E-F4 rows for S-E.

## Class completeness (rule 5/9, SIBLING_MAP axis 13, 34, 3, 15)
- Axis 13: C-F5, C-F6 and C-F9 close the remaining sites, and the S-B must-carry list above aligns the texts.
- Axis 34: the S-E runner is the one road. S-C has the one-road question above, which the Lead decides.
- Axis 3: S-E has a changelog fragment (per the report).
- Axis 15: `say()` guards the console. The report witnesses `test_console_encoding` green.
- The surface of C-F1/C-F2 is "the dispatch key-line recognizer". I walked its neighbouring classes:
  - case: `TEST:` passes;
  - bold placement: C-F1;
  - backtick: passes;
  - heading and numbered markers: refused, consistent with the bullet-only spec, noted;
  - indentation and tab: pass;
  - CRLF: passes;
  - fullwidth colon: refused (builder row);
  - magnitude: 100k passes;
  - empty value: refused.
- The surface of E-F1/E-F2 is "the runner's exception paths around the mutation window". Neighbours walked: the
  Popen start, the wait (KeyboardInterrupt, fine), the restore write, the after-read (guarded by E-F2) and the output
  read (already guarded).

## Trail
Read:
- the spec §5.1, §5.3, §7.1, §7.4, §7.5, §3.4, §2.2, L-1..L-9;
- the S-C staged diff (`dispatch_manifest.py`, `dispatch_new.py`, both test files);
- `dispatch_manifest.py` (`section_cut`, `check_cut`, `_HEADER_RE`, `_IDS_HEADER_RE`, `_NONE_ANSWER_RE`,
  `designer_threshold`, `_parse_skip_line`, `cut_payload`);
- `dispatch_new.py` `_forbidden`/`_empty_item`; `dispatch_gate.decide_full` signature;
- the t-988 and t-982 reports;
- `mutate_once.py` and `test_mutate_once.py` (origin/main), the `test-layers.json` rows of both commits;
- SIBLING_MAP axis 13 head; TESTING.md «Бюджет»; critic-diff-brief items 6-7; the verdict schema.

Probes (scratchpad, not committed):
- `…/scratchpad/k2/probe.py`, `probe2.py` … `probe6.py`;
- `…/scratchpad/k3/probe.py`, plus the CLI runs of `--old -1` / `--old -y`.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "S-C C-F1: _TEST_KEY_RE refuses the bold key '**test**: <where> | expected from: <src>' and '- **test**: ...' with 'test (no line)' -- a false refusal of a form spec 5.1 lists on the pass side; must be fixed before the Lead commits the gate"
  ],
  "fixes": [
    "C-F1 dispatch_manifest.py: one _KEY_PREFIX constant shared by _IDS_HEADER_RE and _TEST_KEY_RE; _TEST_KEY_RE accepts '**test**:'; rows pass-bold-key-inner, pass-bullet-bold-key-inner",
    "C-F2 _TEST_NONE_WORD_RE = none(?=\\s|--|—|$); rows pass-where-path-none-dash (none-left.py::t), pass-where-path-none-dot (none.py), refuse-none-trailing-space",
    "C-F3 rows pass-designer-kind-not-checked, refuse-resubmission-without-line, pass-resubmission-with-skip-door, refuse-ill-formed-label-at-80 (exactly 80 chars, uncut); rename pass-huge-line-at-limit to pass-huge-source-100k",
    "C-F4 split test_test_line_skip_door_and_reader_and_switch into a parameterised door table (skip-unknown-item-tests, skip-no-reason, skip-note-names-test) and three one-behaviour tests (reader, switch off, degraded)",
    "C-F5 TEST_LINE_NOT_ENFORCED_NOTE_TEMPLATE and FORM_NOT_ENFORCED_NOTE_TEMPLATE name the expected forms inline instead of pointing at the INCOMPLETE text that is not printed when the switch is off; switch-off tests assert the form in the note",
    "C-F6 UNCHECKED_NOTE_TEMPLATE lists _DISPLAY over _ALL_ITEMS so it names test; degraded test asserts it",
    "C-F7 restore 'WHAT_DEGRADED = ...' spacing; compute designer_threshold(cut) once in check_cut and pass it to _form_missing",
    "C-F8 S-C report and commit carry 'tests-over: the spec's pass/refuse list for outside input and the E-C3 expectation edits'",
    "C-F9 (owner S-B / Lead at commit) SIBLING_MAP axis 13 'Readers of the cut' gains dispatch_manifest.test_lines and the absorbed-extent trait; S-B designer.md rule 1 carries the forms, trigger, placement, the transition door and dispatch_new --test; the Forge test discipline check lands with or before S-C",
    "E-F1 mutate_once.run_probe: catch OSError around open+Popen, started_ok False, invalid exit 3 after restore+sha (the dead branch becomes live); row popen-raises-is-invalid-restored",
    "E-F2 mutate_once: _restore helper with 3 retries; on final failure save the original bytes to a mkstemp file outside the root, guard the after-read, print 'restore failed: <err>; the original bytes are in <path>' and exit 2 restore-mismatch, never raise; row restore-write-fails-is-restore-mismatch",
    "E-F3 _Parser.error appends the '--old=<text> (or --new=<text>)' door when the value starts with '-'; rows old-value-starting-with-dash-is-refused-naming-the-equals-form, old-value-equals-form-runs",
    "E-F4 row pytest-errors-only-is-invalid (fixture error, exit 1 with errors only -> exit 3 invalid)"
  ],
  "class_completeness": "Axis 13: the iteration sites of spec 5.1 item 4 are all on _ALL_ITEMS; the remaining display sites (UNCHECKED note, the two NOT ENFORCED notes) go in C-F5/C-F6; the new cut reader test_lines needs its axis 13 map row (C-F9, owner S-B). Key-line recognizer surface walked: case, bold placement (C-F1), backtick, heading/numbered (refused, consistent with the bullet-only spec), indent/tab, CRLF, fullwidth colon, magnitude, empty. Runner exception surface walked: Popen start (E-F1), wait interrupt (ok), restore write (E-F2), after-read (E-F2), output read (ok). Axis 34: one runner (S-E); the builder-only scope of the test line versus writing dispatches is a proposed node for the Lead. Axis 3 changelog fragment and axis 15 console guard present per report.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-forge-test-rules-spec.md (5.1, 5.3, 7.1, 7.4, 7.5, 3.4, 2.2, L-1..L-9)",
      ".claude/worktrees/agent-ade5415f4e3e60c56 staged diff: tools/dispatch_manifest.py, tools/dispatch_new.py, tools/test_dispatch_manifest.py, tools/test_dispatch_new.py",
      ".claude/worktrees/agent-ade5415f4e3e60c56/docs/tasks/handoffs/t-988-sc-report.md",
      "docs/tasks/handoffs/t-982-se-report.md",
      "origin/main ai-packages/qa-factory/scripts/tests/mutate_once.py, test_mutate_once.py, test-layers.json (5af9e10c, fe0a3b17)",
      "tools/dispatch_gate.py decide_full and _reconfigure_stderr_utf8",
      "docs/SIBLING_MAP.md axis 13 head; docs/TESTING.md Budget; docs/tasks/critic-diff-brief.md items 6-7; tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "( cd .claude/worktrees/agent-ade5415f4e3e60c56 && python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate.py tools/test_dispatch_gate_md.py -q -p no:cacheprovider )", "result": "790 passed in 29.18s"},
      {"command": "python -m pytest <scratch copy of origin/main>/test_mutate_once.py -q -p no:cacheprovider", "result": "29 passed in 5.10s"},
      {"command": "( cd forge-repo && python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for .../mutate_once.py .../test_mutate_once.py )", "result": "both paths: keep test_mutate_once.py (layer table, covers it)"},
      {"command": "python -B scratchpad/k2/probe.py (dispatch_manifest.check over 40 crafted dispatches)", "result": "false refusals: **test**:, - **test**:, test: none-left.py::t; every other case as spec 5.1 says"},
      {"command": "python -B scratchpad/k3/probe.py (runner on temp copies)", "result": "pass/fail/timeout+grandchild/errors-only identical with the right outcome; Popen OSError -> traceback (exit 1) restored; restore write PermissionError -> traceback, target NOT identical"}
    ]
  }
}
```
