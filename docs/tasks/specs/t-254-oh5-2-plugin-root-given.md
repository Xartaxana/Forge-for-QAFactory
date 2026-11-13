# t-254 — OH5-2 (onboarding-hooks/5, П2): the package root is GIVEN, never a literal `${CLAUDE_PLUGIN_ROOT}` in text a role reads

Draft by designer (t-254) for the Lead. Status: DRAFT, forks open (§6). Findings: B-142, B-166.
Node row: `plans/piles/onboarding-hooks/batch-5-nerazlozhennye-nakhodki.md` OH5-2 (read from the LOCAL checkout, see §8).

## 1. Intent, rules and invariants touched

Intent (Lead brief): a path a role needs is GIVEN to it (FR-15, FR-37, AR-8). No literal `${CLAUDE_PLUGIN_ROOT}` in
any text a role reads. Guard refusal texts substitute the real package root when they are built (the guard knows where it
lives); role bodies (`agents/*.md`) take the path from the brief; `experiments/measurers/run_headless.py` gives its
child what the host would give.

Why it matters (finding evidence): experiment t-024 (B-142): a subagent sees the literal unexpanded, and its Bash has
`CLAUDE_PLUGIN_ROOT` empty unless a parent exported it (R3b); with a parent value it inherits THAT value (R6b), which can be
another copy of the plugin. Only the driver exports it (B-014, `driver_core.py:492-501`).

### AR-n touched, with the change check each one demands (written into the DoD of the parts)

| AR | How this node touches it | Change check (in DoD) |
|---|---|---|
| AR-8 a role is handed its paths and commands | the door command in a refusal and the script a charter names reach the role as an absolute path from the brief card / the guard's own copy | the 4 charters name scripts that are on the role's card (join row, Part B); every guard door names an existing absolute path (Part A rows) |
| AR-13 a fact with a reader is read through it | "the package this process runs" has a reader: `runtime_paths.package_root()` (`runtime_paths.py:229`); the guard door goes through it, never through `os.environ` or a hand-made `Path(__file__)` | grep the guard for `CLAUDE_PLUGIN_ROOT` (case-insensitive, positive control on `hooks/hooks.json`): 0 hits after Part A |
| AR-15 one survivor, wired everywhere | new survivor `runtime_paths.script_command(name, root=None)` spells `python "<root>/scripts/<name>"` once; the guard's 11 sites and `brief_pack.SCRIPTS` call it | list every site (§2 census); a site that cannot call it is named on the new axis (F7). AR-15 says "a new survivor gets an axis in the same commit": the axis text is §7, the Lead writes it (SIBLING_MAP is the Lead's) |
| AR-5 host read through one adapter, no host naming | the root is taken from the running file, not from a host variable; Claude Code and Codex get the same text | no new reader of a host env var; `hooks/hooks.json` and `hooks/codex.json` untouched |
| AR-9 every refusal names a door its receiver can use | the doors of 8 refusal builders change text (not meaning) | `test_refusal_registry.py` green (A24); no new refusal, no new A24 row; `refusal_registry.py --check` green |
| AR-29 code judges data | one NEW check: a refusal_registry finding "a refusal source carries an unexpanded host root variable" | class `shape` (presence of a token in string constants), owner `data`; see census line below |
| AR-20 shrink-only ratchets | no ratchet raised; `role-load` bytes only shrink (Part B removes text) | name any raised count in the report (expected: none) |

### Checks this node adds or alters — owner and census class (AR-29, P27)

| Check | Where | Owner it serves | Census class | Census row |
|---|---|---|---|---|
| refusal source carries `claude_plugin_root` (any case, any spelling) in a string constant → finding | `refusal_registry.findings()` (A24, run by `test_refusal_registry.py` and by `audit_factory` at qa-doctor; A24 is factory-owned, `audit_factory.py:255`) | data (code) | shape | `refusal_registry.py` has no census rows today (grep of `judgment-census.json`: no `"refusal_registry.py"` row; positive control: `"runtime_paths.py"` rows at :710-712 found). If `test_judgment_census.py` names the new function as a check unit, the builder adds ONE row `class: shape, owner: data, roles: ["conductor"]` — no count of word-list/meaning-proxy/meaning/safety moves |
| join: every script a Bash role's charter names with the marker `(on your card)` is on that role's card; no role-read text carries the variable | `scripts/tests/test_ahead_cards.py` (keep, layer data_join) — a test row, not a package check unit | data | — (tests are not census units) | none |
| guard door texts | 8 builder functions in `guard_pre_tool.py` | unchanged: `big_read_check` shape/data, `handoff_write_check` safety/intent, `handoff_values_check` shape/data, `plan_write_check` safety/intent (`judgment-census.json:362-374`) | unchanged | unchanged — only the door wording changes, not what is refused |

FR walk the builder writes (PROJECT.md acceptance rule 1): A (FR-1, FR-2, FR-57 — doors), C (FR-15), D (FR-59 — the unknown
script), G (FR-30 English, FR-32, FR-54); B — "text to a person not changed" (guard texts go to roles and the conductor),
E and F — not applicable.

## 2. Census of the literal (acceptance key 1)

