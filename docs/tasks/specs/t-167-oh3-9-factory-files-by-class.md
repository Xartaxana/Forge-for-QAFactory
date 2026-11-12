# t-167 — OH3-9: the factory settles its own files by class, never asks (DRAFT, fix round after t-170)

Node: `onboarding-forge/1/OH3-9` (`plans/piles/onboarding-forge/batch-1-onboarding-roles-forge.md:30`).
Finding: `plans/piles/onboarding-forge/findings/20261022-onbording-sprashivaet-pro-sluzhebnye-fajly-fabriki.md`, items 1-4.
Owner's word 22.10.2026 (verbatim, finding :5-6): «Фабрика не должна спрашивать о её служебных файлах. Если они не нужны,
то удаляются, если нужны как доказательства для дальнейшей работы со стори — сохранять».
Status: DRAFT by designer, attempt 2 (fix round of critic on plan t-170, verdict `docs/tasks/specs/reviews/t-170-oh3-9-plan.md`).
Forks F-1..F-5 were closed by the Lead 12.11.2026 at the designer's recommendation; the body below states the closed choices
unconditionally (t-170 M3). The Lead decided M1 for this round: F-3 A deletes ONLY machine-local delete-mode rows of the factory's
own technical data (§4.2, §4.4 invariant 8, edge E14). One new fork, F-6 (where the `rebuilt_by` judgment is registered, t-170 M4),
is returned with a recommendation; the node is executable by the recommendation (§8).
This spec changes the MEANING of a gate (the C2 "changed since the summary" refusal) — PROJECT.md «Как принимается изменение
пакета» п. 6 applies: critic on plan before the builder (t-170 done; a re-review only if the Lead judges the fixes architectural).

## Dispatch header (R11-f; copied into the builder dispatch once accepted)

