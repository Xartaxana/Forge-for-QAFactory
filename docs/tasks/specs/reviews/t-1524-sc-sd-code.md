# t-1524 critic: code review of S-C (t-1521, `test:` line gate) and S-D (t-1522, `mutants` in the verdict checker)

Spec/DoD: S-C = dispatch d-1521 + spec `20261117-forge-test-rules-spec.md` §5.1, §7.5; S-D = dispatch d-1522 + card
`20261118-test-rules-sb-sd-decoupled-card.md` §4 (and T2 text for rule 21, §3 lines 86-113).
Trees: S-C `.claude/worktrees/agent-aab6815809df7010e` (staged `dispatch_manifest.py`, `dispatch_new.py`; commit 31ceedd8),
S-D `.claude/worktrees/agent-a7eba3c7c2f4035a2` (staged checker + schema; commit 0be33f3b). Both based on e3ed349b.

## Verdict lines

- **S-C (t-1521): NEEDS WORK** -- 3 fixes in owns (S-C-1, S-C-2, S-C-3), fix before merge; 1 class finding outside owns for the Lead (S-C-4).
- **S-D (t-1522): NEEDS WORK** -- 2 fixes in owns (S-D-1, S-D-2), fix before merge. Card PASS list: no false refusal found.
- Merge of origin/main 29add319: NO conflict in any owned file (`git diff --stat e3ed349b origin/main -- <all 11 owned paths>` prints nothing).
- Nothing blocks outright; JSON `fit_with_fixes`. Acceptance stays the Lead's (rule 6).

## Findings

**S-C-1 (fix before merge) -- a backticked KEY is refused; spec §5.1 PASS list names "a bulleted / bold / backticked key".**
Surface: the `test:` line parser (`dispatch_manifest.py:976-1000`, `_test_line_parse`). It strips backticks only when they
wrap the WHOLE line (`:990-991`), so ``` `test:` tools/x.py | expected from: spec ``` returns None (not a test line).
Probe on the staged file: `` '`test:` tools/x.py | expected from: spec' -> None ``; `` '`test`: ...' -> None ``; full
over-threshold dispatch with only that line -> `2 DISPATCH INCOMPLETE ... Missing: test (no line)`. The builder's row
`pass-backticked` (`test_dispatch_manifest.py` TEST_ROWS) tests only the whole-line form. Neighbours walked: bullet
`-`/`*`/`•` pass, `+` and `1.` are None (not on the PASS list -- note only); bold `**test:**`, `**test**:` pass; tab
separators, `Expected  From` with two spaces pass; CRLF pass. Fix: accept an optional backtick pair around the key
(`` `test:` `` and `` `test`: ``) and add a TEST_ROWS pass row.

**S-C-2 (fix before merge) -- a well-formed test line inside the DoD extent is read as a DoD RUN command and refused.**
Surface: the seam between the new line and `_dod_run_check` (`:1080-1125`) via `_dod_commands` (`:1070-1077`), which takes
every multi-token inline span in the DoD sections as a command. The spec puts the line "inside the DoD" (§5.1 item 4 hint;
TESTING «Строка теста в DoD»), `dispatch_new.py` prints it right under `DoD:` (inside that extent), and the whole-line
backticked form is the one S-C itself accepts. Probe (same dispatch, DoD `` `python -m pytest tools/test_a.py -q` ``):
- `` `test: scripts/tests/test_story_step.py | expected from: spec 5.1` `` -> `2 DOD-RUN REFUSED ... runs the canon-only file(s) test_story_step.py whole`
- three backticked lines naming `tools/test_b|c|d.py` -> `2 DOD-RUN REFUSED ... the DoD commands name 4 test files ..., at most 3`
- the same lines unbackticked -> `0`.
A line that only NAMES where a test row lives is not a run. Fix: `_dod_commands` skips a line for which
`_test_line_parse(line) is not None` (one condition, the parser already exists); one TEST_ROWS pass row with a backticked
line naming a bare `test_*.py` file.

**S-C-3 (fix before merge; Q6/Q7/Q5(c)) -- dead public function, a duplicated loop, a doubled computation, one missing door row.**
- `test_lines` (`:1003-1012`) has NO caller (grep `test_lines\b` over the worktree `tools/`: only its def); `_test_line_state`
  (`:1015-1029`) re-implements the same quoted-skip/parse loop. Build `_test_line_state` on one walk (or have `test_lines`
  return the first bad line too) so the spec's `test_lines` is the one reader.
