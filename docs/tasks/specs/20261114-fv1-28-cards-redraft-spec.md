# Spec redraft — FV1-28 builder cards after the plan critic (t-762)

Pile `live-run-fvf`, batch 1, node FV1-28 (P1). Designer redraft t-762, 14.11.2026, for Lead acceptance. Sources: the first draft
`docs/tasks/specs/20261114-fv1-28-first-look-to-automator-spec.md` (t-749, called "the draft"), the plan critic
`docs/tasks/specs/reviews/20261114-fv1-28-plan-critic.md` (t-755, "the critic"; §B 1-16 and §D binding), the Lead's brief of t-762
(decisions 1-4 final). Forks F-1..F-7 of the draft are CLOSED by the Lead (decision 1) and are not reopened; §6 holds only NEW forks.
The owner's three words and the facts the draft and the critic measured are not repeated here unless a card rests on them; each card
names its carrier.

## Where the code was read (freshness, rule 3)

- `C:\QAFactory\forge-repo\.claude\worktrees\read-main` HEAD = `ba903eb38a9e8f07dcb6c6fc3c0715045397c36e` (read from
  `.git\worktrees\read-main\HEAD`). `origin/main` = `1a00352c0460f3619af8503c6dde805a9ada76c6` (`.git\refs\remotes\origin\main`
  and `FETCH_HEAD`). **read-main is BEHIND origin/main.** This session has no git command, so the per-file difference between
  `ba903eb` and `1a00352` is NOT established. The critic measured at `7379e0d` that among the node files only
  `driver_stage_plan.py` differs (+51 lines, `register_gap_rows`); main has moved again since. Therefore **every code citation below
  is a FUNCTION NAME, never a line number**, except where a line number is quoted from the critic and marked so.
- The root checkout was not read for code (memory note: it is stale).

## §A Amendment map (completeness criterion)

| # | Amendment (critic §B) | Where it lands | Note |
|---|---|---|---|
| 1 | new card A2: survey walk opens on an unknown runtime provenance | card A2 (whole) | which unknowns open is stated by FIELDS; the "no probe registered" case is fork F-9 |
| 2 | A1 evidence through `capture_cited` with quote and item | card A1, item 2 (`evidence`, `quote`, `req` all required) | `capture_cited(task_root, walk, item, path, quote, stand)` read in `walk_session.py`; empty quote refused there |
| 3 | A1 secret guard: `tokens=False`, whitespace-normalised, literal account values, `actor`, class safety | card A1, item 3 (`sign_in_secret_faults`) and §1 census | one guard reused by C1 (AR-15) |
| 4 | C1: no registry write when every row is `blocked_by: access` | card C1, `record_sign_in` step 3 | |
| 5 | B1: no count cap only for `s5_kind == "window"` | card B1, item 3 | plan / legacy / unknown keep `FIRST_LOOK_LINES_MAX` and `+N more` |
| 6 | F-4: the story's OWN `sign_in` in its S3-S7 and walker briefs; B2 lists other stories only | card B1, item 6 (own); card B2, item 1 (other stories; a row whose `story` is this story is skipped) | B1 depends on A1's `read()["sign_in"]`: fork F-8 |
| 7 | last clause per reader; no script named for a shell-less role; B2's cut names the registry file | card B1, item 4 (`FIRST_LOOK_GAP_CLAUSE` data dict); card B2, edges | S5 gets the "name it as a gap" clause until FV1-29 flips its entry (seam) |
| 8 | C1: `SIGN_IN_KEY` branch before the role rules; ONE write function for both roads; `phases/s3.md` names it | card C1, items 2, 4, 5, 6 | the one function is `first_look.record_sign_in`; the acceptance reader moves to `first_look.accepted` (AR-13 kept) |
| 9 | D1: http way = `environment.access`-shaped object, run through FV1-17's roads; ui-only never a pass | card A1 item 2 (the `http` surface carries `access:` checked by `config_contract.access_errors`); card D1 (WAITING) | the shape is fixed in wave 1 so wave 3 can run it |
| 10 | D1: a recorded way that fails names `PK-n` and the revoke door, in the probe line and the S0/S5 warning | card D1, item 3 | |
| 11 | one precedence order beside `project_knowledge.sign_in`, read by D1 and FV1-28e | card C1, item 3 (`SIGN_IN_PRECEDENCE`); card D1; node FV1-28e | the "project" level is `environment.access` for http readers and `manual_capture.login.ui` for ui readers (closed choice C-4) |
| 12 | F-7: the `first_look/empty` seed = all rows `unreachable`/`access` with a capture through `first_look.put` | §3, dry rows | |
| 13 | SIBLING_MAP axis 5 row «How the stand logs in» names the new carrier in the C1 commit; §5 fixes axes 5/6/34 and drops axis 37 | card C1 owns `docs/SIBLING_MAP.md` (that row only); §5 | **"drop axis 37" NOT applicable:** read-main has 37 axes (heading `## Axis 37 — A repeat stop` at line 620; command and control in §5). The critic counted the root checkout, which has 36 (stale local main). §5 enumerates 1-37 |
| 14 | §3 names the departure from finding item 2's «`no_stand` только когда роль не смогла дойти» | §3, first row | |
| 15 | tests: scenario row in `test_first_look_step.py`; one parameterised `sign_in` table; one data-join row per producer -> reader | every card's DoD; §7 test-file check | |
| 16 | §0: refresh `driver_stage_plan.py` refs, "6144 tokens" -> bytes, F6 scope | "Where the code was read" (function names only); §0 F15', F6' | |
| §D | B2 and the app card "Sign-in" section must not render the same fact twice and disagree | card B2, item 2: **ONE carrier = the brief lines of `brief_pack.sign_in_lines`**; the app card does not render a recorded way, it says only that one exists and that it comes first | why this carrier: card B2 |

## §0 Facts the cards rest on (read on read-main `ba903eb`, function names)

