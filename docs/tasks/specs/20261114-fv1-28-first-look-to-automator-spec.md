# Spec draft — FV1-28: the first look reaches the automator in substance; a skipped look is a gap; the role's way in is recorded

Pile `live-run-fvf`, batch 1, node FV1-28 (P1). Designer draft t-749, 14.11.2026, for Lead acceptance. Forks are in §6 and are NOT
decided here; every card is executable on the recommended option until the Lead (or the owner) says otherwise. All facts below were
read on origin/main under `C:\QAFactory\forge-repo\.claude\worktrees\read-main` (called `M\` below; package paths are relative to
`M\ai-packages\qa-factory\`).

## Owner's words (quoted from the carriers, not from the brief)

- «у нас есть "первый взгляд" это как раз то же что делал агент должно быть»; «он должен брать то что уже знает фабрика, но если этого
  не хватает, то идти и смотреть сам» (finding `M\plans\piles\live-run-fvf\findings\20261113-pervyj-vzglyad-ne-dohodit-do-avtomatora.md:22-23`).
- «агент же как-то сам определяет как войти на стенд. Мы не должны ему прописывать действия, просто не мешать» (finding `:34-35`;
  plan `M\docs\tasks\specs\20261113-plan-fabrika-ne-huzhe-agenta.md:346-347`).
- «и её результат должен записываться, что бы проба кода не осталась общим фактом. Роль находит как входить, код записывает для всех
  остальных» (finding `:39-40`; plan `:374-375`: «Способ входа, найденный ролью первого взгляда, становится записью, которую читают проба
  и все следующие роли (P27 …; AR-14 — один писатель); догадка пробы эту запись не перекрывает»).

## §0 Facts read on the carrier

| # | Fact | Carrier |
|---|---|---|
| F1 | The S5 automator brief ALREADY gets first-look lines of kind `s5` on main: `build` calls `first_look_lines(task_root, stage, role)` in the head; `FIRST_LOOK_KIND[("S5","qa-automator")] = "s5"`; kind `s5` carries only the path items `locator`, `api`, `sample`, `data` — NOT `screen` (the url) and NOT `step` | `scripts/brief_pack.py:4403-4408` (`build`), `:4127-4130` (`FIRST_LOOK_KIND`, `FIRST_LOOK_AUTHOR_KINDS`), `:4216-4222` (`_fl_body`) |
| F2 | The block is capped at `FIRST_LOOK_LINES_MAX = 12` lines, each `FIRST_LOOK_LINE_CHARS = 180` (one line per ROW, items joined by `; `), then `+N more: work/first-look.yaml` / `whole: work/first-look.yaml`; rows are NOT filtered by the window (every row of the record) | `brief_pack.py:4121-4122`, `:4154-4163` (`_fl_line`), `:4241-4265` (`first_look_lines`) |
| F3 | No record, a `null` record, an unreadable or a stale one is ONE line: for null "First look: there was no first look - the stand was not walked (no stand)."; the input-file line says "no first look - the stand was not walked (no stand)". Neither names a move nor says it is unknown | `brief_pack.py:4166-4186` (`_fl_state`), `:4016-4034` (`first_look_input_line`) |
| F4 | The finding's line numbers (`brief_pack.py:1195-1197, 3822-3840`) do not match main (`:1247-1249`, `:4241`): main moved since the run. Whether the run's package carried FL-4 is NOT established (no run log read); it does not matter for the run: the record was null, so FL-4 prints exactly one line (F3) — the "one pointer line" of the finding | finding `:12`; `brief_pack.py:1247-1249` |
| F5 | The real run's record: `null: "no_stand"`, `rows: []`, `gaps: ["no first look: no stand"]`, `walk: ""`, `stand: ""`, `walked_at 2026-11-12T17:23:55` — 11 lines | `M\experiments\mybooks\factory-vs-free-agent\runs\factory-out\work\first-look.yaml:1-11` |
| F6 | No non-empty first-look record and no S5 brief of a real run is in the repo: `runs/factory-out/work/` holds no `briefs/` folder (Glob `runs/factory-out/*/*`: 12 files, none a brief; positive control: the same Glob listed `first-look.yaml`). So "what reaches the brief today" is measured on code only, not on a real run | Glob over `experiments/mybooks/factory-vs-free-agent/runs/factory-out` |
| F7 | WHO DECIDES "no stand": code. `first_look.due` returns `(False, "no_stand", ...)` when `pipeline.environment` is empty OR `pipeline.environment_pending` is true; the driver then writes `put --null no_stand` and makes the plan without dispatching the walker | `scripts/first_look.py:661-663` (`due`); `scripts/driver_stage_plan.py:153-159` (`first_look_step`), `:166-179` (`_first_look_null`) |
| F8 | ON WHAT EVIDENCE: `environment_pending` is set true by S0 on ANY non-zero exit of `env_probe.py` (a refused login included: E3/E4 of the stand-login spec — `/api/health` 200, `login: failed HTTP 405`) | `scripts/driver_s0.py:2424-2428` (`if code == 0: pending = False`); stand-login spec `M\docs\tasks\specs\20261113-fv1-17-5-15-stand-login-spec.md:39`, `:58-59` |
| F9 | A dead stand is also measured at walk open: `walk_session.py open` runs a stand probe ("Lease, stand probe, ... A `ServerDead` leaves nothing open"); a failed open writes a null reason through `_first_look_give_up` | `scripts/walk_session.py:1173`; `driver_stage_plan.py:194-207`, `:238-244` |
| F10 | The first-look role can already sign in by itself: a session's actor signs in by code only where gate A proved the recipe; otherwise the refusal tells the role "or sign in yourself with `fill-account <selector> <actor> user|secret` steps in this session" | `scripts/manual_capture.py:2940-2954` (`sign_in_refusal`); `walk_session.py:1296-1322` |
| F11 | TODAY'S STORES OF "HOW TO SIGN IN" (four, none written from a story): (a) `config.json environment.access` + `login_probe` — the onboarding role writes it (`p4-generate.md`), readers `env_probe`, `stand_health`, `config_contract`; (b) `config.json manual_capture.login.ui/http` — the walker's recipe, reader `manual_capture.login_recipe` (default `references/manual-capture-steps.json`); (c) the gate-A sign-in probe rows, reader `manual_capture.sign_in_row` / `sign_in_refusal`; (d) the answer registry `records/project-knowledge.json`, one writer `project_knowledge.record`, readers `state`/`value`/`roster`/`lessons` (a role's `sign_in: account|none` per product role; stand lessons) | stand-login spec C16 (`:44`); `manual_capture.py:4870-4883`, `:2940-2945`; `scripts/project_knowledge.py:45-62`, `:121`, `:449-479`, `:671-701`; `design/architecture.md:63`, `:170` |
| F12 | FV1-17 is NOT built: no `recorded_login`, `try_roads`, `form_login` in `stand_access.py` of main or of any worktree (Grep `def recorded_login|def try_roads|def recorded_seconds` with glob `stand_access.py` over `.claude/worktrees`: only `recorded_seconds` hits, in every worktree — the positive control of the same call). Status report: "FV1-17 ожидает — not merged: spec only" | `M\docs\tasks\specs\reports\20261114-statuses-fv1-report.md:36`; `stand_access.py:55-509` def list |
| F13 | FV1-17's design writes the found login into `config.json environment.access` AT ONBOARDING (the role writes the first road whose answer is `in`); FV1-15's non-goal and fork F7 (A, recommended) exclude "writing `environment.access` from a story" | stand-login spec `:237-240` (item 7), `:391`, `:492-495` |
| F14 | The registry takes a ROLE as a source (`SOURCES = ("person", "role", "legacy_config")`, `BY = ("conductor", "driver")`); a stand-scope fact is recorded `known` only; a new kind of fact is a catalogue row in `references/config-keys.json` section `knowledge` (`store`, `scope`, `compare`) — the road SS1-11 used for `environments.stand_lessons` | `project_knowledge.py:64-121`, `:611-668` (`record_problems`), `:626-627` |
| F15 | The brief is NOT in a role's first-request load: "What the FIRST request of a role holds: the brief, its side files and the form are read later, by tool calls"; the static load counts the brief at an allowance (`allowances.brief` 6144 tokens, an estimate; the brief has no size bound, FV1-4). The ceiling H of the told-before-work spec is `U` = charter + injection layers only | `scripts/role_load.py:57-58`, `:460-470`, `:511-532`; `references/role-load.json:7`; `M\docs\tasks\specs\20261114-told-before-work-t1r-pages-spec.md:30` (F4) |
| F16 | The automator charter already orders "what the first look saw (locator, route, data), the carried-over sample, your live check ... look live only where it is silent or stale" | `agents/qa-automator.md:55` |
| F17 | A case names its requirements; the one reader is `contract.case_requirements(path)`; the window's case files are `brief_pack.case_paths(task_root, scope)` | `scripts/contract.py:3622-3624`; `brief_pack.py:4420` |
| F18 | `first_look.put_problems` REFUSES `rows: []` ("`rows` is one mapping per requirement of the register"): a walked record with no row cannot exist; the declared empty outcome is `put --null <reason>` only | `first_look.py:410-414`, `:504-528` |
| F19 | The three acceptance rows exist only in the amendment spec (Grep `probe_405|entry_recorded|first_look/empty` over `M\`: one file); the dry harness that runs them (P1-b) is not on main | `M\docs\tasks\specs\20261113-p1-specs-amendment-owner-words.md:442-447` |
| F20 | `brief_pack.py` `FIRST_LOOK_*` constants are owned by told-before-work T3b for `FIRST_LOOK_AHEAD`/`FIRST_LOOK_DOD`; A1a (stage critics removed) names `FIRST_LOOK_KIND`; FV1-4 did not edit any `FIRST_LOOK_*` | told-before-work mechanism spec `:741`; stage-critics spec `:943-945`; FV1-4 spec `:363-366`, `:705` |
| F21 | Keep rows (all before `"quarantine"` at `test-layers.json:7168`): `test_brief_pack.py` `:288`, `test_project_knowledge.py` `:4093`, `test_first_look.py` `:6737`, `test_first_look_wiring.py` `:6833`, `test_first_look_briefs.py` `:6847` | `scripts/tests/test-layers.json` |

### The re-read of FV1-5 against the owner's words (finding item 2, last paragraph)

FV1-5's card (`stand-login spec :300-376`) changes the probe's output (`blocked_by` words, `blocked_by_of`) and the driver's SENTENCES
(S0 warning, S1 review, S5/S6 stand question, refusal seam). Nothing in its card contradicts «Мы не должны ему прописывать действия, просто
не мешать» or «проба кода не осталась общим фактом» in what it WRITES. But it leaves the chain untouched: item 4 (`:336-337`) keeps S0
setting `environment_pending` on the failed probe ("it did not pass the check"), its non-goals forbid "a new `pipeline.json` field"
(`:315`), and nothing reads `blocked_by` in `first_look.due`. So after FV1-5 a refused login STILL skips the first look with `no_stand`
(F7, F8). That is not FV1-5's defect (its finding is the false sentence); it is this node's card A1. One line of the TOPIC does contradict
the owner's third word: FV1-15 non-goal "writing `environment.access` from a story (F7)" + F7(A) (`:391`, `:492-495`) — if the role's way in
had to live in `environment.access`, the owner's "код записывает для всех остальных" could not happen from a story. This draft therefore
does NOT write the role's way into `config.json` (fork F-1). The finding's phrase «проба входит так, как входит тест» describes FV1-17's
`harness_command` road (`:224-236`), not FV1-5's card: FV1-17's roads are a tool the ONBOARDING role calls (AR-7), consistent with the
owner's words; it is onboarding-time, not story-time.

## §1 Architecture invariants touched, checks, owners, census class

| AR | How it is touched | Change check written into the DoD |
|---|---|---|
| AR-21 / FR-49 | the first look's substance (url, steps, locators, api, samples, data) reaches S5 for the window, whole, with the cut said | card B1 rows: a window row's every path item is a line; a cut names the record |
| AR-28 / FR-41 / FR-59 | a probe's failure is not "no stand"; a missing look is a GAP worded as unknown | card A1 `due` rows; card B1 gap rows (null/absent/unreadable/stale) |
| AR-23 | empty outcomes: `null` keeps its home; "role could not reach" = rows `unreachable`/`access` (existing words, F18) | card A1/B1 rows for each empty kind |
| AR-14 | one writer per artifact: `first_look.put` writes `work/first-look.yaml` (with the role's `sign_in`); `project_knowledge.record` writes the registry row | card C1: `artifact-writers.json` unchanged (no new artifact); Grep for a second writer of the registry: none |
| AR-13 | the recorded way in has ONE reader for consumers: `project_knowledge.sign_in(root, stand)` | card C1 reader; card B2/D1 call only it (Grep `environments.sign_in` outside `project_knowledge.py` = catalogue row only) |
| AR-3 | a new fact = catalogue row with `absent_means` (absent = "no recorded way: the role finds it") | card C1 `config-keys.json` row; `test_config_migration.py` if `--witness-for` prints it |
| AR-22 | producer `first_look.put` (`sign_in`) -> reader driver acceptance -> producer `record` -> readers `sign_in()` (briefs, probe) | each producer and reader land with a test row naming the other side |
| AR-25 | a registry row has a way out: `project_knowledge.py revoke` (exists) | card C1: `design/state-exits.md` row for `environments.sign_in` |
| AR-29 | every new check is shape/presence | table below |
| AR-12 / AR-11 / AR-20 | brief bytes grow; the brief is not in U/H (F15); no ratchet row moves | card B1 measures the added bytes on its fixture (`role_load.py --role qa-automator --task <fixture>`) before/after; `role-load.json` untouched |
| AR-2 / AR-7 | which way in, which locator to trust: the role's judgment; code carries | named per card |
| AR-15 / AR-19 | `_fl_state` is the one wording of the record's state for S3-S7 — the gap text changes there once, all readers alike | card B1 |
| AR-26 | window = requirements of the window's cases | card B1 (via `contract.case_requirements`) |

Checks the node adds or alters (AR-29; P27):

| Check | Owner it serves | Census class |
|---|---|---|
| `first_look.due` — no `no_stand` on `environment_pending` with a named stand | data (presence of a stand name) | shape |
| `first_look.put_problems` + new `_sign_in_faults` — `sign_in` keys, closed `surface` word | data | shape |
| `project_knowledge.record_problems` + `_sign_in_value_faults` — value shape | data | shape |
| driver `_first_look_accepted` gating of the registry write | judgment (the first look's acceptance = the tier above the role, the driver's acceptance) | shape (it reads the acceptance, never judges the way) |
| `env_probe` precedence (card D1) — recorded way before the guess | data | shape |
| WHETHER the recorded way is right, which locator to use | judgment (role; accepted by the code critic S5 / the driver) | — (no code check) |
| revoke a wrong recorded way | intent (the person, `revoke` with words) | — |

## §2 Cards

Order: A1 ∥ B1 (disjoint files); C1 after A1 (reads A1's `sign_in` from `first_look.read`); B2 after C1; D1 after FV1-5 AND FV1-15
are merged (they own `env_probe.probe`). FV1-29 follows B1 (it writes `brief_pack.py` and `agents/qa-automator.md`). A1a (stage
critics) and T3b touch other `FIRST_LOOK_*` names: B1/B2 do not edit `FIRST_LOOK_KIND`, `FIRST_LOOK_AHEAD`, `FIRST_LOOK_DOD`; if the
Lead's dispatch finds them unmerged, `очередь: A1a -> FV1-28 B1`, T3b by function (PROJECT.md «Командная работа» 3).

### Card A1 — the skipped first look is decided by the role, not by the probe (first_look.py; owner items 2)

given: this spec; `design/factory-rules.md` whole; `plans/builder-rules.md`; the finding; facts F5, F7-F10, F18.
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\first_look.py (`due`, `put_problems`, `put`, `read`, new `_sign_in_faults`, new constant `SIGN_IN_KEYS`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\first-look-statuses.json (new key `sign_in_surfaces`, note sentence)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\artifact-contract-first-look.md (new section "The way in you found")
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_first_look.py (new table rows only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows of the changed/new units only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-28-a1-first-look-not-skipped-by-probe.md (new fragment)
non-goals: `env_probe.py` (FV1-5/FV1-15/D1); the driver's S0 `environment_pending` write; `brief_pack.py` (B1); the registry (C1); new
`null_reasons` words; `walk_session.py`.
handoff: builder report per `.claude/agents/builder.md` rule 7 with the witness, the FR pass (A, C, D, E), the AR line, census rows.

What to build:
1. `first_look.due`: `no_stand` ONLY when `pipeline.environment` is empty (no stand named — a fact of the story, not a probe guess).
   `environment_pending: true` with a named stand no longer returns `no_stand`: the checks go on (attempt on these heads, retries) and
   `due` returns True when nothing else says no. The docstring says why (the owner's word, FR-41).
2. `put_problems` / `put` / `read`: the role's file may carry ONE optional top-level `sign_in:` mapping (TOP_KEYS gains `sign_in`):
   `surface` (a word of `sign_in_surfaces`: `["ui", "http"]`), `url` (text), `steps` (list of lines), `fields` (mapping
   `user`/`secret`/`submit` -> selector text; ui), `request` (mapping `method`, `path`, `body_fields` list of NAMES; http), `landed`
   (mapping `url_not` list of address fragments; ui), `evidence` (capture paths of THIS walk, as rows cite them), `why` (one sentence:
   what the role did). Shape only (`_sign_in_faults`): unknown keys refused with the allowed list; `surface` required; evidence checked
   with `WS.capture_cited(task_root, walk, <any R-n of the walk the capture belongs to>, path, "", stand)` — if `capture_cited` needs a
   quote, `quote` becomes a required key (builder reads `walk_session.capture_cited` and names which in the report). `put` writes the
   mapping into the record unchanged; `read` returns `sign_in` (`{}` when absent). SECRETS: a key whose value looks like a secret is
   refused through `app_card.scrub(..., tokens=True)` != value (no password, token or cookie value is ever stored: names and selectors only).
3. `artifact-contract-first-look.md`: a section "The way in you found" with the YAML example and: "find the way in yourself, as any
   tester would; the factory's own probe is not a fact for you; record the way that worked; if nothing worked, every row is
   `unreachable` with `blocked_by: access` and `why` naming what you tried".

edges:
- INVARIANT (positional, `due`): the order stays `parks_after_s5` -> register unreadable -> empty register -> no stand NAMED -> attempt
  on these heads. What must stay unreachable: a paid walk when no stand is named; a second walk on the same heads and register; a walk
  for a story whose deliverable side does not exist.
- A really dead stand (liveness): `walk_session.py open` fails (F9) -> `_first_look_give_up` writes its cause / `walk_not_opened`; never
  `no_stand` (the null word says the walk could not open). Invariant: "no stand" is never written from a probe result.
- The role cannot reach the stand: it sends rows `unreachable`/`access` with `why` (existing words, F18); no `sign_in`. Invariant: a
  failed login is recorded by the ROLE with what it tried, never by code.
- EMPTY: `sign_in` absent / null / `{}` -> nothing stored, `read` gives `{}`. Two `sign_in` mappings cannot occur (YAML mapping).
- LIMITS (outside input: the role's file): `steps` at most 20 lines, each at most 300 characters; `url`, selectors at most 500
  characters; beyond -> refused with the limit named (rows AT and BEYOND each limit; empty string; a nested mapping where a line is
  expected; a non-UTF-8 file — the existing `_load_input` row).
- TEMPORAL: records written before the change have no `sign_in` -> `read` `{}`; stories with `null: no_stand` already written keep it
  (`put --null` does not replace a current walked record, `:519-523`); on the next S3 entry with new heads `due` is asked again and walks.
  A story already past S3 is not walked again by this change.
- CONFLICT: `sign_in` present but every row `unreachable/access` -> stored as sent (the role's own record; C1's registry write still
  requires an accepted record, see C1).

DoD:
- rows in `test_first_look.py`: `due` with `environment: "local", environment_pending: true` -> True (was `no_stand`); `environment: ""`
  -> `(False, "no_stand", ...)`; the `parks_after_s5`, register and attempt rows unchanged (existing rows stay green);
- `sign_in` battery: whole ui form accepted and read back; http form accepted; unknown key, missing `surface`, unknown surface, a secret
  value, steps at 20/21, line at 300/301, nested mapping in `steps` -> refused with the field named; absent -> `{}`;
- `selftest.py --lang` green on the touched files;
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/first_look.py references/first-look-statuses.json references/artifact-contract-first-look.md`
  and every file it prints (no slow file locally, no CI, no mutations: they are the batch canon), plus `test_judgment_census.py`.
siblings: `driver_stage_plan.first_look_step` reads `due` unchanged (one reader); S6 `s6_no_stand` (`driver_stage_s6.py:599-605`) reads
`environment_pending` for TEST runs — a different decision (no test runs on an unconfirmed stand), not changed, named here.

### Card B1 — the automator's brief carries the window's first look whole; a missing look is a gap (brief_pack.py; owner item 1, 2)

given: this spec; `design/factory-rules.md` whole; `plans/builder-rules.md`; F1-F4, F16, F17, F20.
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py (`first_look_lines`, `_fl_body`, `_fl_state`, `_fl_line`, `first_look_input_line`, `first_look_runner_lines`, constants `FIRST_LOOK_AUTHOR_KINDS`, `FIRST_LOOK_HEADS`, new `FIRST_LOOK_GAP`, new `FIRST_LOOK_ITEM_CHARS`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_first_look_briefs.py (new table rows only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows of the changed units only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-28-b1-first-look-substance.md (new fragment)
non-goals: `FIRST_LOOK_KIND`, `FIRST_LOOK_AHEAD`, `FIRST_LOOK_DOD` (A1a / T3b); the walker card for the automator (FV1-29);
`agents/qa-automator.md` (FV1-29 owns it; line 55 already orders "first look before your own discovery"); `app_card.py`; the
registry line (B2).
handoff: builder report with witness, FR pass (B, C, E), AR line, the byte measure below.

What to build:
1. `FIRST_LOOK_AUTHOR_KINDS["s5"]` = `("screen", "step", "locator", "api", "sample", "data")` (addresses and steps join; the reading stays
   `app_card.first_look_path_items`, the one reader).
2. Kind `s5` only: ONE LINE PER ITEM (not per row): `- R-n <status>: <item text> [first-look:R-n]`; the per-line clip is
   `FIRST_LOOK_ITEM_CHARS = 400` (an item longer is clipped with `...` and the block ends `whole: work/first-look.yaml`, as today's
   `_Clipped` road). The 12-line count cap does NOT apply to kind `s5` window rows (fork F-3); it stays for the other kinds.
3. Window: for an S5 `window` dispatch (`s5_kind == "window"`; `first_look_lines` gets the dispatch `scope` as a new keyword argument
   from `build`, default None = today), rows are those whose `req` is in the union of `contract.case_requirements(p)` over
   `case_paths(task_root, scope)`; one line `- +N requirement(s) of the record outside this window: work/first-look.yaml` when N > 0.
4. The gap (all readers S3-S7, one text, `_fl_state` and `first_look_input_line`): null / absent / unreadable / error ->
   `FIRST_LOOK_GAP` = "First look: a GAP - what the stand shows is not known for this story (<reason words>); it is not a fact that there
   is no stand. Where your work needs the stand, look yourself with the tools your brief names." The stale line keeps its meaning and
   gains the same last sentence. A record whose window rows are ALL `unreachable` with `blocked_by: access` -> one line "First look: the
   walker could not reach these requirements (<the rows' why, whole>): a gap you close with your own look."
5. `first_look_runner_lines` (the walker's own brief): when `pipeline.environment_pending` is true, one line: "The factory's own check of
   the stand did not pass at the start: that is a guess of code, not a fact. Find the way in yourself; if you get in, record it under
   `sign_in` (the form names it); if you cannot, every requirement is `unreachable` with `blocked_by: access` and `why` says what you tried."

edges:
- LIMITS: item text cut at 400 characters, SAID by the closing `whole:` line; rows outside the window counted and the record named;
  no other cut (FV1-4: a cut always names its carrier).
- EMPTY: scope None / plan dispatch / legacy -> all rows (today's behaviour plus items); no case of the window names a requirement ->
  all rows and one line "no case of this window names a requirement: every row is shown" (safe direction: more, never fewer);
  a row with no path items -> no line for it (today) — but the "no row names such a path" line becomes, for `s5`, "no row of this
  window names where it lives on the stand: a gap you close with your own look".
- INVARIANT (positional): the first-look block stays AFTER `provisional_lines` and BEFORE `prior_retro_lines` (`build` :4397-4411, the
  order of §4.4 row h); what must stay unreachable: a first-look value printed as an expected value (every sample and data item keeps its
  `seen:` prefix, FR-58), and a first-look line in the walker's own brief (`if not first_look`).
- CONFLICT: a stale record + window -> the stale single line wins (it confirms nothing), no item lines.
- TEMPORAL: a record written before A1 (no `sign_in`) reads the same; a story whose record is `null: no_stand` gets the GAP text.
- Error direction of the reused `contract.case_requirements` (advice -> filter): it may err only toward MORE rows; adversarial inputs:
  a case file that cannot be read, a case with no requirement line, an R-n not in the record — none removes a row that a window case
  names, and an unreadable case widens to all rows.

DoD:
- rows in `test_first_look_briefs.py` (a keep table, F21): a non-empty record -> the S5 window brief holds the url, a step and the
  locator of a window requirement (the finding's "Тест: непустой first-look.yaml → в брифе S5 есть адрес и локатор окна"), and not those
  of an out-of-window requirement plus the `+N ... outside` line; null `no_stand`, absent, unreadable -> the GAP sentence for S3, S4, S5,
  S6, S7 readers (one parameterised row per reader); all-unreachable/access -> the "could not reach" line; a 401-character item -> clip +
  `whole:`; the runner brief with `environment_pending: true` holds the "guess of code, not a fact" line;
- byte measure: the S5 brief of the table's fixture before/after (`len(bytes)`), reported with the command; `role_load.py --role
  qa-automator` static total unchanged (F15);
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/brief_pack.py`
  and every file it prints (`test_brief_pack.py` included; slow files are judged by the batch canon, named in the report), plus
  `test_judgment_census.py` and `selftest.py --lang`.
siblings: `app_card._first_look` (the card's First look section: the same reading, different reader — unchanged, named); S4 designer
kind `s4` keeps its 12-line cap (fork F-3 option for S4 named there).

### Card C1 — the way in the role found is recorded by code, for every later reader (registry + driver; owner item 3)

given: this spec; `design/factory-rules.md` whole; `plans/builder-rules.md`; F11, F13, F14; A1 merged (`first_look.read()["sign_in"]`).
owns:
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\project_knowledge.py (`record_problems`, new `_sign_in_value_faults`, new `sign_in`, constant `SIGN_IN_KEY`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\references\config-keys.json (section `knowledge`: new row `environments.sign_in`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_stage_plan.py (`_first_look_walk` tail after `_first_look_accepted`, new `_first_look_record_sign_in`)
C:\QAFactory\forge-repo\ai-packages\qa-factory\design\state-exits.md (one row)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_project_knowledge.py (new table rows only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_first_look_wiring.py (new rows only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json (rows of the changed/new units only)
C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fv1-28-c1-sign-in-record.md (new fragment)
non-goals: `config.json` (no write from a story, F13); `env_probe.py` (D1); `manual_capture.py` (fork F-6); `stand_access.py` (FV1-17).
handoff: builder report with witness, FR pass (A, C, D), AR line, census rows.

What to build:
1. Catalogue row `environments.sign_in`: `store: registry`, `scope: stand`, `compare: exact`, `absent_means: "no way in is recorded for
   this stand: the walker finds it itself"`, `needed_by: [S3-S7 briefs, env_probe]`, a `note`.
2. `record_problems`: for `SIGN_IN_KEY` the element is the surface word (`ui`/`http`, read from `first-look-statuses.json` through
   `first_look.data()`), the value the A1 shape minus `evidence`/`why` (shape only, the same limits).
3. `project_knowledge.sign_in(root, stand) -> {"ways": [{"surface", "value", "story", "at", "id"}], "problem"}`: the newest live row per
   surface on the exact stand; PURE, never raises; unreadable registry -> `problem`, never "no way" (FR-59); no stand -> `ways: []`.
4. Driver: right after `_first_look_accepted(FL)` is True, `_first_look_record_sign_in` reads `FL.read(T)["sign_in"]`; non-empty ->
   `project_knowledge.record(root, key="environments.sign_in", environment=<the record's stand>, element=<surface>, state="known",
   scope="stand", value=<shape>, words=<the role's why>, source="role", story=<task>, by="driver", where="first look <walk>",
   task_root=T)`; one printed line "S3: first look: recorded the way in to `<stand>` (<surface>) for later stories" or the refusal's
   reason (P1: never stops S3).
5. `state-exits.md` row: `environments.sign_in` -> way out `project_knowledge.py revoke --id PK-n --words-file F`.

edges:
- INVARIANT (AR-14, P27): the registry is written only by `project_knowledge.record`, and only after the driver ACCEPTED the first look;
  a record `put` wrote under an unaccepted dispatch never reaches the registry (what must stay unreachable).
- A no-trace story (experiment, P8): `record` refuses (`_refuse_no_trace`) -> the line says "not recorded: this run leaves no trace";
  the story's own `work/first-look.yaml` still carries it for this story's readers? NO — readers read only the registry (AR-13); in a
  no-trace story the briefs show no recorded way (fork F-4 names the cost).
- CONFLICT: a newer way for the same stand and surface -> a new row (a changed value is a new row, `:687`); the reader takes the newest.
  The old row stays as history. A person's `revoke` removes it.
- TEMPORAL: before C1 the catalogue has no row -> `sign_in()` returns `problem` naming the missing row (as `lessons`, `:462-464`); after:
  absent rows = `ways: []`.
- EMPTY: `sign_in` `{}` -> nothing recorded, no line.

DoD:
- rows: `record` accepts a ui and an http way (source role, by driver), refuses a wrong shape / a secret value / an empty stand; `sign_in`
  newest per surface, `[]` for another stand, `problem` on an unreadable registry; driver wiring row: an accepted record with `sign_in` ->
  one registry row; an unaccepted one -> none; a no-trace story -> none and the line;
- `test_config_migration.py` and `test_state_exits.py` if `--witness-for` prints them;
- verification: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for scripts/project_knowledge.py references/config-keys.json scripts/driver_stage_plan.py design/state-exits.md`
  and every file it prints, plus `test_judgment_census.py`.
siblings: `project_knowledge.notice_from_handoff` (the other role-sourced write, `:745-768`) — same `by: driver`, the twin; `lessons` —
the reader twin; axis 35 sides rows — same registry, untouched.

### Card B2 — briefs S3-S7 name the recorded way in (brief_pack.py; after C1)

owns: C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\brief_pack.py (new `sign_in_lines`, one call in `build` right after `first_look_lines`); `test_first_look_briefs.py` (new rows); census rows; changelog fragment `fv1-28-b2-sign-in-lines.md`.
What: for the roles of `FIRST_LOOK_KIND` and the first-look walker, one line per recorded way from `project_knowledge.sign_in(root,
stand)`: "Recorded way in to `<stand>` (<surface>, found by the first look in <story>, <date>): <url>; steps: ...; fields: ...; it is what
worked then — if it fails now, find the way yourself and record it." No line when `ways` is empty; `problem` -> one line "the record of
recorded ways in could not be read (<why>)". Edges: no secret values exist in the row (C1 refuses them); line cut at 600 characters with
"whole: `project_knowledge.py show`"; INVARIANT: the line never says the stand is reachable (it is a past observation). DoD: rows for each
reader, empty, problem; verification `scenario_walk.py --witness-for scripts/brief_pack.py` and every file it prints.

### Card D1 — the probe takes the recorded way instead of its guess (env_probe.py; after FV1-5 and FV1-15)

owns: C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\env_probe.py (`probe` login branch only, new `_recorded_way`); rows in the table F6 of the stand-login spec names (`test_http_client.py` if FV1-17's F6(A) lands, else the Lead names it); census rows; changelog fragment.
What: when `project_knowledge.sign_in(root, stand)` holds an `http` way, the probe's login uses its `request` (method, path, body field
NAMES; values from the env keys the access records) instead of the guessed/recorded `environment.access` address; a `ui`-only way -> the
probe does not try a code login and its line says "the recorded way in is through the UI (found by the first look); no code login is
checked" (no Layer-1 block). Edges: INVARIANT — the probe's own guess never overrides a recorded way (precedence: registry way > 
`environment.access` > nothing); a recorded way that fails live IS a measurement -> `blocked_by: login` with "the way in recorded by the
first look did not get in"; lockout invariant of FV1-17 (one submit); unreadable registry -> today's behaviour plus one line (FR-59: never
a pass). DoD: rows recorded-http-ok, recorded-http-refused, recorded-ui, none, unreadable; verification `scenario_walk.py --witness-for
scripts/env_probe.py` and every file it prints.

### The seam left for FV1-29 (not designed here)

FV1-29 adds the walker command card to the automator. Seam: in `brief_pack.build`, the walker lines go right AFTER the block
`first_look_lines(...)` returns for `("S5", "qa-automator")` (and after B2's `sign_in_lines`), triggered by the same `_fl_state` kind
(`null`/`absent`/`unreadable`/`stale`) or B1's "no row of this window names where it lives" condition — B1 leaves both as named
constants/kinds FV1-29 can read; B1's GAP sentence already ends "look yourself with the tools your brief names", which FV1-29's card
makes true for S5. B1 does not touch `agents/qa-automator.md`.

## §3 Acceptance rows (completeness criterion)

| Item | Card | Note |
|---|---|---|
| finding item 1 (substance, window) | B1 | — |
| finding item 2 (probe guess never a fact; role decides; reader sees a gap) | A1 (due, form), B1 (gap, runner line) | the reader's own walker: FV1-29 |
| finding item 2 last para (re-read FV1-5) | §0 re-read | no contradiction in FV1-5's card; the chain is A1's |
| finding item 3 (role finds, code records, probe and briefs read, guess never overrides) | A1 (form), C1 (record), B2 (briefs), D1 (probe) | store: fork F-1 |
| finding "Тест" line | B1 DoD row 1; A1 DoD row 1 | "no_stand без пробы путём тестов не записывается" = A1 `due` row |
| dry row `first_look/probe_405` | A1 (the dispatch happens on a refused login) | stays `known_red: FV1-28` until P1-b's harness exists (F19); flips green when A1 merges and P1-b runs |
| dry row `first_look/empty` | B1 gap rows | DEFECT of the row's seed: the real writer refuses `rows: []` (F18); the seed must be `put --null walk_not_opened` or all-`unreachable/access` rows — returned to the Lead (fork F-7) |
| dry row `first_look/absent` (same label) | B1 gap rows | — |
| dry row `first_look/entry_recorded` | A1 + C1 + B2 + D1 | green only after D1 (probe reader), i.e. after FV1-15; until then `after: FV1-28 D1` for the probe part |

## §4 FR-33 live-proof row (for `live-runs`)

"MyBooks story whose S0 probe fails on the recorded login (old config: `/login` 405): the first look IS dispatched, the walker signs
in by the UI itself and records `sign_in`; the registry holds `environments.sign_in` for the stand; the S5 window brief carries the url,
steps and locators of the window's requirements; a SECOND story on the same stand shows the recorded way in its S3-S7 briefs and the
probe uses it (after D1)." Moves to `live-runs` per PROJECT.md «Командная работа» 9 when the nodes are accepted.

## §5 SIBLING_MAP axes (enumeration; one block for the node's mechanisms: A1 due/form, B1 lines, C1 record, D1 precedence)

- axis 1: n/a — no policy/role-file/journal change.
- axis 2: n/a — no exam instrument.
- axis 3: covered by the release procedure — package files only; changelog fragments per card.
- axis 4: n/a — no FR text change; no debt row added.
- axis 5: covered — `_fl_state` is the one wording for S3-S7 (all twins change together); `notice_from_handoff`/`lessons` named as C1 twins.
- axis 6: queued — `report_facts.knowledge_use` counts first-look rows; a counter for "recorded way used" is not added (critic to judge).
- axis 7: n/a — no test identity.
- axis 8: n/a — no new story path; registry path unchanged.
- axis 9-11: n/a — no test-file, git-top, shell-command logic.
- axis 12: covered — node rows in batch-1 by the Lead; no new pile file.
- axis 13: n/a — dispatch text cut unchanged.
- axis 14, 15: n/a.
- axis 16: covered — every JSON read through `hooklib.read_json` / `first_look.data()`.
- axis 17: n/a — no detector output.
- axis 18: covered — no ratchet row raised; census rows only added for new units (named per card).
- axis 19, 20, 22: n/a — host-independent.
- axis 21: n/a — no markdown table read.
- axis 23, 24, 27, 28: n/a — no `tests[]` row field, run join, profile or row-form render touched.
- axis 25: n/a — freshness predicates untouched (stale record keeps `first_look.read`).
- axis 26: covered — `stand not confirmed` word untouched; S6 `s6_no_stand` named as a sibling, not changed.
- axis 29: n/a — no jsonl append.
- axis 30: n/a.
- axis 31: covered — the role carrier for "first look before discovery" stays `qa-automator.md:55` (FV1-29 owns edits).
- axis 32: covered — §1 table: every check shape/presence; judgment stays with the role and the driver's acceptance.
- axis 33: n/a — dispatch identity untouched.
- axis 34: covered — one road: the gap text is one for every reader; the way in has one store and one reader; no language/project branch
  (surface words are data). Residual named: `manual_capture.login_recipe` not reading the recorded `ui` way (fork F-6, node with owns).
- axis 35: covered — registry rows of sides untouched; same writer reused.
- axis 36: n/a — placeholder rows untouched (B1 keeps the s5 head's placeholder sentence).
- axis 37: n/a.

## §5a Four questions (rule 10), per mechanism

- A1 (due/form): (a) cost — a walker dispatch now runs on stories with a refused probe (one paid S3 runner dispatch; the free agent spent
  6.5 min on the same look, finding `:14`); paid by the factory run. (b) axes above. (c) detector — `test_first_look.py` rows;
  dry row `first_look/probe_405` once P1-b runs; live row §4. (d) on the path — `due` is called by `first_look_step` on every S3 entry.
- B1 (lines): (a) brief bytes per window (measured in the DoD; not in U/H, F15); paid by the automator's context. (b) above. (c)
  `test_first_look_briefs.py`; dry row `first_look/empty`. (d) `build` calls it for every S3-S7 brief.
- C1 (record): (a) one registry row per new way; a person revokes a wrong one. (b) above. (c) `test_project_knowledge.py`,
  `test_state_exits.py`, `test_judgment_census.py`; dry row `entry_recorded`. (d) the driver writes after acceptance; no role writes it.
- D1 (precedence): (a) none beyond today's probe. (b) above. (c) D1 rows; live row. (d) the probe runs at S0/S5 by code.

## §6 Forks (returned; recommendation first; what stays executable before the answer)

- F-1 — WHERE the role's way in is recorded. (A, recommended) the answer registry, new catalogue row `environments.sign_in` (stand scope;
  one writer `project_knowledge.record`; one reader `sign_in`; provenance and revoke exist; lives across stories = "для всех остальных").
  (B) only the story's `work/first-look.yaml` (story scope: the next story rediscovers; the probe at S0 of the next story never sees it).
  (C) `config.json` `environment.access` / `manual_capture.login.ui` written by code from a story (contradicts FV1-15 F7(A) and FV1-17's
  "onboarding writes access"; a third writer of config while OF4-28 is unifying writers). Before the answer: A1 and B1 are executable
  (they do not depend on the store); C1/B2/D1 wait.
- F-2 — `no_stand` when NO stand is named. (A, recommended) code keeps `null: no_stand` for an empty `environment` (a fact of the story,
  not a probe), worded as a GAP by B1. (B) dispatch the walker anyway with "find the stand" (it has no address; cost: a paid dispatch
  that can only fail). Executable before the answer: A1 on (A).
- F-3 — the brief budget for the s5 substance. (A, recommended) window rows whole, one line per item, no count cap, item clip 400 with
  `whole:` (estimate, not measured: ~5 requirements x ~6 items x ~120 B ≈ 3.6 KB ≈ 900 tokens per window; the brief is outside U/H, F15,
  so no ratchet moves; nothing leaves the brief in exchange — if the Lead wants an exchange, the s5 head's placeholder sentence (~300 B)
  can move to the charter line 55, owned by FV1-29). (B) keep the 12-line cap and the pointer (today; contradicts AR-21 "whole" for big
  windows). (C) a side file `work/briefs/<id>-first-look.md` with the window's substance and one head line (side files count per story,
  `role_load.py:584-586`). Also for S4's `s4` kind: same choice, not changed here.
- F-4 — a no-trace (experiment) story: (A, recommended) the registry write is refused as for every fact (P8, FR-53); the story's briefs
  show no recorded way; comparison runs therefore rediscover each time (that is the experiment's meaning). (B) a story-scoped reader of
  `first-look.yaml` `sign_in` as a fallback (a second reader of the same fact: AR-13 breach).
- F-5 — does the record belong to the OF3 knowledge store? Yes: plan §2.2 names "карточка окружения: ... вход" and phase 3 absorbs
  "B-254 и OH3-17 (одно описание входа на стенд)" (`M\plans\project-knowledge-plan.md:76`, `:243`). (A, recommended) build it NOW as one
  catalogue row by the plan's own recipe §2.5 (a row, no new mechanism — as SS1-11 did for `stand_lessons`); OF3-3 later folds it into
  the stand card with the other entry facts. (B) wait for OF3-2/OF3-3 (no commit of them on main beyond K6, batch-3 «Ход» 14.11): the
  owner's third word stays unbuilt until then. Before the answer: C1 on (A); the Lead tells the OF3 owner (dev1) the row exists.
- F-6 — P31: the walker's own sign-in (`manual_capture.login_recipe`, `walk_session` sessions) does not read the recorded `ui` way.
  (A, recommended) node FV1-28e after C1: `login_recipe` takes the registry `ui` way before the factory default and after the project's
  `manual_capture.login.ui` (owns `scripts/manual_capture.py` `login_recipe`; rows in `test_manual_capture.py`; gate-A proof still needed —
  `sign_in_refusal` unchanged). (B) leave the walker to find it again each story (cost: the first look re-discovers sign-in per story).
- F-7 — the dry row `first_look/empty` seeds `rows: []` + `gaps`, which the real writer refuses (F18; P1-b's "only real writers").
  (A, recommended) the Lead amends the row's seed to `put --null walk_not_opened` (and a second row: all rows `unreachable/access`).
  (B) let `put` accept `rows: []` with gaps (changes the form: a requirement could drop out silently — NE37 of `null-outcomes.json`).

## §7 Small choices closed by the designer

- Surface words `ui`/`http` live in `first-look-statuses.json` (the first look's closed words; one reader `first_look.data()`).
- No new `null_reasons` word: "the role could not reach" uses existing `unreachable` + `access` rows.
- Item clip 400, steps cap 20 x 300, url/selector 500, B2 line 600 — chosen to hold a whole selector and a NextAuth-style route.
- B1 passes `scope` to `first_look_lines` as a keyword with default None (every other caller unchanged).

## §8 Contradictions with the brief (reported, not widened)

- "FV1-17 built the login record (`stand_access.py`, `references/stand-answers.json`, the answer registry)": FV1-17 is spec-only (F12);
  `references/stand-answers.json` is FV1-15's (`login_remedies`); the registry is phase-0 `project_knowledge` (F11 d). This draft reuses
  the registry, not a FV1-17 record.
- "the automator is over H; every byte added to its brief is a cost against H": the brief is not in U/H (F15). The bytes are real context
  read by a tool call; measured in B1's DoD; no ratchet row applies (fork F-3).
- "the brief carries only a pointer line": true for the run (null record, F3/F4); on main a non-null record already reaches S5 as
  locator/api/sample/data lines, capped (F1, F2).

## §9 What I did NOT establish

- The run's package version and whether its S5 brief had FL-4 lines (no run log or brief in the repo, F6).
- Whether `walk_session.py open` refuses a stand that is `environment_pending` (not read; A1's builder reads `walk_session.open` and
  names the result: if it refuses, the cause word is carried by `_first_look_give_up`, never `no_stand`).
- The exact keyword `walk_session.capture_cited` needs for a capture outside a requirement item (A1 item 2 names the fallback: `quote`).
- `docs/SIBLING_MAP.md` axis bodies (only headings read); `references/stage-joints.json` beyond the first-look group lines; the P1-b
  harness spec body.
- `code_friction` before/after: not measured (no run); open item for the live row.

## §10 Reading trail

Read (M\ = read-main): the finding (whole); batch-1 rows FV1-5/15/17/28/29 (Grep); plan `:340-386`; amendment `:400-466`; stand-login
spec `:1-80`, `:150-536`; `first_look.py` (whole); `brief_pack.py:3990-4440`; `app_card.py:320-399`; `driver_stage_plan.py:1-330`;
`driver_s0.py:2295-2340` + Grep `env_probe`; `project_knowledge.py:1-125`, `:300-344`, `:425-714`; `manual_capture.py` Grep defs
(`read_login`, `sign_in_refusal`, `login_recipe`, `login_declared_none`, `http_login_source`); `walk_session.py` Grep `login|sign.in`;
`stages.json:95-264`; `artifact-contract-first-look.md`; `first-look-statuses.json`; `role-load.json`; `role_load.py` Grep `brief`;
`architecture.md:55-296`; `qa-automator.md:50-59` + Grep; `contract.py:3615-3644`; t1r spec `:20-45`; FV1-4 spec Grep `FIRST_LOOK|T3b`;
stage-critics spec `:936-949`; statuses report Grep; `project-knowledge-plan.md:46-295`; onboarding-forge batch-3 `:1-40`; SIBLING_MAP
headings; `test-layers.json` Grep (keep rows, `"quarantine"` line); the run's `first-look.yaml`.
Greps with controls: `def recorded_login|def try_roads|def recorded_seconds` over worktrees (control: `recorded_seconds` hit);
`first.look` in `inject-map.json` -i (none; control `qa-automator` -i: 9 hits); `probe_405|entry_recorded|first_look/empty` over M\ (one
file); Glob `runs/factory-out/*/*` (control: `first-look.yaml` listed).
