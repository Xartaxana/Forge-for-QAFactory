# t-811 — topic diff critic, FV1-17a / 17c / 17b / FV1-15 (stand sign-in)

Critic (opus), 14.11.2026. Tree: wave13 at main 0a18b0db (I only read it). Diffs: 3579b260 (17a+17c), a0aa1aec (17b), 0a18b0db (15),
0d149d12 (SKILL.md trim). Spec: `20261114-fv1-17-15-cards-redraft-spec.md` (cards, §2, edges, F-N1..F-N7).

## Verdict

**Topic: GO WITH FIXES.** That is my input to acceptance; the decision stays with the Lead.
- FV1-17a: GO WITH FIXES (B1 lands in `try_roads`; S3, S5).
- FV1-17c: GO WITH FIXES (S6).
- FV1-17b: GO.
- FV1-15: GO WITH FIXES (B1 write side; S1, S2, S4, M1).

There is one blocker, B1: a field's reader is starved, so it blocks per brief q.10. It is a fix-round item, not a reject. The other items are
should-fix (S) or minor (M), sized for ONE fix-round builder. Queue lines (Q) belong to other piles.

## Findings

**B1 (blocker; AR-21/AR-22; Lead decision (b) is WRONG for `unauth_status`).** `try_roads` builds the access of each b/c/d road with no
`unauth_status` (`stand_access.py:958-966`). `record_stand_login` then writes `{**found["access"], "login_probe": ...}`
(`project_decisions.py:709`). That object replaces the whole `environment.access`. But `access.unauth_status` has a live reader that has
nothing to do with signing in: `env_probe.py:1109` `liveness(health_url, ..., access.get("unauth_status"))`. It turns a code the project
recorded as its norm into `wants_login`. Without it, codes such as 404, 405, 4xx-service and 429 read as `dead` (stand-answers C6/C7*).
The breakage has two sides:
1. Inside the run. My probe gave try_roads a recorded `local_login` with `unauth_status:[404]`. The access handed to the probe for road (b)
   was `{"kind":"form_login","form":"csrf-credentials-form","user_key":"U1","secret_key":"S1"}`, with no `unauth_status`. On such a stand,
   road (b) probes liveness without the norm, reads `dead`, and the form is never tried.
2. After a successful search. The norm is dropped from config, so the next probe calls the stand "did not answer".

Fix: in `try_roads`, copy the recorded `unauth_status` (when it is a list) into every b/c/d road's access. The write then carries it. Do
NOT carry `user_field`/`secret_field`/`token_key`/`url`: they belong to the old road. Add one SIGN_IN row:
`roads-unauth-status-carried`.

**S1 (FV1-15; FR-41/FR-59; E-L6 weakened).** `stand_health.py:736-737`. Any `status` that `valid_status` rejects reads `code None`. With
`outcome ok`, that now gives "proved (the project's login command)" for EVERY kind. Probe output: `local_login status 0 -> proved | ...
(the project's login command)`, `local_login 999 -> proved`, while `local_login 405 -> unknown ... contradicts itself`. Before this
change, an int 0 or 999 on an HTTP road was a contradiction. Now it resolves toward success, and the sentence names a command the kind
does not have. The spec mandated status 0 → proved only for E5, a harness record. Fix: "the project's login command" only when
`access.kind == "harness_command"`. Otherwise a raw status that is present, not None and invalid keeps `outcome unknown` /
"contradicts itself". Add a row next to `stand-health-e5`.

**S2 (FV1-15; FR-10 text truth).** `driver_stage_build.py:190` sets `searched` from the PRESENCE of `login_search[env]`, whatever the exit.
The body at `:74` then says "I already tried every way in I know ... and none signed in". That is false in two cases: after exit 0
(a road was recorded, or `unchanged`) when the next probe still fails. Fix: read `exit`. When it is 0, word it as "the way the search
recorded did not sign in when I checked again". The option stays withheld either way (E-D3).

**S3 (17a/15; Lead decision (c): a defect of this topic, AR-13/P31).** Without key names on the access, `try_roads` takes them only from
`--user-key/--secret-key` (`stand_access.py:949-950`). The probe also takes `environment.user_key` and the first `secret_keys` entry when
the access has none (`env_probe.py:941`, `:1035-1037`). This is a second, narrower spelling of "which key names sign in". Concrete case: a
`bearer_env` stand whose token answers `unjudged` gets offered `find the way in`, and the search can never work. Probe:
`bearer + env keys: [('a','wrong_door',..), ('b:csrf-credentials-form','not_tried','no sign-in key names are recorded or given')]`.
Fix: fall back to `environment.user_key` / first `secret_keys`, exactly as the probe does, with one row. This is not a separate node: the
story-time door this topic adds is the one that fails.

