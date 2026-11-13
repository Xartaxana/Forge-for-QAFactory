# t-254 — OH5-2 (onboarding-hooks/5, П2): the package root is GIVEN, never a literal `${CLAUDE_PLUGIN_ROOT}` in text a role reads

> **Amendment of 13.11.2026 05:15** (coordinator, «решила сама»; t-273 builder measurement). The §3.2 legend cell
> "`references/…`, `scripts/…`, the script paths of your brief card (`python "<path>/scripts/<script>"`)" turned out 6-7
> tokens longer than the old cell. That raised 8 roles above slack-0 ratchets, and E23/AR-20 forbid a raise. Part B
> uses the shorter cell "`references/…`, `scripts/…`, the script paths on your card" instead, and DoD 2 reads with that
> text.

Draft by designer (t-254) for the Lead. Status: DRAFT rev 2 (resubmission after critic on plan t-257,
`docs/tasks/specs/reviews/t-257-oh5-2-plan-review.md`; change log at the end). Findings: B-142, B-166.
Node row: `plans/piles/onboarding-hooks/batch-5-nerazlozhennye-nakhodki.md` OH5-2 (origin/main :31, confirmed by the
critic t-257 Key 1; see §8).

## 1. Intent, rules and invariants touched

Intent (Lead brief): a path a role needs is GIVEN to it (FR-15, FR-37, AR-8). No literal `${CLAUDE_PLUGIN_ROOT}` in
any text a role reads. Guard refusal texts substitute the real package root when they are built (the guard knows where it
lives); role bodies (`agents/*.md`) take the path from the brief; `experiments/measurers/run_headless.py` gives its
child what the host is KNOWN to give (rev 2: the desktop road, measured — §3.3).

Why it matters (finding evidence): experiment t-024 (B-142): a subagent sees the literal unexpanded, and its Bash has
`CLAUDE_PLUGIN_ROOT` empty unless a parent exported it (R3b); with a parent value it inherits THAT value (R6b), which can be
another copy of the plugin. Only the driver exports it (B-014, `driver_core.py:492-501`).

### AR-n touched, with the change check each one demands (written into the DoD of the parts)