| # | Fact | Carrier |
|---|---|---|
| F7' | `first_look.due` returns `(False, "no_stand", ...)` when `pipeline.environment` is empty OR `pipeline.environment_pending` is true; the check sits after `parks_after_s5`, the register-unreadable and empty-register checks, and before the attempt check | `scripts/first_look.py` `due` |
| F9' | A survey walk's open runs `Walk._open_actors` -> `MC.stand_probe(self.sink, ..., "start", ...)`; an `EnvBlocked` becomes `ServerDead`; the close runs the same probe at `"end"` in `Walk._shutdown` and writes an `env_blocked` row into every item attempt when it fails. These are the only two `stand_probe(` calls in `walk_session.py` (Grep `stand_probe\(` over `scripts/*.py`: 7 hits; positive control: the definition in `manual_capture.py` is among them) | `scripts/walk_session.py` `Walk._open_actors`, `Walk._shutdown` |
| F9'' | `manual_capture.stand_probe` refuses every record `profile_contract.acceptable_provenance(value, ACCEPTS, task=story)` refuses; `ACCEPTS = ("matched", "person_confirmed", "not_applicable:no_changed_file")`; the refusal is built by `_stand_blocked(profile, when, record, said, story, other_profile)`, which reads FIELDS (`stand_runs_other_build`, `content_differs`, `reason_code` NO_EXPECTED_REVISION / DEVICE_UNREADY, a person word for another story, `asks_person`) but does NOT attach the record to the `EnvBlocked` it returns. `EnvBlocked.row` holds `probe_line`, `remedy`, `owner`, `do_not_retry`, `cause` only | `scripts/manual_capture.py` `stand_probe`, `_stand_blocked`, `EnvBlocked`; `scripts/profile_contract.py` `ACCEPTS`, `acceptable_provenance`, `validate_runtime_provenance` |
| F9''' | `runtime_probe` sets `asks_person` (`how` or `confirm`) on an `unknown` whose stand answered but whose build could not be read or tied; an `unknown` from docker that did not answer carries NO `asks_person` ("E17: no question") | `scripts/runtime_probe.py` module docstring rungs 3 and 8; `confirmed_by_row`, `finish_unknown` |
| F10' | `walk_session.capture_cited(task_root, walk, item, path, quote="", stand="")`: the capture must be under `work/evidence/manual/survey-<item>/<attempt>/` of THAT item's attempt, listed in its `captures.jsonl`; an empty quote is refused ("nothing is quoted") | `scripts/walk_session.py` `capture_cited` |
| F11' | `app_card.scrub(text, tokens=True)` first folds whitespace (`" ".join(text.split())`); `tokens=True` replaces any letters-and-digits run of 24+ characters (`_LONG_MIXED`); `_KV` catches only `password: x` / `password is x` forms | `scripts/app_card.py` `scrub`, `_KV`, `_LONG_MIXED` |
| F12' | `config_contract.access_errors(access)` validates an `environment.access` object; `ACCESS_KINDS = ("harness_command", "local_login", "oidc_password", "bearer_env", "none")` on read-main (`form_login`, `ui_only` arrive with FV1-17, spec-only); every `*_key` must match `KEY_NAME_RE` (a variable NAME) | `scripts/config_contract.py` `access_errors`, `ACCESS_KINDS`, `KEY_NAME_RE` |
| F13' | `project_knowledge.record_problems` has a `LESSONS_KEY` branch placed BEFORE the role rules with the comment "a lesson subject never meets them, and a role key never skips them"; `record` refuses a no-trace story through `_refuse_no_trace`; the same live state AND value is the existing row (`created` False); `revoke(root, pk_id, words)` exists | `scripts/project_knowledge.py` `record_problems`, `record`, `_refuse_no_trace`, `revoke`, `lessons` |
| F14' | The driver's acceptance reader `_first_look_accepted` reads `FL.read_attempt`, `FL.read` and `self.controller_state()["dispatches"][dispatch]["status"] == "accepted"`; `controller_state` reads `state/controller.json` (`driver_core.py`) | `scripts/driver_stage_plan.py` `_first_look_accepted` (read-main; the function name holds on main per the critic) ; `scripts/driver_core.py` `controller_state` |
| F15' | `role-load.json` `allowances.brief` is 6144 **bytes** (the draft said tokens; the critic corrected it); the brief is outside U/H | critic Key 2, F15 row |
| F6' | No real S5 brief of a run is IN THE REPO; the ARM story folder outside the repo holds `LOCAL-1/work/briefs/S5-qa-automator-1..9.md` (11,470-20,678 B, critic Key 7) | critic Key 2, F6 row |
| F16' | The skill road of the first look is `skills/qa-story/phases/s3.md` (line 12 summary and section "First look"); it has no command after an accepted dispatch today | `skills/qa-story/phases/s3.md` |
| F17' | The app card is built only for S6 walk lanes (`driver_dispatch.py` calls `app_card.py build` before an S6 walk); its "Sign-in" section renders `manual_capture.login_recipe(cfg, spec, "ui")` (route, field selectors) and whether gate A proved it | `scripts/app_card.py` `_signin`; `scripts/driver_dispatch.py` (the S6 walk lane function) |
| F18' | Census ratchet ceilings on read-main: `safety: 86`, `blocking_per_role.qa-runner: 160`, `conductor: 764`; "Ceilings only go down"; `tools/architecture_gate.py` lets a raise of `safety` or `blocking_per_role.*` pass only with `judgment: adds data check <unit> -- <why>` or `moves <what> to code`; `first_look.put_problems` is a census row of class `xref` | `scripts/tests/fixtures/judgment-census.json` `ratchet`, row `first_look.py put_problems`; `tools/architecture_gate.py` docstring item 7 |

## §1 Architecture invariants touched, checks, owners, census class

| AR | Touched by | Change check (in that card's DoD) |
|---|---|---|
| AR-28 / FR-59 / FR-41 | A1 (`due`), A2 (survey open), B1 (gap text), D1 (ui-only stays pending) | A1 scenario row; A2 error-direction row; B1 gap row; D1 rows |
| AR-29 / P27 | every check below | census rows of the touched units; `judgment:` line per card |
| AR-2 / AR-7 | which way in, which locator: the role's judgment | no code check judges it (named per card) |
| AR-10 | A1: the form section tells the walker the `sign_in` fields before the work | the contract section exists; B1 runner line names it |
| AR-13 | C1: one reader of the recorded way (`project_knowledge.sign_in`), one acceptance reader (`first_look.accepted`); B1/B2 read the story's own way only through `first_look.read` | Grep `environments.sign_in` outside `project_knowledge.py` and `config-keys.json` = none; Grep `"accepted"` status reads of first-look dispatches = `first_look.accepted` only |
| AR-14 | A1: `first_look.put` stays the one writer of `work/first-look.yaml`; C1: `project_knowledge.record` stays the one writer of the registry | `artifact-writers.json` unchanged |
| AR-15 | one secret guard (`first_look.sign_in_secret_faults`) used by A1 and C1; one line renderer of a way in (`brief_pack.sign_in_lines`) used by B1 and B2 | named in the cards |
| AR-3 | C1: catalogue row `environments.sign_in` with `absent_means` | `test_config_migration.py` if printed (slow: canon) |
| AR-21 / FR-49 | B1: the window's first-look substance reaches S5 whole, every cut said | B1 join row |
| AR-22 | producer `first_look.put` (`sign_in`) -> `first_look.read` -> B1 lines / C1 `record_sign_in` -> registry -> `project_knowledge.sign_in` -> B2 lines, D1, FV1-28e | one data-join row per producer -> reader (A1/B1 F-8, C1, B2) |
| AR-23 | `sign_in` absent / `{}` declared; `ways: []` declared; all-access rows declared | edges per card |
| AR-25 / FR-40 | a registry row has a way out (`revoke`) | C1 `design/state-exits.md` row |
| AR-12 / AR-20 | brief bytes grow (window only); no ratchet row moves except the census ones named in §1b | B1 measures bytes; census raises named |
| AR-19 / axis 5 | driver road and skill road of the first look change together (C1) | C1 owns `phases/s3.md` |

### §1b Checks the node adds or alters (AR-29; P27) — owner and census class

| Check (unit) | Card | Owner it serves | Census class | Ratchet effect, both worlds |
|---|---|---|---|---|
| `first_look.due`: the `environment_pending` operand removed | A1 | data (a stand is named or not) | none — `due` returns a tuple, no refusal site, no census row | none |
| `first_look._sign_in_faults` (part of the `put_problems` unit): keys, surface words, limits, `actor` among the walk's actors, evidence through `capture_cited` | A1 | data | `put_problems` stays `xref` (shape + xref); the helper carries the comment "part of the put_problems unit; not a unit of its own" | none |
| `first_look.sign_in_secret_faults(value, literals)`: a field that looks like a secret, or holds a literal secret of the walk's accounts | A1 (reused by C1) | data (a guard) | **safety** | if `test_judgment_census.py` (canon) makes it a unit: row `safety`, owner `data`, roles `qa-runner`, and the raise `safety 86 -> 87` (and `blocking_per_role.qa-runner` if it grows) is NAMED with `judgment: adds data check first_look.sign_in_secret_faults -- a guard: no account value is ever stored`; if it does not become a unit: the `put_problems` row's note gains "+ safety (secret guard)" and no ceiling moves |
| `walk_session.survey_opens_on(record)` + the survey branch of `Walk._open_actors` / `Walk._shutdown` | A2 | data (fields of the probe record) | shape | if the scan makes `_open_actors` a unit: row `shape`, owner `data`; no ceiling moves (a refusal is REMOVED for one case, none added) |
| brief lines (B1, B2) | B1, B2 | data | none (no refusal) | `judgment: none -- brief lines carry data` |
| `project_knowledge.record_problems` `SIGN_IN_KEY` branch + `_sign_in_value_faults` | C1 | data | `record_problems` stays `shape` (the guard it calls is A1's safety unit) | none |
| `first_look.accepted` (moved from the driver) and `first_look.record_sign_in` (accepted AND at least one row not blocked by access) | C1 | data: the controller's acceptance of a finished dispatch is CODE acceptance, not a tier judgment of the way (critic Key 4) | shape | a CLI refusal site in `_cli record-sign-in` -> row `shape`, owner `data`, roles `conductor`; `blocking_per_role.conductor` may grow by one: named with `judgment: adds data check first_look.record_sign_in -- presence of an acceptance and of one reached row, never whether the way is right` |
| `env_probe.probe` precedence and the ui-only branch | D1 | data | shape | named at D1 dispatch |
| WHETHER a recorded way is right; which locator to trust | — | judgment: the role that uses it (it records a new way when the old fails); accepted by the tier above (S5 code critic; the S6 walker's own record) | — (no code check) | — |
| taking a wrong recorded way back | — | intent: the person, `project_knowledge.py revoke --id PK-n --words-file <F>` | — | — |

## §2 Waves and file ownership

| Wave | Card | Files (owns) | Overlap check |
|---|---|---|---|
| 1 | A1 | `first_look.py` (`due`, `TOP_KEYS`, `put_problems`, `put`, `read`, new `_sign_in_faults`, new `sign_in_secret_faults`, new constants), `first-look-statuses.json`, `artifact-contract-first-look.md`, `test_first_look.py`, `test_first_look_step.py`, census rows, changelog fragment | no other wave-1 card writes these |
| 1 | A2 | `walk_session.py` (`Walk._open_actors`, `Walk._shutdown`, `_Sink.probe`, new `survey_opens_on`), `manual_capture.py` (`_stand_blocked` ONLY), `test_walk_survey_place.py`, census rows, changelog | `manual_capture.py`: no other wave-1 card writes it (A1 only CALLS `read_login`/`resolve_actor`) |
| 1 | B1 | `brief_pack.py` (`first_look_lines`, `_fl_body`, `_fl_state`, `first_look_input_line`, `first_look_runner_lines`, new `sign_in_lines`, new constants `FIRST_LOOK_GAP`, `FIRST_LOOK_GAP_CLAUSE`, `FIRST_LOOK_ITEM_CHARS`, `SIGN_IN_LINE_CHARS`; the two call lines in `build`), `test_first_look_briefs.py`, changelog | `wip/fv16-n2` edits `brief_pack.case_concern_lines` only: function-disjoint (D-0048). B1 does not touch `FIRST_LOOK_KIND` (A1a), `FIRST_LOOK_AHEAD`/`FIRST_LOOK_DOD` (T3b). **Dependency, not overlap:** B1's own-`sign_in` part reads A1's `read()["sign_in"]` -> fork F-8 |
| shared | all | `judgment-census.json` | rows only, merged by appending; the later merge resolves |
| 2 | C1 | `first_look.py` (new `accepted`, new `record_sign_in`, `_cli`/`SUBCOMMANDS` `record-sign-in`, `read` gains `stand`), `project_knowledge.py`, `config-keys.json`, `driver_stage_plan.py` (`_first_look_accepted`, `_first_look_walk` tail), `phases/s3.md`, `design/state-exits.md`, `docs/SIBLING_MAP.md` (axis 5 row «How the stand logs in» only), `test_project_knowledge.py`, census rows, changelog | after A1 merged (same file `first_look.py`) |
| 2 | B2 | `brief_pack.py` (`sign_in_lines` registry part, new `sign_in_ways`), `app_card.py` (`_signin` only), `test_first_look_briefs.py`, changelog | after C1 (reads `project_knowledge.sign_in`) and after B1 (same functions) |
| 3 | D1 | WAITING: after FV1-5 (in main per the Lead; not verified here) AND FV1-17 (not built) | owns `env_probe.py` (`probe` login branch) |
| later | FV1-28e | named node, owns `manual_capture.py` (`login_recipe`) | after C1 |

---

## Card A1 — the role, not the probe, decides whether the first look happens; the way in it found is part of its record

Wave 1. Worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a1` (cut from pushed `origin/main`).

given: this spec (§0 F7', F10', F11', F12', F18'); `ai-packages/qa-factory/design/factory-rules.md` whole; `plans/builder-rules.md`;
`ai-packages/qa-factory/design/architecture.md` (AR-10, AR-13, AR-14, AR-15, AR-23, AR-28, AR-29); `docs/TESTING.md`; the finding
`plans/piles/live-run-fvf/findings/20261113-pervyj-vzglyad-ne-dohodit-do-avtomatora.md`; the real record
`experiments/mybooks/factory-vs-free-agent/runs/factory-out/work/first-look.yaml`.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a1\ai-packages\qa-factory\scripts\first_look.py (`due`, `TOP_KEYS`, `put_problems`, `put`, `read`, new `_sign_in_faults`, new `sign_in_secret_faults`, new constants `SIGN_IN_STEPS_MAX`, `SIGN_IN_LINE_MAX`, `SIGN_IN_TEXT_MAX`, `SIGN_IN_LIST_MAX`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a1\ai-packages\qa-factory\references\first-look-statuses.json (new keys `sign_in_surfaces`, `sign_in_keys`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a1\ai-packages\qa-factory\references\artifact-contract-first-look.md (new section "The way in you found")
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a1\ai-packages\qa-factory\scripts\tests\test_first_look.py (one parameterised table; rewrite of any existing row that asserts `no_stand` on `environment_pending`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a1\ai-packages\qa-factory\scripts\tests\test_first_look_step.py (one scenario row)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a1\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows of the changed/new units only; merge by appending)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a1\ai-packages\qa-factory\changelog.d\fv1-28-a1-first-look-not-skipped-by-probe.md (new fragment)
non-goals: `env_probe.py` and the S0 `environment_pending` write (FV1-5 / D1); `walk_session.py` (A2); `brief_pack.py` (B1); the
registry (C1); new `null_reasons` words; `agents/qa-runner.md`; the S6 `s6_no_stand` decision (`driver_stage_s6.py`: no test run on an
unconfirmed stand — a different decision, unchanged).
handoff: builder report per `.claude/agents/builder.md` rule 7: the witness verbatim, the FR pass (sections A, C, D, E, G), the
`architecture:` and `judgment:` lines, the census rows written and the result of the census question (both worlds of §1b), the files
of the witness list skipped as slow or quarantined, by name.

What to build:
1. `first_look.due`: return `(False, "no_stand", ...)` ONLY when `pipeline.environment` is empty (no stand named: a fact of the
   story). `environment_pending: true` with a named stand goes on to the attempt checks and returns True when nothing else says no.
   The docstring says why: the probe at S0 is a guess of code, the role decides whether it can reach the stand (owner's word;
   FR-41, FR-59). The `why` text of the empty case becomes "no stand is named for this story".
2. `TOP_KEYS` gains `sign_in`. One optional top-level mapping, checked by `_sign_in_faults(task_root, sign_in, attempt)` inside
   `put_problems` (after the rows; its problems join the list), written whole by `put` into the record, returned by `read` as
   `sign_in` (`{}` when absent, null, or not a mapping on disk). Keys (the allowed list is DATA: `first-look-statuses.json`
   `sign_in_keys`, read through `first_look.data()`):
   - `surface` (required): a word of `sign_in_surfaces` = `["ui", "http"]`;
   - `actor` (required): one of the walk's actors from `WS.read_record(task_root, walk)["actors"]`, never `guest` (the record names
     who signed in, never a key or a value);
   - `url` (required, text): where the sign-in starts (ui) / the stand's base address (http);
   - `steps` (optional list of lines): what the role did, in words;
   - ui only: `fields` (required for ui; mapping `user`, `secret`, optional `submit` -> selector text) and `landed` (optional;
     mapping `url_not` -> list of address fragments that mean "still on the sign-in page");
   - http only: `access` (required for http): an `environment.access`-shaped object, checked by `config_contract.access_errors`
     (amendment 9a: D1 later runs exactly this object); kinds `harness_command` and `none` are refused here with the door
     "a way in found in a story names a request, never a command; record the ui way, or leave `sign_in` out" (closed choice C-2);
   - `evidence` (required, non-empty list), `quote` (required, words of those captures), `req` (required, the R-n whose survey
     attempt holds the captures): each path through `WS.capture_cited(task_root, walk, req, path, quote, stand)`; a reason refuses
     naming the path (amendment 2);
   - `why` (required): one sentence, what the role did.
3. `sign_in_secret_faults(sign_in, literals) -> list` (amendment 3), called by `_sign_in_faults` and later by C1: (a) every string
   leaf of `url`, `steps`, `fields`, `landed`, `access` (key-name fields included) compared as
   `app_card.scrub(v, tokens=False) != " ".join(v.split())` -> refused "`sign_in.<path>` looks like a secret value (a password,
   token or cookie); record names and selectors only"; (b) `literals` = the SECRET values of the walk's account actors, read in
   memory through `manual_capture.read_login(cfg, project_root, actor=, stand=, task_root=)` (the builder reads the returned
   object's fields and names them in the report); a string leaf that contains a secret of 4+ characters, or holds a shorter secret
   as a whole token, is refused naming the FIELD, never the value. A `read_login` that raises for an actor -> the record is
   refused with "the account values of `<actor>` cannot be read now, so `sign_in` cannot be checked against them; leave `sign_in`
   out and say in `gaps` how you signed in" (FR-59: the guard does not pass on an unknown).
4. `put`: the record = frame + rows + gaps + `sign_in` (when given). `put --null` writes no `sign_in`.
5. `artifact-contract-first-look.md`, new section "The way in you found": the YAML example for ui and for http (key names only),
   and the rule: "Find the way in yourself, as a tester would; the factory's own probe at the start is a guess, not a fact for you.
   Record the way that worked under `sign_in`, with a capture that shows you landed. If nothing worked, every requirement is
   `unreachable` with `blocked_by: access`, and `why` says what you tried."

edges:
- INVARIANT (positional, `due`): the order stays `parks_after_s5` -> register unreadable -> empty register -> no stand NAMED ->
  attempt on these heads. Unreachable: a paid walk when no stand is named; a second walk on the same heads and register; a walk for
  a story whose deliverable side does not exist. Still refused: nothing new — only the `environment_pending` operand goes.
- A refused login at S0 (`environment_pending: true`, stand named): the walk is now opened. If the stand is really dead, `walk_session
  open` fails (A2 keeps that refusal) -> `_first_look_give_up` writes `walk_not_opened`; INVARIANT: "no stand" is never written from
  a probe result.
- The role cannot reach the stand: rows `unreachable` / `blocked_by: access`, `why` names what it tried; no `sign_in`. INVARIANT: a
  failed login is recorded by the ROLE with what it tried, never by code.
- EMPTY: `sign_in` absent, `null` or `{}` -> nothing stored, `read` gives `{}`; `sign_in: []` or a string -> refused "`sign_in` is a
  mapping"; `steps: []` / absent -> empty list, accepted; `evidence: []` -> refused (a way in without a capture of this walk never
  reaches the record); `url: ""` -> refused; `quote: ""` -> refused by `capture_cited`.
- CONFLICTING PAIR: `fields` or `landed` under `surface: http`, `access` under `surface: ui` -> refused naming the key and the surface.
- LIMITS (outside input: the role's file; a case AT and BEYOND each): `steps` at most `SIGN_IN_STEPS_MAX = 20` lines, each at most
  `SIGN_IN_LINE_MAX = 300` characters; `url`, every selector, every `url_not` fragment at most `SIGN_IN_TEXT_MAX = 500`; `url_not`
  at most `SIGN_IN_LIST_MAX = 20` entries; `why` has no limit (as a row's `why` today). Beyond -> refused with the limit named.
- SECRET GUARD, both directions: a literal account secret in `steps` ("type <secret> into the box") -> refused naming the field;
  `[data-testid=login-form-submit-button-v2]` (a 24+ run) -> PASSES (`tokens=False`); a selector with a double space -> PASSES (the
  compare is against the whitespace-folded value). Error direction: over-refusal; the refusal never prints the value.
- XREF: `actor` not among the walk's actors, or `guest` -> refused naming the walk's actors; `req` not an attempt of the walk ->
  `capture_cited`'s own reason.
- TEMPORAL: records written before the change have no `sign_in` -> `read` gives `{}`; a story with `null: no_stand` already written
  keeps it (`put --null` never replaces a current walked record); on the next S3 entry `due` is asked again and walks; a story past
  S3 is not walked again by this change.
- CONFLICT `sign_in` + every row `unreachable/access`: stored as sent (the role's record); C1 refuses to put it in the registry.

DoD:
- `test_first_look_step.py` (keep `scenario`): ONE new row from the live defect (LOCAL-1: `environment: "local"`,
  `environment_pending: true`): the driver opens the survey walk and registers `S3-qa-runner-<n>`; before the change the same row
  read `null: no_stand`. Any existing row asserting `no_stand` on `environment_pending` is rewritten in this node (find it with
  Grep `environment_pending` over `test_first_look*.py`; TESTING.md "Когда тест покраснел" 1).
- `test_first_look.py` (keep `gate_named`): ONE parameterised table `sign_in_battery`, ids naming each case: whole ui accepted and
  read back; whole http accepted; absent / null / `{}` -> `{}`; `[]` and a string refused; unknown key; missing `surface`; unknown
  surface; `fields` under http; `access` under ui; `access.kind: harness_command`; `actor: guest`; actor not in the walk; empty
  `evidence`; empty `quote`; a capture of another item; steps 20 / 21; a line 300 / 301; url 500 / 501; selector 500 / 501; a nested
  mapping in `steps`; non-UTF-8 file (the existing `_load_input` road); a literal secret in `steps` (refused, value absent from the
  problem text); a 30-character `data-testid` selector (passes); a double-space selector (passes); `read_login` raising (refused).
- `selftest.py --lang` green on the touched files.
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/first_look.py references/first-look-statuses.json references/artifact-contract-first-look.md`
  and every file it prints EXCEPT files in `scripts/slow_tests.json` (`test_judgment_census.py` 33.3 s among them) and files in the
  `quarantine` section of `scripts/tests/test-layers.json`: those are named in the report as "judged by the batch canon". No CI, no
  pipeline wait, no mutations (PROJECT.md «Командная работа» 13).
- commit lines: `architecture: AR-28 -- a refused probe no longer becomes "no stand"; the role decides`; `architecture: AR-29 -- the
  sign_in checks are shape, xref and a safety guard; whether the way is right stays the role's`; `architecture: AR-14 -- first_look.put
  stays the one writer of the record`; `architecture: AR-10 -- the form tells the walker the sign_in fields before the work`; and the
  `judgment:` line of §1b (both worlds).
siblings: `driver_stage_plan.first_look_step` reads `due` (one reader, unchanged); `first_look._show` prints `due` (unchanged);
S6 `s6_no_stand` reads `environment_pending` for test runs — named, unchanged; axis 5 row «The first look» (the skill road reads `due`
through `first_look.py show --json`: unchanged).

---

## Card A2 — a survey walk opens on a stand whose build is not established; a dead stand or a provably other build still refuses

Wave 1. Worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a2`.

given: this spec (§0 F9', F9'', F9'''); `design/factory-rules.md` whole; `plans/builder-rules.md`; `design/architecture.md` (AR-2,
AR-7, AR-28, AR-29); `docs/TESTING.md`; the critic Key 2 "§9 items, measured" and amendment 1.
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a2\ai-packages\qa-factory\scripts\walk_session.py (`Walk._open_actors`, `Walk._shutdown` (the end-probe branch only), `_Sink.probe`, new module function `survey_opens_on`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a2\ai-packages\qa-factory\scripts\manual_capture.py (`_stand_blocked` ONLY)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a2\ai-packages\qa-factory\scripts\tests\test_walk_survey_place.py (one parameterised scenario row)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a2\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-a2\ai-packages\qa-factory\changelog.d\fv1-28-a2-survey-opens-on-unknown-build.md
non-goals: `manual_capture.stand_probe` itself and `ACCEPTS` (the shared gate stays strict for every other caller); standalone
`manual_capture.py ui|http` captures; case, settle and control walks; `first_look._stand_build` (it already says `not_established`);
`runtime_probe.py`.
handoff: builder report with the witness, the FR pass (A, D, G), the `architecture:` / `judgment:` lines, the list of readers of
`probes.jsonl` rows found by Grep and whether any reads the new `taken` key.

What to build:
1. `manual_capture._stand_blocked` sets one attribute on the `EnvBlocked` it returns: `exc.provenance = record` (the probe record it
   judged; `None` for a non-dict). `EnvBlocked.row` is NOT changed (it is persisted into attempts). Every `EnvBlocked` built
   elsewhere has no such attribute; readers use `getattr(exc, "provenance", None)`.
2. `walk_session.survey_opens_on(record) -> bool`, pure, never raises. True ONLY when ALL hold: `record` is a dict;
   `record["result"] == "unknown"`; `profile_contract.validate_runtime_provenance(record)["result"] == "unknown"` (not upgraded to
   `mismatched` by revisions); `not profile_contract.stand_runs_other_build(record)`; `record.get("asks_person")` is a non-empty word
   (the stand answered and only the build could not be read or tied); `record.get("reason_code")` is neither
   `runtime_probe.DEVICE_UNREADY` nor `runtime_probe.NO_EXPECTED_REVISION`. ERROR DIRECTION: it may err only toward False (today's
   refusal); a False on a reachable stand costs one walk not opened, a True on a dead stand or another build would put a false
   observation in the record.
3. `Walk._open_actors`: in the `except MC.EnvBlocked as exc` handler, FIRST test `self.place == SURVEY and
   survey_opens_on(getattr(exc, "provenance", None))`; true -> append the start probe row with `taken: "not_established"`
   (`_Sink.probe(when, profile, command, value, taken="")` gains the optional keyword; a row without it is as today), append to
   `self.notes` "the build on the stand is not established (runtime probe: unknown, <asks_person>); the first look walks the stand as
   it is", and go on opening the actors; false -> `raise ServerDead(...)` exactly as today.
4. `Walk._shutdown`: the same test on the end probe's `EnvBlocked`; true -> the end row with `taken: "not_established"` goes into the
   item attempts and NO `env_blocked` row is written; false -> as today.

edges:
- INVARIANT (positional): the branch is inside the `EnvBlocked` handler and is gated by `self.place == SURVEY` before anything else.
  Unreachable: a case, settle or control walk opening on an unknown build (they produce evidence of runs and verdicts); a standalone
  capture taking an unknown (it never calls `_open_actors`). Still refused on a survey: `mismatched` (other build), a content
  mismatch, an `unknown` with no `asks_person` (docker did not answer; the probe raised -> "stand does not answer", heals by retry:
  `open_failed`, then `walk_not_opened` after `open_retry_max`), `DEVICE_UNREADY`, `NO_EXPECTED_REVISION`, a person's word for another
  story (its door is the person's word for THIS story), no probe registered for the profile (fork F-9), any `EnvBlocked` without a
  `provenance` record.
- What is recorded: the probe record whole in the walk's `probes.jsonl` rows (`taken: not_established`), the walk note, and the
  record's `stand_build: not_established` that `first_look._stand_build` already writes; the S3 brief already says "The stand's build
  is not established" (`brief_pack._fl_body` kind `s3`).
- Reused function in a more consequential role (advice -> gate opening): `validate_runtime_provenance` and `stand_runs_other_build`
  now decide an OPEN. Adversarial inputs that must stay refused (rows of the DoD table): a record declaring `unknown` whose
  `deployed_source_revision` differs from `expected_source_revision` (effective `mismatched`); `asks_person: ""`; `asks_person`
  present on a `matched` record that fails validation; `result: "UNKNOWN"`; a non-dict.
- EMPTY / ABSENT: `provenance` absent -> refused (today).
- TEMPORAL: walk records written before the change have no `taken` key -> read as today.

DoD:
- `test_walk_survey_place.py` (keep `scenario`): ONE parameterised row `survey_open_on_probe`, ids: `unknown_asks_how` (opens; note
  present; probes row `taken: not_established`), `unknown_asks_confirm` (opens), `mismatched` (ServerDead), `unknown_docker_down`
  (no `asks_person`: ServerDead), `unknown_but_revisions_differ` (ServerDead), `other_story_word` (ServerDead), `device_unready`
  (ServerDead), `case_place_unknown_asks` (a `case` walk: ServerDead — the positional invariant), `end_probe_unknown_asks` (close
  writes no `env_blocked`).
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/walk_session.py scripts/manual_capture.py`
  and every file it prints except `slow_tests.json` files (`test_manual_capture.py` 10.6 s is one) and quarantined files, named as
  "judged by the batch canon"; no CI, no mutations.
- commit lines: `architecture: AR-28 -- an unknown build is recorded as not_established, never a pass; a dead stand or another build
  still refuses`; `architecture: AR-2 -- the walker judges what it sees on a stand of unknown build`; `judgment: none -- one probe
  refusal is lifted for survey walks by fields of the record; no judgment moves` (or `adds data check walk_session._open_actors -- ...`
  if the census scan makes it a unit).
siblings: `manual_capture._session_cycle_held` and the `http` capture (their own `stand_probe` calls: unchanged, named); the four
walk places (axis 5 row «The first look»: "the walker's pass is one over its four uses" — only survey changes, by design: a survey
records observations, the other three record evidence).

---

## Card B1 — S5 gets the window's first look in substance; a missing look is a gap; the story's own way in reaches its briefs

Wave 1 (work); merge after A1 (fork F-8). Worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-b1`.

given: this spec; `design/factory-rules.md` whole; `plans/builder-rules.md`; `design/architecture.md` (AR-13, AR-15, AR-21, AR-23,
AR-26, AR-28); `docs/TESTING.md`; the draft's F1-F3, F16, F17 (`brief_pack.FIRST_LOOK_KIND`, `FIRST_LOOK_AUTHOR_KINDS`,
`_fl_body`, `_fl_state`, `first_look_lines`, `build`; `contract.case_requirements`; `brief_pack.case_paths`); A1's `sign_in` shape (card
A1 item 2).
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-b1\ai-packages\qa-factory\scripts\brief_pack.py (`first_look_lines`, `_fl_body`, `_fl_state`, `first_look_input_line`, `first_look_runner_lines`, new `sign_in_lines`, constants `FIRST_LOOK_AUTHOR_KINDS`, new `FIRST_LOOK_GAP`, `FIRST_LOOK_GAP_CLAUSE`, `FIRST_LOOK_ITEM_CHARS`, `SIGN_IN_LINE_CHARS`; in `build` only the `first_look_lines(...)` call line and one new `sign_in_lines(...)` call line)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-b1\ai-packages\qa-factory\scripts\tests\test_first_look_briefs.py (new rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-b1\ai-packages\qa-factory\changelog.d\fv1-28-b1-first-look-substance.md
non-goals: `FIRST_LOOK_KIND` (A1a), `FIRST_LOOK_AHEAD`, `FIRST_LOOK_DOD` (T3b); `case_concern_lines` (fv16-n2); `agents/qa-automator.md`
and the walker card for S5 (FV1-29); `app_card.py` (B2); registry ways (B2); `first_look.py` (A1).
handoff: builder report with the witness, FR pass (B, C, E), `architecture:` / `judgment:` lines, the byte measure.

What to build:
1. `FIRST_LOOK_AUTHOR_KINDS["s5"] = ("screen", "step", "locator", "api", "sample", "data")` (the reading stays
   `app_card.first_look_path_items`, the one reader).
2. Kind `s5`: ONE LINE PER ITEM: `- R-n <status>: <item text> [first-look:R-n]`; an item longer than `FIRST_LOOK_ITEM_CHARS = 400`
   is clipped with `...` (a `_Clipped`), and the block ends `whole: work/first-look.yaml` (today's road).
3. `first_look_lines(task_root, stage, role, *, scope=None, s5_kind="")` (keywords with defaults: every other caller unchanged;
   `build` passes its `scope` and `s5_kind`). Only when `s5_kind == "window"`: rows are those whose `req` is in the union of
   `contract.case_requirements(p)` over `case_paths(task_root, scope)`, NO count cap, and one line `- +N requirement(s) of the record
   outside this window: work/first-look.yaml` when N > 0. Plan, legacy, unknown kinds and every non-S5 kind keep
   `FIRST_LOOK_LINES_MAX` and the `+N more` pointer (amendment 5).
4. The gap, one text for S3-S7 through `_fl_state` (kinds `null`, `absent`, `unreadable`, `error`): `FIRST_LOOK_GAP` = "First look: a
   GAP - what the stand shows is not known for this story ({reason}); it is not a fact that there is no stand. {clause}", where
   `{clause}` comes from the data dict `FIRST_LOOK_GAP_CLAUSE[kind]`: `LOOK` = "Where your work needs the stand, look yourself with the
   tools your brief names." for `s6`, `s7`; `NAME` = "Name it as a gap where your work rests on the stand." for `s3`, `s4`,
   `s4_critic`, `s5`, `s5_critic` (S5 flips to `LOOK` in FV1-29, which gives S5 its walker card: the seam). `_fl_state` gains the
   `kind` argument for the clause. Stale keeps its meaning and gains the same clause. `first_look_input_line` (a file line, no reader
   kind) says "- work/first-look.yaml: a GAP - no first look was written for this story (<reason>); it is not a fact that there is no
   stand". No line names a script (the roles may have no shell).
5. Author kinds `s4`, `s5`: when every row shown is `unreachable` with `blocked_by: access`, the body is one line "First look: the
   walker could not reach these requirements (access): <each row's why, whole>; a gap you close with your own look" (s5) / "...; name
   it as a gap" (s4), instead of "no row names such a path".
6. `sign_in_lines(task_root, stage, role) -> list` (own story part; B2 adds the registry part): for the roles of `FIRST_LOOK_KIND`
   and the first-look walker, one line from `first_look.read(task_root).get("sign_in")` when it is a non-empty mapping: "Way in found
   by this story's first look (walk <W>, <surface>, as <actor>): url <url>; fields user <sel>, secret <sel>, submit <sel>; steps:
   <steps joined by '; '>; it worked then - if it fails now, find the way yourself and record it." (http: "access <kind> at <url>,
   key names <user_key>/<secret_key>"). Every value through `app_card.scrub(..., tokens=False)`. A line longer than
   `SIGN_IN_LINE_CHARS = 600` is cut and followed by `whole: work/first-look.yaml`. `no_trace` is NOT read (amendment 6).
   Call sites: in `build`, right after `head += first_look_lines(...)` inside `if not first_look:`; and at the end of
   `first_look_runner_lines` (a re-walk on new heads sees the way the last walk found).
7. `first_look_runner_lines` (the walker's own brief): when `pipeline.environment_pending` is true, one line: "The factory's own check
   of the stand did not pass at the start: that is a guess of code, not a fact. Find the way in yourself; if you get in, record it
   under `sign_in` (the form names it); if you cannot, every requirement is `unreachable` with `blocked_by: access` and `why` says what
   you tried."

edges:
- LIMITS: item text at 400 / 401 characters (clip + `whole:`); sign-in line 600 / 601 (cut + `whole:`); rows outside the window
  counted and the record named; no other cut (FV1-4: a cut always names its carrier).
- EMPTY: `scope` None / plan / legacy / unknown -> all rows under the 12-line cap (today plus items); a window none of whose cases
  names a requirement -> all rows and the line "no case of this window names a requirement: every row is shown" (error direction:
  more, never fewer); a row with no path item -> no line (today); `sign_in` absent / `{}` -> no sign-in line.
- Reused `contract.case_requirements` in a filter role (advice -> filter): it may err only toward MORE rows. Adversarial inputs that
  stay on the safe side: a case file that cannot be read (-> all rows), a case with no requirement line (-> contributes nothing; if
  no case contributes, all rows), an R-n not in the record (ignored).
- INVARIANT (positional): the first-look block stays AFTER `provisional_lines` and BEFORE `prior_retro_lines` (`build`, the order of
  §4.4 row h); the sign-in line comes right after the first-look block. Unreachable: a first-look value printed as an expected value
  (samples and data keep their `seen:` prefix, FR-58); a first-look block in the walker's own brief (`if not first_look`); any account
  value (A1 refuses them at `put`; the line prints only what the record holds).
- CONFLICT: stale record + window -> the stale single line wins (it confirms nothing): no item lines, no sign-in line from a stale
  record (a stale walk's way is history; closed choice C-6).
- TEMPORAL: before A1 is merged `read()` carries no `sign_in` -> no sign-in line (both worlds; fork F-8 for the test row); a record
  written before A1 reads the same; a `null: no_stand` record now gets the GAP text.

DoD:
- `test_first_look_briefs.py` (keep `data_join`), rows:
  (1) the join row from the finding's "Тест" line: a non-empty record -> the S5 WINDOW brief holds the url, a step and the locator of
  a window requirement, not those of an out-of-window requirement, plus the `+N ... outside` line; variant `item_401` (clip +
  `whole:`); variant `plan_kind` (12-line cap and `+N more` kept);
  (2) ONE parameterised gap row over readers (ids `s3`, `s4`, `s5`, `s6`, `s7`): a `null: no_stand` record -> the GAP sentence with
  that reader's clause (the live defect: "no stand" said as a fact);
  (3) the producer -> reader join row for the own way in: A1's `put` with a `sign_in` -> `first_look.read` -> the S5 and S6 brief line
  (lands per fork F-8);
  (4) the runner brief with `environment_pending: true` holds the "guess of code, not a fact" line.
- byte measure: the S5 window brief of row (1)'s fixture before / after, `len(bytes)`, reported with the command; the brief's size row
  also lands in `state/brief-sizes.jsonl` (`_record_brief_size`); `role_load.py --role qa-automator` static total unchanged.
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/brief_pack.py`
  and every file it prints except `slow_tests.json` files (`test_brief_pack.py` 34.6 s, `test_brief_pack_s5_plan.py` 20.2 s) and
  quarantined files (`test_brief_pack_manual.py`, `test_brief_pack_roles.py`, `test_brief_pack_sd_head.py`,
  `test_brief_pack_timeout.py` are in `quarantine`), named as "judged by the batch canon"; `selftest.py --lang`; no CI, no mutations.
- commit lines: `architecture: AR-21 -- the window's first look reaches S5 whole, every cut names its record`; `architecture: AR-28 --
  a missing look is worded as a gap, never as "no stand"`; `architecture: AR-15 -- one gap text for S3-S7 with a per-reader clause from
  one data dict`; `judgment: none -- brief lines carry data`.
siblings: `app_card._first_look` (the card's First look section, same reading, other reader: unchanged, named); S4 `s4` keeps its
12-line cap; FV1-29 flips `FIRST_LOOK_GAP_CLAUSE["s5"]` and puts its walker lines after this block.

---

## Card C1 — code records the way in the role found, through ONE function both roads call

Wave 2, after A1 merged. Worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1`.

given: this spec (§0 F13', F14', F16', F18'); `design/factory-rules.md` whole; `plans/builder-rules.md`; `design/architecture.md`
(AR-3, AR-13, AR-14, AR-15, AR-19, AR-22, AR-25, AR-29); `docs/TESTING.md`; A1 merged (`first_look.read()["sign_in"]`,
`first_look.sign_in_secret_faults`); `docs/SIBLING_MAP.md` axis 5 rows «How the stand logs in» and «The first look».
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1\ai-packages\qa-factory\scripts\first_look.py (new `accepted`, new `record_sign_in`, `SUBCOMMANDS`, `_parser`, `_cli` subcommand `record-sign-in`; `read` gains `stand`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1\ai-packages\qa-factory\scripts\project_knowledge.py (`record_problems`, new `_sign_in_value_faults`, new `sign_in`, constants `SIGN_IN_KEY`, `SIGN_IN_PRECEDENCE`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1\ai-packages\qa-factory\references\config-keys.json (section `knowledge`: row `environments.sign_in`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1\ai-packages\qa-factory\scripts\driver_stage_plan.py (`_first_look_accepted`, the tail of `_first_look_walk`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1\ai-packages\qa-factory\skills\qa-story\phases\s3.md (section "First look" and the line-12 summary: one command)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1\ai-packages\qa-factory\design\state-exits.md (one row)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1\docs\SIBLING_MAP.md (axis 5 row «How the stand logs in» only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py (one parameterised join row)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-c1\ai-packages\qa-factory\changelog.d\fv1-28-c1-sign-in-record.md
non-goals: `config.json` (no write from a story; FV1-15 F7(A)); `env_probe.py` (D1); `manual_capture.py` (FV1-28e); `stand_access.py`
(FV1-17); `brief_pack.py` (B2); `report_facts.py`.
handoff: builder report with the witness, FR pass (A, C, D), `architecture:` / `judgment:` lines, census rows, the axis block for the
`SIBLING_MAP.md` edit (mechanism gate) and the `tier:` note if the gate asks for it (builder-rules 18: stage, report, Lead commits).

What to build:
1. Catalogue row `environments.sign_in`: `store: registry`, `scope: stand`, `compare: exact`, `absent_means: "no way in is recorded for
   this stand: the walker finds it itself"`, `needed_by` the S3-S7 briefs, `env_probe`, `manual_capture.login_recipe`, and a `note`
   naming the writer (`first_look.record_sign_in` through `project_knowledge.record`) and the reader (`project_knowledge.sign_in`).
2. `record_problems`: a branch `elif key == SIGN_IN_KEY:` placed with the `LESSONS_KEY` branch, BEFORE the role rules, with the
   comment "BEFORE the role rules: a surface word never meets them, and a role key never skips them". It calls
   `_sign_in_value_faults(element, value)` (part of the `record_problems` unit): the element is a word of `first_look.data()
   ["sign_in_surfaces"]`; the value is A1's shape without `evidence`, `quote`, `req`, `why`, checked by A1's own shape rules and
   `first_look.sign_in_secret_faults` (one guard, AR-15; literals from the same `read_login` road).
3. `project_knowledge.sign_in(root, stand) -> {"ways": [{"surface", "value", "story", "at", "id"}], "precedence": SIGN_IN_PRECEDENCE,
   "problem": str, "no_stand": bool}`: the newest live row per surface on the EXACT stand (`_latest`), sorted by surface. PURE, never
   raises; empty / placeholder stand -> `no_stand` True; catalogue without the row or unreadable registry -> `problem`, never "no way"
   (FR-59). `SIGN_IN_PRECEDENCE = ("recorded", "project", "factory_default")`, its docstring the ONE statement of the order
   (amendment 11): a way the first look recorded on this stand, then the project's config (`environment.access` for an http reader,
   `manual_capture.login.ui` for a ui reader), then the factory default; a role-recorded way ranks above the onboarding config ON
   PURPOSE (finding item 3: «догадка пробы никогда не перекрывает эту запись»), and a stale recorded way has one exit, `revoke`.
4. `first_look.accepted(task_root, controller_state) -> bool`: the condition of today's `_first_look_accepted` moved here unchanged
   (attempt `written`, the dispatch `accepted`, a current non-null non-empty record of THAT walk). The driver's
   `_first_look_accepted` becomes `return FL.accepted(self.task_root, self.controller_state())` inside its existing `try` (AR-13: one
   reader).
5. `first_look.record_sign_in(task_root, *, by, controller_state=None) -> {"recorded": bool, "id": str, "line": str}` — THE one
   write function: (1) `controller_state` None -> read through `controller.Controller(task_root).state()` (the builder confirms it is
   side-effect free and names it; if it is not, the CLI reads `state/controller.json` through `hooklib.read_json`, the same file
   `driver_core.controller_state` reads); not `accepted` -> no write, line "S3: first look: the way in was not recorded: the first look
   of these heads was not accepted"; (2) `read(task_root)["sign_in"]` empty -> no write, NO line; (3) every row has `blocked_by: access`
   -> no write, line "... not recorded: every requirement of the record was blocked by access, so this way did not get the walker
   anywhere" (amendment 4); (4) `project_knowledge.record(project_root, key=SIGN_IN_KEY, environment=<the attempt's env>,
   element=<surface>, state="known", scope="stand", value=<shape>, words=<the role's why>, source="role", story=<task name>, by=by,
   where=f"first look {walk}", task_root=task_root)`; created -> line "S3: first look: recorded the way in to `<stand>` (<surface>) as
   PK-n for later stories"; the existing row -> "... already recorded as PK-n"; refused -> "... not recorded (<reason>)". It never
   raises and never stops S3 (P1). CLI: `first_look.py record-sign-in --task-root <T>` (by = `conductor`), prints the line, exit 0
   whether recorded or not (a not-recorded way is a fact, not a failure of the call); exit non-zero only for a bad call.
6. Driver: in `_first_look_walk`, right after `if self._first_look_accepted(FL):` and before `return True`, print the line of
   `FL.record_sign_in(T, by="driver", controller_state=self.controller_state())` when non-empty. Skill road: `phases/s3.md`
   "First look": after an ACCEPTED dispatch, `python "${CLAUDE_PLUGIN_ROOT}/scripts/first_look.py" record-sign-in --task-root <TASK
   ROOT>` (and the same command in the line-12 summary).
7. `state-exits.md` row: `environments.sign_in` -> way out `project_knowledge.py revoke --id PK-n --words-file <F>`.
8. `docs/SIBLING_MAP.md` axis 5 row «How the stand logs in»: append "A sixth carrier (FV1-28 C1): the way in a first look found,
   registry key `environments.sign_in`, one writer `first_look.record_sign_in` -> `project_knowledge.record`, one reader
   `project_knowledge.sign_in`, one order `project_knowledge.SIGN_IN_PRECEDENCE`; the story's own way is read through
   `first_look.read`." (amendment 13).

edges:
- INVARIANT (AR-14, P27): the registry is written only by `project_knowledge.record`, only from `first_look.record_sign_in`, only
  after `first_look.accepted`. Unreachable: a record `put` wrote under a dispatch that was not accepted reaching the registry; a way
  with every row access-blocked reaching it; a second write road (Grep `environments.sign_in` and `SIGN_IN_KEY` outside
  `project_knowledge.py`, `first_look.py`, `config-keys.json`: none).
- INVARIANT (positional, `record_problems`): the `SIGN_IN_KEY` branch sits before the role rules; a surface word never meets
  `_unsafe_role` / `reserved_role`, and a role key never skips them.
- no-trace story (P8): `_refuse_no_trace` refuses -> line "not recorded: this run leaves no trace (an experiment); this story's own
  briefs still show the way (B1)".
- DUPLICATE: the same live state and value for the same stand and surface -> the existing row, `created` False, line "already recorded
  as PK-n"; a changed value -> a new row; the reader takes the newest per surface; the old row stays as history.
- ABSENT registry file: the first write creates it (TEMPORAL: the change creates the first `environments.sign_in` row of a project);
  absent file before any write -> `sign_in()` gives `ways: []`, no problem.
- TEMPORAL: before C1 the catalogue has no row -> `sign_in()` gives `problem` naming the missing row (as `lessons` does); after:
  absent rows = `ways: []`. Records written before A1 -> `sign_in` `{}` -> nothing recorded.
- EMPTY: `sign_in` `{}` -> nothing recorded, no line; stand empty in the attempt -> `record` refuses ("no stand is named") -> the line.
- CONFLICT: accepted record with `sign_in` AND every row access-blocked -> not recorded (amendment 4); accepted with `sign_in` and one
  `confirms` row -> recorded.

DoD:
- `test_project_knowledge.py` (keep `register`): ONE parameterised join row `sign_in_record_join`, producer `first_look.put` (A1)
  -> `first_look.record_sign_in` -> registry row -> reader `project_knowledge.sign_in`; ids: `accepted_with_way` (one row, read back),
  `all_rows_access` (no row, the line), `no_trace` (no row, the line), `not_accepted` (no row), `duplicate` (the existing row).
  No per-branch reader rows (newest per surface, another stand, problem): internal boundaries (TESTING.md).
- `test_state_exits.py` and `test_config_migration.py` only if `--witness-for` prints them; `test_config_migration.py` (17.7 s) is slow:
  named as "judged by the batch canon".
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/first_look.py scripts/project_knowledge.py references/config-keys.json scripts/driver_stage_plan.py skills/qa-story/phases/s3.md design/state-exits.md`
  and every file it prints except slow (`slow_tests.json`) and quarantined files, named; `docs/SIBLING_MAP.md` has no test set
  (outside the package): its doc witness is the key-presence run of CLAUDE.md rule 11 (keys verbatim from item 8; script in full;
  a negative control); no CI, no mutations.
- commit lines: `architecture: AR-13 -- one reader of the recorded way (project_knowledge.sign_in) and one acceptance reader
  (first_look.accepted)`; `architecture: AR-14 -- project_knowledge.record stays the one writer of the registry`; `architecture: AR-19
  -- the driver road and the skill road call one function`; `architecture: AR-25 -- a recorded way has a way out (revoke)`;
  `architecture: AR-3 -- a new fact is a catalogue row with absent_means`; `judgment:` per §1b.
siblings: `project_knowledge.notice_from_handoff` (the other role-sourced write, `by: driver`: the twin; it writes
`noticed_unconfirmed`, this writes `known` — the first role-sourced `known` row, said in the B2 line as "found by the first look");
`lessons` (the reader twin); axis 35 side rows (same registry, untouched); axis 5 «The first look» (both roads, done here).

---

## Card B2 — later stories' briefs name the recorded way in; the app card does not repeat it

Wave 2, after C1 and B1 merged. Worktree `C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-b2`.

given: this spec; `design/factory-rules.md` whole; `plans/builder-rules.md`; `design/architecture.md` (AR-13, AR-15, AR-16, AR-22);
`docs/TESTING.md`; C1 merged (`project_knowledge.sign_in`); B1 merged (`sign_in_lines`); `brief_pack.stand_lesson_lines` (the twin to
copy); `app_card._signin` (§0 F17').
owns:
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-b2\ai-packages\qa-factory\scripts\brief_pack.py (`sign_in_lines` registry part, new `sign_in_ways`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-b2\ai-packages\qa-factory\scripts\app_card.py (`_signin` only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-b2\ai-packages\qa-factory\scripts\tests\test_first_look_briefs.py (one join row with an app-card variant)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-b2\ai-packages\qa-factory\changelog.d\fv1-28-b2-sign-in-lines.md
non-goals: `report_facts.py` (see residual FV1-28f); `manual_capture.login_recipe` (FV1-28e); `env_probe.py` (D1).
handoff: builder report with the witness, FR pass (B, C, E), `architecture:` / `judgment:` lines, and the answer to "does
`report_facts.knowledge_use` count `[knowledge:environments.sign_in]` markers" (Grep, with a positive control on
`[knowledge:product.roles]`).

What to build:
1. `sign_in_ways(task_root, project, stand) -> {"own": dict, "recorded": [ways], "problem": str}`: `own` from `first_look.read`
   (`sign_in`, `{}` when none or stale), `recorded` from `project_knowledge.sign_in(project, stand)["ways"]` minus every way whose
   `story` is this story (amendment 6), `problem` from the reader. `sign_in_lines` (B1) renders `own` as before and then one line per
   `recorded` way: "Recorded way in to `<stand>` (<surface>, found by the first look in <story>, <date>): <the same fields as the own
   line>; it worked then - if it fails now, find the way yourself and record it. [knowledge:environments.sign_in]". `problem` -> one
   line "The record of ways in found by earlier first looks could not be read (<why>)." No line when both are empty.
2. **§D, ONE carrier:** the recorded way in is rendered ONLY by `brief_pack.sign_in_lines` (the brief of every S3-S7 role and of the
   walker, the S6 walk lane included). `app_card._signin` never renders a recorded way. When `sign_in_ways(...)` has `own` or
   `recorded`, the card's recipe line gains one sentence: "A way in found by a first look is in your brief (the line 'Way in found' /
   'Recorded way in'); it comes before this recipe: the order is the recorded way, then the project's config, then the factory default."
   Why this carrier: the brief reaches every reader of the fact (S3-S7, the walker), the card reaches only S6 walk lanes (§0 F17'),
   and the card's recipe line is a DIFFERENT fact (the config's recipe that code signs in with when gate A proved it); with the
   pointer sentence the packet states the precedence instead of showing two answers that disagree (FR-10).

edges:
- LIMITS: a recorded-way line longer than `SIGN_IN_LINE_CHARS = 600` is cut and followed by "whole: `qa-factory/records/
  project-knowledge.json`" — a FILE, never `project_knowledge.py show` (the readers may have no shell; amendment 7). Cases at 600 / 601.
- EMPTY: `ways: []` and no own way -> no line, no card sentence; `no_stand` -> no line; `problem` -> the one problem line, no card
  sentence.
- SECRETS: no value exists in a row (A1 and C1 refuse them); the line still passes every value through `scrub(tokens=False)`.
- INVARIANT: the line never says the stand is reachable (a past observation); the card never shows a recorded way's fields; a way of
  THIS story never appears twice (own line only).
- TEMPORAL: registry rows written before C1 do not exist; a project with no row -> no line.
- CONFLICT: a recorded `ui` way and a config recipe with another route -> the brief shows the recorded way, the card shows the config
  recipe with the precedence sentence (no silent disagreement).

DoD:
- `test_first_look_briefs.py` (keep `data_join`; its `covers` already lists `app_card.py`): ONE join row `recorded_way_join`, producer
  `project_knowledge.record` (a row from story A) -> reader `sign_in_lines` in story B's S5 brief (the line, with the marker), variant
  `same_story` (story A's own brief: only the own line), variant `line_601` (cut naming the registry file), variant `app_card` (story
  B's card: the precedence sentence present, no recorded field in the card).
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/brief_pack.py scripts/app_card.py`
  and every file it prints except slow and quarantined files (`test_app_card.py` is in `quarantine`; `test_brief_pack.py` slow), named;
  no CI, no mutations.
- commit lines: `architecture: AR-13 -- briefs read the recorded way only through project_knowledge.sign_in`; `architecture: AR-15 --
  one renderer of a way in (sign_in_lines) for the own and the recorded way`; `architecture: AR-16 -- one packet states the precedence,
  never two disagreeing answers`; `judgment: none -- brief lines carry data`.
siblings: `stand_lesson_lines` (twin, unchanged); `app_card._signin` (changed here); axis 6 `report_facts.knowledge_use` (residual
FV1-28f).

Residual FV1-28f (named node, opened only if the B2 builder reports that `knowledge_use` does not count the new key): owns
`ai-packages/qa-factory/scripts/report_facts.py` (`knowledge_use`), one row in the keep file `--witness-for` prints for it; DoD: a brief
with `[knowledge:environments.sign_in]` is counted. Axis 6.

---

## Card D1 — WAITING: the probe takes the recorded way before the project's guess

**Status: WAITING.** Depends on FV1-5 (in main per the Lead's brief; NOT verified here: read-main is behind origin/main) AND FV1-17
(`stand_access` roads, `form_login`, `access.kind: ui_only`, `recorded_login`; spec-only:
`docs/tasks/specs/20261113-fv1-17-5-15-stand-login-spec.md` items 3-6). Dispatched only after both are merged; the Lead re-checks the
function names below against main at that moment.

given (at dispatch): this spec; the stand-login spec items 3-6 and its FV1-15 card; `design/factory-rules.md` whole;
`plans/builder-rules.md`; C1 merged (`project_knowledge.sign_in`, `SIGN_IN_PRECEDENCE`).
owns (worktree `fv1-28-d1`):
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-d1\ai-packages\qa-factory\scripts\env_probe.py (`probe` login branch, new `_recorded_way`)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-d1\ai-packages\qa-factory\scripts\tests\test_http_client.py (rows of the table FV1-17 F6(A) names; keep `table`, not slow, not quarantined on read-main)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-d1\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows only)
C:\QAFactory\forge-repo\.claude\worktrees\fv1-28-d1\ai-packages\qa-factory\changelog.d\fv1-28-d1-probe-recorded-way.md
non-goals: `stand_access.py` (FV1-17 owns it; D1 only CALLS its road executor); `config.json`; `manual_capture.py`; the S0
`environment_pending` write.

What to build:
1. `env_probe.probe`: read `project_knowledge.sign_in(root, stand)` and apply `SIGN_IN_PRECEDENCE` (amendment 11). A recorded `http`
   way (its `access` object, A1's shape) is run through FV1-17's road executor (`stand_access.login` with that object; `form_login`
   covers the csrf two-step) INSTEAD of `environment.access`; values come from the env keys the object names (amendment 9a).
2. A recorded `ui`-only way never removes the login layer: the probe line says "login not checked by code; a UI way was recorded by the
   first look in <story>, <date>" and the verdict stays PENDING, unless the project's `access.kind: ui_only` (FV1-17, the person's word)
   says the tests sign in through the UI (amendment 9b).
3. A recorded way that fails live: `blocked_by: login`, and the probe line AND the S0/S5 warning say "the way in recorded by the first
   look (PK-n, <story>) did not get in; if the stand changed its sign-in, take it back: `project_knowledge.py revoke --id PK-n
   --words-file <F>`" (amendment 10; FR-1, FR-2, FR-40).
edges: INVARIANT — the probe's own guess never overrides a recorded way (registry > project config > nothing); a ui-only record never
becomes a pass (FR-59, AR-28); lockout invariant of FV1-17: one submit per probe; unreadable registry -> today's behaviour plus one line
"the record of recorded ways in could not be read (<why>)" (never a pass); a STALE recorded http way that fails -> the PK-n line, and a
later first look that signs in by UI writes a `ui` row while the stale `http` row stays in force until `revoke` (named, the door is in
the line); no recorded way -> today's behaviour.
DoD (at dispatch): rows in `test_http_client.py`: recorded-http-ok, recorded-http-refused (PK-n line), recorded-ui-only (pending),
recorded-ui-only with `access.kind: ui_only` (skipped as FV1-17 says), none (today), unreadable registry; verification
`python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/env_probe.py` and every file it prints except slow
and quarantined (`test_stand_access.py` is in `quarantine`), named; no CI, no mutations. Lines: `architecture: AR-28 -- a ui-only
recorded way never becomes a pass`; `architecture: AR-13 -- the probe reads the recorded way only through project_knowledge.sign_in`;
`architecture: AR-25 -- a failing recorded way names its revoke door`.
siblings: `stand_health._login_receipt` and `readiness` (read the probe's record, unchanged); FV1-28e (same precedence).

## Node FV1-28e — the walker's code sign-in reads the same order (named node, after C1)

owns: `ai-packages/qa-factory/scripts/manual_capture.py` (`login_recipe`); rows in `scripts/tests/test_manual_capture.py` (keep
`detector`; slow 10.6 s: judged by the canon, never run locally by its builder). What: `login_recipe(cfg, spec, "ui")` takes the
recorded `ui` way of `project_knowledge.sign_in` first, then `manual_capture.login.ui` of the config, then the factory default of
`references/manual-capture-steps.json` — the ONE order `SIGN_IN_PRECEDENCE` (amendment 11; the draft's "after the project's
`manual_capture.login.ui`" is gone). Edges to state at its drafting: gate-A proof still required for a code sign-in
(`sign_in_refusal` unchanged: a role-recorded way has no proof); the no-screenshot window (`landing_rule`, `SessionAccount.window`)
keys on the recorded `landed.url_not` — a safety question, so it must not drift from the recorded page; once `login_recipe` returns the
recorded way, `app_card._signin`'s recipe line names its source "recorded by the first look in <story>" and B2's precedence sentence
goes (one carrier kept).

---

## §3 Acceptance rows (finding items, dry rows)

| Item | Card | Note |
|---|---|---|
| finding item 2 «`no_stand` пишется только тогда, когда РОЛЬ не смогла дойти до стенда» | A1 | **Departure, said outright (amendment 14):** the role does not write `no_stand`; when it cannot reach the stand it writes every row `unreachable` / `blocked_by: access` with `why`. Why: `put_problems` refuses `rows: []` (a walked record with no row cannot exist; NE37 of `null-outcomes.json` guarantees no requirement drops out silently), and an access row with `why` says MORE than a null word (what was tried, per requirement). Code keeps `no_stand` only for a story that names no stand (a story fact, not a probe guess). |
| finding item 1 (substance, window) | B1 | |
| finding item 2 (probe guess never a fact; reader sees a gap) | A1, A2, B1 | |
| finding item 3 (role finds, code records, readers read, guess never overrides) | A1, C1, B1, B2, D1, FV1-28e | |
| finding "Тест" line | A1 scenario row; B1 join row (1) | |
| dry row `first_look/probe_405` | A1 + A2 | stays `known_red: FV1-28` until P1-b's harness exists; green when A1 and A2 merge and P1-b runs |
| dry row `first_look/empty` | B1 gap / all-access rows | **seed amended (amendment 12):** the role stub's record through `first_look.put`, every row `unreachable` / `blocked_by: access` WITH a capture (an access row must cite one: only `nature` needs none); no role stub calls `put --null`. The null case stays covered by `first_look/absent` and by a driver-path seed (an empty `environment` -> `no_stand` through `due`). The amendment spec row is the Lead's to edit. |
| dry row `first_look/absent` | B1 gap rows | |
| dry row `first_look/entry_recorded` | A1 + C1 + B2 (+ D1 for the probe part) | the probe part `after: FV1-28 D1` (WAITING) |

## §4 FR-33 live-proof row (for `live-runs`)

"MyBooks story whose S0 probe fails on the recorded login (old config: `/login` 405) and whose runtime probe says `unknown`: the
first look IS dispatched and the survey walk opens (`stand_build: not_established`); the walker signs in by the UI itself and records
`sign_in`; the S5 window brief carries the url, steps and locators of the window's requirements and the story's own way in. Cross-story
half: a SECOND story on the same stand shows the recorded way in its S3-S7 briefs and the probe uses it (after D1) — **needs the owner's
word** (critic §C Q1: one MyBooks story in normal mode; a comparison run leaves no registry row by design)." Moves to `live-runs` per
PROJECT.md «Командная работа» 9 when the nodes are accepted.

## §5 SIBLING_MAP axes — enumeration (37 axes)

Count: Grep `^#+ .*[Aa]xis \d+` over `C:\QAFactory\forge-repo\.claude\worktrees\read-main\docs\SIBLING_MAP.md` -> 37 headings, `Axis 1`
(line 24) through `Axis 37 — A repeat stop` (line 620); the same call shape `^#+ .*[Aa]xis 3[4-9]` over the ROOT checkout's
`docs\SIBLING_MAP.md` -> 3 headings (34, 35, 36): the root checkout (stale local main) has 36 — the source of the "36". origin/main
`1a00352` was not read for this file (no git command): its count is "37 or more, not verified".

One block for the node's mechanisms (A1 due + form, A2 survey open, B1 lines, C1 record, B2 lines, D1 precedence):
- axis 1: n/a — no CLAUDE.md / role file / journal change (the designer rule 1 / critic 11 triplet untouched).
- axis 2: n/a — no exam instrument.
- axis 3: covered — package files only; one changelog fragment per card.
- axis 4: n/a — no FR text, debt row or principle changed.
- axis 5: covered — «The first look»: both roads (C1 `phases/s3.md` + driver call one function); the walker's four places named in A2
  (only survey changes, by design); «How the stand logs in»: C1 appends the sixth carrier (amendment 13); «Acquisition ladder»
  (`env_probe`): D1, WAITING.
- axis 6: covered — `knowledge_use` counts first-look markers as sets of R-n (per-item lines do not inflate it, critic Key 13); the
  registry way carries `[knowledge:environments.sign_in]` (B2); whether the counter counts it: B2 reports; residual node FV1-28f.
- axis 7: n/a — no test identity.
- axis 8: n/a — no story path; the registry path is the existing `qa-factory/records/project-knowledge.json`.
- axis 9: n/a — no test-file recognition.
- axis 10: n/a — no git-top reader.
- axis 11: n/a — no shell-command recognizer.
- axis 12: covered — the node rows in batch-1 are the Lead's; no new pile file by a builder.
- axis 13: n/a — dispatch text cut unchanged.
- axis 14: n/a — no transcript reader.
- axis 15: n/a — no console stream setup.
- axis 16: covered — every JSON read through `hooklib.read_json` / `first_look.data()` / the existing readers.
- axis 17: n/a — no detector verdict shape.
- axis 18: covered — census ceilings: a possible raise of `safety` (A1) and `blocking_per_role.*` (A1, C1) is NAMED with
  `judgment: adds data check ...` (both worlds in §1b); no other ratchet moves.
- axis 19: n/a — no `tools:` line.
- axis 20: n/a — no host receipt.
- axis 21: n/a — no markdown table reader.
- axis 22: n/a — no host return form.
- axis 23: n/a — no `tests[]` field.
- axis 24: n/a — no run join.
- axis 25: n/a — freshness predicates untouched (a stale first-look record keeps `first_look.read`'s meaning).
- axis 26: covered — the word `stand not confirmed` untouched; S6 `s6_no_stand` named as a sibling, unchanged.
- axis 27: n/a — no test-row profile.
- axis 28: n/a — no row-form render site.
- axis 29: n/a — no jsonl append added (brief-sizes is the existing writer).
- axis 30: n/a — no profile commands.
- axis 31: covered — the role carrier for "first look before discovery" stays `agents/qa-automator.md` (FV1-29 owns edits); the form
  section of A1 is the walker's carrier for `sign_in` (one owner: `artifact-contract-first-look.md`).
- axis 32: covered — §1b: every check is shape / xref / safety on data; judgment stays with the role and the tier above; intent with
  the person (`revoke`).
- axis 33: n/a — dispatch identity untouched.
- axis 34: covered — one road: the gap text is one for every reader (per-reader clause is a data row keyed by the brief kind, not a
  branch on a language or project); the way in has one store, one writer, one reader and ONE precedence order read by D1 and FV1-28e
  (amendment 11); the ui-only case is the person's data word `access.kind: ui_only` (FV1-17), not a second road (amendment 9b); the
  survey-only provenance branch is keyed by the walk PLACE (a capability of the walk: observation vs evidence), stated in A2; residuals
  FV1-28e (walker recipe) and D1 are named nodes with owns.
- axis 35: covered — registry rows of sides untouched; the same writer reused.
- axis 36: n/a — placeholder rows untouched (B1 keeps the s5 head's placeholder sentence).
- axis 37: n/a — no repeat stop or `Driver.record_repeat` site touched.

## §5a Four questions (rule 10), per mechanism

- A1 (due + form): (a) one paid S3 walker dispatch on stories with a refused probe (the free agent spent 6.5 min on the same look,
  finding `:14`); the role pays a few lines of `sign_in`. (b) §5. (c) `test_first_look_step.py` scenario row, `test_first_look.py`
  table; dry row `first_look/probe_405`; live row §4. (d) `due` is called by `first_look_step` on every S3 entry; `put_problems` on
  every `put`.
- A2 (survey open): (a) none beyond the walk itself; a wrong True would cost a false observation (error direction toward False).
  (b) §5. (c) `test_walk_survey_place.py` row; live row §4. (d) `_open_actors` runs on every walk open.
- B1 (lines): (a) brief bytes per window (measured in the DoD; brief outside U/H); paid by the automator's context. (b) §5. (c)
  `test_first_look_briefs.py`; dry rows `empty`/`absent`. (d) `build` calls it for every S3-S7 brief.
- C1 (record): (a) one registry row per new way; a person revokes a wrong one. (b) §5. (c) `test_project_knowledge.py` join row; dry
  row `entry_recorded`. (d) the driver calls `record_sign_in` after acceptance; the skill road's phase line names the command —
  ON DISCIPLINE for the skill road (the conductor may skip the command); detector for that leak: the dry row `entry_recorded` run on the
  skill road, else a registry with no `environments.sign_in` row after an accepted look with `sign_in` (calibration: queued to the Lead
  as a check-33 question).
- B2 (lines): (a) one line per recorded way; (b) §5; (c) `test_first_look_briefs.py` join row; (d) `build`.
- D1 (precedence): (a) none beyond today's probe; (b) §5; (c) D1 rows, live row; (d) the probe runs at S0/S5 by code.

## §6 NEW forks (returned; recommendation first; what stays executable before the answer)

- **F-8 — B1's own-`sign_in` part depends on A1, both in wave 1.** B1 item 6 reads `first_look.read()["sign_in"]`, which only A1
  creates; B1's join row (3) cannot pass on a tree without A1. (A, recommended) B1 is worked in parallel with A1 and MERGED after A1
  (`очередь: A1 → B1` for the merge only); B1's builder merges `main` with A1 into its tree before its witness run; if A1 is not merged
  when the rest of B1 is done, B1 waits for that one merge (cost: B1's tail waits for A1; no file is shared). (B) move item 6 and row (3)
  into B2 (wave 2: no dependency problem, but the Lead's decision 2 puts it in B1). (C) serialise B1 entirely after A1 (loses the
  parallel wave). Executable before the answer: everything in B1 except item 6 / row (3).
- **F-9 — a survey walk when the profile has NO runtime probe registered** (`stand_probe` raises "no runtime probe for profile ...",
  cause `build`, before any record exists). The build is as unknown as an `unknown` record, and P5 says a gap the factory itself found is
  a default, not a question; but the critic's binding wording names only an "unknown runtime provenance". (A, recommended) refuse as
  today in A2 (the error direction of A2 is toward refusal; a project with no probe gets the person's door it gets today) and open a
  question to the owner/Lead whether "no probe at all" opens a survey as `not_established` too. (B) open it in A2 as well (cost: one more
  row and a `provenance`-less branch; risk: a project with no probe never states its build anywhere). Executable before the answer: A2 on
  (A).
- **F-10 — the skill road's call to `record-sign-in` is on discipline only.** The driver calls the function in code; the skill road's
  conductor must run the phase line. (A, recommended) accept it for now with the detector named in §5a (C1 (d)); promote to a code gate
  (e.g. `story_step.py finish` of the first-look dispatch calling `record_sign_in`) only on a measured leak (rule 10 (d)). (B) wire it
  into `story_step.py finish` now (cost: a third file in C1 on the hot `story_step.py` path, and a second caller to keep in step).
  Executable before the answer: C1 on (A).

## §7 Test files named — checked against `test-layers.json` and `slow_tests.json` (read-main)

| File | test-layers.json | slow_tests.json | Used by |
|---|---|---|---|
| `test_first_look_step.py` | keep, `scenario` (covers `driver_stage_plan.py`, `first_look.py`, `controller.py`) | not listed | A1 |
| `test_first_look.py` | keep, `gate_named` (covers `first_look.py`, `walk_session.py`, `first-look-statuses.json`) | not listed | A1 |
| `test_walk_survey_place.py` | keep, `scenario` (covers `walk_session.py`, `manual_capture.py`) | not listed | A2 |
| `test_first_look_briefs.py` | keep, `data_join` (covers `brief_pack.py`, `app_card.py`, `first_look.py`) | not listed | B1, B2 |
| `test_project_knowledge.py` | keep, `register` | not listed | C1 |
| `test_http_client.py` | keep, `table` | not listed | D1 (WAITING) |
| `test_manual_capture.py` | keep, `detector` | **slow 10.6 s** | FV1-28e (canon only) |
| `test_brief_pack.py` | keep, `detector` | **slow 34.6 s** | printed for B1/B2: canon only |
| `test_judgment_census.py` | keep, `register` | **slow 33.3 s** | census rows: canon only (the draft asked the builder to run it: removed) |
| `test_config_migration.py` | keep, `detector` | **slow 17.7 s** | C1 if printed: canon only |
| `test_state_exits.py` | keep, `detector` | not listed | C1 if printed |
| `test_app_card.py` | **quarantine** | — | never run or edited (B2 uses `test_first_look_briefs.py`) |
| `test_stand_access.py` | **quarantine** | — | never run or edited (D1) |
| `test_brief_pack_manual.py`, `_roles.py`, `_sd_head.py`, `_timeout.py` | **quarantine** | — | never run or edited |

No new test file is asked for anywhere.

## §8 Small choices closed by the designer

- C-1: the provenance record reaches the survey branch as an attribute `EnvBlocked.provenance` set in `_stand_blocked` (not in `row`,
  which is persisted; not a new `stand_probe` keyword, which would change a shared gate's signature).
- C-2: a story-recorded `http` way refuses `access.kind` `harness_command` and `none` (a role-written command would later run on every
  probe; `none` contradicts a way in). The Lead may lift it.
- C-3: the secret-literal check covers SECRET values only (a user name is a handle; matching it would refuse selectors such as
  `#admin-panel`); secrets under 4 characters match as whole tokens only (a one-character secret would refuse every text).
- C-4: `SIGN_IN_PRECEDENCE` levels are named `recorded`, `project`, `factory_default`; `project` = `environment.access` for http readers
  and `manual_capture.login.ui` for ui readers — the one order amendment 11 asks for, applied to both surfaces.
- C-5: `evidence`, `quote` and `req` are REQUIRED in a `sign_in` (the critic allowed "derived or required"; explicit beats parsing a path).
- C-6: a STALE record's `sign_in` is not rendered (a stale record confirms nothing).
- C-7: the all-access line applies to the author kinds `s4` and `s5` (the kinds whose body is path items); S3/S7 see those rows through
  their red-row lines as today.
- C-8: the B2 app-card row lives in `test_first_look_briefs.py` (its `covers` already lists `app_card.py`; `test_app_card.py` is
  quarantined).
- C-9: limits 20 x 300 for steps, 500 for url/selectors/fragments, 20 entries for lists, 400 per brief item, 600 per sign-in line.
- C-10: worktree names `fv1-28-a1`, `fv1-28-a2`, `fv1-28-b1`, `fv1-28-c1`, `fv1-28-b2`, `fv1-28-d1`.

## §9 Contradictions found (reported, not widened)

- Critic Key 13 / amendment 13 "the current map has 36 axes; drop axis 37": read-main `ba903eb` has axis 37 (`A repeat stop`, line 620);
  the 36 is the root checkout's (stale). §5 keeps axis 37 as n/a.
- The draft's DoDs asked builders to run `test_judgment_census.py`; it is in `slow_tests.json` (33.3 s): never run locally (PROJECT.md
  package change p. 2, builder-rules 7b). Removed from every DoD.
- The draft's F21 cited `test_first_look.py` etc. by line; the critic found them off by one on main; this redraft cites no line numbers.
- Lead decision 2 calls FV1-5 "in main"; not verifiable here (read-main behind, no git); D1 stays WAITING on both.

## §10 What I did NOT establish

- The per-file difference between read-main `ba903eb` and origin/main `1a00352` (no git command); function names were taken from
  read-main and, for `driver_stage_plan.py`, confirmed by the critic at `7379e0d`.
- Whether `runtime_probe`'s `NO_EXPECTED_REVISION` record carries `asks_person` (A2 refuses it either way).
- Whether `controller.Controller(task_root).state()` is side-effect free (C1 item 5 names the fallback).
- The exact fields of the object `manual_capture.read_login` returns (A1 item 3: the builder reads and names them).
- Whether any reader of `probes.jsonl` rows rejects an unknown key `taken` (A2 handoff asks for the Grep).
- Whether `report_facts.knowledge_use` counts `[knowledge:environments.sign_in]` (B2 handoff; residual FV1-28f).
- Whether the census scan makes `sign_in_secret_faults`, `_open_actors` or `record_sign_in` units (both worlds stated in §1b).
- Whether the `scenario_walk.py --witness-for` takes package-relative or repo-relative paths (the DoDs use the package-relative form of
  the accepted draft; the builder uses the form its `--help` names).
- The S5 automator's brief: whether it names a stand tool today (B1 gives S5 the "name it as a gap" clause until FV1-29).
- origin/main's SIBLING_MAP axis count.

## §11 Reading trail

Read whole: the draft `docs/tasks/specs/20261114-fv1-28-first-look-to-automator-spec.md`; the critic
`docs/tasks/specs/reviews/20261114-fv1-28-plan-critic.md`; `docs/TESTING.md`; read-main `ai-packages/qa-factory/scripts/first_look.py`;
read-main `ai-packages/qa-factory/scripts/slow_tests.json`.
Read in part (read-main `ba903eb`): `walk_session.py` (def list; `capture_cited`; `_Sink`, `Walk.__init__`; `start`, `_start`,
`_surface_profile`, `_open_actors`, `_open_actor_http`, `_open_actor`, `_shutdown`, `_new_attempt`, `_open_item`);
`manual_capture.py` (`EnvBlocked`, `_other_profile_remedy` tail, `_stand_blocked`, `stand_probe`, `_session_cycle(_held)` head, the
`http` capture head); `profile_contract.py` (`image_identity`, `validate_runtime_provenance`, `person_confirmed`, `ACCEPTS`,
`acceptable_provenance`); `runtime_probe.py` (docstring rungs; `confirmed_by_row`, `nothing_answered`, `finish`, `finish_unknown`);
`driver_stage_plan.py` (first-look def list; `_first_look_accepted`, `_first_look_give_up`, `_first_look_walk`); `driver_core.py`
`controller_state`; `project_knowledge.py` (def list; `lessons` through `notice_from_handoff`); `brief_pack.py` (`first_look_input_line`
through `first_look_lines`; `build` from the S5 kind to the input names; `walk_brief_lines` head); `app_card.py` (header through
`_signin`); `driver_dispatch.py` (the S6 walk-lane app-card call); `config_contract.py` (`ACCESS_KINDS`, `access_errors` head);
`skills/qa-story/phases/s3.md` (lines 10-57); `judgment-census.json` (head, `ratchet`, rows of the node files);
`scripts/tests/test-layers.json` (keep rows of the named files, cohorts, the `quarantine` rows named in §7);
`plans/builder-rules.md` (7, 7a, 7b); `docs/SIBLING_MAP.md` (axis headings; axis 5 table; axis 6 table); `tools/architecture_gate.py`
(docstring items 3-8); the stand-login spec (Grep of `form_login|try_roads|recorded_login|ui_only|F6|harness_command|lockout|...`;
items 3-6 at its lines 203-230).
Git state: `.claude\worktrees\read-main\.git`, `.git\worktrees\read-main\HEAD`, `.git\refs\remotes\origin\main`, `.git\FETCH_HEAD`,
`.git\packed-refs` (Grep).
Searches with controls: `^#+ .*[Aa]xis \d+` over read-main SIBLING_MAP (37; control: Axis 1 hit) and `^#+ .*[Aa]xis 3[4-9]` over the
root SIBLING_MAP (3 hits: 34-36); `stand_probe\(` over read-main `scripts/*.py` (7; control: the definition itself); `slow_tests.json` Grep
for node names (2 brief_pack hits; then the whole file read); test-layers Grep of the named files (control: `"quarantine"` key found);
Glob over `.claude\worktrees\read-main` returned nothing even for a known file (`test-layers.json`) — Glob does not search that tree, so
no negative claim rests on a Glob; every file claim above rests on Read or Grep.
Not read: `report_facts.py`, `env_probe.py`, `stand_access.py`, `agents/qa-automator.md`, `agents/qa-runner.md`,
`references/artifact-contract-first-look.md`, `references/first-look-statuses.json` (A1 adds keys to both; their present text was read
by the draft, trail there), the P1-b harness spec, origin/main files.
