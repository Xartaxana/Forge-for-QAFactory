# Critic on plan — FV1-28 (t-755): the first look reaches the automator; a skipped look is a gap; the role's way in is recorded

Plan under review: `docs/tasks/specs/20261114-fv1-28-first-look-to-automator-spec.md` (designer t-749). Requirement = the three owner
quotes at its top, checked against the finding `plans/piles/live-run-fvf/findings/20261113-pervyj-vzglyad-ne-dohodit-do-avtomatora.md:22-23, 34-35, 39-40`.
Package read on origin/main `7379e0d`. The read-main worktree sits at `ba903eb` and is behind. The only node file that differs is
`driver_stage_plan.py` (+51 lines at the top: `register_gap_rows`), so every `driver_stage_plan.py:NNN` the spec cites is 31-51 lines
off on main (`first_look_step` is now `:184`, `_first_look_accepted` `:233`, `_first_look_give_up` `:246`, `_first_look_walk` `:261`).
The function names still hold. Nothing was edited except this file. No CI, slow or quarantined tests were run.

**Verdict: fit_with_fixes.** The plan's direction is right on all three owner words, and the forks are mostly right. But one missing
card (N1) would make A1's headline outcome fail on the very stand that motivated the node. Card D1 cannot carry the way in that stand
actually uses (N9). Eight more card-level defects need fixing before dispatch. The binding amendments are in §B.

---

## Key 1 — Owner's words vs cards; the §0 re-read of FV1-5

| Owner item | Carried by | Verdict |
|---|---|---|
| «первый взгляд … то же что делал агент»; «брать то что уже знает фабрика, но если не хватает — идти и смотреть сам» | B1: the substance reaches S5. FV1-29: the automator's own look. B1 gap sentence | Carried, but FV1-29's half is outside the node and named. B1's gap sentence sends readers that have no stand tool to "look yourself" (N7) |
| «агент сам определяет как войти … не прописывать действия, просто не мешать» | A1: `due` no longer skips on a failed probe. A1 form: the role records its way | **Not carried end to end.** A second code probe still skips the look: the runtime-provenance probe at walk open (N1). A1 removes one probe's veto and leaves the other's |
| «результат должен записываться … Роль находит как входить, код записывает для всех остальных» | C1 (registry), B2 (briefs), D1 (probe), FV1-28e (walker recipe) | Carried for later stories. **Not carried within the same story** when the story is no-trace (F-4, N6). That is the class of the run that raised the finding: the ARM `pipeline.json` says `"no_trace": true` |
| finding item 3: «догадка пробы никогда не перекрывает эту запись» | D1 precedence: registry > `environment.access` | Carried. The stale-record direction is unstated (N10) |

Deviation the spec does not name: finding item 2 (`:30`) says «`no_stand` пишется только тогда, когда РОЛЬ не смогла дойти до стенда».
The spec has the role write `unreachable/access` rows instead, and keeps code's `no_stand` for an empty `environment` (F-2 A). I think that
choice is right: `put_problems` refuses `rows: []` (F18, `first_look.py:410-414`), and an access row with `why` says more. But §3 marks
item 2 "covered". It has to say outright that it departs from the finding's own text, and why (amendment 14).

The §0 re-read of FV1-5 is right, checked on the diff `git diff origin/main...wip/fv1-5`. `driver_s0.py:2432` changes only the sentence
("did not pass the check"); the code still sets `pending` on any non-zero exit (main `driver_s0.py:2424-2428`, `if code == 0: pending =
False`). `blocked_by` is read only by `driver_stage_build.stand_question_text`; `first_look.due` never reads it. Reading «проба входит
так, как входит тест» as FV1-17's `harness_command` road matches the carriers too: the phrase appears in the repo only at finding `:37`,
and `harness_command` appears in the two onboarding findings of the same pile.

## Key 2 — Facts by trail

