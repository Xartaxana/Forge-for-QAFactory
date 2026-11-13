# OF3-2 (project-knowledge phase 2) — critic on the plan (t-463)

Critic (Opus), 13.11.2026. Read-only review of `docs/tasks/specs/of3-2-knowledge-phase2-spec.md` (designer draft + Lead fork decisions).
Facts were checked against the worktree `.claude/worktrees/read-main` (origin/main **fb36ae5**). Below, `P` = that worktree's
`ai-packages/qa-factory`.

**Verdict: fit_with_fixes.** The direction holds: build on the phase-0 registry, a pure `fact()` reader plus a driver-side ask half,
the conductor's scope judgment, TR3-10 moved onto the seam, the B-294 guard and the missing map axis. The plan follows §7 of the
project-knowledge plan (C1, C2, C7, C8, C9, C10), and no node starts before the plan's order allows. But the draft was written against
1dfe10a. Since then main gained the SS1-11 stand lessons in the same registry. A few of the draft's mechanics also do not work on the
current code: the K6 guard site, element rules for config-stored keys, the two-ref walk_supply row, the conductor.md byte cap, the
driver layer order, and `walk_ask_once`'s third caller. A Sonnet builder would hit STOP conditions in K1, K3, K4, K5 and K6 as
written. 19 numbered fixes follow. Of these, F-A1..F-A11 must be folded into the spec before any dispatch, and F-B1..F-B8 are smaller
spec edits.

---

## Key 1 — FACTS (section 0 and the nodes, against fb36ae5)

| fact | status | trail (read-main) |
|---|---|---|
| F-1 `RECORD_REL`, lock, `KEYS, CATALOGUE_PROBLEM = _derive_keys()`, KEYS only from `registry`/`config+registry` rows | holds, moved (:45, :46, :117; filter :107) | `P/scripts/project_knowledge.py:45-117` |
| F-2 `STATES = (KNOWN, NOT_NEEDED, NOTICED)`, `asked` reserved, SOURCES, BY | holds, moved (:119-122) | same file |
| F-3 `_latest` later-wins, no `supersedes` | holds, moved (:206-220) | same file |
| F-4 `record_problems`: stand/side keys `known` only, scope refusal | holds, moved (:619-676; known-only :634-635; scope :636-638). **New since the draft:** a `LESSONS_KEY` branch (:652-653) and a lesson door in the empty-words text (:671-672) | same file |
| F-5 `record` idempotence on state+value | holds, moved (:679-709). **Missing from the draft:** for `environments.stand_lessons`, idempotence also compares the person's WORDS (:696-700) | same file |
| F-6 `revoke` via `ER.revoke_row` | holds (:712-717) | same file |
| F-7 `value()` catalogue first, config row present -> known (placeholder reads known) | holds (:344-401; :397-398) | same file; placeholder `"not known"` at `P/references/templates/config.json:63-64` |
| F-8 `notice_from_handoff` reads `roster()` outside the lock | holds (:753-785; roster at :769, record at :775) | same file |
| F-9 catalogue section `knowledge` from :705; "78 rows"; "five registry rows" | **moved/false**: the section has **79 rows** (73 `config:`, 5 `registry`, 1 `config+registry`) and **six** registry keys: `environments.stand_lessons` (:711) was added after the draft. No row for `manual.accounts_way` / `manual.data_way` / `manual.data_way.may` exists (only top-level `manual`, :729) | `P/references/config-keys.json:705-761`; counted by a python run (below) |
| F-10 `already_answered`: body hash against one story's `driver-answers.jsonl` | holds (:381-392); **note:** it matches ANSWERED questions only. Asked-but-unanswered or deferred questions are not in it (see F-A4) | `P/scripts/driver_dialog.py:381-392, 302-314` |
| F-11 `Person` fields; no fact key | holds (driver_core.py:202-233). **Also load-bearing:** `offered` is documented as "Set by `Driver.no_move` ALONE" (:210-212); `no_hold` is an *ad-hoc attribute* row in `driver-layers.json:1118` | `P/scripts/driver_core.py:202-233` |
| F-12 `closed_question` | holds (driver_runner.py:1205) | grep |
| F-13 `deferrable` first line with the kind tuple | holds (:446-461, tuple :456) | driver_dialog.py |
| F-14 TR3-10 `walk_supply_raise` / `walk_ask_once` / `walk_asked` | holds, moved (driver_stage_s6.py:1439-1490). **Missing from the draft:** (i) `walk_supply` is ONE question over TWO facts: refs `["/manual/accounts_way", "/manual/data_way"]` (:1455), raised when `(short and not accounts.known) or (kinds and not data.known)` (:1453). (ii) `walk_ask_once` has a THIRD caller, `walk_account_raise` (:123), which opens a DD row on `/environments/<i>/credentials_by_role/<role>`. (iii) The price keys are `s6.walk_supply` and `s6.data_change` (question-prices.json:231, :241). This resolves the draft's UNVERIFIED in §2 | `P/scripts/driver_stage_s6.py:88-140, 1439-1490`; `P/scripts/driver_dispatch.py:3230-3417` |
| F-15 stand-gap `accept always` -> `environment_record.record` | not re-checked (spec says phase 3.2) | — |
| F-16 conductor-actions rows :26-29 phase-0 doors | **moved**: :26-30, and a `lesson` row was added (:29). The TR3-10 rows `walk_supply_way` / `walk_account_words` / `data_change_words` are at **:37-39** (draft says :36-38) | `P/references/conductor-actions.json:24-39` |
| F-17 `not needed` priced | not re-checked | — |
| F-19 `recorded_writes` / `_decision_writes` / `resolve` receipt (`recorded_at`, `before`) / `upsert` returns an open row of the same refs | holds (config_contract.py:2350-2414; project_decisions.py:400-432, 450-523). **Precision the draft missed:** `upsert` reuses an open row only when its refs SET EQUALS the new refs (`stored(r) == set(refs)`, :421-422). `resolve` requires a value for EVERY pointer of the row (:466-468) and assigns each value WHOLE (`_set_pointer`, :474-475) | files cited |
| F-20 `restore_config` touches `config.json` only | holds (:2498-) | config_contract.py |
| F-21 guard: regex for `project_knowledge.py (account\|role\|revoke\|side)`; `_SANCTIONED_CONFIG_SCRIPTS` with `()` | **moved, and the mechanism is misread.** The regex is at **:1789** and already covers `side\|lesson`; its refusal text is :1740-1747. The sanction table (:1902-1903) only EXEMPTS a script from the write-shape detector, and that detector fires only when the command names `config.json` as a target (`_segment_write_shape` :2105-2150; `_shell_write_shape` :2187-2201). A role running `config_contract.py --record-approval x.json` names no config path, so it passes with or without a sanction entry. See F-A6 | `P/scripts/guard_pre_tool.py:1700-1800, 1890-1910, 2105-2201` |
| F-22 main session never refused by the config guard | holds (comment :1894-1899) | same |
| F-23 install-paths carries the registry, no row for `knowledge.json` | holds (:56) | `P/references/install-paths.json:56` |
| F-24 SIBLING_MAP axes 1-36, none on "memory of a person's answer" | holds (last axis 36 at :606). Case-insensitive grep `memory of a person\|память ответа` returned nothing; positive control: the same file's `## Axis` headings were found | `docs/SIBLING_MAP.md` |
| F-25 keep rows | holds by name (all listed files are in `keep`, checked by a python read of test-layers.json). Line numbers not re-checked | `P/scripts/tests/test-layers.json` |
| F-26 phase-1 node f not on main | holds: `knowledge-read-baseline.json` is absent from `P/scripts/tests/fixtures/` (case-insensitive listing; positive control: `judgment-census.json` is listed there) | ls |
| M-1 (UNMEASURED in the draft) | **measured now**: 37 lines. Kinds: conductor 13, refusal 5, halt 4, repair_limit 3, **gate_B 2**, exit_limit 2, code_close 2, **gate_A 1**, and one each of s1_review, s1_gap, questions, stand_identity, retro. The draft's regex `[a-z_0-9]` missed the three gate lines. Conductor questions by `why_person`: none 9, access 2, gate_word 1, risk 1. Conclusion unchanged: the fixtures cannot measure what `need_fact` would save | python run below |
| M-2 (UNMEASURED) | stays unmeasured (the stand copy is outside the repo) | — |
| UNVERIFIED `take_answer` home | **verified**: `driver_machine.py:3314` (`question_sha` at :3330) | grep |
| UNVERIFIED which price keys the S6 questions use | **verified**: `s6.walk_supply`, `s6.data_change` | question-prices.json:231, :241 |
| UNVERIFIED `test_conductor_doors.py` checks rows against CLIs | it does not check CLIs. It holds the **census of question keys both ways** (`census_problems` :668-680, run at :803) and the **12000-byte cap with a 100-byte margin on conductor.md** (:31, :138-161) | `P/scripts/tests/test_conductor_doors.py` |
| UNVERIFIED `driver_dispatch.py :3271-3412` internals | verified (walk_supply_person :3270, `_resolve_decision_row` :3283, `_answer_walk_supply` :3296, data_change_person :3386, `_answer_data_change` :3397) | driver_dispatch.py |
| UNVERIFIED `artifact-writers.json` lists records; `stages.json` lists roles | not checked | — |
| UNVERIFIED `test_human_questions` holds a price-table test | not checked. The price-table test is in test_conductor_doors.py (K15, :683-) | — |
| (new) `test_config_migration.py` R1 asserts **every catalogue row has `ask_when: null` ("phase 1 fields only")** | holds. It turns red on K1's `first_need` values | `P/scripts/tests/test_config_migration.py:405-407` |
| (new) `test_project_knowledge.py` pins `list(PK.KEYS)` and the exact KEYS dict (:995-1004) and "asked is refused and skipped" (:267-275) | holds. Both turn red on K1 | test file |
| (new) `test_guard_write_owners.py` pins `_SANCTIONED_CONFIG_SCRIPTS` exactly (:815-817) | holds | test file |
| (new) `conductor.md` size | **11897 bytes; cap 12000 with a mandatory 100-byte margin** -> 3 bytes of room for K4's "one paragraph" | `wc -c`; test_conductor_doors.py:31, :161 |
| (new) driver layer order | `driver_dialog` sits BELOW `driver_dispatch` (`layers`), and `Driver.say_once` lives in `driver_dispatch` (driver-layers.json:974). Upward-edge exceptions are shrink-only | `P/scripts/tests/fixtures/driver-layers.json` |