- `designer_threshold(cut)` is computed twice per builder dispatch (`_form_missing` `:962` and `check_cut` `:1191`): pass the
  counts once.
- `--test " "` is refused by the new `"test"` entry of `_empty_item` (`dispatch_new.py:79`) -- a new CLI refusal with no
  row; add `C1-2-empty-test-item` beside `C1-2-empty-owns-item` in `test_dispatch_new.py` CASES.

**S-C-4 (class, outside owns -- the Lead widens the commit of the staged files; not the builder's).**
At S-C's merge two texts become false about the gate it lands:
- `docs/TESTING.md:88` (origin/main): «Наличие и форму строки код пока не проверяет» -- after S-C the code DOES check
  (spec §2.2 drafted «проверяет код (`tools/dispatch_manifest.py`, ...)»; S-A1 landed the pre-S-C wording, E-C2 says
  "after: checked"). No stream of either spec/card owns this sentence after S-A1.
- `CLAUDE.md:82` R11-f lists the header lines `dispatch_manifest.py` refuses a dispatch without (`given:` ... `designer:`);
  an over-threshold builder dispatch is now also refused without `test:`. Card S-B non-goals: "CLAUDE.md beyond R11-h", so
  nobody adds it. Line for «Остатки» if not fixed in this commit:
  `TESTING.md:88 + CLAUDE.md R11-f name the test: gate | узел: <Lead opens>`.

**S-D-1 (fix before merge; Q5(a) killing power) -- no row kills the `show HEAD:` condition of restore-mismatch.**
`_mutant_errors` requires `"show HEAD:" in hits[0]` (`critic_verdict_check.py:214`). Rows: `restore-mismatch no door` uses
remark `M1` -> entry `"M1: add a test"`, which lacks BOTH the target `tools/x.py` and `show HEAD:`; `restore-mismatch no
target` has `show HEAD:` but no target. Traced: deleting the `show HEAD:` conjunct leaves every row green (the "no door" row
still fails on the target). The card's REFUSED list names "an entry lacking the target OR `show HEAD:`". Fix: make the
"no door" row's entry carry the target (e.g. `fixes=("M1: restore tools/x.py by hand", "F2 ...")`).

**S-D-2 (fix before merge; Q7) -- `_mutant_errors` is ~131 lines (`critic_verdict_check.py:102-233`), nesting 4
(for -> if survived -> elif has_rk -> if not hits).** Split the per-item body (field limits, run join, survived/restore
link) into a helper; the green-control tail stays.

## Seam and class notes

- FG7-95 READERS NOTE: `_has_readers_line`/`READERS_NOTE` untouched; the note still appended last in `check_cut` (`:1238-1239`). Survives.
- Item 4 iteration sites verified in the staged file: `_parse_skip_line :316`, `SKIP_REFUSED_TEMPLATE :168`, `newly :1206`,
  `still :1214`, `_DISPLAY.update :111`; `_expected_forms` built over `_FORM_GROUPS` (not ITEMS) -> correctly unchanged.
  Grep `\bITEMS\b` in the staged file: the remaining `for item in ITEMS` (`check_cut :1173`) is the header-section loop, which
  must not see `test` (skips form items itself) -- correct.
- The builder's hint choice (insert `_FORM_HINTS["test"]` into INCOMPLETE only when `test` is still missing): judged against
  §5.1 item 4 -- the spec names the hint, not that every refusal carries it; it appears exactly when the line is owed and
  actionable, and every refuse row asserts `"docs/TESTING.md" in msg`, so the `.replace` anchor cannot silently die. Safe; accepted as Q2.
- Known red `test_main_folds_the_coordinator_read_warn_into_additional_context[main-thread]` reproduced RED on the S-D tree
  (no S-C code): not S-C's.
- Other over-threshold builder prompts outside owns: grep `designer:\s*(skip|resub|[A-Z]:)` -i over the 12 other test files
  that import the dispatch modules -> 0 each; positive control `test_owns_gate.py` -> 1 (builder: green there). No turned case.
- S-D, spec notes (Lead's, not builder findings): the card's regex `--(test|target)\s+...` refuses `--test=<path>` (probe:
  `mutant 0: run names no --test`) and the runner's spec-file form; a control written `tools\test_x.py` fails the "contains"
  join; `run` 1-500 plus "run == command" can refuse a long `--old/--new`. T2 mandates the inline `--test <path>` form, so
  these are rule-backed refusals, not false ones; a backslash control on Windows is the likeliest real hit.
- S-D E-D1: only `_base_fit` gained `mutants: []`/`mutants_none`; `_base_fit_with_fixes`/`_base_blocker` inherit it; every
  pre-existing refusal test is built from a base fixture and asserts its own field word, so no old refusal now passes
  "for the mutants reason". No assertion weakened (diff: +87/-0 in the test file).

## Standing questions

- Q1 fit: S-C items 1-7 done except the backticked-key reading (S-C-1); S-D behaviours 1-7 as written (messages verbatim to card).
- Q2 builder decisions: S-C hint placement safe; S-D "any joined rerun with the outcome word" passes (safe direction); one-line green-control diagnostic -- fine.
- Q3 seams: S-C-2 (DoD-run reader). S-D: none; `install_parity_anchors.json`, `md_regions`, `escape_check` untouched.
- Q4 class: S-C-4 (two texts outside owns). S-D: none found.
- Q5 tests: (a) S-D-1; S-C rows kill the gate (refuse-no-line, switch-off note, skip). (b) values trace to §5.1 / card §4. (c) S-C-3 `--test " "` row. (d) K1/K5/K6/K7 changed, not weakened (K6 text grows `test`, required by §5.1). (e) none. (f) budget: S-C tests +82 vs code +97; S-D +87 vs +199. (g) no new file.
- DUPLICATION AND CONSISTENCY: S-C-3 (`test_lines` vs `_test_line_state`). S-D: none found -- grep `_flag_values|_first_word|_WORD_RE` over `tools/*.py`: only the checker.
- CODE QUALITY: S-C-3; S-D-2.
- Q8 hygiene: tools/ (not package). Cyrillic «Строка теста в DoD» in the hint: dispatch_gate reconfigures stderr to utf-8 (`dispatch_gate.py:1957-1959`); a cp1252 run of `dispatch_new.py` printed the refusal, exit 2.
- Q9 ratchets: no in-tree ratchet row touched by either diff (stat lists). `dup-baseline.json`: the forge-check job's, not yet run for staged code -- Lead reads it at merge.
- Q10 architecture: no AR-n names these files (grep of `ai-packages/qa-factory/design/architecture.md`, `docs/ARCHITECTURE_INDEX.md`). VARIETY: forge-only tools, no project shape affected.
- Q11 judgment: S-C checks presence/form (data); S-D shape/joins only, never load-bearing or equivalence. None.
- Q12 one road: none found -- the gate applies to every builder kind over the threshold; non-builder exclusion is spec §5.1 item 2.

## Trail

Read: d-1521, d-1522; spec §5.1, §5.2, §7.5, §7.6, §2.2; card §0-§4, §7-§8, T2 (lines 86-113); both reports; staged diffs
(`git -C <wt> diff --cached`) and committed test diffs (`git -C <wt> diff origin/main...HEAD`); `dispatch_manifest.py`
`:100-240, :775-790, :925-1260`; `dispatch_new.py :55-100`; `test_dispatch_manifest.py :40-90, :1095-1265`;
`test_critic_verdict_check.py :30-180, :535-620`; `mutate_once.py :1-80, :181-238`; TESTING.md `:61-91`.
Reruns (verbatim tails):
- S-C witness: `python -B -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate.py -q` (S-C tree) -> `FAILED tools/test_dispatch_gate.py::test_main_folds_the_coordinator_read_warn_into_additional_context[main-thread]` / `1 failed, 812 passed in 19.31s` (matches the report's 812).
- `python -B -m pytest tools/test_dispatch_gate_md.py -q` (S-C tree; not run by the builder) -> `55 passed in 0.37s`.
- Known red on S-D tree: `pytest tools/test_dispatch_gate.py::test_main_folds_...` -> `1 failed, 1 passed in 0.75s`.
- S-D witness: `python -B -m pytest tools/test_critic_verdict_check.py -q` (S-D tree) -> `73 passed in 2.08s`.
- `registry_preflight.py check lint` on both trees -> `registry preflight: lint ok (0.1 s)` each.
- Parser probe (S-C-1), dispatch probe (S-C-2), S-D PASS probe: 9 PASS-list/extra cases -> `[]`; `--test=` -> `mutant 0: run names no --test`; backslash control -> `green control missing ...`.
- `git -C <repo> diff --stat e3ed349b origin/main -- <owned paths>` -> empty; `origin/main` = 29add319.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "S-C-1: dispatch_manifest.py:976-1000 _test_line_parse refuses a backticked key (`test:` x | expected from: y), on the spec 5.1 PASS list; accept it, add a TEST_ROWS pass row",
    "S-C-2: dispatch_manifest.py:1070-1077 _dod_commands reads a backticked test: line in the DoD extent as a run (DOD-RUN REFUSED, canon file / 4 test files); skip lines where _test_line_parse is not None, add a row",
    "S-C-3: test_lines (:1003) has no caller and duplicates _test_line_state's loop (:1015); designer_threshold computed twice (:962, :1191); add a --test blank-item row in test_dispatch_new.py CASES",
    "S-C-4 (Lead, outside owns): docs/TESTING.md:88 says code does not check the test line, CLAUDE.md:82 R11-f omits test: from the refused header list; fix in the S-C commit or open a node",
    "S-D-1: test_critic_verdict_check.py MUTANT_ROWS 'restore-mismatch no door' lacks the target too, so the show HEAD: conjunct (critic_verdict_check.py:214) is unkilled; give the entry the target",
    "S-D-2: critic_verdict_check.py:102-233 _mutant_errors is ~131 lines, nesting 4; split the per-item body into a helper"
  ],
  "class_completeness": "S-C: item-4 iteration sites all on ALL_ITEMS; READERS NOTE intact; DoD-run seam broken (S-C-2); two texts outside owns go stale at merge (S-C-4). S-D: one reader check_text, parity/md_regions/escape_check untouched; no sibling found. No conflict with origin/main 29add319 in owned files.",
  "trail": {
    "read": [
      "d-1521.txt", "d-1522.txt",
      "docs/tasks/specs/20261117-forge-test-rules-spec.md 5.1 5.2 7.5 7.6 2.2",
      "docs/tasks/specs/20261118-test-rules-sb-sd-decoupled-card.md 0-4 7-8",
      "S-C tools/dispatch_manifest.py staged :100-240 :775-790 :925-1260", "S-C tools/dispatch_new.py staged :55-100",
      "S-C tools/test_dispatch_manifest.py diff", "S-C tools/test_dispatch_new.py diff",
      "S-D tools/critic_verdict_check.py staged :60-345", "S-D tools/critic_verdict.schema.json diff",
      "S-D tools/test_critic_verdict_check.py :30-180 :535-620",
      "ai-packages/qa-factory/scripts/tests/mutate_once.py :1-80 :181-238", "docs/TESTING.md :61-91 (origin/main)", "CLAUDE.md :82 (origin/main)"
    ],
    "reruns": [
      {"command": "python -B -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate.py -q (S-C tree)", "result": "1 failed, 812 passed in 19.31s; the failure is the known red coordinator_read_warn row"},
      {"command": "python -B -m pytest tools/test_dispatch_gate_md.py -q (S-C tree)", "result": "55 passed in 0.37s"},
      {"command": "python -B -m pytest tools/test_dispatch_gate.py::test_main_folds_the_coordinator_read_warn_into_additional_context -q (S-D tree, no S-C code)", "result": "1 failed, 1 passed in 0.75s"},
      {"command": "python -B -m pytest tools/test_critic_verdict_check.py -q (S-D tree)", "result": "73 passed in 2.08s"},
      {"command": "python -B tools/registry_preflight.py check lint --paths <owned code> (both trees)", "result": "registry preflight: lint ok (0.1 s) each"},
      {"command": "python -B probe_sc.py / probe_sc2.py (parser and check() probes, S-C tree)", "result": "backticked key -> None / Missing: test (no line); backticked test line in DoD -> DOD-RUN REFUSED"},
      {"command": "python -B probe_sd.py (validate_verdict on card PASS cases, S-D tree)", "result": "9 PASS cases -> []; --test= -> run names no --test; backslash control -> green control missing"}
    ]
  },
  "mutants": [],
  "mutants_none": "no probe: the runner rule (critic.md rule 21, S-B) is not landed; killing power judged by reading (S-D-1)"
}
```
