# t-167 — OH3-9: the factory settles its own files by class, never asks (DRAFT for Lead acceptance)

Node: `onboarding-forge/1/OH3-9` (`plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:30`).
Finding: `plans/piles/onboarding-forge/findings/20261022-onbording-sprashivaet-pro-sluzhebnye-fajly-fabriki.md`, items 1-4.
Owner's word 22.10.2026 (verbatim, finding :5-6): «Фабрика не должна спрашивать о её служебных файлах. Если они не нужны,
то удаляются, если нужны как доказательства для дальнейшей работы со стори — сохранять».
Status: DRAFT by designer. Forks F-1..F-5 closed by the Lead 12.11.2026 at the designer's recommendation (F-1 per-row `rebuilt_by`
basis; F-2 a-e as recommended; F-3 A — the owner's word 22.10 "не нужны — удаляются"; F-4 A; F-5 A). C2's meaning changes, so a critic
on plan (t-170) runs before any builder.
This spec changes the MEANING of a gate (the C2 "changed since the summary" refusal) — PROJECT.md «Как принимается изменение
пакета» п. 6 applies: critic on plan before the builder.

## Dispatch header (R11-f; to be copied into the builder dispatch once the forks are closed)

given: C:\QAFactory\forge-repo\docs\tasks\specs\t-167-oh3-9-factory-files-by-class.md (this spec, carries the enumeration), C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md, C:\QAFactory\forge-repo\plans\builder-rules.md, C:\QAFactory\forge-repo\ai-packages\qa-factory\design\architecture.md, C:\QAFactory\forge-repo\docs\TESTING.md, C:\QAFactory\forge-repo\plans\piles\onboarding-forge\findings\20261022-onbording-sprashivaet-pro-sluzhebnye-fajly-fabriki.md, C:\QAFactory\forge-repo\ai-packages\qa-factory\references\install-paths.json, C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\install_paths.py, C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\onboard_apply.py, C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_install_paths.py, C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_install_retire.py, C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\evals\evals.json, C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p4-generate.md, C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\SKILL.md, C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\install-paths.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\install_paths.py (functions: `_shape_errors`, new `_basis_errors`, `validate_table`; nothing else)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\onboard_apply.py (module docstring lines 10-17; `_changed_since_summary`; new `summary_drift`; `_retire`; `apply`; `main` lines 1880-1885 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_install_paths.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_install_retire.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_reinstall_equals_fresh.py (only the REGEN_UNBUILT list at :68-70, and only if F-2 reclasses a row named there)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (only rows `test_judgment_census.py` demands for the units below)
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json (two rows, §4.5)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\evals\evals.json (one eval appended, id 16)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p4-generate.md (§0, the `final` bullet, lines 27-33 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\SKILL.md (## Digest, lines 130-138 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\oh3-9-factory-files-by-class.md (new fragment)
C:\QAFactory\forge-repo\docs\SIBLING_MAP.md (row at :76, one clause appended)
non-goals: OF1-2 (summary seal: `plan`, `config_contract.proposal_hash`, `config_contract.fill_proposal`, `_proposal_for`, the `check_input` path, `_manifest_entries`, p3-summary-gate.md — none touched here); any change to `scan_tree`, `classify`, `find_locks`, `_plan_moves`; any new test file; the doctor; the gate A rehearsal code (`gate_preflight.py`, `onboarding_probe.py`, `report_adapt.py`) — they keep writing and reading the file as today; the AR-22 gap of `benefit-inputs.json` beyond its class (queued, §3.3).
handoff: builder report per `.claude/agents/builder.md` rule 7 (FR walk A-G, AR lines, witness verbatim, analogs noticed), branch `pile/onboarding-forge/batch-1`, commit hash.
edges: §6 of this spec (each with its invariant); summary: home membership battery, temporal (older sealed listing; old manifest; table before/after), positional (where the drift partition sits), empty `after_summary`, no cap on rows.
DoD: §5.4 — `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/install-paths.json scripts/install_paths.py scripts/onboard_apply.py skills/qa-onboarding/evals/evals.json skills/qa-onboarding/phases/p4-generate.md skills/qa-onboarding/SKILL.md design/role-rules.json`, then each printed keep file that is not in `quarantine` and not slow, then `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
siblings: SIBLING_MAP:76 (hook_written narrowing: an older sealed listing is re-asked of the current table — the new "carried now" branch is its twin); axis 34 (one road: home membership read from the table's `home`, never a literal or a language); the regenerated rows of `install-paths.json` :87-119 (walked in §3.3).
designer: C:\QAFactory\forge-repo\docs\tasks\specs\t-167-oh3-9-factory-files-by-class.md (once accepted)

## 1. What this touches (designer rule 1; CLAUDE.md rule 10, P27)

### 1.1 AR-n touched, with the change check each demands (goes into the DoD)

| AR | how touched | change check written into the DoD |
|---|---|---|
| AR-1 | the class of a path and the new `rebuilt_by` basis are data rows; the home prefix is the table's `home` (`install_paths.home_of`, install_paths.py:285-286), never a literal in `summary_drift` | grep `summary_drift` for the literal `"qa-factory"`: none (the home comes from `I.home_of(table)`) |
| AR-13 | `I.classify` stays the one reader of a path's class; `summary_drift` and `_retire` call it and parse nothing themselves | no second matcher of globs in onboard_apply.py (grep `_match(` / `fnmatch` in onboard_apply.py: none added) |
| AR-14 | `install-paths.json` stays the one table; `_retire` stays the one writer of the removal record (onboard_apply.py:1382-1395); the rehearsal file keeps its writers (`gate_preflight.py:3319`, `onboarding_probe.py:379`) | the after-summary deletions go through `_retire` (same record, same `tracking`), never a second unlink site |
| AR-15 | one survivor for "did the project drift since the summary": `summary_drift`, called by BOTH `main` (today onboard_apply.py:1881-1884) and `apply` (today :1441-1444) | both call sites call `summary_drift`; `_changed_since_summary` becomes a thin wrapper over it or is removed with its callers |
| AR-21 | the apply's `after_summary[]` rows travel whole to the role's digest (SKILL.md ## Digest); the role relays every row | the Digest bullet names `after_summary`; eval 16 asserts one line per settled file |
| AR-22 | new field `rebuilt_by` (producer: table rows; reader: `validate_table`); new apply key `after_summary` (producer: `apply`; readers: p4 §0, SKILL Digest); `benefit-inputs.json` has a reader and no producer (§3.3) | grep `rebuilt_by` and `after_summary` case-insensitively over `scripts/ agents/ skills/ references/ handoffs/` with a positive control (`retire_mode` found the same way); every hit is a reader or the producer |
| AR-25 | every outcome has a way out: a deleted file -> the removal record; a kept file -> the next install's summary lists it; the reclassed carried file -> gate A re-rehearses when its `function_sha` no longer matches (CHANGELOG.md:5487) | stated per `after_summary` result in §4.3; no new recorded state, so no `design/state-exits.md` row (reason: `after_summary` is a report of what one apply did, not a state anything resumes from) |
| AR-28 | a path that does not normalise, or whose home membership cannot be established, is treated as OUTSIDE the home: the apply refuses (declared safe default), never deletes | variant rows of §5.2 table B |
| AR-29 | one check added, two altered (below) | owner + census class named per check (§1.2); run `test_judgment_census.py`; a raised count named in the verdict (AR-20) |
| AR-9 | the outside-home refusal keeps `changed_message` (onboard_apply.py:1297-1299) with its door "make the summary again" | text unchanged; C2 test line "names no script and no plugin path" (test_install_retire.py:448) kept as a row |

AR-17 / AR-16: not touched by new code — this node REMOVES a question; no question site is added (no `person-owned` row needed).
AR-19: none — the onboarding apply has no stage twin (the headless entry is the same `main`).

### 1.2 Checks added or altered — owner and census class (AR-29)

| check | new/altered | owner it serves | census class | error direction |
|---|---|---|---|---|
| `install_paths._basis_errors` (via `validate_table`): every `regenerated` row carries a basis | new | data (presence of a basis + a join: the named script exists and contains the row's key). The claim behind `rebuilt_by` ("its absence costs no run, no money, no question") is JUDGMENT of the table's author, accepted by the critic (tier above) | `xref` | may err toward REFUSING (a false refusal costs the author one field); must never accept a regenerated row with no basis. Known false pass: a `rebuilt_by` naming a script that only READS the key passes the text join — judged by the critic, not by code |
| `onboard_apply.summary_drift` (was `_changed_since_summary`) | altered | data (path prefix from the table, class from `classify`, bytes vs the listed sha256). Intent: the owner's word 22.10.2026 decides which files the factory settles alone | `xref` | may err only toward REFUSE (a path outside the home) or KEEP (inside); never toward deleting a path outside the home, a carried path, a link or a folder |
| `_retire` branch "carried by the current table -> kept" | new branch of an existing unit | data | `shape` | only subtracts from a retirement; may err only toward keeping |

## 2. Item 1 — the class of `reporter-rehearsals.json`

Facts (read):
- The row today: `{"glob": "qa-factory/state/reporter-rehearsals.json", "class": "regenerated", "machine_local": true, "reader": "gate_preflight.py"}` — install-paths.json:112 (the finding's ":103" is stale).
- Readers: `gate_preflight.py:865` (`REPORTER_REHEARSALS_FILE`), path built at `gate_preflight.py:3319`; `report_adapt.py:41` (`REHEARSALS_REL`), read at :123-131; writer at onboarding: `onboarding_probe.py:379`. `onboarding_probe.py:17` names it "which gate A reads".
- Because the row is `regenerated` and no `regenerate_step` output (install-paths.json:25-30), `plan` -> `scan_tree(..., retire_unbuilt=True)` (onboard_apply.py:928) lists it for DELETE (install_paths.py:1117-1124) — and the test pins that today: `REGENERATED_UNBUILT` (test_install_paths.py:466) and the Q7 row check (test_install_paths.py:559-562).
- The live run of 0.11.0 on 12.11 repeated the defect ("третье «да» — на удаление собственного reporter-rehearsals.json", batch file :74).

Answer: **`carried` + `machine_local: true` is legal in `state/`; no new class is needed.** `_layout_errors` refuses only a carried row that is NOT machine-local inside an untracked folder (install_paths.py:666-673); a machine-local row is refused only inside a TRACKED folder (:674-679). Twenty carried machine-local rows already live in `state/` (install-paths.json:65-85, e.g. `judgments.jsonl` :81, `dispatch-denials.jsonl` :83), and test F7 asserts exactly this shape (test_install_paths.py:432-433).

Change: install-paths.json:112 becomes
`{"glob": "qa-factory/state/reporter-rehearsals.json", "class": "carried", "machine_local": true, "reader": "gate_preflight.py", "note": "the proof that a profile's test command writes a readable report, per project and command (gate A reads it before rehearsing again): evidence for later story work, kept in place, never retired (owner, 22.10.2026)"}`
and MOVES up into the carried block (after :85), so the regenerated block holds only regenerated rows (readability; precedence does not depend on order between classes, install_paths.py:450).

Consequences named for the builder:
- A carried row never carries `retire_mode` (install_paths.py:562-563) — none is added.
- The manifest: a carried machine-local row is not added by `_manifest_entries` (onboard_apply.py:517-520 add only carried non-local and regenerated local rows). An OLD manifest that names it as `regenerated` machine-local is carried forward with its old class label (onboard_apply.py:521-528) — harmless: machine-local manifest entries never retire (install_paths.py:1166-1168) and classify's precedence wins (closed small choice S-3; `_manifest_entries` is OF1-2's territory and is not touched).
- The description at install-paths.json:3 gets one sentence on `carried`: "carried also covers machine-local evidence a later story or gate reads, whose absence would cost a run, money or a question (owner, 22.10.2026)".

## 3. Item 2 — the class rule, not the instance

### 3.1 The rule

**Every `regenerated` row states its BASIS, and `validate_table` refuses one that does not** (new error code `regenerated_without_basis`). A basis is exactly one of (data, read from the row; the list is the code's closed enumeration of the table's own fields, not of paths):

1. the glob covers an output of a `regenerate_step` (the install itself rebuilds it): `any(_match(o.split("/"), glob.split("/"), False) for o in _step_outputs(table))` (helper at install_paths.py:519-525);
2. `hook_written: true` (a real bool; install_paths.py:571-585 rules unchanged);
3. a valid `lock_kind` (install_paths.py:566-570);
4. a valid `discard_when` (install_paths.py:615-618);
5. NEW field `rebuilt_by: "<script name>"` — a file name under `scripts/` (no slash) that EXISTS and CONTAINS the row's key (`_key_of`, install_paths.py:468-477), case-folded. Its declared meaning (written into the description at install-paths.json:3): "this script writes the file again by itself when it is absent, and its absence costs no test run, no money and no question, and no check reads less for want of it". A row whose honest answer is otherwise is `carried`.

Shape rules for `rebuilt_by` (in `_shape_errors`): must be a non-empty string without `/`, `\\`, `..`; `none` is refused (a file nothing rebuilds is not regenerated); allowed only on a `regenerated` row (on carried / discarded / not_ours: `shape` error).

Why this form and not the brief's literal one: fork F-1.

### 3.2 Error direction and adversarial inputs (designer rule 1: `validate_table` gains a gate role)

`validate_table` is already a gate (the shipped table must validate: test_install_paths.py:51). The new branch may err toward refusing only. Adversarial rows that must stay REFUSED (each a variant row of §5.2 table A):
- a regenerated row with no basis at all (the instance before the fix: row :112 as it stands);
- `rebuilt_by` naming a script absent from `scripts/`;
- `rebuilt_by` naming an existing script that does not contain the key;
- `rebuilt_by: "none"`, `""`, `7`, `"../x.py"`, `"scripts/x.py"`;
- `rebuilt_by` on a carried row;
- `hook_written: "yes"` as the ONLY basis (not a real bool -> no basis; the existing shape error also fires);
- an unknown `lock_kind` as the only basis (shape + no basis).
Each of the five bases alone must be ACCEPTED (one parameterised row with five ids).

### 3.3 The walk of every regenerated row (install-paths.json:87-119, plus :88 outside state/)

Verdict per row; "basis" = which of §3.1 1-5 the row will carry after this node.

| line | glob | reader | basis / evidence | verdict |
|---|---|---|---|---|
| 87 | state/readiness.json | readiness.py | 1: regenerate_step output (:26) | keep |
| 88 | install-manifest.json | install_paths.py | written by the install itself (`write_manifest`, install_paths.py:901; in `written`, onboard_apply.py:926) | keep, `rebuilt_by: install_paths.py` (contains `install-manifest`, :51) |
| 89 | state/factory-dashboard.html | factory_dashboard.py | 1 (:27) | keep |
| 90, 91 | state/dashboard-dirty.json, dashboard-refresh.json | dashboard_refresh.py | 2 | keep |
| 92 | state/host-probe.json | host_probe.py | "THE one writer" host_probe.py:92-96; absent -> `is_probe_child` is False (host_probe.py:585-591, the safe side); rebuilt by the doctor's next probe, not by story work | keep, `rebuilt_by: host_probe.py` — judgment flagged for the critic (F-2 c) |
| 93 | state/metrics*.json | metrics_projection.py | 1: covers `metrics.json` (:27); the two history files under the glob are carried (:78-79, precedence) | keep |
| 94 | state/stand-*.json | stand_lease.py | a lease registry (`LEASE_FILES`, onboard_apply.py:112); a live holder refuses the install | keep, `rebuilt_by: stand_lease.py` |
| 95-99 | the five lock rows | exit_gate / exploration / project_decisions / event_store | 3 | keep |
| 101 | state/execution-leases* | execution_scheduler.py | a lease registry (row note) | keep, `rebuilt_by: execution_scheduler.py` |
| 102 | state/scheduler-requests/** | execution_scheduler.py | written at execution_scheduler.py:565 | keep, `rebuilt_by: execution_scheduler.py` (open question for the critic: a pending request while no lease is alive) |
| 103 | state/.exit_gate_blocks.json | exit_gate.py | written under its lock, exit_gate.py:188-189, 330-336; read by `_existing` :387-391: per-scope block counts (the fuse) | keep, `rebuilt_by: exit_gate.py` — F-2 d (a reset fuse is a check reading less) |
| 104 | state/conductor-stop.json | conductor_stop.py | 2 | keep |
| 105 | state/native-context/** | native_context.py | written under native_context.py:17 | keep, `rebuilt_by: native_context.py` |
| 106, 107 | .dashboard-writer/**, .journal-writer/** | dashboard_refresh / log_append | 2 | keep |
| 108 | state/events.lock | event_store.py | 2 | keep |
| 109 | state/.stand-identity-writer/** | stand_identity.py | the writer folder of the stand registry (row note) | keep, `rebuilt_by: stand_identity.py` |
| 110 | state/bug-snapshot.json | bug_snapshot.py | written bug_snapshot.py:36; read metrics_projection.py:493 | keep, `rebuilt_by: bug_snapshot.py` |
| 111 | state/project-decisions-refresh-stale.json | project_decisions.py | written on a failed refresh, project_decisions.py:348-357; the install's own regenerate step rebuilds the dashboard (onboard_apply.py:1471-1475), which cures the staleness it marks | keep, `rebuilt_by: project_decisions.py` |
| 112 | state/reporter-rehearsals.json | gate_preflight.py | absent -> gate A rehearses again (a test run) | **RECLASS carried** (§2) |
| 113 | state/reporter-unread/** | report_adapt.py | absent -> "no kept report ... the next rehearsal of its command keeps one" (report_adapt.py:218): costs a rehearsal run | **F-2 b** (recommended: reclass carried) |
| 114 | state/benefit-inputs.json | metrics_projection.py | NO writer in the package: read at metrics_projection.py:668, named at :509; written only by a test (test_metrics_contract.py:192). Content only a person produces is `carried` by the table's own definition (install-paths.json:3) | **F-2 a** (recommended: reclass carried + queue the AR-22 gap) |
| 115 | state/budget/** | story_budget.py | "project state, disposable" (story_budget.py:13; row note) | keep, `rebuilt_by: story_budget.py` — F-2 d (a budget reset mid-story) |
| 116 | state/coverage-map.receipt.json | check_coverage.py | written only by `check_coverage.py --write` (:221-222, :246-248); the install runs check_coverage WITHOUT `--write` (onboard_apply.py:1474) so it never rebuilds it; when absent the binding check is silently skipped (:260-274) — an unknown that passes (AR-28) | **F-2 e** (recommended: reclass carried) |
| 117 | state/integrations/jira-direct-probe.json | readiness.py | a probe receipt readiness writes (readiness.py:232-266) | keep, `rebuilt_by: readiness.py` |
| 118 | state/integrations/tracker-write.json | tracker_write.py | 1 (:26) | keep |
| 119 | state/doctor-install-smoke-*.json | install_smoke.py | 4 | keep |

Not regenerated, so out of the rule: :100 `probe-copies/**` (carried), :121-123 discarded rows, :125-126 not_ours.

## 4. Item 3 — the installer

### 4.1 Where a person is asked today

Code does not ask; it REFUSES, and the refusal sends the role back to the person:
- `main`, `--apply` with a sealed proposal: `_changed_since_summary(root, listing_given["retire"], made["retire"], table)` — onboard_apply.py:1881-1884 — adds "a candidate the summary did not list" (:1291-1293) and raises `ApplyRefused(changed_message(...))` ("the project changed since the summary: ...; make the summary again", :1297-1299). This is the road of the incident: the rehearsal written after the summary is a NEW delete candidate.
- `apply`, phases `all`/`final`: `_changed_since_summary(root, listing["retire"], table=table)` — onboard_apply.py:1441-1444 — refuses on a listed file whose sha256 changed or that became a folder/link (:1285-1290).
- p4-generate.md:31-33 tells the role: "if one differs ... it refuses, names the paths and writes nothing: make the summary again." No phase line tells the role to ask about a factory file; the live question ("удалить или отложить в retired/?") was the role improvising on that refusal (finding :8-11).

### 4.2 The new behaviour

One function, `summary_drift(root, listing_retire, now_retire=None, table=None) -> dict`, replaces the body of `_changed_since_summary` (which, if kept, returns `summary_drift(...)["refuse"]`; S-1). Always the same keys (FR-14):

- `refuse[]` — rel paths OUTSIDE the home (or that do not normalise) that changed, became a folder/link, or are new since the summary. Non-empty -> the caller raises `ApplyRefused(changed_message(refuse))` exactly as today.
- `settled[]` — `{rel_path, class, retire_mode, kind, action, sha256, requires}` for paths INSIDE the home: `kind` ∈ `new` (a candidate of the fresh plan the summary did not list) / `changed` (listed, sha256 differs) / `not_a_file` (listed, now a folder or link); `action` ∈ `delete` / `keep`.

Home membership: `rel, why = I.normalize_rel(path)`; inside iff `why is None` and `I._key(rel, fold)` starts with `I._key(I.home_of(table), fold) + "/"`, `fold = I._fold_default()`. Nothing else (AR-1, axis 34).

Action by class (inside the home):

| kind | class now (`I.classify`, current table) | action | depends on |
|---|---|---|---|
| any | `carried` | not a drift row at all (skipped, like hook-written :1286-1287) | — |
| any | hook-written | skipped (unchanged, :1286-1287) | — |
| new | `retire_mode == "delete"` (discarded, regenerated not rebuilt) | delete, through `_retire`, sha256 taken from the fresh plan's item, `requires` kept (a `fold_receipt` item still "waits for the fold", :1348-1349) | F-3 |
| changed | `retire_mode == "delete"` | delete with the sha256 read NOW | F-3 |
| new / changed | `retire_mode == "move"` (undetermined: unrecognised, or named) | keep in place | F-4 |
| not_a_file | any | keep (a folder or a link is never retired, :960-964, :1356-1357) | — |

`apply` gains `after_summary=None` (the `new` rows `main` computed); inside `apply`, phases `all`/`final`:
1. `drift = summary_drift(root, listing["retire"], None, table)` for the listed rows; refuse on `drift["refuse"]` (position: §4.4);
2. the effective retire list handed to `_retire` = the sealed listing, with each `changed`+`delete` row's sha256 replaced by the current one (F-3), plus the `new`+`delete` rows, each marked `after_summary: true`. The sealed proposal and its hash are NOT modified (the effective list is an in-memory copy);
3. `out["after_summary"]` (always present, `[]` when nothing drifted) = one row per settled path: `{rel_path, kind, result, line}`; `result` is `_retire`'s result for acted rows (`deleted`, `kept: ...`, `already gone`, `waits for the fold`) or `kept: set aside only after a summary lists it` / `kept: no longer a plain file` for keep rows; `line` is one sentence a person reads (FR-6: no script name, no plugin path), e.g. "qa-factory/state/jira-probe-x.json: the factory's own technical data, found after the summary — deleted (it is in the removal record)".

Phase `early`: inside-home drift is neither refused nor acted on (early retires nothing, :1451-1460; the final half's own plan sees it again). Outside-home drift refuses in every phase, as today (`main` checks before `apply`, :1881).

`_retire` gains ONE branch, placed after the hook-written branch (:1354) and before the link/sha/delete branches: `elif I.classify(rel, table=table)["class"] == "carried": row["result"] = "kept: the factory keeps it"` (a sealed listing of an OLDER package that still names `reporter-rehearsals.json` for deletion never deletes it — twin of t-298, SIBLING_MAP:76).

p4-generate.md §0 `final` bullet (:27-33): the sentence "It reads every listed file again first; if one differs from what the summary showed it refuses, names the paths and writes nothing: make the summary again." becomes: what the half does with a file under `qa-factory/` that changed or appeared after the summary (settles it by its class and says so in `after_summary`; asks nothing); that it refuses only for a path outside `qa-factory/` (make the summary again — the person sees the new summary); and "Never ask the person what to do with a file under `qa-factory/`: relay the `after_summary` lines in the digest."

SKILL.md ## Digest (:130-138) gains one bullet: "**Factory files settled after the summary** — each `after_summary` line of the final apply half, as it stands; none -> no bullet."

### 4.3 Ways out (AR-25)

deleted -> named in the removal record (`retired/<date>/retire-record*.json`, :1385-1395) and in `tracking.git_rm` when tracked (:1384); kept (move-mode / not a file / changed move-mode) -> the next install's summary lists it under the person's one "yes"; carried kept -> never retired; stale rehearsal proofs are re-proved by gate A on a `function_sha` mismatch (CHANGELOG.md:5487).

### 4.4 Positional invariant (rule 11(ii))

The partition sits where `_changed_since_summary` is called today — `main` after `plan` and before `apply` (:1881-1884); `apply` after the live-writer check (:1425-1427), the proposal-hash check (:1428-1429), the approval check (:1430-1434) and the answers check (:1435-1439), and BEFORE the first write (:1451). What must stay unreachable / refused:
1. any write before the live-writer, hash, approval and answers refusals (order unchanged);
2. a path outside the home that changed, became a folder/link or is new since the summary refuses the WHOLE apply with nothing written (C2 kept for project files);
3. a carried path is never deleted or moved — whatever a listing says (the new `_retire` branch) and whatever a manifest says (install_paths.py:1026-1028);
4. a folder or a link is never retired;
5. an undetermined (move-mode) file is never moved unless a summary listed it;
6. the sealed proposal file and `proposal_hash` are never altered by the drift handling;
7. a hook-written file is never a drift row and never a refusal (t-298 unchanged).

## 5. Item 4 — the eval row

Append to `skills/qa-onboarding/evals/evals.json` (after id 15, :277-290):

```json
{
  "id": 16,
  "prompt": "Run qa-onboarding to the final apply half on a repository where, after the phase-3 summary was approved, the report check of a test profile wrote qa-factory/state/reporter-rehearsals.json and a probe left qa-factory/state/jira-probe-x.json, which the summary did not list.",
  "expected_output": "The final half asks the person nothing about either file. qa-factory/state/reporter-rehearsals.json is still on disk after the apply (gate A reads it). The stale probe file is deleted by its class and is named in the removal record. The digest carries one line per file the factory settled after the summary. A question to the person comes only for a path outside qa-factory/.",
  "files": [],
  "assertions": [
    {"name": "no-question-about-factory-files", "description": "Between the summary's yes and the digest, no message asks the person what to do with a file under qa-factory/."},
    {"name": "evidence-file-kept", "description": "qa-factory/state/reporter-rehearsals.json exists after the final apply half, with the bytes the report check wrote."},
    {"name": "settled-files-reported", "description": "The digest has one line per after_summary row of the final apply, naming the path and what the factory did with it."}
  ]
}
```
(The jira-probe sentence and "deleted" depend on F-3; with F-3 = B they read "kept, the next summary lists it".)

### 4.5 (role rules) Two rows in `design/role-rules.json` (TESTING.md: no text pins; the registry is the guard, test_role_rules.py)

- `p4-no-question-about-factory-files` — rule: "The final apply half settles a file under qa-factory/ by its class and the role never asks the person about it." carrier p4-generate.md, anchor "Never ask the person what" (2-6 words, exact after the edit).
- `skill-digest-settled-files` — rule: "The digest relays every after_summary line." carrier SKILL.md, anchor "settled after the summary".

## 5. Item 5 — owns, tests, witness, quarantine, AR, FR

### 5.1 Owns
In the dispatch header above (files + functions). Functions touched in onboard_apply.py, so OF1-2 can avoid them: module docstring :10-17, `_changed_since_summary` :1275-1294, new `summary_drift`, `_retire` :1335-1396 (one branch), `apply` :1399-1510 (signature + :1440-1444 + :1492-1495 + `out` keys), `main` :1880-1885. Shared files with OF1-2: onboard_apply.py (disjoint functions), p4-generate.md (§0 bullet only), evals.json (tail append) — the Lead writes `очередь: OH3-9 → OF1-2` (batch :68 already lists OH3-9 as a dependency of OF1-2).

### 5.2 Tests — one parameterised table per behaviour, rows not files (TESTING.md: «Новый случай приходит из дефекта»; no new test file)

**Table A — `test_install_paths.py` (keep, `data_join`; test-layers.json:2625-2642): the basis rule.** One new section `section_regenerated_basis`, one table `BASIS_ROWS = [(id, mutation of a deepcopy of TABLE, expected codes)]`:
- `no-basis` (row :112 as it stood: regenerated, no basis) -> `regenerated_without_basis` naming the glob (the defect, red before the fix);
- `rebuilt-by-missing-script`, `rebuilt-by-key-absent` -> `regenerated_without_basis` (or a distinct code; S-2);
- `rebuilt-by-bad-shape` x {`""`, `7`, `"none"`, `"../x.py"`, `"scripts/x.py"`} -> `shape`;
- `rebuilt-by-on-carried` -> `shape`;
- `hook-written-not-bool-only` -> `shape` + `regenerated_without_basis`;
- `basis-accepted` x {step output, hook_written, lock_kind, discard_when, rebuilt_by} -> ok.
Existing rows to flip in the same file (TESTING.md «Когда тест покраснел» 1): `REGENERATED_UNBUILT` (:460-467) loses `reporter-rehearsals.json` (and whatever F-2 reclasses); the Q7 check (:559-562) moves `reporter-rehearsals.json` to the carried machine-local check beside :563-565; `section_report_adaptations` (:759-786) flips only if F-2 b is taken. The shipped-table check (:51) proves every row of §3.3 carries a basis.

**Table B — `test_install_retire.py` (keep, `detector`; test-layers.json:2643-2664): what the apply does with drift.** The C2 section (:434-465) and K-A5 (:1318-1333) become ONE table `AFTER_SUMMARY = [(id, after-summary move, entry, expected)]`, world built once per entry kind:
- `new-evidence-file` (reporter-rehearsals.json written after the summary; cli `--phase final`) -> applied, file present byte for byte, no `after_summary` row, exit 0 — the incident;
- `older-listing-names-evidence` (a sealed listing that names reporter-rehearsals.json with retire_mode delete; apply() and cli) -> applied, file present, `_retire` result `kept: the factory keeps it`;
- `new-discarded-file` (jira-probe-x.json appears after the summary) -> F-3 A: deleted, in the removal record with `after_summary: true`, one row with a `line`;
- `listed-discarded-changed` (the old C2 case, apply() and cli) -> F-3 A: applied, deleted, row `changed`; (was: refused);
- `listed-became-folder` (inside the home) -> applied, kept, row `not_a_file`;
- `new-unrecognised-file` (qa-factory/my-notes.md after the summary) -> F-4 A: applied, file in place, row `kept`;
- `outside-listed-changed` (a project file named with `--also-retire docs/old.md`, changed after the summary) -> exit 1, `changed_message` names it, snapshot of the tree unchanged — the invariant control;
- `outside-new-candidate` (`--also-retire docs/old.md` given only at apply) -> refused, nothing written;
- `phase-early-inside-drift` -> no refusal, nothing retired;
- every `line` holds no `.py` and no `scripts/` (the :448 row, kept).
Plus a pure-function sub-table on `summary_drift` home membership (input from outside: project paths and `--also-retire`): `qa-factory/state/x.json` in; `qa-factory` (the home itself) out; `qa-factory-old/x` out; `qa-factory.bak/x` out; `QA-Factory/state/x.json` in only when the platform folds case; `./qa-factory/x` in; `qa-factory/../src/x` out (does not normalise -> refuse); `""` out; `C:/x` out.

**`test_reinstall_equals_fresh.py`** (keep, `gate_named`, :4259-4274): only if F-2 reclasses a row in `REGEN_UNBUILT` (:68-70: `coverage-map.receipt.json` is there) — move it to the kept side; nothing else.

**`test_role_rules.py`** (keep, `register`, :4479): no edit; it reads the two new registry rows.

**`test_judgment_census.py`** (keep, `register`, :2705): no edit to the test; rows added to `fixtures/judgment-census.json` for the units it names (`install_paths._basis_errors` class `xref` owner `data`; `onboard_apply.summary_drift` class `xref` owner `data`); each raise named in the report (AR-20).

The eval row is a skill eval, not a test (no runner in `scripts/tests` reads id 16).

### 5.3 Quarantine check (read from `scripts/tests/test-layers.json`; `quarantine` starts at :6966)

| file | section | where |
|---|---|---|
| test_install_paths.py | keep (`data_join`) | :2625 (only occurrence) |
| test_install_retire.py | keep (`detector`) | :2643 (only occurrence) |
| test_reinstall_equals_fresh.py | keep (`gate_named`) | :4259 (only occurrence) |
| test_role_rules.py | keep (`register`) | :4479 |
| test_judgment_census.py | keep (`register`) | :2705 |
Positive control of the read: the same Grep found `quarantine` at :6966 and the quarantined `test_acceptance_semantics.py` at :6967; none of the five names occurs after :6966.

### 5.4 DoD (inline; the builder's verification run)

Acceptance criteria:
1. install-paths.json: row of §2, moved into the carried block; every regenerated row carries a §3.1 basis per §3.3 (with the F-1/F-2 choices the Lead closed); description at :3 states `rebuilt_by` and the carried sentence.
2. `validate_table` refuses a regenerated row without a basis (`regenerated_without_basis`, message names the glob and the five ways out — FR-1) and the bad `rebuilt_by` shapes; the shipped table validates.
3. `summary_drift` is the one drift function, called by `main` and `apply`; behaviour per §4.2; positional invariants §4.4 hold; `apply` returns `after_summary` (always a list).
4. `_retire` keeps a path the current table calls carried.
5. p4 §0 bullet and SKILL Digest per §4.2; two role-rules rows; eval 16 appended.
6. FR walk A-G in the report (§5.6); AR lines (§1.1) in the report and commit (`architecture:` and `judgment:` lines).
Verification run (output verbatim in the report):
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/install-paths.json scripts/install_paths.py scripts/onboard_apply.py skills/qa-onboarding/evals/evals.json skills/qa-onboarding/phases/p4-generate.md skills/qa-onboarding/SKILL.md design/role-rules.json`
then `python -B ai-packages/qa-factory/scripts/tests/<file>` for each keep file it prints (expected at least: test_install_paths.py, test_install_retire.py, test_reinstall_equals_fresh.py, test_role_rules.py) — never a quarantined file, never a slow one (CI judges those); then `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` and `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
`docs/SIBLING_MAP.md` (outside the package, no test): doc-dispatch witness per CLAUDE.md rule 11 — key quoted verbatim before the run ("a path the current table calls carried is kept"), the script in full in the report, plus a negative control.

### 5.5 Siblings walked (rule 9)

SIBLING_MAP:76 — the new `_retire` "carried now" branch is the twin of the hook-written narrowing; the row gains one clause naming it. Axis 34 — home membership from the table's `home`; no language, project or case branch. Same artifact (`install-paths.json` regenerated block): all 31 rows enumerated in §3.3. Not walked (queued, not in this node's owns): other callers of `scan_tree(..., retire_unbuilt=True)` — grep showed only `plan` (onboard_apply.py:928) in the package's scripts read for this draft; the builder confirms with a positive-controlled grep and reports.

### 5.6 FR walk A-G (to be answered by the builder's report; designer's expectation)

- A: FR-3 — the factory's own files are reported (`after_summary`), not put as a choice; FR-1/FR-2/FR-57 — the outside-home refusal keeps its text and door; FR-4 — n/a (no informed pass); FR-48 — the conductor is not involved; FR-5, FR-46, FR-50 — n/a.
- B: FR-6 — every `line` and the Digest bullet follow `references/human-questions.md` (no script, no plugin path); FR-10 — p4 §0, SKILL Digest and eval 16 say the same thing; FR-7/8/9 — n/a.
- C: FR-13 — class, basis and home are data; FR-14 — `after_summary` always present; `summary_drift` always the same keys; FR-38 — the new table requirement is stated in the table's description before anyone writes a row; FR-49 — apply's rows reach the digest whole; FR-12, FR-15, FR-39, FR-42, FR-56, FR-11 — n/a (one line each).
- D: FR-40 — every outcome has a way out (§4.3); FR-59 — an unknown home membership refuses; FR-17 — one drift function wired at both sites; FR-16, FR-18, FR-58 — n/a.
- E: FR-37 — every path in a `line` is the path the code deleted or kept; others n/a.
- F: n/a — no money and no measurement changed.
- G: FR-30 English, no Cyrillic; FR-32 root cause + table rows; FR-33 — the role behaviour (no question) is proved only by a live onboarding: one row for the pile `live-runs` (PROJECT.md «Командная работа» п. 9); FR-47 — code settles data, the role relays; FR-54 — §5.5; FR-29, FR-31, FR-43, FR-44, FR-45, FR-52 — n/a.

## 6. Edges (each with the invariant it protects)

| edge | behaviour | invariant |
|---|---|---|
| E1 empty drift | `after_summary: []`, no Digest bullet | a report never invents a settled file |
| E2 no cap | every settled row is listed (onboard_apply.py:1044-1049: no group of the listing is cut) | nothing the factory did is unreported |
| E3 `--apply` without a sealed proposal (`listing_given is None`, :1881) | no drift check, as today | unchanged road |
| E4 new delete-mode file vanished before `_retire` | result `already gone` (:1352-1353) | no error for a file that left by itself |
| E5 new delete-mode file with `requires: ["fold_receipt"]` (product passport) | `waits for the fold` without the receipt (:1348-1349) | a requirement of a row is never skipped by the after-summary road |
| E6 TEMPORAL — table before/after this node | the move that creates `rebuilt_by` and the new class is this commit; before it, no row carries `rebuilt_by` and the shipped table validates; after it, every regenerated row carries a basis and the shipped table validates (:51) | the shipped table always validates |
| E7 TEMPORAL — a proposal sealed by an older package (row :112 regenerated) applied by this one | `_retire` keeps the file (`kept: the factory keeps it`) | a carried path is never deleted, whatever an older listing says |
| E8 TEMPORAL — an old manifest naming reporter-rehearsals.json `regenerated` machine-local | kept; the entry is carried forward with its old label | a manifest's word never retires a carried or machine-local path (install_paths.py:1166-1168, 1026-1028) |
| E9 path under the home that is a symlink/junction to outside | plan refuses links (:960-961); `_retire` keeps them (:1356) | nothing outside the root is touched |
| E10 a path matched by a carried and a regenerated row | carried (precedence, install_paths.py:59-61, 450) | carried wins |
| E11 conflict: owner's "not needed -> deleted" vs C2 "nothing retired that the summary did not list" | resolved by F-3 (recommended: the owner's word for delete-mode factory data inside the home; C2 stays for project files and for undetermined files) | a person's possible file is never removed unseen |
| E12 conflict: "never ask" vs the outside-home refusal | the refusal outside the home stays: that is the person's project file | the person decides only about their project files |
| E13 phase `early` | inside drift ignored, outside drift refused | early retires nothing |

## 7. Forks (returned, not decided)

**F-1 — the form of the class rule.** The brief: "a row whose reader is a gate or story-time script cannot be `regenerated` unless that script is among regenerate_step outputs' writers". The finding: "не может быть regenerated без явного основания".
- A (recommended): a uniform BASIS rule over all regenerated rows (§3.1): step output / hook_written / lock_kind / discard_when / `rebuilt_by` with its declared "absence costs nothing" meaning; the honesty of `rebuilt_by` is the author's judgment, accepted by the critic. Cost: one field on ~14 rows; no list of gate scripts anywhere.
- B (literal brief): reader not among `regenerate_step` scripts -> must not be regenerated. Cost: reclasses ~17 rows to carried, including leases, caches and the doctor smokes (:119), whose `discard_when` then cannot exist (carried never retires) — stale caches accumulate forever; contradicts the owner's "не нужны — удаляются".
- C: a list of "gate / story-time scripts" in the test. Cost: a closed list in code (AR-1 breach), drifts with every new script.
Note: under A the instance is caught only if the author answers `rebuilt_by` honestly (gate_preflight does rebuild the rehearsal — by a test run, which the declared meaning excludes). Code checks presence and the join; the meaning is the critic's question.

**F-2 — siblings found by the walk (§3.3); each its own sub-question.**
- a) `benefit-inputs.json` (:114): no writer in the package. Recommended: reclass carried machine-local now (never delete what nothing can rebuild) + a finding for the AR-22 gap (who should produce it). Alt: leave regenerated and only queue.
- b) `reporter-unread/**` (:113): its absence costs a rehearsal run (report_adapt.py:218); B-416 classed it regenerated on purpose (test_install_paths.py:760-770). Recommended: reclass carried machine-local (same owner's word as the instance). Alt: keep, with `rebuilt_by: report_adapt.py`, and accept the re-run.
- c) `host-probe.json` (:92): rebuilt by the doctor's next probe, unused by story work. Recommended: keep regenerated with `rebuilt_by: host_probe.py`.
- d) `.exit_gate_blocks.json` (:103) and `budget/**` (:115): a reinstall resets a fuse / a story budget. Recommended: keep regenerated (onboarding runs between stories; a live writer refuses the apply) — but the critic on plan should confirm that no story can be mid-run during a reinstall; if one can, both become carried.
- e) `coverage-map.receipt.json` (:116): the install never rebuilds it and its absence silently skips a binding check (AR-28). Recommended: reclass carried machine-local (flips test_reinstall_equals_fresh.py:70 and test_install_paths.py:80, :463). Alt: queue a finding to the pile, keep the row.

**F-3 — a delete-mode factory file under `qa-factory/` that appeared or changed after the summary.**
- A (recommended, the owner's word literally): deleted now, through `_retire`, with the sha256 read at apply time, named in the removal record and in `after_summary`. Cost: a file the person never saw listed is deleted — bounded to rows the table calls the factory's own technical data, and to machine-local state; the risk is a misclassified evidence file, which F-1 A's basis rule targets.
- B (safest): kept in place with a line; the next install's summary lists it. Cost: the leftover stays until the next reinstall (months); the owner's "удаляются" is delayed.
This changes C2's meaning for those files (test_install_retire.py:436-447 and K-A5 :1318-1333 flip): PROJECT.md п. 6 — critic on plan.

**F-4 — an undetermined (move-mode) file under `qa-factory/` that appeared or changed after the summary.** A (recommended): kept in place with a line, set aside only when a summary lists it (it may be the person's file; the owner's word covers the factory's own files). B: moved to `retired/<date>/` like a listed one. Cost of B: a person's file moved without a "yes".

**F-5 — where the report line lives.** A (recommended): `apply` JSON `after_summary[].line` (code writes the sentence once) + the removal record row flag; the role relays the lines in the Digest. B: code returns rows only and the role phrases them (cheaper code, but the text is then unpinned and may drift into a question — the incident's road).

## 8. Small choices closed by the designer (no design weight)

- S-1: `_changed_since_summary` is kept as a one-line wrapper returning `summary_drift(...)["refuse"]` only if a caller outside the two sites exists (the builder greps); otherwise both sites call `summary_drift` and the old name goes.
- S-2: a missing or key-less `rebuilt_by` script is reported under `regenerated_without_basis` with a message that says which (one code keeps the error vocabulary small); shape errors stay `shape`.
- S-3: `_manifest_entries` is not touched (old manifest labels are harmless, E8; and it is OF1-2's neighbourhood).
- S-4: `rebuilt_by` holds a script NAME under `scripts/` only (no package paths, unlike `reader`): a rebuilder is code, never a role text.
- S-5: the reclassed row moves into the carried block of the table (order inside a class matters only for "first row of a class wins", which this row does not overlap).
- S-6: the changelog fragment is one paragraph in English under `changelog.d/` (PROJECT.md «Релиз»).

## 9. Contradictions and analogs noticed in the brief (reported, scope not widened)

- The finding cites `install-paths.json:103` and `gate_preflight.py:495-502`; the carriers today are install-paths.json:112 and gate_preflight.py:865 / :3319 (the brief's ":112" is right).
- The brief's item 2 wording (F-1 B) and the finding's ("без явного основания", F-1 A) differ.
- The live run of 0.11.0 (batch file :74) shows the defect recurring after the finding — the instance is still open in the released package.
- `benefit-inputs.json` has a reader and no producer (AR-22) — a finding for the pile regardless of F-2 a.
- `coverage-map.receipt.json`: an absent receipt makes `check_coverage.py` skip the binding check silently (:260-274) — an AR-28 analog regardless of F-2 e.
- The question in the incident came from no phase line: the role improvised on a refusal whose door ("make the summary again") is a person's move. Other refusals of `onboard_apply` with a person-facing door were not walked (scope).

## 10. Reading trail

Read whole or in the ranges cited: the finding (all 36 lines); install-paths.json (all); install_paths.py :1-1213 (all); onboard_apply.py :1-135, :494-533, :839-1040, :1270-1519, :1775-1913, and a Grep of `def |ask|approved|summary|differ|retire` over it; p4-generate.md :10-49, :636-675 and a Grep for refusal/final/rehearsal; SKILL.md :120-145 and a Grep of headings; evals.json :1-60, :270-293 and a count of ids (15); test_install_paths.py :1-110, :420-820; test_install_retire.py :430-475, :1295-1340 and a Grep of C2 sites; test_reinstall_equals_fresh.py :60-75; test-layers.json :2620-2664, :4255-4274, :6960-6974 and Greps for the five file names (positive control: `quarantine` found at :6966); architecture.md :134-293; TESTING.md (all); exit_gate.py :170-209 and a Grep of `_state_path()`; check_coverage.py :195-279; host_probe.py :1-40, :575-604; project_decisions.py :340-369; Greps over the package for `reporter-rehearsals`, `reporter-unread`, `exit_gate_blocks`, `coverage-map.receipt`, `benefit-inputs` (CHANGELOG excluded; the negative claim "no writer" rests on this Grep, whose same pattern found the known reader metrics_projection.py:668 and the test writer test_metrics_contract.py:192), `bug-snapshot|refresh-stale|native-context|host-probe|jira-direct-probe|scheduler-requests`, `validate_table(`, `_changed_since_summary`; judgment-census.json Greps (install_paths rows :419-423; onboard_apply :581); role-rules.json Grep (p4 rows :166-169); `test_role_rules.py` and `test_judgment_census.py` keep rows; scenario_walk.py :887-931; builder-rules.md :16-20; SIBLING_MAP.md :76, :582; batch file :30, :68, :74; README of the pile :100; changelog.d listing.
Not read (beyond the manifest is none needed): `references/human-questions.md` (the builder reads it for the `line` texts).