Verdict on key 1: section 0 is mostly accurate but stale. **Material misses:** stand lessons (a sixth registry key with its own idempotence and revoke semantics); walk_supply covering two facts; the third `walk_ask_once` caller; the guard mechanism; the conductor.md cap; four pinned test expectations.

## Key 2 — ARCHITECTURE

- **AR-13 (one reader):** holds in design (`fact` / `state` / `value` / `kinds` / `contents` in one module). Risk: `fact()` re-implements head
  selection beside `state()`. The spec must say `state()`, `subjects()`, `roster()`, `lessons()` and `fact()` all go through `_heads`.
  Today `roster()` (:516-518) and `subjects()` (:413-419) carry their own later-wins loops, not `_latest`. The draft lists state,
  subjects, roster and record but not `lessons()`, and does not say that roster's and subjects' own loops are replaced -> **F-B1**.
- **AR-14 (one writer):** registry: `record` stays the one writer; `knowledge.json`: `record_kind`. Holds. But `remember` for a
  registry-stored key duplicates the dedicated doors `role` / `side` / `lesson` / `account`, which are also writers with key-specific
  shape and refusal texts: two roads to one row (also P31) -> **F-A9**.
- **AR-22 (field has producer and reader):** `safe_direction` has no runtime reader in phase 2. The caller (`walk_supply_raise`) ignores
  `while_unknown`, and no text shows it, so its only reader is the data-join test. The price key `knowledge.first_need` (K4) has no
  raising site in phase 2: `need_fact` calls `closed_question(row.question, …)` with a variable, the census scans literal sites, and
  the TR3-10 rows use `s6.*` keys. The generic `knowledge` Person kind, its take_answer branch and the F4 tokens have no phase-2
  consumer -> **F-A10**, **F-B5**.
- **AR-23 (empty outcome):** declared for kinds and contents. Not declared for: `fact()` of a `value: list` key (what `rows` holds when
  no element is named), and `remember --not-needed` on a config key (what the config gets) -> **F-A8**.
- **AR-24:** words whole; holds. But the conditional `not_needed` answer can be HIDDEN by a later `asked` row that supersedes it
  (below) -> **F-A2**.
- **AR-25 (way out):** `asked` has an exit. **Conflict:** the stated exit is "remember --supersedes or revoke". The driver side is
  silent: when `fact()` returns a conflict and the row is `first_need`, `need_fact` raises a question and writes `asked` with
  `supersedes=<head read>`, but with two heads there is no single head. If it supersedes one head, the conflict persists as
  {other answer, asked row}, and the question text never shows the two answers -> **F-A2**. **`unreachable`:** a slot only, stated,
  not built. Acceptable since phase 2 has no producer.