| Fact | Carrier, read | Result |
|---|---|---|
| F1 | `brief_pack.py:4127-4130`, `:4216-4222`, `:4408` | right |
| F2 | `:4121-4122`, `:4154-4163`, `:4241-4265` | right |
| F3 | `:4166-4186`, `:4016-4034` | right. The ARM S5 briefs 1-9 each carry exactly "First look: there was no first look - the stand was not walked (no stand)." (grep of `work/briefs/S5-qa-automator-*.md`, lines 14/15/18) |
| F5 | `experiments/.../factory-out/work/first-look.yaml` (origin/main) and the ARM copy `LOCAL-1/work/first-look.yaml` | right, byte for byte |
| F6 | — | partly wrong: the ARM story folder DOES hold the run's S5 briefs (`LOCAL-1/work/briefs/S5-qa-automator-1..9.md`, 11,470-20,678 B). They are outside the repo, so the claim holds only for the repo |
| F7 | `first_look.py:661-663`; driver `first_look_step` `:184-216` (main) | right (line refs stale, see head) |
| F8 | main `driver_s0.py:2424-2428`. **Measured on the run:** `LOCAL-1/state/events.jsonl` rows 1-18 (S0 done through S2) carry `"environment": "local"`, `"environment_pending": true`; today's `pipeline.json` says `false` (set after the S5 stand answer) | right; the run skipped on the `pending` branch, not on an empty stand |
| F9 | `walk_session.py:1173`, `:1245-1249` | right, and it hides N1: the "stand probe" at open is `MC.stand_probe`, the runtime-provenance probe, which refuses `unknown` |
| F10, F11 | `manual_capture.py:2940-2954`, `:4870-4883`; `project_knowledge.py:119-120` | right. A sixth reader is missing from F11: `app_card` section "Sign-in" (`app_card.py:185-204`) renders `login_recipe` to every walker; in ARM `work/app-card.md` it reads "Sign-in route: /login; fields: username field "" …" |
| F12, F13 | stand-login spec `:235-241`, `:389-392`, `:490-496` | right |
| F14 | `project_knowledge.py:611-668` | right. The role checks (`_unsafe_role`, `reserved_role`) run for every key that is not a side key or `LESSONS_KEY`: C1 needs its own branch before them (N8) |
| F15 | `role_load.py:56-60`, `:460-470`, `:527`; `role-load.json` allowances `brief: 6144` (bytes, same unit as `packet: 5400`) | right. The spec says "6144 tokens"; it is bytes |
| F16 | `agents/qa-automator.md:55` | right |
| F17 | `contract.py:3622-3624`; `brief_pack.py:1297`, `:4420` | right |
| F18 | `first_look.py:410-414`, `:504-528` | right |
| F21 | `test-layers.json` keep rows | off by one (288, 4094, 6738, 6834, 6848 on main); harmless |

The three "contradictions with the brief" in §8: **the designer is right on all three.** (1) FV1-17 is spec-only: there is no
`recorded_login` or `try_roads` in any worktree's diff, and the batch row FV1-17 says the same. (2) The brief is outside U and H:
`FIRST_REQUEST_LAYERS` (`role_load.py:59`) has no `brief`. (3) On main a non-null record already reaches S5, capped at 12.

§9 items, measured:
- **Does `walk_session.py open` refuse an `environment_pending` stand?** It does not read the flag. A case-insensitive Grep of
  `environment_pending` over `scripts/*.py` lists 22 files and `walk_session.py` is not among them; the same call lists `first_look.py`,
  which is the positive control. **But `open` does refuse on the runtime-provenance probe:** `_open_actors` → `MC.stand_probe`
  (`manual_capture.py:1579-1609`) → `acceptable_provenance(value, ACCEPTS)`, where `ACCEPTS = ("matched", "person_confirmed",
  "not_applicable:no_changed_file")` (`profile_contract.py:875`). An `unknown` raises `EnvBlocked`, then `ServerDead`, then
  `_first_look_give_up(... "walk_not_opened")`. A refused sign-in does NOT stop the open: UI actors open unsigned with a note
  (`walk_session.py:1302-1304`); HTTP-only actors open with `signed_in: false` (`:1262-1289`). See N1.
- **What `capture_cited` needs:** the signature is `capture_cited(task_root, walk, item, path, quote="", stand="")`
  (`walk_session.py:569`). The docstring (`:578`) says "An empty quote is refused too". The capture must sit under
  `work/evidence/manual/survey-<item>/<attempt>/` of THAT item (`:599-608`). So A1's literal call with `""` always refuses: `quote` AND
  an item are required (N3).

## Key 3 — Feasibility (functions, signatures, positions)

- A1: `due`, `put_problems`, `put`, `read`, `TOP_KEYS` exist (`first_look.py:60, 394, 504, 558, 647`). `read()` returns a fixed dict
  (`:563-564`) and gains `sign_in`; `put` builds the record from `frame + rows + gaps` (`:545-548`) and must add `sign_in` there. The
  position in `due` is right: the stand test sits at `:661-663`, between the register checks and the attempt check, and only its second
  operand goes away. Invariant check: "no paid walk when no stand is named" still holds. The edge "a dead stand → `walk_not_opened`" holds
  as well, but at a price: walk open runs a probe that ALSO refuses a live stand (N1).
- B1: `first_look_lines(task_root, stage, role)`, `_fl_body`, `_fl_state`, `_fl_line`, `_Clipped`, and `build`'s `scope` all exist; the
  position (after `provisional_lines` `:4402`, before `prior_retro_lines` `:4411`) is as stated. `FIRST_LOOK_ITEM_CHARS` per item with
  the `_Clipped` road works. Uncapped `s5` reaches every S5 automator dispatch kind, not only windows (N5).
- C1: `record(root, *, key, environment, element, state, scope, value, words, source, story, by, where, task_root)` matches
  `project_knowledge.py:671`; `_refuse_no_trace` `:543`; `revoke` `:704`; the duplicate rule (same state AND value) `:686-694`. The driver
  hook point after `_first_look_accepted` is `_first_look_walk:327`. Missing: the skill-road twin (N8).