| AR | How this node touches it | Change check (in DoD) |
|---|---|---|
| AR-8 a role is handed its paths and commands | the door command in a refusal and the script a charter names reach the role as an absolute path from the brief card / the guard's own copy | the 4 charters name scripts that are on the role's card (join row, Part B); every guard door names an existing absolute path (Part A rows) |
| AR-13 a fact with a reader is read through it | "the package this process runs" has a reader: `runtime_paths.package_root()` (`runtime_paths.py:229`); the guard door goes through it, never through `os.environ` or a hand-made `Path(__file__)`; "does a role have Bash" is read through `host_adapter.role_has_bash` (axis 19); the env of a `claude -p` child through `infra_failure.child_env` | grep the guard for `CLAUDE_PLUGIN_ROOT` (case-insensitive, positive control on `hooks/hooks.json`): 0 hits after Part A |
| AR-15 one survivor, wired everywhere | new survivor `runtime_paths.script_command(name, root=None, *, must_exist=True)` spells `python "<root>/scripts/<name>"` once; the guard's 11 sites and the brief card head (`brief_pack`) call it; Part C composes on the existing survivor `infra_failure.child_env` | list every site (§2 census); a site that cannot call it is named on the new axis (F7). The axis is queued to the full Lead (F7): Part A's commit line reads `architecture: AR-15 -- survivor added, axis queued to Lead (F7)`, never "kept" |
| AR-5 host read through one adapter, no host naming | the root is taken from the running file, not from a host variable; Claude Code and Codex get the same text | no new reader of a host env var; `hooks/hooks.json` and `hooks/codex.json` untouched |
| AR-9 every refusal names a door its receiver can use | the doors of 8 refusal builders change text (not meaning); no A24 key changes (keys are the first 90 chars of `block(...)`'s first argument; every site is in a door variable or past char 90 — critic t-257 E11 trace) | `test_refusal_registry.py` green (A24); no new refusal, no new A24 row; `refusal_registry.py --check` green |
| AR-29 code judges data | one NEW check: a refusal_registry finding "a refusal source carries an unexpanded host root variable" | class `shape` (presence of a token in string constants), owner `data`; see census line below |
| AR-20 shrink-only ratchets | Part B shrinks process-kind charter text and the 10 slices; `role_load.process_ratchet_problems` has slack 0 (`role_load.py:259-282`, keep `test_role_load.py:541-546`, audit A22) | process ratchet rows lowered (slack 0) in the same commit; no raise (Part B DoD (5), E23) |

### Checks this node adds or alters — owner and census class (AR-29, P27)

| Check | Where | Owner it serves | Census class | Census row |
|---|---|---|---|---|
| refusal source carries `claude_plugin_root` (any case, any spelling) in a string constant → finding | `refusal_registry.findings()` (A24, run by `test_refusal_registry.py` and by `audit_factory` at qa-doctor; A24 is factory-owned, `audit_factory.py:255`) | data (code) | shape | `refusal_registry.py` has no census rows today (grep of `judgment-census.json`: no `"refusal_registry.py"` row; positive control: the `"runtime_paths.py"` rows found, origin :712-714). `findings()` is not a census unit; a helper named `*_problems` WOULD become one (UNIT_NAME_RE, `test_judgment_census.py` docstring) — so the builder does not name the new helper `*_problems`; if `test_judgment_census.py` still names a unit, ONE row `class: shape, owner: data, roles: ["conductor"]` — no count of word-list/meaning-proxy/meaning/safety moves |
| join: every script a Bash role's charter names with the marker `(on your card)` is on that role's card; no role-read text carries the variable | `scripts/tests/test_ahead_cards.py` (keep, layer data_join) — a test row, not a package check unit | data | — (tests are not census units) | none |
| guard door texts | 8 builder functions in `guard_pre_tool.py` | unchanged: `big_read_check` shape/data, `handoff_write_check` safety/intent, `handoff_values_check` shape/data, `plan_write_check` safety/intent (`judgment-census.json:362-374`) | unchanged | unchanged — only the door wording changes, not what is refused |
| process ratchet rows (`references/role-load.json` `process_ratchet_tokens`) | data rows lowered, check unchanged | data | unchanged | unchanged |

FR walk the builder writes (PROJECT.md acceptance rule 1): A (FR-1, FR-2, FR-57 — doors), C (FR-15), D (FR-59 — the unknown
script), G (FR-30 English, FR-32, FR-54); B — "text to a person not changed" (guard texts go to roles and the conductor),
E and F — not applicable.

## 2. Census of the literal (acceptance key 1)

Command: Grep tool, pattern `CLAUDE_PLUGIN_ROOT`, case-insensitive (`-i`), path `ai-packages/qa-factory/`, count mode.
A case-insensitive substring match covers `${CLAUDE_PLUGIN_ROOT}`, `$CLAUDE_PLUGIN_ROOT`, `%CLAUDE_PLUGIN_ROOT%` and
`$env:CLAUDE_PLUGIN_ROOT` at once. **Positive control of the same shape**: the same call finds `hooks/hooks.json: 19` and
`hooks/codex.json: 28` (known host-config carriers). **Result on origin/main `1fe6fde`: 420 occurrences in 84 files**
(critic t-257 rerun `grep -rio claude_plugin_root <origin extract>/ai-packages/qa-factory | wc -l`; the designer's first
count on the stale local checkout was 417, the critic's local count 419; the delta is conductor-read
`skills/qa-onboarding/phases/p4-generate.md`). No class a Part touches changes (critic t-257 Key 1: charter 5, slice 10,
guard 11, code 8, data 5 — exact on origin). A second call, pattern `\$\{CLAUDE_` (any `${CLAUDE_*}` variable, tests
excluded, local), found 326 in 57 files; it shows the sibling `${CLAUDE_SKILL_DIR}` lives in skills and in the
common-rules legend (see F1).

| Class | Carriers (hits) | Total | Verdict in this node |
|---|---|---|---|
| **host-config** (the host expands it, legitimately) | `hooks/hooks.json` 19, `hooks/codex.json` 28 | 47 | untouched |
| **role-read: subagent charters** | `agents/qa-runner.md:61` 1, `agents/qa-failure-analyst.md:76,78` 2, `agents/qa-doc-scribe.md:63` 1, `agents/qa-retro-analyst.md:60` 1 (4 files; B-142 counted 13 in 7, the node row 5 — runner line is now :61, not :60) | 5 | **Part B** |
| **role-read: injected slices** (generated from `references/common-rules.md:112`, `<!-- roles: ... -->` section; `contract_slices.py --write`) | `references/slices/<10 roles>/common-rules.md` 1 each | 10 | **Part B** (edit the source line, regenerate) |
| **role-read: guard refusal texts** | `scripts/guard_pre_tool.py` :771 (`_config_door`), :823 (`_section_door`), :875 (`big_read_check`), :1086, :1107 (`handoff_write_check`), :1231 (rewrite check, PT-*-rewrite via registry), :1273, :1275, :1286, :1299 (`plan_write_check`), :1616 (`_window_refusal`) | 11 | **Part A** |
| role-read: other code-emitted texts (driver briefs, refusals to roles) | `driver_dispatch.py` :3868, :3910, :3951; `driver_stage_s7.py` :700, :1040; `execution_request.py:2741` (MineRefusal door); `stage_done.py` :209, :651 | 8 | residual node OH5-2d (F1) |
| role-read: data/templates a role is handed | `references/templates/requirements-register.md` :113, :180 (tester's `plugin:` door, `brief_pack.py:94`); `handoffs/s0-setup-to-scout.yaml:61` (scout's `tools.ticket_adapter`); `references/stand-answers.json` :113, :116 | 5 | residual node OH5-2d (F1) |
| conductor-read (skills, phases, references the conductor reads; the conductor has its own resolution rule `references/common-rules.md:131-140` "Resolving the plugin root", roles: none) | `skills/*/SKILL.md` 18; `skills/qa-story/phases/s0..s9.md` 177; `skills/qa-onboarding/phases/*` 34 on origin (31 local; `p4-generate.md` +3 vs the local checkout, per critic's 420-vs-417); `skills/qa-doctor/phases/*` 6; `references/judge.md` 6; `references/handoffs.md` 3; `references/common-rules.md:134` 1 (the rule itself); `config_contract.py` :1220, :1222; `source_exclusions.py:516` (`_script`, spells s1.md's form); `story_step.py` :1034, :1101 | 251 | residual node OH5-2e (F1) — measure first |
| person/developer docs | `README.md` 1, `CHANGELOG.md` 2, `design/codex-compatibility-audit.md:70` 1 | 4 | untouched (not role-read) |
| code (env export, expansion for a smoke, detectors, comments, a deliberate portable spelling) | `driver_core.py` :492, :495 (comments), :501 (export); `install_smoke.py` :196 (comment), :239 (expands the hook line); `session_env.py:10` (docstring); `brief_pack.py` :69, :209, :277 (comments); `regression_scope.py` :188-189 (detector: a regression `Command:` naming the plugin); `delivery_verdict.py` :275, :293 (deliberate: rewrites a machine path INTO the portable `${CLAUDE_PLUGIN_ROOT}/scripts/` form for a regression command a person runs on another machine, P24); `references/human-text.json:62` (detector pattern `plugin_path`) | 15 | untouched |
| eval data | `skills/qa-doctor/evals/evals.json` 1 | 1 | untouched (follows OH5-2e) |
| tests (pins, fixtures, env set-up) | 20 test files + 1 fixture (`fixtures/stories/local-1-0108/.../s3-remarks-*.md`) | 63 | only the pins Part B breaks are rewritten (keep files); quarantined pins: F6 |

Sum (origin): 47+5+10+11+8+5+251+4+15+1+63 = 420. The per-file split of the 3 extra conductor-read hits is the critic's
attribution (one file, `p4-generate.md`); the designer had no shell to re-run the count on origin (§8).

## 3. The mechanism (acceptance key 2)

### 3.1 Guard refusal texts — Part A

- **Survivor** (new): `runtime_paths.script_command(name: str, root=None, *, must_exist: bool = True) -> str` and
  `runtime_paths.script_path(name, root=None) -> Path | None`.
  - `root` defaults to `package_root()` (`runtime_paths.py:229`, "the package this process runs: never a stored value"). The
    guard's `hooklib.PLUGIN_ROOT` and `package_root()` are the same value (`Path(__file__).resolve().parents[1]` of a file in
    `scripts/`); the guard calls the survivor, so there is one spelling (AR-13, AR-15).
  - `script_path` returns `root/"scripts"/name` when that file exists, else `None`.
  - `script_command` returns `python "<root posix>/scripts/<name>"` — `Path.as_posix()`.
  - Quoting (edge E3): double quotes; when the posix root holds `$`, a backtick or `"` and no `'`, single quotes; when it
    holds both kinds, NO command form: the text is `<name> in <root posix>/scripts/ (quote this path for your shell: it
    holds characters a shell expands)`.
  - Script missing (edge E4, FR-59), only when `must_exist=True`: the text is `` `<name>` (missing from the plugin copy at
    <root posix>; the conductor runs qa-doctor to repair the installation) `` — never a path that does not exist (F4).
  - `must_exist=False` skips the existence check and the E4 branch, and keeps the quoting rule. **Choice (N4): the card
    head is built through the survivor** — `brief_pack` writes ``f"Every command is `{RP.script_command('<script>', must_exist=False)}`, ..."``
    at both card heads (`brief_pack.py:3675` walk card, `:4260` tooling card), so the card and every guard door use the
    SAME quote character for every root, E3 roots included (one road, P31). This does not break E3: `<script>` is a literal
    placeholder; quoting depends only on the root's characters, and `must_exist=False` exists precisely so the placeholder
    never reaches the E4 branch. An E3b root (both quote kinds) gives the card head the plain-text form with the
    placeholder — the same text a door would print.
  - Argument tails (N5): a site that appends arguments after the command (`:823`, `:875`, `:1086`, `:1107`, `:1273`,
    `:1275`, `:1286`, `:1299`, `:1616`) keeps its tail after the returned text in every form. In the E4/E3b forms this
    reads `` `plan_row.py` (missing from the plugin copy at X; the conductor runs qa-doctor ...) --task <TICKET> --row ... ``
    — intended: the door is still named and the flags still say what the command takes. DoD (3) pins one E4 rendering of
    `plan_write_check` so the form is deliberate.
  - Never reads `os.environ` (edge E5).