- **AR-28:** the adversarial list is good. Gaps: (1) a registry `known` head for a CONFIG-stored key when the config value is absent
  or a placeholder (step 3 says "a head known (registry-stored fact) -> known"; the parenthesis is the only guard and is ambiguous);
  (2) a `supersedes` cycle or a self-link written by hand; (3) an `asked` row superseding a conditional answer -> **F-A2**, **F-B2**.
- **AR-29 / P27:** holds. Scope of a free answer and a condition's applicability stay with the conductor and role. Code reads
  tokens only.
- **AR-17:** `need_fact` raises a Person, and the `# remains:` comment is required. Holds.
- **AR-16:** holds for TR3-10 if their existing builders stay (F-A3).
- **AR-20:** K3's `say_once` from `driver_dialog` is an upward edge (dialog < dispatch). It is a ratchet raise the spec says the builder
  STOPs on -> **F-A5**. K5 removes `walk_asked` / `walk_ask_once` / two state keys whose rows live in `driver-layers.json`
  (:1023, :1025, :1197), and `driver-layers.json` is not in K5's owns -> **F-B6**.
- **AR-1:** the transitional tuple is honest. K5 removes it.

## Key 3 — PRINCIPLES

- **P31 / axis 34 (one road), four places:**
  (a) `walk_account` (the third TR3-10 question) stays on the DD road while its two siblings move. K5 also deletes `walk_ask_once`,
  which `walk_account_raise` (driver_stage_s6.py:123) still calls. That is a break, not just two roads -> **F-A3**.
  (b) Lessons: today, revoking the newest lesson row revives the previous one (docstring :27-31; test E44 at
  test_project_knowledge.py:879-885). F2(a) says a revoked head does not revive. Two revoke semantics in one registry -> **F-A1**.
  (c) `remember` versus the dedicated registry doors -> **F-A9**.
  (d) The K3..K5 window: kind tuple plus catalogue road. Stated and bounded. Acceptable.
  Text-hash memory beside the registry: not two roads. The in-story hash answers "same question in this story", and the registry
  answers "between stories". C7 says so. Fine. Config write beside `remember`: the hand edit stays possible for the main session.
  F5(a) declares that a hand edit is reverted at story end, which is the honest single road. Fine.
- **P5 / FR-50:** TR3-10 facts are ones a person can give. `unreachable` is not built. Fine.
- **P9 / FR-6:** the "asked earlier" line and the aloud line are new texts a person reads. Their wording is closed by the designer
  ("Small choices"). F4 is correctly the owner's. The aloud line is a text shown to a person, so the owner should see it with F4
  -> owner question Q2.
- **P15 / FR-1 / FR-2:** K2's refusals name doors (show, kind, waiver). The guard text for `remember` / `kind` names "put it in your
  digest". Fine. Missing: the refusal text when `remember` is given a key that has a dedicated door (F-A9), and the exit-2 line wording
  when the value file is not JSON (F-A8).
- **P20 / FR-58:** the tests are written from requirements. One exception: K1 `test_supersede_and_conflict` "two writes through two
  threads -> both saved". With `supersedes=MISSING` = the head under the lock, two phase-0 writers never conflict, so the row tests
  the lock, not PK-B -> **F-A7**.
- **P22:** `need_fact` reads the registry before asking. Holds.
- **P25:** not touched.
- **FR-12:** holds (tokens only).
- **FR-13:** `holds`, `while_unknown` and `answer` are data. Holds.
- **FR-47:** holds.
- **P2:** nothing project-specific. Holds.
- **P13:** not touched.

## Key 4 — FEASIBILITY and ORDER

- **K1** is doable in one dispatch, but as written it trips its own STOP rule four times: test_config_migration R1 (`ask_when` null),
  the KEYS pin, the KEYS list inside a refusal text (`test_config_only_key_refused_with_todays_text` :1007-1012), and
  `test_asked_row_is_skipped`. It also trips the lesson revoke row E44. None of these expected edits is named, and
  `test_config_migration.py` is not owned -> **F-A11**. K1 also cannot write registry rows for the three TR3-10 keys: `_usable` needs a
  non-empty element (:201), and `record_problems` sends a non-side, non-lesson key through the ROLE rules (empty element refused, role
  form, reserved names, :654-664) -> **F-A2 (element rule)**.
- **K2** is doable. It needs the value-file format, `--not-needed` on config keys, the asked-evidence for `upsert`
  (project_decisions.py:402 refuses empty `asked`), and kind scope-change rules -> **F-A8**.
- **K3** is too big and under-specified for one Sonnet dispatch:
  - who BUILDS the Person for TR3-10 (`need_fact` with kind `knowledge`, or the existing builders with their kinds, tokens and
    executors);
  - `ask()` does not copy `fact_key` into `state["asked"]`, so the take_answer branch cannot know which fact was answered, and
    `ask()` is not in K3's owns;
  - the `say_once` layer edge;
  - the invariant that `offered` is set by `no_move` alone;
  - no test row for `need_fact` steps 3 and 5, the refusal path, or the take_answer knowledge branch.
  -> **F-A3, F-A4, F-A5, F-B3**.
- **K4** cannot add a paragraph to conductor.md: 3 bytes of room (11897/12000 with a 100-byte margin) -> **F-A10 (cap)**.
- **K5:**
  - `walk_ask_once` has a third caller;
  - walk_supply is two facts;
  - the legacy two-ref DD row is NOT reused by a one-ref `remember` (set equality), so §4's last edge ("the old open row is reused,
    never duplicated") is false for `walk_supply`;
  - stories in flight across the upgrade hold `walk_supply_asked` with a DD id and deferred items of kind `walk_supply`;
  - driver-layers rows are not owned.
  -> **F-A3, F-B6**.
- **K6:** wrong site (see key 1, F-21). The pinned dict test turns red -> **F-A6**.
- **K7:** doable as a doc dispatch.
- **Groups:**
  - G1 {K1, K6, K7}: disjoint (project_knowledge.py vs guard_pre_tool.py vs SIBLING_MAP.md).
  - G2 {K2 ‖ K3}: K2 owns `test_project_knowledge.py` and `judgment-census.json`; K3 owns neither. Disjoint by file.
  - G3 {K4}: owns conductor-actions.json and question-prices.json. K5 also owns conductor-actions.json, serial. Fine.
  - G4 {K5}: `driver_dialog.py` is shared with K3, serial. Fine.
  - **Missing:** K5 needs `driver-layers.json`, and if F-A3 is taken, also `driver_stage_s6.py:walk_account_raise`'s import of a
    kept helper.