Command: Grep tool, pattern `CLAUDE_PLUGIN_ROOT`, case-insensitive (`-i`), path `ai-packages/qa-factory/`, count mode.
A case-insensitive substring match covers `${CLAUDE_PLUGIN_ROOT}`, `$CLAUDE_PLUGIN_ROOT`, `%CLAUDE_PLUGIN_ROOT%` and
`$env:CLAUDE_PLUGIN_ROOT` at once. **Positive control of the same shape**: the same call finds `hooks/hooks.json: 19` and
`hooks/codex.json: 28` (known host-config carriers). **Result: 417 occurrences in 84 files** (local checkout, 13.11.2026).
A second call, pattern `\$\{CLAUDE_` (any `${CLAUDE_*}` variable, tests excluded), found 326 in 57 files; it shows the sibling
`${CLAUDE_SKILL_DIR}` lives in skills and in the common-rules legend (see F1).

| Class | Carriers (hits) | Total | Verdict in this node |
|---|---|---|---|
| **host-config** (the host expands it, legitimately) | `hooks/hooks.json` 19, `hooks/codex.json` 28 | 47 | untouched |
| **role-read: subagent charters** | `agents/qa-runner.md:61` 1, `agents/qa-failure-analyst.md:76,78` 2, `agents/qa-doc-scribe.md:63` 1, `agents/qa-retro-analyst.md:60` 1 (4 files; B-142 counted 13 in 7, the node row 5 — runner line is now :61, not :60) | 5 | **Part B** |
| **role-read: injected slices** (generated from `references/common-rules.md:112`, `<!-- roles: ... -->` section; `contract_slices.py --write`) | `references/slices/<10 roles>/common-rules.md` 1 each | 10 | **Part B** (edit the source line, regenerate) |
| **role-read: guard refusal texts** | `scripts/guard_pre_tool.py` :771 (`_config_door`), :823 (`_section_door`), :875 (`big_read_check`), :1086, :1107 (`handoff_write_check`), :1231 (rewrite check, PT-*-rewrite via registry), :1273, :1275, :1286, :1299 (`plan_write_check`), :1616 (`_window_refusal`) | 11 | **Part A** |
| role-read: other code-emitted texts (driver briefs, refusals to roles) | `driver_dispatch.py` :3868, :3910, :3951; `driver_stage_s7.py` :700, :1040; `execution_request.py:2741` (MineRefusal door); `stage_done.py` :209, :651 | 8 | residual node OH5-2d (F1) |
| role-read: data/templates a role is handed | `references/templates/requirements-register.md` :113, :180 (tester's `plugin:` door, `brief_pack.py:94`); `handoffs/s0-setup-to-scout.yaml:61` (scout's `tools.ticket_adapter`); `references/stand-answers.json` :113, :116 | 5 | residual node OH5-2d (F1) |
| conductor-read (skills, phases, references the conductor reads; the conductor has its own resolution rule `references/common-rules.md:131-140` "Resolving the plugin root", roles: none) | `skills/*/SKILL.md` 18; `skills/qa-story/phases/s0..s9.md` 177; `skills/qa-onboarding/phases/*` 31; `skills/qa-doctor/phases/*` 6; `references/judge.md` 6; `references/handoffs.md` 3; `references/common-rules.md:134` 1 (the rule itself); `config_contract.py` :1220, :1222; `source_exclusions.py:516` (`_script`, spells s1.md's form); `story_step.py` :1034, :1101 | 248 | residual node OH5-2e (F1) — measure first |
| person/developer docs | `README.md` 1, `CHANGELOG.md` 2, `design/codex-compatibility-audit.md:70` 1 | 4 | untouched (not role-read) |
| code (env export, expansion for a smoke, detectors, comments, a deliberate portable spelling) | `driver_core.py` :492, :495 (comments), :501 (export); `install_smoke.py` :196 (comment), :239 (expands the hook line); `session_env.py:10` (docstring); `brief_pack.py` :69, :209, :277 (comments); `regression_scope.py` :188-189 (detector: a regression `Command:` naming the plugin); `delivery_verdict.py` :275, :293 (deliberate: rewrites a machine path INTO the portable `${CLAUDE_PLUGIN_ROOT}/scripts/` form for a regression command a person runs on another machine, P24); `references/human-text.json:62` (detector pattern `plugin_path`) | 15 | untouched |
| eval data | `skills/qa-doctor/evals/evals.json` 1 | 1 | untouched (follows OH5-2e) |
| tests (pins, fixtures, env set-up) | 20 test files + 1 fixture (`fixtures/stories/local-1-0108/.../s3-remarks-*.md`) | 63 | only the pins Part B breaks are rewritten (keep files); quarantined pins: F6 |

Sum: 47+5+10+11+8+5+248+4+15+1+63 = 417.

## 3. The mechanism (acceptance key 2)

### 3.1 Guard refusal texts — Part A

- **Survivor** (new): `runtime_paths.script_command(name: str, root=None) -> str` and `runtime_paths.script_path(name, root=None) -> Path | None`.
  - `root` defaults to `package_root()` (`runtime_paths.py:229`, "the package this process runs: never a stored value"). The
    guard's `hooklib.PLUGIN_ROOT` and `package_root()` are the same value (`Path(__file__).resolve().parents[1]` of a file in
    `scripts/`); the guard calls the survivor, so there is one spelling (AR-13, AR-15).
  - `script_path` returns `root/"scripts"/name` when that file exists, else `None`.
  - `script_command` returns `python "<root posix>/scripts/<name>"` — `Path.as_posix()`, the SAME form `brief_pack.SCRIPTS`
    gives the card (`brief_pack.py:72`, `:4260` `Every command is \`python "{SCRIPTS}/<script>"\``), so a role sees one
    spelling in its card and in a refusal (P31, one road).
  - Quoting (edge E3): double quotes; when the posix root holds `$`, a backtick or `"` and no `'`, single quotes; when it
    holds both kinds, NO command form: the text is `<name> in <root posix>/scripts/ (quote this path for your shell: it
    holds characters a shell expands)`.
  - Script missing (edge E4, FR-59): the text is `` `<name>` (missing from the plugin copy at <root posix>; the conductor
    runs qa-doctor to repair the installation) `` — never a path that does not exist (F4).
  - Never reads `os.environ` (edge E5).