**S4 (FV1-15; AR-13 residual).** `stand_health.py:704`/`:726` still reads `login_probe` raw, and puts the raw `status` into
`out["status"]` next to `recorded_login`. Fix: drop `receipt`; use `recorded["status"]`, or keep the raw value with a named reason.

**S5 (17a; spec §2.1 vs the table; direction I2).** LA8 maps any 400/422 service answer on local/oidc to `credentials_refused`. §2.1 says
"naming only sent fields", and the error direction forbids erring toward `credentials_refused`. Probe:
`answer_of(400,'{"message":"Bad Request"}',road="local_login") -> credentials_refused`, `complained: []`. In try_roads that stops EVERY
later road ("fix the account first"), which can hide a form road that would sign in. Lead fork, recommendation first:
- (A) In `_login_why`, a local_login 400/422 whose `complained` is empty is `unjudged`; oidc keeps LA8, because OAuth `invalid_grant` is the account.
- (B) Keep the table as is and amend §2.1.

**S6 (17c; Q2 / E5 of the card).** `p4-generate.md:311-312` triggers the roads on "a `skipped` or `not_recorded` one". That includes
`kind: none` and `ui_only`, whose skip IS the person's word. The text even says to add `--user-key/--secret-key` "when the block records
no key names", so the form roads would send the real account against the person's "UI only". Fix: one clause that excludes a skip by
`none` / `ui_only`.

**M1 (FV1-15, latent).** The write takes `found["access"]`, which is `_shown_access` (`stand_access.py:912-918`), a DISPLAY projection
(`url` through `_safe`). Harmless today, because only b-roads (no url) are ever written. Fix: keep the real access in the entry under a
private key, or rebuild it; do not write a display form.

**M2 (17a, duplication).** The block `missing = " and ".join(...)` now exists three times (`stand_access.py:471`, `:523`, `:644`). Extract
one helper in the same round.