- **Dependencies:**
  - Phase-1 node f (F10 a): right.
  - PK2-18 after K1 (F3 a): right, but PK2-18's condition "latest is absent or noticed" must be rewritten against heads. Say so in
    N-q3.
  - PK2-12 (one precedence function `_latest` + `ER.covering`, owns `environment_record.py`) collides with K1's `_heads`, which ER
    does not have. Order K1 first, then re-scope PK2-12 -> **F-B7**.
  - PK2-9 queue: present.
  - PK2-14 (merged in wave 21): `_read` now uses `read_config_file` (project_knowledge.py:225-237). No conflict.
  - OF4-19: `_context` already uses `runtime_paths.project_for_task` (:829). `remember` / `kind` must reuse `_context` /
    `_write_prologue` -> **F-B8**.
  - OF5-7 (`handoff_init --purpose`): no intersection.
  - Streams owning driver files: announced in §7. Fine.
- **Temporal windows:**
  - K1 landed alone: `asked` enters `STATES`, so `_usable` accepts hand-made `asked` rows. `roster()` would list them as elements
    with state `asked`, `subjects()` would count them, and `lessons()` would show them -> **F-A2**.
  - K4 before K5: the conductor sees both `remember` and the DD `resolve` rows for TR3-10 answers. Say which it uses in that window
    (the DD rows, until K5).
  - K5 upgrade with a story in flight -> **F-A3 (d)**.

## Key 5 — EDGES the spec's own requirements create and leave silent

1. Registry rows for config-stored one-value facts: which element (F-A2).
2. `asked` as a head: hides conditional answers, pollutes roster/subjects/lessons, and gets stuck in conflicts (F-A2).
3. The in-story "asked already" check when the `asked` write is refused (no_trace, lock): §4's claim that the hash memory covers it
   is false, because `already_answered` sees only answered questions. A deferred question would be raised again on every S6 entry
   (F-A4).
4. Conflict at `need_fact`: what the asked row supersedes, and what the person reads (F-A2).
5. `supersedes=MISSING` breaks the stated INVARIANT for every phase-0 caller and for `remember` without `--supersedes` (F-A7).
6. Lessons: revive-on-revoke and words-in-idempotence (F-A1).
7. walk_supply = two facts, with an object value merged on write (F-A3).
8. `remember`: value-file format; `--not-needed` on a config key; object pointers assigned whole (merge-on-write is the conductor's
   discipline today, conductor-actions.json:37); empty `asked` refused by `upsert` (F-A8).
9. Kind scope change with existing elements (elements would become unusable by scope mismatch); `project:<kind>` keys must be dynamic
   in `_usable` and `_form` too, not only `record_problems` (F-A8).
