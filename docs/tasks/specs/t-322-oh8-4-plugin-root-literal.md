# t-322 — OH8-4 (onboarding-hooks/8, П2): role-read texts get the package root through `runtime_paths.script_command`, never a literal `${CLAUDE_PLUGIN_ROOT}`

Draft by designer (t-322) for the Lead. Status: DRAFT rev 1. Forks: §7 (returned, not decided).
Node row: `plans/piles/onboarding-hooks/batch-8-ostatki-t-282-t-254-t-287.md:35` (OH8-4). Finding:
`plans/piles/onboarding-hooks/findings/20261113-oh5-2d-bukvalnyj-claude-plugin-root-v-tekstah-dlya-roli-iz-drugogo-koda.md`.
Parent spec: `docs/tasks/specs/t-254-oh5-2-plugin-root-given.md` (§2 census, §4 residual OH5-2d, §6 F1 (a)).
All facts below were read in `.claude/worktrees/read-main` (origin/main `303e89e`), never in the root checkout.

## 1. Intent, the role/conductor line, rules and invariants touched

Intent (Lead brief): every text a ROLE reads names a package script by the absolute path of the copy that serves it, spelled
by the one survivor `runtime_paths.script_command(name, root=None, *, must_exist=True)` (`runtime_paths.py:248-266`, landed
by OH5-2 Part A), or by its card (a data file read raw); no role-read carrier holds `${CLAUDE_PLUGIN_ROOT}` in any spelling.

### 1.1 The line: "a role reads it" against "the conductor reads it" (OH8-5)

A carrier is **role-read** (this node) when ANY of its readers is a role: a line of a role's brief or prompt, a refusal or
note printed by a script a role runs, a file a role is handed or reads by a `plugin:` door, a handoff form addressed to a
role, a table text a script prints to whoever ran it when a role's card names that script. A carrier is **conductor-read**
(OH8-5, after its host experiment) when NO role reads it: `skills/**` and their phases, `references/common-rules.md`
conductor section (:131-140), `references/judge.md`, `references/handoffs.md`, `config_contract.py:1220/1222`,
`source_exclusions._script` (:516), `story_step.py` :1034, :1101 (door lines printed to the orchestrator),
`skills/qa-doctor/evals/evals.json`. Mixed readers (role AND conductor or person) are role-read: an absolute path costs the
conductor nothing, a literal costs the role a failed call.

Why the literal only matters as a LITERAL for OH8-5: a hand-made absolute spelling (`HERE.as_posix()`, `self.scripts`)
already names a real path, so wiring it to the survivor needs no host experiment, whoever reads it (see F5).

### 1.2 AR-n touched, with the change check each demands (written into the DoD of the parts)

| AR | How this node touches it | Change check (DoD) |
|---|---|---|
| AR-8 a role is handed its paths and commands | 8 code sites + swept same-file sites + 3 data carriers stop naming an unexpanded variable or a hand spelling; the path reaches the role from the survivor or from its card | built-text rows (Part 1) and the data join (Part 2): every command a role-read text names resolves to an existing file under the root the role's card names |
| AR-13 a fact with a reader is read only through it | "the spelling of a package script command" has one writer, `script_command`; "the stand-answers table" has one reader, `env_probe.stand_answers` (`env_probe.py:233`) — the token is resolved THERE, never by a second parser in `stand_health` | grep the owned functions for `CLAUDE_PLUGIN_ROOT` (case-insensitive), `HERE.as_posix()`, `{self.scripts}`; positive control `hooks/hooks.json`; 0 hits; pasted in the report (not committed) |
| AR-15 one survivor, wired everywhere | sites move onto `script_command`; Part 2 adds the token expander `runtime_paths.expand_script_tokens` beside it (F4) | list every site (§3, §6); axis 37 (drafted in t-254 §7, queued to the full Lead — not in `docs/SIBLING_MAP.md` on origin: headings stop at Axis 36) moves these sites from "roads off" to "callers"; commit line `architecture: AR-15 -- sites wired to script_command; axis 37 queued to Lead` |
| AR-5 host read through one adapter, no host naming | no text relies on a host expanding a variable; no new reader of any env var | the survivor and the expander never read `os.environ` (t-254 E5 holds) |
| AR-9 every refusal names a door its receiver can use | doors of `stage_done.current_code_diff_refusal`, `execution_request._probe_door` (in the S5 `MineRefusal`), `handoff_check.refusal_text` change their path spelling, not their meaning; A24 keys are the first 90 chars of a `block(...)` first argument — every changed span is past char 90 or in a non-guard refusal | `python -B .../refusal_registry.py --check` green; no new refusal, no A24 row change |
| AR-22 every field read has a producer, every produced field a reader | `stand-answers.json` `login_recheck` and `login_remedies[].remedy` keep their reader (`stand_health._login_receipt` / `_login_remedy` through `env_probe.stand_answers`); `s0-setup-to-scout.yaml` `tools.ticket_adapter` is read by the scout only (no code reader: Grep `tools.ticket_adapter` over the package found none; positive control: the same Grep finds `ticket_adapter_proved` in the yaml) | named in the report; no field renamed |
| AR-1 closed variety in data | the script a table text names stays in the data row (`{script:stand_health.py}`), not in code | the token is generic; no script name is added to code |
| AR-20 shrink-only ratchets | no charter, slice or injected text changes: `references/templates/requirements-register.md` is NOT an inject-map entry (Grep `requirements-register` over `references/inject-map.json`: none; positive control, same call with `plugin:references/`: 71 hits), so `role_load` process rows do not move | if `role_load.py --all` shows any change, report it; no row raised |
| AR-29 code judges data | no product check is added or altered: `expand_script_tokens` is a text transform (not a check unit; it is not named `*_problems`/`*_check`); the new assertions are TEST rows (not census units) | `test_judgment_census.py` green; if it names a unit, ONE row `class: shape, owner: data` |

### 1.3 Checks this node adds or alters — owner and census class (AR-29, P27)

