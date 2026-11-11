# Critic on plan: plans/project-knowledge-plan.md (project knowledge: ask at first need, remember, never ask again)

Critic (Opus), 10.11.2026. One pass, plan only (no code exists). Facts checked in `D:/ws2/wt-fbfix` (branch checked out
there: `fb-fix`, HEAD `68c20d1c7`, 15 commits after the plan's recon hash `6681ba757`; since then only `story_run.py` (+16/-11) and
`p2-interview.md` (+7, TR3-12's interview topic, commit `09b70f0e7`) changed among the files the plan relies on). PKG =
`D:/ws2/wt-fbfix/ai-packages/qa-factory`.

VERDICT: accept-with-fixes

The direction is right. The owner's intent fits the code better than the plan says: FR-59 already describes "a policy kept in data:
the project's registry, grown by the answers of the person and the roles" (PKG/design/factory-rules.md:289-296). And the code already
has more "ask once, remember" mechanisms than the plan counts. But four load-bearing points of §2 and §4 are wrong or missing. A
designer drafting phases 1-2 from the plan as written would build on them: the registry base (C1), the story-end config revert that
would undo every fact the seam writes into config.json during a story (C2), the code that forces the stand login question at
onboarding (C4), and a second key catalogue next to `config-keys.json`, which already carries most of the planned columns (C5). These
are plan edits, not a redesign. Owner decisions В1 and В3-В6 are feasible on the facts. Below I raise only where a decision needs a
condition, or where two of the owner's wishes meet.

Blocking before a designer drafts phases 1-2: C1, C2, C4 (severity blocker). C5 and C6 should be settled at the same time,
because phase 1 depends on them.

---

## 1. FACTS — the load-bearing claims of §1

| # | Claim (plan line) | Result | Evidence |
|---|---|---|---|
| F1 | Interview bank is prose, `p2-interview.md:81-370`, 19 topics / 43 questions / 6 batches (§1, l.14) | TRUE (range 81-377 now; +7 lines from TR3-12 at :297-303) | PKG/skills/qa-onboarding/phases/p2-interview.md:81 `## The ordered question bank`, :378 `## What is never asked here`; audit 20261030-voprosy-onbordinga-audit.md:6, :25, :32-34 |
| F2 | "a required fact is never skipped or filled with a default" `SKILL.md:41-45` | TRUE | PKG/skills/qa-onboarding/SKILL.md:41-46 |
| F3 | "required = whatever code later complains about" `p2-interview.md:44-54` | TRUE | p2-interview.md:44-54 (table: topics 1, 2, 3, 7, 8 required) |
| F4 | "No notion of 'ask later, when needed'" (l.17) | TRUE for onboarding, with a nuance. Own search for `first need\|when (it is\|first) needed\|ask(ed)? later\|at first use\|on first use\|lazy`, case-insensitive, over PKG: no question-related hit. Positive control from the same search: `dependency_drift.py:8` "create on first use", `gate_registry.py:371` "built on first use". The nuance: DD rows have ripeness triggers (`story_count`, `capability_verified`, `date`) for asking AGAIN, `project_decisions.py:381-385`, `due` :510-518, and only after the person was asked once (SKILL.md:47-50) | as cited |
| F5 | Gate A asks the login keys of every story regardless of need, `gate_preflight.py:3823-3857` | TRUE | `check_s5_credentials` :3827 `login = integration_login_keys(env_cfg)`, :3841 `missing = [... if key not in values]`, :3855 `self.add(check, PERSON_DECIDES, ...)`; no case/plan tie on that branch |
| F6 | Integration keys are asked only when the story is tied to the integration (`_integration_keys`, t-218) | PARTLY TRUE. The rule is "asked unless it says nothing": a row with `applicability: required` or ANY `required_by` is asked, falling back to all of `required_by` when nothing of this story matches (`uses = ... or required_by`). An unreadable case keeps the question. The tie therefore rests on onboarding having recorded `required_by`, or on cases declaring `check.integration` | gate_preflight.py:3947-3951, :3989-3992, :3993-3994, :3995-4008 |
| F7 | Memory #1: environment record, typed key, `accept always` (D-0029, D-0032) | TRUE | environment_record.py:1-23, `lasting` :133-147, `record` :326-348, `covering` :300-315, `revoke` :351-356; DECISIONS.md:42, :45 |
| F8 | Memory #2: `stand-account` / `stand-frontend` write config.json directly | TRUE, but not "directly": they go through `upsert`+`resolve`, i.e. a DD row with the person's words plus a receipt | project_decisions.py:641-646, :782-786 |
| F9 | Memory #3: `records/stand-identity.json`, key stand + profile | TRUE (append-only rows, `forget` appends `withdrawn`) | stand_identity.py:1-30 |
| F10 | Memory #4: `factory-backlog.md` + `records/project-decisions.json` DD-n, matched by `field_refs` | TRUE (markdown is the source, JSON is a projection) | project_decisions.py:1-6, `_paths` :269-271, `_persist` :274-281 |
| F11 | Memory #5: retro lessons as prose (`stand_quirk`, `gate_answer`), S9 `knowledge_fold` | TRUE | PKG/handoffs/s9-retro-to-project.yaml:60-66 |
| F12 | Memory #6: `manual.accounts_way` / `data_way`, t-1957 §3.6-3.7, TR3-10 | TRUE as a design. Not in code: TR3-10 is `ожидает` (batch-3-parallelnost.md:31) | t-1957 spec :443-493 |
| F13 | "A question has no stable key; 'already answered' is a hash of the text (`story_run.py:4387`)" (l.40) | HALF FALSE, see C7. 28 `closed_question` sites carry stable keys of `question-prices.json` (e.g. `s6.stand_login`, `s6.stand_confirm`, `s8.delivery.yes`). The hash claim is true, and the plan misses two facts. (a) The memory is PER STORY: `driver-answers.jsonl` lives in `self.state_dir`, which is `task_root/state` (story_run.py:1068, :4395). (b) A hit does not skip the question: the question is asked again with "You have answered this exact question before" (:4308-4320) | story_run.py:4387-4398 |
| F14 | "Only the stand-gap card has 'this story or for good' (`accept` / `accept always`)" (l.42) | FALSE as a negative: the onboarding approvals log remembers a person's answer per JSON pointer for good, until the template default changes (`remembered_answers`, config_contract.py:1280-1304, its use :1460-1466) | see C3 |
| F15 | Two config readers: `read_config_file` (13 files), `load_config` (~56) plus direct reads (l.43) | TRUE in kind, but they read with OPPOSITE error directions (C16). My count (top-level `scripts/*.py` only, tests excluded): 8 and 43 files; 63 files name `"config.json"`. The plan's 13/56 probably include tests and hooks (not re-derived) | config_contract.py:1084-1109 (raises `ConfigUnreadable`); hooklib.py:792-796 (`{}` on broken) |
| F16 | "Nothing pairs a code-read key with a template row and an interview question" (l.44) | TRUE as the recorded gap. architecture.md:65 says so verbatim, and :235 for the reader side. No test pairs reader -> template row: own grep over `scripts/tests/*.py` for `config-keys\|config_keys()` found 9 files, all about the migration/fill/view/readiness, none walks code reads. But `config-keys.json` DOES pair a key with its interview-ish question for `asked_until_answered` (see C4/C5) | as cited |
| F17 | `project_decisions.py:1-17` header | TRUE | |
| F18 | Phase 2.2: "B-296: the registry cannot point into a list element" | STALE, see C12. `_set_pointer` steps through a list index inside its length since HF8-9 | project_decisions.py:349-374, used at :641 |
| F19 | Phase 4.2: "the code already exists: `project_inventory.py`, `propose_access`, `onboarding_probe.py`" | TRUE | `def propose_access` in PKG/scripts/project_inventory.py; onboarding_probe.py exists |
| F20 | `install-paths.json` class "carried" exists for `knowledge.json` | TRUE (class `carried`) | PKG/references/install-paths.json `description` |
| F21 | `question-prices.json`, `person-owned.json` classes, `inject-map.json` exist with the shapes the plan uses | TRUE (`questions`; `classes` incl. `access`, `outbound`, `team_agreement`; `slices/common/kinds/roles`) | PKG/references/*.json |
| F22 | "~120 places" to change without one reader (l.81) | UNVERIFIED. Not re-counted; the 63 files that name `"config.json"` make it plausible | |
| F23 | "six keys nobody reads" (l.15, l.199) | UNVERIFIED by me. Taken from the audit (:25), which carries file:line readers; not re-grepped | |

New project files do not exist yet, as expected: `ls PKG/references | grep -i knowledge` and `ls PKG/scripts | grep -i knowledge` are
empty; the same listing showed `project_inventory.py` and `onboarding_probe.py` (positive control).

## 2. FEASIBILITY of §2

**Can one `need(key, env, story)` sit in front of every asker?** Only if it is split in two (C9). The askers are different shapes:

- **Gate A cards** are not questions. They are findings added by a CHECK script (`gate_preflight`, run as a subprocess; e.g.
  `self.add(check, PERSON_DECIDES, ...)` at gate_preflight.py:3818-3822 and :3855-3857), batched into ONE gate packet the person
  answers in one go. A `need()` that marks `asked` in a registry from inside the check makes the check a writer (FR-45 "a validator
  writes nothing", factory-rules.md:472). It also cannot "ask" per key without breaking the single packet. What fits: a pure
  `state(key, env)` for checks; `asked` / `answered` written by the driver when the packet is shown and answered.
- **Driver questions** (`Person` -> `ask` -> `take_answer`; `closed_question(key, ...)` story_run.py:4612-4615): fit, but the
  question key is a SITE key. One site asks several facts (the login packet asks user key + secret keys + extra keys). The seam needs
  a site-key <-> fact-key(s) map, not "question key = fact key".
- **Deferred questions** (`defer_question`, `deferred_step`): the plan's step 4 ("put to the nearest stop, holds no case") does not
  exist. `deferrable` is False when the question holds no case (story_run.py:4457-4459). `holds_can_wait` reads the S6 scope
  (:4469-4472). A deferred question is asked only at gate B entry (:4522-4556). t-1957 §3.6 step 3 plans a flag for this (spec
  :462-464), but it is TR3-10, not landed. A fact first needed at S1/S3 (`product.roles`, accounts per role for planning) cannot wait
  for gate B: by then the plan is made without it (C8).
- **Stand-gap cards** (`accept` / `accept always` -> `environment_record`): fit, as the "for this stand" scope.
- **Onboarding interview** (a role in chat): the role cannot call a Python seam turn by turn. The answers land through
  `config_contract` approvals (`record_approval` -> `onboarding-approvals.jsonl`; `apply_plan` -> `_write_config`,
  config_contract.py:1922-1925, :1460-1466). That is a third answer store with its own memory. The plan does not say whether
  onboarding answers become registry rows (provenance `onboarding`) or whether the approvals log stays a source of `state()` (C3, C9).

**Where the single order (value -> derive -> registry -> question -> while_unknown) does not fit:**

1. Derive before registry runs a probe (possibly expensive, or the one that produced `unreachable`) even when the person said
   `not_needed`, and re-runs a probe whose `unreachable` is a standing decision for this run (D-0043). Order: value -> registry
   standing state (`not_needed`, run-scoped `unreachable`) -> derive -> open row (`asked`: do not ask again) -> question ->
   `while_unknown`.
2. Gate A: see above. A check reads `state()`, it never asks.
3. Stand selection: `environment_selection.select_environment` already auto-selects a confirmed `default: true` stand or the only one
   (environment_selection.py:10-13), and returns `unknown` for a name not in the config (:6-7). §3.4 "asked in every story" and "a
   new stand creates a card" both change this function (C17).
4. Login at S5 vs S6: S6 `stand_login_gate` is already need-gated by case policy `ui` (story_run.py:12894-12904). Gate A's S5 check
   is not. Two askers of one fact (AR-19 twin), C11.

**Is `project_decisions` a sound base for a per-key / per-environment registry with list elements, provenance and revoke?** Not as
it is. The plan's 2.1 ("upsert / resolve are generalised: a row per key + environment") underestimates it (C1):

- identity by a JSON pointer with a list INDEX: `/environments/{index}/credentials_by_role/<role>` (:641),
  `/environments/{index}/frontend/url` (:737). Every other stand record keys by stand NAME: `environment_record` subject field
  `environment` (:129), `stand_identity.definition_sha_for(cfg, name)` (stand_identity.py:149-154). Reordering or inserting a stand
  silently re-targets an old DD row;
- `upsert` returns an existing row only when it is OPEN (:398-400). After `resolve` closes it, the same refs make a new DD row. No
  function answers "was this key answered, when, in whose words";
- states are only `open` / `closed` (:404, :488): no `asked`, `not_needed`, `unreachable`, `revoked`;
- no revoke for DD rows. Only the environment record and stand identity have a take-back (environment_record.py:351-356,
  stand_identity `forget`);
- the source of truth is a markdown table in the project's `factory-backlog.md`, one line per row with cells collapsed
  (:158-161, :173-189). The JSON is a regenerated projection (:274-281). Per-element provenance of growing lists does not fit a
  one-line cell;
- `_set_pointer` creates objects but never a list element (:365-367). A NEW stand, or a fourth regulator in a list, cannot be
  written;
- `_stand_of` refuses when there is no `environments[]` row, with the door "Record it first (/qa-factory:qa-onboarding, topic 2)"
  (:538-540). That contradicts the owner's word that stands are not asked at onboarding.

A sounder base already exists in the package: the generic record helpers `environment_record.load_rows` / `write_rows` / `next_id` /
`revoke_row` (:208-272). They are already shared by the gap-class record (their docstring, :212-213): JSON, schema-versioned, an
unreadable file covers nothing and is never written over, and revoke keeps the row. `project_decisions` would then stay the writer
of config values (receipt, story-revert safety, C2), and the knowledge registry would be a record of this family.

## 3. ARCHITECTURE

- **AR-29 / P27.** Kept on paper: free words go to the conductor (§2.4), a growing list is never closed by code (§2.6). One gap: a
  role's OBSERVATION becomes a project-wide fact (`knowledge.json` element "по наблюдению роли", §2.6 l.146 and l.138) that then
  steers every later story. A role's inference is not a project fact (P20 says this for code; the same holds for a role's guess
  about the project) — C13.
- **AR-14, one writer of config.json.** It is already plural in code: `config_contract._write_config` (:1925, "the ONE writer",
  onboard_apply.py:1765), `project_decisions.resolve` writes config.json itself (:477-478), and `runtime_probe.py --suggest --write`
  writes it itself (runtime_probe.py:1489). `config-keys.json` `written_by` lists REGENERATED writers (`runtime_probe.py`,
  `ticket_adapter.py`). "The writer of facts is one — the seam" (phase 2 l.227) must name which of these stay (C18). Also the story
  revert decides which writes survive: C2.
- **AR-13, one reader.** The plan adds a reader. It must declare its error direction, because the two readers it unifies have
  opposite ones (C16).
- **AR-28 / FR-59, `while_unknown`, value by value:**
  - `default: <value>`: legal only as a DECLARED SAFE default (FR-59 "takes the safe default it declares"). The plan puts no
    direction constraint on it. A good model in code: `safe_to_break` unknown -> `no` (manual_capture.py:4272-4282). Needs a
    catalogue rule (C10).
  - `gap`: fine if it reaches the report under its owner (AR-27) and only where it changes what is left to the person (D-0047 (2)).
  - `in_turn`: undefined ("обходной путь"). As written, it can be read as "go on". C10.
  - `hold`: fine (holds named cases only).
  - States `not_needed` and `unreachable`: `unreachable` stored project-wide contradicts D-0043's scope ("covers every instance of
    that class until the end of the run", DECISIONS.md:56) and FR-50 (try every route): a VPN missing today would silence the
    probe forever. C10.
- **FR-7.** The registry check by key is an improvement over the per-story body hash (F13). It should state that "answered" means
  "not asked again" across stories, while within a question site FR-7's "comes back changed" (story_run.py:4308-4320) stays.
- **D-0047.** Step 3 voices "acting on your answer of <date>". At the 10th story that is potentially dozens of lines. D-0047 (2)
  limits the REPORT mention to where it changes what is left to the person. The plan should limit the voiced line the same way (one
  summary line per packet, not one per fact) — see §6.
- **FR-12 / AR-1, the two-layer catalogue: one mechanism or two?** One mechanism, if (a) one reader merges both row sources with one
  row schema, (b) one writer, (c) one registry, (d) the plan says plainly that project rows have NO question path of their own. AR-16
  makes every question a `question-prices.json` key (architecture.md:187), and a project-created row cannot add one. So questions
  about project keys exist only as conductor free text, and project keys are add-only facts delivered to roles. Without (d) a
  designer will try to give project rows `ask_when: first_need`, which the question form cannot carry (C20). The real duplication is
  elsewhere: the package layer becomes TWO tables, the new `project-knowledge.json` plus `config-keys.json` (C5).

## 4. COMPLETENESS BY CLASS — "ask once and remember" siblings

Missing from the §1 table (each persists a person's answer or a learned project fact across stories or across questions):

1. **Onboarding approvals memory.** `remembered_answers` (config_contract.py:1280-1304) fills open `required`/`reasked` rows from
   earlier approvals, keyed by JSON pointer, forgotten when the template default moves (:1460-1466). This is the precedent for
   "stable key = pointer" and for answer invalidation.
2. **`asked_until_answered`** in `config-keys.json` (`environment.access`, with its question text). `migration_plan` adds a
   `reasked` row and `apply_plan` refuses until it is answered (config_contract.py:1449-1456, :1712-1726). A per-key "ask"
   declaration already exists in data.
3. **Report adaptations.** `records/report-adaptations.json`, rows `RA-n`, `forget`: the conductor's learned way to read a
   project's report, kept so the problem does not recur (report_adapt.py:1-26, :39).
4. **`waiver.py --carry-from`** carries a person's words (S0-S2 and a class's words, plus `work/gap-classes.json` rows) from one
   story key to another (docs/SIBLING_MAP.md:141).
5. **`obligations.md`**, the "single carrier between stories" with per-row triggers (s9-retro-to-project.yaml:8-10, :51-57). Also
   the knowledge documents `faq.md`, `glossary.md` (`term`) and `project-profile.md` (:63-64). The plan lists `knowledge_fold` but
   not these carriers or `term`.
6. **Confirmed default stand.** `environments[].default: true` is a remembered "test on this one" (environment_selection.py:10-13).
7. Within-story class memory, `work/gap-classes.json` (`source_inventory.live_gap_classes`, :2834-2845): per story, not
   cross-story. Listed so the "only this story" scope (§2.4) names it alongside `pipeline.json` waivers.

Story side, asking about a fact regardless of need, not in phase 3:

- `asked_until_answered: environment.access` and `project_fact: true` on `environment` / `environments` (`not_filled`,
  config_contract.py:1350-1369). These are onboarding-side, and C4 covers them.
- Gate A's `check_s5_credentials` env-file check (:3817-3822): asks to create the env file whether or not any case needs a
  credential. Same class as 3.1.
- S0 halts on `readiness.py --require ticket_adapter,test_repo,vcs,config_schema` (skills/qa-story/phases/s0.md:21).
  `config_schema` counts the `absent_means: required` template keys (readiness.py:907-930). Whatever phase 4 moves to `first_need`
  must stop being `required` there, or S0 halts on it.

No `docs/SIBLING_MAP.md` axis names "a person's answer kept across stories". My grep of the map (case-insensitive, for
`environment-properties|environment_record|remembered_answers|report-adaptations|stand-identity|project_decisions`) hit only the
person-words carriers (:141), the markdown cell grammar (:413) and the profile shape axis (:459). The new survivor needs its axis in
the commit that creates it (AR-15). This plan is that place.

## 5. ORDER AND SLICING

- The order 1 -> 2 -> 3||4 -> 5 -> 6 is right in principle. Two problems:
  - Phase 1.1's mapping `absent_means: required -> onboarding` gives 20 onboarding rows (measured: `config-keys.json` keys
    Counter `{'default': 47, 'required': 20, ...}`), while §2.1's ratchet says <= 10. Phase 1 is either red or carries throwaway
    values. C6.
  - The phase 3 || phase 4 parallel shares hot files: 3.1/3.4 `story_run.py` and `gate_preflight.py`; 4.x `config_contract.py`
    (the `not_filled`/`asked_until_answered` change of C4) plus readiness, which `config_schema` at S0 reads. They need `очередь:`
    lines, or disjoint function lists (D-0048).
- **A smaller first slice exists and should come first.** One fact end to end, before ~68 top-level keys (101 template entries with
  notes) are catalogued. Candidate: `environments[<name>].accounts_by_role` or gate A's login keys. One catalogue row -> `state()` ->
  the driver asks via a keyed `closed_question` -> the registry row (name-keyed, provenance) -> the value survives
  `restore_config` (C2) -> a second story does not ask, and voices it -> revoke -> asked again. That proves C1, C2, C8 and C9 on
  one fact. Phase 1.1 "all keys" and 1.4 "all reads" (43+ files) are then mechanical follow-ups, not prerequisites.
- **Under-specified to the point a designer cannot draft nodes:**
  - Phase 2: the registry schema (C1); what "nearest stop" means per stage (C8); the read/write split of `need()` (C9); whether
    onboarding answers enter the registry (C9).
  - Phase 3.6: depends on В1, fine.
  - Phase 5.2: "spec t-636 — сюда", no content.
  - Phase 6.1: which `stand_quirk` / `gate_answer` rows have a "known key", and who decides it (it is a role's judgment, AR-29).
- **Collisions.**
  - TR3-10 is `ожидает`, depending on TR3-9 -> TR3-6 (batch-3-parallelnost.md:27, :30-31), so В4's branch "wait for phase 2" applies.
    Batch 3 then cannot close until phase 2 lands. Say so in batch 3 (`очередь:` and a `перенос:` per pile rules), and name the
    owner-visible cost: the third walker's accounts flow waits for this pile.
  - TR3-12 is `сдано`, not `принято`, and its topic sits in p2-interview.md:297-303. В5 removes it, which is fine. It is a node of
    a batch under work, so its removal is a line in that batch, not in the new pile.
  - onboarding-forge batch 1 OH1-6 writes `hooklib.py` / `gate_preflight.py` (batch-1:23) and OH3-35 writes `config-keys.json`,
    templates, `config_contract.py`, `onboard_apply.py` (batch-1:27). Phase 1 "absorbs" OH1-6, and phase 4 absorbs OH3-35 whole.
    Both batches are `ожидает`, `взял: —`, so absorbing is legal; the `перенос:` rows must be written in those batches in the same
    move. OH3-35's own target is "<= 3 answers" (batch-1:27) against the plan's 5+1. The owner's 10.11 word supersedes it, so record
    that in OH3-35's row.

## 6. RISKS the plan does not name

1. **Story-end config revert** (C2). The seam's config writes vanish at story end unless the seam is a recorded writer. The revert
   is also skipped when another story ran in the window (config_contract.py:2250-2257): parallel stories.
2. **Migration of existing projects.** The values already in config.json have no provenance. Phase 1 needs a state such as
   `known (source: legacy config)` and must not re-ask them. Existing DD rows with index pointers, environment records keyed by
   stand name, and approvals-log memory must map onto the new registry, or be read by it as they are. Not named.
3. **Comparison runs and no_trace.** Arms run on project copies with the same answers (P8, PROJECT.md "Прогоны и эксперименты").
   Cross-story memory means an arm's second story asks less because of the first. A second arm started from a copy taken after the
   first ran inherits its answers. `no_trace` today guards external writes only: own grep, `no_trace` appears in
   `controller.py, external_writes.py, no_move.py, readiness.py, refusal_registry.py, stage_done.py, story_run.py`, none of the
   record writers. Plan: a knowledge snapshot per arm, plus a "questions avoided by memory" column in the comparison (C14).
4. **A wrong project-wide answer silently steering later stories.** Revoke exists. But detection depends on the person reading a
   voiced line, and D-0047 accepts silence as consent. A role-observed element (C13) or a dirigent-classified scope "проект, всегда"
   from free words (В3) can be wrong with no person ever having said it. Needs provenance shown to roles and a narrow default
   (В3 already says narrow on doubt).
5. **Question volume moves to the first stories.** With ~15+ `first_need` facts, story 1 may ask more than onboarding used to, spread
   over stops. Phase 6.2 measures it but sets no budget. Batching rule needed: one packet per stop, all due facts at once.
6. **Cost of the seam on every stage.** `need()`/`state()` reading config + card + registry (+ project layer) on every gate check,
   brief and driver step. Cheap per call, but on hook paths (`load_config` is a hook-path reader) it adds file reads per tool call.
   State which callers may use it from a hook (or none).
7. **D-0043 scope drift.** `unreachable` persisted beyond a run (C10).
8. **TypeScript-style projects and `dispatch.parallel_windows`.** В5 (accepted) drops the question. The fact ("does the build compile
   the whole test folder") is derivable at discovery (tsconfig / a Java build). Give it a `derive` in the catalogue, or a known bad
   default runs three windows that break each other.

---

## Findings

**C1 — blocker — §2.2 (registry), §4 phase 2.1, §6 "решила сама: реестр — существующий project_decisions".**
Evidence: index-pointer identity project_decisions.py:641, :737 vs name identity environment_record.py:129,
stand_identity.py:149-154; open-only match :398-400; states open/closed only :404, :488; no DD revoke (revoke exists only at
environment_record.py:351-356); markdown source with one-line cells :158-161, :173-189, :274-281; no list append :365-367;
`_stand_of` door to onboarding :538-540.
Change asked: phase 2 states the registry schema before any node. Subject = (fact key, environment NAME or `project`, element id for
list facts). States `known/asked/not_needed/unreachable(run-scoped)/revoked`. Provenance (who, words, story, when, source:
person/probe/role/legacy). Revoke. Append of a list element and of a new stand. Name the base: recommended, a JSON record of the
`environment_record.load_rows/write_rows/revoke_row` family (:208-272), with `project_decisions` kept as the config-value writer
(receipt and revert safety, C2). Rewrite the `_stand_of` door. Move the "решила сама" line to this decision.

**C2 — blocker — §2.2, §2.4 row "проект, всегда -> config.json", phase 2/3.**
Evidence: `restore_config` gives config.json back at story end except writes by a recorded writer, config_contract.py:2264-2275.
Recorded writers are onboarding approvals, report adaptations and project-decision receipts, `recorded_writes` :2116-2154. The revert
is skipped when another story ran in the window, :2250-2257.
Change asked: the plan states that every fact the seam writes into config.json goes through a recorded writer (the
`project_decisions.resolve` receipt path, :465-478) or registers a new one in `recorded_writes`, with a test: "a fact recorded during
story T survives `restore_config(T)`, and story T+1 does not ask it". Writes into the environment card or `knowledge.json` are outside
the revert; say so.

**C3 — should-fix — §1 table ("пять раз, пятью способами"), Q4.**
Evidence: config_contract.py:1280-1304 and :1460-1466 (approvals memory); config-keys.json `asked_until_answered`;
report_adapt.py:1-26, :39 (RA-n); SIBLING_MAP.md:141 (`waiver.py --carry-from`); s9-retro-to-project.yaml:8-10, :51-57, :63-64
(obligations.md, faq/glossary/project-profile, `term`); environment_selection.py:10-13 (confirmed default).
Change asked: add these rows to the §1 table, and for each say: absorbed by phase N / stays because <reason> / queued. Add a
SIBLING_MAP axis "a person's answer or learned project fact kept across stories" naming every member, in the commit that creates
the survivor.

**C4 — blocker — §3 (start set without stands and login, owner-decided), phase 4.**
Evidence: config-keys.json `asked_until_answered: {"environment.access": {...question...}}`; config_contract.py:1449-1456 and
:1712-1726: `apply_plan` refuses until answered. `environment`, `environments` are `project_fact: true` and
`absent_means: required` in config-keys.json; `not_filled` lists them for the person (config_contract.py:1350-1369). `config_schema`
at S0 counts required keys (readiness.py:907-930; s0.md:21). `_stand_of` door, project_decisions.py:538-540.
Change asked: phase 4 lists these carriers and their tests (`test_config_migration.py`, `test_config_fill.py`,
`test_readiness.py`): remove `environment.access` from `asked_until_answered`; make `environment`/`environments` not `project_fact`
for the interview and not `required` for `config_schema` (their template default is the "no stand yet" world). State the behaviour
for BOTH worlds: a project onboarded before (holds stands; nothing re-asked) and a new one (no stand until the first story).

**C5 — should-fix — §2.1, §6 "каталог — новая таблица, config-keys.json остаётся таблицей миграций, их связывает тест".**
Evidence: config-keys.json already carries per key `since`, `absent_means`, `project_fact`, `asked_until_answered.question`,
`written_by` (writer class), `removed` (dead keys with reasons), `value_migrations` (top-level keys listed by
`python -c json.load(...)`). It is read by `migration_plan` and `readiness` (its `about` field).
Change asked: one table per key set (AR-13: one fact, one reader). Either extend `config-keys.json` into the catalogue (add `about`,
`ask_when`, `derive`, `while_unknown`, `needed_by`, `question`, `person_class`; key rows for record-held facts), or make
`project-knowledge.json` the one table and fold config-keys' columns into it, with `config_contract.config_keys()` reading through it.
A sync test between two hand-kept tables is the duplication this plan exists to remove.

**C6 — should-fix — §4 phase 1.1 vs §2.1 ratchet.**
Evidence: 20 `required` keys (measured Counter above), and the ratchet "onboarding rows <= 10" (plan l.68).
Change asked: phase 1 rows carry `ask_when: as_today` (or similar, explicitly transitional). The <= 10 ratchet is born in phase 4
and named there. Or phase 1 classifies for real and is not "pure refactoring". Pick one in the plan.

**C7 — should-fix — §1 l.40 ("у вопроса нет постоянного ключа"), §2.3 step 4, phase 2.3.**
Evidence: 28 keyed `closed_question` sites (`grep -on 'closed_question("[A-Za-z0-9_.-]*"' story_run.py`, e.g. `s6.stand_login`,
`s6.stand_confirm`, `s0.ticket_incomplete`); `already_answered` reads the per-story `state_dir` (story_run.py:1068, :4395) and on a
hit still asks, adding the earlier answer (:4308-4320).
Change asked: restate. Question SITES have stable keys. The answer memory is per story, keyed by body hash, and re-asks by design
(FR-7). Phase 2.3 adds a site-key -> fact-key(s) map (one site can ask several facts: the login packet). "Question key = fact key"
holds only for single-fact sites.

**C8 — should-fix — §2.3 step 4 ("к ближайшей остановке ... не держит кейсы"), phase 2.**
Evidence: story_run.py:4457-4459 (`deferrable` False with no holds), :4469-4472 (S6 scope), :4522-4556 (asked only at gate B entry);
t-1957 :462-464 (the planned flag, TR3-10 not landed).
Change asked: phase 2 gets an explicit node, "a question that holds no case waits for the next stop of ANY stage". The node names the
stops per stage (S1 review, gate A, gate B, ...) and what happens when the fact is first needed at S3 (plan without it +
`while_unknown` + re-plan on answer, or ask at once because the plan depends on it). TR3-10 then builds on it (В4).

**C9 — should-fix — §2.3 (one seam, one order), phase 2.1, phase 3.1, phase 4.1.**
Evidence: gate A cards are added by a check (gate_preflight.py:3818-3822, :3855-3857); FR-45 (factory-rules.md:472); onboarding
answers land via approvals/`_write_config` (config_contract.py:1460-1466, :1922-1925).
Change asked: split the seam into a pure `state(key, env)` (checks, briefs, hooks: no writes) and the driver-side `ask/record`
(writes `asked` when a packet is shown, `known` when answered). Reorder to value -> standing registry state -> derive -> open row ->
question -> `while_unknown` (§2 above). Say whether onboarding answers write registry rows with provenance `onboarding`, or the
approvals log is read by `state()` as a legacy source.

**C10 — should-fix — §2.1 `while_unknown`, §2.2 states.**
Evidence: FR-59 "safe default it declares" (factory-rules.md:289-296); the safe-default model at manual_capture.py:4272-4282; D-0043
"until the end of the run" (DECISIONS.md:56).
Change asked: (a) a catalogue rule plus test: a `default` on a key any gate or refusal reads declares its direction (`safe: ...`),
and a default that would let a gate pass on an unknown is refused by the catalogue test. (b) Define `in_turn` as "the named safe
alternative of this row" or drop it. (c) `unreachable` is run-scoped (re-probed each story), not a project fact. (d) `not_needed`
is a standing decision voiced per D-0047, revocable.

**C11 — should-fix — phase 3.1 ("зеркало `_integration_keys`").**
Evidence: the tie in `_integration_keys` is `required`/`required_by` in config or `check.integration` in cases, and unreadable cases
keep the question (gate_preflight.py:3983-4008, :3993-3994). S6 `stand_login_gate` is need-gated by `manual_policy` ui
(story_run.py:12894-12904). Nothing declares that an S5 automated test needs the login.
Change asked: 3.1 names the tie for login (case preconditions `stand_account` / a ui policy / the automate rows' profile needing
sign-in — which field, produced by whom), the unknown direction (unreadable -> ask, AR-28), and merges the S5 gate-A login card with
S6 `stand_login_gate` as one fact asked once (AR-19 twin).

**C12 — should-fix — phase 2.2 ("B-296: реестр умеет указатель на элемент списка").**
Evidence: project_decisions.py:349-374 (`_LIST_INDEX`, HF8-9) and :641 (writes `/environments/{index}/...` today). BACKLOG.md:245
(B-296 text predates HF8-9).
Change asked: rewrite 2.2 as "append of a list element, and name-keyed subjects" (C1). Close or re-word B-296 in the same move.

**C13 — should-fix — §2.6 ("роль это замечает и добавляет через шов"; "дирижёр — по словам человека или по наблюдению роли").**
Evidence: AR-29 (architecture.md:134-140) and P20/P27: an inference is not a fact. A project row steers every later story's plan.
Change asked: an element or a project key added from a role's observation is stored with provenance `role_observed`, shown to roles
as a hint, and becomes `known` only on a person's word. QUESTION FOR THE OWNER (two wishes meet: "the factory accumulates on its
own, few questions" vs "a project-wide rule only from the person"): is a voiced line "добавила в регуляторы проекта: X; отменить —
словом" plus the person's silence enough to make it a project fact (as D-0047 accepts silence for a decision the person made), or
must the person confirm?

**C14 — should-fix — §4 phase 6, Q6 risk.**
Evidence: `no_trace` appears only in controller/external_writes/no_move/readiness/refusal_registry/stage_done/story_run (own grep),
none of the record writers. P8 and comparison runs on copies (PROJECT.md "Прогоны и эксперименты").
Change asked: a line in §4 (phase 2 or 6): comparison arms start from the same knowledge snapshot, a story's knowledge writes in an
experiment copy are kept per arm, and the comparison reports "questions avoided by memory". Otherwise the 6.3 proof "three stories,
falling question count" is confounded.

**C15 — should-fix — §4 order and slicing.**
Evidence: `config-keys.json` 68 keys and the template 101 top-level entries (measured); phase 1.4 touches `hooklib.py`/
`gate_preflight.py`, which OH1-6 also owns (onboarding-forge batch-1:23); `story_run.py` is queued TR3-2 -> ... -> TR3-10
(batch-3-parallelnost.md:8).
Change asked: a phase 0 (or 2a) "one fact end to end" as in §5 above, before 1.1 "all keys". `очередь:` / `перенос:` lines written in
onboarding-forge batch 1 (OH1-6, OH3-35, OH3-42), batch 2 (OH1-7, OH3-2, OH3-17) and thinking-roles batch 3 (TR3-10, TR3-12) in the
same move the pile is created.

**C16 — note — §4 phase 1.2 ("читает через `config_contract.read_config_file`").**
Evidence: `read_config_file` raises `ConfigUnreadable` (config_contract.py:1094-1108); `load_config` returns `{}` on a broken file
for hooks' no-op contract (hooklib.py:792-796).
Change asked: the one reader exposes both directions explicitly (strict for gates and onboarding, `{}` + a stated "unreadable" for
hooks). Phase 1.4 states per caller class which it takes, so "pure refactoring" stays true.

**C17 — note — §3.1 / phase 3.4 (stand asked in every story).**
Evidence: `select_environment` auto-selects a confirmed default or the only stand (environment_selection.py:10-13) and refuses an
unknown name (:6-7).
Change asked: QUESTION FOR THE OWNER (her two wishes meet: "at each story we confirm which stand" vs "by the 10th story almost no
questions"): per story, is the stand a QUESTION with known stands as options, or a VOICED default ("тестирую на dev, как в прошлый
раз; другой стенд — словом") that becomes a question only for a new story type or when nothing is known? Either way 3.4 names the
`select_environment` change for a new stand name.

**C18 — note — §2.2, phase 2 "писатель фактов один — шов", AR-3, AR-14.**
Evidence: config writers `config_contract._write_config` (:1925), `project_decisions.resolve` (:477-478), `runtime_probe.py:1489`;
`config-keys.json` `written_by`; AR-3 invariant "a project's facts live in its config ... and onboarding asks for it"
(architecture.md:63).
Change asked: list which config writers stay (approvals, adaptation, REGENERATED) and which become the seam. Add
`artifact-writers.json` rows for `knowledge.json` and the registry (AR-14 change check). Move AR-3's text change to the phase that
first stores a project fact outside config.json (phase 2.6 / 3.6), not phase 4 only.

**C19 — note — §2 carriers.**
Evidence: FR-59 already requires "a policy kept in data — the project's registry, grown by the answers of the person and the roles"
(factory-rules.md:289-296).
Change asked: cite FR-59 as the rule this pile implements. The registry is then FR-59's carrier, not a new invention, and the critic
of each node can test against it.

**C20 — note — §2.6 two-layer catalogue.**
Evidence: AR-16 change check "a new question is a `question-prices.json` key" (architecture.md:187).
Change asked: state that project-created keys have no question path (no `ask_when: first_need`, no closed question): they are
add-only facts delivered to roles by `needed_by`, and a question about them is the conductor's free text. That keeps one mechanism
with two row sources, not two mechanisms.

## Owner decisions В1, В3-В6 — feasibility only (not re-litigated)

- В1 (one reader first, the file move later as node 3.6): feasible. `definition_sha` hashes only `base_url`/`frontend_url`/device
  fields (stand_identity.py:129-146), so adding card fields does not void stored stand decisions. 3.6 must re-home
  `definition_sha_for` (:149-154) to the new reader.
- В3 (the conductor decides the scope of a free answer, narrow on doubt): feasible; C13 is the adjacent open question.
- В4 (TR3-10 waits for phase 2 if not started): TR3-10 is `ожидает` (batch-3:31), so "wait" applies; cost noted in §5.
- В5 (drop the TR3-12 topic, default 3): feasible; §6 risk 8 asks for a `derive`.
- В6 (DoD -> `automation.selection`, risk areas -> S4 brief): feasible as the §2.5 recipe; `dod` is `project_fact: true` today
  (config-keys.json), so its removal is part of C4's config-keys edit.

## Facts checked (summary)

F1-F21 in the table of §1: 13 TRUE, 4 PARTLY TRUE / STALE (F6, F8, F13, F18), 1 FALSE (F14), 2 UNVERIFIED (F22, F23). Plus:
`restore_config` / `recorded_writes` behaviour (TRUE, C2); `asked_until_answered` refuses `apply_plan` (TRUE, C4); deferral only at
gate B and S6-scoped (TRUE, C8); `select_environment` auto-select (TRUE, C17); `safe_to_break` safe default (TRUE, C10); D-0043 run
scope (TRUE, C10); config writers >= 3 (TRUE, C18); B-296 still open in BACKLOG.md:245 while the code moved (TRUE, C12).

## TRAIL

Read (whole or the cited ranges), all in `D:/ws2/wt-fbfix` unless marked:
- `D:/ws2/yml-text-factory/plans/project-knowledge-plan.md` (whole)
- PKG/scripts/gate_preflight.py 909-931, 3780-4040
- PKG/scripts/environment_record.py (whole)
- PKG/scripts/project_decisions.py (whole, 928 lines)
- PKG/scripts/config_contract.py 600-700, 1075-1135, 1225-1470, 1700-1735, 2100-2160, 2250-2300
- PKG/scripts/hooklib.py 785-824
- PKG/scripts/story_run.py 4270-4670, 10740-10820, 12880-12950
- PKG/scripts/stand_identity.py 1-30, 129-172
- PKG/scripts/manual_capture.py 4272-4291
- PKG/scripts/environment_selection.py 1-20
- PKG/scripts/report_adapt.py 1-26
- PKG/scripts/readiness.py (def/require index)
- PKG/references/config-keys.json (sections `about`, `since_basis`, `reasked`, `asked_until_answered`, `written_by`, `removed`, key
  counts), templates/config.json (top-level keys), question-prices.json, person-owned.json, inject-map.json, install-paths.json
  (top-level shape)
- PKG/skills/qa-onboarding/SKILL.md 38-48; phases/p2-interview.md 40-56 and headings; diff 6681ba757..HEAD
- PKG/handoffs/s9-retro-to-project.yaml (whole)
- PKG/design/architecture.md 56-280; PKG/design/factory-rules.md 146-152, 289-296, 472-478
- DECISIONS.md lines 42, 45, 56, 60-62
- docs/tasks/specs/t-1957-fast-manual-walker.md 234-255, 443-494 and heading index
- plans/piles/thinking-roles/batch-3-parallelnost.md (whole)
- plans/piles/onboarding-forge/batch-1 and batch-2 (header lines and rows OH1-6, OH3-35, OH3-42, OH1-7, OH3-2, OH3-17)
- docs/tasks/specs/reviews/20261030-voprosy-onbordinga-audit.md (grep for the counts)
- plans/BACKLOG.md rows B-092, B-145, B-220, B-294, B-296
- docs/SIBLING_MAP.md lines 141, 413, 459

Searches run (Grep tool case-insensitive unless noted; each negative with a positive control of the same form):
- `first need|when (it is|first) needed|ask(ed)? later|at first use|on first use|lazy` over PKG: no question-related hit; positive
  hits `dependency_drift.py:8`, `gate_registry.py:371` (F4)
- `grep -on 'closed_question("[A-Za-z0-9_.-]*"'` story_run.py: 28 keyed sites. An earlier Grep-tool form
  `closed_question\("[a-z0-9_]+"` returned nothing because the keys hold dots: a miscall, not absence, corrected by the shell form (F13)
- `asked_until_answered|written_by"|reasked` over scripts/*.py (C4, C5)
- `atomic_json\(.*config|config_path.*write_text|_atomic\(config_path|write_config|def restore_config|suggest.*write` over scripts
  (C18)
- `_write_config|atomic|write_text` in runtime_probe.py: `path.write_text` at :1489 (C18)
- file counts: `read_config_file` 8, `load_config(` 43, `"config.json"` 63 (top-level scripts/*.py) (F15)
- record names `records/...` and `.record(..., "<name>")` over scripts/*.py (C3)
- `no_trace` file list over scripts/*.py (C14)
- `safe_to_break` over scripts and template (C10)
- `environment-properties|environment_record|remembered_answers|report-adaptations|stand-identity|project_decisions` over
  docs/SIBLING_MAP.md (§4)
- `B-296|B-294|B-092|B-145` over plans/BACKLOG.md (C12)
- `git log/diff 6681ba757..HEAD` on the relied-on files (freshness)

Reruns: none (plan review; no mechanical layer; test suites are CI's per the dispatch).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "C1: project_decisions as the knowledge registry: index-pointer identity, open-only match, no states/revoke/append, markdown source - registry schema must be decided before phase 2",
    "C2: restore_config reverts story-time config writes not made by a recorded writer - the seam must write through one",
    "C4: config-keys.json asked_until_answered environment.access and project_fact/required on environment(s) force stand questions at onboarding - phase 4 must name them"
  ],
  "class_completeness": "Siblings missing from the plan's table: onboarding approvals memory (remembered_answers), asked_until_answered, report adaptations RA-n, waiver --carry-from, obligations.md and the knowledge documents, the confirmed default stand; gap-classes as the per-story twin. No SIBLING_MAP axis for answers kept across stories - one is asked for (C3).",
  "trail": {
    "read": [
      "yml-text-factory/plans/project-knowledge-plan.md",
      "wt-fbfix PKG/scripts/gate_preflight.py 909-931 3780-4040",
      "wt-fbfix PKG/scripts/environment_record.py",
      "wt-fbfix PKG/scripts/project_decisions.py",
      "wt-fbfix PKG/scripts/config_contract.py 600-700 1075-1135 1225-1470 1700-1735 2100-2300",
      "wt-fbfix PKG/scripts/hooklib.py 785-824",
      "wt-fbfix PKG/scripts/story_run.py 4270-4670 10740-10820 12880-12950",
      "wt-fbfix PKG/scripts/stand_identity.py 1-30 129-172",
      "wt-fbfix PKG/scripts/manual_capture.py 4272-4291",
      "wt-fbfix PKG/scripts/environment_selection.py 1-20",
      "wt-fbfix PKG/scripts/report_adapt.py 1-26",
      "wt-fbfix PKG/references/config-keys.json and templates/config.json and question-prices/person-owned/inject-map/install-paths",
      "wt-fbfix PKG/skills/qa-onboarding/SKILL.md and phases/p2-interview.md",
      "wt-fbfix PKG/handoffs/s9-retro-to-project.yaml",
      "wt-fbfix PKG/design/architecture.md 56-280 and factory-rules.md FR-7 FR-45 FR-59",
      "wt-fbfix DECISIONS.md D-0029 D-0032 D-0043 D-0047",
      "wt-fbfix docs/tasks/specs/t-1957-fast-manual-walker.md 234-255 443-494",
      "wt-fbfix plans/piles/thinking-roles/batch-3-parallelnost.md",
      "wt-fbfix plans/piles/onboarding-forge batch-1 batch-2",
      "wt-fbfix docs/SIBLING_MAP.md 141 413 459",
      "wt-fbfix plans/BACKLOG.md B-296"
    ],
    "reruns": []
  },
  "fixes": [
    "C1 decide the registry schema (name-keyed subject, states, provenance, revoke, append) and its base before phase 2",
    "C2 seam writes config through a recorded writer; test that a story-time fact survives restore_config",
    "C4 phase 4 names config-keys asked_until_answered/project_fact/absent_means for environment(s), dod, and the _stand_of door, both worlds",
    "C5 one key catalogue, not project-knowledge.json beside config-keys.json",
    "C6 phase 1 ask_when transitional or the <=10 ratchet moves to phase 4",
    "C7 restate the question-key claim; add a site-key to fact-key map",
    "C8 node for no-holds deferral across stages before TR3-10",
    "C9 split need() into pure state() and driver-side ask/record; reorder; onboarding answers' provenance",
    "C10 safe-direction rule for defaults; define or drop in_turn; unreachable run-scoped",
    "C11 name the login tie and merge with S6 stand_login_gate",
    "C12 rewrite phase 2.2 (B-296 stale after HF8-9)",
    "C13 role_observed provenance; owner question on voiced-add plus silence",
    "C14 comparison runs: knowledge snapshot per arm",
    "C15 one-fact end-to-end slice first; queue/carry-over lines in onboarding-forge and thinking-roles batches"
  ]
}
```