- B2: `stand_lesson_lines` (`brief_pack.py:2875`) is the exact twin to copy; the call site in `build` is fine.
- D1: `env_probe.probe` login branch is in FV1-5's diff right now; the single-request `request` shape cannot express the stand's real
  login (N9).

## Key 4 — P27 / AR-29 / AR-2; P5

What code still decides in A1:
- (a) An empty `environment` gives `no_stand`. That is a story fact; right.
- (b) `parks_after_s5` and the register gates. Data; right.
- (c) **The runtime-provenance probe at walk open decides "no look" on `unknown`** (N1). That is a probe's guess vetoing the role's
  work — exactly the class of the owner's word.
- (d) The shape of the role's `sign_in`. Data; right.

The owner word "the role decides, not the probe" is met only for the login probe. Census classes in §1 need correcting: the secret
refusal inside `_sign_in_faults` / `_sign_in_value_faults` is class **safety**, not shape (the census vocabulary is shape, xref,
word-list, meaning-proxy, meaning, safety; `judgment-census.json` "about"). The evidence tie through `capture_cited` is **xref**.

The driver's `_first_look_accepted` reads the controller's dispatch status. That is the right census class (shape), but §1 calls its
owner "judgment = the tier above". The controller's `accepted` for a first-look dispatch is code acceptance of a finished dispatch, not a
tier-above judgment of the way in. Writing a role-sourced row as `known` (the first role-sourced `known` row in the registry:
`notice_from_handoff` writes role facts as `noticed_unconfirmed`, `:767`) is legitimate under the owner's «код записывает». But readers
must not rank it above a person-or-onboarding fact without saying so (N10).

P5: no read route goes through an LLM agent. The role walks with the factory's recorder tools and its captures are evidence; code writes
the registry; readers read files. The secret values never pass through the role, because `fill-account <selector> <actor> user|secret`
(`manual_capture.py:2953`) types them by actor.

## Key 5 — C1: the store, secrets, no-trace

- **F-1 (A): agree.** The knowledge plan names the way in as a fact of the stand card, asked at first need
  (`project-knowledge-plan.md:76`, `:174`, `:190`, `:243`). No OF3 node writes `project_knowledge.py` or `config-keys.json` today: the
  worktree scan found no diff on those paths; OF3-2's remaining parts and OF4-18/OF4-23 are «ожидает» (batch-3 «Ход» 14.11, batch-4
  rows 48 and 53). One writer is preserved (`record`). One reader (`sign_in`) is right, provided D1, B2 and FV1-28e take the precedence
  from that one reader (N10). For the record: C1 adds a new carrier of "how the stand logs in" to the axis-5 row «How the stand logs in
  (two carriers, B-254)» (`SIBLING_MAP.md:127`). That row's own rule ("a change to … the login path or the landing proof names all of
  them") requires the row to be updated in the same commit, and the spec does not do it (amendment 13).
- **Secrets: the guard as designed is wrong in both directions.**
  - Over-refusal. (i) `app_card.scrub` first normalises whitespace (`" ".join(text.split())`, `app_card.py:76`), so any value with a
    double space, a tab or an edge space differs from its scrub and is refused as a "secret". (ii) `tokens=True` replaces any
    letters-and-digits run of 24 or more characters (`_LONG_MIXED`, `:68`); the codebase's own reading says structural fields go
    through `tokens=False` because "a long `data-testid` is not a secret" (`app_card.py:348-350`). A selector like
    `[data-testid=login-form-submit-button-v2]` would be refused.
  - Under-refusal. `_KV` catches only `password: x` / `password is x` forms (`:64`), so a bare value in `steps` ("type admin123 into
    the password box") passes.
  - Fix: compare structural fields with `tokens=False` against the whitespace-normalised value, and ALSO refuse any field holding a
    literal value of the stand's accounts. The values are read in memory through `manual_capture.read_login` / `resolve_actor` and
    never printed; that is the exact guard. The record names the `actor` it signed in as, never keys or values (amendment 3). The error
    direction is over-refusal: the refusal names the field, never the value.
- **F-4 (A): object in part.** Refusing the REGISTRY write in a no-trace story is right (P8, FR-53; `_refuse_no_trace` already does it).
  But the same story's own S3-S7 readers then lose the way the first look found. The run that raised the finding is no-trace
  (`LOCAL-1/pipeline.json` `"no_trace": true`), so in the comparison run the automator still rediscovers sign-in, and the free agent
  keeps that edge. The story's `work/first-look.yaml` `sign_in` is that story's observation, read through `first_look.read`. That is the
  SAME reader the rows already go through, not a second reader of the registry fact. B1 (or B2) must render the story's own `sign_in` to
  that story's S3-S7 briefs whatever `no_trace` says; B2 renders registry rows from OTHER stories (and skips a row whose `story` is this
  one) (amendment 6). The cross-story half of the §4 live row cannot be proved by a no-trace run (question Q1).

## Key 6 — D1 precedence and the direction of error