**Q1 (sibling, axis 5 — not in the spec's sibling list).** First look's `references/first-look-statuses.json:26-27` validates a walker's
`sign_in.http` through `config_contract.ACCESS_KINDS`, which 17a widened. Two consequences: `ui_only` is now an acceptable http "way in"
(it should join `sign_in_http_refused_kinds`), and `form` is not in `sign_in_access_keys` (a found form way cannot name its row;
`test_first_look.py:583` pins the key set). Line for the Lead: `first-look http way: ui_only refused, form key allowed | узел: <new node in
live-run-fvf next to FV2-57 (FV1-28 C1)>`.

**Q2 (17a item 9, dropped edit).** `templates/config.json:47` `environment.note` still lists five kinds. No queue line exists (Grep
`environment\.note|five kinds|seven kinds` over `plans/piles` found one unrelated hit). Line: `template environment.note names the seven
kinds (+ note_history) | узел: <onboarding-forge untaken batch>`.

**Q3 (duplication; AR-16 convergence).** One answer word has four plain-word spellings: `stand_access.WRONG_DOOR_WHY`/`UNJUDGED_WHY`,
`env_probe.LAYER1["login"]` prefixes, `stand_health.ANSWER_WORDS`, and the `driver_stage_build` `login_says` sentences (+ L0). The spec
prescribed each one in place, so this is not a fix of this round. Line: `answer plain words one data table read by stand_health and
stand_question_text | узел: <live-run-fvf next>`.

**Q4 (code quality, queue).** New functions over 60 lines: `_form_run` `stand_access.py:613-741` (~129 lines; nested helpers) and
`try_roads` `:932-1016` (~85 lines, nesting 4 at `:991-997`). Split them (roads list / run loop) when next touched.

**Q5 (minor).** `manual_capture.py:5449` / `investigation_probe.py:425` guard only on `authorization`. On a form stand, a role-supplied
`Cookie` header is silently replaced. Queue next to FV1-28e.

**Pending Lead decision.** FV2-38 (`batch-2-live-run-fvf.md`) asks within FV1-15 whether to keep "or name the way the project signs in"
in `retry`. The diff kept it in both classes (`driver_stage_build.py:91-95`). In the `way` class it now sits next to `find the way in`.
My recommendation: drop it in `way`.

## Judgments on the Lead's decisions (a)-(f)

- (a) RIGHT. One `_http_auth` picks the header. `_http_login` stays token-only for the walker (FV1-28e, a named node). The cookie is
  redacted by name (`manual-capture-steps.json:105`, `redact_headers` has `cookie`), so E1 holds. The capture's own recipe wins over
  access (`_is_form_stand` needs `source == "access"`).
- (b) WRONG for `unauth_status` (B1). Right for every kind-specific key.
- (c) A defect of this topic (S3).
- (d) Deviations 1-6 are acceptable. `ANSWER_WORDS` uses plain words and maps our own closed words, so FR-12 does not apply; with S1 the
  "login command" wording is kept honest. Module constants instead of Driver members are fine. Deviation 7 (a python payload rewrote a
  test file) breaks command hygiene pt.4 and is a calibration line for the Lead, not a code defect.
- (e) RIGHT. No `description` field exists; Q2 queues the note. "No road and no person = a named open gap" matches P22 and the owner-away rule.
- (f) It survives. p4 owns the rule in full (four role-rules anchors in p4), p2 topic 2 keeps its sentence, and the SKILL row points at
  p4, which is read in order. Card item 6 is now unmet as text: record it on the card. Axis 31 (one owner) is better for it.

## Standing questions

1. Fit: met apart from S5 and S6. P1-P5 and D1-D6 are as carded, including E-D1 (`driver_machine.py:3976-3979`), E-D2 and E-P1.
2. Builder choices: all in the safe direction except Q3/Q4 (above).
3. Seams: additive. The census raises are named (q.9): conductor 760→761 (`manual_capture._http_auth`), 761→762
   (`project_decisions.record_stand_login`). The 15 report says "no ceiling raised", which does not match the diff's 761→762; the Lead
   named it at merge.
4. Class: env_probe, try_roads, manual_capture and investigation_probe use the one road; stand_health uses `recorded_login` (S4
   residual); the walker is FV1-28e; onboarding p4 `:269` is F-N4; first look is Q1, NEW.
5. Tests: the SIGN_IN and STAND_LOGIN rows kill the node defects. Missing: a row for the unauth carry (B1) and one for a non-harness
   invalid status (S1).
6. DUPLICATION AND CONSISTENCY: M2 and Q3. I grepped `missing = " and "`, the wrong_door / "look like a sign-in" phrases and
   `login_probe` reads over `scripts/*.py` (case-insensitive).
7. CODE QUALITY: Q4 (two functions over 60 lines), M1 (a name that lies: a display form written as data). No dead branches found.
8. Hygiene: `selftest --lang` 4/4, per the attached layer.
10. ARCHITECTURE: AR-1 holds. Grep `-i "next-?auth|callback/credentials|csrfToken|api/auth"` over the package finds only
    `login-roads.json` (4), tests and one fixture. AR-3: Q2. AR-6 holds: HTTP and subprocess only. AR-9 holds. AR-13: S3 and S4. AR-14
    holds: `upsert`+`resolve`. AR-16 holds: priced variant key. AR-17/AR-25 hold: the `ui_only` state-exits row and `login_search` per
    story. AR-21/22: B1. AR-29 holds.
11. JUDGMENT: none moved. At story time "first road in" can only pick among form rows in data order, all proven by code (road (a) =
    unchanged, no c/d). That is data under the person's token (F-N1 A). At onboarding the role chooses (p4). The census row
    `record_stand_login` (shape/data) holds.
12. ONE ROAD: S3 (key names) and S6 (none/ui_only). Other exclusions are named nodes: walker FV1-28e, p4 `:269` F-N4.

## Secrets

I read every new output line. Form whys go through `_scrub(held)` (user, secret, csrf token, cookies); urls go through `_safe`; the junk
secret is never printed; refusals carry names only; the cookie is redacted by header name. I found no leak.

## Trail

Read: the critic-diff-brief; the cards spec (whole); `stand_access.py` (whole, merge tree); diffs of 3579b260/a0aa1aec/0a18b0db
(product + census + layers + changelog); `git show 0d149d12` (SKILL.md); `env_probe.py:625-700, 856-955, 1025-1054`;
`config_contract.py:100-144, 350-425`; `driver_stage_build.py:136-175`; `first_look.py:574-600`; `stand-answers.json:1-40`; the FV1-15
and 17a builder reports; `batch-2-live-run-fvf.md:60-130`.
Greps: `unauth_status` (-i, package); `"cookie"|redact_headers`; `_http_login\(|_http_auth\(|form_session\(|recorded_login\(|login_probe`;
`stand_access\.` count; the framework names (-i, positive control `login-roads.json`); `sign_in_http_refused_kinds|sign_in_access_keys`;
`environment\.note|five kinds|seven kinds` in `plans/piles`.

Reruns:
- `python -B scripts/tests/test_http_client.py` (package dir, subshell) → `=== http_client: 255/255 ok ===`.
- Probe A (heredoc; try_roads with `env_probe.probe` stubbed): road (b) access has no `unauth_status`; with bearer + env keys, b is `not_tried`.
- Probe B (`_login_receipt`): `local_login 0/999 -> proved (the project's login command)`; `405 -> contradicts itself`.
- Probe C: `answer_of(400, no named field, local_login) -> credentials_refused`.

```json
{"verdict": "fit_with_fixes", "blockers": ["B1: try_roads builds b/c/d road access without the recorded unauth_status (stand_access.py:958-966) and record_stand_login writes it as the whole environment.access (project_decisions.py:709); env_probe.py:1109 liveness reads access.unauth_status, so the road is probed with no norm and the norm is dropped from config after a search"], "fixes": ["B1: carry the recorded unauth_status into every b/c/d road access in try_roads (only that key), plus row roads-unauth-status-carried", "S1: stand_health.py:736 says 'the project's login command' only for kind harness_command; an invalid raw status on another kind stays 'contradicts itself', plus a row", "S2: driver_stage_build.py:190/74 words the searched body by login_search exit (exit 0 = the recorded way did not sign in when checked again)", "S3: try_roads key names fall back to environment.user_key and the first secret_keys as env_probe does, plus a row", "S4: stand_health.py:704/726 drops the raw login_probe read; status from recorded_login", "S5: Lead fork, recommended (A): in _login_why a local_login 400/422 with no complained field is unjudged; oidc keeps LA8", "S6: p4-generate.md:311 excludes a skip by kind none or ui_only from the roads trigger", "M1: record_stand_login writes the real road access, not the _shown_access display form", "M2: one helper for the missing-keys sentence (stand_access.py:471, 523, 644)"], "class_completeness": "Sign-in sites: env_probe, try_roads, manual_capture, investigation_probe on the one road; stand_health via recorded_login (S4 residual); walker = FV1-28e; onboarding p4 :269 = F-N4; NEW sibling not in the spec: first look first-look-statuses.json sign_in_http_refused_kinds lacks ui_only and sign_in_access_keys lacks form (Q1, node line given). Template environment.note five kinds unqueued (Q2). Answer plain words spelled in four modules (Q3, queue).", "trail": {"read": [".claude/worktrees/wave13/docs/tasks/critic-diff-brief.md", ".claude/worktrees/wave13/docs/tasks/specs/20261114-fv1-17-15-cards-redraft-spec.md", ".claude/worktrees/wave13/ai-packages/qa-factory/scripts/stand_access.py", "diffs 3579b260, a0aa1aec, 0a18b0db, 0d149d12 (ai-packages)", ".claude/worktrees/wave13/ai-packages/qa-factory/scripts/env_probe.py:625-700,856-955,1025-1054", ".claude/worktrees/wave13/ai-packages/qa-factory/scripts/config_contract.py:100-144,350-425", ".claude/worktrees/wave13/ai-packages/qa-factory/scripts/driver_stage_build.py:136-175", ".claude/worktrees/wave13/ai-packages/qa-factory/scripts/first_look.py:574-600", ".claude/worktrees/wave13/ai-packages/qa-factory/references/stand-answers.json:1-40", ".claude/worktrees/wave13/docs/tasks/specs/reports/20261114-fv1-15-report.md", ".claude/worktrees/wave13/docs/tasks/specs/reports/20261114-fv1-17a-report.md", ".claude/worktrees/wave13/plans/piles/live-run-fvf/batch-2-live-run-fvf.md:60-130"], "reruns": [{"command": "python -B scripts/tests/test_http_client.py (package dir, subshell)", "result": "=== http_client: 255/255 ok ==="}, {"command": "heredoc probe: try_roads with env_probe.probe stubbed, recorded local_login unauth_status [404]", "result": "road b access = {kind form_login, form, user_key, secret_key} - no unauth_status; bearer_env + environment.user_key: b not_tried 'no sign-in key names are recorded or given'"}, {"command": "heredoc probe: stand_health._login_receipt outcome ok with status 0/999/405", "result": "local_login 0 -> proved (the project's login command); local_login 999 -> proved; local_login 405 -> unknown contradicts itself"}, {"command": "heredoc probe: stand_access.answer_of(400, '{\"message\":\"Bad Request\"}', road=local_login)", "result": "credentials_refused, complained []"}]}}
```