- **Sites**: every one of the 11 guard sites builds its command through `runtime_paths.script_command(...)` (lazy
  `import runtime_paths as RP`, as the guard already does at :554 and :726). `_config_door` keeps its gate (it has another
  door, `Grep -n`; TEMPORAL rule in its docstring :760-761) but spells it `RP.script_path("config_view.py")` instead of
  `(PLUGIN_ROOT / "scripts" / "config_view.py").is_file()` (same value, one reader — critic t-257 Key 3) — it does not
  print the missing form.
- **Error direction** of `package_root()` in its new, more consequential role (from "where am I running" to "the path a
  role is told to run"): it may only name the copy whose guard is refusing — the generation that enforces the rule (B-014).
  It must never name: a parent session's root (env, R6b), a stored root from a story record, a path that does not exist.
  Adversarial inputs that must stay on the safe side (table rows in Part A): a root with spaces; a Windows root with
  backslashes; a root holding `$` / backtick / `"`; a root holding `'` and `$`; a non-ASCII root (`C:/Users/Анна/...`); a
  UNC root (`\\srv\share\qa-factory` → `//srv/share/qa-factory`, as the card spells it); a script name not in `scripts/`.
- **`brief_pack.SCRIPTS`** becomes `(RP.package_root() / "scripts").as_posix()` — same value as `HERE.as_posix()` (F8);
  the two card heads are built through `script_command(..., must_exist=False)` as above.
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
- `references/common-rules.md:112` (the role-section legend; origin row `| ${CLAUDE_PLUGIN_ROOT}, ${CLAUDE_SKILL_DIR},
  references/…, scripts/… | the **installed plugin**, never the project |`): the first cell becomes
  `` `references/…`, `scripts/…`, the script paths of your brief card (`python "<path>/scripts/<script>"`) `` (N3: only
  the card's SCRIPT paths are in the installed-plugin frame — a brief also names `<task root>`, `project:` doors and
  `work/...` files, which are project paths). `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_SKILL_DIR}` leave the ROLE section
  (sweep of the same artifact: the sibling host variable in the same cell). Line 134 (conductor section, roles: none) is
  NOT touched. Then `python -B scripts/contract_slices.py --write` regenerates the 10 slices.
- Ratchet (B1): the edited `## Tools` sections sit under `<!-- kind: process -->` (qa-runner :56; same structure in the other
  three) and every regenerated slice is part of its role's delivered load, so each affected role's process load FALLS;
  with slack 0 a fall is itself a red (`role_load.process_ratchet_problems`, "below its row X: lower to Y"). Part B lowers
  those `process_ratchet_tokens` rows in `references/role-load.json` in the same commit (AR-20).
- Detector: a join row in `test_ahead_cards.py` (F3). The Bash reader is `host_adapter.role_has_bash(role)`
  (`host_adapter.py:519`) over the role names of `agents/*.md` — chosen because it is the PRODUCT's own reader of the
  `tools:` line (axis 19, AR-13); `role_replay.WITH_BASH` (`scripts/tests/role_replay.py:49`) is a test helper built on
  `host_adapter.role_tools`, i.e. a second spelling of the same reader.

### 3.3 run_headless — Part C (rev 2, critic B3; coordinator direction)

- New pure function `child_env(base: dict) -> dict` in `experiments/measurers/run_headless.py`, composed on the package's
  one road for "the env of a `claude -p` child" (`infra_failure.child_env`, `infra_failure.py:133`, data
  `references/driver-infra.json` `child_env`; used by `driver_core.py:500-501`):
  1. `env = infra_failure.child_env(base, infra_failure.rules()[0], {})[0]` — strips what a `claude -p` child must not inherit
     (`CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH`, `CLAUDE_CODE_CHILD_SESSION`, `CLAUDE_CODE_MESSAGING_*` and the other data
     rows — the names behind "Not logged in" on TP1-13877; measured present in a forge desktop session's Bash, critic t-257);
  2. `env["CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS"] = "0"` (as today, :65);
  3. `QA_FACTORY_RUN_MODE` removed;
  4. `CLAUDE_PLUGIN_ROOT` removed.
  `main()` uses `child_env(dict(os.environ))`. `infra_failure` is imported through `paths.PACKAGE / "scripts"` on
  `sys.path`, the way other measurers reach package code; if no measurer does so today, the builder reports the import
  door it used in "needed beyond the manifest".
- Why both are REMOVED: this is the desktop road the run mode already assumes, and it is what the host is KNOWN to give —
  a forge desktop session (where run_headless is launched) measured `CLAUDE_PLUGIN_ROOT=[]` and `QA_FACTORY_RUN_MODE=[]`
  in its Bash (critic t-257 env measurement), so every past headless baseline ran with an empty root and comparability
  holds. `launch_card.desktop_story` (`launch_card.py:165-176`) returns False for ANY non-empty `QA_FACTORY_RUN_MODE`, so no
  value may be set; and removing `CLAUDE_PLUGIN_ROOT` means no stale copy (R6b) can reach the child (B-014 covered).
  `CLAUDE_PLUGIN_ROOT` is SET only after OH5-2e has measured that the desktop host gives it; then OH5-2e changes
  run_headless. Both deviations from B-166's wording are reported in §8.
- Any further host name to strip (`CLAUDECODE` and other `CLAUDE_CODE_*` names the critic measured) is a row in
  `driver-infra.json`, not code in run_headless (reported, not widened).

## 4. Builder parts (acceptance key 3)

Parts A, B, C have disjoint owns and no order between them; they can run in parallel. Each is under ~150 diff lines.
No part owns a file of the dispatch's in-flight list (hooklib.py, host_probe.py, factory_dashboard.py, config_view.py,
check_coverage.py, native_context.py, inject_context.py, stage_guard.py, controller.py); `hooklib.PLUGIN_ROOT`,
`stage_guard.py`, `inject_context.py` and `infra_failure.py` are only READ (import / scan).
**Overlaps with in-flight branches (N6; critic t-257 branch-overlap rerun on origin):**
- Part A shares `scripts/refusal_registry.py` (a REGISTRY entry, +15 lines) and `scripts/tests/fixtures/judgment-census.json`
  (+1 row) with `origin/conv/wave-3` (includes `wip/oh3-36`, t-232): Part A branches after wave-3 merges, or merges main and
  resolves the REGISTRY/census hunks itself (different regions expected).
- Part A shares `scripts/tests/test_runtime_paths.py` with `origin/wip/of4-17b` (2 lines, fix round 2): Part A merges after it.
- Part B shares `references/role-load.json` with `origin/conv/wave-3` and `origin/wip/hf84-p11` (the qa-automator row):
  Part B merges after them, or resolves that one row's conflict itself.
- No overlap found for `wip/of4-20-oh5-12`, `wip/of4-1-4`, SC2-43, `wip/hf84-p2`, the wave-2 fix (critic t-257 N6).
Later nodes waiting on Part A (`guard_pre_tool.py`): OH5-4, OH5-13 (batch row "Зависит от: OH5-2").

---

### Part A — the guard's doors through one survivor (~130 lines)

given: this spec §1, §2, §3.1, §5; C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md (whole); C:/QAFactory/forge-repo/plans/builder-rules.md; C:/QAFactory/forge-repo/docs/TESTING.md; C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/guard_pre_tool.py (:757-827, :872-879, :1070-1111, :1220-1310, :1609-1625); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/runtime_paths.py (:223-231); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/refusal_registry.py (:56-60, :812-940); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py (:62-72, :3671-3676, :4258-4262); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_refusal_registry.py; C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_runtime_paths.py
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/runtime_paths.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/guard_pre_tool.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/refusal_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_runtime_paths.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_refusal_registry.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json
non-goals: no change to what any refusal refuses or to its A24 key; no edit of hooklib.py, stage_guard.py, inject_context.py (in-flight; read only); no other module's literal (driver_*, stage_done, execution_request, story_step, source_exclusions, config_contract: node OH5-2d); no skill/phase/reference text (OH5-2e); no new test file; no edit of a quarantined test file; no edit of docs/SIBLING_MAP.md (axis queued to the full Lead, F7); no helper named `*_problems` for the new finding; judgment-census.json only if test_judgment_census.py demands a row for the new finding (then one row, class shape, owner data); overlaps of §4 resolved by merge order or by the builder in its own tree
handoff: builder report (`.claude/agents/builder.md` rule 7): the diff, the FR walk A-G, the AR lines of §1 (AR-15 line: `survivor added, axis queued to Lead (F7)`), the verbatim witness output, the list of guard sites with the function each now calls, the queued axis line, and "needed beyond the manifest"
edges: E1-E15 of §5 (spaces, backslashes, `$`/backtick/quote roots, missing script, root never from env, Codex = Claude text, non-ASCII, UNC, symlink, hot path, temporal commit order, in-flight scanned files, docstring false positive, concatenation miss, all spellings) and E3c (card head and door quote alike)
DoD: (1) `runtime_paths.script_command` / `script_path` exist with the behaviour of §3.1 (incl. `must_exist`), and ONE table in `test_runtime_paths.py` (the module's table layer; rows named by edge id: E1 spaces, E2 backslash root, E3a `$` root, E3b `'`+`$` root, E3c `must_exist=False` with the `<script>` placeholder on an E3a root gives the same quote character as `must_exist=True` on an existing script, E4 missing script, E7 non-ASCII, E8 UNC) passes `root=` explicitly and checks the exact returned text; (2) the 11 guard sites call the survivor — a Grep, case-insensitive, of `CLAUDE_PLUGIN_ROOT` over `scripts/guard_pre_tool.py` gives 0 hits, with the same Grep finding `hooks/hooks.json` as the positive control, both outputs pasted; (3) a built-text row in `test_refusal_registry.py`: at least `_window_refusal` (stub WF with `cases_of`) and the `plan_write_check` refusal of a JSON plan with rows (temp project, event with a Bash role) are built through the real guard functions, every `python "<p>"` / `python '<p>'` path in them is extracted, and each `<p>` exists and starts with `runtime_paths.package_root().as_posix()`; plus ONE pinned E4 rendering of `plan_write_check` (the survivor called with a `root=` whose `scripts/plan_row.py` is absent, e.g. by monkeypatching `RP.package_root` to a temp dir) showing the gap text followed by the kept argument tail; (4) `refusal_registry.findings()` reports a fake `stage_guard.py` (the existing `_fake_package` helper) holding `"${CLAUDE_PLUGIN_ROOT}/scripts/x.py"` (one variant row in `part_scanner`) and the live package has no finding (the existing `part_live_package` check stays green); (5) `brief_pack.SCRIPTS` equals `(runtime_paths.package_root() / "scripts").as_posix()` and both card heads (:3675, :4260) are built through `script_command('<script>', must_exist=False)`; verification run: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/runtime_paths.py scripts/guard_pre_tool.py scripts/refusal_registry.py scripts/brief_pack.py scripts/tests/test_runtime_paths.py scripts/tests/test_refusal_registry.py` and every test file it prints (quarantined files excluded; it prints `test_role_load.py` via brief_pack — run it), plus `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/refusal_registry.py --check` and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_judgment_census.py`; pasted verbatim
siblings: `story_step.py:276` and `handoff_check.py:2796` spell `python "{HERE.as_posix()}/handoff_check.py"` by hand — queued to OH5-2d (wire to the survivor); `source_exclusions._script` (:514) — OH5-2e; report any other hand-made absolute script spelling you notice, do not fix it
designer: C:/QAFactory/forge-repo/docs/tasks/specs/t-254-oh5-2-plugin-root-given.md

---

### Part B — role charters and slices name the card, not the variable (~70 lines)

given: this spec §1, §2, §3.2, §5; C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md (whole); C:/QAFactory/forge-repo/plans/builder-rules.md; C:/QAFactory/forge-repo/docs/TESTING.md; the four charters below; C:/QAFactory/forge-repo/ai-packages/qa-factory/references/common-rules.md (:103-140); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/brief_pack.py (TOOLING :256-304, TOOLING_MANUAL :330-345, card :4258-4267); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/host_adapter.py (:519-522 `role_has_bash`); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/role_load.py (:255-285 `process_ratchet_problems`); C:/QAFactory/forge-repo/ai-packages/qa-factory/references/role-load.json (`process_ratchet_tokens`); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_role_load.py (:507-546); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_ahead_cards.py; C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py (:216-228); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_brief_pack_roles.py (:270-303, K9 — READ ONLY, quarantined: the old form of the join)
owns:
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-runner.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-failure-analyst.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-doc-scribe.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/agents/qa-retro-analyst.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/common-rules.md
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/slices/ (only the `common-rules.md` files `contract_slices.py --write` regenerates)
C:/QAFactory/forge-repo/ai-packages/qa-factory/references/role-load.json
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_ahead_cards.py
C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py
non-goals: no brief_pack.py edit (the cards already carry the five scripts; Part A owns brief_pack.py); no new brief field; no skill/phase text and no common-rules.md conductor section (:131-140, OH5-2e); no edit of quarantined test files (test_brief_pack_roles.py, test_package_generation.py — F6); no edit of test-layers.json; no other charter wording; no raise of any role-load.json row; `ratchet_tokens` untouched unless test_role_load demands it
handoff: builder report (`.claude/agents/builder.md` rule 7): the diff, the FR walk A-G, the AR lines of §1 (AR-20: rows lowered, none raised — list role → old → new), the verbatim witness, and the list of quarantined checks that will now go red (expected: test_brief_pack_roles.py K9 :300, test_package_generation.py P4 :489, P5 :492, :494)
edges: E18-E23 of §5 (script not on card, role without Bash, join vacuity, slice regeneration diff, quarantined pins, slack-0 ratchet)
DoD: (1) the five charter lines read as §3.2 lists them; (2) `references/common-rules.md:112` reads as §3.2 (first cell: `` `references/…`, `scripts/…`, the script paths of your brief card (`python "<path>/scripts/<script>"`) ``) and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/contract_slices.py --write` regenerated the slices: the slice diff is that one legend line in each of the 10 files, nothing else; (3) one join row in `test_ahead_cards.py`: for every role name of `agents/*.md` for which `host_adapter.role_has_bash(role)` is True (the product's reader of the `tools:` line, axis 19 — never a regex on the role file, never the test helper `role_replay.WITH_BASH`), every `` `<name>.py ...` `` followed by `(on your card)` (or with `on your card` inside the parenthesis that follows it) in its charter is on that role's card (`brief_pack.TOOLING[role]` + `TOOLING_MANUAL[role]`); the join finds exactly the five names of §3.2 (vacuity guard); and no file in `agents/` or `references/slices/` contains `claude_plugin_root` in any case; (4) the key `'python "${CLAUDE_PLUGIN_ROOT}/scripts/manual_evidence.py" validate'` of `test_charters_s5_s9.py:223` is rewritten to the new runner phrase (TESTING.md «Когда тест покраснел» 1: an intended change rewrites the pin in the same node); (5) the `process_ratchet_tokens` rows of every role whose measured process load fell (expected: the 4 charter roles plus every role whose `common-rules.md` slice changed) are lowered to the value `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/role_load.py --all --json` prints; no row is raised; verification run: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for agents/qa-runner.md agents/qa-failure-analyst.md agents/qa-doc-scribe.md agents/qa-retro-analyst.md references/common-rules.md references/role-load.json scripts/tests/test_ahead_cards.py scripts/tests/test_charters_s5_s9.py` and every non-quarantined file it prints, plus `test_ahead_cards.py`, `python -m pytest ai-packages/qa-factory/scripts/tests/test_charters_s5_s9.py -q`, `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_role_load.py` (named explicitly: the witness-for of these paths does not print it) and `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/contract_slices.py --check`; pasted verbatim
siblings: other role-read literals (templates/requirements-register.md, handoffs/s0-setup-to-scout.yaml, stand-answers.json, driver brief lines) — OH5-2d; conductor texts — OH5-2e; report any charter that names a script with no card line
designer: C:/QAFactory/forge-repo/docs/tasks/specs/t-254-oh5-2-plugin-root-given.md

---

### Part C — run_headless gives its child the desktop road, through the package's env survivor (~30 lines)

given: this spec §3.3, §5 E16-E17; C:/QAFactory/forge-repo/experiments/measurers/run_headless.py (whole, 89 lines); C:/QAFactory/forge-repo/experiments/measurers/paths.py (`PACKAGE`); C:/QAFactory/forge-repo/experiments/measurers/test_measurers.py (:1509-1540 `rt_prepare_copy_and_run_headless`, :1605 `main`); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/infra_failure.py (:40-50 `rules`, :133-170 `child_env`, read only); C:/QAFactory/forge-repo/ai-packages/qa-factory/references/driver-infra.json (`child_env`, read only); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/launch_card.py (:165-176, read only); C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/driver_core.py (:490-501, read only — the driver's composition, the model)
owns:
C:/QAFactory/forge-repo/experiments/measurers/run_headless.py
C:/QAFactory/forge-repo/experiments/measurers/test_measurers.py
non-goals: no package file (driver-infra.json rows included — a missing strip name is reported, not added); no change to the claude command line, the tool list or the model; no Codex runner (none exists in experiments/measurers — §8); no QA_FACTORY_RUN_MODE value of any kind; no CLAUDE_PLUGIN_ROOT value (until OH5-2e measures the host)
handoff: builder report: the diff, the import door used for `infra_failure`, and the verbatim witness
edges: E16 parent env holds QA_FACTORY_RUN_MODE=driver, a stale CLAUDE_PLUGIN_ROOT and a host-auth variable; E17 PLUGIN path with spaces
DoD: (1) `run_headless.child_env(base)` exists as §3.3 (composed on `infra_failure.child_env(base, infra_failure.rules()[0], {})[0]`, ceiling `"0"`, `QA_FACTORY_RUN_MODE` and `CLAUDE_PLUGIN_ROOT` removed) and `main()` passes its result to `subprocess.run`; (2) one table in `test_measurers.py` (next to `rt_prepare_copy_and_run_headless`) with rows E16 (base `{"QA_FACTORY_RUN_MODE": "driver", "CLAUDE_PLUGIN_ROOT": "/other/copy", "CLAUDE_CODE_CHILD_SESSION": "1", "X": "1"}` → none of the first three, `X` kept, ceiling `"0"`, `base` unchanged) and E17 (PLUGIN `C:/my plugins/qa-factory` reaches the command as the one `--plugin-dir` argv element, verbatim; the env carries no root); verification run: `python -B C:/QAFactory/forge-repo/experiments/measurers/test_measurers.py` (if the file needs its own folder as cwd, the hygiene door `( cd C:/QAFactory/forge-repo/experiments/measurers && python -B test_measurers.py )`), pasted verbatim
siblings: `infra_failure.child_env` — the survivor this part composes on (axis 6: a measurer uses the package's road, never its own); `driver_core.py:500-501` composes the same survivor and then exports root and run mode `driver` by design (the driver IS the driver); no other launcher of `claude -p` in experiments/measurers (Grep `claude` there: run_headless.py and paths/report tools only)
designer: C:/QAFactory/forge-repo/docs/tasks/specs/t-254-oh5-2-plugin-root-given.md

---

### Residual nodes (named, not drafted here; F1 — carrier: batch-6, written by the coordinator)

Carrier (B2; coordinator direction): batch-5 is taken and frozen (PROJECT.md «Командная работа» п.2). Each residual node is
opened as a `findings/` file of `plans/piles/onboarding-hooks/`, a node row in
`plans/piles/onboarding-hooks/batch-6-ostatki-t-203-i-t-227.md` (status `ожидает`) and a «Содержание» row in the pile's
`README.md` (D-0044). These are written by the **coordinator's doc batch at Part A's acceptance**, not by any builder part of
this spec.

| Node | What | owns (expected) | Test |
|---|---|---|---|
| OH5-2d | role-read literals emitted by other code and data: `driver_dispatch.py` :3868/:3910/:3951, `driver_stage_s7.py` :700/:1040, `execution_request.py:2741`, `stage_done.py` :209/:651, `references/templates/requirements-register.md` :113/:180, `handoffs/s0-setup-to-scout.yaml:61`, `references/stand-answers.json` :113/:116; and wiring `story_step.py:276`, `handoff_check.py:2796` to `runtime_paths.script_command` | those files + their keep tests (`test_stage_cards.py`, `test_story_step_manual_block.py` pins) | extend Part B's join to "no role-read carrier holds the variable" over the carriers above; built-text rows for the driver lines |
| OH5-2e | conductor-read literals (251 hits on origin: skills, phases, judge.md, handoffs.md, config_contract, source_exclusions, story_step doors) and `${CLAUDE_SKILL_DIR}`; then run_headless sets `CLAUDE_PLUGIN_ROOT` if the measurement shows the host gives it. Overlap to declare when drafted: `source_exclusions.py:516` with `wip/of4-20-oh5-12` (N6) | after measurement only | first ONE experiment (CLAUDE.md hygiene 6a): in a desktop session, does the Claude host expand `${CLAUDE_PLUGIN_ROOT}` in skill text, and does the conductor's Bash see it? and the same on Codex. Then either keep the literal under the stated resolution rule (`common-rules.md:131-140`) or rewrite through `runtime_paths.py` entrypoints |

## 5. Edges, each with the invariant it protects (acceptance key 4)

| Id | Edge | Behaviour | Invariant protected |
|---|---|---|---|
| E1 | package root contains spaces (`C:/Program Files/qa factory`) | `python "<root>/scripts/x.py"`, double-quoted | the path is one shell word in bash and PowerShell; a pasted door runs the named file |
| E2 | Windows root with backslashes | `Path.as_posix()` → forward slashes | the guard spells the root exactly as the brief card does (one road, P31); never mixed separators |
| E3a | root holds `$`, a backtick or `"` (no `'`) | single quotes | a pasted door never expands into another path |
| E3b | root holds `'` and one of `$`/backtick/`"` | no command form; name + root as plain text with "quote this path for your shell" | same: no command that resolves elsewhere is ever printed |
| E3c | card head vs door on an E3 root | both built by `script_command` (card: `must_exist=False`) → same quote character / same plain-text form | the card and a door never disagree on how the root is quoted (P31, N4) |
| E4 | the named script is missing from the running copy (partial install, older copy) | `` `<name>` (missing from the plugin copy at <root>; the conductor runs qa-doctor ...) ``, followed by the site's argument tail; `_config_door` keeps omitting its shell line (it has the Grep door) | FR-59: a fabricated path is never printed; FR-57: the refusal still has a door |
| E5 | "root unknown" | cannot occur in the guard: the root is the copy of the running file (`package_root()`); the survivor never reads `CLAUDE_PLUGIN_ROOT` or any env | a parent's or the host's stale value (t-024 R6b) never decides the path; the door names the generation that enforces the rule (B-014) |
| E6 | Codex host vs Claude host | the same text on both; the guard is reached through `hooks/codex.json` or `hooks/hooks.json`, both untouched | AR-5: no host naming; Codex's compat variable is irrelevant to role text |
| E7 | non-ASCII root (`C:/Users/Анна/...`) | kept verbatim; only separators change | no transliteration; the path exists as printed |
| E8 | UNC root `\\srv\share\qa` | `//srv/share/qa`, as the card prints it today | the door and the card agree; this node adds no new UNC behaviour |
| E9 | symlink / junction install | `resolve()` gives the real path, which exists | the printed path exists |
| E10 | hot path | the survivor is called only while building a refusal (on the way to `block`) | a call that passes pays no stat or import (the guard's ORDER rule, `guard_pre_tool.py:839-841`) |
| E11 | TEMPORAL: the survivor and the registry finding do not exist before Part A | the finding, the 11 site rewrites and the survivor land in ONE commit | `test_refusal_registry.py` part_live_package is green at every commit (the finding would fire on the 11 old sites) |
| E12 | in-flight `stage_guard.py` / `inject_context.py` are scanned by the finding | they hold 0 hits today (census §2; critic t-257 rerun on origin: 0 each); if a branch adds one, its own witness names `<file>:<line>` | no refusal source of any copy ships the literal; Part A does not edit those files |
| E13 | a docstring mentions the variable | flagged (string constant) | allowed error direction: a false finding, never a missed literal |
| E14 | a token split by concatenation | not flagged — accepted, named miss | evasion is a review matter (critic), not this scanner's |
| E15 | `$CLAUDE_PLUGIN_ROOT`, `%CLAUDE_PLUGIN_ROOT%`, `$env:CLAUDE_PLUGIN_ROOT`, any case | all flagged (lowercase substring `claude_plugin_root`) | no spelling of the host variable reaches a role from a refusal source |
| E16 | run_headless parent env has `QA_FACTORY_RUN_MODE=driver`, another `CLAUDE_PLUGIN_ROOT`, and `CLAUDE_CODE_CHILD_SESSION` | all three removed (the last by `infra_failure.child_env`); `base` unchanged | a headless turn is the desktop road (`launch_card.desktop_story`) under the conditions the host is measured to give; no stale copy (R6b) and no host-auth variable (TP1-13877) reaches the child; one env road (P31) |
| E17 | PLUGIN path with spaces | one argv element of `--plugin-dir`, verbatim; the env carries no root | argv is not shell text; the root never travels by env until OH5-2e |
| E18 | a charter names with `(on your card)` a script that is not on its card | the join fails naming role and script | a script a role is told to run is reachable by the absolute path its brief gives (FR-15) |
| E19 | a role without Bash (`host_adapter.role_has_bash` False) | outside the join (its card is TOOLING_NO_SHELL); still in the "no variable" scan | a role is not sent to a command it cannot run (FR-2) |
| E20 | the marker spelling drifts and the join finds nothing | the join must find exactly the five names of §3.2 | the join is never vacuous |
| E21 | slice regeneration | diff limited to the legend line in 10 slices; `contract_slices.py --check` green | a slice is never hand-edited; source and slices agree |
| E22 | quarantined pins on the old literal (`test_brief_pack_roles.py` K9 :296-303; `test_package_generation.py` P4 :489-490, P5 :492-495) | not touched; listed in the handoff (F6) | the builder never edits a quarantine file (builder-rules 7b); the red is judged by quarantine-watch as a pin |
| E23 | a shrink below a slack-0 process ratchet | the `process_ratchet_tokens` row is lowered in the same commit to the measured value; no row raised | AR-20: ratchets only shrink, and a shrink is recorded, never left as a red for the canon |

Conflicting requirement pairs named: (a) "run_headless exports what the host would give" vs B-166's "export
`CLAUDE_PLUGIN_ROOT` and `QA_FACTORY_RUN_MODE`" — resolved by E16/F5 (both removed: the host is measured to give neither);
(b) TESTING.md "rewrite a pin in the same node" vs builder-rules 7b "never edit quarantine" — resolved by F6 (keep files
rewritten, quarantine listed); (c) AR-15 "axis in the same commit" vs "SIBLING_MAP is the Lead's" — F7 (queued, the
commit's architecture line says so); (d) "a shrink of role text" vs "ratchet slack 0" — E23 (rows lowered in the same commit).

## 6. Forks (acceptance key 5) — each with a recommendation the builder can run on

- **F1 — scope against one road (designer rule 6, P31).** The node covers agents, guard, run_headless (+ slices, F-sweep).
  The census finds 13 more role-read literals (OH5-2d) and 251 conductor-read ones (OH5-2e). Options: (a) this node only,
  with OH5-2d and OH5-2e each opened as a `findings/` file of onboarding-hooks, a node row in
  `batch-6-ostatki-t-203-i-t-227.md` (status ожидает) and a «Содержание» row in the pile README, in the same move as
  Part A's acceptance (D-0044; batch-5 is taken and frozen); (b) widen this node to OH5-2d (+~13 sites, +2 pinned keep
  tests; Part D ~100 lines; touches `stage_done.py`, `story_step.py`, driver modules — not in-flight, but
  `story_step.py`/`driver_*` are hot files of other piles); (c) everything incl. conductor text (~250 edits, unmeasured
  host behaviour). **Recommendation: (a)** — a slice is no exclusion when the rest is a named node with owns and a test and
  a legal carrier; OH5-2e must MEASURE first (hygiene 6a): the conductor has a documented resolution road and nobody has
  measured whether the Claude host expands the variable in skill text. Cost of covering OH5-2d now: one more builder part,
  ~100 lines.
- **F2 — detector for refusal sources.** (a) a finding in `refusal_registry.findings()` (A24, the one scanner of refusal
  sources, AR-29 carrier) + built-text rows; (b) only built-text rows (cannot see a door nobody builds in the test); (c) a
  source grep test (a "source pin", forbidden by TESTING.md). **Recommendation: (a).**
- **F3 — charter spelling and the join's home.** (a) marker `(on your card)` and the join as a row of keep
  `test_ahead_cards.py` (data_join, "every card names its scripts"); (b) the join keyed on every backticked existing
  `scripts/*.py` name in a Bash charter (no marker; may over-match scripts a charter names for context); (c) a new audit
  check A-nn in `audit_factory.py`. **Recommendation: (a)** — K9's intent moves from a quarantined file into a keep file.
- **F4 — the door when the script is missing.** (a) name the gap and qa-doctor (§3.1); (b) omit the door line silently.
  **Recommendation: (a)** — FR-59 names what could not be established; (b) leaves some refusals (window claim) without a door.
- **F5 — run_headless child env (rev 2).** (a) remove `QA_FACTORY_RUN_MODE`, set `CLAUDE_PLUGIN_ROOT` to the `--plugin-dir`
  copy (rev 1 — rejected by critic t-257 B3: unmeasured premise, changes the baseline, hand-written second env road);
  (b) set `QA_FACTORY_RUN_MODE=desktop` (any non-empty value makes `desktop_story` False — wrong); (c) export only the root
  and inherit the run mode; **(d) compose on `infra_failure.child_env` (strip what it strips), set the ceiling, remove both
  `QA_FACTORY_RUN_MODE` and `CLAUDE_PLUGIN_ROOT`; set `CLAUDE_PLUGIN_ROOT` only after OH5-2e has measured that the desktop
  host gives it (then OH5-2e changes run_headless).** **Recommendation and coordinator direction: (d).** Basis: a forge
  desktop session's Bash measured both variables empty (critic t-257), so (d) is what the host is known to give and keeps
  past headless baselines comparable; `infra_failure.child_env` is the package's one road for a `claude -p` child (P31,
  AR-15). Deviation from B-166's wording: §8.
- **F6 — quarantined pins go red.** `test_brief_pack_roles.py` K9 (:300 expects `["bug_records.py","bug_snapshot.py"]` found
  through the literal) and `test_package_generation.py` P4/P5 (:489-495). (a) leave them; the handoff lists them; the
  quarantine-watch judge classes them as pins of an intended change (TESTING.md «Когда тест покраснел» 1-2), and their join
  intent now lives in keep `test_ahead_cards.py`; (b) the Lead authorises the builder to edit those two quarantined files.
  **Recommendation: (a).** The Lead tells the owner the expected quarantine reds in the same turn as acceptance.
- **F7 — the new axis (AR-15).** `runtime_paths.script_command` is a new survivor; AR-15 wants its axis in the same commit.
  (a) the Lead commits axis 37 (§7) together with Part A's merge; (b) queue the axis. **Recommendation: (a).**
- **F8 — `brief_pack.SCRIPTS` on the survivor.** (a) one line in Part A (proves card and door share one spelling) — rev 2:
  plus the two card heads through `script_command(..., must_exist=False)` (N4); (b) leave for OH5-2d.
  **Recommendation: (a).**

Coordinator decision (13.11 03:05, по рекомендации, до слова владельца; restated for rev 2): F1 (a) — the residual nodes
OH5-2d/OH5-2e go as `findings/` files + rows in `batch-6-ostatki-t-203-i-t-227.md` + README «Содержание» rows, written by
the coordinator's doc batch at Part A's acceptance (B2); F2 (a), F3 (a), F4 (a), F6 (a), F8 (a, with N4's card heads);
F5 changed from (a) to (d) on critic t-257 B3 (coordinator direction: compose on `infra_failure.child_env`, set the ceiling,
remove `QA_FACTORY_RUN_MODE` and `CLAUDE_PLUGIN_ROOT` until OH5-2e measures the host). F7: the axis is a mechanism, so the
full Lead commits it (the coordinator is in a degraded window); queued to Lead. The number 37 is also proposed by spec
t-231 part C, so the Lead assigns both numbers. Part A merges with the axis line queued, its `architecture:` line reads
`AR-15 -- survivor added, axis queued to Lead (F7)`, and the builder's handoff names the queued axis.

Small technical choices closed by the designer (no design weight): the survivor lives in `runtime_paths.py` (FR-37's check
names it; `package_root()` is there); helper names `script_command` / `script_path`; the keyword-only `must_exist`
parameter (N4, one road for card and door); lazy import in the guard as at :554; quoting rule E3; argument tails kept after
the E4/E3b text (N5); `test-layers.json` not edited (DoD names the test files explicitly); the survivor's case table in
`test_runtime_paths.py` (N1, the module's table layer); the Bash reader `host_adapter.role_has_bash` (N2); the legend line
also drops `${CLAUDE_SKILL_DIR}` (same cell, same class); the marker text `(on your card)`.

## 7. Draft axis for docs/SIBLING_MAP.md (the full Lead writes it; F7)

`## Axis 37 — Where the package root is resolved at runtime: one survivor runtime_paths.script_command <-> the role-read texts that name a script <-> the brief card <-> the conductor's rule (OH5-2, t-254; B-142, B-166)`

Why a new axis: axis 3 pairs the package with its release copy and the installed plugin (what is SHIPPED where), and
axis 8 is where the STORY is on disk (B-166's "→ t-304 axis 8" pointer); neither covers which copy's path a running text
names to a role, so the package root at runtime has no host axis.

| Component | Path |
|---|---|
| The survivor | `scripts/runtime_paths.py` `package_root()`, `script_path()`, `script_command(name, root=None, *, must_exist=True)` — the copy that runs, posix spelling, quoting rule; never an env var |
| Callers | `guard_pre_tool.py` (11 door sites, `_config_door` via `script_path`), `brief_pack.SCRIPTS` and the two card heads (`must_exist=False`) |
| Known roads off it (queued) | OH5-2d: `driver_dispatch.py`, `driver_stage_s7.py`, `execution_request.py`, `stage_done.py`, `story_step.py:276`, `handoff_check.py:2796`, `references/templates/requirements-register.md`, `handoffs/s0-setup-to-scout.yaml`, `references/stand-answers.json`; OH5-2e: conductor texts (skills, phases, `judge.md`, `handoffs.md`, `source_exclusions._script`, `config_contract.py`) under `common-rules.md` "Resolving the plugin root"; run_headless's root (removed until OH5-2e measures) |
| Legitimate literals | `hooks/hooks.json`, `hooks/codex.json` (host expands); `delivery_verdict.py` portable regression spelling (P24); detectors `regression_scope.py`, `human-text.json` `plugin_path`; `driver_core.py` export; `install_smoke.py` expansion |
| The symmetry | a text a role reads names a plugin script through the survivor or the brief card; a new door with a script calls `script_command` |
| The detector | `refusal_registry.findings()` (refusal sources), `test_ahead_cards.py` join row (charters, slices), the case-insensitive grep `claude_plugin_root` over `agents/` and `references/slices/` finds nothing (positive control: `hooks/hooks.json`) |

## 8. Reported, not widened (rule 3)

- **Freshness:** this designer has no shell tool, so `git -C C:/QAFactory/forge-repo show refs/remotes/origin/main:<path>`
  was NOT run in either revision. Rev 1 read the LOCAL checkout. Rev 2 takes every origin fact from the critic's quoted
  lines in `docs/tasks/specs/reviews/t-257-oh5-2-plan-review.md` (base `1fe6fde`, `git archive` extract): node row OH5-2 at
  batch-5 :31, B-142/B-166 texts, the 11 guard lines, charter/slice/card lines, census 420, branch overlaps, env
  measurement. Locally re-read in rev 2: `host_adapter.py:519-522`, `infra_failure.py:40-45, :133-139`,
  `tests/role_replay.py:40-49`.
- Node row line numbers drifted: `qa-runner:60` is now :61; B-142's "13 in 7 files" is now 5 in 4 files.
- **Deviations from B-166's wording** ("не экспортирует ни `CLAUDE_PLUGIN_ROOT`, ни `QA_FACTORY_RUN_MODE`", confirmed on
  origin by critic t-257): (1) `QA_FACTORY_RUN_MODE` is REMOVED, not exported — any value breaks desktop detection
  (`launch_card.py:169`); (2) `CLAUDE_PLUGIN_ROOT` is REMOVED, not exported — the desktop host is measured to give it empty
  (critic t-257 env measurement); exporting it would change the conditions of every past headless baseline and rest on an
  unmeasured premise (OH5-2e measures it, then sets it if the host gives it). F5 (d).
- The node row lists `scripts/brief_pack.py` "if the brief carries the root": it already does (`brief_pack.py:72`, `:4260`);
  no new brief field is needed.
- The role-read literals the node row does not name (slices: included in Part B; OH5-2d's 13 sites) — F1.
- `run_headless` also passes `CLAUDECODE` and other desktop-host `CLAUDE_CODE_*` names (critic measurement); the
  data-listed ones are stripped by `infra_failure.child_env`; a further name is a `driver-infra.json` row, not code.
- No Codex headless measurer exists: Grep `codex` (case-insensitive) over `experiments/measurers/` found nothing; positive
  control, same call with `CLAUDE`, found 11 files including `run_headless.py`.

## 9. Reading trail

- `plans/piles/onboarding-hooks/batch-5-nerazlozhennye-nakhodki.md` (whole, local); `findings/B-142-...md`, `findings/B-166-...md` (whole, local); origin versions via critic t-257 Key 1.
- Grep `CLAUDE_PLUGIN_ROOT` -i over `ai-packages/qa-factory/` (count; content over `agents/`, `scripts/*.py`, `skills/*/SKILL.md`, `references/`, `design/`, `handoffs/s0-setup-to-scout.yaml`); Grep `\$\{CLAUDE_` over the package minus tests.
- `scripts/guard_pre_tool.py` :1-60, :755-884, :1070-1119, :1220-1310, :1600-1625; Grep of `PLUGIN_ROOT`, `runtime_paths`, `_has_bash`, `role_ways`.
- `scripts/hooklib.py:30` (via Grep `^PLUGIN_ROOT =`); `scripts/runtime_paths.py` :1-46, :220-234, def list.
- `scripts/brief_pack.py` :55-94, :195-294, :1110-1129, :3655-3684, :4245-4274, Grep `SCRIPTS`, `retro_numbers`.
- `scripts/source_exclusions.py:505-524`; `scripts/execution_request.py:2730-2745`; `scripts/driver_stage_s7.py:692-703`; `scripts/driver_dispatch.py:3860-3874`; `scripts/stage_done.py:203-211`; `scripts/launch_card.py:155-179`; Grep `QA_FACTORY_RUN_MODE`, `RUN_MODE_ENV`.
- `scripts/refusal_registry.py` def list; `scripts/audit_factory.py` def list; `scripts/contract_slices.py` Grep `slices`.
- Rev 2: `scripts/host_adapter.py:519-525`; `scripts/infra_failure.py:40-45, :133-139`; `scripts/tests/role_replay.py:40-54`; `docs/tasks/specs/reviews/t-257-oh5-2-plan-review.md` (whole).
- `references/common-rules.md:100-144`; `references/human-text.json:40-80`.
- Tests: `test_brief_pack_roles.py:260-319`; `test_package_generation.py:425-498`; `test_charters_s5_s9.py:210-235`; `test_guard_command_text.py:1-70`; `test_ahead_cards.py:1-60`; `test_refusal_registry.py:1-90`; `scenario_walk.py:887-931`; `test-layers.json` :1-84, :495-524, :2080-2190, :4250-4265, :9180-9195 and Grep of keep/quarantine rows; `fixtures/judgment-census.json:1-40` and Grep of rows.
- `experiments/measurers/run_headless.py` (whole); `test_measurers.py` def list; Grep `codex` / `CLAUDE` over `experiments/measurers/`.
- `design/factory-rules.md` FR-15 :205, FR-59 :289, FR-37 :357; `design/architecture.md` AR-5..AR-9 :76-111, AR-29/AR-13..AR-16 :134-188.
- `docs/SIBLING_MAP.md` axis headings, axis 13 :311-328, axis 34 :582-593, upkeep :620-636; `docs/TESTING.md:75-144`; `plans/builder-rules.md` 7/7a/7b.

## 10. Change log (rev 2, after critic on plan t-257)

| Item | What changed | Sections |
|---|---|---|
| Census | 417 → 420 on origin (`p4-generate.md` +3, conductor-read); conductor class 248 → 251; no Part-touched class changes | §2 (header text, conductor row, sum), §4 residual OH5-2e, §6 F1 |
| B1 | Part B owns `references/role-load.json`; DoD (5) lowers process ratchet rows, no raise; `test_role_load.py` named in the verification run; edge E23; AR-20 row rewritten; role-load overlap named | §1 AR-20 + checks table, §3.2 ratchet bullet, §4 overlaps, Part B, §5 E23 + pair (d) |
| B2 | residual nodes carried by `findings/` files + batch-6 rows + README «Содержание» rows, written by the coordinator's doc batch at Part A acceptance (batch-5 frozen) | §4 residual heading/paragraph, §6 F1, coordinator decision |
| B3 | Part C composes `infra_failure.child_env(...)`, sets the ceiling, removes `QA_FACTORY_RUN_MODE` and `CLAUDE_PLUGIN_ROOT`; E16 row with `CLAUDE_CODE_CHILD_SESSION`; given/siblings name `infra_failure.py`, `driver-infra.json`; F5 restated as (d); B-166 deviation in §8 | §1 intent + AR-13/AR-15, §3.3, Part C, §5 E16/E17 + pair (a), §6 F5 + coordinator decision, §7 roads, §8 |
| N1 | survivor case table moved to `test_runtime_paths.py`; Part A owns it; merge after `wip/of4-17b` | Part A owns/given/DoD (1), §4 overlaps |
| N2 | the Bash reader is `host_adapter.role_has_bash` (product reader, axis 19), not the test helper `role_replay.WITH_BASH`; one-line reason | §3.2 detector bullet, Part B given/DoD (3), §5 E19 |
| N3 | legend first cell: "the script paths of your brief card (`python "<path>/scripts/<script>"`)" | §3.2, Part B DoD (2) |
| N4 | `script_command(..., *, must_exist=True)`; the two card heads built with `must_exist=False`; E3 not broken (placeholder never hits E4, quoting depends on the root only); edge E3c | §1 AR-15, §3.1, Part A DoD (1)/(5), §5 E3c, §6 F8 + small choices, §7 |
| N5 | argument tails kept after the E4/E3b text, intended; DoD (3) pins one E4 rendering of `plan_write_check` | §3.1, Part A DoD (3), §5 E4 |
| N6 | overlaps declared: refusal_registry.py + judgment-census.json vs conv/wave-3 (oh3-36), role-load.json vs conv/wave-3 + hf84-p11, test_runtime_paths.py vs of4-17b; OH5-2e names source_exclusions.py vs of4-20-oh5-12 | §4 overlaps, §4 residual OH5-2e |
| Key 3 extras | Part A commit line `AR-15 -- survivor added, axis queued to Lead (F7)`; `_config_door` gate through `RP.script_path`; no `*_problems` helper name (census unit) | §1, §3.1 sites, Part A non-goals/handoff |
| §7 | one line on why axes 3 and 8 do not host the package root | §7 |
| Freshness | origin facts taken from the critic's quoted lines (no shell); stated | header, §8 |