- The precedence registry > `environment.access` matches finding item 3. **The stale direction is unstated and partly unrecoverable.**
  Take a person who corrects `environment.access` after the stand changed its login, while the registry still holds an old `http` way.
  D1 then fails every probe with "the way recorded by the first look did not get in". A later first look that signs in by UI writes a
  `ui` row and leaves the stale `http` row in force (newest per SURFACE). The only exit is `revoke` (FR-40 exists), and the probe's
  line does not name it. Amendment 10: the probe's failure line names `PK-n` and the door, and the S0 warning carries it.
- **FV1-28e's precedence is the reverse of D1's.** F-6 says "registry `ui` way before the factory default and AFTER the project's
  `manual_capture.login.ui`"; D1 puts the registry before the config. That is one fact with two precedence orders (P31). One rule, stated
  once in `project_knowledge.sign_in` (or a helper beside it), and read by both (amendment 11).
- **D1's `ui`-only branch turns an unchecked login into a pass.** "no code login is checked … (no Layer-1 block)" confirms the stand for
  the tests on evidence that a role signed in through a browser. The probe's login layer stands for the tests' road (FV1-17: «проба
  входит так, как входит тест»). FR-59 / AR-28: an unknown never becomes a pass. FV1-17 already designs the same fact as data — `access.kind:
  ui_only` set by the person ("the tests sign in through the UI only", stand-login spec `:239-241`, `:73`) — so D1's branch is a second
  road for it (P31). Amendment 9b.

## Key 7 — B1 / F-3 cost; U/H; P11

- The ARM story holds no non-empty first-look record (`LOCAL-1/work/first-look.yaml` = null `no_stand`, 300 B), so the s5 substance
  cannot be measured on real data. The designer's ~3.6 KB per window stays an estimate. What the run does measure: S5 automator briefs of
  11,470-20,678 B (`wc -c LOCAL-1/work/briefs/S5-qa-automator-[1-9].md`, total 144,794 B for 9), against `allowances.brief` 6144 B. Real
  briefs already run at 1.9-3.4 times the allowance.
- "Outside U/H" is true (`role_load.py:58-60`). It is not a P11 hole in design: `build` writes `state/brief-sizes.jsonl`
  (`brief_pack.py:4283-4294`), and `run_counters` reads it (`run_counters.py:37`, `:550`). The ARM run has no such file (`ls state` shows
  none); `run_counters` itself says "the record predates its writer". So the bytes are measured on a current package.
