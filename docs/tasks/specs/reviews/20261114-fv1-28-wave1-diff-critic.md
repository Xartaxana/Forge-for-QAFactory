# FV1-28 wave 1 — code critic on cards A1 and A2 (t-783)

Critic (Opus), 14.11.2026. Diffs: A1 `302180ff` (wip/fv1-28-a1), A2 `01136cc2` (wip/fv1-28-a2), both cut from `e4df9c0f`; origin/main = `2cf488ad`.
DoD: the spec's cards A1/A2 (`docs/tasks/specs/20261114-fv1-28-cards-redraft-spec.md`), with the Lead's choices F-8 A, F-9 A, F-10 A. This verdict is input to acceptance; the Lead accepts.

## Verdict lines

- **Card A1: needs_work — 1 blocker, 7 binding fixes.** Empirics: a literal account password in `sign_in.why` gets written to `work/first-look.yaml` (and C1 will later carry `why` into the registry as `words`).
- **Card A2: accept_with_fixes — 0 blockers, 3 binding fixes.** The code is right for the DoD. The docstring, changelog and commit say "a dead stand still refuses", and that is false for stands with no container. The witness does not cover all of the DoD's run.
- The cards merge independently. A1 and A2 touch disjoint files, and each merges clean onto `2cf488ad` (`git merge-tree`). Merge order: A1 before B1 (F-8). A2 is not ordered against the others.

## (b) A1 — empirics first: adversarial `sign_in` records through `first_look.put`

I used the A1 worktree, a temp story built with the test's own `Story` fixture, and `read_login` faked to return the password `S3cr3t-pw-9`. The verbatim output is in the Trail. Result per spelling:

| Spelling | Written? | Secret in `first-look.yaml`? |
|---|---|---|
| literal password in `steps` (control) | refused | — |
| literal password in **`why`** | **written** | **yes** |
| password in other case (`S3CR3T-PW-9`) in `steps` | written | yes |
| password URL-encoded (`S3cr3t%2Dpw%2D9`) in `url` | written | yes |
| `user:pass@` in url; `?token=`; `PASSWORD=`; `Bearer x`; bare JWT | refused | — |
| `?access_token=…`, `?session=…`, `Cookie: JSESSIONID=…` | written | yes (scrub's `_KEYWORD` has no `cookie`/`session`, and `\btoken` cannot fire after `_`) |
| an unknown key under `landed` holding a password | refused (unknown key) | — |
| http `access: {}`, `access: {kind: ""}`, `access: {foo: bar}` (builder Q1) | **written** | n/a: an http "way in" with no kind |
| `access` extra key `token: <18- or 30-char token>` | written | yes (only the value gets scanned, never its key; `tokens=False`) |
| `access.url` of 5000 chars (builder Q2) | written (5991-byte record) | n/a: no limit |

Decisions on the builder's three questions:
- **Q1:** refuse. A way in that is required for http must name a `kind`. `access_errors` tolerates an empty kind only for an onboarding config, and D1 will later run this object.
- **Q2:** add a limit. Every string leaf of `access` gets `SIGN_IN_TEXT_MAX`, with rows AT and BEYOND it. The limits that exist all have AT/BEYOND rows (steps 20/21, line 300/301, url 500/501, selector 500/501, url_not 20/21, fragment 500/501).
- **Q3:** keep it. `sign_in: ""` refused as "a mapping" is what the spec edge says ("a string -> refused").

### Findings A1

**A1-1 BLOCKER: the literal-secret check skips required free-text fields.**
- Where: `first_look.sign_in_secret_faults` scans only `SIGN_IN_SECRET_FIELDS = (url, steps, fields, landed, access)`. `why`, `quote`, `actor`, `req`, `evidence` and every dict KEY go unread.
- Failure: `why: "I typed S3cr3t-pw-9 and landed"` gives `written=True` and the record holds the password.
- The census note the diff adds says "no account value is ever stored". That annotation is false.
- **Fix:**
  - Run part (b), the literals, over `_leaves(sign_in, "sign_in")` (every string leaf), and also over the dict keys.
  - Run part (a), `scrub`, over `SIGN_IN_SECRET_FIELDS` plus `why`.
  - Test rows in `sign_in_battery`: "a literal account secret in why" refused; "… in quote" refused. Neither problem text may contain the value.

**A1-2 binding: literal matching is case- and encoding-blind.**
- Where: `_holds_secret` does `secret in text`.
- The spec's error direction is over-refusal, so a folded compare stays inside it.
- **Fix:** compare `secret.casefold()` against both `text.casefold()` and `urllib.parse.unquote(text).casefold()`. Apply the same rule to secrets shorter than 4 characters, as whole tokens.
- Rows: the password in upper case inside `steps` is refused; the `%2D`-encoded password inside `url` is refused.

**A1-3 binding (builder Q1): the http `access` shape is open.**
- Where: `_sign_in_access_faults`.
- **Fix:**
  - Refuse an empty or absent `kind` with "`sign_in.access.kind` names how the request signs in (one of …)".
  - Refuse any key outside a data list `sign_in_access_keys` in `first-look-statuses.json`: `kind`, `url`, `client_id_key`, `realm_key`, `user_key`, `secret_key`, `token_key`, `user_field`, `secret_field`, `unauth_status`. The key fields come from `config_contract.ACCESS_KEY_FIELDS` and `BODY_FIELD_KEYS`.
- Rows: `access: {}` refused; `kind: ""` refused; an extra key `token: <value>` refused.

**A1-4 binding (builder Q2): no limit on `access` strings.**
- **Fix:** apply `_text_limit_faults(v, SIGN_IN_TEXT_MAX, "sign_in.access.<k>")` to every string leaf of `access`.
- Rows: `access.url` at 500 written; at 501 refused.

**A1-5 binding: refusals echo a value that may be the secret.**
- Where:
  - `_sign_in_faults` prints `got {str(actor)[:40]!r}`, `got {str(surface)[:40]!r}` and `got {str(req)[:40]!r}`.
  - `unknown key {k}` prints the key name.
  - `actor` is not among the scanned fields.
- Failure: `actor: S3cr3t-pw-9` produces a refusal that contains the password. That breaks the spec edge "the refusal never prints the value".
- **Fix:** compute the account secrets first. Print every got-value and every unknown key through a `_shown(v, secrets)` that returns `[not printed]` when `_holds_secret` fires or `scrub` changes the value.
- Row: `actor` = the secret is refused, and the problem text lacks it.

**A1-6 binding (census, JUDGMENT): the class is declared below what the census rule requires.**
- The `put_problems` unit now holds a secret guard, and the row's own note says so ("+ safety"). The census rule E-A2 says that when two readings meet on one unit, the HIGHER wins: safety > xref (`test_judgment_census.py:35-36`, `higher_class`).
- Keeping the row at `xref` with a note is the cheap way past the `safety` ceiling (brief item 11).
- **Fix:**
  - Set the row `first_look.py put_problems` to `"class": "safety"`.
  - Raise `ratchet.safety` 86 → 87. It is 86 on both the A1 tree and `2cf488ad`.
  - Commit line: `judgment: adds data check first_look.put_problems (sign_in_secret_faults) -- a guard: no account value is ever stored`.
- This contradicts the spec's §1b "world B". The Lead accepted that text, so the call is the Lead's. My recommendation is the fix.

**A1-7 binding (AR-1, DUPLICATION AND CONSISTENCY): closed lists sit in code, and an AR-1 test was weakened to allow it.**
- Where:
  - `SIGN_IN_FIELDS_KEYS`, `SIGN_IN_LANDED_KEYS`, `SIGN_IN_UI_ONLY`/`SIGN_IN_HTTP_ONLY` and `SIGN_IN_HTTP_REFUSED_KINDS` are lists in `first_look.py`.
  - `first-look-statuses.json` `note` says the module "holds none in code".
  - The builder exempted the line `SIGN_IN_ACCESS = ` from `test_statuses_file_is_the_one_home_of_the_words`.
- **Fix:**
  - Add data keys `sign_in_surface_keys` (`{"ui": ["fields","landed"], "http": ["access"]}`), `sign_in_fields_keys`, `sign_in_landed_keys` and `sign_in_http_refused_kinds`, read through `_words`/`data()`.
  - Drop the constants and the test exemption.

**A1-8 binding (DoD witness of the fix round):** re-run `test_first_look.py` and `test_first_look_step.py` and attach the output verbatim.

What holds in A1, by tracing:
- **`due`.** The order is kept: parks → register unreadable → empty → `environment` empty → attempt. `null: no_stand` writes no attempt (`put` docstring and code), so a story that already holds `no_stand` walks on the next S3 entry. That is the TEMPORAL edge.
- **Old records.** A record with no `sign_in` reads `{}`, and so does a non-mapping on disk (tested).
- **`put --null`.** It writes no `sign_in`.
- **Scenario row.** `test_pending_probe_does_not_skip_the_walk` would fail on the old `due`, so it kills the defect the node exists for.

## (c) A1 x A2: which states end where (AR-25, AR-28, FR-59)

Readers of `due` and `no_stand`:
- `driver_stage_plan.first_look_step` / `_first_look_null`.
- `first_look._show`.
- The skill road `phases/s3.md:50`: the `--null` word list does not change.

`stand_check` is S5/S6-only (`driver_stage_s5.py:201,330`, `driver_stage_s6.py:444`), so it does not gate S3. S6 `s6_no_stand` reads `environment_pending` itself, unchanged.

| Story | Before | A1 alone | A2 alone | A1+A2 |
|---|---|---|---|---|
| no stand named | `no_stand` | `no_stand` | `no_stand` | `no_stand` |
| named, pending, probe accepted (matched / person word) | `no_stand` | walk | `no_stand` | walk |
| named, pending, `unknown` + `asks_person` | `no_stand` | open fails → retry → `walk_not_opened` | `no_stand` | walk, `taken: not_established` |
| named, pending, `mismatched` / docker down / device / no revision | `no_stand` | `walk_not_opened` | `no_stand` | `walk_not_opened` |
| named, confirmed, `unknown` + `asks_person` | `walk_not_opened` | same | walk, `not_established` | walk, `not_established` |

No cell turns an unknown into a pass. Every non-walk is a named null, and a walk on an unknown build is recorded `not_established`. **A1 is safe to merge before or without A2.**

## (d) A2 — findings and checks

**A2-1 binding: the docstring, changelog and commit claim something false.**
- `survey_opens_on` says "the stand answered (`asks_person` set)". The changelog and commit say "a dead stand … refused as before".
- `runtime_probe` contradicts this:
  - rung 8 is "nothing answered: `unknown` … `asks_person: how`" (`runtime_probe.py:48`);
  - `finish_unknown` sets `how` unless the run was stopped or docker alone was down (`:1297-1299`);
  - docker rungs run only when a container is named (`docker_ok = bool(ns.container)`, `:663`);
  - a failing registry command sets `command_failed` (`:1070`), which still asks `how`;
  - `runtime_probe` makes no HTTP call (Grep `urlopen|subprocess`: only docker and command subprocesses).
- So on a stand with no container, or one whose registry command fails because it is down, a survey walk now OPENS. It is recorded `not_established`, and the walker records `unreachable/access` rows.
- This error direction is not the one spec F9''' assumed, and it also breaks A1's edge "a really dead stand fails at `walk_session open`".
- **Fix (text only):** say that `asks_person` means "no rung could read or tie the build" (not "the stand answered"). Correct the changelog and the commit body.
- Whether a paid walk on a possibly dead container-less stand is acceptable is a **question to the Lead** (queue line Q4). The code is not changed in this round.

**A2-2 binding: the witness is incomplete and partly paraphrased.**
- The DoD command is `--witness-for scripts/walk_session.py scripts/manual_capture.py`. I re-ran it, and for `manual_capture.py` it prints four fast keep files that are not in `slow_tests.json` and not quarantined: `test_exploratory_findings.py`, `test_gate_role_accounts.py`, `test_manual_evidence.py`, `test_state_exits.py`.
- The report says they were "not in the DoD's named run". That is false.
- The scenario_walk output was retold ("printed 9 files"), not pasted.
- **Fix:** run those four files and paste the scenario_walk output verbatim. Name the slow files (`test_check_delivery`, `test_gate_preflight`, `test_gate_registry`, `test_manual_capture`, `test_profile_reader`, `test_role_commands`, `test_runtime_paths`, `test_story_run_s6`, the three scenarios) as "judged by the batch canon".
- By reading, none of them can turn red: the only change in `manual_capture` is a new attribute. `.row` is unchanged, and no reader of `.provenance` exists outside `walk_session.py:1274,1371-1372` (Grep).

**A2-3 binding (CODE QUALITY):** `walk_session.py`, `Walk._shutdown`: `ends =[r for r …` should read `ends = [r for r …`.

Checked and holding:
- **Only survey opens.** The branch is inside the `EnvBlocked` handler and is gated `self.place == SURVEY and …` before anything else. Case and settle walks are refused (rows `case_place_unknown_asks`, `settle_place_unknown_asks`); control takes the same branch.
- **Other probe callers are untouched.** The standalone captures call `stand_probe` at `manual_capture.py:3341,3358,5393,5439` and never read `.provenance`. `driver_machine.stand_probe` is a different function.
- **Both producers carry the record.** The two `_stand_blocked` producers (`:1608` ProvenanceRefused, `:1613` refused value) both tag it. F-9 A holds: "no probe" is raised at `:1598` without `provenance`, so it is refused.
- **No duplicate start row.** `stand_probe` raises before `attempt.probe` (`:1612-1614`), so the survey branch writes the only start row.
- **`EnvBlocked.row` is unchanged.**
- **Readers of `probes.jsonl`:**
  - `driver_dispatch.walk_facts`: case lanes only, reads `observed_runtime_identity` of the start row;
  - `manual_capture.profiles_of`/`attempt_profiles`;
  - `manual_evidence._recorded_walks`.
  - None reads `taken`, so the field has no reader (AR-22, queue line Q3).
- **Census:** no row is owed. `_open_actors` and `survey_opens_on` do not match `UNIT_NAME_RE`, and no refusal site is added.

## (e) P27 / AR-29

- A1: `due` no longer decides by a probe guess. `_sign_in_faults` judges shape, xref and secrets, never whether the way in is right.
- C-2 (no `harness_command`/`none`) is a safety rule on data.
- A2 opens on FIELDS of the record (FR-12).
- No judgment moves into code. The census CLASS of A1 is wrong (A1-6), but its owner is not.

## (f) Class-wide completeness, DUPLICATION, CODE QUALITY, ONE ROAD

**Surface "the secret guard of role text" (A1), neighbour classes walked:**
- magnitude: `access` unbounded (A1-4);
- nesting: keys unread, `access` open (A1-1, A1-3);
- encoding: case and URL-encoding (A1-2);
- empty: `access: {}` (A1-3).

**Same surface outside the diff:** rows' `why`/`quote`/`path.api.sample.response` have no guard (the builder noticed it): Q2.

**DUPLICATION AND CONSISTENCY:**
- The guard reuses `app_card.scrub`, which is the one scrubber (good). Its keyword gap is Q1.
- The literal set takes only `read_login().password`. `machine_facts.secret_values` (`machine_facts.py:338`, all `secret_keys`) and the project's `secret_content_patterns` (`manual_capture.secret_pattern_hit`, `:575`) are existing readers that the guard ignores. That is a queue line before C1 (Q5), because the spec prescribed `read_login`.
- The leaf walk `_leaves` duplicates `stage_joints._leaves` (`stage_joints.py:98`), but with paths. It is small, so I raise no finding.
- Grep for more: `def (\w*secret\w*|\w*redact\w*|\w*leaves\w*)\(` over `scripts/`.

**CODE QUALITY:**
- `_sign_in_faults` is about 48 lines with nesting ≤ 3, and has no dead branch.
- A2-3 is the whitespace fix.
- None else found.

**ONE ROAD (P31):** none found. A2's branch is keyed by the walk place (observation vs evidence), the shared `stand_probe` is still reached, and the spec states the reason. A1 has no branch on a language or project. Grepped: `place ==` in `walk_session.py`, and the A1 diff.

**SIBLING_MAP:**
- Axis 5 «The first look»: both roads read `due` (the skill road through `show --json`), with no text change needed. The four walk places were checked: case and settle by test, control by the shared branch.
- Axis 18: census → A1-6.
- Axis 26: unchanged.
- Axis 34: as above.

**Census conflicts:**
- `judgment-census.json` is the same on `e4df9c0f` and `2cf488ad` (`git diff --stat` is empty for every owned file), and both branches merge clean.
- A2 does not touch the census.
- A1-6 changes line 4 (`ratchet`). B1 and C1 may change it too, and the later merge resolves it.

## (g) Slow and quarantined files, by reading

- **A1:** the three scenarios (`cart-1`, `local-1-0108`, `local-1-arm-b`) all have `environment_pending: false` in `pipeline.json`, so `due` is unchanged for them. `read()` gains `sign_in: {}`, and the only readers of `FL.read` in tests are the three fast files that ran green. `test_judgment_census.py` stays green as written, but would turn red after A1-6 unless the ceiling rises in the same commit.
- **A2:** `test_manual_capture.py:582,584,2373` assert `_stand_blocked(...).row`, which is unchanged. I expect no red.

## Queue lines (pile form)

- Q1 `app_card.scrub` misses `access_token=`, `session=` and `Cookie:`/`JSESSIONID=`: `_KEYWORD` lacks cookie/session, and `\btoken` does not fire after `_` (empirics above). The refusal text promises "cookie". | перенос: live-run-fvf, следующая невзятая пачка (находка «единый scrub пропускает cookie/session/access_token») | обоснование: `app_card.py` is not in A1's owns, it is shared by every card reader, and over-redaction is the safe direction | подтвердил: —
- Q2 Secret guard on the first-look ROWS' free text (`why`, `quote`, `path.api.sample.response`): the same class as A1-1 | перенос: live-run-fvf, следующая невзятая пачка | обоснование: rows were outside card A1. The class is named, and the fix reuses `sign_in_secret_faults` | подтвердил: —
- Q3 `probes.jsonl` `taken: not_established` has no reader (AR-22). Name its reader (the first-look record or the S3 brief), or declare it evidence-only in the manual-capture contract | перенос: live-run-fvf, следующая невзятая пачка | обоснование: the spec created the field without a reader. It is not the builder's defect | подтвердил: —
- Q4 Spec premise F9''' is false. `asks_person: how` also covers a stand with no container, or a failing registry command, so a survey walk can open on a dead stand. Lead question: accept that (the walker records access rows and the cost is one paid walk), or require a live answer (FV1-5 / D1 `env_probe`) before a survey opens on `not_established` | перенос: live-run-fvf, вопрос Lead к узлу FV1-28 D1 | обоснование: this is an error-direction decision, the Lead's (rule 6) | подтвердил: —
- Q5 The literal set of the secret guard: add the project's `environment.secret_keys` values (`machine_facts.secret_values`) and `secret_content_patterns` (`manual_capture.secret_pattern_hit`) before C1 reuses the guard for the cross-story registry | перенос: live-run-fvf, узел C1 (предусловие) | обоснование: the spec prescribed `read_login` only, and the registry outlives the story | подтвердил: —

## Trail

Read:
- the spec (§0-§2, cards A1/A2/B1/C1, §3, §5-§8) and `critic-diff-brief.md`;
- both builder reports;
- `git show` of both commits (full diffs: `first_look.py`, `first-look-statuses.json`, census row, `artifact-contract-first-look.md`, `test_first_look.py`, `test_first_look_step.py`, `walk_session.py`, `manual_capture.py`, `test_walk_survey_place.py`);
- `manual_capture.py` 196-215, 1544-1615;
- `walk_session.py` 1240-1314, `capture_cited` 569-614;
- `runtime_probe.py` 20-59, 1220-1314 and Grep `asks_person`, `command_failed`, `urlopen|subprocess`;
- `profile_contract.py` 730-755, 809-918, 1044-1060;
- `driver_stage_plan.py` 61-75, 183-262;
- `driver_stage_build.py` 94-140, 236-262;
- `driver_sources.py` 722-745;
- `driver_machine.py` 3955-3975;
- `driver_dispatch.py` 1549-1570;
- `app_card.py` 55-85;
- `config_contract.access_errors`;
- `test_judgment_census.py` 35-36, 75-101;
- `role-load.json`;
- `SIBLING_MAP.md` axis 5 row;
- `slow_tests.json` and `test-layers.json` membership of the printed files;
- Grep `no_stand|\.due\(` and `environment_pending` (package, non-test), and `stand_probe\(|_stand_blocked\(`.

Positive controls: the `no_stand` Grep finds `first_look.py:876`; the `.provenance` Grep finds the new lines in `manual_capture.py:1562`.

Re-runs (verbatim tails):
- `( cd …/fv1-28-a2/ai-packages/qa-factory && python -B scripts/tests/test_walk_survey_place.py )` → `=== test_walk_survey_place: 159/159 ok ===` (matches the report)
- `( cd …/fv1-28-a1/ai-packages/qa-factory && python -B scripts/tests/test_first_look.py )` → `=== test_first_look: 381/381 ok ===` (matches the report)
- `scenario_walk.py --witness-for scripts/walk_session.py scripts/manual_capture.py` (A2 tree) → 27 lines, 15 under `manual_capture.py` (listed in A2-2)
- `git merge-tree --write-tree 2cf488ad 302180ff` → clean; `… 2cf488ad 01136cc2` → clean. The chained third call was misinvoked (a tree passed as a commit), so the pair is judged by disjoint `--stat` file sets instead.
- Probe through `put` (stdin payload, temp dirs only), verbatim:

```text
control: clean ui: written=True leak=[]
control: literal secret in steps: written=False
secret literal in why: written=True leak=['S3cr3t-pw-9']
secret literal other case in steps: written=True leak=['S3CR3T-PW-9']
secret url-encoded in url query: written=True leak=['%2Dpw']
url userinfo / url token= / PASSWORD upper pair / bearer / JWT bare: written=False
url access_token= query: written=True leak=['Zq81Lm02Kd77']
url session= query: written=True leak=['8F3A2B1C9D0E']
cookie in steps: written=True leak=['8F3A2B1C9D0E']
other-credential 28-char token bare in steps: written=True leak=['Zq81Lm02Kd77']
secret in a nested landed key: written=False (unknown key `password`)
selector holds a non-account literal: written=True leak=['hunter2']
http access {} (q1): written=True ; http access kind empty (q1): written=True ; access only unknown keys: True
http access extra key bare token / 30-char token: written=True leak=['Zq81Lm02Kd77']
access.url 5000: True [] 5991
```

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "A1-1: first_look.sign_in_secret_faults checks literal account secrets only in url/steps/fields/landed/access; a password in sign_in.why (also quote, actor, req, keys) is written to work/first-look.yaml (empirics: written=True, leak S3cr3t-pw-9); fix: literal check over every leaf and key, scrub over SIGN_IN_SECRET_FIELDS + why, battery rows why/quote refused"
  ],
  "class_completeness": "Secret-guard surface walked: magnitude (access strings unbounded, A1-4), nesting (keys unread and access open, A1-1/A1-3), encoding (case and URL-encoding, A1-2), empty (access {} accepted, A1-3). Same class outside the diff queued: rows' free text (Q2), scrub keyword gap (Q1), project secret_keys/secret_content_patterns (Q5, before C1). A2: all four walk places checked (case/settle by rows, control by the shared branch); every stand_probe/_stand_blocked caller walked; SIBLING_MAP axes 5/18/26/34 walked; spec premise F9''' wrong, queued Q4.",
  "fixes": [
    "A1-1 (blocker) first_look.sign_in_secret_faults: literal check over _leaves(sign_in) and dict keys; scrub over SIGN_IN_SECRET_FIELDS + why; rows: secret in why / in quote refused, value absent from problem text",
    "A1-2 first_look._holds_secret: casefold and urllib.parse.unquote compare; rows: upper-case secret in steps refused, %2D-encoded secret in url refused",
    "A1-3 first_look._sign_in_access_faults: refuse empty or absent kind and keys outside a data list sign_in_access_keys; rows: access {} / kind empty / extra key token refused",
    "A1-4 first_look._sign_in_access_faults: SIGN_IN_TEXT_MAX on every string leaf of access; rows access.url 500 written / 501 refused",
    "A1-5 first_look._sign_in_faults: no got-value or unknown key echoed unless it passes the literal check and scrub; row actor = secret refused, value absent",
    "A1-6 judgment-census.json: put_problems class xref -> safety per E-A2, ratchet safety 86 -> 87, commit line judgment: adds data check first_look.put_problems (sign_in_secret_faults); this conflicts with spec section 1b world B, Lead decides",
    "A1-7 first-look-statuses.json: move SIGN_IN_FIELDS_KEYS, SIGN_IN_LANDED_KEYS, surface-only keys and SIGN_IN_HTTP_REFUSED_KINDS to data; drop the SIGN_IN_ACCESS exemption in test_statuses_file_is_the_one_home_of_the_words",
    "A1-8 attach the verbatim re-run of test_first_look.py and test_first_look_step.py",
    "A2-1 walk_session.survey_opens_on docstring, changelog fragment and commit body: asks_person means no rung could read or tie the build, not that the stand answered (runtime_probe.py:48, 663, 1070, 1297-1299)",
    "A2-2 witness: run test_exploratory_findings.py, test_gate_role_accounts.py, test_manual_evidence.py, test_state_exits.py; paste the scenario_walk output verbatim; name the slow files as batch canon",
    "A2-3 walk_session.Walk._shutdown: 'ends =[' -> 'ends = ['"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-28-cards-redraft-spec.md",
      "docs/tasks/critic-diff-brief.md",
      ".claude/worktrees/fv1-28-a1/docs/tasks/specs/reports/20261114-fv1-28-a1-report.md",
      ".claude/worktrees/fv1-28-a2/docs/tasks/specs/reports/20261114-fv1-28-a2-report.md",
      "git show 302180ff (full diff)",
      "git show 01136cc2 (full diff)",
      "scripts/manual_capture.py 196-215, 1544-1615, 575-588",
      "scripts/walk_session.py 1240-1314, 569-614",
      "scripts/runtime_probe.py 20-59, 1220-1314",
      "scripts/profile_contract.py 730-755, 809-918, 1044-1060",
      "scripts/driver_stage_plan.py 61-75, 183-262",
      "scripts/driver_stage_build.py 94-140, 236-262",
      "scripts/driver_sources.py 722-745",
      "scripts/driver_dispatch.py 1549-1570",
      "scripts/app_card.py 55-85",
      "scripts/config_contract.py access_errors",
      "scripts/tests/test_judgment_census.py 35-36, 75-101",
      "references/role-load.json",
      "docs/SIBLING_MAP.md axis 5 row The first look"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_walk_survey_place.py (A2 tree)", "result": "=== test_walk_survey_place: 159/159 ok ==="},
      {"command": "python -B scripts/tests/test_first_look.py (A1 tree)", "result": "=== test_first_look: 381/381 ok ==="},
      {"command": "python -B scripts/tests/scenario_walk.py --witness-for scripts/walk_session.py scripts/manual_capture.py (A2 tree)", "result": "27 lines; 4 fast keep files for manual_capture.py not run by the builder"},
      {"command": "git merge-tree --write-tree 2cf488ad 302180ff ; 2cf488ad 01136cc2", "result": "both clean"},
      {"command": "adversarial sign_in probe through first_look.put in temp stories (stdin payload)", "result": "secret in why, case/URL-encoded secret, access_token/session/cookie, access {} and unbounded access.url all written"}
    ]
  }
}
```