given: C:\QAFactory\forge-repo\docs\tasks\specs\t-167-oh3-9-factory-files-by-class.md (this spec, carries the enumeration), C:\QAFactory\forge-repo\ai-packages\qa-factory\design\factory-rules.md, C:\QAFactory\forge-repo\plans\builder-rules.md, C:\QAFactory\forge-repo\ai-packages\qa-factory\design\architecture.md, C:\QAFactory\forge-repo\docs\TESTING.md, C:\QAFactory\forge-repo\plans\piles\onboarding-forge\findings\20261022-onbording-sprashivaet-pro-sluzhebnye-fajly-fabriki.md, C:\QAFactory\forge-repo\ai-packages\qa-factory\references\install-paths.json, C:\QAFactory\forge-repo\ai-packages\qa-factory\references\human-questions.md, C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\install_paths.py, C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\onboard_apply.py, C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_install_paths.py, C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_install_retire.py, C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_reinstall_equals_fresh.py, C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json, C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\evals\evals.json, C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p4-generate.md, C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\SKILL.md, C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json, C:\QAFactory\forge-repo\docs\tasks\specs\reviews\t-170-oh3-9-plan.md
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\install-paths.json
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\install_paths.py (functions: `_shape_errors`, new `_basis_errors`, new `in_home`, `validate_table` (one call line + docstring); nothing else)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\onboard_apply.py (module docstring lines 9-23; `_changed_since_summary` :1275-1294; new `summary_drift`; new `_after_summary_line`; `_retire` :1335-1396; `apply` :1399-1510 (docstring :1401-1409, signature, `out` init :1413-1414, :1440-1444, :1492-1495); `main` :1880-1885 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_install_paths.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_install_retire.py
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_reinstall_equals_fresh.py (only `REGEN_UNBUILT` :68-70 and `MACHINE_LOCAL_KEPT` :109-111)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (only rows `test_judgment_census.py` demands for the units below)
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\role-rules.json (two rows, §5.2)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\evals\evals.json (one eval appended, id 16)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\phases\p4-generate.md (§0, the `final` bullet, lines 27-33 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-onboarding\SKILL.md (## Digest, lines 130-138 only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\oh3-9-factory-files-by-class.md (new fragment)
C:\QAFactory\forge-repo\docs\SIBLING_MAP.md (row at :76, one clause appended)
non-goals: OF1-2 (summary seal: `plan`, `config_contract.proposal_hash`, `config_contract.fill_proposal`, `_proposal_for`, the `check_input` path, `_manifest_entries`, p3-summary-gate.md — none touched here); any change to `scan_tree` (its inline home test at install_paths.py:1126 included — analog, §10), `classify`, `find_locks`, `_plan_moves`; any new test file; the doctor; the gate A rehearsal code (`gate_preflight.py`, `onboarding_probe.py`, `report_adapt.py`) — they keep writing and reading the file as today; the producer of `benefit-inputs.json` (AR-22 gap — finding filed by the Lead, §10); `docs/tasks/critic-diff-brief.md` and `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (F-6, a Lead node).
handoff: builder report per `.claude/agents/builder.md` rule 7 (FR walk A-G, AR lines, witness verbatim, analogs noticed), branch `pile/onboarding-forge/batch-1`, commit hash.
edges: §7 of this spec (each with its invariant); summary: home membership battery (incl. trailing dot/space), temporal (older sealed listing; old manifest; table before/after), positional (where the drift partition sits; §4.4 invariants 1-8), non-machine-local delete-mode row never deleted after the summary, unreadable file kept, empty `after_summary` (and present on every return), no cap on rows.
DoD: §6.4 — `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/install-paths.json scripts/install_paths.py scripts/onboard_apply.py scripts/tests/test_install_paths.py scripts/tests/test_install_retire.py scripts/tests/test_reinstall_equals_fresh.py scripts/tests/fixtures/judgment-census.json design/role-rules.json skills/qa-onboarding/evals/evals.json skills/qa-onboarding/phases/p4-generate.md skills/qa-onboarding/SKILL.md`, then each printed keep file that is not in `quarantine` and not slow, then `python -B ai-packages/qa-factory/scripts/selftest.py --lang`.
siblings: SIBLING_MAP:76 (hook_written narrowing: an older sealed listing is re-asked of the current table — the new "carried now" branch of `_retire` is its twin); axis 34 (one road: home membership read from the table's `home` through `install_paths.in_home`, never a literal or a language); the regenerated rows of `install-paths.json` :87-119 (walked in §3.3); the delete-mode rows outside `state/` (:122 `qa-factory/readiness.json`, :123 `strategy/product-passport.md`; §4.2, M1).
designer: C:\QAFactory\forge-repo\docs\tasks\specs\t-167-oh3-9-factory-files-by-class.md (once accepted)

## 1. What this touches (designer rule 1; CLAUDE.md rule 10, P27)

### 1.1 AR-n touched, with the change check each demands (goes into the DoD)

| AR | how touched | change check written into the DoD |
|---|---|---|
| AR-1 | the class of a path, the `rebuilt_by` basis and its note are data rows; the home prefix is the table's `home` (`install_paths.home_of`, install_paths.py:285), read through the new `install_paths.in_home`, never a literal in `summary_drift` | grep `summary_drift` and `in_home` for the literal `"qa-factory"`: none |
| AR-13 | `I.classify` stays the one reader of a path's class and `machine_local`; `summary_drift` and `_retire` call it and parse no glob themselves | no `_match(` / `fnmatch` added to onboard_apply.py (grep) |
| AR-14 | `install-paths.json` stays the one table; `_retire` stays the one unlink site and the one writer of the removal record (onboard_apply.py:1360-1395); the rehearsal file keeps its writers (`gate_preflight.py:3319`, `onboarding_probe.py:379`) | the after-summary deletions go through `_retire` (same record, same `tracking`), never a second unlink site; grep `os.unlink(` in onboard_apply.py: no new site |
| AR-15 | one survivor for "did the project drift since the summary": `summary_drift`, called by BOTH `main` (today onboard_apply.py:1881-1884) and `apply` (today :1441-1444) | both call sites call `summary_drift`; `_changed_since_summary` is removed (S-1) |
| AR-21 | the apply's `after_summary[]` rows travel whole to the role's digest (SKILL.md ## Digest); the role relays every row | the Digest bullet names `after_summary`; eval 16 asserts one line per settled file |
| AR-22 | new field `rebuilt_by` (producer: table rows; reader: `validate_table` via `_basis_errors`); new apply key `after_summary` (producer: `apply`; readers: p4 §0, SKILL Digest); `benefit-inputs.json` has a reader and no producer (finding filed by the Lead, §10) | grep `rebuilt_by` and `after_summary` case-insensitively over `scripts/ agents/ skills/ references/ handoffs/` with a positive control (`retire_mode` found the same way); every hit is a reader or the producer |
| AR-25 | every outcome has a way out (§4.3) | stated per `after_summary` result in §4.3; no new recorded state, so no `design/state-exits.md` row (reason: `after_summary` is a report of what one apply did, not a state anything resumes from) |
| AR-28 | a path that does not normalise, whose home membership cannot be established, or that cannot be read OUTSIDE the home refuses (declared safe default); inside the home an unreadable file is kept, never deleted | Table B rows `outside-*`, `listed-unreadable`, home-membership sub-table |
| AR-29 | two checks added, two altered (§1.2) | owner + census class named per check (§1.2); run `test_judgment_census.py`; a raised count named in the verdict (AR-20) |
| AR-9 | the outside-home refusal keeps `changed_message` (onboard_apply.py:1297-1299) with its door "make the summary again" | text unchanged; Table B checks every refusal and every `line` for no `.py` and no `scripts/` (today's row test_install_retire.py:448) |

AR-17 / AR-16: not touched by new code — this node REMOVES a question; no question site is added (no `person-owned` row needed).
AR-19: none — the onboarding apply has no stage twin (the headless entry is the same `main`).

### 1.2 Checks added or altered — owner and census class (AR-29)

| check | new/altered | owner it serves | census class | error direction |
|---|---|---|---|---|
| `install_paths._basis_errors` (via `validate_table`): every `regenerated` row carries a basis | new | data (presence of a basis + a join: the named script exists under the package root and contains the row's key). The claim behind `rebuilt_by` ("its absence costs no run, no money, no question") is JUDGMENT of the table's author, written in the row's `note`, accepted by a tier above (F-6) | `xref` | may err toward REFUSING only (a false refusal costs the author one field, and `validate_table` runs only in tests — every caller is under `scripts/tests` (t-170 Key 4; callers listed in §11) — so it costs a red CI, never a person's install); must never accept a regenerated row with no basis. Known false pass: a `rebuilt_by` naming a script that only READS the key passes the text join — that is what the `note` and F-6 exist for |
| `install_paths._shape_errors`: `rebuilt_by` shape + a non-empty `note` on a `rebuilt_by` row | altered | data (presence and type) | `shape` | refuse-only |
| `onboard_apply.summary_drift` (replaces `_changed_since_summary`) | altered | data (home from the table, class and machine_local from `classify`, mode from the listed item, bytes vs the listed sha256). Intent: the owner's word 22.10.2026 decides which files the factory settles alone; the Lead's M1 bound (machine-local only) | `xref` | may err only toward REFUSE (a path outside the home) or KEEP (inside); never toward deleting a path outside the home, a carried path, a non-machine-local path, a link, a folder or an unreadable file |
| `install_paths.in_home` | new (predicate used by the gate above) | data | — (a predicate, not a refusal; census row only if the test demands one) | may err only toward False (outside -> refuse): a path that does not normalise is False |
| `_retire` branch "carried by the current table -> kept" and "unreadable -> kept" | new branches of an existing unit | data | `shape` | only subtract from a retirement; may err only toward keeping |

## 2. Item 1 — the class of `reporter-rehearsals.json`

Facts (read):
- The row today: `{"glob": "qa-factory/state/reporter-rehearsals.json", "class": "regenerated", "machine_local": true, "reader": "gate_preflight.py"}` — install-paths.json:112 (the finding's ":103" is stale).
- Readers: `gate_preflight.py:865` (`REPORTER_REHEARSALS_FILE`), path built at `gate_preflight.py:3319`; `report_adapt.py:41` (`REHEARSALS_REL`), read at :123-131; writer at onboarding: `onboarding_probe.py:379`.
- Because the row is `regenerated`, has no basis and is no `regenerate_step` output (install-paths.json:25-30), `plan` -> `scan_tree(..., retire_unbuilt=True)` (onboard_apply.py:928) lists it for DELETE (install_paths.py:1117-1124) — pinned today by `REGENERATED_UNBUILT` (test_install_paths.py:466) and the Q7 row check (test_install_paths.py:559-562).
- The live run of 0.11.0 on 12.11 repeated the defect (batch file :74).

Answer: **`carried` + `machine_local: true` is legal in `state/`; no new class is needed.** `_layout_errors` refuses only a carried row that is NOT machine-local inside an untracked folder (install_paths.py:668-673); a machine-local row is refused only inside a TRACKED folder (:674-679). Carried machine-local rows already live in `state/` (install-paths.json:65-85), and test F7 asserts this shape (test_install_paths.py:432-433).

Change (one of four reclassed rows, §3.4): install-paths.json:112 becomes
`{"glob": "qa-factory/state/reporter-rehearsals.json", "class": "carried", "machine_local": true, "reader": "gate_preflight.py", "note": "the proof that a profile's test command writes a readable report, per project and command (gate A reads it before rehearsing again): evidence for later story work, kept in place, never retired (owner, 22.10.2026)"}`
and MOVES up into the carried block (after :85).

Consequences named for the builder:
- A carried row never carries `retire_mode` (install_paths.py:562-563) — none is added.
- The manifest: a carried machine-local row is not added by `_manifest_entries` (onboard_apply.py:517-520). An OLD manifest that names it `regenerated` machine-local is carried forward with its old label (onboard_apply.py:521-528) — harmless: machine-local manifest entries never retire (install_paths.py:1166-1168) and classify's precedence wins (S-3; `_manifest_entries` is OF1-2's).
- The description at install-paths.json:3 gets two sentences (exact text in §3.1 and §3.4).

## 3. Item 2 — the class rule, not the instance

### 3.1 The rule

**Every `regenerated` row states its BASIS, and `validate_table` refuses one that does not** (new error code `regenerated_without_basis`). A basis is exactly one of (data read from the row; the list is the code's closed enumeration of the table's own fields, not of paths):

1. the glob covers an output of a `regenerate_step`: `any(_match(o.split("/"), glob.split("/"), False) for o in _step_outputs(table))` (helper at install_paths.py:519-525; same expression as :583);
2. `hook_written is True` (a real bool);
3. `lock_kind in LOCK_KINDS`;
4. a well-formed `discard_when` (`isinstance(cond, dict) and isinstance(cond.get("json_field"), str) and isinstance(cond.get("differs_from"), str)` — the predicate of :615-617);
5. NEW field `rebuilt_by: "<script name>"`: the file `_reader_path(package_root, name)` (install_paths.py:480-481; with no slash that is `<package_root>/scripts/<name>`) read through `_read_lower` (:484-490) is not None and contains `_key_of(row).casefold()` (:468-477). It is resolved under `validate_table`'s `package_root` argument and read DIRECTLY, exactly as the reader check at :758-768 does — never looked up in `_corpus` (:493-511), which excludes this module and the tests (G4 row test_install_paths.py:252: "a mention in tests / this table / this module is not a reader"): a corpus join would refuse row :88 (`rebuilt_by: install_paths.py`) and synthetic test packages would never see it (t-170 M2 b).

`_basis_errors(table, package_root, shaped) -> list` (new, in install_paths.py, placed after `_layout_errors`):
- iterates the valid rules (`class in PRECEDENCE`, string glob) with `class == "regenerated"`;
- SKIPS a row whose glob is in `shaped` (the set of globs that already carry a `shape` error): one error per row, the convention of t-298 (install_paths.py:572-573). A malformed row is refused by its shape error already; this keeps the existing exact-code assertions true (test_install_paths.py:663 "a non-bool flag gives exactly one `shape` error" on `dashboard-dirty.json`, whose only basis is the flag);
- emits `{"code": "regenerated_without_basis", "glob": <glob>, "message": ...}` when none of 1-5 holds. Message (FR-1: what is wrong, what is expected, how): for no basis at all — "regenerated row '<glob>' states no basis: a reinstall would delete it as a leftover nothing rebuilds. Give it one: an output of a `regenerate_step`, `hook_written: true`, a `lock_kind`, a `discard_when`, or `rebuilt_by: <script under scripts/>` with a `note` saying why its absence costs no test run, no money and no question. If its absence costs any of these, the row is `carried`."; for a `rebuilt_by` that does not resolve — "`rebuilt_by` '<name>' of '<glob>' is not in the package (scripts/<name>)" + the same ways out; for a key-less script — "`rebuilt_by` '<name>' does not contain '<key>', the key of '<glob>'" + the same ways out (S-2: one code).

Called from `validate_table` by one line after the reader loop (install_paths.py:758-768) and before `nones = ...` (:769): `errors.extend(_basis_errors(table, package_root, {e["glob"] for e in errors if e["code"] == "shape"}))`. The docstring's code list (:700-707) gains `regenerated_without_basis`.

Shape rules (in `_shape_errors`, one `elif` chain so a row gets at most ONE error from this block):
- `rebuilt_by` present and not a non-empty string, or containing `/`, `\`, `..`, or equal to `none` (casefold) -> `shape` "`rebuilt_by` must be ONE script name under scripts/ (no path, not `none`: a file nothing rebuilds is not regenerated)";
- elif the row's class is not `regenerated` -> `shape` "`rebuilt_by` belongs on a regenerated row only";
- elif `note` is absent, not a string, or blank after strip -> `shape` "a `rebuilt_by` row carries a `note` saying why its absence costs no test run, no money and no question" (t-170 M4: the reviewable claim).

Description sentence appended at install-paths.json:3: "`rebuilt_by` (regenerated rows only) names the script under scripts/ that writes the file again by itself when it is absent; the row's `note` says why its absence costs no test run, no money and no question, and no check reads less for want of it. A regenerated row states one basis: a `regenerate_step` output, `hook_written`, a `lock_kind`, a `discard_when`, or `rebuilt_by` (validate_table refuses a row with none). A row whose absence would cost a run, money or a question is `carried`."

### 3.2 Error direction and adversarial inputs (designer rule 1: `validate_table` gains a gate role)

`validate_table` is already a gate (the shipped table must validate: test_install_paths.py:51). The new branch may err toward refusing only. Rows that must stay REFUSED (each a row of Table A, §6.2): no basis at all (row :112 as it stood); `rebuilt_by` naming a script absent from `scripts/`; `rebuilt_by` naming an existing script without the key; `rebuilt_by` of a bad shape (`""`, `7`, `"none"`, `"../x.py"`, `"scripts/x.py"`, `"a\\b.py"`); `rebuilt_by` on a carried, discarded or not_ours row; a `rebuilt_by` row without a usable `note`; `hook_written: "yes"`, an unknown `lock_kind`, or a malformed `discard_when` as the only "basis" (refused by `shape`). A script larger than `CORPUS_MAX_BYTES` reads as None through `_read_lower` and is refused as not in the package — the safe side (the existing reader check behaves the same). Each of the five bases alone is ACCEPTED.

### 3.3 The walk of every regenerated row (install-paths.json:87-119)

"basis" = which of §3.1 1-5 the row carries after this node. For each `rebuilt_by` row the exact `note` is given (new or replacing the present one). In every `rebuilt_by` row the value equals the row's `reader` (t-170 M4 observation): the field is the explicit claim, the note is its reviewable carrier.

| line | glob | basis after this node | row change |
|---|---|---|---|
| 87 | state/readiness.json | 1 (:26) | none |
| 88 | install-manifest.json | 5 | add `"rebuilt_by": "install_paths.py"`, `"note": "the install record: every apply writes it again (install_paths.write_manifest); a missing one is read as no manifest (onboard_apply.py:1496-1497), as on a fresh install: no test run, no money, no question"` |
| 89 | state/factory-dashboard.html | 1 (:27) | none |
| 90, 91 | dashboard-dirty.json, dashboard-refresh.json | 2 | none |
| 92 | state/host-probe.json | 5 | add `"rebuilt_by": "host_probe.py"`, `"note": "the host probe's cache (host_probe.py is its one writer): the doctor's next probe writes it again; while absent, is_probe_child reads false, the safe side; story work does not read it"` |
| 93 | state/metrics*.json | 1 (covers metrics.json, :27) | none |
| 94 | state/stand-*.json | 5 | add `"rebuilt_by": "stand_lease.py"`, `"note": "a stand lease registry: a live holder refuses the install; with none alive it is a leftover the next lease writes again: no test run, no money, no question"` |
| 95-99 | the five lock rows | 3 | none |
| 101 | state/execution-leases* | 5 | add `"rebuilt_by": "execution_scheduler.py"`; note becomes `"a lease registry: a lease whose holder is alive refuses the install (find_locks); with none alive the file is a leftover this install does not rebuild, and the next lease writes it again: no test run, no money, no question. Its .lock file is the lock row above"` |
| 102 | state/scheduler-requests/** | 5 | add `"rebuilt_by": "execution_scheduler.py"`, `"note": "a scheduler request: a run that wants a lease writes a new one; a request left with no lease alive is a leftover: no test run, no money, no question"` |
| 103 | state/.exit_gate_blocks.json | 5 | add `"rebuilt_by": "exit_gate.py"`, `"note": "the exit gate's per-scope block counts (the fuse): exit_gate writes it again at its next state update. A story paused across a reinstall loses its count, so the gate may run its checks and block once more: one extra gate run, stricter, never looser (accepted, F-2 d, 12.11.2026)"` (t-170 m4) |
| 104 | state/conductor-stop.json | 2 | none |
| 105 | state/native-context/** | 5 | add `"rebuilt_by": "native_context.py"`, `"note": "native context state: native_context writes it again on its next use: no test run, no money, no question"` |
| 106-108 | .dashboard-writer/**, .journal-writer/**, events.lock | 2 | none |
| 109 | state/.stand-identity-writer/** | 5 | add `"rebuilt_by": "stand_identity.py"`; note becomes `"the writer lock of the stand registry; named so the stand-*.json row (stand_lease) never claims it. stand_identity makes it again at its next write: no test run, no money, no question"` |
| 110 | state/bug-snapshot.json | 5 | add `"rebuilt_by": "bug_snapshot.py"`, `"note": "a snapshot bug_snapshot writes again on its next run: no test run, no money, no question"` |
| 111 | state/project-decisions-refresh-stale.json | 5 | add `"rebuilt_by": "project_decisions.py"`, `"note": "the mark of a failed refresh; the install's own regenerate step rebuilds the dashboard, which cures the staleness it marks: no test run, no money, no question"` |
| 112 | state/reporter-rehearsals.json | — | **reclassed carried** (§2) |
| 113 | state/reporter-unread/** | — | **reclassed carried** (§3.4) |
| 114 | state/benefit-inputs.json | — | **reclassed carried** (§3.4) |
| 115 | state/budget/** | 5 | add `"rebuilt_by": "story_budget.py"`; note becomes `"state/budget/<task>.json: the warn-once marker of a story's budget (story_budget.py); the ceiling reads the price, not this file. A story paused across a reinstall gets its budget warning once more: one repeated warning, no test run, no money (accepted, F-2 d, 12.11.2026)"` (t-170 m4) |
| 116 | state/coverage-map.receipt.json | — | **reclassed carried** (§3.4) |
| 117 | state/integrations/jira-direct-probe.json | 5 | add `"rebuilt_by": "readiness.py"`, `"note": "a probe receipt readiness writes again on its next run: no test run, no money, no question"` |
| 118 | state/integrations/tracker-write.json | 1 (:26) | none |
| 119 | state/doctor-install-smoke-*.json | 4 | none |

Not regenerated, so out of the rule: :100 `probe-copies/**` (carried), :121-123 discarded rows, :125-126 not_ours.
Joins: t-170 Key 1 verified by `grep -ciF <key> <script>` that every `rebuilt_by` script above contains the row's key (all >= 1), so the shipped table validates.

### 3.4 The four reclassed rows (closed F-2 a, b, e and the instance)

All four become `carried`, `machine_local: true`, keep their `reader` (and :116 its `key`), lose nothing else, and MOVE into the carried block after :85 in this order:
- :112 reporter-rehearsals.json — row text in §2.
- :113 `{"glob": "qa-factory/state/reporter-unread/**", "class": "carried", "machine_local": true, "reader": "report_adapt.py", "note": "the report a probe run wrote and the code could not read, with its manifest (B-416): the folder of a profile is replaced by the next unread run. Without it the next rehearsal of that command runs again (report_adapt.py), so it is evidence: kept in place, never retired (owner, 22.10.2026)"}` — knowingly overrides B-416's class (t-170: correct under the owner's word).
- :114 `{"glob": "qa-factory/state/benefit-inputs.json", "class": "carried", "machine_local": true, "reader": "metrics_projection.py", "note": "the inputs of the benefit metric: nothing in the package writes it, so nothing could rebuild it: kept in place, never retired (owner, 22.10.2026)"}`.
- :116 `{"glob": "qa-factory/state/coverage-map.receipt.json", "class": "carried", "machine_local": true, "reader": "check_coverage.py", "key": ".receipt.json", "note": "the binding receipt check_coverage.py --write leaves; the install runs check_coverage without --write, so it never rebuilds it: kept in place, never retired (owner, 22.10.2026)"}`.
Description sentence appended at install-paths.json:3: "carried also covers machine-local evidence a later story or gate reads, whose absence would cost a run, money or a question (owner, 22.10.2026)."

## 4. Item 3 — the installer

### 4.1 Where a person is asked today

Code does not ask; it REFUSES, and the refusal sends the role back to the person:
- `main`, `--apply` with a sealed proposal: `_changed_since_summary(root, listing_given.get("retire") or [], made["retire"], I.load_table())` — onboard_apply.py:1882 — adds "a candidate the summary did not list" (:1291-1293) and raises `ApplyRefused(changed_message(...))` (:1883-1884; text :1297-1299). This is the road of the incident: the rehearsal written after the summary is a NEW delete candidate.
- `apply`, phases `all`/`final`: `_changed_since_summary(root, listing["retire"], table=table)` — onboard_apply.py:1441-1444 — refuses on a listed file whose sha256 changed or that became a folder/link (:1285-1290).
- p4-generate.md:31-33 tells the role: "It reads every listed file again first; if one differs from what the summary showed it refuses, names the paths and writes nothing: make the summary again." The live question was the role improvising on that refusal (finding :8-11).

### 4.2 The new behaviour

**`install_paths.in_home(path, table, fold=None) -> bool`** (new): `rel, why = normalize_rel(path)`; False when `why is not None`; `fold = _fold_default() if fold is None else fold`; `h = _key(home_of(table), fold)`; True iff `_key(rel, fold) == h or _key(rel, fold).startswith(h + "/")` — the same test as scan_tree's inline one (install_paths.py:1126), so a later node can make scan_tree call it (§10).

**`onboard_apply.summary_drift(root, listing_retire, now_retire=None, table=None) -> dict`** (new; replaces `_changed_since_summary`, S-1). Always the keys `refuse` (list of rel paths) and `settled` (list of rows `{rel_path, kind, action, item}`) (FR-14). `table = table if table is not None else I.load_table()`.

For each listed item (`listing_retire`), then for each `now_retire` item whose `rel_path.casefold()` is not among the listed ones (same casefold comparison as today :1292):
1. `c = I.classify(item["rel_path"], table=table)`. If `c["class"] == "carried"` or `c["hook_written"]`: skip — not a drift row (carried: never retired; hook-written: unchanged t-298 rule, :1286-1287).
2. Determine `kind`:
   - a `now_retire` item -> `new`;
   - a listed item: `path = _abs(root, rel)`; not `os.path.lexists(path)` -> skip (a listed file that is gone is not a change, today's rule :1278); `os.path.islink(path) or not path.is_file()` -> `not_a_file`; else `sha = I.sha256_file(path)` inside `try/except OSError` -> on OSError `unreadable`; `sha != item["sha256"]` -> `changed`; equal -> skip (no drift).
3. If `not I.in_home(item["rel_path"], table)`: append the rel path to `refuse` (every kind: C2 kept for the person's project files; an unreadable outside file refuses — an unknown never passes, AR-28). Continue.
4. Inside the home, `action` (the M1 bound):

| kind | condition (`retire_mode` = the ITEM's `retire_mode`, set by `scan_tree` with the class's mode — `classify` returns None for a regenerated row without its own mode, install_paths.py:455; `machine_local` = `c["machine_local"]` from the CURRENT table) | action |
|---|---|---|
| new | `retire_mode == "delete"` and `machine_local` is True | `delete` — `item` is the fresh plan's item (its sha256 and `requires` as planned), plus `"after_summary": True` |
| changed | `retire_mode == "delete"` and `machine_local` is True | `delete` — `item` is a copy of the listed item with `sha256` replaced by the sha read in step 2, plus `"after_summary": True` |
| new / changed | any other case: `retire_mode == "move"` (undetermined), a missing `retire_mode`, or a delete-mode row that is NOT machine-local (`qa-factory/strategy/product-passport.md`, install-paths.json:123: tracked, may carry a person's or the fold step's edits) | `keep` — `item` is the item unchanged (a listed one keeps its SEALED sha, so `_retire` keeps it with `kept: changed since the summary`, onboard_apply.py:1358-1359) |
| not_a_file | any | `keep` (a folder or a link is never retired, :1356-1357) |
| unreadable | any | `keep` (never a crash, never a delete; t-170 m5) |

**`apply`** gains the keyword `after_summary=None` (the `new` rows `main` computed). `out` gets `"after_summary": []` in its FIRST literal at :1413-1414, so every return — the `nothing_to_do` return at :1418-1419 and phase `early` included — carries it (FR-14; t-170 m1). In phases `all`/`final`, at :1440-1444:
1. `drift = summary_drift(root, listing["retire"], None, table)`; `if drift["refuse"]: raise ApplyRefused(changed_message(drift["refuse"]))` (position: §4.4);
2. `settled = drift["settled"] + list(after_summary or [])`;
3. at :1492, `_retire` receives an in-memory copy `effective = dict(listing, retire=[...])`: each listed item replaced by its settled row's `item` where the settled action is `delete`, every other listed item unchanged, plus the `new` rows with action `delete` appended. The sealed proposal, its `listing` and `proposal_hash` are NOT modified;
4. after `_retire`, `out["after_summary"]` = one row per settled row: `{rel_path, kind, result, line}`, where `result` is `_retire`'s result for that rel path when the item went to `_retire` (every listed row, every `delete` row), and `"kept: the next summary lists it"` for a `new` row with action `keep`; `line = _after_summary_line(rel_path, kind, result)`.

**`_after_summary_line(rel, kind, result) -> str`** (new; the one place the sentence is written, F-5 A). `seen` = "appeared" for `new`, "changed" for `changed`. Mapping (first match):
- `deleted` -> "<rel>: the factory's own technical data, <seen> after the summary - deleted; the removal record names it."
- `kept: cannot be read` or kind `unreadable` -> "<rel>: could not be read after the summary - kept as it is; the next summary lists it."
- `kept: no longer a plain file` or kind `not_a_file` -> "<rel>: is no longer a plain file - kept as it is."
- `kept: changed since the summary` or `kept: the next summary lists it` -> "<rel>: <seen> after the summary - kept as it is; the next summary lists it."
- `already gone` -> "<rel>: was already gone."
- `waits for the fold` -> "<rel>: kept until its content is folded into the project profile."
- any other `kept: ...` -> "<rel>: could not be removed - kept as it is."
FR-6: the builder checks these sentences against `references/human-questions.md`; where a rule there demands another wording, the builder keeps the content, adjusts the words and names the change in the report. No sentence holds a script name or a plugin path.

**`main`** at :1880-1885: `drift = summary_drift(root, listing_given.get("retire") or [], made["retire"], I.load_table())`; refuse on `drift["refuse"]` exactly as today; then `apply(..., after_summary=[r for r in drift["settled"] if r["kind"] == "new"])` at :1892 (the listed rows are re-judged inside `apply` against the bytes at that moment; passing only `new` rows avoids a double row). `main` checks in every phase (as today); `apply` ignores `after_summary` in phase `early`.

Phase `early`: inside-home drift is neither refused nor acted on (early retires nothing, :1451-1460; the final half's own plan sees it again); `after_summary` is `[]`. Outside-home drift refuses in every phase (`main` checks before `apply`).

**`_retire`** (onboard_apply.py:1335-1396) gains two branches and a docstring clause:
- after the hook-written branch (:1354-1355) and before the link branch (:1356): `elif I.classify(rel, table=table)["class"] == "carried": row["result"] = "kept: the factory keeps it"` (an OLDER sealed listing that still names `reporter-rehearsals.json` for deletion never deletes it — twin of t-298, SIBLING_MAP:76);
- the sha comparison at :1358 is wrapped: an `OSError` from `I.sha256_file(path)` gives `row["result"] = "kept: cannot be read"` (no crash: today it would raise);
- docstring (:1337) "Retire what the sealed listing names" becomes "Retire what the sealed listing names, plus the rows the apply settled after the summary (each marked `after_summary`: the factory's own machine-local technical data, OH3-9)".

**`apply` docstring** (:1401-1409): the return keys gain `after_summary`; "a listed path's sha256 differs from the summary (C2)" becomes "a path OUTSIDE the factory's home that changed, became a folder or link, could not be read, or is new since the summary (C2; inside the home the apply settles such a file by its class and reports it in `after_summary`, OH3-9)".

**Module docstring** (onboard_apply.py:9-23): the invariant (:10-11) becomes "nothing is retired that is carried data, outside the project root, not in the approved listing, or changed by a person since the summary was made — except the factory's own MACHINE-LOCAL technical data (a delete-mode row the table calls machine-local) found new or changed under its home after the summary, which the apply deletes by its class and reports (owner, 22.10.2026; OH3-9)"; the second bullet (:15-17) "one difference refuses the whole apply" becomes "a difference OUTSIDE the factory's home refuses the whole apply, nothing written; inside it the file is settled by its class (`summary_drift`): machine-local technical data deleted, anything else kept and listed by the next summary"; the hook-written bullet (:18-23) unchanged except "sha recheck above" stays true.

**p4-generate.md §0 `final` bullet** (:27-33): the sentence "It reads every listed file again first; if one differs from what the summary showed it refuses, names the paths and writes nothing: make the summary again." is replaced by: "It reads every listed file again first. A file under `qa-factory/` that changed or appeared after the summary is settled by its class and named in `after_summary`: the factory's own machine-local technical data is deleted and named in the removal record; anything else is kept as it is and the next summary lists it. Only a path outside `qa-factory/` that differs from what the summary showed refuses the apply: it names the paths and writes nothing; make the summary again. Never ask the person what to do with a file under `qa-factory/`: relay the `after_summary` lines in the digest." The rest of the bullet (the running-session refusal, :33) is unchanged.

**SKILL.md ## Digest** (:130-138) gains one bullet after "Deferred items": "- **Factory files settled after the summary** — each `after_summary` line of the final apply half, as it stands; none -> no bullet."

### 4.3 Ways out (AR-25)

deleted -> named in the removal record (`retired/<date>/retire-record*.json`, onboard_apply.py:1385-1395, the row carries `after_summary: true`) and in `tracking.git_rm` when tracked (:1384); kept (move-mode, non-machine-local delete-mode, not a file, unreadable) -> the next install's summary lists it under the person's one "yes"; carried kept -> never retired; stale rehearsal proofs are re-proved by gate A on a `function_sha` mismatch (CHANGELOG.md:5487).

### 4.4 Positional invariant (rule 11(ii))

The partition sits where `_changed_since_summary` is called today — `main` after `plan` and its `blocked` refusal and before `apply` (:1876-1884); `apply` after the live-writer check (:1425-1427), the proposal-hash check (:1428-1429), the approval check (:1430-1434) and the answers check (:1435-1439), and BEFORE the first write (:1451). What must stay unreachable / refused:
1. any write before the live-writer, hash, approval and answers refusals (order unchanged);
2. a path outside the home that changed, became a folder/link, cannot be read, or is new since the summary refuses the WHOLE apply with nothing written (C2 kept for project files);
3. a carried path is never deleted or moved — whatever a listing says (the new `_retire` branch) and whatever a manifest says (install_paths.py:1026-1028);
4. a folder or a link is never retired;
5. an undetermined (move-mode) file is never moved unless a summary listed it with the bytes it has now;
6. the sealed proposal file and `proposal_hash` are never altered by the drift handling;
7. a hook-written file is never a drift row and never a refusal (t-298 unchanged);
8. **(M1, Lead 12.11.2026)** the after-summary road deletes ONLY a row that is delete-mode AND machine-local by the current table — the factory's own technical data in `state/` (`jira-probe-*`, the regenerated rows not rebuilt) and `qa-factory/readiness.json` (still behind its own guard :1350-1351). A row that is not machine-local or may carry a person's content (`qa-factory/strategy/product-passport.md`) is NEVER deleted by this road: changed after the summary it is kept byte for byte (`kept: changed since the summary`) and deleted only after a summary lists it with its current bytes (C2 for that file stays: listed in a summary first). Invariant: a file a person or the fold step may have edited is never removed unseen.

## 5. Item 4 — the eval row and the role rules

### 5.1 Eval 16

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

### 5.2 Two rows in `design/role-rules.json` (TESTING.md: no text pins; the registry is the guard, test_role_rules.py)

- `p4-no-question-about-factory-files` — rule: "The final apply half settles a file under qa-factory/ by its class and the role never asks the person about it." carrier p4-generate.md, anchor "Never ask the person what" (exact after the edit).
- `skill-digest-settled-files` — rule: "The digest relays every after_summary line." carrier SKILL.md, anchor "settled after the summary".

## 6. Item 5 — owns, tests, witness, quarantine, AR, FR

### 6.1 Owns and order against OF1-2

In the dispatch header (files + functions). Functions touched in onboard_apply.py: module docstring :9-23, `_changed_since_summary` :1275-1294 (removed), new `summary_drift`, new `_after_summary_line`, `_retire` :1335-1396 (docstring + two branches), `apply` :1399-1510 (docstring, signature, `out` init :1413-1414, :1440-1444, :1492-1495), `main` :1880-1885 (+ the `apply(...)` call at :1892 gains one keyword). Shared with OF1-2: onboard_apply.py, p4-generate.md (§0 bullet), evals.json (tail append). The order rests on the batch's dependency column (batch :68: OF1-2 depends on OH3-9) and on `docs/tasks/onboarding-streams-2026-11-12.md:26` (OH3-9 -> OF1-2). `apply` is possibly shared with OF1-2 item 4 (its finding :28-29 will likely touch the hash and approval refusals :1428-1434): OF1-2 merges `main` into its tree after OH3-9 and re-runs both nodes' pins (PROJECT.md «Командная работа» п. 3). No `очередь:` line is needed: that is a between-batch device, and both nodes are in one batch (t-170 m3).

### 6.2 Tests — one parameterised table per behaviour, rows not files (TESTING.md; no new test file)

**Table A — `test_install_paths.py` (keep, `data_join`; test-layers.json:2625): the basis rule.** New section `section_regenerated_basis` with one table `BASIS_ROWS = [(id, mutation, expected codes)]` run on a synthetic package `tmp_package({"scripts/reader.py": "x = 'alpha.json'\n", "scripts/other.py": "pass\n"})` and the base table `{"home": "qa-factory", "rules": [rule("qa-factory/state/alpha.json", "regenerated", rebuilt_by="reader.py", note="reader.py writes it again; its absence costs nothing")]}`; assertion `codes(r) == expected` (helper :209-210):
- `basis-rebuilt-by` -> `[]`;
- `basis-step-output` (drop rebuilt_by and note; `regenerate_step: [{"script": "reader.py", "outputs": ["qa-factory/state/alpha.json"]}]`) -> `[]`;
- `basis-hook-written` (drop both; `hook_written: True`) -> `[]`;
- `basis-lock-kind` (drop both; `lock_kind: "os"`, `retire_safe: False`) -> `[]`;
- `basis-discard-when` (drop both; `discard_when: {"json_field": "f", "differs_from": "package_fingerprint"}`, `retire_mode: "delete"`) -> `[]`;
- `no-basis` (drop both) -> `["regenerated_without_basis"]`, and the message names the glob and each of `regenerate_step`, `hook_written`, `lock_kind`, `discard_when`, `rebuilt_by`, `carried` (FR-1);
- `rebuilt-by-missing-script` (`"no_such.py"`) -> `["regenerated_without_basis"]`;
- `rebuilt-by-key-absent` (`"other.py"`) -> `["regenerated_without_basis"]`;
- `rebuilt-by-bad-shape` x {`""`, `7`, `"none"`, `"../x.py"`, `"scripts/x.py"`, `"a\\b.py"`} -> `["shape"]` (one id per value);
- `rebuilt-by-note` x {absent, `""`, `"   "`, `7`} -> `["shape"]`;
- `rebuilt-by-on-class` x {`carried`, `discarded`, `not_ours`} (class changed, rebuilt_by and note kept) -> `["shape"]`;
- `hook-written-not-bool-only` (drop both; `hook_written: "yes"`) -> `["shape"]`;
- `lock-kind-unknown-only` (drop both; `lock_kind: "nope"`, `retire_safe: False`) -> `["shape"]`;
- `discard-when-malformed-only` (drop both; `discard_when: {"json_field": 1}`) -> `["shape"]`;
- `shipped-instance-before` (on a deepcopy of the shipped `TABLE`, default package root: the carried reporter-rehearsals row replaced by the old row `{"glob": "qa-factory/state/reporter-rehearsals.json", "class": "regenerated", "machine_local": true, "reader": "gate_preflight.py"}`) -> `["regenerated_without_basis"]` — the defect, red before the fix.

Existing assertions changed in the same file (TESTING.md «Когда тест покраснел» 1; t-170 M2, M3):
- `section_validate` (:213-289): every regenerated fixture row gets a basis that adds no code — a local helper `def regen(glob, reader="reader.py", **kw): return rule(glob, "regenerated", reader, hook_written=True, **kw)` replaces `rule(..., "regenerated", ...)` at :218, :224, :228 (both rows), :231 (the third, alpha, row; the `(a, b)` pair rows stay as they are: their check is `in`), :233, :236, :244 (`alpha`), :268, :270, :272, :275. Legal shape: these synthetic tables carry no `regenerate_step`, so the step-output rule (:583) cannot fire, and no `retire_mode`/`discard_when` sits on them. The exact-code assertions :219, :237, :246, :252, :254, :258, :261, :269, :273 stay unchanged and green;
- `REGENERATED_UNBUILT` (:460-467) loses `reporter-rehearsals.json`, `benefit-inputs.json` and `coverage-map.receipt.json`;
- a new list `CARRIED_EVIDENCE = ["qa-factory/state/reporter-rehearsals.json", "qa-factory/state/benefit-inputs.json", "qa-factory/state/coverage-map.receipt.json", "qa-factory/state/reporter-unread/web/manifest.json"]` beside :470, seeded at :480, with one check in `section_regenerated_not_rebuilt` (:475-) "OH3-9: carried machine-local evidence is never in retire" -> `[p for p in CARRIED_EVIDENCE if p in retired] == []` (red before the fix for the first three);
- the regenerated loop :76-83 loses `coverage-map.receipt.json`;
- the Q7 check :559-562 loses `reporter-rehearsals.json` and `benefit-inputs.json` (`* 5` -> `* 3`); the carried machine-local check :563-565 gains `reporter-rehearsals.json`, `benefit-inputs.json` and `coverage-map.receipt.json` (`* 2` -> `* 5`; label: "carried machine-local evidence (transactions of a decision write, the denied dispatches, the rehearsal proofs, the benefit inputs, the coverage receipt)");
- `section_report_adaptations` (:759-785): the docstring (:760-761) says the kept unread report is CARRIED machine-local evidence (its absence costs a rehearsal run; owner 22.10.2026); :769-770 expect `("carried", True, "report_adapt.py")`; the negative control :781-783 is unchanged (without its row the file is unrecognised).
- The shipped-table checks (:51, :653, :677, :802) prove every row of §3.3 carries a basis.

**Table B — `test_install_retire.py` (keep, `detector`; test-layers.json:2643): what the apply does with drift.** The C2 section `stale_summary` (:434-465) and K-A5 (:1318-1333) become ONE table `AFTER_SUMMARY = [(id, entry, after-summary move, expected)]`, `entry` ∈ {`apply()`, `cli`}, world built by `old_project()` / `hook_project()` (the K-A5 world, which records the fold receipt, :1325-1326), `DISCARDED` from :48-50:
- `new-evidence-file` (cli `--phase final`; `reporter-rehearsals.json` written after the summary) -> exit 0, applied, file present byte for byte, no `after_summary` row for it — the incident (red before the fix: refused);
- `older-listing-names-evidence` (apply() and cli; a proposal sealed under a table copy where row :112 is the old regenerated row, the same pattern as K-A6 :1335-) -> applied, file present, `_retire` result `kept: the factory keeps it`;
- `new-discarded-file` (`qa-factory/state/jira-probe-x.json` appears after the summary) -> applied, deleted, removal-record row with `after_summary: true`, one `after_summary` row `kind new`, `result deleted`, a `line`;
- `listed-discarded-changed` (`DISCARDED[0]`, machine-local jira probe, changed; apply() and cli) -> applied, deleted, row `kind changed`, `result deleted` (was: refused);
- `listed-tracked-discarded-changed` (M1; `DISCARDED[2]` = `qa-factory/strategy/product-passport.md`, fold receipt recorded, changed after the summary) -> applied, the file byte for byte with the NEW bytes, row `kind changed`, `result "kept: changed since the summary"`, the line says it is kept and the next summary lists it;
- `new-tracked-discarded` (M1 neighbour; the passport absent at the summary, written after it) -> applied, file present byte for byte, row `kind new`, `result "kept: the next summary lists it"`;
- `listed-became-folder` (`DISCARDED[1]` replaced by a folder) -> applied, folder kept, row `kind not_a_file`;
- `listed-unreadable` (m5; `I.sha256_file` wrapped by the test to raise `PermissionError` for `DISCARDED[0]` only, restored in `finally`) -> applied, file present, row `kind unreadable`, result `kept: cannot be read`, no traceback;
- `new-unrecognised-file` (`qa-factory/my-notes-2.md` after the summary) -> applied, file in place, row `kind new`, result `kept: the next summary lists it`;
- `listed-unrecognised-changed` (the unrecognised file `old_project()` holds, listed move-mode, changed after the summary) -> applied, file in place byte for byte, row `kind changed`, result `kept: changed since the summary`;
- `outside-listed-changed` (`--also-retire docs/old.md` listed, then changed) -> exit 1, `changed_message` names it, snapshot unchanged — the invariant control;
- `outside-new-candidate` (`--also-retire docs/old.md` given only at apply) -> refused, nothing written;
- `outside-unreadable` (as `listed-unreadable` but on `docs/old.md`) -> refused, nothing written;
- `phase-early-inside-drift` -> no refusal, nothing retired, `after_summary == []`;
- `nothing-to-do-has-key` (m1; the K8 world :428) -> `"after_summary" in out` and `out["after_summary"] == []`;
- every `line` and every refusal holds no `.py` and no `scripts/` (today's :448 row, kept).

Home-membership sub-table on `install_paths.in_home` (input from outside: project paths and `--also-retire`), placed in Table A's file next to `section_glob_and_path_rules`: `qa-factory/state/x.json` True; `qa-factory` True (the home itself, scan_tree's rule :1126; a listed home is a folder -> `not_a_file` keep); `qa-factory-old/x` False; `qa-factory.bak/x` False; `qa-factory./x` False and `qa-factory /x` False (Windows strips trailing dots and spaces, so these name the home on disk; treating them as outside refuses — the safe direction, pinned, t-170 m7); `QA-Factory/state/x.json` True with `fold=True`, False with `fold=False`; `./qa-factory/x` True; `qa-factory\\state\\x` True; `qa-factory/../src/x` False (does not normalise); `""` False; `C:/x` False; `7` False.

**`test_reinstall_equals_fresh.py`** (keep, `gate_named`, test-layers.json:4259): `coverage-map.receipt.json` moves from `REGEN_UNBUILT` (:68-70) to `MACHINE_LOCAL_KEPT` (:109-111); the fixture holds the file (`fixtures/old-generation-project/qa-factory/state/coverage-map.receipt.json`, Glob), `EXTRAS` covers it by derivation from the carried machine-local rows (:119-128), and the byte check :358 then proves it is kept. Nothing else.

**`test_role_rules.py`** (keep, `register`, :4479): no edit; it reads the two new registry rows.

**`test_judgment_census.py`** (keep, `register`, :2705): no edit to the test; rows added to `fixtures/judgment-census.json` only where the test demands them, in the file's form (`{"file", "function", "class", "roles": ["conductor"], "owner": "data"}`, e.g. :419-423): expected `install_paths.py` `_basis_errors` `xref` and `onboard_apply.py` `summary_drift` `xref`; a row for `_changed_since_summary` is not needed (none exists today, and the function is removed). Each raise named in the report (AR-20). Both worlds: if the test demands no row for a unit, none is added.

The eval row is a skill eval, not a test (no runner in `scripts/tests` reads id 16).

### 6.3 Quarantine check (read from `scripts/tests/test-layers.json`; `quarantine` starts at :6966)

| file | section | where |
|---|---|---|
| test_install_paths.py | keep (`data_join`) | :2625 (only occurrence) |
| test_install_retire.py | keep (`detector`) | :2643 (only occurrence) |
| test_reinstall_equals_fresh.py | keep (`gate_named`) | :4259 (only occurrence) |
| test_role_rules.py | keep (`register`) | :4479 |
| test_judgment_census.py | keep (`register`) | :2705 |

Positive control of the read: the same Grep found `quarantine` at :6966 and the quarantined `test_acceptance_semantics.py` at :6967; none of the five names occurs after :6966. None of the five is slow (PROJECT.md «Как принимается изменение пакета» п. 2 list).

### 6.4 DoD (inline; the builder's verification run)

Acceptance criteria:
1. install-paths.json: the four rows of §3.4 are carried machine-local in the carried block; every regenerated row carries the §3.3 basis, every `rebuilt_by` row its §3.3 note; the description at :3 carries the three sentences of §3.1 and §3.4.
2. `validate_table` refuses a regenerated row without a basis (`regenerated_without_basis`, the §3.1 messages) and every bad `rebuilt_by`/`note` shape (`shape`, one per row); `rebuilt_by` is resolved through `_reader_path`/`_read_lower`, never `_corpus`; the shipped table validates.
3. `summary_drift` is the one drift function, called by `main` and `apply`; `_changed_since_summary` is gone; behaviour per §4.2; invariants §4.4 1-8 hold; `apply` returns `after_summary` (a list) on every return.
4. `_retire` keeps a path the current table calls carried, and keeps an unreadable file.
5. p4 §0 bullet and SKILL Digest per §4.2; two role-rules rows; eval 16 appended.
6. FR walk A-G in the report (§6.6); AR lines (§1.1) in the report and commit (`architecture:` and `judgment:` lines).
Verification run (output verbatim in the report):
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for references/install-paths.json scripts/install_paths.py scripts/onboard_apply.py scripts/tests/test_install_paths.py scripts/tests/test_install_retire.py scripts/tests/test_reinstall_equals_fresh.py scripts/tests/fixtures/judgment-census.json design/role-rules.json skills/qa-onboarding/evals/evals.json skills/qa-onboarding/phases/p4-generate.md skills/qa-onboarding/SKILL.md`
then `python -B ai-packages/qa-factory/scripts/tests/<file>` for each keep file it prints (expected at least: test_install_paths.py, test_install_retire.py, test_reinstall_equals_fresh.py, test_role_rules.py, test_judgment_census.py) — never a quarantined file, never a slow one (CI judges those); then `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. A path for which the command prints no row: the report says so and names the test file run for it.
`docs/SIBLING_MAP.md` (outside the package, no test): doc-dispatch witness per CLAUDE.md rule 11 — key quoted verbatim before the run ("a path the current table calls carried is kept"), the script in full in the report, plus a negative control.

### 6.5 Siblings walked (rule 9)

SIBLING_MAP:76 — the new `_retire` "carried now" branch is the twin of the hook-written narrowing; the row gains one clause naming it. Axis 34 — home membership from the table's `home` through `in_home`; no language, project or case branch. Same artifact (`install-paths.json`): every regenerated row enumerated in §3.3 (four reclassed, the rest given a basis); the delete-mode rows outside `state/` walked for M1 (:122 machine-local, still behind :1350; :123 not machine-local, never deleted after the summary). Same function (`onboard_apply` refusals whose door is a person's move): not walked — stated scope, a scout question for the Lead if wanted (t-170 class completeness). Other callers of `scan_tree(..., retire_unbuilt=True)`: only `plan` (onboard_apply.py:928, t-170 Key 1); the builder confirms with a positive-controlled grep and reports.

### 6.6 FR walk A-G (to be answered by the builder's report; designer's expectation)

- A: FR-3 — the factory's own files are reported (`after_summary`), not put as a choice; FR-1/FR-2/FR-57 — the outside-home refusal keeps its text and door, the new `regenerated_without_basis` message says what, why and how; FR-4 — n/a (no informed pass); FR-48 — the conductor is not involved; FR-5, FR-46, FR-50 — n/a.
- B: FR-6 — every `line` and the Digest bullet follow `references/human-questions.md` (no script, no plugin path); FR-10 — p4 §0, SKILL Digest and eval 16 say the same thing; FR-7/8/9 — n/a.
- C: FR-13 — class, basis, note and home are data; FR-14 — `after_summary` on every return, `summary_drift` always the same keys; FR-38 — the table requirement is stated in the table's description before anyone writes a row; FR-49 — apply's rows reach the digest whole; FR-12, FR-15, FR-39, FR-42, FR-56, FR-11 — n/a (one line each).
- D: FR-40 — every outcome has a way out (§4.3); FR-59 — an unknown (not normalising, unreadable outside) refuses, unreadable inside keeps (declared safe default); FR-17 — one drift function wired at both sites; FR-16, FR-18, FR-58 — n/a.
- E: FR-37 — every path in a `line` is the path the code deleted or kept; others n/a.
- F: n/a — no money and no measurement changed.
- G: FR-30 English, no Cyrillic; FR-32 root cause + table rows; FR-33 — the role behaviour (no question) is proved only by a live onboarding: one row for the pile `live-runs` (PROJECT.md «Командная работа» п. 9); FR-47 — code settles data, the role relays; FR-54 — §6.5; FR-29, FR-31, FR-43, FR-44, FR-45, FR-52 — n/a.

## 7. Edges (each with the invariant it protects)

| edge | behaviour | invariant |
|---|---|---|
| E1 empty drift | `after_summary: []`, no Digest bullet | a report never invents a settled file |
| E2 no cap | every settled row is listed (no group of the listing is cut, onboard_apply.py:1044-1049) | nothing the factory did is unreported |
| E3 `--apply` without a sealed proposal (`listing_given is None`, :1881) | no drift check, as today; `after_summary=[]` passed | unchanged road |
| E4 delete row vanished before `_retire` | result `already gone` (:1352-1353) | no error for a file that left by itself |
| E5 new delete-mode file with `requires: ["fold_receipt"]` | not machine-local (the passport) -> kept, never reaches `_retire`; a machine-local one would keep its `requires` and `waits for the fold` without the receipt (:1348-1349) | a requirement of a row is never skipped by the after-summary road |
| E6 TEMPORAL — table before/after this node | this commit creates `rebuilt_by`, `note` on those rows and the four carried rows; before it no row carries `rebuilt_by` and the shipped table validates; after it every regenerated row carries a basis and the shipped table validates (:51) | the shipped table always validates |
| E7 TEMPORAL — a proposal sealed by an older package (row :112 regenerated) applied by this one | `_retire` keeps the file (`kept: the factory keeps it`); `summary_drift` skips it (carried now) | a carried path is never deleted, whatever an older listing says |
| E8 TEMPORAL — an old manifest naming reporter-rehearsals.json `regenerated` machine-local | kept; the entry is carried forward with its old label | a manifest's word never retires a carried or machine-local path (install_paths.py:1166-1168, 1026-1028) |
| E9 path under the home that is a symlink/junction to outside | plan refuses links (:960-961); `summary_drift` gives `not_a_file`, `_retire` keeps them (:1356) | nothing outside the root is touched |
| E10 a path matched by a carried and a regenerated row | carried (precedence, install_paths.py:450) | carried wins |
| E11 conflict: owner's "not needed -> deleted" vs C2 "nothing retired that the summary did not list" | the owner's word for delete-mode MACHINE-LOCAL factory data inside the home (F-3 A as bounded by M1); C2 stays for project files, undetermined files and non-machine-local rows | a person's possible file is never removed unseen |
| E12 conflict: "never ask" vs the outside-home refusal | the refusal outside the home stays: that is the person's project file | the person decides only about their project files |
| E13 phase `early` | inside drift ignored (`after_summary: []`), outside drift refused | early retires nothing |
| E14 (M1) a delete-mode row that is NOT machine-local (`strategy/product-passport.md`) changed or appeared after the summary | kept byte for byte, row in `after_summary` (`kept: changed since the summary` / `kept: the next summary lists it`); deleted only after a summary lists it with its current bytes | a file a person or the fold step may have edited is never deleted by the after-summary road (Table B `listed-tracked-discarded-changed`, `new-tracked-discarded`) |
| E15 (m5) a listed or new file inside the home that cannot be read | `kind unreadable`, kept, a line; `_retire` gives `kept: cannot be read`; outside the home: refuse | an unread file is never deleted and never crashes the apply; an unknown outside never passes |
| E16 (m1) `nothing_to_do` return and the `blocked` raise | `out` carries `after_summary: []` from its first literal (:1413-1414), so the early return (:1418-1419) has it; a raise returns no `out` | FR-14: one output shape on every return |
| E17 a listed item without `retire_mode` | treated as not delete -> kept | a missing mode never deletes |
| E18 trailing dot/space in the home segment (`qa-factory./x`) | outside -> refuse | an unproven home membership never deletes |

## 8. Forks

Closed by the Lead 12.11.2026 (recommendations taken; their text is folded into the body above): F-1 A (per-row basis rule, `rebuilt_by` with a declared meaning), F-2 a/b/e (reclass carried machine-local), F-2 c and d (keep regenerated with `rebuilt_by`; d's residual cost written into the notes), F-3 A (delete after the summary — bounded by M1 to machine-local delete-mode rows, Lead 12.11.2026), F-4 A (undetermined: kept with a line), F-5 A (code writes the line once).

**F-6 (new, t-170 M4) — where the honesty of `rebuilt_by` is judged, so a small table diff cannot skip it.** In this node's owns: the data layer — a `rebuilt_by` row must carry a non-empty `note` (presence, AR-29-clean; §3.1). Outside the owns (mechanism changes, Lead-tier):
- A (recommended): a Lead node that (1) appends to `docs/tasks/critic-diff-brief.md` standing question 11 (JUDGMENT) the clause "a diff that adds or changes a `rebuilt_by` or reclasses a row out of `carried` in `references/install-paths.json`: the critic judges the row's `note` claim (no test run, no money, no question) against the named script", and (2) registers a calibration check in `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md`: `git log -G '"rebuilt_by"' -- ai-packages/qa-factory/references/install-paths.json` over the week; every such commit has an `accepted` event with critic input (not "critic: skipped"). Cost: one clause, one check, a few minutes per calibration; no new code.
- B: a code ratchet — a pinned list of `rebuilt_by` globs in a test, so any addition shows as a test edit. Cost: a text pin TESTING.md discourages; it shows the change but judges nothing.
- C: data only (the `note`), no registered judge. Cost: the M4 hole stays — a one-line table edit can still pass with "critic: skipped", and F-3 A now deletes after the summary what such a row misclassifies.
The node is executable under A without waiting: the builder writes the `note` rule; the Lead opens the A node.

## 9. Small choices closed by the designer (no design weight)

- S-1: `_changed_since_summary` is removed; both sites call `summary_drift` (t-170 Key 1: exactly two call sites, onboard_apply.py:1442 and :1882). If the builder's positive-controlled grep finds another caller, it keeps a one-line wrapper returning `summary_drift(...)["refuse"]` and reports it.
- S-2: a missing or key-less `rebuilt_by` script is reported under `regenerated_without_basis` with a message that says which; shape errors stay `shape`.
- S-3: `_manifest_entries` is not touched (old manifest labels are harmless, E8; it is OF1-2's neighbourhood).
- S-4: `rebuilt_by` holds a script NAME under `scripts/` only: a rebuilder is code, never a role text.
- S-5: the reclassed rows move into the carried block (order inside a class matters only for "first row of a class wins", which these rows do not overlap).
- S-6: the changelog fragment is one paragraph in English under `changelog.d/`.
- S-7: `in_home` counts the home itself as inside, matching scan_tree's inline test (install_paths.py:1126), so a later node can merge the two without a behaviour change; a listed path equal to the home is a folder and is kept as `not_a_file`.
- S-8: `_basis_errors` skips a row that already has a `shape` error (one error per row, t-298 convention :572-573); the row is refused either way.
- S-9: `retire_mode` for the drift action is read from the listed/planned ITEM (scan_tree sets the class's mode, install_paths.py:1097, :1111-1112, :1123-1124), `machine_local` and the carried/hook-written skip from `classify` on the CURRENT table.
- S-10: `main` passes only the `new` rows to `apply`; listed rows are re-judged inside `apply` against the bytes at that moment (no double row).

## 10. Contradictions and analogs noticed (reported, scope not widened)

- The finding cites `install-paths.json:103` and `gate_preflight.py:495-502`; the carriers today are install-paths.json:112 and gate_preflight.py:865 / :3319.
- The brief's item 2 wording (F-1 B) and the finding's ("без явного основания", F-1 A) differ — closed F-1 A.
- The live run of 0.11.0 (batch file :74) shows the defect recurring after the finding.
- **Two analog findings — filer named (t-170 m6):** the Lead of the pile files each as a `findings/` file plus a row in the unfrozen batch of its pile in ONE move (PROJECT.md «Командная работа» п. 2), at acceptance of this spec and before the builder dispatch: (1) AR-22 — `benefit-inputs.json` has a reader (metrics_projection.py:668) and no producer in the package; (2) AR-28 — an absent `coverage-map.receipt.json` makes `check_coverage.py` skip the binding check silently (:260-274) on a fresh project; reclassing it carried does not cure that. Neither is left as "queued".
- Duplication analog: scan_tree's inline home test (install_paths.py:1126) and the new `in_home` — one survivor later (AR-15); scan_tree is a non-goal here.
- The incident's question came from no phase line: the role improvised on a refusal whose door is a person's move. Other refusals of `onboard_apply` with a person-facing door were not walked (scope).

## 11. Reading trail

Attempt 1 (designer): the finding (all); install-paths.json (all); install_paths.py :1-1213; onboard_apply.py :1-135, :494-533, :839-1040, :1270-1519, :1775-1913; p4-generate.md :10-49, :636-675; SKILL.md :120-145; evals.json :1-60, :270-293; test_install_paths.py :1-110, :420-820; test_install_retire.py :430-475, :1295-1340; test_reinstall_equals_fresh.py :60-75; test-layers.json :2620-2664, :4255-4274, :6960-6974; architecture.md :134-293; TESTING.md; exit_gate.py :170-209; check_coverage.py :195-279; host_probe.py :1-40, :575-604; project_decisions.py :340-369; package Greps for the evidence file names (negative "no writer" for benefit-inputs with positive control); judgment-census.json, role-rules.json Greps; scenario_walk.py :887-931; builder-rules.md :16-20; SIBLING_MAP.md :76, :582; batch file :30, :68, :74.
Attempt 2 (this fix round), read again for every claim this round makes: t-170 verdict (all); install-paths.json (all, :1-135); install_paths.py :84-153 (`normalize_rel`, `_key`, `sha256_file`), :404-465 (`classify`: `retire_mode` is the winning row's own, :455), :466-795 (`_key_of`, `_reader_path` :480-481, `_read_lower`, `_corpus`, `_step_outputs`, `_shape_errors` :528-644, `_layout_errors`, `validate_table` :697-785), :1095-1134 (scan_tree retire items carry the class's mode; inline home test :1126); onboard_apply.py :1-41 (module docstring), :1270-1519 (`_changed_since_summary`, `changed_message`, `_retire`, `apply`), :1868-1892 (`main`); test_install_paths.py :40-289 (fixtures and `section_validate`), :290-591, :594-736 (K-A2 exact `["shape"]` at :663 — drives S-8), :752-791; test_install_retire.py :48-50 (`DISCARDED`), :79-86, :239, :425-472, :1259-1339; test_reinstall_equals_fresh.py :50, :60-148, :703-727 and a Grep of `MACHINE_LOCAL_KEPT|REGEN_UNBUILT` (:84, :310, :332, :358); Glob of `fixtures/old-generation-project/qa-factory/state/*` (receipt present); test_cost_capture_start_turn.py :96-111 (its `reporter-unread` is a task-path test, not a class pin); package-tests Grep of `REGENERATED_UNBUILT|REGEN_UNBUILT|reporter-unread|benefit-inputs|coverage-map\.receipt|reporter-rehearsals` and of `validate_table\(` (callers: test_collect_pack.py:121, test_evidence_not_delivered.py:275, test_exploration.py:549, test_install_paths.py, test_reinstall_equals_fresh.py — all on the shipped table or with `in`/`ok False` checks except the section_validate rows handled in §6.2); judgment-census.json :414-425, :576-585; p4-generate.md :25-34; SKILL.md :128-139; Greps of `OH3-9` in the batch file (:30, :68, :74) and in docs/tasks/onboarding-streams-2026-11-12.md (:26); critic-diff-brief.md headings and standing-question numbers (1-12; 11 = JUDGMENT, :67).
Not read: `references/human-questions.md` (the builder reads it for the `line` texts; it is in `given`).

## 12. Fix round t-170 — change list

| t-170 item | what it asked | resolution |
|---|---|---|
| M1 | bound F-3 A deletion to machine-local rows | fixed (Lead decision): §4.2 action table (`delete` only when the item's `retire_mode == "delete"` AND current `machine_local`), §4.4 invariant 8, edge E14, module docstring text, Table B rows `listed-tracked-discarded-changed` and `new-tracked-discarded`; neighbours walked in §6.5. Kept (not refused) per the t-170 fix text, so "never ask" holds for the person's tracked file too |
| M2 (a) | decide the `section_validate` fixture fallout | fixed: `regen()` helper with `hook_written=True` on the named lines; exact-code assertions listed and unchanged (§6.2) |
| M2 (b) | where `rebuilt_by` is resolved | fixed: `_reader_path` + `_read_lower` under `package_root`, never `_corpus` (§3.1 basis 5) |
| M3 | fold closed forks into unconditional text; full flip list; numbering | fixed: §3.3/§3.4 unconditional (four rows reclassed, the rest given a basis); flip list in §6.2 (REGENERATED_UNBUILT loses three; Q7 loses two; loop :76-83 loses the receipt; report_adaptations incl. docstring; reinstall_equals_fresh moves the receipt to `MACHINE_LOCAL_KEPT`); eval 16 F-3 A text only; sections renumbered §1-§12 (eval and role rules are §5.1/§5.2; owns/tests are §6) |
| M4 | register the detector for `rebuilt_by` honesty | fixed in owns: `note` required on a `rebuilt_by` row (§3.1 shape rule, Table A `rebuilt-by-note`), every note written in §3.3; the judgment's registration returned as fork F-6 with recommendation A (critic-brief clause + calibration check, a Lead node); node executable under A |
| m1 | `after_summary` on the `nothing_to_do` return | fixed: init in the first `out` literal at :1413-1414 (the actual lines; t-170 cited :1410-1411/:1416), E16, Table B `nothing-to-do-has-key` |
| m2 | owns ranges | fixed: module docstring 9-23; `apply` docstring :1401-1409 and `_retire` docstring :1337 in owns with their new text (§4.2) |
| m3 | OF1-2 order rests on the dependency column and streams file | fixed: §6.1 (batch :68, streams :26; `apply` possibly shared; OF1-2 merges and re-runs both pins; no `очередь:` line) |
| m4 | F-2 d residual cost in the two notes | fixed: §3.3 notes of :103 and :115 |
| m5 | unreadable listed or new file | fixed: `unreadable` kind (keep inside, refuse outside), `_retire` catches `OSError` -> `kept: cannot be read`, E15, Table B `listed-unreadable` and `outside-unreadable` |
| m6 | name who files the two analog findings | fixed: §10 — the pile's Lead, findings file + batch row in one move, at acceptance, before dispatch |
| m7 | trailing dot/space home rows | fixed: home-membership sub-table rows `qa-factory./x`, `qa-factory /x` -> False (refuse), E18 |
| m8 | drop the "31 rows" count | fixed: §6.5 says "every regenerated row enumerated in §3.3" |
| Key 4 (error direction note) | say `validate_table` runs only in tests | fixed: §1.2 row 1 |
| Key 2 F-2 d (critic's answer: a paused story CAN be reinstalled under) | — | taken: rows stay regenerated with the residual cost in their notes (m4) |
| found in this round (not in t-170) | K-A2 test_install_paths.py:654-663 asserts exactly `["shape"]` for a non-bool `hook_written` on `dashboard-dirty.json`, whose only basis is the flag — the new code would add `regenerated_without_basis` | fixed: S-8 (`_basis_errors` skips a row with a shape error) |
| found in this round | `classify` returns `retire_mode` None for a regenerated row without its own mode (install_paths.py:455), so "class now, retire_mode delete" would never delete a regenerated leftover | fixed: S-9 (mode from the item, `machine_local` from `classify`) |
| found in this round | `_retire` calls `I.sha256_file` unguarded (onboard_apply.py:1358): an unreadable listed file would crash the apply | fixed: §4.2 `_retire` branch |
| found in this round | duplicate home test (scan_tree :1126) | reported as analog §10; `in_home` matches its semantics (S-7) |

Open forks: F-6 only, with recommendation A.