- **F-3 (A) is right for windows, but the spec leaves the cap open for the other S5 kinds.** `first_look_lines` serves every S5 automator
  brief: `plan`, `window`, `legacy` and `unknown` kinds (`brief_pack.py:4371-4387`). B1's edge "scope None / plan dispatch / legacy → all
  rows (today's behaviour plus items)" with "no count cap for kind s5" would print the WHOLE record item by item for the plan dispatch.
  On the ARM register (33 requirements; `grep -c` in `requirements-register.md` gives 33) at the designer's ~6 items × ~120 B, that is
  about 24 KB added to a ~11-20 KB brief, for no window. Amendment 5: no count cap only for `s5_kind == "window"`; the plan, legacy and
  unknown kinds keep the 12-line cap and the `+N more` pointer.

## Key 8 — F-6 / P31

C1 can ship before FV1-28e without creating a second road for the ROLE. The walker reads the recorded way from B2 and signs in through
the existing `fill-account` word. The code sign-in (`login_recipe` with `sign_in_refusal`) acts only with gate-A proof, and a
role-recorded way has none. So F-6 (A) as a later node is acceptable under rule 19, on two conditions:
(1) the node is opened in the batch file with its owns in the same move (proposed, not "recommended");
(2) its precedence is the shared one (amendment 11).

Note for the node: the recipe also feeds the no-screenshot window of a sign-in (`landing_rule(self.recipe)`, `walk_session.py:1201`;
`url_not` in `SessionAccount.window`, `SIBLING_MAP.md:127`). When the real sign-in page differs from the config's, that window keys on
the wrong page. FV1-28e is therefore a safety question as well as a convenience, so it must not drift.

## Key 9 — F-7, the dry row

The `empty` row's seed reads «заглушка роли пишет `rows: []` + `gaps`» (amendment spec `:443`, column «только настоящие писатели»).
With the real writer, that stub is refused (F18) and the record ends absent, which is the `absent` row again. Rejecting F-7 (B) is right:
NE37 (`null-outcomes.json:137-140`) is exactly the guarantee that no requirement drops out silently.

**F-7 (A)'s first seed is wrong.** `put --null walk_not_opened` is the DRIVER's road (`_first_look_give_up`). A role stub calling it
breaks "only real writers", and it writes a false reason, because the walk did open. Amendment 12: the `empty` seed is the role stub's
record whose rows are all `unreachable` with `blocked_by: access` and a capture. That is the role's real empty outcome; note that
`no_capture_needed` is only `nature`, so an access row must cite a capture. The null case stays covered by the `absent` row and by a
driver-path seed (an empty `environment` gives `no_stand` through `due`).

## Key 10 — Edges per card (rule 11)

| Card | Missing edge | Amendment |
|---|---|---|
| A1 | evidence: `quote` and the item (N3); a `ui` key under `surface: http` and the reverse (a conflicting pair, unstated); empty `steps: []`, empty `evidence: []`; the secret check's error direction; DoD rows for the url/selector limit at 500 and 501 (named in edges, absent from the DoD) | 2, 3 |
| A1 | POSITIONAL: the walk open still refuses on provenance (N1) | 1 |
| B1 | the cap for plan, legacy and unknown kinds (N5); which kinds get the "all unreachable/access" line (S5 only, or S3-S7?); readers with no stand tool told to "look yourself" (N7) | 5, 7 |
| C1 | **CONFLICT: `sign_in` present while every row is `unreachable/access`.** The spec stores it, and C1 then records it as a working way for every later story although the role reached nothing. Only an accepted record with at least one row NOT blocked by `access` may reach the registry | 4 |
| C1 | POSITIONAL: the `SIGN_IN_KEY` branch in `record_problems` goes BEFORE the role rules (as `LESSONS_KEY` does, `:644`); the invariant is "a surface word never meets the role checks, and a role key never skips them" | 8 |
| C1 | TEMPORAL is stated; the skill road (phases/s3.md) is not (N8) | 8 |
| B2 | the 600-character cut names `project_knowledge.py show`, a command for roles that may have no shell (`first_look_input_line` docstring `:4019-4020`: "No script is named: the roles that read this line may have no shell"). Name the file `qa-factory/records/project-knowledge.json` instead | 7 |
| D1 | NextAuth needs two requests (csrf then submit), so a single `request` cannot express it (N9); which account signs in (the record must carry `actor`); `ui` only (N9b); stale `http` row (N10) | 9, 10 |

## Key 11 — Tests against docs/TESTING.md

- A1's real behaviour change is a driver flow: "a pending stand → the walk opens → the dispatch is registered". Its home is the scenario
  keep file `test_first_look_step.py` (layer `scenario`, test-layers row 6753), as ONE row taken from the live defect. A
  `due`-function row in `test_first_look.py` (layer `gate_named`) is "a test per function" (TESTING.md «Чего больше нет»). Amendment 15.
- The role's `sign_in` is input from OUTSIDE, so it gets the adversarial mini-battery (rule 11) as ONE parameterised table with case ids:
  magnitude (steps 20/21, a line at 300/301, url/selector 500/501), nesting (a mapping where a line is expected), encoding (non-UTF-8,
  the existing `_load_input` row), empty (absent, `{}`, `[]` in lists, an empty string), plus wrong-surface keys and a secret value. The
  secret case has two halves, a literal account value and a long `data-testid` that must PASS.
- C1/B2/D1 ask for per-branch reader rows (newest per surface, another stand, problem, etc.). Those are internal boundaries ("an internal
  boundary gets no test"). Keep one data-join row per producer → reader (`put` → registry row → `sign_in()` → brief line) and one scenario
  row (accepted first look → registry → the next story's brief). The rest goes.

## Key 12 — Order and overlap (worktree scan of `git diff origin/main...HEAD` plus `status` across all worktrees)

| Branch | Node files touched | Effect |
|---|---|---|
| `wip/fv1-5`, `wip/wave13` | `env_probe.py`, driver files | D1 waits (as planned) |
| `wip/fv16-n2` | `brief_pack.py` `case_concern_lines` only | function-disjoint with B1 (D-0048), parallel OK |
| `wip/tbw-t1r` | `judgment-census.json` (rows) and qa-automator slices | census rows only; append conflicts expected, resolved by the later merge |
| `wip/fv1-9-ta` | no diff left against origin/main | none |

No worktree touches `first_look.py`, `walk_session.py`, `manual_capture.py`, `project_knowledge.py`, `config-keys.json` or
`artifact-contract-first-look.md`.

Runnable in parallel today: **A1 ∥ B1 ∥ A2** (the new card of amendment 1: `walk_session.py` survey open plus the
`manual_capture.stand_probe` caller; disjoint from A1 and B1). C1 waits for A1; B2 for C1; **D1 waits for FV1-5 AND FV1-17** (not only
FV1-15). With amendment 9a, D1 runs the recorded http way through FV1-17's `stand_access` road executor, which exists only in a spec
today. The census file is shared by every card, so dispatches must say "rows only, merge by appending".

## Key 13 — §5 axes and the four questions

- **The current map has 36 axes, not 37.** A case-insensitive Grep of `Axis 3[7-9]` over `docs/SIBLING_MAP.md` finds 0; the same call
  shape with `Axis 3[4-6]` finds 5. The line "axis 37: n/a" enumerates an axis that does not exist.
- axis 5 "covered" is wrong in two places. (i) The first-look row (`SIBLING_MAP.md:157`) requires "the driver's road and the skill's
  road change together": C1's registry write exists only on the driver road, so the skill road (`skills/qa-story/phases/s3.md`,
  lines 12-17 and 39-56) writes nothing after an accepted look (N8). (ii) The row «How the stand logs in» (`:127`) must name the new
  carrier.
- axis 6 "queued — critic to judge" is not a queue (rule 9: an explicit pointer or a fix). My judgment: `knowledge_use` counts
  first-look markers as SETS of R-n (`report_facts.py:2020`), so per-item lines do not inflate it. Whether a registry `sign_in` row
  reaching a brief is counted needs either the `[knowledge:environments.sign_in]` marker on B2's line or a queued row naming
  `report_facts.knowledge_use`. Pick one in the spec.
- axis 34 "covered": not until amendments 9b and 11 land (`ui_only` vs the D1 ui branch; two precedence orders).
- Four questions: (c) for A1 names the dry row and the live row, but the live row cannot pass without amendment 1. (d) "D1: the probe
  runs at S0/S5 by code": right.

---

## §B Binding amendments (one sentence each)

1. **New card A2** (`walk_session.py` `_open_actors`, the survey branch only, plus the `manual_capture.stand_probe` caller): on a
   `place survey` walk, an `unknown` runtime provenance OPENS the walk and is recorded as `stand_build: not_established` (which
   `first_look._stand_build` already reports), while a stand that does not answer, or a provably other build, still refuses. Without
   this, on MyBooks (scout line "No build identifier was found: unknown"; 15 of 15 walk probe results in the run are `person_confirmed`,
   0 `matched`; the deployed word came at 19:17:25, after the null at 17:23:55) A1's look is still skipped, now as `walk_not_opened`.
2. A1 `_sign_in_faults`: `sign_in.evidence` cites captures through `WS.capture_cited(task_root, walk, <item>, path, quote, stand)` with
   a required `quote`, and the item is derived from the path (`survey-<item>/<attempt>/`) or given as a required `req`. The `""` quote
   of item 2 always refuses.
3. A1 secret guard: structural fields (url, steps, selectors, request path, body field names) are compared with
   `app_card.scrub(v, tokens=False)` against the whitespace-normalised value, and any field holding a literal value of the stand's
   accounts (read in memory through `manual_capture.read_login`/`resolve_actor`, never printed) is refused naming the field. `sign_in`
   records the `actor` it signed in as, never keys or values. Census class `safety`.
4. C1 `_first_look_record_sign_in`: no registry write when every row of the accepted record is `blocked_by: access`; the printed line
   says why.
5. B1 `first_look_lines`: the no-count-cap rule applies only when `s5_kind == "window"`; the plan, legacy and unknown kinds keep
   `FIRST_LOOK_LINES_MAX` and the `+N more` pointer.
6. F-4 → render the story's OWN `first_look.read()["sign_in"]` in that story's S3-S7 and walker briefs (B1 or B2; `no_trace`
   irrelevant), and B2 lists registry ways from other stories only.
7. B1 `FIRST_LOOK_GAP` / B2 `sign_in_lines`: the last clause is chosen per reader. "look yourself with the tools your brief names" only
   for readers whose brief names a stand tool (S5 automator once FV1-29 lands, S6 runner, S7 analyst); "name it as a gap" for S3/S4. No
   line names a script for a role that may have no shell, and B2's cut names the registry file, not `project_knowledge.py show`.
8. C1: add a `SIGN_IN_KEY` branch in `record_problems` BEFORE the role rules, with the positional invariant stated. Put the write in ONE
   function both roads call (for example `first_look.py record-sign-in` / a `project_knowledge` helper) and name it in `phases/s3.md`
   "First look" (axis 5 row `:157`).
9. D1: (a) an `http` way is recorded as an `environment.access`-shaped object (validated by `config_contract.access_errors`) and run
   through FV1-17's `stand_access` road executor (`form_login` covers the csrf two-step), so D1 also waits for FV1-17. (b) A `ui`-only way
   never removes the login layer: the probe line says "login not checked by code; a UI way was recorded by the first look in <story, date>"
   and the verdict stays pending, unless the project's `access.kind: ui_only` (FV1-17) says the tests sign in through the UI.
10. D1: a recorded way that fails live names `PK-n` and the door `project_knowledge.py revoke --id PK-n --words-file <F>` in the probe
    line and in the S0/S5 warning (FR-1, FR-2, FR-40).
11. One precedence order for "how to sign in" (recorded registry way > `environment.access` > factory default), stated once beside
    `project_knowledge.sign_in` and read by D1 and FV1-28e. F-6's "after the project's `manual_capture.login.ui`" goes.
12. F-7: the `first_look/empty` seed becomes the role stub's record with every row `unreachable` / `blocked_by: access` with a capture,
    through `first_look.put`; no role stub calls `put --null`.
13. `docs/SIBLING_MAP.md` axis 5 row «How the stand logs in» (`:127`) names `environments.sign_in` (writer `project_knowledge.record`,
    reader `project_knowledge.sign_in`) in the C1 commit. §5 drops "axis 37" and fixes axis 5 / 6 / 34 as above.
14. §3 states that finding item 2's «`no_stand` только когда роль не смогла дойти» is replaced by role-written `unreachable/access` rows
    (F18), and why.
15. A1 DoD: the behaviour row "pending stand → walk opens → first-look dispatch registered" goes to `test_first_look_step.py` (layer
    scenario). The `sign_in` battery is one parameterised table. C1/B2/D1 drop the per-branch reader rows for one data-join row per
    producer → reader.
16. §0: fix the `driver_stage_plan.py` line refs to origin/main, the "6144 tokens" (bytes), and F6's scope ("not in the repo"; the ARM
    folder holds the briefs).

## §C Questions for the owner (plain words, with a recommendation)

- **Q1.** The second half of the live proof is "the next story on the same stand already knows how to sign in". It cannot be shown by a
  comparison run, because comparison runs leave no record on the stand by design. May one MyBooks story be run in the normal mode (it
  writes only into our own stand's project folder, nothing to Jira or MR)? **Recommendation: yes**, one normal run for that row. The
  comparison runs stay as they are; in them the way in still reaches the later stages of the SAME story (amendment 6).
- Nothing else needs the owner. F-1, F-2, F-3 (with amendment 5), F-5 and F-6 (with 11) are technical, and I agree with the Lead's (A).
  F-4 and F-7 are amended above.

## §D Duplication and consistency / code quality (plan gate)

- Duplication: the plan adds a sixth carrier of "how to sign in" (F11 counts four, plus `app_card` "Sign-in" and the new registry row).
  It is justified only with amendments 6, 9, 11 and 13 (one precedence, one http shape, the new carrier named on its axis row). The B2
  line and the `app_card` "Sign-in" section would render the same fact twice and disagree in one packet: the card shows the config's
  `/login` with empty fields. **B2 must also feed `app_card` "Sign-in" (`app_card.py:185-204`) from `project_knowledge.sign_in`, or B2's
  line goes and the card carries it** (part of amendment 7's card set; the builder names which). Grepped: `Sign-in|login_recipe|NOT_PROVEN`
  in `app_card.py` (4 hits).
- Code quality: no other finding beyond the guard's false-positive and false-negative directions (amendment 3).

## §E Trail

Read: the spec whole; the finding `:1-49`; `first_look.py:294-689`; `brief_pack.py:3940-3965`, `:4010-4284`, `:4325-4429`; `app_card.py:55-99`,
`:343-390` plus Grep; `walk_session.py:560-610`, `:1170-1305`; `manual_capture.py:1579-1626`, `:2940-2956`, `:4870-4884`;
`profile_contract.py:875-918`; `project_knowledge.py:440-779` plus a def list; driver_stage_plan (origin/main) `:184-343` plus its diff
vs read-main; `driver_s0.py:2418-2432` (main); the FV1-5 diff (env_probe, driver_s0, driver_stage_build); `role_load.py:40-69` plus Grep;
`role-load.json` head; `first-look-statuses.json`; `null-outcomes.json` NE37; `judgment-census.json` about plus class counts; test-layers
rows; `SIBLING_MAP.md` headings, axis 5 `:111-157`, axis 6 `:159-180`; `TESTING.md:1-70`; `phases/s3.md` Grep; `report_facts.py` Grep
`knowledge_use`; knowledge plan Grep; OF3 batch rows Grep; the amendment spec `:425-454`; stand-login spec `:36-60`, `:235-241`,
`:389-392`, `:490-496` plus Grep; ARM story `LOCAL-1`: `first-look.yaml`, `pipeline.json` (environment, no_trace), `events.jsonl`
(environment fields), `app-card.md`, briefs (sizes, first-look lines), `stand-confirmations.jsonl`, evidence `result` counts.

Searches with positive controls: `environment_pending` -i over `scripts/*.py` (22 files, no `walk_session.py`; control
`first_look.py` listed); `Axis 3[7-9]` -i (0; control `Axis 3[4-6]` -i = 5); `"place": *"survey"` over the stand (0; control
`"place": *"` = 3+ hits); `"result": *"unknown"` in LOCAL-1 (0; control `"result": *"[a-z_:]*"` = 16 hits: 15 person_confirmed, 1 pass);
`как входит тест` -i in the pile (1, the finding itself).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "N1: walk open on a survey walk refuses an unknown runtime provenance (manual_capture.stand_probe, ACCEPTS without unknown), so on MyBooks the first look is still skipped (walk_not_opened) after A1 - a new card A2 is required (amendment 1)",
    "N3: A1 evidence check calls capture_cited with an empty quote, which always refuses; quote and the item are required (amendment 2)",
    "N2: the A1 secret guard via scrub(tokens=True) != value refuses whitespace and long data-testid values and misses bare passwords (amendment 3)",
    "C1 records a sign_in as a working way when every row is unreachable/access (amendment 4)",
    "D1 single-request http shape cannot express the stand's csrf two-step login, and its ui-only branch turns an unchecked login into a pass (amendment 9)"
  ],
  "class_completeness": "Map walked: axis 5 first-look row (skill road phases/s3.md missing for C1's write), axis 5 'How the stand logs in' row (new carrier not named), axis 6 knowledge_use marker (unqueued), axis 34 (two precedence orders; ui_only vs D1 ui branch). Same-artifact sweep of sign-in readers: env_probe (D1), login_recipe (FV1-28e), briefs (B2), app_card Sign-in section (missing), walk-open runtime probe (missing, amendment 1). Section 5 enumerates a non-existent axis 37 (the map has 36).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-fv1-28-first-look-to-automator-spec.md",
      "plans/piles/live-run-fvf/findings/20261113-pervyj-vzglyad-ne-dohodit-do-avtomatora.md",
      "ai-packages/qa-factory/scripts/first_look.py:294-689",
      "ai-packages/qa-factory/scripts/brief_pack.py:3940-3965,4010-4284,4325-4429",
      "ai-packages/qa-factory/scripts/app_card.py:55-99,343-390",
      "ai-packages/qa-factory/scripts/walk_session.py:560-610,1170-1305",
      "ai-packages/qa-factory/scripts/manual_capture.py:1579-1626,2940-2956,4870-4884",
      "ai-packages/qa-factory/scripts/profile_contract.py:875-918",
      "ai-packages/qa-factory/scripts/project_knowledge.py:440-779",
      "ai-packages/qa-factory/scripts/driver_stage_plan.py (origin/main) :184-343",
      "ai-packages/qa-factory/scripts/role_load.py:40-69",
      "ai-packages/qa-factory/references/first-look-statuses.json, null-outcomes.json NE37, role-load.json",
      "ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json about, test-layers.json rows",
      "git diff origin/main...wip/fv1-5 (env_probe, driver_s0, driver_stage_build)",
      "docs/SIBLING_MAP.md axis headings, axis 5, axis 6",
      "docs/TESTING.md:1-70",
      "docs/tasks/specs/20261113-fv1-17-5-15-stand-login-spec.md:36-60,235-241,389-392,490-496",
      "docs/tasks/specs/20261113-p1-specs-amendment-owner-words.md:425-454",
      "C:/QAFactory/mybooks-stand/arm-factory/test-automation-framework/qa-factory/artifacts/LOCAL-1 (first-look.yaml, pipeline.json, events.jsonl, app-card.md, briefs, stand-confirmations.jsonl, evidence results)"
    ],
    "reruns": [
      {"command": "python events.jsonl environment-field extraction (LOCAL-1)", "result": "S0 done..S2: environment local, environment_pending true"},
      {"command": "grep -o no_trace LOCAL-1/pipeline.json", "result": "\"no_trace\": true"},
      {"command": "grep -rho result LOCAL-1/work/evidence | uniq -c", "result": "15 person_confirmed, 1 pass, 0 matched"},
      {"command": "wc -c LOCAL-1/work/briefs/S5-qa-automator-[1-9].md", "result": "11470..20678 B, total 144794"},
      {"command": "Grep environment_pending -i scripts/*.py", "result": "22 files, walk_session.py absent; control first_look.py present"},
      {"command": "Grep Axis 3[7-9] -i SIBLING_MAP.md", "result": "0; control Axis 3[4-6] = 5"},
      {"command": "worktree scan: git diff --name-only origin/main...HEAD per worktree", "result": "env_probe in wip/fv1-5 and wip/wave13; brief_pack case_concern_lines in wip/fv16-n2; census in wip/tbw-t1r; no other node file"}
    ]
  },
  "fixes": [
    "1 new card A2: survey walk open does not refuse an unknown runtime provenance (walk_session._open_actors / manual_capture.stand_probe caller)",
    "2 A1 sign_in evidence: required quote plus item for capture_cited",
    "3 A1 secret guard: tokens=False on structural fields, whitespace-normalised compare, literal account-value refusal, record the actor; census class safety",
    "4 C1: no registry write when every row is blocked_by access",
    "5 B1: uncapped s5 only for s5_kind window",
    "6 F-4: render the story's own first_look sign_in in its S3-S7 briefs; B2 lists other stories' ways",
    "7 B1/B2 wording per reader; no script named for shell-less roles; B2 also feeds app_card Sign-in",
    "8 C1: SIGN_IN_KEY branch before role rules; one write function shared with phases/s3.md",
    "9 D1: http way as an environment.access-shaped object through FV1-17 stand_access roads; ui-only never a silent pass (defer to access.kind ui_only)",
    "10 D1: failure line names PK-n and the revoke door",
    "11 one precedence order beside project_knowledge.sign_in for D1 and FV1-28e",
    "12 F-7: the empty seed is an all unreachable/access role record via put, no role-stub --null",
    "13 SIBLING_MAP axis 5 'How the stand logs in' row names the new carrier; section 5 drops axis 37, fixes axes 5/6/34",
    "14 section 3 names the deviation from finding item 2",
    "15 tests: scenario row in test_first_look_step.py, one parameterised sign_in table, trim the per-branch reader rows",
    "16 section 0: refresh the driver_stage_plan line refs, bytes not tokens, F6 scope"
  ]
}
```