10. A legacy row written after a phase-2 row (an older plugin on a teammate's machine: the registry is carried and committed). It is
    not impossible. Give a deterministic rule (F-B2).
11. A `supersedes` cycle or self-link (hand edit) -> zero heads -> `unknown` with a problem (F-B2).
12. A story spanning the K5 upgrade: a legacy `walk_supply_asked` DD id, deferred items of the old kinds (F-A3).
13. The aloud line, the "asked earlier" line and the `acting on your answer` line pass `human_text.problems`. Only the second has a
    test row (F-B3).

## Key 6 — FORKS

- **F1 (a)** right (legacy rows = later-wins). Add the rule for a legacy row AFTER a phase-2 row (edge 10).
- **F2 (a)** right in principle, but it silently changes the shipped lesson behaviour (revoke the corrected lesson -> the previous one
  shows again, test E44). Either lessons follow F2 (one road; update the docstring :27-31, the revoke sentence in `cmd_revoke`, and
  E44), or the fork is re-opened. Recommendation: lessons follow F2. This is person-visible, so owner question Q3.
- **F3 (a)** right. N-q3 must restate PK2-18's guard against heads.
- **F4:** the owner's. But in phase 2 no consumer shows these tokens if TR3-10 keeps its own value tokens (F-A10): `not needed for the
  project` on "how do walkers get accounts" has no meaning beside `one at a time`. The fork may not need an answer in phase 2 at all
  -> Q1.
- **F5 (a)** right.
- **F6 (a)** right.
- **F7 (a)** right, but only if `asked` is not a head (F-A2). Otherwise an `asked` row written at raise time supersedes the person's
  conditional answer before they ever see the question.
- **F8 (a)** right.
- **F9 (a)** right. Note: walk_supply needs TWO `known` inputs (accounts.known, data.known), see F-A3.
- **F10 (a)** right.
- **F11 (a)** acceptable. It is a stored location on projects' disks, so it is hard to reverse after release. The Lead's closure is
  fine because the plan's own word is `qa-factory/knowledge.json`.
- **"Small choices I closed" that are NOT small (stored formats on projects' disks, or texts a person reads):**
  (1) `project:<name>` key namespace in the carried registry: a stored format; renaming later means migrating rows. It should be a Lead
  decision with the name rules (case fold, spaces).
  (2) `history` inside `knowledge.json`: a stored format. Also, "replaced in place" rewrites a committed file, so say whether the
  whole kind object is kept.
  (3) The aloud line's and the "asked earlier" line's wording: texts a person reads (P9). Show them to the owner with F4.
  (4) `ASKED = "asked"` as a stored state: fine (reserved since phase 0).
  (5) `person_class` values for TR3-10: shown in `driver-questions.jsonl` only. Small.

## Key 7 — TESTS

- K1: behaviour rows are good (`test_fact_toward_asking` as one parameterised set: right per docs/TESTING.md). Missing: lessons under
  F2, `asked` excluded from roster/subjects/lessons, an element rule for config-stored keys, cycles. The thread row tests the lock,
  not the conflict (F-A7).
- K2: `test_remembered_fact_survives_restore` red-first is correct (C2). Missing: value-file format, `--not-needed` on a config key,
  object pointer merge, a key with a dedicated door refused.
- K3: no row drives `need_fact` itself (steps asked_here / unknown-without-first_need / refused `asked` write still asks / conflict),
  and no row covers the take_answer knowledge branch. `test_story_run_deferred.py` is a slow CI file. Fine as a CI row, but K3 then
  has no fast local witness of its own beyond `test_human_questions.py` (F-B3).
- K4: the census row for the new price key and conductor-actions id (test_conductor_doors K15) is not named; the size cap is not named.
- K5: rows are from requirements. Add "accounts known, data unknown -> the way question is still asked" (today's behaviour, :1453) and
  "walk_account unaffected".
- K6: rows fine once the site is right. The pinned sanction dict row (test_guard_write_owners.py:815-817) is an expected edit only if
  the table changes (under F-A6 it does not).
- **FR-33:** the conductor obeying the new paragraph or row, and the person-visible re-ask line across two stories, are proven only by
  a live run. The spec does not say so -> **F-B4** (a `live-runs` row per PROJECT.md «Командная работа» 9).

## Key 8 — INTERSECTIONS

- PK2-14: merged; no conflict (above).
- PK2-18: F3 (a); restate against heads.
- PK2-12: collides with `_heads` (F-B7).
- PK2-9: queued after K6 (present).
- OF4-19: reuse `_context` (F-B8).
- OF5-7: none.
- **Census (rule 10):** the §1 table names owner and class for every altered check. Two notes:
  - `kind_problems` as a new `shape` unit and the guard as existing `safety` units: right. Under F-A6 the guard change lives in
    `human_word_check`, an existing unit, so there is no new unit.
  - `need_fact` is "not a unit", but it raises a Person, so the no-move census (`NO_MOVE_BASELINE` / `# remains:`) applies. The
    spec names the comment. Fine.
- **role-load:** the conductor is not in `references/role-load.json`. The binding cap is `test_conductor_doors.py` SIZE_CAP 12000 with
  a 100-byte margin, and `conductor-actions.json` (26999 bytes) is read on every conductor call. K4 adds one long action row and edits
  three (K5) -> **F-A10**.

---

## FIX LIST (for the Lead to fold into the spec)

### Must be folded before any dispatch

**F-A1 — §0, §3, §4, K1: stand lessons exist and share the registry.**
Add a fact row for `environments.stand_lessons` (project_knowledge.py:58-64, :437-487, :652-653, :696-700).
- K1 keeps the lesson words comparison in idempotence: "same state, value, condition AND, for a lesson, the same words".
- K1 decides lessons under F2(a): revoking the head reads `unknown`, the predecessor does not revive. K1 then owns the docstring change
  (:27-31), the `cmd_revoke` lesson sentence, and the expected edit of `test_lesson_verb_scenario` E44 (test_project_knowledge.py:879-885).
- `_heads` serves `lessons()` too.

Why: P31 (one revoke semantics per registry); otherwise the builder STOPs on E44. Trail: files above.

**F-A2 — §3 (states, heads, record_problems, fact), §4: `asked` is a marker, not an answer; one-value config facts need an element rule.**
(i) `asked` rows never take part in heads: they neither supersede nor get superseded in the answer graph. `fact()` reads "the newest
`asked` row of the subject newer than the head (or with no head)" as a separate lookup.
`_usable`-based readers that list answers (`roster`, `subjects`, `lessons`, `_account_state`) skip `asked` rows. Keep the
`test_asked_row_is_skipped` intent for roster: "an asked row never suppresses nor lifts".
(ii) On a conflict, `need_fact` asks with ONE line naming both answers (dates, stories, words cut by `person_words_whole` rules) and
writes `asked` with no link. The answer's executor (`remember`) passes `--supersedes` for each head it settles. `supersedes` becomes a
list, or `remember` is run once per head; choose one.
(iii) Element rule: a catalogue row with `value: one` uses element `""` (or a fixed `"-"`; choose one). `_usable` and `record_problems`
accept it for those keys only, and the role rules apply only to `role_form` keys.
(iv) Step 3: for a config-stored key, a registry `known` head never yields `known`. The carrier decides at step 2, and the registry row
only adds provenance. Add the adversarial row "config-stored key, registry known head, caller known=False -> unknown".

Why: AR-24/AR-25/AR-28. Without (i), an `asked` row written at raise time (F7 a) hides a conditional answer and lists `asked` roles in
the roster. Without (iii), every phase-2 row for the TR3-10 keys is refused (project_knowledge.py:201, :654-664).

**F-A3 — K3, K5: who builds the TR3-10 Person; walk_supply is two facts; walk_account; the legacy DD row; stories in flight.**
Direction: `need_fact(key, …, build)` only does the bookkeeping (fact read, `asked` write, the in-story check, the "asked earlier"
line handed to `build`). The existing builders (`walk_supply_person` / `data_change_person`) keep their kinds, texts, price keys
(`s6.walk_supply`, `s6.data_change`) and executors, and set `fact_key` + `no_hold`. Then:
- (a) `walk_supply` asks when EITHER `manual.accounts_way` OR `manual.data_way` is unknown, as today (:1453). K5 calls `fact()` for
  both, with known from `accounts.known` / `data.known`, and records `asked` on both.
- (b) `walk_ask_once` STAYS for `walk_account_raise` (:123) until a later node moves the account question. K5 deletes only the supply
  callers' use of it. The remainder is queued with an owner (P31 residual as a node, rule 19).
- (c) The answer executors write through `remember` with the SAME refs as any legacy open row, so `upsert` returns it (refs set
  equality, project_decisions.py:421-422). For walk_supply that means one `remember` call writing two pointers, or `_resolve_decision_row`
  kept with an extra registry write; choose one. Correct §4's last edge, which is false for the two-ref row.
- (d) A story in flight across the upgrade: `state["walk_supply_asked"]` / `["data_change_asked"]` with a DD id and deferred items of
  those kinds are answered by the same executors. State it, with a test row.

Why: today's behaviour (accounts known, data unknown -> asked) would be lost; K5 would break `walk_account_raise`; the "reused" edge is
false. Trail: driver_stage_s6.py:88-140, :1445-1490; driver_dispatch.py:3270-3417.

**F-A4 — §4 edge "asked row in a no_trace story", K3: the in-story guard must not depend on the registry write.**
`already_answered` sees only answered questions (driver_dialog.py:381-392). Keep an in-story record (a state key `knowledge_asked:
{fact_key: at}` or the deferred items by `fact_key`) that `need_fact` checks before `fact()`. A refused `asked` write (no_trace,
lock) then still never raises the question twice in one story. Add a test row: "no_trace story, two S6 entries -> one deferred
item". Correct the §4 sentence.

**F-A5 — K3: layer order and the `offered` invariant.**
`need_fact` lives in `driver_dialog` (below `driver_dispatch`), so it may not call `say_once` (driver-layers.json:974; upward edges
are shrink-only, AR-20). Either home `need_fact` in `driver_dispatch`, or return the acting line to the caller to print. Choose the
first; it matches `say_once`'s home rule. Also: under F-A3, `need_fact` sets no `offered`, so the documented invariant
"`offered` set by `no_move` ALONE" (driver_core.py:210-212) holds. If K3 keeps a generic knowledge Person, that invariant comment and
`ask()`'s seam branch (driver_dialog.py:321-333) are owned edits and must be named. Also K3 owns `ask()` if `fact_key` must reach
`state["asked"]`. Under F-A3 it does not need to: the kind's own executor knows its fact.

**F-A6 — K6: wrong mechanism for B-294 (a).**
The sanction table only exempts a script from a detector that fires on a `config.json` target word (guard_pre_tool.py:2187-2201), so
changing `()` refuses nothing. Put `config_contract.py --record-approval|--apply` and `onboard_apply.py --apply` into
`human_word_check`, in the same shape as the existing doors (:1771-1797): the flag as a whole option `(?![\w-])`, matched on the exec
part. Add one refusal sentence each to the text at :1700-1747, and leave the sanction table and its pin (test_guard_write_owners.py:
815-817) unchanged. Correct the stale line numbers (:1787 -> :1789, :1740-1745 -> :1740-1747). The regex already holds `side|lesson`;
K6 adds `remember|kind`. Note that onboarding is a skill in the main session (no `qa-onboarding` agent in `P/agents/`), so refusing
roles does not block onboarding.

**F-A7 — §3 INVARIANT and K1 tests: state where the PK-B race is caught.**
With `supersedes=MISSING` = the head under the lock, every phase-0 CLI and `remember` without `--supersedes` silently supersede, which
contradicts "the later one never wins silently". Scope the invariant honestly: "a writer that names the head it read". Make the
knowledge answer path name it: the executor passes the head recorded when the question was asked, so a person who answered on the
basis of an old head creates a conflict, not a silent overwrite. Replace the thread row with: "head changed between ask and answer ->
conflict, both heads listed".

**F-A8 — §3 `remember` / kinds, §4, K2: silent edges.**
State:
- (a) `--value-file` holds JSON; a non-JSON or empty file is refused, exit 2, with the door.
- (b) `--not-needed` on a config-stored key writes NO config value, only a registry `not_needed` row (the config keeps its placeholder,
  which is why `fact()` reads the registry at step 3).
- (c) an object pointer is assigned whole by `resolve`; `remember` merges the given keys into the current object (moving the
  "MERGE ON WRITE" rule from the conductor's discipline into code — one road), or refuses an object value. Choose merge.
- (d) the `asked` evidence passed to `upsert` (project_decisions.py:402 refuses empty) = the person's words file's first line, or
  "recorded by the conductor in <story>".
- (e) a kind's `scope` cannot change while it has live elements (refused, with door `revoke` the elements first).
- (f) `project:<kind>` keys are resolved dynamically in `_usable`, `_form`, `record_problems` and `subjects`, not only in
  `record_problems`.

**F-A9 — K2, K4: `remember` must not be a second road to keys that have a door.**
For `product.roles`, `environments.credentials_by_role`, the three side keys and `environments.stand_lessons`, `remember` refuses and
names the dedicated command (role / account / side / lesson). `remember` serves the other catalogued keys and `project:<kind>`.
Test row in `test_remember_roads`. (P31 / axis 34, AR-14.)

**F-A10 — K3, K4, §2: phase 2 builds only what has a consumer, and the conductor text must fit its cap.**
(i) Under F-A3, the generic Person kind `knowledge`, its take_answer branch, the price key `knowledge.first_need` and the F4 tokens
have no phase-2 consumer (AR-22; the K15 census at test_conductor_doors.py:668-680, :803 would flag a data row no site raises). Move
them to phase 3, where gate A keys are the first generic consumer, or list `knowledge.first_need` in `AWAITING_ITS_SITE`. Choose:
move to phase 3. The owner's F4 then also waits for phase 3 (Q1).
(ii) conductor.md is 11897/12000 bytes with a 100-byte margin (test_conductor_doors.py:31, :161). K4's paragraph must go into the
`remember` action row of conductor-actions.json (already read on every call), or K4 must free equal bytes in conductor.md. Name which,
and add the size row to K4's DoD.

**F-A11 — K1 owns and DoD: name the expected test edits.**
K1 adds to its owns `P/scripts/tests/test_config_migration.py` (the R1 row "null ask_when, phase 1 fields only", :405-407 becomes
"`ask_when` is null or one of the phase's values, and a `first_need` row carries its seam fields"). It names as expected edits:
`test_keys_are_derived_from_the_catalogue_in_todays_order` (:995-1004), `test_config_only_key_refused_with_todays_text` (:1007-1012),
`test_asked_row_is_skipped` (:267-275), lesson E44 (F-A1). It also updates the `about` text of `config-keys.json` (line 2: "ask_when
(null until the phase that asks)", "for a registry row scope and compare"). Correct §5's "Existing phase-0 rows stay green unchanged".

### Smaller spec edits

**F-B1 — §3:** say that `_heads` replaces the own later-wins loops of `roster()` (:516-518) and `subjects()` (:413-419) and serves
`lessons()` (:476). Otherwise four precedence rules remain (AR-13).

**F-B2 — §4:** add a legacy row after a phase-2 row (same F1 rule, by time), and a `supersedes` cycle or self-link (zero heads ->
`unknown` + problem) to the adversarial set.

**F-B3 — K3 tests:** rows that drive `need_fact` (asked_here no question; no `first_need` -> caller keeps today's road; refused write
still asks once; conflict line). Put them in `test_walk_supply.py` (K5-owned, so serial) or another fast keep file K3 owns. Name it.
Every new text (acting line, asked-earlier line) passes `human_text.problems` (test_human_questions.py row).

**F-B4 — Every node with a person-visible or conductor-text change (K3, K4, K5):** a `live-runs` row: "two stories on one project:
story 2 is not asked; an unanswered ask comes back with the earlier line; the conductor records a free answer through `remember` and
says the line" (FR-33).

**F-B5 — §2:** `safe_direction`: name its runtime reader (e.g. the `acting`/default note the caller prints), or mark it as
documentation for the conductor with the data-join test as its only reader. Under AR-22, say which.

**F-B6 — K5 owns:** add `P/scripts/tests/fixtures/driver-layers.json`: rows :1023 (`walk_asked`), :1197 (`walk_supply_asked`) and its
data_change twin, :1118 (`no_hold` ad-hoc row, once K3 makes it a formal attribute). Keep :1025 under F-A3 (b). K3 owns the :1118
change if it formalises `no_hold`.

**F-B7 — §5 dependencies:** order K1 before PK2-12 and add a line to PK2-12 (project-knowledge batch-2 :32): "one precedence = `_heads`
(supersedes-aware); `ER.covering` keeps later-wins for the environment record, or gains heads — decide at PK2-12". Otherwise PK2-12
re-merges K1's heads into a later-wins helper.

**F-B8 — K2:** `cmd_remember` / `cmd_kind` reuse `_context` / `_write_prologue` (project_knowledge.py:811-857), so the story-to-project
resolution stays `runtime_paths.project_for_task` (OF4-19's survivor).

## QUESTIONS FOR THE OWNER (plain words, with options)

- **Q1 (F4, may be postponed).** In this phase the only questions that move onto the new road are the two about walkers' accounts and
  records. Their answers are already choices ("the app makes them", "one at a time", …). Should the "not needed now / for this stand /
  for the project" answers appear on them?
  - (a) No: those answers come with the first general questions in the next phase, and F4 is decided then. Recommended.
  - (b) Yes, add them to the two walker questions now.
  - (c) Decide the words now, use them later.
- **Q2 (texts you will read).** After the conductor records your free answer, it will say one line, e.g. "recorded as a rule of the
  project: <your words>; to undo, say so". A question asked again in a later story gets the line "I asked this in <story> on <date> and
  got no answer then." Are these wordings right?
  - (a) Yes.
  - (b) Change them (give your words).
- **Q3 (lessons you taught about a stand).** Today, if you correct a lesson and then take the correction back, the old lesson comes back
  by itself. The new rule for all answers is that a taken-back answer does not bring the older one back; the factory asks again.
  - (a) Same rule for lessons: taking back removes it. Recommended: one rule everywhere.
  - (b) Lessons keep bringing the older one back.

## QUEUE (not for this phase)

- Q-1: move the `walk_account` question onto the seam (its fact is `environments.credentials_by_role`, phase 0's account road). P31
  residual from F-A3 (b). Owner: Lead of onboarding-forge batch 3, phase 3 node.
- Q-2: the generic knowledge question (Person kind, take_answer branch, F4 tokens, `knowledge.first_need`) with the first gate-A key
  consumer (phase 3.1), if F-A10 (i) is taken.
- Q-3: N-q1..N-q3 as drafted; N-q3 restated against heads (F3).

## What I did not check

- `references/artifact-writers.json` (whether records are listed) and `references/stages.json` (roles by name): left UNVERIFIED as the
  draft says.
- F-15 (stand-gap words, `stand_gaps.record_lasting`), F-17, F-18: not re-read.
- `test-layers.json` line numbers: rows are confirmed by name only.
- `driver_machine.take_answer` body (branch order at :3314+): not read. The position statement in K3 is not verified against the
  current branch order.
- `brief_pack.person_words_whole` existence: not checked.
- M-2: unmeasured (stand copy outside the repo).
- The plan's earlier sections 1-3 in full: read §4 phase 2 and §5-§7 only.

## Trail

Read on read-main (fb36ae5):
- `P/scripts/project_knowledge.py:1-830`
- `P/scripts/driver_dialog.py:265-535`
- `P/scripts/driver_core.py:192-245`
- `P/scripts/driver_stage_s6.py:88-140, 1435-1500`
- `P/scripts/driver_dispatch.py:3225-3420`
- `P/scripts/project_decisions.py:400-523`
- `P/scripts/config_contract.py:776-800, 2350-2560`
- `P/scripts/guard_pre_tool.py:1730-1800, 1890-1915, 2105-2215`
- `P/references/conductor-actions.json:24-39`
- `P/references/config-keys.json` (knowledge section)
- `P/references/templates/config.json:63-67`
- `P/references/role-load.json:1-40`
- `P/scripts/tests/test_project_knowledge.py:260-300, 846-905, 995-1035`
- `P/scripts/tests/test_config_migration.py:365-415`
- `P/scripts/tests/test_conductor_doors.py:1-30, 138-161, 660-810`
- `P/scripts/tests/test_guard_write_owners.py:800-840`
- `P/scripts/tests/fixtures/driver-layers.json` (layers, adhoc_attributes, rows :147, :209, :214, :558, :563, :974, :1023-1033, :1118, :1197)
- `P/scripts/tests/fixtures/judgment-census.json:783-784`
- `P/design/state-exits.md` (grep)
- `plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md:18-45`
- `plans/piles/onboarding-forge/batch-3…md:27-30`, `batch-4…:49`, `batch-5…:34`
- `plans/piles/gates-and-words/findings/B-294-…md`
- `docs/SIBLING_MAP.md` (axis headings)
- `plans/project-knowledge-plan.md:200-367`
- the spec in full

Runs:
- (1) Catalogue count: `python -B -c "...len(k)...Counter(store)..." config-keys.json` -> `79`,
  `Counter({'config': 73, 'registry': 5, 'config+registry': 1})`, no `manual.*` sub-rows; scoped rows = the six registry keys incl.
  `environments.stand_lessons`.
- (2) M-1: `python -B -c "...driver-questions.jsonl..."` -> `37`; kinds conductor 13, refusal 5, halt 4, repair_limit 3, gate_B 2,
  exit_limit 2, code_close 2, s1_review/s1_gap/questions/gate_A/stand_identity/retro 1; conductor by why_person: None 9, access 2,
  gate_word 1, risk 1.
- (3) `wc -c conductor.md conductor-actions.json` -> `11897`, `26999`.
- (4) test-layers keep membership read by python: all named files in `keep`.

Searches with positive controls:
- `walk_ask_once(` across driver files: found :123, :1455, :1461 (control: the def at :1466).
- `memory of a person|память ответа` -i in SIBLING_MAP: none (control: `## Axis` headings found).
- `knowledge` -i in the fixtures listing: none (control: judgment-census.json listed).
- `--record-approval` over the package: script and skill hits only (control: config_contract.py:2980 found).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "F-A1 stand lessons share the registry: idempotence by words and revive-on-revoke conflict with F2 (a); test E44 and the docstring are unnamed",
    "F-A2 asked rows as heads hide conditional answers, pollute roster/subjects/lessons, and stick conflicts; config-stored one-value keys cannot be written (element and role rules)",
    "F-A3 TR3-10: walk_supply is two facts; walk_ask_once has a third caller (walk_account_raise :123); a legacy two-ref DD row is not reused by a one-ref upsert; in-flight stories unstated",
    "F-A4 in-story re-ask guard depends on the registry write; already_answered sees only answered questions",
    "F-A5 need_fact in driver_dialog calling say_once (driver_dispatch) is an upward layer edge (AR-20, shrink-only)",
    "F-A6 K6 edits the sanction table, which refuses nothing; the role door belongs in human_word_check",
    "F-A7 the supersedes MISSING default contradicts the stated no-silent-later-wins invariant; the thread test tests the lock",
    "F-A8 remember edges: value-file format, not-needed on config keys, whole-object assignment, upsert asked evidence, kind scope change, dynamic project keys",
    "F-A9 remember duplicates the role/account/side/lesson doors (P31)",
    "F-A10 the generic knowledge Person, price key and F4 tokens have no phase-2 consumer (census red); conductor.md has 3 bytes of room under its cap",
    "F-A11 K1 trips unnamed pinned tests (test_config_migration R1 null ask_when, the KEYS pin, the asked-skipped row) and does not own test_config_migration.py"
  ],
  "class_completeness": "Axis 34 (one road): walk_account left on the DD road while K5 removes its helper (F-A3 b, queued Q-1); remember vs the dedicated doors (F-A9); lessons revoke semantics (F-A1). Axis 16/13 (one reader): roster/subjects/lessons keep their own precedence loops unless F-B1. Axis 5: only S6 consumers in phase 2, stated. New axis 37 (K7) must list lessons (environment-stand lessons, SS1-11) among the carriers. PK2-12 precedence merge collides with _heads (F-B7). No scan beyond the map was done.",
  "trail": {
    "read": [
      "docs/tasks/specs/of3-2-knowledge-phase2-spec.md",
      "plans/project-knowledge-plan.md:200-367",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/project_knowledge.py:1-830",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/driver_dialog.py:265-535",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/driver_core.py:192-245",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/driver_stage_s6.py:88-140,1435-1500",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/driver_dispatch.py:3225-3420",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/project_decisions.py:400-523",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/config_contract.py:776-800,2350-2560",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/guard_pre_tool.py:1730-1800,1890-1915,2105-2215",
      ".claude/worktrees/read-main/ai-packages/qa-factory/references/conductor-actions.json:24-39",
      ".claude/worktrees/read-main/ai-packages/qa-factory/references/config-keys.json (knowledge section)",
      ".claude/worktrees/read-main/ai-packages/qa-factory/references/templates/config.json:63-67",
      ".claude/worktrees/read-main/ai-packages/qa-factory/references/role-load.json",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/tests/test_project_knowledge.py:260-300,846-905,995-1035",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/tests/test_config_migration.py:365-415",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/tests/test_conductor_doors.py:1-30,138-161,660-810",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/tests/test_guard_write_owners.py:800-840",
      ".claude/worktrees/read-main/ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json (layers, adhoc_attributes, named rows)",
      ".claude/worktrees/read-main/plans/piles/project-knowledge/batch-2-usloviya-zamena-oglavlenie.md:18-45",
      ".claude/worktrees/read-main/plans/piles/gates-and-words/findings/B-294-odobreniya-konfiga-b-220-kritik-t-380-dyra.md",
      ".claude/worktrees/read-main/docs/SIBLING_MAP.md (axis headings)"
    ],
    "reruns": [
      {"command": "python -B -c (count knowledge rows and stores in config-keys.json)", "result": "79 rows; config 73, registry 5, config+registry 1; no manual.* sub-rows; six scoped registry keys incl. environments.stand_lessons"},
      {"command": "python -B -c (M-1 kinds of local-1-arm-b driver-questions.jsonl)", "result": "37 lines; conductor 13 (why_person None 9, access 2, gate_word 1, risk 1), refusal 5, halt 4, repair_limit 3, gate_B 2, exit_limit 2, code_close 2, gate_A 1, s1_review 1, s1_gap 1, questions 1, stand_identity 1, retro 1"},
      {"command": "wc -c references/conductor.md references/conductor-actions.json", "result": "11897 and 26999 bytes; cap 12000 with 100-byte margin (test_conductor_doors.py:31,:161)"}
    ]
  },
  "fixes": [
    "F-A1 lessons under F2 (a): keep words in idempotence, name E44 and the docstring/revoke-sentence edits, _heads serves lessons()",
    "F-A2 asked is a marker outside heads; answer-listing readers skip it; conflict asks with both answers and writes asked unlinked; element rule for value:one keys; a registry known head never makes a config-stored key known",
    "F-A3 need_fact(build) bookkeeping only; existing builders keep kinds, price keys s6.walk_supply/s6.data_change and executors; walk_supply over both facts; walk_ask_once kept for walk_account (queue Q-1); same refs as the legacy DD row; in-flight stories stated",
    "F-A4 in-story asked record independent of the registry write; test with a no_trace story and two S6 entries",
    "F-A5 home need_fact in driver_dispatch (or return the line); the offered-by-no_move-alone invariant kept; ask() not edited under F-A3",
    "F-A6 B-294 (a) via human_word_check regexes plus refusal sentences; sanction table and its pin unchanged; line numbers corrected",
    "F-A7 scope the invariant to writers that name the head read; the answer path passes the head recorded at ask time; replace the thread row with a head-changed-between-ask-and-answer row",
    "F-A8 remember: JSON value file, not-needed writes no config, merge objects in code, upsert asked evidence, no kind scope change with live elements, dynamic project keys in _usable/_form/subjects",
    "F-A9 remember refuses keys with a dedicated door, naming it",
    "F-A10 move the generic knowledge Person/price key/F4 tokens to phase 3; K4 text goes into the conductor-actions row, or free bytes in conductor.md; size row in the DoD",
    "F-A11 K1 owns test_config_migration.py; name the pinned test edits and the config-keys about text",
    "F-B1 _heads replaces roster/subjects loops and serves lessons",
    "F-B2 legacy-after-phase-2 row and supersedes cycle edges",
    "F-B3 K3 fast test rows driving need_fact; new texts through human_text.problems",
    "F-B4 live-runs rows for K3/K4/K5 (FR-33)",
    "F-B5 name the runtime reader of safe_direction or mark it documentation",
    "F-B6 K5 owns driver-layers.json rows; K3 owns the no_hold ad-hoc row change",
    "F-B7 order K1 before PK2-12 and restate PK2-12 against heads",
    "F-B8 remember/kind reuse _context/_write_prologue"
  ]
}
```