- **Sites**: every one of the 11 guard sites builds its command through `runtime_paths.script_command(...)` (lazy
  `import runtime_paths as RP`, as the guard already does at :554 and :726). `_config_door` keeps its own
  `is_file()` gate (it has another door, `Grep -n`; TEMPORAL rule in its docstring :760-761) — it does not print the
  missing form.
- **Error direction** of `package_root()` in its new, more consequential role (from "where am I running" to "the path a
  role is told to run"): it may only name the copy whose guard is refusing — the generation that enforces the rule (B-014).
  It must never name: a parent session's root (env, R6b), a stored root from a story record, a path that does not exist.
  Adversarial inputs that must stay on the safe side (table rows in Part A): a root with spaces; a Windows root with
  backslashes; a root holding `$` / backtick / `"`; a root holding `'` and `$`; a non-ASCII root (`C:/Users/Анна/...`); a
  UNC root (`\\srv\share\qa-factory` → `//srv/share/qa-factory`, as the card spells it); a script name not in `scripts/`.
- **`brief_pack.SCRIPTS`** becomes `(RP.package_root() / "scripts").as_posix()` — same value as `HERE.as_posix()` (F8).
- **Detector** (F2): `refusal_registry.findings()` gains one finding: for each file of `SCANNED` (`stage_guard.py`,
  `inject_context.py`, `guard_pre_tool.py`, `refusal_registry.py:56`), any string constant (AST `Constant` str, the
  literal parts of a `JoinedStr`) whose lowercase contains `claude_plugin_root` → `"<file>:<line>: a refusal source names
  the unexpanded host root variable; build the path with runtime_paths.script_command"`. Error direction: may err toward a
  false finding (a docstring that mentions the name) — the safe side; must not miss any spelling of a string literal.
  Accepted miss, named: a token split across concatenation (`"CLAUDE_PLUGIN_" + "ROOT"`); comments are not constants and
  never reach a role.

### 3.2 Role charters — Part B

- No new brief field: the brief ALREADY carries the root — the card head `Every command is \`python "{SCRIPTS}/<script>"\``
  (`brief_pack.py:4260-4262`, walk card `:3675`) and the five scripts are already card lines:
  `TOOLING["qa-failure-analyst"]` `bug_snapshot.py` (:279), `bug_records.py` (:280); `TOOLING["qa-doc-scribe"]`
  `report_facts.py` (:287); `TOOLING["qa-retro-analyst"]` `retro_numbers.py` (:301); `TOOLING["qa-runner"]`
  `manual_evidence.py prepare|validate|write-block` (:263). All four roles have Bash (`agents/*.md:4`).
- Each charter line drops `${CLAUDE_PLUGIN_ROOT}/scripts/` and names the script by its file name followed by the marker
  `(on your card)`:
  - `qa-doc-scribe.md:63`: `` `report_facts.py --task <TICKET> --write` (`python`, on your card) ``
  - `qa-failure-analyst.md:76`: `` `bug_records.py open-bugs --task-root <r> --draft <file>` (on your card) ``
  - `qa-failure-analyst.md:78`: `` `bug_snapshot.py` (on your card) persists bug evidence you hold ``
  - `qa-retro-analyst.md:60`: `` `retro_numbers.py` (on your card) has computed every figure ... ``
  - `qa-runner.md:61`: `` `manual_evidence.py` (`build`, `rejudge`, `validate`; on your card) ``
- `references/common-rules.md:112` (the role-section legend): the first cell becomes `` `references/…`, `scripts/…`,
  the paths on your brief `` — `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_SKILL_DIR}` leave the ROLE section (sweep of the
  same artifact: the sibling host variable in the same cell). Line 134 (conductor section, roles: none) is NOT touched.
  Then `python -B scripts/contract_slices.py --write` regenerates the 10 slices.
- Detector: a join row in `test_ahead_cards.py` (F3).

### 3.3 run_headless — Part C

- New pure function `child_env(base: dict, plugin: str) -> dict` in `experiments/measurers/run_headless.py`: a copy of
  `base` with `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS="0"` (as today, :65), `CLAUDE_PLUGIN_ROOT=plugin` (the `--plugin-dir`
  copy), and `QA_FACTORY_RUN_MODE` REMOVED. `main()` uses `child_env(os.environ, PLUGIN)`.
- Why remove and not set (F5): `launch_card.desktop_story` (`launch_card.py:165-176`) returns False for ANY non-empty
  `QA_FACTORY_RUN_MODE`; a headless turn driven by `--resume` gate messages is the desktop road, where the host sets no
  run mode. B-166's wording "does not export QA_FACTORY_RUN_MODE" is therefore NOT followed literally (reported, §8).

## 4. Builder parts (acceptance key 3)

Parts A, B, C have disjoint owns and no order between them; they can run in parallel. Each is under ~150 diff lines.
None owns an in-flight file (hooklib.py, host_probe.py, factory_dashboard.py, config_view.py, check_coverage.py,
native_context.py, inject_context.py, stage_guard.py, controller.py). `hooklib.PLUGIN_ROOT`, `stage_guard.py` and
`inject_context.py` are only READ (import / scan).
Later nodes waiting on Part A (`guard_pre_tool.py`): OH5-4, OH5-13 (batch row "Зависит от: OH5-2").

---

### Part A — the guard's doors through one survivor (~120 lines)

given: this spec §1, §2, §3.1, §5; C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md (whole); C:/QAFactory/forge-repo/plans/builder-rules.md; C:/QAFactory/forge-repo/docs/TESTING.md; C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/guard_pre_tool.py (:757-827, :872-879, :1070-1111, :1220-1310, :1609-1625); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/runtime_paths.py (:223-231); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/refusal_registry.py (:56-60, :812-940); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py (:62-72); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_refusal_registry.py
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/runtime_paths.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/guard_pre_tool.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/refusal_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_refusal_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
non-goals: no change to what any refusal refuses or to its A24 key; no edit of hooklib.py, stage_guard.py, inject_context.py (in-flight; read only); no other module's literal (driver_*, stage_done, execution_request, story_step, source_exclusions, config_contract: node OH5-2d); no skill/phase/reference text (OH5-2e); no new test file; no edit of a quarantined test file; no edit of docs/SIBLING_MAP.md (the Lead writes axis 37 from §7); judgment-census.json only if test_judgment_census.py demands a row for the new finding function (then one row, class shape, owner data)
handoff: builder report (`.claude/agents/builder.md` rule 7): the diff, the FR walk A-G, the AR lines of §1, the verbatim witness output, the list of guard sites with the function each now calls, and "needed beyond the manifest"
edges: E1-E15 of §5 (spaces, backslashes, `$`/backtick/quote roots, missing script, root never from env, Codex = Claude text, non-ASCII, UNC, symlink, hot path, temporal commit order, in-flight scanned files, docstring false positive, concatenation miss, all spellings)
DoD: (1) `runtime_paths.script_command` / `script_path` exist with the behaviour of §3.1, and one table in `test_refusal_registry.py` (rows named by edge id: E1 spaces, E2 backslash root, E3a `$` root, E3b `'`+`$` root, E4 missing script, E7 non-ASCII, E8 UNC) passes `root=` explicitly and checks the exact returned text; (2) the 11 guard sites call the survivor — a Grep, case-insensitive, of `CLAUDE_PLUGIN_ROOT` over `scripts/guard_pre_tool.py` gives 0 hits, with the same Grep finding `hooks/hooks.json` as the positive control, both outputs pasted; (3) a built-text row: at least `_window_refusal` (stub WF with `cases_of`) and the `plan_write_check` refusal of a JSON plan with rows (temp project, event with a Bash role) are built through the real guard functions, every `python "<p>"` / `python '<p>'` path in them is extracted, and each `<p>` exists and starts with `runtime_paths.package_root().as_posix()`; (4) `refusal_registry.findings()` reports a fake `stage_guard.py` (the existing `_fake_package` helper) holding `"${CLAUDE_PLUGIN_ROOT}/scripts/x.py"` (one variant row in `part_scanner`) and the live package has no finding (the existing `part_live_package` check stays green); (5) `brief_pack.SCRIPTS` equals `(runtime_paths.package_root() / "scripts").as_posix()`; verification run: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/runtime_paths.py scripts/guard_pre_tool.py scripts/refusal_registry.py scripts/brief_pack.py scripts/tests/test_refusal_registry.py` and every test file it prints (quarantined files excluded), plus `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/refusal_registry.py --check` and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_judgment_census.py`; pasted verbatim
siblings: `story_step.py:276` and `handoff_check.py:2796` spell `python "{HERE.as_posix()}/handoff_check.py"` by hand — queued to OH5-2d (wire to the survivor); `source_exclusions._script` (:514) — OH5-2e; report any other hand-made absolute script spelling you notice, do not fix it
designer: C:/QAFactory/forge-repo/docs/tasks/specs/t-254-oh5-2-plugin-root-given.md

---

### Part B — role charters and slices name the card, not the variable (~60 lines)

given: this spec §1, §2, §3.2, §5; C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md (whole); C:/QAFactory/forge-repo/plans/builder-rules.md; C:/QAFactory/forge-repo/docs/TESTING.md; the four charters below; C:/QAFactory/forge-repo/ai-packages/qa-factory/references/common-rules.md (:103-140); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py (TOOLING :256-304, card :4258-4267); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_ahead_cards.py; C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py (:216-228); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack_roles.py (:270-303, K9 — READ ONLY, quarantined: the old form of the join)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-runner.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-failure-analyst.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-doc-scribe.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-retro-analyst.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/common-rules.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/ (only the `common-rules.md` files `contract_slices.py --write` regenerates)
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_ahead_cards.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py
non-goals: no brief_pack.py edit (the cards already carry the five scripts; Part A owns brief_pack.py); no new brief field; no skill/phase text and no common-rules.md conductor section (:131-140, OH5-2e); no edit of quarantined test files (test_brief_pack_roles.py, test_package_generation.py — F6); no edit of test-layers.json; no other charter wording
handoff: builder report (`.claude/agents/builder.md` rule 7): the diff, the FR walk A-G, the AR lines of §1, the verbatim witness, and the list of quarantined checks that will now go red (expected: test_brief_pack_roles.py K9 :300, test_package_generation.py P4 :489, P5 :492, :494)
edges: E18-E22 of §5 (script not on card, role without Bash, join vacuity, slice regeneration diff, quarantined pins)
DoD: (1) the five charter lines read as §3.2 lists them; (2) `references/common-rules.md:112` reads as §3.2 and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/contract_slices.py --write` regenerated the slices: the slice diff is that one legend line in each of the 10 files, nothing else; (3) one join row in `test_ahead_cards.py`: for every role whose `tools:` line holds Bash (through the existing reader `role_rules.WITH_BASH` / `host_adapter.role_has_bash`, never a regex on the role file), every `` `<name>.py ...` `` followed by `(on your card)` (or with `on your card` inside the parenthesis that follows it) in its charter is on that role's card (`brief_pack.TOOLING[role]` + `TOOLING_MANUAL[role]`); the join finds exactly the five names of §3.2 (vacuity guard); and no file in `agents/` or `references/slices/` contains `claude_plugin_root` in any case; (4) the key `'python "${CLAUDE_PLUGIN_ROOT}/scripts/manual_evidence.py" validate'` of `test_charters_s5_s9.py:223` is rewritten to the new runner phrase (TESTING.md «Когда тест покраснел» 1: an intended change rewrites the pin in the same node); verification run: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for agents/qa-runner.md agents/qa-failure-analyst.md agents/qa-doc-scribe.md agents/qa-retro-analyst.md references/common-rules.md scripts/tests/test_ahead_cards.py scripts/tests/test_charters_s5_s9.py` and every non-quarantined file it prints, plus `test_ahead_cards.py`, `python -m pytest ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py -q` and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/contract_slices.py --check`; pasted verbatim
siblings: other role-read literals (templates/requirements-register.md, handoffs/s0-setup-to-scout.yaml, stand-answers.json, driver brief lines) — OH5-2d; conductor texts — OH5-2e; report any charter that names a script with no card line
designer: C:/QAFactory/forge-repo/docs/tasks/specs/t-254-oh5-2-plugin-root-given.md

---

### Part C — run_headless gives its child what the host would give (~25 lines)

given: this spec §3.3, §5 E16-E17; C:/QAFactory/forge-repo/experiments/measurers/run_headless.py (whole, 89 lines); C:/QAFactory/forge-repo/experiments/measurers/test_measurers.py (:1509-1540 `rt_prepare_copy_and_run_headless`, :1605 `main`); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/launch_card.py (:165-176, read only); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_core.py (:490-501, read only — the driver's export, the model)
owns:
C:/QAFactory/forge-repo/experiments/measurers/run_headless.py
C:/QAFactory/forge-repo/experiments/measurers/test_measurers.py
non-goals: no package file; no change to the claude command line, the tool list or the model; no Codex runner (none exists in experiments/measurers — §8); no QA_FACTORY_RUN_MODE value of any kind
handoff: builder report: the diff and the verbatim witness
edges: E16 parent env holds QA_FACTORY_RUN_MODE=driver and a stale CLAUDE_PLUGIN_ROOT; E17 PLUGIN path with spaces
DoD: (1) `run_headless.child_env(base, plugin)` exists as §3.3 and `main()` passes its result to `subprocess.run`; (2) one table in `test_measurers.py` (next to `rt_prepare_copy_and_run_headless`) with rows E16 (base `{"QA_FACTORY_RUN_MODE": "driver", "CLAUDE_PLUGIN_ROOT": "/other/copy", "X": "1"}` → no `QA_FACTORY_RUN_MODE`, root = plugin, `X` kept, ceiling `"0"`) and E17 (plugin `C:/my plugins/qa-factory` → the value verbatim, no quotes), and `base` itself unchanged; verification run: `python -B C:/QAFactory/forge-repo/experiments/measurers/test_measurers.py` (if the file needs its own folder as cwd, the hygiene door `( cd C:/QAFactory/forge-repo/experiments/measurers && python -B test_measurers.py )`), pasted verbatim
siblings: `driver_core.py:501` exports the same root for the driver's child — same intent, different value for the run mode by design (the driver IS the driver); no other launcher of `claude -p` in experiments/measurers (Grep `claude` there: run_headless.py and paths/report tools only)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/t-254-oh5-2-plugin-root-given.md

---

### Residual nodes (named, not drafted here; F1 — the Lead decides to open them)

| Node | What | owns (expected) | Test |
|---|---|---|---|
| OH5-2d | role-read literals emitted by other code and data: `driver_dispatch.py` :3868/:3910/:3951, `driver_stage_s7.py` :700/:1040, `execution_request.py:2741`, `stage_done.py` :209/:651, `references/templates/requirements-register.md` :113/:180, `handoffs/s0-setup-to-scout.yaml:61`, `references/stand-answers.json` :113/:116; and wiring `story_step.py:276`, `handoff_check.py:2796` to `runtime_paths.script_command` | those files + their keep tests (`test_stage_cards.py`, `test_story_step_manual_block.py` pins) | extend Part B's join to "no role-read carrier holds the variable" over the carriers above; built-text rows for the driver lines |
| OH5-2e | conductor-read literals (248 hits: skills, phases, judge.md, handoffs.md, config_contract, source_exclusions, story_step doors) and `${CLAUDE_SKILL_DIR}` | after measurement only | first ONE experiment (CLAUDE.md hygiene 6a): in a desktop session, does the Claude host expand `${CLAUDE_PLUGIN_ROOT}` in skill text, and does the conductor's Bash see it? and the same on Codex. Then either keep the literal under the stated resolution rule (`common-rules.md:131-140`) or rewrite through `runtime_paths.py` entrypoints |

## 5. Edges, each with the invariant it protects (acceptance key 4)

| Id | Edge | Behaviour | Invariant protected |
|---|---|---|---|
| E1 | package root contains spaces (`C:/Program Files/qa factory`) | `python "<root>/scripts/x.py"`, double-quoted | the path is one shell word in bash and PowerShell; a pasted door runs the named file |
| E2 | Windows root with backslashes | `Path.as_posix()` → forward slashes | the guard spells the root exactly as the brief card does (one road, P31); never mixed separators |
| E3a | root holds `$`, a backtick or `"` (no `'`) | single quotes | a pasted door never expands into another path |
| E3b | root holds `'` and one of `$`/backtick/`"` | no command form; name + root as plain text with "quote this path for your shell" | same: no command that resolves elsewhere is ever printed |
| E4 | the named script is missing from the running copy (partial install, older copy) | `` `<name>` (missing from the plugin copy at <root>; the conductor runs qa-doctor ...) ``; `_config_door` keeps omitting its shell line (it has the Grep door) | FR-59: a fabricated path is never printed; FR-57: the refusal still has a door |
| E5 | "root unknown" | cannot occur in the guard: the root is the copy of the running file (`package_root()`); the survivor never reads `CLAUDE_PLUGIN_ROOT` or any env | a parent's or the host's stale value (t-024 R6b) never decides the path; the door names the generation that enforces the rule (B-014) |
| E6 | Codex host vs Claude host | the same text on both; the guard is reached through `hooks/codex.json` or `hooks/hooks.json`, both untouched | AR-5: no host naming; Codex's compat variable is irrelevant to role text |
| E7 | non-ASCII root (`C:/Users/Анна/...`) | kept verbatim; only separators change | no transliteration; the path exists as printed |
| E8 | UNC root `\\srv\share\qa` | `//srv/share/qa`, as the card prints it today | the door and the card agree; this node adds no new UNC behaviour |
| E9 | symlink / junction install | `resolve()` gives the real path, which exists | the printed path exists |
| E10 | hot path | the survivor is called only while building a refusal (on the way to `block`) | a call that passes pays no stat or import (the guard's ORDER rule, `guard_pre_tool.py:839-841`) |
| E11 | TEMPORAL: the survivor and the registry finding do not exist before Part A | the finding, the 11 site rewrites and the survivor land in ONE commit | `test_refusal_registry.py` part_live_package is green at every commit (the finding would fire on the 11 old sites) |
| E12 | in-flight `stage_guard.py` / `inject_context.py` are scanned by the finding | they hold 0 hits today (census §2); if a branch adds one, its own witness names `<file>:<line>` | no refusal source of any copy ships the literal; Part A does not edit those files |
| E13 | a docstring mentions the variable | flagged (string constant) | allowed error direction: a false finding, never a missed literal |
| E14 | a token split by concatenation | not flagged — accepted, named miss | evasion is a review matter (critic), not this scanner's |
| E15 | `$CLAUDE_PLUGIN_ROOT`, `%CLAUDE_PLUGIN_ROOT%`, `$env:CLAUDE_PLUGIN_ROOT`, any case | all flagged (lowercase substring `claude_plugin_root`) | no spelling of the host variable reaches a role from a refusal source |
| E16 | run_headless parent env has `QA_FACTORY_RUN_MODE=driver` and another `CLAUDE_PLUGIN_ROOT` | run mode removed; root overwritten with the `--plugin-dir` copy | a headless turn is the desktop road (`launch_card.desktop_story`); its root is the same copy as its hooks (B-014) |
| E17 | PLUGIN path with spaces | env value verbatim, no quoting | env values are not shell text |
| E18 | a charter names with `(on your card)` a script that is not on its card | the join fails naming role and script | a script a role is told to run is reachable by the absolute path its brief gives (FR-15) |
| E19 | a role without Bash | outside the join (its card is TOOLING_NO_SHELL); still in the "no variable" scan | a role is not sent to a command it cannot run (FR-2) |
| E20 | the marker spelling drifts and the join finds nothing | the join must find exactly the five names of §3.2 | the join is never vacuous |
| E21 | slice regeneration | diff limited to the legend line in 10 slices; `contract_slices.py --check` green | a slice is never hand-edited; source and slices agree |
| E22 | quarantined pins on the old literal (`test_brief_pack_roles.py` K9 :296-303; `test_package_generation.py` P4 :489-490, P5 :492-495) | not touched; listed in the handoff (F6) | the builder never edits a quarantine file (builder-rules 7b); the red is judged by quarantine-watch as a pin |

Conflicting requirement pairs named: (a) "run_headless exports what the host would give" vs B-166's "export QA_FACTORY_RUN_MODE" — resolved by E16/F5 (removal); (b) TESTING.md "rewrite a pin in the same node" vs builder-rules 7b "never edit quarantine" — resolved by F6 (keep files rewritten, quarantine listed); (c) AR-15 "axis in the same commit" vs "SIBLING_MAP is the Lead's" — F7.

## 6. Forks (acceptance key 5) — each with a recommendation the builder can run on

- **F1 — scope against one road (designer rule 6, P31).** The node covers agents, guard, run_headless (+ slices, F-sweep).
  The census finds 13 more role-read literals (OH5-2d) and 248 conductor-read ones (OH5-2e). Options: (a) this node only, with
  OH5-2d and OH5-2e opened as named nodes of this batch now (rows in batch-5 + residual table §4); (b) widen this node to
  OH5-2d (+~13 sites, +2 pinned keep tests; Part D ~100 lines; touches `stage_done.py`, `story_step.py`, driver modules — not
  in-flight, but `story_step.py`/`driver_*` are hot files of other piles); (c) everything incl. conductor text (~250 edits,
  unmeasured host behaviour). **Recommendation: (a)** — a slice is no exclusion when the rest is a named node with owns
  and a test; OH5-2e must MEASURE first (hygiene 6a): the conductor has a documented resolution road and nobody has measured
  whether the Claude host expands the variable in skill text. Cost of covering OH5-2d now: one more builder part, ~100 lines.
- **F2 — detector for refusal sources.** (a) a finding in `refusal_registry.findings()` (A24, the one scanner of refusal
  sources, AR-29 carrier) + built-text rows; (b) only built-text rows (cannot see a door nobody builds in the test); (c) a
  source grep test (a "source pin", forbidden by TESTING.md). **Recommendation: (a).**
- **F3 — charter spelling and the join's home.** (a) marker `(on your card)` and the join as a row of keep
  `test_ahead_cards.py` (data_join, "every card names its scripts"); (b) the join keyed on every backticked existing
  `scripts/*.py` name in a Bash charter (no marker; may over-match scripts a charter names for context); (c) a new audit
  check A-nn in `audit_factory.py`. **Recommendation: (a)** — K9's intent moves from a quarantined file into a keep file.
- **F4 — the door when the script is missing.** (a) name the gap and qa-doctor (§3.1); (b) omit the door line silently.
  **Recommendation: (a)** — FR-59 names what could not be established; (b) leaves some refusals (window claim) without a door.
- **F5 — run_headless run mode.** (a) remove `QA_FACTORY_RUN_MODE`, set `CLAUDE_PLUGIN_ROOT` to the `--plugin-dir` copy;
  (b) set `QA_FACTORY_RUN_MODE=desktop` (any non-empty value makes `desktop_story` False — wrong); (c) export only the root
  and inherit the run mode. **Recommendation: (a).** Cost: a headless run no longer reproduces the DESKTOP empty-root
  condition for conductor text that still holds the literal (OH5-2e); that gap is caught by OH5-2e's measurement, not by
  experiments.
- **F6 — quarantined pins go red.** `test_brief_pack_roles.py` K9 (:300 expects `["bug_records.py","bug_snapshot.py"]` found
  through the literal) and `test_package_generation.py` P4/P5 (:489-495). (a) leave them; the handoff lists them; the
  quarantine-watch judge classes them as pins of an intended change (TESTING.md «Когда тест покраснел» 1-2), and their join
  intent now lives in keep `test_ahead_cards.py`; (b) the Lead authorises the builder to edit those two quarantined files.
  **Recommendation: (a).** The Lead tells the owner the expected quarantine reds in the same turn as acceptance.
- **F7 — the new axis (AR-15).** `runtime_paths.script_command` is a new survivor; AR-15 wants its axis in the same commit.
  (a) the Lead commits axis 37 (§7) together with Part A's merge; (b) queue the axis. **Recommendation: (a).**
- **F8 — `brief_pack.SCRIPTS` on the survivor.** (a) one line in Part A (proves card and door share one spelling); (b) leave
  for OH5-2d. **Recommendation: (a).**

Coordinator decision (13.11 03:05, по рекомендации, до слова владельца): F1 (a), F2 (a), F3 (a), F4 (a), F5 (a), F6 (a),
F8 (a). F7: the axis is a mechanism, so the full Lead commits it (the coordinator is in a degraded window); queued to Lead.
The number 37 is also proposed by spec t-231 part C, so the Lead assigns both numbers. Part A merges with the axis line
queued, and the builder's handoff names it.

Small technical choices closed by the designer (no design weight): the survivor lives in `runtime_paths.py` (FR-37's check
names it; `package_root()` is there); helper names `script_command` / `script_path`; lazy import in the guard as at :554;
quoting rule E3; `test-layers.json` not edited (DoD names the test files explicitly); the legend line also drops
`${CLAUDE_SKILL_DIR}` (same cell, same class); the marker text `(on your card)`.

## 7. Draft axis for docs/SIBLING_MAP.md (the Lead writes it; F7)

`## Axis 37 — Where the package root is resolved at runtime: one survivor runtime_paths.script_command <-> the role-read texts that name a script <-> the brief card <-> the conductor's rule (OH5-2, t-254; B-142, B-166)`

| Component | Path |
|---|---|
| The survivor | `scripts/runtime_paths.py` `package_root()`, `script_path()`, `script_command()` — the copy that runs, posix spelling, quoting rule; never an env var |
| Callers | `guard_pre_tool.py` (11 door sites), `brief_pack.SCRIPTS` (the card head) |
| Known roads off it (queued) | OH5-2d: `driver_dispatch.py`, `driver_stage_s7.py`, `execution_request.py`, `stage_done.py`, `story_step.py:276`, `handoff_check.py:2796`, `references/templates/requirements-register.md`, `handoffs/s0-setup-to-scout.yaml`, `references/stand-answers.json`; OH5-2e: conductor texts (skills, phases, `judge.md`, `handoffs.md`, `source_exclusions._script`, `config_contract.py`) under `common-rules.md` "Resolving the plugin root" |
| Legitimate literals | `hooks/hooks.json`, `hooks/codex.json` (host expands); `delivery_verdict.py` portable regression spelling (P24); detectors `regression_scope.py`, `human-text.json` `plugin_path`; `driver_core.py` export; `install_smoke.py` expansion |
| The symmetry | a text a role reads names a plugin script through the survivor or the brief card; a new door with a script calls `script_command` |
| The detector | `refusal_registry.findings()` (refusal sources), `test_ahead_cards.py` join row (charters, slices), the case-insensitive grep `claude_plugin_root` over `agents/` and `references/slices/` finds nothing (positive control: `hooks/hooks.json`) |

## 8. Reported, not widened (rule 3)

- **Freshness:** I have no shell tool in this dispatch, so the `git show refs/remotes/origin/main:...` reads of the node row,
  B-142 and B-166 were NOT run; I read the LOCAL files. The Lead said the local checkout is behind — the Lead checks the OH5-2
  row and both findings against origin/main before accepting (the census is also local).
- Node row line numbers drifted: `qa-runner:60` is now :61; B-142's "13 in 7 files" is now 5 in 4 files.
- B-166 asks run_headless to "export QA_FACTORY_RUN_MODE": doing so with any value breaks desktop detection
  (`launch_card.py:169`). §3.3 removes it instead (F5).
- The node row lists `scripts/brief_pack.py` "if the brief carries the root": it already does (`brief_pack.py:72`, `:4260`);
  no new brief field is needed.
- The role-read literals the node row does not name (slices: included in Part B; OH5-2d's 13 sites) — F1.
- No Codex headless measurer exists: Grep `codex` (case-insensitive) over `experiments/measurers/` found nothing; positive
  control, same call with `CLAUDE`, found 11 files including `run_headless.py`.

## 9. Reading trail

- `plans/piles/onboarding-hooks/batch-5-nerazlozhennye-nakhodki.md` (whole, local); `findings/B-142-...md`, `findings/B-166-...md` (whole, local).
- Grep `CLAUDE_PLUGIN_ROOT` -i over `ai-packages/qa-factory/` (count; content over `agents/`, `scripts/*.py`, `skills/*/SKILL.md`, `references/`, `design/`, `handoffs/s0-setup-to-scout.yaml`); Grep `\$\{CLAUDE_` over the package minus tests.
- `scripts/guard_pre_tool.py` :1-60, :755-884, :1070-1119, :1220-1310, :1600-1625; Grep of `PLUGIN_ROOT`, `runtime_paths`, `_has_bash`, `role_ways`.
- `scripts/hooklib.py:30` (via Grep `^PLUGIN_ROOT =`); `scripts/runtime_paths.py` :1-46, :220-234, def list.
- `scripts/brief_pack.py` :55-94, :195-294, :1110-1129, :3655-3684, :4245-4274, Grep `SCRIPTS`, `retro_numbers`.
- `scripts/source_exclusions.py:505-524`; `scripts/execution_request.py:2730-2745`; `scripts/driver_stage_s7.py:692-703`; `scripts/driver_dispatch.py:3860-3874`; `scripts/stage_done.py:203-211`; `scripts/launch_card.py:155-179`; Grep `QA_FACTORY_RUN_MODE`, `RUN_MODE_ENV`.
- `scripts/refusal_registry.py` def list; `scripts/audit_factory.py` def list; `scripts/contract_slices.py` Grep `slices`.
- `references/common-rules.md:100-144`; `references/human-text.json:40-80`.
- Tests: `test_brief_pack_roles.py:260-319`; `test_package_generation.py:425-498`; `test_charters_s5_s9.py:210-235`; `test_guard_command_text.py:1-70`; `test_ahead_cards.py:1-60`; `test_refusal_registry.py:1-90`; `scenario_walk.py:887-931`; `test-layers.json` :1-84, :495-524, :2080-2190, :4250-4265, :9180-9195 and Grep of keep/quarantine rows; `fixtures/judgment-census.json:1-40` and Grep of rows.
- `experiments/measurers/run_headless.py` (whole); `test_measurers.py` def list; Grep `codex` / `CLAUDE` over `experiments/measurers/`.
- `design/factory-rules.md` FR-15 :205, FR-59 :289, FR-37 :357; `design/architecture.md` AR-5..AR-9 :76-111, AR-29/AR-13..AR-16 :134-188.
- `docs/SIBLING_MAP.md` axis headings, axis 13 :311-328, axis 34 :582-593, upkeep :620-636; `docs/TESTING.md:75-144`; `plans/builder-rules.md` 7/7a/7b.