| Check | Where | Owner it serves | Census class |
|---|---|---|---|
| join: every script a role-read data carrier names with `(on your card)` is on the card of the role that reads that carrier; no role-read carrier (charters, slices, the three data files) holds `claude_plugin_root` | `test_ahead_cards.charter_card_join` (keep, layer `data_join`) — a test row | data (code) | — (tests are not census units) |
| built-text rows: every command a role-read text built by code names exists under the root of the copy that serves the role | `test_ahead_cards.role_text_roots` (new function in keep `test_ahead_cards.py`) — a test row | data | — |
| token rows of the survivor | `test_runtime_paths.py` (keep, layer `table`, the survivor's table) | data | — |
| guard / refusal behaviour | unchanged: what each refusal refuses and its A24 key | unchanged | unchanged |

FR walk the builder writes (PROJECT.md acceptance rule 1): A (FR-1, FR-2, FR-57 — doors), C (FR-15), D (FR-59 — gap text
for a missing script), E (FR-37 — the path in a text is the path code writes), G (FR-30, FR-32, FR-54). B — the
`execution_request` door and the `stand_health` sentence may reach a person: only the path spelling changes; see edge E22
(the `plugin_path` detector). F — not applicable.

## 2. Census of this node (re-read on origin `303e89e`)

Grep tool, pattern `claude_plugin_root`, `-i`, path `ai-packages/qa-factory/`, count: 402 in 72 files; positive control in
the same call: `hooks/hooks.json: 19`, `hooks/codex.json: 28`. Line numbers that DRIFTED since t-254: `execution_request.py`
:2741 -> **:2751**; `handoff_check.py` :2796 -> **:2836**. All others as t-254 named them.

## 3. Per carrier: current line, new behaviour, who builds the text, who reads it

Root column: `P` = `self.plugin` (the copy the driver dispatches, `driver_core.py:416`; F1); `R` = `runtime_paths.package_root()`
(the copy the process runs; the survivor's default).

### 3.1 Code-built texts (Part 1)

| # | File:line (function) | Current | New | Builder of the text | Reader | Root |
|---|---|---|---|---|---|---|
| C1 | `driver_dispatch.py:3868` (`DriverDispatch.s7_place_lines`) | `py = '`python "${CLAUDE_PLUGIN_ROOT}/scripts/'` then `{py}place_answers.py" list ...`, `{py}manual_capture.py" ...`, `{py}place_answers.py" write ...` | each command is `` `{RP.script_command("<name>.py", self.plugin)} <args>` ``; the `py` prefix variable and every hand-closed `"` go | the driver, per S7 triage dispatch | qa-failure-analyst (Bash) | P |
| C2 | `driver_dispatch.py:3910` (`s7_neighbour_lines`) | `` command = f'`python "${{CLAUDE_PLUGIN_ROOT}}/scripts/bug_neighbours.py" --task-root ...`' `` | `` f'`{RP.script_command("bug_neighbours.py", self.plugin)} --task-root qa-factory/artifacts/{self.task}/`' `` | driver | qa-failure-analyst | P |
| C3 | `driver_dispatch.py:3951` (`s7_session_line`) | `py = ...` prefix; `manual_capture.py`, `walk_session.py` commands | as C1 | driver | qa-failure-analyst | P |
| C4 | `driver_stage_s7.py:700` (`DriverStageS7.investigation_lines`) | `py = ...` prefix; `investigation.py" unresolved ...` (and every later `{py}` use in the method) | as C1 | driver | qa-failure-analyst (investigation) | P |
| C5 | `driver_stage_s7.py:1040` (`s7_rejudge_round`) | `python \"${{CLAUDE_PLUGIN_ROOT}}/scripts/manual_evidence.py\" rejudge --task-root \"{self.task_root}\" ...` | `RP.script_command("manual_evidence.py", self.plugin) + f' rejudge --task-root "{self.task_root}" ...'` (the tail unchanged) | driver, in the `extra` of an S6 rework | qa-runner (Bash) | P |
| C6 | `execution_request.py:2751` (`_probe_door`) | `python "${{CLAUDE_PLUGIN_ROOT}}/scripts/runtime_probe.py" --suggest --write --profile {_word(profile)}` | `f'{RP.script_command("runtime_probe.py")} --suggest --write --profile {_word(profile)}'` (lazy `import runtime_paths as RP` inside the function) | `execution_request` while raising the S5 `MineRefusal` | qa-automator (Bash) or the person, by the conductor | R |
| C7 | `stage_done.py:209` (`current_code_diff_refusal`) | `` `python \"${{CLAUDE_PLUGIN_ROOT}}/scripts/stage_done.py\" --task {task} --set implementation_source=diff` `` | `` f"`{RP.script_command('stage_done.py')} --task {task} --set implementation_source=diff`" `` (`RP` is imported at module level, `stage_done.py:41`) | `stage_done` at the S1 exit | qa-scout (Bash) | R |
| C8 | `stage_done.py:651` (`_s3_remark_package`) | `` `python \"${{CLAUDE_PLUGIN_ROOT}}/scripts/plan_row.py\" --task {task} --show --row <id>` `` (after "with a shell,") | `` f"`{RP.script_command('plan_row.py')} --task {task} --show --row <id>`" ``; the "with a shell," clause stays | `stage_done` at the S3 exit, written to `state/findings/s3-remarks-<sha12>.md` | qa-test-strategist (no Bash: it reads the file; the command is for a strategist given a shell) | R |
| C9 | `story_step.py:276` (`_prompt`) | `python \"{HERE.as_posix()}/handoff_check.py\" --file {form} --task {task} --fix` (hand spelling) | `f"  when it is filled: {RP.script_command('handoff_check.py')} --file {form} --task {task} --fix"` | `story_step start` | a role with Bash (`host_adapter.role_has_bash`) | R (same value as `HERE.parent`) |
| C10 | `handoff_check.py:2836` (`refusal_text`) | `python "{HERE.as_posix()}/handoff_check.py" --file {_arg(form_path)} --fix --values - <<'EOF'` (hand spelling) | `f"{RP.script_command('handoff_check.py')} --file {_arg(form_path)} --fix --values - <<'EOF'"` (lazy import inside the `if shell:` branch) | `handoff_check` and the pre-tool guard (it builds its refusal with this function) | a role with Bash | R |
| C11 (sweep, F5) | `driver_dispatch.py:697` (`run_role`) | ``"Plugin root: {self.plugin} — factory scripts are `python {self.scripts}/<name>.py`; ..."`` (hand spelling, UNQUOTED: a root with a space breaks) | ``f"Plugin root: {self.plugin} — factory scripts are `{RP.script_command('<name>.py', self.plugin, must_exist=False)}`; ..."`` (the card-head form of OH5-2 N4) | driver, every role prompt in driver mode | every role | P |
| C12 (sweep, F5) | `driver_dispatch.py:2491` (`s1_reference_window`) | `f"python \"{self.scripts}/reference_snapshot.py\" put ..."` | `RP.script_command("reference_snapshot.py", self.plugin) + f" put --task-root ..."` | driver, S1 reference window | qa-runner (reference walk) | P |
| C13 (sweep, F5) | `story_step.py:618` (`_s5_plan_init`) and `:734` (`run_mode_refusal`) | `python \"{HERE.as_posix()}/s5_plan.py\" ...`; `python \"{HERE.as_posix()}/waiver.py\" ...` | `RP.script_command("s5_plan.py")` / `RP.script_command("waiver.py")` + the same tails | `story_step start` notes / refusal | the conductor or the driver (`:727` "never for a role") — same artifact, same class, no host question | R |

Nothing else in these functions changes. No new method on any `Driver*` class (a new method needs a row in
`scripts/tests/fixtures/driver-layers.json`: every Driver method is listed there with its home, e.g. `Driver.s7_place_lines`
:683); the builder may bind a local `cmd = lambda name: RP.script_command(name, self.plugin)` inside a method.

### 3.2 Data carriers (Part 2) — how each text is filled, and its reader

| # | Carrier:line | Current | New | How it is filled | Reader |
|---|---|---|---|---|---|
| D1 | `references/templates/requirements-register.md:113` (inside an HTML comment) | `` `python "${CLAUDE_PLUGIN_ROOT}/scripts/branch_accounting.py" --units --task <TICKET>` `` | `` `branch_accounting.py --units --task <TICKET>` (on your card) `` | NOT filled: the role reads the shipped file raw (its brief names it through the `plugin:` door, `brief_pack.py:94`, resolved at `:1117-1121`); the absolute command is on its card (`brief_pack.TOOLING["qa-requirements-tester"]`, `:210`) | qa-requirements-tester (Bash, `agents/qa-requirements-tester.md:4`) |
| D2 | same file `:180` | `` `python "${CLAUDE_PLUGIN_ROOT}/scripts/branch_accounting.py" --attachments --task <TICKET>` `` | `` `branch_accounting.py --attachments --task <TICKET>` (on your card) `` | as D1 | as D1 |
| D3 | `handoffs/s0-setup-to-scout.yaml:61` (+ the comment :58-59) | `ticket_adapter: "python ${CLAUDE_PLUGIN_ROOT}/scripts/ticket_adapter.py"` | `ticket_adapter: "ticket_adapter.py (on your card)"`; comment: "The tools S0 proved before this dispatch, named by script; the scout's card carries each command with its absolute path." (F2) | the contract's value is copied verbatim into an instance by `handoff_init.fill_head` (it substitutes only `<TICKET>`, `<dispatch>` and header fields, `handoff_init.py:119-147`); no build-time change needed | qa-scout (`to_role`, :13; card `brief_pack.TOOLING["qa-scout"]` :186-192) |
| D4 | `references/stand-answers.json:113` (`login_remedies` L3 `remedy`) | `"Look at the stand, not the login: python \"${CLAUDE_PLUGIN_ROOT}/scripts/stand_health.py\" --probe."` | `"Look at the stand, not the login: {script:stand_health.py} --probe."` | resolved by the ONE reader of the table, `env_probe.stand_answers()`, at load: every string of the loaded table goes through `runtime_paths.expand_script_tokens(text)` (root `package_root()`), before any `env_probe.fill` (F3, F4) | `stand_health._login_receipt` / `_login_remedy` -> the sentence of `stand_health.py --probe` (runner card `STAND_PROBE`, `brief_pack.py:150`; the conductor at qa-doctor) |
| D5 | same file `:116` (`login_recheck`) | `"python \"${CLAUDE_PLUGIN_ROOT}/scripts/env_probe.py\" --project-root . --json and record ..."` | `"{script:env_probe.py} --project-root . --json and record its login.record as environment.access.login_probe"` | as D4 | `stand_health._login_receipt` (`:708`) |

The token (F3/F4): `{script:<name>}` where `<name>` matches `[A-Za-z0-9_]+\.py` — ONE path component, no slash, no dot-dot.
`expand_script_tokens(text, root=None) -> str` replaces each such token by `script_command(name, root)` (existence check ON:
a missing script gives the gap text, FR-59); anything else — a non-string, a text with no token, a malformed token
(`{script:}`, `{script:../x.py}`, `{script:a/b.py}`, `{script:x.txt}`) — comes back unchanged. Never reads `os.environ`.

## 4. Builder parts (the node is 15 files: cut into two parts with disjoint owns — F6)

Hot files (D-0048 function lists): `story_step.py (_prompt, _s5_plan_init, run_mode_refusal)`,
`driver_dispatch.py (DriverDispatch.run_role, s1_reference_window, s7_place_lines, s7_neighbour_lines, s7_session_line)`,
`driver_stage_s7.py (DriverStageS7.investigation_lines, s7_rejudge_round)`, `execution_request.py (_probe_door)`. The batch
header already queues `story_step.py`, `driver_*` behind batches 4-7 and onboarding-forge 1-4 (`очередь:` lines :11-19):
the part merges `main` into its tree before the critic, and resolves a conflict in its own functions itself.
Shared test file: `scripts/tests/test_ahead_cards.py` — Part 1 owns `(role_text_roots, main)`, Part 2 owns
`(charter_card_join, ON_CARD_RE, CHARTER_CARD_SCRIPTS, DATA_CARD_SCRIPTS)`; the later part merges the earlier one.

---

### Part 1 — code-built role texts through the survivor

given: this spec §1, §3.1, §5; C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/design/factory-rules.md (whole); C:/QAFactory/forge-repo/plans/builder-rules.md; C:/QAFactory/forge-repo/docs/TESTING.md; under C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/: scripts/runtime_paths.py (:229-266); scripts/driver_dispatch.py (:594-700, :2452-2500, :3861-3970); scripts/driver_stage_s7.py (:693-752, :1010-1062); scripts/execution_request.py (:2738-2766); scripts/stage_done.py (:194-211, :627-665); scripts/story_step.py (:250-295, :604-621, :725-735); scripts/handoff_check.py (:2808-2850); scripts/driver_core.py (:412-417, :492-501, read only); scripts/tests/test_ahead_cards.py (whole); scripts/tests/fixtures/driver-layers.json (read only); scripts/tests/test_execution_request.py (:330-360, read only — its fixtures for a `_probe_door` cfg); scripts/tests/test_s7_rejudge.py (read only, keep — it judges `s7_rejudge_round`); scripts/refusal_registry.py (read only)
owns:
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/driver_dispatch.py (DriverDispatch.run_role, s1_reference_window, s7_place_lines, s7_neighbour_lines, s7_session_line)
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/driver_stage_s7.py (DriverStageS7.investigation_lines, s7_rejudge_round)
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/execution_request.py (_probe_door)
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/stage_done.py (current_code_diff_refusal, _s3_remark_package)
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/story_step.py (_prompt, _s5_plan_init, run_mode_refusal)
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/handoff_check.py (refusal_text)
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/tests/test_ahead_cards.py (role_text_roots (new), main)
non-goals: no change to what any refusal refuses, to its first 90 characters or to its A24 row; no new Driver method and no edit of driver-layers.json; no edit of runtime_paths.py (Part 2) or of any data file; no conductor literal (skills, phases, common-rules.md :131-140, story_step.py :1034/:1101, config_contract.py, source_exclusions.py — OH8-5); no other `self.scripts` hand spelling outside the owned functions (§6 R1); no new test file; no edit of test-layers.json or of a quarantined test (test_story_step_prompt.py, test_story_step_materialize.py, test_s1_exit_impl_diff.py, test_s3_remarks.py, test_s7_investigation_driver.py, test_place_driver.py, test_place_session.py — not run); a keep test that turns red on an intended text change (e.g. test_s7_rejudge.py) is named in the report with the line, not edited outside owns — the Lead adds it to owns in a fix round; no edit of the story fixture `fixtures/stories/local-1-0108/state/findings/s3-remarks-3a9a940b0ea5.md` (an artifact of a real run, it keeps the old literal: E10)
handoff: builder report (`.claude/agents/builder.md` rule 7): the diff; the FR walk A-G; the AR lines of §1.2 (AR-15 line `sites wired to script_command; axis 37 queued to Lead`); the verbatim witness; a table site -> the call it now makes and its root (P or R); the grep of §1.2 AR-13 pasted (owned functions: 0 hits; positive control `hooks/hooks.json`); "needed beyond the manifest"; analogs noticed, not fixed
edges: E1-E12 of §5 (P vs R root, spaces, `$`/quote roots, both quotes, missing script, backticks around the gap text, A24 keys, hot path, no root, s3-remarks name, temporal old files, no-Bash reader)
DoD: (1) the sites C1-C13 read as §3.1 says, each through `RP.script_command` with the root of its row; (2) ONE new function `role_text_roots()` in `test_ahead_cards.py`, called from `main()`, a table whose rows are named by site id — rows C1 (`s7_place_lines`), C2 (`s7_neighbour_lines`), C3 (`s7_session_line`, records `ready` and `failed`), C4 (`investigation_lines`), C5 (`s7_rejudge_round`, with a stub `rework` that records its `extra`), C6 (`_probe_door`, cfg with a recorded checkout and no probe; `runtime_probe.containers` raising), C7 (`current_code_diff_refusal`, a story whose `work/impl-diff.txt` holds a line), C8 (`_s3_remark_package`, the written file's text), C9 (`_prompt`, a Bash role and a form), C10 (`refusal_text`, a Bash role and one real problem) — each built through the REAL function on a stub object / temp story (one world per file, TESTING.md budget) with root `X = <tmp>/qa$copy` holding `scripts/<every name the row's text names>` (driver rows: `stub.plugin = X`; the others: `runtime_paths.package_root` replaced by `lambda: X` and restored in `finally`); each row asserts (a) `claude_plugin_root` is absent (case-insensitive), (b) at least one `python '<p>'` command is found (the `$` root forces the survivor's single-quote form: a hand spelling gives double quotes and fails), (c) every `<p>` starts with `X.as_posix() + "/scripts/"` and exists; plus ONE row C7-E4 with a root lacking `scripts/stage_done.py`: the text holds `` `stage_done.py` (missing from the plugin copy at `` and no `python ` path; (3) verification run, pasted verbatim: `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/driver_dispatch.py scripts/driver_stage_s7.py scripts/execution_request.py scripts/stage_done.py scripts/story_step.py scripts/handoff_check.py scripts/tests/test_ahead_cards.py` and every non-quarantined file it prints, plus `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/tests/test_ahead_cards.py`, `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/tests/test_s7_rejudge.py`, `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/tests/test_driver_layers.py` (a point file, builder-rules 7c), `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/refusal_registry.py --check` and `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4/ai-packages/qa-factory/scripts/tests/test_judgment_census.py`
siblings: R1 (other driver `self.scripts` spellings in role/person texts: `driver_runner.py:1080-1083`, `:1107`, `driver_dialog.py:275`, `driver_gates.py:1168`, `driver_machine.py:147`, `:1715`, `:3913`, `driver_stage_build.py:504`) — §6, not this part; `handoff_check._arg` vs the survivor's quoting (§6 R3); report any other hand-made absolute script spelling you notice, do not fix it
designer: C:/QAFactory/forge-repo/docs/tasks/specs/t-322-oh8-4-plugin-root-literal.md

---

### Part 2 — data carriers: the card marker for raw-read files, a token resolved by the table's reader

given: this spec §1, §3.2, §5; C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/design/factory-rules.md (whole); C:/QAFactory/forge-repo/plans/builder-rules.md; C:/QAFactory/forge-repo/docs/TESTING.md; under C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/: scripts/runtime_paths.py (:229-266, :357-361 the existing tokens); scripts/env_probe.py (:221-263 `stand_answers`, :320-331 `fill`); scripts/stand_health.py (:686-753, read only); references/stand-answers.json (:105-120); references/templates/requirements-register.md (:108-120, :176-186); handoffs/s0-setup-to-scout.yaml (whole); scripts/handoff_init.py (:119-147, read only); scripts/brief_pack.py (:86-95, :184-212, read only); scripts/tests/test_ahead_cards.py (:152-191, :330-345); scripts/tests/test_runtime_paths.py (:500-590)
owns:
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/scripts/runtime_paths.py (expand_script_tokens (new), SCRIPT_TOKEN_RE (new))
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/scripts/env_probe.py (stand_answers)
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/references/stand-answers.json
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/references/templates/requirements-register.md
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/handoffs/s0-setup-to-scout.yaml
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/scripts/tests/test_runtime_paths.py (k5_script_command or one new k-function beside it)
C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/scripts/tests/test_ahead_cards.py (charter_card_join, ON_CARD_RE, CHARTER_CARD_SCRIPTS, DATA_CARD_SCRIPTS (new))
non-goals: no edit of stand_health.py (the token is resolved in the table's one reader, never a second parser), handoff_init.py, brief_pack.py or any code file of Part 1; no new brief or card line (both scripts are already on their roles' cards); no other row or key of stand-answers.json; no other template text; no conductor text (OH8-5); no new test file; no edit of test-layers.json or a quarantined test (test_login_body_fields.py, test_stand_health.py — not run); no helper named `*_problems` / `*_check`
handoff: builder report: the diff; FR walk A-G; AR lines of §1.2; the verbatim witness; the list carrier -> reader -> how filled; "needed beyond the manifest"
edges: E13-E22 of §5 (malformed token, fill after expansion, root with braces, cache, temporal, marker on no card, marker vacuity, old S0 forms, broken card, Codex, human-text detector)
DoD: (1) `runtime_paths.expand_script_tokens(text, root=None)` exists as §3.2 says; ONE table of rows in `test_runtime_paths.py` (named by edge id, `root=` passed explicitly): T-ok (an existing script -> exactly `script_command(name, root)`), T-$ (a `$` root -> the single-quoted form), T-missing (gap text), T-two (two tokens in one text, both expanded), T-none (a text with no token -> equal, unchanged), T-bad (`{script:}`, `{script:../x.py}`, `{script:a/b.py}`, `{script:x.txt}` -> unchanged), T-nonstr (None, 5 -> returned as is); (2) `env_probe.stand_answers()` passes every string of the loaded table (nested in lists and dicts) through `expand_script_tokens` before caching it; D4 and D5 read as §3.2; (3) D1-D3 read as §3.2; (4) `charter_card_join` extended: carriers = `agents/*.md` + `references/slices/**/*.md` + the three data files, none holds `claude_plugin_root` (case-insensitive); the data marker join: for `references/templates/requirements-register.md` the roles are those whose `brief_pack.ROLE_FILES` entry holds `plugin:references/templates/requirements-register.md`, for `handoffs/s0-setup-to-scout.yaml` the role is its parsed `to_role` (through `handoff`'s parser, never a regex on the yaml); every `ON_CARD_RE` script of the carrier is on that role's card; found set == `DATA_CARD_SCRIPTS = {("qa-requirements-tester", "branch_accounting.py"), ("qa-scout", "ticket_adapter.py")}` (vacuity guard); and through the reader: after `env_probe.reload_stand_answers()`, `login_recheck` starts with `RP.script_command("env_probe.py")` and the L3 remedy holds `RP.script_command("stand_health.py")`, no string of the loaded table holds `{script:`; (5) verification run, pasted verbatim: `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/runtime_paths.py scripts/env_probe.py references/stand-answers.json references/templates/requirements-register.md handoffs/s0-setup-to-scout.yaml scripts/tests/test_runtime_paths.py scripts/tests/test_ahead_cards.py` and every non-quarantined file it prints, plus `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/scripts/tests/test_ahead_cards.py`, `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/scripts/tests/test_runtime_paths.py`, `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/scripts/tests/test_judgment_census.py`, and `python -B C:/QAFactory/forge-repo/.claude/worktrees/oh8-4b/ai-packages/qa-factory/scripts/role_load.py --all --json` (report: no process row moved)
siblings: `references/human-text.json:61-63` `plugin_path` pattern no longer sees an installed absolute root (E22, §6 R2); OH8-5 conductor texts; report any other data file a role reads that names a script by the variable
designer: C:/QAFactory/forge-repo/docs/tasks/specs/t-322-oh8-4-plugin-root-literal.md

## 5. Edges, each with the invariant it protects

| Id | Edge | Behaviour | Invariant protected |
|---|---|---|---|
| E1 | driver started with `--plugin-dir X` while its code runs from copy Y | driver texts use `self.plugin` (X) — the copy whose hooks guard the role and whose scripts the driver runs (`self.scripts/<script>`, `driver_runner.py:221`); today the literal resolved to X too (the driver exports `CLAUDE_PLUGIN_ROOT=X`, `driver_core.py:501`) | a brief line and the role's card never name two copies; a driver run's behaviour is unchanged (F1) |
| E2 | root with spaces (`C:/Program Files/qa factory`) | double-quoted by the survivor | one shell word; C11 today is UNQUOTED and breaks — fixed by the move |
| E3 | root with `$`, a backtick or `"` | single quotes | a pasted command never expands into another path |
| E4 | root with `'` and one of `$`/backtick/`"` | the survivor's plain-text form; the site's argument tail follows (OH5-2 N5) | no command that resolves elsewhere is printed; C10 keeps its file door ("or, in any shell or none: Write ...") so FR-57 holds; C9's role still has `finish` running the checker by code |
| E5 | the named script is missing from the copy (partial install) | the gap text `` `<name>` (missing from the plugin copy at <root>; the conductor runs qa-doctor ...) `` + the tail | FR-59: a path that does not exist is never printed |
| E6 | the gap text (it holds backticks) lands inside a backtick span (C1-C4, C6, C7) | accepted: the nesting breaks markdown rendering, the words stay readable; the same shape OH5-2 accepted for guard doors (`guard_pre_tool.py:772`) | one road with the guard (P31); the door is still named |
| E7 | the root is absent | cannot occur: `self.plugin` is always set (`driver_core.py:416`, default `HERE.parent`), `package_root()` is the running file's copy; nothing reads `CLAUDE_PLUGIN_ROOT` | a parent's or host's stale value (t-024 R6b) never decides a path |
| E8 | A24 keys | every changed span is past char 90 of a guard `block(...)` argument, or in a refusal that is not a guard block | the registry is untouched; `refusal_registry.py --check` stays green |
| E9 | hot path | the survivor (one `stat`) runs only while building a text about to be shown: a refusal on its way out, a brief line per dispatch; C6 and C10 import lazily inside the branch | a call that passes pays nothing new |
| E10 | C8: the s3-remarks file name is the sha of its body, and the body now holds an absolute path | the same plan, findings AND copy give the same file (the E6 of `_s3_remark_package`'s docstring narrows by "and copy"); another copy writes a new file beside the old one; the fixture file of `local-1-0108` keeps its literal (a real run's artifact, never rewritten); `test_story_closed.py:628` matches the name by pattern, not by value | a derived file is never rewritten in place (FR-45); no reader of the old file loses it |
| E11 | TEMPORAL (Part 1): a story started before the change holds old derived files (s3-remarks, logged refusals) with the literal | read as they are; nothing migrates them; every NEW text names the path | an artifact on disk is immutable; both worlds stay readable |
| E12 | C8 / C9 / C10 reader without Bash | C8 keeps "with a shell,"; C9 and C10 already branch on `role_has_bash` / `_doors` — the command line is only in the Bash branch | a role is never sent to a command it cannot run (FR-2) |
| E13 | malformed token (`{script:}`, `{script:../x.py}`, `{script:a/b.py}`, `{script:x.txt}`) | left as written | the token never resolves outside `<root>/scripts/` (one component, `.py` only) |
| E14 | `env_probe.fill` runs after the expansion (L3 goes through `_login_remedy` -> `fill`) | expansion happens at load, so `fill` sees no token; a root holding `{`/`}`: `fill` catches the format error and returns its input unchanged (`env_probe.py:327-330`) — the expanded path is kept; a row holding BOTH a token and `{user_key}` would then keep `{user_key}` unfilled (visible, never wrong); no such row exists today (L1/L2 hold `{user_key}` and no command) | the expanded path is never altered by a later fill; a gap is visible, never a wrong value |
| E15 | the table cache (`_stand_cache`, keyed by the table path) | the resolved table is cached per process; the package root does not change inside a process; tests call `reload_stand_answers()` after replacing `package_root` | a cached text never names another copy than the one this process runs |
| E16 | TEMPORAL (Part 2): `expand_script_tokens` does not exist before Part 2 | the expander, the reader change and the two tokens land in ONE commit | a raw `{script:...}` never reaches a reader at any commit |
| E17 | D1-D3 marker form: the script is missing from the reading role's card | the join fails naming carrier, role and script | a script a role is told about is reachable by the absolute path its card gives (FR-15) |
| E18 | the marker spelling drifts and the data join finds nothing | found set must equal `DATA_CARD_SCRIPTS` | the join is never vacuous |
| E19 | an S0 form instance written before the change | keeps the old value; `handoff_check` reads the contract's spec (a plain `text` field, `handoff._spec_of_value`), so both values are "filled" | no refusal appears on an old form |
| E20 | a role reading D1/D2 whose card cannot be built (a broken copy) | the brief already says so (brief_pack's own fallback); this node adds no path | no fabricated path (FR-59) |
| E21 | Codex vs Claude host | the same text on both; no host variable is relied on | AR-5 |
| E22 | `references/human-text.json` `plugin_path` (`CLAUDE_PLUGIN_ROOT` or `ai-packages/qa-factory/(scripts|...)/`) on a person-facing text | before: the literal matched; after: an INSTALLED root (`.../plugins/cache/...`) does not match, a dev checkout still does | reported (§6 R2): the detector's blind spot is named, not fixed here; the person-facing texts of this node (C6 door, D4/D5 sentences) reach a person through the conductor |

Conflicting requirement pairs named: (a) "the root through `script_command`" vs "a data file cannot call a function" — D1-D3
by the card marker (the card is built by `script_command`), D4-D5 by a token resolved in the table's reader (F2, F3);
(b) "draw the line role/conductor" vs the sweep rule (same artifact, same class) — hand spellings with a conductor reader in
`story_step.py` are swept (C13), literals with a conductor reader are not (OH8-5) (F5); (c) AR-15 "axis in the same commit"
vs "SIBLING_MAP is the full Lead's" — queued (t-254 F7 stands); (d) "a new case is a row" vs "15 files in one node" — two
parts, test functions split by D-0048 lists (F6).

## 6. Residuals and reported analogs (named, not widened — rule 3)

- **R1 — the same class beyond this node** (hand-made absolute script spelling in texts outside the owned functions):
  `driver_runner.py:1080-1083` (`python {self.scripts}/planning_contract.py`, unquoted), `:1107` (resume command),
  `driver_dialog.py:275`, `driver_gates.py:1168`, `driver_machine.py:147`, `:1715`, `:3913` (person-word doors),
  `driver_stage_build.py:504` (`stand_identity.py`, unquoted). Readers: roles, the conductor, the person. Proposed node
  (a `findings/` file and a row in an untaken batch of onboarding-hooks, D-0044 — batch-8 is taken): owns those files,
  test = rows in `role_text_roots`. Cost: 5 files, ~10 sites. See F5.
- **R2 — `human-text.json` `plugin_path`** misses an installed absolute root (E22): the pattern could be built with the
  running package root at check time; a human-text matter, not this node.
- **R3 — two quoting rules in one line**: `handoff_check._arg` (`:2815-2818`, quotes on whitespace/quote/shell chars)
  quotes the form path, the survivor quotes the script path differently (`$` -> single quotes). For axis 37's note.
- **Brief/finding contradictions** (reported): the finding's expected owns name `test_stage_cards.py` and
  `test_story_step_manual_block.py` pins; both pin PHASE-FILE (conductor) literals — `test_stage_cards.py:76`
  (`PY_COMMAND` over `skills/qa-story/phases/s*.md` cards) and `test_story_step_manual_block.py:627-645` (`s6.md` card
  lines) — so they belong to OH8-5, not here. The keep tests this node writes are `test_ahead_cards.py` and
  `test_runtime_paths.py`. Keep tests that judge owned functions and do NOT hold the literal (Grep -i
  `claude_plugin_root` over `scripts/tests/*.py`: no hit in them): `test_s7_rejudge.py`; `test_execution_request.py:349`
  and (quarantined) `test_s1_exit_impl_diff.py:54` match a suffix (`runtime_probe.py" --suggest ...`,
  `stage_done.py" --task QA-1 ...`) that the survivor's double-quoted form keeps.
- **Producer of an S0 form instance not found**: Grep `s0-setup-to-scout` over the package finds only `handoffs/index.yaml:40`,
  `handoffs/README.md:40` and the contract; Grep `handoff_init` over `skills/qa-story` finds only `s8.md:223`. Whether any
  code writes an S0 instance today is not established; D3's reader is taken from the contract (`to_role: qa-scout`).
- **Axis 37** (t-254 §7) is not in `docs/SIBLING_MAP.md` on origin; the full Lead writes it with these sites as callers.

## 7a. Lead decisions (coordinator Opus, 2026-11-13; "решила сама", by recommendation until the owner's word)

F1 through F7 are decided as recommended: (a) in every fork. F6 (a) runs Part 1 in worktree `oh8-4` and Part 2 in worktree `oh8-4b`, in parallel. A critic-on-plan (t-327) comes before any builder (rule 3, because the spec carries forks).

## 7b. Critic t-327 fixes (BINDING; each overrides the body text it names)

Review: `docs/tasks/specs/reviews/t-327-oh8-4-plan-review.md`, verdict fit_with_fixes. The coordinator accepts it as follows ("решила сама").

1. **B1 (Part 2).** The D3 value is ``"`ticket_adapter.py` (on your card)"``, with backticks, in §3.2 and §7 F2.
2. **B2 (Part 1): option (a).**
   - Drop C7 (`stage_done.current_code_diff_refusal`) and the row C7-E4 from Part 1. No role reads C7: the conductor (`s1.md:35`) and the driver (`driver_machine.py:928`) run it. `stage_done.py:209` goes to OH8-5, next to `story_step.py:1034/:1101`.
   - The missing-script row moves to C6: `C6-E4`, a root lacking `scripts/runtime_probe.py`, gives the gap text and no `python ` path.
   - Part 1's owns line for `stage_done.py` keeps only `_s3_remark_package`.
3. **B3 (Part 1).** Add rows:
   - `C12`: `s1_reference_window` with `self.py` stubbed;
   - `C13a`: `_s5_plan_init` with `SP.init` raising `PlanUnreadable`;
   - `C13b`: `run_mode_refusal(task, switch)`;
   - `C11`: `run_role` with `run_claude` stubbed to capture `full_prompt`, plus the E2 assertion that a root with a space yields one double-quoted word.

   If `run_role` cannot be driven with that stub alone, C11 becomes a NAMED exemption, judged by the AR-13 grep pasted in the report. The report says which route was taken.
4. **B4.** Add edge E23: C11 names the placeholder `<name>.py`, so `must_exist=False`. A copy missing `scripts/` is not detected there; qa-doctor owns that gap. The invariant: the prompt and the card head spell the root one way.
5. **B5.**
   - Every new import in `test_ahead_cards.py` goes INSIDE its owning function, and neither part owns the module header.
   - `role_text_roots` goes directly before the `if __name__` block.
   - ONE code critic runs after both parts converge. The later part merges the other branch, resolves the conflict, and the critic comes after that merge.
6. **B6.** F4 gets one sentence: `PLUGIN_TOKEN` is a stored-path hint resolved in leading position to a bare path, while `{script:<name>}` is a command spelling resolved through `script_command`. They are two actions, each with one road.
7. **N1.** `handoff_help.py` stays bare in C9/C10. Verdict: n/a. The card head names the root pattern, and keep pin `test_handoff_values_refusal.py:81` holds the text.
8. **N2 and N3.** The coordinator writes, at node acceptance, two lines into batch-8 «Остатки»:
   - what OH8-5 now carries: `story_step.py:1034/:1101` and `stage_done.py:209`;
   - residual R4: widen `refusal_registry._host_root_lines` to the files cleared by OH8-4 and OH8-5.

   This is not builder work.

## 7. Forks — each with options, a recommendation, and what the builder runs on until answered

- **F1 — the root of the driver's texts.** (a) `self.plugin` (the dispatched copy; same as today's resolution of the literal
  in a driver run; agrees with the card the role gets); (b) `package_root()` (the copy the driver code runs; differs from
  (a) only under `--plugin-dir`, and then disagrees with the role's card and guard). **Recommendation: (a).**
- **F2 — data files a role reads RAW (D1-D3).** The brief asks "filled at build time, or a placeholder resolved by the
  reader". (a) the card marker `` `<name>.py ...` (on your card) `` — no build step exists for the template (the role reads
  the shipped file) and none is needed for the S0 form; the absolute command is on the reader's card, built by
  `script_command`; joined by `charter_card_join` (OH5-2 Part B's form, one road with the charters); (b) for D3 only, a
  `{script:ticket_adapter.py}` token expanded by `handoff_init.fill_head` (adds `handoff_init.py` to Part 2; D1 cannot take
  this road, so two forms remain for raw files); (c) serve the template through code (a copy into the story) — a new
  artifact and writer (AR-14), out of proportion. **Recommendation: (a).** Its deviation from the brief's wording: the root
  reaches the role through the card the survivor built, not through the text itself.
- **F3 — the code-read table (D4-D5).** (a) a token `{script:<name>}` resolved by the table's ONE reader
  `env_probe.stand_answers` at load (AR-13; the quarantined `test_login_body_fields.py:422` keeps reading `login_recheck`
  as the sentence carries it); (b) resolve in `stand_health` where the sentence is built (a second parser of the table's
  text); (c) the bare script name (the runner has it on its card, the conductor does not: one reader loses the path).
  **Recommendation: (a).**
- **F4 — where the token expander lives.** (a) `runtime_paths.expand_script_tokens` beside `script_command` (the survivor's
  home; one token spelling for every future data carrier; Part 2 owns `runtime_paths.py` and its table); (b) a private regex
  in `env_probe` (fewer files; a second token road appears with the next data carrier). **Recommendation: (a).**
- **F5 — scope of the sweep (sweep-the-artifact-first rule; designer rule 6).** (a) include the hand spellings of the SAME
  files (C11 `run_role`, C12 `s1_reference_window`, C13 `story_step` :618/:734) and open R1 as a named residual node;
  (b) only the 10 sites the finding names, everything else to R1; (c) widen to R1 now (+5 hot files: `driver_runner`,
  `driver_dialog`, `driver_gates`, `driver_machine`, `driver_stage_build`; ~10 sites; more queue lines). **Recommendation:
  (a)** — C11 is every driver-mode role prompt and is unquoted today (E2); R1 is a node with owns and a test, so it is a
  slice, not an exclusion.
- **F6 — the cut.** (a) two parts as §4, in parallel, Part 1 in worktree `oh8-4`, Part 2 in a new worktree `oh8-4b`, the
  later merge resolves `test_ahead_cards.py` (disjoint function lists); (b) the same two parts sequentially in `oh8-4`
  (Part 2 after Part 1; no merge of the test file; slower; all owns under `oh8-4` as the brief said); (c) one builder,
  15 files. **Recommendation: (a)**; (b) if the Lead keeps every owns under `oh8-4`.
- **F7 — test home of the built-text rows.** (a) `test_ahead_cards.py` (keep, `data_join`: "a text a role reads names
  scripts that exist at its card's copy" is the same join as "every card names its scripts"); (b) `test_runtime_paths.py`
  (keep, `table`: the survivor's table would import six heavy modules). **Recommendation: (a).** Note: the keep row's
  `covers` of `test_ahead_cards.py` (`test-layers.json:55-75`) does not list the six modules, so `--witness-for` of them will
  not print it — the DoD names it explicitly; the Lead may refresh `covers` with `tools/test_quarantine.py` (not the builder).

## 8. Small technical choices closed by the designer (no design weight)

No new Driver method (driver-layers.json lists every method); lazy `import runtime_paths as RP` where the module does not
import it (`execution_request`, `handoff_check`, the driver methods), module-level `RP` where it exists (`stage_done:41`,
`story_step:97`); argument tails kept after the survivor's text; the marker text `(on your card)` (the existing `ON_CARD_RE`,
`test_ahead_cards.py:166`, matches it); token regex `\{script:([A-Za-z0-9_]+\.py)\}`; expansion over every string of the
loaded table (one walk, not per key); `$` temp root in the rows (it discriminates the survivor from a hand spelling); the
survivor's existence check stays ON for every site except C11 (a `<name>` placeholder, `must_exist=False` as the brief card
head); D4/D5 root `package_root()` (the running copy, as the guard), not the table file's folder (a test may point
`STAND_ANSWERS_PATH` at a fixture).

## 9. Reading trail

- `plans/piles/onboarding-hooks/findings/20261113-oh5-2d-...md` (whole); `batch-8-ostatki-t-282-t-254-t-287.md` (whole).
- `docs/tasks/specs/t-254-oh5-2-plugin-root-given.md` (whole, two reads).
- `scripts/runtime_paths.py` (whole).
- Grep `claude_plugin_root` -i over `scripts/*.py` (content) and over the package (count, positive control hooks.json/codex.json).
- `driver_dispatch.py` :680-704, :2470-2501, :3835-3974, def list; `driver_stage_s7.py` :680-719, :1020-1059, def list;
  `driver_core.py` :405-504; `execution_request.py` :2725-2769; `stage_done.py` :190-219, :630-664; `story_step.py`
  :245-289, :600-624, :715-744; `handoff_check.py` :2805-2849; `guard_pre_tool.py` :1110-1120.
- Grep `self\.scripts` (content, count), `script_command`, `self\.plugin\s*=`, `HERE\.as_posix\(\)`, `import runtime_paths`.
- Data: `requirements-register.md` (Grep -C3), `s0-setup-to-scout.yaml` (whole), `stand-answers.json` (Grep -C4);
  `handoffs/README.md` (whole); `handoff_init.py` :1-160, def list; `handoff.py` :429-447, :590-680; `env_probe.py`
  :220-269, :320-331; `stand_health.py` :690-764; Grep `stand-answers|login_recheck`, `s0-setup-to-scout`, `handoff_init`.
- `brief_pack.py` :80-99, :180-219, Grep of `branch_accounting|ticket_adapter|plugin:`; `agents/*.md` `tools:` lines.
- `role_load.py` :215-324; Grep of `inject-map.json` (none / positive control 71).
- Tests: `test_ahead_cards.py` :130-191, imports, main call; `test_stage_cards.py` :1-110; `test_story_step_manual_block.py`
  :615-654; `test_login_body_fields.py` :405-444; `test_story_closed.py` Grep `s3-remarks`; Grep of pins over
  `scripts/tests/*.py`; `test-layers.json` :1-75, :1480-1509, :4254-4313, :4540-4579, section heads (keep :35, cohorts
  :6965, quarantine :7013), keep/quarantine row Grep (keep: test_ahead_cards, test_execution_request, test_refusal_registry,
  test_runtime_paths, test_stage_cards, test_story_step_manual_block, test_s7_rejudge, test_driver_layers,
  test_judgment_census; quarantine: test_bug_neighbours, test_place_answers, test_place_driver, test_place_session,
  test_s1_exit_impl_diff, test_s3_remarks, test_s7_investigation_driver, test_stand_health, test_story_step_materialize,
  test_story_step_prompt, test_login_body_fields); `fixtures/driver-layers.json` Grep; `scenario_walk.py` Grep `covers`;
  `selftest.py` Grep `covers`.
- `design/architecture.md` :98-187; `docs/SIBLING_MAP.md` axis headings 34-36 (no 37); `docs/TESTING.md` :36-135;
  `plans/builder-rules.md` :15-69; `references/human-text.json` :58-65.
